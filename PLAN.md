# Minesweeper Monorepo: AI Agent Team Example

## Vision

This repository serves as an example monorepo demonstrating how a team of specialized AI agents can collaborate to build and iterate on a large-scale project. The example application is a **Minesweeper game** implemented across multiple platforms and languages, with supporting backend services and infrastructure.

The core hypothesis: by providing agents with the right scaffolding -- hierarchical documentation, objective guardrails, structured planning artifacts, and well-defined workflows -- a team of AI agents with distinct, non-overlapping ownership areas can deliver incremental, high-quality changes with minimal human steering.

### Success Criteria

The primary measure of success is **how little manual direction is needed from the user**. Specifically:

- The user writes tickets describing *what* they want (not *how*)
- Agents autonomously plan, verify, implement, accept, and improve
- The user reviews PRs and occasionally adjusts processes
- Over time, low-risk PRs are auto-approved and the human only reviews high-risk changes

### Key Problems This Aims to Solve

1. Agents do not break problems into small vertical slices -- reviewers face large, hard-to-review PRs
2. Large changes cause expensive back-and-forth that fills agent context windows
3. Agents ignore existing patterns and architecture, implementing the easiest path
4. Agents do not account for long-term plans, causing naive implementations
5. Iteration loops are expensive because each round starts with accumulated context debt
6. There is no mechanism for agents to improve their own processes over time

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

## Roles and Ownership

### The Ten Personas

| Role | Owns | Phase 1? |
|------|------|----------|
| Product Manager | Product backlog, priorities, product vision | Human (you) |
| Scrum Master | Agent definitions, workflows, planning schemas, process improvement | Yes |
| Architect | Architecture docs, ADRs, contracts, module boundaries | Covered by Tech Lead |
| Security Engineer | Threat model, security policies, security documentation | Covered by Tech Lead |
| Tech Lead | Technical plans, milestone breakdowns, PR ordering | Yes |
| Acceptance Tester | Integration and E2E tests | Yes |
| Developer | Application source code, project documentation | Yes |
| DevOps Engineer | CI/CD pipelines, build processes, workflow management | Covered by Developer |
| Operator | Infrastructure, logging, monitoring, operational readiness | Covered by Developer |
| Unit Tester | Unit tests, coverage enforcement | Covered by Developer |

### Phase 1: Four Active Agents

In Phase 1, only four agents are active. Each covers an expanded scope until the system matures enough to split roles:

- **Tech Lead** -- also covers Architect and Security Engineer responsibilities
- **Acceptance Tester** -- owns integration/E2E tests
- **Developer** -- also covers DevOps Engineer, Operator, and Unit Tester responsibilities
- **Scrum Master** -- owns process improvement from day one
- **Product Manager** -- the human user manages the backlog

### OWNERS.yaml: File Ownership Enforcement

Every file and folder has an owning role. Agents may only modify files within their ownership scope. CI enforces this via `scripts/ownership/check.py`.

```yaml
product-manager:
  - ".planning/backlog/**"

tech-lead:
  - ".planning/active/**"
  - ".planning/completed/**"
  - ".planning/templates/**"
  # Phase 1 expanded scope:
  - "docs/architecture/**"
  - "contracts/**"
  - "docs/security/**"
  - "guardrails/security.yaml"

acceptance-tester:
  - "projects/*/tests/integration/**"
  - "projects/*/tests/e2e/**"

developer:
  - "projects/*/src/**"
  - "projects/*/README.md"
  - "projects/*/CLAUDE.md"
  # Phase 1 expanded scope:
  - "projects/*/tests/unit/**"
  - "projects/*/src/**/*.test.*"
  - ".github/workflows/ci-*"
  - "Makefile"
  - "guardrails/coverage.yaml"
  - "guardrails/linting.yaml"
  - "projects/*/package.json"
  - "projects/*/tsconfig.json"
  - "projects/*/build.gradle.kts"
  - "projects/*/go.mod"
  - "projects/*/pyproject.toml"
  - "projects/infra/**"

scrum-master:
  - "docs/agents/**"
  - ".planning/schemas/**"
  - "scripts/planning/**"
  - "OWNERS.yaml"
  - "docs/guides/**"
  - "CLAUDE.md"
  - "README.md"
  - ".github/workflows/work-cycle-*"
  - ".github/workflows/reusable/**"
```

