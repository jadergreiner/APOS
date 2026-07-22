# 🎤 R1 Sprint 1 Stakeholder Interviews — Roadmap Completo

**Data:** 2026-07-21 (Dia 1 do Sprint)  
**Objetivo:** Validar 3 hipóteses críticas do sprint via entrevistas estruturadas com 3 stakeholders  
**Entregável:** Síntese de insights + decisões de design pra ProjectAdapter

---

## 📍 Por Que Entrevistas Agora?

**Sprint Goal:** Tornar APOS operacional no Meu PDI com:
- `agent_harness` + `capability_harness` ≥80% coverage
- `ProjectAdapter` protótipo funcional (≥80% descoberta automática)

**Hipóteses críticas a validar:**

1. **≥80% descoberta automática é suficiente?** (Feature completeness)
2. **Dupla via (Harness + ProjectAdapter paralelo) é viável?** (Execution model)
3. **Timeline 1-week é realista?** (Velocity + estimation)

**Por quê entrevistas:**
- Suposições em planning precisam de validação real
- Insights de stakeholders (CEO, SME, SM) fundamentam design decisions
- Dia 2 milestone decision (continua dupla via? Serial?) depende desse input

---

## 📚 Documentos (Leia Nesta Ordem)

### 1️⃣ **INTERVIEW_EXECUTION_CHECKLIST.md** (5 min — COMECE AQUI)

**Para:** Entrevistador (provavelmente Jader)

**Conteúdo:**
- Timeline de 14:00-16:00 (3 entrevistas + síntese)
- Questões quick-reference (copie/cole)
- Red flags (sinais de alerta)
- Pós-entrevista checklist
- TL;DR (pra quando tá corrido)

**Quando usar:** Abra em split-screen ao lado de cada entrevista. Use como "cheat sheet".

**Tempo de leitura:** 5 min (é pragmático, não teórico)

---

### 2️⃣ **STAKEHOLDER_INTERVIEWS.md** (30 min — LEIA ANTES DAS ENTREVISTAS)

**Para:** Entrevistador (preparo antes 14:00) + team (contexto geral)

**Conteúdo:**
- Contexto completo (por que fazemos, como funciona)
- Princípios de entrevista (✅ e ❌)
- 3 seções de entrevista (uma por stakeholder):
  - Perfil/papel
  - 7 questões estruturadas (abertas → técnicas → validação)
  - Tempo estimado
  - Notas de preparação (contexto enviar 24h antes)
  - Template de captura
- Exemplos de bom/ruim
- Referências

**Quando usar:** 
- Entrevistador lê ANTES de cada entrevista (10 min por stakeholder = 30 min total)
- Team lê pra entender metodologia
- Se entrevista fica vaga, volta aqui pra explorar mais

**Tempo de leitura:** 30 min (é comprehensive)

---

### 3️⃣ **SYNTHESIS.md** (Preencher Depois das Entrevistas)

**Para:** Entrevistador + team

**Conteúdo:**
- Template pré-estruturado pra consolidar insights
- Validação de 3 hipóteses (tabelas SIM/NÃO/DEPENDE)
- Insights por dimensão (4 dimensões)
- Riscos identificados (mapa de riscos)
- 4 decisões resultantes (com ações)
- Próximos passos

**Quando usar:**
- Preencher imediatamente após entrevistas (15:00-15:30)
- Referência durante síntese (não deixa você esquecer nada)
- Compartilha com team depois (Slack + standup)

**Tempo de preenchimento:** 30 min (template já está 80% estruturado)

---

## 🎯 Fluxo Completo (Dia 1)

