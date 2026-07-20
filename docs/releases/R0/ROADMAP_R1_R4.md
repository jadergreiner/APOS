# APOS Roadmap: R1-R4 (2026-2027)

**Release:** R0 → R1-R4  
**Período:** Set 2026 - Jun 2027  
**Status:** PLANEJAMENTO (Sprint 0.1 Task T0.1.4)  
**Criado:** 20-07-2026 (Template)

---

## Visão Estratégica

Cada release move em direção ao North Star: **"Times visualizam e raciocinam sobre estratégia de ponta a ponta"**

```
R0 (Jul-Sep 2026): Fundações semânticas ✅
    ↓
R1 (Sep-Nov 2026): Instanciar Knowledge Graph + Loaders
    ↓
R2 (Nov 2026-Jan 2027): Catálogo + Linhagem + Inteligência
    ↓
R3 (Jan-Mar 2027): Governança + Auditoria + Compliance
    ↓
R4 (Mar-Jun 2027): Ecossistema + Comunidade + Go-to-Market
```

---

## R1: Instanciação + Transporte (Sep-Nov 2026)

**Objetivo:** Instanciar knowledge graph real, conectando dados de Jira/Notion/Slack

**Key Results:**
- KR1: 3 loaders funcionais (Jira, Notion, Slack)
- KR2: Knowledge graph com 100+ entidades instanciadas
- KR3: Agentes conseguem navegarem grafo semanticamente

**Temas de Sprint:**
- S1.0: Knowledge Graph Executor (núcleo)
- S1.1: Jira Loader
- S1.2: Notion Loader
- S1.3: Slack Loader + MCP integration

**Effort:** ~20 person-days  
**Dependencies:** R0 COMPLETE (fundações)

---

## R2: Inteligência + Rastreabilidade (Nov 2026-Jan 2027)

**Objetivo:** Catálogo + Linhagem + Navegação automática

**Key Results:**
- KR1: Catálogo com linhagem completa
- KR2: Impact analysis em < 5 min (vs 2h manual)
- KR3: Agentes navegam grafo sem loops

**Temas de Sprint:**
- S2.0: Data Catalog Schema
- S2.1: Lineage Tracing Engine
- S2.2: Impact Analysis CLI
- S2.3: Agent Navigation Harness

**Effort:** ~18 person-days  
**Dependencies:** R1 loaders operacionais

---

## R3: Governança (Jan-Mar 2027)

**Objetivo:** Validação + Auditoria + Compliance

**Key Results:**
- KR1: Gates bloqueiam 95% de desalinhamentos
- KR2: Auditoria rastreia todas violações
- KR3: Token yield reduz 25%, latência reduz 50%

**Temas de Sprint:**
- S3.0: Semantic Gates (validação automática)
- S3.1: Audit Rules + Log Engine
- S3.2: Compliance Frameworks
- S3.3: Observability Dashboard

**Effort:** ~20 person-days  
**Dependencies:** R2 catálogo operacional

---

## R4: Ecosystem (Mar-Jun 2027)

**Objetivo:** Open source + Comunidade + Extensibilidade

**Key Results:**
- KR1: 10+ extensões comunitárias
- KR2: 1000+ downloads
- KR3: "Ontologia de PM" é padrão de mercado

**Temas de Sprint:**
- S4.0: SDK Público + Documentação
- S4.1: Extensões de Domínio (Sales, Support, Finance)
- S4.2: Shared Ontology Library
- S4.3: Go-to-Market + Comunidade

**Effort:** ~18 person-days  
**Dependencies:** R1-R3 estáveis

---

## Timeline Visual (Gantt Simplificado)

```
2026:
  JUL |████ R0.0 ████ R0.1 ████ R0.2 ████ R0.3 | (Sprint 0.0-0.9)
  SEP |  ████ R1.0 ████ R1.1 ████ R1.2 ████ R1.3 |
  NOV | ████ R2.0 ████ R2.1 ████ R2.2 ████ R2.3 |

2027:
  JAN | ████ R3.0 ████ R3.1 ████ R3.2 ████ R3.3 |
  MAR | ████ R4.0 ████ R4.1 ████ R4.2 ████ R4.3 |
  JUN | ✅ COMPLETE
```

---

## Caminho Crítico

**Série:** R0 → R1 → R2 → R3 → R4 (dependência linear)

**Pontos de Risco:**
1. R0 delay → cascata (mitigação: S0.0 mostrou velocity +250%)
2. R1 loaders complexity → R2 agendado (mitigação: parallelization possível S1.1-1.3)
3. R3 gates rigor → customer adoption (mitigação: graduação de restrições)

---

## Restrições de Recursos

**Capacity:** 1 person-time (Jader + Claude Sonnet 5)

**Distribuição:**
- R1-R4: ~76 person-days total (~18 person-days/release)
- Timeline: 12 semanas (18 semanas de esforço, 4 sprints/release)
- Paralelização: S1.1-1.3 (Loaders) podem ser paralelos (~10% economia)

**Pressupostos:**
- Nenhum context switching entre releases
- Velocity 1.5x baseado em S0.0 learning
- Buffer de 20-30% para riscos imprevistos

---

## Métricas de Sucesso

| Release | Métrica-Chave | Target | Validação |
|---------|---------------|--------|-----------|
| **R1** | 3 loaders operacionais | 100% | Testes de integração |
| **R2** | Impact analysis latência | < 5 min | Benchmark suite |
| **R3** | Gates blocking rate | 95% | Audit logs |
| **R4** | Community extensions | 10+ | GitHub contributions |

---

## Decisões Arquiteturais

### Implementação em Fases

1. **R1:** Grafo em memória (MVP, não persistente)
2. **R2:** Adição de storage (PostgreSQL/Neo4j)
3. **R3:** Governança integrada (não retrofit)
4. **R4:** Extensibilidade via plugins

### Priorização de Loaders

**R1.0:** Jira (maior base de usuários)  
**R1.1:** Notion (flexibilidade)  
**R1.2:** Slack (contexto social)

---

## Go-to-Market Timeline

| Milestone | Timing | Atividade |
|-----------|--------|-----------|
| **Beta** | R1 end | Invite 5-10 early users |
| **Alpha** | R2 end | Expand to 50+ beta users |
| **GA** | R4 end | Public launch + community |

---

## Próximas Etapas

- [ ] Sprint 0.1 (T0.1.4): Detalhar R1-R4 sprints e dependências
- [ ] Sprint 0.2+: Validar roadmap contra ontologia + restrições técnicas
- [ ] Sprint 0.9: Aprovação formal + kickoff R1

---

**Versão:** 1.0 (Template)  
**Próximo Review:** Sprint 0.3 (refinement com ontologia validada)
