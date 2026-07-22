# Roteiro de Entrevistas com Stakeholders — R1 Sprint 1

**Data:** 2026-07-21 (Dia 1 do Sprint)  
**Formato:** 3 entrevistas paralelas, 20 min cada  
**Objetivo:** Fundamentar design do ProjectAdapter com insights de UX/experiência real  
**Entrevistador:** Jader Greiner (ou delegado)  
**Output esperado:** Template de captura preenchido + síntese em `SYNTHESIS.md`

---

## 📍 Contexto da Entrevista

### Por quê estamos fazendo entrevistas agora?

**Sprint Goal:** Tornar APOS operacional no Meu PDI com:
- `agent_harness` + `capability_harness` ≥80% coverage
- `ProjectAdapter` protótipo funcional (≥80% descoberta de estrutura Meu PDI)

**Hipótese crítica:** ProjectAdapter funciona se entendermos:
1. **Como** adaptadores são usados hoje (experiência atual)
2. **Onde** doem (pain points reais)
3. **O que** esperam do ProjectAdapter (expectativas)
4. **Se** descoberta automática ≥80% é suficiente

### Por quê 3 entrevistas paralelas?

- **CEO/Product (Jader):** Estratégia, requisitos de negócio, trade-offs
- **SME Técnico:** Viabilidade, restrições técnicas, edge cases
- **Scrum Master/Tech Lead:** Execução, dependências, velocity impact

Parallelizar = insights em 1 hora, não 3 horas sequenciais.

---

## 🎯 Princípios de Entrevista

### ✅ O que fazer:

- **Comece aberto:** "Fale-me sobre sua experiência com adaptadores..."
- **Escute sem interromper** — deixe pessoa falar 30s mínimo
- **Valide hipóteses:** "Você concorda que descoberta automática ≥80% seria suficiente?"
- **Pergunte "por quê"** — não aceite resposta superficial
- **Tome notas** — verbatim quotes são ouro

### ❌ O que evitar:

- Não sugira respostas ("você acha que...?")
- Não debate durante entrevista (reserve pra síntese)
- Não pule para próxima pergunta se resposta incompleta
- Não deixe silêncios — use "hm, entendi. Me fale mais..."

---

## 👤 Entrevista 1: CEO/Product (Jader Greiner)

**Tempo:** 20 min  
**Papel:** Define estratégia, trade-offs, requisitos de negócio  
**Output crítico:** Escopo + constraints de ProjectAdapter  

### Preparação Prévia (enviar 24h antes)

```markdown
## Contexto pra Jader

**Pergunta chave:** O que ProjectAdapter precisa fazer pra ser útil em Meu PDI?

**Contexto:**
- R0 entregou Core + Bootstrap Gate + Release Management
- R1 precisa implementar ProjectAdapter (descoberta automatizada de estrutura)
- Queremos validar se ≥80% descoberta é suficiente

**Você vai responder:**
- Sua experiência com adaptadores
- Dores atuais
- Expectativas pro ProjectAdapter
- Criticidade pra Meu PDI
```

### Questões (Abertas → Validação)

#### Q1: Experiência Atual com Adaptadores (Abertas)

**[Abertura — sem sugestão]**
"Fale-me sobre sua experiência atual com adaptadores em Meu PDI. O que você faz hoje pra conectar diferentes ferramentas/contextos?"

**Variação se resposta curta:**
"Você usa algum adapter no seu workflow? Como você descobre a estrutura de um novo projeto?"

**Procure:**
- Processo atual (manual? semi-automatizado?)
- Ferramentas usadas (Jira? DevOps? Config files?)
- Frequência (diário? semanal?)
- Quem faz isso (você? time? bot?)

---

#### Q2: Validação - Criticidade

**[Validação com hipótese]**
"Você concorda que **descoberta automática ≥80% da estrutura** seria suficiente pra Meu PDI começar?"

**Se "sim":** "O que falta nos 20% restantes?"  
**Se "não":** "O que precisa ser 90%+? Por quê?"  
**Se "depende":** "De quê? Qual é o critério pra suficiência?"

