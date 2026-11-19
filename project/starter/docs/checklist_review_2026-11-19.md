# Provided-checklist review: 2026-11-19

**Independent-review follow-up — 2026-11-19:** Reviewed the portable nesting tests
and presentation-only C0/DEL/C1 escaping now, including decoder-only exception
scope, all 65 controls at each card-text display boundary, and unchanged Unicode/
grading/identity/history/export behavior. Both Windows runtimes pass 343 tests/one
symlink skip and all configured/extracted-bootstrap checks. The earlier partial
terminal-control concern is resolved in this scope. Historical findings below
remain dated evidence; the user accepted these corrections on reported evidence. See
[the review and evidence](independent_review_fixes.md).

**Later approved correction, 2026-11-19:** The initial findings/mapping below are
preserved as the actual pre-fix review. The user subsequently approved F3 and the
eight bootstrap docstring/spacing corrections. The changed source and regression
assertions were reviewed now: only TerminalOutputError is caught around the
startup warning; the RuntimeError control remains visible. All 16 embedded
functions have docstrings and extracted flake8 passes on both runtimes. Both full
suites report 275 passed/one symlink skip, with all configured quality checks
passing. See [the fix review](f3_fix_review.md) and
[before/after source hashes](verification/f3_manifest.json). The historical partial
items caused by these defects are resolved; optional limits and manual observations
are not relabeled as verified. This is a Codex follow-up, not student code review.

Reviewer: **Codex**. This is an actual current review, not a retrospective claim that the student checked every line. The earlier Stage 7 review is supported by real findings/tests but did not contain this item-by-item mapping.

Source checklist: [AI-generated code review checklist](../ai_guidance/code_review_checklist.md). All 99 checkbox prompts are mapped below, including N/A cases, optional limits and the prohibited commit action. The source template remains unchanged.

## Scope and method

Read the 11 production Python files, 13 test files (including the executable bootstrap string), manual PowerShell script, tool/dependency configurations and Git-ignore rules. Function-level inventory, file hashes and notes are in [source-review evidence](verification/final_rubric_source_review.json).

Initial read and detailed analysis were performed today. Step 3 uses the saved clean 3.10.11/3.13.17 runs only after matching current source/tests/tool configuration/dependency hashes to both snapshots. No full suite was rerun for documentation changes. Fresh narrow checks separately linted the executable bootstrap and reproduced the newly suspected startup-interrupt/error path. Step 4 is this dated record, the new audit and log append.

## Mandatory code-documentation gap

**PARTIAL:** Eight test-only functions inside tests/cli_helpers.py::_BOOTSTRAP lack their own docstrings: controlled_input (30), fail_history (42), fail_read (48), denied_read (54), denied_identity (62), denied_home (66), interrupted_export (72), interrupted_summary (76). The line numbers are repository lines. All 208 normally parsed functions have docstrings; the embedded string defines 14 additional executable functions, six documented and eight not.

Reproduction: parse tests/cli_helpers.py with ast, literal_eval the _BOOTSTRAP assignment, parse the resulting script, then select FunctionDef nodes for which ast.get_docstring is None. Exact names/lines are saved in the evidence. Earlier AST statistics explicitly excluded embedded strings, so they did not establish this stronger requirement.

Consequence: the broad mandatory docstring criterion is not fully met despite passing lint/tests. Smallest correction: add short single-triple-quoted docstrings to these wrappers inside the outer raw triple-double-quoted string. No behavior change is needed. **No Python/test edit was made; approval and affected CLI/bootstrap checks are pending.**

## Confirmed embedded-script style gap

The newly extracted _BOOTSTRAP was linted with the existing flake8 configuration via stdin (virtual display name tests/cli_helpers_bootstrap.py; no new source file was created). Exit 1 reports eight E301/E302/E305 blank-line violations. Saved file-level lint results remain true but do not cover the string's executable contents. The mandatory PEP 8/all-lint criteria therefore fail in this expanded scope. Smallest correction: document the eight wrappers and add the required formatting in that same test string after approval; no behavior change or rule suppression. See [actual lint output](verification/final_bootstrap_lint.json).

## Confirmed audit F3: startup interruption loses status 130

At utils/cli.py:233-236, terminal.warn runs inside a KeyboardInterrupt handler. If it raises expected TerminalOutputError, the sibling except clause cannot catch an exception raised from that handler. A healthy-warning control returned 130; real closed-pipe warning probes returned 1, with a traceback visible when stderr was restored. This is an injected exception/native-I/O reproduction, not physical Ctrl+C verification. See [saved reproduction](verification/final_startup_interrupt_reproduction.json).

