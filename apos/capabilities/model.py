"""
APOS Capability Model — Modelo de Capacidades de Agentes (Camada 3.6)

Define a estrutura atômica de uma capability, seu ciclo de vida (máquina de
estados), e o registro central (CapabilityRegistry) para descoberta e consulta.

Conforme CAPABILITY_MODEL.md — Sprint 0.6, Tarefa T0.6.1.
"""

from __future__ import annotations

import copy
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


# ──────────────────────────────────────────────
# Enums Fundamentais
# ──────────────────────────────────────────────


class CapabilityDomain(str, Enum):
    """Domínios funcionais de uma capability.

    - CORE: Núcleo do APOS — operações fundamentais do grafo.
    - SUPPORT: Suporte — operações auxiliares (detecção, manutenção).
    - GOVERNANCE: Governança — auditoria, qualidade, trust score.
    """

    CORE = "core"
    SUPPORT = "support"
    GOVERNANCE = "governance"


class CapabilityStatus(str, Enum):
    """Estados do ciclo de vida de uma capability (máquina de estados).

    Fluxo principal: REGISTERED → READY → RUNNING → COMPLETED / FAILED / TIMEOUT.
    Deprecação a partir de REGISTERED ou READY.
    """

    REGISTERED = "registered"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    DEPRECATED = "deprecated"


class CheckType(str, Enum):
    """Tipos de verificação para pré-condições de capability."""

    NODE_EXISTS = "node_exists"
    EDGE_EXISTS = "edge_exists"
    NODE_HAS_ATTRIBUTE = "node_has_attribute"
    NODE_IN_DOMAIN = "node_in_domain"
    KG_NOT_EMPTY = "kg_not_empty"
    AGENT_AUTHORIZED = "agent_authorized"
    QUERY_HAS_RESULTS = "query_has_results"
    CUSTOM = "custom"


class EffectType(str, Enum):
    """Tipos de efeito que uma capability causa no Knowledge Graph."""

    NODE_CREATED = "node_created"
    NODE_UPDATED = "node_updated"
    NODE_DELETED = "node_deleted"
    EDGE_CREATED = "edge_created"
    EDGE_UPDATED = "edge_updated"
    EVENT_LOGGED = "event_logged"
    TRUST_UPDATED = "trust_updated"
    CONTEXT_INJECTED = "context_injected"


# ──────────────────────────────────────────────
# Dataclasses de Capability
# ──────────────────────────────────────────────


@dataclass
class PreCondition:
    """Pré-condição que deve ser verdadeira antes da execução da capability.

    Attributes:
        description: Descrição legível da condição.
        check_type: Tipo de verificação a realizar.
        params: Parâmetros da verificação (ex.: {"urn": "{target_urn}"}).
    """

    description: str
    check_type: CheckType
    params: dict = field(default_factory=dict)


@dataclass
class Effect:
    """Efeito esperado no Knowledge Graph após execução bem-sucedida.

    Attributes:
        description: Descrição legível do efeito.
        effect_type: Tipo de efeito.
        target: URN ou padrão de URN afetado.
        delta: Mudanças específicas (opcional).
    """

    description: str
    effect_type: EffectType
    target: str = ""
    delta: Optional[dict] = None


@dataclass
class KGPattern:
    """Padrão de leitura/escrita no Knowledge Graph.

    Attributes:
        nodes: Lista de tipos de nó envolvidos.
        edges: Lista de tipos de aresta envolvidos.
        queries: Lista de queries (ex.: Q01–Q16) utilizadas.
        description: Descrição textual do padrão.
    """

    nodes: list[str] = field(default_factory=list)
    edges: list[str] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class CapabilityMetadata:
    """Metadados de registro de uma capability.

    Attributes:
        created_at: ISO 8601 — data de registro.
        updated_at: ISO 8601 — última modificação.
        version: Semver da capability.
        status: Estado atual do ciclo de vida.
        tags: Tags para descoberta.
        author: Quem criou/registrou.
        ttl_hours: Horas até expirar se não usada (0 = sem expiração).
    """

    created_at: str = ""
    updated_at: str = ""
    version: str = "1.0.0"
    status: CapabilityStatus = CapabilityStatus.REGISTERED
    tags: list[str] = field(default_factory=list)
    author: str = ""
    ttl_hours: int = 0


