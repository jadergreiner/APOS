"""
APOS Evaluation Harness — Harness de Avaliação (Sprint 0.7, EVALUATION_HARNESS.md)

Fornece infraestrutura para testar, avaliar e comparar capabilities e agentes
de forma sistemática: testes unitários, integração, regressão, A/B e qualidade,
com coleta de métricas, matriz de confusão, histogramas e geração de relatórios.
"""

from __future__ import annotations

import json
import math
import statistics
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from apos.harness.capability_harness import (
    CapabilityHarness,
    CapabilityRequest,
    ExecutionResult,
)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────


class EvaluationType(str, Enum):
    """Tipos de avaliação suportados.

    - UNIT: Teste de capability isolada com dependências mockadas.
    - INTEGRATION: Teste de chain com dependências reais.
    - REGRESSION: Comparação contra baseline histórico.
    - AB_TEST: Comparação lado a lado de duas versões.
    - QUALITY: Análise estatística de confiabilidade e performance.
    """
    UNIT = "unit"
    INTEGRATION = "integration"
    REGRESSION = "regression"
    AB_TEST = "ab"
    QUALITY = "quality"


class EvaluationStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


# ──────────────────────────────────────────────
# TestCase
# ──────────────────────────────────────────────


@dataclass
class TestCase:
    """Caso de teste individual.

    Attributes:
        id: ID único (ex: "tc-042").
        name: Nome descritivo.
        description: Descrição do cenário.
        input: Parâmetros de entrada.
        expected_output: Saída esperada (se conhecida).
        expected_effects: Efeitos esperados no KG.
        tags: Tags para categorização.
        priority: Prioridade (1=crítica, 5=baixa).
        category: Categoria do teste.
    """
    id: str = ""
    name: str = ""
    description: str = ""
    input: dict = field(default_factory=dict)
    expected_output: Optional[dict] = None
    expected_effects: Optional[list[dict]] = None
    tags: list[str] = field(default_factory=list)
    priority: int = 3
    category: str = "general"


@dataclass
class TestCaseResult:
    """Resultado de um caso de teste individual.

    Attributes:
        test_case_id: ID do caso.
        name: Nome descritivo.
        status: passed | failed | error | timeout.
        input: Parâmetros de entrada usados.
        output: Saída real.
        expected_output: Saída esperada.
        match: True se output == expected_output.
        error: Mensagem de erro.
        latency_ms: Tempo de execução.
        kg_ops: Operações no KG.
        context_tokens: Tokens de contexto.
        details: Detalhes adicionais.
    """
    test_case_id: str = ""
    name: str = ""
    status: str = "passed"
    input: dict = field(default_factory=dict)
    output: Optional[dict] = None
    expected_output: Optional[dict] = None
    match: Optional[bool] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    kg_ops: int = 0
    context_tokens: int = 0
    details: dict = field(default_factory=dict)


# ──────────────────────────────────────────────
# Evaluation Run / Result / Config
# ──────────────────────────────────────────────


@dataclass
class EvaluationRun:
    """Definição completa de uma execução de avaliação.

    Attributes:
        id: UUID gerado pelo sistema.
        type: Tipo de avaliação.
        capability_id: Capability ou chain alvo.
        version_a: Versão A (geralmente a nova).
        version_b: Versão B (baseline, para A/B).
        test_cases: Casos de teste.
        config: Configuração da avaliação.
        created_at: ISO 8601.
        status: Status atual.
    """
    id: str = ""
    type: EvaluationType = EvaluationType.UNIT
    capability_id: str = ""
    version_a: str = ""
    version_b: Optional[str] = None
    test_cases: list[TestCase] = field(default_factory=list)
    config: "EvaluationConfig" = field(default_factory=lambda: EvaluationConfig())
    created_at: str = ""
    status: EvaluationStatus = EvaluationStatus.PENDING

    def __post_init__(self):
        if not self.id:
            self.id = f"eval-run-{uuid.uuid4().hex[:12]}"
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()


