"""Testes do módulo context_engine — Memory Manager e tipos de memória."""
import pytest

from apos.context_engine.memory import (
    EVENT_TTL_DAYS,
    InMemoryBackend,
    LongTermMemory,
    MemoryEntry,
    MemoryEvent,
    MemoryManager,
    MemoryType,
    NODE_TTL_DAYS,
    SemanticMemory,
    ShortTermMemory,
)


# ──────────────────────────────────────────────
# InMemoryBackend
# ──────────────────────────────────────────────


class TestInMemoryBackend:
    def test_put_get(self):
        backend = InMemoryBackend()
        backend.put("key1", {"data": 123})
        assert backend.get("key1") == {"data": 123}

    def test_delete(self):
        backend = InMemoryBackend()
        backend.put("key1", "value1")
        assert backend.delete("key1") is True
        assert backend.get("key1") is None
        assert backend.delete("nonexistent") is False

    def test_search_by_prefix(self):
        backend = InMemoryBackend()
        backend.put("urn:apos:task:a", {"title": "A"})
        backend.put("urn:apos:task:b", {"title": "B"})
        backend.put("urn:apos:feature:c", {"title": "C"})
        results = backend.search_by_prefix("urn:apos:task")
        assert len(results) == 2

    def test_events(self):
        backend = InMemoryBackend()
        e1 = MemoryEvent(event_id="evt-001", session_id="sess-1", event_type="state_change")
        e2 = MemoryEvent(event_id="evt-002", session_id="sess-1", event_type="decision_made")
        e3 = MemoryEvent(event_id="evt-003", session_id="sess-2", event_type="state_change")
        backend.add_event(e1)
        backend.add_event(e2)
        backend.add_event(e3)

        assert len(backend.get_events()) == 3
        assert len(backend.get_events(session_id="sess-1")) == 2
        assert len(backend.get_events(event_type="state_change")) == 2
        assert len(backend.get_events(limit=1)) == 1

    def test_rules(self):
        backend = InMemoryBackend()
        backend.set_rule("rule-1", {"description": "Use snake_case", "priority": 10})
        assert backend.get_rule("rule-1")["description"] == "Use snake_case"
        assert len(backend.list_rules()) == 1

    def test_preferences(self):
        backend = InMemoryBackend()
        backend.set_preferences("agent-1", {"format": "detailed"})
        assert backend.get_preferences("agent-1")["format"] == "detailed"


# ──────────────────────────────────────────────
# ShortTermMemory
# ──────────────────────────────────────────────


class TestShortTermMemory:
    def test_put_get(self):
        stm = ShortTermMemory()
        stm.put("focus", "Implement OAuth")
        assert stm.get("focus") == "Implement OAuth"
        assert stm.get("nonexistent") is None

    def test_remove(self):
        stm = ShortTermMemory()
        stm.put("key", "value")
        assert stm.remove("key") is True
        assert stm.remove("nonexistent") is False

    def test_active_urns(self):
        stm = ShortTermMemory()
        stm.set_active_urns(["urn:apos:task:oauth-123"])
        assert stm.get_active_urns() == ["urn:apos:task:oauth-123"]

    def test_temporary_state(self):
        stm = ShortTermMemory()
        stm.set_temporary_state("last_search", ["result1"])
        assert stm.get_temporary_state("last_search") == ["result1"]

    def test_queries(self):
        stm = ShortTermMemory()
        stm.add_query("What is the status?")
        assert len(stm._recent_queries) == 1

    def test_clear(self):
        stm = ShortTermMemory()
        stm.put("key", "value")
        stm.add_query("test query")
        stm.clear()
        assert stm.get("key") is None
        assert len(stm._recent_queries) == 0

    def test_token_estimate(self):
        stm = ShortTermMemory()
        stm.put("small", "abc")
        stm.put("medium", "x" * 100)
        assert stm.token_estimate() > 0


# ──────────────────────────────────────────────
# MemoryEvent
# ──────────────────────────────────────────────


class TestMemoryEvent:
    def test_create_event(self):
        event = MemoryEvent(
            event_id="evt-001",
            session_id="sess-abc",
            event_type="state_change",
            delta={"field": "status", "old_value": "open", "new_value": "in_progress"},
        )
        assert event.event_id == "evt-001"
        assert event.event_type == "state_change"

    def test_event_ttl_default(self):
        """TTL deve vir do EVENT_TTL_DAYS quando não especificado."""
        event = MemoryEvent(
            event_id="evt-002",
            session_id="sess-abc",
        )
        assert event.ttl_days is None  # default None, é setado no add_event


# ──────────────────────────────────────────────
# MemoryManager
# ──────────────────────────────────────────────


class TestMemoryManager:
    def test_put_and_get_short_term(self):
        mm = MemoryManager()
        mm.put("current_task", "oauth-123", memory_type=MemoryType.SHORT_TERM)
        assert mm.get("current_task") == "oauth-123"

    def test_recall_by_urn(self):
        mm = MemoryManager()
        mm.put("urn:apos:task:oauth-123", {"title": "OAuth"}, memory_type=MemoryType.SHORT_TERM)
        # URN válida mas não está no long_term
        result = mm.recall_by_urn("urn:apos:task:oauth-123")
        # Está no long_term? Não foi inserido lá.
        assert result is None  # só está no short_term

    def test_recall_by_metadata(self):
        mm = MemoryManager()
        mm.long_term.put_node("urn:apos:task:a", {"type": "task", "status": "blocked"})
        mm.long_term.put_node("urn:apos:task:b", {"type": "task", "status": "in_progress"})
        results = mm.recall_by_metadata({"status": "blocked"})
        assert len(results) >= 1

    def test_forget(self):
        mm = MemoryManager()
        mm.put("key1", "value1", memory_type=MemoryType.SHORT_TERM)
        assert mm.forget("key1") is True
        assert mm.get("key1") is None

    def test_end_session(self):
        mm = MemoryManager()
        mm.put("temp", "data", memory_type=MemoryType.SHORT_TERM)
        report = mm.end_session()
        assert "short_term_entries" in report
        assert mm.short_term.token_estimate() == 0

    def test_recall_string_query(self):
        mm = MemoryManager()
        mm.semantic.add_rule("rule-1", {"description": "Sempre usar snake_case"})
        results = mm.recall(query="snake_case")
        assert len(results) >= 1

    def test_purge_expired(self):
        mm = MemoryManager()
        counts = mm.purge_expired()
        assert "episodic" in counts
        assert "long_term" in counts

    def test_multiple_memory_types(self):
        mm = MemoryManager()
        mm.put("st_key", "st_val", memory_type=MemoryType.SHORT_TERM)
        mm.put("lt_key", {"data": "lt_val"}, memory_type=MemoryType.LONG_TERM)
        mm.put("rule-key", {"description": "rule"}, memory_type=MemoryType.SEMANTIC)
        assert mm.get("st_key") == "st_val"
        assert mm.get("lt_key", memory_type=MemoryType.LONG_TERM) == {"data": "lt_val"}


# ──────────────────────────────────────────────
# Constantes
# ──────────────────────────────────────────────


class TestConstants:
    def test_node_ttl_days(self):
        assert NODE_TTL_DAYS["task"] == 7
        assert NODE_TTL_DAYS["feature"] == 30
        assert NODE_TTL_DAYS["okr"] == 90
        assert NODE_TTL_DAYS["persona"] == -1

    def test_event_ttl_days(self):
        assert EVENT_TTL_DAYS["state_change"] == 30
        assert EVENT_TTL_DAYS["decision_made"] == 90
        assert EVENT_TTL_DAYS["query_executed"] == 7
