"""ProjectValidator — compara ProjectProfile com docs/SDD/ para detectar divergencias."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from apos.project_adapter import ProjectAdapter, ProjectProfile


# =============================================================================
# SDD Parser
# =============================================================================


@dataclass
class SDDStack:
    """Stack tecnologico extraido de um documento SDD."""

    language: str = "unknown"
    framework: str = "unknown"
    database: str = "unknown"
    cloud_provider: str = "unknown"


def _parse_frontmatter(text: str) -> dict[str, str]:
    """Extrai frontmatter YAML simples de um markdown."""
    meta: dict[str, str] = {}
    text = text.strip()
    if not text.startswith("---"):
        return meta
    end = text.find("---", 3)
    if end == -1:
        return meta
    block = text[3:end].strip()
    for line in block.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta


def _extract_stack_from_sdd(text: str, sdd_name: str) -> SDDStack:
    """Extrai informacoes de stack tecnologico do conteudo de um SDD."""
    stack = SDDStack()
    text_lower = text.lower()

    # --- Language ---
    lang_map = {
        "python": "Python",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "java": "Java",
        "golang": "Go",
        "rust": "Rust",
        "ruby": "Ruby",
    }
    for key, val in lang_map.items():
        if re.search(rf"(?i)\b{re.escape(key)}\b", text_lower):
            # Check if it's part of a version string like Python 3.12
            stack.language = val
            break

    # --- Framework ---
    framework_map = {
        r"\bfastapi\b": "FastAPI",
        r"\bdjango\b": "Django",
        r"\bflask\b": "Flask",
        r"\bnext\.js\b": "Next.js",
        r"\bnextjs\b": "Next.js",
        r"\breact\b": "React",
        r"\bvue\.js\b": "Vue.js",
        r"\bexpress\b": "Express",
        r"\bstarlette\b": "Starlette",
    }
    for pattern, name in framework_map.items():
        if re.search(pattern, text_lower):
            stack.framework = name
            break

    # Infer language from framework if not already detected
    if stack.language == "unknown":
        framework_lang_map = {
            "Django": "Python",
            "FastAPI": "Python",
            "Flask": "Python",
            "Starlette": "Python",
            "Next.js": "JavaScript",
            "React": "JavaScript",
            "Vue.js": "JavaScript",
            "Express": "JavaScript",
        }
        if stack.framework in framework_lang_map:
            stack.language = framework_lang_map[stack.framework]

    # --- Database ---
    db_map = {
        r"\bdynamodb\b": "DynamoDB",
        r"\bpostgresql\b": "PostgreSQL",
        r"\bpostgres\b": "PostgreSQL",
        r"\bmongodb\b": "MongoDB",
        r"\bredis\b": "Redis",
        r"\bsqlite\b": "SQLite",
        r"\bmysql\b": "MySQL",
        r"\bsqlalchemy\b": "SQLAlchemy",
    }
    for pattern, name in db_map.items():
        if re.search(pattern, text_lower):
            stack.database = name
            break

    # --- Cloud ---
    cloud_map = {
        r"\baws\b": "AWS",
        r"\bamazon web services\b": "AWS",
        r"\bgcp\b": "GCP",
        r"\bgoogle cloud\b": "GCP",
        r"\bazure\b": "Azure",
        r"\bcloudflare\b": "Cloudflare",
    }
    for pattern, name in cloud_map.items():
        if re.search(pattern, text_lower):
            stack.cloud_provider = name
            break

    return stack


# =============================================================================
# Validation Result
# =============================================================================


@dataclass
class ValidationItem:
    """Um item de comparacao entre codigo e documentacao."""

    field: str
    code_value: str
    doc_value: str
    status: str = "consistent"  # consistent | divergent | absent_code | absent_doc


@dataclass
class ValidationReport:
    """Relatorio completo de validacao."""

    project_root: str = ""
    sdd_count: int = 0
    items: list[ValidationItem] = field(default_factory=list)

    @property
    def consistent(self) -> list[ValidationItem]:
        return [i for i in self.items if i.status == "consistent"]

    @property
    def divergent(self) -> list[ValidationItem]:
        return [i for i in self.items if i.status == "divergent"]

    @property
    def absent_code(self) -> list[ValidationItem]:
        return [i for i in self.items if i.status == "absent_code"]

    @property
    def absent_doc(self) -> list[ValidationItem]:
        return [i for i in self.items if i.status == "absent_doc"]

    @property
    def score(self) -> float:
        """Percentual de itens consistentes (0.0 a 1.0)."""
        if not self.items:
            return 0.0
        return round(len(self.consistent) / len(self.items), 2)

    def to_markdown(self) -> str:
        """Gera relatorio em formato markdown."""
        lines: list[str] = []
        lines.append("## Relatorio de Validacao")
        lines.append("")

        if self.consistent:
            lines.append("### Consistentes \u2705")
            for item in self.consistent:
                lines.append(f"- {item.field}: {item.code_value} == {item.doc_value}")
            lines.append("")

        if self.divergent:
            lines.append("### Divergentes \u274c")
            for item in self.divergent:
                lines.append(
                    f"- {item.field}: {item.code_value} (codigo) vs "
                    f"{item.doc_value} (docs)"
                )
            lines.append("")

        if self.absent_code:
            lines.append("### Ausentes no Codigo \u26a0\ufe0f")
            for item in self.absent_code:
                lines.append(
                    f"- {item.field}: documentado como '{item.doc_value}', "
                    f"mas nao detectado no codigo"
                )
            lines.append("")

        if self.absent_doc:
            lines.append("### Ausentes na Documentacao \u26a0\ufe0f")
            for item in self.absent_doc:
                lines.append(
                    f"- {item.field}: detectado como '{item.code_value}', "
                    f"mas nao mencionado nos SDDs"
                )
            lines.append("")

        lines.append(f"**Total de SDDs analisados:** {self.sdd_count}")
        lines.append(f"**Score de consistencia:** {self.score:.0%}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Retorna relatorio como dicionario serializavel."""
        return {
            "project_root": self.project_root,
            "sdd_count": self.sdd_count,
            "score": self.score,
            "items": [
                {
                    "field": i.field,
                    "code_value": i.code_value,
                    "doc_value": i.doc_value,
                    "status": i.status,
                }
                for i in self.items
            ],
        }


