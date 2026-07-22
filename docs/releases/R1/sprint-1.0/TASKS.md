# Sprint Tasks — 1.1

**Sprint:** 1.1 - Harness Coverage + ProjectAdapter Viability  
**Status:** 📋 Planejado (Decisão Executiva CEO integrada)
**Estimado CORE:** 3.5 SP (era 4 SP) | **STRETCH:** +1.0 SP polish  
**Velocity baseline:** 0.7 SP/dia (50% redução vs R0, devido refator + dupla via overhead)
**Personas:** Jader (Dev) + AI Architect + SME (validação)

---

## ⚠️ PRÉ-REQUISITO: Refatoração Meu PDI

**Task ID:** T1.1.0 (pré-sprint)

| Aspecto | Detalhe |
|---------|---------|
| **Timing** | Dia 1, 2026-07-22, 09:00-12:00 BLOQUEANTE |
| **Escopo** | Remove /docs/knowledge/ duplicidade, reorganiza /backend/ (domain/infra split), canonicalize config |
| **Critério de Sucesso** | SME validação score ≥75% (D1 14:00) = libera B. <60% = pausa dupla via |
| **Impacto** | A + B pausadas 09:00-12:00. Necessário pra B atingir 70% acurácia D2. |
| **By SME recommendation** | Refator é PRÉ-REQUISITO, não paralelo. Serial enabler de ProjectAdapter. |

---

## Task Naming Convention

- **T{release}.{sprint}.{number}** — Task ID
  - Ex: T1.1.0 (pré-requisito), T1.1.1, T1.1.2, T1.1.3, T1.1.4

---

## Tarefas Core (3.5 SP)

### Tier 1: Harness Coverage (1.5 SP core)

| ID | Titulo | Descrição | SP | Critério de Sucesso | Status |
|----|--------|-----------|-----|------------------|--------|
|| T1.1.1 | Tests agent_harness (1.587 LOC) | Testes unitários para agent_harness, ≥80% coverage. Testes: execution, state, blocking, mocking | 0.75 | coverage ≥80%, sem god-class refactor needed | ✅ Completo (100 testes, 747 linhas) |
|| T1.1.2 | Tests capability_harness | Testes unitários + integração, ≥80% coverage. E2E: agent+capability ≥70% | 0.75 | coverage ≥80%, integration OK | ✅ Completo (80 testes, 924 linhas) |

### Tier 2: ProjectAdapter Viability (2.0 SP core)

| ID | Titulo | Descrição | SP | Critério de Sucesso | Status |
|----|--------|-----------|-----|------------------|--------|
| T1.1.3 | Implementar ProjectAdapter core | Módulo completo: Detector (ABC), 4 detectores concretos, ProjectAdapter.analyze(), ProjectProfile (Pydantic). **Pós-refator Meu PDI (D1 14:00+)** | 1.2 | discover() extrai stack + módulos + semântica básica | 📋 Planejado |
| T1.1.4 | Testes ProjectAdapter em Meu PDI | Validar descoberta em Meu PDI real: ≥70% estrutura capturada. Relatório: padrões detectados vs faltantes. **Pós-refator** | 0.8 | ≥70% descoberta automatizada (pós-refator) | 📋 Planejado |

### Nice-to-Have / Stretch (1.0 SP adicional)

| ID | Titulo | Descrição | SP | Critério | Condição |
|----|--------|-----------|-----|----------|----------|
| T1.1.5 | Polish + edge cases | Refactor para código, edge cases em descoberta, docs | 1.0 | Cobertura >85%, docs completos | Se D2 PASS (ambas trilhas ≥70%) |

---

## Progress Summary (Inicial)

| Task | Completion | SP | Notes |
|------|----------|-----|-------|
| T1.1.0 (Refator Meu PDI — PRÉ) | 0% | — | **D1 09:00-12:00 BLOQUEANTE** — SME validação score ≥75% (D1 14:00) |
| T1.1.1 (agent_harness tests) | 100% | 0.75 | ✅ 100 testes, 747 linhas, 4 classes |
| T1.1.2 (capability_harness tests) | 100% | 0.75 | ✅ 80 testes, 924 linhas, 7 classes |
| T1.1.3 (ProjectAdapter core) | 0% | 1.2 | Dupla via B, pós-refator (D1 14:30+) |
| T1.1.4 (ProjectAdapter Meu PDI) | 0% | 0.8 | Validação D2 gate (≥70% descoberta) |
| T1.1.5 (Polish/stretch) | 0% | 1.0 | Nice-to-have, se D2 PASS |
| **CORE TOTAL** | **0% (0/4)** | **3.5 SP** | **SPRINT INICIANDO — Decisão CEO aprovada** |
| **STRETCH TOTAL** | **0% (0/5)** | **4.5 SP** | Ideal com buffer D5 |

