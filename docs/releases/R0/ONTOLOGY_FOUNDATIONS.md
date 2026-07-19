# APOS: As 5 Camadas de Contexto Semântico

Referência: [Triggo.ai Cap 2.2](https://triggo.ai/pt/ebook/ontologia-contexto) — "Ontologia, Semantic Layer e Knowledge Graph: Por Que a Confusão de Termos Importa"

**Este documento define as 5 camadas que compõem a solução APOS.**

---

## Por Que Diferenciar as 5 Camadas?

**Problema:** Muitos projetos de "AI agêntica" misturam esses conceitos e falham em produção.

**Gartner 2026:** Projetos que dependem exclusivamente de protocolos de transporte (MCP) sem camada de significado falham.

**Triggo observação:** Confundir Semantic Layer (consulta) com Ontologia (raciocínio) é causa recorrente de falha.

**APOS solução:** Diferenciar explicitamente cada camada e sua responsabilidade.

---

## Camada 1: Ontologia (Especificação Formal)

### O Que É
Especificação formal dos **conceitos, relações e restrições** do domínio de negócio (Product Management).

### O Que Resolve
- ✅ Dá ao agente a capacidade de **raciocinar** — entender o que as coisas são e como se relacionam
- ✅ Define fronteiras semânticas — "isso pertence ao domínio, aquilo não"
- ✅ Valida estrutura — restrições impedem estados inválidos

### O Que NÃO Resolve
- ❌ Não calcula métricas (isso é semantic layer)
- ❌ Não garante governança sozinha (isso é governance layer, R3)
- ❌ Não conecta dados reais (isso é knowledge graph)

### Conceitos Core de APOS

| Conceito | Definição | Exemplo |
|----------|-----------|---------|
| **Task** | Unidade atômica de trabalho que contribui exatamente a 1 Feature | "Implement OAuth login" |
| **Feature** | Agrupamento de Tasks entregue em exatamente 1 Release | "Faster Authentication" |
| **Release** | Versão de software entregue em data específica, alcança N OKRs | "v2.1 (July 2026)" |
| **OKR** | Objetivo estratégico com Key Results mensuráveis | "Reduce churn 5%" |
| **Métrica** | Indicador de sucesso que mede OKR | "Login time < 2s" |

### Relações de Ontologia

```
Task ─contribui_para→ Feature
      (1:1 ou N:1?)    (constraints: cada Task em exatamente 1 Feature)

Feature ─parte_de→ Release
        (N:1)      (constraints: todos Tasks da Feature na mesma Release)

Release ─alcança→ OKR
       (N:M)     (constraints: Release pode alcançar múltiplos OKRs)

OKR ─medido_por→ Métrica
   (1:M)        (constraints: OKR precisa ter ≥1 Métrica)

Task ─impacta→ Métrica
     (N:M)    (inferência: Task afeta Métrica via Feature→Release→OKR)

Task ─bloqueia→ Task (opcional, dependencies)
     (N:M)
```

### Restrições de Ontologia

```
Task:
  - contribui_para: NOT NULL, UNIQUE (cada Task em 1 Feature)
  - status: IN ('open', 'in_progress', 'done', 'blocked')

Feature:
  - parte_of: NOT NULL (toda Feature em 1 Release)
  - name: UNIQUE (não há 2 features com mesmo nome)

Release:
  - version: UNIQUE (não há 2 releases com mesma versão)
  - date: NOT NULL, FUTURE (release é futura ou em progresso)
  - alcança: NOT EMPTY (release deve alcançar ≥1 OKR)

OKR:
  - medido_por: NOT EMPTY (OKR precisa de ≥1 Métrica)
  - alvo: NOT NULL, QUANTIFICADO (target numérico)

Métrica:
  - unidade: NOT NULL (%, horas, count, etc)
  - alvo: NOT NULL (qual é o target?)
  - data_avaliacao: NOT NULL (quando medimos?)
```

### Responsabilidade de R0

**R0 entrega:**
- [x] Conceitos core formalizados (Task, Feature, Release, OKR, Métrica)
- [x] Relações mapeadas
- [x] Restrições documentadas
- [x] Validação: agentes conseguem raciocinar sobre cadeia

**Saída:** `docs/releases/R0/ONTOLOGY_SPEC.md` (detalhe completo)

---

## Camada 2: Semantic Layer (Normalização de Significado)

### O Que É
Camada de abstração que **normaliza significado** através de regras de negócio.

Garante que um termo significa a mesma coisa em todo o sistema, independente da fonte.

### O Que Resolve
- ✅ Ambiguidade: "Feature em Release v2.1" sempre significa a mesma coisa
- ✅ Conflitos: Múltiplas fontes (Jira, Notion, Slack) têm semântica unificada
- ✅ Cálculos: "OKR alcançado" = métrica ≥ alvo (definição explícita)

### O Que NÃO Resolve
- ❌ Não permite raciocínio inter-domínios (isso é ontologia)
- ❌ Não conecta dados reais (isso é knowledge graph)
- ❌ Não governa (isso é governance layer)

### Regras de Semantic Layer (APOS)

#### Regra 1: Feature em Release = Todas Tasks em Release
```
IF Feature F é parte_of Release R
THEN todos os Tasks em F devem ter Release = R
ELSE: Inconsistência! (Task referencia Feature em Release Y, mas Feature está em Release X)
```

#### Regra 2: OKR Alcançado = Métrica ≥ Alvo
```
OKR.alcançado = AND(
  FOR cada Métrica M em OKR.medido_por:
    M.valor_atual >= M.alvo
)
```

#### Regra 3: Release Completa = Todos OKRs Alcançados
```
Release.status = 'completa' 
  IFF todos os OKRs que a Release alcança estão 'alcançados'
```

#### Regra 4: Task Bloqueada = Bloqueia Métrica Relacionada
```
IF Task T tem status='blocked'
THEN qualquer Métrica afetada por T tem flag='at_risk'
```

#### Regra 5: Mudança de Prioridade = Recalcular Impacto
```
WHEN Task T muda de Release de R1 para R2:
  RECALCULATE: impacto_em(OKR_de_R1), impacto_em(OKR_de_R2)
  ALERT: "Task move impacts these OKRs: [list]"
```

### Responsabilidade de R0

**R0 entrega:**
- [x] 10+ regras de negócio documentadas
- [x] Ambiguidades resolvidas
- [x] Validação rules especificadas
- [x] Team consegue aplicar rules sem perguntar

**Saída:** `docs/releases/R0/SEMANTIC_LAYER_SPEC.md`

---

## Camada 3: Knowledge Graph (Dados Conectados)

### O Que É
Instância de **dados conectados e alinhados à ontologia**, com identificadores únicos.

Permite navegação e inferência sobre relações reais entre entidades.

### O Que Resolve
- ✅ Materialização: Ontologia se torna grafo real de dados
- ✅ Navegação: Task-123 → Feature-X → Release-v2.1 → OKR-Churn → Métrica-LoginTime
- ✅ Inferência: "Se mudo Task-123, qual Métrica é afetada?"

### O Que NÃO Resolve
- ❌ Sem ontologia por trás, vira "apenas uma rede de dados sem significado formal"
- ❌ Não garante qualidade de dados (isso é governance)
- ❌ Não conecta múltiplas fontes (isso é loaders + MCP)

### Estrutura de Knowledge Graph (APOS)

```
Task-123 (Implement OAuth)
  ├─ id: "task-123"
  ├─ contribui_para: Feature-X
  ├─ impacta: [Métrica-LoginTime]
  ├─ parte_de: Sprint-0.1
  ├─ status: "in_progress"
  └─ owner: "agent-oauth"

Feature-X (Faster Auth)
  ├─ id: "feature-x"
  ├─ parte_de: Release-v2.1
  ├─ alcança: OKR-Churn-5%
  ├─ tasks: [Task-123, Task-124, ...]
  └─ completeness: 0.75

Release-v2.1 (July 2026)
  ├─ id: "release-v2.1"
  ├─ version: "2.1.0"
  ├─ features: [Feature-X, Feature-Y, ...]
  ├─ alcança: [OKR-Churn-5%, OKR-Performance-10%]
  └─ date: "2026-07-31"

OKR-Churn-5% (Reduce Churn 5%)
  ├─ id: "okr-churn-5"
  ├─ objetivo: "Reduce customer churn"
  ├─ alcançado_por: [Release-v2.1, Feature-X]
  ├─ medido_por: Métrica-Churn
  └─ alvo: 5.0

Métrica-LoginTime (Login < 2s)
  ├─ id: "metric-login-time"
  ├─ unidade: "segundos"
  ├─ alvo: 2.0
  ├─ valor_atual: 2.5
  ├─ impactada_por: [Task-123, Feature-X, Release-v2.1]
  └─ status: "at_risk"
```

### Responsabilidade de R0 vs R1

**R0:** Prepara estrutura (define nós, arestas, identificadores únicos)  
**R1:** Instancia dados reais (popula grafo com 100+ entidades)

---

## Camada 4: Catálogo de Dados (Linhagem)

### O Que É
Inventário de metadados técnicos: de onde vieram os dados, quando foram atualizados, qual é a qualidade.

### O Que Resolve
- ✅ Rastreabilidade: "OKRs vêm de spreadsheet X, atualizado por PM Y em 2026-07-15"
- ✅ Confiabilidade: "essa métrica é calculada de sistema Z, confiabilidade 95%"
- ✅ Lineage: Task foi criada em Jira, movida pra Notion, sincronizada em APOS

### O Que NÃO Resolve
- ❌ Não confere significado de negócio (isso é ontologia)
- ❌ Não garante que dados estão corretos (isso é governança)

### Catálogo de APOS (Estrutura)

```
OKR-Churn-5%:
  source: "spreadsheet:Google Sheets#1abc23"
  last_updated: "2026-07-19 15:30 UTC"
  updated_by: "jader@company.com"
  sync_frequency: "daily"
  quality: 0.95
  
Métrica-LoginTime:
  source: "datawarehouse:Snowflake.analytics.metrics"
  calculation: "SELECT AVG(login_duration_ms) / 1000 FROM events WHERE ..."
  last_calculated: "2026-07-19 10:00 UTC"
  quality: 0.98
  
Task-123:
  created_in: "jira:PROJ-456"
  moved_to: "notion:MyDatabase#7xyz"
  synced_to: "apos:task-123"
  last_synced: "2026-07-19 14:15 UTC"
  sync_status: "active"
```

### Responsabilidade de R0 vs R2

**R0:** Define estrutura de catálogo  
**R2:** Implementa catálogo com linhagem completa

---

## Camada 5: MCP (Protocolo de Contexto)

### O Que É
Protocolo aberto de transporte de contexto entre sistemas e agentes.

**Metáfora:** "O cano, não a água" — conecta fontes, mas não produz significado.

### O Que Resolve
- ✅ Transporte: Jira → APOS, Notion → APOS, Slack → APOS via protocolo unificado
- ✅ Padronização: Mesmo protocolo pra todas as fontes

### O Que NÃO Resolve
- ❌ Não produz significado (sem ontologia por trás = apenas "cano")
- ❌ Não normaliza dados (sem semantic layer = ambiguidade)
- ❌ Não conecta dados (sem knowledge graph = isolados)

### MCP em APOS

**Loaders implementam MCP:**

```
Jira Loader:
  ├─ SOURCE: Jira API (issues, custom fields)
  ├─ TRANSPORT: MCP (message-based, streaming)
  └─ TARGET: APOS Knowledge Graph
  
Notion Loader:
  ├─ SOURCE: Notion API (databases, properties)
  ├─ TRANSPORT: MCP
  └─ TARGET: APOS Knowledge Graph

Slack Loader:
  ├─ SOURCE: Slack API (messages, threads, reactions)
  ├─ TRANSPORT: MCP
  └─ TARGET: APOS Knowledge Graph
```

### Responsabilidade de R0 vs R1-R2

**R0:** Define MCP contract (quais fields, quale tipos, validações)  
**R1:** Implementa loaders que usam MCP  
**R2:** Adiciona streaming, webhooks, bidirectional sync

---

## A Importância: Por Que Não Misturar as Camadas

### ❌ Padrão que Falha (Gartner 2026)

```
1. Conectar MCP a 5 fontes (Jira, Notion, Slack, Spreadsheet, Confluence)
2. Esperar que agentes "entendam"
3. Em produção: agentes alucinam porque sem ontologia/semantic layer
```

### ✅ Padrão que Funciona (APOS)

```
1. Definir Ontologia (conceitos + relações + restrições)
2. Definir Semantic Layer (regras de negócio)
3. Instanciar Knowledge Graph (dados reais conectados)
4. Usar MCP pra transportar (loaders)
5. Governança valida (gates)

Resultado: Agentes raciocinam, não alucinam
```

---

## Cascata: De R0 a Produção

```
R0: Define 5 camadas (conceitual)
    ├─ Ontologia (conceitos + relações + restrições)
    ├─ Semantic Layer (regras de negócio)
    └─ Catálogo (estrutura)

R1: Instancia + Transporta
    ├─ Knowledge Graph (dados reais conectados)
    ├─ MCP Loaders (Jira, Notion, Slack)
    └─ Sincronização em tempo real

R2: Inteligência + Rastreabilidade
    ├─ Catálogo completo (linhagem)
    ├─ Impact analysis ("se mudo X, quebra Y?")
    └─ Semantic reasoning (agente navega sozinho)

R3: Governança
    ├─ Semantic Gates (valida alinhamento)
    ├─ Audit Runner (rastreia violações)
    └─ Quality metrics (monitora saúde)

R4: Ecosystem
    └─ SDK público, extensões, comunidade
```

---

## Métricas de Sucesso (R0)

| Métrica | Target | Medida |
|---------|--------|--------|
| **Clarity of Ontology** | 95% | Team explica 5 conceitos sem doc |
| **Semantic Rules Completeness** | 100% | 10+ rules documentadas |
| **Catalog Structure Defined** | 100% | Schema de linhagem definido |
| **MCP Contract Specified** | 100% | Fields, types, validations |
| **Stakeholder Alignment** | 90% | Consenso sobre design |

---

## Próximas Entregas

- **ONTOLOGY_SPEC.md** — Definição formal de conceitos + restrições
- **SEMANTIC_LAYER_SPEC.md** — Regras de negócio
- **CATALOG_SCHEMA.md** — Schema de linhagem
- **MCP_CONTRACT.md** — Definição de protocolo

---

**Criado em:** 2026-07-19  
**Versão:** Draft  
**Próximo Review:** Sprint 0.2 (quando ontologia e semantic layer forem validados)
