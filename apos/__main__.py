"""CLI entry point for APOS initialization and management."""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print_help()
        return 1

    command = sys.argv[1]

    if command == "init":
        from apos.bootstrap.gate import BootstrapGate

        gate = BootstrapGate(project_root=Path.cwd())
        gate.run()
        return 0
    elif command == "daily":
        return handle_daily_command(sys.argv[2:])
    elif command in ("init-sprint", "init_sprint"):
        return handle_init_sprint_command(sys.argv[2:])
    elif command == "validate-sprint":
        return handle_validate_sprint_command(sys.argv[2:])
    elif command == "--version":
        from apos import __version__

        print(f"APOS {__version__}")
        return 0
    elif command == "context":
        from apos.cli import main as cli_main

        return cli_main(sys.argv[1:])
    elif command == "validate":
        return handle_validate_command(sys.argv[2:])
    elif command in ("--help", "-h"):
        print_help()
        return 0
    else:
        print(f"Unknown command: {command}")
        print_help()
        return 1


def handle_daily_command(args):
    """Manipular subcomando 'daily'.

    python -m apos daily --sprint sprint-0.0 --date 2026-07-22 --mode automatic --tasks-json tasks.json
    python -m apos daily --sprint sprint-0.0 --tasks-json tasks.json
      (sem --mode: pergunta interativamente)
    python -m apos daily --sprint sprint-0.0
      (sem --tasks-json: reconstrói a partir de
       docs/releases/{release}/{sprint}/TASKS.md via Sprint.load_from_markdown())
    """
    parser = argparse.ArgumentParser(
        prog="python -m apos daily",
        description="Executar Daily Standup de um sprint",
    )
    parser.add_argument(
        "--sprint",
        required=True,
        help="ID do sprint (ex: sprint-0.0)",
    )
    parser.add_argument(
        "--date",
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Data da daily (YYYY-MM-DD, default: hoje)",
    )
    parser.add_argument(
        "--mode",
        choices=["automatic", "collaborative"],
        default=None,
        help="Modo de execução (automatic/collaborative, default: pergunta ao usuário)",
    )
    parser.add_argument(
        "--release",
        default="R0",
        help="ID da release (default: R0; usado para inferir diretório de saída)",
    )
    parser.add_argument(
        "--tasks-json",
        required=False,
        default=None,
        help=(
            "Caminho para arquivo JSON com lista de tasks do sprint. "
            "Se omitido, tenta reconstruir a partir de "
            "docs/releases/{release}/{sprint}/TASKS.md"
        ),
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1

    from apos.release_management.sprint import Sprint, Task, TaskStatus

    if parsed_args.tasks_json:
        # Caminho via --tasks-json (explícito)
        tasks_json_path = Path(parsed_args.tasks_json)
        if not tasks_json_path.exists():
            print(f"Erro: arquivo '{tasks_json_path}' não existe")
            return 1

        try:
            with open(tasks_json_path, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Erro ao parsear JSON: {e}")
            return 1

        if not isinstance(tasks_data, list):
            print("Erro: JSON deve conter uma lista de tasks")
            return 1

        sprint = Sprint(
            id=parsed_args.sprint,
            release_id=parsed_args.release,
            title=parsed_args.sprint,
            start_date=parsed_args.date,
            end_date=parsed_args.date,
        )

        # Validar e carregar tasks
        try:
            for task_dict in tasks_data:
                # Validar status enum
                status_value = task_dict.get("status", "planned").lower()
                try:
                    status = TaskStatus(status_value)
                except ValueError:
                    print(f"Erro: status inválido '{status_value}' na task '{task_dict.get('id')}'")
                    print(f"Status válidos: {', '.join(s.value for s in TaskStatus)}")
                    return 1

                task = Task(
                    id=task_dict.get("id", ""),
                    title=task_dict.get("title", ""),
                    description=task_dict.get("description", ""),
                    days_estimate=float(task_dict.get("days_estimate", 1.0)),
                    status=status,
                    assignee=task_dict.get("assignee"),
                    depends_on=task_dict.get("depends_on", []),
                    notes=task_dict.get("notes", ""),
                )
                sprint.add_task(task)
        except (KeyError, TypeError, ValueError) as e:
            print(f"Erro ao processar task do JSON: {e}")
            return 1
    else:
        # Caminho via reconstrução automática a partir de TASKS.md
        tasks_md_path = (
            Path.cwd() / "docs" / "releases" / parsed_args.release / parsed_args.sprint / "TASKS.md"
        )

        if not tasks_md_path.exists():
            print(
                f"Erro: nenhuma fonte de tasks disponível.\n"
                f"  Opção 1: forneça --tasks-json apontando para um arquivo JSON de tasks\n"
                f"  Opção 2: crie '{tasks_md_path}' com tasks preenchidas "
                f"(formato gerado por ReleaseTemplateGenerator.generate_sprint_tasks_template)"
            )
            return 1

        try:
            sprint = Sprint.load_from_markdown(
                sprint_id=parsed_args.sprint,
                release_id=parsed_args.release,
                tasks_md_path=tasks_md_path,
                title=parsed_args.sprint,
                start_date=parsed_args.date,
                end_date=parsed_args.date,
            )
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return 1

    if not sprint.tasks:
        print("Aviso: nenhuma task encontrada")

    # Determinar modo (interativo se não fornecido)
    from apos.release_management.daily_runner import DailyMode

    mode = None
    if parsed_args.mode:
        mode = DailyMode(parsed_args.mode)
    else:
        # Perguntar interativamente
        print("\nEscolha o modo da daily:")
        print("  A) Automático (infere tudo sozinho)")
        print("  B) Colaborativo (analisa e pede sua confirmação)")
        choice = input("> ").strip().lower()

        if choice in ("a", "automatic"):
            mode = DailyMode.AUTOMATIC
        elif choice in ("b", "collaborative"):
            mode = DailyMode.COLLABORATIVE
        else:
            print("Escolha inválida. Use 'A' ou 'B'")
            return 1

    # Executar Daily Standup
    from apos.release_management.daily_runner import DailyStandupRunner

    runner = DailyStandupRunner(
        sprint=sprint,
        date=parsed_args.date,
        mode=mode,
    )

    runner.run()

    # Salvar em arquivo
    sprint_dir = Path.cwd() / "docs" / "releases" / parsed_args.release / parsed_args.sprint
    sprint_dir.mkdir(parents=True, exist_ok=True)

    try:
        runner.save_to_file(sprint_dir)
        return 0
    except Exception as e:
        print(f"Erro ao salvar daily: {e}")
        return 1


def handle_init_sprint_command(args):
    """Handle 'init-sprint' command — create sprint directory with standard structure.

    python -m apos init-sprint --sprint sprint-0.2 --release R0
    python -m apos init-sprint --sprint sprint-0.2 --release R0 --dry-run
    """
    parser = argparse.ArgumentParser(
        prog="python -m apos init-sprint",
        description="Criar diretório de sprint com estrutura padrão (BOARD, USER_STORIES, RETRO, etc)",
    )
    parser.add_argument(
        "--sprint",
        required=True,
        help="ID do sprint (ex: sprint-0.2)",
    )
    parser.add_argument(
        "--release",
        default="R0",
        help="ID da release (default: R0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Apenas mostrar quais arquivos seriam criados, sem criar",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1

    from apos.release_management.sprint import Sprint, SprintManager

    sm = SprintManager(release_id=parsed_args.release)
    sm.create_sprint(
        sprint_id=parsed_args.sprint,
        title=parsed_args.sprint,
        start_date=datetime.now().strftime("%Y-%m-%d"),
        end_date="",
    )

    if parsed_args.dry_run:
        sprint_dir = sm.release_dir / parsed_args.sprint
        print(f"Dry-run: os seguintes arquivos seriam criados em {sprint_dir}/")
        print("  - README.md")
        print("  - TASKS.md")
        print("  - USER_STORIES.md")
        print("  - BOARD.md")
        print("  - STATUS.md")
        print("  - RISK_MITIGATION.md")
        print("  - RETRO.md")
        print(f"  - DAILY_STANDUP_{datetime.now().strftime('%Y-%m-%d')}.md")
        print("  (Nenhum arquivo foi criado — use --dry-run para confirmar)")
        return 0

    sprint_dir = sm.initialize_sprint_directory(parsed_args.sprint)
    print(f"✅ Sprint {parsed_args.sprint} inicializado em {sprint_dir}/")
    print("  ├── README.md")
    print("  ├── TASKS.md")
    print("  ├── USER_STORIES.md")
    print("  ├── BOARD.md")
    print("  ├── STATUS.md")
    print("  ├── RISK_MITIGATION.md")
    print("  ├── RETRO.md")
    print(f"  └── DAILY_STANDUP_{datetime.now().strftime('%Y-%m-%d')}.md")
    print("")
    print("Estrutura de sprint gerada com templates padrao (espelhando Sprint 0.0).")
    print("Preencha TASKS.md e execute:")
    print(f"  python -m apos daily --sprint {parsed_args.sprint} --release {parsed_args.release}")
    return 0


def _create_status_file(sprint_root: Path) -> Path:
    """Auto-cria STATUS.md a partir do template padrao quando ausente."""
    from datetime import datetime

    status_file = sprint_root / "STATUS.md"
    sprint_id = sprint_root.name

    content = f"""# {sprint_id} — Relatorio de Status

**Ultima Atualizacao:** {datetime.now().isoformat()}

---

## 📊 Status Geral

**Fase Atual:** Active
**Total de Tasks:** 0
**Concluidas:** 0
**Em Andamento:** 0

---

## 📌 Commit Tracking (Audit Trail)

*Arquivo auto-gerado por `apos validate-sprint --create-status`.*

| Commit | Descricao | Task |
|--------|-----------|------|
| `[hash]` | | |

---

**Template gerado por APOS SprintQualityGate**
"""
    status_file.write_text(content, encoding="utf-8")
    print(f"📄 STATUS.md criado automaticamente em {status_file}")
    return status_file


def handle_validate_sprint_command(args):
    """Handle 'validate-sprint' command for commit tracking validation.

    python -m apos validate-sprint --sprint-root docs/releases/R0/sprint-0.0/
    python -m apos validate-sprint --sprint-root docs/releases/R0/sprint-0.0/ --strict
    """
    parser = argparse.ArgumentParser(
        prog="python -m apos validate-sprint",
        description="Validar rastreamento de commits em um sprint",
    )
    parser.add_argument(
        "--sprint-root",
        required=True,
        help="Diretório raiz do sprint (ex: docs/releases/R0/sprint-0.0/)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Modo restrito: FAIL se score < 1.0 (deve ter 100% de rastreamento)",
    )
    parser.add_argument(
        "--create-status",
        action="store_true",
        help="Auto-criar STATUS.md se ausente, usando template padrao",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1

    from apos.kernel import CommitTrackingValidator

    sprint_root = Path(parsed_args.sprint_root)
    if not sprint_root.exists():
        print(f"Erro: diretório '{sprint_root}' não existe")
        return 1

    validator = CommitTrackingValidator(str(sprint_root))
    result = validator.validate()

    # Auto-create STATUS.md if missing
    status_file = sprint_root / "STATUS.md"
    if not status_file.exists() and parsed_args.create_status:
        _create_status_file(sprint_root)
        # Re-validate after creating STATUS.md
        result = validator.validate()

    # Print results
    print("\nValidando Rastreamento de Commits")
    print("=" * 60)

    # Print per-artifact validation
    for artifact, valid in result.validation_details.items():
        status = "✅" if valid else "❌"
        print(f"{status} {artifact}")

    # Print summary
    print("\n" + "=" * 60)
    print(f"Score: {result.score:.2f} ({result.status})")
    print(f"Commits rastreados: {len(result.tracked_commits)}")

    if result.issues:
        print("\nProblemas encontrados:")
        for issue in result.issues:
            print(f"  • {issue}")

    if result.untracked_tasks:
        print("\nTarefas sem rastreamento:")
        for task in result.untracked_tasks:
            print(f"  • {task}")

    print()

    # Determine exit code
    if parsed_args.strict:
        # Strict mode: require perfect score
        if result.score >= 1.0:
            print("✅ Commit tracking 100% completo (strict mode)")
            return 0
        else:
            print(f"❌ Commit tracking incompleto (strict mode): {result.score:.0%}")
            return 1
    else:
        # Normal mode: pass if score >= 0.80
        if result.passes():
            print("✅ Commit tracking válido")
            return 0
        else:
            print(f"❌ Commit tracking insuficiente: {result.score:.0%} (requerido: 80%)")
            return 1


def handle_validate_command(args):
    """Handle 'validate' command — compara codigo vs documentacao SDD.

    python -m apos validate [--root PATH] [--format markdown|json]
    """
    parser = argparse.ArgumentParser(
        prog="python -m apos validate",
        description="Validar consistencia entre codigo e documentacao SDD",
    )
    parser.add_argument(
        "--root",
        default=str(Path.cwd()),
        help="Raiz do projeto (default: diretorio atual)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Formato do relatorio (default: markdown)",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1

    root = Path(parsed_args.root)
    if not root.exists():
        print(f"Erro: diretorio '{root}' nao existe")
        return 1

    from apos.validate import ProjectValidator

    validator = ProjectValidator(root)
    report = validator.validate()

    if parsed_args.format == "json":
        import json as json_mod

        print(json_mod.dumps(report.to_dict(), indent=2, ensure_ascii=False))
    else:
        print(report.to_markdown())
        print()

    if report.divergent or report.absent_code or report.absent_doc:
        return 1
    return 0


def print_help():
    from apos import __version__

    print(f"""
APOS {__version__} — A Precise Ontology System for AI agents

Usage:
    python -m apos COMMAND [OPTIONS]

Commands:
    init              Initialize APOS project (validate foundations, bootstrap if needed)
    init-sprint       Create sprint directory with standard structure (BOARD, USER_STORIES, RETRO, etc)
    daily             Execute Daily Standup for a sprint
                      Use: python -m apos daily --sprint SPRINT_ID [--tasks-json FILE] [--mode MODE] [--date DATE] [--release RELEASE]
                      --tasks-json is optional: if omitted, tasks are reconstructed
                      from docs/releases/{{release}}/{{sprint}}/TASKS.md
    validate-sprint   Validate commit tracking in sprint artifacts
                      Use: python -m apos validate-sprint --sprint-root SPRINT_DIR [--strict]
                      Checks: TASKS.md, BOARD.md, STATUS.md, USER_STORIES.md, RETRO.md
    context           Exibe o ProjectProfile como markdown formatado
                      Use: python -m apos context
    validate          Compara codigo vs documentacao SDD
                      Use: python -m apos validate [--root PATH] [--format markdown|json]
    --version         Show version
    --help            Show this help message
""".strip())


if __name__ == "__main__":
    sys.exit(main())
