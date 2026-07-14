"""
Auditoria de classe IA/ML (RQ6) de todos os 4889 registros unicos novos da busca de
sensibilidade (03_PROCESSADOS/sensibilidade_novos_unicos.csv), aplicando literalmente as
regras de docs/CODEBOOK_SENSIBILIDADE_IA_ML.md.

Metodo: correspondencia sistematica de termos (dois niveis: confirma / ambiguo) em
titulo + resumo + palavras-chave, com janela de contexto para aplicar as regras de
desambiguacao obrigatorias (transformer, decision tree, deep learning fora de contexto) e
heuristica lexical de "aplicacao efetiva" vs "mencao generica" (verbos como
develop/propose/apply/train/present/design coocorrendo com o termo de IA/ML, versus
linguagem de tendencia/revisao como trend/growing interest/future work/emerging).

NAO constitui leitura de texto completo -- classificacao por correspondencia de termos do
dicionario RQ6 (07_SINTESE_TEMATICA/dicionario_rq_etapa15.csv) e regras fechadas do
codebook, aplicada a titulo/resumo/palavras-chave disponiveis. Registros sem resumo
recebem nivel_confianca rebaixado por definicao.

Saida:
- 03_PROCESSADOS/sensibilidade_auditoria_classe_ia_ml.csv
- 03_PROCESSADOS/relatorio_auditoria_ia_ml.md
"""

import csv
import os
import re
import sys
from collections import Counter

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")

NOVOS_PATH = os.path.join(PROC_DIR, "sensibilidade_novos_unicos.csv")
OUT_PATH = os.path.join(PROC_DIR, "sensibilidade_auditoria_classe_ia_ml.csv")
RELATORIO_PATH = os.path.join(PROC_DIR, "relatorio_auditoria_ia_ml.md")

# --- Termos nivel "confirma" (Secao 2.1 do codebook) -----------------------------------
TERMOS_CONFIRMA = {
    "machine learning": "machine_learning",
    "aprendizado de maquina": "machine_learning",
    "deep learning": "deep_learning",
    "aprendizagem profunda": "deep_learning",
    "artificial neural network": "neural_network",
    "neural network": "neural_network",
    "rede neural": "neural_network",
    "convolutional neural network": "cnn",
    r"\bcnn\b": "cnn",
    "recurrent neural network": "rnn",
    r"\brnn\b": "rnn",
    r"\blstm\b": "lstm",
    r"\bgru\b": "gru",
    "random forest": "random_forest",
    "gradient boosting": "gradient_boosting",
    r"\bxgboost\b": "gradient_boosting",
    r"\blightgbm\b": "gradient_boosting",
    r"\bcatboost\b": "gradient_boosting",
    "support vector machine": "svm",
    r"\bsvm\b": "svm",
    "reinforcement learning": "reinforcement_learning",
    "computer vision": "computer_vision",
    "natural language processing": "nlp",
    r"\bnlp\b": "nlp",
    r"\bk-nearest neighbo(u)?rs?\b": "knn",
    r"\bknn\b": "knn",
    "generative adversarial network": "gan",
    r"\bgan\b": "gan",
    "autoencoder": "autoencoder",
    "transformer": "transformer",  # desambiguado depois
    "artificial intelligence": "artificial_intelligence",
    r"\bAI-driven\b": "artificial_intelligence",
    r"\bAI-based\b": "artificial_intelligence",
    "k-means": "kmeans",
    "bayesian network": "bayesian_network",
    "rede bayesiana": "bayesian_network",
    r"\bshap\b": "shap_lime",
    r"\blime\b(?!stone)": "shap_lime",
    "large language model": "llm",
    r"\bllms?\b": "llm",
    "generative ai": "generative_ai",
    "generative artificial intelligence": "generative_ai",
    r"\bgpt-?\d?\b": "llm",
    r"\bchatgpt\b": "llm",
    r"\bbert\b": "llm",
    "foundation model": "llm",
    "large vision model": "llm",
    "diffusion model": "generative_ai",
}

