# SÍNTESE: Entrevistas com Stakeholders — R1 Sprint 1

**Data:** 2026-07-21  
**Entrevistador:** [A preencher — Jader ou delegado]  
**Status:** [RASCUNHO / EM PROGRESSO / FINALIZADO]  
**Últimas mudanças:** [___]

---

## 🎯 Resumo Executivo (1 min read)

**3 hipóteses críticas validadas:**

1. **≥80% descoberta automática é suficiente?** → [SIM / NÃO / DEPENDE DE ___]
2. **Dupla via (Harness + ProjectAdapter) é viável?** → [SIM / NÃO / RISCO MÉDIO]
3. **Timeline 1-week é realista?** → [SIM / NÃO / COM AJUSTE]

**Decisão resultante:** [Continua dupla via / Serial em Dia 2 / Replanejamento necessário]

---

## 📊 Hypothesis Validation

### H1: ≥80% Descoberta Automática é Suficiente?

| Stakeholder | Resposta | Justificativa | Confiança |
|------------|----------|---------------|-----------|
| CEO/Product | SIM / NÃO / DEPENDE | [Preencha com citação] | Alta / Média / Baixa |
| SME Técnico | SIM / NÃO / DEPENDE | [Preencha com citação] | Alta / Média / Baixa |
| SM/Tech Lead | SIM / NÃO / DEPENDE | [Preencha com citação] | Alta / Média / Baixa |

**Consolidação:**

```
CONSENSO: [SIM / NÃO / MISTO]
  ├─ Se SIM: "≥80% descoberta é aceitável para MVP ProjectAdapter"
  ├─ Se NÃO: "Descoberta precisa ser ___%; e-o por: [motivo]"
  └─ Se MISTO: "Divergência entre [stakeholder] e [stakeholder]; resolução: [decision]"
```

**Implicação pra Sprint:** [Como isso afeta planejamento?]

---

### H2: Dupla Via (Harness + ProjectAdapter) é Viável?

| Stakeholder | Resposta | Critério | Confiança |
|------------|----------|----------|-----------|
| CEO/Product | SIM / NÃO | Prioridade: Harness >> ProjectAdapter / ProjectAdapter >> Harness / Ambos igual | Alta / Média / Baixa |
| SME Técnico | SIM / NÃO | Acoplamento: Tight / Loose / Nenhum | Alta / Média / Baixa |
| SM/Tech Lead | SIM / NÃO | Execução: Possível / Riscado / Impossível | Alta / Média / Baixa |

**Consolidação:**

```
RESULTADO: [Dupla via recomendada / Serial necessário / Risco alto, mas tentamos dupla]
  ├─ CEO/Product prioridade: [Harness / ProjectAdapter / Ambos]
  ├─ SME viabilidade técnica: [Acoplamento nível] 
  └─ SM/Tech Lead confiança execução: [Nível de confiança]
```

**Implicação pra SPRINT_PLANNING.md:** [Trilhas A/B continuam? Convertem em serial? Que mudança?]

---

### H3: Timeline 1-Week é Realista?

| Stakeholder | Avaliação | Base da Estimativa | Confidence |
|------------|-----------|-------------------|-----------|
| CEO/Product | Realista / Otimista / Pessimista | [Qual critério?] | Alta / Média / Baixa |
| SME Técnico | Realista / Otimista / Pessimista | [Qual critério?] | Alta / Média / Baixa |
| SM/Tech Lead | Realista / Otimista / Pessimista | [Qual critério?] | Alta / Média / Baixa |

**Consolidação:**

```
VELOCIDADE VALIDADA: [SIM / AJUSTE NECESSÁRIO]
  ├─ Se SIM: "4 SP (Harness + ProjectAdapter) em 1 week é realista"
  ├─ Se AJUSTE: "Novo target: [2 / 3 / 5] SP; timeline: [1 / 1.5 / 2] weeks"
  └─ Assumptions críticas:
     ├─ [ ] SME disponibilidade 100%
     ├─ [ ] Tech Lead Meu PDI não bloqueado
     └─ [ ] Meu PDI codebase estrutura esperada (não surpresa)
```

**Implicação pra Sprint:** [Velocity R1 = XX SP/week vs R0 = 7 SP/week; justificativa?]

---

## 🎓 Insights Consolidados (Por Dimensão)

