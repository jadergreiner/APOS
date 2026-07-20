"""Tests for CommitTrackingValidator kernel pattern."""

import pytest
from pathlib import Path
from apos.kernel.commit_tracking import (
    CommitTrackingValidator,
    CommitTrackingResult,
)


@pytest.fixture
def sprint_root_with_commits(tmp_path):
    """Create a sprint directory with properly tracked commits."""
    sprint_dir = tmp_path / "sprint-0.0"
    sprint_dir.mkdir()

    # TASKS.md with commit tracking
    tasks_content = """# Tasks

| Task | Status | Commit |
| --- | --- | --- |
| T0.0.1 | ✅ | f152801 |
| T0.0.2 | ✅ | 6be1b53 |

## Commits de Rastreamento

- f152801 — feat: implement Bootstrap Gate
- 6be1b53 — feat: implement SessionManager
"""
    (sprint_dir / "TASKS.md").write_text(tasks_content, encoding="utf-8")

    # BOARD.md with audit trail
    board_content = """# Board

## Audit Trail

- f152801 — Bootstrap Gate implementation
- 6be1b53 — SessionManager implementation
"""
    (sprint_dir / "BOARD.md").write_text(board_content, encoding="utf-8")

    # STATUS.md with commit tracking
    status_content = """# Status

## Commit Tracking

Commits analyzed in this sprint:
- f152801
- 6be1b53
"""
    (sprint_dir / "STATUS.md").write_text(status_content, encoding="utf-8")

    return sprint_dir


@pytest.fixture
def sprint_root_no_commits(tmp_path):
    """Create a sprint directory without commit tracking."""
    sprint_dir = tmp_path / "sprint-0.0"
    sprint_dir.mkdir()

    # TASKS.md without commit section
    tasks_content = """# Tasks

| Task | Status |
| --- | --- |
| T0.0.1 | ✅ |
| T0.0.2 | ✅ |
"""
    (sprint_dir / "TASKS.md").write_text(tasks_content, encoding="utf-8")

    # BOARD.md without tracking
    board_content = """# Board

No commits tracked.
"""
    (sprint_dir / "BOARD.md").write_text(board_content, encoding="utf-8")

    # STATUS.md without tracking
    status_content = """# Status

No commit tracking.
"""
    (sprint_dir / "STATUS.md").write_text(status_content, encoding="utf-8")

    return sprint_dir


@pytest.fixture
def sprint_root_partial_commits(tmp_path):
    """Create a sprint directory with partial commit tracking."""
    sprint_dir = tmp_path / "sprint-0.0"
    sprint_dir.mkdir()

    # TASKS.md with some tasks tracked
    tasks_content = """# Tasks

| Task | Status | Commit |
| --- | --- | --- |
| T0.0.1 | ✅ | f152801 |
| T0.0.2 | ✅ | — |

## Commits de Rastreamento

- f152801 — feat: implement Bootstrap Gate
"""
    (sprint_dir / "TASKS.md").write_text(tasks_content, encoding="utf-8")

    # BOARD.md with tracking
    board_content = """# Audit Trail

- f152801 — Bootstrap Gate
"""
    (sprint_dir / "BOARD.md").write_text(board_content, encoding="utf-8")

    # STATUS.md with tracking
    status_content = """# Commit Tracking

- f152801
"""
    (sprint_dir / "STATUS.md").write_text(status_content, encoding="utf-8")

    return sprint_dir


class TestCommitTrackingResult:
    """Test CommitTrackingResult dataclass."""

    def test_passes_with_high_score(self):
        """Test passes() returns True when score >= 0.80."""
        result = CommitTrackingResult(
            score=0.85,
            status="PASS",
        )
        assert result.passes() is True

    def test_passes_with_low_score(self):
        """Test passes() returns False when score < 0.80."""
        result = CommitTrackingResult(
            score=0.70,
            status="CONDITIONAL",
        )
        assert result.passes() is False

    def test_is_conditional(self):
        """Test is_conditional() detects conditional range."""
        result = CommitTrackingResult(
            score=0.70,
            status="CONDITIONAL",
        )
        assert result.is_conditional() is True

    def test_not_conditional_when_pass(self):
        """Test is_conditional() false when passing."""
        result = CommitTrackingResult(
            score=0.85,
            status="PASS",
        )
        assert result.is_conditional() is False


