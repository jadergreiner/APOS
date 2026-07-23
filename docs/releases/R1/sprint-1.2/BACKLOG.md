# Backlog R1.2 — Consolidado da Tríade

**Data:** 2026-07-23
**Baseado em:** Entrevista Tech Lead (FINDINGS_TECH_LEAD.md)
**Pareceres:** SME, PM, SM

---

## 1. Velocity e Capacidade

| Sprint | SP | Observação |
|--------|:--:|------------|
| S1.0 | 3.5 | Baseline (primeira sprint dupla via) |
| S1.1 | 6.0 | Curva de aprendizado + subagents |
| **Média** | **4.75** | |
| **Recomendado R1.2** | **5.0** (core) | Buffer para imprevistos |

---

## 2. User Stories Priorizadas

### US-001: Cache de Perfil do Projeto (D01/D03) — P0

**Como** Tech Lead solo
**Quero** que o ProjectAdapter cacheie o profile descoberto entre sessões
**Para** não precisar re-descobrir a estrutura do projeto a cada execução

| Critério | Detalhe |
|----------|---------|
| **DoR** | ProjectAdapter funcional, ProjectProfile schema congelado |
| **SP** | 1.5 (SME) / 1.5 (PM) → **1.5** |
| **Sprint** | R1.2 |

**DoD:**
- [ ] Profile cacheado em disco (JSON, ~2KB)
- [ ] Cache TTL configurável (default 1h)
- [ ] Cache invalida se pyproject.toml mudar (hash)
- [ ] Fallback para discover() se cache expirado
- [ ] Testes: cache hit, cache miss, invalidação, corrupção

**Cenários:**
- CT01: Cache hit → retorna profile sem executar detectores
- CT02: Cache miss → discover() executado, resultado cacheado
- CT03: Invalidação por hash mismatch → recálculo automático
- CT04: Cache corrompido → fallback graceful para discover()

---

### US-002: Injeção Automática de Contexto (D03) — P0

**Como** Hermes Agent
**Quero** receber o ProjectProfile automaticamente no contexto de cada task
**Para** não precisar que o Jader repita 3-5 parágrafos de contexto manualmente

| Critério | Detalhe |
|----------|---------|
| **DoR** | US-001 concluída, ProjectProfile schema disponível |
| **SP** | 2.0 (SME) / 2.0 (PM) → **2.0** |
| **Sprint** | R1.2 |

**DoD:**
- [ ] CLI `apos context` exibe profile atual
- [ ] Formato de saída: markdown pronto para copiar
- [ ] Integração com Hermes: contexto injetado automaticamente
- [ ] Testes: output formatado, dados corretos

**Cenários:**
- CT01: `apos context` → markdown com stack, módulos, padrões
- CT02: Sem cache → mensagem clara "rode discover primeiro"
- CT03: Profile parcial → apenas campos preenchidos aparecem

---

### US-003: Validação Código vs Documentação (D02) — P0

**Como** Tech Lead
**Quero** rodar um comando que compare o profile descoberto com a documentação
**Para** detectar divergências entre código e docs antes que virem dívida técnica

| Critério | Detalhe |
|----------|---------|
| **DoR** | US-001 concluída, BootstrapGateV2 existente |
| **SP** | 1.5 (SME) / 1.5 (PM) → **1.5** |
| **Sprint** | R1.2 (stretch) ou R1.3 |

**DoD:**
- [ ] Comando `apos validate` compara profile vs docs/SDD/
- [ ] Relatório: consistentes, divergentes, ausentes
- [ ] Zero falsos positivos nas primeiras 5 execuções
- [ ] Testes: divergência detectada, consistência confirmada

**Cenários:**
- CT01: Stack coincide → relatório verde
- CT02: Framework diferente → alerta de divergência
- CT03: SDD sem código correspondente → warning
- CT04: Código sem SDD → warning

---

## 3. Matriz de Dependências

```
US-001 (Cache Profile) ← não depende de ninguém
    │
    ├──→ US-002 (Inject Context) ← depende de US-001
    │
    └──→ US-003 (Validate Code vs Docs) ← depende de US-001 + BootstrapGateV2
```

**Ordem de implementação:** US-001 → (US-002 em paralelo com preparação da US-003) → US-003

---

## 4. Alocação Recomendada para R1.2

| US | SP | Prioridade | Sprint |
|----|:--:|:----------:|:------:|
| US-001: Cache Profile | 1.5 | P0 🔴 | Core |
| US-002: Inject Context | 2.0 | P0 🔴 | Core |
| US-003: Validate Code vs Docs | 1.5 | P0 🔴 | Stretch |
| R0-AC04: Stakeholder (carry-over) | 0.5 | 🟡 | Carry-over |
| **Total Core** | **3.5** | | |
| **Total Stretch** | **5.5** | | |

**Capacidade:** 5.0 SP core → US-001 + US-002 + carry-over = 4.0 SP ✅
**Stretch:** US-003 se velocity permitir

---

## 5. Riscos

| Risco | Prob | Impacto | Mitigação |
|-------|:----:|:-------:|-----------|
| US-003 gerar falso positivo → abandonado | Média | Alto | Validar com 3 repos antes de liberar |
| Cache corrompido silenciosamente | Baixa | Alto | Hash validation + fallback automático |
| Context injection quebrar formato do Hermes | Baixa | Alto | Testar com subagent real antes de deploy |

---

## 6. Artefatos Gerados

| Documento | Autor | Local |
|-----------|-------|-------|
| Parecer Técnico | SME | `docs/discovery/PARECER_TECNICO_TECH_LEAD.md` |
| User Stories + Cenários | SME | `docs/discovery/USER_STORIES_TECH_LEAD.md` |
| Recomendação Sprint | SME | `docs/discovery/RECOMENDACAO_SPRINT_TECH_LEAD.md` |
| Parecer de Produto | PM | `docs/discovery/PARECER_PRODUTO_PM.md` |
| Parecer Scrum Master | SM | `docs/releases/R1/sprint-1.2/PARECER_SM_R1.2.md` |
| **Backlog Consolidado** | Tríade | `docs/releases/R1/sprint-1.2/BACKLOG.md` |
