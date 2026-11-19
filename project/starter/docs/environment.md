# Stage 2 environment and baseline

Date: 2026-11-18. Historical Stage 2 setup/baseline snapshot, now accepted by the
user. Application implementation had not begun at that baseline. For current
implementation and verification, see [final_rubric_audit.md](final_rubric_audit.md).
Run commands from `project/starter`.

**Stage 9 update:** Separate clean submission copies and new venvs passed setup,
the full suite and quality commands on Windows CPython 3.10.11 and 3.13.17.
See [the final audit](stage_9_audit.md) and its saved outputs. The paragraphs below
describe the original Stage 2 baseline; their then-pending runtime/reproduction
checks are now resolved only for those two Windows interpreter versions.

## Interpreter and virtual environment

Actual tested interpreter: **64-bit CPython 3.13.17 on Windows**. Pip is 26.2.2.
The initial `python`/`python3` commands resolved to unusable WindowsApps aliases;
the `py` launcher was absent. Checked common Python installation directories and
PythonCore registry locations; no existing usable interpreter was found there.

Downloaded the [official CPython NuGet package](https://docs.python.org/3/using/windows.html#the-nuget-org-packages)
for 3.13.17, extracted it under ignored `.tools/python.3.13.17/`, and used its
`tools/python.exe` to create a standard `.venv`. NuGet here supplies only the
bootstrap interpreter; dependency installation uses standard pip, not a NuGet
project or dependency workflow. No global PATH or registry changes were needed.

The application still targets Python 3.10+ syntax. The seven direct tool pins
were selected with a pip dry-run resolution targeting Python 3.10, because the
newest coverage and flake8 releases required 3.11. That is metadata/resolver
evidence, **not execution on Python 3.10**. Only 3.13.17 has actually run here.
Fresh-environment reproduction remains Stage 9 work.

### Setup with an existing usable Python installation

Use CPython 3.13.17 to match this tested environment. From `project/starter`:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

For the exact Windows/3.13 dependency snapshot, install `requirements-lock.txt`
instead. It includes transitive packages; it is not a platform-independent lock.
Other interpreters/platforms should use `requirements.txt` so pip can resolve
appropriate conditional dependencies. Neither file contains runtime dependencies
for the planned quiz application.

### Project-local bootstrap used on this machine

Use this alternative if Windows aliases prevent `python` from running. Start in
`project/starter`; do not re-extract over an existing installation.

```powershell
New-Item -ItemType Directory -Force -Path .tools | Out-Null
Invoke-WebRequest -Uri 'https://api.nuget.org/v3-flatcontainer/python/3.13.17/python.3.13.17.nupkg' -OutFile '.tools/python.3.13.17.zip' -UseBasicParsing
Expand-Archive -LiteralPath '.tools/python.3.13.17.zip' -DestinationPath '.tools/python.3.13.17'
& '.\.tools\python.3.13.17\tools\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

The actual archive SHA-256 is recorded in `verification/stage_2_followup.json`
for reproducibility; it is a locally observed digest, not separate proof of
publisher authenticity. Network access was required for the download and pip.

Activation with `.\.venv\Scripts\Activate.ps1` is optional. Explicit interpreter
paths work without changing PowerShell execution policy. Once activated,
`python` means the venv interpreter and the assignment's plain `python main.py`
commands can be used later. Recreate the venv rather than copying it between
machines or moving the bootstrap installation it depends on.

## Configuration and dependencies

| File | Responsibility |
| --- | --- |
| `requirements.txt` | Seven pinned direct development tools: pytest, pytest-cov, coverage, Black, flake8, isort, mypy |
| `requirements-lock.txt` | Actual installed transitive dependency snapshot for Windows/CPython 3.13.17 |
| `pyproject.toml` | Black/isort style, strict mypy, pytest discovery, coverage scope/threshold/subprocess capture |
| `.flake8` | 88-character limit and the narrow Black-compatible E203 exception |
| `.gitignore` | Excludes interpreter/venv, caches, generated coverage, and conventional personal state/export directories |

Removed unused direct Sphinx/theme, pre-commit, bandit, safety, requests, click,
and pydantic declarations from the starter. No application behavior needs them.
Click is still installed transitively by Black; that does not introduce Click
as an application dependency. Existing source imports were inspected before
installation: all three Python files contained only docstrings.

Black and isort use 88 columns; isort uses Black's profile. Flake8 retains its
correctness checks and adds only `E203` as a style exception for Black's slice
formatting. Mypy is strict and targets Python 3.10 syntax. No missing-import
suppression or production-code exclusions were added to make checks pass.

Coverage includes `main.py` and all production modules via `source = ["."]`.
Only tests and local tool/environment directories are omitted. Branch coverage
is enabled. The 81% gate is deliberately stronger than strictly above 80%; it
does not accept a rounded 80% result. Subprocess capture is configured through
[coverage's subprocess patch](https://coverage.readthedocs.io/en/latest/subprocess.html#subprocess),
so future entry-point integration tests can contribute coverage. It has been
parsed successfully but is not yet validated with application integration tests.

## Actual baseline results

Raw output and exit codes: [initial baseline](verification/stage_2_baseline.json)
and [isort/config follow-up](verification/stage_2_followup.json).
Each `python` below was the explicit `.venv/Scripts/python.exe`, not the broken
global alias. Native stdout/stderr and exit statuses were captured independently.

| Executed command | Result | Meaning |
| --- | --- | --- |
| `python -m pip check` | Exit 0; no broken requirements | Installed dependency consistency passed |
| `python -m pytest` | Exit 5; collected 0 items | Starter has no tests; not a passing test suite |
| `python -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json` | Exit 5; no tests/no collected data | Tool printed 100% over **zero statements**; not meaningful coverage evidence |
| `python -m black --check .` | Exit 0; 3 files unchanged | Starter placeholders meet formatting |
| `python -m isort --check-only .` | Initial exit 0 with warnings; follow-up exit 0 with empty stderr | See setup refinement below |
| `python -m flake8 .` | Exit 0; no output | No lint errors in placeholders |
| `python -m mypy .` | Exit 0; no issues in 3 files | Docstring-only files type-check; no application behavior checked |
| `python main.py --help` | Exit 0; no output | Placeholder does nothing; help is not implemented |
| `python main.py --mode sequential --file data/glossary.json` | Exit 0; no output | No quiz implementation; not functional success |

The coverage JSON lists `main.py` and `utils/__init__.py`, each with zero
executable statements. The reported percentage is vacuous; do not use it as
submission evidence for the >80% requirement. The JSON retains the no-data
warning and pytest's nonzero status rather than claiming a pass.

Initial isort scanned extensionless `.claude/commands/*` instruction documents
and emitted encoding/parser warnings. Added `.claude` to isort's explicit skip
list; those files are non-Python agent configuration. Retesting isort was clean.
The initial output is retained. No source formatting changes or fake tests were
introduced to hide starter gaps or remove warnings.

## Commands for ongoing work

After adding real application code and tests in later stages:

```powershell
.\.venv\Scripts\python.exe -m pytest --cov=. --cov-report=term-missing --cov-report=html --cov-report=json
.\.venv\Scripts\python.exe -m black --check .
.\.venv\Scripts\python.exe -m isort --check-only .
.\.venv\Scripts\python.exe -m flake8 .
.\.venv\Scripts\python.exe -m mypy .
```

In TypeScript terms, the venv is a project-local tool environment, and
`python -m pip` selects pip belonging to that interpreter. `requirements.txt`
resembles pinned direct `devDependencies`; the platform-specific freeze records
the transitive environment too. Type annotations and successful mypy checks do
not replace runtime JSON validation or behavior tests.

Review the dependency reduction, the single lint-style exception, coverage scope,
and distinction between setup success and missing starter functionality. Stage 2
adds no application functions or tests; stop for review before Stage 3.
