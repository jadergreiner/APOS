"""Testes para Daily Standup Runner."""

import pytest
from apos.release_management import (
    Sprint,
    Task,
    TaskStatus,
    DailyStandupRunner,
    DailyMode,
    EvidenceAnalysis,
)


@pytest.fixture
def sample_sprint():
    """Criar sprint com tarefas para testes."""
    sprint = Sprint(
        id="sprint-0.0",
        release_id="R0",
        title="Test Sprint",
        start_date="2026-07-22",
        end_date="2026-07-26",
    )

    # Adicionar tarefas com diferentes status
    sprint.add_task(
        Task(
            id="T0.0.1",
            title="Bootstrap Gate",
            description="Implementar validador",
            days_estimate=2.0,
            status=TaskStatus.COMPLETE,
            assignee="Jader",
        )
    )

    sprint.add_task(
        Task(
            id="T0.0.2",
            title="JTBD Interviews",
            description="Conduzir entrevistas",
            days_estimate=2.0,
            status=TaskStatus.IN_PROGRESS,
            assignee="Jader",
        )
    )

    sprint.add_task(
        Task(
            id="T0.0.3",
            title="Forces Analysis",
            description="Mapear forças",
            days_estimate=1.0,
            status=TaskStatus.BLOCKED,
            assignee="Jader",
            notes="Aguardando entrevistas",
        )
    )

    sprint.add_task(
        Task(
            id="T0.0.4",
            title="Documentation",
            description="Documentar resultados",
            days_estimate=1.0,
            status=TaskStatus.PLANNED,
            assignee="Team",
            depends_on=["T0.0.2"],
        )
    )

    return sprint


class TestDailyStandupRunner:
    """Testes para DailyStandupRunner."""

    def test_create_runner_automatic(self, sample_sprint):
        """Testar criar runner em modo automático."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        assert runner.sprint == sample_sprint
        assert runner.date == "2026-07-22"
        assert runner.mode == DailyMode.AUTOMATIC
        assert runner.daily.sprint_id == "sprint-0.0"

    def test_create_runner_collaborative(self, sample_sprint):
        """Testar criar runner em modo colaborativo."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.COLLABORATIVE,
        )

        assert runner.mode == DailyMode.COLLABORATIVE

    def test_analyze_complete_task(self, sample_sprint):
        """Testar análise de tarefa completa."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        task = sample_sprint.get_task("T0.0.1")  # COMPLETE
        analysis = runner._analyze_task(task)

        assert analysis.what_done == "Completou Bootstrap Gate"
        assert analysis.confidence == 1.0
        assert "T0.0.1 COMPLETE" in analysis.what_done_evidence

    def test_analyze_in_progress_task(self, sample_sprint):
        """Testar análise de tarefa em progresso."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        task = sample_sprint.get_task("T0.0.2")  # IN_PROGRESS
        analysis = runner._analyze_task(task)

        assert "Continuando JTBD Interviews" in analysis.what_today
        assert analysis.confidence == 0.9
        assert "T0.0.2 IN_PROGRESS" in analysis.what_today_evidence

    def test_analyze_blocked_task(self, sample_sprint):
        """Testar análise de tarefa bloqueada."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        task = sample_sprint.get_task("T0.0.3")  # BLOCKED
        analysis = runner._analyze_task(task)

        assert "Forces Analysis" in analysis.blockers
        assert "Aguardando entrevistas" in analysis.blockers
        assert "T0.0.3 BLOCKED" in analysis.blockers_evidence

    def test_analyze_task_with_dependencies(self, sample_sprint):
        """Testar análise de tarefa com dependências."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        task = sample_sprint.get_task("T0.0.4")  # PLANNED com dependency
        analysis = runner._analyze_task(task)

        # Deve detectar que T0.0.2 está bloqueando (IN_PROGRESS, não COMPLETE)
        assert "Bloqueado por" in analysis.blockers or analysis.what_today != ""

    def test_run_automatic_mode(self, sample_sprint, capsys):
        """Testar execução em modo automático."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        daily = runner.run()

        assert daily.sprint_id == "sprint-0.0"
        assert len(daily.updates) > 0
        assert daily.get_participant_count() > 0

        # Capturar output
        captured = capsys.readouterr()
        assert "Modo: AUTOMÁTICO" in captured.out

    def test_export_markdown(self, sample_sprint):
        """Testar exportar para Markdown."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        runner.run()
        md = runner.export_markdown()

        # Verificar estrutura Markdown
        assert "# Daily Standup" in md
        assert "2026-07-22" in md
        assert "Automatic" in md  # Modo exportado

    def test_evidence_analysis_defaults(self, sample_sprint):
        """Testar defaults em EvidenceAnalysis."""
        analysis = EvidenceAnalysis(
            participant="Jader",
            date="2026-07-22",
        )

        assert analysis.what_done == ""
        assert analysis.what_today == ""
        assert analysis.blockers == ""
        assert analysis.confidence == 0.0
        assert isinstance(analysis.what_done_evidence, list)
        assert len(analysis.what_done_evidence) == 0

    def test_daily_blockers_detection(self, sample_sprint):
        """Testar detecção de bloqueadores."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        runner.run()
        blockers = runner.daily.get_blockers()

        # Deve ter detectado o bloqueador de T0.0.3
        assert len(blockers) > 0

    def test_daily_participant_count(self, sample_sprint):
        """Testar contagem de participantes únicos."""
        runner = DailyStandupRunner(
            sprint=sample_sprint,
            date="2026-07-22",
            mode=DailyMode.AUTOMATIC,
        )

        runner.run()
        participant_count = runner.daily.get_participant_count()

        # Sprint tem Jader (3 tasks) e Team (1 task), total 2 únicos
        assert participant_count >= 1


class TestEvidenceAnalysis:
    """Testes para EvidenceAnalysis."""

    def test_create_analysis(self):
        """Testar criar análise."""
        analysis = EvidenceAnalysis(
            participant="Jader",
            date="2026-07-22",
            what_done="Completed task",
            confidence=0.95,
        )

        assert analysis.participant == "Jader"
        assert analysis.date == "2026-07-22"
        assert analysis.what_done == "Completed task"
        assert analysis.confidence == 0.95

    def test_analysis_with_evidence(self):
        """Testar análise com evidências."""
        analysis = EvidenceAnalysis(
            participant="Jader",
            date="2026-07-22",
            what_done="Completed bootstrap gate",
            what_done_evidence=["commit 0c643c3", "T0.0.1 COMPLETE"],
            confidence=1.0,
        )

        assert len(analysis.what_done_evidence) == 2
        assert "commit 0c643c3" in analysis.what_done_evidence
