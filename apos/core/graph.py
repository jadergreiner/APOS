"""
APOS Knowledge Graph — Grafo de Conhecimento em Memória (Camada 3)

Implementa o ``KnowledgeGraph``, um grafo de conhecimento em memória com
nós e arestas tipados, navegação multi-edge, inferência de impacto,
detecção de nós órfãos, e serialização JSON.
"""

from __future__ import annotations

import copy
from typing import Any, Optional

from apos.core.types import (
    Edge,
    EdgeMetadata,
    EdgeType,
    Node,
    NodeMetadata,
    NodeType,
    make_urn,
    parse_urn,
)

# ──────────────────────────────────────────────
# Matriz de Validação KG-002
# Source NodeType → dict[EdgeType, set[NodeType]]
# ──────────────────────────────────────────────

_VALID_EDGE_MATRIX: dict[NodeType, dict[EdgeType, set[NodeType]]] = {
    NodeType.TASK: {
        EdgeType.CONTRIBUI_PARA: {NodeType.FEATURE},
        EdgeType.IMPACTA: {NodeType.METRIC},
        EdgeType.BLOQUEIA: {NodeType.TASK},
        EdgeType.DEPENDE_DE: {NodeType.TASK},
        EdgeType.PERTENCE_A: {NodeType.SPRINT},
    },
    NodeType.FEATURE: {
        EdgeType.PARTE_DE: {NodeType.RELEASE},
        EdgeType.ENVOLVE: {NodeType.PERSONA},
    },
    NodeType.RELEASE: {
        EdgeType.ALCANCA: {NodeType.OKR},
        EdgeType.ENVOLVE: {NodeType.PERSONA},
    },
    NodeType.OKR: {
        EdgeType.MEDIDO_POR: {NodeType.METRIC},
    },
    NodeType.METRIC: {
        EdgeType.ATINGE: {NodeType.METRIC},
    },
    NodeType.SPRINT: {
        EdgeType.PARTE_DE: {NodeType.RELEASE},
    },
    NodeType.PERSONA: {},
}


def _validate_edge_type(source_type: NodeType, edge_type: EdgeType, target_type: NodeType) -> None:
    """Valida KG-002: tipo de aresta é válido para o par source/target."""
    allowed_targets = _VALID_EDGE_MATRIX.get(source_type, {}).get(edge_type, set())
    if target_type not in allowed_targets:
        raise ValueError(
            f"KG-002: EdgeType '{edge_type.value}' não é válido para "
            f"source={source_type.value} → target={target_type.value}"
        )


# ──────────────────────────────────────────────
# KnowledgeGraph
# ──────────────────────────────────────────────

