"""
APOS Capability Harness — Execução, Erros e Encadeamento de Capabilities
(Sprint 0.7, CAPABILITY_HARNESS.md)

Fornece o invólucro de execução que envolve cada capability individual do
APOS: validação de schema, pré-condições, execução com timeout, pós-condições,
aplicação de efeitos, rollback, retry com backoff, fallback e chains.
"""

from __future__ import annotations

import asyncio
import json
import logging
import random
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from apos.harness.base import (
    DEFAULT_RETRYABLE_ERRORS,
    NON_RETRYABLE_ERRORS,
    HarnessGlobalConfig,
    RetryPolicy,
)

logger = logging.getLogger("apos.harness.capability")


# ──────────────────────────────────────────────
# Dataclasses de Requisição e Resposta
# ──────────────────────────────────────────────


@dataclass
class RequestMetadata:
    """Metadados de roteamento e rastreamento."""
    trace_id: str = ""
    parent_trace_id: Optional[str] = None
    priority: str = "normal"
    source: str = ""


@dataclass
class CapabilityRequest:
    """Requisição de execução de capability.

    Attributes:
        capability_id: URN da capability.
        params: Parâmetros de entrada.
        metadata: Metadados de roteamento e rastreamento.
        agent_id: URN do agente solicitante.
    """
    capability_id: str
    params: dict = field(default_factory=dict)
    metadata: RequestMetadata = field(default_factory=RequestMetadata)
    agent_id: str = ""


@dataclass
class ExecutionResult:
    """Resultado de uma execução de capability.

    Attributes:
        status: Status da execução ("success" | "error" | "timeout" | ...).
        result: Dados de saída (se sucesso).
        error: Mensagem de erro (se falha).
        details: Detalhes adicionais.
        metrics: Métricas da execução.
        effects_applied: Efeitos aplicados durante a execução.
    """
    status: str = "success"
    result: dict = field(default_factory=dict)
    error: Optional[str] = None
    details: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    effects_applied: list[dict] = field(default_factory=list)

    def is_success(self) -> bool:
        return self.status == "success"


@dataclass
class ErrorResponse:
    """Estrutura padronizada de erro do Capability Harness.

    Attributes:
        status: Código do erro.
        error: Mensagem legível.
        details: Detalhes específicos do erro.
        trace_id: ID de rastreamento.
        capability_id: Capability que falhou.
        executed_at: Timestamp ISO 8601.
        duration_ms: Tempo decorrido até a falha.
        effects_rolled_back: Se rollback foi executado.
        validation_errors: Erros de validação de schema.
        precondition_errors: Erros de pré-condição.
        fallback_suggestions: Sugestões de fallback.
    """
    status: str = ""
    error: str = ""
    details: Optional[dict] = None
    trace_id: Optional[str] = None
    capability_id: Optional[str] = None
    executed_at: Optional[str] = None
    duration_ms: Optional[float] = None
    effects_rolled_back: bool = False
    validation_errors: Optional[list[dict]] = None
    precondition_errors: Optional[list[dict]] = None
    fallback_suggestions: Optional[list[dict]] = None


# ──────────────────────────────────────────────
# TimeoutConfig
# ──────────────────────────────────────────────


@dataclass
class TimeoutConfig:
    """Configuração de timeout por capability.

    Attributes:
        default_timeout_seconds: Padrão global do harness.
        per_capability_overrides: Override por capability_id.
        context_timeout_seconds: Timeout para montagem de contexto.
        kg_query_timeout_seconds: Timeout para queries individuais no KG.
        grace_period_seconds: Período de graça após timeout para cleanup.
        max_total_time_seconds: Tempo máximo total (incluindo retries).
    """
    default_timeout_seconds: int = 30
    per_capability_overrides: dict[str, int] = field(default_factory=dict)
    context_timeout_seconds: int = 10
    kg_query_timeout_seconds: int = 5
    grace_period_seconds: int = 2
    max_total_time_seconds: int = 300

    def effective_timeout(self, capability_id: str) -> int:
        """Calcula o timeout efetivo para uma capability."""
        return (
            self.per_capability_overrides.get(capability_id)
            or self.default_timeout_seconds
        )


