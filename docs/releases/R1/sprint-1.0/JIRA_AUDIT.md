# 📊 Jira Audit — R1 Sprint 1.0

**Data:** 2026-07-21  
**Status:** ⚠️ INCONSISTÊNCIA ENCONTRADA

---

## Achados

### ✅ Esperado (Correto)

| Jira Key | Task ID | Descrição | Status |
|----------|---------|-----------|--------|
| SCRUM-55 | T1.1.1 | Tests agent_harness (1.587 LOC) | ✅ |
| SCRUM-56 | T1.1.2 | Tests capability_harness | ✅ |
| SCRUM-57 | T1.1.3 | Implementar ProjectAdapter core | ✅ |
| SCRUM-58 | T1.1.4 | Testes ProjectAdapter em Meu PDI | ✅ |

### ❌ EXTRAS (Não esperadas, devem ser removidas)

| Jira Key | Descrição | Status |
|----------|-----------|--------|
| SCRUM-52 | R1.1 - ProjectAdapter core — descoberta de contexto do projeto | ❌ REMOVER |
| SCRUM-53 | R1.2 - Bootstrap Gate 2.0 — init guiado por contexto | ❌ REMOVER |
| SCRUM-54 | R1.3 - Domain Ontology Adapter — ontologia do projeto | ❌ REMOVER |

---

## Situação

- **Jira Sprint R1:** 7 issues (4 esperadas + 3 extras)
- **TASKS.md local:** 9 tarefas registradas (esperamos 4 + investigar 5 extras)
- **Sincronização:** `.jira_sync_history.json` mapeia apenas 4 issues (SCRUM-55-58)

---

## Ação Necessária

### 1. ⚠️ REMOVER do Jira (Manual)

Abra https://jadergreiner.atlassian.net e:

1. Vá para Sprint **"SCRUM R1 Sprint 1.0"**
2. Remova as 3 issues do sprint (move para backlog):
   - [ ] SCRUM-52
   - [ ] SCRUM-53
   - [ ] SCRUM-54

**Alternativa CLI (quando API permitir):**
```bash
python scripts/jira_remove_issue.py SCRUM-52 SCRUM-53 SCRUM-54
```

### 2. 🔍 INVESTIGAR TASKS.md

**Por que TASKS.md tem 9 tarefas se esperamos 4?**

```bash
grep "^| T" docs/releases/R1/sprint-1.0/TASKS.md
```

Resultado esperado: 4 linhas (T1.1.1 a T1.1.4)  
Resultado atual: 9 linhas (investigar o que são as 5 extras)

---

## Próximos Passos

1. [ ] Remover SCRUM-52, 53, 54 do Sprint (via Jira UI)
2. [ ] Re-auditar: `python scripts/jira_audit.py`
3. [ ] Revisar TASKS.md — por que 9 tasks?
4. [ ] Sincronizar novamente se necessário: `python scripts/jira_sync_tasks.py --force`

---

**Relatório gerado:** 2026-07-21 23:52  
**Script:** `scripts/jira_audit.py`
