# GOVERNANCE.md — APOS Quality & Compliance Framework

**Status**: In Development (R0-Sprint 0.0)

## Overview

APOS Governance is the quality control system that ensures AI agents have reliable, trustworthy semantic context. It defines **gates, metrics, audit rules, and policies** that maintain high standards for knowledge graphs.

Think of it as the "guardrails" that keep context accurate and complete.

## Governance Layers

### Layer 1: Semantic Gates (Quality Thresholds)

**Purpose**: Enforce minimum quality standards before AI agents can use context

**Mechanism**: 
- Calculate semantic score (coverage, quality, consistency)
- Compare against configurable threshold
- Return PASS, CONDITIONAL, or FAIL

**Configuration**:
```python
from apos.governance import GovernanceConfig

config = GovernanceConfig(
    gates={
        "semantic_quality": {
            "enabled": True,
            "min_score": 0.80,
            "severity": "BLOCK",  # BLOCK, WARN, INFO
        },
        "data_freshness": {
            "enabled": True,
            "max_age_hours": 24,
            "severity": "WARN",
        },
    }
)
```

**Gate Types**:

1. **SemanticGate** (primary)
   - Validates: coverage, quality, consistency
   - Threshold: 0.0-1.0 (default 0.80)
   - Action: PASS/CONDITIONAL/FAIL

2. **FreshnessGate** (data staleness)
   - Validates: how recent data is
   - Threshold: max age in hours
   - Action: WARN if stale

3. **ReferentialIntegrityGate** (data validity)
   - Validates: broken links, orphaned nodes
   - Threshold: max orphaned percentage
   - Action: BLOCK if too many orphaned entities

4. **ComplianceGate** (regulatory)
   - Validates: GDPR, PII handling, access control
   - Threshold: project-specific policies
   - Action: BLOCK if violated

### Layer 2: Audit Framework (Diagnostics)

**Purpose**: Identify root causes of quality issues and recommend fixes

**Mechanism**:
- Deep inspection of knowledge graph
- Check every entity, attribute, relationship
- Categorize issues by severity
- Generate actionable recommendations

**Usage**:
```python
from apos.governance import AuditRunner

audit = AuditRunner()
report = audit.audit(graph)

for issue in report.issues:
    print(f"{issue.severity}: {issue.issue_type}")
    print(f"  Message: {issue.message}")
    print(f"  Affected: {len(issue.affected_items)} items")
    print(f"  Fix: {issue.recommendation}")
```

**Audit Categories**:

1. **Coverage Gaps**
   - Missing entity types
   - Entity types with 0 instances
   - Recommendation: Ingest data for missing types

2. **Relationship Quality**
   - Missing required relationships
   - Low cardinality violations
   - Recommendation: Backfill relationships, verify data source

3. **Consistency Issues**
   - Invalid attribute types
   - Null values when required
   - Circular references
   - Recommendation: Data cleanup, validation rules

4. **Staleness**
   - Data older than threshold
   - Entities not updated recently
   - Recommendation: Trigger refresh from source

5. **Security & Compliance**
   - Exposed PII in attributes
   - Insufficient access controls
   - Recommendation: Apply data masking, update policies

### Layer 3: Metrics & Monitoring

**Purpose**: Track quality over time and identify trends

**Key Metrics**:

1. **Coverage Trend**
   ```
   Day 1: 60% coverage
   Day 3: 70% coverage
   Day 7: 85% coverage
   → Improving (positive trend)
   ```

2. **Quality Index**
   ```
   relationship_quality / (coverage + consistency)
   Higher = relationships are well-populated relative to data volume
   ```

3. **Issue Density**
   ```
   issues_per_1000_nodes
   Should decrease over time as data quality improves
   ```

4. **Gate Pass Rate**
   ```
   (gates_passed / total_gate_evaluations) × 100
   Should be >95% for healthy system
   ```

**Tracking**:
```python
from apos.governance import MetricsCollector

collector = MetricsCollector()

# Evaluate over time
for day in range(7):
    score = gate.evaluate(graph)
    collector.record(date=day, score=score)

# Generate report
report = collector.generate_report()
print(f"7-day trend: {report.trend}")  # IMPROVING, STABLE, DECLINING
print(f"Coverage: {report.coverage_change}%")
print(f"Issues: {report.issue_density} per 1000 nodes")
```

### Layer 4: Governance Policies

**Purpose**: Define project-specific rules beyond standard metrics

**Examples**:

1. **Data Residency Policy**
   ```yaml
   policy: data_residency
   rule: "All EU personal data must be stored in EU region"
   enforcement: BLOCK
   check_frequency: continuous
   ```

2. **PII Masking Policy**
   ```yaml
   policy: pii_masking
   rule: "Email, phone, SSN always masked except for authorized roles"
   enforcement: WARN
   affected_entities: [User, Employee]
   ```

3. **Update Frequency Policy**
   ```yaml
   policy: update_frequency
   rule: "Critical entities must update within 24 hours"
   enforcement: WARN
   affected_entities: [StudentEnrollment, CourseOffering]
   ```

4. **Hierarchy Consistency Policy**
   ```yaml
   policy: hierarchy_constraint
   rule: "No circular inheritance allowed"
   enforcement: BLOCK
   check_on: ontology_modification
   ```

**Adding Custom Policies**:
```python
from apos.governance import PolicyEngine

engine = PolicyEngine()
engine.add_policy(
    name="student_integrity",
    rule=lambda graph: all(
        student.email and student.student_id
        for student in graph.get_nodes("Student")
    ),
    severity="BLOCK",
    message="All students must have email and student_id",
)
```

## Governance Workflows

### Workflow 1: Project Initialization

