"""Auto-generate template documents for missing foundations."""

from pathlib import Path
from typing import Optional


class TemplateGenerator:
    """Generates template documents for semantic foundations."""

    TEMPLATES = {
        "NORTH_STAR.md": """# North Star

Vision statement defining ultimate success for this platform.

## Vision
> [Define the long-term vision — what success looks like]

## Strategic Pillars
1. [Pillar 1]
2. [Pillar 2]
3. [Pillar 3]

## Success Metrics
- [Metric 1]
- [Metric 2]
- [Metric 3]

## Timeline
- Phase 1: [Period]
- Phase 2: [Period]
- Phase 3: [Period]
""",
        "OKR.md": """# OKRs (Objectives & Key Results)

Strategic goals and measurable outcomes for this release cycle.

## Objectives
### Objective 1: [Name]
- Key Result 1.1: [Measurable outcome]
- Key Result 1.2: [Measurable outcome]

### Objective 2: [Name]
- Key Result 2.1: [Measurable outcome]
- Key Result 2.2: [Measurable outcome]

## Roadmap Alignment
- [How these OKRs connect to the North Star]

## Measurement
- [How we measure progress]
""",
        "PURPOSE.md": """# Purpose

Why this platform exists and what problem it solves.

## Problem Statement
> [What customer/business problem do we solve?]

## Jobs to be Done
1. [Job 1]
2. [Job 2]
3. [Job 3]

## Unique Value
- [What makes us different?]

## Impact
- [How does solving this create value?]
""",
        "VALUE_PROPOSITION.md": """# Value Proposition

What value APOS delivers and why customers should adopt it.

## Core Value
> [Concise statement of the value we deliver]

## Customer Benefits
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## Competitive Advantages
- [Advantage 1]
- [Advantage 2]
- [Advantage 3]

## Use Cases
1. [Use Case 1]
2. [Use Case 2]
3. [Use Case 3]
""",
        "ONTOLOGY.md": """# Ontology

Formal definition of domain concepts, entities, relationships, and hierarchies.

## Overview
The ontology defines the semantic structure of our domain.

## Entities
### Entity 1: [Name]
- Description: [What is it?]
- Attributes:
  - attr1: [Type]
  - attr2: [Type]

### Entity 2: [Name]
- Description: [What is it?]
- Attributes:
  - attr1: [Type]
  - attr2: [Type]

## Relationships
### Relationship 1: [Name]
- Source: [Entity]
- Target: [Entity]
- Description: [What is the relationship?]

### Relationship 2: [Name]
- Source: [Entity]
- Target: [Entity]
- Description: [What is the relationship?]

## Hierarchies
### [Hierarchy Name]
- [Parent]
  - [Child 1]
  - [Child 2]
""",
        "SEMANTIC_LAYER.md": """# Semantic Layer

How we interpret, score, and govern semantic quality of knowledge.

## Scoring Components
- Coverage: [Definition]
- Quality: [Definition]
- Consistency: [Definition]

## Semantic Metrics
- Completeness Score: [0.0-1.0]
- Accuracy Score: [0.0-1.0]
- Consistency Score: [0.0-1.0]

## Quality Gates
- Minimum Score: [Value]
- Threshold Levels: [Definitions]

## Semantic Validation Rules
- [Rule 1]
- [Rule 2]
- [Rule 3]
""",
        "GOVERNANCE.md": """# Governance

Quality gates, audit rules, and enforcement mechanisms.

## Governance Model
- Gate Thresholds: [Definitions]
- Audit Scope: [What we audit]
- Enforcement: [How we enforce]

## Semantic Gates
- Gate 1: [Condition]
- Gate 2: [Condition]

## Audit Rules
- Rule 1: [What to check]
- Rule 2: [What to check]

## Policies
- Policy 1: [Definition]
- Policy 2: [Definition]
""",
        "BOOTSTRAP_GATE.md": """# Bootstrap Gate

System for validating and establishing semantic foundations.

## Required Foundations
1. NORTH_STAR.md — Vision and strategic direction
2. OKR.md — Objectives and key results
3. PURPOSE.md — Problem statement and jobs
4. VALUE_PROPOSITION.md — Value delivery
5. ONTOLOGY.md — Domain concepts
6. SEMANTIC_LAYER.md — Quality metrics
7. GOVERNANCE.md — Quality gates
8. BOOTSTRAP_GATE.md — This document
9. CAPABILITIES.md — Platform capabilities
10. IMPLEMENTATION_STATUS.md — Status tracking

## Validation Process
1. Check existence of all required files
2. Validate content quality
3. Confirm semantic completeness
4. Gate passes if all checks complete

## Foundation Definition Session
If foundations are missing, initiate guided session:
- Step 1: JTBD Discovery
- Step 2: Platform Identity
- Step 3: Ontology Definition
- Step 4: Governance Setup
""",
        "CAPABILITIES.md": """# Capabilities

Core frameworks and features built into the platform.

## Built-in Frameworks
1. [Framework 1]
   - Purpose: [What does it do?]
   - Use cases: [When to use]

2. [Framework 2]
   - Purpose: [What does it do?]
   - Use cases: [When to use]

## APIs & Integrations
- [API 1]
- [Integration 1]

## Plugins & Extensions
- [Extension 1]
- [Extension 2]
""",
        "IMPLEMENTATION_STATUS.md": """# Implementation Status

Current state of implementation and phase tracking.

## Current Phase
- Phase: [Current phase]
- Start Date: [Date]
- End Date: [Date]

## Completed
- [Feature 1] ✅
- [Feature 2] ✅

## In Progress
- [Feature 1] 🔄
- [Feature 2] 🔄

## Planned
- [Feature 1] 📋
- [Feature 2] 📋

## Known Limitations
- [Limitation 1]
- [Limitation 2]
""",
    }

    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path.cwd()

    def generate(self, filename: str) -> str:
        """Generate template content for a specific file."""
        return self.TEMPLATES.get(filename, f"# {filename}\n\n[Add content here]\n")

    def generate_file(self, filename: str, overwrite: bool = False) -> bool:
        """Write template file to disk."""
        file_path = self.project_root / filename

        if file_path.exists() and not overwrite:
            return False

        template_content = self.generate(filename)
        try:
            file_path.write_text(template_content, encoding="utf-8")
            return True
        except Exception:
            return False

    def generate_missing(
        self, missing_files: list[str], overwrite: bool = False
    ) -> dict[str, bool]:
        """Generate all missing foundation files."""
        results = {}
        for filename in missing_files:
            if filename in self.TEMPLATES:
                results[filename] = self.generate_file(filename, overwrite)
        return results
