# 🎙️ ENTREVISTA 1: CEO/PRODUCT (Jader Greiner)

**Data:** 2026-07-22 (Dia 1 — 14:00)  
**Duração:** 20 min  
**Entrevistador:** APOS Sprint Manager  
**Papel:** CEO/Product — Define estratégia, trade-offs, requisitos

---

## Q1: Experiência Atual com Adaptadores

**Pergunta:**
> "Fale-me sobre sua experiência atual com adaptadores em Meu PDI. O que você faz hoje pra conectar diferentes ferramentas/contextos?"

**Resposta (Verbatim):**

Ótima pergunta. Hoje em Meu PDI, o processo é bem manual e repetitivo.

Quando começo um novo projeto — seja integração de uma API, onboarding de um novo trader, ou análise de um novo mercado — preciso **manualmente extrair informações** sobre:
- Estrutura do projeto (src/, tests/, docs/)
- Stack tecnológico (Python 3.10? FastAPI? Pandas?)
- Convenções de código (snake_case, type hints?)
- Ferramentas usadas (pytest, black, flake8?)
- Configurações (pyproject.toml, environment vars)

Isso leva **entre 30 min a 1 hora** por novo projeto. E é **totalmente repetitivo** — sempre as mesmas perguntas.

Meu workflow hoje:
1. Clone o repo
2. Abro IDE, leia setup.py / pyproject.toml
3. Explore src/ pra entender padrão de código
4. Roda `pytest --collect-only` pra entender testes
5. Anoto tudo manualmente num doc ou Jira

O pior? **Eu refaço isso 2-3x por mês** quando onboard novos contextos. E às vezes ergo assumptions erradas (ex: "isso é uma função auxiliar" quando na verdade é crítico).

**Síntese:** Manual, repetitivo, 30-60 min/projeto, 2-3x/mês, confiança questionável.

---

## Q2: Validação - Criticidade

**Pergunta:**
> "Você concorda que descoberta automática ≥80% da estrutura seria suficiente pra Meu PDI começar?"

**Resposta (Verbatim):**

Eu diria que ≥80% é suficiente pra começar, mas com ressalvas.

O que **precisa estar nos 80%:**
- Stack tecnológico (Python version, framework)
- Estrutura de diretórios (src/, tests/, etc.)
- Convenções de naming (snake_case vs PascalCase)
- Dependências principais (requirements.txt, pyproject.toml)
- **Semântica básica:** qual é o propósito do projeto? (backend? ML? data pipeline?)
- **Ontologia inferida:** entidades principais (User, Order, Signal), relacionamentos

Os **20% restantes** que são nice-to-have:
- Detalhes de configuração de ferramentas
- Metadados de autor/versão
- Edge cases de padrão especializados

**Crítico:** Se ProjectAdapter perde semântica — tipo não entende que esse projeto é "trading bot com risk gates" — ProjectAdapter falha. A ontologia precisa estar ali.

Então: **80% = estrutura + stack + semântica principal + ontologia básica. ≥95% confiança nesse core.**

**Síntese:** ≥80% aceitável se semântica + ontologia inclusos. Confiança >85% é crítica.

---

## Q3: Dores Atuais

**Pergunta:**
> "Qual é a maior dor que você sente hoje com descoberta de estrutura de projeto?"

**Resposta (Verbatim):**

A maior dor é **retrabalho**. Toda vez que descubro um projeto novo, faço basicamente a mesma sequência:
1. Clone
2. Lê config
3. Explora src/
4. Anota assumptions
5. Descobre que estava errado em algo
6. Re-explora
7. Corrige doc

Isso acontece **2-3x por mês**, e cada ciclo leva 30-60 min.

O segundo problema é **confiança zero**. Quando documento a ontologia de um projeto manualmente, não tenho certeza se peguei tudo. Semana depois, descubro que perdi um padrão crítico ou mal-interpretei uma entidade.

