# Plano de Ação — Retro Sprint 1.1

**Objetivo:** Medir, planejar e atuar sobre os 3 itens "Correto Mal" + 3 "Ideias de Melhoria" + 3 "Ações" da Retro.

---

## A1: Template de Artefatos de Sprint (🔴 Alta)

### O Problema
TASKS.md, BOARD.md e STATUS.md foram criados sem a seção de commit tracking. No fechamento, precisou backfill manual para o validator aceitar.

### Métrica
| Indicador | Atual | Target |
|-----------|:-----:|:------:|
| Sprints com commit tracking desde o kickoff | 0/2 | 3/3 (R1.2+) |
| Tempo de backfill pós-sprint | ~15min | 0min |

### Plano
| Passo | O quê | Responsável | Prazo |
|-------|-------|-------------|-------|
| 1 | Criar diretório `docs/releases/.templates/` com templates canônicos | Tech Lead | Antes do kickoff R1.2 |
| 2 | Template `TASKS.md` com seções: header, tasks, progress summary, **commit tracking** | Tech Lead | ↑ |
| 3 | Template `BOARD.md` com seções: header, kanban visual, colunas, **audit trail** | Tech Lead | ↑ |
| 4 | Template `STATUS.md` com seções: burndown, métricas, **commit tracking** | Tech Lead | ↑ |
| 5 | No kickoff da sprint, copiar templates → `docs/releases/R1/sprint-X.Y/` | Tech Lead | Todo kickoff |

### Atuação
```bash
# Durante o kickoff da sprint:
mkdir -p docs/releases/R1/sprint-1.2/
cp docs/releases/.templates/TASKS.md docs/releases/R1/sprint-1.2/
cp docs/releases/.templates/BOARD.md docs/releases/R1/sprint-1.2/
cp docs/releases/.templates/STATUS.md docs/releases/R1/sprint-1.2/
```

---

## A2: STATUS.md Automático no validate-sprint (🟡 Média)

### O Problema
STATUS.md é o artefato mais esquecido. O validator `apos validate-sprint` aponta a falta mas não cria o arquivo.

### Métrica
| Indicador | Atual | Target |
|-----------|:-----:|:------:|
| Sprints com STATUS.md no fechamento | 1/2 | 3/3 |
| Sprints que precisaram criação manual | 2/2 | 0/3 |

### Plano
| Passo | O quê | Responsável | Prazo |
|-------|-------|-------------|-------|
| 1 | Adicionar flag `--create-status` no `apos validate-sprint` | Tech Lead | Antes R1.2 |
| 2 | Quando STATUS.md não existir, auto-gerar com dados do TASKS.md | Tech Lead | ↑ |
| 3 | Template mínimo: burndown, métricas, commit tracking | Tech Lead | ↑ |
| 4 | CI step: `apos validate-sprint --create-status --sprint-root ...` | Tech Lead | ↑ |

### Atuação
```bash
# Comando que cria STATUS.md se ausente:
python3 -m apos validate-sprint --sprint-root docs/releases/R1/sprint-1.2/ --create-status
```

---

## A3: Entrevista Real Stakeholder R1.3 (🟡 Média)

### O Problema
R0-AC04 foi fechado com roleplay supervisionado. As respostas eram genuínas (o próprio Jader é o Tech Lead), mas não substitui uma entrevista com stakeholder externo. Risco de viés de confirmação.

### Métrica
| Indicador | Atual | Target |
|-----------|:-----:|:------:|
| Entrevistas reais com stakeholders | 0 | 1 (até R1.3) |
| Hipotese de valor validada externamente | 0/5 | 3/5 |

### Plano
| Passo | O quê | Responsável | Prazo |
|-------|-------|-------------|-------|
| 1 | Identificar 3 Tech Leads na rede (LinkedIn, comunidades) | PO | R1.2 |
| 2 | Aplicar roteiro JTBD (já preparado em `docs/discovery/ENTREVISTA_TECH_LEAD.md`) | PO | R1.3 |
| 3 | Comparar findings roleplay vs real → ajustar backlog | PO | R1.3 |
| 4 | Documentar divergências | PO | R1.3 |

### Atuação
```markdown
# Pipeline de recrutamento:
1. LinkedIn → search "Tech Lead" + "startup" + "São Paulo"
2. Mensagem: "Estou validando uma ferramenta de contexto semântico para agentes de IA.
   Topa 30min para uma conversa?"
3. Se aceitar → agendar, aplicar roteiro, documentar
```

---

## Acompanhamento

| Ação | Prioridade | Esforço | Sprint | Owner | Checkpoint |
|------|:----------:|:-------:|:------:|-------|------------|
| A1 — Template artefatos | 🔴 Alta | 1h | R1.2 (pré-kickoff) | Tech Lead | Kickoff R1.2 |
| A2 — STATUS.md auto | 🟡 Média | 2h | R1.2 | Tech Lead | Fim R1.2 |
| A3 — Entrevista real | 🟡 Média | 2h (recrutamento) | R1.3 | PO | Fim R1.3 |
