# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

**Current audit note (2026-11-19):** Real exchanges are grouped by authorized stage.
Earlier pending-review/reflection statements describe the state at delivery;
actual later decisions and student input follow in the relevant entries.
The fictional starter example and blank entries were removed. Student acceptance
on reported evidence is not recorded as independent code or physical testing.

**Authoritative resolution — 2026-11-19:** The student has supplied the full rubric
and made 1,000-1,500 words authoritative. Earlier missing-rubric/length-conflict
statements remain historical, not current unresolved items. Today's actual
checklist review, findings and later report approval follow in the existing Stage 9
entry. No manual Ctrl+C observation has been supplied.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Your Log Entries

### 2026-11-18 - Stage 1: inspect the Flashcard Quizzer starter and propose a plan

**Context:** The user is an experienced TypeScript/frontend engineer learning
Python through an Udacity assignment. The requested local `flashcard` folder
was empty. Only inspection and planning were authorized for this stage.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** The attached request begins "Help me build my Udacity
Flashcard Quizzer CLI assignment" and explicitly says "Perform Stage 1 only"
and "Stop before implementing functionality." The accompanying message was
"theres a new folder for that called flashcard iun the workspace". The request
requires preserving the starter structure/template, proposing behavior and
architecture, documenting actual checks, and waiting for review at each stage.

**AI Response:** Inspected the empty workspace and cloned the named official
starter at commit `808893c4f8639804ab81a031dbd2bc3672d308ba`. Recovered from
Windows-incompatible filenames in unrelated lessons using a project-only sparse
checkout. Inspected docstring-only source/test placeholders, both sample formats,
dependencies, README, report template, design patterns, and collaboration guides.
Proposed a typed model/loader, injectable selection strategies, engine, terminal
adapter, thin CLI, and optional history/export modules. Detailed recommendations,
tradeoffs, stage mapping, and verification are in `stage_1_plan.md`.

**Changes Made:** Imported the upstream starter without changing application
code or sample decks. Added `docs/stage_1_plan.md` and this real entry in
`docs/ai_edit_log.md`. Preserved the official report template and the starter's
explicitly labeled example entry; that example is not actual collaboration and
must be removed before submission. At initial delivery, user review was pending;
the actual follow-up review and resulting revisions are recorded below.

**Reasoning:** Inspect the actual contract before implementation; both array and
object-wrapped decks must work. Keep runtime dependencies in the standard library,
avoid inventing CRUD requirements, and expose unresolved choices before coding.

**Actual Verification:**
- Workspace and ancestor instruction inspection: empty directory; no applicable
  `AGENTS.md` found. Initial `git status --short`: not a repository.
- `git clone https://github.com/udacity/cd14602-project-starter.git .`: initial
  sandbox network failure; elevated attempt downloaded the repo but checkout
  failed on an unrelated lesson's `:Zone.Identifier` path.
- `git sparse-checkout set --cone project`: sandbox config write failed;
  elevated retry set project-only scope. `git read-tree -mu HEAD` still failed
  path validation; command-scoped `git -c core.protectNTFS=false read-tree -mu HEAD`
  succeeded. No persistent filename-safety setting was changed.
- `git rev-parse HEAD`, `git ls-tree`, `git ls-files '*AGENTS.md'`,
  `rg --files --hidden`, and `Get-Content`: established source identity,
  structure, lack of repository `AGENTS.md`, and inspected starter contents.
- PowerShell `ConvertFrom-Json`: glossary parsed with 10 cards;
  python_basics parsed with 8. This does not test a Python loader.
- `git diff --exit-code HEAD -- project`: exit 0 before the two documentation
  changes. Initial populated checkout was clean; Git warned that the sandbox
  could not access the user's global ignore file.
- `python --version`: could not run; `py --list`: not found. `Get-Command`
  identified python/python3 WindowsApps aliases. No Python version is tested.
- Application/pytest/coverage/Black/isort/mypy/flake8: **not run**. Stage 1 has
  no implemented functionality or tests; a usable interpreter is not established.
- Final documentation inspection: `git diff --check` passed. Targeted
  `git diff --exit-code HEAD --` confirmed application placeholders, tests,
  decks, requirements, and report template unchanged. `git status --short`
  showed only this modified log and the new plan. `Test-Path` confirmed the plan
  exists, and `Select-String` confirmed review/unrun-check labels.

**Findings Preserved:** Full classroom Instructions/rubric are absent from the
repository. The report template footer says 2,000-3,000 words while the README
and user request say 1,000-1,500. The generic CRUD feature language has not been
verified against classroom criteria. At initial delivery, history, seeding,
export, and behavior details were recommendations; see the follow-up for the
user's actual acceptances and corrections.

**Outcome:** Stage 1 inspection and written plan prepared. No functionality,
environment setup, installs, commits, pushes, or submissions performed.

**User Review - actual Stage 1 follow-up:** The user asked to refine three
choices before Stage 2: (1) moves/renames must preserve history, with reorder/add/
edit behavior explained without unnecessary infrastructure; (2) "don't reject
cards just because their fronts match," distinguishing repeated fronts from
identical cards; (3) compare cumulative mistakes with a score that increases on
incorrect answers and decreases toward zero on correct answers, using a short
multi-session example before choosing.

The user explicitly accepted outer trimming, case-insensitive comparison, empty
answers as incorrect, partial statistics excluding unfinished answers, and finite
sessions asking each card once. They selected persistent adaptive history,
seeded randomness, and optional JSON export as the proposed additions and asked
for a full-rubric check once they provide it. They directed the classroom's
1,000-1,500-word report limit, retaining the conflicting-template note. They
asked to update this same Stage 1 log entry, explain remaining choices before
implementation, and proceed to Stage 2 once choices settle.

**AI Follow-up and Requested Corrections:** Updated the plan to separate
accepted decisions from proposals. Superseded the initial path namespace with
a proposed shared per-card content hash of normalized front/back/optional
context, independent of path and card order. Explained additions, edits, removals,
restoration, cross-deck sharing, and the alternative of explicit IDs. Removed
duplicate-front rejection. Proposed visible optional context and rejection only
of identical normalized content tuples, with actionable list positions; this
identical-card policy remains for review. Compared cumulative mistakes with
`+1` / `max(0, score - 1)` using five sessions, recommending the latter without
treating it as accepted. No application implementation or Stage 2 setup.

**Review Reasoning:** The user's correction exposes two limitations in the
initial recommendation: path-based namespaces disconnect history on moves, and
front-only uniqueness rejects valid questions. Content keys preserve unchanged
cards through deck edits without a registry, at the cost of shared cross-deck
history and resetting edited card content. A decreasing error balance can retire
old priority after successful practice, while cumulative totals cannot. These
are design revisions, not reproduced application defects or regression fixes.

**Follow-up Changed Files:** `docs/stage_1_plan.md` and this existing log entry.
The official report template remains unchanged. Earlier findings and the
original rejected recommendations remain documented as superseded.

**Follow-up Verification:** `Get-Content` inspected both current documents.
`git diff --check` passed; targeted `git diff --exit-code HEAD --` over
`main.py`, `utils/`, `tests/`, `data/`, the report template, and requirements
exited 0. `git status --short` showed only the modified log and new plan.
`rg -n` confirmed revised identity/scoring/duplicate sections, report limit,
and pending decisions. A PowerShell calculation asserted the five documented
cumulative/error-balance score pairs: `(1,0)/(1,0)`, `(2,0)/(2,0)`,
`(2,1)/(1,1)`, `(2,2)/(0,2)`, `(2,2)/(0,1)`; all matched, and a correct answer
at score zero stayed zero. This is documentation arithmetic verification,
not an application test. No Python, pytest, coverage, or quality tools ran
in this follow-up. The prior interpreter finding remains unresolved for Stage 2.

**Review State at First Follow-up Delivery:** Identity, identical-card/context
handling, and adaptive scoring were still proposals then. The actual second
review below resolves those choices; earlier proposals are retained as history.

**User Review - actual second Stage 1 follow-up:** The user accepted content-based
card identity and explicitly required documenting that identical cards share
history across decks, with both sample formats kept compatible. They rejected
the optional context field: "Don't add a `context` field for now." They accepted
matching fronts with different backs and rejection of identical normalized
`(front, back)` pairs, with errors identifying their positions. They requested
showing the expected answer after an incorrect response to help explain
ambiguous cards.

The user accepted error-balance scoring: incorrect adds one; correct subtracts
one with a floor of zero. History updates use completed answers in every mode.
Adaptive order is fixed at session start, each card is asked once, and ties
preserve deck order. The user explicitly said they had not reviewed history
failures/exit statuses and requested a summary in the conversation before
Stage 1 closes. Stage 2 remains conditional on settling those details.

**AI Second Follow-up:** Updated current plan requirements to the accepted
two-string content key, removed context from identity/model/display proposals,
accepted pair-based duplicate validation and expected-answer feedback, and marked
error balance plus fixed-order/every-mode updates as settled. Retained prior
recommendations and user corrections in this same grouped entry. Expanded the
failure/status proposal into explicit tables: missing history starts fresh;
corrupt/unsupported/unreadable history warns, falls back to zero scores, and is
not overwritten; save failure preserves results and reports unsaved history.
Proposed status 1 for degraded history loading as well as save failures, making
that previously implicit persistence-failure interpretation explicit for review.
Proposed independent attempts at history save and requested export, status 0 for
successful completion/help, 2 for argument errors, 1 for operational errors/EOF,
and 130 for Ctrl+C with interruption taking precedence over secondary failures.
No Stage 2 setup or application implementation.

**Second Follow-up Changed Files:** `docs/stage_1_plan.md` and this same existing
Stage 1 log entry. Sample decks, source/test placeholders, requirements, and the
official report template remain unchanged.

**Second Follow-up Verification:** `git diff --check` passed. A targeted
`git diff --exit-code HEAD --` covering application placeholders, tests, sample
decks, requirements, and the report template exited 0. PowerShell checked the
untracked plan for trailing whitespace and found none. `rg -n` confirmed the
accepted rules, removal of context from current requirements, and pending
failure/status proposals. `git status --short` showed only the two documentation
files. Python/application/quality-tool checks were not run; no setup was performed.

**Review State at Second Follow-up Delivery:** Failure handling, statuses, and
zero-answer `N/A` were awaiting review then. The final actual review follows.

**User Review - final Stage 1 acceptance and refinements:** The user explicitly
accepted the failure rules, exit statuses, and zero-answer display. They required
deck/history/requested export to refer to distinct files, checked before quiz
start using resolved paths and existing-file aliases where supported, with helpful
conflict errors. They specified an explicit history warning: previous scores
could not be loaded, adaptive mode will use deck order, and learning updates will
not be saved during this run; preserve the problematic file. They required
documenting that saves occur at session end/orderly interruption, forced process
termination may lose current-session updates, and atomic replacement protects
partial writes but does not resolve concurrent-session conflicts. Their request:
"Proceed to Stage 2: configure the Python environment and quality tools, report
baseline checks, and stop before application implementation."

**Final Stage 1 Update:** Recorded those acceptances and refinements in the plan,
including a proposed `utils/paths.py` responsibility and tests for resolved paths
and aliases. Classified detected role/path conflicts as invalid argument
combinations (status 2); unexpected path-inspection I/O failures use status 1.
These classifications apply the accepted status categories as implementation
planning details, not additional human statements. No path validator or other
application functionality has been implemented. Stage 1 is closed; Stage 2 is
authorized. Earlier proposals/rejections remain visible in this grouped entry.

