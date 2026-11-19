# Stage 7: F1/F2 fixes for review

Date: 2026-11-18. The user approved fixes for the two findings in
[the initial Stage 7 review](stage_7_review.md), with regression failures captured
before production changes. This implementation awaits review; Stage 8 has not begun.
Physical keyboard Ctrl+C remains **unverified**.

## Regression-first evidence

Original source and hashes were saved in
[stage_7_fix_manifest.json](verification/stage_7_fix_manifest.json).
The first test-bootstrap collection attempt contained a nested string-delimiter
mistake; it was corrected before the valid red run. Both attempts are preserved.

Against unchanged production code, the six proposed cases produced **four failed,
two passed**. F1 failed at the history permission guard and at the export boundary
after history committed. F2 failed after EOF and after an input interruption.
The two passing cases protected the existing no-retry behavior for uncertain writes.
Adding a feedback-output case and a programming-error safeguard, still before
implementation, produced **five failed, five passed**, including existing terminal tests.

The first correction passed the full suite (269 passed, one skipped), but a further
F2 check left the failed stdout pipe installed through process shutdown. Python's
shutdown flush changed status to **120** and emitted ignored-exception output.
The permanent-pipe regressions were then added before the shutdown correction:
**two failed, seven passed**. Initial check/hash evidence and the diagnostic probe
were retained. The final focused set has **12 passing tests**.

Evidence:
[initial red](verification/stage_7_fix_red.json),
[expanded red](verification/stage_7_fix_expanded_red.json),
[shutdown probe](verification/stage_7_fix_shutdown_probe.json),
[shutdown red](verification/stage_7_fix_shutdown_red.json),
[final checks](verification/stage_7_fix_checks.json).

## Changes and ownership

`utils/cli.py::_finalize` retains the next pending phase: display, history,
export, then diagnostics. An outer interrupt handler covers read-only preparation
and transitions. A one-shot interrupt marks the session interrupted and continues
pending work. Status 130 takes precedence over operational failures.

Each side effect is marked attempted immediately before invocation. When a history
or export write raises KeyboardInterrupt, the coordinator reports that its outcome
is unconfirmed and proceeds without retrying that operation. A successful history
commit is also never replayed when export preparation is interrupted. This uses
local phase state rather than a new persistence protocol or schema.

The engine still owns completed answers; `HistoryStore.save_session` derives the
updated scores and adopts them in memory after successful persistence.
`history._atomic_save` owns file writing/replacement. The CLI owns attempt/retry
policy and presentation sequencing. None of those history implementations changed.

`utils/terminal.py::_write` wraps only print/flush, translating expected
`OSError`/`UnicodeError` into `TerminalOutputError`. Text formatting occurs outside
that catch; the RuntimeError regression confirms that a formatting bug remains
visible. A failed native stream descriptor is redirected to the null device so
Python cannot retry the failed buffered flush at shutdown and override the exit
status. Buffered output on that failed stream is discarded; stderr carries a
diagnostic when usable.

A structured output error during quiz feedback also finalizes the answer already
graded. Its metadata finish reason is `output_error`, an addition to the typed
FinishReason literal. A summary failure preserves the existing session finish
reason, such as `eof` or `interrupted`, while the exit remains operational failure
or interruption. The main entry point remains thin.

Production changes are limited to CLI orchestration, terminal I/O, and that typed
finish reason. Test changes are the test-only subprocess fault bootstrap, focused
finalization regressions, and the terminal programming-error safeguard. README
and the existing Stage 7 interaction-log entry document the resulting behavior.

## Actual before/after results

All runs use the real main.py guard with synthetic decks and isolated temporary
files. A starts at score 2 and receives one incorrect answer. Attempt counts come
from a test-only wrapper around HistoryStore.save_session.

