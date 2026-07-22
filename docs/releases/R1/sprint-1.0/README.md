# R1 Sprint 1.0 — Harness + ProjectAdapter Viability

**Sprint:** R1 Sprint 1.0  
**Data:** 2026-07-22 a 2026-07-26 (5 dias)  
**Status:** 🚀 **PRÉ-KICKOFF** — Decisão Executiva CEO aprovada, ready pra D1 09:00

---

## 📋 Documentação Sprint

| Documento | Propósito | Status |
|-----------|-----------|--------|
| **[DECISAO_EXECUTIVA.md](DECISAO_EXECUTIVA.md)** | 5 decisões críticas CEO (refator, dupla via, velocity, risk mitigation, release timeline) | ✅ Formalizado |
| **[SPRINT_PLANNING.md](SPRINT_PLANNING.md)** | Planejamento detalhado com refator pré-requisito, dupla via guardrails, D2 milestone gate | ✅ Atualizado |
| **[TASKS.md](TASKS.md)** | 5 tarefas core (3.5 SP) + 1 stretch (1.0 SP). Refator T1.1.0 pré-sprint. | ✅ Reestimado |
| **[BOARD.md](BOARD.md)** | Kanban visual do sprint (backlog, in progress, in review, done) | 📋 Em andamento |
| **[DAILY_STANDUP_YYYY-MM-DD.md](DAILY_STANDUP_2026-07-22.md)** | Daily standups (múltiplos formatos) | ✅ Criado D1 pré-kickoff |
| **[ATA_SPRINT_PLANNING.md](ATA_SPRINT_PLANNING.md)** | Ata do planning (entrevistas + síntese + decisões) | 📋 Referência |
| **[SYNTHESIS.md](SYNTHESIS.md)** | Consolidação de 3 entrevistas (CEO, SME, SM/TL) | ✅ Referência |

---

## 🎯 Sprint Goal

> **Tornar APOS operacional no Meu PDI:** Harness Coverage ≥80% (KR2a) + ProjectAdapter Protótipo ≥70% descoberta (KR1 viabilidade)

**Com refatoração Meu PDI como PRÉ-REQUISITO habilitador.**

---

## 🔴 PRÉ-REQUISITO BLOQUEANTE

### T1.1.0: Refatoração Meu PDI (Dia 1, 09:00-12:00)

**Escopo:** Remove /docs/knowledge/ duplicidade, reorganiza /backend/ (domain/infra split), canonicalize config

**Validação:** SME audita score ≥75% (D1 14:00). Libera dupla via se OK.

**Se falhar (<60%):** Pausa dupla via, converge serial (Harness only, ProjectAdapter → S2)

---

## 🚂 Dupla Via — Sprint 1

### Trilha A: Harness Coverage (1.5 SP)
- **T1.1.1:** Tests agent_harness (0.75 SP)
- **T1.1.2:** Tests capability_harness (0.75 SP)
- **Target D2:** ≥70% coverage (gate)
- **Target D5:** ≥80% coverage (final)

### Trilha B: ProjectAdapter Protótipo (2.0 SP)
- **T1.1.3:** ProjectAdapter core (1.2 SP) — *depende T1.1.0*
- **T1.1.4:** ProjectAdapter Meu PDI (0.8 SP)
- **Target D2:** ≥70% descoberta (gate)
- **Target D5:** ≥80% descoberta (final)

### Stretch Goal (1.0 SP, se D2 PASS)
- **T1.1.5:** Polish + edge cases

---

## 📊 Decisões CEO (Executiva)

| # | Decisão | Opção | Impacto |
|---|---------|-------|---------|
| 1 | Refatoração timing | A | D1 09-12 refactor-only, PRÉ-requisito bloqueante |
| 2 | Dupla via | B | Condicional até D2 14:00, abort-gate se B<50% |
| 3 | Velocity | A | 3.5 SP core (50% redução vs R0), 4.5 SP stretch |
| 4 | Risk mitigation | A | Pre-flight SME 1.5h D1 07:00, fallback pré-decidido |
| 5 | Release timeline | A | Executable test D2 14:00, contingency mapping |

**Documentado:** DECISAO_EXECUTIVA.md

---

## 🎯 Milestone Dia 2 14:00 — Executable Test Gate

### Critérios Executáveis

**Trilha A (Harness):**
```bash
pytest --cov=apos/harness --cov=apos/capabilities tests/ --cov-report=html
# Critério: ≥70% D2 (gate), ≥80% D5 (final)
```

