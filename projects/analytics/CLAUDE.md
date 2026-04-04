# Analytics - Agent Instructions

## Project Overview

Analytics event processing service using Python.

## Key Files

- `src/` -- application source code
- `tests/unit/` -- unit tests (pytest)
- `tests/integration/` -- integration tests
- `tests/e2e/` -- end-to-end tests

## Patterns and Conventions

- Use ruff for linting and formatting
- pytest for all testing
- coverage.py for coverage reporting
- Type hints required on all public functions

## Build and Test

```bash
pip install -e ".[dev]"   # Install
pytest                     # Test
ruff check .               # Lint
```
