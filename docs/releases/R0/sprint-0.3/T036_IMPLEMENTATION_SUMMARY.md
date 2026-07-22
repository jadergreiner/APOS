# T0.3.6 - Implementação de Coleta de Métricas Baseline

**Data:** 2026-07-21  
**Status:** ✅ 100% Completo  
**Responsável:** Claude Code  
**Next:** Execução durante piloto (D1-D6: 24-29 julho)

---

## Visão Geral

Implementado sistema automático de coleta, consolidação e análise de 6 métricas baseline para validar que MVP reduz reexplicação de contexto em 80%+.

**Componentes:**
1. ✅ `scripts/metrics_collector.py` — CLI para coleta de dados
2. ✅ `metrics_data/metrics.json` — Armazenamento estruturado
3. ✅ `metrics_data/summary.csv` — Rollup diário
4. ✅ `RESULTS.md` — Relatório final + Go/No-Go
5. ✅ `METRICS_COLLECTOR_GUIDE.md` — Guia de uso

---

## 1. Arquitetura

```
Coleta de Dados (D1-D6)
    ↓
metrics.json (JSON estruturado)
    ↓
├─ summary.csv (rollup diário, análise rápida)
└─ RESULTS.md (relatório executivo + Go/No-Go)
```

### Dados Coletados

**Setup Time** (D1)
- Persona, start_time, end_time, duration_minutes
- Target: <30 min por persona
- Method: Manual (cronômetro)

**Adoption** (D1-D6)
- Day, personas_active, crashes, notes
- Target: 3/3 ativo D7 (100%)
- Method: Daily check-in + telemetria

**Orphan Detection Accuracy** (D3, D6)
- Persona, manual_count, plugin_count, FN, FP
- Target: 0% FN, <5% FP
- Method: Manual validation (count diferença)

**Trust Score Accuracy** (D4)
- Persona, avg_diff (manual vs plugin), accuracy%
- Target: >85% acurácia
- Method: Compare 5-10 tasks (manual review vs plugin score)

**API Performance** (D1-D6)
- Day, P50/P95/P99 latência, error_rate, total_calls
- Target: P95 <500ms, <2% error rate
- Method: Backend logs/monitoring

**Business Impact** (D5-D6)
- Persona, metric_type (reexplication_hours, orphan_rate, nps)
- Before/after values, reduction%
- Target: >80% reduction
- Method: Personas self-report (D6 call final)

---

## 2. Como Usar

### Inicializar (antes do piloto)

```bash
cd C:\repo\APOS

# Dados já estão prontos (metrics.json vazio + exemplo)
# Nenhuma ação necessária — pronto para começar
```

### Coletar Dados (durante piloto)

#### Dia 1: Setup Times

```bash
# Persona 1
python scripts/metrics_collector.py \
  --action setup \
  --persona "AI Architect" \
  --start-time "2026-07-24T09:30:00" \
  --end-time "2026-07-24T09:52:00"

# Personas 2 e 3 (similar)
```

#### Dias 1-6: Adoption Diária

```bash
# Dia 1
python scripts/metrics_collector.py \
  --day 1 \
  --action record \
  --adoption 3 \
  --crashes 0 \
  --notes "Setup completo, primeiras impressões positivas"

# Dias 2-6 (similar, ajustando personas_active e crashes)
```

#### Dias 3-6: Dados Quantitativos

**Manualmente adicione ao `metrics_data/metrics.json`:**

```json
{
  "orphan_detection": [
    {
      "persona": "AI Architect",
      "day": 3,
      "manual_count": 52,
      "plugin_count": 48,
      "false_negatives": 2,
      "false_positives": 1,
      ...
    }
  ],
  "api_performance": [
    {
      "day": 1,
      "p50_latency_ms": 285.0,
      "p95_latency_ms": 420.0,
      ...
    }
  ],
  "business_impact": [
    {
      "persona": "AI Architect",
      "metric_type": "reexplication_hours",
      "before_value": 2.5,
      "after_value": 0.3,
      ...
    }
  ]
}
```

### Gerar Relatórios

#### Daily Summary (Dias 3-6)

```bash
python scripts/metrics_collector.py --action report

# Output:
# ✅ Summary CSV generated: metrics_data/summary.csv
# (também imprime resumo em stdout)
```

#### Final Report (Dia 6)

```bash
python scripts/metrics_collector.py --action finalize

# Output:
# ✅ Final report generated: RESULTS.md
# (também imprime resumo em stdout)
```

---

## 3. Estrutura de Dados

### metrics.json (Entrada)

```json
{
  "pilot_start": "2026-07-24",
  "pilot_end": "2026-07-29",
  "personas": ["AI Architect", "Product Ops", "Early Adopter"],
  "setup_times": [...],
  "adoption": [...],
  "orphan_detection": [...],
  "trust_scores": [...],
  "api_performance": [...],
  "business_impact": [...],
  "daily_notes": {...}
}
```

### summary.csv (Output)

Tabela com rollup diário:
- Setup Time (avg), Adoption (personas), Crashes
- API P95 (ms), Error Rate (%)
- Orphan FN% / FP%
- Trust Score Accuracy (%)
- Daily notes

Exemplo:
```
Dia,Data,Setup Time,Adoption,Crashes,API P95,API Error,Orphan FN,Orphan FP,Trust Score,Notes
1,2026-07-24,24.0,3/3,0,420,0.8,—,—,—,"Setup ok"
```

### RESULTS.md (Output)

Relatório executivo com:
1. **Go/No-Go Decision** — 🟢 GREEN, 🟡 YELLOW, ou 🔴 RED
2. **Critérios de Sucesso** — Tabela com 6 critérios + status
3. **Métricas Detalhadas** — Histórico D1-D6
4. **Notas Diárias** — Aprendizados por dia
5. **Recomendações** — Próximos passos (baseado em decision)

