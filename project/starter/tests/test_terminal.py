"""Terminal-only escaping and formatting, without changing domain text."""

import json
from io import StringIO
from pathlib import Path

import pytest

from utils.engine import QuizSession
from utils.history import HistoryStore
from utils.models import Flashcard
from utils.results_export import export_results
from utils.strategies import SequentialStrategy
from utils.terminal import configure_streams, format_summary, play, show_summary


@pytest.mark.parametrize("codepoint", [*range(0x20), *range(0x7F, 0xA0)])
def test_card_controls_are_literal_in_questions_feedback_and_missed_summary(
    monkeypatch: pytest.MonkeyPatch, codepoint: int
) -> None:
    """Every C0/DEL/C1 control is escaped at each card-text display boundary."""
    control = chr(codepoint)
    escaped = {9: r"\t", 10: r"\n", 13: r"\r"}.get(codepoint, f"\\x{codepoint:02x}")
    front = f"月{control}[2J café"
    back = f"答{control}[31m naïve"
    card = Flashcard(front, back)
    cards = [card]
    session = QuizSession(cards, SequentialStrategy())
    outgoing = StringIO()
    monkeypatch.setattr("sys.stdin", StringIO("wrong\n"))
    monkeypatch.setattr("sys.stdout", outgoing)
    assert play(session) == "completed"
    assert outgoing.getvalue() == (
        f"\n[1/1] 月{escaped}[2J café\n"
        f"Answer: Incorrect. Expected: 答{escaped}[31m naïve\n"
    )
    summary = format_summary(session.summary, cards, "completed")
    assert f"#1 月{escaped}[2J café" in summary
    assert not any(
        chr(value) in summary
        for value in [*range(0x20), *range(0x7F, 0xA0)]
        if value != 10
    )
    assert (card.front, card.back) == (front, back)


def test_ordinary_unicode_remains_readable(monkeypatch: pytest.MonkeyPatch) -> None:
    """Readable Unicode, including emoji joiners, is not ASCII-escaped."""
    card = Flashcard("月 café 👩‍💻", "Straße λ")
    session = QuizSession([card], SequentialStrategy())
    outgoing = StringIO()
    monkeypatch.setattr("sys.stdin", StringIO("wrong\n"))
    monkeypatch.setattr("sys.stdout", outgoing)
    assert play(session) == "completed"
    assert outgoing.getvalue() == (
        "\n[1/1] 月 café 👩‍💻\nAnswer: Incorrect. Expected: Straße λ\n"
    )
    assert "#1 月 café 👩‍💻" in format_summary(session.summary, [card], "completed")


def test_display_escaping_preserves_grading_identity_history_and_export(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Only presentation changes: domain values and persisted JSON stay original."""
    card = Flashcard("月\x1b[2J", "Straße\x9b31m")
    identity = card.card_id
    session = QuizSession([card], SequentialStrategy())
    outgoing = StringIO()
    monkeypatch.setattr("sys.stdin", StringIO("wrong\n"))
    monkeypatch.setattr("sys.stdout", outgoing)
    assert play(session) == "completed"
    assert r"月\x1b[2J" in outgoing.getvalue()
    assert r"Expected: Straße\x9b31m" in outgoing.getvalue()
    assert (card.front, card.back, card.card_id) == (
        "月\x1b[2J",
        "Straße\x9b31m",
        identity,
    )
    store = HistoryStore(tmp_path / "history.json")
    store.save_session(session.summary)
    assert dict(HistoryStore(store.path).scores) == {identity: 1}
    export = tmp_path / "session.json"
    export_results(export, session.summary, [card], "sequential", None, "completed")
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["missed"] == [
        {"position": 1, "card_id": identity, "front": card.front, "expected": card.back}
    ]
    correct = QuizSession([card], SequentialStrategy())
    assert correct.submit_answer("  STRASSE\x9b31m  ").correct is True
    assert correct.summary.answers[0].card == card
    history = HistoryStore(store.path)
    history.save_session(correct.summary)
    assert dict(HistoryStore(store.path).scores) == {identity: 0}
    literal = QuizSession([card], SequentialStrategy())
    assert literal.submit_answer(r"Straße\x9b31m").correct is False


def test_string_stream_configuration_and_control_display(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Injected streams work and displayed controls remain on one line."""
    incoming = StringIO("wrong\n")
    outgoing = StringIO()
    errors = StringIO()
    monkeypatch.setattr("sys.stdin", incoming)
    monkeypatch.setattr("sys.stdout", outgoing)
    monkeypatch.setattr("sys.stderr", errors)
    configure_streams()
    cards = [Flashcard("A\nB\tC", "Answer\rValue")]
    session = QuizSession(cards, SequentialStrategy())
    assert play(session) == "completed"
    show_summary(session.summary, cards, "completed")
    assert r"A\nB\tC" in outgoing.getvalue()
    assert r"Expected: Answer\rValue" in outgoing.getvalue()
    assert session.summary.answers[0].card.front == "A\nB\tC"
    assert errors.getvalue() == ""


def test_partial_summary_labels_duplicate_fronts_by_position() -> None:
    """Original positions distinguish missed questions that share a front."""
    cards = [Flashcard("bank", "finance"), Flashcard("bank", "river")]
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer("wrong")
    session.submit_answer("wrong")
    text = format_summary(session.summary, cards, "completed")
    assert "#1 bank; #2 bank" in text


def test_summary_programming_error_is_not_disguised(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Expected output handling must not hide a bug in summary formatting."""
    cards = [Flashcard("A", "Alpha")]
    summary = QuizSession(cards, SequentialStrategy()).summary

    def broken_format(*args: object) -> str:
        """Represent a programming bug outside the output operation."""
        raise RuntimeError("scripted formatting bug")

    monkeypatch.setattr("utils.terminal.format_summary", broken_format)
    with pytest.raises(RuntimeError, match="scripted formatting bug"):
        show_summary(summary, cards, "eof")
