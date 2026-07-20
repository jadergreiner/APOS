"""Tests for APOS Bootstrap Gate system."""

import pytest
import tempfile
from pathlib import Path
from apos.bootstrap.gate import BootstrapGate, BootstrapResult
from apos.bootstrap.validators import (
    StrategyValidator,
    OntologyValidator,
    GovernanceValidator,
)
from apos.bootstrap.templates import TemplateGenerator
from apos.bootstrap.session import (
    FoundationDefinitionSession,
    SessionManager,
    matches_session_trigger,
)


class TestBootstrapGate:
    """Tests for BootstrapGate class."""

    def test_bootstrap_gate_creation(self, tmp_path):
        """Test BootstrapGate can be instantiated."""
        gate = BootstrapGate(tmp_path)
        assert gate.project_root == tmp_path

    def test_bootstrap_gate_default_root(self, monkeypatch):
        """Test BootstrapGate uses cwd as default root."""
        monkeypatch.chdir("/tmp")
        gate = BootstrapGate()
        assert gate.project_root == Path.cwd()

    def test_validate_no_foundations(self, tmp_path):
        """Test validation fails when no foundations exist."""
        gate = BootstrapGate(tmp_path)
        result = gate.validate()

        assert not result.passed
        assert result.session_needed
        assert len(result.missing_foundations) == 10
        assert len(result.existing_foundations) == 0

    def test_validate_partial_foundations(self, tmp_path):
        """Test validation with some foundations present."""
        gate = BootstrapGate(tmp_path)

        # Create a few foundation files
        (tmp_path / "NORTH_STAR.md").write_text("# North Star")
        (tmp_path / "OKR.md").write_text("# OKRs")

        result = gate.validate()

        assert not result.passed
        assert result.session_needed
        assert len(result.existing_foundations) == 2
        assert len(result.missing_foundations) == 8
        assert "NORTH_STAR.md" in result.existing_foundations
        assert "OKR.md" in result.existing_foundations

    def test_validate_all_foundations(self, tmp_path):
        """Test validation passes when all foundations exist."""
        gate = BootstrapGate(tmp_path)

        # Create all required foundation files
        for foundation in BootstrapGate.REQUIRED_FOUNDATIONS:
            (tmp_path / foundation).write_text(f"# {foundation}")

        result = gate.validate()

        assert result.passed
        assert not result.session_needed
        assert len(result.existing_foundations) == 10
        assert len(result.missing_foundations) == 0

    def test_bootstrap_result_summary(self, tmp_path):
        """Test BootstrapResult summary generation."""
        gate = BootstrapGate(tmp_path)
        result = gate.validate()

        assert "✅" in result.summary or "❌" in result.summary
        assert "foundations found" in result.summary

    def test_validate_with_details(self, tmp_path):
        """Test detailed validation with validators."""
        gate = BootstrapGate(tmp_path)

        # Create some foundation files
        (tmp_path / "NORTH_STAR.md").write_text("# North Star\nVision statement")
        (tmp_path / "PURPOSE.md").write_text("# Purpose\nProblem statement")

        result = gate.validate_with_details()

        assert isinstance(result, BootstrapResult)
        assert len(result.validation_details) > 0

    def test_generate_missing_templates(self, tmp_path):
        """Test template generation for missing foundations."""
        gate = BootstrapGate(tmp_path)
        generated = gate.generate_missing_templates()

        assert isinstance(generated, dict)
        assert len(generated) > 0

        # Check that some files were created
        created_count = sum(1 for success in generated.values() if success)
        assert created_count > 0


