# Agent Persona

{{persona_content}}

# Task

{{task_prompt}}

# Context

- Work cycle: {{work_cycle}}
- Stage: {{stage_number}} ({{stage_type}})
- Branch: {{branch}}

# Instructions

1. Read CLAUDE.md for universal rules before making any changes.
2. Follow the persona definition above strictly.
3. Only modify files within your persona's ownership scope (defined in OWNERS.yaml).
4. Complete the task described above.
5. Validate your changes (run `make validate-planning` for planning files).
6. Commit and push all changes to the current branch.