@dataclass
class EvaluationResult:
    """Resultado consolidado de uma avaliação.

    Attributes:
        run_id: Referência ao EvaluationRun.
        status: passed | failed | degraded | inconclusive.
        summary: Resumo de métricas.
        details: Resultados por caso de teste.
        comparison: Comparação com baseline (se aplicável).
        report_url: Link para o relatório completo.
        duration_seconds: Duração total da avaliação.
        completed_at: ISO 8601.
    """
    run_id: str = ""
    status: str = "passed"
    summary: "MetricsSummary" = field(default_factory=lambda: MetricsSummary())
    details: list[TestCaseResult] = field(default_factory=list)
    comparison: Optional[ComparisonResult] = None
    report_url: str = ""
    duration_seconds: float = 0.0
    completed_at: str = ""


# ──────────────────────────────────────────────
# Metrics
# ──────────────────────────────────────────────


@dataclass
class MetricsSummary:
    """Resumo agregado de métricas de uma avaliação.

    Conforme EVALUATION_HARNESS.md seção 4.2.
    """
    run_id: str = ""
    capability_id: str = ""
    num_tests: int = 0
    num_passed: int = 0
    num_failed: int = 0
    num_timeout: int = 0

    # Acurácia e qualidade
    accuracy: float = 0.0
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None

    # Performance
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0
    latency_p99_ms: float = 0.0
    latency_mean_ms: float = 0.0
    latency_min_ms: float = 0.0
    latency_max_ms: float = 0.0
    latency_stddev_ms: float = 0.0

    # Erros
    error_rate: float = 0.0
    timeout_rate: float = 0.0
    retry_rate: float = 0.0
    error_distribution: dict[str, int] = field(default_factory=dict)

    # KG e contexto
    coverage: Optional[float] = None
    consistency: Optional[float] = None
    quality_score: Optional[float] = None
    kg_ops_total: int = 0
    context_tokens_avg: float = 0.0

    # Estado
    status: str = "passed"
    completed_at: str = ""
    duration_seconds: float = 0.0


@dataclass
class ConfusionMatrix:
    """Matriz de confusão para avaliação de classificação.

    Conforme EVALUATION_HARNESS.md seção 4.3.
    """
    true_positives: int = 0
    true_negatives: int = 0
    false_positives: int = 0
    false_negatives: int = 0

    @property
    def precision(self) -> float:
        denominator = self.true_positives + self.false_positives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def recall(self) -> float:
        denominator = self.true_positives + self.false_negatives
        return self.true_positives / denominator if denominator > 0 else 0.0

    @property
    def f1(self) -> float:
        p = self.precision
        r = self.recall
        return 2 * (p * r) / (p + r) if (p + r) > 0 else 0.0

    @property
    def accuracy(self) -> float:
        total = self.true_positives + self.true_negatives + self.false_positives + self.false_negatives
        return (self.true_positives + self.true_negatives) / total if total > 0 else 0.0


@dataclass
class LatencyHistogram:
    """Histograma de latência para análise de performance.

    Conforme EVALUATION_HARNESS.md seção 4.4.
    Buckets padrão (ms): 0-50, 50-100, 100-200, 200-500, 500-1000, 1000-2000, 2000-5000, 5000+
    """
    buckets: dict[str, int] = field(default_factory=lambda: {
        "0-50": 0, "50-100": 0, "100-200": 0, "200-500": 0,
        "500-1000": 0, "1000-2000": 0, "2000-5000": 0, "5000+": 0,
    })
    p50_ms: float = 0.0
    p95_ms: float = 0.0
    p99_ms: float = 0.0
    mean_ms: float = 0.0
    stddev_ms: float = 0.0
    min_ms: float = 0.0
    max_ms: float = 0.0
    sample_count: int = 0

    @classmethod
    def from_values(cls, values: list[float]) -> LatencyHistogram:
        """Constrói histograma a partir de lista de valores de latência."""
        h = cls()
        if not values:
            return h

        sorted_vals = sorted(values)
        n = len(sorted_vals)
        h.sample_count = n
        h.min_ms = sorted_vals[0]
        h.max_ms = sorted_vals[-1]
        h.mean_ms = sum(sorted_vals) / n
        h.p50_ms = sorted_vals[int(n * 0.50)]
        h.p95_ms = sorted_vals[int(n * 0.95)]
        h.p99_ms = sorted_vals[int(n * 0.99)]
        h.stddev_ms = statistics.stdev(sorted_vals) if n > 1 else 0.0

        bucket_defs = [(0, 50), (50, 100), (100, 200), (200, 500),
                       (500, 1000), (1000, 2000), (2000, 5000)]
        bucket_labels = ["0-50", "50-100", "100-200", "200-500",
                         "500-1000", "1000-2000", "2000-5000", "5000+"]

        for v in sorted_vals:
            placed = False
            for i, (lo, hi) in enumerate(bucket_defs):
                if lo <= v < hi:
                    h.buckets[bucket_labels[i]] += 1
                    placed = True
                    break
            if not placed:
                h.buckets["5000+"] += 1

        return h


