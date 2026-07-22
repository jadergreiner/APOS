# Interview Execution Checklist — R1 Sprint 1 Stakeholder Research

**Dia:** 2026-07-21 (Dia 1 do Sprint)  
**Timing:** 14:00-16:00 (3 entrevistas paralelas 20 min + síntese 30 min)  
**Entrevistador:** [Jader ou delegado]

---

## ⏰ Timeline Executiva (Copie/Cole)

```
14:00-14:20  | Entrevista 1: CEO/Product (Jader)
14:20-14:40  | Entrevista 2: SME Técnico
14:40-15:00  | Entrevista 3: Scrum Master/Tech Lead
15:00-15:30  | Consolidação em SYNTHESIS.md
15:30-16:00  | Comunicação ao team (apresenta decisões)
```

---

## 📋 PRÉ-ENTREVISTA (Fazer antes 14:00)

- [ ] Leia [STAKEHOLDER_INTERVIEWS.md](STAKEHOLDER_INTERVIEWS.md) (seções Contexto + Princípios)
- [ ] Leia [R1_PLANNING_GUIDE.md](../R1_PLANNING_GUIDE.md) (pra ter contexto de R1 completo)
- [ ] Imprima este checklist (ou abra em split-screen)
- [ ] Abra [SYNTHESIS.md](SYNTHESIS.md) em editor (pra preencher depois)
- [ ] 3x timers de 20 min prontos (phone, watch, ou no.clock)
- [ ] Slack/calendário sincronizado (confirme stakeholders)

**Checklist PRÉ:**
- [ ] Você entende sprint goal (Harness ≥80% + ProjectAdapter ≥80% discovery)
- [ ] Você entende as 3 hipóteses críticas (≥80% suficiente? Dupla via viável? Timeline realista?)
- [ ] Você tem exemplos de bom/ruim entrevista (veja abaixo)
- [ ] Você tá calm e focado (essa síntese é importante pra Dia 2 decision)

---

## 🎤 Durante Entrevista — Comandos Rápidos

### Abertura (1 min)

```
"Oi [Nome]. Essa entrevista vai alimentar nosso design de ProjectAdapter.
Você é [CEO/SME/SM] e seus insights são críticos pra gente validar 
hipóteses do sprint. São 20 min, ok? Sem certo/errado — é sua perspectiva."
```

### Durante Resposta — Se Vago/Curto

```
[ESCUTE 30s completo. Depois, se curto:]

"Entendi. Me fale mais sobre [tópico]. 
Qual é um exemplo específico?"
```

### Durante Resposta — Se Longo/Tangencial

```
[Escute com empatia. Depois, se muito longo:]

"Excelente context. Voltando pro essencial: 
você acha que [questão chave] é [sim/não]?"
```

### Validação (Transição suave)

```
"Deixa eu validar que entendi. Você tá dizendo que 
[resumo 1-2 frases]. Isso é correto?"

[Espere confirmação]

"Perfeito. Próxima pergunta..."
```

### Fechamento (30s antes fim timer)

```
"Última pergunta rápida: [Q7]. Depois a gente consolida tudo."
```

---

## 📌 Questões Rápidas (Copie/Cole)

### Entrevista 1: CEO/Product

**Q1 (Abertas):** "Fale-me sobre sua experiência atual com adaptadores em Meu PDI. O que você faz hoje?"

**Q2 (Validação):** "Você concorda que descoberta automática ≥80% seria suficiente pra Meu PDI começar?"

**Q3 (Abertas):** "Qual é a maior dor que você sente hoje com descoberta de estrutura?"

**Q4 (Abertas):** "Se ProjectAdapter existisse amanhã, como você usaria?"

**Q5 (Validação):** "Se ProjectAdapter descobrir ≥80% no Dia 2, é o bastante pra desbloquear?"

**Q6 (Tradeoff):** "No Dia 2, qual é mais crítico: Harness coverage (≥80%) ou ProjectAdapter (≥80% discovery)?"

**Q7 (Realistic):** "Você acha que ≥80% em 1 week é realista ou otimista?"

---

### Entrevista 2: SME Técnico

**Q1 (Viabilidade):** "Analisando Meu PDI, qual é sua avaliação inicial de viabilidade de ProjectAdapter ≥80%?"

**Q2 (Estratégia):** "Se você fosse implementar, qual seria sua estratégia? Como chegaria aos 80%?"

**Q3 (Dores):** "Na sua experiência, qual é a maior dor técnica de descoberta automática?"

**Q4 (Validação):** "Você concorda que ≥80% descoberta é viável em 1 week pra core?"

**Q5 (Integração):** "Como você vê ProjectAdapter se conectando com BootstrapGate + ContextEngine + KnowledgeGraph?"

**Q6 (Validação arquitetural):** "Você confia que se ProjectAdapter entregar ≥80%, o resto do pipeline funciona?"

