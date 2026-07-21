#!/usr/bin/env python3
"""
APOS T0.3 — Task Import Demo (sem auth real)

Script que:
1. Lê tarefas de docs/releases/R0/sprint-0.3/TASKS.md
2. Gera payloads exatos que seriam criados no Jira
3. Mostra preview das issues sem precisar de autenticação

Útil para validar a estrutura antes de usar credenciais reais.
"""

import re
import json
from typing import List, Dict, Optional


class TaskParser:
    """Parse TASKS.md para extrair tasks"""

    @staticmethod
    def read_markdown_table(file_path: str) -> List[Dict]:
        """Lê tabela markdown de Tier 1 tasks"""

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        tasks = []
        in_tier_table = False
        header_indices = {}

        for i, line in enumerate(lines):
            # Para quando atinge "Tier 2" ou outra seção
            if 'Tier 2' in line or 'Tier 3' in line or 'Progress Summary' in line:
                if in_tier_table:
                    break

            # Procura header da tabela
            if in_tier_table or ('| ID |' in line and 'Titulo' in line):
                if not in_tier_table:
                    in_tier_table = True
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

                    # Valida que é task
                    if not cells[0].startswith('T0.'):
                        break

                    # Mapeia dados
                    task = {}
                    for header, idx in header_indices.items():
                        if idx < len(cells):
                            task[header] = cells[idx]

                    if task.get('id'):
                        tasks.append(task)

        return tasks


class JiraPayloadGenerator:
    """Gera payloads Jira para preview"""

    @staticmethod
    def build_issue_payload(project_key: str, task_dict: Dict) -> Dict:
        """Constrói payload exato da API v2 para uma issue"""

        task_id = task_dict.get('id', '').strip()
        titulo = task_dict.get('titulo', '').strip()
        descricao = task_dict.get('descricao', '').strip()
        duracao = task_dict.get('duracao', '').strip()
        personas = task_dict.get('personas', '').strip()
        status = task_dict.get('status', '').strip()

        # Sumário e descrição
        summary = f"{task_id}: {titulo}" if task_id else titulo

        desc_parts = []
        if descricao:
            desc_parts.append(descricao)
        if duracao:
            desc_parts.append(f"\nDuração estimada: {duracao}")
        if personas:
            desc_parts.append(f"Personas: {personas}")

        full_description = "\n".join(desc_parts) if desc_parts else summary

        # Payload API v2
        payload = {
            "fields": {
                "project": {
                    "key": project_key
                },
                "summary": summary[:255],
                "description": full_description,
                "issuetype": {
                    "name": "Task"
                },
                "labels": [
                    "sprint-0.3",
                    f"apos-{task_id}",
                ] + ([f"duration-{duracao}"] if duracao else []),
            }
        }

        return payload


def main():
    """Executa demo"""

    print("=" * 70)
    print("APOS T0.3 — Task Import to Jira [DEMO - Sem Autenticação Real]")
    print("=" * 70)
    print()

    # Lê TASKS.md
    tasks_file = "docs/releases/R0/sprint-0.3/TASKS.md"

    print(f"📖 Lendo {tasks_file}...\n")

    parser = TaskParser()
    tasks = parser.read_markdown_table(tasks_file)

    if not tasks:
        print("⚠️ Nenhuma task encontrada")
        return

    print(f"📋 Encontradas {len(tasks)} tasks em Tier 1:\n")
    for task in tasks:
        task_id = task.get('id', 'N/A')
        titulo = task.get('titulo', 'N/A')[:50]
        duracao = task.get('duracao', 'N/A')
        print(f"   • {task_id}: {titulo}")
        print(f"     Duração: {duracao}")

    print()
    print("=" * 70)
    print("PAYLOADS QUE SERIAM ENVIADOS PARA JIRA (API v2)")
    print("=" * 70)
    print()

    all_payloads = []

    for i, task in enumerate(tasks, 1):
        payload = JiraPayloadGenerator.build_issue_payload("SCRUM", task)
        all_payloads.append(payload)

        task_id = task.get('id')
        print(f"[{i}] POST /rest/api/2/issue")
        print(f"    Task: {task_id}")
        print(f"    Summary: {payload['fields']['summary'][:60]}...")
        print(f"    Labels: {', '.join(payload['fields']['labels'])}")
        print()

    # JSON completo
    print("=" * 70)
    print("JSON COMPLETO (4 payloads)")
    print("=" * 70)
    print()

    print(json.dumps(all_payloads, indent=2, ensure_ascii=False))

    print()
    print("=" * 70)
    print("INSTRUÇÕES PARA USAR COM JIRA REAL")
    print("=" * 70)
    print()
    print("1. Gere um API token em: https://id.atlassian.com/manage-profile/security/api-tokens")
    print("2. Configure credenciais:")
    print("   export JIRA_API_TOKEN='seu-token'")
    print("   export JIRA_EMAIL='seu@email.com'")
    print("3. Execute o script real:")
    print("   python scripts/jira_create_tasks.py")
    print()
    print("4. Certifique-se de que:")
    print("   - Você tem acesso ao projeto SCRUM na Jira")
    print("   - Seu token tem permissão para criar issues")
    print("   - A URL https://jadergreiner.atlassian.net está correta")
    print()


if __name__ == "__main__":
    main()
