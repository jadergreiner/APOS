# APOS Commit Tracking Convention

**Versão:** 0.1.0-beta  
**Tipo:** Kernel Pattern  
**Status:** Core Standard (obrigatório para Release/Sprint Planning)

---

## O Padrão

Todos os arquivos de gerenciamento de projeto (BOARD.md, STATUS.md, TASKS.md, etc.) **devem incluir referências de commits** para rastreabilidade e auditoria.

```markdown
# Exemplo: TASKS.md

- [x] **T0.0.2** — Implementar Bootstrap Gate (2d) ✅ COMPLETO
  - Commit: `f152801`
  - Data: 19 jul
  - Esforço Real: 1 dia
```

---

## Por Que?

### 1. **Auditoria Completa**
- Cada artefato pode ser rastreado até seu commit
- Permite verificar exatamente o que foi entregue
- CI/CD pode validar alinhamento entre código e docs

### 2. **Accountability**
- Fica claro quem fez o quê
- Git blame/log mostra histórico completo
- Facilita identificar regressions

### 3. **Release Planning**
- Release manager pode validar que todos os itens foram integrados
- Previne "perda" de features entre branches
- Documenta dependências entre commits

### 4. **Retrospectivas**
- Dados concretos para análise de velocity
- Identifica gargalos (commits lentos, bloqueadores)
- Melhora estimativas futuras

---

## Padrão de Aplicação

### Em TASKS.md (Task Tracking)

```markdown
## Resumo

| Tarefa | Status | Commit | Data | Responsável |
| --- | --- | --- | --- | --- |
| T0.0.1 | ✅ COMPLETO | — | 19 jul | PM |
| T0.0.2 | ✅ COMPLETO | `f152801` | 19 jul | Engenharia |
| T0.0.3 | 📋 PRÓXIMO | — | 22+ jul | Engenharia |

**Commits de Rastreamento:**
- `f152801` — feat: implement Bootstrap Gate (T0.0.2)
- `5ce6124` — docs: update board
```

### Em BOARD.md (Sprint Kanban)

```markdown
- [x] **T0.0.2** — Bootstrap Gate (2d) ✅ COMPLETO
  - Commit: `f152801` (19 jul, 1 dia)
  - 3 validadores + 35 testes + 81% cobertura
```

### Em STATUS.md (Daily Standup)

```markdown
## Commit Tracking (Audit Trail)

| Commit | Descrição | Data | Componente |
| --- | --- | --- | --- |
| `f152801` | feat: Bootstrap Gate | 19 jul | T0.0.2 |
| `5ce6124` | docs: update board | 19 jul | BOARD.md |
| `4a3b4a8` | docs: update status | 19 jul | STATUS.md |
```

### Em RISK_MITIGATION.md (Risk Tracking)

```markdown
## Risco Resolvido — Qualidade Bootstrap Gate

**Risco:** Bootstrap Gate needs >80% test coverage  
**Mitigação:** TDD approach with 35 unit + integration tests  
**Status:** ✅ RESOLVIDO  
**Commit:** `f152801` (81% cobertura, zero critical bugs)  
**Verificação:** `pytest --cov=apos/bootstrap tests/test_bootstrap.py`
```

---

## Convenção de Commits

Para rastreamento efetivo, use:

### Formato Padrão
```
[tipo]: [descrição] ([referência de tarefa])

Opções de tipo:
- feat: Nova feature/tarefa
- fix: Bug fix
- docs: Atualização de documentação
- test: Adição/melhoria de testes
- refactor: Refatoração sem mudanças funcionais
- perf: Melhoria de performance
- chore: Manutenção, setup, deps
```

### Exemplos (APOS-compatible)
```
feat: implement Bootstrap Gate validators (T0.0.2)
test: add 35 tests for bootstrap (T0.0.2)
docs: update Sprint 0.0 board with T0.0.2 completion
docs: add commit tracking to STATUS.md
```

