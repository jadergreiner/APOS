# Parecer de Produto — Discovery Tech Lead

**Data:** 2026-07-23
**Elaborado por:** Product Manager (Hermes Agent)
**Base:** `FINDINGS_TECH_LEAD.md` + `ENTREVISTA_TECH_LEAD.md` + `PARECER_TECNICO_TECH_LEAD.md`
**Status:** ✅ Consolidado com User Stories, DoR/DoD, Cenários de Teste e Priorização

---

## Sumário Executivo

A entrevista com Tech Lead validou **5 dores** com severidade entre Alta e Média. Sob a ótica de **Produto**, o problema se traduz em uma ineficiência sistêmica no ciclo de desenvolvimento com IA: **o contexto semântico do projeto se degrada a cada sprint, e não há mecanismo automático para detectar, prevenir ou recuperar esse desalinhamento.**

O custo não é apenas técnico — é um **custo de oportunidade de produto**: cada 20-30min gasto recuperando contexto é tempo que não vai para entender o usuário, validar hipóteses ou entregar valor.

| Dor | Frequência | Impacto no Usuário | Custo Semanal (time 4p) | Prioridade PM |
|-----|-----------|-------------------|----------------------|:------------:|
| **D01** — Contexto perdido entre sprints | Toda retomada de task | +20-30min overhead cognitivo | ~2h/sprint/pessoa | **P0** 🔴 |
| **D02** — Documentação desalinha do código | Contínuo (dias) | Agentes consomem docs obsoletas → retrabalho | 15% rework | **P0** 🔴 |
| **D03** — Contexto repetido em tasks de IA | Toda task delegada | 3-5 parágrafos boilerplate por task | ~30min/task | **P0** 🔴 |
| **D04** — Rastro de decisões espalhado | Pontual (consultas) | Dúvida sobre fonte da verdade | ~1h/consulta | **P1** 🟡 |
| **D05** — Stack assumptions erradas | Ocorrências documentadas | Propostas inválidas de implementação | ~2h/ocorrência | **P1** 🟡 |

---

## 1. Parecer de Produto — Qual Dor Atacar Primeiro

### 1.1 Análise de Valor de Negócio

A priorização de produto considera três dimensões:

1. **Frequência** — Quantas vezes o usuário sente a dor
2. **Severidade Percebida** — O quanto a dor atrapalha o fluxo de trabalho
3. **Custo de Oportunidade** — O que o time deixa de fazer por causa da dor

#### Gráfico de Priorização

```
Valor de Negócio (ROI estimado)
        ↑
    Alto │  D01 ●                D02 ●
        │  (ROI: 8x)             (ROI: 5x)
        │
    Médio│  D03 ●
        │  (ROI: 6x)
        │               D04 ●          D05 ●
    Baixo│               (ROI: 2x)     (ROI: 1.5x)
        │
        └────────────────────────────────────────→
           Baixa           Média          Alta
                          Complexidade Técnica
```

**Conclusão:** D01, D02 e D03 formam um cluster de alto valor com complexidade gerenciável. D04 é valioso mas complexo (depende de ADR padronizado). D05 tem valor incremental mais baixo.

### 1.2 Recomendação de Ordem de Ataque

| Ordem | Dor | Justificativa de Valor |
|:-----:|-----|----------------------|
| **1º** | **D01** | Impacto imediato na produtividade individual. Toda retomada de sprint economiza 20-30min. Visível em 1 sprint. |
| **2º** | **D03** | Elimina repetição manual em toda task de IA. ROI imediato na primeira task delegada. Depende de D01 (perfil populado). |
| **3º** | **D02** | Quebra o ciclo vicioso docs-obsoletas→retrabalho. Previne desalinhamento antes de acontecer. Depende de D01. |
| **4º** | **D04** | Rastreabilidade de decisões. Valoroso para auditoria, mas depende de ADR padronizado. |
| **5º** | **D05** | Stack validation. Solução parcial já existe (StackDetector). Ganho incremental menor. |

### 1.3 ROI Estimado

| Investimento | Retorno | Payback | Justificativa |
|-------------|---------|---------|---------------|
| **D01** — 2 SP | 8h/sprint recuperadas (4 pessoas) | **1 sprint** | 20min × 4 pessoas × 6 tasks/sprint = 8h |
| **D02** — 3 SP | 15% rework eliminado | **2 sprints** | 15% de 4 pessoas × 40h = 24h/sprint |
| **D03** — 2 SP | 3-5 parágrafos/task eliminados | **1 sprint** | 30min × 10 tasks/sprint = 5h |
| **D04** — 3 SP | Consulta única de decisões | **3 sprints** | Reduz dúvida de 1h → 2min |
| **D05** — 1 SP | Propostas inválidas eliminadas | **Imediato** | StackDetector já existe (80% coverage) |

