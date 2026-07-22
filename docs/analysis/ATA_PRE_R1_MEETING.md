# 📄 ATA — REUNIÃO PRÉ-R1 APOS

**Data:** 2026-07-21
**Formato:** Sala Virtual — CEO + 4 Agentes Especialistas
**CEO:** Jader Greiner
**Agentes Convocados:** SME (Domínio Semântico) | Scrum Master (Processo) | Tech Lead (Arquitetura) | Product Manager (Mercado)

---

## 1. OBJETIVO DA REUNIÃO

Validar aberturas, pontos críticos e discordâncias entre os agentes especialistas antes da formalização de R1. Gerar decisões fundamentadas para o roadmap.

---

## 2. ABERTURAS DOS AGENTES

### 2.1 SME — Domínio Semântico
**Voto:** Aprovado com Ressalvas
**Críticas:**
- Harness 50% de cobertura: observabilidade do sistema é caixa-preta
- Governance adiado (Sprint 0.8 cancelado): ontologia degrada sem enforcement
- ProjectAdapter é mudança arquitetural profunda, não sprint simples

### 2.2 Scrum Master — Processo
**Voto:** Crítico ao Planejamento Atual
**Críticas:**
- 194 arquivos no working tree: risco operacional de merge conflict
- Estimativas misturam documentação (10 SP/h) com código (4.7 SP/h) — previsibilidade comprometida
- Zero tarefas de dívida técnica no backlog de R1

### 2.3 Tech Lead — Arquitetura
**Voto:** Condicional (veto até Harness ≥80%)
**Críticas:**
- Harness 50% é passivo técnico: espinha dorsal de testes sem cobertura
- ProjectAdapter nunca testado contra repositório real: 6 SP é chute
- Context Engine e Capabilities têm zero testes de integração

### 2.4 Product Manager — Mercado
**Voto:** Acelerar (MVP em 2 semanas)
**Críticas:**
- Coverage não entrega valor ao usuário: ProjectAdapter é o que importa
- 7.7/10 do auditor + Approval assinado = GO já dado. Perder janela de mercado é risco maior
- Quer entregas visíveis a cada 3-4 dias, não 3 semanas de testes

---

## 3. MATRIZ DE DISCORDÂNCIA

| Decisão | SME | SM | Tech Lead | PM | CEO |
|---------|-----|-----|-----------|-----|-----|
| Sprint Zero (limpeza) | Desejável | **Obrigatório** | Desejável | Não prioridade | **✅ Aprovado** |
| Harness > features | Bloqueante | Bloqueante | VETA | Dívida técnica | ⏳ Pendente |
| ProjectAdapter prioridade | Arriscado | Precisa milestones | Protótipo primeiro | Máxima prioridade | ⏳ Pendente |
| Timeline R1 | 3 semanas | Sprint zero + 3 sem | 2-3 sem condicional | 2 semanas | ⏳ Pendente |
| Governance adiado | **Risco grave** | Pode esperar | Pode esperar R2 | Pode esperar R3 | ⏳ Pendente |

---

## 4. DECISÕES TOMADAS

### Decisão #001 — Sprint Zero ✅ APROVADO

**Decisão do CEO:** Limpar e commitar todo o working tree de R0, criando rastro oficial no repositório. Se R1 quebrar, é possível dar rollback e recomeçar.

**Justificativa:** Risco de 194 arquivos não versionados supera o custo de 1 dia de organização. Rastro oficial de R0 dá segurança para R1.

---

### Decisão #003 — Dupla Via ✅ APROVADO

### Decisão #004 — Governance em R2 ✅ APROVADO

### Decisão #005 — Automação de Cerimônias ✅ APROVADO

### Decisão #006 — Sincronização Automática com Jira ✅ APROVADO

### Decisão #007 — Ciclo Completo de Cerimônias ✅ APROVADO

### Decisão #008 — Ações de Retro Verificáveis ✅ APROVADO

**Decisão do CEO:** Toda ação de retrospectiva deve ter critério de verificação objetivo (SIM/NÃO), dono, due date, e ser carregada automaticamente no próximo Sprint Planning.

**Problema:** Em R0, ações de retro foram geradas mas nunca verificadas — viraram "desejos de ano novo".

**Schema revisado de `RetroAction`:**

| Campo | Descrição |
|-------|-----------|
| `id` | RETRO-NNN (identificador único) |
| `description` | O que precisa ser feito |
| `verification_criteria` | O que precisa ser verdade para considerar feito (SIM/NÃO) |
| `owner` | Responsável |
| `priority` | high / medium / low |
| `status` | pending → in_progress → verified → failed |
| `due_date` | Até quando |
| `verified_at` | Quando foi verificado |
| `verified_by` | Quem verificou |