```
PRÉ-ENTREVISTAS (Antes 14:00)
├─ [ ] Leia INTERVIEW_EXECUTION_CHECKLIST.md (5 min)
├─ [ ] Leia STAKEHOLDER_INTERVIEWS.md (30 min)
├─ [ ] Leia R1_PLANNING_GUIDE.md + SPRINT_PLANNING.md pra contexto (20 min)
├─ [ ] Abra SYNTHESIS.md em editor (pra preencher depois)
└─ [ ] Confirme com stakeholders + prepara setup (timers, etc)

ENTREVISTAS (14:00-15:00)
├─ 14:00-14:20: Entrevista 1 (CEO/Product) — usa INTERVIEW_EXECUTION_CHECKLIST
├─ 14:20-14:40: Entrevista 2 (SME Técnico) — usa INTERVIEW_EXECUTION_CHECKLIST
├─ 14:40-15:00: Entrevista 3 (SM/Tech Lead) — usa INTERVIEW_EXECUTION_CHECKLIST
└─ [Capture respostas em templates]

SÍNTESE (15:00-15:30)
├─ Transfira notas de captura pra SYNTHESIS.md
├─ Consolide hipóteses (tabelas SIM/NÃO/DEPENDE)
├─ Documente riscos (≥3)
├─ Escreva 4 decisões resultantes
└─ Revise pra claridade (team consegue ler em 10 min?)

COMUNICAÇÃO (15:30-16:00)
├─ Compartilhe SYNTHESIS.md com team (Slack link)
├─ Explique decisões em 5 min (resumo executivo)
├─ Se mudanças grandes, atualiza SPRINT_PLANNING.md + BOARD.md
└─ Agenda standup Dia 2 16:00 (milestone decision)
```

---

## 👥 3 Stakeholders & Suas Roles

### Entrevista 1: CEO/Product (Jader Greiner)

**Papel:** Define estratégia, trade-offs, requisitos de negócio

**Perguntas:**
1. Experiência atual com adaptadores
2. Validação: ≥80% é suficiente?
3. Dores atuais (pain points)
4. Expectativa ProjectAdapter
5. Validação: suficiência de automação
6. **Tradeoff crítico:** Harness vs ProjectAdapter (qual priorizar no Dia 2?)
7. Timeline: realista?

**Output crítico:** Escopo + criticidade + trade-offs

**Tempo:** 20 min

---

### Entrevista 2: SME Técnico

**Papel:** Valida viabilidade técnica, surface edge cases, arquitetura

**Perguntas:**
1. Viabilidade técnica ≥80%?
2. Estratégia de descoberta (como faria?)
3. Dores técnicas (onde quebra?)
4. Validação: ≥80% é viável?
5. Integração ProjectAdapter ↔ BootstrapGate ↔ ContextEngine ↔ KnowledgeGraph
6. Validação: suficiência arquitetural?
7. Timeline: realista? Qual % é mais realista?

**Output crítico:** Viabilidade técnica + constraints arquiteturais + edge cases

**Tempo:** 20 min

---

### Entrevista 3: Scrum Master / Tech Lead

**Papel:** Valida execução, mapeia dependências, gerencia velocity

**Perguntas:**
1. Dupla via é factível? Ou serial?
2. Pacing Dia 1-2 (como estruturar pra milestone decision?)
3. Dores de dupla via paralela
4. Validação: 2 SP por track é realista?
5. Convergência Dia 2 (plano A/B/C)
6. Riscos arquiteturais que precisam mitigação Dia 1?
7. Velocity validação (4 SP + buffer é realista? vs R0 baseline 7 SP/week)

**Output crítico:** Plano de execução + dependências + velocity realista

**Tempo:** 20 min

---

## 🎯 3 Hipóteses Críticas

### Hipótese 1: ≥80% Descoberta Automática é Suficiente?

**Por quê:** ProjectAdapter design depende disso. Se precisa 95%, estratégia é diferente.

**Validação:** Pergunte a CEO ("é suficiente pra você?") + SME ("é viável em 1 week?")

**Métrica:** Sim/Não/Depende + justificativa

**Impacto:** Se não → redefine escopo / timeline / prioridade

---

### Hipótese 2: Dupla Via (Harness + ProjectAdapter) é Viável?

**Por quê:** Sprint planning assume paralelo. Se não viável, pivota pra serial.

**Validação:** Pergunte a SME (acoplamento?) + SM (execução?)

**Métrica:** Sim/Não/Com Risco + justificativa

**Impacto:** Se não → SPRINT_PLANNING.md ajusta pra serial; timeline muda

---