class KnowledgeGraph:
    """Grafo de conhecimento em memória com nós e arestas tipados.

    Suporta CRUD de nós e arestas, navegação multi-edge, inferência de
    impacto, detecção de nós órfãos e serialização JSON.

    Attributes:
        node_count: Número de nós no grafo.
        edge_count: Número de arestas no grafo.
    """

    def __init__(self) -> None:
        # URN → Node
        self._nodes: dict[str, Node] = {}
        # Lista completa de arestas
        self._edges: list[Edge] = []
        # URN → lista de arestas (forward)
        self._adjacency: dict[str, list[Edge]] = {}
        # URN → lista de arestas (reverse)
        self._reverse_adj: dict[str, list[Edge]] = {}

    # ───────────────
    # Node CRUD
    # ───────────────

    def add_node(self, node: Node) -> None:
        """Adiciona um nó ao grafo.

        Args:
            node: Nó a ser adicionado.

        Raises:
            ValueError: Se a URN já existir (KG-001).
            ValueError: Se o tipo do nó não for um ``NodeType`` válido.

        KG-001: Unicidade de URN — REJECT se duplicada.
        """
        if not isinstance(node.type, NodeType):
            raise ValueError(f"Node.type inválido: {node.type}")

        if node.id in self._nodes:
            existing = self._nodes[node.id]
            raise ValueError(
                f"KG-001: Node com URN '{node.id}' já existe "
                f"(type={existing.type.value})"
            )

        self._nodes[node.id] = node
        self._adjacency.setdefault(node.id, [])
        self._reverse_adj.setdefault(node.id, [])

    def get_node(self, urn: str) -> Optional[Node]:
        """Retorna um nó pela URN.

        Args:
            urn: URN do nó.

        Returns:
            O nó, ou ``None`` se não encontrado.
        """
        return self._nodes.get(urn)

    def update_node(
        self,
        urn: str,
        attributes: Optional[dict] = None,
        metadata: Optional[dict] = None,
    ) -> bool:
        """Atualiza atributos e/ou metadados de um nó existente.

        Args:
            urn: URN do nó a atualizar.
            attributes: Dicionário com atributos a mesclar (opcional).
            metadata: Dicionário com campos de metadados a mesclar (opcional).

        Returns:
            ``True`` se o nó foi encontrado e atualizado, ``False`` caso contrário.
        """
        node = self._nodes.get(urn)
        if node is None:
            return False

        if attributes:
            node.attributes.update(attributes)

        if metadata:
            for key, value in metadata.items():
                if hasattr(node.metadata, key):
                    setattr(node.metadata, key, value)

        return True

    def remove_node(self, urn: str) -> bool:
        """Remove um nó e todas as arestas conectadas.

        Args:
            urn: URN do nó a remover.

        Returns:
            ``True`` se o nó foi removido, ``False`` se não existia.

        KG-011: Remove também todas as arestas conectadas.
        """
        if urn not in self._nodes:
            return False

        # Remove arestas que envolvem este nó
        self._edges = [
            e for e in self._edges
            if e.source != urn and e.target != urn
        ]

        # Remove das listas de adjacência
        self._adjacency.pop(urn, None)
        self._reverse_adj.pop(urn, None)

        # Remove entradas em adjacências de outros nós
        for adj_list in self._adjacency.values():
            adj_list[:] = [e for e in adj_list if e.source != urn and e.target != urn]
        for rev_list in self._reverse_adj.values():
            rev_list[:] = [e for e in rev_list if e.source != urn and e.target != urn]

        # Remove o nó
        del self._nodes[urn]
        return True

    # ───────────────
    # Edge CRUD
    # ───────────────

    def add_edge(self, edge: Edge) -> None:
        """Adiciona uma aresta ao grafo com validações completas.

        Valida:
        - KG-006/007: Source e Target existem.
        - KG-002: EdgeType é válido para o par source/target.
        - KG-012: weight está em [0.0, 1.0].
        - KG-008: Cardinalidade Task → Feature (N:1).

        Se uma aresta **exatamente idêntica** (mesmo source, target, type)
        já existir, seus ``weight`` e ``confidence`` são atualizados
        (merge em vez de duplicação).

        Args:
            edge: Aresta a ser adicionada.

        Raises:
            ValueError: Se alguma validação falhar.
        """
        # KG-006 / KG-007: integridade referencial
        if edge.source not in self._nodes:
            raise ValueError(
                f"KG-006: Edge.source '{edge.source}' não encontrado no grafo"
            )
        if edge.target not in self._nodes:
            raise ValueError(
                f"KG-007: Edge.target '{edge.target}' não encontrado no grafo"
            )

        # KG-012: peso
        if not (0.0 <= edge.weight <= 1.0):
            raise ValueError(
                f"KG-012: weight {edge.weight} fora do intervalo [0.0, 1.0]"
            )

        # KG-002: tipo de aresta válido
        source_type = self._nodes[edge.source].type
        target_type = self._nodes[edge.target].type
        _validate_edge_type(source_type, edge.type, target_type)

        # Merge se edge idêntica já existe (deve ser verificado ANTES das
        # regras de cardinalidade para permitir atualização de peso)
        for existing_edge in self._edges:
            if (existing_edge.source == edge.source
                    and existing_edge.target == edge.target
                    and existing_edge.type == edge.type):
                existing_edge.weight = edge.weight
                if edge.metadata.confidence is not None:
                    existing_edge.metadata.confidence = edge.metadata.confidence
                return

        # KG-008: cardinalidade Task → Feature (N:1)
        if edge.type == EdgeType.CONTRIBUI_PARA and source_type == NodeType.TASK:
            existing = self._get_outbound(edge.source, EdgeType.CONTRIBUI_PARA)
            if existing:
                raise ValueError(
                    f"KG-008: Task '{edge.source}' já contribui para "
                    f"Feature '{existing[0].target}'"
                )

        # KG-009: cardinalidade Feature → Release (N:1)
        if edge.type == EdgeType.PARTE_DE and source_type == NodeType.FEATURE:
            existing = self._get_outbound(edge.source, EdgeType.PARTE_DE)
            if existing:
                raise ValueError(
                    f"KG-009: Feature '{edge.source}' já pertence à "
                    f"Release '{existing[0].target}'"
                )

        self._edges.append(edge)
        self._adjacency.setdefault(edge.source, []).append(edge)
        self._reverse_adj.setdefault(edge.target, []).append(edge)

    def get_edges(self, urn: str) -> list[Edge]:
        """Retorna todas as arestas conectadas a um nó (entrada e saída).

        Args:
            urn: URN do nó.

        Returns:
            Lista de arestas conectadas ao nó.
        """
        return self._get_outbound(urn) + self._get_inbound(urn)

    def get_neighbors(
        self,
        urn: str,
        edge_type: Optional[EdgeType] = None,
    ) -> list[tuple[str, Edge]]:
        """Retorna vizinhos de um nó, opcionalmente filtrado por tipo de aresta.

        Args:
            urn: URN do nó.
            edge_type: Filtrar por tipo de aresta (opcional).

        Returns:
            Lista de ``(urn_vizinho, aresta)``.
        """
        neighbors: list[tuple[str, Edge]] = []
        for edge in self._get_outbound(urn):
            if edge_type is None or edge.type == edge_type:
                neighbors.append((edge.target, edge))
        return neighbors

    # ───────────────
    # Traversal
    # ───────────────

    def traverse(
        self,
        start_urn: str,
        path: list[EdgeType],
    ) -> list[tuple[str, list[Edge]]]:
        """Navegação multi-edge: percorre uma cadeia de tipos de aresta.

        A partir de ``start_urn``, segue cada ``EdgeType`` em ``path``
        sequencialmente, coletando os nós intermediários e as arestas
        percorridas em cada salto.

        Args:
            start_urn: URN do nó de partida.
            path: Lista de ``EdgeType`` a percorrer em ordem.

        Returns:
            Lista de ``(urn_intermediaria, [edges_percorridas])`` para cada etapa.
        """
        results: list[tuple[str, list[Edge]]] = []
        current_urns: list[str] = [start_urn]

        for edge_type in path:
            next_urns: list[str] = []
            all_edges: list[Edge] = []
            for urn in current_urns:
                for edge in self._get_outbound(urn, edge_type):
                    if edge.target not in next_urns:
                        next_urns.append(edge.target)
                    all_edges.append(edge)
            if not next_urns:
                break
            for target_urn in next_urns:
                hops = [e for e in all_edges if e.target == target_urn]
                results.append((target_urn, hops))
            current_urns = next_urns

        return results

    # ───────────────
    # Inferência de Impacto
    # ───────────────

    def infer_impact(self, start_urn: str) -> list[dict]:
        """Calcula impacto completo a partir de um nó.

        Percorre o grafo a partir de ``start_urn`` seguindo as cadeias de
        relação e encontra todos os nós que podem ser afetados.

        O algoritmo realiza BFS nas direções:
        - Forward: seguindo arestas outgoing
        - Backward: seguindo arestas incoming (quando chega como target)

        Retorna uma lista de dicts com: ``urn``, ``path``, ``distance``,
        ``confidence``.

        Args:
            start_urn: URN do nó de partida.

        Returns:
            Lista de nós impactados com metadados de propagação.
        """
        impacted: list[dict] = []
        visited: set[str] = {start_urn}
        queue: list[tuple[str, list[Edge], int, float]] = [
            (start_urn, [], 0, 1.0)
        ]

        while queue:
            current_urn, current_path, distance, cumulative = queue.pop(0)

            # Pula o nó inicial (já registrado como visited)
            if distance > 0:
                impacted.append({
                    "urn": current_urn,
                    "path": [
                        {
                            "source": e.source,
                            "target": e.target,
                            "type": e.type.value,
                            "weight": e.weight,
                        }
                        for e in current_path
                    ],
                    "distance": distance,
                    "confidence": round(cumulative, 4),
                })

            # Explora forward
            for edge in self._get_outbound(current_urn):
                if edge.target not in visited:
                    visited.add(edge.target)
                    new_path = current_path + [edge]
                    new_cumulative = cumulative * edge.weight
                    queue.append(
                        (edge.target, new_path, distance + 1, new_cumulative)
                    )

            # Explora backward (reverse)
            for edge in self._get_inbound(current_urn):
                if edge.source not in visited:
                    visited.add(edge.source)
                    new_path = current_path + [edge]
                    new_cumulative = cumulative * edge.weight
                    queue.append(
                        (edge.source, new_path, distance + 1, new_cumulative)
                    )

        return impacted

    # ───────────────
    # Detecção de Órfãos
    # ───────────────

    def detect_orphans(
        self,
        node_type: Optional[NodeType] = None,
    ) -> list[Node]:
        """Detecta nós sem conexões obrigatórias.

        Regras:
        - **Task**: sem aresta ``contribui_para`` outgoing.
        - **Feature**: sem aresta ``parte_de`` outgoing.
        - **OKR**: sem aresta ``medido_por`` outgoing.
        - **Metric**: sem aresta ``medido_por`` incoming (não mede nenhum OKR).

        Args:
            node_type: Filtrar por tipo de nó (opcional).

        Returns:
            Lista de nós órfãos encontrados.
        """
        orphans: list[Node] = []

        for node in self._nodes.values():
            if node_type is not None and node.type != node_type:
                continue

            if node.type == NodeType.TASK:
                # Task sem contribui_para outgoing
                if not self._get_outbound(node.id, EdgeType.CONTRIBUI_PARA):
                    orphans.append(node)

            elif node.type == NodeType.FEATURE:
                # Feature sem parte_de outgoing
                if not self._get_outbound(node.id, EdgeType.PARTE_DE):
                    orphans.append(node)

            elif node.type == NodeType.OKR:
                # OKR sem medido_por outgoing
                if not self._get_outbound(node.id, EdgeType.MEDIDO_POR):
                    orphans.append(node)

            elif node.type == NodeType.METRIC:
                # Métrica sem medido_por incoming
                if not self._get_inbound(node.id, EdgeType.MEDIDO_POR):
                    orphans.append(node)

        return orphans

    # ───────────────
    # Serialização
    # ───────────────

    def to_dict(self) -> dict:
        """Serializa o grafo completo para dicionário.

        Returns:
            Dict com chaves ``nodes`` e ``edges``.
        """
        return {
            "nodes": [
                {
                    "id": n.id,
                    "type": n.type.value,
                    "attributes": n.attributes,
                    "metadata": {
                        "created_at": n.metadata.created_at,
                        "updated_at": n.metadata.updated_at,
                        "version": n.metadata.version,
                        "source": n.metadata.source,
                        "description": n.metadata.description,
                    },
                }
                for n in self._nodes.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "type": e.type.value,
                    "weight": e.weight,
                    "metadata": {
                        "created_at": e.metadata.created_at,
                        "updated_at": e.metadata.updated_at,
                        "version": e.metadata.version,
                        "confidence": e.metadata.confidence,
                        "reason": e.metadata.reason,
                    },
                }
                for e in self._edges
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KnowledgeGraph":
        """Carrega um grafo de um dicionário.

        Args:
            data: Dict com chaves ``nodes`` e ``edges``.

        Returns:
            Nova instância de ``KnowledgeGraph`` populada.

        Raises:
            ValueError: Se o dict estiver mal-formado.
        """
        kg = cls()

        node_type_map = {nt.value: nt for nt in NodeType}
        edge_type_map = {et.value: et for et in EdgeType}

        for node_data in data.get("nodes", []):
            nt = node_type_map[node_data["type"]]
            meta = node_data.get("metadata", {})
            node = Node(
                id=node_data["id"],
                type=nt,
                attributes=node_data.get("attributes", {}),
                metadata=NodeMetadata(
                    created_at=meta.get("created_at", ""),
                    updated_at=meta.get("updated_at", ""),
                    version=meta.get("version", 1),
                    source=meta.get("source"),
                    description=meta.get("description"),
                ),
            )
            kg._nodes[node.id] = node

        for edge_data in data.get("edges", []):
            et = edge_type_map[edge_data["type"]]
            meta = edge_data.get("metadata", {})
            edge = Edge(
                source=edge_data["source"],
                target=edge_data["target"],
                type=et,
                weight=edge_data.get("weight", 1.0),
                metadata=EdgeMetadata(
                    created_at=meta.get("created_at", ""),
                    updated_at=meta.get("updated_at", ""),
                    version=meta.get("version", 1),
                    confidence=meta.get("confidence", 1.0),
                    reason=meta.get("reason"),
                ),
            )
            kg._edges.append(edge)
            kg._adjacency.setdefault(edge.source, []).append(edge)
            kg._reverse_adj.setdefault(edge.target, []).append(edge)

        # Garante que adjacências existam para todos os nós
        for nid in kg._nodes:
            kg._adjacency.setdefault(nid, [])
            kg._reverse_adj.setdefault(nid, [])

        return kg

    # ───────────────
    # Properties
    # ───────────────

    @property
    def node_count(self) -> int:
        """Número de nós no grafo."""
        return len(self._nodes)

    @property
    def edge_count(self) -> int:
        """Número de arestas no grafo."""
        return len(self._edges)

    # ───────────────
    # Internal Helpers
    # ───────────────

    def _get_outbound(
        self,
        urn: str,
        edge_type: Optional[EdgeType] = None,
    ) -> list[Edge]:
        """Retorna arestas saindo de um nó, opcionalmente filtradas."""
        edges = self._adjacency.get(urn, [])
        if edge_type is not None:
            return [e for e in edges if e.type == edge_type]
        return list(edges)

    def _get_inbound(
        self,
        urn: str,
        edge_type: Optional[EdgeType] = None,
    ) -> list[Edge]:
        """Retorna arestas chegando em um nó, opcionalmente filtradas."""
        edges = self._reverse_adj.get(urn, [])
        if edge_type is not None:
            return [e for e in edges if e.type == edge_type]
        return list(edges)
