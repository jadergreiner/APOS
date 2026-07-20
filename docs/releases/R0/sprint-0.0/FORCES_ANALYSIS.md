# T0.0.B — Análise de Forças: JTBD Discovery

**Tarefa:** Análise de Forças (Push/Pull/Ansiedade/Hábito)
**Base:** 7 entrevistas JTBD realizadas em T0.0.A
**Data:** 2026-07-19
**Status:** ✅ COMPLETO

---

## 1. Matriz de Forças Consolidada

### Push (Forças que Empurram para a Mudança)

| # | Push | Entrevistas | Frequência |
|---|------|-------------|------------|
| P1 | Contexto desatualizado sem mecanismo de alerta — descobre erro só depois do deploy | 1, 2, 3, 5, 7 | 5/7 |
| P2 | Nenhum mecanismo conecta Task→Feature→Release→OKR→Métrica | 1, 4 | 2/7 |
| P3 | Retrabalho cíclico — mesmo erro volta apesar de checklist/instruções | 1, 2, 5, 7 | 4/7 |
| P4 | Assimetria de informação — decisão tomada por poucos impacta muitos que não estavam na sala | 3, 4, 6 | 3/7 |
| P5 | Custo do desalinhamento invisível — 30-40% do esforço de engenharia desperdiçado sem métrica | 1, 4 | 2/7 |
| P6 | Manutenção manual de contexto (CONTEXT.md, wiki) não escala — vira ruído em dias | 2, 3, 5 | 3/7 |
| P7 | Ontologia invisível — conhecimento existe (na cabeça do sênior, em reunião) mas não chega a quem executa | 6 | 1/7 |
| P8 | Não sabe o que a IA 'viu' pra gerar código — contexto invisível por design | 5, 7 | 2/7 |

**Push dominante (P1):** Contexto desatualizado sem mecanismo de alerta. Unânime entre operadores de IA e devs.

### Pull (Forças que Atraem para a Nova Solução)

| # | Pull | Entrevistas | Frequência |
|---|------|-------------|------------|
| L1 | Confiança como métrica (0.0-1.0 por campo), não atributo binário | 1, 2, 3, 4, 5, 6, 7 | **7/7** |
| L2 | Rastreabilidade — saber qual contexto o agente/usuário usou pra decidir | 1, 2, 3, 4 | 4/7 |
| L3 | Semáforo pré-ação — validar contexto *antes* de implementar, não depois | 1, 2, 5, 6 | 4/7 |
| L4 | Transparência de contexto por sugestão — nível de confiança junto com o código gerado | 7 | 1/7 |
| L5 | Escalabilidade do contexto do líder — deixar de ser gargalo | 3, 4 | 2/7 |
| L6 | Previsibilidade de impacto — saber se a feature vai gerar resultado antes de implementar | 4 | 1/7 |
| L7 | Contexto no fluxo (IDE, terminal, PR) — não dashboard separado | 5, 6 | 2/7 |
| L8 | Auto-descoberta — não depender do usuário saber o que buscar | 6 | 1/7 |

**Pull dominante (L1):** Confiança como métrica granular. **Unânime.** Todas as 7 personas querem um número que diga o quanto confiar em cada informação.

### Ansiedade (Forças que Travam a Mudança)

| # | Ansiedade | Entrevistas | Frequência |
|---|-----------|-------------|------------|
| A1 | **Falso positivo de confiança > ausência de contexto** — se o sistema disser verde e tiver errado, o dano é pior que não ter sistema | 2, 3, 4, 5, 6, 7 | **6/7** |
| A2 | "Quem alimenta?" — se precisar de curadoria manual, não resolve o problema original | 2, 3, 4 | 3/7 |
| A3 | Lock-in — se for proprietário, vira refém | 2, 3 | 2/7 |
| A4 | Curva de aprendizado + mudança de processo | 1, 4 | 2/7 |
| A5 | Perturbar fluxo com alerta excessivo — falso alarme leva a desligar | 5, 7 | 2/7 |
| A6 | Precisão das métricas — "prefiro não sei a 'sei errado'" | 4 | 1/7 |

**Ansiedade dominante (A1):** Falso positivo de confiança. **Unânime entre todos que já usam ferramentas de IA.** É o maior risco percebido e o requisito não-negociável.

### Hábito (Forças que Mantêm o Status Quo)

| # | Hábito | Entrevistas | Frequência |
|---|--------|-------------|------------|
| H1 | Revisão desconfiada — revisar cada linha de IA como se pudesse estar errada | 1, 5, 7 | 3/7 |
| H2 | Prompts defensivos — construídos ao longo de meses, funcionam na prática | 2, 7 | 2/7 |
| H3 | Reuniões de alinhamento como muleta — ineficientes mas dão sensação de controle | 3, 4 | 2/7 |
| H4 | Perguntar pro sênior — ineficiente mas seguro e previsível | 6 | 1/7 |
| H5 | Copia e cola manual de contexto no prompt — trabalhoso mas sabe-se exatamente o que foi passado | 7 | 1/7 |
| H6 | Ciclo "especifica → gera → valida manualmente" | 1 | 1/7 |

**Hábito dominante (H1):** Revisão desconfiada. Mesmo com ferramentas de IA, o instinto de validar manualmente persiste.

---

## 2. Diagrama de Forças

