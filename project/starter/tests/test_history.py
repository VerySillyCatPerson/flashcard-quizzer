"""History format, error-balance updates, atomic saves, and real session round trips."""

import json
from pathlib import Path
from random import Random
from typing import NoReturn

import pytest

import utils.history as history_module
from utils.data_loader import load_flashcards
from utils.engine import QuizSession, evaluate_answer
from utils.history import (
    HistoryLoadError,
    HistorySaveError,
    HistoryStore,
    default_history_path,
    updated_scores,
)
from utils.models import Flashcard, SessionSummary
from utils.strategies import (
    AdaptiveStrategy,
    QuizStrategy,
    RandomStrategy,
    SequentialStrategy,
)


def _document(scores: dict[str, int]) -> dict[str, object]:
    """Create the explicit on-disk schema used in real-file tests."""
    return {"version": 1, "policy": "error-balance-v1", "scores": scores}


def _write_history(path: Path, value: object) -> None:
    """Write an arbitrary valid JSON value before testing history validation."""
    path.write_text(json.dumps(value), encoding="utf-8")


def _one_answer(card: Flashcard, correct: bool = False) -> SessionSummary:
    """Make a real partial session snapshot with one completed answer."""
    session = QuizSession([card], SequentialStrategy())
    session.submit_answer(card.back if correct else "incorrect")
    return session.summary


def test_missing_history_is_fresh_without_creating_files(tmp_path: Path) -> None:
    """First-use loading is normal and has no filesystem-write side effects."""
    path = tmp_path / "new-directory" / "history.json"
    store = HistoryStore(str(path))
    assert store.path == path
    assert dict(store.scores) == {}
    assert store.load_error is None
    assert store.can_save
    assert not path.parent.exists()


def test_default_path_is_separate_user_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Compute the user-state path without touching the actual user's profile."""

    def fake_home() -> Path:
        """Use the isolated test directory as home."""
        return tmp_path

    monkeypatch.setattr(Path, "home", staticmethod(fake_home))
    assert default_history_path() == tmp_path / ".flashcard_quizzer" / "history.json"
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize(
    ("previous", "correct", "expected"),
    [
        (0, True, 0),
        (1, True, 0),
        (3, True, 2),
        (0, False, 1),
        (1, False, 2),
        (3, False, 4),
    ],
)
def test_error_balance_increases_and_decreases_with_zero_floor(
    cards: list[Flashcard], previous: int, correct: bool, expected: int
) -> None:
    """Correct practice can retire old priority without making scores negative."""
    scores = {cards[0].card_id: previous, cards[1].card_id: 4}
    before = scores.copy()
    answers = [evaluate_answer(cards[0], cards[0].back if correct else "incorrect")]
    updated = updated_scores(scores, answers)
    assert updated[cards[0].card_id] == expected
    assert updated[cards[1].card_id] == 4
    assert scores == before


def test_unseen_cards_start_at_zero_and_dormant_scores_survive(
    cards: list[Flashcard],
) -> None:
    """New cards start at zero and unrelated/removed cards are not discarded."""
    old = {cards[0].card_id: 5}
    updated = updated_scores(
        old,
        [evaluate_answer(cards[1], cards[1].back), evaluate_answer(cards[2], "wrong")],
    )
    assert updated == {cards[0].card_id: 5, cards[1].card_id: 0, cards[2].card_id: 1}


def test_real_two_session_round_trip(tmp_path: Path, cards: list[Flashcard]) -> None:
    """Write/reopen twice and show a correct answer reducing future priority."""
    path = tmp_path / "profile" / "history.json"
    first_store = HistoryStore(path)
    first = QuizSession(cards, SequentialStrategy())
    while (card := first.current_card) is not None:
        first.submit_answer(card.back if card.front == "RAM" else "incorrect")
    assert not path.exists()
    first_store.save_session(first.summary)
    assert json.loads(path.read_text(encoding="utf-8")) == _document(
        {cards[0].card_id: 1, cards[1].card_id: 1, cards[2].card_id: 0}
    )

    second_store = HistoryStore(path)
    assert second_store.load_error is None
    assert AdaptiveStrategy(second_store.scores).order(cards) == cards
    second = QuizSession(cards, AdaptiveStrategy(second_store.scores))
    while (card := second.current_card) is not None:
        second.submit_answer("incorrect" if card.front == "CPU" else card.back)
    assert second.summary.is_complete
    second_store.save_session(second.summary)

    reloaded = HistoryStore(path)
    assert dict(reloaded.scores) == {
        cards[0].card_id: 0,
        cards[1].card_id: 2,
        cards[2].card_id: 0,
    }
    assert AdaptiveStrategy(reloaded.scores).order(cards) == [
        cards[1],
        cards[0],
        cards[2],
    ]
    assert set(path.parent.iterdir()) == {path}


