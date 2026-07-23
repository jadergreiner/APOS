# Plano de Testes — Sprint R1.2

**QA:** Hermes Agent
**Escopo:** US-001 (Cache), US-002 (Context), US-003 (Validate)
**Tipo:** Unitários + Integração

---

## US-001: Cache de Perfil (1.5 SP)

### Setup

```python
from pathlib import Path
import tempfile, json, hashlib, time
from apos.project_adapter import ProjectProfile, ProjectAdapter

# Fixture: profile valido
VALID_PROFILE = ProjectProfile(
    language="Python",
    framework="FastAPI",
    database="DynamoDB",
    cloud_provider="AWS",
    runtime_version=">=3.12",
    module_count=10,
    total_loc=50000,
    directory_layout="nested",
    architecture_patterns=["domain_infra_split", "fastapi_routes"],
    has_ontology=True,
    naming_convention="snake_case",
)

# Fixture: temp dir para cache
@pytest.fixture
def cache_dir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)
```

---

#### TC-001: Cache hit retorna profile sem executar detectores

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-001 |
**Cenário** | Cache hit |
**Pré-condição** | Cache existe e TTL válido |
**Passos** | 1. Salvar profile no cache. 2. Ler do cache. |
**Resultado esperado** | Profile retornado, detectores NÃO executados |
**Tipo** | Happy path |

```python
async def test_cache_hit_returns_profile_without_discover():
    cache = ProjectCache(cache_dir)
    await cache.save(VALID_PROFILE)
    profile, source = await cache.load()
    assert profile == VALID_PROFILE
    assert source == "cache"
```

---

#### TC-002: Cache miss executa discover e armazena

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-002 |
**Cenário** | Cache miss |
**Pré-condição** | Cache vazio ou inexistente |
**Passos** | 1. Tentar carregar. 2. Detector executado. 3. Resultado cacheado. |
**Resultado esperado** | discover() executado, profile salvo em disco |
**Tipo** | Happy path |

---

#### TC-003: TTL expirado força novo discover

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-003 |
**Cenário** | TTL expirado |
**Pré-condição** | Cache existe mas TTL expirou (ex: TTL=0) |
**Passos** | 1. Cache salvo com TTL=0. 2. Tentar carregar. |
**Resultado esperado** | Cache ignorado, discover() executado |
**Tipo** | Edge case |

---

#### TC-004: Invalidação por hash mismatch (pyproject.toml alterado)

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-004 |
**Cenário** | Hash mismatch |
**Pré-condição** | Cache existe mas hash do pyproject.toml difere |
**Passos** | 1. Salvar cache. 2. Modificar pyproject.toml. 3. Tentar carregar. |
**Resultado esperado** | Hash detectado diferente → cache invalidado, novo discover() |
**Tipo** | Edge case |

---

#### TC-005: Cache corrompido (JSON inválido)

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-005 |
**Cenário** | Cache corrompido |
**Pré-condição** | Arquivo de cache existe mas JSON inválido |
**Passos** | 1. Escrever JSON mal-formado no cache. 2. Tentar carregar. |
**Resultado esperado** | Exceção tratada → fallback para discover(), SEM crash |
**Tipo** | Edge case |

---

#### TC-006: Cache vazio comporta como miss

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-006 |
**Cenário** | Cache vazio |
**Pré-condição** | Arquivo de cache existe mas vazio (0 bytes) |
**Passos** | 1. Arquivo vazio. 2. Tentar carregar. |
**Resultado esperado** | Comporta como cache miss → discover() |
**Tipo** | Edge case |

---

#### TC-007: Concorrência — duas leituras simultâneas

| Campo | Detalhe |
|-------|---------|
**ID** | CACHE-007 |
**Cenário** | Concorrência |
**Pré-condição** | Cache válido |
**Passos** | 1. Duas coroutines tentam ler simultaneamente |
**Resultado esperado** | Ambas retornam profile, sem race condition |
**Tipo** | Edge case |

---

## US-002: Injeção de Contexto (2.0 SP)

### Setup

```python
from apos.project_adapter import ProjectProfile
from apos.project_adapter.cache import ProjectCache
from pathlib import Path
```

---

#### TC-008: CLI `apos context` com cache válido

| Campo | Detalhe |
|-------|---------|
**ID** | CTX-001 |
**Cenário** | Contexto com cache |
**Pré-condição** | Cache existe e TTL válido |
**Passos** | 1. `apos context` |
**Resultado esperado** | Markdown formatado com: language, framework, database, cloud, modules, patterns |
**Tipo** | Happy path |

**Formato esperado:**
```markdown
## Project Context
- **Language:** Python
- **Framework:** FastAPI
- **Database:** DynamoDB
- **Cloud:** AWS
- **Modules:** 10 detected
- **Patterns:** domain_infra_split, fastapi_routes
- **Has Ontology:** Yes
```

---

#### TC-009: CLI `apos context` sem cache

| Campo | Detalhe |
|-------|---------|
**ID** | CTX-002 |
**Cenário** | Contexto sem cache |
**Pré-condição** | Cache vazio ou inexistente |
**Passos** | 1. `apos context` |
**Resultado esperado** | Mensagem: "Nenhum cache encontrado. Execute 'apos discover' primeiro." |
**Tipo** | Edge case |

---

#### TC-010: Profile parcial — apenas campos preenchidos

| Campo | Detalhe |
|-------|---------|
**ID** | CTX-003 |
**Cenário** | Profile parcial |
**Pré-condição** | Profile com language=Python, todo resto vazio |
**Passos** | 1. `apos context` |
**Resultado esperado** | Apenas language aparece; campos vazios omitidos |
**Tipo** | Edge case |

