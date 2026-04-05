import os

import pytest
import yaml

from detect_completed_milestone import find_newly_completed


class TestFindNewlyCompleted:
    def test_detects_new_completion(self):
        current = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
            ],
        })
        old = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "in-progress"},
            ],
        })
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=current,
            old_content=old,
        )

        assert result is not None
        assert result["plan_id"] == "001"
        assert result["milestone_id"] == "001-M1"

    def test_ignores_already_completed(self):
        current = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
            ],
        })
        old = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
            ],
        })
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=current,
            old_content=old,
        )
        assert result is None

    def test_no_completed_milestones(self):
        current = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "in-progress"},
            ],
        })
        old = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "in-progress"},
            ],
        })
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=current,
            old_content=old,
        )
        assert result is None

    def test_old_content_missing_treats_as_empty(self):
        current = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
            ],
        })
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=current,
            old_content="",
        )

        assert result is not None
        assert result["milestone_id"] == "001-M1"

    def test_multiple_milestones_only_new_one_detected(self):
        current = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
                {"id": "001-M2", "status": "completed"},
            ],
        })
        old = yaml.dump({
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
                {"id": "001-M2", "status": "in-progress"},
            ],
        })
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=current,
            old_content=old,
        )

        assert result is not None
        assert result["milestone_id"] == "001-M2"

    def test_invalid_current_content(self):
        result = find_newly_completed(
            plan_file="plan.yaml",
            current_content=": : : invalid",
            old_content="",
        )
        assert result is None

    def test_reads_from_file(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [
                {"id": "001-M1", "status": "completed"},
            ],
        }
        path = os.path.join(str(tmp_path), "001.yaml")
        with open(path, "w") as f:
            yaml.dump(plan, f)

        result = find_newly_completed(
            plan_file=path,
            old_content=yaml.dump({"milestones": []}),
        )

        assert result is not None
        assert result["milestone_id"] == "001-M1"
