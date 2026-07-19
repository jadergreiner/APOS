# ONTOLOGY.md — APOS Domain Model

**Status**: In Development (R0-Sprint 0.0)

## Overview

This document formalizes APOS's core domain model — the concepts, relationships, and semantic structures that define what APOS manages.

## Core Entities

### 1. **Ontology**
- **Definition**: Formal specification of domain concepts, their properties, and relationships
- **Purpose**: Serves as the schema/blueprint for knowledge graphs
- **Properties**:
  - `id`: Unique identifier
  - `name`: Human-readable name
  - `version`: Semantic versioning
  - `entities`: Collection of Entity definitions
  - `relationships`: Collection of Relationship templates
  - `hierarchies`: Classification structures
  - `created_at`: ISO timestamp
  - `updated_at`: ISO timestamp

### 2. **Entity**
- **Definition**: A concept in the domain (e.g., Student, Course, Project)
- **Purpose**: Represents a class of things that can exist in the knowledge graph
- **Properties**:
  - `id`: Unique identifier within ontology
  - `name`: Entity type name (PascalCase)
  - `description`: What this entity represents
  - `attributes`: List of Attribute objects
  - `is_abstract`: Boolean (abstract entities can't be instantiated)
  - `parent_entity`: Optional reference to parent for hierarchies

### 3. **Attribute**
- **Definition**: A property/field of an Entity
- **Purpose**: Describes what information an entity can hold
- **Properties**:
  - `name`: Attribute name (snake_case)
  - `type`: Data type (string, integer, boolean, datetime, etc.)
  - `required`: Boolean (must have a value)
  - `default`: Optional default value
  - `description`: What this attribute represents
  - `constraints`: Optional validation rules

### 4. **Relationship**
- **Definition**: A connection between two entities
- **Purpose**: Captures how entities relate to each other
- **Properties**:
  - `id`: Unique identifier within ontology
  - `name`: Relationship type (snake_case)
  - `from_entity`: Source entity type
  - `to_entity`: Target entity type
  - `cardinality`: 1-to-1, 1-to-many, many-to-many
  - `description`: Semantic meaning
  - `required`: Boolean (must exist for instances)

### 5. **Node** (Knowledge Graph)
- **Definition**: Instance of an Entity in a Knowledge Graph at runtime
- **Purpose**: Represents actual data/entity instances
- **Properties**:
  - `id`: Unique identifier in graph
  - `entity_type`: Reference to Entity definition
  - `attributes`: Actual attribute values
  - `created_at`: ISO timestamp
  - `updated_at`: ISO timestamp

### 6. **Edge** (Knowledge Graph)
- **Definition**: Instance of a Relationship in a Knowledge Graph at runtime
- **Purpose**: Connects two Nodes according to a Relationship template
- **Properties**:
  - `id`: Unique identifier in graph
  - `relationship_type`: Reference to Relationship definition
  - `from_node`: Source Node ID
  - `to_node`: Target Node ID
  - `metadata`: Optional custom properties
  - `created_at`: ISO timestamp

## Core Relationships

### Ontology → Entities
- **Type**: `defines`
- **Cardinality**: 1-to-many (one ontology defines multiple entities)
- **Meaning**: An Ontology formally specifies what entity types exist

### Entity → Attributes
- **Type**: `has_attribute`
- **Cardinality**: 1-to-many (one entity has multiple attributes)
- **Meaning**: An Entity is composed of Attributes

### Ontology → Relationships
- **Type**: `defines_relationship`
- **Cardinality**: 1-to-many
- **Meaning**: An Ontology formally specifies what relationship types exist

### Entity → Entity (Hierarchy)
- **Type**: `generalizes` / `specializes`
- **Cardinality**: many-to-1 (many specific entities specialize one abstract entity)
- **Meaning**: Inheritance/hierarchy structure

## Semantic Structures

### Hierarchy Pattern
```
Entity (abstract)
├── Entity (child)
│   └── Attributes specific to this specialization
└── Entity (child)
    └── Attributes specific to this specialization
```

### Relationship Constraints
- **Mandatory**: Relationship must exist for instance to be valid
- **Optional**: Relationship may be absent
- **Functional**: At most one target for given source
- **Inverse Functional**: At most one source for given target
- **Reflexive**: Entity can relate to instances of same type

## APOS-Specific Entities

### Release
- **Definition**: Versioned release with defined scope, timeline, and goals
- **Attributes**: `id`, `name`, `version`, `status`, `start_date`, `end_date`, `goals`
- **Relationships**: `contains` (Sprints), `achieves` (OKRs)

### Sprint
- **Definition**: Time-boxed container for work
- **Attributes**: `id`, `number`, `start_date`, `end_date`, `capacity`
- **Relationships**: `part_of` (Release), `contains` (Backlog Items)

### BacklogItem
- **Definition**: Unit of work (story, bug, task)
- **Attributes**: `id`, `title`, `description`, `priority`, `status`, `estimate`
- **Relationships**: `in_sprint` (Sprint), `blocked_by` (other BacklogItem)

### OKR
- **Definition**: Objective & Key Result for strategic alignment
- **Attributes**: `id`, `objective`, `key_results[]`, `owner`, `quarter`
- **Relationships**: `achieved_by` (Release), `measures` (capability)

## Validation Rules

1. **Uniqueness**: Entity IDs are unique within an ontology
2. **Referential Integrity**: Relationships can only reference defined entities
3. **Cardinality**: Relationship instances must respect cardinality constraints
4. **Attribute Types**: Attribute values must match declared type
5. **Acyclicity**: Circular inheritance hierarchies are forbidden

## Evolution

Ontologies can evolve through:
- **Add**: New entities, attributes, relationships
- **Deprecate**: Mark elements as deprecated but keep for compatibility
- **Remove**: Delete unused elements (breaking change)
- **Modify**: Change properties (cardinality, constraints) with care

Version changes:
- **Patch** (0.0.1 → 0.0.2): Non-breaking additions, deprecations
- **Minor** (0.1.0 → 0.2.0): Backward-compatible changes
- **Major** (1.0.0 → 2.0.0): Breaking changes (removals, constraint tightening)

## Example: Student Learning Platform

```
Entities:
  - Student
    - id, name, email, enrollment_date
  - Course
    - id, title, description, credits, max_capacity
  - Instructor
    - id, name, department, email

Relationships:
  - Student enrolled_in Course (many-to-many)
  - Instructor teaches Course (many-to-many)
  - Student submits Assignment (many-to-many)
  - Assignment belongs_to Course (many-to-1)
```

## Next Steps

1. **R0-Sprint 0.1**: Formalize APOS's own ontology (Release, Sprint, OKR, etc.)
2. **R0-Sprint 0.2**: Implement OntologyLoader to parse YAML ontology files
3. **R0-Sprint 0.3**: Add validation rules and constraint checking
4. **R1**: Enable dynamic ontology composition (ontology references other ontologies)

---

**Owner**: Jader Greiner  
**Last Updated**: 2026-07-19  
**Related**: [SEMANTIC_LAYER.md](SEMANTIC_LAYER.md), [GOVERNANCE.md](GOVERNANCE.md)
