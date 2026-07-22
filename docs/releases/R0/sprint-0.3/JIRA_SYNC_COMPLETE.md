# T0.3.3 Plugin Jira — Sincronização Completa ✅

**Status:** ✅ Implementado e Testado  
**Data:** 2026-07-21  
**Resultado:** 8/8 tasks sincronizadas com sucesso

---

## 🎯 O Que Foi Feito

### 1. Script de Sincronização (`scripts/jira_sync_tasks.py`)

**Lê** `docs/releases/R0/sprint-0.3/TASKS.md` → **Sincroniza** com Jira Cloud via API v2 → **Rastreia** localmente para idempotência

```bash
# Visualizar o que será feito (sem criar)
python scripts/jira_sync_tasks.py --dry-run

# Executar sincronização real
python scripts/jira_sync_tasks.py

# Forçar recriação de issues já existentes
python scripts/jira_sync_tasks.py --force
```

### 2. Parser de TASKS.md

Extrai automaticamente:
- **Task ID** (ex: T0.3.1, T0.3.2, ..., T0.3.8)
- **Título** (ex: "Especificacao Tecnica (SPEC.md)")
- **Descrição** (ex: "Design Plugin Jira + Trust Score + Deteccao Orfas")
- **Duração** (ex: "2d")
- **Personas** (ex: "Jader")
- **Tier** (ex: "Tier 1: Core / Must-Have")

### 3. Sincronização com Jira

**Payload criado** para cada issue:
```json
{
  "fields": {
    "project": {"key": "SCRUM"},
    "summary": "T0.3.3: Implementacao Plugin Jira",
    "description": "Integracao Jira API; webhooks; ...\n**Duração:** 2d\n**Personas:** Jader\n**Tier:** ### Tier 1: ...",
    "issuetype": {"name": "Tarefa"},  # ← Project usa "Tarefa" (português), não "Task"
    "labels": ["sprint-0.3", "apos-T0.3.3", "duration-2d", "tier-1-core"]
  }
}
```

### 4. Idempotência

**Arquivo local** (`.jira_sync_history.json`) rastreia task → jira_key:
```json
{
  "T0.3.1": "SCRUM-22",
  "T0.3.2": "SCRUM-23",
  "T0.3.3": "SCRUM-24",
  "T0.3.4": "SCRUM-25",
  "T0.3.5": "SCRUM-26",
  "T0.3.6": "SCRUM-27",
  "T0.3.7": "SCRUM-28",
  "T0.3.8": "SCRUM-29"
}
```

**Testado:**
- ✅ 1ª execução: criadas 8 issues (SCRUM-22 a SCRUM-29)
- ✅ 2ª execução: puladas 8 (0 duplicatas, resultado perfeito!)

---

## 📊 Issues Criadas

| Task | Jira Key | Título | Duração | Status |
|------|----------|--------|---------|--------|
| T0.3.1 | SCRUM-22 | Especificacao Tecnica (SPEC.md) | 1.5d | ✅ |
| T0.3.2 | SCRUM-23 | Design de API REST | 1.5d | ✅ |
| T0.3.3 | SCRUM-24 | Implementacao Plugin Jira | 2d | ✅ |
| T0.3.4 | SCRUM-25 | Trust Score Engine | 1.5d | ✅ |
| T0.3.5 | SCRUM-26 | Piloto com 3 Personas | 6d | ✅ |
| T0.3.6 | SCRUM-27 | Metricas Baseline + Tracking | 3d | ✅ |
| T0.3.7 | SCRUM-28 | Documentacao Completa | 2d | ✅ |
| T0.3.8 | SCRUM-29 | Testing + QA | 3d | ✅ |

---

## 🔧 Desafios Resolvidos

### 1. **Issue Type Inválido** ❌→✅
- **Problema:** Script tentava usar `"Task"` ou `"Story"` (inglês)
- **Erro:** "Especifique algum tipo de item válido"
- **Solução:** Descobrir que projeto SCRUM usa `"Tarefa"` (português)
  - Via UI do Jira: descoberto ao abrir diálogo de criação
  - Tipos disponíveis: Epic, **Tarefa**, História, Função, Bug

### 2. **API v2 Descontinuada para Search** ❌→✅
- **Problema:** `/rest/api/2/search` foi removido
- **Impacto:** Idempotência não funcionava
- **Solução:** Implementar rastreamento local com ``.jira_sync_history.json`
  - Mais robusto que depender de API de busca
  - Funciona offline
  - Rápido (sem latência de rede)

### 3. **Token Permissions** ❌→✅
- **Problema:** Token inicial tinha apenas permissão read-only
- **Solução:** Regenerar via Atlassian web UI com permissões admin
  - Teste de diagnóstico: GET funcionava, POST bloqueado (401)
  - Novo token criado: `apos-admin`

---

## 📝 Próximos Passos Recomendados

### 1. T0.3.4 — Trust Score Engine (Imediato)
- Issues já rastreadas no Jira
- Pode começar implementação

### 2. T0.3.5 — Piloto com 3 Personas (6 dias)
- Validação com dados reais
- Feedback cycles
- Necessário: access a Jira para rastrear progresso

### 3. GitHub Actions (Opcional)
- Automação: toda PR para `develop` = sincronização automática
- Requer: configuração de token Jira em GitHub Secrets
- Benefício: TASKS.md sempre sincronizado com Jira

---

## 🛠 Troubleshooting

### Script não sincroniza nada
```bash
# Verificar cache local
cat .jira_sync_history.json

# Se quiser recriar, use --force
python scripts/jira_sync_tasks.py --force
```

### Issue não aparece no Jira após criar
- Issues criadas vão para **Backlog** (fora do sprint Sprint 0.3)
- Para adicionar ao sprint: arrastar manualmente no Jira ou usar API v3
- Alternativa: adicionar campo "Sprint" no payload (requer Sprint ID)

### Token expirou
```bash
# Regenerar em: https://id.atlassian.com/manage-profile/security/api-tokens
# Atualizar: C:\repo\APOS\.env
JIRA_TOKEN=<novo-token>
```

---

## 📚 Referência

| Arquivo | Propósito |
|---------|-----------|
| `scripts/jira_sync_tasks.py` | Script de sincronização (850+ linhas) |
| `.jira_sync_history.json` | Rastreador local (task_id → jira_key) |
| `docs/releases/R0/sprint-0.3/TASKS.md` | Fonte de verdade de tasks |
| `.env` | Credenciais Jira (JIRA_TOKEN, JIRA_EMAIL, JIRA_URL) |

---

## ✅ Checklist de Conclusão

- [x] Script Python implementado (TasksParser + JiraSync classes)
- [x] Parsing de TASKS.md com 8 tasks extraídas corretamente
- [x] Sincronização com Jira Cloud via API v2
- [x] Idempotência testada e funcionando
- [x] Suporte a --dry-run e --force flags
- [x] Rastreamento local com .jira_sync_history.json
- [x] Documentação de desafios e soluções
- [x] Commit do código

---

**Status:** ✅ **T0.3.3 COMPLETO**

Próxima ação: T0.3.4 Trust Score Engine ou T0.3.5 Piloto

