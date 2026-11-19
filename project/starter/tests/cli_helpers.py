"""Run the actual entry point in isolated subprocesses, with explicit fault hooks."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]

# Test-only subprocess bootstrap: runpy executes main.py's real __main__ guard.
# No production code reads these environment variables or exposes fault flags.
_BOOTSTRAP = r"""
import builtins
import json
import os
import runpy
import sys
from pathlib import Path
from typing import Mapping
import utils.cli as cli
import utils.history as history
import utils.terminal as terminal
from utils.models import SessionSummary

faults = set(json.loads(os.environ['FLASHCARD_TEST_FAULTS']))
original_input = builtins.input
input_count = 0


def controlled_input(prompt: str = '') -> str:
    '''Inject input failures at the requested completed-answer boundary.'''
    global input_count
    if ('interrupt_before' in faults or
            ('interrupt_after_one' in faults and input_count == 1)):
        raise KeyboardInterrupt
    if 'input_error' in faults:
        raise OSError('scripted input failure')
    input_count += 1
    return original_input(prompt)


builtins.input = controlled_input

if 'history_save' in faults or 'interrupt_history_save' in faults:
    def fail_history(path: Path, scores: Mapping[str, int]) -> None:
        '''Fail or interrupt a history write before committing it.'''
        if 'interrupt_history_save' in faults:
            raise KeyboardInterrupt
        raise history.HistorySaveError(path, 'scripted history-save denial')
    history._atomic_save = fail_history
if 'history_read' in faults:
    def fail_read(path: Path) -> dict[str, int]:
        '''Deny history loading without touching the existing file.'''
        raise history.HistoryLoadError(
            path, 'scripted permission denial reading history')
    history._read_scores = fail_read
if 'unreadable_deck' in faults:
    original_read_text = Path.read_text

    def denied_read(
        self: Path, encoding: str | None = None, errors: str | None = None
    ) -> str:
        '''Deny only the test deck while retaining other file reads.'''
        if self.name == 'deck.json':
            raise PermissionError('scripted deck permission denial')
        return original_read_text(self, encoding=encoding, errors=errors)
    Path.read_text = denied_read
if 'path_inspection' in faults:
    def denied_identity(self: Path, other_path: Path) -> bool:
        '''Simulate an expected existing-file identity inspection failure.'''
        raise PermissionError('scripted identity inspection denial')
    Path.samefile = denied_identity
if 'default_home' in faults or 'interrupt_before_quiz' in faults:
    def denied_home() -> Path:
        '''Fail default-history discovery or interrupt before quiz setup.'''
        if 'interrupt_before_quiz' in faults:
            raise KeyboardInterrupt
        raise RuntimeError('scripted unavailable home')
    cli.default_history_path = denied_home
if 'startup_warning_pipe' in faults:
    original_warning = terminal.warn

    def warning_into_closed_pipe(message: str) -> None:
        '''Exercise the real startup warning against a closed native pipe.'''
        previous_stderr = sys.stderr
        read_fd, write_fd = os.pipe()
        os.close(read_fd)
        broken_stream = os.fdopen(write_fd, 'w', encoding='utf-8')
        sys.stderr = broken_stream
        try:
            original_warning(message)
        finally:
            if 'leave_warning_pipe_broken' not in faults:
                sys.stderr = previous_stderr
                try:
                    broken_stream.close()
                except OSError:
                    pass

    terminal.warn = warning_into_closed_pipe
if 'startup_warning_programming_error' in faults:
    def unexpected_warning_error(message: str) -> None:
        '''Expose an unexpected programming error from the startup handler.'''
        raise RuntimeError('unexpected startup warning defect')

    terminal.warn = unexpected_warning_error
if 'interrupt_export' in faults:
    def interrupted_export(*args: object, **kwargs: object) -> None:
        '''Interrupt the export phase without reporting a successful write.'''
        raise KeyboardInterrupt
    cli.export_results = interrupted_export
if 'interrupt_summary' in faults:
    def interrupted_summary(*args: object, **kwargs: object) -> None:
        '''Interrupt summary display after answers have been completed.'''
        raise KeyboardInterrupt
    terminal.show_summary = interrupted_summary