**Procure:**
- Qual cobertura é "bom o bastante"
- Trade-offs aceitáveis (automático vs manual)
- Casos especiais que precisam 100%

---

#### Q3: Dores Atuais (Abertas)

**[Foco em pain points reais]**
"Qual é a maior dor que você sente hoje com descoberta de estrutura de projeto?"

**Variações se precisa de contexto:**
- "O que te faz perder tempo?"
- "Qual é a coisa mais repetitiva/chata que você faz?"
- "Se você pudesse automatizar UMA coisa, qual seria?"

**Procure:**
- Retrabalho (quantas vezes descobre mesma coisa?)
- Erros (o quê erra? Com que frequência?)
- Tempo (quanto tempo gasta? Pra quem?)
- Confiança (você confia no resultado?)

---

#### Q4: Expectativa de ProjectAdapter (Abertas)

**[O que espera, sem sugestão]**
"Se ProjectAdapter existisse amanhã, como você usaria? What would success look like?"

**Se vago:** "Me dê um exemplo específico de algo que ProjectAdapter precisaria fazer pra você usar."

**Procure:**
- Workflow esperado (como acionaria?)
- Integração (onde encaixa em seu processo?)
- Frequência de uso
- Critério de sucesso dele

---

#### Q5: Validação - Suficiência de Automação

**[Testar hipótese de Dia 1]**
"Vamos validar rapidinho: se ProjectAdapter descobrir ≥80% da estrutura Meu PDI no **Dia 2** (milestone), é o bastante pra você desbloquear seu trabalho?"

**Se "sim":** "Ótimo. Se descobre 50%, você consegue ligar manualmente no Dia 2?"  
**Se "não":** "O que você precisa? 85%? 95%? Tipo específico de descoberta?"

**Procure:**
- Blocker real vs nice-to-have
- Fallback aceitável (manual discovery)
- Timeline criticidade

---

#### Q6: Prioridade vs Harness (Tradeoff)

**[Decisão do Dia 2]**
"No Dia 2 da sprint, a gente precisa decidir: **continua trabalhando em ProjectAdapter** ou **foca 100% em Harness coverage** (≥80% tests)? Qual é mais crítico pra você?"

**Se "ambos":** "Se você pudesse escolher UM, qual?"  
**Se hesita:** "Qual deixa Meu PDI mais operacional?"

**Procure:**
- Dependência real (qual desbloqueia mais?)
- Risk tolerance (qual falha ≥80% coverage breaks?)

---

#### Q7: Validação Final - Realistic?

**[Sanity check pra execução]**
"Você acha que ≥80% descoberta automática é realista em 1 week pra ProjectAdapter core? Ou é otimista?"

**Se "realista":** "O que ajudaria a manter no prazo?"  
**Se "otimista":** "O que é mais realista? 60%? 70%?"

**Procure:**
- Feedback sobre estimativa
- Riscos arquiteturais ele vê
- Recursos/bloqueadores que faltam

---

### Template de Captura (Preenchido Entrevistador)

```markdown
## ENTREVISTA 1: CEO/Product (Jader Greiner)

**Data:** 2026-07-21  
**Duração:** XX min  
**Notas completas:**

### Q1: Experiência Atual
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q2: Criticidade
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q3: Dores Atuais
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q4: Expectativa ProjectAdapter
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q5: Suficiência de Automação
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q6: Prioridade Tradeoff (ProjectAdapter vs Harness)
[Resposta verbatim]

**Síntese:** Recomendação: [ProjectAdapter / Harness / Ambos paralelo]

---

### Q7: Realistic?
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Insights-Chave
- [ ] Descoberta ≥80% é suficiente? SIM / NÃO / DEPENDE
- [ ] Prioridade: ProjectAdapter / Harness / Ambos
- [ ] Timeline: Realista / Otimista / Pessimista
- [ ] Bloqueador principal: [_______________]
```

---

## 👨‍💻 Entrevista 2: SME Técnico

**Tempo:** 20 min  
**Papel:** Validar viabilidade técnica, surface edge cases  
**Output crítico:** Constraints arquiteturais + plano técnico

### Preparação Prévia (enviar 24h antes)

