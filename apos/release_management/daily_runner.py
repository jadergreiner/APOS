"""Motor de execução interativa de Daily Standup com 2 modos.

Modo A: Automático
- Analisa evidências (git, task status, board)
- Gera daily standup automaticamente
- Sem interação do usuário

Modo B: Colaborativo
- Sistema analisa evidências
- Apresenta ao usuário para confirmar
- Usuário pode complementar
- Sistema estrutura e documenta
"""

import logging
import subprocess
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum
from pathlib import Path
from datetime import datetime

from apos.release_management.ceremonies import (
    DailyStandup,
    DailyStandupUpdate,
)
from apos.release_management.sprint import Sprint, TaskStatus

logger = logging.getLogger(__name__)


class DailyMode(str, Enum):
    """Modos de execução de Daily Standup."""

    AUTOMATIC = "automatic"  # Opção A: Automático
    COLLABORATIVE = "collaborative"  # Opção B: Colaborativo


@dataclass
class EvidenceAnalysis:
    """Análise de evidências para Daily Standup."""

    participant: str
    date: str

    # O que foi feito ontem (evidências)
    what_done: str = ""
    what_done_evidence: List[str] = None  # Ex: ["commit abc123", "T0.0.1 COMPLETE"]

    # O que vai fazer hoje (inferido de task status)
    what_today: str = ""
    what_today_evidence: List[str] = None  # Ex: ["T0.0.2 IN_PROGRESS"]

    # Bloqueadores detectados
    blockers: str = ""
    blockers_evidence: List[str] = None  # Ex: ["RISK_MITIGATION.md flagged"]

    confidence: float = 0.0  # Confiança da análise (0.0-1.0)

    def __post_init__(self):
        """Inicializar listas vazias."""
        if self.what_done_evidence is None:
            self.what_done_evidence = []
        if self.what_today_evidence is None:
            self.what_today_evidence = []
        if self.blockers_evidence is None:
            self.blockers_evidence = []


