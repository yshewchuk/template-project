#!/usr/bin/env python3
"""Query plans from .planning/plans/ and render them as markdown.

Usage:
    python3 scripts/planning/query-plans.py                       # all plans
    python3 scripts/planning/query-plans.py --status in-progress  # filter by status
    python3 scripts/planning/query-plans.py --status draft --status in-progress
"""

import argparse
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PLANS_DIR = REPO_ROOT / ".planning" / "plans"

VALID_STATUSES = ["draft", "in-progress", "completed", "cancelled"]


def load_plans(statuses: list[str] | None) -> list[tuple[Path, dict]]:
    """Load plans, optionally filtering by status."""
    results = []
    if not PLANS_DIR.exists():
        return results
    for f in sorted(PLANS_DIR.glob("*.yaml")):
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


def status_icon(status: str) -> str:
    return {
        "planned": "\u23f3",
        "in-progress": "\U0001f6a7",
        "completed": "\u2705",
        "merged": "\u2705",
        "cancelled": "\u274c",
        "draft": "\U0001f4dd",
    }.get(status, "\u2753")


def render_plan(filepath: Path, plan: dict) -> str:
    """Render a single plan as markdown."""
    lines = []
    plan_id = plan.get("id", "?")
    lines.append(f"# Plan {plan_id}")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| **ID** | `{plan_id}` |")
    lines.append(f"| **Status** | {status_icon(plan.get('status', ''))} `{plan.get('status', '?')}` |")
    lines.append(f"| **Ticket** | `{plan.get('ticket_reference', '?')}` |")
    lines.append(f"| **File** | `{filepath.relative_to(REPO_ROOT)}` |")

    for ms in plan.get("milestones", []):
        ms_id = ms.get("id", "?")
        ms_status = ms.get("status", "?")
        lines.append("")
        lines.append(f"## Milestone {ms_id}: {ms.get('title', 'Untitled')}")
        lines.append("")
        lines.append(f"**Status:** {status_icon(ms_status)} `{ms_status}`")

        tests = ms.get("acceptance_tests", [])
        if tests:
            lines.append("")
            lines.append("### Acceptance Tests")
            lines.append("")
            lines.append("| Test | Passing At |")
            lines.append("|------|------------|")
            for at in tests:
                lines.append(f"| `{at.get('test', '?')}` | `{at.get('passing_at_pr', '?')}` |")

        prs = ms.get("pull_requests", [])
        if prs:
            lines.append("")
            lines.append("### Pull Requests")
            lines.append("")
            lines.append("| ID | Title | Status | Branch | Est. Lines |")
            lines.append("|----|-------|--------|--------|------------|")
            for pr in prs:
                pr_status = pr.get("status", "?")
                lines.append(
                    f"| `{pr.get('id', '?')}` "
                    f"| {pr.get('title', '?')} "
                    f"| {status_icon(pr_status)} `{pr_status}` "
                    f"| `{pr.get('branch', '?')}` "
                    f"| ~{pr.get('estimated_lines', '?')} |"
                )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Query plans and render as markdown"
    )
    parser.add_argument(
        "--status",
        action="append",
        choices=VALID_STATUSES,
        help="Filter by status (can be specified multiple times)",
    )
    args = parser.parse_args()

    plans = load_plans(args.status)

    if not plans:
        filter_desc = f" with status {args.status}" if args.status else ""
        print(f"No plans found{filter_desc}.")
        return 0

    for i, (filepath, plan) in enumerate(plans):
        if i > 0:
            print("\n---\n")
        print(render_plan(filepath, plan))

    return 0


if __name__ == "__main__":
    sys.exit(main())
