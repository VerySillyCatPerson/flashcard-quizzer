# Final audit against the authoritative rubric

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
| CR2 | Review all AI-generated code using the provided checklist. | **PASS** | checklist_review_2026-11-19.md maps all 99 initial prompts plus dated approved-fix follow-up; f3_fix_review.md reviews changed catch/fault hooks/assertions; f3_manifest.json retains before/red/after source and hashes. |
| CR3 | Document your review process in ai_edit_log.md with specific examples. | **PASS** | docs/ai_edit_log.md Stages 1-9 and dated authoritative-rubric append; checklist_review_2026-11-19.md. |
| CR4 | Show evidence of modifying or rejecting poor AI suggestions. | **PASS** | Log Stage 1 identity/scoring/context, Stage 6 raw-answer/overwrite decisions, Stage 7 F1/F2; stage_7_fix_red.json and stage_7_fix_checks.json. |

### Code Quality

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| CQ1 | All code follows PEP 8 style guidelines. | **PASS** | f3_green_310.json and f3_green_313.json: file-level Black/isort/flake8 and extracted executable _BOOTSTRAP flake8 all exit 0; no rule changes. |
| CQ2 | Proper error handling and input validation. | **PASS** | utils/cli.py::main narrow TerminalOutputError catch; both f3_red_*.json show two failed/two passed before production edits, both f3_green_*.json show four focused passes; RuntimeError traceback remains visible. Existing validation/finalization tests remain passing. |
| CQ3 | Code is readable and maintainable. | **PASS** | Separate engine/strategies/history/terminal/export/paths; main.py thin guard; checklist review sections 2 and 8; documented phase and stream complexity. |
| CQ4 | Functions have appropriate docstrings. | **PASS** | All 210 normally parsed functions documented; all 16 executable bootstrap functions documented (embedded_missing_docstrings empty in both f3_green_*.json). Eight original missing docstrings corrected. |

### Functional Application

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| APP1 | Build a working application that extends the starter code. | **PASS** | main.py + utils CLI meaningfully extend the starter; both current-runtime full suites report 275 passed/one OS symlink skip, including corrected startup-warning status 130. |
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
| UT1 | Achieve >80% test coverage using pytest. | **PASS** | f3_coverage_310.json and f3_coverage_313.json: statements 593/602=98.50%, branches 120/124=96.77%, combined 713/726=98.21%; all 11 production modules including main.py. |
| UT2 | Write tests for both original and AI-generated code. | **PASS** | test_existing_sample_decks preserves original array/wrapper contracts; test_importing_entry_point_does_not_start_quiz and generated domain/CLI tests. Original starter had no implemented runtime logic beyond placeholders. |
| UT3 | Include tests for edge cases and error conditions. | **PASS** | tests/test_data_loader.py missing/unreadable/malformed/type/blank/duplicate/deep/large cases; test_history.py save/load failures; test_finalization.py F1/F2. |
| UT4 | Use clear test names that describe what is being tested. | **PASS** | Examples: test_existing_export_is_refused_without_changing_bytes; test_between_phase_interrupt_continues_pending_work_once; test_real_two_session_round_trip. |

### AI-Generated Code Validation

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| VAL1 | Test all AI-generated code thoroughly. | **PASS** | Current full suites each 275 passed/one privilege-dependent symlink skip; four focused F3 regressions pass after genuine red evidence. All production modules measured; manual verification remains separate. |
| VAL2 | Document any issues found with AI code in ai_edit_log.md. | **PASS** | ai_edit_log.md preserves decoder, F1/F2/shutdown, initial eight-docstring/eight-spacing and F3 findings, actual failures, student approval, correction and dual-runtime verification. |
| VAL3 | Show evidence of fixing or rejecting problematic AI suggestions. | **PASS** | stage_3_regression_before.json and genuine Stage 7 regression chain retained; f3_red_310.json/f3_red_313.json precede production fix; f3_green_310.json/f3_green_313.json show corrected behavior. |

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
| REP4 | Report should be 1000-1500 words. | **PASS** | Approved report 1,381 rendered words / 1,428 raw Markdown whitespace tokens including headings/lists/appendices/footer; original template unchanged; name masked at student request. |

### README Updates

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| README1 | Update README.md with new features and setup instructions. | **PASS** | Root/project/application READMEs describe actual features/setup; current README links post-fix evidence and distinguishes historical clean setup from current-source reruns. |
| README2 | Provide clear usage examples. | **PASS** | Application README help/sequential/adaptive/random/export/overwrite examples; stage_9_commands.json ten actual CLI commands exit 0 across both runtimes. |
| README3 | Document any dependencies or installation requirements. | **PASS** | README Setup, requirements.txt pinned dev tools, requirements-lock.txt Windows/3.13 scope, stdlib-only runtime and explicit interpreter/venv instructions. |

