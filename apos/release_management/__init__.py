"""APOS Release Management Framework.

Fornece estrutura operacional para gerenciar releases, sprints e cerimônias.
Quando um projeto importa APOS, recebe automaticamente:
- Release Plans (R0-R4)
- Sprint Templates (planejamento, board, status, retro)
- Cerimônias (daily standup, sprint planning, retro)
- Automação (generators, validators)

Usage:
    from apos.release_management import ReleaseManager, SprintManager

    # Gerenciar release
    rm = ReleaseManager(project_name="meu-projeto")
    rm.initialize_release("R0")

    # Gerenciar sprint
    sm = SprintManager(release="R0")
    sprint = sm.create_sprint("sprint-0.0", start_date="2026-07-22")
    sprint.add_task("T0.0.1", "Implementar Feature", days=2)
"""

from apos.release_management.release import Release, ReleaseManager, ReleaseObjective
from apos.release_management.sprint import (
    Sprint,
    SprintManager,
    Task,
    TaskStatus,
    UserStory,
)
from apos.release_management.ceremonies import (
    DailyStandup,
    DailyStandupUpdate,
    SprintPlanningSession,
    Retrospective,
    RetroAction,
    RoadmapCeremony,
    RoadmapPhase,
)
from apos.release_management.templates import ReleaseTemplateGenerator
from apos.release_management.daily_runner import (
    DailyStandupRunner,
    DailyMode,
    EvidenceAnalysis,
)

__all__ = [
    # Release Management
    "Release",
    "ReleaseManager",
    "ReleaseObjective",
    # Sprint Management
    "Sprint",
    "SprintManager",
    "Task",
    "TaskStatus",
    "UserStory",
    # Ceremonies
    "DailyStandup",
    "DailyStandupUpdate",
    "SprintPlanningSession",
    "Retrospective",
    "RetroAction",
    "RoadmapCeremony",
    "RoadmapPhase",
    # Templates
    "ReleaseTemplateGenerator",
    # Daily Runner
    "DailyStandupRunner",
    "DailyMode",
    "EvidenceAnalysis",
]
