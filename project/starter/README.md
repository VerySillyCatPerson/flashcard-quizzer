# Flashcard Quizzer

A Python CLI that validates JSON decks, quizzes in sequential/random/adaptive
order, and reports accuracy and missed terms. Persistent error-balance history,
seeded randomness, and optional versioned JSON result export are included.

Stages 7 and 8 are accepted based on reported evidence; final report wording is
approved. Post-fix runs on **Windows CPython 3.10.11 and
3.13.17** each passed **343 tests, 1 skipped**, with **98.21% combined coverage**
including `main.py`. Statement coverage is **98.51%** and branch coverage is
**96.77%**. Symlink creation is privilege-blocked; hard-link tests passed. Final
audit findings are in [the authoritative-rubric audit](docs/final_rubric_audit.md).
The rubric was supplied on 2026-11-19 and makes 1,000-1,500 words authoritative.
Approved test-bootstrap documentation/spacing and startup-interrupt corrections
are verified in [the fix review](docs/f3_fix_review.md). Physical Ctrl+C and actual symlink verification
remain open; their rubric relevance is distinguished
in that audit.

## Setup

Minimum supported version: **Python 3.10**. Clean-environment runtime checks passed
on Windows CPython **3.10.11 and 3.13.17**. Mypy/grammar checks also target 3.10;
those static checks are separate evidence. Other patches/platforms were not tested.
Runtime code uses the standard library; requirements contain development tools.

From `project/starter`, with a usable Python installation:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

Activate with `.\.venv\Scripts\Activate.ps1` for plain `python` commands, or use
`.\.venv\Scripts\python.exe` directly without changing script policy. If WindowsApps
aliases prevent Python running, see [docs/environment.md](docs/environment.md).
`requirements-lock.txt` records the actual Windows/3.13 transitive tool environment;
other platforms/versions should resolve dependencies from `requirements.txt`.

## Usage

```text
python main.py --help
python main.py --mode sequential --file data/glossary.json
python main.py -m adaptive -f data/python_basics.json
python main.py -m random -f data/glossary.json --seed 23 --history results/history.json --export results/session.json
```

`-f/--file` is required except for help. `-m/--mode` defaults to sequential.
`--seed` takes an integer and requires random mode. Each card is asked once;
a valid shuffle may retain original order.

`--history PATH` overrides `~/.flashcard_quizzer/history.json`. `--export PATH`
requests JSON results. Deck, history, and export must identify distinct files:
resolved names and existing-file aliases are checked before the quiz, and canonical
paths are used for I/O.

An existing export is refused by default, with exit 1 after the quiz; its bytes
remain unchanged and completed-answer history still updates normally. Pass
`--overwrite` with `--export` to authorize atomic replacement. The flag affects
only exports and cannot bypass deck/history/export conflict protection.

```text
python main.py -f data/glossary.json --export results/session.json --overwrite
```

Both sample formats work:

```json
[{"front": "API", "back": "Application Programming Interface"}]
```

```json
{"cards": [{"front": "Function keyword?", "back": "def"}]}
```

Cards need nonblank string fronts/backs. UTF-8 BOMs are accepted. Duplicate JSON
keys and identical normalized front/back pairs are rejected. Matching fronts with
different backs are valid; extra metadata is ignored. No context field is added.
Duplicate-pair errors identify both cards' 1-based positions.

Answers ignore case/outer whitespace; punctuation/internal spaces remain
significant. Blank answers count as incorrect. Feedback shows Correct/Incorrect
and the expected answer after a mistake. The table shows deck size, completed
questions, correct count, accuracy, and missed fronts with original positions.

Displayed card fronts and expected answers escape C0 controls (U+0000–U+001F),
DEL (U+007F), and C1 controls (U+0080–U+009F). Newline, carriage return and tab
keep the literal `\n`, `\r` and `\t` conventions; other controls use `\xhh`.
For example, ESC followed by `[2J` displays as `\x1b[2J`, and C1 CSI displays
as `\x9b`. Questions, incorrect-answer feedback and missed-card summaries use
this escaping. Ordinary Unicode stays readable. Grading, identity, history and
JSON export retain the original card values; escaping applies only to presentation.

## History, interruption, and export

History stores version `1`, policy `error-balance-v1`, and content-keyed integer
scores. Incorrect adds one; correct subtracts one with a zero floor. Higher scores
go first; ties retain deck order. Ordering stays fixed during a run. Every mode
updates history from completed answers, including orderly partial sessions.

