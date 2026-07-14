"""
Reavaliacao dos 7 registros do corpus original apontados pelo usuario como candidatos a
reclassificacao apos a criacao da RQ6 (IA/ML): REG_02383, REG_07814, REG_07815, REG_00362,
REG_05418, REG_06151, REG_06840. Decisao registrada manualmente por leitura integral do
resumo de cada um (nao automatizada -- apenas 7 registros), aplicando
docs/CODEBOOK_SENSIBILIDADE_IA_ML.md (Blocos A/B de scripts/python/pre_triagem.py + classe
de IA/ML).

Atualiza 07_SINTESE_TEMATICA/matriz_alinhamento_perguntas_pesquisa.csv (uso_recomendado_artigo,
estrato_uso_resumo, lista_rqs_respondidas, n_rqs_respondidas, justificativa_alinhamento_rq)
para os 4 registros promovidos a nucleo (analise_central).

Saida adicional: docs/REAVALIACAO_7_REGISTROS_SENSIBILIDADE.md
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MATRIZ_PATH = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA", "matriz_alinhamento_perguntas_pesquisa.csv")
RELATORIO_PATH = os.path.join(BASE_DIR, "docs", "REAVALIACAO_7_REGISTROS_SENSIBILIDADE.md")

# decisao_anterior ja documentada: 6 = analise_secundaria (A_nucleo_forte), 1 (REG_06840) = excluir_do_artigo
DECISOES = {
    "REG_02383": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_central",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "back-propagation artificial neural network (BPN)",
        "evidencia": "\"multiple regression analysis and back-propagation artificial neural network (BPN) are used to establish a cost model for predicting maintenance costs\"",
        "justificativa": (
            "Bloco A (objeto predial: \"university buildings\", \"maintenance\") e Bloco B "
            "(sustentabilidade: \"life-cycle cost analyses\") presentes, com técnica de IA/ML "
            "explicitamente aplicada e treinada (BPN) para predizer custo de manutenção -- "
            "atende ao mesmo critério que classificou \"relevante\" no corpus original. "
            "Promovido a análise central (núcleo)."
        ),
    },
    "REG_07814": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_central",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "back-propagation artificial neural network (BPN)",
        "evidencia": "\"a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)\"",
        "justificativa": (
            "Mesmo padrão de REG_02383/REG_07815 (mesmo grupo de pesquisa, campus da National "
            "Taiwan University): Bloco A (university buildings, maintenance) + Bloco B "
            "(life-cycle cost) + BPN treinada para predição de custo. Promovido a análise central."
        ),
    },
    "REG_07815": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_central",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "back-propagation artificial neural network (BPN)",
        "evidencia": "\"a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)\"",
        "justificativa": (
            "Mesmo padrão de REG_02383/REG_07814: Bloco A + Bloco B (life-cycle cost) + BPN "
            "treinada. Promovido a análise central."
        ),
    },
    "REG_00362": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_secundaria",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "random forest classification",
        "evidencia": "\"a random forest classification model is tested for accuracy in predicting primary space use, magnitude of energy consumption, and type of operational strategy\"",
        "justificativa": (
            "IA/ML confirmada (random forest, treinado sobre dados de medidores elétricos), mas "
            "sem termo de Bloco A (manutenção/operação predial) nem Bloco B (sustentabilidade) "
            "em correspondência literal -- o foco é caracterização de uso/desempenho do edifício "
            "a partir de dados de consumo, não manutenção ou sustentabilidade explícitas. "
            "Mantido em análise secundária (relação indireta com o escopo da revisão)."
        ),
    },
    "REG_05418": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_central",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "extreme learning machine (ELM) + simulated annealing",
        "evidencia": "\"A novel ventilation control model, AI-VAV, is developed using a hybrid extreme learning machine (ELM) algorithm combined with simulated annealing (SA) optimisation ... contributing to more sustainable building operations\"",
        "justificativa": (
            "Bloco A (\"building operation\", manutenção de HVAC) + Bloco B (\"sustainable "
            "building operations\") presentes, com técnica de IA/ML explicitamente treinada "
            "(ELM) sobre dados de monitoramento de longo prazo. Promovido a análise central."
        ),
    },
    "REG_06151": {
        "decisao_anterior": "analise_secundaria",
        "decisao_revisada": "analise_secundaria",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "LightGBM, XGBoost, SHAP (XAI)",
        "evidencia": "\"This study employs machine learning and Explainable Artificial Intelligence (XAI) to explore the impact ... of energy variables on carbon emissions in office building operations\"",
        "justificativa": (
            "IA/ML confirmada (LightGBM/XGBoost/SHAP) e Bloco B presente (\"sustainable "
            "buildings\"), mas sem termo de Bloco A (manutenção predial) em correspondência "
            "literal -- foco em emissões de carbono operacionais, não manutenção. Mantido em "
            "análise secundária (IA aplicada à energia/operação predial, relação indireta com "
            "manutenção)."
        ),
    },
    "REG_06840": {
        "decisao_anterior": "excluir_do_artigo",
        "decisao_revisada": "analise_central",
        "estrato_revisado": "A_nucleo_forte",
        "tecnica_ia_ml": "Deep Neural Network (DNN) + Digital Twin",
        "evidencia": "\"integrates Digital Twin (DT) technology with machine learning ... employs a Deep Neural Network (DNN) to predict thermal comfort ... sustainable, efficient, and occupant-friendly smart cities\"",
        "justificativa": (
            "Exclusão anterior não se sustenta: Bloco A (\"smart building operations\") + Bloco B "
            "(\"sustainable\", \"environmental sustainability\") presentes, com IA/ML "
            "explicitamente confirmada e validada empiricamente (DNN treinada e comparada a "
            "modelos tradicionais). O dicionário anterior (RQ0-RQ5) não reconhecia IA/ML como "
            "critério de inclusão, o que motivou a exclusão original apesar da forte relação "
            "temática. Exclusão revertida; promovido a análise central."
        ),
    },
}


def main():
    with open(MATRIZ_PATH, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
        campos = list(linhas[0].keys())

    promovidos = []
    for l in linhas:
        if l["id_unico"] in DECISOES:
            d = DECISOES[l["id_unico"]]
            if d["decisao_revisada"] == "analise_central":
                l["uso_recomendado_artigo"] = "analise_central"
                l["estrato_uso_resumo"] = d["estrato_revisado"]
                rqs = l.get("lista_rqs_respondidas", "") or ""
                if "RQ6" not in rqs:
                    l["lista_rqs_respondidas"] = (rqs + ";RQ6").strip(";")
                try:
                    l["n_rqs_respondidas"] = str(int(l.get("n_rqs_respondidas", "0") or "0") + 1)
                except ValueError:
                    pass
                l["justificativa_alinhamento_rq"] = (
                    (l.get("justificativa_alinhamento_rq", "") or "") +
                    " | RQ6 (IA/ML, reavaliação 2026-07-12): " + d["justificativa"]
                )
                promovidos.append(l["id_unico"])
            else:
                l["justificativa_alinhamento_rq"] = (
                    (l.get("justificativa_alinhamento_rq", "") or "") +
                    " | RQ6 (IA/ML, reavaliação 2026-07-12, mantido secundário): " + d["justificativa"]
                )

    with open(MATRIZ_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)

    linhas_rel = ["# REAVALIAÇÃO DOS 7 REGISTROS — RQ6 (IA/ML)\n"]
    linhas_rel.append(
        "Reavaliação manual (leitura integral do resumo de cada um dos 7 registros já "
        "existentes no corpus, apontados para revisão) aplicando "
        "`docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` — não automatizada, dado o volume pequeno (7 "
        "registros). Gerado/aplicado por `scripts/python/reavaliar_7_registros_ia_ml.py`.\n"
    )
    linhas_rel.append("| id_unico | Decisão anterior | Decisão revisada | Técnica IA/ML | Impacto no núcleo |")
    linhas_rel.append("|---|---|---|---|---|")
    for id_unico, d in DECISOES.items():
        impacto = "PROMOVIDO a análise central" if d["decisao_revisada"] == "analise_central" else "mantido em análise secundária"
        linhas_rel.append(f"| {id_unico} | {d['decisao_anterior']} | {d['decisao_revisada']} | {d['tecnica_ia_ml']} | {impacto} |")

    linhas_rel.append("\n## Evidência e justificativa por registro\n")
    for id_unico, d in DECISOES.items():
        linhas_rel.append(f"### {id_unico}\n")
        linhas_rel.append(f"- **Decisão anterior**: `{d['decisao_anterior']}`")
        linhas_rel.append(f"- **Decisão revisada**: `{d['decisao_revisada']}`")
        linhas_rel.append(f"- **Evidência**: {d['evidencia']}")
        linhas_rel.append(f"- **Justificativa**: {d['justificativa']}\n")

    linhas_rel.append(
        f"\n## Resumo\n\n{len(promovidos)} de 7 registros promovidos a análise central "
        f"(`{', '.join(promovidos)}`); os demais 2 (`REG_00362`, `REG_06151`) mantidos em "
        "análise secundária, por IA/ML confirmada mas relação com manutenção predial "
        "(Bloco A) não estabelecida literalmente no resumo disponível — decisão conservadora, "
        "não ampliada por analogia temática."
    )

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_rel) + "\n")

    print(f"Promovidos a analise_central: {promovidos}")
    print(f"Relatorio: {RELATORIO_PATH}")


if __name__ == "__main__":
    main()
