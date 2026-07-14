"""
Extracao qualitativa (dimensoes/criterios/metodos/contexto/RQs) dos 17 novos registros de
nucleo desta busca de sensibilidade (12 da sensibilidade + 5 REG_ promovidos na reavaliacao),
seguindo o mesmo schema e vocabulario fechado de
latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv (Etapa 8/9 originais).

Extracao manual (leitura integral de titulo+resumo de cada um dos 17 -- volume pequeno,
nao automatizada), aplicando os vocabularios ja documentados em
docs/CODEBOOK_CATEGORIAS_ETAPA_8.md (dimensoes, criterios, metodos, contexto).

Saida: latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv
(104 originais + 17 novos = 121; NAO sobrescreve o arquivo original, que o script R le por
padrao -- ver prompt para Codex em docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md).
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTES_DIR = os.path.join(BASE_DIR, "latex-artigo", "fontes")
ORIGINAL_PATH = os.path.join(FONTES_DIR, "nucleo_final_pos_auditoria_resumos.csv")
CORPUS_V2_PATH = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado_v2_sensibilidade.csv")
OUT_PATH = os.path.join(FONTES_DIR, "nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv")

# id_unico -> (busca este id no id_sensibilidade dentro de ids_brutos_agrupados do corpus v2,
# ou e um REG_ ja existente promovido pela reavaliacao)
REGISTROS = {
    "REG_02383": {
        "ja_existe": True,
        "criterios": "custo;vida_util;condicao_fisica",
        "metodos": "machine learning;life-cycle cost;framework",
        "contexto": "universidade",
        "dimensoes": "economica;ciclo_de_vida;tecnica_operacional",
        "tipo_contribuicao": "gestao_manutencao_predial;custo_ciclo_de_vida;contexto_publico_universitario",
        "evidencia": "\"multiple regression analysis and back-propagation artificial neural network (BPN) are used to establish a cost model for predicting maintenance costs\"",
        "confianca": "alta",
    },
    "REG_07814": {
        "ja_existe": True,
        "criterios": "custo;vida_util",
        "metodos": "machine learning;life-cycle cost",
        "contexto": "universidade",
        "dimensoes": "economica;ciclo_de_vida",
        "tipo_contribuicao": "gestao_manutencao_predial;custo_ciclo_de_vida;contexto_publico_universitario",
        "evidencia": "\"a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)\"",
        "confianca": "alta",
    },
    "REG_07815": {
        "ja_existe": True,
        "criterios": "custo;vida_util",
        "metodos": "machine learning;life-cycle cost",
        "contexto": "universidade",
        "dimensoes": "economica;ciclo_de_vida",
        "tipo_contribuicao": "gestao_manutencao_predial;custo_ciclo_de_vida;contexto_publico_universitario",
        "evidencia": "\"a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)\"",
        "confianca": "alta",
    },
    "REG_05418": {
        "ja_existe": True,
        "criterios": "energia;conforto;desempenho_operacional",
        "metodos": "machine learning;optimization",
        "contexto": "edificio_comercial",
        "dimensoes": "ambiental;tecnica_operacional",
        "tipo_contribuicao": "energia_desempenho_operacional;gestao_manutencao_predial",
        "evidencia": "\"A novel ventilation control model, AI-VAV, is developed using a hybrid extreme learning machine (ELM) algorithm combined with simulated annealing (SA) optimisation\"",
        "confianca": "alta",
    },
    "REG_06840": {
        "ja_existe": True,
        "criterios": "conforto;energia;desempenho_operacional",
        "metodos": "digital twin;machine learning",
        "contexto": "edificio_generico",
        "dimensoes": "tecnica_operacional;ambiental;social",
        "tipo_contribuicao": "energia_desempenho_operacional;risco_seguranca_conforto",
        "evidencia": "\"integrates Digital Twin (DT) technology with machine learning ... employs a Deep Neural Network (DNN) to predict thermal comfort\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_00383": {
        "ja_existe": False,
        "criterios": "condicao_fisica;manutenibilidade;desempenho_operacional",
        "metodos": "machine learning;decision support",
        "contexto": "edificio_residencial",
        "dimensoes": "tecnica_operacional",
        "tipo_contribuicao": "gestao_manutencao_predial",
        "evidencia": "\"CNN algorithm ... trains a multi-layer perceptron (MLP) model to classify damage types and automatically push reasonable maintenance plans\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_00893": {
        "ja_existe": False,
        "criterios": "energia;informacao_dados;desempenho_operacional",
        "metodos": "digital twin;BIM;machine learning;framework",
        "contexto": "edificio_generico",
        "dimensoes": "ambiental;tecnica_operacional;institucional",
        "tipo_contribuicao": "energia_desempenho_operacional",
        "evidencia": "\"Digital Twins support continuous monitoring, predictive maintenance, and performance optimization ... Emerging directions include Artificial Intelligence integration for autonomous optimization\"",
        "confianca": "media",
    },
    "SENS_SCOPUS_00941": {
        "ja_existe": False,
        "criterios": "energia;informacao_dados;conforto",
        "metodos": "IoT;machine learning;framework",
        "contexto": "edificio_generico",
        "dimensoes": "ambiental;tecnica_operacional;institucional",
        "tipo_contribuicao": "energia_desempenho_operacional",
        "evidencia": "\"AI complements these functions through predictive maintenance, energy forecasting, demand-side management, intelligent climate control\"",
        "confianca": "media",
    },
    "SENS_SCOPUS_01442": {
        "ja_existe": False,
        "criterios": "vida_util;manutenibilidade;condicao_fisica",
        "metodos": "machine learning",
        "contexto": "edificio_generico",
        "dimensoes": "ciclo_de_vida;tecnica_operacional",
        "tipo_contribuicao": "custo_ciclo_de_vida;gestao_manutencao_predial",
        "evidencia": "\"we configure building envelope deterioration factors as a generic acyclic graph and employ Graph Neural Networks for node-level regression ... enhance predictive maintenance strategies\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_01593": {
        "ja_existe": False,
        "criterios": "manutenibilidade;risco;condicao_fisica",
        "metodos": "fuzzy;machine learning;decision support",
        "contexto": "patrimonio_historico",
        "dimensoes": "tecnica_operacional;institucional",
        "tipo_contribuicao": "gestao_manutencao_predial;risco_seguranca_conforto",
        "evidencia": "\"fuzzy logic and random forest methodologies manage both data obtained from professional experts and data obtained in situ ... reduces the probability of failure and uncertainty during decision-making\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_01768": {
        "ja_existe": False,
        "criterios": "energia;desempenho_operacional;informacao_dados",
        "metodos": "IoT;machine learning;framework",
        "contexto": "edificio_generico",
        "dimensoes": "ambiental;tecnica_operacional;institucional",
        "tipo_contribuicao": "energia_desempenho_operacional",
        "evidencia": "\"integrating modern technologies such as Internet of Things, Artificial Intelligence, energy management solutions ... predictive maintenance models suitable for legacy systems\"",
        "confianca": "media",
    },
    "SENS_SCOPUS_01973": {
        "ja_existe": False,
        "criterios": "energia;manutenibilidade;conforto",
        "metodos": "IoT;machine learning",
        "contexto": "patrimonio_historico",
        "dimensoes": "ambiental;ciclo_de_vida;tecnica_operacional",
        "tipo_contribuicao": "energia_desempenho_operacional;gestao_manutencao_predial",
        "evidencia": "\"combining the IoT with Deep Learning-enhanced Predictive Energy Modeling (DL-PEM) ... reduce maintenance costs, and pave the way for predictive maintenance\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_02141": {
        "ja_existe": False,
        "criterios": "condicao_fisica;manutenibilidade;desempenho_operacional",
        "metodos": "machine learning",
        "contexto": "edificio_generico",
        "dimensoes": "tecnica_operacional",
        "tipo_contribuicao": "gestao_manutencao_predial",
        "evidencia": "\"Capsule Network-based deep learning model ... detects and identifies thermal anomalies ... improve the efficiency of decision-making for building envelope retrofitting and maintenance\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_02206": {
        "ja_existe": False,
        "criterios": "condicao_fisica;manutenibilidade;risco",
        "metodos": "machine learning",
        "contexto": "edificio_residencial",
        "dimensoes": "tecnica_operacional",
        "tipo_contribuicao": "gestao_manutencao_predial;risco_seguranca_conforto",
        "evidencia": "\"performance of several advanced prediction and ensemble machine learning models is compared ... critical to scheduling and performing effective building maintenance\"",
        "confianca": "alta",
    },
    "SENS_SCOPUS_03129": {
        "ja_existe": False,
        "criterios": "energia;agua;informacao_dados",
        "metodos": "machine learning;decision support",
        "contexto": "edificio_residencial;portfolio_predial",
        "dimensoes": "ambiental;economica",
        "tipo_contribuicao": "energia_desempenho_operacional",
        "evidencia": "\"residential energy and resource consumption estimation model ... using a multi-layer perceptron (MLP) neural network\"",
        "confianca": "alta",
    },
    "SENS_WOS_art02_00048": {
        "ja_existe": False,
        "criterios": "condicao_fisica;seguranca;informacao_dados",
        "metodos": "machine learning;BIM;digital twin;decision support",
        "contexto": "edificio_generico",
        "dimensoes": "tecnica_operacional;institucional",
        "tipo_contribuicao": "gestao_manutencao_predial;risco_seguranca_conforto",
        "evidencia": "\"integration with artificial intelligence, Building Information Modelling, and Digital Twins ... promote sustainable lifecycle management (LCM) practices\"",
        "confianca": "media",
    },
    "SENS_WOS_art02_00550": {
        "ja_existe": False,
        "criterios": "energia;conforto;informacao_dados",
        "metodos": "IoT;machine learning;framework",
        "contexto": "edificio_generico",
        "dimensoes": "ambiental;social;tecnica_operacional",
        "tipo_contribuicao": "energia_desempenho_operacional",
        "evidencia": "\"HVAC optimization: 30-70% through artificial intelligence ... IoT-based systems play a strategic role in achieving environmental sustainability goals\"",
        "confianca": "media",
    },
}

CAMPOS = [
    "id_unico", "ano", "bases_origem", "doi", "titulo", "resumo_presente",
    "decisao_qualitativa_final", "rqs_confirmadas_leitura", "rq0_confirmada",
    "rq1_confirmada", "rq2_confirmada", "rq3_confirmada", "rq4_confirmada",
    "rq5_confirmada", "tipo_contribuicao_artigo", "criterios_identificados_leitura",
    "metodos_decisao_identificados_leitura", "contexto_edificacao_identificado_leitura",
    "dimensoes_sustentabilidade_identificadas_leitura", "lacuna_ou_limite_identificado_leitura",
    "motivo_decisao", "evidencia_curta_do_resumo", "nivel_confianca_decisao",
    "necessita_full_text_pontual", "motivo_full_text_pontual", "asreview_label_compativel",
    "observacao_auditoria",
]

OBS_PADRAO = (
    "Registro incorporado pela busca de sensibilidade IA/ML (2026-07-12). Auditoria de "
    "classe IA/ML por correspondência automatizada de termos (docs/CODEBOOK_SENSIBILIDADE_IA_ML.md, "
    "RQ6) seguida de revisão manual de título/resumo para extração qualitativa; sem uso de "
    "internet, PDFs ou full-text."
)


def main():
    with open(ORIGINAL_PATH, encoding="utf-8-sig", newline="") as f:
        originais = list(csv.DictReader(f))

    corpus_original_path = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado.csv")
    with open(corpus_original_path, encoding="utf-8-sig", newline="") as f:
        corpus_original_por_id = {r["id_unico"]: r for r in csv.DictReader(f)}

    with open(CORPUS_V2_PATH, encoding="utf-8-sig", newline="") as f:
        corpus_v2 = {r["id_unico"]: r for r in csv.DictReader(f)}
        # mapa id_sensibilidade -> linha do corpus v2 (novos registros)
        by_ids_brutos = {}
        for r in corpus_v2.values():
            if r.get("pertence_busca_sensibilidade_ia") == "sim":
                for token in r.get("ids_brutos_agrupados", "").split("|"):
                    by_ids_brutos[token.strip()] = r

    novas_linhas = []
    for chave, dados in REGISTROS.items():
        if dados["ja_existe"]:
            base = corpus_original_por_id[chave]
            id_unico, ano, bases, doi, titulo, resumo_presente = (
                base["id_unico"], base["ano"], base["bases_origem"], base["doi"], base["titulo"], base["resumo_presente"]
            )
        else:
            linha_corpus = by_ids_brutos.get(chave)
            if linha_corpus is None:
                raise SystemExit(f"Nao encontrado no corpus v2: {chave}")
            id_unico = linha_corpus["id_unico"]
            ano = linha_corpus["ano"]
            bases = linha_corpus["bases_origem"]
            doi = linha_corpus["doi"]
            titulo = linha_corpus["titulo"]
            resumo_presente = linha_corpus["resumo_presente"]

        rq0 = "sim"
        rq1 = "sim" if dados["dimensoes"] else "nao"
        rq2 = "sim" if dados["criterios"] else "nao"
        rq3 = "sim" if dados["metodos"] else "nao"
        rq4 = "sim" if dados["contexto"] else "nao"
        rq5 = "nao"
        rqs = ";".join(rq for rq, flag in [("RQ0", rq0), ("RQ1", rq1), ("RQ2", rq2), ("RQ3", rq3), ("RQ4", rq4), ("RQ5", rq5)] if flag == "sim")

        novas_linhas.append({
            "id_unico": id_unico,
            "ano": ano,
            "bases_origem": bases,
            "doi": doi,
            "titulo": titulo,
            "resumo_presente": resumo_presente,
            "decisao_qualitativa_final": "manter_nucleo_principal",
            "rqs_confirmadas_leitura": rqs,
            "rq0_confirmada": rq0, "rq1_confirmada": rq1, "rq2_confirmada": rq2,
            "rq3_confirmada": rq3, "rq4_confirmada": rq4, "rq5_confirmada": rq5,
            "tipo_contribuicao_artigo": dados["tipo_contribuicao"],
            "criterios_identificados_leitura": dados["criterios"],
            "metodos_decisao_identificados_leitura": dados["metodos"],
            "contexto_edificacao_identificado_leitura": dados["contexto"],
            "dimensoes_sustentabilidade_identificadas_leitura": dados["dimensoes"],
            "lacuna_ou_limite_identificado_leitura": "",
            "motivo_decisao": "Bloco A (objeto predial) + Bloco B (sustentabilidade) presentes, com aplicação de IA/ML confirmada (RQ6) -- mesmo critério do núcleo original.",
            "evidencia_curta_do_resumo": dados["evidencia"],
            "nivel_confianca_decisao": dados["confianca"],
            "necessita_full_text_pontual": "nao",
            "motivo_full_text_pontual": "nao_aplicavel",
            "asreview_label_compativel": "include",
            "observacao_auditoria": OBS_PADRAO,
        })

    todas = originais + novas_linhas
    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(todas)

    print(f"Originais: {len(originais)}, novos: {len(novas_linhas)}, total: {len(todas)}")
    print(f"Escrito: {OUT_PATH}")


if __name__ == "__main__":
    main()