---

## Timeline Planejado (com Decisão Executiva)

```
D1 (22 jul):
  09:00-12:00: T1.1.0 (Refator Meu PDI) — BLOQUEANTE, ambas trilhas pausadas
  12:00-14:00: Commit + review refator
  14:00-14:30: SME validação score refator (≥75%? libera B)
  14:30-17:00: T1.1.1 + T1.1.3 setup (paralelo)
  
D2 (23 jul):
  09:00-12:00: T1.1.1 + T1.1.3 progress
  13:00-14:00: T1.1.3 discovery() finalize
  14:00-14:30: MILESTONE GATE — executable test (coverage A, discover B)
  Decision: PASS (continue dupla) | PARTIAL (B→S2) | FAIL (RCA+replan)
  
D3-4 (24-25 jul): 
  Per Dia 2 decision:
  - PASS: T1.1.2 finish (0.75 SP) + T1.1.3/4 finalize
  - PARTIAL: T1.1.2 finish (harness priority) | T1.1.4 → S2
  - FAIL: RCA morning, replan

D5 (26 jul): 
  Buffer, T1.1.4 validation (se PASS) + T1.1.5 polish (stretch)

Meta CORE (3.5 SP): Harness ≥80% (D5) + ProjectAdapter ≥70% descoberta (D2 gate) ou pausa S2
Meta STRETCH (4.5 SP): + Polish + edge cases
```

---

## Dependências (com Decisão Executiva)

```
T1.1.0 (Refator Meu PDI — BLOQUEANTE D1 09:00-12:00)
│
├─→ T1.1.1 (agent_harness) ┐
│                           ├─→ T1.1.2 (capability_harness) ─→ D2 GATE A
R0 harness ────────────────┘
│
└─→ T1.1.3 (ProjectAdapter core — DEPENDENTE T1.1.0) ─→ T1.1.4 (Meu PDI validation) ─→ D2 GATE B
    (não pode começar antes T1.1.0 ≥75% score)
```

**Crítico:** T1.1.0 é PRÉ-REQUISITO BLOQUEANTE. Sem refator Meu PDI score ≥75%, T1.1.3/4 não começam.
- Se refator score <60%, PAUSA dupla via. Converge serial.
- Se refator score 60-74%, RCA+ replan. Decide fallback.
- Se refator score ≥75%, LIBERA dupla via. Ambas trilhas resumem 14:30.


---

## Critérios de Sucesso por Tarefa

### T1.1.0 - Refatoração Meu PDI (PRÉ-REQUISITO BLOQUEANTE) 🔴

**Timing:** Dia 1, 2026-07-22, 09:00-12:00 BLOQUEANTE

**Deliverable:** Meu PDI refatorado (git worktree isolada)

**Critério de Aceite (SME valida D1 14:00):**
- Score ≥75% = ✅ LIBERA dupla via (T1.1.3/4 resumem 14:30)
- Score 60-74% = 🟡 RCA + decide fallback (serial? extend?)
- Score <60% = ❌ PAUSA dupla via (converge serial apenas Harness)

**Escopo:**
- Remove /docs/knowledge/ duplicidade (audit pré-flight SME D1 07:00)
- Reorganiza /backend/: domain/ vs infrastructure/ split
- Canonicalize config (pyproject.toml, env vars)

**Validação:** SME 30min code review + score (architecture quality)

---

### T1.1.1 - Tests agent_harness 

**Timing:** Dia 1 14:30-end, Dia 2-3 (Trilha A, paralelo com B)

**Deliverable:** Testes unitários em `tests/unit/test_harness/test_agent_harness.py`

**Critério de Aceite (Dia 2 14:00 gate):**
- Coverage ≥70% D2 (gate target), ≥80% D5 (final target)
- Pytest `-v` passa sem warnings
- Testes: execution, state, blocking, mocking

