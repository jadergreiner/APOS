"""Exemplo de uso do Release Management Framework de APOS.

Demonstra como um projeto importa APOS e recebe automaticamente:
- Release Manager para gerenciar releases
- Sprint Manager para gerenciar sprints
- Cerimônias (Daily, Planning, Retro)
- Geração de templates
"""

from pathlib import Path
from apos.release_management import (
    ReleaseManager,
    SprintManager,
    DailyStandup,
    DailyStandupUpdate,
    SprintPlanningSession,
    Retrospective,
    RetroAction,
    ReleaseTemplateGenerator,
)
from apos.release_management.sprint import Task, TaskStatus, UserStory


def example_release_management():
    """Exemplo: Gerenciar uma release com APOS."""

    print("\n" + "=" * 60)
    print("EXEMPLO: Release Management com APOS")
    print("=" * 60)

    # 1. Criar gerenciador de releases
    rm = ReleaseManager(project_name="meu-projeto")

    # 2. Criar uma release
    r0 = rm.create_release(
        release_id="R0",
        title="Bootstrap + Platform Identity",
        description="Estabelecer fundações semânticas de APOS",
        start_date="2026-07-19",
        end_date="2026-08-02",
    )

    # 3. Adicionar objetivos à release
    from apos.release_management import ReleaseObjective

    obj1 = ReleaseObjective(
        id="R0-O1",
        title="Estabelecer Fundações Semânticas",
        description="Validar que APOS tem todos os 10 items obrigatórios",
        key_results=[
            "Bootstrap Gate implementado",
            "Todos docs estratégicos criados",
            "APOS usando a si mesmo",
        ],
    )
    r0.add_objective(obj1)

    # 4. Inicializar diretório de release
    release_dir = rm.initialize_release_directory("R0")
    print(f"\n✅ Release R0 inicializada em: {release_dir}")

    # 5. Criar gerenciador de sprints
    sm = SprintManager(release_id="R0")

    # 6. Criar sprints
    sprint_0_0 = sm.create_sprint(
        sprint_id="sprint-0.0",
        title="Scaffold + JTBD Validation",
        start_date="2026-07-22",
        end_date="2026-07-26",
    )

    sprint_0_1 = sm.create_sprint(
        sprint_id="sprint-0.1",
        title="Platform Identity",
        start_date="2026-07-29",
        end_date="2026-08-02",
    )

    # 7. Adicionar tarefas ao sprint
    task1 = Task(
        id="T0.0.1",
        title="Implementar Bootstrap Gate",
        description="Criar validador automático de fundações",
        days_estimate=2.0,
    )
    task2 = Task(
        id="T0.0.2",
        title="Conduzir Entrevistas JTBD",
        description="Validar que APOS resolve job real",
        days_estimate=2.0,
    )
    sprint_0_0.add_task(task1)
    sprint_0_0.add_task(task2)

    print(f"\n✅ Sprint 0.0 criado com {sprint_0_0.total_tasks()} tarefas")
    print(f"   Total de dias: {sprint_0_0.total_days_estimate()}")

    # 8. Adicionar user stories
    story1 = UserStory(
        id="US-0.0.1",
        title="Como PM, quero validar que contexto reduz retrabalho",
        story_points=2.0,
        acceptance_criteria=[
            "Entrevistas com 5+ personas completas",
            "Job statement validado",
        ],
    )
    sprint_0_0.add_user_story(story1)

    # 9. Inicializar diretório de sprint
    sprint_dir = sm.initialize_sprint_directory("sprint-0.0")
    print(f"\n✅ Sprint 0.0 inicializada em: {sprint_dir}")

    # 10. Demonstrar atualização de status
    sprint_0_0.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
    print(f"\n✅ Task T0.0.1 marcada como IN_PROGRESS")

    # 11. Exportar sumário
    summary = sm.export_summary()
    print(f"\n✅ Sumário de Sprints:")
    print(f"   Release: {summary['release_id']}")
    print(f"   Sprints: {summary['num_sprints']}")
    print(f"   Total de tarefas: {summary['total_tasks']}")
    print(f"   Taxa de conclusão: {summary['overall_completion_rate']:.0%}")

    return rm, sm, sprint_0_0


