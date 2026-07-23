# Recomendação de Sprint — User Stories Discovery Tech Lead

**Gerado em:** 2026-07-23  
**Base:** `PARECER_TECNICO_TECH_LEAD.md` + `USER_STORIES_TECH_LEAD.md`

---

## Resumo da Carga

| Sprint | US | Descrição | SP | Depende de |
|--------|----|-----------|----|-----------|
| **R1.2** | US-001 | Cache de Perfil | 2.0 | ProjectAdapter |
| **R1.2** | US-002 | Validação Código vs Docs | 3.0 | US-001 |
| **R1.2** | US-003 | Injeção Automática de Contexto | 1.5 | US-001 |
| | **Total R1.2** | | **6.5 SP** | |
| **R1.3** | US-004 | Rastreamento ADR→SDD→Código | 3.0 | US-002 |
| **R1.3** | US-005 | Validação de Stack | 1.5 | US-001 |
| | **Total R1.3** | | **4.5 SP** | |

---

## Estratégia de Execução

### R1.2 (6.5 SP)

| Ordem | US | Motivo |
|-------|----|--------|
| 1º | **US-001** (Cache) | Base para todas as outras; reúso imediato na sprint |
| 2º | **US-003** (Injeção) | Menor esforço (1.5 SP), maior impacto percebido (contexto automático) |
| 3º | **US-002** (Validação) | Mais complexa (3.0 SP), mas fecha o ciclo descobrir→validar→injetar |

**Setup-zero mantido:** Nenhuma US exige configuração manual — tudo funciona ao rodar `apos discover` ou `apos validate`.

### R1.3 (4.5 SP)

| Ordem | US | Motivo |
|-------|----|--------|
| 1º | **US-005** (Stack) | Rápida (1.5 SP), complementa D05 |
| 2º | **US-004** (Rastreio) | Mais complexa (3.0 SP), exige ADRs padronizados |

---

## Matriz de Valor x Esforço

```
Alto ▲
Valor │  US-003 (1.5)  US-002 (3.0)
      │     ●               ●
      │
      │            US-001 (2.0)
      │               ●
      │
      │         US-005 (1.5)   US-004 (3.0)
      │            ●               ●
Baixo └──────────────────────────────────▶
      Baixo      Esforço            Alto
```

**US-003** tem o melhor ratio valor/esforço — deve ser priorizada logo após a base (US-001).

---

## Riscos da Recomendação

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| US-002 gerar falso positivo nas primeiras execuções | Médio | Heurística conservadora; teste em Meu PDI antes de liberar |
| Cache de perfil ficar obsoleto entre mudanças frequentes | Baixo | Hash cobre pyproject, setup.py e estrutura de módulos |
| ADRs inexistentes ou não padronizados (US-004) | Alto | Adiar para R1.3; usar sprint R1.2 para definir padrão ADR |
| ContextInjector aumentar latência das tasks | Baixo | Limite de 2000 tokens; tempo de injeção < 50ms |

---

## Decisão

**✅ Recomendado:** Contratar R1.2 com US-001 → US-003 → US-002 (6.5 SP total).  
**⏸️ Adiado:** US-004 e US-005 para R1.3 (4.5 SP total).  
**📋 Pré-requisito:** Convocar Tríade para validação do parecer antes de iniciar implementação.
