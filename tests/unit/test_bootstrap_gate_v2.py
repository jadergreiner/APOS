"""Tests for BootstrapGateV2 — 10 scenarios covering init, validate, config, save, report, and integration."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from apos.bootstrap.gate_v2 import BootstrapGateV2, GateResultV2
from apos.project_adapter import ProjectAdapter, ProjectProfile


# =============================================================================
# V1: test_init_with_profile
# =============================================================================


class TestInit:
    """BootstrapGateV2 construction."""

    def test_init_with_profile(self):
        """V1: BootstrapGateV2 accepts a ProjectProfile directly."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            cloud_provider="AWS",
            module_count=5,
            has_ontology=True,
            domain_entities=["User", "Project"],
            detector_results={"stack": {"language": "Python"}},
        )
        gate = BootstrapGateV2(profile=profile)
        assert gate.profile.language == "Python"
        assert gate.profile.framework == "FastAPI"

    def test_init_with_adapter(self, tmp_path: Path):
        """V2: BootstrapGateV2 accepts a ProjectAdapter (runs discover)."""
        # Create a minimal Python project
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "test"\ndependencies = ["fastapi"]\n'
        )
        (tmp_path / "mymod").mkdir()
        (tmp_path / "mymod" / "__init__.py").write_text("#")
        (tmp_path / "main.py").write_text("x = 1")

        pa = ProjectAdapter()
        gate = BootstrapGateV2(adapter=pa, project_root=tmp_path)
        assert gate.profile.language == "Python"
        assert gate.profile.framework == "FastAPI"

    def test_init_no_args_raises(self):
        """V2.5: BootstrapGateV2 without profile or adapter raises."""
        with pytest.raises(ValueError, match="Must provide either"):
            BootstrapGateV2()

    def test_init_profile_takes_precedence(self, tmp_path: Path):
        """When both profile and adapter are given, profile wins."""
        profile = ProjectProfile(language="Go")
        pa = ProjectAdapter()
        gate = BootstrapGateV2(profile=profile, adapter=pa, project_root=tmp_path)
        assert gate.profile.language == "Go"


# =============================================================================
# V3 / V4 / V5: validate
# =============================================================================


class TestValidate:
    """BootstrapGateV2.validate() scenarios."""

    def test_validate_passes(self):
        """V3: Complete profile → passed=True, score >= 0.5."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="PostgreSQL",
            cloud_provider="AWS",
            module_count=5,
            core_modules=["api", "core"],
            architecture_patterns=["domain_infra_split"],
            has_ontology=True,
            domain_entities=["User", "Task"],
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "modules": {"module_count": 5, "core_modules": ["api", "core"]},
                "patterns": {"architecture_patterns": ["domain_infra_split"]},
                "semantic": {"has_ontology": True, "domain_entities": ["User", "Task"]},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        result = gate.validate()

        assert result.passed is True
        assert result.score >= 0.5
        assert len(result.issues) == 0

    def test_validate_fails_language(self):
        """V4: language=unknown → passed=False, score < 0.5."""
        profile = ProjectProfile(
            language="unknown",
            framework="unknown",
            database="unknown",
            module_count=0,
            has_ontology=False,
        )
        gate = BootstrapGateV2(profile=profile)
        result = gate.validate()

        assert result.passed is False
        # With only 1/6 fields filled, confidence should be low
        assert result.score < 0.5
        assert any("language" in i.lower() for i in result.issues)

    def test_validate_fails_low_confidence(self):
        """confidence < MIN_CONFIDENCE (0.5) → passed=False."""
        profile = ProjectProfile(
            language="unknown",
            framework="unknown",
            database="unknown",
            module_count=0,
            has_ontology=False,
        )
        gate = BootstrapGateV2(profile=profile)
        result = gate.validate()

        assert result.passed is False
        assert result.score < 0.5
        assert any("confidence" in i.lower() for i in result.issues)

    def test_validate_warns_no_ontology(self):
        """V5: has_ontology=False → warning list not empty."""
        profile = ProjectProfile(
            language="Python",
            framework="Flask",
            database="SQLite",
            module_count=3,
            core_modules=["app"],
            has_ontology=False,
            detector_results={
                "stack": {"language": "Python"},
                "modules": {"module_count": 3, "core_modules": ["app"]},
                "patterns": {"architecture_patterns": []},
                "semantic": {"has_ontology": False},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        result = gate.validate()

        # Language detected + modules > 0 should give confidence ~ 0.5
        # 2/6 fields filled → 0.33 < 0.5 so it fails on confidence
        # But we also check warnings have ontology message
        assert len(result.warnings) > 0
        assert any("ontology" in w.lower() for w in result.warnings)

    def test_validate_warns_no_modules(self):
        """module_count=0 triggers a warning."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            module_count=0,
            has_ontology=True,
            domain_entities=["X"],
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "modules": {"module_count": 0},
                "patterns": {"architecture_patterns": ["fastapi_routes"]},
                "semantic": {"has_ontology": True, "domain_entities": ["X"]},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        result = gate.validate()

        # With language, framework, database, has_ontology all filled → confidence ≥ 0.5
        # Only architecture_patterns is empty → 5/6 = 0.83
        assert any("modules" in w.lower() for w in result.warnings)


