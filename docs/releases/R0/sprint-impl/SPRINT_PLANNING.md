# Sprint Planning — sprint-impl

**Data:** 2026-07-21
**Duracao:** 60min
**Participantes:** Jader

---

## 🎯 Sprint Goal

> Converter as especificacoes de Sprint 0.5-0.7 (19K linhas de docs) em modulos Python importaveis via pip install apos

---

## 🎯 Alinhamento com OKRs

- O1: Definir Ontologia Formal — KR4: agente consegue raciocinar sobre cadeia
- O4: Estruturar Roadmap R1-R4 — KR1: R1 roadmap definido

Ao tornar Context Engine, Capabilities e Harness importaveis como codigo, APOS sai de especificacao e se torna framework executavel — habilitando R1 (ProjectAdapter)

---

## 📖 User Stories

### US-001: Context Engine importavel

**Descricao:** Como desenvolvedor, quero importar Context Engine via from apos.context_engine para poder montar contexto para agentes a partir do Knowledge Graph

**Prioridade:** P0

**Criterios de Aceitacao:**
- [ ] Pipeline extracao->montagem->injecao->cleanup funcional
- [ ] MemoryManager com 4 tipos de memoria + TTL
- [ ] TokenBudget com limites por tipo de no

### US-002: Capabilities como codigo

**Descricao:** Como desenvolvedor, quero importar modulo de capabilities para registrar, descobrir e rotear capacidades do sistema

**Prioridade:** P0

**Criterios de Aceitacao:**
- [ ] CapabilityRegistry com register/discover/get
- [ ] Router com 3 estrategias de resolucao (exato, node_type, similaridade)
- [ ] Chain de capabilities com max_depth=5

### US-003: Harness executavel

**Descricao:** Como desenvolvedor, quero usar o harness para executar agentes e capabilities com controle de ciclo de vida e simulacao

**Prioridade:** P0

**Criterios de Aceitacao:**
- [ ] AgentHarness com ciclo de vida start/stop/health
- [ ] CapabilityHarness com execucao, erro e fallback
- [ ] EvaluationHarness com 5 tipos e 16 metricas
- [ ] SimulationHarness com 4 perfis de carga

---

## 📋 Tasks Planejadas

| ID | Titulo | Estimativa | Story |
|----|--------|-----------|-------|
| IMPL-001 | apos/context_engine/ | 5.0d | - |
| IMPL-002 | apos/capabilities/ | 4.0d | - |
| IMPL-003 | apos/harness/ | 5.0d | - |

**Total:** 14.0d | **Velocity target:** 3.0d

---

## 🔗 Mapa de Dependencias

- `IMPL-001` → `IMPL-002`: Modulos independentes — paralelo total
- `IMPL-002` → `IMPL-003`: Harness usa Capability model — sequencial parcial

---

## 🚨 Riscos

| Risco | Prob | Impacto | Mitigacao |
|-------|------|---------|-----------|
| 19K linhas de docs para converter — subagent pode timeoutar | Alta | Alto | Delegar um modulo por vez, com validacao apos cada um |
| Qualidade da conversao docs->codigo pode ser baixa | Media | Medio | Validar com pytest e import test apos cada modulo |
| Dependencia entre modulos (harness importa capabilities) | Baixa | Medio | Implementar interfaces primeiro, implementacao depois |

---

## 👥 Entrevistas com Stakeholders

_[Entrevistar stakeholders para validar escopo]_


---

## 📊 Metricas da Sprint

| Metrica | Alvo | Descricao |
|---------|------|-----------|
| Modulos implementados | 3/3 | context_engine, capabilities, harness como Python |
| Import test | 100% | from apos.XXX import ... funciona sem erros |
| Testes passando | >60% | Testes unitarios dos modulos passando |

---

## 🔄 Acoes da Retro Anterior

- Sprint Planning + Jira sync automatico — Status: ✅ Concluido — Dono: Hermes
- Refinamento colaborativo com PM — Status: ✅ Concluido — Dono: Hermes
- User Stories no Sprint Planning — Status: 🔄 Em andamento — Dono: Hermes

---

**Sprint Planning criado:** 2026-07-21