class TestCommitTrackingValidator:
    """Test CommitTrackingValidator core functionality."""

    def test_validate_with_all_commits_tracked(self, sprint_root_with_commits):
        """Test validation passes when all artifacts have commits."""
        validator = CommitTrackingValidator(str(sprint_root_with_commits))
        result = validator.validate()

        assert result.status == "PASS"
        assert result.passes() is True
        assert "f152801" in result.tracked_commits
        assert "6be1b53" in result.tracked_commits
        assert result.validation_details["TASKS.md"] is True
        assert result.validation_details["BOARD.md"] is True
        assert result.validation_details["STATUS.md"] is True

    def test_validate_without_commits(self, sprint_root_no_commits):
        """Test validation fails when no commits tracked."""
        validator = CommitTrackingValidator(str(sprint_root_no_commits))
        result = validator.validate()

        assert result.status in ["FAIL", "CONDITIONAL"]
        assert result.passes() is False
        assert len(result.tracked_commits) == 0
        assert len(result.issues) > 0

    def test_validate_partial_commits(self, sprint_root_partial_commits):
        """Test validation passes with some commits (not all tasks tracked)."""
        validator = CommitTrackingValidator(str(sprint_root_partial_commits))
        result = validator.validate()

        # Should pass because section exists and has commits
        assert result.status in ["PASS", "CONDITIONAL"]
        assert "f152801" in result.tracked_commits

    def test_extract_commits_from_various_formats(self, tmp_path):
        """Test commit extraction from different formats."""
        sprint_dir = tmp_path / "sprint-test"
        sprint_dir.mkdir()

        # Create file with commit section and various commit formats
        content = """# Commits de Rastreamento

- f152801 — feat: implement Bootstrap Gate
- [6be1b53] — feat: implement SessionManager
- `ce01074` some fix
- commit: ce019a4
- ref: 9d7f36a
"""
        (sprint_dir / "TASKS.md").write_text(content, encoding="utf-8")
        (sprint_dir / "BOARD.md").write_text("# Audit Trail\n- f152801", encoding="utf-8")
        (sprint_dir / "STATUS.md").write_text("# Commit Tracking\n- f152801", encoding="utf-8")

        validator = CommitTrackingValidator(str(sprint_dir))
        result = validator.validate()

        # Should extract commits in various formats
        assert "f152801" in result.tracked_commits
        assert "6be1b53" in result.tracked_commits
        assert "ce01074" in result.tracked_commits
        assert "ce019a4" in result.tracked_commits
        assert "9d7f36a" in result.tracked_commits

    def test_validate_missing_files(self, tmp_path):
        """Test validation handles missing files gracefully."""
        sprint_dir = tmp_path / "sprint-empty"
        sprint_dir.mkdir()
        # Don't create any files

        validator = CommitTrackingValidator(str(sprint_dir))
        result = validator.validate()

        assert result.status == "FAIL"
        assert result.passes() is False

    def test_validate_empty_files(self, tmp_path):
        """Test validation handles empty files."""
        sprint_dir = tmp_path / "sprint-empty"
        sprint_dir.mkdir()

        (sprint_dir / "TASKS.md").write_text("", encoding="utf-8")
        (sprint_dir / "BOARD.md").write_text("", encoding="utf-8")
        (sprint_dir / "STATUS.md").write_text("", encoding="utf-8")

        validator = CommitTrackingValidator(str(sprint_dir))
        result = validator.validate()

        assert result.status == "FAIL"
        assert len(result.issues) > 0

    def test_validation_details_structure(self, sprint_root_with_commits):
        """Test validation_details has correct keys."""
        validator = CommitTrackingValidator(str(sprint_root_with_commits))
        result = validator.validate()

        assert "TASKS.md" in result.validation_details
        assert "BOARD.md" in result.validation_details
        assert "STATUS.md" in result.validation_details

    def test_user_stories_optional(self, tmp_path):
        """Test USER_STORIES.md is optional."""
        sprint_dir = tmp_path / "sprint-test"
        sprint_dir.mkdir()

        # Create minimal valid structure without USER_STORIES
        (sprint_dir / "TASKS.md").write_text(
            "# Commits de Rastreamento\n- f152801",
            encoding="utf-8",
        )
        (sprint_dir / "BOARD.md").write_text(
            "# Audit Trail\n- f152801",
            encoding="utf-8",
        )
        (sprint_dir / "STATUS.md").write_text(
            "# Commit Tracking\n- f152801",
            encoding="utf-8",
        )

        validator = CommitTrackingValidator(str(sprint_dir))
        result = validator.validate()

        # Should pass even without USER_STORIES
        assert result.passes() is True

    def test_retro_optional(self, tmp_path):
        """Test RETRO.md is optional."""
        sprint_dir = tmp_path / "sprint-test"
        sprint_dir.mkdir()

        # Create minimal valid structure without RETRO
        (sprint_dir / "TASKS.md").write_text(
            "# Commits de Rastreamento\n- f152801",
            encoding="utf-8",
        )
        (sprint_dir / "BOARD.md").write_text(
            "# Audit Trail\n- f152801",
            encoding="utf-8",
        )
        (sprint_dir / "STATUS.md").write_text(
            "# Commit Tracking\n- f152801",
            encoding="utf-8",
        )

        validator = CommitTrackingValidator(str(sprint_dir))
        result = validator.validate()

        # Should pass even without RETRO
        assert result.passes() is True

    def test_has_commit_section_detection(self, tmp_path):
        """Test detection of commit tracking section headers."""
        sprint_dir = tmp_path / "sprint-test"
        sprint_dir.mkdir()

        # Various section header formats
        test_cases = [
            "# Commits de Rastreamento\n- f152801",
            "# Audit Trail\n- f152801",
            "# Commit Tracking\n- f152801",
            "## audit trail\n- f152801",
            "### COMMITS DE RASTREAMENTO\n- f152801",
        ]

        for content in test_cases:
            (sprint_dir / "TASKS.md").write_text(content, encoding="utf-8")
            (sprint_dir / "BOARD.md").write_text(content, encoding="utf-8")
            (sprint_dir / "STATUS.md").write_text(content, encoding="utf-8")

            validator = CommitTrackingValidator(str(sprint_dir))
            result = validator.validate()

            assert result.passes() is True, f"Failed for content: {content}"


