# Sprint 0.4 — Knowledge Graph Design

**Release:** R0 (Fundações)  
**Periodo:** 2026-07-22 (Qua) a 2026-07-29 (Qua)  
**Status:** 🟢 ACTIVE — D1 em execucao (22 jul)  
**Ultima Atualizacao:** 2026-07-21  

---

## Contexto

Sprint 0.3 entregou MVP funcional (Plugin Jira, Trust Score Engine). 
Agora é hora de voltar ao plano original de R0 e projetar o **modelo formal de Knowledge Graph**.

A ontologia conceitual já foi definida em ONTOLOGY_FOUNDATIONS.md (Camada 3). 
A Sprint 0.4 formaliza esse design em documentos e implementa o grafo em código.

---

## Objetivo

Projetar o modelo de grafo conectado do APOS:
- Nós e arestas tipados (Task, Feature, Release, OKR, Metrica)
- Identificadores únicos e esquema de dados
- Padrões de navegação e inferência
- Implementação inicial em `apos/core/graph.py`

---

## Dependências

- ✅ ONTOLOGY_FOUNDATIONS.md — Conceitos core, relações, restrições (completo)
- 📋 Sprint 0.3 MVP — Plugin Jira, Trust Score Engine (completo)
- 📋 apso/core/ (stubs vazios) — types.py, graph.py, ontology.py

---

## Entregas

| ID | Entrega | Descricao |
|----|---------|-----------|
| T0.4.1 | KNOWLEDGE_GRAPH.md | Modelo formal do grafo |
| T0.4.2 | NODE_TYPES.md | Catalogo de tipos de no |
| T0.4.3 | EDGE_TYPES.md | Catalogo de tipos de aresta |
| T0.4.4 | QUERY_PATTERNS.md | Padroes de navegacao e inferencia |
| T0.4.5 | types.py + graph.py | Implementacao em codigo |
| T0.4.6 | Testes unitarios | >80% cobertura graph.py |

---

## Riscos

- Stubs vazios podem exigir mais refatoracao do que estimado
- Dependencia entre docs e codigo: T0.4.1-4 precisam vir antes de T0.4.5

---

**Criado em:** 2026-07-21  
**Proximo:** Preencher TASKS.md com detalhes de cada tarefa
