#!/usr/bin/env python3
"""Extract filtered planning context for a specific persona.

Usage:
    python3 scripts/planning/extract-context.py --persona tech-lead
    python3 scripts/planning/extract-context.py --persona developer
    python3 scripts/planning/extract-context.py --persona acceptance-tester
    python3 scripts/planning/extract-context.py --persona scrum-master

Each persona gets a tailored view of the planning state:
  - tech-lead:          Full plans (active), ticket summaries, milestone status
  - developer:          Active PRs assigned to current milestone, acceptance criteria
  - acceptance-tester:  Acceptance tests, milestone status, ticket criteria
  - scrum-master:       All plans and tickets (summary view), process metadata
  - product-manager:    Backlog overview, priorities, milestone progress
"""

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
BACKLOG_DIR = REPO_ROOT / ".planning" / "backlog"
ACTIVE_DIR = REPO_ROOT / ".planning" / "active"
COMPLETED_DIR = REPO_ROOT / ".planning" / "completed"

VALID_PERSONAS = [
    "tech-lead",
    "developer",
    "acceptance-tester",
    "scrum-master",
    "product-manager",
]


def load_yaml_files(directory: Path) -> list[dict]:
    """Load all YAML files from a directory, sorted by filename."""
    results = []
    if not directory.exists():
        return results
    for f in sorted(directory.glob("*.yaml")):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            if data:
                data["_source"] = str(f.relative_to(REPO_ROOT))
                results.append(data)
        except yaml.YAMLError:
            continue
    return results


def format_ticket_summary(ticket: dict) -> str:
    """One-line ticket summary."""
    return (
        f"[{ticket.get('id', '?')}] {ticket.get('title', 'Untitled')} "
        f"(status={ticket.get('status', '?')}, priority={ticket.get('priority', '?')})"
    )


def format_ticket_detail(ticket: dict) -> str:
    """Full ticket detail block."""
    lines = [
        f"Ticket {ticket.get('id', '?')}: {ticket.get('title', 'Untitled')}",
        f"  Status: {ticket.get('status', '?')}",
        f"  Priority: {ticket.get('priority', '?')}",
        f"  Created: {ticket.get('created', '?')}",
        f"  Projects: {', '.join(ticket.get('affected_projects', []))}",
        f"  Source: {ticket.get('_source', '?')}",
        f"  Description: {ticket.get('description', '').strip()[:200]}",
        "  Acceptance Criteria:",
    ]
    for criterion in ticket.get("acceptance_criteria", []):
        lines.append(f"    - {criterion}")

    sec = ticket.get("security_assessment", {})
    arch = ticket.get("architectural_assessment", {})
    lines.append(f"  Security Assessment: {sec.get('status', 'N/A')}")
    lines.append(f"  Architectural Assessment: {arch.get('status', 'N/A')}")

    return "\n".join(lines)


def format_plan_summary(plan: dict) -> str:
    """Compact plan summary."""
    milestones = plan.get("milestones", [])
    ms_summary = ", ".join(
        f"{m.get('id', '?')}({m.get('status', '?')})" for m in milestones
    )
    return (
        f"Plan {plan.get('id', '?')}: status={plan.get('status', '?')} "
        f"milestones=[{ms_summary}]"
    )


def format_plan_full(plan: dict) -> str:
    """Full plan detail block."""
    lines = [
        f"Plan {plan.get('id', '?')}",
        f"  Ticket: {plan.get('ticket_reference', '?')}",
        f"  Status: {plan.get('status', '?')}",
        f"  Source: {plan.get('_source', '?')}",
    ]
    for ms in plan.get("milestones", []):
        lines.append(f"  Milestone {ms.get('id', '?')}: {ms.get('title', 'Untitled')}")
        lines.append(f"    Status: {ms.get('status', '?')}")

        for at in ms.get("acceptance_tests", []):
            lines.append(f"    Test: {at.get('test', '?')} -> passing at {at.get('passing_at_pr', '?')}")

        for pr in ms.get("pull_requests", []):
            lines.append(
                f"    PR {pr.get('id', '?')}: {pr.get('title', '?')} "
                f"[{pr.get('status', '?')}] branch={pr.get('branch', '?')} "
                f"~{pr.get('estimated_lines', '?')} lines"
            )

    return "\n".join(lines)


def format_milestone_prs(plan: dict) -> str:
    """Show only in-progress milestone PRs (for developers)."""
    lines = []
    for ms in plan.get("milestones", []):
        if ms.get("status") not in ("in-progress", "planned"):
            continue
        lines.append(f"Milestone {ms.get('id', '?')}: {ms.get('title', '')}")
        for pr in ms.get("pull_requests", []):
            if pr.get("status") in ("planned", "in-progress"):
                lines.append(
                    f"  PR {pr.get('id', '?')}: {pr.get('title', '?')} "
                    f"[{pr.get('status', '?')}] branch={pr.get('branch', '?')} "
                    f"~{pr.get('estimated_lines', '?')} lines"
                )
    return "\n".join(lines)


def format_acceptance_tests(plan: dict) -> str:
    """Show acceptance tests and milestone status (for testers)."""
    lines = []
    for ms in plan.get("milestones", []):
        lines.append(
            f"Milestone {ms.get('id', '?')}: {ms.get('title', '')} [{ms.get('status', '?')}]"
        )
        tests = ms.get("acceptance_tests", [])
        if tests:
            for at in tests:
                lines.append(
                    f"  Test: {at.get('test', '?')} -> passing at {at.get('passing_at_pr', '?')}"
                )
        else:
            lines.append("  (no acceptance tests defined)")
        for pr in ms.get("pull_requests", []):
            lines.append(
                f"  PR {pr.get('id', '?')}: {pr.get('title', '?')} [{pr.get('status', '?')}]"
            )
    return "\n".join(lines)


