"""Testes unitários para apos/capabilities/model.py — 21 cenários (M1–M21)."""

from __future__ import annotations

import pytest

from apos.capabilities.model import (
    Capability,
    CapabilityDomain,
    CapabilityMetadata,
    CapabilityRegistry,
    CapabilityStatus,
    CheckType,
    Effect,
    EffectType,
    KGPattern,
    PreCondition,
    can_transition,
    transition,
)


# ══════════════════════════════════════════════
# Fixtures Compartilhadas
# ══════════════════════════════════════════════


@pytest.fixture
def mini_cap() -> Capability:
    """Capability mínima — apenas id e name."""
    return Capability(
        id="urn:apos:cap:core:test.minimal",
        name="test.minimal",
        description="Minimal capability for testing",
    )


@pytest.fixture
def full_cap() -> Capability:
    """Capability completa com todos os campos preenchidos."""
    return Capability(
        id="urn:apos:cap:governance:full.test",
        name="full.test",
        description="Full capability with all fields",
        domain=CapabilityDomain.GOVERNANCE,
        version="2.1.0",
        input_schema={"type": "object", "properties": {"x": {"type": "string"}}},
        output_schema={"type": "object", "properties": {"y": {"type": "integer"}}},
        pre_conditions=[
            PreCondition(
                description="Node must exist",
                check_type=CheckType.NODE_EXISTS,
                params={"urn": "{target_urn}"},
            ),
        ],
        effects=[
            Effect(
                description="Creates edge in KG",
                effect_type=EffectType.EDGE_CREATED,
                target="urn:apos:kg:edge:*",
                delta={"weight": 1.0},
            ),
        ],
        enabled_agents=["urn:apos:agent:hermes", "urn:apos:agent:orchestrator"],
        kg_read=[
            KGPattern(
                nodes=["Concept", "Relation"],
                edges=["related_to"],
                queries=["Q01"],
                description="Read concept relations",
            ),
        ],
        kg_write=[
            KGPattern(
                nodes=["Event"],
                edges=["triggered_by"],
                queries=["Q05"],
                description="Write events",
            ),
        ],
        metadata=CapabilityMetadata(
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-02T00:00:00Z",
            version="2.1.0",
            status=CapabilityStatus.REGISTERED,
            tags=["test", "full", "governance"],
            author="tester",
            ttl_hours=48,
        ),
    )


@pytest.fixture
def registry() -> CapabilityRegistry:
    """Registry vazio, pronto para testes."""
    return CapabilityRegistry()


# ══════════════════════════════════════════════
# M1 — Capability mínima
# ══════════════════════════════════════════════