```
Bootstrap Gate → Validate Foundations → Initialize Governance Config
```

1. Check required foundation documents
2. Extract governance requirements
3. Create default policies
4. Run first audit
5. Generate improvement roadmap

### Workflow 2: Data Ingestion

```
New Data → Validate Schema → Check Gates → Store/Reject
```

1. Incoming data is validated against ontology
2. Semantic gates are evaluated
3. If passes → store in graph
4. If fails → reject with clear feedback
5. Log all gate results for metrics

### Workflow 3: Quality Improvement

```
Low Score → Run Audit → Generate Recommendations → Track Progress
```

1. Semantic gate returns score 0.65 (below threshold)
2. Audit runner identifies root causes
3. Produces prioritized fix list
4. Track as improvements in backlog
5. Re-run audit after fixes to measure improvement

### Workflow 4: Incident Response

```
Gate Fails → Incident Alert → Run Audit → Execute Playbook
```

1. Gate failure triggers alert
2. Quick audit identifies issue type
3. Look up incident playbook (by issue type)
4. Execute playbook steps automatically
5. Escalate if playbook doesn't resolve

## Incident Playbooks

### Playbook: Missing Required Relationship

**Trigger**: Relationship Quality Gate fails

**Symptoms**:
```
10 Student → Enrollment relationships missing
Expected: 100, Actual: 90, Quality: 90%
```

**Diagnosis Steps**:
1. Identify missing relationship type
2. Check source data system
3. Verify transformation logic
4. Check access permissions

**Resolution**:
1. Backfill missing relationships from source
2. Add data validation check to prevent recurrence
3. Trigger alert if >5% relationships missing again

### Playbook: Data Type Mismatch

**Trigger**: Consistency Gate fails

**Symptoms**:
```
CourseCode attribute: expected string, found integer (50 instances)
```

**Diagnosis**:
1. Identify affected entities
2. Check data source
3. Verify transformation

**Resolution**:
1. Coerce to correct type or flag for manual review
2. Update data pipeline to prevent recurrence
3. Add pre-ingestion validation

### Playbook: Circular Inheritance

**Trigger**: Governance Policy violation

**Symptoms**:
```
Entity hierarchy: A → B → C → A (cycle detected)
```

**Diagnosis**:
1. Trace parent references
2. Identify cycle

**Resolution**:
1. Remove circular edge
2. Clarify intended hierarchy
3. Add cycle-detection to schema validation

## Configuration Files

### governance-config.yaml

```yaml
# Governance configuration for project
version: "1.0"

gates:
  semantic_quality:
    enabled: true
    min_score: 0.80
    severity: BLOCK
    check_frequency: continuous

  data_freshness:
    enabled: true
    max_age_hours: 24
    severity: WARN
    check_frequency: hourly

  referential_integrity:
    enabled: true
    max_orphaned_percent: 5
    severity: BLOCK
    check_frequency: continuous

metrics:
  collection_enabled: true
  retention_days: 90
  alert_thresholds:
    coverage_drop_percent: 10  # Alert if coverage drops >10% in 7 days
    issue_density_per_node: 0.05  # Alert if >5% of nodes have issues

policies:
  - name: pii_masking
    enabled: true
    severity: BLOCK
  
  - name: hierarchy_constraint
    enabled: true
    severity: BLOCK

audit:
  auto_run_on_ingest: true
  deep_scan_frequency: weekly
  report_recipients:
    - jadergreiner@gmail.com
```

## Integration with Other Layers

**Semantic Layer** (`SEMANTIC_LAYER.md`):
- Governance uses semantic scores as primary signal
- Customizes weights per project need

**Bootstrap Gate** (`BOOTSTRAP_GATE.md`):
- Governance config is validated during project init
- Creates default policies from foundation documents

**Ontology** (`ONTOLOGY.md`):
- Governance enforces ontology constraints
- Audit checks data against ontology schema

## Implementation Roadmap

### R0-Sprint 0.0 (Foundation)
- ✅ Define governance framework
- ✅ Document gate types and policies
- ✅ Create incident playbooks
- ⏳ Implement SemanticGate enforcement

### R0-Sprint 0.1 (Core Gates)
- ⏳ Implement SemanticGate (semantic scoring + threshold)
- ⏳ Implement AuditRunner (issue detection)
- ⏳ Add governance config loading

### R0-Sprint 0.2 (Advanced Gates)
- ⏳ Implement FreshnessGate, ReferentialIntegrityGate
- ⏳ Add policy engine
- ⏳ Implement metrics collection

### R0-Sprint 0.3 (Observability)
- ⏳ Add alerting (gate failures trigger alerts)
- ⏳ Implement metric dashboards
- ⏳ Auto-execute incident playbooks

## Best Practices

1. **Start conservative, relax carefully**
   - Begin with high thresholds (0.90+)
   - Lower thresholds only after confirming they don't miss issues

2. **Track metrics, not just snapshots**
   - A single score is less useful than a trend
   - Monitor 7-day and 30-day trends

3. **Custom policies for domain-specific rules**
   - Standard gates handle common cases
   - Add custom policies for your domain

4. **Automate incident response**
   - Map issue types to playbooks
   - Execute playbooks automatically when possible
   - Escalate only when playbook doesn't resolve

5. **Audit before assuming**
   - Low score? Always run audit first
   - Don't guess at root cause

---

**Owner**: Jader Greiner  
**Last Updated**: 2026-07-19  
**Related**: [SEMANTIC_LAYER.md](SEMANTIC_LAYER.md), [BOOTSTRAP_GATE.md](BOOTSTRAP_GATE.md), [ONTOLOGY.md](ONTOLOGY.md)
