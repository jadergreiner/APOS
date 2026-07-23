"""Document Auditor — structural/quality audit for markdown documents.

Note: this is distinct from the `AuditRunner(ontology, graph)` shape sketched
in README.md's aspirational examples — that requires an `Ontology` class that
does not exist yet in this codebase. `DocumentAuditor` audits a single markdown
document's structure and content-quality signals (placeholders, broken
relative links, empty/duplicate sections) — a smaller, real, immediately
useful scope.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

PLACEHOLDER_PATTERN = re.compile(r"\[[A-Za-z][^\]\n]{0,80}\](?!\()|TODO|FIXME|\bXXX\b")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class AuditFinding:
    """A single issue found while auditing a document."""

    severity: str  # "blocker", "warning", "info"
    section: str
    message: str

    def to_dict(self) -> dict:
        return {"severity": self.severity, "section": self.section, "message": self.message}


@dataclass
class AuditReport:
    """Result of auditing a document."""

    document: str
    findings: list[AuditFinding] = field(default_factory=list)
    sections_found: list[str] = field(default_factory=list)
    word_count: int = 0

    @property
    def passed(self) -> bool:
        """No blockers means the document passes the gate (warnings are informational)."""
        return not any(f.severity == "blocker" for f in self.findings)

    def blockers(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.severity == "blocker"]

    def warnings(self) -> list[AuditFinding]:
        return [f for f in self.findings if f.severity == "warning"]

    def to_dict(self) -> dict:
        return {
            "document": self.document,
            "passed": self.passed,
            "num_sections": len(self.sections_found),
            "word_count": self.word_count,
            "num_findings": len(self.findings),
            "num_blockers": len(self.blockers()),
            "num_warnings": len(self.warnings()),
            "findings": [f.to_dict() for f in self.findings],
        }

    def render_markdown(self) -> str:
        """Render a human-readable audit report."""
        lines = [f"# Audit Report — {self.document}", ""]
        lines += [f"**Status:** {'✅ PASSED' if self.passed else '❌ BLOCKED'}"]
        lines += [f"**Sections:** {len(self.sections_found)} | **Words:** {self.word_count}", ""]

        if self.blockers():
            lines += ["## ❌ Blockers", ""]
            for f in self.blockers():
                lines += [f"- **{f.section}:** {f.message}"]
            lines += [""]

        if self.warnings():
            lines += ["## ⚠️ Warnings", ""]
            for f in self.warnings():
                lines += [f"- **{f.section}:** {f.message}"]
            lines += [""]

        if not self.findings:
            lines += ["No issues found.", ""]

        return "\n".join(lines) + "\n"


class DocumentAuditor:
    """Audits a single markdown document for structural/content-quality issues.

    Checks performed:
    - Unresolved placeholders (`[Foo]`, `TODO`, `FIXME`, `XXX`)
    - Broken relative links (markdown links pointing to files that don't exist)
    - Duplicate headings at the same level (often a copy-paste artifact)
    - Empty sections (a heading immediately followed by another heading)
    """

    def __init__(self, path: Path, project_root: Optional[Path] = None):
        self.path = Path(path)
        self.project_root = Path(project_root) if project_root else self.path.parent

    def run(self) -> AuditReport:
        text = self.path.read_text(encoding="utf-8")
        report = AuditReport(document=str(self.path))
        report.word_count = len(text.split())
        report.sections_found = [m.group(2) for m in HEADING_PATTERN.finditer(text)]

        self._check_placeholders(text, report)
        self._check_broken_links(text, report)
        self._check_duplicate_headings(text, report)
        self._check_empty_sections(text, report)

        return report

    def _check_placeholders(self, text: str, report: AuditReport) -> None:
        for match in PLACEHOLDER_PATTERN.finditer(text):
            line_no = text.count("\n", 0, match.start()) + 1
            report.findings.append(
                AuditFinding(
                    severity="blocker",
                    section=f"line {line_no}",
                    message=f"Unresolved placeholder: {match.group(0)!r}",
                )
            )

    def _check_broken_links(self, text: str, report: AuditReport) -> None:
        for match in MARKDOWN_LINK_PATTERN.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target_path = (self.project_root / target.split("#")[0]).resolve()
            if not target_path.exists():
                line_no = text.count("\n", 0, match.start()) + 1
                report.findings.append(
                    AuditFinding(
                        severity="blocker",
                        section=f"line {line_no}",
                        message=f"Broken relative link: {target!r} does not exist",
                    )
                )

    def _check_duplicate_headings(self, text: str, report: AuditReport) -> None:
        seen: dict[str, int] = {}
        for match in HEADING_PATTERN.finditer(text):
            heading = match.group(2).strip()
            seen[heading] = seen.get(heading, 0) + 1
        for heading, count in seen.items():
            if count > 1:
                report.findings.append(
                    AuditFinding(
                        severity="warning",
                        section=heading,
                        message=f"Heading appears {count} times — possible duplication",
                    )
                )

    def _check_empty_sections(self, text: str, report: AuditReport) -> None:
        headings = list(HEADING_PATTERN.finditer(text))
        for current, nxt in zip(headings, headings[1:] + [None]):
            start = current.end()
            end = nxt.start() if nxt else len(text)
            body = text[start:end].strip()
            body = re.sub(r"^-{3,}\s*$", "", body, flags=re.MULTILINE).strip()
            if not body:
                report.findings.append(
                    AuditFinding(
                        severity="warning",
                        section=current.group(2).strip(),
                        message="Section has no content",
                    )
                )
