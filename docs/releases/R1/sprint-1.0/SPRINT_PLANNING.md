# Sprint Planning — R1 Sprint 1

**Data:** 2026-07-21
**Duração:** 60min
**Participantes:** Jader (CEO + Tech Lead + PM + SME)
**Formato:** Dupla Via

---

## 🎯 Sprint Goal

> Tornar APOS operacional no Meu PDI: agent_harness/capability_harness ≥80% + ProjectAdapter protótipo funcional.

---

## ✅ Pré-Requisitos Verificados

| Pré-Requisito | Status | Evidência |
|--------------|--------|-----------|
| Sprint Zero executado | ✅ | Tag `r0-2026-07-21`, working tree limpo |
| Jira sync configurado | ✅ | `.jira_sync_history.json` (SCRUM-22 a SCRUM-29) |
| Tag de rollback | ✅ | `r0-2026-07-21` |
| BOARD.md populado | 🔄 | Este documento |

---

## 📊 Alinhamento com OKRs

| KR | Descrição | Sprint | Status |
|----|-----------|--------|--------|
| KR1 | ProjectAdapter descobre ≥80% Meu PDI | S1 protótipo, S2 completo | 🎯 Sprint 1 alvo |
| KR2a | agent_harness + capability_harness ≥80% | Sprint 1 (2 SP) | 🎯 Sprint 1 alvo |
| KR4 | Baseline métricas + 1º comparativo | Iniciar imediatamente | 📋 Iniciar |

---

## 🚂 Dupla Via — Sprint 1

### Trilha A: Harness Coverage (2 SP)
**Meta:** agent_harness + capability_harness ≥80%
**Owner:** Jader
**Milestone:** Dia 2 — coverage report deve mostrar ≥70% ou repriorizar

| Task | Estimativa | Critério de Sucesso |
|------|-----------|---------------------|
| R1-S1-A1: Tests agent_harness (1.587 LOC) | 1.0 SP | coverage report ≥80% |
| R1-S1-A2: Tests capability_harness | 1.0 SP | coverage report ≥80% |

### Trilha B: ProjectAdapter Protótipo (2 SP)
**Meta:** `ProjectAdapter.discover()` funcional em Meu PDI
**Owner:** Jader
**Milestone:** Dia 2 — `discover()` deve extrair ≥50% da estrutura ou pausar

| Task | Estimativa | Critério de Sucesso |
|------|-----------|---------------------|
| R1-S1-B1: Implementar ProjectAdapter core | 1.5 SP | discover() extrai stack + módulos |
| R1-S1-B2: Testes ProjectAdapter em Meu PDI | 0.5 SP | ≥50% descoberta automatizada |

### Buffer (1 dia)
- Folga para imprevistos, integração, ou dívida técnica de R0

---

## ⏱ Milestone de 2 Dias (Obrigatório)

| Dia | Trilha A | Trilha B | Gate |
|-----|----------|----------|------|
| **Dia 1** | Setup testes + agent_harness | Esboço ProjectAdapter | — |
| **Dia 2** | capability_harness coverage | discover() funcional | **🔴 MILESTONE** — Decisão: continua dupla via ou converge? |
| **Dia 3** | Buffer / Convergência | Buffer / Convergência | Decisão documentada |

**Regra:** Se no Dia 2 nenhuma trilha atingir milestone → convergir para Trilha A (harness é crítico para R2). Se ambas progredindo → manter dupla via.

---

## 🚨 Riscos

| Risco | Prob | Impacto | Mitigação |
|-------|------|---------|-----------|
| ProjectAdapter é arquiteturalmente mais complexo que estimado | Média | Alto | Protótipo primeiro; milestone Dia 2 valida |
| Harness 50%→80% expõe dívida técnica profunda | Baixa | Alto | Se coverage >70% no Dia 2, aceitar como suficiente para S1 |
| Dependência de Meu PDI real para testes | Média | Médio | Usar estrutura do próprio APOS para testes offline |
| Jira sync não integrado com Sprint Start | Baixa | Médio | Sync manual temporário; automatizar no S2 |

---

## 🔄 Ações da Retro Anterior (Baseline R0)

| ID | Descrição | Critério de Verificação | Dono | Prioridade | Due |
|----|-----------|------------------------|------|-----------|-----|
| R0-AC01 | Planning paralelo (Tier 1+2) como default | SPRINT_PLANNING.md tem trilhas paralelas | SM | high | S1 |
| R0-AC02 | Templates de cerimônia pré-criados no kickoff | BOARD.md + TASKS.md + SPRINT_PLANNING.md existem no D1 | SM | high | S1 |
| R0-AC03 | Commit Tracking validation integrado | Script de verificação commit → task linkado | Dev | medium | S2 |
| R0-AC04 | Recrutar persona real externa para validação | 1 entrevista externa agendada | CEO | high | S2 |
| R0-AC05 | Refinar baseline de velocity | Estimativas vs real do Sprint Zero documentado | SM | medium | S1 |

---

## 📈 Métricas da Sprint

| Métrica | Alvo | Como medir |
|---------|------|-----------|
| Harness coverage | ≥80% | `pytest --cov=apos/harness --cov=apos/capabilities` |
| ProjectAdapter discovery | ≥50% estrutura Meu PDI | `adapter.discover()` + inspeção manual |
| Milestone Dia 2 | Decisão tomada | Registro em DAILY_STANDUP.md |
| Velocity | 4 SP + buffer | Story points completos / dias |

---

**Sprint Planning criado:** 2026-07-21
**Scrum Master:** Hermes Agent
**Aprovação:** Pendente — CEO deve revisar milestone rules
