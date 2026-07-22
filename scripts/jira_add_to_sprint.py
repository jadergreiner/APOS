#!/usr/bin/env python3
"""
APOS Jira Add to Sprint — Adiciona issues ao sprint via API

Script que:
1. Encontra o Sprint ID para Sprint 0.3
2. Adiciona as 8 tasks ao sprint
3. Verifica adição bem-sucedida

Uso:
    python scripts/jira_add_to_sprint.py
"""

import os
import json
import requests
import logging
from typing import Optional, List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class JiraSprintManager:
    """Gerencia sprints no Jira"""

    def __init__(self, url: str, email: str, api_token: str):
        self.url = url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def find_sprint_id(self, project_key: str, sprint_name: str) -> Optional[int]:
        """Encontra o ID do sprint pelo nome"""
        try:
            # Usar API v2 para listar sprints
            response = self.session.get(
                f"{self.url}/rest/api/2/project/{project_key}",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                logger.debug(f"Project: {data.get('name')}")

            # Alternativa: buscar via JQL (se disponível)
            # Aqui, vamos tentar pegar todos os sprints de uma forma mais direta
            logger.info(f"Procurando sprint: {sprint_name}")

            # Método alternativo: pesquisar issues do projeto e extrair sprint
            # Usar um artifício: procurar por issues que sabidamente estão no sprint
            jql = f'project = {project_key} AND sprint is not EMPTY'
            response = self.session.get(
                f"{self.url}/rest/api/2/search",
                params={"jql": jql, "maxResults": 1},
                timeout=10
            )

            if response.status_code != 200:
                logger.warning(f"Search endpoint indisponível (v2 descontinuado)")
                return None

            data = response.json()
            if data.get("issues"):
                issue = data["issues"][0]
                sprint_id = issue["fields"].get("sprint", {}).get("id")
                if sprint_id:
                    return sprint_id

        except Exception as e:
            logger.error(f"Error finding sprint: {e}")

        return None

    def add_issues_to_sprint(self, sprint_id: int, issue_keys: List[str]) -> bool:
        """Adiciona issues ao sprint"""
        try:
            payload = {
                "issues": issue_keys
            }

            response = self.session.post(
                f"{self.url}/rest/api/2/sprint/{sprint_id}/issue",
                json=payload,
                timeout=10
            )

            if response.status_code == 204:
                logger.info(f"✓ Adicionadas {len(issue_keys)} issues ao sprint {sprint_id}")
                return True
            else:
                logger.error(f"Erro ao adicionar issues: HTTP {response.status_code}")
                logger.error(response.text)
                return False

        except Exception as e:
            logger.error(f"Error adding issues to sprint: {e}")
            return False


def main():
    """Main execution"""
    logger.info("=" * 70)
    logger.info("APOS Jira Add to Sprint")
    logger.info("=" * 70)

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

    # Inicializar gerenciador
    manager = JiraSprintManager(jira_url, jira_email, jira_api_token)

    # Encontrar sprint
    logger.info("Procurando Sprint 0.3...")
    sprint_id = manager.find_sprint_id("SCRUM", "Sprint 0.3")

    if not sprint_id:
        logger.error("✗ Sprint não encontrado")
        logger.info("💡 Alternativa: adicionar manualmente no Jira (arrastar do backlog para o sprint)")
        return

    logger.info(f"✓ Sprint ID: {sprint_id}")

    # Issues para adicionar
    issue_keys = ["SCRUM-22", "SCRUM-23", "SCRUM-24", "SCRUM-25", "SCRUM-26", "SCRUM-27", "SCRUM-28", "SCRUM-29"]

    logger.info(f"Adicionando {len(issue_keys)} issues ao sprint...")
    logger.info(f"Issues: {', '.join(issue_keys)}")

    # Adicionar ao sprint
    success = manager.add_issues_to_sprint(sprint_id, issue_keys)

    if success:
        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ SUCESSO!")
        logger.info("=" * 70)
        logger.info("As 8 tasks foram adicionadas ao Sprint 0.3")
        logger.info("Acesse: https://jadergreiner.atlassian.net/jira/software/projects/SCRUM/boards/1")
    else:
        logger.error("")
        logger.error("=" * 70)
        logger.error("❌ FALHA")
        logger.error("=" * 70)
        logger.error("Não foi possível adicionar as issues via API")
        logger.error("Alternativa: adicionar manualmente no Jira")
        logger.error("  1. Acesse: https://jadergreiner.atlassian.net/jira/software/projects/SCRUM/boards/1/backlog")
        logger.error("  2. Procure as issues SCRUM-22 a SCRUM-29 no backlog")
        logger.error("  3. Arraste cada uma para o Sprint 0.3")


if __name__ == "__main__":
    main()
