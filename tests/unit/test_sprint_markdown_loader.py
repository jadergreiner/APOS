"""Testes para Sprint.load_from_markdown()."""

from pathlib import Path

import pytest

from apos.release_management.sprint import Sprint, TaskStatus

REPO_ROOT = Path(__file__).resolve().parents[2]


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


class TestNarrativeFormat:
    """Testes de reconstrução a partir do formato narrativo ("## {ID}: {Título}")."""

    def test_load_from_markdown_narrative_format_single_task(self, tmp_path):
        """Deve parsear uma única seção narrativa com todos os campos."""
        content = """# Sprint Tasks

## T0.0.1: Implementar Framework de Gerenciamento de Release (1 dia-pessoa)

**Objetivo:** Criar artefatos de Gerenciamento de Release que todo projeto que importa APOS recebe

**Tarefas:**
- [ ] Criar `docs/releases/R0/SPRINT_PLAN.md`
- [ ] Criar `docs/releases/R0/BACKLOG.md`

**Entregável:** `Framework de Gerenciamento de Release (templates + docs)`

**Responsável:** PM / Skill de Gerenciamento de Release
**Esforço:** 1 dia
**Status:** COMPLETO (Em R0/APOS, este framework já foi criado)

---
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
        assert task is not None
        assert task.title == "Implementar Framework de Gerenciamento de Release"
        assert "Criar artefatos de Gerenciamento de Release" in task.description
        assert task.days_estimate == 1.0
        assert task.status == TaskStatus.COMPLETE
        assert task.assignee == "PM / Skill de Gerenciamento de Release"

    def test_load_from_markdown_narrative_format_multiple_tasks(self, tmp_path):
        """Deve parsear múltiplas seções narrativas sequenciais."""
        content = """# Sprint Tasks

## T0.0.1: Primeira Tarefa

**Objetivo:** Fazer a primeira coisa

**Responsável:** Jader
**Esforço:** 1 dia
**Status:** COMPLETO

---

## T0.0.2: Segunda Tarefa

**Objetivo:** Fazer a segunda coisa

**Responsável:** Maria
**Esforço:** 2 dias
**Status:** EM ANDAMENTO

---

## T0.0.A: Terceira Tarefa (ID alfanumérico)

**Objetivo:** Fazer a terceira coisa

**Responsável:** Jader
**Esforço:** 1 dia
**Status:** Planejado
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
        assert sprint.get_task("T0.0.2").status == TaskStatus.IN_PROGRESS
        assert sprint.get_task("T0.0.2").assignee == "Maria"
        assert sprint.get_task("T0.0.A").status == TaskStatus.PLANNED
        assert sprint.get_task("T0.0.A").title == "Terceira Tarefa"

    @pytest.mark.parametrize(
        "status_text,expected_status",
        [
            ("NÃO INICIADO", TaskStatus.PLANNED),
            ("PLANEJADO", TaskStatus.PLANNED),
            ("DEFINIDO", TaskStatus.PLANNED),
            ("EM ANDAMENTO", TaskStatus.IN_PROGRESS),
            ("EM REVISÃO", TaskStatus.IN_REVIEW),
            ("COMPLETO", TaskStatus.COMPLETE),
            ("CONCLUÍDO", TaskStatus.COMPLETE),
            ("BLOQUEADO", TaskStatus.BLOCKED),
            ("COMPLETO (Em R0/APOS, este framework já foi criado)", TaskStatus.COMPLETE),
        ],
    )
    def test_load_from_markdown_narrative_status_mapping(
        self, tmp_path, status_text, expected_status
    ):
        """Deve mapear valores de status narrativo (NARRATIVE_STATUS_MAP) corretamente."""
        content = f"""## T0.0.1: Task X

**Objetivo:** Fazer algo

**Responsável:** Jader
**Esforço:** 1 dia
**Status:** {status_text}
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert sprint.get_task("T0.0.1").status == expected_status

    @pytest.mark.parametrize(
        "effort_text,expected_days",
        [
            ("1 dia", 1.0),
            ("2 dias", 2.0),
            ("1,5 dia", 1.5),
            ("4 dias-pessoa", 4.0),
        ],
    )
    def test_load_from_markdown_narrative_effort_parsing(
        self, tmp_path, effort_text, expected_days
    ):
        """Deve parsear duração narrativa aceitando vírgula como decimal."""
        content = f"""## T0.0.1: Task X

