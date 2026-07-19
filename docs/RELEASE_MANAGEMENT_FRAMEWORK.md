# Release Management Framework — Core do APOS

**Data:** 19 de julho de 2026  
**Status:** ✅ Implementado e testado (22/22 testes passando)  
**Commit:** `0c643c3`

---

## Visão Geral

O **Release Management Framework** é um sistema operacional de gerenciamento de produto **embarcado no Core do APOS**. Quando um projeto importa APOS, recebe automaticamente:

- ✅ Gerenciamento de múltiplas releases (R0-R4)
- ✅ Gerenciamento de sprints com tarefas e user stories
- ✅ Cerimônias estruturadas (Daily Standup, Sprint Planning, Retrospective)
- ✅ Templates auto-gerados (8+ formatos Markdown)
- ✅ Métricas de progresso (velocity, completion_rate, burndown)
- ✅ Estrutura de diretórios pronta (`docs/releases/`)

---

## Módulos Implementados

### 1. `apos/release_management/release.py`

**Classes:**
- `Release`: Model para representar uma release
- `ReleaseManager`: Gerenciar múltiplas releases
- `ReleaseObjective`: Objetivos estratégicos com key results

**Funcionalidades:**
```python
# Criar release
rm = ReleaseManager(project_name="seu-projeto")
r0 = rm.create_release(
    release_id="R0",
    title="Bootstrap + Platform Identity",
    description="Estabelecer fundações",
    start_date="2026-07-19",
    end_date="2026-08-02"
)

# Adicionar objetivos
obj = ReleaseObjective(
    id="R0-O1",
    title="Estabelecer Fundações",
    key_results=["Bootstrap Gate", "JTBD Validado"]
)
r0.add_objective(obj)

# Auto-gerar estrutura
rm.initialize_release_directory("R0")

# Exportar sumário
summary = rm.export_summary()
```

---

### 2. `apos/release_management/sprint.py`

**Classes:**
- `Sprint`: Model para representar um sprint
- `SprintManager`: Gerenciar sprints dentro de uma release
- `Task`: Tarefa do sprint
- `TaskStatus`: Enum (backlog, planned, in_progress, in_review, complete, blocked)
- `UserStory`: User story com acceptance criteria

**Funcionalidades:**
```python
# Criar sprint
sm = SprintManager(release_id="R0")
sprint = sm.create_sprint(
    sprint_id="sprint-0.0",
    title="Scaffold + JTBD",
    start_date="2026-07-22",
    end_date="2026-07-26"
)

# Adicionar tarefas
task = Task(
    id="T0.0.1",
    title="Implementar Bootstrap Gate",
    description="Validador automático",
    days_estimate=2.0
)
sprint.add_task(task)

# Rastrear progress
sprint.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
sprint.completion_rate()  # 0.0-1.0
sprint.total_days_estimate()  # Dias totais

# Auto-gerar estrutura
sm.initialize_sprint_directory("sprint-0.0")
```

---

### 3. `apos/release_management/ceremonies.py`

**Classes:**
- `DailyStandup`: Daily standup com updates de participantes
- `DailyStandupUpdate`: Update individual (o que fez, o que faz, blockers)
- `SprintPlanningSession`: Planejamento de sprint
- `Retrospective`: Retrospectiva com ações de melhoria
- `RetroAction`: Ação de melhoria com prioridade

**Funcionalidades:**
```python
# Daily Standup
daily = DailyStandup(sprint_id="sprint-0.0", date="2026-07-22")
update = DailyStandupUpdate(
    participant="Jader",
    date="2026-07-22",
    what_done="Scaffolding",
    what_today="Bootstrap Gate",
    blockers="Agendamento"
)
daily.add_update(update)
daily.get_blockers()  # Lista de bloqueadores

# Sprint Planning
planning = SprintPlanningSession(
    sprint_id="sprint-0.0",
    date="2026-07-22",
    duration_minutes=120
)
planning.add_goal("Implementar Bootstrap Gate")
planning.add_planned_task("T0.0.1", "Bootstrap", 2.0)
planning.velocity_target = 4.0

# Retrospective
retro = Retrospective(
    sprint_id="sprint-0.0",
    date="2026-07-26",
    velocity_achieved=4.0,
    completion_rate=1.0
)
retro.add_well("Velocidade excepcional")
retro.add_action(RetroAction(
    category="improvements",
    description="Criar template de recrutamento",
    priority="high"
))
retro.get_high_priority_actions()
```

---

### 4. `apos/release_management/templates.py`

**Classe:**
- `ReleaseTemplateGenerator`: Gera templates Markdown

**Templates Disponíveis:**
1. `generate_release_readme()` — README de release
2. `generate_sprint_readme()` — README de sprint
3. `generate_sprint_tasks_template()` — TASKS.md
4. `generate_sprint_board_template()` — BOARD.md (Kanban)
5. `generate_sprint_status_template()` — STATUS.md (burndown)
6. `generate_daily_standup_template()` — DAILY_STANDUP.md (4 formatos)
7. `generate_retro_template()` — RETRO.md

