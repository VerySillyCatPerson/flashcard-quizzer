"""Resolve quiz file roles and reject path aliases before any quiz or writes."""

import errno
import os
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

_UNSUPPORTED_IDENTITY = {
    errno.ENOSYS,
    getattr(errno, "ENOTSUP", errno.ENOSYS),
    getattr(errno, "EOPNOTSUPP", errno.ENOSYS),
}


class PathValidationError(Exception):
    """A file role could not be resolved or safely inspected."""


class PathConflictError(PathValidationError):
    """Two file roles resolve to the same destination or existing file identity."""


@dataclass(frozen=True)
class QuizPaths:
    """Canonical destinations used for subsequent reading and writing."""

    deck: Path
    history: Path
    export: Path | None


def _resolve(role: str, path: Path) -> Path:
    """Expand and resolve paths, including absent outputs and existing symlinks."""
    try:
        return path.expanduser().resolve()
    except (OSError, RuntimeError, ValueError) as error:
        raise PathValidationError(
            f"Could not resolve {role.lower()} path '{path}': {error}"
        ) from error


def _same_existing_file(left: Path, right: Path) -> bool:
    """Detect hard-link aliases where supported without hiding permission errors."""
    try:
        return left.samefile(right)
    except (FileNotFoundError, NotADirectoryError, NotImplementedError):
        return False
    except OSError as error:
        if error.errno in _UNSUPPORTED_IDENTITY:
            return False
        raise PathValidationError(
            f"Could not compare file identities for '{left}' and '{right}': {error}"
        ) from error


def validate_paths(deck: Path, history: Path, export: Path | None) -> QuizPaths:
    """Require distinct resolved files for all roles before loading or writing.

    Resolved-name comparison includes absent outputs; samefile additionally
    catches existing hard links. This is preflight validation, not a filesystem
    lock or protection against concurrent path changes after inspection.
    """
    paths = QuizPaths(
        deck=_resolve("Deck", deck),
        history=_resolve("History", history),
        export=_resolve("Export", export) if export is not None else None,
    )
    roles = [("Deck", paths.deck), ("History", paths.history)]
    if paths.export is not None:
        roles.append(("Export", paths.export))
    for (left_role, left), (right_role, right) in combinations(roles, 2):
        same_name = os.path.normcase(str(left)) == os.path.normcase(str(right))
        if same_name or _same_existing_file(left, right):
            raise PathConflictError(
                f"{left_role} '{left}' and {right_role} '{right}' refer to the same "
                "file; choose distinct paths."
            )
    return paths
