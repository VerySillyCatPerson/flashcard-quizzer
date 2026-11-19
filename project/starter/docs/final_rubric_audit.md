# Final audit against the authoritative rubric

**Independent-review update — 2026-11-19:** Portable nesting tests and card-text
control escaping are verified on Windows Python 3.10.11/3.13.17; the student
accepted these corrections and factual updates based on reported evidence. The reviewer’s Linux/Python 3.12.14 issue was not
executed here. [Actual changes/red-green evidence](independent_review_fixes.md)
and [the prior audit snapshot](verification/independent_review_before_audit.json)
separate current results from historical F1/F2/F3/clean-setup evidence.

Updated after approved corrections: **2026-11-19**. Authority:
[the supplied request/rubric](authoritative_audit_request.md).
**39 PASS; no remaining confirmed mandatory gaps.** This is an evidence-based
audit; the student accepted F3/bootstrap corrections on reported regression evidence.
It is not a submission-readiness claim. Final report wording is approved; physical
Ctrl+C remains the student's outstanding readiness gate. Actual symlinks
remain privilege-blocked and unverified.

The authoritative report limit is **1,000-1,500 words**. The unchanged official
template's old 2,000-3,000 footer is superseded, not an unresolved requirement.
The initial 34 PASS/two PARTIAL/three FAIL findings are preserved in
[the before-audit snapshot](verification/f3_before_audit.json), the interaction log,
initial machine evidence and [before/after manifest](verification/f3_manifest.json).

## 1. Mandatory requirement-by-requirement audit

Paths are relative to project/starter unless described as repository root; saved
JSON names are under docs/verification. The [structured matrix](verification/final_rubric_requirements.json)
also records gap/consequence/smallest-correction fields. No unresolved correction
is required for the current PASS rows; this does not certify every possible input
or platform, subjective grading, or student final approval.

### AI Code Review

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| CR1 | Use AI tools to generate code for your application. | **PASS** | utils/models.py; utils/cli.py; docs/ai_edit_log.md Stage 3/6/7 implementation records; stage_7_fix_manifest.json original_code and current source. |
| CR2 | Review all AI-generated code using the provided checklist. | **PASS** | checklist_review_2026-11-19.md maps initial prompts and follow-ups; independent_review_fixes.md reviews decoder-only mocks, card display controls and original-domain persistence; independent_review_manifest.json identifies final tested source. |
| CR3 | Document your review process in ai_edit_log.md with specific examples. | **PASS** | docs/ai_edit_log.md Stages 1-9 and dated authoritative-rubric append; checklist_review_2026-11-19.md. |
| CR4 | Show evidence of modifying or rejecting poor AI suggestions. | **PASS** | Log Stage 1 identity/scoring/context, Stage 6 raw-answer/overwrite decisions, Stage 7 F1/F2; stage_7_fix_red.json and stage_7_fix_checks.json. |

### Code Quality

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| CQ1 | All code follows PEP 8 style guidelines. | **PASS** | independent_review_green_310.json and independent_review_green_313.json: Black/isort/flake8 plus extracted executable bootstrap flake8 all exit 0, using unchanged configuration. |
| CQ2 | Proper error handling and input validation. | **PASS** | utils/terminal.py::_one_line escapes C0/DEL/C1 card text; tests cover all 65 controls at each display boundary. utils/data_loader.py decoder handling is unchanged; deterministic boundary and real nested-file contracts pass. Existing F3/finalization/error tests pass both full suites. |
| CQ3 | Code is readable and maintainable. | **PASS** | Separate engine/strategies/history/terminal/export/paths; main.py thin guard; checklist review sections 2 and 8; documented phase and stream complexity. |
| CQ4 | Functions have appropriate docstrings. | **PASS** | 215 normally parsed functions and all 16 executable bootstrap functions have docstrings; current source/AST inspection and unchanged bootstrap checks verified. |

### Functional Application

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| APP1 | Build a working application that extends the starter code. | **PASS** | Implemented main.py CLI and both current Windows runtime full suites: 343 passed/one privilege-dependent symlink skip, including original modes, persistence, export and new display protection. |
| APP2 | Implement at least 3 new features beyond basic CRUD operations. | **PASS** | Persistent adaptive learning: history.py/AdaptiveStrategy + test_history_reuse_changes_next_adaptive_order; seeded replay: RandomStrategy + test_seeded_randomness_reproduces_order; JSON session export: results_export.py + actual export/overwrite transcripts. |
| APP3 | Application should have clear functionality and purpose. | **PASS** | README.md purpose/usage; finite quizzes with immediate feedback and answered-only statistics. |
| APP4 | Use AI assistance throughout the development process. | **PASS** | ai_edit_log.md planning, setup, implementation, debugging, review, verification and documentation entries; no invented line-by-line authorship metric. |

