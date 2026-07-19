# APOS Bootstrap Gate — Inicialização de Projeto

**Versão:** 0.1.0-beta  
**Tipo:** Sistema de Inicialização Automática  
**Acionado:** Quando projeto importa APOS pela primeira vez

---

## O Que é Bootstrap Gate?

Bootstrap Gate é um **sistema de validação automática** que verifica se as fundações semânticas de um projeto estão em lugar.

**Fluxo:**

```
Projeto importa APOS
    ↓
Bootstrap Gate verifica:
  ✓ North Star existe?
  ✓ OKRs definidos?
  ✓ Purpose definido?
  ✓ Value Proposition definida?
  ✓ Ontologia definida?
  ✓ Semantic Layer definida?
  ✓ Knowledge Graph inicializado?
    ↓
SE TUDO EXISTE:
  → Projeto pode proceder (Release Planning)
    ↓
SE FALTA ALGO:
  → Inicia FOUNDATION DEFINITION SESSION
    → Auto-gera estrutura de Sprint 0.0
    → Guia projeto através de JTBD → North Star → OKRs → Ontology
    → Cria artefatos necessários
    ↓
APÓS SESSÃO:
  → Bootstrap Gate valida novamente
  → Se passou → Projeto pode proceder
```

---

## Checklist de Validação

### Nível Estratégico (Obrigatório)

- [ ] **NORTH_STAR.md** existe
  - Contém: visão de sucesso a longo prazo
  - Formato: "Teams [ação] [outcomes]"
  
- [ ] **PURPOSE.md** existe
  - Contém: por que projeto existe
  - Vinculado a: North Star
  
- [ ] **VALUE_PROPOSITION.md** existe
  - Contém: o que projeto entrega
  - Validado com: personas/stakeholders
  
- [ ] **OKR.md** existe
  - Contém: OKRs com métricas mensuráveis
  - Períodos: R0/R1/R2, anual, multi-ano
  - Cada OKR tem: Objetivo + 3-5 Key Results
  
- [ ] **CAPABILITIES.md** existe
  - Contém: capabilities built-in que vêm com projeto
  - Mapeado a: como projeto usa APOS

### Nível Fundações (Obrigatório)

- [ ] **ONTOLOGY_FOUNDATIONS.md** ou equivalente
  - Contém: 5 camadas (Ontologia, Semantic Layer, Knowledge Graph, Catálogo, MCP)
  - Define: conceitos core do projeto
  - Define: relações entre conceitos
  - Define: restrições de domínio
  
- [ ] **Conceitos Core Mapeados** (mínimo 5)
  - [ ] Identificados
  - [ ] Relacionados
  - [ ] Restrições definidas
  
- [ ] **Semantic Layer Definida** (mínimo 10 regras)
  - Exemplo: "Feature em Release X = todos Tasks em Release X"
  - Exemplo: "OKR alcançado = todas Métricas >= alvo"

### Nível Execução (Obrigatório)

- [ ] **Release Plan** existe
  - Contém: sprints mapeados
  - Cada sprint tem: objetivo, tasks, deliverables, risks
  
- [ ] **Sprint 0.0 Estrutura** criada
  - [ ] sprint-0.0/README.md
  - [ ] sprint-0.0/TASKS.md
  - [ ] sprint-0.0/USER_STORIES.md
  - [ ] sprint-0.0/BOARD.md
  - [ ] sprint-0.0/STATUS.md
  - [ ] sprint-0.0/RISK_MITIGATION.md
  - [ ] sprint-0.0/RETRO.md

### Nível Governança (Obrigatório)

- [ ] **GOVERNANCE.md** ou SEMANTIC_GOVERNANCE definida
  - Contém: como projeto garante alinhamento
  - Define: gates de validação
  - Define: quem aprova o quê

---

## Fluxo de Inicialização Automática

Se algum item do checklist **não existir**, o Bootstrap Gate ativa:

### Fase 1: Detecção de Gaps

