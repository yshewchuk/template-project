# Minesweeper Monorepo: AI Agent Team Example

## Vision

This repository serves as an example monorepo demonstrating how a team of specialized AI agents can collaborate to build and iterate on a large-scale project. The example application is a **Minesweeper game** implemented across multiple platforms and languages, with supporting backend services and infrastructure.

The core hypothesis: by providing agents with the right scaffolding -- hierarchical documentation, objective guardrails, structured planning artifacts, and well-defined workflows -- a team of AI agents with conflicting specialized roles can deliver incremental, high-quality changes with minimal human steering.

### Success Criteria

The primary measure of success is **how little manual direction is needed from the user**. Specifically:

- The user writes tickets describing *what* they want (not *how*)
- Agents autonomously break down, plan, implement, test, and review changes
- The user reviews PRs and occasionally adjusts processes
- Over time, low-risk PRs are auto-approved and the human only reviews high-risk changes

### Key Problems This Aims to Solve

1. Agents don't break problems into small vertical slices -- reviewers face large, hard-to-review PRs
2. Large changes cause expensive back-and-forth that fills agent context windows
3. Agents ignore existing patterns and architecture, implementing the easiest path
4. Agents don't account for long-term plans, causing naive implementations
5. Iteration loops are expensive because each round starts with accumulated context debt

---

## The Example Application: Minesweeper

**Minesweeper** is a single-player logic game played on a rectangular grid of cells. Some cells contain hidden mines. The player reveals cells one at a time:

- A revealed cell shows a number indicating how many of its 8 neighbors contain mines
- A blank cell (0 adjacent mines) automatically reveals its neighbors
- The player can flag cells they believe contain mines
- Revealing a mine ends the game
- Revealing all non-mine cells wins the game

Standard difficulty levels: Beginner (9x9, 10 mines), Intermediate (16x16, 40 mines), Expert (16x30, 99 mines).

This game was chosen because it has well-known semantics, enough complexity to exercise real architecture (game state, timers, scoring, configuration), and the rules can be extended with curveball variants to simulate evolving real-world requirements.

---

## Repository Structure

