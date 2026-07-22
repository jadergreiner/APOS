"""Testes do módulo context_engine — ContextBlock e ContextPipeline."""
import json
from datetime import datetime, timezone

import pytest

from apos.context_engine.context import (
    CONTEXT_TEMPLATE,
    CORE_CONTEXT_URNS,
    ContextBlock,
    ContextPipeline,
    PRIORITY_TIERS,
    TOKEN_LIMITS,
    assemble_context,
    calculate_relevance,
    cleanup_context,
    extract_context,
    fallback_strategy,
    get_core_context,
    inject_context,
)
from apos.core.graph import KnowledgeGraph
from apos.core.types import (
    Edge,
    EdgeMetadata,
    EdgeType,
    Node,
    NodeMetadata,
    NodeType,
    make_urn,
)


# ──────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────


@pytest.fixture
def sample_kg() -> KnowledgeGraph:
    kg = KnowledgeGraph()
    task = Node(
        id=make_urn("task", "oauth-123"),
        type=NodeType.TASK,
        attributes={"title": "Implement OAuth Login", "status": "in_progress", "priority": "high"},
        metadata=NodeMetadata(
            created_at="2026-07-15T10:00:00Z",
            updated_at="2026-07-21T14:30:00Z",
            version=3,
        ),
    )
    feature = Node(
        id=make_urn("feature", "faster-auth"),
        type=NodeType.FEATURE,
        attributes={"name": "Faster Authentication", "status": "in_progress", "completeness": 0.75},
        metadata=NodeMetadata(
            created_at="2026-07-10T10:00:00Z",
            updated_at="2026-07-20T14:00:00Z",
            version=4,
        ),
    )
    release = Node(
        id=make_urn("release", "v2-1"),
        type=NodeType.RELEASE,
        attributes={"version": "2.1.0", "status": "in_progress"},
        metadata=NodeMetadata(
            created_at="2026-07-01T08:00:00Z",
            updated_at="2026-07-20T10:00:00Z",
            version=5,
        ),
    )
    okr = Node(
        id=make_urn("okr", "churn-5pct"),
        type=NodeType.OKR,
        attributes={"objective": "Reduce churn by 5%", "status": "on_track"},
        metadata=NodeMetadata(
            created_at="2026-06-15T08:00:00Z",
            updated_at="2026-07-20T09:00:00Z",
            version=6,
        ),
    )
    kg.add_node(task)
    kg.add_node(feature)
    kg.add_node(release)
    kg.add_node(okr)
    kg.add_edge(Edge(
        source=task.id, target=feature.id,
        type=EdgeType.CONTRIBUI_PARA, weight=1.0,
    ))
    kg.add_edge(Edge(
        source=feature.id, target=release.id,
        type=EdgeType.PARTE_DE, weight=1.0,
    ))
    kg.add_edge(Edge(
        source=release.id, target=okr.id,
        type=EdgeType.ALCANCA, weight=0.7,
    ))
    return kg


@pytest.fixture
def sample_block() -> ContextBlock:
    return ContextBlock(
        source="urn:apos:task:oauth-123",
        type="task",
        relevance=0.92,
        content={
            "title": "Implement OAuth Login",
            "status": "in_progress",
            "priority": "high",
        },
        metadata={
            "freshness": "2026-07-21T14:30:00Z",
            "ttl_hours": 24,
            "version": 3,
            "depth": 0,
        },
    )


# ──────────────────────────────────────────────
# ContextBlock
# ──────────────────────────────────────────────


class TestContextBlock:
    def test_create(self, sample_block):
        assert sample_block.source == "urn:apos:task:oauth-123"
        assert sample_block.type == "task"
        assert sample_block.relevance == 0.92
        assert sample_block.content["title"] == "Implement OAuth Login"

    def test_estimate_tokens(self, sample_block):
        tokens = sample_block.estimate_tokens()
        assert isinstance(tokens, int)
        assert tokens > 0

    def test_render_markdown(self, sample_block):
        md = sample_block.render(fmt="markdown")
        assert "**TASK:**" in md
        assert "Relevância:" in md
        assert "Implement OAuth Login" in md

    def test_render_json(self, sample_block):
        js = sample_block.render(fmt="json")
        parsed = json.loads(js)
        assert parsed["source"] == sample_block.source
        assert parsed["relevance"] == 0.92

    def test_compress(self, sample_block):
        compressed = sample_block.compress()
        assert compressed.metadata.get("compressed") is True
        assert compressed.content.get("title") == "Implement OAuth Login"
        assert compressed.content.get("_compressed") is True

    def test_compress_keeps_essentials(self, sample_block):
        """Compressão mantém campos essenciais."""
        sample_block.content["description"] = "Uma descrição longa..."
        compressed = sample_block.compress()
        assert "title" in compressed.content
        assert "status" in compressed.content
        assert "description" not in compressed.content


