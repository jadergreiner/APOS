# APOS Setup & First Use - Guia Prático

**Versão:** 1.0  
**Estimado:** 15-20 minutos (primeira vez)  
**Nível:** Iniciante (sem conhecimento técnico necessário)  
**Última atualização:** 2026-07-29

---

## Visão Geral do Tutorial

Este guia cobre **tudo que você precisa fazer** para:

1. ✅ Instalar plugin Jira
2. ✅ Configurar API key
3. ✅ Sincronizar dados iniciais
4. ✅ Ver dashboard
5. ✅ Vincular primeira tarefa a OKR

Após 15 min, APOS estará detectando features orfas automaticamente.

---

## Pré-requisitos

Antes de começar, verifique:

- ✅ **Jira Cloud account** (com permissão Admin)
- ✅ **Email confirmado** no Jira
- ✅ **Browser moderno:** Chrome 90+, Firefox 88+, Safari 14+
- ✅ **Acesso a email** (para receber API key)

**Não tem Jira?** Crie uma conta gratuita em [jira.com](https://www.atlassian.com/software/jira/free)

---

## Step 1: Instalar Plugin Jira (2-3 min)

### 1.1 Acessar Jira Marketplace

1. Abra **Jira Cloud**
2. Click no ícone de **configurações** (⚙️) no canto superior direito
3. Selecione **"Apps"** → **"Find new apps"**

![Jira Apps Menu]

Ou acesse direto: [Jira Marketplace - APOS](https://marketplace.atlassian.com/apps/1234567890/apos)

### 1.2 Buscar e Instalar APOS

1. Na barra de busca, digite `APOS`
2. Clique no resultado **"APOS - Semantic Context for Jira"**
3. Click no botão **"Get it now"**
4. Selecione o **workspace** onde deseja instalar

### 1.3 Autorizar Permissões

Plugin pede acesso a:
- ✅ **Ler issues/tasks** (necessário para detectar orfas)
- ✅ **Ler custom fields** (necessário para encontrar OKRs)
- ✅ **Webhooks** (necessário para sync automático)

Click **"Authorize"** para confirmar.

**Resultado esperado:** ✅ "Plugin instalado com sucesso"

---

## Step 2: Obter API Key (2 min)

Você recebeu um email: **"APOS - Ative sua conta"**

### 2.1 Confirmar Email

1. Abra seu **email**
2. Procure por mensagem de "APOS Team" (verificar spam se necessário)
3. Click no link **"Activate Account"**
4. Você será redirecionado para **apos.io** (seu dashboard)

### 2.2 Copiar API Key

1. No dashboard, vá para **Settings** → **API Keys**
2. Você verá uma chave já gerada:
   ```
   pk_live_1a2b3c4d5e6f7g8h9i0j
   ```
3. Click no ícone de **"copy"** (📋)
4. Guarde essa chave em local seguro (não compartilhe!)

**Importante:** Essa chave é **única para seu account**. Se perder, regenere em Settings.

---

## Step 3: Configurar Plugin Jira (3-5 min)

### 3.1 Acessar Plugin Settings

1. Volte para **Jira Cloud**
2. Procure pelo ícone de **APOS** (🧠) na barra lateral esquerda
3. Plugin abre um **sidebar**
4. Click em **"Settings"** (ícone ⚙️)

### 3.2 Cole API Key

1. Campo: **"API Key"**
2. Cole a chave copiada no Step 2.2
3. Campo: **"API Endpoint"**
4. URL padrão: `https://api.apos.io/api/v1` (deixe como está)
5. Click **"Test Connection"**

### 3.3 Validar Conexão

Você verá:
- ✅ **Verde "Connected"** = sucesso! API key válida
- ❌ **Vermelho "Failed"** = verifique:
  - API key foi copiada corretamente?
  - Seu email foi confirmado?
  - Firewall/proxy bloqueando?

Se falhar, email: jadergreiner@gmail.com

### 3.4 Salvar Settings

Click **"Save"**

**Status esperado:** ✅ "Settings saved successfully"

---

## Step 4: Sincronizar Dados Iniciais (5-10 min)

### 4.1 Iniciar Sync

1. No sidebar do APOS, você verá:
   ```
   📊 Dashboard
   🔄 Sync Status
   ⚙️ Settings
   ```

2. Click em **"Sync Status"**
3. Click no botão azul **"Sync Now"**
4. Plugin inicia sincronização de todas as tasks

### 4.2 Monitorar Progresso

Você verá uma barra de progresso:
```
Syncing Jira data...
50/247 tasks processed (20%)
Estimated time: 1 minute...
```

**O que acontece:**
- Backend baixa todas as tasks do seu projeto
- Verifica qual tem OKR linkado
- Identifica "features orfas" (sem OKR)
- Calcula Trust Score

**Tempo esperado:** 1-5 minutos (dependendo do volume)

### 4.3 Conclusão

Quando concluir, você verá:
```
✅ Sync completed!
- Total tasks: 247
- Linked tasks: 210
- Orphan tasks: 37
- Trust Score: 0.78
```

---

## Step 5: Ver Dashboard (2 min)

### 5.1 Abrir Dashboard

1. No sidebar, click em **"Dashboard"**
2. Você verá a página principal do APOS:

```
╔════════════════════════════════════════╗
║         APOS Dashboard - R0            ║
╠════════════════════════════════════════╣
║                                        ║
║  📊 Trust Score: 0.78 (Healthy)       ║
║                                        ║
║  Breakdown:                            ║
║  - Coverage:    85% (210/247 linked)   ║
║  - Quality:     72% (links valid)      ║
║  - Consistency: 95% (no conflicts)     ║
║                                        ║
║  🚨 Orphan Tasks: 37                   ║
║     Time to fix: ~2 hours              ║
║                                        ║
║  ⏱️  Last sync: 2 min ago              ║
║                                        ║
╚════════════════════════════════════════╝
```

### 5.2 Interpretar Scores

**Trust Score (0.0-1.0):**

| Score | Status | Significado |
|-------|--------|-------------|
| 0.7-1.0 | ✅ Healthy | Seu contexto está claro, continue |
| 0.3-0.7 | ⚠️ Caution | Algumas gaps, revise orfas |
| 0.0-0.3 | 🔴 Critical | Muitas orfas, contexto quebrado |

**Coverage (% de tasks linked):**
- 85% = 210 de 247 tasks têm OKR
- 15% = 37 tasks SEM OKR (orfas)

**Próximo passo:** Vincular as 37 orfas!

---

## Step 6: Vincular Primeira Tarefa a OKR (3 min)

### 6.1 Ver Lista de Orfas

1. No dashboard, click em **"View orphans"** ou **"37 orphan tasks"**
2. Você verá uma lista:

```
Orphan Tasks (37)

1. JIRA-124: "Refatorar banco de dados"
   Status: backlog | Priority: medium
   Created: 7 days ago

2. JIRA-130: "Atualizar dependências npm"
   Status: in_progress | Priority: low
   Created: 12 days ago

...
```

### 6.2 Vincular Uma Tarefa

1. Clique em qualquer tarefa (ex: JIRA-124)
2. Modal abre com opções:

```
╔═════════════════════════════════════╗
║ Link OKR to JIRA-124               ║
╠═════════════════════════════════════╣
║                                     ║
║ Task: Refatorar banco de dados      ║
║                                     ║
║ Which OKR does this support?       ║
║ ┌─────────────────────────────────┐║
║ │ Select OKR...                  ▼││
║ │ • OKR-2026-Q3-001               ││
║ │   "Aumentar transparência       ││
║ │    estratégica"                 ││
║ │ • OKR-2026-Q3-002               ││
║ │   "Melhorar performance DB"     ││
║ │ • OKR-2026-Q3-003               ││
║ │   "Reduzir tech debt"           ││
║ └─────────────────────────────────┘║
║                                     ║
║ Confidence: [████████░] 0.85       ║
║                                     ║
║ [Cancel]  [Link OKR]                ║
╚═════════════════════════════════════╝
```

### 6.3 Selecionar OKR

1. Click na dropdown **"Select OKR"**
2. Escolha o OKR que faz sense para essa tarefa
3. Exemplo: "Refatorar DB" → "Melhorar performance DB"
4. Confidence score aparece automaticamente (ex: 0.85)

### 6.4 Confirmar

1. Click **"Link OKR"**
2. Modal fecha
3. Você verá feedback:

```
✅ Task linked!

JIRA-124 → OKR-2026-Q3-002
Trust Score recalculated: 0.78 → 0.81

Dashboard atualizado em tempo real.
```

**Parabéns!** Você vinculou sua primeira tarefa! 🎉

---

## Step 7: Daily Usage (Rotina)

### 7.1 Novo Task Criado

1. Dev/PM cria um novo task no Jira
2. APOS detecta automaticamente (via webhook)
3. Se task tem OKR histórico similar → auto-sugere
4. Se não → marca como orfã + notifica

### 7.2 Receber Alertas

Plugin envia alertas automáticos (Slack/email, R1):
- "3 novos orfas detectados"
- "Trust Score caiu de 0.81 → 0.75"
- "Orphan JIRA-150 está blocking"

### 7.3 Vincular no Dashboard

1. Click em "Orphans" no sidebar
2. Veja lista atualizada
3. Vincule os novos orfas (3-5 min)
4. Trust Score sobe automaticamente

### 7.4 Recalcular Score

Trust Score recalcula **automaticamente** quando você:
- Vincula uma tarefa
- Deleta uma tarefa
- Muda status de uma tarefa
- Executa sync manual

Não precisa fazer nada — APOS cuida disso!

---

## Troubleshooting

### Problema: Plugin não aparece no Jira

**Solução:**
1. F5 (refresh) na página
2. Cache do browser pode estar velha
3. Ctrl+Shift+Delete (clear cache)
4. Abra Jira novamente

### Problema: "Connection test failed"

**Causas possíveis:**
1. **API key inválida** — Regenere em Settings
2. **Email não confirmado** — Check email spam folder
3. **Firewall** — Contate TI se estiver em empresa
4. **API offline** — Tente novamente em 5 min

**Teste rápido:**
```bash
curl -X GET "https://api.apos.io/api/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Problema: Sync não termina

**Solução:**
1. Aguarde (sync grande pode levar 10+ min)
2. Se > 15 min, click "Cancel" e tente novamente
3. Se persistir, email: jadergreiner@gmail.com

### Problema: Trust Score não muda após vincular

**Solução:**
1. Cache TTL é 1 hora
2. Click em **"Recalculate Now"** para forçar
3. Dashboard atualiza em <5 segundos

### Problema: OKR não aparece na dropdown

**Solução:**
1. OKR precisa estar em um desses locais:
   - Custom field no Jira
   - Notion database linkada
   - Spreadsheet linkado
2. Verifique que OKR foi configurado no Step 3
3. Se ainda não aparecer, email: jadergreiner@gmail.com

---

## Próximos Passos

Após completar este tutorial, você está pronto para:

1. **[Usar no dia-a-dia](README.md#fluxo-de-uso-típico)** — workflow diário
2. **[Integração Slack](README.md#próximos-passos)** — alertas automáticos (R1)
3. **[Documentação API](API_DOCS.md)** — se você é desenvolvedor

---

## FAQ Rápido

**P: Preciso de conhecimento técnico para usar APOS?**
A: Não! Interface é visual, clique e pronto. Conhecimento técnico é opcional.

**P: Posso desfazer um link (OKR)?**
A: Sim, click em "Unlink" no modal. Trust Score recalcula automaticamente.

**P: E se eu deleto uma task no Jira?**
A: APOS sincroniza automaticamente. Task desaparece do dashboard.

**P: Quantas tarefas APOS consegue gerenciar?**
A: 10K+ tasks (testado). Recomendação: use filtros se > 1K tasks.

**P: Posso mudar meu API key?**
A: Sim, Settings → API Keys → Regenerate (antiga expira automaticamente).

---

## Contato & Suporte

- **Email:** jadergreiner@gmail.com (tempo de resposta: <2h)
- **Docs:** [README.md](README.md) para conceitos
- **API Docs:** [API_DOCS.md](API_DOCS.md) para developers
- **FAQ:** [FAQ.md](FAQ.md) para mais troubleshooting

---

**Primeira vez usando APOS?** Parabéns! Você agora tem contexto semântico claro. 🚀

**Última atualização:** 2026-07-29
