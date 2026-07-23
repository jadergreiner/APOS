"""Testes unitários para apos/capabilities/taxonomy.py — 10 cenários (T1–T10)."""

from __future__ import annotations

import pytest

from apos.capabilities.taxonomy import (
    Acao,
    Capacidade,
    Categoria,
    CriterioClassificacao,
    Dominio,
    Habilidade,
    Maturidade,
    Parametro,
)


# ══════════════════════════════════════════════
# T1 — Domínio
# ══════════════════════════════════════════════


class TestCapabilityTaxonomy:
    """10 cenários de teste para a taxonomia de capabilities (T1–T10)."""

    # ────────────────
    # Criação dos 4 níveis
    # ────────────────

    def test_dominio_create(self):
        """T1: Dominio com nome e descrição."""
        dominio = Dominio(
            id="DOM-01",
            nome="Contexto",
            descricao="Montagem, gestão e entrega de contexto semântico",
            capacidades=["ctx-montagem", "ctx-pipeline"],
        )
        assert dominio.id == "DOM-01"
        assert dominio.nome == "Contexto"
        assert dominio.descricao == "Montagem, gestão e entrega de contexto semântico"
        assert dominio.capacidades == ["ctx-montagem", "ctx-pipeline"]

    def test_capacidade_create(self):
        """T2: Capacidade vinculada a um Domínio."""
        capacidade = Capacidade(
            id="ctx-montagem",
            nome="Montagem de Contexto",
            dominio_id="DOM-01",
            categoria=Categoria.CORE,
            maturidade=Maturidade.L1_ESTRUTURADO,
            habilidades=["hab-montar-contexto", "hab-validar-fontes"],
            version="1.0.0",
            descricao="Monta o contexto do agente a partir de fontes",
            owner="time-contexto",
        )
        assert capacidade.id == "ctx-montagem"
        assert capacidade.nome == "Montagem de Contexto"
        assert capacidade.dominio_id == "DOM-01"
        assert capacidade.categoria == Categoria.CORE
        assert capacidade.maturidade == Maturidade.L1_ESTRUTURADO
        assert capacidade.habilidades == ["hab-montar-contexto", "hab-validar-fontes"]
        assert capacidade.owner == "time-contexto"

    def test_habilidade_create(self):
        """T3: Habilidade vinculada a uma Capacidade."""
        habilidade = Habilidade(
            id="hab-montar-contexto",
            nome="Montar Contexto do Agente",
            capacidade_id="ctx-montagem",
            entrada={"urn": "str", "depth": "int"},
            saida="Context",
            pre_condicoes=["KG não vazio", "agente autorizado"],
            acoes=["KG.traverse", "KG.filter"],
            version="1.0.0",
        )
        assert habilidade.id == "hab-montar-contexto"
        assert habilidade.nome == "Montar Contexto do Agente"
        assert habilidade.capacidade_id == "ctx-montagem"
        assert habilidade.entrada == {"urn": "str", "depth": "int"}
        assert habilidade.saida == "Context"
        assert len(habilidade.pre_condicoes) == 2
        assert habilidade.acoes == ["KG.traverse", "KG.filter"]
        assert habilidade.version == "1.0.0"

    def test_acao_create(self):
        """T4: Acao vinculada a uma Habilidade."""
        acao = Acao(
            id="KG.traverse",
            nome="KnowledgeGraph.traverse()",
            chamada="KG.traverse(urn, depth)",
            descricao="Percorre o grafo a partir de uma URN",
            habilidade_id="hab-montar-contexto",
            params=[
                Parametro(nome="urn", tipo="str", descricao="URN de partida", obrigatorio=True),
                Parametro(nome="depth", tipo="int", descricao="Profundidade máxima", obrigatorio=False, default=3),
            ],
            retorno="list[dict]",
        )
        assert acao.id == "KG.traverse"
        assert acao.nome == "KnowledgeGraph.traverse()"
        assert acao.chamada == "KG.traverse(urn, depth)"
        assert acao.habilidade_id == "hab-montar-contexto"
        assert len(acao.params) == 2
        assert acao.params[0].nome == "urn"
        assert acao.params[0].tipo == "str"
        assert acao.params[0].obrigatorio is True
        assert acao.params[1].nome == "depth"
        assert acao.params[1].default == 3
        assert acao.retorno == "list[dict]"

    # ────────────────
    # Maturidade
    # ────────────────

    def test_maturidade_level(self):
        """T5: L0_CONCEITUAL.level == 0, L3_OTIMIZADO.level == 3."""
        assert Maturidade.L0_CONCEITUAL.level == 0
        assert Maturidade.L1_ESTRUTURADO.level == 1
        assert Maturidade.L2_IMPLEMENTADO.level == 2
        assert Maturidade.L3_OTIMIZADO.level == 3

    def test_maturidade_comparison(self):
        """T6: L2 >= L1 → True, L1 >= L2 → False."""
        assert Maturidade.L2_IMPLEMENTADO >= Maturidade.L1_ESTRUTURADO
        assert Maturidade.L2_IMPLEMENTADO > Maturidade.L1_ESTRUTURADO
        assert not (Maturidade.L1_ESTRUTURADO >= Maturidade.L2_IMPLEMENTADO)
        assert Maturidade.L1_ESTRUTURADO < Maturidade.L2_IMPLEMENTADO
        assert Maturidade.L1_ESTRUTURADO <= Maturidade.L2_IMPLEMENTADO
        assert Maturidade.L0_CONCEITUAL <= Maturidade.L0_CONCEITUAL
        assert Maturidade.L3_OTIMIZADO >= Maturidade.L3_OTIMIZADO

    def test_maturidade_sorting(self):
        """T7: sorted([L1, L3, L0]) == [L0, L1, L3]."""
        unsorted = [Maturidade.L1_ESTRUTURADO, Maturidade.L3_OTIMIZADO, Maturidade.L0_CONCEITUAL]
        expected = [Maturidade.L0_CONCEITUAL, Maturidade.L1_ESTRUTURADO, Maturidade.L3_OTIMIZADO]
        assert sorted(unsorted) == expected

    # ────────────────
    # Categoria
    # ────────────────

    def test_categoria_values(self):
        """T8: Categoria.CORE, SUPORTE, GOVERNANCA existem com valores corretos."""
        assert Categoria.CORE.value == "core"
        assert Categoria.SUPORTE.value == "suporte"
        assert Categoria.GOVERNANCA.value == "governanca"
        # Verifica que os três existem
        expected = {"core", "suporte", "governanca"}
        actual = {c.value for c in Categoria}
        assert actual == expected

    # ────────────────
    # Critério de Classificação
    # ────────────────

    def test_criterio_classificacao(self):
        """T9: CriterioClassificacao com código, nome, descrição e verificação."""
        criterio = CriterioClassificacao(
            codigo="D01",
            nome="Escopo Estratégico",
            descricao="Representa uma área de negócio com propósito estratégico próprio",
            como_verificar="O domínio tem um 'por quê' que justifica existência independente",
        )
        assert criterio.codigo == "D01"
        assert criterio.nome == "Escopo Estratégico"
        assert criterio.descricao.startswith("Representa")
        assert "por quê" in criterio.como_verificar

    # ────────────────
    # Hash de Acao
    # ────────────────

    def test_acao_hash(self):
        """T10: Acao.__hash__ é consistente — mesmo id → mesmo hash."""
        a1 = Acao(
            id="KG.traverse",
            nome="KnowledgeGraph.traverse()",
            chamada="KG.traverse(urn, depth)",
            descricao="Percorre o grafo",
            habilidade_id="hab-montar-contexto",
        )
        a2 = Acao(
            id="KG.traverse",
            nome="KnowledgeGraph.traverse()",
            chamada="KG.traverse(urn, depth)",
            descricao="Percorre o grafo",
            habilidade_id="hab-montar-contexto",
        )
        a3 = Acao(
            id="KG.filter",
            nome="KG.filter()",
            chamada="KG.filter(conditions)",
            descricao="Filtra nós",
            habilidade_id="hab-montar-contexto",
        )
        # Mesmo id → mesmo hash
        assert hash(a1) == hash(a2)
        # ids diferentes → hashes diferentes (provável, não garantido matematicamente,
        # mas com hash() de string é quase certo)
        assert hash(a1) != hash(a3)
        # Pode ser usado em conjunto
        s = {a1, a3}
        assert len(s) == 2
        # a2 é igual a a1 pelo hash
        assert a2 in s  # depends on id
