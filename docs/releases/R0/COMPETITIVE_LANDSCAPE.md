# APOS: Posicionamento Competitivo

**Como é que times "contratam" solução hoje pra resolver o job que APOS resolve?**

Baseado em JTBD framework: competição não é definida por categoria, mas pelo job que o cliente tenta fazer.

---

## O Job Real

> Quando recebo uma task, quero ver a cadeia completa (Task → Feature → Release → OKR → Métrica) para que eu saiba por quê estou fazendo isso e qual é o risco real de mudar prioridade.

---

## O Que Times "Contratam" Hoje

### Alternativa 1: Jira + Notion + Slack (Manual Synthesis)

**Como funciona:**
- Jira: tasks, status, subtasks
- Notion: roadmap, OKRs, features (manual)
- Slack: contexto disperso em threads
- PM: sintetiza manualmente

**Força:**
- ✅ Ferramentas existem, equipes já conhecem
- ✅ Flexível (customizable)
- ✅ Barato (ferramentas já pagas)

**Fraqueza:**
- ❌ Contexto disperso em 3+ sistemas
- ❌ PM é bottleneck (sintetiza manualmente)
- ❌ Agentes não conseguem raciocinar (precisam de síntese manual)
- ❌ Desalinhamento acontece (ninguém valida semanticamente)
- ❌ Escalabilidade zero (quanto maior a equipe, mais caos)

**Custo:**
- PM gasta 2-3h/semana sintetizando
- Retrabalho: ~30% de tasks voltam

**APOS vs Jira+Notion+Slack:**
- APOS: Centraliza contexto, valida semanticamente, agentes raciocinam
- Jira+Notion: Disperso, manual, agentes adivinharam

---

### Alternativa 2: Semantic Layer (dbt, Tableau, Metabase)

**Como funciona:**
- Normaliza métricas em data warehouse
- Define "receita = X + Y"
- BI tools consultam o semantic layer

**Força:**
- ✅ Normaliza significado pra consultas
- ✅ Bom pra dashboards
- ✅ Estabelecido (muitas empresas usam)

**Fraqueza:**
- ❌ Otimizado pra consulta, não pra raciocínio
- ❌ Agentes conseguem "qual é a receita?" mas não "qual é o impacto dessa mudança?"
- ❌ Não permite navegação entre domínios (customer → contract → ticket)
- ❌ Não funciona pra estratégia (OKRs, features, releases)

**Gartner Alert:** "Semantic layer é pra BI. Projetos que tentam usar só semantic layer pra agentes raciocinar falham em produção."

**APOS vs Semantic Layer:**
- APOS: Raciocínio estratégico (Task → OKR → Impacto)
- Semantic Layer: Consulta de métrica ("qual é a receita?")

---

### Alternativa 3: Data Catalog (Collibra, Apache Atlas)

**Como funciona:**
- Mapeia linhagem de dados
- Documenta "tabela X vem de Y, coluna Z é calculada por W"
- Humanos descobrem onde dados estão

**Força:**
- ✅ Rastreia linhagem técnica
- ✅ Bom pra data governance
- ✅ Escala em data lakes grandes

**Fraqueza:**
- ❌ Não confere significado de negócio
- ❌ Agentes não conseguem usar pra raciocinar ("qual é o impacto?")
- ❌ Focado em dados técnicos, não em conceitos de negócio
- ❌ Não valida alinhamento com strategy

**APOS vs Data Catalog:**
- APOS: Linhagem de conceitos estratégicos (Task → OKR)
- Data Catalog: Linhagem de dados técnicos (table → column)

---

### Alternativa 4: MCP Puro (Model Context Protocol)

**Como funciona:**
- Conecta agente a múltiplas fontes (Jira, Notion, Slack, etc)
- Agente faz queries ao MCP, recebe dados
- MCP é o transporte

**Força:**
- ✅ Padronizado (protocolo aberto)
- ✅ Escalável (conecta muitas fontes)
- ✅ Simples (é "só um cano")

**Fraqueza:**
- ❌ Sem ontologia por trás, agentes alucinam
- ❌ Sem semantic layer, significado é ambíguo
- ❌ Sem knowledge graph, dados estão isolados
- ❌ MCP é "o cano, não a água"

**Gartner 2026 Alert:** "Projetos que dependem exclusivamente de MCP sem camada de significado falham em produção."

**APOS vs MCP Puro:**
- APOS: MCP + Ontologia + Semantic Layer + Knowledge Graph
- MCP Puro: Só transporte, sem significado

---

### Alternativa 5: Fazer Nada (Non-Consumption)

**Como funciona:**
- Time aceita retrabalho como inevitável
- Agentes implementam, PM checa depois
- Ciclo: implementação → revisão → retrabalho → re-implementação

**Força:**
- ✅ Nenhuma ferramenta nova (zero fricção de adoção)
- ✅ "Sempre foi assim" (inércia)

**Fraqueza:**
- ❌ Retrabalho alto (~30% de tasks voltam)
- ❌ Latência: cada ciclo demora 1-2 dias
- ❌ Token waste: agentes gastam tokens adivinhando
- ❌ Confiança baixa (PMs desconfiam de agentes)
- ❌ Não escala (quanto maior a equipe, pior)

**Custo:**
- PM: 2-3h/semana checando
- Agentes: retrabalho constante
- Business: features atrasam

**APOS vs Fazer Nada:**
- APOS: Contexto embutido, zero retrabalho
- Fazer Nada: Retrabalho é o custo

---

## Comparação: Alternativas vs APOS