class CompositeMetrics:
    """Métricas compostas que combinam múltiplas métricas base.

    Conforme EVALUATION_HARNESS.md seção 4.5.
    """

    @staticmethod
    def overall_quality(summary: MetricsSummary) -> float:
        """Score composto de qualidade (0.0 a 1.0)."""
        w_accuracy = 0.30
        w_latency = 0.20
        w_errors = 0.25
        w_coverage = 0.15
        w_consist = 0.10

        accuracy_score = summary.accuracy
        latency_score = 1.0 - (summary.latency_p95_ms / 10000.0)
        error_score = 1.0 - summary.error_rate
        coverage_score = summary.coverage if summary.coverage else 0.5
        consist_score = summary.consistency if summary.consistency else 0.5

        return (
            w_accuracy * accuracy_score
            + w_latency * max(0.0, min(1.0, latency_score))
            + w_errors * error_score
            + w_coverage * coverage_score
            + w_consist * consist_score
        )

    @staticmethod
    def performance_index(summary: MetricsSummary) -> float:
        """Índice de performance (0.0 a 1.0)."""
        return 1.0 - (
            0.4 * (summary.latency_p95_ms / 10000.0)
            + 0.3 * summary.error_rate
            + 0.3 * summary.timeout_rate
        )


# ──────────────────────────────────────────────
# A/B Testing
# ──────────────────────────────────────────────


@dataclass
class ABTestEvaluation:
    """Configuração de avaliação A/B.

    Conforme EVALUATION_HARNESS.md seção 5.1.
    """
    id: str = ""
    capability_id: str = ""
    version_a_label: str = ""
    version_b_label: str = ""
    test_cases: list[TestCase] = field(default_factory=list)
    parallel: bool = True
    num_iterations: int = 1
    metrics: list[str] = field(default_factory=lambda: ["accuracy", "latency_p95", "error_rate"])
    significance_level: float = 0.05
    auto_promote: bool = False

    def __post_init__(self):
        if not self.id:
            self.id = f"eval-ab-{uuid.uuid4().hex[:8]}"


@dataclass
class ComparisonResult:
    """Resultado da comparação entre duas versões.

    Conforme EVALUATION_HARNESS.md seção 5.3.
    """
    version_a: str = ""
    version_b: str = ""
    summary_a: MetricsSummary = field(default_factory=MetricsSummary)
    summary_b: MetricsSummary = field(default_factory=MetricsSummary)
    deltas: dict[str, float] = field(default_factory=dict)
    verdict: str = "draw"
    significance: dict[str, float] = field(default_factory=dict)
    recommended: str = ""
    reasons: list[str] = field(default_factory=list)


@dataclass
class StatisticalTest:
    """Resultado de teste estatístico para comparação A/B.

    Conforme EVALUATION_HARNESS.md seção 5.6.
    """
    test_type: str = "paired_t"
    statistic: float = 0.0
    p_value: float = 1.0
    significant: bool = False
    effect_size: float = 0.0
    confidence_interval: tuple[float, float] = (0.0, 0.0)


# ──────────────────────────────────────────────
# Report
# ──────────────────────────────────────────────


@dataclass
class MetricsPoint:
    """Um ponto no histórico de métricas."""
    timestamp: str = ""
    accuracy: float = 0.0
    latency_p95_ms: float = 0.0
    error_rate: float = 0.0
    coverage: Optional[float] = None