@pytest.mark.parametrize("mode", ["sequential", "random", "adaptive"])
def test_completed_answers_update_history_in_every_mode(
    tmp_path: Path, cards: list[Flashcard], mode: str
) -> None:
    """Mode selects order only; all completed answers use the same update path."""
    path = tmp_path / "history.json"
    _write_history(path, _document({card.card_id: 2 for card in cards}))
    store = HistoryStore(path)
    strategy: QuizStrategy
    if mode == "sequential":
        strategy = SequentialStrategy()
    elif mode == "random":
        strategy = RandomStrategy(Random(7))
    else:
        strategy = AdaptiveStrategy(store.scores)
    session = QuizSession(cards, strategy)
    while (card := session.current_card) is not None:
        session.submit_answer(card.back if card.front == "API" else "incorrect")
    store.save_session(session.summary)
    assert dict(HistoryStore(path).scores) == {
        cards[0].card_id: 1,
        cards[1].card_id: 3,
        cards[2].card_id: 3,
    }


def test_adaptive_order_stays_fixed_during_session(cards: list[Flashcard]) -> None:
    """Even changing the external score map cannot reorder pending cards."""
    scores = {cards[0].card_id: 1, cards[2].card_id: 1}
    session = QuizSession(cards, AdaptiveStrategy(scores))
    assert session.current_card == cards[0]
    session.submit_answer(cards[0].back)
    scores[cards[1].card_id] = 100
    for expected in (cards[2], cards[1]):
        assert session.current_card == expected
        session.submit_answer(expected.back)
    assert session.current_card is None
    assert session.summary.answered_count == len(cards)
    assert session.summary.is_complete


def test_shared_identity_across_real_deck_files(tmp_path: Path) -> None:
    """A wrapped/reordered second deck reuses the first deck's learned score."""
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"
    first_path.write_text('[{"front":"A","back":"Alpha"}]', encoding="utf-8")
    second_path.write_text(
        '{"cards":[{"front":"B","back":"Beta"},{"front":" a ","back":"ALPHA"}]}',
        encoding="utf-8",
    )
    first_cards = load_flashcards(first_path)
    second_cards = load_flashcards(second_path)
    history_path = tmp_path / "history.json"
    store = HistoryStore(history_path)
    store.save_session(_one_answer(first_cards[0]))
    shared = HistoryStore(history_path)
    assert first_cards[0].card_id == second_cards[1].card_id
    assert shared.scores[second_cards[1].card_id] == 1
    assert AdaptiveStrategy(shared.scores).order(second_cards) == list(
        reversed(second_cards)
    )


