import json
import os

import pytest
import yaml

from generate_workflows import (
    build_all_stages_json,
    build_branch_job,
    build_detect_job,
    build_stage_job,
    build_trigger,
    generate_workflow,
    slugify,
    workflow_to_yaml,
)


MINIMAL_CONFIG = {
    "work_cycle": "test",
    "trigger": {"type": "push", "branches": ["main"], "paths": [".planning/**"]},
    "detect": {
        "job_name": "Detect",
        "script": "echo 'ok'",
        "outputs": ["should_run"],
        "should_run_condition": "needs.detect.outputs.should_run == 'true'",
    },
    "stages": [
        {
            "name": "do work",
            "persona": "developer",
            "type": "contribute",
            "label": "stage/developer",
            "prompt_template": "test/prompt.md",
            "prompt_vars": ["x=1"],
        },
    ],
}


class TestSlugify:
    def test_basic(self):
        assert slugify("tech-lead", "create plan") == "tech-lead-create-plan"

    def test_special_chars(self):
        assert slugify("developer", "CI, logging, unit tests") == "developer-ci-logging-unit-tests"

    def test_uppercase(self):
        assert slugify("Scrum-Master", "Retrospective") == "scrum-master-retrospective"


class TestBuildAllStagesJson:
    def test_single_stage(self):
        stages = [{"persona": "developer", "type": "contribute"}]
        result = json.loads(build_all_stages_json(stages))
        assert len(result) == 1
        assert result[0]["number"] == 1
        assert result[0]["persona"] == "Developer"
        assert result[0]["type"] == "contribute"

    def test_display_names(self):
        stages = [
            {"persona": "tech-lead", "type": "contribute"},
            {"persona": "product-manager", "type": "review"},
        ]
        result = json.loads(build_all_stages_json(stages))
        assert result[0]["persona"] == "Tech Lead"
        assert result[1]["persona"] == "Product Manager"
        assert result[1]["number"] == 2

    def test_skipped_flag(self):
        stages = [{"persona": "developer", "type": "contribute", "skipped": True}]
        result = json.loads(build_all_stages_json(stages))
        assert result[0]["skipped"] is True


class TestBuildTrigger:
    def test_push_trigger(self):
        trigger = {"type": "push", "branches": ["main"], "paths": [".planning/**"]}
        result = build_trigger(trigger)
        assert result == {"push": {"branches": ["main"], "paths": [".planning/**"]}}

    def test_pull_request_trigger(self):
        trigger = {"type": "pull_request", "branches": ["main"], "types": ["closed"]}
        result = build_trigger(trigger)
        assert result == {"pull_request": {"branches": ["main"], "types": ["closed"]}}

    def test_push_without_paths(self):
        trigger = {"type": "push", "branches": ["main"]}
        result = build_trigger(trigger)
        assert "paths" not in result["push"]


class TestBuildDetectJob:
    def test_basic(self):
        config = MINIMAL_CONFIG
        job = build_detect_job(config, config["trigger"])
        assert job["name"] == "Detect"
        assert "detect" in job["outputs"]["should_run"]
        assert any(s.get("id") == "detect" for s in job["steps"])

    def test_with_python(self):
        config = {**MINIMAL_CONFIG, "detect": {**MINIMAL_CONFIG["detect"], "needs_python": True}}
        job = build_detect_job(config, config["trigger"])
        step_names = [s.get("name", "") for s in job["steps"]]
        assert "Set up Python" in step_names
        assert "Install dependencies" in step_names

    def test_merged_only(self):
        trigger = {"type": "pull_request", "branches": ["main"], "merged_only": True}
        config = {**MINIMAL_CONFIG, "trigger": trigger}
        job = build_detect_job(config, trigger)
        assert job["if"] == "github.event.pull_request.merged == true"

    def test_fetch_depth(self):
        config = {**MINIMAL_CONFIG, "detect": {**MINIMAL_CONFIG["detect"], "fetch_depth": 2}}
        job = build_detect_job(config, config["trigger"])
        checkout = job["steps"][0]
        assert checkout["with"]["fetch-depth"] == 2


class TestBuildBranchJob:
    def test_no_branch(self):
        assert build_branch_job(MINIMAL_CONFIG) is None

    def test_with_prefix_and_suffix(self):
        config = {
            **MINIMAL_CONFIG,
            "branch": {"prefix": "verify", "suffix": "${{ needs.detect.outputs.milestone_id }}"},
        }
        job = build_branch_job(config)
        assert job is not None
        assert job["name"].startswith("Create")
        run_step = [s for s in job["steps"] if s.get("id") == "branch"][0]
        assert "verify/" in run_step["run"]

    def test_from_output_with_fallback(self):
        config = {
            **MINIMAL_CONFIG,
            "branch": {"from_output": "pr_branch", "fallback_prefix": "impl", "fallback_suffix": "${{ x }}"},
        }
        job = build_branch_job(config)
        assert job is not None
        run_step = [s for s in job["steps"] if s.get("id") == "branch"][0]
        assert "pr_branch" in run_step["run"]
        assert "impl/" in run_step["run"]


