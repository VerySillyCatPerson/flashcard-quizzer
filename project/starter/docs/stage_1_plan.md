# Stage 1: inspection and proposed design

**Dated resolution — 2026-11-19:** The student has supplied the authoritative
rubric; the 1,000-1,500-word limit is authoritative. The planning uncertainties
below are preserved as historical observations. Current criterion evidence and
remaining gaps are recorded in [the final audit](final_rubric_audit.md).

Date: 2026-11-18. Status: **Stage 1 decisions accepted; Stage 2 authorized**.
Stage 1 changed no application functionality, dependencies, or quality configuration.

## Workspace and source evidence

- Requested workspace: `C:/Projects/flashcard`; initially empty, with no Git repository.
- Source: https://github.com/udacity/cd14602-project-starter
- Inspected commit: `808893c4f8639804ab81a031dbd2bc3672d308ba`.
- Application working directory: `C:/Projects/flashcard/project/starter`.
- The clone contains unrelated course lessons with Windows-incompatible
  `:Zone.Identifier` filenames. Checkout initially failed. A sparse checkout
  now includes `project/` and root files; the original commit and history remain.
  The incompatible lessons are excluded, and the project structure is preserved.
- No `AGENTS.md` was found at `C:/`, `C:/Projects/`, or in this repository.
  The supplied NCU instructions concern a different project. Reviewed this
  starter's `.claude/CLAUDE.md`, AI guidance, and design pattern guide for context.

### Actual starter inventory

| Existing path | Observed contents | Proposed changes |
| --- | --- | --- |
| `main.py` | Module docstring only | Thin import/exit wrapper, Stage 6 |
| `utils/__init__.py` | Package docstring only | Preserve package; add modules below |
| `tests/__init__.py` | Package docstring only; no tests | Focused pytest suite, Stages 3-6 |
| `data/glossary.json` | Bare array, 10 front/back cards | Preserve as sample and compatibility fixture |
| `data/python_basics.json` | Object containing `cards`, 8 cards | Preserve; loader must support this shape too |
| `requirements.txt` | Testing, quality, documentation, security, optional runtime tools | Review/minimize and resolve compatible versions in Stage 2 |
| `README.md` | Flashcard instructions and verification commands | Rewrite for actual application in Stage 8 |
| `docs/report_template.md` | Official report outline with placeholders | Preserve; draft a separate `docs/final_report.md` in Stage 8 |
| `docs/ai_edit_log.md` | Instructions, labeled fictional example, blank entries | Record real interactions throughout; remove example before submission |
| `docs/design_patterns.md` | Strategy/Factory guidance plus generic examples | Reference, no changes needed now |
| `.editorconfig` | Four spaces; Python line length 88 | Align quality configuration in Stage 2 |
| `.gitignore` | Ignores `venv/`, caches, coverage output; lacks `.venv/` and quiz state | Extend in Stage 2, before generating local artifacts |
| `.claude/`, `ai_guidance/` | Agent context and review/prompt guides | Preserve |

### Missing or conflicting instructions

The project README explicitly delegates the full specification and rubric to
Udacity's classroom Instructions page. Those documents are absent here; the
user's pasted requirements are the current working specification. Classroom-only
criteria cannot yet be independently audited.

The starter README and user request require a 1,000-1,500-word report; the report
template footer instead says 2,000-3,000. The user explicitly confirmed the
classroom's **1,000-1,500-word limit** in the Stage 1 review. Follow that limit,
retain the template headings, and keep this conflict note. The full classroom
text has not yet been supplied or independently inspected.

The generic rubric's "three new features beyond CRUD" wording is supplied by
the user, not independently verified. This starter has no CRUD application.
The user selected persistent adaptive history, seeded randomness, and optional
JSON results export as the **proposed additions**. Check their sufficiency against
the full rubric once provided. Detailed behavior was settled through the recorded
Stage 1 reviews; Stage 2 authorizes environment setup only, before implementation.
Do not add deck editing or a database.

## Architecture and requirement mapping

All new production modules stay inside the starter's `utils/` package.

