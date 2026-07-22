# Sprint 0.3 - Especificacao Tecnica

**Sprint:** 0.3 - Beta Prep (MVP Implementation)  
**Data:** 2026-07-20 (Pre-planning)  
**Status:** 📋 Especificacao pronta para implementacao  
**Validado por:** Job Statement (Sprint 0.2) + Forças Analysis

---

## 1. Visao Geral

**MVP:** Plugin Jira + Semantic Layer + Trust Score

**O que faz:**
1. Conecta com Jira (lê tasks/issues)
2. Auto-mapeia tasks para OKRs (via custom fields)
3. Detecta "features orfas" (sem OKR)
4. Calcula Trust Score 0.0-1.0 (confianca no contexto)
5. Exibe dashboard visual (Task → OKR → Metrica)

**Usuarios:** PM Leaders, EMs, AI Architects (internamente no Jira)

---

## 2. Arquitetura

```
┌─────────────────────────────────────────────┐
│            Jira (Frontend)                  │
│  - Plugin sidebar                           │
│  - Modal "Vincular OKR"                     │
│  - Dashboard Task→OKR                       │
└──────────────────┬──────────────────────────┘
                   │
                   ↓ (API calls)
┌──────────────────────────────────────────────┐
│       Backend API (REST - Port 5000)         │
│  - GET /tasks                                │
│  - GET /okrs                                 │
│  - GET /relationships                        │
│  - GET /trust-score                          │
└──────────────────┬──────────────────────────┘
                   │
                   ↓ (Python)
┌──────────────────────────────────────────────┐
│    Semantic Layer (apos package)             │
│  - Ontology (Task, OKR, Relationship)       │
│  - KnowledgeGraph (instances in-memory)     │
│  - SemanticGate (trust-score calculator)    │
└──────────────────┬──────────────────────────┘
                   │
                   ↓
┌──────────────────────────────────────────────┐
│      Data Store (SQL/JSON)                   │
│  - Tasks (Jira sync)                         │
│  - OKRs (Notion/manual input)               │
│  - Relationships (Task→OKR mappings)        │
│  - Scores (cached, TTL 1h)                  │
└──────────────────────────────────────────────┘
```

---

## 3. Fluxo de Dados

### 3.1 Onboarding (First Time)

```
1. PM instala Plugin Jira
2. Setup: autentica com Jira + backend API
3. Backend: faz sync inicial de todas tasks (100s, 1000s)
4. Backend: usuário define "onde estao meus OKRs?" (custom field, Notion link, etc)
5. Backend: mapeia tasks existentes para OKRs (manual + auto-suggest)
6. Dashboard: exibe visao inicial Task→OKR
```

**Tempo esperado:** 5-15 min (setup) + 30 min (mapping manual inicial)

### 3.2 Daily Usage

```
1. Dev cria task no Jira (ou PM cria)
2. Webhook Jira → Backend (task criada)
3. Backend: auto-verifica "essa task tem OKR?"
   - Se SIM: auto-mapeia (match com historico)
   - Se NAO: marca como "orfao" + alerta
4. PM vê dashboard: lista de "features orfas" + "score de confianca"
5. PM action: "vincular OKR" ou "despriorizar"
6. Backend recalcula Trust Score (coverage↑, quality✓)
```

**Latencia:** <500ms por operacao (AI Architect requirement)

---

## 4. Componentes Principais

### 4.1 Plugin Jira

**Tecnologia:** Jira App SDK (Node.js, React)

**Features:**
- Sidebar: lista de tasks orfas + scores
- Modal: "Vincular OKR" (dropdown, search, create)
- Context menu: "Este task contribui para qual OKR?"
- Dashboard: grafico Task→OKR (Recharts, D3)

**Performance:** <30s load, <100ms interacoes

**Setup:** <30 min (Early Adopter requirement)

### 4.2 Backend API (REST)

**Framework:** Flask/FastAPI (Python)

**Endpoints:**

```python
GET /api/v1/tasks
  # Lista todas tasks (paginated)
  # Params: project_id, status, okr_id
  # Returns: [{ id, title, status, okr_id, created_at, orphan: bool, score }]

GET /api/v1/tasks/{task_id}
  # Detalhes de uma task
  # Returns: { id, title, description, okr_id, subtasks, relationships }

GET /api/v1/okrs
  # Lista OKRs (conecta com Notion ou internal DB)
  # Returns: [{ id, name, description, key_results, target_date }]

GET /api/v1/relationships
  # Lista mappings Task→OKR
  # Returns: [{ task_id, okr_id, confidence, created_by, created_at }]

POST /api/v1/relationships
  # Cria novo mapping
  # Body: { task_id, okr_id }
  # Returns: { id, task_id, okr_id, confidence, created_at }

GET /api/v1/trust-score
  # Calcula overall trust score do grafo
  # Params: project_id (opcional)
  # Returns: { score: 0.85, coverage: 0.9, quality: 0.8, consistency: 0.85, details }

GET /api/v1/orphans
  # Lista features orfas (sem OKR)
  # Returns: [{ task_id, title, risk_level, suggestion }]
```

**Rate limiting:** 1000 req/min (development), 100 req/min (production)

**Auth:** API key (piloto) → OAuth (production)

### 4.3 Semantic Layer

**Componente:** APOS package (apos/core + apos/governance)

**Classes:**