class DailyStandupRunner:
    """Motor para executar Daily Standup em 2 modos."""

    def __init__(
        self,
        sprint: Sprint,
        date: str,  # ISO format
        mode: DailyMode = DailyMode.COLLABORATIVE,
        repo_path: Optional[Path] = None,
    ):
        """Inicializar runner de Daily.

        Args:
            sprint: Sprint em execução
            date: Data da daily (ISO format)
            mode: Modo de execução (automatic ou collaborative)
            repo_path: Caminho do repositório git usado para buscar evidências
                de commits (default: Path.cwd())
        """
        self.sprint = sprint
        self.date = date
        self.mode = mode
        self.repo_path = repo_path or Path.cwd()
        self.daily = DailyStandup(sprint_id=sprint.id, date=date)

    def run(self) -> DailyStandup:
        """Executar Daily Standup no modo configurado.

        Returns:
            DailyStandup preenchido
        """
        if self.mode == DailyMode.AUTOMATIC:
            return self._run_automatic()
        else:  # COLLABORATIVE
            return self._run_collaborative()

    def _run_automatic(self) -> DailyStandup:
        """Modo Automático: Inferir de evidências sem interação."""
        print(f"\n{'='*60}")
        print(f"📋 Daily Standup — {self.sprint.id} ({self.date})")
        print(f"{'='*60}")
        print(f"\n🤖 Modo: AUTOMÁTICO (inferência de evidências)")
        print(f"Analisando: commits, task status, board...\n")

        for task in self.sprint.tasks:
            analysis = self._analyze_task(task)

            if analysis.what_done or analysis.what_today or analysis.blockers:
                update = DailyStandupUpdate(
                    participant=analysis.participant,
                    date=self.date,
                    what_done=analysis.what_done,
                    what_today=analysis.what_today,
                    blockers=analysis.blockers,
                    notes=f"Confiança: {analysis.confidence:.0%}\nEvidências: {len(analysis.what_done_evidence) + len(analysis.what_today_evidence) + len(analysis.blockers_evidence)}",
                )
                self.daily.add_update(update)

                print(f"✅ {analysis.participant}")
                print(
                    f"   {analysis.what_done if analysis.what_done else '(nenhuma evidência de conclusão)'}"
                )
                print(
                    f"   {analysis.what_today if analysis.what_today else '(nenhuma tarefa em progresso)'}"
                )
                if analysis.blockers:
                    print(f"   🚨 {analysis.blockers}")
                print()

        print(f"\n{'='*60}")
        print(f"✅ Daily Automática Completa ({len(self.daily.updates)} updates)")
        print(f"{'='*60}\n")

        return self.daily

    def _run_collaborative(self) -> DailyStandup:
        """Modo Colaborativo: Sistema analisa, usuário confirma e complementa."""
        print(f"\n{'='*60}")
        print(f"📋 Daily Standup — {self.sprint.id} ({self.date})")
        print(f"{'='*60}")
        print(f"\n👥 Modo: COLABORATIVO (análise + confirmação do usuário)")
        print(f"Analisando evidências (commits, tasks, board)...\n")

        for task in self.sprint.tasks:
            analysis = self._analyze_task(task)

            print(f"\n{'─'*60}")
            print(f"Participante: {analysis.participant}")
            print(f"{'─'*60}")

            # 1. APRESENTAR ANÁLISE
            print(f"\n📊 Análise de Evidências:")
            print(f"   Confiança: {analysis.confidence:.0%}")

            print(f"\n✅ O que você fez ontem:")
            if analysis.what_done:
                print(f"   → {analysis.what_done}")
                print(f"   Evidências: {', '.join(analysis.what_done_evidence)}")
            else:
                print(f"   (Sistema não encontrou evidências)")

            print(f"\n🎯 O que você vai fazer hoje:")
            if analysis.what_today:
                print(f"   → {analysis.what_today}")
                print(f"   Evidências: {', '.join(analysis.what_today_evidence)}")
            else:
                print(f"   (Sistema não encontrou tarefas em progresso)")

            if analysis.blockers:
                print(f"\n🚨 Bloqueadores detectados:")
                print(f"   → {analysis.blockers}")
                print(f"   Evidências: {', '.join(analysis.blockers_evidence)}")

            # 2. SOLICITAR CONFIRMAÇÃO E COMPLEMENTOS
            print(f"\n{'─'*60}")
            print(f"🔄 Sua volta:")
            print(f"{'─'*60}")

            confirmed_done = input(
                f"\n✅ Isso está correto? (Enter para confirmar ou digite nova descrição):\n> "
            )
            if confirmed_done:
                what_done = confirmed_done
            else:
                what_done = analysis.what_done

            confirmed_today = input(
                f"\n🎯 Seu plano para hoje? (Enter para confirmar ou digite novo):\n> "
            )
            if confirmed_today:
                what_today = confirmed_today
            else:
                what_today = analysis.what_today

            blockers_input = input(f"\n🚨 Algum bloqueador? (Enter se nenhum, ou descreva):\n> ")
            blockers = blockers_input if blockers_input else analysis.blockers

            # 3. ESTRUTURAR E DOCUMENTAR
            update = DailyStandupUpdate(
                participant=analysis.participant,
                date=self.date,
                what_done=what_done,
                what_today=what_today,
                blockers=blockers,
                notes=f"Confiança inicial: {analysis.confidence:.0%}\nConfirmado e complementado pelo usuário",
            )
            self.daily.add_update(update)

            print(f"\n✅ Update de {analysis.participant} registrado!")

        # 4. SUMÁRIO FINAL
        print(f"\n{'='*60}")
        print(f"📊 SUMÁRIO DA DAILY")
        print(f"{'='*60}")
        print(f"Participantes: {self.daily.get_participant_count()}")
        print(f"Updates: {len(self.daily.updates)}")
        print(f"Bloqueadores: {len(self.daily.get_blockers())}")

        if self.daily.get_blockers():
            print(f"\n🚨 Bloqueadores Críticos:")
            for blocker in self.daily.get_blockers():
                print(f"   • {blocker}")

        print(f"\n{'='*60}\n")

        return self.daily

    def _analyze_task(self, task) -> EvidenceAnalysis:
        """Analisar tarefa para extrair evidências.

        Args:
            task: Tarefa a analisar

        Returns:
            EvidenceAnalysis com conclusões
        """
        analysis = EvidenceAnalysis(
            participant=task.assignee or "Unassigned",
            date=self.date,
        )

        # Analisar status da tarefa
        if task.status == TaskStatus.COMPLETE:
            analysis.what_done = f"Completou {task.title}"
            analysis.what_done_evidence = [f"{task.id} COMPLETE"]
            analysis.what_done_evidence.extend(
                self._get_git_evidence(task, self.date, analysis.participant)
            )
            analysis.confidence = 1.0

        elif task.status == TaskStatus.IN_PROGRESS:
            analysis.what_today = f"Continuando {task.title}"
            analysis.what_today_evidence = [f"{task.id} IN_PROGRESS"]
            analysis.what_today_evidence.extend(
                self._get_git_evidence(task, self.date, analysis.participant)
            )
            analysis.confidence = 0.9

        elif task.status == TaskStatus.BLOCKED:
            analysis.blockers = f"{task.title} está bloqueado"
            analysis.blockers_evidence = [f"{task.id} BLOCKED"]
            if task.notes:
                analysis.blockers += f": {task.notes}"
            analysis.confidence = 1.0

        elif task.status == TaskStatus.PLANNED:
            analysis.what_today = f"Iniciando {task.title}"
            analysis.what_today_evidence = [f"{task.id} PLANNED"]
            analysis.confidence = 0.7

        # Validar dependências
        if task.depends_on:
            blocking_tasks = [
                self.sprint.get_task(dep_id)
                for dep_id in task.depends_on
                if self.sprint.get_task(dep_id)
            ]
            blocking_incomplete = [
                t for t in blocking_tasks if t and t.status != TaskStatus.COMPLETE
            ]
            if blocking_incomplete:
                analysis.blockers = (
                    f"Bloqueado por: {', '.join(t.title for t in blocking_incomplete)}"
                )
                analysis.blockers_evidence.extend(
                    [f"{t.id} {t.status.value}" for t in blocking_incomplete]
                )

        return analysis

    def _get_git_evidence(
        self, task, since_date: str, participant: Optional[str] = None
    ) -> List[str]:
        """Buscar evidências reais de commits no git log.

        Roda `git log --since=<since_date> [--author=<participant>] --oneline
        --no-merges` no repositório configurado em self.repo_path. Falhas
        (diretório não é repo git, git ausente, timeout) não propagam
        exceção — retornam lista vazia e registram warning, para não
        quebrar a execução da daily.

        Args:
            task: Tarefa sendo analisada (reservado para filtros futuros)
            since_date: Data a partir da qual buscar commits (ISO format)
            participant: Nome do autor para filtrar (--author). Se None ou
                "Unassigned", não filtra por autor.

        Returns:
            Lista de strings "commit {hash}: {mensagem}" para cada commit
            encontrado, ou lista vazia se nenhum commit for encontrado ou
            se a busca falhar.
        """
        cmd = ["git", "log", f"--since={since_date}", "--oneline", "--no-merges"]
        if participant and participant != "Unassigned":
            cmd.append(f"--author={participant}")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5,
            )
        except (subprocess.TimeoutExpired, OSError) as e:
            logger.warning("Falha ao buscar evidências git: %s", e)
            return []

        if result.returncode != 0:
            logger.warning(
                "git log retornou código %s: %s",
                result.returncode,
                result.stderr.strip(),
            )
            return []

        evidence = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            commit_hash, _, message = line.partition(" ")
            evidence.append(f"commit {commit_hash}: {message}")

        return evidence

    def export_markdown(self) -> str:
        """Exportar Daily em formato Markdown.

        Returns:
            Conteúdo Markdown formatado
        """
        md = f"# Daily Standup — {self.sprint.id}\n\n"
        md += f"**Data:** {self.date}\n"
        md += f"**Modo:** {self.mode.value.title()}\n"
        md += f"**Participantes:** {self.daily.get_participant_count()}\n"
        md += f"**Updates:** {len(self.daily.updates)}\n\n"

        md += "---\n\n"

        for update in self.daily.updates:
            md += f"## {update.participant}\n\n"

            if update.what_done:
                md += f"**✅ Ontem:** {update.what_done}\n\n"

            if update.what_today:
                md += f"**🎯 Hoje:** {update.what_today}\n\n"

            if update.blockers:
                md += f"**🚨 Blockers:** {update.blockers}\n\n"

            if update.notes:
                md += f"*Notas:* {update.notes}\n\n"

            md += "---\n\n"

        if self.daily.get_blockers():
            md += "## 🚨 Bloqueadores Críticos\n\n"
            for blocker in self.daily.get_blockers():
                md += f"- {blocker}\n"
            md += "\n"

        if self.daily.action_items:
            md += "## 📋 Ações Identificadas\n\n"
            for action in self.daily.action_items:
                md += f"- [ ] {action}\n"
            md += "\n"

        return md

    def save_to_file(self, sprint_dir: Path) -> Path:
        """Salvar Daily em arquivo Markdown.

        Args:
            sprint_dir: Diretório do sprint

        Returns:
            Path do arquivo criado
        """
        filename = f"DAILY_STANDUP_{self.date}.md"
        filepath = sprint_dir / filename

        md_content = self.export_markdown()

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"✅ Daily salva em: {filepath}")

        return filepath
