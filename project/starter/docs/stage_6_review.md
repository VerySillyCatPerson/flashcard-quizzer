# Stage 6: CLI, terminal UI, persistence, and result export

Date: 2026-11-18. Stage 5 accepted after four existing save-retry cases passed.
Stage 6 implementation/verification complete; user review pending.
Runtime: Windows CPython 3.13.17; minimum/static compatibility target: Python 3.10.

## Files and data flow

| File | Responsibility/change |
| --- | --- |
| `main.py` | Import CLI and propagate status under the main guard |
| `utils/cli.py` | Flags, strategy selection, path preflight, interaction, independent finalization |
| `utils/terminal.py` | UTF-8 streams, prompts, feedback, warnings, single-line display, summary table |
| `utils/paths.py` | Resolved names and existing-file identity checks; canonical I/O destinations |
| `utils/results_export.py` | Versioned session JSON and atomic result replacement; no history or terminal dependency |
| `utils/models.py` | Added typed finish-reason alias; grading/results behavior unchanged |
| `tests/cli_helpers.py` | Isolated subprocesses and test-only runpy fault bootstrap |
| `tests/test_cli.py` | 52 entry-point cases, including one unavailable-symbolic-link skip |
| `tests/test_paths.py`, `test_results_export.py`, `test_terminal.py` | Path edge cases, export preservation/schema, presentation |
| `docs/manual_stage_6.ps1` | Temp-file PowerShell checks and optional physical Ctrl+C |

README documents the working CLI. The historical Stage 5 entry records its actual
acceptance. Engine, loader, history implementation, sample decks, dependencies,
configuration, and report template remain unchanged by Stage 6. Tests/demos used
isolated temporary homes and learning/export files, not a real user profile.

Flow: argparse -> path preflight -> validated deck -> history -> strategy ->
engine plus external terminal input/feedback -> summary -> independent history
commit/export -> status. Engine/history still have no terminal or exit handling.
The thin main file has three executable statements and both guard branches covered.

## CLI and summaries

`-f/--file` is required except for help. `-m/--mode` accepts sequential/random/
adaptive, default sequential. `--history PATH` overrides the user-state default;
default-home lookup occurs after parsing, so help does not inspect a profile.
`--seed INTEGER` requires random mode. `--export PATH` opts into JSON results.
`--overwrite` requires `--export` and explicitly authorizes replacing its existing
file. Without it, export refusal is an operational error (1) after quiz/history
finalization, preserving the old bytes. Existing history still updates normally;
the flag neither changes history behavior nor bypasses role-conflict checks.

Streams use UTF-8. Display escapes line controls without changing raw comparison
data. Each question is followed immediately by Correct or Incorrect with its
expected answer. The table contains deck size, completed-question/correct counts,
accuracy, and missed fronts with original one-based positions. EOF/Ctrl+C exclude
unfinished answers; zero completed answers means N/A and no misses. Full question
completion can coexist with an operational failure; it is not an exit-status flag.

The CLI is the composition root, analogous to TS code wiring typed domain APIs
and an input adapter. Parser-converted values are captured in an options record.
Expected errors are handled at operation boundaries; unexpected programming
errors are not turned into wrong answers or generic invalid-input messages.

## Paths, warnings, and exit policy

All three role pairs are checked before loading/asking/writing. Resolved,
platform-normalized names catch relative components, symlinks, and the same absent
destination. `Path.samefile` additionally detects existing hard links. Canonical
destinations are used for I/O. Known unsupported identity operations fall back
to resolved names; unexpected permission/inspection errors abort with status 1.
Conflicts name both roles/paths and exit 2 before a quiz/write. This is not a lock
against concurrent changes after inspection.

Corrupt/unreadable/unsupported history prints cause/path and every agreed effect:

```text
Previous scores could not be loaded. Adaptive mode will use deck order.
Learning updates will not be saved during this run.
```

Practice/export continue while the problematic history is preserved. Missing
history is a fresh profile. The table survives history/export failure. Both
persistence operations are attempted independently; diagnostics are deferred
until both attempts finish. Warnings/errors use stderr; quiz/table use stdout.

| Exit | Meaning |
| --- | --- |
| 0 | Help or completed quiz with successful persistence/requested export; wrong answers alone do not fail |
| 1 | Deck/path/input/history/export operational failure, degraded history, or premature EOF |
| 2 | Argument errors, seed outside random mode, or conflicting roles |
| 130 | KeyboardInterrupt/Ctrl+C, overriding secondary failures |

Interruptions during finalization also retain 130 and permit the next independent
operation where possible. Completed answers commit once at session end/orderly
interruption. Forced termination can lose updates; atomic replacement does not
merge concurrent sessions. Existing persistence limits remain in force.

## Result schema

Version 1 includes mode, seed/null, finish reason (`completed`, `eof`, `interrupted`,
`input_error`), question-completion flag, deck/answered/correct counts, unrounded
percentage/null, and structured misses. Missed cards include ID, original position,
front, and expected answer. Submitted answer text, per-answer records, and local
file paths are excluded. The original unaccepted audit-oriented raw-answer
addition had no agreed requirement and was removed following actual user review.
Completion describes answered questions independently of operational status.

