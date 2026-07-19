# Daily Standup — Dois Modos Dinâmicos

**Data:** 19 de julho de 2026  
**Status:** ✅ Implementado (13/13 testes passando)  
**Commit:** `b3b26e8`

---

## Visão Geral

O **Daily Standup** no APOS oferece **2 modos dinâmicos** que podem ser escolhidos na execução:

- **Opção A: Automático** — Sistema infere e gera automaticamente
- **Opção B: Colaborativo** — Sistema analisa, apresenta, usuário confirma/complementa

---

## Opção A: Automático

### O Que É

Sistema infere **automaticamente** o que foi feito olhando para evidências:
- Git commits
- Task status (COMPLETE, IN_PROGRESS, BLOCKED, PLANNED)
- Board updates
- Dependências entre tarefas
- Bloqueadores detectados

**Sem nenhuma interação do usuário.**

### Quando Usar

✅ CI/CD pipelines (automated daily reports)  
✅ Sprints rápidos (5 dias, muita automação)  
✅ Grandes equipes (muitos participantes)  
✅ Daily async (não há reunião síncrona)  
✅ Low-touch management

### Fluxo

```
System executa DailyStandupRunner(mode=AUTOMATIC)
    ↓
Analisa cada tarefa do sprint
    ├─ COMPLETE → "Completou [task]"
    ├─ IN_PROGRESS → "Continuando [task]"
    ├─ BLOCKED → "Bloqueado por: [reason]"
    └─ PLANNED → "Iniciando [task]"
    ↓
Detecta bloqueadores
    ├─ Status BLOCKED
    ├─ Dependências não completas
    └─ Task notes
    ↓
Exporta markdown com 100% confiança
    ↓
DAILY_STANDUP_2026-07-22.md criado
```

### Exemplo de Uso

```python
from apos.release_management import DailyStandupRunner, DailyMode

# Modo automático
runner = DailyStandupRunner(
    sprint=sprint_0_0,
    date="2026-07-22",
    mode=DailyMode.AUTOMATIC  # ← Automático
)

daily = runner.run()  # Executa automaticamente
runner.save_to_file(sprint_dir)  # Salva markdown

# Output
# ============================================================
# 📋 Daily Standup — sprint-0.0 (2026-07-22)
# ============================================================
#
# 🤖 Modo: AUTOMÁTICO (inferência de evidências)
# Analisando: commits, task status, board...
#
# ✅ Jader
#    Completou Bootstrap Gate
#    Continuando JTBD Interviews
#    🚨 Forces Analysis está bloqueado: Aguardando entrevistas
#
# ✅ Team
#    Iniciando Documentation
#    🚨 Bloqueado por: JTBD Interviews
#
# ============================================================
# ✅ Daily Automática Completa (2 updates)
# ============================================================
```

### Output Markdown

```markdown
# Daily Standup — sprint-0.0

**Data:** 2026-07-22
**Modo:** Automatic
**Participantes:** 2
**Updates:** 4

---

## Jader

**✅ Ontem:** Completou Bootstrap Gate

**🎯 Hoje:** Continuando JTBD Interviews

**🚨 Blockers:** Forces Analysis está bloqueado: Aguardando entrevistas

---

## 🚨 Bloqueadores Críticos

- Forces Analysis está bloqueado: Aguardando entrevistas
- Bloqueado por: JTBD Interviews
```

---

## Opção B: Colaborativo

### O Que É

Sistema **analisa evidências PRIMEIRO**, depois **apresenta ao usuário** para confirmação e complementos.

**Análise + Confirmação + Complementação.**

### Quando Usar

✅ Reuniões diárias síncronas  
✅ Equipes pequenas (5-10 pessoas)  
✅ High-touch management  
✅ Primeira vez fazendo daily  
✅ Precisão é crítico  
✅ Discussão em tempo real

### Fluxo

