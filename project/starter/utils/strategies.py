"""Interchangeable, finite card-ordering strategies without I/O or grading."""

from random import Random
from typing import Mapping, Protocol, Sequence

from utils.models import Flashcard


class QuizStrategy(Protocol):
    """Structural interface for a permutation of the validated source deck."""

    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return each input card exactly once without modifying the input."""
        ...


class SequentialStrategy:
    """Select cards in their original order."""

    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return an independent list, even for empty or single-card decks."""
        return list(cards)


class RandomStrategy:
    """Shuffle a copy using an injected or privately owned random generator."""

    def __init__(self, rng: Random | None = None) -> None:
        """Accept Random(seed) for reproducibility without global RNG state."""
        self._rng = rng if rng is not None else Random()

    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return a shuffled copy; a valid shuffle may retain original order."""
        ordered = list(cards)
        self._rng.shuffle(ordered)
        return ordered


class AdaptiveStrategy:
    """Prioritize error-balance scores, with original deck order breaking ties."""

    def __init__(self, scores: Mapping[str, int]) -> None:
        """Snapshot validated nonnegative scores without depending on storage."""
        self._scores = dict(scores)

    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
        """Return each card once, highest priority first; unseen cards score zero."""
        return sorted(cards, key=lambda card: -self._scores.get(card.card_id, 0))
