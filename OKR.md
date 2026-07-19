# APOS OKRs: Visão de Produto (2026-2028)

OKRs do APOS em nível de produto. Cada release (R0-R4) contribui a esses objetivos.

Leia também:
- [NORTH_STAR.md](NORTH_STAR.md) — Visão qualitativa de longo prazo
- [PURPOSE.md](PURPOSE.md) — Por que APOS existe
- [VALUE_PROPOSITION.md](VALUE_PROPOSITION.md) — O que APOS entrega

---

## 2026: Foundation + Instantiation

### Objetivo 1: Definir Fundações Semânticas
**Por quê:** Sem ontologia formal, agentes alucinam. Precisamos de "database choice" rigoroso para contexto corporativo.

**Key Results:**
- KR1: Ontologia formal com 5 conceitos core (Task, Feature, Release, OKR, Métrica) + relações + restrições definidas
- KR2: Semantic layer com 10+ regras de negócio documentadas e validadas
- KR3: JTBD research com 20+ entrevistas confirmando job fit
- KR4: Roadmap R1-R4 estruturado e validado com stakeholders

**Como R0 entrega:** Sprint 0.0-0.3 executam cada KR.  
**Métrica:** Completude 100% (tudo documentado) + Validação 90% (stakeholders concordam)

---

### Objetivo 2: Instanciar Knowledge Graph
**Por quê:** Ontologia sozinha é teoria. Grafo conecta dados reais e prova que semântica funciona.

**Key Results:**
- KR1: 3 loaders funcionais (Jira, Notion, Slack → APOS)
- KR2: Knowledge graph com 100+ entidades instanciadas (Tasks, Features, Releases, OKRs, Metrics)
- KR3: Agentes conseguem navegar grafo semanticamente (traçar Task → Feature → OKR sem loops)
- KR4: MCP integrado (protocolo de transporte)

**Como R1 entrega:** Loaders + Knowledge Graph executor implementados.  
**Métrica:** 100% das entidades navegáveis, latência < 100ms

---

## 2027: Intelligence + Governance

### Objetivo 3: Reduzir Token Yield e Latência
**Por quê:** APOS só tem valor se reduzir o custo/tempo de agentes operarem. Triggo provou que contexto indexado = -25% tokens, -50% latência.

**Key Results:**
- KR1: Token yield reduz 25% vs busca federada (agentes raciocinam mais, adivinham menos)
- KR2: Latência de decisão reduz 50% vs manual ("qual é o impacto?" em < 5min vs 2h)
- KR3: Retrabalho reduz 85% (tasks voltam pra revisão < 5% vs ~30% hoje)
- KR4: Confiança em agentes sobe 90% (vs ~30% hoje)

**Como R2-R3 entregam:** Catálogo + Linhagem + Governança removem loops manuais.  
**Métrica:** Benchmark comparativo (busca federada vs APOS indexado)

---

### Objetivo 4: Implementar Governança Semântica
**Por quê:** Sem governança, ontologia não força alinhamento. Gates validam que implementações respeitam strategy.

**Key Results:**
- KR1: Semantic gates bloqueiam 95% de desalinhamentos antes de implementação
- KR2: Audit rules rastreiam 100% de violações de policy
- KR3: Quality metrics (token yield, latência, retrabalho) rastreadas contínuamente
- KR4: Sistema de recomendação sugere prioridades alinhadas com OKRs

**Como R3 entrega:** Gates + Audit runner + Monitoring implementados.  
**Métrica:** 0 desalinhamentos não detectados, 100% de issues auditadas

---

## 2028: Ecosystem + Market Traction

### Objetivo 5: Tornar APOS um Padrão de Mercado
**Por quê:** APOS só tem valor se times o adotarem. Ecosistem amplifica valor através de extensões comunitárias.

**Key Results:**
- KR1: SDK público com 10+ métodos de extensão
- KR2: 10+ extensões comunitárias (Sales, Support, Finance, HR ontologies)
- KR3: 1000+ downloads
- KR4: "Ontologia de PM" é considerada baseline (como "user + role" em auth)

**Como R4 entrega:** Open source + comunidade governance + shared library.  
**Métrica:** NPM/PyPI downloads, GitHub stars, community contributions

---

## Cascata: Como Releases Decompõem OKRs de Produto

```
OKR de Produto (2026): "Definir fundações semânticas"
    ↓
R0 OKR: "Defina ontologia formal, semantic layer, JTBD research"
    ↓
Sprint 0.0 OKR: "Validar job, explorar forças"
Sprint 0.1 OKR: "Definir value prop e positioning"
Sprint 0.2 OKR: "Documentar ontologia e semantic layer"
Sprint 0.3 OKR: "Estruturar roadmap R1-R4"
```

---

## Alinhamento com North Star

Cada OKR move em direção ao North Star: **"Teams visualize and reason about strategy end-to-end"**

| Ano | Foco | Como | Métrica |
|-----|------|------|---------|
| **2026** | Foundation | Ontologia + Semantic Layer | Conceitos definidos, validados |
| **2027** | Intelligence | Knowledge Graph + Governança | Token yield -25%, latência -50% |
| **2028** | Ecosystem | SDK + Comunidade | 1000+ downloads, padrão market |

---

## Métricas Globais de Sucesso (Fim de 2028)

| Métrica | Target | Atual | Impacto |
|---------|--------|-------|--------|
| **Token Yield** | -25% | Baseline | Agentes mais eficientes |
| **Latência de Decisão** | -50% | Baseline | PMs tomam decisões rápidas |
| **Retrabalho** | -85% | ~30% | Teams implementam alinhado |
| **Confiança em Agentes** | 90% | ~30% | Agentes viram confiáveis |
| **Market Adoption** | 1000+ downloads | 0 | APOS é usado por teams |

---

## Review Schedule

- **Q3 2026 (Fim R0):** Review OKRs de produto, ajustar R1
- **Q4 2026 (Fim R1):** Avaliar progresso em token yield/latência, refinar R2
- **Q2 2027 (Fim R2-R3):** Validar governança está funcionando, preparar ecosystem
- **Q3 2028 (Fim R4):** Avaliar se "ontologia de PM" é padrão

---

**Criado em:** 2026-07-19  
**Versão:** Draft  
**Próximo Review:** 2026-09-30 (Fim R0)
