# 🎙️ ENTREVISTA 3: SCRUM MASTER / TECH LEAD

**Data:** 2026-07-22 (Dia 1 — 14:40)  
**Duração:** 20 min  
**Entrevistador:** APOS Sprint Manager  
**Papel:** Validar execução, mapear dependências, gerenciar velocity

---

## Q1: Dupla Via é Factível?

**Pergunta:**
> "Dupla via (Harness + ProjectAdapter paralelo) é factível em 1 week? Ou devemos serial?"

**Resposta (Verbatim):**

Dupla via é factível, mas **COM risco controlado**.

**Dependências entre trilhas:**

Trilha A (Harness) e Trilha B (ProjectAdapter) são **loose coupling**:
- Harness testa capabilities (agnostic de onde os dados vêm)
- ProjectAdapter descobre estrutura (agnostic de como capabilities são testadas)
- Cruzam só em Q5 (BootstrapGate validation) — late stage

**Então:** Podem rodar paralelo Dias 1-4 sem blocking.

**Critical path:**
- A (Harness): mais straightforward, menos risco
- B (ProjectAdapter): mais complexo, mais risco
- **Recomendação:** Harness é "safety net" — se B atrasa, A já está pronto

**Acoplamento real aparece Dia 2-3:**
- SME (Q5) disse: refatoração Meu PDI é PRÉ-REQUISITO
- Isso afeta B, não A
- A continua independente

**Fallback:**
- Se B falha: A (Harness) ≥80% já entrega valor (confira capabilities)
- Se A falha: B (ProjectAdapter) pode continuar, mas sem validação confiança
- Melhor cenário: A passes, B derisked — ambos ✅

**Veredito:** Dupla via é **VIÁVEL COM RISCO BAIXO** pq loose coupling. Harness é safety net.

**Síntese:** Loose coupling, A é safety net, B is critical path. Dupla via viável com risco baixo.

---

## Q2: Pacing para Dia 2 Milestone

**Pergunta:**
> "Como você estruturaria Dia 1-2 pra ter dados suficientes no milestone decision do Dia 2?"

**Resposta (Verbatim):**

Pacing seria:

**Dia 1 (Seg):**
- **A1 (Harness tests):** Start, aim ≥20% coverage (low-hanging fruit)
- **B1 (ProjectAdapter):** Design phase (não code, só arquitetura)
- **B-Refactor:** Start refatoração Meu PDI (SME priority)

**Dia 2 (Ter, até 16:00 milestone):**
- **A1:** ≥50% coverage (phase 1 + start phase 2)
- **B1:** ≥30% code done (fase 1 + start fase 2)
- **B-Refactor:** ≥80% completo (domains/, config, etc.)
- **Validation:** SME testa ProjectAdapter em refactored Meu PDI

**Definition of Done pro Dia 2 Milestone:**

✅ **PASS Criteria:**
- Harness: ≥50% coverage achievable in codebase (no blocker encontrado)
- ProjectAdapter: Fase 1 code works, zero blocking architecture issues
- Refactoring: domains/ + infrastructure/ split complete, config canonical
- Both: zero external blockers (dependencies resolved, team unblocked)

❌ **FAIL Criteria:**
- Harness: <30% coverage (architecture broken)
- ProjectAdapter: <20% progress (scope issue)
- Refactoring: not >70% done (blocks ProjectAdapter testing)

**How to validate % of discovery:**

```
Dia 2 16:00:
- Deploy ProjectAdapter.analyze() against refactored Meu PDI
- Run: apos project_adapter analyze /path/to/meu-pdi
- Check: confidence_score ≥ 50% (proof it works)
- Check: zero errors (not just warnings)
```

**Success = "both tracks unblocked, confidence ≥50% ProjectAdapter works"**

Not "perfect", just "not doomed".

**Síntese:** Dia 1: A ≥20%, B design, refactor start. Dia 2: A ≥50%, B ≥30%, refactor ≥80%, validation run. Success = both unblocked, ≥50% confidence ProjectAdapter.

---

## Q3: Dores de Execução Paralela

**Pergunta:**
> "Qual é a maior dor de dupla via paralela? O quê mais quebra quando fazes paralelo?"

**Resposta (Verbatim):**

