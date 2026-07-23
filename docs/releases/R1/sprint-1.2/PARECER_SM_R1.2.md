# 🏗️ Parecer do Scrum Master — Planejamento R1 Sprint 1.2

**Autor:** Hermes Agent (Scrum Master)
**Sprint:** R1 Sprint 1.2 — Contexto + Ontologia + Observabilidade
**Data:** 2026-07-23
**Baseado em:** FINDINGS_TECH_LEAD.md, dados reais de S1.0 e S1.1, R1_PLAN_REVISED.md

---

## 1. 📊 Diagnóstico da Saúde do Sprint Atual (S1.1)

| Métrica | Planejado | Real | Δ | 
|---------|-----------|------|---|
| **SP totais** | 6.5 SP | **6.0 SP** (92%) | 🟡 0.5 SP carry-over |
| **Tasks core** | 4 tasks | **3/4 concluídas** | 🟢 |
| **T1.1.5 (Polish)** | 1.0 SP | ✅ 200 testes, 100% core coverage | 🟢 Excedeu |
| **R1.T2 (Capabilities)** | 2.0 SP | ✅ 68 testes, 85% coverage | 🟢 Excedeu |
| **R1.2 (Bootstrap Gate 2.0)** | 3.0 SP | ✅ gate_v2.py, 19 testes, 95% coverage | 🟢 Excedeu |
| **R0-AC04 (Stakeholder)** | 0.5 SP | 📋 Em andamento (kit preparado) | 🟡 Carry-over |
| **Regressão** | 0 bugs | ✅ Zero regressão | 🟢 |
| **WIP simultâneo** | 2 tasks | Máx 2 tasks/dia via subagentes | 🟢 |

### 1.1 Análise de Saúde

**🟢 Pontos Fortes:**
- **Consistência**: Segunda sprint consecutiva com entrega ≥92% — não é sorte, é padrão.
- **Qualidade técnica**: Todas as entregas excederam métricas mínimas (85-100% coverage vs 80% target).
- **Zero regressão**: Nenhuma quebra de testes existentes — disciplina de DoR está funcionando.
- **Automação produtiva**: Subagents (delegate_task) comprovadamente eficazes para tarefas de teste (8x mais rápido) e implementação.

**🟡 Atenção:**
- **0.5 SP carry-over**: R0-AC04 (Stakeholder) não foi concluída — task de discovery que compete com tasks técnicas.
- **WIP limit empírico**: O time (1 pessoa + subagents) consegue sustentar **2 tasks simultâneas** no máximo. Acima disso, o contexto humano vira gargalo (revisão, integração).
- **R0-AC04 é atípica**: Task de discovery/recrutamento não compete bem com tasks técnicas no mesmo sprint — requer modo "pessoa" (recrutar, agendar, entrevistar) que subagent não faz.

### 1.2 Capacidade do Time

| Fator | Valor | Fonte |
|-------|-------|-------|
| **Pessoas** | 1 (Jader = CEO + PM + Tech Lead + Dev) | Perfil do projeto |
| **Assistentes AI** | Subagents via delegate_task + session agents | Evidência empírica |
| **Stack** | 100% AWS serverless + Python | Documentado |
| **Tamanho código** | ~3.400 arquivos .py, ~130 testes (cresce ~200/sprint) | FINDINGS |
| **Disponibilidade** | 100% (full-time) | Estimado |

---

## 2. 📈 Análise de Velocity

### 2.1 Histórico Real

| Sprint | Planejado | Entregue | % | Observação |
|--------|-----------|----------|---|------------|
| **S0** (R0 sprint-impl) | — | ~4.5 SP | — | Baseline histórica |
| **S1.0** | 3.5 SP | **3.5 SP** | **100%** | 180 testes, 99% harness coverage ✅ |
| **S1.1** | 6.5 SP | **6.0 SP** | **92%** | 287+ testes novos, 3/4 tasks ✅ |
| **Média simples** | — | **4.75 SP** | — | S1.0 + S1.1 |
| **Média ponderada** | — | **4.7 SP** | — | Incluindo S0 baseline |

### 2.2 Velocity Real vs Estimada