**Outstanding Evidence:** Full rubric and personal reflections remain pending.
Acceptance is not taken as evidence of inspection beyond actual statements, and
the grouped Stage 1 review is not fabricated separate examples.

**Lessons Learned:** User reflections pending. Technical explanation provided:
Python Protocols resemble TS structural interfaces, dataclass/type annotations
do not validate JSON at runtime, and selection/I/O separation enables focused
tests without terminal interaction.

---

### 2026-11-18 - Stage 2: configure Python and quality tools; capture baseline

**Context:** Stage 1 behavior choices were explicitly accepted. The user
authorized environment/quality configuration and baseline checks, then a stop
before application implementation.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** "Proceed to Stage 2: configure the Python environment and
quality tools, report baseline checks, and stop before application implementation."
The same message adds path validation, explicit degraded-history warnings, and
persistence-limit documentation, recorded in the existing Stage 1 entry above.

**AI Response:** Investigated unusable Python aliases before installing packages.
No usable interpreter was found in common installation/registry locations.
Consulted official Python distribution and quality-tool documentation/metadata.
Downloaded project-local CPython 3.13.17 from the official Python NuGet package,
created a standard `.venv`, and installed only pinned required development tools
with pip. Direct tool versions were first resolved with Python 3.10 as the
metadata target; actual execution was on Windows CPython 3.13.17 only.

Configured Black/isort at 88 columns, strict mypy with a 3.10 target, pytest
discovery, and branch/subprocess coverage over all production files with an 81%
gate. Added only E203 to flake8's ignored style codes for Black compatibility.
Excluded environments/tools and non-Python Claude command documents from relevant
discovery, without hiding application source or disabling correctness checks.

**Changed Files:** `requirements.txt`, `requirements-lock.txt`, `pyproject.toml`,
`.flake8`, `.gitignore`, `README.md`, `docs/environment.md`,
`docs/verification/stage_2_baseline.json`, `docs/verification/stage_2_followup.json`,
and this log. The final Stage 1 plan/entry also record the preceding acceptance.
Local `.tools/` and `.venv/` are ignored. Source/test placeholders, sample decks,
and the report template remain unchanged.

**Dependency Decisions:** Replaced the broad starter requirements with pytest,
pytest-cov, coverage, Black, flake8, isort, and mypy. Removed unused direct docs,
security, HTTP, CLI-framework, and runtime validation packages. Black still
brings Click transitively. Pinned coverage/flake8 versions retain Python 3.10
metadata compatibility; do not claim an actual Python 3.10 execution result.
The lock file records the actual Windows/3.13 transitive environment and is
explicitly not a universal cross-platform lock.

**Actual Setup and Verification:**
- `Get-Command`, common installation-directory checks, and PythonCore registry
  queries found only WindowsApps Python aliases, no `py`, and no usable existing
  interpreter in the locations checked.
- `Invoke-WebRequest` downloaded CPython's 3.13.17 NuGet archive;
  `Expand-Archive` extracted it under `.tools/`. Its `python.exe --version`
  reported 3.13.17. `python -m venv .venv` succeeded; venv pip reported 26.2.2.
- PyPI metadata was inspected for all seven direct tools. A pip dry run using
  `--ignore-installed --python-version 3.10 --only-binary=:all:` resolved versions
  before the pinned `python -m pip install -r requirements.txt` succeeded.
- `python -m pip check`: exit 0, no broken requirements. `pip freeze` captured
  the actual installed transitive versions in `requirements-lock.txt`.
- `python -m pytest`: exit 5, 0 tests collected. This is a starter gap.
- `python -m pytest --cov=. --cov-report=term-missing --cov-report=html
  --cov-report=json`: exit 5. Report says 100% over **zero executable statements**,
  with a no-data warning. This does not establish coverage or functionality.
- `python -m black --check .`: exit 0, 3 files unchanged.
- `python -m isort --check-only .`: initial exit 0 with warnings for extensionless
  `.claude/commands/*` files; after excluding that non-Python configuration
  directory, rerun exited 0 with empty stderr. Both outputs are preserved.
- `python -m flake8 .`: exit 0, no lint output.
- `python -m mypy .`: exit 0, no issues in 3 source files.
- `python main.py --help` and the specified sequential command both exited 0
  with no output: the placeholder does nothing, so neither is functional success.
- Coverage's effective source/omit/branch/parallel/subprocess/threshold settings
  were read back from the installed coverage API. Scope includes `main.py` and
  all production modules, omitting only tests/local tools/environments.
- Raw commands, outputs, tool versions, and statuses are saved in the two
  verification JSON artifacts. The downloaded archive's observed SHA-256 is
  recorded for reproducibility, without claiming independent publisher proof.

**Setup Refinement:** Isort's scan warnings came from non-Python extensionless
agent documents; the narrow `.claude` skip resolved them. The empty test suite,
zero-statement coverage, and silent CLI are starter omissions, not setup failures.
No application code or artificial tests were added to turn those gaps green.

**Final Artifact Checks:** Compared installed distribution versions with every
direct and transitive pin; parsed `pyproject.toml` and both evidence JSON files;
read coverage's zero-statement file list; checked new plan/environment documents
for trailing whitespace. The initial inspection assertion expected forward-slash
coverage paths but Windows produced `utils\\__init__.py`; corrected the inspection
to normalize separators, then all artifact assertions passed. This was an ad hoc
inspection-helper issue, not an application defect or changed coverage data.
`git diff --check` passed. Targeted `git diff --exit-code HEAD --` over source,
tests, decks, and report template exited 0. `git check-ignore -v` confirmed local
interpreter/venv/cache/coverage artifacts are ignored, and `git status --short`
showed only intended configuration, requirements, README, and documentation
changes. No user files or production code were modified to fix that assertion.

**Outcome:** Python/venv and required tools configured; baseline captured.
No application implementation, commits, pushes, or submission. Stage 2 complete
with final artifact checks passed; review was pending at delivery and is now
explicitly accepted in the following review record.

**User Review - actual acceptance:** The user explicitly said "Accept Stage 2."
They acknowledged that the baseline has no tests/application functionality and
required that the zero-statement coverage result never be presented as submission
evidence. They retained Python 3.10 as the minimum: avoid newer-only syntax/APIs,
keep mypy's target at 3.10, and distinguish compatibility checking from runtime
testing. They authorized Stage 3 models/loading/validation/tests and a stop for
review afterward. This accepts Stage 2; it does not certify runtime testing on
Python 3.10 or supply personal learning reflections.

**Lessons/Explanation:** Explained interpreter-bound `python -m` invocations,
venv isolation, direct pins versus a platform-specific transitive snapshot,
static type checking versus runtime validation, and vacuous zero-statement
coverage. User learning reflections are pending.

---

### 2026-11-18 - Stage 3: implement typed cards and validated JSON loading

**Context:** Stage 2 was accepted. The user authorized typed models, data loading,
and focused tests only, with no CLI/engine implementation yet.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** Implement typed flashcard models and JSON ingestion for both
starter formats using agreed normalization/duplicate rules; separate loader
errors from terminal presentation. Test missing/unreadable/malformed files,
invalid structures/types, blanks, empty decks, and duplicate pairs. Demonstrate
matching fronts/different backs; explain with TS comparisons; show actual tests;
retain Python 3.10 minimum and distinguish static checks from runtime testing;
update Stage 2 acceptance and stop after Stage 3.

**Implementation:** Added frozen `Flashcard` records, `normalize_text`, normalized
pair identity, and versioned SHA-256 content IDs. Added `load_flashcards` with
UTF-8/BOM reading, explicit schema/type/value checks, duplicate-pair positions,
strict object-key/constant handling, and `FlashcardLoadError(path, detail)`.
Unknown metadata is ignored. The loader preserves source order/capitalization,
trims outer whitespace, never prints/exits/writes the deck, and returns no
partially validated result. Programmatic card construction relies on typed
callers; runtime validation of untrusted data belongs to the loader.

**Changed Files:** New `utils/models.py`, `utils/data_loader.py`,
`tests/test_models.py`, `tests/test_data_loader.py`, `docs/stage_3_review.md`,
and four `docs/verification/stage_3_*.json` artifacts. Updated README/current-stage
links, labeled the environment guide's Stage 2 snapshot as accepted/historical,
and updated this log. Source/test initializer placeholders, `main.py`, both
samples, dependency/configuration files, and report template remain unchanged
by Stage 3. No new dependencies or context field.

**Actual Verification:**
- Initial interpreter/dependency check: CPython 3.13.17 and `python -m pip check`
  exit 0. No Python 3.10 runtime was installed or executed.
- Black formatted the new loader test file; the other 3 new files were unchanged.
  Isort was also run on the new files.
- Initial full coverage run: 78 tests passed, 89 statements/24 branches covered.
  Strict mypy/Black/flake8 passed. Isort exited 0 but warned about a Unicode source
  literal under the default cp1252 locale; diagnostic `python -X utf8 -m isort
  --check-only .` was clean.
- Replaced non-ASCII test-source literals with equivalent Unicode escapes. This
  preserves actual Unicode/BOM file data and Unicode casefolding assertions;
  no test assertion was weakened or source file excluded. Default isort rerun
  then exited 0 without warnings.
- Added an oversized-integer regression test and ran it before changing the
  loader: it failed with the decoder's raw `ValueError` on a 10,000-digit back
  value. Saved actual failure output in `stage_3_regression_before.json`.
- Fixed only the JSON-decode boundary to translate decoder `ValueError`, keeping
  card-validation handling separate and leaving the runtime digit limit intact.
- Final `python -m pytest --cov=. --cov-report=term-missing --cov-report=html
  --cov-report=json`: exit 0, **79 passed**, **100%** across 94 executable statements
  and 24 branches in all current production modules. `main.py` remains included
  with zero statements. This is a Stage 3 checkpoint, not final submission proof.
- Final Black, isort, flake8, and strict mypy commands all exited 0. Black reported
  7 unchanged files; mypy reported no issues in 7 files. No warning suppression
  or quality configuration changes were made in this stage.
- Parsed all 7 source/test files using `ast.parse` with `feature_version=(3, 10)`
  on the 3.13.17 interpreter. This and mypy's 3.10 target are compatibility checks,
  not execution on Python 3.10; stdlib API choices were also reviewed for 3.10.
- Executed examples: matching `bank` fronts with two different backs loaded as
  two records with distinct IDs; normalized identical pairs produced an error
  naming positions 1 and 2; blank back produced the named field/position error.
  Saved these results in `stage_3_examples.json`.
- `git diff --check` and targeted `git diff --exit-code HEAD -- main.py data
  docs/report_template.md` exited 0 before documentation updates. Samples,
  entry point, and official report template are unchanged.

**Evidence:** `stage_3_checks.json` records final native commands/status/output;
`stage_3_coverage.json` copies the actual coverage data; the regression-before and
examples artifacts preserve actual execution evidence. The historical Stage 2
zero-statement result is explicitly not submission evidence.

**Final Artifact Checks:** Parsed all four Stage 3 JSON artifacts, asserted all
six recorded final checks exited 0, and verified 94 statements/24 branches with
none missed. Verified the coverage file set includes `main.py`, package
initializer, model, and loader, excluding no production module. Checked new
source/test/review files for trailing whitespace; `git diff --check` passed.
The final targeted entry-point/sample/template comparison again exited 0.