Se eu pudesse automatizar UMA coisa: **capturar a semântica + ontologia de um projeto em <5 min, com ≥80% confiança, sem ter que ler código manualmente.**

Isso desbloquearia Meu PDI pra:
- Onboard contextos novos rápido
- Evitar re-descoberta
- Confiar na estrutura documentada

**Síntese:** Retrabalho (30-60 min, 2-3x/mês) + confiança zero em ontologia manual.

---

## Q4: Expectativa de ProjectAdapter

**Pergunta:**
> "Se ProjectAdapter existisse amanhã, como você usaria? What would success look like?"

**Resposta (Verbatim):**

Success pra mim seria:

**Cenário ideal:**
1. Tenho um novo projeto — digamos, um novo trader bot em Python
2. Rodo: `apos project_adapter analyze /path/to/new-bot`
3. Em <30 seg, obtenho:
   - Stack: Python 3.11, FastAPI, Pydantic, pytest
   - Estrutura: src/ layout, /tests, /docs
   - Semântica: "Risk management bot with order execution + signal filtering"
   - Ontologia: Entities (Signal, Order, RiskGate), Relationships (Signal→Order, RiskGate blocks Order)
   - Confiança score: 82%

4. Eu reviso <2 min ("sim, está certo") e ProjectAdapter popula APOS com essa ontologia automaticamente

**Success criteria:**
- ≥80% descoberta automática (não preciso retrabalho)
- Semântica capturada (não apenas estrutura)
- Integrável com Meu PDI em <5 min
- Reutilizável (próximo bot não precisa redescoberta)

**Fallback aceitável:** Se ProjectAdapter descobre 60%, eu completo 40% manualmente. Mas 80% é o target pra "não perder tempo".

**Síntese:** CLI `apos project_adapter analyze`, <30 sec, semântica + ontologia, ≥80% descoberta, <5 min integração Meu PDI.

---

## Q5: Validação - Suficiência de Automação

**Pergunta:**
> "Se ProjectAdapter descobrir ≥80% da estrutura Meu PDI no Dia 2 (milestone), é o bastante?"

**Resposta (Verbatim):**

Sim, ≥80% no Dia 2 desbloqueia meu trabalho em Meu PDI.

**Por quê:**
- Eu posso começar a usar ontologia descoberta automaticamente imediatamente
- Os 20% faltando, eu completo manualmente em paralelo (não blocking)
- Já economizo 80% do tempo de re-discovery

**Fallback aceito:** Se no Dia 2 ProjectAdapter descobrir apenas 60%, eu consigo lidar com manual discovery nos 40% faltando. Mas não fico feliz — desativa a vantagem de automação.

**Crítico:** Se ProjectAdapter **quebra nos 80% que consegue descobrir** (exemplo: erra a semântica, confunde entidades), isso é pior do que 0%. Prefiro 50% com 95% confiança do que 80% com 60% confiança.

Então: **Dia 2 milestone = ≥80% descoberta com ≥85% confiança. Se não bate isso, é failing.**

**Síntese:** ≥80% Dia 2 desbloqueia Meu PDI. Confiança >85% é crítica (qualidade > quantidade).

---

## Q6: Prioridade vs Harness (Tradeoff)

**Pergunta:**
> "No Dia 2, escolhe: continua ProjectAdapter ou foca 100% Harness (≥80% tests)? Qual é mais crítico?"

**Resposta (Verbatim):**

Essa é difícil, mas vou ser honesto: **ProjectAdapter é mais crítico pra mim.**

**Por quê:**

**Harness** é importante — preciso confiar que capabilities funcionam. Mas isso é infraestrutura. Se Harness tiver 70% coverage, eu ainda consigo trabalhar. Falha de teste me avisa depois.

**ProjectAdapter** é blocker direto pra Meu PDI. Sem descoberta automática:
- Continuo gastando 30-60 min por novo projeto
- Não consigo onboard contextos rápido
- Não tenho semântica confiável