---

## The Five Work Cycles

The development process is organized into five work cycles. Each work cycle produces a specific type of PR with specific collaborators. Only one agent is active at a time within a work cycle, and work cycles execute in sequence.

### Work Cycle 1: Planning

**Trigger:** A new ticket is posted as a PR to `.planning/backlog/`.

**Full team:** Product Manager -> Security Engineer -> Architect -> Tech Lead
**Phase 1:** Human (PM) writes ticket -> Tech Lead (expanded scope handles security, architecture, and planning)

**Output PR:** Ticket in ordered backlog, updated threat model, updated architecture docs/ADRs, granular technical plan with milestones and ordered PRs. PM orders milestones across conflicting priorities.

```
Ticket PR merged to .planning/backlog/
    |
    v
[Product Manager] -- order backlog, confirm priorities
    |
    v
[Security Engineer] -- update threat model
    |
    v
[Architect] -- update architecture docs, write ADRs
    |
    v
[Tech Lead] -- create plan: milestones, ordered PRs, estimates
    |
    v
Planning PR -> human review -> merge
```

### Work Cycle 2: Verification

**Trigger:** A milestone is started (plan merged, milestone set to active).

**Full team:** Tech Lead -> DevOps Engineer -> Acceptance Tester
**Phase 1:** Tech Lead -> Acceptance Tester (Developer covers DevOps in Phase 1)

**Output PR:** Failing acceptance tests (TDD) plus any build/CI setup needed to run them, plus plan updates documenting which tests pass at each step.

```
Milestone activated in plan
    |
    v
[Tech Lead] -- review milestone, confirm PR ordering
    |
    v
[DevOps Engineer] -- set up build/CI for new components if needed
                     ensure acceptance test infrastructure is in place
    |
    v
[Acceptance Tester] -- write failing E2E/integration tests
                       annotate plan with test-to-PR mapping
    |
    v
Verification PR -> human review -> merge
```

### Work Cycle 3: Implementation

**Trigger:** Verification PR merged. Iterates once per PR in the milestone.

**Full team:** Developer -> DevOps Engineer -> Operator -> Unit Tester
**Phase 1:** Developer (expanded scope handles all four roles)

**Output PR:** Implementation matching one PR from the plan, with unit tests, CI/build updates, and operational readiness.

```
For each PR in the milestone plan:
    |
    v
[Developer] -- implement per plan
    |
    v
[DevOps Engineer] -- update CI/build if needed
    |
    v
[Operator] -- add logging, monitoring, health checks
    |
    v
[Unit Tester] -- write unit tests
    |
    v
Implementation PR -> proceed to Accept work cycle
```

### Work Cycle 4: Accept

**Trigger:** Implementation PR is ready for review.

**Full team:** Security Engineer -> Architect -> Tech Lead -> Acceptance Tester
**Phase 1:** Tech Lead (expanded scope) -> Acceptance Tester

**Output:** Approved and merged implementation PR. Follow-up PR if needed with updated threat model, architecture docs, plan status, and acceptance test adjustments.

```
Implementation PR ready
    |
    v
[Security Engineer] -- review for vulnerabilities
    |
    v
[Architect] -- review for architectural consistency
    |
    v
[Tech Lead] -- review for plan adherence
    |
    v
[Acceptance Tester] -- review unit test adequacy
    |
    v
PR approved -> merge -> next Implementation PR or milestone complete
```

### Work Cycle 5: Improve

**Trigger:** A milestone is completed (all PRs merged, acceptance tests passing).

**Participants:** Scrum Master

**Output PR:** Updated agent definitions, workflow docs, planning schemas, OWNERS.yaml adjustments, and retrospective notes.

```
Milestone complete
    |
    v
[Scrum Master] -- review all PRs and discussions from the milestone
                   identify misunderstandings, bottlenecks, failures
                   propose process improvements
    |
    v
Improve PR -> human review -> merge
```

---

## Repository Structure

