"""Validates governance and quality foundations per BOOTSTRAP_GATE.md spec."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class GovernanceValidationResult:
    """Result of governance validation."""

    valid: bool
    file: str
    issues: list[str]
    gate_count: int = 0


class GovernanceValidator:
    """
    Validates governance foundations per BOOTSTRAP_GATE.md:
    - GOVERNANCE.md: Quality gates, audit rules, approval workflows
    - BOOTSTRAP_GATE.md: Foundation validation checklist
    - CAPABILITIES.md: Built-in frameworks and features
    - IMPLEMENTATION_STATUS.md: Phase tracking and known limitations
    """

    GOVERNANCE_FILES = [
        "GOVERNANCE.md",
        "BOOTSTRAP_GATE.md",
        "CAPABILITIES.md",
        "IMPLEMENTATION_STATUS.md",
    ]

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def validate_all(self) -> list[GovernanceValidationResult]:
        """Validate all governance files."""
        results = []
        for file in self.GOVERNANCE_FILES:
            result = self.validate_file(file)
            results.append(result)
        return results

    def validate_file(self, filename: str) -> GovernanceValidationResult:
        """Validate a single governance file."""
        file_path = self.project_root / filename
        issues = []

        if not file_path.exists():
            return GovernanceValidationResult(
                valid=False, file=filename, issues=["File not found"]
            )

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return GovernanceValidationResult(
                valid=False, file=filename, issues=[f"Read error: {type(e).__name__}"]
            )

        if not content.strip():
            return GovernanceValidationResult(
                valid=False, file=filename, issues=["Empty file"]
            )

        if filename == "GOVERNANCE.md":
            issues.extend(self._validate_governance(content))
        elif filename == "BOOTSTRAP_GATE.md":
            issues.extend(self._validate_bootstrap_gate(content))
        elif filename == "CAPABILITIES.md":
            issues.extend(self._validate_capabilities(content))
        elif filename == "IMPLEMENTATION_STATUS.md":
            issues.extend(self._validate_implementation_status(content))

        return GovernanceValidationResult(
            valid=len(issues) == 0, file=filename, issues=issues
        )

    def _validate_governance(self, content: str) -> list[str]:
        """
        GOVERNANCE.md must contain:
        - How project ensures quality and alignment
        - Semantic gates and validation rules
        - Approval workflows
        - Audit checklist
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        if not any(
            kw in content_lower
            for kw in ["gate", "validation", "quality", "approval", "audit", "rules"]
        ):
            issues.append(
                "Missing governance mechanisms (gates, validation, approval, audit)"
            )

        if "gate" not in content_lower and "rule" not in content_lower:
            issues.append("Missing semantic gates or governance rules")

        return issues

    def _validate_bootstrap_gate(self, content: str) -> list[str]:
        """
        BOOTSTRAP_GATE.md must contain:
        - List of required foundations (10 items)
        - Validation checklist
        - Foundation definition workflow steps
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        required_items = [
            "north_star",
            "purpose",
            "okr",
            "value",
            "ontology",
            "semantic",
            "governance",
            "capabilities",
        ]
        found_items = sum(1 for item in required_items if item in content_lower)
        if found_items < 6:
            issues.append(
                f"Bootstrap checklist incomplete (found ~{found_items} of 10 required items)"
            )

        if not any(
            kw in content_lower
            for kw in ["validation", "validate", "check", "verificar"]
        ):
            issues.append("Missing validation process description")

        return issues

    def _validate_capabilities(self, content: str) -> list[str]:
        """
        CAPABILITIES.md must contain:
        - Built-in frameworks
        - Use cases for each capability
        - APIs and integrations
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        capability_keywords = [
            "framework",
            "capability",
            "feature",
            "api",
            "integration",
        ]
        if not any(kw in content_lower for kw in capability_keywords):
            issues.append(
                "Missing capability descriptions (should list frameworks/APIs/integrations)"
            )

        if "use case" not in content_lower and "example" not in content_lower:
            issues.append("Missing use cases or examples for capabilities")

        return issues

    def _validate_implementation_status(self, content: str) -> list[str]:
        """
        IMPLEMENTATION_STATUS.md must contain:
        - Current phase
        - Completed features
        - In-progress items
        - Known limitations
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        status_sections = [
            "phase",
            "completed",
            "progress",
            "planned",
            "limitation",
        ]
        found_sections = sum(1 for section in status_sections if section in content_lower)
        if found_sections < 3:
            issues.append(
                f"Missing status sections (found {found_sections} of 5: phase, completed, progress, planned, limitations)"
            )

        if not any(kw in content_lower for kw in ["✅", "🔄", "📋", "completed"]):
            issues.append(
                "Missing status markers or phase tracking (use ✅ 🔄 📋 or similar)"
            )

        return issues
