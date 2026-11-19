# Stage 9: clean reproduction and final audit findings

**Later resolution — 2026-11-19:** The student has now supplied the authoritative
rubric, which fixes the report at 1,000-1,500 words. That former gap is resolved.
The [current rubric audit](final_rubric_audit.md) and
[dated checklist review](checklist_review_2026-11-19.md) supersede this historical
snapshot for current compliance status. They record eight missing test-bootstrap
docstrings, eight embedded-script spacing errors and the F3 startup-interruption
exit-status defect in the initial audit. The user subsequently approved corrections;
[the fix review](f3_fix_review.md) records both runtimes passing all affected/full
checks after the regression-first fix. Physical Ctrl+C and actual
symlink behavior remain unverified; neither is an explicit rubric requirement.
Report wording and the agreed manual result remain separate readiness gates.

Date: 2026-11-18. Stage 8 verification/documentation was accepted on reported
evidence; **report wording remains subject to the student's final review**.
This audit checks available repository/user requirements. The full classroom rubric
was not supplied, so **complete rubric compliance is not claimed**.

**Cleanup follow-up — 2026-11-19:** The user accepted the reproduction evidence
and authorized link/ignore cleanup. The three root placeholder links were removed
and replaced with an application-README link. New repository-wide rules ignore
local .env variants and conventional private-key names while retaining named
dummy examples/templates, public-key names, and certificates. All 168 Git path
probes passed; no existing candidate file was hidden. Current documentation and
Git-exclusion results are in [cleanup evidence](verification/stage_9_cleanup_checks.json).
The report is now 1,255 rendered words after the factual cleanup-status update.
The missing rubric, blocked symlink check, physical Ctrl+C, and final report
wording review remain unresolved. Submission readiness is not claimed.

The sections below preserve the original 2026-11-18 audit and its then-open
link/ignore findings. The follow-up above resolves those two cleanup findings;
historical command outputs and inventories have not been rewritten.

## Initial result and concrete gaps (2026-11-18)

No application defect was reproduced. Application code, tests, dependencies,
quality/coverage configuration, samples and the official template were not changed.

1. **Repository documentation gap:** The inherited root README has three
   placeholder links: www.item1.com, www.item2.com and www.item3.com (lines 47–49).
   Without schemes they are relative paths and do not resolve. Application README
   and report file links resolve in the tested repository layout. Root placeholders
   were left unchanged for review.
2. **Unverified checks:** Physical keyboard Ctrl+C and actual file-symlink behavior
   remain unverified. Windows rejects symlink creation with WinError 1314, including
   the follow-up outside the sandbox. Hard-link tests passed.
3. **Audit/approval limits:** The full rubric is unavailable and report wording is
   not finally approved. The three proposed additions cannot be certified against
   the generic “beyond CRUD” wording without that rubric.
4. **Optional repository hardening:** No credential files or recognizable secrets
   were detected, but .env/private-key patterns are absent from .gitignore.
   This is a policy gap for possible future files, not a detected credential leak.

No application change is proposed from these findings. Root-link cleanup and
optional ignore hardening remain visible findings rather than silent scope changes.
Repeated interruption, forced termination, uncertain writes, concurrent sessions
and preflight-only path checks retain their previously accepted limits.

## Separate clean reproduction

An explicit Git candidate selection included current tracked and untracked work:
`git ls-files --cached --others --exclude-standard -- project README.md LICENSE.txt CODEOWNERS`.

The initial **106-file** snapshot preserved root/project/starter layout, including
the relative license target. It contained no .git, existing venv, .tools, caches
or personal history. A second identical snapshot was made from those files.
Hashes are in [the copy manifest](verification/stage_9_clean_copy.json).
The final candidate inventory grows only by subsequent audit/documentation artifacts.

Two new venvs were created inside the copies with the README's standard venv/pip
workflow, using installed CPython 3.13.17 and an official NuGet CPython 3.10.11
bootstrap. Neither old site-packages nor workspace application imports were reused.
Environment records show different prefixes, include-system-site-packages=false,
and disabled user site. These are clean environments on this Windows machine,
not a fresh OS or a cold package cache.

Initial sandbox network attempts failed for PyPI/NuGet. The pip “no matching
distribution” text followed connection denial; the same requirements installed
successfully with allowed network access. Requirements/pins were not changed.
Standard pip caches could be reused. The observed NuGet package SHA-256 and source
URL are recorded, without representing the hash as independent publisher proof.

Python 3.10 conditional dependencies differ (including tomli/exceptiongroup and
an older compatible platformdirs). The Windows/3.13 lock was not imposed on 3.10;
both used requirements.txt as README instructs.

[Setup outputs](verification/stage_9_setup.json) retain failed and successful attempts.

## Actual checks and commands

