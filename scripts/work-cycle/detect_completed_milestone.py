#!/usr/bin/env python3
"""Detect a newly completed milestone by comparing current and previous plan state.

Compares a plan file's milestones against a previous version to find milestones
that just transitioned to 'completed' status.

Usage:
    python detect_completed_milestone.py --plan-file <path> [--old-content <yaml>]
    python detect_completed_milestone.py --plan-files <file1> [<file2> ...]

If --old-content is not provided, runs `git show HEAD~1:<path>` to get the
previous version.

Outputs (one per line):
    should_run=true|false
    plan_file=<path>
    plan_id=<id>
    milestone_id=<id>
"""

import argparse
import subprocess
import sys

import yaml


def get_old_plan(plan_file: str, old_content: str | None = None) -> dict:
    """Load the previous version of a plan file."""
    if old_content is not None:
        try:
            return yaml.safe_load(old_content) or {}
        except yaml.YAMLError:
            return {}

    try:
        result = subprocess.run(
            ["git", "show", f"HEAD~1:{plan_file}"],
            capture_output=True, text=True, check=True,
        )
        return yaml.safe_load(result.stdout) or {}
    except (subprocess.CalledProcessError, yaml.YAMLError):
        return {}


def find_newly_completed(
    plan_file: str,
    current_content: str | None = None,
    old_content: str | None = None,
) -> dict | None:
    """Return info about a newly completed milestone, or None."""
    if current_content is not None:
        try:
            current = yaml.safe_load(current_content)
        except yaml.YAMLError:
            return None
    else:
        try:
            with open(plan_file) as f:
                current = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            return None

    if not current or not isinstance(current, dict):
        return None

    old = get_old_plan(plan_file, old_content)

    old_completed = {
        m["id"]
        for m in old.get("milestones", [])
        if m.get("status") == "completed"
    }

    for milestone in current.get("milestones", []):
        if (
            milestone.get("status") == "completed"
            and milestone["id"] not in old_completed
        ):
            return {
                "plan_file": plan_file,
                "plan_id": current["id"],
                "milestone_id": milestone["id"],
            }

    return None


def get_changed_plans(plan_files: list[str] | None = None) -> list[str]:
    if plan_files is not None:
        return plan_files
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", ".planning/plans/"],
        capture_output=True, text=True,
    )
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-files", nargs="*", default=None,
                        help="Explicit list of plan files to check")
    parser.add_argument("--old-content", default=None,
                        help="Previous plan YAML content (for testing)")
    args = parser.parse_args()

    plan_files = get_changed_plans(args.plan_files)

    for plan_file in plan_files:
        result = find_newly_completed(plan_file, old_content=args.old_content)
        if result:
            print("should_run=true")
            print(f"plan_file={result['plan_file']}")
            print(f"plan_id={result['plan_id']}")
            print(f"milestone_id={result['milestone_id']}")
            return

    print("should_run=false")
    print("plan_file=")
    print("plan_id=")
    print("milestone_id=")


if __name__ == "__main__":
    main()
