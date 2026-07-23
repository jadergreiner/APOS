"""Testes unitários para agent_harness — ciclo de vida, máquina de estados,
health check, contexto e observabilidade.
"""

import uuid
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime, timezone, timedelta

import pytest

from apos.harness.base import HarnessGlobalConfig, HealthStatus
from apos.harness.agent_harness import (
    AgentHarness,
    AgentLifecycle,
    AgentState,
    AgentConfig,
    AgentRegistration,
    HealthConfig,
    IsolationConfig,
    CircuitBreakerConfig,
    ExecutionControl,
    ContextInjectionParams,
    HealthCheckResult,
    TraceSpan,
    AgentDashboard,
    _VALID_TRANSITIONS,
)


# ═══════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════

def make_registration(urn="urn:apos:agent:test", **kw):
    return AgentRegistration(urn=urn, name=kw.pop("name", "Test Agent"), **kw)


# ═══════════════════════════════════════════════════════════
# TestLifecycleExecution
# ═══════════════════════════════════════════════════════════

class TestLifecycleExecution:
    """Dataclasses, inicialização, registro básico e consulta."""

    # ── Dataclasses ──────────────────────────────────────

    def test_agent_config_defaults(self):
        cfg = AgentConfig()
        assert cfg.default_timeout_s == 60
        assert cfg.max_timeout_s == 300
        assert cfg.default_max_tokens == 4096
        assert cfg.default_temperature == 0.3
        assert cfg.allowed_model_overrides == []

    def test_agent_registration_defaults(self):
        reg = AgentRegistration(urn="u:1", name="n1")
        assert reg.domain == "core"
        assert reg.maturity == "L0"
        assert isinstance(reg.config, AgentConfig)
        assert isinstance(reg.isolation, IsolationConfig)
        assert isinstance(reg.health, HealthConfig)

    def test_health_config_defaults(self):
        hc = HealthConfig()
        assert hc.interval_seconds == 15
        assert hc.consecutive_failures == 3
        assert hc.heartbeat_interval_s == 15
        assert hc.heartbeat_timeout_s == 45
        assert hc.heartbeat_grace_period_s == 10
        assert hc.missed_heartbeats_max == 3

    def test_isolation_config_defaults(self):
        iso = IsolationConfig()
        assert iso.sandbox_type == "none"
        assert iso.max_memory_mb == 512
        assert iso.max_cpu_percent == 50.0
        assert iso.max_concurrent_requests == 5
        assert iso.state_ttl_s == 300
        assert iso.network_access is False
        assert iso.filesystem_access is False

    def test_circuit_breaker_config_defaults(self):
        cb = CircuitBreakerConfig()
        assert cb.failure_threshold == 5
        assert cb.recovery_timeout_s == 30
        assert cb.half_open_max_retries == 3

    def test_execution_control_defaults(self):
        ec = ExecutionControl()
        assert ec.timeout_s == 60
        assert ec.max_tokens == 4096
        assert ec.temperature == 0.3
        assert ec.model_override is None
        assert ec.priority == 3
        assert ec.max_retries == 3
        assert ec.execution_id.startswith("exec-")

    def test_execution_control_custom_id_preserved(self):
        ec = ExecutionControl(execution_id="my-custom-id")
        assert ec.execution_id == "my-custom-id"

    def test_execution_control_validate_valid(self):
        ec = ExecutionControl(timeout_s=60, max_tokens=4096, temperature=0.3)
        assert ec.validate() == []

    def test_execution_control_validate_timeout_out_of_range(self):
        ec = ExecutionControl(timeout_s=0)
        violations = ec.validate()
        assert any("timeout" in v for v in violations)

        ec2 = ExecutionControl(timeout_s=301)
        violations2 = ec2.validate()
        assert any("timeout" in v for v in violations2)

    def test_execution_control_validate_max_tokens_out_of_range(self):
        ec = ExecutionControl(max_tokens=100)
        assert ec.validate()

    def test_execution_control_validate_temperature_out_of_range(self):
        ec = ExecutionControl(temperature=-0.1)
        violations = ec.validate()
        assert any("temperature" in v for v in violations)

        ec2 = ExecutionControl(temperature=2.1)
        violations2 = ec2.validate()
        assert any("temperature" in v for v in violations2)

    def test_context_injection_params_defaults(self):
        cip = ContextInjectionParams()
        assert cip.mode == "direct"
        assert cip.format == "markdown"
        assert cip.max_tokens == 8000
        assert cip.extraction_depth == 2
        assert cip.relevance_threshold == 0.3
        assert cip.include_trust_summary is False
        assert cip.include_alerts is False

    def test_context_injection_params_get_core_context_with_anchor(self):
        cip = ContextInjectionParams(anchor_urn="urn:anchor:1")
        assert cip.get_core_context() == ["urn:anchor:1"]

    def test_context_injection_params_get_core_context_empty(self):
        cip = ContextInjectionParams()
        assert cip.get_core_context() == []

    def test_health_check_result_defaults(self):
        hcr = HealthCheckResult(agent_id="urn:test")
        assert hcr.is_healthy() is True
        assert hcr.is_degraded() is False
        assert hcr.status == HealthStatus.HEALTHY

    def test_health_check_result_is_degraded(self):
        hcr = HealthCheckResult(agent_id="urn:test", status=HealthStatus.DEGRADED)
        assert hcr.is_degraded() is True
        assert hcr.is_healthy() is False

    def test_trace_span_post_init(self):
        ts = TraceSpan(trace_id="trace-1", agent_urn="u1", operation="op1")
        assert ts.span_id.startswith("span-")
        assert ts.start_time != ""

    def test_trace_span_custom_span_id(self):
        ts = TraceSpan(trace_id="t1", span_id="custom-span")
        assert ts.span_id == "custom-span"

    def test_trace_span_complete(self):
        ts = TraceSpan(trace_id="t1", agent_urn="u1", operation="op1")
        ts.complete("ok")
        assert ts.end_time is not None
        assert ts.duration_ms is not None
        assert ts.duration_ms >= 0
        assert ts.status == "ok"

    def test_trace_span_complete_with_error(self):
        ts = TraceSpan(trace_id="t1", agent_urn="u1", operation="op1")
        ts.complete("error")
        assert ts.status == "error"

    def test_trace_span_to_dict(self):
        ts = TraceSpan(trace_id="t1", span_id="s1", agent_urn="u1", operation="op")
        d = ts.to_dict()
        assert d["trace_id"] == "t1"
        assert d["span_id"] == "s1"
        assert d["agent_urn"] == "u1"
        assert d["operation"] == "op"

    def test_agent_dashboard_defaults(self):
        ad = AgentDashboard(agent_urn="u1")
        assert ad.agent_urn == "u1"
        assert ad.current_state == ""
        assert ad.executions_total == 0

    # ── AgentHarness init ────────────────────────────────

    def test_harness_init_default(self):
        h = AgentHarness()
        assert isinstance(h.config, HarnessGlobalConfig)
        assert h._agents == {}
        assert h._states == {}
        assert h._execution_log == []

    def test_harness_init_with_config(self):
        cfg = HarnessGlobalConfig(log_level="DEBUG")
        h = AgentHarness(config=cfg)
        assert h.config.log_level == "DEBUG"

    # ── Register / Unregister ────────────────────────────

    def test_register_success(self):
        h = AgentHarness()
        reg = make_registration("urn:1")
        assert h.register(reg) is True
        assert h.get_state("urn:1") == AgentLifecycle.REGISTERED

    def test_register_duplicate(self):
        h = AgentHarness()
        reg = make_registration("urn:1")
        assert h.register(reg) is True
        assert h.register(reg) is False

    def test_register_sets_consecutive_failures_zero(self):
        h = AgentHarness()
        h.register(make_registration("urn:1"))
        assert h._consecutive_failures["urn:1"] == 0

    def test_unregister_success(self):
        h = AgentHarness()
        h.register(make_registration("urn:1"))
        assert h.unregister("urn:1") is True
        assert h.get_state("urn:1") is None

    def test_unregister_not_found(self):
        h = AgentHarness()
        assert h.unregister("nonexistent") is False

    def test_unregister_cleans_internal_dicts(self):
        h = AgentHarness()
        h.register(make_registration("urn:1"))
        h.ready("urn:1")
        h.run("urn:1")
        h.unregister("urn:1")
        assert "urn:1" not in h._agents
        assert "urn:1" not in h._states
        assert "urn:1" not in h._health_cache
        assert "urn:1" not in h._heartbeats
        assert "urn:1" not in h._consecutive_failures

    # ── Query methods ────────────────────────────────────

    def test_get_state_not_registered(self):
        assert AgentHarness().get_state("nonexistent") is None

    def test_get_registration_found(self):
        h = AgentHarness()
        reg = make_registration("urn:1")
        h.register(reg)
        assert h.get_registration("urn:1") is reg

    def test_get_registration_not_found(self):
        assert AgentHarness().get_registration("nosuch") is None

    def test_list_agents_empty(self):
        assert AgentHarness().list_agents() == []

    def test_list_agents_with_agents(self):
        h = AgentHarness()
        h.register(make_registration("urn:a"))
        h.register(make_registration("urn:b"))
        assert sorted(h.list_agents()) == ["urn:a", "urn:b"]