Maior dor: **Context switching + async blockers.**

**O que mais quebra em paralelo:**

1. **Context switching (developer mental model):**
   - Dev roda ProjectAdapter Dias 1-2, pensa "estrutura"
   - Dia 3 precisa rodar Harness tests, pensa "capabilities"
   - Brain switch = 30 min perda + bugs por distração
   - **Mitigation:** Não alternar same dev. Dedica Dev1 → ProjectAdapter, Dev2 → Harness.

2. **Async blockers que parecem independent:**
   - B (ProjectAdapter) assume refactoring feita
   - Refactoring é paralelizável com A (Harness)? SIM
   - Mas refactoring não é código; é renomear/mover arquivos
   - Se B começa antes refactoring 100% done, analisa "legacy" struktur
   - **Risk:** Dia 2, refactoring final 20%, B descobre padrão novo = rewrite
   - **Mitigation:** Refactoring strictly Dia 1 (não paralelo com B).

3. **Communication overhead:**
   - "Is refactoring done?" = 5 messages
   - "What's new in structure?" = 10 messages
   - Per day = 30+ async messages = 2-3h distraction
   - **Mitigation:** Standup 15 min 2x/day (09:00, 15:00). Async chat fora.

4. **Integration surprises Dia 2-3:**
   - A (Harness) assumes ProjectProfile format X
   - B (ProjectAdapter) produces format Y
   - They discover mismatch = 4-6h debug
   - **Mitigation:** Freeze ProjectProfile schema Dia 1 (no changes after).

**Velocity impact of parallelism:**
- **Serial:** 100% of estimated effort
- **Parallelism (loose coupling):** 95% of estimated effort (+5% overhead)
- **Our case:** Low overhead pq architecture is good

**Mitigations that work:**
- Dedicate devs (no context switching)
- Refactoring first (Dia 1 complete)
- Schema frozen (Dia 1)
- Standups (2x/day, 15 min each)
- Async discipline (chat only for status, not blocking decisions)

**Síntese:** Context switching + async blockers. Mitigations: dedicate devs, refactor first, schema frozen, 2x standups, async discipline. Overhead: ~5%.

---

## Q4: 2 SPs é suficiente?

**Pergunta:**
> "Você concorda que 2 SP por track (Harness + ProjectAdapter = 4 SP total + 1 buffer) é realista pra atingir milestone Dia 2?"

**Resposta (Verbatim):**

Não. 2 SP por track é **OTIMISTA**.

**Breakdown realista:**

```
Trilha A (Harness):
- Phase 1 (low-hanging): 0.5 SP (1 dia)
- Phase 2 (medium): 1.0 SP (2 dias)
- Estimate Dia 2: 1.0 SP done, 0.5 SP in progress = ≥50% coverage ✅

Trilha B (ProjectAdapter):
- Design: 0.5 SP (1 dia)
- Phase 1 (filesystem): 0.75 SP (1.5 dias)
- Phase 2 start: 0.5 SP (1 dia)
- Estimate Dia 2: 0.75 SP done = Phase 1 complete, Phase 2 started ✅

Trilha C (Refactoring Meu PDI — BLOCKING):
- Remove duplicity: 0.25 SP (0.5 dia)
- Reorganize domain/infrastructure: 0.75 SP (1.5 dias)
- Estimate Dia 2: 1.0 SP done = ≥80% complete ✅

TOTAL Dia 2: A (1.0 SP) + B (0.75 SP) + C (1.0 SP) = 2.75 SP
TOTAL full week: A (1.5 SP) + B (1.5 SP) + C (1.5 SP) = 4.5 SP
```

**So:**
- Dia 2 milestone: **2.75 SP** (not 2)
- Full week: **4.5 SP** (not 4)
- Plus buffer: **5.5 SP total** (not 5)

**Critical assumptions (if ANY break, timeline fails):**

1. **No major architecture discovery:** "This doesn't work" moments = add 2-3h each
2. **Refactoring is smooth:** No import cycles, no hidden dependencies = +20% if messy
3. **Dedicate devs:** No context switching = +30% if devs split attention
4. **ProjectProfile schema freezes Día 1:** No format changes = +1 day if changes
5. **Meu PDI has no hidden complexity:** No edge cases = +1 day if finds surprises

