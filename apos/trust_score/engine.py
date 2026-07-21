"""
Trust Score Engine

Calcula um score de confiança (0.0-1.0) que mede quanto do trabalho (tasks)
está estrategicamente alinhado com objetivos (OKRs).

Formula:
  Trust Score = (0.3 × coverage) + (0.5 × quality) + (0.2 × consistency)

Componentes:
  - Coverage (30%): Percentual de tasks vinculadas a um OKR
  - Quality (50%): Validade das relações Task→OKR + data freshness
  - Consistency (20%): Ausência de conflitos (task vinculada a OKRs contraditórios)

Referencia: SPEC.md Seção 4.3 + NORTH_STAR.md (Task→OKR→Metric alignment)
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import json


@dataclass
class Task:
    """Representação de uma tarefa (e.g., JIRA issue)"""
    id: str
    title: str
    status: str  # backlog, in_progress, in_review, done
    project_id: str
    okr_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OKR:
    """Representação de um Objetivo-Chave (OKR)"""
    id: str
    name: str
    project_id: str
    target_date: Optional[datetime] = None
    created_at: Optional[datetime] = None


@dataclass
class Relationship:
    """Relação Task→OKR"""
    task_id: str
    okr_id: str
    confidence: float  # 0.0-1.0 (1.0 = manual, 0.7+ = auto)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class ScoreComponent:
    """Um componente individual da pontuação"""
    name: str  # "coverage", "quality", "consistency"
    value: float  # 0.0-1.0
    weight: float  # peso na fórmula geral
    details: Dict


@dataclass
class TrustScoreResult:
    """Resultado completo da avaliação de confiança"""
    score: float  # 0.0-1.0
    components: Dict[str, ScoreComponent]
    issues: List[str]  # Problemas identificados
    orphan_count: int  # Quantas tasks sem OKR
    total_tasks: int
    recommendation: str  # Ação sugerida


class TrustScoreEngine:
    """
    Motor de cálculo de Trust Score.

    Uso:
        engine = TrustScoreEngine(
            tasks=[...],
            okrs=[...],
            relationships=[...]
        )
        result = engine.calculate()
        print(f"Score: {result.score:.2%}")
    """

    def __init__(
        self,
        tasks: List[Task],
        okrs: List[OKR],
        relationships: List[Relationship],
        weights: Optional[Dict[str, float]] = None,
    ):
        """
        Inicializa o engine com dados.

        Args:
            tasks: Lista de tarefas
            okrs: Lista de OKRs
            relationships: Lista de relações Task→OKR
            weights: Pesos customizados (default: coverage=0.3, quality=0.5, consistency=0.2)
        """
        self.tasks = tasks
        self.okrs = okrs
        self.relationships = relationships

        # Pesos da fórmula
        self.weights = weights or {
            "coverage": 0.3,
            "quality": 0.5,
            "consistency": 0.2,
        }

        # Validar que pesos somam 1.0
        total_weight = sum(self.weights.values())
        if abs(total_weight - 1.0) > 0.001:
            raise ValueError(
                f"Pesos devem somar 1.0, mas somam {total_weight}"
            )

        # Build índices para acesso rápido
        self.okr_map = {okr.id: okr for okr in okrs}
        self.task_map = {task.id: task for task in tasks}
        self.rels_by_task = self._build_rels_by_task()

    def calculate(self) -> TrustScoreResult:
        """Calcula o trust score completo."""
        # Calcular componentes
        coverage = self._calculate_coverage()
        quality = self._calculate_quality()
        consistency = self._calculate_consistency()

        # Calcular score combinado
        score = (
            self.weights["coverage"] * coverage.value
            + self.weights["quality"] * quality.value
            + self.weights["consistency"] * consistency.value
        )

        # Identificar problemas
        issues = self._identify_issues()

        # Contar orfas
        orphan_count = len([t for t in self.tasks if t.okr_id is None])

        # Recomendação
        recommendation = self._get_recommendation(
            score, orphan_count, len(self.tasks)
        )

        return TrustScoreResult(
            score=max(0.0, min(1.0, score)),  # Clamp 0-1
            components={
                "coverage": coverage,
                "quality": quality,
                "consistency": consistency,
            },
            issues=issues,
            orphan_count=orphan_count,
            total_tasks=len(self.tasks),
            recommendation=recommendation,
        )

    def _calculate_coverage(self) -> ScoreComponent:
        """
        Coverage (30%): % de tasks vinculadas a um OKR

        Fórmula:
          coverage = len(tasks_with_okr) / len(total_tasks)

        Edge case:
          - Se não há tasks: coverage = 0.0
        """
        if not self.tasks:
            return ScoreComponent(
                name="coverage",
                value=0.0,
                weight=self.weights["coverage"],
                details={
                    "linked_tasks": 0,
                    "total_tasks": 0,
                    "percentage": 0.0,
                },
            )

        linked = len([t for t in self.tasks if t.okr_id])
        total = len(self.tasks)
        coverage_value = linked / total if total > 0 else 0.0

        return ScoreComponent(
            name="coverage",
            value=coverage_value,
            weight=self.weights["coverage"],
            details={
                "linked_tasks": linked,
                "total_tasks": total,
                "percentage": round(coverage_value * 100, 1),
            },
        )

    def _calculate_quality(self) -> ScoreComponent:
        """
        Quality (50%): Validade das relações Task→OKR + data freshness

        Fórmula:
          quality = (valid_relationships / total_relationships) × freshness

        Valid = task existe + OKR existe + não é contraditório
        Freshness = relação atualizada nos últimos 7 dias (0.0 se mais velha)

        Edge case:
          - Se não há relationships: quality = coverage (nenhuma inválida)
        """
        if not self.relationships:
            # Sem relacionamentos = qualidade é baseada só em coverage
            # Se tudo está orfão, qualidade = 1.0 (não há relações inválidas)
            # Se há tasks, presume-se que poderiam ter qualidade
            return ScoreComponent(
                name="quality",
                value=1.0,
                weight=self.weights["quality"],
                details={
                    "valid_relationships": 0,
                    "total_relationships": 0,
                    "freshness_score": 1.0,
                    "invalid_relationships": [],
                },
            )

        # Validar cada relationship
        valid_rels = 0
        invalid_rels = []
        freshness_scores = []

        for rel in self.relationships:
            is_valid = (
                rel.task_id in self.task_map
                and rel.okr_id in self.okr_map
            )

            if is_valid:
                valid_rels += 1
                # Calcular freshness (0.0 se mais de 7 dias, 1.0 se recente)
                freshness = self._calculate_freshness(rel.updated_at)
                freshness_scores.append(freshness)
            else:
                invalid_rels.append(
                    f"{rel.task_id} → {rel.okr_id} "
                    f"(task existe: {rel.task_id in self.task_map}, "
                    f"okr existe: {rel.okr_id in self.okr_map})"
                )

        # Quality = (valid / total) × avg(freshness)
        validity_score = valid_rels / len(self.relationships) if self.relationships else 0.0
        freshness_avg = (
            sum(freshness_scores) / len(freshness_scores)
            if freshness_scores
            else 0.0
        )
        quality_value = validity_score * freshness_avg

        return ScoreComponent(
            name="quality",
            value=quality_value,
            weight=self.weights["quality"],
            details={
                "valid_relationships": valid_rels,
                "total_relationships": len(self.relationships),
                "validity_percentage": round(validity_score * 100, 1),
                "freshness_score": round(freshness_avg, 2),
                "invalid_relationships": invalid_rels,
            },
        )

    def _calculate_consistency(self) -> ScoreComponent:
        """
        Consistency (20%): Ausência de conflitos nas vinculações

        Fórmula:
          consistency = 1.0 - (conflicts / total_relationships)

        Conflito = task vinculada a 2+ OKRs (apenas 1 é esperado, múltiplos é risco)

        Edge case:
          - Se não há relationships: consistency = 1.0 (perfeito)
        """
        if not self.relationships:
            return ScoreComponent(
                name="consistency",
                value=1.0,
                weight=self.weights["consistency"],
                details={
                    "conflicts": 0,
                    "total_relationships": 0,
                    "conflicting_tasks": [],
                },
            )

        # Contar tasks vinculadas a múltiplos OKRs
        task_okr_count: Dict[str, int] = {}
        for rel in self.relationships:
            task_okr_count[rel.task_id] = task_okr_count.get(rel.task_id, 0) + 1

        # Identificar conflitos (task com 2+ OKRs)
        conflicts = 0
        conflicting_tasks = []
        for task_id, count in task_okr_count.items():
            if count > 1:
                conflicts += 1
                okrs = [
                    rel.okr_id
                    for rel in self.relationships
                    if rel.task_id == task_id
                ]
                conflicting_tasks.append(f"{task_id} vinculada a {count} OKRs: {okrs}")

        consistency_value = (
            1.0 - (conflicts / len(self.relationships))
            if self.relationships
            else 1.0
        )

        return ScoreComponent(
            name="consistency",
            value=consistency_value,
            weight=self.weights["consistency"],
            details={
                "conflicts": conflicts,
                "total_relationships": len(self.relationships),
                "conflict_percentage": round(
                    (conflicts / len(self.relationships) * 100) if self.relationships else 0, 1
                ),
                "conflicting_tasks": conflicting_tasks,
            },
        )

    def _calculate_freshness(self, updated_at: Optional[datetime]) -> float:
        """
        Calcula freshness de um relacionamento.

        1.0 se atualizado nos últimos 7 dias
        0.0 se mais antigo ou nunca atualizado
        """
        if updated_at is None:
            return 0.0

        days_old = (datetime.utcnow() - updated_at).days
        if days_old <= 7:
            return 1.0
        elif days_old <= 14:
            return 0.5
        else:
            return 0.0

    def _identify_issues(self) -> List[str]:
        """Identifica problemas na confiança."""
        issues = []

        # Issue 1: Muitas tasks orfas
        orphan_count = len([t for t in self.tasks if t.okr_id is None])
        orphan_pct = (orphan_count / len(self.tasks) * 100) if self.tasks else 0
        if orphan_pct > 30:
            issues.append(
                f"🚨 {orphan_count} tasks ({orphan_pct:.0f}%) sem OKR (orfas)"
            )

        # Issue 2: Tasks completadas sem OKR (HIGH RISK)
        done_orphans = [
            t.id
            for t in self.tasks
            if t.okr_id is None and t.status == "done"
        ]
        if done_orphans:
            issues.append(
                f"🚨 {len(done_orphans)} tasks completadas sem OKR: {', '.join(done_orphans[:3])}..."
            )

        # Issue 3: Relacionamentos inválidos
        invalid_rels = [
            rel
            for rel in self.relationships
            if rel.task_id not in self.task_map or rel.okr_id not in self.okr_map
        ]
        if invalid_rels:
            issues.append(
                f"⚠️ {len(invalid_rels)} relacionamentos inválidos (task ou OKR não existe)"
            )

        # Issue 4: Relacionamentos desatualizados
        stale_rels = [
            rel
            for rel in self.relationships
            if rel.updated_at
            and (datetime.utcnow() - rel.updated_at).days > 14
        ]
        if stale_rels:
            issues.append(
                f"⚠️ {len(stale_rels)} relacionamentos desatualizados (>14 dias)"
            )

        # Issue 5: Conflitos de vinculação
        task_okr_count = {}
        for rel in self.relationships:
            task_okr_count[rel.task_id] = (
                task_okr_count.get(rel.task_id, 0) + 1
            )
        conflicts = [t for t, c in task_okr_count.items() if c > 1]
        if conflicts:
            issues.append(
                f"⚠️ {len(conflicts)} tasks vinculadas a múltiplos OKRs"
            )

        return issues

    def _get_recommendation(
        self, score: float, orphan_count: int, total_tasks: int
    ) -> str:
        """Gera recomendação baseada no score."""
        if score >= 0.85:
            return "✅ Excelente alinhamento estratégico. Continuar monitorando."
        elif score >= 0.70:
            return f"🟡 Bom alinhamento, mas {orphan_count} tasks precisam de contexto OKR."
        elif score >= 0.50:
            return f"⚠️ Alinhamento fraco. Vincule {orphan_count} tasks orfas a OKRs."
        else:
            return f"🚨 Alinhamento crítico. {orphan_count}/{total_tasks} tasks sem propósito estratégico claro."

    def _build_rels_by_task(self) -> Dict[str, List[Relationship]]:
        """Constrói índice para acesso rápido de rels por task."""
        rels_by_task: Dict[str, List[Relationship]] = {}
        for rel in self.relationships:
            if rel.task_id not in rels_by_task:
                rels_by_task[rel.task_id] = []
            rels_by_task[rel.task_id].append(rel)
        return rels_by_task

    def to_json(self) -> str:
        """Serializa resultado para JSON."""
        result = self.calculate()
        return json.dumps(
            {
                "score": round(result.score, 3),
                "components": {
                    name: {
                        "value": round(comp.value, 3),
                        "weight": round(comp.weight, 3),
                        "details": comp.details,
                    }
                    for name, comp in result.components.items()
                },
                "issues": result.issues,
                "orphan_count": result.orphan_count,
                "total_tasks": result.total_tasks,
                "recommendation": result.recommendation,
            },
            indent=2,
        )


__all__ = [
    "Task",
    "OKR",
    "Relationship",
    "ScoreComponent",
    "TrustScoreResult",
    "TrustScoreEngine",
]
