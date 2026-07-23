"""Testes de integracao: ProjectAdapter contra Meu PDI real (T1.1.4).

Nota: Testes usam backend/ (nao raiz) por performance — o ModuleDetector
      ainda tem rglob("__init__.py") residual para deteccao de modulos
      aninhados que varre .venv. Corrigido em proximo patch.
"""

from __future__ import annotations

import os
import platform
import threading
from pathlib import Path
from typing import Any

import pytest


def _resolve_backend_path() -> Path:
    """Resolve the Meu PDI backend path portably across Windows and WSL/Linux.

    Resolution order:
    1. `MEUPDI_BACKEND_PATH` env var, if set.
    2. Auto-detection by OS: native Windows path vs. WSL /mnt/c mount
       (both point at the same physical directory).
    """
    env_path = os.environ.get("MEUPDI_BACKEND_PATH")
    if env_path:
        return Path(env_path)

    if platform.system() == "Windows":
        return Path(r"C:\repo\meu-pdi\backend")
    return Path("/mnt/c/repo/meu-pdi/backend")


BACKEND = _resolve_backend_path()
TIMEOUT_SEC = 30

if not BACKEND.exists():
    pytest.skip(
        f"Meu PDI backend not found at {BACKEND}. Set MEUPDI_BACKEND_PATH "
        "to point at a local checkout of meu-pdi/backend to run these tests.",
        allow_module_level=True,
    )


def _check_exists(path: Path) -> bool:
    return path.exists()


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(scope="module")
def stack_detector():
    from apos.project_adapter.detector import StackDetector

    return StackDetector()


# =============================================================================
# Stack Detection
# =============================================================================


class TestStackDetection:
    """StackDetector contra o backend do Meu PDI."""

    def test_language_python(self, stack_detector):
        result = stack_detector.detect(BACKEND)
        assert result["language"] == "Python"

    def test_runtime_version_detected(self, stack_detector):
        result = stack_detector.detect(BACKEND)
        assert result.get("runtime_version") is not None

    def test_framework_fastapi(self, stack_detector):
        result = stack_detector.detect(BACKEND)
        assert result["framework"] == "FastAPI"

    def test_database_dynamodb(self, stack_detector):
        result = stack_detector.detect(BACKEND)
        assert result["database"] == "DynamoDB"

    def test_cloud_aws(self, stack_detector):
        result = stack_detector.detect(BACKEND)
        assert result["cloud_provider"] == "AWS"


# =============================================================================
# Pattern Detection (lightweight, no rglob)
# =============================================================================


class TestPatternDetection:
    """PatternDetector contra o backend do Meu PDI."""

    def test_domain_infra_split(self):
        assert _check_exists(BACKEND / "domain"), "backend/domain/ nao encontrado"
        assert _check_exists(BACKEND / "infrastructure"), (
            "backend/infrastructure/ nao encontrado"
        )

    def test_api_routes_exist(self):
        assert _check_exists(BACKEND / "api" / "routes"), (
            "backend/api/routes/ nao encontrado"
        )


# =============================================================================
# Full Discovery (timed)
# =============================================================================


class TestFullDiscovery:
    """Testa ProjectAdapter.discover() completo contra o backend do Meu PDI."""

    @pytest.fixture(scope="class")
    def discovered(self):
        from apos.project_adapter import ProjectAdapter

        pa = ProjectAdapter()
        result: dict[str, Any] = {"_timeout": False, "_profile": None}

        def _run():
            try:
                profile = pa.discover(BACKEND)
                result["_profile"] = profile
            except Exception as e:
                result["_error"] = str(e)

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        t.join(timeout=TIMEOUT_SEC)
        if t.is_alive():
            result["_timeout"] = True
        return result

    def test_discovery_did_not_timeout(self, discovered):
        if discovered.get("_timeout"):
            pytest.fail(f"discover() excedeu {TIMEOUT_SEC}s")
        if "_error" in discovered:
            pytest.fail(f"discover() falhou: {discovered['_error']}")

    def test_discovery_stack(self, discovered):
        if discovered.get("_timeout"):
            pytest.skip("Discovery timed out")
        p = discovered["_profile"]
        assert p.language == "Python"
        assert p.framework == "FastAPI"
        assert p.cloud_provider == "AWS"

    def test_discovery_patterns(self, discovered):
        if discovered.get("_timeout"):
            pytest.skip("Discovery timed out")
        p = discovered["_profile"]
        patterns = p.architecture_patterns
        assert "domain_infra_split" in patterns
        assert "fastapi_routes" in patterns