**Trilha B (ProjectAdapter):**
```bash
python apos/project_adapter/discover.py /path/to/meu_pdi
# Critério: ≥70% estrutura capturada D2 (gate), ≥80% D5 (final)
```

### Decision Tree (Dia 2 14:30)

| A | B | Decisão | Release | Ação |
|---|---|---------|---------|------|
| ✅ ≥70% | ✅ ≥70% | **PASS** | 2026-08-02 | Continue dupla D3-5 |
| ✅ ≥70% | ❌ <50% | **PARTIAL** | 2026-08-09 (+1 sem) | Converge A-only, B→S2 |
| ❌ <70% | ❌ <70% | **FAIL** | 2026-08-16 (+2 sem) | RCA + replan D3 |

---

## 📅 Timeline Dia 1 Kickoff (2026-07-22)

```
07:00-08:30: 🚀 Pre-flight SME audit (riscos top 3)
09:00-12:00: 🔴 Refator Meu PDI (A+B pausa, bloqueante)
12:00-14:00: ✅ Commit + review refator
14:00-14:30: 📊 SME validação score (≥75%? libera B)
14:30-17:00: 📋 Kickoff + A/B setup
17:00-18:00: 🎤 Daily standup #1 + DAILY_STANDUP_2026-07-22.md
```

---

## 🚨 Riscos Pré-Identificados

| Risco | Prob | Mitigação |
|-------|------|-----------|
| Refator encontra "ouro" em /docs/knowledge/ | 60% | Pre-flight SME audit (D1 07:00) |
| agent_harness é "god class" | 40% | SME code review (D1 07:00), pre-refactor se needed |
| ProjectAdapter mais complexo que prototipável | 50% | D2 gate executável (teste real, não opinião) |
| Context-switch A/B causa bugs | 30% | 2x standups (09:00, 15:00), pair review |

**Mitigação:** Pre-flight SME D1 07:00-08:30 identifica riscos early. Fallback pré-decidido.

---

## 📈 Métricas — Rastrear

| Métrica | D2 Gate | D5 Final | Responsável |
|---------|---------|----------|------------|
| Refator score | ≥75% (libera B) | ✅ Complete | SME |
| Harness coverage (A) | ≥70% | ≥80% | Jader |
| ProjectAdapter discovery (B) | ≥70% | ≥80% | Jader |
| Velocity | 0.7 SP/dia | 3.5 SP total | SM/TL |
| Pre-flight findings | Documented | Resolved/escalated | SME |

---

## ✅ Checklists

### Dia 1 Pré-Kickoff (Antes 09:00)

- [ ] SME executa pre-flight audit 07:00-08:30 (3 riscos top)
- [ ] Refator scope finalizado (git worktree pronta)
- [ ] A/B tasks entendidas (T1.1.1-4 ready)
- [ ] Jira sincronizado com TASKS.md
- [ ] DAILY_STANDUP_2026-07-22.md criado

### Dia 2 Milestone Gate (14:00)

- [ ] Coverage report A pronto (`pytest --cov`)
- [ ] Discover() test B pronto (`adapter.discover()`)
- [ ] Decision documentada + communicated
- [ ] Contingency path iniciado (se PARTIAL/FAIL)

### Dia 5 Final (17:00)

- [ ] Harness ≥80% (KR2a)
- [ ] ProjectAdapter ≥80% ou pausa S2 (KR1 viabilidade)
- [ ] Retro preparada (RETRO.md)
- [ ] Release status comunicado ao business

---

## 📚 Referências

- **Entrevistas base:** ENTREVISTA_1_CEO.md, ENTREVISTA_2_SME.md, ENTREVISTA_3_SMTL.md
- **Síntese:**SYNTHESIS.md
- **Jira:** Sprint "SCRUM R1 Sprint 1.0" (ID: 8) — 4 tasks mapeadas (SCRUM-55-58)
- **Comms:** Stakeholder notificado D1 pré-kickoff (transparência: 3.5 SP, +1 semana se PARTIAL)

---

**Sprint criado:** 2026-07-21  
**Atualizado:** 2026-07-22 (Decisão Executiva CEO integrada)  
**Status:** ✅ Pronto pra D1 09:00 kickoff  
**Próximo checkpoint:** D2 14:00 Milestone Gate (executable test)
