"""
APOS Knowledge Graph — Tipos Base (Camada 3)

Define os tipos fundamentais do grafo de conhecimento:
Node, Edge, enums NodeType/EdgeType, metadados, e helpers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ──────────────────────────────────────────────
# NodeType (Enum)
# ──────────────────────────────────────────────

class NodeType(Enum):
    """Tipos ontológicos de nó no Knowledge Graph do APOS."""
    TASK = "task"
    FEATURE = "feature"
    RELEASE = "release"
    OKR = "okr"
    METRIC = "metric"
    SPRINT = "sprint"
    PERSONA = "persona"

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# EdgeType (Enum)
# ──────────────────────────────────────────────

class EdgeType(Enum):
    """Tipos ontológicos de aresta no Knowledge Graph do APOS."""
    CONTRIBUI_PARA = "contribui_para"   # Task → Feature
    PARTE_DE = "parte_de"               # Feature → Release, Sprint → Release
    ALCANCA = "alcanca"                 # Release → OKR
    MEDIDO_POR = "medido_por"           # OKR → Metric
    IMPACTA = "impacta"                 # Task → Metric
    BLOQUEIA = "bloqueia"               # Task → Task
    DEPENDE_DE = "depende_de"           # Task → Task
    PERTENCE_A = "pertence_a"           # Task → Sprint
    ENVOLVE = "envolve"                 # Feature → Persona, Release → Persona
    ATINGE = "atinge"                   # Metric → Metric

    def __str__(self) -> str:
        return self.value


# ──────────────────────────────────────────────
# NodeMetadata
# ──────────────────────────────────────────────

@dataclass
class NodeMetadata:
    """Metadados estruturais de um nó.

    Attributes:
        created_at: ISO 8601 — data de criação do nó no grafo.
        updated_at: ISO 8601 — data da última modificação.
        version: Número de versão incremental (1-based).
        source: Fonte original (ex: "jira:PROJ-456") — opcional.
        description: Descrição legível — opcional.
    """
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    version: int = 1
    source: Optional[str] = None
    description: Optional[str] = None


# ──────────────────────────────────────────────
# Node
# ──────────────────────────────────────────────

@dataclass
class Node:
    """Unidade fundamental do Knowledge Graph.

    Attributes:
        id: URN única no formato ``urn:apos:{type}:{local_id}``.
        type: Tipo ontológico do nó.
        attributes: Atributos específicos do tipo (snake_case).
        metadata: Metadados estruturais do nó.
    """
    id: str  # URN
    type: NodeType
    attributes: dict = field(default_factory=dict)
    metadata: NodeMetadata = field(default_factory=lambda: NodeMetadata(
        created_at="", updated_at=""
    ))


# ──────────────────────────────────────────────
# EdgeMetadata
# ──────────────────────────────────────────────

@dataclass
class EdgeMetadata:
    """Metadados estruturais de uma aresta.

    Attributes:
        created_at: ISO 8601 — data de criação.
        updated_at: ISO 8601 — data da última modificação.
        version: Versão incremental (1-based).
        confidence: Confiança na relação [0.0, 1.0] (default: 1.0).
        reason: Razão contextual — opcional.
    """
    created_at: str  # ISO 8601
    updated_at: str  # ISO 8601
    version: int = 1
    confidence: float = 1.0  # [0.0, 1.0]
    reason: Optional[str] = None


# ──────────────────────────────────────────────
# Edge
# ──────────────────────────────────────────────

@dataclass
class Edge:
    """Relação direcionada entre dois Nodes.

    Attributes:
        source: URN do nó de origem.
        target: URN do nó de destino.
        type: Tipo ontológico da relação.
        weight: Peso da relação [0.0, 1.0] (padrão: 1.0).
        metadata: Metadados estruturais da aresta.
    """
    source: str  # URN
    target: str  # URN
    type: EdgeType
    weight: float = 1.0  # [0.0, 1.0]
    metadata: EdgeMetadata = field(default_factory=lambda: EdgeMetadata(
        created_at="", updated_at=""
    ))


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

# Padrão de caracteres permitidos para local_id URN
_LOCAL_ID_PATTERN = re.compile(r"^[a-z0-9\-]+$")


def make_urn(entity_type: str, local_id: str) -> str:
    """Cria uma URN no padrão APOS.

    Normaliza o ``local_id`` para lowercase-kebab-case e valida os
    caracteres permitidos (``[a-z0-9-]``).

    Args:
        entity_type: Tipo da entidade (ex: ``"task"``, ``"feature"``).
        local_id: Identificador local (será normalizado).

    Returns:
        URN no formato ``urn:apos:{entity_type}:{local_id}``.

    Examples:
        >>> make_urn("task", "OAuth login")
        'urn:apos:task:oauth-login'
        >>> make_urn("feature", "Faster Auth")
        'urn:apos:feature:faster-auth'
    """
    # Normaliza: lowercase, substitui underscores e espaços por hífens
    normalized = local_id.lower().replace("_", "-").replace(" ", "-")
    # Remove caracteres não permitidos
    normalized = re.sub(r"[^a-z0-9\-]", "", normalized)
    # Elimina hífens duplicados e nas bordas
    normalized = re.sub(r"-+", "-", normalized).strip("-")
    return f"urn:apos:{entity_type}:{normalized}"


def parse_urn(urn: str) -> Optional[tuple[str, str]]:
    """Analisa uma URN APOS e retorna (entity_type, local_id).

    Args:
        urn: URN no formato ``urn:apos:{type}:{local_id}``.

    Returns:
        Tupla ``(entity_type, local_id)`` ou ``None`` se inválida.
    """
    parts = urn.split(":", 3)
    if len(parts) == 4 and parts[0] == "urn" and parts[1] == "apos":
        return parts[2], parts[3]
    return None


def is_valid_urn(urn: str) -> bool:
    """Verifica se uma string é uma URN APOS válida.

    Args:
        urn: String a ser validada.

    Returns:
        ``True`` se a URN segue o padrão ``urn:apos:{type}:{local_id}``.
    """
    return parse_urn(urn) is not None
