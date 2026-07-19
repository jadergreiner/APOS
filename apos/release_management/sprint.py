"""Sprint management — estrutura para planejar e rastrear sprints."""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from pathlib import Path


class TaskStatus(str, Enum):
    """Status de uma tarefa."""
    BACKLOG = "backlog"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETE = "complete"
    BLOCKED = "blocked"


class SprintPhase(str, Enum):
    """Fases de um sprint."""
    PLANNING = "planning"
    ACTIVE = "active"
    CLOSING = "closing"
    COMPLETE = "complete"


@dataclass
class Task:
    """Representa uma tarefa em um sprint."""

    id: str  # Ex: "T0.0.1"
    title: str
    description: str
    days_estimate: float  # Dias-pessoa
    status: TaskStatus = TaskStatus.PLANNED
    assignee: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)  # Task IDs
    notes: str = ""

    def to_dict(self) -> dict:
        """Serializar tarefa."""
        return {
            "id": self.id,
            "title": self.title,
            "days_estimate": self.days_estimate,
            "status": self.status.value,
            "assignee": self.assignee,
            "depends_on": self.depends_on,
        }


@dataclass
class UserStory:
    """Representa uma user story em um sprint."""

    id: str  # Ex: "US-0.0.1"
    title: str
    description: str
    story_points: float
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "planned"
    owner: Optional[str] = None

    def to_dict(self) -> dict:
        """Serializar user story."""
        return {
            "id": self.id,
            "title": self.title,
            "story_points": self.story_points,
            "status": self.status,
            "num_criteria": len(self.acceptance_criteria),
        }


@dataclass
class Sprint:
    """Representa um sprint."""

    id: str  # Ex: "sprint-0.0"
    release_id: str  # Ex: "R0"
    title: str
    start_date: str  # ISO format
    end_date: str
    phase: SprintPhase = SprintPhase.PLANNING
    tasks: List[Task] = field(default_factory=list)
    user_stories: List[UserStory] = field(default_factory=list)
    velocity_target: float = 0.0  # Pontos alvo
    velocity_actual: float = 0.0  # Pontos reais

    def add_task(self, task: Task) -> None:
        """Adicionar tarefa ao sprint."""
        self.tasks.append(task)

    def add_user_story(self, story: UserStory) -> None:
        """Adicionar user story ao sprint."""
        self.user_stories.append(story)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Obter tarefa por ID."""
        return next((t for t in self.tasks if t.id == task_id), None)

    def get_task_status(self, task_id: str) -> Optional[TaskStatus]:
        """Obter status de uma tarefa."""
        task = self.get_task(task_id)
        return task.status if task else None

    def update_task_status(self, task_id: str, status: TaskStatus) -> bool:
        """Atualizar status de tarefa."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False

    def total_days_estimate(self) -> float:
        """Total de dias estimados."""
        return sum(t.days_estimate for t in self.tasks)

    def total_tasks_complete(self) -> int:
        """Contar tarefas completas."""
        return sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETE)

    def total_tasks(self) -> int:
        """Total de tarefas."""
        return len(self.tasks)

    def completion_rate(self) -> float:
        """Taxa de conclusão (0.0-1.0)."""
        if not self.tasks:
            return 0.0
        return self.total_tasks_complete() / self.total_tasks()

    def to_dict(self) -> dict:
        """Serializar sprint."""
        return {
            "id": self.id,
            "release_id": self.release_id,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "phase": self.phase.value,
            "num_tasks": len(self.tasks),
            "num_stories": len(self.user_stories),
            "total_days": self.total_days_estimate(),
            "completion_rate": self.completion_rate(),
            "tasks": [t.to_dict() for t in self.tasks],
        }


class SprintManager:
    """Gerencia sprints de uma release."""

    def __init__(
        self, release_id: str, project_root: Optional[Path] = None
    ):
        """Inicializar gerenciador de sprints.

        Args:
            release_id: ID da release (ex: "R0")
            project_root: Raiz do projeto
        """
        self.release_id = release_id
        self.project_root = project_root or Path.cwd()
        self.release_dir = self.project_root / "docs" / "releases" / release_id
        self.sprints: dict[str, Sprint] = {}

    def create_sprint(
        self,
        sprint_id: str,
        title: str,
        start_date: str,
        end_date: str,
    ) -> Sprint:
        """Criar novo sprint.

        Args:
            sprint_id: ID do sprint (ex: "sprint-0.0")
            title: Título do sprint
            start_date: Data de início (ISO format)
            end_date: Data de fim (ISO format)

        Returns:
            Objeto Sprint criado
        """
        sprint = Sprint(
            id=sprint_id,
            release_id=self.release_id,
            title=title,
            start_date=start_date,
            end_date=end_date,
        )
        self.sprints[sprint_id] = sprint
        return sprint

    def get_sprint(self, sprint_id: str) -> Optional[Sprint]:
        """Obter sprint por ID."""
        return self.sprints.get(sprint_id)

    def list_sprints(self) -> List[Sprint]:
        """Listar sprints em ordem."""
        return sorted(self.sprints.values(), key=lambda s: s.id)

    def initialize_sprint_directory(self, sprint_id: str) -> Path:
        """Criar diretório de sprint com estrutura padrão.

        Cria:
        - README.md: Contexto do sprint
        - TASKS.md: Tarefas detalhadas
        - USER_STORIES.md: User stories
        - BOARD.md: Kanban board
        - STATUS.md: Relatório de status
        - DAILY_STANDUP_[DATE].md: Daily standup template
        - RISK_MITIGATION.md: Riscos e mitigações
        - RETRO.md: Retrospectiva template

        Args:
            sprint_id: ID do sprint

        Returns:
            Caminho do diretório criado
        """
        sprint_dir = self.release_dir / sprint_id
        sprint_dir.mkdir(parents=True, exist_ok=True)

        # Criar estrutura padrão de sprint
        files = [
            "README.md",
            "TASKS.md",
            "USER_STORIES.md",
            "BOARD.md",
            "STATUS.md",
            "RISK_MITIGATION.md",
            "RETRO.md",
        ]

        for filename in files:
            (sprint_dir / filename).touch()

        return sprint_dir

    def export_summary(self) -> dict:
        """Exportar sumário de sprints."""
        sprints_data = []
        total_tasks = 0
        total_complete = 0

        for sprint in self.list_sprints():
            sprints_data.append(sprint.to_dict())
            total_tasks += sprint.total_tasks()
            total_complete += sprint.total_tasks_complete()

        return {
            "release_id": self.release_id,
            "num_sprints": len(self.sprints),
            "total_tasks": total_tasks,
            "total_complete": total_complete,
            "overall_completion_rate": (
                total_complete / total_tasks if total_tasks > 0 else 0.0
            ),
            "sprints": sprints_data,
            "timestamp": datetime.now().isoformat(),
        }