### Dimensão 1: Experiência Atual com Adaptadores

**De CEO/Product:**
- Processo atual: [___]
- Frequência: [___]
- Tempo investido: [___]
- Confiança em resultado: [___]

**De SME Técnico:**
- Padrões descobríveis: [Models / APIs / Relationships / Config / Middleware / ___]
- Padrões difíceis: [___]
- Viabilidade AST: [Alta / Média / Baixa]

**De SM/Tech Lead:**
- Duração média onboarding novo dev: [___]
- Retrabalho % (retry discovery): [___]
- Blockers recorrentes: [___]

**Síntese:** [1-2 linhas consolidando]

---

### Dimensão 2: Dores de Ponto (Pain Points)

**Maior dor CEO/Product:**
- Descrição: [___]
- Frequência: [___]
- Impacto: [___]

**Maior pain técnico SME:**
- Descrição: [___]
- Causa raiz: [___]
- Impacto em estimativa: [___]

**Execução dor SM/Tech Lead:**
- Descrição: [___]
- Risco: [Alto / Médio / Baixo]
- Mitigação: [___]

**Síntese:** [Qual dor ProjectAdapter resolve? Qual fica?]

---

### Dimensão 3: Expectativas do ProjectAdapter

**CEO/Product expect:**
- Use case principal: [___]
- Success criteria: [___]
- Fallback aceitável: [___]

**SME Técnico expect:**
- Architecture: [___]
- Integration points: [___]
- Test strategy: [___]

**SM/Tech Lead expect:**
- Pacing: [___]
- Dependency management: [___]
- Escalation path: [___]

**Síntese:** [Expectativa alinhada? Gaps?]

---

### Dimensão 4: Criticidade & Priorização

**Tradeoff Dia 2 (Harness vs ProjectAdapter):**

| Stakeholder | Prioridade | Justificativa |
|------------|-----------|--------------|
| CEO/Product | Harness >> ProjectAdapter / ProjectAdapter >> Harness / Igual | [___] |
| SME Técnico | [___] | [Bloqueador? Nice-to-have?] |
| SM/Tech Lead | [___] | [Execution complexity?] |

**Decisão:** [Se consenso SIM; Se divergência, qual path?]

---

## 🚨 Riscos Identificados

| Risco | Descrição | Prob | Impacto | Identificado por | Mitigação |
|-------|-----------|------|---------|-----------------|-----------|
| [Risco 1] | [Descrição] | Alto / Médio / Baixo | Alto / Médio / Baixo | [Stakeholder] | [Ação] |
| [Risco 2] | [Descrição] | Alto / Médio / Baixo | Alto / Médio / Baixo | [Stakeholder] | [Ação] |
| [Risco 3] | [Descrição] | Alto / Médio / Baixo | Alto / Médio / Baixo | [Stakeholder] | [Ação] |

**Riscos a mitigar antes Dia 2:** [Qual? Como?]

---

## ✅ Decisões Resultantes

### Decisão 1: Dupla Via vs Serial

**Resultado:** [DUPLA VIA / SERIAL / HÍBRIDO]

**Justificativa:**
- CEO/Product: [Razão]
- SME Técnico: [Razão]
- SM/Tech Lead: [Razão]
- Consenso: [SIM / NÃO; se não, resolution applied]

**Ação:**
- [ ] SPRINT_PLANNING.md atualizado (trilhas A/B ou solo track)
- [ ] BOARD.md atualizado (tarefas reorganizadas)
- [ ] Team sincronizado (Slack + standup)

---

### Decisão 2: Milestone Dia 2 Success Criteria

**Critério de sucesso Harness:**
- Coverage: ≥ [70% / 75% / 80%]
- Tests: [Integração? Unit? Ambos?]
- Validação: [Coverage report / Manual review / Teste em Meu PDI real]

**Critério de sucesso ProjectAdapter:**
- Discovery: ≥ [50% / 70% / 80%] estrutura Meu PDI
- O quê descobrir: [Models / Relationships / Adapters / Config / Outros]
- Validação: [Inspeção manual + teste em Meu PDI]

**Decisão de Convergência:**
- Se ambos ≥ target: [Continua dupla via com integração / Converge em trilha única]
- Se 1 falha: [Plano B: abandona fraco? Pivota? Ajusta target?]
- Se ambos falham: [Dia 3 replaning / Estende sprint / Escalation]