| Check | Windows CPython 3.13.17 | Windows CPython 3.10.11 |
| --- | --- | --- |
| Full pytest/coverage | 271 passed, one skipped; 22.69 s | 271 passed, one skipped; 22.53 s |
| Black --check | Exit 0; 24 files unchanged | Exit 0; 24 files unchanged |
| isort --check-only | Exit 0 | Exit 0 |
| flake8 | Exit 0; no errors | Exit 0; no errors |
| Strict mypy | Exit 0; 24 files | Exit 0; 24 files |
| pip check | Exit 0 | Exit 0 |
| Five documented CLI examples | All exit 0 | All exit 0 |

Executed quality commands are the exact README commands with the new venv's
interpreter. CLI examples cover help, the specified sequential glossary command,
adaptive python_basics, seeded random export, and authorized overwrite.
Explicit venv interpreter paths are the README-supported alternative to activation.

Default HOME/USERPROFILE was isolated. Inputs were scripted sample backs; in the
random example that stream does not guarantee correct answers after shuffling.
Wrong answers alone correctly return zero. Final overwrite export has 10 correct
and only the agreed metadata/statistics/missed-card schema. No student quiz answers
or personal study history were used.

[3.13 command outputs](verification/stage_9_checks_313.json),
[3.10 command outputs](verification/stage_9_checks_310.json), and
[CLI transcripts/dependency snapshots](verification/stage_9_commands.json)
preserve actual results.

The documented PowerShell script also ran in the clean 3.13 copy with
-SkipInteractive. Expected status markers were sequential/adaptive/random 0,
EOF 1, conflict 2, corrupt-history 1, export failure/refusal 1, and authorized
overwrite 0; refusal preserved bytes. [Its full output](verification/stage_9_manual_script.json)
is saved. Physical Ctrl+C was intentionally not performed.

## Coverage configuration and results

Both runtimes produced identical instrumented counts:

| Measure | Covered / total | Percent |
| --- | ---: | ---: |
| Statements | 590 / 599 | 98.50% |
| Branch outcomes | 120 / 124 | 96.77% |
| Combined coverage.py total | 710 / 723 | 98.20% |

Combined is `(590 + 120) / (599 + 124)`, not the branch-only percentage.
Nine statement lines and four branch outcomes are missing; four branches are partial.

The unchanged configuration includes all 11 production Python modules, including
main.py. Only tests/local tools/environments are omitted; the combined gate remains
81%, strictly above 80%. No exclusions, assertions or lint/type rules were weakened.
Historical Stage 2 zero-statement coverage is not submission evidence.

[3.13 raw coverage](verification/stage_9_coverage_313.json),
[3.10 raw coverage](verification/stage_9_coverage_310.json), and
[derived figures](verification/stage_9_metrics.json) retain full data.
Uncovered defensive export inspection/encoding/cleanup and terminal/finalization
fallbacks remain as documented in Stage 8; optional coverage additions were not made.

## Available-criterion audit

These rows map the supplied assignment/request, not an unseen classroom rubric.

| Available criterion | Finding and repository evidence |
| --- | --- |
| Load JSON flashcards | Pass: loader tests and both actual sample CLI runs |
| Validate structure, required fields and values | Pass: malformed/empty/type/blank/duplicate tests in test_data_loader.py |
| Graceful missing/unreadable/malformed input | Pass: structured loader errors and actual-entry-point error tests |
| Present fronts and read text answers | Pass: terminal module, native CLI transcripts and integration tests |
| Case-insensitive comparison | Pass: strip/casefold tests; internal spacing/punctuation retained |
| Immediate Correct/Incorrect feedback | Pass: terminal tests/transcripts; expected answer displayed after misses |
| Sequential, random and adaptive modes | Pass: all modes ask each card once; seeded membership/source-preservation tests and stable adaptive ties |
| Final table: questions/accuracy/missed terms | Pass: zero/partial/complete summaries and original-position misses |
| Minimum Python 3.10 | Runtime verified on Windows CPython 3.10.11, separately from static checks; not every patch/platform |
| Standard pip/venv | Pass: fresh setup via documented commands on both interpreters |
| Modular architecture/thin main.py | Pass: 11 production modules, three-statement entry point; engine remains independent of I/O/storage |
| Strategy Pattern/extensibility | Pass: QuizStrategy Protocol and strategies; extension/permutation tests |
| Type hints/docstrings | Pass: strict mypy plus AST audit of every named source/test function, with implicit self/cls; embedded bootstrap strings are separate |
| Readability/style | Black/isort/flake8 pass; 88-column/Black-compatible E203 exception unchanged |
| pytest normal/edge/error behavior | Pass: 271 tests per interpreter; one explicitly unavailable symlink case |
| Coverage above 80% across production | Pass: all modules included; measured figures above; no test-code inflation |
| Dependency inspection/minimal runtime | Pass: runtime imports standard library/local modules; declared dev tools installed in new environments |
| Persistent adaptive history | Pass: error balance, cross-deck identity, fixed ordering, round-trip and retry tests |
| Seeded randomness | Pass: repeatable local seeded behavior and source-copy tests; no changed-shuffle assumption |
| Optional JSON export | Pass: metadata/statistics/misses only; byte-preserving refusal, explicit atomic overwrite and competing-destination tests |
| Completed-answer history in every mode | Pass: partial sessions and every-mode integration tests |
| Independent failures/interruption | Pass for tested scenarios: F1/F2 regressions, uncertain writes before/after real replacement, terminal/shutdown failures, status 130 precedence |
| Distinct deck/history/export paths | Pass for resolved names and actual hard links; actual symlink remains unavailable |
| Required source/data/tests/configuration | Present, validated, and unchanged against the tested snapshot |
| README setup/features/usage/verification | Clean reproduction succeeds; factual status updated afterward |
| Five detailed real AI examples | Nine grouped stage entries with actual requests/decisions/corrections; not fictional exchanges or chat-turn counts |
| Official-template report and length | Current draft: 1,253 rendered words / 1,300 raw tokens; headings retained; footer conflict noted; wording still awaits review |
| Relative file links | Application README/report/docs pass; three inherited root placeholders fail |
| Credentials/env/cache/personal-state exclusion | Current candidate passes filename/pattern/artifact scan; see limitations below |
| Generic three additions beyond CRUD | Additions were agreed and implemented; rubric sufficiency remains unverified |
| Full classroom compliance | Cannot certify: full rubric unavailable |