@dataclass
class EvaluationReport:
    """Relatório completo de uma avaliação.

    Conforme EVALUATION_HARNESS.md seção 6.1.
    """
    run_id: str = ""
    type: EvaluationType = EvaluationType.UNIT
    capability_id: str = ""
    title: str = ""
    created_at: str = ""
    config: 'EvaluationConfig' = field(default_factory=dict)
    summary: MetricsSummary = field(default_factory=MetricsSummary)
    verdict: str = "passed"
    verdict_reason: str = ""
    test_results: list[TestCaseResult] = field(default_factory=list)
    comparison: Optional[ComparisonResult] = None
    metrics_over_time: Optional[list[MetricsPoint]] = None
    duration_seconds: float = 0.0
    dataset_version: str = ""
    environment: str = "local"
    executed_by: str = ""
    report_url: str = ""
    raw_data_url: str = ""
    log_url: str = ""

    def to_markdown(self) -> str:
        """Gera versão Markdown do relatório."""
        lines = [
            f"# Relatório de Avaliação: {self.capability_id}",
            f"",
            f"**Run ID:** {self.run_id}  ",
            f"**Tipo:** {self.type.value}  ",
            f"**Data:** {self.created_at}  ",
            f"**Veredito:** {self.verdict}  ",
            f"",
            f"---",
            f"",
            f"## Sumário Executivo",
            f"",
            f"| Métrica | Valor |",
            f"|---------|:-----:|",
            f"| Accuracy | {self.summary.accuracy:.3f} |",
            f"| Latência P95 | {self.summary.latency_p95_ms:.1f}ms |",
            f"| Error Rate | {self.summary.error_rate:.3f} |",
            f"| Testes | {self.summary.num_passed}/{self.summary.num_tests} passaram |",
            f"",
            f"**Veredito:** {self.verdict_reason}",
        ]
        return "\n".join(lines)


@dataclass
class EvaluationDashboard:
    """Dashboard consolidado de avaliações.

    Conforme EVALUATION_HARNESS.md seção 6.3.
    """
    total_runs: int = 0
    passed_runs: int = 0
    failed_runs: int = 0
    degraded_runs: int = 0
    pass_rate: float = 0.0
    accuracy_trend: list[MetricsPoint] = field(default_factory=list)
    latency_trend: list[MetricsPoint] = field(default_factory=list)
    error_trend: list[MetricsPoint] = field(default_factory=list)
    by_capability: dict[str, CapabilityHealth] = field(default_factory=dict)
    active_alerts: list[EvaluationAlert] = field(default_factory=list)
    recent_runs: list[EvaluationReport] = field(default_factory=list)


@dataclass
class CapabilityHealth:
    """Saúde consolidada de uma capability."""
    capability_id: str = ""
    last_run_status: str = ""
    last_run_at: str = ""
    running_average_accuracy: float = 0.0
    running_average_latency_p95: float = 0.0
    current_accuracy: float = 0.0
    accuracy_trend: str = "stable"
    alert_count: int = 0


@dataclass
class EvaluationAlert:
    """Alerta gerado por condição de avaliação.

    Conforme EVALUATION_HARNESS.md seção 6.4.
    """
    id: str = ""
    severity: str = "medium"
    metric: str = ""
    current_value: float = 0.0
    threshold: float = 0.0
    message: str = ""
    capability_id: str = ""
    created_at: str = ""
    acknowledged: bool = False
    resolved_at: Optional[str] = None


# ──────────────────────────────────────────────
# Evaluation Configs
# ──────────────────────────────────────────────


@dataclass
class EvaluationConfig:
    """Configuração específica do Evaluation Harness.

    Conforme EVALUATION_HARNESS.md seção 8.1.
    """
    # Timeouts
    test_timeout_seconds: int = 120
    ab_test_timeout_seconds: int = 300
    quality_timeout_seconds: int = 600

    # Concorrência
    max_concurrent_tests: int = 3
    parallel_ab_execution: bool = True

    # Métricas
    collect_detailed_metrics: bool = True
    track_kg_operations: bool = True
    track_context_tokens: bool = True
    latency_histogram_buckets: list[int] = field(
        default_factory=lambda: [50, 100, 200, 500, 1000, 2000, 5000]
    )

    # Report
    auto_generate_report: bool = True
    report_format: str = "markdown"
    archive_results: bool = True

    # Thresholds
    default_accuracy_threshold: float = 0.80
    default_latency_p95_threshold_ms: float = 5000.0
    default_error_rate_threshold: float = 0.10
    regression_max_degradation: float = 0.05

    # A/B
    ab_significance_level: float = 0.05
    ab_min_effect_size: float = 0.01
    ab_num_iterations_default: int = 3

    # Dataset
    dataset_version: str = "latest"
    auto_load_dataset: bool = True
    mock_registry_enabled: bool = True


