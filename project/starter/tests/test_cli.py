"""Actual-entry-point integration tests, including explicit interruption injection."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from tests.cli_helpers import ROOT, run_cli, write_deck


def test_help_does_not_require_a_file_or_touch_history(tmp_path: Path) -> None:
    """The actual required-file parser still permits help before any I/O."""
    result = run_cli(["--help"], tmp_path)
    assert result.returncode == 0
    assert "--mode" in result.stdout and "--history" in result.stdout
    assert "--seed" in result.stdout and "--export" in result.stdout
    assert "--overwrite" in result.stdout
    assert result.stderr == ""
    assert not (tmp_path / "home").exists()


@pytest.mark.parametrize(
    "arguments",
    [
        [],
        ["--unknown"],
        ["--file", "x", "--mode", "unknown"],
        ["--file", "x", "--seed", "1"],
        ["--file", "x", "--overwrite"],
        ["--file", "x", "--mode", "random", "--seed", "not-an-integer"],
    ],
)
def test_invalid_arguments_exit_two(tmp_path: Path, arguments: list[str]) -> None:
    """Argparse reports usage errors before deck/history access."""
    result = run_cli(arguments, tmp_path)
    assert result.returncode == 2
    assert "usage:" in result.stderr and "error:" in result.stderr
    assert "Traceback" not in result.stderr
    assert "Completed session" not in result.stdout
    assert not (tmp_path / "home").exists()


@pytest.mark.parametrize("mode", ["sequential", "random", "adaptive"])
def test_all_modes_finish_and_update_history(tmp_path: Path, mode: str) -> None:
    """Wrong answers still complete successfully, once per card in every mode."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    args = [
        "-f",
        str(deck),
        "-m",
        mode,
        "--history",
        str(history),
        "--export",
        str(export),
    ]
    if mode == "random":
        args.extend(["--seed", "23"])
    before = deck.read_bytes()
    result = run_cli(args, tmp_path, "wrong\nwrong\nwrong\n")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.count("Incorrect. Expected:") == 3
    assert "Completed session (completed)" in result.stdout
    assert "0.00%" in result.stdout
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["version"] == 1 and document["mode"] == mode
    assert document["complete"] is True and document["answered_count"] == 3
    assert document["finish_reason"] == "completed"
    assert "answers" not in document
    assert sorted(card["position"] for card in document["missed"]) == [1, 2, 3]
    assert {card["front"]: card["position"] for card in document["missed"]} == {
        "A": 1,
        "B": 2,
        "C": 3,
    }
    assert sorted(card["front"] for card in document["missed"]) == ["A", "B", "C"]
    assert len({card["card_id"] for card in document["missed"]}) == 3
    assert sorted(re.findall(r"^\[\d+/\d+\] (.+)$", result.stdout, re.MULTILINE)) == [
        "A",
        "B",
        "C",
    ]
    stored = json.loads(history.read_text(encoding="utf-8"))
    assert set(stored["scores"].values()) == {1}
    assert len(stored["scores"]) == 3
    assert deck.read_bytes() == before


def test_two_correct_answers_feedback_and_summary(tmp_path: Path) -> None:
    """The public command provides immediate expected-answer feedback and totals."""
    deck = write_deck(tmp_path)
    result = run_cli(
        ["--file", str(deck), "--history", str(tmp_path / "history.json")],
        tmp_path,
        " alpha \nwrong\nGAMMA\n",
    )
    assert result.returncode == 0
    assert result.stdout.count("Answer: Correct") == 2
    assert "Incorrect. Expected: Beta" in result.stdout
    assert "66.67%" in result.stdout and "#2 B" in result.stdout


