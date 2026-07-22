#!/usr/bin/env python3
"""
APOS Jira Add Sprint (Agile API) — Move issues to sprint

Script que usa a Agile API v1.0 para mover issues para o sprint
"""

import os
import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    # Load config
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    if not jira_api_token:
        try:
            with open('.env', 'r') as f:
                for line in f:
                    if 'JIRA_TOKEN' in line:
                        jira_api_token = line.split('=', 1)[1].strip()
                        break
        except:
            pass

    if not jira_api_token:
        logger.error("✗ JIRA_API_TOKEN não configurado")
        return

    logger.info("=" * 70)
    logger.info("APOS Jira Add Sprint (Agile API)")
    logger.info("=" * 70)

    # Create session
    session = requests.Session()
    session.auth = (jira_email, jira_api_token)
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json"
    })

    # Sprint ID (descoberto anteriormente)
    sprint_id = 2
    issue_keys = ["SCRUM-22", "SCRUM-23", "SCRUM-24", "SCRUM-25", "SCRUM-26", "SCRUM-27", "SCRUM-28", "SCRUM-29"]

    logger.info(f"Sprint ID: {sprint_id}")
    logger.info(f"Issues: {', '.join(issue_keys)}")
    logger.info("")

    # Endpoint: POST /rest/agile/1.0/sprint/{sprintId}/issue
    endpoint = f"{jira_url.rstrip('/')}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {
        "issues": issue_keys
    }

    logger.info(f"Endpoint: {endpoint}")
    logger.info(f"Payload: {payload}")
    logger.info("")

    try:
        logger.info("Enviando request...")
        response = session.post(endpoint, json=payload, timeout=10)

        logger.info(f"Status: {response.status_code}")

        if response.status_code == 204:
            logger.info("")
            logger.info("=" * 70)
            logger.info("✅ SUCESSO!")
            logger.info("=" * 70)
            logger.info("Todas as 8 issues foram adicionadas ao Sprint 0.3")
            logger.info("")
            logger.info("Acesse o board:")
            logger.info("https://jadergreiner.atlassian.net/jira/software/projects/SCRUM/boards/1")
        else:
            logger.error(f"Erro: HTTP {response.status_code}")
            logger.error(response.text)

    except Exception as e:
        logger.error(f"Exception: {e}")


if __name__ == "__main__":
    main()
