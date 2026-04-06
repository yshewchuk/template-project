import pytest

from classify_pr import classify_pr


class TestClassifyPR:
    def test_verification_by_branch(self):
        result = classify_pr("verify/001-M1", [])
        assert result["is_verification"] is True
        assert result["is_acceptance"] is False
        assert result["is_implementation"] is False

    def test_acceptance_by_branch(self):
        result = classify_pr("accept/001-M1-PR1", [])
        assert result["is_acceptance"] is True
        assert result["is_verification"] is False
        assert result["is_implementation"] is False

    def test_acceptance_by_label(self):
        result = classify_pr("some-branch", ["work-cycle/acceptance"])
        assert result["is_acceptance"] is True

    def test_implementation_by_impl_branch(self):
        result = classify_pr("impl/001-M1-PR1", [])
        assert result["is_implementation"] is True
        assert result["is_verification"] is False
        assert result["is_acceptance"] is False

    def test_implementation_by_feat_branch(self):
        result = classify_pr("feat/001-m1-game-state", [])
        assert result["is_implementation"] is True

    def test_implementation_by_label(self):
        result = classify_pr("random-branch", ["work-cycle/implementation"])
        assert result["is_implementation"] is True

    def test_unrelated_branch(self):
        result = classify_pr("main", [])
        assert result["is_verification"] is False
        assert result["is_acceptance"] is False
        assert result["is_implementation"] is False

    def test_unrelated_branch_with_unrelated_labels(self):
        result = classify_pr("fix/typo", ["bugfix", "docs"])
        assert result["is_verification"] is False
        assert result["is_acceptance"] is False
        assert result["is_implementation"] is False

    def test_branch_with_verify_in_middle(self):
        result = classify_pr("feat/verify-email", [])
        assert result["is_verification"] is False

    def test_branch_with_accept_in_middle(self):
        result = classify_pr("feat/accept-cookies", [])
        assert result["is_acceptance"] is False

    def test_empty_branch_and_labels(self):
        result = classify_pr("", [])
        assert result["is_verification"] is False
        assert result["is_acceptance"] is False
        assert result["is_implementation"] is False

    def test_multiple_labels(self):
        result = classify_pr("accept/123", ["work-cycle/acceptance", "work-cycle/implementation"])
        assert result["is_acceptance"] is True
        assert result["is_implementation"] is True