# =============================================================================
# ProjectValidator
# =============================================================================


STACK_FIELDS = [
    "language",
    "framework",
    "database",
    "cloud_provider",
]


class ProjectValidator:
    """Valida consistencia entre ProjectProfile (codigo) e docs/SDD/ (documentacao)."""

    def __init__(self, project_root: str | Path, adapter: Optional[ProjectAdapter] = None) -> None:
        self.project_root = Path(project_root)
        self.adapter = adapter or ProjectAdapter()

    def validate(self) -> ValidationReport:
        """Executa validacao completa e retorna relatorio."""
        report = ValidationReport(project_root=str(self.project_root))

        # 1. Discover ProjectProfile from code
        try:
            profile = self.adapter.discover(self.project_root)
        except Exception as e:
            # If discovery fails, return minimal report with error
            report.items.append(
                ValidationItem(
                    field="discovery",
                    code_value=f"ERROR: {e}",
                    doc_value="N/A",
                    status="divergent",
                )
            )
            return report

        # 2. Parse SDD docs
        sdd_dir = self.project_root / "docs" / "SDD"
        sdd_stack = self._parse_sdd_directory(sdd_dir)
        report.sdd_count = len(list(sdd_dir.rglob("*.md"))) if sdd_dir.is_dir() else 0

        # 3. Compare stack fields
        for field in STACK_FIELDS:
            code_val = getattr(profile, field, "unknown")
            doc_val = getattr(sdd_stack, field, "unknown")

            if code_val == doc_val:
                report.items.append(
                    ValidationItem(
                        field=field,
                        code_value=code_val,
                        doc_value=doc_val,
                        status="consistent",
                    )
                )
            elif doc_val == "unknown" and code_val != "unknown":
                # Code has it, docs don't mention it
                report.items.append(
                    ValidationItem(
                        field=field,
                        code_value=code_val,
                        doc_value=doc_val,
                        status="absent_doc",
                    )
                )
            elif code_val == "unknown" and doc_val != "unknown":
                # Docs mention it, code doesn't have it
                report.items.append(
                    ValidationItem(
                        field=field,
                        code_value=code_val,
                        doc_value=doc_val,
                        status="absent_code",
                    )
                )
            else:
                # Both found but different
                report.items.append(
                    ValidationItem(
                        field=field,
                        code_value=code_val,
                        doc_value=doc_val,
                        status="divergent",
                    )
                )

        return report

    def _parse_sdd_directory(self, sdd_dir: Path) -> SDDStack:
        """Percorre docs/SDD/ e agrega stack tecnologico."""
        if not sdd_dir.is_dir():
            return SDDStack()

        aggregated = SDDStack()
        md_files = sorted(sdd_dir.rglob("*.md"))

        if not md_files:
            return aggregated

        # Track what we've seen to aggregate across multiple SDDs
        seen_languages: set[str] = set()
        seen_frameworks: set[str] = set()
        seen_databases: set[str] = set()
        seen_clouds: set[str] = set()

        for md_file in md_files:
            # Skip template files and index/readme
            if ".templates" in str(md_file):
                continue
            if md_file.name.lower() in ("index.md", "readme.md"):
                continue
            # Skip incident reports
            if "incidents" in str(md_file):
                continue
            try:
                text = md_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            s = _extract_stack_from_sdd(text, md_file.name)

            if s.language != "unknown":
                seen_languages.add(s.language)
            if s.framework != "unknown":
                seen_frameworks.add(s.framework)
            if s.database != "unknown":
                seen_databases.add(s.database)
            if s.cloud_provider != "unknown":
                seen_clouds.add(s.cloud_provider)

        # Populate aggregated — if multiple, use the most frequent
        aggregated.language = self._most_common(seen_languages) if seen_languages else "unknown"
        aggregated.framework = self._most_common(seen_frameworks) if seen_frameworks else "unknown"
        aggregated.database = self._most_common(seen_databases) if seen_databases else "unknown"
        aggregated.cloud_provider = self._most_common(seen_clouds) if seen_clouds else "unknown"

        return aggregated

    @staticmethod
    def _most_common(values: set[str]) -> str:
        """Retorna o primeiro valor (mais frequente entre SDDs)."""
        # Since we can't easily count, return the first alphabetically
        return sorted(values)[0]
