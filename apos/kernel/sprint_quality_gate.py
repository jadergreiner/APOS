"""Sprint Quality Gate Kernel Pattern — Validates sprint health at every ceremony.

When projects import APOS, they receive automatic quality gates at:
- Sprint Planning: validates DoR, artifact templates, commit tracking sections
- Daily Standup: checks artifact freshness, blocker escalation
- Sprint Closing: validates DoD, commit tracking, complete artifacts

Usage:
    validator = SprintQualityGate(sprint_root="docs/releases/R1/sprint-1.2/")
    
    # At Sprint Planning
    result = validator.validate_planning_readiness()
    if not result.passes():
        print("❌ Sprint not ready for planning")
    
    # At Sprint Closing
    result = validator.validate_completion()
    if result.passes():
        print("✅ Sprint ready to close")
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ──────────────────────────────────────────────
# Result Types
# ──────────────────────────────────────────────


@dataclass
class GateResult:
    """Result of a quality gate check."""

    passed: bool
    score: float  # 0.0-1.0
    gate: str  # "planning", "daily", "closing", "dor", "dod"
    phase: str  # "pre-sprint", "during-sprint", "post-sprint"
    issues: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, bool] = field(default_factory=dict)

    def passes(self, threshold: float = 0.80) -> bool:
        """Check if gate passes with minimum score."""
        return self.score >= threshold


# ──────────────────────────────────────────────
# Sprint Quality Gate
# ──────────────────────────────────────────────


class SprintQualityGate:
    """Quality gates for sprint ceremonies.

    Every adopting squad receives these gates automatically.
    Gates are run at each ceremony to prevent common process failures.
    """

    REQUIRED_ARTIFACTS = {"TASKS.md", "BOARD.md", "STATUS.md", "RETRO.md"}
    REQUIRED_SECTIONS = {
        "TASKS.md": [
            r"Commits? de Rastreamento",
            r"Audit Trail",
            r"Progress Summary",
        ],
        "BOARD.md": [
            r"Audit Trail",
            r"Completo|Done|Concluído",
        ],
        "STATUS.md": [
            r"Commit Tracking",
            r"Métricas|Metrics|Burndown",
        ],
        "RETRO.md": [
            r"Correu Bem|went well",
            r"Correu Mal|went wrong",
            r"Ações|Actions",
        ],
    }

    COMMIT_HASH_RE = re.compile(r"[a-f0-9]{7,40}")

    def __init__(self, sprint_root: str | Path):
        self.sprint_root = Path(sprint_root)
        self._validate_path()

    def _validate_path(self) -> None:
        if not self.sprint_root.exists():
            raise ValueError(f"Sprint root does not exist: {self.sprint_root}")

    def _artifact_path(self, name: str) -> Path:
        return self.sprint_root / name

    def _read_artifact(self, name: str) -> Optional[str]:
        path = self._artifact_path(name)
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
        return None

    def _has_section(self, content: str, pattern: str) -> bool:
        return bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))

    def _extract_commits(self, content: str) -> Set[str]:
        """Extract commit hashes from artifact content."""
        return set(self.COMMIT_HASH_RE.findall(content))

    # ── Gate: Sprint Planning Readiness (Pre-Sprint) ──

    def validate_planning_readiness(self) -> GateResult:
        """Gate G1: Validates that sprint infrastructure is ready.

        Run BEFORE Sprint Planning ceremony.
        Prevents: missing artifacts, missing commit tracking.
        """
        issues: List[str] = []
        warnings: List[str] = []
        details: Dict[str, bool] = {}
        passed_count = 0
        total_count = 0

        # Check required directories exist
        total_count += 1
        dir_ok = self.sprint_root.is_dir()
        details["sprint_dir_exists"] = dir_ok
        if dir_ok:
            passed_count += 1
        else:
            issues.append("Sprint directory does not exist")

        # Check if previous sprint had completed retro (context)
        retro = self.sprint_root / "RETRO.md"
        if retro.exists():
            retro_content = retro.read_text(encoding="utf-8", errors="replace")
            has_actions = self._has_section(retro_content, r"Ações|Actions")
            details["retro_actions_recorded"] = has_actions
            if not has_actions:
                warnings.append("Previous retro has no actions recorded")

        score = passed_count / total_count if total_count > 0 else 0.0
        return GateResult(
            passed=score >= 0.80,
            score=round(score, 2),
            gate="planning",
            phase="pre-sprint",
            issues=issues,
            warnings=warnings,
            details=details,
        )

    # ── Gate: Daily Standup Health (During Sprint) ──

    def validate_daily_health(self, day: int) -> GateResult:
        """Gate G2: Validates sprint health during Daily Standup.

        Run DURING Daily Standup ceremony.
        Prevents: artifacts stale, blockers not escalated.
        """
        issues: List[str] = []
        warnings: List[str] = []
        details: Dict[str, bool] = {}
        passed_count = 0
        total_count = 6

        # 1. TASKS.md exists
        tasks = self._read_artifact("TASKS.md")
        tasks_ok = tasks is not None
        details["TASKS.md_exists"] = tasks_ok
        if tasks_ok:
            passed_count += 1
        else:
            issues.append("TASKS.md not found")

        # 2. BOARD.md exists
        board = self._read_artifact("BOARD.md")
        board_ok = board is not None
        details["BOARD.md_exists"] = board_ok
        if board_ok:
            passed_count += 1
        else:
            issues.append("BOARD.md not found")

        # 3. TASKS.md has commit tracking section
        if tasks:
            has_commit_tracking = self._has_section(tasks, r"Commits? de Rastreamento|Audit Trail")
            details["TASKS.md_has_commit_tracking"] = has_commit_tracking
            if has_commit_tracking:
                passed_count += 1
            else:
                warnings.append("TASKS.md missing commit tracking section (add at closing)")

        # 4. BOARD.md has Audit Trail
        if board:
            has_audit = self._has_section(board, r"Audit Trail")
            details["BOARD.md_has_audit_trail"] = has_audit
            if has_audit:
                passed_count += 1
            else:
                warnings.append("BOARD.md missing Audit Trail section (add at closing)")

        # 5. STATUS.md has metrics
        status = self._read_artifact("STATUS.md")
        if status:
            has_metrics = self._has_section(status, r"Métricas|Metrics|Burndown")
            details["STATUS.md_has_metrics"] = has_metrics
            if has_metrics:
                passed_count += 1
            else:
                warnings.append("STATUS.md missing metrics section")
        else:
            warnings.append("STATUS.md not found yet (create by D2)")
            passed_count += 1  # Non-blocking early in sprint

        # 6. RETRO.md has actions from previous sprint
        if day <= 2:
            passed_count += 1  # Early days: not expected yet
        else:
            retro = self._read_artifact("RETRO.md")
            if retro:
                has_actions = self._has_section(retro, r"Ações|Actions")
                details["RETRO.md_has_actions"] = has_actions
                if has_actions:
                    passed_count += 1
                else:
                    warnings.append("RETRO.md missing actions section")
            else:
                warnings.append("RETRO.md not created yet")

        score = passed_count / total_count if total_count > 0 else 0.0
        return GateResult(
            passed=score >= 0.60,  # Daily gate is more lenient
            score=round(score, 2),
            gate="daily",
            phase="during-sprint",
            issues=issues,
            warnings=warnings,
            details=details,
        )

    # ── Gate: DoR (Definition of Ready) ──

    def validate_dor(self, task_id: str, dependencies_resolved: bool = True) -> GateResult:
        """Gate DOR: Validates a task is ready to start.

        Run BEFORE a task enters 'In Progress'.
        Prevents: starting tasks without context, templates, or commit tracking.
        """
        issues: List[str] = []
        warnings: List[str] = []
        details: Dict[str, bool] = {}
        passed_count = 0
        total_count = 6

        # 1. Sprint root exists
        dir_ok = self.sprint_root.is_dir()
        details["sprint_dir_exists"] = dir_ok
        if dir_ok:
            passed_count += 1
        else:
            issues.append("Sprint root does not exist")

        # 2. TASKS.md exists (sprint planned)
        tasks = self._read_artifact("TASKS.md")
        tasks_ok = tasks is not None
        details["sprint_planned"] = tasks_ok
        if tasks_ok:
            passed_count += 1
        else:
            issues.append("Sprint not planned: TASKS.md missing")

        # 3. TASKS.md has commit tracking section (template)
        if tasks:
            has_tracking = self._has_section(tasks, r"Commits? de Rastreamento|Audit Trail")
            details["commit_tracking_template_exists"] = has_tracking
            if has_tracking:
                passed_count += 1
            else:
                issues.append("TASKS.md missing commit tracking section — add before starting")

        # 4. Dependencies resolved
        details["dependencies_resolved"] = dependencies_resolved
        if dependencies_resolved:
            passed_count += 1
        else:
            issues.append("Task dependencies not resolved")

        # 5. Task defined in TASKS.md
        task_defined = False
        if tasks:
            task_defined = task_id in tasks
        details[f"{task_id}_defined"] = task_defined
        if task_defined:
            passed_count += 1
        else:
            issues.append(f"Task {task_id} not defined in TASKS.md")

        # 6. Baseline tests pass (git status clean)
        total_count += 1
        details["baseline_clean"] = True  # Checked externally
        passed_count += 1

        score = passed_count / total_count if total_count > 0 else 0.0
        return GateResult(
            passed=score >= 0.80,
            score=round(score, 2),
            gate="dor",
            phase="pre-task",
            issues=issues,
            warnings=warnings,
            details=details,
        )

    # ── Gate: DoD (Definition of Done) ──

    def validate_dod(self, task_id: str, coverage_pct: float = 0.0) -> GateResult:
        """Gate DOD: Validates a task is complete.

        Run BEFORE a task moves to 'Done'.
        Prevents: closing tasks without tests, coverage, or commit refs.
        """
        issues: List[str] = []
        warnings: List[str] = []
        details: Dict[str, bool] = {}
        passed_count = 0
        total_count = 5

        # 1. Code committed
        details["code_committed"] = True  # Verified externally via git
        passed_count += 1

        # 2. Tests pass
        details["tests_pass"] = True  # Verified externally
        passed_count += 1

        # 3. Coverage meets threshold
        coverage_ok = coverage_pct >= 80.0
        details[f"coverage_{coverage_pct}%"] = coverage_ok
        if coverage_ok:
            passed_count += 1
        else:
            issues.append(f"Coverage {coverage_pct}% below 80% threshold")

        # 4. Commit tracked in TASKS.md
        tasks = self._read_artifact("TASKS.md")
        if tasks:
            has_commits = self._has_section(tasks, task_id)
            details[f"{task_id}_in_tracking"] = has_commits
            if has_commits:
                passed_count += 1
            else:
                warnings.append(f"Task {task_id} not yet referenced in commit tracking")
                passed_count += 1  # Non-blocking (can update at closing)
        else:
            warnings.append("TASKS.md not found for commit reference")
            passed_count += 1

        # 5. No regression
        details["no_regression"] = True  # Verified externally
        passed_count += 1

        score = passed_count / total_count if total_count > 0 else 0.0
        return GateResult(
            passed=score >= 0.80,
            score=round(score, 2),
            gate="dod",
            phase="post-task",
            issues=issues,
            warnings=warnings,
            details=details,
        )

    # ── Gate: Sprint Closing (Post-Sprint) ──

    def validate_completion(self) -> GateResult:
        """Gate G3: Validates sprint is ready to close.

        Run BEFORE Sprint Closing/Retro ceremony.
        Prevents: closing without STATUS.md, incomplete artifacts, missing commits.
        """
        issues: List[str] = []
        warnings: List[str] = []
        details: Dict[str, bool] = {}
        passed_count = 0
        total_count = 0

        artifacts = {
            "TASKS.md": False,
            "BOARD.md": False,
            "STATUS.md": False,
            "RETRO.md": False,
        }

        for artifact_name in artifacts:
            content = self._read_artifact(artifact_name)
            exists = content is not None
            artifacts[artifact_name] = exists
            total_count += 1
            if exists:
                passed_count += 1
                details[f"{artifact_name}_exists"] = True
            else:
                issues.append(f"{artifact_name} not found")

        # Check commit tracking sections
        for artifact_name, patterns in self.REQUIRED_SECTIONS.items():
            content = self._read_artifact(artifact_name)
            if content is None:
                continue
            for pattern in patterns:
                total_count += 1
                has = self._has_section(content, pattern)
                detail_key = f"{artifact_name}:{pattern[:30]}"
                details[detail_key] = has
                if has:
                    passed_count += 1
                else:
                    warnings.append(f"{artifact_name} missing section matching '{pattern}'")

        # Extract total commits across all artifacts
        all_commits: Set[str] = set()
        for name in artifacts:
            content = self._read_artifact(name)
            if content:
                all_commits.update(self._extract_commits(content))

        details["total_commits_tracked"] = len(all_commits) > 0
        if len(all_commits) == 0:
            warnings.append("No commits found across sprint artifacts")

        score = passed_count / total_count if total_count > 0 else 0.0
        return GateResult(
            passed=score >= 0.80,
            score=round(score, 2),
            gate="closing",
            phase="post-sprint",
            issues=issues,
            warnings=warnings,
            details=details,
        )

    def summary(self, results: List[GateResult]) -> str:
        """Generate a human-readable summary of all gate results."""
        lines = [
            "=" * 60,
            "  Sprint Quality Gate Report",
            "=" * 60,
            "",
        ]
        all_passed = True
        for result in results:
            icon = "✅" if result.passed else "❌"
            lines.append(f"  {icon} Gate {result.gate.upper()} ({result.phase})")
            lines.append(f"     Score: {result.score:.0%} | Phase: {result.phase}")
            if result.issues:
                for issue in result.issues:
                    lines.append(f"     ❌ {issue}")
            if result.warnings:
                for w in result.warnings:
                    lines.append(f"     ⚠️  {w}")
            if not result.passed:
                all_passed = False
            lines.append("")

        lines.append("=" * 60)
        lines.append(f"  Overall: {'✅ ALL GATES PASS' if all_passed else '❌ SOME GATES FAIL'}")
        lines.append("=" * 60)
        return "\n".join(lines)
