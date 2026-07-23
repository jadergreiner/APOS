# Discovery — Entrevista Tech Lead (Simulada)

**Data:** 2026-07-22
**Entrevistado:** Jader (Tech Lead Meu PDI — roleplay)
**Perfil:** Tech Lead solo, startup early-stage, stack 100% AWS serverless

---

## Perfil do Projeto

| Aspecto | Detalhe |
|---------|---------|
| Time | 1 (CEO + PM + Tech Lead + Dev) |
| Stack | FastAPI + Lambda + DynamoDB single-table + Cognito + S3/CloudFront |
| Tamanho | ~3.400 arquivos .py, ~50 SDDs, ~130 testes |
| Ambientes | dev / hom / prod (serverless) |
| Maturidade | Pré-product-market fit, validação ativa |

---

## Dores Validadas

| ID | Dor | Severidade | Evidência |
|----|-----|-----------|-----------|
| D01 | Contexto perdido entre sprints — 20-30min para retomar | 🔴 Alta | Relato direto |
| D02 | Documentação desalinha do código em dias sem detecção | 🔴 Alta | ADR-009, _validate_schema stub |
| D03 | Contexto repetido manualmente em toda task de IA | 🔴 Alta | 3-5 parágrafos por delegacao |
| D04 | Rastro de decisões espalhado em 20+ documentos | 🟡 Média | OAuth state em 4 referências |
| D05 | Stack assumptions erradas por agentes (ex: Redis, PostgreSQL) | 🟡 Média | SDD-0006, SDD-0072 |

## Proposta de Valor Validada

| Hipótese | Resultado |
|----------|-----------|
| "Descoberta automática de estrutura do projeto é útil" | ✅ Sim — reduziria 50% overhead |
| "Validação código vs documentação" | ✅ Sim — desde que zero falsos positivos |
| "Setup zero é condição sine qua non" | ✅ Validado |
| "Rastreamento de decisão (código → ADR → SDD)" | ✅ Desejo explícito |

## Barreiras Identificadas

- Setup complexo → não adotado
- Falsos positivos nas primeiras execuções → abandonado
- Primeiro impacto precisa ser imediato e óbvio (<10 min)

## Próximos Passos

- [ ] Convocar Tríade para consolidar achados
- [ ] Gerar backlog com User Stories
- [ ] Priorizar itens para R1.3
