"""Foundation Definition Session — guided setup for semantic foundations."""

from pathlib import Path
from typing import Optional


class FoundationDefinitionSession:
    """
    Guides a project through structured JTBD → Strategy → Ontology → Governance
    foundation definition workflow. Auto-generates templates for missing foundations.
    """

    def __init__(
        self,
        project_root: Optional[Path] = None,
        missing_foundations: Optional[list[str]] = None,
    ):
        self.project_root = project_root or Path.cwd()
        self.missing_foundations = missing_foundations or []
        self.defined_foundations = {}

    def run(self) -> dict:
        """Execute the full foundation definition workflow."""
        print("\n📋 Foundation Definition Workflow")
        print("=" * 60)
        print("""
This guided session will help you define semantic foundations through:

1️⃣  JTBD Discovery  — Understand jobs your system solves
2️⃣  Platform Identity — Define North Star, OKRs, positioning
3️⃣  Ontology Definition — Structure concepts and semantics
4️⃣  Governance Setup — Define quality rules and guardrails

Let's begin...\n""")

        # Step 1: JTBD Discovery
        if "PURPOSE.md" in self.missing_foundations or self._should_update("PURPOSE"):
            self.run_jtbd_discovery()

        # Step 2: Platform Identity (North Star + OKRs)
        if (
            "NORTH_STAR.md" in self.missing_foundations
            or "OKR.md" in self.missing_foundations
            or self._should_update("NORTH_STAR")
        ):
            self.run_platform_identity()

        # Step 3: Ontology Definition
        if "ONTOLOGY.md" in self.missing_foundations or self._should_update("ONTOLOGY"):
            self.run_ontology_definition()

        # Step 4: Governance Setup
        if "GOVERNANCE.md" in self.missing_foundations or self._should_update("GOVERNANCE"):
            self.run_governance_setup()

        print("\n✅ Foundation Definition Session Complete!")
        return self.defined_foundations

    def run_jtbd_discovery(self) -> None:
        """Step 1: Jobs to be Done discovery."""
        print("\n1️⃣  JTBD Discovery")
        print("-" * 60)
        print("""
Understanding the jobs your system solves is foundational.

Jobs are outcome-driven tasks customers want to accomplish.
Example: 'Help teams make aligned decisions faster'

""")

        purpose = self.project_root / "PURPOSE.md"
        if purpose.exists():
            print("   ✓ PURPOSE.md already exists — skipping")
            return

        print("Let's define what problem APOS solves...\n")

        # For now, we show what was already defined in the root
        self.defined_foundations["PURPOSE"] = "See PURPOSE.md"
        print("   → Check PURPOSE.md for defined JTBD")

    def run_platform_identity(self) -> None:
        """Step 2: Platform identity (North Star, OKRs, positioning)."""
        print("\n2️⃣  Platform Identity")
        print("-" * 60)
        print("""
Define your platform's strategic identity:
- North Star: Vision of ultimate success
- OKRs: Objectives & Key Results for this phase
- Value Proposition: What you deliver

""")

        north_star = self.project_root / "NORTH_STAR.md"
        okr = self.project_root / "OKR.md"

        if north_star.exists() and okr.exists():
            print("   ✓ NORTH_STAR.md and OKR.md already exist")
            return

        self.defined_foundations["NORTH_STAR"] = "See NORTH_STAR.md"
        self.defined_foundations["OKR"] = "See OKR.md"
        print("   → Check NORTH_STAR.md and OKR.md for strategy")

    def run_ontology_definition(self) -> None:
        """Step 3: Ontology definition (concepts, semantics)."""
        print("\n3️⃣  Ontology Definition")
        print("-" * 60)
        print("""
An ontology formalizes your domain's concepts:
- Entities: Core domain concepts (e.g., Student, Course)
- Relationships: How entities connect (e.g., enrolled_in)
- Attributes: Properties of entities and relationships
- Hierarchies: Classification structures

""")

        ontology = self.project_root / "ONTOLOGY.md"
        if ontology.exists():
            print("   ✓ ONTOLOGY.md already exists — skipping")
            return

        print("   → Ontologies are typically defined in YAML format")
        print("   → See ONTOLOGY.md for structure and examples")
        self.defined_foundations["ONTOLOGY"] = "ONTOLOGY.md (to be created)"

    def run_governance_setup(self) -> None:
        """Step 4: Governance setup (quality gates, audit rules)."""
        print("\n4️⃣  Governance Setup")
        print("-" * 60)
        print("""
Governance ensures quality and consistency:
- Semantic Gates: Quality thresholds for context
- Audit Rules: Checks to catch semantic issues
- Metrics: Scoring components (coverage, quality, consistency)
- Policies: Custom governance rules

""")

        governance = self.project_root / "GOVERNANCE.md"
        if governance.exists():
            print("   ✓ GOVERNANCE.md already exists — skipping")
            return

        print("   → See GOVERNANCE.md for governance framework")
        self.defined_foundations["GOVERNANCE"] = "GOVERNANCE.md (to be created)"

        print("\n" + "=" * 60)
        print("✨ Foundation Definition Complete!")

    def _should_update(self, foundation_name: str) -> bool:
        """Check if a foundation should be updated (simplified for now)."""
        return False