Moving/renaming/reordering preserves unchanged card identity. Identical normalized
content across decks shares history. Meaningful front/back edits start fresh;
removed entries remain dormant. No deck registry exists.

Missing history starts fresh. Corrupt/unreadable/unsupported history is preserved,
warns explicitly, falls back to zero scores, and disables saving for that run.
Requested export is still attempted. Save/export failures retain the summary and
report on stderr; history saving and export are attempted independently.

Terminal output failure also allows saving and export to continue; diagnostics
use stderr when available. A quiz output failure uses export finish reason
`output_error`. Summary output failure retains the session's existing finish
reason (such as EOF or interruption) and still causes an operational failure.
Failed native output descriptors are redirected to the null device to prevent
Python's shutdown flush from replacing the intended exit status. Output on that
failed stream is discarded; descriptor retirement is best effort.

EOF/Ctrl+C show partial statistics, save completed-answer history, and export
partial statistics where possible.
Unfinished input is neither wrong nor recorded. With zero completed answers,
accuracy is table `N/A` / JSON `null`. Export contains version, mode, seed, finish
reason, completion flag, counts, unrounded accuracy, and missed cards with
IDs/positions/fronts/expected answers. Submitted answer text and per-answer records
are excluded. Completion describes questions answered independently of operational
exit status. Export includes no local file paths.

New exports publish a complete staged file without replacing an existing path,
including one that appears after the initial check. Unsupported exclusive
publication fails safely. Authorized replacement uses atomic `os.replace`.

Saving occurs at session end/orderly interruption. Forced termination may lose
that session's updates. Atomic sibling replacement prevents partial destination
writes, but does not merge concurrent sessions or lock paths against later changes.
An interruption between finalization phases continues pending work with status
130. Once a write is attempted, an interruption may leave its commit outcome
uncertain; that write is not automatically retried, and other pending work proceeds.

| Exit | Meaning |
| --- | --- |
| `0` | Help or completed quiz with successful persistence/export; wrong answers alone do not fail |
| `1` | Deck/path/input/output/history/export operational failure, degraded history, or premature EOF |
| `2` | Argument errors, including conflicting file roles |
| `130` | Ctrl+C priority over expected secondary failures, including startup warning-output failure; physical keyboard delivery remains unverified |

## Verification and manual checks

```powershell
.\.venv\Scripts\python.exe -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json
.\.venv\Scripts\python.exe -m black --check .
.\.venv\Scripts\python.exe -m isort --check-only .
.\.venv\Scripts\python.exe -m flake8 .
.\.venv\Scripts\python.exe -m mypy .
.\.venv\Scripts\python.exe -m pip check
```

Coverage includes all production modules and `main.py`, excludes only tests/local
tool and environment directories, and enforces an overall **81% combined** gate
(strictly above 80%). With branch measurement enabled, the tool's total combines
covered statements and branch outcomes; it is not the branch-only percentage or
an unweighted average of percentages.

| Post-independent-review coverage (both Windows runtimes) | Covered / total | Percent |
| --- | --- | --- |
| Statements | 595 / 604 | 98.51% |
| Branch outcomes | 120 / 124 | 96.77% |
| Combined tool total | 715 / 728 | 98.21% |

The historical zero-statement Stage 2 result is not submission evidence. Saved
current [3.10 checks](docs/verification/independent_review_green_310.json),
[3.13 checks](docs/verification/independent_review_green_313.json), and
[coverage](docs/verification/independent_review_coverage_313.json) measure the corrected source.
These use the existing isolated environments against the current working tree;
they are not a new clean-install reproduction. The [independent-review fixes](docs/independent_review_fixes.md)
separate the reported Linux/Python 3.12 nesting-test failure from actual Windows
results. Linux/Python 3.12 was not executed. These corrections and factual documentation updates were accepted on reported evidence.
Historical
[check outputs](docs/verification/stage_8_checks.json),
[coverage data](docs/verification/stage_8_coverage.json), and
[derived metrics](docs/verification/stage_8_metrics.json) record this run on
Windows CPython 3.13.17. Stage 9 separately reproduced clean setup and all documented
quality commands; [3.13 results](docs/verification/stage_9_checks_313.json) and
[3.10 results](docs/verification/stage_9_checks_310.json) preserve actual output.
These were new isolated venvs on this machine, not a fresh operating system;
standard pip caches could be reused. Initial sandbox network failures and allowed
network retries are recorded in [setup evidence](docs/verification/stage_9_setup.json).

