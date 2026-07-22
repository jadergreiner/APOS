"""Testes para o ProjectAdapter e ProjectProfile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from apos.project_adapter import Detector, ProjectAdapter, ProjectProfile
from apos.project_adapter.errors import DetectorExecutionError

# =============================================================================
# ProjectProfile
# =============================================================================


class TestProjectProfile:
    def test_default_values(self):
        p = ProjectProfile()
        assert p.language == "unknown"
        assert p.framework == "unknown"
        assert p.database == "unknown"
        assert p.cloud_provider == "unknown"
        assert p.runtime_version is None
        assert p.module_count == 0
        assert p.core_modules == []
        assert p.directory_layout == "flat"
        assert p.total_loc == 0
        assert p.architecture_patterns == []
        assert p.detected_patterns == []
        assert p.has_ontology is False
        assert p.domain_entities == []
        assert p.naming_convention == "unknown"
        assert p.detector_results == {}

    def test_custom_values(self):
        p = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="PostgreSQL",
            cloud_provider="AWS",
            runtime_version=">=3.11",
            module_count=5,
            core_modules=["apos", "tests"],
            directory_layout="nested",
            total_loc=1234,
            architecture_patterns=["fastapi_routes"],
            detected_patterns=["fastapi_routes"],
            has_ontology=True,
            domain_entities=["Project", "Profile"],
            naming_convention="snake_case",
            detector_results={"stack": {"language": "Python"}},
        )
        assert p.language == "Python"
        assert p.detector_results == {"stack": {"language": "Python"}}

    def test_model_dump_json(self):
        p = ProjectProfile()
        dumped = p.model_dump_json()
        assert isinstance(dumped, str)
        assert '"language":"unknown"' in dumped or '"language": "unknown"' in dumped

    def test_model_dump(self):
        p = ProjectProfile(language="Python")
        d = p.model_dump()
        assert isinstance(d, dict)
        assert d["language"] == "Python"


# =============================================================================
# ProjectAdapter
# =============================================================================


class TestProjectAdapter:
    def test_init_with_default_detectors(self):
        pa = ProjectAdapter()
        # 4 default detectors: stack, modules, patterns, semantic
        assert len(pa._detectors) >= 4

    def test_register_detector(self):
        pa = ProjectAdapter()
        initial_count = len(pa._detectors)

        class MockDetector(Detector):
            name = "mock"

            def detect(self, project_root: Path) -> dict[str, Any]:
                return {"mock": True}

        pa.register_detector(MockDetector())
        assert len(pa._detectors) == initial_count + 1

    def test_discover_in_existing_dir(self, tmp_path: Path):
        pa = ProjectAdapter()
        profile = pa.discover(tmp_path)
        assert isinstance(profile, ProjectProfile)
        # Empty dir should have all defaults
        assert profile.language == "unknown"

    def test_discover_with_pyproject(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "test"\ndependencies = ["fastapi"]\n'
        )
        pa = ProjectAdapter()
        profile = pa.discover(tmp_path)
        assert profile.language == "Python"
        assert profile.framework == "FastAPI"

    def test_discover_nonexistent_dir_raises(self):
        pa = ProjectAdapter()
        with pytest.raises(ValueError, match="Project root does not exist"):
            pa.discover("/nonexistent/path/xyz123")

    def test_discover_detector_error_raises(self, tmp_path: Path):
        class BrokenDetector(Detector):
            name = "broken"

            def detect(self, project_root: Path) -> dict[str, Any]:
                raise RuntimeError("something broke")

        pa = ProjectAdapter()
        pa.register_detector(BrokenDetector())
        with pytest.raises(DetectorExecutionError, match="'broken' falhou"):
            pa.discover(tmp_path)

    def test_analyze_returns_dict_with_profile_and_confidence(self, tmp_path: Path):
        pa = ProjectAdapter()
        result = pa.analyze(tmp_path)
        assert isinstance(result, dict)
        assert "profile" in result
        assert "confidence" in result
        assert isinstance(result["profile"], dict)
        assert isinstance(result["confidence"], float)

    def test_analyze_confidence_scale(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "test"\ndependencies = ["fastapi", "boto3"]\n'
        )
        pa = ProjectAdapter()
        result = pa.analyze(tmp_path)
        assert 0.0 <= result["confidence"] <= 1.0

    def test_discover_detector_exeception_passthrough(self, tmp_path: Path):
        class FailDetector(Detector):
            name = "fail"

            def detect(self, project_root: Path) -> dict[str, Any]:
                raise DetectorExecutionError("custom error")

        pa = ProjectAdapter()
        pa.register_detector(FailDetector())
        with pytest.raises(DetectorExecutionError, match="custom error"):
            pa.discover(tmp_path)

    def test_discover_ignores_ignored_dirs(self, tmp_path: Path):
        # Even with ignored dirs, discovery should not crash
        (tmp_path / "node_modules").mkdir()
        (tmp_path / ".git").mkdir()
        (tmp_path / "venv").mkdir()
        (tmp_path / "__pycache__").mkdir()
        pa = ProjectAdapter()
        profile = pa.discover(tmp_path)
        assert isinstance(profile, ProjectProfile)

    def test_confidence_zero_on_empty(self, tmp_path: Path):
        pa = ProjectAdapter()
        result = pa.analyze(tmp_path)
        assert result["confidence"] == 0.0

    def test_confidence_full_on_rich_project(self, tmp_path: Path):
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "full"\ndependencies = ["fastapi", "boto3", "psycopg2"]\n'
        )
        (tmp_path / "apos").mkdir()
        (tmp_path / "apos" / "__init__.py").write_text("#")
        (tmp_path / "docs" / "SDD").mkdir(parents=True)
        (tmp_path / "docs" / "SDD" / "arch.md").write_text("entity Project\nentity Task\n")
        (tmp_path / "router.py").write_text(
            "from fastapi import APIRouter\nrouter = APIRouter()\n@router.get('/')\ndef h(): pass\n"
        )
        pa = ProjectAdapter()
        result = pa.analyze(tmp_path)
        assert result["confidence"] > 0.0
        assert result["profile"]["has_ontology"] is True


# =============================================================================
# Integration: discover no proprio APOS
# =============================================================================


def test_discover_apos_itself():
    """Descobre o profile do proprio projeto APOS."""
    pa = ProjectAdapter()
    # Get repo root: tests/unit/test_project_adapter/test_adapter.py -> APOS/
    repo = Path(__file__).resolve().parents[3]
    if not (repo / "apos" / "project_adapter").exists():
        pytest.skip("Not in APOS repo root")
    profile = pa.discover(repo)
    assert profile.language == "Python"
    assert isinstance(profile.module_count, int)
    assert isinstance(profile.total_loc, int)
