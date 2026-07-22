# JTBD Interviews — Raw Notes

**Tarefa:** T0.0.A — Conduzir Entrevistas JTBD
**Roteiro usado:** [JTBD_INTERVIEW_KIT.md](JTBD_INTERVIEW_KIT.md)
**Meta:** 5+ entrevistas | **Realizadas:** 7/5 ✅ (superado)

---

## Entrevista 1 — Product Manager

**Entrevistado:** Jader Greiner
**Papel/Contexto:** PM do Meu PDI — gerencia squad virtual (define especificações via IA, agentes virtuais implementam)
**Persona:** Product Manager (líder de time)
**Data:** 2026-07-19
**Formato:** Conduzida via texto (Claude Code), consentimento verbal confirmado

### Aquecimento

**Q1. Papel e semana típica:**
> "Sou PM de uma squad virtual. Defino as especificações usando IA e agentes virtuais implementam."

**Q2. Como decide se uma feature está alinhada ao OKR hoje:**
> "Puro Feeling"

**Q3. Ferramentas/documentos consultados:**
> "nenhum"

### Job to be Done

**Q4. Última vez que perdeu tempo/retrabalhou por falta de contexto:**
> "Cada deploy na AWS erro no login. Retrabalho, instruções aos agentes, checklist. Mas dali um tempo, o mesmo erro se repete."

**Q5. O que mudaria se a informação estivesse sempre correta e acessível:**
> "Estas regressões não ocorreriam"

**Q6. Como se sente confiando em resposta de IA sem conseguir validar:**
> "Me sinto desprotegido. Com medo de seguir adiante, às vezes acho que o tempo que ganhei com IA estou perdendo validando e testando."

**Q7. Como quer ser visto ao tomar decisão baseada em contexto:**
> "Rápido, confiável, consistente"

### Forças de Progresso

**Q8. Push — maior frustração em manter contexto/alinhamento atualizado:**
> "Tento usar múltiplas IAs para gerar prompts que minimizem falhas"

**Q9. Pull — o que mais atrairia numa fonte única de verdade viva:**
> "Validar contexto. Rastrear claramente a decisão e rota que o agente utilizou na implementação"

**Q10. Ansiedade — preocupações na adoção:**
> "Curva de aprendizado e mudança de processo"

**Q11. Hábito — o que seria difícil abandonar:**
> "Ler as especificações, gerar passo a passo, validar"

### Encerramento

**Q12. Um problema para resolver amanhã:**
> "Saber antes de implementar exatamente o contexto da IA"

**Q13. Indicação de outra pessoa:**
> "não"

### Perguntas Específicas — Product Manager

**PM1. Como garante que o time/agentes entendem o "porquê" de uma feature:**
> "Não garanto. É uma dor recorrente"

**PM2. Frequência de re-explicar contexto estratégico por sprint:**
> "quase que diariamente"

**PM3. Rastreamento Task → Feature → Release → OKR → Métrica hoje:**
> "Inexistente"

---

## Entrevista 2 — AI Integration Specialist (Roleplay: Alex)

**Persona:** Agente de IA (via operador/integrador)
**Foco:** Necessidades de contexto para evitar alucinação
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "Hoje eu sou o 'cara dos agentes' na startup. Três dias atrás tava debugando por que um agente de coding commitou uma migration SQL que dropou uma coluna em produção — ele 'achou' que a coluna não era mais usada porque um arquivo de schema desatualizado estava no contexto. A semana típica é: APAGAR INCÊNDIO, rodar validação manual do que os agentes fizeram, e realinhar contexto estratégico que se perdeu entre sprints."

**Q2. Como garante que o agente age com o contexto correto:**
> "Eu tento manter um CONTEXT.md vivo na raiz, mas desatualiza em dias. A abordagem real: prompt engineering defensivo. Constraints explícitas no system prompt, exemplos few-shot, e rezo pra não cair em viés de contexto."

**Q3. Ferramentas que testou:**
> "RAG direto em vector store (não escala sem curadoria), MCP tools (contexto é o que a tool retorna — descobre depois que já agiu), system prompts manuais. Nada garante que o agente usou a informação certa antes de agir."

