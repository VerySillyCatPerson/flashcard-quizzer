"""Canonical path comparison and supported/unsupported identity inspection."""

import errno
from pathlib import Path

import pytest

from utils.paths import PathConflictError, PathValidationError, validate_paths


def test_absent_outputs_are_compared_by_resolved_name(tmp_path: Path) -> None:
    """Both missing outputs can still conflict through normalized path components."""
    deck = tmp_path / "deck.json"
    history = tmp_path / "subdirectory" / ".." / "out.json"
    with pytest.raises(PathConflictError, match="History.*Export"):
        validate_paths(deck, history, tmp_path / "out.json")
    assert not (tmp_path / "out.json").exists()


def test_valid_paths_return_canonical_destinations(tmp_path: Path) -> None:
    """The later store/export use the resolved paths that were actually inspected."""
    paths = validate_paths(
        tmp_path / "deck.json", tmp_path / "x" / ".." / "history.json", None
    )
    assert paths.deck == (tmp_path / "deck.json").resolve()
    assert paths.history == (tmp_path / "history.json").resolve()
    assert paths.export is None


@pytest.mark.parametrize(
    "failure", [NotImplementedError(), OSError(errno.ENOSYS, "unsupported")]
)
def test_identity_inspection_falls_back_only_when_unsupported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: Exception
) -> None:
    """Unavailable identity support still permits distinct canonical destinations."""

    def unsupported(self: Path, other: Path) -> bool:
        """Simulate a platform without the relevant file-identity operation."""
        raise failure

    monkeypatch.setattr(Path, "samefile", unsupported)
    result = validate_paths(tmp_path / "deck.json", tmp_path / "history.json", None)
    assert result.deck != result.history


@pytest.mark.parametrize(
    "failure",
    [
        PermissionError("denied"),
        RuntimeError("symlink loop"),
        ValueError("invalid path"),
    ],
)
def test_resolution_failures_remain_expected_path_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: Exception
) -> None:
    """Resolve errors do not become ignored alias-inspection failures."""

    def fail_resolve(self: Path, strict: bool = False) -> Path:
        """Represent an OS/path-resolution failure without modifying files."""
        raise failure

    monkeypatch.setattr(Path, "resolve", fail_resolve)
    with pytest.raises(PathValidationError, match="Could not resolve deck") as captured:
        validate_paths(tmp_path / "deck.json", tmp_path / "history.json", None)
    assert captured.value.__cause__ is failure
