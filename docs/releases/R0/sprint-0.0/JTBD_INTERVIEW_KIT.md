# Kit de Entrevista JTBD — Sprint 0.0

**Tarefa:** T0.0.A — Conduzir Entrevistas JTBD
**Objetivo:** Entender o job real que APOS resolve, através de 5+ entrevistas estruturadas com personas-alvo
**Duração por entrevista:** 60-90 min
**Deadline de agendamento:** 21 jul | **Execução:** 23-24 jul

---

## 1. Personas a Entrevistar

| # | Persona | Foco da Entrevista | Status |
| --- | --- | --- | --- |
| 1 | Product Manager (líder de time) | Overhead de alinhamento estratégico | 📋 A agendar |
| 2 | Agente de IA (conceitual — via seu operador/integrador) | Necessidades de contexto para evitar alucinação | 📋 A agendar |
| 3 | CTO / Arquiteto | Viabilidade técnica, custo de integração | 📋 A agendar |
| 4 | Stakeholder (negócios) | ROI, valor percebido | 📋 A agendar |
| 5 | Early Adopter (time early-stage) | Adoção, fricção de onboarding | 📋 A agendar |

---

## 2. Termo de Consentimento (ler no início da chamada)

> "Obrigado por participar. Esta conversa faz parte da fase de Descoberta do APOS, um framework de camada semântica para agentes de IA. Vou gravar esta chamada apenas para uso interno de análise — a gravação não será compartilhada publicamente e você pode pedir para pausar a gravação a qualquer momento. Não há respostas certas ou erradas; queremos entender sua realidade atual. Tudo bem para você?"

**Checklist antes de começar:**

- [ ] Consentimento verbal obtido e registrado
- [ ] Gravação iniciada (Zoom/Teams)
- [ ] Nome, papel e empresa/contexto do entrevistado anotados

---

## 3. Estrutura Geral da Entrevista (60-90 min)

| Bloco | Duração | Objetivo |
| --- | --- | --- |
| 1. Abertura + Consentimento | 5 min | Contexto, consentimento, rapport |
| 2. Aquecimento (contexto atual) | 10 min | Entender o dia a dia, sem mencionar APOS |
| 3. Perguntas JTBD (comuns) | 20 min | Extrair o job funcional/emocional/social |
| 4. Forças de Progresso (Push/Pull/Ansiedade/Hábito) | 20 min | Mapear o que empurra e o que trava a mudança |
| 5. Perguntas específicas da persona | 15-25 min | Aprofundar ângulo único da persona |
| 6. Encerramento | 5 min | Agradecer, próximos passos, follow-up |

---

## 4. Perguntas Comuns (todas as personas)

### Aquecimento

1. Me conta um pouco sobre seu papel hoje e como é uma semana típica de trabalho.
2. Quando você precisa tomar uma decisão que depende de contexto de produto/estratégia (ex: "essa feature está alinhada com o OKR?"), como você faz isso hoje?
3. Quais ferramentas ou documentos você consulta para isso?

### Job to be Done (funcional / emocional / social)

4. Me conta sobre a última vez que você (ou seu time) perdeu tempo ou retrabalhou algo por falta de contexto claro — o que aconteceu?
5. Se essa informação estivesse sempre correta e acessível, o que mudaria no seu dia a dia?
6. Como você se sente quando precisa confiar em uma resposta de IA (ou de outra pessoa) sem conseguir validar se está certa?
7. Como você quer ser visto pelo seu time quando toma uma decisão baseada em dados/contexto? (ex: como alguém confiável, rigoroso, rápido?)

### Push / Pull / Ansiedade / Hábito

8. **Push:** O que hoje te frustra mais nesse processo de manter contexto/alinhamento atualizado?
9. **Pull:** Se existisse uma "fonte única de verdade" viva e conectada a agentes de IA, o que te atrairia mais nela?
10. **Ansiedade:** O que te preocuparia em adotar algo assim? (confiabilidade, curva de aprendizado, mudança de processo, custo)
11. **Hábito:** O que você faz hoje que seria difícil de abandonar, mesmo sabendo que existe algo melhor?

### Encerramento

12. Se pudesse resolver **um** problema relacionado a isso amanhã, qual seria?
13. Há mais alguém que você recomendaria eu conversar sobre esse tema?

---

## 5. Perguntas Específicas por Persona

### 5.1 Product Manager (líder de time)

- Como você garante hoje que todo o time entende o "porquê" por trás de uma feature (não só o "o quê")?
- Quantas vezes por sprint você precisa re-explicar contexto estratégico que já deveria estar documentado?
- Como fica o rastreamento entre Task → Feature → Release → OKR → Métrica hoje? É manual?

### 5.2 Agente de IA (via operador/integrador)

- Quando um agente de IA que você opera "alucina" ou dá uma resposta desalinhada com a estratégia, qual costuma ser a causa raiz?
- Que tipo de contexto estruturado (não só texto solto) ajudaria o agente a tomar decisões mais alinhadas?
- Como você mede hoje a "confiança" de um contexto fornecido a um agente?

### 5.3 CTO / Arquiteto

- Quais riscos técnicos você vê em manter uma camada semântica/ontológica viva conectada a múltiplos sistemas?
- Como isso se compararia, na sua visão, com abordagens que você já usa (ex: RAG puro, grafos de conhecimento, metadata catalogs)?
- O que precisaria ser verdade tecnicamente para você aprovar a adoção disso na arquitetura?

### 5.4 Stakeholder (negócios)

- Como você mede hoje o custo de desalinhamento entre estratégia e execução (retrabalho, atraso, decisões erradas)?
- O que faria você confiar no ROI de uma ferramenta assim antes de ver resultado?
- Que métrica de negócio mudaria se esse problema fosse resolvido?

### 5.5 Early Adopter (time early-stage)

- O que faria você experimentar uma ferramenta nova como essa amanhã, mesmo em fase beta?
- Qual seria o critério para você abandonar no meio do caminho?
- O que precisaria estar pronto no "dia 1" para você não desistir na primeira semana?

---

## 6. Pós-Entrevista (checklist)

- [ ] Transcrever/anotar insights brutos em até 24h (memória fresca)
- [ ] Marcar trechos-chave de Push / Pull / Ansiedade / Hábito
- [ ] Salvar em `JTBD-INTERVIEWS-RAW-NOTES.md` (entregável de T0.0.A)
- [ ] Identificar 1-2 citações fortes por entrevista (para uso posterior no Job Statement)

---

**Criado:** 2026-07-19
**Relacionado:** [TASKS.md](TASKS.md) (T0.0.A) | [BOARD.md](BOARD.md)
**Próximo entregável:** `JTBD-INTERVIEWS-RAW-NOTES.md` após as entrevistas (23-24 jul)
