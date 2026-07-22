"""
Testes para Trust Score Engine

Cobertura: >80% do engine.py

Cenários testados:
- Projeto vazio (0 tasks)
- Projeto perfeito (todas tasks com OKR)
- Projeto com orfas (tasks sem OKR)
- Relacionamentos inválidos
- Conflitos de vinculação
- Freshness de dados
"""

import pytest
from datetime import datetime, timedelta
from apos.trust_score import (
    TrustScoreEngine,
    Task,
    OKR,
    Relationship,
    TrustScoreResult,
)


class TestTrustScoreEngineBasics:
    """Testes básicos do engine."""

    def test_empty_project(self):
        """Projeto sem tasks: coverage=0, mas quality/consistency=1.0 (nada inválido)"""
        engine = TrustScoreEngine(tasks=[], okrs=[], relationships=[])
        result = engine.calculate()

        # Score = 0.3*0.0 + 0.5*1.0 + 0.2*1.0 = 0.7
        # Interpretação: sem dados = sem problemas de validade/consistência
        assert result.score == 0.7
        assert result.orphan_count == 0
        assert result.total_tasks == 0
        assert result.components["coverage"].value == 0.0
        assert result.components["quality"].value == 1.0
        assert result.components["consistency"].value == 1.0

    def test_perfect_alignment(self):
        """Projeto perfeito (100% coverage, válido, sem conflitos)"""
        tasks = [
            Task(id="T1", title="Feature 1", status="in_progress", project_id="P1", okr_id="OKR-1"),
            Task(id="T2", title="Feature 2", status="in_progress", project_id="P1", okr_id="OKR-2"),
        ]
        okrs = [
            OKR(id="OKR-1", name="Goal 1", project_id="P1"),
            OKR(id="OKR-2", name="Goal 2", project_id="P1"),
        ]
        rels = [
            Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=datetime.utcnow()),
            Relationship(task_id="T2", okr_id="OKR-2", confidence=1.0, updated_at=datetime.utcnow()),
        ]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert result.score == 1.0
        assert result.orphan_count == 0
        assert result.components["coverage"].value == 1.0
        assert result.components["quality"].value == 1.0
        assert result.components["consistency"].value == 1.0
        assert len(result.issues) == 0

    def test_orphans_detection(self):
        """Detectar tasks sem OKR"""
        tasks = [
            Task(id="T1", title="Feature 1", status="in_progress", project_id="P1", okr_id="OKR-1"),
            Task(id="T2", title="Orphan", status="in_progress", project_id="P1", okr_id=None),
        ]
        okrs = [OKR(id="OKR-1", name="Goal 1", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0)]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert result.orphan_count == 1
        assert result.components["coverage"].value == 0.5
        assert "sem OKR" in result.issues[0]

    def test_done_task_without_okr_high_risk(self):
        """Task completada sem OKR = HIGH RISK"""
        tasks = [
            Task(id="T1", title="Done orphan", status="done", project_id="P1", okr_id=None),
        ]
        okrs = []
        rels = []

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert result.orphan_count == 1
        # Deve ter issue de HIGH RISK
        done_orphan_issues = [i for i in result.issues if "completadas sem OKR" in i]
        assert len(done_orphan_issues) > 0


class TestCoverageComponent:
    """Testes do componente Coverage."""

    def test_coverage_calculation(self):
        """Coverage = linked_tasks / total_tasks"""
        tasks = [
            Task(id="T1", title="F1", status="in_progress", project_id="P1", okr_id="OKR-1"),
            Task(id="T2", title="F2", status="in_progress", project_id="P1", okr_id="OKR-1"),
            Task(id="T3", title="F3", status="in_progress", project_id="P1", okr_id=None),
            Task(id="T4", title="F4", status="in_progress", project_id="P1", okr_id=None),
        ]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [
            Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0),
            Relationship(task_id="T2", okr_id="OKR-1", confidence=1.0),
        ]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # 2/4 = 0.5
        assert result.components["coverage"].value == 0.5
        assert result.components["coverage"].details["linked_tasks"] == 2
        assert result.components["coverage"].details["total_tasks"] == 4
        assert result.components["coverage"].details["percentage"] == 50.0


