# Stage 7 review: findings before changes

Date: 2026-11-18. Stage 6 export refinements accepted by the user based on reported tests.
Physical keyboard Ctrl+C remains **unverified**. This review changes documentation
and evidence only; application, tests, README, dependencies, and quality/coverage
configuration are unchanged.

## Confirmed defects

### F1 — An interrupt between protected finalization operations skips persistence (P2)

Location: `utils/cli.py:124`, with fallback at `utils/cli.py:204`.

**Reproduction:** Use a three-card deck A/Alpha, B/Beta, C/Gamma, with A's existing
error-balance score 2. Submit `wrong`, then EOF. At the first
`HistoryStore.can_save` access, inject one `KeyboardInterrupt`; subsequent access
would return normally. Run the real `main.py` guard through the recorded runpy
bootstrap, using distinct writable temporary history/export files.

**Observed:** exit 130, A's score remains 2 instead of 3, and export does not exist.
The summary already printed, but the warning says interruption occurred “before
quiz finalization.” An identical control without the injected interrupt saves
score 3 and writes the partial export.

**Cause/consequence:** The property check is outside the phase's interrupt handler.
The outer handler exits without resuming finalization. An orderly interrupt at
this boundary loses a completed answer's learning update and skips the independent
requested export despite working destinations. The exception is deliberately
injected at a deterministic boundary; this is not evidence of a physical Ctrl+C
test or a claim that it happens on every interruption.

**Proposed correction, not implemented:** Keep finalization progress and interrupt
status in a coordinator that also covers the transitions between phases. Continue
unattempted persistence/export work after a single interruption. Do not blindly
restart the entire finalizer: a completed history commit must never be counted
twice, and an interrupted commit can have an uncertain outcome.

**Proposed regression:** Parameterize one-shot interrupts at the permission guard
and between finalization phases. Assert status 130, score 3 exactly once, an export
with one completed answer and interrupted finish reason, and no replay of already
committed work. Keep the normal EOF control.

### F2 — A summary-output failure bypasses saving/export and can lose status 130 (P2)

Locations: `utils/cli.py:119` and `utils/terminal.py:125`.

**Reproduction:** Use the same deck, starting score, answer, and paths. At summary
display, route the original summary printer to an OS pipe whose read end is closed.
The diagnostic wrapper restores stdout afterward; the exception comes from the
real printer/OS rather than a replacement that merely raises an exception.
Run once following EOF and once after injecting `KeyboardInterrupt` at the second
input prompt.

**Observed:** On this Windows runtime the summary print raises
`OSError: [Errno 22] Invalid argument`. Both runs produce a traceback, leave A's
score at 2, and create no export. The already interrupted run exits **1 instead of
130**. The noninterrupted EOF control saves score 3 and exports successfully.

**Cause/consequence:** Summary display catches only `KeyboardInterrupt`.
An expected terminal write failure escapes before either persistence operation;
it also overrides an interruption already recognized during input. Display is
therefore able to prevent completed-answer persistence and independent export.

**Proposed correction, not implemented:** Translate expected terminal output errors
at a narrow terminal I/O boundary and arrange saving/export independently of display
success. Report failure through a usable diagnostic stream and retain interruption
precedence. Leave unexpected programming errors visible.

**Proposed regression:** Parameterize EOF and prior input interruption, then fail
summary output through a closed pipe or deterministic output `OSError`.
Require status 1/130 respectively, no traceback for this expected failure, score
3, and a partial export containing only the completed answer. Verify both writes
are attempted even if printing is unavailable.

## Actual diagnostic outputs

The exact bootstraps, argv, input, stdout, stderr, and resulting file observations
are in [stage_7_reproductions.json](verification/stage_7_reproductions.json).
All inputs were synthetic and histories/exports isolated in temporary directories.

| Scenario | Exit | Stored A score | Export exists | Traceback |
| --- | ---: | ---: | --- | --- |
| Control: wrong answer then EOF | 1 | 3 | Yes | No |
| One interrupt at history permission guard | 130 | 2 | No | No |
| Closed summary pipe after EOF | 1 | 2 | No | Yes |
| Closed summary pipe after input interruption | 1 | 2 | No | Yes |

To repeat an individual diagnostic, recreate the deck above, initialize history
as `{"version":1,"policy":"error-balance-v1","scores":{A_CARD_ID:2}}` using A's
`Flashcard.card_id`, and pass the recorded bootstrap to Python's `-c` option,
followed by `-f DECK --history HISTORY --export NEW_EXPORT`. Supply `wrong\n` on
stdin. Omit the bootstrap and invoke `main.py` directly for the control. Recorded
absolute temporary paths are historical observations, not persistent fixtures.

## Review against agreed behavior

