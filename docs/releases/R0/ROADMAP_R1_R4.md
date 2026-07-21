# APOS Roadmap: R1-R4 (2026-2027)

**Release:** R0 → R1-R4  
**Período:** Out 2026 - Jun 2027  
**Status:** REPOSICIONADO (ponto de inflexao — APOS como framework projeto-consciente)  
**Criado:** 20-07-2026 (Template)  
**Revisado:** 21-07-2026 (Ponto de inflexao — APOS para de se autogerir)

---

## 🧭 Ponto de Inflexao Estrategico

**Problema identificado:** APOS passou 7 sprints se autodesenvolvendo — seus proprios OKRs, sprints, KG, capabilities, roadmap. Mas seu proposito nunca foi ser um projeto em si.

**Correcao:** APOS deve ser um framework que, ao ser importado, aprende sobre o **projeto hospedeiro** (ex: Meu PDI) e aplica suas competencias a ele — nao a si mesmo.

```
ANTES (autorreferente)                     DEPOIS (projeto-consciente)
───────────────────────────────            ───────────────────────────────
from apos import SprintManager             from apos import ProjectAdapter
sm = SprintManager("R0")                   projeto = ProjectAdapter()
sm.create_sprint("sprint-0.8")             projeto.load("meu-pdi")
# APOS gerencia APOS                       # APOS gerencia o projeto
```

**Isso reposiciona todo o roadmap de R1 em diante.**

---

---

## Status de Deliverables vs R0

O roadmap original R1-R4 foi criado na Sprint 0.1. Desde então, as Sprints 0.3-0.7 entregaram
parte significativa do escopo originalmente planejado para R1, R2 e R3.
A tabela abaixo mostra o que mudou.

| Item Planejado | Originalmente em | Status | Onde foi entregue |
|----------------|------------------|--------|-------------------|
| Knowledge Graph Executor (núcleo CRUD) | R1 / S1.0 | ✅ **JÁ ENTREGUE** | Sprint 0.4: `graph.py` + `types.py` (84 testes, 100% coverage) |
| Knowledge Graph Design (node/edge types) | R1 / S1.0 | ✅ **JÁ ENTREGUE** | Sprint 0.4: KNOWLEDGE_GRAPH.md, NODE_TYPES.md, EDGE_TYPES.md |
| Query Patterns (traversal, impacto, órfãos) | R1 / S1.2 | ✅ **JÁ ENTREGUE** | Sprint 0.4: QUERY_PATTERNS.md (16 padrões Q01-Q16) |
| Agent Navigation (design) | R2 / S2.3 | ✅ **JÁ ENTREGUE (design)** | Sprint 0.6: AGENT_MAP.md + CAPABILITY_ROUTING.md |
| Agent/Capability Harness (design) | R2 / S2.3 | ✅ **JÁ ENTREGUE (design)** | Sprint 0.7: AGENT_HARNESS.md + CAPABILITY_HARNESS.md |
| Evaluation Harness (design) | R3 / S3.x | ✅ **JÁ ENTREGUE (design)** | Sprint 0.7: EVALUATION_HARNESS.md (5 tipos, 16 métricas) |
| Trust Score Engine | R1/R2 (implícito) | ✅ **JÁ ENTREGUE** | Sprint 0.3: Trust Score 0.0-1.0 (coverage, quality, consistency) |
| Métricas Baseline | R2/R3 (implícito) | ✅ **JÁ ENTREGUE** | Sprint 0.3: METRICS_BASELINE.md + tracking |
| Jira Sync (TASKS.md → Jira) | R1 / S1.1 | ✅ **JÁ ENTREGUE (parcial)** | Sprint 0.3: Jira sync automático (plugin, não loader MCP) |
| Capability Model (design) | R2 (implícito) | ✅ **JÁ ENTREGUE (design)** | Sprint 0.6: CAPABILITY_MODEL.md + CAPABILITY_TAXONOMY.md |
| Context Model | — | ✅ **JÁ ENTREGUE** | Sprint 0.5: CONTEXT_MODEL.md + MEMORY_MODEL.md + CONTEXT_BOUNDARIES.md + RETRIEVAL_STRATEGY.md |
| Simulation Harness (design) | — | ✅ **JÁ ENTREGUE (design)** | Sprint 0.7: SIMULATION_HARNESS.md (5 tipos) |

