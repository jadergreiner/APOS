"""
APOS Harness — Configuração Global e Tipos Base (Sprint 0.7)

Define ``HarnessGlobalConfig``, ``HarnessType``, e classes auxiliares
compartilhadas por todos os tipos de harness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ──────────────────────────────────────────────
# HarnessType
# ──────────────────────────────────────────────


class HarnessType(Enum):
    """Tipos de harness suportados pelo APOS.

    - AGENT: Harness de agente — ciclo de vida, health check, estados.
    - CAPABILITY: Harness de capability — execução, erros, rollback.
    - EVALUATION: Harness de avaliação — testes, métricas, comparação.
    - SIMULATION: Harness de simulação — carga, estresse, cenários.
    """

    AGENT = "agent"
    CAPABILITY = "capability"
    EVALUATION = "evaluation"
    SIMULATION = "simulation"


# ──────────────────────────────────────────────
# HealthStatus
# ──────────────────────────────────────────────


class HealthStatus(Enum):
    """Status de saúde de um agente."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


# ──────────────────────────────────────────────
# Constantes de Erros Retentáveis
# ──────────────────────────────────────────────

DEFAULT_RETRYABLE_ERRORS = frozenset({
    "timeout",
    "rate_limited",
    "service_unavailable",
    "kg_contention",
    "context_stale",
})

NON_RETRYABLE_ERRORS = frozenset({
    "invalid_input",
    "unauthorized",
    "precondition_fail",
    "capability_not_found",
    "circular_dependency",
})


# ──────────────────────────────────────────────
# RetryPolicy
# ──────────────────────────────────────────────


@dataclass
class RetryPolicy:
    """Política de retry com exponential backoff.

    Attributes:
        max_retries: Máximo de tentativas.
        base_delay_seconds: Delay base (exponential backoff).
        max_delay_seconds: Delay máximo entre retries.
        jitter: Adicionar variação aleatória.
        multiplier: Fator de backoff exponencial.
        retry_on_timeout: Se timeout também retenta.
        max_total_retry_seconds: Tempo máximo total gasto em retries.
        retryable_errors: Erros que podem ser retentados.
    """

    max_retries: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    jitter: bool = True
    multiplier: float = 2.0
    retry_on_timeout: bool = True
    max_total_retry_seconds: float = 120.0
    retryable_errors: set[str] = field(default_factory=lambda: set(DEFAULT_RETRYABLE_ERRORS))


# ──────────────────────────────────────────────
# HarnessGlobalConfig
# ──────────────────────────────────────────────


@dataclass
class HarnessGlobalConfig:
    """Configuração global do Harness APOS.

    Attributes:
        default_timeout_seconds: Timeout padrão para execução.
        max_timeout_seconds: Timeout máximo absoluto.
        context_timeout_seconds: Timeout para montagem de contexto.
        kg_query_timeout_seconds: Timeout para queries no KG.
        health_check_timeout_seconds: Timeout para health check.
        max_retries: Tentativas padrão.
        retry_base_delay_seconds: Delay base (exponential backoff).
        retry_max_delay_seconds: Delay máximo entre retries.
        retry_jitter: Jitter para evitar thundering herd.
        max_concurrent_executions: Execuções simultâneas por harness.
        max_concurrent_per_agent: Execuções simultâneas por agente.
        max_queued_requests: Máximo de requisições na fila.
        request_queue_timeout_seconds: Tempo máximo na fila.
        log_level: Nível de log.
        metrics_enabled: Habilitar coleta de métricas.
        trace_enabled: Habilitar tracing distribuído.
        event_logging: Habilitar registro de eventos no KG.
        metrics_export_interval_seconds: Intervalo de exportação de métricas.
        context_cache_ttl_seconds: TTL do cache de contexto.
        routing_cache_ttl_seconds: TTL do cache de roteamento.
        max_context_cache_entries: Máximo de entradas no cache de contexto.
        health_check_interval_seconds: Intervalo padrão de health check.
        health_check_consecutive_failures: Falhas consecutivas para unhealthy.
        auto_recover: Tentar recuperação automática.
        max_memory_mb_per_agent: Limite de memória por agente (MB).
        max_kg_ops_per_execution: Máximo de operações no KG por execução.
        max_payload_size_bytes: Tamanho máximo do payload (1 MB).
    """

    # ── Timeouts ──────────────────────────────────────────
    default_timeout_seconds: int = 30
    max_timeout_seconds: int = 300
    context_timeout_seconds: int = 10
    kg_query_timeout_seconds: int = 5
    health_check_timeout_seconds: int = 3

    # ── Retries ───────────────────────────────────────────
    max_retries: int = 3
    retry_base_delay_seconds: float = 1.0
    retry_max_delay_seconds: float = 30.0
    retry_jitter: bool = True

    # ── Concorrência ──────────────────────────────────────
    max_concurrent_executions: int = 10
    max_concurrent_per_agent: int = 5
    max_queued_requests: int = 100
    request_queue_timeout_seconds: int = 10

    # ── Logging e Telemetria ──────────────────────────────
    log_level: str = "INFO"
    metrics_enabled: bool = True
    trace_enabled: bool = True
    event_logging: bool = True
    metrics_export_interval_seconds: int = 60

    # ── Cache ─────────────────────────────────────────────
    context_cache_ttl_seconds: int = 300
    routing_cache_ttl_seconds: int = 300
    max_context_cache_entries: int = 1000

    # ── Health Check ──────────────────────────────────────
    health_check_interval_seconds: int = 30
    health_check_consecutive_failures: int = 3
    auto_recover: bool = True

    # ── Resource Limits ───────────────────────────────────
    max_memory_mb_per_agent: int = 512
    max_kg_ops_per_execution: int = 100
    max_payload_size_bytes: int = 1_048_576

    def to_dict(self) -> dict:
        """Serializa para dicionário."""
        return {
            "default_timeout_seconds": self.default_timeout_seconds,
            "max_timeout_seconds": self.max_timeout_seconds,
            "context_timeout_seconds": self.context_timeout_seconds,
            "kg_query_timeout_seconds": self.kg_query_timeout_seconds,
            "max_retries": self.max_retries,
            "retry_base_delay_seconds": self.retry_base_delay_seconds,
            "max_concurrent_executions": self.max_concurrent_executions,
            "log_level": self.log_level,
            "metrics_enabled": self.metrics_enabled,
            "trace_enabled": self.trace_enabled,
            "event_logging": self.event_logging,
            "health_check_interval_seconds": self.health_check_interval_seconds,
            "auto_recover": self.auto_recover,
        }

    def with_overrides(self, overrides: dict) -> HarnessGlobalConfig:
        """Retorna uma cópia com overrides aplicados."""
        new = HarnessGlobalConfig(
            **{k: v for k, v in self.__dict__.items()
               if k in HarnessGlobalConfig.__dataclass_fields__}
        )
        for key, value in overrides.items():
            if key in new.__dataclass_fields__:
                setattr(new, key, value)
        return new