### Hipótese 3: Timeline 1-Week é Realista?

**Por quê:** Se otimista, milestone Dia 2 não vai validar nada (progress será muito baixo).

**Validação:** Pergunte a CEO + SME + SM ("você acha realista?")

**Métrica:** Realista/Otimista/Pessimista + estimativa revisada

**Impacto:** Se pessimista → extend pra 1.5 weeks / redefine scope

---

## 🚨 Dia 2 Milestone Decision (O Por Que Disso Tudo)

**No Dia 2 16:00, você precisa decidir:**

> "Continuamos dupla via (Harness + ProjectAdapter paralelo) ou pivotamos pra serial?"

**Critério de decisão** (definido em entrevistas):

| Cenário | Ação |
|---------|------|
| Ambos ≥70% | Continua dupla via; converge em integração |
| ProjectAdapter <50% | Pausa ProjectAdapter; 100% Harness |
| Harness <60% | Pausa outros; debugar Harness |
| Ambos falham | Dia 3 replaning; estende timeline |

**Por que entrevistas agora:** Você SABE critério de sucesso antes de Dia 1; não tá fazendo isso on-the-fly.

---

## 📝 Estrutura de Cada Entrevista

### Setup

```
Antes: Envie contexto ao stakeholder 24h antes
Durante: Abra timer, 20 min exato
Depois: Capture notas imediatamente
```

### Fluxo de Questões

```
Q1-Q3: Abertas (Entender experiência atual + dores)
Q4:    Abertas (Expectativa/vision)
Q5-Q6: Validação (Confirmar hipóteses)
Q7:    Realistic? (Sanity check)
```

### Captura

```
Durante: Verbatim quotes (pelo menos 2-3 por questão)
Depois:  Síntese 1-linha (pra consolidação)
         Decisão SIM/NÃO/DEPENDE (pra cada hipótese)
         Confiança Alta/Média/Baixa
```

---

## 🎓 Princípios Chave

### ✅ Faça Isso

- **Comece aberto:** "Fale-me sobre sua experiência..."
- **Escute 30s:** Deixa pessoa responder completamente
- **Explore "Por quê?":** Não aceite resposta superficial
- **Valide entendimento:** "Deixa eu validar que entendi..."
- **Tome notas:** Quotes reais > interpretação sua
- **Respeite tempo:** 20 min é apertado; redirecione suave

### ❌ Evite Isso

- Sugerir respostas ("você acha que...?")
- Debater durante entrevista
- Pular pergunta se resposta incompleta
- Deixar silêncios > 30s (pessoa fica confortável demais)
- Tomar notas interpretadas (verbatim é ouro)

---

## 📊 Resultado Esperado

### Imediatamente Após Entrevistas

**SYNTHESIS.md preenchido com:**

- [ ] Hipóteses 1-3 validadas (SIM/NÃO/DEPENDE)
- [ ] Risco ≥3 identificados + mitigação
- [ ] 4 decisões principais documentadas
- [ ] Próximos passos claros (ações pra Dia 2)

### Comunicação ao Team (15:30-16:00)

**Email/Slack:**

```
"Rodamos as 3 entrevistas. Aqui estão os insights:

✅ HIPÓTESE 1 (≥80% suficiente): [SIM/NÃO/DEPENDE]
✅ HIPÓTESE 2 (Dupla via viável): [SIM/NÃO/COM RISCO]
✅ HIPÓTESE 3 (Timeline realista): [SIM/NÃO/AJUSTE]

DECISÃO RESULTANTE:
→ Mantém dupla via / Pivota pra serial / Outro

Síntese completa: [link SYNTHESIS.md]
Próximo: Standup Dia 2 16:00 (milestone decision)
"
```

### SPRINT_PLANNING.md Atualizado (Se Decisões Mudaram)

Se entrevistas revelarem que timeline/escopo precisa ajuste:
- [ ] Trilhas A/B ajustadas (se decisão de dupla via mudou)
- [ ] Sprint milestones ajustados
- [ ] Buffer redefinido (se velocity ajustou)

---

## 🎓 Recursos por Papel

### Se Você é o Entrevistador (Jader)

