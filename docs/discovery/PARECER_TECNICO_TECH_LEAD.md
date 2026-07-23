# Parecer Técnico — Entrevista Tech Lead (R0-AC04)

**Data:** 2026-07-23  
**Elaborado por:** APOS Discovery Agent  
**Base:** `FINDINGS_TECH_LEAD.md` + `ENTREVISTA_TECH_LEAD.md`  
**Status:** ✅ Consolidado e priorizado

---

## 1. Resumo Executivo

A entrevista com o Tech Lead (roleplay Jader — Meu PDI) validou **5 dores** com severidade entre Alta e Média. As dores convergem para um problema-raiz: **inexistência de um mecanismo automático de contexto semântico que evolua com o código e a documentação.**

O ProjectAdapter já existe como base técnica, mas está subutilizado — não há validação ativa código↔docs, rastreamento de decisões nem prevenção de desalinhamento. O parecer recomenda tratar as 3 dores críticas (D01, D02, D03) como requisitos **R1.2 obrigatórios**, e D04/D05 como **R1.3 desejáveis**, respeitando a regra de setup zero.

---

## 2. Análise de Riscos por Dor

### 🔴 D01 — Contexto perdido entre sprints (20-30min retomada)

| Dimensão | Análise |
|----------|---------|
| **Severidade** | Alta |
| **Frequência** | Toda troca de sprint / retomada de task |
| **Impacto atual** | 20-30 min de overhead cognitivo por retomada. Em 10 sprints, ~4h desperdiçadas por pessoa. Em time de 4 pessoas: ~16h/sprint cycle |
| **Risco técnico** | Baixo — solução é viável com ProjectProfile + metadata persistido |
| **Impacto na arquitetura** | Adiciona persistência de sessão/cache de contexto no ProjectProfile. Pode exigir hash do estado do projeto para invalidar cache |
| **Tratamento** | Cache de perfil com invalidação via diff de estrutura. Recalcular apenas quando houve mudança detectada |

### 🔴 D02 — Documentação desalinha do código sem detecção

| Dimensão | Análise |
|----------|---------|
| **Severidade** | Alta |
| **Frequência** | Contínua — documentação desalinha em dias (ADR-009) |
| **Impacto atual** | Agentes de IA consomem docs obsoletas → decisões erradas → retrabalho |
| **Risco técnico** | Médio — falsos positivos são barreira de adoção confirmada. Exige heurística conservadora |
| **Impacto na arquitetura** | Novo módulo `apos/validation/` com comparador código↔docs. Integração com BootstrapGate. Precisa de baseline (hash atual) e diff |
| **Tratamento** | Validar contra hash do projeto, não contra docs externas. Regra: só reportar divergência confirmada por parsing de AST |

### 🔴 D03 — Contexto repetido manualmente em tasks de IA

| Dimensão | Análise |
|----------|---------|
| **Severidade** | Alta |
| **Frequência** | Toda task delegada a agente (3-5 parágrafos por vez) |
| **Impacto atual** | 3-5 parágrafos de contexto boilerplate por task. Propaga inconsistências |
| **Risco técnico** | Baixo — o ProjectProfile já estrutura esse contexto. Falta middleware de injeção automática |
| **Impacto na arquitetura** | Cria `ContextInjector` como middleware entre delegador e executor. Compatível com Harness |
| **Tratamento** | Template de contexto enriquecido com output do ProjectAdapter. Injeção automática via decorator/middleware |

### 🟡 D04 — Rastro de decisões espalhado em 20+ docs

| Dimensão | Análise |
|----------|---------|
| **Severidade** | Média |
| **Frequência** | Consultas pontuais — OAuth state documentado em 4 lugares diferentes |
| **Impacto atual** | Dúvida sobre qual doc é a fonte da verdade. Risco de seguir decisão revogada |
| **Risco técnico** | Médio — exige rastreamento ADR → SDD → código. ADRs não estruturados hoje |
| **Impacto na arquitetura** | Novo módulo `apos/traceability/`. Mapeamento de referências cruzadas entre artefatos |
| **Tratamento** | Não cria ADR retroativamente. Impõe que novas decisões sigam o rastro. Pode indexar docs existentes |

### 🟡 D05 — Stack assumptions erradas por agentes

| Dimensão | Análise |
|----------|---------|
| **Severidade** | Média |
| **Frequência** | Ocorrências documentadas (SDD-0006, SDD-0072) |
| **Impacto atual** | Agentes assumem Redis/PostgreSQL num projeto que usa DynamoDB single-table. Gera propostas de implementação inválidas |
| **Risco técnico** | Baixo — o StackDetector já cobre 80% deste cenário |
| **Impacto na arquitetura** | Enriquecer StackDetector com mais heurísticas. Publicar restrições de stack no perfil |
| **Tratamento** | Expandir detecção de serviços AWS. Incluir alerta de "non-stack" em propostas |

---

## 3. Priorização

| Dor | Impacto Técnico | Risco de Implementação | Dependência | Prioridade | Sprint |
|-----|----------------|----------------------|-------------|-----------|--------|
| **D01** | Médio | Baixo | ProjectProfile existente | **P0** | R1.2 |
| **D02** | Alto | Médio | D01 + BootstrapGate | **P0** | R1.2 |
| **D03** | Médio | Baixo | D01 (perfil populado) | **P0** | R1.2 |
| **D04** | Alto | Médio | ADR schema padronizado | **P1** | R1.3 |
| **D05** | Baixo | Baixo | StackDetector existente | **P1** | R1.3 |

**Critério de priorização:** Dores P0 afetam o ciclo inteiro de desenvolvimento (toda task, toda sprint). Dores P1 afetam cenários específicos.

---

## 4. Matriz de Dependências

```
D01 (cache perfil) ──────────────┐
                                  ├── D03 (injeção contexto) ─── R1.2
D02 (validação docs vs código) ───┘
                                       ┌── D04 (rastreio decisões) ─── R1.3
ProjectAdapter (existente) ────────────┤
                                       └── D05 (stack validation) ──── R1.3
```

---

## 5. Recomendação Final

**Contratar R1.2 com as 3 US de prioridade P0**, que atacam diretamente as dores de maior frequência e impacto. Protótipo funcional em < 10 min (setup zero validado). Adiar D04 e D05 para R1.3, pois:

1. D04 exige padronização de ADRs que ainda não foi iniciada
2. D05 tem solução parcial (StackDetector já existe) — o ganho incremental de expandi-lo agora é menor que o custo
3. As 3 P0 juntas formam um MVP coerente: **descobrir → validar → injetar** (ciclo fechado)

Próximo passo: Convocar Tríade para validação do parecer, converter US abaixo em tarefas no board.
