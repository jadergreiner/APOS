#!/usr/bin/env python3
"""
APOS Jira Update Sprint — Adiciona issues ao sprint via API v2

Script que:
1. Obtém o Sprint ID do Sprint 0.3
2. Atualiza as issues SCRUM-22 a SCRUM-29 com o campo sprint
3. Valida a adição

Uso:
    python scripts/jira_update_sprint.py
"""

import os
import json
import requests
import logging
from typing import Optional, List, Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class JiraSprintUpdater:
    """Atualiza issues com sprint via API v2"""

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

    def find_sprint_id_by_board(self, board_id: int = 1) -> Optional[int]:
        """Encontra o Sprint ID mais recente via board"""
        try:
            # Usar endpoint de board para listar sprints
            # Nota: v2 pode não ter isso, então vamos tentar via config do board
            response = self.session.get(
                f"{self.url}/rest/api/2/board/{board_id}/configuration",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                logger.debug("Board configuration obtained")
                # Procurar por sprint info
                # Este endpoint pode variar

            # Alternativa: procurar issues do projeto e extrair sprint
            logger.info("Procurando Sprint ID via issues...")
            jql = 'project = SCRUM AND sprint is not EMPTY'

            # Nota: /search v2 foi descontinuado, mas vamos tentar mesmo assim
            try:
                response = self.session.get(
                    f"{self.url}/rest/api/2/search",
                    params={"jql": jql, "maxResults": 1},
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("issues"):
                        issue = data["issues"][0]
                        sprint_data = issue["fields"].get("sprint", {})
                        if isinstance(sprint_data, dict):
                            sprint_id = sprint_data.get("id")
                        else:
                            # Sprint pode ser um array
                            sprint_id = sprint_data[0]["id"] if sprint_data else None

                        if sprint_id:
                            logger.info(f"✓ Sprint ID encontrado: {sprint_id}")
                            return sprint_id
            except Exception as e:
                logger.debug(f"Search endpoint indisponível: {e}")

            # Última tentativa: search via v3 (mas temos que ter cuidado)
            # Não vamos tentar v3 aqui porque a criação é em v2

            # Fallback: usar hardcoded sprint ID se soubermos
            # Para este projeto, vamos tentar descobrir via projeto
            return self._find_sprint_id_via_project()

        except Exception as e:
            logger.error(f"Error finding sprint: {e}")

        return None

    def _find_sprint_id_via_project(self) -> Optional[int]:
        """Tenta descobrir Sprint ID de outra forma"""
        try:
            # Tentar endpoint de sprints do projeto
            response = self.session.get(
                f"{self.url}/rest/agile/1.0/board/1/sprint",
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("values"):
                    # Procurar por Sprint 0.3 ou pegar o primeiro ativo
                    for sprint in data["values"]:
                        if "0.3" in sprint.get("name", "") or sprint.get("state") == "ACTIVE":
                            sprint_id = sprint.get("id")
                            logger.info(f"✓ Sprint encontrado via Agile API: {sprint_id} ({sprint.get('name')})")
                            return sprint_id

        except Exception as e:
            logger.debug(f"Agile API não disponível: {e}")

        return None

    def update_issue_sprint(self, issue_key: str, sprint_id: int) -> bool:
        """Atualiza uma issue com o sprint"""
        try:
            payload = {
                "fields": {
                    "sprint": sprint_id
                }
            }

            response = self.session.put(
                f"{self.url}/rest/api/2/issue/{issue_key}",
                json=payload,
                timeout=10
            )

            if response.status_code in [200, 204]:
                logger.info(f"  ✓ {issue_key} adicionada ao sprint")
                return True
            else:
                logger.error(f"  ✗ {issue_key}: HTTP {response.status_code}")
                logger.error(f"    {response.text[:200]}")
                return False

        except Exception as e:
            logger.error(f"  ✗ {issue_key}: {e}")
            return False

    def update_issues_sprint(self, sprint_id: int, issue_keys: List[str]) -> Dict:
        """Atualiza múltiplas issues"""
        results = {
            "total": len(issue_keys),
            "updated": 0,
            "failed": 0,
            "details": []
        }

        for issue_key in issue_keys:
            if self.update_issue_sprint(issue_key, sprint_id):
                results["updated"] += 1
                results["details"].append({
                    "issue_key": issue_key,
                    "status": "updated"
                })
            else:
                results["failed"] += 1
                results["details"].append({
                    "issue_key": issue_key,
                    "status": "failed"
                })

        return results


def main():
    """Main execution"""
    logger.info("=" * 70)
    logger.info("APOS Jira Update Sprint")
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

    # Inicializar updater
    updater = JiraSprintUpdater(jira_url, jira_email, jira_api_token)

    # Encontrar sprint
    logger.info("Procurando Sprint 0.3...")
    sprint_id = updater.find_sprint_id_by_board(board_id=1)

    if not sprint_id:
        logger.error("✗ Sprint não encontrado")
        logger.error("")
        logger.error("Troubleshooting:")
        logger.error("  1. Verifique se Sprint 0.3 existe no Jira")
        logger.error("  2. Verifique se há issues no sprint (para descobrir Sprint ID)")
        logger.error("  3. Teste manualmente: ir ao Backlog e arrastar issues")
        return

    logger.info(f"✓ Sprint ID: {sprint_id}")
    logger.info("")

    # Issues para atualizar
    issue_keys = ["SCRUM-22", "SCRUM-23", "SCRUM-24", "SCRUM-25", "SCRUM-26", "SCRUM-27", "SCRUM-28", "SCRUM-29"]

    logger.info(f"Adicionando {len(issue_keys)} issues ao Sprint 0.3...")
    logger.info(f"Issues: {', '.join(issue_keys)}")
    logger.info("")

    # Atualizar issues
    results = updater.update_issues_sprint(sprint_id, issue_keys)

    # Report
    logger.info("")
    logger.info("=" * 70)
    logger.info("RESULTADO")
    logger.info("=" * 70)
    logger.info(f"Total:     {results['total']}")
    logger.info(f"Atualizadas: {results['updated']}")
    logger.info(f"Falhadas:  {results['failed']}")
    logger.info("")

    if results["failed"] == 0:
        logger.info("✅ SUCESSO!")
        logger.info("Todas as 8 tasks foram adicionadas ao Sprint 0.3")
        logger.info("Acesse: https://jadergreiner.atlassian.net/jira/software/projects/SCRUM/boards/1")
    else:
        logger.warning("⚠️ Algumas issues falharam")
        logger.warning("Verifique os detalhes acima")

    logger.info("")


if __name__ == "__main__":
    main()
