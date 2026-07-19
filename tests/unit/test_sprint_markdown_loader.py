"""Testes para Sprint.load_from_markdown()."""

import pytest

from apos.release_management.sprint import Sprint, TaskStatus


class TestLoadFromMarkdown:
    """Testes de reconstrução de Sprint a partir de TASKS.md."""

    def test_load_from_markdown_parses_single_tier(self, tmp_path):
        """Deve parsear tasks de uma única tabela (Tier 1)."""
        content = """# Sprint Tasks

**Status:** Planning

---

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.1 | Bootstrap Gate | Implementar validador | 2d | in_progress | Jader |
| T0.0.2 | Auto-ID APOS | Implementar CLI | 1d | planned | Jader |

---
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert sprint.id == "sprint-0.0"
        assert sprint.release_id == "R0"
        assert len(sprint.tasks) == 2

        task1 = sprint.get_task("T0.0.1")
        assert task1 is not None
        assert task1.title == "Bootstrap Gate"
        assert task1.description == "Implementar validador"
        assert task1.days_estimate == 2.0
        assert task1.status == TaskStatus.IN_PROGRESS
        assert task1.assignee == "Jader"

        task2 = sprint.get_task("T0.0.2")
        assert task2 is not None
        assert task2.status == TaskStatus.PLANNED

    def test_load_from_markdown_parses_multiple_tiers(self, tmp_path):
        """Deve parsear tasks de múltiplas tabelas (Tier 1, 2, 3)."""
        content = """# Sprint Tasks

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.1 | Bootstrap Gate | Desc 1 | 2d | complete | Jader |

### Tier 2: Important (Should Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.2 | JTBD Interviews | Desc 2 | 2d | blocked | Maria |

### Tier 3: Nice-to-Have (Could Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.3 | Polish Docs | Desc 3 | 1d | backlog | |

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de Tarefas | 3 |
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert len(sprint.tasks) == 3
        assert sprint.get_task("T0.0.1").status == TaskStatus.COMPLETE
        assert sprint.get_task("T0.0.2").status == TaskStatus.BLOCKED
        assert sprint.get_task("T0.0.2").assignee == "Maria"
        assert sprint.get_task("T0.0.3").status == TaskStatus.BACKLOG
        assert sprint.get_task("T0.0.3").assignee is None

    def test_load_from_markdown_skips_placeholder_rows(self, tmp_path):
        """Deve ignorar linhas de placeholder não preenchidas (template em branco)."""
        content = """# Sprint Tasks

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T | | | | planned | |

### Tier 2: Important (Should Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T | | | | planned | |
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert len(sprint.tasks) == 0

    def test_load_from_markdown_handles_unparseable_duration_gracefully(self, tmp_path):
        """Deve usar 0.0 e não levantar exceção se a duração não for parseável."""
        content = """# Sprint Tasks

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.1 | Task X | Desc | TBD | planned | Jader |
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert len(sprint.tasks) == 1
        task = sprint.get_task("T0.0.1")
        assert task.days_estimate == 0.0

    def test_load_from_markdown_handles_unknown_status_gracefully(self, tmp_path):
        """Deve usar TaskStatus.PLANNED e não levantar exceção para status desconhecido."""
        content = """# Sprint Tasks

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.1 | Task X | Desc | 1d | weird_status | Jader |
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert len(sprint.tasks) == 1
        task = sprint.get_task("T0.0.1")
        assert task.status == TaskStatus.PLANNED

    def test_load_from_markdown_missing_file_raises_clear_error(self, tmp_path):
        """Deve levantar FileNotFoundError com mensagem clara se o arquivo não existir."""
        missing_path = tmp_path / "nonexistent_TASKS.md"

        with pytest.raises(FileNotFoundError) as exc_info:
            Sprint.load_from_markdown(
                sprint_id="sprint-0.0",
                release_id="R0",
                tasks_md_path=missing_path,
            )

        assert str(missing_path) in str(exc_info.value)