```
PUSH (por que mudar)                     PULL (para onde ir)
─────────────────────                    ────────────────────
P1  Contexto desatualizado    ████████   L1  Confiança granular     ████████████████
P3  Retrabalho cíclico       ██████      L2  Rastreabilidade        ████████
P6  Manutenção manual        ██████      L3  Semáforo pré-ação      ████████
P4  Assimetria informação    ██████      L5  Escalar contexto       ████
P8  Contexto IA invisível    ████        L7  Contexto no fluxo      ████
                                         L8  Auto-descoberta        ██

ANSIEDADE (por que não mudar)            HÁBITO (por que continua)
────────────────────────────             ──────────────────────
A1  Falso positivo > ausência ██████████████  H1  Revisão desconfiada   ██████
A2  Quem alimenta?           ██████           H2  Prompts defensivos    ████
A5  Perturbar fluxo          ████            H3  Reuniões              ████
                                             H5  Copia e cola manual   ██
```

### Equação de Mudança

```
P1 + P3 + P6 + P8  >  A1 + H1 + H2
(ALTA)                (MUITO ALTA)
```

**Interpretação:** A pressão para mudar (Push+Pull) é alta, mas a Ansiedade (A1 — falso positivo) e o Hábito (H1 — revisão desconfiada) formam barreiras significativas. A adoção só acontecerá se o sistema **provar que falso positivo é extremamente raro** (A1) e **oferecer transparência que substitua a revisão manual** (combater H1 com L4).

---

## 3. Job Statement Final (T0.0.C)

Validado por 7/7 personas:

> **When** [dependo de agentes de IA (ou times) para implementar sem visibilidade do contexto que eles usam],
> **I want** [um sistema que me mostre o nível de confiança de cada informação *antes* de agirem],
> **so I can** [delegar com segurança e eliminar o ciclo de retrabalho por contexto desatualizado].

### Job em 3 Dimensões

| Dimensão | Agora | Desejado |
|----------|-------|----------|
| **Funcional** | Validação manual pós-fato → descobre erro no deploy | Validação prévia com semáforo de confiança (0.0-1.0) |
| **Emocional** | Desprotegido, desconforto constante, ansiedade quieta | Confiança para delegar, não apenas supervisionar |
| **Social** | "Rápido mas quebra" / "quase confiável" | "Rápido SEM quebrar" — credibilidade para delegar |

---

## 4. Seis Requisitos de Produto (Emergentes)

| # | Requisito | Fonte (Força) | Impacto |
|---|-----------|---------------|---------|
| R1 | **Confiança granular (0.0-1.0 por campo/informação)** — não binário | L1 (Pull) | Diferencial competitivo — ninguém oferece |
| R2 | **Falso positivo é inaceitável** — precisão > recall | A1 (Ansiedade) | Requisito arquitetural nº1 — unânime |
| R3 | **Auto-atualização via eventos** — sem curadoria manual | A2, P6 (Ansiedade+Push) | Define escalabilidade |
| R4 | **Contexto no fluxo** (IDE, terminal, PR) — não dashboard separado | L7, A5 (Pull+Ansiedade) | Define adoção |
| R5 | **Auto-descoberta** — não depende do usuário saber o que buscar | P7, L8 (Push+Pull) | Define usabilidade para juniores |
| R6 | **Custo do desalinhamento visível em $** — métrica de negócio | P5, L6 (Push+Pull) | Define valor para stakeholders |

---

## 5. Segmentação de Mercado (por Perfil)

| Segmento | Prioridade | Job Principal | Barreira de Adoção |
|----------|-----------|---------------|-------------------|
| **PM / AI Operator** (perfis 1, 2) | 🔴 Alto | Validar contexto antes do agente agir | Curva de aprendizado |
| **CTO / Arquiteto** (perfil 3) | 🔴 Alto | Escalar contexto do líder; auditabilidade | Falso positivo |
| **Stakeholder Negócios** (perfil 4) | 🟡 Médio | Previsibilidade de impacto; custo visível | Precisa ver ROI em $ |
| **Devs que usam IA** (perfis 5, 7) | 🟡 Médio | Transparência de contexto por sugestão | Perturbar fluxo |
| **Júnior/Sem experiência** (perfil 6) | 🟢 Baixo | Contexto que se descobre sozinho | Não sabe que precisa |

---

## 6. Risco vs. Oportunidade

### Risco Crítico
**Falso positivo de confiança.** Se o sistema disser que o contexto é confiável quando não é, a credibilidade é perdida para sempre (especialmente em contextos financeiros — perfil 7). Este risco define a arquitetura: **precisão > recall** para o MVP.

### Oportunidade Principal
**Ninguém oferece confiança granular como métrica hoje.** RAG puro, MCP tools, metadata catalogs — nenhum resolve "quanto confiar nesta informação antes de agir". APOS ocupa um espaço em branco.

---

## 7. Próximos Passos

- [x] **T0.0.A**: 7/5 entrevistas realizadas ✅
- [x] **T0.0.B**: Análise de Forças completa ✅
- [ ] **T0.0.C**: Job Statement Final validado com stakeholders reais
- [ ] **Atualizar VALUE_PROPOSITION.md** com insights refinados
- [ ] **Apresentar findings** para o board/stakeholder APOS

---

**Criado:** 2026-07-19
**Baseado em:** T0.0.A (7 entrevistas JTBD)
**Relacionado:** [JTBD-INTERVIEWS-RAW-NOTES.md](JTBD-INTERVIEWS-RAW-NOTES.md) | [JTBD_INTERVIEW_KIT.md](JTBD_INTERVIEW_KIT.md) | [TASKS.md](TASKS.md)
