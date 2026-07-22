# 🎙️ ENTREVISTA 2: SME TÉCNICO

**Data:** 2026-07-22 (Dia 1 — 14:20)  
**Duração:** 20 min  
**Entrevistador:** APOS Sprint Manager  
**Papel:** SME Técnico — Validar viabilidade técnica, surface edge cases

---

## Q1: Viabilidade Técnica

**Pergunta:**
> "Analisando Meu PDI como codebase, qual é sua avaliação inicial de viabilidade do ProjectAdapter? É factível descobrir ≥80% automaticamente?"

**Resposta (Verbatim):**

Viabilidade é boa, mas com nuances.

**O que é fácil (descobrível em 30 min):**
- Stack: Python version, Django, FastAPI, requirements.txt — trivial via regex/AST
- Estrutura: src/, tests/, docs/ — filesystem inspection
- Naming conventions: snake_case vs PascalCase — sampling de arquivos
- Config: pyproject.toml, setup.py — parser TOML/INI

**O que é harder (1-2h de análise):**
- Módulos + imports: Preciso parse Python AST completo pra mapear dependencies
- ORM models (Django): Need análise de models.py — doável, mas requires Python parsing
- API endpoints (FastAPI): Routes estão em decorators — AST parsing resolve

**O que é muito hard (3-4h, possível mas complexo):**
- Domain relationships: "Signal triggers Order, RiskGate blocks Order" — não está no código, está na lógica de negócio
- Semantics: Qual é propósito real? ("risk bot" vs "data ingestion") — precisa LLM ou manual inference
- Business rules: Onde estão constraints (ex: "risk never > 10%") — espalhados em business logic

**Viabilidade realista:**
- **80% estrutural (stack, modules, patterns):** Sim, 100% factível em 1 week
- **80% com domain semantics:** Borderline — precisa de heuristics + maybe LLM para inference
- **80% com business rules:** Não realista sem manual input

**Meu veredito:** ≥80% descoberta é viável se focamos em estrutura + stack + modules. Semântica/domínio vai ser ~60-70% automático, precisará revisão/manual.

**Síntese:** Estrutura/stack viável (90% realista). Semântica complexa (60-70% realista). Total: 75-80% viável.

---

## Q2: Estratégia de Descoberta

**Pergunta:**
> "Se você fosse implementar ProjectAdapter, qual seria sua estratégia de descoberta? Como chegaria aos 80%?"

**Resposta (Verbatim):**

Eu faria em 3 fases, progressivas:

**Fase 1 — Discovery de estrutura real (Dia 1-2, 50% cobertura):**
1. Filesystem inspection: detecta todos os top-level directories (src/, backend/, frontend/, docs/, knowledge/, scripts/, etc.)
2. Characteriza cada diretório:
   - `backend/` → backend code (Python, Node, Go?)
   - `frontend/` → frontend code (React, Vue, etc.)
   - `knowledge/` → domain/knowledge base (not code, but important semantically)
   - `docs/` → documentation
3. Config parsing: pyproject.toml, setup.py, package.json, requirements.txt (qualquer que exista)
4. Identifica entry points: qual é o "main" do projeto?

Isso é flexible — filesystem walk + pattern matching. Não assume src/tests/docs, se adapta ao que existe. ~6-8 horas de dev.

**Fase 2 — Language-specific module mapping (Dia 2-3, +25% = 75% total):**
1. Para cada directory identificado, detecta linguagem (Python? JavaScript? etc.)
2. Parse language-specific AST:
   - **Python:** AST parsing, imports, classes/functions
   - **JavaScript:** Parse .js files, extract functions/components
   - **Documentation:** Parse markdown headers, structure
3. Build dependency graph (what depends on what)
4. Identify patterns:
   - `backend/models/` → likely ORM models
   - `frontend/components/` → likely UI components
   - `knowledge/ontology/` → likely domain entities/relationships

Isso é modular — cada linguagem tem seu detector. ~8-10 horas de dev.

**Fase 3 — Heuristic semântica (Dia 3-4, +5-10% = 80-85% total):**
1. Cross-directory relationships:
   - `backend/models/Signal` + `backend/services/SignalProcessor` → "Signal is processed by SignalProcessor"
   - `knowledge/entities/` + class definitions → map entities to code