Serialization precedes writes. Existing exports are refused by default before
staging. The complete sibling temp file is flushed/synced/closed; without the
flag it is published exclusively using a hard link, then the staging name is
removed. This also refuses a competing file created after the absence check.
Unsupported exclusive publication fails rather than silently overwriting.
With `--overwrite`, publication uses atomic replacement. Expected failure
preserves an existing export; cleanup errors do not mask the original failure.
Tests verify omitted submitted text, misses/statistics, refusal byte preservation,
authorized replacement/failures, race protection, and independent history updates.

## Actual outputs

`verification/stage_6_commands.json` preserves the 13 initial-delivery transcripts
before the export-policy refinement. Current policy examples are in
`stage_6_export_review_commands.json`. All inputs are scripted. Initial native
sequential output (whose presentation remains unchanged) included:

```text
Answer: Correct
Answer: Incorrect. Expected: Beta
Answer: Correct

Completed session (completed)
+-----------------+--------+
| Deck size       | 3      |
| Total questions | 3      |
| Correct         | 2      |
| Accuracy        | 66.67% |
| Missed terms    | #2 B   |
+-----------------+--------+
exit 0
```

Adaptive reuse then asked B/A/C and finished at 100%, exit 0. Seed 7 random order
was C/A/B on this runtime; tests require reproducibility/membership, not changed
order. EOF after alpha returned a partial 1/3 table, 100% over one answer, no
misses, exit 1. A deck/export conflict returned usage plus role/path error, exit 2.
Corrupt history warned, preserved bytes, completed practice/export, and exited 1.
Native export-to-directory failure retained the table/saved history, exit 1.

An entry-point runpy subprocess with an injected history-save error still wrote
the complete export, exit 1. With KeyboardInterrupt after one answer plus history
save failure and native export failure, the result remained **130** with a partial
table. The exact required glossary command also completed all 10 scripted answers,
exit 0, using an isolated temporary default home. No production fault flags exist.

## Actual verification and manual script

| Final command/check | Result |
| --- | --- |
| `python -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 0; **261 passed, 1 skipped** |
| All-production coverage, including main | **98.96%**; 562 statements, 112 branches |
| Black/isort/flake8 | Exit 0; 23 files formatted, no warnings/lint errors |
| Strict mypy | Exit 0; no issues in 23 files; target 3.10 |
| Python 3.10 grammar parse | All 23 files accepted on the 3.13.17 interpreter |

Current export-review checks/manual output are in `stage_6_export_review_checks.json`;
coverage is in `stage_6_export_review_coverage.json`. Export inspection/encoding/
cleanup edge paths remain uncovered. Initial-delivery `stage_6_checks.json`,
`stage_6_coverage.json`, and command transcripts remain historical evidence from
before these refinements; they do not define the current export contract.
Initial pytest also passed 252/1 skipped, while five long source lines and one
unused test import failed lint. Wrapped source text/test bootstrap lines and
removed the import, retaining assertions/rules; initial evidence is preserved.

The symbolic-link creation test skipped on WinError 1314 (account lacks required
privilege). Actual deck/history and history/export hard-link tests passed.
Existing-symlink behavior was not runtime-tested here. Other path resolution and
unsupported/error fallback cases are tested.

Ordinary entry-point tests invoke main.py directly. Deterministic fault cases use
a test-only runpy bootstrap executing its actual guard/CLI. Ctrl+C tests inject
Python's KeyboardInterrupt at input/finalization boundaries. **Physical keyboard
or console-signal delivery was not automated.**

The manual script creates a fresh temporary deck/history/export directory,
prints expected results, retains artifacts, and ends with optional physical
Ctrl+C. It now demonstrates default export refusal with a byte-hash comparison
and successful explicit replacement using a separate history file. Its
noninteractive portion ran successfully. Direct script execution was
blocked by local policy; verification used a child process with a process-only
override, changing no machine/user policy:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\manual_stage_6.ps1
```

Add `-SkipInteractive` for the automated portion. For physical Ctrl+C, enter alpha,
then interrupt at the next prompt; expect partial results, completed-answer
save/export, and application status 130. If the host also stops the script,
inspect `$LASTEXITCODE` after returning to its prompt.

## Actual export review and requested refinements

The user explicitly withheld Stage 6 acceptance and rejected raw-answer export
without an agreed requirement. The initial audit-convenience rationale did not
satisfy that requirement; no raw-answer export option was retained. Schema tests
assert exactly metadata/statistics/misses and absence of synthetic submitted text.

The user required default no-overwrite plus explicit `--overwrite`, keeping
history updates separate. Tests confirm refusal leaves existing bytes unchanged,
including a destination created after the initial check. Authorized replacement
remains atomic, and expected write failure preserves previous bytes. Actual CLI
tests run consecutive sessions: history scores move 1 to 2 despite export refusal,
then to 1 after correct answers with authorized export replacement. Conflict
tests run with and without the flag. Physical Ctrl+C remains **unverified** until
the user performs the manual check; automated tests still inject KeyboardInterrupt.

Current command evidence demonstrates initial creation (0), refusal with preserved
bytes (1), and authorized replacement (0), with no submitted-answer fields. A long
help line found by flake8 was shortened; quality checks passed without suppression.
The same Stage 6 log entry records the actual review and this response. Stage 6
acceptance and personal reflections remain pending; stop here for review.

Only CPython 3.13.17 was executed. Syntax/APIs retain the 3.10 target; static
checking is not runtime testing. No dependency or quality exception was added.
The Stage 2 zero-statement result is not submission evidence. Review/report/
rubric/clean-setup work remains in Stages 7-9. Stop for Stage 6 review.
