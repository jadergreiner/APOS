"""ProjectAdapter — descobre contexto do projeto hospedeiro."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel

from apos.project_adapter.detector import (
    Detector,
    ModuleDetector,
    PatternDetector,
    SemanticDetector,
    StackDetector,
)
from apos.project_adapter.errors import DetectorExecutionError


class ProjectProfile(BaseModel):
    """Perfil completo do projeto descoberto pelos detectores."""

    # Stack
    language: str = "unknown"
    framework: str = "unknown"
    database: str = "unknown"
    cloud_provider: str = "unknown"
    runtime_version: Optional[str] = None

    # Modulos
    module_count: int = 0
    core_modules: list[str] = []
    directory_layout: str = "flat"
    total_loc: int = 0

    # Padroes
    architecture_patterns: list[str] = []
    detected_patterns: list[str] = []

    # Semantica
    has_ontology: bool = False
    domain_entities: list[str] = []
    naming_convention: str = "unknown"

    # Raw
    detector_results: dict[str, dict] = {}


class ProjectAdapter:
    """Adaptador que coordena detectores para produzir um ProjectProfile."""

    def __init__(self) -> None:
        self._detectors: list[Detector] = [
            StackDetector(),
            ModuleDetector(),
            PatternDetector(),
            SemanticDetector(),
        ]

    def register_detector(self, detector: Detector) -> None:
        """Registra um detector customizado."""
        self._detectors.append(detector)

    def discover(self, project_root: str | Path) -> ProjectProfile:
        """Executa todos os detectores e retorna um perfil completo."""
        root = Path(project_root)
        if not root.exists():
            raise ValueError(f"Project root does not exist: {root}")

        results: dict[str, dict[str, Any]] = {}
        for detector in self._detectors:
            try:
                results[detector.name] = detector.detect(root)
            except DetectorExecutionError:
                raise
            except Exception as e:
                raise DetectorExecutionError(
                    f"Detector '{detector.name}' falhou: {e}"
                ) from e

        return self._build_profile(results)

    def analyze(self, project_root: str | Path) -> dict[str, Any]:
        """Retorna perfil + metrica de confianca."""
        profile = self.discover(project_root)
        return {
            "profile": profile.model_dump(),
            "confidence": self._calculate_confidence(profile),
        }

    def _build_profile(self, results: dict[str, dict[str, Any]]) -> ProjectProfile:
        stack = results.get("stack", {})
        modules = results.get("modules", {})
        patterns = results.get("patterns", {})
        semantic = results.get("semantic", {})

        return ProjectProfile(
            language=stack.get("language", "unknown"),
            framework=stack.get("framework", "unknown"),
            database=stack.get("database", "unknown"),
            cloud_provider=stack.get("cloud_provider", "unknown"),
            runtime_version=stack.get("runtime_version"),
            module_count=modules.get("module_count", 0),
            core_modules=modules.get("core_modules", []),
            directory_layout=modules.get("directory_layout", "flat"),
            total_loc=modules.get("total_loc", 0),
            architecture_patterns=patterns.get("architecture_patterns", []),
            detected_patterns=patterns.get("detected_patterns", []),
            has_ontology=semantic.get("has_ontology", False),
            domain_entities=semantic.get("domain_entities", []),
            naming_convention=semantic.get("naming_convention", "unknown"),
            detector_results=results,
        )

    def _calculate_confidence(self, profile: ProjectProfile) -> float:
        """Calcula um score de confianca (0.0 a 1.0) baseado em
        quantos campos foram preenchidos com valores nao-default."""
        total = 0
        filled = 0

        # language
        total += 1
        if profile.language != "unknown":
            filled += 1

        # framework
        total += 1
        if profile.framework != "unknown":
            filled += 1

        # database
        total += 1
        if profile.database != "unknown":
            filled += 1

        # modules
        total += 1
        if profile.module_count > 0:
            filled += 1

        # patterns
        total += 1
        if len(profile.architecture_patterns) > 0:
            filled += 1

        # ontology
        total += 1
        if profile.has_ontology:
            filled += 1

        return round(filled / total, 2) if total > 0 else 0.0
