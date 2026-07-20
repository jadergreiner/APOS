# JTBD Interviews — Documentação de Descobertas

**Sprint:** 0.2 - JTBD Deep Dive
**Período:** 22-26 julho 2026
**Entrevistador:** Jader Greiner
**Framework:** Jobs to Be Done (Push/Pull/Habit/Anxiety Forces)

---

## Entrevista #1: [Persona Tipo]

**Data:** [Data]  
**Duração:** [45-60 min]  
**Persona:** [Nome, Role, Equipe]  
**Contexto:** [Company, tamanho equipe, stack tech]  

### Resumo de Descobertas (3-5 bullets)

- **Push Force (Frustração):** [O que empurra para solução]
- **Pull Force (Atração):** [O que puxa para APOS]
- **Habit Force (Status Quo):** [O que mantém preso no workflow atual]
- **Anxiety Force (Medo):** [O que gera hesitação em adotar]

### Key Findings

**Pain Point #1: [Tema]**
- Frequência: [Quantas vezes por semana/dia/mês]
- Impacto: [Tempo perdido, qualidade, frustração]
- Contexto: [Quando ocorre, com quem]

> **Direct Quote:**  
> "[Pessoa]: [Aspas exatas do que disse]"

**Pain Point #2: [Tema]**
- Frequência: [...]
- Impacto: [...]
- Contexto: [...]

> **Direct Quote:**  
> "[Pessoa]: [Aspas exatas]"

### Validação de VALUE_PROPOSITION

| Aspecto | Validou? | Feedback |
|---------|----------|----------|
| Proposta de Valor | ✅/❌/🤔 | [Pessoa concordou/discordou/questiona] |
| Diferenciação | ✅/❌/🤔 | [Resonância com ontologia + trust score] |
| Casos de Uso | ✅/❌/🤔 | [Cenários mencionados são reais?] |
| Benefícios Quantificáveis | ✅/❌/🤔 | [-25% tokens, -50% latência, etc ressoam?] |

### Jobs Framework Analysis

**Push Forces (O que empurra):**
```
- [Force 1]: [Descrição + frequência + impacto]
- [Force 2]: [...]
```

**Pull Forces (O que atrai):**
```
- [Pull 1]: [Descrição + diferencial]
- [Pull 2]: [...]
```

**Habit Forces (Status Quo):**
```
- [Habit 1]: [Descrição + switching cost]
- [Habit 2]: [...]
```

**Anxiety Forces (Medo de adotar):**
```
- [Anxiety 1]: [Descrição + severidade]
- [Anxiety 2]: [...]
```

### Padrões Identificados

**Alinhamento com outras personas:**
- Persona A também mencionou [tema similar]?
- Persona B viu [pain] de forma diferente?

**Surpresas / Contradições:**
- Esperava [X], mas pessoa descreveu [Y]
- Questiona [aspecto de VALUE_PROPOSITION]

### Interesse em Piloto

**Pergunta:** Estaria aberto a ser early adopter?  
**Resposta:** [Sim / Não / Talvez]  
**Condições:** [Se há condições específicas]  
**Timeline:** [Quando poderia fazer piloto]  

### Follow-up Actions

- [ ] Enviar obrigado
- [ ] Revisar se há perguntas de follow-up
- [ ] Adicionar a lista de early adopters (se interessado)
- [ ] Referência para outra persona?

### Notas Internas

[Qualquer observação pessoal, tonalidade, insights extras que não couberam acima]

---

## Entrevista #2

[Repetir estrutura acima]

---

## Entrevista #3

[Repetir estrutura acima]

---

## Entrevista #4

[Repetir estrutura acima]

---

## Entrevista #5

[Repetir estrutura acima]

---

## Consolidação: Padrões Comuns

### Push Forces (Agregado)

**Tema 1: [X]**
- Personas que mencionaram: [1, 3, 5]
- Frequência média: [X vezes por semana]
- Impacto médio: [Resultado quantificável]
- Intensidade (1-10): [9]

