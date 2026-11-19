"""Terminal-only escaping and formatting, without changing domain text."""

from io import StringIO

import pytest

from utils.engine import QuizSession
from utils.models import Flashcard
from utils.strategies import SequentialStrategy
from utils.terminal import configure_streams, format_summary, play, show_summary


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
