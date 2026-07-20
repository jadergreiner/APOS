# Commit Tracking Kernel Implementation Spec

**Status:** 🔴 **NOT STARTED** (Sprint 0.1 task)  
**Objective:** Converter Commit Tracking de padrão documentado para **Kernel implementado** — validação automática enforçada por CI/CD quando projeto importa APOS.

---

## Por Que Isso É Kernel?

Quando projeto importa APOS, deve receber:

✅ **Bootstrap Gate** — validação automática de 10 fundações (já implementado)  
✅ **Semantic Validation** — enforcement de critérios reais em validators (já implementado)  
🔴 **Commit Tracking CI** — validação que tarefas têm refs de commit (TODO)

Sem Commit Tracking validado automaticamente:
- ❌ Audit trail invisível
- ❌ Retrospectivas sem dados concretos
- ❌ Release planning sem rastreabilidade
- ❌ Débito técnico escondido

---

## O Que Implementar

### 1. **CommitTrackingValidator** (`apos/kernel/commit_tracking.py`)

**Responsabilidade:** Validar que artefatos de sprint têm refs de commit.

```python
from apos.kernel.commit_tracking import CommitTrackingValidator

validator = CommitTrackingValidator(
    sprint_root="docs/releases/R0/sprint-0.0/"
)

result = validator.validate()
# Returns: ValidationResult
#   - tasks_with_commits: 8/8 ✅
#   - board_tracked: True ✅
#   - status_tracked: True ✅
#   - issues: []
#   - score: 1.0
```

**Validações:**

- [ ] TASKS.md tem seção "Commits de Rastreamento" com lista de commits
  - [ ] Cada tarefa completa referencia ≥1 commit
  - [ ] Formato: `commit_hash — commit message`
- [ ] BOARD.md tem "Audit Trail" section com commits
- [ ] STATUS.md tem "Commit Tracking" section com timeline
- [ ] USER_STORIES.md tem "Commit(s)" field para cada story
- [ ] RETRO.md tem "Commits Analisados" seção

**Output:**

```python
@dataclass
class CommitTrackingResult:
    score: float  # 0.0-1.0
    status: str  # "PASS", "CONDITIONAL", "FAIL"
    issues: List[str]  # Detalhes de o quê faltou
    tracked_commits: List[str]  # Commits encontrados
    untracked_tasks: List[str]  # Tarefas sem commit
    validation_details: Dict[str, bool]  # Por artefato
```

---

### 2. **BootstrapGate Integration**

**Onde integrar:** `apos/bootstrap/gate.py`

BootstrapGate já checa 10 fundações. Precisamos adicionar validação de commit tracking ao fluxo:

```python
def validate_with_details(self) -> BootstrapResult:
    # Validações existentes (NORTH_STAR, OKR, etc.)
    existing_checks = [...]
    
    # NOVO: Commit tracking validation
    if self.is_release_sprint():  # Se em contexto de release/sprint
        commit_result = CommitTrackingValidator(
            sprint_root=self.sprint_path
        ).validate()
        
        if commit_result.score < 0.80:
            return BootstrapResult(
                status="CONDITIONAL",
                issues=[...existing..., commit_result.issues]
            )
```

**Quando executar:**

- ✅ `python -m apos init` — valida foundation + commit tracking
- ✅ `python -m apos validate-sprint` — valida sprint integrity (novo comando)
- 🔴 CI/CD — GitHub Actions workflow (TODO: adicionar)

---

### 3. **GitHub Actions CI/CD Integration**

**Arquivo:** `.github/workflows/validate-commit-tracking.yml`

```yaml
name: Validate Commit Tracking

on:
  pull_request:
    paths:
      - 'docs/releases/**/TASKS.md'
      - 'docs/releases/**/BOARD.md'
      - 'docs/releases/**/STATUS.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install APOS
        run: pip install -e ".[dev]"
      
      - name: Validate Commit Tracking
        run: |
          python -m apos validate-sprint \
            --sprint-root docs/releases/ \
            --strict
      
      - name: Report Issues
        if: failure()
        run: |
          echo "❌ Commit Tracking Validation Failed"
          echo "All deliverables must reference commits:"
          echo "  - TASKS.md: Commits de Rastreamento section"
          echo "  - BOARD.md: Audit Trail section"
          echo "  - STATUS.md: Commit Tracking section"
          exit 1
```

**Comportamento:**
- 🟢 PASS (score ≥0.80): PR pode merge
- 🟡 CONDITIONAL (0.60-0.80): PR blocked, precisa de action
- 🔴 FAIL (<0.60): PR blocked, deve documentar commits

---

### 4. **CLI Command: `python -m apos validate-sprint`**

**Adicionar:** `apos/__main__.py`