```python
class Task(Entity):
    id: str
    title: str
    status: Enum  # backlog, in_progress, review, done
    okr_id: Optional[str]  # None = orfao
    created_at: datetime

class OKR(Entity):
    id: str
    name: str
    key_results: List[str]
    target_date: date

class Relationship(Edge):
    task_id: str
    okr_id: str
    confidence: float  # 0.0-1.0 (manual = 1.0, auto-suggested = 0.7)

class KnowledgeGraph:
    def add_task(task: Task) → None
    def add_okr(okr: OKR) → None
    def link_task_to_okr(task_id, okr_id) → None
    def get_orphans() → List[Task]  # tasks sem OKR

class SemanticGate:
    def evaluate(graph: KnowledgeGraph) → Score
    # Score = { value: 0.0-1.0, coverage, quality, consistency, issues }
    
class Score:
    value: float  # 0.0-1.0
    coverage: float  # % da ontologia representada
    quality: float  # % de dados validos
    consistency: float  # sem contradicoes
    issues: List[str]  # o que melhorar
```

**Trust Score Calculo:**

```
score = (0.3 × coverage) + (0.5 × quality) + (0.2 × consistency)

coverage = len(tasks_linked_to_okr) / len(total_tasks)
  # Exemplo: 8/10 tasks vinculadas = 0.8 coverage

quality = (valid_relationships / total_relationships) × (data_freshness)
  # Valido = task existe, OKR existe, nao e contraditorio
  # Freshness = relacao foi atualizada nos ultimos 7 dias

consistency = 1.0 - (conflicts / total_relationships)
  # Conflito = task vinculada a 2 OKRs mutuamente exclusivos
```

---

## 5. Data Model

### Task

```json
{
  "id": "JIRA-123",
  "title": "Implementar plugin Jira",
  "description": "...",
  "status": "in_progress",
  "project_id": "R0",
  "okr_id": "OKR-2026-Q3-001",
  "created_at": "2026-07-22T09:00:00Z",
  "updated_at": "2026-07-22T14:30:00Z",
  "created_by": "jader@apos.io",
  "priority": "high"
}
```

### OKR

```json
{
  "id": "OKR-2026-Q3-001",
  "name": "Validar MVP com pilotos",
  "description": "Piloto com 3+ personas, validar market fit",
  "key_results": [
    "3+ personas usando plugin por 7 dias consecutivos",
    "Trust score accuracy <5% false positives",
    "Setup time <30 min"
  ],
  "target_date": "2026-07-29",
  "created_at": "2026-07-20T00:00:00Z"
}
```

### Relationship

```json
{
  "id": "REL-456",
  "task_id": "JIRA-123",
  "okr_id": "OKR-2026-Q3-001",
  "confidence": 1.0,
  "created_by": "jader@apos.io",
  "created_at": "2026-07-22T09:15:00Z"
}
```

---

## 6. Deteccao de Orfas

**O que e orfao:** Task em qualquer status que NAO tem okr_id preenchido

**Logica:**

```python
def get_orphans(project_id: str) -> List[Task]:
    all_tasks = db.query(Task).filter(Task.project_id == project_id)
    orphans = [t for t in all_tasks if t.okr_id is None]
    
    # Risk level baseado em status
    for orphan in orphans:
        if orphan.status == "done":
            orphan.risk = "HIGH"  # entregue mas ninguem sabe por que
        elif orphan.status == "in_progress":
            orphan.risk = "MEDIUM"
        else:  # backlog
            orphan.risk = "LOW"
    
    return orphans
```

**Alerta:** Plugin exibe com icone 🚨 HIGH, 🟡 MEDIUM

---

## 7. Edge Cases & Validacoes

| Edge Case | Logica |
|-----------|--------|
| Task sem OKR (orfao) | Detectado automaticamente, alerta |
| OKR sem tasks | Valido (planejamento futuro) |
| Task vinculada a 2+ OKRs | Alertado (contradicao?) |
| OKR deletado em Notion | Relationship deprecated, task orfao automaticamente |
| Task status = done mas orfao | HIGH risk (entrega nao rastreavel) |
| Webhook fail (Jira offline) | Retry com exponential backoff (3x) |
| API timeout (latencia > 500ms) | Log + fallback (cache anterior) |

---

## 8. Performance & Limits

| Aspecto | Alvo | Como |
|---------|------|------|
| API latencia P95 | <500ms | Redis cache (1h TTL), async recalc |
| Load time plugin | <30s | Lazy loading de dados, progressive rendering |
| Setup time | <30 min | Script de setup automatizado |
| Sync Jira | Daily 2am | Cron job, incremental (nao full resync) |
| Trust score recalc | <1s | Batch operation, nao realtime |
| Suport >1000 tasks | Sim | Pagination, indexed queries |

---

## 9. Securtiy & Auth

- API Key auth (piloto) + OAuth2 (production)
- CORS: whitelist jira.yourcompany.com
- Data: nao armazena senhas, tokens rotated 24h
- Encryption: HTTPS, encrypted DB connections

---

## 10. Roadmap (Post-MVP)

**R1 (Post-0.3):**
- Notificacoes em tempo real (Slack, email)
- Integration com Amplitude (tracking adoption)
- Historical analytics (trending de orphans)

**R1.1:**
- Integration com GitHub Actions (CI/CD linking)
- Custom rules (P.ex: "todos features em High priority precisam de OKR")

---

**Status:** 📋 Especificacao concluida  
**Validado por:** MVP scope (Sprint 0.2)  
**Proxima:** Implemetacao (Sprint 0.3 T0.3.1-4)

