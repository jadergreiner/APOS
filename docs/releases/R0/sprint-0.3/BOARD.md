# Sprint Board — Kanban

**Sprint:** 0.3 — Beta Prep (MVP Implementation)  
**Status:** 🟠 IN EXECUTION (Dia 2, 2026-07-23)  
**Ultima Atualizacao:** 2026-07-23 09:00am UTC  

---

## 📊 Resumo Visual

```
Backlog        A Fazer       Em Progresso    Em Revisao    Completo
   (0)            (6)            (2)            (1)          (2)

   ---            v              v              v           Done
                                                            T0.3.1 ✅
                                                            T0.3.2 ✅
```

**Progresso:** 25% (2/8 completo) — Dia 2 em andamento

---

## 📋 Backlog (Nao Iniciado)

**Total:** 0 items (todos ja em "A Fazer")

---

## ✅ A Fazer (Pronto para Comecar)

**Total:** 6 items (Tier 2 + Tier 3, esperar T0.3.3-4)

### Tier 2: Important (Should-Have)

- [ ] **T0.3.5** — Piloto com 3 Personas (PILOT_PLAN.md) — 2d
  - Onboarding (Dia 3)
  - Feedback cycles (Dias 4-5)
  - Final call + Go/No-Go decision (Dia 6)

- [ ] **T0.3.6** — Metricas Baseline + Tracking — 1d
  - Setup monitoring
  - Baseline coleta (before/after)
  - Dashboard preparacao

### Tier 3: Support (Nice-to-Have)

- [ ] **T0.3.7** — Documentacao Completa — 1d
  - README, API docs, tutorial, troubleshooting

- [ ] **T0.3.8** — Testing + QA — 0.5d
  - Unit tests (>80% cobertura)
  - Integration tests
  - Edge cases validation

---

## 🔄 Em Progresso

**Total:** 2 items (Dia 2 em andamento, paralelo)

- [ ] **T0.3.3** — Implementacao Plugin Jira (2d) — 🟠 IN PROGRESS
  - Jira API connection + webhook receiver
  - Orphan detection UI + modal "Vincular OKR"
  - Dashboard Task→OKR visual

- [ ] **T0.3.4** — Trust Score Engine (1.5d) — 🟠 IN PROGRESS
  - SemanticGate class implementation
  - Formula: (0.3 × coverage) + (0.5 × quality) + (0.2 × consistency)
  - Testes unitarios (>80% cobertura)

---

## 👀 Em Revisao

**Total:** 1 item (validacao completa de SPEC.md)

- [ ] **SPEC.md Refinements** (30 min) — ⚠️ PENDING UPDATES
  1. Adicione Seção 11: "Resumo Semanal" (MVP Should-Have)
  2. Refine Seção 4.3: Data Freshness scoring (clarity para T0.3.4)
  3. Expand Seção 7: Conflict detection logic (edge case crítico)
  
  **Status:** Validacao completa + achados 3/3 documentados
  **Blocker:** Nao — T0.3.3-4 podem começar sem esses refinements
  **Recomendacao:** Aplique refinements apos Dia 2 (nao crítico hoje)

---

## ✅ Completo

**Total:** 2 items (Dia 1 concluido!)

### Tier 1: Core (Completo)

- [x] **T0.3.1** — Especificacao Tecnica (SPEC.md) — 1.5d — ✅ COMPLETO
  **Validacao:** 95/100 (Job Statement ✅, Forças ✅, MVP Scope ✅, Schemas ✅, Fluxo dados ✅)
  **Refinements pending:** 3 menores (Resumo Semanal, Freshness clarity, Conflict logic)
  **Status:** Pronto para T0.3.3-4 sem bloqueadores

- [x] **T0.3.2** — Design de API REST (API_DESIGN.md) — 1.5d — ✅ COMPLETO
  **Deliverables:** 6 endpoints (GET /tasks, /okrs, POST /relationships, /trust-score, /orphans)
  **Exemplos:** curl commands + request/response schemas
  **Pronto para:** T0.3.3-4 implementacao

---

**Board Atualizado:** 2026-07-23 09:00am UTC (Dia 2)  
**Status:** T0.3.3-4 em progresso (paralelo), T0.3.1-2 validadas
**Proxima Atualizacao:** 2026-07-24 (Dia 3 — Piloto onboarding)  
**Burndown esperado:** 50% completo ao final Dia 2 (3d/6.5d)
