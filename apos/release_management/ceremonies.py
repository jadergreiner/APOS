"""Cerimônias de sprint — estrutura para daily standup, planning e retro."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class DailyStandupUpdate:
    """Um update de um participante em daily standup."""

    participant: str
    date: str  # ISO format
    what_done: str  # O que foi feito ontem
    what_today: str  # O que vai fazer hoje
    blockers: str = ""  # Bloqueadores (se houver)
    notes: str = ""


@dataclass
class DailyStandup:
    """Estrutura de daily standup."""

    sprint_id: str
    date: str  # ISO format (ex: 2026-07-22)
    updates: List[DailyStandupUpdate] = field(default_factory=list)
    summary: str = ""  # Sumário geral
    action_items: List[str] = field(default_factory=list)

    def add_update(self, update: DailyStandupUpdate) -> None:
        """Adicionar update de participante."""
        self.updates.append(update)

    def get_participant_count(self) -> int:
        """Contar participantes únicos."""
        return len(set(u.participant for u in self.updates))

    def get_blockers(self) -> List[str]:
        """Listar todos os bloqueadores relatados."""
        return [u.blockers for u in self.updates if u.blockers]

    def to_dict(self) -> dict:
        """Serializar daily standup."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "num_participants": self.get_participant_count(),
            "num_blockers": len(self.get_blockers()),
            "num_action_items": len(self.action_items),
            "blockers": self.get_blockers(),
            "action_items": self.action_items,
        }


@dataclass
class SprintPlanningSession:
    """Estrutura de sprint planning."""

    sprint_id: str
    date: str  # ISO format
    duration_minutes: int = 120
    attendees: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    planned_tasks: List[dict] = field(
        default_factory=list
    )  # {id, title, estimate}
    velocity_target: float = 0.0
    dependencies_identified: List[str] = field(default_factory=list)
    risks_identified: List[str] = field(default_factory=list)
    notes: str = ""

    def add_attendee(self, name: str) -> None:
        """Adicionar participante."""
        if name not in self.attendees:
            self.attendees.append(name)

    def add_goal(self, goal: str) -> None:
        """Adicionar objetivo do sprint."""
        self.goals.append(goal)

    def add_planned_task(self, task_id: str, title: str, estimate: float) -> None:
        """Adicionar tarefa ao plano."""
        self.planned_tasks.append(
            {"id": task_id, "title": title, "estimate": estimate}
        )

    def total_estimated_days(self) -> float:
        """Total de dias estimados."""
        return sum(t["estimate"] for t in self.planned_tasks)

    def to_dict(self) -> dict:
        """Serializar sprint planning."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "duration_minutes": self.duration_minutes,
            "num_attendees": len(self.attendees),
            "num_goals": len(self.goals),
            "num_planned_tasks": len(self.planned_tasks),
            "velocity_target": self.velocity_target,
            "total_estimated_days": self.total_estimated_days(),
            "num_dependencies": len(self.dependencies_identified),
            "num_risks": len(self.risks_identified),
        }


@dataclass
class RetroAction:
    """Uma ação de melhoria da retrospectiva."""

    category: str  # "what_went_well", "what_went_wrong", "improvements"
    description: str
    owner: Optional[str] = None
    priority: str = "medium"  # low, medium, high


@dataclass
class Retrospective:
    """Estrutura de sprint retrospective."""

    sprint_id: str
    date: str  # ISO format
    duration_minutes: int = 60
    attendees: List[str] = field(default_factory=list)
    what_went_well: List[str] = field(default_factory=list)
    what_went_wrong: List[str] = field(default_factory=list)
    improvement_ideas: List[str] = field(default_factory=list)
    action_items: List[RetroAction] = field(default_factory=list)
    velocity_achieved: float = 0.0
    completion_rate: float = 0.0
    overall_sentiment: str = "neutral"  # positive, neutral, negative
    notes: str = ""

    def add_attendee(self, name: str) -> None:
        """Adicionar participante."""
        if name not in self.attendees:
            self.attendees.append(name)

    def add_well(self, item: str) -> None:
        """Adicionar item positivo."""
        self.what_went_well.append(item)

    def add_wrong(self, item: str) -> None:
        """Adicionar item negativo."""
        self.what_went_wrong.append(item)

    def add_improvement(self, idea: str) -> None:
        """Adicionar ideia de melhoria."""
        self.improvement_ideas.append(idea)

    def add_action(self, action: RetroAction) -> None:
        """Adicionar ação de melhoria."""
        self.action_items.append(action)

    def get_high_priority_actions(self) -> List[RetroAction]:
        """Listar ações de alta prioridade."""
        return [a for a in self.action_items if a.priority == "high"]

    def to_dict(self) -> dict:
        """Serializar retrospective."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "duration_minutes": self.duration_minutes,
            "num_attendees": len(self.attendees),
            "num_positive_items": len(self.what_went_well),
            "num_negative_items": len(self.what_went_wrong),
            "num_improvement_ideas": len(self.improvement_ideas),
            "num_action_items": len(self.action_items),
            "num_high_priority_actions": len(self.get_high_priority_actions()),
            "velocity_achieved": self.velocity_achieved,
            "completion_rate": self.completion_rate,
            "overall_sentiment": self.overall_sentiment,
        }
