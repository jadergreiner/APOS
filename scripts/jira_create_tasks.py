#!/usr/bin/env python3
"""
APOS T0.3 — Task Import Script

Script que:
1. Lê tarefas de docs/releases/R0/sprint-0.3/TASKS.md
2. Cria issues no Jira via API REST

Credenciais via variáveis de ambiente:
    - JIRA_URL: https://jadergreiner.atlassian.net
    - JIRA_EMAIL: jadergreiner@gmail.com
    - JIRA_API_TOKEN: <seu api token>
"""

import os
import re
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime


class TaskParser:
    """Parse TASKS.md para extrair tasks em tabela markdown"""

    @staticmethod
    def read_markdown_table(file_path: str, table_name: str = "Tarefas") -> List[Dict]:
        """
        Lê tabela markdown do arquivo e retorna lista de dicts

        Formato esperado:
        | ID | Titulo | Descricao | Duracao | Personas | Status |
        |----|--------|-----------|---------|----------|--------|
        | T0.3.1 | ... | ... | 1.5d | Jader | ✅ 100% |
        """

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Encontra seção de "Tier 1: Core / Must-Have"
        lines = content.split('\n')

        tasks = []
        in_tier_table = False
        header_indices = {}

        for i, line in enumerate(lines):
            # Para quando atinge "Tier 2" ou outra seção
            if 'Tier 2' in line or 'Tier 3' in line or 'Progress Summary' in line or 'Timeline' in line:
                if in_tier_table:
                    break

            # Procura header da tabela
            if in_tier_table or ('| ID |' in line and 'Titulo' in line):
                if not in_tier_table:
                    in_tier_table = True
                    # Parse headers
                    headers = [h.strip() for h in line.split('|')[1:-1]]
                    header_indices = {h.lower(): idx for idx, h in enumerate(headers)}
                    continue

                # Pula separator
                if line.strip().startswith('|-'):
                    continue

                # Parse dados
                if '|' in line:
                    cells = [c.strip() for c in line.split('|')[1:-1]]

                    if len(cells) < 3:
                        continue

                    # Pula headers/vazios
                    if cells[0].startswith('ID') or not cells[0]:
                        continue

                    # Valida que é task (começa com T0.3.X)
                    if not cells[0].startswith('T0.'):
                        break  # Fim da tabela

                    # Mapeia dados
                    task = {}
                    for header, idx in header_indices.items():
                        if idx < len(cells):
                            task[header] = cells[idx]

                    if task.get('id'):
                        tasks.append(task)

        return tasks


class JiraTaskCreator:
    """Cria issues no Jira via API"""

    def __init__(self, url: str, email: str, api_token: str):
        self.url = url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def create_issue(self, project_key: str, task_dict: Dict) -> Optional[Dict]:
        """
        Cria uma issue no Jira

        Mapeia campos TASKS.md para Jira:
        - ID → summary (ex: T0.3.1)
        - Titulo → description
        - Descricao → description (append)
        - Duracao → customfield (labels ou campo próprio)
        - Status → status ou labels
        """

        task_id = task_dict.get('id', '').strip()
        titulo = task_dict.get('titulo', '').strip()
        descricao = task_dict.get('descricao', '').strip()
        duracao = task_dict.get('duracao', '').strip()
        personas = task_dict.get('personas', '').strip()
        status = task_dict.get('status', '').strip()

        # Construir sumário e descrição
        summary = f"{task_id}: {titulo}" if task_id else titulo

        desc_parts = []
        if descricao:
            desc_parts.append(descricao)
        if duracao:
            desc_parts.append(f"\n\nDuração estimada: {duracao}")
        if personas:
            desc_parts.append(f"Personas: {personas}")

        full_description = "\n".join(desc_parts) if desc_parts else summary

        # Parse status (remove emoji)
        clean_status = status.replace('✅', '').replace('📋', '').strip()

        # Payload da API v2 (mais compatível)
        payload = {
            "fields": {
                "project": {
                    "key": project_key
                },
                "summary": summary[:255],  # Jira limit
                "description": full_description,
                "issuetype": {
                    "name": "Task"  # Tipo padrão
                },
                "labels": [
                    f"sprint-0.3",
                    f"apos-{task_id}",
                    f"duration-{duracao}" if duracao else None,
                ],
            }
        }

        # Remove None labels
        payload["fields"]["labels"] = [l for l in payload["fields"]["labels"] if l]

        # Tenta API v2 (mais compatível)
        endpoint = f"{self.url}/rest/api/2/issue"

        try:
            response = self.session.post(endpoint, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "task_id": task_id,
                    "jira_key": result.get("key"),
                    "jira_id": result.get("id"),
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": f"HTTP {response.status_code}",
                    "response": response.text[:200],
                }

        except Exception as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": str(e),
            }

    def create_issues_from_tasks(self, project_key: str, tasks: List[Dict]) -> Dict:
        """
        Cria múltiplas issues e retorna relatório
        """

        results = {
            "total": len(tasks),
            "created": 0,
            "failed": 0,
            "issues": [],
        }

        for task in tasks:
            result = self.create_issue(project_key, task)
            results["issues"].append(result)

            if result["success"]:
                results["created"] += 1
                print(f"  ✓ {result['task_id']} → {result['jira_key']}")
            else:
                results["failed"] += 1
                print(f"  ✗ {result['task_id']} — {result.get('error')}")

        return results


def main():
    """Executa import de tasks"""

    print("=" * 70)
    print("APOS T0.3 — Task Import to Jira")
    print("=" * 70)
    print()

    # Carrega credenciais
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    if not jira_api_token:
        print("✗ JIRA_API_TOKEN não configurado")
        print("Configure: export JIRA_API_TOKEN='seu-token'")
        return

    # Lê TASKS.md
    tasks_file = "docs/releases/R0/sprint-0.3/TASKS.md"

    if not os.path.exists(tasks_file):
        print(f"✗ Arquivo não encontrado: {tasks_file}")
        return

    print(f"📖 Lendo {tasks_file}...\n")

    parser = TaskParser()
    tasks = parser.read_markdown_table(tasks_file)

    if not tasks:
        print("⚠️ Nenhuma task encontrada no arquivo")
        return

    print(f"📋 Encontradas {len(tasks)} tasks:\n")
    for task in tasks:
        task_id = task.get('id', 'N/A')
        titulo = task.get('titulo', 'N/A')[:40]
        print(f"   • {task_id}: {titulo}...")

    print(f"\n🔗 Conectando a {jira_url}...\n")

    # Cria issues
    creator = JiraTaskCreator(jira_url, jira_email, jira_api_token)
    results = creator.create_issues_from_tasks("SCRUM", tasks)

    # Relatório
    print()
    print("=" * 70)
    print("RESULTADO")
    print("=" * 70)
    print()
    print(f"Total tasks:  {results['total']}")
    print(f"Criadas:      {results['created']}")
    print(f"Falhadas:     {results['failed']}")
    print()

    # JSON export
    print("=" * 70)
    print("DETALHES (JSON)")
    print("=" * 70)
    print()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