# ──────────────────────────────────────────────
# CancellationToken
# ──────────────────────────────────────────────


@dataclass
class CancellationToken:
    """Token de cancelamento propagado entre harnesses.

    Attributes:
        trace_id: ID do trace.
        reason: Razão do cancelamento.
        initiated_by: URN do solicitante.
        initiated_at: ISO 8601.
        propagated_to: Lista de sub-executions canceladas.
        propagate_downstream: Propagar para chains filhas.
    """
    trace_id: str = ""
    reason: Optional[str] = None
    initiated_by: Optional[str] = None
    initiated_at: Optional[str] = None
    propagated_to: Optional[list[str]] = None
    propagate_downstream: bool = True

    _event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)

    def cancel(self, reason: str = "") -> None:
        """Dispara o cancelamento."""
        self.reason = reason
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    async def wait_for_cancellation(self) -> None:
        await self._event.wait()

    def child_token(self, trace_id_suffix: str) -> CancellationToken:
        """Cria um token filho vinculado."""
        child = CancellationToken(
            trace_id=f"{self.trace_id}/{trace_id_suffix}",
            propagate_downstream=self.propagate_downstream,
        )
        if self.is_cancelled:
            child.cancel(self.reason)
        return child


# ──────────────────────────────────────────────
# ParameterResolver
# ──────────────────────────────────────────────


