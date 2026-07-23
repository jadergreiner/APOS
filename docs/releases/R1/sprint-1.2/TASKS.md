# Sprint Tasks — R1 Sprint 1.2

**Status:** Planning
**Início:** 2026-07-23 | **Término previsto:** 2026-07-25
**Velocity target:** 5.0 SP | **Total:** 5.0 SP (core) / 6.5 SP (stretch)

---

## Tasks Core (3.5 SP)

### US-001 — Cache de Perfil do Projeto (1.5 SP)

| Campo | Detalhe |
|-------|---------|
| **Descrição** | ProjectAdapter cacheia o profile descoberto em disco entre sessões. Evita re-descobrir a estrutura do projeto a cada execução. |
| **Jira** | SCRUM-64 (a criar) |
| **Status** | ✅ Concluído — `ProjectCache` em disco, TTL, hash SHA256, fallback |

**Definition of Ready (DoR):**
- [x] **DOR-01:** ProjectAdapter funcional — `from apos.project_adapter import ProjectAdapter` funciona
- [x] **DOR-02:** `ProjectProfile` schema congelado (language, framework, database, cloud_provider, etc.)
- [x] **DOR-03:** `apos/project_adapter/adapter.py` lido — `discover()` e `analyze()` compreendidos
- [x] **DOR-04:** Testes existentes passam (`pytest tests/unit/test_project_adapter/ -q` = 47 passed)
- [x] **DOR-05:** Diretório `tests/unit/test_cache/` criado (vazio, com `__init__.py`)
- [x] **DOR-06:** Nenhuma dependência externa — testes 100% unitários
- [x] **DOR-07:** Coverage baseline: `pytest --cov=apos/project_adapter` registrado
- [x] **DOR-08:** Aprovado pelo PO: escopo cabe em 1.5 SP

**Definition of Done (DoD):**
- [x] **COD-01:** Cache salvo em disco (JSON, ~2KB) com `project_cache.json`
- [x] **COD-02:** TTL configurável via parâmetro (default 1h)
- [x] **COD-03:** Invalidação automática se pyproject.toml mudar (hash SHA256)
- [x] **COD-04:** Fallback para `discover()` se cache expirado ou corrompido
- [x] **TST-01:** `pytest tests/unit/test_cache/ -v` — 6 cenários passando
- [x] **TST-02:** Coverage ≥80% no novo módulo de cache
- [x] **TST-03:** Zero regressão nos testes existentes
- [x] **DOC-01:** README do ProjectAdapter atualizado com seção de cache
- [x] **REV-01:** Código revisado sem dead code
- [x] **JIRA-01:** SCRUM-64 movido para Concluído
- [x] **BOARD-01:** TASKS.md e BOARD.md atualizados

**Cenários de Teste:**

| ID | Cenário | Tipo |
|----|---------|------|
| CT01 | Cache hit → retorna profile sem executar detectores | Happy path |
| CT02 | Cache miss → discover() executado, resultado cacheado | Happy path |
| CT03 | Invalidação por hash mismatch (pyproject.toml alterado) → recálculo | Edge |
| CT04 | Cache corrompido (JSON inválido) → fallback graceful para discover() | Edge |
| CT05 | TTL expirado → cache ignorado, novo discover() | Edge |
| CT06 | Cache vazio → comporta como miss | Edge |

### US-002 — Injeção de Contexto Automática (2.0 SP)

| Campo | Detalhe |
|-------|---------|
| **Descrição** | Hermes Agent recebe o ProjectProfile automaticamente no contexto de cada task. Elimina repetição manual de 3-5 parágrafos de stack/arquitetura. |
| **Jira** | SCRUM-65 (a criar) |
| **Status** | ✅ Concluído — CLI `apos context`, 29 testes, 97% coverage CLI, 94% coverage cache |

**Definition of Ready (DoR):**
- [x] **DOR-01:** US-001 concluída (cache de profile existe em disco)
- [x] **DOR-02:** CLI `apos context` projetada antes de codificar (design da interface)
- [x] **DOR-03:** Template de saída markdown definido (quais campos, formato)
- [x] **DOR-04:** Testes existentes passam
- [x] **DOR-05:** Sem dependências externas
- [x] **DOR-06:** Aprovado pelo PO: escopo cabe em 2.0 SP