def example_ceremonies():
    """Exemplo: Conduzir cerimônias."""

    print("\n" + "=" * 60)
    print("EXEMPLO: Cerimônias (Daily, Planning, Retro)")
    print("=" * 60)

    # 1. Daily Standup
    daily = DailyStandup(
        sprint_id="sprint-0.0",
        date="2026-07-22",
    )

    update1 = DailyStandupUpdate(
        participant="Jader",
        date="2026-07-22",
        what_done="Scaffolding completo",
        what_today="Iniciar Bootstrap Gate",
        blockers="Nenhum",
    )
    daily.add_update(update1)

    update2 = DailyStandupUpdate(
        participant="Team",
        date="2026-07-22",
        what_done="Estrutura de sprint",
        what_today="JTBD interviews",
        blockers="Agendamento de personas",
    )
    daily.add_update(update2)

    print(f"\n✅ Daily Standup criado:")
    print(f"   Participantes: {daily.get_participant_count()}")
    print(f"   Bloqueadores: {daily.get_blockers()}")

    # 2. Sprint Planning
    planning = SprintPlanning(
        sprint_id="sprint-0.0",
        date="2026-07-22",
        duration_minutes=120,
    )

    planning.add_attendee("Jader")
    planning.add_attendee("PM")
    planning.add_attendee("Engineer")

    planning.add_goal("Implementar Bootstrap Gate")
    planning.add_goal("Validar job statement")

    planning.add_planned_task("T0.0.1", "Bootstrap Gate", 2.0)
    planning.add_planned_task("T0.0.A", "JTBD Interviews", 2.0)

    planning.velocity_target = 4.0

    print(f"\n✅ Sprint Planning criado:")
    print(f"   Attendees: {len(planning.attendees)}")
    print(f"   Goals: {len(planning.goals)}")
    print(f"   Tarefas planejadas: {len(planning.planned_tasks)}")
    print(f"   Velocity target: {planning.velocity_target} pts")
    print(f"   Total estimado: {planning.total_estimated_days()} dias")

    # 3. Retrospective
    retro = Retrospective(
        sprint_id="sprint-0.0",
        date="2026-07-26",
        velocity_achieved=4.0,
        completion_rate=1.0,
        overall_sentiment="positive",
    )

    retro.add_attendee("Jader")
    retro.add_attendee("Team")

    retro.add_well("Velocidade excepcional (5x alvo)")
    retro.add_well("Documentação clara")
    retro.add_wrong("Agendamento de entrevistas lento")

    retro.add_improvement("Iniciar recrutamento de personas mais cedo")
    retro.add_improvement("Usar mais templates automáticos")

    action = RetroAction(
        category="improvements",
        description="Criar template de recrutamento para próximas sprints",
        owner="Jader",
        priority="high",
    )
    retro.add_action(action)

    print(f"\n✅ Retrospective criado:")
    print(f"   Velocity: {retro.velocity_achieved} pts")
    print(f"   Completion: {retro.completion_rate:.0%}")
    print(f"   Pontos positivos: {len(retro.what_went_well)}")
    print(f"   Pontos negativos: {len(retro.what_went_wrong)}")
    print(f"   Ações de alta prioridade: {len(retro.get_high_priority_actions())}")

    return daily, planning, retro


