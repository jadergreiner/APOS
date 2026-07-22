"""
APOS Agent Map — Mapa de Agentes e Capabilities (Camada 3.6)

Define o catálogo oficial dos agentes do ecossistema APOS, incluindo:
- 6 agentes com URN, propósito e capabilities
- Matriz agente × capability (completa Sprint 0.6)
- Regras de roteamento por domínio e contexto

Conforme AGENT_MAP.md — Sprint 0.6, Tarefa T0.6.3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ──────────────────────────────────────────────
# AgentURN — Helpers
# ──────────────────────────────────────────────

AGENT_URN_PREFIX = "urn:apos:agent:"


def make_agent_urn(agent_name: str) -> str:
    """Cria uma URN de agente no padrão APOS.

    Args:
        agent_name: Nome do agente em kebab-case.

    Returns:
        URN no formato ``urn:apos:agent:{agent_name}``.
    """
    return f"{AGENT_URN_PREFIX}{agent_name}"


# ──────────────────────────────────────────────
# Enums e Dataclasses
# ──────────────────────────────────────────────


class AgentMaturidade(str, Enum):
    """Nível de maturidade de um agente."""

    L0_CONCEITUAL = "L0_conceitual"
    L1_ESTRUTURADO = "L1_estruturado"
    L2_IMPLEMENTADO = "L2_implementado"
    L3_OTIMIZADO = "L3_otimizado"


class AgentDominio(str, Enum):
    """Domínio primário do agente."""

    AGENTES = "Agentes"
    GRAFO = "Grafo"
    CONTEXTO = "Contexto"
    GOVERNANCA = "Governança"


class AgentCategoria(str, Enum):
    """Categoria do agente."""

    CORE = "core"
    SUPPORT = "support"
    GOVERNANCE = "governance"


@dataclass
class AgentDescriptor:
    """Descrição formal de um agente do ecossistema APOS.

    Attributes:
        urn: URN única no formato ``urn:apos:agent:{name}``.
        nome: Nome legível do agente.
        descricao: Propósito e responsabilidades.
        dominio: Domínio primário de atuação.
        categoria: Categoria (core, support, governance).
        maturidade: Nível de maturidade R0.
        habilidades: Lista de habilidades do agente.
        capabilities: Lista de nomes de capabilities que implementa.
        limitacoes: Lista de limitações conhecidas.
    """

    urn: str
    nome: str
    descricao: str
    dominio: AgentDominio = AgentDominio.AGENTES
    categoria: AgentCategoria = AgentCategoria.CORE
    maturidade: AgentMaturidade = AgentMaturidade.L0_CONCEITUAL
    habilidades: list[str] = field(default_factory=list)
    capabilities: list[str] = field(default_factory=list)
    limitacoes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "urn": self.urn,
            "nome": self.nome,
            "descricao": self.descricao,
            "dominio": self.dominio.value,
            "categoria": self.categoria.value,
            "maturidade": self.maturidade.value,
            "habilidades": list(self.habilidades),
            "capabilities": list(self.capabilities),
            "limitacoes": list(self.limitacoes),
        }


# ──────────────────────────────────────────────
# Catálogo de Agentes (6 agentes — Sprint 0.6)
# ──────────────────────────────────────────────

AGENT_HERMES = AgentDescriptor(
    urn="urn:apos:agent:hermes",
    nome="Hermes Agent",
    descricao=(
        "Agente principal de desenvolvimento e execução de tarefas. "
        "Interface primária entre o usuário e o ecossistema APOS. "
        "Orquestra solicitações, delega para outros agentes e executa "
        "tarefas de desenvolvimento diretamente."
    ),
    dominio=AgentDominio.AGENTES,
    categoria=AgentCategoria.CORE,
    maturidade=AgentMaturidade.L2_IMPLEMENTADO,
    habilidades=[
        "Desenvolvimento de código",
        "Execução de tarefas",
        "Orquestração de workflows",
        "Delegação para subagentes",
    ],
    capabilities=[
        "graph.traverse",
        "context.assemble",
        "query.execute",
        "task-to-okr",
        "feature-metrics",
        "impact.analyze",
    ],
    limitacoes=[
        "Não possui capabilities de governança dedicadas",
        "Delega trust-score.calculate, integrity.validate e coverage.report para agentes especializados",
    ],
)

AGENT_KG = AgentDescriptor(
    urn="urn:apos:agent:knowledge-graph",
    nome="Knowledge Graph Agent",
    descricao=(
        "Agente especializado em operações sobre o Knowledge Graph. "
        "Executa consultas, travessias, análise de impacto e detecção "
        "de problemas estruturais (órfãos, ciclos) no grafo."
    ),
    dominio=AgentDominio.GRAFO,
    categoria=AgentCategoria.CORE,
    maturidade=AgentMaturidade.L2_IMPLEMENTADO,
    habilidades=[
        "Navegação do grafo",
        "Query Patterns (Q01–Q16)",
        "Gestão de nós e arestas",
        "Detecção de problemas estruturais",
    ],
    capabilities=[
        "graph.traverse",
        "query.execute",
        "task-to-okr",
        "feature-metrics",
        "impact.analyze",
        "orphans.detect",
        "cycles.detect",
    ],
    limitacoes=[
        "Não monta contexto para agentes",
        "Não calcula trust score",
        "Somente leitura no KG (Sprint 0.6)",
    ],
)

AGENT_CONTEXT = AgentDescriptor(
    urn="urn:apos:agent:context-agent",
    nome="Context Agent",
    descricao=(
        "Agente especializado na montagem, gestão e entrega de contexto "
        "semântico para outros agentes. Extrai nós do Knowledge Graph, "
        "monta blocos de contexto, calcula relevância e otimiza o uso "
        "de tokens dentro dos limites de cada agente."
    ),
    dominio=AgentDominio.CONTEXTO,
    categoria=AgentCategoria.CORE,
    maturidade=AgentMaturidade.L1_ESTRUTURADO,
    habilidades=[
        "Extração de contexto do KG",
        "Montagem de blocos",
        "Cálculo de relevância",
        "Compactação e poda",
        "Cache de contexto",
    ],
    capabilities=[
        "context.assemble",
        "graph.traverse",
        "query.execute",
    ],
    limitacoes=[
        "Não executa queries de negócio (task-to-okr, feature-metrics)",
        "Não realiza análise de impacto",
        "Não modifica o KG",
    ],
)

AGENT_TRUST_SCORE = AgentDescriptor(
    urn="urn:apos:agent:trust-score",
    nome="Trust Score Agent",
    descricao=(
        "Agente especializado no cálculo de Trust Score de nós do "
        "Knowledge Graph. Utiliza as queries Q14 (cobertura), Q15 "
        "(qualidade referencial) e Q16 (consistência) para produzir "
        "um score [0.0, 1.0] que reflete a confiabilidade de cada nó."
    ),
    dominio=AgentDominio.GOVERNANCA,
    categoria=AgentCategoria.GOVERNANCE,
    maturidade=AgentMaturidade.L0_CONCEITUAL,
    habilidades=[
        "Cálculo de trust score",
        "Análise de cobertura",
        "Avaliação de qualidade referencial",
        "Verificação de consistência",
    ],
    capabilities=[
        "trust-score.calculate",
        "coverage.report",
        "integrity.validate",
    ],
    limitacoes=[
        "Apenas leitura no KG (Sprint 0.6)",
        "Não modifica atributos de nós",
        "Não executa queries de navegação",
    ],
)

AGENT_GOVERNANCE = AgentDescriptor(
    urn="urn:apos:agent:governance",
    nome="Governance Agent",
    descricao=(
        "Agente de auditoria, validação e governança do ecossistema APOS. "
        "Responsável por relatórios de cobertura, validação de integridade, "
        "detecção de problemas estruturais e garantia de conformidade com "
        "as regras da ontologia. Atua em caráter preventivo e corretivo."
    ),
    dominio=AgentDominio.GOVERNANCA,
    categoria=AgentCategoria.GOVERNANCE,
    maturidade=AgentMaturidade.L0_CONCEITUAL,
    habilidades=[
        "Auditoria de ações",
        "Validação de integridade",
        "Relatórios de cobertura",
        "Detecção de órfãos",
        "Semantic gates",
    ],
    capabilities=[
        "integrity.validate",
        "coverage.report",
        "orphans.detect",
        "cycles.detect",
        "impact.analyze",
    ],
    limitacoes=[
        "Não calcula trust score (delega para Trust Score Agent)",
        "Somente leitura no KG (Sprint 0.6)",
        "Execução assíncrona/batch",
    ],
)

AGENT_ROUTER = AgentDescriptor(
    urn="urn:apos:agent:capability-router",
    nome="Capability Router Agent",
    descricao=(
        "Agente responsável pelo roteamento inteligente de requisições "
        "para a capability e o agente mais adequados. Analisa o contexto "
        "da requisição (domínio, URN alvo, tipo de operação), consulta "
        "o Capability Registry e decide qual agente deve executar a capability."
    ),
    dominio=AgentDominio.AGENTES,
    categoria=AgentCategoria.CORE,
    maturidade=AgentMaturidade.L0_CONCEITUAL,
    habilidades=[
        "Análise de contexto de requisição",
        "Consulta ao Capability Registry",
        "Decisão de roteamento por domínio",
        "Balanceamento de carga entre agentes",
        "Fallback e tolerância a falhas",
    ],
    capabilities=[
        "routing.resolve",
    ],
    limitacoes=[
        "Não executa capabilities de negócio",
        "Atua exclusivamente como orquestrador de roteamento",
        "Depende do Capability Registry para decisões",
    ],
)

# Catálogo completo de agentes
AGENT_CATALOG: list[AgentDescriptor] = [
    AGENT_HERMES,
    AGENT_KG,
    AGENT_CONTEXT,
    AGENT_TRUST_SCORE,
    AGENT_GOVERNANCE,
    AGENT_ROUTER,
]

# Índices
AGENTS_POR_URN: dict[str, AgentDescriptor] = {a.urn: a for a in AGENT_CATALOG}
AGENTS_POR_NOME: dict[str, AgentDescriptor] = {a.nome: a for a in AGENT_CATALOG}


# ──────────────────────────────────────────────
# Matriz Agente × Capability
# ──────────────────────────────────────────────


@dataclass
class AgentCapabilityEntry:
    """Entrada da matriz agente × capability.

    Attributes:
        capability: Nome da capability.
        domain: Domínio funcional.
        agent_urns: Mapa de URN de agente → habilitado (True/False).
    """

    capability: str
    domain: str  # core, support, governance
    agent_urns: dict[str, bool] = field(default_factory=dict)


# Matriz completa (AGENT_MAP.md §3.1)
AGENT_CAPABILITY_MATRIX: list[AgentCapabilityEntry] = [
    AgentCapabilityEntry(
        capability="graph.traverse",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": True,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="context.assemble",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": True,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="query.execute",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": True,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="task-to-okr",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="feature-metrics",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="trust-score.calculate",
        domain="governance",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": True,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="integrity.validate",
        domain="governance",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": True,
            "urn:apos:agent:governance": True,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="coverage.report",
        domain="governance",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": True,
            "urn:apos:agent:governance": True,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="orphans.detect",
        domain="support",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": True,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="cycles.detect",
        domain="support",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": True,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="impact.analyze",
        domain="support",
        agent_urns={
            "urn:apos:agent:hermes": True,
            "urn:apos:agent:knowledge-graph": True,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": True,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="metrics.refresh",
        domain="support",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": False,
        },
    ),
    AgentCapabilityEntry(
        capability="routing.resolve",
        domain="core",
        agent_urns={
            "urn:apos:agent:hermes": False,
            "urn:apos:agent:knowledge-graph": False,
            "urn:apos:agent:context-agent": False,
            "urn:apos:agent:trust-score": False,
            "urn:apos:agent:governance": False,
            "urn:apos:agent:capability-router": True,
        },
    ),
]


# ──────────────────────────────────────────────
# Regras de Roteamento (AGENT_MAP.md §4)
# ──────────────────────────────────────────────


@dataclass
class RoutingRule:
    """Regra de roteamento para um contexto específico.

    Attributes:
        contexto: Descrição do contexto da requisição.
        capability: Nome da capability alvo.
        agente_primario: URN do agente primário.
        agente_fallback: URN(s) do(s) agente(s) de fallback.
        criterio: Justificativa da regra.
    """

    contexto: str
    capability: str
    agente_primario: str
    agente_fallback: list[str] = field(default_factory=list)
    criterio: str = ""


# Regras de roteamento por domínio
ROUTING_RULES_CORE: list[RoutingRule] = [
    RoutingRule(
        contexto="Travessia simples no KG",
        capability="graph.traverse",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:hermes"],
        criterio="KG Agent é especialista em operações de grafo",
    ),
    RoutingRule(
        contexto="Montagem de contexto para agente",
        capability="context.assemble",
        agente_primario="urn:apos:agent:context-agent",
        agente_fallback=["urn:apos:agent:hermes"],
        criterio="Context Agent possui pipeline de montagem dedicado",
    ),
    RoutingRule(
        contexto="Execução de query isolada",
        capability="query.execute",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:hermes"],
        criterio="KG Agent otimizado para queries Q01–Q16",
    ),
    RoutingRule(
        contexto="Mapeamento Task → OKR",
        capability="task-to-okr",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:hermes"],
        criterio="KG Agent executa Q01 diretamente",
    ),
    RoutingRule(
        contexto="Mapeamento Feature → Métricas",
        capability="feature-metrics",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:hermes"],
        criterio="KG Agent executa Q02 diretamente",
    ),
]

ROUTING_RULES_SUPPORT: list[RoutingRule] = [
    RoutingRule(
        contexto="Detecção de nós órfãos",
        capability="orphans.detect",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:governance"],
        criterio="KG Agent tem acesso completo ao grafo",
    ),
    RoutingRule(
        contexto="Detecção de ciclos",
        capability="cycles.detect",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:governance"],
        criterio="Requer travessia no grafo",
    ),
    RoutingRule(
        contexto="Análise de impacto",
        capability="impact.analyze",
        agente_primario="urn:apos:agent:knowledge-graph",
        agente_fallback=["urn:apos:agent:hermes", "urn:apos:agent:governance"],
        criterio="Requer travessia + contexto de negócio",
    ),
]

ROUTING_RULES_GOVERNANCE: list[RoutingRule] = [
    RoutingRule(
        contexto="Cálculo de Trust Score",
        capability="trust-score.calculate",
        agente_primario="urn:apos:agent:trust-score",
        agente_fallback=["urn:apos:agent:governance"],
        criterio="Trust Score Agent é especialista no cálculo",
    ),
    RoutingRule(
        contexto="Validação de integridade",
        capability="integrity.validate",
        agente_primario="urn:apos:agent:governance",
        agente_fallback=["urn:apos:agent:trust-score"],
        criterio="Governance Agent coordena auditoria",
    ),
    RoutingRule(
        contexto="Relatório de cobertura",
        capability="coverage.report",
        agente_primario="urn:apos:agent:governance",
        agente_fallback=["urn:apos:agent:trust-score"],
        criterio="Governance Agent gera relatórios consolidados",
    ),
]

# Todas as regras consolidadas
ROUTING_RULES: list[RoutingRule] = (
    ROUTING_RULES_CORE + ROUTING_RULES_SUPPORT + ROUTING_RULES_GOVERNANCE
)


# ──────────────────────────────────────────────
# Funções de Consulta
# ──────────────────────────────────────────────


def get_agent(urn_or_name: str) -> Optional[AgentDescriptor]:
    """Obtém um agente por URN ou nome.

    Args:
        urn_or_name: URN (``urn:apos:agent:...``) ou nome do agente.

    Returns:
        AgentDescriptor ou None se não encontrado.
    """
    if urn_or_name.startswith(AGENT_URN_PREFIX):
        return AGENTS_POR_URN.get(urn_or_name)
    return AGENTS_POR_NOME.get(urn_or_name)


def get_agents_by_capability(capability_name: str) -> list[AgentDescriptor]:
    """Retorna todos os agentes que implementam uma capability.

    Args:
        capability_name: Nome da capability (ex.: ``graph.traverse``).

    Returns:
        Lista de agentes habilitados para a capability.
    """
    for entry in AGENT_CAPABILITY_MATRIX:
        if entry.capability == capability_name:
            enabled_urns = [
                urn for urn, enabled in entry.agent_urns.items() if enabled
            ]
            return [AGENTS_POR_URN[urn] for urn in enabled_urns if urn in AGENTS_POR_URN]
    return []


def get_capabilities_by_agent(agent_urn: str) -> list[str]:
    """Retorna todas as capabilities que um agente pode executar.

    Args:
        agent_urn: URN do agente.

    Returns:
        Lista de nomes de capabilities.
    """
    return [
        entry.capability
        for entry in AGENT_CAPABILITY_MATRIX
        if entry.agent_urns.get(agent_urn, False)
    ]


def get_primary_agent(capability_name: str) -> Optional[str]:
    """Retorna o agente primário para uma capability.

    Args:
        capability_name: Nome da capability.

    Returns:
        URN do agente primário ou None se não encontrado.
    """
    for rule in ROUTING_RULES:
        if rule.capability == capability_name:
            return rule.agente_primario
    return None


def get_fallback_agents(capability_name: str) -> list[str]:
    """Retorna os agentes de fallback para uma capability.

    Args:
        capability_name: Nome da capability.

    Returns:
        Lista de URNs de fallback.
    """
    for rule in ROUTING_RULES:
        if rule.capability == capability_name:
            return rule.agente_fallback
    return []