**Tema 2: [Y]**
- Personas: [2, 4]
- Frequência: [...]
- Impacto: [...]
- Intensidade: [...]

**Tema 3: [Z]**
- [...]

### Pull Forces (Agregado)

**Diferenciador #1: [Ontologia + Trust Score]**
- Personas atraídas: [1, 3, 5]
- Nível de atração (1-10): [8]
- Mencionado espontaneamente? [Sim/Não]

**Diferenciador #2: [Automatic Governance]**
- Personas: [2, 4]
- Nível: [...]
- Espontâneo? [...]

**Diferenciador #3: [...]**
- [...]

### Habit Forces (Agregado)

**Blocker #1: [Jira Integration]**
- Personas afetadas: [1, 2, 4]
- Severidade (1-10): [7]
- Mitigation: [Precisa build connector pra Jira?]

**Blocker #2: [Learning Curve]**
- Personas: [3, 5]
- Severidade: [...]
- Mitigation: [...]

**Blocker #3: [...]**
- [...]

### Anxiety Forces (Agregado)

**Risk #1: [Data Quality]**
- Personas preocupadas: [2, 4]
- Severity (1-10): [6]
- Mitigation: [Como garantir qualidade?]

**Risk #2: [Integration Complexity]**
- Personas: [1, 3]
- Severity: [...]
- Mitigation: [...]

**Risk #3: [...]**
- [...]

---

## Validação de Hipóteses

### VALUE_PROPOSITION

**Hipótese:** APOS reduz retrabalho de contexto em -80%

| Persona | Mencionou Retrabalho? | Magnitude | Validou? |
|---------|----------------------|-----------|----------|
| PM Leader | Sim | "3-5x/semana" | ✅ |
| EM | Sim | "Constant" | ✅ |
| AI Architect | Não | — | ❌ |
| Product Ops | Sim | "10-15h/semana" | ✅ |
| Early Adopter | Sim | "Daily frustration" | ✅ |

**Conclusão:** 4/5 validaram (80% de confiança)  
**Ajuste necessário:** Mensagem AI Architect diferente (context fetching, não retrabalho)

### COMPETITIVE_POSITIONING

**Hipótese:** APOS é único em "formal ontology + trust scoring"

| Persona | Concorda? | Diferencial Visto Como? |
|---------|-----------|------------------------|
| PM Leader | Sim | Sim, visual + confiança |
| EM | Sim | Sim, quality gates |
| AI Architect | Sim | Sim, semântica formal |
| Product Ops | Talvez | "Neo4j também faz" |
| Early Adopter | Sim | Sim, única solução |

**Conclusão:** 4/5 validaram diferencial  
**Ajuste:** Product Ops precisa understand diferential vs. Neo4j (pricing? implementation cost?)

### OKRs & ROADMAP

**Hipótese:** R0-R1 timeline (Sep 2026 primeiro MVP) é viável?

| Persona | Timeline Viável? | Feedback |
|---------|------------------|----------|
| PM Leader | Sim | "Q3 é agressivo mas possível" |
| EM | Talvez | "Depende de escopo de MVP" |
| AI Architect | Sim | "KG é sólido, MVP é rápido" |
| Product Ops | Não | "Precisa 4+ meses mínimo" |
| Early Adopter | Sim | "Somos pacientes, 6 meses OK" |

**Conclusão:** 3/5 validaram, 1 questionou  
**Ajuste:** Revisar timeline com EM + Product Ops, confirmar MVP scope

---

## Minimum Viable Proposition (MVP)

Baseado em 5 entrevistas, APOS MVP precisa ter MÍNIMO:

**Must-Have:**
- [ ] [Feature 1]: [Por que? Mencionado por X personas]
- [ ] [Feature 2]: [...]
- [ ] [Feature 3]: [...]

**Should-Have:**
- [ ] [Feature A]: [Validado por 3+ personas, não essencial]
- [ ] [Feature B]: [...]

