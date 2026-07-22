# APOS FAQ - Perguntas Frequentes & Troubleshooting

**Versão:** 1.0  
**Categorias:** Setup, Funcionalidade, Performance, Data, Admin  
**Última atualização:** 2026-07-29

---

## 📋 Índice Rápido

- [Setup Issues](#-setup-issues)
- [Trust Score Issues](#-trust-score-issues)
- [Performance Issues](#-performance-issues)
- [Data Issues](#-data-issues)
- [OKR & Linking Issues](#-okr--linking-issues)
- [API Issues](#-api-issues)

---

## 🔧 Setup Issues

### P: Plugin não aparece no Jira após instalação

**R:** Isso é normal! Pode levar 2-5 minutos para ativar. Tente:

1. Atualize a página (F5)
2. Limpe cache do browser: Ctrl+Shift+Delete
3. Abra Jira novamente em uma aba nova
4. Se ainda não aparecer após 5 min:
   - Verifique se você tem **permissão Admin** (obrigatório para instalar apps)
   - Tente em um workspace diferente primeiro (para testar)
   - Email: jadergreiner@gmail.com

**Tempo esperado:** Plugin aparece em <5 min 90% das vezes.

---

### P: "Connection test failed" — o que fazer?

**R:** Erro de conexão entre plugin e backend. Siga checklist:

**1. Validar API Key:**
   - Copie novamente da chave de Settings (não colei errado?)
   - Regenere a chave se tiver dúvida: Settings → "Regenerate"
   - Tente cola de novo

**2. Validar Email Confirmado:**
   - Você confirmou o email? (Check sua caixa de entrada)
   - Não viu email? Check **spam folder**
   - Não chegou email? Click "Resend" em apos.io

**3. Testar Conectividade:**
   ```bash
   # Se você é tech-savvy, rode:
   curl -X GET "https://api.apos.io/api/v1/health" \
     -H "Authorization: Bearer YOUR_API_KEY"
   
   # Resposta esperada:
   # {"status": "healthy", ...}
   ```

**4. Firewall/Proxy:**
   - Você está em rede corporativa?
   - Admin pode estar bloqueando `api.apos.io`
   - Solução: usar VPN ou contatar TI

**5. Última opção:**
   - Email completo (screenshot do erro): jadergreiner@gmail.com
   - Resposta em <2 horas

---

### P: Meu workspace tem múltiplos projetos. APOS funciona com todos?

**R:** Sim! Mas você configura por **projeto**.

- Você pode ter múltiplos projects no Jira (R0, R1, Platform, etc)
- APOS sincroniza tasks de **todos** os projetos automaticamente
- Dashboard mostra stats **agregadas** (todos os projetos) ou **filtradas** (um projeto)
- API key funciona para todos os projetos

**Para filtrar um projeto específico:**
```bash
GET /api/v1/tasks?project_id=R0
GET /api/v1/trust-score?project_id=R0
GET /api/v1/orphans?project_id=R0
```

---

### P: Posso instalar APOS em múltiplos workspaces?

**R:** Não recomendado. Melhor usar **um workspace com múltiplos projetos**.

Se você realmente precisa (ex: Dev + Prod):
- Crie dois API keys diferentes (uma por workspace)
- Dashboard será separado
- Suportado, mas menos ideal

**Recomendação:** Use um workspace, múltiplos projetos (R0, R1, Platform, etc).

---

## 📊 Trust Score Issues

### P: Meu Trust Score é muito baixo (0.3) — o que significa?

**R:** Seu contexto semântico tem **problemas críticos**. Quebra down:

```
Score 0.3 =
- Coverage:    40% (muitas tasks sem OKR)
- Quality:     20% (links frágeis)
- Consistency: 80% (sem conflitos)
```

**Ações para melhorar:**

1. **Aumentar Coverage (mais urgente):**
   - Click "View Orphans"
   - Veja lista de tasks sem OKR
   - Vincule os OKRs pendentes (2-5 min por batch)
   - Score sobe rapidamente

2. **Melhorar Quality:**
   - Alguns links são fracos (confidence baixa)
   - Review links com score <0.7
   - Re-link se necessário

3. **Resultados esperados:**
   - Após vincular 50% dos orfas → score sobe a ~0.5
   - Após vincular 80% → score sobe a ~0.7
   - Após vincular todos → score → 0.85+

**Benchmarks:**
- Sprint 0.3 Piloto: começou em 0.62, acabou em 0.88 (3 dias)

---

### P: Score não muda após vincular uma tarefa

**R:** Cache TTL é **1 hora**. Opções:

1. **Esperar:** Dashboard atualiza automaticamente em <1h
2. **Forçar agora:** Click "Recalculate Now" (se disponível)
3. **Manual API:** 
   ```bash
   curl -X GET "https://api.apos.io/api/v1/trust-score?project_id=R0" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```

Dashboard visual atualiza em <5 segundos após recalc forçado.

---

### P: Trust Score subiu para 1.1 ou desceu para -0.5 — bug?

**R:** Sim, isso é bug! 😅 Trust Score **sempre** deve estar entre 0.0-1.0.

**Reporte isso:**
1. Screenshot do erro
2. Qual ação você fez? (linking, sync, etc)
3. Qual era o score antes?
4. Email: jadergreiner@gmail.com

Vamos investigar em <1h.

---

### P: Qual é um Trust Score "bom"?

**R:** Interpretação:

| Score | Status | Ação |
|-------|--------|------|
| 0.0-0.3 | 🔴 Critical | Muito trabalho, muitas orfas |
| 0.3-0.7 | ⚠️ Caution | Revisar links, melhorar cobertura |
| 0.7-0.85 | 💚 Good | Bom! Continue |
| 0.85-1.0 | ✅ Excellent | Excelente contexto, muito claro |

**Benchmark Sprint 0.3:**
- Piloto personas terminou com score médio **0.88**
- Começaram com **0.62**
- Melhoria: **+0.26 pontos em 3 dias**

**Target recomendado:** 0.75+ para produção

---

## ⚡ Performance Issues

### P: Dashboard carrega muito lento

**R:** Causas possíveis:

**1. Muitos tasks (>1000)?**
   - Use **filtros** para reduzir volume
   ```bash
   GET /tasks?project_id=R0&status=in_progress
   ```

**2. Browser cache velho?**
   - Limpe cache: Ctrl+Shift+Delete
   - Reabra plugin

**3. Latência de rede?**
   - Teste ping: `ping api.apos.io`
   - Ideal: <100ms
   - Aceitável: <500ms
   - Ruim: >500ms → contate seu ISP

**4. Servidor está lento?**
   ```bash
   curl -w "@curl-format.txt" -o /dev/null -s \
     "https://api.apos.io/api/v1/health"
   ```

**Se persistir:**
   - Email com: screenshot, número de tasks, país/região
   - Vamos investigar em <1h

---

### P: Plugin carrega lentamente quando abro Jira

**R:** Problema comum com primeiro carregamento. Soluções:

1. **Aguarde 10s** (primeira vez pode ser lenta)
2. **Limpe cache:** Ctrl+Shift+Delete
3. **Desabilite plugins desnecessários** (Jira Settings)
4. **Reinicie browser** completamente
5. **Use browser mais rápido:** Chrome < Firefox < Safari

Após primer loading, deve ser rápido (<1s).

---

### P: Webhook delays — sync atrasado

**R:** Webhook pode ter latência. Soluções:

1. **Tente novamente:** às vezes é fluke
2. **Força manual:** Click "Sync Now" (força sync imediato)
3. **Check Jira health:** Às vezes Jira está lento
4. **Firewall corporativo?** Pode estar bloqueando webhooks
5. Se >15min atrasado:
   - Email com timestamp: jadergreiner@gmail.com
   - Vamos investigar logs

**SLA esperado:** Webhook deliverá em <30s 95% das vezes.

---

## 💾 Data Issues

### P: Task desapareceu do dashboard

**R:** Siga o flowchart:

**1. Task foi deletada no Jira?**
   - APOS sincroniza automaticamente
   - Se deletou, desaparece de APOS também
   - Normal ✅

**2. Task foi movida de projeto?**
   - Se mudou para project não rastreado
   - Desaparece do dashboard
   - Normal ✅

**3. Task foi arquivada?**
   - Jira arquiva algumas issues
   - APOS sincroniza
   - Desaparece ✅

**4. Nenhum dos acima?**
   - Possível bug 🐛
   - Email com:
     - Task ID (JIRA-XXX)
     - Quando desapareceu?
     - Screenshot se possível
   - Vamos investigar audit logs

---

### P: OKR não aparece na dropdown "Select OKR"

**R:** OKR precisa estar em um desses formatos suportados:

**✅ Suportado:**
1. **Custom field no Jira** (ex: "OKR_ID")
   - Setup: Settings → "Configure OKR source" → "Jira custom field"
   - Selecione field
   - Click "Save"

2. **Notion database linkada**
   - Setup: Settings → "Configure OKR source" → "Notion"
   - Paste URL da database
   - Click "Authorize Notion"

3. **Spreadsheet (Google Sheets)**
   - Setup: Settings → "Configure OKR source" → "Google Sheets"
   - Paste share link
   - Click "Authorize"

**❌ Não suportado (R1):**
- Monday.com
- Asana
- Linear
- Custom API (será R2)

**Se OKR está em um desses formatos suportados mas não aparece:**
- Verifique que OKR foi configurado em Settings
- Force sync: Click "Sync Now"
- Se persistir, email: jadergreiner@gmail.com

---

### P: OKR foi deletado — e agora minhas tasks orfam?

**R:** Depende da configuração:

**Opção 1: Soft-delete (recomendado)**
- OKR fica marcado como "archived"
- Tasks continuam linkadas
- Score sobe um pouco (menos links vivos)
- Você consegue unlink manualmente

**Opção 2: Hard-delete**
- OKR sumiu completamente
- APOS detecta links quebrados
- Tasks ficam "orphaned"
- Você precisa re-linkar ou deletar

**Recomendação:** Nunca delete OKRs. Archive em vez disso (Settings → "Archiving policy").

---

### P: Relationship foi deletada por acidente

**R:** Você pode restaurar via:

**1. Backup (7 dias):**
   - APOS mantém backup de 7 dias
   - Email: jadergreiner@gmail.com com:
     - Task ID
     - OKR ID
     - Quando foi deletado?
   - Vamos restaurar em <1h

**2. Re-link manualmente:**
   - Quickest: click "Link OKR" novamente
   - Takes <1 min

**3. API batch restore:**
   ```bash
   curl -X POST "https://api.apos.io/api/v1/relationships/restore" \
     -H "Authorization: Bearer YOUR_API_KEY" \
     -d '{...}'
   ```
   (Disponível R1)

---

## 🔗 OKR & Linking Issues

### P: Como funciona "auto-suggest" para links?

**R:** APOS usa **machine learning simples**:

1. **Histórico de links similares:**
   - Se JIRA-100 ("Build feature X") foi linkado a OKR-2026-Q3-001
   - Novo task JIRA-200 ("Feature X: polish") → auto-sugere mesma OKR

2. **Semantic similarity:**
   - Keywords no título/descrição
   - Exemplo: "Database" task → "Database optimization" OKR

3. **Confidence score:**
   - 0.95 = muito confiante (use auto-link)
   - 0.7 = moderado (revisar manualmente)
   - 0.4 = baixo (ignore, link manualmente)

**Como ativar auto-suggest:**
- Settings → "Auto-linking" → On
- Default: ligado

---

### P: Posso linkar uma task a MÚLTIPLOS OKRs?

**R:** Não (Sprint 0.3), sim (R1).

**Sprint 0.3:** Uma task = um OKR apenas.

**R1:** Suportará múltiplos OKRs por task:
```
Task "Build platform" pode linkar a:
- OKR-2026-Q3-001: "Aumentar transparência"
- OKR-2026-Q3-002: "Melhorar performance"
```

**Workaround hoje:** Crie sub-tasks separadas.

---

### P: Unlinked uma task — e agora virou orfã?

**R:** Sim, esperado! 😄

- Unlink = remover OKR
- Task fica orfã automaticamente
- Score cai um pouco (menos coverage)
- Você pode re-link a qualquer hora

---

## 🔌 API Issues

### P: API retorna 400 "confidence_out_of_range"

**R:** Você mandou `confidence > 1.0` ou `< 0.0`.

**Solução:**
```bash
# ❌ Errado:
POST /relationships
{
  "confidence": 1.5  // out of range!
}

# ✅ Correto:
POST /relationships
{
  "confidence": 0.95  // entre 0.0 e 1.0
}
```

Valid range: **0.0-1.0** sempre.

---

### P: API retorna 409 "relationship_exists"

**R:** Você tentou linkar uma task a um OKR que já está linkado.

**Solução:**

```bash
# ❌ Seu comando (erro):
POST /relationships
{
  "task_id": "JIRA-123",
  "okr_id": "OKR-2026-Q3-001"
}
# Erro: Esse link já existe!

# ✅ Solução 1: Verificar se link existe
GET /relationships?task_id=JIRA-123&okr_id=OKR-2026-Q3-001

# ✅ Solução 2: Update existing link
PUT /relationships/{relationship_id}
{
  "confidence": 0.9  // nova confiança
}

# ✅ Solução 3: Unlink first, then re-link
DELETE /relationships/{relationship_id}
# wait 1 sec
POST /relationships {...}
```

---

### P: Rate limit exceeded — como contornar?

**R:** Você fez muitas requisições muito rápido.

**Limites:**
- Piloto/Dev: 1,000 req/min
- Production: 100 req/min
- Sync endpoints: 10 req/min

**Soluções:**

1. **Aguarde:** Espere 60s antes de retry
2. **Paginar:** Use `limit` e `page` em vez de mega-queries
   ```bash
   # ❌ Errado: puxar 100K tasks de uma vez
   GET /tasks?project_id=R0&limit=100000
   
   # ✅ Correto: paginar
   GET /tasks?project_id=R0&limit=100&page=1
   GET /tasks?project_id=R0&limit=100&page=2
   ```
3. **Cache:** Guarde resultados localmente, não requery
4. **Batch:** Use batch endpoints (R1) para múltiplas operações

---

### P: API retorna 500 "Internal Server Error"

**R:** Server side issue. Siga:

1. **Tente novamente em 30s**
   - Às vezes é problema temporário

2. **Check status:**
   ```bash
   curl -X GET "https://api.apos.io/api/v1/health" \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```
   - Se retorna 200 = API está up
   - Se timeout = API down

3. **Email + request_id:**
   - Há um `request_id` no erro JSON
   - Email com: request_id, timestamp, o que você fez
   - Vamos investigar logs em <1h

**SLA:** 99.5% uptime

---

### P: Qual é a latência esperada da API?

**R:** **P95 latency: <500ms** (AI Architect requirement).

Benchmarks:

| Endpoint | P50 | P95 | P99 |
|----------|-----|-----|-----|
| GET /tasks (paginated) | 50ms | 150ms | 300ms |
| GET /trust-score | 100ms | 250ms | 500ms |
| POST /relationships | 75ms | 200ms | 400ms |
| GET /orphans | 80ms | 200ms | 350ms |

**Se você vê >500ms:**
- Pode ser sua rede (check ping)
- Pode ser nossos servers (report com request_id)

---

## 🎓 Conceitual Issues

### P: O que significa "semantic context"?

**R:** Significa que **você entende por que cada tarefa existe**.

**Sem semantic context (problema):**
```
Dev: "Qual é essa task JIRA-100?"
PM: (gasta 10 min explicando)
Dev: "Como conecta com estratégia?"
PM: (gasta mais 10 min explicando)
```
❌ Retrabalho, confusão, decisões ruins

**Com semantic context (solução APOS):**
```
Dev: Abre dashboard APOS
Dashboard mostra:
  JIRA-100 → OKR-2026-Q3-001 "Aumentar retenção"
  → KR: "+15% DAU até 2026-07-15"
  → Métrica conectada: database performance
Dev: "Entendi, começo agora!" ✅
```

APOS **automatiza a explicação** via contexto visual.

---

### P: O que significa "Trust Score"?

**R:** Score 0.0-1.0 que mede: **"Quanto confiança tenho no meu contexto estratégico?"**

**Alta confiança (0.85):**
- 90%+ tasks têm OKR
- Todos OKRs têm métricas
- Sem conflitos
- → Posso confiar em decisões estratégicas

**Baixa confiança (0.3):**
- 40% tasks sem OKR
- Não sei por que existem
- Alguns links fracos
- → Preciso parar, clarificar, depois executar

APOS **força clareza antes de execução**.

---

## 📞 Não Encontrou Sua Pergunta?

**Nenhum problema!** Envie email:

```
Para: jadergreiner@gmail.com
Assunto: APOS FAQ - [sua pergunta]
Corpo:
  - O que você tentou?
  - Qual foi o erro?
  - Screenshot se possível?
  - Browser + version?
```

**Tempo de resposta:** <2 horas  
**Ao feedback:** Adicionamos sua pergunta à FAQ! 📝

---

**Última atualização:** 2026-07-29  
**Versão APOS:** 0.1.0-beta  
**Próxima review:** 2026-08-15 (após R1)
