# Analytics

Analytics event processing service built with Python.

## Stack

- **Language:** Python
- **Linter:** ruff
- **Test Framework:** pytest
- **Coverage:** coverage.py

## Development

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .

# Coverage
pytest --cov
```

## Directory Structure

```
analytics/
├── src/           # Application source code
├── tests/
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
└── docs/          # Project-specific documentation
```