| Area | Review/evidence |
| --- | --- |
| Loading/model boundaries | Both sample formats; malformed/oversized JSON, missing/unreadable input, strict fields, blank/empty decks and positioned duplicate pairs tested. Loader errors do not print or exit. |
| Normalization/identity | Trim/casefold only; internal spaces/punctuation retained. JSON-pair serialization distinguishes concatenation ambiguities. Equal fronts/different backs valid; identical content shares history across decks. |
| Engine/strategies | Typed Strategy protocol, no terminal/storage dependency, finite fixed session order, immutable source/summaries, non-consuming reads and post-completion rejection tested. Random assertions allow an unchanged shuffle. |
| Adaptive/history | Stable descending error balance, +1/-1 with zero floor, all modes update completed answers. Two-session temporary-file reuse, shared identity, bad/missing history, atomic failure preservation and retry without recounting tested. |
| CLI/feedback/statistics | Actual entry-point help/modes/seed/argument and file errors tested. Expected answers after misses; answered-only partial summaries and zero-answer N/A/null tested. |
| Export content/overwrite | Metadata/statistics/missed cards only, no submitted answers. Default existing-byte preservation and explicit atomic replacement pass. A destination created after the initial absence check is protected by exclusive publication. |
| Independent expected failures | Tests verify export after structured history-save failure; export failure/refusal leaves history updates intact. Corrupt history stays unchanged and warns explicitly. These pass; F1/F2 expose separate finalization paths. |
| Path conflicts | All role pairs, resolved relative paths, absent output names, hard links and overwrite flag combinations reject conflicts before quiz. Inspection failure is operational error, not silently ignored. Canonical destinations are used afterward. |
| Interruption/status | Input EOF/Ctrl+C, interrupts inside selected finalization calls, and combined history/export errors are tested. Status 130 holds in those tests, but F1/F2 show remaining gaps. Physical Ctrl+C is unverified. |

Path checks are preflight checks, not protection against arbitrary later filesystem
changes. Atomic replacement still does not merge concurrent learning sessions.
Forced process termination can lose session updates. These are the accepted limits,
not newly classified defects. Unsupported exclusive export publication fails safely
rather than replacing an existing file.

## Optional improvements, separate from defects

Add focused export error-boundary cases listed below if their diagnostic behavior
needs stronger evidence. They are additional fault coverage, not evidence of another
confirmed defect. No refactor, new export data, new runtime dependency, or changed
coverage exclusion is proposed as a prerequisite to addressing F1/F2.

## Checks and remaining gaps

Actual rerun: **261 passed, 1 skipped in 17.20 seconds**, on Windows CPython 3.13.17.
Combined statement/branch coverage: **98.96%**, 562 statements, 112 branches, six missing statements
and one partial branch. Black, isort, flake8, and strict mypy all exit 0.
Python 3.10 grammar parsing passes for all 23 Python files; mypy targets 3.10.
These are compatibility checks, not Python 3.10 runtime testing.

All uncovered statement lines are in `utils/results_export.py`:

| Lines/branch | Behavior not exercised by the suite |
| --- | --- |
| 59–60 | Destination `lstat` fails with an OS error other than absence; translate to structured export inspection error. |
| 91–92 | JSON encoding raises ValueError; translate to structured encoding error. Valid current model/session values do not naturally exercise this defensive branch. |
| 124–125 | Temporary-file cleanup itself fails after an export write/publication failure; append cleanup details. |
| 121 → 126 | Failure occurs before a temporary path exists, so cleanup is skipped (for example, parent creation or temporary-file opening fails). |

Coverage exclusions are unchanged. CLI/terminal line coverage of 100% does not prove
all exception timings or combined failures: F1/F2 are missing scenarios on lines
already exercised by passing tests.

The single skipped entry-point case creates a symbolic-link alias to the deck.
Windows returned **WinError 1314**, “A required privilege is not held by the client,”
so no symlink was created. Real hard-link aliases and canonical path conflicts
passed. A symlink-capable environment must run the skipped case; neither hard-link
success nor a simulated resolve failure verifies actual symlink traversal.

Remaining verification: physical Ctrl+C, Python 3.10 runtime, the unavailable
symlink case, and review against the full classroom rubric once supplied.
The report remains Stage 8 work with the classroom's 1,000–1,500-word limit and
the conflicting template-footer note retained.

Only review/log/evidence artifacts were written. The 29-file before/after SHA-256
manifest confirms unchanged application, tests, README and configuration.
**Initial review outcome:** Stopped for user review with neither defect fixed.
The user subsequently approved fixes for F1/F2. See
[the fix review](stage_7_fix_review.md) for regression failures captured before
implementation, the resulting changes, final checks, and remaining limitations.
Stage 7 fixes await review; Stage 8 has not started.

