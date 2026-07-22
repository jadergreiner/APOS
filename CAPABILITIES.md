# APOS Capabilities — Built-in Product Management Framework

**Version:** 0.1.0-beta  
**Status:** DEFINED IN R0  
**Part of Core:** YES

---

## O que são APOS Capabilities?

Capabilities são **frameworks e ferramentas semânticas** que vêm built-in com APOS.

Quando você importa APOS, você não recebe só "ontologia abstrata". Você recebe:
1. **Ontologia formal** (conceitos, relações, semântica)
2. **Frameworks prontos para usar** que usam essa ontologia
3. **Estruturas de governança** que garantem consistência

---

## Capability 1: Release + Sprint Management Framework

**Included in:** APOS Core  
**Semantic Foundation:** Ontologia de Release/Sprint/Task/OKR/Métrica  
**What it does:** Gerencia releases e sprints de forma estruturada e semanticamente consistente

### Artefatos Fornecidos

Quando você importa APOS, você recebe:

**Nível Release:**
- `RELEASE_PLAN.md` — Template executável
- `SPRINT_PLAN.md` — Breakdown de sprints
- `BACKLOG.md` — Items priorizados
- `DEPENDENCY_MAP.md` — Mapa de dependências
- `OKR.md` — Objetivos e key results

**Nível Sprint (Template):**
- `sprint-X/README.md` — Contexto e status
- `sprint-X/TASKS.md` — Breakdown de tasks
- `sprint-X/USER_STORIES.md` — User stories
- `sprint-X/BOARD.md` — Kanban board
- `sprint-X/STATUS.md` — Status report
- `sprint-X/RISK_MITIGATION.md` — Risk log
- `sprint-X/RETRO.md` — Retrospectiva
- `sprint-X/DAILY_STANDUP_{date}.md` — Gerado por `DailyStandupRunner`
  (`python -m apos daily`), não pelo gerador de template estático

### Daily Standup: DailyStandupRunner

Diferente dos demais artefatos (templates estáticos preenchidos manualmente),
a Daily Standup é **executada e computada** pelo `DailyStandupRunner`
(`apos/release_management/daily_runner.py`), com dois modos:

- **Automático** — infere `what_done`/`what_today`/`blockers` a partir do
  status das tasks (`TaskStatus`) e de commits reais encontrados via
  `git log`, sem interação do usuário
- **Colaborativo** — apresenta a análise inferida e pede confirmação/
  complemento do usuário antes de registrar

As tasks do sprint são reconstruídas automaticamente a partir de `TASKS.md`
(via `Sprint.load_from_markdown()`) ou de um `--tasks-json` explícito. Ver
[docs/DAILY_STANDUP_MODES.md](docs/DAILY_STANDUP_MODES.md) para o
comportamento completo, incluindo as limitações da evidência de git
(match literal de autor, falhas silenciosas).

### Como Funciona (Semanticamente)

```
Release (conceito)
    ├─ alcança N OKRs (relação semântica)
    └─ contém M Sprints (relação)
        ├─ cada Sprint tem N Sprints (relação)
        └─ cada Sprint contém M Tasks (relação)
            ├─ cada Task contribui_para 1 Feature (relação)
            └─ cada Task impacta N Métricas (relação)

Validação Semântica:
- Task não pode estar em 2 Features
- Release só termina se todos OKRs alcançados
- Sprint só termina se todos Tasks feitos
- OKR não pode ter 0 Métricas
```

### Valor Entregue

| Antes (sem APOS) | Depois (com APOS) |
|------------------|------------------|
| Releases ad-hoc, dispersas | Releases estruturadas e semânticas |
| Tasks desconectadas de OKRs | Tasks sempre conectadas a OKRs (validado) |
| Retrabalho (desalinhamento) | Zero retrabalho (alinhamento garantido) |
| Impacto de mudanças desconhecido | Impacto calculado em tempo real |
| PM "à deriva" | PM com propósito claro (conectado a North Star) |

---

## Capability 2: JTBD Discovery Framework

**Included in:** APOS Core (Sprint 0.0)  
**Semantic Foundation:** Ontologia de Job/Forces/Competitive Landscape  
**What it does:** Estrutura discovery de "jobs to be done" para validar que produto resolve job real

### Artefatos Fornecidos

- `R0/JTBD_RESEARCH.md` — Relatório de JTBD
- `R0/JOB_STATEMENT.md` — Job statement validado
- `R0/FORCES_ANALYSIS.md` — Push/Pull/Anxiety/Habit mapeado
- `R0/COMPETITIVE_LANDSCAPE.md` — Posicionamento

### Valor Entregue

Teams não correm o risco de buildarem algo que ninguém quer. Job é validado através de framework rigoroso.

---

## Capability 3: Ontology-Driven Product Strategy

**Included in:** APOS Core (Sprint 0.1-0.2)  
**Semantic Foundation:** Ontologia de North Star/OKR/Feature/Release  
**What it does:** Strategy é estruturada, semântica, e totalmente rastreável

### Artefatos Fornecidos

- `NORTH_STAR.md` — Visão de sucesso
- `PURPOSE.md` — Por quê produto existe
- `VALUE_PROPOSITION.md` — O que produto entrega
- `OKR.md` — Objetivos mensuráveis
- `COMPETITIVE_LANDSCAPE.md` — Posicionamento

### Valor Entregue