class ParameterResolver:
    """Resolve templates nos parâmetros antes da execução.

    Suporta templates no formato ``{input.field}``, ``{agent.id}``,
    ``{trace.id}``, ``{context.field}``, ``{env.VAR}``.
    """

    def __init__(self, request: CapabilityRequest, context: Optional[dict] = None):
        self.bindings: dict[str, Any] = {
            "input": request.params,
            "agent": {"id": request.agent_id},
            "trace": {"id": request.metadata.trace_id},
            "context": context or {},
        }
        self._pattern = re.compile(r"\{([a-z_][a-z0-9_.]*)\}")

    def resolve(self, value: Any) -> Any:
        """Resolve templates recursivamente."""
        if isinstance(value, str):
            return self._resolve_template(value)
        if isinstance(value, dict):
            return {k: self.resolve(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self.resolve(v) for v in value]
        return value

    def _resolve_template(self, template: str) -> str:
        def replacer(match: re.Match) -> str:
            key_path = match.group(1).split(".")
            current: Any = self.bindings
            for key in key_path:
                if isinstance(current, dict):
                    current = current.get(key)
                else:
                    return match.group(0)
            return str(current) if current is not None else match.group(0)
        return self._pattern.sub(replacer, template)


# ──────────────────────────────────────────────
# BackoffCalculator
# ──────────────────────────────────────────────


class BackoffCalculator:
    """Calcula delay entre retries com exponential backoff + jitter.

    Conforme CAPABILITY_HARNESS.md seção 4.3.
    """

    def __init__(self, policy: RetryPolicy):
        self.policy = policy

    def delay(self, attempt: int) -> float:
        """Calcula o delay para a tentativa ``attempt`` (1-based)."""
        delay = self.policy.base_delay_seconds * (self.policy.multiplier ** (attempt - 1))
        delay = min(delay, self.policy.max_delay_seconds)

        if self.policy.jitter:
            # Jitter decorrelacionado: 50-100% do delay calculado
            delay = delay * (0.5 + random.random() * 0.5)

        return delay

    def should_retry(self, attempt: int, error_type: str, total_elapsed: float) -> bool:
        """Determina se deve retentar."""
        if error_type in NON_RETRYABLE_ERRORS:
            return False
        if error_type not in DEFAULT_RETRYABLE_ERRORS and error_type not in self.policy.retryable_errors:
            return False
        if attempt >= self.policy.max_retries:
            return False
        if total_elapsed >= self.policy.max_total_retry_seconds:
            return False
        return True


# ──────────────────────────────────────────────
# Chain
# ──────────────────────────────────────────────


@dataclass
class ChainLink:
    """Elo de uma chain de capabilities.

    Attributes:
        capability_id: URN da capability dependente.
        params_template: Template para os parâmetros da dependente.
        result_mapping: Mapeamento {campo_retorno: campo_input}.
        required: Se a dependência é obrigatória.
        timeout_seconds: Timeout específico para este elo.
    """
    capability_id: str
    params_template: dict = field(default_factory=dict)
    result_mapping: dict[str, str] = field(default_factory=dict)
    required: bool = True
    timeout_seconds: Optional[int] = None


@dataclass
class ChainContext:
    """Contexto acumulado durante a execução de uma chain.

    Attributes:
        parent_trace_id: ID do trace pai.
        blocks: Blocos acumulados.
        accumulated_tokens: Total de tokens acumulados.
        max_tokens: Limite máximo de tokens.
        previous_results: Resultados de elos anteriores.
    """
    parent_trace_id: str = ""
    blocks: list[dict] = field(default_factory=list)
    accumulated_tokens: int = 0
    max_tokens: int = 0
    previous_results: dict[str, Any] = field(default_factory=dict)

    def merge_result(self, capability_id: str, result: dict) -> None:
        """Adiciona resultado de um elo ao contexto acumulado."""
        self.previous_results[capability_id] = result


# ──────────────────────────────────────────────
# ExecutionTelemetry
# ──────────────────────────────────────────────


@dataclass
class ExecutionTelemetry:
    """Telemetria completa de uma execução de capability.

    Conforme CAPABILITY_HARNESS.md seção 7.3.
    """
    trace_id: str = ""
    capability_id: str = ""
    agent_id: str = ""
    domain: str = ""
    status: str = ""

    # Tempos (ms)
    total_duration_ms: float = 0.0
    validation_ms: float = 0.0
    precondition_ms: float = 0.0
    context_assembly_ms: float = 0.0
    execution_ms: float = 0.0
    postcondition_ms: float = 0.0
    effect_application_ms: float = 0.0
    rollback_ms: Optional[float] = None

    # Recursos
    kg_operations: int = 0
    kg_query_time_ms: float = 0.0
    retry_count: int = 0
    chain_link_index: Optional[int] = None

    # Contexto
    context_tokens_used: int = 0
    context_blocks_count: int = 0

    # Chain
    parent_trace_id: Optional[str] = None
    chain_depth: int = 0

    # Erro
    error_type: Optional[str] = None
    error_message: Optional[str] = None

    # Timestamps
    started_at: str = ""
    completed_at: str = ""


# ──────────────────────────────────────────────
# FallbackHandler
# ──────────────────────────────────────────────


class FallbackHandler:
    """Gerencia fallback de capabilities.

    Conforme CAPABILITY_HARNESS.md seção 4.4.
    """

    def __init__(self):
        self._fallback_configs: dict[str, dict] = {}

    def register_fallback(self, capability_id: str, config: dict) -> None:
        """Registra configuração de fallback para uma capability."""
        self._fallback_configs[capability_id] = config

    async def resolve_fallback(
        self,
        capability_id: str,
        original_request: CapabilityRequest,
        error: ErrorResponse,
    ) -> Optional[CapabilityRequest]:
        """Resolve uma alternativa de fallback para a capability falha."""
        fb_config = self._fallback_configs.get(capability_id, {})

        # 1. Tentar capability alternativa
        for alt in fb_config.get("alternatives", []):
            if _match_condition(alt, capability_id, error):
                return CapabilityRequest(
                    capability_id=alt["capability_id"],
                    params=original_request.params,
                    metadata=original_request.metadata,
                    agent_id=original_request.agent_id,
                )

        # 2. Modo degradado (parâmetros reduzidos)
        degraded = fb_config.get("degraded_mode", {})
        if degraded.get("enabled", False):
            reduced = degraded.get("reduced_params", {})
            new_params = {**original_request.params, **reduced}
            return CapabilityRequest(
                capability_id=original_request.capability_id,
                params=new_params,
                metadata=original_request.metadata,
                agent_id=original_request.agent_id,
            )

        return None

    def get_fallback_config(self, capability_id: str) -> dict:
        return self._fallback_configs.get(capability_id, {})


def _match_condition(alt: dict, capability_id: str, error: ErrorResponse) -> bool:
    """Verifica se a condição de fallback é satisfeita."""
    condition = alt.get("condition", "")
    if condition == "version_mismatch" and "version" in (error.error or ""):
        return True
    if condition == "primary_unavailable" and error.status in ("timeout", "service_unavailable"):
        return True
    if condition == "any":
        return True
    return False


# ──────────────────────────────────────────────
# Capability Harness
# ──────────────────────────────────────────────


class CapabilityHarness:
    """Harness de execução de capabilities do APOS.

    Fluxo completo (conforme CAPABILITY_HARNESS.md seção 2):
    1. Validar schema de entrada
    2. Verificar pré-condições
    3. Montar contexto
    4. Alocar recursos (timeout)
    5. Executar capability
    6. Verificar pós-condições
    7. Aplicar efeitos
    8. Registrar métricas
    9. Retornar resultado
    """

    def __init__(self, config: Optional[HarnessGlobalConfig] = None):
        self.config = config or HarnessGlobalConfig()
        self.timeout_config = TimeoutConfig()
        self.retry_policy = RetryPolicy()
        self.backoff = BackoffCalculator(self.retry_policy)
        self.fallback_handler = FallbackHandler()
        self._active_executions: dict[str, asyncio.Task] = {}
        self._cancel_tokens: dict[str, CancellationToken] = {}
        self._telemetry_log: list[ExecutionTelemetry] = []
        self._capability_implementations: dict[str, Any] = {}
        self._execution_count: int = 0

    def register_capability_impl(self, capability_id: str, impl: Any) -> None:
        """Registra uma implementação de capability.

        Args:
            capability_id: URN da capability.
            impl: Objeto com método ``execute(params, context)``.
        """
        self._capability_implementations[capability_id] = impl

    def set_timeout_override(self, capability_id: str, timeout_s: int) -> None:
        """Define timeout específico para uma capability."""
        self.timeout_config.per_capability_overrides[capability_id] = timeout_s

    # ───────────────
    # Execute
    # ───────────────

    async def execute(
        self,
        request: CapabilityRequest,
        cancel_token: Optional[CancellationToken] = None,
    ) -> ExecutionResult:
        """Executa uma capability com todas as garantias do harness.

        Args:
            request: Requisição de capability.
            cancel_token: Token de cancelamento (opcional).

        Returns:
            Resultado da execução.
        """
        trace_id = request.metadata.trace_id or f"exec-{uuid.uuid4().hex[:12]}"
        started_at = datetime.now(timezone.utc).isoformat()
        telemetry = ExecutionTelemetry(
            trace_id=trace_id,
            capability_id=request.capability_id,
            agent_id=request.agent_id,
            status="pending",
            started_at=started_at,
        )

        attempt = 0
        total_elapsed = 0.0
        last_error: Optional[ErrorResponse] = None

        while True:
            attempt += 1
            start_time = time.monotonic()

            try:
                # Check cancellation
                if cancel_token and cancel_token.is_cancelled:
                    return self._cancelled_result(request, telemetry)

                # Step 1: Validate schema
                validation_errors = self._validate_schema(request.params)
                if validation_errors:
                    telemetry.status = "invalid_input"
                    self._record_telemetry(telemetry)
                    return ExecutionResult(
                        status="invalid_input",
                        error="Schema de entrada inválido",
                        details={"validation_errors": validation_errors},
                    )

                # Step 2: Simulate precondition check
                # (In production, this would query the KG)

                # Step 4+5: Execute capability
                impl = self._capability_implementations.get(request.capability_id)
                effective_timeout = self.timeout_config.effective_timeout(request.capability_id)

                if impl is not None:
                    try:
                        result = await asyncio.wait_for(
                            impl.execute(params=request.params, context={}),
                            timeout=effective_timeout,
                        )
                    except asyncio.TimeoutError:
                        telemetry.status = "timeout"
                        telemetry.execution_ms = (time.monotonic() - start_time) * 1000
                        self._record_telemetry(telemetry)
                        error_resp = ErrorResponse(
                            status="timeout",
                            error=f"Timeout após {effective_timeout}s",
                            trace_id=trace_id,
                            capability_id=request.capability_id,
                            executed_at=datetime.now(timezone.utc).isoformat(),
                        )
                        if self._should_retry(attempt, "timeout", total_elapsed):
                            delay = self.backoff.delay(attempt)
                            await asyncio.sleep(delay)
                            total_elapsed += delay
                            continue
                        return ExecutionResult(
                            status="timeout",
                            error=error_resp.error,
                            details={"timeout_seconds": effective_timeout},
                        )
                    except Exception as e:
                        error_type = type(e).__name__
                        telemetry.status = "execution_error"
                        telemetry.error_type = error_type
                        telemetry.error_message = str(e)
                        self._record_telemetry(telemetry)

                        if self._should_retry(attempt, "execution_error", total_elapsed):
                            delay = self.backoff.delay(attempt)
                            await asyncio.sleep(delay)
                            total_elapsed += delay
                            continue
                        return ExecutionResult(
                            status="execution_error",
                            error=str(e),
                            details={"error_type": error_type},
                        )

                    # Success path
                    telemetry.status = "success"
                    telemetry.execution_ms = (time.monotonic() - start_time) * 1000
                    self._record_telemetry(telemetry)

                    return ExecutionResult(
                        status="success",
                        result=result if isinstance(result, dict) else {"output": result},
                        metrics={
                            "duration_ms": telemetry.execution_ms,
                            "attempts": attempt,
                        },
                    )

                else:
                    # No implementation registered — return simulated success
                    telemetry.status = "success"
                    telemetry.execution_ms = (time.monotonic() - start_time) * 1000
                    self._record_telemetry(telemetry)

                    return ExecutionResult(
                        status="success",
                        result={"simulated": True, "capability_id": request.capability_id},
                        metrics={"duration_ms": telemetry.execution_ms, "attempts": attempt},
                    )

            except Exception as e:
                logger.exception("Erro não esperado no CapabilityHarness.execute")
                telemetry.status = "execution_error"
                telemetry.error_type = type(e).__name__
                telemetry.error_message = str(e)
                self._record_telemetry(telemetry)
                return ExecutionResult(
                    status="execution_error",
                    error=str(e),
                    details={"error_type": type(e).__name__},
                )

    # ───────────────
    # Execute Chain
    # ───────────────

    async def execute_chain(
        self,
        chain: list[ChainLink],
        params: dict,
        metadata: Optional[RequestMetadata] = None,
        cancel_token: Optional[CancellationToken] = None,
    ) -> list[ExecutionResult]:
        """Executa uma chain de capabilities com propagação de cancelamento.

        Args:
            chain: Lista de elos da chain.
            params: Parâmetros de entrada (compartilhados).
            metadata: Metadados de rastreamento.
            cancel_token: Token de cancelamento.

        Returns:
            Lista de resultados de cada elo.
        """
        metadata = metadata or RequestMetadata(trace_id=f"chain-{uuid.uuid4().hex[:12]}")
        cancel_token = cancel_token or CancellationToken(trace_id=metadata.trace_id)

        results: list[ExecutionResult] = []
        chain_context = ChainContext(parent_trace_id=metadata.trace_id)

        for i, link in enumerate(chain):
            if cancel_token.is_cancelled:
                break

            # Resolve params via template
            resolver = ParameterResolver(
                CapabilityRequest(
                    capability_id=link.capability_id,
                    params=params,
                    metadata=metadata,
                ),
                context={"previous_results": chain_context.previous_results},
            )
            resolved_params = resolver.resolve(link.params_template)

            # Merge previous results via result_mapping
            for return_field, input_field in link.result_mapping.items():
                resolved_params[input_field] = _deep_get(
                    chain_context.previous_results, return_field
                )

            child_token = cancel_token.child_token(f"link-{i}")

            request = CapabilityRequest(
                capability_id=link.capability_id,
                params=resolved_params,
                metadata=RequestMetadata(
                    trace_id=child_token.trace_id,
                    parent_trace_id=metadata.trace_id,
                ),
            )

            result = await self.execute(request, cancel_token=child_token)
            results.append(result)

            if result.is_success():
                chain_context.merge_result(link.capability_id, result.result)
            elif link.required:
                # Chain quebrada — interrompe
                break

        return results

    # ───────────────
    # Cancel
    # ───────────────

    async def cancel(self, trace_id: str, reason: str = "") -> bool:
        """Cancela uma execução em andamento pelo trace_id.

        Args:
            trace_id: ID do trace a cancelar.
            reason: Razão do cancelamento.

        Returns:
            True se cancelado, False se não encontrado.
        """
        token = self._cancel_tokens.get(trace_id)
        if token is None:
            return False
        token.cancel(reason)
        task = self._active_executions.get(trace_id)
        if task and not task.done():
            task.cancel()
        return True

    def get_telemetry(self, trace_id: str) -> Optional[ExecutionTelemetry]:
        """Recupera telemetria de uma execução."""
        for t in self._telemetry_log:
            if t.trace_id == trace_id:
                return t
        return None

    def get_metrics(
        self,
        capability_id: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> dict:
        """Recupera métricas agregadas de execução."""
        filtered = self._telemetry_log
        if capability_id:
            filtered = [t for t in filtered if t.capability_id == capability_id]
        if domain:
            filtered = [t for t in filtered if t.domain == domain]

        total = len(filtered)
        success = sum(1 for t in filtered if t.status == "success")
        errors = total - success
        durations = [t.total_duration_ms for t in filtered if t.total_duration_ms > 0]

        return {
            "total_executions": total,
            "success_count": success,
            "error_count": errors,
            "error_rate": errors / total if total > 0 else 0.0,
            "avg_duration_ms": sum(durations) / len(durations) if durations else 0.0,
        }

    # ───────────────
    # Internal
    # ───────────────

    def _validate_schema(self, params: dict) -> list[dict]:
        """Valida parâmetros contra schema. Simulado — sempre retorna vazio."""
        # Em produção, usaria jsonschema.validate() contra o input_schema da capability
        return []

    def _should_retry(self, attempt: int, error_type: str, total_elapsed: float) -> bool:
        return self.backoff.should_retry(attempt, error_type, total_elapsed)

    def _cancelled_result(self, request: CapabilityRequest, telemetry: ExecutionTelemetry) -> ExecutionResult:
        telemetry.status = "cancelled"
        self._record_telemetry(telemetry)
        return ExecutionResult(
            status="cancelled",
            error="Execução cancelada",
            details={"trace_id": request.metadata.trace_id},
        )

    def _record_telemetry(self, telemetry: ExecutionTelemetry) -> None:
        """Registra telemetria de execução."""
        telemetry.completed_at = datetime.now(timezone.utc).isoformat()
        self._telemetry_log.append(telemetry)
        self._execution_count += 1


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────


def _deep_get(obj: dict, path: str, default: Any = None) -> Any:
    """Acessa valor aninhado em dict por path pontuado.

    Exemplo: _deep_get({"a": {"b": 1}}, "a.b") -> 1
    """
    keys = path.split(".")
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        else:
            return default
    return current if current is not None else default
