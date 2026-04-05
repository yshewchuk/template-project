# Accept Loop

## Purpose

Assess the current state of acceptance tests after an implementation PR merges. Record which tests now pass, adjust expectations for future tests, and update the plan to request additional implementation work if tests that should be passing are not.

Contributors in this loop do **not** iterate to make failing tests pass. They observe, record, and plan.

## Trigger

Implementation PR is merged and acceptance tests need to be re-evaluated against the new code.

## Output

An Acceptance PR containing:
- Updated acceptance test expectations (adjust which tests are expected to pass at which PR)
- Plan updates recording current acceptance state and any requested implementation changes
- New planned PRs if the implementation needs further work to satisfy acceptance criteria

## Phase 1 Flow

```
Implementation PR merged
    |
    v
[Developer] -- update build/CI for acceptance tests if needed
               (Phase 1: DevOps scope covered by Developer)
    |
    v
[Acceptance Tester] -- run acceptance tests, record results
                    -- adjust future test expectations if needed
                    -- flag tests that should pass but don't
    |
    v
[Tech Lead] -- update plan with acceptance state
             -- add new planned PRs if implementation gaps found
    |
    v
[Product Manager] -- review acceptance results and plan updates
    |
    v
Acceptance PR -> merge
    |
    v
Next Implementation PR or milestone complete
```

## Full Team Flow (Phase 2+)

```
Implementation PR merged
    |
    v
[DevOps Engineer] -- update build/CI for acceptance tests if needed
    |
    v
[Acceptance Tester] -- run acceptance tests, record results
                    -- adjust future test expectations if needed
    |
    v
[Tech Lead] -- update plan with acceptance state
             -- add new planned PRs if implementation gaps found
    |
    v
[Security Engineer] -- review security acceptance coverage
    |
    v
[Architect] -- review test infrastructure alignment
    |
    v
[Product Manager] -- review acceptance results and plan updates
    |
    v
Acceptance PR -> merge
```

## Stage Sequence

### Phase 1

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Build/CI updates | Developer | contribute |
| 2 | Acceptance assessment | Acceptance Tester | contribute |
| 3 | Plan updates | Tech Lead | contribute |
| 4 | Final review | Product Manager (human) | review |

### Full Team (Phase 2+)

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Build/CI updates | DevOps Engineer | contribute |
| 2 | Acceptance assessment | Acceptance Tester | contribute |
| 3 | Plan updates | Tech Lead | contribute |
| 4 | Security acceptance review | Security Engineer | review |
| 5 | Architecture review | Architect | review |
| 6 | Final review | Product Manager (human) | review |

## Acceptance Tester Checklist

When running this loop:

- [ ] Run all acceptance tests for the milestone
- [ ] Record which tests now pass and which still fail
- [ ] Verify that previously passing tests still pass (no regressions)
- [ ] For tests that should pass after this PR but don't: flag them as implementation gaps for the Tech Lead
- [ ] For tests that aren't expected to pass yet: confirm they still fail for the right reasons
- [ ] Adjust test-to-PR mappings if tests should be remapped to a different future PR

**Do NOT** fix implementation code, iterate on failing tests to make them pass, or modify test assertions to match incorrect behavior.

## Plan Update Rules

The Tech Lead updates the plan to reflect:
- Which acceptance tests now pass (update `passing_at_pr` fields)
- PR status changes (mark merged PRs as `merged`)
- Regressions: tests that previously passed but now fail
- Implementation gaps: if tests that should pass after this PR don't, add new planned PRs to the milestone to address the gaps
- Adjusted test-to-PR mappings if the Acceptance Tester remapped expectations

## Key Principle

The Accept loop is an **observation and planning** step, not an **iteration** step. If the implementation is incomplete or incorrect, the remedy is a new planned PR in the Implementation loop -- not rework within the Accept loop.

## Milestone Completion

When all PRs in a milestone are merged and all acceptance tests pass:
1. The milestone status is updated to `completed`
2. The Improve loop is triggered
3. The next milestone (if any) can begin its Verification loop

## Labels

- `stage/developer` -- Developer updating build/CI (Phase 1)
- `stage/acceptance-tester` -- Acceptance Tester assessing tests
- `stage/tech-lead` -- Tech Lead updating plan
- `stage/review-product-manager` -- PM reviewing results
