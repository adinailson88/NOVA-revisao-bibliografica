"""
Normaliza os 3 arquivos brutos da busca de sensibilidade IA/ML (2026-07-12) para o
schema comum solicitado, reaproveitando a logica de normalizacao de titulo/DOI de
scripts/python/consolidar_deduplicar.py.

Entrada:
- 02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/scopus/SCOPUS_A5_2009-2026.csv
- 02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/wos/WOS_NUCLEO_05_20260712_part{01,02}.ris
- 02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/crossref/crossref_ia_todos_resultados.csv

Saida:
- 03_PROCESSADOS/registros_normalizados_sensibilidade_ia.csv
- 03_PROCESSADOS/relatorio_normalizacao_sensibilidade_ia.md
"""

import csv
import os
import re
import sys
import unicodedata

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "busca_sensibilidade_ia_20260712")
OUT_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")

SCOPUS_PATH = os.path.join(RAW_DIR, "scopus", "SCOPUS_A5_2009-2026.csv")
WOS_PATHS = [
    os.path.join(RAW_DIR, "wos", "WOS_NUCLEO_05_20260712_part01.ris"),
    os.path.join(RAW_DIR, "wos", "WOS_NUCLEO_05_20260712_part02.ris"),
]
CROSSREF_PATH = os.path.join(RAW_DIR, "crossref", "crossref_ia_todos_resultados.csv")

NORMALIZADOS_PATH = os.path.join(OUT_DIR, "registros_normalizados_sensibilidade_ia.csv")
RELATORIO_PATH = os.path.join(OUT_DIR, "relatorio_normalizacao_sensibilidade_ia.md")

CAMPOS = [
    "id_sensibilidade", "database", "string_id", "arquivo_origem", "identificador_fonte",
    "eid", "wos_accession_number", "doi", "doi_norm", "titulo", "titulo_norm", "resumo",
    "palavras_chave", "autores", "ano", "fonte_periodico", "tipo_documento", "url",
    "citacoes", "idioma", "resumo_presente",
]

# Harmonizacao de tipo documental (mesmas 3 categorias usadas no nucleo final --
# latex-artigo/fontes/tabela34_tipos_documentais_harmonizados_nucleo_final_104.csv):
# "Artigo de periodico", "Trabalho em evento", "Livro ou serie de livro". Tipos fora
# desse dominio ficam com o rotulo original entre colchetes para revisao manual.
HARMONIZACAO_TIPO = {
    # Scopus (Document Type)
    "article": "Artigo de periodico",
    "article in press": "Artigo de periodico",
    "review": "Artigo de periodico",
    "conference paper": "Trabalho em evento",
    "conference review": "Trabalho em evento",
    "book": "Livro ou serie de livro",
    "book chapter": "Livro ou serie de livro",
    "editorial": "Artigo de periodico",
    "note": "Artigo de periodico",
    "short survey": "Artigo de periodico",
    # WoS (TY)
    "jour": "Artigo de periodico",
    "cpaper": "Trabalho em evento",
    "conf": "Trabalho em evento",
    "book": "Livro ou serie de livro",
    "chap": "Livro ou serie de livro",
    # Crossref (type)
    "journal-article": "Artigo de periodico",
    "proceedings-article": "Trabalho em evento",
    "book-chapter": "Livro ou serie de livro",
    "book": "Livro ou serie de livro",
    "monograph": "Livro ou serie de livro",
    "reference-entry": "Livro ou serie de livro",
}


def harmonizar_tipo(tipo_original):
    if not tipo_original:
        return ""
    chave = tipo_original.strip().lower()
    harmonizado = HARMONIZACAO_TIPO.get(chave)
    return harmonizado if harmonizado else f"[nao_mapeado] {tipo_original.strip()}"


def normalizar_titulo(titulo):
    if not titulo:
        return ""
    t = unicodedata.normalize("NFKD", titulo)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def normalizar_doi(doi):
    if not doi:
        return ""
    d = doi.strip().lower()
    d = re.sub(r"^https?://(dx\.)?doi\.org/", "", d)
    d = re.sub(r"^doi:\s*", "", d)
    return d.strip().rstrip(".").strip()


def limpar_jats(texto):
    if not texto:
        return ""
    t = re.sub(r"</?jats:[a-zA-Z0-9]+[^>]*>", "", texto)
    return re.sub(r"\s+", " ", t).strip()


def extrair_ano(valor):
    if not valor:
        return ""
    m = re.search(r"(19|20)\d{2}", str(valor))
    return m.group(0) if m else ""


# ---------------------------------------------------------------------------
# Scopus
# ---------------------------------------------------------------------------

