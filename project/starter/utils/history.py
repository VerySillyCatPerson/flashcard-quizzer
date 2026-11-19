"""Versioned error-balance persistence, independent of selection and terminal I/O."""

import json
import os
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from types import MappingProxyType
from typing import Mapping, NoReturn, Sequence

from utils.models import AnswerResult, SessionSummary

_VERSION = 1
_POLICY = "error-balance-v1"
_CARD_ID = re.compile(r"card-v1:[0-9a-f]{64}")


class HistoryError(Exception):
    """A structured expected history error for callers to present."""

    def __init__(self, path: Path, detail: str) -> None:
        """Retain the affected path and operation-specific error detail."""
        self.path = path
        self.detail = detail
        super().__init__(f"History error for '{path}': {detail}")


class HistoryLoadError(HistoryError):
    """Previous scores could not be loaded; this run must not overwrite them."""


class HistorySaveError(HistoryError):
    """Completed-answer updates were not successfully saved."""


class _HistoryFormatError(ValueError):
    """An explicit history format failure, not an unexpected programming error."""


def default_history_path() -> Path:
    """Return the separate user-state path without creating or reading anything."""
    return Path.home() / ".flashcard_quizzer" / "history.json"


def updated_scores(
    scores: Mapping[str, int], answers: Sequence[AnswerResult]
) -> dict[str, int]:
    """Copy validated scores and apply only completed answers from any quiz mode.

    Incorrect adds one; correct subtracts one with a zero floor. Keep dormant
    card entries so reintroduced content resumes its prior learning history.
    """
    updated = dict(scores)
    for result in answers:
        key = result.card.card_id
        previous = updated.get(key, 0)
        updated[key] = max(0, previous - 1) if result.correct else previous + 1
    return updated


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate JSON keys instead of replacing a previous score silently."""
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _HistoryFormatError(f"Duplicate JSON object key {key!r}.")
        result[key] = value
    return result


def _reject_constant(value: str) -> NoReturn:
    """Reject nonstandard NaN/Infinity constants in stored JSON."""
    raise _HistoryFormatError(f"Invalid JSON constant {value!r}.")


def _validate_history(value: object) -> dict[str, int]:
    """Require the supported schema/policy and content-keyed nonnegative scores."""
    if not isinstance(value, dict):
        raise _HistoryFormatError("History must be a JSON object.")
    if type(value.get("version")) is not int or value["version"] != _VERSION:
        raise _HistoryFormatError("Unsupported or missing history version.")
    if value.get("policy") != _POLICY:
        raise _HistoryFormatError("Unsupported or missing history scoring policy.")
    if set(value) != {"version", "policy", "scores"}:
        raise _HistoryFormatError("Expected only version, policy, and scores fields.")
    raw_scores = value["scores"]
    if not isinstance(raw_scores, dict):
        raise _HistoryFormatError("History 'scores' must be an object.")
    scores: dict[str, int] = {}
    for key, score in raw_scores.items():
        if not isinstance(key, str) or not _CARD_ID.fullmatch(key):
            raise _HistoryFormatError(f"Invalid card identity key {key!r}.")
        if type(score) is not int or score < 0:
            raise _HistoryFormatError(
                f"Score for {key!r} must be a nonnegative integer, not a boolean."
            )
        scores[key] = score
    return scores


def _read_scores(path: Path) -> dict[str, int]:
    """Read valid history; a genuinely absent file is a normal fresh profile."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return {}
    except (OSError, UnicodeDecodeError) as error:
        raise HistoryLoadError(
            path, f"Could not read previous scores: {error}"
        ) from error

    try:
        value: object = json.loads(
            text, object_pairs_hook=_unique_object, parse_constant=_reject_constant
        )
    except (ValueError, RecursionError) as error:
        raise HistoryLoadError(path, f"Invalid history JSON: {error}") from error
    try:
        return _validate_history(value)
    except _HistoryFormatError as error:
        raise HistoryLoadError(path, str(error)) from error


def _atomic_save(path: Path, scores: Mapping[str, int]) -> None:
    """Replace one complete file; preserve an old valid file on expected failure.

    Sibling temporary files keep replacement on one filesystem. Closing before
    replacement supports Windows. Atomicity does not merge concurrent sessions
    or guarantee retention of in-memory answers after forced process termination.
    """
    try:
        content = (
            json.dumps(
                {"version": _VERSION, "policy": _POLICY, "scores": dict(scores)},
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )
    except ValueError as error:
        raise HistorySaveError(path, f"Could not encode history: {error}") from error

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
        os.replace(temporary_path, path)
    except OSError as error:
        detail = f"Could not save learning updates: {error}"
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError as cleanup_error:
                detail += f" Temporary file cleanup also failed: {cleanup_error}"
        raise HistorySaveError(path, detail) from error


class HistoryStore:
    """One quiz run's load state and at most one successful session-end commit.

    Corrupt/unreadable/unsupported history yields zero scores and a structured
    load_error. Saving is disabled for that run, preserving the problematic file.
    Callers decide warnings/statuses; this class never prints or exits.
    """

    def __init__(self, path: str | Path) -> None:
        """Load once without creating a missing file or its parent directories."""
        self._path = Path(path)
        self._scores: dict[str, int] = {}
        self._load_error: HistoryLoadError | None = None
        self._saved = False
        try:
            self._scores = _read_scores(self._path)
        except HistoryLoadError as error:
            self._load_error = error

    @property
    def path(self) -> Path:
        """Return the history destination bound to this run."""
        return self._path

    @property
    def scores(self) -> Mapping[str, int]:
        """Return a read-only snapshot for selection without exposing mutable state."""
        return MappingProxyType(self._scores.copy())

    @property
    def load_error(self) -> HistoryLoadError | None:
        """Return degraded-load information for the later terminal adapter."""
        return self._load_error

    @property
    def can_save(self) -> bool:
        """Report whether this run has usable history and has not committed yet."""
        return self._load_error is None and not self._saved

    def save_session(self, summary: SessionSummary) -> None:
        """Commit completed answers once, from any mode or an orderly partial run.

        No answers means no file write. Expected failures leave both prior disk
        state and in-memory scores unchanged, allowing retry. Reopen a store for
        the next quiz run; a second successful commit would double-count answers.
        """
        if self._load_error is not None:
            raise HistorySaveError(
                self._path,
                "Previous scores could not be loaded; learning updates are disabled.",
            ) from self._load_error
        if self._saved:
            raise HistorySaveError(
                self._path, "This run's history is already finalized."
            )
        if summary.answers:
            scores = updated_scores(self._scores, summary.answers)
            _atomic_save(self._path, scores)
            self._scores = scores
        self._saved = True
