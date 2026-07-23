"""Testes para US-002: CLI `apos context` — Injecao de Contexto Automatica.

Cenarios (4):
    CTX-001 (Happy): `apos context` com cache valido → markdown formatado
    CTX-002 (Edge):  `apos context` sem cache → mensagem clara
    CTX-003 (Edge):  Profile parcial → apenas campos preenchidos
    CTX-004 (Happy): Saida markdown parseavel
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from unittest.mock import ANY, AsyncMock, MagicMock, patch

import pytest

from apos.cli import _format_no_cache, _profile_to_markdown, main as cli_main
from apos.project_adapter import ProjectProfile


# =============================================================================
# Helpers
# =============================================================================


def _make_profile(
    language: str = "Python",
    framework: str = "FastAPI",
    database: str = "PostgreSQL",
    cloud_provider: str = "AWS",
    runtime_version: str | None = ">=3.11",
    module_count: int = 5,
    core_modules: list[str] | None = None,
    directory_layout: str = "nested",
    total_loc: int = 12345,
    architecture_patterns: list[str] | None = None,
    detected_patterns: list[str] | None = None,
    has_ontology: bool = True,
    domain_entities: list[str] | None = None,
    naming_convention: str = "snake_case",
) -> ProjectProfile:
    """Cria um ProjectProfile com valores customizaveis.
    
    Parametros com None usam defaults internos. Listas explicitamente
    vazias devem ser passadas como [] via kwargs.
    """
    return ProjectProfile(
        language=language,
        framework=framework,
        database=database,
        cloud_provider=cloud_provider,
        runtime_version=runtime_version,
        module_count=module_count,
        core_modules=core_modules if core_modules is not None else ["module_a", "module_b"],
        directory_layout=directory_layout,
        total_loc=total_loc,
        architecture_patterns=architecture_patterns if architecture_patterns is not None else ["fastapi_routes"],
        detected_patterns=detected_patterns if detected_patterns is not None else ["fastapi_routes"],
        has_ontology=has_ontology,
        domain_entities=domain_entities if domain_entities is not None else ["Project", "Sprint"],
        naming_convention=naming_convention,
    )


def _write_cache(
    cache_dir: Path,
    profile: ProjectProfile,
    pyproject_hash: str = "",
) -> Path:
    """Escreve um cache valido em disco."""
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = cache_dir / "project_cache.json"
    data = {
        "version": 1,
        "created_at": "2026-07-23T00:00:00",
        "profile": profile.model_dump(mode="json"),
        "pyproject_hash": pyproject_hash,
    }
    cache_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return cache_file


# =============================================================================
# Factory for cli_main test
# =============================================================================


@pytest.fixture
def mock_cache_hit():
    """Mocka ProjectCache.load() para retornar profile valido."""
    profile = _make_profile()
    with patch("apos.project_adapter.cache.ProjectCache") as MockCache:
        instance = MagicMock()
        instance.load = AsyncMock(return_value=(profile, "hit"))
        MockCache.return_value = instance
        yield MockCache, instance, profile


@pytest.fixture
def mock_cache_miss():
    """Mocka ProjectCache.load() para retornar cache miss."""
    with patch("apos.project_adapter.cache.ProjectCache") as MockCache:
        instance = MagicMock()
        instance.load = AsyncMock(return_value=(None, "miss"))
        MockCache.return_value = instance
        yield MockCache, instance


# =============================================================================
# CTX-001: Cache valido → markdown formatado
# =============================================================================


class TestCtx001CacheHit:
    """CTX-001 (Happy): `apos context` com cache valido → markdown formatado."""

    def test_returns_markdown_with_all_fields(self, mock_cache_hit):
        """Saida markdown contem todos os campos esperados."""
        exit_code = cli_main(["context"])
        assert exit_code == 0

    def test_output_contains_language(self, mock_cache_hit, capsys):
        """Markdown contem linguagem."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "Python" in captured.out

    def test_output_contains_framework(self, mock_cache_hit, capsys):
        """Markdown contem framework."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "FastAPI" in captured.out

    def test_output_contains_database(self, mock_cache_hit, capsys):
        """Markdown contem database."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "PostgreSQL" in captured.out

    def test_output_contains_cloud(self, mock_cache_hit, capsys):
        """Markdown contem cloud provider."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "AWS" in captured.out

    def test_output_contains_modules(self, mock_cache_hit, capsys):
        """Markdown contem modulos."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "module_a" in captured.out
        assert "module_b" in captured.out

    def test_output_contains_patterns(self, mock_cache_hit, capsys):
        """Markdown contem padroes."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "fastapi_routes" in captured.out

    def test_output_contains_heading(self, mock_cache_hit, capsys):
        """Markdown contem cabecalho."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "## Project Context" in captured.out

    def test_output_contains_table(self, mock_cache_hit, capsys):
        """Markdown contem tabela."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "| Campo | Valor |" in captured.out

    def test_output_terminator(self, mock_cache_hit, capsys):
        """Markdown termina com asterisco de autoria."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "*Contexto gerado automaticamente" in captured.out

    def test_output_includes_runtime(self, mock_cache_hit, capsys):
        """Markdown inclui runtime version quando disponivel."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert ">=3.11" in captured.out

    def test_output_includes_loc(self, mock_cache_hit, capsys):
        """Markdown inclui total_loc."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "12345" in captured.out


