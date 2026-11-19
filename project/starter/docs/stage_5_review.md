# Stage 5: adaptive ordering and separate history persistence

Date: 2026-11-18. Stage 4 accepted after its three requested tests passed.
Historical Stage 5 snapshot, accepted after its four requested retry cases passed.
Current CLI integration is described in [stage_6_review.md](stage_6_review.md).
Runtime tested: Windows CPython 3.13.17. Compatibility target remains Python 3.10.

## Files and ownership

| File | Stage 5 responsibility |
| --- | --- |
| `utils/strategies.py` | Added `AdaptiveStrategy`: stable ordering from a copied score snapshot; no persistence or terminal calls |
| `utils/history.py` | Pure score updates, strict versioned history validation, per-run load state, atomic session-end save, structured errors |
| `tests/test_history.py` | 58 tests for policy, real round trips, every mode, identity, partial/zero-answer runs, invalid history, and save failures |
| `tests/test_strategies.py` | Five adaptive tests added to the existing permutation tests |
| `docs/verification/stage_4_review_checks.json` | Actual three-test evidence satisfying conditional Stage 4 acceptance |
| `docs/verification/stage_5_initial_checks.json` | Preserved initial test-fixture/style/type failures |
| `docs/verification/stage_5_checks.json` | Final successful commands, statuses, and output |
| `docs/verification/stage_5_coverage.json` | Actual all-production coverage snapshot |
| `docs/verification/stage_5_demo.json` | Scripted real temporary-file sessions and preservation demonstrations |

README/environment links point to this current review; the previous stage's
review and existing log entry record its actual acceptance. No engine/model/loader
implementation, dependencies, configuration, entry point, samples, or report
template changed. No real user learning profile was written.

## History schema

History is separate from a deck and stores only these top-level fields:

| Field | Contract |
| --- | --- |
| `version` | Integer `1`, with booleans explicitly rejected |
| `policy` | String `error-balance-v1` |
| `scores` | Object mapping full `card-v1:<64 lowercase hex digits>` identities to nonnegative integers |

The actual persisted documents are included in the demo artifact. The schema
stores no deck path, prompt, expected answer, submitted answer, or timestamp.
Zero scores are valid and retained. Dormant identities remain when cards disappear
from a deck; restoring identical content resumes their score. Meaningful front/
back edits create a new identity starting at zero. Identical normalized content
in other decks shares the same score, including across the two supported formats.

Missing fields, additional top-level fields, unsupported version/policy, malformed
identity keys, negative/float/string/null/container scores, and boolean scores
invalidate the whole history. A valid first entry cannot cause partial loading
when a later entry is invalid. Duplicate JSON keys, nonstandard constants, bad
encoding, malformed JSON, excessive nesting, and integer decode limits are
expected load failures. Future format changes require an explicit version/policy
decision; no migration or guessed interpretation is performed.

## Policy and separation of concerns

`updated_scores(scores, completed_answers)` is a pure copy/update function:
incorrect adds one; correct subtracts one with a floor of zero. It preserves
unrelated entries and changes only supplied completed answers. Every strategy
uses the same history update path; mode selection affects order only. Tests run
sequential, random, and adaptive sessions through real history files.

`AdaptiveStrategy` copies the supplied validated score map and returns a stable
sort by descending score. Missing cards score zero. Ties preserve input deck
order, regardless of dictionary insertion order. It neither repeats cards nor
imports storage. `QuizSession` already calls a strategy once and snapshots the
result; changing external scores or answering correctly cannot reorder pending
questions during that run. Every card is still asked once.

Typical future terminal orchestration, not an implemented CLI:

```python
history = HistoryStore(history_path)
session = QuizSession(cards, AdaptiveStrategy(history.scores))
# Obtain and submit completed answers externally.
# On normal finish or orderly interruption, inspect history.load_error first.
history.save_session(session.summary)
```

The store loads once for one quiz run. `scores` returns a read-only snapshot;
`load_error` exposes a structured `HistoryLoadError`; `can_save` reports usable,
not-yet-finalized state. A successful `save_session` finalizes this run, preventing
accidental double-counting from submitting the same summary again. Open a new
store for another session. Failed saves leave the original scores and writable
state intact so a retry applies the answers once. A zero-answer finalization
writes no file or directory. Partial summaries save only completed answers.

Python `Mapping[str, int]` resembles TS `ReadonlyMap<string, number>` at the
selection boundary, while runtime JSON validation additionally rejects booleans
and fractional values. The mapping proxy prevents assignment; copying also
prevents later store changes from altering previously returned snapshots.

## Missing/corrupt history and failures

An absent history file is a fresh profile with zero scores and saving enabled.
Loading creates no file or parent directory. `default_history_path()` computes
`Path.home() / ".flashcard_quizzer" / "history.json"` without touching it; every
test/demo uses explicit temporary paths instead of the real user profile.

Corrupt, unreadable, or unsupported history yields empty scores, a load error,
and disabled saving for that run. Adaptive selection then uses deck order.
Calling `save_session` on the degraded store raises `HistorySaveError` before
any write, preserving the problematic bytes. Neither persistence nor selection
prints. The Stage 6 terminal layer must show the accepted warning plus cause/path:

```text
Previous scores could not be loaded. Adaptive mode will use deck order.
Learning updates will not be saved during this run.
```

The agreed operational exit statuses are also Stage 6 presentation policy;
Stage 5 supplies structured information rather than printing/exiting itself.
Unexpected validation programming errors propagate instead of being mislabeled
as corrupt input. Decoder-only and explicit schema errors are translated at
their narrow operation boundaries, matching the reviewed loader design.

Saving serializes a whole document first, writes a uniquely named sibling
temporary file, flushes and syncs its data, closes it, then uses `os.replace`.
Closing before replacement is important for Windows. On expected I/O failure,
the previous valid file and in-memory scores remain unchanged; the temp is removed
when possible. If cleanup also fails, its failure is appended to the structured
save error without hiding the original failure. A temporary file may remain in
that cleanup-failure case, which is explicitly tested.

Saving occurs **only at session end or orderly interruption**. Forced process
termination can lose that session's in-memory updates. Atomic replacement
protects against partial destination writes; it **does not resolve concurrent
session conflicts** or merge their snapshots. No file-locking or power-loss
durability guarantee is introduced. Deck/history/export alias preflight remains
required before the quiz in Stage 6; this store alone is not that coordinator.

## Actual two-session round trip

Real temporary files were written and new `HistoryStore` instances reopened them
between sessions. Scripted answers are labeled as a demonstration, not user input.

| Step | API | CPU | RAM | Next adaptive order |
| --- | --- | --- | --- | --- |
| New profile | 0 | 0 | 0 | API, CPU, RAM |
| Session 1: API/CPU wrong, RAM correct | 1 | 1 | 0 | API, CPU, RAM |
| Session 2: API correct, CPU wrong, RAM correct | 0 | 2 | 0 | CPU, API, RAM |

API's correct answer removes its old priority. CPU now comes first; the zero-
score API/RAM tie retains deck order. The demonstration also wrote another deck
with reversed order, the other JSON shape, and casing variants: CPU retained its
same identity and score 2. Corrupt history bytes survived a refused commit.
A controlled replacement permission error preserved the previous valid history
byte-for-byte, kept in-memory scores unchanged, and removed its temporary file.

## Actual checks and refinements

All final commands used `.venv/Scripts/python.exe` from `project/starter`:

| Check | Observed result |
| --- | --- |
| `python -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 0; **194 passed** |
| All-production coverage, including `main.py` | **100%**, 297 statements and 64 branches, none missed |
| `python -m black --check .` | Exit 0; 14 files unchanged |
| `python -m isort --check-only .` | Exit 0; no warnings |
| `python -m flake8 .` | Exit 0; no lint output |
| `python -m mypy .` | Exit 0; strict 3.10-target check passed on 14 files |
| Python 3.10 grammar parse of all 14 source/test files | Passed on the 3.13.17 interpreter |

The initial full run had 193 passes and one failed test: a global `json.dumps`
mock also intercepted card identity serialization before reaching the intended
history serialization failure. Narrowed that test mock to the history document,
preserving card-key encoding and all old-file/state preservation assertions.
Also shortened two overlong docstrings and used string patch targets for imported
module internals to satisfy strict mypy. Those initial failures are preserved in
`stage_5_initial_checks.json`. No production fix, weakened assertions, new lint
exceptions, disabled checks, or skipped tests were used to obtain the final pass.

Expected save failures are injected at mkdir, temporary-file creation, fsync,
and replacement boundaries; the old/new files themselves are real temporary
files. Permission tests simulate OS denial deterministically on elevated Windows.
Real successful round trips exercise native Windows writing/closing/replacement.
This verifies controlled failure handling, not an actual full-disk/power-loss event.

Only **CPython 3.13.17** was executed. `MappingProxyType`, `NamedTemporaryFile`
with `delete=False`, `os.replace`, `fsync`, `Path.unlink(missing_ok=True)`, and the
typing syntax/APIs are available for the 3.10 target; static checking is not 3.10
runtime testing. Current coverage is a stage checkpoint, and the Stage 2 zero-
statement baseline remains excluded as submission evidence.

Review the strict version/policy schema, one-store-per-run commit guard, score
decay and shared identity, degraded-load protection, and atomic-save limitations.
CLI orchestration, terminal text, path-alias validation, export, and actual exit
codes remain Stage 6 work. Stop here for Stage 5 review.

## Actual Stage 5 retry review and acceptance

The user requested proof that a failed save retry persists the candidate once,
plus an ownership explanation, and authorized acceptance/Stage 6 if it passes.
The existing test `test_failed_save_preserves_previous_valid_history_and_can_retry`
passed all four cases (mkdir/temp/fsync/replace). Initial score 2 remains 2 on
disk and in memory after failure; retrying the same summary reloads 3, not 4.
No production/test change was required. Evidence: `stage_5_review_checks.json`.

`updated_scores` owns pure arithmetic; `HistoryStore.save_session` coordinates
candidate creation and adopts it only after `_atomic_save` succeeds;
`_atomic_save` owns writing/replacement. A retry therefore starts from the same
unchanged base. The user's express condition is met and acceptance is recorded
in the existing Stage 5 log entry. No broader human review is inferred.