---

### T1.1.2 - Tests capability_harness 

**Timing:** Dia 2-3 (Trilha A, após T1.1.1 progresso)

**Deliverable:** Testes unitários + integração em `tests/unit/test_harness/test_capability_harness.py`

**Critério de Aceite (Dia 5 final):**
- Coverage ≥80% em `apos/harness/capability_harness.py`
- UnitEvaluation + payload binding + mocking testados
- E2E: agent_harness + capability_harness ≥70%

---

### T1.1.3 - Implementar ProjectAdapter core 

**Timing:** Dia 1 14:30+ (APÓS T1.1.0 score ≥75%), Dia 2-3 (Trilha B)

**Deliverable:** Módulo `apos/project_adapter/` com 4 detectores base

**Critério de Aceite (Dia 2 14:00 gate):**
- `ProjectAdapter.discover()` extrai ≥70% estrutura Meu PDI (pós-refator)
- ProjectProfile captura: stack, módulos, padrões, semântica básica
- Sem erros (DetectorExecutionError)
- Testes unitários básicos passando

---

### T1.1.4 - Testes ProjectAdapter em Meu PDI 

**Timing:** Dia 2 13:00-14:00 + Dia 5 (Trilha B, finalize)

**Deliverable:** Relatório de descoberta (`ProjectProfile` JSON + análise)

**Critério de Aceite (Dia 2 14:00 gate):**
- ≥70% descoberta em Meu PDI (pós-refator, validação executável)
- Sem erros de execução
- Relatório: padrões detectados vs faltantes
- **Se <70%:** converge pra PARTIAL (ProjectAdapter → S2)

---

### T1.1.5 - Polish + Edge Cases (STRETCH, se PASS D2)

**Timing:** Dia 3-5 (opcional, se PASS gate)

**Deliverable:** Code refactor, edge case handling, docs completos

**Critério de Aceite:**
- Coverage >85% em ambas trilhas
- Zero warnings, code quality checks pass
- Docs atualizadas

---

## 🎯 Milestone Dia 2 14:00 — Executable Test Gate (Obrigatório)

**(Decisão Executiva #5)**

### Gate Criteria (Dia 2 14:00-14:30)

**Trilha A - Harness Coverage:**
```bash
pytest --cov=apos/harness --cov=apos/capabilities tests/ --cov-report=html
# Critério Dia 2: ≥70% (gate), Dia 5: ≥80% (final)
```

**Trilha B - ProjectAdapter Discovery:**
```bash
python apos/project_adapter/discover.py /path/to/meu_pdi
# Critério Dia 2: ≥70% estrutura capturada (gate), Dia 5: ≥80% (final)
```

### Decision Tree (Dia 2 14:30)

| A Coverage | B Discovery | Decisão | Release | Próximos Passos |
|-----------|------------|---------|---------|-----------------|
| ✅ ≥70% | ✅ ≥70% | **PASS** | 2026-08-02 (on track) | Continue dupla D3-5. Especializa sem context-switch. T1.1.5 stretch opcional. |
| ✅ ≥70% | ❌ <50% | **PARTIAL** | 2026-08-09 (+1 sem) | A finish D5. B → S2 (full scope). Comunica stakeholder D2 14:30. |
| ❌ <70% | ❌ <70% | **FAIL** | 2026-08-16 (+2 sem) | D2 15:00 RCA. D3 10:00 replan. Decide: tech debt? scope? estimate wrong? |

### Contingency Paths (Pre-decided)

**If PARTIAL (A pass, B fail):**
- Harness ≥80% guaranteed D5
- ProjectAdapter full scope → S2 (known, not surprise)
- Release slip: +1 week (acceptable, pre-communicated)

**If FAIL (both <70%):**
- SME + CEO RCA D2 15:00-16:00
- D3 morning: Decide pivot (extend? reduce scope? fix tech debt?)
- Release: +2 weeks (if extend), or reduce KRs (if cut features)

---

**Atualizado:** 2026-07-22 (Decisão Executiva integrada)  
**Sprint Manager:** APOS  
**Aprovação CEO:** ✅ Jader Greiner (Caminho 3 — Default Path, 5 decisões aprovadas)
