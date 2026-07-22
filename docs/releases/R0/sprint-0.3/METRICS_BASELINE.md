# Sprint 0.3 - Metricas Baseline & Tracking

**Sprint:** 0.3 - Beta Prep (MVP Implementation)  
**Data:** 2026-07-20 (Pre-planning)  
**Status:** 📋 Baseline definida — Sera preenchida durante piloto  
**Owner:** Jader + Product Ops persona

---

## 1. Objetivos

Medir impacto do MVP (Plugin Jira + Trust Score) em 3 personas:

1. **Setup Accessibility** — Plugin pronto para usar em <30 min
2. **Functional Correctness** — Deteccao de orfas + Trust Score funciona
3. **Performance** — API responde rápido (<500ms)
4. **Adoption** — Personas continuam usando (Dia 7)
5. **Business Impact** — Reducao real de retrabalho (2-3h → <30min/semana)

---

## 2. Baseline Metrics (ANTES do Piloto)

### 2.1 Contexto Desatualizado (Sprint 0.2 Discovery)

**Metrica:** Tempo gasto em "reexplicacao de contexto" por semana

| Persona | Baseline | Fonte |
|---------|----------|-------|
| PM Leader (Sarah) | 2-3h/semana | Entrevista #1 Sprint 0.2 |
| Product Ops | 60-80h/mes (40% do time) | Entrevista #4 Sprint 0.2 |
| Early Adopter (Jader) | 15-20% esforco desperdicado | Entrevista #6 Sprint 0.2 |

**Traducao para metricas:**
- Sarah: ~0.5-0.75 trabalhos perdidos por semana
- Ops: ~10 horas/semana de retrabalho
- EA: ~1-2 horas/semana em "cacar contexto"

### 2.2 Features Orfas (Sem OKR)

**Metrica:** % de tasks sem OKR linkado

| Persona | Baseline | Como Medir |
|---------|----------|-----------|
| AI Architect | ~40-60% (estimado) | Jira query: tasks count / linked tasks |
| Product Ops | ~50% (auto-report) | Confluence/OKR doc vs Jira |
| Early Adopter | ~30% (menor, mais disciplined) | Self-report |

**Target after MVP:** <10% orphan rate

### 2.3 Setup Time (Nova Ferramenta)

**Baseline:** 60-120 min (típico para plugins Jira)

**Target:** <30 min

---

## 3. Metricas de Implementacao (DURANTE Piloto)

### 3.1 Plugin Setup & Adoption

**Metrica:** Setup time de onboarding (Dia 1)

```
Persona 1 (AI Architect):  _____ min (clock start → dados synced)
Persona 2 (Ops):           _____ min
Persona 3 (Early Adopter): _____ min
Average:                   _____ min

Target: < 30 min TODOS 3
Status: ✅ PASS or ❌ FAIL
```

**Metrica:** Plugin crashes durante piloto

```
Persona 1: _____ crashes (zero esperado)
Persona 2: _____ crashes
Persona 3: _____ crashes

Target: 0 crashes
Status: ✅ PASS or ❌ FAIL
```

**Metrica:** Adoption (usuarios ativos Dia 7)

```
Dia 1: 3/3 personas onboarded
Dia 2: 3/3 usando plugin (exploracao)
Dia 3: 3/3 usando plugin
Dia 4: 3/3 usando plugin (post-fix round)
Dia 5: 3/3 usando plugin
Dia 6: 3/3 usando plugin (final testing)
Dia 7: _____ /3 ainda usando sem prompt

Target: 3/3 (100%)
Metrica: Retention after pilot = 80%+ continuam apos 7 dias
Status: ✅ PASS or ❌ FAIL
```

### 3.2 Deteccao de Orfas (Accuracy)

**Metrica:** False Negatives (orfas que plugin nao detectou)

```
AI Architect:
  - Manual count: _____ orfas em seus tasks
  - Plugin count: _____ orfas detectadas
  - False Negatives: _____ (diferenca)
  - FN Rate: _____% (target: 0%)

Product Ops:
  - Manual count: _____
  - Plugin count: _____
  - FN Rate: _____% (target: 0%)

Early Adopter:
  - Manual count: _____
  - Plugin count: _____
  - FN Rate: _____% (target: 0%)

Average FN Rate: _____%
Target: 0% (nenhuma orfa perdida)
Status: ✅ PASS or ❌ FAIL
```

**Metrica:** False Positives (tasks marcadas como orfas que NAO sao)

```
AI Architect:
  - Plugin marked as orphan: _____ items
  - After review, true orphans: _____ items
  - False Positives: _____
  - FP Rate: _____%

Ops + EA: (similar)

Average FP Rate: _____%
Target: < 5% (alguns falsos positivos aceitavel)
Status: ✅ PASS or ⚠️ CONDITIONAL or ❌ FAIL
```

### 3.3 Trust Score Accuracy

**Metrica:** Score prediction accuracy (valida contra manual assessment)

```
Methodology:
1. Para cada persona, seleciona 5-10 tasks com OKR linkado
2. Manual assess: "quao confiavel e esse link?" (0.0-1.0)
3. Plugin calcula: Trust Score para esse task
4. Compara: manual vs plugin score (diferenca deve ser <0.2)

Results:
  Persona 1 (AI): Avg diff = ______ (target: <0.2)
  Persona 2 (Ops): Avg diff = ______
  Persona 3 (EA): Avg diff = ______
  
Overall Accuracy: ______%
Target: >85% accurate
Status: ✅ PASS or ❌ FAIL
```

### 3.4 API Performance

