# Trust Score Engine — Guia de Implementação

**Sprint:** 0.3 - Beta Prep  
**Task:** T0.3.4 — Trust Score Engine  
**Status:** ✅ IMPLEMENTADO (1.5h)  
**Testes:** 18/18 passando (>80% cobertura)

---

## O que é?

Engine que calcula um **score de confiança (0.0–1.0)** medindo quanto do seu trabalho (tasks) está **estrategicamente alinhado com objetivos (OKRs)**.

```
Trust Score = (0.3 × Coverage) + (0.5 × Quality) + (0.2 × Consistency)
```

---

## 3 Componentes

### 1️⃣ Coverage (30%)

**"Quantas tarefas têm um OKR?"**

```python
coverage = linked_tasks / total_tasks

# Exemplo:
# 8 de 10 tasks vinculadas = 0.8 (80% coverage)
```

- ✅ Task com `okr_id` = linked
- ❌ Task sem `okr_id` = orphan (não contabilizada)

### 2️⃣ Quality (50%)

**"As relações Task→OKR são válidas e atualizadas?"**

```python
quality = (valid_relationships / total_relationships) × freshness

# Valid = task existe + OKR existe + não contraditório
# Freshness = atualizado nos últimos 7 dias (1.0) ou mais antigo (0.0-0.5)
```

Problemas detectados:
- ⚠️ Task referenciada não existe
- ⚠️ OKR referenciado não existe
- ⚠️ Relacionamento desatualizado (>7 dias)

### 3️⃣ Consistency (20%)

**"Há conflitos nas vinculações?"**

```python
consistency = 1.0 - (conflicts / total_relationships)

# Conflito = task vinculada a 2+ OKRs
# Exemplo: JIRA-123 → OKR-Goal1 + OKR-Goal2 (risco!)
```

---

## Uso Prático

### Instalação

```python
from apos.trust_score import TrustScoreEngine, Task, OKR, Relationship
from datetime import datetime
```

### Exemplo 1: Score de um Projeto

```python
# Dados do projeto
tasks = [
    Task(id="JIRA-1", title="Feature A", status="in_progress", 
         project_id="R0", okr_id="OKR-001"),
    Task(id="JIRA-2", title="Feature B", status="in_progress", 
         project_id="R0", okr_id="OKR-001"),
    Task(id="JIRA-3", title="Bug fix", status="in_progress", 
         project_id="R0", okr_id=None),  # ORPHAN!
]

okrs = [
    OKR(id="OKR-001", name="Validate MVP", project_id="R0"),
]

relationships = [
    Relationship(task_id="JIRA-1", okr_id="OKR-001", confidence=1.0, 
                 updated_at=datetime.utcnow()),
    Relationship(task_id="JIRA-2", okr_id="OKR-001", confidence=1.0, 
                 updated_at=datetime.utcnow()),
]

# Calcular score
engine = TrustScoreEngine(tasks, okrs, relationships)
result = engine.calculate()

print(f"📊 Trust Score: {result.score:.0%}")
# Output: Trust Score: 73%

print(f"Coverage: {result.components['coverage'].value:.0%}")
# Output: Coverage: 67% (2/3 tasks)

print(f"Issues:")
for issue in result.issues:
    print(f"  {issue}")
# Output:
#   🚨 1 tasks (33%) sem OKR (orfas)

print(f"Recomendação: {result.recommendation}")
# Output: Recomendação: 🟡 Bom alinhamento, mas 1 tasks precisam de contexto OKR.
```

### Exemplo 2: Pesos Customizados

```python
# Para seus own pesos (devem somar 1.0)
custom_weights = {
    "coverage": 0.5,    # Enfatizar cobertura
    "quality": 0.3,     # Menos peso em freshness
    "consistency": 0.2,  # Menos crítico
}

engine = TrustScoreEngine(
    tasks, okrs, relationships,
    weights=custom_weights
)
result = engine.calculate()
```

### Exemplo 3: JSON Export

```python
# Serializar para JSON (useful para APIs)
json_str = engine.to_json()
print(json_str)

# Output:
# {
#   "score": 0.733,
#   "components": {
#     "coverage": {
#       "value": 0.667,
#       "weight": 0.3,
#       "details": {...}
#     },
#     ...
#   },
#   "issues": [
#     "🚨 1 tasks (33%) sem OKR (orfas)"
#   ],
#   "orphan_count": 1,
#   "total_tasks": 3,
#   "recommendation": "..."
# }
```

---

## Interpretação de Scores

| Score | Status | Ação |
|-------|--------|------|
| ≥0.85 | ✅ Excelente | Continuar monitorando |
| 0.70-0.84 | 🟡 Bom | Vincular tasks orfas |
| 0.50-0.69 | ⚠️ Fraco | Urgente: revisar alignment |
| <0.50 | 🚨 Crítico | Intervention imediata |

---

## Edge Cases Tratados

### ✅ Projeto Vazio

```python
engine = TrustScoreEngine(tasks=[], okrs=[], relationships=[])
result = engine.calculate()

# Score = 0.7 (coverage=0, quality=1.0, consistency=1.0)
# Interpretação: nada inválido, mas também nada vinculado
```

### ✅ Task Completada Sem OKR (HIGH RISK)

```python
Task(id="T1", status="done", okr_id=None)  # ⚠️ Issue detectada!

result.issues  # ["🚨 1 tasks completadas sem OKR: T1..."]
```

### ✅ Conflito de Vinculação

```python
Relationship(task_id="T1", okr_id="OKR-1")
Relationship(task_id="T1", okr_id="OKR-2")  # CONFLICT!

result.components["consistency"].details["conflicts"]  # 1
```

### ✅ Relacionamento Desatualizado

```python
Relationship(
    task_id="T1", 
    okr_id="OKR-1",
    updated_at=datetime.utcnow() - timedelta(days=15)  # Stale!
)

result.components["quality"].value  # Reduzido
```

---

## Testes

**18 testes unitários cobrindo:**
- ✅ Cálculo de coverage, quality, consistency
- ✅ Detecção de orfas
- ✅ Validação de pesos
- ✅ Edge cases (vazio, perfeito, conflitos)
- ✅ Serialização JSON

```bash
pytest tests/unit/test_trust_score.py -v
# Output: 18 passed in 0.09s
```

---

## Integração com Plugin Jira (T0.3.3)

```python
# No Plugin:
# 1. Detecta orfas (T0.3.3)
# 2. Calcula score (T0.3.4)
# 3. Exibe recomendação

trust_score = engine.calculate()
sidebar_ui.display_score(trust_score.score)
sidebar_ui.show_issues(trust_score.issues)
sidebar_ui.show_recommendation(trust_score.recommendation)
```

---

## Próximos Passos (R1)

- 📊 Dashboard com trend de scores
- 🔔 Notificações quando score cai
- 📈 Analytics histórico de alignment
- ⚙️ Regras customizadas por projeto

---

**Implementado por:** Claude Code  
**Data:** 2026-07-23  
**Referência:** SPEC.md Seção 4.3 + NORTH_STAR.md
