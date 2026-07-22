#!/usr/bin/env python3
"""
APOS Jira Sprint Setup — Cria sprint R1.1.0 e adiciona tasks
"""

import os
import json
import requests
from datetime import datetime, timedelta

def get_jira_config():
    """Carrega configuração Jira do .env"""
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_token = os.getenv("JIRA_TOKEN")

    if not jira_token:
        raise ValueError("JIRA_TOKEN não configurado")

    return jira_url, jira_email, jira_token

def create_sprint(session, jira_url, project_key="SCRUM"):
    """Cria sprint R1.1.0 no projeto SCRUM"""

    # Busca ID do board do projeto
    url = f"{jira_url}/rest/agile/1.0/board?projectKeyOrId={project_key}"
    resp = session.get(url)
    if resp.status_code != 200:
        print(f"❌ Erro ao buscar board: {resp.status_code}")
        print(resp.text)
        return None

    boards = resp.json().get("values", [])
    if not boards:
        print(f"❌ Nenhum board encontrado para {project_key}")
        return None

    board_id = boards[0]["id"]
    print(f"✅ Board encontrado: {board_id}")

    # Cria sprint via /rest/agile/1.0/sprint (endpoint correto)
    url = f"{jira_url}/rest/agile/1.0/sprint"

    start_date = datetime.now().date()
    end_date = (datetime.now() + timedelta(days=5)).date()

    payload = {
        "name": "R1 Sprint 1.0",
        "startDate": start_date.isoformat(),
        "endDate": end_date.isoformat(),
        "boardId": board_id
    }

    resp = session.post(url, json=payload)

    if resp.status_code == 201:
        sprint_data = resp.json()
        sprint_id = sprint_data["id"]
        print(f"✅ Sprint criado: {sprint_data['name']} (ID: {sprint_id})")
        return sprint_id
    elif resp.status_code == 400:
        # Sprint pode já existir — tenta buscar via board
        print("⚠️  Sprint pode já existir, buscando...")
        url = f"{jira_url}/rest/agile/1.0/board/{board_id}/sprint"
        resp = session.get(url)
        sprints = resp.json().get("values", [])
        for sprint in sprints:
            if "R1 Sprint 1.0" in sprint["name"] or "R1" in sprint["name"]:
                print(f"✅ Sprint encontrado: {sprint['name']} (ID: {sprint['id']})")
                return sprint["id"]
        print(f"❌ Não conseguiu criar/encontrar sprint")
        return None
    else:
        print(f"❌ Erro ao criar sprint: {resp.status_code}")
        print(resp.text)
        return None

def add_issues_to_sprint(session, jira_url, sprint_id, issue_keys):
    """Adiciona issues ao sprint"""

    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}/issue"

    payload = {
        "issues": issue_keys
    }

    resp = session.post(url, json=payload)

    if resp.status_code == 204:
        print(f"✅ {len(issue_keys)} issues adicionadas ao sprint")
        return True
    else:
        print(f"❌ Erro ao adicionar issues: {resp.status_code}")
        print(resp.text)
        return False

def main():
    print("=" * 70)
    print("APOS Jira Sprint Setup")
    print("=" * 70)
    print()

    jira_url, jira_email, jira_token = get_jira_config()

    session = requests.Session()
    session.auth = (jira_email, jira_token)
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })

    print(f"🔗 Jira: {jira_url}")
    print(f"📧 Email: {jira_email}")
    print()

    # Cria sprint
    sprint_id = create_sprint(session, jira_url)
    if not sprint_id:
        print("❌ Falha ao criar/buscar sprint")
        return

    print()

    # Adiciona issues ao sprint
    issue_keys = ["SCRUM-55", "SCRUM-56", "SCRUM-57", "SCRUM-58"]
    success = add_issues_to_sprint(session, jira_url, sprint_id, issue_keys)

    print()
    if success:
        print("=" * 70)
        print("✅ SPRINT SETUP COMPLETO")
        print("=" * 70)
        print(f"Sprint ID: {sprint_id}")
        print(f"Issues: {', '.join(issue_keys)}")
    else:
        print("❌ Setup falhou")

if __name__ == "__main__":
    main()
