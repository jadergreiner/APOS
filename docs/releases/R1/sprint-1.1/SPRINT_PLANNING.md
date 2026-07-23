# Sprint Planning — R1 Sprint 1.1

**Data:** 2026-07-22
**Duracao:** 30min
**Status:** ✅ APROVADO (Jader, 2026-07-22)
**Participantes:** Jader (CEO + Tech Lead + Dev)

---

## 1. Contexto — Onde Estamos

**Sprint 1.0 entregou:** 3.5/3.5 SP core
- ✅ Trilha A: Harness Coverage (180 testes, 99% coverage) — **R1.T1 concluído**
- ✅ Trilha B: ProjectAdapter core + validacao Meu PDI (47+10 testes) — **R1.1 concluído**

**O plano original R1.** 1 ja esta 40% entregue na Semana 1.

---

## 2. Sprint 1.1 — Escopo Proposto

### 🎯 Sprint Goal

> **"Fechar lacunas de cobertura + integrar ProjectAdapter com BootstrapGate — 6 SP em 1 sprint."**

| Item | Origem | SP | Prioridade |
|------|--------|----|-----------|
| **T1.1.5** — Polish + edge cases (stretch) | Sprint 1.0 carry-over | 1.0 | 🟡 Media |
| **R1.T2** — Capabilities Coverage 80%+ | R1 plan | 2.0 | 🔴 Alta |
| **R1.2** — Bootstrap Gate 2.0 (integrar ProjectAdapter) | R1 plan | 3.0 | 🔴 Alta |
| **R0-AC04** — Recrutar persona real externa | Backlog | 0.5 | 🟢 Baixa |
| **Total** | | **6.5 SP** | |

### Detalhamento

**T1.1.5 — Polish + Edge Cases (1.0 SP)**
- Coverage >85% em agent_harness + capability_harness
- Testes de edge cases documentados na retro

**R1.T2 — Capabilities Coverage (2.0 SP)**
- `apos/capabilities/` tem 5 modulos (615 stmts, 0% coverage)
- Alvo: ≥80% coverage
- Testes: taxonomy, router, model, capability_types

**R1.2 — Bootstrap Gate 2.0 (3.0 SP)**
- Integrar ProjectAdapter com BootstrapGate
- Gate 2.0 usa `ProjectProfile` para validar fundacoes
- Auto-gerar APOS_CONFIG.yaml com base em descoberta
- Testes passam com Meu PDI real

**R0-AC04 — Stakeholder Externo (0.5 SP)**
- Recrutar 1 persona real para validacao
- Aplicar JTBD interview framework

---

## 3. Timeline Estimada

| Dia | Foco | Tasks |
|-----|------|-------|
| D1 | Capabilities + Setup | R1.T2 (scaffold + tests iniciais) |
| D2 | Bootstrap Gate | R1.2 (design + implementacao) |
| D3 | Bootstrap Gate | R1.2 (testes + integracao ProjectAdapter) |
| D4 | Polish + Stakeholder | T1.1.5 + R0-AC04 |
| D5 | Buffer + Review | Fechamento, retro, docs |

---

## 4. Dependencias

| Task | Depende de | Desbloqueia |
|------|-----------|-------------|
| R1.2 (Bootstrap Gate 2.0) | ProjectAdapter (S1.0) | R1.3 (Ontology Adapter) |
| R1.T2 (Capabilities) | Nenhuma | — |
| T1.1.5 (Polish) | Nenhuma | — |

---

## 5. Riscos

| Risco | Prob | Impacto | Mitigacao |
|-------|------|---------|-----------|
| Capabilities tem 0% coverage hoje | Alta | Medio | Focar em modulos core (taxonomy, router) |
| Bootstrap Gate 2.0 depende de API do PA que mudou | Media | Alto | Congelar API do ProjectAdapter |
| Sem stakeholder externo reduz validacao | Media | Baixo | Aceitar auto-validacao nesta sprint |

---

## 6. Decisao

**Aguardando aprovacao para iniciar Sprint 1.1.**

Quer ajustar o escopo (mais/menos SP) ou confirma os 6.5 SP propostos?
