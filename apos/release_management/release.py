"""Release management — estrutura para planejar e rastrear releases."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pathlib import Path


class ReleasePhase(str, Enum):
    """Fases de uma release."""

    PLANNING = "planning"
    ACTIVE = "active"
    SHIPPED = "shipped"
    RETRO = "retro"


@dataclass
class ReleaseObjective:
    """Um objetivo em uma release."""

    id: str
    title: str
    description: str
    key_results: List[str] = field(default_factory=list)
    status: str = "planned"  # planned, in_progress, at_risk, complete
    owner: Optional[str] = None


@dataclass
class Release:
    """Representa uma release (R0, R1, etc.)."""

    id: str  # Ex: "R0", "R1"
    title: str
    description: str
    start_date: str  # ISO format: 2026-07-19
    end_date: str
    phase: ReleasePhase = ReleasePhase.PLANNING
    objectives: List[ReleaseObjective] = field(default_factory=list)
    sprints: List[str] = field(default_factory=list)  # Sprint IDs

    def add_objective(self, objective: ReleaseObjective) -> None:
        """Adicionar objetivo à release."""
        self.objectives.append(objective)

    def add_sprint(self, sprint_id: str) -> None:
        """Registrar sprint como parte desta release."""
        if sprint_id not in self.sprints:
            self.sprints.append(sprint_id)

    def to_dict(self) -> dict:
        """Serializar para dicionário."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "phase": self.phase.value,
            "num_objectives": len(self.objectives),
            "num_sprints": len(self.sprints),
            "objectives": [
                {
                    "id": obj.id,
                    "title": obj.title,
                    "status": obj.status,
                    "key_results": len(obj.key_results),
                }
                for obj in self.objectives
            ],
            "sprints": self.sprints,
        }


class ReleaseManager:
    """Gerencia releases de um projeto."""

    def __init__(self, project_name: str, project_root: Optional[Path] = None):
        """Inicializar gerenciador de releases.

        Args:
            project_name: Nome do projeto
            project_root: Raiz do projeto (default: diretório atual)
        """
        self.project_name = project_name
        self.project_root = project_root or Path.cwd()
        self.releases_dir = self.project_root / "docs" / "releases"
        self.releases: dict[str, Release] = {}

    def create_release(
        self,
        release_id: str,
        title: str,
        description: str,
        start_date: str,
        end_date: str,
    ) -> Release:
        """Criar nova release.

        Args:
            release_id: ID da release (ex: "R0", "R1")
            title: Título/nome da release
            description: Descrição do escopo
            start_date: Data de início (ISO format)
            end_date: Data de fim (ISO format)

        Returns:
            Objeto Release criado
        """
        release = Release(
            id=release_id,
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )
        self.releases[release_id] = release
        return release

    def get_release(self, release_id: str) -> Optional[Release]:
        """Obter release por ID."""
        return self.releases.get(release_id)

    def list_releases(self) -> List[Release]:
        """Listar todas as releases em ordem."""
        return sorted(self.releases.values(), key=lambda r: r.id)

    def initialize_release_directory(self, release_id: str) -> Path:
        """Criar diretório de release com estrutura padrão.

        Args:
            release_id: ID da release

        Returns:
            Caminho do diretório criado
        """
        release_dir = self.releases_dir / release_id
        release_dir.mkdir(parents=True, exist_ok=True)

        # Criar estrutura padrão
        (release_dir / "README.md").touch()
        (release_dir / "OKR.md").touch()
        (release_dir / "SPRINT_PLAN.md").touch()
        (release_dir / "BACKLOG.md").touch()
        (release_dir / "DEPENDENCY_MAP.md").touch()

        return release_dir

    def export_summary(self) -> dict:
        """Exportar sumário de todas as releases."""
        return {
            "project": self.project_name,
            "releases": [r.to_dict() for r in self.list_releases()],
            "total_releases": len(self.releases),
            "timestamp": datetime.now().isoformat(),
        }
