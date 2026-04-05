A new ticket has been merged: {{ticket_file}}

Your task in the Planning work cycle:
1. Read the ticket at `{{ticket_file}}`.
2. Assess security implications — update `docs/security/threat-model.md` if needed.
3. Assess architectural implications — write ADRs to `docs/architecture/decisions/` if needed.
4. Update `contracts/` if APIs are affected.
5. Create a technical plan in `.planning/plans/` with:
   - Milestones that group related PRs
   - PRs ordered so each is independently mergeable
   - Estimated line counts per PR (target < 400 lines)
   - Branch names following `feat/<ticket-id>-<milestone>-<description>`
   - Acceptance test mappings (which tests pass after which PR)
6. Run `make validate-planning` to verify the plan.
7. Create a new branch (e.g. `plan/{{ticket_id}}`) and push a PR with the planning changes.
