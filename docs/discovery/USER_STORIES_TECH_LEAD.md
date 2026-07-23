# User Stories — Discovery Tech Lead (R0-AC04)

**Data:** 2026-07-23  
**Base:** `FINDINGS_TECH_LEAD.md` | `PARECER_TECNICO_TECH_LEAD.md`  
**Total:** 5 User Stories (3 P0 → R1.2, 2 P1 → R1.3)

---

## Sprint R1.2 — P0 Obrigatório

---

### US-001: Cache de Perfil de Projeto com Detecção de Mudanças

**Como** Tech Lead  
**Quero** que o perfil do projeto descoberto pelo ProjectAdapter seja armazenado em cache e reutilizado entre sprints  
**Para** eliminar os 20-30min de retomada de contexto manual a cada sprint

**DoR (Definition of Ready):**
- [ ] ProjectAdapter.discover() implementado e testado com Meu PDI real
- [ ] ProjectProfile schema congelado (sem breaking changes pendentes)
- [ ] Discussão técnica sobre formato de cache (JSON vs pickle vs SQLite)
- [ ] Path do cache decidido (`.apos/cache/profile.json` ou similar)
- [ ] Hash de estado do projeto (checksum de arquivos-chave) aprovado

**DoD (Definition of Done):**
- [ ] `apos/core/profile_cache.py` implementado com classe `ProfileCache`
- [ ] `ProfileCache.get_or_discover(project_root) -> ProjectProfile` — retorna cache se válido, redescobre se expirado
- [ ] Hash de invalidação: checksum combinado de `pyproject.toml`, `setup.py`, `requirements.txt`, estrutura de diretórios (`__init__.py` count, módulos top-level)
- [ ] Cache é invalidado automaticamente quando qualquer arquivo monitorado muda
- [ ] Fallback: cache corrompido → rediscovery silenciosa com log warning
- [ ] Setup zero: nenhuma configuração manual necessária para ativar cache
- [ ] Testes unitários: ≥90% de cobertura no módulo
- [ ] Cache persiste entre sessões (serializado em disco sob `.apos/cache/`)
- [ ] Documentação em `docs/discovery/PROFILE_CACHE.md`
- [ ] US-001 não quebra testes existentes do ProjectAdapter

**Cenários:**

| CT | Tipo | Descrição | Resultado Esperado |
|----|------|-----------|-------------------|
| CT01 | Happy Path | Descobrir perfil, cachear, rediscovery em nova sessão sem mudanças | Retorna cache sem reexecutar detectores |
| CT02 | Happy Path | Descobrir perfil, modificar `pyproject.toml`, rediscovery | Invalida cache → rediscovery executada |
| CT03 | Edge | Cache corrompido (JSON malformado) | Fallback silencioso para rediscovery, log warning |
| CT04 | Edge | Projeto nunca descoberto antes | Cache vazio → discover() normal |
| CT05 | Race | Múltiplas chamadas simultâneas | Apenas 1 discovery executada, demais aguardam e pegam cache |
| CT06 | Edge | PermissionError no diretório de cache | Fallback para cache em memória (session-only), log |
| CT07 | Performance | Projeto com 10.000+ arquivos | Discovery + save cache < 30s |
| CT08 | Performance | Cache hit | Retorno em < 100ms |

**Prioridade:** Alta  
**Sprint:** R1.2  
**Esforço estimado:** 2.0 SP  
**Depende de:** ProjectAdapter (entregue na Sprint 1.0)

---

### US-002: Validação Código vs Documentação

**Como** Tech Lead  
**Quero** que o APOS detecte automaticamente quando a documentação desalinha do código real  
**Para** evitar que agentes de IA tomem decisões baseadas em documentação obsoleta

