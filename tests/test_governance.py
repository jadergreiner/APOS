"""Testes para o Governance Framework (DocumentAuditor)."""

from pathlib import Path

import pytest

from apos.governance import DocumentAuditor


@pytest.fixture
def tmp_project(tmp_path):
    (tmp_path / "OTHER.md").write_text("# Other\n\nExists.\n", encoding="utf-8")
    return tmp_path


class TestDocumentAuditorClean:
    def test_clean_document_passes(self, tmp_project):
        doc = tmp_project / "CLEAN.md"
        doc.write_text(
            "# Title\n\nSome real content.\n\n## Section\n\nMore real content, "
            "linking to [other](OTHER.md).\n",
            encoding="utf-8",
        )

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert report.passed
        assert report.blockers() == []
        assert report.sections_found == ["Title", "Section"]
        assert report.word_count > 0


class TestDocumentAuditorPlaceholders:
    def test_detects_bracket_placeholder(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\n[Define the vision here]\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert not report.passed
        assert any("placeholder" in f.message.lower() for f in report.blockers())

    def test_detects_todo_and_fixme(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\nTODO: write this.\nFIXME later.\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert len(report.blockers()) == 2


class TestDocumentAuditorLinks:
    def test_detects_broken_relative_link(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\nSee [missing](MISSING.md).\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert not report.passed
        assert any("Broken relative link" in f.message for f in report.blockers())

    def test_existing_relative_link_is_fine(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\nSee [other](OTHER.md).\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert report.passed

    def test_external_and_anchor_links_are_ignored(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text(
            "# Title\n\n[ext](https://example.com) [anchor](#title) "
            "[mail](mailto:a@b.com)\n",
            encoding="utf-8",
        )

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert report.passed


class TestDocumentAuditorHeadings:
    def test_detects_duplicate_heading(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text(
            "# Title\n\ncontent\n\n## Repeated\n\ncontent\n\n## Repeated\n\ncontent\n",
            encoding="utf-8",
        )

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert report.passed  # duplicates are warnings, not blockers
        assert any("appears 2 times" in f.message for f in report.warnings())

    def test_detects_empty_section(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\n## Empty Section\n\n## Next\n\ncontent\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()

        assert any(
            f.section == "Empty Section" and "no content" in f.message
            for f in report.warnings()
        )


class TestAuditReport:
    def test_to_dict_and_render_markdown(self, tmp_project):
        doc = tmp_project / "DOC.md"
        doc.write_text("# Title\n\n[placeholder]\n", encoding="utf-8")

        report = DocumentAuditor(doc, project_root=tmp_project).run()
        d = report.to_dict()
        md = report.render_markdown()

        assert d["passed"] is False
        assert d["num_blockers"] == 1
        assert "❌ BLOCKED" in md
        assert "Unresolved placeholder" in md
