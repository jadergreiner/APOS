# R0-AC04: Entrevista JTBD — Tech Lead

**Persona:** Tech Lead de outro projeto (não APOS)
**Objetivo:** Validar se a proposta de valor do APOS (contexto semântico para agentes) resolve uma dor real
**Formato:** 30 min, remoto (Google Meet / Zoom)

---

## 1. Perfil do Participante

| Critério | Obrigatório? |
|----------|:-----------:|
| Tech Lead ou equivalente técnico | ✅ Sim |
| Projeto com 2+ desenvolvedores | ✅ Sim |
| Usa ou ja tentou usar IA em esteira de desenvolvimento | 🟡 Preferencial |
| NÃO é do time APOS/Meu PDI | ✅ Sim |

**Onde encontrar:**
- Networking pessoal do Jader
- LinkedIn: Tech Leads de startups em SP
- Comunidades: Devs Norte, Python Brasil, He4rt

---

## 2. Roteiro de Entrevista (JTBD)

### Abertura (3 min)
- "Obrigado por participar. Estou validando uma hipótese de produto com Tech Leads."
- "Não há resposta certa ou errada — sua experiência real é o que importa."

### Warm-up (5 min)
1. "Me conta um pouco sobre o time que você lidera e o projeto principal."
2. "Quantas pessoas no time? Qual a stack? Qual o maior desafio de contexto hoje?"

### Diagnóstico — A Dor (10 min)
3. "Você já teve situações onde um agente de IA (ou novo dev) entregou algo fora do contexto porque não tinha visibilidade do negócio?"
4. **Se sim:** "Como você lidou? Quanto tempo gastou para alinhar?"
5. **Se não:** "Quando um novo desenvolvedor entra no time, quanto tempo leva até ele entender o domínio do produto?"
6. "Você usa alguma ferramenta para documentar contexto de negócio? (ADR? Wiki? README?)"
7. "O que acontece quando a documentação desalinha do código?"

### Proposta de Valor (7 min)
8. "Se eu te dissesse que existe uma ferramenta que **automaticamente descobre a estrutura do seu projeto** (stack, módulos, padrões) e valida se a documentação está alinhada com o código real, isso seria útil?"
9. "O que seria o mínimo viável para você testar essa ferramenta no seu dia-a-dia?"
10. "Qual seria a maior barreira para adotar algo assim?"

### Fechamento (5 min)
11. "Se você pudesse pedir uma funcionalidade específica, qual seria?"
12. "Posso voltar a te procurar quando tivermos um protótipo funcional para testar?"
13. "Alguém mais do seu time você recomendaria para entrevistarmos?"

---

## 3. Documentação dos Findings

Após a entrevista, documentar em `docs/discovery/entrevista-TL-YYYY-MM-DD.md`:

```markdown
# Entrevista — Tech Lead

**Data:** YYYY-MM-DD
**Participante:** [Nome], [Empresa]
**Perfil:** Tech Lead, [stack], [tamanho time]

## Dores Identificadas
- [ ] Dor confirmada: [descrição]
- [ ] Dor não confirmada: [descrição]

## Proposta de Valor
- [ ] Resolve problema real: sim/não/parcial
- [ ] Feedback sobre MVP mínimo:

## Citações Literais
> "..."

## Ações
- [ ] Incorporar feedback no backlog
- [ ] Convidar para teste de protótipo
```

---

## 4. Critério de Sucesso

- [ ] 1 entrevista realizada com Tech Lead de outro projeto
- [ ] Findings documentados em `docs/discovery/`
- [ ] No mínimo 1 dor validada ou 1 hipótese refutada
- [ ] Convite para teste de protótipo estendido (se aplicável)
