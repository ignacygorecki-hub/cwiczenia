[![CI](https://github.com/ignacygorecki-hub/cwiczenia/actions/workflows/ci.yml/badge.svg)](https://github.com/ignacygorecki-hub/cwiczenia/actions/workflows/ci.yml) [![Coverage](https://codecov.io/gh/ignacygorecki-hub/cwiczenia/branch/main/graph/badge.svg)](https://codecov.io/gh/ignacygorecki-hub/cwiczenia)

# python-project

Minimal Python project scaffold created by GitHub Copilot.

## Structure

- `src/` - project source
- `tests/` - tests

## Usage

Create a virtual environment, install dependencies, and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m src.main
```

Run tests locally:

```powershell
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt pytest
.\.venv\Scripts\python -m pytest -q
```

## CI

A GitHub Actions workflow runs `pytest` on pushes and pull requests to `main`. Check the badge at the top of this file to see the build status.

## Docker

A minimal Docker image is provided via the `Dockerfile` in the project root. Build and run with:

```bash
docker build -t python-project:latest .
docker run --rm python-project:latest
```

> Note: you can add any system deps required by extra packages to `Dockerfile`.

---

If you want, I can add a coverage badge, a README example, or expand the contributing section.
