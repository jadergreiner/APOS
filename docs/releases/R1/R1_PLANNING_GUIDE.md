# 📋 R1 PLANNING GUIDE — Para SME & Scrum Master

**Data:** 2026-07-21  
**Audiência:** SME (Subject Matter Expert APOS) + Scrum Master + Tech Lead  
**Objetivo:** Orientar R1 planning de forma realista, baseado em R0 realidade

---

## 🎯 LEIA ISTO PRIMEIRO

Antes de planejar R1, **leia nesta ordem:**

1. **[R0_REALITY_CHECK.md](../../analysis/R0_REALITY_CHECK.md)** (10 min)
   - Entenda o que R0 REALMENTE entregou
   - Confirme base sólida pra R1

2. **[R1_PLAN_REVISED.md](../../analysis/R1_PLAN_REVISED.md)** (15 min)
   - Novo scope de R1 (realista)
   - Timeline de 3 weeks
   - 15 SP distribuído

3. **[PRE_R1_REALISTIC.md](../../analysis/PRE_R1_REALISTIC.md)** (10 min)
   - Pré-requisitos validados
   - O que fazer antes de kickoff

**Total:** 35 min de leitura = R1 planning fundado em realidade

---

## 🚨 CONTEXTO CRÍTICO

### O Que Mudou

```
DISCOVERY: ProjectAdapter não existe em R0
├─ Estava no ROADMAP (planejado)
├─ Documentado em R1/sprint-1.0/SPRINT_PLANNING.md
└─ MAS: Sem código, apenas design

IMPLICAÇÃO:
├─ PRÉ-REQ original (teste piloto ProjectAdapter) é IMPOSSÍVEL
├─ ProjectAdapter é deliverable de R1.1, não pré-requisito
└─ R1 precisa IMPLEMENTAR ProjectAdapter, não validar

DECISÃO:
├─ Remover teste piloto do PRÉ-R1
├─ Manter foco: Core + Bootstrap + Harness coverage
└─ R1.1 deliverable: Implementar ProjectAdapter do zero
```

### O Que R0 Realmente Entregou

```
✅ SÓLIDO (Use com confiança):
   - Core Layer (100% testado)
   - Bootstrap Gate (81% testado)
   - TrustScore Engine
   - ReleaseManagement
   - CommitTrackingValidator

⚠️  INCOMPLETO (Use mas termine):
   - ContextEngine (80% pronto)
   - Harness (50% pronto) ← CRÍTICO, precisa 3 SP em R1.1
   - Capabilities (60% pronto)

❌ NÃO EXISTE (R1 deve implementar):
   - ProjectAdapter (é R1.1)
   - Governance (será R3)
```

---

## 📅 R1 PLANNING CEREMONY

### Duração: 3 Horas

```
14:00-14:30  | Context Setting (30 min)
14:30-15:00  | Scope Deep-Dive (30 min)
15:00-15:45  | Sprint Breakdown (45 min)
15:45-16:00  | Q&A + Clarifications (15 min)
16:00-17:00  | Optional: Team grooming (se tempo)
```

### Participantes

- ✅ **SME (You)** — Decisões técnicas, priorização
- ✅ **Scrum Master** — Facilita processo, gerencia tempo
- ✅ **Tech Lead APOS** — Estimativas realistas, riscos
- ✅ **PM Meu PDI** — Observabilidade, contexto do projeto
- ✅ **Tech Lead Meu PDI** — Integração, prazos

---

## 🎬 FASE 1: Context Setting (14:00-14:30)

### Apresentação (15 min)

**Você (SME) apresenta:**

1. **"O que R0 realmente entregou"** (5 min)
   - Mostrar: Core, Bootstrap, TrustScore funcionando
   - Demonstrar: `import apos; print(apos.__file__)` ✅ site-packages
   - Explicar: ProjectAdapter não existe, é R1.1

2. **"Por que R1 é diferente"** (5 min)
   - Original plan: teste piloto ProjectAdapter
   - Realidade: ProjectAdapter não existe
   - Novo plan: IMPLEMENTAR ProjectAdapter em R1.1