```
/
+-- .github/workflows/
|   +-- ci-web-game.yml            # Path-filtered CI for web-game
|   +-- ci-mobile-game.yml         # Path-filtered CI for mobile-game
|   +-- ci-api.yml                 # Path-filtered CI for api
|   +-- ci-analytics.yml           # Path-filtered CI for analytics
|   +-- ci-infra.yml               # Path-filtered CI for infra
|   +-- work-cycle-planning.yml          # Planning work cycle orchestration
|   +-- work-cycle-verification.yml      # Verification work cycle orchestration
|   +-- work-cycle-implementation.yml    # Implementation work cycle orchestration
|   +-- work-cycle-accept.yml            # Accept work cycle orchestration
|   +-- work-cycle-improve.yml           # Improve work cycle orchestration
|   +-- reusable/
|       +-- agent-invoke.yml       # Shared agent invocation template
|
+-- CLAUDE.md                      # Root agent instructions (source of truth)
+-- OWNERS.yaml                    # File/folder ownership per role
|
+-- projects/
|   +-- web-game/                  # TypeScript (React + Vite)
|   +-- mobile-game/               # Kotlin (Android)
|   +-- api/                       # Go
|   +-- analytics/                 # Python
|   +-- infra/                     # Terraform (AWS)
|
+-- contracts/
|   +-- openapi/api.yaml           # High score API spec
|   +-- events/analytics.yaml      # Analytics event schemas
|
+-- docs/
|   +-- architecture/              # System architecture, ADRs
|   +-- security/                  # Threat model, security policies
|   +-- agents/
|   |   +-- overview.md
|   |   +-- personas/              # One file per persona
|   |   +-- work-cycles/           # One file per work cycle
|   +-- guides/
|       +-- onboarding.md
|       +-- adding-a-project.md
|
+-- .planning/
|   +-- schemas/                   # JSON Schemas for ticket + plan YAML
|   +-- backlog/                   # Ordered product backlog
|   +-- active/                    # Active plans with status
|   +-- completed/                 # Archived work
|   +-- templates/                 # YAML templates
|
+-- scripts/
|   +-- planning/                  # validate, render, extract-context, status-update
|   +-- ownership/check.py         # Validate PR changes against OWNERS.yaml
|   +-- guardrails/                # coverage, docs, architecture checks
|
+-- guardrails/                    # Shared thresholds (coverage, linting, arch, security)
+-- Makefile                       # Top-level task runner
+-- README.md
```

Each project under `projects/` has its own `CLAUDE.md`, `README.md`, `docs/`, and language-idiomatic build configuration.

---

## Planning System

All planning artifacts use YAML files validated against JSON Schemas. Scripts extract filtered context per persona to avoid context bloat.

### Ticket Example

```yaml
id: "001"
title: "Implement basic Minesweeper game for web"
status: backlog  # backlog | assessed | planned | in-progress | done
priority: high
created: "2026-04-03"
description: |
  Implement a basic Minesweeper game playable in a web browser.
  Should support beginner difficulty (9x9, 10 mines).
acceptance_criteria:
  - "Player can start a new beginner-difficulty game"
  - "Clicking a cell reveals it with correct mine count"
  - "Clicking a mine ends the game"
  - "Revealing all non-mine cells wins"
  - "Player can flag/unflag cells"
  - "Game can be reset without page reload"
affected_projects: [web-game]
security_assessment:
  status: pending
architectural_assessment:
  status: pending
plan_reference: ""
```

### Plan Example

```yaml
id: "001"
ticket_reference: ".planning/backlog/001-basic-minesweeper-web.yaml"
status: in-progress
milestones:
  - id: "001-M1"
    title: "Core game logic"
    status: in-progress
    acceptance_tests:
      - test: "test_new_game_creates_board"
        passing_at_pr: "001-M1-PR1"
      - test: "test_reveal_shows_mine_count"
        passing_at_pr: "001-M1-PR2"
    pull_requests:
      - id: "001-M1-PR1"
        title: "Game state model and mine placement"
        status: merged
        branch: "feat/001-m1-game-state"
        estimated_lines: 150
      - id: "001-M1-PR2"
        title: "Cell reveal logic with flood fill"
        status: in-progress
        branch: "feat/001-m1-reveal"
        estimated_lines: 120
```

---

## Orchestration

### Platform: Claude Code via GitHub Actions

Uses `anthropics/claude-code-action` as the single orchestration platform. Persona definitions in `docs/agents/personas/*.md` are the single source of truth. Cursor users get a minimal `.cursor/rules/global.mdc` pointing to these docs.