class TestStrategyValidator:
    """Tests for StrategyValidator."""

    def test_strategy_validator_creation(self, tmp_path):
        """Test StrategyValidator can be instantiated."""
        validator = StrategyValidator(tmp_path)
        assert validator.project_root == tmp_path

    def test_validate_file_not_found(self, tmp_path):
        """Test validation fails for missing file."""
        validator = StrategyValidator(tmp_path)
        result = validator.validate_file("NORTH_STAR.md")

        assert not result.valid
        assert "File not found" in result.issues

    def test_validate_file_empty(self, tmp_path):
        """Test validation detects empty files."""
        validator = StrategyValidator(tmp_path)
        (tmp_path / "PURPOSE.md").write_text("")

        result = validator.validate_file("PURPOSE.md")

        assert not result.valid
        assert "Empty file" in result.issues

    def test_validate_file_valid(self, tmp_path):
        """Test validation passes for valid files."""
        validator = StrategyValidator(tmp_path)
        (tmp_path / "NORTH_STAR.md").write_text(
            "# North Star\n\nTeams visualize strategy end-to-end with clarity.\n\n## Success Metrics\n- Alignment score 90%"
        )

        result = validator.validate_file("NORTH_STAR.md")

        assert result.valid
        assert len(result.issues) == 0

    def test_validate_all_strategy_files(self, tmp_path):
        """Test validation of all strategy files."""
        validator = StrategyValidator(tmp_path)

        # Create valid strategy files with proper content
        files_content = {
            "NORTH_STAR.md": "# North Star\nTeams visualize strategy end-to-end.\n## Success Metrics\n- Alignment 90%",
            "OKR.md": "# OKRs\n## Objective 1: Growth\n- Key Result 1: 50% user increase\n- Key Result 2: 90% retention\n- Key Result 3: NPS 60%",
            "PURPOSE.md": "# Purpose\nWhy we exist: solve team alignment.\n## Jobs to be Done\nHelp teams make aligned decisions.\n## North Star Link\nAligns with our North Star vision.",
            "VALUE_PROPOSITION.md": "# Value Proposition\nWe deliver semantic clarity for AI agents.\n## Benefits\n- Benefit 1: 50% faster alignment\n- Benefit 2: Fewer errors\n- Benefit 3: Better decisions\n## Competitive Advantage\nOur unique approach to ontology.\n## Stakeholder Validation\nValidated with 5 PMs and 3 CTOs.",
        }

        for file, content in files_content.items():
            (tmp_path / file).write_text(content)

        results = validator.validate_all()

        assert len(results) == len(validator.STRATEGY_FILES)
        assert all(r.valid for r in results)


class TestOntologyValidator:
    """Tests for OntologyValidator."""

    def test_ontology_validator_creation(self, tmp_path):
        """Test OntologyValidator can be instantiated."""
        validator = OntologyValidator(tmp_path)
        assert validator.project_root == tmp_path

    def test_validate_file_not_found(self, tmp_path):
        """Test validation fails for missing file."""
        validator = OntologyValidator(tmp_path)
        result = validator.validate_file("ONTOLOGY.md")

        assert not result.valid
        assert "File not found" in result.issues

    def test_validate_file_empty(self, tmp_path):
        """Test validation detects empty ontology files."""
        validator = OntologyValidator(tmp_path)
        (tmp_path / "ONTOLOGY.md").write_text("")

        result = validator.validate_file("ONTOLOGY.md")

        assert not result.valid
        assert "Empty file" in result.issues

    def test_validate_file_with_entities(self, tmp_path):
        """Test validation detects entities."""
        validator = OntologyValidator(tmp_path)
        content = """# Ontology

## Entity Student
- Description: A learner
- Attributes: id, name, email

## Entity Course
- Description: Learning path
- Attributes: id, title, level

## Entity Instructor
- Description: Teaching professional
- Attributes: id, name, specialties

## Entity Enrollment
- Description: Student-Course relationship
- Attributes: id, date_joined, progress

## Entity Certificate
- Description: Achievement record
- Attributes: id, earned_date

## Relationships
- Student enrolls_in Course
- Instructor teaches Course
- Student receives Certificate

## Constraints
- Each Student can enroll in multiple Courses
- Each Course must have at least one Instructor
- Certificate is awarded only upon completion
"""
        (tmp_path / "ONTOLOGY.md").write_text(content)

        result = validator.validate_file("ONTOLOGY.md")

        assert result.valid
        assert result.entity_count >= 5

    def test_validate_all_ontology_files(self, tmp_path):
        """Test validation of all ontology files."""
        validator = OntologyValidator(tmp_path)

        # Create valid ontology files with proper content
        (tmp_path / "ONTOLOGY.md").write_text("""# Ontology

## Entity Feature
- Description: Product capability
- Attributes: id, name, status

## Entity Release
- Description: Product release
- Attributes: id, version, date

## Entity Task
- Description: Work unit
- Attributes: id, title, effort

## Entity Epic
- Description: Feature container
- Attributes: id, name, roadmap

## Entity Milestone
- Description: Timeline marker
- Attributes: id, name, date

## Relationships
- Feature belongs_to Release
- Task belongs_to Feature
- Epic contains Feature

## Constraints
- Each Feature must have a Release
- Tasks cannot exceed Feature scope
""")

        (tmp_path / "SEMANTIC_LAYER.md").write_text("""# Semantic Layer

## Scoring Components
- Coverage: Entity attribute completeness
- Quality: Relationship validity
- Consistency: Cross-entity alignment

## Semantic Rules (10+ required)
1. Feature in Release X = all Tasks in Release X
2. OKR achieved = all Metrics >= target
3. Epic complete = all Features released
4. Milestone passed = all Dependencies met
5. Task closed = all Subtasks done
6. Release ready = all Features tested
7. Feature valid = ontology constraints pass
8. Dependency chains must be acyclic
9. Entity relationships must be consistent
10. No orphaned entities allowed
11. Semantic coverage >= 80%
12. Quality score >= 0.70

## Validation Gates
- Gate 1: Coverage >= 80%
- Gate 2: Quality >= 0.70
- Gate 3: Consistency >= 0.85
""")

        results = validator.validate_all()

        assert len(results) == len(validator.ONTOLOGY_FILES)
        assert all(r.valid for r in results)


