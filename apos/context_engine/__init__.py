"""
APOS Context Engine (Camada 3.5) — Contexto para Agentes de IA.

Fornece o pipeline completo de transformação do Knowledge Graph em contexto
consumível por agentes: extração, montagem, injeção e cleanup.
"""

from apos.context_engine.context import (
    ContextBlock,
    ContextPipeline,
    calculate_relevance,
    CONTEXT_TEMPLATE,
    PRIORITY_TIERS,
    TOKEN_LIMITS,
    CORE_CONTEXT_URNS,
    get_core_context,
    fallback_strategy,
)
from apos.context_engine.memory import (
    MemoryManager,
    ShortTermMemory,
    LongTermMemory,
    EpisodicMemory,
    SemanticMemory,
    InMemoryBackend,
    MemoryEntry,
    MemoryEvent,
    MemoryType,
)
from apos.context_engine.boundaries import (
    TokenBudget,
    InclusionCriteria,
    ExclusionRules,
    sanitize_attributes,
    validate_context_isolation,
    BUDGET_ALLOCATION,
    AGENT_BUDGET_PROFILES,
    NODE_TOKEN_LIMITS,
    RELEVANCE_THRESHOLDS,
    PRIVACY_BARRIERS,
)
from apos.context_engine.retrieval import (
    QueryRegistry,
    QuerySpec,
    CacheManager,
    CacheEntry,
    ScoringEngine,
    RankedResult,
    FallbackChain,
    RetrievalPipeline,
    RetrievalQuery,
    RetrievalResult,
    QueryPlan,
    QUERY_INTENT_MAP,
    QUERY_TTLS,
    QUERY_MAX_RESULTS,
    RETRIEVAL_THRESHOLDS,
)

__all__ = [
    # context
    "ContextBlock",
    "ContextPipeline",
    "calculate_relevance",
    "CONTEXT_TEMPLATE",
    "PRIORITY_TIERS",
    "TOKEN_LIMITS",
    "CORE_CONTEXT_URNS",
    "get_core_context",
    "fallback_strategy",
    # memory
    "MemoryManager",
    "ShortTermMemory",
    "LongTermMemory",
    "EpisodicMemory",
    "SemanticMemory",
    "InMemoryBackend",
    "MemoryEntry",
    "MemoryEvent",
    "MemoryType",
    # boundaries
    "TokenBudget",
    "InclusionCriteria",
    "ExclusionRules",
    "sanitize_attributes",
    "validate_context_isolation",
    "BUDGET_ALLOCATION",
    "AGENT_BUDGET_PROFILES",
    "NODE_TOKEN_LIMITS",
    "RELEVANCE_THRESHOLDS",
    "PRIVACY_BARRIERS",
    # retrieval
    "QueryRegistry",
    "QuerySpec",
    "CacheManager",
    "CacheEntry",
    "ScoringEngine",
    "RankedResult",
    "FallbackChain",
    "RetrievalPipeline",
    "RetrievalQuery",
    "RetrievalResult",
    "QueryPlan",
    "QUERY_INTENT_MAP",
    "QUERY_TTLS",
    "QUERY_MAX_RESULTS",
    "RETRIEVAL_THRESHOLDS",
]