### Work Cycle Workflows

Each work cycle has a dedicated GitHub Actions workflow triggered by specific events:

- `work-cycle-planning.yml` -- triggered when ticket merges to backlog
- `work-cycle-verification.yml` -- triggered when plan merges with active milestone
- `work-cycle-implementation.yml` -- triggered when verification PR merges
- `work-cycle-accept.yml` -- triggered when implementation PR is ready
- `work-cycle-improve.yml` -- triggered when milestone completes

All use `reusable/agent-invoke.yml` which handles checkout, persona loading, context extraction, ownership validation, and Claude Code invocation.

### Serialized Execution

```yaml
concurrency:
  group: agent-execution
  cancel-in-progress: false
```

Only one agent active at a time. Queued triggers execute in order.

### PR Stage Model: Multi-Agent Collaboration on a Single PR

When multiple agents contribute to a single PR (e.g., an Implementation PR where Developer, DevOps, Operator, and Unit Tester each push commits), the PR moves through a defined sequence of **stages**. Each stage is either a "contribute" stage (an agent pushes commits) or a "review" stage (a reviewer approves or requests changes).

#### Stage Tracking Mechanism

Three mechanisms work together:

1. **PR Labels** -- Machine-readable current stage. The orchestration workflow sets a label like `stage/developer` or `stage/review-tech-lead` to indicate what is happening now. Only one stage label is active at a time.

2. **Tracking Comment** -- Human-readable progress. The orchestration bot posts and continuously updates a comment on the PR showing a checklist of all stages with their completion status. This is the at-a-glance view of where the PR stands.

3. **GitHub Reviews** -- Native approval mechanism for review stages. Reviewers use GitHub's approve/request-changes to signal their decision. The orchestration workflow watches for review events to advance or revert stages.

#### Stage Sequences Per Work Cycle

Each work cycle defines an ordered sequence of personas that follows a **growing cycle** pattern:

1. Each persona is either a **contributor** or a **reviewer** for that work cycle.
2. Contributors add to the PR in order. After each contribution, all previous personas review and iterate until aligned before the work cycle expands.
3. Reviewers validate the work against their area of responsibility and can request changes from contributors.
4. If a reviewer identifies issues requiring changes to plans, architecture, or threat models, the milestone is paused and a Planning PR is raised to address the changes before the current PR resumes.

Sequences below use `|` to separate contributors (left) from reviewers (right):

```
Planning: PM → Architect → Security Engineer → Tech Lead
  PM:                [contribute] requirements, backlog ordering, priorities
  Architect:         [contribute] architecture docs, ADRs, contract definitions
  Security Engineer: [contribute] threat model, security assessment
  Tech Lead:         [contribute] technical plan with milestones and ordered PRs

Verification: DevOps Engineer → Acceptance Tester → Tech Lead | Security Engineer → Architect → PM
  DevOps Engineer:   [contribute] build system, test automation infrastructure
  Acceptance Tester: [contribute] integration/E2E tests fitting the automation
  Tech Lead:         [contribute] plan updates linking acceptance tests to planned PRs
  Security Engineer: [review] security acceptance test coverage
  Architect:         [review] test infrastructure architectural alignment
  PM:                [review] tests implement desired experience

Implementation: Developer → DevOps Engineer → Operator → Unit Tester | Tech Lead → Security Engineer → Architect → Acceptance Tester → PM
  Developer:         [contribute] functional code
  DevOps Engineer:   [contribute] CI/build updates
  Operator:          [contribute] logging, monitoring, health checks
  Unit Tester:       [contribute] unit tests
  Tech Lead:         [review] plan adherence
  Security Engineer: [review] vulnerabilities
  Architect:         [review] architectural consistency
  Acceptance Tester: [review] unit test adequacy
  PM:                [review] requirements satisfaction

Acceptance: DevOps Engineer → Acceptance Tester → Tech Lead | Security Engineer → Architect → PM
  DevOps Engineer:   [contribute] update build system/automation if needed
  Acceptance Tester: [contribute] iterate on acceptance tests based on implementation results
  Tech Lead:         [contribute] plan updates reflecting current acceptance state
  Security Engineer: [review] security acceptance test coverage
  Architect:         [review] test infrastructure architectural alignment
  PM:                [review] tests implement desired experience

Improvement: Scrum Master | PM → Architect → Security Engineer → Tech Lead
  Scrum Master:      [contribute] retrospective, process improvements, updated agent definitions
  PM:                [review] process changes against product workflow
  Architect:         [review] process changes against architecture workflow
  Security Engineer: [review] process changes against security workflow
  Tech Lead:         [review] process changes against technical workflow
```