Strategy não é documento estático. É um **grafo semântico vivo** que guia todas as decisões:
- Sprint goal → conectado a OKR
- Feature → conectada a Release → conectada a OKR
- Task → conectada a Feature → conectada a OKR → conectada a Métrica

---

## Capability 4: Semantic Governance

**Included in:** APOS Core (Sprint 0.8)  
**Semantic Foundation:** Ontologia de Governance/Rules/Compliance  
**What it does:** Governança automática que valida alinhamento semântico

### Artefatos Fornecidos

- `GOVERNANCE.md` — Framework de governança
- `EVALUATIONS.md` — Avaliações de capabilities
- `AUDIT_FRAMEWORK.md` — Framework de auditoria

### Valor Entregue

Nenhuma task é implementada fora de domínio. Nenhuma feature é adicionada sem conexão a OKR. Nenhuma release perde deadline por desalinhamento.

---

## Como Usar APOS Capabilities

### Passo 1: Importar APOS

```python
from apos import ReleaseManagement, JTBDFramework, Ontology, SemanticGovernance

apos = APOS()
```

### Passo 2: Carregar seu Produto no APOS

```python
# Definir sua ontologia (baseada no template de APOS)
product_ontology = apos.Ontology.load_yaml("ontologies/product.yaml")

# Carregar seu conhecimento (OKRs, releases, features)
graph = apos.KnowledgeGraph()
graph.load_ontology(product_ontology)
graph.add_from_yaml("releases/R0/OKR.md")
graph.add_from_yaml("releases/R0/SPRINT_PLAN.md")
```

### Passo 3: Usar os Frameworks

```python
# Executar JTBD Discovery
jtbd = apos.JTBDFramework()
job = jtbd.discover(interviews=5, personas=["PM", "Agent", "Stakeholder"])
jtbd.validate(job)  # Valida que job é real

# Gerenciar Releases Semanticamente
release_mgmt = apos.ReleaseManagement()
release = release_mgmt.create_release(
    name="R0",
    okrs=graph.query("SELECT okr WHERE release='R0'"),
    sprints=10,
    governance_config=apos.SemanticGovernance.default()
)

# Adicionar Sprint
sprint = release_mgmt.add_sprint(
    sprint_id=0.0,
    tasks=[...],
    owner="PM"
)

# Validar Alinhamento
validator = apos.SemanticGovernance()
result = validator.validate_sprint(sprint)
# Valida: cada task conectada a feature? feature conectada a release? 
# release conectada a OKR? OKR conectada a métrica?
if not result.passes():
    print(f"Alinhamento quebrado: {result.issues}")
```

---

## Extensibilidade

APOS capabilities podem ser **estendidas** para novos domínios:

```python
# Criar capability customizada baseada em framework APOS
class SalesOperationsFramework(apos.Capability):
    """Estende Release Management para Sales."""
    
    def __init__(self, base_ontology):
        self.ontology = base_ontology
        # Adiciona conceitos: SalesGoal, Territory, Pipeline
        self.ontology.extend(SalesOntology)
    
    def manage_sales_cycle(self, ...):
        # Usa a mesma semântica de Release Management
        # mas aplicada a Sales
        pass
```

---

## O Diferencial de APOS

Outras ferramentas de PM (Jira, Asana, Linear):
- ❌ Armazenam dados em silos
- ❌ Sem semântica formal
- ❌ Retrabalho por desalinhamento
- ❌ Governança manual

**APOS:**
- ✅ Grafo semântico unificado
- ✅ Ontologia formal
- ✅ Validação automática de alinhamento
- ✅ Governança semântica
- ✅ Capabilities extensíveis

---

## Roadmap de Capabilities (R0-R4)

| Release | Capabilities | Status |
|---------|--------------|--------|
| **R0** | Release/Sprint Mgmt, JTBD, Ontology, Semantic Layer | DEFINING |
| **R1** | Knowledge Graph instantiation, Governance | PLANNED |
| **R2** | Impact Analysis, Linhagem de dados | PLANNED |
| **R3** | Semantic Gates, Audit Framework | PLANNED |
| **R4** | Agent Contracts, Ecosystem extensibility | PLANNED |

---

## Implementação em APOS

Esses frameworks **vivem em APOS como código**:

```
apos/
├── capabilities/
│   ├── release_management.py      # Release/Sprint framework
│   ├── jtbd_discovery.py          # JTBD framework
│   ├── ontology_driven_strategy.py # Strategy framework
│   └── semantic_governance.py      # Governance framework
│
├── examples/
│   ├── release_plan_R0.yaml       # Exemplo: R0 de APOS
│   ├── jtbd_interview_kit.md      # Kit de entrevistas
│   └── sprint_template/           # Template de sprint
│
└── templates/
    ├── RELEASE_PLAN.md
    ├── SPRINT_PLAN.md
    ├── BACKLOG.md
    └── sprint-X/
```

---

## Conceito Crítico: APOS Usa APOS

**O próprio APOS usa seus próprios frameworks para se desenvolver.**

- APOS R0 é gerenciado com Release Management Capability
- APOS sprints usam Sprint Framework
- APOS OKRs são rastreáveis via grafo semântico

**Isso garante:**
1. ✅ Dogfooding — detectamos problemas cedo
2. ✅ Validação — se APOS não consegue gerenciar a si mesmo, tem um problema
3. ✅ Credibilidade — time acredita no framework porque o usa

---

**Created:** 2026-07-19  
**Version:** 0.1.0-beta  
**Status:** Part of APOS Core (R0)