```
/
+-- .github/
|   +-- workflows/
|       +-- ci-web-game.yml           # Path-filtered CI for web-game
|       +-- ci-mobile-game.yml        # Path-filtered CI for mobile-game
|       +-- ci-api.yml                # Path-filtered CI for api
|       +-- ci-analytics.yml          # Path-filtered CI for analytics
|       +-- ci-infra.yml              # Path-filtered CI for infra
|       +-- on-pr-merge.yml           # Coordination: determine next agent after merge
|       +-- on-pr-iterate.yml         # Coordination: determine next agent during review
|       +-- reusable/
|           +-- lint-and-test.yml     # Shared CI template
|           +-- agent-invoke.yml      # Shared agent invocation template
|
+-- CLAUDE.md                         # Root-level Claude Code instructions (source of truth)
|
+-- projects/
|   +-- web-game/                     # TypeScript (React + Vite)
|   |   +-- CLAUDE.md
|   |   +-- README.md
|   |   +-- docs/
|   |   +-- package.json
|   |   +-- tsconfig.json
|   |   +-- vitest.config.ts
|   |   +-- eslint.config.js
|   |   +-- src/
|   |
|   +-- mobile-game/                  # Kotlin (Android)
|   |   +-- CLAUDE.md
|   |   +-- README.md
|   |   +-- docs/
|   |   +-- build.gradle.kts
|   |   +-- app/
|   |
|   +-- api/                          # Go
|   |   +-- CLAUDE.md
|   |   +-- README.md
|   |   +-- docs/
|   |   +-- go.mod
|   |   +-- cmd/
|   |   +-- internal/
|   |
|   +-- analytics/                    # Python
|   |   +-- CLAUDE.md
|   |   +-- README.md
|   |   +-- docs/
|   |   +-- pyproject.toml
|   |   +-- src/
|   |
|   +-- infra/                        # Terraform (AWS)
|       +-- CLAUDE.md
|       +-- README.md
|       +-- docs/
|       +-- main.tf
|       +-- modules/
|
+-- contracts/                        # Shared API specs and schemas
|   +-- openapi/
|   |   +-- api.yaml                  # High score API spec
|   +-- events/
|       +-- analytics.yaml            # Analytics event schemas
|
+-- docs/
|   +-- architecture/
|   |   +-- overview.md               # System architecture overview
|   |   +-- decisions/                # Architecture Decision Records (ADRs)
|   |   +-- diagrams/
|   +-- agents/
|   |   +-- overview.md               # How the agent team works
|   |   +-- personas/                 # Detailed persona definitions
|   |   |   +-- architect.md
|   |   |   +-- tech-lead.md
|   |   |   +-- developer.md
|   |   |   +-- acceptance-tester.md
|   |   |   +-- unit-tester.md
|   |   |   +-- security-reviewer.md
|   |   |   +-- devops-engineer.md
|   |   |   +-- operations-specialist.md
|   |   +-- workflows/
|   |       +-- ticket-lifecycle.md
|   |       +-- review-protocol.md
|   +-- guides/
|       +-- onboarding.md
|       +-- adding-a-project.md
|
+-- .planning/
|   +-- schemas/                      # JSON Schemas for all planning YAML files
|   |   +-- ticket.schema.json
|   |   +-- plan.schema.json
|   +-- backlog/                      # Tickets awaiting planning (YAML files)
|   +-- active/                       # Work in progress (plans + status tracking)
|   +-- completed/                    # Archived completed work
|   +-- templates/                    # Templates for tickets, plans, reviews
|       +-- ticket.template.yaml
|       +-- plan.template.yaml
|
+-- scripts/
|   +-- planning/                     # Scripts to work with planning YAML
|   |   +-- render-plan.py            # YAML to Markdown rendering
|   |   +-- validate.py               # Schema validation
|   |   +-- extract-context.py        # Extract subsets for agent context
|   |   +-- status-update.py          # Update plan status fields
|   +-- guardrails/
|       +-- check-coverage.sh         # Test coverage gate
|       +-- check-docs.sh             # Documentation coverage check
|       +-- check-architecture.sh     # Architectural fitness checks
|
+-- guardrails/
|   +-- coverage.yaml                 # Per-project coverage thresholds
|   +-- linting.yaml                  # Linting configuration pointers
|   +-- architecture.yaml             # Architectural constraints
|   +-- security.yaml                 # Security policy and checks
|
+-- Makefile                          # Top-level task runner
+-- README.md                         # Project overview and navigation
```

---

## Agent Personas

Each persona is defined as a reusable identity with specific goals, constraints, and review criteria. Personas are **not** tied to specific workflows -- they are skill sets that can be applied to any task.

### Single Source of Truth

Persona definitions live in one place: `docs/agents/personas/<name>.md`. These are the canonical definitions read by both humans and agents. When a GitHub Actions workflow invokes an agent, it reads the relevant persona file and passes it as part of the prompt. There is no duplication across platforms.

For Cursor users working manually, a minimal `.cursor/rules/global.mdc` points to these persona docs. It does not duplicate their content.

### Agent Priority Order

When work is available, agents operate in strict priority order (highest abstraction first). This ensures that the largest misalignments are surfaced as early as possible, before detailed work begins:

| Priority | Persona | Focus |
|----------|---------|-------|
| 1 | Architect | Long-term technical direction, system coherence |
| 2 | Tech Lead | Work decomposition, vertical slices, plan tracking |
| 3 | DevOps Engineer | Development processes, CI/CD, workflow management |
| 4 | Acceptance Tester | E2E tests from requirements (TDD) |
| 5 | Developer | Implementation per the plan |
| 6 | Unit Tester | Fine-grained correctness verification |
| 7 | Security Reviewer | Security audit of changes |
| 8 | Operations Specialist | Logging, monitoring, observability |