2. Heuristics por directory type:
   - Anything in `knowledge/` → semantic importance (domain entities, rules, constraints)
   - `backend/` + `frontend/` → client-server relationship
   - `docs/` → documentation of relationships (parse README, architecture docs)
3. Optional: LLM inference (README → propósito do projeto)

**Meu sequenciamento:**
- **Dia 1:** Directory structure discovery + config (flexible, adaptive)
- **Dia 2:** Language-specific AST parsing (Python, JavaScript, etc.)
- **Dia 3:** Cross-directory relationships + heuristics
- **Dia 4:** Teste em Meu PDI (backend/ + frontend/ + knowledge/ discovery), refine heuristics
- **Dia 5:** Buffer + polish

**Priorização:** Estrutura real > Language-specific modules > Semântica. Se rodar out of time, drop semântica, mantém 70% structural (ainda útil).

**Síntese:** 3 fases (filesystem → language-specific AST → heuristics). Flexible pra estruturas variadas. Prioriza estrutura > semântica.

---

## Q3: Dores Técnicas

**Pergunta:**
> "Na sua experiência com descoberta de estrutura, qual é a maior dor técnica? O quê mais quebra?"

**Resposta (Verbatim):**

Maior dor: **Ambiguidade em padrões + redundância estrutural.**

**Exemplos que quebram descoberta:**

1. **Redundância/Duplicidade de propósito:**
   - `/docs/knowledge/` vs `/knowledge/` na raiz — mesma coisa em dois lugares?
   - Qual é canonical? Qual é legacy?
   - Automação não sabe qual confiar, pode detectar ambas como "duplicadas" ou perder uma

2. **Diretórios com múltiplos propósitos:**
   - `/backend/utils/` — é utility? Ou é mini-feature?
   - `/knowledge/rules/` — são regras de negócio? Ou configuração?
   - Decisão é subjetiva, automação erra 40% das vezes

3. **Implícito vs explícito:**
   - Relacionamento `Signal → Order`: está em decorador? Em lógica de negócio? Em banco de dados?
   - Não é óbvio onde procurar, precisa análise contextual profunda

4. **Linguagens mistas:**
   - Meu PDI tem backend Python + frontend JavaScript + knowledge markdown
   - Preciso de 3 parsers diferentes, cada um com suas quirks
   - Integrar os 3 pra ter view coerente é o harder

5. **Evolução de padrões:**
   - Projeto começa com `backend/models/`, depois migra pra `backend/domain/`
   - Ainda tem ambos em código (legacy + novo)
   - Descoberta precisa lidar com coexistência + detectar qual é "active"

**Onde gasto mais tempo debugando:**
- **Redundância:** quando mesmo conceito está em múltiplos places (docs/ vs knowledge/)
- Relacionamentos entre módulos (import analysis)
- Distinguir "real module" vs "utility folder" vs "legacy folder"
- Determinar se algo é semanticamente importante (domain entity) vs infrastructure

**Crítico:** Falsa positivos (detecta estrutura que não é real) vs falsos negativos (perde padrão importante). E agora: **como lidar com duplicidade sem descartar informação importante?**

**Síntese:** Duplicidade + ambiguidade + linguagens mistas + evolução. Maior risco: falsos positivos/negativos.

---

## Q4: Validação - ≥80% é viável?

**Pergunta:**
> "Você concorda que ≥80% descoberta automática é viável em 1 week pra ProjectAdapter core? Qual % é realista?"

**Resposta (Verbatim):**

Depende da definição de "80%".

**Se 80% significa "estrutura + stack + módulos":** Sim, 100% viável em 1 week. Isso é determinístico — filesystem walk + AST parsing. Realista: 85-90%.

**Se 80% inclui "semântica + relacionamentos + redundância handling":** Mais tight. Realista: 70-75%.

**Minha avaliação honesta:**

- **Estrutural descoberta:** 90% realista (directories, stack, modules, patterns)
- **Semântica descoberta:** 60% realista (domain entities, relationships — precisa heuristics)
- **Redundância handling:** 50% realista (detect duplicidade? Qual é canonical? Hard problem)
- **Confiança geral:** 75% (qual é a qualidade dos 80% descobertos?)

