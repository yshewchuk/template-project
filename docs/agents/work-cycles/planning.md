# Planning Work Cycle

## Purpose

Transform a product ticket into an actionable technical plan with milestones, ordered PRs, security assessments, and architectural decisions.

## Trigger

A new ticket PR is merged into `.planning/backlog/`.

## Output

A Planning PR containing:
- Updated threat model in `docs/security/` (if applicable)
- Updated architecture docs and ADRs in `docs/architecture/` (if applicable)
- Updated contract definitions in `contracts/` (if APIs are affected)
- A technical plan in `.planning/plans/` with milestones, ordered PRs, estimates, and branch names

## Flow

The Tech Lead covers all contributing roles (Architect, Security Engineer):

```
Ticket PR merged to .planning/backlog/
    |
    v
[Tech Lead] -- assess security, update threat model
             -- assess architecture, write ADRs if needed
             -- create technical plan with milestones and PRs
    |
    v
Planning PR -> human (PM) review -> merge
```

## Stage Sequence

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Requirements & planning | Tech Lead | contribute |
| 2 | Final review | Product Manager (human) | review |

## Tech Lead Checklist

When executing this work cycle, the Tech Lead must:

- [ ] Read the ticket's acceptance criteria and description
- [ ] Assess security implications; update `docs/security/threat-model.md` if needed
- [ ] Assess architectural implications; write ADRs to `docs/architecture/decisions/` if needed
- [ ] Update `contracts/` if APIs are affected
- [ ] Create a plan YAML in `.planning/plans/` with:
  - Milestones that group related PRs
  - PRs ordered so each is independently mergeable
  - Estimated line counts per PR (target < 400 lines)
  - Branch names following `feat/<ticket-id>-<milestone>-<description>` convention
  - Acceptance test mappings (which tests pass after which PR)
- [ ] Run `make validate-planning` to verify the plan
- [ ] Push the Planning PR for human review

## Validation

- `make validate-planning` must pass (schema validation of all `.planning/` YAML)
- All referenced projects must exist in the Project Index
- PR ordering must not have circular dependencies
- Each PR's estimated lines should be under 400

## Labels

- PR label during Tech Lead contribution: `stage/tech-lead`
- PR label during PM review: `stage/review-product-manager`
