"""Testes unitários para capability_harness — dataclasses, timeout,
cancelamento, backoff, fallback, resolver de parâmetros e harness principal.
"""

import asyncio
import random
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from apos.harness.base import RetryPolicy
from apos.harness.capability_harness import (
    BackoffCalculator,
    CancellationToken,
    CapabilityHarness,
    CapabilityRequest,
    ChainContext,
    ChainLink,
    ErrorResponse,
    ExecutionResult,
    ExecutionTelemetry,
    FallbackHandler,
    ParameterResolver,
    RequestMetadata,
    TimeoutConfig,
    _deep_get,
    _match_condition,
)


# ═══════════════════════════════════════════════════════════
# 1. TestDataclasses
# ═══════════════════════════════════════════════════════════

class TestDataclasses:
    """RequestMetadata, CapabilityRequest, ExecutionResult,
    ErrorResponse, ChainLink, ChainContext."""

    def test_request_metadata_defaults(self):
        rm = RequestMetadata()
        assert rm.trace_id == ""
        assert rm.parent_trace_id is None
        assert rm.priority == "normal"
        assert rm.source == ""

    def test_request_metadata_custom(self):
        rm = RequestMetadata(
            trace_id="t-1", parent_trace_id="t-0",
            priority="high", source="cli",
        )
        assert rm.trace_id == "t-1"
        assert rm.parent_trace_id == "t-0"
        assert rm.priority == "high"
        assert rm.source == "cli"

    def test_capability_request_defaults(self):
        req = CapabilityRequest(capability_id="cap:test")
        assert req.capability_id == "cap:test"
        assert req.params == {}
        assert isinstance(req.metadata, RequestMetadata)
        assert req.agent_id == ""

    def test_capability_request_custom(self):
        req = CapabilityRequest(
            capability_id="cap:x",
            params={"key": "val"},
            metadata=RequestMetadata(trace_id="t1"),
            agent_id="agent:1",
        )
        assert req.params == {"key": "val"}
        assert req.metadata.trace_id == "t1"
        assert req.agent_id == "agent:1"

    def test_execution_result_defaults_and_is_success(self):
        er = ExecutionResult()
        assert er.status == "success"
        assert er.result == {}
        assert er.error is None
        assert er.details == {}
        assert er.metrics == {}
        assert er.effects_applied == []
        assert er.is_success() is True

    def test_execution_result_error_not_success(self):
        er = ExecutionResult(status="error", error="fail")
        assert er.is_success() is False

    def test_error_response_defaults(self):
        err = ErrorResponse()
        assert err.status == ""
        assert err.error == ""
        assert err.effects_rolled_back is False
        assert err.validation_errors is None
        assert err.fallback_suggestions is None

    def test_error_response_full(self):
        err = ErrorResponse(
            status="timeout",
            error="Timeout after 30s",
            trace_id="t1",
            capability_id="cap:x",
            executed_at="2025-01-01T00:00:00",
            duration_ms=30000.0,
            effects_rolled_back=True,
            validation_errors=[{"field": "x"}],
            precondition_errors=[{"cond": "y"}],
            fallback_suggestions=[{"alt": "cap:y"}],
        )
        assert err.status == "timeout"
        assert err.effects_rolled_back is True
        assert len(err.validation_errors) == 1

    def test_chain_link_defaults(self):
        link = ChainLink(capability_id="cap:a")
        assert link.params_template == {}
        assert link.result_mapping == {}
        assert link.required is True
        assert link.timeout_seconds is None

    def test_chain_link_optional(self):
        link = ChainLink(
            capability_id="cap:b",
            params_template={"x": "{input.y}"},
            result_mapping={"out": "in"},
            required=False,
            timeout_seconds=10,
        )
        assert link.required is False
        assert link.timeout_seconds == 10

    def test_chain_context_defaults_and_merge(self):
        ctx = ChainContext()
        assert ctx.parent_trace_id == ""
        assert ctx.blocks == []
        assert ctx.accumulated_tokens == 0
        assert ctx.max_tokens == 0
        assert ctx.previous_results == {}

        ctx.merge_result("cap:a", {"ok": True})
        assert ctx.previous_results == {"cap:a": {"ok": True}}