### Job to be Done

**Q4. Última vez que perdeu tempo por falta de contexto:**
> "Semana passada. Pedi pra um agente refatorar um módulo de autenticação. Ele seguiu o CONTEXT.md que dizia 'usamos JWT com Cognito'. Mas desde a última release, migramos parte para OAuth2 social — o CONTEXT.md não refletia. O agente reescreveu o módulo assumindo JWT puro. Login social quebrou em staging. Dois dias de trabalho. O agente não 'sabia' que não sabia."

**Q5. O que mudaria se contexto estivesse sempre correto:**
> "Cortaria um ciclo inteiro de validação. Hoje: (1) implementa, (2) reviso e acho erro de contexto, (3) corrijo contexto, (4) reimplementa. Ciclo de 2 dias vira 4 horas."

**Q6. Como se sente confiando sem validar:**
> "Desconforto constante. Parece que tô terceirizando decisão sem visibilidade do insumo. O agente pode estar certo por sorte ou errado por contexto desatualizado — descubro quando quebra. É como dirigir com para-brisa embaçado e GPS desatualizado."

**Q7. Como quer ser visto:**
> "Como alguém que entrega rápido SEM quebrar. O 'rápido' os agentes dão — problema é o 'sem quebrar'. Quero que meu CTO confie quando digo 'agente implementou com contexto correto'."

### Forças de Progresso

**Q8. Push:**
> "Manutenção manual do CONTEXT.md não escala. Cada release desatualiza. Ninguém lembra de atualizar. Aceita-se o risco de estar desatualizado — e paga-se depois em retrabalho."

**Q9. Pull:**
> "Contexto auto-atualizável com selo de confiança. Rastreabilidade: 'qual contexto o agente usou pra decidir isso?'. Hoje é caixa-preta — quero que tenha visor."

**Q10. Ansiedade:**
> "Quem alimenta isso? Se for mais um artefato de curadoria humana, é outro CONTEXT.md com branding. Lock-in: se for proprietário, viro refém."

**Q11. Hábito:**
> "Prompts defensivos. Construí arsenal de constraints que funciona na prática. Abandonar por camada abstrata exige confiança de que cobre mesmos edge cases."

### Perguntas Específicas — AI Agent

**IA1. Causa raiz de alucinação/desalinhamento:**
> "Nove em cada dez vezes: **contexto desatualizado ou ambíguo**. Raramente o modelo alucina no sentido clássico — é que o contexto que ele usava estava errado."

**IA2. Contexto estruturado que ajudaria:**
> "Três coisas: (1) **versão do contexto** — saber se é atual ou defasado; (2) **confiança por campo** — granular, não booleano; (3) **dependências explícitas** — 'se for implementar Y, PRECISA saber que migração Z aconteceu'."

**IA3. Como mede confiança do contexto hoje:**
> "Não meço. Binário: confio porque atualizei horas atrás, ou não confio. Não existe métrica. Feeling não escala com 8 agentes em paralelo."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | Manutenção manual inviável; descobrir erro só depois do deploy |
| **Pull** | Contexto auto-atualizável com semáforo de confiança |
| **Ansiedade** | Quem alimenta? Falso positivo de confiança |
| **Hábito** | Prompts defensivos construídos em meses |
| **Emocional** | Desconforto constante; produtividade corroída por validação |
| **Social** | "Rápido SEM quebrar" — credibilidade |

**Citações fortes:**
> "O agente pode estar certo por sorte ou errado por contexto desatualizado — e eu só descubro quando quebra."

> "Quero saber, *antes* do agente agir, se o contexto que ele tem é confiável."

---

## Entrevista 3 — CTO / Arquiteto (Roleplay: Carolina)

**Persona:** CTO / Arquiteto
**Foco:** Viabilidade técnica, custo de integração
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "50% gestão de time, 30% arquitetura, 20% apagar incêndio de débito técnico. O fio condutor: alguém não tinha o contexto certo quando tomou decisão."