**Testing Limits:** Permission errors are injected at the filesystem boundary
for deterministic Windows/elevated runs; directory and missing-file tests use
real paths. No engine, adaptive history persistence, answer feedback, path-alias
preflight, or CLI behavior is implemented here; later stages retain those tasks.

**Explanation Provided:** Frozen dataclass versus readonly TS record; annotations
versus runtime validation of `unknown`; `object` narrowing; custom error data and
exception causes; mutable deck list versus immutable records; normalized content
identity across decks. Full explanation, examples, tradeoffs, and review points
are in `stage_3_review.md`.

**Outcome:** Stage 3 functionality/tests and evidence prepared. User review
pending; stop before Stage 4. No commits, pushes, or submission.

**User Review - actual conditional acceptance:** The user requested the exact
pre-hash serialization and a field-boundary test; the oversized-integer regression
and exact exception boundary; and confirmation that identity preserves punctuation
and internal spaces while ignoring outer whitespace/case. They authorized recording
acceptance if the checks reveal no problems, then proceeding to Stage 4 with
terminal I/O outside the engine. This is conditional acceptance of those checks,
not an invented claim of inspecting every file or providing personal reflections.

**Review Follow-up and Result:** Showed canonical arrays `["ab","c"]` and
`["a","bc"]` and their distinct actual IDs. Existing tests already checked field
boundaries/internal spacing; added explicit punctuation/internal-space tests for
both front and back and a normalization-equivalence example. Demonstrated that
the 10,000-digit numeric back is wrapped from decoder `ValueError` into
`FlashcardLoadError`. Reviewed the try-block boundary: `ValueError` handling
surrounds only `json.loads`, while the separate `_parse_deck` block catches only
the known `_DeckFormatError`. Added two tests injecting unexpected validation
`ValueError`/`RuntimeError`, which propagated as the exact original objects.
No production change was needed. The review command passed **19 tests** with
empty stderr on CPython 3.13.17; exact serialization, IDs, exception cause, and
output are in `docs/verification/stage_3_review_checks.json`.

**Acceptance Recorded:** The requested checks revealed no implementation problem;
recording Stage 3 accepted under the user's express condition and proceeding to
Stage 4. Test refinements and explanations are part of this same entry. Personal
learning reflections remain pending. Earlier Stage 3 test/coverage artifacts are
historical snapshots and are not overwritten by later-stage checks.

---

### 2026-11-18 - Stage 4: strategies and an I/O-free quiz engine

**Context:** The user conditionally accepted Stage 3 after specific identity and
exception-boundary checks. Those checks passed, as recorded in the Stage 3 entry.
Stage 4 authorization includes engine, sequential/random strategies, grading,
statistics, a demonstration, and a stop for review.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** "Implement the engine, sequential/random strategies, answer
evaluation, and statistics. Keep terminal I/O outside the engine." Test random
mode asks each card once without changing the source deck, without assuming a
shuffle must change order. Explain the Strategy interface, demonstrate three
cards with two correct answers, then stop for review.

**Implementation:** Added a structural `QuizStrategy` Protocol and sequential/
random implementations. Randomness is an optional injected `Random` instance or
a private generator, not module-global state. `QuizSession` snapshots input,
calls the strategy exactly once, validates permutation membership/multiplicity,
and freezes its order. The public API is `current_card`, `submit_answer`, and
`summary`; there are no terminal functions or I/O callbacks. Pure evaluation
uses shared normalization and returns frozen `AnswerResult`. Frozen summary
snapshots derive answered/correct counts, accuracy over completed answers only,
missed cards, and completion. Zero answers yield `None` accuracy, not a fabricated
percentage; later presentation supplies `N/A`.

**Architecture Refinement:** The user expressly required terminal I/O outside
the engine. Superseded the initial plan's injected-I/O sketch with explicit
session state. The future terminal layer obtains input and submits only complete
answers; EOF/Ctrl+C handling can inspect partial snapshots without scoring pending
input. The engine propagates unexpected failures and does not choose exit codes.

**Changed Files:** Added `utils/engine.py`, `utils/strategies.py`,
`tests/conftest.py`, `tests/test_engine.py`, `tests/test_strategies.py`,
`docs/stage_4_review.md`, and checks/coverage/demo Stage 4 JSON evidence. Extended
`utils/models.py` with result/summary records. Updated README/environment links,
the plan's I/O description, and this log. The same turn adds Stage 3 review tests
and evidence in the previous entry and marks that stage accepted under the user's
condition. Loader implementation, `main.py`, samples, requirements/configuration,
and report template are unchanged by Stage 4.

**Tests and Actual Checks:**
- Added 15 strategy tests and 28 engine tests; together with Stage 3 and its
  review additions, the suite now contains 131 tests. Tested empty/single/full
  strategy inputs, source-copy independence, multiple random seeds, same-seed
  reproducibility, global RNG isolation, and an explicitly unchanged shuffle.
- Tested finite random sessions with one completed answer per card and no source
  mutation. Assertions compare length/multisets, never demand a changed order.
- Tested pure normalization, empty answers, punctuation/internal-space matching,
  repeated-front grading against the individual back, zero/partial/full
  statistics, 0/100% extremes, stable snapshots, source/strategy-list mutation,
  an extension strategy without inheritance, and invalid permutation rejection.
- Forbidden-input and captured-output tests verify no terminal I/O. A grading
  failure propagates unchanged without consuming the current card. Finished
  sessions reject extra answers; empty programmatic sessions are rejected.
- Black reformatted engine/test layout; isort ran on changed files. The first
  full Stage 4 coverage run passed: `python -m pytest --cov=.
  --cov-report=term-missing --cov-report=html --cov-report=json`, exit 0,
  **131 passed**, **100%** across 166 statements and 34 branches, none missed.
- Black, isort, flake8, and strict mypy checks all exited 0. Black found 12 files
  unchanged; mypy found no issues in 12 files; no isort warnings. No exclusions,
  weakened assertions, or new quality exceptions were used to obtain a pass.
- Python 3.10 grammar parsed for all 12 source/test files using the 3.13.17
  interpreter; mypy still targets 3.10 and APIs were reviewed for compatibility.
  No execution on Python 3.10 is claimed.
- Saved actual final native commands/exits/output in `stage_4_checks.json` and
  copied the real coverage snapshot to `stage_4_coverage.json`. Historical
  Stage 2/3 artifacts remain unchanged; the zero-statement baseline is not
  submission evidence, and current coverage is not final-feature proof.
- Executed a scripted caller outside the engine: API answered correctly with
  outer whitespace/case normalization, CPU incorrectly, RAM correctly. Actual
  result: 3 answered, 2 correct, 66.67% displayed, CPU missed, complete true.
  Saved raw answer/result/summary data in `stage_4_demo.json`, explicitly labeled
  as scripted demonstration rather than user input. The caller printed feedback;
  engine code performed no terminal I/O.

**Explanation Provided:** Protocol resembles a TS structural interface; a
matching class needs no inheritance. Strategies choose a permutation; the session
engine handles progression/evaluation without mode-specific branches or I/O.
Tuple snapshots and frozen results protect historical observations. Statistics
count only submitted answers, retain raw answers separately from comparison,
and leave percentage rounding to presentation. Full review is in
`docs/stage_4_review.md`.

**Final Artifact Checks:** Parsed/asserted the Stage 3 review arrays/distinct IDs,
all six successful Stage 4 recorded checks, exact coverage file set and
166-statement/34-branch totals with none missed, and the scripted demo's 3/2/CPU/
complete/accuracy results. Source/test/review whitespace checks passed.
`git diff --check` exited 0; targeted `git diff --exit-code HEAD -- main.py data
docs/report_template.md` exited 0, confirming the entry point, sample decks, and
official report template remain unchanged. Git status includes accumulated prior
stage work; nothing was discarded or committed.

**Outcome:** Stage 4 implemented and checks/demo passed. Stop before adaptive
history (Stage 5) or CLI/terminal/path/export work (Stage 6). No commits, push,
or submission.

**User Review - actual conditional acceptance:** The user confirmed the identity
serialization/narrow decoder exception explanation resolves their Stage 3 concerns.
For Stage 4, they requested existing tests proving non-consuming `current_card`,
rejection after completion without result changes, and stable earlier summaries.
They explicitly authorized acceptance and Stage 5 if those tests already pass,
without additional implementation. Ran the three named existing tests:
`test_unanswered_session_has_no_accuracy_or_misses`,
`test_answer_after_completion_does_not_change_results`, and
`test_partial_statistics_and_snapshot_are_stable`. Result: **3 passed**, exit 0,
empty stderr on CPython 3.13.17. Exact command/output are saved in
`docs/verification/stage_4_review_checks.json`. Showed the relevant assertions
and explained the pending-card counts, unchanged completed summary, and differing
new/old partial snapshots. No engine/test implementation change was required.

**Acceptance Recorded:** The user's express condition is satisfied: Stage 4
accepted and Stage 5 authorized. This does not imply inspection beyond those
actual statements, or acceptance of as-yet unwritten history code. Personal
reflections remain the user's to supply.

---

### 2026-11-18 - Stage 5: adaptive score ordering and history persistence

**Context:** The three requested existing Stage 4 state/snapshot tests passed,
satisfying the user's explicit acceptance condition. Stage 4 acceptance/evidence
is recorded in its existing entry. Stage 5 was authorized with a stop for review.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** Implement adaptive ordering and persistent history with
incorrect +1, correct -1/floor zero, stable deck-order ties, fixed session order,
and updates from completed answers in every mode. Verify real two-session
temporary-file round trips, shared identity across decks, missing/corrupt state,
and failed saves preserving old valid history. Separate persistence, selection,
and terminal presentation; explain schema/priority decay, run checks, log, stop.

**Proposal and Implementation:** Demonstrated the agreed policy before coding:
API=1/CPU=1/RAM=0, followed by correct API and wrong CPU, becomes 0/2/0, putting
CPU first next run. Added a stable adaptive sorter using a copied score map.
Added a separate history module: strict `version=1`, `policy=error-balance-v1`,
and content-keyed nonnegative integer scores; pure completed-answer updates;
structured load/save errors; read-only score snapshots; and session-end atomic
saves. The store loads once per run and finalizes at most once to avoid double
updates. Successful saves update memory only after replacement; expected failures
preserve old disk/memory state and permit retry. Zero-answer runs write nothing.

Missing history is a normal writable fresh profile. Corrupt/unreadable/unsupported
history falls back to zero with a structured load error and saving disabled;
attempted saves cannot overwrite it. The store never prints or chooses statuses;
Stage 6 will format the already agreed warning's three effects plus cause/path.
No history file is accessed by the sorter or engine. No real user profile was
created; tests and demos use explicit temporary files.

**Changed Files:** New `utils/history.py`, `tests/test_history.py`,
`docs/stage_5_review.md`, and initial/final checks, coverage, and demo Stage 5 JSON
evidence. Extended `utils/strategies.py` and `tests/test_strategies.py`. Updated
README/environment links and the historical Stage 4 review/entry with actual
acceptance and `stage_4_review_checks.json`. No engine, loader, model, main entry,
sample deck, requirements/configuration, or report-template changes in Stage 5.

**Actual Testing and Refinements:**
- The Stage 4 review command ran the three requested existing tests: **3 passed**,
  exit 0, no implementation/test changes needed, evidence preserved separately.
