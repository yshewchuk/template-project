import os

import pytest
import yaml

from detect_impl_pr import find_impl_pr


def write_plan(directory, filename, plan):
    path = os.path.join(directory, filename)
    with open(path, "w") as f:
        yaml.dump(plan, f)
    return path


class TestFindImplPR:
    def test_matches_by_branch(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "in-progress", "branch": "feat/001-m1-game-state"},
                    {"id": "001-M1-PR2", "status": "planned", "branch": "feat/001-m1-reveal"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_impl_pr("feat/001-m1-game-state", str(tmp_path))

        assert result is not None
        assert result["pr_id"] == "001-M1-PR1"
        assert result["milestone_id"] == "001-M1"

    def test_falls_back_to_in_progress_status(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "in-progress", "branch": "feat/something-else"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_impl_pr("impl/001-M1-PR1", str(tmp_path))

        assert result is not None
        assert result["pr_id"] == "001-M1-PR1"

    def test_skips_completed_milestones(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [{
                "id": "001-M1",
                "status": "completed",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "in-progress", "branch": "feat/match"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_impl_pr("feat/match", str(tmp_path))
        assert result is None

    def test_no_match(self, tmp_path):
        plan = {
            "id": "001",
            "milestones": [{
                "id": "001-M1",
                "status": "in-progress",
                "pull_requests": [
                    {"id": "001-M1-PR1", "status": "merged", "branch": "feat/other"},
                ],
            }],
        }
        write_plan(str(tmp_path), "001.yaml", plan)
        result = find_impl_pr("feat/no-match", str(tmp_path))
        assert result is None

    def test_empty_directory(self, tmp_path):
        result = find_impl_pr("feat/anything", str(tmp_path))
        assert result is None