---

## 4. Exemplo Prático (Test Run)

Já incluímos dados de exemplo em `metrics_data/metrics_example.json`. Você pode testar:

```bash
# Copiar exemplo → dados reais
cp metrics_data/metrics_example.json metrics_data/metrics.json

# Gerar relatórios
python scripts/metrics_collector.py --action finalize

# Verificar
ls -lh metrics_data/
cat metrics_data/summary.csv
cat RESULTS.md | head -50
```

**Output esperado:**
- ✅ Setup Time: 24.0 min (PASS)
- ✅ Adoption: 3/3 (PASS)
- ✅ Orphan Detection FP: 0.67% (PASS)
- ✅ API P95: 340ms (PASS)
- ✅ Trust Score: 92% (PASS)
- **Decision: 🟢 GREEN - SHIP MVP**

---

## 5. Timeline de Execução

| Dia | Data | O Que Fazer | Script |
|-----|------|-----------|--------|
| D1 | 24 jul | Record 3x setup times | `--action setup` |
| D1 | 24 jul | Record adoption D1 | `--action record --day 1` |
| D2 | 25 jul | Record adoption D2 | `--action record --day 2` |
| D3 | 26 jul | Record adoption D3, manual orphan tests | `--action record --day 3` |
| D3 | 26 jul | Gerar summary CSV | `--action report` |
| D4 | 27 jul | Record adoption D4, API data | `--action record --day 4` |
| D5 | 28 jul | Record adoption D5, trust score | `--action record --day 5` |
| D6 | 29 jul | Record adoption D6, business impact | `--action record --day 6` |
| D6 | 29 jul | Gerar RESULTS.md final | `--action finalize` |
| D6 | 29 jul | Call 1h com personas → NPS + decision | (manual) |

---

## 6. Critérios de Go/No-Go

**6 Critérios High-Priority (todos devem passar):**

| Criterio | Alvo | Status PASS |
|----------|------|-----------|
| Setup time <30 min | <30 min | 3/3 personas |
| Adoption 3/3 Dia 7 | 100% | 3/3 ativo |
| Orphan Detection 0% FN | 0% | Zero false negatives |
| Orphan Detection <5% FP | <5% | <5% false positives |
| API P95 <500ms | <500ms | P95 latência |
| Trust Score >85% accuracy | >85% | Acurácia |

**Decision:**
- ✅ **GREEN**: 6/6 passed → SHIP MVP (R1 planning)
- ⚠️ **YELLOW**: 5/6 passed → ITERATE 1 week
- ❌ **RED**: <5/6 passed → BACK TO DRAWING BOARD

---

## 7. Troubleshooting

### JSON Encoding Error
→ Use UTF-8. Script já está configurado com `encoding='utf-8'`

### Emoji em Terminal
→ Script usa substituição ASCII: ✅ → [PASS], ❌ → [FAIL], etc.

### CSV não gerou
→ Verifique permissões: `ls -la metrics_data/`

### RESULTS.md vazio
→ Certifique que dados foram coletados em `metrics.json`

---

## 8. Checklist de Implementação

- ✅ `scripts/metrics_collector.py` implementado (700+ linhas)
- ✅ Suporte a 6 tipos de dados (setup, adoption, orphans, trust, api, impact)
- ✅ CLI com 4 ações (setup, record, report, finalize)
- ✅ Geração automática de CSV (summary)
- ✅ Geração automática de Markdown (RESULTS.md)
- ✅ Go/No-Go logic implementada (6 critérios)
- ✅ Exemplo de dados (metrics_example.json)
- ✅ Guia de uso (METRICS_COLLECTOR_GUIDE.md)
- ✅ Documentação inline (docstrings)
- ✅ Encoding UTF-8 (suporta caracteres especiais)

---

## 9. Próximos Passos

### Antes do Piloto (23 jul)
1. ✅ Review METRICS_BASELINE.md (já feito)
2. ✅ Review PILOT_PLAN.md (já feito)
3. ✅ Test metrics_collector.py com dados exemplo (já feito)
4. ⏳ **Jader:** Confirmar que T0.3.5 (Piloto) está pronto

### Durante o Piloto (D1-D6: 24-29 jul)
1. D1: Record setup times (3x) + adoption
2. D2-D6: Record adoption diária + notas
3. D3: First manual validation (orphan detection)
4. D4: Trust Score accuracy validation
5. D5-D6: Business impact data
6. D6 (final): Gerar RESULTS.md + call com personas

### Após Piloto (30 jul+)
1. Compilar RESULTS.md com Go/No-Go decision
2. Se GREEN: Merge para main + iniciar R1 planning
3. Se YELLOW: 1 week iteração + re-test
4. Se RED: RCA + re-arquiteurar R0.3.1

---

## Ficheiro de Referência

| Arquivo | Propósito | Status |
|---------|-----------|--------|
| `scripts/metrics_collector.py` | CLI para coleta | ✅ 100% |
| `metrics_data/metrics.json` | Dados estruturados | ✅ Template pronto |
| `metrics_data/summary.csv` | Rollup diário | ✅ Auto-gerado |
| `RESULTS.md` | Relatório final | ✅ Auto-gerado |
| `METRICS_BASELINE.md` | Definição original | ✅ Existente |
| `METRICS_COLLECTOR_GUIDE.md` | Guia de uso | ✅ 100% |
| `PILOT_PLAN.md` | Plano executivo | ✅ Existente |

---

**Status Final:** 🟢 PRONTO PARA PILOTO

Todas as ferramentas estão implementadas e testadas. Sistema pronto para coletar dados D1-D6 e gerar relatório final com Go/No-Go decision em D6.

