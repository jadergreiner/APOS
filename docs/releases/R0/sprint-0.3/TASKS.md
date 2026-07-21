# Sprint Tasks — 0.3

**Sprint:** 0.3 - Beta Prep (MVP Implementation)  
**Status:** 🔄 Em Progresso — Dia 2 em andamento (2026-07-23)  
**Estimado:** ~6.5 dias (paralelizacao esperada)  
**Atual:** 40% completo (T0.3.1 + T0.3.2 + T0.3.3 = 100%; T0.3.4 iniciando)  
**Personas:** Jader (Dev) + AI Architect + Product Ops + Early Adopter (Piloto)

---

## Task Naming Convention

- **T{release}.{sprint}.{number}** — Task ID
  - Ex: T0.3.1, T0.3.2

---

## Tarefas

### Tier 1: Core / Must-Have

| ID | Titulo | Descricao | Duracao | Personas | Status |
|----|--------|-----------|---------|----------|--------|
| T0.3.1 | Especificacao Tecnica (SPEC.md) | Design Plugin Jira + Trust Score + Deteccao Orfas; arquitetura; fluxo dados | 1.5d | Jader | ✅ 100% |
| T0.3.2 | Design de API REST | Endpoints: /tasks, /okrs, /relationships, /trust-score; schemas; validacoes | 1.5d | Jader | ✅ 100% |
| T0.3.3 | Implementacao Plugin Jira | Integracao Jira API; webhooks; auto-deteccao features orfas; UI plugin | 2d | Jader | ✅ 100% |
| T0.3.4 | Trust Score Engine | Implementacao 0.0-1.0 score; calculo (coverage, quality, consistency); validacoes | 1.5d | Jader | ✅ 100% |

### Tier 2: Important / Should-Have

| ID | Titulo | Descricao | Duracao | Personas | Status |
|----|--------|-----------|---------|----------|--------|
| T0.3.5 | Piloto com 3 Personas | Deploy em sandbox + onboarding (AI Architect, Ops, Early Adopter); feedback cycles | 2d | Piloto + Jader | 📋 Planejado |
| T0.3.6 | Metricas Baseline + Tracking | Setup monitoring (reexplicacao tempo, adoption, trust score accuracy); dashboard | 1d | Ops + Jader | 📋 Planejado |

### Tier 3: Support / Nice-to-Have

| ID | Titulo | Descricao | Duracao | Personas | Status |
|----|--------|-----------|---------|----------|--------|
| T0.3.7 | Documentacao Completa | README, API docs, tutorial, troubleshooting | 1d | Jader | 📋 Planejado |
| T0.3.8 | Testing + QA | Testes unitarios, integracao, edge cases; validacao de dados | 0.5d | Jader | 📋 Planejado |

---

## Progress Summary (Dia 2 — 2026-07-23)

| Task | Completion | Commits | Lines | Notes |
|------|----------|---------|-------|-------|
| T0.3.1 (Spec) | ✅ 100% | 7 | — | SPEC.md finalizado D1 |
| T0.3.2 (API) | ✅ 100% | 4 | — | API_DESIGN.md finalizado D1 |
| T0.3.3 (Plugin) | ✅ 100% | 3 | 2591 | **5h/5h** Phase 1-4 completo! |
| T0.3.4 (Score) | ✅ 100% | 1 | 1122 | 18/18 testes passing, 3 componentes |
| T0.3.5-8 | 📋 0% | — | — | Prontos para iniciar (D3) |
| **Total** | **60%** | **15** | **3713** | +5 horas ahead! ✅ |

---

## Timeline Estimado