| Scenario | Original code | Final code |
| --- | --- | --- |
| Interrupt at history permission guard | 130; score 2; no export; zero save attempts | 130; score 3; export; one attempt |
| Interrupt after committed history, before export | 130; score 3; no export; one attempt | 130; score 3; export; one attempt |
| Summary closed pipe after EOF | 1; traceback; score 2; no export | 1; no traceback; score 3; export |
| Summary closed pipe after input interruption | 1; traceback; score 2; no export | 130; no traceback; score 3; export |
| Interrupt before history commit | 130; score 2; export; one attempt | Same |
| Interrupt immediately after real history replacement | 130; score 3; export; one attempt | Same |

The permanent-pipe cases additionally verify the final statuses through interpreter
shutdown: **1 after EOF, 130 after interruption**, with neither traceback nor ignored
shutdown-exception output. Both persist score 3 and export the completed answer.
The feedback-output case returns 1, persists score 3 once, and exports one answer's
statistics with finish reason output_error.

Full stdout/stderr, arguments, score/attempt observations, and exported documents:
[before commands](verification/stage_7_fix_before_commands.json) and
[after commands](verification/stage_7_fix_after_commands.json).

## Uncertain write outcomes

The after-replacement regression performs the real os.replace and then interrupts
before the store adopts the candidate score in memory. The file already contains
score 3 even though the call did not report success. The precommit case leaves 2.
The coordinator attempts saving once in both cases and still exports session
statistics. It does not infer that an exception means no commit occurred, reload
the file and reapply the answer, or trust can_save as proof of noncommit.

Marking an attempt immediately before its call is conservative: interruption at
that handoff is treated as an uncertain attempt. There is no atomic Python-level
transaction covering method entry, filesystem replacement, and in-memory state.
Explicit retry after a known structured HistorySaveError remains supported by the
unchanged store and its existing tests; automatic retry after KeyboardInterrupt
is deliberately avoided.

An interrupted export may likewise leave a complete file already published.
The coordinator neither retries nor rewrites it to record a later interruption;
its outcome is reported as unconfirmed. Status 130 still wins.

## Preserved behavior and checks

Exports remain metadata, statistics and missed cards only. The new tests assert
that their private synthetic answer text is absent. Existing tests still verify
default byte-preserving refusal, late-arriving destination protection, explicit
atomic overwrite, all role conflicts, export after history-save failure, and
history preservation after export failure. Export implementation and optional
export error-boundary tests are unchanged.

Final full command:

```powershell
.\.venv\Scripts\python.exe -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json
```

Actual result: **271 passed, one skipped in 20.80 seconds**; coverage **98.20%**,
599 statements, 124 branches, nine missing statements and four partial branches.
Black, isort, flake8 and strict mypy all exit 0. Python 3.10 grammar parsing passes
for all 24 Python files; runtime testing is Windows CPython 3.13.17.

The lower percentage than the original 98.96% reflects additional defensive
orchestration/stream-retirement paths. Coverage exclusions were not changed.
Remaining uncovered export paths are the same inspection, encoding, cleanup and
pre-temporary-file failure cases discussed in the initial review. New uncovered
paths include resuming directly at diagnostics, a diagnostic-stream failure,
pre-session output-error fallback, and a stream that cannot be retired or is not
a native TextIOWrapper. Optional coverage additions were left out.

The before/after hash manifest verifies unchanged export implementation, optional
export tests, dependencies and quality/coverage configuration. Original and
intermediate evidence are retained rather than replaced with the final results.

## Remaining limits and review state

Physical Ctrl+C is unverified. The symbolic-link case still skips on WinError 1314;
actual hard-link and resolved-name cases pass. Python 3.10 has static/grammar
checks but no runtime run. A completely unusable stderr cannot deliver diagnostics,
and failure to retire a native descriptor remains a best-effort fallback.

Repeated interruptions or forced termination can prevent progress or lose updates.
Interrupted writes can leave temporary files or an uncertain old/new destination.
Atomic replacement does not merge concurrent sessions; path checks are preflight,
not filesystem locks. Those limits are retained.

The full classroom rubric is pending. Stage 8 report work remains deferred, with
the 1,000–1,500-word limit and conflicting-template-footer note retained.
**Stop for user review; no Stage 8 work, commit, push or submission.**

