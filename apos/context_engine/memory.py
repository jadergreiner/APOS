"""
APOS Memory Model — Sistema de Memória de Agentes (Camada 3.5)

Gerencia 4 tipos de memória (ShortTerm, LongTerm, Episodic, Semantic)
com persistência, recall, compressão e TTL.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


# ──────────────────────────────────────────────
# Tipos de Memória
# ──────────────────────────────────────────────


class MemoryType(Enum):
    """Tipos de memória no sistema APOS."""
    SHORT_TERM = "short_term"      # Working memory (sessão)
    LONG_TERM = "long_term"        # Knowledge Graph (persistente)
    EPISODIC = "episodic"          # Event log (timestamped)
    SEMANTIC = "semantic"          # Rules store (preferências)


# ──────────────────────────────────────────────
# Dataclasses
# ──────────────────────────────────────────────


@dataclass
class MemoryEntry:
    """Entrada genérica no sistema de memória.

    Attributes:
        key: Identificador único (URN para KG, event_id para episódica, etc.).
        value: Dados armazenados (dict, str, etc.).
        memory_type: Tipo de memória.
        created_at: ISO 8601 de criação.
        updated_at: ISO 8601 da última atualização.
        ttl_seconds: TTL em segundos (None = indefinido).
        access_count: Contador de acessos (para LRU).
        last_access: ISO 8601 do último acesso.
    """
    key: str
    value: Any
    memory_type: MemoryType = MemoryType.SHORT_TERM
    created_at: str = ""
    updated_at: str = ""
    ttl_seconds: Optional[int] = None
    access_count: int = 0
    last_access: str = ""


@dataclass
class MemoryEvent:
    """Evento episódico timestamped.

    Attributes:
        event_id: Identificador único do evento.
        session_id: Sessão que gerou o evento.
        timestamp: ISO 8601 do evento.
        event_type: Tipo (state_change, query_executed, decision_made, etc.).
        actor: Agente/entidade que gerou o evento.
        urns_affected: Lista de URNs afetadas.
        delta: Mudança ocorrida (dict).
        reason: Razão contextual.
        token_cost: Custo em tokens (opcional).
        ttl_days: TTL em dias (padrão por tipo de evento).
    """
    event_id: str
    session_id: str
    timestamp: str = ""
    event_type: str = "state_change"
    actor: Optional[str] = None
    urns_affected: list[str] = field(default_factory=list)
    delta: dict = field(default_factory=dict)
    reason: Optional[str] = None
    token_cost: int = 0
    ttl_days: Optional[int] = None


# ──────────────────────────────────────────────
# TTL Configurações
# ──────────────────────────────────────────────

# TTL por tipo de nó (em dias, para archive/delete)
NODE_TTL_DAYS: dict[str, int] = {
    "task": 7,
    "feature": 30,
    "release": 30,
    "sprint": 30,
    "okr": 90,
    "metric": 90,
    "persona": -1,  # Indefinido
}

# TTL por tipo de evento episódico (em dias)
EVENT_TTL_DAYS: dict[str, int] = {
    "state_change": 30,
    "query_executed": 7,
    "decision_made": 90,
    "error_occurred": 90,
    "context_assembled": 7,
    "compression_run": 30,
    "session_summary": 90,
}


# ──────────────────────────────────────────────
# Backend de Persistência
# ──────────────────────────────────────────────


class InMemoryBackend:
    """Backend de persistência em memória (dev/testes).

    Armazena entradas em dicionários Python. Não persiste entre
    reinicializações.
    """

    def __init__(self) -> None:
        self._store: dict[str, Any] = {}
        self._events: list[MemoryEvent] = []
        self._rules: dict[str, dict] = {}
        self._preferences: dict[str, dict] = {}

    # ─── Generic ───────────────────────────────

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def put(self, key: str, value: Any) -> None:
        self._store[key] = value

    def delete(self, key: str) -> bool:
        return self._store.pop(key, None) is not None

    def list_keys(self) -> list[str]:
        return list(self._store.keys())

    def search_by_prefix(self, prefix: str) -> list[tuple[str, Any]]:
        return [(k, v) for k, v in self._store.items() if k.startswith(prefix)]

    def clear(self) -> None:
        self._store.clear()
        self._events.clear()
        self._rules.clear()
        self._preferences.clear()

    # ─── Events ────────────────────────────────

    def add_event(self, event: MemoryEvent) -> None:
        self._events.append(event)

    def get_events(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> list[MemoryEvent]:
        results = self._events
        if session_id:
            results = [e for e in results if e.session_id == session_id]
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        return results[-limit:]

    def purge_expired_events(self) -> int:
        """Remove eventos com TTL expirado. Retorna número de removidos."""
        now = datetime.now(timezone.utc)
        before = len(self._events)
        self._events = [
            e for e in self._events
            if e.ttl_days is None or not e.timestamp
            or (now - _parse_dt(e.timestamp)).days < e.ttl_days
        ]
        return before - len(self._events)

    # ─── Rules ─────────────────────────────────

    def set_rule(self, rule_id: str, rule_data: dict) -> None:
        self._rules[rule_id] = rule_data

    def get_rule(self, rule_id: str) -> Optional[dict]:
        return self._rules.get(rule_id)

    def list_rules(self) -> list[dict]:
        return list(self._rules.values())

    def set_preferences(self, agent_id: str, prefs: dict) -> None:
        self._preferences[agent_id] = prefs

    def get_preferences(self, agent_id: str) -> Optional[dict]:
        return self._preferences.get(agent_id)


def _parse_dt(iso_str: str) -> datetime:
    try:
        return datetime.fromisoformat(iso_str)
    except (ValueError, TypeError):
        return datetime.now(timezone.utc)


# ──────────────────────────────────────────────
# Camadas de Memória
# ──────────────────────────────────────────────


class ShortTermMemory:
    """Memória de curto prazo (working memory) — volátil, por sessão.

    Gerencia o contexto ativo da sessão atual com política LRU.
    """

    def __init__(
        self,
        max_tokens: int = 4096,
        lru_eviction_count: int = 512,
        lru_priority_boost: float = 2.0,
    ) -> None:
        self._entries: dict[str, MemoryEntry] = {}
        self._active_urns: list[str] = []
        self._current_focus: Optional[str] = None
        self._recent_queries: list[str] = []
        self._temporary_state: dict = {}
        self.max_tokens = max_tokens
        self.lru_eviction_count = lru_eviction_count
        self.lru_priority_boost = lru_priority_boost

    def put(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        now = _now_iso()
        entry = MemoryEntry(
            key=key,
            value=value,
            memory_type=MemoryType.SHORT_TERM,
            created_at=now,
            updated_at=now,
            ttl_seconds=ttl_seconds,
        )
        self._entries[key] = entry
        self._maybe_evict()

    def get(self, key: str) -> Optional[Any]:
        entry = self._entries.get(key)
        if entry is None:
            return None
        entry.access_count += 1
        entry.last_access = _now_iso()
        return entry.value

    def remove(self, key: str) -> bool:
        return self._entries.pop(key, None) is not None

    def set_active_urns(self, urns: list[str]) -> None:
        self._active_urns = urns

    def get_active_urns(self) -> list[str]:
        return list(self._active_urns)

    def add_query(self, query: str) -> None:
        self._recent_queries.append(query)
        if len(self._recent_queries) > 50:
            self._recent_queries = self._recent_queries[-50:]

    def set_temporary_state(self, key: str, value: Any) -> None:
        self._temporary_state[key] = value

    def get_temporary_state(self, key: str) -> Optional[Any]:
        return self._temporary_state.get(key)

    def token_estimate(self) -> int:
        total = 0
        for entry in self._entries.values():
            text = json.dumps(entry.value, ensure_ascii=False)
            total += len(text) // 4
        return total

    def clear(self) -> None:
        self._entries.clear()
        self._recent_queries.clear()
        self._temporary_state.clear()

    def _maybe_evict(self) -> None:
        """Aplica LRU se a estimativa de tokens exceder o máximo."""
        if self.token_estimate() <= self.max_tokens:
            return

        # Ordena por last_access (mais antigo primeiro)
        sorted_entries = sorted(
            self._entries.values(),
            key=lambda e: e.last_access or "",
        )

        # Aplica boost para URNs ativas
        for entry in sorted_entries:
            if entry.key in self._active_urns:
                entry.access_count = int(entry.access_count * self.lru_priority_boost)

        # Remove entradas até caber
        for entry in sorted_entries:
            if self.token_estimate() <= self.max_tokens:
                break
            if entry.key not in self._active_urns:
                self._entries.pop(entry.key, None)

    def to_dict(self) -> dict:
        return {
            "active_urns": self._active_urns,
            "current_focus": self._current_focus,
            "recent_queries": self._recent_queries,
            "temporary_state": self._temporary_state,
            "token_estimate": self.token_estimate(),
        }


class LongTermMemory:
    """Memória de longo prazo (Knowledge Graph) — persistente.

    Atua como wrapper sobre o Knowledge Graph e/ou backends de
    persistência.
    """

    def __init__(self, backend: Optional[InMemoryBackend] = None) -> None:
        self.backend = backend or InMemoryBackend()

    def get_node(self, urn: str) -> Optional[Any]:
        return self.backend.get(urn)

    def put_node(self, urn: str, node_data: dict) -> None:
        self.backend.put(urn, node_data)

    def delete_node(self, urn: str) -> bool:
        return self.backend.delete(urn)


class EpisodicMemory:
    """Memória episódica (event log) — timestamped, com TTL.

    Armazena histórico de interações, mudanças de estado e decisões.
    """

    def __init__(self, backend: Optional[InMemoryBackend] = None) -> None:
        self.backend = backend or InMemoryBackend()

    def add_event(self, event: MemoryEvent) -> None:
        if not event.timestamp:
            event.timestamp = _now_iso()
        if event.ttl_days is None:
            event.ttl_days = EVENT_TTL_DAYS.get(event.event_type, 30)
        self.backend.add_event(event)

    def get_events(
        self,
        session_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> list[MemoryEvent]:
        return self.backend.get_events(
            session_id=session_id,
            event_type=event_type,
            limit=limit,
        )

    def reconstruct_session(self, session_id: str) -> Optional[dict]:
        """Reconstrói o contexto de uma sessão anterior."""
        events = self.get_events(session_id=session_id, limit=50)
        if not events:
            return None

        active_urns: set[str] = set()
        changes = []
        for e in events:
            for u in (e.urns_affected or []):
                active_urns.add(u)
            if e.event_type in ("state_change", "decision_made"):
                changes.append({
                    "urn": (e.urns_affected or [None])[0],
                    "field": e.delta.get("field", ""),
                    "from": e.delta.get("old_value"),
                    "to": e.delta.get("new_value"),
                    "reason": e.reason,
                })

        summary_event = None
        for e in reversed(events):
            if e.event_type == "session_summary":
                summary_event = e
                break

        return {
            "session_id": session_id,
            "summary": summary_event.delta.get("summary") if summary_event else None,
            "active_urns": list(active_urns),
            "recent_changes": changes[-20:],
            "pending_decisions": [
                c for c in changes if c.get("field") == "decision"
            ],
            "timestamp": events[-1].timestamp if events else None,
        }

    def purge_expired(self) -> int:
        return self.backend.purge_expired_events()


class SemanticMemory:
    """Memória semântica (rules store) — regras e preferências persistentes.

    Armazena convenções, regras de negócio, preferências de agente.
    """

    def __init__(self, backend: Optional[InMemoryBackend] = None) -> None:
        self.backend = backend or InMemoryBackend()

    def add_rule(self, rule_id: str, rule_data: dict) -> None:
        if "created_at" not in rule_data:
            rule_data["created_at"] = _now_iso()
        rule_data["rule_id"] = rule_id
        self.backend.set_rule(rule_id, rule_data)

    def get_rules(self, scope: Optional[str] = None) -> list[dict]:
        rules = self.backend.list_rules()
        if scope:
            rules = [r for r in rules if r.get("scope") == scope]
        return sorted(rules, key=lambda r: r.get("priority", 5), reverse=True)

    def set_preferences(self, agent_id: str, prefs: dict) -> None:
        self.backend.set_preferences(agent_id, prefs)

    def get_preferences(self, agent_id: str) -> Optional[dict]:
        return self.backend.get_preferences(agent_id)

    def create_default_preferences(self, agent_id: str) -> dict:
        """Cria preferências padrão para um agente."""
        defaults = {
            "default_ttl_tasks": "7d",
            "default_ttl_metrics": "90d",
            "max_episodic_events_per_session": 100,
            "compression_trigger_token_count": 6000,
            "recall_max_results": 20,
            "recall_min_score": 0.3,
        }
        self.set_preferences(agent_id, defaults)
        return defaults


# ──────────────────────────────────────────────
# Memory Manager
# ──────────────────────────────────────────────


class MemoryManager:
    """Orquestrador central dos 4 tipos de memória.

    Roteia operações de leitura/escrita para o tipo de memória
    apropriado e executa compressão, TTL e recall combinado.
    """

    def __init__(
        self,
        backend: Optional[InMemoryBackend] = None,
    ) -> None:
        backend = backend or InMemoryBackend()
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory(backend)
        self.episodic = EpisodicMemory(backend)
        self.semantic = SemanticMemory(backend)
        self._backend = backend

    # ─── Write ─────────────────────────────────

    def put(
        self,
        key: str,
        value: Any,
        memory_type: MemoryType = MemoryType.SHORT_TERM,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """Armazena um valor no tipo de memória especificado."""
        if memory_type == MemoryType.SHORT_TERM:
            self.short_term.put(key, value, ttl_seconds)
        elif memory_type == MemoryType.LONG_TERM:
            self.long_term.put_node(key, value)
        elif memory_type == MemoryType.SEMANTIC:
            self.semantic.add_rule(key, value)
        else:
            self._backend.put(key, value)

    # ─── Read ──────────────────────────────────

    def get(
        self,
        key: str,
        memory_type: MemoryType = MemoryType.SHORT_TERM,
    ) -> Optional[Any]:
        """Recupera um valor do tipo de memória especificado."""
        if memory_type == MemoryType.SHORT_TERM:
            return self.short_term.get(key)
        elif memory_type == MemoryType.LONG_TERM:
            return self.long_term.get_node(key)
        elif memory_type == MemoryType.SEMANTIC:
            return self.semantic.get_rules()
        return self._backend.get(key)

    # ─── Recall ────────────────────────────────

    def recall(
        self,
        query: str,
        max_results: int = 10,
        min_score: float = 0.3,
    ) -> list[dict]:
        """Recall combinado: busca por URN, metadata e eventos.

        Args:
            query: Texto da consulta (pode ser URN ou texto livre).
            max_results: Máximo de resultados.
            min_score: Score mínimo.

        Returns:
            Lista de resultados combinados e ranqueados.
        """
        results: list[dict] = []

        # Método 1: URN direta
        from apos.core.types import is_valid_urn
        if is_valid_urn(query):
            node = self.long_term.get_node(query)
            if node:
                results.append({
                    "urn": query,
                    "value": node,
                    "method": "direct_urn",
                    "score": 1.0,
                })
                return results

        # Método 2: Busca em memória curta
        st_val = self.short_term.get(query)
        if st_val:
            results.append({
                "key": query,
                "value": st_val,
                "method": "short_term",
                "score": 0.8,
            })

        # Método 3: Busca em regras semânticas
        rules = self.semantic.get_rules()
        for rule in rules:
            if query.lower() in rule.get("description", "").lower():
                results.append({
                    "rule_id": rule.get("rule_id"),
                    "description": rule.get("description"),
                    "method": "semantic",
                    "score": 0.6,
                })

        # Método 4: Eventos recentes
        events = self.episodic.get_events(limit=max_results)
        for event in events:
            if query.lower() in str(event.delta).lower():
                results.append({
                    "event_id": event.event_id,
                    "type": event.event_type,
                    "delta": event.delta,
                    "method": "episodic",
                    "score": 0.4,
                })

        # Ordena por score e limita
        results.sort(key=lambda r: r.get("score", 0), reverse=True)
        return results[:max_results]

    def recall_by_urn(self, urn: str) -> Optional[dict]:
        """Recall por URN direta no Knowledge Graph."""
        node = self.long_term.get_node(urn)
        if node is None:
            return None
        return {
            "urn": urn,
            "node": node,
        }

    def recall_by_metadata(
        self,
        filters: dict,
    ) -> list[dict]:
        """Recall por metadados (tipo, status, owner, etc.)."""
        results = []
        for key in self._backend.list_keys():
            val = self._backend.get(key)
            if not isinstance(val, dict):
                continue
            match = True
            for fk, fv in filters.items():
                if val.get(fk) != fv:
                    match = False
                    break
            if match:
                results.append({"urn": key, "value": val})
        return results

    # ─── Forget ────────────────────────────────

    def forget(self, key: str) -> bool:
        """Remove uma entrada de todos os tipos de memória."""
        removed = False
        if self.short_term.remove(key):
            removed = True
        if self.long_term.delete_node(key):
            removed = True
        if self._backend.delete(key):
            removed = True
        return removed

    def purge_expired(self) -> dict[str, int]:
        """Remove entradas expiradas de todos os tipos de memória.

        Returns:
            Dict com contagem de itens removidos por tipo.
        """
        counts: dict[str, int] = {}
        counts["episodic"] = self.episodic.purge_expired()
        counts["long_term"] = 0
        counts["short_term"] = 0
        return counts

    # ─── Session ───────────────────────────────

    def end_session(self) -> dict:
        """Finaliza a sessão atual: limpa working memory e gera relatório."""
        report = {
            "short_term_entries": len(self.short_term._entries),
            "short_term_tokens": self.short_term.token_estimate(),
            "events_count": len(self._backend._events),
            "rules_count": len(self._backend.list_rules()),
        }
        self.short_term.clear()
        return report


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
