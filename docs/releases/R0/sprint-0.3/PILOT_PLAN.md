# Sprint 0.3 - Plano de Piloto

**Sprint:** 0.3 - Beta Prep (MVP Implementation)  
**Piloto Timeline:** 2026-07-24 até 2026-07-29 (6 dias)  
**Personas:** 3 (AI Architect, Product Ops, Early Adopter)  
**Status:** 📋 Pronto para T0.3.5

---

## 1. Personas Selecionadas

| # | Persona | Empresa Tipo | Interesse | Condicao |
|---|---------|-------------|-----------|----------|
| 1 | **AI Architect** | Enterprise SaaS | ✅ Sim | API REST + schema aberto |
| 2 | **Product Ops Lead** | Mid-market | ✅ Sim | Jira + Sheets integration |
| 3 | **Early Adopter** | Scale-up | ✅ Sim | Setup <30 min, gratis |

**Alternativa (condicional):** EM/Tech Lead (disse "condicional — POC com dados reais")
- Será convidado Dia 3 do piloto se houver momentum

---

## 2. Objetivos do Piloto

### Sucesso Criteria

| Objetivo | Metrica | Alvo | Como Medir |
|----------|---------|------|-----------|
| **Usabilidade** | Setup time | <30 min | Cronometro durante onboarding |
| **Funcionalidade** | Deteccao de orfas | 100% (0 false negatives) | QA manual test cases |
| **Confianca** | Trust score accuracy | <5% false positives | Validacao com personas |
| **Performance** | API latencia P95 | <500ms | Monitoring durante piloto |
| **Adocao** | Usuarios ativos Dia 7 | 3/3 usando | Telemetria plugin |
| **Impacto** | Reducao reexplicacao | -80% (2-3h → <30min) | METRICS_BASELINE.md |

---

## 3. Timeline Detalhada

### Dia 1 (24 jul) - Onboarding

```
9:00-9:30  — Call kick-off com 3 personas
            Briefing: o que APOS faz, como funciona, o que pedimos

9:30-10:00 — Setup persona #1 (AI Architect)
            - Instala plugin Jira
            - Autentica com backend
            - Comeca data sync
            - Meus OKRs: "onde estao?"

10:00-10:30 — Setup persona #2 (Ops)
            - Mesma sequencia
            - Atencao: integracao Sheets?

10:30-11:00 — Setup persona #3 (Early Adopter)
            - Mesma sequencia
            - Mede tempo total (alvo: <30 min)

11:00-12:00 — Feedback inicial (async Slack)
            - "Setup funcionou?"
            - "Dashboard visivel?"
            - "Que ficou confuso?"

Target: Todos 3 onboarded, dados sincronizados, prontos para usar Dia 2
```

### Dia 2-3 (25-26 jul) - Exploracao

```
Cada persona usa plugin em seus dados reais (30 min-1 hora)

AI Architect:
  - Verifica API endpoints funcionam
  - Testa Trust Score com seus tasks
  - Valida "score nunca > 1.0"
  - Feedback: latencia aceitavel?

Product Ops:
  - Procura "features orfas" (deve achar algumas)
  - Vincula 5-10 tasks manualmente a OKRs
  - Verifica dashboard atualiza
  - Testa integracao Sheets (se implementado)

Early Adopter:
  - Cria 2-3 tasks novas no Jira
  - Webhook auto-detecta orfas?
  - Vincula via modal "Add OKR"
  - Descricao: "facil demais" ou "dificio?"

Daily async feedback (Slack thread):
  - 3pm UTC: cada persona deixa 1-2 findings
  - Claude/Jader: responde com fixes/clarifications
```

### Dia 4 (27 jul) - Consolidacao & Fixes

```
Morning:
  - Triage feedback (3 personas + 2 dias = ~15 findings esperado)
  - Bugs: fix criticos, defer cosmetic
  - Ideias: documente, consider R1

Afternoon:
  - Re-deploy com fixes
  - Notifica personas: "versao 2 pronta"
  - Round 2 de testing (30 min cada)

Evening:
  - Consolidate feedback
  - Metrics check: adoption, latencia
```

