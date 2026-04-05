# Verification Work Cycle

## Purpose

Write failing acceptance tests (TDD) before implementation begins. Set up any build/CI infrastructure needed to run those tests. Annotate the plan with test-to-PR mappings.

## Trigger

A milestone is activated: a plan is merged with a milestone status set to `in-progress`.

## Output

A Verification PR containing:
- Failing integration and/or E2E tests for all acceptance criteria
- Build/CI setup needed to run the tests (if not already in place)
- Plan updates with test-to-PR mappings

## Flow

```
Milestone activated in plan
    |
    v
[Tech Lead] -- review milestone, confirm PR ordering
    |
    v
[Developer] -- set up build/CI for new components if needed
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

## Stage Sequence

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Confirm milestone | Tech Lead | contribute |
| 2 | Build/CI setup | Developer | contribute |
| 3 | Write acceptance tests | Acceptance Tester | contribute |
| 4 | Update plan mappings | Tech Lead | contribute |
| 5 | Final review | Product Manager (human) | review |

## Acceptance Tester Checklist

When writing tests in this work cycle:

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
- `stage/developer` -- Developer setting up build/CI
- `stage/acceptance-tester` -- Acceptance Tester writing tests
- `stage/review-product-manager` -- PM reviewing
