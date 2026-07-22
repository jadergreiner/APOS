# Sprint 0.2: Analise de Forcas (Jobs Framework)

**Sprint:** 0.2 - JTBD Deep Dive
**Framework:** Jobs to Be Done — Forcas de Progresso
**Data:** 2026-07-20
**Status:** ✅ COMPLETO (5/5 entrevistas)

---

## Matriz de Forcas por Persona

### Sumario Visual

| Forca | PM Leader | EM / Tech Lead | AI Architect | Product Ops | Early Adopter | Incidencia |
|-------|-----------|----------------|--------------|-------------|---------------|-----------|
| **Push** (dor) | ⚡ 9/10 | ⚡ 9/10 | ⚡ 8/10 | ⚡ 9/10 | ⚡ 8/10 | **5/5** |
| **Pull** (atracao) | 🔥 9/10 | 🔥 7/10 | 🔥 10/10 | 🔥 8/10 | 🔥 9/10 | **5/5** |
| **Habit** (status quo) | 🛑 8/10 | 🛑 7/10 | 🛑 6/10 | 🛑 7/10 | 🛑 8/10 | **5/5** |
| **Anxiety** (medo) | ⚠️ 7/10 | ⚠️ 7/10 | ⚠️ 7/10 | ⚠️ 8/10 | ⚠️ 8/10 | **5/5** |

---

## 1. Push Forces (O Que Empurra Para Solucao)

### 1.1 Contexto desatualizado / retrabalho

**Personas:** PM Leader, EM/Tech Lead, AI Architect
**Intensidade media:** 9/10
**Frequencia:** Constante (3-4x/semana)

| Persona | Manifestacao | Impacto |
|---------|-------------|---------|
| PM Leader | Reexplica "por que" 3-4x/semana | 2-3h/semana perdidas |
| EM / Tech Lead | 30-40% retrabalho por contexto incompleto | Features entregues e despriorizadas |
| AI Architect | 15-20% interacoes com alucinacao | 20-30% do time em remediacao |

> **Padrao central:** Todas as personas perdem tempo porque o contexto estrategico morre entre a decisao e a execucao. Nao e falta de documentacao inicial — e falta de **contexto vivo**.

### 1.2 Falta de visibilidade Task→OKR

**Personas:** PM Leader, EM/Tech Lead, Product Ops, Early Adopter
**Intensidade media:** 9/10

| Persona | Manifestacao | Impacto |
|---------|-------------|---------|
| PM Leader | Nao ve se feature move OKR ate a review | Planejamento cego |
| EM / Tech Lead | Nao consegue argumentar contra scope creep | "Task de 3d vira 5d" |
| Product Ops | 60% OKRs desalinhados com tarefas reais | Reports sem credibilidade |
| Early Adopter | 60% features "soltas" sem vinculo | 15-20% esforco desperdicado |

> **Padrao central:** Sem vinculo visivel Task→OKR, times trabalham em paralelo, features perdem prioridade sem comunicacao, e o desperdicio so e descoberto na review.

### 1.3 Desperdicio de tempo manual

**Personas:** PM Leader, Product Ops, AI Architect
**Intensidade media:** 8/10

| Persona | Manifestacao | Impacto |
|---------|-------------|---------|
| PM Leader | Reunioes de realinhamento | 2-3h/semana |
| Product Ops | Roll-up manual de OKRs | 60-80h/mes (40% do time) |
| AI Architect | Investigacao de incidentes de contexto | 20-30% do time |

> **Padrao central:** Trabalho que um sistema bem feito faria em 5 minutos consome horas de pessoas qualificadas — desperdicio de talento, nao so de tempo.

---

## 2. Pull Forces (O Que Atrai Para APOS)

### 2.1 Automacao Task→OKR→Metrica

**Personas atraidas:** PM Leader, EM/Tech Lead, Product Ops, Early Adopter
**Nivel de atracao:** 9/10
**Mencionado espontaneamente:** Sim (por todas as 4)

| Persona | O Que Atrai | Por Que |
|---------|------------|---------|
| PM Leader | Dashboard visual Task→OKR | "Mudaria meu dia" |
| EM / Tech Lead | Alerta de "feature sem OKR" | Municao pra argumentar com PM |
| Product Ops | Rastreamento automatico | Elimina 80% do trabalho manual |
| Early Adopter | Resumo semanal automatico | Setup em 5 min, valor imediato |

