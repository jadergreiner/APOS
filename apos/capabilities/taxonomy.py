"""
APOS Capability Taxonomy — Hierarquia de Classificação de Capabilities (Camada 3.6)

Define o sistema de classificação hierárquica de 4 níveis:
  Domínio (N1) → Capacidade (N2) → Habilidade (N3) → Ação (N4)

Inclui categorias (Core, Suporte, Governança), níveis de maturidade
(L0–L3), e critérios de classificação (D01–D05, C01–C06, etc.).

Conforme CAPABILITY_TAXONOMY.md — Sprint 0.6, Tarefa T0.6.2.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────


class Categoria(str, Enum):
    """Categoria transversal que corta os domínios.

    - CORE: Essencial para o funcionamento do APOS.
    - SUPORTE: Auxiliares que otimizam a operação.
    - GOVERNANCA: Auditoria, qualidade e conformidade.
    """

    CORE = "core"
    SUPORTE = "suporte"
    GOVERNANCA = "governanca"


class Maturidade(str, Enum):
    """Níveis de maturidade de uma capacidade.

    - L0: Conceitual — documentada como conceito, sem implementação.
    - L1: Estruturado — com estrutura formal (atributos, assinaturas).
    - L2: Implementado — implementação funcional em código.
    - L3: Otimizado — métricas de performance e melhorias contínuas.
    """

    L0_CONCEITUAL = "L0_conceitual"
    L1_ESTRUTURADO = "L1_estruturado"
    L2_IMPLEMENTADO = "L2_implementado"
    L3_OTIMIZADO = "L3_otimizado"

    @property
    def level(self) -> int:
        """Retorna o nível numérico (0, 1, 2, 3)."""
        return int(self.value[1])

    def __ge__(self, other: Maturidade) -> bool:
        if not isinstance(other, Maturidade):
            return NotImplemented
        return self.level >= other.level

    def __le__(self, other: Maturidade) -> bool:
        if not isinstance(other, Maturidade):
            return NotImplemented
        return self.level <= other.level

    def __gt__(self, other: Maturidade) -> bool:
        if not isinstance(other, Maturidade):
            return NotImplemented
        return self.level > other.level

    def __lt__(self, other: Maturidade) -> bool:
        if not isinstance(other, Maturidade):
            return NotImplemented
        return self.level < other.level


# ──────────────────────────────────────────────
# Dataclasses dos 4 Níveis
# ──────────────────────────────────────────────


@dataclass
class Parametro:
    """Parâmetro de uma ação."""

    nome: str
    tipo: str  # tipo como string (ex.: "str", "int", "list[dict]")
    descricao: str = ""
    obrigatorio: bool = True
    default: Any = None


@dataclass
class Acao:
    """Nível 4 — Operação elementar atômica e indivisível.

    Mapeia 1:1 para uma chamada de API, método de classe ou função.
    """

    id: str  # ex.: "KG.traverse"
    nome: str  # ex.: "KnowledgeGraph.traverse()"
    chamada: str  # ex.: "KG.traverse(urn, depth)"
    descricao: str
    habilidade_id: str
    params: list[Parametro] = field(default_factory=list)
    retorno: str = "dict"

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Habilidade:
    """Nível 3 — Ação atômica composta que transforma entrada em saída.

    Composta por uma ou mais ações elementares.
    """

    id: str  # ex.: "ctx-extract"
    nome: str  # ex.: "Extrair contexto do KG" (infinitivo)
    capacidade_id: str
    entrada: dict[str, str] = field(default_factory=dict)  # nome → tipo
    saida: str = "dict"
    pre_condicoes: list[str] = field(default_factory=list)
    acoes: list[str] = field(default_factory=list)  # IDs das ações
    version: str = "1.0.0"

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass
class Capacidade:
    """Nível 2 — Agrupamento coeso de habilidades com objetivo comum.

    Attributes:
        id: Identificador único.
        nome: Nome no formato "[Substantivo] de/do [Complemento]".
        dominio_id: ID do domínio pai.
        categoria: Categoria (Core, Suporte, Governanca).
        maturidade: Nível de maturidade (L0–L3).
        habilidades: IDs das habilidades que compõem esta capacidade.
        version: Versão semântica.
        descricao: Descrição textual.
        owner: Responsável pela capacidade.
    """

    id: str
    nome: str
    dominio_id: str
    categoria: Categoria = Categoria.CORE
    maturidade: Maturidade = Maturidade.L0_CONCEITUAL
    habilidades: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    descricao: str = ""
    owner: str = ""


@dataclass
class Dominio:
    """Nível 1 — Área de negócio de alto nível.

    Agrupa capacidades relacionadas a um mesmo propósito estratégico.
    Máximo de 8 domínios no APOS R0.
    """

    id: str  # ex.: "DOM-01"
    nome: str  # ex.: "Contexto"
    descricao: str
    capacidades: list[str] = field(default_factory=list)  # IDs das capacidades


# ──────────────────────────────────────────────
# Critérios de Classificação
# ──────────────────────────────────────────────


@dataclass
class CriterioClassificacao:
    """Um critério de classificação com regra de verificação."""

    codigo: str  # ex.: "D01", "C01", "H01", "A01"
    nome: str
    descricao: str
    como_verificar: str = ""


# Critérios para Domínio (D01–D05)
CRITERIOS_DOMINIO: list[CriterioClassificacao] = [
    CriterioClassificacao(
        codigo="D01",
        nome="Escopo Estratégico",
        descricao="Representa uma área de negócio com propósito estratégico próprio",
        como_verificar="O domínio tem um 'por quê' que justifica existência independente",
    ),
    CriterioClassificacao(
        codigo="D02",
        nome="Coesão Semântica",
        descricao="Todas as capacidades do domínio compartilham vocabulário e regras",
        como_verificar="Um termo significa a mesma coisa dentro do domínio inteiro",
    ),
    CriterioClassificacao(
        codigo="D03",
        nome="Fronteira Clara",
        descricao="Não há ambiguidade sobre o que pertence ou não ao domínio",
        como_verificar="Um observador externo consegue classificar sem ajuda",
    ),
    CriterioClassificacao(
        codigo="D04",
        nome="Mínimo de 2 Capacidades",
        descricao="Domínios com 1 capacidade devem ser reavaliados",
        como_verificar="Contagem de capacidades filhas",
    ),
    CriterioClassificacao(
        codigo="D05",
        nome="Máximo de 8 Domínios",
        descricao="Controla complexidade cognitiva da taxonomia",
        como_verificar="Contagem total ≤ 8",
    ),
]

# Critérios para Capacidade (C01–C06)
CRITERIOS_CAPACIDADE: list[CriterioClassificacao] = [
    CriterioClassificacao(
        codigo="C01",
        nome="Agrupamento Coeso",
        descricao="Habilidades dentro da capacidade compartilham objetivo comum",
        como_verificar="As habilidades resolvem o mesmo 'problema'",
    ),
    CriterioClassificacao(
        codigo="C02",
        nome="Auto-Contida",
        descricao="A capacidade pode ser descrita em 1-2 frases sem referenciar outras capacidades",
        como_verificar="Descrição independe de outras capacidades",
    ),
    CriterioClassificacao(
        codigo="C03",
        nome="Mínimo de 2 Habilidades",
        descricao="Capacidades com 1 habilidade devem ser fundidas",
        como_verificar="Contagem de habilidades filhas",
    ),
    CriterioClassificacao(
        codigo="C04",
        nome="Máximo de 8 Habilidades",
        descricao="Controla complexidade interna da capacidade",
        como_verificar="Contagem de habilidades ≤ 8",
    ),
    CriterioClassificacao(
        codigo="C05",
        nome="Categoria Definida",
        descricao="Toda capacidade tem uma categoria (Core, Suporte ou Governança)",
        como_verificar="Atributo categoria preenchido",
    ),
    CriterioClassificacao(
        codigo="C06",
        nome="Maturidade Atribuída",
        descricao="Toda capacidade tem um nível de maturidade (L0-L3)",
        como_verificar="Atributo maturidade preenchido",
    ),
]

# Critérios para Habilidade (H01–H05)
CRITERIOS_HABILIDADE: list[CriterioClassificacao] = [
    CriterioClassificacao(
        codigo="H01",
        nome="Atomicidade Composta",
        descricao="A operação resolve um problema completo, mas pode ser decomposta em ações",
        como_verificar="Pode ser descrita como uma sequência de ações",
    ),
    CriterioClassificacao(
        codigo="H02",
        nome="Entrada/Saída Definidos",
        descricao="Parâmetros de entrada e tipo de retorno são formalmente especificados",
        como_verificar="Assinatura documentada",
    ),
    CriterioClassificacao(
        codigo="H03",
        nome="Pré-Condições",
        descricao="Condições que devem ser verdade antes da execução",
        como_verificar="Lista de pré-condições não vazia",
    ),
    CriterioClassificacao(
        codigo="H04",
        nome="Testável Isoladamente",
        descricao="A habilidade pode ser testada sem depender de outras habilidades",
        como_verificar="Teste unitário possível",
    ),
    CriterioClassificacao(
        codigo="H05",
        nome="Nome no Infinitivo",
        descricao="Segue o padrão de nomenclatura (Extrair, Montar, Validar, etc.)",
        como_verificar="Verificação de nomenclatura",
    ),
]

# Critérios para Ação (A01–A04)
CRITERIOS_ACAO: list[CriterioClassificacao] = [
    CriterioClassificacao(
        codigo="A01",
        nome="Atomicidade Simples",
        descricao="A operação não pode ser decomposta em sub-operações significativas",
        como_verificar="Executa em 1 chamada de API/método",
    ),
    CriterioClassificacao(
        codigo="A02",
        nome="Mapeamento 1:1",
        descricao="Corresponde exatamente a uma função/método/chamada de sistema",
        como_verificar="Há código correspondente no repositório",
    ),
    CriterioClassificacao(
        codigo="A03",
        nome="Sem Efeitos Colaterais Ocultos",
        descricao="Toda mudança de estado é explícita na assinatura",
        como_verificar="Documentação de side effects",
    ),
    CriterioClassificacao(
        codigo="A04",
        nome="Auditável",
        descricao="A execução da ação pode ser registrada em log com timestamp e identidade",
        como_verificar="Formato de log definido",
    ),
]

# Mapa de todos os critérios por código
CRITERIOS_POR_CODIGO: dict[str, CriterioClassificacao] = {
    c.codigo: c
    for c in (
        CRITERIOS_DOMINIO + CRITERIOS_CAPACIDADE + CRITERIOS_HABILIDADE + CRITERIOS_ACAO
    )
}

# Critérios de categoria (K01–K05): Core vs Suporte vs Governança
CRITERIOS_CATEGORIA: dict[str, dict[str, str]] = {
    "K01": {
        "nome": "Caminho crítico de jornada primária",
        "core": "Obrigatório",
        "suporte": "Opcional",
        "governanca": "Opcional",
    },
    "K02": {
        "nome": "Impacto direto na experiência do agente",
        "core": "Alto",
        "suporte": "Médio",
        "governanca": "Indireto",
    },
    "K03": {
        "nome": "Pode ser desligado sem perda funcional",
        "core": "Não",
        "suporte": "Sim",
        "governanca": "Sim (temporário)",
    },
    "K04": {
        "nome": "Executa em tempo real",
        "core": "Sim",
        "suporte": "Sim",
        "governanca": "Assíncrono/Batch",
    },
    "K05": {
        "nome": "Provê auditoria ou controle",
        "core": "Não",
        "suporte": "Não",
        "governanca": "Sim",
    },
}


# ──────────────────────────────────────────────
# MaturityMatrix
# ──────────────────────────────────────────────


@dataclass
class MaturityEntry:
    """Entrada da matriz de maturidade para uma capacidade."""

    capacidade_id: str
    dominio: str
    capacidade: str
    categoria: Categoria
    maturidade_r0: Maturidade
    maturidade_target_r1: Maturidade
    depende_de: list[str] = field(default_factory=list)


# Matriz completa de maturidade (extraída da CAPABILITY_TAXONOMY.md §4.2)
MATURITY_MATRIX: list[MaturityEntry] = [
    MaturityEntry("ctx-montagem", "Contexto", "Montagem de Contexto", Categoria.CORE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["DOM-02"]),
    MaturityEntry("ctx-pipeline", "Contexto", "Pipeline de Contexto", Categoria.CORE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["ctx-montagem"]),
    MaturityEntry("ctx-memoria", "Contexto", "Memória de Sessão", Categoria.CORE, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, ["ctx-pipeline"]),
    MaturityEntry("ctx-compressao", "Contexto", "Compressão de Blocos", Categoria.SUPORTE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["ctx-montagem"]),
    MaturityEntry("grafo-navegacao", "Grafo", "Navegação do Grafo", Categoria.CORE, Maturidade.L2_IMPLEMENTADO, Maturidade.L3_OTIMIZADO, ["DOM-05"]),
    MaturityEntry("grafo-queries", "Grafo", "Query Patterns", Categoria.CORE, Maturidade.L2_IMPLEMENTADO, Maturidade.L3_OTIMIZADO, ["grafo-navegacao"]),
    MaturityEntry("grafo-nos", "Grafo", "Gestão de Nós", Categoria.CORE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["grafo-navegacao"]),
    MaturityEntry("grafo-arestas", "Grafo", "Gestão de Arestas", Categoria.CORE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["grafo-navegacao"]),
    MaturityEntry("ag-dispatching", "Agentes", "Dispatching", Categoria.CORE, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, ["DOM-01"]),
    MaturityEntry("ag-ciclo-vida", "Agentes", "Ciclo de Vida", Categoria.CORE, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["ag-dispatching"]),
    MaturityEntry("ag-roteamento", "Agentes", "Roteamento", Categoria.CORE, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, ["ag-dispatching"]),
    MaturityEntry("gov-trust-score", "Governança", "Trust Score", Categoria.GOVERNANCA, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, ["DOM-02"]),
    MaturityEntry("gov-orphans", "Governança", "Detecção de Órfãos", Categoria.GOVERNANCA, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["DOM-02"]),
    MaturityEntry("gov-semantic-gates", "Governança", "Semantic Gates", Categoria.GOVERNANCA, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["DOM-05"]),
    MaturityEntry("gov-auditoria", "Governança", "Auditoria de Ações", Categoria.GOVERNANCA, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, ["DOM-03"]),
    MaturityEntry("ont-gestao", "Ontologia", "Gestão de Ontologia", Categoria.CORE, Maturidade.L2_IMPLEMENTADO, Maturidade.L3_OTIMIZADO, []),
    MaturityEntry("ont-validacao", "Ontologia", "Validação de Restrições", Categoria.SUPORTE, Maturidade.L1_ESTRUTURADO, Maturidade.L2_IMPLEMENTADO, ["ont-gestao"]),
    MaturityEntry("cat-rastreabilidade", "Catálogo", "Rastreabilidade", Categoria.SUPORTE, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["DOM-02"]),
    MaturityEntry("cat-qualidade", "Catálogo", "Qualidade de Dados", Categoria.GOVERNANCA, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["cat-rastreabilidade"]),
    MaturityEntry("infra-cache", "Infraestrutura", "Cache", Categoria.SUPORTE, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, []),
    MaturityEntry("infra-mcp", "Infraestrutura", "Transporte MCP", Categoria.SUPORTE, Maturidade.L0_CONCEITUAL, Maturidade.L2_IMPLEMENTADO, []),
    MaturityEntry("obs-metricas", "Observabilidade", "Métricas", Categoria.SUPORTE, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, []),
    MaturityEntry("obs-alertas", "Observabilidade", "Alertas", Categoria.SUPORTE, Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, ["obs-metricas"]),
]


# ──────────────────────────────────────────────
# Funções de Validação e Evolução
# ──────────────────────────────────────────────


def todas_habilidades_definidas(capacidade: Capacidade) -> bool:
    """Verifica se todas as habilidades de uma capacidade estão definidas.

    (Implementação conceitual — em produção consultaria um repositório.)
    """
    return len(capacidade.habilidades) >= 2


def todas_habilidades_implementadas(capacidade: Capacidade) -> bool:
    """Verifica se todas as habilidades estão implementadas.

    (Implementação conceitual.)
    """
    return len(capacidade.habilidades) >= 2


def cobertura_testes(capacidade: Capacidade) -> float:
    """Retorna cobertura de testes simulada.

    (Implementação conceitual — em produção consultaria ferramentas de cobertura.)
    """
    return 1.0 if capacidade.maturidade >= Maturidade.L1_ESTRUTURADO else 0.0


def pode_evoluir(capacidade: Capacidade, nivel_alvo: Maturidade) -> bool:
    """Verifica se uma capacidade pode evoluir para o nível de maturidade alvo.

    Regras definidas na CAPABILITY_TAXONOMY.md §5.6.

    Args:
        capacidade: A capacidade a ser avaliada.
        nivel_alvo: Nível de maturidade desejado.

    Returns:
        True se a evolução é permitida.
    """
    if nivel_alvo == Maturidade.L1_ESTRUTURADO:
        return todas_habilidades_definidas(capacidade)

    if nivel_alvo == Maturidade.L2_IMPLEMENTADO:
        return (
            capacidade.maturidade >= Maturidade.L1_ESTRUTURADO
            and todas_habilidades_implementadas(capacidade)
            and cobertura_testes(capacidade) >= 0.7
        )

    if nivel_alvo == Maturidade.L3_OTIMIZADO:
        return (
            capacidade.maturidade >= Maturidade.L2_IMPLEMENTADO
            # Em produção: benchmark_definido, metricas_performance_coletadas
            # e revisao_arquitetura_aprovada
        )

    return False


# ──────────────────────────────────────────────
# Catálogo de Domínios (R0)
# ──────────────────────────────────────────────

DOMINIOS_R0: list[Dominio] = [
    Dominio(
        id="DOM-01",
        nome="Contexto",
        descricao="Montagem, gestão e entrega de contexto semântico para agentes",
        capacidades=["ctx-montagem", "ctx-pipeline", "ctx-memoria"],
    ),
    Dominio(
        id="DOM-02",
        nome="Grafo",
        descricao="Operações sobre o Knowledge Graph (nós, arestas, queries)",
        capacidades=["grafo-navegacao", "grafo-queries", "grafo-nos", "grafo-arestas"],
    ),
    Dominio(
        id="DOM-03",
        nome="Agentes",
        descricao="Ciclo de vida, dispatchers e execução de agentes de IA",
        capacidades=["ag-dispatching", "ag-ciclo-vida", "ag-roteamento"],
    ),
    Dominio(
        id="DOM-04",
        nome="Governança",
        descricao="Auditoria, trust score, regras e conformidade",
        capacidades=["gov-trust-score", "gov-orphans", "gov-semantic-gates", "gov-auditoria"],
    ),
    Dominio(
        id="DOM-05",
        nome="Ontologia",
        descricao="Definição, validação e evolução da ontologia do sistema",
        capacidades=["ont-gestao", "ont-validacao"],
    ),
    Dominio(
        id="DOM-06",
        nome="Catálogo",
        descricao="Linhagem de dados, proveniência e metadados",
        capacidades=["cat-rastreabilidade", "cat-qualidade"],
    ),
    Dominio(
        id="DOM-07",
        nome="Infraestrutura",
        descricao="Suporte técnico: logging, cache, transporte MCP",
        capacidades=["infra-cache", "infra-mcp"],
    ),
    Dominio(
        id="DOM-08",
        nome="Observabilidade",
        descricao="Métricas, tracing e monitoramento do sistema",
        capacidades=["obs-metricas", "obs-alertas"],
    ),
]

# Catálogo de Domínios por ID
DOMINIOS_POR_ID: dict[str, Dominio] = {d.id: d for d in DOMINIOS_R0}


def classificar_categoria(capacidade: Capacidade) -> Categoria:
    """Classifica a categoria de uma capacidade com base nos critérios K01–K05.

    Args:
        capacidade: Capacidade a ser classificada.

    Returns:
        Categoria inferida.
    """
    # Lógica simplificada: se o domínio é Ontologia e é gestão, é Core
    if capacidade.dominio_id in ("DOM-05",) and "gestão" in capacidade.nome.lower():
        return Categoria.CORE

    # Domínios que mapeiam diretamente para categoria
    dominio_categoria: dict[str, Categoria] = {
        "DOM-01": Categoria.CORE,
        "DOM-02": Categoria.CORE,
        "DOM-03": Categoria.CORE,
        "DOM-04": Categoria.GOVERNANCA,
        "DOM-05": Categoria.CORE,
    }

    return dominio_categoria.get(capacidade.dominio_id, Categoria.SUPORTE)


def validar_dominio(dominio: Dominio) -> list[str]:
    """Valida um domínio contra os critérios D01–D05.

    Returns:
        Lista de códigos de critérios não atendidos (vazia se válido).
    """
    violacoes: list[str] = []

    # D04: Mínimo de 2 Capacidades
    if len(dominio.capacidades) < 2:
        violacoes.append("D04")

    return violacoes


def validar_capacidade(capacidade: Capacidade) -> list[str]:
    """Valida uma capacidade contra os critérios C01–C06.

    Returns:
        Lista de códigos de critérios não atendidos (vazia se válido).
    """
    violacoes: list[str] = []

    # C03: Mínimo de 2 Habilidades
    if len(capacidade.habilidades) < 2:
        violacoes.append("C03")

    # C04: Máximo de 8 Habilidades
    if len(capacidade.habilidades) > 8:
        violacoes.append("C04")

    return violacoes
