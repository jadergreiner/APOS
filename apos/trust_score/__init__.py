"""
Trust Score Engine Module

Calcula confiança de alinhamento estratégico (Task → OKR).

Exemplo:
    from apos.trust_score import TrustScoreEngine, Task, OKR, Relationship

    tasks = [Task(id="T1", title="Feature X", status="in_progress", project_id="P1", okr_id="OKR-1")]
    okrs = [OKR(id="OKR-1", name="Goal 1", project_id="P1")]
    rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0)]

    engine = TrustScoreEngine(tasks, okrs, rels)
    result = engine.calculate()

    print(f"Score: {result.score:.0%}")
    print(f"Issues: {result.issues}")
"""

from .engine import (
    Task,
    OKR,
    Relationship,
    ScoreComponent,
    TrustScoreResult,
    TrustScoreEngine,
)

__version__ = "0.1.0"

__all__ = [
    "Task",
    "OKR",
    "Relationship",
    "ScoreComponent",
    "TrustScoreResult",
    "TrustScoreEngine",
]
