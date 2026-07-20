# JTBD Interview #1: PM Leader (Mock)

**Data:** 2026-07-20 (Mock for demonstration)  
**Duração:** ~45 min  
**Persona:** Sarah Chen, VP of Product  
**Contexto:** TechStartup (12 PMs, ~100 eng, Jira/Confluence)

---

## Resumo de Descobertas

- **Push Force (Frustração):** Re-explica contexto 5h/semana, orphaned features 20-30%
- **Pull Force (Atração):** Dashboard visual Task→OKR→Métrica + automação
- **Habit Force (Status Quo):** Jira integrado + adoption friction
- **Anxiety Force (Medo):** Confiabilidade de dados, integração complexity

---

## Key Findings

### **Pain Point #1: Context Loss & Re-explanation**

**Frequência:** 3-5x por semana (daily basis)  
**Impacto:** ~5 horas/semana (10% do tempo de VP)  
**Contexto:** Novos PMs + time membros perguntam por que X é priorizado

> **Direct Quote:**  
> "Sarah: Diário. No mínimo 3-5 vezes por semana eu estou explicando contexto de prioridade... Deve ser umas 5 horas por semana que eu gasto re-explicando contexto."

### **Pain Point #2: Orphaned Features**

**Frequência:** Contínuo (descoberto months after delivery)  
**Impacto:** 20-30% de capacity em features sem OKR backing  
**Contexto:** Features fazer sentido isoladamente, mas não aligned com estratégia

> **Direct Quote:**  
> "Sarah: Features que fazem sentido em isolação, mas não aligned com estratégia. A gente deve ter uns 20-30% de capacity em features assim."

### **Pain Point #3: Manual OKR Validation**

**Frequência:** Ad-hoc (ao revisar OKRs trimestrais)  
**Impacto:** Descoberta tardia (meses depois) que feature não era prioritária  
**Contexto:** Sem real-time visibility se delivery mapeia para estratégia

> **Direct Quote:**  
> "Sarah: Ad-hoc. A gente entrega, e aí alguns meses depois revisamos OKRs e vemos se feature ajudou ou não."

---

## Validação de VALUE_PROPOSITION

| Aspecto | Validou? | Feedback |
|---------|----------|----------|
| Proposta de Valor | ✅ FORTE | "Game-changer" se pudesse clicar Task→OKR→Métrica |
| Redução de Retrabalho | ✅ FORTE | 5h/semana em re-explanation, -50% seria impacto |
| Visibilidade de Alinhamento | ✅ FORTE | "Aí eu não teria que ficar repetindo" |
| Prevenção de Orphaned Features | ✅ FORTE | "Ajudaria a evitar features sem OKR" |
| Simplicidade é Key | ✅ Conditionally | Toparia testar "se for super simples" |

**Score:** 4/5 aspectos validados com força

---

## Jobs Framework Analysis

### **Push Forces (O que empurra)**

**Force #1: Frustração de Retrabalho Contínuo**
- Frequência: Daily (3-5x/semana explícito)
- Intensidade: 9/10
- Quote: "Você sente que está indo em círculos. O trabalho não progride."
- Impacto: 5h/semana, 10% do tempo de VP

**Force #2: Visibility Gap em Alinhamento**
- Frequência: Contínuo (cada task/feature)
- Intensidade: 8/10
- Quote: "Se a gente visse 'essa feature não tá mapeada a um OKR ativo', a gente questionava"
- Impacto: 20-30% capacity em features orphaned

**Force #3: Team Frustração (Cascata)**
- Frequência: Regular
- Intensidade: 7/10
- Quote: "Alguns PMs juniores me disseram que se sentem perdidos"
- Impacto: Morale, efficiency

**Agregação Push:** Muito forte (8.3/10 média), múltiplas frentes

### **Pull Forces (O que atrai)**

**Pull #1: Automated Context Accessibility**
- Atração Level: 9/10
- Quote: "Se eu pudesse clicar em uma task e ver 'aqui está o OKR'"
- Diferencial: Visual + real-time + centralized

**Pull #2: Zero Switching Cost Learning**
- Atração Level: 8/10
- Quote: "Novo PM chega, eu aponto 'clica aqui, veja Task → OKR'"
- Diferencial: Knowledge embedded in tool

**Pull #3: Capacity Liberation**
- Atração Level: 8/10
- Quote: "20% de capacity liberada para coisas que realmente importam"
- Diferencial: ROI quantificável

**Agregação Pull:** Forte (8.3/10 média), múltiplas frentes

### **Habit Forces (Status Quo)**

**Habit #1: Jira Ecosystem Dependence**
- Severidade: 7/10
- Quote: "Jira tá integrado em tudo. CI/CD, roadmap tools, tudo fala com Jira"
- Switching Cost: High (integration work)