# ═══════════════════════════════════════════════════════════
# 2. TestTimeoutConfig
# ═══════════════════════════════════════════════════════════

class TestTimeoutConfig:
    """effective_timeout com e sem override."""

    def test_effective_timeout_default(self):
        tc = TimeoutConfig(default_timeout_seconds=30)
        assert tc.effective_timeout("cap:unknown") == 30

    def test_effective_timeout_with_override(self):
        tc = TimeoutConfig(
            default_timeout_seconds=30,
            per_capability_overrides={"cap:slow": 60},
        )
        assert tc.effective_timeout("cap:slow") == 60

    def test_effective_timeout_zero_override_falls_to_default(self):
        """Override 0 é falsy em Python — `or` cai para default."""
        tc = TimeoutConfig(
            default_timeout_seconds=30,
            per_capability_overrides={"cap:zero": 0},
        )
        assert tc.effective_timeout("cap:zero") == 30


# ═══════════════════════════════════════════════════════════
# 3. TestCancellationToken
# ═══════════════════════════════════════════════════════════

class TestCancellationToken:
    """cancel, is_cancelled, child_token (SYNC — testar _event)."""

    def test_default_not_cancelled(self):
        ct = CancellationToken(trace_id="t1")
        assert ct.is_cancelled is False
        assert ct.reason is None

    def test_cancel_sets_event_and_reason(self):
        ct = CancellationToken(trace_id="t1")
        ct.cancel("user request")
        assert ct.is_cancelled is True
        assert ct.reason == "user request"

    def test_child_token_inherits_propagate(self):
        parent = CancellationToken(trace_id="parent", propagate_downstream=True)
        child = parent.child_token("link-0")
        assert child.trace_id == "parent/link-0"
        assert child.propagate_downstream is True
        assert child.is_cancelled is False

    def test_child_token_cancelled_when_parent_cancelled(self):
        parent = CancellationToken(trace_id="parent")
        parent.cancel("parent cancelled")
        child = parent.child_token("link-0")
        assert child.is_cancelled is True
        assert child.reason == "parent cancelled"


# ═══════════════════════════════════════════════════════════
# 4. TestBackoffCalculator
# ═══════════════════════════════════════════════════════════

class TestBackoffCalculator:
    """delay exponential, cap, jitter deterministico, should_retry."""

    def test_delay_exponential(self):
        policy = RetryPolicy(
            base_delay_seconds=1.0, multiplier=2.0,
            max_delay_seconds=100.0, jitter=False,
        )
        calc = BackoffCalculator(policy)
        assert calc.delay(1) == 1.0
        assert calc.delay(2) == 2.0
        assert calc.delay(3) == 4.0
        assert calc.delay(4) == 8.0

    def test_delay_capped_at_max(self):
        policy = RetryPolicy(
            base_delay_seconds=10.0, multiplier=4.0,
            max_delay_seconds=30.0, jitter=False,
        )
        calc = BackoffCalculator(policy)
        # attempt 1: 10*4^0=10 (≤30)
        assert calc.delay(1) == 10.0
        # attempt 2: 10*4=40 (>30) → capped at 30
        assert calc.delay(2) == 30.0

    def test_delay_jitter_deterministic(self, monkeypatch):
        monkeypatch.setattr(random, "random", lambda: 0.5)
        policy = RetryPolicy(
            base_delay_seconds=2.0, multiplier=2.0,
            max_delay_seconds=100.0, jitter=True,
        )
        calc = BackoffCalculator(policy)
        # attempt 1: delay = 2.0 → jitter: 2.0 * (0.5 + 0.5*0.5) = 2.0 * 0.75 = 1.5
        assert calc.delay(1) == 2.0 * (0.5 + 0.5 * 0.5)

    def test_should_retry_non_retryable_error(self):
        policy = RetryPolicy(max_retries=3)
        calc = BackoffCalculator(policy)
        assert calc.should_retry(1, "invalid_input", 0.0) is False

    def test_should_retry_unknown_error(self):
        policy = RetryPolicy(max_retries=3, retryable_errors={"timeout"})
        calc = BackoffCalculator(policy)
        assert calc.should_retry(1, "some_random_error", 0.0) is False

    def test_should_retry_exceeds_max_retries(self):
        policy = RetryPolicy(max_retries=3)
        calc = BackoffCalculator(policy)
        assert calc.should_retry(3, "timeout", 0.0) is False

    def test_should_retry_exceeds_max_total(self):
        policy = RetryPolicy(max_retries=5, max_total_retry_seconds=120.0)
        calc = BackoffCalculator(policy)
        assert calc.should_retry(1, "timeout", 120.0) is False

    def test_should_retry_success(self):
        policy = RetryPolicy(max_retries=5, max_total_retry_seconds=120.0)
        calc = BackoffCalculator(policy)
        # timeout is in DEFAULT_RETRYABLE_ERRORS
        assert calc.should_retry(1, "timeout", 0.0) is True

    def test_should_retry_custom_retryable_error(self):
        policy = RetryPolicy(
            max_retries=5, max_total_retry_seconds=120.0,
            retryable_errors={"db_timeout"},
        )
        calc = BackoffCalculator(policy)
        assert calc.should_retry(1, "db_timeout", 0.0) is True


