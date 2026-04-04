# API

High score and game state API built with Go.

## Stack

- **Language:** Go
- **Linter:** golangci-lint
- **Test Framework:** go test
- **Coverage:** go tool cover

## Development

```bash
# Build
go build ./...

# Run tests
go test ./...

# Lint
golangci-lint run
```

## Directory Structure

```
api/
├── src/           # Application source code
├── tests/
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
└── docs/          # Project-specific documentation
```
