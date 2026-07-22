# Regenerar Token Jira com Permissões Admin — Guia Passo a Passo

**Objetivo:** Dar permissões de escrita (criar projeto + issues) à API  
**Tempo:** 5 minutos  
**Resultado:** Token com permissões completas

---

## 🔐 PASSO 1: Acessar Gerenciador de Tokens

1. Abra seu navegador
2. Vá para: **https://id.atlassian.com/manage-profile/security/api-tokens**
3. Você será pedido para fazer login se não estiver
4. Entre com: **jadergreiner@gmail.com**

![Login Atlassian]

---

## 🗑️ PASSO 2: Revogar Token Antigo

Na página de API tokens, você verá uma lista de tokens:

```
API tokens
├─ apos-import (created 2026-07-23)
│  ATATT3xFfGF0e-9W9BTuYABaSDNIeHeFtqotp8cmgcCJ00eFgx4xv-pzB9xu...
```

1. **Encontre** o token que começa com `ATATT3xFfGF0e...`
2. **Clique em "..."** (menu de três pontos) no final da linha
3. **Clique** "Revoke"
4. **Confirme** "Revoke API token"

✓ Token antigo foi revogado

---

## ✨ PASSO 3: Criar Novo Token com Permissões Completas

1. **Clique** "Create API token" (botão no topo)

2. **Preencha:**
   ```
   Label: apos-admin
   (deixe os outros campos em branco)
   ```

3. **Clique** "Create"

4. **Copie o token gerado:**
   ```
   Token (selecione tudo e copie):
   ATATT3xFfGF0e... (novo token)
   ```

   ⚠️ **IMPORTANTE:** Copie AGORA! Você não conseguirá ver depois!

---

## 📝 PASSO 4: Atualizar `.env` com Novo Token

1. **Abra arquivo:** `C:\repo\APOS\.env`

2. **Encontre a linha:**
   ```
   JIRA_TOKEN=ATATT3xFfGF0e-9W9BTuYABaSDNIeHeFtqotp8cmgcCJ00eFgx4xv-pzB9xu...
   ```

3. **Substitua pelo novo token:**
   ```
   JIRA_TOKEN=seu-novo-token-aqui
   ```

4. **Salve** (Ctrl+S)

---

## 🧪 PASSO 5: Testar Novo Token

Abra PowerShell e execute:

```powershell
cd C:\repo\APOS
python scripts/jira_setup_complete.py
```

**Resultado esperado:**

```
🔗 Jira: https://jadergreiner.atlassian.net
📧 Email: jadergreiner@gmail.com

FASE 1: Projeto SCRUM
🔨 Criando projeto SCRUM...
✓ Projeto criado: SCRUM

⏳ Aguardando projeto estar pronto...
✓ Projeto SCRUM pronto!

FASE 2: Importar Tasks
📋 Importando 4 tasks:

  ✓ T0.3.1 → SCRUM-1
  ✓ T0.3.2 → SCRUM-2
  ✓ T0.3.3 → SCRUM-3
  ✓ T0.3.4 → SCRUM-4

✅ SETUP COMPLETO!
✓ Projeto: SCRUM
✓ Tasks importadas: 4/4
```

Se vir isso: ✅ **Funcionou!**

---

## 🚀 Próximos Passos

1. **Acesse Jira:**
   ```
   https://jadergreiner.atlassian.net/jira/software/projects/SCRUM
   ```

2. **Veja as 4 issues criadas:**
   - SCRUM-1: Especificacao Tecnica
   - SCRUM-2: Design de API REST
   - SCRUM-3: Implementacao Plugin Jira
   - SCRUM-4: Trust Score Engine

3. **Inicie T0.3.5 Piloto:**
   ```
   6 dias de validação com dados reais
   ```

---

## ⚠️ Troubleshooting

### "Token still says read-only"
→ Aguarde 30 segundos após criar  
→ Feche PowerShell e abra novamente  
→ Execute script novamente

### "HTTP 403 - Forbidden"
→ Token não tem permissão de admin  
→ Verifique que copiu o token COMPLETO  
→ Tente regenerar novamente

### "Project already exists"
→ Projeto foi criado mas não viu confirmação  
→ Execute: `python scripts/jira_setup_auto.py`  
→ Ele vai detectar e importar tasks

### Script para mas não mostra erro
→ Pode estar aguardando inicialização  
→ Deixe rodar por 1-2 minutos

---

## 📋 Checklist de Conclusão

- [ ] 1. Acessei https://id.atlassian.com/manage-profile/security/api-tokens
- [ ] 2. Revoquei token antigo (ATATT3xFfGF0e...)
- [ ] 3. Criei novo token com label "apos-admin"
- [ ] 4. Copiei novo token
- [ ] 5. Atualizei .env com novo token
- [ ] 6. Testei: `python scripts/jira_setup_complete.py`
- [ ] 7. Vejo 4 issues em SCRUM (SCRUM-1 até SCRUM-4)
- [ ] 8. Pronto para T0.3.5 Piloto!

---

## 🎉 Quando Estiver Pronto

Você terá:
- ✅ Token Jira com permissões completas
- ✅ Projeto SCRUM criado automaticamente
- ✅ 4 tasks importadas (SCRUM-1, 2, 3, 4)
- ✅ Pronto para começar Piloto (6 dias de validação)

**Tempo total: 5 minutos + ~2 minutos script = 7 minutos**

---

## 🔒 Segurança

⚠️ **Importante:** Nunca compartilhe seu token! Se vazar:
1. Revogue imediatamente em https://id.atlassian.com/manage-profile/security/api-tokens
2. Crie novo token
3. Atualize .env

---

**Guia criado:** 2026-07-23  
**Próxima ação:** Seguir passos 1-5 acima
