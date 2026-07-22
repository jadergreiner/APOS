# APOS Jira Plugin

**Version:** 0.3.0-beta  
**Status:** 🟠 IN DEVELOPMENT (Sprint 0.3)  
**Sprint:** T0.3.3 — Plugin Jira Implementation

---

## Overview

APOS Plugin for Jira detects orphaned features (tasks without OKRs), links tasks to OKRs automatically, and calculates trust scores for your project's strategic alignment.

**Features:**
- 🔍 Detect "orphaned" features (no OKR linkage)
- 🔗 Link tasks to OKRs via Jira UI
- 📊 Calculate Trust Score (0.0-1.0) for project alignment
- 🚀 <30 min setup (Early Adopter requirement)
- ⚡ <500ms API latency (AI Architect requirement)

---

## Architecture

```
┌─────────────────────────┐
│    Jira (Frontend)      │
│  - Plugin Sidebar       │
│  - Modal (Link OKR)     │
│  - Dashboard            │
└────────────┬────────────┘
             │ (REST API calls)
             ↓
┌─────────────────────────┐
│  Backend API (Python)   │
│  - GET /tasks           │
│  - POST /relationships  │
│  - GET /trust-score     │
│  - GET /orphans         │
└────────────┬────────────┘
             │ (KnowledgeGraph)
             ↓
┌─────────────────────────┐
│  Semantic Layer (APOS)  │
│  - Trust Score calc     │
│  - Orphan detection     │
│  - Data validation      │
└─────────────────────────┘
```

---

## Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Jira Cloud instance
- APOS Backend API running (`http://localhost:5000`)

### Installation

```bash
# 1. Install dependencies
npm install

# 2. Build plugin
npm run build

# 3. Upload to Jira Cloud
# Follow: https://developer.atlassian.com/cloud/jira/platform/getting-started-with-connect/
```

### Environment Variables

Create `.env` file:

```env
REACT_APP_API_URL=http://localhost:5000/api/v1
REACT_APP_JIRA_CLIENT_ID=your_jira_oauth_client_id
REACT_APP_JIRA_CLIENT_SECRET=your_jira_oauth_client_secret
```

---

## Development

### Run in Dev Mode

```bash
npm run dev
# Opens http://localhost:3000
```

### Build for Production

```bash
npm run build
# Creates `dist/` folder
```

### Run Tests

```bash
npm test           # Single run
npm run test:watch # Watch mode
```

### Lint Code

```bash
npm run lint
```

---

## Modules

### 1. **Sidebar** (`src/modules/sidebar.js`)
- Displays list of orphaned features (without OKR)
- Shows trust score
- Allows quick linking via modal

**Status:** 🟠 PLANNED (T0.3.3 Fase 3)

### 2. **Webhooks** (`src/modules/webhooks.js`)
- Listens to Jira events (issue created, updated, deleted)
- Notifies backend API
- Handles sync errors with retry

**Status:** 🟠 PLANNED (T0.3.3 Fase 2)

### 3. **Context Menu** (`src/modules/contextMenu.js`)
- Right-click on issue → "Link to OKR"
- Quick OKR selection dropdown

**Status:** 🟠 PLANNED (T0.3.3 Fase 3)

---

## API Integration

### Endpoints Used (from API_DESIGN.md)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/tasks` | Fetch all tasks (paginated) |
| GET | `/api/v1/okrs` | Fetch all OKRs |
| POST | `/api/v1/relationships` | Link task to OKR |
| GET | `/api/v1/trust-score` | Calculate project's trust score |
| GET | `/api/v1/orphans` | Get unlinked features |

### Example: Get Orphans

```javascript
import APISClient from './api/APISClient';

const client = new APISClient('http://localhost:5000/api/v1');

// Get all orphaned features in project "R0"
const orphans = await client.getOrphans('R0');

// orphans = {
//   "data": [
//     {
//       "task_id": "JIRA-456",
//       "title": "Fix database migration",
//       "status": "done",
//       "risk_level": "HIGH",
//       "suggestion": "Task was delivered but impact is untracked..."
//     }
//   ],
//   "summary": {
//     "total_orphans": 25,
//     "high_risk": 5,
//     "medium_risk": 10,
//     "low_risk": 10
//   }
// }
```

---

## Performance Targets

| Metric | Target | Implementation |
|--------|--------|-----------------|
| Plugin Load | <30s | Lazy loading + code splitting |
| API Call P95 | <500ms | Caching + indexed queries (backend) |
| Setup Time | <30 min | Automated setup script |
| Sidebar Render | <100ms | Virtual scrolling for large lists |

---

## Security

- **Auth:** OAuth2 with Jira
- **API Auth:** Bearer token (session-based)
- **Data:** No passwords stored, tokens rotated 24h
- **Transport:** HTTPS only
- **CORS:** Whitelist jira.yourdomain.com

---

## Testing

### Unit Tests

```bash
npm test
```

Covered:
- JiraAPI.authenticate() ✅
- APISClient.getOrphans() ✅
- Sidebar render ✅
- Error handling ✅

### Manual Testing (Checklist)

- [ ] Plugin loads in <30 seconds
- [ ] Sidebar displays orphans correctly
- [ ] "Link to OKR" modal opens
- [ ] Linking task → updates Jira issue
- [ ] Trust score updates after linking
- [ ] Webhook receives issue.created event
- [ ] API error (500) triggers retry

---

## Roadmap (Post-MVP)

**R1 (Next release):**
- Real-time notifications (Slack, email)
- Amplitude integration (adoption tracking)
- Historical analytics (orphan trends)

**R1.1:**
- GitHub Actions integration (CI/CD linking)
- Custom rules ("high-priority tasks need OKR")

---

## Troubleshooting

### Plugin won't load

**Check:**
1. Backend API is running (`curl http://localhost:5000/api/v1/health`)
2. Jira OAuth is configured
3. Browser console for errors

### Linking task fails

**Check:**
1. Backend /relationships endpoint is working
2. OKR ID is valid
3. Custom field `apos_okr_id` exists in Jira

### Trust score wrong

**Check:**
1. Backend /trust-score endpoint
2. All tasks synced (GET /tasks)
3. Relationships accurate (GET /relationships)

---

## References

- **SPEC.md** — Full technical specification (Seção 4.1)
- **API_DESIGN.md** — Backend API endpoints
- **PILOT_PLAN.md** — Testing with 3 personas
- **METRICS_BASELINE.md** — Performance targets

---

**Status:** 🟠 IN DEVELOPMENT  
**Last Updated:** 2026-07-23  
**Next:** Phase 2 - Jira API Connection
