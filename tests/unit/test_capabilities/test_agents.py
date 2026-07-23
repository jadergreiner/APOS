"""Testes unitarios para apos/capabilities/agents.py (A1-A11)."""

import pytest

from apos.capabilities.agents import (
    AGENT_CATALOG,
    AGENT_CONTEXT,
    AGENT_GOVERNANCE,
    AGENT_HERMES,
    AGENT_KG,
    AGENT_ROUTER,
    AGENT_TRUST_SCORE,
    AGENTS_POR_NOME,
    AGENTS_POR_URN,
    AgentCategoria,
    AgentDescriptor,
    AgentDominio,
    AgentMaturidade,
    get_agent,
    get_agents_by_capability,
    get_fallback_agents,
    get_primary_agent,
    make_agent_urn,
)


class TestCapabilityAgents:
    """11 cenarios para o modulo agents.py."""

    # ------------------------------------------------------------------
    # A1 — AgentDescriptor com todos os campos
    # ------------------------------------------------------------------
    def test_agent_descriptor_full(self):
        """A1: AgentDescriptor com todos os campos."""
        desc = AgentDescriptor(
            urn="urn:apos:agent:test-agent",
            nome="Test Agent",
            descricao="Um agente de teste.",
            dominio=AgentDominio.AGENTES,
            categoria=AgentCategoria.CORE,
            maturidade=AgentMaturidade.L2_IMPLEMENTADO,
            habilidades=["codigo", "testes"],
            capabilities=["graph.traverse", "context.assemble"],
            limitacoes=["sem acesso a producao"],
        )
        assert desc.urn == "urn:apos:agent:test-agent"
        assert desc.nome == "Test Agent"
        assert desc.descricao == "Um agente de teste."
        assert desc.dominio == AgentDominio.AGENTES
        assert desc.categoria == AgentCategoria.CORE
        assert desc.maturidade == AgentMaturidade.L2_IMPLEMENTADO
        assert isinstance(desc.habilidades, list)
        assert len(desc.habilidades) == 2
        assert isinstance(desc.capabilities, list)
        assert len(desc.capabilities) == 2
        assert isinstance(desc.limitacoes, list)
        assert len(desc.limitacoes) == 1

    def test_agent_descriptor_defaults(self):
        """A1b: AgentDescriptor com valores padrao."""
        desc = AgentDescriptor(
            urn="urn:apos:agent:minimo",
            nome="Minimo",
            descricao="Apenas campos obrigatorios.",
        )
        assert desc.dominio == AgentDominio.AGENTES
        assert desc.categoria == AgentCategoria.CORE
        assert desc.maturidade == AgentMaturidade.L0_CONCEITUAL
        assert desc.habilidades == []
        assert desc.capabilities == []
        assert desc.limitacoes == []

    # ------------------------------------------------------------------
    # A2 — to_dict
    # ------------------------------------------------------------------
    def test_agent_descriptor_to_dict(self):
        """A2: to_dict() retorna dict com chaves esperadas."""
        desc = AgentDescriptor(
            urn="urn:apos:agent:to-dict",
            nome="To Dict",
            descricao="Testando to_dict.",
            dominio=AgentDominio.GRAFO,
            categoria=AgentCategoria.SUPPORT,
            maturidade=AgentMaturidade.L1_ESTRUTURADO,
            habilidades=["skill-a"],
            capabilities=["cap-a"],
            limitacoes=["lim-a"],
        )
        d = desc.to_dict()
        expected_keys = {
            "urn", "nome", "descricao", "dominio", "categoria",
            "maturidade", "habilidades", "capabilities", "limitacoes",
        }
        assert set(d.keys()) == expected_keys
        assert d["urn"] == "urn:apos:agent:to-dict"
        assert d["nome"] == "To Dict"
        assert d["dominio"] == AgentDominio.GRAFO.value
        assert d["categoria"] == AgentCategoria.SUPPORT.value
        assert d["maturidade"] == AgentMaturidade.L1_ESTRUTURADO.value
        assert isinstance(d["habilidades"], list)
        assert isinstance(d["capabilities"], list)
        assert isinstance(d["limitacoes"], list)

    # ------------------------------------------------------------------
    # A3 — make_agent_urn
    # ------------------------------------------------------------------
    def test_make_agent_urn(self):
        """A3: make_agent_urn('test') -> 'urn:apos:agent:test'."""
        assert make_agent_urn("test") == "urn:apos:agent:test"
        assert make_agent_urn("knowledge-graph") == "urn:apos:agent:knowledge-graph"
        assert make_agent_urn("hermes") == "urn:apos:agent:hermes"

    # ------------------------------------------------------------------
    # A4 — get_agent found
    # ------------------------------------------------------------------
    def test_get_agent_found(self):
        """A4: get_agent('Hermes Agent') -> AgentDescriptor."""
        # Por nome
        agent = get_agent("Hermes Agent")
        assert agent is not None
        assert isinstance(agent, AgentDescriptor)
        assert agent.urn == "urn:apos:agent:hermes"
        assert agent.nome == "Hermes Agent"

        # Por URN
        agent2 = get_agent("urn:apos:agent:hermes")
        assert agent2 is not None
        assert agent2.nome == "Hermes Agent"

        # Knowledge Graph Agent
        kg = get_agent("Knowledge Graph Agent")
        assert kg is not None
        assert kg.urn == "urn:apos:agent:knowledge-graph"

    # ------------------------------------------------------------------
    # A5 — get_agent not found
    # ------------------------------------------------------------------
    def test_get_agent_not_found(self):
        """A5: get_agent('inexistente') -> None."""
        assert get_agent("Agente Inexistente") is None
        assert get_agent("urn:apos:agent:fake") is None
        assert get_agent("") is None

    # ------------------------------------------------------------------
    # A6 — get_agents_by_capability
    # ------------------------------------------------------------------
    def test_get_agents_by_capability(self):
        """A6: filtra agentes por capability_id."""
        # graph.traverse: hermes, kg, context-agent
        agents = get_agents_by_capability("graph.traverse")
        assert isinstance(agents, list)
        urns = {a.urn for a in agents}
        assert "urn:apos:agent:hermes" in urns
        assert "urn:apos:agent:knowledge-graph" in urns
        assert "urn:apos:agent:context-agent" in urns

        # trust-score.calculate: apenas trust-score
        ts = get_agents_by_capability("trust-score.calculate")
        assert len(ts) == 1
        assert ts[0].urn == "urn:apos:agent:trust-score"

    # ------------------------------------------------------------------
    # A7 — get_agents_by_capability empty
    # ------------------------------------------------------------------
    def test_get_agents_by_capability_empty(self):
        """A7: capability sem agentes -> lista vazia."""
        # metrics.refresh tem todos False
        agents = get_agents_by_capability("metrics.refresh")
        assert agents == []

        # Capability inexistente
        agents2 = get_agents_by_capability("nonexistent.capability")
        assert agents2 == []

    # ------------------------------------------------------------------
    # A8 — get_primary_agent
    # ------------------------------------------------------------------
    def test_get_primary_agent(self):
        """A8: retorna o agente primario de uma capability."""
        cap_map = {
            "graph.traverse": "urn:apos:agent:knowledge-graph",
            "context.assemble": "urn:apos:agent:context-agent",
            "trust-score.calculate": "urn:apos:agent:trust-score",
            "coverage.report": "urn:apos:agent:governance",
        }
        for cap_name, expected_urn in cap_map.items():
            primary = get_primary_agent(cap_name)
            assert primary == expected_urn, f"{cap_name} -> {primary} != {expected_urn}"

    def test_get_primary_agent_not_found(self):
        """A8b: capability sem regra -> None."""
        assert get_primary_agent("nonexistent.cap") is None

    # ------------------------------------------------------------------
    # A9 — get_fallback_agents
    # ------------------------------------------------------------------
    def test_get_fallback_agents(self):
        """A9: retorna fallbacks se primary falha."""
        fallbacks = get_fallback_agents("graph.traverse")
        assert isinstance(fallbacks, list)
        assert "urn:apos:agent:hermes" in fallbacks

        # impact.analyze tem dois fallbacks
        impact = get_fallback_agents("impact.analyze")
        assert len(impact) == 2
        assert "urn:apos:agent:hermes" in impact
        assert "urn:apos:agent:governance" in impact

    def test_get_fallback_agents_not_found(self):
        """A9b: capability sem regra -> lista vazia."""
        assert get_fallback_agents("nonexistent.cap") == []

    # ------------------------------------------------------------------
    # A10 — AgentDominio enum
    # ------------------------------------------------------------------
    def test_agent_dominio_enum(self):
        """A10: AgentDominio tem AGENTES, GRAFO, CONTEXTO, GOVERNANCA."""
        assert AgentDominio.AGENTES.value == "Agentes"
        assert AgentDominio.GRAFO.value == "Grafo"
        assert AgentDominio.CONTEXTO.value == "Contexto"
        assert AgentDominio.GOVERNANCA.value == "Governança"
        assert len(AgentDominio) == 4

    # ------------------------------------------------------------------
    # A11 — AgentCategoria enum
    # ------------------------------------------------------------------
    def test_agent_categoria_enum(self):
        """A11: AgentCategoria tem CORE, SUPPORT, GOVERNANCE."""
        assert AgentCategoria.CORE.value == "core"
        assert AgentCategoria.SUPPORT.value == "support"
        assert AgentCategoria.GOVERNANCE.value == "governance"
        assert len(AgentCategoria) == 3


