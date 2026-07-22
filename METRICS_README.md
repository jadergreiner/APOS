# APOS Sprint 0.3 - Sistema de Coleta de Métricas Baseline

**Status:** ✅ Pronto para Piloto (24-29 julho)  
**Responsável:** T0.3.6 - Claude Code  
**Propósito:** Validar que MVP reduz reexplicação de contexto em 80%+

---

## Visão Rápida

Sistema automático para coletar, consolidar e analisar 6 métricas baseline durante piloto de 6 dias (D1-D6).

**6 Métricas Críticas:**
1. **Setup Time** — <30 min para onboarding
2. **Adoption** — 3/3 personas ativas D7
3. **Orphan Detection** — 0% FN, <5% FP
4. **Trust Score Accuracy** — >85%
5. **API Performance** — P95 <500ms
6. **Business Impact** — >80% reduction em reexplicação

**Deliverables:**
- 📊 `metrics_data/metrics.json` — Dados estruturados (entrada)
- 📈 `metrics_data/summary.csv` — Rollup diário (análise)
- 📋 `RESULTS.md` — Relatório final + Go/No-Go decision

---

## Início Rápido

### 1. Testar com Dados de Exemplo

```bash
cd C:\repo\APOS

# Copiar exemplo
cp docs/releases/R0/sprint-0.3/metrics_data/metrics_example.json \
   docs/releases/R0/sprint-0.3/metrics_data/metrics.json

# Gerar relatórios
python scripts/metrics_collector.py --action finalize

# Resultado esperado: 🟢 GREEN - SHIP MVP
```

### 2. Durante Piloto (D1-D6)

#### Dia 1: Setup Times

```bash
python scripts/metrics_collector.py \
  --action setup \
  --persona "AI Architect" \
  --start-time "2026-07-24T09:30:00" \
  --end-time "2026-07-24T09:52:00"
```

#### Dias 1-6: Adoption Diária

```bash
python scripts/metrics_collector.py \
  --day 1 \
  --action record \
  --adoption 3 \
  --crashes 0 \
  --notes "Setup completo, dashboard OK"
```

#### Dias 3-6: Dados Quantitativos

Adicione manualmente ao `metrics_data/metrics.json`:

```json
{
  "orphan_detection": [{...}],
  "trust_scores": [{...}],
  "api_performance": [{...}],
  "business_impact": [{...}]
}
```

#### Dia 6: Gerar Relatório Final

```bash
python scripts/metrics_collector.py --action finalize

# Output: RESULTS.md com decision 🟢/🟡/🔴
```

---

## Documentação Completa

| Arquivo | Propósito |
|---------|-----------|
| **scripts/metrics_collector.py** | CLI Python para coleta |
| **METRICS_COLLECTOR_GUIDE.md** | Guia passo-a-passo (como coletar dados) |
| **T036_IMPLEMENTATION_SUMMARY.md** | Resumo técnico da implementação |
| **METRICS_BASELINE.md** | Definição original de métricas |
| **PILOT_PLAN.md** | Plano executivo do piloto |

---

## Go/No-Go Decision

**Critérios (todos devem passar):**

| Criterio | Alvo | Pass? |
|----------|------|-------|
| Setup time <30 min | <30 min | ✅ |
| Adoption 3/3 Dia 7 | 100% | ✅ |
| Orphan Detection 0% FN | 0% | ✅ |
| Orphan Detection <5% FP | <5% | ✅ |
| API P95 <500ms | <500ms | ✅ |
| Trust Score >85% accuracy | >85% | ✅ |

**Decision Logic:**
- ✅ **GREEN** (6/6 pass) → SHIP MVP, iniciar R1
- ⚠️ **YELLOW** (5/6 pass) → Iterate 1 week
- ❌ **RED** (<5/6 pass) → Back to drawing board

---

## Estrutura de Dados

### Entrada: metrics.json

```json
{
  "pilot_start": "2026-07-24",
  "pilot_end": "2026-07-29",
  "personas": ["AI Architect", "Product Ops", "Early Adopter"],
  
  "setup_times": [
    {"persona": "AI Architect", "duration_minutes": 22.0, ...}
  ],
  
  "adoption": [
    {"day": 1, "personas_active": 3, "crashes": 0, ...}
  ],
  
  "orphan_detection": [
    {"persona": "AI Architect", "day": 3, 
     "manual_count": 52, "plugin_count": 48, 
     "false_negatives": 2, "false_positives": 1, ...}
  ],
  
  "trust_scores": [
    {"persona": "AI Architect", "day": 4, 
     "accuracy_percentage": 92.5, ...}
  ],
  
  "api_performance": [
    {"day": 1, "p95_latency_ms": 420.0, 
     "error_rate_percentage": 0.8, ...}
  ],
  
  "business_impact": [
    {"persona": "AI Architect", "metric_type": "reexplication_hours",
     "before_value": 2.5, "after_value": 0.3, 
     "reduction_percentage": 88.0, ...}
  ],
  
  "daily_notes": {
    "day_1": {"date": "2026-07-24", "notes": "Setup ok"}
  }
}
```

