# Accept Loop

## Purpose

Validate that implementation meets acceptance criteria by updating and running acceptance tests, then iterating until all tests pass. Also update the plan to reflect the current acceptance state.

## Trigger

Implementation PR is merged and acceptance tests need to be re-evaluated against the new code.

## Output

An Acceptance PR containing:
- Updated acceptance tests (if implementation revealed gaps or edge cases)
- Build/CI updates for test automation (if needed)
- Plan updates reflecting which acceptance tests now pass
- Confirmation that expected tests pass after the merged implementation

## Phase 1 Flow

```
Implementation PR merged
    |
    v
[Developer] -- update build/CI for acceptance tests if needed
               (Phase 1: DevOps scope covered by Developer)
    |
    v
[Acceptance Tester] -- run acceptance tests
                    -- update tests if implementation revealed gaps
    |
    v
[Tech Lead] -- update plan with acceptance state
    |
    v
[Product Manager] -- review acceptance results
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
[Acceptance Tester] -- run and update acceptance tests
    |
    v
[Tech Lead] -- update plan reflecting acceptance state
    |
    v
[Security Engineer] -- review security acceptance coverage
    |
    v
[Architect] -- review test infrastructure alignment
    |
    v
[Product Manager] -- review acceptance results
    |
    v
Acceptance PR -> merge
```

## Stage Sequence

### Phase 1

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Build/CI updates | Developer | contribute |
| 2 | Acceptance test updates | Acceptance Tester | contribute |
| 3 | Plan status updates | Tech Lead | contribute |
| 4 | Final review | Product Manager (human) | review |

### Full Team (Phase 2+)

| # | Stage | Persona | Type |
|---|-------|---------|------|
| 1 | Build/CI updates | DevOps Engineer | contribute |
| 2 | Acceptance test updates | Acceptance Tester | contribute |
| 3 | Plan status updates | Tech Lead | contribute |
| 4 | Security acceptance review | Security Engineer | review |
| 5 | Architecture review | Architect | review |
| 6 | Final review | Product Manager (human) | review |

## Acceptance Tester Checklist

When running this loop:

- [ ] Run all acceptance tests for the milestone
- [ ] Verify that tests mapped to the just-merged PR now pass
- [ ] Verify that previously passing tests still pass (no regressions)
- [ ] If tests fail unexpectedly, determine if the issue is in the test or the implementation
- [ ] Update tests if the implementation revealed edge cases not covered
- [ ] Add new tests if the plan or acceptance criteria evolved

## Plan Update Rules

The Tech Lead updates the plan to reflect:
- Which acceptance tests now pass (update `passing_at_pr` fields)
- PR status changes (mark merged PRs as `merged`)
- Any scope adjustments discovered during acceptance

## Milestone Completion

When all PRs in a milestone are merged and all acceptance tests pass:
1. The milestone status is updated to `completed`
2. The Improve loop is triggered
3. The next milestone (if any) can begin its Verification loop

## Labels

- `stage/developer` -- Developer updating build/CI (Phase 1)
- `stage/acceptance-tester` -- Acceptance Tester running/updating tests
- `stage/tech-lead` -- Tech Lead updating plan
- `stage/review-product-manager` -- PM reviewing results
