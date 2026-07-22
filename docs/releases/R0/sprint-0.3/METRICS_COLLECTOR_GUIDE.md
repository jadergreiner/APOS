# Guia de Uso - Metrics Collector (T0.3.6)

**Propósito:** Coletar e consolidar 6 métricas baseline durante piloto (D1-D6).

**Arquivo:** `scripts/metrics_collector.py`

**Output:**
- `metrics_data/metrics.json` — Dados estruturados (todas métricas)
- `metrics_data/summary.csv` — Rollup diário (para análise)
- `RESULTS.md` — Relatório final com Go/No-Go decision

---

## 1. Setup Inicial

```bash
cd C:\repo\APOS

# Criar diretório de dados
mkdir -p docs/releases/R0/sprint-0.3/metrics_data

# Verificar instalação
python scripts/metrics_collector.py

# Esperado: Resumo vazio (0 métricas coletadas ainda)
```

---

## 2. Coleta de Métricas (D1-D6)

### D1 (24 jul) - Setup Time

```bash
# Persona 1: AI Architect
python scripts/metrics_collector.py \
  --action setup \
  --persona "AI Architect" \
  --start-time "2026-07-24T09:30:00" \
  --end-time "2026-07-24T09:52:00"

# Persona 2: Product Ops
python scripts/metrics_collector.py \
  --action setup \
  --persona "Product Ops" \
  --start-time "2026-07-24T10:05:00" \
  --end-time "2026-07-24T10:31:00"

# Persona 3: Early Adopter
python scripts/metrics_collector.py \
  --action setup \
  --persona "Early Adopter" \
  --start-time "2026-07-24T10:45:00" \
  --end-time "2026-07-24T11:09:00"
```

**Esperado Output:**
```
✅ Setup recorded: AI Architect - 22.0 min
✅ Setup recorded: Product Ops - 26.0 min
✅ Setup recorded: Early Adopter - 24.0 min
```

### D1-D6 - Adoption Diária

```bash
# Dia 1: 3/3 personas ativo, 0 crashes
python scripts/metrics_collector.py \
  --day 1 \
  --action record \
  --adoption 3 \
  --crashes 0 \
  --notes "Setup completo. Primeiras impressões positivas. Dashboard carregando bem."

# Dia 2: continua 3/3, 0 crashes
python scripts/metrics_collector.py \
  --day 2 \
  --action record \
  --adoption 3 \
  --crashes 0 \
  --notes "Exploracao de features. Encontrou 2 UX issues (modal width, button text)."

# ... continue para dias 3-6
```

### D4-D6 - Importar Dados Quantitativos

**Detecção de Orfas:** Requer coleta manual (não automática)

```bash
# Importar dados como JSON direto no metrics.json
# Exemplo: Adicione manualmente ao arquivo metrics_data/metrics.json:

{
  "orphan_detection": [
    {
      "persona": "AI Architect",
      "day": 3,
      "manual_count": 52,
      "plugin_count": 48,
      "false_negatives": 2,
      "false_positives": 1,
      "fn_rate_percentage": 3.85,
      "fp_rate_percentage": 2.08,
      "fn_status": "⚠️ CONDITIONAL",
      "fp_status": "✅ PASS"
    }
  ]
}
```

**Trust Score Accuracy:** Manual validation contra 5-10 tasks

```json
{
  "trust_scores": [
    {
      "persona": "AI Architect",
      "day": 4,
      "avg_diff": 0.15,
      "accuracy_percentage": 92.5,
      "target_accuracy": 85,
      "status": "✅ PASS"
    }
  ]
}
```

**API Performance:** Cole dados de backend logs/monitoring

```json
{
  "api_performance": [
    {
      "day": 1,
      "p50_latency_ms": 285.0,
      "p95_latency_ms": 420.0,
      "p99_latency_ms": 580.0,
      "error_rate_percentage": 0.8,
      "total_calls": 1250,
      "error_calls": 10,
      "target_p95_ms": 500,
      "target_error_rate": 2.0,
      "p95_status": "✅ PASS",
      "error_status": "✅ PASS"
    }
  ]
}
```

---

## 3. Checklist de Coleta por Dia

### Dia 1 (24 jul)
- [ ] Record setup times (3 personas)
- [ ] Record adoption (3/3)
- [ ] Add daily notes

### Dia 2 (25 jul)
- [ ] Record adoption
- [ ] Manual test: Orphan detection (1 persona)
- [ ] Add daily notes

### Dia 3 (26 jul)
- [ ] Record adoption
- [ ] Manual test: Orphan detection (all 3 personas)
- [ ] Manual test: Trust Score accuracy (all 3 personas)
- [ ] Generate report: `python scripts/metrics_collector.py --action report`

### Dia 4 (27 jul)
- [ ] Record adoption + any crashes
- [ ] Collect API performance data from backend logs
- [ ] Manual revalidate: Orphan detection accuracy
- [ ] Add daily notes with fixes applied

### Dia 5 (28 jul)
- [ ] Final adoption check
- [ ] Collect updated API metrics
- [ ] Manual test: Trust Score with D5 data
- [ ] Update business impact metrics (before/after)

### Dia 6 (29 jul)
- [ ] Final adoption validation
- [ ] Call final com 3 personas (NPS, feedback)
- [ ] Compile all business impact data
- [ ] Finalize report: `python scripts/metrics_collector.py --action finalize`

---

## 4. Coleta de Dados Subjetivos (Business Impact)

**Re-explicação de Contexto:**

Perguntar personas no Dia 6:
- "Quanto tempo você passou reexplicando contexto esta semana?"
- "Antes do MVP, era ~2-3 horas. Hoje?"

```bash
python scripts/metrics_collector.py \
  --action record \
  --day 6 \
  --notes "Business Impact - AI Architect: before=2.5h, after=0.3h, reduction=88%"
```

