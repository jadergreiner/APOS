"""APOS Governance Framework.

Provides document-level and (eventually) ontology-level audit tooling.

Usage:
    from apos.governance import DocumentAuditor

    auditor = DocumentAuditor("docs/product/PRODUCT_VISION.md", project_root=".")
    report = auditor.run()
    print(report.render_markdown())
"""

from apos.governance.audit import AuditFinding, AuditReport, DocumentAuditor

__all__ = [
    "AuditFinding",
    "AuditReport",
    "DocumentAuditor",
]
