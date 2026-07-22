# Sprint Planning — R1 Sprint 1 (Dupla Via)

**Data:** 2026-07-21
**Duracao:** 60min (Tech Lead Review)
**Participantes:** Jader (SME + Tech Lead + Dev)

---

## 1. APRESENTACAO — Tech Lead

### Estado Atual do Codigo (Auditado em 2026-07-21)

| Componente | LOC | Testes Dedicados | Cobertura Est. | Risco |
|------------|-----|------------------|----------------|-------|
| `agent_harness.py` | 787 | **ZERO** | ~50% (adventicia) | 🔴 |
| `capability_harness.py` | 800 | **ZERO** | ~50% (adventicia) | 🔴 |
| `ProjectAdapter` | 0 | N/A | N/A | 🔴 Novo |

### Diagnostico Arquitetural

**agent_harness.py (787 linhas):** Contem 4+ responsabilidades num arquivo so:
- Maquina de estados (AgentLifecycle com 6 estados, transicoes validas)
- Gerenciamento de sessoes (AgentRegistration, ExecutionControl)
- Observabilidade (TraceSpan, AgentDashboard)
- Residencia (CircuitBreakerConfig, IsolationConfig)

**capability_harness.py (800 linhas):** Mesmo problema:
- Execucao com schema/pre/pos/rollback
- Retry com backoff exponencial
- Chain de capabilities (ChainLink, ChainContext)
- Telemetria e resolucao de parametros

**Problema arquitetural identificado:** Ambos os modulos misturam **logica de dominio** com **infraestrutura** (logging, telemetria). Para testar Coverage ≥80%, PRECISAMOS refatorar em partes — nao da pra testar 1587 linhas monoliticas sem quebrar em modulos menores.

### Dupla Via: Verdadeiramente Paralela?

| Condicao | Track A (Harness Tests) | Track B (ProjectAdapter) |
|----------|------------------------|--------------------------|
| Depende de codigo novo? | Nao — codigo ja existe | Sim — criar do zero |
| Depende da outra track? | Nao | Nao |
| Bloqueio mutuo? | Nenhum | Nenhum |
| Risco de integracao? | Baixo — ja consome `apos.harness` | **Medio** — precisa rodar contra repositorio real |

**Veredito:** ✅ Paralelismo REAL. Track A escreve testes sobre codigo existente. Track B cria codigo novo. Zero dependencia. Mas ATENCAO: as tracks se encontram no Dia 3 — se o ProjectAdapter revelar que a arquitetura do harness nao suporta o caso de uso, paramos.

---

## 2. SPRINT GOAL

> **"Harness confiavel (coverage ≥80%) + ProjectAdapter prototipado contra Meu PDI real — entregue ate Dia 2 compilavel/testavel."**

Esta goal tem um **milestone critico**: Fim do Dia 2, ambos prototipos (testes do harness + discover() do ProjectAdapter) precisam compilar e rodar. Se ate Dia 2 um dos dois nao estiver verde, reavaliamos o escopo.

---

## 3. USER STORY

### US-R1S1: Dupla Via Operacional

**Como** Tech Lead APOS
**Quero** que o harness tenha coverage ≥80% E o ProjectAdapter consiga descobrir a stack de um repositorio real
**Para** validar que a arquitetura do APOS suporta o caso de uso do Meu PDI antes de investir mais 2 sprints

**Criterios de Aceitacao (RIGOROSOS):**

**Track A — Harness Coverage:**
- [ ] `agent_harness.py` — testes unitarios para: ciclo de vida completo (REGISTERED → READY → RUNNING → STOPPED), transicoes invalidas (RUNNING → REGISTERED), health check (HEALTHY/DEGRADED/UNHEALTHY), circuit breaker (abertura apos N falhas)
- [ ] `capability_harness.py` — testes unitarios para: execucao basica (success/error/timeout), retry com backoff (max_retries respeitado, base_delay aplicado), chain execution (ordem preservada, erro interrompe cadeia), rollback (chamado apos falha)
- [ ] Cobertura ≥80% para ambos (medido via `pytest --cov=apos.harness`)
- [ ] Zero testes flaky (determinismo verificado)

**Track B — ProjectAdapter Prototype:**
- [ ] `ProjectAdapter.discover()` implementado como classe em `apos/project_adapter/`
- [ ] Detecta `pyproject.toml` → extrai nome, versao, dependencias
- [ ] Detecta estrutura de diretorios (`src/`, `tests/`, `docs/`, `app/`)
- [ ] Identifica framework (FastAPI/Django/Flask via `pyproject.toml` OR `requirements.txt`)
- [ ] Roda contra repositorio **real** (Meu PDI em `/mnt/c/repo/meu-pdi/`)
- [ ] Retorna `ProjectDiscoveryResult` com: `stack`, `domain_hints`, `modules`, `confidence_score`

**Gate (Dia 2):**
- [ ] Ambos compilaveis: `python -c "from apos.harness import AgentHarness; from apos.project_adapter import ProjectAdapter"`
- [ ] Ambos testaveis: `pytest tests/harness/ -q` e `python -c "ProjectAdapter().discover('/tmp/test-repo')"`
- [ ] Se falhar, **paramos** e reavaliamos a arquitetura

---

## 4. RISCO — Analise do Tech Lead

### R1: Harness God Classes (Alta Probabilidade, Alto Impacto)

**Problema:** `agent_harness.py` (787 LOC) e `capability_harness.py` (800 LOC) sao god classes. Testar sem refatorar primeiro pode ser impossivel — metodos privados, acoplamento com logging/telemetria, estado interno complexo.

