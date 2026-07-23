"""Testes para Release Management Framework."""

import pytest
from pathlib import Path
from apos.release_management import (
    Release,
    ReleaseManager,
    ReleaseObjective,
    Sprint,
    SprintManager,
    Task,
    TaskStatus,
    UserStory,
    DailyStandup,
    DailyStandupUpdate,
    SprintPlanningSession,
    Retrospective,
    RetroAction,
    RoadmapCeremony,
    RoadmapPhase,
)


class TestRelease:
    """Testes para classe Release."""

    def test_create_release(self):
        """Testar criação de release."""
        release = Release(
            id="R0",
            title="Bootstrap",
            description="Fundações",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )
        assert release.id == "R0"
        assert release.title == "Bootstrap"
        assert len(release.objectives) == 0
        assert len(release.sprints) == 0

    def test_add_objective(self):
        """Testar adicionar objetivo."""
        release = Release(
            id="R0",
            title="Bootstrap",
            description="Fundações",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )

        obj = ReleaseObjective(
            id="R0-O1",
            title="Teste",
            description="Teste objetivo",
            key_results=["KR1", "KR2"],
        )

        release.add_objective(obj)
        assert len(release.objectives) == 1
        assert release.objectives[0].id == "R0-O1"

    def test_add_sprint(self):
        """Testar adicionar sprint."""
        release = Release(
            id="R0",
            title="Bootstrap",
            description="Fundações",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )

        release.add_sprint("sprint-0.0")
        release.add_sprint("sprint-0.0")  # Duplicado

        assert len(release.sprints) == 1
        assert "sprint-0.0" in release.sprints

    def test_to_dict(self):
        """Testar serialização."""
        release = Release(
            id="R0",
            title="Bootstrap",
            description="Fundações",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )

        data = release.to_dict()
        assert data["id"] == "R0"
        assert data["title"] == "Bootstrap"
        assert data["num_objectives"] == 0
        assert data["num_sprints"] == 0


class TestReleaseManager:
    """Testes para ReleaseManager."""

    def test_create_release(self):
        """Testar criar release via manager."""
        rm = ReleaseManager(project_name="test-project")

        release = rm.create_release(
            release_id="R0",
            title="Bootstrap",
            description="Fundações",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )

        assert release.id == "R0"
        assert rm.get_release("R0") == release

    def test_list_releases(self):
        """Testar listar releases."""
        rm = ReleaseManager(project_name="test-project")

        rm.create_release("R0", "Bootstrap", "Desc", "2026-07-19", "2026-08-02")
        rm.create_release("R1", "Knowledge Graph", "Desc", "2026-09-01", "2026-11-30")

        releases = rm.list_releases()
        assert len(releases) == 2
        assert releases[0].id == "R0"
        assert releases[1].id == "R1"

    def test_export_summary(self):
        """Testar export de sumário."""
        rm = ReleaseManager(project_name="test-project")
        rm.create_release("R0", "Bootstrap", "Desc", "2026-07-19", "2026-08-02")

        summary = rm.export_summary()
        assert summary["project"] == "test-project"
        assert summary["total_releases"] == 1
        assert len(summary["releases"]) == 1