---

## 2. User Stories

### US-D01: Cache de Contexto de Sprint

**Formato:** Como [persona]... Quero... Para...

> **Como** Tech Lead ou Dev retomando uma sprint após pausa,
> **Quero** que o APOS preserve e restaure automaticamente o contexto da sprint anterior (stack, módulos, decisões recentes, tarefas em andamento),
> **Para que** eu não precise gastar 20-30min relendo documentação e reconstruindo mentalmente o estado do projeto.

**Valor de Negócio:** 8/10 — Economia de 2h/pessoa/sprint. Baixa complexidade técnica.

**Story Points Estimados:** 2 SP

#### Definition of Ready (DoR)

- [ ] ProjectAdapter.discover() funcional e testado (retorna stack + módulos)
- [ ] ProjectProfile persistido em disco (JSON/YAML)
- [ ] Mecanismo de diff entre estado atual e último perfil salvo
- [ ] Critério claro do que é "contexto de sprint" (módulos tocados, tasks abertas, branches ativas)
- [ ] Time definiu quais informações compõem o "snapshot de sprint"
- [ ] Casos de uso de retomada documentados (mesma sprint, sprint nova, branch diferente)

#### Definition of Done (DoD)

- [ ] `apos/context/cache.py` implementado com `save_snapshot()` e `restore_snapshot()`
- [ ] Snapshot contém: módulos alterados, tasks ativas, branches, stack detectada
- [ ] `restore_snapshot()` retorna contexto em formato pronto para prompt de IA
- [ ] Preservação de snapshots por sprint (mínimo 3 últimos)
- [ ] Testes unitários com cobertura ≥90%
- [ ] Invalidação automática quando diff > 30% do projeto (mudança estrutural grande)
- [ ] Documentação de uso: `apos context save` / `apos context restore`
- [ ] Exemplo funcional no repositório

---

### US-D02: Validação Código vs Documentação

**Formato:** Como [persona]... Quero... Para...

> **Como** Tech Lead ou SME revisando tasks de IA,
> **Quero** que o APOS detecte automaticamente quando a documentação (ADRs, SDDs, READMEs) desalinha do código real,
> **Para que** agentes de IA nunca consumam contexto obsoleto e eu não descubra o desalinhamento depois do deploy.

**Valor de Negócio:** 7/10 — Elimina o ciclo docs-obsoletas→decisões-erradas→retrabalho.

**Story Points Estimados:** 3 SP

#### Definition of Ready (DoR)

- [ ] US-D01 concluída (ProjectProfile com estrutura do projeto)
- [ ] BootstrapGate operacional e exportável
- [ ] Mapeamento de quais docs têm correspondência no código (ex: ADR → arquivo tocado)
- [ ] Mecanismo de hash/checksum para detectar mudanças sem re-parsing completo
- [ ] Definido o que é "desalinhamento": data, hash, referência quebrada, schema desatualizado
- [ ] Regra de falsos positivos: parser de AST para confirmar divergências

#### Definition of Done (DoD)

- [ ] `apos/validation/doc_code_alignment.py` com `validate_alignment()`
- [ ] Algoritmo compara: data de modificação, hash de conteúdo, referências de arquivo
- [ ] Geração de relatório: quais docs desalinharam, desde quando, % de divergência
- [ ] Modo "silent" (apenas log) + modo "enforce" (bloqueia execução)
- [ ] Zero falsos positivos no modo enforce (validado por parser AST)
- [ ] Integração com BootstrapGate para validação pré-execução
- [ ] Testes com fixture de docs intencionalmente desalinhadas
- [ ] Cobertura ≥85%

---

### US-D03: Injeção Automática de Contexto

**Formato:** Como [persona]... Quero... Para...

> **Como** Dev ou Tech Lead delegando tasks para agentes de IA,
> **Quero** que o APOS injete automaticamente o contexto do projeto (stack, arquitetura, módulos, decisões recentes) no prompt de cada task delegada,
> **Para que** eu não precise escrever 3-5 parágrafos de contexto boilerplate por task e elimine inconsistências na comunicação de contexto.