**Metrica:** Latencia P95 durante piloto

```
Monitoring setup:
  - Backend logs latencia de cada /api call
  - Collect durante Dia 1-6

Latencia P95 (99th percentile):
  Dia 1-2 (initial): _____ ms
  Dia 3-4 (after fix): _____ ms
  Dia 5-6 (final): _____ ms
  
Target P95: < 500 ms
Status: ✅ PASS or ⚠️ CONDITIONAL (<750ms) or ❌ FAIL
```

**Metrica:** Error rate (4xx, 5xx responses)

```
Total API calls: _____
Error calls (4xx+5xx): _____
Error rate: _____%

Target: < 2% error rate
Status: ✅ PASS or ❌ FAIL
```

### 3.5 Plugin Performance

**Metrica:** Load time (tiempo desde open Jira ate plugin ready)

```
Persona 1: _____ ms
Persona 2: _____ ms
Persona 3: _____ ms

Average: _____ ms
Target: < 3000 ms (3 seg)
Status: ✅ PASS or ❌ FAIL
```

---

## 4. Impacto de Negocio (DEPOIS do Piloto)

### 4.1 Reexplicacao de Contexto (Time Saved)

**Baseline:** 2-3h/semana por PM

**Medida:** Personas self-report (before/after)

```
PM Leader (Sarah):
  Before: "Gasto 2-3h/semana reexplicando 'por que' dessa feature"
  After: "Agora, com plugin mostrando Task→OKR, leva _____ min/semana"
  
  Reducao: _____ % (target: 80% = 2-3h → 30 min)

Product Ops:
  Before: "60-80h/mes em roll-up manual"
  After: "Agora dashboard auto-consolida, ~_____ h/mes"
  
  Reducao: _____ % (target: 80% = 60h → 12h)

Early Adopter:
  Before: "15-20% do tempo caçando 'qual era o contexto dessa task?'"
  After: "Agora, ~_____ % desperdicado"
  
  Reducao: _____ % (target: 80%)
```

### 4.2 Feature Orphan Rate

**Baseline:** 40-60% (discovered in interviews)

**After Piloto:**

```
AI Architect:
  Before: _____ orfas / _____ total tasks = _____ % orphan rate
  After: _____ orfas / _____ total tasks = _____ % orphan rate
  
  Reducao: _____ % (target: <10% orphan rate by end of sprint)

Ops + EA: (similar)
```

### 4.3 NPS & Satisfaction

**Metrica:** Net Promoter Score

```
Question: "Quanto você recomendaria APOS para um colega?"
Scale: 0-10

Persona 1 (AI): ___/10 (Promoter if >8, Passive if 7-8, Detractor if <7)
Persona 2 (Ops): ___/10
Persona 3 (EA): ___/10

NPS = (# Promoters - # Detractors) / Total × 100
    = (_____ - _____) / 3 × 100 = _____

Target NPS: >50 (excellent)
Status: ✅ PASS or ⚠️ CONDITIONAL (30-50) or ❌ FAIL (<30)
```

**Metrica:** Open feedback

```
"Qual foi a melhor coisa?"
  Persona 1: _____________________________
  Persona 2: _____________________________
  Persona 3: _____________________________

"Qual foi a pior coisa?"
  Persona 1: _____________________________
  Persona 2: _____________________________
  Persona 3: _____________________________

"O que teria mudado sua mente se tivesse sido diferente?"
  (captura criticas potencialmente fatais)
```

---

## 5. Go/No-Go Decision Criteria

**To ship MVP after Sprint 0.3:**

| Criterio | Peso | Alvo | Resultado | Pass? |
|----------|------|------|-----------|-------|
| Setup time <30 min | High | 3/3 personas | _____/3 | ✅/❌ |
| Deteccao orfas 0% FN | High | 100% | _____% | ✅/❌ |
| Deteccao orfas <5% FP | High | <5% | _____% | ✅/❌ |
| Trust score >85% accurate | Medium | >85% | _____% | ✅/⚠️/❌ |
| API <500ms P95 | Medium | <500ms | _____ms | ✅/⚠️/❌ |
| Adoption 3/3 Dia 7 | High | 100% | _____% | ✅/❌ |
| NPS >50 | High | >50 | _____ | ✅/⚠️/❌ |
| Business impact (reexpl) | High | >80% savings | _____% | ✅/⚠️/❌ |

**Decision:**
- ✅ GREEN: 6+ High passed → SHIP MVP (R1 planning)
- ⚠️ YELLOW: 5 High + some Medium conditional → ITERATE 1 week, re-test
- ❌ RED: <5 High passed → Back to drawing board (R0.3.1)

---

## 6. Tracking During Piloto

**Daily:** Update STATUS.md com metrics-in-progress

```markdown
## Metrics So Far

| Metrica | Dia 1 | Dia 2 | Dia 3 | Dia 4 | Dia 5 | Dia 6 | Alvo |
|---------|-------|-------|-------|-------|-------|-------|------|
| Setup time avg | 28 min | — | — | — | — | — | <30 |
| Adoption | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| Plugin crashes | 0 | 0 | 1* | 1* | 0 | 0 | 0 |
| API latencia P95 | 420ms | 380ms | 560ms* | 380ms | 350ms | 340ms | <500 |
| Orphan FN rate | — | 2%* | 0% | 0% | 0% | 0% | 0% |

*Fixado Dia 4
```

---

**Status:** 📋 Baseline definida  
**Preenchimento:** Dias 1-6 de piloto (24-29 julho)  
**Decision:** Dia 6, final call (29 julho, 3pm UTC)

