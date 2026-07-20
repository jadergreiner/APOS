"""Commit Tracking Kernel Pattern — Validates audit trail in sprint artifacts.

When projects using APOS complete sprints, they must track commit refs in:
- TASKS.md — "Commits de Rastreamento" section
- BOARD.md — "Audit Trail" section
- STATUS.md — "Commit Tracking" section
- USER_STORIES.md — "Commit(s)" field per story
- RETRO.md — "Commits Analisados" section

This validator ensures audit trail is complete before artifacts are finalized.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class CommitTrackingResult:
    """Result of commit tracking validation."""

    score: float  # 0.0-1.0
    status: str  # "PASS", "CONDITIONAL", "FAIL"
    issues: List[str] = field(default_factory=list)
    tracked_commits: List[str] = field(default_factory=list)
    untracked_tasks: List[str] = field(default_factory=list)
    validation_details: Dict[str, bool] = field(default_factory=dict)

    def passes(self) -> bool:
        """Check if validation passes (score >= 0.80)."""
        return self.score >= 0.80

    def is_conditional(self) -> bool:
        """Check if validation is conditional (0.60-0.80)."""
        return 0.60 <= self.score < 0.80


class CommitTrackingValidator:
    """Validates commit tracking across sprint artifacts.

    Usage:
        validator = CommitTrackingValidator(sprint_root="docs/releases/R0/sprint-0.0/")
        result = validator.validate()
        if result.passes():
            print("✅ All tasks tracked with commits")
        else:
            print(f"❌ Missing commits: {result.untracked_tasks}")
    """

    COMMIT_HASH_PATTERN = re.compile(r"^[a-f0-9]{7,40}$")
    TASKS_SECTION_PATTERN = re.compile(
        r"Commits? de Rastreamento|Audit Trail|Commit Tracking", re.IGNORECASE
    )

    def __init__(self, sprint_root: str):
        """Initialize validator with sprint root directory.

        Args:
            sprint_root: Path to sprint directory (e.g., docs/releases/R0/sprint-0.0/)
        """
        self.sprint_root = Path(sprint_root)
        self.tasks_file = self.sprint_root / "TASKS.md"
        self.board_file = self.sprint_root / "BOARD.md"
        self.status_file = self.sprint_root / "STATUS.md"
        self.user_stories_file = self.sprint_root / "USER_STORIES.md"
        self.retro_file = self.sprint_root / "RETRO.md"

    def validate(self) -> CommitTrackingResult:
        """Run complete validation across all sprint artifacts."""
        details = {}
        all_issues = []
        all_commits = set()
        all_untracked = []

        # Validate each artifact
        tasks_valid, tasks_commits, tasks_issues, tasks_untracked = (
            self._validate_tasks()
        )
        details["TASKS.md"] = tasks_valid
        all_commits.update(tasks_commits)
        all_issues.extend(tasks_issues)
        all_untracked.extend(tasks_untracked)

        board_valid, board_commits, board_issues = self._validate_board()
        details["BOARD.md"] = board_valid
        all_commits.update(board_commits)
        all_issues.extend(board_issues)

        status_valid, status_commits, status_issues = self._validate_status()
        details["STATUS.md"] = status_valid
        all_commits.update(status_commits)
        all_issues.extend(status_issues)

        (
            user_stories_valid,
            user_stories_commits,
            user_stories_issues,
        ) = self._validate_user_stories()
        details["USER_STORIES.md"] = user_stories_valid
        all_commits.update(user_stories_commits)
        all_issues.extend(user_stories_issues)

        retro_valid, retro_commits, retro_issues = self._validate_retro()
        details["RETRO.md"] = retro_valid
        all_commits.update(retro_commits)
        all_issues.extend(retro_issues)

        # Calculate score
        valid_files = sum(1 for v in details.values() if v)
        total_files = len(details)
        base_score = valid_files / total_files if total_files > 0 else 0.0

        # Adjust for untracked tasks
        if all_untracked:
            base_score *= 0.7  # Penalize untracked tasks heavily

        # Determine status
        if base_score >= 0.80:
            status = "PASS"
        elif base_score >= 0.60:
            status = "CONDITIONAL"
        else:
            status = "FAIL"

        return CommitTrackingResult(
            score=base_score,
            status=status,
            issues=all_issues,
            tracked_commits=sorted(list(all_commits)),
            untracked_tasks=all_untracked,
            validation_details=details,
        )

    def _validate_tasks(
        self,
    ) -> tuple[bool, set, List[str], List[str]]:
        """Validate TASKS.md has commit tracking section."""
        if not self.tasks_file.exists():
            return False, set(), ["TASKS.md not found"], []

        try:
            content = self.tasks_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return False, set(), [f"Error reading TASKS.md: {e}"], []

        if not content.strip():
            return False, set(), ["TASKS.md is empty"], []

        # Check for commit tracking section
        if not self._has_commit_section(content):
            return False, set(), ["TASKS.md missing 'Commits de Rastreamento' section"], []

        commits = self._extract_commits(content)
        issues = []
        untracked = []

        # Extract task list and check each has commit
        task_pattern = re.compile(r"^\|\s*T\d+\.\d+\.\w+\s*\|")
        tasks_in_file = task_pattern.findall(content)

        if tasks_in_file:
            # For each complete task (marked as ✅ COMPLETO or similar)
            complete_pattern = re.compile(
                r"✅|✔|COMPLETO|COMPLETE", re.IGNORECASE
            )
            complete_count = len(complete_pattern.findall(content))

            if complete_count > 0 and len(commits) == 0:
                issues.append(
                    "Tasks marked complete but no commits referenced in section"
                )
                untracked = tasks_in_file

        return len(commits) > 0 or not tasks_in_file, commits, issues, untracked

    def _validate_board(self) -> tuple[bool, set, List[str]]:
        """Validate BOARD.md has audit trail section."""
        if not self.board_file.exists():
            return False, set(), ["BOARD.md not found"]

        try:
            content = self.board_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return False, set(), [f"Error reading BOARD.md: {e}"]

        if not content.strip():
            return False, set(), ["BOARD.md is empty"]

        has_section = self._has_commit_section(content)
        commits = self._extract_commits(content)

        if not has_section:
            return False, commits, ["BOARD.md missing 'Audit Trail' or tracking section"]

        return True, commits, []

    def _validate_status(self) -> tuple[bool, set, List[str]]:
        """Validate STATUS.md has commit tracking section."""
        if not self.status_file.exists():
            return False, set(), ["STATUS.md not found"]

        try:
            content = self.status_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return False, set(), [f"Error reading STATUS.md: {e}"]

        if not content.strip():
            return False, set(), ["STATUS.md is empty"]

        has_section = self._has_commit_section(content)
        commits = self._extract_commits(content)

        if not has_section:
            return False, commits, ["STATUS.md missing 'Commit Tracking' or audit section"]

        return True, commits, []

    def _validate_user_stories(self) -> tuple[bool, set, List[str]]:
        """Validate USER_STORIES.md has commits for stories."""
        if not self.user_stories_file.exists():
            return True, set(), []  # Optional file

        try:
            content = self.user_stories_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return False, set(), [f"Error reading USER_STORIES.md: {e}"]

        if not content.strip():
            return True, set(), []  # Empty but valid

        commits = self._extract_commits(content)

        # Check if stories reference commits
        story_pattern = re.compile(r"^##\s+US-", re.MULTILINE)
        stories = story_pattern.findall(content)

        if stories and not commits:
            return False, commits, ["User stories found but no commits referenced"]

        return True, commits, []

    def _validate_retro(self) -> tuple[bool, set, List[str]]:
        """Validate RETRO.md has commits analyzed section."""
        if not self.retro_file.exists():
            return True, set(), []  # Optional file

        try:
            content = self.retro_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return False, set(), [f"Error reading RETRO.md: {e}"]

        if not content.strip():
            return True, set(), []  # Empty but valid

        commits = self._extract_commits(content)
        return True, commits, []

    def _has_commit_section(self, content: str) -> bool:
        """Check if content has commit tracking section header."""
        return bool(self.TASKS_SECTION_PATTERN.search(content))

    def _extract_commits(self, content: str) -> set:
        """Extract commit hashes from content.

        Looks for:
        - commit_hash — commit message
        - [commit_hash]
        - `commit_hash`
        """
        commits = set()

        # Pattern 1: hash — message
        pattern1 = re.compile(r"(?:^|\s)([a-f0-9]{7,40})\s*(?:—|-|:)\s*", re.MULTILINE)
        commits.update(m.group(1) for m in pattern1.finditer(content))

        # Pattern 2: [hash]
        pattern2 = re.compile(r"\[([a-f0-9]{7,40})\]")
        commits.update(m.group(1) for m in pattern2.finditer(content))

        # Pattern 3: `hash`
        pattern3 = re.compile(r"`([a-f0-9]{7,40})`")
        commits.update(m.group(1) for m in pattern3.finditer(content))

        # Pattern 4: Inline links or references
        pattern4 = re.compile(r"(?:commit|ref|sha)[\s:]+([a-f0-9]{7,40})", re.IGNORECASE)
        commits.update(m.group(1) for m in pattern4.finditer(content))

        return {c for c in commits if self.COMMIT_HASH_PATTERN.match(c)}
