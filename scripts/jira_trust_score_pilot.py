#!/usr/bin/env python3
"""
APOS T0.3.5 Pilot: Real Jira Data + Trust Score Calculation

Script que:
1. Conecta ao Jira Cloud API
2. Extrai todas as tasks do projeto SCRUM
3. Calcula Trust Score com dados reais
4. Mostra relatório de análise

Uso:
    python scripts/jira_trust_score_pilot.py

Credenciais:
    Passa via variáveis de ambiente:
    - JIRA_URL: https://jadergreiner.atlassian.net
    - JIRA_EMAIL: jadergreiner@gmail.com
    - JIRA_API_TOKEN: <seu api token>
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional
from apos.trust_score import (
    TrustScoreEngine,
    Task,
    OKR,
    Relationship,
)


class JiraDataExtractor:
    """Extrai dados do Jira via API REST"""

    def __init__(self, url: str, email: str, api_token: str):
        self.url = url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json"})

    def get_issues(self, project_key: str) -> List[Dict]:
        """Extrai todas as issues de um projeto via JQL"""
        jql = f'project = "{project_key}"'
        endpoint = f"{self.url}/rest/api/3/search"

        print(f"🔍 Buscando issues do projeto {project_key}...")

        issues = []
        start_at = 0
        max_results = 50

        while True:
            params = {
                "jql": jql,
                "startAt": start_at,
                "maxResults": max_results,
                "expand": "changelog",
                "fields": [
                    "key",
                    "summary",
                    "status",
                    "created",
                    "updated",
                    "issuetype",
                    "customfield_10000",  # OKR field (pode variar)
                    "customfield_10001",  # Alternativo
                    "customfield_10002",  # Alternativo
                    "labels",  # Procura por label "OKR-*"
                ],
            }

            try:
                response = self.session.get(endpoint, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if "issues" not in data or not data["issues"]:
                    break

                issues.extend(data["issues"])
                start_at += max_results

                if data.get("isLast", True):
                    break

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Erro ao buscar issues: {e}")
                break

        print(f"✅ Encontradas {len(issues)} issues")
        return issues

    def parse_issues_to_tasks(self, issues: List[Dict]) -> tuple:
        """Converte issues do Jira em objetos Task + Relationship"""
        tasks = []
        relationships = []
        okrs_found = set()

        for issue in issues:
            fields = issue.get("fields", {})
            key = issue.get("key", "UNKNOWN")
            summary = fields.get("summary", "Sem título")
            status = fields.get("status", {}).get("name", "unknown").lower()
            created = fields.get("created")
            updated = fields.get("updated")

            # Procura por OKR em diferentes campos customizados
            okr_id = None

            # Tenta campo customizado padrão
            for custom_field in [
                "customfield_10000",
                "customfield_10001",
                "customfield_10002",
            ]:
                if fields.get(custom_field):
                    okr_id = str(fields.get(custom_field))
                    break

            # Tenta em labels (ex: "OKR-2026-Q3-001")
            if not okr_id:
                labels = fields.get("labels", [])
                for label in labels:
                    if label.startswith("OKR-"):
                        okr_id = label
                        break

            # Parse dates
            created_dt = None
            updated_dt = None
            if created:
                try:
                    created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                except:
                    pass
            if updated:
                try:
                    updated_dt = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                except:
                    pass

            # Cria Task
            task = Task(
                id=key,
                title=summary,
                status=status,
                project_id="SCRUM",
                okr_id=okr_id,
                created_at=created_dt,
                updated_at=updated_dt,
            )
            tasks.append(task)

            # Se tem OKR, registra relationship
            if okr_id:
                okrs_found.add(okr_id)
                rel = Relationship(
                    task_id=key,
                    okr_id=okr_id,
                    confidence=1.0,  # Manual assignment
                    created_at=created_dt,
                    updated_at=updated_dt,
                )
                relationships.append(rel)

        # Cria OKRs dummy (não temos dados reais de OKRs no Jira)
        okrs = [OKR(id=okr_id, name=f"OKR: {okr_id}", project_id="SCRUM") for okr_id in okrs_found]

        print(f"📊 Parsed: {len(tasks)} tasks, {len(okrs)} OKRs, {len(relationships)} relationships")
        return tasks, okrs, relationships


def main():
    """Executa piloto com dados reais do Jira"""

    # Carrega credenciais
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    if not jira_api_token:
        print("⚠️ JIRA_API_TOKEN não configurado")
        print("Para usar este script, configure:")
        print('  export JIRA_URL="https://seu-jira.atlassian.net"')
        print('  export JIRA_EMAIL="seu@email.com"')
        print('  export JIRA_API_TOKEN="seu-api-token"')
        print()
        print("Usando dados MOCK para demonstração...")
        demo_pilot()
        return

    # Extrai dados do Jira
    print(f"🔗 Conectando a {jira_url}...\n")

    extractor = JiraDataExtractor(jira_url, jira_email, jira_api_token)

    try:
        issues = extractor.get_issues("SCRUM")
        tasks, okrs, relationships = extractor.parse_issues_to_tasks(issues)
    except Exception as e:
        print(f"❌ Erro ao conectar ao Jira: {e}")
        print("Usando dados MOCK para demonstração...\n")
        demo_pilot()
        return

    # Calcula Trust Score
    print("\n" + "=" * 60)
    print("🧮 CALCULANDO TRUST SCORE")
    print("=" * 60 + "\n")

    engine = TrustScoreEngine(tasks, okrs, relationships)
    result = engine.calculate()

    # Exibe resultados
    print(f"📊 TRUST SCORE: {result.score:.1%}")
    print()

    print("📈 COMPONENTES:")
    print(f"  • Coverage:    {result.components['coverage'].value:.1%}  (30% weight)")
    print(f"  • Quality:     {result.components['quality'].value:.1%}  (50% weight)")
    print(f"  • Consistency: {result.components['consistency'].value:.1%}  (20% weight)")
    print()

    print(f"🎯 ESTATÍSTICAS:")
    print(f"  • Total tasks:   {result.total_tasks}")
    print(f"  • Orphaned:      {result.orphan_count} ({result.orphan_count/result.total_tasks*100 if result.total_tasks else 0:.0f}%)")
    print(f"  • Linked:        {result.total_tasks - result.orphan_count}")
    print()

    if result.issues:
        print("⚠️ ISSUES DETECTADAS:")
        for issue in result.issues:
            print(f"  {issue}")
        print()

    print(f"💡 RECOMENDAÇÃO:")
    print(f"  {result.recommendation}")
    print()

    print("📋 DETALHES DOS COMPONENTES:")
    print()

    # Coverage details
    cov_details = result.components["coverage"].details
    print(f"Coverage ({cov_details['linked_tasks']}/{cov_details['total_tasks']}):")
    print(f"  {cov_details['percentage']}% das tasks vinculadas a OKRs")
    print()

    # Quality details
    qual_details = result.components["quality"].details
    print(f"Quality ({qual_details['valid_relationships']}/{qual_details['total_relationships']}):")
    print(f"  {qual_details['validity_percentage']}% relacionamentos válidos")
    print(f"  Freshness: {qual_details['freshness_score']:.2f}")
    if qual_details["invalid_relationships"]:
        print("  Inválidas:")
        for rel in qual_details["invalid_relationships"]:
            print(f"    - {rel}")
    print()

    # Consistency details
    cons_details = result.components["consistency"].details
    print(f"Consistency:")
    print(f"  {cons_details['conflicts']} conflitos detectados")
    print(f"  {cons_details['conflict_percentage']}% taxa de conflito")
    if cons_details["conflicting_tasks"]:
        print("  Tasks com conflito:")
        for task in cons_details["conflicting_tasks"]:
            print(f"    - {task}")
    print()

    # JSON output
    print("=" * 60)
    print("📄 JSON OUTPUT:")
    print("=" * 60)
    print(engine.to_json())


def demo_pilot():
    """Piloto com dados MOCK para demonstração"""
    print("=" * 60)
    print("🧪 DEMO PILOTO (Dados Mock)")
    print("=" * 60 + "\n")

    # Dados mock baseados no board real
    tasks = [
        Task(
            id="SCRUM-1",
            title="T0.3.1 - Especificacao Tecnica (SPEC.md)",
            status="a_fazer",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-001",
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 23),
        ),
        Task(
            id="SCRUM-2",
            title="Tarefa 2 - User Story",
            status="em_andamento",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-001",
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 23),
        ),
        Task(
            id="SCRUM-3",
            title="Implementation Task",
            status="backlog",
            project_id="SCRUM",
            okr_id=None,  # ORPHAN!
            created_at=datetime(2026, 7, 22),
            updated_at=datetime(2026, 7, 22),
        ),
        Task(
            id="SCRUM-4",
            title="Bug Fix - Critical",
            status="em_andamento",
            project_id="SCRUM",
            okr_id="OKR-2026-Q3-002",
            created_at=datetime(2026, 7, 21),
            updated_at=datetime(2026, 7, 22),
        ),
        Task(
            id="SCRUM-5",
            title="Deploy em sandbox + onboarding",
            status="a_fazer",
            project_id="SCRUM",
            okr_id=None,  # ORPHAN!
            created_at=datetime(2026, 7, 23),
            updated_at=datetime(2026, 7, 23),
        ),
    ]

    okrs = [
        OKR(id="OKR-2026-Q3-001", name="Validar MVP com pilotos", project_id="SCRUM"),
        OKR(id="OKR-2026-Q3-002", name="Melhorar performance", project_id="SCRUM"),
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

    print(f"📊 Dados MOCK: {len(tasks)} tasks, {len(okrs)} OKRs, {len(relationships)} relationships\n")

    # Calcula Trust Score
    engine = TrustScoreEngine(tasks, okrs, relationships)
    result = engine.calculate()

    # Exibe resultados (mesmo formato que acima)
    print(f"📊 TRUST SCORE: {result.score:.1%}")
    print()

    print("📈 COMPONENTES:")
    print(f"  • Coverage:    {result.components['coverage'].value:.1%}  (30% weight)")
    print(f"  • Quality:     {result.components['quality'].value:.1%}  (50% weight)")
    print(f"  • Consistency: {result.components['consistency'].value:.1%}  (20% weight)")
    print()

    print(f"🎯 ESTATÍSTICAS:")
    print(f"  • Total tasks:   {result.total_tasks}")
    print(f"  • Orphaned:      {result.orphan_count} ({result.orphan_count/result.total_tasks*100:.0f}%)")
    print(f"  • Linked:        {result.total_tasks - result.orphan_count}")
    print()

    print("⚠️ ISSUES DETECTADAS:")
    for issue in result.issues:
        print(f"  {issue}")
    print()

    print(f"💡 RECOMENDAÇÃO:")
    print(f"  {result.recommendation}")
    print()

    print("=" * 60)
    print("📄 JSON OUTPUT:")
    print("=" * 60)
    print(engine.to_json())


if __name__ == "__main__":
    main()
