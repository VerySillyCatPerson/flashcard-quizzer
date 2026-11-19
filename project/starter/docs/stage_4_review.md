# Stage 4: strategies, session engine, grading, and statistics

Date: 2026-11-18. Historical Stage 4 delivery snapshot, accepted after the user's
three requested existing tests passed. Current adaptive/history work is in
[stage_5_review.md](stage_5_review.md).
Actual runtime: Windows CPython 3.13.17. Compatibility target remains Python 3.10.

## Stage 3 checks before implementation

The user's conditional acceptance was satisfied by 19 focused review tests.
The exact JSON identity arrays are `["ab","c"]` and `["a","bc"]`, with distinct
SHA-256 IDs. Tests preserve field boundaries, punctuation, and internal spaces,
while allowing outer-whitespace and case variants. The large-integer regression
was already fixed at the JSON decoder boundary; unexpected card-validation
exceptions propagate. No production defect was found by these review checks.
The actual evidence is `verification/stage_3_review_checks.json`; explanations
and acceptance are grouped in the existing Stage 3 AI log entry.

## Files and responsibilities

| File | Stage 4 change |
| --- | --- |
| `utils/models.py` | Added frozen `AnswerResult` and `SessionSummary` with completed-answer statistics |
| `utils/strategies.py` | Structural `QuizStrategy` contract; sequential and injectable random permutations |
| `utils/engine.py` | Pure evaluation and finite `QuizSession` state, without terminal input/output |
| `tests/conftest.py` | Fresh three-card fixture shared by strategy/engine tests |
| `tests/test_strategies.py` | 15 tests for order, membership, copy ownership, seeds, unchanged shuffle, global RNG isolation |
| `tests/test_engine.py` | 28 tests for matching, state, summaries, extensions, errors, finite random sessions, and no terminal I/O |
| `tests/test_models.py`, `tests/test_data_loader.py` | Focused Stage 3 review additions for punctuation, spaces, and exception isolation |
| `docs/verification/stage_4_checks.json` | Actual final check commands, exits, and output |
| `docs/verification/stage_4_coverage.json` | Actual production coverage snapshot |
| `docs/verification/stage_4_demo.json` | Scripted three-card demonstration, explicitly not user answers |

Updated current README/environment links, the design plan's earlier injected-I/O
sketch, historical Stage 3 review, and AI log. No dependencies/configuration,
loader implementation, entry point, samples, or official report template changed.

## Strategy interface and ownership

```python
class QuizStrategy(Protocol):
    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]: ...
```

This resembles a structural TypeScript interface: a class with the right method
can be passed to the engine without inheriting a base class. `Sequence` gives
read-only access in the contract. `SequentialStrategy` returns `list(cards)`;
`RandomStrategy` shuffles that independent list using a privately owned or
injected `random.Random`. `RandomStrategy(Random(23))` makes tests reproducible
without changing global RNG state. The same-runtime reproducibility test does
not promise identical shuffle results across all future Python versions.

The engine snapshots input as a tuple, calls `strategy.order` once, checks that
the result has the same card multiplicities, and freezes that result as a tuple.
Invalid strategies cannot drop, duplicate, or inject questions silently. Future
adaptive selection can provide this method without changing the engine. A test
passes a new reverse-order strategy without inheritance or production code edits.

A valid shuffle may keep the original order. Tests check length and multiset
membership, independent ownership, and unchanged source data, never requiring
different order. A controlled no-op shuffle is explicitly accepted. Random
session tests submit exactly once per source card and verify termination, unique
membership for the validated deck, and unchanged caller ordering.

## Engine API and data flow

```python
session = QuizSession(cards, SequentialStrategy())
card = session.current_card
result = session.submit_answer("completed answer")
summary = session.summary
```

`current_card` is a non-consuming property; reading it twice does not advance.
`submit_answer` invokes the pure `evaluate_answer`, records the returned immutable
result, then advances to the next pending card. After completion, `current_card`
is `None`, and additional submission raises `RuntimeError` without changing
results. An empty programmatic deck is rejected because the loader contract
requires at least one card. Validated deck data remains the input precondition.

The engine imports no terminal functions and accepts no input/output callbacks.
It never prints, prompts, catches EOF/Ctrl+C, writes history, or chooses exit
statuses. The future terminal adapter reads input and displays `result.correct`
and `result.card.back`. On EOF/Ctrl+C it can use `session.summary` without ever
submitting the unfinished input. Tests forbid `input` and capture empty stdout/
stderr. Unexpected grading errors propagate, leaving the pending card unconsumed.