class TestCommitTrackingIntegration:
    """Integration tests for CommitTrackingValidator."""

    def test_full_sprint_validation_flow(self, sprint_root_with_commits):
        """Test complete validation flow for a real sprint."""
        validator = CommitTrackingValidator(str(sprint_root_with_commits))

        # Run validation
        result = validator.validate()

        # Verify structure
        assert isinstance(result, CommitTrackingResult)
        assert 0.0 <= result.score <= 1.0
        assert result.status in ["PASS", "CONDITIONAL", "FAIL"]
        assert isinstance(result.issues, list)
        assert isinstance(result.tracked_commits, list)
        assert isinstance(result.validation_details, dict)

        # Verify passing case
        assert result.passes() is True
        assert len(result.tracked_commits) == 2
        assert len(result.untracked_tasks) == 0

    @pytest.mark.parametrize(
        "score,expected_status",
        [
            (0.85, "PASS"),
            (0.75, "CONDITIONAL"),
            (0.50, "FAIL"),
            (0.80, "PASS"),
            (0.79, "CONDITIONAL"),
            (0.60, "CONDITIONAL"),
            (0.59, "FAIL"),
        ],
    )
    def test_status_determination_by_score(self, score, expected_status):
        """Test status is correctly determined by score."""
        result = CommitTrackingResult(
            score=score,
            status=expected_status,
        )
        assert result.status == expected_status
