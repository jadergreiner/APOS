#!/usr/bin/env python3
"""
APOS T0.3 — Jira Setup com Fallback Manual

Script que:
1. Tenta criar projeto SCRUM via API (se token tiver permissões)
2. Se falhar, oferece guia manual de 2 minutos
3. Aguarda confirmação que projeto foi criado
4. Importa 4 tasks automaticamente
"""

import os
import time
import json
import requests
from typing import Dict, Optional


class JiraSetup:
    """Gerencia setup do Jira com fallback manual"""

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
            endpoint = f"{self.url}/rest/api/2/project/search?keys={project_key}"
            response = self.session.get(endpoint, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data.get('values', []) and len(data['values']) > 0
        except:
            pass
        return False

    def create_project_via_api(self, project_key: str) -> bool:
        """Tenta criar projeto via API"""
        print("🔨 Tentando criar projeto via API...")

        endpoint = f"{self.url}/rest/api/2/project"
        payload = {
            "key": project_key,
            "name": "SCRUM Sprint 0.3",
            "projectTypeKey": "software",
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=10)

            if response.status_code in [200, 201]:
                print("✓ Projeto criado via API!")
                return True
            else:
                print(f"✗ API retornou HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Erro: {e}")
            return False

    def wait_for_project(self, project_key: str, max_retries: int = 12) -> bool:
        """Aguarda projeto estar pronto"""
        print(f"⏳ Aguardando projeto estar pronto...")

        for attempt in range(max_retries):
            if self.project_exists(project_key):
                print(f"✓ Projeto {project_key} pronto!")
                return True

            print(f"  Tentativa {attempt + 1}/{max_retries}...", end="\r")
            time.sleep(5)

        return False

    def read_tasks(self, file_path: str) -> list:
        """Lê tasks de TASKS.md"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        tasks = []
        in_tier_table = False
        header_indices = {}

        for line in lines:
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

                    if len(cells) < 3 or cells[0].startswith('ID') or not cells[0]:
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
        desc_parts = [descricao] if descricao else []
        if duracao:
            desc_parts.append(f"Duração: {duracao}")
        if personas:
            desc_parts.append(f"Personas: {personas}")

        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary[:255],
                "description": "\n".join(desc_parts) if desc_parts else summary,
                "issuetype": {"name": "Task"},
                "labels": ["sprint-0.3", f"apos-{task_id}"] + ([f"duration-{duracao}"] if duracao else []),
            }
        }

        try:
            response = self.session.post(endpoint, json=payload, timeout=10)
            if response.status_code in [200, 201]:
                result = response.json()
                return {"success": True, "task_id": task_id, "jira_key": result.get("key")}
            else:
                return {"success": False, "task_id": task_id, "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"success": False, "task_id": task_id, "error": str(e)}

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
                print(f"  ✗ {result['task_id']}")

        return results


def show_manual_setup_guide():
    """Mostra guia manual de setup"""
    print()
    print("=" * 70)
    print("CRIAÇÃO MANUAL DE PROJETO (2 minutos)")
    print("=" * 70)
    print()
    print("Como token possui permissões limitadas, crie o projeto manualmente:")
    print()
    print("1. Acesse: https://jadergreiner.atlassian.net")
    print("2. Clique: Projects → Create project")
    print("3. Preencha:")
    print("   • Type: Scrum (ou Kanban)")
    print("   • Name: SCRUM")
    print("   • Key: SCRUM")
    print("   • Lead: Jader Greiner")
    print("4. Clique: Create")
    print("5. Aguarde ~30 segundos para inicialização")
    print()


def main():
    """Executa setup"""

    print("=" * 70)
    print("APOS T0.3 — Jira Setup Automático")
    print("=" * 70)
    print()

    # Carrega credenciais
    jira_url = os.getenv("JIRA_URL", "https://jadergreiner.atlassian.net")
    jira_email = os.getenv("JIRA_EMAIL", "jadergreiner@gmail.com")
    jira_api_token = os.getenv("JIRA_API_TOKEN")

    # Fallback .env
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
        print("✗ Token não encontrado")
        return

    print(f"🔗 Jira: {jira_url}")
    print(f"📧 Email: {jira_email}")
    print()

    setup = JiraSetup(jira_url, jira_email, jira_api_token)

    # Fase 1: Projeto
    print("=" * 70)
    print("FASE 1: Projeto SCRUM")
    print("=" * 70)
    print()

    if setup.project_exists("SCRUM"):
        print("✓ Projeto SCRUM encontrado!")
    else:
        print("🔍 Projeto SCRUM não encontrado")
        print()
        print("Tentando criar via API...")

        if setup.create_project_via_api("SCRUM"):
            print("✓ Projeto criado via API")
            setup.wait_for_project("SCRUM")
        else:
            print()
            show_manual_setup_guide()
            print("⏹️  PARADO: Crie o projeto e execute novamente:")
            print("   python scripts/jira_setup_auto.py")
            print()
            return

    print()

    # Fase 2: Tasks
    print("=" * 70)
    print("FASE 2: Importar Tasks")
    print("=" * 70)
    print()

    tasks_file = "docs/releases/R0/sprint-0.3/TASKS.md"
    if not os.path.exists(tasks_file):
        print(f"✗ {tasks_file} não encontrado")
        return

    tasks = setup.read_tasks(tasks_file)
    if not tasks:
        print("⚠️ Nenhuma task encontrada")
        return

    print(f"📋 Importando {len(tasks)} tasks:\n")

    results = setup.import_tasks("SCRUM", tasks)

    print()
    print("=" * 70)
    print("✅ SETUP COMPLETO!")
    print("=" * 70)
    print()
    print(f"✓ Projeto: SCRUM")
    print(f"✓ Tasks importadas: {results['created']}/{results['total']}")

    if results["created"] > 0:
        print()
        print("Próximos passos:")
        print("1. Acesse: https://jadergreiner.atlassian.net/jira/software/projects/SCRUM")
        print("2. Veja as issues (SCRUM-1 até SCRUM-4)")
        print("3. Inicie T0.3.5 Piloto (6 dias de validação com dados reais)")
        print()
        print("T0.3.5 Piloto começa agora! 🚀")


if __name__ == "__main__":
    main()
