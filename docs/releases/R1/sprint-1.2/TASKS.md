# Sprint Tasks — R1 Sprint 1.2

**Status:** Planning
**Início:** 2026-07-23 | **Término previsto:** 2026-07-25
**Velocity target:** 5.0 SP | **Total:** 5.0 SP (core) / 6.5 SP (stretch)

---

## Tasks Core (3.5 SP)

### US-001 — Cache de Perfil do Projeto (1.5 SP)

| Campo | Detalhe |
|-------|---------|
| **Descrição** | ProjectAdapter cacheia o profile descoberto em disco entre sessões. Evita re-descobrir a estrutura do projeto a cada execução. |
| **DoR** | ProjectAdapter funcional, ProjectProfile schema congelado |
| **DoD** | Cache em disco, TTL configurável, invalidação por hash, fallback para discover() |
| **Status** | planned |

**Cenários:**
- CT01: Cache hit → retorna profile sem executar detectores
- CT02: Cache miss → discover() executado, resultado cacheado
- CT03: Invalidação por hash mismatch → recálculo automático
- CT04: Cache corrompido → fallback graceful para discover()

### US-002 — Injeção de Contexto Automática (2.0 SP)

| Campo | Detalhe |
|-------|---------|
| **Descrição** | Hermes Agent recebe o ProjectProfile automaticamente no contexto de cada task. Elimina repetição manual de 3-5 parágrafos de stack/arquitetura. |
| **DoR** | US-001 concluída |
| **DoD** | CLI `apos context`, formato markdown, integração com Hermes |
| **Status** | planned |

## Tasks Stretch (1.5 SP)

### US-003 — Validação Código vs Documentação (1.5 SP)

| Campo | Detalhe |
|-------|---------|
| **Descrição** | Comando que compara o profile descoberto com a documentação em docs/SDD/. Detecta divergências entre código e docs antes que virem dívida. |
| **DoR** | US-001 concluída, BootstrapGateV2 existente |
| **DoD** | Comando `apos validate`, relatório de divergências, zero falsos positivos |
| **Status** | stretch |

---

## 📌 Commits de Rastreamento (Audit Trail)

*Registre aqui os commits a cada task concluída durante a sprint.*

| Commit | Task | Descrição |
|--------|------|-----------|
| `[hash]` | `US-001` | [descrição] |
| `[hash]` | `US-002` | [descrição] |
| `[hash]` | `US-003` | [descrição] |

**Total de commits rastreados:** 0

---

## Progress Summary

| Task | Completion | SP | Notes |
|------|-----------|-----|-------|
| US-001 (Cache Profile) | 0% | 1.5 | P0 — começar primeiro |
| US-002 (Inject Context) | 0% | 2.0 | P0 — depende de US-001 |
| US-003 (Validate Code vs Docs) | 0% | 1.5 | Stretch — se velocity permitir |
| **CORE TOTAL** | **0%** | **3.5 SP** | |
| **STRETCH TOTAL** | **0%** | **5.0 SP** | |

---

## Timeline

```
D1: US-001 (Cache) — implementar cache em disco + TTL
D2: US-001 finalize + US-002 (Context) — CLI apos context
D3: US-002 finalize + US-003 (Validate) — stretch 
```

---

**Sprint Quality Gate:** `python -m apos validate-sprint --sprint-root docs/releases/R1/sprint-1.2/`