def test_seeded_randomness_reproduces_order(tmp_path: Path) -> None:
    """Same seed reproduces membership/order without demanding a changed shuffle."""
    deck = write_deck(tmp_path)
    orders: list[list[str]] = []
    for index in range(2):
        export = tmp_path / f"results-{index}.json"
        result = run_cli(
            [
                "--file",
                str(deck),
                "--mode",
                "random",
                "--seed",
                "7",
                "--history",
                str(tmp_path / f"history-{index}.json"),
                "--export",
                str(export),
            ],
            tmp_path,
            "wrong\nwrong\nwrong\n",
        )
        assert result.returncode == 0
        data = json.loads(export.read_text(encoding="utf-8"))
        assert data["seed"] == 7
        orders.append([entry["card_id"] for entry in data["missed"]])
        assert [entry["front"] for entry in data["missed"]] == re.findall(
            r"^\[\d+/\d+\] (.+)$", result.stdout, re.MULTILINE
        )
    assert orders[0] == orders[1]
    assert len(set(orders[0])) == 3


def test_history_reuse_changes_next_adaptive_order(tmp_path: Path) -> None:
    """A real first CLI run influences ordering and decay in the second."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    first = run_cli(
        ["-f", str(deck), "--history", str(history)], tmp_path, "alpha\nwrong\ngamma\n"
    )
    assert first.returncode == 0
    second = run_cli(
        ["-f", str(deck), "-m", "adaptive", "--history", str(history)],
        tmp_path,
        "beta\nalpha\ngamma\n",
    )
    assert second.returncode == 0
    assert re.findall(r"^\[\d+/\d+\] (.+)$", second.stdout, re.MULTILINE) == [
        "B",
        "A",
        "C",
    ]
    assert "100.00%" in second.stdout
    assert set(json.loads(history.read_text(encoding="utf-8"))["scores"].values()) == {
        0
    }


def test_default_history_path_uses_isolated_home(tmp_path: Path) -> None:
    """Omitting --history uses the documented location without touching real state."""
    deck = write_deck(tmp_path)
    result = run_cli(["-f", str(deck)], tmp_path, "alpha\nbeta\ngamma\n")
    assert result.returncode == 0
    assert (tmp_path / "home" / ".flashcard_quizzer" / "history.json").is_file()


@pytest.mark.parametrize(
    "kind", ["missing", "malformed", "schema", "empty", "encoding", "directory"]
)
def test_invalid_deck_files_fail_without_traceback(tmp_path: Path, kind: str) -> None:
    """Expected file failures produce no quiz, history, or export side effects."""
    deck = tmp_path / "deck.json"
    if kind == "directory":
        deck.mkdir()
    elif kind == "encoding":
        deck.write_bytes(b"\xff\xfeinvalid")
    elif kind != "missing":
        deck.write_text(
            {
                "malformed": "{bad",
                "schema": '{"cards":[{"front":true,"back":"x"}]}',
                "empty": "[]",
            }[kind],
            encoding="utf-8",
        )
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)], tmp_path
    )
    assert result.returncode == 1
    assert "Error: Cannot load flashcards" in result.stderr
    assert "Traceback" not in result.stderr
    assert "[1/" not in result.stdout and "session (" not in result.stdout
    assert not history.exists() and not export.exists()


def test_unreadable_deck_at_actual_entry_point(tmp_path: Path) -> None:
    """Inject a permission error at file reading, without a production fault flag."""
    deck = write_deck(tmp_path)
    result = run_cli(["-f", str(deck)], tmp_path, faults=["unreadable_deck"])
    assert result.returncode == 1
    assert "Permission denied reading file" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("unreadable", [False, True])
def test_bad_history_warns_preserves_bytes_and_still_exports(
    tmp_path: Path, unreadable: bool
) -> None:
    """Degraded history never prevents practice/export or overwrites old state."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    history.write_text("{bad history", encoding="utf-8")
    before = history.read_bytes()
    export = tmp_path / "results.json"
    result = run_cli(
        [
            "-f",
            str(deck),
            "-m",
            "adaptive",
            "--history",
            str(history),
            "--export",
            str(export),
        ],
        tmp_path,
        "alpha\nbeta\ngamma\n",
        faults=["history_read"] if unreadable else [],
    )
    assert result.returncode == 1
    assert "Previous scores could not be loaded." in result.stderr
    assert "Adaptive mode will use deck order." in result.stderr
    assert "Learning updates will not be saved during this run." in result.stderr
    assert str(history.resolve()) in result.stderr
    assert "Traceback" not in result.stderr
    assert history.read_bytes() == before
    assert export.is_file()
    assert "100.00%" in result.stdout
    assert re.findall(r"^\[\d+/\d+\] (.+)$", result.stdout, re.MULTILINE) == [
        "A",
        "B",
        "C",
    ]


def test_export_is_attempted_after_history_save_failure(tmp_path: Path) -> None:
    """The real entry point writes the export despite a structured save failure."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    history.write_text(
        '{"version":1,"policy":"error-balance-v1","scores":{}}', encoding="utf-8"
    )
    before = history.read_bytes()
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "alpha\nbeta\ngamma\n",
        faults=["history_save"],
    )
    assert result.returncode == 1
    assert "scripted history-save denial" in result.stderr
    assert "Learning updates were not saved" in result.stderr
    assert history.read_bytes() == before
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["answered_count"] == 3 and document["complete"] is True
    assert "100.00%" in result.stdout


def test_export_failure_keeps_history_and_summary(tmp_path: Path) -> None:
    """A directory export destination fails after a complete successful quiz."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    destination = tmp_path / "export-directory"
    destination.mkdir()
    result = run_cli(
        [
            "-f",
            str(deck),
            "--history",
            str(history),
            "--export",
            str(destination),
            "--overwrite",
        ],
        tmp_path,
        "alpha\nbeta\ngamma\n",
    )
    assert result.returncode == 1
    assert "Cannot export results" in result.stderr and "Traceback" not in result.stderr
    assert "Could not write results" in result.stderr
    assert history.is_file() and destination.is_dir()
    assert "Completed session" in result.stdout and "100.00%" in result.stdout
    assert not list(tmp_path.glob(".export-directory.*.tmp"))


def test_export_refusal_and_overwrite_leave_history_updates_independent(
    tmp_path: Path,
) -> None:
    """Export refusal preserves bytes while existing history continues updating."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    args = ["-f", str(deck), "--history", str(history), "--export", str(export)]
    private = "PRIVATE submitted text 7"
    first = run_cli(args, tmp_path, (private + "\n") * 3)
    assert first.returncode == 0
    original = export.read_bytes()
    assert private not in original.decode("utf-8")
    assert "answers" not in json.loads(original)

    refused = run_cli(args, tmp_path, (private + "\n") * 3)
    assert refused.returncode == 1
    assert "use --overwrite" in refused.stderr
    assert "Completed session" in refused.stdout
    assert export.read_bytes() == original
    scores = json.loads(history.read_text(encoding="utf-8"))["scores"]
    assert len(scores) == 3 and set(scores.values()) == {2}

    authorized = run_cli([*args, "--overwrite"], tmp_path, "alpha\nbeta\ngamma\n")
    assert authorized.returncode == 0
    replacement = json.loads(export.read_text(encoding="utf-8"))
    assert replacement["correct_count"] == 3
    assert replacement["missed"] == [] and "answers" not in replacement
    assert export.read_bytes() != original
    scores = json.loads(history.read_text(encoding="utf-8"))["scores"]
    assert len(scores) == 3 and set(scores.values()) == {1}


def test_existing_export_refusal_does_not_override_ctrl_c(tmp_path: Path) -> None:
    """A preserved existing export is still a secondary failure after interruption."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    export.write_bytes(b"existing export")
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "alpha\n",
        faults=["interrupt_after_one"],
    )
    assert result.returncode == 130
    assert "use --overwrite" in result.stderr
    assert export.read_bytes() == b"existing export"
    assert len(json.loads(history.read_text(encoding="utf-8"))["scores"]) == 1


