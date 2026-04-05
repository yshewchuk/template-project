# Verification Loop

## Purpose

Write failing acceptance tests (TDD) before implementation begins. Set up any build/CI infrastructure needed to run those tests. Annotate the plan with test-to-PR mappings.

## Trigger

A milestone is activated: a plan is merged with a milestone status set to `in-progress`.

## Output

A Verification PR containing:
- Failing integration and/or E2E tests for all acceptance criteria
- Build/CI setup needed to run the tests (if not already in place)
- Plan updates with test-to-PR mappings

## Phase 1 Flow

```
Milestone activated in plan
    |
    v
[Tech Lead] -- review milestone, confirm PR ordering
    |
    v
[Developer] -- set up build/CI for new components if needed
               (Phase 1: DevOps scope covered by Developer)
    |
    v
[Acceptance Tester] -- write failing E2E/integration tests
    |
    v
[Tech Lead] -- annotate plan with test-to-PR mapping
    |
    v
Verification PR -> human (PM) review -> merge
```

## Full Team Flow (Phase 2+)

```
Milestone activated in plan
    |
    v
[Tech Lead] -- review milestone, confirm PR ordering
    |
    v
[DevOps Engineer] -- set up build/CI for new components
    |
    v
[Acceptance Tester] -- write failing tests
    |
    v
[Tech Lead] -- update plan with test-to-PR mappings
    |
    v
[Security Engineer] -- review security test coverage
    |
    v
[Architect] -- review test infrastructure alignment
    |
    v
[Product Manager] -- review tests match desired experience
    |
    v
Verification PR -> merge
```

## Stage Sequence

### Phase 1

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Confirm milestone | Tech Lead | contribute |
| 2 | Build/CI setup | Developer | contribute |
| 3 | Write acceptance tests | Acceptance Tester | contribute |
| 4 | Update plan mappings | Tech Lead | contribute |
| 5 | Final review | Product Manager (human) | review |

### Full Team (Phase 2+)

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Confirm milestone | Tech Lead | contribute |
| 2 | Build/CI setup | DevOps Engineer | contribute |
| 3 | Write acceptance tests | Acceptance Tester | contribute |
| 4 | Update plan mappings | Tech Lead | contribute |
| 5 | Security test review | Security Engineer | review |
| 6 | Architecture review | Architect | review |
| 7 | Final review | Product Manager (human) | review |

## Acceptance Tester Checklist

When writing tests in this loop:

- [ ] Read the milestone's acceptance criteria from the ticket
- [ ] For each criterion, write at least one integration or E2E test
- [ ] Place tests in `projects/<name>/tests/integration/` or `projects/<name>/tests/e2e/`
- [ ] Use the project's standard test framework
- [ ] Verify all tests *fail* (no implementation exists yet)
- [ ] Use descriptive test names that reference the acceptance criterion
- [ ] Avoid flaky patterns: no timing dependencies, mock external services

## Validation

- All tests must compile/parse without errors
- All tests must fail (since implementation does not exist yet)
- Test file paths must be within the Acceptance Tester's ownership scope
- Plan updates must pass `make validate-planning`

## Labels

Stage labels follow the pattern `stage/<persona>` or `stage/review-<persona>`:
- `stage/tech-lead` -- Tech Lead confirming milestone
- `stage/developer` -- Developer setting up build/CI (Phase 1)
- `stage/acceptance-tester` -- Acceptance Tester writing tests
- `stage/review-product-manager` -- PM reviewing
