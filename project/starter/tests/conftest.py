"""Shared validated three-card deck for session and strategy behavior tests."""

import pytest

from utils.models import Flashcard


@pytest.fixture
def cards() -> list[Flashcard]:
    """Provide independent immutable records in a fresh mutable source list."""
    return [
        Flashcard("API", "Application Programming Interface"),
        Flashcard("CPU", "Central Processing Unit"),
        Flashcard("RAM", "Random Access Memory"),
    ]