| Proposed file | Owns | Main evidence to add |
| --- | --- | --- |
| `utils/models.py` | Immutable typed card, answer result, session summary | Valid data, computed statistics, zero answers |
| `utils/data_loader.py` | File reading, both JSON shapes, field validation, contextual load errors | Missing/unreadable file, encoding/JSON errors, every invalid field/shape |
| `utils/strategies.py` | Strategy interface; sequential, random, adaptive algorithms; simple mode factory | Order, membership, no deck mutation, stable ties, finite output |
| `utils/engine.py` | Pure answer evaluation and finite session state with no terminal I/O or callbacks | Matching, returned feedback data, counts, partial state without scoring unfinished input |
| `utils/history.py` | History schema, identity, load/save and persistence errors | Across-session priority, portable identity, corrupt/unwritable state |
| `utils/terminal.py` | Prompts, feedback, plain-text summary table | Correct/Incorrect, accuracy and missed terms, partial summary |
| `utils/cli.py` | `argparse`, wiring, error boundaries, exit status | Subprocess tests through actual `main.py` |
| `utils/paths.py` | Preflight validation that deck/history/requested export identify distinct files | Resolved relative paths, symlinks and hard links where supported, absent outputs, helpful conflict errors |
| `utils/results_export.py` | Optional versioned JSON export, if agreed | Completed/partial sessions, invalid output path |
| `main.py` | Call CLI and propagate its integer exit status | Entry-point help, mode/file flags, error codes |

Data flow: CLI arguments -> loader -> validated cards -> strategy orders a copy
-> terminal obtains an answer -> engine evaluates/records and returns results
-> terminal feedback/summary -> history and optional export. File operations
remain outside selection algorithms. Domain code returns typed results; the CLI
handles expected failures without a traceback. The Stage 4 instruction supersedes
the original injected-I/O sketch: engine state exposes `current_card`,
`submit_answer`, and immutable summary snapshots, without I/O callbacks.

Proposed Strategy contract (design sketch only):

```python
class QuizStrategy(Protocol):
    def order(self, cards: Sequence[Flashcard]) -> list[Flashcard]: ...
```

`SequentialStrategy` copies deck order. `RandomStrategy` receives a
`random.Random` instance and shuffles a copy. `AdaptiveStrategy` receives a
snapshot of priority scores and sorts a copy. The engine only calls `order`;
adding a strategy requires registering it in the CLI factory, not rewriting
the engine. Each returns every input card exactly once. A factory function is
sufficient; no extra Factory class is needed.

### Python concepts for a TypeScript engineer

- A `Protocol` resembles a structural TS interface: matching methods satisfy
  the contract without explicit inheritance. An abstract base class is an
  alternative if runtime enforcement is preferred. Recommend `Protocol` for
  this small injectable contract.
- A frozen `dataclass` generates initialization and value comparison for a
  record, roughly like a readonly TS data model. It does not validate raw JSON;
  the loader must check runtime values before constructing it.
- `Sequence[Flashcard]` accepts ordered input without granting list mutation
  in the interface. `list[Flashcard]` is a new, concrete output list.
- Type hints are checked by mypy, not enforced by the Python runtime. Treat
  decoded JSON like TS `unknown`, narrowing its shape before use.
- Use `with` for file lifetime management and specific exceptions for expected
  failures. Keep terminal input/output outside the engine, advancing state only
  with completed submissions. Avoid a broad `except Exception` that hides defects.
- Keep the entry point under `if __name__ == "__main__"` so importing modules
  during tests does not start a quiz.

## Agreed behavior and proposals for review

The user's first review explicitly accepts outer-whitespace trimming,
case-insensitive answer comparison, empty answers counting as incorrect, partial
statistics excluding unfinished answers, and finite sessions asking each card
once. These rules are settled. Details below are labeled where still proposed.

### JSON contract and matching

Accept both existing shapes unchanged:

```json
[{"front": "API", "back": "Application Programming Interface"}]
```

```json
{"cards": [{"front": "Which keyword defines a function?", "back": "def"}]}
```

