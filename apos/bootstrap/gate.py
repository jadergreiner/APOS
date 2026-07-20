"""BootstrapGate — validates semantic foundations before project execution."""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BootstrapResult:
    """Result of bootstrap validation."""

    passed: bool
    missing_foundations: list[str]
    existing_foundations: list[str]
    session_needed: bool
    summary: str
    validation_details: dict = field(default_factory=dict)


class BootstrapGate:
    """
    Validates that a project has required semantic foundations before execution.
    If missing, can initiate a guided Foundation Definition Session.
    """

    REQUIRED_FOUNDATIONS = [
        "NORTH_STAR.md",
        "OKR.md",
        "PURPOSE.md",
        "VALUE_PROPOSITION.md",
        "ONTOLOGY.md",
        "SEMANTIC_LAYER.md",
        "GOVERNANCE.md",
        "BOOTSTRAP_GATE.md",
        "CAPABILITIES.md",
        "IMPLEMENTATION_STATUS.md",
    ]

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def validate(self) -> BootstrapResult:
        """Check which foundations exist and which are missing."""
        missing = []
        existing = []

        for foundation in self.REQUIRED_FOUNDATIONS:
            path = self.project_root / foundation
            if path.exists():
                existing.append(foundation)
            else:
                missing.append(foundation)

        passed = len(missing) == 0
        session_needed = len(missing) > 0

        summary = f"✅ {len(existing)}/{len(self.REQUIRED_FOUNDATIONS)} foundations found"
        if missing:
            summary += f"\n❌ Missing: {', '.join(missing)}"

        return BootstrapResult(
            passed=passed,
            missing_foundations=missing,
            existing_foundations=existing,
            session_needed=session_needed,
            summary=summary,
        )

    def validate_with_details(self) -> BootstrapResult:
        """Validate foundations with detailed validation of each file."""
        from apos.bootstrap.validators import (
            StrategyValidator,
            OntologyValidator,
            GovernanceValidator,
        )

        result = self.validate()
        validation_details = {}

        # Strategy validation
        strategy_val = StrategyValidator(self.project_root)
        for val_result in strategy_val.validate_all():
            validation_details[val_result.file] = {
                "valid": val_result.valid,
                "issues": val_result.issues,
            }

        # Ontology validation
        ontology_val = OntologyValidator(self.project_root)
        for val_result in ontology_val.validate_all():
            validation_details[val_result.file] = {
                "valid": val_result.valid,
                "issues": val_result.issues,
                "entity_count": val_result.entity_count,
                "relationship_count": val_result.relationship_count,
            }

        # Governance validation
        governance_val = GovernanceValidator(self.project_root)
        for val_result in governance_val.validate_all():
            validation_details[val_result.file] = {
                "valid": val_result.valid,
                "issues": val_result.issues,
            }

        # Commit Tracking validation (for active sprints)
        commit_tracking_details = self.validate_commit_tracking()
        if commit_tracking_details:
            validation_details.update(commit_tracking_details)

        result.validation_details = validation_details
        return result

    def generate_missing_templates(self) -> dict[str, bool]:
        """Auto-generate template files for missing foundations."""
        from apos.bootstrap.templates import TemplateGenerator

        result = self.validate()
        generator = TemplateGenerator(self.project_root)
        return generator.generate_missing(result.missing_foundations)

    def validate_commit_tracking(self) -> dict:
        """Validate commit tracking in active sprints (optional).

        Looks for docs/releases/*/sprint-*/ directories and validates
        that TASKS.md, BOARD.md, STATUS.md have commit references.

        Returns:
            Dict of sprint validation details, empty if no sprints found.
        """
        from apos.kernel import CommitTrackingValidator

        details = {}
        releases_dir = self.project_root / "docs" / "releases"

        if not releases_dir.exists():
            return details

        # Find all sprints
        for release_dir in releases_dir.iterdir():
            if not release_dir.is_dir():
                continue

            for sprint_dir in release_dir.iterdir():
                if not sprint_dir.is_dir() or not sprint_dir.name.startswith(
                    "sprint-"
                ):
                    continue

                # Validate sprint
                validator = CommitTrackingValidator(str(sprint_dir))
                result = validator.validate()

                sprint_key = f"commit_tracking_{release_dir.name}_{sprint_dir.name}"
                details[sprint_key] = {
                    "valid": result.passes(),
                    "score": result.score,
                    "status": result.status,
                    "issues": result.issues,
                    "tracked_commits": sorted(result.tracked_commits),
                }

        return details

    def run(self) -> bool:
        """
        Main entry point for `python -m apos init`.
        Validates foundations and guides session if needed.
        """
        print("\nAPOS Project Initialization")
        print("=" * 60)

        result = self.validate()
        print(f"\n{result.summary}\n")

        if result.passed:
            print("✨ Project foundations are complete.")
            print("   Ready for execution!\n")
            return True

        if result.session_needed:
            print("⚠️  Missing foundations detected.")
            print("   Generating template files...\n")

            templates_generated = self.generate_missing_templates()
            for filename, success in templates_generated.items():
                status = "✓" if success else "✗"
                print(f"   {status} {filename}")

            print("\n   Initiating Foundation Definition Session...\n")

            from apos.bootstrap.session import FoundationDefinitionSession

            session = FoundationDefinitionSession(
                project_root=self.project_root,
                missing_foundations=result.missing_foundations,
            )
            session.run()

            # Re-validate after session
            result_after = self.validate()
            if result_after.passed:
                print("\n✨ All foundations are now defined!")
                print("   Project is ready for execution.\n")
                return True
            else:
                print("\n⚠️  Some foundations still need attention:")
                print(f"   {', '.join(result_after.missing_foundations)}\n")
                return False

        return False