# ═══════════════════════════════════════════════════════════
# 5. TestFallbackHandler
# ═══════════════════════════════════════════════════════════

class TestFallbackHandler:
    """register, resolve alternatives/degraded, _match_condition."""

    def setup_method(self):
        self.handler = FallbackHandler()

    def test_register_and_get_fallback_config(self):
        config = {"alternatives": [], "degraded_mode": {}}
        self.handler.register_fallback("cap:main", config)
        assert self.handler.get_fallback_config("cap:main") == config
        assert self.handler.get_fallback_config("cap:unknown") == {}

    @pytest.mark.asyncio
    async def test_resolve_fallback_alternatives_any(self):
        self.handler.register_fallback("cap:main", {
            "alternatives": [
                {"capability_id": "cap:alt1", "condition": "any"},
            ],
        })
        original = CapabilityRequest(capability_id="cap:main", params={"x": 1})
        error = ErrorResponse(status="error", error="something broke")
        result = await self.handler.resolve_fallback("cap:main", original, error)
        assert result is not None
        assert result.capability_id == "cap:alt1"
        assert result.params == {"x": 1}

    @pytest.mark.asyncio
    async def test_resolve_fallback_alternatives_version_mismatch(self):
        self.handler.register_fallback("cap:main", {
            "alternatives": [
                {"capability_id": "cap:alt2", "condition": "version_mismatch"},
            ],
        })
        original = CapabilityRequest(capability_id="cap:main")
        error = ErrorResponse(status="error", error="version mismatch detected")
        result = await self.handler.resolve_fallback("cap:main", original, error)
        assert result is not None
        assert result.capability_id == "cap:alt2"

    @pytest.mark.asyncio
    async def test_resolve_fallback_alternatives_primary_unavailable(self):
        self.handler.register_fallback("cap:main", {
            "alternatives": [
                {"capability_id": "cap:alt3", "condition": "primary_unavailable"},
            ],
        })
        original = CapabilityRequest(capability_id="cap:main")
        error = ErrorResponse(status="timeout", error="timeout")
        result = await self.handler.resolve_fallback("cap:main", original, error)
        assert result is not None
        assert result.capability_id == "cap:alt3"

    @pytest.mark.asyncio
    async def test_resolve_fallback_degraded_mode(self):
        self.handler.register_fallback("cap:main", {
            "degraded_mode": {
                "enabled": True,
                "reduced_params": {"precision": "low"},
            },
        })
        original = CapabilityRequest(
            capability_id="cap:main", params={"mode": "full"},
        )
        error = ErrorResponse(status="error", error="failed")
        result = await self.handler.resolve_fallback("cap:main", original, error)
        assert result is not None
        assert result.capability_id == "cap:main"
        assert result.params == {"mode": "full", "precision": "low"}

    @pytest.mark.asyncio
    async def test_resolve_fallback_no_match(self):
        self.handler.register_fallback("cap:main", {
            "alternatives": [
                {"capability_id": "cap:alt", "condition": "version_mismatch"},
            ],
        })
        original = CapabilityRequest(capability_id="cap:main")
        error = ErrorResponse(status="error", error="generic fail")
        result = await self.handler.resolve_fallback("cap:main", original, error)
        assert result is None

    @pytest.mark.asyncio
    async def test_resolve_fallback_no_config(self):
        original = CapabilityRequest(capability_id="cap:no-config")
        error = ErrorResponse(status="error", error="fail")
        result = await self.handler.resolve_fallback("cap:no-config", original, error)
        assert result is None

    def test_match_condition_version_mismatch(self):
        alt = {"condition": "version_mismatch"}
        err = ErrorResponse(error="version conflict")
        assert _match_condition(alt, "cap:x", err) is True
        err2 = ErrorResponse(error="other error")
        assert _match_condition(alt, "cap:x", err2) is False

    def test_match_condition_primary_unavailable(self):
        alt = {"condition": "primary_unavailable"}
        assert _match_condition(alt, "cap:x", ErrorResponse(status="timeout")) is True
        assert _match_condition(alt, "cap:x", ErrorResponse(status="service_unavailable")) is True
        assert _match_condition(alt, "cap:x", ErrorResponse(status="error")) is False

    def test_match_condition_any(self):
        alt = {"condition": "any"}
        err = ErrorResponse(status="anything", error="anything")
        assert _match_condition(alt, "cap:x", err) is True

    def test_match_condition_no_condition(self):
        alt = {"not_a_condition": True}
        err = ErrorResponse(status="error", error="fail")
        assert _match_condition(alt, "cap:x", err) is False