[Structured criteria/evidence](verification/stage_9_criteria.json) and
[final document validation](verification/stage_9_report_validation.json) retain
the file checks, heading/word-count checks and links.

## Submission hygiene and source provenance

The candidate selection includes modified/untracked implementation files; it is
not a git archive of the untouched starter commit. Ignored .venv/.tools/caches,
generated coverage directories, results and conventional personal-history paths
are excluded. Those local artifacts still physically exist; this audit did not
delete them or claim that an indiscriminate folder zip would exclude them.

No credential filenames or recognizable private-key/API-token patterns were
detected. This bounded scan cannot prove absence of arbitrary secret strings.
Synthetic scores/answers in tests and evidence, the student's supplied name and
local/temp paths are intentional documentation, not personal learning state.
.env and private.key ignore probes fail, so optional ignore hardening is explicit.

[Repository hygiene](verification/stage_9_repository_hygiene.json) records scan
scope and ignore rules; [final inventory](verification/stage_9_submission_inventory.json)
records eligible paths. Match values are not printed.

Both samples retain their original bytes/content through the audit: a 10-card array
and an 8-card cards wrapper. They validate without blank or duplicate pairs.
Samples and the official template have no Git diff against HEAD.
[Source/sample records](verification/stage_9_samples_and_source.json) also show
HEAD unchanged at the initial starter commit. The
[before/after source manifest](verification/stage_9_manifest.json) confirms unchanged
application, tests, dependencies, configuration, samples and template.

## Symlink investigation and remaining verification

Actual creation failed with WinError 1314 in the native probe and both full suites.
A targeted outside-sandbox attempt first failed during pytest setup because that
context could not use existing temp/cache directories. A fresh isolated basetemp
and disabled cache fixed the fixture issue: one hard-link case passed, one symlink
case still skipped with WinError 1314. No Windows settings/privileges were changed.
[Probe](verification/stage_9_alias_probe.json) and
[follow-up](verification/stage_9_alias_followup.json) preserve these outcomes.
Neither a simulated resolve test nor a hard link is labeled symlink verification.

Physical Ctrl+C remains unverified. The shortest interactive PowerShell check,
from project/starter, is:

```powershell
$quizTemp = Join-Path $env:TEMP ([guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe main.py -f data/glossary.json --history "$quizTemp\history.json" --export "$quizTemp\session.json"
$LASTEXITCODE
```

Press Enter once for a blank completed answer, then Ctrl+C at the second prompt.
Run the final line immediately at the returned prompt. Expected: 130, a partial
one-incorrect-answer summary, and history/session files under the unique temp path.
Do not record this as passed until the student performs it and reports results.

The full rubric remains unavailable. Other Python patches/platforms and an OS-level
clean machine were not tested. Final report wording is still pending student review.

## Documentation and stop boundary

README/environment/report facts now reflect actual Stage 9 results. Personal
learning/reflection text and all four student ratings are unchanged; the ratings
are contextualized as supplied at Stage 8. The report remains a draft.
[Documentation differences](verification/stage_9_documentation_updates.json)
make factual updates reviewable without inventing new personal opinions.

The existing Stage 8 entry records actual acceptance with the report-wording
qualification; the Stage 9 entry records setup failures, fixture/helper corrections,
results, gaps and this stop. Historical evidence remains intact.

**Stop with these findings. No application changes, commit, push or submission.**

