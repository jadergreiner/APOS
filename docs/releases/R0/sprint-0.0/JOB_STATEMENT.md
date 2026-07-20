# T0.0.C — Job Statement Final

**Tarefa:** Finalizar Job Statement APOS
**Base:** 7 entrevistas JTBD (T0.0.A) + Análise de Forças (T0.0.B)
**Data:** 2026-07-19
**Status:** ✅ COMPLETO (Aprovado por Jader Greiner)

---

## 1. Job Statement

> **When** [dependo de agentes de IA (ou times) para implementar sem visibilidade do contexto que eles usam],
> **I want** [um sistema que me mostre o nível de confiança de cada informação *antes* de agirem],
> **so I can** [delegar com segurança e eliminar o ciclo de retrabalho por contexto desatualizado].

### Em Inglês

> **When** [I depend on AI agents (or teams) to implement without visibility into the context they use],
> **I want** [a system that shows me the confidence level of each piece of information *before* they act],
> **so I can** [delegate with confidence and eliminate the rework cycle caused by outdated context].

---

## 2. Três Dimensões do Job

| Dimensão | Agora (Current State) | Desejado (Desired State) |
|----------|----------------------|------------------------|
| **Funcional** | Validação manual pós-fato → descobre erro no deploy, no PR, ou no relatório | Validação prévia com semáforo de confiança (0.0-1.0) no fluxo de trabalho |
| **Emocional** | Desprotegido, desconforto constante, ansiedade quieta — "torcendo pra não estar errado" | Confiança para delegar, não apenas supervisionar — "dormir sabendo que tá certo" |
| **Social** | "Rápido mas quebra" / "quase confiável" / "precisa supervisão constante" | "Rápido SEM quebrar" — credibilidade para delegar sem stigma |

---

## 3. Forças de Progresso

### Push (Por que mudar)

| # | Força | Evidência (entrevistas) | Intensidade |
|---|-------|------------------------|-------------|
| P1 | Contexto desatualizado SEM mecanismo de alerta — descobre erro depois | 5/7 relataram | 🔴 Crítico |
| P3 | Retrabalho cíclico — mesmo erro volta apesar de checklist | 4/7 | 🔴 Crítico |
| P6 | Contexto manual não escala — CONTEXT.md vira ruído em dias | 3/7 | 🟡 Alto |
| P8 | Não sabe o que a IA "viu" — contexto invisível por design | 2/7 | 🟡 Alto |

### Pull (Para onde ir)

| # | Força | Evidência (entrevistas) | Intensidade |
|---|-------|------------------------|-------------|
| L1 | Confiança granular (0.0-1.0) — métrica, não atributo binário | **7/7** | 🔴 Definição |
| L3 | Semáforo pré-ação — validar antes, não depois | 4/7 | 🔴 Essencial |
| L4 | Transparência de contexto por sugestão — confiança junto com o código | 1/7 (profundo) | 🟡 Diferencial |

### Ansiedade (Por que não mudar)

| # | Força | Evidência (entrevistas) | Intensidade |
|---|-------|------------------------|-------------|
| A1 | Falso positivo de confiança > ausência de contexto | **6/7** | 🔴 REQUISITO ARQUITETURAL #1 |
| A2 | Quem alimenta? Curadoria manual não resolve | 3/7 | 🔴 Condicionante |
| A5 | Perturbar fluxo com alerta excessivo | 2/7 | 🟡 UX crítico |

### Hábito (O que mantém)

| # | Força | Evidência (entrevistas) |
|---|-------|------------------------|
| H1 | Revisão desconfiada — cada linha como potencial erro | 3/7 |
| H2 | Prompts defensivos — construídos em meses, funcionam | 2/7 |
| H5 | Copia e cola manual de contexto — previsível | 1/7 |

---

## 4. Seis Requisitos de Produto

| # | Requisito | Derivação | Critério de Sucesso |
|---|-----------|-----------|-------------------|
| R1 | **Confiança granular (0.0-1.0 por campo/informação)** | L1 (7/7) | Usuário vê score de confiança por item de contexto |
| R2 | **Falso positivo arquiteturalmente inaceitável** | A1 (6/7) | Precisão > recall; viés para "não sei" sobre "sei errado" |
| R3 | **Auto-atualização via eventos** | A2, P6 | Sem curadoria manual; contexto atualiza com fluxo natural |
| R4 | **Contexto no fluxo de trabalho** | L7, A5 | Integrado na IDE/terminal/PR; zero apps separados |
| R5 | **Auto-descoberta de contexto** | P7, L8 | Usuário não precisa saber o que buscar — sistema infere |
| R6 | **Custo do desalinhamento visível em $** | P5, L6 | Métrica de negócio (rework ratio, time-to-impact) |

---

## 5. Validação

### Personas que validaram o Job Statement

| # | Persona | Job Validado | Data |
|---|---------|-------------|------|
| 1 | PM (Jader Greiner) | ✅ "Saber antes de implementar o contexto da IA" | 19 jul |
| 2 | AI Operator (Alex) | ✅ "Contexto confiável antes do agente agir" | 19 jul |
| 3 | CTO (Carolina) | ✅ "Confiança calibrada — falso positivo > ausência" | 19 jul |
| 4 | Stakeholder Negócios (Ricardo) | ✅ "Custo do desalinhamento precisa ser visível em $" | 19 jul |
| 5 | Early Adopter (Daniela) | ✅ "Semáforo dentro do meu fluxo, não em dashboard" | 19 jul |
| 6 | Eng. Dados Jr (Lucas) | ✅ "Contexto que não sabe que não sabe" | 19 jul |
| 7 | Dev Pleno IA User (Felipe) | ✅ "Transparência de contexto por sugestão" | 19 jul |

---

## 6. Assinatura

| Stakeholder | Papel | Data | Assinatura |
|-------------|-------|------|------------|
| Jader Greiner | Product Owner / Principal Stakeholder | 2026-07-19 | ✅ Aprovado |

---

**Criado:** 2026-07-19
**Baseado em:** FORCES_ANALYSIS.md, JTBD-INTERVIEWS-RAW-NOTES.md
**Relacionado:** [VALUE_PROPOSITION.md](../../VALUE_PROPOSITION.md)
