# APOS MVP - Plugin Jira + Semantic Context

**Status:** ✅ **RELEASE CANDIDATO** — Sprint 0.3 Completo  
**Versão:** 0.1.0-beta  
**Data:** 2026-07-29  
**Última atualização:** 2026-07-29 20:00

---

## O que é APOS?

**APOS** é um plugin Jira que detecta **features orfas** (tarefas sem estratégia conectada) e calcula um **Trust Score** (0.0-1.0) que mede a confiança no contexto semântico do seu roadmap.

### Problema que resolve

PMs perdem **2-3 horas por semana** re-explicando por que tarefas existem e como conectam com OKRs. APOS automatiza isso: une Tasks → OKRs → Métricas em um dashboard único, eliminando retrabalho.

### O que você recebe

| Feature | Benefício |
|---------|-----------|
| **Detecção de Features Orfas** | Identifique tarefas sem OKR em segundos |
| **Trust Score Automático** | Confiança 0.0-1.0 no seu contexto estratégico |
| **Dashboard Visual** | Veja Task → OKR → Metrica conectadas |
| **Sync em Tempo Real** | Webhook automático quando task muda |

---

## Quick Start (5 minutos)

### Pré-requisitos

- Jira Cloud account com permissão de Admin
- API endpoint + API key (fornecido durante setup)
- Browser: Chrome, Firefox ou Safari (últimas 2 versões)

### 4 Passos para Começar

#### 1. Instalar Plugin (2 min)

- Acesse [Jira Marketplace](https://marketplace.atlassian.com)
- Busque por "APOS"
- Click **"Get it now"** → selecione seu workspace
- Autorize permissões (leitura de tasks/issues)

#### 2. Setup Inicial (1 min)

- Plugin sidebar aparece no Jira (ícone 🧠)
- Click **"Settings"**
- Cole **API endpoint** (ex: `https://api.apos.io/v1`)
- Cole **API key** (fornecida por email após sign-up)
- Click **"Test Connection"** → verde = sucesso

#### 3. Sincronizar Dados (1 min)

- Click **"Sync Now"**
- Backend inicia sync de todas as tasks (background job)
- Status: "Syncing... 50/247 tasks"
- Aguarde conclusão (~30-60s dependendo do volume)

#### 4. Verificar Dashboard (1 min)

- Sync concluído? Dashboard aparece
- Veja:
  - **Total tasks:** X
  - **Orphan tasks (sem OKR):** Y
  - **Average Trust Score:** Z

**Parabéns!** Seu APOS está pronto. Próximo passo: [TUTORIAL.md](TUTORIAL.md) para usar no dia-a-dia.

---

## Arquitetura (em 4 camadas)

```
┌─────────────────────────────────────────┐
│  Jira Frontend (Plugin Sidebar)         │
│  - Dashboard de orfas                  │
│  - Modal "Vincular OKR"                │
│  - Trust Score visual                  │
└──────────────┬──────────────────────────┘
               │ REST API
               ↓
┌─────────────────────────────────────────┐
│  Backend API (REST, Port 5000)          │
│  - GET /tasks, /okrs, /relationships    │
│  - POST /relationships (vincular)       │
│  - GET /trust-score (calcular)          │
│  - GET /orphans (listar orfas)          │
└──────────────┬──────────────────────────┘
               │ Python
               ↓
┌─────────────────────────────────────────┐
│  Semantic Layer (apos package)          │
│  - Ontology (Task, OKR, Relationship)   │
│  - KnowledgeGraph (calcular grafo)      │
│  - SemanticGate (gerar Trust Score)     │
└──────────────┬──────────────────────────┘
               │ Query
               ↓
┌─────────────────────────────────────────┐
│  Data Store (PostgreSQL + Cache)        │
│  - Tasks (sync Jira)                    │
│  - OKRs (Notion/custom field)          │
│  - Relationships (Task ↔ OKR)           │
│  - Scores (cache TTL 1h)                │
└─────────────────────────────────────────┘
```

---

## Conceitos Chave

### Task
Uma issue/story no Jira. Exemplos: "Implementar login OAuth", "Refactor DB".

### OKR (Objective & Key Results)
Objetivo estratégico com métricas. Exemplo: "Aumentar retenção de usuários" (Key Result: "+15% DAU").

Pode estar em:
- Custom field Jira
- Notion database
- Spreadsheet linkado

### Orphan (Feature Orfã)
Task **sem OKR linkado**. Significa: ninguém sabe por que essa tarefa existe ou como conecta com a estratégia.

### Trust Score
Número 0.0-1.0 que mede confiança no seu contexto semântico:
- **0.0-0.3** = Crítico (muitas orfas, contexto quebrado)
- **0.3-0.7** = Caution (algumas gaps)
- **0.7-1.0** = Healthy (confiança alta, contexto claro)

Calculado por:
```
Score = (Coverage × 40%) + (Quality × 40%) + (Consistency × 20%)

Coverage     = % de tasks com OKR linkado
Quality      = Validade dos links (score 0-1)
Consistency  = Sem conflitos/redundâncias
```

---

## Fluxo de Uso Típico

### Dia 1: Onboarding

```
1. Instala plugin Jira
2. Setup: API key + endpoint
3. Sync inicial: todas as tasks
4. Vê dashboard: "Você tem 60 orfas"
5. Começa a vincular OKRs
```

**Tempo:** ~30 min (primeira vez)

### Dia-a-dia

```
1. Dev abre task no Jira
2. Webhook → Backend
3. Backend: auto-detecta "task sem OKR?"
   - Se tem OKR histórico similar → auto-sugere
   - Se não → marca orfã + alerta
4. PM vê sidebar "Novos orfas: 2"
5. PM: clica → modal "vincular OKR"
6. Seleciona OKR → Backend recalcula score
7. Trust Score sobe (coverage ↑)
```

**Latência:** <500ms (AI Architect requirement)

---

## Próximos Passos

- **[TUTORIAL.md](TUTORIAL.md)** — Setup detalhado + primeiro uso
- **[API_DOCS.md](API_DOCS.md)** — Referência técnica de endpoints
- **[FAQ.md](FAQ.md)** — Troubleshooting + perguntas comuns

---

## Suporte & Feedback

**Feedback durante piloto?** Abra uma issue em [GitHub](https://github.com/jadergreiner/APOS/issues)

**Problema crítico?** Email: jadergreiner@gmail.com (tempo de resposta: <2h)

**Documentação faltando algo?** Pull request bem-vindo!

---

**Status do Piloto:** 3/3 personas onboarded ✅  
**Próximo Release:** R1 (Integração Slack, Custom Rules) — 2026-08-15  
**Última atualização:** 2026-07-29  
