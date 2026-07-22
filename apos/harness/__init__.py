"""
APOS Harness — Camada de Execução e Gerenciamento de Agentes (Sprint 0.7)

Fornece a infraestrutura operacional que envolve, gerencia, monitora e controla
agentes, capabilities, avaliações e simulações no ecossistema APOS.
"""

from apos.harness.base import (
    HarnessGlobalConfig,
    HarnessType,
    HealthStatus,
    RetryPolicy,
    DEFAULT_RETRYABLE_ERRORS,
    NON_RETRYABLE_ERRORS,
)
from apos.harness.agent_harness import (
    AgentHarness,
    AgentLifecycle,
    AgentRegistration,
    AgentConfig,
    AgentState,
    ExecutionControl,
    ContextInjectionParams,
    HealthCheckResult,
    TraceSpan,
    AgentDashboard,
    IsolationConfig,
    CircuitBreakerConfig,
)
from apos.harness.capability_harness import (
    CapabilityHarness,
    CapabilityRequest,
    ExecutionResult,
    ErrorResponse,
    BackoffCalculator,
    FallbackHandler,
    TimeoutConfig,
    CancellationToken,
    ChainLink,
    ChainContext,
    ExecutionTelemetry,
    ParameterResolver,
)
from apos.harness.evaluation import (
    EvaluationHarness,
    EvaluationType,
    EvaluationRun,
    EvaluationResult,
    EvaluationConfig,
    EvaluationReport,
    TestCase,
    TestCaseResult,
    TestDataset,
    MetricsSummary,
    ConfusionMatrix,
    LatencyHistogram,
    CompositeMetrics,
    ComparisonResult,
    ABTestEvaluation,
    StatisticalTest,
    EvaluationDashboard,
    CapabilityHealth,
    EvaluationAlert,
    MetricsPoint,
    MockDefinition,
    MockRegistry,
    UnitEvaluation,
    IntegrationEvaluation,
    RegressionEvaluation,
    QualityEvaluation,
)
from apos.harness.simulation import (
    SimulationHarness,
    SimulationType,
    LoadProfile,
    LoadConfig,
    SyntheticDataGenerator,
    SimulationReport,
    SimulationRun,
)

__all__ = [
    # Base
    "HarnessGlobalConfig", "HarnessType", "HealthStatus",
    "RetryPolicy", "DEFAULT_RETRYABLE_ERRORS", "NON_RETRYABLE_ERRORS",
    # Agent
    "AgentHarness", "AgentLifecycle", "AgentRegistration", "AgentConfig",
    "AgentState", "ExecutionControl", "ContextInjectionParams",
    "HealthCheckResult", "TraceSpan", "AgentDashboard",
    "IsolationConfig", "CircuitBreakerConfig",
    # Capability
    "CapabilityHarness", "CapabilityRequest", "ExecutionResult",
    "ErrorResponse", "BackoffCalculator", "FallbackHandler",
    "TimeoutConfig", "CancellationToken", "ChainLink", "ChainContext",
    "ExecutionTelemetry", "ParameterResolver",
    # Evaluation
    "EvaluationHarness", "EvaluationType", "EvaluationRun",
    "EvaluationResult", "EvaluationConfig", "EvaluationReport",
    "TestCase", "TestCaseResult", "TestDataset",
    "MetricsSummary", "ConfusionMatrix", "LatencyHistogram",
    "CompositeMetrics", "ComparisonResult", "ABTestEvaluation",
    "StatisticalTest", "EvaluationDashboard", "CapabilityHealth",
    "EvaluationAlert", "MetricsPoint", "MockDefinition", "MockRegistry",
    "UnitEvaluation", "IntegrationEvaluation", "RegressionEvaluation",
    "QualityEvaluation",
    # Simulation
    "SimulationHarness", "SimulationType",
    "LoadProfile", "LoadConfig",
    "SyntheticDataGenerator", "SimulationReport",
    "SimulationRun",
]
