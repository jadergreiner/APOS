# Sprint Tasks — 0.4

**Sprint:** 0.4 — Knowledge Graph Design  
**Status:** 📋 PLANNING  
**Estimado:** ~5 dias  
**Dependencias:** ONTOLOGY_FOUNDATIONS.md (completo)

---

## Task Naming Convention

- **T{release}.{sprint}.{number}** — Task ID
  - Ex: T0.4.1, T0.4.2

---

## Tarefas

### Tier 1: Docs (Design Formal)

| ID | Titulo | Descricao | Duracao | Status |
|----|--------|-----------|---------|--------|
| T0.4.1 | KNOWLEDGE_GRAPH.md | Modelo formal do grafo: estrutura de nos, arestas, identificadores unicos, esquema de dados | 1d | 📋 Planned |
| T0.4.2 | NODE_TYPES.md | Catalogo de tipos de no com atributos: Task, Feature, Release, OKR, Metrica, Sprint, Persona | 0.5d | 📋 Planned |
| T0.4.3 | EDGE_TYPES.md | Catalogo de tipos de aresta: contribui_para, parte_de, alcanca, impacta, medido_por, bloqueia, depende_de | 0.5d | 📋 Planned |
| T0.4.4 | QUERY_PATTERNS.md | Padroes de navegacao: Task→OKR, Feature→Metrica, Release→OKR; inferencia de impacto | 1d | 📋 Planned |

### Tier 2: Code (Implementacao)

| ID | Titulo | Descricao | Duracao | Status |
|----|--------|-----------|---------|--------|
| T0.4.5 | types.py + graph.py | Implementar KnowledgeGraph: Node/Edge dataclasses, CRUD, traversal, IDs | 1.5d | 📋 Planned |

### Tier 3: Tests

| ID | Titulo | Descricao | Duracao | Status |
|----|--------|-----------|---------|--------|
| T0.4.6 | Testes graph.py | Testes unitarios (>80% cobertura): criacao, consulta, traversal, edge cases | 0.5d | 📋 Planned |

---

## Timeline Sugerido

| Dia | Foco | Tasks |
|-----|------|-------|
| D1 | Design docs | T0.4.1 + T0.4.2 (paralelo) |
| D2 | Design docs | T0.4.3 + T0.4.4 (paralelo) |
| D3 | Implementacao | T0.4.5 types.py + graph.py |
| D4 | Testes + QA | T0.4.6 + revisao geral |
| D5 | Buffer | Ajustes, refinamentos, revisao |

---

**Criado em:** 2026-07-21  
**Status:** 📋 AGUARDANDO INICIO