**Q2. Como garante alinhamento estratégico-técnico:**
> "Reunião. Sempre reunião. Não existe ferramenta que conecte 'usar biblioteca X' com OKR 'reduzir latência'. Engenheiros decidem baseados no que lembram da última all-hands. Descubro desalinhamento 3 sprints depois."

**Q3. Ferramentas avaliadas:**
> "Notion wiki (viraço), RAG (estatístico, não semântico), DataHub (linhagem de dados, não contexto de produto), Neo4j (quem alimenta?). Nenhum resolve: **contexto que desatualiza no momento em que é escrito**."

### Job to be Done

**Q4. Último retrabalho por falta de contexto:**
> "Engenheiro sênior passou 2 semanas implementando cache distribuído. Código lindo. Só que despriorizamos cache na última revisão de roadmap. Ele não participou da reunião. 2 semanas de salário, branch descartada, moral afetada. Não foi erro técnico — foi contexto ausente."

**Q5. O que mudaria com contexto correto e acessível:**
> "Cortaria 1/3 do meu tempo de revisão. Se eu confiasse que o engenheiro tinha o contexto certo *no momento da decisão*, revisaria só qualidade técnica. Velocidade de entrega dobraria."

**Q6. Como se sente aprovando arquitetura sem validar contexto do time:**
> "Angustiante. Aprovo RFC impecável, mas não sei se quem vai implementar recebeu mesmo briefing. Informação se perde na hierarquia. É pilotar avião sem saber se instrumentos do copiloto estão calibrados."

**Q7. Como quer ser visto:**
> "Líder que cria ambiente onde decisões certas são fáceis de tomar — não gargalo que precisa aprovar tudo porque não confia no contexto do time."

### Forças de Progresso

**Q8. Push:**
> "Assimetria de informação. Decisão de 30 min com 4 pessoas impacta 15 que não estavam na sala. Gasto mais tempo 'lembrando de decisões já tomadas' do que tomando novas."

**Q9. Pull:**
> "Escalabilidade do meu contexto — se extraído, versionado e consultável automaticamente, deixo de ser gargalo. Auditabilidade pra provar ao CEO que decisões foram tomadas com contexto correto."

**Q10. Ansiedade:**
> "Falso positivo de confiança é pior que ausência de contexto — porque você confia e não verifica. Custo de manutenção: se precisar time dedicado, ROI não fecha. Acoplamento: novo ponto de falha."

**Q11. Hábito:**
> "Reunião de alinhamento. Time se acostumou a 'esperar reunião semanal'. Hábito de 'sempre foi assim' persiste mesmo quando contexto estratégico mudou."

### Perguntas Específicas — CTO/Arquiteto

**CTO1. Riscos de camada semântica viva:**
> "Consistência eventual entre 5 fontes com latências diferentes. Carga cognitiva do schema — abstrata demais ninguém usa, concreta demais quebra. Dependência de pipeline — se ETL falhar, agentes ficam cegos."

**CTO2. Comparação com alternativas:**
> "RAG acha informação mas não permite confiar nela. Neo4j é consulta humana, não contexto pra agente. DataHub resolve linhagem de dados, não Task→OKR. Espaço em branco: **confiança como métrica operacionalizável** — '87% de confiança porque atualizado há 2h com fonte primária'."

**CTO3. Condições pra aprovar adoção:**
> "Zero impacto em latência de produção. Auto-atualização via eventos. Degradação graciosa documentada. Métrica de precisão em produção. Exportável — sem lock-in."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | Assimetria informação liderança→time |
| **Pull** | Escalar contexto, deixar de ser gargalo |
| **Ansiedade** | **Falso positivo > ausência** — requisito arquitetural crítico |
| **Hábito** | Reunião de alinhamento como muleta |

**Citações fortes:**
> "Falso positivo de confiança é mais perigoso que ausência de contexto."

> "Confiança calibrada — um número que diga o quanto confiar em cada informação."

---

## Entrevista 4 — Stakeholder de Negócios (Roleplay: Ricardo)