> **Diferencial APOS:** Nao e so "dashboard bonito" — e deteccao proativa de desalinhamento + acao viavel ("quer vincular ou despriorizar?").

### 2.2 Trust Score / Confianca no Contexto

**Personas atraidas:** AI Architect, Product Ops
**Nivel de atracao:** 9/10 (AI), 6/10 (Ops)

| Persona | O Que Atrai | Por Que |
|---------|------------|---------|
| AI Architect | Trust score 0.0-1.0 | "Muda radicalmente como operamos" |
| Product Ops | Confianca nos dados | "Preciso responder 'sim, 100%' pro VP" |

> **Diferencial APOS:** Unico no mercado com pontuacao de confianca semantica. Para AI Architects, e o recurso mais valioso. Para Product Ops, e uma camada de credibilidade.

### 2.3 Rastreabilidade de Decisao

**Personas atraidas:** PM Leader, EM/Tech Lead
**Nivel de atracao:** 7/10

| Persona | O Que Atrai | Por Que |
|---------|------------|---------|
| PM Leader | Historico de "por que priorizamos X" | Onboarding + mudancas de prioridade |
| EM / Tech Lead | ADR + Jira + Notion conectados | "Horas de reuniao economizadas" |

> **Diferencial APOS:** Nao e so archive — e rastreabilidade viva, atualizada automaticamente.

---

## 3. Habit Forces (O Que Mantem no Status Quo)

### 3.1 Jira lock-in (ecossistema)

**Personas afetadas:** Todas (5/5)
**Severidade:** 8/10

| Persona | Manifestacao | Switching Cost |
|---------|-------------|----------------|
| PM Leader | 7 PMs + 20 engenheiros usam Jira | Treinar 27 pessoas |
| EM / Tech Lead | GitHub + Jira + Slack = fluxo | Muscle memory do time |
| AI Architect | Pipelines de embedding + vector store | Investimento ja feito |
| Product Ops | Sheets + Jira integrados | Reports quebram |
| Early Adopter | Toda empresa usa Jira | Nao da pra trocar |

> **Conclusao:** APOS nao compete com Jira — APOS **complementa** Jira. Plugin, nao substituicao.

### 3.2 Ceticismo pos-falha

**Personas afetadas:** EM/Tech Lead, Early Adopter
**Severidade:** 7/10

| Persona | Trauma | Impacto |
|---------|--------|---------|
| EM / Tech Lead | "Dashboards bonitos que ninguem usa" | So acredita vendo POC real |
| Early Adopter | 3 ferramentas de OKR que prometeram e falharam | "Risco politico > risco de nao fazer nada" |

> **Conclusao:** So POC com dados reais + casos de sucesso de empresas similares vencem o ceticismo.

### 3.3 Sheets como ferramenta final

**Personas afetadas:** Product Ops
**Severidade:** 6/10

| Persona | Manifestacao | Por Que |
|---------|-------------|---------|
| Product Ops | Reports sao no Google Sheets | Flexibilidade > especializacao |

> **Conclusao:** Integracao bidirecional com Sheets e requisito pra Product Ops.

---

## 4. Anxiety Forces (O Que Gera Medo de Adotar)

### 4.1 Falso positivo / credibilidade

**Personas preocupadas:** PM Leader, EM/Tech Lead, Product Ops
**Severidade:** 8/10

| Persona | Medo | Consequencia |
|---------|------|-------------|
| PM Leader | "Gritar alerta toda hora" | Time ignora |
| EM / Tech Lead | "Flag tudo sem OKR" | Perde credibilidade |
| Product Ops | "Dado errado apresentado ao CEO" | Dano irreparavel |

> **Mitigacao:** Nuance nos alertas — distinguir "feature sem OKR porque e divida tecnica" vs "feature sem OKR porque e feature aleatoria".

### 4.2 Interrupcao no fluxo de trabalho

**Personas preocupadas:** EM/Tech Lead, AI Architect
**Severidade:** 7/10

