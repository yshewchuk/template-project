#!/usr/bin/env python3
"""Generate GitHub Actions workflow YAML from declarative stage definitions.

Reads stage definition files from docs/agents/work-cycles/stages/*.yaml
and generates the corresponding workflow files under .github/workflows/.

Usage:
    python generate_workflows.py [--stages-dir DIR] [--output-dir DIR] [--check]

With --check, exits non-zero if generated files differ from what's on disk.
"""

import argparse
import glob
import json
import os
import re
import sys
import textwrap

import yaml

GENERATED_HEADER = "# AUTO-GENERATED from {source}\n# Do not edit manually. Run: make generate-workflows\n"
PERSONA_DISPLAY_NAMES = {
    "tech-lead": "Tech Lead",
    "developer": "Developer",
    "acceptance-tester": "Acceptance Tester",
    "scrum-master": "Scrum Master",
    "product-manager": "Product Manager",
}


def slugify(persona: str, name: str) -> str:
    """Create a job ID slug from persona + stage name."""
    parts = persona + "-" + name
    return re.sub(r"[^a-z0-9]+", "-", parts.lower()).strip("-")


def build_all_stages_json(stages: list[dict]) -> str:
    """Build the JSON array used for tracking comments."""
    entries = []
    for i, stage in enumerate(stages, 1):
        display = PERSONA_DISPLAY_NAMES.get(stage["persona"], stage["persona"])
        entries.append({
            "number": i,
            "type": stage["type"],
            "persona": display,
            "skipped": stage.get("skipped", False),
        })
    return json.dumps(entries, separators=(",", ":"))


def build_trigger(trigger: dict) -> dict:
    """Build the 'on:' section of a workflow."""
    t = trigger["type"]
    if t == "push":
        on = {"push": {"branches": trigger["branches"]}}
        if "paths" in trigger:
            on["push"]["paths"] = trigger["paths"]
        return on
    elif t == "pull_request":
        pr: dict = {"branches": trigger["branches"]}
        if "types" in trigger:
            pr["types"] = trigger["types"]
        return {"pull_request": pr}
    return {t: {}}


def build_detect_job(config: dict, trigger: dict) -> dict:
    """Build the detect/trigger detection job."""
    detect = config["detect"]
    steps: list[dict] = []

    checkout: dict = {"name": "Checkout", "uses": "actions/checkout@v4"}
    fetch_depth = detect.get("fetch_depth")
    if fetch_depth:
        checkout["with"] = {"fetch-depth": fetch_depth}
    steps.append(checkout)

    if detect.get("needs_python", False):
        steps.append({
            "name": "Set up Python",
            "uses": "actions/setup-python@v5",
            "with": {"python-version": "3.12"},
        })
        steps.append({"name": "Install dependencies", "run": "pip install pyyaml"})

    steps.append({
        "name": detect.get("job_name", "Detect trigger"),
        "id": "detect",
        "shell": "bash",
        "run": detect["script"].rstrip(),
    })

    job: dict = {
        "name": detect.get("job_name", "Detect trigger"),
        "runs-on": "ubuntu-latest",
        "outputs": {
            out: f"${{{{ steps.detect.outputs.{out} }}}}"
            for out in detect["outputs"]
        },
        "steps": steps,
    }

    if trigger.get("merged_only"):
        job["if"] = "github.event.pull_request.merged == true"

    return job


