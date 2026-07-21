"""APOS Capabilities Module — Capacidades, taxonomia, agentes e roteamento."""

from apos.capabilities.model import (
    Capability,
    CapabilityDomain,
    CapabilityStatus,
    CapabilityRegistry,
    PreCondition,
    Effect,
)
from apos.capabilities.taxonomy import (
    Dominio,
    Capacidade,
    Habilidade,
    Acao,
    Categoria,
    Maturidade,
    CriterioClassificacao,
)
from apos.capabilities.agents import (
    AgentDescriptor,
    AgentDominio,
    AgentCategoria,
    get_agent,
    get_agents_by_capability,
    get_primary_agent,
    get_fallback_agents,
)
from apos.capabilities.router import (
    CapabilityRouter,
    CapabilityRequest,
    ResolutionResult,
    MatchStrategy,
    create_default_router,
)

__all__ = [
    "Capability", "CapabilityDomain", "CapabilityStatus", "CapabilityRegistry",
    "PreCondition", "Effect",
    "Dominio", "Capacidade", "Habilidade", "Acao",
    "Categoria", "Maturidade", "CriterioClassificacao",
    "AgentDescriptor", "AgentDominio", "AgentCategoria",
    "get_agent", "get_agents_by_capability", "get_primary_agent", "get_fallback_agents",
    "CapabilityRouter", "CapabilityRequest", "ResolutionResult", "MatchStrategy",
    "create_default_router",
]
