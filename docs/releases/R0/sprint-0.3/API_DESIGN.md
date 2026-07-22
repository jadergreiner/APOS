# Sprint 0.3 - API Design (REST)

**Sprint:** 0.3 - Beta Prep  
**Status:** ✅ **COMPLETO** — Endpoints, schemas, examples  
**Framework:** Flask/FastAPI (Python)  
**Base URL:** `http://localhost:5000/api/v1` (dev) | `https://api.apos.io/api/v1` (prod)

---

## 1. Overview

5 principais endpoints para Plugin Jira:

```
GET  /tasks              — Listar todas tasks (paginated)
GET  /tasks/{id}        — Detalhes de uma task
GET  /okrs              — Listar OKRs
POST /relationships     — Vincular task a OKR
GET  /trust-score       — Calcula confianca do grafo
GET  /orphans           — Features orfas (sem OKR)
```

---

## 2. Endpoints Detalhados

### A. GET /tasks

**Listar todas tasks com paginacao**

```bash
curl -X GET "http://localhost:5000/api/v1/tasks?project_id=R0&status=in_progress&page=1&limit=50" \
  -H "Authorization: Bearer API_KEY"
```

**Response (200):**
```json
{
  "data": [
    {
      "id": "JIRA-123",
      "title": "Implementar plugin Jira",
      "status": "in_progress",
      "okr_id": "OKR-2026-Q3-001",
      "orphan": false,
      "trust_score": 0.85,
      "created_at": "2026-07-22T09:00:00Z",
      "updated_at": "2026-07-22T14:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 247,
    "pages": 5
  }
}
```

**Query Params:**
- `project_id` (str) — OBRIGATORIO
- `status` (enum) — backlog, in_progress, review, done
- `okr_id` (str) — filtrar por OKR específico
- `page` (int) — default 1
- `limit` (int) — default 50, max 100

**Status Codes:**
- `200 OK` — sucesso
- `400 Bad Request` — missing project_id
- `401 Unauthorized` — invalid API key
- `500 Internal Server Error` — database fail

---

### B. GET /tasks/{id}

**Detalhes completos de uma task**

```bash
curl -X GET "http://localhost:5000/api/v1/tasks/JIRA-123" \
  -H "Authorization: Bearer API_KEY"
```

**Response (200):**
```json
{
  "id": "JIRA-123",
  "title": "Implementar plugin Jira",
  "description": "Integrar APOS com Jira, detectar features orfas",
  "status": "in_progress",
  "project_id": "R0",
  "okr_id": "OKR-2026-Q3-001",
  "priority": "high",
  "created_by": "jader@apos.io",
  "created_at": "2026-07-22T09:00:00Z",
  "updated_at": "2026-07-22T14:30:00Z",
  "subtasks": [
    {
      "id": "JIRA-124",
      "title": "API endpoints design",
      "status": "done"
    }
  ],
  "relationships": [
    {
      "id": "REL-001",
      "okr_id": "OKR-2026-Q3-001",
      "confidence": 1.0,
      "linked_by": "jader@apos.io"
    }
  ]
}
```

---

### C. GET /okrs

**Listar OKRs (from Notion ou internal DB)**

```bash
curl -X GET "http://localhost:5000/api/v1/okrs?project_id=R0" \
  -H "Authorization: Bearer API_KEY"
```

**Response (200):**
```json
{
  "data": [
    {
      "id": "OKR-2026-Q3-001",
      "name": "Validar MVP com pilotos",
      "description": "Piloto com 3+ personas, validar market fit",
      "key_results": [
        "3+ personas usando plugin por 7 dias",
        "Trust score accuracy <5% FP",
        "Setup time <30 min"
      ],
      "target_date": "2026-07-29",
      "created_at": "2026-07-20T00:00:00Z"
    }
  ]
}
```

---

### D. POST /relationships

**Vincular task a OKR (ou criar novo mapping)**

```bash
curl -X POST "http://localhost:5000/api/v1/relationships" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "JIRA-123",
    "okr_id": "OKR-2026-Q3-001",
    "confidence": 1.0
  }'
```

**Request Body:**
```json
{
  "task_id": "JIRA-123",              // OBRIGATORIO
  "okr_id": "OKR-2026-Q3-001",        // OBRIGATORIO
  "confidence": 1.0                   // 0.0-1.0 (1.0 = manual, 0.7 = auto-suggested)
}
```

**Response (201 Created):**
```json
{
  "id": "REL-456",
  "task_id": "JIRA-123",
  "okr_id": "OKR-2026-Q3-001",
  "confidence": 1.0,
  "created_by": "jader@apos.io",
  "created_at": "2026-07-22T15:00:00Z"
}
```

**Error (400):**
```json
{
  "error": "Task already linked to conflicting OKR",
  "details": {
    "task_id": "JIRA-123",
    "current_okr": "OKR-2026-Q3-002",
    "requested_okr": "OKR-2026-Q3-001"
  }
}
```

---

### E. GET /trust-score

**Calcula Trust Score geral do grafo (0.0-1.0)**

```bash
curl -X GET "http://localhost:5000/api/v1/trust-score?project_id=R0" \
  -H "Authorization: Bearer API_KEY"
```

**Response (200):**
```json
{
  "score": 0.85,
  "components": {
    "coverage": 0.90,       // 90% das tasks vinculadas
    "quality": 0.85,        // 85% valid relationships
    "consistency": 0.80     // 80% sem contradicoes
  },
  "timestamp": "2026-07-22T15:05:00Z",
  "cache_ttl": 3600,
  "issues": [
    {
      "type": "low_coverage",
      "description": "10% das tasks ainda sem OKR",
      "affected_count": 25,
      "action": "Review backlog, vincular OKRs faltantes"
    }
  ]
}
```

