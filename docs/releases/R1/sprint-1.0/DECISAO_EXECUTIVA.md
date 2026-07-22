# 🎯 DECISÃO EXECUTIVA — R1 Sprint 1

**Data:** 2026-07-22 (Dia 1)  
**Decidor:** CEO (Jader Greiner)  
**Baseado em:** 3 perspectivas independentes (Product Lead, SME Técnico, SM/Tech Lead)  
**Status:** ✅ APROVADO — Implementar caminho 3 (Default Path)

---

## 5 DECISÕES CRÍTICAS

### **DECISÃO 1: Refatoração Meu PDI — APROVADO OPÇÃO A**

**Decisão:** Aloca Dia 1 09:00-12:00 **APENAS refatoração Meu PDI**. Suspende A+B nesse período.

| Aspecto | Detalhe |
|---------|---------|
| **Quando** | Dia 1, 2026-07-22, 09:00-12:00 (3h) |
| **O quê** | Refatora Meu PDI: remove /docs/knowledge/ duplicidade, reorganiza /backend/ domain/infra, canonicalize config |
| **Owner** | Jader (CEO + Tech Lead) |
| **Validação** | SME audita viabilidade D1 14:00 (30min). Score ≥75% = libera ProjectAdapter. Score <60% = pausa dupla via |
| **Git strategy** | Usa `git worktree` isolada. Não contamina main. |
| **D1 timeline** | 09:00-12:00 refactor, 12:00-14:00 commit+review, 14:00-14:30 SME validação, 14:30-end A+B resume |
| **Impacto** | Atrasa A/B em 3h. B ganha 70% acurácia D2 (vs 30% sem refator). Trade-off worth it. |

**Razão:** SME + SM/TL dizem refator é PRÉ-REQUISITO serial. Sem isso, ProjectAdapter accuracy cai 50%→80%.

---

### **DECISÃO 2: Dupla Via — APROVADO OPÇÃO B (Condicional)**

**Decisão:** Dupla via A+B D1-D2. Dia 2 14:00, **abort-gate**: Se A≥70% ✅ continue dupla D3-5. Se B<50%, **converge pra Harness-only D3-5**.

| Aspecto | Detalhe |
|---------|---------|
| **D1-2 estrutura** | A (Harness tests) + B (ProjectAdapter core) paralelo |
| **D2 14:00 gate** | **Executable test** (não opinião): Coverage report A, discover() score B |
| **PASS (A≥70% + B≥70%)** | ✅ Continue dupla D3-5. Especializa sem context-switch. Timeline: 2026-08-02 on track. |
| **PARTIAL (A≥70%, B<50%)** | 🟡 Converge pra Harness-only D3-5. ProjectAdapter → S2 (+1 semana). Revised timeline: 2026-08-09. |
| **FAIL (nenhuma≥70%)** | 🔴 RCA same-day D2 15:00. Decide pivot/pause/extend. Timeline: 2026-08-16 (se extend). |
| **Guardrails** | (1) Dedicate devs (Jader só), (2) Refactor FIRST (Decisão 1), (3) Schema freeze D1 (não muda Meu PDI core), (4) 2x standups (09:00, 15:00), (5) Serialize dependencies (não cross-contaminate) |
| **Context-switch overhead** | ~0.5 SP real. Budget = 3.5 SP (não 4.5 SP). Comunicado. |

**Razão:** Product + SME + SM/TL concordam dupla via é viável com guardrails. Abort-gate D2 é safety valve.

---

### **DECISÃO 3: Velocity — APROVADO OPÇÃO A (3.5 SP Core)**

**Decisão:** **3.5 SP "definite"** (guaranteed), 4.5 SP "stretch" (ideal).

| Aspecto | Detalhe |
|---------|---------|
| **Core tasks (3.5 SP)** | T1.1.1-4 reestimadas: Harness 1.5 SP, ProjectAdapter 2.0 SP, validação 0.5 SP |
| **Stretch goal (4.5 SP)** | + 1.0 SP polish/optimization se D2 vai bem |
| **Velocity baseline** | R0: 1.4 SP/dia. R1 S1: 0.7 SP/dia (50% redução). Esperado: refactor startup + dupla via overhead + validation. |
| **Dia 2 milestone targets** | A ≥70% (Harness), B ≥70% (ProjectAdapter) — mais realista com budget correto |
| **Stakeholder communication** | "3.5 SP guaranteed. Dupla via é trade-off: velocidade vs robustez. Aceitamos 50% redução pra ter ≥70% confiança D2." |

**Razão:** SME + SM/TL dizem 3.5 SP é realistic. 4.5 SP é otimista. Comunicar honestamente economiza "Dia 5 surprises".

---

### **DECISÃO 4: Risk Mitigation — APROVADO OPÇÃO A (Pre-flight Dia 0)**

**Decisão:** SME faz **1.5h audit DIA 0 HOJE** (antes D1 kickoff). Identifica riscos early. Guarda ~2 dias se descobre issues.