## O que AINDA NÃO foi entregue (e PRECISA ser implementado como codigo)

### Implementacao obrigatoria antes de R1

As Sprints 0.5-0.7 entregaram **especificacoes em markdown**, mas NAO codigo importavel.
Um projeto que fizer `pip install apos` hoje NAO recebe Context Engine, Capability Model ou Harness.

| Documento | Status | Precisa virar modulo | Estimativa |
|-----------|--------|---------------------|-----------|
| CONTEXT_MODEL.md + MEMORY_MODEL.md | 📋 design feito | `apos/context_engine/` | 3d |
| CONTEXT_BOUNDARIES.md + RETRIEVAL_STRATEGY.md | 📋 design feito | `apos/context_engine/` | 2d |
| CAPABILITY_MODEL.md + CAPABILITY_TAXONOMY.md | 📋 design feito | `apos/capabilities/` | 2d |
| AGENT_MAP.md + CAPABILITY_ROUTING.md | 📋 design feito | `apos/capabilities/` | 2d |
| HARNESS.md + AGENT_HARNESS.md | 📋 design feito | `apos/harness/` | 2d |
| CAPABILITY_HARNESS.md + EVALUATION_HARNESS.md | 📋 design feito | `apos/harness/` | 2d |
| SIMULATION_HARNESS.md | 📋 design feito | `apos/harness/` | 1d |
| **Total** | | | **~14d** |

### Demais entregas pendentes (R1-R4)

- **Loaders reais** (MCP): Jira (temos sync, não loader), Notion, Slack
- **MCP Server / protocol** para agentes externos
- **Instanciação de 100+ entidades** no Knowledge Graph (temos o motor, não os dados)
- **Data Catalog** (schema formal de catálogo)
- **Lineage Tracing** (rastreio de linhagem entre entidades)
- **Impact Analysis CLI** (ferramenta de impacto)
- **Semantic Gates** implementados (só design)
- **Audit Rules + Log Engine** (só design)
- **Compliance Frameworks** (não iniciado)
- **Observability Dashboard** (não iniciado)
- **SDK Público** (não iniciado)
- **Extensões de Domínio / Comunidade** (não iniciado)

---

## Visão Estratégica (Reposicionada)

Cada release move em direção ao North Star: **"Times visualizam e raciocinam sobre estratégia de ponta a ponta"**

A diferença: quem "visualiza e raciocina" nao é o APOS sobre si mesmo — é o **projeto hospedeiro** usando APOS como framework.

```
R0 (Jul-Set 2026): Fundações semanticas + MVP (autodesenvolvimento) ✅
    │  APOS aprendeu sobre si mesmo para poder ensinar outros.
    │  Conhecimento adquirido: KG, Context, Capabilities, Harness.
    ↓
R1 (Out-Nov 2026): Project Adapter — APOS aprende sobre o PROJETO
    │  from apos import ProjectAdapter
    │  adapter = ProjectAdapter()
    │  adapter.discover("meu-pdi")  # descobre stack, dominio, OKRs, times
    ↓
R2 (Dez 2026-Fev 2027): Domain KG — KG do dominio do projeto
    │  adapter.kg.add_node(domain_entity)
    │  adapter.ceremonies.sprint_planning()
    ↓
R3 (Fev-Abr 2027): Project Governance — Gates + Audit para o projeto
    │  adapter.governance.validate_alignment()
    ↓
R4 (Abr-Jun 2027): Framework SDK — projetos empacotam APOS como dependencia
    │  pip install apos
    │  apos init meu-pdi  # setup automatico
```

**Ajuste pos-ponto de inflexao:** TODO o escopo de R1-R4 foi recalibrado.
Nao se trata mais de "APOS construir seus loaders". Trata-se de APOS **servir** projetos.

---

## R1: Project Adapter — APOS aprende sobre o PROJETO (Out-Nov 2026)

