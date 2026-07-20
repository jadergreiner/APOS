# APOS R0 Dependency Map

**Release:** R0 (APOS Foundations)  
**Mapa de Dependências:** Entre sprints, tarefas e stakeholders  
**Status:** PLANNED

---

## Dependências entre Sprints

```
Sprint 0.0 (JTBD Discovery)
    ├─ Output: Job statement validado
    └─ Bloqueador: Sem job validado, value prop fica fraca
        ↓
Sprint 0.1 (Value Prop + Positioning)
    ├─ Input: Job statement do 0.0
    ├─ Output: Value prop testado, positioning claro
    └─ Bloqueador: Sem value prop, ontologia não tem direção
        ↓
Sprint 0.2 (Purpose + Ontologies) ← CAN START IN PARALLEL
    ├─ Input: Job statement (para informar design de conceitos)
    ├─ Output: Ontologia formal, semantic layer
    └─ Bloqueador: Sem ontologia, não há foundation
        ↓
Sprint 0.3 (North Star + OKRs + Roadmap)
    ├─ Input: Tudo de 0.0-0.2 (job, value prop, ontologia)
    ├─ Output: North Star refinado, OKRs, roadmap R1-R4
    └─ Bloqueador: Sem North Star refinado, R1 não tem direção
        ↓
R1 Kick-off
    ├─ Input: Roadmap R1, OKRs de R1, ontologia validada
    └─ Output: R1 começa 2026-08-19
```

### Análise de Paralelização

**Série Crítica:** Sprint 0.0 → 0.1 → 0.3 (job → value prop → final)  
**Paralelo:** Sprint 0.2 (ontologia) pode começar junto com 0.1

**Impacto:** Com paralelização, ganha ~1 semana

---

## Dependências Intra-Sprint

### Sprint 0.0: JTBD Discovery

```
JTBD Interviews (B0.1)
    └─ Outputs: Raw notes, themes, forces
        ↓
Job Statement Validation (B0.2)
    └─ Inputs: Interview data
    ├─ Outputs: Validated job statement
    └─ Deliverable: JTBD_RESEARCH.md
```

**Bloqueador:** Interviews devem ser feitos primeiro (B0.1 → B0.2)  
**Duration:** ~3-4 days serial

---

### Sprint 0.1: Value Prop + Positioning

```
Refine VALUE_PROPOSITION.md (já existente)
    └─ Input: Job statement do 0.0
    ├─ Output: Value prop draft
    └─ Dependency: B0.0 COMPLETE

Detalhar COMPETITIVE_LANDSCAPE.md (já existente)
    └─ Input: Job statement, value prop
    ├─ Output: Competitive analysis
    └─ Dependency: B0.0 COMPLETE

Validate Positioning (B1.3)
    └─ Inputs: Value prop, competitive analysis
    └─ Dependency: Refine + Detalhar COMPLETE (serial)

Draft GTM Strategy (B1.4)
    └─ Input: Validated positioning
    └─ Dependency: B1.3 COMPLETE

Deliverables: VALUE_PROP_REFINED.md, GTM_STRATEGY.md
```

**Critical Path:** Value prop → Positioning validation → GTM (serial)  
**Duration:** ~2 days

---

### Sprint 0.2: Purpose + Ontologies

```
Define 5 Conceitos Core (B0.3)
    └─ Inputs: Job statement (informação)
    ├─ Output: 5 conceitos especificados
    └─ No dependency (pode começar em paralelo com 0.1)

Map Relações Semânticas (B0.4)
    └─ Input: 5 conceitos definidos
    ├─ Output: Relações mapeadas
    └─ Dependency: B0.3 COMPLETE

Especificar Restrições (semelhante)
    └─ Input: Conceitos + Relações
    └─ Dependency: B0.3 + B0.4 COMPLETE

Definir Semantic Layer Rules (B0.5)
    └─ Input: Conceitos, relações, restrições
    ├─ Output: 10+ regras documentadas
    └─ Dependency: B0.3 + B0.4 + Restrições COMPLETE

Validar Ontologia (B0.6)
    └─ Input: Ontologia completa
    └─ Dependency: Tudo acima COMPLETE

Deliverables: ONTOLOGY_SPEC.md, SEMANTIC_LAYER_SPEC.md
```