@dataclass
class Capability:
    """Unidade atômica de competência que um agente APOS possui.

    Attributes:
        id: URN única no formato ``urn:apos:cap:{domain}:{name}``.
        name: Nome legível (dot-notation, ex.: ``trust-score.calculate``).
        description: Descrição do que a capability faz.
        domain: Domínio funcional (core, support, governance).
        version: Semver da capability.
        input_schema: Schema JSON (Draft 2020-12) dos parâmetros de entrada.
        output_schema: Schema JSON do retorno.
        pre_conditions: Lista de pré-condições para execução.
        effects: Lista de efeitos no KG após execução.
        enabled_agents: URNs dos agentes que podem executar esta capability.
        kg_read: Padrões de leitura no KG.
        kg_write: Padrões de escrita no KG.
        metadata: Metadados de registro.
    """

    id: str  # urn:apos:cap:{domain}:{name}
    name: str
    description: str
    domain: CapabilityDomain = CapabilityDomain.CORE
    version: str = "1.0.0"
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    pre_conditions: list[PreCondition] = field(default_factory=list)
    effects: list[Effect] = field(default_factory=list)
    enabled_agents: list[str] = field(default_factory=list)
    kg_read: list[KGPattern] = field(default_factory=list)
    kg_write: list[KGPattern] = field(default_factory=list)
    metadata: CapabilityMetadata = field(default_factory=CapabilityMetadata)

    def __post_init__(self) -> None:
        if not self.id.startswith("urn:apos:cap:"):
            raise ValueError(
                f"Capability id deve começar com 'urn:apos:cap:'. Obtido: {self.id}"
            )

    @property
    def status(self) -> CapabilityStatus:
        """Acesso rápido ao status atual."""
        return self.metadata.status

    def to_dict(self) -> dict:
        """Serializa a capability para dicionário JSON-compatível."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "domain": self.domain.value,
            "version": self.version,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "pre_conditions": [
                {
                    "description": pc.description,
                    "check_type": pc.check_type.value,
                    "params": pc.params,
                }
                for pc in self.pre_conditions
            ],
            "effects": [
                {
                    "description": e.description,
                    "effect_type": e.effect_type.value,
                    "target": e.target,
                    "delta": e.delta,
                }
                for e in self.effects
            ],
            "enabled_agents": list(self.enabled_agents),
            "kg_read": [
                {
                    "nodes": p.nodes,
                    "edges": p.edges,
                    "queries": p.queries,
                    "description": p.description,
                }
                for p in self.kg_read
            ],
            "kg_write": [
                {
                    "nodes": p.nodes,
                    "edges": p.edges,
                    "queries": p.queries,
                    "description": p.description,
                }
                for p in self.kg_write
            ],
            "metadata": {
                "created_at": self.metadata.created_at,
                "updated_at": self.metadata.updated_at,
                "version": self.metadata.version,
                "status": self.metadata.status.value,
                "tags": self.metadata.tags,
                "author": self.metadata.author,
                "ttl_hours": self.metadata.ttl_hours,
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> Capability:
        """Constrói uma capability a partir de um dicionário."""
        pre_conditions = []
        for pc in data.get("pre_conditions", []):
            pre_conditions.append(
                PreCondition(
                    description=pc["description"],
                    check_type=CheckType(pc["check_type"]),
                    params=pc.get("params", {}),
                )
            )

        effects = []
        for e in data.get("effects", []):
            effects.append(
                Effect(
                    description=e["description"],
                    effect_type=EffectType(e["effect_type"]),
                    target=e.get("target", ""),
                    delta=e.get("delta"),
                )
            )

        kg_read = [
            KGPattern(
                nodes=p.get("nodes", []),
                edges=p.get("edges", []),
                queries=p.get("queries", []),
                description=p.get("description", ""),
            )
            for p in data.get("kg_read", [])
        ]

        kg_write = [
            KGPattern(
                nodes=p.get("nodes", []),
                edges=p.get("edges", []),
                queries=p.get("queries", []),
                description=p.get("description", ""),
            )
            for p in data.get("kg_write", [])
        ]

        meta = data.get("metadata", {})
        metadata = CapabilityMetadata(
            created_at=meta.get("created_at", ""),
            updated_at=meta.get("updated_at", ""),
            version=meta.get("version", "1.0.0"),
            status=CapabilityStatus(meta.get("status", "registered")),
            tags=meta.get("tags", []),
            author=meta.get("author", ""),
            ttl_hours=meta.get("ttl_hours", 0),
        )

        return cls(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            domain=CapabilityDomain(data.get("domain", "core")),
            version=data.get("version", "1.0.0"),
            input_schema=data.get("input_schema", {}),
            output_schema=data.get("output_schema", {}),
            pre_conditions=pre_conditions,
            effects=effects,
            enabled_agents=data.get("enabled_agents", []),
            kg_read=kg_read,
            kg_write=kg_write,
            metadata=metadata,
        )


# ──────────────────────────────────────────────
# Ciclo de Vida
# ──────────────────────────────────────────────


_VALID_TRANSITIONS: dict[CapabilityStatus, set[CapabilityStatus]] = {
    CapabilityStatus.REGISTERED: {CapabilityStatus.READY, CapabilityStatus.DEPRECATED},
    CapabilityStatus.READY: {CapabilityStatus.RUNNING, CapabilityStatus.DEPRECATED},
    CapabilityStatus.RUNNING: {
        CapabilityStatus.COMPLETED,
        CapabilityStatus.FAILED,
        CapabilityStatus.TIMEOUT,
    },
    CapabilityStatus.COMPLETED: {CapabilityStatus.READY},
    CapabilityStatus.FAILED: {CapabilityStatus.READY},
    CapabilityStatus.TIMEOUT: {CapabilityStatus.READY},
    CapabilityStatus.DEPRECATED: set(),
}


def can_transition(current: CapabilityStatus, target: CapabilityStatus) -> bool:
    """Verifica se a transição de estado é válida."""
    return target in _VALID_TRANSITIONS.get(current, set())


def transition(current: CapabilityStatus, target: CapabilityStatus) -> CapabilityStatus:
    """Executa a transição de estado, levantando erro se inválida.

    Returns:
        O novo estado (target).

    Raises:
        ValueError: Se a transição não for permitida.
    """
    if not can_transition(current, target):
        raise ValueError(
            f"Transição inválida: {current.value} → {target.value}. "
            f"Transições permitidas de '{current.value}': "
            f"{[s.value for s in _VALID_TRANSITIONS.get(current, set())]}"
        )
    return target


@dataclass
class LifecycleConfig:
    """Parâmetros configuráveis do ciclo de vida de uma capability.

    Attributes:
        max_retries: Tentativas antes de falhar definitivamente.
        retry_delay_seconds: Intervalo entre retentativas.
        max_execution_seconds: Timeout por execução.
        ttl_days_unused: Dias sem uso até deprecação automática.
        version_compatibility: Range semver aceito.
    """

    max_retries: int = 3
    retry_delay_seconds: int = 5
    max_execution_seconds: int = 30
    ttl_days_unused: int = 90
    version_compatibility: str = "^1.0"


# ──────────────────────────────────────────────
# CapabilityRegistry
# ──────────────────────────────────────────────


class CapabilityRegistry:
    """Registro central de capabilities do APOS.

    Gerencia o ciclo de vida, descoberta e consulta de capabilities.
    Capabilities são armazenadas em memória com indexação por domínio,
    agente e status para lookup eficiente.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}
        self._domain_index: dict[str, set[str]] = {}
        self._agent_index: dict[str, set[str]] = {}
        self._execution_log: list[dict] = []

    # ───────────────
    # CRUD
    # ───────────────

    def register(self, capability: Capability) -> bool:
        """Registra uma nova capability.

        Se o ID já existir, retorna False sem modificar o registro.
        Se for um registro novo, status é definido como REGISTERED.

        Returns:
            True se registrada com sucesso, False se ID já existir.
        """
        if capability.id in self._capabilities:
            return False

        # Garante metadados de criação
        now = datetime.now(timezone.utc).isoformat()
        capability.metadata.created_at = now
        capability.metadata.updated_at = now
        if capability.metadata.status == CapabilityStatus.REGISTERED:
            pass  # já está no estado correto

        self._capabilities[capability.id] = capability

        # Indexa por domínio
        domain = capability.domain.value
        self._domain_index.setdefault(domain, set()).add(capability.id)

        # Indexa por agente
        for agent_urn in capability.enabled_agents:
            self._agent_index.setdefault(agent_urn, set()).add(capability.id)

        return True

    def unregister(self, capability_id: str) -> bool:
        """Remove (depreca) uma capability pelo ID.

        A capability é marcada como DEPRECATED e removida dos índices.
        O registro original permanece acessível via get() para rastreabilidade.

        Returns:
            True se encontrada e deprecada, False se não existir.
        """
        cap = self._capabilities.get(capability_id)
        if cap is None:
            return False

        cap.metadata.status = CapabilityStatus.DEPRECATED
        cap.metadata.updated_at = datetime.now(timezone.utc).isoformat()

        # Remove dos índices
        domain = cap.domain.value
        if domain in self._domain_index:
            self._domain_index[domain].discard(capability_id)

        for agent_urn in list(self._agent_index.keys()):
            self._agent_index[agent_urn].discard(capability_id)

        return True

    def get(self, capability_id: str) -> Optional[Capability]:
        """Recupera uma capability pelo ID.

        Args:
            capability_id: URN da capability.

        Returns:
            A capability ou None se não encontrada.
        """
        return self._capabilities.get(capability_id)

    # ───────────────
    # Busca e Descoberta
    # ───────────────

    def discover(self, query: str = "", **filters: Any) -> list[Capability]:
        """Descobre capabilities por critérios de busca.

        Args:
            query: Texto livre para busca no nome e descrição.
            **filters: Filtros adicionais (domain, status, tag, agent).

        Returns:
            Lista de capabilities que correspondem aos critérios.
        """
        results = list(self._capabilities.values())

        # Filtro por texto livre
        if query:
            q = query.lower()
            results = [
                c
                for c in results
                if q in c.name.lower() or q in c.description.lower()
            ]

        # Filtro por domínio
        domain = filters.get("domain")
        if domain is not None:
            if isinstance(domain, CapabilityDomain):
                domain = domain.value
            results = [c for c in results if c.domain.value == domain]

        # Filtro por status
        status = filters.get("status")
        if status is not None:
            if isinstance(status, CapabilityStatus):
                status = status.value
            results = [c for c in results if c.metadata.status.value == status]

        # Filtro por tag
        tag = filters.get("tag")
        if tag is not None:
            results = [c for c in results if tag in c.metadata.tags]

        # Filtro por agente
        agent = filters.get("agent")
        if agent is not None:
            results = [c for c in results if agent in c.enabled_agents]

        return results

    def find(self, status: str = "ready", **filters: Any) -> list[Capability]:
        """Busca capabilities por status e filtros adicionais.

        Args:
            status: Status desejado (default: "ready").
            **filters: Filtros adicionais.

        Returns:
            Lista de capabilities correspondentes.
        """
        return self.discover(status=status, **filters)

    def list_by_domain(self, domain: str | CapabilityDomain) -> list[Capability]:
        """Lista todas as capabilities de um domínio.

        Args:
            domain: Domínio (string ou enum).

        Returns:
            Lista de capabilities do domínio.
        """
        if isinstance(domain, CapabilityDomain):
            domain = domain.value
        cap_ids = self._domain_index.get(domain, set())
        return [self._capabilities[cid] for cid in cap_ids if cid in self._capabilities]

    def list_by_agent(self, agent_urn: str) -> list[Capability]:
        """Lista todas as capabilities habilitadas para um agente.

        Args:
            agent_urn: URN do agente (ex.: ``urn:apos:agent:hermes``).

        Returns:
            Lista de capabilities que o agente pode executar.
        """
        cap_ids = self._agent_index.get(agent_urn, set())
        return [self._capabilities[cid] for cid in cap_ids if cid in self._capabilities]

    def find_by_agent(self, agent_id: str) -> list[Capability]:
        """Alias para list_by_agent."""
        return self.list_by_agent(agent_id)

    def find_by_urn(self, target_urn: str) -> list[Capability]:
        """Retorna capabilities que podem operar sobre uma URN específica.

        Verifica se a URN alvo corresponde a padrões declarados em kg_read.

        Args:
            target_urn: URN alvo.

        Returns:
            Lista de capabilities relevantes para a URN.
        """
        results: list[Capability] = []
        for cap in self._capabilities.values():
            for pattern in cap.kg_read:
                if any(tag in target_urn for tag in pattern.nodes):
                    if cap not in results:
                        results.append(cap)
                        break
        return results

    # ───────────────
    # Execução
    # ───────────────

    def execute(
        self, capability_id: str, input_data: dict, agent_id: str
    ) -> dict:
        """Executa uma capability e registra a execução.

        Valida pré-condições, transiciona estados e loga o resultado.

        Args:
            capability_id: URN da capability.
            input_data: Dados de entrada conforme input_schema.
            agent_id: URN do agente solicitante.

        Returns:
            Dict com status, result (se completed) ou error_message.

        Raises:
            ValueError: Se capability não encontrada ou agente não autorizado.
        """
        cap = self.get(capability_id)
        if cap is None:
            raise ValueError(f"Capability '{capability_id}' não encontrada")

        if agent_id not in cap.enabled_agents:
            raise ValueError(
                f"Agente '{agent_id}' não está habilitado para '{capability_id}'"
            )

        # Transição READY → RUNNING
        if cap.status == CapabilityStatus.READY:
            cap.metadata.status = CapabilityStatus.RUNNING
            cap.metadata.updated_at = datetime.now(timezone.utc).isoformat()
        elif cap.status != CapabilityStatus.RUNNING:
            # Se não está READY, tenta transicionar de REGISTERED para READY
            if cap.status == CapabilityStatus.REGISTERED:
                cap.metadata.status = CapabilityStatus.READY
            cap.metadata.status = CapabilityStatus.RUNNING

        execution_id = str(uuid.uuid4())
        started_at = datetime.now(timezone.utc).isoformat()

        execution_record = {
            "execution_id": execution_id,
            "capability_id": capability_id,
            "agent_id": agent_id,
            "input_snapshot": input_data,
            "status": "running",
            "started_at": started_at,
        }

        try:
            # Aqui seria chamada a implementação real da capability
            # Por enquanto, simulamos execução bem-sucedida
            output = {"executed": True, "capability": capability_id}

            cap.metadata.status = CapabilityStatus.COMPLETED
            cap.metadata.updated_at = datetime.now(timezone.utc).isoformat()

            execution_record["status"] = "completed"
            execution_record["output_snapshot"] = output
            execution_record["completed_at"] = datetime.now(timezone.utc).isoformat()

            self._execution_log.append(execution_record)

            return {
                "status": "completed",
                "execution_id": execution_id,
                "result": output,
            }

        except Exception as e:
            cap.metadata.status = CapabilityStatus.FAILED
            cap.metadata.updated_at = datetime.now(timezone.utc).isoformat()

            execution_record["status"] = "failed"
            execution_record["error_message"] = str(e)
            execution_record["completed_at"] = datetime.now(timezone.utc).isoformat()

            self._execution_log.append(execution_record)

            return {
                "status": "failed",
                "execution_id": execution_id,
                "error_message": str(e),
            }

    # ───────────────
    # Transição de Estado
    # ───────────────

    def set_status(
        self, capability_id: str, new_status: CapabilityStatus
    ) -> bool:
        """Define o status de uma capability, validando a transição.

        Args:
            capability_id: URN da capability.
            new_status: Status alvo.

        Returns:
            True se a transição foi bem-sucedida.

        Raises:
            ValueError: Se capability não encontrada ou transição inválida.
        """
        cap = self.get(capability_id)
        if cap is None:
            raise ValueError(f"Capability '{capability_id}' não encontrada")

        current = cap.metadata.status
        cap.metadata.status = transition(current, new_status)
        cap.metadata.updated_at = datetime.now(timezone.utc).isoformat()
        return True

    def list_executions(
        self, capability_id: Optional[str] = None, limit: int = 100
    ) -> list[dict]:
        """Retorna o histórico de execuções.

        Args:
            capability_id: Filtrar por capability (opcional).
            limit: Máximo de registros.

        Returns:
            Lista de registros de execução.
        """
        if capability_id:
            return [
                e
                for e in self._execution_log
                if e["capability_id"] == capability_id
            ][-limit:]
        return self._execution_log[-limit:]

    @property
    def count(self) -> int:
        """Número total de capabilities registradas."""
        return len(self._capabilities)

    def __contains__(self, capability_id: str) -> bool:
        return capability_id in self._capabilities

    def __len__(self) -> int:
        return self.count

    def __iter__(self):
        return iter(self._capabilities.values())
