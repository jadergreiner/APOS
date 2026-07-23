"""Testes para o ProjectCache — 6 cenarios obrigatorios.

Cenarios:
  CACHE-001: Cache hit retorna profile sem executar detectores
  CACHE-002: Cache miss executa discover e armazena
  CACHE-003: TTL expirado forca novo discover
  CACHE-004: Hash mismatch (pyproject.toml alterado) invalida cache
  CACHE-005: Cache corrompido (JSON invalido) faz fallback graceful
  CACHE-006: Cache vazio (0 bytes) comporta como miss
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from apos.project_adapter import ProjectAdapter, ProjectCache, ProjectProfile


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def cache() -> ProjectCache:
    """Cache com TTL padrao de 1 hora."""
    return ProjectCache()


@pytest.fixture
def sample_profile() -> ProjectProfile:
    """Profile minimo para testes de cache."""
    return ProjectProfile(
        language="Python",
        framework="FastAPI",
        detector_results={"stack": {"language": "Python", "framework": "FastAPI"}},
    )


@pytest.fixture
def project_with_pyproject(tmp_path: Path) -> Path:
    """Cria um diretorio de projeto com pyproject.toml."""
    root = tmp_path / "myproject"
    root.mkdir()
    (root / "pyproject.toml").write_text(
        '[project]\nname = "test"\ndependencies = ["fastapi"]\n',
        encoding="utf-8",
    )
    return root


# =============================================================================
# CACHE-001: Cache hit retorna profile sem executar detectores
# =============================================================================


class TestCacheHit:
    """Cache hit — profile salvo e carregado com sucesso."""

    def test_save_and_load(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Salva e carrega o profile — caminho feliz."""
        cache.save(sample_profile, project_with_pyproject)
        loaded = cache.load(project_with_pyproject)
        assert loaded is not None
        assert loaded.language == "Python"
        assert loaded.framework == "FastAPI"
        assert loaded.detector_results == sample_profile.detector_results

    def test_cache_file_created(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Verifica que o arquivo JSON foi criado no disco."""
        cache.save(sample_profile, project_with_pyproject)
        cache_file = project_with_pyproject / ".apos_cache" / "project_cache.json"
        assert cache_file.exists()
        raw = cache_file.read_text(encoding="utf-8")
        assert "profile" in raw
        assert "timestamp" in raw
        assert "pyproject_hash" in raw

    def test_is_valid_after_save(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """is_valid() retorna True apos save."""
        cache.save(sample_profile, project_with_pyproject)
        assert cache.is_valid(project_with_pyproject) is True

    def test_is_valid_before_save(self, cache: ProjectCache, project_with_pyproject: Path):
        """is_valid() retorna False antes de qualquer save."""
        assert cache.is_valid(project_with_pyproject) is False


# =============================================================================
# CACHE-002: Cache miss executa discover e armazena
# =============================================================================


class TestCacheMiss:
    """Cache miss — descobre e armazena."""

    def test_load_returns_none_on_empty(self, cache: ProjectCache, project_with_pyproject: Path):
        """Cache miss quando nao ha arquivo de cache."""
        loaded = cache.load(project_with_pyproject)
        assert loaded is None

    def test_discover_and_store(self, cache: ProjectCache, project_with_pyproject: Path):
        """Descobre via adapter, salva no cache, carrega depois."""
        adapter = ProjectAdapter()
        profile = adapter.discover(project_with_pyproject)
        assert profile.language == "Python"

        cache.save(profile, project_with_pyproject)
        loaded = cache.load(project_with_pyproject)
        assert loaded is not None
        assert loaded.language == "Python"
        assert loaded.framework == "FastAPI"

    def test_cache_miss_then_hit(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Miss → descobre e salva → hit."""
        # Miss
        assert cache.load(project_with_pyproject) is None
        # Save
        cache.save(sample_profile, project_with_pyproject)
        # Hit
        assert cache.load(project_with_pyproject) is not None


# =============================================================================
# CACHE-003: TTL expirado forca novo discover
# =============================================================================


class TestTTLExpired:
    """TTL expirado faz load retornar None."""

    def test_ttl_not_expired(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Cache valido dentro do TTL."""
        cache.save(sample_profile, project_with_pyproject)
        assert cache.load(project_with_pyproject) is not None

    def test_ttl_short_expires(self, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """TTL de 0 segundos expira imediatamente."""
        short_cache = ProjectCache(ttl=0)
        short_cache.save(sample_profile, project_with_pyproject)
        assert short_cache.load(project_with_pyproject) is None

    @pytest.mark.skip(reason="time.sleep(1) e muito lento; testado via ttl=0 acima")
    def test_ttl_one_second(self, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """TTL de 1 segundo expira apos espera."""
        cache = ProjectCache(ttl=1)
        cache.save(sample_profile, project_with_pyproject)
        assert cache.load(project_with_pyproject) is not None
        time.sleep(1.1)
        assert cache.load(project_with_pyproject) is None

    def test_ttl_negative_raises(self):
        """TTL negativo deve levantar erro."""
        with pytest.raises(ValueError, match="TTL must be non-negative"):
            ProjectCache(ttl=-1)

    def test_ttl_expired_by_timestamp_manipulation(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Simula TTL expirado manipulando o timestamp no JSON."""
        cache.save(sample_profile, project_with_pyproject)
        cache_file = project_with_pyproject / ".apos_cache" / "project_cache.json"
        data = json.loads(cache_file.read_text(encoding="utf-8"))
        # Poem timestamp 2 horas atras
        old_time = (datetime.now() - timedelta(hours=2)).isoformat()
        data["timestamp"] = old_time
        cache_file.write_text(json.dumps(data), encoding="utf-8")
        assert cache.load(project_with_pyproject) is None

    def test_ttl_default_value(self):
        """TTL default deve ser 3600 segundos (1 hora)."""
        c = ProjectCache()
        assert c.ttl == 3600
        assert c.ttl_timedelta == timedelta(seconds=3600)

    def test_ttl_custom_value(self):
        """TTL customizado deve ser respeitado."""
        c = ProjectCache(ttl=7200)
        assert c.ttl == 7200
        assert c.ttl_timedelta == timedelta(seconds=7200)


# =============================================================================
# CACHE-004: Hash mismatch (pyproject.toml alterado) invalida cache
# =============================================================================


class TestHashMismatch:
    """Hash mismatch quando pyproject.toml muda."""

    def test_hash_mismatch_invalidates(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """Alterar pyproject.toml depois do save invalida o cache."""
        cache.save(sample_profile, project_with_pyproject)
        # Modifica o pyproject.toml
        (project_with_pyproject / "pyproject.toml").write_text(
            '[project]\nname = "changed"\ndependencies = ["django"]\n',
            encoding="utf-8",
        )
        assert cache.load(project_with_pyproject) is None

    def test_hash_unchanged_valid(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """pyproject.toml inalterado mantem o cache valido."""
        cache.save(sample_profile, project_with_pyproject)
        # Nao modifica nada
        assert cache.load(project_with_pyproject) is not None

    def test_hash_no_pyproject_uses_empty(self, cache: ProjectCache, tmp_path: Path, sample_profile: ProjectProfile):
        """Projeto sem pyproject.toml usa hash vazio (consistente)."""
        root = tmp_path / "nopyproject"
        root.mkdir()
        cache.save(sample_profile, root)
        assert cache.load(root) is not None

    def test_hash_add_pyproject_after_save(self, cache: ProjectCache, tmp_path: Path, sample_profile: ProjectProfile):
        """Adicionar pyproject.toml depois do save altera o hash."""
        root = tmp_path / "addpyproject"
        root.mkdir()
        cache.save(sample_profile, root)
        # Agora adiciona pyproject.toml — hash muda de "" para algo
        (root / "pyproject.toml").write_text(
            '[project]\nname = "new"\n',
            encoding="utf-8",
        )
        assert cache.load(root) is None


# =============================================================================
# CACHE-005: Cache corrompido (JSON invalido) faz fallback graceful
# =============================================================================


class TestCorruptedCache:
    """Cache corrompido trata como miss."""

    def test_invalid_json(self, cache: ProjectCache, project_with_pyproject: Path):
        """JSON mal formatado retorna None."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text(
            "{isto nao e json valido!!!}", encoding="utf-8"
        )
        assert cache.load(project_with_pyproject) is None

    def test_partial_json(self, cache: ProjectCache, project_with_pyproject: Path):
        """JSON truncado retorna None."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text(
            '{"profile": {"language": "Python"', encoding="utf-8"
        )
        assert cache.load(project_with_pyproject) is None

    def test_json_without_profile_key(self, cache: ProjectCache, project_with_pyproject: Path):
        """JSON valido sem chave 'profile' retorna None."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text(
            json.dumps({"foo": "bar"}), encoding="utf-8"
        )
        assert cache.load(project_with_pyproject) is None

    def test_json_without_timestamp(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """JSON sem timestamp retorna None."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text(
            json.dumps({"profile": sample_profile.model_dump(), "pyproject_hash": ""}),
            encoding="utf-8",
        )
        assert cache.load(project_with_pyproject) is None


# =============================================================================
# CACHE-006: Cache vazio (0 bytes) comporta como miss
# =============================================================================


class TestEmptyCache:
    """Cache vazio (0 bytes) tratado como miss."""

    def test_empty_file_is_miss(self, cache: ProjectCache, project_with_pyproject: Path):
        """Arquivo de cache vazio retorna None."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text("", encoding="utf-8")
        assert cache.load(project_with_pyproject) is None

    def test_whitespace_only_is_invalid(self, cache: ProjectCache, project_with_pyproject: Path):
        """Arquivo com apenas espacos em branco trata como corrompido."""
        cache_dir = project_with_pyproject / ".apos_cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "project_cache.json").write_text("   \n  \n  ", encoding="utf-8")
        assert cache.load(project_with_pyproject) is None


# =============================================================================
# Invalidate
# =============================================================================


class TestInvalidate:
    """Invalidacao manual do cache."""

    def test_invalidate_removes_cache(self, cache: ProjectCache, project_with_pyproject: Path, sample_profile: ProjectProfile):
        """invalidate() remove o arquivo de cache."""
        cache.save(sample_profile, project_with_pyproject)
        assert cache.load(project_with_pyproject) is not None
        cache.invalidate(project_with_pyproject)
        assert cache.load(project_with_pyproject) is None
        cache_file = project_with_pyproject / ".apos_cache" / "project_cache.json"
        assert not cache_file.exists()

    def test_invalidate_nonexistent(self, cache: ProjectCache, project_with_pyproject: Path):
        """invalidate() em cache inexistente nao levanta erro."""
        cache.invalidate(project_with_pyproject)  # nao deve lancar excecao


# =============================================================================
# Cache directory name customizado
# =============================================================================


class TestCustomCacheDir:
    """Cache com nome de diretorio customizado."""

    def test_custom_cache_dir_name(self, tmp_path: Path, sample_profile: ProjectProfile):
        """Usa nome de diretorio customizado."""
        cache = ProjectCache(cache_dir_name=".mycache")
        root = tmp_path / "customdir"
        root.mkdir()
        cache.save(sample_profile, root)
        assert (root / ".mycache" / "project_cache.json").exists()
        assert cache.load(root) is not None

    def test_default_cache_dir_name(self):
        """Nome padrao do diretorio de cache."""
        c = ProjectCache()
        assert c.cache_dir_name == ".apos_cache"