```
SP por Sprint
     ^
  7 -| 
  6 -|     ● 6.0 (S1.1)
  5 -|     ┃
  4 -| ● 4.5 (S0)    ● 4.7 (média)
  3 -| ┃   ┃   ● 3.5 (S1.0)
  2 -| ┃   ┃   ┃
  1 -| ┃   ┃   ┃
  0 -┼───┼───┼───┼───
      S0  S1.0 S1.1  S1.2?
```

### 2.3 Capacidade Projetada para R1.2

**Recomendação de WIP: 5.0 SP**

Justificativa:
- **Velocity média**: 4.75 SP/sprint (S1.0 + S1.1)
- **Tendência**: Crescimento de 71% de S1.0 para S1.1 (curva de aprendizado + subagents)
- **Fator carry-over**: 0.5 SP de R0-AC04 precisa ser absorvido
- **Booking realista**: **4.5–5.5 SP** (Range seguro: entre a média e o pico)
- **Recomendado: 5.0 SP** — conservador o suficiente para absorver imprevistos, ambicioso o suficiente para manter ritmo

**WIP máximo recomendado: 5.5 SP** (apenas se R0-AC04 for concluída extra-sprint)

| Cenário | SP | Confiança |
|---------|----|-----------|
| 🟢 Seguro (média) | 4.5 SP | 95% |
| 🟡 Alvo (recomendado) | **5.0 SP** | 80% |
| 🔴 Agressivo (pico S1.1) | 6.0 SP | 50% |

---

## 3. 🎯 User Stories para R1.2 (Baseadas nos Findings)

A partir dos **5 findings** (D01-D05), mapeio as seguintes User Stories priorizadas:

### Topo da Pilha — Deve Entregar (Core)

| # | US | Finding | Descrição | SP | Depende de | Risco |
|---|----|---------|-----------|----|-----------|-------|
| **US-01** | **Auto-Contexto Inter-Sprint** | D01, D03 | Como Tech Lead, quero que o contexto da sprint anterior seja automaticamente carregado na nova sprint, para não perder 20-30min retomando. | **2.0** | R1.2 (Bootstrap Gate) ✅ concluído | 🟡 Médio |
| **US-02** | **Validação Código ↔ Docs** | D02 | Como Tech Lead, quero que a documentação seja validada contra o código automaticamente, para detectar desalinhamento em horas (não dias). | **1.5** | R1.T2 (Capabilities) ✅ concluído | 🔴 Alto — risco de falso positivo |
| **US-03** | **Observabilidade Meu PDI** | — [R1.T3 backlog] | Como PM, quero coletar métricas baseline do Meu PDI (token count, latência, retrabalho %) para validar impacto do APOS. | **1.0** | R1.2 ✅, CI/CD existente | 🟡 Médio |

### Segunda Camada — Se Houver Capacidade

| # | US | Finding | Descrição | SP | Depende de | Risco |
|---|----|---------|-----------|----|-----------|-------|
| **US-04** | **Rastro de Decisões Unificado** | D04 | Como Tech Lead, quero um ponto centralizado de rastreamento de decisões (código → ADR → SDD), para não perder contexto em 20+ documentos. | **1.5** | US-01, US-02 | 🟡 Médio |
| **US-05** | **Stack-Aware Agent Guard** | D05 | Como Tech Lead, quero que os agentes conheçam a stack real do projeto (AWS serverless, DynamoDB), para evitar assumptions erradas (Redis, PostgreSQL). | **1.0** | US-01 | 🟢 Baixo |
| **R0-AC04** | **Stakeholder Externo** | — | Recrutar persona real, aplicar JTBD interview, documentar findings. | 0.5 | — | 🟢 Baixo |

### Priorização Final — Recomendação de Escopo

```
┌─────────────────────────────────────────────────────┐
│              R1 SPRINT 1.2 — ESCOPO RECOMENDADO      │
├─────────────────────────────────────────────────────┤
│                                                       │
│  🔴 CORE (OBRIGATÓRIO) — 4.5 SP                      │
│  ┌───────────────────────────────────────────────┐   │
│  │ US-01: Auto-Contexto Inter-Sprint     2.0 SP  │   │
│  │ US-02: Validação Código ↔ Docs        1.5 SP  │   │
│  │ US-03: Observabilidade Meu PDI         1.0 SP  │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  🟡 ESTRETCH (CAPACIDADE EXTRA) — 2.0-3.0 SP          │
│  ┌───────────────────────────────────────────────┐   │
│  │ US-04: Rastro Decisões Unificado      1.5 SP  │   │
│  │ US-05: Stack-Aware Agent Guard        1.0 SP  │   │
│  │ R0-AC04 (stakeholder carry-over)      0.5 SP  │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  TOTAL CORE: 4.5 SP                                   │
│  TOTAL C/ STRETCH: 6.5 SP                             │
│  WIP RECOMENDADO: 5.0 SP (core + 0.5 carry)          │
└─────────────────────────────────────────────────────┘
```

