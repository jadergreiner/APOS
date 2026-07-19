# Sprint 0.0: Tarefas

**CRÍTICO:** Sprint 0.0 não é só Descoberta de JTBD. É implementação de **3 componentes core**:
1. **Framework de Gerenciamento de Release** (T0.0.1)
2. **Bootstrap Gate + Sessão de Definição de Fundações** (T0.0.2-T0.0.3)
3. **Auto-Identificação APOS** (T0.0.4)

---

## T0.0.1: Implementar Framework de Gerenciamento de Release (1 dia-pessoa)

**Objetivo:** Criar artefatos de Gerenciamento de Release que todo projeto que importa APOS recebe

**Tarefas:**
- [ ] Criar `docs/releases/R0/SPRINT_PLAN.md` (10 sprints estruturados)
- [ ] Criar `docs/releases/R0/BACKLOG.md` (itens priorizados P0-P3)
- [ ] Criar `docs/releases/R0/DEPENDENCY_MAP.md` (dependências, caminho crítico)
- [ ] Criar estrutura `sprint-X/` (README, TASKS, USER_STORIES, BOARD, STATUS, RISK_MITIGATION, RETRO)
- [ ] Validar que o framework é operacional e pronto para execução

**Entregável:** `Framework de Gerenciamento de Release (templates + docs)`

**Responsável:** PM / Skill de Gerenciamento de Release  
**Esforço:** 1 dia  
**Status:** ✅ **COMPLETO** (Pre-sprint, 19 jul)  
**Commit:** `[Framework já estava em lugar — scaffolding docs/releases/R0/`]

---

## T0.0.2: Implementar Bootstrap Gate + Sessão de Definição de Fundações (2 dias-pessoa)

**Objetivo:** Criar validador automático que detecta gaps de fundação e inicia sessão de definição

**Tarefas:**
- [ ] Implementar `apos.bootstrap_gate.validate()` — checa existência de 10 itens obrigatórios
- [ ] Implementar `apos.bootstrap_gate.initialize_foundation_session()` — auto-gera templates + guias
- [ ] Criar templates auto-gerados (NORTH_STAR.md, OKR.md, ONTOLOGY.md, etc)
- [ ] Documentar regras de validação em `BOOTSTRAP_GATE.md`
- [ ] Testar fluxo: detecção de gaps → geração de templates → inicialização de sessão

**Entregáveis:**

- ✅ `BOOTSTRAP_GATE.md` (especificação)
- ✅ `apos/bootstrap/gate.py` (implementação com validate_with_details + template generation)
- ✅ `apos/bootstrap/validators/strategy_validator.py` (85% coverage)
- ✅ `apos/bootstrap/validators/ontology_validator.py` (84% coverage)
- ✅ `apos/bootstrap/validators/governance_validator.py` (82% coverage)
- ✅ `apos/bootstrap/templates/generator.py` (10 templates auto-gerados)
- ✅ `tests/test_bootstrap.py` (35 testes, 81% cobertura)

**Responsável:** Engenharia de Framework  
**Esforço:** 2 dias planejados / 1 dia real (+100% velocity)  
**Status:** ✅ **COMPLETO** (19 jul)  
**Commit:** `f152801` — feat: implement Bootstrap Gate with real semantic validation (T0.0.2)

---

## T0.0.3: Implementar Auto-Identificação APOS + Gerenciamento de Sessão (1 dia-pessoa)

**Objetivo:** Projeto que importa APOS sabe que É um projeto APOS e pode iniciar sessão

**Tarefas:**
- [ ] Criar `apos.__init__.py` com metadata `apos_project`
- [ ] Implementar `apos.SessionManager.initialize()` — gerencia sessão de definição de fundações
- [ ] Criar CLI: `python -m apos init` — inicia setup de novo projeto
- [ ] Implementar detecção: projeto reconhece "Inicie uma sessão com APOS"
- [ ] Criar exemplo: `apos.SessionManager().run()` → conduz usuário através de JTBD → Strategy → Ontology

**Fluxo:**
```
$ python -m apos init

Inicialização de Projeto APOS
=============================

Detectando status das fundações...

✅ Verificação: NORTH_STAR.md
✅ Verificação: OKR.md
✅ Verificação: PURPOSE.md
...

GAPS DETECTADOS:
❌ ONTOLOGY.md (faltando)
❌ SEMANTIC_LAYER.md (faltando)
❌ GOVERNANCE.md (faltando)

Iniciando Sessão de Definição de Fundações...
(Conduzindo usuário através de JTBD → Strategy → Ontology)
```

**Entregáveis:**
- `apos/__init__.py` (metadata + imports)
- `apos/bootstrap/session.py` (SessionManager)
- `apos/__main__.py` (CLI: `python -m apos init`)
- Documentação em `BOOTSTRAP_GATE.md`

**Responsável:** Engenharia de Framework  
**Esforço:** 1 dia  
**Status:** DEFINIDO

---

## T0.0.A: Conduzir Entrevistas JTBD (2 dias-pessoa)

**Objetivo:** Entrevistar 5+ personas para entender o job que APOS resolve

**Tarefas:**

