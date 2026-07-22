"""Roteamento de requisicoes para capabilities do APOS."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional, Callable
import time
import re


class MatchStrategy(Enum):
    EXACT = "exact"
    NODE_TYPE = "node_type"
    SIMILARITY = "similarity"


@dataclass
class CapabilityRequest:
    """Requisicao de capability."""
    id: str
    type: str = "capability"
    target: str = ""  # URN ou descricao
    params: dict = field(default_factory=dict)
    context: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


@dataclass
class ResolutionResult:
    """Resultado da resolucao de uma requisicao."""
    capability_id: str
    agent_urn: str
    match_strategy: MatchStrategy
    confidence: float = 1.0
    chain: list[str] = field(default_factory=list)


@dataclass
class NoCapabilityResult:
    """Resultado quando nenhuma capability atende."""
    request: CapabilityRequest
    suggestions: list[str] = field(default_factory=list)
    hint: str = ""


@dataclass
class CacheEntry:
    """Entrada no cache de roteamento."""
    result: ResolutionResult
    created_at: float = field(default_factory=time.time)
    ttl: float = 300.0  # 5 min default

    @property
    def expired(self) -> bool:
        return time.time() - self.created_at > self.ttl


class CapabilityRouter:
    """Roteador de requisicoes para capabilities.

    Suporta 3 estrategias de resolucao em cascata:
    1. Match exato por nome/URN
    2. Match por tipo de no (extraido da URN/descricao)
    3. Match por similaridade semantica (fallback)
    """

    def __init__(self):
        self._capabilities: dict[str, dict] = {}
        self._agents: dict[str, str] = {}  # agent_urn -> capability_id
        self._cache: dict[str, CacheEntry] = {}
        self._cache_ttl: float = 300.0  # 5 min

    def register_capability(self, cap_id: str, metadata: dict) -> None:
        """Registrar capability no roteador."""
        self._capabilities[cap_id] = metadata

    def register_agent(self, agent_urn: str, capability_id: str) -> None:
        """Registrar mapeamento agente -> capability."""
        self._agents[agent_urn] = capability_id

    def resolve(self, request: CapabilityRequest) -> ResolutionResult:
        """Resolver requisicao para a melhor capability.

        Tenta estrategias em ordem: exato -> node_type -> similaridade.
        """
        # 1. Check cache
        cache_key = f"{request.type}:{request.target}"
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if not entry.expired:
                return entry.result

        # 2. Match exato
        result = self._match_exact(request)
        if result:
            self._cache[cache_key] = CacheEntry(result, ttl=self._cache_ttl)
            return result

        # 3. Match por tipo de no
        result = self._match_by_node_type(request)
        if result:
            self._cache[cache_key] = CacheEntry(result, ttl=self._cache_ttl)
            return result

        # 4. Fallback: similaridade
        result = self._match_by_similarity(request)
        if result:
            self._cache[cache_key] = CacheEntry(result, ttl=self._cache_ttl * 2)
            return result

        raise LookupError(f"Nenhuma capability encontrada para: {request.target}")

    def resolve_chain(self, request: CapabilityRequest, max_depth: int = 5) -> list[ResolutionResult]:
        """Resolver chain de capabilities.

        Se uma capability retornar uma requisicao para outra capability,
        o router segue a chain ate max_depth.
        """
        results = []
        current = request
        for _ in range(max_depth):
            try:
                result = self.resolve(current)
                results.append(result)
            except LookupError:
                break
            # Se a capability resolvida indica proxima na chain
            cap = self._capabilities.get(result.capability_id, {})
            next_target = cap.get("routes_to")
            if not next_target:
                break
            current = CapabilityRequest(
                id=f"{current.id}-chain",
                target=next_target,
                params=current.params,
                context=current.context,
            )
        return results

    def invalidate_cache(self, target: Optional[str] = None) -> None:
        """Invalidar cache de roteamento."""
        if target:
            self._cache.pop(f"capability:{target}", None)
        else:
            self._cache.clear()

    def _match_exact(self, request: CapabilityRequest) -> Optional[ResolutionResult]:
        """Match exato por nome/URN da capability."""
        target = request.target.lower().strip()

        # Match por URN
        for cap_id, meta in self._capabilities.items():
            if cap_id.lower() == target:
                return self._make_result(cap_id, MatchStrategy.EXACT, 1.0)

        # Match por nome
        for cap_id, meta in self._capabilities.items():
            name = meta.get("name", "").lower()
            if name == target:
                return self._make_result(cap_id, MatchStrategy.EXACT, 0.95)

        return None

    def _match_by_node_type(self, request: CapabilityRequest) -> Optional[ResolutionResult]:
        """Match por tipo de no extraido da URN/descricao."""
        target = request.target.lower()

        # Extrair tipo da URN: urn:apos:{type}:{id}
        urn_match = re.match(r"urn:apos:(\w+):", target)
        node_type = urn_match.group(1) if urn_match else None

        # Extrair tipo da descricao
        if not node_type:
            type_keywords = {
                "task": ["task", "tarefa"],
                "feature": ["feature", "funcionalidade"],
                "release": ["release", "versao"],
                "okr": ["okr", "objetivo"],
                "metric": ["metrica", "metric"],
                "sprint": ["sprint"],
                "persona": ["persona", "usuario", "user"],
            }
            for ntype, keywords in type_keywords.items():
                if any(k in target for k in keywords):
                    node_type = ntype
                    break

        if node_type:
            for cap_id, meta in self._capabilities.items():
                read_types = [t.lower() for t in meta.get("kg_read", {}).get("node_types", [])]
                if node_type in read_types:
                    return self._make_result(cap_id, MatchStrategy.NODE_TYPE, 0.8)

        return None

    def _match_by_similarity(self, request: CapabilityRequest) -> Optional[ResolutionResult]:
        """Match por similaridade de descricao (fallback)."""
        target = request.target.lower()
        best_score = 0.0
        best_cap = None

        for cap_id, meta in self._capabilities.items():
            keywords = [
                meta.get("name", "").lower(),
                meta.get("description", "").lower(),
            ]
            desc = " ".join(keywords)
            # Simple word overlap score
            words = set(target.split())
            desc_words = set(desc.split())
            if not words:
                continue
            overlap = len(words & desc_words)
            score = overlap / max(len(words), 1)
            if score > best_score:
                best_score = score
                best_cap = cap_id

        if best_cap and best_score > 0.3:
            return self._make_result(best_cap, MatchStrategy.SIMILARITY, best_score)

        return None

    def _make_result(self, cap_id: str, strategy: MatchStrategy, confidence: float) -> ResolutionResult:
        """Criar resultado de resolucao."""
        agent_urn = ""
        for a_urn, c_id in self._agents.items():
            if c_id == cap_id:
                agent_urn = a_urn
                break
        return ResolutionResult(
            capability_id=cap_id,
            agent_urn=agent_urn,
            match_strategy=strategy,
            confidence=round(confidence, 2),
        )

    @property
    def cache_size(self) -> int:
        return len(self._cache)


def create_default_router() -> CapabilityRouter:
    """Criar router com capabilities e agentes padrao do APOS."""
    router = CapabilityRouter()

    # Capacidades core
    capabilities = {
        "trust_score.calculate": {
            "name": "Calcular Trust Score",
            "domain": "governance",
            "kg_read": {"node_types": ["task", "feature", "okr"]},
        },
        "orphans.detect": {
            "name": "Detectar Orfaos",
            "domain": "governance",
            "kg_read": {"node_types": ["task", "feature", "okr", "metric"]},
        },
        "context.assemble": {
            "name": "Montar Contexto",
            "domain": "core",
            "kg_read": {"node_types": ["task", "feature", "release", "okr", "metric"]},
        },
        "graph.traverse": {
            "name": "Navegar Grafo",
            "domain": "core",
            "kg_read": {"node_types": ["task", "feature", "release", "okr", "metric", "sprint"]},
        },
        "governance.validate": {
            "name": "Validar Alinhamento",
            "domain": "governance",
            "kg_read": {"node_types": ["task", "feature", "release", "okr"]},
        },
        "capability.router": {
            "name": "Roteamento Interno",
            "domain": "support",
            "kg_read": {"node_types": []},
        },
    }

    for cap_id, meta in capabilities.items():
        router.register_capability(cap_id, meta)

    # Agentes
    agents = {
        "urn:apos:agent:hermes": "context.assemble",
        "urn:apos:agent:knowledge-graph": "graph.traverse",
        "urn:apos:agent:trust-score": "trust_score.calculate",
        "urn:apos:agent:governance": "governance.validate",
        "urn:apos:agent:capability-router": "capability.router",
    }

    for agent_urn, cap_id in agents.items():
        router.register_agent(agent_urn, cap_id)

    return router