def extract_tech_lead(tickets: list, active_plans: list, completed_plans: list) -> str:
    """Tech lead sees full plans and ticket details for active work."""
    sections = ["=== PLANNING CONTEXT FOR: tech-lead ===\n"]

    sections.append("--- Active Plans ---")
    if active_plans:
        for plan in active_plans:
            sections.append(format_plan_full(plan))
            sections.append("")
    else:
        sections.append("(no active plans)\n")

    sections.append("--- Backlog Tickets ---")
    if tickets:
        for ticket in tickets:
            sections.append(format_ticket_detail(ticket))
            sections.append("")
    else:
        sections.append("(no tickets in backlog)\n")

    if completed_plans:
        sections.append("--- Completed Plans (summary) ---")
        for plan in completed_plans:
            sections.append(format_plan_summary(plan))
        sections.append("")

    return "\n".join(sections)


def extract_developer(tickets: list, active_plans: list, _completed: list) -> str:
    """Developer sees in-progress PRs and acceptance criteria for active tickets."""
    sections = ["=== PLANNING CONTEXT FOR: developer ===\n"]

    sections.append("--- Active PRs ---")
    if active_plans:
        for plan in active_plans:
            pr_text = format_milestone_prs(plan)
            if pr_text:
                sections.append(pr_text)
                sections.append("")
    else:
        sections.append("(no active plans)\n")

    sections.append("--- Relevant Acceptance Criteria ---")
    active_ticket_ids = {p.get("id") for p in active_plans}
    relevant = [t for t in tickets if t.get("id") in active_ticket_ids]
    if relevant:
        for ticket in relevant:
            sections.append(f"Ticket {ticket.get('id', '?')}: {ticket.get('title', '')}")
            for c in ticket.get("acceptance_criteria", []):
                sections.append(f"  - {c}")
            sections.append("")
    elif tickets:
        sections.append("(no tickets match active plans)\n")
    else:
        sections.append("(no tickets in backlog)\n")

    return "\n".join(sections)


def extract_acceptance_tester(
    tickets: list, active_plans: list, _completed: list
) -> str:
    """Acceptance tester sees tests, milestone status, and ticket criteria."""
    sections = ["=== PLANNING CONTEXT FOR: acceptance-tester ===\n"]

    sections.append("--- Acceptance Tests & Milestones ---")
    if active_plans:
        for plan in active_plans:
            sections.append(f"Plan {plan.get('id', '?')} ({plan.get('status', '?')}):")
            sections.append(format_acceptance_tests(plan))
            sections.append("")
    else:
        sections.append("(no active plans)\n")

    sections.append("--- Ticket Acceptance Criteria ---")
    if tickets:
        for ticket in tickets:
            sections.append(
                f"Ticket {ticket.get('id', '?')}: {ticket.get('title', '')}"
            )
            for c in ticket.get("acceptance_criteria", []):
                sections.append(f"  - {c}")
            sections.append("")
    else:
        sections.append("(no tickets)\n")

    return "\n".join(sections)


def extract_scrum_master(
    tickets: list, active_plans: list, completed_plans: list
) -> str:
    """Scrum master gets a summary view of everything for process analysis."""
    sections = ["=== PLANNING CONTEXT FOR: scrum-master ===\n"]

    sections.append("--- Backlog Overview ---")
    if tickets:
        for ticket in tickets:
            sections.append(format_ticket_summary(ticket))
    else:
        sections.append("(empty backlog)")
    sections.append("")

    sections.append("--- Active Plans ---")
    if active_plans:
        for plan in active_plans:
            sections.append(format_plan_summary(plan))
    else:
        sections.append("(no active plans)")
    sections.append("")

    sections.append("--- Completed Plans ---")
    if completed_plans:
        for plan in completed_plans:
            sections.append(format_plan_summary(plan))
    else:
        sections.append("(no completed plans)")
    sections.append("")

    return "\n".join(sections)


def extract_product_manager(
    tickets: list, active_plans: list, completed_plans: list
) -> str:
    """Product manager sees backlog priorities and milestone progress."""
    sections = ["=== PLANNING CONTEXT FOR: product-manager ===\n"]

    sections.append("--- Backlog (ordered by priority) ---")
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    sorted_tickets = sorted(
        tickets, key=lambda t: priority_order.get(t.get("priority", "low"), 99)
    )
    if sorted_tickets:
        for ticket in sorted_tickets:
            sections.append(format_ticket_detail(ticket))
            sections.append("")
    else:
        sections.append("(empty backlog)\n")

    sections.append("--- Milestone Progress ---")
    all_plans = active_plans + completed_plans
    if all_plans:
        for plan in all_plans:
            sections.append(format_plan_summary(plan))
    else:
        sections.append("(no plans)")
    sections.append("")

    return "\n".join(sections)


EXTRACTORS = {
    "tech-lead": extract_tech_lead,
    "developer": extract_developer,
    "acceptance-tester": extract_acceptance_tester,
    "scrum-master": extract_scrum_master,
    "product-manager": extract_product_manager,
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract filtered planning context for a persona"
    )
    parser.add_argument(
        "--persona",
        required=True,
        choices=VALID_PERSONAS,
        help="Persona to extract context for",
    )
    args = parser.parse_args()

    tickets = load_yaml_files(BACKLOG_DIR)
    active_plans = load_yaml_files(ACTIVE_DIR)
    completed_plans = load_yaml_files(COMPLETED_DIR)

    extractor = EXTRACTORS[args.persona]
    output = extractor(tickets, active_plans, completed_plans)
    print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