**Revised velocity:**
- If all assumptions hold: **4.5 SP in 1 week** ✓
- If 1-2 assumptions break: **3.5-4.0 SP** (tight)
- If 3+ assumptions break: **2.5-3.0 SP** (miss milestone)

**Veredito:** 2 SP per track is **OPTIMISTIC**. Real estimate: 2.75 SP Dia 2 (for pass criteria), 4.5 SP full week. **Add contingency buffer = 5.5 SP total.**

**Síntese:** 2 SP otimista. Realista: 2.75 SP Dia 2, 4.5 SP full week, 5.5 SP com buffer. Assumptions: smooth refactor, dedicate devs, schema frozen, no hidden complexity.

---

## Q5: Convergência Dia 2

**Pergunta:**
> "Se Dia 2 milestone vier bom (≥70% em ambos), como você estrutura Dia 3-5? E se vier ruim?"

**Resposta (Verbatim):**

3 planos contingentes:

**Plano A: SUCESSO (Dia 2: A ≥70% + B ≥70%)**

```
Dias 3-4: Paralelo convergência
- A (Harness): Fase 2 + Fase 3 → ≥80% coverage
- B (ProjectAdapter): Fase 2 + Fase 3 → ≥80% discovery
- Integração: ProjectAdapter output → BootstrapGate → KnowledgeGraph (validation)

Dia 5: Buffer + Polish
- A: Edge cases + refinement
- B: Semântica refinement + Meu PDI edge cases
- Integration tests: ProjectAdapter → Harness pipeline E2E

Outcome: Both tracks ≥80%, Sprint Goal achieved ✅
```

**Plano B: PARTIAL (Dia 2: A ≥70% + B <50%)**

```
Decision: Converge to Trilha A (Harness prioritário)

Dias 3-5: 100% Harness coverage
- A Phase 2 + Phase 3 + refinement → ≥80% coverage
- B (ProjectAdapter) → DESCOPE, move to Sprint 2

Outcome: Harness ≥80% ✅, ProjectAdapter postponed
Risk: Meu PDI onboarding delayed (CEO unhappy, but acceptable)
Rationale: "Coverage > Discovery; infrastructure > feature"
```

**Plano C: FAILURE (Dia 2: Both <60%)**

```
Decision: Pausar, reavaliar escopo

Dia 3: Root cause analysis
- "Why did both miss 60%?" → Refactoring incomplete? Architecture broken? Scope wrong?

Dias 3-5: Adjust
- Reduce scope (smaller coverage target, smaller discovery scope)
- OR extend timeline (ask exec for 10-12 days instead of 5)
- OR pivot (focus on one track only)

Outcome: Degraded, but honest; reset expectations
```

**Decisão tree:**

```
Dia 2 16:00 milestone check:
├─ A ≥70% AND B ≥70%?
│  └─ YES → Plano A (dupla via convergência)
├─ A ≥70% AND B <50%?
│  └─ YES → Plano B (100% Harness, descope ProjectAdapter)
├─ A <60% OR B <60%?
│  └─ YES → Plano C (RCA + replan)
```

**Order of Dias 3-5 (if Plano A):**

Dia 3:
1. Harness Phase 2 (medium difficulty)
2. ProjectAdapter Phase 2 (medium difficulty)
3. Start integration validation

Dia 4:
1. Harness Phase 3 + refinement
2. ProjectAdapter Phase 3 + heuristics
3. ProjectAdapter test in refactored Meu PDI
4. Integration edge cases

Dia 5:
1. Harness polish + edge cases
2. ProjectAdapter semântica refinement
3. E2E pipeline validation (ProjectAdapter → BootstrapGate → KnowledgeGraph)
4. Buffer

**Síntese:** Plano A (dupla via): Dias 3-4 paralelo, Dia 5 polish. Plano B (Harness only): descope ProjectAdapter. Plano C (RCA): replan. Decision tree claro.

---

## Q6: Risco Arquitetural?

**Pergunta:**
> "Você vê riscos arquiteturais em ProjectAdapter ou integração com BootstrapGate que precisam ser mitigados **antes** de Sprint 2?"

**Resposta (Verbatim):**