Smallest proposed fix is a narrow TerminalOutputError catch around that warning, followed by unconditional return 130; unexpected programming errors must still propagate. Add healthy/restored/permanent-warning regression cases and verify no pre-quiz history/export side effects. No application/test change has been implemented.

## Evidence used

- Models/loader/engine/strategies: tests/test_models.py, test_data_loader.py, test_engine.py and test_strategies.py; both original formats and no-shuffle-change assumptions inspected.
- History: tests/test_history.py, including real round trips and four failed-save/retry boundaries.
- CLI/exports/paths/terminal: tests/test_cli.py, test_results_export.py, test_paths.py, test_terminal.py and test_finalization.py; helper bootstrap is reviewed as executable code.
- F1/F2: stage_7_fix_red.json, stage_7_fix_expanded_red.json, stage_7_fix_shutdown_red.json and stage_7_fix_checks.json; assertions and before/after code were checked.
- Saved clean runtime/quality evidence: stage_9_checks_310.json and stage_9_checks_313.json; coverage JSON includes all production modules.

## Checklist mapping

### Pre-Review Questions

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 1 / 8 | Do I understand what this code is supposed to do? | PASS | Purpose reviewed: finite JSON flashcard practice; supplied contract and current CLI agree. |
| 2 / 9 | Does it solve the problem I asked for? | PASS | Loader, three modes, grading, summary and three independent additions implement the requested local CLI. |
| 3 / 10 | Is it appropriate for my project's context? | PASS | Standard-library runtime and modular scope fit a learning assignment; optional patterns/APIs are unnecessary. |
### 1. Correctness and Functionality

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 4 / 15 | Does the code implement the correct algorithm? | PASS | Reviewed stable descending error balance (+1/-1 floor zero), permutation checks and one submission per pending card. |
| 5 / 16 | Are all edge cases handled appropriately? | PARTIAL | Tested boundaries pass, but defensive cleanup paths and physical/symlink observations are not all verified; not a claim that every possible edge is covered. |
| 6 / 17 | Does the logic flow make sense? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 7 / 18 | Are there any obvious bugs or logical errors? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 8 / 21 | Are all inputs validated properly? | PASS | JSON roots/cards/fields/duplicates and history schema/policy/score types are validated; argparse validates public flags. |
| 9 / 22 | Are return values correct and consistent? | PASS | Frozen results/summaries, zero-answer None accuracy and explicit exit categories are consistent. |
| 10 / 23 | Does the function handle empty/null inputs gracefully? | PASS | Empty decks/blank fields are rejected; empty answers are wrong; zero-answer summaries are N/A/null. |
| 11 / 24 | Are error conditions properly managed? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 12 / 27 | Can I trace through the code with example inputs? | PASS | Traced three-card two-correct session and two-session adaptive examples against saved native transcripts. |
| 13 / 28 | Have I tested with boundary conditions? | PASS | Reviewed floor zero, repeated fronts, field-boundary identity, malformed/deep/oversized JSON and completed-session rejection tests. |
| 14 / 29 | Does the code behave correctly with unexpected inputs? | PASS | Wrong types and nonstandard constants are rejected; programmer-error propagation has dedicated tests. |
### 2. Code Quality

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 15 / 34 | Is the code easy to understand? | PASS | Small domain modules and explicit CLI composition are readable; finalization/stream recovery are the main documented complexity. |
| 16 / 35 | Are variable names descriptive and meaningful? | PASS | Names describe cards, scores, pending phases and finish reasons; private helpers indicate ownership. |
| 17 / 36 | Is the code structure logical and well-organized? | PASS | Models/loading, engine/strategies, history, terminal, paths/export and CLI are separated. |
| 18 / 37 | Are there appropriate comments where needed? | PASS | Comments explain uncertain commits, shutdown descriptor recovery, serialization boundaries and no-clobber publication. |
| 19 / 40 | Does the code follow Python PEP 8 style guidelines? | PARTIAL | File-level checks pass, but today extracted bootstrap flake8 found eight E301/E302/E305 spacing errors. Mandatory correction awaits approval. |
| 20 / 41 | Are naming conventions consistent with the project? | PASS | snake_case functions, PascalCase types and private helper prefixes are consistent. |
| 21 / 42 | Is indentation and formatting correct? | PARTIAL | Outer formatting passes; eight blank-line violations in executable embedded source are confirmed in final_bootstrap_lint.json. |
| 22 / 43 | Are imports organized properly? | PARTIAL | Outer isort passes; embedded import grouping is outside that saved file-level scope and should be included in the bootstrap formatting correction. |
| 23 / 46 | Are docstrings present and informative? | PARTIAL | All 208 normally parsed functions have docstrings, but 8 of 14 executable functions inside tests/cli_helpers.py _BOOTSTRAP do not. Add their docstrings after approval. |
| 24 / 47 | Are parameter types and return values documented? | PARTIAL | Annotations document signatures; eight bootstrap wrappers lack accompanying function-level descriptions. The supplied checklist review now includes that embedded code. |
| 25 / 48 | Are usage examples provided where helpful? | PASS | README, manual script, source docstrings and actual transcript evidence provide usage examples. |
| 26 / 49 | Are any assumptions or limitations documented? | PASS | Identity sharing, finite fixed order, overwrite policy, partial statistics and persistence/concurrency/interrupt limits are documented. |
### 3. Security Considerations

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 27 / 54 | Are all user inputs validated and sanitized? | PARTIAL | Schemas and numeric/type constraints are strict. Display escapes newline/carriage/tab only, not every ANSI control. Stronger local-deck terminal-control filtering is optional hardening, not an explicit rubric feature. |
| 28 / 55 | Are file paths and names checked for security issues? | PASS | Canonical names and existing aliases are compared before I/O; arbitrary user-selected paths are intentional, not a hosted upload boundary. Preflight is not a lock. |
| 29 / 56 | Are SQL queries parameterized (if applicable)? | N/A | No database or SQL queries exist. |
| 30 / 57 | Are regular expressions safe from ReDoS attacks? | PASS | Only fixed-format fullmatch identity regex and bounded test regexes are used; no production nested-quantifier/user-supplied regex. |
| 31 / 60 | Are sensitive data (passwords, tokens) handled securely? | PASS | Application does not collect credentials; export omits raw answers; candidate scan and ignore exceptions were inspected. This is a bounded scan, not arbitrary-secret certification. |
| 32 / 61 | Are temporary files created with appropriate permissions? | PARTIAL | NamedTemporaryFile provides exclusive staging names and context-managed handles; platform/default parent ACLs are not independently audited. No permission-hardening requirement is invented. |
| 33 / 62 | Is data serialization/deserialization safe? | PASS | Uses JSON, not pickle/eval; strict schemas and explicit unsupported-policy behavior protect history. |
| 34 / 63 | Are there any potential injection vulnerabilities? | PARTIAL | No eval or user-driven shell commands in production. Remaining terminal control characters can affect a local display; optional stronger display policy is not added during this audit. |
| 35 / 66 | Do error messages avoid exposing sensitive information? | PASS | Messages include useful local paths/format details, not deliberately logged tokens or submitted answer text. Expected card backs are intentionally displayed. |
| 36 / 67 | Are exceptions caught and handled appropriately? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 37 / 68 | Are stack traces filtered in production scenarios? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
### 4. Performance and Efficiency

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 38 / 73 | Is the algorithm's time complexity acceptable? | PASS | Adaptive sorting is O(n log n). Repeated immutable snapshots incur cumulative copying; acceptable for this finite local-deck scope without a specified performance SLA. |
| 39 / 74 | Are there any unnecessary nested loops? | PASS | No unnecessary algorithmic nested loops were found; sequential/random and score updates are direct scans. |
| 40 / 75 | Could data structures be optimized? | N/A | Possible counter/hash caching is optional optimization; no data-structure change is required or implemented. |
| 41 / 76 | Are there redundant operations? | PARTIAL | Summary snapshots and content hashes are recomputed in some paths. This is a reviewed optional optimization, not a correctness/rubric failure. |
| 42 / 79 | Are large data structures handled efficiently? | PARTIAL | JSON/decks/history are loaded in memory with no configured size limit; enormous-input resource hardening is outside the agreed scope. |
| 43 / 80 | Are resources properly cleaned up? | PARTIAL | Normal file handles close and failed writes clean staging where possible; interruption/cleanup failure may leave a temp file, an accepted documented limitation. |
| 44 / 81 | Are there potential memory leaks? | PASS | Sessions and RNGs are scoped; no growing global application collection or retained completed-session loop was found. |
| 45 / 82 | Could memory usage be optimized? | N/A | Optimizing snapshot allocation is optional performance work and was not pursued. |
| 46 / 85 | Are file operations handled efficiently? | PASS | Each deck/history is loaded once per run and history/export write once per attempt; writes flush/fsync before publication. |
| 47 / 86 | Are database queries optimized? | N/A | No database queries. |
| 48 / 87 | Are network requests handled appropriately? | N/A | No application network requests; environment package downloads are separate setup evidence. |
| 49 / 88 | Are there unnecessary I/O operations? | PASS | No per-question persistence or network I/O is introduced; only terminal I/O occurs while asking cards. |
### 5. Error Handling and Robustness

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 50 / 93 | Are appropriate exception types used? | PASS | Deck/history/export/terminal exception types convey expected operations without hiding implementation failures. |
| 51 / 94 | Are exceptions caught at the right level? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 52 / 95 | Are error messages helpful and informative? | PASS | Errors identify file/field/card positions or operation and give an overwrite remedy where applicable. |
| 53 / 96 | Is the application state consistent after errors? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 54 / 99 | Are assumptions validated with assertions? | N/A | Runtime preconditions use explicit exceptions rather than optimizable assert statements; tests assert invariants. |
| 55 / 100 | Are preconditions checked? | PASS | Nonempty deck, strategy permutation, history version/policy and public flag/path constraints are checked. |
| 56 / 101 | Are postconditions verified? | PASS | Tests verify membership, counts, unchanged bytes, one-attempt persistence, export shape and immutable snapshots. |
| 57 / 102 | Is the code robust against unexpected inputs? | PASS | Malformed/unreadable files and wrong inputs are covered; no claim is made about unlimited resources or repeated forced interrupts. |
### 6. Integration and Compatibility

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 58 / 107 | Does the code fit well with existing project structure? | PASS | Starter project/starter layout, data samples and original report template are preserved. |
| 59 / 108 | Are dependencies appropriate and necessary? | PASS | Runtime imports are stdlib/local; pinned development requirements installed in both clean venvs. |
| 60 / 109 | Are interfaces consistent with the rest of the codebase? | PASS | QuizStrategy.order and typed model/store APIs have consistent ownership; engine has no terminal/storage dependency. |
| 61 / 110 | Will this code work with existing components? | PARTIAL | Confirmed audit F3: a pre-quiz KeyboardInterrupt followed by warning-output TerminalOutputError escapes main and returns 1 rather than 130. Normal session/finalization paths remain tested; narrow fix awaits approval. |
| 62 / 113 | Does the code maintain existing APIs? | PASS | Both original JSON shapes remain compatible; there was no starter executable API to preserve beyond that contract. |
| 63 / 114 | Are breaking changes documented? | PASS | Reviewed export content/overwrite refinements were requested before acceptance and are documented; raw-answer removal is not concealed. |
| 64 / 115 | Are migration paths provided if needed? | N/A | No released legacy history migration is required; unsupported version/policy is preserved with saving disabled. |
### 7. Testing and Testability

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 65 / 120 | Is the code easily testable? | PASS | Pure engine/scoring/selection and separate adapters permit unit tests without terminal input. |
| 66 / 121 | Are dependencies injectable for mocking? | PASS | Random is injected; filesystem/terminal faults are injected only in tests, with real file observations. |
| 67 / 122 | Are side effects minimized? | PASS | Selection/grading are side-effect free; I/O is confined to terminal/store/export/CLI. |
| 68 / 123 | Can edge cases be easily tested? | PASS | Tests cover empty/invalid/boundary values, decoder limits, duplicate distinctions and fixed snapshots. |
| 69 / 126 | Are all code paths testable? | PARTIAL | Defensive branches are testable but not all exercised; actual symlink/physical signal behavior depends on the environment. Coverage is reported honestly. |
| 70 / 127 | Are error conditions testable? | PASS | Explicit file/format/stream fault seams support error-condition tests; no production fault flags. |
| 71 / 128 | Are there integration testing opportunities? | PASS | Subprocess tests execute main.py and real two-session files; F1/F2 include native closed pipes and real replacement. |
### 8. Maintainability

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 72 / 133 | Is the code properly modularized? | PASS | Each module has one domain/adaptor responsibility; the entry point is thin. |
| 73 / 134 | Are responsibilities clearly separated? | PASS | State, strategy, persistence, export and presentation do not duplicate ownership. |
| 74 / 135 | Is coupling between components minimized? | PASS | Engine depends on a structural ordering interface and immutable values rather than CLI/store globals. |
| 75 / 136 | Is cohesion within components maximized? | PASS | Related validation, state transitions and I/O operations stay within their owning modules. |
| 76 / 139 | Can the code be easily extended? | PASS | ReverseStrategy test demonstrates adding an algorithm without engine edits. |
| 77 / 140 | Are design patterns used appropriately? | PASS | Strategy is listed in docs/design_patterns.md section 1 and is useful for real mode interchangeability. |
| 78 / 141 | Are configuration options provided where needed? | PASS | Mode, seed, history, export and overwrite flags expose the needed choices; extra configuration is optional. |
| 79 / 142 | Is the code flexible for future requirements? | PASS | Typed interfaces and schema/policy versions permit planned extension; no new pattern/infrastructure is added. |
### Red Flags That Require Immediate Attention

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 80 / 190 | **Hardcoded credentials or sensitive data** | PASS | No hardcoded credential/private-key finding in current bounded candidate scan; synthetic fixture data is intentionally retained. |
| 81 / 191 | **SQL injection vulnerabilities** | N/A | No SQL surface. |
| 82 / 192 | **Infinite loops or recursion without proper termination** | PARTIAL | Quiz sessions are finite; repeated external interruptions can prevent finalization progress, an accepted limit. |
| 83 / 193 | **Memory leaks or resource leaks** | PARTIAL | No unbounded application retention was found; interrupted staging cleanup is best effort and can leave a file. |
| 84 / 194 | **Race conditions in concurrent code** | PARTIAL | Concurrent sessions are last-writer-wins and path checks are preflight. These explicit limits are not represented as solved; concurrency infrastructure is optional. |
| 85 / 195 | **Unsafe deserialization** | PASS | No unsafe deserializer/eval is used. |
| 86 / 196 | **Path traversal vulnerabilities** | N/A | User-authorized local file paths are not restricted to a sandbox; no remote traversal boundary is claimed. Alias conflicts are checked. |
| 87 / 197 | **Unvalidated user input** | PASS | External JSON/CLI values are validated; trusted programmatic model constructors rely on their documented typed contract. |
### After Review Actions