**Passo 1:** Abra INTERVIEW_EXECUTION_CHECKLIST.md (pra fazer)

**Passo 2:** Leia STAKEHOLDER_INTERVIEWS.md seção inteira (pra preparar)

**Passo 3:** Durante entrevista, usa INTERVIEW_EXECUTION_CHECKLIST como "cheat sheet"

**Passo 4:** Depois, preenche SYNTHESIS.md (consolidação)

**Passo 5:** Compartilha resultado com team

---

### Se Você é Stakeholder (CEO/SME/SM)

**Você vai receber:** Email 24h antes com contexto (enviado via STAKEHOLDER_INTERVIEWS.md seção de preparação)

**Você faz:** Responde 7 questões (20 min)

**Você vê depois:** SYNTHESIS.md consolidado (insights seus + outros stakeholders) + decisões resultantes

---

### Se Você é Team Member (Engineers, etc)

**Você pode:** Ler STAKEHOLDER_INTERVIEWS.md pra entender metodologia

**Você receberá:** SYNTHESIS.md consolidado (Slack link, Dia 1 15:45)

**Você usa:** Pra entender decisões de design + milestone criteria

---

## 🚀 Próximos Passos Após Síntese

**Dia 1 (depois síntese):**
- [ ] SYNTHESIS.md compartilhado com team
- [ ] SPRINT_PLANNING.md atualizado (se mudanças)
- [ ] Standup Dia 2 agendado (16:00)

**Dia 2 (milestone decision):**
- [ ] Valida progress vs criteria (definido em entrevistas)
- [ ] Decide: continua dupla via? Pivota?
- [ ] Documenta decisão em DAILY_STANDUP.md

**Dia 3+:**
- [ ] Executa convergência plan (definido em entrevistas)
- [ ] Integração ProjectAdapter + Harness

---

## 📞 Troubleshooting

| Problema | Solução |
|----------|---------|
| "Entrevistador não tem 1h?" | Delega pra SM ou Tech Lead; fornece roteiro |
| "Stakeholder não consegue 20 min?" | 15 min minimal; prioriza Q1/Q2/Q6/Q7 (key 4) |
| "Síntese tá vaga?" | Volta pra notas; adiciona verbatim quotes; pede clarificação |
| "Decisão não ficou clara?" | 15 min follow-up com stakeholders; resolve ambiguidade |
| "SYNTHESIS.md tá bom mas time não entende?" | Resume em 5 min no standup; deixa documento pra referência |

---

## 📚 Arquivos Relacionados

**Nesta pasta:**
- [INTERVIEW_EXECUTION_CHECKLIST.md](INTERVIEW_EXECUTION_CHECKLIST.md) — Cheat sheet pra executar
- [STAKEHOLDER_INTERVIEWS.md](STAKEHOLDER_INTERVIEWS.md) — Roteiro completo
- [SYNTHESIS.md](SYNTHESIS.md) — Template de consolidação
- [SPRINT_PLANNING.md](SPRINT_PLANNING.md) — Sprint plan (atualiza se decisões mudam)
- [BOARD.md](BOARD.md) — Kanban board

**Fora desta pasta:**
- [R1_PLANNING_GUIDE.md](../R1_PLANNING_GUIDE.md) — Context de R1
- [R1/README.md](../README.md) — Overview de R1

---

## ⚡ TL;DR (Pra Quando Tá Corrido)

1. **Leia INTERVIEW_EXECUTION_CHECKLIST.md** (5 min cheat sheet)
2. **Rode 3 entrevistas 20 min cada** (14:00-15:00)
3. **Preenche SYNTHESIS.md** (15:00-15:30)
4. **Comunica ao team** (15:30-16:00)
5. **Atualiza SPRINT_PLANNING.md se decisões mudaram**
6. **Próximo: Milestone Dia 2 decision**

---

**Criado:** 2026-07-21  
**Tipo:** Research Protocol  
**Timing:** Dia 1 Sprint 1 (14:00-16:00)  
**Output:** SYNTHESIS.md + decisões claras pra Dia 2  
**Público:** Team APOS + Jader