```python
gate = BootstrapGate(project_path)
result = gate.validate()

if not result.passes():
    print(f"Missing foundations detected:")
    for gap in result.gaps:
        print(f"  - {gap.item}: {gap.description}")
    
    # Inicia sessão automaticamente
    session = gate.initialize_foundation_session()
```

### Fase 2: Auto-geração de Estrutura

Bootstrap Gate **auto-gera a estrutura** que falta:

```
Se falta NORTH_STAR.md:
  → Cria template docs/NORTH_STAR.md
  → Guia projeto: "Defina visão de sucesso"
  → Solicita input: descrição, métricas-chave, horizonte

Se falta OKR.md:
  → Cria template docs/OKR.md
  → Guia projeto: "Defina objetivos"
  → Solicita input: objetivos (3-5), key results (3-5 each)

Se falta Ontologia:
  → Cria template docs/ONTOLOGY.md
  → Guia projeto: "Defina conceitos core"
  → Solicita input: 5 conceitos, relações, restrições

Se falta Release Plan:
  → Cria template docs/releases/R0/SPRINT_PLAN.md
  → Cria template docs/releases/R0/BACKLOG.md
  → Cria template sprint-0.0/ structure
```

### Fase 3: Sprint 0.0 Foundation Definition

Projeto passa por **Sprint 0.0 guiado**:

```
Sprint 0.0: Foundation Definition
├─ Week 1: JTBD Discovery
│   └─ Resultado: JOB_STATEMENT.md validado
├─ Week 2: Platform Identity
│   └─ Resultado: NORTH_STAR.md, OKR.md, VALUE_PROP.md
├─ Week 3: Ontology Definition
│   └─ Resultado: ONTOLOGY.md, relações, restrições
├─ Week 4: Governance Setup
│   └─ Resultado: GOVERNANCE.md, gates definidos
└─ Resultado Final: Projeto passa Bootstrap Gate ✅
```

### Fase 4: Re-validação

```python
# Após Sprint 0.0, Bootstrap Gate valida novamente
gate.validate_after_foundation_session()

if result.passes():
    print("✅ Foundation Complete!")
    print("Projeto está pronto para:")
    print("  - Sprint Planning (R0-R4)")
    print("  - Release Execution")
    print("  - Semantic Governance")
else:
    print("❌ Gaps ainda existem, corrigir:")
    for gap in result.gaps:
        print(f"  - {gap.item}")
```

---

## Implementação em Sprint 0.0

Sprint 0.0 de qualquer projeto que importa APOS faz:

### Tarefa T0.0.1: Implementar Release Management Framework

**O quê:**
- Implementar `releases/R0/SPRINT_PLAN.md`
- Implementar `releases/R0/BACKLOG.md`
- Implementar `releases/R0/DEPENDENCY_MAP.md`
- Criar `sprint-0.0/` estrutura

**Por quê:** Projeto precisa de estrutura de execução

**Entrega:** Framework operacional, pronto para sprints

---

### Tarefa T0.0.2: Definir Fundações (via Bootstrap Gate)

**O quê:**
- JTBD Discovery (validar job)
- Definir NORTH_STAR.md
- Definir PURPOSE.md
- Definir VALUE_PROPOSITION.md
- Definir ONTOLOGY.md
- Definir SEMANTIC_LAYER.md
- Definir GOVERNANCE.md

**Por quê:** Projeto precisa de fundações semânticas

**Entrega:** Todos os docs necessários existem e validados

---

### Tarefa T0.0.3: Executar Bootstrap Gate

**O quê:**
- Rodar `apos.bootstrap_gate.validate()`
- Se falha: corrigir gaps
- Se passa: liberar projeto para Sprint Planning

**Por quê:** Garantir que fundações estão em lugar

**Entrega:** ✅ Bootstrap Gate PASSED

---

## Exemplo: APOS Usando Seu Próprio Bootstrap Gate

