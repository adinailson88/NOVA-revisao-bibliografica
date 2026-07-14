"""
Deduplicacao em 3 camadas da busca de sensibilidade IA/ML (2026-07-12):
(a) intra-base, (b) entre as 3 bases, (c) contra 03_PROCESSADOS/corpus_consolidado.csv.

Cascata: DOI normalizado -> EID/accession -> titulo exato -> titulo aproximado
(com blocking por palavra rara + confirmacao por ano/autor/periodico) -> classificacao.

(a)+(b) sao resolvidos numa unica passada de uniao-e-busca sobre o conjunto combinado dos
6728 registros normalizados da sensibilidade (mesma abordagem de consolidar_deduplicar.py:
DOI/titulo exato agrupam registros de qualquer base). A comparacao aproximada de titulo,
dentro do proprio conjunto de sensibilidade e contra o corpus, usa um indice invertido por
palavra rara (blocking) para evitar O(n*m) ingenuo em ~6700 x ~9500 registros.

Entrada:
- 03_PROCESSADOS/registros_normalizados_sensibilidade_ia.csv
- 03_PROCESSADOS/corpus_consolidado.csv

Saida (em 03_PROCESSADOS/):
- sensibilidade_dedup_classificacao.csv
- sensibilidade_ja_existia_corpus.csv
- sensibilidade_novos_unicos.csv
- sensibilidade_duplicatas_requerem_revisao.csv
- relatorio_deduplicacao_sensibilidade.md
"""

import csv
import os
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")

SENS_PATH = os.path.join(PROC_DIR, "registros_normalizados_sensibilidade_ia.csv")
CORPUS_PATH = os.path.join(PROC_DIR, "corpus_consolidado.csv")

OUT_CLASS = os.path.join(PROC_DIR, "sensibilidade_dedup_classificacao.csv")
OUT_JA_EXISTIA = os.path.join(PROC_DIR, "sensibilidade_ja_existia_corpus.csv")
OUT_NOVOS = os.path.join(PROC_DIR, "sensibilidade_novos_unicos.csv")
OUT_DUVIDA = os.path.join(PROC_DIR, "sensibilidade_duplicatas_requerem_revisao.csv")
OUT_RELATORIO = os.path.join(PROC_DIR, "relatorio_deduplicacao_sensibilidade.md")

TITULO_MIN_LEN = 8
TITULO_APROX_THRESHOLD = 0.90
STOPWORDS = {
    "the", "a", "an", "of", "in", "on", "for", "and", "or", "to", "with", "by", "from",
    "based", "using", "study", "case", "review", "analysis", "approach", "framework",
    "system", "systems", "building", "buildings", "maintenance", "management", "toward",
    "towards", "into", "via", "new", "development", "research",
}


def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def palavras_raras(titulo_norm):
    """Retorna as palavras de titulo_norm com >=5 caracteres, fora da stoplist,
    usadas como chave de blocking para achar candidatos aproximados sem comparar tudo com tudo."""
    return [p for p in titulo_norm.split() if len(p) >= 5 and p not in STOPWORDS]


def sobrenomes(autores_str):
    """Extrai um conjunto aproximado de sobrenomes a partir do campo de autores (formatos
    variados entre bases: 'Silva, J.; Souza, A.' ou 'Silva J., Souza A.' ou 'John Silva')."""
    if not autores_str:
        return set()
    partes = [p.strip() for p in autores_str.replace(" and ", ";").split(";") if p.strip()]
    nomes = set()
    for p in partes:
        p = p.split(",")[0].strip()
        p = p.split(".")[0].strip()
        tokens = [t for t in p.split() if len(t) >= 3]
        if tokens:
            nomes.add(tokens[-1].lower() if "," in p or len(tokens) == 1 else tokens[0].lower())
            nomes.add(tokens[0].lower())
    return nomes


class UniaoConjuntos:
    def __init__(self, n):
        self.pai = list(range(n))

    def encontrar(self, x):
        while self.pai[x] != x:
            self.pai[x] = self.pai[self.pai[x]]
            x = self.pai[x]
        return x

    def unir(self, a, b):
        ra, rb = self.encontrar(a), self.encontrar(b)
        if ra != rb:
            self.pai[ra] = rb