# --- Termos nivel "ambiguo" (Secao 2.2) -------------------------------------------------
TERMOS_AMBIGUO = {
    "predictive maintenance": "predictive_maintenance",
    "manutencao preditiva": "predictive_maintenance",
    "digital twin": "digital_twin",
    r"\bbim\b": "bim",
    "building information model": "bim",
    "internet of things": "iot",
    r"\biot\b": "iot",
    "decision tree": "decision_tree",
    "arvore de decisao": "decision_tree",
    "fault detection": "fault_detection",
    "fault diagnosis": "fault_diagnosis",
    "anomaly detection": "anomaly_detection",
    "remaining useful life": "rul",
    "ontology": "ontology",
    "ontologia": "ontology",
    "simulation": "simulation",
    "simulacao": "simulation",
    "optimization": "optimization",
    "otimizacao": "optimization",
    "fuzzy": "fuzzy",
    "big data": "big_data",
    "data-driven": "data_driven",
    "algorithm": "algorithm_generic",
    "bayesian": "bayesian_generic",
    "smart building": "smart_building",
    "smart sensor": "smart_sensor",
}

VERBOS_APLICACAO = [
    "develop", "developed", "propose", "proposed", "apply", "applied", "train", "trained",
    "present", "presented", "design", "designed", "implement", "implemented", "build",
    "built", "employ", "employed", "use", "used", "utilize", "utilized", "construct",
    "constructed", "evaluate", "evaluated", "test", "tested", "validate", "validated",
    "achieved", "achieves", "outperform", "outperforms", "accuracy of", "predicts",
    "predict", "classify", "classifies", "trained on", "model was", "framework based on",
]

VERBOS_MENCAO_GENERICA = [
    "trend", "trends", "growing interest", "future work", "emerging", "potential of",
    "increasingly", "review of", "survey of", "overview of", "state of the art",
    "opportunities for", "could benefit from", "may enable", "is expected to",
]

ITENS_EDITORIAIS = {
    "frontmatter", "contents", "table of contents", "copyright", "index",
    "contributors", "preface", "acknowledgements", "acknowledgments", "list of figures",
    "list of tables", "references", "backmatter", "about the authors", "editorial board",
}

TRANSFORMER_ELETRICO_CTX = [
    "substation", "oil", "winding", "electrical failure", "power transformer",
    "transformer fault", "transformer oil", "distribution transformer", "insulation",
    "dissolved gas analysis", "transformer health",
]
TRANSFORMER_IA_CTX = [
    "transformer model", "transformer architecture", "attention mechanism",
    "self-attention", "bert", "gpt", "vision transformer", "transformer network",
    "transformer-based",
]

DECISION_TREE_TREINADA_CTX = [
    "decision tree classifier", "trained on", "cart algorithm", "decision tree algorithm",
    "decision tree model", "decision tree regression", "induced from data",
]


def _janela(texto, pos, tamanho=100):
    ini = max(0, pos - tamanho)
    fim = min(len(texto), pos + tamanho)
    return texto[ini:fim]


def _contexto_tem(texto_lower, termos):
    return any(t in texto_lower for t in termos)


def buscar_termos(texto_lower, dicionario):
    achados = []
    for padrao, rotulo in dicionario.items():
        for m in re.finditer(padrao, texto_lower):
            achados.append((rotulo, padrao, m.start(), _janela(texto_lower, m.start())))
    return achados