### Saída: summary.csv

Tabela com rollup diário (1 linha = 1 dia):

```
Dia,Data,Setup Time,Adoption,Crashes,API P95,API Error,FN%,FP%,Trust Score,Notes
1,2026-07-24,24.0,3/3,0,420,0.8,—,—,—,"Setup ok"
2,2026-07-25,—,3/3,0,380,0.6,1.5,1.5,—,"Exploracao"
```

### Saída: RESULTS.md

Relatório executivo com:
- 🟢/🟡/🔴 Decision + Rationale
- Critérios (6) + Status
- Métricas Detalhadas (D1-D6)
- Notas Diárias + Aprendizados
- Recomendações Próximos Passos

---

## CLI Reference

```bash
# Ajuda
python scripts/metrics_collector.py --help

# Setup time (D1)
python scripts/metrics_collector.py \
  --action setup \
  --persona "AI Architect" \
  --start-time "2026-07-24T09:30:00" \
  --end-time "2026-07-24T09:52:00"

# Adoption + notes (D1-D6)
python scripts/metrics_collector.py \
  --day 1 \
  --action record \
  --adoption 3 \
  --crashes 0 \
  --notes "Descricao do dia"

# Daily report
python scripts/metrics_collector.py --action report

# Final report
python scripts/metrics_collector.py --action finalize
```

---

## Timeline

| Quando | O Que | Script |
|--------|-------|--------|
| D1 (24 jul) | Record 3x setup + adoption | `--action setup` + `--action record` |
| D2-D3 (25-26 jul) | Record adoption + manual tests | `--action record` |
| D3 (26 jul) | Gerar summary CSV | `--action report` |
| D4-D5 (27-28 jul) | Record adoption + quant data | `--action record` |
| D6 (29 jul) | Record final + gerar RESULTS | `--action record` + `--action finalize` |
| D6 (29 jul) | Call 1h com personas → decision | (manual) |

---

## Arquivos

```
C:\repo\APOS\
├── scripts/
│   └── metrics_collector.py (700+ linhas, CLI tool)
│
├── docs/releases/R0/sprint-0.3/
│   ├── METRICS_BASELINE.md (definição original de 6 métricas)
│   ├── METRICS_COLLECTOR_GUIDE.md (guia passo-a-passo)
│   ├── T036_IMPLEMENTATION_SUMMARY.md (resumo técnico)
│   ├── PILOT_PLAN.md (plano do piloto D1-D6)
│   ├── RESULTS.md (gerado automaticamente no D6)
│   │
│   └── metrics_data/
│       ├── metrics.json (dados estruturados - ENTRADA)
│       ├── metrics_example.json (exemplo para teste)
│       └── summary.csv (gerado automaticamente)
│
└── METRICS_README.md (este arquivo)
```

---

## Exemplo: Test Run

```bash
cd C:\repo\APOS

# 1. Usar dados de exemplo
cp docs/releases/R0/sprint-0.3/metrics_data/metrics_example.json \
   docs/releases/R0/sprint-0.3/metrics_data/metrics.json

# 2. Gerar relatórios
python scripts/metrics_collector.py --action finalize

# 3. Verificar outputs
ls -lh docs/releases/R0/sprint-0.3/metrics_data/
cat docs/releases/R0/sprint-0.3/RESULTS.md | head -30
```

**Expected Output:**
```
Setup Time (avg): 24.0 min (target: <30 min) - [PASS]
Adoption (latest): 3/3 - [PASS]
API P95 Latency (latest): 340ms (target: <500ms) - [PASS]
Orphan Detection: FN=1.08% (target: 0%), FP=0.67% (target: <5%)
Trust Score Accuracy: 92.00% (target: >85%)

Decision: 🟢 GREEN - SHIP MVP
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| **UnicodeEncodeError** | Já fixado. Script usa UTF-8 + safe_print() |
| **metrics.json não carrega** | Valide JSON: `python -m json.tool metrics.json` |
| **CSV não gerou** | Verifique permissões do diretório |
| **RESULTS.md vazio** | Certifique que dados foram coletados |

---

## Próximos Passos

1. ✅ **Pronto:** Tudo implementado e testado
2. ⏳ **D1 (24 jul):** Começar coleta durante piloto
3. ⏳ **D6 (29 jul):** Gerar RESULTS.md + decision
4. ⏳ **D7 (30 jul):** Executar decision (ship / iterate / redesign)

---

**Compilado por:** Claude Code  
**Data:** 2026-07-21  
**Status:** 🟢 Pronto para Piloto