class TestGovernanceValidator:
    """Tests for GovernanceValidator."""

    def test_governance_validator_creation(self, tmp_path):
        """Test GovernanceValidator can be instantiated."""
        validator = GovernanceValidator(tmp_path)
        assert validator.project_root == tmp_path

    def test_validate_file_not_found(self, tmp_path):
        """Test validation fails for missing file."""
        validator = GovernanceValidator(tmp_path)
        result = validator.validate_file("GOVERNANCE.md")

        assert not result.valid
        assert "File not found" in result.issues

    def test_validate_file_valid(self, tmp_path):
        """Test validation passes for valid files."""
        validator = GovernanceValidator(tmp_path)
        (tmp_path / "GOVERNANCE.md").write_text("# Governance\n\nRules")

        result = validator.validate_file("GOVERNANCE.md")

        assert result.valid
        assert len(result.issues) == 0

    def test_validate_all_governance_files(self, tmp_path):
        """Test validation of all governance files."""
        validator = GovernanceValidator(tmp_path)

        # Create valid governance files with proper content
        (tmp_path / "GOVERNANCE.md").write_text("""# Governance

## Quality Gates
- Gate 1: Coverage must be >= 80%
- Gate 2: Quality score must be >= 0.70
- Gate 3: All audit rules must pass

## Validation Rules
- Check entity completeness
- Check relationship validity
- Verify semantic consistency

## Approval Workflow
- PM approves feature spec
- CTO approves architecture
- Release Manager approves release
""")

        (tmp_path / "BOOTSTRAP_GATE.md").write_text("""# Bootstrap Gate

## Required Foundations
- NORTH_STAR.md
- PURPOSE.md
- OKR.md
- VALUE_PROPOSITION.md
- ONTOLOGY.md
- SEMANTIC_LAYER.md
- GOVERNANCE.md
- CAPABILITIES.md
- IMPLEMENTATION_STATUS.md
- BOOTSTRAP_GATE.md

## Validation Process
1. Check all files exist
2. Validate content structure
3. Verify semantic alignment
""")

        (tmp_path / "CAPABILITIES.md").write_text("""# Capabilities

## Built-in Frameworks
- Release Management Framework
- Sprint Planning Framework
- JTBD Discovery Framework

## Use Cases
- Use case 1: Multi-team product planning
- Use case 2: Cross-functional alignment
- Use case 3: Semantic governance

## APIs and Integrations
- APOS REST API
- Python SDK
""")

        (tmp_path / "IMPLEMENTATION_STATUS.md").write_text("""# Implementation Status

## Current Phase
- Phase: Beta (v0.1.0)
- Started: 2026-07-19
- Status: Active Development

## Completed Features
- [x] Bootstrap Gate system
- [x] Semantic Layer framework

## In Progress
- [ ] Release Management
- [ ] Governance enforcement

## Planned
- [ ] Advanced analytics
- [ ] Integration marketplace

## Known Limitations
- Limited to 100 entities per ontology (Beta)
- Real-time sync requires polling
""")

        results = validator.validate_all()

        assert len(results) == len(validator.GOVERNANCE_FILES)
        assert all(r.valid for r in results)