**Objetivo:** Criar o `ProjectAdapter` — camada que, ao ser importada, descobre o contexto do projeto hospedeiro e configura APOS para servi-lo.

```
# Visao de uso final
from apos import ProjectAdapter

adapter = ProjectAdapter()
adapter.discover()  
# → Detecta: pyproject.toml, CLAUDE.md, docs/, tests/
# → Infere: stack (FastAPI/Django/Next.js), dominio, OKRs
# → Sugere: ontologia adaptada ao dominio
# → Configura: ceremonies, KG, capabilities para o projeto
```

**Key Results:**
- KR1: `ProjectAdapter.discover()` analisa repositorio e extrai stack, dominio, estrutura
- KR2: Bootstrap Gate 2.0 guia projeto na definicao de fundacoes (NORTH_STAR, OKR, ONTOLOGY)
- KR3: Ontologia geral do APOS e adaptada ao vocabulario do projeto (ex: "Aluno" em vez de "Persona")
- KR4: `from apos import SprintManager` usa configuracoes do projeto, nao do APOS

**Temas de Sprint:**
- S1.0: **ProjectAdapter core** — discover() que analisa repositorio (pyproject.toml, docs, CLAUDE.md)
- S1.1: **Bootstrap Gate 2.0** — init guiado por contexto do projeto (nao generico)
- S1.2: **Domain Ontology Adapter** — mapeia ontologia generica para vocabulario do projeto
- S1.3: **Config Profiles** — perfis de configuracao (solo dev, squad, enterprise)

**O que NAO esta mais em R1** (reposicionado):
- Loaders MCP (Jira, Notion, Slack) → movido para R2 (projeto pode usar se precisar)
- MCP Server → movido para R2

**Effort:** ~18 person-days  
**Dependencies:**
- R0 COMPLETE (fundacoes — em progresso)
- Conhecimento adquirido em Sprints 0.4-0.7 (KG, Context, Capabilities, Harness) — disponivel como especificacao

---

## R2: Domain KG + Project Ceremonies (Dez 2026-Fev 2027)

**Objetivo:** Knowledge Graph e cerimonias operando para o dominio do projeto, nao do APOS.

**Key Results:**
- KR1: Projeto consegue instanciar entidades de seu dominio no KG (ex: "Aluno", "Curso", "Mentoria")
- KR2: Sprint Planning e Daily usam dados reais do projeto, nao templates genericos
- KR3: Cerimonias adaptadas ao ritmo do projeto (solo, squad, OKR-cycle)
- KR4: Loaders MCP opcionais (Jira/Notion/Slack) disponiveis se projeto quiser conectar

**Temas de Sprint:**
- S2.0: **Domain Knowledge Graph** — adapter.kg.add_domain_entity("Aluno") cria no com atributos do projeto
- S2.1: **Project Ceremonies** — Sprint Planning, Daily, Review, Retro com dados do projeto
- S2.2: **MCP Loaders (opcionais)** — Jira, Notion, Slack loaders (se projeto usar essas ferramentas)
- S2.3: **Capability Routing real** — implementar CAPABILITY_ROUTING.md para o dominio do projeto

**O que NAO esta mais em R2** (ja entregue em R0):
- Agent Navigation design ✅ Sprint 0.6
- Capability model design ✅ Sprint 0.6
- Agent Map + Routing design ✅ Sprint 0.6

**Effort:** ~20 person-days  
**Dependencies:**
- R1 ProjectAdapter funcional
- Sprint 0.4-0.7 designs como especificacao disponivel

---

## R3: Project Governance (Fev-Abr 2027)

**Objetivo:** Gates, auditoria e compliance operando para o projeto, nao para o APOS.

**Key Results:**
- KR1: Semantic Gates validam alinhamento das entregas do projeto com seus OKRs
- KR2: Audit Engine rastreia decisoes do projeto com diagnostico
- KR3: Trust Score mede saude semântica do projeto (cobertura, qualidade, consistencia)

