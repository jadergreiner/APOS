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

Template files have been auto-generated. Review and update them.\n""")

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
        if "GOVERNANCE.md" in self.missing_foundations or self._should_update(
            "GOVERNANCE"
        ):
            self.run_governance_setup()

        print("\n" + "=" * 60)
        print("✅ Foundation Definition Session Complete!")
        print("\n🔄 Next Steps:")
        print("   1. Review and update generated template files")
        print("   2. Run 'python -m apos init' again to validate")
        print("   3. Fix any validation issues reported")
        print("   4. Once all foundations pass validation, you're ready to execute!\n")

        return self.defined_foundations

    def run_jtbd_discovery(self) -> None:
        """Step 1: Jobs to be Done discovery."""
        print("\n1️⃣  JTBD Discovery")
        print("-" * 60)
        print("""
Understanding the jobs your system solves is foundational.

Jobs are outcome-driven tasks customers want to accomplish.
Example: 'Help teams make aligned decisions faster'

What problems does your solution solve?
Who are your customers and what outcomes do they need?

Instructions:
- Edit PURPOSE.md with your domain's problem statement
- List the core jobs your system addresses
- Describe unique value you provide""")

        purpose = self.project_root / "PURPOSE.md"
        if purpose.exists():
            print("\n   ✓ PURPOSE.md exists — skipping generation")
            return

        self.defined_foundations["PURPOSE"] = "PURPOSE.md"
        print("\n   → Template PURPOSE.md has been generated")
        print("   → Edit it with your JTBD analysis")

    def run_platform_identity(self) -> None:
        """Step 2: Platform identity (North Star, OKRs, positioning)."""
        print("\n2️⃣  Platform Identity")
        print("-" * 60)
        print("""
Define your platform's strategic identity:
- North Star: Vision of ultimate success
- OKRs: Objectives & Key Results for this phase
- Value Proposition: What you deliver

Instructions:
- NORTH_STAR.md: Define your long-term vision (2-3 years)
- OKR.md: Set measurable objectives for current cycle
- VALUE_PROPOSITION.md: Articulate unique value and benefits""")

        north_star = self.project_root / "NORTH_STAR.md"
        okr = self.project_root / "OKR.md"
        value_prop = self.project_root / "VALUE_PROPOSITION.md"

        existing = []
        missing = []

        if north_star.exists():
            existing.append("NORTH_STAR.md")
        else:
            missing.append("NORTH_STAR.md")

        if okr.exists():
            existing.append("OKR.md")
        else:
            missing.append("OKR.md")

        if value_prop.exists():
            existing.append("VALUE_PROPOSITION.md")
        else:
            missing.append("VALUE_PROPOSITION.md")

        if existing:
            print(f"\n   ✓ Found: {', '.join(existing)}")
        if missing:
            print(f"   → Generated: {', '.join(missing)}")
            for filename in missing:
                self.defined_foundations[filename.replace(".md", "")] = filename

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

Instructions:
- ONTOLOGY.md: Define entities, relationships, hierarchies
- SEMANTIC_LAYER.md: Define how we score semantic quality

This is critical for enabling AI agents to reason correctly!""")

        ontology = self.project_root / "ONTOLOGY.md"
        semantic = self.project_root / "SEMANTIC_LAYER.md"

        existing = []
        missing = []

        if ontology.exists():
            existing.append("ONTOLOGY.md")
        else:
            missing.append("ONTOLOGY.md")

        if semantic.exists():
            existing.append("SEMANTIC_LAYER.md")
        else:
            missing.append("SEMANTIC_LAYER.md")

        if existing:
            print(f"\n   ✓ Found: {', '.join(existing)}")
        if missing:
            print(f"   → Generated: {', '.join(missing)}")
            for filename in missing:
                self.defined_foundations[filename.replace(".md", "")] = filename

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

Instructions:
- GOVERNANCE.md: Define quality gates and audit rules
- BOOTSTRAP_GATE.md: How foundations are validated
- CAPABILITIES.md: Document built-in frameworks
- IMPLEMENTATION_STATUS.md: Track implementation phases""")

        governance = self.project_root / "GOVERNANCE.md"
        bootstrap = self.project_root / "BOOTSTRAP_GATE.md"
        capabilities = self.project_root / "CAPABILITIES.md"
        status = self.project_root / "IMPLEMENTATION_STATUS.md"

        existing = []
        missing = []

        for file in [governance, bootstrap, capabilities, status]:
            if file.exists():
                existing.append(file.name)
            else:
                missing.append(file.name)

        if existing:
            print(f"\n   ✓ Found: {', '.join(existing)}")
        if missing:
            print(f"   → Generated: {', '.join(missing)}")
            for filename in missing:
                self.defined_foundations[filename.replace(".md", "")] = filename

    def _should_update(self, foundation_name: str) -> bool:
        """Check if a foundation should be updated (simplified for now)."""
        return False
