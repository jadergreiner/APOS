# APOS R0 Backlog

**Release:** R0 (APOS Foundations)  
**Prioridade:** Todas as tasks de R0 são críticas (100% deve ser feito)  
**Status:** PLANNED

---

## Backlog Prioritizado

### P0: Must-Have (Sprint-Blocking)

| ID | Item | Sprint | Effort | Owner | Status |
|----|------|--------|--------|-------|--------|
| **B0.1** | Conduzir JTBD interviews (5+) | 0.0 | 2d | PM | Planned |
| **B0.2** | Validar job statement | 0.0 | 1d | PM | Planned |
| **B0.3** | Definir 5 conceitos core da ontologia | 0.2 | 1.5d | Architect | Planned |
| **B0.4** | Mapear relações semânticas | 0.2 | 1d | Architect | Planned |
| **B0.5** | Especificar 10+ regras de semantic layer | 0.2 | 1d | Architect | Planned |
| **B0.6** | Validar ontologia com team | 0.2 | 0.5d | PM | Planned |
| **B0.7** | Refinar North Star | 0.3 | 0.5d | PM | Planned |
| **B0.8** | Definir OKRs de R0 com métricas | 0.3 | 1d | PM | Planned |
| **B0.9** | Estruturar roadmap R1-R4 | 0.3 | 1.5d | PM | Planned |

**Subtotal P0:** 10 tasks, ~9.5 person-days

### P1: Should-Have (Enhancements)

| ID | Item | Sprint | Effort | Owner | Status |
|----|------|--------|--------|-------|--------|
| **B1.1** | Documentar catálogo schema (estrutura) | 0.2 | 0.5d | Architect | Planned |
| **B1.2** | Especificar MCP contract | 0.2 | 0.5d | Architect | Planned |
| **B1.3** | Validar positioning com personas | 0.1 | 0.5d | PM | Planned |
| **B1.4** | Draft go-to-market strategy | 0.1 | 0.5d | PM | Planned |
| **B1.5** | Preparar materiais de kick-off R1 | 0.3 | 0.5d | PM | Planned |

**Subtotal P1:** 5 tasks, ~2.5 person-days

### P2: Could-Have (Nice-to-Have)

| ID | Item | Sprint | Effort | Owner | Status |
|----|------|--------|--------|-------|--------|
| **B2.1** | Criar proof-of-concept simples (grafo em memória) | 0.2 | 1d | Architect | Backlog |
| **B2.2** | Documentar exemplos de Knowledge Graph | 0.2 | 0.5d | PM | Backlog |
| **B2.3** | Criar presentation slides (visão, OKRs) | 0.3 | 0.5d | PM | Backlog |

**Subtotal P2:** 3 tasks, ~2 person-days

### P3: Won't-Have (Out of Scope R0)

| ID | Item | Reason | Target |
|----|------|--------|--------|
| **B3.1** | Implementar Knowledge Graph | Escopo de R1 | R1 |
| **B3.2** | Criar loaders (Jira, Notion, Slack) | Escopo de R1 | R1 |
| **B3.3** | Implementar semantic gates | Escopo de R3 | R3 |
| **B3.4** | Criar audit runner | Escopo de R3 | R3 |
| **B3.5** | Build dashboard visual | Escopo de R1-R2 | R1-R2 |

---

## Distribuição por Sprint

### Sprint 0.0: JTBD Discovery

**Foco:** Validar job real

**P0 Tasks:**
- B0.1: JTBD interviews (2d)
- B0.2: Job statement validation (1d)

**Subtotal:** 3d

---

### Sprint 0.1: Value Prop + Positioning

**Foco:** Comunicação clara da diferenciação

**P0 Tasks:**
- Refinar VALUE_PROPOSITION.md (já está criado, refinamento 0.5d)
- Detalhar COMPETITIVE_LANDSCAPE.md (já está criado, refinamento 0.5d)

**P1 Tasks:**
- B1.3: Validar positioning (0.5d)
- B1.4: GTM strategy draft (0.5d)

**Subtotal:** 2d

---

### Sprint 0.2: Purpose + Ontologies

**Foco:** Fundações semânticas formais

**P0 Tasks:**
- B0.3: Definir conceitos (1.5d)
- B0.4: Mapear relações (1d)
- B0.5: Semantic layer rules (1d)
- B0.6: Validar com team (0.5d)

**P1 Tasks:**
- B1.1: Catálogo schema (0.5d)
- B1.2: MCP contract (0.5d)

**P2 Tasks (se houver tempo):**
- B2.1: Proof-of-concept (1d, optional)

**Subtotal:** 5-6d

---

### Sprint 0.3: North Star + OKRs + Roadmap

**Foco:** Refinamento estratégico e planejamento de R1

**P0 Tasks:**
- B0.7: Refinar North Star (0.5d)
- B0.8: Definir OKRs (1d)
- B0.9: Roadmap R1-R4 (1.5d)

**P1 Tasks:**
- B1.5: Kick-off R1 prep (0.5d)

**P2 Tasks (se houver tempo):**
- B2.3: Presentation slides (0.5d, optional)

**Subtotal:** 3.5-4d

---

## Estimation Summary

| Prioridade | # Tasks | Effort | Sprint Target |
|-----------|---------|--------|--------------|
| **P0** | 9 | ~9.5d | Sprint 0.0-0.3 (MUST) |
| **P1** | 5 | ~2.5d | Sprint 0.1-0.3 (SHOULD) |
| **P2** | 3 | ~2d | If time allows |
| **TOTAL** | 17 | ~13.5d | 4 weeks capacity |

**Capacity:** 20 person-days (4w × 5d)  
**P0+P1:** 12 person-days (60% utilization — healthy)  
**Buffer:** 8 person-days (40% — standups, admin, risks, delays)

---

## Definition of Done (R0 Complete)

R0 é considerado COMPLETE quando:

- ✅ JTBD research validou job (Sprint 0.0)
- ✅ VALUE_PROPOSITION.md testado com personas (Sprint 0.1)
- ✅ COMPETITIVE_LANDSCAPE.md documentado (Sprint 0.1)
- ✅ ONTOLOGY_SPEC.md + SEMANTIC_LAYER_SPEC.md completamente definidas (Sprint 0.2)
- ✅ NORTH_STAR.md refinado e validado (Sprint 0.3)
- ✅ R0 OKRs definidas com métricas mensuráveis (Sprint 0.3)
- ✅ Roadmap R1-R4 estruturado (Sprint 0.3)
- ✅ R1 kick-off agendado com team (Sprint 0.3)
- ✅ Stakeholder alignment > 90% (All sprints)

---

## Velocity Tracking

Será atualizado após cada sprint:

| Sprint | Planned | Completed | Velocity | Notes |
|--------|---------|-----------|----------|-------|
| 0.0 | 3d | TBD | TBD | |
| 0.1 | 2d | TBD | TBD | |
| 0.2 | 5-6d | TBD | TBD | |
| 0.3 | 3.5-4d | TBD | TBD | |

---

**Criado em:** 2026-07-19  
**Versão:** 1.0 (Draft)  
**Próximo Update:** Após Sprint 0.0 (2026-07-26)