# =============================================================================
# V6 / V7: generate_config / save_config
# =============================================================================


class TestConfig:
    """Config generation and saving."""

    def test_generate_config(self):
        """V6: generate_config() returns valid YAML string with profile data."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            cloud_provider="AWS",
            module_count=5,
            has_ontology=True,
            domain_entities=["User", "Project"],
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "semantic": {"has_ontology": True, "domain_entities": ["User", "Project"]},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        yaml_str = gate.generate_config()

        # Validate it's proper YAML
        parsed = yaml.safe_load(yaml_str)
        assert parsed["project"]["language"] == "Python"
        assert parsed["project"]["framework"] == "FastAPI"
        assert parsed["project"]["database"] == "DynamoDB"
        assert parsed["project"]["cloud_provider"] == "AWS"
        assert parsed["ontology"]["has_ontology"] is True
        assert parsed["ontology"]["domain_entities"] == ["User", "Project"]
        assert parsed["governance"]["min_confidence"] == 0.5
        assert isinstance(parsed["governance"]["confidence_score"], float)

    def test_save_config(self, tmp_path: Path):
        """V7: save_config() writes YAML file to disk."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            cloud_provider="AWS",
            module_count=3,
            has_ontology=False,
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "semantic": {"has_ontology": False},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        target = tmp_path / "APOS_CONFIG.yaml"
        saved_path = gate.save_config(str(target))

        assert Path(saved_path).exists()
        assert Path(saved_path) == target.resolve()

        # Verify content
        content = target.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        assert parsed["project"]["language"] == "Python"


# =============================================================================
# V8: report
# =============================================================================