```bash
$ python -m apos validate-sprint \
  --sprint-root docs/releases/R0/sprint-0.0 \
  --strict

Validando Commit Tracking
==========================

✅ TASKS.md — 8/8 tarefas rastreadas
✅ BOARD.md — Audit Trail section encontrado
✅ STATUS.md — Commit Tracking section encontrado
✅ USER_STORIES.md — 5/5 histórias com commits
✅ RETRO.md — 10 commits analisados

Score: 1.0 (PASS)
────────────────

Todos artefatos têm rastreamento de commit ✅
```

---

### 5. **Export público no package**

**Arquivo:** `apos/__init__.py`

```python
from apos.kernel.commit_tracking import CommitTrackingValidator, CommitTrackingResult

__all__ = [
    # Kernel patterns
    "BootstrapGate",
    "SemanticGate",
    "CommitTrackingValidator",  # NEW
    # ... resto ...
]
```

**Uso por downstream projects:**

```python
from apos import CommitTrackingValidator

# Em seu CI/CD ou script de validação
validator = CommitTrackingValidator(sprint_root="docs/releases/R0/sprint-0.0")
result = validator.validate()

if result.status != "PASS":
    print(f"Commit tracking issues: {result.issues}")
    sys.exit(1)
```

---

## Implementation Checklist

### Phase 1: Core Implementation (Sprint 0.1 — 1 dia)

- [ ] `apos/kernel/` — Criar diretório + `__init__.py`
- [ ] `apos/kernel/commit_tracking.py` — CommitTrackingValidator class
  - [ ] `validate()` — main validation method
  - [ ] `validate_tasks()` — check TASKS.md
  - [ ] `validate_board()` — check BOARD.md
  - [ ] `validate_status()` — check STATUS.md
  - [ ] `validate_user_stories()` — check USER_STORIES.md
  - [ ] `validate_retro()` — check RETRO.md
- [ ] `CommitTrackingResult` dataclass
- [ ] Tests: `tests/unit/test_commit_tracking_validator.py`
  - [ ] Test valid sprint (all commits tracked)
  - [ ] Test missing section (no Audit Trail)
  - [ ] Test partial tracking (some tasks missing commits)
  - [ ] Test edge cases

### Phase 2: BootstrapGate Integration (Sprint 0.1 — 1 dia)

- [ ] Add CommitTrackingValidator check to `BootstrapGate.validate_with_details()`
- [ ] Integrate result into `BootstrapResult`
- [ ] Update tests: `tests/test_bootstrap.py`
- [ ] Document in CLAUDE.md

### Phase 3: CLI Command (Sprint 0.1 — 0.5 dia)

- [ ] Add `validate-sprint` subcommand to `apos/__main__.py`
- [ ] Implement argument parsing (--sprint-root, --strict)
- [ ] Pretty-print results
- [ ] Tests: `tests/unit/test_main_cli.py` (add validate-sprint tests)

### Phase 4: CI/CD Integration (Sprint 0.1 — 0.5 dia)

- [ ] Create `.github/workflows/validate-commit-tracking.yml`
- [ ] Test with real PR (trigger on TASKS.md/BOARD.md changes)
- [ ] Document in CLAUDE.md → "GitHub Actions" section

### Phase 5: Export + Documentation (Sprint 0.1 — 0.5 dia)

- [ ] Export CommitTrackingValidator in `apos/__init__.py`
- [ ] Add usage examples to `examples/`
- [ ] Update `README.md` with Kernel pattern reference
- [ ] Update `CLAUDE.md` → "Padrões de Kernel"

---

## Success Criteria

✅ Sprint 0.1 end-of-sprint should have:

- [ ] CommitTrackingValidator implemented + tested (≥80% coverage)
- [ ] BootstrapGate integrated + tests passing
- [ ] CLI command working: `python -m apos validate-sprint`
- [ ] CI/CD workflow configured + tested
- [ ] Public export in `apos/__init__.py`
- [ ] CLAUDE.md updated → Commit Tracking is now FULL KERNEL
- [ ] Documentation clear: "Quando projeto importa APOS, recebe CommitTrackingValidator automático"

---

## Rationale

**Sprint 0.0 Learning:** Commit Tracking pattern foi estabelecido como kernel, mas não é enforçado automaticamente. Isso significa:

- ❌ Downstream projects que importam APOS podem ignorar padrão
- ❌ Audit trail é "esperado" mas não garantido
- ❌ Retrospectivas podem ter dados incompletos

**Com Commit Tracking Kernel:**

- ✅ BootstrapGate valida automaticamente
- ✅ CI/CD bloqueia PRs sem commit tracking
- ✅ Audit trail é garantido, não aspiracional
- ✅ Release planning baseado em dados concretos é padrão

---

**Referência:** [docs/COMMIT_TRACKING.md](COMMIT_TRACKING.md), [CLAUDE.md](../CLAUDE.md), [Sprint 0.0 RETRO](releases/R0/sprint-0.0/RETRO.md)