**Fluxo de verificação:**

```
Sprint N Retro
  → Gera ações com critérios verificáveis
  → Salva em RETRO.md

Sprint N+1 Planning
  → Carrega automaticamente ações pendentes
  → Se 'high' não verificada → alerta (não bloqueia, mas explicita)
  → CEO decide: manter, estender, cancelar

Sprint N+1 Retro
  → Abre com verificação das ações anteriores
  → Não verificadas por 2 sprints → escala para CEO
```

**Métrica de saúde:** R1 target: ≥80% de ações verificadas dentro do prazo.

**Decisão do CEO:** R1 deve implementar o ciclo completo de cerimônias de sprint: Planning (início), Review (fim), Retro (fim). Todas automatizadas com reuniões virtuais e geração de artefatos.

**Ciclo de cada sprint:**

```
Sprint Start ──→ Sprint Planning ──→ Execução ──→ Sprint Review ──→ Sprint Retro
                      ↓                              ↓                    ↓
                  OKRs + Agentes              Devs demonstram       Time reflete
                  SPRINT_PLANNING.md          entregas              RETRO.md + ações
                                             REVIEW.md
```

**Cerimônias:**

| Cerimônia | Quando | Duração | Quem | Artefato | Status Código |
|-----------|--------|---------|------|----------|---------------|
| **Planning** | Início do sprint | 30-60min | Agentes + CEO | SPRINT_PLANNING.md | ✅ `SprintPlanningSession` + `render_markdown()` |
| **Review** | Fim do sprint | 20-30min | Devs + CEO + PM | REVIEW.md | ❌ Classe `SprintReview` por criar |
| **Retro** | Fim do sprint | 30-45min | Agentes + CEO | RETRO.md + ações | ✅ `Retrospective` + `RetroAction` (falta `render_markdown()`) |

**Formato de cada cerimônia:**
- **Planning:** Reunião virtual com 4 agentes (SME, SM, Tech Lead, PM). CEO decide. Template pré-preenchido com OKRs.
- **Review:** Devs convocados para demonstrar entregas. CEO + PM validam. Diff automático "planejado vs entregue".
- **Retro:** Interativa — rodadas de "o que foi bem", "o que foi mal", "o que melhorar". Ações viram input do próximo Planning.

**Cronograma de implementação em R1:**

| Sprint | Cerimônia | Ação |
|--------|-----------|------|
| Sprint 1 | Planning | Integrar com Sprint Start + Jira |
| Sprint 2 | Daily EOD | Standup automático |
| Sprint 3 | Review + Retro | Construir classes + gatilhos |

**Decisão do CEO:** Incorporar sync automático com Jira no Sprint 1 de R1, junto com Sprint Start automation.

**Justificativa:** O código existe (5.000+ LOC em scripts e plugin Jira). Faltam schedule, deploy e testes de integração (~2 SP). Atrito manual de sync em R0 foi alto — CEO precisou solicitar múltiplas vezes.

**Componentes:**

| Componente | Status R0 | Ação R1 |
|------------|-----------|---------|
| `jira_sync_tasks.py` | ✅ Pronto | Schedule em cron |
| `jira_add_sprint_agile.py` | ✅ Pronto | Integrar com Sprint Start |
| `jira_create_tasks.py` | ✅ Pronto | Integrar com Sprint Start |
| `jira_update_sprint.py` | ✅ Pronto | Integrar com Sprint End |
| Webhook plugin (webhooks.js) | ✅ Pronto | Deploy no ambiente Jira |
| Testes de integração | ❌ Ausente | 2 SP — Sprint 1 |

**Cronograma:**

| Sprint | Automação Cerimônias | Jira Sync |
|--------|----------------------|-----------|
| Sprint 1 | Sprint Start (BOARD, TASKS, SPRINT_PLANNING) | Schedule scripts + deploy webhook |
| Sprint 2 | Daily EOD (standup automático) | Cron diário Jira → APOS |
| Sprint 3 | Sprint End (RETRO, STATUS, métricas) | Trust Score com dados reais |

**Decisão do CEO:** Incorporar automação de cerimônias e artefatos como parte da execução de R1.

**Problema:** Em R0, CEO precisou solicitar manualmente cada artefato (BOARD, STATUS, TASKS, standups). Processo reativo, não escala.

**Solução — 3 gatilhos automáticos:**

