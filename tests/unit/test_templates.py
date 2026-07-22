"""Testes para ReleaseTemplateGenerator."""

import re
from datetime import datetime

import pytest
from apos.release_management.templates import ReleaseTemplateGenerator


class TestReleaseTemplateGenerator:
    """Testes para ReleaseTemplateGenerator."""

    def test_generate_release_readme(self):
        """Gerar README de release."""
        content = ReleaseTemplateGenerator.generate_release_readme(
            release_id="R0",
            title="Fundacoes Estrategicas",
            description="Descricao da release",
            start_date="2026-07-19",
            end_date="2026-08-02",
        )

        assert "# Release R0: Fundacoes Estrategicas" in content
        assert "**Status:** Planning" in content
        assert "2026-07-19 at" in content
        assert "2026-08-02" in content
        assert "Descricao da release" in content
        assert "OKR.md" in content
        assert "SPRINT_PLAN.md" in content
        assert "BACKLOG.md" in content
        assert "DEPENDENCY_MAP.md" in content

    def test_generate_sprint_readme(self):
        """Gerar README de sprint."""
        content = ReleaseTemplateGenerator.generate_sprint_readme(
            sprint_id="sprint-0.2",
            release_id="R0",
            title="JTBD Deep Dive",
            start_date="2026-07-22",
            end_date="2026-07-26",
        )

        assert "# R0 - sprint-0.2: JTBD Deep Dive" in content
        assert "**Status:** Planning" in content
        assert "2026-07-22 at" in content
        assert "2026-07-26" in content
        assert "TASKS.md" in content
        assert "USER_STORIES.md" in content
        assert "BOARD.md" in content
        assert "STATUS.md" in content
        assert "RISK_MITIGATION.md" in content
        assert "RETRO.md" in content

    def test_generate_sprint_tasks_template(self):
        """Gerar template de TASKS.md."""
        content = ReleaseTemplateGenerator.generate_sprint_tasks_template()

        assert "# Sprint Tasks" in content
        assert "**Status:** Planning" in content
        assert "T{release}.{sprint}.{number}" in content
        assert "Tier 1: Core / Blockers (Must Have)" in content
        assert "Tier 2: Important (Should Have)" in content
        assert "Tier 3: Nice-to-Have (Could Have)" in content
        assert "## Resumo" in content
        assert "Total de Tarefas" in content

    def test_generate_sprint_board_template(self):
        """Gerar template de BOARD.md (Kanban)."""
        content = ReleaseTemplateGenerator.generate_sprint_board_template()

        assert "# Sprint Board — Kanban" in content
        assert "**Status Atualizado:" in content
        assert "Backlog        A Fazer       Em Progresso    Em Revis" in content
        assert "(N)" in content
        assert "## 📋 Backlog (Não Iniciado)" in content
        assert "## ✅ Completo" in content
        assert "**Board Atualizado:** Diariamente" in content

    def test_generate_sprint_status_template(self):
        """Gerar template de STATUS.md."""
        content = ReleaseTemplateGenerator.generate_sprint_status_template(
            sprint_id="sprint-0.2"
        )

        assert "# sprint-0.2 — Relatório de Status" in content
        assert "**Fase Atual:** Planning" in content
        assert "Progresso: 0 / N dias-pessoa (0%)" in content
        assert "## 📈 Burndown" in content
        assert "## ✅ Completo" in content
        assert "## 🚨 Riscos" in content
        assert "RISK_MITIGATION.md" in content
        assert "**Status Atualizado:** Diariamente (07:00)" in content

    def test_generate_daily_standup_text_format(self):
        """Gerar daily standup em formato texto."""
        content = ReleaseTemplateGenerator.generate_daily_standup_template(
            sprint_id="sprint-0.2", format_type="text"
        )

        assert "DAILY STANDUP — sprint-0.2" in content
        assert "PARTICIPANTE 1:" in content
        assert "- Ontem:" in content
        assert "- Hoje:" in content
        assert "- Blockers:" in content
        assert "PRÓXIMA DAILY:" in content

    def test_generate_daily_standup_markdown_format(self):
        """Gerar daily standup em formato markdown."""
        content = ReleaseTemplateGenerator.generate_daily_standup_template(
            sprint_id="sprint-0.2", format_type="markdown"
        )

        assert "# Daily Standup — sprint-0.2" in content
        assert "**Data:" in content
        assert "### 1. Formato Texto (Simples)" in content
        assert "### 2. Formato Structured (Detalhado)" in content
        assert "### 3. Formato Kanban (Visual)" in content
        assert "### 4. Formato Estruturado (Para Líderes)" in content
        assert "## Sumário da Daily" in content
        assert "**Próxima Daily:** Tomorrow 07:00" in content

    def test_generate_retro_template(self):
        """Gerar template de retrospetiva."""
        content = ReleaseTemplateGenerator.generate_retro_template()

        assert "# Sprint Retrospective" in content
        assert "## O Que Correu Bem" in content
        assert "## O Que Correu Mal" in content
        assert "## Ideias de Melhoria" in content
        assert "## Ações para Próximo Sprint" in content
        assert "Proprietário" in content

    def test_generate_user_stories_template(self):
        """Gerar template de user stories."""
        content = ReleaseTemplateGenerator.generate_user_stories_template()

        assert "# Sprint Stories — User Stories" in content
        assert "**Status:** Planning" in content
        assert "US-X.Y.Z:" in content
        assert "**Critérios de Aceitação:" in content
        assert "**Total de Histórias:" in content

    def test_generate_risk_mitigation_template(self):
        """Gerar template de mitigação de riscos."""
        content = ReleaseTemplateGenerator.generate_risk_mitigation_template()

        assert "# Sprint — Mitigação de Riscos" in content
        assert "## Registro de Riscos" in content
        assert "### Risco 1:" in content
        assert "**Probabilidade:**" in content
        assert "**Impacto:**" in content
        assert "**Mitigação:**" in content
        assert "## Resumo" in content

    def test_generate_timestamps_are_dynamic(self):
        """Verificar que timestamps sao dinamicos."""
        content = ReleaseTemplateGenerator.generate_sprint_board_template()
        # Deve conter um timestamp ISO ou data
        assert re.search(r"\d{4}-\d{2}-\d{2}", content)