def test_edited_card_gets_fresh_score_without_erasing_old_identity(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """An edit starts fresh while the original content retains its old score."""
    path = tmp_path / "history.json"
    original = cards[0]
    _write_history(path, _document({original.card_id: 3}))
    edited = Flashcard(original.front, "A different answer")
    store = HistoryStore(path)
    assert store.scores.get(edited.card_id, 0) == 0
    store.save_session(_one_answer(edited, correct=True))
    reloaded = HistoryStore(path)
    assert reloaded.scores[edited.card_id] == 0
    assert reloaded.scores[original.card_id] == 3


def test_partial_session_updates_only_submitted_answers(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """Partial saves exclude pending answers and preserve earlier snapshots."""
    path = tmp_path / "history.json"
    initial = {card.card_id: 2 for card in cards}
    _write_history(path, _document(initial))
    before = path.read_bytes()
    store = HistoryStore(path)
    snapshot = store.scores
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer(cards[0].back)
    assert session.current_card == cards[1]
    assert path.read_bytes() == before
    store.save_session(session.summary)
    assert not session.summary.is_complete
    assert dict(store.scores) == {
        cards[0].card_id: 1,
        cards[1].card_id: 2,
        cards[2].card_id: 2,
    }
    assert dict(snapshot) == initial


def test_zero_answer_session_does_not_create_history(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """Stopping before the first completed answer writes no personal state."""
    path = tmp_path / "profile" / "history.json"
    store = HistoryStore(path)
    store.save_session(QuizSession(cards, SequentialStrategy()).summary)
    assert not path.parent.exists()
    assert not store.can_save


@pytest.mark.parametrize(
    "value",
    [
        None,
        [],
        True,
        1,
        {},
        {"version": True},
        {"version": 2},
        {"version": 1, "policy": "other", "scores": {}},
        {"version": 1, "policy": "error-balance-v1"},
        {"version": 1, "policy": "error-balance-v1", "scores": []},
        {"version": 1, "policy": "error-balance-v1", "scores": {}, "unknown": 1},
    ],
)
def test_invalid_history_schema_is_preserved_and_save_disabled(
    tmp_path: Path, cards: list[Flashcard], value: object
) -> None:
    """Schema/policy failures fall back to zero without overwriting the file."""
    path = tmp_path / "history.json"
    _write_history(path, value)
    original = path.read_bytes()
    store = HistoryStore(path)
    assert isinstance(store.load_error, HistoryLoadError)
    assert store.load_error.path == path
    assert dict(store.scores) == {}
    assert not store.can_save
    assert AdaptiveStrategy(store.scores).order(cards) == cards
    with pytest.raises(HistorySaveError, match="disabled"):
        store.save_session(_one_answer(cards[0]))
    assert path.read_bytes() == original


@pytest.mark.parametrize("score", [-1, True, False, 1.5, "2", None, [], {}])
def test_invalid_scores_do_not_partially_load(
    tmp_path: Path, cards: list[Flashcard], score: object
) -> None:
    """A valid first entry cannot leak through when a later score is invalid."""
    value = {
        "version": 1,
        "policy": "error-balance-v1",
        "scores": {cards[0].card_id: 5, cards[1].card_id: score},
    }
    path = tmp_path / "history.json"
    _write_history(path, value)
    before = path.read_bytes()
    store = HistoryStore(path)
    assert store.load_error is not None
    assert "nonnegative integer" in store.load_error.detail
    assert dict(store.scores) == {}
    assert path.read_bytes() == before


@pytest.mark.parametrize("key", ["", "old-card", "card-v1:" + "A" * 64])
def test_invalid_identity_keys_disable_saving(tmp_path: Path, key: str) -> None:
    """Unsupported identity formats are preserved rather than guessed/migrated."""
    path = tmp_path / "history.json"
    _write_history(path, _document({key: 1}))
    store = HistoryStore(path)
    assert store.load_error is not None
    assert "Invalid card identity" in store.load_error.detail
    assert not store.can_save


@pytest.mark.parametrize(
    "text",
    [
        "",
        "{bad json",
        '{"version":1,"version":1}',
        '{"version":1,"policy":"error-balance-v1","scores":NaN}',
        "[" * 5000 + "0" + "]" * 5000,
        '{"version":' + "9" * 10000 + "}",
    ],
)
def test_corrupt_history_json_is_preserved(tmp_path: Path, text: str) -> None:
    """Decode failures, nonstandard constants, and resource limits are load errors."""
    path = tmp_path / "history.json"
    path.write_text(text, encoding="utf-8")
    before = path.read_bytes()
    store = HistoryStore(path)
    assert store.load_error is not None
    assert dict(store.scores) == {}
    assert not store.can_save
    assert path.read_bytes() == before


def test_invalid_utf8_history_is_preserved(tmp_path: Path) -> None:
    """Encoding errors disable saving without replacing the problematic bytes."""
    path = tmp_path / "history.json"
    path.write_bytes(b"\xff\xfeinvalid")
    store = HistoryStore(path)
    assert store.load_error is not None
    assert isinstance(store.load_error.__cause__, UnicodeDecodeError)
    assert not store.can_save
    assert path.read_bytes() == b"\xff\xfeinvalid"


def test_valid_utf8_bom_history(tmp_path: Path, cards: list[Flashcard]) -> None:
    """Accept a BOM while preserving zero scores as legitimate integer values."""
    path = tmp_path / "history.json"
    path.write_text(json.dumps(_document({cards[0].card_id: 0})), encoding="utf-8-sig")
    store = HistoryStore(path)
    assert store.load_error is None
    assert store.scores[cards[0].card_id] == 0


def test_unreadable_history_disables_saving(
    tmp_path: Path, cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Permission failure cannot be mistaken for a fresh writable profile."""
    path = tmp_path / "history.json"
    _write_history(path, _document({cards[0].card_id: 2}))
    before = path.read_bytes()

    def denied_read(
        self: Path, encoding: str | None = None, errors: str | None = None
    ) -> str:
        """Simulate a read failure independently of Windows privilege level."""
        raise PermissionError("read denied")

    monkeypatch.setattr(Path, "read_text", denied_read)
    store = HistoryStore(path)
    assert store.load_error is not None
    assert isinstance(store.load_error.__cause__, PermissionError)
    assert dict(store.scores) == {}
    assert not store.can_save
    with pytest.raises(HistorySaveError):
        store.save_session(_one_answer(cards[0]))
    assert path.read_bytes() == before


@pytest.mark.parametrize("boundary", ["replace", "fsync", "temporary", "mkdir"])
def test_failed_save_preserves_previous_valid_history_and_can_retry(
    tmp_path: Path,
    cards: list[Flashcard],
    monkeypatch: pytest.MonkeyPatch,
    boundary: str,
) -> None:
    """Expected I/O failures never replace old data or advance in-memory scores."""
    path = tmp_path / "history.json"
    initial = {cards[0].card_id: 2}
    _write_history(path, _document(initial))
    before = path.read_bytes()
    store = HistoryStore(path)
    summary = _one_answer(cards[0])

    def denied(*args: object, **kwargs: object) -> NoReturn:
        """Represent a controlled OS failure at one persistence boundary."""
        raise PermissionError("write denied")

    with monkeypatch.context() as patch:
        if boundary == "temporary":
            patch.setattr(history_module, "NamedTemporaryFile", denied)
        elif boundary == "mkdir":
            patch.setattr(Path, "mkdir", denied)
        else:
            patch.setattr(f"utils.history.os.{boundary}", denied)
        with pytest.raises(HistorySaveError, match="Could not save learning updates"):
            store.save_session(summary)
    assert path.read_bytes() == before
    assert dict(store.scores) == initial
    assert store.can_save
    assert set(tmp_path.iterdir()) == {path}
    store.save_session(summary)
    assert HistoryStore(path).scores[cards[0].card_id] == 3
    assert not store.can_save


def test_failed_serialization_preserves_old_file(
    tmp_path: Path, cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A decoder-compatible score may still hit a serialization resource limit."""
    path = tmp_path / "history.json"
    _write_history(path, _document({cards[0].card_id: 2}))
    before = path.read_bytes()
    store = HistoryStore(path)

    original_dumps = json.dumps

    def encoding_limit(
        value: object,
        *,
        indent: int | None = None,
        sort_keys: bool = False,
        ensure_ascii: bool = True,
        separators: tuple[str, str] | None = None,
    ) -> str:
        """Fail on the history document while leaving card-key encoding intact."""
        if isinstance(value, dict):
            raise ValueError("integer encoding limit")
        return original_dumps(
            value,
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii,
            separators=separators,
        )

    monkeypatch.setattr("utils.history.json.dumps", encoding_limit)
    with pytest.raises(HistorySaveError, match="Could not encode history"):
        store.save_session(_one_answer(cards[0]))
    assert path.read_bytes() == before
    assert store.scores[cards[0].card_id] == 2


def test_cleanup_failure_is_reported_without_losing_old_file(
    tmp_path: Path, cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A failed temporary-file cleanup must not hide the original save failure."""
    path = tmp_path / "history.json"
    _write_history(path, _document({cards[0].card_id: 2}))
    before = path.read_bytes()
    store = HistoryStore(path)

    def denied(*args: object, **kwargs: object) -> NoReturn:
        """Represent replacement/cleanup permission failures."""
        raise PermissionError("denied")

    with monkeypatch.context() as patch:
        patch.setattr("utils.history.os.replace", denied)
        patch.setattr(Path, "unlink", denied)
        with pytest.raises(HistorySaveError, match="cleanup also failed"):
            store.save_session(_one_answer(cards[0]))
    assert path.read_bytes() == before
    assert store.scores[cards[0].card_id] == 2
    assert len(list(tmp_path.glob(".history.json.*.tmp"))) == 1


def test_successful_session_cannot_be_counted_twice(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """Finalize once per store/run; reopening is explicit for the next session."""
    path = tmp_path / "history.json"
    store = HistoryStore(path)
    summary = _one_answer(cards[0])
    store.save_session(summary)
    before = path.read_bytes()
    with pytest.raises(HistorySaveError, match="already finalized"):
        store.save_session(summary)
    assert path.read_bytes() == before
    assert HistoryStore(path).scores[cards[0].card_id] == 1


def test_unexpected_validation_error_is_not_disguised(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Only explicitly classified format errors become degraded-load state."""
    path = tmp_path / "history.json"
    _write_history(path, _document({}))
    failure = ValueError("validation programming bug")

    def broken_validation(value: object) -> dict[str, int]:
        """Raise an unexpected failure after decoding has completed."""
        raise failure

    monkeypatch.setattr(history_module, "_validate_history", broken_validation)
    with pytest.raises(ValueError) as captured:
        HistoryStore(path)
    assert captured.value is failure


def test_history_never_prints(
    tmp_path: Path, cards: list[Flashcard], capsys: pytest.CaptureFixture[str]
) -> None:
    """Persistence supplies structured state/errors rather than terminal policy."""
    path = tmp_path / "history.json"
    store = HistoryStore(path)
    store.save_session(_one_answer(cards[0]))
    path.write_text("corrupt", encoding="utf-8")
    failed = HistoryStore(path)
    assert failed.load_error is not None
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