**Temas de Sprint:**
- S3.0: **Project Gates** — gates configurados para o dominio do projeto (gates de ontologia, alinhamento, cobertura)
- S3.1: **Project Audit** — auditoria rastreia decisoes do projeto, nao do APOS
- S3.2: **Trust Score Dashboard** — dashboard com metricas do projeto (nao de APOS)
- S3.3: **Compliance Templates** — LGPD, SOC 2 templates adaptaveis ao projeto

**O que NAO esta mais em R3** (ja entregue em R0):
- Evaluation Harness design ✅ Sprint 0.7
- Trust Score Engine ✅ Sprint 0.3
- Metricas baseline ✅ Sprint 0.3

**Effort:** ~20 person-days  
**Dependencies:**
- R2 Domain KG populado com dados do projeto
- Sprint 0.7 Evaluation Harness design (disponivel como especificacao)

---

## R4: Framework SDK — APOS como dependencia de projetos (Abr-Jun 2027)

**Objetivo:** Projetos empacotam APOS como dependencia (`pip install apos`) e rodam `apos init` para configuracao automatica.

**Key Results:**
- KR1: `pip install apos` + `apos init meu-projeto` configura tudo automaticamente
- KR2: SDK publico com extension points para qualquer projeto
- KR3: 5+ projetos usando APOS como framework de gestao semantica

**Temas de Sprint:**
- S4.0: **CLI + Init** — `apos init <projeto>` detecta, configura e bootstrappa
- S4.1: **Extension Points** — plugins de dominio (Educacao, Saude, Financas) como pacotes instalaveis
- S4.2: **Documentation + Quickstart** — docs focadas no projeto, nao no APOS
- S4.3: **Community + Case Studies** — Meu PDI como primeiro caso de uso documentado

**O que NAO esta mais em R4** (reposicionado):
- "Ontologia de PM como padrao de mercado" → nao é mais o objetivo. O objetivo é APOS como framework adaptavel a qualquer dominio.

**Effort:** ~18 person-days  
**Dependencies:**
- R1-R3 estaveis
- Meu PDI como projeto piloto validando o fluxo completo

---

## Timeline Visual (Gantt Simplificado) — Reposicionado

```
2026:
  JUL-AGO |████ R0.0-0.7 (autodesenvolvimento) ████ | ✅
  SET     |█ R0.8-0.9 + implementacao 0.5-0.7 em code ██ |
  ────────|─── Transicao: APOS para de se autogerir ─────
  OUT     |  ████ S1.0 ████ S1.1 ████ | (R1 — ProjectAdapter)
  NOV     | ████ S1.2 ████ S1.3 ████ | (R1)
  DEZ     | ████ S2.0 ████ S2.1 ████ | (R2 — Domain KG + Ceremonies)

2027:
  JAN     | ████ S2.2 ████ S2.3 ████ | (R2)
  FEV     | ████ S3.0 ████ S3.1 ████ | (R3 — Project Governance)
  MAR     | ████ S3.2 ████ S3.3 ████ | (R3)
  ABR     | ████ S4.0 ████ S4.1 ████ | (R4 — Framework SDK)
  MAI     | ████ S4.2 ████ S4.3 ████ | (R4)
  JUN     | ✅ FRAMEWORK PRONTO
```

> **⚠ Nota:** A implementacao dos modulos `apos/context_engine/`, `apos/capabilities/` e `apos/harness/` (docs → codigo) esta marcada como pre-requisito implicito antes de R1. Sem ela, `pip install apos` nao entrega as competencias de Sprint 0.5-0.7 como codigo importavel. Pode ser executada em paralelo com R0.8-0.9 ou como sprint dedicada de implementacao.

> **⚠ Ponto de inflexao:** A partir de R1, APOS nao gerencia mais a si mesmo. O `ProjectAdapter` gerencia o projeto hospedeiro. O roadmap deixa de ser "o que APOS precisa construir" e passa a ser "o que APOS oferece a projetos".

---

## Caminho Crítico

**Série:** R0 → R1 → R2 → R3 → R4 (dependência linear)