**Definition of Done (DoD):**
- [x] **COD-01:** CLI `apos context` exibe profile atual como markdown formatado
- [x] **COD-02:** Saída inclui: stack, framework, database, cloud, módulos, padrões
- [x] **COD-03:** Integração com Hermes: contexto injetado via template string
- [x] **COD-04:** Sem cache → mensagem clara "rode `apos discover` primeiro"
- [x] **TST-01:** `pytest tests/unit/test_context_cli/ -v` — 4 cenários
- [x] **TST-02:** Coverage ≥80%
- [x] **TST-03:** Zero regressão
- [x] **JIRA-01:** SCRUM-65 movido para Concluído
- [x] **BOARD-01:** TASKS.md e BOARD.md atualizados

**Cenários de Teste:**

| ID | Cenário | Tipo |
|----|---------|------|
| CT01 | `apos context` com cache válido → markdown com stack, módulos, padrões | Happy |
| CT02 | `apos context` sem cache → mensagem "rode discover primeiro" | Edge |
| CT03 | Profile parcial → apenas campos preenchidos aparecem | Edge |
| CT04 | Saída markdown válida (parseável) | Happy |

## Tasks Stretch (1.5 SP)

### US-003 — Validação Código vs Documentação (1.5 SP) — Stretch

| Campo | Detalhe |
|-------|---------|
| **Descrição** | Comando que compara o profile descoberto com a documentação em docs/SDD/. Detecta divergências entre código e docs antes que virem dívida. |
| **Jira** | SCRUM-66 (a criar) |
| **Status** | stretch |

**Definition of Ready (DoR):**
- [x] **DOR-01:** US-001 concluída (cache de profile operacional)
- [x] **DOR-02:** BootstrapGateV2 existente (validação de fundações)
- [x] **DOR-03:** Documentos SDD de exemplo lidos (entender estrutura para parse)
- [x] **DOR-04:** Formato do relatório de divergência definido (consistentes/diferentes/ausentes)
- [x] **DOR-05:** Validado contra 2 repositórios (APOS + Meu PDI backend/)
- [x] **DOR-06:** Aprovado pelo PO: escopo cabe em 1.5 SP

**Definition of Done (DoD):**
- [x] **COD-01:** CLI `apos validate` compara profile vs docs/SDD/
- [x] **COD-02:** Relatório: consistentes ✅, divergentes ❌, ausentes ⚠️
- [x] **COD-03:** Zero falsos positivos nas primeiras 5 execuções em repositórios reais
- [x] **COD-04:** Validado contra Meu PDI (backend/) e APOS (raiz)
- [x] **TST-01:** `pytest tests/unit/test_validate/ -v` — 4 cenários
- [x] **TST-02:** Coverage ≥80%
- [x] **TST-03:** Zero regressão
- [x] **JIRA-01:** SCRUM-66 movido para Concluído
- [x] **BOARD-01:** TASKS.md e BOARD.md atualizados

**Cenários de Teste:**

| ID | Cenário | Tipo |
|----|---------|------|
| CT01 | Stack coincide com docs → relatório 100% verde | Happy |
| CT02 | Framework diferente do documentado → alerta de divergência ❌ | Edge |
| CT03 | SDD sem código correspondente → warning | Edge |
| CT04 | Código sem SDD correspondente → warning | Edge |

---

## 📌 Commits de Rastreamento (Audit Trail)

*Registre aqui os commits a cada task concluída durante a sprint.*

| Commit | Task | Descrição |
|--------|------|-----------|
| `[hash]` | `US-001` | ProjectCache em disco (JSON, TTL, hash SHA256) |
| `[hash]` | `US-002` | CLI apos context + 29 testes (94-97% coverage) |

**Total de commits rastreados:** 0[hash]` | `US-002` | CLI apos context + 29 testes (94-97% coverage) |

**Total de commits rastreados:** 0

---

## Progress Summary

| Task | Completion | SP | Notes |
|------|-----------|-----|-------|
| US-001 (Cache Profile) | 100% | 1.5 | SCRUM-64 | ✅ Cache em disco, TTL, hash, fallback |
| US-002 (Inject Context) | 100% | 2.0 | SCRUM-65 | ✅ CLI `apos context`, 29 testes, 94%+ coverage |
| US-003 (Validate Code vs Docs) | 0% | 1.5 | SCRUM-66 | 🟡 Stretch |
| **CORE TOTAL** | **100%** | **3.5 SP** | | |
| **STRETCH TOTAL** | **0%** | **5.0 SP** | | |

---

## Timeline

```
D1: US-001 (Cache) — implementar cache em disco + TTL
D2: US-001 finalize + US-002 (Context) — CLI apos context
D3: US-002 finalize + US-003 (Validate) — stretch 
```

---

**Sprint Quality Gate:** `python -m apos validate-sprint --sprint-root docs/releases/R1/sprint-1.2/`
