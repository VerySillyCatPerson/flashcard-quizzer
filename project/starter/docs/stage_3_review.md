# Stage 3: typed flashcards and validated JSON loading

Date: 2026-11-18. Historical Stage 3 delivery snapshot, accepted after the user's
requested focused checks. Follow-up results are recorded below; current engine
and statistics work is described in [stage_4_review.md](stage_4_review.md).
Runtime tested: Windows CPython 3.13.17. Minimum supported design target: 3.10.
No new dependencies, engine, strategies, history persistence, or CLI behavior.

## Files and data flow

| File | Responsibility |
| --- | --- |
| `utils/models.py` | Frozen `Flashcard(front, back)`, common normalization, versioned content identity |
| `utils/data_loader.py` | Read UTF-8, decode both JSON shapes, validate fields/duplicates, raise structured errors |
| `tests/test_models.py` | 9 tests for immutability, normalization, and identity behavior |
| `tests/test_data_loader.py` | 70 tests for file/JSON/schema failures, samples, metadata, ordering, identity, and no terminal output |
| `docs/verification/stage_3_checks.json` | Actual final commands, exit statuses, and captured output |
| `docs/verification/stage_3_coverage.json` | Actual current-stage coverage snapshot across all production files |
| `docs/verification/stage_3_regression_before.json` | Actual failing oversized-integer regression before correction |
| `docs/verification/stage_3_examples.json` | Executed valid/invalid loading examples |

README now reflects Stage 3 progress; the environment guide remains labeled as
the historical Stage 2 baseline. The AI log records Stage 2 acceptance and this
stage. `main.py`, both sample decks, and the report template remain unchanged.

`load_flashcards(path)` reads a file, decodes JSON into an unknown value, narrows
the root to the card list, validates every entry, and returns `list[Flashcard]`
in original order. It never rewrites the deck, prints, or exits. If any card is
invalid, no partially valid deck is returned. The list is mutable; the records
are frozen. Future strategies must copy rather than mutate the source ordering.

## Model and validation, compared with TypeScript

`Flashcard` is a frozen dataclass: Python generates its initializer and value
equality, and normal assignment to its string fields raises an error at runtime.
This is similar to a readonly TS record, with runtime assignment protection.
Its type annotations still do not validate incoming JSON. Programmatic callers
can construct records directly and are responsible for honoring their contract;
all untrusted deck data must go through `load_flashcards`.

`payload: object` plays the role of TS `unknown`. `isinstance` checks and explicit
field validation narrow it before construction, rather than an unchecked type
assertion. Nulls, booleans, numbers, and objects are not coerced to strings.

The public `FlashcardLoadError` resembles a custom TS Error with structured
`path` and `detail` properties. Internal format errors and filesystem/decoder
errors are translated at the loader boundary. `raise ... from error` retains
the underlying cause for tests/debugging. Later terminal code can choose how
to display the error; the loader has no terminal or exit-status dependency.
Calling the loader without catching its exception can still show a traceback;
the graceful CLI boundary belongs to Stage 6.

`normalize_text` applies `strip().casefold()`. Loader display fields are trimmed
while preserving capitalization and internal spaces. Normalized pairs drive
duplicate checks and identity; answer evaluation will reuse normalization in
Stage 4. Unicode casefolding treats `Stra\u00dfe` and `STRASSE` alike, but does
not remove accents, collapse internal spaces, or provide fuzzy matching.

`card_id` hashes a fixed ASCII JSON array of the normalized front/back pair
with SHA-256 and prefixes it with `card-v1:`. It does not use paths, list positions,
or Python's randomized `hash()`. JSON field boundaries avoid concatenation
ambiguity. Identical content shares identity across decks. Meaningful front/back
edits change identity; moves/reordering/case/outer-whitespace changes do not.
This stage computes keys only; it does not load or write learning history.

## Accepted formats and examples

Both existing formats work unchanged:

```json
[{"front": "API", "back": "Application Programming Interface"}]
```

```json
{"cards": [{"front": "Which keyword defines a function?", "back": "def"}]}
```

Actual samples load with 10 and 8 cards, respectively. Additional wrapper/card
metadata is allowed but ignored; it does not extend the model or change identity.
No context field was introduced.

Executed example: `bank / financial institution` and ` BANK  / river edge`
load successfully as two cards with distinct IDs. Matching fronts do not imply
alternative answers: the later engine must compare only that card's back.

`API / Answer` and ` api  /  ANSWER ` fail with:

```text
Cards 1 and 2 have identical normalized (front, back) content.
```

`{"front": "API", "back": "   "}` fails with:

```text
Card 1: 'back' must be a non-empty string.
```

