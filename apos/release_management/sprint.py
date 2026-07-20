"""Sprint management — estrutura para planejar e rastrear sprints."""

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


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


# Mapeamento de valores de status em texto livre (formato narrativo de
# TASKS.md, ex: "**Status:** COMPLETO (Em R0/APOS...)") para TaskStatus.
# Chaves em minúsculas; o parser normaliza e remove parenteticais antes de
# comparar. Estender aqui ao encontrar novos rótulos usados nos TASKS.md.
NARRATIVE_STATUS_MAP = {
    "não iniciado": TaskStatus.PLANNED,
    "planejado": TaskStatus.PLANNED,
    "planned": TaskStatus.PLANNED,
    "definido": TaskStatus.PLANNED,
    "em andamento": TaskStatus.IN_PROGRESS,
    "ativo": TaskStatus.IN_PROGRESS,
    "in progress": TaskStatus.IN_PROGRESS,
    "em revisão": TaskStatus.IN_REVIEW,
    "completo": TaskStatus.COMPLETE,
    "concluído": TaskStatus.COMPLETE,
    "complete": TaskStatus.COMPLETE,
    "bloqueado": TaskStatus.BLOCKED,
    "blocked": TaskStatus.BLOCKED,
}

# Formato tabular: qualquer linha de cabeçalho "| ID | ... |" em qualquer
# lugar do arquivo indica que o documento usa o formato gerado por
# ReleaseTemplateGenerator.generate_sprint_tasks_template().
_TABULAR_HEADER_RE = re.compile(r"^\s*\|\s*ID\s*\|", re.IGNORECASE | re.MULTILINE)

