# APOS R0 Sprint Plan — Atualizado

**Release:** R0 (APOS Foundations)  
**Sprints:** 0.0 - 0.9  
**Duracao Total:** 10 semanas (2026-07-22 a 2026-09-30)  
**Status:** ✅ Sprint 0.0 → Sprint 0.3 CONCLUIDAS — SHIP MVP  
**Lead Skill:** PM-Skills

---

## Visão Estratégica de R0

R0 estabelece todas as **fundações do APOS** através do Skill Council (11 skills).

**North Star:** 100% das capabilities possuem representação semântica oficial derivando de uma única fonte de verdade.

---

## Sprint Overview — Estado Real vs Planejado

| Sprint | Tema Original | Tema Real | Status | 
|--------|--------------|-----------|--------|
| **0.0** | Knowledge Consolidation | Knowledge Consolidation | ✅ COMPLETE (25f3474) |
| **0.1** | Platform Identity | Platform Identity | ✅ COMPLETE (d14f7c8) |
| **0.2** | Ontology | **JTBD Deep Dive** ↻ | ✅ COMPLETA (pivot p/ validacao) |
| **0.3** | Semantic Layer | **Beta Prep — MVP** ↻ | ✅ COMPLETA — SHIP MVP |
| **0.4** | Knowledge Graph | Knowledge Graph | 📅 PLANNED |
| **0.5** | Context Engineering | Context Engineering | 📅 PLANNED |
| **0.6** | Capability Modeling | Capability Modeling | 📅 PLANNED |
| **0.7** | Harness | Harness | 📅 PLANNED |
| **0.8** | Governance | Governance | 📅 PLANNED |
| **0.9** | Agent Contracts | Agent Contracts | 📅 PLANNED |

---

### Sprint 0.0: Knowledge Consolidation ✅ COMPLETE

**Period:** 2026-07-19 (1 day, +250% velocity!)  
**Lead Skill:** JTBD Framework + Bootstrap Gate Implementation  
**Goal:** Validar o job real que APOS resolve + implementar 3 componentes core

**Tier 1 Deliverables (Core Implementation):**

- ✅ `apos/bootstrap/gate.py` — BootstrapGate com validators semânticos
- ✅ `apos/bootstrap/validators/` — 3 validators (Strategy, Ontology, Governance) com 85%+ coverage
- ✅ `apos/bootstrap/session.py` — SessionManager + Foundation Definition Session
- ✅ `apos/__main__.py` — CLI: `python -m apos init`
- ✅ `apos/kernel/commit_tracking.py` — CommitTrackingValidator (Phase 1-3)
- ✅ Tests: 145 testes passando, 83% cobertura

**Tier 2 Deliverables (JTBD Discovery):**

- ✅ `JTBD-INTERVIEWS-RAW-NOTES.md` — 7 personas entrevistadas (Jader + 6 roleplay)
- ✅ `FORCES_ANALYSIS.md` — Matriz Push/Pull/Ansiedade/Hábito consolidada
- ✅ `JOB_STATEMENT.md` — Job Statement final validado com 100% consenso

**Status:** ✅ **COMPLETO** ([Relatório Completo](sprint-0.0/README.md))

---

### Sprint 0.1: Platform Identity ✅ COMPLETE

**Period:** 2026-07-19 (1 dia)  
**Goal:** Definir identidade, proposta, posicionamento de APOS

**Deliverables:**
- VALUE_PROPOSITION.md — Proposta de valor final
- COMPETITIVE_POSITIONING.md — Diferenciação competitiva
- OKR.md — OKRs de Produto R0-R4
- ROADMAP_R1_R4.md — Plano de releases

**Status:** ✅ **COMPLETO** (d14f7c8)

---

### Sprint 0.2: JTBD Deep Dive ✅ COMPLETA (Pivot Estratégico)

**Period:** 2026-07-20 (1 dia sprint agil)  
**Pivot:** Originalmente "Ontology", re-planejado para validacao mais profunda com stakeholders reais  
**Goal:** 6 entrevistas JTBD documentadas, forças analysis, validação VALUE_PROPOSITION

**Deliverables:**
- ✅ 6 entrevistas JTBD documentadas (5 personas + Jader PM)
- ✅ FORCES_ANALYSIS.md — Matriz completa
- ✅ JOB_STATEMENT.md — Formalizado + validado
- ✅ BETA_PROGRAM.md — Programa piloto MVP
- ✅ VALUE_PROPOSITION: 4.5/5 validado (VERY STRONG)

**Status:** ✅ **COMPLETA** — Decisao: VERDE, proceder MVP

---

### Sprint 0.3: Beta Prep — MVP Implementation ✅ COMPLETA

**Period:** 2026-07-22 a 2026-07-29 (sprint de execucao)  
**Pivot:** Originalmente "Semantic Layer", re-planejado para implementar MVP  
**Goal:** Entregar MVP funcional — Plugin Jira, Trust Score Engine, Piloto, Metricas

