# Sprint Planning — R1 Sprint 1

**Data:** 2026-07-21 (criado), 2026-07-22 (atualizado com DECISÃO_EXECUTIVA)
**Duração:** 60min (D1 kickoff)
**Participantes:** Jader (CEO + Tech Lead + PM + SME)
**Formato:** Dupla Via (condicional até D2 14:00 milestone)
**Status:** ✅ APROVADO — Decisão Executiva CEO incorporada

---

## 🎯 Sprint Goal

> Tornar APOS operacional no Meu PDI: **Harness ≥80% (A) + ProjectAdapter protótipo ≥70% (B)** em 1 semana, com refatoração Meu PDI como enabler.
>
> **Milestone Dia 2:** Executable test gate. PASS = continue dupla. PARTIAL = converge D3 (ProjectAdapter → S2). FAIL = RCA + replan.

---

## ✅ Pré-Requisitos Verificados

| Pré-Requisito | Status | Evidência |
|--------------|--------|-----------|
| Sprint Zero executado | ✅ | Tag `r0-2026-07-21`, working tree limpo |
| Jira sync configurado | ✅ | `.jira_sync_history.json` (SCRUM-55 a SCRUM-58) |
| Tag de rollback | ✅ | `r0-2026-07-21` |
| Decisão Executiva CEO | ✅ | DECISAO_EXECUTIVA.md (5 decisões aprovadas) |
| Pre-flight SME audit | ✅ 🔄 | Agendada D1 07:00-08:30 (antes kickoff) |

---

## 📊 Alinhamento com OKRs

| KR | Descrição | Sprint | Status |
|----|-----------|--------|--------|
| KR1 | ProjectAdapter descobre ≥80% Meu PDI | S1 protótipo, S2 completo | 🎯 Sprint 1 alvo |
| KR2a | agent_harness + capability_harness ≥80% | Sprint 1 (2 SP) | 🎯 Sprint 1 alvo |
| KR4 | Baseline métricas + 1º comparativo | Iniciar imediatamente | 📋 Iniciar |

---

## 🔴 PRÉ-REQUISITO: Refatoração Meu PDI (Dia 1 09:00-12:00)