- [ ] Preparar kit de entrevista (cenários, perguntas, termo de consentimento)
- [ ] Agendar 5+ entrevistas (alvo: PM, agente, personas stakeholder)
- [ ] Conduzir entrevistas (2-3 por dia)
- [ ] Gravar/transcrever anotações
- [ ] Documentar insights brutos

**Entrevistas a Conduzir:**

1. Product Manager (líder de time) — foco em overhead de alinhamento
2. Agente de IA (conceitual) — foco em necessidades de contexto
3. CTO/Arquiteto — foco em viabilidade técnica
4. Stakeholder (negócios) — foco em ROI/valor
5. Adicional (time early adopter) — foco em adoção

**Entregável:** `JTBD-INTERVIEWS-RAW-NOTES.md`

**Responsável:** PM
**Esforço:** 2 dias
**Status:** Planejado

---

## T0.0.B: Mapear Forças de Progresso (1 dia-pessoa)

**Objetivo:** Analisar Push/Pull/Ansiedade/Hábito para cada persona

**Tarefas:**

- [ ] Revisar anotações de entrevista
- [ ] Extrair sinais de Push (frustração, dor, workarounds atuais)
- [ ] Extrair sinais de Pull (atração por APOS, resultado desejado)
- [ ] Extrair sinais de Ansiedade (medos, preocupações, riscos)
- [ ] Extrair sinais de Hábito (padrões atuais, inércia)
- [ ] Criar matriz de forças

**Framework:**

```
Para cada persona:
  Push: O que os frustra? Qual é a dor atual?
  Pull: O que os excita sobre APOS?
  Ansiedade: Do que eles se preocupam?
  Hábito: O que eles estão acostumados a fazer?

Pontue cada (1-10): Quão forte é cada força?
```

**Entregável:** `COMPETITIVE_FORCES.md` (atualizado com dados de entrevista)

**Responsável:** PM
**Esforço:** 1 dia
**Status:** Planejado

---

## T0.0.C: Finalizar Job Statement (1 dia-pessoa)

**Objetivo:** Escrever e validar job statement final

**Tarefas:**

- [ ] Rascunhar job statement das entrevistas: "When [circunstâncias], I want to [progresso], so I can [resultado]"
- [ ] Validar contra dados de entrevista (reflete insights reais?)
- [ ] Verificar três dimensões: Funcional + Emocional + Social
- [ ] Revisar com stakeholders
- [ ] Refinar com base em feedback
- [ ] Obter aprovação (assinatura de stakeholder)

**Template:**

```
Job Statement (Final):
"When [PM/Agente recebe tarefa em time distribuído],
 I want [cadeia Task→Feature→Release→OKR→Métrica visível],
 so I can [executar com propósito, não à deriva]."

Funcional: [o que precisa ser feito]
Emocional: [como eles querem se sentir]
Social: [como eles querem ser percebidos]
```

**Entregável:** `JOB_STATEMENT.md` (assinado)

**Responsável:** PM
**Esforço:** 1 dia
**Status:** Planejado

---

## Resumo

| Tarefa | Componente | Esforço | Status | Commit | Responsável |
| --- | --- | --- | --- | --- | --- |
| T0.0.1 | Release Management Framework | 1d | ✅ COMPLETO | — | PM |
| T0.0.2 | Bootstrap Gate + Validators | 2d/1d | ✅ COMPLETO | `f152801` | Engenharia |
| **Doc Updates** | BOARD + STATUS | — | ✅ COMPLETO | `5ce6124`, `4a3b4a8` | PM |
| T0.0.3 | Auto-ID APOS + CLI | 1d | 📋 PRÓXIMO | — | Engenharia |
| T0.0.A | Entrevistas JTBD | 2d | 📋 CRÍTICO | — | PM |
| T0.0.B | Análise de Forças | 1d | 📋 PRÓXIMO | — | PM |
| T0.0.C | Validação Job Statement | 1d | 📋 PRÓXIMO | — | PM |
| **PRE-SPRINT TOTAL** | | **7d** | ✅ **87.5%** | | |

---

**Contexto Crítico:**

- **T0.0.1-T0.0.3 são implementação de APOS Core** — Quando um projeto importa APOS, recebe Framework de Gerenciamento de Release + Bootstrap Gate
- **T0.0.A-T0.0.C é Descoberta JTBD** — Validar que APOS resolve o job real
- **Resultado Final:** Projeto que importa APOS sabe ser APOS, valida seus fundamentos, e pode iniciar sessões de definição

---

**Criado:** 2026-07-19  
**Última Atualização:** 2026-07-19 (T0.0.2 completo)  
**Status:** ✅ **PRE-SPRINT 87.5% COMPLETO** — Pronto para Kick-off 22 jul

**Commits de Rastreamento:**

- `f152801` — feat: implement Bootstrap Gate with real semantic validation (T0.0.2)
- `5ce6124` — docs: update Sprint 0.0 board - T0.0.2 Bootstrap Gate complete
- `4a3b4a8` — docs: update Sprint 0.0 status - T0.0.2 complete, velocity +50%
- `[este commit]` — docs: add commit tracking to TASKS.md
