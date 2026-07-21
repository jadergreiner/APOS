"""
APOS Retrieval Strategy — Estratégia de Recuperação de Contexto (Camada 3.5)

Define como o sistema consulta o Knowledge Graph para montar o contexto
dos agentes: queries padrão, caching multi-camada, scoring composto,
fallback progressivo e pipeline completo de retrieval.
"""

from __future__ import annotations

import copy
import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from apos.core.graph import KnowledgeGraph
from apos.core.types import EdgeType, Node, NodeType, parse_urn


# ──────────────────────────────────────────────
# Dataclasses
# ──────────────────────────────────────────────


@dataclass
class CacheEntry:
    """Entrada no sistema de cache multi-camada.

    Attributes:
        key: Chave única da cache.
        value: Dados armazenados.
        ttl_seconds: TTL em segundos.
        created_at: ISO 8601 de criação.
        hit_count: Contador de acessos (para LRU).
    """
    key: str
    value: Any
    ttl_seconds: int = 300
    created_at: Optional[datetime] = None
    hit_count: int = 0

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)

    @property
    def is_expired(self) -> bool:
        if self.created_at is None:
            return True
        age = (datetime.now(timezone.utc) - self.created_at).total_seconds()
        return age > self.ttl_seconds


@dataclass
class QuerySpec:
    """Especificação de uma query Q01-Q16.

    Attributes:
        type: Tipo da query (``"q01"``, ``"q04"``, etc.).
        cache_key: Chave para cache.
        description: Descrição legível.
        ttl: TTL em segundos.
        max_results: Máximo de resultados.
    """
    type: str
    cache_key: str = ""
    description: str = ""
    ttl: int = 300
    max_results: int = 50


@dataclass
class RankedResult:
    """Resultado ranqueado do motor de scoring.

    Attributes:
        urn: URN do nó.
        type: Tipo do nó.
        query_type: Tipo da query que originou.
        retrieval_score: Score composto [0.0, 1.0].
        data: Dados completos do resultado.
    """
    urn: str
    type: str
    query_type: str = ""
    retrieval_score: float = 0.0
    data: dict = field(default_factory=dict)


@dataclass
class RetrievalQuery:
    """Consulta do agente ao sistema de retrieval.

    Attributes:
        agent_id: ID do agente.
        anchor_urn: URN do nó âncora.
        intent: Intenção do agente (``"status"``, ``"impact"``, etc.).
        max_context_tokens: Limite de tokens.
        session_id: ID da sessão (opcional).
    """
    agent_id: str = ""
    anchor_urn: str = ""
    intent: str = "default"
    max_context_tokens: int = 8000
    session_id: Optional[str] = None


@dataclass
class QueryPlan:
    """Plano de queries a executar para uma dada intenção.

    Attributes:
        queries: Lista de especificações de query.
    """
    queries: list[QuerySpec] = field(default_factory=list)


@dataclass
class RetrievalResult:
    """Resultado completo do pipeline de retrieval.

    Attributes:
        context: Lista de blocos de contexto montados.
        tracing: Metadados de tracing da execução.
    """
    context: list[Any] = field(default_factory=list)
    tracing: dict = field(default_factory=dict)


# ──────────────────────────────────────────────
# Constantes de Queries
# ──────────────────────────────────────────────

# TTL por query (segundos)
QUERY_TTLS: dict[str, int] = {
    "q01": 300,   # 5 min
    "q02": 600,   # 10 min
    "q03": 600,   # 10 min
    "q04": 300,   # 5 min
    "q05": 1800,  # 30 min
    "q06": 300,   # 5 min
    "q07": 300,   # 5 min
    "q08": 300,   # 5 min
    "q09": 300,   # 5 min
    "q10": 3600,  # 1 h
    "q11": 3600,  # 1 h
    "q12": 3600,  # 1 h
    "q13": 3600,  # 1 h
    "q14": 3600,  # 1 h
    "q15": 1800,  # 30 min
    "q16": 1800,  # 30 min
}

# Max results por query
QUERY_MAX_RESULTS: dict[str, int] = {
    "q01": 10,
    "q02": 20,
    "q03": 50,
    "q04": 1,
    "q05": 20,
    "q06": 20,
    "q07": 10,
    "q08": 10,
    "q09": 50,
    "q10": 100,
    "q11": 100,
    "q12": 100,
    "q13": 100,
    "q14": 1,
    "q15": 1,
    "q16": 1,
}

# Thresholds por categoria de query
RETRIEVAL_THRESHOLDS: dict[str, float] = {
    "navigation": 0.3,
    "impact": 0.4,
    "orphan": 0.0,
    "trust": 0.0,
}