finalization_faults = {
    'interrupt_history_guard', 'interrupt_after_history_commit',
    'history_interrupt_before_commit', 'history_interrupt_after_replace',
    'summary_closed_pipe',
    'quiz_output_failure',
}
if faults & finalization_faults:
    original_save_session = history.HistoryStore.save_session
    save_committed = False

    def traced_save(self: history.HistoryStore, summary: SessionSummary) -> None:
        '''Record each attempt, including a deliberately uncertain write.'''
        global save_committed
        with Path(os.environ['FLASHCARD_TEST_TRACE']).open(
                'a', encoding='utf-8') as trace:
            trace.write('history\n')
        if 'history_interrupt_before_commit' in faults:
            raise KeyboardInterrupt
        original_save_session(self, summary)
        save_committed = True
    history.HistoryStore.save_session = traced_save

if 'interrupt_history_guard' in faults:
    original_can_save = history.HistoryStore.can_save.fget
    guard_interrupted = False

    def interrupt_guard_once(self: history.HistoryStore) -> bool:
        '''Interrupt a read-only phase check once, before any save attempt.'''
        global guard_interrupted
        if not guard_interrupted:
            guard_interrupted = True
            raise KeyboardInterrupt
        return original_can_save(self)
    history.HistoryStore.can_save = property(interrupt_guard_once)

if 'interrupt_after_history_commit' in faults:
    original_getattribute = cli.QuizPaths.__getattribute__
    boundary_interrupted = False

    def interrupt_export_boundary_once(self: cli.QuizPaths, name: str) -> object:
        '''Interrupt between a successful history commit and export selection.'''
        global boundary_interrupted
        if name == 'export' and save_committed and not boundary_interrupted:
            boundary_interrupted = True
            raise KeyboardInterrupt
        return original_getattribute(self, name)
    cli.QuizPaths.__getattribute__ = interrupt_export_boundary_once

if 'history_interrupt_after_replace' in faults:
    original_replace = history.os.replace
    history_destination = Path(sys.argv[sys.argv.index('--history') + 1])

    def replace_then_interrupt(source: Path, destination: Path) -> None:
        '''Commit the real file, then interrupt before memory adopts the score.'''
        original_replace(source, destination)
        if Path(destination) == history_destination:
            raise KeyboardInterrupt
    history.os.replace = replace_then_interrupt

if 'summary_closed_pipe' in faults:
    original_show_summary = terminal.show_summary

    def summary_into_closed_pipe(*args: object, **kwargs: object) -> None:
        '''Exercise the original printer against a real unavailable reader.'''
        previous_stdout = sys.stdout
        read_fd, write_fd = os.pipe()
        os.close(read_fd)
        broken_stream = os.fdopen(write_fd, 'w', encoding='utf-8')
        sys.stdout = broken_stream
        try:
            original_show_summary(*args, **kwargs)
        finally:
            if 'leave_summary_pipe_broken' not in faults:
                sys.stdout = previous_stdout
                try:
                    broken_stream.close()
                except OSError:
                    pass
    terminal.show_summary = summary_into_closed_pipe

if 'quiz_output_failure' in faults:
    def fail_feedback(*args: object, **kwargs: object) -> None:
        '''Fail only the output operation after an answer has been recorded.'''
        if args and str(args[0]).startswith('Incorrect. Expected:'):
            raise OSError('scripted quiz output failure')
        builtins.print(*args, **kwargs)
    terminal.print = fail_feedback

sys.argv = ['main.py', *sys.argv[1:]]
runpy.run_path('main.py', run_name='__main__')
"""


def run_cli(
    arguments: Sequence[str],
    tmp_path: Path,
    answers: str = "",
    *,
    faults: Sequence[str] = (),
) -> subprocess.CompletedProcess[str]:
    """Run main.py with isolated home/history, capturing actual streams and status."""
    environment = os.environ.copy()
    environment["HOME"] = str(tmp_path / "home")
    environment["USERPROFILE"] = str(tmp_path / "home")
    command = [sys.executable]
    if faults:
        environment["FLASHCARD_TEST_FAULTS"] = json.dumps(list(faults))
        environment["FLASHCARD_TEST_TRACE"] = str(tmp_path / "save-attempts.txt")
        command.extend(["-c", _BOOTSTRAP])
    else:
        command.append("main.py")
    return subprocess.run(
        [*command, *arguments],
        input=answers,
        text=True,
        encoding="utf-8",
        capture_output=True,
        cwd=ROOT,
        env=environment,
        timeout=30,
    )


def write_deck(tmp_path: Path) -> Path:
    """Create a compact three-card native-entry-point fixture."""
    path = tmp_path / "deck.json"
    path.write_text(
        '[{"front":"A","back":"Alpha"},{"front":"B","back":"Beta"},'
        '{"front":"C","back":"Gamma"}]',
        encoding="utf-8",
    )
    return path