# ═══════════════════════════════════════════════════════════
# TestStateMachine
# ═══════════════════════════════════════════════════════════

class TestStateMachine:
    """Transições de estado válidas e inválidas."""

    def setup_method(self):
        self.h = AgentHarness()
        self.h.register(make_registration("urn:agent-1"))

    # ── ready ────────────────────────────────────────────

    def test_ready_success(self):
        assert self.h.ready("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.READY

    def test_ready_from_wrong_state_fails(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.ready("urn:agent-1") is False

    # ── run ──────────────────────────────────────────────

    def test_run_success(self):
        self.h.ready("urn:agent-1")
        assert self.h.run("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.RUNNING

    def test_run_from_registered_fails(self):
        assert self.h.run("urn:agent-1") is False

    # ── pause ────────────────────────────────────────────

    def test_pause_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.pause("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.PAUSED

    def test_pause_from_registered_fails(self):
        assert self.h.pause("urn:agent-1") is False

    # ── resume ───────────────────────────────────────────

    def test_resume_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.pause("urn:agent-1")
        assert self.h.resume("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.RUNNING

    def test_resume_from_ready_succeeds(self):
        """READY → RUNNING é válido (resume é _transition para RUNNING)."""
        self.h.ready("urn:agent-1")
        assert self.h.resume("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.RUNNING

    # ── stop ─────────────────────────────────────────────

    def test_stop_from_running_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.stop("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.STOPPED

    def test_stop_from_paused_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.pause("urn:agent-1")
        assert self.h.stop("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.STOPPED

    def test_stop_from_registered_fails(self):
        assert self.h.stop("urn:agent-1") is False

    # ── fail ─────────────────────────────────────────────

    def test_fail_from_running_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.fail("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.FAILED

    def test_fail_from_paused_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.pause("urn:agent-1")
        assert self.h.fail("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.FAILED

    def test_fail_from_registered_fails(self):
        assert self.h.fail("urn:agent-1") is False

    # ── retry ────────────────────────────────────────────

    def test_retry_success(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.fail("urn:agent-1")
        assert self.h.retry("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.READY

    def test_retry_resets_consecutive_failures(self):
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.fail("urn:agent-1")
        self.h._consecutive_failures["urn:agent-1"] = 5
        self.h.retry("urn:agent-1")
        assert self.h._consecutive_failures["urn:agent-1"] == 0

    def test_retry_from_running_fails(self):
        """retry de RUNNING falha pois só FAILED → READY é válido."""
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.retry("urn:agent-1") is False

    # ── Transition edge cases ────────────────────────────

    def test_idempotent_transition_returns_true(self):
        """Transição para o mesmo estado deve ser True."""
        assert self.h.ready("urn:agent-1") is True
        assert self.h.ready("urn:agent-1") is True  # já READY → idempotente

    def test_transition_for_unregistered_agent_fails(self):
        assert self.h.ready("nonexistent") is False

    def test_full_lifecycle_flow(self):
        """Fluxo completo: REGISTERED → READY → RUNNING → PAUSED → RUNNING → STOPPED."""
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.REGISTERED
        assert self.h.ready("urn:agent-1") is True
        assert self.h.run("urn:agent-1") is True
        assert self.h.pause("urn:agent-1") is True
        assert self.h.resume("urn:agent-1") is True
        assert self.h.stop("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.STOPPED

    def test_fail_retry_flow(self):
        """Fluxo: RUNNING → FAILED → READY."""
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        assert self.h.fail("urn:agent-1") is True
        assert self.h.retry("urn:agent-1") is True
        assert self.h.get_state("urn:agent-1") == AgentLifecycle.READY

    # ── _VALID_TRANSITIONS matrix ────────────────────────

    def test_valid_transitions_matrix(self):
        assert _VALID_TRANSITIONS[AgentLifecycle.REGISTERED] == {AgentLifecycle.READY}
        assert _VALID_TRANSITIONS[AgentLifecycle.READY] == {AgentLifecycle.RUNNING}
        assert _VALID_TRANSITIONS[AgentLifecycle.RUNNING] == {
            AgentLifecycle.PAUSED, AgentLifecycle.STOPPED, AgentLifecycle.FAILED,
        }
        assert _VALID_TRANSITIONS[AgentLifecycle.PAUSED] == {
            AgentLifecycle.RUNNING, AgentLifecycle.STOPPED, AgentLifecycle.FAILED,
        }
        assert _VALID_TRANSITIONS[AgentLifecycle.STOPPED] == set()
        assert _VALID_TRANSITIONS[AgentLifecycle.FAILED] == {AgentLifecycle.READY}

    def test_invalid_transition_across_all_states(self):
        """Testa que transições inválidas retornam False."""
        # De REGISTERED só pode ir para READY
        assert self.h.run("urn:agent-1") is False
        assert self.h.pause("urn:agent-1") is False
        assert self.h.stop("urn:agent-1") is False
        assert self.h.fail("urn:agent-1") is False

    def test_ready_after_stopped_fails(self):
        """STOPPED não tem transições de saída."""
        self.h.ready("urn:agent-1")
        self.h.run("urn:agent-1")
        self.h.stop("urn:agent-1")
        assert self.h.ready("urn:agent-1") is False

    def test_state_enum_alias(self):
        assert AgentState.REGISTERED.value == AgentLifecycle.REGISTERED.value
        assert AgentState.READY.value == AgentLifecycle.READY.value
        assert AgentState.RUNNING.value == AgentLifecycle.RUNNING.value
        assert AgentState.PAUSED.value == AgentLifecycle.PAUSED.value
        assert AgentState.STOPPED.value == AgentLifecycle.STOPPED.value
        assert AgentState.FAILED.value == AgentLifecycle.FAILED.value


# ═══════════════════════════════════════════════════════════
# TestHealthCheck
# ═══════════════════════════════════════════════════════════

class TestHealthCheck:
    """Health check, heartbeat e resultados."""

    def setup_method(self):
        self.h = AgentHarness()
        self.h.register(make_registration("urn:agent-hc"))

    def test_health_check_unregistered_raises(self):
        with pytest.raises(ValueError, match="não está registrado"):
            self.h.health_check("no-such-urn")

    def test_heartbeat_updates_timestamp(self):
        before = datetime.now(timezone.utc).isoformat()
        self.h.heartbeat("urn:agent-hc")
        after = self.h._heartbeats["urn:agent-hc"]
        assert after >= before

    def test_heartbeat_only_for_registered(self):
        """heartbeat para agente não registrado não faz nada (sem erro)."""
        self.h.heartbeat("nonexistent")
        # apenas não deve lançar exceção
        assert "nonexistent" not in self.h._heartbeats

    def test_health_check_returns_result_with_agent_id(self):
        result = self.h.health_check("urn:agent-hc")
        assert result.agent_id == "urn:agent-hc"

    def test_health_check_returns_healthy_for_fresh_agent(self):
        result = self.h.health_check("urn:agent-hc")
        assert result.is_healthy() is True

    def test_health_check_status_healthy(self):
        result = self.h.health_check("urn:agent-hc")
        assert result.status == HealthStatus.HEALTHY
        assert result.warnings == []

    def test_health_check_includes_usage_metrics(self):
        result = self.h.health_check("urn:agent-hc")
        assert 1.0 <= result.response_time_ms <= 50.0
        assert 50.0 <= result.memory_usage_mb <= 512.0

    def test_health_check_with_running_state(self):
        self.h.ready("urn:agent-hc")
        self.h.run("urn:agent-hc")
        result = self.h.health_check("urn:agent-hc")
        assert result.active_requests == 1

    def test_health_cache_updated(self):
        result = self.h.health_check("urn:agent-hc")
        cached = self.h.get_latest_health("urn:agent-hc")
        assert cached is result

    def test_get_latest_health_none_for_unchecked(self):
        assert self.h.get_latest_health("urn:agent-hc") is None

    def test_get_latest_health_unregistered(self):
        assert self.h.get_latest_health("nonexistent") is None

    def test_health_check_degraded_by_heartbeat_age(self):
        """Envelhece o heartbeat artificialmente para testar DEGRADED.
        Com interval=15, timeout=45, max=3 → hb_age=55s → missed=3 → DEGRADED (3 ≤ 3 e 55 > 45)."""
        old_ts = (datetime.now(timezone.utc) - timedelta(seconds=55)).isoformat()
        self.h._heartbeats["urn:agent-hc"] = old_ts
        result = self.h.health_check("urn:agent-hc")
        assert result.status == HealthStatus.DEGRADED
        assert result.warnings == ["Heartbeat atrasado"]

    def test_health_check_unhealthy_by_missed_heartbeats(self):
        """Muitos heartbeats perdidos → UNHEALTHY."""
        very_old = (datetime.now(timezone.utc) - timedelta(seconds=300)).isoformat()
        self.h._heartbeats["urn:agent-hc"] = very_old
        result = self.h.health_check("urn:agent-hc")
        assert result.status == HealthStatus.UNHEALTHY

    def test_health_check_invalid_heartbeat_date(self):
        """Heartbeat inválido → UNHEALTHY sem OverflowError."""
        self.h._heartbeats["urn:agent-hc"] = "not-a-date"
        result = self.h.health_check("urn:agent-hc")
        assert result.status == HealthStatus.UNHEALTHY
        assert "Heartbeat date is invalid or extreme" in result.warnings

    def test_health_check_extreme_timestamp(self):
        """Timestamp extremamente antigo (ano 1900) → trata sem OverflowError."""
        old_ts = datetime(1900, 1, 1, tzinfo=timezone.utc).isoformat()
        self.h._heartbeats["urn:agent-hc"] = old_ts
        result = self.h.health_check("urn:agent-hc")
        # deve ser UNHEALTHY (muitos heartbeats perdidos) sem OverflowError
        assert result.status == HealthStatus.UNHEALTHY

    def test_health_check_consecutive_failures_propagated(self):
        self.h._consecutive_failures["urn:agent-hc"] = 2
        result = self.h.health_check("urn:agent-hc")
        assert result.consecutive_failures == 2
        assert result.error_count == 2

    def test_heartbeat_logs_event(self):
        self.h.heartbeat("urn:agent-hc")
        log = self.h._execution_log
        events = [e for e in log if e["event"] == "heartbeat.received"]
        assert len(events) == 1
        assert events[0]["agent_urn"] == "urn:agent-hc"

    def test_health_check_updates_cache(self):
        r1 = self.h.health_check("urn:agent-hc")
        r2 = self.h.health_check("urn:agent-hc")
        assert self.h._health_cache["urn:agent-hc"] is r2  # último resultado


# ═══════════════════════════════════════════════════════════
# TestMockingContext
# ═══════════════════════════════════════════════════════════

class TestMockingContext:
    """Context injection, tracing, dashboard e observabilidade."""

    def setup_method(self):
        self.h = AgentHarness()
        self.h.register(make_registration("urn:agent-ctx"))

    # ── Context Injection ────────────────────────────────

    def test_inject_context_stores(self):
        self.h.inject_context("urn:agent-ctx", "context-data")
        assert self.h.get_injected_context("urn:agent-ctx") == "context-data"

    def test_inject_context_updates(self):
        self.h.inject_context("urn:agent-ctx", "first")
        self.h.inject_context("urn:agent-ctx", "second")
        assert self.h.get_injected_context("urn:agent-ctx") == "second"

    def test_inject_context_logs_event(self):
        self.h.inject_context("urn:agent-ctx", "data")
        log = self.h._execution_log
        assert any(e["event"] == "context.injected" for e in log)
        injected_events = [e for e in log if e["event"] == "context.injected"]
        assert injected_events[0]["data"]["context_length"] == 4

    def test_get_injected_context_none(self):
        assert self.h.get_injected_context("urn:nonexistent") is None

    def test_build_context_basic(self):
        params = ContextInjectionParams(
            anchor_urn="urn:anchor:1",
            agent_urn="urn:agent-ctx",
            mode="direct",
            extraction_depth=2,
            max_tokens=8000,
        )
        ctx = self.h.build_context(params)
        assert "urn:agent-ctx" in ctx
        assert "urn:anchor:1" in ctx
        assert "direct" in ctx
        assert "Trust Score" not in ctx

    def test_build_context_with_trust_summary(self):
        params = ContextInjectionParams(
            anchor_urn="urn:a",
            agent_urn="urn:b",
            include_trust_summary=True,
        )
        ctx = self.h.build_context(params)
        assert "Trust Score" in ctx

    def test_build_context_with_alerts(self):
        params = ContextInjectionParams(
            anchor_urn="urn:a",
            agent_urn="urn:b",
            include_alerts=True,
        )
        ctx = self.h.build_context(params)
        assert "Alertas" in ctx

    def test_build_context_both_flags(self):
        params = ContextInjectionParams(
            anchor_urn="urn:a",
            agent_urn="urn:b",
            include_trust_summary=True,
            include_alerts=True,
        )
        ctx = self.h.build_context(params)
        assert "Trust Score" in ctx
        assert "Alertas" in ctx

    # ── Tracing ──────────────────────────────────────────

    def test_start_trace_creates_span(self):
        span = self.h.start_trace("trace-1", "urn:agent-ctx", "op-test")
        assert span.trace_id == "trace-1"
        assert span.agent_urn == "urn:agent-ctx"
        assert span.operation == "op-test"
        assert span.parent_span_id is None

    def test_start_trace_with_parent_span(self):
        span = self.h.start_trace("trace-1", "urn:agent-ctx", "op", parent_span_id="parent-1")
        assert span.parent_span_id == "parent-1"

    def test_complete_trace_finalizes(self):
        span = self.h.start_trace("trace-1", "urn:agent-ctx", "op")
        self.h.complete_trace(span, "ok")
        assert span.end_time is not None
        assert span.duration_ms is not None
        assert span.status == "ok"

    def test_complete_trace_with_error(self):
        span = self.h.start_trace("trace-1", "urn:agent-ctx", "op")
        self.h.complete_trace(span, "error")
        assert span.status == "error"

    def test_get_trace_found(self):
        self.h.start_trace("trace-1", "urn:agent-ctx", "op1")
        self.h.start_trace("trace-1", "urn:agent-ctx", "op2")
        spans = self.h.get_trace("trace-1")
        assert len(spans) == 2

    def test_get_trace_not_found(self):
        assert self.h.get_trace("nonexistent") == []

    def test_start_trace_logs_event(self):
        self.h.start_trace("trace-1", "urn:agent-ctx", "op")
        log = self.h._execution_log
        assert any(e["event"] == "trace.started" for e in log)

    # ── Dashboard ────────────────────────────────────────

    def test_dashboard_returns_none_for_unregistered(self):
        assert self.h.get_dashboard("nonexistent") is None

    def test_dashboard_basic(self):
        self.h.ready("urn:agent-ctx")
        self.h.run("urn:agent-ctx")
        dash = self.h.get_dashboard("urn:agent-ctx")
        assert dash.agent_urn == "urn:agent-ctx"
        assert dash.current_state == AgentLifecycle.RUNNING.value
        # register + ready + run each log events → 3 entries (nenhum tem status="success")
        assert dash.executions_total == 3
        assert dash.error_rate == 1.0

    def test_dashboard_with_executions(self):
        self.h.ready("urn:agent-ctx")
        self.h.run("urn:agent-ctx")
        self.h.health_check("urn:agent-ctx")
        dash = self.h.get_dashboard("urn:agent-ctx")
        assert dash.health_status == HealthStatus.HEALTHY.value

    def test_dashboard_errors_reflected(self):
        # Usa harness limpo para controlar exatamente o _execution_log
        h = AgentHarness()
        h.register(make_registration("urn:agent-ctx"))
        h._execution_log.append({
            "agent_urn": "urn:agent-ctx",
            "status": "success",
            "duration_ms": 100,
        })
        h._execution_log.append({
            "agent_urn": "urn:agent-ctx",
            "status": "error",
            "duration_ms": 50,
        })
        dash = h.get_dashboard("urn:agent-ctx")
        assert dash.executions_total == 3  # register log + 2 manuais
        assert dash.executions_succeeded == 1
        assert dash.executions_failed == 2
        assert dash.error_rate == 2.0 / 3.0

    def test_dashboard_p95_calculation(self):
        for i in range(20):
            self.h._execution_log.append({
                "agent_urn": "urn:agent-ctx",
                "status": "success",
                "duration_ms": float(i * 10),
            })
        dash = self.h.get_dashboard("urn:agent-ctx")
        # 20 itens, 0.95*20 = 19 → sorted_dur[19] = 190
        assert dash.p95_duration_ms == 190.0

    # ── _log_event / _execution_log ──────────────────────

    def test_log_event_structure(self):
        self.h._log_event("custom.event", "urn:agent-ctx", {"key": "val"})
        entry = self.h._execution_log[-1]
        assert entry["event"] == "custom.event"
        assert entry["agent_urn"] == "urn:agent-ctx"
        assert entry["data"] == {"key": "val"}
        assert entry["level"] == "info"
        assert entry["service"] == "agent-harness"
        assert "timestamp" in entry

    def test_log_event_debug_level_does_not_crash(self):
        h = AgentHarness(config=HarnessGlobalConfig(log_level="DEBUG"))
        h.register(make_registration("urn:debug"))
        # logger.debug é chamado, mas não deve crashar
        h._log_event("debug.test", "urn:debug", {"x": 1})
        assert len(h._execution_log) >= 1

    # ── AgentState enum ──────────────────────────────────

    def test_agent_state_is_alias(self):
        assert AgentState.__members__ == AgentLifecycle.__members__


# ═══════════════════════════════════════════════════════════
# TestConcurrency (1.4)
# ═══════════════════════════════════════════════════════════

class TestConcurrency:
    """Edge cases de concorrência: registros simultâneos,
    transições concorrentes e idempotência de registro."""

    def test_simultaneous_registrations(self):
        """2 agentes registrados em sequência rápida, ambos existem."""
        h = AgentHarness()
        reg_a = make_registration("urn:conc:a")
        reg_b = make_registration("urn:conc:b")

        assert h.register(reg_a) is True
        assert h.register(reg_b) is True

        assert h.get_state("urn:conc:a") == AgentLifecycle.REGISTERED
        assert h.get_state("urn:conc:b") == AgentLifecycle.REGISTERED
        assert sorted(h.list_agents()) == ["urn:conc:a", "urn:conc:b"]

    def test_concurrent_state_transitions(self):
        """Transições concorrentes não corrompem estado."""
        import threading

        h = AgentHarness()
        h.register(make_registration("urn:conc-trans"))
        h.ready("urn:conc-trans")

        errors = []

        def try_transition(target_state):
            try:
                if target_state == "run":
                    h.run("urn:conc-trans")
                elif target_state == "pause":
                    h.pause("urn:conc-trans")
                elif target_state == "stop":
                    h.stop("urn:conc-trans")
            except Exception as e:
                errors.append(str(e))

        threads = [
            threading.Thread(target=try_transition, args=("run",)),
            threading.Thread(target=try_transition, args=("pause",)),
            threading.Thread(target=try_transition, args=("stop",)),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Nenhuma exceção, estado final é um dos estados válidos
        assert len(errors) == 0
        final_state = h.get_state("urn:conc-trans")
        assert final_state in (AgentLifecycle.RUNNING, AgentLifecycle.PAUSED,
                               AgentLifecycle.STOPPED)

    def test_concurrent_ready_transitions(self):
        """Múltiplas chamadas READY concorrentes não quebram estado."""
        h = AgentHarness()
        h.register(make_registration("urn:conc-ready"))

        results = set()
        results.add(h.ready("urn:conc-ready"))  # primeira
        results.add(h.ready("urn:conc-ready"))  # segunda (idempotente)

        # READY é idempotente — ambas retornam True
        assert results == {True}
        assert h.get_state("urn:conc-ready") == AgentLifecycle.READY

    def test_registration_idempotency(self):
        """Registrar mesmo agente 2x → segundo não cria duplicata."""
        h = AgentHarness()
        reg = make_registration("urn:dup")

        first = h.register(reg)
        second = h.register(reg)

        assert first is True
        assert second is False  # False indica que já existia

        # Apenas uma entrada em _agents
        assert len(h._agents) == 1
        assert h.get_state("urn:dup") == AgentLifecycle.REGISTERED

    def test_registration_idempotency_different_objects(self):
        """Registrar mesmo URN com objeto diferente não duplica."""
        h = AgentHarness()
        reg1 = make_registration("urn:dup2", name="First")
        reg2 = make_registration("urn:dup2", name="Second")

        assert h.register(reg1) is True
        assert h.register(reg2) is False  # mesmo URN → False

        # O primeiro registro é preservado
        assert h.get_registration("urn:dup2") is reg1
        assert h.get_registration("urn:dup2").name == "First"


# ═══════════════════════════════════════════════════════════
# TestGlobalConfig — to_dict / with_overrides
# ═══════════════════════════════════════════════════════════


class TestGlobalConfig:
    """Testes para HarnessGlobalConfig.to_dict() e .with_overrides()."""

    EXPECTED_TO_DICT_KEYS: int = 13  # Contagem das chaves em to_dict()

    def test_to_dict_returns_all_fields(self):
        d = HarnessGlobalConfig().to_dict()
        assert isinstance(d, dict)
        assert len(d) == self.EXPECTED_TO_DICT_KEYS

    def test_to_dict_values_match(self):
        cfg = HarnessGlobalConfig()
        d = cfg.to_dict()
        assert d["default_timeout_seconds"] == 30
        assert d["max_timeout_seconds"] == 300
        assert d["context_timeout_seconds"] == 10
        assert d["kg_query_timeout_seconds"] == 5
        assert d["max_retries"] == 3
        assert d["retry_base_delay_seconds"] == 1.0
        assert d["max_concurrent_executions"] == 10
        assert d["log_level"] == "INFO"
        assert d["metrics_enabled"] is True
        assert d["trace_enabled"] is True
        assert d["event_logging"] is True
        assert d["health_check_interval_seconds"] == 30
        assert d["auto_recover"] is True

    def test_with_overrides_partial(self):
        cfg = HarnessGlobalConfig()
        overrides = {
            "log_level": "DEBUG",
            "max_retries": 5,
            "health_check_interval_seconds": 15,
        }
        new = cfg.with_overrides(overrides)
        # 3 overridden
        assert new.log_level == "DEBUG"
        assert new.max_retries == 5
        assert new.health_check_interval_seconds == 15
        # 10 preserved
        assert new.default_timeout_seconds == 30
        assert new.max_timeout_seconds == 300
        assert new.context_timeout_seconds == 10
        assert new.kg_query_timeout_seconds == 5
        assert new.retry_base_delay_seconds == 1.0
        assert new.max_concurrent_executions == 10
        assert new.metrics_enabled is True
        assert new.trace_enabled is True
        assert new.event_logging is True
        assert new.auto_recover is True

    def test_with_overrides_empty(self):
        cfg = HarnessGlobalConfig(log_level="DEBUG")
        new = cfg.with_overrides({})
        assert new.log_level == "DEBUG"
        assert new.default_timeout_seconds == 30

    def test_with_overrides_invalid_key(self):
        """Chave desconhecida é ignorada sem erro."""
        cfg = HarnessGlobalConfig()
        new = cfg.with_overrides({"nonexistent": 42})
        assert new.log_level == "INFO"  # default preservado
        assert not hasattr(new, "nonexistent")
