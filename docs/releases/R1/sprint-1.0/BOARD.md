# Sprint 1 — Quadro Kanban

**Sprint:** R1 Sprint 1 (Dupla Via)
**Data:** 2026-07-21
**Milestone:** Dia 2 (2026-07-23)

---

## 📊 Resumo Visual

```
Backlog        A Fazer       Em Progresso    Em Revisão    Completo
   (1)            (2)            (0)             (0)          (2)

   ---            ↓              ↓               ↓
 R0-AC04      R1-S1-A1       (vazio)          (vazio)
               R1-S1-A2
               R1-S1-B1
               R1-S1-B2
```

---

## 📋 Backlog

| ID | Descrição | Trilha | SP | Prioridade |
|----|-----------|--------|----|-----------|
| R0-AC04 | Recrutar persona real externa | Meta | 0.5 | Média |

---

## ✅ A Fazer (Pronto para Começar)

| ID | Descrição | Trilha | SP | Estimativa | Critério |
|----|-----------|--------|----|-----------|----------|
| R1-S1-B1 | Implementar ProjectAdapter core | B | 1.5 | 1.5 dias | discover() extrai stack+módulos |
| R1-S1-B2 | Testes ProjectAdapter em Meu PDI | B | 0.5 | 0.5 dia | ≥50% descoberta |

---

## 🔄 Em Progresso

*(vazio — Sprint acabou de iniciar)*

---

## 👀 Em Revisão

*(vazio)*

---

## ✅ Completo

| ID | Descrição | Trilha | SP | Entregue |
|----|-----------|--------|----|----------|
| R1-S1-A1 | Tests agent_harness (1.587 LOC) | A | 0.75 | 100 testes, 100% pass ✅ |
| R1-S1-A2 | Tests capability_harness | A | 0.75 | 80 testes, 100% pass ✅ |

*(vazio)*

---

## 🚨 Bloqueado

*(nenhum)*

---

## 🔗 Dependências

| Task | Depende de | Desbloqueia |
|------|-----------|-------------|
| R1-S1-A1 | R0 harness (50% coverage existente) | Trilha B (confiança para ProjectAdapter) |
| R1-S1-B1 | R0 core (KnowledgeGraph, Node, Edge) | R1-S1-B2 |
| R1-S1-B2 | R1-S1-B1 | KR1 (S2) |

---

## 📈 Milestone Dia 2 — Critérios de Decisão

| Cenário | Decisão |
|---------|---------|
| ✅ Trilha A ≥70% E Trilha B funcional | Manter dupla via |
| ✅ Só Trilha A progrediu | Convergir para A (harness prioritário) |
| ✅ Só Trilha B progrediu | Convergir para B (KR1 prioritário) |
| ❌ Nenhuma progrediu | Pausar, reavaliar escopo |

---

**Board atualizado:** 2026-07-21
**Próxima atualização:** Daily Standup Dia 2 (2026-07-23)
