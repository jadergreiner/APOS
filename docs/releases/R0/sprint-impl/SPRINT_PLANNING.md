# Sprint Planning — Sprint IMPL

**Data:** 2026-07-21  
**Sprint:** IMPL — Implementacao docs → codigo  
**Periodo:** 2026-07-21 a 2026-08-04  
**Attendees:** Jader Greiner  

---

## 🎯 Goal

Converter as especificacoes de Sprint 0.5-0.7 em modulos Python importaveis via `from apos import ...`.

---

## 📋 Tasks

| ID | Modulo | SP | Jira |
|----|--------|----|------|
| IMPL-001 | `apos/context_engine/` — Context, Memory, Retrieval | 5 | SCRUM-49 |
| IMPL-002 | `apos/capabilities/` — Capability Model, Routing | 4 | SCRUM-50 |
| IMPL-003 | `apos/harness/` — Agent, Capability, Evaluation, Simulation | 5 | SCRUM-51 |

**Total: 14 SP**

---

## 🔗 Dependencias

- ✅ Sprint 0.5 docs (CONTEXT_MODEL, MEMORY_MODEL, BOUNDARIES, RETRIEVAL)
- ✅ Sprint 0.6 docs (CAPABILITY_MODEL, TAXONOMY, AGENT_MAP, ROUTING)
- ✅ Sprint 0.7 docs (HARNESS, AGENT_HARNESS, CAPABILITY_HARNESS, EVALUATION, SIMULATION)
- ✅ graph.py/types.py (KnowledgeGraph base)

---

**Sprint Planning criado:** 2026-07-21  
**Jira:** Sprint IMPL (id=7), SCRUM-49 a 51
