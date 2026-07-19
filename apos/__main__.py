"""CLI entry point for APOS initialization and management."""
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print_help()
        return 1

    command = sys.argv[1]

    if command == "init":
        from apos.bootstrap.gate import BootstrapGate
        gate = BootstrapGate(project_root=Path.cwd())
        gate.run()
        return 0
    elif command == "--version":
        from apos import __version__
        print(f"APOS {__version__}")
        return 0
    elif command in ("--help", "-h"):
        print_help()
        return 0
    else:
        print(f"Unknown command: {command}")
        print_help()
        return 1


def print_help():
    from apos import __version__
    print(f"""
APOS {__version__} — A Precise Ontology System for AI agents

Usage:
    python -m apos COMMAND

Commands:
    init              Initialize APOS project (validate foundations, bootstrap if needed)
    --version         Show version
    --help            Show this help message
""".strip())


if __name__ == "__main__":
    sys.exit(main())
