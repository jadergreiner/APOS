# Sprint 0.2: Plano de Entrevistas de Validação

**Sprint:** 0.2 - JTBD Deep Dive
**Objetivo:** Validar que APOS resolve jobs reais através de 5+ entrevistas JTBD
**Data de Execução:** 2026-07-22 até 2026-07-26

---

## Contexto

Sprint 0.1 entregou artefatos estratégicos (VALUE_PROPOSITION.md, OKR.md, ROADMAP_R1_R4.md). Sprint 0.2 valida que esses artefatos refletem necessidades reais de mercado através de JTBD (Jobs to Be Done) Discovery.

### Jobs Framework

Cada entrevista explora **Forças de Progresso** que movem adotantes em direção a APOS:

- **Push Forces** — O que empurra personas para encontrar solução (frustração com alternativas atuais)
- **Pull Forces** — O que puxa personas para APOS (recursos únicos, proposição de valor)
- **Habit Forces** — O que mantém personas presas ao status quo (switching costs, familiaridade)
- **Anxiety Forces** — O que retém personas de adotar (risco, complexidade, prova de conceito)

---

## Personas Alvo (5+ Entrevistas)

### 1. **Líder de PM** (Equipe de 4-12 pessoas)

**Perfil:**
- Responsável por roadmap de produto + priorização
- Usa Jira, Notion, Linear para rastrear trabalho
- Frustra-se com retrabalho de contexto estratégico

**Hipótese:**
- Push: -80% tempo re-explicando contexto de decisão
- Pull: Dashboard visual de Task→Feature→OKR→Métrica
- Habit: Jira está integrado em toda a equipe
- Anxiety: Curva de aprendizado, mudança de workflow

**Perguntas-chave:**
1. Como você hoje documenta contexto estratégico de uma tarefa/feature?
2. Quantas vezes por semana você re-explica por que X está priorizado?
3. Se pudesse visualizar Task→OKR→Métrica de impacto em 10 segundos, qual seria o impacto?
4. O que precisaria para trocar seu workflow atual?

**Tempo:** 45 min  
**Responsável:** Jader Greiner

---

### 2. **Gerente de Engenharia** (Tech Lead / EM)

**Perfil:**
- Responsável por capacidade de entrega + quality gates
- Preocupado com retrabalho, scope creep, débito técnico
- Trabalha com código, testes, CI/CD

**Hipótese:**
- Push: -25% retrabalho causado por scope creep / contexto incompleto
- Pull: Validação automática de alinhamento estratégico (features com OKRs fracossos)
- Habit: Workflow de code review já estabelecido
- Anxiety: Integração complexa com CI/CD, false positives em governança

**Perguntas-chave:**
1. De onde vem retrabalho em seus sprints?
2. Com que frequência você entrega features que depois foram de-priorizadas?
3. Como você hoje valida que uma feature mapeia para uma métrica real?
4. Qual seria o impacto de detectar "orphaned features" (sem OKR) automaticamente?

**Tempo:** 45 min  
**Responsável:** Jader Greiner

---

### 3. **Arquiteto de Agentes IA** (AI/ML Engineer)

**Perfil:**
- Trabalha com LLMs, prompting, RAG, context injection
- Busca contexto preciso para reduzir alucinação
- Familiares com grafos de conhecimento, embeddings

**Hipótese:**
- Push: -50% latência de contexto, -25% tokens gastos em re-fetching contexto
- Pull: Semântica formal com pontuação de confiança 0.0-1.0
- Habit: Já usa vectors/embeddings, confortável com ontologias
- Anxiety: Integração com framework LLM específico (LangChain, etc.)

**Perguntas-chave:**
1. Hoje, como você seleciona contexto para passar ao agente de IA?
2. Com que frequência o agente alucinaria porque contexto foi incompleto?
3. Se você pudesse ter "confiança semântica 0.8+" sobre contexto, qual seria impacto?
4. Seria útil ter ontologia formal vs. ad-hoc RAG retrieval?

**Tempo:** 45 min  
**Responsável:** Jader Greiner

---

### 4. **Líder de Operações de Produto** (Product Operations / Analytics)

**Perfil:**
- Responsável por métricas, dashboards, OKR tracking
- Interface entre estratégia e execução
- Trabalha com data warehouse, BI tools

**Hipótese:**
- Push: -80% trabalho manual de "roll-up" de dados para relatórios de OKR
- Pull: Query engine automática Task→Feature→Release→OKR→Métrica
- Habit: Snowflake/BigQuery + Tableau/Looker já estabelecido
- Anxiety: Data quality, integração com warehouse existente