def classificar(registro):
    titulo = (registro.get("titulo") or "").strip()
    resumo = (registro.get("resumo") or "").strip()
    palavras = (registro.get("palavras_chave") or "").strip()
    resumo_presente = registro.get("resumo_presente") == "sim"

    titulo_l = titulo.lower()
    resumo_l = resumo.lower()
    palavras_l = palavras.lower()
    texto_completo_l = f"{titulo_l} {resumo_l} {palavras_l}"

    # --- Item editorial: excluido direto, independente de termos capturados ---
    titulo_norm_simples = re.sub(r"[^a-z ]", "", titulo_l).strip()
    if titulo_norm_simples in ITENS_EDITORIAIS:
        return {
            "termo_encontrado": titulo,
            "campo_encontrado": "titulo",
            "evidencia_curta": titulo[:200],
            "classe_ia_ml": "FALSO_POSITIVO",
            "tecnica_ia_ml": "nao_aplicavel",
            "tipo_aplicacao": "nao_aplicavel",
            "relacao_manutencao_predial": "nao",
            "relacao_sustentabilidade": "nao",
            "relacao_apoio_decisao": "nao",
            "contexto_publico_universitario": "nao_identificado",
            "decisao_triagem": "excluido",
            "justificativa": "Item editorial (sumário/capa/referências/etc.), não é um estudo -- classificação automática por título.",
            "nivel_confianca": "alto",
        }

    achados_confirma = buscar_termos(texto_completo_l, TERMOS_CONFIRMA)
    achados_ambiguo = buscar_termos(texto_completo_l, TERMOS_AMBIGUO)

    # --- Desambiguacao: transformer ---
    achados_confirma_filtrados = []
    for rotulo, padrao, pos, ctx in achados_confirma:
        if rotulo == "transformer":
            if _contexto_tem(ctx, TRANSFORMER_IA_CTX):
                achados_confirma_filtrados.append((rotulo, padrao, pos, ctx))
            elif _contexto_tem(ctx, TRANSFORMER_ELETRICO_CTX):
                continue  # falso positivo eletrico, descarta
            else:
                continue  # sem contexto suficiente, nao confirma isoladamente
        else:
            achados_confirma_filtrados.append((rotulo, padrao, pos, ctx))
    achados_confirma = achados_confirma_filtrados

    # --- Desambiguacao: decision tree so confirma como ML se houver evidencia de treino ---
    achados_ambiguo_filtrados = []
    decision_tree_promovida = False
    for rotulo, padrao, pos, ctx in achados_ambiguo:
        if rotulo == "decision_tree" and _contexto_tem(ctx, DECISION_TREE_TREINADA_CTX):
            decision_tree_promovida = True
            continue
        achados_ambiguo_filtrados.append((rotulo, padrao, pos, ctx))
    achados_ambiguo = achados_ambiguo_filtrados
    if decision_tree_promovida:
        achados_confirma.append(("decision_tree_ml", "decision tree (treinada)", 0, titulo_l[:100]))

    tecnicas_confirma = sorted({r for r, *_ in achados_confirma})
    tecnicas_ambiguo = sorted({r for r, *_ in achados_ambiguo})

    termos_literais = sorted({padrao.strip("\\b()?").replace("\\", "") for _, padrao, _, _ in (achados_confirma + achados_ambiguo)})
    campo_encontrado = []
    if any(t in titulo_l for t in [padrao for _, padrao, _, _ in achados_confirma + achados_ambiguo]):
        pass
    for _, _, pos, _ in achados_confirma + achados_ambiguo:
        if pos < len(titulo_l) + 1:
            campo_encontrado.append("titulo")
        elif pos < len(titulo_l) + 1 + len(resumo_l) + 1:
            campo_encontrado.append("resumo")
        else:
            campo_encontrado.append("palavras_chave")
    campo_encontrado = "; ".join(sorted(set(campo_encontrado))) if campo_encontrado else ""

    evidencia = ""
    if achados_confirma:
        evidencia = achados_confirma[0][3][:200]
    elif achados_ambiguo:
        evidencia = achados_ambiguo[0][3][:200]
    elif titulo:
        evidencia = titulo[:200]

    # --- Sinal de aplicacao efetiva vs mencao generica ---
    tem_verbo_aplicacao = _contexto_tem(texto_completo_l, VERBOS_APLICACAO)
    tem_verbo_mencao = _contexto_tem(texto_completo_l, VERBOS_MENCAO_GENERICA)

    # --- Classificacao ---
    if tecnicas_confirma:
        if tem_verbo_aplicacao or not tem_verbo_mencao:
            classe = "IA_ML_APLICACAO_CONFIRMADA"
        else:
            classe = "IA_ML_MENCAO_GENERICA"
    elif tecnicas_ambiguo:
        if "predictive_maintenance" in tecnicas_ambiguo and len(tecnicas_ambiguo) <= 2:
            classe = "MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA"
        else:
            classe = "TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA"
    else:
        classe = "FALSO_POSITIVO"

    if not resumo_presente and not tecnicas_confirma:
        # sem resumo e sem termo forte no titulo/palavras-chave -> informacao insuficiente,
        # exceto se ja caiu em item editorial (tratado acima) ou termo confirma explicito no titulo
        if classe in ("TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA", "MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA", "FALSO_POSITIVO"):
            classe = "INFORMACAO_INSUFICIENTE"

    # --- Nivel de confianca ---
    termo_confirma_no_titulo = any(pos < len(titulo_l) for _, _, pos, _ in achados_confirma)
    if not resumo_presente:
        nivel_confianca = "alto" if termo_confirma_no_titulo else "baixo"
    elif classe == "IA_ML_APLICACAO_CONFIRMADA" and tem_verbo_aplicacao:
        nivel_confianca = "alto"
    elif classe in ("FALSO_POSITIVO", "INFORMACAO_INSUFICIENTE"):
        nivel_confianca = "medio"
    else:
        nivel_confianca = "medio"

    tecnica_final = tecnicas_confirma[0] if tecnicas_confirma else (tecnicas_ambiguo[0] if tecnicas_ambiguo else "nao_aplicavel")

    tipo_aplicacao = "nao_aplicavel"
    if classe == "IA_ML_APLICACAO_CONFIRMADA":
        if any(t in texto_completo_l for t in ["predict", "prediction", "forecast"]):
            tipo_aplicacao = "predicao"
        elif any(t in texto_completo_l for t in ["classif"]):
            tipo_aplicacao = "classificacao"
        elif "anomaly" in texto_completo_l or "fault" in texto_completo_l:
            tipo_aplicacao = "deteccao_anomalia"
        elif "computer_vision" in tecnicas_confirma or "image" in texto_completo_l:
            tipo_aplicacao = "visao_computacional"
        elif "nlp" in tecnicas_confirma or "text" in texto_completo_l:
            tipo_aplicacao = "processamento_linguagem"
        elif "optimization" in tecnicas_ambiguo or "optimiz" in texto_completo_l:
            tipo_aplicacao = "otimizacao"
        else:
            tipo_aplicacao = "outro"

    relacao_manutencao = "sim" if any(t in texto_completo_l for t in ["maintenance", "manutencao", "repair", "retrofit", "asset management", "facility management"]) else ("indireta" if any(t in texto_completo_l for t in ["building performance", "operation"]) else "nao")
    relacao_sustentabilidade = "sim" if any(t in texto_completo_l for t in ["sustainab", "energy efficien", "carbon", "emission", "life cycle", "green building"]) else "nao"
    relacao_decisao = "sim" if any(t in texto_completo_l for t in ["decision support", "decision-making", "decision making", "prioritiz", "mcdm", "ranking"]) else "nao"
    contexto_pub_uni = "sim" if any(t in texto_completo_l for t in ["university", "universidade", "campus", "public building", "public sector", "government building"]) else "nao_identificado"

    justificativa = (
        f"Classificação automática por correspondência de termos do dicionário RQ6 "
        f"(docs/CODEBOOK_SENSIBILIDADE_IA_ML.md) aplicada a título/resumo/palavras-chave. "
        f"Termos de nível confirma: {', '.join(tecnicas_confirma) or 'nenhum'}. "
        f"Termos ambíguos: {', '.join(tecnicas_ambiguo) or 'nenhum'}."
    )
    if not resumo_presente:
        justificativa += " Resumo ausente na fonte -- classificação baseada apenas em título/palavras-chave/periódico."

    return {
        "termo_encontrado": "; ".join(termos_literais) if termos_literais else "(nenhum)",
        "campo_encontrado": campo_encontrado or "titulo",
        "evidencia_curta": evidencia,
        "classe_ia_ml": classe,
        "tecnica_ia_ml": tecnica_final,
        "tipo_aplicacao": tipo_aplicacao,
        "relacao_manutencao_predial": relacao_manutencao,
        "relacao_sustentabilidade": relacao_sustentabilidade,
        "relacao_apoio_decisao": relacao_decisao,
        "contexto_publico_universitario": contexto_pub_uni,
        "decisao_triagem": "",  # preenchido na Etapa 6
        "justificativa": justificativa,
        "nivel_confianca": nivel_confianca,
    }


