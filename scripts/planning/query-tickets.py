#!/usr/bin/env python3
"""Query tickets from .planning/tickets/ and render them as markdown.

Usage:
    python3 scripts/planning/query-tickets.py                    # all tickets
    python3 scripts/planning/query-tickets.py --status backlog   # filter by status
    python3 scripts/planning/query-tickets.py --status in-progress --status planned
"""

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TICKETS_DIR = REPO_ROOT / ".planning" / "tickets"

VALID_STATUSES = ["backlog", "assessed", "planned", "in-progress", "done"]


def load_tickets(statuses: list[str] | None) -> list[tuple[Path, dict]]:
    """Load tickets, optionally filtering by status."""
    results = []
    if not TICKETS_DIR.exists():
        return results
    for f in sorted(TICKETS_DIR.glob("*.yaml")):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh)
            if data is None:
                continue
            if statuses and data.get("status") not in statuses:
                continue
            results.append((f, data))
        except yaml.YAMLError:
            continue
    return results


def render_ticket(filepath: Path, ticket: dict) -> str:
    """Render a single ticket as markdown."""
    lines = []
    lines.append(f"# Ticket {ticket.get('id', '?')}: {ticket.get('title', 'Untitled')}")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **ID** | `{ticket.get('id', '?')}` |")
    lines.append(f"| **Status** | `{ticket.get('status', '?')}` |")
    lines.append(f"| **Priority** | `{ticket.get('priority', '?')}` |")
    lines.append(f"| **Created** | {ticket.get('created', '?')} |")
    projects = ", ".join(f"`{p}`" for p in ticket.get("affected_projects", []))
    lines.append(f"| **Projects** | {projects} |")
    lines.append(f"| **File** | `{filepath.relative_to(REPO_ROOT)}` |")

    plan_ref = ticket.get("plan_reference", "")
    if plan_ref:
        lines.append(f"| **Plan** | `{plan_ref}` |")
    else:
        lines.append(f"| **Plan** | _(none)_ |")

    lines.append("")
    lines.append("## Description")
    lines.append("")
    lines.append(ticket.get("description", "").strip())

    lines.append("")
    lines.append("## Acceptance Criteria")
    lines.append("")
    for criterion in ticket.get("acceptance_criteria", []):
        lines.append(f"- {criterion}")

    sec = ticket.get("security_assessment", {})
    arch = ticket.get("architectural_assessment", {})
    if sec or arch:
        lines.append("")
        lines.append("## Assessments")
        lines.append("")
        if sec:
            sec_notes = sec.get("notes", "")
            notes_str = f" -- {sec_notes}" if sec_notes else ""
            lines.append(f"- **Security:** `{sec.get('status', 'N/A')}`{notes_str}")
        if arch:
            arch_notes = arch.get("notes", "")
            notes_str = f" -- {arch_notes}" if arch_notes else ""
            lines.append(f"- **Architectural:** `{arch.get('status', 'N/A')}`{notes_str}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query tickets and render as markdown"
    )
    parser.add_argument(
        "--status",
        action="append",
        choices=VALID_STATUSES,
        help="Filter by status (can be specified multiple times)",
    )
    args = parser.parse_args()

    tickets = load_tickets(args.status)

    if not tickets:
        filter_desc = f" with status {args.status}" if args.status else ""
        print(f"No tickets found{filter_desc}.")
        return 0

    for i, (filepath, ticket) in enumerate(tickets):
        if i > 0:
            print("\n---\n")
        print(render_ticket(filepath, ticket))

    return 0


if __name__ == "__main__":
    sys.exit(main())
