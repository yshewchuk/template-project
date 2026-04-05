#!/usr/bin/env python3
"""Detect new or changed tickets from a git diff.

Reads the list of changed files between HEAD~1 and HEAD under
.planning/tickets/ and outputs the first ticket's ID and file path.

Usage:
    python detect_ticket.py [--diff-output <text>]

If --diff-output is not provided, runs git diff automatically.

Outputs (one per line, for consumption by GitHub Actions):
    ticket_id=<id>
    ticket_file=<path>
"""

import argparse
import os
import re
import subprocess
import sys


def get_changed_tickets(diff_output: str | None = None) -> list[str]:
    if diff_output is not None:
        lines = diff_output.strip().splitlines()
    else:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD", "--", ".planning/tickets/"],
            capture_output=True, text=True,
        )
        lines = result.stdout.strip().splitlines()
    return [line.strip() for line in lines if line.strip()]


def extract_ticket_info(changed_files: list[str]) -> tuple[str, str]:
    """Return (ticket_id, ticket_file) from a list of changed ticket paths.

    Returns ("", "") if no valid ticket found.
    """
    if not changed_files:
        return ("", "")

    ticket_file = changed_files[0]
    basename = os.path.basename(ticket_file)
    name_without_ext = basename.removesuffix(".yaml").removesuffix(".yml")
    match = re.match(r"^(\d+)", name_without_ext)
    ticket_id = match.group(1) if match else ""

    return (ticket_id, ticket_file)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff-output", default=None,
                        help="Pre-computed git diff output (for testing)")
    args = parser.parse_args()

    changed = get_changed_tickets(args.diff_output)
    ticket_id, ticket_file = extract_ticket_info(changed)

    if not ticket_id:
        print("No ticket changes detected", file=sys.stderr)

    print(f"ticket_id={ticket_id}")
    print(f"ticket_file={ticket_file}")


if __name__ == "__main__":
    main()