**Então:**
- **80% quantity (descobrir X% das coisas):** Realista
- **80% quality (confiar nos 80% descobertos):** Mais pessimista — talvez 70% confidence

**Minha recomendação:** Target 80% quantity em Dia 2. Depois refine quality (confiança) em Dias 3-4 com testes em Meu PDI.

**Se forçado a escolher:** 80% estrutura + 60% semântica = hybrid "70% útil". Mas isso é suficiente pra desbloquear Meu PDI (conforme CEO disse).

**Síntese:** 80% quantity realista (estrutura+modules). 70% quality realista (confiança). Hybrid: 70% útil é suficiente.

---

## Q5: Integração com APOS + Plano de Refatoração

**Pergunta:**
> "Como você vê ProjectAdapter se conectando com BootstrapGate + ContextEngine + KnowledgeGraph? Quais são dependências e mudanças no projeto?"

**Resposta (Verbatim):**

Analisando integração APOS + Meu PDI, encontro **4 problemas estruturais** que bloqueiam viabilidade:

### **Problema 1: Duplicidade Semântica**

**Situação:** `/docs/knowledge/` + `/knowledge/` na raiz — mesma coisa, dois places.

**Impacto:**
- ProjectAdapter detecta ambas como "knowledge"
- BootstrapGate não sabe qual é canonical
- ContextEngine constrói ontologia duplicada

**Solução (Mudança no Projeto):**
```
REMOVER: /docs/knowledge/ 
MOVER: /knowledge/ → /docs/knowledge/ (canonical)
RESULTADO: Single source of truth em /docs/knowledge/
```

**Justificativa:** Conhecimento é documentação, pertence em /docs/. Limpa raiz.

---

### **Problema 2: Ambiguidade Estrutural**

**Situação:** `/backend/` contém tudo (models, services, utils). Impossível distinguir "domain" de "infrastructure".

**Impacto:**
- ProjectAdapter não sabe o que é semanticamente importante
- Ontologia fica confusa (Order é entity ou util?)
- Confiança score cai

**Solução (Mudança no Projeto):**
```
RENOMEAR: /backend/models/ → /backend/domain/entities/
RENOMEAR: /backend/services/ → /backend/domain/services/
MOVER: /backend/utils/ → /backend/infrastructure/utils/
RESULTADO: domain/ claramente separado de infrastructure/

Novo layout:
/backend/domain/
  ├── entities/ (Signal, Order, RiskGate)
  ├── services/ (SignalProcessor, OrderExecutor)
  └── rules/ (business constraints)
/backend/infrastructure/
  ├── database/
  ├── utils/
  └── config/
```

**Justificativa:** Domain-Driven Design. ProjectAdapter descobre semanticamente sem ambiguidade.

---

### **Problema 3: Desnormalização de Config**

**Situação:** Configuração espalhada em `pyproject.toml`, `.env`, `/backend/config/`, `/docs/CONFIG.md`.

**Impacto:**
- ProjectAdapter não sabe qual é "canonical config"
- Diferentes places têm valores conflitantes
- Semântica fica inconsistente

**Solução (Mudança no Projeto):**
```
CANONICAL: /backend/config/settings.py (código fonte)
UNIFICAR: pyproject.toml, .env, CONFIG.md → referenciam /backend/config/settings.py
RESULTADO: Single source of truth pra config
```

**Justificativa:** Elimina conflito, ProjectAdapter encontra config em um place.

---

### **Problema 4: Incompatibilidade Frontend-Backend**

**Situação:** `/frontend/` é React standalone, `/backend/` é Django. Não está claro como se integram.

**Impacto:**
- ProjectAdapter não detecta "API contract" entre front/back
- Ontologia não sabe que Signal → Order é cross-boundary
- Semântica fica split

