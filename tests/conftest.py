"""
Pytest configuration and fixtures for APOS tests.
"""

import pytest
import sys
from pathlib import Path

# Add apos to path so tests can import it
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def sample_ontology_dict():
    """Sample ontology data for tests."""
    return {
        "name": "Student Journey",
        "version": "1.0",
        "entities": [
            {"id": "student", "name": "Student", "description": "A learner"},
            {"id": "course", "name": "Course", "description": "Learning path"},
        ],
        "relationships": [
            {"source": "student", "target": "course", "type": "enrolled_in"},
        ],
    }


@pytest.fixture
def sample_graph_data():
    """Sample graph data for tests."""
    return {
        "nodes": [
            {"id": "student_001", "entity_id": "student", "attrs": {"name": "Alice"}},
            {"id": "course_101", "entity_id": "course", "attrs": {"name": "Python"}},
        ],
        "edges": [
            {"source": "student_001", "target": "course_101", "type": "enrolled_in"},
        ],
    }
