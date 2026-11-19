"""Versioned JSON result export, independent of terminal output and history."""

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Sequence

from utils.models import FinishReason, Flashcard, SessionSummary


class ResultsExportError(Exception):
    """A requested result file could not be written."""

    def __init__(self, path: Path, detail: str) -> None:
        """Retain structured destination/error data for terminal presentation."""
        self.path = path
        self.detail = detail
        super().__init__(f"Cannot export results to '{path}': {detail}")


def results_document(
    summary: SessionSummary,
    cards: Sequence[Flashcard],
    mode: str,
    seed: int | None,
    reason: FinishReason,
) -> dict[str, object]:
    """Build session metadata/statistics and missed cards, without submitted text."""
    positions = {card.card_id: index for index, card in enumerate(cards, start=1)}
    return {
        "version": 1,
        "mode": mode,
        "seed": seed,
        "finish_reason": reason,
        "complete": summary.is_complete,
        "deck_size": summary.deck_size,
        "answered_count": summary.answered_count,
        "correct_count": summary.correct_count,
        "accuracy_percent": summary.accuracy_percent,
        "missed": [
            {
                "position": positions[card.card_id],
                "card_id": card.card_id,
                "front": card.front,
                "expected": card.back,
            }
            for card in summary.missed_cards
        ],
    }


def _require_absent(path: Path) -> None:
    """Refuse existing path entries, including dangling links, before staging."""
    try:
        path.lstat()
    except FileNotFoundError:
        return
    except OSError as failure:
        raise ResultsExportError(
            path, f"Could not inspect export destination: {failure}"
        ) from failure
    raise ResultsExportError(
        path, "Export already exists; use --overwrite to replace it."
    )


def export_results(
    path: Path,
    summary: SessionSummary,
    cards: Sequence[Flashcard],
    mode: str,
    seed: int | None,
    reason: FinishReason,
    *,
    overwrite: bool = False,
) -> None:
    """Publish complete JSON without replacing a file unless explicitly allowed.

    An exclusive hard-link publication prevents a late-arriving destination from
    being overwritten after the initial absence check. Authorized replacement
    uses atomic os.replace. Unsupported exclusive publication fails safely.
    """
    if not overwrite:
        _require_absent(path)
    document = results_document(summary, cards, mode, seed, reason)
    try:
        content = (
            json.dumps(document, indent=2, ensure_ascii=True, allow_nan=False) + "\n"
        )
    except ValueError as failure:
        raise ResultsExportError(
            path, f"Could not encode results: {failure}"
        ) from failure
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        if overwrite:
            os.replace(temporary_path, path)
        else:
            os.link(temporary_path, path)
            temporary_path.unlink()
    except OSError as failure:
        detail = (
            "Export already exists; use --overwrite to replace it."
            if isinstance(failure, FileExistsError) and not overwrite
            else f"Could not write results: {failure}"
        )
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as cleanup_failure:
                detail += f" Temporary file cleanup also failed: {cleanup_failure}"
        raise ResultsExportError(path, detail) from failure