**Solução (Mudança no Projeto):**
```
CRIAR: /backend/api/schemas/ (OpenAPI/YAML)
RESULTADO: API contracts explícitos, descobríveis

/backend/api/
  ├── schemas/
  │   ├── Signal.yaml
  │   ├── Order.yaml
  │   └── RiskGate.yaml
  └── routes/
      ├── signals.py
      └── orders.py

/frontend/api/
  └── generated/
      └── client.ts (auto-gerado de schemas/)
```

**Justificativa:** API contracts são semântica explícita. ProjectAdapter lê schemas, descobre relationships.

---

### **Plano de Refatoração (Dia 1 ou antes de Dia 2)**

| # | Mudança | Tipo | Esforço | Bloqueador? |
|---|---------|------|---------|------------|
| 1 | Remove `/docs/knowledge/`, manter `/knowledge/` | Remover | 30 min | ⚠️ SIM |
| 2 | Reorganize `/backend/` em domain/ + infrastructure/ | Renomear + Mover | 2-3h | ⚠️ SIM |
| 3 | Canonicalize config em `/backend/config/settings.py` | Unificar | 1-2h | 🟡 NICE |
| 4 | Explicit API contracts em `/backend/api/schemas/` | Criar | 2-3h | 🟡 NICE |

**Crítico:** Mudanças #1 e #2 precisam ser feitas ANTES de ProjectAdapter rodar. Senão descoberta fica 60% confidence.

**Síntese:** 4 problemas (duplicidade, ambiguidade, desnormalização, incompatibilidade) + 4 soluções (remover, renomear, unificar, mover). Refatoração é pré-requisito.

---

## Q6: Suficiência Arquitetural

**Pergunta:**
> "Se ProjectAdapter descobrir ≥80% e passar pro BootstrapGate, você confia que o resto do pipeline funciona?"

**Resposta (Verbatim):**

Sim, **com ressalvas críticas.**

**Se as mudanças de refatoração (Q5) forem feitas:**
- Estrutura limpa (domain/ separado de infrastructure/)
- Config canonicalizado
- API contracts explícitos
- Duplicidades resolvidas

**Então:** Sim, confio que pipeline funciona end-to-end.

**Mas depende de 3 assunções críticas que PRECISAM ser true:**

### **Assunção 1: ProjectProfile schema está correto**

Se ProjectProfile carrega estrutura + detections + confidence_score + canonical_choices, então BootstrapGate consegue validar.

**Risco:** Schema muda durante implementação, causa incompatibilidade.

**Mitigation:** Freezar schema Dia 1, não mexer.

---

### **Assunção 2: BootstrapGate consegue validar com confiança 70-80%**

Se Gate consegue dizer "essa estrutura é ≥70% confiável", então ContextEngine confia em input.

**Risco:** Gate rejeita ProjectProfile por "não confiável o bastante", bloqueia pipeline.

**Mitigation:** Define limiar realista (70%, não 95%).

---

### **Assunção 3: ContextEngine consegue transformar ProjectProfile em ontologia coerente**

Se ContextEngine pega ProjectProfile + refactored Meu PDI e produz ontologia que KnowledgeGraph entende, então tudo conecta.

**Risco:** ContextEngine espera formato que ProjectProfile não produz.

**Mitigation:** Alinhar ContextEngine spec com ProjectProfile output agora (antes de dev).

---

## **Se refatoração NÃO for feita:**

Pipeline ainda funciona, mas:
- ProjectProfile confidence = 60%
- BootstrapGate rejeita por "low confidence"
- Bloqueia tudo

**Veredito:** Refatoração é PRÉ-REQUISITO, não optional.

**Síntese:** Sim, se refatoração feita + 3 assunções true. Senão: bloqueado.

---

## Q7: Realistic Timeline

**Pergunta:**
> "≥80% ProjectAdapter core em 1 week é realista? Qual é sua estimativa honesta?"

**Resposta (Verbatim):**

Realista, **MAS com dependência crítica de refatoração.**

**Estimativa breakdown:**