@pytest.mark.parametrize("pair", ["deck-history", "deck-export", "history-export"])
@pytest.mark.parametrize("overwrite", [False, True])
def test_conflicting_roles_are_rejected_before_quiz(
    tmp_path: Path, pair: str, overwrite: bool
) -> None:
    """Equal destinations are invalid even when both output files are absent."""
    deck = write_deck(tmp_path)
    before = deck.read_bytes()
    history = deck if pair == "deck-history" else tmp_path / "history.json"
    export = (
        deck
        if pair == "deck-export"
        else history if pair == "history-export" else tmp_path / "results.json"
    )
    args = ["-f", str(deck), "--history", str(history), "--export", str(export)]
    if overwrite:
        args.append("--overwrite")
    result = run_cli(args, tmp_path)
    assert result.returncode == 2
    assert "refer to the same file" in result.stderr
    assert "[1/" not in result.stdout
    assert deck.read_bytes() == before
    if history != deck:
        assert not history.exists()


def test_resolved_relative_path_conflict(tmp_path: Path) -> None:
    """Argument strings differ while the resolved export still targets the deck."""
    deck = write_deck(tmp_path)
    folder = tmp_path / "folder"
    folder.mkdir()
    alias = folder / ".." / "deck.json"
    result = run_cli(
        [
            "-f",
            str(deck),
            "--history",
            str(tmp_path / "history.json"),
            "--export",
            str(alias),
        ],
        tmp_path,
    )
    assert result.returncode == 2 and "refer to the same file" in result.stderr