Require a nonempty card list; each card must be an object containing nonempty
string `front` and `back` values after trimming outer whitespace. Reject null,
numbers, arrays as cards, missing fields, wrong types, empty strings, and duplicate
JSON object keys. Duplicate JSON keys within one object (for example, two `back`
keys) are distinct from repeated cards in the list.

**Accepted after review:** Repeated fronts are allowed when backs differ.
Reject identical normalized `(front, back)` pairs, with a clear message naming
both one-based card positions, such as `Cards 2 and 5 have identical front/back
content after normalization`. Normalize both strings with `strip().casefold()`.
Do not silently remove duplicates. Arbitrary ignored metadata does not distinguish
cards. Additional metadata remains allowed but ignored under the proposed loader
rules; it does not affect identity or scoring.

The original front-only uniqueness proposal was rejected. The follow-up optional
`context` field was also rejected: do not introduce a context field, model member,
identity component, or display feature. Both starter formats remain compatible.

For example, front `bank` / back `financial institution` and front `bank` / back
`river edge` are distinct valid cards. Each card expects its own back, not any
answer associated with that front. After an incorrect response, display
`Incorrect` and that card's expected answer. This accepted feedback rule helps
explain ambiguous repeated-front cards, although it cannot disambiguate the
prompt in advance. Repeating the same normalized front/back pair is an error.

Decode UTF-8 (accept an initial BOM), preserve user-facing capitalization, and
compare `answer.strip().casefold()` with `back.strip().casefold()`. `casefold`
handles Unicode case matching more fully than lowercasing; it does not provide
fuzzy matching or normalize accents/internal spaces. Empty answers count as
incorrect attempts, keeping the session finite without a retry loop.

Examples: `" DEF "` matches `"def"`; `"application  programming interface"`
does not match the glossary answer with single internal spaces. A blank `back`
should produce a message such as `Card 3: 'back' must be a non-empty string`.

### Portable history identity: accepted

The user requires moves and renames to preserve learning history. The initial
absolute-path deck namespace is **rejected and superseded**.

Use a shared, per-card history map with **no deck namespace**, as accepted:

1. Normalize front and back using `strip().casefold()`.
2. Serialize the two strings as an unambiguous JSON array using fixed encoding
   settings; compute a SHA-256 digest with a version prefix such as `card-v1:`.
3. Use that deterministic key to look up the card's priority score in the existing
   separate history file. Do not use Python's process-dependent `hash()`.

This requires no registry, UUID assignment, sidecar files, database, or changes
to either starter deck. SHA-256 is standard-library functionality. Paths,
deck filenames, array positions, JSON indentation, and wrapper shape do not
participate in identity.

| Deck/card change | Accepted history behavior |
| --- | --- |
| Move or rename deck | All card scores preserved, using the same history file |
| Reorder cards | Scores preserved; new deck order determines tied priorities |
| Add card | Existing scores preserved; new content starts at zero |
| Edit front or back meaningfully | Edited card starts at zero; unchanged cards retain scores |
| Change only outer whitespace or case | Scores preserved under normalization |
| Change ignored metadata | Scores preserved |
| Remove card | Retain dormant score; do not ask removed card |
| Restore previously seen content | Resume its prior score |
| Copy card into another deck | Share the same score intentionally |

The user explicitly accepted shared learning state across decks containing
identical normalized front/back content. There is no independent deck learning
profile. Moving to another computer
still requires copying the history file; this is portable identity, not cloud
sync. If that sharing is unwanted, the smallest alternative is an explicit
stable `deck_id` in the object wrapper plus content-based card keys. That isolates
decks, but requires assigning and maintaining IDs and a migration decision for
plain-array decks. Hashing the entire deck is unsuitable: adding/editing one card
would change the deck hash and lose lookup of unchanged cards.

A meaningful edit starts fresh rather than guessing whether prior mastery still
applies. Explicit stable card IDs could preserve state through edits, but would
require more schema and editing rules. Content keys are the accepted choice.

### Adaptive scoring: accepted error balance, with comparison retained

Both policies ask each card exactly once, sort by descending score, and preserve
deck order for ties. The user accepted fixing adaptive order at session start
and updating history from completed answers in every mode; unfinished input
produces no update. Each card is asked once per session.

