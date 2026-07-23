"""Geradores de templates para releases e sprints."""

from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


class ReleaseTemplateGenerator:
    """Gera templates de arquivos de release."""

    @staticmethod
    def generate_release_readme(
        release_id: str,
        title: str,
        description: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Gerar README.md de release."""
        return f"""# Release {release_id}: {title}

**Status:** Planning
**Período:** {start_date} até {end_date}

## Visão Geral

{description}

## Objetivos (OKRs)

Veja [OKR.md](OKR.md) para objetivos estratégicos desta release.

## Plano de Sprints

Veja [SPRINT_PLAN.md](SPRINT_PLAN.md) para cronograma de sprints.

## Backlog

Veja [BACKLOG.md](BACKLOG.md) para items priorizados (P0-P3).

## Dependências & Caminho Crítico

Veja [DEPENDENCY_MAP.md](DEPENDENCY_MAP.md) para análise de dependências.

## Marcos Chave

- [ ] Sprint planning complete
- [ ] Beta customers onboarded
- [ ] Market validation
- [ ] Feature complete
- [ ] Release shipped

---

**Criado:** {datetime.now().isoformat()}
"""

    @staticmethod
    def generate_sprint_readme(
        sprint_id: str,
        release_id: str,
        title: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Gerar README.md de sprint."""
        return f"""# {release_id} - {sprint_id}: {title}

**Status:** Planning
**Período:** {start_date} até {end_date}

## Contexto

Este sprint faz parte de [{release_id}](../) e deve entregar:

## Tarefas Planejadas

Veja [TASKS.md](TASKS.md) para lista detalhada de tarefas.

## User Stories

Veja [USER_STORIES.md](USER_STORIES.md) para histórias de usuário.

## Board Kanban

Veja [BOARD.md](BOARD.md) para status em tempo real.

## Status Diário

Veja [STATUS.md](STATUS.md) para burndown e métricas.

## Riscos & Mitigações

Veja [RISK_MITIGATION.md](RISK_MITIGATION.md) para análise de riscos.

## Daily Standups

Veja [DAILY_STANDUP_*.md](.) para updates diárias.

## Retrospectiva

Veja [RETRO.md](RETRO.md) para lições aprendidas.

---

**Criado:** {datetime.now().isoformat()}
"""

    @staticmethod
    def generate_sprint_tasks_template() -> str:
        """Gerar template de TASKS.md."""
        return """# Sprint Tasks

**Status:** Planning

---

## Task Naming Convention

- **T{release}.{sprint}.{number}** — Task ID
  - Ex: T0.0.1, T0.0.2, T1.2.5

## Tasks

### Tier 1: Core / Blockers (Must Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T | | | | planned | |

### Tier 2: Important (Should Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T | | | | planned | |

### Tier 3: Nice-to-Have (Could Have)

| ID | Título | Descrição | Duração | Status | Responsável |
|----|--------|-----------|---------|--------|-------------|
| T | | | | planned | |

---

## Dependências

- [ ] Tarefa X bloqueia Tarefa Y

---

## Resumo

| Métrica | Valor |
|---------|-------|
| Total de Tarefas | — |
| Dias Estimados | — |
| Completadas | — |
| Taxa de Conclusão | — |

---

## 📌 Commits de Rastreamento (Audit Trail)

*Registre aqui os commits a cada task concluída durante a sprint.*

| Commit | Task | Descrição |
|--------|------|-----------|
| `[hash]` | `[T-ID]` | [descrição] |

**Total de commits rastreados:** 0

---

**Última Atualização:** {datetime.now().isoformat()}
"""

    @staticmethod
    def generate_sprint_board_template() -> str:
        """Gerar template de BOARD.md (Kanban) — espelha estrutura do Sprint 0.0."""
        return f"""# Sprint Board — Kanban

**Status Atualizado:** {datetime.now().isoformat()}

---

## 📊 Resumo Visual

```
Backlog        A Fazer       Em Progresso    Em Revisão    Completo
   (N)            (N)            (N)            (N)          (N)

   ---            ↓              ↓              ↓           Done
```

---

## 📋 Backlog (Não Iniciado)

**Total de Backlog:** N items | N pontos planejados

### Tier N: [Nome da Tier]

- [ ] **T-X.Y.Z** — Título da tarefa (Nd)
  - Detalhe 1
  - Detalhe 2

---

## ✅ A Fazer (Pronto para Começar)

(Nenhum ainda)

---

## 🔄 Em Progresso

(Nenhum)

---

## 👀 Em Revisão

(Nenhum)

---

## ✅ Completo

(Nenhum ainda)

---

## 🚨 Bloqueado

(Nenhum)

---

## Audit Trail

| Commit | Task | Descrição |
|--------|------|-----------|
| `[hash]` | `[T-ID]` | [descrição] |

**Total de commits rastreados:** 0

---

**Board Atualizado:** Diariamente
**Próxima Atualização:** Tomorrow 07:00
"""

    @staticmethod
    def generate_sprint_status_template(sprint_id: str) -> str:
        """Gerar template de STATUS.md."""
        return f"""# {sprint_id} — Relatório de Status

**Última Atualização:** {datetime.now().isoformat()}

---

## 📊 Status Geral

**Fase Atual:** Planning

```
Progresso: 0 / N dias-pessoa (0%)
├─ Completo: —
├─ Em Progresso: —
├─ Planejado: N tarefas
└─ Em Risco: —
```

---

## 📈 Burndown

| Dia | Planejado | Completo | Status |
|-----|-----------|----------|--------|
| D1 | — | — | — |
| D2 | — | — | — |
| D3 | — | — | — |
| D4 | — | — | — |
| D5 | — | — | — |

---

## ✅ Completo

(Nenhum ainda)

---

## 🔄 Em Progresso

(Nenhum ainda)

---

## ⏳ Planejado

(Ver TASKS.md)

---

## 🚨 Riscos

**Riscos Ativos:** 0
**Riscos Mitigados:** 0

Veja [RISK_MITIGATION.md](RISK_MITIGATION.md) para detalhes.

---

## 🎯 Métricas

| Métrica | Alvo | Atual | Status |
|---------|------|-------|--------|
| Conclusão | 100% | — | — |
| Qualidade | — | — | — |
| Velocity | — | — | — |

---

## ⏱️ Métricas de Fluxo (Cycle Time)

| Task/US | Entrou em Progresso | Saiu para Completo | Cycle Time (dias) | Responsável |
|---------|---------------------|-------------------|-------------------|-------------|
| | | | | |

**Cycle Time Médio do Sprint:** — dias
**Tasks acima da média (investigar gargalo):** —

---

## 🔄 Retrabalho / Qualidade

| Task/US | Voltou para revisão? | Motivo | Nº de vezes |
|---------|----------------------|--------|-------------|
| | | | |

**Taxa de Retrabalho do Sprint:** — % (meta North Star: redução de 70%+ ao longo do tempo)
**Bugs abertos durante o sprint:** —

---

## 📌 Commit Tracking (Audit Trail)

*Registre commits das tasks concluídas durante a sprint.*

| Commit | Descrição | Task |
|--------|-----------|------|
| `[hash]` | | |

---

**Status Atualizado:** Diariamente (07:00)
**Próxima Atualização:** Tomorrow
"""

    @staticmethod
    def generate_daily_standup_template(sprint_id: str, format_type: str = "text") -> str:
        """Gerar template de Daily Standup.

        Args:
            sprint_id: ID do sprint
            format_type: "text" ou "markdown"
        """
        today = datetime.now().strftime("%Y-%m-%d")

        if format_type == "markdown":
            return f"""# Daily Standup — {sprint_id}

**Data:** {today}
**Time:** 07:00

---

## Formatos Disponíveis

Escolha um dos formatos abaixo:

### 1. Formato Texto (Simples)

**Participante:** [Seu Nome]
- ✅ Ontem: [O que você fez]
- 🎯 Hoje: [O que você vai fazer]
- 🚨 Blockers: [Bloqueadores, se houver]

### 2. Formato Structured (Detalhado)

**Participante:** [Seu Nome]

**O Que Fez Ontem:**
- [ ] Task 1
- [ ] Task 2

**O Que Vai Fazer Hoje:**
- [ ] Task A
- [ ] Task B

**Blockers / Impedimentos:**
- Blocker 1 (Severidade: 🔴/🟡/🟢)

**Notas:**
- Detalhe adicional

### 3. Formato Kanban (Visual)

**Participante:** [Seu Nome]

```
A Fazer      Em Progresso     Completo
[Task]  →    [Task]      →    [Task]
```

### 4. Formato Estruturado (Para Líderes)

**Data:** {today}

**Status Geral:** 🟢/🟡/🔴

**Progresso Geral:**
- Tarefas completas: N/N
- Taxa de conclusão: %
- Velocidade: pts/dia

**Top 3 Blockers:**
1. [Blocker]
2. [Blocker]
3. [Blocker]

**Próximos Passos:**
- [ ] Ação 1
- [ ] Ação 2

---

## Participantes

### [Participante 1]

**Formato escolhido:** [texto/structured/kanban/estruturado]

[Conteúdo aqui]

---

### [Participante 2]

[Conteúdo aqui]

---

## Sumário da Daily

- 🟢 Status: [On track / At risk / Blocked]
- ✅ Completado: [Quantas tarefas]
- 🚨 Blockers: [Quantos / quais]
- 🎯 Próximos: [Próximos passos]

---

**Facilitador:** [Nome]
**Duração:** [Minutos]
**Próxima Daily:** Tomorrow 07:00
"""

        else:  # text format
            return f"""DAILY STANDUP — {sprint_id}
Data: {today}
Hora: 07:00

=====================================

PARTICIPANTE 1: [Seu Nome]
- Ontem: [O que fez]
- Hoje: [O que vai fazer]
- Blockers: [Se houver]

PARTICIPANTE 2: [Seu Nome]
- Ontem: [O que fez]
- Hoje: [O que vai fazer]
- Blockers: [Se houver]

=====================================

BLOCKERS CRÍTICOS:
[Lista de bloqueadores]

PRÓXIMOS PASSOS:
[Ações identificadas]

PRÓXIMA DAILY: Tomorrow 07:00
"""

    @staticmethod
    def generate_retro_template() -> str:
        """Gerar template de RETRO.md."""
        return f"""# Sprint Retrospective

**Data:** {datetime.now().isoformat()}

---

## O Que Correu Bem ✅

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

---

## O Que Correu Mal ❌

- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

---

## Ideias de Melhoria 💡

- [ ] Melhoria 1
- [ ] Melhoria 2
- [ ] Melhoria 3

---

## Ações para Próximo Sprint

| Ação | Proprietário | Prioridade | Sprint |
|------|--------------|-----------|--------|
| | | high/med/low | |

---

## Métricas

| Métrica | Alvo | Valor | Status |
|---------|------|-------|--------|
| Velocidade Alcançada | — | — pts | |
| Taxa de Conclusão | 100% | — % | |
| Cycle Time Médio | ≤ 2 dias | — dias | |
| Taxa de Retrabalho | ≤ 15% | — % | |
| Moral da Equipe | — | — | |

---

## Lições Aprendidas

1. Lição 1
2. Lição 2
3. Lição 3

---

## Feedback Geral

[Espaço para feedback aberto]

---

**Facilitador:** [Nome]
**Duração:** [Minutos]
**Participantes:** [Nomes]
"""

    @staticmethod
    def generate_user_stories_template() -> str:
        """Gerar template de USER_STORIES.md."""
        return """# Sprint Stories — User Stories

**Status:** Planning

---

## US-X.Y.Z: [Título da História]

**Descrição:**
Como [persona], quero [funcionalidade] para que [benefício].

**Critérios de Aceitação:**
- [ ] Critério 1
- [ ] Critério 2
- [ ] Critério 3

**Sprint:** [sprint_id]
**Pontos:** N
**Responsável:** [Nome]
**Status:** 📅 PLANNED

---

**Total de Histórias:** N
**Pontos Totais:** N
**Completas:** 0
"""

    @staticmethod
    def generate_risk_mitigation_template() -> str:
        """Gerar template de RISK_MITIGATION.md."""
        return f"""# Sprint — Mitigação de Riscos

**Sprint:** [sprint_id]

---

## Registro de Riscos

### Risco 1: [Título do Risco]

**Probabilidade:** BAIXA / MÉDIA / ALTA
**Impacto:** BAIXO / MÉDIO / ALTO
**Severidade:** BAIXA / MÉDIA / ALTA

**Descrição:**
[Descrição do risco]

**Mitigação:**
[Ação de mitigação]

**Status:** 🟢 Aceito / 🟡 Monitorando / 🔴 Materializado

---

## Resumo

| Risco | Probabilidade | Impacto | Status |
|-------|--------------|---------|--------|
| | | | |

**Última Atualização:** {datetime.now().isoformat()}
"""


# --- Public API ---
