import os

import pytest
import yaml

from detect_next_pr import find_next_pr


def write_plan(directory, filename, plan):
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        yaml.dump(plan, f)
    return path


class TestFindNextPR:
    def test_finds_first_planned_pr(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "merged", "title": "First", "branch": "feat/001-m1-first"},
                    {"id": "001-M1-PR2", "status": "planned", "title": "Second", "branch": "feat/001-m1-second"},
                    {"id": "001-M1-PR3", "status": "planned", "title": "Third", "branch": "feat/001-m1-third"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))

        assert result is not None
        assert result["pr_id"] == "001-M1-PR2"
        assert result["pr_title"] == "Second"
        assert result["pr_branch"] == "feat/001-m1-second"
        assert result["milestone_id"] == "001-M1"

    def test_finds_in_progress_pr(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "in-progress", "title": "Active", "branch": "feat/active"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))

        assert result is not None
        assert result["pr_id"] == "001-M1-PR1"

    def test_skips_non_active_plans(self, tmp_path):
        plan = {
            "id": "001",
            "status": "completed",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "planned", "title": "X"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))
        assert result is None

    def test_skips_non_active_milestones(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [{
                "id": "001-M1",
                "status": "completed",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "planned", "title": "X"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))
        assert result is None

    def test_all_prs_merged(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "merged"},
                    {"id": "001-M1-PR2", "status": "merged"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))
        assert result is None

    def test_empty_directory(self, tmp_path):
        result = find_next_pr(str(tmp_path))
        assert result is None

    def test_handles_missing_optional_fields(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "planned"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_next_pr(str(tmp_path))

        assert result is not None
        assert result["pr_title"] == ""
        assert result["pr_branch"] == ""