**Perguntas-chave:**
1. Hoje, quanto trabalho você gasta em "roll-up" de tarefas para relatórios de OKR?
2. Com que frequência métricas de OKR estão desalinhadas com tarefas reais?
3. Se pudesse ter visibilidade automática Task→OKR em tempo real, qual seria impacto?
4. Qual seria o custo de integração com seu warehouse existente?

**Tempo:** 45 min  
**Responsável:** Jader Greiner

---

### 5. **Early Adopter / Cliente Potencial**

**Perfil:**
- PM de empresa que está crescendo (10-100 pessoas)
- Sofrendo com retrabalho de contexto / governança
- Aberto a ferramentas novas se resolverem pain real

**Hipótese:**
- Push: -50% retrabalho, -25% tempo em alinhamento estratégico
- Pull: Plataforma AI-first com contexto confiável
- Habit: Ferramentas consolidadas (Jira, Slack, Linear)
- Anxiety: Risk de adotar algo novo, complexidade de integração

**Perguntas-chave:**
1. Qual é seu maior pain com governança estratégica hoje?
2. Se pudesse ter Task→Feature→OKR→Métrica em um lugar, qual seria impacto?
3. Estaria disposto a pilotar APOS com sua equipe?
4. Qual seria o ROI mínimo para justificar switching?

**Tempo:** 60 min  
**Responsável:** Jader Greiner

---

## Script de Entrevista (45-60 min)

### Abertura (5 min)

> "Obrigado por participar! Estou pesquisando como equipes de PM hoje lidam com contexto estratégico e governança. Vou fazer perguntas abertas — não há respostas certas, quero ouvir sua experiência real. Ok?"

### Warm-up (5 min)

- Conte-me sobre sua função
- Qual é o tamanho da sua equipe?
- Quais ferramentas vocês usam para rastrear trabalho?

### Core Questions (30 min)

**Seção 1: Status Quo (10 min)**
- Como você documenta contexto estratégico de uma task/feature?
- Com que frequência você re-explica por que X está priorizado?
- Qual é seu maior pain com alinhamento estratégico?

**Seção 2: Needs Exploration (10 min)**
- Se pudesse resolver um pain em governança estratégica, qual seria?
- O que seria sucesso para você?
- Qual seria o impacto quantificável?

**Seção 3: Jobs Framework (10 min)**
- O que a empurraria a mudar sua ferramenta/workflow atual?
- O que a puxaria para uma solução como APOS?
- O que mantém você presa ao status quo?
- O que gera ansiedade em adotar algo novo?

### Close (5 min)

- Ficou algo em aberto?
- Posso enviar artefatos (VALUE_PROPOSITION.md, OKR.md) para feedback?
- Interessado em piloto / early adopter program?

---

## Cronograma de Entrevistas

| Data | Persona | Entrevistador | Duração | Status |
|------|---------|---------------|---------|--------|
| 22 jul | Líder de PM | Jader | 45 min | 📋 Agendar |
| 23 jul | Gerente de Engenharia | Jader | 45 min | 📋 Agendar |
| 23 jul | Arquiteto IA | Jader | 45 min | 📋 Agendar |
| 24 jul | Líder de Ops de Produto | Jader | 45 min | 📋 Agendar |
| 25 jul | Early Adopter | Jader | 60 min | 📋 Agendar |

**Total de Entrevistas:** 5  
**Tempo Total:** ~4.25 horas

---

## Saídas Esperadas

### T0.2.3: JTBD_INTERVIEWS.md
- Sumário de cada entrevista (persona, date, key findings)
- Análise qualitativa de padrões
- Direct quotes validando pain points + value proposition

### T0.2.4: FORCES_ANALYSIS.md
- Push/Pull/Habit/Anxiety analysis consolidada
- Matriz de força por persona
- Identificação de "minimum viable proposição" para adoção

### T0.2.6: JOB_STATEMENT.md
- Declaração formal do job: "Help {persona} to {job} so that {outcome}"
- Contexto de situação (circunstâncias triggering need)
- Critérios de sucesso (como personas medem sucesso)

---

## Critérios de Sucesso

✅ **Sprint 0.2 Completo Quando:**

1. **5+ entrevistas realizadas** (mínimo 3 personas diferentes)
2. **Padrões claros identificados** em Push/Pull/Habit/Anxiety
3. **Job Statement finalizado** — documentado em JOB_STATEMENT.md
4. **Validação de VALUE_PROPOSITION** — artefatos ressoa com 3+ personas
5. **Decision Point**: Prosseguir com Beta Prep (Sprint 0.3) ou iterar proposição?

---

**Próximo Sprint:** Sprint 0.3 - Beta Prep (recruiting, documentation, examples)
