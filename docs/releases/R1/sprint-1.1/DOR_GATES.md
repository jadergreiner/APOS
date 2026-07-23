# DoR Gates — Sprint 1.1

**Regra:** NENHUM subagent inicia implementacao sem que TODOS os criterios do DoR estejam verdes.
**Gate tipo:** Pre-flight — cancela se qualquer criterio falhar.

---

## Gate G0: DoR Geral (TODAS as tasks)

### Contexto Carregado
- [ ] **G0-CTX-01:** Repositorio APOS clonado em `/mnt/c/repo/APOS`
- [ ] **G0-CTX-02:** `python3 -c "import apos"` funciona sem erro
- [ ] **G0-CTX-03:** `pytest --version` disponivel
- [ ] **G0-CTX-04:** Modulo alvo da task existe (`ls apos/<modulo>/`)

### Dependências
- [ ] **G0-DEP-01:** Nenhuma dependencia externa bloqueante (API, servico externo)
- [ ] **G0-DEP-02:** Tasks predecessor concluidas (se aplicavel)
- [ ] **G0-DEP-03:** Artefatos de design/refinamento existem (se aplicavel)

### Baseline
- [ ] **G0-BSL-01:** Coverage baseline registrado (`pytest --cov=apos/<modulo>`)
- [ ] **G0-BSL-02:** Testes existentes passando antes de qualquer alteracao
- [ ] **G0-BSL-03:** `git status` limpo (working tree sem modificacoes nao comitadas)

### Ambiente
- [ ] **G0-ENV-01:** Python >= 3.9 disponivel
- [ ] **G0-ENV-02:** Dependencias do projeto instaladas (`pip install -e ".[dev]"`)
- [ ] **G0-ENV-03:** Espaco em disco > 500MB

---

## Gate G1: DoR Especifico por Task

### T1.1.5 — Polish + Edge Cases ✅ (Concluida)

| ID | Criterio | Status |
|----|----------|--------|
| G1-01 | Tech Lead review (PARECER_TECH_LEAD_TRILHA_A.md) lido | ✅ |
| G1-02 | Gaps de coverage conhecidos: base.py 90%, OverflowError, schema stub | ✅ |
| G1-03 | 100 testes agent_harness + 80 testes capability_harness existentes | ✅ |
| G1-04 | `pytest --cov=apos/harness` baseline = 99% core | ✅ |

### R1.T2 — Capabilities Coverage 80%+

| ID | Criterio | Quem Verifica |
|----|----------|---------------|
| **G1-R1T2-01** | `R1.T2_REFINAMENTO.md` existe com 57 cenarios mapeados | PO/PM |
| **G1-R1T2-02** | 4 modulos mapeados: model.py, taxonomy.py, router.py, agents.py | PO/PM |
| **G1-R1T2-03** | Nenhuma dependencia externa — testes sao 100% unitarios | Tech Lead |
| **G1-R1T2-04** | Diretorio `tests/unit/test_capabilities/` criado (vazio) | Ambiente |
| **G1-R1T2-05** | Coverage baseline: `pytest --cov=apos/capabilities` = 0% registrado | Tech Lead |
| **G1-R1T2-06** | `from apos.capabilities import *` funciona sem erro de import | Ambiente |
| **G1-R1T2-07** | Ordem de implementacao: model.py → taxonomy.py → agents.py → router.py | Tech Lead |
| **G1-R1T2-08** | NENHUM subagent comeca sem DoR aprovado pelo PO | PO |

**Script de verificacao (rodar antes de comecar):**
```bash
cd /mnt/c/repo/APOS
echo "=== G1-R1T2-04 ===" && ls tests/unit/test_capabilities/ 2>/dev/null || mkdir -p tests/unit/test_capabilities/ && touch tests/unit/test_capabilities/__init__.py
echo "=== G1-R1T2-05 ===" && python3 -m pytest --cov=apos/capabilities --cov-report=term-missing tests/unit/test_capabilities/ -q 2>&1 | tail -5
echo "=== G1-R1T2-06 ===" && python3 -c "from apos.capabilities import model, taxonomy, router, agents; print('imports OK')"
```