def dedup_exato(registros):
    """Uniao-e-busca por DOI normalizado e por titulo normalizado exato (>=8 chars),
    igual a consolidar_deduplicar.py::deduplicar -- resolve intra-base e entre bases
    numa unica passada, ja que o conjunto de entrada mistura as 3 bases."""
    n = len(registros)
    uf = UniaoConjuntos(n)

    por_doi = defaultdict(list)
    for i, r in enumerate(registros):
        if r["doi_norm"]:
            por_doi[r["doi_norm"]].append(i)
    for indices in por_doi.values():
        for i in indices[1:]:
            uf.unir(indices[0], i)

    por_titulo = defaultdict(list)
    for i, r in enumerate(registros):
        if r["titulo_norm"] and len(r["titulo_norm"]) >= TITULO_MIN_LEN:
            por_titulo[r["titulo_norm"]].append(i)
    for indices in por_titulo.values():
        if len(indices) < 2:
            continue
        dois_presentes = {registros[i]["doi_norm"] for i in indices if registros[i]["doi_norm"]}
        if len(dois_presentes) <= 1:
            for i in indices[1:]:
                uf.unir(indices[0], i)
        # se houver DOIs diferentes no mesmo titulo, nao funde automaticamente (mesma regra
        # do pipeline original) -- fica para a camada de titulo aproximado/revisao decidir.

    grupos = defaultdict(list)
    for i in range(n):
        grupos[uf.encontrar(i)].append(i)
    return list(grupos.values())


def indice_invertido(titulos_norm):
    idx = defaultdict(list)
    for pos, t in enumerate(titulos_norm):
        for palavra in set(palavras_raras(t)):
            idx[palavra].append(pos)
    return idx


def candidatos_aproximados(titulo_norm, idx):
    candidatos = set()
    for palavra in palavras_raras(titulo_norm):
        candidatos.update(idx.get(palavra, []))
    return candidatos


def confirmar_par(rep_a, rep_b):
    """Confirmacao por ano (+-1) OU sobrenome de autor em comum OU periodico em comum,
    para reduzir falso positivo do titulo aproximado."""
    ano_a, ano_b = rep_a.get("ano") or rep_a.get("ano_corpus"), rep_b.get("ano") or rep_b.get("ano_corpus")
    try:
        if ano_a and ano_b and abs(int(ano_a) - int(ano_b)) <= 1:
            return True
    except ValueError:
        pass
    aut_a = sobrenomes(rep_a.get("autores", ""))
    aut_b = sobrenomes(rep_b.get("autores", ""))
    if aut_a and aut_b and (aut_a & aut_b):
        return True
    per_a = (rep_a.get("fonte_periodico") or "").strip().lower()
    per_b = (rep_b.get("fonte_periodico") or "").strip().lower()
    if per_a and per_b and per_a == per_b:
        return True
    return False


def escolher_representante(registros, indices):
    """Prefere o registro com resumo mais longo; empate por titulo mais longo."""
    melhor = max(indices, key=lambda i: (len(registros[i].get("resumo") or ""), len(registros[i].get("titulo") or "")))
    return melhor


def escrever_csv(caminho, campos, linhas):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)