class TestTemplateGenerator:
    """Tests for TemplateGenerator."""

    def test_template_generator_creation(self, tmp_path):
        """Test TemplateGenerator can be instantiated."""
        generator = TemplateGenerator(tmp_path)
        assert generator.project_root == tmp_path

    def test_generate_template_content(self):
        """Test template content generation."""
        generator = TemplateGenerator()
        content = generator.generate("NORTH_STAR.md")

        assert isinstance(content, str)
        assert len(content) > 0
        assert "# North Star" in content

    def test_generate_all_templates(self):
        """Test all templates can be generated."""
        generator = TemplateGenerator()

        for filename in TemplateGenerator.TEMPLATES.keys():
            content = generator.generate(filename)
            assert isinstance(content, str)
            assert len(content) > 0

    def test_generate_file(self, tmp_path):
        """Test writing template file to disk."""
        generator = TemplateGenerator(tmp_path)
        success = generator.generate_file("NORTH_STAR.md")

        assert success
        assert (tmp_path / "NORTH_STAR.md").exists()
        content = (tmp_path / "NORTH_STAR.md").read_text()
        assert "# North Star" in content

    def test_generate_file_no_overwrite(self, tmp_path):
        """Test template generation respects no-overwrite flag."""
        generator = TemplateGenerator(tmp_path)

        # Create initial file
        initial_content = "# Original Content"
        (tmp_path / "PURPOSE.md").write_text(initial_content)

        # Try to generate without overwrite
        success = generator.generate_file("PURPOSE.md", overwrite=False)

        assert not success
        # Original content should be preserved
        assert (tmp_path / "PURPOSE.md").read_text() == initial_content

    def test_generate_file_with_overwrite(self, tmp_path):
        """Test template generation with overwrite flag."""
        generator = TemplateGenerator(tmp_path)

        # Create initial file
        (tmp_path / "PURPOSE.md").write_text("# Original")

        # Generate with overwrite
        success = generator.generate_file("PURPOSE.md", overwrite=True)

        assert success
        content = (tmp_path / "PURPOSE.md").read_text()
        assert "# Purpose" in content
        assert "Original" not in content

    def test_generate_missing(self, tmp_path):
        """Test generating multiple missing templates."""
        generator = TemplateGenerator(tmp_path)
        missing_files = ["NORTH_STAR.md", "OKR.md", "PURPOSE.md"]

        results = generator.generate_missing(missing_files)

        assert len(results) == 3
        assert all(results.values())  # All should be True
        assert (tmp_path / "NORTH_STAR.md").exists()
        assert (tmp_path / "OKR.md").exists()
        assert (tmp_path / "PURPOSE.md").exists()


class TestFoundationDefinitionSession:
    """Tests for FoundationDefinitionSession."""

    def test_session_creation(self, tmp_path):
        """Test FoundationDefinitionSession can be instantiated."""
        session = FoundationDefinitionSession(tmp_path)
        assert session.project_root == tmp_path
        assert isinstance(session.defined_foundations, dict)

    def test_session_with_missing_foundations(self, tmp_path):
        """Test session initialization with missing foundations."""
        missing = ["NORTH_STAR.md", "OKR.md", "PURPOSE.md"]
        session = FoundationDefinitionSession(tmp_path, missing)

        assert session.missing_foundations == missing

    def test_session_run_output(self, tmp_path, capsys):
        """Test session run produces output."""
        # Create templates first
        generator = TemplateGenerator(tmp_path)
        generator.generate_file("PURPOSE.md")

        session = FoundationDefinitionSession(tmp_path, ["PURPOSE.md"])
        result = session.run()

        captured = capsys.readouterr()
        assert "Foundation Definition Workflow" in captured.out

    @pytest.mark.integration
    def test_session_full_workflow(self, tmp_path):
        """Test complete foundation definition workflow."""
        missing = [
            "NORTH_STAR.md",
            "OKR.md",
            "PURPOSE.md",
            "VALUE_PROPOSITION.md",
            "ONTOLOGY.md",
            "SEMANTIC_LAYER.md",
            "GOVERNANCE.md",
            "BOOTSTRAP_GATE.md",
            "CAPABILITIES.md",
            "IMPLEMENTATION_STATUS.md",
        ]

        # Generate templates
        generator = TemplateGenerator(tmp_path)
        for file in missing:
            generator.generate_file(file)

        # Run session
        session = FoundationDefinitionSession(tmp_path, missing)
        result = session.run()

        assert isinstance(result, dict)
        # All files should exist after session
        for file in missing:
            assert (tmp_path / file).exists()


