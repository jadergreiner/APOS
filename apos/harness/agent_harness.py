"""
APOS Agent Harness — Harness de Agentes (Sprint 0.7, AGENT_HARNESS.md)

Gerencia o ciclo de vida de cada agente APOS: registro, inicialização,
execução, pausa, finalização, health check, injeção de contexto e
observabilidade.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from apos.harness.base import HarnessGlobalConfig, HealthStatus

logger = logging.getLogger("apos.harness.agent")


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────


class AgentLifecycle(str, Enum):
    """Estados do ciclo de vida de um agente no harness.

    Fluxo: REGISTERED → READY → RUNNING → PAUSED → STOPPED → [*]
                                                    → FAILED → READY (retry)
    """
    REGISTERED = "registered"
    READY = "ready"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    FAILED = "failed"


class AgentState(str, Enum):
    """Alias para estados exportáveis do agente."""
    REGISTERED = AgentLifecycle.REGISTERED.value
    READY = AgentLifecycle.READY.value
    RUNNING = AgentLifecycle.RUNNING.value
    PAUSED = AgentLifecycle.PAUSED.value
    STOPPED = AgentLifecycle.STOPPED.value
    FAILED = AgentLifecycle.FAILED.value


# Transições válidas
_VALID_TRANSITIONS: dict[AgentLifecycle, set[AgentLifecycle]] = {
    AgentLifecycle.REGISTERED: {AgentLifecycle.READY},
    AgentLifecycle.READY: {AgentLifecycle.RUNNING},
    AgentLifecycle.RUNNING: {AgentLifecycle.PAUSED, AgentLifecycle.STOPPED, AgentLifecycle.FAILED},
    AgentLifecycle.PAUSED: {AgentLifecycle.RUNNING, AgentLifecycle.STOPPED, AgentLifecycle.FAILED},
    AgentLifecycle.STOPPED: set(),
    AgentLifecycle.FAILED: {AgentLifecycle.READY},
}


# ──────────────────────────────────────────────
# Dataclasses de Configuração
# ──────────────────────────────────────────────


@dataclass
class AgentConfig:
    """Configuração de execução de um agente.

    Attributes:
        default_timeout_s: Timeout padrão em segundos.
        max_timeout_s: Timeout máximo permitido.
        default_max_tokens: Tokens máximos padrão.
        default_temperature: Temperatura padrão.
        allowed_model_overrides: Models permitidos para override.
    """
    default_timeout_s: int = 60
    max_timeout_s: int = 300
    default_max_tokens: int = 4096
    default_temperature: float = 0.3
    allowed_model_overrides: list[str] = field(default_factory=list)


@dataclass
class AgentRegistration:
    """Registro de um agente no harness.

    Attributes:
        urn: URN do agente (ex: urn:apos:agent:hermes).
        name: Nome amigável do agente.
        capabilities: Lista de capabilities que implementa.
        domain: Domínio funcional (core, support, governance).
        maturity: Maturidade R0 (L0, L1, L2).
        config: Configuração de execução.
        isolation: Configuração de isolamento.
        health: Configuração de health check.
    """
    urn: str
    name: str
    capabilities: list[str] = field(default_factory=list)
    domain: str = "core"
    maturity: str = "L0"
    config: AgentConfig = field(default_factory=AgentConfig)
    isolation: IsolationConfig = field(default_factory=lambda: IsolationConfig(sandbox_type="none"))
    health: HealthConfig = field(default_factory=lambda: HealthConfig())


@dataclass
class HealthConfig:
    """Configuração de health check para um agente.

    Attributes:
        interval_seconds: Intervalo entre health checks.
        consecutive_failures: Falhas consecutivas para marcar unhealthy.
        heartbeat_interval_s: Intervalo esperado entre heartbeats.
        heartbeat_timeout_s: Tempo sem heartbeat antes de unhealthy.
        heartbeat_grace_period_s: Período de tolerância após timeout.
        missed_heartbeats_max: Máximo de heartbeats perdidos antes de FAILED.
    """
    interval_seconds: int = 15
    consecutive_failures: int = 3
    heartbeat_interval_s: int = 15
    heartbeat_timeout_s: int = 45
    heartbeat_grace_period_s: int = 10
    missed_heartbeats_max: int = 3


@dataclass
class IsolationConfig:
    """Configuração de isolamento por agente.

    Attributes:
        sandbox_type: Tipo de sandbox ("process", "container", "thread", "none").
        max_memory_mb: Limite máximo de memória.
        max_cpu_percent: Limite máximo de CPU (%).
        max_concurrent_requests: Requisições simultâneas máximas.
        state_ttl_s: TTL do estado do agente.
        network_access: Acesso à rede externa.
        filesystem_access: Acesso ao filesystem.
        allowed_dependencies: Dependências externas permitidas.
    """
    sandbox_type: str = "none"
    max_memory_mb: int = 512
    max_cpu_percent: float = 50.0
    max_concurrent_requests: int = 5
    state_ttl_s: int = 300
    network_access: bool = False
    filesystem_access: bool = False
    allowed_dependencies: list[str] = field(default_factory=list)


@dataclass
class CircuitBreakerConfig:
    """Configuração do circuit breaker.

    Attributes:
        failure_threshold: Falhas consecutivas para abrir.
        recovery_timeout_s: Tempo antes de half-open.
        half_open_max_retries: Tentativas em half-open.
    """
    failure_threshold: int = 5
    recovery_timeout_s: int = 30
    half_open_max_retries: int = 3


@dataclass
class ExecutionControl:
    """Parâmetros de controle de execução.

    Attributes:
        timeout_s: Tempo máximo de execução.
        max_tokens: Limite máximo de tokens na resposta.
        temperature: Controla criatividade/determinismo.
        model_override: Modelo de linguagem específico (opcional).
        priority: Prioridade de execução (1-5).
        max_retries: Tentativas máximas em caso de falha.
        execution_id: UUID gerado pelo harness.
    """
    timeout_s: int = 60
    max_tokens: int = 4096
    temperature: float = 0.3
    model_override: Optional[str] = None
    priority: int = 3
    max_retries: int = 3
    execution_id: str = ""

    def __post_init__(self):
        if not self.execution_id:
            self.execution_id = f"exec-{uuid.uuid4().hex[:12]}"

    def validate(self) -> list[str]:
        """Valida os parâmetros de execução. Retorna lista de violações."""
        violations = []
        if self.timeout_s < 1 or self.timeout_s > 300:
            violations.append(f"timeout {self.timeout_s}s fora do intervalo [1, 300]")
        if self.max_tokens < 256 or self.max_tokens > 32768:
            violations.append(f"max_tokens {self.max_tokens} fora do intervalo [256, 32768]")
        if self.temperature < 0.0 or self.temperature > 2.0:
            violations.append(f"temperature {self.temperature} fora do intervalo [0.0, 2.0]")
        return violations


# ──────────────────────────────────────────────
# Context Injection
# ──────────────────────────────────────────────


@dataclass
class ContextInjectionParams:
    """Parâmetros para injeção de contexto no agente.

    Attributes:
        anchor_urn: URN do nó âncora.
        agent_urn: URN do agente destino.
        mode: Modo de injeção ("direct", "structured", "reference").
        format: Formato ("markdown", "json", "slots").
        max_tokens: Limite de tokens para o contexto.
        extraction_depth: Profundidade de extração no KG.
        relevance_threshold: Relevance mínimo para incluir bloco.
        include_trust_summary: Incluir trust score no contexto.
        include_alerts: Incluir alertas no contexto.
    """
    anchor_urn: str = ""
    agent_urn: str = ""
    mode: str = "direct"
    format: str = "markdown"
    max_tokens: int = 8000
    extraction_depth: int = 2
    relevance_threshold: float = 0.3
    include_trust_summary: bool = False
    include_alerts: bool = False

    def get_core_context(self) -> list[str]:
        """Retorna as URNs do core context (sempre incluído)."""
        return [self.anchor_urn] if self.anchor_urn else []


# ──────────────────────────────────────────────
# Health Check
# ──────────────────────────────────────────────


@dataclass
class HealthCheckResult:
    """Resultado de um health check de agente.

    Attributes:
        agent_id: URN do agente verificado.
        status: healthy | degraded | unhealthy.
        last_heartbeat: ISO 8601 do último sinal.
        response_time_ms: Tempo de resposta do health check.
        memory_usage_mb: Uso de memória estimado.
        active_requests: Requisições em andamento.
        consecutive_failures: Falhas consecutivas.
        details: Detalhes específicos do agente.
        uptime_s: Segundos desde o último READY.
        active_capability: Capability em execução (se RUNNING).
        error_count: Erros desde o último reset.
        warnings: Alertas ativos.
    """
    agent_id: str
    status: HealthStatus = HealthStatus.HEALTHY
    last_heartbeat: str = ""
    response_time_ms: float = 0.0
    memory_usage_mb: float = 0.0
    active_requests: int = 0
    consecutive_failures: int = 0
    details: dict = field(default_factory=dict)
    uptime_s: int = 0
    active_capability: Optional[str] = None
    error_count: int = 0
    warnings: list[str] = field(default_factory=list)

    def is_healthy(self) -> bool:
        return self.status == HealthStatus.HEALTHY

    def is_degraded(self) -> bool:
        return self.status == HealthStatus.DEGRADED


# ──────────────────────────────────────────────
# Observability
# ──────────────────────────────────────────────


@dataclass
class TraceSpan:
    """Span de tracing para rastreamento distribuído.

    Attributes:
        trace_id: ID do trace (compartilhado entre agentes).
        span_id: ID do span (único por operação).
        parent_span_id: Span pai (se parte de workflow maior).
        agent_urn: Agente que criou o span.
        operation: Nome da operação (capability).
        start_time: ISO 8601.
        end_time: ISO 8601 (preenchido ao finalizar).
        duration_ms: Duração em ms (calculado ao finalizar).
        status: "ok" | "error" | "timeout".
        metadata: Metadados adicionais.
    """
    trace_id: str
    span_id: str = ""
    parent_span_id: Optional[str] = None
    agent_urn: str = ""
    operation: str = ""
    start_time: str = ""
    end_time: Optional[str] = None
    duration_ms: Optional[int] = None
    status: str = "ok"
    metadata: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.span_id:
            self.span_id = f"span-{uuid.uuid4().hex[:12]}"
        if not self.start_time:
            self.start_time = datetime.now(timezone.utc).isoformat()

    def complete(self, status: str = "ok"):
        """Finaliza o span com duração calculada."""
        self.end_time = datetime.now(timezone.utc).isoformat()
        start = datetime.fromisoformat(self.start_time)
        end = datetime.fromisoformat(self.end_time)
        self.duration_ms = int((end - start).total_seconds() * 1000)
        self.status = status

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "agent_urn": self.agent_urn,
            "operation": self.operation,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_ms": self.duration_ms,
            "status": self.status,
        }


@dataclass
class AgentDashboard:
    """Resumo de observabilidade por agente para visualização.

    Attributes:
        agent_urn: URN do agente.
        current_state: Estado atual do agente.
        uptime_s: Segundos de atividade.
        executions_total: Total de execuções.
        executions_succeeded: Execuções bem-sucedidas.
        executions_failed: Execuções com falha.
        avg_duration_ms: Duração média das execuções.
        p95_duration_ms: Percentil 95 de duração.
        error_rate: Proporção de falhas.
        retry_rate: Proporção de retries.
        memory_current_mb: Memória atual.
        memory_peak_mb: Pico de memória.
        context_tokens_avg: Média de tokens de contexto.
        health_status: Status de saúde.
        last_error: Último erro encontrado.
    """
    agent_urn: str
    current_state: str = ""
    uptime_s: int = 0
    executions_total: int = 0
    executions_succeeded: int = 0
    executions_failed: int = 0
    avg_duration_ms: float = 0.0
    p95_duration_ms: float = 0.0
    error_rate: float = 0.0
    retry_rate: float = 0.0
    memory_current_mb: float = 0.0
    memory_peak_mb: float = 0.0
    context_tokens_avg: float = 0.0
    health_status: str = "healthy"
    last_error: Optional[str] = None


# ──────────────────────────────────────────────
# Agent Harness
# ──────────────────────────────────────────────


class AgentHarness:
    """Harness de gerenciamento de ciclo de vida de agentes APOS.

    Gerencia registro, inicialização, execução, pausa, health check,
    injeção de contexto e observabilidade de agentes.
    """

    def __init__(self, config: Optional[HarnessGlobalConfig] = None):
        self.config = config or HarnessGlobalConfig()
        # Registro de agentes: urn -> AgentRegistration
        self._agents: dict[str, AgentRegistration] = {}
        # Estado atual: urn -> AgentLifecycle
        self._states: dict[str, AgentLifecycle] = {}
        # Health check cache: urn -> HealthCheckResult
        self._health_cache: dict[str, HealthCheckResult] = {}
        # Heartbeat tracking: urn -> timestamp ISO 8601
        self._heartbeats: dict[str, str] = {}
        # Contagem de falhas consecutivas: urn -> int
        self._consecutive_failures: dict[str, int] = {}
        # Traces ativos
        self._traces: dict[str, list[TraceSpan]] = {}
        # Contextos injetados: urn -> str
        self._injected_contexts: dict[str, str] = {}
        # Métricas acumuladas
        self._execution_log: list[dict] = []

    # ───────────────
    # Lifecycle Management
    # ───────────────

    def register(self, registration: AgentRegistration) -> bool:
        """Registra um agente no harness.

        Args:
            registration: Dados de registro do agente.

        Returns:
            True se registrado com sucesso, False se já existir.
        """
        if registration.urn in self._agents:
            return False
        self._agents[registration.urn] = registration
        self._states[registration.urn] = AgentLifecycle.REGISTERED
        self._heartbeats[registration.urn] = datetime.now(timezone.utc).isoformat()
        self._consecutive_failures[registration.urn] = 0
        self._log_event("agent.registered", registration.urn,
                        {"name": registration.name, "domain": registration.domain})
        return True

    def unregister(self, urn: str) -> bool:
        """Remove o registro de um agente.

        Args:
            urn: URN do agente.

        Returns:
            True se removido, False se não encontrado.
        """
        if urn not in self._agents:
            return False
        self._transition(urn, AgentLifecycle.STOPPED)
        self._agents.pop(urn, None)
        self._states.pop(urn, None)
        self._health_cache.pop(urn, None)
        self._heartbeats.pop(urn, None)
        self._consecutive_failures.pop(urn, None)
        return True

    def ready(self, urn: str) -> bool:
        """Transiciona um agente registrado para READY.

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.READY)

    def run(self, urn: str) -> bool:
        """Inicia a execução de um agente (READY -> RUNNING).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.RUNNING)

    def pause(self, urn: str) -> bool:
        """Pausa a execução de um agente (RUNNING -> PAUSED).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.PAUSED)

    def resume(self, urn: str) -> bool:
        """Retoma a execução de um agente pausado (PAUSED -> RUNNING).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.RUNNING)

    def stop(self, urn: str) -> bool:
        """Finaliza a execução de um agente (RUNNING/PAUSED -> STOPPED).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.STOPPED)

    def fail(self, urn: str) -> bool:
        """Marca um agente como falho (RUNNING/PAUSED -> FAILED).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        return self._transition(urn, AgentLifecycle.FAILED)

    def retry(self, urn: str) -> bool:
        """Tenta recuperar um agente falho (FAILED -> READY).

        Args:
            urn: URN do agente.

        Returns:
            True se a transição foi bem-sucedida.
        """
        if not self._transition(urn, AgentLifecycle.READY):
            return False
        self._consecutive_failures[urn] = 0
        return True

    def get_state(self, urn: str) -> Optional[AgentLifecycle]:
        """Retorna o estado atual de um agente.

        Args:
            urn: URN do agente.

        Returns:
            Estado atual ou None se não registrado.
        """
        return self._states.get(urn)

    def get_registration(self, urn: str) -> Optional[AgentRegistration]:
        """Retorna o registro de um agente."""
        return self._agents.get(urn)

    def list_agents(self) -> list[str]:
        """Lista todas as URNs de agentes registrados."""
        return list(self._agents.keys())

    # ───────────────
    # Context Injection
    # ───────────────

    def inject_context(self, agent_urn: str, context: str) -> None:
        """Injeta contexto no agente.

        O contexto é armazenado internamente; em um cenário real seria
        injetado no system prompt do agente.

        Args:
            agent_urn: URN do agente destino.
            context: Contexto formatado para injeção.
        """
        self._injected_contexts[agent_urn] = context
        self._log_event("context.injected", agent_urn,
                        {"context_length": len(context)})

    def get_injected_context(self, agent_urn: str) -> Optional[str]:
        """Recupera o contexto injetado em um agente."""
        return self._injected_contexts.get(agent_urn)

    def build_context(self, params: ContextInjectionParams) -> str:
        """Simula a montagem de contexto. Em produção, isso chamaria o Context Engine.

        Args:
            params: Parâmetros de injeção de contexto.

        Returns:
            Contexto formatado como string.
        """
        parts = [
            f"# Contexto para {params.agent_urn}",
            f"Âncora: {params.anchor_urn}",
            f"Modo: {params.mode}",
            f"Profundidade: {params.extraction_depth}",
            f"Tokens máximos: {params.max_tokens}",
        ]
        if params.include_trust_summary:
            parts.append("Trust Score: N/A (simulado)")
        if params.include_alerts:
            parts.append("Alertas: Nenhum alerta ativo")
        return "\n".join(parts)

    # ───────────────
    # Health Check
    # ───────────────

    def health_check(self, urn: str) -> HealthCheckResult:
        """Executa health check em um agente.

        Args:
            urn: URN do agente.

        Returns:
            Resultado do health check.

        Raises:
            ValueError: Se o agente não estiver registrado.
        """
        if urn not in self._agents:
            raise ValueError(f"Agente '{urn}' não está registrado")

        reg = self._agents[urn]
        state = self._states.get(urn, AgentLifecycle.REGISTERED)
        last_hb = self._heartbeats.get(urn, "")

        # Simula verificação de heartbeat
        now = datetime.now(timezone.utc)
        hb_age_s = 0
        if last_hb:
            try:
                hb_time = datetime.fromisoformat(last_hb)
                hb_age_s = (now - hb_time).total_seconds()
            except (ValueError, TypeError):
                hb_age_s = float("inf")

        missed = int(hb_age_s / reg.health.heartbeat_interval_s) if reg.health.heartbeat_interval_s > 0 else 0

        if missed > reg.health.missed_heartbeats_max:
            status = HealthStatus.UNHEALTHY
        elif hb_age_s > reg.health.heartbeat_timeout_s:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY

        result = HealthCheckResult(
            agent_id=urn,
            status=status,
            last_heartbeat=last_hb,
            response_time_ms=random.uniform(1.0, 50.0),
            memory_usage_mb=random.uniform(50.0, reg.isolation.max_memory_mb),
            active_requests=1 if state == AgentLifecycle.RUNNING else 0,
            consecutive_failures=self._consecutive_failures.get(urn, 0),
            uptime_s=int(hb_age_s),
            active_capability=None,
            error_count=self._consecutive_failures.get(urn, 0),
            warnings=[] if status == HealthStatus.HEALTHY else ["Heartbeat atrasado"],
        )

        self._health_cache[urn] = result
        self._log_event(f"health.{status.value}", urn, {"response_time_ms": result.response_time_ms})
        return result

    def heartbeat(self, urn: str) -> None:
        """Registra um heartbeat do agente.

        Args:
            urn: URN do agente.
        """
        if urn in self._agents:
            self._heartbeats[urn] = datetime.now(timezone.utc).isoformat()
            self._log_event("heartbeat.received", urn, {})

    def get_latest_health(self, urn: str) -> Optional[HealthCheckResult]:
        """Retorna o último resultado de health check."""
        return self._health_cache.get(urn)

    # ───────────────
    # Observability
    # ───────────────

    def start_trace(self, trace_id: str, agent_urn: str, operation: str,
                    parent_span_id: Optional[str] = None) -> TraceSpan:
        """Inicia um novo span de tracing.

        Args:
            trace_id: ID do trace.
            agent_urn: URN do agente.
            operation: Nome da operação.
            parent_span_id: Span pai (opcional).

        Returns:
            O span criado.
        """
        span = TraceSpan(
            trace_id=trace_id,
            agent_urn=agent_urn,
            operation=operation,
            parent_span_id=parent_span_id,
        )
        self._traces.setdefault(trace_id, []).append(span)
        self._log_event("trace.started", agent_urn, span.to_dict())
        return span

    def complete_trace(self, span: TraceSpan, status: str = "ok") -> None:
        """Finaliza um span de tracing."""
        span.complete(status)

    def get_trace(self, trace_id: str) -> list[TraceSpan]:
        """Retorna todos os spans de um trace."""
        return self._traces.get(trace_id, [])

    def get_dashboard(self, urn: str) -> Optional[AgentDashboard]:
        """Gera o dashboard de observabilidade para um agente."""
        reg = self._agents.get(urn)
        if not reg:
            return None

        state = self._states.get(urn, AgentLifecycle.REGISTERED)
        health = self._health_cache.get(urn)
        executions = [e for e in self._execution_log if e.get("agent_urn") == urn]

        total = len(executions)
        succeeded = sum(1 for e in executions if e.get("status") == "success")
        failed = total - succeeded
        durations = [e.get("duration_ms", 0) for e in executions if e.get("duration_ms")]
        avg_dur = sum(durations) / len(durations) if durations else 0.0
        sorted_dur = sorted(durations)
        p95 = sorted_dur[int(len(sorted_dur) * 0.95)] if sorted_dur else 0.0

        return AgentDashboard(
            agent_urn=urn,
            current_state=state.value,
            uptime_s=health.uptime_s if health else 0,
            executions_total=total,
            executions_succeeded=succeeded,
            executions_failed=failed,
            avg_duration_ms=avg_dur,
            p95_duration_ms=p95,
            error_rate=failed / total if total > 0 else 0.0,
            retry_rate=0.0,
            memory_current_mb=health.memory_usage_mb if health else 0.0,
            memory_peak_mb=health.memory_usage_mb if health else 0.0,
            context_tokens_avg=0.0,
            health_status=health.status.value if health else "unknown",
            last_error=None,
        )

    # ───────────────
    # Internal
    # ───────────────

    def _transition(self, urn: str, target: AgentLifecycle) -> bool:
        """Executa uma transição de estado validada."""
        current = self._states.get(urn)
        if current is None:
            return False
        if current == target:
            return True  # idempotente
        allowed = _VALID_TRANSITIONS.get(current, set())
        if target not in allowed:
            logger.warning(
                "Transição inválida: %s → %s para agente %s. "
                "Permitidas de '%s': %s",
                current.value, target.value, urn,
                current.value, [s.value for s in allowed],
            )
            return False
        self._states[urn] = target
        self._log_event("agent.state.transition", urn, {
            "from_state": current.value,
            "to_state": target.value,
        })
        return True

    def _log_event(self, event: str, agent_urn: str, data: dict) -> None:
        """Registra um evento estruturado de observabilidade.

        Formato: JSON estruturado conforme AGENT_HARNESS.md seção 6.1.
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": "info",
            "service": "agent-harness",
            "agent_urn": agent_urn,
            "event": event,
            "data": data,
        }
        self._execution_log.append(entry)
        if self.config.log_level == "DEBUG":
            logger.debug(json.dumps(entry))