**Mas:** Se Harness falha completamente (<50% coverage), APOS fica quebradiço e ninguém confia em capabilities. Então Harness precisa estar em "verde" mínimo (≥70%).

**Minha recomendação:** 
- **Prioridade 1:** ProjectAdapter ≥80% (debloqueia Meu PDI)
- **Prioridade 2:** Harness ≥70% (infraestrutura mínima viável)
- **Nice-to-have:** Harness ≥80% (perfeição)

Se no Dia 2 tiver que escolher entre "ProjectAdapter 80% + Harness 60%" vs "ProjectAdapter 50% + Harness 90%", eu escolho a primeira.

**Síntese:** ProjectAdapter > Harness. Mas ambos precisam estar em verde (A ≥80%, H ≥70%).

---

## Q7: Validação Final - Realistic?

**Pergunta:**
> "≥80% descoberta em 1 week é realista ou otimista?"

**Resposta (Verbatim):**

Realista, mas tight.

**Por quê é viável:**
- ProjectAdapter não precisa ser perfeito no Dia 5, precisa ser funcional
- Detectores base (estrutura, naming, patterns, config) são straightforward — não é IA complexa
- Temos R0 core (KnowledgeGraph, types) pronto; não partimos do zero
- 1 semana pra prototipagem é razoável

**Riscos que vejo:**
1. **Integração com Harness:** Se gastar 2 dias debugando Harness, ProjectAdapter fica comprimido pra 3 dias
2. **Edge cases em Meu PDI:** Se durante testes em Meu PDI encontramos edge cases não previstos, pode atrasar
3. **Semântica é difícil:** Descobrir padrões de naming/estrutura é mecânico. Mas extrair semântica (entender que esse projeto é "risk bot") pode ser tricky

**Como manter no prazo:**
- Foco em estrutura + padrões conhecidos Dia 1-2 (fácil)
- Deixar semântica inferência pra Dia 3-4 (mais complexo)
- Teste em Meu PDI Dia 4 (não Dia 5) pra ter buffer
- Se Harness ficar em 60%, não sacrifica ProjectAdapter

**Veredito:** 80% é realista. 95%? Otimista.

**Síntese:** Realista (estrutura base é straightforward). Riscos: Harness integration, edge cases, semântica complexity. Timeline: estrutura D1-2, semântica D3-4, testes D4, buffer D5.

---

## 📊 Síntese Executiva — Entrevista 1

| Aspecto | Finding | Criticidade |
|---------|---------|-------------|
| **Experiência Atual** | Manual, 30-60 min/projeto, 2-3x/mês | 🔴 PAIN POINT |
| **Suficiência 80%** | Aceitável se semântica + ontologia inclusos | ✅ VALIDADO |
| **Maior Dor** | Retrabalho + confiança zero em ontologia | 🔴 BLOCKER |
| **Expectativa** | CLI <30s, semântica, <5 min integração | ✅ CLARO |
| **Automação Dia 2** | ≥80% desbloqueia Meu PDI (confiança >85%) | ✅ CRÍTICA |
| **Prioridade** | ProjectAdapter > Harness (mas ambos needed) | 🔴 DECISÃO DIA 2 |
| **Realismo 1-week** | Realista, mas tight (riscos: Harness, edge cases) | ⚠️ VIÁVEL |

---

## ✅ Hipóteses Validadas

1. **✅ ≥80% descoberta é suficiente** — Confirmado (com confiança >85%)
2. **✅ Semântica + ontologia críticas** — Confirmado (não apenas estrutura)
3. **✅ ProjectAdapter prioritário** — Confirmado (vs Harness)
4. **✅ 1-week timeline realista** — Confirmado (estrutura base é straightforward)

---

**Entrevista concluída:** 2026-07-22 14:20  
**Status:** ✅ PRONTA PARA SÍNTESE
