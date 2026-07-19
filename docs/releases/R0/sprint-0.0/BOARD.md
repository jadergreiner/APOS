# Sprint 0.0: Quadro Kanban

**Status Atualizado:** 2026-07-19 (Daily - Pré-Sprint, Kick-off: 22 jul)  
**Contexto:** R0-S0.1 (Platform Identity) COMPLETADA com sucesso em 1 dia. S0.0 inicia 22 jul.

---

## 📊 Resumo Visual

```
Backlog        A Fazer       Em Progresso    Em Revisão    Completo
   (8)            (5)            (0)            (0)          (0)
   
   ↓→ Preparação  ↓             ↓              ↓             ↓
```

---

## 📋 Backlog (Não Iniciado)

**Total de Backlog**: 8 items | 8 pontos planejados | 0 iniciados

### Tier 1: Implementação Core (Framework + Bootstrap)

- [ ] **T0.0.1** — Implementar Release Management Framework (1d) *REPOSITÓRIO PRONTO*
  - `docs/releases/R0/SPRINT_PLAN.md` ✅ Criado
  - `docs/releases/R0/BACKLOG.md` ✅ Criado
  - `docs/releases/R0/DEPENDENCY_MAP.md` ✅ Criado
  - Sprint templates estruturados ✅

- [ ] **T0.0.2** — Implementar Bootstrap Gate (2d) *NÃO INICIADO*
  - `apos/bootstrap/gate.py` — BootstrapGate class
  - `apos/bootstrap/validators/` — Validadores especializados
  - `apos/bootstrap/templates/` — Docs auto-gerados
  - Tests + documentação

- [ ] **T0.0.3** — Implementar Auto-Identificação APOS + CLI (1d) *NÃO INICIADO*
  - `apos/__init__.py` com metadata
  - `apos/bootstrap/session.py` — SessionManager
  - `apos/__main__.py` — CLI (`python -m apos init`)
  - Testes end-to-end

### Tier 2: Validação de Job (JTBD Discovery)

- [ ] **T0.0.A** — Conduzir Entrevistas JTBD (2d) *PREPARAÇÃO NECESSÁRIA*
  - 5+ personas: PM, Agente, CTO, Stakeholder, Early Adopter
  - Preparar kit de entrevista (questões, roteiro)
  - Agendar + conduzir entrevistas (23-24 jul)
  - Documentar raw insights

- [ ] **T0.0.B** — Mapear Forças de Progresso (1d) *DEPENDENTE DE T0.0.A*
  - Analisar Push/Pull/Ansiedade/Hábito por persona
  - Criar matriz de forças (scores 1-10)
  - Documentar competitive landscape

- [ ] **T0.0.C** — Finalizar Job Statement (1d) *DEPENDENTE DE T0.0.B*
  - Rascunho job statement baseado em dados
  - Validar 3 dimensões (Funcional/Emocional/Social)
  - Obter sign-off de stakeholders

---

## ✅ A Fazer (Pronto para Começar)

**Prioridade ALTA — Iniciar HOJE (19 jul)**

1. **[CRÍTICO]** Preparar Kit de Entrevista JTBD
   - [ ] Estruturar questões por persona (PM vs Agente vs CTO)
   - [ ] Criar roteiro (60-90 min)
   - [ ] Preparar termo de consentimento
   - [ ] Setup de gravação (Zoom/Teams)
   - **Deadline**: 20 jul (segunda)

2. **[CRÍTICO]** Agendar 5+ Entrevistas JTBD
   - [ ] PM (produto) — frustração de alinhamento
   - [ ] Agente de IA — necessidades de contexto
   - [ ] CTO/Arquiteto — viabilidade técnica
   - [ ] Stakeholder (negócios) — ROI
   - [ ] Early Adopter — adoção/feedback
   - **Target**: 23-24 jul | **Deadline Agenda**: 21 jul

3. **[IMPORTANTE]** Recrutamento de Beta Customers
   - [ ] Identificar 10 early adopters (LinkedIn, Product communities)
   - [ ] Preparar outreach message
   - [ ] Começar contatos
   - **Target**: 10 customers enrollados por Sep 2026

---

## 🔄 Em Progresso

**Atual**: Nenhum (fase de planejamento/preparação)

---

## 👀 Em Revisão

**Atual**: Nenhum

---

## ✅ Completo

### Sprint 0.1: Platform Identity ✅ (Concluído: 19 jul)

- [x] **VALUE_PROPOSITION.md** — Diferenciação + benefícios (1.0)
- [x] **COMPETITIVE_POSITIONING.md** — Análise de mercado (1.0)
- [x] **OKR.md (R0-R4)** — Objetivos estratégicos (1.0)
- [x] **ROADMAP_R1_R4.md** — Plano 18 meses (1.0)

**Taxa de Conclusão**: 100% | **Pontos**: 5 | **Esforço Real**: 1 dia

---

## 🚨 Bloqueado

**Atual**: Nenhum bloqueado permanentemente

**Dependências Críticas**:
- T0.0.A (Entrevistas) → bloqueia T0.0.B
- T0.0.B (Forças) → bloqueia T0.0.C
- T0.0.1-T0.0.3 (Bootstrap) → Parallelizável com T0.0.A

---

## 📈 Capacidade & Timeline

| Fase | Período | Capacidade | Tarefas | Status |
|------|---------|-----------|---------|--------|
| Preparação | 19-21 jul | 3 dias | Kit + Agenda | 🚀 HOJE |
| Execução S0.0 | 22-26 jul | 5 dias | T0.0.1-C | 📋 Pronto |
| Execução S0.1 | 29 jul+ | TBD | Próximo sprint | 📅 |

---

## ⚡ Indicadores de Status

**Saúde Geral**: 🟢 **VERDE** (no track)
- Fase anterior (S0.1) entregou 5 pts em 1 dia (+25% velocidade)
- Preparação S0.0 crítica = agendar entrevistas HOJE
- Zero blockers identificados

**Risco**: 🟡 **MÉDIO**
- Recrutamento de entrevistas pode ser lento
- Mitigação: Iniciar outreach em paralelo com múltiplos canais

---

## 🔗 Dependências Externas

- **Personas disponibilidade** — Confirmar até 21 jul
- **Beta customer recruitment** — Começar AGORA
- **Engenharia Bootstrap Gate** — Pode paralelizar com JTBD

---

**Próxima Atualização**: 20 jul 09:00 (Daily — Preparo de Kit)  
**Board Atualizado**: Diariamente às 07:00 durante sprint