**Valor de Negócio:** 7/10 — Elimina repetição em toda task IA. Melhora consistência do contexto.

**Story Points Estimados:** 2 SP

#### Definition of Ready (DoR)

- [ ] US-D01 concluída (ProjectProfile com contexto estruturado)
- [ ] Template de prompt definido pelo time (quais informações incluir)
- [ ] Mecanismo de middleware/decorator para injeção na task
- [ ] Estratégia de budget de tokens para cada seção do contexto
- [ ] Definição de quais tarefas recebem injeção automática (flags: full, minimal, none)

#### Definition of Done (DoD)

- [ ] `ContextInjector` como middleware/decorator `@inject_context(profile="minimal")`
- [ ] Template de contexto configurável (seções opcionais: stack, módulos, decisões, tasks)
- [ ] Budget de tokens configurável por seção
- [ ] Flag de consentimento: dev pode opt-out por task
- [ ] Testes com múltiplos perfis de projeto (Django, FastAPI, NestJS)
- [ ] Cobertura ≥85%

---

### US-D04: Rastreamento de Decisão (ADR → SDD → Código)

**Formato:** Como [persona]... Quero... Para...

> **Como** SME ou Tech Lead auditando decisões de arquitetura,
> **Quero** que o APOS trace automaticamente a cadeia ADR → SDD → Código,
> **Para que** eu saiba exatamente qual decisão motivou cada trecho de código e qual documento é a fonte da verdade.

**Valor de Negócio:** 5/10 — Resolve dúvida pontual mas tem dependência de padronização ADR.

**Story Points Estimados:** 3 SP

#### Definition of Ready (DoR)

- [ ] US-D01 concluída (ProjectProfile com estrutura de docs)
- [ ] Schema de ADR padronizado (ADR-XXX, campos obrigatórios)
- [ ] Mapeamento de naming conventions (ADR → SDD → código)
- [ ] Pelo menos 3 ADRs reais existentes no projeto para teste

#### Definition of Done (DoD)

- [ ] `apos/traceability/link.py` com `trace_decision(adr_id)` → cadeia completa
- [ ] Indexação de referências cruzadas: ADR → SDD → módulos → funções
- [ ] Query: "Quem decidiu isso?" → retorna decisão original + contexto
- [ ] Não criar ADR retroativamente — apenas rastrear decisões novas
- [ ] Relatório de "decisões órfãs" (código sem ADR)
- [ ] Cobertura ≥80%

---

### US-D05: Validação de Stack e Restrições

**Formato:** Como [persona]... Quero... Para...

> **Como** Tech Lead revisando propostas de agentes de IA,
> **Quero** que o APOS valide automaticamente se a stack assumida pela proposta é compatível com o projeto real,
> **Para que** agentes não gerem código assumindo PostgreSQL (quando usamos DynamoDB) ou Redis (quando usamos SQS).

**Valor de Negócio:** 4/10 — Problema real mas solução parcial já existe.

**Story Points Estimados:** 1 SP

#### Definition of Ready (DoR)

- [ ] StackDetector existente com cobertura ≥80%
- [ ] Lista de stacks confirmadas do projeto (DynamoDB, SQS, Cognito, etc.)
- [ ] Definição de "non-stack" (o que o projeto NÃO usa)

#### Definition of Done (DoD)

- [ ] StackDetector enriquecido com detecção de serviços AWS adicionais
- [ ] Alerta de "non-stack" emitido quando proposta assume tecnologia fora do perfil
- [ ] Integração com ContextInjector para incluir restrições de stack
- [ ] Testes com cenários de erro: agente assume Redis → alerta
- [ ] Cobertura ≥90%

---

## 3. Matriz de Dependências

```
US-D01 (Cache de Contexto) ───────────────┐
    (ProjectProfile, persistência)         │
                                           ├── US-D03 (Injeção Automática)
US-D02 (Validação Docs vs Código) ─────────┤    (perfil populado)
    (ProjectProfile + BootstrapGate)       │
                                           └── US-D04 (Rastreamento Decisão)
US-D05 (Stack Validation) ─────────────────┘    (perfil + docs indexados)
    (StackDetector existente)
```

**Dependências técnicas:**
- US-D02 depende de US-D01 (precisa de ProjectProfile)
- US-D03 depende de US-D01 (precisa de perfil populado)
- US-D04 depende de US-D01 (precisa de estrutura de docs) + padronização ADR
- US-D05 é independente (só enriquecer StackDetector)