# ──────────────────────────────────────────────
# Cálculo de Relevância
# ──────────────────────────────────────────────


class TestCalculateRelevance:
    def test_anchor_block_gets_max_score(self, sample_block):
        score = calculate_relevance(
            sample_block,
            anchor_urn="urn:apos:task:oauth-123",
            freshness="2026-07-21T14:30:00Z",
        )
        assert score == 1.0

    def test_depth_1_block(self):
        block = ContextBlock(
            source="urn:apos:feature:faster-auth",
            type="feature",
            metadata={"depth": 1, "edge_weight": 0.8},
        )
        score = calculate_relevance(
            block,
            anchor_urn="urn:apos:task:oauth-123",
            freshness="2026-07-21T14:30:00Z",
        )
        assert 0.6 < score < 1.0

    def test_depth_3_low_relevance(self):
        block = ContextBlock(
            source="urn:apos:metric:some-metric",
            type="metric",
            metadata={"depth": 3, "edge_weight": 0.2},
        )
        score = calculate_relevance(
            block,
            anchor_urn="urn:apos:task:oauth-123",
            freshness="2026-07-01T00:00:00Z",  # muito antigo
        )
        assert score < 0.5

    def test_freshness_decay(self):
        """Bloco muito recente e muito antigo."""
        block = ContextBlock(
            source="urn:apos:task:recent",
            type="task",
            metadata={"depth": 1, "edge_weight": 1.0},
        )
        # Fresco (< 1h)
        fresh_score = calculate_relevance(
            block, anchor_urn="urn:apos:task:anchor",
            freshness=datetime.now(timezone.utc).isoformat(),
        )
        # Antigo (> 72h)
        old_score = calculate_relevance(
            block, anchor_urn="urn:apos:task:anchor",
            freshness="2026-01-01T00:00:00Z",
        )
        assert fresh_score > old_score


# ──────────────────────────────────────────────
# ContextPipeline
# ──────────────────────────────────────────────


class TestExtractContext:
    def test_extract_from_anchor(self, sample_kg):
        raw = extract_context(
            anchor_urn=make_urn("task", "oauth-123"),
            depth=2,
            kg=sample_kg,
        )
        assert len(raw) >= 2  # âncora + pelo menos 1 vizinho
        urns = [r["urn"] for r in raw]
        assert make_urn("task", "oauth-123") in urns
        assert make_urn("feature", "faster-auth") in urns

    def test_extract_without_kg_returns_empty(self):
        assert extract_context("urn:apos:task:test", depth=2) == []


class TestAssembleContext:
    def test_assemble_orders_by_relevance(self, sample_kg):
        raw = extract_context(
            anchor_urn=make_urn("task", "oauth-123"),
            depth=2,
            kg=sample_kg,
        )
        blocks = assemble_context(raw, anchor_urn=make_urn("task", "oauth-123"))
        assert len(blocks) > 0
        # Deve estar ordenado por relevância decrescente
        relevances = [b.relevance for b in blocks]
        assert relevances == sorted(relevances, reverse=True)

    def test_anchor_comes_first(self, sample_kg):
        raw = extract_context(
            anchor_urn=make_urn("task", "oauth-123"),
            depth=2,
            kg=sample_kg,
        )
        blocks = assemble_context(raw, anchor_urn=make_urn("task", "oauth-123"))
        assert blocks[0].source == make_urn("task", "oauth-123")
        assert blocks[0].relevance == 1.0


class TestInjectContext:
    def test_inject_markdown(self, sample_block):
        result = inject_context([sample_block])
        assert "Contexto do Grafo APOS" in result
        assert "TASK" in result

    def test_inject_empty_blocks(self):
        result = inject_context([])
        assert "N/A" in result