These are the public exception's `detail`; its full message also names the
source path. Malformed JSON includes line/column; missing fields name their
one-based card position and field. Duplicate object keys are rejected before
decoding would silently replace their values. This differs from repeated fronts.
NaN/Infinity tokens are rejected as nonstandard JSON, including in metadata.
UTF-8 with an initial BOM is accepted; invalid UTF-8 is an expected load error.

## Actual checks and refinements

All commands ran from `project/starter` using `.venv/Scripts/python.exe`.
Full invocation strings and output are in `verification/stage_3_checks.json`.

| Executed check | Result |
| --- | --- |
| `python -m pip check` | Exit 0, no broken requirements |
| `python -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 0; **79 passed** |
| Coverage across all current production modules, including `main.py` | **100%**; 94 statements and 24 branches, none missed |
| `python -m black --check .` | Exit 0; 7 files unchanged |
| `python -m isort --check-only .` | Exit 0; no warnings after the source-encoding refinement below |
| `python -m flake8 .` | Exit 0; no lint output |
| `python -m mypy .` | Exit 0; strict checks passed on 7 files with target 3.10 |
| `ast.parse(..., feature_version=(3, 10))` on all 7 source/test files | Accepted 3.10 grammar on the 3.13.17 interpreter |

The initial implementation passed 78 tests. An added oversized-integer test
then reproduced an actual failure: stdlib JSON decoding raised a raw `ValueError`
at its integer digit limit. The regression was captured before fixing it.
The loader now translates that decoder failure to `FlashcardLoadError` in the
JSON-decode try block, separately from card validation. The final 79-test suite
includes the regression; no integer safety limit was disabled. Excessive JSON
nesting is also translated at the decoder boundary.

The initial isort run returned 0 but warned when its default Windows locale
could not encode a Chinese test literal. A diagnostic run in Python UTF-8 mode
was clean. Replaced non-ASCII source literals with equivalent Python Unicode
escapes; runtime test files still contain actual UTF-8 text and BOM bytes.
The default isort command is now warning-free. No test was skipped and no source
file was excluded to hide the issue. Black formatted the new test file normally.

Unreadable-file tests inject `PermissionError` and another `OSError` at
`Path.read_text`, because chmod-based permissions are unreliable on elevated
Windows runs. Missing-file, directory-read, invalid-byte, and JSON cases use real
temporary paths/files. Captured-output tests verify silence on success/failure.

All current production files remain in coverage scope. `main.py` and the package
initializer still have zero executable statements. The real Stage 3 coverage
is a checkpoint for implemented models/loading, not proof of the final quiz's
coverage or functionality. The historical Stage 2 zero-statement result is
not submission evidence. Remeasure the completed application in Stages 8-9.

No newer-only syntax/APIs were introduced: 3.10 union annotations and built-in
generic types are supported by the minimum target; the runtime code uses older
stdlib dataclasses, JSON, hashlib, and pathlib APIs. Mypy and grammar checking
are compatibility checks, not runtime testing. **Python 3.10 was not executed**.

Review the loader-only validation boundary, duplicate normalization, strict JSON
handling, and shared content identity. Engine behavior, expected-answer feedback,
preflight deck/history/export alias validation, persistence, and CLI statuses
remain for their planned later stages. Stop after Stage 3 for user review.

## Actual Stage 3 review and conditional acceptance

The user requested exact pre-hash serialization, the integer regression/fix, and
tests for spaces/punctuation. They explicitly authorized acceptance and Stage 4
if these checks found no problems. The existing model serializes normalized
pairs with `json.dumps(pair, ensure_ascii=True, separators=(",", ":"))` before
hashing the ASCII bytes. `("ab", "c")` becomes `["ab","c"]`, while
`("a", "bc")` becomes `["a","bc"]`; their actual digests differ. The existing
field-boundary test asserts distinct IDs. Added tests explicitly verify retained
punctuation and internal spaces in both fields, while casing and outer whitespace
do not affect identity.

The oversized numeric back raised stdlib decoder `ValueError`; the saved
pre-fix regression shows the failure. The existing fix translates `ValueError`
only around `json.loads`. Validation is a separate block catching only its
explicit `_DeckFormatError`. New tests inject unexpected validation `ValueError`
and `RuntimeError` and confirm the original exception objects propagate unchanged.
No production loader/identity change was required.

The focused review command passed **19 tests**, with serialization, actual IDs,
exception cause, and output saved in `verification/stage_3_review_checks.json`.
The checks satisfied the user's stated condition: Stage 3 accepted and Stage 4
authorized. This is not a claim of broader human inspection or personal reflection.
