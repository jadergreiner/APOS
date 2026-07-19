"""Testes para CLI de APOS."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from apos.__main__ import handle_daily_command
from apos.release_management.daily_runner import DailyMode


@pytest.fixture
def sample_tasks_json(tmp_path):
    """Fixture com arquivo JSON de tasks de amostra."""
    tasks = [
        {
            "id": "T0.0.1",
            "title": "Bootstrap Gate",
            "description": "Implementar Bootstrap Gate",
            "days_estimate": 2.0,
            "status": "in_progress",
            "assignee": "Jader",
            "depends_on": [],
            "notes": "",
        },
        {
            "id": "T0.0.2",
            "title": "Auto-ID APOS",
            "description": "Implementar auto-identificação",
            "days_estimate": 1.0,
            "status": "planned",
            "assignee": "Jader",
            "depends_on": ["T0.0.1"],
            "notes": "",
        },
    ]
    tasks_file = tmp_path / "tasks.json"
    with open(tasks_file, "w", encoding="utf-8") as f:
        json.dump(tasks, f)
    return tasks_file


@pytest.fixture
def sample_output_dir(tmp_path):
    """Fixture para diretório de saída."""
    return tmp_path


class TestDailyCommandArgumentParsing:
    """Testes de parsing de argumentos do comando daily."""

    def test_daily_command_requires_sprint_and_tasks_json(self, tmp_path):
        """Comando daily deve exigir --sprint e --tasks-json."""
        # Sem argumentos
        result = handle_daily_command([])
        assert result == 1

        # Sem --tasks-json
        result = handle_daily_command(["--sprint", "sprint-0.0"])
        assert result == 1

    def test_daily_command_rejects_invalid_tasks_json_path(self, tmp_path):
        """Comando deve rejeitar arquivo JSON que não existe."""
        result = handle_daily_command(
            [
                "--sprint",
                "sprint-0.0",
                "--tasks-json",
                "/nonexistent/path/tasks.json",
            ]
        )
        assert result == 1

    def test_daily_command_rejects_invalid_json_format(self, tmp_path):
        """Comando deve rejeitar JSON malformado."""
        bad_json_file = tmp_path / "bad.json"
        bad_json_file.write_text("{ invalid json", encoding="utf-8")

        result = handle_daily_command(
            ["--sprint", "sprint-0.0", "--tasks-json", str(bad_json_file)]
        )
        assert result == 1

    def test_daily_command_rejects_json_not_list(self, tmp_path):
        """Comando deve rejeitar JSON que não é lista de tasks."""
        bad_json_file = tmp_path / "bad.json"
        bad_json_file.write_text('{"not": "a list"}', encoding="utf-8")

        result = handle_daily_command(
            ["--sprint", "sprint-0.0", "--tasks-json", str(bad_json_file)]
        )
        assert result == 1


class TestDailyCommandTaskProcessing:
    """Testes de processamento de tasks do JSON."""

    def test_daily_command_rejects_invalid_task_status_in_json(self, tmp_path, sample_output_dir):
        """Comando deve rejeitar status de task inválido."""
        tasks = [
            {
                "id": "T0.0.1",
                "title": "Task",
                "description": "Desc",
                "days_estimate": 1.0,
                "status": "invalid_status",
                "assignee": "User",
                "depends_on": [],
                "notes": "",
            }
        ]
        tasks_file = tmp_path / "tasks.json"
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f)

        result = handle_daily_command(["--sprint", "sprint-0.0", "--tasks-json", str(tasks_file)])
        assert result == 1

    def test_daily_command_accepts_valid_task_statuses(self, tmp_path, sample_output_dir):
        """Comando deve aceitar todos os TaskStatus válidos."""
        valid_statuses = ["backlog", "planned", "in_progress", "in_review", "complete", "blocked"]

        for status in valid_statuses:
            tasks = [
                {
                    "id": "T0.0.1",
                    "title": "Task",
                    "description": "Desc",
                    "days_estimate": 1.0,
                    "status": status,
                    "assignee": "User",
                    "depends_on": [],
                    "notes": "",
                }
            ]
            tasks_file = tmp_path / f"tasks_{status}.json"
            with open(tasks_file, "w", encoding="utf-8") as f:
                json.dump(tasks, f)

            with (
                patch(
                    "apos.release_management.daily_runner.DailyStandupRunner"
                ) as mock_runner_class,
                patch("builtins.input", return_value="a"),
            ):  # Modo automático
                mock_runner = MagicMock()
                mock_runner_class.return_value = mock_runner
                mock_runner.save_to_file.return_value = Path("file.md")

                result = handle_daily_command(
                    [
                        "--sprint",
                        "sprint-0.0",
                        "--tasks-json",
                        str(tasks_file),
                    ]
                )
                assert result == 0, f"Failed for status: {status}"


class TestDailyCommandModeSelection:
    """Testes de seleção de modo (automático/colaborativo)."""

    def test_daily_command_accepts_mode_automatic(self, sample_tasks_json, tmp_path):
        """Comando deve aceitar --mode automatic."""
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "automatic",
                ]
            )
            assert result == 0
            # Verificar que DailyStandupRunner foi instanciado com modo AUTOMATIC
            mock_runner_class.assert_called_once()
            call_kwargs = mock_runner_class.call_args.kwargs
            assert call_kwargs["mode"] == DailyMode.AUTOMATIC

    def test_daily_command_accepts_mode_collaborative(self, sample_tasks_json, tmp_path):
        """Comando deve aceitar --mode collaborative."""
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "collaborative",
                ]
            )
            assert result == 0
            # Verificar que DailyStandupRunner foi instanciado com modo COLLABORATIVE
            mock_runner_class.assert_called_once()
            call_kwargs = mock_runner_class.call_args.kwargs
            assert call_kwargs["mode"] == DailyMode.COLLABORATIVE

    def test_daily_command_prompts_when_mode_missing(self, sample_tasks_json, tmp_path):
        """Comando deve perguntar modo ao usuário se --mode não for fornecido."""
        with (
            patch("builtins.input", return_value="a") as mock_input,
            patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class,
        ):
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                ]
            )
            assert result == 0
            # Verificar que input foi chamado
            mock_input.assert_called()
            # Verificar que modo foi definido como AUTOMATIC (resposta 'a')
            call_kwargs = mock_runner_class.call_args.kwargs
            assert call_kwargs["mode"] == DailyMode.AUTOMATIC

    def test_daily_command_prompts_accepts_b_for_collaborative(self, sample_tasks_json, tmp_path):
        """Comando deve aceitar 'B' na prompt para modo colaborativo."""
        with (
            patch("builtins.input", return_value="b"),
            patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class,
        ):
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                ]
            )
            assert result == 0
            call_kwargs = mock_runner_class.call_args.kwargs
            assert call_kwargs["mode"] == DailyMode.COLLABORATIVE

    def test_daily_command_prompts_rejects_invalid_mode_choice(self, sample_tasks_json, tmp_path):
        """Comando deve rejeitar escolha de modo inválida."""
        with patch("builtins.input", return_value="X"):
            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                ]
            )
            assert result == 1


class TestDailyCommandDateHandling:
    """Testes de processamento de data."""

    def test_daily_command_uses_provided_date(self, sample_tasks_json, tmp_path):
        """Comando deve usar --date fornecido."""
        test_date = "2026-07-22"
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--date",
                    test_date,
                    "--mode",
                    "automatic",
                ]
            )
            assert result == 0
            call_kwargs = mock_runner_class.call_args.kwargs
            assert call_kwargs["date"] == test_date

    def test_daily_command_defaults_to_today(self, sample_tasks_json, tmp_path):
        """Comando deve usar data de hoje como default."""
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "automatic",
                ]
            )
            assert result == 0
            call_kwargs = mock_runner_class.call_args.kwargs
            # Verificar que date está no formato ISO
            date_str = call_kwargs["date"]
            assert len(date_str) == 10  # YYYY-MM-DD
            assert date_str.count("-") == 2


class TestDailyCommandOutputDirectory:
    """Testes de criação de diretório de saída."""

    def test_daily_command_creates_output_directory(self, sample_tasks_json, tmp_path):
        """Comando deve criar diretório de saída."""
        output_base = tmp_path / "output"

        with (
            patch("apos.__main__.Path.cwd", return_value=output_base),
            patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class,
        ):
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = (
                output_base
                / "docs"
                / "releases"
                / "R0"
                / "sprint-0.0"
                / "DAILY_STANDUP_2026-07-22.md"
            )

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "automatic",
                    "--release",
                    "R0",
                    "--date",
                    "2026-07-22",
                ]
            )
            assert result == 0

    def test_daily_command_uses_release_argument(self, sample_tasks_json, tmp_path):
        """Comando deve usar --release para derivar diretório."""
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-1.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "automatic",
                    "--release",
                    "R1",
                ]
            )
            assert result == 0
            # Verificar que save_to_file foi chamado com caminho contendo R1
            call_args = mock_runner.save_to_file.call_args
            sprint_dir = call_args[0][0]
            assert "R1" in str(sprint_dir)


class TestDailyCommandIntegration:
    """Testes de integração do comando daily."""

    def test_daily_command_full_flow_automatic_mode(self, sample_tasks_json, tmp_path):
        """Teste fluxo completo: parsing → runner → save."""
        with patch("apos.release_management.daily_runner.DailyStandupRunner") as mock_runner_class:
            mock_runner = MagicMock()
            mock_runner_class.return_value = mock_runner
            mock_runner.save_to_file.return_value = Path("saved_file.md")

            result = handle_daily_command(
                [
                    "--sprint",
                    "sprint-0.0",
                    "--tasks-json",
                    str(sample_tasks_json),
                    "--mode",
                    "automatic",
                    "--date",
                    "2026-07-22",
                ]
            )

            assert result == 0
            mock_runner_class.assert_called_once()
            mock_runner.run.assert_called_once()
            mock_runner.save_to_file.assert_called_once()