# Descrições das queries
QUERY_DESCRIPTIONS: dict[str, str] = {
    "q01": "Task → OKR (cadeia completa T→F→R→O)",
    "q02": "Feature → Métricas (F→R→O→M)",
    "q03": "Release Dashboard (visão consolidada)",
    "q04": "Task → Sprint (pertence_a)",
    "q05": "Persona → Features (envolve)",
    "q06": "Task Bloqueada → Métricas em Risco",
    "q07": "Impacto de Mudança de Task",
    "q08": "Impacto de Feature Removida",
    "q09": "Propagação de Bloqueio (BFS)",
    "q10": "Tasks Órfãs (sem contribui_para)",
    "q11": "Features Órfãs (sem parte_de)",
    "q12": "Métricas Órfãs (sem medido_por incoming)",
    "q13": "OKRs Órfãos (sem alcanca incoming)",
    "q14": "Trust Score — Coverage",
    "q15": "Trust Score — Quality",
    "q16": "Trust Score — Consistency",
}

# Mapa de invalidação de cache por mutação
INVALIDATION_MAP: dict[str, list[str]] = {
    "node_added": ["q10", "q11", "q12", "q13", "q14", "q15", "q16"],
    "node_removed": ["q10", "q11", "q12", "q13", "q14", "q15", "q16"],
    "edge_contribui": ["q01", "q06", "q07", "q10", "q14"],
    "edge_parte_de": ["q02", "q03", "q08", "q11", "q14"],
    "edge_alcanca": ["q01", "q02", "q03", "q13", "q14"],
    "edge_medido_por": ["q02", "q03", "q12", "q14"],
    "edge_bloqueia": ["q06", "q09"],
    "edge_pertence_a": ["q04"],
    "edge_envolve": ["q05"],
    "attr_changed": ["q01", "q04", "q06", "q07"],
    "any": ["q14", "q15", "q16"],
}

# Mapa de intenções para queries
QUERY_INTENT_MAP: dict[str, dict[Optional[NodeType], Any]] = {
    "status": {
        NodeType.TASK: QueryPlan(queries=[
            QuerySpec(type="q04", ttl=300, max_results=1, description="Task → Sprint"),
            QuerySpec(type="q01", ttl=300, max_results=10, description="Task → OKR"),
            QuerySpec(type="q06", ttl=300, max_results=20, description="Bloqueios → Métricas"),
        ]),
        NodeType.FEATURE: QueryPlan(queries=[
            QuerySpec(type="q02", ttl=600, max_results=20, description="Feature → Métricas"),
            QuerySpec(type="q05", ttl=1800, max_results=20, description="Personas envolvidas"),
        ]),
        NodeType.RELEASE: QueryPlan(queries=[
            QuerySpec(type="q03", ttl=600, max_results=50, description="Release Dashboard"),
            QuerySpec(type="q05", ttl=1800, max_results=20, description="Personas envolvidas"),
        ]),
        NodeType.OKR: QueryPlan(queries=[
            QuerySpec(type="q13", ttl=3600, max_results=100, description="OKRs Órfãos"),
            QuerySpec(type="q02", ttl=600, max_results=20, description="Métricas vinculadas"),
        ]),
        NodeType.METRIC: QueryPlan(queries=[
            QuerySpec(type="q12", ttl=3600, max_results=100, description="Métricas Órfãs"),
            QuerySpec(type="q07", ttl=300, max_results=10, description="Tasks que impactam"),
        ]),
        NodeType.SPRINT: QueryPlan(queries=[
            QuerySpec(type="q04", ttl=300, max_results=50, description="Tasks na Sprint (reverse)"),
        ]),
        NodeType.PERSONA: QueryPlan(queries=[
            QuerySpec(type="q05", ttl=1800, max_results=20, description="Features da Persona"),
        ]),
    },
    "impact": {
        NodeType.TASK: QueryPlan(queries=[
            QuerySpec(type="q07", ttl=300, max_results=10, description="Impacto de mudança"),
            QuerySpec(type="q06", ttl=300, max_results=20, description="Bloqueio → Métricas"),
            QuerySpec(type="q01", ttl=300, max_results=10, description="Task → OKR"),
        ]),
        NodeType.FEATURE: QueryPlan(queries=[
            QuerySpec(type="q08", ttl=300, max_results=10, description="Feature removida"),
            QuerySpec(type="q02", ttl=600, max_results=20, description="Feature → Métricas"),
        ]),
        NodeType.RELEASE: QueryPlan(queries=[
            QuerySpec(type="q03", ttl=600, max_results=50, description="Release Dashboard"),
            QuerySpec(type="q08", ttl=300, max_results=10, description="Impacto remoção"),
        ]),
    },
    "blockers": {
        NodeType.TASK: QueryPlan(queries=[
            QuerySpec(type="q09", ttl=300, max_results=50, description="Propagação de bloqueio"),
            QuerySpec(type="q06", ttl=300, max_results=20, description="Métricas em risco"),
        ]),
    },
    "orphans": {
        None: QueryPlan(queries=[
            QuerySpec(type="q10", ttl=3600, max_results=100, description="Tasks Órfãs"),
            QuerySpec(type="q11", ttl=3600, max_results=100, description="Features Órfãs"),
            QuerySpec(type="q12", ttl=3600, max_results=100, description="Métricas Órfãs"),
            QuerySpec(type="q13", ttl=3600, max_results=100, description="OKRs Órfãos"),
        ]),
    },
    "health": {
        None: QueryPlan(queries=[
            QuerySpec(type="q14", ttl=3600, max_results=1, description="Coverage"),
            QuerySpec(type="q15", ttl=1800, max_results=1, description="Quality"),
            QuerySpec(type="q16", ttl=1800, max_results=1, description="Consistency"),
        ]),
    },
    "default": {
        None: QueryPlan(queries=[
            QuerySpec(type="q01", ttl=300, max_results=10, description="Navegação básica"),
            QuerySpec(type="q04", ttl=300, max_results=1, description="Sprint da Task"),
        ]),
    },
}

