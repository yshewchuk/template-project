# Agent System Overview

This document describes the AI agent collaboration system used in this repository. The system enables multiple specialized agents to work together on a monorepo, each with clearly defined responsibilities, ownership boundaries, and interaction patterns.

## Architecture

The agent system is built on three pillars:

1. **Personas** define *who* each agent is: its goals, constraints, owned files, and review criteria.
2. **Loops** define *how* agents collaborate: the trigger, sequence of stages, and output for each workflow.
3. **Guardrails** define *what quality means*: automated checks that every PR must pass.

## Active Personas (Phase 1)

In Phase 1, four agent personas are active. Some cover expanded scopes that will be split into dedicated personas in later phases.

| Persona | Expanded Scope (Phase 1) | Definition |
|---------|--------------------------|------------|
| **Tech Lead** | + Architect, Security Engineer | [`personas/tech-lead.md`](personas/tech-lead.md) |
| **Acceptance Tester** | (none) | [`personas/acceptance-tester.md`](personas/acceptance-tester.md) |
| **Developer** | + DevOps Engineer, Operator, Unit Tester | [`personas/developer.md`](personas/developer.md) |
| **Scrum Master** | (none) | [`personas/scrum-master.md`](personas/scrum-master.md) |

The **Product Manager** role is filled by the human user.

## Planned Personas (Phase 2+)

These will be split from their Phase 1 hosts as the system matures:

| Persona | Split From | Trigger |
|---------|-----------|---------|
| Architect | Tech Lead | Milestone 2, Step 1 |
| Security Engineer | Tech Lead | Milestone 2, Step 2 |
| Unit Tester | Developer | Milestone 2, Step 4 |
| DevOps Engineer | Developer | Milestone 2, Step 6 |
| Operator | Developer | Milestone 2, Step 6 |

## The Five Loops

Loops are sequential workflows triggered by specific events. Only one agent is active at a time within a loop.

| Loop | Trigger | Output | Documentation |
|------|---------|--------|---------------|
| **Planning** | Ticket merged to backlog | Technical plan with milestones and PRs | [`loops/planning.md`](loops/planning.md) |
| **Verification** | Milestone activated | Failing acceptance tests (TDD) | [`loops/verification.md`](loops/verification.md) |
| **Implementation** | Verification PR merged | Code implementing one planned PR | [`loops/implementation.md`](loops/implementation.md) |
| **Accept** | Implementation PR ready | Approved and merged PR | [`loops/accept.md`](loops/accept.md) |
| **Improve** | Milestone completed | Process improvements | [`loops/improve.md`](loops/improve.md) |

## Serialized Execution

All loops share a single concurrency group. Only one agent executes at a time; queued triggers run in order. This prevents conflicting changes and simplifies reasoning about repository state.

## Ownership Enforcement

Every file has exactly one owning persona defined in `OWNERS.yaml`. Agents may only modify files within their ownership scope. The `scripts/ownership/check.py` script validates this in CI.

## Context Extraction

Agents never read `.planning/` files in full. Instead, `scripts/planning/extract-context.py` produces focused summaries filtered by persona and task, keeping agent context windows small and relevant.

## PR Stage Model

When multiple agents contribute to a single PR, it moves through a sequence of **stages**. Each stage is either a "contribute" stage (agent pushes commits) or a "review" stage (agent approves or requests changes). Stage progress is tracked via:

- **PR labels** for machine-readable current stage
- **Tracking comments** for human-readable progress checklists
- **GitHub reviews** for native approval/rejection

See individual loop documentation for the stage sequences.
