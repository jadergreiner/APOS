#!/usr/bin/env python3
"""
APOS Jira Task Sync — Sincronização automática de TASKS.md → Jira

Script que:
1. Lê TASKS.md do repositório
2. Sincroniza com Jira via API (idempotente)
3. Cria/atualiza issues conforme necessário
4. Mantém histórico de sincronização

Uso:
    python scripts/jira_sync_tasks.py [--dry-run] [--force]

Flags:
    --dry-run: Mostra o que seria feito, sem fazer
    --force: Recria issues mesmo que já existam
"""

import os
import json
import re
import requests
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict, field

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Representa uma task do TASKS.md"""
    task_id: str
    titulo: str
    descricao: str
    duracao: str
    personas: str
    status: str
    tier: str  # "Tier 1", "Tier 2", etc

    def to_jira_payload(self, project_key: str, issue_type: str = "Tarefa") -> Dict:
        """Converte para payload Jira API v2"""
        summary = f"{self.task_id}: {self.titulo}"

        desc_parts = [self.descricao]
        if self.duracao:
            desc_parts.append(f"\n**Duração:** {self.duracao}")
        if self.personas:
            desc_parts.append(f"**Personas:** {self.personas}")
        if self.tier:
            desc_parts.append(f"**Tier:** {self.tier}")

        description = "\n".join(desc_parts)

        return {
            "fields": {
                "project": {"key": project_key},
                "summary": summary[:255],
                "description": description,
                "issuetype": {"name": issue_type},
                "labels": [
                    "sprint-0.3",
                    f"apos-{self.task_id}",
                    f"duration-{self.duracao}" if self.duracao else None,
                    self.tier.lower().replace(" ", "-") if self.tier else None,
                ],
            }
        }

    @property
    def jira_key_pattern(self) -> str:
        """Padrão para encontrar JIRA key desta task"""
        return self.task_id


class TasksParser:
    """Parse TASKS.md → Lista de tasks"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.tasks: List[Task] = []

    def parse(self) -> List[Task]:
        """Parseia TASKS.md e retorna lista de tasks"""
        logger.info(f"Parsing {self.file_path}...")

        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        tasks = []
        current_tier = None

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Detecta seção de tier
            if 'Tier 1:' in line or 'Tier 2:' in line or 'Tier 3:' in line:
                current_tier = line.strip()

            # Procura por tabela de tarefas
            if '| ID |' in line and 'Titulo' in line:
                i += 1  # Pula header
                i += 1  # Pula separator

                # Parse linhas da tabela
                while i < len(lines):
                    row = lines[i]
                    if not row.strip().startswith('|'):
                        break

                    # Parse células
                    cells = [c.strip() for c in row.split('|')[1:-1]]
                    if len(cells) >= 5:
                        task_id = cells[0]
                        if task_id and task_id.startswith('T0.'):
                            task = Task(
                                task_id=task_id,
                                titulo=cells[1],
                                descricao=cells[2],
                                duracao=cells[3],
                                personas=cells[4],
                                status=cells[5] if len(cells) > 5 else "",
                                tier=current_tier or "Unknown"
                            )
                            tasks.append(task)
                            logger.info(f"  ✓ {task.task_id}: {task.titulo[:40]}")

                    i += 1

            i += 1

        self.tasks = tasks
        logger.info(f"Total tasks: {len(tasks)}")
        return tasks