---

## 4. Cenários de Teste

### 4.1 US-D01: Cache de Contexto

#### Funcionais

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC01 | Salvar snapshot | `save_snapshot(sprint="R1.2")` | Arquivo persistido com módulos, tasks, branches |
| TC02 | Restaurar snapshot | `restore_snapshot(sprint="R1.2")` | Retorna contexto formatado para prompt IA |
| TC03 | Múltiplos snapshots | 3 snapshots de sprints diferentes | Lista ou recupera qualquer um |
| TC04 | Atualizar snapshot | Mudar 1 módulo, salvar de novo | Diff registrado, versão anterior preservada |

#### Edge Cases

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC05 | Snapshot inexistente | `restore_snapshot(sprint="R99")` | Erro amigável + sugestão de sprints disponíveis |
| TC06 | Projeto mudou drasticamente | +50% novos módulos | Snapshot marcado como "stale", alerta ao usuário |
| TC07 | Snapshot corrompido | Arquivo JSON inválido | Fallback: recria snapshot do zero com warning |
| TC08 | Concorrência | 2 snapshots salvos simultaneamente | Lock de arquivo, sem perda de dados |

### 4.2 US-D02: Validação Código vs Docs

#### Funcionais

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC09 | Docs OK | ADR-009, código correspondente sem alterações | ✅ PASS |
| TC10 | Doc desatualizada | ADR-009, código foi alterado há 3 dias | ❌ FAIL + relatório de divergência |
| TC11 | Doc removida | README.md deletado mas referenciado | ❌ Referência quebrada detectada |

#### Edge Cases

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC12 | Falso positivo evitar | Renomeação de função (AST diferente, semântica igual) | ⚠️ WARNING apenas, não FAIL |
| TC13 | Doc recém-criada | ADR criada há 5 minutos | ✅ Ignorar (janela de tolerância) |
| TC14 | Documentação auto-gerada | `pydoc` ou `sphinx` | Auto-docs excluídas da verificação |
| TC15 | Projeto sem docs | `validate_alignment()` em repo vazio | ✅ PASS sem alertas |

### 4.3 US-D03: Injeção Automática

#### Funcionais

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC16 | Injeção full | `@inject_context(profile="full")` | Prompt com stack + módulos + decisões + tasks |
| TC17 | Injeção minimal | `@inject_context(profile="minimal")` | Apenas stack + módulos ativos |
| TC18 | Opt-out | `@inject_context(profile="none")` | Nenhum contexto injetado |

#### Edge Cases

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC19 | Token budget excedido | Contexto de projeto gigante >8K tokens | Truncagem inteligente por prioridade |
| TC20 | Perfil vazio | `restore_snapshot()` retorna vazio | Template minimal com fallback |
| TC21 | Projeto não-APOS | `inject_context()` sem bootstrapping | Erro: "Execute `apos init` primeiro" |
| TC22 | Contexto sensível | Decisão marcada como `confidential: true` | Excluída da injeção automática |

### 4.4 US-D04: Rastreamento de Decisão

#### Funcionais

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC23 | Trace completo | `trace_decision("ADR-012")` | ADR-012 → SDD-0006 → módulo `auth/` → função `login()` |
| TC24 | Decisão sem código | ADR recém-criada, sem implementação | ✅ ADR encontrada, sem correspondência de código |
| TC25 | Decisões órfãs | `trace_orphans()` | Lista de código sem ADR associado |

#### Edge Cases

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC26 | ADR inexistente | `trace_decision("ADR-999")` | ❌ "ADR não encontrada" + sugestão de ADRs próximas |
| TC27 | Referência circular | ADR-A → SDD-X → ADR-A | ❌ Detectado loop, truncado |
| TC28 | Múltiplas fontes | Módulo referenciado por 2 ADRs | ✅ Lista ambas com data e contexto |

### 4.5 US-D05: Stack Validation

#### Funcionais

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC29 | Stack compatível | Proposta usa DynamoDB, projeto usa DynamoDB | ✅ PASS |
| TC30 | Stack incompatível | Proposta assume Redis, projeto usa SQS | ❌ Alerta "Redis não faz parte da stack" |
| TC31 | Nova stack detectada | Projeto agora usa EventBridge | ✅ Adicionado ao perfil |

#### Edge Cases