```
D1 (22 jul): T0.3.1 (Spec) + T0.3.2 (API) paralelo
D2 (23 jul): T0.3.3 (Plugin Jira) + T0.3.4 (Trust Score) paralelo
D3 (24 jul): T0.3.5 (Piloto) comeca
D4-5 (25-26 jul): T0.3.5 (Piloto feedback cycles)
D5-6 (26-27 jul): T0.3.6 (Metricas) + T0.3.7 (Docs) + T0.3.8 (Testing)
D7 (29 jul): Consolidacao + Piloto final + Decisao

Estimado: 6.5d (compreensao com paralelizacao)
Meta: Completar em ~5 dias (como Sprint 0.2)
```

---

## Dependencias

```
T0.3.1 (Spec) ┐
              ├─→ T0.3.3 (Plugin Jira)
T0.3.2 (API)  ┘

T0.3.2 (API) ─→ T0.3.4 (Trust Score)

T0.3.3 + T0.3.4 ─→ T0.3.5 (Piloto)

T0.3.5 ─→ T0.3.6 (Metricas)

Paralelo: T0.3.7 (Docs) + T0.3.8 (Testing) podem correr com qualquer coisa
```

---

## Criterios de Sucesso por Tarefa

### T0.3.1 - Especificacao Tecnica ✅

**Deliverable:** SPEC.md (completo)

**Criterios:**
- [ ] Arquitetura definida (camadas: Jira → Semantic Layer → Trust Score)
- [ ] Fluxo de dados documentado (task → ontology → score)
- [ ] Deteccao de orfas: logica clara (feature sem OKR = orfao)
- [ ] Edge cases mapeados (tarefas sem project, OKRs sem metricas, etc)
- [ ] Validado por: Jader (10/10) + Review informal (AI Architect, se disponivel)

---

### T0.3.2 - Design de API REST ✅

**Deliverable:** API_DESIGN.md (schemas, endpoints, validacoes)

**Criterios:**
- [ ] 4 endpoints principais: GET /tasks, GET /okrs, GET /relationships, GET /trust-score
- [ ] Schemas JSON definidos (task, okr, relationship, score)
- [ ] Status codes: 200, 400, 404, 500 documentados
- [ ] Validacoes: business logic (score nunca > 1.0, nunca < 0.0)
- [ ] Rate limiting pensado (piloto vai bater a API frequentemente)
- [ ] Validado por: Jader + Code review

---

### T0.3.3 - Plugin Jira ✅

**Deliverable:** Plugin funcional + PLUGIN_README.md

**Criterios:**
- [ ] Conecta com Jira API (auth, webhooks)
- [ ] Auto-detecta "features orfas" (issue sem OKR custom field)
- [ ] UI: sidebar + modal de "vincular OKR"
- [ ] Performance: <500ms para queries (AI Architect requiremento)
- [ ] Setup: <30 min (Early Adopter requiremento)
- [ ] Testado em: Jira sandbox + versoes multiplas

---

### T0.3.4 - Trust Score Engine ✅

**Deliverable:** trust_score.py (classe + testes)

**Criterios:**
- [ ] Score 0.0-1.0 calculado corretamente
- [ ] Metricas: coverage (quanto da ontologia representado), quality (dados validos), consistency (sem contradicoes)
- [ ] Weights: 0.3 coverage + 0.5 quality + 0.2 consistency (tweavel)
- [ ] Edge cases: grafo vazio = 0.0, grafo perfeito = 1.0
- [ ] Documentacao: formula clara, exemplos com dados reais
- [ ] Testado: >80% cobertura (pytest)

---

### T0.3.5 - Piloto com 3 Personas ✅

**Deliverable:** PILOT_FEEDBACK.md (sintese + actionitems)

**Criterios:**
- [ ] 3 personas onboarded (<30 min cada)
- [ ] Usando Plugin Jira por 3-5 dias (dados reais, nao simulados)
- [ ] Feedback coletado: o que funcionou, o que nao, ideias
- [ ] Trust Score testado em seus proprios dados
- [ ] Metricas baseline coletadas (tempo reexplicacao antes/depois)
- [ ] Condicional (EM): agora pronto para "sim"?

---

### T0.3.6 - Metricas + Tracking ✅