class TestQualityComponent:
    """Testes do componente Quality."""

    def test_quality_with_valid_relationships(self):
        """Quality com relacionamentos válidos e atualizados"""
        now = datetime.utcnow()
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=now)]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # Todas válidas e recentes → quality = 1.0
        assert result.components["quality"].value == 1.0

    def test_quality_with_invalid_relationship(self):
        """Quality com task inválida (não existe)"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [
            Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0),  # válida
            Relationship(task_id="T-INVALID", okr_id="OKR-1", confidence=1.0),  # inválida
        ]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # 1/2 válidas = quality reduzido
        quality_details = result.components["quality"].details
        assert quality_details["valid_relationships"] == 1
        assert quality_details["total_relationships"] == 2
        assert len(quality_details["invalid_relationships"]) == 1

    def test_quality_with_stale_relationships(self):
        """Quality com relacionamentos desatualizados (>7 dias)"""
        now = datetime.utcnow()
        stale = now - timedelta(days=8)

        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=stale)]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # Relacionamento válido mas stale → quality < 1.0
        assert result.components["quality"].value < 1.0


class TestConsistencyComponent:
    """Testes do componente Consistency."""

    def test_consistency_no_conflicts(self):
        """Sem conflitos de vinculação = consistency 1.0"""
        tasks = [
            Task(id="T1", title="F1", status="in_progress", project_id="P1"),
            Task(id="T2", title="F2", status="in_progress", project_id="P1"),
        ]
        okrs = [
            OKR(id="OKR-1", name="Goal 1", project_id="P1"),
            OKR(id="OKR-2", name="Goal 2", project_id="P1"),
        ]
        rels = [
            Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0),
            Relationship(task_id="T2", okr_id="OKR-2", confidence=1.0),
        ]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert result.components["consistency"].value == 1.0
        assert result.components["consistency"].details["conflicts"] == 0

    def test_consistency_with_conflicts(self):
        """Task vinculada a múltiplos OKRs = conflict"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = [
            OKR(id="OKR-1", name="Goal 1", project_id="P1"),
            OKR(id="OKR-2", name="Goal 2", project_id="P1"),
        ]
        rels = [
            Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0),
            Relationship(task_id="T1", okr_id="OKR-2", confidence=1.0),
        ]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # 1 conflito em 2 relacionamentos → consistency = 1.0 - (1/2) = 0.5
        assert result.components["consistency"].value == 0.5
        assert result.components["consistency"].details["conflicts"] == 1
        assert len(result.components["consistency"].details["conflicting_tasks"]) == 1


class TestScoreFormula:
    """Testes da fórmula combinada."""

    def test_formula_weights(self):
        """Verificar que formula usa pesos corretos"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1", okr_id="OKR-1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=datetime.utcnow())]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # score = 0.3*coverage + 0.5*quality + 0.2*consistency
        coverage = result.components["coverage"].value  # 1.0
        quality = result.components["quality"].value    # 1.0
        consistency = result.components["consistency"].value  # 1.0

        expected_score = 0.3 * coverage + 0.5 * quality + 0.2 * consistency
        assert abs(result.score - expected_score) < 0.001

    def test_score_clamped_0_1(self):
        """Score sempre entre 0.0 e 1.0"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = []
        rels = []

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert 0.0 <= result.score <= 1.0


class TestRecommendations:
    """Testes de recomendações geradas."""

    def test_recommendation_excellent(self):
        """Score >= 0.85 → Excelente"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1", okr_id="OKR-1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=datetime.utcnow())]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        assert "Excelente" in result.recommendation

    def test_recommendation_with_orphans(self):
        """Projeto com muitas orfas = recomendação menciona contexto OKR"""
        tasks = [
            Task(id="T1", title="F1", status="done", project_id="P1", okr_id=None),
            Task(id="T2", title="F2", status="in_progress", project_id="P1", okr_id=None),
            Task(id="T3", title="F3", status="in_progress", project_id="P1", okr_id=None),
        ]
        okrs = []
        rels = []

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # Recomendação mencionará tarefas e contexto
        assert "tasks" in result.recommendation and "OKR" in result.recommendation


class TestEdgeCases:
    """Testes de edge cases."""

    def test_weights_validation(self):
        """Pesos devem somar 1.0"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = []
        rels = []

        with pytest.raises(ValueError):
            TrustScoreEngine(
                tasks,
                okrs,
                rels,
                weights={"coverage": 0.3, "quality": 0.4, "consistency": 0.2},  # soma = 0.9
            )

    def test_custom_weights(self):
        """Aceitar pesos customizados (que somem 1.0)"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1", okr_id="OKR-1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=datetime.utcnow())]

        custom_weights = {"coverage": 0.5, "quality": 0.3, "consistency": 0.2}
        engine = TrustScoreEngine(tasks, okrs, rels, weights=custom_weights)
        result = engine.calculate()

        # Com custom weights, score ainda deve ser 1.0 (tudo perfeito)
        assert result.score == 1.0

    def test_relationship_without_update_time(self):
        """Relacionamentos sem update_at devem ter freshness 0.0"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=None)]

        engine = TrustScoreEngine(tasks, okrs, rels)
        result = engine.calculate()

        # Sem update_at → freshness 0.0 → quality reduzido
        assert result.components["quality"].value == 0.0


class TestJSONSerialization:
    """Testes de serialização para JSON."""

    def test_to_json(self):
        """Resultado deve serializar para JSON válido"""
        tasks = [Task(id="T1", title="F1", status="in_progress", project_id="P1", okr_id="OKR-1")]
        okrs = [OKR(id="OKR-1", name="Goal", project_id="P1")]
        rels = [Relationship(task_id="T1", okr_id="OKR-1", confidence=1.0, updated_at=datetime.utcnow())]

        engine = TrustScoreEngine(tasks, okrs, rels)
        json_str = engine.to_json()

        # Deve ser válido JSON
        import json
        data = json.loads(json_str)

        assert "score" in data
        assert "components" in data
        assert "issues" in data
        assert data["orphan_count"] == 0
        assert data["total_tasks"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