Depois, manualmente adicione ao `metrics.json`:

```json
{
  "business_impact": [
    {
      "persona": "AI Architect",
      "metric_type": "reexplication_hours",
      "before_value": 2.5,
      "after_value": 0.3,
      "reduction_percentage": 88.0,
      "target_reduction": 80.0,
      "status": "✅ PASS"
    }
  ]
}
```

**NPS Score:**

```json
{
  "nps_data": [
    {
      "persona": "AI Architect",
      "score": 9,
      "category": "Promoter"
    },
    {
      "persona": "Product Ops",
      "score": 8,
      "category": "Promoter"
    },
    {
      "persona": "Early Adopter",
      "score": 7,
      "category": "Passive"
    }
  ]
}
```

---

## 5. Geração de Relatórios

### Daily Summary (Dias 3-6)

```bash
python scripts/metrics_collector.py --action report

# Output esperado:
# ✅ Summary CSV generated: docs/releases/R0/sprint-0.3/metrics_data/summary.csv
```

Isso gera uma tabela com rollup diário:

```
Dia,Data,Setup Time (min),Adoption,Crashes,API P95 (ms),Orphan FN%,Orphan FP%,...
1,2026-07-24,24.0,3/3,0,420,0.0,2.0,...
2,2026-07-25,—,3/3,0,380,1.5,1.5,...
...
```

### Final Report (Dia 6)

```bash
python scripts/metrics_collector.py --action finalize

# Output esperado:
# ✅ Final report generated: docs/releases/R0/sprint-0.3/RESULTS.md
```

Isso gera:
1. **Go/No-Go Decision** — 🟢 GREEN, 🟡 YELLOW, ou 🔴 RED
2. **Critérios de Sucesso** — Tabela com todos 6 critérios + status
3. **Métricas Detalhadas** — Todas 6 métricas com histórico D1-D6
4. **Notas Diárias** — Aprendizados e contexto
5. **Recomendações** — Próximos passos baseado em decision

---

## 6. Estrutura do JSON (Reference)

```json
{
  "pilot_start": "2026-07-24",
  "pilot_end": "2026-07-29",
  "personas": ["AI Architect", "Product Ops", "Early Adopter"],
  
  "setup_times": [
    {
      "persona": "AI Architect",
      "start_time": "2026-07-24T09:30:00",
      "end_time": "2026-07-24T09:52:00",
      "duration_minutes": 22.0,
      "target_minutes": 30,
      "status": "✅ PASS"
    }
  ],
  
  "adoption": [
    {
      "day": 1,
      "personas_active": 3,
      "total_personas": 3,
      "adoption_percentage": 100.0,
      "plugin_crashes": 0,
      "notes": "Setup completo",
      "status": "✅ PASS"
    }
  ],
  
  "orphan_detection": [
    {
      "persona": "AI Architect",
      "day": 3,
      "manual_count": 52,
      "plugin_count": 48,
      "false_negatives": 2,
      "false_positives": 1,
      "fn_rate_percentage": 3.85,
      "fp_rate_percentage": 2.08,
      "fn_status": "⚠️ CONDITIONAL",
      "fp_status": "✅ PASS"
    }
  ],
  
  "trust_scores": [
    {
      "persona": "AI Architect",
      "day": 4,
      "avg_diff": 0.15,
      "accuracy_percentage": 92.5,
      "target_accuracy": 85,
      "status": "✅ PASS"
    }
  ],
  
  "api_performance": [
    {
      "day": 1,
      "p50_latency_ms": 285.0,
      "p95_latency_ms": 420.0,
      "p99_latency_ms": 580.0,
      "error_rate_percentage": 0.8,
      "total_calls": 1250,
      "error_calls": 10,
      "target_p95_ms": 500,
      "target_error_rate": 2.0,
      "p95_status": "✅ PASS",
      "error_status": "✅ PASS"
    }
  ],
  
  "business_impact": [
    {
      "persona": "AI Architect",
      "metric_type": "reexplication_hours",
      "before_value": 2.5,
      "after_value": 0.3,
      "reduction_percentage": 88.0,
      "target_reduction": 80.0,
      "status": "✅ PASS"
    }
  ],
  
  "daily_notes": {
    "day_1": {
      "date": "2026-07-24",
      "notes": "Setup completo. Primeiras impressões positivas."
    }
  }
}
```

---

## 7. Troubleshooting

### Erro: "target project doesn't exist"
→ Certifique que os SCRUM issues foram criados (T0.3.5)

### Erro ao ler metrics.json
→ Valide JSON com: `python -m json.tool metrics_data/metrics.json`

### CSV não gerou
→ Verifique permissões: `ls -la metrics_data/`

### RESULTS.md vazio
→ Certifique que pelo menos alguns dados foram coletados em `metrics.json`

---

## 8. Timeline de Referência

| Dia | Data | Atividades | Output |
|-----|------|-----------|--------|
| D1 | 24 jul | Setup times (3), Adoption | setup_times[], adoption[day=1] |
| D2 | 25 jul | Adoption, Orphan manual count | adoption[day=2], orphan_detection[day=2] |
| D3 | 26 jul | Adoption, All manual tests | adoption[day=3], orphan_detection[day=3-6], trust_scores[day=3] |
| D4 | 27 jul | Adoption, API data, Fixes | adoption[day=4], api_performance[day=4] |
| D5 | 28 jul | Final adoption, Business impact | adoption[day=5], business_impact[] |
| D6 | 29 jul | Final call, NPS, Compilation | RESULTS.md, summary.csv |

---

**Status:** 📋 Template pronto
**Próximo Passo:** Executar durante D1 do piloto (24 jul, 9:30 UTC)