```markdown
## Contexto pra SME

**Pergunta chave:** Quais são os constraints técnicos do ProjectAdapter?

**Contexto:**
- Meu PDI é monorepo Django complex com múltiplos adaptadores
- ProjectAdapter precisa descobrir: stack, modules, relationships, domain
- Precisa fazer isso em ≥80% cobertura

**Você vai responder:**
- Viabilidade técnica
- Edge cases que quebram
- Arquitetura recomendada
- Riscos técnicos
```

### Questões (Abertas → Técnicas → Validação)

#### Q1: Viabilidade Técnica (Abertas)

**[Foco em feasibility]**
"Analisando Meu PDI como codebase, qual é sua avaliação inicial de viabilidade do ProjectAdapter? É factível descobrir ≥80% automaticamente?"

**Variações se resposta vaga:**
- "Quais são os maiores challenges técnicos?"
- "Qual arquivo/padrão é mais difícil de descobrir?"
- "Você vê edge cases que quebram descoberta?"

**Procure:**
- Análise de codebase (quão complex?)
- Padrões que são descobríveis (ORM models? APIs? Config?)
- Padrões que são hard (business logic? Relationships não-óbvias?)

---

#### Q2: Estratégia de Descoberta (Técnicas)

**[Como você faria]**
"Se você fosse implementar ProjectAdapter, qual seria sua estratégia de descoberta? Como você chegaria aos 80%?"

**Variações:**
- "Qual é a sequência de passos?"
- "Qual arquivo/padrão você atacaria primeiro?"
- "Qual é mais important: modules ou relationships?"

**Procure:**
- Priorização (o quê é fácil? Difícil?)
- Dependências (um padrão depende do outro?)
- Trade-offs (speed vs accuracy?)

---

#### Q3: Dores Técnicas (Abertas)

**[Pain points da implementação]**
"Na sua experiência com descoberta de estrutura, qual é a maior dor técnica?"

**Variações:**
- "O quê mais quebra?"
- "Qual é o padrão mais impredictível?"
- "Onde você gasta mais tempo debugando?"

**Procure:**
- Bugs recorrentes (qual é padrão?)
- Ambiguidade (onde decisão é hard?)
- Performance (qual análise é custosa?)

---

#### Q4: Validação - ≥80% é viável?

**[Testar hipótese de viabilidade]**
"Você concorda que ≥80% descoberta automática é viável em 1 week pra ProjectAdapter **core** (sem polimento)?"

**Se "sim":** "O que os últimos 20% seriam? Muito hard?"  
**Se "não":** "Qual % é realista? 50%? 60%?"  
**Se "depende":** "Do quê? Qual é o critério?"

**Procure:**
- Viabilidade realista (número % alcançável)
- O que fica de fora (aceitável?)
- Variação por padrão (Django descoberta vs API descoberta)

---

#### Q5: Integração com APOS (Técnicas)

**[Como ProjectAdapter se integra com resto do APOS]**
"Como você vê ProjectAdapter se conectando com BootstrapGate + ContextEngine + KnowledgeGraph? Quais são dependências?"

**Variações:**
- "Qual é a interface entre ProjectAdapter e BootstrapGate?"
- "ProjectAdapter output alimenta diretamente KnowledgeGraph?"
- "Context Engine precisa dados do ProjectAdapter?"

**Procure:**
- Dependências claras (qual módulo precisa qual)
- Data flow (ProjectAdapter → X → Y)
- Coupling (tight vs loose? Problema?)

---

#### Q6: Validação - Suficiência Arquitetural

**[Testar se design é sound]**
"Se ProjectAdapter descobrir ≥80% e passar pro BootstrapGate, você confia que o resto do pipeline (Gate → Ontology → KnowledgeGraph) vai funcionar?"

**Se "sim":** "Quais são assunções críticas que precisam ser true?"  
**Se "não":** "O que precisa mudar?"

**Procure:**
- Assunções que se não forem true, quebram tudo
- Riscos arquiteturais
- Pontos de falha

---

#### Q7: Realistic Timeline?