| Policy | Incorrect answer | Correct answer | Tradeoff |
| --- | --- | --- | --- |
| Original cumulative mistakes | `score + 1` | Score unchanged | Records lifetime errors; old difficulty remains prioritized after mastery |
| Accepted error balance | `score + 1` | `max(0, score - 1)` | Responds to successful practice with one nonnegative integer per card |

Example: deck order `[A, B]`, initial scores `(0, 0)`. The table shows scores
**after** each completed session and resulting order for the **next** session.
Outcomes refer to card labels regardless of which order that policy asked them.

| Session | A answer | B answer | Cumulative scores; next order | Error-balance scores; next order |
| --- | --- | --- | --- | --- |
| 1 | Incorrect | Correct | `(1, 0)`; A, B | `(1, 0)`; A, B |
| 2 | Incorrect | Correct | `(2, 0)`; A, B | `(2, 0)`; A, B |
| 3 | Correct | Incorrect | `(2, 1)`; A, B | `(1, 1)`; A, B |
| 4 | Correct | Incorrect | `(2, 2)`; A, B | `(0, 2)`; B, A |
| 5 | Correct | Correct | `(2, 2)`; A, B | `(0, 1)`; B, A |

After session 4, A has recovered under error balance and B goes first.
Cumulative scores tie and keep A first because of deck order. Another correct
answer by B reduces its balance to zero; correct answers at zero stay at zero.

Use accepted error balance (`+1` / `-1`, floor zero), with no cap or time-based decay.
It is a priority heuristic, not a mastery probability or spaced repetition.
Many accumulated mistakes still require many correct answers to recover; ties
fall back to deck order; new zero-score cards may follow difficult cards, but all
are still asked in the finite session. Store a history schema/policy version so
future policy changes cannot silently reinterpret old scores. There is no actual
prior history to migrate yet. Cumulative mistakes are retained above solely to
document the comparison that informed the user's decision.

### Preflight path validation: accepted refinement

Before starting the quiz or writing any output, require deck, history (including
its default path), and requested export to identify distinct files. Resolve
relative paths, `..`, and existing symlinks with `Path.resolve()`; compare resolved
paths with platform-appropriate case semantics. Where both paths exist, also
use `Path.samefile()` to catch existing-file aliases such as hard links where
supported. Do not rely on argument-string equality alone. Check all three pairs.
Reject detected conflicts with a helpful message naming both roles and paths
(for example, `Deck and export refer to the same file; choose a different export
path`) and exit 2 as an invalid argument combination, without starting a session
or touching those files. Report unexpected path-resolution/identity inspection
I/O errors helpfully with status 1 rather than silently declaring paths safe.
Nonexistent output files can still conflict through their resolved destination.
These checks are a preflight safeguard, not a concurrent-filesystem locking scheme.

### Persistence and failure behavior: accepted

- Default history: versioned JSON in `Path.home() / ".flashcard_quizzer" /
  "history.json"`, separate from decks and the repository. A `--history` override
  allows isolated tests or profiles. No state file is created in Stage 1.

The user explicitly accepted the summarized failure rules and statuses, then
required the warning and persistence-limit refinements below.

| Condition | Accepted behavior | Status after otherwise completed quiz |
| --- | --- | --- |
| History file absent | Start scores at zero; create history when saving completed answers | 0 if saving succeeds |
| Corrupt JSON, invalid history values, or unsupported version | Warn; use zero scores for this run; disable saving to that history path and leave it untouched | 1 |
| Existing history unreadable | Warn; use zero scores for this run; disable saving to that history path and leave it untouched | 1 |
| History cannot be saved, including parent-directory creation failure | Keep quiz feedback and summary; report that updates were not saved; preserve any previous valid history | 1 |

History trouble does not prevent practicing the deck. Adaptive mode falls back
to deck order when no history scores can be loaded. Even if answers are completed
successfully, status 1 makes a history failure visible to scripts. Do not silently
overwrite corrupt/unreadable/unsupported state or imply learning updates persisted.
When existing history cannot be loaded, explicitly state all three effects:
`Previous scores could not be loaded. Adaptive mode will use deck order.
Learning updates will not be saved during this run.` Include the actual cause
and affected path, and preserve the problematic file. Normal missing-history
initialization is not a load failure and does not disable saving.

