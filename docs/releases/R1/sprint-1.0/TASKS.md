# Sprint Tasks — 1.1

**Sprint:** 1.1 - Harness Coverage + ProjectAdapter Viability  
**Status:** 📋 Planejado  
**Estimado:** ~4 dias  
**Personas:** Jader (Dev) + AI Architect

---

## Task Naming Convention

- **T{release}.{sprint}.{number}** — Task ID
  - Ex: T1.1.1, T1.1.2

---

## Tarefas

### Tier 1: Core / Must-Have

| ID | Titulo | Descricao | Duracao | Personas | Status |
|----|--------|-----------|---------|----------|--------|
| T1.1.1 | Tests agent_harness (1.587 LOC) | Escrever testes unitários para agent_harness, atingindo ≥80% de cobertura. Testes cobrem: execution, state, blocking, mocking | 1d | Jader | 📋 Planejado |
| T1.1.2 | Tests capability_harness | Escrever testes unitários + integração para capability_harness, atingindo ≥80% de cobertura. E2E: agent_harness + capability_harness ≥70% | 1d | Jader | 📋 Planejado |

### Tier 2: Important / Should-Have

| ID | Titulo | Descricao | Duracao | Personas | Status |
|----|--------|-----------|---------|----------|--------|
| T1.1.3 | Implementar ProjectAdapter core | Implementar módulo ProjectAdapter com detectores base (structure, naming, patterns, config). Classes Detector (ABC), 4 detectores concretos, ProjectAdapter.analyze() retorna ProjectProfile (Pydantic) | 1.5d | Jader | 📋 Planejado |
| T1.1.4 | Testes ProjectAdapter em Meu PDI | Validar que ProjectAdapter descobre corretamente stack e estrutura do projeto Meu PDI; coverage ≥50% de detectores. Validar: Python/FastAPI, pytest, arquivo config, estrutura src/ | 0.5d | Jader | 📋 Planejado |

---

## Progress Summary (Inicial)

| Task | Completion | Sprint Days | Notes |
|------|----------|---------|-------|
| T1.1.1 (agent_harness tests) | 0% | 1 | Harness priority |
| T1.1.2 (capability_harness tests) | 0% | 1 | Harness priority |
| T1.1.3 (ProjectAdapter core) | 0% | 1.5 | Dupla via prototype |
| T1.1.4 (ProjectAdapter Meu PDI) | 0% | 0.5 | Viability validation |
| **Total** | **0% (0/4)** | **4d** | **SPRINT INICIANDO** |

---

## Timeline Planejado

```
D1 (22 jul): T1.1.1 (agent_harness tests) + T1.1.3 (ProjectAdapter core) paralelo
D2 (23 jul): T1.1.2 (capability_harness) + continue T1.1.3. GATE: ≥70% em ambas trilhas?
D3 (24 jul): Continue trilhas conforme gate Dia 2 (dupla via ou serial)
D4-5 (25-26 jul): Refinamento + T1.1.4 (Meu PDI validation)

Meta: Harness ≥80% + ProjectAdapter ≥50% descoberta
```

---

## Dependencias

```
T1.1.1 (agent_harness) ┐
                        ├─→ T1.1.2 (capability_harness)
R0 harness (50%)  ──────┘

R0 core (graph) ─→ T1.1.3 (ProjectAdapter core) ─→ T1.1.4 (Meu PDI validation)
```

---

## Criterios de Sucesso por Tarefa

### T1.1.1 - Tests agent_harness ✅

**Deliverable:** Testes unitários em `tests/unit/test_harness/test_agent_harness.py`

**Critério de Aceite:**
- Coverage ≥80% em `apos/harness/agent_harness.py`
- Pytest `-v` passa sem warnings
- Testes cobrem: execution, state, blocking, mocking

---

### T1.1.2 - Tests capability_harness ✅

**Deliverable:** Testes unitários + integração em `tests/unit/test_harness/test_capability_harness.py`

**Critério de Aceite:**
- Coverage ≥80% em `apos/harness/capability_harness.py`
- UnitEvaluation + payload binding + mocking testados
- E2E: agent_harness + capability_harness ≥70%

---

### T1.1.3 - Implementar ProjectAdapter core ✅

**Deliverable:** Módulo `apos/project_adapter/` (8 arquivos: errors, types, detector, 4 detectores, adapter, __init__)

**Critério de Aceite:**
- Scaffold completo (type hints, docstrings)
- `ProjectAdapter.analyze(path)` executa todos 4 detectores
- `ProjectProfile` serializa para dict (`.model_dump()`)
- Testes unitários básicos (stubs ok)
- Executa contra APOS real sem erros

---

### T1.1.4 - Testes ProjectAdapter em Meu PDI ✅

**Deliverable:** Relatório de descoberta (`ProjectProfile` JSON)

**Critério de Aceite:**
- ProjectAdapter descobre ≥4 padrões em Meu PDI
- Sem erros (DetectorExecutionError, path issues)
- ProfileResult.passes() = True ou CONDITIONAL (não FAIL)
- Relatório: quais padrões detectou, quais faltaram

---

## Milestone Dia 2 — Critérios de Decisão

**Gate 16:00 Dia 2:**

- ✅ **Harness A1 ≥70% E ProjectAdapter B1 funcional** → Manter dupla via (D3-5 ambas trilhas)
- ⚠️ **Só Trilha A progrediu** → Convergir para A (harness prioritário, ProjectAdapter → Sprint 2)
- ⚠️ **Só Trilha B progrediu** → Convergir para B (KR1 prioritário, complete ProjectAdapter)
- ❌ **Nenhuma progrediu** → Pausar, reavaliar escopo

---

**Atualizado:** 2026-07-21  
**Sprint Manager:** APOS
