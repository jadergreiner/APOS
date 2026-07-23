"""
APOS Context Model — Pipeline de Contexto para Agentes (Camada 3.5)

Transforma dados do Knowledge Graph em contexto consumível por agentes
de IA através de 4 etapas: extração → montagem → injeção → cleanup.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional

from apos.core.graph import KnowledgeGraph
from apos.core.types import EdgeType, Node, NodeType


# ──────────────────────────────────────────────
# ContextBlock
# ──────────────────────────────────────────────


@dataclass
class ContextBlock:
    """Unidade autônoma de informação gerada a partir de um nó do grafo.

    Attributes:
        source: URN do nó que originou este bloco.
        type: Tipo do nó (task, feature, release, okr, metric, sprint, persona).
        relevance: Score de relevância [0.0, 1.0].
        content: Atributos do nó formatados para consumo do agente.
        metadata: Metadados (freshness, TTL, versão, profundidade, edge_type, etc.).
    """
    source: str
    type: str
    relevance: float = 0.0
    content: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=lambda: {
        "freshness": "",
        "ttl_hours": 24,
        "version": 1,
        "depth": 0,
    })

    def estimate_tokens(self) -> int:
        """Estima o número de tokens deste bloco.

        Regra aproximada: 1 token ≈ 4 caracteres, mais overhead fixo.
        """
        text = json.dumps(self.content, ensure_ascii=False)
        return len(text) // 4 + 20

    def render(self, fmt: str = "markdown") -> str:
        """Renderiza o bloco em formato texto.

        Args:
            fmt: Formato de saída: ``"markdown"``, ``"json"``, ou ``"template"``.

        Returns:
            String formatada do bloco.
        """
        if fmt == "markdown":
            return self._to_markdown()
        elif fmt == "json":
            return self._to_json()
        return self._to_markdown()

    def compress(self) -> "ContextBlock":
        """Comprime o bloco mantendo apenas campos essenciais.

        Remove campos como description, acceptance_criteria, tags e
        adiciona flags de compressão nos metadados.
        """
        essential_keys = {
            "title", "name", "objective", "status",
            "current_value", "target", "version",
            "priority", "story_points", "owner",
            "completeness", "unit", "goal",
        }
        compressed = {
            k: v for k, v in self.content.items()
            if k in essential_keys
        }
        fields_removed = len(self.content) - len(compressed)
        compressed["_compressed"] = True
        if fields_removed > 0:
            compressed["_fields_removed"] = fields_removed
        return ContextBlock(
            source=self.source,
            type=self.type,
            relevance=self.relevance,
            content=compressed,
            metadata={**self.metadata, "compressed": True},
        )

    def _to_markdown(self) -> str:
        """Renderiza como Markdown."""
        lines = [
            f"**{self.type.upper()}:** `{self.source}`",
            f"  - Relevância: {self.relevance:.2f}",
        ]
        for key, value in self.content.items():
            lines.append(f"  - {key}: {value}")
        lines.append(f"  - Atualizado em: {self.metadata.get('freshness', 'N/A')}")
        return "\n".join(lines)

    def _to_json(self) -> str:
        """Renderiza como JSON."""
        return json.dumps({
            "source": self.source,
            "type": self.type,
            "relevance": self.relevance,
            "content": self.content,
            "metadata": self.metadata,
        }, ensure_ascii=False, indent=2)


# ──────────────────────────────────────────────
# Constantes de Relevância
# ──────────────────────────────────────────────

PRIORITY_TIERS: dict[str, tuple[float, float]] = {
    "critical": (0.8, 1.0),
    "high": (0.5, 0.79),
    "normal": (0.0, 0.49),
}

TOKEN_LIMITS: dict[str, float] = {
    "critical": 0.50,
    "high": 0.35,
    "normal": 0.15,
}

CORE_CONTEXT_URNS: dict[str, int] = {
    "min_always": 1,
    "min_blockers": 5,
    "min_alerts": 3,
}


# ──────────────────────────────────────────────
# Cálculo de Relevância
# ──────────────────────────────────────────────


def calculate_relevance(
    block: ContextBlock,
    anchor_urn: str,
    freshness: str,
    weight_distance: float = 0.35,
    weight_confidence: float = 0.25,
    weight_freshness: float = 0.25,
    weight_recency: float = 0.15,
) -> float:
    """Calcula o score de relevância de um bloco de contexto.

    Args:
        block: Bloco de contexto a avaliar.
        anchor_urn: URN do nó âncora.
        freshness: ISO 8601 da última atualização.
        weight_*: Pesos de cada fator (devem somar 1.0).

    Returns:
        Float entre 0.0 e 1.0.
    """
    # O próprio nó âncora sempre recebe relevância máxima, independente
    # dos demais fatores (confiança, frescor, recência).
    if block.source == anchor_urn:
        return 1.0

    now = datetime.now(timezone.utc)

    # 1. Score de Distância (quão perto do âncora)
    depth = block.metadata.get("depth", 99)
    if depth == 0:
        distance_score = 1.0
    elif depth == 1:
        distance_score = 0.8
    elif depth == 2:
        distance_score = 0.5
    else:
        distance_score = 0.2

    # 2. Score de Confiança (pesos das arestas no caminho)
    edge_weight = block.metadata.get("edge_weight", 0.5)
    confidence_score = edge_weight

    # 3. Score de Frescor (quão recente é a atualização)
    try:
        updated = datetime.fromisoformat(freshness)
        age_hours = (now - updated).total_seconds() / 3600
        if age_hours <= 1:
            freshness_score = 1.0
        elif age_hours <= 24:
            freshness_score = 0.9 - (age_hours - 1) * (0.4 / 23)
        elif age_hours <= 72:
            freshness_score = 0.5 - (age_hours - 24) * (0.3 / 48)
        else:
            freshness_score = 0.1
    except (ValueError, TypeError):
        freshness_score = 0.5

    # 4. Score de Recência (frequência de acesso/blocos similares)
    recency_score = block.metadata.get("recency_boost", 0.5)

    relevance = (
        weight_distance * distance_score
        + weight_confidence * confidence_score
        + weight_freshness * freshness_score
        + weight_recency * recency_score
    )

    return round(min(max(relevance, 0.0), 1.0), 4)


# ──────────────────────────────────────────────
# Template de Contexto
# ──────────────────────────────────────────────

CONTEXT_TEMPLATE = """\
## Contexto do Grafo APOS