**[Sanity check]**
"De novo: ≥80% ProjectAdapter core em 1 week é realista? Qual é sua estimativa honesta?"

**Se "realista":** "Qual é tamanho story point?"  
**Se "não":** "O que levaria 2 weeks? 3 weeks?"

**Procure:**
- Estimativa técnica (valida planning ou não?)
- Complexity (1.5 SP? 3 SP? 5 SP?)
- Uncertainty (range: 1-2 weeks? 1-3 weeks?)

---

### Template de Captura (Preenchido Entrevistador)

```markdown
## ENTREVISTA 2: SME Técnico

**Data:** 2026-07-21  
**Duração:** XX min  
**Notas completas:**

### Q1: Viabilidade Técnica
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q2: Estratégia de Descoberta
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q3: Dores Técnicas
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q4: ≥80% é viável?
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q5: Integração com APOS
[Resposta verbatim]

**Síntese:** [Dependências: ___; Data flow: ___]

---

### Q6: Suficiência Arquitetural
[Resposta verbatim]

**Síntese:** [Assunções críticas: ___]

---

### Q7: Realistic Timeline?
[Resposta verbatim]

**Síntese:** Estimativa: [1.5 / 3 / 5] SP; Range: [1-2 / 1-3 / 2-4] weeks

---

### Insights-Chave
- [ ] ≥80% viável? SIM / NÃO / DEPENDE
- [ ] Maior pain point: [_______________]
- [ ] Arquitetura é sound? SIM / NÃO / PRECISA REFINO
- [ ] Timeline: Realista / Otimista / Pessimista
```

---

## 👷 Entrevista 3: Scrum Master / Tech Lead

**Tempo:** 20 min  
**Papel:** Valida execução, mapeia dependências, gerencia velocity  
**Output crítico:** Plano de sprint, derisking, pacing

### Preparação Prévia (enviar 24h antes)

```markdown
## Contexto pra SM/Tech Lead

**Pergunta chave:** Como executamos ProjectAdapter + Harness coverage em 1 week?

**Contexto:**
- Sprint Goal: Harness ≥80% + ProjectAdapter ≥80% discovery
- Dupla via = paralelo A (Harness) + B (ProjectAdapter)
- Milestone Dia 2 = decisão de continuar dupla via ou converger

**Você vai responder:**
- Viabilidade de dupla via
- Dependências entre trabalhos
- Velocity realista
- Plano de Dia 2 decision
```

### Questões (Abertas → Planejamento → Validação)

#### Q1: Dupla Via é Factível? (Abertas)

**[Foco em execução paralela]**
"Na sua opinião, dupla via (Harness + ProjectAdapter paralelo) é factível em 1 week? Ou devemos serial?"

**Variações:**
- "Quais são dependências entre os dois tracks?"
- "Qual é mais critical path?"
- "Se um atrasa, o outro consegue continuar?"

**Procure:**
- Acoplamento (tight ou loose?)
- Criticality (qual é blocker?)
- Fallback (se um fala, o que fazemos?)

---

#### Q2: Pacing para Dia 2 Milestone (Planejamento)

**[Como você estruturaria o pacing]**
"Como você pensa em estruturar Dia 1-2 pra ter dados suficientes no milestone decision do Dia 2?"

**Variações:**
- "Qual task roda Dia 1? Qual Dia 2?"
- "Como você valida % de descoberta?"
- "Qual é 'definition of done' pra milestone?"

**Procure:**
- Sequência lógica (o que primeiro?)
- Validação cedo (como sabes que tá on track?)
- Decision criteria (o que você precisa saber no Dia 2?)

---

#### Q3: Dores de Execução Paralela (Abertas)

**[Pain points de dupla via]**
"Na sua experiência, qual é a maior dor de dupla via paralela?"

**Variações:**
- "O quê mais quebra quando fazes paralelo?"
- "Como você previne context switching?"
- "Qual é o risco mais alto?"

**Procure:**
- Problemas reais (comunicação? Sync?)
- Mitigações que funcionam (standups? Reviews?)
- Velocity impact (paralelo custa quantos % em overhead?)

---

#### Q4: Validação - 2 SPs é suficiente? (Validação)