**Nice-to-Have:**
- [ ] [Feature X]: [Mencionado por 1 persona]
- [ ] [Feature Y]: [...]

**NOT in MVP:**
- ❌ [Feature N]: [Apenas 1 persona, complexo demais, pode esperar R1.1]
- ❌ [Feature M]: [Ninguém pediu explicitamente]

---

## Job Statement

[Baseado em 5 entrevistas, qual é o JOB que personas estão tentando fazer?]

### Situação Trigger

[Contexto em que necessidade surge]

```
"When [situação], I need to [job],
so that I can [outcome que valor pessoal/profissional]"
```

**Exemplo:**
```
"When my team is planning a sprint and we have 20+ tasks in backlog,
I need to quickly understand which tasks map to which OKRs,
so that I can make data-driven prioritization decisions and avoid scope creep"
```

### Circunstâncias

**Quando:** [Frequência + contexto]  
**Quem:** [Personas specifically]  
**Onde:** [Ambiente de trabalho]  
**Com quem:** [Quem está envolvido]  

### Critérios de Sucesso

[Como persona mede sucesso de solução?]

1. **Métrica 1:** [Específica, mensurável] — Mencionado por X personas
2. **Métrica 2:** [...]
3. **Métrica 3:** [...]

**Exemplo:**
```
1. Redução de tempo em explicação de contexto: -50% (de 5h → 2.5h/semana)
2. Aumento de confiança em priorização: score passa de 5/10 → 8/10
3. Automation de roll-up: 0 horas manuais (100% automático)
```

### Competidores No Job

[Quem mais está resolvendo este job hoje?]

- Competitor A: [Como resolve?] [Fraquezas?]
- Competitor B: [...]

### Razão Pela Qual APOS Ganha

[Baseado em Push/Pull/Habit/Anxiety, por que APOS é solução certa?]

1. [Diferencial #1 que ressoou]
2. [Diferencial #2]
3. [...]

---

## Decisão: Prosseguir?

### Questões Críticas

- [ ] **Hipótese Principal Validada?** — 4/5 personas confirmaram value prop?
- [ ] **Job Clear?** — Consegue descrever job que APOS resolve em 1 frase?
- [ ] **MVP Defined?** — Sabe o mínimo que precisa build?
- [ ] **Early Adopters Interessados?** — 2+ personas topam fazer piloto?

### Recomendação

**Verde (Prosseguir com Confiança):**
- 4/5 personas validaram value prop
- Job clear e diferencial (vs competitors) óbvio
- 3+ interessados em piloto
- MVP scope agreed

**Amarelo (Iterar, Depois Prosseguir):**
- 3/5 personas validaram (não suficiente)
- Job não está claro
- Competidor surgiu que não previmos
- Interesse de piloto baixo (1 pessoa)

**Vermelho (Re-pensar Proposição):**
- <3 personas validaram
- Job é "nice-to-have", não "must-have"
- Anxiety forces superam pull forces
- Ninguém quer piloto

### Proximos Passos (se Verde)

- [ ] Documentar findings em JOB_STATEMENT.md
- [ ] Agendar piloto com 2-3 early adopters
- [ ] Sprint 0.3: Beta Prep
- [ ] R1: MVP Implementation

### Proximos Passos (se Amarelo)

- [ ] 2-3 entrevistas adicionais com diferentes personas
- [ ] Iterar VALUE_PROPOSITION.md com base em feedback
- [ ] Revisar competitive landscape
- [ ] Re-validar com 3+ personas
- [ ] Então, prosseguir

### Proximos Passos (se Vermelho)

- [ ] Deep dive com founders/stakeholders
- [ ] Reconsiderar customer segment?
- [ ] Reconsiderar value prop?
- [ ] Pivotear ou descartar?

---

**Entrevistas Completadas:** [ ] / 5  
**Job Statement Status:** [ ] Definido  
**Recomendação Final:** [ ] Verde / Amarelo / Vermelho

**Data de Consolidação:** [Data]
