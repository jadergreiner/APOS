# 📋 R1 PLAN REVISED — Baseado em Realidade de R0

**Data:** 2026-07-21  
**Baseado em:** R0_REALITY_CHECK.md + código real de APOS + R1/sprint-1.0/SPRINT_PLANNING.md  
**Objetivo:** Plano realista de R1 que aproveita O QUE R0 REALMENTE ENTREGOU

---

## 🎯 VISÃO R1

**Missão:** Tornar APOS operacional em Meu PDI com ProjectAdapter + observabilidade real

**Objetivo:** Validar que APOS reduz retrabalho em produção (não estimativa, dados reais)

---

## 📊 O QUE R0 ENTREGOU (Use Isto)

```
✅ Core Layer (100% testado)
   - KnowledgeGraph
   - Node/Edge types
   - Entity/Relationship primitives

✅ Bootstrap Gate (81% testado)
   - Valida 10 fundações
   - Auto-gera templates
   - Sessão guiada de definição

✅ Trust Score Engine
   - 3 dimensões (coverage, quality, consistency)
   - Scoring 0.0-1.0
   - Operacional

✅ Release Management
   - Release, Sprint, Task management
   - Ceremony support (daily standup, retro, planning)
   - Template generation

⚠️  Context Engine (80% pronto)
   - Boundaries, Retrieval, Memory
   - Tem gaps, precisa testes

⚠️  Harness (50% pronto — CRÍTICO)
   - Agent/Capability/Evaluation harness
   - PRECISA de testes urgente (3 SP)

⚠️  Capabilities (60% pronto)
   - Taxonomy, Router, Model
   - Precisa testes (2 SP)
```

---

## 🆕 O QUE R1 DEVE ENTREGAR (Novo)

### R1.1: ProjectAdapter Core (3 SP)

**O Quê:**
```python
from apos import ProjectAdapter

adapter = ProjectAdapter()
discovery = adapter.discover("/path/to/meu-pdi")

# Retorna:
# {
#   "stack": ["Python", "Django", "PostgreSQL"],
#   "domain": "trading/fintech",
#   "modules": {...},
#   "relationships": {...},
#   "confidence": 0.85
# }
```

**Por Quê:**
- Meu PDI precisa descobrir sua própria estrutura automaticamente
- BootstrapGate + ProjectAdapter = fundações prontas pra APOS

**Critério de Sucesso:**
- ✅ `discover()` funciona em Meu PDI
- ✅ Descobre ≥80% da estrutura real
- ✅ Testes passam com repositório real

**Dependências:**
- Usa: BootstrapGate (já existe)
- Precisa: Meu PDI setup (será feito em R1.2)

---

### R1.2: Bootstrap Gate 2.0 (3 SP)

**O Quê:**
- Refazer BootstrapGate pra ser integrado com ProjectAdapter
- Usar contexto descoberto por ProjectAdapter pra validar fundações
- Auto-gerar APOS_CONFIG.yaml com base em descoberta

**Por Quê:**
- Gate 1.0 valida fundações APOS (genérico)
- Gate 2.0 valida fundações Meu PDI (específico, usando ProjectAdapter)

**Critério de Sucesso:**
- ✅ Aceita output de ProjectAdapter
- ✅ Valida usando contexto real de Meu PDI
- ✅ Gera APOS_CONFIG.yaml automático

---

### R1.3: Domain Ontology Adapter (2 SP)

**O Quê:**
- Camada que mapeia estrutura descoberta por ProjectAdapter → APOS Ontology
- Cria Node/Edge types baseado em contexto real de Meu PDI

**Por Quê:**
- ProjectAdapter descobre "stack: Django" → Ontology precisa saber o que é Django
- Mapeia domínio real (trading, signals, risk) → ontologia

**Critério de Sucesso:**
- ✅ Mapeia Django models → Node types
- ✅ Mapeia relacionamentos Django → Edge types
- ✅ Cria KnowledgeGraph inicial

---

## 🔧 O QUE R1 DEVE MELHORAR (Existente)

### R1.T1: Harness Coverage Aumentada (3 SP)

**O Quê:**
- Aumentar harness/ de 50% → 80%+ coverage
- Adicionar integration tests

**Por Quê:**
- Harness é observabilidade do sistema
- 50% é inaceitável pra componente crítica

**Critério de Sucesso:**
- ✅ coverage >= 80%
- ✅ Integration tests validam trust score calculation

---

### R1.T2: Capabilities Coverage Aumentada (2 SP)

**O Quê:**
- Aumentar capabilities/ de 60% → 80%+ coverage

**Por Quê:**
- Routing e Taxonomy precisam ser confiáveis

**Critério de Sucesso:**
- ✅ coverage >= 80%
- ✅ Testes de routing com casos reais

---

### R1.T3: Meu PDI Observabilidade Setup (2 SP)

**O Quê:**
- Setup de logging/observabilidade em Meu PDI
- Coleta de: token count, latência, retrabalho %

**Por Quê:**
- Baseline pré-APOS necessária pra validar impacto
- Sem dados, não sabemos se APOS funciona

**Critério de Sucesso:**
- ✅ Logging setup em Meu PDI
- ✅ 2 semanas de dados baseline coletados
- ✅ Dashboard de métricas criado

---

## 📅 R1 TIMELINE (3 Semanas)