| Item / source line | Prompt | Result | Actual review note |
| --- | --- | --- | --- |
| 88 / 212 | Run final tests | PASS | Reused the unchanged-source clean runtime/test/quality evidence as the current user explicitly instructed; no new execution date is invented. |
| 89 / 213 | Update documentation | PASS | Current documentation resolves the supplied rubric/length decision and records the actual code-documentation gap. |
| 90 / 214 | Log AI interaction details | PASS | This dated review and exact evidence are appended to the interaction log. |
| 91 / 215 | Commit with clear commit message | N/A | Commit action is prohibited by the user; no commit/push/publish/submit is performed. |
| 92 / 218 | Document specific issues | PASS | Eight missing executable-bootstrap docstrings are named with source lines and a reproducible AST inspection. |
| 93 / 219 | Make necessary modifications | PENDING | Eight docstrings plus required bootstrap formatting await approval; no active Python/test source was edited. |
| 94 / 220 | Test changes thoroughly | PENDING | After approval, exercise affected CLI/bootstrap tests and quality checks; do not claim they ran for an unimplemented change. |
| 95 / 221 | Update AI edit log with changes made | PASS | The code-quality finding and no-code-change boundary are recorded in the log. |
| 96 / 224 | Document why it's not suitable | N/A | The functioning application is not rejected wholesale; specific test-helper documentation/style criteria remain unmet. |
| 97 / 225 | Create a new, more specific prompt | N/A | No replacement implementation/prompt is needed during this audit. |
| 98 / 226 | Consider alternative approaches | N/A | Optional alternative architectures/patterns are not pursued. |
| 99 / 227 | Learn from the experience | N/A | No new student learning reflection is invented; only reviewer observations and supplied student reflections are recorded. |

## Disposition

The checklist has been applied to all active submission code in the declared scope. This does not turn every checklist suggestion into a mandatory rubric requirement. The missing bootstrap docstrings and confirmed spacing violations are mandatory code-quality findings; large-input/performance/security hardening and concurrency features are not added. Physical Ctrl+C and symlink verification are still UNVERIFIED, not automatically rubric failures. A focused follow-up confirmed audit F3: startup interruption plus expected warning-output failure loses status 130. Its narrow application fix awaits approval.

The user must approve the startup-interrupt application fix, narrow test-source documentation/style correction and final report wording before readiness can be claimed. The physical manual result remains a separate agreed release gate. No commit, push, publication or submission.
