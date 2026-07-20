# SEMANTIC_LAYER.md — APOS Semantic Scoring & Pontuação

**Status**: In Development (R0-Sprint 0.0)

## Overview

The Semantic Layer is APOS's quality control mechanism. It continuously evaluates how well a Knowledge Graph represents its domain through **semantic scoring** — a formal measure of context completeness, accuracy, and consistency.

Instead of binary pass/fail, APOS gives nuanced scores (0.0-1.0) to guide AI agents on confidence in context.

## Why Semantic Scoring?

Traditional systems either trust all data or trust none. APOS says: "**Here's exactly how confident I am in this context.**"

This enables:
- **AI agents** to make decisions proportional to confidence
- **Governance gates** to enforce quality thresholds  
- **Improvement tracking** to measure when context gets better
- **Root cause analysis** to see what's missing or broken

## Scoring Framework

### Components of a Semantic Score

A semantic score = **weighted combination** of:

1. **Ontology Coverage** (weight: 30%)
   - Percentage of defined entity types that have at least one instance
   - Formula: `instances_with_type / total_entity_types`
   - Example: 5 of 8 entity types have data → 62.5% coverage

2. **Relationship Quality** (weight: 35%)
   - Percentage of mandatory relationships that are populated
   - Formula: `populated_required_edges / total_required_edges`
   - Example: 12 of 15 required relationships exist → 80% quality

3. **Data Consistency** (weight: 35%)
   - Percentage of data that passes domain constraints
   - Checks: type correctness, referential integrity, business rule compliance
   - Formula: `valid_attributes / total_attributes`
   - Example: 48 of 50 attributes are valid → 96% consistency

### Calculation

```
Semantic Score = (coverage × 0.30) + (quality × 0.35) + (consistency × 0.35)

Range: 0.0 to 1.0
- 1.0 = Perfect (complete, accurate, consistent)
- 0.75 = Good (minor gaps)
- 0.60 = Acceptable (meaningful gaps)
- 0.40 = Poor (major issues)
- 0.0 = Unusable (critical failures)
```

## Score Interpretation

| Score | Status | AI Agent Behavior | Recommended Action |
|-------|--------|-------------------|--------------------|
| 0.90-1.0 | ✅ Excellent | Use with high confidence | Monitor and maintain |
| 0.75-0.89 | ✅ Good | Use with caution | Address known gaps |
| 0.60-0.74 | ⚠️ Acceptable | Use carefully; flag risks | Prioritize improvements |
| 0.40-0.59 | ❌ Poor | Use only with validation | Major remediation needed |
| 0.0-0.39 | ❌ Unusable | Reject; do not use | Critical fixes required |

## Real Example

### Student Learning Platform

**Ontology**:
- Student (entity type)
- Course (entity type)
- Enrollment (entity type)

**Data State**:
- Students: 100 instances ✓
- Courses: 40 instances ✓
- Enrollments: 200 instances ✓
- All 3 entity types have data → **Coverage = 100%**

**Relationships** (required):
- Student → Enrollment: 200 edges (required) ✓
- Course → Enrollment: 190 edges (required) — missing 10
- 2/3 required relationships fully populated → **Quality = 67%**

**Consistency**:
- Student attributes: 480 valid, 20 invalid (bad email format)
- Course attributes: 120 valid, 0 invalid
- Enrollment attributes: 600 valid, 100 invalid (circular dates)
- 1200/1320 attributes valid → **Consistency = 91%**

**Final Score**:
```
(1.0 × 0.30) + (0.67 × 0.35) + (0.91 × 0.35)
= 0.30 + 0.23 + 0.32
= 0.85 (GOOD)
```

**Interpretation**: "Use with caution; address the 10 missing enrollments and fix 100 bad enrollment dates before relying fully on this context."

## Scoring in Practice

### Continuous Evaluation

Every time data changes:

```python
from apos import KnowledgeGraph, SemanticGate

graph = KnowledgeGraph()
# ... load ontology, add nodes/edges ...

gate = SemanticGate()
score = gate.evaluate(graph)

print(f"Score: {score.overall:.2f}")
print(f"  Coverage: {score.coverage:.2f}")
print(f"  Quality: {score.quality:.2f}")
print(f"  Consistency: {score.consistency:.2f}")
print(f"  Issues: {score.issues}")
```

### Gates & Thresholds

```python
gate = SemanticGate(min_score=0.80)
result = gate.evaluate(graph)

if result.passes():
    context = prepare_agent_context(graph)
    agent.execute(context)
else:
    print(f"Context quality insufficient: {result.score:.2f} < {result.threshold}")
    print(f"Fix these: {result.issues}")
```

## Customization

Projects can customize scoring weights:

```python
from apos.governance import GovernanceConfig, SemanticGate

config = GovernanceConfig(
    min_score=0.85,
    weights={
        "coverage": 0.20,      # Less critical if data is sparse
        "quality": 0.50,       # Relationships are critical
        "consistency": 0.30,   # Some flexibility on edge cases
    }
)

gate = SemanticGate(config=config)
```

## Auditing & Improvement

When a score is low, audit tools provide specific recommendations:

```python
from apos.governance import AuditRunner

audit = AuditRunner()
report = audit.audit(graph)

print(f"Score: {report.score:.2f}")
print("Issues found:")
for issue in report.issues:
    print(f"  - {issue.severity}: {issue.message}")
    print(f"    → {issue.recommendation}")
```

Example output:

```
Score: 0.62 (ACCEPTABLE)
Issues found:
  - HIGH: Course entity has 0% coverage
    → Add at least 5 Course instances to increase coverage
  
  - MEDIUM: 45 Student → Course relationships missing
    → Backfill enrollment data from registrar system
  
  - LOW: 15 attributes have null values when required=true
    → Update Student records to include phone_number
```

## Implementation Status (R0)

### Phase 1: Foundation (R0-Sprint 0.0)
- ✅ Define semantic scoring model
- ✅ Document components and formulas
- ⏳ Implement metric calculations

### Phase 2: Core (R0-Sprint 0.1-0.2)
- ⏳ Implement `SemanticGate.evaluate()`
- ⏳ Add customizable weighting
- ⏳ Create audit tools

### Phase 3: Integration (R0-Sprint 0.3)
- ⏳ Hook into project initialization (BootstrapGate)
- ⏳ Add monitoring dashboards
- ⏳ Create improvement playbooks

## Key Design Principles

1. **Transparency**: Scores are never black boxes; components are always visible
2. **Actionability**: Every low score comes with specific remediation steps
3. **Flexibility**: Weights and thresholds are customizable per project
4. **Composability**: Scores combine multiple dimensions into one signal
5. **Evolution**: Scores improve as data and ontology mature

## Related Concepts

- **Knowledge Graph** (apos/core/graph.py): Runtime instances scored by this layer
- **Ontology** (apos/core/ontology.py): Schema that defines what "complete" means
- **Semantic Gate** (apos/governance/gate.py): Enforcement mechanism using scores
- **Audit Runner** (apos/governance/audit.py): Detailed diagnostics and recommendations

---

**Owner**: Jader Greiner  
**Last Updated**: 2026-07-19  
**Related**: [ONTOLOGY.md](ONTOLOGY.md), [GOVERNANCE.md](GOVERNANCE.md), [BOOTSTRAP_GATE.md](BOOTSTRAP_GATE.md)