**Q7 (Timeline):** "≥80% em 1 week — realista ou otimista? Qual sua estimativa?"

---

### Entrevista 3: Scrum Master/Tech Lead

**Q1 (Dupla via):** "Dupla via (Harness + ProjectAdapter paralelo) é factível em 1 week? Ou serial?"

**Q2 (Pacing):** "Como você estruturaria Dia 1-2 pra ter dados suficientes no milestone decision?"

**Q3 (Dores):** "Na sua experiência, qual é a maior dor de dupla via paralela?"

**Q4 (Validação):** "Você concorda que 2 SP por track (4 SP + buffer total) é realista pra atingir milestone?"

**Q5 (Convergência):** "Se Dia 2 vier bom (≥70% em ambos), como você estrutura Dia 3-5? E se ruim?"

**Q6 (Risco):** "Você vê riscos arquiteturais que precisam ser mitigados antes Sprint 2?"

**Q7 (Velocity):** "R0 velocity foi 7 SP/week. Você confirma 4 SP + buffer em R1.1 é realista?"

---

## ✍️ Captura Rápida (Template)

**Durante entrevista, preencha:**

```markdown
## ENTREVISTA X: [Nome]

**Q1:** [Verbatim key quote]
**Síntese:** [1 linha]

**Q2:** [Verbatim key quote]
**Síntese:** [1 linha]

[... repita Q3-Q7]

**Decisão:** [SIM/NÃO pra cada hipótese]
**Confiança:** [Alta/Média/Baixa]
```

---

## 🚨 Sinais de Alerta (Red Flags)

**Se escutar isso, explore mais:**

| Red Flag | Como responder |
|----------|-----------------|
| "Hmm, nunca pensei nisso" | "Ok, sem pressão. O que você acha agora?" |
| "Depende de muita coisa" | "Do quê especificamente?" |
| "Teoricamente, sim, mas..." | "Mas o quê? Qual é o real blocker?" |
| "Acho difícil" (sem detalhe) | "Difícil em quê? Tempo? Complexidade? Incerteza?" |
| "Vai dar problema" (vago) | "Qual tipo de problema? Como você mitigaria?" |

**Objetivo:** Transformar vago em concreto.

---

## ✅ Pós-Entrevista (Imediatamente Depois)

Enquanto memória está fresca:

- [ ] Tipo de resposta (SIM/NÃO/DEPENDE pra cada questão)
- [ ] Confiança (Alta/Média/Baixa)
- [ ] Verbatim quotes (pelo menos 2-3 frases chave por questão)
- [ ] Síntese 1-linha (pra consolidação depois)

---

## 🔄 Consolidação (15:00-15:30)

**Imediatamente após as 3 entrevistas:**

1. **Transfira** notas de captura pra [SYNTHESIS.md](SYNTHESIS.md)
2. **Consolide** tabelas de hypothesis validation
3. **Identifique** riscos (pelo menos 3)
4. **Documente** decisões 1-4
5. **Escreva** 3-5 insights principais (não seja tímido)

**Tempo:** 30 min (não perfeito, é síntese dinâmica)

---

## 📢 Comunicação (15:30-16:00)

**Depois da síntese, comunique ao team:**

```
"Rodamos as 3 entrevistas. Aqui estão os highlights:

HIPÓTESE 1 (≥80% suficiente): [SIM/NÃO/DEPENDE]
→ [1-2 linhas justificativa]

HIPÓTESE 2 (Dupla via viável): [SIM/NÃO/COM RISCO]
→ [1-2 linhas justificativa]

HIPÓTESE 3 (Timeline realista): [SIM/NÃO/AJUSTE NECESSÁRIO]
→ [1-2 linhas justificativa]

DECISÃO RESULTANTE:
→ [O que muda no SPRINT_PLANNING.md? Em que trilha focamos?]

Síntese completa em: [SYNTHESIS.md](SYNTHESIS.md)

Próximos passos: [Ações de hoje pra executar amanhã]
"
```

**Slack thread:** Compartilhe síntese link + decisões
**Daily standup:** Menção decisões críticas (pra time estar ciente)

---

## 🎓 Exemplos de Bom vs Ruim

### ❌ Pergunta Ruim (Sugere resposta)

```
"Você acha que ≥80% é bom o bastante, certo?"
```

**Problema:** Sugere resposta ("certo?")

---

### ✅ Pergunta Boa (Aberta + Validação)

```
"Qual % de descoberta seria suficiente pra você?
[Escuta resposta]
Você concorda que ≥80% é aquele nível? Por quê?"
```

**Por quê:** Deixa pessoa falar; depois valida

---

### ❌ Resposta Ruim (Aceitou superficial)

```
Entrevistador: "ProjectAdapter é viável?"
Stakeholder: "Sim."
Entrevistador: "Ótimo. Próxima pergunta..."
```

