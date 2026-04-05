# Implementation Loop

## Purpose

Implement code for one planned PR from the milestone. The Developer posts the PR as soon as the functional code is complete and acceptance tests pass. Other contributors then layer on CI/build, operational, and unit test work.

## Trigger

Either:
1. **Verification PR merged** -- starts the first implementation PR in the milestone.
2. **Acceptance PR merged** -- continues with the next planned PR if the milestone still has remaining PRs (including any new PRs added by the Accept loop to address implementation gaps).

## Output

An Implementation PR containing:
- Functional code implementing the planned scope (Developer posts PR at this point)
- CI/build updates if needed (added after initial post)
- Logging, monitoring, and health checks where appropriate (added after initial post)
- Unit tests meeting coverage requirements (added after initial post)
- Updated project documentation if patterns or commands changed

## Phase 1 Flow

In Phase 1, the Developer covers all contributing roles. The PR is posted as soon as the functional code is done:

```
For each PR in the milestone plan:
    |
    v
[Developer] -- implement functional code
             -- run acceptance tests to verify correctness
             -- POST PR as soon as functional changes are complete
    |
    v
[Developer] -- update CI/build if needed (DevOps scope)
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
             -- run acceptance tests to verify correctness
             -- POST PR as soon as functional changes are complete
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

| # | Stage | Persona | Type | Notes |
|---|-------|---------|------|-------|
| 1 | Functional code | Developer | contribute | **PR posted after this stage** |
| 2 | CI/build, operational, unit tests | Developer | contribute | DevOps + Operator + Unit Tester scope |
| 3 | Plan adherence + architecture + security | Tech Lead | review | |
| 4 | Unit test adequacy | Acceptance Tester | review | |
| 5 | Requirements satisfaction | Product Manager (human) | review | |

### Full Team (Phase 2+)

| # | Stage | Persona | Type | Notes |
|---|-------|---------|------|-------|
| 1 | Functional code | Developer | contribute | **PR posted after this stage** |
| 2 | CI/build updates | DevOps Engineer | contribute | |
| 3 | Operational readiness | Operator | contribute | |
| 4 | Unit tests | Unit Tester | contribute | |
| 5 | Plan adherence | Tech Lead | review | |
| 6 | Security review | Security Engineer | review | |
| 7 | Architecture review | Architect | review | |
| 8 | Test adequacy | Acceptance Tester | review | |
| 9 | Requirements review | Product Manager (human) | review | |

## Developer Checklist (Phase 1)

Before posting the PR (functional code complete):

- [ ] Code implements exactly the planned PR scope (no more, no less)
- [ ] Acceptance tests for this PR pass
- [ ] Linting passes with zero errors
- [ ] Type checking passes with zero errors
- [ ] Build succeeds cleanly
- [ ] No critical CVEs in new dependencies

After posting the PR, before handing off to reviewers:

- [ ] CI/build workflows updated if the implementation requires it
- [ ] Logging, monitoring, and health checks added where appropriate
- [ ] Unit tests written; coverage meets the hard gate (>= 50%)
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