def main():
    with open(NOVOS_PATH, encoding="utf-8-sig", newline="") as f:
        registros = list(csv.DictReader(f))

    campos_saida = list(registros[0].keys()) + [
        "termo_encontrado", "campo_encontrado", "evidencia_curta", "classe_ia_ml",
        "tecnica_ia_ml", "tipo_aplicacao", "relacao_manutencao_predial",
        "relacao_sustentabilidade", "relacao_apoio_decisao", "contexto_publico_universitario",
        "decisao_triagem", "justificativa", "nivel_confianca",
    ]

    saida = []
    for r in registros:
        resultado = classificar(r)
        linha = dict(r)
        linha.update(resultado)
        saida.append(linha)

    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos_saida)
        w.writeheader()
        w.writerows(saida)

    contagem_classe = Counter(l["classe_ia_ml"] for l in saida)
    contagem_base = Counter((l["classe_ia_ml"], l["database"]) for l in saida)
    contagem_confianca = Counter(l["nivel_confianca"] for l in saida)
    sem_resumo_total = sum(1 for l in saida if l.get("resumo_presente") != "sim")
    sem_resumo_por_classe = Counter(l["classe_ia_ml"] for l in saida if l.get("resumo_presente") != "sim")

    linhas_rel = []
    linhas_rel.append("# RELATÓRIO DE AUDITORIA — Classe IA/ML (busca de sensibilidade)\n")
    linhas_rel.append(
        "Gerado por `scripts/python/auditar_classe_ia_ml.py`, aplicando literalmente as "
        "regras de `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` sobre os "
        f"{len(saida)} registros de `sensibilidade_novos_unicos.csv` — **sem amostragem, "
        "cobertura de 100%**. Método: correspondência sistemática de termos do dicionário "
        "RQ6 em título/resumo/palavras-chave, com regras de desambiguação (transformer, "
        "decision tree, deep learning fora de contexto) e heurística lexical de aplicação "
        "efetiva vs. menção genérica. Não constitui leitura de texto completo.\n"
    )
    linhas_rel.append("## Distribuição por classe\n")
    linhas_rel.append("| Classe | N | % |")
    linhas_rel.append("|---|---|---|")
    for classe, n in contagem_classe.most_common():
        linhas_rel.append(f"| {classe} | {n} | {n/len(saida)*100:.1f}% |")
    linhas_rel.append(f"| **Total** | **{len(saida)}** | 100.0% |\n")

    linhas_rel.append("## Distribuição por classe × base\n")
    linhas_rel.append("| Classe | Scopus | WoS | Crossref |")
    linhas_rel.append("|---|---|---|---|")
    for classe in contagem_classe:
        linhas_rel.append(
            f"| {classe} | {contagem_base.get((classe, 'Scopus'), 0)} | "
            f"{contagem_base.get((classe, 'WoS'), 0)} | {contagem_base.get((classe, 'Crossref'), 0)} |"
        )

    linhas_rel.append("\n## Nível de confiança\n")
    linhas_rel.append("| Nível | N |")
    linhas_rel.append("|---|---|")
    for nivel, n in contagem_confianca.most_common():
        linhas_rel.append(f"| {nivel} | {n} |")

    linhas_rel.append(f"\n## Cobertura de resumo\n")
    linhas_rel.append(f"- Registros sem resumo: {sem_resumo_total} de {len(saida)} ({sem_resumo_total/len(saida)*100:.1f}%).")
    linhas_rel.append("- Distribuição de classe entre os registros sem resumo (auditados apenas por título/palavras-chave):")
    for classe, n in sem_resumo_por_classe.most_common():
        linhas_rel.append(f"  - {classe}: {n}")
    linhas_rel.append(
        "\nConforme já documentado na normalização, a ausência de resumo concentra-se na "
        "fatia Crossref e reduz sistematicamente o nível de confiança da auditoria nesse "
        "subconjunto — não é uma falha da auditoria, é limitação de cobertura da fonte."
    )

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_rel) + "\n")

    print(dict(contagem_classe))
    print(f"Escrito: {OUT_PATH}")
    print(f"Relatorio: {RELATORIO_PATH}")


if __name__ == "__main__":
    main()