### Submission Checklist

| ID | Mandatory requirement | Status | Exact evidence |
| --- | --- | --- | --- |
| SUB1 | Complete codebase with all source files, tests, and documentation. | **PASS** | Concrete final_submission_inventory.json includes all 11 production/13 test Python files, two sample decks, readmes, guides, report/log and evidence. CQ4 is satisfied by the verified bootstrap docstring corrections. |
| SUB2 | Completed ai_edit_log.md with at least 5 detailed AI interaction examples. | **PASS** | docs/ai_edit_log.md nine grouped stages and current dated resolution; see LOG1-LOG4. |
| SUB3 | Final project report using the provided template (1000-1500 words). | **PASS** | See REP1-REP4; report content/template/length pass and student wording approval is recorded; requested name masking applied. |
| SUB4 | Updated README.md with current setup instructions and feature descriptions. | **PASS** | See README1-README3; root/application/project entry points have no relevant stubs or current missing-rubric claim. |
| SUB5 | Test coverage report demonstrating >80% coverage. | **PASS** | f3_coverage_310.json and f3_coverage_313.json plus complete measurement commands in f3_green_310.json/f3_green_313.json; raw reports included in inventory. |
| SUB6 | Code quality verification: all linting tools should pass without errors. | **PASS** | f3_green_310.json and f3_green_313.json: Black/isort/flake8/strict mypy/pip check/extracted-bootstrap flake8 all exit 0. Earlier lint failure remains in final_bootstrap_lint.json. |


## 2. Approved corrections and genuine before/after evidence

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

Both runs use previously isolated Windows environments against current source.
They are actual runtime runs, not grammar/static checks or another clean install.
The historical Stage 9 clean-install evidence remains valid for its earlier source
snapshot; it is not presented as current-source verification.

| Current check | Python 3.10.11 | Python 3.13.17 |
| --- | --- | --- |
| Focused F3 | 4 passed, 9 deselected | 4 passed, 9 deselected |
| Full pytest | 275 passed, 1 skipped; 22.56s | 275 passed, 1 skipped; 22.99s |
| Black/isort/flake8/strict mypy/pip check | All exit 0 | All exit 0 |
| Extracted executable bootstrap flake8 | Exit 0 | Exit 0 |

All commands, runtime versions, executable paths, cwd and actual streams are saved
in f3_green_310.json/f3_green_313.json. Measurement uses the respective interpreter:

```powershell
python -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json:docs/verification/f3_coverage_310.json
```

The 3.13 run substitutes f3_coverage_313.json. All 11 production modules including
main.py appear in both raw coverage reports. Configurations and exclusions are
unchanged; the combined 81% gate is stricter than the rubric's >80% requirement.
The zero-statement Stage 2 baseline is not submission evidence.

| Coverage | Covered/total | Percent |
| --- | ---: | ---: |
| Statements | 593/602 | 98.50% |
| Branch outcomes | 120/124 | 96.77% |
| Combined | 713/726 | 98.21% |

Combined is (593+120)/(602+124), not branch-only coverage or an average of
percentages. Nine statements/four branch outcomes remain uncovered in defensive
terminal/export/cleanup paths. Optional extra coverage was not added. The same
actual symlink test skips with WinError 1314; passing hard-link tests are separate.

## 6. Report, submission inventory and hygiene

The report contains **1,381 rendered-text words / 1,428 raw Markdown
whitespace tokens**, including headings, lists, appendices and footer. It has no
tables; none are excluded by this method. Rendered counting strips Markdown
syntax/link destinations only. All template headings and three examples remain;
the official template, supplied reflection paragraphs and four rating values are
unchanged. The student authorized factual updates to stale self-assessment reasons;
the original reasons remain preserved in the historical log.
Factual metrics now identify current-source runs rather than reusing old coverage.
**Final wording is approved.** The student's name is masked as requested.

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
| Report wording | Approved | User readiness gate satisfied | Student explicitly approved and requested name masking |
| Physical Ctrl+C | UNVERIFIED | Not explicitly required; user readiness gate | Perform shortest README procedure and report actual 130/partial-summary/files observations |
| Actual symlink behavior | UNVERIFIED | No explicit requirement; coverage threshold already met | Optional capable-environment run; retain WinError 1314 limit |
| Other platforms/patches | UNVERIFIED | No requirement to test every environment | Keep tested-runtime scope explicit |
| Forced termination/concurrency/uncertain writes | Documented limits | No new infrastructure requirement inferred | No blind interrupted-write replay; no concurrent merge guarantee |

No confirmed mandatory gaps remain in the inspected scope. Report wording is
approved; the physical result remains pending. No human observation or post-fix acceptance
was invented. Stop for review. No commit, push, publication or submission.