Sim, 3 riscos arquiteturais críticos:

**Risco 1: ProjectProfile Schema Coupling**

**Problema:** ProjectAdapter produz `ProjectProfile` dict. BootstrapGate espera schema X. Se divergem, integração quebra.

**Mitigação:** 
- **Timing:** Dia 1 (AGORA, não Dia 3)
- **PoC:** Design spec, compartilhe com ambos times
- **Validação:** Mock test (ProjectAdapter mock output → BootstrapGate mock input)

**Criticality:** 🔴 BLOCKING — se não faz PoC Dia 1, Dia 2 descobrem incompatibilidade.

---

**Risco 2: Refactoring Meu PDI não completo Dia 2**

**Problema:** ProjectAdapter assume estrutura refactored (domain/, canonical config). Se refactoring atrasa, ProjectAdapter accuracy cai para 50%.

**Mitigação:**
- **Timing:** Dia 1-2 (refactoring first, no delays)
- **PoC:** Validate refactoring 80% complete antes ProjectAdapter Fase 2
- **Validation:** ProjectAdapter test run em partially-refactored Meu PDI (Dia 2 EOD)

**Criticality:** 🔴 BLOCKING — refactoring must complete Dia 2, not Dia 3.

---

**Risco 3: Semântica Inference não confiável**

**Problema:** ProjectAdapter usa heuristics pra inferir domain semantics (Signal = entity, Signal → Order = relationship). Heuristics podem errar 40% das vezes.

**Mitigação:**
- **Timing:** Dia 2 (validate heuristics against real Meu PDI)
- **PoC:** Run heuristics on refactored Meu PDI, manually check 10 entities. If ≥70% correct, proceed. If <70%, redesign heuristics.
- **Validation:** SME reviews ProjectAdapter ontology output Dia 2, says "yes/no/needs refine"

**Criticality:** 🟠 MEDIUM — if heuristics fail, ProjectAdapter discovery drops to 60%, still usable but needs manual refinement.

---

**Additional risk: Integration with BootstrapGate + ContextEngine**

**Problem:** ProjectProfile → BootstrapGate → ContextEngine. What if ContextEngine can't consume ProjectProfile format?

**Mitigation:**
- **Timing:** Dia 1 (align with ContextEngine team)
- **PoC:** Design spec, walkthrough with ContextEngine tech lead
- **Validation:** No code needed; just agreement on data contract

**Criticality:** 🟡 LOW — loose coupling, easy to fix if problem found early.

---

**Mitigation Summary:**

| Risk | Mitigation | Timing | PoC Type | Criticality |
|------|-----------|--------|----------|------------|
| ProjectProfile schema | Design spec + mock test | Día 1 | Spec + code | 🔴 BLOCKING |
| Refactoring incomplete | Validate 80% Día 2 | Día 1-2 | Validation | 🔴 BLOCKING |
| Semántica heuristics | Test on Meu PDI Día 2 | Día 2 | Validation | 🟠 MEDIUM |
| ContextEngine integration | Alignment call Día 1 | Día 1 | Spec | 🟡 LOW |

**Timeline: Risk mitigation starts NOW, not Día 3.**

**Síntese:** 3 critical risks (ProjectProfile schema, refactor incomplete, semántica heuristics) + 1 low (integration). Mitigation starts Día 1, not Día 3.

---

## Q7: Velocity Baseline Confirmado?

**Pergunta:**
> "R0 velocity foi ~7 SP/week. Você confirma que 4.5 SP + buffer em R1.1 é realista? Ou ajustamos?"

**Resposta (Verbatim):**

R0 was 7 SP/week, but contexto era diferente. R1 Sprint 1 é **TIGHTER**.

**Por quê R0 = 7 SP/week:**
- Scaffold (new repo setup, basic tests, docs) = straightforward, bem-understood
- Team was aligned, minimal discovery needed
- 4 tasks, all delivered 100%

**Por quê R1 Sprint 1 é diferente:**
- Dupla via = parallelism overhead
- Refactoring Meu PDI = unpredictable (legacy code, hidden dependencies)
- New module (ProjectAdapter) = architecture validation needed
- Integration risk (BootstrapGate, ContextEngine) = unknown unknowns