**[Testar se estimativa é sound]**
"Você concorda que 2 SP por track (Harness + ProjectAdapter = 4 SP total + 1 buffer) é realista pra atingir milestone Dia 2?"

**Se "sim":** "O que faz você confiante? Qual é assumption crítica?"  
**Se "não":** "Qual é mais realista? 3 SP? 4 SP?"

**Procure:**
- Validação de estimativa (está certa ou não?)
- Assumptions críticas (se falharem, tudo falha)
- Slack necessário (quanto buffer é safeguard?)

---

#### Q5: Convergência Dia 2 (Planejamento)

**[Decision tree do milestone]**
"Se Dia 2 milestone vier bom (≥70% em ambos), como você estrutura Dia 3-5 pra convergir? E se vier ruim?"

**Variações:**
- "Qual é plano A se ambos ≥70%?"
- "Qual é plano B se ProjectAdapter <50%?"
- "Qual é plano C se Harness <60%?"

**Procure:**
- Contingency planning (não deixar pra Dia 2)
- Sequência pós-milestone (qual order convergir?)
- Fallback tasks (o quê fazer se uma falha?)

---

#### Q6: Validação - Risco Arquitetural (Técnica)

**[Testar se risks são mitigados]**
"Você vê riscos arquiteturais em ProjectAdapter ou integração com BootstrapGate que precisam ser mitigados **antes** de Sprint 2?"

**Se "sim":** "Qual é mitigação? Proof-of-concept? Design review?"  
**Se "não":** "O quê te deixa confiante?"

**Procure:**
- Riscos identificados (PoC? Design? Integration?)
- Mitigação (o que fazer pra deriscar?)
- Timing (quando validar? Dia 1? Dia 2?)

---

#### Q7: Velocity Baseline Confirmado? (Validação)

**[Sanity check final]**
"R0 velocity foi ~7 SP/week. Você confirma que 4 SP + buffer em R1.1 é realista? Ou ajustamos?"

**Se "realista":** "O que mudou vs R0 pra velocity ser mesmo/diferente?"  
**Se "não":** "Qual % adjustment (80%? 60%? 120%)?"

**Procure:**
- Validação vs R0 baseline
- Justificativa de mudança (por quê mais/menos lento?)
- Revised velocity (pra Sprint 1 e Sprint 2-3)

---

### Template de Captura (Preenchido Entrevistador)

```markdown
## ENTREVISTA 3: Scrum Master / Tech Lead

**Data:** 2026-07-21  
**Duração:** XX min  
**Notas completas:**

### Q1: Dupla Via é Factível?
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q2: Pacing para Dia 2 Milestone
[Resposta verbatim]

**Síntese:** [Milestone success criteria: ___]

---

### Q3: Dores de Execução Paralela
[Resposta verbatim]

**Síntese:** [1 linha]

---

### Q4: 2 SPs é suficiente?
[Resposta verbatim]

**Síntese:** Validado / Não validado; Assumptions: [___]

---

### Q5: Convergência Dia 2
[Resposta verbatim]

**Síntese:** [Plano A: ___; Plano B: ___; Plano C: ___]

---

### Q6: Risco Arquitetural?
[Resposta verbatim]

**Síntese:** Riscos: [___]; Mitigação: [___]; Timing: [___]

---

### Q7: Velocity Baseline Confirmado?
[Resposta verbatim]

**Síntese:** Velocity R1.1: [__] SP/week (vs R0: 7 SP/week)

---

### Insights-Chave
- [ ] Dupla via viável? SIM / NÃO / COM RISCO
- [ ] Milestone Dia 2 criteria claro? SIM / NÃO
- [ ] Convergência plan defined? SIM / NÃO
- [ ] Velocity validated? SIM / NÃO
```

---

## 📝 Síntese & Consolidação

### Timing da Síntese

**Depois das 3 entrevistas** (total: 1 hora, 14:00-15:00):
- **15:00-15:30:** Síntese (consolidar em documento)
- **15:30-16:00:** Comunicação ao time

### Estrutura de Síntese (`SYNTHESIS.md`)