| # | Cenário | Entrada | Resultado Esperado |
|---|---------|---------|-------------------|
| TC32 | Serviço não-determinado | `StackDetector.describe()` retorna incerto | ⚠️ WARNING "stack não confirmada" |
| TC33 | Multi-service ambíguo | Projeto usa DynamoDB + PostgreSQL | ✅ Ambos listados, alerta apenas para não-listados |
| TC34 | Stack detector offline | `StackDetector` não disponível | Fallback para configuração manual |

---

## 5. Priorização — Qual US Entrega Mais Valor Primeiro

### Score de Priorização

Fórmula: **Valor = (Frequência × Impacto × Confiança) / (Complexidade × Risco × Dependência)**

| US | Frequência | Impacto | Confiança | Complexidade | Risco | Dependência | **Score** |
|:--:|:----------:|:-------:|:---------:|:------------:|:-----:|:-----------:|:---------:|
| US-D01 | 5/5 | 4/5 | 5/5 | 2/5 | 2/5 | 1/5 | **25.0** |
| US-D03 | 5/5 | 4/5 | 4/5 | 2/5 | 2/5 | 3/5 | **13.3** |
| US-D02 | 4/5 | 5/5 | 4/5 | 3/5 | 3/5 | 3/5 | **5.9** |
| US-D05 | 3/5 | 3/5 | 4/5 | 1/5 | 1/5 | 1/5 | **36.0** |
| US-D04 | 2/5 | 4/5 | 3/5 | 3/5 | 3/5 | 4/5 | **1.3** |

> **Nota:** US-D05 tem score alto por ser simples e independente, mas o valor absoluto é menor (4/10). Priorizamos por impacto no ciclo de desenvolvimento, não só por facilidade.

### Ordem de Implementação Recomendada

```
Sprint 1: US-D01 (Cache) + US-D05 (Stack Validation)
Sprint 2: US-D03 (Injeção Automática) — depende de D01
Sprint 3: US-D02 (Validação Docs vs Código) — depende de D01
Sprint 4: US-D04 (Rastreamento Decisão) — depende de ADR + D01
```

**Justificativa:**
- US-D01 primeiro porque é a base para D02 e D03
- US-D05 é independente e cabe como "spillover" — enriquecimento rápido
- US-D03 vem antes de D02 porque gera valor imediato (elimina boilerplate) com menos risco técnico
- US-D02 é o maior ganho de qualidade mas tem mais risco de falso positivo — merece maturação
- US-D04 é o mais complexo e depende de padronização ADR — naturalmente mais tarde

---

## 6. Recomendação de Sprint

### Contexto Atual

| Release/Sprint | Status | Foco |
|---------------|--------|------|
| R0 | ✅ FECHADO | Fundações estratégicas |
| R1 Sprint 1.0 | 🚀 EM EXECUÇÃO (2026-07-22 a 26) | Harness + ProjectAdapter protótipo |
| R1 Sprint 1.1 | 📋 Planejado | Pós-gate D2 — continuação |

### Recomendação: R1.2 (não backlog)

**Decisão:** As 3 US de maior valor (D01, D02, D03) devem ser **contratadas na R1.2**, não postergadas para backlog.

**Racional:**

| Fator | Análise | Score |
|-------|---------|:-----:|
| **Urgência** | D01 já custa ~8h/pessoa/sprint. Atraso de 1 sprint = +8h de desperdício | 🔴 Alta |
| **Maturidade** | ProjectAdapter já existe e está sendo testado em R1 Sprint 1.0 | 🟢 Alta |
| **Dependências** | D01 é independente; D02 e D03 dependem de D01 — natural pipeline | 🟢 Favorável |
| **Capacidade** | 5 SP estimados (D01: 2SP + D03: 2SP + D05: 1SP) — cabem em 1 sprint | 🟢 Viável |
| **Setup zero** | Condição validada na entrevista. ProjectAdapter + CLI prontos | 🟢 OK |
| **ROI** | Payback em 1-2 sprints | 🟢 Atraente |

### Plano de Sprints Recomendado

#### R1 Sprint 1.1 (Atual + extensão — ProjectAdapter Core)

```
ProjectAdapter.discover() funcional         [3 SP] ✅ JÁ EM ANDAMENTO
├── Descoberta de stack, módulos, docs
├── Persistência de Profile (JSON/YAML)
└── Testes ≥80% cobertura
```

#### R1 Sprint 1.2 (Context Cache + Stack Validation)