3. **"Timeline realista"** (5 min)
   - Original: 8 SP em 1 week (otimista)
   - Realista: 15 SP em 3 weeks
   - Breakdown: R1.1-R1.3 (new) + R1.T1-T3 (improvements)

### Q&A (15 min)

- SME responde dúvidas
- Scrum Master anota blockers
- Discute capacidade do time

---

## 🎬 FASE 2: Scope Deep-Dive (14:30-15:00)

### R1.1: ProjectAdapter Core (3 SP)

**O quê:**
```python
adapter = ProjectAdapter()
discovery = adapter.discover("/path/to/meu-pdi")
# Retorna: stack, domain, modules, relationships, confidence
```

**Por quê:**
- Meu PDI precisa descobrir estrutura automaticamente
- Conecta com BootstrapGate 2.0 (R1.2)

**Critérios de aceitação:**
- [ ] `discover()` funciona em repositórios reais
- [ ] Descobre ≥80% da estrutura
- [ ] 80%+ test coverage
- [ ] Testes passam com Meu PDI real

**Tech Lead APOS estima:** 3 SP (implementação + testes)

---

### R1.2: Bootstrap Gate 2.0 (3 SP)

**O quê:**
- Refazer Gate para aceitar output de ProjectAdapter
- Validar usando contexto real de Meu PDI
- Auto-gerar APOS_CONFIG.yaml

**Por quê:**
- Gate 1.0 genérica (APOS fundações)
- Gate 2.0 específica (Meu PDI usando ProjectAdapter)

**Critérios de aceitação:**
- [ ] Aceita output de ProjectAdapter
- [ ] Valida usando contexto real
- [ ] Gera APOS_CONFIG.yaml
- [ ] Tests passam

**Tech Lead APOS estima:** 3 SP

---

### R1.3: Domain Ontology Adapter (2 SP)

**O quê:**
- Mapear contexto ProjectAdapter → APOS Ontology
- Criar Node/Edge types baseado em estrutura real
- Inicializar KnowledgeGraph

**Por quê:**
- "Stack: Django" descoberto → Ontology precisa entender Django
- "Domain: Trading" descoberto → Ontology precisa conceitos de trading

**Critérios de aceitação:**
- [ ] Mapeia Django models → Node types
- [ ] Mapeia relacionamentos → Edge types
- [ ] Cria KnowledgeGraph inicial
- [ ] Tests passam com Meu PDI

**Tech Lead APOS estima:** 2 SP

---

### R1.T1: Harness Coverage (3 SP)

**O quê:**
- Aumentar harness/ de 50% → 80%+ coverage
- Adicionar integration tests

**Por quê:**
- Harness é observabilidade do sistema
- 50% coverage é risco inaceitável

**Critérios de aceitação:**
- [ ] Coverage >= 80%
- [ ] Integration tests validam trust score calculation
- [ ] CI passa

**Tech Lead APOS estima:** 3 SP

---

### R1.T2: Capabilities Coverage (2 SP)

**O quê:**
- Aumentar capabilities/ de 60% → 80%+ coverage

**Critérios de aceitação:**
- [ ] Coverage >= 80%
- [ ] Routing tests com casos reais
- [ ] CI passa

**Tech Lead APOS estima:** 2 SP

---

### R1.T3: Meu PDI Observabilidade (2 SP)

**O quê:**
- Setup logging em Meu PDI
- Coletar: token count, latência, retrabalho %

**Por quê:**
- Baseline pré-APOS necessária
- Sem dados, não sabemos se APOS funciona

**Critérios de aceitação:**
- [ ] Logging setup complete
- [ ] 2 weeks baseline data collected
- [ ] Dashboard de métricas
- [ ] Ready para measurement

**PM Meu PDI estima:** 2 SP

---

## 🎬 FASE 3: Sprint Breakdown (15:00-15:45)

### Sprint 1 (Semana 1) — Foundation

**Meta:** Harness + ProjectAdapter core