DEFAULT_QUERY_PLAN = QueryPlan(queries=[
    QuerySpec(type="q01", ttl=300, max_results=10, description="Navegação básica"),
    QuerySpec(type="q04", ttl=300, max_results=1, description="Sprint da Task"),
])


# ──────────────────────────────────────────────
# QueryRegistry
# ──────────────────────────────────────────────


class QueryRegistry:
    """Registro central de queries Q01-Q16.

    Fornece acesso a definições de queries, cache keys,
    limites e descrições.
    """

    @staticmethod
    def get_query(query_type: str, anchor_urn: str = "") -> QuerySpec:
        """Retorna a especificação de uma query.

        Args:
            query_type: Tipo da query (``"q01"``, ..., ``"q16"``).
            anchor_urn: URN âncora para gerar cache_key.

        Returns:
            QuerySpec configurada.
        """
        cache_key = f"{query_type}:{anchor_urn}" if anchor_urn else query_type
        return QuerySpec(
            type=query_type,
            cache_key=cache_key,
            description=QUERY_DESCRIPTIONS.get(query_type, ""),
            ttl=QUERY_TTLS.get(query_type, 300),
            max_results=QUERY_MAX_RESULTS.get(query_type, 50),
        )

    @staticmethod
    def get_queries_for_intent(
        intent: str,
        anchor_type: Optional[NodeType] = None,
    ) -> QueryPlan:
        """Retorna o plano de queries para uma intenção e tipo de âncora.

        Args:
            intent: Intenção do agente.
            anchor_type: Tipo do nó âncora.

        Returns:
            QueryPlan com as queries a executar.
        """
        intent_map = QUERY_INTENT_MAP.get(intent, {})
        plan = intent_map.get(anchor_type) or intent_map.get(None)
        if plan is None:
            return DEFAULT_QUERY_PLAN
        return plan

    @staticmethod
    def classify_query_type(query_type: str) -> str:
        """Classifica o tipo de query para aplicar threshold adequado."""
        if query_type in ("q01", "q02", "q03", "q04", "q05"):
            return "navigation"
        elif query_type in ("q06", "q07", "q08", "q09"):
            return "impact"
        elif query_type in ("q10", "q11", "q12", "q13"):
            return "orphan"
        elif query_type in ("q14", "q15", "q16"):
            return "trust"
        return "navigation"


# ──────────────────────────────────────────────
# CacheManager
# ──────────────────────────────────────────────


