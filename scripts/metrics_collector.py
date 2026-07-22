#!/usr/bin/env python3
"""
APOS Sprint 0.3 Metrics Collector
==================================

Coleta e consolida 6 métricas baseline durante piloto (D1-D6).

Uso:
    python metrics_collector.py --day 1 --action setup
    python metrics_collector.py --day 6 --action finalize
    python metrics_collector.py --day 3 --action report

Estrutura:
    - metrics_D[1-6].json: dados colecionados por dia
    - metrics_summary.csv: rollup diário
    - RESULTS.md: compilação final + Go/No-Go
"""

import json
import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class MetricStatus(Enum):
    """Status de uma métrica."""
    PASS = "✅"
    FAIL = "❌"
    CONDITIONAL = "⚠️"
    PENDING = "📋"


@dataclass
class SetupTimeMetric:
    """Métrica de tempo de setup."""
    persona: str
    start_time: str  # ISO format
    end_time: Optional[str] = None  # ISO format
    duration_minutes: Optional[float] = None
    target_minutes: float = 30.0

    def status(self) -> MetricStatus:
        if self.duration_minutes is None:
            return MetricStatus.PENDING
        return MetricStatus.PASS if self.duration_minutes <= self.target_minutes else MetricStatus.FAIL


@dataclass
class OrphanDetectionMetric:
    """Métrica de detecção de orfas."""
    persona: str
    day: int
    manual_count: Optional[int] = None  # Contagem manual
    plugin_count: Optional[int] = None  # Detectado pelo plugin
    false_negatives: Optional[int] = None  # Orfas que plugin não detectou
    false_positives: Optional[int] = None  # Falsos positivos

    def fn_rate(self) -> Optional[float]:
        if self.manual_count is None or self.false_negatives is None:
            return None
        return (self.false_negatives / self.manual_count * 100) if self.manual_count > 0 else 0.0

    def fp_rate(self) -> Optional[float]:
        if self.plugin_count is None or self.false_positives is None:
            return None
        return (self.false_positives / self.plugin_count * 100) if self.plugin_count > 0 else 0.0


@dataclass
class TrustScoreMetric:
    """Métrica de Trust Score accuracy."""
    persona: str
    day: int
    avg_diff: Optional[float] = None  # Diferença média entre manual vs plugin (target: <0.2)
    accuracy_percentage: Optional[float] = None  # % de acurácia (target: >85%)
    target_accuracy: float = 85.0


@dataclass
class APIPerformanceMetric:
    """Métrica de performance da API."""
    day: int
    p50_latency_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None
    p99_latency_ms: Optional[float] = None
    error_rate_percentage: Optional[float] = None
    total_calls: Optional[int] = None
    error_calls: Optional[int] = None
    target_p95_ms: float = 500.0
    target_error_rate: float = 2.0

    def status_p95(self) -> MetricStatus:
        if self.p95_latency_ms is None:
            return MetricStatus.PENDING
        if self.p95_latency_ms <= self.target_p95_ms:
            return MetricStatus.PASS
        elif self.p95_latency_ms <= 750:
            return MetricStatus.CONDITIONAL
        else:
            return MetricStatus.FAIL


@dataclass
class AdoptionMetric:
    """Métrica de adoption (D1-D7)."""
    day: int
    personas_active: int = 0
    total_personas: int = 3
    plugin_crashes: int = 0
    notes: str = ""

    def status(self) -> MetricStatus:
        if self.day == 7 and self.personas_active == 3:
            return MetricStatus.PASS
        elif self.personas_active == 3:
            return MetricStatus.PASS
        elif self.personas_active >= 2:
            return MetricStatus.CONDITIONAL
        else:
            return MetricStatus.FAIL


@dataclass
class BusinessImpactMetric:
    """Métrica de impacto de negócio (antes/depois)."""
    persona: str
    metric_type: str  # "reexplication_hours", "orphan_rate", "nps"
    before_value: Optional[float] = None
    after_value: Optional[float] = None
    reduction_percentage: Optional[float] = None  # (before - after) / before * 100
    target_reduction: float = 80.0  # % de redução esperada

    def calculate_reduction(self):
        if self.before_value and self.after_value:
            self.reduction_percentage = (self.before_value - self.after_value) / self.before_value * 100


