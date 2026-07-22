# APOS R0: Fundações Estratégicas

**Versão:** 0.1.0-beta  
**Data de Início:** 2026-07-19  
**Status:** IN PROGRESS (Sprint 0.0 ✅ | Sprint 0.1 ✅ | Sprint 0.2 ✅ | Sprint 0.3 ✅ COMPLETA — SHIP MVP)

---

## Visão Executiva

**APOS R0 é como R0 implementa o North Star de APOS.**

Leia primeiro a estratégia do projeto:
- **[North Star](../../NORTH_STAR.md)** — Visão: "Teams visualize and reason about strategy end-to-end"
- **[Purpose](../../PURPOSE.md)** — Por quê APOS existe
- **[Value Proposition](../../VALUE_PROPOSITION.md)** — O que APOS entrega

**R0 especificamente** define as fundações (ontologia formal, semantic layer, conceitos core) que permitem que esse North Star seja alcançado.

---

## O Problema (JTBD Discovery) — Sprint 0.0 ✅ COMPLETO

**Pesquisa Realizada:** 7 personas entrevistadas (Jader Greiner PM + 6 roleplay via Hermes)  
**Consenso:** 100% em problema-raiz. Zero pivots necessários.  
**Documento:** [JOB_STATEMENT.md](sprint-0.0/JOB_STATEMENT.md)

### Segmento Validado

- Equipes pequenas (4-8 pessoas) ✅
- Distribuídas remotamente ✅
- Apagando incêndio (prioridades mudam constantemente) ✅
- Usando agentes de IA para implementação ✅

### O Job Real (Validado)

> **Quando** [PM/Agente definem trabalho sem visibilidade do contexto estratégico]  
> **Eu quero** [camada semântica viva que valida contexto antes da implementação]  
> **Para que eu possa** [evitar alucinações/regressões e parar de perder produtividade em validação]

**Contexto crítico:** Contexto DESATUALIZADO é causa de 90% dos "erros de agentes" — não alucinação clássica.

### Custo Atual (Validado contra 7 personas)

- Agentes implementam fora de domínio → retrabalho cíclico (ex: mesmo erro de login em cada deploy AWS)
- Prioridades mudam sem entender impacto + dependências invisíveis
- Team não sabe se está progredindo → Task→OKR→Métrica rastreamento é invisível
- PM re-explica contexto estratégico quase diariamente → bottleneck constante

### Alternativas Hoje (Documentado)

- Adivinhar baseado em padrões anteriores ("puro feeling" — Jader PM)
- Pedir ao PM pra cada dúvida (PM é bottleneck, "me sinto desprotegido")
- Aceitar retrabalho como inevitável ("corre atrás de problema de ontem")
- Fazer nada — continue com ciclos de debug manual

### 6 Requisitos de Produto Emergentes

1. **Validação de Contexto** — semáforo de confiança por campo (granular, não booleano)
2. **Rastreabilidade** — decisão + rota usada pelo agente visível
3. **Auto-Atualização** — contexto não fica desatualizado entre releases
4. **Versionamento de Contexto** — histórico e rollback se necessário
5. **Dependências Explícitas** — saber que Feature Y depende de Migration Z
6. **Integração Sem Fricção** — não ser "mais um CONTEXT.md com branding"

---

## A Solução: APOS

APOS é uma **camada de contexto semântico** composta por:

1. **Ontologia Formal** (R0)
   - Conceitos: Task, Feature, Release, OKR, Métrica
   - Relações: Task→Feature→Release→OKR→Métrica
   - Restrições: validações de domínio

2. **Semantic Layer** (R0-R1)
   - Regras de negócio que normalizam significado
   - "Feature em Release Y significa todas as Tasks estão na Y"
   - "OKR alcançado = todas as Métricas ≥ alvo"

3. **Knowledge Graph** (R1)
   - Dados conectados, alinhados à ontologia
   - Task-123 → Feature-X → Release-v2.1 → OKR-Churn → Métrica-LoginTime

4. **Catálogo de Dados** (R2)
   - Linhagem: "de onde vieram esses OKRs?"
   - Confiabilidade: "quanto essa métrica é confiável?"

5. **MCP** (R1-R2)
   - Conecta Jira, Notion, Slack, Spreadsheet → APOS
   - Loaders normalizam pra ontologia

---

## Estrutura de R0 (4 Sprints)

| Sprint | Foco | Resultado |
|--------|------|-----------|
| **0.0** (Semana 1) | JTBD Discovery + Problem Exploration | Validar job, entender segmento, explorar forças (Push/Pull/Anxiety/Habit) |
| **0.1** (Semana 2) | Value Prop + Positioning | Definir VALUE_PROPOSITION.md, COMPETITIVE_LANDSCAPE.md |
| **0.2** (Semana 3) | Purpose + Ontologies | Definir PURPOSE.md, ONTOLOGY_FOUNDATIONS.md (as 5 camadas) |
| **0.3** (Semana 4) | North Star + OKRs | Refinar NORTH_STAR.md, OKR.md, preparar Roadmap R1-R4 |

---

## Artefatos de R0

- **NORTH_STAR.md** — Visão de sucesso a longo prazo
- **PURPOSE.md** — Por que APOS existe
- **VALUE_PROPOSITION.md** — O que APOS entrega
- **OKR.md** — Objetivos e Key Results (R0, R1-R4, multi-ano)
- **ONTOLOGY_FOUNDATIONS.md** — As 5 camadas (Ontologia, Semantic Layer, Knowledge Graph, Catálogo, MCP)
- **COMPETITIVE_LANDSCAPE.md** — Posicionamento vs alternativas
- **ROADMAP_R1_R2_R3_R4.md** — Quebra de estratégia em releases

---

## Próximo Passo

**Sprint 0.0 inicia 2026-07-22** com **JTBD Discovery** usando Jobs-to-be-Done Framework (wondelai/skills).

Objetivo: Validar o job real, explorar forças, mapear competitive landscape.

Output: `sprint-0.0/JTBD_RESEARCH.md`

---

## Contexto: Por Que R0 Importa

APOS não é um projeto técnico. É uma **decisão arquitetural estratégica** (equivalente à escolha de um banco de dados para sistemas críticos).

Referências:
- Triggo.ai: "Ontologia, Semantic Layer e Knowledge Graph" (Cap 2.2)
- Gartner 2026: Projetos de analytics agêntico que usam só MCP (sem ontologia) falham em produção
- SNYK/Triggo: Token yield aumenta 25%, latência reduz 50% com contexto indexado

**APOS aplica esses princípios a Product Management.**

---

**Autor:** Jader Greiner  
**Stakeholder Principal:** Jader Greiner (jadergreiner@gmail.com)  
**Equipe:** APOS Core Team
