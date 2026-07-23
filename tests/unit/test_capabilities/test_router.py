"""Testes unitarios para apos/capabilities/router.py (R1-R15)."""

import time
from unittest.mock import patch

import pytest

from apos.capabilities.router import (
    CacheEntry,
    CapabilityRequest,
    CapabilityRouter,
    MatchStrategy,
    NoCapabilityResult,
    ResolutionResult,
    create_default_router,
)


# ===================================================================
# R1 — register_capability
# ===================================================================
class TestCapabilityRouter:
    """15 cenarios para CapabilityRouter."""

    def test_register_capability(self):
        """R1: register_capability() armazena a capability."""
        router = CapabilityRouter()
        router.register_capability("my.cap", {"name": "Minha Cap", "domain": "core"})
        assert router._capabilities["my.cap"] == {"name": "Minha Cap", "domain": "core"}
        assert len(router._capabilities) == 1

    # ------------------------------------------------------------------
    # R2 — register_agent
    # ------------------------------------------------------------------
    def test_register_agent(self):
        """R2: register_agent(urn, cap_id) mapeia agente -> capability."""
        router = CapabilityRouter()
        router.register_capability("cap.a", {"name": "Cap A"})
        router.register_agent("urn:apos:agent:alpha", "cap.a")
        assert router._agents["urn:apos:agent:alpha"] == "cap.a"

    # ------------------------------------------------------------------
    # R3 — resolve exato
    # ------------------------------------------------------------------
    def test_resolve_exact(self):
        """R3: resolve() com match exato por URN -> ResolutionResult."""
        router = CapabilityRouter()
        router.register_capability("graph.traverse", {"name": "Navegar Grafo"})
        router.register_agent("urn:apos:agent:kg", "graph.traverse")

        req = CapabilityRequest(id="r1", target="graph.traverse")
        result = router.resolve(req)

        assert isinstance(result, ResolutionResult)
        assert result.capability_id == "graph.traverse"
        assert result.match_strategy == MatchStrategy.EXACT
        # Agente mapeado
        assert result.agent_urn == "urn:apos:agent:kg"

    # ------------------------------------------------------------------
    # R4 — resolve por node_type
    # ------------------------------------------------------------------
    def test_resolve_node_type(self):
        """R4: resolve() cai em _match_by_node_type quando exact falha."""
        router = CapabilityRouter()
        router.register_capability(
            "task.router",
            {
                "name": "Roteador de Tarefas",
                "domain": "core",
                "kg_read": {"node_types": ["task"]},
            },
        )
        router.register_agent("urn:apos:agent:tasks", "task.router")

        # URN com tipo "task" -> deve resolver por node_type
        req = CapabilityRequest(id="r4", target="urn:apos:task:123")
        result = router.resolve(req)

        assert isinstance(result, ResolutionResult)
        assert result.capability_id == "task.router"
        assert result.match_strategy == MatchStrategy.NODE_TYPE
        assert 0.0 < result.confidence <= 1.0

    # ------------------------------------------------------------------
    # R5 — resolve por similaridade
    # ------------------------------------------------------------------
    def test_resolve_similarity(self):
        """R5: resolve() cai em _match_by_similarity como fallback."""
        router = CapabilityRouter()
        router.register_capability(
            "metrics.pipeline",
            {
                "name": "Pipeline de Métricas",
                "description": "processa metricas de sprint",
            },
        )
        router.register_agent("urn:apos:agent:metrics", "metrics.pipeline")

        # target com overlap de palavras com a descricao
        req = CapabilityRequest(id="r5", target="metricas sprint")
        result = router.resolve(req)

        assert isinstance(result, ResolutionResult)
        # Como "metricas" e "sprint" aparecem na descricao, deve cair em similarity
        assert result.match_strategy == MatchStrategy.SIMILARITY
        assert result.confidence > 0.3

    # ------------------------------------------------------------------
    # R6 — nenhum match
    # ------------------------------------------------------------------
    def test_resolve_no_match(self):
        """R6: nenhum match -> LookupError (codigo atual)."""
        router = CapabilityRouter()
        req = CapabilityRequest(id="r6", target="completely.unknown.target")

        with pytest.raises(LookupError, match="Nenhuma capability encontrada"):
            router.resolve(req)

        # NoCapabilityResult esta definido no modulo (never used in resolve)
        # Mas podemos validar que a dataclass existe
        ncr = NoCapabilityResult(request=req, suggestions=["cap.a"], hint="tente cap.a")
        assert ncr.request is req
        assert ncr.suggestions == ["cap.a"]
        assert ncr.hint == "tente cap.a"

    # ------------------------------------------------------------------
    # R7 — resolve_chain
    # ------------------------------------------------------------------
    def test_resolve_chain(self):
        """R7: resolve_chain() retorna lista ordenada de resultados."""
        router = CapabilityRouter()
        router.register_capability(
            "cap.a",
            {"name": "Cap A", "domain": "core", "routes_to": "cap.b"},
        )
        router.register_capability(
            "cap.b",
            {"name": "Cap B", "domain": "core"},
        )
        router.register_agent("urn:apos:agent:a", "cap.a")
        router.register_agent("urn:apos:agent:b", "cap.b")

        req = CapabilityRequest(id="chain1", target="cap.a")
        results = router.resolve_chain(req, max_depth=5)

        assert isinstance(results, list)
        assert len(results) >= 2
        assert results[0].capability_id == "cap.a"
        assert results[1].capability_id == "cap.b"

    # ------------------------------------------------------------------
    # R8 — resolve_chain vazia
    # ------------------------------------------------------------------
    def test_resolve_chain_empty(self):
        """R8: resolve_chain sem match -> lista vazia."""
        router = CapabilityRouter()
        req = CapabilityRequest(id="chain_empty", target="nothing.here")
        results = router.resolve_chain(req)
        assert results == []

    # ------------------------------------------------------------------
    # R9 — cache hit
    # ------------------------------------------------------------------
    def test_cache_hit(self):
        """R9: mesma request 2x -> usa cache (confere tempo)."""
        router = CapabilityRouter()
        router.register_capability("fast.cap", {"name": "Cap Rapida"})
        router.register_agent("urn:apos:agent:fast", "fast.cap")

        req = CapabilityRequest(id="c1", target="fast.cap")

        # Primeira chamada — popula cache
        result1 = router.resolve(req)
        assert router.cache_size == 1

        # Cache key deve existir
        cache_key = f"{req.type}:{req.target}"
        assert cache_key in router._cache

        # Segunda chamada — hit no cache
        result2 = router.resolve(req)

        assert result1 is result2  # mesma instancia (cache devolve o objeto armazenado)

    # ------------------------------------------------------------------
    # R10 — cache expired
    # ------------------------------------------------------------------
    def test_cache_expired(self):
        """R10: CacheEntry.expired() apos TTL."""
        res = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.EXACT,
            confidence=1.0,
        )

        # Entrada fresca — nao expirou
        fresh = CacheEntry(result=res, ttl=3600)
        assert not fresh.expired

        # Entrada com created_at antigo — expirou
        past = CacheEntry(result=res, created_at=0, ttl=1)
        assert past.expired

        # Entrada com ttl=0 — expirou imediatamente
        instant = CacheEntry(result=res, created_at=time.time(), ttl=0)
        assert instant.expired

    # ------------------------------------------------------------------
    # R11 — invalidate_cache all
    # ------------------------------------------------------------------
    def test_invalidate_cache_all(self):
        """R11: invalidate_cache() limpa todo o cache."""
        router = CapabilityRouter()
        router.register_capability("cap.x", {"name": "Cap X"})
        router.register_agent("urn:apos:agent:x", "cap.x")

        # Forcar cache
        req = CapabilityRequest(id="inv1", target="cap.x")
        router.resolve(req)
        assert router.cache_size > 0

        router.invalidate_cache()
        assert router.cache_size == 0

    # ------------------------------------------------------------------
    # R12 — invalidate_cache target
    # ------------------------------------------------------------------
    def test_invalidate_cache_target(self):
        """R12: invalidate_cache('id') limpa so um alvo."""
        router = CapabilityRouter()
        router.register_capability("cap.a", {"name": "Cap A"})
        router.register_capability("cap.b", {"name": "Cap B"})
        router.register_agent("urn:apos:agent:a", "cap.a")
        router.register_agent("urn:apos:agent:b", "cap.b")

        # Popular cache com 2 entradas
        router.resolve(CapabilityRequest(id="a", target="cap.a"))
        router.resolve(CapabilityRequest(id="b", target="cap.b"))
        assert router.cache_size == 2

        # Invalidar apenas cap.a — cache key é "capability:cap.a"
        router.invalidate_cache("cap.a")
        assert router.cache_size == 1  # sobra "capability:cap.b"

        # Invalidar cap.b — zera cache
        router.invalidate_cache("cap.b")
        assert router.cache_size == 0

    # ------------------------------------------------------------------
    # R13 — CapabilityRequest
    # ------------------------------------------------------------------
    def test_capability_request(self):
        """R13: CapabilityRequest com todos os campos."""
        req = CapabilityRequest(
            id="req-001",
            type="custom",
            target="urn:apos:agent:hermes",
            params={"key": "value"},
            context={"env": "prod"},
            metadata={"source": "test"},
        )
        assert req.id == "req-001"
        assert req.type == "custom"
        assert req.target == "urn:apos:agent:hermes"
        assert req.params == {"key": "value"}
        assert req.context == {"env": "prod"}
        assert req.metadata == {"source": "test"}

    def test_capability_request_defaults(self):
        """R13b: CapabilityRequest com defaults."""
        req = CapabilityRequest(id="minimo")
        assert req.type == "capability"
        assert req.target == ""
        assert req.params == {}
        assert req.context == {}
        assert req.metadata == {}

    # ------------------------------------------------------------------
    # R14 — ResolutionResult confidence
    # ------------------------------------------------------------------
    def test_resolution_result_confidence_range(self):
        """R14: ResolutionResult confidence entre 0 e 1."""
        # Confianca baixa
        low = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.SIMILARITY,
            confidence=0.0,
        )
        assert 0.0 <= low.confidence <= 1.0

        # Confianca alta
        high = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.EXACT,
            confidence=1.0,
        )
        assert 0.0 <= high.confidence <= 1.0

        # Confianca media
        mid = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.NODE_TYPE,
            confidence=0.75,
        )
        assert 0.0 <= mid.confidence <= 1.0

    def test_resolution_result_chain(self):
        """R14b: ResolutionResult pode carregar chain."""
        result = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.EXACT,
            confidence=1.0,
            chain=["cap.a", "cap.b"],
        )
        assert result.chain == ["cap.a", "cap.b"]

    def test_resolution_result_defaults(self):
        """R14c: ResolutionResult confidence default 1.0."""
        result = ResolutionResult(
            capability_id="c",
            agent_urn="u",
            match_strategy=MatchStrategy.EXACT,
        )
        assert result.confidence == 1.0
        assert result.chain == []

    # ------------------------------------------------------------------
    # R15 — create_default_router
    # ------------------------------------------------------------------
    def test_create_default_router(self):
        """R15: create_default_router() retorna roteador configurado."""
        router = create_default_router()

        # Deve ter 6 capabilities
        assert len(router._capabilities) == 6
        assert "trust_score.calculate" in router._capabilities
        assert "orphans.detect" in router._capabilities
        assert "context.assemble" in router._capabilities
        assert "graph.traverse" in router._capabilities
        assert "governance.validate" in router._capabilities
        assert "capability.router" in router._capabilities

        # Deve ter 5 agentes
        assert len(router._agents) == 5
        assert router._agents["urn:apos:agent:hermes"] == "context.assemble"
        assert router._agents["urn:apos:agent:knowledge-graph"] == "graph.traverse"
        assert router._agents["urn:apos:agent:trust-score"] == "trust_score.calculate"
        assert router._agents["urn:apos:agent:governance"] == "governance.validate"
        assert router._agents["urn:apos:agent:capability-router"] == "capability.router"

    def test_create_default_router_resolve(self):
        """R15b: default router consegue resolver requests conhecidos."""
        router = create_default_router()

        # Match exato por URN de capability
        req = CapabilityRequest(id="t1", target="graph.traverse")
        result = router.resolve(req)
        assert result.capability_id == "graph.traverse"
        assert result.agent_urn == "urn:apos:agent:knowledge-graph"

        # Match por node_type: "sprint" aparece nos node_types do graph.traverse
        req2 = CapabilityRequest(id="t2", target="urn:apos:sprint:s01")
        result2 = router.resolve(req2)
        assert result2.match_strategy == MatchStrategy.NODE_TYPE