```
DIA 1-2: R1.T1 (Harness Coverage)
│ └─ Aumentar testes harness de 50% → 80%
│    Owner: Tech Lead APOS
│    Acceptance: Coverage report ✓

DIA 2-3: R1.1 (ProjectAdapter Core)
│ └─ Implementar discover() functionality
│    Owner: Tech Lead APOS
│    Acceptance: Descobre ≥80% estrutura

DIA 3: R1.T2 (Capabilities Coverage)
│ └─ Aumentar coverage de 60% → 80%
│    Owner: Tech Lead APOS
│    Acceptance: Coverage report ✓

REVIEW: Sexta 16:00
│ └─ Demo: Harness tests, ProjectAdapter discovery working
│    Retro: o que funcionou, o que ajustar
```

**Sprint 1 Goals (OKRs):**
- ✅ Harness confiável (80% coverage)
- ✅ ProjectAdapter core funcional
- ✅ Discover() validado com Meu PDI (≥80%)

---

### Sprint 2 (Semana 2) — Integration

**Meta:** Bootstrap Gate 2.0 + Validação

```
DIA 4-5: R1.2 (Bootstrap Gate 2.0)
│ └─ Integrar com ProjectAdapter
│    Depends: R1.1 (ProjectAdapter) completo
│    Owner: Tech Lead APOS

DIA 5: R1.T3 (Observabilidade Setup)
│ └─ Setup logging em Meu PDI
│    Owner: PM Meu PDI
│    Acceptance: Logging ativo, dados coletados

DIA 6: E2E Integration
│ └─ ProjectAdapter → Bootstrap → Ontology
│    Owner: Tech Lead APOS + PM Meu PDI

REVIEW: Sexta 16:00
│ └─ Demo: ProjectAdapter → Bootstrap → Ontology pipeline
│    Retro: integração funcionou?
```

**Sprint 2 Goals:**
- ✅ Bootstrap Gate 2.0 operacional
- ✅ Integração E2E validada
- ✅ Observabilidade coletando dados

---

### Sprint 3 (Semana 3) — Testing + Documentation

**Meta:** R1.3 + Testes finais

```
DIA 7: R1.3 (Domain Ontology Adapter)
│ └─ Mapear contexto Meu PDI → Ontology
│    Depends: R1.1 + R1.2 + R1.T3
│    Owner: Tech Lead APOS

DIA 7-8: Integration Testing
│ └─ E2E tests (ProjectAdapter → Bootstrap → Ontology → KG)
│    Owner: Tech Lead APOS

DIA 9: Documentation
│ └─ Update docs, examples, guides
│    Owner: Tech Lead APOS + SME

REVIEW: Sexta 16:00
│ └─ Demo: Full R1 pipeline working
│    Retro: o que correu bem em R1
```

**Sprint 3 Goals:**
- ✅ Domain Ontology Adapter pronto
- ✅ Full pipeline E2E funcionando
- ✅ Documentação atualizada

---

## 📊 CAPACITY & ESTIMATION

### Team Capacity

| Pessoa | Disponibilidade | Estimativa |
|--------|-----------------|-----------|
| Tech Lead APOS | 100% | R1.1 (3 SP) + R1.2 (3 SP) + R1.3 (2 SP) + R1.T1 (3 SP) + R1.T2 (2 SP) = 13 SP |
| PM Meu PDI | 50% | R1.T3 (2 SP) |
| **TOTAL** | | **15 SP em 3 weeks** |

### Velocity Baseline (De R0)

- Código real: ~4.7 SP/h
- Documentação: ~10 SP/h
- Média: ~7.25 SP/h

**R1 Estimativa:**
- 15 SP / 7.25 SP/h = ~2h estimado
- Mas com integração real: +50% overhead
- Total: ~3 weeks (realista)

---

## 🎯 DEFINITIONS OF DONE

### Cada Sprint

**Código:**
- [ ] Testes escritos + passando
- [ ] Coverage >= mínimo (Harness: 80%, Capabilities: 80%)
- [ ] Code review aprovado
- [ ] Integração com R0 components testada

**Documentação:**
- [ ] README atualizado
- [ ] Examples funcionam
- [ ] Docstrings completos

**Validação:**
- [ ] Tests passam com Meu PDI real
- [ ] Benchmarks (se aplicável) documentados
- [ ] Performance aceitável

---

