# Approved F3 and bootstrap corrections — 2026-11-19

The student approved the proposed startup-interruption fix and eight bootstrap
docstring/spacing corrections, required test-first evidence and complete checks on
Python 3.10.11 and 3.13.17, and retained the report/manual-result review gates.
No commit, push, publication or submission was authorized.

## Actual regression-first evidence

Added to tests/test_finalization.py:

- test_startup_interrupt_retains_130_when_warning_output_fails, parametrized as
  healthy, restored_pipe and permanent_pipe. Each runs main.py through the
  test-only bootstrap. Closed-pipe cases use the real warning printer and OS pipe.
  All require 130, no expected-error/shutdown traceback, no quiz output, unchanged
  deck and no pre-quiz default history/export.
- test_startup_interrupt_does_not_hide_warning_programming_errors requires a
  visible RuntimeError traceback and status 1. This deliberately unexpected error
  must not become an expected terminal failure.

Before editing utils/cli.py, both runtimes reported **two failed, two passed**:
healthy and programming-error controls passed; restored/permanent pipes failed
because status was 1 rather than 130. [3.10 red](verification/f3_red_310.json) and
[3.13 red](verification/f3_red_313.json) preserve commands and complete output.
The [manifest](verification/f3_manifest.json) proves production hash equality
between the initial and red phases, and retains initial/red/final source text.

## Small correction and ownership

utils/cli.py's startup KeyboardInterrupt handler now catches only
terminal.TerminalOutputError around terminal.warn, then returns 130. Other
exceptions remain visible. The terminal module still owns expected write/flush
translation and descriptor retirement. The engine/history/export are unchanged;
this pre-quiz path has no completed answers to save or export. Existing independent
finalization, uncertain-write and overwrite regressions remain in the full suite.

Added docstrings to controlled_input, fail_history, fail_read, denied_read,
denied_identity, denied_home, interrupted_export and interrupted_summary inside
tests/cli_helpers.py::_BOOTSTRAP. Added the required blank lines at the eight
original lint violations. Two new documented fault hooks exercise the warning
cases; all **16 embedded functions** now have docstrings. Normal checks parse the
outer module, so the extracted string is additionally passed to flake8 on stdin
with display name tests/cli_helpers_bootstrap.py, using the existing configuration.
No extra source module, lint suppression or rule change is introduced.

## Actual complete verification

These runs use the previously created isolated Windows environments against the
current working tree, not another clean-install reproduction. Saved commands name
their actual interpreter and cwd.

| Check | Python 3.10.11 | Python 3.13.17 |
| --- | --- | --- |
| Focused F3 regressions | 4 passed, 9 deselected | 4 passed, 9 deselected |
| Full pytest | 275 passed, 1 skipped; 22.56s | 275 passed, 1 skipped; 22.99s |
| Black / isort / flake8 / strict mypy | All exit 0 | All exit 0 |
| pip check | Exit 0 | Exit 0 |
| Extracted-bootstrap flake8 | Exit 0 | Exit 0 |
| Embedded missing docstrings | None | None |

[3.10 complete results](verification/f3_green_310.json) and
[3.13 complete results](verification/f3_green_313.json) preserve actual output.
Both [3.10 coverage](verification/f3_coverage_310.json) and
[3.13 coverage](verification/f3_coverage_313.json) include all 11 production modules:

| Measurement | Covered / total | Percent |
| --- | ---: | ---: |
| Statements | 593 / 602 | 98.50% |
| Branch outcomes | 120 / 124 | 96.77% |
| Combined | 713 / 726 | 98.21% |

Combined is (593+120)/(602+124). Nine statement lines/four branch outcomes remain
uncovered in defensive output, export and cleanup paths. No additional optional
coverage work was added. The same privilege-blocked symlink test is skipped with
WinError 1314; hard links do not establish symlink behavior.

The manifest proves only utils/cli.py, tests/cli_helpers.py and
tests/test_finalization.py changed among the 31 protected files. Formatter, lint,
typing and coverage configurations, dependencies, main.py, original samples and
official template are byte-identical. No existing assertion was weakened.

## Current review boundary

**Later user acceptance — 2026-11-19:** The student accepted F3/bootstrap
corrections based on the reported regression evidence, and authorized factual
self-assessment/SUB1 documentation updates while preserving rating values and
historical log entries. Final report approval and physical Ctrl+C remain pending.

The five previously nonpassing mandatory criteria are corrected on this evidence;
the current matrix is 39 PASS with no confirmed mandatory gap. This does not
establish correctness on all inputs/platforms or final report approval.
Physical Ctrl+C, actual symlinks and final report wording remain unverified or
pending, with the first and last still the student's readiness gates. Concurrent
sessions, forced termination and uncertain-write limitations remain documented.
Stop for review. No commit, push, publication or submission.

**Final report approval — 2026-11-19:** The student has now approved report wording
and requested masking the name. Physical Ctrl+C remains pending; symlinks remain
unverified. Earlier pending statements above describe their historical review date.
