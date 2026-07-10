"""
Script de priorizacao da leitura full-text (adendo da ETAPA_11 -- SINTESE_TEMATICA_PRELIMINAR).

Nao le nenhum texto completo. Gera apenas a ORDEM em que os 3.678 registros do nucleo revisado
deveriam ser lidos integralmente numa etapa futura, a partir de
07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv.

Criterio de priorizacao (decisao registrada em 00_CONTROLE/DECISOES_METODOLOGICAS.md, entrada de
2026-07-09): o objetivo geral e os objetivos especificos do artigo
(ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt, secao 4) exigem mapeamento amplo da producao cientifica,
nao a leitura exaustiva de um unico eixo tematico antes dos outros -- ODS/ESG e MCDM/TOPSIS sao
instrumentos, nao o foco central (roteiro, secao 1 e CONTEXTO_CURTO_ARTIGO.md). Por isso, a fila
de leitura intercala os 5 eixos tematicos preliminares de forma proporcional ao tamanho de cada
grupo (metodo de alocacao proporcional tipo "maior resto/fila justa": a cada posicao da fila,
escolhe-se o eixo cujo proximo item deixaria a proporcao lida mais proxima da proporcao real do
eixo no nucleo). Isso garante que qualquer prefixo da fila (por exemplo, os primeiros 100 ou 500
registros lidos) já tenha representacao proporcional dos 5 eixos -- e portanto dos objetivos
especificos 2 a 5, que mapeiam nesses eixos (ver ESTADO_ATUAL.md, secao ETAPA_11).

Ordenacao interna de cada eixo (antes de intercalar): por ano decrescente, depois por titulo em
ordem alfabetica -- deterministico, sem uso de aleatoriedade, para reprodutibilidade.

Saidas:
- 07_SINTESE_TEMATICA/fila_priorizacao_leitura_full_text.csv
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATRIZ_PATH = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA", "matriz_sintese_tematica_preliminar.csv")
OUT_DIR = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA")
FILA_PATH = os.path.join(OUT_DIR, "fila_priorizacao_leitura_full_text.csv")

TAMANHO_LOTE = 100


def ano_para_ordenacao(valor):
    try:
        return -int(valor)
    except (TypeError, ValueError):
        return 0


def main():
    with open(MATRIZ_PATH, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))

    total = len(linhas)

    grupos = {}
    for linha in linhas:
        eixo = linha["eixo_tematico_preliminar"]
        grupos.setdefault(eixo, []).append(linha)

    for eixo, itens in grupos.items():
        itens.sort(key=lambda l: (ano_para_ordenacao(l.get("ano", "")), l.get("titulo", "")))

    filas = {eixo: list(itens) for eixo, itens in grupos.items()}
    tamanhos = {eixo: len(itens) for eixo, itens in grupos.items()}
    selecionados = {eixo: 0 for eixo in grupos}

    ordem_final = []
    while len(ordem_final) < total:
        eixo_escolhido = min(
            (eixo for eixo in grupos if filas[eixo]),
            key=lambda eixo: (selecionados[eixo] + 1) / tamanhos[eixo],
        )
        item = filas[eixo_escolhido].pop(0)
        selecionados[eixo_escolhido] += 1
        ordem_final.append(item)

    with open(FILA_PATH, "w", encoding="utf-8-sig", newline="") as f:
        campos = [
            "ordem_prioridade", "lote_leitura", "id_unico", "doi", "titulo", "ano",
            "eixo_tematico_preliminar", "metodo_mcdm_especifico", "tecnologia_especifica",
            "necessita_leitura_completa",
        ]
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for i, item in enumerate(ordem_final, start=1):
            w.writerow({
                "ordem_prioridade": i,
                "lote_leitura": (i - 1) // TAMANHO_LOTE + 1,
                "id_unico": item["id_unico"],
                "doi": item["doi"],
                "titulo": item["titulo"],
                "ano": item["ano"],
                "eixo_tematico_preliminar": item["eixo_tematico_preliminar"],
                "metodo_mcdm_especifico": item["metodo_mcdm_especifico"],
                "tecnologia_especifica": item["tecnologia_especifica"],
                "necessita_leitura_completa": item["necessita_leitura_completa"],
            })

    n_lotes = (total - 1) // TAMANHO_LOTE + 1

    # Validacao de proporcionalidade: composicao do eixo nos primeiros 100, 500 e 1000 da fila.
    print(f"Total na fila: {total} (esperado: {len(linhas)})")
    print(f"Numero de lotes de {TAMANHO_LOTE}: {n_lotes}")
    for corte in (100, 500, 1000, total):
        prefixo = ordem_final[:corte]
        cont = {}
        for item in prefixo:
            e = item["eixo_tematico_preliminar"]
            cont[e] = cont.get(e, 0) + 1
        print(f"Composicao dos primeiros {corte}:")
        for eixo, n in sorted(cont.items(), key=lambda kv: -kv[1]):
            print(f"  {eixo}: {n} ({100*n/corte:.1f}%)")


if __name__ == "__main__":
    main()