---

## 4. 🔗 Dependências e Ordem de Implementação

### Grafo de Dependências

```
US-01 (Auto-Contexto) ──→ US-04 (Rastro Decisões)
       │                        │
       ▼                        ▼
US-02 (Validação Docs)    US-05 (Stack Guard)
       │
       ▼
US-03 (Observabilidade)
       │
       ▼
R1.3 (Ontology Adapter — sprint futuro)
```

### Ordem Recomendada

| Ordem | US | Justificativa |
|-------|----|--------------|
| **1º** | US-01 (2.0 SP) | **Fundação** — sem contexto transversal, as outras US sofrem do mesmo mal que tentam curar. Desbloqueia US-04 e US-05. |
| **2º** | US-03 (1.0 SP) | **Paralelizável** com US-02 — não depende de descoberta, é configuração de observabilidade. Setup de logging não compete com código. |
| **3º** | US-02 (1.5 SP) | **Pode começar após US-01 scaffold** — validação código vs docs usa o contexto carregado. Maior risco técnico (falso positivo), então começar cedo. |
| **4º** | US-04/05 (Stretch) | **Dependentes de US-01** — construir rastro e guardrails depois do contexto funcionar. |

**Paralelização possível:**
- US-01 (scaffold) + US-03 (setup) podem rodar simultaneamente (2 tracks)
- US-02 + US-03 podem rodar simultâneas (validação + observabilidade)

### WIP Tracking

```
┌─────────┬────────┬────────┬────────┬────────┬────────┐
│         │  D1    │  D2    │  D3    │  D4    │  D5    │
├─────────┼────────┼────────┼────────┼────────┼────────┤
│ US-01   │ ████░░ │ ██████ │ ██████ │ ██████ │ ██████ │
│ (2.0)   │ setup  │ impl   │ tests  │        │        │
├─────────┼────────┼────────┼────────┼────────┼────────┤
│ US-03   │ ██░░░░ │ ██████ │ ██████ │ ██████ │ ██████ │
│ (1.0)   │        │ setup  │ setup  │        │        │
├─────────┼────────┼────────┼────────┼────────┼────────┤
│ US-02   │        │ ░░░░░░ │ ██████ │ ██████ │ ██████ │
│ (1.5)   │        │        │ impl   │ tests  │        │
├─────────┼────────┼────────┼────────┼────────┼────────┤
│ US-04/05│        │        │        │ ░░░░░░ │ ██████ │
│ Stretch │        │        │        │        │        │
└─────────┴────────┴────────┴────────┴────────┴────────┘
```

---

## 5. ⚠️ Análise de Riscos

### Matriz de Riscos

| # | Risco | Prob | Impacto | Severidade | Mitigação |
|---|-------|------|---------|-----------|-----------|
| **R1** | **US-02: Falsos positivos** na validação código↔docs | 🔴 Alta | 🔴 Alto | 🔴 **CRÍTICO** | Implementar com modo "suggest, não enforce" na v1. Testar em repositório conhecido primeiro. Gatilho: se >10% falsos positivos nas primeiras 50 validações, pausar e recalibrar. |
| **R2** | **US-01: Contexto transversal polui** em vez de ajudar | 🟡 Média | 🟡 Médio | 🟡 **ALTO** | Design com escopo estrito (apenas sprint atual + anterior). Não carregar todo o histórico. |
| **R3** | **US-03: Observabilidade bloqueada** em Meu PDI (permissões, deploy) | 🟡 Média | 🟡 Médio | 🟡 **ALTO** | Plano B: logging manual em arquivo local. Não depender de infraestrutura de produção. |
| **R4** | **Overhead de contexto humano** — 1 pessoa revendo 4+ US | 🟡 Média | 🟡 Médio | 🟡 **ALTO** | Subagents executam, Jader revisa. Limitar WIP a 2 tasks simultâneas. Buffer de revisão ao final de cada dia. |
| **R5** | **Stakeholder externo (R0-AC04)** não recrutado a tempo | 🟢 Baixa | 🟢 Baixo | 🟢 **BAIXO** | Aceitar carry-over para S1.3. Auto-validação é suficiente para esta sprint. |
| **R6** | **Dívida técnica acumulada** — 3 sprints sem refator | 🟡 Média | 🟡 Médio | 🟡 **ALTO** | Alocar 0.5 SP por sprint para refator preventivo. Monitorar cobertura de testes como proxy de saúde. |

