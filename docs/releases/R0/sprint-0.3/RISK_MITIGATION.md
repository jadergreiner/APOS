# Sprint 0.3 - Risk Mitigation

**Sprint:** 0.3 - Beta Prep (MVP Implementation)  
**Data:** 2026-07-20 (Pre-sprint planning)  
**Source:** Sprint 0.2 Forças Analysis (Push/Pull/Habit/Anxiety)  
**Status:** 📋 Riscos mapeados, mitigacoes definidas

---

## Riscos Identificados (Sprint 0.2)

Baseado em Forças Analysis (entrevistas com 5 personas), 4 principais riscos de adocao foram identificados.

---

## 1. Jira Lock-In (Habit Force)

### Risco

**Severidade:** 🔴 Alta (8/10)  
**Persona:** Todas 5 (100%)  

"Jira ja e o ecossistema. Por que adicionar outra ferramenta?"

**Manifestacao:**
- 7 PMs + 20 engineers ja usam Jira
- GitHub + Jira + Slack = fluxo estabelecido
- Custo de switching ("treinar 27 pessoas") e alto

### Mitigacao Implementada

✅ **Plugin, nao substituicao**
- APOS Plugin Jira = adiciona UI dentro de Jira
- Users nao mudam workflow
- Sem "saia do Jira, use APOS"

✅ **Escopo Sprint 0.3:** T0.3.3 = implementa Plugin Jira (nao API standalone)

✅ **Piloto:** 3 personas testam plugin IN Jira (nao migram)

**Resultado Esperado:** Se Jira lock-in 8/10 antes, cai para 2/10 com plugin (familiar interface)

---

## 2. Falso Positivo / Credibilidade (Anxiety Force)

### Risco

**Severidade:** 🔴 Alta (8/10)  
**Persona:** PM, EM, Ops (3/5)  

"Se APOS gritar alerta toda hora, ninguem acredita."

**Manifestacao:**
- "Alertas que ninguém lê = credibilidade perdida"
- Ops perde confianca em dados (VP/C-level questiona tudo)
- Devs ignoram notificacoes (alert fatigue)

### Mitigacao Implementada

✅ **Nuance nos alertas**
- "Feature sem OKR porque e divida tecnica" ≠ "feature aleatoria sem justificativa"
- Trust Score diferencia:
  - High risk: task entregue, ninguem sabe por que (prioridade maxima)
  - Medium risk: task em progresso sem contexto (acao sugerida)
  - Low risk: task em backlog ainda sem OKR (nao pressa)

✅ **Escopo Sprint 0.3:** 
- T0.3.1 (SPEC.md) = define risk levels explicitamente
- T0.3.4 (Trust Score) = calcula scores com nuance (nao binario pass/fail)

✅ **Piloto:** Persona Ops vai validar "alertas sao credibles" (nao criados automaticamente todos)

**Resultado Esperado:** Se falso positivo severity 8/10 antes, cai para 2/10 com nuance (aleratas relevantes)

---

## 3. Interrupcao no Fluxo de Trabalho (Anxiety Force)

### Risco

**Severidade:** 🟡 Media (7/10)  
**Persona:** EM/Tech Lead, AI Architect (2/5)  

"Se devs precisam preencher mais campos, nao vao usar."

**Manifestacao:**
- Plugin que pede mais informacoes = friction
- "Dev ja ta ocupado, nao quer overhead"
- Latencia >500ms = interrupção (AI Architect)

### Mitigacao Implementada

✅ **Plugin passivo (zero overhead)**
- Nao exige acao do usuario
- Auto-detecta orfas sem intervencao
- Sync com Jira em background (nao sincronamente)

✅ **Performance (Latencia <500ms)**
- Escopo Sprint 0.3: T0.3.4 (API design) = otimizar queries
- Metricas (METRICS_BASELINE.md) = monitorar P95 latencia

✅ **Piloto:** Persona EM vai validar "nenhuma interrupcao, funciona em background"

**Resultado Esperado:** Se interrupcao risk 7/10 antes, cai para 1/10 com plugin passivo

---

## 4. Lock-In / Dependencia de Fornecedor (Anxiety Force)

### Risco

**Severidade:** 🟡 Media (6/10)  
**Persona:** AI Architect, Early Adopter (2/5)  

"Se amarrar em ontologia proprietaria, meu contexto some se APOS fecha."

**Manifestacao:**
- Vendor lock-in (dados presos em APOS)
- Sem portabilidade para outras tools
- Risk: "apos fechar, meu contexto some"

### Mitigacao Implementada

✅ **Schema de dados aberto**
- Data model = RDF/OWL-like (nao binario APOS)
- Tasks, OKRs, Relationships = estrutura padrão
- Pode ser migrada para outro tool se necessário

✅ **Export garantido**
- API /export endpoint (Sprint 0.3+)
- Dados em JSON (nao banco de dados proprietario)
- Sem penalty para migrar

✅ **Escopo Sprint 0.3:** 
- T0.3.2 (API_DESIGN.md) = define schema aberto
- Documentado = no lock-in by design

✅ **Piloto:** Persona AI vai validar "schema nao e proprietario"

**Resultado Esperado:** Se lock-in risk 6/10 antes, cai para 1/10 com schema aberto

---

## Risk Dashboard (Pre-Sprint)

| Risk | Severity | Mitigacao | Sprint 0.3 Validacao | Go/No-Go |
|------|----------|-----------|---------------------|----------|
| Jira lock-in | 8/10 | Plugin Jira | T0.3.3 testa plugin | ✅ |
| Falso positivo | 8/10 | Nuance alerts | T0.3.4 Trust Score | ✅ |
| Interrupcao fluxo | 7/10 | Plugin passivo | Piloto (EM feedback) | ✅ |
| Vendor lock-in | 6/10 | Schema aberto | T0.3.2 API design | ✅ |

**Risco Critico Identificado:** Nenhum (todos 4 tem mitigacoes claras)

**Status de Risco Pre-Sprint:** 🟢 **VERDE** — riscos mapeados, mitigacoes implementadas

---

## Contingency Plans (If Needed)

### Se plugin Jira nao funcionar com Jira API (T0.3.3)

**Plano B:** Usar Jira webhook + polling em vez de live API calls

**Delay:** +1d estimado

### Se Trust Score calculo muito complexo (T0.3.4)

**Plano B:** MVP com versao simples (coverage + manual mappings, sem consistency check)

**Delay:** None (versao simpler ainda valida)

### Se personas nao disponivel para piloto (T0.3.5)

**Plano B:** Usar dados simulados (como Sprint 0.2), mas com AI Architect feedback priorizado

**Delay:** None (simulated vs real data, metodologia igual)

### Se latencia >500ms nao conseguimos (T0.3.4)

**Plano B:** Aceitavel ate 750ms (AI Architect pode tolerar com caveats)

**Decision:** Conditional GREEN (EM valida "aceitavel?")

---

## Go/No-Go Decision Trigger

**Se qualquer mitigacao NAO funciona em Sprint 0.3:**

- T0.3.3 falha (plugin Jira) → Risk 8/10 volta → Conditional VERDE
- T0.3.4 falha (Trust Score) → Risk 8/10 volta → Conditional VERDE
- Piloto persona EM diz "interrupcao" → Risk 7/10 volta → Conditional YELLOW
- Schema nao e aberto → Risk 6/10 volta → Conditional YELLOW

**Acao:** Se qualquer acima, discuss com personas antes de Ship R1

---

**Status:** 📋 Mitigacoes definidas  
**Review:** Dia 6 (29 julho), decisao final pós-piloto  
**Owner:** Jader (monitoring), Piloto personas (validacao)
