import os
import tempfile

import pytest
import yaml

from detect_milestone import find_activated_milestone


def write_plan(tmpdir, filename, plan):
    path = os.path.join(tmpdir, filename)
    with open(path, "w") as f:
        yaml.dump(plan, f)
    return path


class TestFindActivatedMilestone:
    def test_finds_in_progress_milestone(self, tmp_path):
        plan = {
            "id": "001",
            "status": "in-progress",
            "milestones": [
                {"id": "001-M1", "status": "in-progress"},
            ],
        }
        path = write_plan(str(tmp_path), "001.yaml", plan)
        result = find_activated_milestone([path])

        assert result is not None
        assert result["plan_id"] == "001"
        assert result["milestone_id"] == "001-M1"
        assert result["plan_file"] == path

    def test_skips_completed_milestones(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
                {"id": "001-M2", "status": "planned"},
            ],
        }
        path = write_plan(str(tmp_path), "001.yaml", plan)
        result = find_activated_milestone([path])
        assert result is None

    def test_finds_first_in_progress(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
                {"id": "001-M2", "status": "in-progress"},
                {"id": "001-M3", "status": "in-progress"},
            ],
        }
        path = write_plan(str(tmp_path), "001.yaml", plan)
        result = find_activated_milestone([path])

        assert result is not None
        assert result["milestone_id"] == "001-M2"

    def test_empty_plan_list(self):
        result = find_activated_milestone([])
        assert result is None

    def test_nonexistent_file(self):
        result = find_activated_milestone(["/nonexistent/path.yaml"])
        assert result is None

    def test_no_milestones_key(self, tmp_path):
        plan = {"id": "001", "status": "in-progress"}
        path = write_plan(str(tmp_path), "001.yaml", plan)
        result = find_activated_milestone([path])
        assert result is None

    def test_multiple_plan_files(self, tmp_path):
        plan1 = {
            "id": "001",
            "milestones": [{"id": "001-M1", "status": "completed"}],
        }
        plan2 = {
            "id": "002",
            "milestones": [{"id": "002-M1", "status": "in-progress"}],
        }
        path1 = write_plan(str(tmp_path), "001.yaml", plan1)
        path2 = write_plan(str(tmp_path), "002.yaml", plan2)
        result = find_activated_milestone([path1, path2])

        assert result is not None
        assert result["plan_id"] == "002"
        assert result["milestone_id"] == "002-M1"

    def test_invalid_yaml(self, tmp_path):
        path = os.path.join(str(tmp_path), "bad.yaml")
        with open(path, "w") as f:
            f.write(": : : invalid yaml [[[")
        result = find_activated_milestone([path])
        assert result is None