- Added 58 history tests and five adaptive-order tests. Real file tests cover two
  saved/reopened sessions, every mode's updates, case-normalized shared identity
  across both deck formats, edited/dormant cards, and partial/zero-answer runs.
- Policy tests use explicit before/answer/expected score cases, including zero
  floor. Adaptive tests cover missing scores, stable ties, copying, and score
  snapshot independence; session tests verify finite fixed ordering.
- Validation tests cover root/schema/version/policy/identity errors, booleans and
  other bad scores, all-or-nothing loading, malformed/duplicate-key/nonstandard/
  deep/oversized JSON, UTF-8 errors/BOM, and unreadable-history protection.
- Save tests inject expected failures at parent creation, temp creation, fsync,
  and replacement. Previous valid bytes/memory remain unchanged; cleanup and
  retry are verified. A cleanup failure is included in the structured error;
  double commit is rejected. Unexpected validation errors propagate. Terminal
  capture tests show no printed output.
- Black reformatted the history implementation/test layout. Initial full check:
  193 passed/1 failed, because the test's global `json.dumps` fault mock also
  intercepted card-ID serialization. The initial run additionally found two
  overlong docstrings and three strict-mypy imported-attribute patch errors.
  Saved all initial native outputs in `stage_5_initial_checks.json`.
- Corrected test instrumentation: the serialization mock fails only on the
  history document and delegates card-key encoding; string patch targets avoid
  relying on non-exported module attributes. Shortened docstrings. Production
  history code needed no correction from those results; assertions stayed intact.
- Final `python -m pytest --cov=. --cov-report=term-missing --cov-report=html
  --cov-report=json`: exit 0, **194 passed**, **100%** across 297 production
  statements and 64 branches, none missed. All production modules including
  `main.py` remain in scope. This is current-stage evidence, not final coverage.
- Final Black, isort, flake8, and strict mypy all exited 0; 14 source/test files
  checked, no warnings/lint/type errors. Python 3.10 grammar parsing also passed
  for all 14 files on CPython 3.13.17. API choices were reviewed for 3.10; no
  runtime testing on Python 3.10 is claimed and no new dependencies were added.

**Actual Demonstration:** A scripted caller wrote history to a real temporary
directory, saved a sequential run (API/CPU wrong, RAM correct), reopened it for
an adaptive run (API/RAM correct, CPU wrong), saved/reopened again, and observed
scores 1/1/0 then 0/2/0 with next order CPU/API/RAM. It verified CPU's shared
identity/score in a reversed second deck with casing changes and the other
JSON wrapper, corrupt-file byte preservation with saving blocked, and a
replacement-denial failure preserving valid bytes/memory and removing the temp.
Actual schema documents and results are in `stage_5_demo.json`, labeled as
scripted demonstration rather than user answers. No personal history is committed.

**Persistence Limits Explained:** Saves happen at session end/orderly interruption,
not after each answer; forced termination can lose that session's updates.
Atomic sibling replacement protects destination completeness but does not merge
concurrent sessions or guarantee power-loss durability. Failure/status/warning
presentation and deck/history/export path-alias preflight remain Stage 6 work.

**Explanation Provided:** Versioned schema protects policy interpretation; shared
content keys survive path/deck changes; correct answers reduce priority; stable
sort and engine snapshots preserve session order. A read-only mapping snapshot
resembles TS `ReadonlyMap` with runtime write protection. Store lifecycle separates
load state, pure score changes, and one final commit. Full details in
`docs/stage_5_review.md`.

**Final Artifact Checks:** Parsed/asserted Stage 4's three-test acceptance evidence,
preserved the initial Stage 5 failure record, verified all six final checks exited
0, and checked the exact all-production file set with 297 statements/64 branches
and none missed. Asserted the demo's 1/1/0 then 0/2/0 scores, next order CPU/API/RAM,
shared CPU score, corrupt-byte preservation, and failed-replacement preservation/
cleanup. Source/test/review whitespace checks passed. `git diff --check` and
targeted `git diff --exit-code HEAD -- main.py data docs/report_template.md` exited
0. The user's "contrinue" arrived while this stage's final artifacts were being
checked; treated as continuation of active Stage 5 work, not fabricated evidence
that they had reviewed the as-yet-undelivered Stage 5 summary.

**Outcome:** Stage 5 implemented; final checks and round-trip/failure demonstration
passed. Stop before Stage 6. No commits, pushes, or submission.

**User Review - actual conditional acceptance:** The user requested a test proving
that retrying a failed save persists the same updated scores without counting
answers twice, plus an explanation of arithmetic versus writer ownership. They
authorized acceptance/Stage 6 if it passes. Ran the existing parametrized
`test_failed_save_preserves_previous_valid_history_and_can_retry`: **4 passed**,
exit 0, covering mkdir/temp/fsync/replace. Each starts at score 2; failed save
leaves disk/memory at 2; retrying the same summary reloads score 3, not 4.
Actual command/output is in `stage_5_review_checks.json`.

Explained that pure `updated_scores` owns arithmetic, `HistoryStore.save_session`
owns coordination and adopts the candidate only after `_atomic_save` succeeds,
and `_atomic_save` owns file writing/replacement. Failure therefore leaves the
original base for a retry. No implementation/test change was needed. The user's
condition is met: Stage 5 accepted and Stage 6 authorized. This is not invented
broader human inspection or personal reflection; those remain the user's.

---

### 2026-11-18 - Stage 6: CLI, terminal UI, history, seeds, and JSON export

**Context:** The four existing save-retry cases passed, satisfying the user's
Stage 5 acceptance condition, recorded in its existing entry. Stage 6 was
authorized with actual-entry-point/manual verification and a stop for review.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** Connect CLI/terminal/history/seeded randomness/optional JSON
export. Implement agreed warnings/statuses/partial statistics/path conflicts.
Keep main thin and presentation outside engine/history. Test actual entry point
for help/all modes/invalid args/files/history/export/conflicts/EOF/Ctrl+C; verify
export after failed history save and priority 130. Show actual outputs and a short
PowerShell manual script using temporary history/export; log and stop for review.

**Implementation:** Added argparse composition, deferred default-history lookup,
mode factory, seed restrictions, and independent finalization. Main only imports
the CLI and propagates status under its guard. Terminal module owns UTF-8 streams,
prompts, feedback/expected answers, warnings, and original-position summary tables.
Engine/history implementations remain unchanged. Path preflight resolves all
roles and checks normalized destinations plus samefile aliases before interaction;
unexpected inspection failures are operational errors, and conflicts are argument
errors. The resolved paths are used for subsequent reading/writing.

Added optional atomic version-1 JSON with mode/seed/reason/completion, counts,
unrounded percentage/null, misses, and completed raw/expected answers with IDs
and original positions. No local paths in result documents. History and export
are attempted independently; summaries survive failures, and 130 takes priority.
Test-only runpy bootstraps execute actual main.py for controlled input/I/O faults;
no production code exposes fault flags or reads test environment variables.

**Changed Files:** `main.py`; new `utils/cli.py`, `terminal.py`, `paths.py`, and
`results_export.py`; finish-reason type alias in `utils/models.py`; new
`tests/cli_helpers.py`, `test_cli.py`, `test_paths.py`, `test_results_export.py`,
`test_terminal.py`; README, current/historical review links, this log,
`docs/stage_6_review.md`, `docs/manual_stage_6.ps1`, and Stage 6 initial/final/
coverage/command evidence. Stage 5 acceptance remains in its existing entry and
`stage_5_review_checks.json`. Dependencies/configuration, engine, loader/history
implementations, sample decks, and original report template are unchanged.

**Actual Tests and Refinements:**
- Added 59 collected cases (46 entry-point plus path/export/terminal units).
  The full suite collects 253: **252 passed, 1 skipped**. Native cases test help,
  modes/seed reproducibility, default-home isolation, history reuse, bad flags/
  files, degraded history, independent save/export, all role pairs, resolved/
  hard-link aliases, EOF/zero answers, interrupted input/finalization, UTF-8,
  and safe import of main.py. Existing earlier-stage tests still pass.
- Actual hard-link cases passed. Test symbolic-link creation returned WinError
  1314 (required privilege absent), so that one actual-link case was skipped
  explicitly with reason reported by pytest -rs. No symlink runtime claim.
- Initial pytest passed 252/1 skipped with 99.23% coverage; strict mypy, Black,
  isort, and 3.10 grammar passed. Flake8 found five overlong source lines and
  one unused test import. Wrapped help/test-bootstrap/source text and removed
  the import; no assertions/rules weakened. Preserved initial output in
  `stage_6_initial_checks.json`.
- Final `python -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html
  --cov-report=json`: exit 0, **252 passed, 1 skipped**, **99.23%** across all
  production modules: 546 statements, 106 branches. Main is fully covered with
  both guard branches. Export encoding/cleanup edge paths remain uncovered.
- Final Black/isort/flake8/strict mypy: exit 0; 23 source/test files unchanged/
  type-checked; no warnings/lint/type errors. Python 3.10 grammar parsed all 23
  on CPython 3.13.17. APIs were reviewed for 3.10 compatibility; no Python 3.10
  execution claimed. No new dependencies, suppressions, or exclusions added.
- Export units verify raw/partial data, null no-answer accuracy, expected answers/
  positions, and old-byte preservation on controlled fsync/replacement failure.
  Path units cover absent outputs, canonical paths, unsupported identity fallback,
  and resolution errors. Presentation units keep display controls separate from
  stored data. All source modules, including main, remain in coverage scope.
- Ctrl+C tests inject KeyboardInterrupt at Python input/finalization boundaries
  in actual-entry-point subprocesses, not physical keys/OS signal delivery.
  Expected permission/save failures likewise use deterministic injected boundaries
  with real output-file/byte assertions. Ordinary cases invoke main.py directly.

**Actual Command Outputs:** `stage_6_commands.json` preserves 13 full transcripts
with stdin/args/status/stdout/stderr and injection labels. Native cases include
help, sequential two-correct export, adaptive reuse, seeded random, EOF partial
export, invalid flags/file, conflict rejection, corrupt history continued practice/
export, native export failure, and the exact glossary command with 10 scripted
correct answers. Two explicitly labeled runpy fault cases prove export is written
after history save failure (status 1) and Ctrl+C plus history-save/native-export
failure remains **130** with a partial table. Synthetic data/isolated homes were
used; these are scripted examples, not user answers or personal learning state.