@dataclass
class UnitEvaluation:
    """Configuração de avaliação unitária."""
    id: str = ""
    capability_id: str = ""
    test_cases: list[TestCase] = field(default_factory=list)
    mock_kg: bool = True
    mock_context: bool = True
    expected_output: Optional[dict] = None
    expected_effects: Optional[list[dict]] = None


@dataclass
class IntegrationEvaluation:
    """Configuração de avaliação de integração."""
    id: str = ""
    chain_id: str = ""
    test_cases: list[TestCase] = field(default_factory=list)
    use_real_kg: bool = True
    use_real_context: bool = True
    validate_effects: bool = True
    teardown_cleanup: bool = True


@dataclass
class RegressionEvaluation:
    """Configuração de avaliação de regressão."""
    id: str = ""
    baseline_id: str = ""
    test_suite: list[TestCase] = field(default_factory=list)
    metrics_threshold: dict[str, float] = field(default_factory=dict)
    compare_to_baseline: bool = True
    auto_fail_on_regression: bool = True


@dataclass
class QualityEvaluation:
    """Configuração de avaliação de qualidade."""
    id: str = ""
    capability_id: str = ""
    num_runs: int = 100
    test_cases: list[TestCase] = field(default_factory=list)
    metrics_to_collect: list[str] = field(
        default_factory=lambda: ["accuracy", "latency_p50", "latency_p95", "error_rate", "coverage"]
    )
    confidence_level: float = 0.95
    include_outliers: bool = False


# ──────────────────────────────────────────────
# Dataset & Mock
# ──────────────────────────────────────────────


@dataclass
class TestDataset:
    """Dataset versionado de casos de teste."""
    id: str = ""
    version: str = "1.0.0"
    capability_id: str = ""
    description: str = ""
    test_cases: list[TestCase] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_at: str = ""
    author: str = ""


@dataclass
class MockDefinition:
    """Definição de um mock para substituir dependência real."""
    dependency_id: str = ""
    method: str = ""
    input_matcher: dict = field(default_factory=dict)
    output: dict = field(default_factory=dict)
    latency_ms: int = 0
    error: Optional[str] = None


class MockRegistry:
    """Registro central de mocks para testes.

    Conforme EVALUATION_HARNESS.md seção 7.4.
    """

    def __init__(self):
        self._mocks: dict[str, list[MockDefinition]] = {}

    def register(self, mock: MockDefinition) -> None:
        """Registra um novo mock."""
        self._mocks.setdefault(mock.dependency_id, []).append(mock)

    def resolve(self, dependency_id: str, input_data: dict) -> Optional[MockDefinition]:
        """Resolve o mock mais específico para o input fornecido."""
        candidates = self._mocks.get(dependency_id, [])
        for mock in candidates:
            if all(input_data.get(k) == v for k, v in mock.input_matcher.items()):
                return mock
        return None


# ──────────────────────────────────────────────
# Evaluation Harness
# ──────────────────────────────────────────────


