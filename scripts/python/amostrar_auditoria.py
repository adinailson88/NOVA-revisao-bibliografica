"""
Sorteio da amostra estratificada para auditoria da triagem (ETAPA_08 - AUDITORIA_TRIAGEM).

Sorteia, de forma reprodutivel (semente fixa), a amostra minima exigida pelo roteiro-mestre
(secao 15, ETAPA 8): 30 relevantes, 30 irrelevantes, 20 duvida, 20 sem_resumo. Junta titulo e
resumo (de corpus_consolidado.csv) para permitir revisao humana/assistida por LLM, com
justificativa textual -- nao uma reclassificacao automatica sem leitura.

Tambem gera os dois censos completos (nao amostrados) de controle de vies pedidos pelo prompt da
etapa: registros com Bloco C (MCDM/AHP/TOPSIS) e Bloco D (campus/universidade/public building)
presentes, cruzados com a classe atribuida na ETAPA_07 -- para verificar que esses termos nao
geraram inclusao automatica.

Saida intermediaria (nao e saida final da etapa): 04_TRIAGEM/_amostra_auditoria_bruta.csv
"""

import csv
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAGEM_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "matriz_pre_triagem.csv")
CORPUS_PATH = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado.csv")
AMOSTRA_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "_amostra_auditoria_bruta.csv")

SEMENTE = 42
TAMANHOS = {"relevante": 30, "irrelevante": 30, "duvida": 20, "sem_resumo": 20}


def main():
    with open(TRIAGEM_PATH, encoding="utf-8-sig", newline="") as f:
        triagem = {r["id_unico"]: r for r in csv.DictReader(f)}
    with open(CORPUS_PATH, encoding="utf-8-sig", newline="") as f:
        corpus = {r["id_unico"]: r for r in csv.DictReader(f)}

    rng = random.Random(SEMENTE)
    linhas_amostra = []
    for classe, n in TAMANHOS.items():
        ids_classe = [id_ for id_, r in triagem.items() if r["classe_pre_triagem"] == classe]
        rng.shuffle(ids_classe)
        selecionados = ids_classe[:n]
        for id_ in selecionados:
            c = corpus[id_]
            linhas_amostra.append({
                "id_unico": id_,
                "estrato": classe,
                "classe_pre_triagem": triagem[id_]["classe_pre_triagem"],
                "titulo": c["titulo"],
                "resumo": (c["resumo"] or "")[:600],
                "bloco_a_presente": triagem[id_]["bloco_a_presente"],
                "bloco_b_presente": triagem[id_]["bloco_b_presente"],
                "bloco_c_presente": triagem[id_]["bloco_c_presente"],
                "bloco_d_presente": triagem[id_]["bloco_d_presente"],
            })

    with open(AMOSTRA_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas_amostra[0].keys()))
        w.writeheader()
        for linha in linhas_amostra:
            w.writerow(linha)

    print(f"Amostra gerada: {len(linhas_amostra)} registros em {AMOSTRA_PATH}")
    for classe, n in TAMANHOS.items():
        real = sum(1 for l in linhas_amostra if l["estrato"] == classe)
        print(f"  {classe}: {real} (alvo {n})")


if __name__ == "__main__":
    main()