### Nó Âncora
{anchor_block}

### Relações Diretas
{direct_blocks}

### Relações Indiretas
{indirect_blocks}

### Trust Score do Grafo
{trust_summary}"""


# ──────────────────────────────────────────────
# Funções de Extração / Montagem / Injeção / Cleanup
# ──────────────────────────────────────────────


def extract_context(
    anchor_urn: str,
    depth: int = 2,
    kg: Optional[KnowledgeGraph] = None,
) -> list[dict]:
    """Extrai contexto do KG a partir de uma URN âncora.

    Percorre o grafo radialmente até a profundidade especificada,
    coletando nós e arestas conectados.

    Args:
        anchor_urn: URN do nó central do contexto.
        depth: Profundidade máxima de expansão (padrão: 2 saltos).
        kg: Instância do Knowledge Graph.

    Returns:
        Lista de dicts brutos com {urn, type, attributes, edges}.
    """
    if kg is None:
        return []

    raw_nodes: dict[str, dict] = {}
    visited: set[str] = set()
    queue: list[tuple[str, int]] = [(anchor_urn, 0)]

    while queue:
        current_urn, current_depth = queue.pop(0)
        if current_urn in visited or current_depth > depth:
            continue
        visited.add(current_urn)

        node = kg.get_node(current_urn)
        if node is None:
            continue

        out_edges = kg._get_outbound(current_urn)
        in_edges = kg._get_inbound(current_urn)

        raw_nodes[current_urn] = {
            "urn": current_urn,
            "type": node.type.value,
            "attributes": node.attributes,
            "metadata": {
                "created_at": node.metadata.created_at,
                "updated_at": node.metadata.updated_at,
                "version": node.metadata.version,
            },
            "out_edges": [
                {"target": e.target, "type": e.type.value, "weight": e.weight}
                for e in out_edges
            ],
            "in_edges": [
                {"source": e.source, "type": e.type.value, "weight": e.weight}
                for e in in_edges
            ],
        }

        if current_depth < depth:
            for e in out_edges:
                if e.target not in visited:
                    queue.append((e.target, current_depth + 1))
            for e in in_edges:
                if e.source not in visited:
                    queue.append((e.source, current_depth + 1))

    return list(raw_nodes.values())


def format_node_content(node_data: dict) -> dict:
    """Formata atributos de um nó para consumo do agente."""
    return dict(node_data.get("attributes", {}))


def assemble_context(
    raw_nodes: list[dict],
    anchor_urn: str,
) -> list[ContextBlock]:
    """Monta blocos de contexto a partir de dados brutos do KG.

    Args:
        raw_nodes: Lista de nós extraídos (formato da Etapa 1).
        anchor_urn: URN do nó âncora para ordenação.

    Returns:
        Lista de ContextBlock ordenados por relevância.
    """
    blocks: list[ContextBlock] = []

    for node_data in raw_nodes:
        block = ContextBlock(
            source=node_data["urn"],
            type=node_data["type"],
            content=format_node_content(node_data),
            metadata={
                "freshness": node_data["metadata"]["updated_at"],
                "version": node_data["metadata"]["version"],
            },
        )
        blocks.append(block)

    now = datetime.now(timezone.utc).isoformat()

    for block in blocks:
        score = calculate_relevance(
            block=block,
            anchor_urn=anchor_urn,
            freshness=block.metadata.get("freshness", now),
        )
        block.relevance = score

    blocks.sort(key=lambda b: b.relevance, reverse=True)
    return blocks


def inject_context(
    blocks: list[ContextBlock],
    template: str = CONTEXT_TEMPLATE,
    _get_trust_summary_fallback: Optional[str] = None,
) -> str:
    """Injeta blocos de contexto no prompt usando um template.

    Args:
        blocks: Lista ordenada de blocos de contexto.
        template: Template string com placeholders.
        _get_trust_summary_fallback: Fallback para resumo de trust score.

    Returns:
        String do contexto renderizado.
    """
    anchor = blocks[0] if blocks else None
    direct = [b for b in blocks[1:] if b.relevance >= 0.7]
    indirect = [b for b in blocks[1:] if 0.4 <= b.relevance < 0.7]

    return template.format(
        anchor_block=anchor.render() if anchor else "N/A",
        direct_blocks="\n".join(b.render() for b in direct) if direct else "Nenhuma",
        indirect_blocks="\n".join(b.render() for b in indirect) if indirect else "Nenhuma",
        trust_summary=_get_trust_summary_fallback or "N/A",
    )


def cleanup_context(
    blocks: list[ContextBlock],
    max_tokens: int = 8000,
    block_max_tokens: int = 1500,
) -> list[ContextBlock]:
    """Limpa e otimiza a lista de blocos para caber na janela de contexto.

    Aplica expurgo por TTL, deduplicação, podagem e compressão.

    Args:
        blocks: Lista ordenada de blocos.
        max_tokens: Limite total de tokens permitido.
        block_max_tokens: Limite de tokens por bloco individual.

    Returns:
        Lista filtrada e comprimida de blocos.
    """
    now = datetime.now(timezone.utc)

    # 1. Expurgo por TTL
    valid = []
    for b in blocks:
        ttl = b.metadata.get("ttl_hours")
        freshness = b.metadata.get("freshness")
        if ttl is not None and freshness:
            try:
                age_hours = (
                    now - datetime.fromisoformat(freshness)
                ).total_seconds() / 3600
                if age_hours > ttl:
                    continue
            except (ValueError, TypeError):
                pass
        valid.append(b)

    # 2. Deduplicação (mantém o mais recente/maior relevância)
    seen: dict[str, ContextBlock] = {}
    for b in valid:
        if b.source not in seen:
            seen[b.source] = b
        elif b.relevance > seen[b.source].relevance:
            seen[b.source] = b
    deduped = list(seen.values())

    # 3. Ordena por relevância (decrescente)
    deduped.sort(key=lambda b: b.relevance, reverse=True)

    # 4. Podagem — remove blocos de baixa relevância até caber
    token_count = sum(b.estimate_tokens() for b in deduped)
    while token_count > max_tokens and len(deduped) > 1:
        removed = deduped.pop()
        token_count = sum(b.estimate_tokens() for b in deduped)
        _ = removed  # bloco descartado

    # 5. Compressão de blocos muito grandes
    for i, b in enumerate(deduped):
        if b.estimate_tokens() > block_max_tokens:
            deduped[i] = b.compress()

    return deduped


def get_core_context(
    anchor_urn: str,
    kg: Optional[KnowledgeGraph] = None,
) -> list[ContextBlock]:
    """Retorna o core context mínimo que sempre deve ser injetado.

    Args:
        anchor_urn: URN do nó âncora.
        kg: Instância do Knowledge Graph.

    Returns:
        Lista de blocos de core context.
    """
    if kg is None:
        return []

    core: list[ContextBlock] = []

    # 1. Nó âncora
    anchor_node = kg.get_node(anchor_urn)
    if anchor_node:
        core.append(ContextBlock(
            source=anchor_urn,
            type=anchor_node.type.value,
            relevance=1.0,
            content=anchor_node.attributes,
            metadata={
                "freshness": anchor_node.metadata.updated_at,
                "depth": 0,
                "ttl_hours": 24,
            },
        ))

    # 2. Bloqueios incoming
    blockers = kg._get_inbound(anchor_urn, EdgeType.BLOQUEIA)
    for edge in blockers[:CORE_CONTEXT_URNS["min_blockers"]]:
        blocker_node = kg.get_node(edge.source)
        if blocker_node:
            core.append(ContextBlock(
                source=edge.source,
                type="task",
                relevance=0.95,
                content=blocker_node.attributes,
                metadata={
                    "freshness": blocker_node.metadata.updated_at,
                    "depth": 1,
                    "ttl_hours": 12,
                },
            ))

    # 3. Nós com status crítico
    for edge in kg._get_outbound(anchor_urn):
        target = kg.get_node(edge.target)
        if target and target.attributes.get("status") in ("critical", "at_risk"):
            core.append(ContextBlock(
                source=target.id,
                type=target.type.value,
                relevance=0.9,
                content=target.attributes,
                metadata={
                    "freshness": target.metadata.updated_at,
                    "depth": 1,
                    "ttl_hours": 12,
                },
            ))

    return core


def fallback_strategy(
    core: list[ContextBlock],
    max_tokens: int,
) -> tuple[list[ContextBlock], str]:
    """Estratégia de fallback quando o core context não cabe na janela.

    Returns:
        (blocos_reduzidos, modo_operação) onde modo pode ser:
        "full", "compressed", "summary_only", ou "urns_only".
    """
    total_tokens = sum(b.estimate_tokens() for b in core)

    if total_tokens <= max_tokens:
        return core, "full"

    # Modo 1: Compressão máxima de todos os blocos
    # Um bloco só é considerado "comprimido" com sucesso se ainda retiver
    # alguma informação de fato (não apenas as flags de metadados) — caso
    # contrário a "compressão" apenas descartou o conteúdo, o que não é
    # uma redução válida e deve escalar para o próximo modo de fallback.
    compressed = [b.compress() for b in core]
    compressed_tokens = sum(b.estimate_tokens() for b in compressed)
    compressed_has_content = all(
        any(not k.startswith("_") for k in b.content) for b in compressed
    )
    if compressed_tokens <= max_tokens and compressed_has_content:
        return compressed, "compressed"

    # Modo 2: Apenas sumário
    # Da mesma forma, o sumário só é útil se o bloco original de fato tinha
    # um campo "status" — caso contrário o valor "unknown" é apenas um
    # placeholder vazio, sem informação real para o agente.
    summary = []
    summary_has_content = True
    for b in core:
        if "status" not in b.content:
            summary_has_content = False
        summary_block = ContextBlock(
            source=b.source,
            type=b.type,
            relevance=b.relevance,
            content={
                "status": b.content.get("status", "unknown"),
                "_summary_only": True,
            },
            metadata={**b.metadata, "summary_mode": True},
        )
        summary.append(summary_block)
    summary_tokens = sum(b.estimate_tokens() for b in summary)
    if summary_tokens <= max_tokens and summary_has_content:
        return summary, "summary_only"

    # Modo 3: Apenas URNs
    urn_list = [b.source for b in core[:5]]
    return [
        ContextBlock(
            source="fallback",
            type="urn_list",
            relevance=0.0,
            content={
                "urns": urn_list,
                "message": "Contexto excedeu limite de tokens — carregue URNs sob demanda",
            },
            metadata={"fallback": True},
        )
    ], "urns_only"


# ──────────────────────────────────────────────
# ContextPipeline
# ──────────────────────────────────────────────


class ContextPipeline:
    """Pipeline completo de transformação do KG em contexto para agentes.

    O pipeline executa 4 etapas:
    1. **Extração**: consulta o KG para obter nós e arestas relevantes.
    2. **Montagem**: transforma nós em ContextBlocks com score de relevância.
    3. **Injeção**: renderiza contexto no formato alvo (markdown, json, template).
    4. **Cleanup**: aplica TTL, pruning, compressão e deduplicação.

    Args:
        kg: Instância do Knowledge Graph (opcional, pode ser injetada depois).
    """

    def __init__(self, kg: Optional[KnowledgeGraph] = None) -> None:
        self._kg = kg

    @property
    def kg(self) -> Optional[KnowledgeGraph]:
        """Knowledge Graph associado ao pipeline."""
        return self._kg

    @kg.setter
    def kg(self, value: KnowledgeGraph) -> None:
        self._kg = value

    def run(
        self,
        anchor_urn: str,
        depth: int = 2,
        max_tokens: int = 8000,
        output_format: str = "markdown",
    ) -> str:
        """Executa o pipeline completo e retorna contexto renderizado.

        Args:
            anchor_urn: URN do nó âncora.
            depth: Profundidade máxima de expansão.
            max_tokens: Limite de tokens para o contexto final.
            output_format: Formato de saída (``"markdown"``, ``"json"``).

        Returns:
            Contexto renderizado como string.
        """
        # 1. Extração
        raw = extract_context(anchor_urn, depth=depth, kg=self._kg)

        # 2. Montagem
        blocks = assemble_context(raw, anchor_urn)

        # 3. Cleanup (antes da injeção para garantir limites)
        blocks = cleanup_context(blocks, max_tokens=max_tokens)

        # 4. Injeção
        if output_format == "json":
            return json.dumps(
                [b._to_json() for b in blocks],
                ensure_ascii=False,
                indent=2,
            )
        # Markdown com separadores
        parts = [
            f"# Contexto APOS — Âncora: {anchor_urn}\n",
        ]
        for b in blocks:
            parts.append(b.render(fmt=output_format))
            parts.append("---")
        return "\n".join(parts)