## 🚨 RISCOS & MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| ProjectAdapter discovery <80% | Média | Alto | Ter plano B (manual mapping) |
| Harness tests falham | Baixa | Médio | Tech Lead revisão extra |
| Meu PDI observabilidade bloqueada | Baixa | Médio | Simplificar pra manual logging |
| Integração E2E quebra | Média | Alto | Testes incremental, não final |

**Risk Mitigation Strategy:**
- Daily standups (15:00) — identifica blockers cedo
- Sprint reviews (sexta) — valida incrementalmente
- Tech lead + SME sempre available pra escalate

---

## 📋 PLANNING CHECKLIST

```
PRÉ-PLANNING (Fazer antes):
[ ] Todos leram R0_REALITY_CHECK.md
[ ] Todos leram R1_PLAN_REVISED.md
[ ] Todos leram PRE_R1_REALISTIC.md
[ ] Tech Lead estimou tasks
[ ] PM Meu PDI confirmou disponibilidade

PLANNING CEREMONY:
[ ] Context Setting (30 min)
  [ ] R0 reality apresentado
  [ ] ProjectAdapter status claro
  [ ] Timeline realista confirmado
[ ] Scope Deep-Dive (30 min)
  [ ] R1.1-R1.3 detalhado
  [ ] R1.T1-T3 detalhado
  [ ] Critérios de aceitação claros
[ ] Sprint Breakdown (45 min)
  [ ] Sprint 1-3 detalhado
  [ ] Dependências mapeadas
  [ ] DORs documentados
[ ] Q&A + Clarifications (15 min)
  [ ] Todos entendem escopo
  [ ] Riscos reconhecidos
  [ ] Próximos passos claro

PÓS-PLANNING:
[ ] Commitou sprint plans em git
[ ] Standup agendado (15:00 diário)
[ ] Sprint reviews agendado (sexta 16:00)
[ ] Retros agendado (fim de cada sprint)
```

---

## 📞 ESCALATION PATHS

**Se Tech Lead não consegue estimar:**
→ SME + Tech Lead + PM juntos (30 min deep-dive)

**Se ProjectAdapter parece impossível:**
→ SME: "Isso é normal, é novo. Vamos quebrar em 1-week tasks"

**Se observabilidade bloqueada em Meu PDI:**
→ PM + SME: "Simplificamos, começamos com logging manual"

**Se Sprint 1 vai passar do tempo:**
→ Scrum Master: "Movemos R1.T2 pra Sprint 2, foco em ProjectAdapter"

---

## 🎓 KEY MESSAGES PARA COMMUNIC

**1. "R0 entregou sólido. ProjectAdapter é novo."**
   - Não é "R0 falhou"
   - É "R0 fez o essencial, R1 faz ProjectAdapter"

**2. "15 SP em 3 weeks é realista."**
   - Baseado em R0 velocity real
   - Não é otimista

**3. "Sem teste piloto impossível. Focamos em build + validate."**
   - ProjectAdapter não existe, então descoberta é novo
   - Validação vem depois de implementação

**4. "Observabilidade real é crítica."**
   - Sem dados, não sabemos se APOS funciona
   - Investimento em baseline é investimento em confiança

---

## 📚 REFERÊNCIAS

```
Documentação Base:
├─ [R0_REALITY_CHECK.md](../../analysis/R0_REALITY_CHECK.md)
├─ [R1_PLAN_REVISED.md](../../analysis/R1_PLAN_REVISED.md)
├─ [PRE_R1_REALISTIC.md](../../analysis/PRE_R1_REALISTIC.md)
└─ [R1_PLANNING_GUIDE.md](this file)

Specs Técnicas:
├─ [R1/sprint-1.0/SPRINT_PLANNING.md](sprint-1.0/SPRINT_PLANNING.md)
├─ [APOS Core Docs](../../docs/)
└─ [Release Management Docs](../README.md)

Artifacts:
├─ [R0 Closure](../R0_CLOSURE.md)
├─ [INVESTOR_REPORT](../INVESTOR_REPORT.md)
└─ [Metrics Baseline](../sprint-0.3/METRICS_BASELINE.md)
```

---

**Criado:** 2026-07-21  
**Para:** R1 Planning Ceremony  
**SME:** Use esse documento pra guiar a sessão de 3h  
**Scrum Master:** Use checklist acima pra garantir cobertura completa