```markdown
# SÍNTESE: Entrevistas com Stakeholders — R1 Sprint 1

**Data:** 2026-07-21  
**Entrevistador:** [___]  
**Facilitador síntese:** [___]

---

## 🎯 Hypothesis Validation

### H1: ≥80% descoberta automática é suficiente?

| Stakeholder | Resposta | Confiança |
|------------|----------|-----------|
| CEO/Product | SIM / NÃO / DEPENDE | Alta / Média / Baixa |
| SME Técnico | SIM / NÃO / DEPENDE | Alta / Média / Baixa |
| SM/Tech Lead | SIM / NÃO / DEPENDE | Alta / Média / Baixa |

**Consolidação:** [Consenso ou divergência?]

**Ação:** [Se divergência, qual path escolhemos?]

---

### H2: Dupla via (Harness + ProjectAdapter) é viável?

| Stakeholder | Resposta | Confidence |
|------------|----------|-----------|
| CEO/Product | SIM / NÃO | [Prioridade clara] |
| SME Técnico | SIM / NÃO | [Acoplamento avaliado] |
| SM/Tech Lead | SIM / NÃO | [Execução validada] |

**Consolidação:** [Dupla via recomendado? Ou serial?]

**Ação:** [SPRINT_PLANNING.md ajusta pra dupla via / serial]

---

### H3: Timeline 1-week é realista?

| Stakeholder | Avaliação | Confidence |
|------------|-----------|-----------|
| CEO/Product | Realista / Otimista / Pessimista | [___] |
| SME Técnico | Realista / Otimista / Pessimista | [___] |
| SM/Tech Lead | Realista / Otimista / Pessimista | [___] |

**Consolidação:** [Consenso ou ajuste necessário?]

**Ação:** [Se ajuste, qual é nova estimativa?]

---

## 🎓 Insights-Chave (Por Stakeholder)

### CEO/Product Insights
- **Prioridade principal:** [ProjectAdapter / Harness / Ambos]
- **Pain point crítico:** [___]
- **Success criteria:** [___]
- **Expectativa no Dia 2:** [___]

### SME Técnico Insights
- **Viabilidade ≥80%:** [Alta / Média / Baixa]
- **Maior challenge:** [___]
- **Arquitetura recomendada:** [___]
- **Riscos principais:** [___]

### SM/Tech Lead Insights
- **Pacing factível:** [Sim, com risco / Sim / Não]
- **Milestone Dia 2 criteria:** [___]
- **Convergência plan:** [___]
- **Velocity realista:** [__] SP/week

---

## 🚨 Riscos Identificados

| Risco | Prob | Impacto | Mitigação | Dono |
|-------|------|---------|-----------|------|
| [___] | [___] | [___] | [___] | [___] |

---

## ✅ Decisões Resultantes

**Decisão 1:** [Dupla via confirmada / Serial necessário / Ajuste de scope]  
**Justificativa:** [Baseado em feedback de ___]  
**Ação:** [SPRINT_PLANNING.md é atualizado; team sincronizado]

**Decisão 2:** [Milestone Dia 2 criteria = ___]  
**Justificativa:** [Consenso de CEO/SME/SM]  
**Ação:** [BOARD.md + SPRINT_PLANNING.md documentam]

**Decisão 3:** [Timeline ajustado? SIM/NÃO; Novo: ___]  
**Justificativa:** [Validação de velocity]  
**Ação:** [Sprint planning revisto se necessário]

---

## 📋 Próximos Passos

- [ ] Síntese compartilhada com team (15:30)
- [ ] SPRINT_PLANNING.md atualizado (com decisões)
- [ ] BOARD.md atualizado (com criteria clarificado)
- [ ] Standup Dia 2 agendado (16:00 — milestone decision)
```

---

## 🎬 Execução — Passo a Passo

### Pré-Entrevista (Antes 14:00)

- [ ] Imprima este documento (ou abra em 3 abas)
- [ ] Prepare 3 timers (20 min cada)
- [ ] Confirme com stakeholders (Slack/email rápido)
- [ ] Abra 3 documentos de captura (ou use template acima)
- [ ] Estude R0_REALITY_CHECK + R1_PLAN_REVISED (contexto crítico)

