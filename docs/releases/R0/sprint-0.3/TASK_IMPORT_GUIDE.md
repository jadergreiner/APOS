# Task Import to Jira — Guia Prático

**Sprint:** 0.3 - Beta Prep  
**Task:** T0.3.5 — Suporte para Piloto + Task Import  
**Status:** ✅ Scripts prontos (Demo + Real)  
**Data:** 2026-07-23

---

## Visão Geral

Dois scripts Python para gerenciar tasks no Jira:

1. **`jira_create_tasks_demo.py`** — Preview dos payloads (sem autenticação)
2. **`jira_create_tasks.py`** — Cria issues reais (com autenticação)

Ambos leem `TASKS.md` e geram issues no projeto SCRUM.

---

## Quick Start

### 1️⃣ Gerar Token Jira

1. Acesse: [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Clique "Create API token"
3. Nomeie: `apos-import`
4. Copie o token gerado

### 2️⃣ Executar Demo (sem auth)

```bash
cd C:\repo\APOS
python scripts/jira_create_tasks_demo.py
```

**Output:**
- Lista 4 tasks de Tier 1
- Mostra payloads JSON exatos
- Nenhuma chamada de API

### 3️⃣ Executar Real (com auth)

```bash
cd C:\repo\APOS
export JIRA_API_TOKEN='seu-token-aqui'
python scripts/jira_create_tasks.py
```

**Credenciais automáticas:**
- JIRA_URL: `https://jadergreiner.atlassian.net`
- JIRA_EMAIL: `jadergreiner@gmail.com`
- JIRA_API_TOKEN: (via env var)

---

## Tasks Criadas

| ID | Título | Duração | Descrição |
|----|--------|---------|-----------|
| T0.3.1 | Especificacao Tecnica | 1.5d | Design Plugin Jira + Trust Score |
| T0.3.2 | Design de API REST | 1.5d | Endpoints: /tasks, /okrs, /trust-score |
| T0.3.3 | Implementacao Plugin Jira | 2.0d | Integracao, webhooks, UI |
| T0.3.4 | Trust Score Engine | 1.5d | Score 0.0-1.0, calculo componentes |

**Labels automaticamente aplicadas:**
- `sprint-0.3`
- `apos-{task-id}` (ex: `apos-T0.3.1`)
- `duration-{duracao}` (ex: `duration-1.5d`)

---

## Troubleshooting

### Erro: "The target project doesn't exist..."

**Causa:** Projeto SCRUM não existe ou sem permissão

**Solução:**
1. Crie projeto SCRUM na Jira manualmente, OU
2. Atualize o script para usar projeto existente:
   ```python
   creator.create_issues_from_tasks("MEU_PROJETO", tasks)
   ```

### Erro: "Client must be authenticated..."

**Causa:** Token inválido ou expirado

**Solução:**
1. Regenere token em: https://id.atlassian.com/manage-profile/security/api-tokens
2. Confirme que tem permissão para criar issues
3. Revise se o email está correto

### Erro: "HTTP 404 - No endpoint POST..."

**Causa:** URL da Jira está incorreta

**Solução:**
- Confirme URL: deve ser `https://{seu-domínio}.atlassian.net`
- Atualize em `os.getenv("JIRA_URL")`

---

## Arquitetura

### TaskParser (Demo + Real)

```python
parser = TaskParser()
tasks = parser.read_markdown_table("docs/releases/R0/sprint-0.3/TASKS.md")
# → List[Dict] com ID, Titulo, Descricao, Duracao, Personas, Status
```

**Lê tabela markdown Tier 1:**
- Extrai apenas tarefas (T0.3.X)
- Para quando atinge "Tier 2" ou outra seção
- Mapeia colunas para dict

### JiraPayloadGenerator (Demo)

```python
payload = JiraPayloadGenerator.build_issue_payload("SCRUM", task)
# → Dict com estrutura exata da API v2
```

**Campos mapeados:**
| TASKS.md | Jira API | Campo |
|----------|----------|-------|
| ID | summary | Prefixo + título |
| Titulo | summary | Título completo |
| Descricao | description | Corpo da issue |
| Duracao | labels | Tag `duration-X` |
| Personas | description | Mencionado no corpo |

### JiraTaskCreator (Real)

```python
creator = JiraTaskCreator(url, email, token)
result = creator.create_issues_from_tasks("SCRUM", tasks)
# → Dict com total, created, failed, issues[]
```

**API usada:** `/rest/api/2/issue` (v2)

---

## Estrutura de Saída

### Demo Output

```json
[
  {
    "fields": {
      "project": {"key": "SCRUM"},
      "summary": "T0.3.1: Especificacao Tecnica (SPEC.md)",
      "description": "Design Plugin Jira + Trust Score...",
      "issuetype": {"name": "Task"},
      "labels": ["sprint-0.3", "apos-T0.3.1", "duration-1.5d"]
    }
  },
  ...
]
```

### Real Output

```json
{
  "total": 4,
  "created": 3,
  "failed": 1,
  "issues": [
    {
      "success": true,
      "task_id": "T0.3.1",
      "jira_key": "SCRUM-123",
      "jira_id": "10000"
    },
    {
      "success": false,
      "task_id": "T0.3.2",
      "error": "HTTP 400",
      "response": "..."
    }
  ]
}
```

---

## Próximos Passos (T0.3.5 Piloto)

1. ✅ Scripts prontos
2. ➡️ Usuário configura token + executa real
3. ➡️ Testa T0.3.5 com dados em Jira (6 dias)
4. ➡️ Coleta feedback de pilotos
5. ➡️ T0.3.6-8 (Métricas, Docs, Testing)

---

## Referência

- **SPEC.md**: Arquitetura de integração Jira
- **API_DESIGN.md**: Endpoints REST do sistema
- **TRUST_SCORE_GUIDE.md**: Engine de scoring
- **Plugin Jira (T0.3.3)**: Integração de UI

**Implementado por:** Claude Code  
**Data:** 2026-07-23