# ═══════════════════════════════════════════════════════════
# 6. TestParameterResolver
# ═══════════════════════════════════════════════════════════

class TestParameterResolver:
    """Resolve templates input/agent/trace/env/unknown,
    dict/list recursao, _deep_get."""

    def make_request(self, **overrides):
        params = overrides.pop("params", {"field": "value"})
        metadata = overrides.pop("metadata", RequestMetadata(trace_id="trace-abc"))
        return CapabilityRequest(
            capability_id="cap:test",
            params=params,
            metadata=metadata,
            agent_id="agent:123",
            **overrides,
        )

    def test_resolve_input_template(self):
        req = self.make_request(params={"field": "hello"})
        resolver = ParameterResolver(req)
        assert resolver.resolve("{input.field}") == "hello"

    def test_resolve_agent_template(self):
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve("{agent.id}") == "agent:123"

    def test_resolve_trace_template(self):
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve("{trace.id}") == "trace-abc"

    def test_resolve_context_template(self):
        req = self.make_request()
        resolver = ParameterResolver(req, context={"session": "s1"})
        assert resolver.resolve("{context.session}") == "s1"

    def test_resolve_unknown_template_unchanged(self):
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve("{unknown.key}") == "{unknown.key}"

    def test_resolve_missing_nested_key_unchanged(self):
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve("{input.missing}") == "{input.missing}"

    def test_resolve_dict_recursive(self):
        req = self.make_request(params={"name": "world"})
        resolver = ParameterResolver(req)
        resolved = resolver.resolve({
            "greeting": "Hello {input.name}",
            "nested": {"id": "{agent.id}"},
        })
        assert resolved["greeting"] == "Hello world"
        assert resolved["nested"]["id"] == "agent:123"

    def test_resolve_list_recursive(self):
        req = self.make_request(params={"x": "y"})
        resolver = ParameterResolver(req)
        resolved = resolver.resolve(["{input.x}", "literal"])
        assert resolved == ["y", "literal"]

    def test_resolve_non_string_unchanged(self):
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve(42) == 42
        assert resolver.resolve(None) is None
        assert resolver.resolve(True) is True

    def test_resolve_env_not_supported(self):
        """{env.VAR} não está nas bindings — permanece inalterado."""
        req = self.make_request()
        resolver = ParameterResolver(req)
        assert resolver.resolve("{env.HOME}") == "{env.HOME}"

    def test_deep_get(self):
        data = {"a": {"b": {"c": 42}}}
        assert _deep_get(data, "a.b.c") == 42
        assert _deep_get(data, "a.b") == {"c": 42}
        assert _deep_get(data, "x") is None
        assert _deep_get(data, "x.y", default=0) == 0

    def test_deep_get_non_dict_intermediate(self):
        data = {"a": 1}
        assert _deep_get(data, "a.b") is None


# ═══════════════════════════════════════════════════════════
# 7. TestCapabilityHarness
# ═══════════════════════════════════════════════════════════