### Design Patterns

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| DP1 | Implement at least 1 design pattern from the provided guide. | **PASS** | docs/design_patterns.md section 1 Strategy Pattern; utils/strategies.py::QuizStrategy, SequentialStrategy, RandomStrategy, AdaptiveStrategy. |
| DP2 | Pattern should serve a real purpose, not be forced. | **PASS** | engine.py::QuizSession calls strategy.order once; test_structural_strategy_runs_once_and_order_is_snapshotted proves a new strategy without engine changes. |
| DP3 | Document why you chose the pattern in your final report. | **PASS** | final_report.md Software Engineering Practices / Design Patterns Used explicitly names guide section 1 and the goal of changing ordering without rewriting grading/progress. |

### Unit Testing

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| UT1 | Achieve >80% test coverage using pytest. | **PASS** | independent_review_coverage_310.json and independent_review_coverage_313.json: statements 595/604=98.51%, branches 120/124=96.77%, combined 715/728=98.21%; all 11 production modules including main.py. |
| UT2 | Write tests for both original and AI-generated code. | **PASS** | test_existing_sample_decks preserves original array/wrapper contracts; test_importing_entry_point_does_not_start_quiz and generated domain/CLI tests. Original starter had no implemented runtime logic beyond placeholders. |
| UT3 | Include tests for edge cases and error conditions. | **PASS** | tests/test_data_loader.py decoder-only RecursionError translation plus real 5,000-deep rejection; tests/test_terminal.py all C0/DEL/C1 display contexts, Unicode and domain round trips; existing history/export/finalization error tests retained. |
| UT4 | Use clear test names that describe what is being tested. | **PASS** | Examples: test_existing_export_is_refused_without_changing_bytes; test_between_phase_interrupt_continues_pending_work_once; test_real_two_session_round_trip. |

### AI-Generated Code Validation

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| VAL1 | Test all AI-generated code thoroughly. | **PASS** | Both current full suites: 343 passed/one symlink skip; revised nesting 2 passed and terminal 70 passed. Linux/Python 3.12 reported issue is distinguished from Windows baseline observations, not claimed executed. |
| VAL2 | Document any issues found with AI code in ai_edit_log.md. | **PASS** | ai_edit_log.md existing stage entries plus actual independent-review request, Windows original nesting baseline, new red terminal results, minimal fix, dual-runtime green/quality and actual user acceptance on reported evidence. |
| VAL3 | Show evidence of fixing or rejecting problematic AI suggestions. | **PASS** | Earlier decoder/F1/F2/F3 red-green records preserved; independent_review_red_310.json and independent_review_red_313.json show 63 failed/7 passed terminal tests before production change; current green files show 70 terminal passes. |

### AI Interaction Log

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| LOG1 | Complete detailed ai_edit_log.md with specific examples of AI usage. | **PASS** | Nine detailed stage entries with grouped actual follow-ups; fictional starter example removed, historical facts preserved. |
| LOG2 | Document prompts you used and AI responses you received. | **PASS** | Each stage records Prompt/Request, AI Response, changes, reasons and actual outputs; attached original/final audit requests preserved. |
| LOG3 | Explain your decision-making process for accepting/rejecting AI suggestions. | **PASS** | Explicit User Review sections separate proposed versus accepted identity, scoring, duplicates/context, export and finalization policies. |
| LOG4 | Include at least 5 meaningful AI interactions. | **PASS** | Five concrete examples detailed in current audit: Stage 1 identity/scoring, Stage 3 narrow decoder fix, Stage 5 retry review, Stage 6 export refinements, Stage 7 F1/F2 correction. |

### Final Report

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| REP1 | Complete the final report using the provided template. | **PASS** | final_report.md preserves every major/minor template heading; report_template.md unchanged SHA-256; all report fields filled. |
| REP2 | Explain how you used AI throughout your development process. | **PASS** | Report Executive Summary, AI Collaboration Experience, three actual examples including F1/F2, current checklist attribution. |
| REP3 | Reflect on what you learned about working with AI tools. | **PASS** | Report reflection paragraphs and four rating values match student input; authorized factual self-assessment reasons now reflect completed runtime/reproduction/rubric checks. Original reasons remain in the Stage 8 log. |
| REP4 | Report should be 1000-1500 words. | **PASS** | Report 1,398 rendered words / 1,445 raw Markdown whitespace tokens including headings/lists/appendices/footer. Earlier wording approval preserved; current factual verification updates accepted on reported evidence; reflection/rating text unchanged. |

