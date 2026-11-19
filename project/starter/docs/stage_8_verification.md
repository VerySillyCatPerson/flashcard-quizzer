# Stage 8 verification and documentation audit

**Resolution dated 2026-11-19:** The authoritative rubric has been supplied and
the 1,000-1,500-word limit is settled. This file retains Stage 8's historical
results and then-pending items. See [the current audit](final_rubric_audit.md)
for current mandatory/optional distinctions and the dated checklist review.

Date: 2026-11-18. Stage 7 was accepted explicitly on reported regression evidence
and explained limitations. Stage 8 verification/documentation is complete for
review; no Stage 8 acceptance or submission authorization is inferred.

## Executed checks

Run from `C:/Projects/flashcard/project/starter` using the existing
`.venv/Scripts/python.exe`: **Windows CPython 3.13.17**. No new environment or
dependency installation was performed.

| Command after the interpreter | Actual result |
| --- | --- |
| `-m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 0; 271 passed, one skipped in 21.78 seconds |
| `-m black --check .` | Exit 0; 24 Python files unchanged |
| `-m isort --check-only .` | Exit 0; existing configured skips only |
| `-m flake8 .` | Exit 0; no lint output |
| `-m mypy .` | Exit 0; no issues in 24 files; strict target 3.10 |
| `-m pip check` | Exit 0; no broken requirements |
| `ast.parse(..., feature_version=(3, 10))` over all Python source/tests | Exit 0; 24 files parse; execution was 3.13.17 |

[Raw commands, statuses and output](verification/stage_8_checks.json) preserve
the run. These are current-environment results, not Stage 9 clean-install proof.
The Stage 2 empty-test/zero-statement baseline is historical and is not submission
coverage evidence.

## Coverage: three distinct measures

Coverage.py's branch-enabled total combines executable statement lines and branch
outcomes. It is not branch coverage alone and not an unweighted mean of the two
percentages.

| Measure | Covered | Total | Missing | Percent |
| --- | ---: | ---: | ---: | ---: |
| Executable statements | 590 | 599 | 9 | 98.50% |
| Branch outcomes | 120 | 124 | 4 | 96.77% |
| Combined tool total | 710 | 723 | 13 opportunities | 98.20% |

Combined calculation: `(590 + 120) / (599 + 124) * 100`.
There are four partially covered branches. The configured gate is **81% combined**,
strictly above 80%. All production modules, including main.py and the package
initializer, are present; tests, local tools and environments are omitted by the
unchanged configuration. No coverage exclusion was added.

The [raw coverage JSON](verification/stage_8_coverage.json) and
[derived metrics](verification/stage_8_metrics.json) retain exact counts and
unrounded percentages. Local generated HTML is `htmlcov/index.html`; the retained
JSON remains reviewable without that ignored directory.

Uncovered behavior remains explicit:

| Location | Unexercised behavior |
| --- | --- |
| results_export.py 59–60 | Destination inspection raises an OS error rather than absence |
| results_export.py 91–92 | Encoding raises ValueError |
| results_export.py 124–125 | Cleanup raises another OS error |
| results_export.py 121 → 126 | Failure before a temporary path exists, skipping cleanup |
| cli.py 237 | Pre-session structured output-error fallback |
| cli.py 145 → 169 | Resuming directly at warnings, bypassing export selection |
| cli.py 182 → 122 | Warning-output failure continues without enqueueing another diagnostic |
| terminal.py 33–34 | Native descriptor retirement itself fails |
| terminal.py 27 → 35 | Failed output stream is not a native TextIOWrapper |

The optional export error-boundary tests remain deferred as requested. Coverage
does not prove every interruption timing, combined failure or platform behavior.

## Requirement and behavior evidence

| Agreed behavior | Current evidence |
| --- | --- |
| Both sample formats and strict runtime validation | Loader/model tests, original sample bytes unchanged |
| Case/outer-space normalization; internal spaces/punctuation meaningful | Identity/evaluation tests; identical normalized pairs rejected with positions; same front/different back allowed |
| Finite sessions and immutable observations | Engine/strategy tests verify one-card-once, stable snapshots, source preservation and non-consuming reads |
| Seeded randomness and stable adaptive order | Same-seed behavior, valid unchanged shuffle, fixed session order and deck-order ties |
| Error balance and shared history | +1/-1 floor zero, completed answers in every mode, real two-session temporary-file round trips and cross-deck identity |
| Missing/corrupt/unreadable/save-failed history | Fresh start or explicit degraded warning; problematic bytes preserved; known failure retries do not recount |
| Export content and overwrite protection | Metadata/statistics/missed cards only; no raw answers; default refusal preserves bytes; explicit replacement and late-arriving-destination protection |
| Path conflicts | All role pairs and overwrite combinations; canonical names and real hard-link aliases; symlink case outstanding |
| F1/F2 finalization | Boundary interrupts, uncertain commits before/after replacement, output failure and permanent broken pipes retain pending work and statuses |
| Human/OS interaction and classroom compliance | Limited by the outstanding items below; no full-rubric compliance claim |

The current suite reruns Stage 7 regressions. Their original failing outputs were
captured in Stage 7, not recreated or relabeled as new Stage 8 failures.
[The fix review](stage_7_fix_review.md) links red/green evidence and explains:
history already committed is never replayed; an interrupted write may already
have committed, so that attempt is not blindly retried. Output failure permits
saving/export, and failed native descriptors are retired to preserve 1/130 through
shutdown. Formatting programming errors remain visible.

## Interaction-log audit

[The audited log](ai_edit_log.md) has eight actual stage entries with grouped
follow-ups; that exceeds the supplied requirement for five detailed real examples
without inventing exchanges. It is not a count of every chat turn.

- Stage 1 retains rejected path identity, front-only uniqueness, cumulative
  scoring and optional context, followed by actual accepted rules.
- Stage 2 distinguishes setup from absent functionality and zero-statement
  coverage; the user's acceptance preserves Python 3.10 as the target.
- Stages 3–5 retain decoder regression, state/snapshot checks, mock-scope/type/lint
  corrections, and conditional acceptances only after the requested checks.
- Stage 6 retains original export behavior, the actual no-raw-answer/overwrite
  refinement, initial lint corrections and the acceptance based on reported tests.
- Stage 7 retains findings before fixes, original regression failures, harness
  correction, the additional shutdown-status failure and subsequent passing checks.
  Its acceptance is now recorded verbatim on the user's stated basis.
- Stage 8 records the current request and both actual student responses before
  personal sections were written. Self-ratings are student opinions, not test scores.

The fictional starter example and two blank entries were removed. Historical
“pending review/reflections” statements describe their delivery time; actual later
decisions resolve them without rewriting earlier history. The user's “contrinue”
is not treated as review. Authorship/edit line counts and personal rankings were
not fabricated. Two historical log labels and the initial Stage 7 review label
were corrected from branch-only wording to combined coverage; original numbers
and raw evidence remain untouched.

One audit search used a literal Windows wildcard path; rerunning with rg's glob
filter corrected the documentation search. This was not an application failure.
An initial footer validation assertion also failed because the helper's literal
en dash became a question mark over PowerShell's ASCII stdin transport. The report
was already valid UTF-8; escaped Unicode fixed the helper, and validation passed.

The [structured audit](verification/stage_8_log_audit.json) records acceptance
provenance, retained corrections and linked evidence checks.

## Report and measured code size

[The report draft](final_report.md) follows the official template's section order,
contains three concrete collaboration examples including F1/F2, and incorporates
A***** P*****'s supplied reflections and four self-assessment ratings of 4/5.
It distinguishes assistant-run checks from student review on reported evidence.

The report is **1,223 words** after removing Markdown syntax/link destinations
and counting whitespace-separated rendered text across the whole file, including
headings, appendices and footer. Raw Markdown has **1,270 whitespace tokens**.
Both measures are inside **1,000–1,500**. The unchanged official template's
conflicting 2,000–3,000 footer is explicitly noted; the classroom/user limit governs.
Submission date, due date and missing instructions are not invented.

Metrics are measured from source rather than inferred AI authorship:

| Scope | Python files | Physical lines | Nonblank lines | Functions including methods/nested | Classes |
| --- | ---: | ---: | ---: | ---: | ---: |
| Production | 11 | 1,162 | 976 | 62 | 22 |
| Tests | 13 | 2,566 | 2,223 | 146 | 2 |

Physical lines include comments/docstrings and blanks; executable coverage
statement counts are a different measure. Flake8 supplies an exit result, not a
numeric linting score. [Report validation](verification/stage_8_report_validation.json)
records counting rules, heading checks and local-link validation.

## Outstanding verification and accepted limits

| Outstanding | Status |
| --- | --- |
| Full classroom rubric | Unavailable. Proposed additions are persistent adaptive history, seeded randomness and JSON export; generic “beyond CRUD” sufficiency remains unaudited. |
| Physical Ctrl+C | Unverified. KeyboardInterrupt injection is not keyboard/OS signal delivery. The existing manual script's noninteractive run is historical Stage 6 evidence. |
| Python 3.10 runtime | Unverified. Static/grammar and prior resolver checks do not substitute for executing on 3.10. |
| Actual symlink | One test skipped after WinError 1314, missing creation privilege. Real hard-link and resolved-name tests passed; neither verifies symlink traversal. |
| Clean-environment reproduction | Stage 9 work, not performed here. |

Repeated interrupts/forced termination can prevent finalization. An interrupted
write can have uncertain old/new state or leave a temporary file; retries are
conservative. Atomic replacement does not merge concurrent sessions, and preflight
path checks do not lock later filesystem changes. An unusable stderr cannot
deliver warnings; descriptor retirement has a best-effort fallback.

README reflects these behavior and verification limits. The
[before/after manifest](verification/stage_8_manifest.json) confirms unchanged
application/tests, dependencies, configuration, official template and sample decks.
Only documentation and verification artifacts changed.

**Stage 8 stops here for review. No Stage 9 execution, commit, push or submission.**

