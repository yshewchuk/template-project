#!/usr/bin/env python3
"""Validate .planning/ YAML files against their JSON Schemas.

Validates:
  - .planning/backlog/*.yaml   against  .planning/schemas/ticket.schema.json
  - .planning/active/*.yaml    against  .planning/schemas/plan.schema.json
  - .planning/completed/*.yaml against  .planning/schemas/plan.schema.json
  - .planning/templates/ticket.yaml against ticket schema
  - .planning/templates/plan.yaml   against plan schema

Exit code 0 if all files are valid (or no YAML files exist).
Exit code 1 if any validation errors are found.
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCHEMAS_DIR = REPO_ROOT / ".planning" / "schemas"

VALIDATION_MAP = {
    "ticket": {
        "schema_file": "ticket.schema.json",
        "directories": [
            REPO_ROOT / ".planning" / "backlog",
        ],
        "template": REPO_ROOT / ".planning" / "templates" / "ticket.yaml",
    },
    "plan": {
        "schema_file": "plan.schema.json",
        "directories": [
            REPO_ROOT / ".planning" / "active",
            REPO_ROOT / ".planning" / "completed",
        ],
        "template": REPO_ROOT / ".planning" / "templates" / "plan.yaml",
    },
}


def load_schema(schema_file: str) -> dict:
    schema_path = SCHEMAS_DIR / schema_file
    if not schema_path.exists():
        print(f"ERROR: Schema file not found: {schema_path}")
        sys.exit(1)
    with open(schema_path) as f:
        return json.load(f)


def validate_file(filepath: Path, schema: dict) -> list[str]:
    """Validate a single YAML file against a schema. Returns list of error messages."""
    errors = []
    try:
        with open(filepath) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML parse error in {filepath}: {e}"]

    if data is None:
        return [f"Empty YAML file: {filepath}"]

    validator = jsonschema.Draft7Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in error.absolute_path) or "(root)"
        errors.append(f"  {filepath}: [{path}] {error.message}")

    return errors


def main() -> int:
    all_errors: list[str] = []
    files_checked = 0

    for doc_type, config in VALIDATION_MAP.items():
        schema = load_schema(config["schema_file"])

        for directory in config["directories"]:
            if not directory.exists():
                continue
            for yaml_file in sorted(directory.glob("*.yaml")):
                files_checked += 1
                errors = validate_file(yaml_file, schema)
                if errors:
                    all_errors.extend(errors)
                else:
                    print(f"  OK: {yaml_file.relative_to(REPO_ROOT)}")

        template = config.get("template")
        if template and template.exists():
            files_checked += 1
            errors = validate_file(template, schema)
            if errors:
                all_errors.extend(errors)
            else:
                print(f"  OK: {template.relative_to(REPO_ROOT)} (template)")

    if files_checked == 0:
        print("No YAML files found to validate.")
        return 0

    print(f"\nValidated {files_checked} file(s).")

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found:\n")
        for err in all_errors:
            print(err)
        return 1

    print("All files valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
