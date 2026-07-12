"""
Forma o novo corpus consolidado (Etapa 7): corpus original elegivel + novos elegiveis da
busca de sensibilidade IA/ML - duplicatas - falsos positivos, preservando proveniencia.

Nao sobrescreve 03_PROCESSADOS/corpus_consolidado.csv (original, 9542 registros) -- gera uma
nova versao com os NOVOS registros unicos da sensibilidade que nao existiam no corpus
(sensibilidade_novos_unicos.csv, 4889 registros, todos com decisao de triagem), preservando
pertence_corpus_original / pertence_busca_sensibilidade_ia.

Saida: 03_PROCESSADOS/corpus_consolidado_v2_sensibilidade.csv
"""

import csv
import os
import sys

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")
TRIAGEM_DIR = os.path.join(BASE_DIR, "04_TRIAGEM")

CORPUS_PATH = os.path.join(PROC_DIR, "corpus_consolidado.csv")
TRIAGEM_PATH = os.path.join(TRIAGEM_DIR, "sensibilidade_triagem_final.csv")
OUT_PATH = os.path.join(PROC_DIR, "corpus_consolidado_v2_sensibilidade.csv")

CAMPOS_SAIDA = [
    "id_unico", "doi", "titulo", "ano", "autores", "fonte_periodico", "tipo_documento",
    "resumo", "palavras_chave", "bases_origem", "strings_origem", "n_registros_agrupados",
    "doi_presente", "resumo_presente", "resumo_enriquecido_manualmente", "ids_brutos_agrupados",
    "pertence_corpus_original", "pertence_busca_sensibilidade_ia", "classe_ia_ml",
    "decisao_triagem_sensibilidade",
]


def main():
    with open(CORPUS_PATH, encoding="utf-8-sig", newline="") as f:
        original = list(csv.DictReader(f))
    with open(TRIAGEM_PATH, encoding="utf-8-sig", newline="") as f:
        sensibilidade = list(csv.DictReader(f))

    linhas = []
    for r in original:
        linha = {k: r.get(k, "") for k in CAMPOS_SAIDA if k in r}
        linha["pertence_corpus_original"] = "sim"
        linha["pertence_busca_sensibilidade_ia"] = "nao"
        linha["classe_ia_ml"] = ""
        linha["decisao_triagem_sensibilidade"] = ""
        linhas.append(linha)

    proximo_id = max(int(r["id_unico"].split("_")[1]) for r in original) + 1
    for r in sensibilidade:
        novo_id = f"REG_{proximo_id:05d}"
        proximo_id += 1
        linha = {
            "id_unico": novo_id,
            "doi": r.get("doi", ""),
            "titulo": r.get("titulo", ""),
            "ano": r.get("ano", ""),
            "autores": r.get("autores", ""),
            "fonte_periodico": r.get("fonte_periodico", ""),
            "tipo_documento": r.get("tipo_documento", ""),
            "resumo": r.get("resumo", ""),
            "palavras_chave": r.get("palavras_chave", ""),
            "bases_origem": r.get("database", ""),
            "strings_origem": r.get("string_id", ""),
            "n_registros_agrupados": r.get("n_registros_agrupados_sensibilidade", "1"),
            "doi_presente": "sim" if r.get("doi") else "nao",
            "resumo_presente": r.get("resumo_presente", ""),
            "resumo_enriquecido_manualmente": "nao",
            "ids_brutos_agrupados": r.get("ids_sensibilidade_agrupados", r.get("id_sensibilidade", "")),
            "pertence_corpus_original": "nao",
            "pertence_busca_sensibilidade_ia": "sim",
            "classe_ia_ml": r.get("classe_ia_ml", ""),
            "decisao_triagem_sensibilidade": r.get("decisao_triagem", ""),
        }
        linhas.append(linha)

    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_SAIDA)
        w.writeheader()
        w.writerows(linhas)

    n_original = len(original)
    n_novos = len(sensibilidade)
    n_nucleo_sens = sum(1 for r in sensibilidade if r["decisao_triagem"] == "nucleo")
    n_secundario_sens = sum(1 for r in sensibilidade if r["decisao_triagem"] == "secundario")
    print(f"Corpus original: {n_original}")
    print(f"Novos da sensibilidade incorporados: {n_novos}")
    print(f"  - nucleo: {n_nucleo_sens}, secundario: {n_secundario_sens}")
    print(f"Total v2: {len(linhas)}")
    print(f"Escrito: {OUT_PATH}")


if __name__ == "__main__":
    main()