class EvaluationHarness:
    """Harness de avaliação de capabilities e agentes APOS.

    Executa testes unitários, integração, regressão, A/B e qualidade,
    coletando métricas e gerando relatórios.
    """

    def __init__(
        self,
        capability_harness: Optional[CapabilityHarness] = None,
        config: Optional[EvaluationConfig] = None,
    ):
        self.capability_harness = capability_harness or CapabilityHarness()
        self.config = config or EvaluationConfig()
        self.mock_registry = MockRegistry()
        self._run_history: list[EvaluationReport] = []

    # ───────────────
    # Run Methods
    # ───────────────

    async def run(self, run: EvaluationRun) -> EvaluationResult:
        """Executa uma avaliação com base no tipo configurado."""
        run.status = EvaluationStatus.RUNNING
        start_time = datetime.now(timezone.utc)

        if run.type == EvaluationType.UNIT:
            result = await self._run_unit(run)
        elif run.type == EvaluationType.INTEGRATION:
            result = await self._run_integration(run)
        elif run.type == EvaluationType.REGRESSION:
            result = await self._run_regression(run)
        elif run.type == EvaluationType.AB_TEST:
            result = await self._run_ab_test_internal(run)
        elif run.type == EvaluationType.QUALITY:
            result = await self._run_quality(run)
        else:
            result = EvaluationResult(
                run_id=run.id,
                status="failed",
                summary=MetricsSummary(run_id=run.id, status="failed"),
            )

        result.duration_seconds = (
            datetime.now(timezone.utc) - start_time
        ).total_seconds()
        result.completed_at = datetime.now(timezone.utc).isoformat()

        run.status = EvaluationStatus.COMPLETED

        if self.config.auto_generate_report:
            self._archive_report(run, result)

        return result

    async def run_unit(self, config: UnitEvaluation) -> EvaluationResult:
        """Executa avaliação unitária."""
        run = EvaluationRun(
            type=EvaluationType.UNIT,
            capability_id=config.capability_id,
            test_cases=config.test_cases,
        )
        return await self.run(run)

    async def run_integration(self, config: IntegrationEvaluation) -> EvaluationResult:
        """Executa avaliação de integração."""
        run = EvaluationRun(
            type=EvaluationType.INTEGRATION,
            capability_id=config.chain_id,
            test_cases=config.test_cases,
        )
        return await self.run(run)

    async def run_regression(self, config: RegressionEvaluation) -> EvaluationResult:
        """Executa avaliação de regressão."""
        run = EvaluationRun(
            type=EvaluationType.REGRESSION,
            capability_id=config.baseline_id,
            test_cases=config.test_suite,
        )
        return await self.run(run)

    async def run_ab_test(self, config: ABTestEvaluation) -> ComparisonResult:
        """Executa avaliação A/B e retorna o resultado da comparação."""
        test_case_list = config.test_cases
        if not test_case_list:
            test_case_list = [TestCase(
                id="default", name="Default test case",
                input={"simulated": True},
            )]

        # Execute version A
        results_a: list[TestCaseResult] = []
        for tc in test_case_list:
            for _ in range(config.num_iterations):
                req = CapabilityRequest(capability_id=config.capability_id, params=tc.input)
                exec_result = await self.capability_harness.execute(req)
                results_a.append(TestCaseResult(
                    test_case_id=tc.id,
                    name=tc.name,
                    status="passed" if exec_result.is_success() else exec_result.status,
                    output=exec_result.result,
                    expected_output=tc.expected_output,
                    match=_check_match(exec_result.result, tc.expected_output),
                ))

        # Execute version B (simulated with slight variation)
        results_b: list[TestCaseResult] = []
        for tc in test_case_list:
            for _ in range(config.num_iterations):
                req = CapabilityRequest(
                    capability_id=config.capability_id + "_v2",
                    params=tc.input,
                )
                exec_result = await self.capability_harness.execute(req)
                results_b.append(TestCaseResult(
                    test_case_id=tc.id,
                    name=tc.name,
                    status="passed" if exec_result.is_success() else exec_result.status,
                    output=exec_result.result,
                    expected_output=tc.expected_output,
                    match=_check_match(exec_result.result, tc.expected_output),
                ))

        summary_a = _compute_metrics_summary(results_a)
        summary_b = _compute_metrics_summary(results_b)

        deltas = {}
        if summary_a is not None and summary_b is not None:
            deltas["accuracy"] = summary_a.accuracy - summary_b.accuracy
            deltas["latency_p95_ms"] = summary_a.latency_p95_ms - summary_b.latency_p95_ms
            deltas["error_rate"] = summary_a.error_rate - summary_b.error_rate

        comparison = ComparisonResult(
            version_a=config.version_a_label,
            version_b=config.version_b_label,
            summary_a=summary_a,
            summary_b=summary_b,
            deltas=deltas,
        )

        # Determine verdict
        acc_delta = deltas.get("accuracy", 0.0)
        lat_delta = deltas.get("latency_p95_ms", 0.0)

        if acc_delta >= 0.02 and lat_delta <= 0:
            comparison.verdict = "a_wins"
            comparison.recommended = "A"
            comparison.reasons.append(f"Versão A {acc_delta:+.1%} mais precisa com latência igual ou menor")
        elif acc_delta <= -0.02 and lat_delta >= 0:
            comparison.verdict = "b_wins"
            comparison.recommended = "B"
            comparison.reasons.append(f"Versão B {-acc_delta:+.1%} mais precisa")
        elif acc_delta < -0.05:
            comparison.verdict = "degradation"
            comparison.recommended = "B"
            comparison.reasons.append("Degradação significativa de accuracy em A")
        else:
            comparison.verdict = "draw"
            comparison.recommended = "A"
            comparison.reasons.append("Nenhuma diferença significativa detectada")

        return comparison

    async def run_quality(self, config: QualityEvaluation) -> EvaluationResult:
        """Executa avaliação de qualidade."""
        run = EvaluationRun(
            type=EvaluationType.QUALITY,
            capability_id=config.capability_id,
            test_cases=config.test_cases,
        )
        return await self.run(run)

    # ───────────────
    # Compare & Report
    # ───────────────

    def compare(self, run_a_id: str, run_b_id: str) -> Optional[ComparisonResult]:
        """Compara duas execuções pelos IDs."""
        report_a = next((r for r in self._run_history if r.run_id == run_a_id), None)
        report_b = next((r for r in self._run_history if r.run_id == run_b_id), None)
        if not report_a or not report_b:
            return None

        return ComparisonResult(
            version_a=run_a_id,
            version_b=run_b_id,
            summary_a=report_a.summary,
            summary_b=report_b.summary,
            deltas={
                "accuracy": report_a.summary.accuracy - report_b.summary.accuracy,
                "latency_p95_ms": report_a.summary.latency_p95_ms - report_b.summary.latency_p95_ms,
                "error_rate": report_a.summary.error_rate - report_b.summary.error_rate,
            },
        )

    def report(self, run_id: str) -> Optional[EvaluationReport]:
        """Gera relatório de uma execução."""
        return next((r for r in self._run_history if r.run_id == run_id), None)

    def dashboard(self) -> EvaluationDashboard:
        """Obtém dashboard consolidado."""
        total = len(self._run_history)
        passed = sum(1 for r in self._run_history if r.verdict == "passed")
        failed = sum(1 for r in self._run_history if r.verdict == "failed")
        degraded = sum(1 for r in self._run_history if r.verdict == "degraded")

        return EvaluationDashboard(
            total_runs=total,
            passed_runs=passed,
            failed_runs=failed,
            degraded_runs=degraded,
            pass_rate=passed / total if total > 0 else 1.0,
            recent_runs=self._run_history[-10:] if self._run_history else [],
        )

    # ──────────────────────────────────────────
    # Dataset Management
    # ──────────────────────────────────────────

    def load_dataset(self, dataset: TestDataset) -> list[TestCase]:
        """Carrega casos de teste de um dataset."""
        return dataset.test_cases

    def register_dataset(self, dataset: TestDataset) -> None:
        """Registra um novo dataset (armazenamento futuro)."""
        pass

    # ───────────────
    # Internal
    # ───────────────

    async def _run_unit(self, run: EvaluationRun) -> EvaluationResult:
        results: list[TestCaseResult] = []
        for tc in run.test_cases:
            req = CapabilityRequest(capability_id=run.capability_id, params=tc.input)
            exec_result = await self.capability_harness.execute(req)
            results.append(TestCaseResult(
                test_case_id=tc.id,
                name=tc.name,
                status="passed" if exec_result.is_success() else exec_result.status,
                input=tc.input,
                output=exec_result.result,
                expected_output=tc.expected_output,
                match=_check_match(exec_result.result, tc.expected_output),
                error=exec_result.error,
                latency_ms=exec_result.metrics.get("duration_ms", 0),
            ))

        summary = _compute_metrics_summary(results)
        status = "passed" if all(r.status == "passed" for r in results) else "failed"
        return EvaluationResult(
            run_id=run.id,
            status=status,
            summary=summary,
            details=results,
        )

    async def _run_integration(self, run: EvaluationRun) -> EvaluationResult:
        # Similar to unit but with real KG context
        return await self._run_unit(run)

    async def _run_regression(self, run: EvaluationRun) -> EvaluationResult:
        results: list[TestCaseResult] = []
        for tc in run.test_cases:
            req = CapabilityRequest(capability_id=run.capability_id, params=tc.input)
            exec_result = await self.capability_harness.execute(req)
            results.append(TestCaseResult(
                test_case_id=tc.id,
                name=tc.name,
                status="passed" if exec_result.is_success() else exec_result.status,
                input=tc.input,
                output=exec_result.result,
                expected_output=tc.expected_output,
                match=_check_match(exec_result.result, tc.expected_output),
                latency_ms=exec_result.metrics.get("duration_ms", 0),
            ))

        summary = _compute_metrics_summary(results)
        is_degraded = summary.accuracy < (1.0 - self.config.regression_max_degradation)
        status = "degraded" if is_degraded else "passed"
        return EvaluationResult(
            run_id=run.id,
            status=status,
            summary=summary,
            details=results,
        )

    async def _run_ab_test_internal(self, run: EvaluationRun) -> EvaluationResult:
        ab_config = ABTestEvaluation(
            capability_id=run.capability_id,
            test_cases=run.test_cases,
        )
        comparison = await self.run_ab_test(ab_config)
        return EvaluationResult(
            run_id=run.id,
            status=comparison.verdict,
            comparison=comparison,
        )

    async def _run_quality(self, run: EvaluationRun) -> EvaluationResult:
        all_results: list[TestCaseResult] = []
        for tc in run.test_cases:
            for _ in range(max(1, 100 // max(len(run.test_cases), 1))):
                req = CapabilityRequest(capability_id=run.capability_id, params=tc.input)
                exec_result = await self.capability_harness.execute(req)
                all_results.append(TestCaseResult(
                    test_case_id=tc.id,
                    name=tc.name,
                    status="passed" if exec_result.is_success() else exec_result.status,
                    output=exec_result.result,
                    match=_check_match(exec_result.result, tc.expected_output),
                    latency_ms=exec_result.metrics.get("duration_ms", 0),
                    error=exec_result.error,
                ))

        summary = _compute_metrics_summary(all_results)
        return EvaluationResult(
            run_id=run.id,
            status="passed" if summary.accuracy >= self.config.default_accuracy_threshold else "failed",
            summary=summary,
            details=all_results,
        )

    def _archive_report(self, run: EvaluationRun, result: EvaluationResult) -> None:
        report = EvaluationReport(
            run_id=run.id,
            type=run.type,
            capability_id=run.capability_id,
            title=f"{run.type.value.capitalize()} - {run.capability_id}",
            created_at=run.created_at,
            summary=result.summary,
            verdict=result.status,
            verdict_reason=f"{result.summary.num_passed}/{result.summary.num_tests} passaram",
            test_results=result.details,
            comparison=result.comparison,
            duration_seconds=result.duration_seconds,
        )
        self._run_history.append(report)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


def _check_match(actual: Optional[dict], expected: Optional[dict]) -> Optional[bool]:
    """Verifica se a saída real corresponde à esperada."""
    if actual is None or expected is None:
        return None
    return actual == expected


def _compute_metrics_summary(results: list[TestCaseResult]) -> MetricsSummary:
    """Calcula o resumo de métricas a partir dos resultados dos testes."""
    if not results:
        return MetricsSummary()

    total = len(results)
    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status in ("failed", "error"))
    timeout = sum(1 for r in results if r.status == "timeout")
    latencies = [r.latency_ms for r in results if r.latency_ms > 0]
    matches = [r for r in results if r.match is not None]
    correct = sum(1 for r in matches if r.match)

    summary = MetricsSummary(
        num_tests=total,
        num_passed=passed,
        num_failed=failed,
        num_timeout=timeout,
        accuracy=correct / len(matches) if matches else 1.0,
        error_rate=failed / total if total > 0 else 0.0,
        timeout_rate=timeout / total if total > 0 else 0.0,
        kg_ops_total=sum(r.kg_ops for r in results),
    )

    if latencies:
        sorted_lat = sorted(latencies)
        n = len(sorted_lat)
        summary.latency_mean_ms = sum(sorted_lat) / n
        summary.latency_min_ms = sorted_lat[0]
        summary.latency_max_ms = sorted_lat[-1]
        summary.latency_p50_ms = sorted_lat[int(n * 0.50)]
        summary.latency_p95_ms = sorted_lat[int(n * 0.95)]
        summary.latency_p99_ms = sorted_lat[int(n * 0.99)]
        summary.latency_stddev_ms = statistics.stdev(sorted_lat) if n > 1 else 0.0

    return summary
