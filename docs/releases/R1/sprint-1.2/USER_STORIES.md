# User Stories — Sprint R1.2

---

## US-001: Cache de Perfil do Projeto

**Como** Tech Lead solo
**Quero** que o ProjectAdapter salve o perfil descoberto em disco com TTL
**Para** não precisar re-executar detectores a cada sessão, eliminando 20-30min de retomada de contexto entre sprints

### Relação com Tasks

| Task | Tipo | Descrição |
|------|------|-----------|
| T1.1.3 | 📋 Pré-requisito | ProjectAdapter core (implementado em S1.0) |
| T1.1.4 | 📋 Pré-requisito | Validação Meu PDI (implementado em S1.1) |
| **US-001** | 🎯 **Esta US** | Cache de Perfil com TTL, hash e fallback |
| US-002 | ⏩ Dependente | Injeção de Contexto (depende do cache) |
| US-003 | ⏩ Dependente | Validação Código vs Docs (depende do cache) |

### Critérios de Aceitação

- CT01: Cache hit → retorna profile sem executar detectores
- CT02: Cache miss → discover() executado, resultado cacheado
- CT03: Invalidação por hash mismatch → recálculo automático
- CT04: Cache corrompido → fallback graceful para discover()
- CT05: TTL expirado → cache ignorado, novo discover()
- CT06: Cache vazio → comporta como miss

### Notas

- Setup zero: cache salvo automaticamente na primeira execução
- TTL default 1h, configurável via argumento
- Hash SHA256 do pyproject.toml para detecção de mudanças

---

## US-002: Injeção de Contexto Automática

**Como** Hermes Agent (agente de IA)
**Quero** receber o ProjectProfile do projeto como contexto markdown em cada task
**Para** que o Tech Lead não precise repetir manualmente 3-5 parágrafos de stack, arquitetura e decisões a cada delegação

### Relação com Tasks

| Task | Tipo | Descrição |
|------|------|-----------|
| US-001 | 🔗 Pré-requisito | Cache de Perfil (precisa do profile em disco) |
| **US-002** | 🎯 **Esta US** | CLI `apos context` + template markdown |
| US-003 | 🔗 Relacionada | Validação Código vs Docs (usa o mesmo profile) |
| R1-AC04 | 📋 Discovery | Entrevista que validou a dor (implementado em S1.1) |

### Critérios de Aceitação

- CT01: `apos context` → markdown formatado com: language, framework, database, cloud, modules, patterns
- CT02: Sem cache → "rode `apos discover` primeiro"
- CT03: Profile parcial → apenas campos preenchidos aparecem
- CT04: Saída markdown válida (parseável por outro agente)

### Notas

- Saída pensada para ser copiada diretamente no contexto de subagents
- Formato markdown para compatibilidade com Hermes, Claude Code, Codex
- Zero configuração necessária

---

## US-003: Validação Código vs Documentação

**Como** Tech Lead
**Quero** rodar `apos validate` para comparar o perfil real do projeto com o que está documentado nos SDDs
**Para** detectar divergências entre código e documentação antes que virem dívida técnica invisível

### Relação com Tasks

| Task | Tipo | Descrição |
|------|------|-----------|
| US-001 | 🔗 Pré-requisito | Cache de Perfil (profile descoberto) |
| R1.2 | 🔗 Pré-requisito | BootstrapGateV2 (validação de fundações, S1.1) |
| T1.1.3 | 📋 Pré-requisito | ProjectAdapter detectores (implementado) |
| **US-003** | 🎯 **Esta US** | CLI `apos validate` + relatório de divergências |
| R1.3 | 📋 Futuro | Rastreamento ADR→SDD→Código (impactado por esta US) |

### Critérios de Aceitação

- CT01: Stack coincide → relatório 100% verde ✅
- CT02: Framework diferente do documentado → alerta ❌
- CT03: SDD sem código correspondente → warning ⚠️
- CT04: Código sem SDD correspondente → warning ⚠️

### Notas

- **Regra de ouro:** zero falsos positivos nas primeiras 5 execuções
- Validado contra 2 repositórios reais (APOS raiz + Meu PDI backend/)
- Relatório em formato markdown para fácil leitura

---

## Mapa de Dependências

```
US-001 (Cache Profile) ──→ US-002 (Inject Context)
     │
     └──→ US-003 (Validate Code vs Docs) ←── R1.2 (BootstrapGateV2)
```

| US | Depende de | Desbloqueia |
|----|-----------|-------------|
| US-001 | ProjectAdapter (S1.0) | US-002, US-003 |
| US-002 | US-001 | — |
| US-003 | US-001 + BootstrapGateV2 | R1.3 (Trace) |

---

**Total:** 3 User Stories | **Core:** 2 (3.5 SP) | **Stretch:** 1 (1.5 SP)