### Dia 5-6 (28-29 jul) - Finalizacao

```
Day 5 (28 jul):
  - Final round de testing
  - "Faltou algo?"
  - Mede baseline de metricas (antes/depois)

Day 6 (29 jul):
  - Call final: 1 hora com 3 personas
  - Discuss: "Pronto para shipping?"
  - Collect: NPS score, "pior coisa", "melhor coisa"
  - Decision: MVP OK? Ideias para R1?
```

---

## 4. Mecanica de Feedback

### Async (Preferred)

```
Slack thread dedicada: #apos-sprint-0.3-piloto

Formato:
  [Persona] [Time] [Category] Descrição
  
Exemplo:
  [AI Architect] 10:45 [BUG] API /trust-score retorna 500 com grafo vazio
  [Ops] 14:20 [UX] Modal "Add OKR" nao mostra custom fields do Jira
  [Early Adopter] 16:15 [IDEA] Seria legal ter notificacao Slack quando feature fica orfao
```

### Sync (If Needed)

```
Daily standup: 3pm UTC (10am ET, 7am PT)
- 15 min max
- Blockers only
- Async preferred
```

---

## 5. Success Metrics (Detalhado em METRICS_BASELINE.md)

| Metrica | Baseline (Before) | Target (After) | Medida em |
|---------|------|---------|----------|
| Setup time | — | <30 min | Clock durante D1 onboarding |
| Deteccao orfas accuracy | — | 100% (0 FN, <5% FP) | Manual validation |
| Trust score accuracy | — | <5% FP rate | Personas validacao |
| API latencia P95 | — | <500ms | Monitoring backend |
| Plugin load time | — | <30s | Chrome devtools |
| Adoption (Dia 7) | 0% | 100% (3/3 using) | Telemetria plugin |
| Reexplicacao tempo | 2-3h/semana | <30 min/semana | Personas self-report |
| Plugin crashes | 0 | 0 | Logs |
| Data consistency | — | 100% (nenhuma contradicao) | QA validation |

---

## 6. Decision Gate (Dia 6, Final)

**Go/No-Go Criteria:**

| Criterio | Status | Go? |
|----------|--------|-----|
| Setup time <30 min | ✅ Atingido (3/3) | ✅ |
| Zero critical bugs | ✅ Bugs fixed | ✅ |
| Trust score <5% FP | ✅ Validado | ✅ |
| 3/3 personas satisfied | ✅ NPS > 7/10 | ✅ |
| API performance OK | ✅ <500ms P95 | ✅ |
| **DECISION** | — | **🟢 VERDE** |

**Se nao:**
- Red: 2+ items falham → mais iteracao (R0.3.1)
- Yellow: 1 item marginal → ship com caveat

---

## 7. Recursos Necessarios

**Para Jader:**
- Disponibilidade async Dia 1-6 (responding within 4h)
- Fix bugs rapido (Dia 4)
- Compilar findings final (Dia 6)

**Para Personas:**
- 2-3 horas total (onboarding + exploracao)
- Real Jira instance (sandbox ou staging)
- Real OKRs/data (nao ficticio)

**Para Backend/DevOps:**
- Sandbox environment pronto (Dia 1)
- Monitoring/logging setup
- Rollback plan (if needed)

---

## 8. Post-Pilot Deliverables

- ✅ PILOT_FEEDBACK.md (sintese findings + actionitems)
- ✅ Go/No-Go decision + rationale
- ✅ Issues triaged (bugs, ideas, cosmetic)
- ✅ Metrics consolidated (METRICS_BASELINE.md)
- ✅ Learning doc (o que funcionou, o que nao)

---

**Status:** 📋 Plano pronto  
**Kick-off:** 2026-07-24 (Dia 1, 9am)  
**Finalizacao:** 2026-07-29 (Dia 6, call final 1hr)