```
US-D01: Cache de Contexto de Sprint         [2 SP] ← PRIORIDADE MÁXIMA
├── save_snapshot() / restore_snapshot()
├── Snapshot mínimo: módulos, tasks, branches
└── Contexto formatado para prompt IA

US-D05: Stack Validation                    [1 SP]
├── Enriquecer StackDetector
└── Alerta de "non-stack" em propostas
```

#### R1 Sprint 1.3 (Injeção de Contexto + Validação Docs)

```
US-D03: Injeção Automática de Contexto       [2 SP]
├── ContextInjector middleware
├── Templates de prompt configuráveis
└── Budget de tokens por seção

US-D02: Validação Código vs Docs             [3 SP]
├── validate_alignment()
├── Parser AST para evitar falsos positivos
└── Integração com BootstrapGate
```

#### R1 Sprint 2.0+ (Rastreamento de Decisão)

```
US-D04: Rastreamento ADR → SDD → Código     [3 SP]
├── Padronização de schema ADR
├── trace_decision() / trace_orphans()
└── Indexação de referências cruzadas
```

### Mapa Visual

```
Sprint 1.0     Sprint 1.1     Sprint 1.2         Sprint 1.3         R2+
──────────     ──────────     ──────────         ──────────         ───
Harness    →   ProjectAdapter → US-D01 (Cache) → US-D03 (Inject) → US-D04 (Trace)
Coverage   →   Core        →   US-D05 (Stack) → US-D02 (Validate)
                [AGORA]        [PRÓXIMO]         [SEQUÊNCIA]        [FUTURO]
```

### Riscos da Recomendação

| Risco | Probabilidade | Impacto | Mitigação |
|-------|:-----------:|:-------:|-----------|
| ProjectAdapter discovery <80% | Média | Alto | Ter fallback de mapeamento manual |
| US-D01 aumenta complexidade do perfil | Baixa | Médio | Snapshot mínimo para MVP |
| US-D02 falsos positivos iniciais | Média | Alto | Modo "silent" como default, modo enforce só após validação |
| Sprint 1.2 superlotado | Baixa | Médio | Mover US-D05 para Sprint 1.1 (spillover) |

---

## 7. Métricas de Sucesso por US

| US | Métrica | Baseline | Target | Prazo | Como Medir |
|:--:|---------|:--------:|:------:|:-----:|-----------|
| D01 | Tempo de retomada de sprint | 20-30 min | <5 min | 1 sprint | Time tracking |
| D02 | % tasks com docs desalinhadas | ~30% atual | <5% | 3 sprints | Relatório alignment |
| D03 | Caracteres de boilerplate/task | 500-1000 | <50 | 1 task | Média por task |
| D04 | Tempo para encontrar decisão original | 1h+ | <5min | 1 sprint | Teste cego |
| D05 | % propostas com stack errada | ~10% | <1% | 1 sprint | StackDetector log |

---

## 8. Resumo da Recomendação Final

**Ação imediata:**
Incluir US-D01 (Cache de Contexto) e US-D05 (Stack Validation) como **compromisso da R1.2**, amarrando-as ao sprint que sucede a R1 Sprint 1.0.

**Pipeline completo sugerido:**

| Sprint | US | SP | ROI Esperado |
|--------|:--:|:--:|:-----------:|
| R1.2 | US-D01 (Cache) + US-D05 (Stack) | 3 SP | 8h/sprint recuperadas |
| R1.3 | US-D03 (Inject) + US-D02 (Validate) | 5 SP | Boilerplate eliminado + rework -15% |
| R2.0 | US-D04 (Trace) | 3 SP | Rastreabilidade completa |

**Impacto total estimado no time de 4 pessoas:**
- **Horas recuperadas/sprint:** ~10-12h (D01 + D03)
- **Redução de retrabalho:** ~15% (D02)
- **Propostas inválidas eliminadas:** ~10% (D05)
- **Tempo de auditoria de decisões:** de 1h → 5min (D04)

**Validação final:** A sequência proposta respeita a regra de **setup zero** (condição sine qua non), ataca primeiro a dor de maior frequência (D01), constrói base para as demais, e entrega ROI visível em 1 sprint.

---

**Documento gerado por:** Hermes Agent — Product Manager Analysis
**Baseado em:** Entrevista Tech Lead (FINDINGS_TECH_LEAD.md) + Parecer Técnico (PARECER_TECNICO_TECH_LEAD.md)
**Status:** ✅ Finalizado — pronto para validação da Tríade (PM + Tech Lead + SME)
