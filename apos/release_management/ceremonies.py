"""Cerimônias de sprint — estrutura para daily standup, planning e retro."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class DailyStandupUpdate:
    """Um update de um participante em daily standup."""

    participant: str
    date: str  # ISO format
    what_done: str  # O que foi feito ontem
    what_today: str  # O que vai fazer hoje
    blockers: str = ""  # Bloqueadores (se houver)
    notes: str = ""


@dataclass
class DailyStandup:
    """Estrutura de daily standup."""

    sprint_id: str
    date: str  # ISO format (ex: 2026-07-22)
    updates: List[DailyStandupUpdate] = field(default_factory=list)
    summary: str = ""  # Sumário geral
    action_items: List[str] = field(default_factory=list)

    def add_update(self, update: DailyStandupUpdate) -> None:
        """Adicionar update de participante."""
        self.updates.append(update)

    def get_participant_count(self) -> int:
        """Contar participantes únicos."""
        return len(set(u.participant for u in self.updates))

    def get_blockers(self) -> List[str]:
        """Listar todos os bloqueadores relatados."""
        return [u.blockers for u in self.updates if u.blockers]

    def to_dict(self) -> dict:
        """Serializar daily standup."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "num_participants": self.get_participant_count(),
            "num_blockers": len(self.get_blockers()),
            "num_action_items": len(self.action_items),
            "blockers": self.get_blockers(),
            "action_items": self.action_items,
        }