**DoR (Definition of Ready):**
- [ ] US-001 entregue (ProfileCache como baseline)
- [ ] Definição de quais artefatos comparar (docs/SDD/*.md vs apos/*.py)
- [ ] Estratégia de parsing definida (AST vs regex vs markdown headers)
- [ ] Tolerância a falso positivo definida (critério: 0 falso positivo nas primeiras 10 execuções)
- [ ] Schema de relatório de divergência aprovado

**DoD (Definition of Done):**
- [ ] Módulo `apos/validation/schema_validator.py` com classe `SchemaValidator`
- [ ] `validate(profile: ProjectProfile, docs_path: Path) -> ValidationReport` implementado
- [ ] Comparação: entidades do `SemanticDetector` vs entidades referenciadas em SDDs
- [ ] Comparação: stack declarada vs stack implícita em docs de arquitetura
- [ ] Zero falsos positivos no report — toda divergência é código real vs doc real
- [ ] `ValidationReport` com: total_checks, passed, failed, warnings, detalhes por item
- [ ] Relatório exportável em JSON para consumo por agentes
- [ ] Setup zero: executa automaticamente no discover() quando docs/SDD existe
- [ ] Testes: ≥85% coverage, incluindo mock de docs divergentes
- [ ] Integração: BootstrapGate pode consumir ValidationReport como métrica de "saúde"

**Cenários:**

| CT | Tipo | Descrição | Resultado Esperado |
|----|------|-----------|-------------------|
| CT01 | Happy Path | Código e SDDs perfeitamente alinhados | 100% passed, 0 failed, 0 warnings |
| CT02 | Happy Path | Entidade removida do código mas ainda documentada | 1 failed com detalhe "Entity X not found in source" |
| CT03 | Happy Path | Stack mudou (ex: migrou de DynamoDB para PostgreSQL) mas docs não | 1 failed: "Database mismatch: code=DynamoDB, doc=PostgreSQL" |
| CT04 | Edge | Projeto sem docs/SDD | Warnings, não erros — relatório vazio com nota |
| CT05 | Edge | SDD com erros de markdown (quebra de parsing) | Warning de parsing, não bloqueia outras validações |
| CT06 | Edge | Falso positivo induzido por naming diferente (ex: `User` vs `user_model`) | Heurística de similaridade >80% não reporta como falha |
| CT07 | Regression | Executar validação sem ProfileCache | Fallback: execute discover() completo primeiro |
| CT08 | Smoke | Validar Meu PDI real (3.400 arquivos, 50 SDDs) | Completa em <60s |

**Prioridade:** Alta  
**Sprint:** R1.2  
**Esforço estimado:** 3.0 SP  
**Depende de:** US-001, ProjectAdapter

---

### US-003: Injeção Automática de Contexto para Agentes

**Como** Tech Lead  
**Quero** que o contexto do projeto (stack, módulos, decisões ativas) seja injetado automaticamente em toda task delegada a agentes de IA  
**Para** eliminar a repetição manual de 3-5 parágrafos de contexto por task

**DoR (Definition of Ready):**
- [ ] US-001 entregue (ProfileCache como fonte de contexto)
- [ ] Harness/Hermes middleware extension point identificado
- [ ] Template de contexto aprovado (formato markdown, quais campos incluir)
- [ ] Decisão sobre momento de injeção (pré-prompt vs system prompt vs decorator)

**DoD (Definition of Done):**
- [ ] `apos/context_injector.py` com classe `ContextInjector`
- [ ] `inject(profile: ProjectProfile, task_prompt: str) -> str` — enriquece prompt com contexto estruturado
- [ ] Template de contexto inclui: stack, módulos core, padrões arquiteturais, entidades de domínio, ADRs ativos
- [ ] Modo "dry-run": mostra o contexto que seria injetado sem modificar o prompt
- [ ] Setup zero: ContextInjector é ativado por default se ProjectProfile disponível
- [ ] Chave `APOS_CONTEXT_INJECTOR=false` permite desligar seletivamente
- [ ] Compatibilidade: funciona com Harness sem quebrar testes existentes
- [ ] Testes: ≥85% coverage, testando override por env var
- [ ] Contexto nunca excede 2000 tokens (trunca se necessário com warning)

**Cenários:**

| CT | Tipo | Descrição | Resultado Esperado |
|----|------|-----------|-------------------|
| CT01 | Happy Path | Prompt vazio + profile disponível | Contexto completo injetado no início do prompt |
| CT02 | Happy Path | Prompt já contém stack info manual | ContextInjector deduplica, não duplica |
| CT03 | Edge | `APOS_CONTEXT_INJECTOR=false` | Prompt original retornado sem modificação |
| CT04 | Edge | Profile indisponível (erro no cache) | Prompt original passa sem injeção, log warning |
| CT05 | Edge | Contexto gerado >2000 tokens | Trunca mantendo stack + módulos core, log truncation |
| CT06 | Performance | Injeção em prompt de 10KB | Processamento < 50ms |
| CT07 | Integration | Prompt + injeção → delegado Harness | Task executa sem erro, contexto aparece no log |

**Prioridade:** Alta  
**Sprint:** R1.2  
**Esforço estimado:** 1.5 SP  
**Depende de:** US-001

---

## Sprint R1.3 — P1 Desejável

---

### US-004: Rastreamento de Decisões ADR → SDD → Código

**Como** Tech Lead  
**Quero** que o APOS rastreie a cadeia de decisões desde o ADR até o código implementado  
**Para** saber qual documento é a fonte da verdade quando uma decisão está documentada em múltiplos lugares

**DoR (Definition of Ready):**
- [ ] Padrão de ADR definido no repositório (formato, localização)
- [ ] Pelo menos 1 ADR existente para usar como caso de teste
- [ ] Mapeamento de referências entre SDDs e código existente
- [ ] Schema de TraceLink aprovado

**DoD (Definition of Done):**
- [ ] Módulo `apos/traceability/tracer.py` com classe `DecisionTracer`
- [ ] `TraceLink` model: source (ADR|SDD|código), target, relationship_type, confidence, timestamp
- [ ] `trace(adr_path: Path) -> list[TraceLink]` — mapeia um ADR para SDDs e código impactado
- [ ] Indexador de referências: varre SDDs e docs por menções a ADRs, classes, módulos
- [ ] `get_decision_chain(entity_name: str) -> list[TraceLink]` — retorna cadeia reversa de decisões
- [ ] Relatório markdown: "Decision Trail for {entity}" com links para cada artefato
- [ ] Setup zero: funciona com docs existentes (não exige reescrita retroativa)
- [ ] Tratamento de ambiguidade: se mesma decisão em 2 ADRs, marca prioridade (mais recente vence)
- [ ] Testes: ≥80% coverage

**Cenários:**

| CT | Tipo | Descrição | Resultado Esperado |
|----|------|-----------|-------------------|
| CT01 | Happy Path | ADR-009 → SDD correspondente → classe implementada | Cadeia completa com 3 links |
| CT02 | Happy Path | Entity User referenciada em 3 SDDs + 2 classes | 5 TraceLinks retornados |
| CT03 | Edge | Decisão em ADR sem código implementado | Warning "ADR-XXX: no code implementation found" |
| CT04 | Edge | ADR revogado por ADR mais recente | Ambos retornados, prioridade no mais recente |
| CT05 | Edge | Entidade sem nenhuma decisão registrada | Lista vazia, log info |
| CT06 | Performance | Indexar repositório com 50 SDDs + 20 ADRs | Completo em <30s |

**Prioridade:** Média  
**Sprint:** R1.3  
**Esforço estimado:** 3.0 SP  
**Depende de:** US-002 (validação ativa)

---

### US-005: Validação de Stack com Alerta de Non-Standard

**Como** Tech Lead  
**Quero** que o APOS alerte automaticamente quando um agente propõe algo fora da stack do projeto  
**Para** evitar propostas inválidas (ex: sugerir Redis num projeto DynamoDB)

**DoR (Definition of Ready):**
- [ ] StackDetector enriquecido com mais heurísticas de serviços AWS
- [ ] Lista de "stack allowlist" por projeto definida
- [ ] Integração ponto com Harness ou ContextInjector definida

**DoD (Definition of Done):**
- [ ] StackDetector expandido: detecta Lambda Layers, EventBridge, SQS, SNS, Step Functions
- [ ] `allowed_services: list[str]` e `blocked_services: list[str]` no ProjectProfile
- [ ] `validate_proposal(tools: list[str], profile: ProjectProfile) -> ValidationResult` em `apos/validation/stack_validator.py`
- [ ] Alerta por warning estruturado (não bloqueio) — "non-stack tool detected"
- [ ] Permite override via config: `allowed_services_extra: [Redis, PostgreSQL]`
- [ ] Sugestão automática: quando tool non-stack detectada, sugere alternativa da stack
- [ ] Testes: ≥85% coverage

**Cenários:**

| CT | Tipo | Descrição | Resultado Esperado |
|----|------|-----------|-------------------|
| CT01 | Happy Path | Agente propõe Lambda + DynamoDB (na stack) | Validação passa |
| CT02 | Happy Path | Agente propõe PostgreSQL (fora da stack) | Warning "Non-stack: PostgreSQL. Stack usa DynamoDB" |
| CT03 | Edge | Agente propõe Redis com override configurado | Passa com nota "allowed via override" |
| CT04 | Edge | Stack não detectada (all unknown) | Warn genérico, não bloqueia |
| CT05 | Edge | Múltiplos non-stack tools no mesmo proposal | 1 warning agregado, não 1 por tool |
| CT06 | Performance | Validar proposta com 20 ferramentas | < 10ms |

**Prioridade:** Média  
**Sprint:** R1.3  
**Esforço estimado:** 1.5 SP  
**Depende de:** US-001 (perfil populado)