Validate nested types and nonnegative integer scores, explicitly excluding
booleans. Save updates from completed answers once at session end, including
EOF/Ctrl+C, when history is usable. Use a temporary sibling file and atomic
replacement to avoid partially overwriting valid history. Attempt requested
results export independently even if history fails; export failure does not
suppress the terminal summary or an otherwise possible history save. Saving
occurs only at session end or orderly interruption: forced process termination
may lose that session's updates. Atomic replacement protects against partial
writes; it does not resolve concurrent-session conflicts (one session can
overwrite another session's updates). Document both limits. Never save an
unfinished answer.

### Summary, interruption, and exit status

The table shows deck size, total answered, correct count, accuracy percentage,
and missed fronts. Completed sessions answer the whole deck. Interrupted sessions
show a clear partial label; accuracy uses answered cards only. An input interrupted
before submission is unanswered, not missed (accepted by the user). Recommend
labeling missed cards with original one-based list position and front, so repeated
fronts remain distinguishable. With zero answers show `N/A` accuracy
and an empty missed list; do not divide by zero or call it 0% performance.

Accepted exit statuses (path-conflict classification is a Stage 2 design detail):

| Status | Meaning |
| --- | --- |
| 0 | Help, or completed quiz with successful required persistence and requested export; wrong answers do not make the command fail |
| 1 | Missing/unreadable/malformed/invalid deck; degraded history loading or failed history save; failed requested export; or EOF before all answers are completed |
| 2 | Invalid CLI arguments, such as an unknown mode, missing required file flag, or conflicting deck/history/export paths |
| 130 | Ctrl+C interruption, including when saving or export also reports a failure |

EOF/Ctrl+C during a session print a clearly partial summary, save completed answers
when possible, and attempt requested partial results export. Unasked/unfinished
cards do not affect accuracy, misses, or history. For zero completed answers,
use accepted accuracy `N/A`, answered count zero, and no missed cards. A failure
before the quiz starts produces a helpful error without a fabricated quiz summary.
Expected errors and warnings go to stderr without tracebacks; prompts, feedback,
and table go to stdout. Unexpected defects remain distinguishable during
development rather than being swallowed. These failure/status and zero-answer
rules are explicitly accepted in the final Stage 1 review.

## Dependencies and later verification

Recommend standard-library runtime modules: `argparse`, `dataclasses`, `json`,
`pathlib`, `random`, `hashlib`, `typing`, `tempfile`, and `os`. No runtime package
is needed for loading, validation, a summary table, or Strategy selection.

The starter already declares pytest/pytest-cov, Black, flake8, isort, mypy,
Sphinx/themes, pre-commit, bandit, safety, requests, click, and pydantic. The last
three are labeled optional but still installed by the current requirements file.
Recommend retaining only the required test/quality tools (including isort to
match the starter guidance) and pinning versions actually verified with the
selected interpreter in Stage 2. This dependency change is still a proposal.

Use a local `.venv` with standard pip. The Claude note about no venv refers to
the hosted course workspace; this is Windows, and the user's venv requirement
and starter's local setup guidance apply.

In Stage 2 align Black/isort at 88 columns and flake8's line length/Black-related
spacing compatibility; enable strict mypy over application and tests. Explain
any narrow style exceptions; do not suppress correctness checks. Coverage must
include `main.py` and all production modules, exclude only tests/environments,
and enforce an unrounded total strictly above 80% (for example, a gate of 81%).
Use subprocess integration coverage for the real entry point as well.

Proposed verification commands from `project/starter`, after setup:

```text
python main.py --help
python main.py --mode sequential --file data/glossary.json
python main.py -m adaptive -f data/python_basics.json
python -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json --cov-fail-under=81
python -m black --check .
python -m isort --check-only .
python -m flake8 .
python -m mypy .
```

These commands were **not run**. There is no implemented CLI or test suite yet.
Archive actual check output and a coverage summary under `docs/verification/`
in Stage 8; repeat installation/checks in a separate clean environment in Stage 9.
Do not report compatibility with an interpreter that has not been tested.

## Executed inspection and results

- `Get-ChildItem -Force` and ancestor instruction checks: empty target; no
  applicable ancestor `AGENTS.md` found. `git status --short` initially confirmed
  the folder was not a repository.
- Opened the supplied GitHub URL through web browsing; cloned that same source.
  Initial network attempt failed; elevated network attempt downloaded the repo
  but checkout failed on an unrelated lesson filename.
- `git sparse-checkout set --cone project`: initial sandbox attempt could not
  write Git config; elevated retry succeeded, but files were still absent.
- `git read-tree -mu HEAD`: failed on the incompatible index path.
  `git -c core.protectNTFS=false read-tree -mu HEAD` then populated the sparse
  worktree successfully. The override was command-scoped, not a global setting.
- `git rev-parse HEAD`, `git ls-tree`/`git ls-files`, `rg --files --hidden`, and
  `Get-Content`: inspected source identity, tracked paths, code, requirements,
  README, template, log, pattern guide, and agent/review guidance.
- `ConvertFrom-Json` on both sample files: parsed successfully; counts 10 and 8.
  This is sample syntax inspection, not application validation.
- `git diff --exit-code HEAD -- project`: exit 0 before documentation edits.
  `git status --short`: no changes before documentation edits; sandbox emitted
  a nonfatal warning accessing the user's global ignore file.
- `python --version`: command could not run. `py --list`: launcher not found.
  `Get-Command python,python3,py`: python/python3 resolve to WindowsApps aliases;
  no usable interpreter version has been established. Investigate in Stage 2
  before installing anything. No Python compatibility or test result is claimed.
- After documentation edits, `git diff --check` passed. A targeted
  `git diff --exit-code HEAD --` over `main.py`, `utils/`, `tests/`, `data/`,
  `docs/report_template.md`, and `requirements.txt` exited 0, confirming those
  starter files are unchanged. `git status --short` showed only the modified
  AI log and new plan. `Test-Path` confirmed the plan exists; `Select-String`
  confirmed the documents explicitly mark pending review and unrun checks.
- First-review follow-up: reread both documents with `Get-Content`; after the
  revisions, `git diff --check` and the same targeted starter-file comparison
  passed (exit 0). `git status --short` still showed only the two documentation
  files; `rg -n` confirmed revised sections, report limit, and pending decisions.
  A PowerShell arithmetic check replayed all five sessions, asserted every
  cumulative/error-balance score pair against the documented table, and checked
  the zero floor; all passed. This verifies the example, not Python functionality.
  Application/quality checks were not run; Stage 2 has not started.

## Recorded reviews and remaining decisions

Accepted: trimming, case-insensitive comparison, empty answers as incorrect,
partial statistics excluding unfinished answers, one attempt per card per finite
session, and the 1,000-1,500-word report limit with the template-conflict note.
Persistent adaptive history, seeded randomness, and optional JSON export are the
selected proposed additions, pending a full rubric check when supplied.

The first review rejected path-based identity and front-only duplicate rejection,
and requested the scoring comparison. The second review accepted:

1. Content-based identity with shared history for identical cards across decks;
   preserve the sample array and object-wrapper formats.
2. No `context` field. Allow repeated fronts with different backs; reject only
   identical normalized `(front, back)` pairs, reporting both positions.
3. Show the expected answer after an incorrect response.
4. Error-balance scoring, `+1` after incorrect, `max(0, score - 1)` after correct;
   updates from completed answers in every mode; fixed adaptive order at session
   start, one question per card, and deck-order ties.

Earlier context-based and cumulative-scoring alternatives remain documented in
the AI log and the retained scoring comparison; they are not current requirements.
The final review explicitly accepts failure behavior, zero-answer `N/A`, and exit
statuses. It adds resolved-path/existing-alias conflict checks, an explicit
history-load warning, and session-end/forced-termination/concurrency documentation.
Stage 1 is closed and Stage 2 environment setup is authorized, stopping before
application implementation. Full rubric verification and user reflections remain
pending; acceptance does not imply personal reflections or review of every detail.
