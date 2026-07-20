"""Validates strategy and vision foundations per BOOTSTRAP_GATE.md spec."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationResult:
    """Result of validation."""

    valid: bool
    file: str
    issues: list[str]


class StrategyValidator:
    """
    Validates strategy foundations per BOOTSTRAP_GATE.md requirements:
    - NORTH_STAR: Vision in "Teams [action] [outcomes]" format
    - OKR: Objectives with 3-5 Key Results each
    - PURPOSE: Why project exists, linked to North Star
    - VALUE_PROPOSITION: What project delivers, stakeholder-validated
    """

    STRATEGY_FILES = [
        "NORTH_STAR.md",
        "OKR.md",
        "PURPOSE.md",
        "VALUE_PROPOSITION.md",
    ]

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def validate_all(self) -> list[ValidationResult]:
        """Validate all strategy files."""
        results = []
        for file in self.STRATEGY_FILES:
            result = self.validate_file(file)
            results.append(result)
        return results

    def validate_file(self, filename: str) -> ValidationResult:
        """Validate a single strategy file."""
        file_path = self.project_root / filename
        issues = []

        if not file_path.exists():
            return ValidationResult(
                valid=False, file=filename, issues=["File not found"]
            )

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return ValidationResult(
                valid=False, file=filename, issues=[f"Read error: {type(e).__name__}"]
            )

        if not content.strip():
            return ValidationResult(
                valid=False, file=filename, issues=["Empty file"]
            )

        if filename == "NORTH_STAR.md":
            issues.extend(self._validate_north_star(content))
        elif filename == "OKR.md":
            issues.extend(self._validate_okr(content))
        elif filename == "PURPOSE.md":
            issues.extend(self._validate_purpose(content))
        elif filename == "VALUE_PROPOSITION.md":
            issues.extend(self._validate_value_prop(content))

        return ValidationResult(valid=len(issues) == 0, file=filename, issues=issues)

    def _validate_north_star(self, content: str) -> list[str]:
        """
        NORTH_STAR.md must contain:
        - A heading
        - Vision statement in "Teams [action] [outcomes]" format
        - Long-term success criteria
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()
        has_vision_format = (
            ("teams " in content_lower or "times " in content_lower)
            and any(
                word in content_lower
                for word in ["visualize", "reason", "decide", "achieve", "reach"]
            )
        )
        if not has_vision_format:
            issues.append(
                'Vision should follow format "Teams [action] [outcomes]" (e.g., "Teams visualize strategy end-to-end")'
            )

        if "success" not in content_lower and "metrics" not in content_lower:
            issues.append("Missing success criteria or metrics")

        return issues

    def _validate_okr(self, content: str) -> list[str]:
        """
        OKR.md must contain:
        - Objectives (at least 1)
        - Each objective with 3-5 Key Results
        - Measurable outcomes
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()
        obj_count = content_lower.count("objective") + content_lower.count("objetivo")
        if obj_count == 0:
            issues.append("No objectives found (use 'Objective' or 'Objetivo')")

        kr_count = (
            content_lower.count("key result")
            + content_lower.count("resultado-chave")
        )
        if kr_count == 0:
            issues.append("No key results found (use 'Key Result' or 'Resultado-chave')")

        if kr_count < 3:
            issues.append("Minimum 3 Key Results required per objective")

        metric_keywords = ["score", "metric", "number", "percent", "%", "reduced"]
        has_metrics = any(kw in content_lower for kw in metric_keywords)
        if not has_metrics:
            issues.append("Key Results should be measurable (include scores/metrics)")

        return issues

    def _validate_purpose(self, content: str) -> list[str]:
        """
        PURPOSE.md must contain:
        - Why project exists
        - Problem statement
        - Jobs to be done
        - Link to North Star (reference or similarity)
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()
        if not any(
            kw in content_lower
            for kw in ["problem", "purpose", "why", "job", "solve", "objetivo"]
        ):
            issues.append("Missing problem/purpose statement or jobs to be done")

        if not any(
            kw in content_lower for kw in ["north star", "strategy", "vision", "align"]
        ):
            issues.append("Should reference North Star or strategic alignment")

        return issues

    def _validate_value_prop(self, content: str) -> list[str]:
        """
        VALUE_PROPOSITION.md must contain:
        - What project delivers
        - Customer benefits (3+)
        - Competitive advantages
        - Stakeholder/persona validation
        """
        issues = []

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()
        benefit_keywords = ["benefit", "advantage", "deliver", "value", "provide"]
        if not any(kw in content_lower for kw in benefit_keywords):
            issues.append("Missing benefits or value statements")

        benefit_count = sum(
            content_lower.count(kw) for kw in ["benefit", "advantage", "deliver"]
        )
        if benefit_count < 2:
            issues.append("Should list at least 3 customer benefits or competitive advantages")

        if not any(
            kw in content_lower
            for kw in ["stakeholder", "persona", "customer", "user", "audience", "validate"]
        ):
            issues.append("Should reference stakeholder/persona validation")

        return issues
