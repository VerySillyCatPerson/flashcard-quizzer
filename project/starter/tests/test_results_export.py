"""Result schema details and preservation on expected export write failures."""

import json
import os
from pathlib import Path
from typing import NoReturn

import pytest

from utils.engine import QuizSession
from utils.models import Flashcard
from utils.results_export import ResultsExportError, export_results, results_document
from utils.strategies import SequentialStrategy


def test_partial_export_omits_submitted_text_and_keeps_missed_position(
    cards: list[Flashcard], tmp_path: Path
) -> None:
    """Export is limited to metadata/statistics/misses, without submitted text."""
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer(" application programming interface ")
    session.submit_answer("PRIVATE submitted text 7")
    destination = tmp_path / "new" / "results.json"
    export_results(destination, session.summary, cards, "sequential", None, "eof")
    data = json.loads(destination.read_text(encoding="utf-8"))
    assert data["complete"] is False and data["answered_count"] == 2
    assert data["accuracy_percent"] == 50
    assert "answers" not in data
    assert "PRIVATE submitted text 7" not in destination.read_text(encoding="utf-8")
    assert " application programming interface " not in destination.read_text(
        encoding="utf-8"
    )
    assert set(data) == {
        "version",
        "mode",
        "seed",
        "finish_reason",
        "complete",
        "deck_size",
        "answered_count",
        "correct_count",
        "accuracy_percent",
        "missed",
    }
    assert data["missed"] == [
        {
            "position": 2,
            "card_id": cards[1].card_id,
            "front": cards[1].front,
            "expected": cards[1].back,
        }
    ]
    assert "path" not in data and "history" not in data


def test_zero_answer_result_is_json_null(cards: list[Flashcard]) -> None:
    """No-answer performance is unknown, not a zero percent score."""
    summary = QuizSession(cards, SequentialStrategy()).summary
    data = results_document(summary, cards, "random", 7, "interrupted")
    assert data["accuracy_percent"] is None
    assert "answers" not in data and data["missed"] == []
    assert data["seed"] == 7 and data["finish_reason"] == "interrupted"


@pytest.mark.parametrize("boundary", ["replace", "fsync"])
def test_failed_export_preserves_previous_file(
    tmp_path: Path,
    cards: list[Flashcard],
    monkeypatch: pytest.MonkeyPatch,
    boundary: str,
) -> None:
    """An expected write failure leaves the old export intact and cleans staging."""
    path = tmp_path / "results.json"
    path.write_text('{"old":true}', encoding="utf-8")
    before = path.read_bytes()
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer("wrong")

    def denied(*args: object, **kwargs: object) -> NoReturn:
        """Inject an expected OS failure at the chosen export operation."""
        raise PermissionError("scripted export denial")

    monkeypatch.setattr(f"utils.results_export.os.{boundary}", denied)
    with pytest.raises(ResultsExportError, match="Could not write results"):
        export_results(
            path, session.summary, cards, "sequential", None, "eof", overwrite=True
        )
    assert path.read_bytes() == before
    assert set(tmp_path.iterdir()) == {path}


def test_existing_export_is_refused_without_changing_bytes(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """The default call cannot replace an existing export or create staging files."""
    path = tmp_path / "results.json"
    path.write_bytes(b"existing export bytes\x00\xff")
    before = path.read_bytes()
    summary = QuizSession(cards, SequentialStrategy()).summary
    with pytest.raises(ResultsExportError, match="use --overwrite"):
        export_results(path, summary, cards, "sequential", None, "eof")
    assert path.read_bytes() == before
    assert set(tmp_path.iterdir()) == {path}


def test_explicit_overwrite_atomically_replaces_existing_export(
    tmp_path: Path, cards: list[Flashcard]
) -> None:
    """Replacement remains available only through explicit authorization."""
    path = tmp_path / "results.json"
    path.write_bytes(b"old content")
    session = QuizSession(cards, SequentialStrategy())
    session.submit_answer("wrong")
    export_results(
        path, session.summary, cards, "sequential", None, "eof", overwrite=True
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["answered_count"] == 1
    assert "answers" not in data
    assert set(tmp_path.iterdir()) == {path}


def test_file_created_after_absence_check_is_not_overwritten(
    tmp_path: Path, cards: list[Flashcard], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exclusive publication protects a destination that appears while staging."""
    path = tmp_path / "results.json"
    original_link = os.link

    def publish_after_competing_writer(source: Path, destination: Path) -> None:
        """Create another writer's bytes immediately before publication."""
        destination.write_bytes(b"created by another writer")
        original_link(source, destination)

    monkeypatch.setattr("utils.results_export.os.link", publish_after_competing_writer)
    with pytest.raises(ResultsExportError, match="use --overwrite"):
        export_results(
            path,
            QuizSession(cards, SequentialStrategy()).summary,
            cards,
            "sequential",
            None,
            "eof",
        )
    assert path.read_bytes() == b"created by another writer"
    assert set(tmp_path.iterdir()) == {path}