**Ação:**
- [ ] Milestone criteria documentado em BOARD.md
- [ ] Standup Dia 2 16:00 agenda (decisão)
- [ ] Plano de convergência clear

---

### Decisão 3: Timeline & Velocity

**Validação R1.1 Velocity:**
- Sprint 1 target: [4 SP / 2 SP / 3 SP] (vs planejado 4 SP)
- R1 total realista: [15 SP em 3 weeks / 12 SP em 3 weeks / outro]
- Justificativa: [Vs R0 baseline 7 SP/week; Mudança? Por quê?]

**Timeline Ajustado:**
- [ ] SIM — timeline 1 week mantido; Sprint planning é ótimo
- [ ] NÃO — novo timeline: [1.5 weeks / 2 weeks / outro]

**Ação:**
- [ ] SPRINT_PLANNING.md dias ajustados (se necessário)
- [ ] R1_PLAN_REVISED.md velocity table atualizada
- [ ] Comunicado ao CEO/stakeholders

---

### Decisão 4: Prioridade Técnica (Harness vs ProjectAdapter)

**Se Dia 2 força choice (não pode continuar dupla):**

**Opção A:** Harness prioritário
- Justificativa: [Agent/capability harness é foundation pra REST do APOS]
- Impact: ProjectAdapter para (resume Sprint 1.1 ou R2)
- Risk: ProjectAdapter não existe; Meu PDI discovery ainda manual

**Opção B:** ProjectAdapter prioritário
- Justificativa: [Meu PDI descoberta automática é game-changer; Harness pode esperar]
- Impact: Harness coverage fica 50-60% (aceitável? Não-blocking?)
- Risk: Observabilidade system (harness) incompleto

**Opção C:** Híbrido/Serializado
- Justificativa: [Terça (Dia 3): qual ordem?]
- Impact: [Timeline ajusta; ambos completam mas sequencial]
- Risk: [Context switching overhead]

**Recomendação:** [A / B / C baseado em feedback]

**Ação:**
- [ ] CEO aprova / confirma prioridade
- [ ] Contingency plan anexado a SPRINT_PLANNING.md

---

## 📈 Métrica de Sucesso da Síntese

**Como saber se síntese foi bem-feita:**

- [ ] Hypotheses 1-3 têm resposta clara (SIM/NÃO/DEPENDE)
- [ ] Decisão 1-4 têm justificativa baseada em feedback (não arbitrary)
- [ ] Riscos > 3 identificados (senão foi superficial)
- [ ] Próximos passos acionáveis (não vago)
- [ ] Team consegue ler síntese em 10 min (conciso)

---

## 📋 Próximos Passos (Action Items)

**Imediatamente (15:00-15:30):**
- [ ] Síntese consolidada e shared com Jader
- [ ] Decisões 1-4 documentadas acima
- [ ] Riscos priorizados

**Antes Standup Dia 2 (09:00 Dia 2):**
- [ ] SPRINT_PLANNING.md atualizado (se mudanças de escopo/timing)
- [ ] BOARD.md atualizado (tarefas reorganizadas conforme decisões)
- [ ] Team sincronizado (Slack thread com síntese)

**Dia 2 16:00 (Milestone Decision):**
- [ ] Standup valida progress vs criteria
- [ ] Decision criteria from síntese aplicada
- [ ] Convergência plan acionado (se necessário)

---

## 📚 Attachments

**Entrevistas brutas:**
- Entrevista 1 template: [STAKEHOLDER_INTERVIEWS.md#Entrevista1]
- Entrevista 2 template: [STAKEHOLDER_INTERVIEWS.md#Entrevista2]
- Entrevista 3 template: [STAKEHOLDER_INTERVIEWS.md#Entrevista3]

**Documentação relacionada:**
- [SPRINT_PLANNING.md](SPRINT_PLANNING.md) — Sprint plan original
- [R1_PLANNING_GUIDE.md](../R1_PLANNING_GUIDE.md) — Context de R1
- [BOARD.md](BOARD.md) — Kanban board

---

**Síntese criada:** 2026-07-21  
**Preenchimento esperado:** Depois das 3 entrevistas (15:00-15:30)  
**Público:** Team APOS + Jader + Stakeholders  
**Confidência:** Public (parte de artefatos de sprint)