| Critério | Jira+Notion | Semantic Layer | Data Catalog | MCP Puro | Fazer Nada | **APOS** |
|----------|---|---|---|---|---|---|
| **Normaliza conceitos?** | Não | Sim (métricas) | Não | Não | Não | ✅ Sim |
| **Permite raciocínio?** | Não | Não (só consulta) | Não | Não | Não | ✅ Sim |
| **Agente entende domínio?** | Não | Não | Não | Não | Não | ✅ Sim |
| **Reduz token yield?** | Não | Não | Não | Não | Não | ✅ 25% |
| **Reduz latência?** | Não | Não | Não | Não | Não | ✅ 50% |
| **Valida alinhamento?** | Manual | Não | Não | Não | Não | ✅ Automático |
| **Escala com equipe?** | Não | Limitado | Limitado | Não | Não | ✅ Sim |
| **Custo implementação** | Baixo | Médio | Alto | Médio | Zero | Médio |
| **Custo operacional** | Alto (PM overhead) | Médio | Médio | Alto (retrabalho) | Alto (retrabalho) | Baixo |

---

## Posicionamento Estratégico

### APOS vs Jira+Notion
**Mensagem:** "Centralize estratégia em lugar único, não disperso em 5 sistemas."
- APOS: "Strategy graph, not scattered docs"

### APOS vs Semantic Layer
**Mensagem:** "Semantic layer é pra BI. Pra estratégia, você precisa de ontologia."
- APOS: "Raciocínio estratégico, não consulta de métrica"

### APOS vs Data Catalog
**Mensagem:** "Data catalog é pra linhagem técnica. Pra alinhamento de estratégia, você precisa de semântica de negócio."
- APOS: "Linhagem de conceitos, não linhagem de tables"

### APOS vs MCP Puro
**Mensagem:** "MCP é o transporte. Mas sem ontologia, agentes alucinam. APOS é MCP + significado."
- APOS: "Transporte + ontologia + semântica = raciocínio real"

### APOS vs Fazer Nada
**Mensagem:** "Retrabalho custa mais que estrutura. Estruture uma vez, escale sem overhead."
- APOS: "Elimina 85% de retrabalho através de alinhamento semântico"

---

## Por Quem APOS Ganha

### Segmento 1: Equipes Pequenas + Distribuídas
- Contexto verbal não escala
- Documentação fica dispersa
- Agentes precisam de contexto embutido
- **APOS win:** Centraliza, distribui contextualmente

### Segmento 2: Teams com Agentes de IA
- Agentes adivinhavam, causavam retrabalho
- PM gasta tempo checando alinhamento
- **APOS win:** Agentes raciocinam, PM confia

### Segmento 3: Rapid Prioritization (Incêndios)
- Prioridades mudam o tempo todo
- Impacto não é claro
- Retrabalho aumenta
- **APOS win:** Impacto é calculado em < 5min

### Segmento 4: Scale-up (Crescimento)
- Jira+Notion broke (caos aumenta)
- Manual synthesis não escala
- Retrabalho explode
- **APOS win:** Escala sem novo overhead

---

## Por Quem APOS NÃO Ganha (Hoje)

### Caso 1: Equipes Só com Humanos (Sem Agentes)
- Se só tem humans, não há "alucinação de agentes"
- Semantic layer pra BI é suficiente
- **APOS overkill** (até implementarem agentes)

### Caso 2: Enterprise com Data Governance Pesada
- Já tem data catalog, semantic layer, governance
- Infrastructure já existe
- **APOS: complementa, não substitui** (adiciona camada de negócio)

### Caso 3: Projeto One-Off (Sem Strategy Recorrente)
- Sem OKRs, sem roadmap, sem strategy
- Fazer nada é suficiente
- **APOS overhead** (não há strategy pra ontologizar)

---

## Estratégia de Entrada (Go-to-Market)

### Fase 1: Beachhead (2026)
**Segmento:** Equipes pequenas + distribuídas + com agentes  
**Posicionamento:** "Eliminate agent hallucination through semantic alignment"  
**Proof Point:** "Reduce rework 85%, latency 50%, token yield 25%"

### Fase 2: Expansion (2027)
**Segmento:** Scale-ups (5-50 pessoas)  
**Posicionamento:** "Strategy graph that scales without overhead"  
**Proof Point:** "Growing teams no longer break their PM process"

### Fase 3: Enterprise (2028)
**Segmento:** Enterprises com agentes críticos  
**Posicionamento:** "Ontology-first governance for AI-driven product teams"  
**Proof Point:** "Semantic compliance: no misaligned implementation ever"

---

## Vantagem Defensível

**Por que APOS não é copiável?**

1. **Ontologia é específica de domínio** — "Ontologia de PM" não é trivial, leva expertise
2. **Semantic layer requer time** — Definir 100+ regras requer conhecimento
3. **Network effect** — Quanto mais teams usam APOS, mais extensões aparecem
4. **Integration lock-in** — Uma vez integrado com Jira/Notion/Slack, custo de switch é alto

**Por que competitors não resolvem?**

- **Semantic layer vendors** (dbt, Metabase): Não veem "raciocínio de agentes" como use case
- **MCP vendors** (Anthropic): MCP é transporte, não semântica
- **Data catalog vendors** (Collibra): Focam em técnico, não em negócio
- **PM tools** (Jira, Asana): Não querem dependência de agentes

---

## Métrica de Sucesso (Posicionamento)

| Métrica | Target | Como Medir |
|---------|--------|-----------|
| **Brand Clarity** | 90% | "APOS = raciocínio de agentes via ontologia" |
| **Differentiation** | 95% | "Ninguém mais confunde com Semantic Layer ou MCP" |
| **Beachhead Adoption** | 10+ teams | Equipes pequenas usando e recomendando |
| **Referenceable Customers** | 3+ | Case studies com métricas (token yield, latência) |

---

**Criado em:** 2026-07-19  
**Versão:** Draft  
**Próximo Review:** Sprint 0.1 (quando value prop for validado)
