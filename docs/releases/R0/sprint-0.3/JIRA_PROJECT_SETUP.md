# Jira Project Setup — SCRUM

**Status:** Manual setup necessário antes de executar task import  
**Token:** ✅ Já configurado em `.env`  
**Data:** 2026-07-23

---

## Quick Start

### 1️⃣ Criar Projeto SCRUM no Jira

1. Acesse: https://jadergreiner.atlassian.net
2. Clique "Projects" → "Create project"
3. Preencha:
   - **Project type:** Scrum (ou Kanban)
   - **Project name:** SCRUM (ou seu nome preferido)
   - **Project key:** SCRUM (automático)
   - **Project lead:** Jader Greiner (você)
4. Clique "Create"

**Espere:** 30-60 segundos para inicialização

### 2️⃣ Verificar Acesso

```bash
cd C:\repo\APOS

# Test com o token já configurado em .env
python scripts/jira_create_tasks.py
```

**Resultado esperado:**
```
✓ T0.3.1 → SCRUM-1
✓ T0.3.2 → SCRUM-2
✓ T0.3.3 → SCRUM-3
✓ T0.3.4 → SCRUM-4

Criadas: 4 / Falhadas: 0
```

---

## Se Preferir Outro Nome de Projeto

Se quiser usar um nome diferente (ex: `R0` em vez de `SCRUM`), atualize o script:

```bash
# Edite: scripts/jira_create_tasks.py
# Linha ~200:
creator.create_issues_from_tasks("R0", tasks)  # Mude "SCRUM" para "R0"
```

---

## Troubleshooting

### "403 Forbidden" quando criar projeto
→ Você pode não ter permissão de admin  
→ Contacte o admin da Jira Cloud

### "Projeto criado mas não aparece em listagem"
→ Aguarde 1-2 minutos e tente novamente  
→ Recarregue página no navegador

### Script ainda diz "project doesn't exist"
→ Confirme que o projeto key exato está correto  
→ Verifique em: https://jadergreiner.atlassian.net/jira/projects

---

## Depois de Criar

Após criar o projeto SCRUM, execute:

```bash
python scripts/jira_create_tasks.py
```

**4 issues serão criadas automaticamente:**
- SCRUM-1: T0.3.1 Especificacao Tecnica
- SCRUM-2: T0.3.2 Design de API REST  
- SCRUM-3: T0.3.3 Implementacao Plugin Jira
- SCRUM-4: T0.3.4 Trust Score Engine

Pronto para iniciar T0.3.5 Piloto! 🚀

---

**Setup levará:** ~2 minutos  
**Criação de issues:** ~30 segundos
