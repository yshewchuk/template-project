#!/usr/bin/env python3
"""Detect plan context for a merged implementation PR.

Given a branch name, searches active plans for a matching PR entry
(by branch or in-progress status in an in-progress milestone).

Usage:
    python detect_impl_pr.py --branch <branch-name> [--plans-dir <dir>]

Outputs (one per line):
    plan_file=<path>
    milestone_id=<id>
    pr_id=<id>
"""

import argparse
import glob
import sys

import yaml


def find_impl_pr(branch: str, plans_dir: str = ".planning/plans") -> dict | None:
    """Return plan context for a branch, or None."""
    for plan_file in sorted(glob.glob(f"{plans_dir}/*.yaml")):
        try:
            with open(plan_file) as f:
                plan = yaml.safe_load(f)
        except (OSError, yaml.YAMLError):
            continue

        if not plan or not isinstance(plan, dict):
            continue

        for milestone in plan.get("milestones", []):
            if milestone.get("status") != "in-progress":
                continue
            for pr in milestone.get("pull_requests", []):
                pr_branch = pr.get("branch", "")
                if pr_branch == branch or pr.get("status") == "in-progress":
                    return {
                        "plan_file": plan_file,
                        "milestone_id": milestone["id"],
                        "pr_id": pr["id"],
                    }
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True,
                        help="Branch name of the merged implementation PR")
    parser.add_argument("--plans-dir", default=".planning/plans",
                        help="Directory containing plan YAML files")
    args = parser.parse_args()

    result = find_impl_pr(args.branch, args.plans_dir)

    if result is None:
        print("plan_file=")
        print("milestone_id=")
        print("pr_id=")
    else:
        print(f"plan_file={result['plan_file']}")
        print(f"milestone_id={result['milestone_id']}")
        print(f"pr_id={result['pr_id']}")


if __name__ == "__main__":
    main()