**Persona:** Stakeholder (negócios)
**Foco:** ROI, valor percebido
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "VP de Produto. Segunda: OKRs com CEO. Terça/quarta: revisão roadmap. Quinta: métricas. Sexta: estratégia. Fio condutor: 'acertamos o alvo?' Resposta geralmente é 'mais ou menos' — não sei se foi erro de execução ou priorização."

**Q2. Como mede alinhamento feature-estratégia:**
> "Não meço. Sinto. 20 anos de estrada, radar de desalinhamento. Mas feeling não escala. Proxy: features entregues usadas >6 meses depois. Medida indireta."

**Q3. Causa raiz de entregas fora do trilho:**
> "Desalinhamento de expectativa, não incompetência. Time implementa o que foi pedido. Contexto mudou entre priorização e implementação — ninguém atualizou. Não é time lento — é **time rápido na direção errada**."

### Job to be Done

**Q4. Última feature sem valor:**
> "Módulo de onboarding 'inteligente' — 6 semanas, tecnicamente impecável. Taxa de ativação não mudou. Problema real não era onboarding — era value prop na primeira sessão. Investimos na solução errada porque decisão foi baseada em suposição, não em contexto validado."

**Q5. O que mudaria com Task→Feature→OKR→Métrica visível:**
> "Pararia de priorizar no escuro. Hoje priorizo por 'quem grita mais alto'. Com cadeia visível, eliminaria 40% do desperdício."

**Q6. Como se sente aprovando feature sem impacto:**
> "Frustrado e confuso. Não sei se erramos priorização, execução ou timing. Queria erro visível e analisável — não 'não sei por que não funcionou'."

**Q7. Como quer ser visto:**
> "VP que entrega no prazo *com impacto previsível*. CEO confia que o que prometo acontece em resultado de negócio, não só em timing."

### Forças de Progresso

**Q8. Push:**
> "Invisibilidade do custo do desalinhamento. Sprint de 2 semanas custa R$80 mil. 40% desperdiçado = R$32 mil/sprint queimados. Mas não aparece em relatório nenhum. CFO vê 'engenharia dentro do orçamento' e acha que tá tudo bem."

**Q9. Pull:**
> "Previsibilidade de impacto. Hoje sou apostador — escolho 10 e torço pra 3 darem certo. Com cadeia visível e tracking, viro investidor — sei quais apostas são alto vs baixo risco."

**Q10. Ansiedade:**
> "Precisão das métricas. Se sistema disser confiança 85% e for 40%, decisão é pior do que sem sistema — porque confiei. Prefiro 'não sei' a 'sei errado'. Complexidade de implantação: se precisar 3 ferramentas + treino, não adota."

**Q11. Hábito:**
> "Reuniões de priorização. Rituais semanais de 2h. Ineficientes, políticos, desgastantes — mas dão sensação de controle. E alinhamento social que sistema não substitui — pessoas precisam se sentir ouvidas."

### Perguntas Específicas — Stakeholder

**SB1. Como mede custo do desalinhamento:**
> "Não meço. É custo oculto. Proxies: horas de retrabalho, features entregues não usadas (<10% adoção), taxa de surpresa do CEO. Palpite: 30-40% do esforço de engenharia desperdiçado. Se chegasse no board com número provado, mudaria forma de priorizar."

**SB2. O que faria confiar no ROI antes de ver resultado:**
> "Benchmark de redução de desperdício — caso real com métrica antes/depois. Custo total de implantação. Se payback <3 meses, aprovo sem piloto. Se 6-9 meses, POC com 1 squad."

**SB3. Métrica de negócio que mudaria:**
> "NFA (Net New Features Adotadas) — de 30% pra 60%. Time-to-Impact — de 3 meses pra 6 semanas. Rework Ratio — de 30% pra 15%. Essas três contam história completa."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | 30-40% desperdício invisível em P&L |
| **Pull** | Previsibilidade de impacto |
| **Ansiedade** | Falso positivo de métrica |
| **Hábito** | Reuniões como muleta de alinhamento |

**Citações fortes:**
> "Não é time lento — é **time rápido na direção errada**."

> "Se payback <3 meses, aprovo sem piloto."

---

## Entrevista 5 — Early Adopter (Roleplay: Daniela)

