# Sprint 0.0: Tasks

**CRITICAL:** Sprint 0.0 não é só JTBD Discovery. É implementação de **3 componentes core**:
1. **Release Management Framework** (T0.0.1)
2. **Bootstrap Gate + Foundation Definition Session** (T0.0.2-T0.0.3)
3. **APOS Self-Identification** (T0.0.4)

---

## T0.0.1: Implement Release Management Framework (1 person-day)

**Objective:** Criar artefatos de Release Management que todo projeto que importa APOS recebe

**Tasks:**
- [ ] Criar `docs/releases/R0/SPRINT_PLAN.md` (10 sprints estruturados)
- [ ] Criar `docs/releases/R0/BACKLOG.md` (items priorizados P0-P3)
- [ ] Criar `docs/releases/R0/DEPENDENCY_MAP.md` (dependencies, critical path)
- [ ] Criar `sprint-X/` structure (README, TASKS, USER_STORIES, BOARD, STATUS, RISK_MITIGATION, RETRO)
- [ ] Validar que framework é operacional e pronto para execução

**Deliverable:** `Release Management Framework (templates + docs)`

**Owner:** PM / Release Management Skill  
**Effort:** 1 day  
**Status:** DONE (Em R0/APOS, este framework já foi criado)

---

## T0.0.2: Implement Bootstrap Gate + Foundation Definition Session (2 person-days)

**Objective:** Criar validator automático que detecta gaps de fundação e inicia sessão de definição

**Tasks:**
- [ ] Implementar `apos.bootstrap_gate.validate()` — checa existência de 10 itens obrigatórios
- [ ] Implementar `apos.bootstrap_gate.initialize_foundation_session()` — auto-gera templates + guias
- [ ] Criar templates auto-gerados (NORTH_STAR.md, OKR.md, ONTOLOGY.md, etc)
- [ ] Documentar validação rules em `BOOTSTRAP_GATE.md`
- [ ] Testar fluxo: gap detection → template generation → session initialization

**Deliverables:** 
- `BOOTSTRAP_GATE.md` (specification)
- `apos/bootstrap/gate.py` (implementation)
- `apos/bootstrap/templates/` (auto-generated docs)

**Owner:** PM / Framework Engineering  
**Effort:** 2 days  
**Status:** DEFINED (em BOOTSTRAP_GATE.md)

---

## T0.0.3: Implement APOS Self-Identification + Session Management (1 person-day)

**Objective:** Projeto que importa APOS sabe que É um projeto APOS e pode iniciar sesão

**Tasks:**
- [ ] Criar `apos.__init__.py` com `apos_project` metadata
- [ ] Implementar `apos.SessionManager.initialize()` — gerencia sessão de foundation definition
- [ ] Criar CLI: `python -m apos init` — inicia setup de novo projeto
- [ ] Implementar detecção: projeto reconhece "Inicie uma sessão com APOS"
- [ ] Criar exemplo: `apos.SessionManager().run()` → conduz usuário através de JTBD → Strategy → Ontology

**Fluxo:**
```
$ python -m apos init

APOS Project Initialization
===========================

Detectando status de fundações...

✅ Cheque: NORTH_STAR.md
✅ Cheque: OKR.md
✅ Cheque: PURPOSE.md
...

GAPS DETECTADOS:
❌ ONTOLOGY.md (missing)
❌ SEMANTIC_LAYER.md (missing)
❌ GOVERNANCE.md (missing)

Iniciando Foundation Definition Session...
(Conduzindo usuário através de JTBD → Strategy → Ontology)
```

**Deliverables:**
- `apos/__init__.py` (metadata + imports)
- `apos/bootstrap/session.py` (SessionManager)
- `apos/__main__.py` (CLI: `python -m apos init`)
- Documentação em `BOOTSTRAP_GATE.md`

**Owner:** Framework Engineering  
**Effort:** 1 day  
**Status:** DEFINED

---