### README Updates

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| README1 | Update README.md with new features and setup instructions. | **PASS** | Application README documents display-only C0/DEL/C1 escaping, original domain values, current tests/coverage/setup and explicit Linux/Python 3.12 limit; root/project links remain valid. |
| README2 | Provide clear usage examples. | **PASS** | Application README help/sequential/adaptive/random/export/overwrite examples; stage_9_commands.json ten actual CLI commands exit 0 across both runtimes. |
| README3 | Document any dependencies or installation requirements. | **PASS** | README Setup, requirements.txt pinned dev tools, requirements-lock.txt Windows/3.13 scope, stdlib-only runtime and explicit interpreter/venv instructions. |

### Submission Checklist

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| SUB1 | Complete codebase with all source files, tests, and documentation. | **PASS** | Concrete final_submission_inventory.json includes all 11 production/13 test Python files, two sample decks, readmes, guides, report/log and evidence. CQ4 is satisfied by the verified bootstrap docstring corrections. |
| SUB2 | Completed ai_edit_log.md with at least 5 detailed AI interaction examples. | **PASS** | docs/ai_edit_log.md nine grouped stages and current dated resolution; see LOG1-LOG4. |
| SUB3 | Final project report using the provided template (1000-1500 words). | **PASS** | See REP1-REP4; template/content/length criteria pass. Prior report wording approval remains recorded; independent-review factual metric updates were accepted on reported evidence. |
| SUB4 | Updated README.md with current setup instructions and feature descriptions. | **PASS** | See README1-README3; root/application/project entry points have no relevant stubs or current missing-rubric claim. |
| SUB5 | Test coverage report demonstrating >80% coverage. | **PASS** | Current independent_review_coverage_310.json/independent_review_coverage_313.json and complete measurement commands in independent_review_green_310.json/independent_review_green_313.json are included in inventory. |
| SUB6 | Code quality verification: all linting tools should pass without errors. | **PASS** | independent_review_green_310.json and independent_review_green_313.json: full Black/isort/flake8/strict mypy/pip check and extracted-bootstrap flake8 all exit 0 with unchanged rules. |


## 2. Historical approved F3 corrections and genuine before/after evidence

The user explicitly approved the F3 correction and bootstrap docstring/spacing
work. Both runtimes first ran the new tests against unchanged production:
**two failed/two passed**. Healthy-warning and unexpected-RuntimeError controls
passed; restored/permanently broken native pipes returned 1 instead of 130.
After the narrow TerminalOutputError catch around the startup warning, all four
pass. Unexpected RuntimeError retains a visible traceback; expected I/O failures
retain 130 without a traceback or pre-quiz history/export. These are injected
interruptions and real native pipes, not a physical keyboard check.

Eight missing embedded helper docstrings and eight E301/E302/E305 blank-line
violations were corrected. All 210 normally parsed and 16 embedded functions are
documented; extracted-script flake8 now exits 0 on both runtimes. No quality rule,
existing assertion or coverage configuration changed. Only utils/cli.py,
tests/cli_helpers.py and tests/test_finalization.py changed among 31 protected files.

See [fix review](f3_fix_review.md), [3.10 red](verification/f3_red_310.json),
[3.13 red](verification/f3_red_313.json), [3.10 green/full](verification/f3_green_310.json),
[3.13 green/full](verification/f3_green_313.json) and the source manifest.
The original [failing embedded lint](verification/final_bootstrap_lint.json) and
[F3 probe](verification/final_startup_interrupt_reproduction.json) remain intact.

Earlier genuine F1/F2 evidence also remains: original red **4 failed/2 passed**,
expanded red **5/5**, permanent-pipe shutdown red **2/7**, then **12 focused passes**
in stage_7_fix_checks.json. Harness collection failures are labeled separately.
Full current suites retain committed-once history, independent export, uncertain
write, default overwrite refusal and no-raw-answer assertions.

## 3. Actual checklist review and meaningful interactions

[The checklist review](checklist_review_2026-11-19.md) maps all 99 prompts and
preserves its initial 59 PASS/24 PARTIAL/14 N/A/two pending dispositions. A dated
follow-up reviews these approved source/assertion changes and resolves the defects;
it does not erase optional limits, invent earlier review or claim student all-line
inspection. The initial source-review hashes describe the initial code; the new
manifest identifies final tested source. Four supplied student ratings and
first-person reflections are unchanged.