def main():
    sens = ler_csv(SENS_PATH)
    corpus = ler_csv(CORPUS_PATH)

    # --- Camada (a)+(b): dedup exato intra+entre-bases dentro do conjunto de sensibilidade ---
    grupos_exatos = dedup_exato(sens)

    # Teste de sanidade: a dedup intra-Crossref por DOI deve encontrar as 7 duplicatas ja
    # conhecidas (2000 linhas Crossref -> 1993 unicos so considerando DOI dentro do Crossref).
    crossref_indices = [i for i, r in enumerate(sens) if r["database"] == "Crossref"]
    doi_crossref = Counter(sens[i]["doi_norm"] for i in crossref_indices if sens[i]["doi_norm"])
    duplicatas_crossref_doi = sum(c - 1 for c in doi_crossref.values() if c > 1)

    # --- Camada de titulo aproximado dentro do conjunto de sensibilidade (registros que a
    # dedup exata NAO uniu) ---
    representantes = []  # 1 entrada por grupo exato, guarda indices originais do grupo
    for grupo in grupos_exatos:
        rep_i = escolher_representante(sens, grupo)
        representantes.append({"grupo": grupo, "rep_i": rep_i})

    titulos_rep = [sens[r["rep_i"]]["titulo_norm"] for r in representantes]
    idx_sens = indice_invertido(titulos_rep)

    uf_rep = UniaoConjuntos(len(representantes))
    duvidas_intra_sens = []
    for a in range(len(representantes)):
        titulo_a = titulos_rep[a]
        if len(titulo_a) < 15:
            continue
        for b in candidatos_aproximados(titulo_a, idx_sens):
            if b <= a:
                continue
            titulo_b = titulos_rep[b]
            ratio = SequenceMatcher(None, titulo_a, titulo_b).ratio()
            if ratio >= TITULO_APROX_THRESHOLD:
                rep_a_reg = sens[representantes[a]["rep_i"]]
                rep_b_reg = sens[representantes[b]["rep_i"]]
                doi_a, doi_b = rep_a_reg["doi_norm"], rep_b_reg["doi_norm"]
                if doi_a and doi_b and doi_a != doi_b:
                    continue  # DOIs diferentes e ambos presentes -> nunca funde automaticamente
                if confirmar_par(rep_a_reg, rep_b_reg):
                    uf_rep.unir(a, b)
                else:
                    duvidas_intra_sens.append((a, b, ratio))

    grupos_rep2 = defaultdict(list)
    for i in range(len(representantes)):
        grupos_rep2[uf_rep.encontrar(i)].append(i)

    unicos_sensibilidade = []
    for raiz, idxs_rep in grupos_rep2.items():
        indices_originais = []
        for ir in idxs_rep:
            indices_originais.extend(representantes[ir]["grupo"])
        rep_final = escolher_representante(sens, indices_originais)
        unicos_sensibilidade.append({
            "indices_originais": indices_originais,
            "rep": sens[rep_final],
        })

    # --- Camada (c): contra corpus_consolidado.csv ---
    corpus_por_doi = {}
    corpus_por_titulo = defaultdict(list)
    for c in corpus:
        doi_c = (c.get("doi") or "").strip().lower()
        if doi_c:
            corpus_por_doi.setdefault(doi_c, c["id_unico"])
        tnorm = _normalizar_titulo_local(c.get("titulo") or "")
        c["_titulo_norm"] = tnorm
        if tnorm and len(tnorm) >= TITULO_MIN_LEN:
            corpus_por_titulo[tnorm].append(c)

    titulos_corpus = [c["_titulo_norm"] for c in corpus]
    idx_corpus = indice_invertido(titulos_corpus)

    linhas_classificacao = []
    ja_existia = []
    novos = []
    duvidas_corpus = []

    for grupo in unicos_sensibilidade:
        rep = grupo["rep"]
        doi_norm = rep["doi_norm"]
        titulo_norm = rep["titulo_norm"]
        classe = None
        match_id = ""
        motivo_match = ""

        if doi_norm and doi_norm in corpus_por_doi:
            classe = "JA_EXISTIA_NO_CORPUS"
            match_id = corpus_por_doi[doi_norm]
            motivo_match = "doi_exato"
        elif titulo_norm and titulo_norm in corpus_por_titulo:
            candidatos = corpus_por_titulo[titulo_norm]
            dois_candidatos = {c.get("doi", "").strip().lower() for c in candidatos if c.get("doi")}
            if doi_norm and dois_candidatos and doi_norm not in dois_candidatos:
                duvidas_corpus.append((rep, candidatos[0], "titulo_exato_doi_diferente"))
                classe = "DUPLICATA_PROVAVEL_REQUER_REVISAO"
            else:
                classe = "JA_EXISTIA_NO_CORPUS"
                match_id = candidatos[0]["id_unico"]
                motivo_match = "titulo_exato"
        else:
            melhor_ratio, melhor_c = 0.0, None
            if titulo_norm and len(titulo_norm) >= 15:
                for pos in candidatos_aproximados(titulo_norm, idx_corpus):
                    ratio = SequenceMatcher(None, titulo_norm, titulos_corpus[pos]).ratio()
                    if ratio > melhor_ratio:
                        melhor_ratio, melhor_c = ratio, corpus[pos]
            if melhor_c and melhor_ratio >= TITULO_APROX_THRESHOLD:
                doi_c = (melhor_c.get("doi") or "").strip().lower()
                if doi_norm and doi_c and doi_norm != doi_c:
                    pass  # DOIs diferentes -> nao considera match, cai para NOVO/SEM_ID abaixo
                elif confirmar_par(rep, {"ano": melhor_c.get("ano"), "autores": melhor_c.get("autores"), "fonte_periodico": melhor_c.get("fonte_periodico")}):
                    classe = "JA_EXISTIA_NO_CORPUS"
                    match_id = melhor_c["id_unico"]
                    motivo_match = f"titulo_aproximado_{melhor_ratio:.2f}_confirmado"
                else:
                    classe = "DUPLICATA_PROVAVEL_REQUER_REVISAO"
                    duvidas_corpus.append((rep, melhor_c, f"titulo_aproximado_{melhor_ratio:.2f}_nao_confirmado"))

        if classe is None:
            if doi_norm:
                classe = "NOVO_POR_DOI"
            elif titulo_norm and len(titulo_norm) >= TITULO_MIN_LEN:
                classe = "NOVO_POR_TITULO"
            else:
                classe = "SEM_IDENTIFICADOR_SUFICIENTE"

        linha = {
            "id_sensibilidade": rep["id_sensibilidade"],
            "database": rep["database"],
            "string_id": rep["string_id"],
            "titulo": rep["titulo"],
            "doi": rep["doi"],
            "ano": rep["ano"],
            "n_registros_agrupados_sensibilidade": len(grupo["indices_originais"]),
            "ids_sensibilidade_agrupados": "|".join(sens[i]["id_sensibilidade"] for i in grupo["indices_originais"]),
            "classe": classe,
            "match_corpus_id": match_id,
            "motivo_match": motivo_match,
        }
        linhas_classificacao.append(linha)
        if classe == "JA_EXISTIA_NO_CORPUS":
            ja_existia.append(linha)
        elif classe in ("NOVO_POR_DOI", "NOVO_POR_TITULO", "SEM_IDENTIFICADOR_SUFICIENTE"):
            novos.append({**linha, **{k: rep.get(k, "") for k in ["resumo", "palavras_chave", "autores", "fonte_periodico", "tipo_documento", "url", "citacoes", "idioma", "resumo_presente"]}})

    campos_class = ["id_sensibilidade", "database", "string_id", "titulo", "doi", "ano",
                     "n_registros_agrupados_sensibilidade", "ids_sensibilidade_agrupados",
                     "classe", "match_corpus_id", "motivo_match"]
    escrever_csv(OUT_CLASS, campos_class, linhas_classificacao)
    escrever_csv(OUT_JA_EXISTIA, campos_class, ja_existia)
    campos_novos = campos_class + ["resumo", "palavras_chave", "autores", "fonte_periodico", "tipo_documento", "url", "citacoes", "idioma", "resumo_presente"]
    escrever_csv(OUT_NOVOS, campos_novos, novos)

    campos_duvida = ["titulo_sensibilidade", "id_sensibilidade", "doi_sensibilidade",
                      "titulo_pareado", "id_pareado", "doi_pareado", "motivo"]
    linhas_duvida = []
    for a, b, ratio in duvidas_intra_sens:
        ra, rb = sens[representantes[a]["rep_i"]], sens[representantes[b]["rep_i"]]
        linhas_duvida.append({
            "titulo_sensibilidade": ra["titulo"], "id_sensibilidade": ra["id_sensibilidade"], "doi_sensibilidade": ra["doi"],
            "titulo_pareado": rb["titulo"], "id_pareado": rb["id_sensibilidade"], "doi_pareado": rb["doi"],
            "motivo": f"intra_sensibilidade_titulo_aproximado_{ratio:.2f}_nao_confirmado",
        })
    for rep, corpus_c, motivo in duvidas_corpus:
        linhas_duvida.append({
            "titulo_sensibilidade": rep["titulo"], "id_sensibilidade": rep["id_sensibilidade"], "doi_sensibilidade": rep["doi"],
            "titulo_pareado": corpus_c.get("titulo", ""), "id_pareado": corpus_c.get("id_unico", ""), "doi_pareado": corpus_c.get("doi", ""),
            "motivo": motivo,
        })
    escrever_csv(OUT_DUVIDA, campos_duvida, linhas_duvida)

    # --- Relatorio ---
    contagem_classes = Counter(l["classe"] for l in linhas_classificacao)
    linhas_rel = []
    linhas_rel.append("# RELATÓRIO DE DEDUPLICAÇÃO — Busca de sensibilidade IA/ML\n")
    linhas_rel.append(
        "Gerado por `scripts/python/deduplicar_sensibilidade_ia.py`. Cascata: DOI normalizado "
        "→ título exato → título aproximado (blocking por palavra rara, limiar "
        f"{TITULO_APROX_THRESHOLD}, confirmado por ano±1/autor/periódico) → contra "
        "`corpus_consolidado.csv`.\n"
    )
    linhas_rel.append("## Funil completo\n")
    linhas_rel.append("| Etapa | N |")
    linhas_rel.append("|---|---|")
    linhas_rel.append(f"| Bruto normalizado (entrada) | {len(sens)} |")
    linhas_rel.append(f"| Após dedup exata intra+entre-bases (DOI/título exato) | {len(grupos_exatos)} |")
    linhas_rel.append(f"| Após dedup por título aproximado dentro da sensibilidade | {len(unicos_sensibilidade)} |")
    linhas_rel.append(f"| Classificados JA_EXISTIA_NO_CORPUS | {contagem_classes.get('JA_EXISTIA_NO_CORPUS', 0)} |")
    linhas_rel.append(f"| Classificados NOVO_POR_DOI | {contagem_classes.get('NOVO_POR_DOI', 0)} |")
    linhas_rel.append(f"| Classificados NOVO_POR_TITULO | {contagem_classes.get('NOVO_POR_TITULO', 0)} |")
    linhas_rel.append(f"| Classificados SEM_IDENTIFICADOR_SUFICIENTE | {contagem_classes.get('SEM_IDENTIFICADOR_SUFICIENTE', 0)} |")
    linhas_rel.append(f"| Classificados DUPLICATA_PROVAVEL_REQUER_REVISAO | {contagem_classes.get('DUPLICATA_PROVAVEL_REQUER_REVISAO', 0)} |")
    linhas_rel.append(f"| **Novos únicos que seguem para auditoria de classe IA/ML** | **{len(novos)}** |\n")

    linhas_rel.append("## Teste de sanidade — duplicatas internas conhecidas do Crossref\n")
    linhas_rel.append(
        f"Duplicatas por DOI dentro do próprio Crossref (das 2000 linhas): **{duplicatas_crossref_doi}** "
        f"(esperado: 7, conforme já documentado pelo usuário nos metadados do arquivo fornecido).\n"
    )

    linhas_rel.append("## Casos que requerem revisão manual pontual\n")
    linhas_rel.append(
        f"- Dúvidas de título aproximado dentro do conjunto de sensibilidade (não confirmadas por "
        f"ano/autor/periódico): {len(duvidas_intra_sens)}.\n"
        f"- Dúvidas de possível duplicata contra o corpus original: {len(duvidas_corpus)}.\n"
        f"- Total em `sensibilidade_duplicatas_requerem_revisao.csv`: {len(linhas_duvida)}.\n"
    )

    linhas_rel.append("## Arquivos gerados\n")
    linhas_rel.append("- `sensibilidade_dedup_classificacao.csv` — todos os registros únicos com classificação.")
    linhas_rel.append("- `sensibilidade_ja_existia_corpus.csv` — subconjunto já presente no corpus original.")
    linhas_rel.append("- `sensibilidade_novos_unicos.csv` — subconjunto que segue para auditoria de classe IA/ML (Etapa 5).")
    linhas_rel.append("- `sensibilidade_duplicatas_requerem_revisao.csv` — pares ambíguos para revisão manual pontual.")

    with open(OUT_RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_rel) + "\n")

    print(f"Bruto: {len(sens)} | Unicos apos dedup exata+aproximada intra-sensibilidade: {len(unicos_sensibilidade)}")
    print(f"Duplicatas Crossref (DOI, esperado 7): {duplicatas_crossref_doi}")
    print(dict(contagem_classes))
    print(f"Novos para auditoria: {len(novos)}")
    print(f"Duvidas para revisao manual: {len(linhas_duvida)}")


def _normalizar_titulo_local(titulo):
    import re
    import unicodedata
    if not titulo:
        return ""
    t = unicodedata.normalize("NFKD", titulo)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


if __name__ == "__main__":
    main()
