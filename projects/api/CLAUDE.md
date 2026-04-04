# API - Agent Instructions

## Project Overview

High score and game state API using Go.

## Key Files

- `src/` -- application source code
- `tests/unit/` -- unit tests (go test)
- `tests/integration/` -- integration tests
- `tests/e2e/` -- end-to-end tests

## Patterns and Conventions

- Follow Go standard project layout
- Use golangci-lint for code quality
- Table-driven tests preferred
- Standard library `net/http` unless complexity warrants a framework

## Build and Test

```bash
go build ./...        # Build
go test ./...         # Run tests
golangci-lint run     # Lint
```