def build_branch_job(config: dict) -> dict | None:
    """Build the create-branch job, or None if not needed."""
    branch = config.get("branch")
    if not branch:
        return None
    if not branch.get("prefix") and not branch.get("from_output"):
        return None

    if branch.get("from_output"):
        output_ref = f"${{{{ needs.detect.outputs.{branch['from_output']} }}}}"
        fallback = f"{branch.get('fallback_prefix', 'impl')}/{branch.get('fallback_suffix', '')}"
        script = (
            f'BRANCH="{output_ref}"\n'
            f'if [ -z "$BRANCH" ]; then\n'
            f'  BRANCH="{fallback}"\n'
            f'fi\n'
        )
    elif branch.get("fallback_suffix"):
        suffix = branch["suffix"]
        fallback = branch["fallback_suffix"]
        script = (
            f'SUFFIX="{suffix}"\n'
            f'if [ -z "$SUFFIX" ]; then\n'
            f'  SUFFIX="{fallback}"\n'
            f'fi\n'
            f'BRANCH="{branch["prefix"]}/$SUFFIX"\n'
        )
    else:
        suffix = branch.get("suffix", "")
        script = f'BRANCH="{branch["prefix"]}/{suffix}"\n'

    script += 'git checkout -b "$BRANCH"\ngit push -u origin "$BRANCH"\necho "name=$BRANCH" >> "$GITHUB_OUTPUT"'

    return {
        "name": f"Create {config['work_cycle']} branch",
        "needs": "detect",
        "if": config["detect"]["should_run_condition"],
        "runs-on": "ubuntu-latest",
        "outputs": {"branch": "${{ steps.branch.outputs.name }}"},
        "steps": [
            {"name": "Checkout", "uses": "actions/checkout@v4"},
            {"name": "Create branch", "id": "branch", "shell": "bash", "run": script},
        ],
    }


def build_stage_job(
    config: dict,
    stage: dict,
    stage_number: int,
    all_stages_json: str,
    prev_job_id: str,
    has_branch: bool,
    has_pr: bool,
) -> tuple[str, dict]:
    """Build a single stage job. Returns (job_id, job_dict)."""
    display = PERSONA_DISPLAY_NAMES.get(stage["persona"], stage["persona"])
    job_id = f"stage-{stage_number}-{slugify(stage['persona'], stage['name'])}"

    needs = ["detect"]
    if has_branch:
        needs.append("create-branch")
    if has_pr:
        needs.append("open-pr")
    if prev_job_id and prev_job_id not in needs:
        needs.append(prev_job_id)

    with_block: dict = {
        "work_cycle": config["work_cycle"],
        "persona": stage["persona"],
        "stage_number": str(stage_number),
        "stage_type": stage["type"],
        "stage_label": stage["label"],
        "prompt_template": f"docs/agents/prompts/{stage['prompt_template']}",
        "prompt_vars": " ".join(stage.get("prompt_vars", [])),
        "all_stages_json": all_stages_json,
    }

    if has_branch:
        with_block["branch"] = "${{ needs.create-branch.outputs.branch }}"

    if has_pr and stage["type"] == "review":
        with_block["pr_number"] = "${{ needs.open-pr.outputs.pr_number }}"

    job: dict = {
        "name": f"Stage {stage_number}: {display} — {stage['name']}",
        "needs": needs,
        "uses": "./.github/workflows/agent-invoke.yml",
        "with": with_block,
        "secrets": {"ANTHROPIC_API_KEY": "${{ secrets.ANTHROPIC_API_KEY }}"},
    }

    return job_id, job


def build_open_pr_job(config: dict, last_contribute_job_id: str) -> dict:
    """Build the open-pr job."""
    pr = config["create_pr"]
    needs = ["detect", "create-branch", last_contribute_job_id]

    return {
        "name": f"Open {config['work_cycle']} PR",
        "needs": needs,
        "runs-on": "ubuntu-latest",
        "outputs": {"pr_number": "${{ steps.pr.outputs.number }}"},
        "steps": [
            {
                "name": "Checkout",
                "uses": "actions/checkout@v4",
                "with": {"ref": "${{ needs.create-branch.outputs.branch }}"},
            },
            {
                "name": "Create PR",
                "id": "pr",
                "uses": "actions/github-script@v7",
                "with": {
                    "script": (
                        "const fn = require('./scripts/work-cycle/github/create-work-cycle-pr.js');\n"
                        "await fn({ github, context, core });\n"
                    ),
                },
                "env": {
                    "PR_TITLE": pr["title"],
                    "PR_BODY": pr["body"],
                    "HEAD_BRANCH": "${{ needs.create-branch.outputs.branch }}",
                    "WORK_CYCLE_LABEL": pr["label"],
                },
            },
        ],
    }