class TestSessionTrigger:
    """Tests for matches_session_trigger detection helper."""

    @pytest.mark.parametrize(
        "message",
        [
            "Inicie uma sessão com APOS",
            "APOS inicie uma sessão nova e gerencie",
            "Start a session with APOS",
            "vamos começar uma sessão do APOS agora",
        ],
    )
    def test_matches_valid_triggers(self, message):
        assert matches_session_trigger(message)

    @pytest.mark.parametrize(
        "message",
        [
            "Qual o estado atual da Sprint 0-0?",
            "Inicie uma sessão",  # missing "apos"
            "APOS é um framework de camada semântica",  # no verb+session combo
        ],
    )
    def test_rejects_non_triggers(self, message):
        assert not matches_session_trigger(message)


class TestSessionManager:
    """Tests for SessionManager (auto-identification + session entry point)."""

    def test_initialize_returns_manager(self, tmp_path):
        manager = SessionManager.initialize(tmp_path)
        assert isinstance(manager, SessionManager)
        assert manager.project_root == tmp_path

    def test_default_project_root(self, monkeypatch, tmp_path):
        monkeypatch.chdir(tmp_path)
        manager = SessionManager()
        assert manager.project_root == Path.cwd()

    def test_run_skips_session_when_complete(self, tmp_path, capsys):
        for foundation in BootstrapGate.REQUIRED_FOUNDATIONS:
            (tmp_path / foundation).write_text(f"# {foundation}")

        manager = SessionManager(tmp_path)
        result = manager.run()

        assert result == {}
        captured = capsys.readouterr()
        assert "no session needed" in captured.out

    def test_run_generates_templates_and_runs_session(self, tmp_path, capsys):
        manager = SessionManager(tmp_path)
        result = manager.run()

        assert isinstance(result, dict)
        # Templates should have been generated as part of the session
        assert (tmp_path / "NORTH_STAR.md").exists()
        captured = capsys.readouterr()
        assert "Foundation Definition Workflow" in captured.out


class TestBootstrapIntegration:
    """Integration tests for Bootstrap system."""

    @pytest.mark.integration
    def test_bootstrap_full_cycle(self, tmp_path):
        """Test complete bootstrap cycle: validation → generation → validation."""
        gate = BootstrapGate(tmp_path)

        # Initial validation should fail
        result1 = gate.validate()
        assert not result1.passed

        # Generate templates
        generated = gate.generate_missing_templates()
        assert len(generated) > 0

        # All files should now exist
        result2 = gate.validate()
        assert result2.passed
        assert len(result2.existing_foundations) == 10

    @pytest.mark.integration
    def test_bootstrap_with_custom_content(self, tmp_path):
        """Test bootstrap with user-customized foundation files."""
        # Create custom foundation files
        (tmp_path / "NORTH_STAR.md").write_text("# Custom North Star\nOur vision...")
        (tmp_path / "PURPOSE.md").write_text("# Custom Purpose\nOur mission...")

        gate = BootstrapGate(tmp_path)
        result = gate.validate()

        # Should still fail due to missing files
        assert not result.passed
        assert 8 in [len(result.missing_foundations)]

        # Generate missing
        gate.generate_missing_templates()

        # Should now pass
        result2 = gate.validate()
        assert result2.passed

        # Custom content should be preserved
        north_star = (tmp_path / "NORTH_STAR.md").read_text()
        assert "Custom North Star" in north_star