class CacheManager:
    """Gerenciador de cache multi-camada (L1 memória, L2 Redis, L3 DynamoDB).

    Attributes:
        l1_max_entries: Máximo de entradas no cache L1 (default: 10000).
    """

    def __init__(self, l1_max_entries: int = 10000) -> None:
        self._l1: dict[str, CacheEntry] = {}
        self.l1_max_entries = l1_max_entries
        self._redis_prefix = "apos:retrieval:"
        self._redis_available = False  # Será configurado externamente
        self._dynamo_available = False

    # ─── L1 (local memory) ─────────────────────

    def get(self, key: str) -> Optional[Any]:
        """Busca resultado do cache L1 (memória local)."""
        entry = self._l1.get(key)
        if entry and not entry.is_expired:
            entry.hit_count += 1
            return entry.value
        if entry and entry.is_expired:
            self._l1.pop(key, None)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Armazena resultado no cache L1."""
        ttl = ttl or 300
        self._l1[key] = CacheEntry(
            key=key,
            value=value,
            ttl_seconds=ttl,
        )
        self._maybe_evict()

    def delete(self, key: str) -> bool:
        """Remove entrada do cache L1."""
        return self._l1.pop(key, None) is not None

    def clear(self) -> None:
        """Limpa todo o cache L1."""
        self._l1.clear()

    # ─── Multi-layer (L1 → L2 → L3) ────────────

    async def get_cached_query(
        self,
        query_type: str,
        query_key: str,
    ) -> Optional[Any]:
        """Busca resultado do cache (L1 → L2 → L3).

        Args:
            query_type: Tipo da query (q01, q04, etc.).
            query_key: Chave completa da query.

        Returns:
            Resultado em cache ou None.
        """
        full_key = f"{query_type}:{query_key}"

        # L1: Memória local
        entry = self._l1.get(full_key)
        if entry and not entry.is_expired:
            entry.hit_count += 1
            return entry.value
        if entry and entry.is_expired:
            self._l1.pop(full_key, None)

        # L2: Redis (stub — será implementado com redis-py)
        if self._redis_available:
            try:
                # Placeholder para redis.get(f"{self._redis_prefix}{full_key}")
                pass
            except ConnectionError:
                pass

        # L3: DynamoDB (apenas queries de scan)
        if self._dynamo_available and query_type in (
            "q10", "q11", "q12", "q13", "q14", "q15", "q16"
        ):
            # Placeholder para consulta DynamoDB
            pass

        return None

    async def set_cached_query(
        self,
        query_type: str,
        query_key: str,
        value: Any,
        ttl: Optional[int] = None,
    ) -> None:
        """Armazena resultado no cache (L1 + L2, L3 para scans).

        Args:
            query_type: Tipo da query.
            query_key: Chave completa.
            value: Valor a armazenar.
            ttl: TTL em segundos (opcional).
        """
        full_key = f"{query_type}:{query_key}"
        ttl = ttl or QUERY_TTLS.get(query_type, 300)

        # L1: Sempre
        self.set(full_key, value, ttl=ttl)

        # L2: Redis (best-effort)
        if self._redis_available:
            try:
                # Placeholder para redis.setex(...)
                pass
            except ConnectionError:
                pass

        # L3: DynamoDB (apenas queries de scan)
        if self._dynamo_available and query_type in (
            "q10", "q11", "q12", "q13", "q14", "q15", "q16"
        ):
            # Placeholder para DynamoDB put
            pass

    async def invalidate_for_urn(
        self,
        urn: str,
        mutation_type: str,
    ) -> None:
        """Invalida entradas de cache afetadas por uma mutação no KG.

        Args:
            urn: URN que sofreu mutação.
            mutation_type: Tipo de mutação (node_added, edge_contribui, etc.).
        """
        keys_to_invalidate = INVALIDATION_MAP.get(mutation_type, [])

        for key_pattern in keys_to_invalidate:
            if "*" in key_pattern:
                # Remove por padrão wildcard
                prefix = key_pattern.replace("*", "")
                keys_to_remove = [
                    k for k in self._l1 if k.startswith(prefix)
                ]
                for k in keys_to_remove:
                    self._l1.pop(k, None)
            elif key_pattern.startswith("q"):
                # Remove específico ou pattern
                if ":" in key_pattern:
                    self._l1.pop(key_pattern, None)
                else:
                    # Remove todas as entradas deste tipo de query
                    keys_to_remove = [
                        k for k in self._l1 if k.startswith(f"{key_pattern}:")
                    ]
                    for k in keys_to_remove:
                        self._l1.pop(k, None)

    # ─── LRU Eviction ──────────────────────────

    def _maybe_evict(self) -> None:
        """Aplica LRU se o número de entradas exceder o máximo."""
        if len(self._l1) <= self.l1_max_entries:
            return

        # Ordena por hit_count (menos acessados primeiro) e depois por idade
        sorted_entries = sorted(
            self._l1.values(),
            key=lambda e: (
                e.hit_count,
                e.created_at.timestamp() if e.created_at else 0,
            ),
        )

        # Remove até voltar ao limite
        excess = len(self._l1) - self.l1_max_entries
        for entry in sorted_entries[:excess]:
            self._l1.pop(entry.key, None)


# ──────────────────────────────────────────────
# ScoringEngine
# ──────────────────────────────────────────────


class ScoringEngine:
    """Motor de scoring composto para ranqueamento de resultados.

    Calcula o retrieval score combinando 3 fatores:
    relevance (0.5), freshness (0.3), recency (0.2).
    """

    @staticmethod
    def calculate_retrieval_score(
        node_type: str,
        edge_weight: float,
        updated_at: str,
        query_recency: float = 0.5,
        weight_relevance: float = 0.5,
        weight_freshness: float = 0.3,
        weight_recency: float = 0.2,
    ) -> float:
        """Calcula o score composto para ranqueamento de resultados.

        Args:
            node_type: Tipo do nó.
            edge_weight: Peso da aresta que conecta ao nó âncora.
            updated_at: ISO 8601 da última atualização.
            query_recency: Frequência de consulta [0.0, 1.0].
            weight_*: Pesos de cada fator.

        Returns:
            Float entre 0.0 e 1.0.
        """
        now = datetime.now(timezone.utc)

        # 1. Relevance — Peso da aresta
        relevance_score = edge_weight

        # 2. Freshness — Quão recente é a atualização
        try:
            updated = datetime.fromisoformat(updated_at)
            age_hours = (now - updated).total_seconds() / 3600
        except (ValueError, TypeError):
            age_hours = 999

        if age_hours <= 1:
            freshness_score = 1.0
        elif age_hours <= 6:
            freshness_score = 0.9
        elif age_hours <= 24:
            freshness_score = 0.7
        elif age_hours <= 72:
            freshness_score = 0.4
        elif age_hours <= 168:
            freshness_score = 0.2
        else:
            freshness_score = 0.1

        # 3. Recency — Frequência de consulta
        recency_score = min(query_recency, 1.0)

        score = (
            weight_relevance * relevance_score
            + weight_freshness * freshness_score
            + weight_recency * recency_score
        )

        return round(min(max(score, 0.0), 1.0), 4)

    @staticmethod
    async def rank_results(
        query_results: dict[str, list[dict]],
    ) -> list[RankedResult]:
        """Combina e ranqueia resultados de múltiplas queries.

        Args:
            query_results: Dict {query_type: [resultados]}.

        Returns:
            Lista de RankedResult ordenada por retrieval_score.
        """
        ranked: list[RankedResult] = []

        for query_type, results in query_results.items():
            category = QueryRegistry.classify_query_type(query_type)
            threshold = RETRIEVAL_THRESHOLDS.get(category, 0.3)
            max_results = QUERY_MAX_RESULTS.get(query_type, 50)

            for result in results[:max_results]:
                score = ScoringEngine.calculate_retrieval_score(
                    node_type=result.get("type", "unknown"),
                    edge_weight=result.get("weight", 0.5),
                    updated_at=result.get("updated_at", ""),
                    query_recency=0.5,
                )

                if score >= threshold:
                    ranked.append(RankedResult(
                        urn=result.get("urn", ""),
                        type=result.get("type", "unknown"),
                        query_type=query_type,
                        retrieval_score=score,
                        data=result,
                    ))

        # Ordena por score decrescente
        ranked.sort(key=lambda r: r.retrieval_score, reverse=True)

        # Deduplica por URN (mantém o de maior score)
        seen: dict[str, RankedResult] = {}
        for r in ranked:
            if r.urn not in seen or r.retrieval_score > seen[r.urn].retrieval_score:
                seen[r.urn] = r

        return list(seen.values())


# ──────────────────────────────────────────────
# FallbackChain
# ──────────────────────────────────────────────


DEFAULT_CONTEXT_TEMPLATE = {
    "status": "empty_graph",
    "anchor_urn": None,
    "message": (
        "O Knowledge Graph não contém informações sobre esta consulta. "
        "Isso pode ocorrer se:\n"
        "1. A URN não existe no grafo — verifique se o nó foi criado.\n"
        "2. O nó existe mas não tem conexões — é um nó órfão.\n"
        "3. O grafo está vazio — nenhum nó foi carregado.\n\n"
        "Ação recomendada: Criar o nó ou verificar a base de conhecimento."
    ),
    "blocks": [],
    "trust": None,
    "fallback": "template_default",
}


class FallbackChain:
    """Cadeia de fallback progressivo.

    Quando a query primária falha, tenta estratégias progressivamente
    mais caras: expandir profundidade → similaridade → contexto mínimo.
    """

    def __init__(self, kg: Optional[KnowledgeGraph] = None) -> None:
        self.kg = kg

    async def execute(
        self,
        query_type: str,
        anchor_urn: str,
    ) -> list[dict]:
        """Executa a cadeia de fallback completa.

        Args:
            query_type: Tipo da query original.
            anchor_urn: URN âncora.

        Returns:
            Resultados do primeiro fallback que funcionar.
        """
        # F1: Expandir profundidade
        results = await self._expand_depth(query_type, anchor_urn)
        if results:
            for r in results:
                r["fallback"] = "depth_expanded"
            return results

        # F2: Similaridade de atributos
        results = await self._similarity(anchor_urn)
        if results:
            for r in results:
                r["fallback"] = "attribute_similarity"
            return results

        # F3: Template default
        return [fallback_default_context(anchor_urn)]

    async def _expand_depth(
        self,
        query_type: str,
        anchor_urn: str,
    ) -> list[dict]:
        """Fallback 1: Expande profundidade da navegação."""
        if self.kg is None:
            return []

        depth_config = {
            "q01": {"path": [EdgeType.CONTRIBUI_PARA, EdgeType.PARTE_DE,
                             EdgeType.ALCANCA, EdgeType.MEDIDO_POR]},
            "q02": {"path": [EdgeType.PARTE_DE, EdgeType.ALCANCA,
                             EdgeType.MEDIDO_POR, EdgeType.ATINGE]},
        }

        config = depth_config.get(query_type)
        if config is None:
            return []

        if "path" in config:
            results = self.kg.traverse(start_urn=anchor_urn, path=config["path"])
            return [
                {"urn": urn, "edges": [
                    {"source": e.source, "target": e.target,
                     "type": e.type.value, "weight": e.weight}
                    for e in edge_list
                ], "type": ""}
                for urn, edge_list in results
            ]

        return []

    async def _similarity(
        self,
        anchor_urn: str,
        node_type: Optional[str] = None,
    ) -> list[dict]:
        """Fallback 2: Busca por similaridade textual nos atributos."""
        if self.kg is None:
            return []

        parsed = parse_urn(anchor_urn)
        name_hint = parsed[1] if parsed else anchor_urn.split(":")[-1]
        keywords = re.split(r"[-_]", name_hint)

        candidates = []

        for node in self.kg._nodes.values():
            if node_type and node.type.value != node_type:
                continue

            attrs_text = json.dumps(node.attributes).lower()
            match_count = sum(1 for kw in keywords if kw.lower() in attrs_text)

            if match_count > 0:
                candidates.append({
                    "urn": node.id,
                    "type": node.type.value,
                    "match_score": round(match_count / max(len(keywords), 1), 4),
                    "attributes": node.attributes,
                    "fallback": "attribute_similarity",
                })

        candidates.sort(key=lambda c: c["match_score"], reverse=True)
        return candidates[:5]

    @staticmethod
    def set_kg(self, kg: KnowledgeGraph) -> None:
        """Define o Knowledge Graph para fallbacks que precisam de acesso ao grafo."""
        self.kg = kg


def fallback_default_context(
    anchor_urn: Optional[str] = None,
) -> dict:
    """Fallback 3: Retorna contexto mínimo quando o grafo está vazio."""
    ctx = copy.deepcopy(DEFAULT_CONTEXT_TEMPLATE)
    if anchor_urn:
        ctx["anchor_urn"] = anchor_urn
        ctx["message"] = (
            f"A URN '{anchor_urn}' não foi encontrada no Knowledge Graph "
            "ou não possui conexões suficientes para montar contexto."
        )
    return ctx


# ──────────────────────────────────────────────
# RetrievalPipeline
# ──────────────────────────────────────────────


class RetrievalPipeline:
    """Pipeline completo de recuperação de contexto.

    Recebe uma consulta do agente, executa queries no KG,
    aplica scoring, boundaries e monta o contexto final.

    Args:
        kg: Instância do Knowledge Graph.
        cache: Gerenciador de cache.
        boundaries: Sistema de fronteiras de contexto (opcional).
    """

    def __init__(
        self,
        kg: Optional[KnowledgeGraph] = None,
        cache: Optional[CacheManager] = None,
        boundaries: Optional[Any] = None,
    ) -> None:
        self.kg = kg
        self.cache = cache or CacheManager()
        self.boundaries = boundaries
        self.fallback = FallbackChain(kg)
        self._node_type_cache: dict[str, Optional[NodeType]] = {}

    def _get_node_type(self, urn: str) -> Optional[NodeType]:
        """Identifica o tipo do nó a partir da URN."""
        if urn in self._node_type_cache:
            return self._node_type_cache[urn]

        if self.kg is None:
            parsed = parse_urn(urn)
            if parsed:
                try:
                    nt = NodeType(parsed[0])
                    self._node_type_cache[urn] = nt
                    return nt
                except (ValueError, KeyError):
                    pass
            return None

        node = self.kg.get_node(urn)
        if node:
            self._node_type_cache[urn] = node.type
            return node.type
        return None

    def _parse_query(self, query: RetrievalQuery) -> QueryPlan:
        """Mapeia a consulta do agente para queries Q01-Q16."""
        anchor_type = self._get_node_type(query.anchor_urn)

        intent_map = QUERY_INTENT_MAP.get(query.intent, {})
        plan = intent_map.get(anchor_type) or intent_map.get(None)

        if plan is None:
            plan = DEFAULT_QUERY_PLAN

        # Aplica cache_key a cada query
        updated_queries = []
        for q in plan.queries:
            updated_queries.append(QuerySpec(
                type=q.type,
                cache_key=f"{q.type}:{query.anchor_urn}",
                description=q.description,
                ttl=q.ttl,
                max_results=q.max_results,
            ))
        return QueryPlan(queries=updated_queries)

    async def _execute_query(
        self,
        q: QuerySpec,
        anchor_urn: str,
    ) -> list[dict]:
        """Executa uma query específica no Knowledge Graph."""
        if self.kg is None:
            return []

        if q.type == "q01":
            return await self._q01_task_to_okr(anchor_urn)
        elif q.type == "q04":
            return await self._q04_task_to_sprint(anchor_urn)
        elif q.type == "q06":
            return await self._q06_blocked_to_metrics(anchor_urn)
        elif q.type == "q10":
            return await self._q10_orphan_tasks()
        elif q.type == "q11":
            return await self._q11_orphan_features()
        elif q.type == "q12":
            return await self._q12_orphan_metrics()
        elif q.type == "q13":
            return await self._q13_orphan_okrs()
        elif q.type == "q14":
            return await self._q14_coverage()
        elif q.type == "q15":
            return await self._q15_quality()
        elif q.type == "q16":
            return await self._q16_consistency()
        return []

    async def _q01_task_to_okr(self, task_urn: str) -> list[dict]:
        """Q01: Task → OKR via cadeia T→F→R→O."""
        if self.kg is None:
            return []
        results = self.kg.traverse(
            start_urn=task_urn,
            path=[EdgeType.CONTRIBUI_PARA, EdgeType.PARTE_DE, EdgeType.ALCANCA],
        )
        output = []
        for urn, edges in results:
            node = self.kg.get_node(urn)
            attrs = node.attributes if node else {}
            weight = edges[-1].weight if edges else 0.5
            updated = node.metadata.updated_at if node else ""
            output.append({
                "urn": urn,
                "type": node.type.value if node else "okr",
                "weight": weight,
                "attributes": attrs,
                "updated_at": updated,
            })
        return output

    async def _q04_task_to_sprint(self, task_urn: str) -> list[dict]:
        """Q04: Task → Sprint."""
        if self.kg is None:
            return []
        results = self.kg.traverse(
            start_urn=task_urn,
            path=[EdgeType.PERTENCE_A],
        )
        output = []
        for urn, edges in results:
            node = self.kg.get_node(urn)
            attrs = node.attributes if node else {}
            weight = edges[-1].weight if edges else 1.0
            updated = node.metadata.updated_at if node else ""
            output.append({
                "urn": urn,
                "type": node.type.value if node else "sprint",
                "weight": weight,
                "attributes": attrs,
                "updated_at": updated,
            })
        return output

    async def _q06_blocked_to_metrics(self, task_urn: str) -> list[dict]:
        """Q06: Task Bloqueada → Métricas em Risco."""
        if self.kg is None:
            return []
        node = self.kg.get_node(task_urn)
        if node is None:
            return []
        if node.attributes.get("status") != "blocked":
            return []

        # BFS por bloqueios
        visited: set[str] = set()
        queue: list[tuple[str, int]] = [(task_urn, 0)]
        blocked_tasks: list[str] = []

        while queue:
            current_urn, depth = queue.pop(0)
            if current_urn in visited or depth > 5:
                continue
            visited.add(current_urn)

            if depth > 0:
                blocked_tasks.append(current_urn)

            for edge in self.kg._get_outbound(current_urn, EdgeType.BLOQUEIA):
                if edge.target not in visited:
                    queue.append((edge.target, depth + 1))

        # Para cada task bloqueada, encontra métricas impactadas
        output = []
        for bt_urn in blocked_tasks:
            impact_results = self.kg.traverse(
                start_urn=bt_urn,
                path=[EdgeType.IMPACTA],
            )
            for urn, edges in impact_results:
                node = self.kg.get_node(urn)
                attrs = node.attributes if node else {}
                weight = edges[-1].weight if edges else 0.5
                updated = node.metadata.updated_at if node else ""
                output.append({
                    "urn": urn,
                    "type": node.type.value if node else "metric",
                    "weight": weight,
                    "attributes": attrs,
                    "updated_at": updated,
                    "blocked_by": bt_urn,
                })
        return output

    async def _q10_orphan_tasks(self) -> list[dict]:
        """Q10: Tasks Órfãs (sem contribui_para)."""
        if self.kg is None:
            return []
        orphans = self.kg.detect_orphans(node_type=NodeType.TASK)
        return [
            {
                "urn": n.id,
                "type": n.type.value,
                "attributes": n.attributes,
                "updated_at": n.metadata.updated_at,
            }
            for n in orphans
        ]

    async def _q11_orphan_features(self) -> list[dict]:
        """Q11: Features Órfãs (sem parte_de)."""
        if self.kg is None:
            return []
        orphans = self.kg.detect_orphans(node_type=NodeType.FEATURE)
        return [
            {
                "urn": n.id,
                "type": n.type.value,
                "attributes": n.attributes,
                "updated_at": n.metadata.updated_at,
            }
            for n in orphans
        ]

    async def _q12_orphan_metrics(self) -> list[dict]:
        """Q12: Métricas Órfãs (sem medido_por incoming)."""
        if self.kg is None:
            return []
        orphans = self.kg.detect_orphans(node_type=NodeType.METRIC)
        return [
            {
                "urn": n.id,
                "type": n.type.value,
                "attributes": n.attributes,
                "updated_at": n.metadata.updated_at,
            }
            for n in orphans
        ]

    async def _q13_orphan_okrs(self) -> list[dict]:
        """Q13: OKRs Órfãos (sem alcanca incoming)."""
        if self.kg is None:
            return []
        # Usa o detect_orphans já existente para OKR
        orphans = self.kg.detect_orphans(node_type=NodeType.OKR)
        return [
            {
                "urn": n.id,
                "type": n.type.value,
                "attributes": n.attributes,
                "updated_at": n.metadata.updated_at,
            }
            for n in orphans
        ]

    async def _q14_coverage(self) -> list[dict]:
        """Q14: Trust Score — Coverage."""
        if self.kg is None:
            return []
        type_counts: dict[str, dict] = {}
        for node in self.kg._nodes.values():
            t = node.type.value
            if t not in type_counts:
                type_counts[t] = {"total": 0, "linked": 0}
            type_counts[t]["total"] += 1

        # Verifica links obrigatórios
        for node in self.kg._nodes.values():
            t = node.type.value
            if t == "task":
                if self.kg._get_outbound(node.id, EdgeType.CONTRIBUI_PARA):
                    type_counts[t]["linked"] += 1
            elif t == "feature":
                if self.kg._get_outbound(node.id, EdgeType.PARTE_DE):
                    type_counts[t]["linked"] += 1
            elif t == "okr":
                if self.kg._get_outbound(node.id, EdgeType.MEDIDO_POR):
                    type_counts[t]["linked"] += 1
            elif t == "metric":
                if self.kg._get_inbound(node.id, EdgeType.MEDIDO_POR):
                    type_counts[t]["linked"] += 1

        scores = []
        for t, counts in type_counts.items():
            if counts["total"] > 0:
                scores.append(counts["linked"] / counts["total"] * 100)

        overall = sum(scores) / max(len(scores), 1) if scores else 0.0
        return [{
            "type": "coverage",
            "overall": round(overall, 2),
            "by_type": type_counts,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }]

    async def _q15_quality(self) -> list[dict]:
        """Q15: Trust Score — Quality (integridade referencial)."""
        if self.kg is None:
            return []
        total_edges = len(self.kg._edges)
        if total_edges == 0:
            return [{"type": "quality", "overall": 100.0, "updated_at": datetime.now(timezone.utc).isoformat()}]

        valid_sources = sum(
            1 for e in self.kg._edges if e.source in self.kg._nodes
        )
        valid_targets = sum(
            1 for e in self.kg._edges if e.target in self.kg._nodes
        )

        quality = (valid_sources + valid_targets) / (2 * total_edges) * 100
        return [{
            "type": "quality",
            "overall": round(quality, 2),
            "total_edges": total_edges,
            "valid_sources": valid_sources,
            "valid_targets": valid_targets,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }]

    async def _q16_consistency(self) -> list[dict]:
        """Q16: Trust Score — Consistency."""
        if self.kg is None:
            return []
        # Regras de consistência simplificadas
        issues = []

        for node in self.kg._nodes.values():
            if node.type == NodeType.FEATURE:
                if node.attributes.get("status") == "shipped":
                    has_release = self.kg._get_outbound(node.id, EdgeType.PARTE_DE)
                    if not has_release:
                        issues.append(f"Feature {node.id} shipped but no release")
            if node.type == NodeType.TASK:
                if node.attributes.get("status") == "done":
                    blockers = self.kg._get_inbound(node.id, EdgeType.BLOQUEIA)
                    for b in blockers:
                        blocker_node = self.kg.get_node(b.source)
                        if blocker_node and blocker_node.attributes.get("status") == "blocked":
                            issues.append(f"Task {node.id} done but blocked by {b.source}")

        score = max(0, 100 - len(issues) * 10)
        return [{
            "type": "consistency",
            "overall": round(score, 2),
            "issues": issues[:20],
            "issue_count": len(issues),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }]

    async def retrieve(
        self,
        query: RetrievalQuery,
    ) -> RetrievalResult:
        """Pipeline completo de retrieval.

        Args:
            query: Consulta do agente.

        Returns:
            RetrievalResult com contexto montado + metadados de tracing.
        """
        from apos.context_engine.context import assemble_context

        start_time = time.time()
        tracing: dict = {
            "queries_executed": [],
            "cache_hits": [],
            "fallback_used": None,
        }

        # ── 1. Parsear consulta ──────────────────────────
        query_plan = self._parse_query(query)

        # ── 2. Executar queries ──────────────────────────
        all_results: list[dict] = []

        for q in query_plan.queries:
            q_key = f"{q.type}:{query.anchor_urn}"

            # 2a. Tentar cache
            cached = await self.cache.get_cached_query(q.type, q_key)
            if cached is not None:
                tracing.setdefault("cache_hits", []).append(q.type)
                if isinstance(cached, list):
                    all_results.extend(cached)
                else:
                    all_results.append(cached) if isinstance(cached, dict) else None
                continue

            # 2b. Executar query no KG
            results = await self._execute_query(q, query.anchor_urn)

            # 2c. Fallback se necessário
            if not results:
                fallback_results = await self.fallback.execute(q.type, query.anchor_urn)
                if fallback_results:
                    tracing["fallback_used"] = q.type
                    results = fallback_results

            # 2d. Popular cache
            if results:
                await self.cache.set_cached_query(
                    q.type, q_key, results, ttl=q.ttl
                )

            tracing.setdefault("queries_executed", []).append({
                "type": q.type,
                "count": len(results),
                "cached": False,
            })
            all_results.extend(results)

        # ── 3. Scoring e Ranking ──────────────────────────
        ranked = await ScoringEngine.rank_results(
            query_results={"composite": all_results}
        )

        # ── 4. Aplicar Boundaries ─────────────────────────
        bounded = ranked
        if self.boundaries is not None:
            bounded = self.boundaries.apply(
                results=ranked,
                max_tokens=query.max_context_tokens,
            )

        # ── 5. Montar contexto final ──────────────────────
        context = assemble_context(
            raw_nodes=[r.data for r in bounded],
            anchor_urn=query.anchor_urn,
        )

        elapsed = time.time() - start_time

        return RetrievalResult(
            context=context,
            tracing={
                "elapsed_ms": round(elapsed * 1000, 2),
                **tracing,
                "total_results": len(all_results),
                "ranked_results": len(ranked),
                "bounded_results": len(bounded),
            },
        )
