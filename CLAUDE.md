# CLAUDE.md

Este arquivo fornece orientação ao Claude Code (<https://claude.ai/code>) ao trabalhar com código neste repositório.

## Visão Geral do Projeto

**APOS** (A Precise Ontology System) é um framework de camada semântica que fornece contexto de negócios preciso, vivo e conectado aos agentes de IA. Elimina alucinação e retrabalho em aplicações impulsionadas por IA, mantendo uma única fonte de verdade para conhecimento de domínio através de ontologias, grafos de conhecimento e portais de pontuação semântica.

Versão atual: **0.1.0-beta** (fase inicial de scaffolding)

**Principal stakeholder**: Jader Greiner (jadergreiner@gmail.com)

## Estratégia (Leia Primeiro)

Antes de trabalhar no código, entenda a estratégia do projeto:

- **[NORTH_STAR.md](NORTH_STAR.md)** — Visão de sucesso a longo prazo: "Teams visualize and reason about strategy end-to-end"
- **[PURPOSE.md](PURPOSE.md)** — Por que APOS existe: eliminar alucinação em aplicações com agentes de IA
- **[VALUE_PROPOSITION.md](VALUE_PROPOSITION.md)** — O que APOS entrega: contexto semântico formal para Product Management

## Core Capabilities

APOS não é só ontologia abstrata. Quando você importa APOS, você recebe:

- **[CAPABILITIES.md](CAPABILITIES.md)** — Frameworks built-in para Release/Sprint Management, JTBD Discovery, Semantic Governance
- **Release Management Framework** — Templates executáveis para gerenciar releases, sprints, backlogs semanticamente
- **JTBD Discovery Framework** — Kit estruturado para validar que produto resolve job real
- **Semantic Governance** — Validação automática de alinhamento estratégico

Exemplo: APOS R0 é gerenciado **usando os próprios frameworks de APOS** ([docs/releases/R0/](docs/releases/R0/)).

## Padrões de Kernel (Implementados + Obrigatórios)

**Quando projeto importa APOS, recebe automaticamente estes padrões implementados no package:**

### ✅ Semantic Validation Rule (FULL KERNEL)

Quando implementar validadores (ontologia, governança, estratégia), **enforce critérios REAIS de qualidade**, nunca decorativo:

❌ **ANTI-PADRÃO (Decorativo):**

```python
def validate_strategy(file_path):
    if file_exists(file_path) and not is_empty(file_path):
        return PASS  # Apenas verifica existência + tamanho
    return FAIL
```

✅ **PADRÃO (Semântica Real):**

```python
def validate_strategy(file_path):
    content = read_file(file_path)
    # Enforça NORTH_STAR format: "Teams [verb] [outcome]"
    # Enforça 5+ Key Results com métricas numéricas
    # Enforça PURPOSE conectado a NORTH_STAR
    # Enforça 3+ stakeholder validations
    if all_criteria_pass(content):
        return PASS
    return FAIL  # Com detalhes de quais critérios falharam
```

**Status:** ✅ Implementado em `apos/bootstrap/validators/` (24 testes, 85%+ cobertura)  
**Export:** `from apos.bootstrap.validators import StrategyValidator, OntologyValidator, GovernanceValidator`

---

### ✅ Bootstrap Gate Pattern (FULL KERNEL)

Quando projeto importa APOS pela primeira vez:

- **[BOOTSTRAP_GATE.md](BOOTSTRAP_GATE.md)** — Sistema automático que valida fundações semânticas
  - Verifica: NORTH_STAR.md, OKRs, PURPOSE, VALUE_PROPOSITION, Ontologia, Semantic Layer, Governance
  - Se falta algo: auto-gera templates + guia sessão de Foundation Definition
  - Se tudo OK: libera projeto para Release Planning
  - **Validação de Entrega**: Verifica que todas as tarefas têm commits rastreados

**3 Componentes-chave:**

1. **Detecção automática** — Identifica quais das 10 fundações estão presentes/ausentes
2. **Geração de templates** — Auto-cria NORTH_STAR.md, OKR.md, ONTOLOGY.md, etc. com instruções
3. **Sessão guiada** — Conduz projeto através de JTBD Discovery → Strategy Definition → Ontology Design → Governance Setup

**Uso prático:**

```bash
$ python -m apos init

APOS Project Initialization
===========================

Detectando fundações...
✅ NORTH_STAR.md
✅ OKR.md
❌ ONTOLOGY.md (missing)
❌ GOVERNANCE.md (missing)

GAPS encontrados. Iniciando Foundation Definition Session...
(Conduzindo through JTBD → Strategy → Ontology)
```

**Status:** ✅ Implementado em `apos/bootstrap/gate.py` + `apos/bootstrap/session.py` (35 testes, 81% cobertura)  
**Export:** `from apos import BootstrapGate, SessionManager`  
**Padrão reutilizável:** Use em todas releases (R0-R4) + sub-sistemas.

---

### 🔴 Commit Tracking CI Validation (IN PROGRESS → Sprint 0.1)

**O que é:** Validação automática que artefatos de sprint (TASKS.md, BOARD.md, STATUS.md) têm refs de commit.

**Por quê Kernel:** Audit trail precisa ser garantido, não aspiracional.

**Status atual:**
- ✅ Especificação: [docs/COMMIT_TRACKING.md](docs/COMMIT_TRACKING.md)
- ✅ Padrão documentado: Sprint 0.0 exemplo completo
- 🔴 Implementação: `apos/kernel/commit_tracking.py` (TODO — Sprint 0.1)
- 🔴 CI/CD validation: `.github/workflows/` (TODO — Sprint 0.1)
- 🔴 Export: `from apos import CommitTrackingValidator` (TODO)

**Será Kernel quando:**
- ✅ CommitTrackingValidator implementado + testado
- ✅ BootstrapGate integrado com validator
- ✅ CI/CD workflow validando PRs
- ✅ Documentação: "Projeto que importa APOS recebe validação automática de commit tracking"

**Spec detalhada:** [docs/KERNEL_COMMIT_TRACKING_SPEC.md](docs/KERNEL_COMMIT_TRACKING_SPEC.md)

---

## Padrões de Processo (Recomendado, Não Enforçado)

**Padrões de workflow recomendados, não implementados em código:**

### Paralelização Padrão em Sprint Planning

**Aprendizado Sprint 0.0:** Planning assumiu sequencial (Tier 1 Core → Tier 2 JTBD), mas descoberta durante execução: **paralelização era viável e entregou +250% velocidade**.

**Regra de Planning:**

1. **Sempre questione dependências** — não assuma sequencial
2. **Default a paralelo, não serial** — mude para serial apenas se bloqueador real existir
3. **Documente razão de sequencial** — se T2 depende de T1 result, deixe explícito
4. **Ajuste velocity base** — Sprint 0.0 +250% sugere previous estimativas muito conservadoras

**Exemplo Sprint 0.0:**

```text
PLANEJADO (Sequencial):
  Tier 1 (Core): 4 dias
  Tier 2 (JTBD): 4 dias (bloqueador de Tier 1)
  Total: 8 dias

REAL (Paralelo):
  Tier 1 (Core) + Tier 2 (JTBD) simultâneos
  Habilitador: T0.0.2 (Bootstrap Gate) virou enabler para T0.0.3
  Total: 3 dias (~250% faster)
```

**Aplicação:** R0-R4 sprint planning — sempre revise parallelizability em planning, não discovery.

## Releases & Planejamento

Cada release (R0-R4) implementa essa estratégia. Veja [docs/releases/](docs/releases/) para:
- **Release Plans** — Planejamento executivo
- **Sprint Plans** — Breakdown de sprints (templates + estruturas)
- **Backlogs** — Items priorizados
- **Dependencies** — Mapa de dependências

## Setup do Ambiente de Desenvolvimento

```bash
# Clone e setup
git clone https://github.com/jadergreiner/APOS.git
cd APOS
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou: venv\Scripts\activate  # Windows

# Instala em modo desenvolvimento (inclui dependências de dev)
pip install -e ".[dev]"
```

## Comandos Comuns

### Testes

```bash
pytest                                    # Executa todos os testes
pytest -v                                 # Saída verbose
pytest tests/unit/test_ontology.py       # Executa arquivo de teste específico
pytest tests/unit/test_ontology.py::TestClass::test_method  # Executa teste único
pytest --cov=apos tests/                 # Com relatório de cobertura
pytest -x                                 # Para no primeiro erro
```

### Qualidade de Código

```bash
black apos/ tests/                       # Formata código
flake8 apos/ tests/                      # Verifica estilo
black --check apos/ tests/                # Verifica formato sem alterar
```

### Package & Verificação

```bash
python -c "import apos; print(apos.__version__)"  # Verifica versão
python examples/basic_usage.py           # Executa exemplo
pip install -e ".[dev]"                  # Reinstala após mudanças em setup.py
```

## Estrutura do Projeto

```
APOS/
├── apos/                          # Package principal
│   ├── __init__.py                # Versão, exports públicos
│   ├── core/                      # Abstrações core (stubs vazios)
│   │   ├── __init__.py
│   │   ├── types.py               # Tipos de domínio (Entity, Relationship, Node, Edge)
│   │   ├── ontology.py            # Modelo de ontologia
│   │   ├── graph.py               # Grafo de conhecimento
│   │   └── semantic.py            # Lógica de pontuação semântica
│   ├── bootstrap/                  # Bootstrap Gate + Inicialização (R0-S0.0)
│   │   ├── __init__.py
│   │   ├── gate.py                # BootstrapGate — validação de fundações
│   │   ├── session.py             # Foundation Definition Session
│   │   ├── validators/            # Validadores especializados
│   │   │   ├── strategy_validator.py
│   │   │   ├── ontology_validator.py
│   │   │   └── governance_validator.py
│   │   └── templates/             # Templates auto-gerados
│   │       ├── NORTH_STAR.md
│   │       ├── OKR.md
│   │       ├── ONTOLOGY.md
│   │       ├── SEMANTIC_LAYER.md
│   │       └── GOVERNANCE.md
│   ├── release_management/        # Gerenciamento de Releases & Sprints (NOVO!)
│   │   ├── __init__.py            # Exports: ReleaseManager, SprintManager, Ceremonies
│   │   ├── release.py             # Release, ReleaseManager, ReleaseObjective
│   │   ├── sprint.py              # Sprint, SprintManager, Task, UserStory, TaskStatus
│   │   ├── ceremonies.py          # DailyStandup, SprintPlanning, Retrospective
│   │   └── templates.py           # ReleaseTemplateGenerator (4+ formatos)
│   ├── governance/                # Framework de governança (stubs vazios)
│   │   ├── __init__.py
│   │   ├── gate.py                # Verificações de qualidade SemanticGate
│   │   ├── metrics.py             # Métricas de pontuação
│   │   ├── audit.py               # Ferramentas de auditoria
│   │   └── config.py              # Configuração de governança
│   ├── loader/                    # Carregadores de dados (stub)
│   │   ├── ontology_loader.py     # Carrega ontologias de YAML/JSON
│   │   └── graph_loader.py        # Carrega grafos
│   ├── utils/                     # Utilitários (stubs vazios)
│   │   ├── __init__.py
│   │   ├── validators.py          # Helpers de validação
│   │   ├── serializers.py         # Serialização
│   │   └── logger.py              # Logging
│   └── errors.py                  # Exceções customizadas
├── tests/                         # Suite de testes (pytest)
│   ├── conftest.py                # Configuração pytest + fixtures
│   ├── unit/                      # Testes unitários (principalmente stubs vazios)
│   ├── integration/               # Testes de integração
│   └── fixtures/                  # Dados de teste compartilhados
├── examples/                      # Exemplos de uso
│   ├── basic_usage.py
│   ├── meu_pdi_integration.py
│   └── enterprise_usage.py
├── docs/                          # Documentação
│   ├── ARCHITECTURE.md            # Design do sistema (atualmente vazio)
│   ├── API.md                     # Referência de API (atualmente vazio)
│   ├── INTEGRATION.md
│   ├── GOVERNANCE.md
│   └── DEVELOPMENT.md
├── pyproject.toml                 # Configuração moderna do projeto Python
├── setup.py                       # Configuração Setuptools
├── .gitignore
├── CHANGELOG.md
└── README.md                      # Documentação principal
```

## Arquitetura & Conceitos Chave

### Camada Core (`apos/core/`)

A fundação do APOS. Define abstrações de domínio que todas as outras camadas constroem:

- **types.py**: Primitivos de domínio
  - `Entity`: Representa um conceito no seu domínio (ex: "Student", "Course")
  - `Relationship`: Conexões entre entidades (ex: "enrolled_in")
  - `Node`: Nó do grafo envolvendo uma instância de entidade
  - `Edge`: Aresta do grafo representando uma instância de relacionamento

- **ontology.py**: Modelo estrutural do seu domínio
  - `Ontology`: Container para entidades, relacionamentos e hierarquias
  - Definições imutáveis do que pode existir no seu domínio
  - Exemplo: "Uma entidade Student pode ter atributos: id, name, email"

- **graph.py**: Grafo de conhecimento em tempo de execução construído a partir de ontologia
  - `KnowledgeGraph`: Grafo em memória de instâncias de domínio
  - Armazena nós de dados reais e seus relacionamentos
  - Exemplo: Nó "student_001" (Alice) conecta a "course_101" (Python)

- **semantic.py**: Lógica de pontuação
  - Mede completude, acurácia e consistência de um grafo de conhecimento
  - Componentes: ontology_coverage, relationship_quality, data_consistency
  - Pondera estes em uma pontuação semântica geral (0.0-1.0)

### Camada de Governança (`apos/governance/`)

Portais de qualidade e auditoria para garantir confiabilidade de contexto:

- **gate.py**: `SemanticGate` - valida que um grafo de conhecimento atenda aos limiares de qualidade
  - min_score configurável (padrão 0.80)
  - Retorna um `GateResult` com score, status e problemas detalhados
  - PASS (≥0.80), CONDITIONAL (0.60-0.80), FAIL (<0.60)

- **metrics.py**: Componentes individuais de pontuação
  - Calcula scores de componentes (coverage, quality, consistency)
  - Combina em pontuação semântica geral

- **audit.py**: `AuditRunner` - inspeção profunda e recomendações de melhoria
  - Identifica lacunas em cobertura de ontologia
  - Lista problemas de validade de relacionamentos
  - Fornece recomendações de melhoria

- **config.py**: Configurações de governança sintonizáveis
  - Limiares de portais semânticos
  - Pesos de métricas (coverage, quality, consistency)
  - Regras de governança customizadas

### Camada Release Management (`apos/release_management/`)

**Sistema operacional de gerenciamento de produto** embarcado em APOS. Quando um projeto importa APOS, recebe automaticamente:

- **release.py**: `Release` + `ReleaseManager`
  - Gerenciar múltiplas releases (R0-R4) com objetivos, sprints, dependências
  - Auto-gerar estrutura de diretórios (`docs/releases/R0/`)
  - Rastrear fases (planning, active, shipped, retro)

- **sprint.py**: `Sprint` + `SprintManager`
  - Gerenciar sprints com tarefas (`Task`), user stories (`UserStory`)
  - Rastrear status (`TaskStatus`: backlog, planned, in_progress, in_review, complete, blocked)
  - Calcular métricas (total_days_estimate, completion_rate, velocity)
  - Auto-gerar estrutura de sprint (`docs/releases/R0/sprint-0.0/`)

- **ceremonies.py**: `DailyStandup`, `SprintPlanning`, `Retrospective`
  - Daily Standup: capturar updates de participantes (o que fez, o que faz, blockers)
  - Sprint Planning: planejar tarefas, goals, velocity target
  - Retrospective: capturar o que correu bem/mal, ideias de melhoria, ações

- **templates.py**: `ReleaseTemplateGenerator`
  - Gerar templates de documentos (README, TASKS, BOARD, STATUS, RETRO)
  - Daily Standup com **4 formatos**: text, markdown, kanban, estruturado
  - Todos os templates são Markdown prontos para usar

**Estrutura gerada automaticamente:**
```
docs/releases/R0/
├── README.md (release level)
├── OKR.md
├── SPRINT_PLAN.md
├── BACKLOG.md
├── DEPENDENCY_MAP.md
└── sprint-0.0/
    ├── README.md (sprint context)
    ├── TASKS.md (tarefas detalhadas)
    ├── USER_STORIES.md (histórias)
    ├── BOARD.md (kanban visual)
    ├── STATUS.md (burndown + métricas)
    ├── DAILY_STANDUP_[DATE].md (múltiplos formatos)
    ├── RISK_MITIGATION.md (riscos + mitigações)
    └── RETRO.md (retrospectiva)
```

**Exemplo de uso:**
```python
from apos.release_management import ReleaseManager, SprintManager

# Gerenciar releases
rm = ReleaseManager(project_name="seu-projeto")
r0 = rm.create_release("R0", "Bootstrap", "...", "2026-07-19", "2026-08-02")
rm.initialize_release_directory("R0")

# Gerenciar sprints
sm = SprintManager(release_id="R0")
sprint = sm.create_sprint("sprint-0.0", "Scaffold", "2026-07-22", "2026-07-26")
sprint.add_task("T0.0.1", "Bootstrap Gate", days=2)
sm.initialize_sprint_directory("sprint-0.0")

# Conduzir cerimônias
daily = DailyStandup(sprint_id="sprint-0.0", date="2026-07-22")
daily.add_update(DailyStandupUpdate(...))

planning = SprintPlanning(sprint_id="sprint-0.0", date="2026-07-22")
planning.add_goal("Implementar Bootstrap Gate")

retro = Retrospective(sprint_id="sprint-0.0", date="2026-07-26")
retro.add_well("Velocidade excepcional")
retro.add_action(RetroAction(...))
```

### Camada Bootstrap (`apos/bootstrap/`)

Inicialização automática de projetos APOS (R0-Sprint 0.0):

- **gate.py**: `BootstrapGate` - valida fundações semânticas necessárias
  - `validate()`: checa existência de 10 itens obrigatórios
  - `initialize_foundation_session()`: inicia sessão guiada se faltam items
  - `validate_after_session()`: re-valida após definição de fundações

- **session.py**: `FoundationDefinitionSession` - guia projeto através de JTBD → Strategy → Ontology
  - `run_jtbd_discovery()`: Conduz entrevistas estruturadas
  - `run_platform_identity()`: Define North Star, OKRs, posicionamento
  - `run_ontology_definition()`: Estrutura conceitos e semântica
  - `run_governance_setup()`: Define regras de governança

- **validators/**: Validadores especializados para cada tipo de fundação
  - Verifica corretude de estrutura, completude de campos, consistência

- **templates/**: Templates auto-gerados para cada documento de fundação
  - Auto-populados com instruções e exemplos

**Propósito:** Quando projeto importa APOS, Bootstrap Gate **garante que fundações existem antes de execução começar**. Se faltam, guia projeto através de sessão estruturada de definição.

### Camada de Loader (`apos/loader/`)

Ingestão de dados (implementação stub):

- **ontology_loader.py**: `OntologyLoader.from_yaml()`, `from_json()` - carrega modelos de domínio estruturados
- **graph_loader.py**: Carrega dados em tempo de execução em grafos de conhecimento

### Utilitários (`apos/utils/`)

Helpers e infraestrutura:

- **validators.py**: Validação de dados (estrutura de ontologia, tipos de entidade, etc.)
- **serializers.py**: Serialização/desserialização de grafos e ontologias
- **logger.py**: Logging estruturado

## Estado Atual (Beta)

A maioria dos módulos core são **scaffolded com type hints mas ainda não implementados**. A API pública é definida em docstrings e anotações de tipo, mas os corpos estão vazios ou contêm stubs de TODO.

**Ao implementar features:**

1. Comece com a camada mais baixa (`core/types.py`) para estabelecer primitivos de domínio
2. Construa até `core/ontology.py` e `core/graph.py`
3. Camada em `core/semantic.py` para pontuação
4. Finalmente, adicione lógica de portais de governança e auditoria
5. Escreva testes junto - abordagem TDD é preferida

**Fixtures de teste** (em `conftest.py`) fornece estruturas de ontologia e grafo de exemplo para reuso.

## Dependências

**Dependências core** (produção):

- `pyyaml>=6.0` — Analisa definições de ontologia YAML
- `pydantic>=2.0` — Validação de dados e type hints

**Dependências de dev**:

- `pytest>=7.0` — Framework de testes
- `pytest-cov>=4.0` — Relatório de cobertura
- `black>=23.0` — Formatação de código (comprimento de linha 100 caracteres)
- `flake8>=6.0` — Verificação de estilo

## Estilo de Código & Convenções

**Formatação**:

- Black com limite de linha de 100 caracteres (veja `pyproject.toml`)
- Execute `black apos/ tests/` antes de fazer commit

**Testes**:

- Marcas pytest: `@pytest.mark.unit` e `@pytest.mark.integration`
- Fixtures em `conftest.py` (prefira em vez de setup/teardown)
- Objetivo ≥80% de cobertura (enforced em CI)

**Naming**:

- Classes: PascalCase (`SemanticGate`, `KnowledgeGraph`)
- Funções/métodos: snake_case (`add_node`, `evaluate`)
- Constantes: UPPER_SNAKE_CASE (`MIN_SCORE`, `METRIC_WEIGHTS`)
- Privado/interno: prefixo com `_`

**Type hints**:

- Use em toda parte (requerido para este beta)
- Modelos Pydantic para data classes
- Type hints de retorno para todas as APIs públicas

**Imports**:

- Biblioteca padrão primeiro, depois third-party (pydantic, pyyaml), depois local
- Use imports absolutos de `apos.*`

**Erros**:

- Defina exceções customizadas em `apos/errors.py`
- Herde de classe base `AposError`
- Lance com mensagens claras e acionáveis

## Estratégia de Testes

**Testes unitários** (`tests/unit/`):

- Teste classes e funções individuais isoladamente
- Use fixtures de `conftest.py` para dados de amostra
- Sem I/O ou dependências externas (mock se necessário)

**Testes de integração** (`tests/integration/`):

- Teste workflows através de múltiplas camadas
- Carregue ontologias YAML reais, construa grafos, pontue-os
- Exemplo: `OntologyLoader.from_yaml()` → `KnowledgeGraph` → `SemanticGate.evaluate()`

**Expectativas de cobertura**:

- Objetivo ≥80% para package `apos/`
- CI enforça via `pytest --cov=apos`

**Ao adicionar features**:

1. Escreva teste primeiro (TDD)
2. Implemente feature
3. Execute `pytest tests/unit/test_feature.py -v`
4. Verifique cobertura com `pytest --cov=apos tests/`
5. Formata e lint antes de fazer commit

## Pontos de Integração

APOS é projetado para ser consumido por projetos downstream (atualmente: Meu PDI). Padrões chave de integração:

**Uso básico** (veja `examples/basic_usage.py`):

```python
from apos import Ontology, KnowledgeGraph, SemanticGate
from apos.loader import OntologyLoader

# 1. Carregue ontologia (define estrutura de domínio)
ontology = OntologyLoader.from_yaml("ontologies/student_journey.yaml")

# 2. Construa grafo de conhecimento (popule com dados reais)
graph = KnowledgeGraph()
graph.load_ontology(ontology)
# ... adicione nós e arestas da sua fonte de dados ...

# 3. Avalie com portal de governança
gate = SemanticGate(min_score=0.80)
score = gate.evaluate(graph)

# 4. Use contexto se portal passar
if score.passes():
    context = prepare_agent_context(graph)
    agent.execute(context)
else:
    print(f"Problemas de contexto: {score.issues}")
```

**Avançado**: Customize configuração de governança

```python
from apos.governance import GovernanceConfig, SemanticGate

config = GovernanceConfig(
    min_score=0.85,  # Mais rigoroso
    weights={"coverage": 0.2, "quality": 0.5, "consistency": 0.3}
)
gate = SemanticGate(config=config)
```

## PM Skills & Frameworks Complementares

Para ontologias, workflows e frameworks de **Product Management específicos**, recomendamos:

### PM-Skills Library

**Referência**: [github.com/product-on-purpose/pm-skills](https://github.com/product-on-purpose/pm-skills)

- **68 production-ready PM skills** organizados por ciclo (Discover → Define → Develop → Deliver → Measure → Iterate)
- **Triple Diamond Framework** — modelo estruturado para inovação de produto
- **12 workflows prontos** (Feature Kickoff, Lean Startup, Foundation Sprint, Design Sprint, etc.)
- **5 sub-agentes orquestrados** para automação de processos PM
- **200+ output samples** como referência de qualidade

**Quando usar**:
- Você precisa de templates de PM executáveis (PRD, user stories, roadmaps)
- Você quer workflows orquestrados para processos comuns (feature discovery, sprint planning)
- Você busca referência de estrutura para skills customizados

**Integração com APOS**:
- Use PM-Skills para **executar processos** que fundamentam suas ontologias de domínio
- Use APOS para **validar semântica e confiança** dos artefatos gerados por PM-Skills
- Complementaridade: PM-Skills = "como fazer" | APOS = "validar qualidade e alinhamento"

**Instalação**:
```bash
# Claude Code (recomendado)
/plugin marketplace add product-on-purpose/agent-plugins
/plugin install pm-skills@product-on-purpose

# Cross-agent (Cursor, Copilot, Cline, etc)
npx skills add product-on-purpose/pm-skills

# Clone direto
git clone https://github.com/product-on-purpose/pm-skills.git
```

## Tarefas Comuns de Desenvolvimento

### Adicionar novo tipo de entidade ao modelo de ontologia

1. Atualize `core/types.py` com novos campos (se necessário)
2. Adicione testes em `tests/unit/test_types.py`
3. Atualize `ARCHITECTURE.md` para documentar o novo tipo

### Implementar nova métrica de pontuação

1. Adicione função de métrica a `governance/metrics.py`
2. Fiação em lógica de pontuação `core/semantic.py`
3. Adicione testes em `tests/unit/test_semantic.py`
4. Atualize pesos em `governance/config.py` se necessário

### Carregamento de novo formato de dados (ex: JSON)

1. Adicione método carregador a `loader/ontology_loader.py` (ex: `from_json()`)
2. Adicione testes que comparem com saída YAML
3. Documente em `docs/INTEGRATION.md`

### Adicionar nova regra de governança

1. Implemente em `governance/audit.py` ou `gate.py`
2. Adicione opção de configuração a `governance/config.py`
3. Escreva testes de integração com dados de amostra
4. Atualize `docs/GOVERNANCE.md`

## Arquivos de Documentação

- **README.md**: Visão geral do projeto, quick start, conceitos core, roadmap
- **docs/ARCHITECTURE.md**: Design do sistema, interações de componentes, fluxo de dados (atualmente vazio)
- **docs/API.md**: Referência de API detalhada com exemplos (atualmente vazio)
- **docs/INTEGRATION.md**: Como usar APOS no seu projeto
- **docs/GOVERNANCE.md**: Detalhes de portais de governança e framework de auditoria
- **docs/DEVELOPMENT.md**: Diretrizes de contribuição, estilo de código, testes
- **CHANGELOG.md**: Histórico de versão e mudanças breaking (atualmente vazio)

## Workflow Git

**Naming de branch**: `feature/name-of-feature`, `fix/issue-name`, `docs/topic`

**Mensagens de commit**:

```
feat: add new entity validation
fix: resolve ontology coverage calculation
docs: update API reference for SemanticGate
test: add integration tests for graph loading
```

**Antes de fazer push**:

```bash
pytest --cov=apos tests/          # Testes passam + cobertura ≥80%
black apos/ tests/                # Código formatado
flake8 apos/ tests/               # Linting passa
git status                        # Revise o que você está fazendo commit
```

**Verificações de CI** (GitHub Actions):

- Todos os testes devem passar
- Cobertura deve ser ≥80%
- Código deve passar em black + flake8

## Arquivos Chave para Entender

**Comece aqui para entender a arquitetura**:

1. `README.md` — Visão do projeto e quick start
2. `apos/core/types.py` — Primitivos de domínio (Entity, Relationship, Node, Edge)
3. `apos/core/ontology.py` — Estrutura do modelo de ontologia
4. `apos/core/graph.py` — Operações de grafo de conhecimento
5. `apos/governance/gate.py` — Enforcement de qualidade SemanticGate
6. `tests/conftest.py` — Fixtures de teste com dados de exemplo

## Contexto de Roadmap

**Phase 1 - Scaffolding** ✅ (atual — Sprint 0.0 completo)

- ✅ Estrutura de repositório em lugar
- ✅ Type hints e docstrings definidos
- ✅ Framework de teste configurado (145 testes, 83% cobertura)
- ✅ Bootstrap Gate pattern com validators semânticos
- ✅ Release Management framework implementado
- ✅ JTBD Discovery kit validado com 7 personas

**Phase 2 - Core Implementation** (próximo — Sprint 0.1+)

- Implemente `ontology.py`, `graph.py`, `semantic.py` do código Meu PDI existente
- Escreva testes unitários (objetivo 80%+ cobertura)
- Documente API
- Implement relação Task→Feature→Release para rastreamento básico

**Phase 3 - Governance** (semana 3-4)

- Implemente portais de governança e framework de auditoria
- Testes de integração com dados reais

**Phase 4 - Semantic Layer Avançada** (Sprint 1.0+)

- **Strategic Gap (Sprint 0.0 Learning):** Rastreamento Task→Release→OKR→Métrica é invisível hoje
  - **Problema:** PMs re-explicam contexto estratégico quase diariamente; zero ferramentas conectam task/feature/release/OKR/métrica visualmente
  - **Solução APOS:** Semantic Layer com entity tracing + auto-visualization de dependências
  - **Impacto estimado:** 80% redução em overhead de "context re-explanation"
  - **Implementação:** Ontologia de OKR + relações tipadas + query engine de dependências + dashboard de rastreamento

**Phase 5 - Polish** (semana 4+)

- Implementações de loader (YAML, JSON)
- Integrações de exemplo
- Integração de agent context injection automática
- Documentação completa
- Release v0.1.0-beta → v0.2.0

## Quando Pedir Ajuda

Este é um **projeto beta em desenvolvimento ativo**. Consulte:

- `README.md` para conceitos de domínio e padrões de uso
- `docs/DEVELOPMENT.md` para diretrizes de contribuição
- GitHub Issues: <https://github.com/jadergreiner/APOS/issues>
- Contato: jadergreiner@gmail.com

## Notas para Contribuidores Futuros

- Este é um trabalho inicial. APIs podem mudar durante beta.
- A maioria dos módulos são scaffolded mas não implementados — use as docstrings como fonte de verdade para comportamento pretendido.
- O projeto Meu PDI tem implementações funcionais de módulos core; referencie esse codebase durante implementação Phase 2.
- Lógica de pontuação semântica é crítica para o valor de APOS — cobertura de teste para `semantic.py` deve ser especialmente completa.
- Portais de governança são o mecanismo de enforcement — garanta que capturem problemas de qualidade reais sem falsos positivos.