| Gatilho | Artefato | Timeline |
|---------|----------|----------|
| Sprint Start | README.md, BOARD.md, TASKS.md, SPRINT_PLANNING.md | Sprint 1 |
| Daily EOD | DAILY_STANDUP.md (apenas se houve commit) | Sprint 2 |
| Sprint End | RETRO.md, STATUS.md, métricas consolidadas | Sprint 3 |

**Regras de design:**
- Daily standup só gera se houve commit no dia — silêncio = sem atividade
- Sprint start usa templates de `release_management/templates.py`
- Sprint end consolida daily standups + git log
- CEO pode override via comando manual

**Formato:** A definir — cron job (automático) vs skill invocável (manual sob demanda). Pendente CEO.

**Decisão do CEO:** Governance postergado para R2, após Harness ≥80%.

**Justificativa:** A cadeia Harness → Trust Score → Governance exige que o elo anterior esteja sólido antes do próximo. Governance ANTES de Harness seria construir regras sobre métrica não verificada.

**Cronograma consolidado:**

| Release | Foco |
|---------|------|
| R1 | Harness ≥80% + ProjectAdapter + Trust Score operacional |
| R2 | Governance (SemanticGate, AuditRunner, Metrics) |

**Decisão do CEO:** Sprint 1 executado em modelo de dupla via.

| Trilha | Foco | SP | KR |
|--------|------|-----|-----|
| A | agent_harness + capability_harness ≥80% | 2 SP | KR2a |
| B | ProjectAdapter protótipo funcional | 2 SP | KR1 (parcial) |

**Condições:**
1. Se protótipo revelar refatoração no harness → parar e repriorizar (Tech Lead)
2. Milestones de 2 dias para validar capacidade (Scrum Master)
3. evaluation.py (KR2b) mantido na Sprint 2 (SME)
4. KR1 completo na Sprint 2, não morre (PM)

**Implicações:**
- D003 (Timeline) pode ser calculada: ~2.5 a 3 semanas (Sprints 1-3)
- D004 (ProjectAdapter) resolvido: protótipo S1, completo S2
- KR2a desbloqueado

**Decisão do CEO:** OKRs de R1 revisados para refletir o ponto de inflexão de R0. OKR.md antigo (Knowledge Graph + loaders) substituído.

**R1-O1: APOS operacional no Meu PDI com contexto semântico vivo**

| KR | Descrição | Sprint | Critério de Sucesso |
|----|-----------|--------|---------------------|
| KR1 | ProjectAdapter descobre stack + domínio Meu PDI | S1 protótipo, S2 completo | ≥80% discovery automatizada |
| KR2a | agent_harness + capability_harness ≥80% | Sprint 1 | 1.587 LOC testados (~2 SP) |
| KR2b | evaluation.py ≥80% | Sprint 2 | 1.077 LOC testados (~1.5 SP) |
| KR3 | 3 chains Task→Feature→OKR com trust score | Sprint 2-3 | Decisões rastreadas no Meu PDI |
| KR4 | Baseline métricas + 1º comparativo pós-APOS | Iniciar imediatamente | Token, latência, retrabalho |

**Implicação crítica:** Com OKRs revisados, D002 (Harness coverage) agora pode ser decidida no contexto correto — KR2a e KR2b já definem o que precisa ser coberto e quando.

**Implicações:**
- Working tree será commitado em lotes lógicos (analysis, releases, código, scripts, plugins, testes)
- Tag de release R0 será criada para rollback
- R1 começará com baseline limpa

---

## 5. PRÓXIMAS DECISÕES (PENDENTES)

| # | Decisão | Opções | Status |
|---|---------|--------|--------|
| Decisão | Status |
|---------|--------|
| D002 Harness coverage | ⏳ Aguardando definição |
| D003 Timeline | ⏳ Aguarda D002 |
| D004 ProjectAdapter | ⏳ Aguarda D002 |
| D005 Governance | ⏳ Em aberto |

---

## 6. AÇÕES

| # | Ação | Responsável | Status |
|---|------|-------------|--------|
| A1 | Commitar working tree (Sprint Zero) | Hermes Agent | **✅ Concluído** |
| A2 | Decidir Harness coverage vs features | CEO | ⏳ Pendente |
| A3 | Decidir Timeline R1 | CEO | ⏳ Pendente |
| A4 | Formalizar cronograma R1 | Agentes | ⏳ Aguarda A2+A3 |

---

## 7. HISTÓRICO DE REVISÕES

| Versão | Data | Alteração |
|--------|------|-----------|
| 1.0 | 2026-07-21 | Criação da ATA. Decisão #001 registrada. |

---

**ATA gerada por:** Hermes Agent
**Arquivo:** `docs/analysis/ATA_PRE_R1_MEETING.md`