### R1.2 — Bootstrap Gate 2.0

| ID | Criterio | Quem Verifica |
|----|----------|---------------|
| **G1-R12-01** | ProjectAdapter existe e `from apos.project_adapter import ProjectAdapter` funciona | Ambiente |
| **G1-R12-02** | `BootstrapGate` existe em `apos/bootstrap/gate.py` — lido e compreendido | Tech Lead |
| **G1-R12-03** | `ProjectProfile` schema conhecido (campos: language, framework, database, etc.) | Tech Lead |
| **G1-R12-04** | `apos/project_adapter/adapter.py` lido — `analyze()` retorna profile + confidence | Tech Lead |
| **G1-R12-05** | Testes existentes do BootstrapGate passam (`pytest tests/ -k bootstrap -q`) | Ambiente |
| **G1-R12-06** | Meu PDI acessivel em `/mnt/c/repo/meu-pdi` (para testes de integracao) | Ambiente |
| **G1-R12-07** | Ordem: analisar gate.py → criar BootstrapGateV2 → testes unitarios → integracao | Tech Lead |
| **G1-R12-08** | NENHUM subagent comeca sem DoR aprovado pelo PO | PO |

**Script de verificacao:**
```bash
cd /mnt/c/repo/APOS
echo "=== G1-R12-01 ===" && python3 -c "from apos.project_adapter import ProjectAdapter; print('ProjectAdapter OK')"
echo "=== G1-R12-02 ===" && python3 -c "from apos.bootstrap.gate import BootstrapGate; print('BootstrapGate OK')"
echo "=== G1-R12-04 ===" && python3 -c "
from apos.project_adapter import ProjectAdapter
pa = ProjectAdapter()
from pathlib import Path
p = pa.discover(Path('/mnt/c/repo/meu-pdi/backend'))
print(f'discover() OK: {p.language}, {p.framework}')
"
echo "=== G1-R12-05 ===" && python3 -m pytest tests/ -k bootstrap -q --tb=short
echo "=== G1-R12-06 ===" && ls /mnt/c/repo/meu-pdi/ 2>/dev/null | head -3
```

### R0-AC04 — Stakeholder Externo

| ID | Criterio | Quem Verifica |
|----|----------|---------------|
| **G1-AC04-01** | Perfil da persona definido (ex: gestor de produto, dev lider) | PO |
| **G1-AC04-02** | Roteiro de entrevista JTBD preparado | PO/PM |
| **G1-AC04-03** | Nao depende de codigo — task 100% de descoberta | Tech Lead |
| **G1-AC04-04** | Consumidor identificado para os findings (ex: backlog do produto) | PO |
| **G1-AC04-05** | NENHUM subagent comeca sem DoR aprovado pelo PO | PO |

---

## Gate G2: Pre-Implementation Gate (Subagent)

**O subagent DEVE rodar este gate antes de escrever QUALQUER linha de codigo.**

```python
def pre_implementation_gate(task_id: str) -> bool:
    \"\"\"Retorna True se todos os criterios DoR estao verdes.\"\"\"
    checks = {
        "G0-CTX-01": Path("/mnt/c/repo/APOS").exists(),
        "G0-CTX-02": __import__("apos"),
        "G0-BSL-01": True,  # coverage baseline registrado
        "G0-BSL-02": True,  # testes existentes passam
        "G0-BSL-03": True,  # git status limpo
        # ... criterios especificos da task
    }
    for name, result in checks.items():
        if not result:
            print(f"❌ {name}: FAIL — nao iniciar implementacao")
            return False
    print("✅ DoR Gate PASS — pode iniciar implementacao")
    return True
```

---

## Gatilhos de Cancelamento

Se qualquer criterio DoR falhar, o subagent DEVE:
1. **Parar imediatamente** — nao escrever codigo
2. **Reportar** qual criterio falhou e por que
3. **Sugerir acao** — o que precisa ser resolvido para destravar
4. **Aguardar aprovacao** do PO/PM para prosseguir

**NUNCA** contornar um DoR falho com "vou implementar e depois ajusto." Isso gera retrabalho documentado em S1.0.
