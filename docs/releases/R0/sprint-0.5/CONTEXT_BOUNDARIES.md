# APOS Context Boundaries — Fronteiras de Contexto para Agentes de IA

**Documento:** CONTEXT_BOUNDARIES.md  
**Release:** R0 | **Sprint:** 0.5  
**Tarefa:** T0.5.1 — Modelo de contexto para agentes  
**Dependência:** CONTEXT_MODEL.md (pipeline, relevância, priorização)  
**Criado em:** 2026-07-21  
**Versão:** v0.1-draft

---

## Índice

1. [Introdução](#1-introdução)
2. [Critérios de Inclusão](#2-critérios-de-inclusão)
3. [Critérios de Exclusão](#3-critérios-de-exclusão)
4. [Priorização por Token Budget](#4-priorização-por-token-budget)
5. [Regras de Não Vazamento](#5-regras-de-não-vazamento)
6. [Limites por Tipo de Nó](#6-limites-por-tipo-de-nó)
7. [Exemplo Completo](#7-exemplo-completo)

---

## 1. Introdução

### 1.1 O Que São Fronteiras de Contexto

As **fronteiras de contexto** definem **o que entra e o que fica fora** da janela de contexto de um agente APOS. Enquanto o **CONTEXT_MODEL.md** define *como transformar o grafo em contexto* (o pipeline de extração, montagem, injeção e cleanup), o CONTEXT_BOUNDARIES.md define *o que é permitido e proibido entrar nesse contexto* — um conjunto de regras de fronteira que protegem a qualidade, a segurança e a eficiência do prompt.

Uma fronteira de contexto responde a três perguntas:

| Pergunta | Resposta |
|----------|----------|
| **O que deve entrar?** | Critérios de inclusão (relevância, profundidade, temporalidade) |
| **O que não deve entrar?** | Critérios de exclusão (dados sensíveis, expirados, irrelevantes) |
| **Quanto de cada coisa?** | Token budget por tipo e prioridade |

### 1.2 Por Que São Necessárias

Sem fronteiras de contexto bem definidas, o agente APOS sofre de:

| Problema | Sintoma | Consequência |
|----------|---------|--------------|
| **Poluição de prompt** | Informação irrelevante ocupa tokens preciosos | Agente perde foco, respostas degradam |
| **Vazamento de dados** | Dados sensíveis ou de outros usuários aparecem no contexto | Risco de segurança, violação de privacidade |
| **Estouro de janela** | Contexto > limite do modelo | Erro de processamento, truncamento silencioso |
| **Viés de recência** | Informação recente sem relevância real recebe peso excessivo | Decisões sub-ótimas do agente |
| **Carga cognitiva excessiva** | Agente recebe mais informação do que consegue processar | Lentidão, alucinação, contradições |

### 1.3 Relação com o Context Model

```
CONTEXT_MODEL.md                        CONTEXT_BOUNDARIES.md
─────────────────────                   ────────────────────────
Pipeline (extração → cleanup)           O que pode ser extraído
Relevance scoring                       O que NÃO pode ser incluído
Token limits por tier                   Token budget por tipo de nó
Core context (sempre incluso)           Regras de não vazamento
Modos de fallback                       Limites máximos por entidade
```

O **Context Model** implementa o motor; o **Context Boundaries** é o volante e os freios.

### 1.4 Princípios de Fronteira

1. **Mínimo Necessário** — Inclua apenas o contexto indispensável para a decisão do agente.
2. **Exclusão por Default** — Tudo está fora até que um critério de inclusão seja satisfeito.
3. **Isolamento por Domínio** — Sessões de diferentes agentes/usuários não compartilham contexto.
4. **Expiração Obrigatória** — Todo bloco carrega TTL; expirado = excluído.
5. **Auditabilidade** — Cada decisão de exclusão deve ser rastreável (URN, motivo, timestamp).

---

## 2. Critérios de Inclusão

### 2.1 Relevância Direta (URN Âncora)

O nó cuja URN foi explicitamente consultada pelo agente **sempre** entra no contexto.

| Condição | Inclusão | Exceção |
|----------|:--------:|---------|
| URN consultada está no KG | ✅ Sempre incluso | — |
| URN consultada **não** está no KG | ❌ Excluído | Retorna erro `NODE_NOT_FOUND` |
| URN consultada tem status `archived` | ❌ Excluído | Só incluso se agente explicitamente solicitar |

```python
def should_include_anchor(urn: str, kg: KnowledgeGraph) -> bool:
    """Verifica se a URN âncora pode ser incluída no contexto."""
    node = kg.get_node(urn)
    if node is None:
        return False
    if node.attributes.get("status") == "archived":
        return False  # Só inclui se agente solicitar explicitamente
    return True
```

### 2.2 Relevância Indireta (Vizinhos até Profundidade N)

Nós vizinhos ao âncora são incluídos conforme a profundidade e o peso da aresta.

| Profundidade | Peso Mínimo da Aresta | Inclusão | Condição Extra |
|:------------:|:---------------------:|:--------:|---------------|
| 1 (aresta direta) | ≥ 0.3 | ✅ Sempre avaliado | — |
| 2 (segundo salto) | ≥ 0.5 | ✅ Avaliado se token budget permite | Apenas se nó intermediário também incluso |
| 3+ (terceiro salto+) | — | ❌ Excluído | Exceto para alertas/bloqueios críticos |

```python
def should_include_neighbor(
    edge_weight: float,
    depth: int,
    anchor_urn: str,
    node_type: str,
) -> bool:
    """Decide se um nó vizinho deve ser incluído."""
    if depth == 0:
        return True  # âncora
    if depth == 1 and edge_weight >= 0.3:
        return True
    if depth == 2 and edge_weight >= 0.5:
        return True  # sujeito a token budget
    # Profundidade 3+: apenas para bloqueios ou alertas críticos
    if depth >= 3 and node_type == "blocker":
        return True
    return False
```

### 2.3 Relevância Temporal

Nós e arestas são incluídos ou excluídos com base na idade da última atualização.

| Janela Temporal | Inclusão | Prioridade |
|:---------------:|:--------:|:----------:|
| Últimas 1 hora | ✅ Sempre incluso | Alta |
| Últimas 24 horas | ✅ Sempre incluso (se relevante) | Alta |
| 24h–72h atrás | ✅ Incluso se relevância ≥ 0.5 | Média |
| 3–7 dias atrás | ✅ Incluso se relevância ≥ 0.7 **e** edge_weight ≥ 0.6 | Baixa |
| > 7 dias atrás | ❌ Excluído (exceto OKRs e Personas) | — |

**Exceções temporais:**

| Tipo de Nó | Janela Máxima | Motivo |
|------------|:-------------:|--------|
| OKR | 30 dias | OKRs têm ciclos longos (trimestrais) |
| Persona | 90 dias | Personas mudam raramente |
| Regra Semântica | Indefinido | Regras têm validade permanente |
| Evento Episódico | 7 dias | Eventos operacionais perdem relevância rápido |

```python
def is_fresh_enough(
    updated_at: str,
    node_type: str,
    now: datetime,
) -> tuple[bool, str]:
    """Verifica se o nó é recente o suficiente para entrar no contexto.

    Returns:
        (included: bool, reason: str)
    """
    age_hours = (now - datetime.fromisoformat(updated_at)).total_seconds() / 3600

    window = {
        "task": 72,      # 3 dias
        "feature": 72,   # 3 dias
        "release": 72,   # 3 dias
        "sprint": 168,   # 7 dias
        "okr": 720,      # 30 dias
        "metric": 168,   # 7 dias
        "persona": 2160, # 90 dias
        "rule": float("inf"),
    }.get(node_type, 72)

    if age_hours <= 24:
        return True, "fresh"
    if age_hours <= window:
        return True, "aging"
    return False, f"expired (age={age_hours:.1f}h > window={window}h)"
```

### 2.4 Regra Geral de Inclusão

Um nó ou aresta **entra** no contexto se **todas** as condições abaixo forem verdadeiras:

1. ✅ A URN existe no Knowledge Graph
2. ✅ O nó não está em status `archived` (salvo solicitação explícita)
3. ✅ A profundidade em relação ao âncora ≤ 2 (salvo bloqueios/alertas)
4. ✅ O peso da aresta ≥ threshold por profundidade
5. ✅ A última atualização está dentro da janela temporal do tipo
6. ✅ O TTL do bloco não expirou
7. ✅ O bloco não contém dados sensíveis (seção 5)

---

## 3. Critérios de Exclusão

### 3.1 O Que NUNCA Entra no Contexto

| Categoria | O Que Excluir | Exemplo | Mecanismo |
|-----------|---------------|---------|-----------|
| **Dados Sensíveis** | PII, tokens de API, secrets, senhas, chaves | `db_password`, `api_key`, `cpf_usuario` | Sanitização + blocking list |
| **Contexto Expirado** | Nós com TTL vencido | Task atualizada há 5 dias atrás (TTL=24h) | Cleanup por TTL |
| **Baixa Relevância** | Score de relevância < threshold | Feature com relevance 0.12 (threshold=0.3) | Podagem por score |
| **Nós Arquivedados** | Status = `archived` | Release v1.0 (shipped e arquivada) | Filtro de status |
| **Nós Órfãos** | Sem arestas de entrada/saída | Nó criado por engano, sem conexões | Detecção de orphans (Q15) |
| **Dados de Dev em Prod** | Flag `environment=dev` em produção | Nó de teste com env=dev | Filtro de ambiente |
| **Metadados Internos** | Embeddings, vectores, hashes | Blob de embedding (F32, 384d) | Excluído do ContextBlock |

### 3.2 Thresholds de Relevância

| Tier | Relevance Score | Ação |
|:----:|:---------------:|------|
| **CRITICAL** | ≥ 0.80 | **Sempre incluso** (não pode ser removido) |
| **HIGH** | 0.50 – 0.79 | **Incluso se houver budget**; pode ser comprimido |
| **NORMAL** | 0.30 – 0.49 | **Incluso por último**; removido primeiro |
| **BAIXO** | 0.10 – 0.29 | **Excluído por default** — só incluso se agente pedir |
| **IRRELEVANTE** | < 0.10 | **Nunca incluso** — descartado na extração |

```python
RELEVANCE_THRESHOLDS = {
    "always_include": 0.80,     # CRITICAL — sempre incluso
    "budget_dependent": 0.50,   # HIGH — incluso se houver budget
    "optional": 0.30,           # NORMAL — baixa prioridade
    "exclude_default": 0.10,     # BAIXO — excluído por default
}
```

### 3.3 Exclusão por TTL Expirado

| Tipo de Nó | TTL Padrão (h) | TTL Máximo (h) | Ação ao Expirar |
|------------|:--------------:|:---------------:|-----------------|
| Task | 24 | 72 | Remove do contexto |
| Feature | 48 | 96 | Remove do contexto |
| Release | 48 | 96 | Remove do contexto |
| Sprint | 24 | 72 | Remove do contexto |
| OKR | 72 | 720 (30d) | Arquiva com aviso |
| Metric | 72 | 168 (7d) | Remove do contexto |
| Persona | 168 (7d) | 2160 (90d) | Arquiva com aviso |

```python
def is_ttl_expired(
    freshness: str,
    ttl_hours: int,
    now: datetime,
) -> bool:
    """Verifica se o TTL de um bloco expirou."""
    age_hours = (now - datetime.fromisoformat(freshness)).total_seconds() / 3600
    return age_hours > ttl_hours
```

### 3.4 Exclusão por Ambiente (Dev vs Produção)

O sistema DEVE garantir que dados de ambientes diferentes nunca se misturem.

| Ambiente do Agente | Ambiente do Nó | Inclusão? |
|:------------------:|:--------------:|:---------:|
| production | production | ✅ Permitido |
| production | dev/staging | ❌ Bloqueado |
| dev/staging | dev/staging | ✅ Permitido |
| dev/staging | production | ⚠️ Permitido só com flag `allow_prod_data_in_dev=true` |

### 3.5 Ordem de Exclusão

Quando a janela de contexto estoura, os blocos são excluídos na seguinte ordem:

1. 🔴 **Nós com relevance < 0.30** (BAIXO / IRRELEVANTE)
2. 🔴 **Nós com TTL expirado** (> 72h sem atualização)
3. 🟡 **Personas sem conexão direta com o âncora**
4. 🟡 **Métricas com status "healthy" e sem alertas**
5. 🟢 **Releases finalizadas (status = "shipped")**
6. 🟢 **Tasks concluídas (status = "done") sem bloqueios pendentes**

---

## 4. Priorização por Token Budget

### 4.1 Alocação Base

O token budget é dividido em 4 categorias que definem **quanto contexto de cada tipo** entra no prompt.

| Categoria | % do Budget | Descrição |
|:---------:|:-----------:|-----------|
| **Core Context** | 30% | Nó âncora + bloqueios + nós críticos — **sempre incluso** |
| **Auxiliar** | 40% | Features, releases, sprints, métricas relacionadas ao âncora |
| **Histórico** | 20% | Eventos episódicos, decisões passadas, sessoes anteriores |
| **Metadados** | 10% | Timestamps, versões, trust scores, URNs |

```python
BUDGET_ALLOCATION = {
    "core": 0.30,       # 30% — sempre incluso
    "auxiliary": 0.40,  # 40% — features, sprints, releases
    "historical": 0.20, # 20% — eventos, decisões, sessões anteriores
    "metadata": 0.10,   # 10% — timestamps, versões, trust scores
}
```

### 4.2 Exemplo para Janela de 8000 Tokens

| Categoria | % | Tokens | Conteúdo Típico |
|:---------:|:-:|:------:|-----------------|
| Core | 30% | 2400 | Nó âncora (1200) + 2 bloqueios (1200) |
| Auxiliar | 40% | 3200 | Feature (800) + Sprint (600) + Metric (500) + Release (450) + OKR (450) + Persona (400) |
| Histórico | 20% | 1600 | 3 eventos episódicos (900) + 1 decisão (400) + 1 sessão anterior sumário (300) |
| Metadados | 10% | 800 | Trust score (400) + versões (200) + URNs (200) |
| **Total** | **100%** | **8000** | |

### 4.3 Alocação por Tipo de Agente

Agentes diferentes recebem alocações diferentes do mesmo budget.

| Tipo de Agente | Core | Auxiliar | Histórico | Metadados | Total |
|:--------------:|:----:|:--------:|:---------:|:---------:|:-----:|
| Task Agent | 35% | 40% | 15% | 10% | 8000 |
| Feature/OKR Agent | 25% | 45% | 20% | 10% | 8000 |
| Release Manager | 20% | 50% | 20% | 10% | 8000 |
| Sprint Agent | 30% | 35% | 25% | 10% | 8000 |
| Query/Read Agent | 20% | 30% | 35% | 15% | 4000 |

```python
AGENT_BUDGET_PROFILES = {
    "task_agent": {"core": 0.35, "auxiliary": 0.40, "historical": 0.15, "metadata": 0.10, "max_tokens": 8000},
    "feature_agent": {"core": 0.25, "auxiliary": 0.45, "historical": 0.20, "metadata": 0.10, "max_tokens": 8000},
    "release_manager": {"core": 0.20, "auxiliary": 0.50, "historical": 0.20, "metadata": 0.10, "max_tokens": 8000},
    "sprint_agent": {"core": 0.30, "auxiliary": 0.35, "historical": 0.25, "metadata": 0.10, "max_tokens": 8000},
    "query_agent": {"core": 0.20, "auxiliary": 0.30, "historical": 0.35, "metadata": 0.15, "max_tokens": 4000},
}
```

### 4.4 Limites por Categoria

| Categoria | Mínimo Blocos | Máximo Blocos | Tokens Máximo por Bloco |
|:---------:|:-------------:|:-------------:|:----------------------:|
| Core | 1 (âncora) | 5 | 1500 |
| Auxiliar | 0 | 8 | 800 |
| Histórico | 0 | 5 | 600 |
| Metadados | 0 | 3 | 400 |

### 4.5 Priorização Intra-Categoria

Dentro de cada categoria, os blocos seguem esta ordem:

**Core (30%):**
1. Nó âncora (sempre primeiro)
2. Bloqueios ativos (arestas `bloqueia` incoming)
3. Nós com status `critical` ou `at_risk`
4. Trust score < 80% (alerta de integridade)

**Auxiliar (40%):**
1. Features conectadas por `contribui_para` (peso ≥ 0.7)
2. Sprints conectadas por `pertence_a`
3. Métricas impactadas (arestas `impacta`)
4. Releases pai (`parte_de`)
5. OKRs vinculados (`alcanca`)
6. Personas relacionadas

**Histórico (20%):**
1. Decisões recentes sobre a mesma URN (últimas 24h)
2. Eventos de mudança de estado da URN âncora
3. Sessões anteriores que mencionam a mesma URN
4. Erros/falhas relacionados

**Metadados (10%):**
1. Trust score do grafo (sempre incluso se disponível)
2. Versão dos nós principais
3. Timestamps de última atualização

---

## 5. Regras de Não Vazamento

### 5.1 O Que o Agente NÃO Deve Ver

| Categoria | O Que NÃO Incluir | Mecanismo de Bloqueio |
|-----------|-------------------|-----------------------|
| **Outras Sessões** | Contexto de sessões de outros agentes/usuários | Filtro `session_id` no recall |
| **Dados de Produção em Dev** | Nós com `env=production` em ambiente dev | Filtro de ambiente (seção 3.4) |
| **Dados Sensíveis** | PII, tokens, secrets, senhas | Regex blocking list + sanitização |
| **Conteúdo Irrelevante** | Nós sem arestas para o âncora | Algoritmo de expansão radial (seção 2.2) |
| **Metadados Internos** | Embeddings, vectores, hashes, configuração de DB | Exclusão no formato do ContextBlock |
| **Nós Deletados** | Nós com flag `deleted=true` no KG | Filtro de exclusão lógica |

### 5.2 Barreiras de Privacidade

```python
PRIVACY_BARRIERS = {
    # Campos bloqueados — NUNCA entram no contexto do agente
    "blocked_fields": [
        "password", "api_key", "secret", "token", "credential",
        "cpf", "ssn", "email_personal", "phone", "address",
        "internal_note", "audit_log_raw", "raw_prompt",
    ],
    # Padrões de PII — bloqueados por regex
    "blocked_patterns": [
        r"^sk-[A-Za-z0-9]{32,}$",           # OpenAI keys
        r"^ghp_[A-Za-z0-9]{36}$",            # GitHub PAT
        r"^AKIA[A-Z0-9]{16}$",               # AWS Access Key
        r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",    # CPF
        r"\b\d{2}/\d{2}/\d{4}\b",            # Data de nascimento
    ],
    # Tipos de nó que nunca entram no contexto
    "blocked_node_types": [
        "internal_config",
        "audit_entry",
        "raw_embedding",
    ],
}
```

### 5.3 Sanitização de Atributos

Antes de montar um ContextBlock, os atributos do nó passam por sanitização:

```python
def sanitize_attributes(attributes: dict) -> dict:
    """Remove campos sensíveis dos atributos antes de montar o bloco."""
    blocked = PRIVACY_BARRIERS["blocked_fields"]
    blocked_patterns = [re.compile(p) for p in PRIVACY_BARRIERS["blocked_patterns"]]

    sanitized = {}
    for key, value in attributes.items():
        # Bloqueia por nome de campo
        if key.lower() in blocked:
            continue
        # Bloqueia por padrão de valor
        if isinstance(value, str):
            if any(p.search(value) for p in blocked_patterns):
                continue
        sanitized[key] = value
    return sanitized
```

### 5.4 Isolamento por Tenant/Agente

O sistema DEVE garantir que:

1. **Agente A** nunca vê contexto de sessões do **Agente B**
2. **Usuário 1** nunca vê dados do **Usuário 2**
3. **Ambiente dev** usa apenas dados dev (salvo flag explícita)
4. **Cada sessão** tem seu próprio `session_id` e não herda contexto de sessões paralelas

```python
def validate_context_isolation(
    agent_id: str,
    blocks: list[ContextBlock],
    environment: str,
) -> list[ContextBlock]:
    """Remove blocos que violam o isolamento do agente/ambiente."""
    validated = []
    for block in blocks:
        block_env = block.metadata.get("environment", environment)
        if block_env != environment:
            continue  # Bloqueia dados de ambiente errado
        block_agent = block.metadata.get("agent_id")
        if block_agent and block_agent != agent_id:
            continue  # Bloqueia dados de outro agente
        validated.append(block)
    return validated
```

### 5.5 Regras de Não Vazamento — Resumo

| # | Regra | Onde se Aplica | Consequência da Violação |
|:-:|-------|:--------------:|--------------------------|
| 1 | Agente X só vê dados do Agente X | Recall, inject | Vazamento entre agentes |
| 2 | Dados sensíveis são sanitizados | Assembly (montagem) | Exposição de PII/secrets |
| 3 | Dev não acessa prod sem flag explícita | Extração | Contaminação de ambiente |
| 4 | Nós órfãos/deletados são excluídos | Extração, Cleanup | Poluição de prompt |
| 5 | Sessões paralelas não compartilham contexto | Recall | Confusão de estado |
| 6 | Metadados internos do KG nunca vazam | Format output | Exposição de infraestrutura |

---

## 6. Limites por Tipo de Nó

### 6.1 Tabela de Limites

Cada tipo de nó tem um limite máximo de tokens que pode ocupar no contexto, independentemente do budget disponível.

| Tipo de Nó | Max Tokens | TTL Padrão (h) | Prioridade | Pode Ser Comprimido? |
|------------|:----------:|:---------------:|:----------:|:--------------------:|
| **Task** | 500 | 24 | Alta | Sim (remove description, acceptance_criteria) |
| **Feature** | 300 | 48 | Alta | Sim (remove description, tags) |
| **Release** | 400 | 48 | Média | Sim (remove release_notes) |
| **OKR** | 300 | 72 | Média | Sim (remove description) |
| **Metric** | 200 | 72 | Média-Alta | Sim (remove formula, source) |
| **Sprint** | 300 | 24 | Alta (ativo) / Baixa (encerrado) | Sim (remove goal detalhado) |
| **Persona** | 350 | 168 (7d) | Baixa | Sim (remove citações, detailed_description) |
| **Blocker** | 250 | 12 | Crítica | Não (deve ser completo) |
| **Edge (aresta)** | 100 | — | Conforme nó alvo | Sempre (apenas URN + tipo + peso) |

```python
NODE_TOKEN_LIMITS = {
    "task":     {"max_tokens": 500,  "ttl_hours": 24,  "compressible": True,  "priority": "high"},
    "feature":  {"max_tokens": 300,  "ttl_hours": 48,  "compressible": True,  "priority": "high"},
    "release":  {"max_tokens": 400,  "ttl_hours": 48,  "compressible": True,  "priority": "medium"},
    "okr":      {"max_tokens": 300,  "ttl_hours": 72,  "compressible": True,  "priority": "medium"},
    "metric":   {"max_tokens": 200,  "ttl_hours": 72,  "compressible": True,  "priority": "medium_high"},
    "sprint":   {"max_tokens": 300,  "ttl_hours": 24,  "compressible": True,  "priority": "high"},
    "persona":  {"max_tokens": 350,  "ttl_hours": 168, "compressible": True,  "priority": "low"},
    "blocker":  {"max_tokens": 250,  "ttl_hours": 12,  "compressible": False, "priority": "critical"},
    "edge":     {"max_tokens": 100,  "ttl_hours": None, "compressible": True,  "priority": "variable"},
}
```

### 6.2 Composição por Tipo (O Que Ocupa os Tokens)

| Tipo | Campo | Tokens Aprox. | Compressível? |
|------|-------|:-------------:|:-------------:|
| **Task** | title | 50 | ❌ |
| | status | 10 | ❌ |
| | priority | 10 | ❌ |
| | story_points | 10 | ❌ |
| | owner | 20 | ❌ |
| | description | 200 | ✅ (removível) |
| | acceptance_criteria | 150 | ✅ (removível) |
| | tags | 50 | ✅ (removível) |
| **Feature** | name | 30 | ❌ |
| | status | 10 | ❌ |
| | completeness | 10 | ❌ |
| | description | 150 | ✅ (removível) |
| | tags | 100 | ✅ (removível) |
| **Release** | version | 20 | ❌ |
| | status | 10 | ❌ |
| | date | 10 | ❌ |
| | release_notes | 300 | ✅ (removível) |
| | milestones | 60 | ✅ (parcial) |

### 6.3 Política de Compressão por Tipo

| Tipo | O Que é Removido na Compressão | O Que é Mantido |
|------|-------------------------------|-----------------|
| Task | `description`, `acceptance_criteria`, `tags` | `title`, `status`, `priority`, `story_points`, `owner` |
| Feature | `description`, `tags`, `dependencies` | `name`, `status`, `completeness` |
| Release | `release_notes`, `milestones_detail` | `version`, `status`, `date` |
| OKR | `description`, `context`, `notes` | `objective`, `status`, `current_value`, `target_value` |
| Metric | `formula`, `source`, `history` | `name`, `current_value`, `target`, `status`, `unit` |
| Sprint | `goal_detail`, `risks`, `notes` | `name`, `status`, `goal`, `start_date`, `end_date` |

### 6.4 Limite Global de Blocos no Contexto

| Métrica | Limite | Observação |
|---------|:------:|------------|
| Blocos totais no contexto | ≤ 20 | Acima disso, qualidade degrada |
| Blocos do mesmo tipo | ≤ 5 | Evita repetição (ex: 5 tasks similares) |
| Blocos de profundidade 2 | ≤ 3 | Apenas os mais relevantes |
| Blocos comprimidos | ≤ 50% do total | Garante que informação essencial não é perdida |

---

## 7. Exemplo Completo

### Cenário: "Agente pergunta sobre Task X, sistema decide quais nós incluir e excluir"

**Contexto:** Um agente task agent consulta a Task `urn:apos:task:oauth-123`. O sistema precisa montar o contexto respeitando as fronteiras definidas.

### 7.1 Knowledge Graph (Dados de Origem)

```json
{
  "nodes": [
    {
      "id": "urn:apos:task:oauth-123",
      "type": "task",
      "attributes": { "title": "Implement OAuth Login", "status": "in_progress", "priority": "high", "story_points": 5, "owner": "agent-oauth", "description": "Implementar fluxo OAuth 2.0 com Google e GitHub" },
      "metadata": { "created_at": "2026-07-15T10:00:00Z", "updated_at": "2026-07-21T14:30:00Z", "version": 3, "environment": "production" }
    },
    {
      "id": "urn:apos:feature:faster-auth",
      "type": "feature",
      "attributes": { "name": "Faster Authentication", "status": "in_progress", "completeness": 0.75, "owner": "team-auth" },
      "metadata": { "created_at": "2026-07-10T10:00:00Z", "updated_at": "2026-07-20T14:00:00Z", "version": 4, "environment": "production" }
    },
    {
      "id": "urn:apos:release:v2-1",
      "type": "release",
      "attributes": { "version": "2.1.0", "status": "in_progress", "date": "2026-07-31" },
      "metadata": { "created_at": "2026-07-01T08:00:00Z", "updated_at": "2026-07-20T10:00:00Z", "version": 5, "environment": "production" }
    },
    {
      "id": "urn:apos:okr:churn-5pct",
      "type": "okr",
      "attributes": { "objective": "Reduce customer churn by 5%", "status": "on_track", "current_value": 3.2, "target_value": 5.0 },
      "metadata": { "created_at": "2026-06-15T08:00:00Z", "updated_at": "2026-07-20T09:00:00Z", "version": 6, "environment": "production" }
    },
    {
      "id": "urn:apos:metric:login-time",
      "type": "metric",
      "attributes": { "name": "Login Time", "unit": "seconds", "current_value": 2.5, "target": 2.0, "status": "at_risk" },
      "metadata": { "created_at": "2026-06-20T08:00:00Z", "updated_at": "2026-07-20T12:00:00Z", "version": 3, "environment": "production" }
    },
    {
      "id": "urn:apos:sprint:s0-4",
      "type": "sprint",
      "attributes": { "name": "Sprint 0.4", "status": "active", "goal": "Finalizar design do Knowledge Graph", "start_date": "2026-07-20", "end_date": "2026-08-03" },
      "metadata": { "created_at": "2026-07-20T08:00:00Z", "updated_at": "2026-07-21T08:00:00Z", "version": 1, "environment": "production" }
    },
    {
      "id": "urn:apos:sprint:s0-3",
      "type": "sprint",
      "attributes": { "name": "Sprint 0.3", "status": "closed", "goal": "Setup inicial do projeto" },
      "metadata": { "created_at": "2026-07-06T08:00:00Z", "updated_at": "2026-07-19T18:00:00Z", "version": 2, "environment": "production" }
    },
    {
      "id": "urn:apos:task:legacy-debt",
      "type": "task",
      "attributes": { "title": "Refactor legacy auth", "status": "archived", "priority": "low" },
      "metadata": { "created_at": "2026-06-01T08:00:00Z", "updated_at": "2026-06-30T10:00:00Z", "version": 1, "environment": "production" }
    },
    {
      "id": "urn:apos:config:db-credentials",
      "type": "internal_config",
      "attributes": { "host": "db.internal", "password": "sk-secret-abc123", "port": 5432 },
      "metadata": { "created_at": "2026-07-01T08:00:00Z", "updated_at": "2026-07-01T08:00:00Z", "version": 1, "environment": "production" }
    }
  ],
  "edges": [
    {"source": "urn:apos:task:oauth-123", "target": "urn:apos:feature:faster-auth", "type": "contribui_para", "weight": 1.0},
    {"source": "urn:apos:feature:faster-auth", "target": "urn:apos:release:v2-1", "type": "parte_de", "weight": 1.0},
    {"source": "urn:apos:release:v2-1", "target": "urn:apos:okr:churn-5pct", "type": "alcanca", "weight": 0.7},
    {"source": "urn:apos:okr:churn-5pct", "target": "urn:apos:metric:login-time", "type": "medido_por", "weight": 1.0},
    {"source": "urn:apos:task:oauth-123", "target": "urn:apos:metric:login-time", "type": "impacta", "weight": 0.8},
    {"source": "urn:apos:task:oauth-123", "target": "urn:apos:sprint:s0-4", "type": "pertence_a", "weight": 1.0}
  ]
}
```

### 7.2 Decisão de Inclusão/Exclusão

O sistema processa cada nó candidato contra as regras de fronteira:

| Nó | Prof. | Edge Weight | Freshness | Relevance | Decisão | Motivo |
|:--:|:-----:|:-----------:|:---------:|:---------:|:-------:|--------|
| `task:oauth-123` | 0 | — | 1h | 1.0000 | ✅ **Incluir** | URN âncora — core context |
| `feature:faster-auth` | 1 | 1.0 | 24h | 0.8625 | ✅ **Incluir** | Relação direta, peso ≥ 0.3, freshness < 72h |
| `metric:login-time` | 1 | 0.8 | 26h | 0.7563 | ✅ **Incluir** | Relação direta, peso ≥ 0.3, status at_risk |
| `sprint:s0-4` | 1 | 1.0 | 6h | 0.8375 | ✅ **Incluir** | Relação direta, sprint ativo |
| `release:v2-1` | 2 | 1.0 | 28h | 0.6563 | ✅ **Incluir** | Profundidade 2, peso ≥ 0.5, freshness < 72h |
| `okr:churn-5pct` | 2 | 0.7 | 29h | 0.5563 | ⚠️ **Incluir (se couber)** | Profundidade 2, peso ≥ 0.5, HIGH priority |
| `sprint:s0-3` | 2 | 0.3 | 48h | 0.3500 | ❌ **Excluir** | Sprint encerrado, relevância < 0.5 |
| `task:legacy-debt` | — | — | 504h | 0.0500 | ❌ **Excluir** | Status `archived`, freshness > 7 dias |
| `config:db-credentials` | — | — | — | — | ❌ **Excluir (bloqueado)** | Tipo `internal_config` — nono sensível |

### 7.3 Token Budget Applied (Agente Task, 8000 Tokens)

| Categoria | Budget | Tokens Usados | Blocos |
|:---------:|:-----:|:-------------:|--------|
| **Core (30%)** | 2400 | 1200 | task:oauth-123 (âncora) |
| **Auxiliar (40%)** | 3200 | 2300 | feature:faster-auth (300), sprint:s0-4 (300), metric:login-time (200), release:v2-1 (400), okr:churn-5pct (300), arestas (5×100=500) |
| **Histórico (20%)** | 1600 | 900 | 2 eventos recentes (600) + 1 decisão (300) |
| **Metadados (10%)** | 800 | 600 | Trust score (400) + versões (100) + URNs (100) |
| **Total** | **8000** | **5000** | ✅ Dentro do budget (3000 tokens livres) |

### 7.4 Verificação de Fronteiras — Checklist

```python
checklist = {
    "Âncora incluso?": True,
    "Feature incluso? (peso=1.0, depth=1)": True,
    "Métrica at_risk incluso?": True,
    "Sprint s0-3 excluído? (closed, relevance<0.5)": True,
    "Task archived excluída?": True,
    "DB credentials excluídos? (internal_config)": True,
    "Dados de produção usados? (env match)": True,
    "TTL válido para todos os blocos?": True,
    "Tokens dentro do budget? (5000 < 8000)": True,
    "Nenhum campo sensível no contexto?": True,
}
```

### 7.5 Contexto Renderizado (Resumo)

```
## Contexto APOS — Task Agent

### 🎯 Core (30%) — [1 bloco]
  TASK: urn:apos:task:oauth-123 | "Implement OAuth Login" | status: in_progress

### 🔗 Auxiliar (40%) — [5 blocos]
  FEATURE: faster-auth | relevance: 0.86 | completeness: 75%
  SPRINT: s0-4 | relevance: 0.84 | active
  METRIC: login-time | relevance: 0.76 | at_risk ⚠️
  RELEASE: v2-1 | relevance: 0.66 | date: 2026-07-31
  OKR: churn-5pct | relevance: 0.56 | on_track

### 📜 Histórico (20%) — [3 eventos]
  - 2026-07-21 10:00: Task status changed: open → in_progress
  - 2026-07-20 14:00: Feature faster-auth completeness: 50% → 75%
  - 2026-07-19 09:00: Decisão: priorizar OAuth sobre rate-limiting

### 📊 Metadados (10%)
  Trust Score: 84.9 (GOOD) | Versão KG: 3 | 5 blocos ativos

### ❌ Excluídos (fora da fronteira)
  - Sprint s0-3 (closed, expired)
  - Task legacy-debt (archived)
  - DB credentials (blocked: internal_config)
```

---

## Apêndice A — Resumo de Parâmetros de Fronteira

| Parâmetro | Padrão | Descrição |
|-----------|:------:|-----------|
| `max_depth_default` | 2 | Profundidade máxima de expansão padrão |
| `max_depth_blockers` | 3 | Profundidade máxima para bloqueios |
| `edge_weight_min_depth_1` | 0.3 | Peso mínimo para inclusão em profundidade 1 |
| `edge_weight_min_depth_2` | 0.5 | Peso mínimo para inclusão em profundidade 2 |
| `relevance_always_include` | 0.80 | Score mínimo para inclusão obrigatória |
| `relevance_exclude_default` | 0.10 | Abaixo deste score, excluído por default |
| `budget_core` | 0.30 | % do token budget para core context |
| `budget_auxiliary` | 0.40 | % para contexto auxiliar |
| `budget_historical` | 0.20 | % para histórico |
| `budget_metadata` | 0.10 | % para metadados |
| `max_blocks_total` | 20 | Máximo de blocos no contexto |
| `max_blocks_same_type` | 5 | Máximo de blocos do mesmo tipo |
| `max_blocks_depth_2` | 3 | Máximo de blocos de profundidade 2 |
| `privacy_sanitize_enabled` | true | Sanitização de dados sensíveis ativada |
| `environment_isolation` | true | Isolamento por ambiente ativado |

## Apêndice B — Glossário de Fronteiras

| Termo | Definição |
|-------|-----------|
| **Fronteira de Contexto** | Limite que define o que pode ou não entrar no contexto do agente |
| **Inclusão** | Decisão de permitir que um nó/aresta entre no contexto |
| **Exclusão** | Decisão de barrar um nó/aresta do contexto |
| **Token Budget** | Alocação percentual de tokens entre categorias de contexto |
| **Core Context** | Blocos que SEMPRE entram (30% do budget) |
| **Não Vazamento** | Garantia de que dados sensíveis ou de terceiros não vazam para o agente |
| **Sanitização** | Remoção de campos sensíveis dos atributos antes da montagem |
| **Isolamento por Ambiente** | Garantia de que dados dev/prod não se misturam |
| **Profundidade Máxima** | Número máximo de saltos no grafo a partir do âncora |
| **Threshold de Relevância** | Valor mínimo de relevance score para inclusão |
