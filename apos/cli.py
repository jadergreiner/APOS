"""CLI para APOS — comandos de contexto e utilitarios.

Comandos disponiveis:
    apos context   Exibe o ProjectProfile como markdown formatado.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional


def build_parser() -> argparse.ArgumentParser:
    """Constroi o parser principal com subcomandos."""
    parser = argparse.ArgumentParser(
        prog="apos",
        description="APOS — A Precise Ontology System for AI agents",
    )
    sub = parser.add_subparsers(dest="command", help="Comandos disponiveis")

    # --- apos context ---
    ctx = sub.add_parser("context", help="Exibe o ProjectProfile como markdown")
    ctx.add_argument(
        "--cache-dir",
        default=".apos",
        help="Diretorio do cache (default: .apos)",
    )
    ctx.add_argument(
        "--ttl",
        type=int,
        default=3600,
        help="TTL do cache em segundos (default: 3600)",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    """Entry point da CLI.

    Args:
        argv: Lista de argumentos (default: sys.argv[1:]).

    Returns:
        Codigo de saida (0 = sucesso, 1 = erro).
    """
    parser = build_parser()
    args = parser.parse_args(argv or sys.argv[1:])

    if args.command == "context":
        return _handle_context(args)
    else:
        parser.print_help()
        return 1


def _handle_context(args: argparse.Namespace) -> int:
    """Executa o comando ``context``."""
    from apos.project_adapter.cache import ProjectCache

    import asyncio

    cache = ProjectCache(cache_dir=args.cache_dir, ttl=args.ttl)
    profile, status = asyncio.run(cache.load())

    if profile is None:
        reason_map = {
            "miss": "Nenhum cache encontrado.",
            "expired": "Cache expirado.",
            "hash_mismatch": "pyproject.toml foi modificado desde o ultimo cache.",
            "corrupted": "Cache corrompido ou invalido.",
        }
        reason = reason_map.get(status, "Erro desconhecido.")
        print(_format_no_cache(reason))
        return 1

    print(_profile_to_markdown(profile))
    return 0


def _profile_to_markdown(profile) -> str:
    """Converte um ProjectProfile para markdown formatado.

    Args:
        profile: Instancia de ProjectProfile.

    Returns:
        String markdown com os dados do profile.
    """
    lines: list[str] = []
    lines.append("## Project Context")
    lines.append("")
    lines.append("| Campo | Valor |")
    lines.append("|-------|-------|")

    # Stack
    lines.append(f'| **Linguagem** | `{profile.language}` |')
    lines.append(f'| **Framework** | `{profile.framework}` |')
    lines.append(f'| **Database** | `{profile.database}` |')
    lines.append(f'| **Cloud Provider** | `{profile.cloud_provider}` |')
    if profile.runtime_version:
        lines.append(f'| **Runtime** | `{profile.runtime_version}` |')

    # Modulos
    if profile.module_count > 0:
        modules_str = ", ".join(f"`{m}`" for m in profile.core_modules)
        lines.append(
            f"| **Modulos ({profile.module_count})** | {modules_str} |"
        )
        lines.append(f"| **Diretorio** | `{profile.directory_layout}` |")
        lines.append(f"| **LOC total** | `{profile.total_loc}` |")

    # Padroes
    if profile.architecture_patterns:
        pat_str = ", ".join(f"`{p}`" for p in profile.architecture_patterns)
        lines.append(f"| **Padroes** | {pat_str} |")

    # Semantic
    if profile.has_ontology:
        lines.append("| **Ontologia** | `true` |")
    if profile.domain_entities:
        ent_str = ", ".join(f"`{e}`" for e in profile.domain_entities)
        lines.append(f"| **Dominio** | {ent_str} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        "*Contexto gerado automaticamente por `apos context`. "
        "Para atualizar, execute `apos discover`.*"
    )

    return "\n".join(lines)


def _format_no_cache(reason: str) -> str:
    """Formata mensagem quando nao ha cache disponivel.

    Args:
        reason: Motivo da ausencia de cache.

    Returns:
        String markdown com a mensagem.
    """
    lines: list[str] = []
    lines.append("## Project Context — Nao Disponivel")
    lines.append("")
    lines.append(f"> {reason}")
    lines.append("")
    lines.append("Execute o comando abaixo para gerar o profile do projeto:")
    lines.append("")
    lines.append("```bash")
    lines.append("apos discover")
    lines.append("```")
    lines.append("")
    lines.append(
        "*O profile sera cacheado automaticamente e ficara "
        "disponivel para `apos context` na proxima execucao.*"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