---

#### TC-011: Saída markdown é parseável

| Campo | Detalhe |
|-------|---------|
**ID** | CTX-004 |
**Cenário** | Validação de formato |
**Pré-condição** | Cache válido |
**Passos** | 1. `apos context > /tmp/ctx.md`. 2. Parse com python-markdown |
**Resultado esperado** | Markdown válido (parseável sem erro) |
**Tipo** | Happy path |

---

#### TC-012: Contexto injetado em subagent via template

| Campo | Detalhe |
|-------|---------|
**ID** | CTX-005 |
**Cenário** | Integração Hermes |
**Pré-condição** | Cache válido, template string configurada |
**Passos** | 1. `apos context --template` |
**Resultado esperado** | String formatada para copiar no goal do delegate_task |
**Tipo** | Integração |

---

## US-003: Validação Código vs Docs (1.5 SP)

### Setup

```python
from apos.validate import ProjectValidator
from apos.project_adapter import ProjectProfile
```

---

#### TC-013: Stack coincide → relatório 100% verde

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-001 |
**Cenário** | Consistência total |
**Pré-condição** | Profile bate com docs/SDD/ |
**Passos** | 1. `apos validate`. 2. Verificar relatório. |
**Resultado esperado** | Todas as seções ✅. Score 100%. |
**Tipo** | Happy path |

---

#### TC-014: Framework diferente do documentado

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-002 |
**Cenário** | Divergência detectada |
**Pré-condição** | Profile diz FastAPI, docs dizem Flask |
**Passos** | 1. `apos validate`. 2. Verificar alerta. |
**Resultado esperado** | ❌ "framework: profile=FastAPI, docs=Flask" |
**Tipo** | Edge case |

---

#### TC-015: SDD sem código correspondente

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-003 |
**Cenário** | Documentação órfã |
**Pré-condição** | SDD existe no docs/ mas features não detectadas no código |
**Passos** | 1. `apos validate`. 2. Listar SDDs sem match. |
**Resultado esperado** | ⚠️ "SDD-00XX: features listadas não detectadas no código" |
**Tipo** | Edge case |

---

#### TC-016: Código sem SDD correspondente

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-004 |
**Cenário** | Código não documentado |
**Pré-condição** | Feature detectada no código mas sem SDD correspondente |
**Passos** | 1. `apos validate`. 2. Listar código sem docs. |
**Resultado esperado** | ⚠️ "Módulo X detectado mas sem SDD correspondente" |
**Tipo** | Edge case |

---

#### TC-017: Validação contra Meu PDI real (backend/)

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-005 |
**Cenário** | Integração Meu PDI |
**Pré-condição** | Meu PDI acessível em `/mnt/c/repo/meu-pdi/backend` |
**Passos** | 1. `apos validate --path /mnt/c/repo/meu-pdi/backend`. 2. Verificar relatório. |
**Resultado esperado** | ≥80% consistência. Nenhum falso positivo. |
**Tipo** | Integração |

---

#### TC-018: Zero falsos positivos (3 execuções consecutivas)

| Campo | Detalhe |
|-------|---------|
**ID** | VAL-006 |
**Cenário** | Regressão de falsos positivos |
**Pré-condição** | Profile idêntico ao docs |
**Passos** | 1. Executar `validate` 3x. 2. Todas as execuções retornam mesmo resultado. |
**Resultado esperado** | Score idêntico nas 3 execuções. Zero alertas espúrios. |
**Tipo** | Regressão |

---

## Matriz de Rastreabilidade

| US | ID | Cenário | Tipo | Prioridade |
|----|----|---------|------|:----------:|
| **US-001** | CACHE-001 | Cache hit | Happy | 🔴 Alta |
| | CACHE-002 | Cache miss | Happy | 🔴 Alta |
| | CACHE-003 | TTL expirado | Edge | 🟡 Média |
| | CACHE-004 | Hash mismatch | Edge | 🔴 Alta |
| | CACHE-005 | Cache corrompido | Edge | 🔴 Alta |
| | CACHE-006 | Cache vazio | Edge | 🟡 Média |
| | CACHE-007 | Concorrência | Edge | 🟢 Baixa |
| **US-002** | CTX-001 | Contexto com cache | Happy | 🔴 Alta |
| | CTX-002 | Contexto sem cache | Edge | 🔴 Alta |
| | CTX-003 | Profile parcial | Edge | 🟡 Média |
| | CTX-004 | Markdown parseável | Happy | 🟡 Média |
| | CTX-005 | Integração Hermes | Integr. | 🟢 Baixa |
| **US-003** | VAL-001 | Stack coincide | Happy | 🔴 Alta |
| | VAL-002 | Framework diverge | Edge | 🔴 Alta |
| | VAL-003 | SDD órfão | Edge | 🟡 Média |
| | VAL-004 | Código órfão | Edge | 🟡 Média |
| | VAL-005 | Meu PDI real | Integr. | 🔴 Alta |
| | VAL-006 | Falso positivo | Regr. | 🔴 Alta |

## Sumário

| Métrica | Valor |
|---------|-------|
| **Total de cenários** | 18 |
| Happy path | 5 |
| Edge cases | 10 |
| Integração | 2 |
| Regressão | 1 |
| **Prioridade Alta** | 10 |
| **Prioridade Média** | 6 |
| **Prioridade Baixa** | 2 |
