# APOS R0 OKRs: Decomposição de OKRs de Produto

## Hierarquia de OKRs

```
APOS/OKR.md (Produto - 2026-2028)
    ↓
docs/releases/R0/OKR.md (Release - 2026-Q3) ← Você está aqui
    ↓
sprint-0.0/TASKS.md (Sprint - Semana 1)
sprint-0.1/TASKS.md (Sprint - Semana 2)
sprint-0.2/TASKS.md (Sprint - Semana 3)
sprint-0.3/TASKS.md (Sprint - Semana 4)
```

**Leia antes:** [APOS/OKR.md](../../OKR.md) — OKRs de produto (2026-2028)

R0 é responsável por entregar os primeiros dois OKRs de produto:
1. **Definir fundações semânticas** (ontologia, semantic layer, JTBD)
2. **Instanciar knowledge graph** (começa em R1, mas preparado em R0)

---

## R0 OKRs: Fundações (2026-Q3)

### Objetivo 1: Definir Ontologia Formal
**Descrição:** Especificar formalmente os 5 conceitos core de Product Management e suas relações.

**Key Results:**
- KR1: 5 conceitos core definidos (Task, Feature, Release, OKR, Métrica) com propriedades e restrições
- KR2: Relações entre conceitos mapeadas (Task→Feature→Release→OKR→Métrica)
- KR3: Restrições de domínio documentadas (ex: "Task não pode estar em 2 Features")
- KR4: Validação: agente consegue raciocinar sobre cadeia sem pergunta ad-hoc

**Resultado:** `docs/releases/R0/ONTOLOGY_FOUNDATIONS.md`

---

### Objetivo 2: Definir Semantic Layer (Regras de Negócio)
**Descrição:** Codificar regras que normalizam significado entre domínios.

**Key Results:**
- KR1: 10+ regras de negócio documentadas (ex: "Feature em Release Y = todas Tasks em Release Y")
- KR2: Ambiguidades resolvidas ("O que significa 'OKR alcançado'?")
- KR3: Validação rules implementadas (ex: "OKR precisa ter Métrica")
- KR4: Team consegue aplicar rules sem perguntar

**Resultado:** `docs/releases/R0/ONTOLOGY_FOUNDATIONS.md` + `docs/releases/R1/SEMANTIC_LAYER_SPEC.md`

---

### Objetivo 3: Validar Job Fit (JTBD) ✅ COMPLETO

**Descrição:** Confirmar que ontologia resolve o job real de equipes pequenas distribuídas.

**Key Results:**

- ✅ KR1: **7 JTBD interviews** com equipes (meta 10+, superado com roleplay)
- ✅ KR2: **Job statement validado** — 100% consenso, zero pivots maiores
- ✅ KR3: **Forças de progresso mapeadas** — Push/Pull/Ansiedade/Hábito consolidadas
- ✅ KR4: **Competitive landscape documentado** — 6 requisitos de produto emergentes

**Status:** ✅ COMPLETO (Sprint 0.0, 19 jul)  
**Resultado:** [JOB_STATEMENT.md](sprint-0.0/JOB_STATEMENT.md) + [FORCES_ANALYSIS.md](sprint-0.0/FORCES_ANALYSIS.md)

**Descobertas Chave:**

- **Problem Root:** Contexto desatualizado = 90% de "erros de agentes"
- **100% Consenso:** Todos 7 personas aligned no job statement
- **Emergent Requirements:** Validação, Rastreabilidade, Auto-Atualização, Versionamento, Dependências, Integração sem fricção

**Resultado:** `docs/releases/R0/sprint-0.0/JTBD_RESEARCH.md`

---

### Objetivo 4: Estruturar Roadmap R1-R4
**Descrição:** Quebrar estratégia em releases concretas com deliverables.

**Key Results:**
- KR1: R1 roadmap definido (Knowledge Graph instanciação)
- KR2: R2 roadmap definido (Catálogo + Linhagem)
- KR3: R3 roadmap definido (Governança + Gates)
- KR4: R4 roadmap definido (Ecosystem + Integrações)

**Resultado:** `docs/releases/R0/ROADMAP_R1_R2_R3_R4.md`

---

## Métricas de Sucesso de R0

| Métrica | Target | Medida |
|---------|--------|--------|
| **Clarity of Ontology** | 95% | Team consegue explicar 5 conceitos sem documentação |
| **Semantic Layer Completeness** | 100% | 10+ rules documentadas e validadas |
| **JTBD Validation** | 90% | Job statement valida em 9 de 10 interviews |
| **Roadmap Confidence** | 85% | Team confia que R1-R4 implementam North Star |
| **Stakeholder Alignment** | 90% | Stakeholders concordam com estratégia |

---

## Roadmap R1-R4 (Visão de Alto Nível)

### R1: Instanciação + Transporte (2026-Q4)
- **Objetivo:** Instanciar knowledge graph real
- **Deliverables:**
  - Knowledge Graph executor (conectar Task-123 → Feature-X → Release-v2.1)
  - Loaders para Jira, Notion, Slack
  - MCP integrado
- **OKRs:**
  - KR1: 3 loaders funcionais (Jira, Notion, Slack)
  - KR2: Knowledge graph com 100+ entidades instanciadas
  - KR3: Agentes conseguem navegarem grafo semanticamente

---

### R2: Inteligência + Rastreabilidade (2027-Q1)
- **Objetivo:** Catálogo + Linhagem + Navegação automática
- **Deliverables:**
  - Data catalog (inventário de linhagem)
  - Impact analysis ("se mudo isso, quebra aquilo?")
  - Semantic reasoning (agente navegue sem guia)
- **OKRs:**
  - KR1: Catálogo com linhagem completa
  - KR2: Impact analysis em < 5 min (vs 2h manual)
  - KR3: Agentes navegam grafo sem loops

---

### R3: Governança (2027-Q2)
- **Objetivo:** Validação + Auditoria + Compliance
- **Deliverables:**
  - Semantic gates (valida alinhamento automaticamente)
  - Audit rules (política de negócio)
  - Quality metrics (token yield, latência)
- **OKRs:**
  - KR1: Gates bloqueiam 95% de desalinhamentos
  - KR2: Auditoria rastreia todas violações
  - KR3: Token yield reduz 25%, latência reduz 50%

---

### R4: Ecosystem (2027-Q3)
- **Objetivo:** Open source + Comunidade + Extensibilidade
- **Deliverables:**
  - SDK público
  - Extensões de domínio (Sales, Support, Finance)
  - Shared ontology library
- **OKRs:**
  - KR1: 10+ extensões comunitárias
  - KR2: 1000+ downloads
  - KR3: "Ontologia de PM" é padrão de mercado

---

## Alinhamento com North Star

Cada release move em direção ao North Star:

```
NORTH STAR: "Teams visualize and reason about strategy end-to-end"
    ↓
R0: Defina o que "end-to-end" significa (ontologia + semantic layer)
R1: Instancie dados reais (knowledge graph)
R2: Permita raciocínio automático (inteligência + linhagem)
R3: Valide alinhamento (governança)
R4: Escale com comunidade (ecosystem)
```

---

**Criado em:** 2026-07-19  
**Versão:** Draft  
**Próximo Review:** Sprint 0.3 (OKRs refinados com feedback de R0.0-R0.2)