[The PowerShell script](docs/manual_stage_6.ps1) uses a fresh temporary deck/history/
export directory and prints expected outcomes, then offers a physical Ctrl+C check.
Artifacts remain for inspection. Its noninteractive portion was executed successfully.
This machine blocks direct scripts; a process-scoped invocation is:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\docs\manual_stage_6.ps1
```

Add `-SkipInteractive` to omit keyboard input. This changes no machine/user policy.
Automated Ctrl+C tests inject KeyboardInterrupt in a subprocess executing the actual
entry point; physical keyboard/OS signal delivery was not automated.

See [Stage 8 verification and log audit](docs/stage_8_verification.md),
[the report draft](docs/final_report.md), [Stage 7 fix evidence](docs/stage_7_fix_review.md),
and [the interaction log](docs/ai_edit_log.md). Historical Stage 6 transcripts remain
available as evidence of the earlier CLI/export review. The supplied authoritative
rubric fixes the report limit at 1,000-1,500 words; the original template footer
is preserved as historical template text, not an unresolved length decision.
The [provided-checklist review](docs/checklist_review_2026-11-19.md) was performed
by Codex on 2026-11-19; it is not a retrospective claim of student line-by-line review.

Shortest physical Ctrl+C check, from this folder in interactive PowerShell:

```powershell
$quizTemp = Join-Path $env:TEMP ([guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe main.py -f data/glossary.json --history "$quizTemp\history.json" --export "$quizTemp\session.json"
$LASTEXITCODE
```

Press Enter once for a blank completed answer; press Ctrl+C at the next prompt,
then run the final line at the returned PowerShell prompt. Expected: status 130,
a partial summary with one incorrect answer, and history/session files under
`$quizTemp`. This physical check has **not** been performed.

## Known limits and outstanding verification

| Outstanding item | Current evidence / next step |
| --- | --- |
| Authoritative rubric | Supplied on 2026-11-19; [mandatory requirements and optional suggestions](docs/authoritative_audit_request.md) are now audited separately. |
| Physical Ctrl+C | Unverified; automated KeyboardInterrupt tests do not prove keyboard/OS signal delivery. Use the manual script when available. |
| Python 3.10 runtime | Verified on Windows CPython 3.10.11; this does not establish every patch/platform. |
| Actual symlink conflict | Test skipped after WinError 1314; run it in a symlink-capable environment. Hard-link success is separate evidence. |
| Clean-environment reproduction | Completed in Stage 9 with two new environments and identical submission copies; not an OS-level clean machine. |
| Report wording | Approved by the student; the name is masked as requested. |
| Root README placeholder links | Removed during the accepted Stage 9 follow-up; the root README links to these application instructions. |
| Credential ignore rules | Repository-wide `.env` and conventional private-key rules preserve explicitly named examples/templates, public keys, and certificates. No credential files were detected. |
| Required test-bootstrap quality | Resolved after approval: eight missing docstrings and eight spacing violations corrected; all 16 embedded functions documented and extracted-script flake8 passes on both runtimes. |
| Confirmed startup error handling | F3 resolved after test-first correction: expected warning-output failure retains 130; unexpected RuntimeError remains visible. These are injected-interruption/native-pipe tests, not physical Ctrl+C. |

[Cleanup verification](docs/verification/stage_9_cleanup_checks.json) records the
link and Git-ignore checks. Submission readiness remains unconfirmed pending the
student's physical Ctrl+C result. Final report wording and verified corrections
are accepted. The rubric is available; the blocked
symlink check remains explicitly unverified and is not itself a rubric failure.

Repeated interruptions or forced termination can prevent finalization. An
interrupted write can leave a temporary file or an uncertain committed result;
automatic replay is avoided. Concurrent sessions are not merged, and preflight
path checks do not lock files against later filesystem changes. If stderr is
unusable, warnings cannot be delivered. Uncovered defensive inspection/encoding/
cleanup and stream-retirement paths are documented in the Stage 8 review; coverage
does not establish every failure combination.

## Structure and license

`main.py` delegates to CLI. `utils/` separates models/loading, strategies, engine,
history, path checks, terminal UI, orchestration, and export. `tests/` contains unit
and entry-point tests; `data/` preserves samples; `docs/` holds reviews/evidence.

[License](../../LICENSE.txt)