**Velocity adjustment:**

```
R0: 7 SP/week (baseline, well-understood scope)

R1.1: 4.5 SP realistic estimate
     = 64% of R0 velocity
     = ~2-3 day loss due to:
       - Parallelism overhead: 0.5 SP
       - Refactoring unknown: 0.75 SP
       - Architecture validation: 0.5 SP
       - Integration risk: 0.75 SP

R1.2-1.3 (after validation): Expect 6-7 SP/week again (back to normal once risks mitigated)
```

**Revised velocity baseline for R1:**

| Sprint | Estimate | Confidence | Notes |
|--------|----------|------------|-------|
| R1.1 (1-week) | 4.5 SP | 70% | First sprint, new module, risks high |
| R1.2 (1-week) | 5.5-6.0 SP | 80% | Risks mitigated, velocity recovering |
| R1.3+ (1-week) | 6.5-7.0 SP | 85% | Normal velocity, mature module |

**What changed vs R0:**

1. **Complexity:** ProjectAdapter is new, requires validation (vs R0 scaffold = straightforward)
2. **Scope:** Dupla via = more work in parallel (vs R0 sequential)
3. **Risk:** Refactoring Meu PDI unknown (vs R0 known codebase)
4. **Team:** Same team, but context-switching overhead (vs R0 focused)

**Sanity check: Is 4.5 SP realistic?**

Yes, if:
- Refactoring happens Día 1 (not spread)
- Schema freezes Día 1 (not evolves)
- No major architecture discovery (plan for edge cases)
- Team is full-time (no distractions)

**If conditions break:** Velocity drops to 3-3.5 SP (worst case).

**Veredito:** R1.1 = 4.5 SP realista (64% of R0). R1.2+ recover to 6-7 SP. Honest assessment: first sprint of new module is always slower.

**Síntese:** R0 = 7 SP/week (understood scope). R1.1 = 4.5 SP (new module, parallelism, refactor unknown). R1.2+ = 6-7 SP (back to normal). Velocity drops 64% due to complexity/novelty.

---

## 📊 Síntese Executiva — Entrevista 3

| Aspecto | Finding | Criticidade |
|---------|---------|------------|
| **Dupla via viável?** | Sim, loose coupling, A é safety net | ✅ VIÁVEL |
| **Pacing Dia 1-2** | A ≥50%, B ≥30%, refactor ≥80%, validate run | ✅ CLARO |
| **Dores paralelo** | Context switching + async blockers (mitigável) | ⚠️ CONTROLADO |
| **2 SP por track** | Otimista; realista 2.75 SP Dia 2, 4.5 SP full week | ⚠️ APERTADO |
| **Convergência Dia 2** | 3 planos (A: success, B: partial, C: failure) | ✅ PREPARADO |
| **Riscos arquiteturais** | 3 críticos (schema, refactor, heuristics) + 1 baixo | ⚠️ MITIGÁVEL |
| **Velocity R1 vs R0** | 4.5 SP (64% of R0); R1.2+ recover to 6-7 SP | ⚠️ REALISTA |

---

## ✅ Recomendações Críticas

1. **DUPLICATE DEV TEAMS (não alternar):**
   - Dev1 → ProjectAdapter (full week)
   - Dev2 → Harness (full week)
   - Reduz context switching loss

2. **REFACTORING STRICTLY DIA 1** (não spread)
   - Must be 100% done before ProjectAdapter Fase 2
   - Mitigates uncertainty

3. **SCHEMA FROZEN DIA 1** (no changes after)
   - ProjectProfile format locked
   - Prevents integration surprises

4. **2x DAILY STANDUPS** (09:00, 15:00, 15 min each)
   - Sync dependencies early
   - Reduce async overhead

5. **POC RISK MITIGATIONS DIA 1:**
   - ProjectProfile schema validation (mock test)
   - ContextEngine integration alignment
   - Start ahead, don't discover Dia 3

6. **MILESTONE SUCCESS = "BOTH UNBLOCKED"**
   - Not perfect, just not doomed
   - A ≥50%, B ≥30%, refactor ≥80%

---

**Entrevista concluída:** 2026-07-22 15:00  
**Status:** ✅ PRONTA PARA SÍNTESE