**Problema:** "Sim" é vago. Por quê sim? Qual confiança?

---

### ✅ Resposta Boa (Explorou)

```
Entrevistador: "ProjectAdapter é viável?"
Stakeholder: "Sim, acho que sim."
Entrevistador: "Legal. Me fale mais. O que te deixa confiante?"
Stakeholder: "Models e adapters são descobríveis via AST parsing. 
Relacionamentos são harder, mas 80% é viável."
Entrevistador: "Entendi. Os últimos 20% seria quê, então?"
Stakeholder: "Edge cases tipo middleware custom ou monkey patches."
```

**Por quê:** Tem detalhe, confiança clara, edge cases mapeados

---

## 📌 Dicas de Ouro

1. **Silêncio é ouro.** Se terminou pergunta, fica quieto 30s. Deixa pessoa pensar.

2. **"Por quê?" é seu amigo.** Quando ouve resposta, próxima pergunta é sempre "Por quê?"

3. **Confirme que entendeu.** "Deixa eu validar: você está dizendo que..."

4. **Tome notas verbatim.** Quotes reais vale mais que sua interpretação.

5. **Não debate durante entrevista.** Se discorda, salva pra síntese. Entrevista é coleta, não argumentação.

6. **Respeite o tempo.** 20 min é apertado. Se entrevistado fala muito, redirecione suave: "Ótimo, deixa eu ir pra próxima pra pegar seus insights em 2-3 mais."

7. **Comece aberto, termina validando.** Q1-3 abertas (entender experiência), Q4-7 validação (confirmar hipóteses).

---

## 🎯 Definição de Sucesso

**Você fez entrevista bem se:**

- [ ] Cada stakeholder respondeu Q1-7 (não precisa ser perfeito)
- [ ] Tem pelo menos 2-3 quotes verbatim por entrevista
- [ ] Sabe SIM/NÃO/DEPENDE pra 3 hipóteses (não vago)
- [ ] Identificou pelo menos 3 riscos distintos
- [ ] Consegue resumir síntese em 5 min pro team
- [ ] SYNTHESIS.md preenchido e coerente

---

## 🆘 Troubleshooting

| Problema | Solução |
|----------|---------|
| Stakeholder não mostra | Começa entrevista com outros; depois tenta reschedule |
| Resposta muito vaga | Pergunta "Qual é um exemplo específico?" 3x |
| Entrevista vai muito longo | "Rápido: [pergunta chave]. Depois a gente detalha." |
| Você não entende técnico | "Desculpa, não sou técnico. Simplifica?" |
| Síntese tá vaga depois | Volta pra notas; adiciona 1-2 quotes verbatim |
| Decisões não ficaram claras | Agenda 15 min follow-up com stakeholders; valida |

---

## 📊 Métricas de Execução

**Como saber se rodou bem:**

```
[ ] Entrevistas finalizadas: 3/3
[ ] Duração respeitada: 20 min cada
[ ] Notas capturadas: Sim
[ ] Síntese preenchida: Sim
[ ] Hipóteses validadas: 3/3 (SIM/NÃO/DEPENDE)
[ ] Decisões documentadas: 4/4
[ ] Riscos identificados: ≥3
[ ] Team comunicado: Sim (síntese + decisões)
[ ] SPRINT_PLANNING.md atualizado: [SIM / não necessário]
```

---

## 📞 Escalation

**Se alguma decisão é "blocker" (tá paralisando sprint):**

→ Agenda 30 min com Jader + stakeholders pra quebra-empate  
→ Não deixa indefinido; melhor decisão errada que indefinição  
→ Documente decisão + reasoning em SYNTHESIS.md

---

## 📁 Arquivos para Referência

- **[STAKEHOLDER_INTERVIEWS.md](STAKEHOLDER_INTERVIEWS.md)** — Roteiro completo (leia antes)
- **[SYNTHESIS.md](SYNTHESIS.md)** — Template de consolidação (preencha depois)
- **[SPRINT_PLANNING.md](SPRINT_PLANNING.md)** — Sprint plan (atualiza se decisões mudam)
- **[R1_PLANNING_GUIDE.md](../R1_PLANNING_GUIDE.md)** — Context de R1 completo

---

## ⚡ TL;DR (Pra When You're in a Rush)

1. **Abra timer.** 20 min por entrevista.
2. **Q1 sempre aberta.** Deixa pessoa falar.
3. **Q7 sempre validação.** Confirma SIM/NÃO.
4. **Notas durante.** Verbatim quotes.
5. **Síntese depois.** Tabelas + decisions.
6. **Comunique.** Slack + standup.

---

**Criado:** 2026-07-21  
**Usar:** Dia 1 Sprint 1 (14:00-16:00)  
**Entrevistador:** Jader ou delegado  
**Output:** SYNTHESIS.md preenchido + team sincronizado  

Boa entrevista! 🎤