```
ProjectAdapter core (sem refatoração): 1.5 SP (4-5 dias)
- Fase 1 (filesystem + config): 0.5 SP (1 dia)
- Fase 2 (AST parsing + modules): 0.75 SP (2 dias)
- Fase 3 (heuristics + semântica): 0.25 SP (1 dia)

Refatoração Meu PDI (pré-requisito): 1.5 SP (2-3 dias)
- Remove duplicidade: 0.25 SP (30 min)
- Reorganize domain/infrastructure: 0.75 SP (2-3h)
- Canonicalize config: 0.5 SP (1-2h)

TOTAL: 3.0 SP (5-6 dias) ← TIGHT pra 1 week
```

**Cronograma realista:**

```
Dia 1 (Seg):   Refatoração start + ProjectAdapter design
Dia 2 (Ter):   Refatoração 80% done + ProjectAdapter Fase 1
Dia 3 (Qua):   Refatoração complete + ProjectAdapter Fase 2
Dia 4 (Qui):   ProjectAdapter Fase 3 + testes em Meu PDI
Dia 5 (Sex):   Buffer + polish

Milestone Dia 2 (Ter 16h):
  - ProjectAdapter ≥50% (Fase 1 completa)
  - Refatoração em progresso (Dia 2 ~80%)
  - Viabilidade confirmada (não bloqueado)
```

**Incertezas:**

1. **Refatoração é REAL WORK:** Não é só renamear; é atualizar imports, testes, documentação. Pode ter bugs. Estimativa: +20% buffer.

2. **Edge cases em Meu PDI:** Pode haver padrões não previstos (config em lugar estranho, imports circulares, etc.). Descoberto Dia 3-4. Impacto: 1+ dia.

3. **Integração com Harness:** Se Harness tests quebram em paralelo, puede atrasar. Impacto: compartilha contexto, developer distraction.

**Meu veredito:** ✅ Realista se:
- Refatoração começa JÁ (Dia 1)
- Harness não atrasa em paralelo
- Edge cases são mínimos

❌ Se qualquer desses falha: 1 week é tight, melhor dizer 10-12 dias.

**Honest estimate: 1.5 SP ProjectAdapter + 1.5 SP Refatoração = 3 SP total. 1 week cobre se developer trabalha full-time, sem interruptions.**

**Síntese:** Realista se refatoração já começa. 3 SP total (ProjectAdapter 1.5 + Refatoração 1.5). Tight, não confortável.

---

## 📊 Síntese Executiva — Entrevista 2

| Aspecto | Finding | Criticidade |
|---------|---------|------------|
| **Viabilidade Estrutura** | 90% realista (filesystem + AST) | ✅ VIÁVEL |
| **Viabilidade Semântica** | 60% realista (heuristics, LLM needed) | ⚠️ COMPLEXA |
| **Duplicidade** | /docs/knowledge/ vs /knowledge/ | 🔴 BLOCKER |
| **Ambiguidade** | /backend/ sem domain/infrastructure split | 🔴 BLOCKER |
| **Desnormalização** | Config espalhada em 4 places | 🟠 PROBLEMA |
| **Incompatibilidade** | Frontend/backend sem API contracts | 🟠 PROBLEMA |
| **80% Viável?** | Sim, se refatoração feita | ✅ COM CONDIÇÃO |
| **Timeline 1-week** | Realista, mas tight (3 SP total) | ⚠️ APERTADO |

---

## ✅ Recomendações Críticas

1. **START REFACTORING NOW** (Dia 1, não Dia 2)
   - Remove /docs/knowledge/ duplicity
   - Split /backend/ into domain/ + infrastructure/
   - Canonicalize config

2. **FREEZE ProjectProfile SCHEMA TODAY** (Dia 1, não durante dev)
   - Define exact fields: structure, detections, confidence_score, canonical_choices
   - Share with BootstrapGate + ContextEngine teams

3. **PARALLELIZE AGGRESSIVELY**
   - Refactoring Team: Dia 1-3 (Meu PDI)
   - ProjectAdapter Team: Dia 1-5 (code)
   - Harness Team: Dia 1-5 (tests)
   - NO SERIALIZATION

4. **MILESTONE Dia 2 SUCCESS = Refactoring DONE + ProjectAdapter Fase 1 COMPLETE**
   - Not "perfect", just "unblocked"

---

**Entrevista concluída:** 2026-07-22 14:40  
**Status:** ✅ PRONTA PARA SÍNTESE
