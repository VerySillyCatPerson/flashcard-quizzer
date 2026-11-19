"""Quiz state and answer evaluation; terminal input/output belongs to callers."""

from collections import Counter
from typing import Sequence

from utils.models import AnswerResult, Flashcard, SessionSummary, normalize_text
from utils.strategies import QuizStrategy


def evaluate_answer(card: Flashcard, answer: str) -> AnswerResult:
    """Compare a completed answer using the same normalization as identity."""
    return AnswerResult(
        card=card,
        answer=answer,
        correct=normalize_text(answer) == normalize_text(card.back),
    )


class QuizSession:
    """A finite session over a validated deck, advanced only by submissions.

    Callers read current_card, obtain input externally, and submit_answer only
    after input is completed. EOF/Ctrl+C handling can use summary without
    submitting or scoring an unfinished answer. No terminal callbacks are used.
    """

    def __init__(self, cards: Sequence[Flashcard], strategy: QuizStrategy) -> None:
        """Snapshot one strategy permutation and reject an empty/invalid order."""
        source = tuple(cards)
        if not source:
            raise ValueError("A quiz session requires at least one card.")
        ordered = tuple(strategy.order(source))
        if Counter(ordered) != Counter(source):
            raise ValueError("Strategy must return every source card exactly once.")
        self._ordered = ordered
        self._answers: list[AnswerResult] = []

    @property
    def current_card(self) -> Flashcard | None:
        """Return the pending card, or None after every card has been answered."""
        if len(self._answers) == len(self._ordered):
            return None
        return self._ordered[len(self._answers)]

    def submit_answer(self, answer: str) -> AnswerResult:
        """Grade the pending card once; reject submissions after completion."""
        card = self.current_card
        if card is None:
            raise RuntimeError("The quiz session is already complete.")
        result = evaluate_answer(card, answer)
        self._answers.append(result)
        return result

    @property
    def summary(self) -> SessionSummary:
        """Return a stable snapshot that cannot acquire later submissions."""
        return SessionSummary(
            deck_size=len(self._ordered), answers=tuple(self._answers)
        )