Five concrete actual review groups:


| Actual request/review | Decision or correction | Evidence |
| --- | --- | --- |
| Stage 1: moving decks must preserve history; compare cumulative versus decreasing mistakes; distinguish duplicate fronts | Rejected path identity/front-only uniqueness and optional context; accepted content-pair identity and error balance | ai_edit_log.md Stage 1 actual follow-ups; models.py card_id; test_identity_survives_rename_reorder_and_additions; test_matching_fronts_with_different_backs_are_valid |
| Stage 3: show field-boundary serialization and oversized-integer regression/exception scope | Confirmed JSON-pair hashing distinguishes ab/c from a/bc; reviewed decoder-only ValueError handling and preserved unexpected validation errors | stage_3_regression_before.json; stage_3_review_checks.json; test_oversized_integer_field_is_a_loader_error; test_unexpected_validation_errors_are_not_disguised |
| Stage 5: confirm failed-save retry does not count answers twice | Retained copy-then-commit ownership; four known failure boundaries keep score 2 until retry writes 3, not 4; no extra implementation was needed for acceptance | stage_5_review_checks.json; test_failed_save_preserves_previous_valid_history_and_can_retry |
| Stage 6: remove unnecessary raw answers; require explicit result replacement | Removed per-answer export data, added --overwrite, retained independent history updates, byte-preserving refusal and atomic publication | stage_6_export_review_checks.json; test_export_refusal_and_overwrite_leave_history_updates_independent; test_file_created_after_absence_check_is_not_overwritten |
| Stage 7: reproduce F1/F2 before changing code; resume pending phases without blind replay | Failing regressions preceded phase/terminal fixes; additional native-pipe shutdown regression caught status 120; no committed history replay | stage_7_fix_red.json, expanded_red, shutdown_red and checks; tests/test_finalization.py |

These are real requests/decisions, not artificial exchanges invented to satisfy
a count. The log separately attributes AI proposals, student acceptance/rejection,
assistant-run checks and unperformed manual observations. Student reflections and
four 4/5 ratings are retained from the actual Stage 8 replies.


## 4. Three distinct non-CRUD additions and CLI proof

| Counted feature | User-visible purpose and implementation | Independent CLI/test proof |
| --- | --- | --- |
| 1. Persistent adaptive learning | Past completed answers change future practice order; error balance decreases after correct practice. HistoryStore plus AdaptiveStrategy work across sessions. | --mode adaptive --history; test_history_reuse_changes_next_adaptive_order; test_real_two_session_round_trip; stage_9_commands.json |
| 2. Seeded random sessions | A chosen seed reproduces the random session order without depending on history or export. This is reproducible practice, not just bare shuffling. | --mode random --seed; test_seeded_randomness_reproduces_order asserts paired CLI sessions; test_same_seed_reproduces_order; saved native seeded examples |
| 3. Optional JSON session export | Produces machine-readable metadata/statistics/missed cards for review; distinct from displaying the table or storing learning scores. | --export/--overwrite; exact-schema/no-raw-answer tests; five documented CLI examples per runtime and export transcripts |

Content hashing, atomic writes, path-conflict protection, comparison normalization
and overwrite permission support these features; they are not counted again as
extra features. No CRUD editor/database was invented. Optional multiple patterns,
external APIs, logging/configuration systems, diagrams or optimization work were
not added for rubric points.

Strategy is explicitly listed at docs/design_patterns.md section 1 (line 7).
QuizStrategy/three implementations provide interchangeable ordering; QuizSession
requests one permutation, then handles grading/progress without mode branches.
test_structural_strategy_runs_once_and_order_is_snapshotted demonstrates a
fourth algorithm without modifying the engine. The report explains this choice.


## 5. Current full verification and coverage

Both Windows runtime runs use existing isolated environments against current
source, not new clean installations or Linux verification. The original nesting
test passed on both Windows versions before editing. The revised decoder/real-file
tests each pass, without relying on the decoder's recursion threshold. Before
production changes, terminal tests gave 63 failed/7 passed on each runtime.

| Current check | Python 3.10.11 | Python 3.13.17 |
| --- | --- | --- |
| Revised nesting | 2 passed, 71 deselected | 2 passed, 71 deselected |
| Terminal regressions | 70 passed | 70 passed |
| Full pytest | 343 passed, 1 skipped; 22.80s | 343 passed, 1 skipped; 22.38s |
| Black/isort/flake8/strict mypy/pip check | All exit 0 | All exit 0 |
| Extracted executable bootstrap flake8 | Exit 0 | Exit 0 |