**Habit #2: Team Familiarity**
- Severidade: 6/10
- Quote: "Meu time já tá acostumado com Jira"
- Switching Cost: Learning curve

**Habit #3: Status Quo Inertia**
- Severidade: 5/10
- Quote: N/A (not strongly mentioned)
- Switching Cost: "If not broken..."

**Agregação Habit:** Moderate (6/10 média), can be overcome com simplicity

### **Anxiety Forces (Medo)**

**Anxiety #1: Adoption Friction**
- Severidade: 8/10
- Quote: "Adoption é continuous... Se tool é complexa, não usa, vira shelfware"
- Preocupação: Tool complexity

**Anxiety #2: Data Reliability**
- Severidade: 6/10
- Quote: "Se tool quebra ou dados desalinham de Jira, a gente tem um problema"
- Preocupação: Data quality + sync

**Anxiety #3: Integration Complexity**
- Severidade: 5/10 (conditional)
- Quote: "Se a gente troca ou adiciona outra ferramenta, é trabalho de integração"
- Preocupação: One-time but friction

**Agregação Anxiety:** Moderate-High (6.3/10), mitigable com design

---

## Padrões Identificados (vs VALUE_PROPOSITION)

**Alinhamento:**
- ✅ "Reduce context re-explanation" — Direct validation (5h/week)
- ✅ "Prevent orphaned features" — Direct validation (20-30% capacity)
- ✅ "Real-time visibility Task→OKR→Metric" — Direct validation ("game-changer")
- ✅ "Confidence scoring" — Not mentioned, but "data reliability" is concern

**Não Mencionados Espontaneamente:**
- ❌ AI agent context injection (Sarah não é AI focused)
- ❌ Semantic governance (não uso language formal)
- ❌ Knowledge graph modeling (too technical)

**Recomendação:** VALUE_PROPOSITION deve emphasize PM workflow + visualization, não semantic layer jargon

---

## Interesse em Piloto

**Pergunta:** Estaria aberto a ser early adopter?  
**Resposta:** ✅ SIM, com condições

**Condições:**
- MVP deve estar ready antes de setembro (Q4 planning)
- Deve ser "super simples" (simplicity is prerequisite)
- Integration com Jira must work seamlessly

**Timeline:** Q4 2026 para piloto ideal (pré-Black Friday roadmap)

**Referências:** VP Engineering + Analytics Lead (similar pain)

---

## Follow-up Actions

- [x] Documentar entrevista (JTBD_INTERVIEWS.md)
- [ ] Send thank you (Slack/email)
- [ ] Add Sarah to early adopter list (conditional)
- [ ] Follow up com VP Eng + Analytics Lead referrals

---

## Notas Internas

**Tonalidade:** Sarah foi open, honest, genuinely frustrated com status quo. Alta receptividade a solução. Não foi defensive.

**Confidence:** High confidence nesta entrevista. Push forces são real, pull forces resonate, anxiety é solvable com design (simplicity is key).

**Next Interview Insight:** Esperaríamos que EM/Tech Lead valide "orphaned features" desde perspectiva diferente (code delivery), AI Architect valide "context for agents".

---

## Consolidação: MVP Implication

Baseado nesta entrevista:

**Must-Have para MVP:**
1. ✅ Task→OKR linkage (core job)
2. ✅ Visual dashboard (PM workflow requirement)
3. ✅ "Unmapped features" detection (orphaned feature problem)
4. ✅ Real-time updates (not batch/delayed)

**Should-Have:**
1. ~ Jira native connector (integration prerequisite)
2. ~ Onboarding for new PMs (knowledge transfer)

**Nice-to-Have:**
1. ~ Analytics export (not mentioned)
2. ~ AI context injection (not mentioned by PM persona)

**NOT in MVP:**
1. ❌ Semantic scoring (too complex, not mentioned)
2. ❌ Full governance framework (later release)
3. ❌ Support for 10+ integrations (Jira-only MVP)

---

## Job Statement (Preliminary)

**Based on single interview — validate with 4+ more:**

```
When [VP/PM Leader] is planning sprints and has 20+ tasks/features in backlog,
I need to quickly see which tasks map to which OKRs and which features lack OKR backing,
so that I can make data-driven prioritization decisions and avoid wasting 20-30% of capacity on misaligned work.
```

**Key Metrics:**
- Reduction in context re-explanation: -50% to -75% (from 5h → 1-2h/week)
- Prevention of orphaned features: Avoid 10-20% of misdirected capacity
- Time-to-context: From "re-explain in meeting" to "click in tool" (<5 seconds)

---

**Interview Quality:** ⭐⭐⭐⭐⭐ (Excellent — clear pain, clear need, clear value)

**Validation Strength:** Strong (4/5 VALUE_PROPOSITION aspects validated)

**Confidence in Direction:** HIGH