```
SEMANA 1: Foundation + Core

  DIA 1-2: R1.T1 (Harness Coverage 80%)
  └─ Aumentar testes harness
  
  DIA 2-3: R1.1 (ProjectAdapter Core)
  └─ Implementar discover()
  
  DIA 3: R1.T2 (Capabilities Coverage)
  └─ Aumentar testes capabilities

SEMANA 2: Integration + Validation

  DIA 4-5: R1.2 (Bootstrap Gate 2.0)
  └─ Integrar com ProjectAdapter
  
  DIA 5: R1.T3 (Observabilidade Setup)
  └─ Setup logging Meu PDI
  
  DIA 6: Integração E2E
  └─ ProjectAdapter → Bootstrap → Ontology

SEMANA 3: Testing + Documentation

  DIA 7: R1.3 (Domain Ontology Adapter)
  └─ Mapear contexto Meu PDI → Ontology
  
  DIA 7-8: Integration Testing
  └─ Testes end-to-end
  
  DIA 9: Documentation
  └─ Atualizar docs
```

---

## 📊 R1 SCOPE (Story Points)

| Sprint | Task | SP | Owner | Status |
|--------|------|----|----|--------|
| R1.1 | ProjectAdapter Core | 3 | Tech Lead APOS | New |
| R1.2 | Bootstrap Gate 2.0 | 3 | Tech Lead APOS | New |
| R1.3 | Domain Ontology Adapter | 2 | Tech Lead APOS | New |
| R1.T1 | Harness Coverage 80%+ | 3 | Tech Lead APOS | Improvement |
| R1.T2 | Capabilities Coverage 80%+ | 2 | Tech Lead APOS | Improvement |
| R1.T3 | Meu PDI Observabilidade | 2 | PM Meu PDI | Setup |
| **TOTAL** | | **15 SP** | | **3 weeks** |

---

## 🎯 R1 DEFIN ITIONS OF DONE

### ProjectAdapter (R1.1)
- [ ] `ProjectAdapter` class implemented
- [ ] `discover()` method works on real projects
- [ ] Tests pass (min 80% coverage)
- [ ] Works on Meu PDI (discovers ≥80%)
- [ ] Documentation updated

### Bootstrap Gate 2.0 (R1.2)
- [ ] Integrates with ProjectAdapter output
- [ ] Validates using real Meu PDI context
- [ ] Auto-generates APOS_CONFIG.yaml
- [ ] Tests pass
- [ ] Documentation updated

### Domain Ontology Adapter (R1.3)
- [ ] Maps Django models → Node types
- [ ] Maps relationships → Edge types
- [ ] Creates initial KnowledgeGraph
- [ ] Tests pass
- [ ] Works with Meu PDI

### Harness Coverage (R1.T1)
- [ ] Coverage increased 50% → 80%+
- [ ] Integration tests added
- [ ] CI passes

### Capabilities Coverage (R1.T2)
- [ ] Coverage increased 60% → 80%+
- [ ] Routing tests with real cases
- [ ] CI passes

### Meu PDI Observabilidade (R1.T3)
- [ ] Logging setup complete
- [ ] 2 weeks baseline data collected
- [ ] Metrics dashboard working
- [ ] Ready for APOS measurement

---

## 📈 SUCCESS METRICS

### Technical (Must Have)
- ✅ ProjectAdapter discovers ≥80% Meu PDI structure
- ✅ Bootstrap Gate 2.0 validates using real context
- ✅ Harness coverage ≥80%
- ✅ Capabilities coverage ≥80%
- ✅ E2E tests pass (ProjectAdapter → Bootstrap → Ontology → KG)

### Business (Should Have)
- 📊 Baseline metrics collected (token count, latency, rework %)
- 📊 APOS integrated with Meu PDI (no local copies)
- 📊 Team can use APOS in production

---

## 🚫 OUT OF SCOPE (R1)

```
❌ Governance Gates        — Move to R3
❌ Advanced Semantic Layer — Move to R2
❌ Multiple Ontologies     — Keep simple in R1
❌ Performance Optimization— Focus on correctness first
❌ CLI Tools              — Use Python API directly
```

---

## 🔗 DEPENDENCIES

**R1 Depends On:**
- ✅ R0 deliverables (Core, Bootstrap, TrustScore, ReleaseManagement)
- ✅ Meu PDI codebase (real project to test against)
- ✅ Python 3.11+ environment

**R1 Unblocks:**
- R2: Domain KG + Ceremonies (using context from R1)
- R3: Governance (using confidence scores from R1)
- R4: Framework SDK (using integration learnings from R1)

---

## 💡 KEY CHANGES FROM ORIGINAL PLAN

| Original | Revised | Reason |
|----------|---------|--------|
| ProjectAdapter validation was blocker | ProjectAdapter is deliverable | It didn't exist in R0 |
| 8 SP in 1 week | 15 SP in 3 weeks | Realistic estimation |
| "Test pilot then build" | "Build, then validate" | Pilot was impossible (code doesn't exist) |
| Focus on coverage metrics | Focus on real functionality | Coverage doesn't guarantee it works |
| Assume ProjectAdapter exists | Implement ProjectAdapter | Reality check revealed gap |

---

**Status:** ✅ REALISTIC PLAN BASED ON R0 REALITY  
**Next:** Execute PRÉ-R1 to validate prerequisites  
**Confidence:** ✅ HIGH — plan is grounded in what actually exists