**Objetivo:** Fazer algo

**Responsável:** Jader
**Esforço:** {effort_text}
**Status:** Planejado
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert sprint.get_task("T0.0.1").days_estimate == expected_days

    def test_load_from_markdown_auto_detects_tabular_vs_narrative(self, tmp_path):
        """Deve detectar automaticamente o formato sem exigir especificação do usuário."""
        tabular_content = """## Tasks

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T0.0.1 | Tabular Task | Desc | 1d | planned | Jader |
"""
        narrative_content = """## T0.0.1: Narrative Task

**Objetivo:** Desc

**Responsável:** Jader
**Esforço:** 1 dia
**Status:** Planejado
"""
        tabular_md = tmp_path / "TABULAR.md"
        tabular_md.write_text(tabular_content, encoding="utf-8")
        narrative_md = tmp_path / "NARRATIVE.md"
        narrative_md.write_text(narrative_content, encoding="utf-8")

        tabular_sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0", release_id="R0", tasks_md_path=tabular_md
        )
        narrative_sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0", release_id="R0", tasks_md_path=narrative_md
        )

        assert tabular_sprint.get_task("T0.0.1").title == "Tabular Task"
        assert narrative_sprint.get_task("T0.0.1").title == "Narrative Task"

    def test_load_from_markdown_ignores_non_task_sections(self, tmp_path):
        """Deve ignorar seções cujo ID não case com o padrão de task (ex: "## Resumo")."""
        content = """## T0.0.1: Task Válida

**Objetivo:** Desc

**Responsável:** Jader
**Esforço:** 1 dia
**Status:** Planejado

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total | 1 |
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=tasks_md,
        )

        assert len(sprint.tasks) == 1
        assert sprint.get_task("T0.0.1") is not None

    def test_load_from_markdown_unrecognized_format_raises_clear_error(self, tmp_path):
        """Deve levantar ValueError claro se nem formato tabular nem narrativo forem encontrados."""
        content = """# Apenas um documento qualquer

Nenhuma tabela e nenhum header de task aqui, só texto solto.

## Resumo

Isso não é uma task.
"""
        tasks_md = tmp_path / "TASKS.md"
        tasks_md.write_text(content, encoding="utf-8")

        with pytest.raises(ValueError) as exc_info:
            Sprint.load_from_markdown(
                sprint_id="sprint-0.0",
                release_id="R0",
                tasks_md_path=tasks_md,
            )

        assert "não reconhecido" in str(exc_info.value)

    def test_load_from_markdown_integration_real_sprint_0_0_tasks_md(self):
        """Teste de integração: lê o TASKS.md real de sprint-0.0 do repositório."""
        real_tasks_md = REPO_ROOT / "docs" / "releases" / "R0" / "sprint-0.0" / "TASKS.md"
        assert real_tasks_md.exists(), f"Arquivo real não encontrado: {real_tasks_md}"

        sprint = Sprint.load_from_markdown(
            sprint_id="sprint-0.0",
            release_id="R0",
            tasks_md_path=real_tasks_md,
        )

        # O arquivo real tem 6 tasks: T0.0.1, T0.0.2, T0.0.3, T0.0.A, T0.0.B, T0.0.C
        assert len(sprint.tasks) == 6

        task_ids = {t.id for t in sprint.tasks}
        assert task_ids == {"T0.0.1", "T0.0.2", "T0.0.3", "T0.0.A", "T0.0.B", "T0.0.C"}

        # T0.0.1 está documentado como "COMPLETO (Em R0/APOS...)"
        assert sprint.get_task("T0.0.1").status == TaskStatus.COMPLETE
        # T0.0.2 e T0.0.3 estão documentados como "DEFINIDO"
        assert sprint.get_task("T0.0.2").status == TaskStatus.PLANNED
        assert sprint.get_task("T0.0.3").status == TaskStatus.PLANNED
        # T0.0.A/B/C estão documentados como "Planejado"
        assert sprint.get_task("T0.0.A").status == TaskStatus.PLANNED
        assert sprint.get_task("T0.0.B").status == TaskStatus.PLANNED
        assert sprint.get_task("T0.0.C").status == TaskStatus.PLANNED