| Aspecto | Detalhe |
|---------|---------|
| **Quando** | Hoje, Dia 1, 07:00-08:30 (antes 09:00 kickoff) — OU post-refactor 12:00-13:30 |
| **O quê** | SME audita: (1) /docs/knowledge/ gold vs dross, (2) agent_harness 1.587 LOC (god class?), (3) ProjectAdapter scope viability |
| **Output** | Pre-flight Audit Report (30 min doc). Identifica: é refactor blocker? É agent_harness blocker? É ProjectAdapter scope OK? |
| **Ação** | Se descobrir issues, RCA same-day. Pre-comprometer fallback (serial, reduce scope, extend). Não surprises D2. |
| **Contingency decidido pre-D1** | SME + SM/TL discutem hoje pre-kickoff. Se refator é >8h, converge serial pre-start. Se agent_harness é god class, pre-refactor D1 antes B. |

**Razão:** Product + SME + SM/TL concordam: estrutura + pre-flight = menos surprises. 1.5h investimento economiza 2+ dias later.

---

### **DECISÃO 5: Release Timeline & Gates — APROVADO OPÇÃO A (Executable Test D2)**

**Decisão:** Dia 2 14:00 é **não-negotiable milestone**. Teste executável (não opinião). Contingency timeline formalizada.

| Aspecto | Detalhe |
|---------|---------|
| **Dia 2 14:00 gate** | **Executable test:** `pytest --cov=apos/harness` (A score), `adapter.discover()` (B score) + manual inspection |
| **Critérios de decisão** | A ≥70% coverage ✅ | B ≥70% discovery ✅ | Ambas = PASS → continue dupla |
| | A ≥70% coverage ✅ | B <50% discovery ❌ | Partial → converge D3, ProjectAdapter S2 |
| | Nenhuma ≥70% ❌ | — | FAIL → RCA 15:00, decide extend/pivot/reduce scope |
| **Contingency timeline** | PASS: 2026-08-02 (on track), PARTIAL: 2026-08-09 (+1 sem), FAIL: 2026-08-16 (+2 sem, com RCA) |
| **Comunicação upfront** | Stakeholder sabe Dia 1: "Dupla via risco Dia 2. Se PARTIAL, +1 semana. Se FAIL, +2 semana (com RCA). É aceitável?" Transparência. |
| **Documentação** | DAILY_STANDUP.md D2 14:00 registra decision + rationale + next steps |

**Razão:** Product Lead recommends transparência. SME + SM/TL formalizam gate. Contingency paths pré-decididas evitam "Dia 5 panic".

---

## 📋 RESUMO EXECUTIVO

| Decisão | Opção | Impacto |
|---------|-------|---------|
| **1. Refatoração** | A | D1 09-12 refactor-only, SME validação D1 14:00. B ganha accuracy. |
| **2. Dupla Via** | B | D1-2 paralelo, D2 14:00 abort-gate. Se B<50%, converge D3. |
| **3. Velocity** | A | 3.5 SP definite, 4.5 SP stretch. Comunica 50% redução vs R0. |
| **4. Risk Mitigation** | A | SME pre-flight 1.5h hoje. Identifica riscos early, fallback pre-decidido. |
| **5. Release Timeline** | A | Dia 2 14:00 executable test. PASS=on-track, PARTIAL=+1sem, FAIL=+2sem+RCA. |

---

## ✅ PRÓXIMOS PASSOS

### **Hoje (Dia 1, 2026-07-22)**

- [ ] **07:00-08:30:** SME pre-flight audit (Decisão 4) — report 15min
- [ ] **09:00-12:00:** Refator Meu PDI + A setup (Decisão 1)
- [ ] **12:00-14:00:** Commit refator, SME review
- [ ] **14:00-14:30:** SME validação score (Decisão 1 gate)
- [ ] **14:30-17:00:** Kickoff + A/B resume (D1 evening)
- [ ] **17:00-18:00:** Daily standup #1 + DAILY_STANDUP_2026-07-22.md

### **Dia 2 (2026-07-23)**

- [ ] **09:00-12:00:** A + B progress (time-box alternating)
- [ ] **14:00-14:30:** **MILESTONE GATE** — execute tests (Decisão 5)
- [ ] **14:30-15:00:** Decision + documentation (DAILY_STANDUP_2026-07-23.md)
- [ ] **15:00-17:00:** Continue ou converge (based on gate result)

### **Dia 3-5**

- [ ] Per Dia 2 gate result:
  - **If PASS:** Specialized A/B (no context-switch), target delivery D5
  - **If PARTIAL:** Converge A-only, ProjectAdapter → S2, rework timeline
  - **If FAIL:** RCA + replan (Dia 3 morning), extend sprint if needed

---

## 📊 MÉTRICAS PARA RASTREAR

| Métrica | Target D2 | Target D5 |
|---------|-----------|-----------|
| Harness coverage (A) | ≥70% | ≥80% |
| ProjectAdapter discovery (B) | ≥70% | ≥80% |
| Refator Meu PDI score | ≥75% | ✅ Complete |
| Velocity vs estimate | 0.7 SP/dia | 3.5 SP total |
| Risk pre-flight findings | Documented | Resolved (or escalated) |

---

**Decisão autorizada:** CEO Jader Greiner  
**Data:** 2026-07-22  
**Próxima revisão:** Dia 2 14:00 (milestone gate)  
**Arquivo:** DECISAO_EXECUTIVA.md