### Heatmap de Riscos

```
Impacto
  ▲
  │
  │     R1 (FP)
  │     ●
  │
  │  R2  R3  R4
  │  ●   ●   ●
  │
  │           R5  R6
  │           ●   ●
  │
  └───────────────────▶ Probabilidade
       Baixa  Média  Alta
```

### Riscos da Sprint Anterior que Não se Concretizaram

| Risco S1.1 | Ocorreu? | Lição |
|-----------|---------|-------|
| Capabilities 0% coverage → difícil | ❌ Não — 68 testes, 85% coverage ✅ | Subagents performam bem em cobertura |
| Bootstrap Gate 2.0 depende de API que mudou | ❌ Não — ProjectAdapter estável | Congelamento de API funcionou |
| Sem stakeholder externo reduz validação | 🟡 Parcial — R0-AC04 não concluída | Task de discovery precisa de tratamento diferente |

---

## 6. 📋 Definition of Ready (DoR) — Proposta Geral

### DoR Geral (G0) — Toda Task

#### Contexto
- [ ] **G0-CTX-01**: Repositório APOS acessível em `/mnt/c/repo/APOS`
- [ ] **G0-CTX-02**: `python3 -c "import apos"` funciona sem erro
- [ ] **G0-CTX-03**: `pytest --version` disponível
- [ ] **G0-CTX-04**: Módulo alvo da task existe ou está documentado como novo
- [ ] **G0-CTX-05**: Contexto da sprint anterior carregado na sessão ativa

#### Dependências
- [ ] **G0-DEP-01**: Nenhuma dependência externa bloqueante (API, serviço externo)
- [ ] **G0-DEP-02**: Tasks predecessor concluídas (ver BOARD.md)
- [ ] **G0-DEP-03**: Artefatos de design existem ou foram criados na sprint

#### Baseline
- [ ] **G0-BSL-01**: Coverage baseline registrado (`pytest --cov=apos/<modulo> --cov-report=term-missing`)
- [ ] **G0-BSL-02**: Testes existentes passando **antes** de qualquer alteração
- [ ] **G0-BSL-03**: `git status` limpo (working tree sem modificações não comitadas)
- [ ] **G0-BSL-04**: Branch criada a partir de `main` ou branch base atualizada

#### Ambiente
- [ ] **G0-ENV-01**: Python ≥ 3.9 disponível
- [ ] **G0-ENV-02**: Dependências do projeto instaladas (`pip install -e ".[dev]"`)
- [ ] **G0-ENV-03**: Espaço em disco > 500 MB

### DoR Específico por US (G1)

| US | Critérios Adicionais |
|----|---------------------|
| **US-01** | Mecanismo de persistência definido (JSON, SQLite, DynamoDB?); Schema da "sessão comprimida" acordado |
| **US-02** | Algoritmo de diff código↔docs definido; Limiar de falso positivo aceito pelo time; Repositório de teste conhecido |
| **US-03** | Métricas a coletar definidas (token count, latência, retrabalho %); Destino dos dados acordado (CloudWatch, arquivo local) |
| **US-04** | Formato de entrada (ADR, SDD, decisões) conhecido; Mecanismo de linking código→decisão definido |
| **US-05** | Stack real documentada (DynamoDB single-table, Cognito, S3/CloudFront, Lambda); Comportamento esperado quando agentes assumem stack errada |

---

## 7. ✅ Definition of Done (DoD) — Proposta Geral

### DoD Geral (Aplicável a Toda US)