**Formula:**
```
score = (0.3 × coverage) + (0.5 × quality) + (0.2 × consistency)
```

---

### F. GET /orphans

**Listar features orfas (sem OKR) com risk levels**

```bash
curl -X GET "http://localhost:5000/api/v1/orphans?project_id=R0" \
  -H "Authorization: Bearer API_KEY"
```

**Response (200):**
```json
{
  "data": [
    {
      "task_id": "JIRA-456",
      "title": "Fix database migration",
      "status": "done",
      "risk_level": "HIGH",           // DONE sem OKR = HIGH risk
      "priority": "medium",
      "created_at": "2026-07-15T10:00:00Z",
      "suggestion": "Task foi entregue mas ninguem rastreia impacto. Vincule a um OKR para documentar."
    },
    {
      "task_id": "JIRA-789",
      "title": "Refactor auth module",
      "status": "in_progress",
      "risk_level": "MEDIUM",         // IN_PROGRESS sem OKR = MEDIUM
      "priority": "high",
      "suggestion": "Vincule este task a um OKR para alinhar com estrategia."
    }
  ],
  "summary": {
    "total_orphans": 25,
    "high_risk": 5,    // DONE
    "medium_risk": 10, // IN_PROGRESS
    "low_risk": 10     // BACKLOG
  }
}
```

---

## 3. Authentication & Authorization

### API Key (Development/Piloto)

```
Authorization: Bearer sk_test_abc123def456
```

### OAuth2 (Production)

```
Authorization: Bearer eyJhbGc...jwt_token...
```

---

## 4. Rate Limiting

**Development:** 1000 req/min per API key  
**Production:** 100 req/min per user

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1626980420
```

**Error (429 Too Many Requests):**
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

---

## 5. Error Handling

**Standard Error Response:**
```json
{
  "error": "string",          // error message
  "error_code": "string",     // e.g. "ORPHAN_TASK_NOT_FOUND"
  "details": {},              // context-specific
  "timestamp": "2026-07-22T15:00:00Z",
  "request_id": "req_12345"   // para debugging
}
```

**Common Status Codes:**
- `200 OK` — sucesso
- `201 Created` — recurso criado
- `400 Bad Request` — validacao falhou
- `401 Unauthorized` — auth falhou
- `404 Not Found` — recurso nao existe
- `429 Too Many Requests` — rate limit
- `500 Internal Server Error` — bug/database fail

---

## 6. Validacoes (Business Logic)

| Validacao | Regra |
|-----------|-------|
| **Task→OKR linking** | Task so pode ter 1 okr_id (ou NULL) |
| **Trust Score bounds** | Sempre 0.0-1.0, nunca negativo |
| **Relationship confidence** | 0.0-1.0 (1.0 = manual, 0.7+ = auto) |
| **Orphan detection** | Task sem okr_id = orfao automaticamente |
| **OKR deletion** | Deleta OKR → tasks vinculadas ficam orfas |
| **Webhook retry** | Falha → retry 3x com exponential backoff |

---

## 7. Caching Strategy

| Recurso | TTL | Invalidacao |
|---------|-----|-------------|
| **GET /tasks** | 5 min | Task atualizado via Jira webhook |
| **GET /okrs** | 15 min | OKR alterado (manual ou Notion sync) |
| **GET /trust-score** | 1h | Relationship criado/deletado |
| **GET /orphans** | 10 min | Task status mudou ou okr_id alterado |

---

## 8. Performance Targets

| Operacao | P95 Latencia | SLA |
|----------|-------------|-----|
| GET /tasks (50 items) | <200ms | 99.5% uptime |
| GET /trust-score | <500ms | 99.5% uptime |
| POST /relationships | <300ms | 99.5% uptime |
| GET /orphans | <400ms | 99.5% uptime |

---

## 9. Webhook (Jira → Backend)

**When:** Task criada, atualizada, deletada em Jira  
**Endpoint:** `POST https://api.apos.io/webhooks/jira`  
**Payload:**
```json
{
  "event": "issue.created|updated|deleted",
  "issue_id": "JIRA-123",
  "title": "...",
  "status": "in_progress",
  "project_id": "R0",
  "timestamp": "2026-07-22T15:00:00Z"
}
```

**Retry:** 3x com exponential backoff (1s, 2s, 4s)

---

## 10. Exemplo: Flow Completo

```bash
# 1. Listar tasks orphas
curl "http://localhost:5000/api/v1/orphans?project_id=R0" \
  -H "Authorization: Bearer API_KEY"

# 2. Ver OKRs disponiveis
curl "http://localhost:5000/api/v1/okrs?project_id=R0" \
  -H "Authorization: Bearer API_KEY"

# 3. Vincular task a OKR
curl -X POST "http://localhost:5000/api/v1/relationships" \
  -H "Authorization: Bearer API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "JIRA-456", "okr_id": "OKR-2026-Q3-001", "confidence": 1.0}'

# 4. Verificar novo trust score
curl "http://localhost:5000/api/v1/trust-score?project_id=R0" \
  -H "Authorization: Bearer API_KEY"
```

---

**Status:** ✅ **API Design Completo**  
**Pronto para:** T0.3.3 (Plugin Jira) — consumir estes endpoints  
**Documentacao:** Referencia SPEC.md para data model + logica  
