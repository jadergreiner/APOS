"""
APOS Context Boundaries — Fronteiras de Contexto para Agentes de IA (Camada 3.5)

Define o que entra e o que fica fora da janela de contexto de um agente:
critérios de inclusão, exclusão, token budget, sanitização e não vazamento.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────

# Alocação base de token budget (percentuais)
BUDGET_ALLOCATION: dict[str, float] = {
    "core": 0.30,
    "auxiliary": 0.40,
    "historical": 0.20,
    "metadata": 0.10,
}

# Perfis de budget por tipo de agente
AGENT_BUDGET_PROFILES: dict[str, dict] = {
    "task_agent": {"core": 0.35, "auxiliary": 0.40, "historical": 0.15, "metadata": 0.10, "max_tokens": 8000},
    "feature_agent": {"core": 0.25, "auxiliary": 0.45, "historical": 0.20, "metadata": 0.10, "max_tokens": 8000},
    "release_manager": {"core": 0.20, "auxiliary": 0.50, "historical": 0.20, "metadata": 0.10, "max_tokens": 8000},
    "sprint_agent": {"core": 0.30, "auxiliary": 0.35, "historical": 0.25, "metadata": 0.10, "max_tokens": 8000},
    "query_agent": {"core": 0.20, "auxiliary": 0.30, "historical": 0.35, "metadata": 0.15, "max_tokens": 4000},
}

# Limites de tokens por tipo de nó
NODE_TOKEN_LIMITS: dict[str, dict] = {
    "task":     {"max_tokens": 500,  "ttl_hours": 24,  "compressible": True,  "priority": "high"},
    "feature":  {"max_tokens": 300,  "ttl_hours": 48,  "compressible": True,  "priority": "high"},
    "release":  {"max_tokens": 400,  "ttl_hours": 48,  "compressible": True,  "priority": "medium"},
    "okr":      {"max_tokens": 300,  "ttl_hours": 72,  "compressible": True,  "priority": "medium"},
    "metric":   {"max_tokens": 200,  "ttl_hours": 72,  "compressible": True,  "priority": "medium_high"},
    "sprint":   {"max_tokens": 300,  "ttl_hours": 24,  "compressible": True,  "priority": "high"},
    "persona":  {"max_tokens": 350,  "ttl_hours": 168, "compressible": True,  "priority": "low"},
    "blocker":  {"max_tokens": 250,  "ttl_hours": 12,  "compressible": False, "priority": "critical"},
    "edge":     {"max_tokens": 100,  "ttl_hours": None, "compressible": True,  "priority": "variable"},
}

# Thresholds de relevância
RELEVANCE_THRESHOLDS: dict[str, float] = {
    "always_include": 0.80,
    "budget_dependent": 0.50,
    "optional": 0.30,
    "exclude_default": 0.10,
}

# Janelas temporais por tipo de nó (horas)
FRESHNESS_WINDOWS: dict[str, float] = {
    "task": 72,
    "feature": 72,
    "release": 72,
    "sprint": 168,
    "okr": 720,
    "metric": 168,
    "persona": 2160,
    "rule": float("inf"),
}

# Barreiras de privacidade
PRIVACY_BARRIERS: dict = {
    "blocked_fields": [
        "password", "api_key", "secret", "token", "credential",
        "cpf", "ssn", "email_personal", "phone", "address",
        "internal_note", "audit_log_raw", "raw_prompt",
    ],
    "blocked_patterns": [
        r"^sk-[A-Za-z0-9]{32,}$",
        r"^ghp_[A-Za-z0-9]{36}$",
        r"^AKIA[A-Z0-9]{16}$",
        r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b",
        r"\b\d{2}/\d{2}/\d{4}\b",
    ],
    "blocked_node_types": [
        "internal_config",
        "audit_entry",
        "raw_embedding",
    ],
}


# ──────────────────────────────────────────────
# TokenBudget
# ──────────────────────────────────────────────


@dataclass
class TokenBudget:
    """Gerencia a alocação de tokens entre categorias de contexto.

    Attributes:
        max_tokens: Limite total de tokens.
        core_pct: Percentual para core context.
        auxiliary_pct: Percentual para contexto auxiliar.
        historical_pct: Percentual para histórico.
        metadata_pct: Percentual para metadados.
    """
    max_tokens: int = 8000
    core_pct: float = 0.30
    auxiliary_pct: float = 0.40
    historical_pct: float = 0.20
    metadata_pct: float = 0.10

    # Limites de blocos por categoria
    cat_min_blocks: dict[str, int] = field(default_factory=lambda: {
        "core": 1,
        "auxiliary": 0,
        "historical": 0,
        "metadata": 0,
    })
    cat_max_blocks: dict[str, int] = field(default_factory=lambda: {
        "core": 5,
        "auxiliary": 8,
        "historical": 5,
        "metadata": 3,
    })
    cat_max_tokens_per_block: dict[str, int] = field(default_factory=lambda: {
        "core": 1500,
        "auxiliary": 800,
        "historical": 600,
        "metadata": 400,
    })

    @classmethod
    def from_agent_profile(cls, profile_name: str = "task_agent") -> "TokenBudget":
        """Cria um TokenBudget a partir de um perfil de agente."""
        profile = AGENT_BUDGET_PROFILES.get(profile_name, AGENT_BUDGET_PROFILES["task_agent"])
        return cls(
            max_tokens=profile.get("max_tokens", 8000),
            core_pct=profile.get("core", 0.30),
            auxiliary_pct=profile.get("auxiliary", 0.40),
            historical_pct=profile.get("historical", 0.20),
            metadata_pct=profile.get("metadata", 0.10),
        )

    @property
    def tokens_per_category(self) -> dict[str, int]:
        """Retorna tokens alocados por categoria."""
        return {
            "core": int(self.max_tokens * self.core_pct),
            "auxiliary": int(self.max_tokens * self.auxiliary_pct),
            "historical": int(self.max_tokens * self.historical_pct),
            "metadata": int(self.max_tokens * self.metadata_pct),
        }

    def fits(self, category: str, tokens: int) -> bool:
        """Verifica se um bloco cabe em determinada categoria."""
        allocated = self.tokens_per_category.get(category, 0)
        # Verificação simplificada — sem tracking de uso acumulado
        return tokens <= allocated


# ──────────────────────────────────────────────
# InclusionCriteria
# ──────────────────────────────────────────────


class InclusionCriteria:
    """Critérios de inclusão de nós no contexto do agente.

    Avalia se um nó ou aresta deve entrar com base em relevância,
    profundidade, peso de aresta e temporalidade.
    """

    @staticmethod
    def should_include_anchor(urn: str, kg: Any) -> bool:
        """Verifica se a URN âncora pode ser incluída no contexto."""
        from apos.core.graph import KnowledgeGraph
        if not isinstance(kg, KnowledgeGraph):
            return False
        node = kg.get_node(urn)
        if node is None:
            return False
        if node.attributes.get("status") == "archived":
            return False
        return True

    @staticmethod
    def should_include_neighbor(
        edge_weight: float,
        depth: int,
        anchor_urn: str,
        node_type: str,
    ) -> bool:
        """Decide se um nó vizinho deve ser incluído."""
        if depth == 0:
            return True
        if depth == 1 and edge_weight >= 0.3:
            return True
        if depth == 2 and edge_weight >= 0.5:
            return True
        if depth >= 3 and node_type == "blocker":
            return True
        return False

    @staticmethod
    def is_fresh_enough(
        updated_at: str,
        node_type: str,
        now: Optional[datetime] = None,
    ) -> tuple[bool, str]:
        """Verifica se o nó é recente o suficiente para entrar no contexto.

        Returns:
            (included: bool, reason: str)
        """
        if now is None:
            now = datetime.now(timezone.utc)
        try:
            age_hours = (now - datetime.fromisoformat(updated_at)).total_seconds() / 3600
        except (ValueError, TypeError):
            return False, "invalid_date"

        window = FRESHNESS_WINDOWS.get(node_type, 72)

        if age_hours <= 24:
            return True, "fresh"
        if age_hours <= window:
            return True, "aging"
        return False, f"expired (age={age_hours:.1f}h > window={window}h)"


# ──────────────────────────────────────────────
# ExclusionRules
# ──────────────────────────────────────────────


class ExclusionRules:
    """Regras de exclusão: o que NUNCA entra no contexto.

    Engloba dados sensíveis, TTL expirado, baixa relevância,
    nós órfãos, arquivados e isolamento de ambiente.
    """

    @staticmethod
    def is_sensitive(attributes: dict) -> bool:
        """Verifica se atributos contêm dados sensíveis."""
        blocked_lower = {f.lower() for f in PRIVACY_BARRIERS["blocked_fields"]}
        patterns = [re.compile(p) for p in PRIVACY_BARRIERS["blocked_patterns"]]

        for key, value in attributes.items():
            if key.lower() in blocked_lower:
                return True
            if isinstance(value, str):
                for pattern in patterns:
                    if pattern.search(value):
                        return True
        return False

    @staticmethod
    def is_ttl_expired(
        freshness: str,
        ttl_hours: int,
        now: Optional[datetime] = None,
    ) -> bool:
        """Verifica se o TTL de um bloco expirou."""
        if now is None:
            now = datetime.now(timezone.utc)
        try:
            age_hours = (now - datetime.fromisoformat(freshness)).total_seconds() / 3600
        except (ValueError, TypeError):
            return False
        return age_hours > ttl_hours

    @staticmethod
    def is_low_relevance(relevance_score: float) -> bool:
        """Verifica se a relevância está abaixo do mínimo."""
        return relevance_score < RELEVANCE_THRESHOLDS["exclude_default"]

    @staticmethod
    def is_orphan(node: Any, kg: Any) -> bool:
        """Verifica se um nó é órfão (sem conexões obrigatórias)."""
        from apos.core.graph import KnowledgeGraph
        from apos.core.types import NodeType

        if not isinstance(kg, KnowledgeGraph):
            return False
        if not hasattr(node, "type"):
            return False

        if node.type == NodeType.TASK:
            from apos.core.types import EdgeType
            return not kg._get_outbound(node.id, EdgeType.CONTRIBUI_PARA)
        elif node.type == NodeType.FEATURE:
            from apos.core.types import EdgeType
            return not kg._get_outbound(node.id, EdgeType.PARTE_DE)
        return False

    @staticmethod
    def is_environment_mismatch(
        block_env: Optional[str],
        agent_env: str,
    ) -> bool:
        """Verifica se há mismatch de ambiente entre bloco e agente."""
        if block_env is None:
            return False
        if agent_env == "production" and block_env in ("dev", "staging"):
            return True
        return False


# ──────────────────────────────────────────────
# Sanitização
# ──────────────────────────────────────────────


def sanitize_attributes(attributes: dict) -> dict:
    """Remove campos sensíveis dos atributos antes de montar o bloco.

    Args:
        attributes: Atributos originais do nó.

    Returns:
        Atributos sanitizados.
    """
    blocked_lower = {f.lower() for f in PRIVACY_BARRIERS["blocked_fields"]}
    compiled_patterns = [re.compile(p) for p in PRIVACY_BARRIERS["blocked_patterns"]]

    sanitized = {}
    for key, value in attributes.items():
        if key.lower() in blocked_lower:
            continue
        if isinstance(value, str):
            if any(p.search(value) for p in compiled_patterns):
                continue
        sanitized[key] = value
    return sanitized


def validate_context_isolation(
    agent_id: str,
    blocks: list[Any],
    environment: str,
) -> list[Any]:
    """Remove blocos que violam o isolamento do agente/ambiente.

    Args:
        agent_id: ID do agente.
        blocks: Lista de blocos (ContextBlock ou similar com .metadata).
        environment: Ambiente atual (``"production"``, ``"dev"``).

    Returns:
        Lista filtrada de blocos.
    """
    validated = []
    for block in blocks:
        block_env = block.metadata.get("environment", environment)
        if block_env != environment:
            continue
        block_agent = block.metadata.get("agent_id")
        if block_agent and block_agent != agent_id:
            continue
        validated.append(block)
    return validated


# ──────────────────────────────────────────────
# ContextBoundaries (Orquestrador)
# ──────────────────────────────────────────────


class ContextBoundaries:
    """Orquestrador de fronteiras de contexto.

    Aplica todas as regras de inclusão, exclusão, budget,
    sanitização e isolamento em uma única chamada.
    """

    def __init__(self, budget: Optional[TokenBudget] = None) -> None:
        self.budget = budget or TokenBudget()
        self.inclusion = InclusionCriteria()
        self.exclusion = ExclusionRules()

    def apply(
        self,
        results: list[Any],
        max_tokens: Optional[int] = None,
        agent_id: Optional[str] = None,
        environment: str = "production",
    ) -> list[Any]:
        """Aplica todas as regras de fronteira a uma lista de resultados.

        Args:
            results: Resultados ranqueados (RankedResult ou dicts).
            max_tokens: Limite de tokens (opcional, usa do budget se None).
            agent_id: ID do agente para isolamento (opcional).
            environment: Ambiente para isolamento.

        Returns:
            Lista filtrada de resultados.
        """
        if max_tokens is not None:
            self.budget.max_tokens = max_tokens

        filtered = []

        for result in results:
            # Extrai dados do resultado (suporta RankedResult ou dict)
            if hasattr(result, "data"):
                data = result.data
            elif isinstance(result, dict):
                data = result
            else:
                data = {}

            attrs = data.get("attributes", {})
            node_type = data.get("type", "unknown")

            # 1. Exclusão por tipo bloqueado
            if node_type in PRIVACY_BARRIERS["blocked_node_types"]:
                continue

            # 2. Exclusão por dados sensíveis
            if self.exclusion.is_sensitive(attrs):
                continue

            # 3. Sanitização
            if attrs:
                data["attributes"] = sanitize_attributes(attrs)

            # 4. Isolamento por ambiente
            meta = data.get("metadata", {})
            block_env = meta.get("environment", environment)
            if self.exclusion.is_environment_mismatch(block_env, environment):
                continue

            # 5. Isolamento por agente
            block_agent = meta.get("agent_id")
            if block_agent and agent_id and block_agent != agent_id:
                continue

            # 6. Check de budget por tipo de nó
            node_config = NODE_TOKEN_LIMITS.get(node_type, {})
            max_tok = node_config.get("max_tokens", 500)

            # Estima tamanho em tokens (aproximação)
            text_size = len(json.dumps(data.get("attributes", {}))) // 4
            if text_size > max_tok:
                # Se compressível, permitimos (compressão acontece depois)
                if not node_config.get("compressible", True):
                    continue

            filtered.append(result)

        return filtered