**Formatos de Daily Standup:**
```python
# Formato 1: Text (simples)
template = ReleaseTemplateGenerator.generate_daily_standup_template(
    sprint_id="sprint-0.0",
    format_type="text"
)

# Formato 2: Markdown (estruturado)
template = ReleaseTemplateGenerator.generate_daily_standup_template(
    sprint_id="sprint-0.0",
    format_type="markdown"
)

# Formato 3: Kanban (visual)
# Formato 4: Estruturado (para líderes)
```

---

## Estrutura Gerada Automaticamente

Quando `ReleaseManager.initialize_release_directory()` ou `SprintManager.initialize_sprint_directory()` são chamados:

```
docs/releases/R0/                    (Release level)
├── README.md                        ← generate_release_readme()
├── OKR.md                           (pre-filled)
├── SPRINT_PLAN.md                   (pre-filled)
├── BACKLOG.md                       (pre-filled)
├── DEPENDENCY_MAP.md                (pre-filled)
│
└── sprint-0.0/                      (Sprint level)
    ├── README.md                    ← generate_sprint_readme()
    ├── TASKS.md                     ← generate_sprint_tasks_template()
    ├── USER_STORIES.md              (empty, pronto para preencher)
    ├── BOARD.md                     ← generate_sprint_board_template()
    ├── STATUS.md                    ← generate_sprint_status_template()
    ├── DAILY_STANDUP_2026-07-22.md  ← generate_daily_standup_template()
    ├── RISK_MITIGATION.md           (empty, pronto para preencher)
    └── RETRO.md                     ← generate_retro_template()
```

---

## Exemplo de Uso Completo

```python
from apos.release_management import (
    ReleaseManager,
    SprintManager,
    Task,
    TaskStatus,
    DailyStandup,
    DailyStandupUpdate,
    SprintPlanningSession,
    Retrospective,
    RetroAction,
    ReleaseTemplateGenerator,
)

# 1. SETUP: Inicializar releases
rm = ReleaseManager(project_name="meu-projeto")

# 2. CRIAR RELEASE
r0 = rm.create_release(
    release_id="R0",
    title="Bootstrap + Platform Identity",
    description="Estabelecer fundações semânticas",
    start_date="2026-07-19",
    end_date="2026-08-02"
)
rm.initialize_release_directory("R0")

# 3. CRIAR SPRINTS
sm = SprintManager(release_id="R0")

sprint_0_0 = sm.create_sprint(
    sprint_id="sprint-0.0",
    title="Scaffold + JTBD",
    start_date="2026-07-22",
    end_date="2026-07-26"
)

sm.initialize_sprint_directory("sprint-0.0")

# 4. ADICIONAR TAREFAS
task1 = Task(
    id="T0.0.1",
    title="Implementar Bootstrap Gate",
    days_estimate=2.0
)
sprint_0_0.add_task(task1)

# 5. CONDUZIR DAILY STANDUP
daily = DailyStandup(sprint_id="sprint-0.0", date="2026-07-22")
daily.add_update(DailyStandupUpdate(
    participant="Jader",
    date="2026-07-22",
    what_done="Estrutura de sprint",
    what_today="Bootstrap Gate",
    blockers="Nenhum"
))

# 6. CONDUZIR SPRINT PLANNING
planning = SprintPlanningSession(
    sprint_id="sprint-0.0",
    date="2026-07-22"
)
planning.add_attendee("Jader")
planning.add_goal("Implementar Bootstrap Gate")
planning.add_planned_task("T0.0.1", "Bootstrap", 2.0)

# 7. ATUALIZAR STATUS
sprint_0_0.update_task_status("T0.0.1", TaskStatus.IN_PROGRESS)
sprint_0_0.update_task_status("T0.0.1", TaskStatus.COMPLETE)

# 8. CONDUZIR RETROSPECTIVE
retro = Retrospective(
    sprint_id="sprint-0.0",
    date="2026-07-26",
    velocity_achieved=4.0,
    completion_rate=1.0
)
retro.add_well("Velocidade excepcional (5x alvo)")
retro.add_action(RetroAction(
    category="improvements",
    description="Iniciar recrutamento mais cedo",
    owner="Jader",
    priority="high"
))

# 9. EXPORTAR RELATÓRIOS
summary = sm.export_summary()
print(f"Sprints: {summary['num_sprints']}")
print(f"Taxa de conclusão: {summary['overall_completion_rate']:.0%}")

# 10. TEMPLATES (auto-gerados quando você chama initialize_*_directory)
readme = ReleaseTemplateGenerator.generate_sprint_readme(
    sprint_id="sprint-0.0",
    release_id="R0",
    title="Scaffold",
    start_date="2026-07-22",
    end_date="2026-07-26"
)
```

---

## Testes

**Arquivo:** `tests/unit/test_release_management.py`  
**Status:** ✅ 22/22 testes passando