class TestCleanupContext:
    def test_cleanup_removes_expired(self, sample_block):
        sample_block.metadata["ttl_hours"] = 0  # expira imediatamente
        sample_block.metadata["freshness"] = "2026-01-01T00:00:00Z"
        cleaned = cleanup_context([sample_block], max_tokens=8000)
        assert len(cleaned) == 0

    def test_cleanup_dedup(self):
        b1 = ContextBlock(
            source="urn:apos:task:same",
            type="task",
            relevance=0.5,
            content={"title": "Old"},
            metadata={"freshness": "2026-01-01T00:00:00Z"},
        )
        b2 = ContextBlock(
            source="urn:apos:task:same",
            type="task",
            relevance=0.9,
            content={"title": "New"},
            metadata={"freshness": "2026-07-21T00:00:00Z"},
        )
        cleaned = cleanup_context([b1, b2])
        assert len(cleaned) == 1
        assert cleaned[0].relevance == 0.9

    def test_cleanup_pruning(self):
        blocks = []
        for i in range(10):
            blocks.append(ContextBlock(
                source=f"urn:apos:task:block-{i}",
                type="task",
                relevance=1.0 - i * 0.1,
                content={"data": "x" * 500},
                metadata={"freshness": "2026-07-21T00:00:00Z"},
            ))
        cleaned = cleanup_context(blocks, max_tokens=300)
        assert len(cleaned) < len(blocks)

    def test_cleanup_compress_large_blocks(self):
        block = ContextBlock(
            source="urn:apos:task:large",
            type="task",
            relevance=0.8,
            content={"data": "x" * 10000},
            metadata={"freshness": "2026-07-21T00:00:00Z"},
        )
        cleaned = cleanup_context([block], block_max_tokens=100)
        assert len(cleaned) == 1
        assert cleaned[0].metadata.get("compressed")


class TestContextPipeline:
    def test_run_pipeline(self, sample_kg):
        pipeline = ContextPipeline(kg=sample_kg)
        result = pipeline.run(
            anchor_urn=make_urn("task", "oauth-123"),
            depth=2,
            max_tokens=8000,
        )
        assert "Contexto APOS" in result
        assert "oauth-123" in result

    def test_run_pipeline_json(self, sample_kg):
        pipeline = ContextPipeline(kg=sample_kg)
        result = pipeline.run(
            anchor_urn=make_urn("task", "oauth-123"),
            depth=2,
            output_format="json",
        )
        # JSON output
        assert '"source"' in result or result.startswith("[")

    def test_run_without_kg(self):
        pipeline = ContextPipeline()
        result = pipeline.run(
            anchor_urn="urn:apos:task:test",
            depth=2,
        )
        assert "Contexto APOS" in result


class TestGetCoreContext:
    def test_includes_anchor(self, sample_kg):
        core = get_core_context(make_urn("task", "oauth-123"), kg=sample_kg)
        assert len(core) >= 1
        assert core[0].relevance == 1.0

    def test_without_kg_returns_empty(self):
        assert get_core_context("urn:apos:task:test") == []


class TestFallbackStrategy:
    def test_full_mode(self, sample_block):
        core, mode = fallback_strategy([sample_block], max_tokens=8000)
        assert mode == "full"
        assert len(core) == 1

    def test_urns_only_when_extreme(self, sample_block):
        sample_block.content = {"x": "y" * 100000}
        core, mode = fallback_strategy([sample_block], max_tokens=100)
        assert mode == "urns_only"


# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────


class TestConstants:
    def test_priority_tiers(self):
        assert PRIORITY_TIERS["critical"] == (0.8, 1.0)
        assert PRIORITY_TIERS["high"] == (0.5, 0.79)
        assert PRIORITY_TIERS["normal"] == (0.0, 0.49)

    def test_token_limits(self):
        assert abs(TOKEN_LIMITS["critical"] - 0.50) < 0.01
        assert abs(TOKEN_LIMITS["high"] - 0.35) < 0.01
        assert abs(TOKEN_LIMITS["normal"] - 0.15) < 0.01

    def test_core_context_urns(self):
        assert CORE_CONTEXT_URNS["min_always"] == 1
        assert CORE_CONTEXT_URNS["min_blockers"] == 5
