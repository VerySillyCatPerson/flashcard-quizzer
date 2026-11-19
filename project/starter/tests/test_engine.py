"""Pure grading, finite session state, interchangeable strategies, and results."""

from collections import Counter
from random import Random
from typing import Sequence

import pytest

from utils.engine import QuizSession, evaluate_answer
from utils.models import Flashcard
from utils.strategies import RandomStrategy, SequentialStrategy


@pytest.mark.parametrize(
    ("expected", "answer", "correct"),
    [
        ("def", " DEF \t", True),
        ("Stra\u00dfe", "STRASSE", True),
        ("two words", "two  words", False),
        ("answer!", "ANSWER!", True),
        ("answer!", "answer", False),
        ("a-b", "ab", False),
        ("'term'", "'TERM'", True),
        ("def", "", False),
        ("def", "\u2003\t", False),
        ("def", "not def", False),
    ],
)
def test_answer_evaluation(expected: str, answer: str, correct: bool) -> None:
    """Grade only by agreed case/outer-space rules while retaining raw input."""
    card = Flashcard("Question", expected)
    result = evaluate_answer(card, answer)
    assert result.card == card
    assert result.answer == answer
    assert result.correct is correct


def test_unanswered_session_has_no_accuracy_or_misses(cards: list[Flashcard]) -> None:
    """Unfinished input is not a submission or an incorrect answer."""
    session = QuizSession(cards, SequentialStrategy())
    assert session.current_card == cards[0]
    assert session.current_card == cards[0]
    summary = session.summary
    assert summary.deck_size == 3
    assert summary.answered_count == 0
    assert summary.correct_count == 0
    assert summary.accuracy_percent is None
    assert summary.missed_cards == ()
    assert summary.answers == ()
    assert not summary.is_complete


def test_three_card_session_with_two_correct(cards: list[Flashcard]) -> None:
    """Sequential sessions finish once with results and missed-card identity."""
    source = cards.copy()
    session = QuizSession(cards, SequentialStrategy())
    assert session.current_card == cards[0]
    assert session.submit_answer(" application programming interface ").correct
    assert session.current_card == cards[1]
    missed = session.submit_answer("incorrect")
    assert not missed.correct
    assert missed.card.back == "Central Processing Unit"
    assert session.current_card == cards[2]
    assert session.submit_answer("RANDOM ACCESS MEMORY").correct
    assert session.current_card is None
    summary = session.summary
    assert summary.deck_size == 3
    assert summary.answered_count == 3
    assert summary.correct_count == 2
    assert summary.accuracy_percent == pytest.approx(200 / 3)
    assert summary.missed_cards == (cards[1],)
    assert [result.card for result in summary.answers] == source
    assert summary.is_complete
    assert cards == source


@pytest.mark.parametrize("all_correct", [False, True])
def test_all_correct_or_all_incorrect_statistics(
    cards: list[Flashcard], all_correct: bool
) -> None:
    """Score extremes yield 100/0 percent and only genuinely missed cards."""
    session = QuizSession(cards, SequentialStrategy())
    while (card := session.current_card) is not None:
        session.submit_answer(card.back if all_correct else "incorrect")
    assert session.summary.correct_count == (3 if all_correct else 0)
    assert session.summary.accuracy_percent == (100 if all_correct else 0)
    assert session.summary.missed_cards == (() if all_correct else tuple(cards))


def test_partial_statistics_and_snapshot_are_stable(cards: list[Flashcard]) -> None:
    """A partial summary excludes pending cards and never changes retroactively."""
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer(cards[0].back)
    first = session.summary
    session.submit_answer("")
    second = session.summary
    assert first.answered_count == 1
    assert first.correct_count == 1
    assert first.accuracy_percent == 100
    assert first.missed_cards == ()
    assert second.answered_count == 2
    assert second.correct_count == 1
    assert second.accuracy_percent == 50
    assert second.missed_cards == (cards[1],)
    assert not second.is_complete
    assert session.current_card == cards[2]


@pytest.mark.parametrize("seed", [0, 7, 42])
def test_random_session_asks_every_card_once(cards: list[Flashcard], seed: int) -> None:
    """Random sessions terminate with one answer per card without deck mutation."""
    before = cards.copy()
    session = QuizSession(cards, RandomStrategy(Random(seed)))
    asked: list[Flashcard] = []
    for _ in cards:
        card = session.current_card
        assert card is not None
        asked.append(card)
        session.submit_answer(card.back)
    assert session.current_card is None
    assert len(asked) == len(before)
    assert Counter(asked) == Counter(before)
    assert session.summary.is_complete
    assert cards == before


