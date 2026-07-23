"""ProjectCache — cache em disco para ProjectProfile.

Permite que o profile descoberto seja reutilizado entre sessoes
sem re-executar detectores, com suporte a TTL e validacao por hash.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from apos.project_adapter.adapter import ProjectProfile


class ProjectCache:
    """Cache em disco para ProjectProfile.

    Attributes:
        ttl: Tempo de vida do cache em segundos (default 3600 = 1h).
        cache_dir_name: Nome do diretorio de cache (default ".apos_cache").

    Usage:
        cache = ProjectCache()
        # Tenta carregar do cache
        profile = cache.load("/path/to/project")
        if profile is None:
            adapter = ProjectAdapter()
            profile = adapter.discover("/path/to/project")
            cache.save(profile, "/path/to/project")
    """

    _CACHE_FILENAME = "project_cache.json"

    def __init__(self, ttl: int = 3600, cache_dir_name: str = ".apos_cache") -> None:
        if ttl < 0:
            raise ValueError("TTL must be non-negative")
        self.ttl = ttl
        self.cache_dir_name = cache_dir_name

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def save(self, profile: ProjectProfile, project_root: str | Path) -> None:
        """Salva o profile em disco como JSON.

        Cria o diretorio de cache se necessario e inclui metadados
        (timestamp, hash do pyproject.toml) para validacao futura.

        Args:
            profile: ProjectProfile a ser cacheado.
            project_root: Diretorio raiz do projeto.
        """
        root = Path(project_root)
        cache_dir = root / self.cache_dir_name
        cache_dir.mkdir(parents=True, exist_ok=True)

        data = {
            "profile": profile.model_dump(),
            "timestamp": datetime.now().isoformat(),
            "pyproject_hash": self._compute_hash(root),
        }
        (cache_dir / self._CACHE_FILENAME).write_text(
            json.dumps(data, indent=2, default=str, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self, project_root: str | Path) -> Optional[ProjectProfile]:
        """Carrega o profile do cache se valido.

        Retorna None quando:
        - Cache nao existe (miss)
        - Cache esta corrompido ou vazio
        - TTL expirou
        - Hash do pyproject.toml mudou

        Nestes casos o chamador deve executar discover() e salvar o resultado.

        Args:
            project_root: Diretorio raiz do projeto.

        Returns:
            ProjectProfile se cache valido, None caso contrario.
        """
        root = Path(project_root)
        cache_file = root / self.cache_dir_name / self._CACHE_FILENAME

        if not cache_file.exists():
            return None

        # --- Arquivo vazio ---
        if cache_file.stat().st_size == 0:
            return None

        # --- JSON corrompido ---
        try:
            raw = cache_file.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError):
            return None

        # --- Estrutura invalida ---
        if not isinstance(data, dict) or "profile" not in data:
            return None

        # --- TTL expirado ---
        timestamp_str = data.get("timestamp")
        if timestamp_str:
            try:
                cached_time = datetime.fromisoformat(timestamp_str)
            except (ValueError, TypeError):
                return None
            elapsed = (datetime.now() - cached_time).total_seconds()
            if elapsed > self.ttl:
                return None
        else:
            return None

        # --- Hash mismatch (pyproject.toml alterado) ---
        cached_hash = data.get("pyproject_hash", "")
        current_hash = self._compute_hash(root)
        if cached_hash != current_hash:
            return None

        return ProjectProfile(**data["profile"])

    def invalidate(self, project_root: str | Path) -> None:
        """Remove o arquivo de cache do disco.

        Args:
            project_root: Diretorio raiz do projeto.
        """
        root = Path(project_root)
        cache_file = root / self.cache_dir_name / self._CACHE_FILENAME
        if cache_file.exists():
            cache_file.unlink()

    def is_valid(self, project_root: str | Path) -> bool:
        """Verifica se o cache existe e e valido sem carregar o profile.

        Args:
            project_root: Diretorio raiz do projeto.

        Returns:
            True se o cache existe e nao esta expirado/invalido.
        """
        return self.load(project_root) is not None

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_hash(project_root: Path) -> str:
        """Calcula SHA256 do pyproject.toml para detectar alteracoes.

        Retorna string vazia se o arquivo nao existir.

        Args:
            project_root: Diretorio raiz do projeto.

        Returns:
            Hex digest SHA256 ou string vazia.
        """
        pyproject = project_root / "pyproject.toml"
        if not pyproject.exists():
            return ""
        try:
            return hashlib.sha256(pyproject.read_bytes()).hexdigest()
        except (OSError, PermissionError):
            return ""

    @property
    def ttl_timedelta(self) -> timedelta:
        """Retorna o TTL como timedelta para uso em comparacoes."""
        return timedelta(seconds=self.ttl)
