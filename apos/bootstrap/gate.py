"""BootstrapGate — validates semantic foundations before project execution."""

from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class BootstrapResult:
    """Result of bootstrap validation."""

    passed: bool
    missing_foundations: list[str]
    existing_foundations: list[str]
    session_needed: bool
    summary: str


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
            print("   Initiating Foundation Definition Session...\n")

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
