"""Stage 7 regressions through main.py, including real interrupted commits."""

import json
from pathlib import Path

import pytest

from tests.cli_helpers import run_cli, write_deck
from utils.models import Flashcard


@pytest.mark.parametrize("warning", ["healthy", "restored_pipe", "permanent_pipe"])
def test_startup_interrupt_retains_130_when_warning_output_fails(
    tmp_path: Path, warning: str
) -> None:
    """Expected warning failures preserve interruption without pre-quiz writes."""
    deck = write_deck(tmp_path)
    before = deck.read_bytes()
    export = tmp_path / "results.json"
    faults = ["interrupt_before_quiz"]
    if warning != "healthy":
        faults.append("startup_warning_pipe")
    if warning == "permanent_pipe":
        faults.append("leave_warning_pipe_broken")
    result = run_cli(
        ["-f", str(deck), "--export", str(export)], tmp_path, faults=faults
    )
    assert result.returncode == 130, result.stderr
    assert "Traceback" not in result.stderr
    assert "Exception ignored" not in result.stderr
    assert result.stdout == ""
    if warning == "healthy":
        assert "Interrupted by Ctrl+C before quiz finalization." in result.stderr
    assert not export.exists()
    assert not (tmp_path / "home").exists()
    assert deck.read_bytes() == before


def test_startup_interrupt_does_not_hide_warning_programming_errors(
    tmp_path: Path,
) -> None:
    """Only expected terminal errors are caught inside the interrupt handler."""
    deck = write_deck(tmp_path)
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--export", str(export)],
        tmp_path,
        faults=["interrupt_before_quiz", "startup_warning_programming_error"],
    )
    assert result.returncode == 1
    assert "Traceback" in result.stderr
    assert "RuntimeError: unexpected startup warning defect" in result.stderr
    assert result.stdout == ""
    assert not export.exists()
    assert not (tmp_path / "home").exists()


def _existing_history(tmp_path: Path) -> tuple[Path, str]:
    """Start A at score two so a lost or duplicated update is observable."""
    card_id = Flashcard("A", "Alpha").card_id
    history = tmp_path / "history.json"
    history.write_text(
        json.dumps(
            {"version": 1, "policy": "error-balance-v1", "scores": {card_id: 2}}
        ),
        encoding="utf-8",
    )
    return history, card_id


@pytest.mark.parametrize(
    "fault", ["interrupt_history_guard", "interrupt_after_history_commit"]
)
def test_between_phase_interrupt_continues_pending_work_once(
    tmp_path: Path, fault: str
) -> None:
    """A one-shot transition interrupt resumes pending work, never committed work."""
    deck = write_deck(tmp_path)
    history, card_id = _existing_history(tmp_path)
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "private raw reply\n",
        faults=[fault],
    )
    assert result.returncode == 130
    assert json.loads(history.read_text(encoding="utf-8"))["scores"][card_id] == 3
    assert export.exists(), result.stderr
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["answered_count"] == 1
    assert document["finish_reason"] == "interrupted"
    assert "answers" not in document
    assert "private raw reply" not in export.read_text(encoding="utf-8")
    assert (tmp_path / "save-attempts.txt").read_text().splitlines() == ["history"]
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("after_input_interrupt", [False, True])
@pytest.mark.parametrize("keep_broken", [False, True])
def test_summary_output_failure_keeps_writes_and_exit_precedence(
    tmp_path: Path, after_input_interrupt: bool, keep_broken: bool
) -> None:
    """A native summary-output error cannot prevent either persistence phase."""
    deck = write_deck(tmp_path)
    history, card_id = _existing_history(tmp_path)
    export = tmp_path / "results.json"
    faults = ["summary_closed_pipe"]
    if keep_broken:
        faults.append("leave_summary_pipe_broken")
    if after_input_interrupt:
        faults.append("interrupt_after_one")
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "private raw reply\n",
        faults=faults,
    )
    assert result.returncode == (130 if after_input_interrupt else 1)
    assert "Traceback" not in result.stderr
    assert "Exception ignored" not in result.stderr
    assert "Could not write terminal output" in result.stderr
    assert json.loads(history.read_text(encoding="utf-8"))["scores"][card_id] == 3
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["answered_count"] == 1 and document["correct_count"] == 0
    assert document["finish_reason"] == (
        "interrupted" if after_input_interrupt else "eof"
    )
    assert "answers" not in document
    assert "private raw reply" not in export.read_text(encoding="utf-8")
    assert (tmp_path / "save-attempts.txt").read_text().splitlines() == ["history"]


@pytest.mark.parametrize("after_replace", [False, True])
def test_uncertain_history_write_is_not_retried_and_export_continues(
    tmp_path: Path, after_replace: bool
) -> None:
    """An interrupted attempt may or may not commit; neither outcome is replayed."""
    deck = write_deck(tmp_path)
    history, card_id = _existing_history(tmp_path)
    export = tmp_path / "results.json"
    fault = (
        "history_interrupt_after_replace"
        if after_replace
        else "history_interrupt_before_commit"
    )
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "private raw reply\n",
        faults=[fault],
    )
    assert result.returncode == 130
    assert "persistence is not confirmed" in result.stderr
    assert "Traceback" not in result.stderr
    expected_score = 3 if after_replace else 2
    assert json.loads(history.read_text(encoding="utf-8"))["scores"][card_id] == (
        expected_score
    )
    assert (tmp_path / "save-attempts.txt").read_text().splitlines() == ["history"]
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["answered_count"] == 1
    assert document["finish_reason"] == "interrupted"
    assert "answers" not in document
    assert "private raw reply" not in export.read_text(encoding="utf-8")


def test_feedback_output_error_saves_the_completed_answer(tmp_path: Path) -> None:
    """An output failure immediately after grading still finalizes that answer."""
    deck = write_deck(tmp_path)
    history, card_id = _existing_history(tmp_path)
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "private raw reply\n",
        faults=["quiz_output_failure"],
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "scripted quiz output failure" in result.stderr
    assert json.loads(history.read_text(encoding="utf-8"))["scores"][card_id] == 3
    assert (tmp_path / "save-attempts.txt").read_text().splitlines() == ["history"]
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["answered_count"] == 1
    assert document["finish_reason"] == "output_error"
    assert "answers" not in document
    assert "private raw reply" not in export.read_text(encoding="utf-8")