class JiraSync:
    """Sincroniza tasks com Jira"""

    SYNC_HISTORY_FILE = ".jira_sync_history.json"

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
        self.sync_history = self._load_sync_history()

    def _load_sync_history(self) -> Dict:
        """Carrega histórico de sincronizações"""
        if os.path.exists(self.SYNC_HISTORY_FILE):
            try:
                with open(self.SYNC_HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_sync_history(self):
        """Salva histórico de sincronizações"""
        with open(self.SYNC_HISTORY_FILE, 'w') as f:
            json.dump(self.sync_history, f, indent=2)

    def _get_cached_issue(self, task_id: str) -> Optional[str]:
        """Retorna issue key do cache se existir"""
        return self.sync_history.get(task_id)

    def search_issue(self, project_key: str, task_id: str) -> Optional[str]:
        """Procura por issue existente com este task_id"""
        try:
            jql = f'project = {project_key} AND summary ~ "{task_id}"'
            response = self.session.get(
                f"{self.url}/rest/api/3/issues/search",
                params={"jql": jql},
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("issues"):
                    return data["issues"][0]["key"]
            else:
                logger.debug(f"Search returned {response.status_code} for {task_id}")
        except Exception as e:
            logger.debug(f"Error searching for {task_id}: {e}")

        return None

    def create_issue(self, project_key: str, task: Task, issue_type: str = "Tarefa") -> Tuple[bool, str]:
        """Cria nova issue no Jira"""
        endpoint = f"{self.url}/rest/api/2/issue"
        payload = task.to_jira_payload(project_key, issue_type=issue_type)

        # Remove None labels
        payload["fields"]["labels"] = [l for l in payload["fields"]["labels"] if l]

        try:
            response = self.session.post(endpoint, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                result = response.json()
                return True, result.get("key")
            else:
                error = response.text[:200]
                return False, f"HTTP {response.status_code}: {error}"

        except Exception as e:
            return False, str(e)

    def sync_tasks(
        self,
        project_key: str,
        tasks: List[Task],
        dry_run: bool = False,
        force: bool = False,
        issue_type: str = "Tarefa"
    ) -> Dict:
        """Sincroniza tasks com Jira"""
        results = {
            "total": len(tasks),
            "created": 0,
            "updated": 0,
            "failed": 0,
            "skipped": 0,
            "details": []
        }

        for task in tasks:
            logger.info(f"\nProcessing {task.task_id}...")

            # Procura por issue no cache local
            cached_key = self._get_cached_issue(task.task_id)

            if cached_key and not force:
                logger.info(f"  ✓ SKIPPED: {cached_key} já existe")
                results["skipped"] += 1
                results["details"].append({
                    "task_id": task.task_id,
                    "status": "skipped",
                    "jira_key": cached_key
                })
                continue

            if dry_run:
                logger.info(f"  [DRY-RUN] Would create: {task.task_id}")
                results["details"].append({
                    "task_id": task.task_id,
                    "status": "dry_run"
                })
                continue

            # Cria nova issue
            success, result = self.create_issue(project_key, task, issue_type=issue_type)

            if success:
                logger.info(f"  ✓ CREATED: {result}")
                results["created"] += 1
                # Salva no cache
                self.sync_history[task.task_id] = result
                self._save_sync_history()
                results["details"].append({
                    "task_id": task.task_id,
                    "status": "created",
                    "jira_key": result
                })
            else:
                logger.error(f"  ✗ FAILED: {result}")
                results["failed"] += 1
                results["details"].append({
                    "task_id": task.task_id,
                    "status": "failed",
                    "error": result
                })

        return results


def main():
    """Main execution"""
    import sys

    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv

    logger.info("=" * 70)
    logger.info("APOS Jira Task Sync")
    logger.info("=" * 70)

    if dry_run:
        logger.info("🔍 DRY-RUN MODE (no changes will be made)")
    if force:
        logger.info("⚠️  FORCE MODE (will recreate existing issues)")

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

    logger.info(f"🔗 Jira: {jira_url}")
    logger.info(f"📧 Email: {jira_email}")
    logger.info("")

    # Parse tasks
    parser = TasksParser("docs/releases/R0/sprint-0.3/TASKS.md")
    tasks = parser.parse()
    logger.info("")

    # Sync com Jira
    sync = JiraSync(jira_url, jira_email, jira_api_token)
    results = sync.sync_tasks("SCRUM", tasks, dry_run=dry_run, force=force)

    # Report
    logger.info("")
    logger.info("=" * 70)
    logger.info("RESULTADO DA SINCRONIZAÇÃO")
    logger.info("=" * 70)
    logger.info(f"Total:     {results['total']}")
    logger.info(f"Criadas:   {results['created']}")
    logger.info(f"Puladas:   {results['skipped']}")
    logger.info(f"Falhadas:  {results['failed']}")
    logger.info("")

    if results["failed"] > 0:
        logger.warning("⚠️ Algumas issues falharam:")
        for detail in results["details"]:
            if detail["status"] == "failed":
                logger.warning(f"  • {detail['task_id']}: {detail['error']}")

    logger.info("")
    logger.info("JSON OUTPUT:")
    logger.info(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