def ler_scopus():
    registros = []
    nome_arquivo = os.path.basename(SCOPUS_PATH)
    with open(SCOPUS_PATH, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        for i, linha in enumerate(leitor):
            titulo = (linha.get("Title") or "").strip()
            doi = (linha.get("DOI") or "").strip()
            eid = (linha.get("EID") or "").strip()
            resumo = (linha.get("Abstract") or "").strip()
            registros.append({
                "id_sensibilidade": f"SENS_SCOPUS_{i:05d}",
                "database": "Scopus",
                "string_id": "scopus_nucleo_a5_sensibilidade_ia_ml",
                "arquivo_origem": nome_arquivo,
                "identificador_fonte": eid,
                "eid": eid,
                "wos_accession_number": "",
                "doi": doi,
                "doi_norm": normalizar_doi(doi),
                "titulo": titulo,
                "titulo_norm": normalizar_titulo(titulo),
                "resumo": resumo,
                "palavras_chave": (linha.get("Author Keywords") or "").strip(),
                "autores": (linha.get("Authors") or "").strip(),
                "ano": extrair_ano(linha.get("Year")),
                "fonte_periodico": (linha.get("Source title") or "").strip(),
                "tipo_documento": harmonizar_tipo(linha.get("Document Type")),
                "url": (linha.get("Link") or "").strip(),
                "citacoes": (linha.get("Cited by") or "").strip(),
                "idioma": (linha.get("Language of Original Document") or "").strip(),
                "resumo_presente": "sim" if resumo else "nao",
            })
    return registros


# ---------------------------------------------------------------------------
# WoS (RIS)
# ---------------------------------------------------------------------------

def parsear_ris(caminho):
    texto = open(caminho, encoding="utf-8-sig").read()
    linhas = texto.split("\n")
    registros = []
    atual = {}
    ultimo_tag = None
    padrao_tag = re.compile(r"^([A-Z0-9]{2})  -( (.*))?$")
    for linha in linhas:
        linha = linha.rstrip("\r")
        m = padrao_tag.match(linha)
        if m:
            tag, valor = m.group(1), (m.group(3) or "")
            if tag == "TY":
                atual = {}
            if tag == "ER":
                if atual:
                    registros.append(atual)
                atual = {}
                ultimo_tag = None
                continue
            if tag == "AU":
                atual.setdefault("AU", []).append(valor)
            else:
                atual[tag] = (atual.get(tag, "") + " " + valor).strip() if tag in atual else valor
            ultimo_tag = tag
        elif linha.strip() and ultimo_tag:
            if ultimo_tag != "AU":
                atual[ultimo_tag] = (atual.get(ultimo_tag, "") + " " + linha.strip()).strip()
    if atual:
        registros.append(atual)
    return registros


def ler_wos():
    registros = []
    for caminho in WOS_PATHS:
        nome_arquivo = os.path.basename(caminho)
        for i, r in enumerate(parsear_ris(caminho)):
            titulo = (r.get("TI") or "").strip()
            doi = (r.get("DO") or "").strip()
            an = (r.get("AN") or "").strip()
            resumo = (r.get("AB") or "").strip()
            registros.append({
                "id_sensibilidade": f"SENS_WOS_{nome_arquivo[-9:-4]}_{i:05d}",
                "database": "WoS",
                "string_id": "wos_nucleo_a5_sensibilidade_ia_ml",
                "arquivo_origem": nome_arquivo,
                "identificador_fonte": an,
                "eid": "",
                "wos_accession_number": an,
                "doi": doi,
                "doi_norm": normalizar_doi(doi),
                "titulo": titulo,
                "titulo_norm": normalizar_titulo(titulo),
                "resumo": resumo,
                "palavras_chave": (r.get("DE") or r.get("ID") or "").strip(),
                "autores": "; ".join(r.get("AU", [])),
                "ano": extrair_ano(r.get("PY")),
                "fonte_periodico": (r.get("T2") or r.get("JI") or "").strip(),
                "tipo_documento": harmonizar_tipo(r.get("TY")),
                "url": "",
                "citacoes": (r.get("TC") or "").strip(),
                "idioma": (r.get("LA") or "").strip(),
                "resumo_presente": "sim" if resumo else "nao",
            })
    return registros


# ---------------------------------------------------------------------------
# Crossref
# ---------------------------------------------------------------------------

def ler_crossref():
    registros = []
    nome_arquivo = os.path.basename(CROSSREF_PATH)
    with open(CROSSREF_PATH, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        for i, linha in enumerate(leitor):
            titulo = (linha.get("title") or "").strip()
            doi = (linha.get("doi") or "").strip()
            resumo = limpar_jats((linha.get("abstract") or "").strip())
            registros.append({
                "id_sensibilidade": f"SENS_CROSSREF_{i:05d}",
                "database": "Crossref",
                "string_id": (linha.get("string_id") or "").strip(),
                "arquivo_origem": nome_arquivo,
                "identificador_fonte": "",
                "eid": "",
                "wos_accession_number": "",
                "doi": doi,
                "doi_norm": normalizar_doi(doi),
                "titulo": titulo,
                "titulo_norm": normalizar_titulo(titulo),
                "resumo": resumo,
                "palavras_chave": (linha.get("subject") or "").strip(),
                "autores": (linha.get("author") or "").strip(),
                "ano": extrair_ano(linha.get("published")),
                "fonte_periodico": (linha.get("container_title") or "").strip(),
                "tipo_documento": harmonizar_tipo(linha.get("type")),
                "url": (linha.get("url") or "").strip(),
                "citacoes": (linha.get("is_referenced_by_count") or "").strip(),
                "idioma": (linha.get("language") or "").strip(),
                "resumo_presente": "sim" if resumo else "nao",
            })
    return registros


def escrever_csv(caminho, campos, linhas):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    scopus = ler_scopus()
    wos = ler_wos()
    crossref = ler_crossref()
    registros = scopus + wos + crossref

    escrever_csv(NORMALIZADOS_PATH, CAMPOS, registros)

    def stats(nome, lote):
        n = len(lote)
        com_doi = sum(1 for r in lote if r["doi_norm"])
        com_resumo = sum(1 for r in lote if r["resumo_presente"] == "sim")
        nao_mapeados = sum(1 for r in lote if r["tipo_documento"].startswith("[nao_mapeado]"))
        return n, com_doi, com_resumo, nao_mapeados

    linhas_rel = []
    linhas_rel.append("# RELATÓRIO DE NORMALIZAÇÃO — Busca de sensibilidade IA/ML\n")
    linhas_rel.append(
        "Gerado por `scripts/python/normalizar_sensibilidade_ia.py`. Três parsers dedicados "
        "(Scopus CSV, WoS RIS tag-a-tag, Crossref CSV) convergem para o schema comum de 21 "
        "campos. Reaproveita a mesma lógica de normalização de título/DOI de "
        "`consolidar_deduplicar.py`.\n"
    )
    linhas_rel.append("## Contagens de entrada/saída por base\n")
    linhas_rel.append("| Base | Registros | Com DOI | % DOI | Com resumo | % resumo | Tipo doc. não mapeado |")
    linhas_rel.append("|---|---|---|---|---|---|---|")
    total_n = total_doi = total_resumo = total_naomap = 0
    for nome, lote in [("Scopus", scopus), ("WoS", wos), ("Crossref", crossref)]:
        n, com_doi, com_resumo, nao_mapeados = stats(nome, lote)
        total_n += n
        total_doi += com_doi
        total_resumo += com_resumo
        total_naomap += nao_mapeados
        linhas_rel.append(
            f"| {nome} | {n} | {com_doi} | {com_doi/n*100:.1f}% | {com_resumo} | "
            f"{com_resumo/n*100:.1f}% | {nao_mapeados} |"
        )
    linhas_rel.append(
        f"| **Total** | **{total_n}** | **{total_doi}** | {total_doi/total_n*100:.1f}% | "
        f"**{total_resumo}** | {total_resumo/total_n*100:.1f}% | **{total_naomap}** |\n"
    )
    linhas_rel.append(
        "## Limitação conhecida\n\n"
        "A fatia Crossref apresenta ausência sistemática de resumo (a API do Crossref só "
        "retorna `abstract` quando o editor o submeteu — minoria dos registros). Isso é "
        "esperado e reduz a confiança da auditoria temática (Etapa 5) nessa fatia — registros "
        "sem resumo são auditados apenas por título/palavras-chave/periódico, com "
        "`nivel_confianca` rebaixado por definição salvo termo IA/ML inequívoco no próprio "
        "título. Não é uma falha de normalização, é uma limitação de cobertura da fonte.\n"
    )
    if total_naomap:
        tipos_naomap = sorted({r["tipo_documento"] for r in registros if r["tipo_documento"].startswith("[nao_mapeado]")})
        linhas_rel.append("## Tipos documentais não mapeados na harmonização\n")
        for t in tipos_naomap:
            linhas_rel.append(f"- {t}")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_rel) + "\n")

    print(f"Scopus: {len(scopus)}, WoS: {len(wos)}, Crossref: {len(crossref)}, total: {len(registros)}")
    print(f"Normalizados escritos em {NORMALIZADOS_PATH}")
    print(f"Relatorio escrito em {RELATORIO_PATH}")


if __name__ == "__main__":
    main()