# --- Testes adicionais para cobertura do catalogo ---
class TestAgentCatalog:
    """Testes extras para o catalogo de agentes."""

    def test_catalog_has_six_agents(self):
        """Catalogo possui 6 agentes definidos."""
        assert len(AGENT_CATALOG) == 6

    def test_catalog_contains_all_agents(self):
        """Todos os agentes esperados estao no catalogo."""
        urns = {a.urn for a in AGENT_CATALOG}
        expected = {
            "urn:apos:agent:hermes",
            "urn:apos:agent:knowledge-graph",
            "urn:apos:agent:context-agent",
            "urn:apos:agent:trust-score",
            "urn:apos:agent:governance",
            "urn:apos:agent:capability-router",
        }
        assert urns == expected

    def test_indices_consistent(self):
        """Indices AGENTS_POR_URN e AGENTS_POR_NOME sao consistentes."""
        assert len(AGENTS_POR_URN) == 6
        assert len(AGENTS_POR_NOME) == 6
        for agent in AGENT_CATALOG:
            assert AGENTS_POR_URN[agent.urn] is agent
            assert AGENTS_POR_NOME[agent.nome] is agent

    def test_agent_maturidade_values(self):
        """AgentMaturidade tem os 4 niveis esperados."""
        assert len(AgentMaturidade) == 4
        assert AgentMaturidade.L0_CONCEITUAL.value == "L0_conceitual"
        assert AgentMaturidade.L1_ESTRUTURADO.value == "L1_estruturado"
        assert AgentMaturidade.L2_IMPLEMENTADO.value == "L2_implementado"
        assert AgentMaturidade.L3_OTIMIZADO.value == "L3_otimizado"