def test_history_and_export_hard_link_aliases_are_rejected(tmp_path: Path) -> None:
    """Existing outputs must be checked against each other, not only the deck."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    history.write_text(
        '{"version":1,"policy":"error-balance-v1","scores":{}}', encoding="utf-8"
    )
    try:
        os.link(history, export)
    except (OSError, NotImplementedError) as failure:
        pytest.skip(f"Hard links unavailable: {failure}")
    before = history.read_bytes()
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)], tmp_path
    )
    assert result.returncode == 2 and "refer to the same file" in result.stderr
    assert history.read_bytes() == export.read_bytes() == before


@pytest.mark.parametrize("link_type", ["hard", "symbolic"])
def test_existing_file_alias_conflict(tmp_path: Path, link_type: str) -> None:
    """Check actual filesystem aliases, skipping only unavailable link support."""
    deck = write_deck(tmp_path)
    alias = tmp_path / "alias.json"
    try:
        if link_type == "hard":
            os.link(deck, alias)
        else:
            alias.symlink_to(deck)
    except (OSError, NotImplementedError) as failure:
        pytest.skip(f"{link_type} links unavailable: {failure}")
    before = deck.read_bytes()
    result = run_cli(["-f", str(deck), "--history", str(alias)], tmp_path)
    assert result.returncode == 2
    assert "refer to the same file" in result.stderr
    assert deck.read_bytes() == alias.read_bytes() == before


@pytest.mark.parametrize("answers", ["", "alpha\n"])
def test_eof_exports_partial_summary_and_saves_completed_history(
    tmp_path: Path, answers: str
) -> None:
    """EOF excludes the pending card and keeps no-answer accuracy as JSON null/N/A."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        answers,
    )
    assert result.returncode == 1 and "(EOF)" in result.stderr
    assert "Partial session (eof)" in result.stdout
    document = json.loads(export.read_text(encoding="utf-8"))
    count = 1 if answers else 0
    assert document["answered_count"] == count and document["correct_count"] == count
    assert document["complete"] is False and document["finish_reason"] == "eof"
    assert document["missed"] == []
    if count:
        assert document["accuracy_percent"] == 100
        assert len(json.loads(history.read_text(encoding="utf-8"))["scores"]) == 1
    else:
        assert document["accuracy_percent"] is None
        assert "N/A" in result.stdout and not history.exists()