**Critical Path:** Conceitos → Relações → Restrições → Rules → Validação (serial)  
**Duration:** ~4.5 days

---

### Sprint 0.3: North Star + OKRs + Roadmap

```
Refine NORTH_STAR.md (B0.7)
    └─ Inputs: Tudo de 0.0-0.2
    └─ Dependency: 0.0 + 0.1 + 0.2 COMPLETE

Define OKRs de R0 (B0.8)
    └─ Inputs: North Star, value prop, job statement
    ├─ Output: OKRs com métricas
    └─ Dependency: B0.7 COMPLETE (ou paralelo)

Structure Roadmap R1-R4 (B0.9)
    └─ Inputs: OKRs de R0, ontologia, market validation
    ├─ Output: Roadmap com timelines
    └─ Dependency: B0.8 COMPLETE

Kick-off R1 Prep (B1.5)
    └─ Input: Roadmap R1, OKRs
    └─ Dependency: B0.9 COMPLETE

Deliverables: NORTH_STAR_FINAL.md, R1/README.md, R1/OKR.md
```

**Critical Path:** North Star → OKRs → Roadmap → Kick-off (serial)  
**Duration:** ~3.5 days

---

## Dependências de Stakeholder

| Stakeholder | Quando Needed | O Que Precisa | Por Quê |
|-------------|--------------|---------------|---------|
| **Business Sponsor** | Sprint 0.0 (kickoff) | Alinhamento com strategy | Autoriza recursos |
| **Domain Experts** | Sprint 0.0-0.2 | Validação de conceitos | Ontologia está correta |
| **Engineering Lead** | Sprint 0.2 | Review de ontologia | Feedback técnico |
| **Team** | Sprint 0.2 (mid) | Clareza de conceitos | Podem trabalhar em R1 |
| **All Stakeholders** | Sprint 0.3 (end) | Aprovação de roadmap | Alinhamento antes R1 |

---

## Risks & Mitigations: Dependência-Based

### Risk 1: Sprint 0.0 não valida job
**Probabilidade:** Média  
**Impacto:** ALTO (bloqueia 0.1 e cascata)  
**Mitigation:**
- Entrevistar 5+ personas DISTINTAS (não só PMs)
- Usar framework JTBD rigoroso (wondelai/skills)
- Weekly sync com sponsor pra feedback

### Risk 2: Job statement muda depois de 0.0
**Probabilidade:** Baixa  
**Impacto:** ALTO (invalida value prop, ontologia)  
**Mitigation:**
- Sign-off formal de job statement (fim 0.0)
- Não permitir mudanças após sign-off (exceto sprint 0.3 review)

### Risk 3: Ontologia fica too complex
**Probabilidade:** Média  
**Impacto:** MÉDIO (2.2 toma mais tempo, atrasa 0.3)  
**Mitigation:**
- Start with 5 conceitos SIMPLES
- Refine depois em R1-R2
- Weekly validation com domain expert

### Risk 4: 0.2 leva mais tempo que estimado
**Probabilidade:** Alta (usual em design)  
**Impacto:** MÉDIO (aperta timeline 0.3)  
**Mitigation:**
- Começar 0.2 em paralelo com 0.1
- Ter buffer de 1 day no final de 0.2
- Cut "nice-to-have" se necessário

### Risk 5: Stakeholders não alignam em 0.3
**Probabilidade:** Baixa  
**Impacto:** ALTO (atrasa R1 kickoff)  
**Mitigation:**
- Weekly syncs com sponsor durante 0.0-0.2
- Draft de North Star no final de 0.2
- Approval meeting no meio de 0.3

---

## Crítico-path Analysis

**Caminho Crítico:** 0.0 → 0.1 → 0.3 (job → value prop → final)