`AnswerResult` contains the card, original answer text, and correctness. Comparison
uses the shared `strip().casefold()` function. Empty answers are completed wrong
answers; punctuation, internal spaces, and each repeated-front card's own back
remain significant. Raw answer text is retained separately from comparison.

`SessionSummary` captures a tuple of completed results and deck size. Properties
derive answered/correct counts, unrounded percentage, missed cards, and completion.
With no submissions, accuracy is `None` for the later adapter's `N/A` display.
With one correct of two answered in a three-card deck, accuracy is 50%, not a
percentage of deck size. Missed cards retain their own backs and appear in session
order. Older summary snapshots do not change when a session advances.

In TypeScript terms, the engine is an explicit stateful domain object rather
than an async readline loop. Frozen result records and tuple snapshots resemble
readonly result collections; the externally managed input lifecycle determines
when a completed answer is submitted. Statistics sum booleans as 1/0 for counts.

## Actual three-card demonstration

The scripted caller (outside engine code) submitted the following answers:

| Card | Submitted answer | Result |
| --- | --- | --- |
| API | ` application programming interface ` | Correct |
| CPU | `incorrect` | Incorrect; expected `Central Processing Unit` |
| RAM | `RANDOM ACCESS MEMORY` | Correct |

Summary: deck size 3, answered 3, correct 2, **66.67%** when formatted for display,
missed term **CPU**, complete true. The stored percentage is unrounded; the
demonstration caller formats it, not the engine. This does not implement a CLI
or claim the user supplied these answers.

## Actual verification and limitations

Executed from `project/starter` with the explicit `.venv/Scripts/python.exe`:

| Check | Observed result |
| --- | --- |
| `python -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 0; **131 passed** |
| Coverage of all current production files, including `main.py` | **100%**, 166 statements and 34 branches, none missed |
| `python -m black --check .` | Exit 0; 12 files unchanged |
| `python -m isort --check-only .` | Exit 0; no warnings |
| `python -m flake8 .` | Exit 0; no lint output |
| `python -m mypy .` | Exit 0; strict 3.10-target checks passed on 12 files |
| Python 3.10 grammar parse of all 12 source/test files | Accepted on the 3.13.17 interpreter |

Source, fixture, and tests use Python 3.10-compatible syntax and existing stdlib
APIs (`Protocol`, `Sequence`, dataclasses, `Random`, `Counter`). No new dependency
or quality exception was added. **Python 3.10 was not runtime-tested**; mypy and
grammar checks are compatibility evidence only. The first full Stage 4 run passed;
Black reformatted the new engine/test layout before checks, and no assertions
were weakened or tests skipped to obtain the results.

Current coverage is a stage checkpoint. The empty `main.py` remains included;
the finished CLI, history, and all later production modules must be measured in
the final audit. The zero-statement Stage 2 baseline is not submission evidence.

Review the structural strategy contract, immutable session ordering, raw versus
normalized answers, partial-summary denominator, and independent result snapshots.
Adaptive ordering/history remains Stage 5; terminal rendering, flags, path-alias
preflight, exit handling, and export remain Stage 6. Stop here for Stage 4 review.

## Actual Stage 4 review and acceptance

The user requested three existing tests and authorized acceptance/Stage 5 if
they pass without new implementation. Ran exactly these tests on CPython 3.13.17:

- `test_unanswered_session_has_no_accuracy_or_misses`: reads `current_card` twice,
  checks the same first card is pending, answered/correct counts remain zero,
  accuracy is `None`, answers/misses are empty, and the session is incomplete.
- `test_answer_after_completion_does_not_change_results`: saves a completed
  summary, asserts another submission raises `RuntimeError`, and checks the
  current summary equals the saved one.
- `test_partial_statistics_and_snapshot_are_stable`: retains the first snapshot,
  submits another answer, and checks the first still has one correct/100%/no
  misses while the new snapshot has two answers/one correct/50%/one miss.

All **3 passed**, with empty stderr; command/output are saved in
`verification/stage_4_review_checks.json`. No engine/test implementation changed.
The user's stated condition is met and Stage 4 acceptance is recorded in its
existing AI log entry. Stage 5 acceptance remains a separate pending review.