#### Código
- [ ] **COD-01**: Implementação completa conforme critérios de aceite
- [ ] **COD-02**: Testes unitários escritos (cobertura ≥80% no módulo alterado)
- [ ] **COD-03**: `pytest . -v` — todos os testes passam, zero regressão
- [ ] **COD-04**: `pytest --cov=apos/<modulo>` — coverage ≥80%
- [ ] **COD-05**: Sem dead code, sem imports não utilizados (verificado via `pylint`/`ruff`)
- [ ] **COD-06**: Type hints presentes em funções públicas
- [ ] **COD-07**: Docstrings em funções públicas (mínimo: descrição, args, returns)

#### Integração
- [ ] **INT-01**: Integração com módulos existentes testada (sem quebras)
- [ ] **INT-02**: Se aplicável, smoke test com Meu PDI real
- [ ] **INT-03**: Performance aceitável (sem regressão >10% em tempo de execução)

#### Documentação
- [ ] **DOC-01**: README do módulo atualizado (se aplicável)
- [ ] **DOC-02**: ADR criado/atualizado para decisões arquiteturais relevantes
- [ ] **DOC-03**: CHANGELOG ou release notes com entrada da US

#### Governança
- [ ] **GOV-01**: Código commitado com mensagem descritiva (`git commit -m "US-0X: descrição"`)
- [ ] **GOV-02**: Pull Request aberto e revisado
- [ ] **GOV-03**: BOARD.md atualizado com status final
- [ ] **GOV-04**: TASKS.md atualizado com progresso e métricas reais
- [ ] **GOV-05**: Jira issue movida para "Concluído"

### DoD Específico por US

| US | Critérios Adicionais |
|----|---------------------|
| **US-01** | Ao iniciar nova sprint, contexto anterior é carregado em <5s; Sessão comprimida armazena: tasks concluídas, decisões, blockers, coverage atual |
| **US-02** | Script de validação executa em <30s para módulo médio; Taxa de falso positivo <5% nos primeiros 100 testes |
| **US-03** | Dados de baseline sendo coletados por ≥24h consecutivas; Dashboard ou planilha com métricas visível |
| **US-04** | Consulta por "decisão sobre X" retorna até 3 resultados em <3 chamadas; Rastro inclui: código → ADR → SDD → data → autor |
| **US-05** | Agente consulta stack antes de fazer assumption; Resposta errada de stack é detectada e corrigida em <1min; Log de correções disponível |

---

## 8. 🚀 Recomendações Executivas

### Para o Sprint Planning

1. **Comprometer 4.5 SP (core) + 0.5 carry-over = 5.0 SP**
   - US-01 (2.0), US-02 (1.5), US-03 (1.0), R0-AC04 (0.5)
   - Esticar para US-04/US-05 apenas se D1-D2 mostrarem folga consistente

2. **Proteger o sprint de WIP >2 tasks simultâneas**
   - Uma pessoa = gargalo de revisão. Subagents escrevem, Jader revisa.
   - Alternar: manhã = review de código, tarde = nova implementação

3. **R0-AC04 merece tratamento especial**
   - É a 3ª sprint que esta task aparece
   - Sugiro: transformar em "spike externo" (rodar em background, não contar no sprint commitment)
   - Ou: alocar 30min fixes por dia para recrutamento

4. **Incluir 0.5 SP de refator preventivo por sprint**
   - Dívida técnica de 3 sprints sem refator começa a pesar
   - Sugiro: "US-00: Refator + cleanup" como item recorrente (0.5 SP)

### Timeline Recomendada