**Deliverables:**
- ✅ T0.3.1 SPEC.md — Especificação técnica
- ✅ T0.3.2 API_DESIGN.md — Design de API REST (6 endpoints)
- ✅ T0.3.3 Plugin Jira — Sincronização automática TASKS.md → Jira
- ✅ T0.3.4 Trust Score Engine — Cálculo 0.0-1.0 (coverage, quality, consistency)
- ✅ T0.3.5 Piloto Setup — Scripts, onboarding, personas
- ✅ T0.3.6 Metricas Baseline — Setup monitoring + coleta
- ✅ T0.3.7 Documentação MVP — README, API docs, tutorial
- ✅ T0.3.8 Testing + QA — Validação final

**Resultado:** 🟢 **GREEN — SHIP MVP**  
**Commits:** 30+ na branch develop  
**Status:** ✅ **COMPLETA** ([Sprint 0.3](sprint-0.3/README.md))

---

### Sprint 0.4: Knowledge Graph (Proximo)

**Period:** (A definir)  
**Lead Skill:** Knowledge Graph Design  
**Goal:** Projetar modelo de grafo conectado

**Deliverables:**
- KNOWLEDGE_GRAPH.md (modelo de grafo)
- NODE_TYPES.md (tipos de nós)
- EDGE_TYPES.md (tipos de arestas)
- QUERY_PATTERNS.md (padrões de navegação)

**Effort:** 5 person-days  
**Status:** 📅 PLANNED

---

### Sprint 0.5: Context Engineering

**Period:** (A definir)  
**Lead Skill:** Context Engineering  
**Goal:** Modelar contexto e memória de APOS

**Deliverables:**
- CONTEXT_MODEL.md (modelo de contexto)
- MEMORY_MODEL.md (modelo de memória)
- CONTEXT_BOUNDARIES.md (fronteiras de contexto)
- RETRIEVAL_STRATEGY.md (estratégia de recuperação)

**Effort:** 5 person-days  
**Status:** 📅 PLANNED

---

### Sprint 0.6: Capability Modeling

**Period:** (A definir)  
**Lead Skill:** Agentic Architecture  
**Goal:** Modelar capabilities e mapear agentes

**Deliverables:**
- CAPABILITY_MODEL.md (modelo de capabilities)
- CAPABILITY_TAXONOMY.md (taxonomia de capabilities)
- AGENT_MAP.md (mapa de agentes)
- CAPABILITY_ROUTING.md (roteamento de capabilities)

**Effort:** 5 person-days  
**Status:** 📅 PLANNED

---

### Sprint 0.7: Harness

**Period:** (A definir)  
**Lead Skill:** Harness Design  
**Goal:** Projetar harness de agentes, capabilities, avaliação e simulação

**Deliverables:**
- HARNESS.md (especificação de harness)
- AGENT_HARNESS.md (harness de agentes)
- CAPABILITY_HARNESS.md (harness de capabilities)
- EVALUATION_HARNESS.md (harness de avaliação)
- SIMULATION_HARNESS.md (harness de simulação)

**Effort:** 6 person-days  
**Status:** 📅 PLANNED

---

### Sprint 0.8: Governance

**Period:** (A definir)  
**Lead Skill:** AI Governance  
**Goal:** Estruturar governança, avaliações e observabilidade

**Deliverables:**
- GOVERNANCE.md (framework de governança)
- EVALUATIONS.md (avaliações de capabilities)
- OBSERVABILITY.md (estratégia de observabilidade)
- COMPLIANCE.md (requisitos de compliance)
- AUDIT_FRAMEWORK.md (framework de auditoria)

**Effort:** 6 person-days  
**Status:** 📅 PLANNED

---

### Sprint 0.9: Agent Contracts

**Period:** (A definir)  
**Lead Skill:** Agentic Architecture  
**Goal:** Especificar contratos de agentes

**Deliverables:**
- AGENT_CONTRACTS.md (contrato de agentes)
- CONTRACT_SPEC.md (especificação técnica)
- INTERFACE_DEFINITIONS.md (definições de interface)
- EXECUTION_PROTOCOL.md (protocolo de execução)

**Effort:** 5 person-days  
**Status:** 📅 PLANNED

---

## Definition of Done (R0 Complete)

R0 é COMPLETE quando:

- ✅ 0.0: Job validado com stakeholder sign-off
- ✅ 0.1: North Star, OKRs, Roadmap R1-R4 finalizados
- ✅ 0.2: JTBD validado com 6 entrevistas reais (pivot estrategico)
- ✅ 0.3: MVP implementado e validado (SHIP MVP)
- 📅 0.4: Grafo knowledge especificado (pronto para implementação R1)
- 📅 0.5: Contexto e memória modelados
- 📅 0.6: Capabilities mapeadas, agentes categorizados
- 📅 0.7: Harness especificado (4 tipos)
- 📅 0.8: Governança, avaliações, observabilidade definidas
- 📅 0.9: Contratos de agentes especificados

---

**Created:** 2026-07-19  
**Updated:** 2026-07-21 — Sprint 0.3 completa SHIP MVP  
**Next:** Sprint 0.4 (Knowledge Graph) ou R1 planning