def example_templates():
    """Exemplo: Gerar templates."""

    print("\n" + "=" * 60)
    print("EXEMPLO: Geração de Templates")
    print("=" * 60)

    # 1. Release README
    readme = ReleaseTemplateGenerator.generate_release_readme(
        release_id="R0",
        title="Bootstrap + Platform Identity",
        description="Estabelecer fundações semânticas de APOS",
        start_date="2026-07-19",
        end_date="2026-08-02",
    )
    print(f"\n✅ Release README gerado ({len(readme)} chars)")

    # 2. Sprint README
    sprint_readme = ReleaseTemplateGenerator.generate_sprint_readme(
        sprint_id="sprint-0.0",
        release_id="R0",
        title="Scaffold + JTBD",
        start_date="2026-07-22",
        end_date="2026-07-26",
    )
    print(f"✅ Sprint README gerado ({len(sprint_readme)} chars)")

    # 3. TASKS template
    tasks = ReleaseTemplateGenerator.generate_sprint_tasks_template()
    print(f"✅ TASKS.md template gerado ({len(tasks)} chars)")

    # 4. BOARD template
    board = ReleaseTemplateGenerator.generate_sprint_board_template()
    print(f"✅ BOARD.md template gerado ({len(board)} chars)")

    # 5. STATUS template
    status = ReleaseTemplateGenerator.generate_sprint_status_template("sprint-0.0")
    print(f"✅ STATUS.md template gerado ({len(status)} chars)")

    # 6. Daily Standup (múltiplos formatos)
    daily_md = ReleaseTemplateGenerator.generate_daily_standup_template(
        sprint_id="sprint-0.0", format_type="markdown"
    )
    print(f"✅ Daily Standup (Markdown) gerado ({len(daily_md)} chars)")

    daily_txt = ReleaseTemplateGenerator.generate_daily_standup_template(
        sprint_id="sprint-0.0", format_type="text"
    )
    print(f"✅ Daily Standup (Text) gerado ({len(daily_txt)} chars)")

    # 7. RETRO template
    retro = ReleaseTemplateGenerator.generate_retro_template()
    print(f"✅ RETRO.md template gerado ({len(retro)} chars)")

    print("\n💡 Formatos disponíveis para Daily Standup:")
    print("   1. Text (simples)")
    print("   2. Structured (detalhado)")
    print("   3. Kanban (visual)")
    print("   4. Structured (para líderes)")

    return {
        "release_readme": readme,
        "sprint_readme": sprint_readme,
        "tasks": tasks,
        "board": board,
        "status": status,
        "daily_md": daily_md,
        "daily_txt": daily_txt,
        "retro": retro,
    }


def main():
    """Executar todos os exemplos."""

    print("\n" + "=" * 60)
    print("APOS Release Management Framework — Exemplos")
    print("=" * 60)
    print("\nEste exemplo mostra como usar os componentes de Release Management")
    print("quando um projeto importa APOS.\n")

    # Exemplos
    rm, sm, sprint = example_release_management()
    daily, planning, retro = example_ceremonies()
    templates = example_templates()

    # Sumário final
    print("\n" + "=" * 60)
    print("SUMÁRIO")
    print("=" * 60)

    print("\n✅ Release Management Framework Embarcado em APOS:")
    print("\n1. Release Manager")
    print("   - Gerenciar múltiplas releases (R0-R4)")
    print("   - Auto-gerar estrutura de diretórios")
    print("   - Rastrear objetivos e dependências")

    print("\n2. Sprint Manager")
    print("   - Gerenciar sprints dentro de uma release")
    print("   - Adicionar tarefas e user stories")
    print("   - Rastrear progress e velocidade")

    print("\n3. Cerimônias Embarcadas")
    print("   - Daily Standup (com múltiplos formatos)")
    print("   - Sprint Planning")
    print("   - Retrospective")

    print("\n4. Templates Auto-Gerados")
    print("   - Release README")
    print("   - Sprint README")
    print("   - TASKS, BOARD, STATUS, RETRO")
    print("   - Daily Standup (4 formatos)")

    print("\n🚀 Quando um projeto importa APOS:")
    print("   1. Bootstrap Gate valida 10 fundações")
    print("   2. Auto-gera R0 com estrutura completa")
    print("   3. Recebe Release Management embarcado")
    print("   4. Pode começar planning com templates prontos")

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
