# Mobile Game

Android Minesweeper app built with Kotlin.

## Stack

- **Language:** Kotlin
- **Platform:** Android
- **Test Framework:** JUnit 5
- **Linter:** ktlint + detekt
- **Coverage:** JaCoCo

## Development

```bash
# Build
./gradlew build

# Run tests
./gradlew test

# Lint
./gradlew ktlintCheck detekt
```

## Directory Structure

```
mobile-game/
├── src/           # Application source code
├── tests/
│   ├── unit/          # Unit tests
│   ├── integration/   # Integration tests
│   └── e2e/           # End-to-end tests
└── docs/          # Project-specific documentation
```