Only one agent is active at a time, operating on a stable codebase.

### The Personas

#### Architect (Priority 1)

**Goal:** Ensure the system's long-term technical health and coherence.

**Triggers:** New tickets merged to backlog, significant PRs touching multiple projects.

**Responsibilities:**
- Assess how new requirements fit into the existing architecture
- Write and update Architecture Decision Records (ADRs)
- Define and enforce module boundaries and dependency rules
- Review PRs for architectural consistency
- Maintain the architecture overview documentation

**Constraints:**
- Cannot implement features directly
- Must justify decisions in writing (ADRs)
- Must consider the full backlog when making architectural decisions

**Review Criteria:** Does this change respect module boundaries? Are dependencies flowing in the right direction? Is this consistent with existing ADRs? Will this approach scale to the known backlog?

#### Tech Lead (Priority 2)

**Goal:** Break work into small, reviewable, vertical slices and track progress.

**Triggers:** Architect completes assessment of a ticket, WIP limit has capacity.

**Responsibilities:**
- Decompose tickets into plans with ordered, small PRs
- Each PR should be a vertical slice (independently testable and reviewable)
- Track plan status and update planning artifacts
- Review developer PRs for adherence to the plan
- Ensure incremental progress is visible

**Constraints:**
- Cannot implement features directly
- Plans must result in PRs that are each < 400 lines of meaningful change
- Each PR in a plan must have a clear, testable outcome
- Must account for the architecture and long-term direction

**Review Criteria:** Does this PR match the plan? Is it a clean vertical slice? Is it small enough to review efficiently? Does it build incrementally on prior work?

#### DevOps Engineer (Priority 3)

**Goal:** Ensure development processes, CI/CD pipelines, and workflows run smoothly and efficiently.

**Triggers:** New projects added, CI failures, workflow changes needed.

**Responsibilities:**
- Maintain and improve CI/CD pipelines
- Optimize build times and caching strategies
- Manage GitHub Actions workflows for agent orchestration
- Ensure development environment consistency
- Monitor and improve the agent orchestration workflows themselves

**Constraints:**
- Cannot implement application features directly
- Changes to workflows must be tested before merge
- Must not break existing CI for any project

**Review Criteria:** Are CI pipelines efficient? Are workflows reliable and idempotent? Is caching effective? Are build times reasonable?

#### Acceptance Tester (Priority 4)

**Goal:** Ensure that user-facing requirements are verifiable through end-to-end tests.

**Triggers:** Tech lead merges a plan, unit tester completes test implementation.

**Responsibilities:**
- Write end-to-end / integration tests based on ticket requirements and plans (TDD -- tests are merged before they pass)
- Review unit test coverage to ensure fine-grained tests adequately cover the acceptance criteria
- Update test status as implementation progresses

**Constraints:**
- Tests must be written based on the ticket and plan, not the implementation
- Must not look at implementation code when writing acceptance tests
- Tests should be merged in a failing state and tracked to passing

**Review Criteria:** Do the acceptance tests cover the ticket's requirements? Are they testing behavior, not implementation? Is the unit test suite sufficient to give confidence in the acceptance criteria?

#### Developer (Priority 5)

**Goal:** Implement functional changes that satisfy the plan, following existing patterns and architecture.

**Triggers:** Acceptance tests are merged for a plan item.

**Responsibilities:**
- Implement code changes per the tech lead's plan
- Follow existing patterns and architecture (read ADRs and project docs first)
- Keep changes small and focused on a single PR from the plan
- Update planning artifacts with implementation status