## T0.0.A: Conduct JTBD Interviews (2 person-days)

**Objective:** Interview 5+ personas to understand the job APOS solves

**Tasks:**

- [ ] Prepare interview kit (scenarios, questions, consent form)
- [ ] Schedule 5+ interviews (target: PM, agent, stakeholder personas)
- [ ] Conduct interviews (2-3 per day)
- [ ] Record/transcribe notes
- [ ] Document raw insights

**Interviews to Conduct:**

1. Product Manager (team lead) — focus on overhead of alignment
2. AI Agent (conceptual) — focus on context needs
3. CTO/Architect — focus on technical feasibility
4. Stakeholder (business) — focus on ROI/value
5. Additional (early adopter team) — focus on adoption

**Deliverable:** `JTBD-INTERVIEWS-RAW-NOTES.md`

**Owner:** PM
**Effort:** 2 days
**Status:** Planned

---

## T0.0.B: Map Forces of Progress (1 person-day)

**Objective:** Analyze Push/Pull/Anxiety/Habit for each persona

**Tasks:**

- [ ] Review interview notes
- [ ] Extract signals of Push (frustration, pain, current workarounds)
- [ ] Extract signals of Pull (attraction to APOS, desired outcome)
- [ ] Extract signals of Anxiety (fears, concerns, risks)
- [ ] Extract signals of Habit (current patterns, inertia)
- [ ] Create forces matrix

**Framework:**

```
For each persona:
  Push: What frustrates them? What's the current pain?
  Pull: What excites them about APOS?
  Anxiety: What worries them?
  Habit: What are they used to doing?

Score each (1-10): How strong is each force?
```

**Deliverable:** `COMPETITIVE_FORCES.md` (updated with interview data)

**Owner:** PM
**Effort:** 1 day
**Status:** Planned

---

## T0.0.C: Finalize Job Statement (1 person-day)

**Objective:** Write and validate final job statement

**Tasks:**

- [ ] Draft job statement from interviews: "When [circumstances], I want to [progress], so I can [outcome]"
- [ ] Validate against interview data (does it reflect real insights?)
- [ ] Check three dimensions: Functional + Emotional + Social
- [ ] Review with stakeholders
- [ ] Refine based on feedback
- [ ] Get sign-off (stakeholder approval)

**Template:**

```
Job Statement (Final):
"When [PM/Agent receives task in distributed team],
 I want [cadeia Task→Feature→Release→OKR→Métrica visible],
 so I can [execute with purpose, not at drift]."

Functional: [what needs to be done]
Emotional: [how they want to feel]
Social: [how they want to be perceived]
```

**Deliverable:** `JOB_STATEMENT.md` (signed off)

**Owner:** PM
**Effort:** 1 day
**Status:** Planned

---

## Summary

| Task | Component | Effort | Status | Owner |
|------|-----------|--------|--------|-------|
| T0.0.1 | Release Management Framework Implementation | 1d | DONE | PM |
| T0.0.2 | Bootstrap Gate + Session Manager | 2d | DEFINED | Engineering |
| T0.0.3 | APOS Self-Identification + CLI | 1d | DEFINED | Engineering |
| T0.0.A | JTBD Discovery Interviews | 2d | Planned | PM |
| T0.0.B | Forces Analysis | 1d | Planned | PM |
| T0.0.C | Job Statement Validation | 1d | Planned | PM |
| **TOTAL** | | **8d** | | |

---

**Critical Context:**

- **T0.0.1-T0.0.3 são implementação de APOS Core** — Quando um projeto importa APOS, recebe Release Management Framework + Bootstrap Gate
- **T0.0.A-T0.0.C é JTBD Discovery** — Validar que APOS resolve job real
- **Resultado Final:** Projeto que importa APOS sabe ser APOS, valida seus fundamentos, e pode iniciar sesões de definição

---

**Created:** 2026-07-19
**Status:** PLANNED — Ready for Sprint 0.0 Kickoff