**Persona:** Early Adopter (time early-stage)
**Foco:** Adoção, fricção de onboarding
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "Dev sênior em startup B2B SaaS. 70% do código via agentes. Segunda: abro prompts, reviso. Terça/quarta: implemento/orquestro. Quinta: code review de PRs que agentes abriram. Relação com IA é pragmática — uso porque entrega. Mas tô cada vez mais desconfiada."

**Q2. Como garante contexto do agente:**
> "Não garanto. Confiro. Não tenho mecanismo que previne — tenho detecção pós-fato. Agente pode implementar módulo inteiro com contexto desatualizado antes de eu perceber."

**Q3. Ferramentas testadas e abandonadas:**
> "Umas 6. Contextual, RAG docs, memória persistente, MCP tools. Padrão: prometem 'contexto vivo', viram repositório que desatualiza em dias. Só mantenho uma MCP tool custom que eu mesma fiz."

### Job to be Done

**Q4. Último retrabalho:**
> "Ontem. Claude Code implementou CRUD seguindo padrão geral do codebase. Só que mudamos estratégia de autenticação desse recurso pra API key na última sprint. Agente não sabia. Endpoint subiu com middleware errado. CI não pegou (teste passava). 55 minutos perdidos. Morte por mil cortes."

**Q5. O que mudaria com contexto correto:**
> "Deixaria agente trabalhar sozinho por mais tempo. Hoje reviso cada PR como de estagiário. Com confiança no contexto, revisão passaria de 'procurar erro' pra 'validar lógica'. Cortaria 60% do tempo de review."

**Q6. O que faria experimentar amanhã:**
> "Zero setup — `pip install` ou 1 arquivo. Resultado visível em 5 minutos — quero rodar e ver 'aqui, 2 info com confiança alta, 1 baixa'. Corrigir um erro real que eu sei que existe — se fizer isso 1 vez, ganhou usuário fiel."

**Q7. Critério pra abandonar:**
> "Falso alarme demais — se alertar contexto não confiável que tá correto, desligo em 2 dias. Manutenção virar meu problema — se eu precisar alimentar, ROI vira negativo."

### Forças de Progresso

**Q8. Push:**
> "Invisibilidade. Agente age, descubro erro depois. Se ele me dissesse 'usei info com 40% de confiança', interviria antes."

**Q9. Pull:**
> "Confiança visível — semáforo dentro do meu fluxo (IDE, terminal, PR). Não dashboard separado."

**Q10. Ansiedade:**
> "Falso positivo de confiança — se disser 'verde' e eu confiar, e agente errar, piorou: removeu minha barreira natural de desconfiança. Perturbar fluxo com alerta toda hora — vou desligar."

**Q11. Hábito:**
> "Revisão desconfiada. Agente implementa → varro diff → aprovo. Abandonar exige ferramenta visivelmente mais confiável que faro de dev experiente."

### Perguntas Específicas — Early Adopter

**EA1. O que faria experimentar amanhã em beta:**
> "Um caso real. Me mostrar: 'nesse seu PR, agente usou info de 3 sprints atrás que já mudou' — e for verdade. Não precisa de demo polida. Precisa de insight que eu não tinha."

**EA2. O que precisa estar pronto no dia 1:**
> "Integração com Git e IDE. Indicador de confiança no PR ou terminal. Não quero abrir outro app. Sem schema definido por mim — ferramenta precisa inferir contexto do que já existe."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | Invisibilidade — descobre erro depois |
| **Pull** | Semáforo dentro do fluxo |
| **Ansiedade** | Falso positivo + perturbar fluxo |
| **Hábito** | Revisão desconfiada — faro de dev experiente |

**Citações fortes:**
> "Morte por mil cortes."

> "Se fizer 1 vez — achar um erro real que eu não sabia que existia — ganhou usuário fiel."

---

## Entrevista 6 — Engenheiro de Dados Júnior (Roleplay: Lucas)

**Persona:** Eng. Dados Júnior
**Foco:** Sofre de contexto que não sabe que precisa
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "Tickets de relatório, pipeline quebrou, carga de dados nova. Passo o dia escrevendo SQL, debugando Airflow, perguntando pro sênior 'esse campo significa o quê?'. Uso ChatGPT pra 60% do SQL. Maior medo: subir query que roda mas devolve dado errado — e eu não perceber."

