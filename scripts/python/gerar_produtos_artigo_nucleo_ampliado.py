"""
Reimplementacao em Python de scripts/r/10_gerar_produtos_artigo.R para o nucleo ampliado
de 121 registros (104 originais + 17 da busca de sensibilidade IA/ML).

Motivo: a execucao via R/Codex solicitada em docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md
nao chegou a ser commitada na branch (nenhum artefato _nucleo_ampliado_121 foi encontrado).
Por decisao explicita do usuario nesta sessao, a logica do script R foi recriada aqui em
Python (nao executo R), replicando termo a termo as mesmas regras de agregacao/rotulagem.

Entrada:
- latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv (121 registros)
- latex-artigo/fontes/dicionario_criterio_dimensao_etapa17.csv
- 03_PROCESSADOS/corpus_consolidado_v2_sensibilidade.csv (para tipo_documento raw dos 121)
- latex-artigo/fontes/tabela34_distribuicao_base_tipo_nucleo_final_104.csv (tipo_documento raw dos 104 originais)

Saida (todas com sufixo _nucleo_ampliado_121, NAO sobrescrevem os arquivos _nucleo_final_104),
nomes literais (para conferencia por scripts/python/verificar_artigo.py):
- latex-artigo/fontes/tabela26_criterios_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela27_dimensoes_sustentabilidade_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela28_metodos_decisao_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela29_contexto_edificacao_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela30_lacunas_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela31_coocorrencia_criterio_metodo_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela32_coocorrencia_dimensao_metodo_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela33_distribuicao_temporal_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela34_bases_origem_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela34_tipos_documentais_harmonizados_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela35_mencoes_ods_esg_nucleo_ampliado_121.csv
- latex-artigo/fontes/tabela36_tipo_contribuicao_artigo_nucleo_ampliado_121.csv
- latex-artigo/figuras/figura09_distribuicao_temporal_nucleo_ampliado_121.png
- latex-artigo/figuras/figura11_metodos_mcdm_mais_frequentes_nucleo_ampliado_121.png
- latex-artigo/figuras/figura12_dimensoes_sustentabilidade_nucleo_ampliado_121.png
- latex-artigo/figuras/figura13_heatmap_criterios_metodos_nucleo_ampliado_121.png
- latex-artigo/figuras/figura14_matriz_analitica_dimensao_metodo_nucleo_ampliado_121.png
- docs/RELATORIO_EXECUCAO_R_NUCLEO_AMPLIADO.md (comparativo 104 vs 121)
"""

import csv
import os
import sys
from collections import Counter, defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTES_DIR = os.path.join(BASE_DIR, "latex-artigo", "fontes")
FIGURAS_DIR = os.path.join(BASE_DIR, "latex-artigo", "figuras")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

NUCLEO_PATH = os.path.join(FONTES_DIR, "nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv")
DICIONARIO_PATH = os.path.join(FONTES_DIR, "dicionario_criterio_dimensao_etapa17.csv")
CORPUS_V2_PATH = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado_v2_sensibilidade.csv")
TIPOS_104_PATH = os.path.join(FONTES_DIR, "tabela34_distribuicao_base_tipo_nucleo_final_104.csv")

SUFIXO = "_nucleo_ampliado_121"


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def escrever_csv(caminho, campos, linhas):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for l in linhas:
            w.writerow(l)


def expandir_multivalor(dados, campo):
    """Retorna lista de (id_unico, valor) para cada valor nao vazio, separado por ';'."""
    pares = []
    vistos = set()
    for r in dados:
        valores = (r.get(campo) or "").strip()
        if not valores:
            continue
        for v in valores.split(";"):
            v = v.strip()
            if v and (r["id_unico"], v) not in vistos:
                vistos.add((r["id_unico"], v))
                pares.append((r["id_unico"], v))
    return pares


def resumir_multivalor(pares, n_total):
    """pares: lista de (id_unico, valor). Retorna lista de dicts ordenada por total desc."""
    por_valor = defaultdict(set)
    for id_unico, valor in pares:
        por_valor[valor].add(id_unico)
    linhas = []
    for valor, ids in por_valor.items():
        linhas.append({
            "valor": valor,
            "total_registros": len(ids),
            "percentual": round(100 * len(ids) / n_total, 1),
            "ids": ";".join(sorted(ids)),
        })
    linhas.sort(key=lambda l: (-l["total_registros"], l["valor"]))
    return linhas