```
System executa DailyStandupRunner(mode=COLLABORATIVE)
    ↓
PARA CADA TAREFA:
    ├─ ANALISA evidências
    │  ├─ Status (COMPLETE/IN_PROGRESS/BLOCKED/PLANNED)
    │  ├─ Dependências (bloqueando?)
    │  ├─ Bloqueadores (flagged?)
    │  └─ Confiança (%)
    │
    ├─ APRESENTA ao usuário
    │  ├─ "Ontem: [evidência]"
    │  ├─ "Hoje: [tarefa em progresso]"
    │  └─ "Bloqueadores: [detectados]"
    │
    └─ SOLICITA CONFIRMAÇÃO + COMPLEMENTOS
       ├─ "Isso está correto?"
       │  └─ User confirma ou digita novo
       ├─ "Seu plano para hoje?"
       │  └─ User confirma ou digita novo
       └─ "Algum bloqueador?"
          └─ User confirma ou adiciona
    ↓
ESTRUTURA E DOCUMENTA tudo
    ↓
DAILY_STANDUP_2026-07-22.md criado
```

### Exemplo de Uso

```python
from apos.release_management import DailyStandupRunner, DailyMode

# Modo colaborativo
runner = DailyStandupRunner(
    sprint=sprint_0_0,
    date="2026-07-22",
    mode=DailyMode.COLLABORATIVE  # ← Colaborativo
)

daily = runner.run()  # Interativo!
runner.save_to_file(sprint_dir)
```

### Interação com Usuário

```
============================================================
📋 Daily Standup — sprint-0.0 (2026-07-22)
============================================================

👥 Modo: COLABORATIVO (análise + confirmação do usuário)
Analizando evidências (commits, tasks, board)...


────────────────────────────────────────────────────────────
Participante: Jader
────────────────────────────────────────────────────────────

📊 Análise de Evidências:
   Confiança: 100%

✅ O que você fez ontem:
   → Completou Bootstrap Gate
   Evidências: T0.0.1 COMPLETE

🎯 O que você vai fazer hoje:
   → Continuando JTBD Interviews
   Evidências: T0.0.2 IN_PROGRESS

────────────────────────────────────────────────────────────
🔄 Sua volta:
────────────────────────────────────────────────────────────

✅ Isso está correto? (Enter para confirmar ou digite nova descrição):
> [User presses Enter]

🎯 Seu plano para hoje? (Enter para confirmar ou digite novo):
> Entrevistar 3 mais personas

🚨 Algum bloqueador? (Enter se nenhum, ou descreva):
> Agendamento um pouco lento

✅ Update de Jader registrado!

────────────────────────────────────────────────────────────
Participante: Team
────────────────────────────────────────────────────────────

📊 Análise de Evidências:
   Confiança: 70%

✅ O que você fez ontem:
   (Sistema não encontrou evidências)

🎯 O que você vai fazer hoje:
   → Iniciando Documentation
   Evidências: T0.0.4 PLANNED

🚨 Bloqueadores detectados:
   → Bloqueado por: JTBD Interviews
   Evidências: T0.0.2 IN_PROGRESS

────────────────────────────────────────────────────────────
🔄 Sua volta:
────────────────────────────────────────────────────────────

✅ Isso está correto? (Enter para confirmar ou digite nova descrição):
> Resolvi alguns bugs também

🎯 Seu plano para hoje? (Enter para confirmar ou digite novo):
> Continuar docs + começar testes

🚨 Algum bloqueador? (Enter se nenhum, ou descreva):
> Preciso que JTBD termine para começar testes

✅ Update de Team registrado!

============================================================
📊 SUMÁRIO DA DAILY
============================================================
Participantes: 2
Updates: 2
Bloqueadores: 1

🚨 Bloqueadores Críticos:
   • Bloqueado por: JTBD Interviews

============================================================
```

### Output Markdown

