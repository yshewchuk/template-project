import pytest

from render_tracking_comment import render_tracking_comment


class TestRenderTrackingComment:
    STAGES = [
        {"number": 1, "type": "contribute", "persona": "Developer", "skipped": False},
        {"number": 2, "type": "contribute", "persona": "Developer", "skipped": False},
        {"number": 3, "type": "review", "persona": "Tech Lead", "skipped": False},
        {"number": 4, "type": "review", "persona": "Acceptance Tester", "skipped": False},
        {"number": 5, "type": "review", "persona": "Product Manager", "skipped": False},
    ]

    def test_header_contains_work_cycle_name(self):
        result = render_tracking_comment(self.STAGES, 1, "implementation", "Developer", "contribute")
        assert "## PR Progress: implementation work cycle" in result

    def test_active_stage_marked(self):
        result = render_tracking_comment(self.STAGES, 3, "implementation", "Tech Lead", "review")
        assert "**Active**" in result
        lines = result.split("\n")
        for line in lines:
            if "Tech Lead" in line and "3" in line:
                assert "Active" in line
                break
        else:
            pytest.fail("Active stage not found in output")

    def test_previous_stages_done(self):
        result = render_tracking_comment(self.STAGES, 3, "implementation", "Tech Lead", "review")
        lines = result.split("\n")
        done_count = sum(1 for line in lines if "Done" in line)
        assert done_count == 2

    def test_future_stages_pending(self):
        result = render_tracking_comment(self.STAGES, 3, "implementation", "Tech Lead", "review")
        lines = result.split("\n")
        pending_count = sum(1 for line in lines if line.strip().endswith("Pending |"))
        assert pending_count == 2

    def test_skipped_stages(self):
        stages = [
            {"number": 1, "type": "contribute", "persona": "Developer", "skipped": False},
            {"number": 2, "type": "contribute", "persona": "Operator", "skipped": True},
            {"number": 3, "type": "review", "persona": "Tech Lead", "skipped": False},
        ]
        result = render_tracking_comment(stages, 1, "implementation", "Developer", "contribute")
        assert "Skipped (Phase 1)" in result

    def test_contribute_icon(self):
        result = render_tracking_comment(self.STAGES, 1, "implementation", "Developer", "contribute")
        assert "\U0001f528 contribute" in result

    def test_review_icon(self):
        result = render_tracking_comment(self.STAGES, 3, "implementation", "Tech Lead", "review")
        assert "\U0001f440 review" in result

    def test_current_stage_footer(self):
        result = render_tracking_comment(self.STAGES, 3, "implementation", "Tech Lead", "review")
        assert "Current stage: **3 \u2014 Tech Lead (review)**" in result

    def test_table_has_correct_columns(self):
        result = render_tracking_comment(self.STAGES, 1, "implementation", "Developer", "contribute")
        assert "| # | Type | Agent | Status |" in result
        assert "|---|------|-------|--------|" in result

    def test_single_stage(self):
        stages = [{"number": 1, "type": "contribute", "persona": "Scrum Master", "skipped": False}]
        result = render_tracking_comment(stages, 1, "improve", "Scrum Master", "contribute")
        assert "Scrum Master" in result
        assert "Active" in result

    def test_all_stages_done(self):
        result = render_tracking_comment(self.STAGES, 6, "implementation", "Nobody", "review")
        lines = result.split("\n")
        done_count = sum(1 for line in lines if "Done" in line)
        assert done_count == 5