**Status:** ✅ APROVADO (Decisão Executiva #1, Opção A)

| Aspecto | Detalhe |
|---------|---------|
| **Quando** | Dia 1, 2026-07-22, **09:00-12:00 APENAS** |
| **O quê** | Remove /docs/knowledge/ duplicidade, reorganiza /backend/ (domain/infra split), canonicalize config |
| **Owner** | Jader (CEO + Tech Lead) |
| **Validação** | SME audita score D1 14:00. ≥75% = libera ProjectAdapter. <60% = pausa dupla via. |
| **Git strategy** | `git worktree` isolada. Não contamina main. |
| **A+B impact** | Ambas trilhas **pausadas 09:00-12:00**. Resume 14:30 (pós-SME validação). |
| **Por quê** | SME + SM/TL: refator é PRÉ-REQUISITO serial. Sem isso, B cai 80%→30% accuracy. |

**Resultado esperado Dia 1 14:00:** ✅ Refator completo + SME validação (score ≥75%) = ProjectAdapter liberada com 70% accuracy projetada D2.

---

## 🚂 Dupla Via — Sprint 1 (D1 14:30 - D5)

### Trilha A: Harness Coverage (1.5 SP core)
**Meta:** agent_harness + capability_harness ≥80%
**Owner:** Jader
**Milestone Dia 2:** Coverage ≥70% ou repriorizar

| Task | Estimativa | Critério de Sucesso |
|------|-----------|---------------------|
| T1.1.1: Tests agent_harness (1.587 LOC) | 0.75 SP | coverage ≥80%, no god-class refactor needed |
| T1.1.2: Tests capability_harness | 0.75 SP | coverage ≥80%, integration OK |

### Trilha B: ProjectAdapter Protótipo (2.0 SP core)
**Meta:** `ProjectAdapter.discover()` funcional em Meu PDI (pós-refator)
**Owner:** Jader
**Milestone Dia 2:** discover() ≥70% ou pausar (converge para S2)

| Task | Estimativa | Critério de Sucesso |
|------|-----------|---------------------|
| T1.1.3: Implementar ProjectAdapter core | 1.2 SP | discover() extrai stack + módulos + semântica básica |
| T1.1.4: Testes ProjectAdapter em Meu PDI | 0.8 SP | ≥70% descoberta automatizada (pós-refator) |

### Guardrails — Dupla Via Condicional
**(Decisão Executiva #2, Opção B)**

- ✅ Dedicate dev (Jader só, nada paralelo fora sprint)
- ✅ Refatoração FIRST (Dia 1 09-12, PRÉ-requisito)
- ✅ Schema freeze D1 (não muta Meu PDI core sem SME OK)
- ✅ 2x standups (09:00, 15:00, D1-5)
- ✅ Serialize dependencies (A + B não cruzam contexto)

### Velocity Realista (3.5 SP core)
**(Decisão Executiva #3, Opção A)**

- **Core tasks:** 3.5 SP (A 1.5 + B 2.0)
- **Stretch:** +1.0 SP polish (se D2 PASS)
- **Redução vs R0:** 50% (1.4 → 0.7 SP/dia). Esperado: refator startup + dupla via overhead.
- **Overhead real:** ~0.5 SP context-switching. Já inclusos nas estimativas acima.

### Buffer (0.5 dia)
- Folga para validação Dia 2 gate + contingency buffer

---

## 🎯 Milestone Dia 2 14:00 — Executable Test Gate (Obrigatório)

**(Decisão Executiva #5, Opção A)**

| Dia | Trilha A | Trilha B | Gate | Status |
|-----|----------|----------|------|--------|
| **Dia 1** | 09:00-12:00 PAUSA (refator), 14:30-17:00 Setup | 09:00-12:00 PAUSA, 14:30-17:00 Esboço | SME pre-flight audit 14:00 (score refator) | Pre-flight |
| **Dia 2** | 09:00-12:00 + 14:00-14:00 capability_harness | 09:00-12:00 + 13:00-14:00 discover() finalize | **14:00-14:30: Executable test** | 🎯 GATE |
| **Dia 3+** | Per gate result | Per gate result | Decisão documentada + communicated | Implementation |

### Executable Test Criteria (Dia 2 14:00)

**Trilha A (Harness):**
```bash
pytest --cov=apos/harness --cov=apos/capabilities tests/ --cov-report=html
# Critério: Coverage ≥70% (D2 gate), ≥80% (D5 target)
```

**Trilha B (ProjectAdapter):**
```bash
python apos/project_adapter/discover.py /path/to/meu_pdi
# Critério: discover() output + manual inspection
# Score ≥70% estrutura capturada (D2 gate), ≥80% (D5 target)
```

### Gate Decision Tree (Dia 2 14:30)

| Trilha A | Trilha B | Decisão | Release Timeline | Next Steps |
|----------|----------|---------|-----------------|------------|
| ✅ ≥70% | ✅ ≥70% | **PASS** — Continue dupla D3-5 | 2026-08-02 (on track) | Especializa A+B (sem context-switch), target D5 delivery |
| ✅ ≥70% | ❌ <50% | **PARTIAL** — Converge A-only D3-5 | 2026-08-09 (+1 sem) | A finish D5. B → S2 (full scope). Comunica stakeholder |
| ❌ <70% | ❌ <70% | **FAIL** — RCA same-day 15:00 | 2026-08-16 (+2 sem, TBD) | SME + Jader RCA. Decide: refactor issue? Scope issue? Tech debt? Replan D3 morning |

### Contingency Paths (Pre-decided, no surprises)

**If PARTIAL (A pass, B fail):**
- D3-5: finish Harness (KR2a ≥80% EOD D5)
- ProjectAdapter full scope → S2 R1 (known, not surprise)
- Comms: CEO tells stakeholder D2 14:30 "Dupla via B hit complexity, moving to S2"

**If FAIL (both <70%):**
- D2 15:00-16:00: SME + Jader RCA
- D3 morning: Decide 1 of 3: (1) Tech debt refactor needed? (2) Scope too big? (3) Estimate was wrong?
- D3 10:00: Re-plan sprint. Either extend (2-3 days) or reduce scope (cut B features, keep core).
- Release: +2 weeks possible, but plan B exists (Harness-only R1, ProjectAdapter R2).

---

## 🚨 Riscos & Mitigação Pre-Flight (Decisão Executiva #4)

**Status:** SME pre-flight audit agendada D1 07:00-08:30 (1.5h)

| Risco | Prob | Impacto | Mitigação | Pre-Flight Check |
|-------|------|---------|-----------|-----------------|
| Refatoração Meu PDI encontra "ouro" em /docs/knowledge/ | 60% | +1-2d | SME audita /docs/knowledge/ (gold vs dross). Prioriza o quê remover vs manter. | ✅ Planned |
| agent_harness é "god class" (1.587 LOC monolítico) | 40% | +1d refactor | SME code review agent_harness. Se problema, pre-refactor antes B starts. | ✅ Planned |
| ProjectAdapter mais complexo que prototipável em 2 SP | 50% | B cai <50% D2 | Dia 2 runnable test (não opinião). Se score <30%, pause tripla via. Converge S2. | ✅ Milestone gate |
| Context-switching A/B causa bugs silent | 30% | Low | 2x standups + pair review D3-5 com SME. Não solo coding. | ✅ Guardrail |
| Jira sync inconsistência | 20% | Low | Manual sync Dia 1 kickoff. Automatizar S2. | ✅ Known |

**Pre-Flight Audit Output (D1 08:30):** 
- ✅ /docs/knowledge/ scope finalized (30 min work estimate)
- ✅ agent_harness refactor needs? (yes/no + scope)
- ✅ ProjectAdapter scope confidence (high/medium/low)
- ✅ RCA fallback pre-decided if any risk is critical

---

## 📋 Pre-Flight Checklist — Dia 1 Antes Kickoff

- [ ] **07:00-08:30:** SME executa pre-flight audit (3 riscos top)
- [ ] **08:30-09:00:** SME + Jader sync: resultados, fallback decisions
- [ ] **09:00-12:00:** Refator Meu PDI (Decisão 1)
- [ ] **12:00-14:00:** Commit, review, SME validation
- [ ] **14:00-14:30:** SME score refator ≥75% = libera B, <60% = pausa
- [ ] **14:30-17:00:** D1 evening: A/B resume, standups, DAILY_STANDUP_2026-07-22.md

---

## 🔄 Ações da Retro Anterior (Baseline R0)

| ID | Descrição | Critério de Verificação | Dono | Prioridade | Due |
|----|-----------|------------------------|------|-----------|-----|
| R0-AC01 | Planning paralelo (Tier 1+2) como default | SPRINT_PLANNING.md tem trilhas paralelas | SM | high | S1 |
| R0-AC02 | Templates de cerimônia pré-criados no kickoff | BOARD.md + TASKS.md + SPRINT_PLANNING.md existem no D1 | SM | high | S1 |
| R0-AC03 | Commit Tracking validation integrado | Script de verificação commit → task linkado | Dev | medium | S2 |
| R0-AC04 | Recrutar persona real externa para validação | 1 entrevista externa agendada | CEO | high | S2 |
| R0-AC05 | Refinar baseline de velocity | Estimativas vs real do Sprint Zero documentado | SM | medium | S1 |

---

## 📈 Métricas da Sprint

| Métrica | Alvo | Como medir |
|---------|------|-----------|
| Harness coverage | ≥80% | `pytest --cov=apos/harness --cov=apos/capabilities` |
| ProjectAdapter discovery | ≥50% estrutura Meu PDI | `adapter.discover()` + inspeção manual |
| Milestone Dia 2 | Decisão tomada | Registro em DAILY_STANDUP.md |
| Velocity | 4 SP + buffer | Story points completos / dias |

---

**Sprint Planning criado:** 2026-07-21  
**Atualizado:** 2026-07-22 (Decisão Executiva CEO + 5 decisões críticas)  
**Scrum Master:** Hermes Agent  
**Aprovação:** ✅ APROVADO — CEO Jader Greiner (Caminho 3 — Default Path)

---

## ✅ APROVAÇÃO EXECUTIVA

**Decisão Executiva Reference:** DECISAO_EXECUTIVA.md

- [x] **Decisão 1:** Refatoração → Opção A (D1 09-12 refactor-only)
- [x] **Decisão 2:** Dupla Via → Opção B (condicional até D2 14:00)
- [x] **Decisão 3:** Velocity → Opção A (3.5 SP core, 4.5 SP stretch)
- [x] **Decisão 4:** Risk Mitigation → Opção A (pre-flight SME D1 07:00)
- [x] **Decisão 5:** Release Timeline → Opção A (executable test D2 14:00)

**Status:** ✅ Ready for Dia 1 Kickoff
**Next checkpoint:** Dia 2 14:00 Milestone Gate (executable test)
