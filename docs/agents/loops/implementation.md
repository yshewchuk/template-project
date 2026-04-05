# Implementation Loop

## Purpose

Implement code for one planned PR from the milestone. This loop executes once per PR in the milestone plan, in order.

## Trigger

Either:
1. **Verification PR merged** -- starts the first implementation PR in the milestone.
2. **Acceptance PR merged** -- continues with the next planned PR if the milestone still has remaining PRs (including any new PRs added by the Accept loop to address implementation gaps).

## Output

An Implementation PR containing:
- Functional code implementing the planned scope
- CI/build updates if needed
- Logging, monitoring, and health checks where appropriate
- Unit tests meeting coverage requirements
- Updated project documentation if patterns or commands changed

## Phase 1 Flow

In Phase 1, the Developer covers all contributing roles:

```
For each PR in the milestone plan:
    |
    v
[Developer] -- implement code
             -- update CI/build if needed (DevOps scope)
             -- add logging/monitoring (Operator scope)
             -- write unit tests (Unit Tester scope)
    |
    v
[Tech Lead] -- review for plan adherence,
               architecture, and security
    |
    v
[Acceptance Tester] -- review unit test adequacy
    |
    v
[Product Manager] -- review requirements satisfaction
    |
    v
Implementation PR -> merge -> Accept loop
```

## Full Team Flow (Phase 2+)

```
For each PR in the milestone plan:
    |
    v
[Developer] -- implement functional code
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
[Tech Lead] -- review plan adherence
    |
    v
[Security Engineer] -- review for vulnerabilities
    |
    v
[Architect] -- review architectural consistency
    |
    v
[Acceptance Tester] -- review unit test adequacy
    |
    v
[Product Manager] -- review requirements satisfaction
    |
    v
Implementation PR -> merge -> Accept loop
```

## Stage Sequence

### Phase 1

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Implementation (all contribute roles) | Developer | contribute |
| 2 | Plan adherence + architecture + security | Tech Lead | review |
| 3 | Unit test adequacy | Acceptance Tester | review |
| 4 | Requirements satisfaction | Product Manager (human) | review |

### Full Team (Phase 2+)

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Functional code | Developer | contribute |
| 2 | CI/build updates | DevOps Engineer | contribute |
| 3 | Operational readiness | Operator | contribute |
| 4 | Unit tests | Unit Tester | contribute |
| 5 | Plan adherence | Tech Lead | review |
| 6 | Security review | Security Engineer | review |
| 7 | Architecture review | Architect | review |
| 8 | Test adequacy | Acceptance Tester | review |
| 9 | Requirements review | Product Manager (human) | review |

## Developer Checklist (Phase 1)

Before pushing the Implementation PR:

- [ ] Code implements exactly the planned PR scope (no more, no less)
- [ ] Linting passes with zero errors
- [ ] Type checking passes with zero errors
- [ ] Unit tests pass
- [ ] Coverage meets the hard gate (>= 50%)
- [ ] Build succeeds cleanly
- [ ] No critical CVEs in new dependencies
- [ ] Project `README.md` updated if new commands or patterns were introduced
- [ ] Project `CLAUDE.md` updated if new key files or conventions were added

## Review Rejection Flow

If a reviewer requests changes:

1. The tracking comment is updated to show the rejection.
2. The stage label reverts to `stage/developer`.
3. The Developer is invoked with the review feedback as context.
4. The Developer pushes new commits addressing the feedback.
5. The stage advances back to the reviewer who rejected.

This continues until the reviewer approves.

## Validation

- All project-specific guardrails must pass (lint, type check, test, coverage, build)
- `scripts/ownership/check.py` must confirm all changed files are within Developer ownership
- PR size should be under the 400-line soft limit

## Labels

- `stage/developer` -- Developer implementing
- `stage/review-tech-lead` -- Tech Lead reviewing
- `stage/review-acceptance-tester` -- Acceptance Tester reviewing
- `stage/review-product-manager` -- PM reviewing
