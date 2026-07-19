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
    elif command == "--version":
        from apos import __version__

        print(f"APOS {__version__}")
        return 0
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
        required=True,
        help="Caminho para arquivo JSON com lista de tasks do sprint",
    )

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit:
        return 1

    # Validar arquivo JSON
    # TODO: hoje não existe um método para reconstruir um Sprint a partir de
    # TASKS.md/BOARD.md já gravados em disco. --tasks-json é uma solução
    # temporária. Quando essa funcionalidade existir (ex: um método
    # Sprint.load_from_markdown() ou similar), este comando deve passar a usá-la
    # como default, tornando --tasks-json opcional/legado.
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

    # Instanciar Sprint e Tasks a partir do JSON
    from apos.release_management.sprint import Sprint, Task, TaskStatus

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

    if not sprint.tasks:
        print("Aviso: nenhuma task encontrada no JSON")

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


def print_help():
    from apos import __version__

    print(f"""
APOS {__version__} — A Precise Ontology System for AI agents

Usage:
    python -m apos COMMAND [OPTIONS]

Commands:
    init              Initialize APOS project (validate foundations, bootstrap if needed)
    daily             Execute Daily Standup for a sprint
                      Use: python -m apos daily --sprint SPRINT_ID --tasks-json FILE [--mode MODE] [--date DATE] [--release RELEASE]
    --version         Show version
    --help            Show this help message
""".strip())


if __name__ == "__main__":
    sys.exit(main())