Actual runtime/cwd/commands/streams are in independent_review_green_310.json and
independent_review_green_313.json; before-production results are in the red files.
Measurement uses each corresponding interpreter:

```powershell
python -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json:docs/verification/independent_review_coverage_310.json
```

The 3.13 run substitutes independent_review_coverage_313.json. All 11 production
modules including main.py appear in both raw reports. The 81% combined gate,
coverage exclusions, dependencies and quality rules are unchanged. The Stage 2
zero-statement baseline and earlier source coverage are not current submission
evidence.

| Coverage | Covered/total | Percent |
| --- | ---: | ---: |
| Statements | 595/604 | 98.51% |
| Branch outcomes | 120/124 | 96.77% |
| Combined | 715/728 | 98.21% |

Combined is (595+120)/(604+124). Nine statements/four branch outcomes remain
uncovered in existing defensive terminal/export/cleanup paths. The same actual
symlink test skips with WinError 1314; hard-link success is separate evidence.
Physical Ctrl+C and Linux/Python 3.12 were not verified.

## 6. Report, submission inventory and hygiene

The report contains **1,398 rendered-text words / 1,445 raw Markdown
whitespace tokens**, including headings, lists, appendices and footer. It has no
tables; none are excluded by this method. Rendered counting strips Markdown
syntax/link destinations only. All template headings and three examples remain;
the official template, supplied reflection paragraphs and four rating values are
unchanged. The student authorized factual updates to stale self-assessment reasons;
the original reasons remain preserved in the historical log.
Factual metrics now identify current-source runs rather than reusing old coverage.
**Prior report wording approval is preserved.** The current factual verification
updates and independent-review correction are accepted on reported evidence. The name remains masked.

Use [the concrete inventory](verification/final_submission_inventory.json), which
includes current uncommitted files rather than a whole workspace or HEAD-only zip:

- Root .gitignore, README.md, LICENSE.txt, CODEOWNERS and project/README.md.
- main.py plus utils/*.py (11 production files), all 13 test/helper Python files.
- data/glossary.json and data/python_basics.json, preserving both original formats.
- Application README/.gitignore/.editorconfig/.flake8/pyproject.toml and both
  requirements files; the lock file's Windows/3.13 scope remains explicit.
- Report, log, unchanged official template, pattern/checklist guides, audit,
  manual/environment instructions and original instructional scaffolding.
- Verification evidence, including historical failures, new red/green runs,
  current coverage, source manifest, inventory and integrity checks.

[Integrity results](verification/final_rubric_audit_checks.json) check required paths,
relative file links, referenced evidence accessibility and actual eligible files.
No detected credentials/private keys, real learning/session state, environments,
caches or local tools belong to the inventory. Synthetic fixtures/evidence and
documented author/machine metadata are intentional. The recognizable-secret scan
is bounded, not proof against every undisclosed secret. The prior 168 Git-ignore
probes remain valid against unchanged rules. No optional feature/dependency/pattern
or performance work was added.

## 7. Remaining limits and user actions

| Item | State | Explicit rubric blocker? | Required action |
| --- | --- | --- | --- |
| F3, helper spacing/docstrings | Corrected, verified and accepted | Previously CQ1/CQ2/CQ4/APP1/SUB6; now PASS | Student accepted on reported regression evidence; no further correction pending |
| Independent-review fixes | Verified and accepted | No confirmed mandatory gap after checks | Student accepted corrections and factual metric updates on reported evidence |
| Linux/Python 3.12.14 | UNVERIFIED | No requirement to execute every platform | Reviewer observation is reported, not independently reproduced |
| Report wording | Prior wording approved | User readiness gate satisfied | Student explicitly approved and requested name masking |
| Physical Ctrl+C | UNVERIFIED | Not explicitly required; user readiness gate | Perform shortest README procedure and report actual 130/partial-summary/files observations |
| Actual symlink behavior | UNVERIFIED | No explicit requirement; coverage threshold already met | Optional capable-environment run; retain WinError 1314 limit |
| Other platforms/patches | UNVERIFIED | No requirement to test every environment | Keep tested-runtime scope explicit |
| Forced termination/concurrency/uncertain writes | Documented limits | No new infrastructure requirement inferred | No blind interrupted-write replay; no concurrent merge guarantee |

No confirmed mandatory gaps remain in the inspected scope. Report wording is
approved; the physical result remains pending. No human observation or post-fix acceptance
was invented. No further implementation or audit cycle is requested. No commit, push, publication or submission.
