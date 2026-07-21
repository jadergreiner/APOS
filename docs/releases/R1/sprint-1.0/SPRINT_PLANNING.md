# Sprint Planning — R1-sprint-1.0

**Data:** 2026-07-21
**Duracao:** 60min
**Participantes:** Jader

---

## 🎯 Sprint Goal

> Criar o ProjectAdapter — modulo que descobre o contexto do projeto hospedeiro e configura APOS para servi-lo

---

## 🎯 Alinhamento com OKRs

- R1-KR1: ProjectAdapter.discover() analisa repositorio e extrai stack, dominio, estrutura
- R1-KR2: Bootstrap Gate 2.0 guia projeto na definicao de fundacoes
- R1-KR3: Ontologia adaptada ao vocabulario do projeto

Este sprint implementa o core do R1 (ProjectAdapter). E o primeiro sprint pos-ponto-de-inflexao: APOS para de se autogerir e comeca a servir projetos.

---

## 📖 User Stories

### US-001: Descoberta automatica de contexto

**Descricao:** Como desenvolvedor, quero rodar ProjectAdapter.discover() no meu repositorio para que APOS entenda minha stack, dominio e estrutura automaticamente

**Prioridade:** P0

**Criterios de Aceitacao:**
- [ ] Detecta pyproject.toml, package.json, CLAUDE.md
- [ ] Extrai nome, descricao, stack (Python/Node/Go)
- [ ] Identifica framework (FastAPI/Django/Next)
- [ ] Detecta docs/ tests/ src/ structure

### US-002: Init guiado por contexto

**Descricao:** Como desenvolvedor, quero rodar apos init e receber perguntas adaptadas ao meu dominio, nao perguntas genericas de PM

**Prioridade:** P0

**Criterios de Aceitacao:**
- [ ] Perguntas adaptadas ao dominio (educacao, saude, fintech)
- [ ] Sugestoes de entidades baseadas no contexto
- [ ] Fallback para template generico se dominio desconhecido

### US-003: Ontologia adaptada ao projeto

**Descricao:** Como desenvolvedor, quero que APOS use os termos do MEU projeto (ex: Aluno, Curso, Mentoria) em vez de termos genericos (Task, Feature)

**Prioridade:** P1

**Criterios de Aceitacao:**
- [ ] Mapper Persona→Aluno, Task→Atividade configurado
- [ ] Mapper reverso para reports (Aluno→Persona)
- [ ] Plugavel: projetos podem customizar mapeamentos

---

## 📋 Tasks Planejadas

| ID | Titulo | Estimativa | Story |
|----|--------|-----------|-------|
| R1.1 | ProjectAdapter core — descoberta | 3.0d | - |
| R1.2 | Bootstrap Gate 2.0 — init guiado | 3.0d | - |
| R1.3 | Domain Ontology Adapter — mapper | 2.0d | - |

**Total:** 8.0d | **Velocity target:** 3.0d

---

## 🔗 Mapa de Dependencias

- `R1.1` → `R1.2`: Gate 2.0 depende do contexto descoberto pelo ProjectAdapter
- `R1.1` → `R1.3`: Ontology Adapter usa contexto do ProjectAdapter

---

## 🚨 Riscos

| Risco | Prob | Impacto | Mitigacao |
|-------|------|---------|-----------|
| Projetos podem ter estruturas muito diferentes — discover() pode falhar | Media | Alto | Detectores modulares com fallback generico |
| Ontologia generica do APOS pode nao se adaptar bem a dominios muito especificos | Baixa | Medio | Mapper configurável, documentar limites |

---

## 👥 Entrevistas com Stakeholders

_[Entrevistar stakeholders para validar escopo]_


---

## 📊 Metricas da Sprint

| Metrica | Alvo | Descricao |
|---------|------|-----------|
| ProjectAdapter | discover() funcional | Analisa repositorio e extrai contexto |
| Bootstrap Gate | init guiado por contexto | Perguntas adaptadas ao dominio |
| Ontology Adapter | mapper funcional | Traduz ontologia generica para projeto |

---

## 🔄 Acoes da Retro Anterior

- Sprint Planning + Jira sync automatico — Status: ✅ Concluido — Dono: Hermes
- User Stories no Sprint Planning — Status: ✅ Concluido — Dono: Hermes
- Retro Actions Tracker mantido — Status: ✅ Concluido — Dono: Hermes

---

**Sprint Planning criado:** 2026-07-21