```
┌─────────────────────────────────────────────────────────────────────┐
│              R1 SPRINT 1.2 — TIMELINE (5 DIAS)                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  D1 (24 jul):                                                       │
│   09:00-09:30 — Sprint Planning + carregar contexto US-01           │
│   09:30-12:00 — US-01: Design + scaffold (subagent)                 │
│   12:00-13:00 — Review + ajustes                                    │
│   13:00-15:00 — US-03: Setup inicial observabilidade (subagent)     │
│   15:00-15:30 — Daily Standup                                       │
│                                                                     │
│  D2 (25 jul):                                                       │
│   09:00-12:00 — US-01: Implementação completa + testes              │
│   12:00-13:00 — Review US-01 + commit                               │
│   13:00-15:00 — US-02: Design validação código↔docs                 │
│   15:00-15:30 — Daily Standup                                       │
│                                                                     │
│  D3 (26 jul):                                                       │
│   09:00-12:00 — US-02: Implementação + testes iniciais              │
│   12:00-13:00 — US-03: Finalizar setup + verificar coleta           │
│   13:00-15:00 — US-02: Testes de validação + falso positivo         │
│   15:00-15:30 — Daily Standup                                       │
│                                                                     │
│  D4 (27 jul):                                                       │
│   09:00-12:00 — US-02: Finalizar + documentar                       │
│   12:00-13:00 — Review + correções US-02                            │
│   13:00-15:00 — Stretch: US-04 ou US-05 (se folga)                  │
│   15:00-15:30 — Daily Standup                                       │
│                                                                     │
│  D5 (28 jul):                                                       │
│   09:00-11:00 — Stretch + polish                                    │
│   11:00-12:00 — Sprint Review (demo interno)                        │
│   12:00-13:00 — Retrospective                                       │
│   13:00-15:00 — Buffer + fechamento de docs                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 9. 📊 Resumo Executivo

```text
┌────────────────────────────────────────────────────────────────────┐
│                PARECER DO SCRUM MASTER — R1 Sprint 1.2              │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  SITUAÇÃO ATUAL                                                     │
│  ├─ S1.1: 6.0/6.5 SP (92%) — segunda sprint consecutiva >90%      │
│  ├─ Tendência: crescimento de 71% na capacidade (3.5 → 6.0 SP)    │
│  └─ Maturidade: time e subagents operando em regime previsível     │
│                                                                     │
│  VELOCITY                                                            │
│  ├─ Média real: 4.75 SP/sprint (S1.0 + S1.1)                       │
│  ├─ Recomendação: 5.0 SP para S1.2 (conservador + 0.5 carry)      │
│  └─ WIP máximo: 2 tasks simultâneas (gargalo humano de revisão)    │
│                                                                     │
│  ESCOPO RECOMENDADO (4.5 SP core + 0.5 carry)                       │
│  ├─ US-01: Auto-Contexto Inter-Sprint          2.0 SP (🔴 alta)    │
│  ├─ US-02: Validação Código ↔ Docs             1.5 SP (🔴 alta)    │
│  ├─ US-03: Observabilidade Meu PDI             1.0 SP (🟡 média)   │
│  └─ R0-AC04: Stakeholder (carry-over)          0.5 SP (🟢 baixa)   │
│                                                                     │
│  STRETCH (2.0-3.0 SP adicionais)                                    │
│  ├─ US-04: Rastro Decisões Unificado           1.5 SP               │
│  ├─ US-05: Stack-Aware Agent Guard             1.0 SP               │
│                                                                     │
│  PRINCIPAL RISCO                                                     │
│  └─ US-02: Falso positivo na validação código↔docs (prob: alta,    │
│      impacto: alto) — mitigar com modo "suggest, não enforce" v1   │
│                                                                     │
│  SAÚDE DO PROCESSO                                                   │
│  ├─ DoR atual (G0 + G1) funcionando — zero regressão em 2 sprints │
│  ├─ DoD proposto: 17 critérios gerais + específicos por US         │
│  └─ Melhoria: adicionar 0.5 SP de refator preventivo por sprint   │
│                                                                     │
│  Veredito: ✅ TIME PRONTO PARA R1.2 COM 5.0 SP                      │
│  Condição: WIP ≤ 2, US-02 em modo suggest na v1                    │
└────────────────────────────────────────────────────────────────────┘
```

---

**Elaborado por:** Hermes Agent (Scrum Master)
**Baseado em dados reais:** S1.0 (3.5/3.5 SP), S1.1 (6.0/6.5 SP), FINDINGS_TECH_LEAD.md
**Documentos relacionados:**
- `docs/discovery/FINDINGS_TECH_LEAD.md` — Findings e User Stories
- `docs/releases/R1/sprint-1.1/TASKS.md` — Tasks concluídas em S1.1
- `docs/releases/R1/sprint-1.1/DOR_GATES.md` — DoR atual (base para proposta)
- `docs/releases/R1/sprint-1.0/RETRO.md` — Retro S1.0
- `docs/releases/R1/sprint-1.0/PARECER_SM_D1.md` — Parecer SM anterior
- `docs/analysis/R1_PLAN_REVISED.md` — Plano R1 original