# =============================================================================
# CTX-002: Sem cache → mensagem clara
# =============================================================================


class TestCtx002NoCache:
    """CTX-002 (Edge): `apos context` sem cache → mensagem clara."""

    def test_exit_code_on_miss(self, mock_cache_miss):
        """Sem cache, codigo de saida deve ser 1."""
        exit_code = cli_main(["context"])
        assert exit_code == 1

    def test_message_contains_discover_hint(self, mock_cache_miss, capsys):
        """Mensagem deve sugerir `apos discover`."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "apos discover" in captured.out

    def test_message_contains_no_cache_warning(self, mock_cache_miss, capsys):
        """Mensagem deve indicar que nao ha cache."""
        cli_main(["context"])
        captured = capsys.readouterr()
        assert "Nao Disponivel" in captured.out or "Nenhum cache" in captured.out

    def test_no_cache_format_function(self):
        """_format_no_cache retorna markdown com hint."""
        result = _format_no_cache("Nenhum cache encontrado.")
        assert "## Project Context" in result
        assert "apos discover" in result
        assert "Nenhum cache" in result

    def test_expired_cache(self, capsys):
        """Cache expirado deve mostrar mensagem adequada."""
        with patch("apos.project_adapter.cache.ProjectCache") as MockCache:
            instance = MagicMock()
            instance.load = AsyncMock(return_value=(None, "expired"))
            MockCache.return_value = instance
            exit_code = cli_main(["context"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Cache expirado" in captured.out

    def test_hash_mismatch_cache(self, capsys):
        """Hash mismatch deve mostrar mensagem adequada."""
        with patch("apos.project_adapter.cache.ProjectCache") as MockCache:
            instance = MagicMock()
            instance.load = AsyncMock(return_value=(None, "hash_mismatch"))
            MockCache.return_value = instance
            exit_code = cli_main(["context"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "pyproject.toml foi modificado" in captured.out

    def test_corrupted_cache(self, capsys):
        """Cache corrompido deve mostrar mensagem adequada."""
        with patch("apos.project_adapter.cache.ProjectCache") as MockCache:
            instance = MagicMock()
            instance.load = AsyncMock(return_value=(None, "corrupted"))
            MockCache.return_value = instance
            exit_code = cli_main(["context"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "corrompido" in captured.out or "invalido" in captured.out


# =============================================================================
# CTX-003: Profile parcial → apenas campos preenchidos
# =============================================================================


class TestCtx003PartialProfile:
    """CTX-003 (Edge): Profile parcial → apenas campos preenchidos."""

    def test_partial_profile_omits_empty_modules(self, capsys):
        """Profile sem modulos nao deve exibir secao de modulos."""
        profile = _make_profile(
            module_count=0,
            core_modules=[],
            total_loc=0,
            architecture_patterns=[],
            detected_patterns=[],
            has_ontology=False,
            domain_entities=[],
        )
        md = _profile_to_markdown(profile)
        # Nao deve conter secoes vazias
        assert "Modulos" not in md
        assert "Padroes" not in md
        assert "Ontologia" not in md
        assert "Dominio" not in md

    def test_partial_profile_still_shows_stack(self, capsys):
        """Profile parcial ainda exibe stack basica."""
        profile = _make_profile(
            module_count=0,
            core_modules=[],
            total_loc=0,
            architecture_patterns=[],
            detected_patterns=[],
            has_ontology=False,
            domain_entities=[],
        )
        md = _profile_to_markdown(profile)
        assert "Python" in md
        assert "FastAPI" in md

    def test_partial_profile_minimal(self, capsys):
        """Profile minimo (so language) funciona."""
        profile = ProjectProfile(
            language="Python",
        )
        md = _profile_to_markdown(profile)
        assert "## Project Context" in md
        assert "Python" in md
        assert "unknown" in md  # campos que ficaram default

    def test_partial_profile_with_runtime_only(self, capsys):
        """Profile com runtime mas sem outros campos opcionais."""
        profile = _make_profile(
            runtime_version=">=3.12",
            module_count=0,
            core_modules=[],
            total_loc=0,
            architecture_patterns=[],
            domain_entities=[],
            has_ontology=False,
        )
        md = _profile_to_markdown(profile)
        assert ">=3.12" in md
        assert "Modulos" not in md

    def test_partial_profile_with_patterns_only(self, capsys):
        """Profile com padroes mas sem modulos."""
        profile = _make_profile(
            module_count=0,
            core_modules=[],
            total_loc=0,
            architecture_patterns=["clean_architecture"],
            detected_patterns=["clean_architecture"],
            has_ontology=False,
            domain_entities=[],
        )
        md = _profile_to_markdown(profile)
        assert "clean_architecture" in md
        assert "Padroes" in md
        assert "Modulos" not in md


# =============================================================================
# CTX-004: Saida markdown parseavel
# =============================================================================


class TestCtx004ParseableMarkdown:
    """CTX-004 (Happy): Saida markdown parseavel."""

    def test_markdown_has_valid_table(self, mock_cache_hit, capsys):
        """Tabela markdown tem cabecalho e separador validos."""
        cli_main(["context"])
        captured = capsys.readouterr()
        lines = captured.out.strip().split("\n")
        # Deve ter pelo menos: heading, blank, table header, separator, data...
        assert "| Campo | Valor |" in lines
        assert "|-------|-------|" in lines

    def test_markdown_table_has_pipe_count(self, mock_cache_hit, capsys):
        """Cada linha de tabela tem 2 pipes (3 colunas)."""
        cli_main(["context"])
        captured = capsys.readouterr()
        for line in captured.out.split("\n"):
            line_stripped = line.strip()
            if line_stripped.startswith("|"):
                # Deve ter pelo menos 2 pipes (abre/fecha)
                assert line_stripped.count("|") >= 2

    def test_markdown_parseable_by_regex(self, mock_cache_hit, capsys):
        """Markdown pode ser parseado por regex para extracao de dados."""
        cli_main(["context"])
        captured = capsys.readouterr()
        # Regex para extrair pares chave:valor da tabela
        pattern = r"\|\s*\*\*([^*]+)\*\*\s*\|\s*`([^`]+)`\s*\|"
        matches = re.findall(pattern, captured.out)
        fields = {k.strip(): v.strip() for k, v in matches}
        assert fields.get("Linguagem") == "Python"
        assert fields.get("Framework") == "FastAPI"
        assert fields.get("Database") == "PostgreSQL"
        assert fields.get("Cloud Provider") == "AWS"

    def test_markdown_heading_structure(self, capsys):
        """Markdown tem heading H2."""
        profile = _make_profile()
        md = _profile_to_markdown(profile)
        assert md.startswith("## Project Context")

    def test_markdown_closing_statement(self, capsys):
        """Markdown termina com disclaimer."""
        profile = _make_profile()
        md = _profile_to_markdown(profile)
        assert "*Contexto gerado automaticamente" in md