**Deliverable:** METRICS_BASELINE.md (completo) + dashboard/script

**Criterios:**
- [ ] Baseline antes (reexplicacao = 2-3h/semana; desperdicio = 15-20%)
- [ ] Baseline depois (target: <30 min/semana; desperdicio < 5%)
- [ ] Adoption metric: % of piloto users still using dia 7 (target: 80%+)
- [ ] Trust Score accuracy: falsos positivos <5%
- [ ] Plugin latencia: <500ms P95
- [ ] Relatório consolidado pronto para apresentar

---

### T0.3.7 - Documentacao ✅

**Deliverable:** README.md + API_DOCS.md + TUTORIAL.md

**Criterios:**
- [ ] README: quick start (<5 min), high-level overview
- [ ] API_DOCS: todos endpoints, schemas, exemplos de curl
- [ ] TUTORIAL: passo-a-passo para setup + primeiro uso
- [ ] Troubleshooting: FAQ, erros comuns + solucoes
- [ ] Qualidade: zero broken links, grammar check, consistent

---

### T0.3.8 - Testing ✅

**Deliverable:** test_plugin.py + test_trust_score.py + report

**Criterios:**
- [ ] Unit tests: >80% cobertura (trust_score.py)
- [ ] Integration tests: Plugin + API + Jira mock
- [ ] Edge cases: vazio, perfeito, dados corrompidos
- [ ] Performance: timeout tests (<500ms)
- [ ] All tests pass before Deploy
- [ ] Coverage report gerado

---

## Bloqueadores Conhecidos & Mitigacoes

| Bloqueador | Severity | Mitigacao |
|-----------|----------|----------|
| Acesso Jira sandbox nao garantido | 🟡 Media | Usar test account ou mock API |
| Personas nao disponivel 100% tempo | 🟡 Media | Agendamento flexivel, feedback async |
| Trust Score calculo pode ser complexo | 🟡 Media | Comece com versao simples, itere |

---

## Outputs de Qualidade (Documentacao Desde D1)

**Sprint 0.3 aplica Lição #5 de 0.2:** "Documentacao completa desde dia 1"

Documentos prontos ANTES de D1:
- ✅ README.md (este arquivo)
- ✅ SPEC.md (template pronto)
- ✅ API_DESIGN.md (template pronto)
- ✅ PILOT_PLAN.md (template pronto)
- ✅ METRICS_BASELINE.md (template pronto)
- ✅ BOARD.md (template kanban)
- ✅ STATUS.md (template burndown)
- ✅ RETRO.md (template vazio, preenchido ao final)
- ✅ DAILY_STANDUP_TEMPLATE.md (template reusavel)
- ✅ RISK_MITIGATION.md (template pronto)

**Meta:** Zero template vazio = zero retrabalho

---

---

## Sprint Velocity & Projections

```
D1 (2026-07-22):
  ✅ T0.3.1 (Spec) — 1.5d estimate, ~6h actual (parallelizable)
  ✅ T0.3.2 (API) — 1.5d estimate, ~4h actual (parallelizable)
  Status: 3d estimated work done in 1d (3x parallelization bonus!)

D2 (2026-07-23):
  ✅ T0.3.3 (Plugin Jira) — 2d estimate, 5h actual (4 phases @ 1h-1.5h)
  🔄 T0.3.4 (Trust Score) — 1.5d estimate, INICIANDO
  Status: +40% ahead of 80% target

Projeção D3+:
  T0.3.4 → T0.3.5 (Piloto) → T0.3.6-8 (Metrics + Docs + QA)
  Esperado: Completar Sprint 0.3 por 2026-07-26 (~4d real vs 6.5d estimado)
```

---

**Sprint Status:** 🔄 Em Andamento (Dia 2)  
**Próxima Atualizacao:** 2026-07-23 (Dia 2 — T0.3.4 iniciado)  
**Ultimo atualizado:** 2026-07-23T13:45:00Z