```markdown
# Daily Standup — sprint-0.0

**Data:** 2026-07-22
**Modo:** Collaborative
**Participantes:** 2
**Updates:** 2

---

## Jader

**✅ Ontem:** Completou Bootstrap Gate

**🎯 Hoje:** Entrevistar 3 mais personas

**🚨 Blockers:** Agendamento um pouco lento

*Notas:* Confiança inicial: 100%
Confirmado e complementado pelo usuário

---

## Team

**🎯 Hoje:** Continuar docs + começar testes

**🚨 Blockers:** Preciso que JTBD termine para começar testes

*Notas:* Confiança inicial: 70%
Confirmado e complementado pelo usuário

---

## 🚨 Bloqueadores Críticos

- Bloqueado por: JTBD Interviews
```

---

## Comparação: Automático vs Colaborativo

| Aspecto | Automático | Colaborativo |
|---------|-----------|--------------|
| **Interação** | Nenhuma | Total (Q&A) |
| **Análise** | Sim | Sim (apresentado) |
| **Confirmação** | N/A | Sim (usuário) |
| **Complementação** | Não | Sim |
| **Tempo** | 1-2s | 5-10 min |
| **Precisão** | Média (100% evidence-based) | Alta (human-reviewed) |
| **Ideal para** | CI/CD, async | Reuniões síncronas |
| **Flexibilidade** | Baixa | Alta |
| **Confidência** | Rastreada | Rastreada |

---

## Como Usar

### Setup Básico

```python
from apos.release_management import (
    DailyStandupRunner,
    DailyMode,
    Sprint,
)

# Criar sprint
sprint = Sprint(
    id="sprint-0.0",
    release_id="R0",
    title="Bootstrap",
    start_date="2026-07-22",
    end_date="2026-07-26"
)

# Adicionar tarefas
sprint.add_task(...)

# Escolher modo
mode = DailyMode.COLLABORATIVE  # ou AUTOMATIC
```

### Executar Daily

```python
# Modo Automático
runner = DailyStandupRunner(sprint, date="2026-07-22", mode=DailyMode.AUTOMATIC)
daily = runner.run()

# Modo Colaborativo
runner = DailyStandupRunner(sprint, date="2026-07-22", mode=DailyMode.COLLABORATIVE)
daily = runner.run()  # Interativo!
```

### Salvar Resultado

```python
from pathlib import Path

sprint_dir = Path("docs/releases/R0/sprint-0.0")
runner.save_to_file(sprint_dir)
# Cria: DAILY_STANDUP_2026-07-22.md

# Ou exportar markdown
md_content = runner.export_markdown()
```

---

## Análise de Evidências

Ambos os modos usam `EvidenceAnalysis` para rastrear confiança:

```python
@dataclass
class EvidenceAnalysis:
    participant: str
    date: str
    what_done: str          # O que foi feito
    what_done_evidence: []  # ["commit abc", "T0.0.1 COMPLETE"]
    what_today: str         # O que vai fazer
    what_today_evidence: [] # ["T0.0.2 IN_PROGRESS"]
    blockers: str           # Bloqueadores
    blockers_evidence: []   # ["T0.0.3 BLOCKED", "RISK flagged"]
    confidence: float       # 0.0-1.0
```

### Scoring de Confiança

- **1.0** = Task COMPLETE ou BLOCKED (100% evidência)
- **0.9** = Task IN_PROGRESS (evidência clara)
- **0.7** = Task PLANNED (inferência)
- **0.0** = Nenhuma evidência

---

## Integração com Sprint

```python
sprint = Sprint(...)

# Adicionar tarefas com assignees
task = Task(
    id="T0.0.1",
    title="Bootstrap Gate",
    assignee="Jader",  # ← Necessário para Daily
    status=TaskStatus.IN_PROGRESS,
)
sprint.add_task(task)

# Daily automática agrupa por assignee
runner = DailyStandupRunner(sprint, "2026-07-22", DailyMode.AUTOMATIC)
daily = runner.run()
# Agrupa updates por Jader, Team, etc.
```

