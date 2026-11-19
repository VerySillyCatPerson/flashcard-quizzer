# Independent-review corrections — 2026-11-19

The user requested a portable excessive-nesting test and terminal control escaping,
with tests before production changes, actual Windows 3.10.11/3.13.17 verification,
preserved rules/assertions, factual documentation updates, and a review stop.
No commit, push, publication or submission is authorized.

## Nesting portability: reported versus observed

The reviewer reported that Linux/Python 3.12.14 decoded 5,000 nested arrays, then
correctly rejected the deck with "Card 1 must be a JSON object." That made the old
test's decoder-specific message assertion fail. This runtime was **not executed
here**. Before changing tests, the original test passed on both available Windows
runtimes; these are not reproduced Linux failures.

Split the contracts in tests/test_data_loader.py:

- test_decoder_recursion_error_becomes_nesting_load_error uses a temporary
  monkeypatch.context affecting json.loads only during the loader invocation.
  It requires the exact "JSON nesting is too deep." detail, original path and
  identical RecursionError cause. Loading the valid file after the context proves
  restoration. File I/O and structural validation are not mocked.
- test_excessive_json_nesting reads the real 5,000-deep file and requires
  FlashcardLoadError plus the source path, without choosing a decoder threshold
  or message. Decoder rejection and successful decoding followed by deck rejection
  both meet this contract.

The loader production code and its narrow exception boundaries are byte-identical.
All other loader assertions remain. The original baseline results and source are
retained in [the manifest](verification/independent_review_manifest.json).

## Terminal display: actual red then green

New tests in tests/test_terminal.py enumerate all 65 C0/DEL/C1 code points. Each
requires exact captured question/incorrect-feedback text and protected missed-card
summary text, including literal ESC/CSI representations. Other tests preserve
ordinary Unicode/emoji joiners and verify original fronts/backs, identity, correct
case-insensitive grading, rejection of a literal escaped substitute, history
increment/decay, and actual JSON export round-trip values.

Before editing utils/terminal.py, both runtimes reported **63 failed/7 passed**
terminal cases. The 62 previously unescaped controls and the domain/display
integration case failed; existing newline/carriage-return/tab and Unicode cases
passed. The two nesting tests passed. [3.10 red](verification/independent_review_red_310.json)
and [3.13 red](verification/independent_review_red_313.json) preserve complete outputs.
The manifest proves production was unchanged through this red phase.

The only production change is _one_line: a translation map escapes C0/DEL/C1 to
literal backslash-x hexadecimal, retaining backslash-n/r/t conventions. Ordinary
Unicode passes through. Existing calls already protect fronts in questions and
summaries and backs in incorrect feedback. No model, loader, engine, history,
identity or export code changed. Tests capture StringIO/subprocess output; hostile
terminal sequences were not emitted to the interactive console.

## Actual final checks

| Check | Windows Python 3.10.11 | Windows Python 3.13.17 |
| --- | --- | --- |
| Original nesting baseline | 1 passed | 1 passed |
| Revised nesting tests | 2 passed, 71 deselected | 2 passed, 71 deselected |
| Terminal tests after fix | 70 passed | 70 passed |
| Full pytest | 343 passed, 1 skipped; 22.80s | 343 passed, 1 skipped; 22.38s |
| Black / isort / flake8 / strict mypy / pip check | All exit 0 | All exit 0 |
| Extracted executable bootstrap flake8 | Exit 0 | Exit 0 |

[3.10 final output](verification/independent_review_green_310.json) and
[3.13 final output](verification/independent_review_green_313.json) contain every
actual command, runtime path, cwd, status and stream. These reuse the existing
isolated Windows environments against current source; they are not new clean
installs or Linux runs. Measurement uses the corresponding interpreter:

```powershell
python -m pytest -rs --cov=. --cov-report=term-missing --cov-report=html --cov-report=json:docs/verification/independent_review_coverage_310.json
```

The 3.13 run uses the analogous _313.json destination. All 11 production modules,
including main.py, are measured in both raw coverage files.

| Coverage | Covered / total | Percent |
| --- | ---: | ---: |
| Statements | 595 / 604 | 98.51% |
| Branch outcomes | 120 / 124 | 96.77% |
| Combined | 715 / 728 | 98.21% |

Combined is (595+120)/(604+124). Nine statements/four branch outcomes remain
uncovered in earlier defensive terminal/export/cleanup paths; no exclusions or
81% gate were changed. Original samples, template, dependencies and quality
configuration are unchanged. Existing unrelated assertions were not weakened.
The specifically invalid runtime-dependent nesting-message assumption is replaced
by the two stronger, separate contracts above.

## User acceptance and remaining limits

The student accepted these corrections and factual documentation updates on
2026-11-19 based on reported evidence. Earlier report approval is preserved.
They requested no further implementation or audit cycle.
Reflections, rating values/reasons and masked name remain unchanged. Actual
symlink behavior is still privilege-blocked (WinError 1314); hard links are separate
evidence. Physical Ctrl+C remains unverified. Expected warning/path messages are
outside this card-text escaping change; control escaping is not a general Unicode
spoofing policy or a guarantee for arbitrary third-party renderers of exported JSON.
No commit, push, publication or submission. Work stopped as requested.
