# Minesweeper Monorepo

An example monorepo demonstrating how a team of specialized AI agents can collaborate to build and iterate on a large-scale project. The application is a **Minesweeper game** implemented across multiple platforms and languages, with supporting backend services and infrastructure.

## Repository Structure

```
/
├── .github/workflows/          # CI and loop orchestration workflows
│   └── reusable/               # Shared workflow templates
├── projects/
│   ├── web-game/               # TypeScript (React + Vite)
│   ├── mobile-game/            # Kotlin (Android)
│   ├── api/                    # Go
│   ├── analytics/              # Python
│   └── infra/                  # Terraform (AWS)
├── contracts/
│   ├── openapi/                # High score API spec
│   └── events/                 # Analytics event schemas
├── docs/
│   ├── architecture/           # System architecture, ADRs
│   ├── security/               # Threat model, security policies
│   ├── agents/                 # Persona definitions and loop docs
│   │   ├── personas/
│   │   └── loops/
│   └── guides/                 # Onboarding and how-to guides
├── .planning/
│   ├── schemas/                # JSON Schemas for ticket + plan YAML
│   ├── backlog/                # Ordered product backlog
│   ├── active/                 # Active plans with status
│   ├── completed/              # Archived work
│   └── templates/              # YAML templates
├── scripts/
│   ├── planning/               # validate, render, extract-context
│   ├── ownership/              # OWNERS.yaml enforcement
│   └── guardrails/             # coverage, docs, architecture checks
├── guardrails/                 # Shared thresholds (coverage, linting, etc.)
├── CLAUDE.md                   # Root agent instructions
├── OWNERS.yaml                 # File/folder ownership per role
├── Makefile                    # Top-level task runner
└── PLAN.md                     # Development plan
```

## Projects

| Project | Language | Description |
|---------|----------|-------------|
| web-game | TypeScript | Browser-based Minesweeper (React + Vite) |
| mobile-game | Kotlin | Android Minesweeper app |
| api | Go | High score and game state API |
| analytics | Python | Analytics event processing |
| infra | Terraform | AWS infrastructure |

## Agent Roles (Phase 1)

| Role | Scope |
|------|-------|
| Tech Lead | Technical plans, architecture, security, ADRs, contracts |
| Acceptance Tester | Integration and E2E tests |
| Developer | Application code, CI/CD, unit tests, operations |
| Scrum Master | Agent definitions, workflows, process improvement |
| Product Manager | Product backlog and priorities (human) |

## Development Loops

1. **Planning** -- ticket assessment, architecture, security review, technical planning
2. **Verification** -- failing acceptance tests (TDD), build/CI setup
3. **Implementation** -- code, CI updates, unit tests, operational readiness
4. **Accept** -- security, architecture, plan adherence, and test adequacy review
5. **Improve** -- retrospective, process improvements, updated agent definitions

## Quick Start

```bash
make validate-planning    # Validate .planning/ YAML files
make check-ownership      # Verify file ownership against OWNERS.yaml
```

See `docs/guides/` for detailed onboarding instructions.