### Entrevista 1 (14:00-14:20)

- **Antes:** "Essa entrevista vai alimentar design de ProjectAdapter"
- **Durante:** Questões Q1-Q7 (abertas primeiro)
- **Depois:** "Obrigado. Seus insights vão pro síntese"
- **Captura:** Preencha template imediatamente

### Entrevista 2 (14:20-14:40)

- Repita fluxo (diferente stakeholder, mesmas questões estrutura)
- Procure por divergência ou confirmação vs Entrevista 1

### Entrevista 3 (14:40-15:00)

- Repita fluxo (foco em execução)
- Capture pacing + convergência plan

### Síntese (15:00-15:30)

- Consolidar 3 templates em `SYNTHESIS.md`
- Validar hypotheses (consensus?)
- Identificar riscos
- Documentar decisões

### Comunicação (15:30-16:00)

- Compartilhe síntese com team
- "Aqui tá os insights dos stakeholders. Impacta assim:"
- Ajuste SPRINT_PLANNING.md se decisões mudaram

---

## 🎓 Exemplos de Captura (Verbatim)

### Exemplo Q3 (Dores Atuais) — CEO/Product

**Pergunta:** "Qual é a maior dor que você sente hoje com descoberta de estrutura?"

**Resposta (verbatim):**  
"Toda vez que chega um novo dev, ou a gente precisa entender uma parte da codebase, a gente faz o mesmo processo: procurar models, entender relacionamentos, encontrar adapters que já existem. Demora umas 4-6 horas pra um dev novo fazer deploy do Meu PDI. E aí a gente sempre esquece de um padrão ou adapter, então ele descobre só quando precisa. ProjectAdapter seria game-changer se conseguisse pegar isso auto."

**Síntese:** Onboarding é lento (4-6h); descoberta manual é recorrente + error-prone

---

### Exemplo Q2 (Criticidade) — SME Técnico

**Pergunta:** "Você concorda que ≥80% descoberta automática é viável em 1 week?"

**Resposta (verbatim):**  
"Sim, é viável. Models e adapters são descobríveis via AST parsing + imports. Relationships são harder — tem muito Django magic que requer execução ou heurística. Mas 80% é viável: models ✅, adapters ✅, major relationships ✅. Os últimos 20% seria edge cases tipo custom middleware ou monkey patches que realmente precisam análise manual."

**Síntese:** ≥80% viável via AST + heuristics; últimos 20% é edge cases (aceitável)

---

### Exemplo Q5 (Convergência) — SM/Tech Lead

**Pergunta:** "Se Dia 2 milestone vier bom (≥70%), como você estrutura Dia 3-5 pra convergir?"

**Resposta (verbatim):**  
"Plano A: Se ambos ≥70%, a gente converge em Dia 3-4 em integração (ProjectAdapter → BootstrapGate → Ontology). Plano B: Se ProjectAdapter <50%, pausamos, focamos 100% em Harness (que é crítico pro harness funcionar mesmo). Plano C: Se Harness <60%, temos problema — pausamos tudo, debugamos, replanejamod. Mas eu acho que Dia 2 vai mostrar que dupla via funciona."

**Síntese:** Convergência plan: integração full se ambos ≥70%; fallback to Harness-only se ProjectAdapter <50%

---

## 📚 Referências

**Documentação importante pra ler ANTES de entrevistar:**

- [R0_REALITY_CHECK.md](../../analysis/R0_REALITY_CHECK.md) — O que R0 realmente entregou
- [R1_PLAN_REVISED.md](../../analysis/R1_PLAN_REVISED.md) — Scope real de R1
- [SPRINT_PLANNING.md](SPRINT_PLANNING.md) — Current sprint plan
- [../README.md](../README.md) — Context de release R1

---

**Criado:** 2026-07-21  
**Tipo:** Stakeholder Research Interview  
**Output:** SYNTHESIS.md (consolidar aqui)  
**Timing:** Dia 1 Sprint 1 (14:00-16:00)  
**Público:** Jader (entrevistador) + team (síntese)

