# Agent Instructions

This is the root instruction file for all AI agents working in this repository.

## Universal Rules

1. **Read before writing.** Always read existing files before modifying them.
2. **Respect ownership.** Only modify files within your role's scope as defined in `OWNERS.yaml`.
3. **Follow the plan.** Check `.planning/plans/` for the current plan and work within its scope.
4. **Small PRs.** Each PR should correspond to one planned PR unit. Do not combine multiple units.
5. **No context pollution.** Do not load files outside your ownership scope unless extracting read-only context.
6. **Validate before pushing.** Run `make validate-planning` for planning changes; run project-specific checks for code changes.
7. **Preserve patterns.** Match the style, conventions, and patterns of existing code in each project.

## Project Index

| Project | Path | Stack |
|---------|------|-------|
| web-game | `projects/web-game/` | TypeScript, React, Vite, Vitest |
| mobile-game | `projects/mobile-game/` | Kotlin, Android, JUnit 5 |
| api | `projects/api/` | Go, golangci-lint |
| analytics | `projects/analytics/` | Python, ruff, pytest |
| infra | `projects/infra/` | Terraform, tflint, tfsec |

Each project has its own `CLAUDE.md` with project-specific instructions.

## Agent System

See `docs/agents/overview.md` for a complete description of the agent collaboration system,
including the PR stage model and context extraction.

### Phase 1 Active Personas

Four personas are active in Phase 1. See `docs/agents/personas/` for full definitions:
- `tech-lead.md` -- Tech Lead (+ Architect + Security Engineer in Phase 1)
- `acceptance-tester.md` -- Acceptance Tester
- `developer.md` -- Developer (+ DevOps + Operator + Unit Tester in Phase 1)
- `scrum-master.md` -- Scrum Master

The Product Manager role is filled by the human user.

## Work Cycle Documentation

See `docs/agents/work-cycles/` for work cycle documentation:
- `planning.md` -- Planning work cycle
- `verification.md` -- Verification work cycle
- `implementation.md` -- Implementation work cycle
- `accept.md` -- Accept work cycle
- `improve.md` -- Improve work cycle

## Planning Context

Never read `.planning/` files in full. Use `scripts/planning/extract-context.py` to get
a filtered summary relevant to your persona and current task.

## Guardrails

All PRs must pass:
- Ownership check (`scripts/ownership/check.py`)
- Schema validation for `.planning/` changes
- Project-specific linting, type checking, and tests
- Coverage thresholds defined in `guardrails/`
