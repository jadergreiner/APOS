"""Testes para auto-identificação de projeto APOS (apos/__init__.py)."""

from pathlib import Path

import apos


class TestAposProjectIdentity:
    """Testes para APOS_PROJECT_METADATA e is_apos_project()."""

    def test_metadata_has_required_fields(self):
        assert apos.APOS_PROJECT_METADATA["framework"] == "apos"
        assert apos.APOS_PROJECT_METADATA["framework_version"] == apos.__version__
        assert apos.APOS_PROJECT_METADATA["marker_file"] == "BOOTSTRAP_GATE.md"

    def test_is_apos_project_false_for_empty_dir(self, tmp_path):
        assert not apos.is_apos_project(tmp_path)

    def test_is_apos_project_true_when_marker_exists(self, tmp_path):
        (tmp_path / "BOOTSTRAP_GATE.md").write_text("# Bootstrap Gate")
        assert apos.is_apos_project(tmp_path)

    def test_is_apos_project_uses_cwd_by_default(self, monkeypatch, tmp_path):
        (tmp_path / "BOOTSTRAP_GATE.md").write_text("# Bootstrap Gate")
        monkeypatch.chdir(tmp_path)
        assert apos.is_apos_project()

    def test_exports_bootstrap_symbols(self):
        assert apos.BootstrapGate is not None
        assert apos.FoundationDefinitionSession is not None
        assert apos.SessionManager is not None
        assert callable(apos.matches_session_trigger)
