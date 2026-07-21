#!/usr/bin/env python3
"""
APOS T0.3.5 Pilot Demo — Trust Score com Dados Reais do Jira

Demo inline que mostra Trust Score em ação com dados mock
baseados no seu board SCRUM real.
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class Task:
    id: str
    title: str
    status: str
    project_id: str
    okr_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class OKR:
    id: str
    name: str
    project_id: str


@dataclass
class Relationship:
    task_id: str
    okr_id: str
    confidence: float = 1.0
    updated_at: Optional[datetime] = None


def calculate_trust_score(tasks: List[Task], okrs: List[OKR], relationships: List[Relationship]) -> Dict:
    """Calcula Trust Score com 3 componentes"""

    # 1. COVERAGE (30%): % de tasks vinculadas
    if tasks:
        linked = len([t for t in tasks if t.okr_id])
        coverage = linked / len(tasks)
    else:
        coverage = 0.0

    # 2. QUALITY (50%): validade + freshness
    if relationships:
        okr_map = {okr.id: okr for okr in okrs}
        task_map = {task.id: task for task in tasks}

        valid_rels = 0
        freshness_scores = []

        for rel in relationships:
            is_valid = rel.task_id in task_map and rel.okr_id in okr_map
            if is_valid:
                valid_rels += 1
                # Freshness: 1.0 se <7 dias, 0.0 se >7 dias
                if rel.updated_at:
                    days_old = (datetime.utcnow() - rel.updated_at).days
                    if days_old <= 7:
                        freshness_scores.append(1.0)
                    elif days_old <= 14:
                        freshness_scores.append(0.5)
                    else:
                        freshness_scores.append(0.0)
                else:
                    freshness_scores.append(0.0)

        validity_score = valid_rels / len(relationships) if relationships else 0.0
        freshness_avg = sum(freshness_scores) / len(freshness_scores) if freshness_scores else 0.0
        quality = validity_score * freshness_avg
    else:
        quality = 1.0  # Sem relacionamentos = perfeito (nada inválido)

    # 3. CONSISTENCY (20%): sem conflitos
    if relationships:
        task_okr_count = {}
        for rel in relationships:
            task_okr_count[rel.task_id] = task_okr_count.get(rel.task_id, 0) + 1

        conflicts = len([t for t, c in task_okr_count.items() if c > 1])
        consistency = 1.0 - (conflicts / len(relationships)) if relationships else 1.0
    else:
        consistency = 1.0

    # Score final
    score = 0.3 * coverage + 0.5 * quality + 0.2 * consistency
    score = max(0.0, min(1.0, score))  # Clamp 0-1

    # Issues
    issues = []
    orphan_count = len([t for t in tasks if t.okr_id is None])
    orphan_pct = (orphan_count / len(tasks) * 100) if tasks else 0
    if orphan_pct > 30:
        issues.append(f"[CRITICAL] {orphan_count} tasks ({orphan_pct:.0f}%) sem OKR (orfas)")

    done_orphans = [t.id for t in tasks if t.okr_id is None and t.status == "done"]
    if done_orphans:
        issues.append(f"[CRITICAL] {len(done_orphans)} tasks completadas sem OKR")

    return {
        "score": score,
        "components": {
            "coverage": {"value": coverage, "weight": 0.3, "count": len([t for t in tasks if t.okr_id])},
            "quality": {"value": quality, "weight": 0.5},
            "consistency": {"value": consistency, "weight": 0.2},
        },
        "stats": {
            "total_tasks": len(tasks),
            "orphan_count": orphan_count,
            "linked_count": len([t for t in tasks if t.okr_id]),
            "relationships": len(relationships),
        },
        "issues": issues,
        "recommendation": _get_recommendation(score, orphan_count, len(tasks)),
    }


def _get_recommendation(score: float, orphan_count: int, total_tasks: int) -> str:
    """Gera recomendação baseada no score"""
    if score >= 0.85:
        return "[OK] Excelente alinhamento estrategico. Continuar monitorando."
    elif score >= 0.70:
        return f"[MEDIUM] Bom alinhamento, mas {orphan_count} tasks precisam de contexto OKR."
    elif score >= 0.50:
        return f"[WARNING] Alinhamento fraco. Vincule {orphan_count} tasks orfas a OKRs."
    else:
        return f"[CRITICAL] Alinhamento critico. {orphan_count}/{total_tasks} tasks sem proposito estrategico claro."


def main():
    """Executa demo com dados MOCK baseados no Jira real"""

    print("=" * 70)
    print("APOS T0.3.5 PILOT - TRUST SCORE COM DADOS REAIS DO JIRA")
    print("=" * 70)
    print()

    # Dados mock baseados no seu board SCRUM real
    tasks = [
        Task(
            id="SCRUM-1",
            title="T0.3.1 - Especificacao Tecnica (SPEC.md)",
            status="a_fazer",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-001",  # Vinculada
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 23),
        ),
        Task(
            id="SCRUM-2",
            title="Tarefa 2 - User Story",
            status="em_andamento",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-001",  # Vinculada
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 23),
        ),
        Task(
            id="SCRUM-3",
            title="Implementation Task - Feature A",
            status="backlog",
            project_id="SCRUM",
            okr_id=None,  # ORFÃ!
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 22),
        ),
        Task(
            id="SCRUM-4",
            title="Bug Fix - Critical Performance",
            status="em_andamento",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-002",  # Vinculada
            created_at=datetime(2026, 7, 21),
            updated_at=datetime(2026, 7, 23),
        ),
        Task(
            id="SCRUM-5",
            title="Deploy em sandbox + onboarding (Piloto)",
            status="a_fazer",
            project_id="SCRUM",
            okr_id=None,  # ORFÃ!
            created_at=datetime(2026, 7, 23),
            updated_at=datetime(2026, 7, 23),
        ),
    ]

    okrs = [
        OKR(id="OKR-2026-Q3-001", name="Validar MVP com pilotos", project_id="SCRUM"),
        OKR(id="OKR-2026-Q3-002", name="Melhorar performance P95", project_id="SCRUM"),
    ]

    relationships = [
        Relationship(
            task_id="SCRUM-1",
            okr_id="OKR-2026-Q3-001",
            confidence=1.0,
            updated_at=datetime.utcnow(),
        ),
        Relationship(
            task_id="SCRUM-2",
            okr_id="OKR-2026-Q3-001",
            confidence=1.0,
            updated_at=datetime.utcnow(),
        ),
        Relationship(
            task_id="SCRUM-4",
            okr_id="OKR-2026-Q3-002",
            confidence=1.0,
            updated_at=datetime.utcnow(),
        ),
    ]

    print(f"DADOS CARREGADOS:")
    print(f"   * {len(tasks)} tasks (do seu board SCRUM)")
    print(f"   * {len(okrs)} OKRs")
    print(f"   * {len(relationships)} relacionamentos Task->OKR")
    print()

    # Calcula Trust Score
    result = calculate_trust_score(tasks, okrs, relationships)

    # Exibe resultados
    print("=" * 70)
    print("TRUST SCORE CALCULADO")
    print("=" * 70)
    print()

    score = result["score"]
    print(f"SCORE FINAL: {score:.1%}")
    print()

    print("BREAKDOWN DOS COMPONENTES:")
    for comp_name, comp_data in result["components"].items():
        value = comp_data["value"]
        weight = comp_data["weight"]
        contribution = value * weight
        print(f"   * {comp_name.upper():12} {value:6.1%}  (weight: {weight:.1%}, contribui: {contribution:6.1%})")
    print()

    print("ESTATISTICAS:")
    stats = result["stats"]
    print(f"   * Total tasks:        {stats['total_tasks']}")
    print(f"   * Vinculadas a OKR:   {stats['linked_count']} ({stats['linked_count']/stats['total_tasks']*100:.0f}%)")
    print(f"   * Orfas (sem OKR):    {stats['orphan_count']} ({stats['orphan_count']/stats['total_tasks']*100:.0f}%)")
    print()

    if result["issues"]:
        print("ISSUES DETECTADAS:")
        for issue in result["issues"]:
            print(f"   {issue}")
        print()

    print("RECOMENDACAO:")
    print(f"   {result['recommendation']}")
    print()

    # Detalhes por task
    print("=" * 70)
    print("DETALHES POR TASK")
    print("=" * 70)
    print()

    for task in tasks:
        status = "[OK]" if task.okr_id else "[ORPHAN]"
        okr_info = f"-> {task.okr_id}" if task.okr_id else "(SEM OKR)"
        print(f"{status} {task.id:8} | {task.title:45} | {task.status:15} {okr_info}")
    print()

    # JSON export
    print("=" * 70)
    print("JSON OUTPUT (Para Integração)")
    print("=" * 70)
    print()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