### Referência a Tarefas (Sempre incluir)
```
feat: implement strategy validator

Implements StrategyValidator for NORTH_STAR, OKR, PURPOSE, VALUE_PROPOSITION
validation. Enforces real quality criteria per BOOTSTRAP_GATE.md spec.

- 85% code coverage
- Validates format + content + linkage
- Fixes [T0.0.2] Bootstrap Gate implementation

Commit-Ref: f152801 (rastreabilidade)
```

---

## Padrão de Atualização (Daily/Sprint)

### Frequência
- **Daily Standups**: Atualizar STATUS.md com novos commits (07:00)
- **Sprint Planning**: Atualizar TASKS.md com rastreamento (início do sprint)
- **Release Planning**: Criar COMMIT_SUMMARY.md com audit trail completo

### Checklist
```markdown
## Antes de Fazer Push

- [ ] Código está commitado e referenciado
- [ ] Documentação atualiza TASKS.md/BOARD.md com commit
- [ ] STATUS.md inclui novo commit em audit trail
- [ ] Commit message tem referência à tarefa (T0.0.X)
- [ ] `git log --oneline` mostra histórico limpo
```

---

## Ferramentas & Automação

### Script: Extract Commits from Branch
```bash
#!/bin/bash
# Extrai commits desde última release

git log --oneline main..HEAD | grep -E "T0\.|S0\.|R[0-9]"
```

### Script: Validate Commit Coverage
```bash
#!/bin/bash
# Verifica que todas as tasks têm commits

grep -r "T0\.\|T0_[0-9]" docs/releases/ | grep -v "Commit:" | wc -l
# Deveria retornar 0 (nenhuma task sem commit)
```

### CI/CD Integration (GitHub Actions Example)
```yaml
name: Validate Commit Tracking

on: [pull_request]

jobs:
  track-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate commits in docs
        run: |
          # Verifica que cada tarefa tem commit
          grep -r "T0\." docs/releases/ | \
            grep -v "Commit:" | \
            grep -v "PRÓXIMO\|PLANEJADO" && \
            echo "❌ Tasks sem commit encontradas" && exit 1 || \
            echo "✅ Todas as tasks têm commits"
```

---

## Integração com Bootstrap Gate

O Bootstrap Gate **valida que todos os artefatos entregues têm commits referenciados**:

```python
# apos/bootstrap/validators/delivery_validator.py (futuro)

class DeliveryValidator:
    """Valida que tarefas completadas têm commits documentados."""
    
    def validate_commit_tracking(self, sprint_docs_path):
        """Verifica que cada task completa tem commit ref."""
        tasks = self._load_tasks(sprint_docs_path)
        
        for task in tasks:
            if task.status == "COMPLETO":
                if not task.commit_ref:
                    raise MissingCommitTracking(
                        f"{task.id}: Task marcada completa mas sem commit ref"
                    )
```

---

## Exemplos do Kernel

### Sprint 0.0 (19 jul)
```
✅ Completo com rastreamento:
├─ f152801 — Bootstrap Gate implementation
├─ 5ce6124 — BOARD.md updated
├─ 4a3b4a8 — STATUS.md updated
├─ 4265724 — TASKS.md tracking added
└─ ce01074 — STATUS.md audit trail
```

### Convenção Aplicada ao APOS Itself
```
APOS usa seus próprios padrões (dogfooding):
- Cada release tem COMMIT_SUMMARY.md
- Cada sprint tem commits documentados no BOARD.md
- Retrospectivas usam dados de commits para análise
```

---

## Referências

- [BOOTSTRAP_GATE.md](BOOTSTRAP_GATE.md) — Validação de fundações
- [docs/releases/R0/TASKS.md](releases/R0/sprint-0.0/TASKS.md) — Exemplo aplicado
- [CLAUDE.md](../CLAUDE.md) — Convenções de código

---

**Criado:** 2026-07-19  
**Versão:** 0.1.0-beta  
**Status:** Core Standard  
**Maintenance:** Team Lead / Release Manager