**Constraints:**
- Must read project documentation and relevant ADRs before implementing
- Must follow the plan -- deviations require updating the plan first
- PRs must be small vertical slices as defined in the plan
- Must not write tests (that is the unit tester's job)

**Review Criteria:** Does the implementation match the plan? Does it follow existing patterns? Is it a clean, small change? Does it respect module boundaries?

#### Unit Tester (Priority 6)

**Goal:** Verify the fine-grained correctness of implementations through comprehensive unit tests.

**Triggers:** Developer PR passes tech lead and architect review.

**Responsibilities:**
- Write unit tests for newly implemented code
- Ensure tests cover edge cases, error paths, and boundary conditions
- Maintain test coverage above hard thresholds
- Aim for soft coverage targets

**Constraints:**
- Tests must be independent and deterministic
- Must not modify implementation code (only test code)
- Must achieve hard coverage thresholds; should aim for soft targets

**Review Criteria:** Are edge cases covered? Are tests independent and deterministic? Do they test behavior rather than implementation details? Is coverage at or above thresholds?

#### Security Reviewer (Priority 7)

**Goal:** Ensure that every change is secure by default.

**Triggers:** Developer PR passes tech lead and architect review.

**Responsibilities:**
- Review code changes for security vulnerabilities
- Check dependency updates for known CVEs
- Verify authentication/authorization patterns
- Ensure secrets are not hardcoded
- Review infrastructure changes for security misconfigurations

**Constraints:**
- Cannot approve a PR with known security issues (hard gate)
- Must provide specific, actionable feedback (not vague warnings)
- Must reference relevant security standards or CVEs

**Review Criteria:** Are there injection risks? Are dependencies safe? Are secrets properly managed? Does the infrastructure follow least-privilege? Are auth patterns correct?

#### Operations Specialist (Priority 8)

**Goal:** Ensure that everything built is observable, monitorable, and operationally sound.

**Triggers:** Developer PR passes reviews, infrastructure changes.

**Responsibilities:**
- Review changes for adequate logging and error reporting
- Ensure monitoring and alerting hooks are in place
- Verify health check endpoints exist for services
- Review infrastructure for operational readiness (backups, scaling, failover)
- Ensure runbooks and operational documentation are maintained

**Constraints:**
- Cannot implement application features directly
- Must provide specific operational requirements, not vague suggestions
- Recommendations must be proportional to the service's criticality

**Review Criteria:** Is there adequate logging? Are errors reported with sufficient context? Are health checks in place? Can this be debugged in production? Is there a runbook?

---

## Orchestration: How Agents Coordinate

### Platform: Claude Code via GitHub Actions

The system uses **Claude Code** (`anthropics/claude-code-action`) as the single orchestration platform. This avoids the maintenance burden and drift risk of supporting two platforms with different instruction formats.

Key reasons for this choice:
- Native GitHub Actions support with the `prompt` input for automation mode
- Hierarchical `CLAUDE.md` files for context scoping (loaded automatically per working directory)
- Well-documented with many public examples (good for agent learnability)
- Cost controls via `--max-budget-usd` and `--max-turns` flags

Cursor can still be used for ad-hoc manual work. A minimal `.cursor/rules/global.mdc` file points to the canonical persona docs in `docs/agents/personas/` so manual Cursor users have access to the same instructions.

### Two Coordination Workflows

Rather than a separate workflow per agent, there are two coordination workflows that determine which agent acts next:

**`on-pr-merge.yml`** -- Triggered when any PR merges. It inspects what changed and what state the planning system is in, then invokes the highest-priority agent that has work to do:
- If a ticket was merged to backlog -> invoke Architect
- If an architect assessment was merged -> invoke Tech Lead (if WIP allows)
- If a plan was merged to active -> invoke Acceptance Tester
- If acceptance tests were merged -> invoke Developer
- If a developer PR was merged with approvals -> invoke Unit Tester, then Security Reviewer, then Operations Specialist (in priority order, one at a time)

**`on-pr-iterate.yml`** -- Triggered when a PR receives a review or comment. It determines which agent should respond:
- If the PR has requested changes from a reviewer -> invoke the original author agent to address feedback
- If all required reviews are approved -> proceed to next agent in the pipeline

Both workflows use a shared `reusable/agent-invoke.yml` template that handles:
1. Checkout and context extraction
2. Reading the appropriate persona definition from `docs/agents/personas/`
3. Extracting relevant planning context via `scripts/planning/extract-context.py`
4. Invoking Claude Code Action with the persona + context as the prompt
5. Ensuring only one agent runs at a time (concurrency controls)

### Serialized Execution

A GitHub Actions concurrency group ensures only one agent is active at a time:

```yaml
concurrency:
  group: agent-execution
  cancel-in-progress: false
```

This guarantees every agent operates on a stable, consistent codebase. If multiple triggers arrive, they queue and execute in order.

### WIP Limits

The system enforces a configurable WIP (Work In Progress) limit. Before the Tech Lead breaks down a new ticket, the coordination workflow checks how many items are in `.planning/active/`. If at capacity, new tickets remain in the backlog until active work completes.

### No Agent Has Absolute Authority

No single agent can unilaterally merge or approve work:

- **Architect** can assess and recommend, but cannot implement
- **Tech Lead** can plan, but cannot implement or approve security
- **Developer** can implement, but cannot write tests or approve their own work
- **Testers** verify but cannot modify implementation
- **Security Reviewer** can block but cannot implement fixes
- **DevOps Engineer** maintains workflows but cannot approve application logic
- **Operations Specialist** reviews operational readiness but cannot modify features

Every PR requires passing CI checks (hard gates) plus reviews from the relevant personas before it can be merged. Initially, the human reviews every PR. Over time, auto-merge rules can be added for low-risk categories.

---

## Ticket Lifecycle

```
User writes ticket -> Merge to .planning/backlog/
                           |
                           v
                  +------------------+
                  |    ARCHITECT     |  Assess architectural impact
                  |   (priority 1)  |  Write/update ADRs if needed
                  +--------+---------+  Update ticket with assessment
                           |
                           v
                  +------------------+
                  |   TECH LEAD     |  Break into plan with ordered PRs
                  |  (priority 2)   |  Each PR = vertical slice
                  +--------+---------+  Merge plan to .planning/active/
                           |
                           v
                  +------------------+
                  | ACCEPTANCE      |  Write E2E tests (failing, TDD)
                  | TESTER (pri 4)  |  Merge tests ahead of passing
                  +--------+---------+
                           |
                           v
                  +------------------+
                  |   DEVELOPER     |  Implement per plan
                  |  (priority 5)   |  Small vertical slice PRs
                  +--------+---------+
                           |
              +------------+------------+
              v            v            v
        +-----------+ +-----------+ +-----------+
        | TECH LEAD | | ARCHITECT | | SECURITY  |
        | review:   | | review:   | | REVIEWER  |
        | plan      | | arch      | | (pri 7)   |
        +-----------+ +-----------+ +-----------+
              |            |            |
              +------+-----+-----+------+
                     |           |
                     v           v
              +-----------+ +-----------+
              | UNIT      | | OPS       |
              | TESTER    | | SPECIALIST|
              | (pri 6)   | | (pri 8)   |
              +-----------+ +-----------+
                     |           |
                     +-----+-----+
                           |
                           v
                  +------------------+
                  | ACCEPTANCE      |
                  | TESTER          |
                  | Review unit     |
                  | test coverage   |
                  +--------+---------+
                           |
                           v
                     PR merged
                     Acceptance tests show
                     incremental improvement
```

---

## Planning System

### YAML-Based Structured Planning

All planning artifacts use YAML files validated against JSON Schemas. This enables:

- **Machine-readable status tracking** -- workflows can parse and route work automatically
- **Subset extraction** -- scripts can pull only relevant context for each agent, avoiding context bloat
- **Schema validation in CI** -- invalid planning files are caught before merge
- **Markdown rendering** -- scripts convert YAML to human-readable markdown for review

### Ticket Schema

A plan is a set of milestones, and milestones contain ordered PRs. Plans and tickets are separate documents because they have different lifecycles (a ticket exists in the backlog before any plan is created), but a plan always references its parent ticket.

```yaml
# Example: .planning/backlog/001-basic-minesweeper-web.yaml
id: "001"
title: "Implement basic Minesweeper game for web"
status: backlog  # backlog | assessed | planned | in-progress | done
priority: high
created: "2026-04-03"

description: |
  Implement a basic Minesweeper game playable in a web browser.
  Should support beginner difficulty (9x9, 10 mines).
  Must include: grid rendering, click to reveal, right-click to flag,
  mine counting, win/loss detection, and game reset.

acceptance_criteria:
  - "Player can start a new beginner-difficulty game"
  - "Clicking a cell reveals it with correct mine count"
  - "Clicking a mine ends the game with a loss indication"
  - "Revealing all non-mine cells shows a win indication"
  - "Player can flag/unflag cells with right-click"
  - "Game can be reset without page reload"

affected_projects:
  - web-game

architectural_assessment:
  status: pending  # pending | complete
  notes: ""
  adrs_created: []
  adrs_updated: []

plan_reference: ""  # Path to plan in .planning/active/ once created
```

### Plan Schema

```yaml
# Example: .planning/active/001-basic-minesweeper-web/plan.yaml
id: "001"
ticket_reference: ".planning/backlog/001-basic-minesweeper-web.yaml"
status: in-progress  # planned | in-progress | done
created: "2026-04-03"

milestones:
  - id: "001-M1"
    title: "Core game logic"
    status: in-progress
    pull_requests:
      - id: "001-M1-PR1"
        title: "Game state model and mine placement"
        status: merged
        branch: "feat/001-m1-game-state"
        description: "Core data structures for game board, cell state, mine placement"
        estimated_lines: 150

      - id: "001-M1-PR2"
        title: "Cell reveal logic with flood fill"
        status: in-progress
        branch: "feat/001-m1-reveal"
        description: "Cell reveal including recursive reveal for zero-count cells"
        estimated_lines: 120

  - id: "001-M2"
    title: "Web UI rendering"
    status: planned
    pull_requests:
      - id: "001-M2-PR1"
        title: "Grid component with cell rendering"
        status: planned
        branch: "feat/001-m2-grid"
        description: "React component for the game grid"
        estimated_lines: 200
```

### Context Extraction

The `scripts/planning/extract-context.py` script produces filtered views of planning data for each agent. This prevents any agent from being overwhelmed with irrelevant context:

- **Architect** gets: all backlog tickets, architecture docs, active plan summaries
- **Tech Lead** gets: assessed tickets, active plans (for WIP counting), architecture overview
- **Developer** gets: their assigned PR details, plan context, relevant project docs
- **Tester** gets: ticket acceptance criteria, the plan, current test coverage data

---

## Documentation Hierarchy

### Design Principle: Agents Should Never Read More Than They Need

Documentation is structured so that an agent working on a specific project or task can find the relevant context quickly without reading the entire repository's documentation.

### Layer 1: Navigation (always loaded)

- **Root `README.md`** -- Project overview, directory map, how to navigate
- **Root `CLAUDE.md`** -- Universal rules, project index with one-line descriptions, pointers to deeper docs

These files are kept under 200 lines each. They tell the agent *where to look*, not *what to know*.

### Layer 2: Domain Documentation (loaded per-project)

- **`projects/<name>/README.md`** -- Project overview, tech stack, how to build/test/run
- **`projects/<name>/CLAUDE.md`** -- Project-specific agent instructions (patterns, key files, gotchas)
- **`projects/<name>/docs/`** -- Detailed project documentation

### Layer 3: Cross-Cutting Documentation (loaded on demand)

- **`docs/architecture/`** -- System-level architecture, ADRs
- **`docs/agents/`** -- Persona definitions, workflows
- **`contracts/`** -- API specifications, event schemas

### Layer 4: Planning Context (extracted by scripts)

- **`.planning/`** -- YAML files that are never read directly by agents in full. Instead, `scripts/planning/extract-context.py` produces focused summaries containing only what a specific agent needs for their current task.

---

## Guardrails

Guardrails are built into each project's build system using idiomatic tools for each language. The top-level `guardrails/` directory defines shared thresholds and policies that per-project CI reads from.

### Hard Gates (PR cannot merge if violated)

| Guardrail | Threshold | Applies To |
|-----------|-----------|------------|
| Unit test coverage | >= 50% | All projects except infra |
| Linting | Zero errors | All projects |
| Type checking | Zero errors | TypeScript, Kotlin, Go |
| Schema validation | All planning YAML valid | `.planning/` files |
| Build succeeds | Clean build | All projects |
| No critical CVEs | Zero critical vulnerabilities | All dependencies |
| Terraform validate | Valid configuration | infra project |

### Soft Warnings (reported but don't block)

| Guardrail | Target | Applies To |
|-----------|--------|------------|
| Unit test coverage | >= 80% | All projects except infra |
| Documentation coverage | All public APIs documented | All projects |
| PR size | < 400 lines of meaningful change | All PRs |
| Cyclomatic complexity | < 10 per function | All projects |
| Dependency freshness | No deps > 6 months old | All projects |
| Test execution time | < 60 seconds | Per project test suite |

### Per-Project CI with Language-Idiomatic Tooling

| Project | Language | Linter | Test Framework | Coverage Tool |
|---------|----------|--------|----------------|---------------|
| web-game | TypeScript | ESLint | Vitest | v8/istanbul |
| mobile-game | Kotlin | ktlint + detekt | JUnit 5 | JaCoCo |
| api | Go | golangci-lint | go test | go tool cover |
| analytics | Python | ruff | pytest | coverage.py |
| infra | Terraform | tflint + tfsec | terratest | N/A |

Each project's build system (package.json scripts, gradle tasks, go makefile targets, etc.) implements these guardrails natively. The top-level `Makefile` delegates to per-project build systems.

---

## Milestone 1: Vertical Slice -- One Project, Two Agents, End-to-End

**Objective:** Get a minimal version of the entire system running end-to-end rather than building components in isolation. By the end of this milestone, the Developer and Unit Tester agents should be able to collaborate on a PR for the web-game project, with CI enforcing guardrails.

This means we build the minimum of everything: just enough planning system to track one ticket, just enough CI to gate one project, just enough documentation for agents to navigate, and just enough orchestration to trigger two agents.

### Step 1: Repository Foundation and Web Game Scaffolding

**What:** Create the directory structure, root configs, and get the web-game project building with lint + test + coverage working.

**Deliverables:**
- Directory structure (empty dirs with `.gitkeep` where needed)
- Root `README.md` with project overview and navigation
- Root `CLAUDE.md` with universal agent instructions and project index
- `.gitignore` for all five language ecosystems
- `Makefile` with top-level targets that delegate to per-project builds
- `projects/web-game/` fully scaffolded: `package.json`, `tsconfig.json`, `vite.config.ts`, `vitest.config.ts`, `eslint.config.js`, stub `src/App.tsx` and `src/App.test.tsx`
- `projects/web-game/README.md` and `projects/web-game/CLAUDE.md`

**Acceptance criteria:**
- `make lint` passes (delegates to web-game ESLint)
- `make test` passes (delegates to web-game Vitest)
- `make coverage` reports a number
- Web-game builds and runs locally

### Step 2: CI Pipeline for Web Game

**What:** GitHub Actions workflow that runs lint, test, and coverage for the web-game on every PR, with hard gate enforcement.

**Deliverables:**
- `.github/workflows/ci-web-game.yml` with path-based triggers
- Coverage reporting as PR comment
- Hard gates: coverage >= 50%, lint clean, types clean
- Soft warnings: coverage < 80%, PR size

**Acceptance criteria:**
- PRs touching `projects/web-game/` trigger CI
- A PR that drops coverage below 50% is blocked
- A PR with lint errors is blocked
- Soft warnings appear as PR comments but don't block

### Step 3: Planning System (Minimal)

**What:** Schemas, templates, and validation for tickets and plans. Just enough to track one ticket through the system.

**Deliverables:**
- `.planning/schemas/ticket.schema.json` and `.planning/schemas/plan.schema.json`
- `.planning/templates/ticket.template.yaml` and `.planning/templates/plan.template.yaml`
- `scripts/planning/validate.py` -- validates YAML against schemas
- `scripts/planning/extract-context.py` -- extracts filtered context per persona
- CI validation of planning YAML (can be part of a general CI workflow)

**Acceptance criteria:**
- `make validate-planning` passes with template files
- `make validate-planning` fails with intentionally invalid YAML
- Context extraction produces different output for Developer vs. Tester personas

### Step 4: Developer and Unit Tester Persona Definitions

**What:** Define the two personas needed for the vertical slice, plus the minimal orchestration docs.

**Deliverables:**
- `docs/agents/personas/developer.md` -- full persona definition
- `docs/agents/personas/unit-tester.md` -- full persona definition
- `docs/agents/overview.md` -- brief overview of the agent team
- `.cursor/rules/global.mdc` -- minimal Cursor rules pointing to persona docs
- Update root `CLAUDE.md` with persona pointers

**Acceptance criteria:**
- Each persona has clear goals, constraints, triggers, and review criteria
- An agent given the persona definition could act on it without additional context

### Step 5: Agent Orchestration (Minimal)

**What:** A coordination workflow that can invoke the Developer and Unit Tester in sequence on a PR.

**Deliverables:**
- `.github/workflows/on-pr-merge.yml` -- coordination workflow (initially handling just: plan merged -> invoke Developer; developer PR merged -> invoke Unit Tester)
- `.github/workflows/reusable/agent-invoke.yml` -- shared template for agent invocation
- Concurrency group to ensure serialized execution

**Acceptance criteria:**
- Merging a plan triggers the Developer agent
- Developer's merged PR triggers the Unit Tester agent
- Only one agent runs at a time
- Each agent receives its persona definition and relevant context

### Step 6: End-to-End Validation

**What:** Create a sample ticket and plan, then verify the Developer and Unit Tester can collaborate on a real (trivial) change.

**Deliverables:**
- A sample ticket in `.planning/backlog/` (e.g., "Add a page title to the web-game stub")
- A sample plan in `.planning/active/` referencing the ticket
- Run the Developer agent on the plan item and verify it produces a PR
- Run the Unit Tester agent on the Developer's PR and verify it adds tests
- Document any manual steps still needed and create follow-up tickets

**Acceptance criteria:**
- The two-agent collaboration produces a working, tested change
- CI passes on the final PR
- The process is documented for replication

---

## Milestone 2 (Preview -- to be planned after Milestone 1)

Expand the system incrementally:

1. Add remaining personas (Architect, Tech Lead, Acceptance Tester, Security Reviewer, DevOps Engineer, Operations Specialist)
2. Expand orchestration to handle the full ticket lifecycle
3. Scaffold remaining projects (api, mobile-game, analytics, infra)
4. Add architecture documentation and ADRs
5. Begin actual Minesweeper implementation via the agent team

Each of these would be broken into vertical slices -- e.g., add the Architect persona and the backlog-to-assessment workflow together, then validate end-to-end before adding the Tech Lead.

---

## Open Questions and Future Considerations

1. **Auto-merge policies:** What criteria should qualify a PR for auto-merge without human review? Candidates: documentation-only changes, test-only changes, changes below a certain size that pass all gates.

2. **Agent cost controls:** Each agent invocation has a token/dollar cost. Should we set per-agent budgets? Per-ticket budgets? The `--max-budget-usd` flag in Claude Code and model selection can help here.

3. **Cross-project changes:** When a change spans multiple projects (e.g., adding an API endpoint requires changes to the API, the contract, and the web frontend), how should the plan decompose this? Likely: contract first, then parallel implementation.

4. **Game variant extensions:** The user plans to introduce curveball rules. This will test whether the architecture is flexible and whether agents handle evolving requirements gracefully.
