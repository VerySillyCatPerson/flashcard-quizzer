"""CLI composition, expected failure handling, and independent finalization."""

import argparse
from dataclasses import dataclass
from pathlib import Path
from random import Random
from typing import Mapping, Sequence

from utils import terminal
from utils.data_loader import FlashcardLoadError, load_flashcards
from utils.engine import QuizSession
from utils.history import HistorySaveError, HistoryStore, default_history_path
from utils.models import FinishReason, Flashcard
from utils.paths import (
    PathConflictError,
    PathValidationError,
    QuizPaths,
    validate_paths,
)
from utils.results_export import ResultsExportError, export_results
from utils.strategies import (
    AdaptiveStrategy,
    QuizStrategy,
    RandomStrategy,
    SequentialStrategy,
)


@dataclass(frozen=True)
class _Options:
    """Converted argument values; argparse owns validation of flags and choices."""

    mode: str
    deck: Path
    history: Path | None
    export: Path | None
    seed: int | None
    overwrite: bool


def _parser() -> argparse.ArgumentParser:
    """Describe the public flags without reading a deck or user profile."""
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="Quiz JSON flashcards in sequential, random, or adaptive order.",
        epilog=(
            "History saves at session end or orderly interruption. "
            "Forced termination may lose updates; concurrent sessions are not merged."
        ),
    )
    parser.add_argument(
        "-f", "--file", type=Path, required=True, help="UTF-8 JSON deck"
    )
    parser.add_argument(
        "-m",
        "--mode",
        choices=("sequential", "random", "adaptive"),
        default="sequential",
        help="quiz order (default: sequential)",
    )
    parser.add_argument(
        "--history",
        type=Path,
        help="history file (default: ~/.flashcard_quizzer/history.json)",
    )
    parser.add_argument(
        "--seed", type=int, help="reproducible seed, only with --mode random"
    )
    parser.add_argument(
        "--export",
        type=Path,
        help="optional JSON metadata/statistics/misses file (refuses existing files)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="atomically replace an existing --export file; history is unaffected",
    )
    return parser


def _strategy(options: _Options, scores: Mapping[str, int]) -> QuizStrategy:
    """Select implementations outside the engine, including controlled randomness."""
    if options.mode == "sequential":
        return SequentialStrategy()
    if options.mode == "random":
        return RandomStrategy(Random(options.seed))
    return AdaptiveStrategy(scores)


def _prepare_paths(options: _Options) -> QuizPaths:
    """Obtain the default history location only after flags have been validated."""
    history = options.history
    if history is None:
        try:
            history = default_history_path()
        except (OSError, RuntimeError) as failure:
            raise PathValidationError(
                f"Could not locate the default history file: {failure}"
            ) from failure
    return validate_paths(options.deck, history, options.export)


def _finalize(
    session: QuizSession,
    cards: Sequence[Flashcard],
    history: HistoryStore,
    paths: QuizPaths,
    options: _Options,
    reason: FinishReason,
    input_detail: str | None,
) -> int:
    """Resume pending phases; never retry a write with an uncertain outcome.

    Advance before calling each side effect. Read-only preparation stays pending
    on interruption; a started write is attempted at most once during this run.
    """
    phase = "display"
    failed = False
    interrupted = reason == "interrupted"
    messages: list[str] = []
    while True:
        try:
            summary = session.summary
            failed = failed or history.load_error is not None
            if phase == "display":
                phase = "history"
                terminal.show_summary(summary, cards, reason, input_detail)
            if phase == "history":
                can_save = history.can_save
                phase = "export"
                if can_save:
                    try:
                        history.save_session(summary)
                    except HistorySaveError as failure:
                        failed = True
                        messages.append(f"{failure}. Learning updates were not saved.")
                    except KeyboardInterrupt:
                        interrupted = True
                        reason = "interrupted"
                        messages.append(
                            "History saving was interrupted; persistence is not "
                            "confirmed. It will not be retried during this run."
                        )
            if phase == "export":
                export_path = paths.export
                phase = "warnings"
                if export_path is not None:
                    try:
                        export_results(
                            export_path,
                            summary,
                            cards,
                            options.mode,
                            options.seed,
                            reason,
                            overwrite=options.overwrite,
                        )
                    except ResultsExportError as failure:
                        failed = True
                        messages.append(str(failure))
                    except KeyboardInterrupt:
                        interrupted = True
                        reason = "interrupted"
                        messages.append(
                            "Results export was interrupted; output is not confirmed. "
                            "It will not be retried during this run."
                        )
            while messages:
                terminal.warn(messages.pop(0))
            if interrupted:
                return 130
            return 1 if failed or reason != "completed" else 0
        except KeyboardInterrupt:
            interrupted = True
            reason = "interrupted"
            messages.append(
                "Interrupted by Ctrl+C during finalization; pending work will continue."
            )
        except terminal.TerminalOutputError as failure:
            failed = True
            if phase != "warnings":
                messages.append(str(failure))


def _execute(options: _Options, paths: QuizPaths, cards: list[Flashcard]) -> int:
    """Load history, run external terminal interaction, and finalize once."""
    history = HistoryStore(paths.history)
    if history.load_error is not None:
        terminal.warn_history(history.load_error)
    session = QuizSession(cards, _strategy(options, history.scores))
    reason: FinishReason = "completed"
    input_detail: str | None = None
    try:
        reason = terminal.play(session)
    except KeyboardInterrupt:
        reason = "interrupted"
    except terminal.TerminalInputError as failure:
        reason = "input_error"
        input_detail = str(failure)
    except terminal.TerminalOutputError as failure:
        reason = "output_error"
        input_detail = str(failure)
    return _finalize(session, cards, history, paths, options, reason, input_detail)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI; argparse owns help/usage exits, this function owns run status."""
    try:
        terminal.configure_streams()
        parser = _parser()
        args = parser.parse_args(list(argv) if argv is not None else None)
        options = _Options(
            args.mode, args.file, args.history, args.export, args.seed, args.overwrite
        )
        if options.seed is not None and options.mode != "random":
            parser.error("--seed requires --mode random")
        if options.overwrite and options.export is None:
            parser.error("--overwrite requires --export")
        try:
            paths = _prepare_paths(options)
        except PathConflictError as failure:
            parser.error(str(failure))
        except PathValidationError as failure:
            terminal.error(str(failure))
            return 1
        try:
            cards = load_flashcards(paths.deck)
        except FlashcardLoadError as failure:
            terminal.error(str(failure))
            return 1
        return _execute(options, paths, cards)
    except KeyboardInterrupt:
        try:
            terminal.warn("Interrupted by Ctrl+C before quiz finalization.")
        except terminal.TerminalOutputError:
            pass
        return 130
    except terminal.TerminalOutputError:
        return 1