```
APOS importa a si mesmo (dogfooding)
    ↓
Bootstrap Gate verifica:
  ✓ NORTH_STAR.md ✅ (existe em APOS/)
  ✓ OKR.md ✅ (existe em APOS/)
  ✓ PURPOSE.md ✅ (existe em APOS/)
  ✓ VALUE_PROPOSITION.md ✅ (existe em APOS/)
  ✓ ONTOLOGY_FOUNDATIONS.md ✅ (existe em docs/releases/R0/)
  ✓ Release Plan ✅ (existe em docs/releases/R0/SPRINT_PLAN.md)
  ✓ Sprint 0.0 ✅ (estrutura em sprint-0.0/)
    ↓
Bootstrap Gate PASSED ✅
    ↓
APOS está pronto para executar Sprint 0.0
(E de fato, está executando agora!)
```

---

## Benefícios do Bootstrap Gate

| Benefício | Valor |
|-----------|-------|
| **Auto-discovery** | Projeto sabe exatamente o que falta |
| **Auto-remediation** | Templates auto-gerados, guias passo-a-passo |
| **Consistency** | Todos os projetos que usam APOS têm mesma estrutura |
| **Accountability** | Gate passa só quando fundações estão reais (não "by assumption") |
| **Dogfooding** | APOS se valida a si mesmo |
| **Knowledge Transfer** | Novo projeto aprende APOS através de Sprint 0.0 guiado |

---

## Código do Bootstrap Gate (Pseudo)

```python
class BootstrapGate:
    """Sistema de validação e inicialização automática de fundações APOS."""
    
    REQUIRED_ITEMS = [
        'NORTH_STAR.md',
        'PURPOSE.md',
        'VALUE_PROPOSITION.md',
        'OKR.md',
        'ONTOLOGY_FOUNDATIONS.md',
        'CAPABILITIES.md',
        'docs/releases/R0/SPRINT_PLAN.md',
        'docs/releases/R0/BACKLOG.md',
        'sprint-0.0/',
        'GOVERNANCE.md'
    ]
    
    def validate(self):
        """Valida se todas as fundações existem e estão mapeadas."""
        gaps = []
        for item in self.REQUIRED_ITEMS:
            if not self._exists(item):
                gaps.append(Gap(item))
        
        return GateResult(
            passes=len(gaps) == 0,
            gaps=gaps
        )
    
    def initialize_foundation_session(self):
        """Inicia sessão guiada de definição de fundações."""
        session = FoundationDefinitionSession()
        
        # Guia projeto através de JTBD → Strategy → Ontology
        session.run_jtbd_discovery()
        session.run_platform_identity()
        session.run_ontology_definition()
        session.run_governance_setup()
        
        # Auto-gera todos os artefatos
        session.generate_artifacts()
        
        return session
    
    def validate_after_session(self):
        """Re-valida após sessão de inicialização."""
        return self.validate()
```

---

## Deploy de Bootstrap Gate

Bootstrap Gate é parte do **APOS Core**:

```
apos/
├── bootstrap/
│   ├── __init__.py
│   ├── gate.py                 # Bootstrap Gate logic
│   ├── session.py              # Foundation Definition Session
│   ├── templates/              # Auto-generated templates
│   │   ├── NORTH_STAR.md
│   │   ├── OKR.md
│   │   ├── ONTOLOGY.md
│   │   └── ...
│   └── validators/             # Validation rules
│       ├── strategy_validator.py
│       ├── ontology_validator.py
│       └── governance_validator.py
│
└── __init__.py
    # from .bootstrap import BootstrapGate
    # apos.bootstrap_gate = BootstrapGate()
```

---

## Uso Prático

```python
# Projeto novo importa APOS
import apos

# Rodar Bootstrap Gate
gate = apos.BootstrapGate()
result = gate.validate()

if not result.passes():
    print("Fundações faltando, iniciando sessão...")
    session = gate.initialize_foundation_session()
    # Projeto passa por Sprint 0.0 guiado
    session.run()
    
    # Re-validar
    result = gate.validate_after_session()
    if result.passes():
        print("✅ Fundações definidas! Pronto para Sprint Planning.")

# Se passou, projeto pode fazer release planning
release_mgr = apos.ReleaseManagement()
release = release_mgr.create_release("R0", ...)
```

---

**Created:** 2026-07-19  
**Version:** 0.1.0-beta  
**Status:** Parte de APOS Core (R0-Sprint-0.0)
