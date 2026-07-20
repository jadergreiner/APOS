# APOS — Job Statement

**Sprint:** 0.2 - JTBD Deep Dive
**Framework:** Jobs to Be Done
**Data:** 2026-07-20
**Status:** ✅ DEFINIDO (5/5 entrevistas validadas)

---

## Job Statement

```
When    minha equipe esta planejando ou executando um sprint,
        e o contexto estrategico das tarefas esta espalhado,
        desatualizado ou simplesmente invisivel,

I want  uma camada semantica que conecte automaticamente
        tasks → features → OKRs → metricas de impacto,
        com pontuacao de confianca sobre a qualidade do contexto,

So that eu possa priorizar com base em dados, eliminar retrabalho
        de contexto, e garantir que o time esta construindo
        o que realmente importa — sem depender de documentacao
        manual que morre no dia seguinte.
```

---

## Situacao Trigger

### Quando o Job Surge

| Situacao | Frequencia | Personas |
|----------|-----------|----------|
| Planejamento de sprint (20+ tasks no backlog) | Semanal | PM Leader, EM |
| Mudanca de prioridade no meio do sprint | 2-3x/sprint | PM Leader, EM |
| Novo membro entra no time e precisa de contexto | A cada onboarding | PM Leader, EM |
| Revisao de OKR (fim do mes/trimestre) | Mensal/Trimestral | Product Ops, PM Leader |
| Incidente de alucinacao de agente por contexto falho | Diario/Semanal | AI Architect |
| Pergunta do VP/C-level "esse numero ta certo?" | Mensal | Product Ops |
| Descoberta de que 2 squads resolveram o mesmo problema | A cada 2-3 sprints | EM, Early Adopter |

### Quem Sente o Job

- **Primario:** PM Leaders, Engineering Managers, Product Ops
- **Secundario:** AI/ML Engineers, PMs individuais
- **Impactado:** Todo o time de produto e engenharia

### Onde Ocorre

- Jira / Linear / GitHub Projects (rastreamento de trabalho)
- Slack / reunioes (comunicacao de contexto)
- Notion / Confluence (documentacao de decisoes)
- Planilhas (consolidacao manual de OKRs)
- Pipelines de IA (context injection para agentes)

---

## O Job Que APOS Resolve

### Job Funcional

Conectar o "o que" (tasks) ao "por que" (OKRs) automaticamente, sem depender de preenchimento manual ou documentacao que desatualiza.

### Job Emocional

Dar confianca de que o time esta construindo o que realmente importa — eliminar a ansiedade de "sera que isso ainda e prioridade?" e a frustracao de "por que ninguem me contou que mudou?".

### Job Social

Permitir que PMs e EMs respondam ao leadership com dados concretos ("sim, essa feature moveu a metrica X em Y%") em vez de "acho que sim, com ressalvas".

---

## Job Map (Etapas Que o Consumidor Tenta Fazer)

```
1. DEFINIR PRIORIDADES
   ├── 1.1 Entender contexto estrategico atual
   ├── 1.2 Identificar quais tasks mapeiam para quais OKRs
   ├── 1.3 Detectar "orphaned features" (sem OKR)
   └── 1.4 Decidir o que entra no sprint

2. EXECUTAR COM ALINHAMENTO
   ├── 2.1 Comunicar "por que" para o time
   ├── 2.2 Manter contexto atualizado durante execucao
   ├── 2.3 Detectar mudancas de prioridade em tempo real
   └── 2.4 Evitar scope creep sem justificativa

3. MEDIR E REPORTAR
   ├── 3.1 Consolidar tasks entregues vs OKRs
   ├── 3.2 Calcular impacto nas metricas de produto
   ├── 3.3 Preparar report para leadership
   └── 3.4 Responder "essa feature moveu qual numero?"

4. APRENDER E ITERAR
   ├── 4.1 Revisar o que foi entregue vs o que foi planejado
   ├── 4.2 Identificar padroes de desperdicio
   ├── 4.3 Alinhar proximo ciclo com licoes aprendidas
   └── 4.4 Manter rastro de decisoes para futuro
```

---

## Criterios de Sucesso (Como o Consumidor Mede)

### Funcionais

| # | Criterio | Metrica | Validado Por |
|---|----------|---------|-------------|
| 1 | Reducao no tempo de reexplicacao de contexto | -80% (de 2-3h → <30 min/semana) | PM Leader, EM |
| 2 | Aumento de features vinculadas a OKR | de 40% → 95%+ | Product Ops, Early Adopter |
| 3 | Eliminacao de roll-up manual de OKR | 0 horas/mes | Product Ops |
| 4 | Setup da ferramenta | <30 minutos | Early Adopter |
| 5 | Acuracia do trust score | <5% falso positivo | AI Architect |
| 6 | Latencia de consulta de contexto | <500ms | AI Architect |

### Emocionais

| # | Criterio | Evidencia |
|---|----------|-----------|
| 1 | Confianca em priorizacao | Score de 5/10 → 8/10 |
| 2 | Credibilidade em reports | VP/C-level para de questionar os numeros |
| 3 | Ansiedade reduzida | Devs nao precisam mais "caçar contexto" |

### De Adocao

| # | Criterio | Target |
|---|----------|--------|
| 1 | Interesse em piloto | 4/5 entrevistados sim ou condicional |
| 2 | Plugin Jira instalado | Setup em 5 min, valor em 30 min |
| 3 | Retencao no primeiro mes | 80%+ ainda usando apos 30 dias |

---

## Job Statement Alternativo (1 Frase)

**Para times de produto que lutam com contexto estrategico desatualizado e retrabalho, APOS e uma camada semantica que conecta automaticamente tasks a OKRs com pontuacao de confianca — ao contrario de documentacao manual ou dashboards que ninguem atualiza.**

---

## Validacao com Stakeholders

| Stakeholder | Job Ressoa? | Feedback |
|------------|------------|----------|
| PM Leader | ✅ Sim | "Descreveu exatamente meu dia" |
| EM / Tech Lead | ✅ Sim | "30-40% do retrabalho e isso" |
| AI Architect | ✅ Sim | "Trust score e o que faltava" |
| Product Ops | ✅ Sim | "80h/mes dizendo 'com ressalvas'" |
| Early Adopter | ✅ Sim | "15-20% desperdicio por falta de visibilidade" |

**Conclusao:** 5/5 validaram — job real, bem compreendido, com urgencia crescente.

---

## Referencias

- [JTBD_INTERVIEWS_TEMPLATE.md](JTBD_INTERVIEWS_TEMPLATE.md) — 5 entrevistas documentadas
- [FORCES_ANALYSIS.md](FORCES_ANALYSIS.md) — Push/Pull/Habit/Anxiety por persona
- [VALUE_PROPOSITION.md](../../../../VALUE_PROPOSITION.md) — Proposta de valor do APOS
- [STAKEHOLDER_INTERVIEWS_PLAN.md](STAKEHOLDER_INTERVIEWS_PLAN.md) — Plano de entrevistas original

---

**Data:** 2026-07-20
**Status:** ✅ DEFINIDO E VALIDADO
**Proximo:** Sprint 0.3 — Beta Prep
