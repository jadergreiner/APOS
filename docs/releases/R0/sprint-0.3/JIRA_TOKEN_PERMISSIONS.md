# Jira Token Permissions — Diagnóstico

**Status:** Token atual tem permissões **read-only**  
**Data:** 2026-07-23  
**Solução:** 2 opções (regenerar ou criar manualmente)

---

## 🔍 Diagnóstico

Token atual (`JIRA_TOKEN` em `.env`):
- ✅ **Leitura (GET):** Funciona
  - `/rest/api/2/project/search` — OK
  - Listar projetos — OK
  - Buscar issues — OK

- ❌ **Escrita (POST/PUT):** Bloqueada
  - Criar projeto — 401 Unauthorized
  - Criar issues — Funcionaria se projeto existisse
  - Atualizar issues — Bloqueado

**Erro:** "You are not authenticated for this operation"

---

## 💡 Soluções

### Opção 1: Regenerar Token (Recomendado para Automação Completa)

Se quiser automação 100% via API (sem criação manual):

1. **Acesse:**
   ```
   https://id.atlassian.com/manage-profile/security/api-tokens
   ```

2. **Revogue token atual:**
   - Encontre `ATATT3xFfGF0e...`
   - Clique "Revoke"

3. **Crie novo token:**
   - "Create API token"
   - Nome: `apos-admin` (ou similar)
   - **Permissões:** Deixe todas as permissões (default)
   - Copie o token

4. **Atualize `.env`:**
   ```
   JIRA_TOKEN=seu-novo-token-aqui
   ```

5. **Teste criação:**
   ```bash
   python scripts/jira_setup_complete.py
   # Deve criar projeto + importar tasks em ~2 min
   ```

### Opção 2: Setup Manual (2 minutos, sem novo token)

Mantendo token atual e criando projeto manualmente:

1. **Acesse Jira:**
   ```
   https://jadergreiner.atlassian.net
   ```

2. **Crie projeto SCRUM:**
   - Projects → Create project
   - Type: Scrum (ou Kanban)
   - Name: SCRUM
   - Key: SCRUM
   - Lead: Jader Greiner
   - Click Create

3. **Aguarde ~30 segundos**

4. **Execute import:**
   ```bash
   python scripts/jira_setup_auto.py
   # Detecta projeto + importa 4 tasks automaticamente
   ```

---

## 🔐 Diferença de Permissões

| Operação | Token Atual | Token New (Admin) |
|----------|------------|------------------|
| Listar projetos | ✓ | ✓ |
| Listar issues | ✓ | ✓ |
| **Criar projeto** | ✗ | ✓ |
| **Criar issues** | ✗ (sem projeto) | ✓ |
| **Atualizar issues** | ✗ | ✓ |
| **Deletar** | ✗ | ✓ |

---

## 📋 Script Recomendado por Permissão

| Permissão | Script | Tempo |
|-----------|--------|-------|
| Read-only (atual) | `jira_setup_auto.py` | 2-3m (com setup manual) |
| Admin (novo token) | `jira_setup_complete.py` | ~2m (100% automático) |

---

## ⚡ Quick Decision

**Se quer agora:**
→ Opção 2 (Setup manual, 2 min)
→ `python scripts/jira_setup_auto.py`

**Se quer automação futura:**
→ Opção 1 (Regenerar token)
→ `python scripts/jira_setup_complete.py`

---

## 🚀 Recomendação

**Recomendo Opção 2 para agora:**
1. Crie projeto SCRUM manualmente no Jira web (2 min)
2. Execute: `python scripts/jira_setup_auto.py`
3. 4 tasks importadas automaticamente
4. Pronto para T0.3.5 Piloto

**Depois, se quiser:**
1. Regenere token com permissões admin
2. Use `jira_setup_complete.py` para automação futura

---

## 📝 Resumo

```bash
# AGORA (Opção 2 - Recomendado):
# 1. Crie projeto SCRUM manualmente no Jira (2 min)
# 2. Execute:
python scripts/jira_setup_auto.py
# ✓ Setup completo em ~1 min

# DEPOIS (Opção 1 - Se quiser):
# 1. Regenere token em https://id.atlassian.com/manage-profile/security/api-tokens
# 2. Atualize .env
# 3. Execute:
python scripts/jira_setup_complete.py
# ✓ Setup 100% automático próxima vez
```

---

**Análise feita:** 2026-07-23  
**Status:** Token verificado, soluções documentadas
