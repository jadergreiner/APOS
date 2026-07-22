#!/usr/bin/env python3
"""
APOS Jira Audit — Verifica consistência entre Jira e TASKS.md local
"""

import os
import json
import requests

def get_jira_config():
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_token = os.getenv("JIRA_TOKEN")
    if not jira_token:
        raise ValueError("JIRA_TOKEN não configurado")
    return jira_url, jira_email, jira_token

def list_sprint_issues(session, jira_url, sprint_id=8):
    """Lista todas as issues no sprint"""
    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    resp = session.get(url)
    if resp.status_code == 200:
        return resp.json().get("issues", [])
    else:
        print(f"❌ Erro ao buscar issues: {resp.status_code}")
        return []

def parse_tasks_md(file_path):
    """Extrai task IDs do TASKS.md"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tasks = []
    for line in content.split('\n'):
        if line.startswith('| T'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 1 and parts[1].startswith('T'):
                task_id = parts[1]
                tasks.append(task_id)

    return tasks

def main():
    print("=" * 70)
    print("APOS Jira Audit — Consistência")
    print("=" * 70)
    print()

    jira_url, jira_email, jira_token = get_jira_config()

    session = requests.Session()
    session.auth = (jira_email, jira_token)
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })

    # Busca issues no Sprint
    print("📊 Buscando issues no Sprint R1...")
    issues = list_sprint_issues(session, jira_url, sprint_id=8)
    jira_keys = {issue['key'] for issue in issues}
    jira_issues = {issue['key']: issue for issue in issues}
    print(f"✅ {len(jira_keys)} issues encontradas no Jira")
    print()

    # Busca tasks no TASKS.md
    print("📋 Lendo TASKS.md local...")
    local_tasks = parse_tasks_md("docs/releases/R1/sprint-1.0/TASKS.md")
    print(f"✅ {len(local_tasks)} tasks encontradas localmente")
    print()

    # Lê histórico de sync
    with open('.jira_sync_history.json', 'r') as f:
        sync_history = json.load(f)

    expected_keys = {sync_history.get(task) for task in local_tasks if task in sync_history}
    print(f"✅ {len(expected_keys)} issues esperadas (via sync_history)")
    print()

    # Comparação
    print("=" * 70)
    print("ANÁLISE")
    print("=" * 70)
    print()

    extras = jira_keys - expected_keys
    missing = expected_keys - jira_keys

    if extras:
        print(f"❌ EXTRAS no Jira (não esperadas):")
        for key in sorted(extras):
            issue = jira_issues.get(key)
            print(f"   • {key}: {issue['fields']['summary'] if issue else '?'}")
        print()

    if missing:
        print(f"❌ FALTANDO no Jira (esperadas mas não encontradas):")
        for key in sorted(missing):
            print(f"   • {key}")
        print()

    if not extras and not missing:
        print("✅ CONSISTÊNCIA PERFEITA")
        print(f"   Jira Sprint: {len(jira_keys)} issues")
        print(f"   TASKS.md: {len(local_tasks)} tasks")
        print(f"   Sync history: {len(expected_keys)} mapeadas")
        print()

    # Recomendação
    print("=" * 70)
    print("RECOMENDAÇÃO")
    print("=" * 70)
    print()

    if extras:
        print(f"AÇÃO: Remover {len(extras)} extras do Sprint R1 no Jira:")
        for key in sorted(extras):
            print(f"  python scripts/jira_remove_issue.py {key}")
        print()

    if missing:
        print(f"AÇÃO: Re-sincronizar — há {len(local_tasks)} tasks em TASKS.md")
        print("  python scripts/jira_sync_tasks.py --force")
        print()

if __name__ == "__main__":
    main()
