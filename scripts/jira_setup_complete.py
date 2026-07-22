#!/usr/bin/env python3
"""
APOS T0.3 — Complete Jira Setup Automation

Script que:
1. Cria projeto SCRUM via API Jira
2. Aguarda inicialização
3. Importa 4 tasks automaticamente

Execução única: ~2-3 minutos
"""

import os
import time
import json
import requests
from datetime import datetime
from typing import Dict, Optional


class JiraProjectManager:
    """Gerencia criação de projetos no Jira via API"""

    def __init__(self, url: str, email: str, api_token: str):
        self.url = url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def project_exists(self, project_key: str) -> bool:
        """Verifica se projeto já existe"""
        try:
            endpoint = f"{self.url}/rest/api/2/project/{project_key}"
            response = self.session.get(endpoint, timeout=5)
            return response.status_code == 200
        except:
            return False

    def create_project(self, project_key: str, project_name: str) -> Optional[Dict]:
        """
        Cria novo projeto no Jira

        API v2 endpoint para criar projeto
        """
        endpoint = f"{self.url}/rest/api/2/project"

        payload = {
            "key": project_key,
            "name": project_name,
            "projectTypeKey": "software",  # Software project
            "lead": self.email,  # Project lead = current user
        }

        try:
            print(f"🔨 Criando projeto {project_key}...")
            response = self.session.post(endpoint, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✓ Projeto criado: {result.get('key')}")
                return result
            else:
                error_msg = response.text[:200]
                print(f"✗ Erro HTTP {response.status_code}: {error_msg}")
                return None

        except Exception as e:
            print(f"✗ Erro ao criar projeto: {e}")
            return None

    def wait_for_project(self, project_key: str, max_retries: int = 12, delay: int = 5) -> bool:
        """
        Aguarda projeto estar pronto para uso

        Jira Cloud pode levar alguns segundos após criação
        """
        print(f"⏳ Aguardando projeto estar pronto...")

        for attempt in range(max_retries):
            if self.project_exists(project_key):
                print(f"✓ Projeto {project_key} pronto!")
                return True

            print(f"  Tentativa {attempt + 1}/{max_retries}... aguardando {delay}s")
            time.sleep(delay)

        print(f"✗ Timeout: projeto não ficou pronto após {max_retries * delay}s")
        return False


class TaskImporter:
    """Importa tasks do TASKS.md para o Jira"""

    def __init__(self, url: str, email: str, api_token: str):
        self.url = url.rstrip("/")
        self.email = email
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

    def read_tasks(self, file_path: str) -> list:
        """Lê tasks de TASKS.md"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        tasks = []
        in_tier_table = False
        header_indices = {}

        for i, line in enumerate(lines):
            if 'Tier 2' in line or 'Tier 3' in line or 'Progress Summary' in line:
                if in_tier_table:
                    break

            if in_tier_table or ('| ID |' in line and 'Titulo' in line):
                if not in_tier_table:
                    in_tier_table = True
                    headers = [h.strip() for h in line.split('|')[1:-1]]
                    header_indices = {h.lower(): idx for idx, h in enumerate(headers)}
                    continue

                if line.strip().startswith('|-'):
                    continue

                if '|' in line:
                    cells = [c.strip() for c in line.split('|')[1:-1]]

                    if len(cells) < 3:
                        continue

                    if cells[0].startswith('ID') or not cells[0]:
                        continue

                    if not cells[0].startswith('T0.'):
                        break

                    task = {}
                    for header, idx in header_indices.items():
                        if idx < len(cells):
                            task[header] = cells[idx]

                    if task.get('id'):
                        tasks.append(task)

        return tasks

    def create_issue(self, project_key: str, task_dict: Dict) -> Optional[Dict]:
        """Cria uma issue no Jira"""
        endpoint = f"{self.url}/rest/api/2/issue"

        task_id = task_dict.get('id', '').strip()
        titulo = task_dict.get('titulo', '').strip()
        descricao = task_dict.get('descricao', '').strip()
        duracao = task_dict.get('duracao', '').strip()
        personas = task_dict.get('personas', '').strip()

        summary = f"{task_id}: {titulo}" if task_id else titulo

        desc_parts = []
        if descricao:
            desc_parts.append(descricao)
        if duracao:
            desc_parts.append(f"\nDuração estimada: {duracao}")
        if personas:
            desc_parts.append(f"Personas: {personas}")

        full_description = "\n".join(desc_parts) if desc_parts else summary

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary[:255],
                "description": full_description,
                "issuetype": {"name": "Task"},
                "labels": [
                    "sprint-0.3",
                    f"apos-{task_id}",
                ] + ([f"duration-{duracao}"] if duracao else []),
            }
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                result = response.json()
                return {
                    "success": True,
                    "task_id": task_id,
                    "jira_key": result.get("key"),
                }
            else:
                return {
                    "success": False,
                    "task_id": task_id,
                    "error": f"HTTP {response.status_code}",
                }

        except Exception as e:
            return {
                "success": False,
                "task_id": task_id,
                "error": str(e),
            }

    def import_tasks(self, project_key: str, tasks: list) -> Dict:
        """Importa múltiplas tasks"""
        results = {"total": len(tasks), "created": 0, "failed": 0, "issues": []}

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
    """Executa setup completo"""

    print("=" * 70)
    print("APOS T0.3 — Complete Jira Setup Automation")
    print("=" * 70)
    print()

    # Carrega credenciais
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    # Tenta ler de .env se não estiver em variável de ambiente
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
        print("✗ JIRA_API_TOKEN não encontrado")
        print("Configure via: export JIRA_API_TOKEN='seu-token'")
        print("Ou adicione em: .env")
        return

    print(f"🔗 Conectando a {jira_url}...")
    print(f"📧 Email: {jira_email}")
    print()

    # Fase 1: Criar Projeto
    print("=" * 70)
    print("FASE 1: Criar Projeto SCRUM")
    print("=" * 70)
    print()

    project_manager = JiraProjectManager(jira_url, jira_email, jira_api_token)

    if project_manager.project_exists("SCRUM"):
        print("✓ Projeto SCRUM já existe!")
    else:
        result = project_manager.create_project("SCRUM", "SCRUM Sprint 0.3")
        if not result:
            print("✗ Falha ao criar projeto")
            return

        # Aguarda projeto estar pronto
        if not project_manager.wait_for_project("SCRUM"):
            print("✗ Projeto não ficou pronto no tempo")
            return

    print()

    # Fase 2: Importar Tasks
    print("=" * 70)
    print("FASE 2: Importar Tasks")
    print("=" * 70)
    print()

    importer = TaskImporter(jira_url, jira_email, jira_api_token)

    tasks_file = "docs/releases/R0/sprint-0.3/TASKS.md"
    if not os.path.exists(tasks_file):
        print(f"✗ Arquivo não encontrado: {tasks_file}")
        return

    tasks = importer.read_tasks(tasks_file)
    if not tasks:
        print("⚠️ Nenhuma task encontrada")
        return

    print(f"📋 Importando {len(tasks)} tasks:\n")

    results = importer.import_tasks("SCRUM", tasks)

    print()
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print()
    print(f"✓ Projeto SCRUM: Criado")
    print(f"✓ Tasks importadas: {results['created']}/{results['total']}")

    if results["failed"] > 0:
        print(f"✗ Tasks falhadas: {results['failed']}")

    print()
    print("=" * 70)
    print("✅ SETUP COMPLETO!")
    print("=" * 70)
    print()
    print("Próximos passos:")
    print("1. Acesse: https://jadergreiner.atlassian.net/jira/software/projects/SCRUM")
    print("2. Veja as 4 issues criadas (SCRUM-1, SCRUM-2, SCRUM-3, SCRUM-4)")
    print("3. Inicie T0.3.5 Piloto (6 dias de validação com dados reais)")
    print()

    # JSON export
    print("=" * 70)
    print("DETALHES (JSON)")
    print("=" * 70)
    print()
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