class TestReport:
    """Human-readable report."""

    def test_report(self):
        """V8: report() returns formatted string with profile info."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="PostgreSQL",
            cloud_provider="AWS",
            module_count=7,
            has_ontology=True,
            domain_entities=["User", "Task", "Project"],
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "modules": {"module_count": 7},
                "patterns": {"architecture_patterns": []},
                "semantic": {"has_ontology": True, "domain_entities": ["User", "Task", "Project"]},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        report = gate.report()

        assert isinstance(report, str)
        assert "BootstrapGateV2" in report
        assert "Python" in report
        assert "FastAPI" in report
        assert "Passed" in report or "PASSED" in report
        assert "Confidence" in report


# =============================================================================
# V9: integration with ProjectAdapter
# =============================================================================


class TestIntegration:
    """Integration with real ProjectAdapter discover."""

    def test_integration_with_project_adapter(self, tmp_path: Path):
        """V9: ProjectAdapter.discover() → BootstrapGateV2.validate() → passed."""
        # Create a rich project
        (tmp_path / "pyproject.toml").write_text(
            '[project]\nname = "rich"\ndependencies = ["fastapi", "boto3", "psycopg2"]\n'
        )
        (tmp_path / "core").mkdir()
        (tmp_path / "core" / "__init__.py").write_text("#")
        (tmp_path / "core" / "models.py").write_text(
            "class User:\n    pass\n\nclass Task:\n    pass\n"
        )
        (tmp_path / "core" / "routes.py").write_text(
            "from fastapi import APIRouter\nrouter = APIRouter()\n@router.get('/')\ndef h(): pass\n"
        )
        (tmp_path / "docs" / "SDD").mkdir(parents=True)
        (tmp_path / "docs" / "SDD" / "arch.md").write_text(
            "# Architecture\nentity Project\nentity Task\n"
        )

        pa = ProjectAdapter()
        gate = BootstrapGateV2(adapter=pa, project_root=tmp_path)
        result = gate.validate()

        # Should have high confidence (Python, FastAPI, DynamoDB, AWS, modules>0, ontology)
        assert result.score >= 0.5
        assert len(result.issues) == 0

    def test_validate_with_real_meupdi(self):
        """V10: discover(meu-pdi/backend/) → validate → passed, score >= 0.5."""
        backend = Path("/mnt/c/repo/meu-pdi/backend")
        if not backend.exists():
            pytest.skip("Meu PDI backend not found at /mnt/c/repo/meu-pdi/backend")

        pa = ProjectAdapter()
        gate = BootstrapGateV2(adapter=pa, project_root=backend)
        result = gate.validate()
        report = gate.report()

        assert gate.profile.language == "Python"
        assert gate.profile.framework == "FastAPI"
        assert gate.profile.cloud_provider == "AWS"
        assert result.score >= 0.5
        # Meu PDI has no ontology (has_ontology=False), so there may be warnings
        # but confidence should still be high enough to pass
        assert "Python" in report
        assert "FastAPI" in report


# =============================================================================
# Coverage edge cases: fallback confidence, internal helpers
# =============================================================================


class TestCoverageEdgeCases:
    """Tests to push coverage of gate_v2.py to ≥80%."""

    def test_fallback_confidence_framework_database(self):
        """_fallback_confidence: framework + database filled."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="PostgreSQL",
            cloud_provider="unknown",
            module_count=0,
            architecture_patterns=[],
            has_ontology=False,
        )
        gate = BootstrapGateV2(profile=profile)
        confidence = gate._fallback_confidence()
        # 3/6 filled (language, framework, database) → 0.50
        assert confidence == 0.5

    def test_fallback_confidence_all_filled(self):
        """_fallback_confidence: all fields filled → 1.0."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="PostgreSQL",
            cloud_provider="AWS",
            module_count=5,
            architecture_patterns=["fastapi_routes"],
            has_ontology=True,
        )
        gate = BootstrapGateV2(profile=profile)
        confidence = gate._fallback_confidence()
        assert confidence == 1.0

    def test_fallback_confidence_empty(self):
        """_fallback_confidence: all unknown/zero → 0.0."""
        profile = ProjectProfile()
        gate = BootstrapGateV2(profile=profile)
        confidence = gate._fallback_confidence()
        assert confidence == 0.0

    def test_compute_confidence_uses_confidence_method(self):
        """_compute_confidence delegates to ProjectAdapter._calculate_confidence."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            cloud_provider="AWS",
            module_count=3,
            architecture_patterns=["fastapi_routes"],
            has_ontology=True,
            domain_entities=["User"],
            detector_results={
                "stack": {"language": "Python"},
                "modules": {"module_count": 3},
                "patterns": {"architecture_patterns": ["fastapi_routes"]},
                "semantic": {"has_ontology": True, "domain_entities": ["User"]},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        confidence = gate._compute_confidence()
        assert confidence > 0.0
        assert confidence <= 1.0

    def test_save_config_default_path(self, tmp_path: Path):
        """save_config with default path argument."""
        profile = ProjectProfile(
            language="Python",
            framework="FastAPI",
            database="DynamoDB",
            has_ontology=True,
            detector_results={
                "stack": {"language": "Python", "framework": "FastAPI"},
                "semantic": {"has_ontology": True},
            },
        )
        gate = BootstrapGateV2(profile=profile)
        orig_cwd = Path.cwd()
        try:
            import os
            os.chdir(str(tmp_path))
            saved = gate.save_config()
            assert Path("APOS_CONFIG.yaml").exists()
            assert Path(saved).exists()
            content = Path("APOS_CONFIG.yaml").read_text()
            assert "language: Python" in content
        finally:
            os.chdir(str(orig_cwd))
