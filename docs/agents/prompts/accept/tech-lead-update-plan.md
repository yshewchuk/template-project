The Acceptance Tester has assessed test results for PR {{pr_id}}.

Your task:
1. Review the acceptance test results.
2. Update the plan at {{plan_file}} to reflect:
   - Which acceptance tests now pass (update `passing_at_pr` fields)
   - Mark the merged PR status as `merged`
   - Note any regressions
   - If tests that should pass don't: add new planned PRs to address gaps
   - Adjust test-to-PR mappings if remapped by the Acceptance Tester
3. If all PRs in the milestone are merged and all tests pass:
   - Update milestone status to `completed`
4. Run `make validate-planning` to verify the plan.
5. Commit and push changes.