In Phase 1, stages for roles not yet active are skipped (e.g., DevOps, Operator, Unit Tester stages are handled by the Developer in a single contribute stage).

#### Tracking Comment Format

The orchestration bot posts a comment like this on each PR and updates it as stages complete:

```markdown
## PR Progress: 001-M1-PR1 Game state model

| # | Stage | Agent | Status | Commit/Review |
|---|-------|-------|--------|---------------|
| 1 | Contribute | Developer | Done | abc1234 |
| 2 | Review | Tech Lead | Done | Approved |
| 3 | Contribute | DevOps Engineer | Done | def5678 |
| 4 | Contribute | Operator | Skipped (Phase 1) | -- |
| 5 | Contribute | Unit Tester | Done | ghi9012 |
| 6 | Review | Security Engineer | **Active** | Awaiting review |
| 7 | Review | Architect | Pending | -- |
| 8 | Review | Tech Lead | Pending | -- |
| 9 | Review | Acceptance Tester | Pending | -- |
| 10 | Review | Product Manager | Pending | -- |

Current stage: **6 -- Security Engineer review**
```

#### Review Rejection Flow

When a reviewer requests changes, the workflow:

1. Updates the tracking comment to show the rejection
2. Reverts the stage label back to the relevant contributor (e.g., if Tech Lead requests changes at stage 2, the label goes back to `stage/developer` at stage 1)
3. Invokes the contributor agent with the review feedback as context
4. The contributor pushes new commits addressing the feedback
5. The workflow advances back to the review stage

This creates a tight feedback cycle between contributor and reviewer until the reviewer approves, then the PR advances to the next stage.

#### Implementation Details

The `reusable/agent-invoke.yml` template handles stage management:

1. Read the current stage from PR labels
2. Determine if this is a contribute or review stage
3. For contribute stages: invoke the agent with persona + context + any prior review feedback
4. After the agent pushes commits: advance the label to the next stage
5. For review stages: request a review from the appropriate agent (or human)
6. Watch for review events via `on-pr-iterate.yml` (triggered by `pull_request_review`)
7. On approval: advance to next stage. On request-changes: revert to contributor stage.
8. When all stages complete: mark PR as ready to merge

The stage sequence definitions live in `docs/agents/work-cycles/<cycle-name>.md` alongside the work cycle documentation, making them easy for the Scrum Master to adjust during Improve work cycles.

---

## Guardrails

Built into each project's build system with idiomatic tools. Shared thresholds in `guardrails/*.yaml`.

### Hard Gates

| Guardrail | Threshold | Applies To |
|-----------|-----------|------------|
| Unit test coverage | >= 50% | All projects except infra |
| Linting | Zero errors | All projects |
| Type checking | Zero errors | TypeScript, Kotlin, Go |
| Schema validation | Valid YAML | `.planning/` files |
| Build succeeds | Clean build | All projects |
| No critical CVEs | Zero critical | All dependencies |
| Ownership check | No out-of-scope files | All PRs |

### Soft Warnings

| Guardrail | Target | Applies To |
|-----------|--------|------------|
| Unit test coverage | >= 80% | All except infra |
| PR size | < 400 lines | All PRs |
| Cyclomatic complexity | < 10/function | All projects |

### Per-Project Tooling

| Project | Language | Linter | Test Framework | Coverage |
|---------|----------|--------|----------------|----------|
| web-game | TypeScript | ESLint | Vitest | v8/istanbul |
| mobile-game | Kotlin | ktlint + detekt | JUnit 5 | JaCoCo |
| api | Go | golangci-lint | go test | go tool cover |
| analytics | Python | ruff | pytest | coverage.py |
| infra | Terraform | tflint + tfsec | terratest | N/A |

---

## Documentation Hierarchy

### Layer 1: Navigation (always loaded)

