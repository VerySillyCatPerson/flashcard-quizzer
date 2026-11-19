"""Typed cards, content identity, and result snapshots independent of storage."""

import hashlib
import json
from dataclasses import dataclass
from typing import Literal

FinishReason = Literal["completed", "eof", "interrupted", "input_error", "output_error"]


def normalize_text(value: str) -> str:
    """Trim outer whitespace and fold Unicode case without altering inner spaces."""
    return value.strip().casefold()


@dataclass(frozen=True)
class Flashcard:
    """An immutable front/back record; validate untrusted data through the loader.

    Type annotations do not enforce runtime validation. The loader supplies
    nonblank strings with outer whitespace trimmed and capitalization preserved.
    """

    front: str
    back: str

    @property
    def normalized_pair(self) -> tuple[str, str]:
        """Return the shared normalization used for duplicate checks and identity."""
        return normalize_text(self.front), normalize_text(self.back)

    @property
    def card_id(self) -> str:
        """Return a versioned content key shared by identical cards in any deck.

        A JSON array avoids concatenation ambiguities. Fixed ASCII serialization
        makes the digest independent of file encoding, formatting, and paths.
        """
        content = json.dumps(
            self.normalized_pair, ensure_ascii=True, separators=(",", ":")
        )
        return "card-v1:" + hashlib.sha256(content.encode("ascii")).hexdigest()


@dataclass(frozen=True)
class AnswerResult:
    """One completed answer, retaining raw input and the associated card."""

    card: Flashcard
    answer: str
    correct: bool


@dataclass(frozen=True)
class SessionSummary:
    """An immutable snapshot; all statistics use completed answers only."""

    deck_size: int
    answers: tuple[AnswerResult, ...]

    @property
    def answered_count(self) -> int:
        """Return the number of submitted answers, excluding unasked cards."""
        return len(self.answers)

    @property
    def correct_count(self) -> int:
        """Count correct submissions without treating unasked cards as wrong."""
        return sum(result.correct for result in self.answers)

    @property
    def accuracy_percent(self) -> float | None:
        """Return unrounded percentage, or None when no answer is completed."""
        if not self.answers:
            return None
        return self.correct_count / self.answered_count * 100

    @property
    def missed_cards(self) -> tuple[Flashcard, ...]:
        """Return incorrectly answered cards in session order, retaining backs."""
        return tuple(result.card for result in self.answers if not result.correct)

    @property
    def is_complete(self) -> bool:
        """Report whether every card in the deck has a completed answer."""
        return self.answered_count == self.deck_size
