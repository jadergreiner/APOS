# APOS — A Precise Ontology System

[![Tests](https://github.com/jadergreiner/APOS/workflows/Tests/badge.svg)](https://github.com/jadergreiner/APOS/actions)
[![Lint](https://github.com/jadergreiner/APOS/workflows/Lint/badge.svg)](https://github.com/jadergreiner/APOS/actions)

**APOS is a semantic layer that provides precise, vivo (live), and connected business context to AI agents — enabling them to implement exactly what matters, on the first attempt, without hallucination, rework, or token waste.**

## What is APOS?

APOS (A Precise Ontology System) is a framework for building and maintaining a **single source of truth** for business context in AI-driven applications. It combines:

- **Ontology**: Structured domain model (entities, relationships, hierarchies)
- **Knowledge Graph**: Connected data representing your business domain
- **Semantic Layer**: Precision scoring and quality gates
- **Governance**: Audit trails, validation, and continuous improvement

**Use Cases:**
- 🎓 [Meu PDI](https://github.com/jadergreiner/meu-pdi) — First production use case (student journey personalization)
- 🏦 Enterprise systems (Itau, etc.) — Reducing agent hallucination, improving implementation quality
- 🤖 Any AI-powered product using LLM agents for code generation, decision-making, or automation

**Why it Matters:**
When agents lack precise context, they:
- Hallucinate business logic that doesn't match reality
- Generate rework-prone implementations
- Waste tokens on clarification loops
- Miss domain constraints and requirements

APOS eliminates this by providing agents (and their human operators) with **truth they can trust**.

---

## Quick Start

### Prerequisites

- Python 3.9+
- pip or conda
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/jadergreiner/APOS.git
cd APOS

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install APOS in development mode
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Run tests to confirm setup
pytest

# Check version
python -c "import apos; print(apos.__version__)"
```

### Hello World

```python
from apos import Ontology, KnowledgeGraph, SemanticGate
from apos.loader import OntologyLoader

# Load ontology from YAML
ontology = OntologyLoader.from_yaml("examples/sample_ontology.yaml")

# Build knowledge graph
graph = KnowledgeGraph()
graph.load_ontology(ontology)

# Evaluate with governance gate
gate = SemanticGate(min_score=0.80)
score = gate.evaluate(graph)

print(f"Semantic Score: {score.value:.3f}")
print(f"Status: {score.status}")

if score.status == "acceptable":
    print("✅ Context is ready for agent consumption")
else:
    print("⚠️  Context needs improvement")
    print(f"Issues: {score.issues}")
```

Run it:
```bash
python examples/basic_usage.py
```

---

## Project Structure

```
APOS/
├── apos/                          # Main package
│   ├── __init__.py                # Version, exports
│   ├── __main__.py                # CLI entry point (init, init-sprint, daily, validate-sprint)
│   ├── core/                      # Core abstractions
│   │   ├── types.py               # Domain types (Entity, Relationship, Node, Edge)
│   │   ├── ontology.py            # Ontology model
│   │   ├── graph.py               # Knowledge graph
│   │   └── semantic.py            # Semantic scoring
│   ├── bootstrap/                 # Bootstrap Gate + project initialization
│   │   ├── gate.py                # BootstrapGate — validates 10 semantic foundations
│   │   ├── session.py             # FoundationDefinitionSession — guided setup
│   │   ├── validators/            # Specialized validators (Strategy, Ontology, Governance)
│   │   └── templates/             # Auto-generated foundation templates
│   ├── governance/                # Governance framework
│   │   ├── gate.py                # Semantic gate
│   │   ├── metrics.py             # Metrics & scoring
│   │   ├── audit.py               # Audit tools
│   │   └── config.py              # Governance config
│   ├── kernel/                    # Kernel patterns (enforced across all sprints)
│   │   ├── __init__.py
│   │   └── commit_tracking.py     # Commit tracking validation
│   ├── release_management/        # Release & Sprint management
│   │   ├── release.py             # Release, ReleaseManager
│   │   ├── sprint.py              # Sprint, SprintManager, Task, TaskStatus
│   │   ├── ceremonies.py          # DailyStandup, SprintPlanning, Retrospective
│   │   ├── daily_runner.py        # Automated daily standup runner
│   │   └── templates.py           # Template generator (README, BOARD, STATUS, RETRO, etc)
│   ├── loader/                    # Data loaders
│   │   ├── ontology_loader.py     # Load ontologies
│   │   └── graph_loader.py        # Load graphs
│   ├── utils/                     # Utilities
│   │   ├── validators.py
│   │   ├── serializers.py
│   │   └── logger.py
│   └── errors.py                  # Custom exceptions
│
├── tests/                         # Test suite (pytest)
│   ├── conftest.py
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── fixtures/                  # Test data
│
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md            # System design
│   ├── API.md                     # API reference
│   ├── INTEGRATION.md             # Integration guide
│   ├── GOVERNANCE.md              # Governance details
│   └── DEVELOPMENT.md             # Contributing guide
│
├── examples/                      # Usage examples
│   ├── basic_usage.py
│   ├── meu_pdi_integration.py
│   └── enterprise_usage.py
│
├── setup.py                       # Package metadata
├── pyproject.toml                 # Modern Python config
├── requirements.txt               # Dependencies
├── requirements-dev.txt           # Dev dependencies
├── .gitignore
├── LICENSE                        # Proprietary
└── README.md                      # This file
```

---

## Development Workflow

### 1. Local Setup

```bash
# Clone and install
git clone https://github.com/jadergreiner/APOS.git
cd APOS
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

### 2. Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/unit/test_ontology.py

# With coverage report
pytest --cov=apos tests/

# Watch mode (re-run on file change) — install pytest-watch first
ptw
```

### 3. Linting & Formatting

```bash
# Format code (Black)
black apos/ tests/

# Check style (Flake8)
flake8 apos/ tests/

# Check types (optional; add mypy later if needed)
mypy apos/
```

### 4. Add a Feature

1. **Write a test first** (TDD):
   ```bash
   # Create test in tests/unit/test_new_feature.py
   ```

2. **Implement the feature**:
   ```bash
   # Add code to apos/ (appropriate module)
   ```

3. **Run tests**:
   ```bash
   pytest tests/unit/test_new_feature.py -v
   ```

4. **Verify coverage**:
   ```bash
   pytest --cov=apos tests/
   ```

5. **Commit**:
   ```bash
   git add .
   git commit -m "feat: add new feature X"
   ```

### 4. APOS CLI

APOS comes with a built-in CLI for project initialization and sprint management.

```bash
# Initialize APOS project (validate 10 semantic foundations)
python -m apos init

# Create a new sprint with standard structure (BOARD, USER_STORIES, RETRO, etc)
python -m apos init-sprint --sprint sprint-0.2 --release R0

# Preview without creating files
python -m apos init-sprint --sprint sprint-0.2 --dry-run

# Run a Daily Standup
python -m apos daily --sprint sprint-0.0 --mode automatic

# Validate commit tracking in sprint artifacts
python -m apos validate-sprint --sprint-root docs/releases/R0/sprint-0.0/
```

### 5. GitHub Workflow

APOS runs automated checks on every push/PR:

- **Tests**: `pytest` (all tests must pass)
- **Lint**: `black` + `flake8` (code style)
- **Coverage**: Must maintain ≥80%

View results in GitHub Actions: https://github.com/jadergreiner/APOS/actions

---

## Core Concepts

### Ontology

A structured representation of your domain — entities, relationships, hierarchies.

```yaml
# Example: ontology.yaml
entities:
  - id: student
    name: "Student"
    description: "A learner in the system"
    attributes:
      - id
      - name
      - email
  
  - id: course
    name: "Course"
    description: "Learning path"

relationships:
  - source: student
    target: course
    type: enrolled_in
```

### Knowledge Graph

Nodes and edges representing actual instances and connections.

```python
from apos import KnowledgeGraph, Entity

graph = KnowledgeGraph()
graph.add_node("student_001", Entity(id="student", attrs={"name": "Alice"}))
graph.add_node("course_101", Entity(id="course", attrs={"name": "Python"}))
graph.add_edge("student_001", "course_101", "enrolled_in")

# Query
edges = graph.get_edges("student_001")  # → [("course_101", "enrolled_in")]
```

### Semantic Scoring

Measures how "complete" and "accurate" your context is. Used as a gate for agent consumption.

**Components:**
- `ontology_coverage`: % of entities defined (e.g., 0.49 = 49% complete)
- `relationship_quality`: % of relationships valid (e.g., 0.95 = 95% valid)
- `data_consistency`: Internal contradiction score (e.g., 0.92 = 92% consistent)

**Overall Score:**
```
Score = (coverage × 0.3) + (relationship_quality × 0.4) + (consistency × 0.3)
```

**Gate:**
- ✅ Score ≥ 0.80: PASS (acceptable for agents)
- ⚠️ Score 0.60-0.80: CONDITIONAL (use with caution)
- ❌ Score < 0.60: FAIL (not ready)

---

## Governance Gates

APOS enforces quality gates to ensure context reliability.

### SemanticGate

Checks that context semantic score meets minimum threshold.

```python
from apos.governance import SemanticGate

gate = SemanticGate(min_score=0.80)
score = gate.evaluate(graph)

if score.passes():
    print("✅ Context is production-ready")
    # Safe to use in agents
else:
    print("❌ Context has issues:")
    for issue in score.issues:
        print(f"  - {issue}")
```

### Audit

Run audits to identify gaps and issues.

```python
from apos.governance import AuditRunner

audit = AuditRunner(ontology, graph)
report = audit.run()

print(f"Entities defined: {report.entities_count}")
print(f"Gaps found: {len(report.gaps)}")
print(f"Recommendations: {report.recommendations}")
```

---

## Configuration

### Governance Configuration

`apos/governance/config.py` defines weights, thresholds, and rules.

```python
# Default config
SEMANTIC_GATE_MIN_SCORE = 0.80
METRIC_WEIGHTS = {
    "ontology_coverage": 0.3,
    "relationship_quality": 0.4,
    "data_consistency": 0.3,
}
```

To customize:
```python
from apos.governance import GovernanceConfig

config = GovernanceConfig(
    min_score=0.85,  # Stricter gate
    weights={"coverage": 0.2, "quality": 0.5, "consistency": 0.3}
)
gate = SemanticGate(config=config)
```

---

## Integration with Other Projects

### For Meu PDI (and Others)

Once APOS Beta is ready, integrate it like this:

```python
# In your application code
from apos import Ontology, KnowledgeGraph, SemanticGate
from apos.loader import OntologyLoader

# 1. Load your domain ontology
ontology = OntologyLoader.from_yaml("data/ontologies/student_journey.yaml")

# 2. Build knowledge graph with your data
graph = KnowledgeGraph()
graph.load_ontology(ontology)
# ... populate with your data ...

# 3. Validate with gate
gate = SemanticGate(min_score=0.80)
score = gate.evaluate(graph)

# 4. Pass to agents if gate passes
if score.passes():
    context = prepare_agent_context(graph)
    agent.execute(context)
else:
    log_governance_violation(score)
```

See `docs/INTEGRATION.md` for detailed setup.

---

## API Reference

### Quick Reference

| Class/Function | Purpose | Example |
|---|---|---|
| `Ontology` | Domain model | `ontology.add_entity(Entity(...))` |
| `KnowledgeGraph` | Graph structure | `graph.add_node("id", entity)` |
| `SemanticGate` | Quality gate | `gate.evaluate(graph)` |
| `OntologyLoader` | Load from YAML/JSON | `OntologyLoader.from_yaml(path)` |
| `AuditRunner` | Run audits | `audit.run()` |

See `docs/API.md` for full reference.

---

## Documentation

| Document | Purpose |
|---|---|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, component roles, data flow |
| [API.md](docs/API.md) | Detailed API reference (classes, methods, examples) |
| [INTEGRATION.md](docs/INTEGRATION.md) | How to use APOS in your project |
| [GOVERNANCE.md](docs/GOVERNANCE.md) | How gates & audits work |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Contributing, code style, testing |

---

## Release Management

APOS includes a built-in Release Management framework for structuring product development in releases and sprints.

```bash
# Sprint lifecycle
python -m apos init-sprint --sprint sprint-0.2 --release R0   # Create sprint structure
python -m apos daily --sprint sprint-0.0 --mode automatic     # Run daily standup
python -m apos validate-sprint --sprint-root docs/releases/R0/sprint-0.0/  # Validate tracking
```

Each sprint directory enforces a consistent structure (mirroring Sprint 0.0):

```
docs/releases/R0/sprint-0.2/
├── README.md              # Sprint context
├── TASKS.md               # Task breakdown
├── USER_STORIES.md        # User stories
├── BOARD.md               # Kanban board
├── STATUS.md              # Burndown & metrics
├── RISK_MITIGATION.md     # Risk register
├── RETRO.md               # Retrospective
└── DAILY_STANDUP_*.md     # Daily updates
```

This structure is **enforced by the kernel** — every sprint created via `init-sprint` generates all 8 artifacts with template content, ensuring consistency across releases.

See [docs/releases/R0/](docs/releases/R0/) and [docs/RELEASE_MANAGEMENT_FRAMEWORK.md](docs/RELEASE_MANAGEMENT_FRAMEWORK.md) for detailed documentation.

---

## Roadmap

### Current Status: R0 (Sprint 0.0 ✅ + Sprint 0.1 ✅ + Sprint 0.2 ✅)

| Sprint | Theme | Status |
|--------|-------|--------|
| **0.0** | Bootstrap + Core Scaffolding | ✅ MERGED to develop |
| **0.1** | Platform Identity (Value Prop, OKR, Roadmap) | ✅ COMPLETE (+500% velocity) |
| **0.2** | JTBD Deep Dive (5 interviews, market validation) | ✅ COMPLETE (7/7 tasks, Decisao: VERDE) |
| **0.3** | Semantic Layer | 📅 NEXT |

### JTBD Discovery Results (Sprint 0.2)

5 personas entrevistadas (PM Leader, EM, AI Architect, Product Ops, Early Adopter):
- **Push:** 30-40% retrabalho por contexto desatualizado, 60-80h/mes em roll-up manual
- **Pull:** Trust score 0.0-1.0, automacao Task→OKR→Metrica, plugin Jira
- **Decisao:** VERDE ✅ — prosseguir para Beta Prep (Sprint 0.3)
- **Early adopters:** 4/5 interessados em piloto
- **Job:** Priorizar com base em dados em vez de achismo

### Phase 2: Core Implementation (Sprint 0.3+)
- [ ] Migrate `ontology.py` from Meu PDI
- [ ] Migrate `graph.py` from Meu PDI
- [ ] Migrate `semantic.py` + scoring logic
- [ ] Write unit tests (target 80%+ coverage)
- [ ] Document API

### Phase 3: Governance (Week 3-4)
- [ ] Migrate `gate.py` + governance rules
- [ ] Migrate audit framework
- [ ] Integration tests with real data
- [ ] Document governance gates

### Phase 4: Polish & Release (Week 4)
- [ ] Loader implementations (YAML, JSON)
- [ ] Example integrations
- [ ] Full documentation
- [ ] Tag `v0.1.0-beta`

**Target**: Beta ready by EOD Sprint 0.1 (~2-3 weeks)

---

## Versioning

APOS follows semantic versioning:

- **0.x.y-beta**: Pre-release. Breaking changes OK (document in CHANGELOG)
- **1.0.0+**: Production. Stable API, semantic versioning enforced

Current version: `0.1.0-beta` (see `apos/__init__.py`)

---

## License & Ownership

**License**: Proprietary (not open source yet)

**Owner**: Jader Greiner  
**Contact**: jadergreiner@gmail.com

APOS is a strategic asset. Not for public distribution or commercial licensing (yet).

---

## Getting Help

### For Development Issues

1. Check `docs/DEVELOPMENT.md` for common patterns
2. Run `pytest -v` to see detailed test output
3. Check GitHub Issues: https://github.com/jadergreiner/APOS/issues

### For Architecture Questions

See `docs/ARCHITECTURE.md` or open a GitHub Discussion.

### For Integration Help

See `docs/INTEGRATION.md` or examples in `examples/`.

---

## Common Commands

```bash
# Setup
git clone https://github.com/jadergreiner/APOS.git && cd APOS
python3 -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# Development
pytest                           # Run all tests
pytest --cov=apos tests/         # With coverage
black apos/ tests/ && flake8 apos/  # Format & lint
python examples/basic_usage.py   # Run example

# Commit
git add . && git commit -m "feat: description"
git push origin feature-branch

# Release (later)
pip install wheel
python setup.py sdist bdist_wheel
# Upload to PyPI or private registry
```

---

## Contributing

APOS is in active development. Contributions welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests first (TDD)
4. Commit changes (`git commit -m 'feat: add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

See `docs/DEVELOPMENT.md` for detailed contribution guidelines.

---

## Frequently Asked Questions

### Q: When will APOS be open source?
**A:** Not yet. It's proprietary during Beta. May open-source after v1.0 if strategic fit.

### Q: Can I use APOS in my project now?
**A:** Yes, if it's Meu PDI or an authorized use case. Private consumption only until v1.0.

### Q: What about other languages (TypeScript, Go)?
**A:** Python first. SDKs for other languages are post-v1.0 (P2).

### Q: How do I report a bug?
**A:** Open an issue on GitHub: https://github.com/jadergreiner/APOS/issues

### Q: Can I contribute?
**A:** Yes! See `docs/DEVELOPMENT.md` and open a PR.

---

## Contact & Support

- **Author**: Jader Greiner (jadergreiner@gmail.com)
- **Repository**: https://github.com/jadergreiner/APOS
- **Issues**: https://github.com/jadergreiner/APOS/issues
- **Discussions**: https://github.com/jadergreiner/APOS/discussions

---

**APOS: Precision for AI Agents**

Made with ❤️ to eliminate hallucination, rework, and token waste in AI-driven development.

*Last Updated: 2026-07-20*  
*Current Version: 0.1.0-beta*