@pytest.mark.parametrize("after_one", [False, True])
def test_ctrl_c_exports_partial_results_and_returns_130(
    tmp_path: Path, after_one: bool
) -> None:
    """Inject Python's Ctrl+C exception at input while executing actual main.py."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    result = run_cli(
        ["-f", str(deck), "--history", str(history), "--export", str(export)],
        tmp_path,
        "alpha\n",
        faults=["interrupt_after_one" if after_one else "interrupt_before"],
    )
    assert result.returncode == 130
    assert "Interrupted by Ctrl+C" in result.stderr and "Traceback" not in result.stderr
    assert "Partial session (interrupted)" in result.stdout
    document = json.loads(export.read_text(encoding="utf-8"))
    assert document["finish_reason"] == "interrupted"
    assert document["answered_count"] == (1 if after_one else 0)
    assert history.exists() is after_one


@pytest.mark.parametrize("export_fails", [False, True])
def test_ctrl_c_wins_even_when_history_save_and_export_fail(
    tmp_path: Path, export_fails: bool
) -> None:
    """Status 130 takes precedence, and export is attempted after failed saving."""
    deck = write_deck(tmp_path)
    history = tmp_path / "history.json"
    export = tmp_path / "results.json"
    if export_fails:
        export.mkdir()
    args = ["-f", str(deck), "--history", str(history), "--export", str(export)]
    if export_fails:
        args.append("--overwrite")
    result = run_cli(
        args,
        tmp_path,
        "alpha\n",
        faults=["interrupt_after_one", "history_save"],
    )
    assert result.returncode == 130
    assert "scripted history-save denial" in result.stderr
    assert "Traceback" not in result.stderr
    if export_fails:
        assert "Cannot export results" in result.stderr
        assert "Could not write results" in result.stderr
    else:
        assert json.loads(export.read_text(encoding="utf-8"))["answered_count"] == 1


@pytest.mark.parametrize(
    "fault", ["interrupt_history_save", "interrupt_export", "interrupt_summary"]
)
def test_interrupt_during_finalization_still_returns_130(
    tmp_path: Path, fault: str
) -> None:
    """An interruption after answering cannot become a success or ordinary failure."""
    deck = write_deck(tmp_path)
    export = tmp_path / "results.json"
    result = run_cli(
        [
            "-f",
            str(deck),
            "--history",
            str(tmp_path / "history.json"),
            "--export",
            str(export),
        ],
        tmp_path,
        "alpha\nbeta\ngamma\n",
        faults=[fault],
    )
    assert result.returncode == 130 and "Traceback" not in result.stderr
    if fault != "interrupt_export":
        document = json.loads(export.read_text(encoding="utf-8"))
        assert document["finish_reason"] == "interrupted"
        assert document["answered_count"] == 3


@pytest.mark.parametrize(
    "fault", ["input_error", "path_inspection", "default_home", "interrupt_before_quiz"]
)
def test_other_expected_operational_boundaries(tmp_path: Path, fault: str) -> None:
    """Expected environment/input failures remain helpful, with interrupt priority."""
    deck = write_deck(tmp_path)
    args = ["-f", str(deck), "--export", str(tmp_path / "results.json")]
    if fault not in {"default_home", "interrupt_before_quiz"}:
        args.extend(["--history", str(tmp_path / "history.json")])
    result = run_cli(args, tmp_path, faults=[fault])
    assert result.returncode == (130 if fault == "interrupt_before_quiz" else 1)
    assert "Traceback" not in result.stderr
    if fault == "input_error":
        document = json.loads((tmp_path / "results.json").read_text(encoding="utf-8"))
        assert (
            document["finish_reason"] == "input_error"
            and document["answered_count"] == 0
        )
    else:
        assert "session (" not in result.stdout


def test_unicode_input_and_output(tmp_path: Path) -> None:
    """The native Windows subprocess reads/writes UTF-8 rather than locale-loss text."""
    deck = tmp_path / "deck.json"
    deck.write_text('[{"front":"\u6708","back":"Stra\u00dfe"}]', encoding="utf-8")
    result = run_cli(
        ["-f", str(deck), "--history", str(tmp_path / "history.json")],
        tmp_path,
        "STRASSE\n",
    )
    assert result.returncode == 0 and "\u6708" in result.stdout
    assert "100.00%" in result.stdout


def test_importing_entry_point_does_not_start_quiz() -> None:
    """The thin __main__ guard keeps imports safe for tooling and callers."""
    result = subprocess.run(
        [sys.executable, "-c", "import main; print('imported')"],
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=30,
    )
    assert result.returncode == 0 and result.stdout.strip() == "imported"
    assert result.stderr == ""