def main():
    os.makedirs(FONTES_DIR, exist_ok=True)
    os.makedirs(FIGURAS_DIR, exist_ok=True)

    dados = ler_csv(NUCLEO_PATH)
    if len(dados) != 121:
        raise SystemExit(f"Esperado 121 registros, encontrado {len(dados)}.")
    ids_unicos = [r["id_unico"] for r in dados]
    if len(ids_unicos) != len(set(ids_unicos)):
        raise SystemExit("id_unico duplicado no nucleo ampliado.")
    N = len(dados)

    dicionario = {r["criterio"]: r["dimensao_roteiro"] for r in ler_csv(DICIONARIO_PATH)}

    # --- Tabela 26: criterios ---
    criterios_pares = expandir_multivalor(dados, "criterios_identificados_leitura")
    tabela26 = resumir_multivalor(criterios_pares, N)
    for l in tabela26:
        l["criterio"] = l.pop("valor")
        l["dimensao_roteiro"] = dicionario.get(l["criterio"], "")
        l["percentual_dos_121"] = l.pop("percentual")
    campos26 = ["criterio", "dimensao_roteiro", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela26_criterios{SUFIXO}.csv"), campos26, tabela26)

    # --- Tabela 27: dimensoes (canonicas) ---
    dimensoes_canonicas = ["tecnica_operacional", "institucional", "ambiental", "ciclo_de_vida", "economica", "social"]
    dimensoes_pares = expandir_multivalor(dados, "dimensoes_sustentabilidade_identificadas_leitura")
    tabela27_bruta = {l["valor"]: l for l in resumir_multivalor(dimensoes_pares, N)}
    tabela27 = []
    for dim in dimensoes_canonicas:
        l = tabela27_bruta.get(dim, {"total_registros": 0, "percentual": 0.0, "ids": ""})
        tabela27.append({
            "dimensao_identificada_leitura": dim,
            "total_registros": l["total_registros"],
            "percentual_dos_121": l["percentual"],
            "ids": l["ids"],
        })
    campos27 = ["dimensao_identificada_leitura", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela27_dimensoes_sustentabilidade{SUFIXO}.csv"), campos27, tabela27)

    # --- Tabela 28: metodos ---
    metodos_pares = expandir_multivalor(dados, "metodos_decisao_identificados_leitura")
    tabela28 = resumir_multivalor(metodos_pares, N)
    for l in tabela28:
        l["metodo_identificado_leitura"] = l.pop("valor")
        l["percentual_dos_121"] = l.pop("percentual")
    campos28 = ["metodo_identificado_leitura", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela28_metodos_decisao{SUFIXO}.csv"), campos28, tabela28)

    # --- Tabela 29: contexto edificacao ---
    contexto_pares = expandir_multivalor(dados, "contexto_edificacao_identificado_leitura")
    tabela29 = resumir_multivalor(contexto_pares, N)
    for l in tabela29:
        l["contexto_identificado_leitura"] = l.pop("valor")
        l["percentual_dos_121"] = l.pop("percentual")
    campos29 = ["contexto_identificado_leitura", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela29_contexto_edificacao{SUFIXO}.csv"), campos29, tabela29)

    # --- Tabela 30: lacunas ---
    com_lacuna_ids, sem_lacuna_ids, lacuna_ies_ids = [], [], []
    for r in dados:
        texto = (r.get("lacuna_ou_limite_identificado_leitura") or "").strip().lower()
        if texto.startswith("nao_identificada") or texto == "":
            sem_lacuna_ids.append(r["id_unico"])
        else:
            com_lacuna_ids.append(r["id_unico"])
        contrib = (r.get("tipo_contribuicao_artigo") or "")
        if any(t.strip() == "lacuna_para_ies_publicas" for t in contrib.split(";")):
            lacuna_ies_ids.append(r["id_unico"])
    tabela30 = [
        {"categoria": "com_lacuna_identificada_no_resumo", "total_registros": len(com_lacuna_ids), "percentual_dos_121": round(100 * len(com_lacuna_ids) / N, 1), "ids": ";".join(sorted(com_lacuna_ids))},
        {"categoria": "sem_lacuna_identificada_no_resumo", "total_registros": len(sem_lacuna_ids), "percentual_dos_121": round(100 * len(sem_lacuna_ids) / N, 1), "ids": ";".join(sorted(sem_lacuna_ids))},
        {"categoria": "lacuna_especifica_ies_publicas", "total_registros": len(lacuna_ies_ids), "percentual_dos_121": round(100 * len(lacuna_ies_ids) / N, 1), "ids": ";".join(sorted(lacuna_ies_ids))},
    ]
    campos30 = ["categoria", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela30_lacunas{SUFIXO}.csv"), campos30, tabela30)

    # --- Tabela 36: tipo de contribuicao ---
    contrib_pares = expandir_multivalor(dados, "tipo_contribuicao_artigo")
    tabela36 = resumir_multivalor(contrib_pares, N)
    for l in tabela36:
        l["tipo_contribuicao"] = l.pop("valor")
        l["percentual_dos_121"] = l.pop("percentual")
    campos36 = ["tipo_contribuicao", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela36_tipo_contribuicao_artigo{SUFIXO}.csv"), campos36, tabela36)

    # --- Tabela 31: coocorrencia criterio x metodo ---
    metodo_por_id = defaultdict(set)
    for id_unico, m in metodos_pares:
        metodo_por_id[id_unico].add(m)
    criterio_por_id = defaultdict(set)
    for id_unico, c in criterios_pares:
        criterio_por_id[id_unico].add(c)

    coocorr_cm = Counter()
    ids_cm = defaultdict(set)
    for id_unico in ids_unicos:
        for c in criterio_por_id.get(id_unico, []):
            for m in metodo_por_id.get(id_unico, []):
                coocorr_cm[(c, m)] += 1
                ids_cm[(c, m)].add(id_unico)
    tabela31 = [
        {"criterio": c, "metodo": m, "n_registros_comuns": n, "ids": ";".join(sorted(ids_cm[(c, m)]))}
        for (c, m), n in sorted(coocorr_cm.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))
    ]
    campos31 = ["criterio", "metodo", "n_registros_comuns", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela31_coocorrencia_criterio_metodo{SUFIXO}.csv"), campos31, tabela31)

    # --- Tabela 32: coocorrencia dimensao x metodo ---
    dimensoes_matriz = ["ambiental", "economica", "social", "tecnica_operacional", "institucional"]
    dimensao_por_id = defaultdict(set)
    for id_unico, d in dimensoes_pares:
        if d in dimensoes_matriz:
            dimensao_por_id[id_unico].add(d)

    coocorr_dm = Counter()
    ids_dm = defaultdict(set)
    for id_unico in ids_unicos:
        for d in dimensao_por_id.get(id_unico, []):
            for m in metodo_por_id.get(id_unico, []):
                coocorr_dm[(d, m)] += 1
                ids_dm[(d, m)].add(id_unico)
    tabela32 = [
        {"dimensao_roteiro": d, "metodo": m, "n_registros_comuns": n, "ids": ";".join(sorted(ids_dm[(d, m)]))}
        for (d, m), n in sorted(coocorr_dm.items(), key=lambda kv: (-kv[1], kv[0][0], kv[0][1]))
    ]
    campos32 = ["dimensao_roteiro", "metodo", "n_registros_comuns", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela32_coocorrencia_dimensao_metodo{SUFIXO}.csv"), campos32, tabela32)

    # --- Tabela 33: distribuicao temporal ---
    por_ano = defaultdict(list)
    for r in dados:
        try:
            ano = int(r["ano"])
        except (ValueError, TypeError):
            continue
        por_ano[ano].append(r["id_unico"])
    tabela33 = []
    for ano in range(2010, 2027):
        ids_ano = sorted(por_ano.get(ano, []))
        tabela33.append({
            "ano": ano,
            "total_registros": len(ids_ano),
            "percentual_dos_121": round(100 * len(ids_ano) / N, 1),
            "ids": ";".join(ids_ano),
        })
    campos33 = ["ano", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela33_distribuicao_temporal{SUFIXO}.csv"), campos33, tabela33)

    # --- Tabela 34a: bases de origem ---
    bases_pares = []
    vistos = set()
    for r in dados:
        for b in (r.get("bases_origem") or "").split("|"):
            b = b.strip()
            if b and (r["id_unico"], b) not in vistos:
                vistos.add((r["id_unico"], b))
                bases_pares.append((r["id_unico"], b))
    tabela_bases = resumir_multivalor(bases_pares, N)
    for l in tabela_bases:
        l["categoria"] = l.pop("valor")
        l["percentual_dos_121"] = l.pop("percentual")
        l["dimensao"] = "base_origem"
    campos_bases = ["dimensao", "categoria", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela34_bases_origem{SUFIXO}.csv"), campos_bases, tabela_bases)

    # --- Tabela 34b: tipos documentais harmonizados ---
    # 104 originais: harmonizacao ja documentada em tabela34_distribuicao_base_tipo_nucleo_final_104.csv
    tipos_104_raw = ler_csv(TIPOS_104_PATH)

    def harmonizar_tipo_raw(categoria):
        if categoria in ("Journal", "JOUR", "journal-article"):
            return "Artigo de periodico"
        if categoria in ("Conference Proceeding", "CPAPER"):
            return "Trabalho em evento"
        if categoria in ("Book Series", "Book"):
            return "Livro ou serie de livro"
        return "Outro"

    tipos_harmonizados = Counter()
    for r in tipos_104_raw:
        if r["dimensao"] == "tipo_documento":
            tipos_harmonizados[harmonizar_tipo_raw(r["categoria"])] += int(r["total_registros"])

    corpus_v2 = {r["id_unico"]: r for r in ler_csv(CORPUS_V2_PATH)}
    ids_originais = set(ids_unicos[:104])
    ids_novos = set(ids_unicos[104:])
    for id_unico in ids_novos:
        linha_corpus = corpus_v2.get(id_unico)
        if linha_corpus is None:
            raise SystemExit(f"id nao encontrado no corpus v2 para tipo_documento: {id_unico}")
        tipo = linha_corpus.get("tipo_documento", "").strip()
        # Os 12 registros vindos diretamente da busca de sensibilidade ja chegam com o rotulo
        # harmonizado (normalizar_sensibilidade_ia.py). Os 5 REG_ promovidos na reavaliacao sao
        # registros do corpus ORIGINAL, com tipo_documento em rotulo bruto (ex. "Journal") --
        # aplicar a mesma harmonizacao usada para o nucleo de 104 antes de classificar como "Outro".
        if tipo not in ("Artigo de periodico", "Trabalho em evento", "Livro ou serie de livro"):
            tipo = harmonizar_tipo_raw(tipo)
        tipos_harmonizados[tipo] += 1

    tabela34_tipos = [
        {"tipo_harmonizado": tipo, "total_registros": n, "percentual_dos_121": round(100 * n / N, 1)}
        for tipo, n in sorted(tipos_harmonizados.items(), key=lambda kv: -kv[1])
    ]
    campos34t = ["tipo_harmonizado", "total_registros", "percentual_dos_121"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela34_tipos_documentais_harmonizados{SUFIXO}.csv"), campos34t, tabela34_tipos)

    # --- Tabela 35: mencoes ODS/ESG ---
    import re
    mencao_ods_ids, mencao_esg_ids = [], []
    for r in dados:
        texto = " ".join([
            r.get("titulo", ""), r.get("tipo_contribuicao_artigo", ""),
            r.get("criterios_identificados_leitura", ""), r.get("metodos_decisao_identificados_leitura", ""),
            r.get("dimensoes_sustentabilidade_identificadas_leitura", ""),
            r.get("lacuna_ou_limite_identificado_leitura", ""), r.get("evidencia_curta_do_resumo", ""),
        ])
        if re.search(r"\b(ODS|SDGs?)\b", texto, re.IGNORECASE):
            mencao_ods_ids.append(r["id_unico"])
        if re.search(r"\bESG\b", texto, re.IGNORECASE):
            mencao_esg_ids.append(r["id_unico"])
    tabela35 = [
        {"marcador": "ODS ou SDG", "total_registros": len(mencao_ods_ids), "percentual_dos_121": round(100 * len(mencao_ods_ids) / N, 1), "ids": ";".join(sorted(mencao_ods_ids))},
        {"marcador": "ESG", "total_registros": len(mencao_esg_ids), "percentual_dos_121": round(100 * len(mencao_esg_ids) / N, 1), "ids": ";".join(sorted(mencao_esg_ids))},
    ]
    campos35 = ["marcador", "total_registros", "percentual_dos_121", "ids"]
    escrever_csv(os.path.join(FONTES_DIR, f"tabela35_mencoes_ods_esg{SUFIXO}.csv"), campos35, tabela35)

    # =========================== FIGURAS (matplotlib, tons de cinza) ===========================
    plt.rcParams.update({"font.size": 11, "axes.edgecolor": "black"})

    # figura09: distribuicao temporal
    anos = [l["ano"] for l in tabela33]
    totais_ano = [l["total_registros"] for l in tabela33]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.bar(anos, totais_ano, color="#b8b8b8", edgecolor="black", linewidth=0.35, width=0.78)
    for x, y in zip(anos, totais_ano):
        if y > 0:
            ax.text(x, y + 0.3, str(y), ha="center", va="bottom", fontsize=9)
    ax.set_xticks(anos)
    ax.set_xticklabels(anos, rotation=45, ha="right")
    ax.set_xlabel("Ano de publicação")
    ax.set_ylabel("Registros")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURAS_DIR, f"figura09_distribuicao_temporal{SUFIXO}.png"), dpi=300, facecolor="white")
    plt.close(fig)

    # figura12: dimensoes de sustentabilidade
    rotulos_dim = {
        "tecnica_operacional": "Técnica e operacional", "institucional": "Institucional",
        "ambiental": "Ambiental", "ciclo_de_vida": "Ciclo de vida", "economica": "Econômica", "social": "Social",
    }
    labels_dim = [rotulos_dim[d] for d in dimensoes_canonicas]
    valores_dim = [next(l["total_registros"] for l in tabela27 if l["dimensao_identificada_leitura"] == d) for d in dimensoes_canonicas]
    pct_dim = [next(l["percentual_dos_121"] for l in tabela27 if l["dimensao_identificada_leitura"] == d) for d in dimensoes_canonicas]
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    y_pos = range(len(labels_dim))
    ax.barh(list(y_pos)[::-1], valores_dim, color="#adadad", edgecolor="black", linewidth=0.35, height=0.72)
    ax.set_yticks(list(y_pos)[::-1])
    ax.set_yticklabels(labels_dim)
    for i, (v, p) in enumerate(zip(valores_dim, pct_dim)):
        ax.text(v + 1, list(y_pos)[::-1][i], f"{v} ({p}%)", va="center", fontsize=10)
    ax.set_xlim(0, N + 5)
    ax.set_xlabel("Registros")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURAS_DIR, f"figura12_dimensoes_sustentabilidade{SUFIXO}.png"), dpi=300, facecolor="white")
    plt.close(fig)

    # figura11: metodos mais frequentes (gerais x estruturados)
    metodos_gerais = ["framework", "decision support", "BIM", "optimization", "scoring", "life-cycle cost",
                       "fuzzy", "ranking", "IoT", "machine learning", "digital twin"]
    metodos_estruturados = ["AHP", "TOPSIS", "ANP", "MCDM", "Delphi", "balanced scorecard",
                             "case-based reasoning", "Bayesian Best Worst Method"]
    rotulos_met = {
        "framework": "Framework", "decision support": "Apoio à decisão", "BIM": "BIM",
        "optimization": "Otimização", "scoring": "Pontuação", "life-cycle cost": "Custo do ciclo de vida",
        "fuzzy": "Lógica difusa", "ranking": "Ordenação", "IoT": "IoT",
        "machine learning": "Aprendizado de máquina", "digital twin": "Digital twin",
        "AHP": "AHP", "TOPSIS": "TOPSIS", "ANP": "ANP", "MCDM": "MCDM", "Delphi": "Delphi",
        "balanced scorecard": "Balanced scorecard", "case-based reasoning": "Raciocínio baseado em casos",
        "Bayesian Best Worst Method": "Bayesian Best-Worst Method",
    }
    tabela28_dict = {l["metodo_identificado_leitura"]: l["total_registros"] for l in tabela28}
    itens_gerais = [(m, tabela28_dict.get(m, 0)) for m in metodos_gerais if tabela28_dict.get(m, 0) > 0]
    itens_estrut = [(m, tabela28_dict.get(m, 0)) for m in metodos_estruturados if tabela28_dict.get(m, 0) > 0]
    itens_gerais.sort(key=lambda kv: kv[1])
    itens_estrut.sort(key=lambda kv: kv[1])

    fig, axes = plt.subplots(2, 1, figsize=(9, 8.2), gridspec_kw={"height_ratios": [len(itens_gerais) or 1, len(itens_estrut) or 1]})
    for ax, itens, titulo, cor in [
        (axes[0], itens_gerais, "Abordagens e instrumentos gerais", "#b8b8b8"),
        (axes[1], itens_estrut, "Métodos formalmente nomeados", "#737373"),
    ]:
        if itens:
            labels = [rotulos_met[m] for m, _ in itens]
            vals = [v for _, v in itens]
            ax.barh(range(len(labels)), vals, color=cor, edgecolor="black", linewidth=0.3, height=0.72)
            ax.set_yticks(range(len(labels)))
            ax.set_yticklabels(labels)
            for i, v in enumerate(vals):
                ax.text(v + 0.3, i, str(v), va="center", fontsize=9)
        ax.set_title(titulo, fontsize=11, loc="left")
        ax.spines[["top", "right"]].set_visible(False)
    axes[1].set_xlabel("Registros")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURAS_DIR, f"figura11_metodos_mcdm_mais_frequentes{SUFIXO}.png"), dpi=300, facecolor="white")
    plt.close(fig)

    # figura13: heatmap criterio x metodo (top 10 x top 10)
    tabela26_dict = {l["criterio"]: l["total_registros"] for l in tabela26}
    top_criterios = [c for c, _ in sorted(tabela26_dict.items(), key=lambda kv: -kv[1])[:10]]
    top_metodos = [m for m, _ in sorted(tabela28_dict.items(), key=lambda kv: -kv[1])[:10]]
    rotulos_crit = {
        "desempenho_operacional": "Desempenho operacional", "informacao_dados": "Informação e dados",
        "custo": "Custo", "vida_util": "Vida útil", "energia": "Energia", "risco": "Risco",
        "condicao_fisica": "Condição física", "manutenibilidade": "Manutenibilidade",
        "conforto": "Conforto", "seguranca": "Segurança",
    }
    matriz = [[coocorr_cm.get((c, m), 0) for m in top_metodos] for c in top_criterios]
    fig, ax = plt.subplots(figsize=(10.5, 7.2))
    im = ax.imshow(matriz, cmap="Greys", aspect="auto")
    ax.set_xticks(range(len(top_metodos)))
    ax.set_xticklabels([rotulos_met.get(m, m) for m in top_metodos], rotation=45, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(top_criterios)))
    ax.set_yticklabels([rotulos_crit.get(c, c) for c in top_criterios], fontsize=9.5)
    vmax = max(max(row) for row in matriz) or 1
    for i, row in enumerate(matriz):
        for j, v in enumerate(row):
            ax.text(j, i, str(v), ha="center", va="center", color="white" if v > vmax * 0.55 else "black", fontsize=9.5)
    ax.set_xlabel("Instrumento de apoio à decisão")
    ax.set_ylabel("Critério")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURAS_DIR, f"figura13_heatmap_criterios_metodos{SUFIXO}.png"), dpi=300, facecolor="white")
    plt.close(fig)

    # figura14: heatmap dimensao x metodo
    matriz_d = [[coocorr_dm.get((d, m), 0) for m in top_metodos] for d in dimensoes_matriz]
    fig, ax = plt.subplots(figsize=(10.5, 5.6))
    im = ax.imshow(matriz_d, cmap="Greys", aspect="auto")
    ax.set_xticks(range(len(top_metodos)))
    ax.set_xticklabels([rotulos_met.get(m, m) for m in top_metodos], rotation=45, ha="right", fontsize=9.5)
    ax.set_yticks(range(len(dimensoes_matriz)))
    ax.set_yticklabels([rotulos_dim[d] for d in dimensoes_matriz], fontsize=10)
    vmax_d = max(max(row) for row in matriz_d) or 1
    for i, row in enumerate(matriz_d):
        for j, v in enumerate(row):
            ax.text(j, i, str(v), ha="center", va="center", color="white" if v > vmax_d * 0.55 else "black", fontsize=9.5)
    ax.set_xlabel("Instrumento de apoio à decisão")
    ax.set_ylabel("Dimensão")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGURAS_DIR, f"figura14_matriz_analitica_dimensao_metodo{SUFIXO}.png"), dpi=300, facecolor="white")
    plt.close(fig)

    print(f"N = {N}")
    print("Tabela 27 (dimensoes):", {l["dimensao_identificada_leitura"]: l["total_registros"] for l in tabela27})
    print("Tabela 26 (top criterios):", sorted(tabela26_dict.items(), key=lambda kv: -kv[1])[:5])
    print("Tabela 28 (top metodos):", sorted(tabela28_dict.items(), key=lambda kv: -kv[1])[:8])
    print("Tabela 34 tipos:", dict(tipos_harmonizados))
    print("Tabela 35 ODS/ESG:", len(mencao_ods_ids), len(mencao_esg_ids))
    print("Bases:", {l["categoria"]: l["total_registros"] for l in tabela_bases})
    print("Tabelas e graficos do nucleo ampliado gerados com sucesso (Python).")


if __name__ == "__main__":
    main()
