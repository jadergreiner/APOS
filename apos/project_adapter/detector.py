"""Detectores para descobrir contexto do projeto hospedeiro.

Cada detector examina o filesystem local e retorna um dicionario
com informacoes especificas do dominio.
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


IGNORE_DIRS = frozenset({"node_modules", "venv", ".venv", ".git", "__pycache__", ".mypy_cache", ".pytest_cache", "dist", "build", ".tox", "eggs", ".eggs", "env"})


class Detector(ABC):
    """Base abstrata para todos os detectores."""

    name: str = ""

    @abstractmethod
    def detect(self, project_root: Path) -> dict[str, Any]:
        """Executa a deteccao no diretorio do projeto."""
        ...


class StackDetector(Detector):
    """Detecta linguagem, framework, database e cloud provider."""

    name = "stack"

    def detect(self, project_root: Path) -> dict[str, Any]:
        result: dict[str, Any] = {
            "language": "unknown",
            "framework": "unknown",
            "database": "unknown",
            "cloud_provider": "unknown",
            "runtime_version": None,
        }

        pyproject = project_root / "pyproject.toml"
        package_json = project_root / "package.json"
        requirements = project_root / "requirements.txt"
        dockerfile = project_root / "Dockerfile"
        setup_py = project_root / "setup.py"

        # --- pyproject.toml ---
        if pyproject.exists():
            result["language"] = "Python"
            content = pyproject.read_text(encoding="utf-8", errors="replace")

            # Try to extract runtime version from requires-python
            m = re.search(r'requires-python\s*=\s*["\']([^"\']+)["\']', content)
            if m:
                result["runtime_version"] = m.group(1)

            # Detect framework/database from dependencies
            deps_lower = content.lower()

            if "fastapi" in deps_lower:
                result["framework"] = "FastAPI"
            elif "django" in deps_lower:
                result["framework"] = "Django"
            elif "flask" in deps_lower:
                result["framework"] = "Flask"
            elif "starlette" in deps_lower:
                result["framework"] = "Starlette"

            if "boto3" in deps_lower or "boto" in deps_lower:
                result["cloud_provider"] = "AWS"
            if "psycopg" in deps_lower or "asyncpg" in deps_lower:
                result["database"] = "PostgreSQL"
            elif "sqlalchemy" in deps_lower:
                result["database"] = result.get("database") or "SQLAlchemy"
            elif "pymongo" in deps_lower or "motor" in deps_lower:
                result["database"] = "MongoDB"

        # --- package.json ---
        if package_json.exists():
            result["language"] = result["language"] if result["language"] != "unknown" else "JavaScript"
            content = package_json.read_text(encoding="utf-8", errors="replace")
            deps_lower = content.lower()

            if "next" in deps_lower:
                result["framework"] = "Next.js"
            elif "react" in deps_lower:
                result["framework"] = result.get("framework") if result.get("framework") != "unknown" else "React"
            elif "express" in deps_lower:
                result["framework"] = "Express"
            elif "vue" in deps_lower:
                result["framework"] = "Vue.js"

            if result["language"] == "JavaScript":
                m = re.search(r'"node"\s*:\s*"[^0-9]*([0-9.]+)"', content)
                if m:
                    result["runtime_version"] = m.group(1)
                if "typescript" in content.lower():
                    result["language"] = "TypeScript"

        # --- requirements.txt ---
        if requirements.exists() and result["language"] == "unknown":
            result["language"] = "Python"

        # --- Dockerfile ---
        if dockerfile.exists():
            content = dockerfile.read_text(encoding="utf-8", errors="replace")
            for line in content.splitlines():
                line_lower = line.lower().strip()
                if line_lower.startswith("from"):
                    for lang in ("python", "node", "golang", "ruby", "php", "rust"):
                        if lang in line_lower:
                            if result["language"] == "unknown":
                                result["language"] = lang.capitalize()
                            break
                    # Check for cloud base images
                    for cloud in ("amazonlinux", "aws", "gcr", "gcloud", "azure"):
                        if cloud in line_lower:
                            if cloud in ("amazonlinux", "aws"):
                                result["cloud_provider"] = "AWS"
                            elif cloud in ("gcr", "gcloud"):
                                result["cloud_provider"] = "GCP"
                            elif "azure" in cloud:
                                result["cloud_provider"] = "Azure"
                            break

        # --- setup.py ---
        if setup_py.exists() and result["language"] == "unknown":
            result["language"] = "Python"

        return result


class ModuleDetector(Detector):
    """Detecta estrutura de modulos do projeto."""

    name = "modules"

    def detect(self, project_root: Path) -> dict[str, Any]:
        result: dict[str, Any] = {
            "module_count": 0,
            "core_modules": [],
            "directory_layout": "flat",
            "total_loc": 0,
        }

        # Scan top-level subdirectories for core modules (dirs with __init__.py)
        core_modules: list[str] = []
        total_loc = 0

        try:
            for entry in sorted(project_root.iterdir()):
                if entry.name.startswith("."):
                    continue
                if entry.name in IGNORE_DIRS:
                    continue
                if entry.is_dir() and (entry / "__init__.py").exists():
                    core_modules.append(entry.name)

            # Count total LOC in .py files (non-recursive in root, recursive in modules)
            py_files = list(project_root.rglob("*.py"))
            for pyf in py_files:
                # Skip files inside ignored dirs
                rel = pyf.relative_to(project_root)
                if any(part in IGNORE_DIRS for part in rel.parts):
                    continue
                try:
                    text = pyf.read_text(encoding="utf-8", errors="replace")
                    total_loc += text.count("\n") + 1
                except Exception:
                    pass

            result["module_count"] = len(core_modules)
            result["core_modules"] = core_modules

            # Determine directory layout
            has_nested_modules = False
            has_monorepo_hints = False
            for entry in sorted(project_root.iterdir()):
                if entry.name.startswith("."):
                    continue
                if entry.name in IGNORE_DIRS:
                    continue
                if entry.is_dir():
                    # Check if any subdir has __init__.py (nested python modules)
                    sub_inits = list(entry.rglob("__init__.py"))
                    if len(sub_inits) > 1:
                        has_nested_modules = True
                    # Monorepo hints: packages/ or apps/ directory
                    if entry.name in ("packages", "apps", "services"):
                        has_monorepo_hints = True

            if has_monorepo_hints:
                result["directory_layout"] = "monorepo"
            elif has_nested_modules or len(core_modules) > 3:
                result["directory_layout"] = "nested"
            else:
                result["directory_layout"] = "flat"

            result["total_loc"] = total_loc

        except PermissionError:
            pass

        return result


class PatternDetector(Detector):
    """Detecta padroes arquiteturais conhecidos no codigo."""

    name = "patterns"

    def detect(self, project_root: Path) -> dict[str, Any]:
        result: dict[str, Any] = {
            "architecture_patterns": [],
            "detected_patterns": [],
        }

        patterns: list[str] = []

        # --- domain/infra split ---
        backend = project_root / "backend"
        if backend.is_dir():
            has_domain = (backend / "domain").is_dir()
            has_infra = (backend / "infrastructure").is_dir()
        else:
            has_domain = (project_root / "domain").is_dir()
            has_infra = (project_root / "infrastructure").is_dir()
        if has_domain and has_infra:
            patterns.append("domain_infra_split")

        # --- clean architecture ---
        has_entities = any(
            p.name == "entities" and p.is_dir()
            for p in project_root.iterdir()
            if not p.name.startswith(".") and p.name not in IGNORE_DIRS
        )
        has_use_cases = any(
            p.name in ("use_cases", "usecases", "use-cases") and p.is_dir()
            for p in project_root.iterdir()
            if not p.name.startswith(".") and p.name not in IGNORE_DIRS
        )
        if has_entities and has_use_cases:
            patterns.append("clean_architecture")

        # --- FastAPI routes ---
        fastapi_pattern = re.compile(
            r"@\w*\.?(get|post|put|delete|patch|router\.get|router\.post|router\.put|router\.delete|router\.patch)"
        )
        for py_file in project_root.rglob("*.py"):
            rel = py_file.relative_to(project_root)
            if any(part in IGNORE_DIRS for part in rel.parts):
                continue
            try:
                text = py_file.read_text(encoding="utf-8", errors="replace")
                if fastapi_pattern.search(text):
                    patterns.append("fastapi_routes")
                    break
            except Exception:
                continue

        # --- Lambda handlers ---
        lambda_pattern = re.compile(r"def lambda_handler\s*\(|from\s+aws_lambda|boto3")
        for py_file in project_root.rglob("*.py"):
            rel = py_file.relative_to(project_root)
            if any(part in IGNORE_DIRS for part in rel.parts):
                continue
            try:
                text = py_file.read_text(encoding="utf-8", errors="replace")
                if lambda_pattern.search(text):
                    patterns.append("lambda_handlers")
                    break
            except Exception:
                continue

        # --- DynamoDB (single-table pattern via boto3 references) ---
        dynamodb_pattern = re.compile(r"boto3\.resource\(.*['\"]dynamodb['\"]|boto3\.client\(.*['\"]dynamodb['\"]|dynamodb|table\.get_item|table\.put_item|table\.query")
        for py_file in project_root.rglob("*.py"):
            rel = py_file.relative_to(project_root)
            if any(part in IGNORE_DIRS for part in rel.parts):
                continue
            try:
                text = py_file.read_text(encoding="utf-8", errors="replace")
                if dynamodb_pattern.search(text):
                    patterns.append("dynamodb_single_table")
                    break
            except Exception:
                continue

        result["architecture_patterns"] = patterns
        result["detected_patterns"] = list(patterns)

        return result


class SemanticDetector(Detector):
    """Detecta contexto semantico: documentacao, ontologia, convencoes."""

    name = "semantic"

    def detect(self, project_root: Path) -> dict[str, Any]:
        result: dict[str, Any] = {
            "has_ontology": False,
            "domain_entities": [],
            "naming_convention": "unknown",
        }

        # --- Ontology check ---
        docs_sdd = project_root / "docs" / "SDD"
        has_ontology = docs_sdd.is_dir()
        if not has_ontology:
            # Broader: any */ontology* file or dir
            for p in project_root.rglob("*"):
                if p.name.startswith("."):
                    continue
                if any(part in IGNORE_DIRS for part in p.relative_to(project_root).parts):
                    continue
                if "ontology" in p.name.lower() and p.is_file():
                    has_ontology = True
                    break

        result["has_ontology"] = has_ontology

        # --- Domain entities from SDD files ---
        domain_entities: list[str] = []
        if docs_sdd.is_dir():
            for sdd_file in sorted(docs_sdd.rglob("*.md")):
                try:
                    text = sdd_file.read_text(encoding="utf-8", errors="replace")
                    # Extract class/entity definitions
                    for m in re.finditer(
                        r"(?:class|entity|schema|model|interface)\s+([A-Za-z_]\w*)",
                        text,
                    ):
                        entity_name = m.group(1)
                        if entity_name not in domain_entities:
                            domain_entities.append(entity_name)
                except Exception:
                    continue

        # Also check NORTH_STAR.md, CAPABILITIES.md for entity references
        for doc_name in ("NORTH_STAR.md", "CAPABILITIES.md", "ONTOLOGY.md", "ontology.md"):
            doc_file = project_root / doc_name
            if doc_file.exists():
                try:
                    text = doc_file.read_text(encoding="utf-8", errors="replace")
                    for m in re.finditer(
                        r"(?:class|entity|schema|model|interface)\s+([A-Za-z_]\w*)",
                        text,
                    ):
                        entity_name = m.group(1)
                        if entity_name not in domain_entities:
                            domain_entities.append(entity_name)
                except Exception:
                    continue

        result["domain_entities"] = domain_entities

        # --- Naming convention sampling ---
        py_files = [
            p
            for p in project_root.rglob("*.py")
            if not any(part in IGNORE_DIRS for part in p.relative_to(project_root).parts)
        ]
        if py_files:
            snake_count = 0
            camel_count = 0
            pascal_count = 0
            samples = 0

            for pyf in py_files[:20]:  # Sample up to 20 files
                try:
                    text = pyf.read_text(encoding="utf-8", errors="replace")
                    for line in text.splitlines():
                        line = line.strip()
                        if line.startswith("#") or line.startswith('"') or line.startswith("'"):
                            continue
                        # Look for function/class defs and variable assignments
                        for token in re.findall(r"(?:def |class |@\w+\.)?([a-zA-Z_]\w*)\s*(?:\(|=|:)", line):
                            if "_" in token and token == token.lower():
                                snake_count += 1
                            elif token and token[0].isupper() and "_" not in token:
                                pascal_count += 1
                            elif token and token[0].islower() and token != token.lower() and "_" not in token:
                                camel_count += 1
                            samples += 1
                except Exception:
                    continue

            if samples > 0:
                if snake_count > camel_count and snake_count > pascal_count:
                    result["naming_convention"] = "snake_case"
                elif pascal_count > snake_count and pascal_count > camel_count:
                    result["naming_convention"] = "PascalCase"
                elif camel_count > snake_count and camel_count > pascal_count:
                    result["naming_convention"] = "camelCase"
                else:
                    result["naming_convention"] = "snake_case"  # Python default

        return result