class TestBuildStageJob:
    def test_contribute_stage(self):
        stage = MINIMAL_CONFIG["stages"][0]
        all_json = build_all_stages_json(MINIMAL_CONFIG["stages"])
        job_id, job = build_stage_job(MINIMAL_CONFIG, stage, 1, all_json, "", False, False)
        assert "stage-1" in job_id
        assert "developer" in job_id
        assert job["with"]["stage_type"] == "contribute"
        assert job["with"]["persona"] == "developer"
        assert "detect" in job["needs"]

    def test_review_stage_with_pr(self):
        stage = {
            "name": "review",
            "persona": "tech-lead",
            "type": "review",
            "label": "stage/review-tech-lead",
            "prompt_template": "test.md",
            "prompt_vars": [],
        }
        all_json = "[]"
        _, job = build_stage_job(MINIMAL_CONFIG, stage, 3, all_json, "stage-2", True, True)
        assert "open-pr" in job["needs"]
        assert "create-branch" in job["needs"]
        assert job["with"]["pr_number"] == "${{ needs.open-pr.outputs.pr_number }}"

    def test_no_duplicate_needs(self):
        stage = MINIMAL_CONFIG["stages"][0]
        all_json = "[]"
        _, job = build_stage_job(MINIMAL_CONFIG, stage, 1, all_json, "detect", False, False)
        assert job["needs"].count("detect") == 1


class TestGenerateWorkflow:
    def test_minimal_config(self):
        workflow = generate_workflow(MINIMAL_CONFIG)
        assert workflow["name"] == "Work Cycle: Test"
        assert "detect" in workflow["jobs"]
        assert "create-branch" not in workflow["jobs"]

    def test_with_branch_and_pr(self):
        config = {
            **MINIMAL_CONFIG,
            "branch": {"prefix": "test", "suffix": "123"},
            "create_pr": {
                "after_stage": 1,
                "title": "Test PR",
                "body": "body",
                "label": "work-cycle/test",
            },
            "stages": [
                {**MINIMAL_CONFIG["stages"][0]},
                {"name": "review", "persona": "product-manager", "type": "review",
                 "label": "stage/review-product-manager", "prompt_template": "t.md", "prompt_vars": []},
            ],
        }
        workflow = generate_workflow(config)
        assert "create-branch" in workflow["jobs"]
        assert "open-pr" in workflow["jobs"]

    def test_stage_count(self):
        config = {
            **MINIMAL_CONFIG,
            "stages": [
                {**MINIMAL_CONFIG["stages"][0], "name": "first"},
                {**MINIMAL_CONFIG["stages"][0], "name": "second"},
                {**MINIMAL_CONFIG["stages"][0], "name": "third"},
            ],
        }
        workflow = generate_workflow(config)
        stage_jobs = [k for k in workflow["jobs"] if k.startswith("stage-")]
        assert len(stage_jobs) == 3


class TestWorkflowToYaml:
    def test_output_is_valid_yaml(self):
        workflow = generate_workflow(MINIMAL_CONFIG)
        content = workflow_to_yaml(workflow, "test.yaml")
        data = yaml.safe_load(content)
        assert data is not None
        assert "jobs" in data

    def test_has_generated_header(self):
        workflow = generate_workflow(MINIMAL_CONFIG)
        content = workflow_to_yaml(workflow, "test.yaml")
        assert "AUTO-GENERATED" in content
        assert "test.yaml" in content
        assert "make generate-workflows" in content


class TestRealStageFiles:
    """Test that the actual stage definition files in the repo produce valid workflows."""

    @pytest.fixture
    def stage_files(self):
        stage_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "docs", "agents", "work-cycles", "stages"
        )
        import glob as g
        files = sorted(g.glob(os.path.join(stage_dir, "*.yaml")))
        if not files:
            pytest.skip("No stage files found")
        return files

    def test_all_stage_files_generate_valid_yaml(self, stage_files):
        for path in stage_files:
            with open(path) as f:
                config = yaml.safe_load(f)
            workflow = generate_workflow(config)
            content = workflow_to_yaml(workflow, path)
            data = yaml.safe_load(content)
            assert data is not None, f"Invalid YAML from {path}"
            assert "jobs" in data, f"No jobs in workflow from {path}"

    def test_all_stage_files_have_detect_job(self, stage_files):
        for path in stage_files:
            with open(path) as f:
                config = yaml.safe_load(f)
            workflow = generate_workflow(config)
            assert "detect" in workflow["jobs"], f"No detect job for {path}"

    def test_all_stage_files_have_concurrency(self, stage_files):
        for path in stage_files:
            with open(path) as f:
                config = yaml.safe_load(f)
            workflow = generate_workflow(config)
            assert workflow["concurrency"]["group"] == "agent-execution"

    def test_stage_count_matches(self, stage_files):
        for path in stage_files:
            with open(path) as f:
                config = yaml.safe_load(f)
            workflow = generate_workflow(config)
            stage_jobs = [k for k in workflow["jobs"] if k.startswith("stage-")]
            assert len(stage_jobs) == len(config["stages"]), (
                f"Stage count mismatch for {path}: {len(stage_jobs)} jobs vs {len(config['stages'])} stages"
            )
