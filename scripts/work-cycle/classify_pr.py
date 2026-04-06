#!/usr/bin/env python3
"""Classify a merged PR to determine which work cycle should trigger next.

Checks the branch name and labels of a merged PR to determine whether
it is a verification, acceptance, or implementation PR.

Usage:
    python classify_pr.py --branch <branch> --labels '["label1","label2"]'

Outputs (one per line):
    is_verification=true|false
    is_acceptance=true|false
    is_implementation=true|false
"""

import argparse
import json
import re
import sys


def classify_pr(branch: str, labels: list[str]) -> dict[str, bool]:
    """Return classification flags for a PR based on branch and labels."""
    is_verification = bool(re.match(r"^verify/", branch))

    is_acceptance = (
        "work-cycle/acceptance" in labels
        or bool(re.match(r"^accept/", branch))
    )

    is_implementation = (
        "work-cycle/implementation" in labels
        or bool(re.match(r"^(impl/|feat/)", branch))
    )

    return {
        "is_verification": is_verification,
        "is_acceptance": is_acceptance,
        "is_implementation": is_implementation,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True, help="Head branch of the merged PR")
    parser.add_argument("--labels", default="[]",
                        help="JSON array of label names on the PR")
    args = parser.parse_args()

    try:
        labels = json.loads(args.labels)
    except json.JSONDecodeError:
        labels = []

    result = classify_pr(args.branch, labels)

    for key, value in result.items():
        print(f"{key}={'true' if value else 'false'}")


if __name__ == "__main__":
    main()
