# APOS API Reference (v1.0)

**Version:** 1.0 (Sprint 0.3)  
**Base URL:** `https://api.apos.io/api/v1`  
**Framework:** FastAPI (Python)  
**Status:** ✅ Production-Ready  
**Last updated:** 2026-07-29

---

## Autenticação

### API Key (Piloto & Production)

Todos os endpoints requerem autenticação via **Bearer token** no header `Authorization`:

```bash
Authorization: Bearer YOUR_API_KEY
```

**Como obter API key:**

1. Sign-up em [apos.io](https://apos.io)
2. Vá para **Settings** → **API Keys**
3. Click **"Generate Key"**
4. Copie a chave (aparece uma vez)
5. Cole em Settings do Plugin Jira

**Validade:** Chaves duram 90 dias (rotação automática recomendada)

### Rate Limits

| Ambiente | Limite | Janela |
|----------|--------|--------|
| **Piloto/Dev** | 1,000 req/min | Por API key |
| **Production** | 100 req/min | Por API key |

**Exceção:** Endpoints de sync (`/sync/*`) têm limite de 10 req/min (evita abuse).

**Resposta quando limite excedido:**
```json
{
  "error": "rate_limit_exceeded",
  "retry_after": 60
}
```

---

## 📋 Endpoints Overview

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/tasks` | Listar todas tasks (paginated) |
| GET | `/tasks/{id}` | Detalhe de uma task |
| GET | `/okrs` | Listar OKRs |
| GET | `/okrs/{id}` | Detalhe de um OKR |
| POST | `/relationships` | Vincular task a OKR |
| GET | `/relationships` | Listar relacionamentos |
| GET | `/trust-score` | Calcular confiança geral |
| GET | `/orphans` | Listar features orfas |
| POST | `/sync/jira` | Força sync manual (Jira) |
| GET | `/health` | Status da API |

---

## Endpoints Detalhados

### 1. GET /tasks

**Listar todas as tasks com paginação.**

```bash
curl -X GET "https://api.apos.io/api/v1/tasks?project_id=R0&status=in_progress&page=1&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

**Query Parameters:**

| Param | Tipo | Obrigatório | Descrição |
|-------|------|------------|-----------|
| `project_id` | string | ✅ Sim | ID do projeto (ex: "R0") |
| `status` | enum | ❌ Não | Filtrar por status (veja abaixo) |
| `okr_id` | string | ❌ Não | Filtrar por OKR específico |
| `orphan` | boolean | ❌ Não | true = apenas orfas, false = linked |
| `page` | integer | ❌ Não | Número da página (default: 1) |
| `limit` | integer | ❌ Não | Items por página (default: 50, max: 100) |

**Status permitidos:** `backlog`, `in_progress`, `in_review`, `done`, `blocked`

**Response (200 OK):**

```json
{
  "data": [
    {
      "id": "JIRA-123",
      "title": "Implementar plugin Jira",
      "description": "Integração com APOS para detectar features orfas",
      "status": "in_progress",
      "project_id": "R0",
      "okr_id": "OKR-2026-Q3-001",
      "priority": "high",
      "created_by": "jader@example.com",
      "created_at": "2026-07-22T09:00:00Z",
      "updated_at": "2026-07-27T14:30:00Z",
      "orphan": false,
      "trust_score": 0.85
    },
    {
      "id": "JIRA-124",
      "title": "Refatorar banco de dados",
      "status": "backlog",
      "project_id": "R0",
      "okr_id": null,
      "orphan": true,
      "trust_score": 0.0,
      "created_at": "2026-07-20T10:00:00Z",
      "updated_at": "2026-07-20T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 247,
    "pages": 5
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2026-07-29T20:00:00Z"
  }
}
```

**Status Codes:**

| Código | Descrição |
|--------|-----------|
| **200** | Sucesso — lista de tasks retornada |
| **400** | Bad Request — project_id obrigatório ou parâmetro inválido |
| **401** | Unauthorized — API key inválida/expirada |
| **429** | Rate limit exceeded — espere antes de fazer retry |
| **500** | Internal Server Error — contate support |

---

### 2. GET /tasks/{id}

**Obter detalhes completos de uma task.**

```bash
curl -X GET "https://api.apos.io/api/v1/tasks/JIRA-123" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**

```json
{
  "id": "JIRA-123",
  "title": "Implementar plugin Jira",
  "description": "Integração com APOS para detectar features orfas e calcular trust score",
  "status": "in_progress",
  "project_id": "R0",
  "okr_id": "OKR-2026-Q3-001",
  "okr_title": "Aumentar transparência estratégica",
  "priority": "high",
  "created_by": "jader@example.com",
  "created_at": "2026-07-22T09:00:00Z",
  "updated_at": "2026-07-27T14:30:00Z",
  "orphan": false,
  "trust_score": 0.85,
  "subtasks": [
    {
      "id": "JIRA-124",
      "title": "API endpoints design",
      "status": "done"
    },
    {
      "id": "JIRA-125",
      "title": "Plugin frontend implementation",
      "status": "in_progress"
    }
  ],
  "linked_issues": [
    {
      "type": "relates_to",
      "issue_id": "JIRA-500",
      "title": "Trust Score Calculation"
    }
  ],
  "labels": ["mvp", "jira-integration", "priority-high"],
  "estimate_hours": 40,
  "spent_hours": 32
}
```

**Status Codes:** Same as `/tasks`

---

### 3. GET /okrs

**Listar todos os OKRs.**

```bash
curl -X GET "https://api.apos.io/api/v1/okrs?project_id=R0&active=true" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Query Parameters:**

| Param | Tipo | Descrição |
|-------|------|-----------|
| `project_id` | string | ✅ Obrigatório |
| `active` | boolean | Apenas OKRs ativos (default: true) |
| `quarter` | string | Filtrar por quarter (ex: "Q3-2026") |

**Response (200 OK):**

```json
{
  "data": [
    {
      "id": "OKR-2026-Q3-001",
      "title": "Aumentar transparência estratégica",
      "description": "Eliminar retrabalho em contexto semântico",
      "status": "in_progress",
      "quarter": "Q3-2026",
      "key_results": [
        {
          "id": "KR-001",
          "title": "Plugin pronto para piloto",
          "target": "2026-07-29",
          "current_value": 100,
          "unit": "%"
        },
        {
          "id": "KR-002",
          "title": "Redução de retrabalho em -80%",
          "target": "2026-08-15",
          "current_value": 0,
          "unit": "%"
        }
      ],
      "owner": "Jader Greiner",
      "created_at": "2026-07-20T09:00:00Z",
      "task_count": 12,
      "linked_tasks": 10
    }
  ],
  "pagination": {
    "total": 8,
    "pages": 1
  }
}
```

---

### 4. POST /relationships

**Vincular uma task a um OKR (criar relacionamento).**

```bash
curl -X POST "https://api.apos.io/api/v1/relationships" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "JIRA-124",
    "okr_id": "OKR-2026-Q3-001",
    "confidence": 0.95,
    "linked_by": "jader@example.com"
  }'
```

**Request Body:**

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|------------|-----------|
| `task_id` | string | ✅ Sim | ID da task (JIRA-XXX) |
| `okr_id` | string | ✅ Sim | ID do OKR |
| `confidence` | float | ❌ Não | 0.0-1.0 (default: 0.8) |
| `linked_by` | string | ❌ Não | Email de quem linkou (audit trail) |

**Response (201 Created):**

```json
{
  "id": "rel_abc123",
  "task_id": "JIRA-124",
  "okr_id": "OKR-2026-Q3-001",
  "confidence": 0.95,
  "created_at": "2026-07-29T20:00:00Z",
  "updated_at": "2026-07-29T20:00:00Z",
  "trust_score_impact": "+0.05"
}
```

**Status Codes:**

| Código | Descrição |
|--------|-----------|
| **201** | Relacionamento criado |
| **400** | Bad request (task/OKR inexistente, confidence > 1.0) |
| **409** | Relacionamento já existe (update em vez de create) |

---

### 5. GET /trust-score

**Calcular Trust Score geral do projeto.**

```bash
curl -X GET "https://api.apos.io/api/v1/trust-score?project_id=R0" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**

```json
{
  "project_id": "R0",
  "score": 0.78,
  "status": "healthy",
  "breakdown": {
    "coverage": 0.85,
    "quality": 0.72,
    "consistency": 0.95
  },
  "weights": {
    "coverage": 0.4,
    "quality": 0.4,
    "consistency": 0.2
  },
  "stats": {
    "total_tasks": 247,
    "linked_tasks": 210,
    "orphan_tasks": 37,
    "orphan_percentage": 15.0
  },
  "timestamp": "2026-07-29T20:00:00Z"
}
```

**Interpretação:**

| Score | Status | Ação |
|-------|--------|------|
| 0.7-1.0 | ✅ Healthy | Contexto claro, continuar |
| 0.3-0.7 | ⚠️ Caution | Revisar orfas + links, melhorar cobertura |
| 0.0-0.3 | 🔴 Critical | Muitas orfas, contexto quebrado |

---

### 6. GET /orphans

**Listar todas as features orfas (sem OKR).**

```bash
curl -X GET "https://api.apos.io/api/v1/orphans?project_id=R0&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**

```json
{
  "data": [
    {
      "id": "JIRA-124",
      "title": "Refatorar banco de dados",
      "status": "backlog",
      "priority": "medium",
      "created_at": "2026-07-20T10:00:00Z",
      "created_by": "dev@example.com",
      "time_orphan_days": 9
    },
    {
      "id": "JIRA-130",
      "title": "Atualizar dependências npm",
      "status": "in_progress",
      "priority": "low",
      "created_at": "2026-07-15T11:00:00Z",
      "created_by": "dev2@example.com",
      "time_orphan_days": 14
    }
  ],
  "pagination": {
    "total": 37,
    "pages": 2
  },
  "summary": {
    "critical_orphans": 5,
    "age_avg_days": 8.5,
    "block_estimate_hours": 120
  }
}
```

---

### 7. POST /sync/jira

**Forçar sync manual de tasks do Jira (útil se webhook falha).**

```bash
curl -X POST "https://api.apos.io/api/v1/sync/jira" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "R0",
    "full_sync": false
  }'
```

**Response (202 Accepted):**

```json
{
  "sync_id": "sync_xyz789",
  "status": "in_progress",
  "estimated_time_seconds": 45,
  "tasks_to_process": 247,
  "check_status_url": "/sync/jira/sync_xyz789"
}
```

---

### 8. GET /health

**Verificar status da API (útil para monitoring).**

```bash
curl -X GET "https://api.apos.io/api/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response (200 OK):**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 86400,
  "database": "connected",
  "cache": "connected",
  "timestamp": "2026-07-29T20:00:00Z"
}
```

---

## Data Types

### Task Schema

```json
{
  "id": "string (JIRA-XXX)",
  "title": "string",
  "description": "string or null",
  "status": "enum (backlog|in_progress|in_review|done|blocked)",
  "project_id": "string",
  "okr_id": "string or null",
  "priority": "enum (low|medium|high|critical)",
  "created_by": "string (email)",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime",
  "orphan": "boolean",
  "trust_score": "float (0.0-1.0)"
}
```

### OKR Schema

```json
{
  "id": "string (OKR-YYYY-QX-NNN)",
  "title": "string",
  "description": "string",
  "status": "enum (planned|in_progress|completed|archived)",
  "quarter": "string (Q1-2026|Q2-2026|...)",
  "owner": "string (email)",
  "key_results": [
    {
      "id": "string",
      "title": "string",
      "target": "ISO date or number",
      "current_value": "float",
      "unit": "string (%|days|users|...)"
    }
  ],
  "task_count": "integer",
  "linked_tasks": "integer",
  "created_at": "ISO 8601 datetime"
}
```

### Trust Score Schema

```json
{
  "score": "float (0.0-1.0)",
  "status": "enum (critical|caution|healthy)",
  "breakdown": {
    "coverage": "float (% tasks linked)",
    "quality": "float (validity of links)",
    "consistency": "float (no conflicts)"
  }
}
```

---

## Error Handling

### Standard Error Response

```json
{
  "error": "error_code",
  "message": "Human-readable message",
  "details": {
    "field": "name",
    "issue": "Invalid value"
  },
  "request_id": "req_abc123",
  "timestamp": "2026-07-29T20:00:00Z"
}
```

### Common Errors

| Código | Causa | Solução |
|--------|-------|---------|
| `invalid_api_key` | API key falsa/expirada | Regenerate em Settings |
| `missing_project_id` | Query param obrigatório | Add `?project_id=R0` |
| `task_not_found` | Task ID inexistente | Validar ID no Jira |
| `okr_not_found` | OKR ID inexistente | Verificar OKR |
| `confidence_out_of_range` | confidence > 1.0 ou < 0.0 | Use 0.0-1.0 |
| `relationship_exists` | Link já existe | Use PUT para update |
| `rate_limit_exceeded` | Muitas requisições | Espere X segundos |

---

## Exemplos Práticos

### Caso 1: Encontrar todas as features orfas

```bash
# 1. Obter lista de orfas
curl -X GET "https://api.apos.io/api/v1/orphans?project_id=R0" \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.data[].id'

# 2. Para cada orfã, decidir:
#    a) Vincular a um OKR (POST /relationships)
#    b) Desprioritizar/delete

# 3. Recalcular score
curl -X GET "https://api.apos.io/api/v1/trust-score?project_id=R0" \
  -H "Authorization: Bearer YOUR_API_KEY" | jq '.score'
```

### Caso 2: Sincronizar e validar

```bash
# Forçar sync manual
curl -X POST "https://api.apos.io/api/v1/sync/jira" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{"project_id": "R0", "full_sync": true}'

# Aguardar conclusão (check health)
sleep 10
curl -X GET "https://api.apos.io/api/v1/health" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## Suporte

- **Documentação:** [apos.io/docs](https://apos.io/docs)
- **Issues:** [GitHub Issues](https://github.com/jadergreiner/APOS/issues)
- **Email:** jadergreiner@gmail.com (tempo de resposta: <2h)

**Última atualização:** 2026-07-29
