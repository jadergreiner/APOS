# APOS Roadmap: R1-R4 (2026-2027)

**Release:** R0 → R1-R4  
**Período:** Out 2026 - Jun 2027  
**Status:** REVISADO (pós-Sprint 0.7)  
**Criado:** 20-07-2026 (Template)  
**Revisado:** 21-07-2026 (Sprint 0.7)

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

## Visão Estratégica

Cada release move em direção ao North Star: **"Times visualizam e raciocinam sobre estratégia de ponta a ponta"**

```
R0 (Jul-Set 2026): Fundações semânticas + MVP ✅
    ↓
R1 (Out-Nov 2026): Instanciar Knowledge Graph + Loaders MCP
    ↓
R2 (Dez 2026-Fev 2027): Catálogo + Linhagem + Inteligência
    ↓
R3 (Fev-Abr 2027): Governança + Auditoria + Compliance
    ↓
R4 (Abr-Jun 2027): Ecossistema + Comunidade + Go-to-Market
```

**Ajuste pós-R0:** O escopo de R1-R3 foi reduzido porque ~30% do que era planejado já foi
entregue como design/fundação em R0. O foco agora é **implementação real + carga real**.

---

## R1: Instanciação + Transporte (Out-Nov 2026)

**Objetivo:** Instanciar knowledge graph com dados reais via loaders MCP, conectando Jira/Notion/Slack

**Key Results:**
- KR1: 3 loaders MCP funcionais (Jira, Notion, Slack)
- KR2: Knowledge graph com 100+ entidades instanciadas de projetos reais
- KR3: Agentes conseguem navegar grafo usando query patterns Q01-Q16

**Temas de Sprint:**
- S1.0: **Jira MCP Loader** — refatorar sync TASKS.md → Jira para loader MCP bidirecional; instanciar 50+ entidades Task/Feature/Release no KG
- S1.1: **MCP Server** — servidor MCP para APOS expor KG + queries Q01-Q16 como tools para agentes externos
- S1.2: **Notion Loader** — loader MCP para Notion (projetos, documentação, OKRs); instanciar 30+ entidades
- S1.3: **Slack Loader + Data Load** — loader MCP para Slack (decisões, contextos); carga total 100+ entidades

**O que NÃO está mais em R1** (já foi entregue em R0):
- Knowledge Graph core (graph.py) ✅ Sprint 0.4
- Query patterns Q01-Q16 ✅ Sprint 0.4
- Agent navigation design ✅ Sprint 0.6

**Effort:** ~18 person-days  
**Dependencies:**
- R0 COMPLETE (fundações — em progresso)
- Sprint 0.4 KG design (✅ já disponível)
- Sprint 0.5 Retrieval Strategy (✅ já disponível)

---

## R2: Inteligência + Rastreabilidade (Dez 2026-Fev 2027)

**Objetivo:** Catálogo + Linhagem + Impact Analysis operacional

**Key Results:**
- KR1: Catálogo com schema formal e linhagem completa entre entidades
- KR2: Impact analysis CLI em < 5 min (vs 2h manual)
- KR3: Agentes executam queries semânticas com fallback e cache funcional

**Temas de Sprint:**
- S2.0: **Data Catalog Schema** — schema formal de catálogo (tipos, atributos, indexação); API de busca + descoberta
- S2.1: **Lineage Tracing Engine** — rastreio de linhagem entre Task → Feature → Release → OKR com propagação de mudanças
- S2.2: **Impact Analysis CLI** — CLI que calcula impacto de mudanças usando queries Q09-Q12; output estruturado
- S2.3: **Capability Routing Implementation** — implementar o algoritmo de resolução de CAPABILITY_ROUTING.md; chain, fallback, cache real

**O que NÃO está mais em R2** (já foi entregue em R0):
- Agent Navigation Harness design ✅ Sprint 0.7 (AGENT_HARNESS.md)
- Capability model design ✅ Sprint 0.6 (CAPABILITY_MODEL.md)
- Agent Map + Matriz ✅ Sprint 0.6 (AGENT_MAP.md)
- Capability Routing design ✅ Sprint 0.6 (CAPABILITY_ROUTING.md)