| Persona | Medo | Condicao |
|---------|------|----------|
| EM / Tech Lead | "Dev precisar preencher mais coisa" | Rejeicao na hora |
| AI Architect | "Latencia maior que 500ms" | Query ontologica lenta |

> **Mitigacao:** Plugin passivo — nao exige acao do usuario. Funciona em background.

### 4.3 Lock-in / dependencia de fornecedor

**Personas preocupadas:** AI Architect, Early Adopter
**Severidade:** 6/10

| Persona | Medo | Condicao |
|---------|------|----------|
| AI Architect | "Se amarrar em ontologia proprietaria" | Precisa de schema aberto |
| Early Adopter | "Se APOS fechar, meu contexto some" | Export garantido |

> **Mitigacao:** Schema de dados aberto (RDF/OWL-like), export via API, sem lock-in.

---

## 5. Grafico de Intensidade

```
Push (dor)          ██████████░░ 9/10  ← Maior consenso
Pull (atracao)      ████████░░░░ 8/10  ← Trust score e o pico
Habit (status quo)  ███████░░░░░ 7/10  ← Jira e maior barreira
Anxiety (medo)      ███████░░░░░ 7/10  ← Credibilidade e maior risco

Forcas a favor (Push + Pull):   17/20  ✅ FORTE
Forcas contra (Habit + Anxiety): 14/20  ⚠️ GERENCIAVEL
Diferencial liquido:            +3/20  ✅ FAVORAVEL
```

---

## 6. Recomendacoes de Produto

Baseado na analise de forcas:

### Prioridade Maxima (Remove Habit + Anxiety)

| Acao | Forca Enderecada | Impacto |
|------|------------------|---------|
| Plugin Jira (nao substituicao) | Habit #1: Jira lock-in | Remove barreira #1 |
| Alertas com nuance | Anxiety #1: falso positivo | Preserva credibilidade |
| Nao exigir preenchimento manual | Anxiety #2: interrupcao | Garante adocao |

### Diferencial Competitivo (Maximiza Pull)

| Acao | Forca Enderecada | Impacto |
|------|------------------|---------|
| Trust score 0.0-1.0 | Pull #2: confianca no contexto | Unico no mercado |
| Dashboard Task→OKR ao vivo | Pull #1: automacao | Visibilidade imediata |
| Schema de dados aberto | Anxiety #3: lock-in | Adocao por AI Architects |

### Roadmap Sugerido

```
MVP (R1):
  Plugin Jira + Deteccao de orfas + Resumo semanal
  ├─ Elimina 80% do roll-up manual (Ops)
  ├─ Reduz reexplicacao em 50% (PM)
  └─ Setup < 30 min (Early Adopter)

R1.1:
  Trust Score + Dashboard ao vivo
  ├─ Diferencial real vs concorrentes
  └─ Atraca AI Architects + PM Leaders

R1.2:
  API REST + Schema aberto
  ├─ Integracao com ferramentas existentes
  └─ Remove anxiety de lock-in
```

---

## 7. Risco de Nao Agir

Se APOS nao for construida:

| Consequencia | Personas Afetadas | Probabilidade |
|-------------|-------------------|---------------|
| Continuidade do desperdicio de 2-3h/semana por PM | PM Leader | 100% |
| 30-40% retrabalho continua sendo aceito como "normal" | EM / Tech Lead | 100% |
| 15-20% alucinacao de agentes persiste sem remedio | AI Architect | 100% |
| 60-80h/mes de roll-up manual continuam | Product Ops | 100% |
| 15-20% esforco desperdicado continua invisivel | Early Adopter | 100% |

**Custo acumulado anual (estimado):**
- PM Leader: ~R$ 14.400/ano (2-3h/semana a R$ 100/h)
- EM/Tech Lead: ~R$ 38.400/ano (30-40% retrabalho)
- AI Architect: ~R$ 57.600/ano (20-30% do time em incidentes)
- Product Ops: ~R$ 38.400/ano (40% do time em roll-up)
- Early Adopter: ~R$ 28.800/ano (15-20% esforco desperdicado)

**Custo total estimado por empresa:** ~R$ 177.600/ano — so com retrabalho de contexto.

---

**Analise consolidada por:** Hermes Agent (simulacao JTBD)
**Framework:** Jobs to Be Done — Forcas de Progresso
**Data:** 2026-07-20