**Mitigacao:** Dia 1 comecar com extracao de modulos menores:
- `agent_lifecycle.py` — estados e transicoes (purificado)
- `agent_config.py` — dataclasses de configuracao
- `capability_execution.py` — schema, pre/pos, rollback
- `capability_chain.py` — ChainLink, ChainContext

**Plano B:** Se a extracao consumir >0.5 SP, aceitar coverage menor (≥70%) no Sprint 1 e completar no Sprint 2.

### R2: ProjectAdapter Discovery < 80% em Repositorio Real (Media Probabilidade, Alto Impacto)

**Problema:** Meu PDI tem estrutura complexa (monorepo? varios frameworks? configs aninhadas?). O prototype pode descobrir menos de 80%.

**Mitigacao:** Definir "80%" como: detecta pyproject.toml + estrutura de pastas + framework principal. Nao incluir deteccao de todas as dependecias. Prototipo funcional != discovery completo.

**Plano B:** Se descubrir < 50%, pivotar para `discover()` com fallback manual (CLI pergunta o que nao detectou).

### R3: Falso Paralelismo (Baixa Probabilidade, Impacto Critico)

**Problema:** As tracks sao paralelas AGORA, mas o Sprint 2 (Bootstrap Gate 2.0) depende de ProjectAdapter. Se o prototipo atrasar, o Sprint 2 inteiro atrasa.

**Mitigacao:** Isso e risco futuro, nao deste sprint. Para R1-Sprint-1, o paralelismo e real. Documentar o risco no plano de R1.

### R4: Coverage Medido Errado (Baixa Probabilidade, Impacto Medio)

**Problema:** Coverage "adventicia" de outros testes pode contaminar a medicao. Se outros modulos chamam o harness indiretamente, a cobertura parece maior do que realmente e.

**Mitigacao:** Usar `--cov=apos.harness --cov-report=term-missing` para isolar APENAS o modulo de harness. Documentar baseline ANTES de comecar.

---

## 5. PERGUNTA AO DEV

### Pergunta Unica (Decisiva para Arquitetura)

> **O `ProjectAdapter.discover()` precisa ser um scanner sincrono que le o filesystem, ou pode ser um conjunto de detectores modulares com plugin points para diferentes repositorios?**

**Contexto:** A decisao arquitetonica do ProjectAdapter determina se:
1. **Opcao A (Scanner Unico):** `discover()` implementa tudo internamente — le pyproject.toml, package.json, CLAUDE.md, estrutura de pastas. Simples de comecar, mas cada novo tipo de repositorio exige mudanca no core.
2. **Opcao B (Detectores Modulares):** `discover()` delega para `Detector` objs registrados (`PythonDetector`, `NodeDetector`, `GoDetector`). Cada detector sabe reconhecer sua stack. Mais complexo no inicio, mas escalavel.

**Recomendacao do Tech Lead:** **Opcao B (Detectores Modulares)** — mesmo que implementemos so `PythonDetector` no prototipo. A razao: se o prototipo precisar de 2+ detectores em R1.2, a migracao de A para B sera cara. Comecar modular desde o Dia 1 custa +0.5 SP agora, mas evita refactor caro depois.

**Perguntas ao Dev:**
1. Qual o modelo de dados do `discover()`? `ProjectDiscoveryResult` com `stack: list[str]`, `domain_hints: list[str]`, `confidence: float`?
2. Testes do harness: prefere refatorar primeiro (extrair modulos menores) ou testar os god classes como estao (com monkeypatch pesado)?
3. Confirmacao: o milestone do Dia 2 e ambos compilaveis+testaveis, nao necessariamente coverage ≥80% ainda — correto?

---

## DECISAO DO TECH LEAD

### Checklist de Aprovacao

| Criterio | Status | Nota |
|----------|--------|------|
| Dupla via e verdadeiramente paralela? | ✅ SIM | Zero dependencia entre tracks |
| Prototipo roda contra repositorio real? | ✅ SIM | Meu PDI em /mnt/c/repo/meu-pdi/ |
| Stop condition definida? | ✅ SIM | Dia 2 — ambos compilaveis+testaveis |
| Definition de "prototipo funcional"? | ✅ SIM | discover() basico + 2 detectores |
| Risco de god class enderecado? | ⚠️ PARCIAL | Mitigacao documentada, Plano B definido |
| Milestone Dia 2 claro? | ✅ SIM | Compilavel + testavel |

### Veredito Final

**APROVADO COM RESSALVAS.** A dupla via e arquiteturalmente solida — as tracks sao genuinamente paralelas e o stop condition do Dia 2 protege contra investimento cego. As ressaltas sao:

1. **Refatorar god classes primeiro** — nao tentar testar 1587 linhas monoliticas. Extrair `agent_lifecycle.py` e `capability_execution.py` no Dia 1.
2. **Detectores modulares** — comecar o ProjectAdapter com `PythonDetector` modular, nao scanner unico. Custa +0.5 SP agora, evita refactor caro depois.
3. **Coverage baseline** — rodar `pytest --cov=apos.harness --cov-report=term-missing` ANTES de qualquer mudanca para documentar o ponto de partida real.

| Track | SP | Tech Lead Confidence |
|-------|----|---------------------|
| Track A: Harness Coverage ≥80% | 2.0 | 🔶 70% (god class risk) |
| Track B: ProjectAdapter Prototype | 2.0 | ✅ 85% (escopo bem definido) |
| Buffer (refactor + imprevistos) | 0.5 | Necessario |
| **Total** | **4.5** | |

---

*Tech Lead: Jader (Hermes Agent)*
*Data: 2026-07-21*
*Review mode: Sprint Planning R1 Sprint 1 — Dupla Via*
