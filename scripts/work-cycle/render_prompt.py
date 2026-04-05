#!/usr/bin/env python3
"""Render a prompt template by substituting {{variable}} placeholders.

Templates are markdown files stored under docs/agents/prompts/ with
{{variable_name}} placeholders. Variables are provided as key=value
command-line arguments.

Usage:
    python render_prompt.py --template docs/agents/prompts/planning/tech-lead-create-plan.md \\
        ticket_file=.planning/tickets/001.yaml

Undefined variables are left as-is with a warning on stderr.

Outputs the rendered prompt to stdout.
"""

import argparse
import re
import sys


def render_template(template: str, variables: dict[str, str]) -> str:
    """Replace {{key}} placeholders with values from the variables dict."""
    used = set()

    def replacer(match: re.Match) -> str:
        key = match.group(1).strip()
        if key in variables:
            used.add(key)
            return variables[key]
        print(f"Warning: undefined template variable '{key}'", file=sys.stderr)
        return match.group(0)

    result = re.sub(r"\{\{(\s*[\w.-]+\s*)\}\}", replacer, template)

    unused = set(variables.keys()) - used
    for key in sorted(unused):
        print(f"Warning: variable '{key}' was provided but not used in template", file=sys.stderr)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, help="Path to template file")
    parser.add_argument("vars", nargs="*", metavar="KEY=VALUE",
                        help="Template variables as key=value pairs")
    args = parser.parse_args()

    with open(args.template) as f:
        template = f.read()

    variables: dict[str, str] = {}
    for var in args.vars:
        if "=" not in var:
            print(f"Error: variable must be KEY=VALUE, got: {var}", file=sys.stderr)
            sys.exit(1)
        key, _, value = var.partition("=")
        variables[key] = value

    rendered = render_template(template, variables)
    print(rendered, end="")


if __name__ == "__main__":
    main()