class TestCapabilityModel:
    """21 cenários de teste para o modelo de capabilities (M1–M21)."""

    # ────────────────
    # Criação
    # ────────────────

    def test_create_minimal(self):
        """M1: Capability com id e nome apenas."""
        cap = Capability(
            id="urn:apos:cap:core:minimal",
            name="core.minimal",
            description="Apenas o essencial",
        )
        assert cap.id == "urn:apos:cap:core:minimal"
        assert cap.name == "core.minimal"
        assert cap.domain == CapabilityDomain.CORE  # default
        assert cap.version == "1.0.0"  # default
        assert cap.pre_conditions == []
        assert cap.effects == []
        assert cap.enabled_agents == []
        assert cap.kg_read == []
        assert cap.kg_write == []
        assert isinstance(cap.metadata, CapabilityMetadata)

    def test_create_full(self, full_cap):
        """M2: Capability com todos os campos preenchidos."""
        cap = full_cap
        assert cap.id == "urn:apos:cap:governance:full.test"
        assert cap.name == "full.test"
        assert cap.domain == CapabilityDomain.GOVERNANCE
        assert cap.version == "2.1.0"
        assert cap.input_schema == {"type": "object", "properties": {"x": {"type": "string"}}}
        assert len(cap.pre_conditions) == 1
        assert len(cap.effects) == 1
        assert len(cap.enabled_agents) == 2
        assert len(cap.kg_read) == 1
        assert len(cap.kg_write) == 1
        assert cap.metadata.tags == ["test", "full", "governance"]
        assert cap.metadata.ttl_hours == 48

    # ────────────────
    # Status inicial
    # ────────────────

    def test_status_initial(self, mini_cap):
        """M3: Capability recém-criada tem status REGISTERED."""
        assert mini_cap.status == CapabilityStatus.REGISTERED
        assert mini_cap.metadata.status == CapabilityStatus.REGISTERED

    # ────────────────
    # Transições de estado
    # ────────────────

    def test_transition_valid(self):
        """M4: Cadeia registered→ready→running→completed."""
        assert can_transition(CapabilityStatus.REGISTERED, CapabilityStatus.READY)
        assert transition(CapabilityStatus.REGISTERED, CapabilityStatus.READY) == CapabilityStatus.READY

        assert can_transition(CapabilityStatus.READY, CapabilityStatus.RUNNING)
        assert transition(CapabilityStatus.READY, CapabilityStatus.RUNNING) == CapabilityStatus.RUNNING

        assert can_transition(CapabilityStatus.RUNNING, CapabilityStatus.COMPLETED)
        assert transition(CapabilityStatus.RUNNING, CapabilityStatus.COMPLETED) == CapabilityStatus.COMPLETED

    def test_transition_invalid(self):
        """M5: completed→running levanta ValueError."""
        assert not can_transition(CapabilityStatus.COMPLETED, CapabilityStatus.RUNNING)
        with pytest.raises(ValueError, match="Transição inválida"):
            transition(CapabilityStatus.COMPLETED, CapabilityStatus.RUNNING)

    # ────────────────
    # Registro (CapabilityRegistry)
    # ────────────────

    def test_register_duplicate(self, registry, mini_cap):
        """M6: Registrar mesma ID duas vezes → False na segunda."""
        assert registry.register(mini_cap) is True
        assert registry.register(mini_cap) is False

    def test_unregister_exists(self, registry, mini_cap):
        """M7: Unregister de capability existente → True."""
        registry.register(mini_cap)
        assert registry.unregister(mini_cap.id) is True

    def test_unregister_not_found(self, registry):
        """M8: Unregister de ID inexistente → False."""
        assert registry.unregister("urn:apos:cap:nonexistent") is False

    # ────────────────
    # Consulta
    # ────────────────

    def test_get_found(self, registry, mini_cap):
        """M9: get por ID existente → Capability."""
        registry.register(mini_cap)
        result = registry.get(mini_cap.id)
        assert result is not None
        assert result.id == mini_cap.id
        assert result.name == mini_cap.name

    def test_get_not_found(self, registry):
        """M10: get por ID inexistente → None."""
        assert registry.get("urn:apos:cap:nobody") is None

    # ────────────────
    # Descoberta
    # ────────────────

    def test_discover_query(self, registry):
        """M11: discover(\"consulta\") filtra por texto no nome/descrição."""
        a = Capability(id="urn:apos:cap:core:alpha", name="alpha", description="Alpha desc")
        b = Capability(id="urn:apos:cap:core:beta", name="beta", description="Beta desc")
        registry.register(a)
        registry.register(b)

        found = registry.discover(query="alpha")
        assert len(found) == 1
        assert found[0].name == "alpha"

    def test_discover_domain_filter(self, registry):
        """M12: discover com filter por domínio."""
        core_cap = Capability(
            id="urn:apos:cap:core:c1", name="core.c1", description="Core cap",
            domain=CapabilityDomain.CORE,
        )
        gov_cap = Capability(
            id="urn:apos:cap:governance:g1", name="gov.g1", description="Gov cap",
            domain=CapabilityDomain.GOVERNANCE,
        )
        registry.register(core_cap)
        registry.register(gov_cap)

        found = registry.discover(domain="core")
        assert len(found) == 1
        assert found[0].domain == CapabilityDomain.CORE

    def test_discover_all(self, registry, mini_cap, full_cap):
        """M13: discover(\"\") retorna todas as capabilities registradas."""
        registry.register(mini_cap)
        registry.register(full_cap)
        assert len(registry.discover()) == 2
        assert len(registry.discover(query="")) == 2

    # ────────────────
    # find
    # ────────────────

    def test_find_by_status(self, registry, mini_cap):
        """M14: find(status=\"ready\") retorna capabilities ready."""
        cap_ready = Capability(
            id="urn:apos:cap:core:ready1", name="ready.one", description="Ready cap",
            metadata=CapabilityMetadata(status=CapabilityStatus.READY),
        )
        registry.register(mini_cap)  # registered
        registry.register(cap_ready)
        found = registry.find(status="ready")
        assert len(found) == 1
        assert found[0].id == cap_ready.id

    def test_find_status_empty(self, registry):
        """M15: find(status=\"invalid\") → lista vazia."""
        found = registry.find(status="invalid")
        assert found == []

    # ────────────────
    # Listagem por domínio / agente
    # ────────────────

    def test_list_by_domain(self, registry):
        """M16: list_by_domain(\"core\") retorna capabilities do domínio core."""
        c1 = Capability(
            id="urn:apos:cap:core:c1", name="core.c1", description="C1",
            domain=CapabilityDomain.CORE,
        )
        c2 = Capability(
            id="urn:apos:cap:core:c2", name="core.c2", description="C2",
            domain=CapabilityDomain.CORE,
        )
        s1 = Capability(
            id="urn:apos:cap:support:s1", name="s1", description="S1",
            domain=CapabilityDomain.SUPPORT,
        )
        registry.register(c1)
        registry.register(c2)
        registry.register(s1)

        core_list = registry.list_by_domain("core")
        assert len(core_list) == 2
        assert CapabilityDomain.CORE in (c.domain for c in core_list)

    def test_list_by_agent(self, registry):
        """M17: list_by_agent(\"urn:apos:agent:x\") retorna caps do agente."""
        cap_a = Capability(
            id="urn:apos:cap:core:a", name="agent.a", description="A",
            enabled_agents=["urn:apos:agent:hermes"],
        )
        cap_b = Capability(
            id="urn:apos:cap:core:b", name="agent.b", description="B",
            enabled_agents=["urn:apos:agent:orchestrator"],
        )
        registry.register(cap_a)
        registry.register(cap_b)

        hermes_caps = registry.list_by_agent("urn:apos:agent:hermes")
        assert len(hermes_caps) == 1
        assert hermes_caps[0].id == cap_a.id

    # ────────────────
    # Serialização
    # ────────────────

    def test_to_dict(self, full_cap):
        """M18: Capability.to_dict() → dict com campos esperados."""
        d = full_cap.to_dict()
        assert isinstance(d, dict)
        assert d["id"] == "urn:apos:cap:governance:full.test"
        assert d["name"] == "full.test"
        assert d["domain"] == "governance"
        assert d["version"] == "2.1.0"
        assert len(d["pre_conditions"]) == 1
        assert d["pre_conditions"][0]["check_type"] == "node_exists"
        assert len(d["effects"]) == 1
        assert d["effects"][0]["effect_type"] == "edge_created"
        assert len(d["enabled_agents"]) == 2
        assert len(d["kg_read"]) == 1
        assert len(d["kg_write"]) == 1
        assert d["metadata"]["status"] == "registered"
        assert d["metadata"]["tags"] == ["test", "full", "governance"]

    def test_from_dict(self, full_cap):
        """M19: Capability.from_dict(data) → Capability igual à original."""
        data = full_cap.to_dict()
        restored = Capability.from_dict(data)
        assert isinstance(restored, Capability)
        assert restored.id == full_cap.id
        assert restored.name == full_cap.name
        assert restored.domain == full_cap.domain
        assert restored.version == full_cap.version
        assert len(restored.pre_conditions) == 1
        assert restored.pre_conditions[0].check_type == CheckType.NODE_EXISTS
        assert len(restored.effects) == 1
        assert restored.effects[0].effect_type == EffectType.EDGE_CREATED
        assert restored.enabled_agents == full_cap.enabled_agents
        assert restored.metadata.tags == full_cap.metadata.tags

        # Round-trip: serializar o restaurado deve ser igual ao original
        assert restored.to_dict() == data

    # ────────────────
    # Pré-condições
    # ────────────────

    def test_precondition_eval(self):
        """M20: PreCondition pode ser criada e acessada."""
        pc = PreCondition(
            description="Knowledge Graph must not be empty",
            check_type=CheckType.KG_NOT_EMPTY,
            params={"mode": "strict"},
        )
        assert pc.description == "Knowledge Graph must not be empty"
        assert pc.check_type == CheckType.KG_NOT_EMPTY
        assert pc.params == {"mode": "strict"}
        # Serialização compatível
        assert pc.check_type.value == "kg_not_empty"

    # ────────────────
    # Efeitos
    # ────────────────

    def test_effect_apply(self):
        """M21: Effect pode ser criado sem erro e seus campos são acessíveis."""
        effect = Effect(
            description="Node created in KG",
            effect_type=EffectType.NODE_CREATED,
            target="urn:apos:kg:node:concept:*",
            delta={"label": "Concept", "source": "extractor"},
        )
        assert effect.description == "Node created in KG"
        assert effect.effect_type == EffectType.NODE_CREATED
        assert effect.target == "urn:apos:kg:node:concept:*"
        assert effect.delta == {"label": "Concept", "source": "extractor"}
        # Serialização compatível
        assert effect.effect_type.value == "node_created"