- Root `README.md` -- overview, directory map (< 200 lines)
- Root `CLAUDE.md` -- universal rules, project index, persona pointers (< 200 lines)

### Layer 2: Per-Project (loaded per task)

- `projects/<name>/README.md` -- tech stack, build/test/run
- `projects/<name>/CLAUDE.md` -- agent instructions, patterns, key files

### Layer 3: Cross-Cutting (loaded on demand)

- `docs/architecture/` -- system architecture, ADRs
- `docs/security/` -- threat model, policies
- `docs/agents/` -- personas, work cycles
- `contracts/` -- API specs, event schemas

### Layer 4: Planning (extracted by scripts)

- `.planning/` -- never read in full; `extract-context.py` produces focused summaries per persona.

---

## Milestone 1: Vertical Slice -- Four Agents, End-to-End

**Objective:** Get Tech Lead, Acceptance Tester, Developer, and Scrum Master operating end-to-end on the web-game project. The human acts as Product Manager.

### Step 1: Repository Foundation

Create directory structure, root configs, and OWNERS.yaml.

**Deliverables:**
- Full directory structure with `.gitkeep` placeholders
- Root README.md, CLAUDE.md, .gitignore, OWNERS.yaml, Makefile

**Done when:** Directory structure exists, OWNERS.yaml is valid, root configs are in place.

### Step 2: Planning System (Minimal)

Schemas, templates, validation, context extraction for one ticket.

**Deliverables:**
- JSON Schemas for ticket and plan
- Template YAML files
- `scripts/planning/validate.py` and `extract-context.py`
- CI validation of planning YAML

**Done when:** `make validate-planning` passes/fails correctly, context extraction differs per persona.

### Step 3: Four Persona Definitions

Define Tech Lead, Acceptance Tester, Developer, Scrum Master with Phase 1 expanded scopes.

**Deliverables:**
- `docs/agents/personas/{tech-lead,acceptance-tester,developer,scrum-master}.md`
- `docs/agents/overview.md` and `docs/agents/work-cycles/{planning,verification,implementation,accept,improve}.md`
- `.cursor/rules/global.mdc` and updated root CLAUDE.md

**Done when:** Each persona has clear goals, constraints, ownership, triggers, and review criteria.

### Step 4: Work Cycle Orchestration Workflows

GitHub Actions for all five work cycles wired for Phase 1 agents.

**Deliverables:**
- `work-cycle-planning.yml`, `work-cycle-verification.yml`, `work-cycle-implementation.yml`, `work-cycle-accept.yml`, `work-cycle-improve.yml`
- `reusable/agent-invoke.yml`
- Concurrency group for serialized execution

**Done when:** Each work cycle triggers correctly and invokes the right agents in order.

### Step 5: End-to-End Validation

Run a real ticket through all five work cycles. The agents themselves scaffold and build the web game as the first real ticket.

**Deliverables:**
- Sample ticket and plan for web-game scaffolding
- Observe all work cycles: planning, verification, implementation, accept, improve
- Document manual steps still needed

**Done when:** Full cycle completes, web-game is scaffolded by the agents, CI passes, Scrum Master produces an improvement suggestion.

---

## Milestone 2 (Preview)

Expand incrementally, each as a vertical slice validated end-to-end:

1. Split Architect from Tech Lead + add to Planning and Accept work cycles
2. Split Security Engineer from Tech Lead + add to Planning and Accept work cycles
3. Scaffold Go API project + extend agent scope
4. Split Unit Tester from Developer + add to Implementation work cycle
5. Scaffold remaining projects (mobile-game, analytics, infra)
6. Split DevOps Engineer and Operator from Developer
7. Begin actual Minesweeper implementation via agent team
8. Explore Product Manager automation

---

## Open Questions

1. **Auto-merge policies:** What PR categories can be auto-merged? Candidates: doc-only, test-only, small changes passing all gates and reviews.
2. **Agent cost controls:** Per-agent and per-ticket budgets via `--max-budget-usd`.
3. **Cross-project changes:** Decompose as contract first, then parallel implementation.
4. **Ownership conflicts:** PRs touching multiple roles' files need each owner to contribute their portion.
5. **Scrum Master data:** What should it analyze? PR threads, CI logs, time-to-merge, review iteration count, context usage.
