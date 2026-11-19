"""Interactive prompts, feedback, warnings, and summary rendering for the CLI."""

import os
import sys
from io import TextIOWrapper
from typing import Sequence

from utils.engine import QuizSession
from utils.history import HistoryLoadError
from utils.models import FinishReason, Flashcard, SessionSummary


class TerminalInputError(Exception):
    """Input could not be read; completed answers remain available for saving."""


class TerminalOutputError(Exception):
    """Terminal output failed; presentation must not prevent finalization."""


def _write(message: str, *, error_stream: bool = False) -> None:
    """Translate expected write errors only, leaving formatting bugs visible."""
    stream = sys.stderr if error_stream else sys.stdout
    try:
        print(message, file=stream, flush=True)
    except (OSError, UnicodeError) as failure:
        if isinstance(stream, TextIOWrapper):
            # Retire a failed native descriptor so shutdown cannot flush it again
            # and override our exit status. Existing buffered text is discarded.
            try:
                with open(os.devnull, "w", encoding="utf-8") as sink:
                    os.dup2(sink.fileno(), stream.fileno())
            except (OSError, ValueError):
                pass
        raise TerminalOutputError(
            f"Could not write terminal output: {failure}"
        ) from failure


def configure_streams() -> None:
    """Use UTF-8 for native CLI streams; tolerate unencodable display values."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if isinstance(stream, TextIOWrapper):
            stream.reconfigure(
                encoding="utf-8",
                errors="strict" if stream is sys.stdin else "backslashreplace",
            )


def _one_line(value: str) -> str:
    """Escape line controls for display without changing stored/comparison text."""
    return value.translate({ord("\n"): r"\n", ord("\r"): r"\r", ord("\t"): r"\t"})


def warn(message: str) -> None:
    """Display an operational warning on stderr."""
    _write(f"Warning: {message}", error_stream=True)


def error(message: str) -> None:
    """Display an expected pre-session failure without a traceback."""
    _write(f"Error: {message}", error_stream=True)


def warn_history(failure: HistoryLoadError) -> None:
    """Explain every agreed degraded-history effect and the affected file/cause."""
    warn(
        "Previous scores could not be loaded. Adaptive mode will use deck order. "
        "Learning updates will not be saved during this run. "
        f"History '{failure.path}': {failure.detail}"
    )


def play(session: QuizSession) -> FinishReason:
    """Obtain input externally to the engine and return on completion or EOF.

    KeyboardInterrupt deliberately propagates to CLI orchestration so completed
    answers can be finalized with status 130. Input errors are classified only
    at the input operation; grading/programming errors are not swallowed.
    """
    while (card := session.current_card) is not None:
        snapshot = session.summary
        _write(
            f"\n[{snapshot.answered_count + 1}/{snapshot.deck_size}] "
            f"{_one_line(card.front)}"
        )
        try:
            answer = input("Answer: ")
        except EOFError:
            return "eof"
        except (OSError, UnicodeError) as failure:
            raise TerminalInputError(f"Could not read answer: {failure}") from failure
        result = session.submit_answer(answer)
        _write(
            (
                "Correct"
                if result.correct
                else f"Incorrect. Expected: {_one_line(result.card.back)}"
            )
        )
    return "completed"


def format_summary(
    summary: SessionSummary, cards: Sequence[Flashcard], reason: FinishReason
) -> str:
    """Render a table using completed-answer accuracy and original card positions."""
    positions = {card.card_id: index for index, card in enumerate(cards, start=1)}
    missed = (
        "; ".join(
            f"#{positions[card.card_id]} {_one_line(card.front)}"
            for card in summary.missed_cards
        )
        or "None"
    )
    accuracy = (
        "N/A"
        if summary.accuracy_percent is None
        else f"{summary.accuracy_percent:.2f}%"
    )
    rows = [
        ("Deck size", str(summary.deck_size)),
        ("Total questions", str(summary.answered_count)),
        ("Correct", str(summary.correct_count)),
        ("Accuracy", accuracy),
        ("Missed terms", missed),
    ]
    label_width = max(len(label) for label, _ in rows)
    value_width = max(len(value) for _, value in rows)
    border = f"+-{'-' * label_width}-+-{'-' * value_width}-+"
    title = "Completed session" if summary.is_complete else "Partial session"
    lines = [f"{title} ({reason})", border]
    lines.extend(
        f"| {label:<{label_width}} | {value:<{value_width}} |" for label, value in rows
    )
    lines.append(border)
    return "\n".join(lines)


def show_summary(
    summary: SessionSummary,
    cards: Sequence[Flashcard],
    reason: FinishReason,
    input_detail: str | None = None,
) -> None:
    """Print the table and explain orderly interruption on the error stream."""
    _write("\n" + format_summary(summary, cards, reason))
    if reason == "eof":
        warn("Input ended before the quiz was complete (EOF).")
    elif reason == "interrupted":
        warn("Interrupted by Ctrl+C.")
    elif reason == "input_error":
        warn(input_detail or "Could not read answer.")
    elif reason == "output_error":
        warn(input_detail or "Could not display quiz output.")