---

## Testes (13/13 Passando)

```
TestDailyStandupRunner (11 testes)
├─ test_create_runner_automatic ✅
├─ test_create_runner_collaborative ✅
├─ test_analyze_complete_task ✅
├─ test_analyze_in_progress_task ✅
├─ test_analyze_blocked_task ✅
├─ test_analyze_task_with_dependencies ✅
├─ test_run_automatic_mode ✅
├─ test_export_markdown ✅
├─ test_evidence_analysis_defaults ✅
├─ test_daily_blockers_detection ✅
└─ test_daily_participant_count ✅

TestEvidenceAnalysis (2 testes)
├─ test_create_analysis ✅
└─ test_analysis_with_evidence ✅
```

Executar:
```bash
pytest tests/unit/test_daily_runner.py -v
```

---

## Comando CLI: `python -m apos daily`

### Uso

```bash
# Com modo explícito
python -m apos daily --sprint sprint-0.0 --date 2026-07-22 --mode automatic --tasks-json tasks.json

# Modo colaborativo
python -m apos daily --sprint sprint-0.0 --date 2026-07-22 --mode collaborative --tasks-json tasks.json

# Sem modo: pergunta interativamente
python -m apos daily --sprint sprint-0.0 --tasks-json tasks.json
```

### Argumentos

- `--sprint` (obrigatório): ID do sprint (ex: `sprint-0.0`)
- `--date` (opcional): Data da daily (formato `YYYY-MM-DD`, default: hoje)
- `--mode` (opcional): `automatic` ou `collaborative`. Se não fornecido, pergunta ao usuário
- `--release` (opcional): ID da release (default: `R0`)
- `--tasks-json` (obrigatório): Caminho para arquivo JSON com tasks

### Formato JSON de Tasks

```json
[
  {
    "id": "T0.0.1",
    "title": "Bootstrap Gate",
    "description": "Implementar Bootstrap Gate",
    "days_estimate": 2.0,
    "status": "in_progress",
    "assignee": "Jader",
    "depends_on": [],
    "notes": ""
  }
]
```

### Status Válidos (TaskStatus enum)

- `backlog`
- `planned`
- `in_progress`
- `in_review`
- `complete`
- `blocked`

### Limitação Atual

**TODO:** Hoje não existe um método para reconstruir um Sprint a partir de `TASKS.md`/`BOARD.md` já gravados em disco. `--tasks-json` é uma solução temporária. Quando essa funcionalidade existir (ex: um método `Sprint.load_from_markdown()` ou similar), este comando deve passar a usá-la como default, tornando `--tasks-json` opcional/legado.

### Output

```
✅ Daily salva em: docs/releases/R0/sprint-0.0/DAILY_STANDUP_2026-07-22.md
```

---

## Próximos Passos

1. **Webhooks e Notificações**
   - Post daily summary to Slack
   - Email relatório de bloqueadores

2. **Dashboards**
   - Visualizar velocity histórica
   - Trends de blockers ao longo das sprints

3. **Histórico**
   - Guardar histórico de dailies
   - Análise de trends

4. **Reconstrução a partir de Markdown**
   - Implementar `Sprint.load_from_markdown()` para ler `TASKS.md`/`BOARD.md`
   - Tornar `--tasks-json` opcional no CLI

---

## Resumo

✅ **Daily Standup agora oferece 2 dinâmicas:**

- **Opção A (Automático):** Perfeito para CI/CD, sem interação
- **Opção B (Colaborativo):** Perfeito para reuniões síncronas, human-reviewed

**Projeto que importa APOS recebe ambas as opções embarcadas e pode escolher na execução.**

---

**Versão:** 1.0  
**Status:** ✅ Pronto para produção  
**Testes:** 13/13 passando
