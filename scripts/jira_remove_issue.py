#!/usr/bin/env python3
"""
APOS Jira Remove Issue — Remove uma issue do Sprint
"""

import os
import sys
import requests

def get_jira_config():
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_token = os.getenv("JIRA_TOKEN")
    if not jira_token:
        raise ValueError("JIRA_TOKEN não configurado")
    return jira_url, jira_email, jira_token

def remove_issue_from_sprint(session, jira_url, issue_key, sprint_id=8):
    """Remove issue do sprint (move para backlog)"""
    url = f"{jira_url}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": [issue_key]}

    resp = session.delete(url, json=payload)

    if resp.status_code == 204:
        print(f"✅ {issue_key} removida do sprint")
        return True
    else:
        print(f"❌ Erro ao remover {issue_key}: {resp.status_code}")
        print(resp.text)
        return False

def main():
    if len(sys.argv) < 2:
        print("Uso: python jira_remove_issue.py <ISSUE_KEY> [<ISSUE_KEY2> ...]")
        print("Ex:  python jira_remove_issue.py SCRUM-52 SCRUM-53 SCRUM-54")
        sys.exit(1)

    issue_keys = sys.argv[1:]

    jira_url, jira_email, jira_token = get_jira_config()

    session = requests.Session()
    session.auth = (jira_email, jira_token)
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })

    print("=" * 70)
    print("APOS Jira Remove Issue")
    print("=" * 70)
    print()

    for key in issue_keys:
        remove_issue_from_sprint(session, jira_url, key)

    print()
    print("=" * 70)
    print(f"✅ {len(issue_keys)} issues removidas do sprint")
    print("=" * 70)

if __name__ == "__main__":
    main()