**Duração:** 
- Sprint 0.0: 3d
- Sprint 0.1: 2d
- Sprint 0.3: 3.5d
- **Total:** ~8.5 days

**Slack:**
- Sprint 0.2 (paralelo): ~4.5 days (pode começar depois de 0.1 start)
- Total capacity: ~20 days
- **Buffer:** ~11.5 days (buffer grande = healthy)

**Conclusão:** Timeline é confortável. Risco baixo de atraso.

---

## Dependency Board (Visual)

```
Sprint 0.0
├─ B0.1 JTBD Interviews (2d)
└─ B0.2 Job Statement (1d) ← SIGN-OFF NEEDED
    │
    ├──→ Sprint 0.1 Value Prop
    │    ├─ Refine VALUE_PROP (0.5d)
    │    ├─ Detail COMPETITIVE (0.5d)
    │    └─ B1.3 Validate (0.5d) ← SIGN-OFF NEEDED
    │         │
    │         └──→ B1.4 GTM Strategy (0.5d)
    │
    └──→ Sprint 0.2 Ontologies (PARALLEL START OK)
         ├─ B0.3 Conceitos (1.5d)
         ├─ B0.4 Relações (1d) ← depends on B0.3
         ├─ Restrições (0.5d) ← depends on B0.3 + B0.4
         ├─ B0.5 Semantic Layer (1d) ← depends on all above
         └─ B0.6 Validar (0.5d) ← SIGN-OFF NEEDED
              │
              └──→ Sprint 0.3 Final
                   ├─ B0.7 North Star (0.5d)
                   ├─ B0.8 OKRs (1d)
                   ├─ B0.9 Roadmap R1-R4 (1.5d)
                   └─ B1.5 Kick-off Prep (0.5d)
                        │
                        └──→ R1 Kick-off (2026-08-19)
```

---

## Aplicação de Learnings Sprint 0.0 (RCA 20-07)

### Parallelization Rules (Sprint 0.1+)

**Learning:** Sprint 0.0 planejamento assumiu sequencial (Tier 1 → Tier 2), mas execução descobriu que paralelização era viável (+250% velocity). Planning foi muito conservador.

**Regra 1: Questionar Bloqueadores Agressivamente**
- Para cada dependência "B depende de A", perguntar: "O que é EXATAMENTE a saída de A que B precisa?"
- Se resposta é "conceito/direção", A pode começar em paralelo com rascunho
- Se resposta é "dados concretos", então bloqueador real existe

**Regra 2: MVP Gates entre Tarefas Bloqueadas**
- Tarefas bloqueadas podem começar com RASCUNHO enquanto bloqueador ainda executa
- Bloqueador entrega MVP (esboço, direção) → bloqueado começa com rascunho → bloqueador refina
- Exemplo S0.1: T0.1.1 (VALUE_PROP esboço) → T0.1.3 (OKR rascunho) paralelo

**Regra 3: Validar Paralelização no Kick-off**
- Reserve 15 min no kick-off para "dependency challenge" — questionar cada bloqueador
- Prototipo rápido: executar primeira tarefa de bloqueador, criar MVP output, validar que bloqueado pode começar

**Resultado S0.1 Aplicado:**
- T0.1.1 (1.5d) + T0.1.2 (1d) **paralelo** (sem mudança)
- T0.1.3 (1.5d) **inicia com rascunho** enquanto T0.1.1 refina → economia ~0.5d
- Estimativa: 5d planejado → 4-4.5d real (1.1x, vs. 2.2x S0.0)

---

## Histórico de Atualizações

| Data | O Quê | Razão |
|------|-------|-------|
| 19-07 | Draft inicial | Planning S0.0-0.3 |
| 20-07 | MVP Gates + Parallelization Rules | RCA S0.0 learnings |

---

**Criado em:** 2026-07-19  
**Versão:** 2.0 (com learnings S0.0)  
**Próximo Update:** Após Sprint 0.1 (validar paralelização real)
