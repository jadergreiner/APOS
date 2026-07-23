"""APOS Kernel Patterns — Guaranteed behavior when importing APOS.

Kernel patterns are implemented, tested, and guaranteed to work when projects
import APOS. They are immutable during version lifecycle and form the contract
between APOS and downstream projects.

## Available Patterns

- **CommitTrackingValidator** — Validates commit tracking in sprint artifacts
- **SprintQualityGate** — Quality gates for sprint ceremonies (planning, daily, closing)
  Validates DoR, DoD, artifact completeness, and commit tracking.
  Usage:
      from apos.kernel import SprintQualityGate
      gate = SprintQualityGate(sprint_root="docs/releases/R1/sprint-1.2/")
      result = gate.validate_completion()
      if result.passes():
          print("✅ Sprint ready to close")
"""

from apos.kernel.commit_tracking import (
    CommitTrackingResult,
    CommitTrackingValidator,
)
from apos.kernel.sprint_quality_gate import (
    SprintQualityGate,
    GateResult,
)

__all__ = [
    "CommitTrackingValidator",
    "CommitTrackingResult",
    "SprintQualityGate",
    "GateResult",
]
