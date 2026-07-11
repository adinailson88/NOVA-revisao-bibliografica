"""
Script da Etapa 9 (docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md, secao 15) -- avaliacao metodologica dos
estudos.

Classifica o desenho metodologico dos 104 estudos do nucleo final por casamento de frases-chave em
titulo + evidencia_curta_do_resumo (mesmo padrao ja usado em scripts/python/pre_triagem.py e
scripts/python/sintese_tematica_preliminar.py: regras explicitas, sem leitura de texto completo e
sem LLM para gerar o achado). Nao le PDF; usa apenas os campos documentais ja existentes em
latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv.

Categoria unica por registro, por ordem de prioridade documentada (permite reproducao):
1. revisao_bibliometrica -- autodeclarado como revisao/analise bibliometrica.
2. estudo_caso_empirico -- estudo de caso ou ambiente/instituicao real nomeados.
3. estudo_survey_percepcao -- levantamento, entrevista, questionario ou percepcao de stakeholders.
4. aplicacao_metodo_decisao_quantitativo -- metodo multicriterio, estocastico, de otimizacao ou de
   aprendizado de maquina nomeado explicitamente, sem caso empirico ou survey dominante.
5. estudo_simulacao_modelagem_digital -- simulacao, gemeo digital, modelo computacional ou BIM
   aplicado, sem metodo de decisao nomeado.
6. proposta_framework_conceitual -- proposta de framework/modelo conceitual, sem os sinais acima.
7. nao_classificavel_pelo_resumo -- nenhum sinal suficiente em titulo+evidencia.

Saidas:
- latex-artigo/fontes/tabela37_desenho_metodologico_nucleo_final_104.csv
- docs/RELATORIO_ETAPA_9.md (secao de dados; o relatorio completo da etapa e escrito a parte)
"""

import csv
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NUCLEO_PATH = os.path.join(BASE_DIR, "latex-artigo", "fontes", "nucleo_final_pos_auditoria_resumos.csv")
OUT_PATH = os.path.join(BASE_DIR, "latex-artigo", "fontes", "tabela37_desenho_metodologico_nucleo_final_104.csv")

REVISAO = [
    "systematic review", "literature review", "bibliometric analysis", "bibliometric review",
    "a review", "review of", "review on", "thematic review", "scoping review", "mixed review",
    "comprehensive review", "an overview of", "overview of key",
]
CASO_EMPIRICO = [
    "case study", "a case study", "case-study",
]
SURVEY = [
    "survey", "questionnaire", "interview", "perception of", "stakeholder", "stakeholders'",
    "perceived", "perceptions",
]
METODO_QUANTITATIVO = [
    "fuzzy", "ahp", "anp", "topsis", "multi-criteria", "multicriteria", "multi criteria",
    "mcdm", "mcda", "stochastic", "optimization", "optimisation", "delphi", "regression",
    "machine learning", "neural network", "vector autoregressive", "life cycle cost",
    "life-cycle cost", " lcc ", "lcca",
]
SIMULACAO_MODELAGEM = [
    "simulation", "digital twin", "digital twins", "building information model", " bim ",
    "computational model", "control strategy", "control logic",
]
FRAMEWORK = [
    "framework", "conceptual", "proposes", "propose a", "proposed model", "develop a",
    "development of a", "methodology for",
]


def normalizar(texto):
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\s+", " ", t)
    return f" {t.strip()} "


def contem_algum(texto_norm, termos):
    return any(t in texto_norm for t in termos)


def classificar(titulo, evidencia):
    texto_norm = normalizar(titulo) + normalizar(evidencia)
    if contem_algum(texto_norm, REVISAO):
        return "revisao_bibliometrica"
    if contem_algum(texto_norm, CASO_EMPIRICO):
        return "estudo_caso_empirico"
    if contem_algum(texto_norm, SURVEY):
        return "estudo_survey_percepcao"
    if contem_algum(texto_norm, METODO_QUANTITATIVO):
        return "aplicacao_metodo_decisao_quantitativo"
    if contem_algum(texto_norm, SIMULACAO_MODELAGEM):
        return "estudo_simulacao_modelagem_digital"
    if contem_algum(texto_norm, FRAMEWORK):
        return "proposta_framework_conceitual"
    return "nao_classificavel_pelo_resumo"


def main():
    with open(NUCLEO_PATH, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))

    if len(linhas) != 104:
        raise SystemExit(f"ERRO: nucleo final com {len(linhas)} registros; esperado 104.")

    saida = []
    for row in linhas:
        desenho = classificar(row.get("titulo", ""), row.get("evidencia_curta_do_resumo", ""))
        saida.append({
            "id_unico": row["id_unico"],
            "titulo": row["titulo"],
            "desenho_metodologico_classificado": desenho,
        })

    contagem = {}
    for r in saida:
        contagem[r["desenho_metodologico_classificado"]] = (
            contagem.get(r["desenho_metodologico_classificado"], 0) + 1
        )

    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["desenho_metodologico_classificado", "total_registros", "percentual_dos_104"])
        for k, v in sorted(contagem.items(), key=lambda kv: -kv[1]):
            w.writerow([k, v, f"{100*v/104:.1f}"])

    ids_path = os.path.join(BASE_DIR, "latex-artigo", "fontes", "tabela37_ids_por_desenho_nucleo_final_104.csv")
    por_categoria = {}
    for r in saida:
        por_categoria.setdefault(r["desenho_metodologico_classificado"], []).append(r["id_unico"])
    with open(ids_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["desenho_metodologico_classificado", "ids"])
        for k, v in sorted(por_categoria.items(), key=lambda kv: -len(kv[1])):
            w.writerow([k, ";".join(sorted(v))])

    print(f"Total classificado: {len(saida)}")
    for k, v in sorted(contagem.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v} ({100*v/104:.1f}%)")


if __name__ == "__main__":
    main()
