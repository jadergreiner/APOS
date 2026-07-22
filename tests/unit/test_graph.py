"""
Testes unitários para o Knowledge Graph do APOS (T0.4.5 / T0.4.6).

Cobre:
- Types: Node, Edge, enums, helpers (make_urn, parse_urn, is_valid_urn)
- Graph CRUD: add_node, get_node, update_node, remove_node
- Edge CRUD: add_edge, get_edges, get_neighbors, validações KG-002/006/007/008/009/012
- Traverse: navegação multi-edge (cadeia Task→Feature→Release→OKR)
- Inferência de impacto: infer_impact
- Detecção de órfãos: detect_orphans
- Serialização: to_dict / from_dict roundtrip
"""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from apos.core import (
    Edge,
    EdgeMetadata,
    EdgeType,
    KnowledgeGraph,
    Node,
    NodeMetadata,
    NodeType,
    is_valid_urn,
    make_urn,
    parse_urn,
)


# ═══════════════════════════════════════════════
# Helpers para testes
# ═══════════════════════════════════════════════

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_task(
    local_id: str = "task-001",
    title: str = "Test Task",
    status: str = "open",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("task", local_id),
        type=NodeType.TASK,
        attributes={"title": title, "status": status, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_feature(
    local_id: str = "feature-001",
    name: str = "Test Feature",
    status: str = "planned",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("feature", local_id),
        type=NodeType.FEATURE,
        attributes={"name": name, "status": status, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_release(
    local_id: str = "release-001",
    version: str = "1.0.0",
    status: str = "planned",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("release", local_id),
        type=NodeType.RELEASE,
        attributes={"version": version, "status": status, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_okr(
    local_id: str = "okr-001",
    objective: str = "Test OKR",
    status: str = "on_track",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("okr", local_id),
        type=NodeType.OKR,
        attributes={"objective": objective, "status": status, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_metric(
    local_id: str = "metric-001",
    name: str = "Test Metric",
    unit: str = "percent",
    target: float = 100.0,
    **attrs,
) -> Node:
    return Node(
        id=make_urn("metric", local_id),
        type=NodeType.METRIC,
        attributes={"name": name, "unit": unit, "target": target, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_sprint(
    local_id: str = "sprint-001",
    name: str = "Sprint 1",
    status: str = "active",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("sprint", local_id),
        type=NodeType.SPRINT,
        attributes={"name": name, "status": status, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def make_persona(
    local_id: str = "persona-001",
    name: str = "Developer",
    role: str = "engineer",
    **attrs,
) -> Node:
    return Node(
        id=make_urn("persona", local_id),
        type=NodeType.PERSONA,
        attributes={"name": name, "role": role, **attrs},
        metadata=NodeMetadata(created_at=now_iso(), updated_at=now_iso()),
    )


def full_graph() -> KnowledgeGraph:
    """Cria um grafo completo para testes (baseado no exemplo da secao 8 de KNOWLEDGE_GRAPH.md)."""
    kg = KnowledgeGraph()

    # Nodes
    t1 = make_task("oauth-123", "Implement OAuth Login", "in_progress",
                    priority="high", story_points=5, owner="agent-oauth",
                    tags=["auth", "security"])
    t2 = make_task("rate-limit", "Add API Rate Limiting", "open",
                    priority="medium", story_points=3, owner="agent-infra",
                    tags=["infra", "security"])
    t3 = make_task("session-mgmt", "Session Management", "done",
                    priority="high", story_points=8, owner="agent-auth",
                    tags=["auth", "infra"])
    f1 = make_feature("faster-auth", "Faster Authentication", "in_progress",
                       completeness=0.75, owner="team-auth",
                       description="Reduzir tempo de login para < 2s")
    r1 = make_release("v2-1", "2.1.0", "in_progress",
                      date="2026-07-31", name="Summer Release 2026")
    o1 = make_okr("churn-5pct", "Reduce customer churn by 5%", "on_track",
                   target_value=5.0, current_value=3.2, owner="jader",
                   quarter="2026-Q3")
    o2 = make_okr("perf-10pct", "Improve system performance by 10%", "at_risk",
                   target_value=10.0, current_value=4.5, owner="jader",
                   quarter="2026-Q3")
    m1 = make_metric("login-time", "Login Time", "seconds", 2.0,
                      current_value=2.5, direction="lower_is_better",
                      status="at_risk", formula="avg(login_duration_ms) / 1000")
    m2 = make_metric("error-rate", "API Error Rate", "percent", 0.5,
                      current_value=0.3, direction="lower_is_better",
                      status="healthy", formula="(error_count / total_requests) * 100")
    s1 = make_sprint("s0-4", "Sprint 0.4", "active",
                     start_date="2026-07-21", end_date="2026-07-25",
                     goal="Finalizar design do Knowledge Graph")
    p1 = make_persona("developer", "Developer", "engineer",
                      description="Engenheiro de software que implementa features",
                      impact="Impactado por mudanças na API de autenticação")

    for node in [t1, t2, t3, f1, r1, o1, o2, m1, m2, s1, p1]:
        kg.add_node(node)

    # Edges
    ts = now_iso()
    edges = [
        Edge(source=t1.id, target=f1.id, type=EdgeType.CONTRIBUI_PARA, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=t2.id, target=f1.id, type=EdgeType.CONTRIBUI_PARA, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=t3.id, target=f1.id, type=EdgeType.CONTRIBUI_PARA, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=f1.id, target=r1.id, type=EdgeType.PARTE_DE, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=r1.id, target=o1.id, type=EdgeType.ALCANCA, weight=0.7,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=0.9)),
        Edge(source=r1.id, target=o2.id, type=EdgeType.ALCANCA, weight=0.5,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=0.8)),
        Edge(source=o1.id, target=m1.id, type=EdgeType.MEDIDO_POR, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=o2.id, target=m2.id, type=EdgeType.MEDIDO_POR, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=t1.id, target=m1.id, type=EdgeType.IMPACTA, weight=0.8,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=0.9)),
        Edge(source=t1.id, target=m2.id, type=EdgeType.IMPACTA, weight=0.3,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=0.7)),
        Edge(source=t2.id, target=m2.id, type=EdgeType.IMPACTA, weight=0.5,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=0.8)),
        Edge(source=t1.id, target=s1.id, type=EdgeType.PERTENCE_A, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=t2.id, target=s1.id, type=EdgeType.PERTENCE_A, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=t3.id, target=s1.id, type=EdgeType.PERTENCE_A, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=f1.id, target=p1.id, type=EdgeType.ENVOLVE, weight=1.0,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
        Edge(source=m1.id, target=m1.id, type=EdgeType.ATINGE, weight=0.8,
             metadata=EdgeMetadata(created_at=ts, updated_at=ts, confidence=1.0)),
    ]
    for edge in edges:
        kg.add_edge(edge)

    return kg


# ═══════════════════════════════════════════════
# Testes: Types
# ═══════════════════════════════════════════════

class TestNodeType:
    def test_values(self):
        assert NodeType.TASK.value == "task"
        assert NodeType.FEATURE.value == "feature"
        assert NodeType.RELEASE.value == "release"
        assert NodeType.OKR.value == "okr"
        assert NodeType.METRIC.value == "metric"
        assert NodeType.SPRINT.value == "sprint"
        assert NodeType.PERSONA.value == "persona"

    def test_str(self):
        assert str(NodeType.TASK) == "task"


class TestEdgeType:
    def test_values(self):
        assert EdgeType.CONTRIBUI_PARA.value == "contribui_para"
        assert EdgeType.PARTE_DE.value == "parte_de"
        assert EdgeType.ALCANCA.value == "alcanca"
        assert EdgeType.MEDIDO_POR.value == "medido_por"
        assert EdgeType.IMPACTA.value == "impacta"
        assert EdgeType.BLOQUEIA.value == "bloqueia"
        assert EdgeType.DEPENDE_DE.value == "depende_de"
        assert EdgeType.PERTENCE_A.value == "pertence_a"
        assert EdgeType.ENVOLVE.value == "envolve"
        assert EdgeType.ATINGE.value == "atinge"

    def test_str(self):
        assert str(EdgeType.CONTRIBUI_PARA) == "contribui_para"


class TestNodeMetadata:
    def test_defaults(self):
        m = NodeMetadata(created_at="2026-01-01", updated_at="2026-01-02")
        assert m.created_at == "2026-01-01"
        assert m.updated_at == "2026-01-02"
        assert m.version == 1
        assert m.source is None
        assert m.description is None

    def test_custom(self):
        m = NodeMetadata(
            created_at="2026-01-01", updated_at="2026-01-02",
            version=3, source="jira:PROJ-456",
            description="My node",
        )
        assert m.version == 3
        assert m.source == "jira:PROJ-456"
        assert m.description == "My node"


class TestNode:
    def test_create_minimal(self):
        n = Node(
            id="urn:apos:task:test",
            type=NodeType.TASK,
        )
        assert n.id == "urn:apos:task:test"
        assert n.type == NodeType.TASK
        assert n.attributes == {}
        assert n.metadata.version == 1

    def test_create_full(self):
        n = Node(
            id="urn:apos:task:test",
            type=NodeType.TASK,
            attributes={"title": "Test", "status": "open"},
            metadata=NodeMetadata(
                created_at="2026-01-01T00:00:00Z",
                updated_at="2026-01-02T00:00:00Z",
                version=2,
            ),
        )
        assert n.attributes["title"] == "Test"
        assert n.metadata.version == 2


class TestEdgeMetadata:
    def test_defaults(self):
        m = EdgeMetadata(created_at="2026-01-01", updated_at="2026-01-02")
        assert m.version == 1
        assert m.confidence == 1.0
        assert m.reason is None


class TestEdge:
    def test_create_minimal(self):
        e = Edge(
            source="urn:apos:task:src",
            target="urn:apos:feature:tgt",
            type=EdgeType.CONTRIBUI_PARA,
            metadata=EdgeMetadata(created_at="2026-01-01", updated_at="2026-01-01"),
        )
        assert e.weight == 1.0
        assert e.metadata.confidence == 1.0

    def test_create_full(self):
        e = Edge(
            source="urn:apos:task:src",
            target="urn:apos:feature:tgt",
            type=EdgeType.CONTRIBUI_PARA,
            weight=0.7,
            metadata=EdgeMetadata(
                created_at="2026-01-01", updated_at="2026-01-01",
                confidence=0.8, reason="Test",
            ),
        )
        assert e.weight == 0.7
        assert e.metadata.confidence == 0.8
        assert e.metadata.reason == "Test"


class TestMakeURN:
    def test_basic(self):
        assert make_urn("task", "oauth-123") == "urn:apos:task:oauth-123"

    def test_normalizes_spaces(self):
        assert make_urn("task", "OAuth login") == "urn:apos:task:oauth-login"

    def test_normalizes_underscores(self):
        assert make_urn("feature", "Faster_Auth") == "urn:apos:feature:faster-auth"

    def test_normalizes_uppercase(self):
        assert make_urn("release", "V2.1") == "urn:apos:release:v21"

    def test_strips_invalid_chars(self):
        urn = make_urn("okr", "Churn 5%")
        # % is stripped; only [a-z0-9-] remains
        assert urn == "urn:apos:okr:churn-5"
        assert "%" not in urn

    def test_no_double_hyphens(self):
        urn = make_urn("sprint", "Sprint--0.4")
        assert "--" not in urn


class TestParseURN:
    def test_valid(self):
        result = parse_urn("urn:apos:task:oauth-123")
        assert result == ("task", "oauth-123")

    def test_invalid_prefix(self):
        assert parse_urn("urn:other:task:x") is None

    def test_invalid_format(self):
        assert parse_urn("not-a-urn") is None


class TestIsValidURN:
    def test_valid(self):
        assert is_valid_urn("urn:apos:feature:faster-auth") is True

    def test_invalid(self):
        assert is_valid_urn("invalid") is False

    def test_invalid_prefix(self):
        assert is_valid_urn("urn:other:task:x") is False


# ═══════════════════════════════════════════════
# Testes: KnowledgeGraph CRUD - Nodes
# ═══════════════════════════════════════════════

class TestKnowledgeGraphNodeCRUD:
    def test_add_node(self):
        kg = KnowledgeGraph()
        task = make_task()
        kg.add_node(task)
        assert kg.node_count == 1
        assert kg.get_node(task.id) is task

    def test_add_node_duplicate_urn(self):
        kg = KnowledgeGraph()
        kg.add_node(make_task())
        with pytest.raises(ValueError, match="KG-001"):
            kg.add_node(make_task())

    def test_get_node_nonexistent(self):
        kg = KnowledgeGraph()
        assert kg.get_node("urn:apos:task:nonexistent") is None

    def test_update_node_attributes(self):
        kg = KnowledgeGraph()
        task = make_task()
        kg.add_node(task)
        kg.update_node(task.id, attributes={"status": "done"})
        assert task.attributes["status"] == "done"

    def test_update_node_metadata(self):
        kg = KnowledgeGraph()
        task = make_task()
        kg.add_node(task)
        kg.update_node(task.id, metadata={"version": 5})
        assert task.metadata.version == 5

    def test_update_node_nonexistent(self):
        kg = KnowledgeGraph()
        assert kg.update_node("urn:apos:task:nonexistent", attributes={"x": 1}) is False

    def test_remove_node(self):
        kg = full_graph()
        assert kg.node_count == 11
        ok = kg.remove_node("urn:apos:task:oauth-123")
        assert ok is True
        assert kg.node_count == 10
        assert kg.get_node("urn:apos:task:oauth-123") is None
        # Arestas conectadas devem ter sido removidas
        assert kg.edge_count == 12  # 16 - 4 (contribui_para, pertence_a, 2x impacta)

    def test_remove_node_nonexistent(self):
        kg = KnowledgeGraph()
        assert kg.remove_node("urn:apos:task:nonexistent") is False

    def test_remove_node_empty_graph(self):
        kg = KnowledgeGraph()
        assert kg.remove_node("anything") is False

    @pytest.mark.parametrize("invalid_type", ["task", 123, None, []])
    def test_add_node_invalid_type(self, invalid_type):
        kg = KnowledgeGraph()
        n = Node(id="test", type=invalid_type)  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="Node.type inválido"):
            kg.add_node(n)


# ═══════════════════════════════════════════════
# Testes: KnowledgeGraph CRUD - Edges
# ═══════════════════════════════════════════════

class TestKnowledgeGraphEdgeCRUD:
    def test_add_edge_basic(self):
        kg = KnowledgeGraph()
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        e = Edge(
            source=t.id, target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        kg.add_edge(e)
        assert kg.edge_count == 1

    def test_add_edge_nonexistent_source(self):
        kg = KnowledgeGraph()
        f = make_feature()
        kg.add_node(f)
        e = Edge(
            source="urn:apos:task:nonexistent",
            target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-006"):
            kg.add_edge(e)

    def test_add_edge_nonexistent_target(self):
        kg = KnowledgeGraph()
        t = make_task()
        kg.add_node(t)
        e = Edge(
            source=t.id,
            target="urn:apos:feature:nonexistent",
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-007"):
            kg.add_edge(e)

    @pytest.mark.parametrize("weight", [-0.1, 1.5, 2.0, -5])
    def test_add_edge_invalid_weight(self, weight):
        kg = KnowledgeGraph()
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        e = Edge(
            source=t.id, target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=weight,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-012"):
            kg.add_edge(e)

    def test_add_edge_invalid_type_task_to_release(self):
        """KG-002: Task → Release não é válido para nenhum EdgeType."""
        kg = KnowledgeGraph()
        t = make_task()
        r = make_release()
        kg.add_node(t)
        kg.add_node(r)
        e = Edge(
            source=t.id, target=r.id,
            type=EdgeType.CONTRIBUI_PARA,  # Task → Release via contribui_para é inválido
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-002"):
            kg.add_edge(e)

    def test_add_edge_invalid_type_feature_to_metric(self):
        """KG-002: Feature → Metric não é válido."""
        kg = KnowledgeGraph()
        f = make_feature()
        m = make_metric()
        kg.add_node(f)
        kg.add_node(m)
        e = Edge(
            source=f.id, target=m.id,
            type=EdgeType.IMPACTA,  # Feature → Metric via impacta é inválido
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-002"):
            kg.add_edge(e)

    def test_add_edge_duplicate_merge(self):
        """Edge idêntica (source, target, type) faz merge de weight + confidence."""
        kg = KnowledgeGraph()
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        e1 = Edge(
            source=t.id, target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso(), confidence=1.0),
        )
        kg.add_edge(e1)
        e2 = Edge(
            source=t.id, target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=0.5,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso(), confidence=0.7),
        )
        kg.add_edge(e2)
        assert kg.edge_count == 1
        assert kg._edges[0].weight == 0.5
        assert kg._edges[0].metadata.confidence == 0.7

    def test_get_edges(self):
        kg = full_graph()
        urn = "urn:apos:task:oauth-123"
        edges = kg.get_edges(urn)
        # Esta task tem: contribui_para, 2x impacta, pertence_a = 4 outgoing
        assert len(edges) == 4

    def test_get_neighbors_all(self):
        kg = full_graph()
        urn = "urn:apos:task:oauth-123"
        neighbors = kg.get_neighbors(urn)
        # outgoing: feature(1), metric(2), sprint(1) = 4
        assert len(neighbors) == 4

    def test_get_neighbors_filtered(self):
        kg = full_graph()
        urn = "urn:apos:task:oauth-123"
        neighbors = kg.get_neighbors(urn, EdgeType.IMPACTA)
        assert len(neighbors) == 2
        targets = {n[0] for n in neighbors}
        assert "urn:apos:metric:login-time" in targets
        assert "urn:apos:metric:error-rate" in targets

    def test_cardinality_task_feature(self):
        """KG-008: Task só pode ter 1 contribui_para."""
        kg = KnowledgeGraph()
        t = make_task()
        f1 = make_feature("f1")
        f2 = make_feature("f2")
        kg.add_node(t)
        kg.add_node(f1)
        kg.add_node(f2)
        e1 = Edge(
            source=t.id, target=f1.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        kg.add_edge(e1)
        e2 = Edge(
            source=t.id, target=f2.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=0.5,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-008"):
            kg.add_edge(e2)

    def test_cardinality_feature_release(self):
        """KG-009: Feature só pode ter 1 parte_de."""
        kg = KnowledgeGraph()
        f = make_feature()
        r1 = make_release("r1")
        r2 = make_release("r2")
        kg.add_node(f)
        kg.add_node(r1)
        kg.add_node(r2)
        e1 = Edge(
            source=f.id, target=r1.id,
            type=EdgeType.PARTE_DE,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        kg.add_edge(e1)
        e2 = Edge(
            source=f.id, target=r2.id,
            type=EdgeType.PARTE_DE,
            weight=0.5,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-009"):
            kg.add_edge(e2)


# ═══════════════════════════════════════════════
# Testes: Traverse
# ═══════════════════════════════════════════════

class TestTraverse:
    def test_traverse_single_hop(self):
        kg = full_graph()
        results = kg.traverse(
            "urn:apos:task:oauth-123",
            [EdgeType.CONTRIBUI_PARA],
        )
        assert len(results) == 1
        assert results[0][0] == "urn:apos:feature:faster-auth"

    def test_traverse_canonical_chain(self):
        """Cadeia: Task → Feature → Release → OKR."""
        kg = full_graph()
        results = kg.traverse(
            "urn:apos:task:oauth-123",
            [
                EdgeType.CONTRIBUI_PARA,
                EdgeType.PARTE_DE,
                EdgeType.ALCANCA,
            ],
        )
        # Espera 2 OKRs
        urns = {r[0] for r in results}
        assert "urn:apos:okr:churn-5pct" in urns
        assert "urn:apos:okr:perf-10pct" in urns

    def test_traverse_empty_result(self):
        kg = full_graph()
        # A partir de uma persona, alcanca não tem sentido
        results = kg.traverse(
            "urn:apos:persona:developer",
            [EdgeType.ALCANCA],
        )
        assert results == []

    def test_traverse_no_nodes_found(self):
        kg = KnowledgeGraph()
        results = kg.traverse("urn:apos:task:nonexistent", [EdgeType.CONTRIBUI_PARA])
        assert results == []


# ═══════════════════════════════════════════════
# Testes: Inferência de Impacto
# ═══════════════════════════════════════════════

class TestInferImpact:
    def test_infer_impact_from_task(self):
        kg = full_graph()
        impacts = kg.infer_impact("urn:apos:task:oauth-123")
        # Deve encontrar vários nós via BFS bidirecional
        urns = {i["urn"] for i in impacts}
        # Forward: feature, release, okrs, metrics, sprint, persona
        assert "urn:apos:feature:faster-auth" in urns
        assert "urn:apos:release:v2-1" in urns
        assert "urn:apos:okr:churn-5pct" in urns
        assert "urn:apos:okr:perf-10pct" in urns
        assert "urn:apos:metric:login-time" in urns
        assert "urn:apos:metric:error-rate" in urns
        assert "urn:apos:sprint:s0-4" in urns
        assert "urn:apos:persona:developer" in urns

    def test_infer_impact_distance_and_confidence(self):
        kg = full_graph()
        impacts = kg.infer_impact("urn:apos:task:oauth-123")
        # Feature está a distance 1
        feat = [i for i in impacts if i["urn"] == "urn:apos:feature:faster-auth"]
        assert len(feat) == 1
        assert feat[0]["distance"] >= 1
        # Metric login-time via impacta direct (w=0.8)
        metrics = [i for i in impacts if i["urn"] == "urn:apos:metric:login-time"]
        assert len(metrics) >= 1
        # Pode chegar tanto via impacta direto quanto via cadeia

    def test_infer_impact_no_edges(self):
        kg = KnowledgeGraph()
        t = make_task()
        kg.add_node(t)
        impacts = kg.infer_impact(t.id)
        assert impacts == []


# ═══════════════════════════════════════════════
# Testes: Detecção de Órfãos
# ═══════════════════════════════════════════════

class TestDetectOrphans:
    def test_no_orphans_in_full_graph(self):
        kg = full_graph()
        orphans = kg.detect_orphans()
        # No grafo completo, todos os nós têm suas conexões obrigatórias
        assert len(orphans) == 0

    def test_orphan_task(self):
        kg = KnowledgeGraph()
        t = make_task()
        kg.add_node(t)
        orphans = kg.detect_orphans()
        assert len(orphans) == 1
        assert orphans[0].type == NodeType.TASK

    def test_orphan_feature(self):
        kg = KnowledgeGraph()
        f = make_feature()
        kg.add_node(f)
        orphans = kg.detect_orphans()
        assert len(orphans) == 1
        assert orphans[0].type == NodeType.FEATURE

    def test_orphan_okr(self):
        kg = KnowledgeGraph()
        o = make_okr()
        kg.add_node(o)
        orphans = kg.detect_orphans()
        assert len(orphans) == 1
        assert orphans[0].type == NodeType.OKR

    def test_orphan_metric(self):
        kg = KnowledgeGraph()
        m = make_metric()
        kg.add_node(m)
        orphans = kg.detect_orphans()
        assert len(orphans) == 1
        assert orphans[0].type == NodeType.METRIC

    def test_orphan_filter_by_type(self):
        kg = KnowledgeGraph()
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        # Filtra só por Feature
        feature_orphans = kg.detect_orphans(node_type=NodeType.FEATURE)
        assert len(feature_orphans) == 1
        assert feature_orphans[0].type == NodeType.FEATURE

    def test_empty_graph_no_orphans(self):
        kg = KnowledgeGraph()
        assert kg.detect_orphans() == []


# ═══════════════════════════════════════════════
# Testes: Serialização
# ═══════════════════════════════════════════════

class TestSerialization:
    def test_to_dict_roundtrip(self):
        kg1 = full_graph()
        data = kg1.to_dict()

        # Verifica keys
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 11
        assert len(data["edges"]) == 16

        # Reconstrói
        kg2 = KnowledgeGraph.from_dict(data)
        assert kg2.node_count == 11
        assert kg2.edge_count == 16
        assert kg2.get_node("urn:apos:task:oauth-123") is not None
        assert kg2.get_node("urn:apos:feature:faster-auth") is not None
        assert kg2.get_node("urn:apos:release:v2-1") is not None

    def test_to_dict_empty_graph(self):
        kg = KnowledgeGraph()
        data = kg.to_dict()
        assert data == {"nodes": [], "edges": []}

    def test_from_dict_empty(self):
        kg = KnowledgeGraph.from_dict({"nodes": [], "edges": []})
        assert kg.node_count == 0
        assert kg.edge_count == 0

    def test_json_roundtrip(self):
        """Garante que to_dict produz JSON serializável e que from_dict o lê de volta."""
        kg1 = full_graph()
        data = kg1.to_dict()
        json_str = json.dumps(data, sort_keys=True)
        data2 = json.loads(json_str)
        kg2 = KnowledgeGraph.from_dict(data2)
        assert kg2.node_count == kg1.node_count
        assert kg2.edge_count == kg1.edge_count

    def test_from_dict_preserves_attributes(self):
        kg = KnowledgeGraph.from_dict({
            "nodes": [
                {
                    "id": "urn:apos:task:test",
                    "type": "task",
                    "attributes": {"title": "Test", "story_points": 5},
                    "metadata": {
                        "created_at": "2026-01-01", "updated_at": "2026-01-02",
                    },
                }
            ],
            "edges": [],
        })
        n = kg.get_node("urn:apos:task:test")
        assert n is not None
        assert n.attributes["title"] == "Test"
        assert n.attributes["story_points"] == 5


# ═══════════════════════════════════════════════
# Testes: Properties
# ═══════════════════════════════════════════════

class TestProperties:
    def test_node_count(self):
        kg = KnowledgeGraph()
        assert kg.node_count == 0
        kg.add_node(make_task())
        assert kg.node_count == 1

    def test_edge_count(self):
        kg = KnowledgeGraph()
        assert kg.edge_count == 0
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        kg.add_edge(Edge(
            source=t.id, target=f.id, type=EdgeType.CONTRIBUI_PARA,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        ))
        assert kg.edge_count == 1


# ═══════════════════════════════════════════════
# Testes: Validações Adicionais (KG rules)
# ═══════════════════════════════════════════════

class TestKGRules:
    def test_kg001_duplicate_urn(self):
        """KG-001: URN duplicada é rejeitada."""
        kg = KnowledgeGraph()
        kg.add_node(make_task("same-id"))
        with pytest.raises(ValueError, match="KG-001"):
            kg.add_node(make_task("same-id"))

    def test_kg002_invalid_edge_type(self):
        """KG-002: OKR → Feature é inválido (medido_por só vai para Metric)."""
        kg = KnowledgeGraph()
        o = make_okr()
        f = make_feature()
        kg.add_node(o)
        kg.add_node(f)
        e = Edge(
            source=o.id, target=f.id,
            type=EdgeType.MEDIDO_POR,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-002"):
            kg.add_edge(e)

    def test_kg006_missing_source(self):
        kg = KnowledgeGraph()
        f = make_feature()
        kg.add_node(f)
        e = Edge(
            source="urn:apos:task:ghost",
            target=f.id,
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-006"):
            kg.add_edge(e)

    def test_kg007_missing_target(self):
        kg = KnowledgeGraph()
        t = make_task()
        kg.add_node(t)
        e = Edge(
            source=t.id,
            target="urn:apos:feature:ghost",
            type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        )
        with pytest.raises(ValueError, match="KG-007"):
            kg.add_edge(e)

    def test_kg008_cardinality_task_feature(self):
        """KG-008: Task não pode contribuir para 2 features."""
        kg = KnowledgeGraph()
        t = make_task()
        f1 = make_feature("f1")
        f2 = make_feature("f2")
        kg.add_node(t)
        kg.add_node(f1)
        kg.add_node(f2)
        kg.add_edge(Edge(
            source=t.id, target=f1.id, type=EdgeType.CONTRIBUI_PARA,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        ))
        with pytest.raises(ValueError, match="KG-008"):
            kg.add_edge(Edge(
                source=t.id, target=f2.id, type=EdgeType.CONTRIBUI_PARA,
                weight=0.5,
                metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
            ))

    def test_kg009_cardinality_feature_release(self):
        """KG-009: Feature não pode pertencer a 2 releases."""
        kg = KnowledgeGraph()
        f = make_feature()
        r1 = make_release("r1")
        r2 = make_release("r2")
        kg.add_node(f)
        kg.add_node(r1)
        kg.add_node(r2)
        kg.add_edge(Edge(
            source=f.id, target=r1.id, type=EdgeType.PARTE_DE,
            weight=1.0,
            metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
        ))
        with pytest.raises(ValueError, match="KG-009"):
            kg.add_edge(Edge(
                source=f.id, target=r2.id, type=EdgeType.PARTE_DE,
                weight=0.5,
                metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
            ))

    def test_kg012_weight_out_of_range(self):
        """KG-012: weight < 0 ou > 1 é rejeitado."""
        kg = KnowledgeGraph()
        t = make_task()
        f = make_feature()
        kg.add_node(t)
        kg.add_node(f)
        with pytest.raises(ValueError, match="KG-012"):
            kg.add_edge(Edge(
                source=t.id, target=f.id, type=EdgeType.CONTRIBUI_PARA,
                weight=-0.01,
                metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
            ))
        with pytest.raises(ValueError, match="KG-012"):
            kg.add_edge(Edge(
                source=t.id, target=f.id, type=EdgeType.CONTRIBUI_PARA,
                weight=1.01,
                metadata=EdgeMetadata(created_at=now_iso(), updated_at=now_iso()),
            ))

    def test_valid_edge_types_all_combinations(self):
        """Testa que todos os EdgeTypes válidos passam na validação."""
        kg = KnowledgeGraph()

        # Popula nós de todos os tipos
        t = make_task()
        f = make_feature()
        r = make_release()
        o = make_okr()
        m = make_metric()
        s = make_sprint()
        p = make_persona()
        for n in [t, f, r, o, m, s, p]:
            kg.add_node(n)

        ts = now_iso()
        valid_edges = [
            # Task → Feature
            Edge(source=t.id, target=f.id, type=EdgeType.CONTRIBUI_PARA, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Task → Metric
            Edge(source=t.id, target=m.id, type=EdgeType.IMPACTA, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Task → Task
            Edge(source=t.id, target=make_task("t2").id, type=EdgeType.BLOQUEIA, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            Edge(source=t.id, target=make_task("t3").id, type=EdgeType.DEPENDE_DE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Task → Sprint
            Edge(source=t.id, target=s.id, type=EdgeType.PERTENCE_A, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Feature → Release
            Edge(source=f.id, target=r.id, type=EdgeType.PARTE_DE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Feature → Persona
            Edge(source=f.id, target=p.id, type=EdgeType.ENVOLVE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Release → OKR
            Edge(source=r.id, target=o.id, type=EdgeType.ALCANCA, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Release → Persona
            Edge(source=r.id, target=p.id, type=EdgeType.ENVOLVE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # OKR → Metric
            Edge(source=o.id, target=m.id, type=EdgeType.MEDIDO_POR, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Metric → Metric
            Edge(source=m.id, target=m.id, type=EdgeType.ATINGE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
            # Sprint → Release
            Edge(source=s.id, target=r.id, type=EdgeType.PARTE_DE, weight=1.0,
                 metadata=EdgeMetadata(created_at=ts, updated_at=ts)),
        ]

        kg2 = KnowledgeGraph()
        # Re-adiciona nós + t2, t3 para as edges Task→Task
        t2 = make_task("t2")
        t3 = make_task("t3")
        for n in [t, t2, t3, f, r, o, m, s, p]:
            kg2.add_node(n)

        for edge in valid_edges:
            kg2.add_edge(edge)

        assert kg2.edge_count == len(valid_edges)


# ═══════════════════════════════════════════════
# Testes: Integração — Query Patterns (Q01–Q04)
# ═══════════════════════════════════════════════

class TestQueryPatterns:
    """Implementa os padrões de query Q01-Q04 do QUERY_PATTERNS.md."""

    def test_q01_task_to_okr(self):
        """Q01: Task → OKR via contribui_para → parte_de → alcanca."""
        kg = full_graph()
        results = kg.traverse(
            "urn:apos:task:oauth-123",
            [EdgeType.CONTRIBUI_PARA, EdgeType.PARTE_DE, EdgeType.ALCANCA],
        )
        okr_urns = {r[0] for r in results}
        assert "urn:apos:okr:churn-5pct" in okr_urns
        assert "urn:apos:okr:perf-10pct" in okr_urns

    def test_q02_feature_to_metrics(self):
        """Q02: Feature → Métricas via parte_de → alcanca → medido_por."""
        kg = full_graph()
        # Step 1: Feature → Release
        r_results = kg.traverse(
            "urn:apos:feature:faster-auth",
            [EdgeType.PARTE_DE],
        )
        assert len(r_results) == 1
        release_urn = r_results[0][0]

        # Step 2: Release → OKRs
        okr_results = kg.traverse(release_urn, [EdgeType.ALCANCA])
        okr_urns = [r[0] for r in okr_results]

        # Step 3: OKRs → Metrics
        metric_urns = set()
        for okr_urn in okr_urns:
            m_results = kg.traverse(okr_urn, [EdgeType.MEDIDO_POR])
            for m in m_results:
                metric_urns.add(m[0])

        assert "urn:apos:metric:login-time" in metric_urns
        assert "urn:apos:metric:error-rate" in metric_urns

    def test_q03_release_dashboard(self):
        """Q03: Release → OKRs → Metrics + Features."""
        kg = full_graph()
        release_urn = "urn:apos:release:v2-1"

        # Forward: Release → OKRs
        okrs = kg.traverse(release_urn, [EdgeType.ALCANCA])

        # Reverse: Features ← parte_de
        features = []
        for edge in kg._get_inbound(release_urn, EdgeType.PARTE_DE):
            features.append(edge.source)

        assert len(okrs) == 2
        assert len(features) == 1
        assert "urn:apos:feature:faster-auth" in features

    def test_q04_task_to_sprint(self):
        """Q04: Task → Sprint via pertence_a."""
        kg = full_graph()
        results = kg.traverse(
            "urn:apos:task:oauth-123",
            [EdgeType.PERTENCE_A],
        )
        assert len(results) == 1
        assert results[0][0] == "urn:apos:sprint:s0-4"
