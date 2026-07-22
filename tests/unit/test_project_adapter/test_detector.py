"""Testes para os detectores do project_adapter."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from apos.project_adapter.detector import (
    Detector,
    ModuleDetector,
    PatternDetector,
    SemanticDetector,
    StackDetector,
)
from apos.project_adapter.errors import DetectorExecutionError

# =============================================================================
# Detector ABC
# =============================================================================


def test_detector_abc_cannot_be_instantiated():
    """Detector ABC nao pode ser instanciada diretamente."""
    with pytest.raises(TypeError):
        Detector()  # type: ignore[abstract]


def test_detector_abc_has_abstract_method():
    """Detector exige implementacao de detect()."""
    with pytest.raises(TypeError):

        class Incomplete(Detector):
            name = "incomplete"

        Incomplete()


class ConcreteDetector(Detector):
    name = "concrete"

    def detect(self, project_root: Path) -> dict:
        return {"done": True}


def test_detector_concrete_can_be_instantiated():
    d = ConcreteDetector()
    assert d.name == "concrete"
    assert d.detect(Path(".")) == {"done": True}


# =============================================================================
# StackDetector
# =============================================================================


class TestStackDetector:
    def test_empty_dir_returns_unknowns(self, tmp_path: Path):
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] == "unknown"
        assert result["framework"] == "unknown"
        assert result["database"] == "unknown"
        assert result["cloud_provider"] == "unknown"
        assert result["runtime_version"] is None

    def test_pyproject_toml_fastapi(self, tmp_path: Path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "myapp"\nrequires-python = ">=3.11"\n'
            'dependencies = ["fastapi", "uvicorn", "boto3", "psycopg2-binary"]\n'
        )
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] == "Python"
        assert result["framework"] == "FastAPI"
        assert result["database"] == "PostgreSQL"
        assert result["cloud_provider"] == "AWS"
        assert result["runtime_version"] == ">=3.11"

    def test_pyproject_django(self, tmp_path: Path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(
            '[project]\nname = "myapp"\ndependencies = ["django", "djangorestframework"]\n'
        )
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["framework"] == "Django"

    def test_package_json_nextjs(self, tmp_path: Path):
        pkg = tmp_path / "package.json"
        pkg.write_text('{"dependencies": {"next": "14.0.0", "react": "18.0.0"}}\n')
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] in ("JavaScript", "TypeScript")
        assert result["framework"] == "Next.js"

    def test_package_json_express(self, tmp_path: Path):
        pkg = tmp_path / "package.json"
        pkg.write_text('{"dependencies": {"express": "^4.18.0"}}\n')
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["framework"] == "Express"

    def test_requirements_txt_only(self, tmp_path: Path):
        (tmp_path / "requirements.txt").write_text("requests\nflask\n")
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] == "Python"

    def test_dockerfile_python(self, tmp_path: Path):
        (tmp_path / "Dockerfile").write_text("FROM python:3.12-slim\n")
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] == "Python"

    def test_setup_py(self, tmp_path: Path):
        (tmp_path / "setup.py").write_text("from setuptools import setup\n")
        d = StackDetector()
        result = d.detect(tmp_path)
        assert result["language"] == "Python"


# =============================================================================
# ModuleDetector
# =============================================================================


class TestModuleDetector:
    def test_empty_dir(self, tmp_path: Path):
        d = ModuleDetector()
        result = d.detect(tmp_path)
        assert result["module_count"] == 0
        assert result["core_modules"] == []
        assert result["total_loc"] == 0

    def test_detects_core_modules(self, tmp_path: Path):
        (tmp_path / "apos").mkdir()
        (tmp_path / "apos" / "__init__.py").write_text("# apos")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "__init__.py").write_text("# tests")
        d = ModuleDetector()
        result = d.detect(tmp_path)
        assert result["module_count"] == 2
        assert "apos" in result["core_modules"]
        assert "tests" in result["core_modules"]

    def test_ignores_node_modules_venv_git(self, tmp_path: Path):
        for ignored in ("node_modules", "venv", ".git", "__pycache__"):
            (tmp_path / ignored).mkdir(exist_ok=True)
            (tmp_path / ignored / "__init__.py").write_text("# ignored")
        d = ModuleDetector()
        result = d.detect(tmp_path)
        assert result["module_count"] == 0

    def test_counts_loc(self, tmp_path: Path):
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "__init__.py").write_text("# src module\n")
        (tmp_path / "src" / "main.py").write_text("def main():\n    pass\n")
        d = ModuleDetector()
        result = d.detect(tmp_path)
        assert result["total_loc"] > 0

    def test_directory_layout_nested(self, tmp_path: Path):
        (tmp_path / "mod1").mkdir()
        (tmp_path / "mod1" / "__init__.py").write_text("")
        (tmp_path / "mod1" / "sub").mkdir()
        (tmp_path / "mod1" / "sub" / "__init__.py").write_text("")
        (tmp_path / "mod2").mkdir()
        (tmp_path / "mod2" / "__init__.py").write_text("")
        d = ModuleDetector()
        result = d.detect(tmp_path)
        # mod1 and mod2 = 2 core modules; mod1/sub = nested init
        assert result["directory_layout"] == "nested"


# =============================================================================
# PatternDetector
# =============================================================================


class TestPatternDetector:
    def test_no_patterns_in_empty_dir(self, tmp_path: Path):
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert result["architecture_patterns"] == []

    def test_domain_infra_split(self, tmp_path: Path):
        (tmp_path / "backend" / "domain").mkdir(parents=True)
        (tmp_path / "backend" / "infrastructure").mkdir(parents=True)
        (tmp_path / "backend" / "domain" / "__init__.py").write_text("")
        (tmp_path / "backend" / "infrastructure" / "__init__.py").write_text("")
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert "domain_infra_split" in result["architecture_patterns"]

    def test_clean_architecture(self, tmp_path: Path):
        (tmp_path / "entities").mkdir()
        (tmp_path / "use_cases").mkdir()
        (tmp_path / "entities" / "__init__.py").write_text("")
        (tmp_path / "use_cases" / "__init__.py").write_text("")
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert "clean_architecture" in result["architecture_patterns"]

    def test_fastapi_routes(self, tmp_path: Path):
        (tmp_path / "routes.py").write_text(
            "from fastapi import APIRouter\nrouter = APIRouter()\n\n@router.get('/')\nasync def root():\n    return {'ok': True}\n"
        )
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert "fastapi_routes" in result["architecture_patterns"]

    def test_lambda_handlers(self, tmp_path: Path):
        (tmp_path / "handler.py").write_text(
            "def lambda_handler(event, context):\n    return {'statusCode': 200}\n"
        )
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert "lambda_handlers" in result["architecture_patterns"]

    def test_dynamodb_pattern(self, tmp_path: Path):
        (tmp_path / "db.py").write_text(
            'import boto3\ntable = boto3.resource("dynamodb").Table("my-table")\n'
        )
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert "dynamodb_single_table" in result["architecture_patterns"]

    def test_no_false_positives(self, tmp_path: Path):
        (tmp_path / "readme.md").write_text("This is just a readme.\n")
        d = PatternDetector()
        result = d.detect(tmp_path)
        assert result["architecture_patterns"] == []


# =============================================================================
# SemanticDetector
# =============================================================================


class TestSemanticDetector:
    def test_no_ontology_in_empty_dir(self, tmp_path: Path):
        d = SemanticDetector()
        result = d.detect(tmp_path)
        assert result["has_ontology"] is False
        assert result["domain_entities"] == []
        assert result["naming_convention"] == "unknown"

    def test_detects_ontology_via_docs_sdd(self, tmp_path: Path):
        (tmp_path / "docs" / "SDD").mkdir(parents=True)
        (tmp_path / "docs" / "SDD" / "architecture.md").write_text(
            "# Architecture\nentity Project\nentity Profile\n"
        )
        d = SemanticDetector()
        result = d.detect(tmp_path)
        assert result["has_ontology"] is True
        assert "Project" in result["domain_entities"]
        assert "Profile" in result["domain_entities"]

    def test_detects_ontology_file(self, tmp_path: Path):
        (tmp_path / "ONTOLOGY.md").write_text("# Ontology\nmodel User\nmodel Task\n")
        d = SemanticDetector()
        result = d.detect(tmp_path)
        assert result["has_ontology"] is True
        assert "User" in result["domain_entities"]

    def test_naming_convention_snake_case(self, tmp_path: Path):
        (tmp_path / "module.py").write_text(
            "def my_function():\n    my_variable = 1\n    return my_variable\n"
        )
        d = SemanticDetector()
        result = d.detect(tmp_path)
        assert result["naming_convention"] == "snake_case"

    def test_naming_convention_pascal_case(self, tmp_path: Path):
        (tmp_path / "models.py").write_text(
            "class UserProfile:\n    def Validate(self):\n        pass\n"
        )
        d = SemanticDetector()
        result = d.detect(tmp_path)
        assert result["naming_convention"] == "PascalCase"
