"""Validates ontology and semantic foundations per BOOTSTRAP_GATE.md spec."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class OntologyValidationResult:
    """Result of ontology validation."""

    valid: bool
    file: str
    issues: list[str]
    entity_count: int = 0
    relationship_count: int = 0
    rule_count: int = 0


class OntologyValidator:
    """
    Validates ontology foundations per BOOTSTRAP_GATE.md:
    - ONTOLOGY.md: 5+ core concepts, relationships, constraints
    - SEMANTIC_LAYER.md: 10+ semantic rules, scoring components
    """

    ONTOLOGY_FILES = [
        "ONTOLOGY.md",
        "SEMANTIC_LAYER.md",
    ]

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def validate_all(self) -> list[OntologyValidationResult]:
        """Validate all ontology files."""
        results = []
        for file in self.ONTOLOGY_FILES:
            result = self.validate_file(file)
            results.append(result)
        return results

    def validate_file(self, filename: str) -> OntologyValidationResult:
        """Validate a single ontology file."""
        file_path = self.project_root / filename
        issues = []

        if not file_path.exists():
            return OntologyValidationResult(
                valid=False, file=filename, issues=["File not found"]
            )

        try:
            content = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return OntologyValidationResult(
                valid=False, file=filename, issues=[f"Read error: {type(e).__name__}"]
            )

        if not content.strip():
            return OntologyValidationResult(
                valid=False, file=filename, issues=["Empty file"]
            )

        if filename == "ONTOLOGY.md":
            return self._validate_ontology_md(content, filename)
        elif filename == "SEMANTIC_LAYER.md":
            return self._validate_semantic_layer(content, filename)

        return OntologyValidationResult(valid=True, file=filename, issues=[])

    def _validate_ontology_md(
        self, content: str, filename: str
    ) -> OntologyValidationResult:
        """
        ONTOLOGY.md must contain:
        - Heading
        - 5+ core entities (concepts)
        - Relationships between entities
        - Domain constraints
        - Attribute definitions
        """
        issues = []
        entity_count = 0
        relationship_count = 0

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        entity_count = (
            content_lower.count("## entity")
            + content_lower.count("### entity")
            + content_lower.count("entidade")
        )
        if entity_count < 5:
            issues.append(f"Minimum 5 core entities required (found {entity_count})")

        relationship_count = (
            content_lower.count("relationship")
            + content_lower.count("relacionamento")
        )
        if relationship_count == 0:
            issues.append("Missing entity relationships")

        if (
            "constraint" not in content_lower
            and "restricao" not in content_lower
            and "- " not in content
        ):
            issues.append("Missing domain constraints")

        attr_keywords = ["attribute", "properties", "property", "atributo"]
        has_attributes = any(kw in content_lower for kw in attr_keywords)
        if not has_attributes:
            issues.append("Missing entity attribute definitions")

        return OntologyValidationResult(
            valid=len(issues) == 0,
            file=filename,
            issues=issues,
            entity_count=entity_count,
            relationship_count=relationship_count,
        )

    def _validate_semantic_layer(
        self, content: str, filename: str
    ) -> OntologyValidationResult:
        """
        SEMANTIC_LAYER.md must contain:
        - Heading
        - 10+ semantic rules
        - Coverage, quality, consistency components
        - Scoring definitions
        """
        issues = []
        rule_count = 0

        if "# " not in content:
            issues.append("Missing heading")

        content_lower = content.lower()

        rule_keywords = ["rule", "regra", "constraint", "restricao", "criteria"]
        rule_count = sum(content_lower.count(kw) for kw in rule_keywords)

        numbered_rules = len([line for line in content.split("\n") if line.strip() and line[0].isdigit() and "." in line])
        rule_count = max(rule_count, numbered_rules)

        if rule_count < 10:
            issues.append(f"Minimum 10 semantic rules required (found ~{rule_count})")

        scoring_keywords = [
            "coverage",
            "quality",
            "consistency",
            "score",
            "metric",
        ]
        has_scoring = any(kw in content_lower for kw in scoring_keywords)
        if not has_scoring:
            issues.append("Missing scoring components (coverage, quality, consistency)")

        if "gate" not in content_lower and "validation" not in content_lower:
            issues.append("Missing semantic gate or validation thresholds")

        return OntologyValidationResult(
            valid=len(issues) == 0,
            file=filename,
            issues=issues,
            rule_count=rule_count,
        )