class MetricsCollector:
    """Gerenciador central de coleta de métricas."""

    def __init__(self, sprint_dir: str = None):
        self.sprint_dir = Path(sprint_dir or "docs/releases/R0/sprint-0.3")
        self.data_dir = self.sprint_dir / "metrics_data"
        self.data_dir.mkdir(exist_ok=True)

        # Arquivos de armazenamento
        self.metrics_file = self.data_dir / "metrics.json"
        self.summary_file = self.data_dir / "summary.csv"
        self.results_file = self.sprint_dir / "RESULTS.md"

        # Carregar dados existentes se houver
        self.data = self._load_metrics_data()

    def _load_metrics_data(self) -> Dict:
        """Carrega dados de métricas existentes."""
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "pilot_start": "2026-07-24",
            "pilot_end": "2026-07-29",
            "personas": ["AI Architect", "Product Ops", "Early Adopter"],
            "setup_times": [],
            "orphan_detection": [],
            "trust_scores": [],
            "api_performance": [],
            "adoption": [],
            "business_impact": [],
            "daily_notes": {}
        }

    def _save_metrics_data(self):
        """Salva dados de métricas em JSON."""
        with open(self.metrics_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def record_setup_time(self, persona: str, start_time: str, end_time: str):
        """Registra tempo de setup para persona."""
        from datetime import datetime
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = (end - start).total_seconds() / 60

        metric = {
            "persona": persona,
            "start_time": start_time,
            "end_time": end_time,
            "duration_minutes": round(duration, 2),
            "target_minutes": 30,
            "status": "✅ PASS" if duration <= 30 else "❌ FAIL"
        }
        self.data["setup_times"].append(metric)
        self._save_metrics_data()
        return metric

    def record_orphan_detection(self, persona: str, day: int,
                               manual_count: int, plugin_count: int,
                               false_negatives: int, false_positives: int):
        """Registra métrica de detecção de orfas."""
        fn_rate = (false_negatives / manual_count * 100) if manual_count > 0 else 0
        fp_rate = (false_positives / plugin_count * 100) if plugin_count > 0 else 0

        metric = {
            "persona": persona,
            "day": day,
            "manual_count": manual_count,
            "plugin_count": plugin_count,
            "false_negatives": false_negatives,
            "false_positives": false_positives,
            "fn_rate_percentage": round(fn_rate, 2),
            "fp_rate_percentage": round(fp_rate, 2),
            "fn_status": "✅ PASS" if fn_rate == 0 else "❌ FAIL",
            "fp_status": "✅ PASS" if fp_rate < 5 else "⚠️ CONDITIONAL" if fp_rate < 10 else "❌ FAIL"
        }
        self.data["orphan_detection"].append(metric)
        self._save_metrics_data()
        return metric

    def record_trust_score_accuracy(self, persona: str, day: int,
                                   avg_diff: float, accuracy_percentage: float):
        """Registra métrica de Trust Score accuracy."""
        metric = {
            "persona": persona,
            "day": day,
            "avg_diff": round(avg_diff, 3),
            "accuracy_percentage": round(accuracy_percentage, 2),
            "target_accuracy": 85,
            "status": "✅ PASS" if accuracy_percentage >= 85 else "⚠️ CONDITIONAL" if accuracy_percentage >= 80 else "❌ FAIL"
        }
        self.data["trust_scores"].append(metric)
        self._save_metrics_data()
        return metric

    def record_api_performance(self, day: int,
                              p50_ms: float, p95_ms: float, p99_ms: float,
                              error_rate: float, total_calls: int, error_calls: int):
        """Registra métrica de performance da API."""
        metric = {
            "day": day,
            "p50_latency_ms": round(p50_ms, 2),
            "p95_latency_ms": round(p95_ms, 2),
            "p99_latency_ms": round(p99_ms, 2),
            "error_rate_percentage": round(error_rate, 2),
            "total_calls": total_calls,
            "error_calls": error_calls,
            "target_p95_ms": 500,
            "target_error_rate": 2.0,
            "p95_status": "✅ PASS" if p95_ms <= 500 else "⚠️ CONDITIONAL" if p95_ms <= 750 else "❌ FAIL",
            "error_status": "✅ PASS" if error_rate < 2 else "❌ FAIL"
        }
        self.data["api_performance"].append(metric)
        self._save_metrics_data()
        return metric

    def record_adoption(self, day: int, personas_active: int, crashes: int = 0, notes: str = ""):
        """Registra métrica de adoption."""
        metric = {
            "day": day,
            "personas_active": personas_active,
            "total_personas": 3,
            "adoption_percentage": round(personas_active / 3 * 100, 2),
            "plugin_crashes": crashes,
            "notes": notes,
            "status": "✅ PASS" if personas_active == 3 else "⚠️ CONDITIONAL" if personas_active >= 2 else "❌ FAIL"
        }
        self.data["adoption"].append(metric)
        self._save_metrics_data()
        return metric

    def record_daily_notes(self, day: int, notes: str):
        """Registra notas diárias."""
        self.data["daily_notes"][f"day_{day}"] = {
            "date": self._day_to_date(day),
            "notes": notes
        }
        self._save_metrics_data()

    def record_business_impact(self, persona: str, metric_type: str,
                              before_value: float, after_value: float):
        """Registra métrica de impacto de negócio."""
        reduction = (before_value - after_value) / before_value * 100 if before_value > 0 else 0

        metric = {
            "persona": persona,
            "metric_type": metric_type,
            "before_value": round(before_value, 2),
            "after_value": round(after_value, 2),
            "reduction_percentage": round(reduction, 2),
            "target_reduction": 80,
            "status": "✅ PASS" if reduction >= 80 else "⚠️ CONDITIONAL" if reduction >= 70 else "❌ FAIL"
        }
        self.data["business_impact"].append(metric)
        self._save_metrics_data()
        return metric

    def _day_to_date(self, day: int) -> str:
        """Converte número do dia (1-6) para data (2026-07-24 a 2026-07-29)."""
        pilot_start = datetime(2026, 7, 24)
        date = pilot_start + timedelta(days=day - 1)
        return date.strftime("%Y-%m-%d")

    def generate_summary_csv(self) -> Path:
        """Gera CSV com resumo diário de métricas."""
        with open(self.summary_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Header
            writer.writerow([
                "Dia", "Data",
                "Setup Time (min)", "Avg Setup Status",
                "Adoption (personas)", "Adoption Status",
                "Plugin Crashes",
                "API P95 (ms)", "API P95 Status",
                "API Error Rate (%)", "API Error Status",
                "Orphan FN Rate (%)", "Orphan FP Rate (%)",
                "Trust Score Accuracy (%)",
                "Notes"
            ])

            # Dados por dia
            for day in range(1, 7):
                setup_times = [m for m in self.data.get("setup_times", []) if "duration_minutes" in m]
                setup_avg = sum(m["duration_minutes"] for m in setup_times) / len(setup_times) if setup_times else None
                setup_status = "✅" if setup_avg and setup_avg <= 30 else "❌" if setup_avg else "📋"

                adoption = next((a for a in self.data.get("adoption", []) if a["day"] == day), None)
                adoption_count = adoption["personas_active"] if adoption else "—"
                adoption_status = adoption["status"] if adoption else "📋"
                crashes = adoption["plugin_crashes"] if adoption else 0

                api_perf = next((a for a in self.data.get("api_performance", []) if a["day"] == day), None)
                p95 = api_perf["p95_latency_ms"] if api_perf else "—"
                p95_status = api_perf["p95_status"] if api_perf else "📋"
                error_rate = api_perf["error_rate_percentage"] if api_perf else "—"
                error_status = api_perf["error_status"] if api_perf else "📋"

                orphans = [o for o in self.data.get("orphan_detection", []) if o["day"] == day]
                avg_fn_rate = sum(o["fn_rate_percentage"] for o in orphans) / len(orphans) if orphans else "—"
                avg_fp_rate = sum(o["fp_rate_percentage"] for o in orphans) / len(orphans) if orphans else "—"

                trust_scores = [t for t in self.data.get("trust_scores", []) if t["day"] == day]
                avg_accuracy = sum(t["accuracy_percentage"] for t in trust_scores) / len(trust_scores) if trust_scores else "—"

                notes = self.data.get("daily_notes", {}).get(f"day_{day}", {}).get("notes", "")

                writer.writerow([
                    day,
                    self._day_to_date(day),
                    f"{setup_avg:.1f}" if setup_avg else "—",
                    setup_status,
                    adoption_count,
                    adoption_status,
                    crashes,
                    f"{p95:.0f}" if isinstance(p95, (int, float)) else p95,
                    p95_status,
                    f"{error_rate:.1f}" if isinstance(error_rate, (int, float)) else error_rate,
                    error_status,
                    f"{avg_fn_rate:.1f}" if isinstance(avg_fn_rate, (int, float)) else avg_fn_rate,
                    f"{avg_fp_rate:.1f}" if isinstance(avg_fp_rate, (int, float)) else avg_fp_rate,
                    f"{avg_accuracy:.1f}" if isinstance(avg_accuracy, (int, float)) else avg_accuracy,
                    notes[:50] + "..." if len(notes) > 50 else notes
                ])

        return self.summary_file

    def generate_results_markdown(self) -> Path:
        """Gera relatório RESULTS.md com Go/No-Go decision."""
        # Calcular estatísticas
        setup_times = [m["duration_minutes"] for m in self.data.get("setup_times", []) if "duration_minutes" in m]
        avg_setup = sum(setup_times) / len(setup_times) if setup_times else None

        adoption_final = self.data.get("adoption", [])[-1] if self.data.get("adoption") else None

        api_perf_final = self.data.get("api_performance", [])[-1] if self.data.get("api_performance") else None

        orphans = self.data.get("orphan_detection", [])
        avg_fn_rate = sum(o["fn_rate_percentage"] for o in orphans) / len(orphans) if orphans else None
        avg_fp_rate = sum(o["fp_rate_percentage"] for o in orphans) / len(orphans) if orphans else None

        trust_final = self.data.get("trust_scores", [])
        avg_accuracy = sum(t["accuracy_percentage"] for t in trust_final) / len(trust_final) if trust_final else None

        business_impact = self.data.get("business_impact", [])

        # Decisão Go/No-Go
        go_pass_count = 0
        total_high_priority = 0

        criteria = []

        # Setup time
        if avg_setup and avg_setup <= 30:
            criteria.append(("Setup time <30 min", "✅ PASS", avg_setup))
            go_pass_count += 1
        else:
            criteria.append(("Setup time <30 min", "❌ FAIL", avg_setup))
        total_high_priority += 1

        # Adoption
        if adoption_final and adoption_final["personas_active"] == 3:
            criteria.append(("Adoption 3/3 Dia 7", "✅ PASS", adoption_final["personas_active"]))
            go_pass_count += 1
        else:
            criteria.append(("Adoption 3/3 Dia 7", "❌ FAIL", adoption_final["personas_active"] if adoption_final else 0))
        total_high_priority += 1

        # Detecção de orfas (FN)
        if avg_fn_rate is not None and avg_fn_rate == 0:
            criteria.append(("Orphan Detection 0% FN", "✅ PASS", f"{avg_fn_rate:.2f}%"))
            go_pass_count += 1
        else:
            criteria.append(("Orphan Detection 0% FN", "❌ FAIL" if (avg_fn_rate and avg_fn_rate > 0) else "📋 PENDING", f"{avg_fn_rate:.2f}%" if avg_fn_rate is not None else "N/A"))
        total_high_priority += 1

        # Detecção de orfas (FP)
        if avg_fp_rate is not None and avg_fp_rate < 5:
            criteria.append(("Orphan Detection <5% FP", "✅ PASS", f"{avg_fp_rate:.2f}%"))
            go_pass_count += 1
        else:
            criteria.append(("Orphan Detection <5% FP", "⚠️ CONDITIONAL" if (avg_fp_rate and avg_fp_rate < 10) else "❌ FAIL" if avg_fp_rate else "📋 PENDING", f"{avg_fp_rate:.2f}%" if avg_fp_rate is not None else "N/A"))
        total_high_priority += 1

        # API Performance
        if api_perf_final and api_perf_final["p95_latency_ms"] <= 500:
            criteria.append(("API P95 <500ms", "✅ PASS", f"{api_perf_final['p95_latency_ms']:.0f}ms"))
            go_pass_count += 1
        else:
            criteria.append(("API P95 <500ms", "⚠️ CONDITIONAL" if (api_perf_final and api_perf_final["p95_latency_ms"] <= 750) else "❌ FAIL" if api_perf_final else "📋 PENDING", f"{api_perf_final['p95_latency_ms']:.0f}ms" if api_perf_final else "N/A"))
        total_high_priority += 1

        # Trust Score Accuracy
        if avg_accuracy is not None and avg_accuracy >= 85:
            criteria.append(("Trust Score >85% accuracy", "✅ PASS", f"{avg_accuracy:.2f}%"))
            go_pass_count += 1
        else:
            criteria.append(("Trust Score >85% accuracy", "⚠️ CONDITIONAL" if (avg_accuracy and avg_accuracy >= 80) else "❌ FAIL" if avg_accuracy else "📋 PENDING", f"{avg_accuracy:.2f}%" if avg_accuracy is not None else "N/A"))

        # Decisão
        if go_pass_count >= 5:
            decision = "🟢 GREEN - SHIP MVP"
            rationale = "MVP atinge todos critérios high-priority. Recomendação: Ship R0-MVP e iniciar R1 planning."
        elif go_pass_count >= 4:
            decision = "🟡 YELLOW - ITERATE 1 WEEK"
            rationale = "1+ critério marginal. Recomendação: Fix e re-test em 1 semana antes de ship."
        else:
            decision = "🔴 RED - BACK TO DRAWING BOARD"
            rationale = "<4 critérios high-priority passos. Recomendação: Re-arquiteurar e planejar R0.3.1."

        # Gerar markdown
        content = f"""# Sprint 0.3 - Resultados Finais & Go/No-Go Decision

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Status:** 📊 Análise Completa
**Piloto Duração:** 6 dias (2026-07-24 a 2026-07-29)
**Personas:** 3 (AI Architect, Product Ops, Early Adopter)

---

## 1. Go/No-Go Decision

### Decisão Final: {decision}

**Rationale:** {rationale}

---

## 2. Critérios de Sucesso

| Criterio | Status | Resultado | Alvo |
|----------|--------|-----------|------|
"""

        for criterion, status, result in criteria:
            alvo = {
                "Setup time <30 min": "<30 min",
                "Adoption 3/3 Dia 7": "3/3 personas",
                "Orphan Detection 0% FN": "0%",
                "Orphan Detection <5% FP": "<5%",
                "API P95 <500ms": "<500ms",
                "Trust Score >85% accuracy": ">85%"
            }.get(criterion, "Ver alvo")
            content += f"| {criterion} | {status} | {result} | {alvo} |\n"

        content += f"""
---

## 3. Métricas Detalhadas

### 3.1 Setup Time
"""

        if setup_times:
            content += f"""
**Resultado:** {len(setup_times)} personas onboarded
**Tempo Médio:** {avg_setup:.1f} min
**Alvo:** <30 min
**Status:** {'✅ PASS' if avg_setup <= 30 else '❌ FAIL'}

| Persona | Duração (min) | Status |
|---------|---------------|--------|
"""
            for metric in self.data.get("setup_times", []):
                content += f"| {metric['persona']} | {metric['duration_minutes']:.1f} | {metric['status']} |\n"
        else:
            content += "\n**Status:** 📋 Dados ainda não coletados\n"

        content += f"""
### 3.2 Adoption (D1-D7)

| Dia | Data | Personas Ativas | Status | Crashes | Notes |
|-----|------|-----------------|--------|---------|-------|
"""
        for day in range(1, 7):
            adoption = next((a for a in self.data.get("adoption", []) if a["day"] == day), None)
            if adoption:
                content += f"| {day} | {self._day_to_date(day)} | {adoption['personas_active']}/3 | {adoption['status']} | {adoption['plugin_crashes']} | {adoption['notes']} |\n"
            else:
                content += f"| {day} | {self._day_to_date(day)} | — | 📋 | — | — |\n"

        content += f"""
### 3.3 Detecção de Orfas

**Accuracy Média:**
- False Negatives: {f"{avg_fn_rate:.2f}%" if avg_fn_rate is not None else "📋 Pendente"}%
- False Positives: {f"{avg_fp_rate:.2f}%" if avg_fp_rate is not None else "📋 Pendente"}%

| Persona | Dia | Manual | Plugin | FN | FN% | FP | FP% |
|---------|-----|--------|--------|----|----|----|----|
"""

        for metric in self.data.get("orphan_detection", []):
            content += f"| {metric['persona']} | {metric['day']} | {metric['manual_count']} | {metric['plugin_count']} | {metric['false_negatives']} | {metric['fn_rate_percentage']:.2f}% | {metric['false_positives']} | {metric['fp_rate_percentage']:.2f}% |\n"

        content += f"""
### 3.4 API Performance

**P95 Latência:** {f"{api_perf_final['p95_latency_ms']:.0f}ms" if api_perf_final else "📋 Pendente"}
**Alvo:** <500ms
**Status:** {api_perf_final['p95_status'] if api_perf_final else "📋 Pendente"}

| Dia | P50 (ms) | P95 (ms) | P99 (ms) | Error Rate (%) | Status |
|-----|----------|----------|----------|----------------|--------|
"""

        for metric in self.data.get("api_performance", []):
            content += f"| {metric['day']} | {metric['p50_latency_ms']:.0f} | {metric['p95_latency_ms']:.0f} | {metric['p99_latency_ms']:.0f} | {metric['error_rate_percentage']:.2f}% | {metric['p95_status']} |\n"

        content += f"""
### 3.5 Trust Score Accuracy

**Accuracy Média:** {f"{avg_accuracy:.2f}%" if avg_accuracy is not None else "📋 Pendente"}
**Alvo:** >85%
**Status:** {trust_final[0]['status'] if trust_final else "📋 Pendente"}

| Persona | Dia | Avg Diff | Accuracy (%) | Status |
|---------|-----|----------|--------------|--------|
"""

        for metric in self.data.get("trust_scores", []):
            content += f"| {metric['persona']} | {metric['day']} | {metric['avg_diff']:.3f} | {metric['accuracy_percentage']:.2f}% | {metric['status']} |\n"

        content += """
### 3.6 Business Impact

"""

        if business_impact:
            content += """| Persona | Métrica | Before | After | Redução (%) | Status |
|---------|---------|--------|-------|-------------|--------|
"""
            for metric in business_impact:
                content += f"| {metric['persona']} | {metric['metric_type']} | {metric['before_value']} | {metric['after_value']} | {metric['reduction_percentage']:.1f}% | {metric['status']} |\n"
        else:
            content += "**Status:** 📋 Dados ainda não coletados\n"

        content += f"""
---

## 4. Notas Diárias & Aprendizados

"""

        for day in range(1, 7):
            notes = self.data.get("daily_notes", {}).get(f"day_{day}", {}).get("notes", "")
            if notes:
                content += f"\n### Dia {day} ({self._day_to_date(day)})\n{notes}\n"

        content += f"""
---

## 5. Recomendações Próximos Passos

### Se GREEN (Ship MVP):
1. ✅ Merge PR para main
2. ✅ Deploy para staging
3. ✅ Iniciar R1 planning (Feature Expansion, Enterprise Features)
4. ✅ Notificar personas: "MVP approved para produção"

### Se YELLOW (Iterate 1 week):
1. ⚠️ Priorizar fix de marginal items
2. ⚠️ Re-test em 1 semana
3. ⚠️ Documenta blockers em RISK_MITIGATION.md
4. ⚠️ Adjust R1 timeline +1 semana

### Se RED (Back to Drawing Board):
1. ❌ RCA (Root Cause Analysis) em critérios que falharam
2. ❌ Escalate para Jader + stakeholders
3. ❌ Re-arquiteurar (talvez usar diferente approach)
4. ❌ Plan R0.3.1 iteração

---

## 6. Anexos

### Dados Brutos
- 📊 `metrics_data/metrics.json` — Dados estruturados de todas métricas
- 📈 `metrics_data/summary.csv` — Rollup diário para análise

### Documentação
- 📋 `METRICS_BASELINE.md` — Definição original de métricas
- 📋 `PILOT_PLAN.md` — Plano executivo do piloto
- 📋 `STATUS.md` — Status daily durant piloto

---

**Compilado por:** Claude Code Metrics Collector
**Version:** 1.0
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}

"""

        with open(self.results_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return self.results_file

    def print_summary(self):
        """Imprime resumo de métricas coletadas."""
        safe_print("\n" + "="*70)
        safe_print("APOS Sprint 0.3 - Metrics Summary")
        safe_print("="*70)

        # Setup times
        setup_times = [m["duration_minutes"] for m in self.data.get("setup_times", []) if "duration_minutes" in m]
        if setup_times:
            avg = sum(setup_times) / len(setup_times)
            status = "[PASS]" if avg <= 30 else "[FAIL]"
            safe_print(f"\nSetup Time (avg): {avg:.1f} min (target: <30 min) - {status}")

        # Adoption
        adoption = self.data.get("adoption", [])
        if adoption:
            latest = adoption[-1]
            safe_print(f"Adoption (latest): {latest['personas_active']}/3 - {latest['status']}")

        # API Performance
        api = self.data.get("api_performance", [])
        if api:
            latest = api[-1]
            safe_print(f"API P95 Latency (latest): {latest['p95_latency_ms']:.0f}ms (target: <500ms) - {latest['p95_status']}")

        # Orphan Detection
        orphans = self.data.get("orphan_detection", [])
        if orphans:
            avg_fn = sum(o["fn_rate_percentage"] for o in orphans) / len(orphans)
            avg_fp = sum(o["fp_rate_percentage"] for o in orphans) / len(orphans)
            safe_print(f"Orphan Detection: FN={avg_fn:.2f}% (target: 0%), FP={avg_fp:.2f}% (target: <5%)")

        # Trust Score
        trust = self.data.get("trust_scores", [])
        if trust:
            avg_acc = sum(t["accuracy_percentage"] for t in trust) / len(trust)
            safe_print(f"Trust Score Accuracy: {avg_acc:.2f}% (target: >85%)")

        safe_print("\n" + "="*70 + "\n")


def safe_print(msg: str):
    """Print com fallback para caracteres ASCII."""
    msg = msg.replace("✅", "[PASS]")
    msg = msg.replace("❌", "[FAIL]")
    msg = msg.replace("⚠️", "[WARN]")
    msg = msg.replace("📋", "[TODO]")
    msg = msg.replace("🟢", "[GREEN]")
    msg = msg.replace("🟡", "[YELLOW]")
    msg = msg.replace("🔴", "[RED]")
    print(msg)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Collect and analyze APOS Sprint 0.3 metrics")
    parser.add_argument("--day", type=int, help="Pilot day (1-6)")
    parser.add_argument("--action", choices=["setup", "record", "report", "finalize"],
                       help="Action to perform")
    parser.add_argument("--persona", help="Persona name (for setup time)")
    parser.add_argument("--start-time", help="Setup start time (ISO format)")
    parser.add_argument("--end-time", help="Setup end time (ISO format)")
    parser.add_argument("--adoption", type=int, help="Number of active personas")
    parser.add_argument("--crashes", type=int, default=0, help="Number of plugin crashes")
    parser.add_argument("--notes", help="Daily notes")

    args = parser.parse_args()

    collector = MetricsCollector()

    if args.action == "setup":
        if args.persona and args.start_time and args.end_time:
            result = collector.record_setup_time(args.persona, args.start_time, args.end_time)
            safe_print(f"[PASS] Setup recorded: {result['persona']} - {result['duration_minutes']:.1f} min")
        else:
            safe_print("[FAIL] Requires: --persona, --start-time, --end-time")

    elif args.action == "record" and args.day:
        if args.adoption is not None:
            result = collector.record_adoption(args.day, args.adoption, args.crashes, args.notes or "")
            safe_print(f"[PASS] Adoption recorded (Day {args.day}): {result['personas_active']}/3 active")

        if args.notes:
            collector.record_daily_notes(args.day, args.notes)
            safe_print(f"[PASS] Daily notes recorded (Day {args.day})")

    elif args.action == "report":
        collector.generate_summary_csv()
        safe_print(f"[PASS] Summary CSV generated: {collector.summary_file}")
        collector.print_summary()

    elif args.action == "finalize":
        collector.generate_summary_csv()
        collector.generate_results_markdown()
        safe_print(f"[PASS] Final report generated: {collector.results_file}")
        collector.print_summary()

    else:
        collector.print_summary()


if __name__ == "__main__":
    main()