@dataclass
class SprintPlanningSession:
    """Estrutura completa de sprint planning com OKRs, stories, riscos e metricas."""

    sprint_id: str
    date: str  # ISO format
    duration_minutes: int = 120
    attendees: List[str] = field(default_factory=list)
    sprint_goal: str = ""  # Frase unica definindo o objetivo do sprint

    # OKR Alignment
    okrs_contemplated: List[str] = field(default_factory=list)  # Quais OKRs este sprint atende
    okr_alignment_notes: str = ""  # Como este sprint contribui para cada OKR

    # User Stories
    user_stories: List[dict] = field(default_factory=list)  # {id, titulo, descricao, criterios_aceitacao, prioridade}

    # Tasks
    goals: List[str] = field(default_factory=list)
    planned_tasks: List[dict] = field(default_factory=list)  # {id, title, estimate, story_id}
    velocity_target: float = 0.0

    # Dependencies & Risks
    dependencies_identified: List[dict] = field(default_factory=list)  # {de_task, para_task, descricao}
    risks_identified: List[dict] = field(default_factory=list)  # {descricao, probabilidade, impacto, mitigacao}

    # Stakeholders
    stakeholder_interviews: List[dict] = field(default_factory=list)  # {persona, data, feedback, acoes}

    # Metrics
    sprint_metrics: List[dict] = field(default_factory=list)  # {nome, alvo, descricao}

    # Retro Actions Review
    retro_actions_carried_over: List[dict] = field(default_factory=list)  # {acao_da_retro, status, dono}

    notes: str = ""

    def add_attendee(self, name: str) -> None:
        """Adicionar participante."""
        if name not in self.attendees:
            self.attendees.append(name)

    def add_goal(self, goal: str) -> None:
        """Adicionar objetivo do sprint."""
        self.goals.append(goal)

    def add_planned_task(self, task_id: str, title: str, estimate: float) -> None:
        """Adicionar tarefa ao plano."""
        self.planned_tasks.append({"id": task_id, "title": title, "estimate": estimate})

    def total_estimated_days(self) -> float:
        """Total de dias estimados."""
        return sum(t["estimate"] for t in self.planned_tasks)

    def to_dict(self) -> dict:
        """Serializar sprint planning."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "duration_minutes": self.duration_minutes,
            "num_attendees": len(self.attendees),
            "sprint_goal": self.sprint_goal,
            "num_okrs": len(self.okrs_contemplated),
            "num_stories": len(self.user_stories),
            "num_goals": len(self.goals),
            "num_planned_tasks": len(self.planned_tasks),
            "velocity_target": self.velocity_target,
            "total_estimated_days": self.total_estimated_days(),
            "num_dependencies": len(self.dependencies_identified),
            "num_risks": len(self.risks_identified),
            "num_stakeholders": len(self.stakeholder_interviews),
            "num_metrics": len(self.sprint_metrics),
            "num_retro_actions": len(self.retro_actions_carried_over),
        }

    def render_markdown(self) -> str:
        """Renderizar sprint planning completo como markdown."""
        lines = [f"# Sprint Planning — {self.sprint_id}", ""]
        lines += [f"**Data:** {self.date}", f"**Duracao:** {self.duration_minutes}min"]
        if self.attendees:
            lines += [f"**Participantes:** {', '.join(self.attendees)}", ""]

        # Sprint Goal
        lines += ["---", "", "## 🎯 Sprint Goal", ""]
        if self.sprint_goal:
            lines += [f"> {self.sprint_goal}", ""]
        else:
            lines += ["_[Definir goal do sprint]_", ""]

        # OKR Alignment
        lines += ["---", "", "## 🎯 Alinhamento com OKRs", ""]
        if self.okrs_contemplated:
            for okr in self.okrs_contemplated:
                lines += [f"- {okr}"]
        else:
            lines += ["_[Quais OKRs este sprint atende?]_", ""]
        if self.okr_alignment_notes:
            lines += ["", self.okr_alignment_notes, ""]

        # User Stories
        lines += ["---", "", "## 📖 User Stories", ""]
        if self.user_stories:
            for s in self.user_stories:
                lines += [f"### {s.get('id','US-?')}: {s.get('titulo','')}", ""]
                lines += [f"**Descricao:** {s.get('descricao','')}", ""]
                lines += [f"**Prioridade:** {s.get('prioridade','media')}", ""]
                lines += ["**Criterios de Aceitacao:**"]
                for ac in s.get('criterios_aceitacao', []):
                    lines += [f"- [ ] {ac}"]
                lines += [""]
        else:
            lines += ["_[Listar user stories do sprint]_", ""]

        # Tasks
        lines += ["---", "", "## 📋 Tasks Planejadas", ""]
        if self.planned_tasks:
            lines += ["| ID | Titulo | Estimativa | Story |", "|----|--------|-----------|-------|"]
            for t in self.planned_tasks:
                story = t.get('story_id', '-')
                lines += [f"| {t['id']} | {t['title']} | {t['estimate']}d | {story} |"]
            lines += [f"", f"**Total:** {self.total_estimated_days():.1f}d | **Velocity target:** {self.velocity_target}d", ""]
        else:
            lines += ["_[Listar tasks planejadas]_", ""]

        # Dependencies
        lines += ["---", "", "## 🔗 Mapa de Dependencias", ""]
        if self.dependencies_identified:
            for d in self.dependencies_identified:
                lines += [f"- `{d.get('de_task','?')}` → `{d.get('para_task','?')}`: {d.get('descricao','')}"]
        else:
            lines += ["_[Mapear dependencias entre tasks]_", ""]

        # Risks
        lines += ["", "---", "", "## 🚨 Riscos", ""]
        if self.risks_identified:
            lines += ["| Risco | Prob | Impacto | Mitigacao |", "|-------|------|---------|-----------|"]
            for r in self.risks_identified:
                lines += [f"| {r.get('descricao','')} | {r.get('probabilidade','?')} | {r.get('impacto','?')} | {r.get('mitigacao','')} |"]
        else:
            lines += ["_[Listar riscos com probabilidade, impacto e mitigacao]_", ""]

        # Stakeholder Interviews
        lines += ["", "---", "", "## 👥 Entrevistas com Stakeholders", ""]
        if self.stakeholder_interviews:
            for si in self.stakeholder_interviews:
                lines += [f"- **{si.get('persona','')}** ({si.get('data','')}): {si.get('feedback','')}"]
                if si.get('acoes'):
                    lines += [f"  - Acoes: {si['acoes']}"]
        else:
            lines += ["_[Entrevistar stakeholders para validar escopo]_", ""]

        # Sprint Metrics
        lines += ["", "---", "", "## 📊 Metricas da Sprint", ""]
        if self.sprint_metrics:
            lines += ["| Metrica | Alvo | Descricao |", "|---------|------|-----------|"]
            for m in self.sprint_metrics:
                lines += [f"| {m.get('nome','')} | {m.get('alvo','')} | {m.get('descricao','')} |"]
        else:
            lines += ["_[Definir metricas de sucesso do sprint]_", ""]

        # Retro Actions Review
        lines += ["", "---", "", "## 🔄 Acoes da Retro Anterior", ""]
        if self.retro_actions_carried_over:
            for a in self.retro_actions_carried_over:
                lines += [f"- {a.get('acao_da_retro','')} — Status: {a.get('status','pendente')} — Dono: {a.get('dono','')}"]
        else:
            lines += ["_[Revisar acoes pendentes da retro anterior]_", ""]

        lines += ["", "---", "", f"**Sprint Planning criado:** {self.date}", ""]
        return "\n".join(lines) + "\n"


@dataclass
class RoadmapPhase:
    """Uma fase do roadmap do produto (ex: Fundacao, Core Produto, Hub Bilateral)."""

    name: str
    period: str  # ex: "2026 Q2-Q3"
    goal: str = ""
    priority_items: List[dict] = field(default_factory=list)  # {priority, item, delivery}

    def add_item(self, priority: str, item: str, delivery: str) -> None:
        """Adicionar item priorizado a fase."""
        self.priority_items.append({"priority": priority, "item": item, "delivery": delivery})


@dataclass
class RoadmapCeremony:
    """Cerimonia de Roadmap Planning — estrutura oficial de roadmap do produto.

    Consolida North Star, fases priorizadas e matriz de dependencias em um
    unico documento de roadmap, no mesmo espirito de SprintPlanningSession
    mas em escala de produto (multiplas fases/releases) em vez de sprint.
    """

    product_id: str
    date: str  # ISO format
    facilitator: str = ""
    attendees: List[str] = field(default_factory=list)
    north_star: str = ""
    north_star_metric: str = ""
    phases: List[RoadmapPhase] = field(default_factory=list)
    dependency_matrix: List[dict] = field(default_factory=list)  # {item, depends_on}
    notes: str = ""

    def add_attendee(self, name: str) -> None:
        """Adicionar participante."""
        if name not in self.attendees:
            self.attendees.append(name)

    def add_phase(self, name: str, period: str, goal: str = "") -> RoadmapPhase:
        """Criar e adicionar uma fase ao roadmap, retornando-a para configuracao adicional."""
        phase = RoadmapPhase(name=name, period=period, goal=goal)
        self.phases.append(phase)
        return phase

    def add_dependency(self, item: str, depends_on: str) -> None:
        """Registrar dependencia entre itens do roadmap."""
        self.dependency_matrix.append({"item": item, "depends_on": depends_on})

    def total_items(self) -> int:
        """Total de itens priorizados em todas as fases."""
        return sum(len(p.priority_items) for p in self.phases)

    def to_dict(self) -> dict:
        """Serializar roadmap ceremony."""
        return {
            "product_id": self.product_id,
            "date": self.date,
            "num_attendees": len(self.attendees),
            "north_star": self.north_star,
            "north_star_metric": self.north_star_metric,
            "num_phases": len(self.phases),
            "total_items": self.total_items(),
            "num_dependencies": len(self.dependency_matrix),
        }

    def render_markdown(self) -> str:
        """Renderizar estrutura oficial de ROADMAP.md."""
        lines = [f"# Roadmap — {self.product_id}", ""]
        lines += [f"**Data:** {self.date}"]
        if self.facilitator:
            lines += [f"**Facilitador:** {self.facilitator}"]
        if self.attendees:
            lines += [f"**Participantes:** {', '.join(self.attendees)}"]
        lines += [""]

        # North Star
        lines += ["---", "", "## 🌟 North Star", ""]
        if self.north_star:
            lines += [f"> {self.north_star}", ""]
        else:
            lines += ["_[Definir North Star do produto]_", ""]
        if self.north_star_metric:
            lines += [f"**North Star Metric:** {self.north_star_metric}", ""]

        # Phases
        lines += ["---", "", "## 🗺️ Fases", ""]
        if self.phases:
            for phase in self.phases:
                lines += [f"### {phase.name} ({phase.period})", ""]
                if phase.goal:
                    lines += [f"**Goal:** {phase.goal}", ""]
                if phase.priority_items:
                    lines += ["| Prioridade | Item | Entrega |", "|---|---|---|"]
                    for it in phase.priority_items:
                        lines += [f"| {it['priority']} | {it['item']} | {it['delivery']} |"]
                    lines += [""]
                else:
                    lines += ["_[Priorizar itens desta fase]_", ""]
        else:
            lines += ["_[Definir fases do roadmap]_", ""]

        # Dependency Matrix
        lines += ["---", "", "## 🔗 Matriz de Dependências", ""]
        if self.dependency_matrix:
            for d in self.dependency_matrix:
                lines += [f"- `{d['item']}` depende de `{d['depends_on']}`"]
            lines += [""]
        else:
            lines += ["_[Mapear dependências entre itens do roadmap]_", ""]

        if self.notes:
            lines += ["---", "", "## 📝 Notas", "", self.notes, ""]

        lines += ["---", "", f"**Roadmap gerado:** {self.date}", ""]
        return "\n".join(lines) + "\n"


@dataclass
class RetroAction:
    """Uma ação de melhoria da retrospectiva."""

    category: str  # "what_went_well", "what_went_wrong", "improvements"
    description: str
    owner: Optional[str] = None
    priority: str = "medium"  # low, medium, high


@dataclass
class Retrospective:
    """Estrutura de sprint retrospective."""

    sprint_id: str
    date: str  # ISO format
    duration_minutes: int = 60
    attendees: List[str] = field(default_factory=list)
    what_went_well: List[str] = field(default_factory=list)
    what_went_wrong: List[str] = field(default_factory=list)
    improvement_ideas: List[str] = field(default_factory=list)
    action_items: List[RetroAction] = field(default_factory=list)
    velocity_achieved: float = 0.0
    completion_rate: float = 0.0
    overall_sentiment: str = "neutral"  # positive, neutral, negative
    notes: str = ""

    def add_attendee(self, name: str) -> None:
        """Adicionar participante."""
        if name not in self.attendees:
            self.attendees.append(name)

    def add_well(self, item: str) -> None:
        """Adicionar item positivo."""
        self.what_went_well.append(item)

    def add_wrong(self, item: str) -> None:
        """Adicionar item negativo."""
        self.what_went_wrong.append(item)

    def add_improvement(self, idea: str) -> None:
        """Adicionar ideia de melhoria."""
        self.improvement_ideas.append(idea)

    def add_action(self, action: RetroAction) -> None:
        """Adicionar ação de melhoria."""
        self.action_items.append(action)

    def get_high_priority_actions(self) -> List[RetroAction]:
        """Listar ações de alta prioridade."""
        return [a for a in self.action_items if a.priority == "high"]

    def to_dict(self) -> dict:
        """Serializar retrospective."""
        return {
            "sprint_id": self.sprint_id,
            "date": self.date,
            "duration_minutes": self.duration_minutes,
            "num_attendees": len(self.attendees),
            "num_positive_items": len(self.what_went_well),
            "num_negative_items": len(self.what_went_wrong),
            "num_improvement_ideas": len(self.improvement_ideas),
            "num_action_items": len(self.action_items),
            "num_high_priority_actions": len(self.get_high_priority_actions()),
            "velocity_achieved": self.velocity_achieved,
            "completion_rate": self.completion_rate,
            "overall_sentiment": self.overall_sentiment,
        }