# Formato narrativo: headers "## {ID}: {Título}" — só é considerado task
# se o ID casar com o padrão usado no projeto (ex: T0.0.1, T0.0.A, T1.2.5).
_NARRATIVE_HEADER_RE = re.compile(r"^##\s+(?P<id>\S+?):\s*(?P<title>.+)$", re.MULTILINE)
_TASK_ID_PATTERN = re.compile(r"^T\d+\.\d+\.\w+$")


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
    status_history: List[dict] = field(default_factory=list)  # Histórico de transições
    rework_count: int = 0  # Quantas vezes retrabalhou (voltou de IN_REVIEW/COMPLETE)

    def cycle_time_days(self) -> Optional[float]:
        """Calcula o cycle time em dias para a tarefa.

        Cycle time = tempo desde que entrou em IN_PROGRESS até sair para COMPLETE.

        Returns:
            Dias (float) entre IN_PROGRESS e COMPLETE, ou None se não completou.
        """
        if self.status != TaskStatus.COMPLETE:
            return None

        # Encontrar timestamps de IN_PROGRESS e COMPLETE
        in_progress_time = None
        complete_time = None

        for entry in self.status_history:
            if entry.get("status") == TaskStatus.IN_PROGRESS.value:
                if in_progress_time is None:  # Primeira vez que entrou em progresso
                    in_progress_time = entry.get("timestamp")
            elif entry.get("status") == TaskStatus.COMPLETE.value:
                complete_time = entry.get("timestamp")

        if in_progress_time is None or complete_time is None:
            return None

        # Calcular diferença em dias
        try:
            start = datetime.fromisoformat(in_progress_time)
            end = datetime.fromisoformat(complete_time)
        except (ValueError, TypeError):
            return None

        if end < start:
            return 0.0

        delta = end - start

        return delta.total_seconds() / (24 * 3600)  # Converter para dias

    def to_dict(self) -> dict:
        """Serializar tarefa."""
        return {
            "id": self.id,
            "title": self.title,
            "days_estimate": self.days_estimate,
            "status": self.status.value,
            "assignee": self.assignee,
            "depends_on": self.depends_on,
            "cycle_time_days": self.cycle_time_days(),
            "rework_count": self.rework_count,
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

    @classmethod
    def load_from_markdown(
        cls,
        sprint_id: str,
        release_id: str,
        tasks_md_path: Path,
        title: str = "",
        start_date: str = "",
        end_date: str = "",
    ) -> "Sprint":
        """Reconstruir um Sprint a partir de um arquivo TASKS.md.

        Não parseia BOARD.md nem reconstrói status_history/timestamps — o
        objetivo é apenas reconstruir tasks + status atual a partir de
        TASKS.md.

        Suporta dois formatos, detectados automaticamente:
        - **Tabular**: tabelas Markdown "| ID | Título | Descrição | Duração
          | Status | Responsável |" sob headers "### Tier N: ..." (formato
          gerado por ReleaseTemplateGenerator.generate_sprint_tasks_template()).
          Ignora linhas de cabeçalho, separadores e placeholders não
          preenchidos (ID vazio ou "T")
        - **Narrativo**: headers "## {ID}: {Título}" com campos em negrito
          ("**Objetivo:**", "**Esforço:**", "**Status:**", "**Responsável:**")
          — formato usado nos TASKS.md reais do projeto

        Args:
            sprint_id: ID do sprint (ex: "sprint-0.0")
            release_id: ID da release (ex: "R0")
            tasks_md_path: Caminho para o arquivo TASKS.md
            title: Título do sprint (opcional, default: sprint_id)
            start_date: Data de início (opcional)
            end_date: Data de fim (opcional)

        Returns:
            Sprint reconstruído com as tasks encontradas no arquivo

        Raises:
            FileNotFoundError: se tasks_md_path não existir
            ValueError: se o formato do arquivo não for reconhecido (nem
                tabular, nem narrativo com pelo menos um header de task)
        """
        tasks_md_path = Path(tasks_md_path)
        if not tasks_md_path.exists():
            raise FileNotFoundError(f"Arquivo TASKS.md não encontrado: {tasks_md_path}")

        content = tasks_md_path.read_text(encoding="utf-8")

        sprint = cls(
            id=sprint_id,
            release_id=release_id,
            title=title or sprint_id,
            start_date=start_date,
            end_date=end_date,
        )

        if _TABULAR_HEADER_RE.search(content):
            cls._parse_tabular_format(sprint, content)
        elif any(
            _TASK_ID_PATTERN.match(m.group("id")) for m in _NARRATIVE_HEADER_RE.finditer(content)
        ):
            cls._parse_narrative_format(sprint, content)
        else:
            raise ValueError(
                f"Formato de TASKS.md não reconhecido em '{tasks_md_path}': "
                "esperado formato tabular ('| ID | Título | ... |') ou "
                "narrativo ('## T0.0.1: Título' com campos em negrito)"
            )

        return sprint

    @classmethod
    def _parse_tabular_format(cls, sprint: "Sprint", content: str) -> None:
        """Parsear formato tabular ("| ID | Título | ... |") e popular sprint.

        Comportamento inalterado desde a implementação original (Fase 1):
        tabelas sob headers "### Tier N: ...", ignora cabeçalho, separador
        e placeholders não preenchidos (ID vazio ou "T").
        """
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped.startswith("|"):
                continue

            cells = [c.strip() for c in stripped.strip("|").split("|")]

            if len(cells) < 6:
                continue

            first_cell = cells[0]

            # Ignorar linha de cabeçalho ("ID | Título | ...") e separador ("----|----|...")
            if first_cell.lower() == "id" or (first_cell and set(first_cell) <= {"-"}):
                continue

            task_id = first_cell
            if not task_id or task_id == "T":
                continue  # Placeholder não preenchido (template em branco)

            title_cell, description_cell, duration_cell, status_cell, assignee_cell = cells[1:6]

            days_estimate = cls._parse_duration(duration_cell)
            status = cls._parse_status(status_cell)
            assignee = assignee_cell if assignee_cell else None

            task = Task(
                id=task_id,
                title=title_cell,
                description=description_cell,
                days_estimate=days_estimate,
                status=status,
                assignee=assignee,
            )
            sprint.add_task(task)

    @classmethod
    def _parse_narrative_format(cls, sprint: "Sprint", content: str) -> None:
        """Parsear formato narrativo ("## {ID}: {Título}") e popular sprint.

        Para cada header cujo ID case com _TASK_ID_PATTERN, extrai campos
        em negrito ("**Objetivo:**", "**Esforço:**", "**Status:**",
        "**Responsável:**") do corpo da seção (até o próximo header "## "
        ou fim do arquivo). Headers cujo ID não case com o padrão (ex:
        "## Resumo") são ignorados silenciosamente.
        """
        matches = list(_NARRATIVE_HEADER_RE.finditer(content))

        for i, match in enumerate(matches):
            task_id = match.group("id").strip()
            if not _TASK_ID_PATTERN.match(task_id):
                continue  # Não é uma seção de task (ex: "## Resumo")

            title_raw = match.group("title").strip()
            # Remover parenteticais no fim do título, ex: "(1 dia-pessoa)"
            title = re.sub(r"\s*\([^)]*\)\s*$", "", title_raw).strip()

            body_start = match.end()
            body_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            body = content[body_start:body_end]

            description = cls._extract_narrative_field(body, "Objetivo") or ""
            effort_str = cls._extract_narrative_field(body, "Esforço")
            status_str = cls._extract_narrative_field(body, "Status")
            assignee_str = cls._extract_narrative_field(body, "Responsável")

            days_estimate = cls._parse_duration(effort_str.replace(",", ".")) if effort_str else 0.0
            status = cls._parse_narrative_status(status_str) if status_str else TaskStatus.PLANNED
            assignee = assignee_str if assignee_str else None

            task = Task(
                id=task_id,
                title=title,
                description=description,
                days_estimate=days_estimate,
                status=status,
                assignee=assignee,
            )
            sprint.add_task(task)

    @staticmethod
    def _extract_narrative_field(body: str, field_name: str) -> Optional[str]:
        """Extrair valor de um campo em negrito ("**Campo:** valor").

        Captura o texto até a próxima linha em branco, o próximo campo em
        negrito, ou o fim do corpo — o que vier primeiro.

        Returns:
            Texto extraído (strip aplicado), ou None se o campo não existir.
        """
        pattern = rf"\*\*{re.escape(field_name)}:\*\*\s*(.+?)(?=\n[ \t]*\n|\n\*\*[^\n*]+:\*\*|\Z)"
        match = re.search(pattern, body, re.DOTALL)
        if not match:
            return None
        return match.group(1).strip()

    @staticmethod
    def _parse_narrative_status(status_str: str) -> TaskStatus:
        """Mapear valor de status narrativo para TaskStatus via NARRATIVE_STATUS_MAP.

        Remove parenteticais (ex: "COMPLETO (Em R0/APOS...)" -> "COMPLETO")
        antes de comparar. Valor não reconhecido -> TaskStatus.PLANNED +
        warning de log.
        """
        cleaned = re.sub(r"\([^)]*\)", "", status_str).strip()
        # Remove markdown bold markers and leading emoji/symbols (ex: "✅ **COMPLETO**")
        cleaned = cleaned.replace("*", "").strip()
        cleaned = re.sub(r"^[^\w]+", "", cleaned, flags=re.UNICODE).strip()
        normalized = cleaned.lower()

        for key in sorted(NARRATIVE_STATUS_MAP, key=len, reverse=True):
            if normalized.startswith(key):
                return NARRATIVE_STATUS_MAP[key]

        logger.warning("Status narrativo desconhecido '%s', usando TaskStatus.PLANNED", status_str)
        return TaskStatus.PLANNED

    @staticmethod
    def _parse_duration(duration_str: str) -> float:
        """Parsear duração de string ("2d", "2", "2.0", "2 dias") para float.

        Se não conseguir extrair um número, registra warning e retorna 0.0
        em vez de levantar exceção.
        """
        match = re.search(r"(\d+(?:\.\d+)?)", duration_str)
        if match:
            return float(match.group(1))
        logger.warning("Não foi possível parsear duração '%s', usando 0.0", duration_str)
        return 0.0

    @staticmethod
    def _parse_status(status_str: str) -> TaskStatus:
        """Parsear status de string para TaskStatus enum (case-insensitive).

        Se o valor não corresponder a nenhum TaskStatus conhecido, registra
        warning e retorna TaskStatus.PLANNED em vez de levantar exceção.
        """
        normalized = status_str.strip().lower()
        try:
            return TaskStatus(normalized)
        except ValueError:
            logger.warning("Status desconhecido '%s', usando TaskStatus.PLANNED", status_str)
            return TaskStatus.PLANNED

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
        """Atualizar status de tarefa.

        Registra a transição no histórico de status e incrementa rework_count
        se a tarefa voltou para IN_PROGRESS de IN_REVIEW ou COMPLETE.
        """
        task = self.get_task(task_id)
        if task:
            # Registrar transição no histórico
            task.status_history.append(
                {
                    "status": status.value,
                    "timestamp": datetime.now().isoformat(),
                }
            )

            # Contar retrabalho: se volta para IN_PROGRESS de IN_REVIEW ou COMPLETE
            if status == TaskStatus.IN_PROGRESS:
                if task.status in (TaskStatus.IN_REVIEW, TaskStatus.COMPLETE):
                    task.rework_count += 1

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

    def average_cycle_time(self) -> Optional[float]:
        """Calcula o cycle time médio do sprint.

        Média de cycle_time_days() entre tasks que já completaram.
        Ignora tasks que ainda não completaram (retornam None).

        Returns:
            Dias médios, ou None se nenhuma task completou.
        """
        completed_cycle_times = [
            t.cycle_time_days() for t in self.tasks if t.cycle_time_days() is not None
        ]

        if not completed_cycle_times:
            return None

        return sum(completed_cycle_times) / len(completed_cycle_times)

    def rework_rate(self) -> float:
        """Calcula a taxa de retrabalho do sprint.

        Proporção de tasks com rework_count > 0 sobre o total de tasks.

        Returns:
            Taxa 0.0-1.0, ou 0.0 se não há tasks.
        """
        if not self.tasks:
            return 0.0

        tasks_with_rework = sum(1 for t in self.tasks if t.rework_count > 0)
        return tasks_with_rework / len(self.tasks)

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
            "average_cycle_time": self.average_cycle_time(),
            "rework_rate": self.rework_rate(),
            "tasks": [t.to_dict() for t in self.tasks],
        }


class SprintManager:
    """Gerencia sprints de uma release."""

    def __init__(self, release_id: str, project_root: Optional[Path] = None):
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
            "overall_completion_rate": (total_complete / total_tasks if total_tasks > 0 else 0.0),
            "sprints": sprints_data,
            "timestamp": datetime.now().isoformat(),
        }
