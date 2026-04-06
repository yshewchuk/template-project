#!/usr/bin/env python3
"""Detect the next planned PR to implement from active plans.

Scans all plan files under .planning/plans/ (or a provided list) and finds
the first PR with status 'planned' or 'in-progress' in an in-progress
milestone of an in-progress plan.

Usage:
    python detect_next_pr.py [--plans-dir <dir>]

Outputs (one per line):
    should_run=true|false
    plan_file=<path>
    milestone_id=<id>
    pr_id=<id>
    pr_title=<title>
    pr_branch=<branch>
"""

import argparse
import glob
import sys

import yaml


def find_next_pr(plans_dir: str = ".planning/plans") -> dict | None:
    """Return info about the next PR to implement, or None."""
    for plan_file in sorted(glob.glob(f"{plans_dir}/*.yaml")):
        try:
            with open(plan_file) as f:
                plan = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            continue

        if not plan or not isinstance(plan, dict):
            continue
        if plan.get("status") != "in-progress":
            continue

        for milestone in plan.get("milestones", []):
            if milestone.get("status") != "in-progress":
                continue
            for pr in milestone.get("pull_requests", []):
                if pr.get("status") in ("planned", "in-progress"):
                    return {
                        "plan_file": plan_file,
                        "milestone_id": milestone["id"],
                        "pr_id": pr["id"],
                        "pr_title": pr.get("title", ""),
                        "pr_branch": pr.get("branch", ""),
                    }
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plans-dir", default=".planning/plans",
                        help="Directory containing plan YAML files")
    args = parser.parse_args()

    result = find_next_pr(args.plans_dir)

    if result is None:
        print("should_run=false")
        print("plan_file=")
        print("milestone_id=")
        print("pr_id=")
        print("pr_title=")
        print("pr_branch=")
    else:
        print("should_run=true")
        print(f"plan_file={result['plan_file']}")
        print(f"milestone_id={result['milestone_id']}")
        print(f"pr_id={result['pr_id']}")
        print(f"pr_title={result['pr_title']}")
        print(f"pr_branch={result['pr_branch']}")


if __name__ == "__main__":
    main()
