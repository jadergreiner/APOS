"""APOS Kernel Patterns — Guaranteed behavior when importing APOS.

Kernel patterns are implemented, tested, and guaranteed to work when projects
import APOS. They are immutable during version lifecycle and form the contract
between APOS and downstream projects.
"""

from apos.kernel.commit_tracking import (
    CommitTrackingResult,
    CommitTrackingValidator,
)

__all__ = [
    "CommitTrackingValidator",
    "CommitTrackingResult",
]