def generate_workflow(config: dict) -> dict:
    """Generate a complete workflow dict from a stage config."""
    trigger = config["trigger"]
    all_stages_json = build_all_stages_json(config["stages"])

    jobs: dict = {}

    jobs["detect"] = build_detect_job(config, trigger)

    branch_job = build_branch_job(config)
    has_branch = branch_job is not None
    if has_branch:
        jobs["create-branch"] = branch_job

    create_pr = config.get("create_pr")
    has_create_pr = create_pr is not None and "after_stage" in create_pr
    pr_after_stage = create_pr["after_stage"] if has_create_pr else None

    prev_job_id = ""
    last_contribute_job_id = ""

    for i, stage in enumerate(config["stages"], 1):
        has_pr = has_create_pr and i > pr_after_stage
        job_id, job = build_stage_job(
            config, stage, i, all_stages_json,
            prev_job_id, has_branch, has_pr,
        )
        jobs[job_id] = job
        prev_job_id = job_id

        if stage["type"] == "contribute":
            last_contribute_job_id = job_id

        if has_create_pr and i == pr_after_stage:
            jobs["open-pr"] = build_open_pr_job(config, last_contribute_job_id)
            prev_job_id = "open-pr"

    workflow: dict = {
        "name": f"Work Cycle: {config['work_cycle'].title()}",
    }

    on = build_trigger(trigger)
    workflow["on"] = on
    workflow["concurrency"] = {"group": "agent-execution", "cancel-in-progress": False}
    workflow["permissions"] = {
        "contents": "write",
        "pull-requests": "write",
        "issues": "write",
    }
    workflow["jobs"] = jobs

    return workflow


def workflow_to_yaml(workflow: dict, source_file: str) -> str:
    """Serialize a workflow dict to YAML with the generated header."""
    header = GENERATED_HEADER.format(source=source_file)

    class FlowStyleDumper(yaml.SafeDumper):
        pass

    def str_representer(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        if "${{" in data or data.startswith('"') or data.startswith("'"):
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    FlowStyleDumper.add_representer(str, str_representer)

    # 'on' is a reserved YAML keyword that becomes True; handle it manually
    workflow_copy = dict(workflow)
    on_block = workflow_copy.pop("on", None)

    body = yaml.dump(
        workflow_copy,
        Dumper=FlowStyleDumper,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=200,
    )

    if on_block:
        on_yaml = yaml.dump(
            {"on": on_block},
            Dumper=FlowStyleDumper,
            default_flow_style=False,
            sort_keys=False,
            width=200,
        )
        # Insert 'on:' block after 'name:' line
        name_line_end = body.index("\n") + 1
        body = body[:name_line_end] + on_yaml + body[name_line_end:]

    return header + "\n" + body


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stages-dir",
        default="docs/agents/work-cycles/stages",
        help="Directory containing stage definition YAML files",
    )
    parser.add_argument(
        "--output-dir",
        default=".github/workflows",
        help="Directory to write generated workflow files",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check mode: exit non-zero if generated files differ from disk",
    )
    args = parser.parse_args()

    stage_files = sorted(glob.glob(os.path.join(args.stages_dir, "*.yaml")))
    if not stage_files:
        print(f"No stage files found in {args.stages_dir}", file=sys.stderr)
        sys.exit(1)

    diffs = []

    for stage_file in stage_files:
        with open(stage_file) as f:
            config = yaml.safe_load(f)

        workflow = generate_workflow(config)
        rel_source = os.path.relpath(stage_file)
        content = workflow_to_yaml(workflow, rel_source)

        basename = os.path.basename(stage_file).removesuffix(".yaml")
        output_path = os.path.join(args.output_dir, f"work-cycle-{basename}.yml")

        if args.check:
            try:
                with open(output_path) as f:
                    existing = f.read()
                if existing != content:
                    diffs.append(output_path)
                    print(f"STALE: {output_path}", file=sys.stderr)
                else:
                    print(f"OK:    {output_path}")
            except FileNotFoundError:
                diffs.append(output_path)
                print(f"MISSING: {output_path}", file=sys.stderr)
        else:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w") as f:
                f.write(content)
            print(f"Generated: {output_path}")

    if args.check and diffs:
        print(
            f"\n{len(diffs)} workflow(s) out of date. Run 'make generate-workflows' to update.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