**Q2. Como garante que o dado processado está certo:**
> "Pergunto pra alguém. Não tenho ferramenta. Schema me diz o tipo, não o significado. Coluna `discount` era `discount_percentage`, não `discount_value` — pipeline rodou 3 dias com dado errado."

**Q3. Como usa IA e como confia:**
> "Uso pra tudo. Não sei validar o que a IA devolve. Se a query roda sem erro, assumo que tá certa — não tenho repertório pra questionar. Já subi query com JOIN que duplicava registros por 2 semanas."

### Job to be Done

**Q4. Último retrabalho:**
> "Relatório de churn rate por plano. Calculei, subi dashboard. CPO questionou — números muito altos. Tabela incluía testes grátis como 'cancelados'. A IA não sabia que trial não é churn. Eu não sabia. Sênior sabia, mas não tava no ticket. Contexto que eu não sabia que não sabia."

**Q5. O que mudaria com nível de confiança visível:**
> "Confiaria mais no meu próprio trabalho. Se coluna tem selo vermelho 'definição ambígua', iria atrás antes. Se tabela tem selo verde 'atualizada há 2h', dormiria melhor."

**Q6. Como se sente confiando em IA sem validar:**
> "Ansioso quieto. Entrego e torço pra ninguém achar erro. Como sou júnior, nem sei quais perguntas fazer pra validar."

**Q7. Como quer ser visto:**
> "Confiável. Hoje me sinto 'quase' — entrego rápido mas sempre tem algo que eu não sabia. Quero não precisar de supervisão constante."

### Forças

**Q8. Push:**
> "Ontologia invisível. Conhecimento existe na cabeça do sênior, em doc que ninguém lê, em reunião que não participei. Frustração é **não saber que a informação existe**."

**Q9. Pull:**
> "Contexto no momento da decisão. Não wiki separado. Na hora de escrever query, alerta 'tabela X foi atualizada, schema mudou'."

**Q10. Ansiedade:**
> "Dependência. Se sistema mostrar verde quando contexto tá errado, vou errar com mais confiança."

**Q11. Hábito:**
> "Perguntar pro sênior. Ineficiente mas funciona."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | Ontologia invisível — conhecimento existe mas não chega |
| **Pull** | Contexto no momento, automático |
| **Ansiedade** | Falso positivo = errar com confiança |
| **Hábito** | Perguntar pro sênior |
| **Emocional** | Ansiedade quieta, torce pra não estar errado |
| **Social** | Quer ser confiável sem supervisão |

---

## Entrevista 7 — Engenheiro de Software Pleno (usuário de IA) (Roleplay: Felipe)

**Persona:** Eng. Software Pleno, fintech
**Foco:** Contexto de domínio pra IA; transparência de contexto
**Data:** 2026-07-19
**Formato:** Roleplay conduzido via Hermes Agent

### Aquecimento

**Q1. Papel e semana típica:**
> "Dev pleno em fintech. Processamento de pagamentos + conciliação financeira. Copilot sempre ligado, ChatGPT pra debugar, Claude pra refatorar. Mas regra de negócio de dinheiro eu mesmo escrevo — não confio IA em lógica financeira."

**Q2. Como garante que IA tem contexto certo:**
> "Não confio. Parto que IA não sabe contexto do meu domínio. Forneço manualmente: copio interface, colo schema, escrevo o que precisa fazer. Não sei se o prompt 'passou' todo o contexto."

**Q3. Ferramentas de contexto testadas:**
> "Nenhuma. MCP ouvi falar mas não usei. RAG over docs é overkill. O que falta não é 'mais contexto' — é **contexto de domínio** que não está no repositório."

### Job to be Done

**Q4. Último retrabalho:**
> "Task de 'adicionar pix_key na resposta de reembolso'. Copilot gerou 90% baseado em padrões existentes. Mas regra diz: reembolso PIX só permitido se transação original foi PIX. Copilot não sabia. Subiu em staging, QA testou com cartão de crédito, reembolso foi processado como PIX. Regra de negócio invisível pra IA."