class TestCapabilityHarness:
    """register_impl, execute, execute_chain, cancel, telemetry, metrics."""

    @pytest.fixture(autouse=True)
    def _harness(self):
        self.h = CapabilityHarness()
        return self.h

    # ── register / config ──────────────────────────────

    def test_register_capability_impl(self):
        impl = MagicMock()
        self.h.register_capability_impl("cap:greet", impl)
        assert self.h._capability_implementations["cap:greet"] is impl

    def test_set_timeout_override(self):
        self.h.set_timeout_override("cap:slow", 60)
        assert self.h.timeout_config.per_capability_overrides["cap:slow"] == 60

    # ── execute success ────────────────────────────────

    @pytest.mark.asyncio
    async def test_execute_success_with_impl(self):
        impl = AsyncMock()
        impl.execute = AsyncMock(return_value={"result": "ok"})
        self.h.register_capability_impl("cap:greet", impl)

        req = CapabilityRequest(
            capability_id="cap:greet",
            params={"name": "World"},
            metadata=RequestMetadata(trace_id="t-exec-1"),
        )
        result = await self.h.execute(req)
        assert result.status == "success"
        assert result.result == {"result": "ok"}
        assert "duration_ms" in result.metrics
        impl.execute.assert_awaited_once_with(params={"name": "World"}, context={})

    @pytest.mark.asyncio
    async def test_execute_simulated_no_impl(self):
        req = CapabilityRequest(
            capability_id="cap:missing",
            metadata=RequestMetadata(trace_id="t-sim"),
        )
        result = await self.h.execute(req)
        assert result.status == "success"
        assert result.result == {"simulated": True, "capability_id": "cap:missing"}
        assert result.metrics["attempts"] == 1

    # ── execute timeout ────────────────────────────────

    @pytest.mark.asyncio
    async def test_execute_timeout(self):
        impl = AsyncMock()
        impl.execute = AsyncMock(side_effect=asyncio.TimeoutError)
        self.h.register_capability_impl("cap:slow", impl)

        req = CapabilityRequest(
            capability_id="cap:slow",
            metadata=RequestMetadata(trace_id="t-timeout"),
        )
        # timeout after 1 attempt (max_retries=3, timeout retryable → 3 attempts)
        # We'll set retry_policy to not retry so it returns immediately
        self.h.retry_policy.max_retries = 1
        result = await self.h.execute(req)
        assert result.status == "timeout"
        assert "Timeout" in (result.error or "")

    # ── execute cancelled ──────────────────────────────

    @pytest.mark.asyncio
    async def test_execute_cancelled(self):
        ct = CancellationToken(trace_id="t-cancel")
        ct.cancel("manually cancelled")

        req = CapabilityRequest(
            capability_id="cap:any",
            metadata=RequestMetadata(trace_id="t-cancel"),
        )
        result = await self.h.execute(req, cancel_token=ct)
        assert result.status == "cancelled"
        assert result.error == "Execução cancelada"

    # ── execute validation error ───────────────────────

    @pytest.mark.asyncio
    async def test_execute_validation_error(self):
        """_validate_schema retorna [] sempre, então esse caminho só é
        atingido se o método for mockado. Testamos o fluxo real."""
        req = CapabilityRequest(capability_id="cap:any")
        result = await self.h.execute(req)
        # Sem impl → simulated success (sem validação real)
        assert result.status == "success"

    # ── execute execution_error ────────────────────────

    @pytest.mark.asyncio
    async def test_execute_execution_error_no_retry(self):
        impl = AsyncMock()
        impl.execute = AsyncMock(side_effect=ValueError("boom"))
        self.h.register_capability_impl("cap:crash", impl)
        # Make ValueError non-retryable by setting empty retryable_errors
        self.h.retry_policy.retryable_errors = set()

        req = CapabilityRequest(
            capability_id="cap:crash",
            metadata=RequestMetadata(trace_id="t-crash"),
        )
        result = await self.h.execute(req)
        assert result.status == "execution_error"
        assert "boom" in (result.error or "")

    # ── execute_chain ──────────────────────────────────

    @pytest.mark.asyncio
    async def test_execute_chain_success(self):
        impl_a = AsyncMock()
        impl_a.execute = AsyncMock(return_value={"output": "from_a"})
        impl_b = AsyncMock()
        impl_b.execute = AsyncMock(return_value={"output": "from_b"})
        self.h.register_capability_impl("cap:a", impl_a)
        self.h.register_capability_impl("cap:b", impl_b)

        chain = [
            ChainLink(capability_id="cap:a", params_template={"x": "{input.p}"}),
            ChainLink(capability_id="cap:b", params_template={"prev": "{context.previous_results}"}),
        ]
        metadata = RequestMetadata(trace_id="t-chain-ok")
        results = await self.h.execute_chain(chain, {"p": 1}, metadata=metadata)
        assert len(results) == 2
        assert results[0].status == "success"
        assert results[1].status == "success"

    @pytest.mark.asyncio
    async def test_execute_chain_breaks_on_required_fail(self):
        impl_a = AsyncMock()
        impl_a.execute = AsyncMock(side_effect=ValueError("fail"))
        impl_b = AsyncMock()
        impl_b.execute = AsyncMock(return_value={"output": "from_b"})
        self.h.register_capability_impl("cap:a", impl_a)
        self.h.register_capability_impl("cap:b", impl_b)

        # Make ValueError non-retryable
        self.h.retry_policy.retryable_errors = set()
        self.h.retry_policy.max_retries = 1

        chain = [
            ChainLink(capability_id="cap:a", params_template={}, required=True),
            ChainLink(capability_id="cap:b", params_template={}),
        ]
        metadata = RequestMetadata(trace_id="t-chain-break")
        results = await self.h.execute_chain(chain, {}, metadata=metadata)
        assert len(results) == 1  # second link should NOT execute

    @pytest.mark.asyncio
    async def test_execute_chain_non_required_continues(self):
        impl_a = AsyncMock()
        impl_a.execute = AsyncMock(side_effect=ValueError("fail"))
        impl_b = AsyncMock()
        impl_b.execute = AsyncMock(return_value={"output": "from_b"})
        self.h.register_capability_impl("cap:a", impl_a)
        self.h.register_capability_impl("cap:b", impl_b)

        self.h.retry_policy.retryable_errors = set()
        self.h.retry_policy.max_retries = 1

        chain = [
            ChainLink(capability_id="cap:a", params_template={}, required=False),
            ChainLink(capability_id="cap:b", params_template={}),
        ]
        metadata = RequestMetadata(trace_id="t-chain-cont")
        results = await self.h.execute_chain(chain, {}, metadata=metadata)
        assert len(results) == 2

    @pytest.mark.asyncio
    async def test_execute_chain_cancelled_stops(self):
        """Chain com cancel_token já cancelado — deve parar imediatamente."""
        impl_b = AsyncMock()
        impl_b.execute = AsyncMock(return_value={"ok": True})
        self.h.register_capability_impl("cap:b", impl_b)

        ct = CancellationToken(trace_id="t-chain-cancel")
        ct.cancel("stopped")

        chain = [ChainLink(capability_id="cap:b", params_template={})]
        metadata = RequestMetadata(trace_id="t-chain-cancel")
        results = await self.h.execute_chain(chain, {}, metadata=metadata, cancel_token=ct)
        assert len(results) == 0

    # ── cancel ─────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_cancel_found(self):
        ct = CancellationToken(trace_id="t-cancel-me")
        self.h._cancel_tokens["t-cancel-me"] = ct

        result = await self.h.cancel("t-cancel-me", reason="admin request")
        assert result is True
        assert ct.is_cancelled is True
        assert ct.reason == "admin request"

    @pytest.mark.asyncio
    async def test_cancel_not_found(self):
        result = await self.h.cancel("nonexistent")
        assert result is False

    # ── telemetry ──────────────────────────────────────

    def test_get_telemetry_found(self):
        t = ExecutionTelemetry(trace_id="t1", capability_id="cap:a", status="success")
        self.h._telemetry_log.append(t)
        assert self.h.get_telemetry("t1") is t

    def test_get_telemetry_not_found(self):
        assert self.h.get_telemetry("nonexistent") is None

    def test_record_telemetry_sets_completed_at(self):
        t = ExecutionTelemetry(trace_id="t-rec")
        self.h._record_telemetry(t)
        assert t.completed_at != ""
        assert len(self.h._telemetry_log) == 1
        assert self.h._execution_count == 1

    # ── metrics ────────────────────────────────────────

    def test_get_metrics_all(self):
        self.h._telemetry_log = [
            ExecutionTelemetry(capability_id="cap:a", domain="dom1", status="success", total_duration_ms=100.0),
            ExecutionTelemetry(capability_id="cap:a", domain="dom1", status="error", total_duration_ms=50.0),
            ExecutionTelemetry(capability_id="cap:b", domain="dom2", status="success", total_duration_ms=200.0),
        ]
        metrics = self.h.get_metrics()
        assert metrics["total_executions"] == 3
        assert metrics["success_count"] == 2
        assert metrics["error_count"] == 1
        assert metrics["error_rate"] == 1.0 / 3.0
        # avg = (100 + 50 + 200) / 3 = 116.666...
        assert metrics["avg_duration_ms"] == pytest.approx(116.666, rel=0.01)

    def test_get_metrics_filtered_by_capability(self):
        self.h._telemetry_log = [
            ExecutionTelemetry(capability_id="cap:a", domain="dom1", status="success", total_duration_ms=100.0),
            ExecutionTelemetry(capability_id="cap:a", domain="dom1", status="error", total_duration_ms=50.0),
            ExecutionTelemetry(capability_id="cap:b", domain="dom2", status="success", total_duration_ms=200.0),
        ]
        metrics = self.h.get_metrics(capability_id="cap:a")
        assert metrics["total_executions"] == 2
        assert metrics["success_count"] == 1
        assert metrics["error_count"] == 1

    def test_get_metrics_filtered_by_domain(self):
        self.h._telemetry_log = [
            ExecutionTelemetry(capability_id="cap:a", domain="dom1", status="success", total_duration_ms=100.0),
        ]
        metrics = self.h.get_metrics(domain="dom2")
        assert metrics["total_executions"] == 0
        assert metrics["avg_duration_ms"] == 0.0

    def test_get_metrics_empty(self):
        metrics = self.h.get_metrics()
        assert metrics["total_executions"] == 0
        assert metrics["error_rate"] == 0.0
        assert metrics["avg_duration_ms"] == 0.0

    # ── internal helpers ───────────────────────────────

    def test_cancelled_result(self):
        req = CapabilityRequest(
            capability_id="cap:x",
            metadata=RequestMetadata(trace_id="t-cr"),
        )
        telemetry = ExecutionTelemetry(trace_id="t-cr")
        result = self.h._cancelled_result(req, telemetry)
        assert result.status == "cancelled"
        assert result.error == "Execução cancelada"
        assert telemetry.status == "cancelled"
        # telemetry should have been recorded
        assert len(self.h._telemetry_log) == 1

    def test_should_retry_delegates(self):
        assert self.h._should_retry(1, "timeout", 0.0) is True
        assert self.h._should_retry(1, "invalid_input", 0.0) is False

    # ── gap coverage: retry paths ─────────────────────

    @pytest.mark.asyncio
    async def test_execute_timeout_with_retry_then_fail(self):
        """Timeout → retry (sleep+continue) → timeout → fail (max retries)."""
        async def slow_execute(params, context):
            await asyncio.sleep(100)
            return {"done": True}

        impl = MagicMock()
        impl.execute = slow_execute
        self.h.register_capability_impl("cap:slow", impl)
        self.h.retry_policy.max_retries = 2
        self.h.retry_policy.base_delay_seconds = 0.01
        self.h.set_timeout_override("cap:slow", 1)  # 1s timeout

        req = CapabilityRequest(
            capability_id="cap:slow",
            metadata=RequestMetadata(trace_id="t-timeout-retry"),
        )
        result = await self.h.execute(req)
        assert result.status == "timeout"
        assert "Timeout" in (result.error or "")

    @pytest.mark.asyncio
    async def test_execute_exception_retry_then_succeed(self):
        """Exception → retry (sleep+continue) → success."""
        call_count = 0

        async def flaky_execute(params, context):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("transient")
            return {"ok": True}

        impl = MagicMock()
        impl.execute = flaky_execute
        self.h.register_capability_impl("cap:flaky", impl)
        self.h.retry_policy.max_retries = 3
        self.h.retry_policy.base_delay_seconds = 0.01
        # ValueError is NOT in DEFAULT_RETRYABLE_ERRORS, so add it
        self.h.retry_policy.retryable_errors = {"execution_error"}

        req = CapabilityRequest(
            capability_id="cap:flaky",
            metadata=RequestMetadata(trace_id="t-retry-exc"),
        )
        result = await self.h.execute(req)
        assert result.status == "success"
        assert result.result == {"ok": True}
        assert call_count == 2

    @pytest.mark.asyncio
    async def test_execute_outer_except_caught(self):
        """Outer try/except — force _validate_schema to raise."""
        original = self.h._validate_schema

        def _broken_validate(params):
            raise RuntimeError("unexpected crash")

        self.h._validate_schema = _broken_validate
        req = CapabilityRequest(capability_id="cap:crash")
        result = await self.h.execute(req)
        assert result.status == "execution_error"
        assert "unexpected crash" in (result.error or "")
        self.h._validate_schema = original  # restore

    @pytest.mark.asyncio
    async def test_execute_chain_with_result_mapping(self):
        """Result mapping via _deep_get."""
        impl_a = AsyncMock()
        impl_a.execute = AsyncMock(return_value={"output": "value_a"})
        impl_b = AsyncMock()
        impl_b.execute = AsyncMock(return_value={"done": True})
        self.h.register_capability_impl("cap:a", impl_a)
        self.h.register_capability_impl("cap:b", impl_b)

        chain = [
            ChainLink(capability_id="cap:a", params_template={}),
            ChainLink(
                capability_id="cap:b",
                params_template={"input_x": "{input.placeholder}"},
                result_mapping={"cap:a.output": "input_x"},
            ),
        ]
        metadata = RequestMetadata(trace_id="t-chain-map")
        results = await self.h.execute_chain(chain, {"placeholder": "orig"}, metadata=metadata)
        assert len(results) == 2
        assert results[0].status == "success"
        assert results[1].status == "success"
        # verify impl_b was called with mapped param
        impl_b.execute.assert_called_once()
        call_kwargs = impl_b.execute.call_args[1]
        # result_mapping overrides the template value
        assert call_kwargs["params"]["input_x"] == "value_a"

    @pytest.mark.asyncio
    async def test_cancel_active_task(self):
        """Cancel with an in-flight asyncio.Task."""
        started = asyncio.Event()

        async def never_ending(params, context):
            started.set()
            await asyncio.Event().wait()  # sleep forever
            return {"done": True}

        impl = MagicMock()
        impl.execute = never_ending
        self.h.register_capability_impl("cap:forever", impl)

        ct = CancellationToken(trace_id="t-active")
        self.h._cancel_tokens["t-active"] = ct

        req = CapabilityRequest(
            capability_id="cap:forever",
            metadata=RequestMetadata(trace_id="t-active"),
        )
        task = asyncio.create_task(self.h.execute(req, cancel_token=ct))
        await asyncio.wait_for(started.wait(), timeout=5)
        self.h._active_executions["t-active"] = task

        cancelled = await self.h.cancel("t-active", reason="kill")
        assert cancelled is True
        assert ct.is_cancelled
        assert ct.reason == "kill"

    @pytest.mark.asyncio
    async def test_wait_for_cancellation(self):
        """CancellationToken.wait_for_cancellation async path."""
        ct = CancellationToken(trace_id="t-wait")

        async def cancel_soon():
            await asyncio.sleep(0.05)
            ct.cancel("time to go")

        await asyncio.gather(ct.wait_for_cancellation(), cancel_soon())
        assert ct.is_cancelled is True
        assert ct.reason == "time to go"

    @pytest.mark.asyncio
    async def test_execute_invalid_input_via_mock(self):
        """_validate_schema returning errors → invalid_input status."""
        def _with_errors(params):
            return [{"field": "name", "message": "required"}]

        self.h._validate_schema = _with_errors
        req = CapabilityRequest(
            capability_id="cap:any",
            params={"bad": True},
            metadata=RequestMetadata(trace_id="t-invalid"),
        )
        result = await self.h.execute(req)
        assert result.status == "invalid_input"
        assert "Schema" in (result.error or "")
