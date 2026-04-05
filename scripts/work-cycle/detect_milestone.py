#!/usr/bin/env python3
"""Detect an activated (in-progress) milestone from changed plan files.

Scans plan files that changed between HEAD~1 and HEAD and finds the first
milestone with status 'in-progress'.

Usage:
    python detect_milestone.py [--plan-files <file1> <file2> ...]

If --plan-files is not provided, discovers changed files via git diff.

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


def get_changed_plans(plan_files: list[str] | None = None) -> list[str]:
    if plan_files is not None:
        return plan_files
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", ".planning/plans/"],
        capture_output=True, text=True,
    )
    return [f.strip() for f in result.stdout.strip().splitlines() if f.strip()]


def find_activated_milestone(plan_files: list[str]) -> dict | None:
    """Return info about the first in-progress milestone, or None."""
    for plan_file in plan_files:
        try:
            with open(plan_file) as f:
                plan = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            continue

        if not plan or not isinstance(plan, dict):
            continue

        for milestone in plan.get("milestones", []):
            if milestone.get("status") == "in-progress":
                return {
                    "plan_file": plan_file,
                    "plan_id": plan["id"],
                    "milestone_id": milestone["id"],
                }
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-files", nargs="*", default=None,
                        help="Explicit list of plan files to check")
    args = parser.parse_args()

    changed = get_changed_plans(args.plan_files)
    result = find_activated_milestone(changed)

    if result is None:
        print("should_run=false")
        print("plan_file=")
        print("plan_id=")
        print("milestone_id=")
    else:
        print("should_run=true")
        print(f"plan_file={result['plan_file']}")
        print(f"plan_id={result['plan_id']}")
        print(f"milestone_id={result['milestone_id']}")


if __name__ == "__main__":
    main()