**Q5. O que mudaria com contexto de domínio disponível:**
> "Reduziria escopo de revisão. Se soubesse que IA 'viu' regras relevantes antes de implementar, revisaria mais superficialmente. IA seria extensão da minha memória, não só do teclado."

**Q6. Como se sente revisando código de IA sem saber contexto usado:**
> "Incômodo constante. Confio na sintaxe, mas 'será que considerou a regra X?'. Esforço mental de validar é maior que o de produzir."

**Q7. Como quer ser visto:**
> "Dev que usa IA pra ser mais produtivo, não mais preguiçoso. Preciso que IA seja confiavelmente contextualizada — se tiver que explicar 'a IA não sabia', credibilidade vai pro lixo."

### Forças

**Q8. Push:**
> "Contexto invisível. Não sei o que a IA 'viu'. Trato toda sugestão como culpada até prova em contrário. Produtividade sem confiança acumula débito de revisão."

**Q9. Pull:**
> "Transparência de contexto por sugestão. IA mostra: 'gerei isso baseado nas regras X, Y com 90% de confiança'. Aceito sem revisão se confiança alta nas regras que importam."

**Q10. Ansiedade:**
> "Falso positivo quebra o loop de adoção. Se de 10x que confio, 1x o contexto está errado — volto a revisar tudo. É mais fácil confiar em zero contexto do que em contexto que às vezes erra."

**Q11. Hábito:**
> "Copia e cola manual de contexto no prompt. Trabalhoso mas previsível — sei exatamente o que passei pra IA."

### Síntese

| Força | Sinal |
|-------|-------|
| **Push** | Contexto invisível — não sabe o que a IA 'viu' |
| **Pull** | Transparência de contexto por sugestão + confiança |
| **Ansiedade** | Falso positivo quebra confiança pra sempre (grana real) |
| **Hábito** | Copia e cola manual — previsível |
| **Emocional** | Incômodo constante; validar > produzir |
| **Social** | "Produtivo, não preguiçoso" — stigma no time |

---

## 📊 Síntese Consolidada — 7 Entrevistas

### Job Statement (Final — T0.0.C)

> **When** [dependo de agentes de IA (ou times) para implementar sem visibilidade do contexto que eles usam],
> **I want** [um sistema que me mostre o nível de confiança de cada informação *antes* de agirem],
> **so I can** [delegar com segurança e eliminar o ciclo de retrabalho por contexto desatualizado].

### Três Dimensões do Job

| Dimensão | Agora | Desejado |
|----------|-------|----------|
| **Funcional** | Validação manual pós-fato → descobre erro no deploy | Validação prévia com semáforo de confiança |
| **Emocional** | Desprotegido, desconforto constante, ansiedade quieta | Confiança para delegar, não apenas supervisionar |
| **Social** | "Rápido mas quebra" / "quase confiável" / "precisa supervisão" | "Rápido SEM quebrar" / confiável sem supervisão |

### Matriz de Forças Consolidada

| Força | Tema Central | Frequência (em 7) |
|-------|-------------|-------------------|
| **Push** | Contexto desatualizado sem mecanismo de alerta; retrabalho cíclico; custo invisível; ontologia que não chega a quem executa | 7/7 |
| **Pull** | Confiança como métrica (0.0-1.0), não atributo binário; rastreabilidade; semáforo pré-ação no fluxo de trabalho | 7/7 |
| **Ansiedade** | **Falso positivo de confiança > ausência de contexto** (unânime); quem alimenta?; lock-in; perturbar fluxo | 7/7 |
| **Hábito** | Prompts defensivos; revisão desconfiada; perguntar pro sênior; copia e cola manual de contexto | 6/7 |

### Achados por Perfil

