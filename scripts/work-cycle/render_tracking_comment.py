#!/usr/bin/env python3
"""Render a PR tracking comment for work cycle stage progress.

Takes a JSON array of stage definitions and the current stage number,
produces the markdown body for the tracking comment.

Usage:
    python render_tracking_comment.py \\
        --stages '[{"number":1,"type":"contribute","persona":"Developer","skipped":false}]' \\
        --current-stage 1 \\
        --work-cycle implementation \\
        --current-persona Developer \\
        --current-type contribute

Outputs the full markdown body to stdout.
"""

import argparse
import json
import sys


STAGE_TYPE_ICONS = {
    "contribute": "\U0001f528",  # 🔨
    "review": "\U0001f440",      # 👀
}


def render_tracking_comment(
    stages: list[dict],
    current_stage: int,
    work_cycle: str,
    current_persona: str,
    current_type: str,
) -> str:
    """Render the markdown tracking comment body."""
    lines = [f"## PR Progress: {work_cycle} work cycle\n"]

    lines.append("| # | Type | Agent | Status |")
    lines.append("|---|------|-------|--------|")

    for stage in stages:
        number = stage["number"]
        stage_type = stage["type"]
        persona = stage["persona"]
        skipped = stage.get("skipped", False)

        if skipped:
            status = "\u23ed\ufe0f Skipped (Phase 1)"
        elif number < current_stage:
            status = "\u2705 Done"
        elif number == current_stage:
            status = "\U0001f504 **Active**"
        else:
            status = "Pending"

        icon = STAGE_TYPE_ICONS.get(stage_type, "")
        lines.append(f"| {number} | {icon} {stage_type} | {persona} | {status} |")

    lines.append("")
    lines.append(
        f"Current stage: **{current_stage} \u2014 {current_persona} ({current_type})**"
    )

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stages", required=True, help="JSON array of stage definitions")
    parser.add_argument("--current-stage", type=int, required=True)
    parser.add_argument("--work-cycle", required=True)
    parser.add_argument("--current-persona", required=True)
    parser.add_argument("--current-type", required=True)
    args = parser.parse_args()

    stages = json.loads(args.stages)
    body = render_tracking_comment(
        stages=stages,
        current_stage=args.current_stage,
        work_cycle=args.work_cycle,
        current_persona=args.current_persona,
        current_type=args.current_type,
    )
    print(body)


if __name__ == "__main__":
    main()