class TestSprint:
    """Testes para classe Sprint."""

    def test_create_sprint(self):
        """Testar criação de sprint."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        assert sprint.id == "sprint-0.0"
        assert sprint.release_id == "R0"
        assert len(sprint.tasks) == 0

    def test_add_task(self):
        """Testar adicionar tarefa."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Bootstrap Gate",
            description="Implementar validador",
            days_estimate=2.0,
        )

        sprint.add_task(task)
        assert len(sprint.tasks) == 1
        assert sprint.get_task("T0.0.1") == task

    def test_total_days_estimate(self):
        """Testar cálculo total de dias."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        sprint.add_task(
            Task(
                id="T0.0.1",
                title="Task 1",
                description="Desc",
                days_estimate=2.0,
            )
        )
        sprint.add_task(
            Task(
                id="T0.0.2",
                title="Task 2",
                description="Desc",
                days_estimate=1.5,
            )
        )

        assert sprint.total_days_estimate() == 3.5

    def test_completion_rate(self):
        """Testar taxa de conclusão."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task1 = Task(
            id="T0.0.1",
            title="Task 1",
            description="Desc",
            days_estimate=2.0,
            status=TaskStatus.COMPLETE,
        )
        task2 = Task(
            id="T0.0.2",
            title="Task 2",
            description="Desc",
            days_estimate=1.5,
            status=TaskStatus.PLANNED,
        )

        sprint.add_task(task1)
        sprint.add_task(task2)

        assert sprint.completion_rate() == 0.5
        assert sprint.total_tasks_complete() == 1
        assert sprint.total_tasks() == 2

    def test_add_user_story(self):
        """Testar adicionar user story."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        story = UserStory(
            id="US-0.0.1",
            title="Como PM...",
            description="Quero validar...",
            story_points=3.0,
        )

        sprint.add_user_story(story)
        assert len(sprint.user_stories) == 1

    def test_update_task_status(self):
        """Testar atualizar status de tarefa."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Task",
            description="Desc",
            days_estimate=2.0,
        )

        sprint.add_task(task)
        result = sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)

        assert result is True
        assert sprint.get_task("T0.0.1").status == TaskStatus.IN_PROGRESS

    def test_task_cycle_time_days_when_complete(self):
        """Testar cálculo de cycle time para tarefa completa."""
        from datetime import datetime, timedelta

        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Task",
            description="Desc",
            days_estimate=2.0,
        )

        sprint.add_task(task)

        # Simular transições
        now = datetime.now()
        task.status_history = [
            {
                "status": TaskStatus.IN_PROGRESS.value,
                "timestamp": now.isoformat(),
            },
            {
                "status": TaskStatus.COMPLETE.value,
                "timestamp": (now + timedelta(days=2)).isoformat(),
            },
        ]
        task.status = TaskStatus.COMPLETE

        cycle_time = task.cycle_time_days()
        assert cycle_time is not None
        assert 1.9 < cycle_time < 2.1  # Aproximadamente 2 dias

    def test_task_cycle_time_days_when_not_complete_returns_none(self):
        """Testar que cycle_time_days retorna None para tarefa não completa."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Task",
            description="Desc",
            days_estimate=2.0,
            status=TaskStatus.IN_PROGRESS,
        )

        sprint.add_task(task)

        assert task.cycle_time_days() is None

    def test_task_rework_count_increments_on_status_regression(self):
        """Testar que rework_count incrementa quando tarefa volta para IN_PROGRESS."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Task",
            description="Desc",
            days_estimate=2.0,
        )

        sprint.add_task(task)

        # Workflow: PLANNED → IN_PROGRESS → IN_REVIEW → IN_PROGRESS (retrabalho!)
        sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
        assert task.rework_count == 0

        sprint.update_task_status("T0.0.1", TaskStatus.IN_REVIEW)
        assert task.rework_count == 0

        sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
        assert task.rework_count == 1  # ← Incrementou!

        # Mais uma vez: IN_REVIEW → IN_PROGRESS
        sprint.update_task_status("T0.0.1", TaskStatus.IN_REVIEW)
        sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
        assert task.rework_count == 2

    def test_sprint_average_cycle_time(self):
        """Testar cálculo de cycle time médio da sprint."""
        from datetime import datetime, timedelta

        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        now = datetime.now()

        # Task 1: 2 dias de cycle time
        task1 = Task(
            id="T0.0.1",
            title="Task 1",
            description="Desc",
            days_estimate=2.0,
            status=TaskStatus.COMPLETE,
            status_history=[
                {
                    "status": TaskStatus.IN_PROGRESS.value,
                    "timestamp": now.isoformat(),
                },
                {
                    "status": TaskStatus.COMPLETE.value,
                    "timestamp": (now + timedelta(days=2)).isoformat(),
                },
            ],
        )

        # Task 2: 4 dias de cycle time
        task2 = Task(
            id="T0.0.2",
            title="Task 2",
            description="Desc",
            days_estimate=2.0,
            status=TaskStatus.COMPLETE,
            status_history=[
                {
                    "status": TaskStatus.IN_PROGRESS.value,
                    "timestamp": now.isoformat(),
                },
                {
                    "status": TaskStatus.COMPLETE.value,
                    "timestamp": (now + timedelta(days=4)).isoformat(),
                },
            ],
        )

        sprint.add_task(task1)
        sprint.add_task(task2)

        avg = sprint.average_cycle_time()
        assert avg is not None
        assert 2.9 < avg < 3.1  # Média de 3 dias

    def test_sprint_rework_rate(self):
        """Testar cálculo de taxa de retrabalho da sprint."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        # 3 tasks: 1 com retrabalho, 2 sem
        task1 = Task(
            id="T0.0.1",
            title="Task 1",
            description="Desc",
            days_estimate=2.0,
            rework_count=2,  # Retrabalhado 2 vezes
        )
        task2 = Task(
            id="T0.0.2",
            title="Task 2",
            description="Desc",
            days_estimate=2.0,
            rework_count=0,  # Sem retrabalho
        )
        task3 = Task(
            id="T0.0.3",
            title="Task 3",
            description="Desc",
            days_estimate=2.0,
            rework_count=0,  # Sem retrabalho
        )

        sprint.add_task(task1)
        sprint.add_task(task2)
        sprint.add_task(task3)

        rate = sprint.rework_rate()
        assert rate == pytest.approx(1.0 / 3.0, abs=0.01)  # 1 de 3 tarefas

    def test_status_history_is_recorded_on_update_task_status(self):
        """Testar que status_history é preenchido ao atualizar status."""
        sprint = Sprint(
            id="sprint-0.0",
            release_id="R0",
            title="Scaffold",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        task = Task(
            id="T0.0.1",
            title="Task",
            description="Desc",
            days_estimate=2.0,
        )

        sprint.add_task(task)

        # Inicialmente vazia
        assert len(task.status_history) == 0

        # Primeira transição
        sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
        assert len(task.status_history) == 1
        assert task.status_history[0]["status"] == TaskStatus.IN_PROGRESS.value
        assert "timestamp" in task.status_history[0]

        # Segunda transição
        sprint.update_task_status("T0.0.1", TaskStatus.IN_REVIEW)
        assert len(task.status_history) == 2
        assert task.status_history[1]["status"] == TaskStatus.IN_REVIEW.value


class TestDailyStandup:
    """Testes para Daily Standup."""

    def test_create_daily(self):
        """Testar criar daily standup."""
        daily = DailyStandup(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        assert daily.sprint_id == "sprint-0.0"
        assert len(daily.updates) == 0

    def test_add_update(self):
        """Testar adicionar update."""
        daily = DailyStandup(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        update = DailyStandupUpdate(
            participant="Jader",
            date="2026-07-22",
            what_done="Scaffolding",
            what_today="Bootstrap Gate",
            blockers="Nenhum",
        )

        daily.add_update(update)
        assert len(daily.updates) == 1

    def test_get_blockers(self):
        """Testar extrair bloqueadores."""
        daily = DailyStandup(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        daily.add_update(
            DailyStandupUpdate(
                participant="Jader",
                date="2026-07-22",
                what_done="Scaffolding",
                what_today="Bootstrap Gate",
                blockers="Agendamento",
            )
        )

        blockers = daily.get_blockers()
        assert "Agendamento" in blockers


class TestSprintPlanningSession:
    """Testes para Sprint Planning."""

    def test_create_planning(self):
        """Testar criar sprint planning."""
        planning = SprintPlanningSession(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        assert planning.sprint_id == "sprint-0.0"
        assert len(planning.attendees) == 0

    def test_add_attendees_and_goals(self):
        """Testar adicionar attendees e goals."""
        planning = SprintPlanningSession(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        planning.add_attendee("Jader")
        planning.add_goal("Implementar Bootstrap Gate")

        assert len(planning.attendees) == 1
        assert len(planning.goals) == 1

    def test_total_estimated_days(self):
        """Testar cálculo de dias estimados."""
        planning = SprintPlanningSession(
            sprint_id="sprint-0.0",
            date="2026-07-22",
        )

        planning.add_planned_task("T0.0.1", "Bootstrap", 2.0)
        planning.add_planned_task("T0.0.A", "JTBD", 2.0)

        assert planning.total_estimated_days() == 4.0


class TestRetrospective:
    """Testes para Retrospective."""

    def test_create_retro(self):
        """Testar criar retrospective."""
        retro = Retrospective(
            sprint_id="sprint-0.0",
            date="2026-07-26",
        )

        assert retro.sprint_id == "sprint-0.0"
        assert len(retro.action_items) == 0

    def test_add_items(self):
        """Testar adicionar itens."""
        retro = Retrospective(
            sprint_id="sprint-0.0",
            date="2026-07-26",
        )

        retro.add_well("Velocidade excepcional")
        retro.add_wrong("Agendamento lento")
        retro.add_improvement("Iniciar mais cedo")

        assert len(retro.what_went_well) == 1
        assert len(retro.what_went_wrong) == 1
        assert len(retro.improvement_ideas) == 1

    def test_add_actions(self):
        """Testar adicionar ações."""
        retro = Retrospective(
            sprint_id="sprint-0.0",
            date="2026-07-26",
        )

        action = RetroAction(
            category="improvements",
            description="Criar template de recrutamento",
            owner="Jader",
            priority="high",
        )

        retro.add_action(action)
        assert len(retro.action_items) == 1
        assert len(retro.get_high_priority_actions()) == 1


class TestRoadmapCeremony:
    """Testes para Roadmap Ceremony."""

    def test_create_roadmap(self):
        """Testar criar roadmap ceremony."""
        roadmap = RoadmapCeremony(
            product_id="meu-pdi",
            date="2026-07-23",
            north_star="Tornar cada profissional capaz de evoluir continuamente",
            north_star_metric="Taxa de conclusao de ciclos de desenvolvimento",
        )

        assert roadmap.product_id == "meu-pdi"
        assert len(roadmap.phases) == 0

    def test_add_attendee(self):
        """Testar adicionar participante (sem duplicar)."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")

        roadmap.add_attendee("Jader")
        roadmap.add_attendee("Jader")

        assert roadmap.attendees == ["Jader"]

    def test_add_phase_returns_phase_for_chaining(self):
        """Testar que add_phase retorna a fase para adicionar itens."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")

        phase = roadmap.add_phase("Fundacao", "2026 Q2-Q3", goal="Estabelecer a base do produto")
        phase.add_item("P0", "CAP-IDENTITY", "Auth multi-role")
        phase.add_item("P0", "CAP-PLANS", "PDI manual + IA")

        assert len(roadmap.phases) == 1
        assert roadmap.phases[0].name == "Fundacao"
        assert len(roadmap.phases[0].priority_items) == 2

    def test_add_dependency(self):
        """Testar registrar dependencia entre itens."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")

        roadmap.add_dependency("CAP-GOALS", "CAP-CAREER")

        assert len(roadmap.dependency_matrix) == 1
        assert roadmap.dependency_matrix[0] == {"item": "CAP-GOALS", "depends_on": "CAP-CAREER"}

    def test_total_items(self):
        """Testar contagem total de itens priorizados em todas as fases."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")

        p1 = roadmap.add_phase("Fundacao", "2026 Q2-Q3")
        p1.add_item("P0", "CAP-IDENTITY", "Auth")
        p2 = roadmap.add_phase("Core Produto", "2026 Q3-Q4")
        p2.add_item("P0", "CAP-GOALS", "Metas")
        p2.add_item("P1", "CAP-COACH", "Check-ins")

        assert roadmap.total_items() == 3

    def test_render_markdown_includes_key_sections(self):
        """Testar que o markdown renderizado contem as secoes oficiais."""
        roadmap = RoadmapCeremony(
            product_id="meu-pdi",
            date="2026-07-23",
            north_star="Evoluir continuamente",
            north_star_metric="Ciclos concluidos",
        )
        phase = roadmap.add_phase("Fundacao", "2026 Q2-Q3", goal="Base do produto")
        phase.add_item("P0", "CAP-IDENTITY", "Auth")
        roadmap.add_dependency("CAP-GOALS", "CAP-CAREER")

        md = roadmap.render_markdown()

        assert "# Roadmap — meu-pdi" in md
        assert "North Star" in md
        assert "Evoluir continuamente" in md
        assert "Fundacao (2026 Q2-Q3)" in md
        assert "CAP-IDENTITY" in md
        assert "CAP-GOALS` depende de `CAP-CAREER`" in md

    def test_render_markdown_placeholders_when_empty(self):
        """Testar que secoes vazias geram placeholders, nao quebram."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")

        md = roadmap.render_markdown()

        assert "_[Definir North Star do produto]_" in md
        assert "_[Definir fases do roadmap]_" in md
        assert "_[Mapear dependências entre itens do roadmap]_" in md

    def test_to_dict(self):
        """Testar serializacao."""
        roadmap = RoadmapCeremony(product_id="meu-pdi", date="2026-07-23")
        phase = roadmap.add_phase("Fundacao", "2026 Q2-Q3")
        phase.add_item("P0", "CAP-IDENTITY", "Auth")

        d = roadmap.to_dict()

        assert d["product_id"] == "meu-pdi"
        assert d["num_phases"] == 1
        assert d["total_items"] == 1