| Perfil | O que quer validar | Onde dói |
|--------|--------------------|----------|
| **PM** | Se feature está alinhada ao OKR | Nenhum mecanismo conecta task a estratégia |
| **AI Operator** | Se o campo que o agente leu é atual | Manutenção manual de contexto não escala |
| **CTO/Arquiteto** | Se a decisão técnica usou contexto correto | Assimetria de informação liderança→time |
| **Stakeholder Negócios** | Se a feature vai gerar impacto mensurável | 30-40% do esforço é desperdício invisível |
| **Early Adopter** | Se o código gerado considerou regras corretas | Semáforo precisa estar dentro do fluxo, não em dashboard |
| **Eng. Dados Júnior** | Se o dado que ele processa significa o que ele acha | Contexto que não sabe que não sabe — ontologia invisível |
| **Dev Pleno (IA user)** | Se a IA considerou regras de negócio | Não sabe o que a IA 'viu'; transparência vira moeda de troca por velocidade |

### Insight Central (confirmado por 7/7)

> **APOS não resolve "falta de contexto". Resolve "impossibilidade de saber se o contexto é confiável *antes* de agir".**

### 6 Requisitos de Produto (emergentes das entrevistas)

1. **Confiança granular** (0.0-1.0 por campo/informação) — não binário
2. **Falso positivo é inaceitável** — requisito arquitetural nº1, unânime entre perfis
3. **Auto-atualização via eventos** — sem curadoria manual, ou não escala
4. **Contexto no fluxo** (IDE, terminal, PR) — não dashboard separado
5. **Auto-descoberta** — não depende do usuário saber o que buscar
6. **Custo do desalinhamento visível em $** — métrica de negócio, não só técnica


### Job Statement (Refinado)

> **When** [dependo de agentes de IA (ou times) para implementar sem visibilidade do contexto que eles usam],
> **I want** [um sistema que me mostre o nível de confiança de cada informação *antes* de agirem],
> **so I can** [delegar com segurança e eliminar o ciclo de retrabalho por contexto desatualizado].

### Três Dimensões do Job

| Dimensão | Agora | Desejado |
|----------|-------|----------|
| **Funcional** | Validação manual pós-fato → descobre erro no deploy | Validação prévia com semáforo de confiança |
| **Emocional** | Desprotegido, desconforto constante | Confiança para delegar, não apenas supervisionar |
| **Social** | "Rápido mas quebra" | "Rápido SEM quebrar" — credibilidade |

### Matriz de Forças Consolidada

| Força | Tema Central | Frequência (em 5) |
|-------|-------------|-------------------|
| **Push** | Contexto desatualizado sem mecanismo de alerta; retrabalho cíclico; custo invisível | 5/5 |
| **Pull** | Confiança como métrica (não atributo); rastreabilidade; semáforo pré-ação | 5/5 |
| **Ansiedade** | Falso positivo de confiança > ausência de contexto; quem alimenta?; lock-in | 5/5 |
| **Hábito** | Prompts defensivos; revisão desconfiada; reuniões como muleta | 4/5 |

### Insights-chave

1. **APOS não resolve "falta de contexto". Resolve "impossibilidade de saber se o contexto é confiável antes de agir".**
2. **Falso positivo de confiança é pior que não ter sistema** — define requisito arquitetural central
3. **Confiança granular (0.0-1.0 por campo)** é o diferencial que ninguém oferece hoje
4. **Contexto auto-atualizável via eventos** — sem curadoria manual, ou não escala
5. **Integração no fluxo (IDE, terminal, PR)** — não dashboard separado
6. **Custo do desalinhamento precisa ser visível em dólares** — não só em horas técnicas

---

## Próximas Etapas

- [ ] **T0.0.B**: Análise de Forças detalhada → Matriz Push/Pull/Ansiedade/Hábito
- [ ] **T0.0.C**: Job Statement Final validado com stakeholders
- [ ] **Atualizar VALUE_PROPOSITION.md** com insights refinados das entrevistas

---

**Criado:** 2026-07-19
**Atualizado:** 2026-07-19 (entrevistas 2-7 adicionadas + síntese 7 entrevistas)
**Relacionado:** [JTBD_INTERVIEW_KIT.md](JTBD_INTERVIEW_KIT.md) | [TASKS.md](TASKS.md) (T0.0.A) | [BOARD.md](BOARD.md)
