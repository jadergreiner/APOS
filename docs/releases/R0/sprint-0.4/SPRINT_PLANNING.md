# Sprint Planning — Sprint 0.4

**Data:** 2026-07-21  
**Sprint:** 0.4 — Knowledge Graph Design  
**Periodo:** 2026-07-22 (Qua) a 2026-07-29 (Qua)  
**Duracao:** 7 dias (5 dias uteis)  
**Attendees:** Jader Greiner  

---

## 🎯 Goals

1. Projetar modelo formal de Knowledge Graph do APOS
2. Implementar graph.py com Node/Edge tipados
3. Testes unitarios >80%
4. Docs: NODE_TYPES, EDGE_TYPES, QUERY_PATTERNS

---

## 📋 Planned Tasks (6 tasks, 5.0d estimados)

| ID | Titulo | Estimativa |
|----|--------|-----------|
| T0.4.1 | KNOWLEDGE_GRAPH.md — Modelo formal do grafo | 1.0d |
| T0.4.2 | NODE_TYPES.md — Catalogo de tipos de no | 0.5d |
| T0.4.3 | EDGE_TYPES.md — Catalogo de tipos de aresta | 0.5d |
| T0.4.4 | QUERY_PATTERNS.md — Padroes de navegacao | 1.0d |
| T0.4.5 | types.py + graph.py — Implementacao | 1.5d |
| T0.4.6 | Testes graph.py >80% | 0.5d |

**Total estimado:** 5.0d  
**Velocity target:** 5.0d

---

## 📅 Timeline Sugerido

| Dia | Data | Foco | Tasks |
|-----|------|------|-------|
| D1 | 22 jul (Qua) | Design docs | T0.4.1 + T0.4.2 paralelo |
| D2 | 23 jul (Qui) | Design docs | T0.4.3 + T0.4.4 paralelo |
| D3 | 24 jul (Sex) | Implementacao | T0.4.5 graph.py |
| D4 | 27 jul (Seg) | Testes | T0.4.6 + revisao |
| D5 | 28-29 jul | Buffer/ajustes | Refinamentos |

---

## 🔗 Dependencias

- ONTOLOGY_FOUNDATIONS.md (completo — Camada 3 ja definida conceitualmente)

## 🚨 Riscos

- Stubs types.py/graph.py vazios podem exigir mais refatoracao que o estimado
- Dependencia sequencial: docs (T0.4.1-4) antes do codigo (T0.4.5)

---

**Planning criado:** 2026-07-21  
**Proxima cerimonia:** Daily Standup (22 jul)