def test_source_mutation_cannot_change_an_active_session(
    cards: list[Flashcard],
) -> None:
    """The session owns a snapshot instead of retaining the caller's list."""
    before = cards.copy()
    session = QuizSession(cards, SequentialStrategy())
    cards.clear()
    for expected in before:
        assert session.current_card == expected
        session.submit_answer(expected.back)
    assert session.summary.deck_size == len(before)
    assert session.summary.is_complete


def test_structural_strategy_runs_once_and_order_is_snapshotted(
    cards: list[Flashcard],
) -> None:
    """A new strategy needs matching methods, not inheritance or engine changes."""

    class ReverseStrategy:
        """Test extension whose mutable output is deliberately changed later."""

        def __init__(self) -> None:
            """Track calls and retain the list returned to the engine."""
            self.calls = 0
            self.ordered: list[Flashcard] = []

        def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]:
            """Reverse once to demonstrate interchangeability."""
            self.calls += 1
            self.ordered = list(reversed(cards))
            return self.ordered

    strategy = ReverseStrategy()
    session = QuizSession(cards, strategy)
    strategy.ordered.clear()
    for expected in reversed(cards):
        assert session.current_card == expected
        session.submit_answer(expected.back)
    assert strategy.calls == 1
    assert session.summary.is_complete


@pytest.mark.parametrize("kind", ["missing", "duplicate", "foreign"])
def test_invalid_strategy_output_is_rejected(cards: list[Flashcard], kind: str) -> None:
    """A strategy cannot silently drop, repeat, or inject a question."""

    class InvalidStrategy:
        """Return an invalid permutation for each contract-failure scenario."""

        def order(self, source: Sequence[Flashcard]) -> list[Flashcard]:
            """Produce a deterministic invalid order for the chosen case."""
            if kind == "missing":
                return list(source[:-1])
            if kind == "duplicate":
                return [source[0]] * len(source)
            return [*source[:-1], Flashcard("foreign", "answer")]

    with pytest.raises(ValueError, match="every source card exactly once"):
        QuizSession(cards, InvalidStrategy())


def test_empty_session_is_rejected() -> None:
    """Programmatic callers must obey the loader's nonempty-deck contract."""
    with pytest.raises(ValueError, match="at least one card"):
        QuizSession([], SequentialStrategy())


def test_answer_after_completion_does_not_change_results(
    cards: list[Flashcard],
) -> None:
    """A finished session cannot score additional answers or repeat a question."""
    session = QuizSession(cards[:1], SequentialStrategy())
    session.submit_answer(cards[0].back)
    before = session.summary
    with pytest.raises(RuntimeError, match="already complete"):
        session.submit_answer("extra")
    assert session.summary == before


def test_matching_fronts_grade_against_their_own_backs() -> None:
    """Matching one repeated question's answer does not satisfy another's back."""
    cards = [
        Flashcard("bank", "financial institution"),
        Flashcard("bank", "river edge"),
    ]
    session = QuizSession(cards, SequentialStrategy())
    assert session.submit_answer("financial institution").correct
    assert not session.submit_answer("financial institution").correct
    assert session.summary.missed_cards == (cards[1],)


def test_engine_does_not_read_or_print(
    cards: list[Flashcard],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Terminal I/O can be provided later without changing session code."""

    def forbidden_input(prompt: str = "") -> str:
        """Fail the test if engine code attempts interactive input."""
        raise AssertionError("Engine must not read input")

    monkeypatch.setattr("builtins.input", forbidden_input)
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer(cards[0].back)
    _ = session.summary
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_unexpected_grading_error_preserves_pending_card(
    cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Unexpected failures propagate and do not consume an unrecorded answer."""
    failure = ValueError("grading bug")

    def broken_evaluation(card: Flashcard, answer: str) -> None:
        """Simulate a programmer error rather than an incorrect user answer."""
        raise failure

    monkeypatch.setattr("utils.engine.evaluate_answer", broken_evaluation)
    session = QuizSession(cards, SequentialStrategy())
    with pytest.raises(ValueError) as captured:
        session.submit_answer("answer")
    assert captured.value is failure
    assert session.current_card == cards[0]
    assert session.summary.answered_count == 0