**Manual Script:** The PowerShell script makes temporary deck/history/export files,
prints expected results, retains artifacts, and offers optional physical Ctrl+C.
Direct invocation was blocked by local script policy. Verification used a child
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File ... -SkipInteractive`;
process exited 0 and all status markers matched (0/0/0/1/2/1/1). Machine/user policy
was not changed. Initial policy rejection and full successful output are in
`stage_6_checks.json`. Physical Ctrl+C remains a manual step, not an executed claim.

**Explanation Provided:** CLI composes typed domain APIs; terminal owns prompts/
warnings/tables; engine owns grading/state; pure score arithmetic and atomic history
writer retain their reviewed ownership. Paths are checked before interaction;
independent finalization and interruption priority implement the accepted policy.
Result completion describes answered questions independently of command status.
Current README/review explain schema, flags, actual outputs, and verification limits.

**Final Artifact Checks:** Parsed/asserted all six final check exits, the four-case
Stage 5 acceptance evidence, exact production coverage scope including fully
covered main guard, 546 statements/106 branches, and 13 actual command transcripts.
Verified status 130 plus both secondary-error messages in the interruption case.
Read the manual script's retained synthetic artifacts: original 2-correct export,
one-answer partial export, completed degraded-history export, corrupt bytes still
present, and final valid history scores. Source/test/README/review/script whitespace
checks passed. `git diff --check` and targeted sample/report-template comparison
exited 0. Historical artifacts and accumulated prior-stage edits are preserved.

**Outcome:** Stage 6 functionality, evidence, manual script, and final artifact
checks complete; user review pending. Stop before Stage 7 defect review. No
commits, pushes, publication, or submission.

**Review State at Initial Stage 6 Delivery:** User review was pending. The initial
export choices described above are superseded by the actual refinement below.

**User Review - actual export refinements before acceptance:** The user asked why
raw answers were included, required default export to contain metadata/statistics/
missed cards, and requested removing raw answers absent a concrete agreed need.
They required refusal of existing exports unless explicitly authorized with
`--overwrite`, preservation of atomic authorized replacement, and byte-preservation
tests. Existing history updates must remain normal behavior. They requested help,
README, tests, and this same Stage 6 log be updated, affected checks rerun, and a
stop for review. They expressly required physical Ctrl+C remain unverified until
they perform the manual check. Stage 6 acceptance was not granted.

**Follow-up Rationale and Changes:** Acknowledged raw export was an unrequested
audit convenience, not an agreed requirement. Removed the whole per-answer array;
results now contain exactly metadata, aggregate statistics, and missed-card data
(identity/position/front/expected answer). No raw-answer option was added. Engine
records remain internal; history never stores submitted text. New-schema tests
assert absence of synthetic submitted text and the exact allowed root fields.

Added keyword-only `overwrite=False` to the export API and `--overwrite` CLI
flag, which requires `--export`. Refusal occurs at export finalization with status
1, after normal quiz/history handling, preserving the prior export. History is
unaffected by the flag. Existing-file inspection precedes staging; exclusive
hard-link publication of a closed/synced staging file prevents overwriting a
destination that appears after the initial check. Unsupported publication fails
safely. Explicit replacement still uses atomic `os.replace`. Role-conflict checks
remain mandatory even with the flag.

**Follow-up Files:** `utils/results_export.py`, `utils/cli.py`,
`tests/test_results_export.py`, `tests/test_cli.py`, README,
`docs/stage_6_review.md`, `docs/manual_stage_6.ps1`, this entry, and new
`stage_6_export_review_checks.json`, `stage_6_export_review_coverage.json`, and
`stage_6_export_review_commands.json`. Engine/history/model/main/path validation,
dependencies/configuration, samples, and report template were unchanged by this
review. Initial delivery artifacts remain historical, not the current contract.

**Actual Follow-up Verification:**
- Added nine collected cases: three export units (default refusal, authorized
  replacement, competing destination), two CLI policy cases, an invalid
  overwrite-without-export argument, and three additional role-conflict cases
  with overwrite enabled. Existing authorized-failure tests now explicitly set
  the flag so they continue exercising actual write failures rather than refusal.
- Random/member/order assertions now use question prompts and missed-card records
  in all-wrong sessions instead of the removed per-answer array, retaining
  one-card-once/source-preservation checks. Export schema tests assert no submitted
  text, exact allowed keys, statistics, and expected missed-card content.
- CLI consecutive-session test verifies scores 1 -> 2 despite byte-preserving
  export refusal, then 2 -> 1 on correct answers with explicit replacement.
  Another test retains 130 when an existing export is refused after injected
  interruption. All three file-role conflict pairs reject even with the flag.
- Full suite rerun: `python -m pytest -rs --cov=. --cov-report=term-missing
  --cov-report=html --cov-report=json`, exit 0, **261 passed, 1 skipped**,
  **98.96%** across all production files: 562 statements/112 branches. Same
  symbolic-link creation skip: WinError 1314, missing Windows privilege.
- Black/isort/flake8/strict mypy and Python 3.10 grammar checks passed for all 23
  source/test files. Initial follow-up flake8 found one overlong help line; it was
  shortened, with help test/quality checks and then the full suite rerun. Initial
  lint output remains in the review-check artifact; no rule was relaxed.
- Runtime remains CPython 3.13.17 only. Mypy/grammar target 3.10 is compatibility
  evidence, not 3.10 runtime execution. No dependency or exclusion changes.
- Reran the manual script with `-SkipInteractive` in a process-scoped PowerShell
  policy override. Status markers included refusal 1, preserved-byte hash True,
  and authorized replacement 0; history used a separate temporary profile.
  The write-failure scenario supplies --overwrite to exercise native failure.
- New direct-entry-point transcripts assert creation 0 / refusal 1 / replacement
  0, no submitted text/answer fields, equal byte hashes on refusal, and history
  values [1,1,1] -> [2,2,2] -> [1,1,1]. These use synthetic temporary fixtures.

**Follow-up Artifact Checks:** Asserted all recorded checks exited 0, the exact
metadata/statistics/misses schema, equal before/refusal export hashes, changed
authorized-replacement hash, and independent history values 2 then 1. Verified
retained manual output contains refusal/byte-preservation/replacement markers
and its final export has three correct with no submitted-answer records. Current
coverage includes every production module (562 statements/112 branches).
Whitespace checks and `git diff --check` passed; samples/report template remain
unchanged. Both new check/transcript artifacts explicitly mark physical Ctrl+C
unverified. Historical artifacts were preserved rather than rewritten.

**Review Status at Export-Refinement Delivery:** Implementation was complete and
review pending. The user's subsequent actual acceptance follows.

**User Review - actual Stage 6 acceptance:** The user said "Accept the Stage 6
export refinements based on the reported tests" and explicitly kept physical
Ctrl+C unverified. Stage 6 acceptance is recorded on that stated basis; no physical
manual test or broader human inspection is inferred. They authorized Stage 7
review of all code/tests, with findings before any code changes, confirmed defects
separate from optional improvements, reproductions/consequences/proposed regression
tests, attention to overwrite/independent failures/interruption/path conflicts,
and an explanation of uncovered behavior/symlink skip without exclusion changes.
They requested the log updated and a stop for review.

**Physical Ctrl+C remains unverified.** Only injected KeyboardInterrupt and
noninteractive script portions have run. Personal reflections/full rubric remain
pending. No fixes are authorized by Stage 7's findings-only request in this turn.

---

### 2026-11-18 - Stage 7: complete code/test review, findings before fixes

**Context:** The user accepted the Stage 6 export refinements based on reported
tests; that actual acceptance is recorded in the existing Stage 6 entry.
Physical Ctrl+C remains unverified. They requested a review of the complete code
and tests before any code changes, defect reproductions/consequences/proposed
regressions, separate optional improvements, uncovered behavior and symlink-skip
explanations, a log update, and a stop for review.

**AI Tool Used:** Codex.

**Prompt/Request:** Review agreed requirements, focusing on export overwrite
protection, independent persistence/export failures, interruption, and file-role
conflicts. Do not change code before presenting findings or change coverage
exclusions.

**AI Response:** Reviewed models, decoding/validation, engine, all strategies,
history, paths, terminal, export, CLI/entry point, associated tests and project
configuration/documentation. Reported two confirmed finalization defects (P2)
with actual entry-point diagnostics and a normal control. F1: a single injected
KeyboardInterrupt at the unguarded history permission check returns 130 but skips
both persistence and export. F2: a real closed OS pipe during original summary
printing raises OSError on Windows, skips both writes, and returns 1 even after
an input interruption already required 130. For each, documented reproduction,
impact, narrow proposed correction and regression expectations. These are
diagnostic injections, not physical Ctrl+C verification.

**Changes Made:** Added `docs/stage_7_review.md`, reproduction evidence in
`docs/verification/stage_7_reproductions.json`, fresh check/coverage evidence and
a before/after source/configuration hash manifest. Updated this log only for the
actual user acceptance and current review. Application code, tests, README,
dependencies and coverage configuration/exclusions were not changed. No defect
fix was made.

**Reasoning:** Existing passing tests verify default export byte preservation,
late-arriving-destination protection, authorized atomic overwrite, expected
history/export failure independence, interruption inside selected calls, and
canonical/hard-link conflicts. They do not cover every asynchronous interruption
boundary or terminal output failure. Reproducing those gaps separates observed
defects from optional additional error-boundary coverage. A finalization fix must
retain exactly-once history updates and avoid hiding unexpected programming errors.

**Actual Checks:** Full suite: 261 passed, 1 skipped in 17.20 seconds; combined
statement/branch coverage 98.96% (562 statements, 112 branches, six missing statements, one partial
branch). Black, isort, flake8, strict mypy all passed. Python 3.10 grammar parsing
passed for 23 files; actual runtime was Windows CPython 3.13.17. Python 3.10
runtime compatibility remains unverified. Remaining uncovered export branches:
destination inspection OSError, JSON encoding ValueError, cleanup OSError, and
failure before a temporary path exists. No exclusion changes.

**Diagnostic Results:** Starting A's score at 2, one wrong answer plus EOF normally
saves 3 and exports (status 1). An injected one-shot interrupt at the history
permission guard leaves 2/no export (status 130). A native closed-summary-pipe
failure leaves 2/no export with a traceback (status 1), including after input
KeyboardInterrupt where status should remain 130. Full bootstraps, outputs and
file observations are preserved in the reproduction artifact.

**Environment Limit:** The symbolic-link alias case skipped after WinError 1314
because this process lacks the required creation privilege. Actual hard-link and
resolved-name tests passed; these do not substitute for a real symlink run.
Physical keyboard Ctrl+C remains unverified. The full rubric is still pending.
The classroom 1,000–1,500-word report limit and conflicting-template-footer note
remain recorded; report drafting is Stage 8 work.

**Outcome at Initial Stage 7 Delivery:** Review/report/evidence complete; two confirmed defects await user
review before changes. Stage 7 is not accepted. Stop here. No commits, push,
deployment, submission, or invented human review/reflection.

**User Review - actual fix authorization:** The user said "Approve fixes for F1
and F2." They required regression tests first with failures against unchanged
code, the smallest correction keeping display/history/export independent,
one-shot transition-interrupt recovery with status 130, no repeated committed
history updates, and an explanation of uncertain write outcomes without blind
retry. Expected terminal output errors must be caught narrowly, completed answers
must still save/export, EOF/interruption must retain 1/130 without expected-error
tracebacks, and export content/overwrite protection must remain unchanged. They
excluded optional coverage additions, requested full checks and before/after
evidence, and required a stop before Stage 8. This authorizes these fixes, not
acceptance of the resulting implementation.

**Regression-First Evidence:** Saved original source and SHA-256 hashes before
editing production. An initial bootstrap collection attempt had nested string
delimiter syntax wrong; corrected the test harness before drawing conclusions.
Then the proposed six cases ran against unchanged application code: four failed,
two passed. Added feedback-output and programming-error safeguards before
implementation: five failed, five passed including existing terminal cases.
The red outputs and original code are preserved in Stage 7 fix evidence.

**Authorized Changes:** Finalization now retains the next pending phase inside
an interrupt-handling loop. Read-only preparation can resume after a one-shot
interrupt. Each side effect is marked attempted before invocation; completed or
uncertain writes are not replayed. The CLI separately catches structured history
and export failures, and narrow TerminalOutputError, while retaining status 130.
Terminal writes translate only OSError/UnicodeError around print/flush; formatting
stays outside that boundary and a RuntimeError regression still propagates. Quiz
output failure finalizes completed answers with finish reason output_error.

**Shutdown Follow-up Within F2:** The first correction passed 269 tests/one skip,
but an additional native closed-pipe check without restoring stdout exposed
Python shutdown flushing the same failed descriptor and replacing status 130
with 120. Preserved this probe and initial passing check/hash evidence. Added
the two permanent-pipe cases before correction: two failed, seven passed. The
terminal boundary now redirects the failed native descriptor to the null device
before raising its structured error, preventing the repeated shutdown flush.
These F2 regressions now retain statuses 1/130 without traceback or shutdown
exception output. This is core status preservation, not the optional export
coverage work the user excluded.

**Uncertain Commits:** A test interrupts before a history commit; another performs
the real os.replace then raises KeyboardInterrupt before the store adopts scores
in memory. Both make exactly one save attempt, continue export, and return 130.
Their disk scores remain 2 and 3 respectively. A separate interrupt after successful
history saving also leaves score 3 and one save attempt while export continues.
The coordinator does not infer noncommit from an exception or from can_save.
Known structured save-failure retry behavior in HistoryStore remains unchanged.

**Final Actual Checks:** 271 passed, one skipped in 20.80 seconds; combined statement/branch coverage
98.20% (599 statements, 124 branches, nine missing statements, four partial
branches). Black, isort, flake8, strict mypy all passed. Python 3.10 grammar checks
passed on all 24 Python files; actual runtime remains Windows CPython 3.13.17.
Focused regression/terminal set: 12 passed. Coverage exclusions, export code and
optional export tests are unchanged; overwrite preservation/path conflict tests
still pass. Export contains no raw submitted answers. README now reflects these
results and interruption/output behavior.

**Evidence and Review State:** Added docs/stage_7_fix_review.md and red/expanded-red/
shutdown-red, before/after command outputs, original/intermediate/final hashes,
and check/coverage artifacts under docs/verification/stage_7_fix*.json. The initial
Stage 7 findings remain historical evidence with a link to the fixes. The optional
export error-boundary cases were left out. Physical Ctrl+C, Python 3.10 runtime,
and the WinError 1314 symlink case remain unverified. Forced termination, repeated
interrupts and concurrent writers remain limitations. Fixes await the user's
review; Stage 8 has not begun. No commits, push, deployment, or submission.

**User Review - actual Stage 7 acceptance:** The user said "Accept Stage 7 based
on the reported regression evidence and explained limitations." Acceptance is
recorded on that basis, without inferring independent code inspection, physical
terminal testing, or broader verification. They authorized Stage 8 verification,
README/log audit, and a report using the official template and agreed word limit,
with student reflections requested before writing them. They explicitly retained
the full-rubric, physical Ctrl+C, Python 3.10 runtime, and symlink gaps and required
a stop after Stage 8 without commit, push, or submission.

**Stage 8 Audit Clarification:** The historical 98.96% and 98.20% values above are
coverage.py's combined statement/branch figures, not branch-only percentages.
Only those labels were corrected; original output/evidence and result values
remain unchanged. The fresh Stage 8 entry reports separate statement and branch
ratios. Earlier "pending" review/reflection statements describe their delivery
time and are resolved only by the actual later messages recorded here/in Stage 8.

**Lessons Learned:** AI review observation: high coverage can coexist with
uncovered combinations of terminal failure and finalization interruption.
The user's personal reflection is pending.

---
### 2026-11-18 - Stage 8: verify, audit documentation, and draft the report

**Context:** The user accepted Stage 7 on reported regression evidence and
explained limitations. That actual acceptance is recorded in its existing entry.
Stage 8 authorizes verification and documentation only, followed by review;
commit, push, submission, and Stage 9 reproduction remain unauthorized.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** Run required tests/coverage/quality checks and save actual
results; distinguish combined coverage from statement and branch figures. Update
README, audit this log without invented human review, and draft a 1,000-1,500-word
report using the official template with its conflicting-footer note. Use F1/F2
as actual review/correction examples. Ask for the student's own reflections
before writing those sections and continue factual work while awaiting answers.
Retain full-rubric, physical Ctrl+C, Python 3.10 runtime and symlink gaps, then stop.

**AI Response:** Read the supplied original request, preserved official template,
current README, log, configuration, and historical evidence. Asked for personal
reflections first using asynchronous user input, continued factual verification,
and then asked for the template's self-ratings and student name. Both responses
arrived before the personal sections were drafted. Wrote factual sections from
repository/evidence, personal sections from those actual responses, and
distinguished assistant-executed checks from student review based on evidence.

**Changes Made:** Updated README behavior/limits/current evidence links; recorded
actual Stage 7 acceptance in its existing entry; removed the explicitly fictional
example and two empty entry placeholders; corrected two historical combined-
coverage labels and the same label in docs/stage_7_review.md without changing
result values or raw evidence. Added docs/final_report.md following the official
headings, docs/stage_8_verification.md, and Stage 8 checks/coverage/metrics/log-audit/
report-validation/unchanged-source hash artifacts. Kept grouped historical
requests, proposals, acceptances, failures and corrections visible. No application,
tests, dependencies, quality configuration, sample decks or template were changed.

**Reasoning:** A branch-enabled coverage.py total combines covered statements and
branch outcomes. It must not be described as branch-only coverage. Similarly,
passing static checks is not runtime compatibility, injected KeyboardInterrupt is
not physical signal verification, and staged acceptance is not proof of independent
code inspection. Personal reflections and self-ratings belong to the student.
The summary counts detailed stage entries, not raw chat turns; line-by-line AI
authorship/edit counts and personal interaction rankings were not tracked.

**Actual Student Reflection Response (verbatim):**

> What I learned: Python type annotations don’t validate JSON at runtime, much like TypeScript types. I also learned how Protocols resemble structural interfaces, and why high coverage doesn’t guarantee correct behavior across failure scenarios.
>
> Suggestions I questioned: I challenged path-based history identity because moving a file shouldn’t erase progress, and cumulative mistake scoring because learned cards could remain prioritized indefinitely. I also requested removing unnecessary raw answers from exports and requiring explicit permission to overwrite results.
>
> The staged workflow: Pausing between stages gave me manageable decisions to review. However, the repeated review rounds were lengthy, and I relied on explanations and test evidence for Python details I couldn’t independently assess.
>
> Next time: I’d provide the full rubric earlier, agree on data storage and export behavior before implementation, and run manual terminal checks earlier alongside automated tests.

**Actual Student Self-Assessment Response (verbatim):**

> Readability: 4/5. Clear module responsibilities and typed models. Finalization and stream handling require more careful reading.
>
> Maintainability: 4/5. Engine, storage, and presentation are separated. Interruption handling adds complexity, but its tradeoffs are documented.
>
> Test quality: 4/5. Strong behavioral tests and regression evidence, including entry-point subprocesses. Physical Ctrl+C, symlinks, and Python 3.10 runtime remain unverified.
>
> Documentation: 4/5. Detailed setup instructions, behavior, limitations, and verification records. Clean-environment reproduction and the full rubric audit remain pending.
>
> Student name: A***** P*****.

These are student-supplied opinions and ratings, not external quality scores.
Earlier reflection-pending statements remain historical; this is when input arrived.

**Actual Verification:** Ran the full pytest/coverage command in the existing
Windows CPython 3.13.17 venv: 271 passed, one skipped in 21.78 seconds, exit 0.
Combined coverage: 710/723 = 98.20%; statements: 590/599 = 98.50%; branch outcomes:
120/124 = 96.77%. Nine executable statement lines and four branch outcomes remain
uncovered; four branches are partial. main.py and every production module remain
included, with the original 81% combined gate and exclusions unchanged.
Black, isort, flake8, strict mypy and pip check all exited 0. Python 3.10 grammar
parsing passed on 24 files on the 3.13 runtime. Full commands/output are saved in
stage_8_checks.json; raw coverage and separately derived metrics are retained.
The Stage 2 zero-statement result remains explicitly unsuitable submission evidence.

**Metrics and Report:** AST/source inspection measured production: 11 files,
1,162 physical lines, 976 nonblank lines, 62 function definitions including methods
and nested functions, and 22 classes. These are measured size statistics, not
AI-authorship counts. The report has 1,223 rendered-text whitespace words including
all headings, appendices, and footer (1,270 raw Markdown whitespace tokens).
The classroom limit is retained; the original template and conflicting footer
are unchanged. Student name, supplied reflections, and four 4/5 self-ratings are
used. No submission date, due date, missing rubric, or human inspection is invented.

**Log Audit:** Checked actual Stage 1-7 requests/decisions and their acceptance
basis against visible conversation and retained evidence. Retained rejected
identity/duplicate/scoring/context proposals, zero-test setup baseline, decoder
regression, test-mock/type/lint corrections, export refinements, F1/F2 red/green
runs, and shutdown status-120 correction. The Stage 5 "contrinue" remains only
continuation. Historical reviews resolve only through actual later acceptance.
The template example was never counted as collaboration and has now been removed.
One documentation search passed a Windows wildcard as a literal path; reran with
rg's glob filter. This was a search correction, not an application/check failure.
An initial report-validation helper failed its footer assertion because Windows
PowerShell's ASCII stdin transport replaced its literal en dash with question
mark (observed code point 63). The UTF-8 report was correct. Changed only the
helper to use escaped Unicode; validation then passed for both word counts,
template headings, student name/ratings, local links, source hashes and coverage
scope. This was an inspection-helper correction, not an application/test failure.

**Outstanding:** Full classroom rubric unavailable; physical Ctrl+C unverified;
Python 3.10 runtime untested; real symlink test skipped after WinError 1314.
Hard-link success is separate evidence. Clean-environment reproduction is Stage 9
and was not performed. Forced termination, repeated interrupts, uncertain writes,
unusable diagnostic streams, concurrent-session conflicts, and preflight-only
path validation retain their documented limits. Optional coverage additions remain
deferred; no exclusions changed.

**Outcome:** Stage 8 checks, README/log audit, report draft, and evidence prepared.
Student personal input is incorporated, but Stage 8 review/acceptance is pending.
Stop before Stage 9. No commit, push, publication, or submission.

**User Review - actual Stage 8 acceptance:** The user accepted "Stage 8's
verification and documentation work based on the reported evidence" while keeping
report wording subject to final review. They authorized Stage 9 clean reproduction
using only README/submission files, actual command evidence, and an audit against
available criteria. They requested Python 3.10 runtime and real symlink checks if
possible, a minimal physical Ctrl+C procedure, explicit unavailable checks, and
concrete gaps before application changes. Missing full rubric limits compliance
claims. Stop with findings; no commit, push, or submission. Report wording is not
accepted by this statement.

**Lessons Learned:** Student reflections above are the only source for personal
learning claims. Audit observation: measure and label coverage components
separately, and preserve the provenance and limits of both tests and review.

---

### 2026-11-18 - Stage 9: clean reproduction and final available-criteria audit

**Context:** The user accepted Stage 8 verification/documentation based on reported
evidence, explicitly leaving report wording subject to final review. That
acceptance is recorded in its existing entry. Stage 9 authorizes clean setup,
documented commands, an evidence audit, available runtime/alias checks, logging,
and final findings. No commit, push, submission, or application change is implied.

**AI Tool Used:** ChatGPT / Codex.

**Prompt/Request:** Reproduce using only README/submission files in a separate
clean environment and save actual results. Audit every available criterion,
required files, report length, relative links, sample data, coverage scope and
credentials/environment/cache/personal-state exclusion. Verify Python 3.10 and
actual symlinks if permitted, mark unavailable checks honestly, provide the
shortest physical Ctrl+C procedure, and report gaps before application changes.
Treat the missing full rubric as an audit limit; stop with final findings.

**AI Response:** Copied 106 selected submission files into an ignored reproduction
directory, preserving repository-root/project/starter layout and the license
link. Selection included current tracked and untracked work, excluding ignored
files; no old venv, .tools, caches or .git was copied. Created new venvs in two
identical submission snapshots, using CPython 3.13.17 and newly downloaded 3.10.11.
The copies contain all source/tests/docs needed by the README, without importing
original-workspace application modules or old site-packages. Base interpreters
are prerequisites, not copied application dependencies.

**Setup Failures and Corrections:** Default sandbox network access blocked NuGet
and PyPI; the pip output's no-matching-version message followed connection denial,
not an unavailable pin. Saved these failures, then reran the same install with
allowed network access. Both fresh environments installed requirements.txt and
passed pip check. Pip could reuse standard download caches; no old environment
was reused and no cold-cache/new-OS claim is made. CPython 3.10.11 came from the
official NuGet package URL and its observed SHA-256 is recorded, without claiming
independent publisher authentication. Conditional 3.10 dependencies differ from
the Windows/3.13 lock, as README already instructs; no pins were changed.

**Actual Clean Results:** CPython 3.13.17: 271 passed, one skipped in 22.69 seconds.
CPython 3.10.11: 271 passed, one skipped in 22.53 seconds. All documented Black,
isort, flake8, strict mypy and pip-check commands exited 0 in both environments.
Each has its own prefix/site-packages, include-system-site-packages=false, and
disabled user site. Each measures 590/599 statements (98.50%), 120/124 branch
outcomes (96.77%), and combined 710/723 (98.20%). All 11 production modules,
including main.py, remain in scope. Neither exclusions nor the 81% gate changed.

**Documented Commands:** In each copy, ran help, the exact sequential glossary
command, adaptive python_basics, seeded random export, and authorized overwrite:
all five exited 0. Inputs came from sample backs, not the student's answers;
the random run does not imply every streamed answer matches its shuffled card.
Default HOME/USERPROFILE was isolated. Final export has only the agreed
metadata/statistics/missed-card schema. Saved full transcripts and per-runtime
pip freeze. Reran the documented PowerShell script with -SkipInteractive in the
3.13 clean copy; exit 0 and all status/hash markers matched. This is not physical
Ctrl+C verification.

**Actual Alias Limits:** A fresh native symlink probe failed with WinError 1314;
a real hard-link probe passed. Both full suites skipped the same symlink test.
An additional outside-sandbox targeted attempt hit pytest temp/cache permission
errors before tests ran. Retried with a new isolated --basetemp and no cache:
one hard-link test passed, one symlink case skipped with WinError 1314. No Windows
privileges/settings were changed. Actual symlink behavior remains unverified;
available broader execution did not remove that limit.

**Audit Findings Before Application Changes:** No application defect was
reproduced and no application/test/dependency/configuration changes were made.
Three inherited root README targets (www.item1.com, www.item2.com, www.item3.com)
are invalid relative links. Application README/report links resolve in the
preserved layout. Left root placeholders unchanged as a repository-level gap.
Current candidate files contain no detected credentials, venvs/tools/caches,
generated coverage directories or personal learning state. Recognizable secret
patterns/credential filenames are absent; the scan is not proof against arbitrary
secrets. Synthetic histories in tests/evidence and the supplied author name are
intentional. .env/private.key are not ignored by current rules, an optional
hardening gap with no detected leak; no ignore-policy change was made.

**Source/Submission Checks:** Original 10-card array and 8-card object-wrapper
samples validate; sample/template diff against HEAD is clean. All parsed named
source/test functions have docstrings and explicit annotations (self/cls implicit;
embedded bootstrap strings are outside that AST count). Required app/tests/docs/
requirements/configuration are present; current-source hashes match both tested
copies. The Git HEAD remains the initial starter commit. Ignored local artifacts
remain on disk but are excluded from the candidate selection; no cleanup or
whole-worktree archive is represented as a sanitized submission.

**Documentation Changes:** Updated README/environment factual verification status
and added docs/stage_9_audit.md plus Stage 9 setup/check/coverage/command/inventory/
hygiene/link/report/hash evidence. Updated only report facts: clean results,
runtime status, ninth log entry and current gaps. Learning/reflection sections and
four student ratings are unchanged; ratings are now explicitly contextualized
as supplied during Stage 8. The report is 1,253 rendered words (1,300 raw Markdown
tokens), still within 1,000-1,500 and the template headings. The conflicting
template-footer note remains, and report wording still awaits final student
review. Initial documentation patch context and orchestration quoting errors
were corrected before further execution; these were helper errors, not product
failures. Original/updated documentation differences are retained.

**Final Audit Checks:** Mapped 33 available criteria without claiming the missing
rubric. Final candidate inventory contains 125 files. Checked 69 local Markdown
file links; only the three inherited root placeholders are missing, and no
heading-fragment references were present. Application README/report links pass.
All 31 protected files and both tested snapshots match current source. Report
headings and word counts pass, original README command blocks remain intact,
and personal reflection/rating text is unchanged. Final bounded credential/artifact
scan has no findings; optional ignore gaps remain explicit. Validation data and
actual command outputs are retained under docs/verification/stage_9_*.json.

**Outstanding and Manual Procedure:** Full rubric unavailable, preventing complete
rubric compliance claims. Physical Ctrl+C and actual symlink behavior remain
unverified. Other interpreter patches/operating systems were not tested. The
short manual check uses a unique temporary path, one blank completed answer,
then Ctrl+C at the second prompt and immediate inspection of LASTEXITCODE;
expected status 130 and partial one-answer history/export. No physical result is
recorded without the user's actual run.

**Outcome:** Clean reproduction and the available-criteria audit completed with
concrete gaps and evidence. Root README placeholder links, optional credential
ignore hardening, unavailable rubric/symlink/physical checks, and final report
wording remain for review. No claim of full rubric compliance, no application
changes, and no commit, push, publication or submission. Stop with findings.

**User Review and Cleanup — 2026-11-19:** The user accepted Stage 9's reproduction
evidence and requested removing/fixing the three inherited README placeholder
links, narrowly scoped .env/private-key ignore rules preserving examples, actual
link/exclusion verification, and recording results. They explicitly retained the
missing rubric, blocked symlink test, physical Ctrl+C, final report-wording review
and manual result as unresolved; no submission-readiness claim is authorized.
They required a stop after cleanup without commit, push or submission.

**Cleanup Changes:** Replaced the root README's three placeholder targets with
the real application README link. Added a root .gitignore so credential-name
rules apply throughout the repository, including outside project/starter. The
rules target .env variants, .key/key.pem/private-PEM conventions and standard SSH
private-key names; they do not blanket-ignore PEM certificates or JSON. Explicit
example/sample/template and recognized public-key names remain eligible. Updated
current README/report cleanup facts and added a dated note to the original audit;
preserved historical failing-link/ignore evidence and student personal text.

**Cleanup Verification:** 168 actual git check-ignore probes passed across root,
starter, and nested locations. Expected credential names are ignored; named dummy
examples/templates, public keys, certificates and ordinary JSON remain eligible.
No recognized environment/key example files existed to modify, and no existing
submission candidate became hidden. The new root .gitignore is explicitly included
in candidate selection. All 69 current Markdown relative file links were checked,
including the root/application READMEs and report; none are broken. All 31
application/test/dependency/configuration/template/sample hashes are unchanged.
The report remains within the agreed limit at 1,255 rendered words; wording is
still a draft for the student's review. Source/tests were not changed, so the
cleanup did not rerun or relabel earlier runtime/coverage checks as new results.
Actual results are saved in docs/verification/stage_9_cleanup_checks.json.

**Cleanup Review State:** Full rubric unavailable; symlink still blocked and
unverified; physical Ctrl+C still unverified. Student report-wording review and
manual-test result are pending. No claim of submission readiness, no application
changes, and no commit, push or submission. Stop after this cleanup.

**Authoritative Rubric Audit Request — 2026-11-19:** The student supplied the
authoritative rubric and requested a final requirement-by-requirement audit of
actual repository files, exact evidence, mandatory/optional distinctions, genuine
review/correction examples, final inventory and unresolved-item relevance. They
explicitly permitted factual documentation/link/inventory corrections, required
valid unchanged-source verification to be reused, prohibited retrospective human
checklist claims, and required proposed necessary code changes to stop for review
before implementation. No commit, push, publication or submission was authorized.
The exact request is preserved in docs/authoritative_audit_request.md with its
attachment hash in docs/verification/final_rubric_source_review.json.

**Actual Checklist Review Today:** Prior Stage 7 findings/tests demonstrated real
review but did not prove an item-by-item application of the supplied checklist.
Codex read active production/tests/helper code and applied all 99 checkbox prompts
now, dated 2026-11-19. The record covers 34 code/configuration/template/sample
files, 208 normally parsed functions and 14 separately parsed executable bootstrap
functions. The original checklist remains unchanged. The initial mapping recorded
67 PASS, 16 PARTIAL, 14 N/A and two pending actions before the further style/F3
probes, including optional limitations and the
user-prohibited commit step. These are review prompts, not 99 mandatory rubric
requirements. No student all-line review was invented.

**Confirmed Mandatory Gaps:** Eight functions inside tests/cli_helpers.py's
_BOOTSTRAP lack docstrings: controlled_input, fail_history, fail_read, denied_read,
denied_identity, denied_home, interrupted_export and interrupted_summary. Exact
repository lines and AST reproduction results are saved. All 208 outer functions
are documented; the earlier outer-only AST checks explicitly excluded embedded
strings. A new focused flake8 check of the extracted executable string returned
exit 1 with eight E301/E302/E305 blank-line errors. Saved file-level checks were
genuine, but did not cover that string's executable contents. This is a real
expanded-scope lint failure, not a runtime failure or a fabricated regression.

Smallest proposed correction is docstrings and required formatting in that same
test bootstrap, followed by affected CLI/bootstrap and quality checks, including
the extracted-script check. No assertions/quality rules need weakening and no
functional change is proposed. No Python/test source was edited; correction
awaits approval under the user's review boundary.

**Evidence Reuse and Inspection:** Read actual models, loader, engine, strategies,
history, paths, CLI, terminal, export, all tests and PowerShell helper; inspected
the supplied design guide's Strategy section and real Protocol implementation.
Current application/tests/tool configurations/dependencies match the 31 protected
hashes and both saved clean copies. Both native runtime evidence sets show 271
passed/one OS-dependent symlink skip, not merely grammar checks. Coverage remains
590/599 statements, 120/124 branch outcomes and combined 710/723. No full suite
was repeated for doc-only changes. Confirmed F1/F2 records: original red four
failed/two passed; expanded red five/five; permanent-pipe red two/seven; final
focused green 12 passed. Initial collection/mock/setup errors remain labeled as
such rather than reused as product-defect proof.

**Documentation and Audit Corrections:** Replaced remaining inherited root README
stubs with an actual landing page; updated project/application READMEs, environment
link and current report facts. Added dated rubric/length resolutions to historical
plan/audit snapshots instead of rewriting their earlier findings. The supplied
rubric now confirms the authoritative 1,000-1,500 limit; the official template and
its superseded footer are preserved. Strategy's real purpose and guide membership
are explicit. The report labels its technical future-feature possibility as not
a student wish list. First-person supplied reflections and all rating lines remain
unchanged, and final wording is not approved. The factual report is now 1,328
rendered words / 1,375 raw Markdown whitespace tokens. An initial documentation
patch attempted duplicate operations on the same path and was rejected before
execution; the corrected Update patch succeeded without an application change.

**Initial Mandatory/Optional Result, Before F3:** The 39 literal mandatory bullets (including repeated
submission-checklist items) map to 36 PASS, one PARTIAL and two FAIL. Missing
bootstrap docstrings cause the partial documentation criterion; the same confirmed
spacing issue affects PEP 8 and all-lint verification, explaining the two failed
criteria without inventing separate application bugs. Persistent adaptive learning,
seeded replay and optional JSON session export are three distinct implemented
non-CRUD capabilities, each verified through main.py. IDs, atomic writes and
overwrite/path protections are supporting details, not extra feature counts.
No optional pattern, API, dependency, optimization or logging feature was added.

**Readiness and Stop:** The full rubric and report-length decision are resolved.
Physical Ctrl+C and actual symlink behavior remain UNVERIFIED; they are not explicit
rubric requirements and are not automatically failed mandatory tests. The manual
result and final report approval remain the user's separate readiness gates.
The code-documentation/style corrections are mandatory and await review. Current
inventory, required evidence accessibility, links and exclusions are recorded in
the final audit checks. No claim of submission readiness, no active code edits,
and no commit, push, publication or submission. Stop for the user's review.

**Additional Confirmed Finding F3 and Final Audit State — 2026-11-19:** The actual
review identified another narrow failure path in utils/cli.py:233-236. Injecting
KeyboardInterrupt before the quiz returns 130 when warning output succeeds.
Routing the real warning printer through a native pipe with its reader closed
returns 1 instead: the restored-diagnostic case shows a TerminalOutputError
traceback; the permanently broken-pipe case also returns 1. These are injected
exception/native-I/O probes, not physical Ctrl+C. Actual bootstraps, interpreter
version and outputs are saved in
docs/verification/final_startup_interrupt_reproduction.json.

An exception raised inside the KeyboardInterrupt handler is not caught by its
sibling except clause. The smallest proposed correction is to catch only
TerminalOutputError around that warning and retain return 130. Proposed regressions
cover healthy, restored and permanently failed warnings, preserving unexpected
programming errors and asserting no pre-quiz persistence side effects. No answers
were completed in this reproduction, so no history-loss claim is made. No fix or
test-source edit was implemented: the user's explicit audit boundary requires
review before necessary application changes.

The final current matrix is **34 PASS, two PARTIAL and three FAIL** across 39
mandatory bullets. CQ1/SUB6 fail for the eight extracted-bootstrap spacing errors;
CQ4 is partial for its eight missing docstrings; CQ2 fails and APP1 is partial for
F3. The final provided-checklist mapping is **59 PASS, 24 PARTIAL, 14 N/A and two
pending actions** across 99 prompts, reflecting these additional findings. The
report's factual finding update brings it to **1,335 rendered words / 1,382 raw
Markdown whitespace tokens**, including headings, lists, appendices and footer.
Its supplied personal reflections and four ratings remain unchanged.

The current final audit, matrix, inventory and integrity results supersede the
initial counts above without deleting that audit progression. The unchanged-source
clean suites remain valid evidence, while the new probes show behavior those suites
did not cover. The mandatory gaps and user's report/manual-result readiness gates
remain open; actual symlink behavior remains unverified rather than an automatic
rubric failure. Final integrity checks mapped all 39 supplied bullets exactly,
verified 136 eligible inventory files and 102 resolving relative file links,
and found all 26 evidence filenames referenced by the report/log in that inventory.
No forbidden local-artifact path or recognizable credential was detected by the
bounded scan. All protected source hashes still match; git diff --check returned
0 (with only Git's existing LF-to-CRLF notice). Actual check output is saved in
docs/verification/final_rubric_audit_checks.json. An initial transient command for
recording these results failed to parse after PowerShell removed argument quotes;
it changed no files. Piping the literal recording script corrected that tooling
error, and every candidate JSON file then parsed successfully. No optional work, source change,
commit, push, publication, submission or readiness claim was made.

**User Approval and Correction Request — 2026-11-19:** The student approved F3 and
the eight bootstrap spacing/docstring corrections, required healthy/restored-pipe/
permanently broken warning regressions before production edits, narrow handling
with programming errors visible, full tests/quality checks on both 3.10.11 and
3.13.17, updated coverage/audit/inventory/report/log, unchanged personal text, and
a stop for review. Physical Ctrl+C and report wording remain pending. No commit,
push, publication or submission was authorized.

**Regression Evidence Before Production Change:** Added three parametrized
startup-interruption cases and a separate RuntimeError visibility control in
tests/test_finalization.py, with two documented bootstrap fault hooks. Both
Python versions returned **two failed/two passed**: healthy output and the
programming-error control passed; restored/permanently broken native warning
pipes returned 1 rather than 130. Complete outputs are f3_red_310.json and
f3_red_313.json under docs/verification. f3_manifest.json retains original/red/
final source and proves utils/cli.py was byte-identical through the red phase.
These are injected KeyboardInterrupt/native-pipe results, not physical Ctrl+C.

**Approved Small Corrections:** Wrapped only terminal.warn inside the top-level
KeyboardInterrupt handler with except terminal.TerminalOutputError, then return
130. RuntimeError remains visible. Added the original eight embedded helper
docstrings and required spacing; all 16 embedded functions now have docstrings.
Normal file-level checks are supplemented with extracted-bootstrap flake8 using
the existing configuration. Only utils/cli.py, tests/cli_helpers.py and
tests/test_finalization.py changed among 31 protected source/config/dependency/
template/sample files. Dependencies, rules, exclusions and existing assertions
were not weakened. Engine/history/export code did not change.

**Actual Complete Post-Fix Checks:** Existing isolated Windows environments ran
against current source, not another clean install. Both Python 3.10.11 and
3.13.17 passed **four focused F3 cases** and **275 full tests/one symlink skip**
(22.56s and 22.99s respectively). Black/isort/flake8/strict mypy/pip check and
extracted-bootstrap flake8 all returned 0 on both. Saved f3_green_310.json and
f3_green_313.json contain actual commands/runtime paths/cwd/output; raw
f3_coverage_310.json and f3_coverage_313.json show **593/602 statements (98.50%),
120/124 branch outcomes (96.77%), combined 713/726 (98.21%)** over all 11 production
modules including main.py. The same symlink test skips with WinError 1314; hard
links and keyboard injection remain separate evidence. Prior F1/F2 and F3 red
evidence are retained rather than relabeled as passing.

**Documentation and Review State:** Updated current root/application READMEs,
checklist follow-up, rubric matrix/audit, concrete inventory and factual report
metrics; preserved the initial audit in f3_before_audit.json and initial integrity
record in f3_before_audit_checks.json. The report is **1,346 rendered words / 1,393
raw Markdown whitespace tokens**, including headings/lists/appendices/footer;
all supplied reflection paragraphs and four rating lines remain unchanged.
The original template remains byte-identical. Current mandatory matrix: **39
PASS**, with no confirmed mandatory gap in inspected scope; this is Codex's audit,
not student acceptance of the corrections or complete correctness on all inputs.
Physical Ctrl+C, actual symlink behavior and report wording remain unverified or
pending; physical result/report approval are still the student's readiness gates.
Final integrity checks verified **146 eligible files, 115 resolving relative file
links and 35 accessible report/log evidence filenames**. All candidate JSON files
parse; no recognizable credentials or forbidden local artifacts were detected by
the bounded scan. The same 168 ignore probes remain valid against unchanged rules;
git diff --check returns 0. Existing finalization test functions are AST-identical,
and protected hash checks confirm unchanged rules/dependencies/exclusions/template.
Results are saved in docs/verification/final_rubric_audit_checks.json. No optional
feature, dependency or performance work was added. Stop for review;
no commit, push, publication, submission or readiness claim.

**User Acceptance and Factual Documentation Update — 2026-11-19:** The student
accepted F3/bootstrap corrections based on reported regression evidence and
requested correction of stale self-assessment reasons and the SUB1 sentence.
Updated Test Quality reasons to acknowledge verified Windows Python 3.10.11 and
3.13.17 runtimes while keeping physical Ctrl+C/actual symlinks unverified. Updated
Documentation reasons to acknowledge completed clean reproduction and authoritative
rubric audit while keeping report approval/manual result pending. All four ratings
remain 4/5; supplied reflection paragraphs and original historical log entries,
including original Stage 8 reasons, are unchanged. No new student opinion is added.

Removed the stale claim that CQ4 remains a content-quality gap from the current
SUB1 evidence in both Markdown and JSON; verified bootstrap docstrings satisfy it.
Current acceptance markers now reflect this actual user acceptance, without
approving final report wording. Documentation checks recount the report at
**1,379 rendered words / 1,426 raw Markdown whitespace tokens**, including
headings/lists/appendices/footer. Current matrix remains 39 PASS. Source/test/
configuration/dependency/template hashes still match the tested F3 manifest;
the earlier dual-runtime tests and coverage were reused, not rerun. Relative links,
evidence accessibility, inventory, JSON and whitespace checks are recorded in
docs/verification/final_documentation_checks.json. Stop after this documentation
cleanup. Final report approval and physical Ctrl+C remain pending; symlinks remain
privilege-blocked. No application changes, commit, push, publication or submission.

**Final Report Approval and Name Masking — 2026-11-19:** The student explicitly
approved the final report and requested initials with every remaining name letter
replaced by an asterisk. Applied `A***** P*****` to the report and all seven eligible
documentation/evidence files containing the full name. Historical decisions,
test outcomes and ratings are preserved; only the personal-name text in historical
entries/snapshots is redacted at the student's request. This documented privacy
redaction supersedes earlier claims of byte-identical personal-name text; no source,
test, configuration, dependency or template file changed.

Updated current README/audit/approval metadata to record actual wording approval.
The report contains **1,381 rendered words / 1,428 raw Markdown whitespace
tokens**, including headings/lists/appendices/footer. Ratings remain four 4/5.
Documentation/link/JSON and tested-source hash checks are saved in
docs/verification/final_report_approval.json. No full tests were rerun for these
documentation-only changes. Physical Ctrl+C remains unobserved; actual symlinks
remain privilege-blocked and unverified. Report approval is not submission
authorization. No commit, push, publication or submission.

**Lessons Learned:** Audit observation: fresh interpreter execution is stronger
evidence than static compatibility checks; clean venvs are distinct from clean
machines, and ignored on-disk artifacts are distinct from candidate files.
No new student reflection or independent human verification is invented.

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

At the end of your project, fill out these statistics:

- **Recorded detailed stage entries:** 9 (grouped follow-ups; not a count of chat turns)
- **Lines of AI-generated code used:** Not tracked line by line; physical source size is reported separately.
- **Lines of AI-generated code modified:** Not reliably measurable from the available uncommitted history.
- **Most helpful AI interaction:** The student described valuable reviews but did not rank one interaction.
- **Most challenging AI interaction:** No individual interaction was ranked by the student.
- **Student-reported lessons:** Annotations do not validate JSON; Protocols resemble structural interfaces; high coverage does not guarantee correct failure behavior.

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.
