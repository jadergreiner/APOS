# JTBD Interviews — Raw Notes

**Tarefa:** T0.0.A — Conduzir Entrevistas JTBD
**Roteiro usado:** [JTBD_INTERVIEW_KIT.md](JTBD_INTERVIEW_KIT.md)
**Meta:** 5+ entrevistas | **Realizadas até agora:** 1/5

---

## Entrevista 1 — Product Manager

**Entrevistado:** Jader Greiner
**Papel/Contexto:** PM do Meu PDI — gerencia squad virtual (define especificações via IA, agentes virtuais implementam)
**Persona:** Product Manager (líder de time)
**Data:** 2026-07-19
**Formato:** Conduzida via texto (Claude Code), consentimento verbal confirmado

### Aquecimento

**Q1. Papel e semana típica:**
> "Sou PM de uma squad virtual. Defino as especificações usando IA e agentes virtuais implementam."

**Q2. Como decide se uma feature está alinhada ao OKR hoje:**
> "Puro Feeling"

**Q3. Ferramentas/documentos consultados:**
> "nenhum"

### Job to be Done

**Q4. Última vez que perdeu tempo/retrabalhou por falta de contexto:**
> "Cada deploy na AWS erro no login. Retrabalho, instruções aos agentes, checklist. Mas dali um tempo, o mesmo erro se repete."

**Q5. O que mudaria se a informação estivesse sempre correta e acessível:**
> "Estas regressões não ocorreriam"

**Q6. Como se sente confiando em resposta de IA sem conseguir validar:**
> "Me sinto desprotegido. Com medo de seguir adiante, às vezes acho que o tempo que ganhei com IA estou perdendo validando e testando."

**Q7. Como quer ser visto ao tomar decisão baseada em contexto:**
> "Rápido, confiável, consistente"

### Forças de Progresso

**Q8. Push — maior frustração em manter contexto/alinhamento atualizado:**
> "Tento usar múltiplas IAs para gerar prompts que minimizem falhas"

**Q9. Pull — o que mais atrairia numa fonte única de verdade viva:**
> "Validar contexto. Rastrear claramente a decisão e rota que o agente utilizou na implementação"

**Q10. Ansiedade — preocupações na adoção:**
> "Curva de aprendizado e mudança de processo"

**Q11. Hábito — o que seria difícil abandonar:**
> "Ler as especificações, gerar passo a passo, validar"

### Encerramento

**Q12. Um problema para resolver amanhã:**
> "Saber antes de implementar exatamente o contexto da IA"

**Q13. Indicação de outra pessoa:**
> "não"

### Perguntas Específicas — Product Manager

**PM1. Como garante que o time/agentes entendem o "porquê" de uma feature:**
> "Não garanto. É uma dor recorrente"

**PM2. Frequência de re-explicar contexto estratégico por sprint:**
> "quase que diariamente"

**PM3. Rastreamento Task → Feature → Release → OKR → Métrica hoje:**
> "Inexistente"

---

## Síntese de Sinais — Entrevista 1

| Força | Sinal Extraído |
| --- | --- |
| **Push** | Zero ferramenta de apoio à decisão ("puro feeling"); orquestra múltiplas IAs manualmente para blindar prompts; regressões cíclicas (mesmo erro de deploy/login volta apesar de checklist/instruções) |
| **Pull** | Validar contexto antes de implementar; rastrear claramente decisão e rota usada pelo agente |
| **Ansiedade** | Curva de aprendizado; mudança de processo |
| **Hábito** | Ler especificação → gerar passo a passo → validar manualmente (loop que resiste à mudança) |
| **Emocional** | Sensação de desproteção; medo de avançar; suspeita de que o ganho de produtividade da IA é consumido pela validação/teste |
| **Social** | Quer ser percebido como rápido, confiável, consistente |

**Dores estruturais (não pontuais) identificadas:**

1. Nenhum mecanismo garante que o "porquê" estratégico chegue aos agentes/time — dor recorrente, não incidente isolado
2. Rastreamento Task→Feature→Release→OKR→Métrica é **inexistente**
3. Contexto estratégico precisa ser re-explicado quase diariamente
4. Regressões cíclicas mesmo com checklist/instruções — indica falta de contexto *persistente* (não é problema de documentação pontual, é falta de memória viva)

**Citações fortes para o Job Statement:**

> "Me sinto desprotegido... acho que o tempo que ganhei com IA estou perdendo validando e testando."

> "Saber antes de implementar exatamente o contexto da IA."

**Rascunho de Job Statement (a validar em T0.0.C):**

> "When [PM define especificações para agentes de IA implementarem sem visibilidade prévia do contexto que o agente vai usar], I want [validar e rastrear o contexto/decisão do agente antes e durante a implementação], so I can [evitar regressões cíclicas e parar de perder em validação o tempo que ganhei com IA]."

---

## Próximas Entrevistas (4 restantes)

| # | Persona | Status |
| --- | --- | --- |
| 2 | Agente de IA (via operador/integrador) | 📋 A agendar |
| 3 | CTO / Arquiteto | 📋 A agendar |
| 4 | Stakeholder (negócios) | 📋 A agendar |
| 5 | Early Adopter | 📋 A agendar |

---

**Criado:** 2026-07-19
**Relacionado:** [JTBD_INTERVIEW_KIT.md](JTBD_INTERVIEW_KIT.md) | [TASKS.md](TASKS.md) (T0.0.A) | [BOARD.md](BOARD.md)