**Pontos de Risco:**
1. **R1 loaders complexity** — integração com APIs externas (Jira, Notion, Slack) pode ter atritos de auth/rate-limit. Mitigação: paralelização S1.0-1.2
2. **R1 data instanciação** — 100+ entidades reais requer dados de qualidade. Mitigação: seed data via Jira sync existente (Sprint 0.3)
3. **R2 lineage tracing** — propagação correta entre tipos de entidade é não-trivial. Mitigação: EDGE_TYPES.md já define 10 tipos de aresta com regras de propagação
4. **R3 gates sem dados reais** — gates precisam de KG populado para validação. Mitigação: R1 data load é pré-requisito

---

## Restrições de Recursos

**Capacity:** 1 persona (Jader + Claude Sonnet 5)

**Distribuição:**
- R1-R4: ~76 person-days total (~18-20 person-days/release)
- Timeline: 36 semanas (~9 meses) de Out 2026 a Jun 2027
- Paralelização: Loaders (S1.0-1.2) podem ser paralelos (~15% economia)
- R0 absorveu ~30% do escopo original de R1-R3, liberando capacidade para aprofundamento

**Pressupostos:**
- Velocity 1.5x (validado: Sprints 0.3-0.7 entregaram 5 sprints de design em ~2 semanas)
- Buffer de 20-30% para riscos imprevistos
- Sem context switching significativo entre releases

---

## Métricas de Sucesso

| Release | Métrica-Chave | Target | Validação |
|---------|---------------|--------|-----------|
| **R1** | 3 loaders MCP operacionais | 100% | Testes de integração + 100+ entidades |
| **R1** | Knowledge Graph populado | 100+ entidades | `kg.stats()` |
| **R2** | Impact analysis latency | < 5 min | Benchmark suite |
| **R2** | Capability routing funcional | 3+ chains | Testes de integração |
| **R3** | Semantic Gates blocking rate | 95% | Audit logs |
| **R3** | Trust Score tracking | Dashboard ao vivo | Métricas históricas |
| **R4** | Community extensions | 10+ | GitHub contributions |
| **R4** | SDK downloads | 1000+ | PyPI stats |

---

## Decisões Arquiteturais (Atualizadas)

### Implementação em Fases

1. **R1:** Loaders MCP + KG populado (motor já existe do R0)
2. **R2:** Catalog schema + Lineage + Capability routing real
3. **R3:** Governance implementado (design já existe do R0)
4. **R4:** Extensibilidade via plugins + SDK

### Priorização de Loaders

| Loader | Sprint | Porquê |
|--------|--------|--------|
| **Jira MCP** | S1.0 | Já temos sync (Sprint 0.3), refatorar para loader MCP é menor esforço |
| **Notion** | S1.2 | Documentação de produto + OKRs |
| **Slack** | S1.3 | Decisões de equipe + contexto social |

### MCP como Protocolo Padrão

Todos os loaders em R1 serão expostos via **MCP Server** (S1.1), permitindo que agentes
externos (Claude, Codex, etc.) consultem o KG nativamente via tools MCP.

---

## Go-to-Market Timeline

| Milestone | Timing | Atividade |
|-----------|--------|-----------|
| **Beta Interno** | R1 end | KG populado com dados reais; 3 loaders operacionais |
| **Alpha** | R2 end | Impact Analysis + Capability Routing; 5-10 early adopters |
| **Beta Público** | R3 end | Governance + Audit + Dashboard; invite 20-50 usuários |
| **GA** | R4 end | SDK público + Community + Go-to-Market |

---

## Próximas Etapas

- [X] Sprint 0.1 (T0.1.4): Roadmap original criado (template)
- [X] Sprint 0.3-0.7: KG, Context, Capability, Harness entregues em R0
- [ ] Sprint 0.8-0.9: Refinamento R1-R4 com base na revisão atual
- [ ] Pós-R0: Aprovação formal + kickoff R1 (S1.0: Jira MCP Loader)
- [ ] R1: Validar roadmap contra carga real de dados

---

**Versão:** 2.0 (Revisado pós-Sprint 0.7)  
**Próximo Review:** Sprint 0.9 (refinement com dados reais de R0)