```
TestRelease (4 testes)
├─ test_create_release ✅
├─ test_add_objective ✅
├─ test_add_sprint ✅
└─ test_to_dict ✅

TestReleaseManager (3 testes)
├─ test_create_release ✅
├─ test_list_releases ✅
└─ test_export_summary ✅

TestSprint (6 testes)
├─ test_create_sprint ✅
├─ test_add_task ✅
├─ test_total_days_estimate ✅
├─ test_completion_rate ✅
├─ test_add_user_story ✅
└─ test_update_task_status ✅

TestDailyStandup (3 testes)
├─ test_create_daily ✅
├─ test_add_update ✅
└─ test_get_blockers ✅

TestSprintPlanningSession (3 testes)
├─ test_create_planning ✅
├─ test_add_attendees_and_goals ✅
└─ test_total_estimated_days ✅

TestRetrospective (3 testes)
├─ test_create_retro ✅
├─ test_add_items ✅
└─ test_add_actions ✅
```

**Executar testes:**
```bash
pytest tests/unit/test_release_management.py -v
```

---

## Exemplo Executável

**Arquivo:** `examples/release_management_example.py`

Demonstra uso completo do framework com 3 exemplos:
1. `example_release_management()` — Release + Sprints
2. `example_ceremonies()` — Daily, Planning, Retro
3. `example_templates()` — Geração de templates

**Executar:**
```bash
python examples/release_management_example.py
```

---

## Integração com Bootstrap Gate

Quando um projeto importa APOS e passa pelo Bootstrap Gate:

1. **Validação**: Bootstrap Gate valida 10 fundações
2. **Auto-geração**: Auto-gera `docs/releases/R0/` com estrutura completa
3. **Embedding**: Projeto recebe ReleaseManager + SprintManager
4. **Pronto**: Projeto pode começar planejamento com templates

```python
import apos

# Ao importar APOS
from apos.release_management import ReleaseManager

# Projeto recebe sistema completo de management
rm = ReleaseManager(project_name="seu-projeto")
rm.initialize_release_directory("R0")  # Estrutura criada automaticamente
```

---

## Padrão de Processo Embarcado

### Release Cycle (R0-R4)
- Release Planning → Sprint Planning → Execution → Retro

### Sprint Cycle (5-7 dias)
- Sprint Planning → Daily Standups → Execution → Retro

### Templates por Nível

| Nível | Arquivos | Gerador |
|-------|----------|---------|
| **Release** | README, OKR, SPRINT_PLAN, BACKLOG, DEPENDENCY_MAP | ReleaseTemplateGenerator |
| **Sprint** | README, TASKS, BOARD, STATUS, DAILY, RISK, RETRO | ReleaseTemplateGenerator |
| **Daily** | DAILY_STANDUP (4 formatos) | ReleaseTemplateGenerator |

---

## CLI Commands

### `python -m apos daily`

Comando para executar Daily Standup de um sprint.

```bash
# Com modo explícito
python -m apos daily --sprint sprint-0.0 --date 2026-07-22 --mode automatic --tasks-json tasks.json

# Sem modo: pergunta ao usuário
python -m apos daily --sprint sprint-0.0 --tasks-json tasks.json
```

Ver documentação completa em [docs/DAILY_STANDUP_MODES.md](DAILY_STANDUP_MODES.md#comando-cli-python--m-apos-daily).

### Limitação Conhecida

**TODO:** `--tasks-json` é temporário. Quando existir `Sprint.load_from_markdown()`, será possível reconstruir Sprint a partir de `TASKS.md`/`BOARD.md`, tornando `--tasks-json` opcional.

---

## Próximos Passos

1. **Integração com Bootstrap Gate**
   - Bootstrap Gate auto-chama `ReleaseManager.initialize_release_directory("R0")`
   - Quando projeto passa validação, recebe estrutura de sprint pronta

2. **JTBD Discovery Framework**
   - Integrar `SprintPlanning` com JTBD questions
   - Auto-gerar `JTBD_INTERVIEWS.md` dentro do sprint

3. **Métricas & Dashboards**
   - Dashboard de velocidade (burndown, completion_rate)
   - Exportar relatórios JSON para ferramentas externas

4. **CLI Expansion**
   - `python -m apos sprint create sprint-0.0` → cria sprint + estrutura
   - Reconstrução de Sprint a partir de Markdown (`Sprint.load_from_markdown()`)

---

## Resumo

✅ **Release Management Framework está pronto e testado.**

Qualquer projeto que importa APOS recebe:
- Sistema operacional de gerenciamento de produto
- Templates prontos para 8+ documentos
- Cerimônias estruturadas (Daily, Planning, Retro)
- Métricas automatizadas (velocity, completion_rate)
- Padrão de processo validado (R0-S0 funcionando perfeitamente)

**Commit:** `0c643c3` — Release Management Framework Implementation

---

**Versão:** 1.0  
**Status:** ✅ Pronto para produção  
**Próxima revisão:** Integração com Bootstrap Gate