**Effort:** ~20 person-days  
**Dependencies:**
- R1 loaders operacionais (dados reais no KG)
- R1 MCP Server (para agentes consumirem)

---

## R3: Governança + Auditoria (Fev-Abr 2027)

**Objetivo:** Validação automática + Auditoria + Observabilidade

**Key Results:**
- KR1: Semantic Gates implementados bloqueiam 95% de desalinhamentos
- KR2: Audit Engine rastreia todas violações com diagnóstico
- KR3: Trust Score tracking + dashboard de observabilidade

**Temas de Sprint:**
- S3.0: **Semantic Gates Implementation** — implementar gates baseados em EVALUATION_HARNESS.md; PASS/CONDITIONAL/FAIL com thresholds configuráveis
- S3.1: **Audit Rules + Log Engine** — engine de auditoria que rastreia desvios, categoriza issues e gera diagnósticos acionáveis
- S3.2: **Compliance Framework** — frameworks de compliance (LGPD, SOC 2); regras configuráveis por domínio
- S3.3: **Observability Dashboard** — dashboard com Trust Score tracking, métricas de coverage, tendências, alertas

**O que NÃO está mais em R3** (já foi entregue em R0):
- Evaluation Harness design ✅ Sprint 0.7 (5 tipos, 16 métricas, A/B testing)
- Trust Score Engine ✅ Sprint 0.3 (0.0-1.0, três dimensões)
- Métricas baseline ✅ Sprint 0.3

**Effort:** ~20 person-days  
**Dependencies:**
- R2 catalog + lineage (gates dependem de linhagem)
- Sprint 0.7 Evaluation Harness design (✅ já disponível)

---

## R4: Ecossistema + Comunidade (Abr-Jun 2027)

**Objetivo:** Open source + SDK + Extensibilidade

**Key Results:**
- KR1: 10+ extensões comunitárias
- KR2: 1000+ downloads (PyPI)
- KR3: "Ontologia de PM" como padrão de mercado

**Temas de Sprint:**
- S4.0: **SDK Público + Documentação** — SDK Python público com extensão points, plugin architecture, contribution guide
- S4.1: **Extensões de Domínio** — Sales, Support, Finance ontologies como pacotes instaláveis
- S4.2: **Shared Ontology Library** — repositório comunitário de ontologias compartilhadas; sistema de review + versionamento
- S4.3: **Go-to-Market + Comunidade** — landing page, pricing, case studies, webinars, open source community

**Effort:** ~18 person-days  
**Dependencies:**
- R1-R3 estáveis
- R2 MCP Server maduro
- R3 gates + audit operacionais

---

## Timeline Visual (Gantt Simplificado)

```
2026:
  JUL-AGO |████ R0.0-0.3 Sprint ████ R0.4-0.7 Sprint ████ | (Sprint 0.0-0.7)
  SET     |█ R0.8-0.9 ██ | (R0 encerramento)
  ────────|─── R0.5-0.7 IMPL ◄── ~14d para virar codigo importavel
  OUT     |  ████ S1.0 ████ S1.1 ████ | (R1 — loaders)
  NOV     | ████ S1.2 ████ S1.3 ████ | (R1)
  DEZ     | ████ S2.0 ████ S2.1 ████ | (R2)

2027:
  JAN     | ████ S2.2 ████ S2.3 ████ | (R2)
  FEV     | ████ S3.0 ████ S3.1 ████ | (R3)
  MAR     | ████ S3.2 ████ S3.3 ████ | (R3)
  ABR     | ████ S4.0 ████ S4.1 ████ | (R4)
  MAI     | ████ S4.2 ████ S4.3 ████ | (R4)
  JUN     | ✅ COMPLETE
```

> **⚠ Nota:** A implementacao dos modulos `apos/context_engine/`, `apos/capabilities/` e `apos/harness/` (docs → codigo) esta marcada como pre-requisito implicito antes de R1. Sem ela, `pip install apos` nao entrega as competencias de Sprint 0.5-0.7 como codigo importavel. Pode ser executada em paralelo com R0.8-0.9 ou como sprint dedicada de implementacao.

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
