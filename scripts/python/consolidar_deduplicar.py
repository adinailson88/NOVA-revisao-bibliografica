"""
Script de consolidacao e deduplicacao (ETAPA_06 - CONSOLIDAR_DEDUPLICAR).

Le os brutos ja coletados de Scopus (CSV), Crossref (CSV) e Web of Science (RIS manual),
padroniza os campos em um schema comum e deduplica por DOI normalizado e por titulo
normalizado, preservando proveniencia (bases_origem, strings_origem, ids brutos agrupados).

Regra vigente (01_PROTOCOLO/protocolo_busca_reprodutivel.md, secao 7): nunca apagar duplicata
sem preservar proveniencia. Conflitos (mesmo titulo normalizado, DOIs diferentes e ambos
presentes) NAO sao mesclados automaticamente -- ficam registrados para revisao manual, para
evitar fundir por engano dois trabalhos distintos.

Fontes lidas:
- 02_DADOS_BRUTOS/scopus/scopus_nucleo_a{1,2,3,4}_*_raw.csv (coleta via API, sem resumo --
  view=STANDARD nao traz dc:description)
- 02_DADOS_BRUTOS/scopus/SCOPUS_A{1,2,3,4}_*.csv (export manual do site da Scopus em 2026-07-09,
  com resumo -- usado para enriquecer os registros da API por EID; registros so encontrados no
  manual, e nao na API, tambem sao incluidos)
- 02_DADOS_BRUTOS/crossref/crossref_nucleo_a{1,2,3,4,5}_raw.csv
- 02_DADOS_BRUTOS/wos_manual/WOS_NUCLEO_0{1,2,3,4}_20260708_part01.ris

NAO le (deixados de lado por decisao do usuario -- strings incorretas, ver
00_CONTROLE/DECISOES_METODOLOGICAS.md, entradas de 2026-07-08 e 2026-07-09):
- 02_DADOS_BRUTOS/scopus/SCOPUS_NUCLEO_01-04_20260708_part01.csv.csv (A1 manual com string antiga,
  MCDM/ESG obrigatorio -- substituido pelos SCOPUS_A1_*.csv acima, com a string vigente)

Saidas:
- 03_PROCESSADOS/registros_normalizados.csv   (um registro por linha bruta, campos padronizados)
- 03_PROCESSADOS/corpus_consolidado.csv       (um registro por obra unica, pos-deduplicacao)
- 03_PROCESSADOS/duplicatas_detectadas.csv    (grupos de duplicatas, para auditoria)
- 03_PROCESSADOS/relatorio_deduplicacao.md    (relatorio objetivo, com contagens rastreaveis)
"""

import csv
import glob
import json
import os
import re
import sys
import unicodedata

# O export manual da Scopus inclui colunas muito longas (ex. "References", com centenas de
# citacoes por linha), que estouram o limite padrao do csv do Python (131072 bytes/campo).
csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPUS_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "scopus")
CROSSREF_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "crossref")
WOS_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "wos_manual")
OUT_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")

NORMALIZADOS_PATH = os.path.join(OUT_DIR, "registros_normalizados.csv")
CONSOLIDADO_PATH = os.path.join(OUT_DIR, "corpus_consolidado.csv")
DUPLICATAS_PATH = os.path.join(OUT_DIR, "duplicatas_detectadas.csv")
RELATORIO_PATH = os.path.join(OUT_DIR, "relatorio_deduplicacao.md")

NORM_FIELDS = [
    "id_registro", "database", "string_id", "identificador_fonte", "doi", "doi_norm",
    "titulo", "titulo_norm", "resumo", "ano", "autores", "fonte_periodico", "tipo_documento",
    "palavras_chave", "url", "citacoes", "idioma", "abstract_enriquecido_manualmente",
]

CONSOLIDADO_FIELDS = [
    "id_unico", "doi", "titulo", "ano", "autores", "fonte_periodico", "tipo_documento",
    "resumo", "palavras_chave", "bases_origem", "strings_origem", "n_registros_agrupados",
    "doi_presente", "resumo_presente", "resumo_enriquecido_manualmente", "ids_brutos_agrupados",
]

DUPLICATAS_FIELDS = [
    "id_unico", "criterio_agrupamento", "n_registros_agrupados", "bases_origem",
    "strings_origem", "titulos_originais", "ids_brutos_agrupados",
]


# ---------------------------------------------------------------------------
# Normalizacao de texto
# ---------------------------------------------------------------------------

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
    d = d.strip().rstrip(".").strip()
    return d


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
# Leitura das 3 bases
# ---------------------------------------------------------------------------

# Export manual do site da Scopus (via proxy institucional), feito em 2026-07-09 para suprir a
# ausencia de resumo na coleta via API (view=STANDARD nao traz dc:description -- tentativa de
# usar view=COMPLETE falhou com HTTP 401, chave sem entitlement mesmo em rede institucional; ver
# 00_CONTROLE/DECISOES_METODOLOGICAS.md). Strings usadas no site sao as mesmas de
# 01_PROTOCOLO/strings_nativas_por_base.md (confirmado com o usuario apos incidente com a string
# antiga da secao 9 do roteiro-mestre -- ver mesma entrada de decisoes). A1 foi particionado por
# ano no site (limite pratico de exportacao da Scopus); A2-A4 vieram inteiros.
#
# NAO confundir com os 4 CSVs antigos "SCOPUS_NUCLEO_01-04_20260708_part01.csv.csv" (prefixo
# diferente, "SCOPUS_NUCLEO_0X" em vez de "SCOPUS_AX_") -- esses usaram a string errada (com MCDM/
# ESG obrigatorio) e continuam fora de uso, nao sao lidos por este script.
SCOPUS_MANUAL_GLOB_POR_STRING = {
    "scopus_nucleo_a1_manutencao_sustentabilidade": "SCOPUS_A1_*.csv",
    "scopus_nucleo_a2_contexto_publico_universitario": "SCOPUS_A2_*.csv",
    "scopus_nucleo_a3_priorizacao_estrategia_manutencao": "SCOPUS_A3_*.csv",
    "scopus_nucleo_a4_gestao_ativos_ciclo_vida": "SCOPUS_A4_*.csv",
}


def _linha_manual_scopus(linha, string_id):
    titulo = (linha.get("Title") or "").strip()
    doi = (linha.get("DOI") or "").strip()
    return {
        "identificador_fonte": (linha.get("EID") or "").strip(),
        "doi": doi,
        "doi_norm": normalizar_doi(doi),
        "titulo": titulo,
        "titulo_norm": normalizar_titulo(titulo),
        "resumo": (linha.get("Abstract") or "").strip(),
        "ano": extrair_ano(linha.get("Year")),
        "autores": (linha.get("Authors") or "").strip(),
        "fonte_periodico": (linha.get("Source title") or "").strip(),
        "tipo_documento": (linha.get("Document Type") or "").strip(),
        "palavras_chave": (linha.get("Author Keywords") or "").strip(),
        "url": (linha.get("Link") or "").strip(),
        "citacoes": (linha.get("Cited by") or "").strip(),
        "idioma": (linha.get("Language of Original Document") or "").strip(),
        "string_id": string_id,
    }


def carregar_scopus_manual():
    """Retorna {string_id: {eid: linha_manual}} a partir dos exports do site da Scopus."""
    por_string = {}
    for string_id, padrao in SCOPUS_MANUAL_GLOB_POR_STRING.items():
        arquivos = sorted(glob.glob(os.path.join(SCOPUS_DIR, padrao)))
        por_eid = {}
        for caminho in arquivos:
            with open(caminho, encoding="utf-8-sig", newline="") as f:
                for linha in csv.DictReader(f):
                    dados = _linha_manual_scopus(linha, string_id)
                    eid = dados["identificador_fonte"]
                    if eid and eid not in por_eid:
                        por_eid[eid] = dados
        por_string[string_id] = por_eid
    return por_string


def ler_scopus():
    registros = []
    manual_por_string = carregar_scopus_manual()
    arquivos = sorted(glob.glob(os.path.join(SCOPUS_DIR, "scopus_nucleo_a*_raw.csv")))
    for caminho in arquivos:
        nome_base = os.path.basename(caminho)
        string_id_arquivo = nome_base.replace("_raw.csv", "")
        manual_desta_string = manual_por_string.get(string_id_arquivo, {})
        eids_vistos_na_api = set()
        with open(caminho, encoding="utf-8-sig", newline="") as f:
            leitor = csv.DictReader(f)
            for i, linha in enumerate(leitor):
                eid = (linha.get("eid") or "").strip()
                eids_vistos_na_api.add(eid)
                manual = manual_desta_string.get(eid)
                titulo = (linha.get("title") or "").strip()
                doi = (linha.get("doi") or "").strip()
                resumo = (manual["resumo"] if manual else "") or (linha.get("abstract") or "").strip()
                registros.append({
                    "id_registro": f"SCOPUS::{nome_base}::{i:05d}",
                    "database": "Scopus",
                    "string_id": (linha.get("string_id") or "").strip(),
                    "identificador_fonte": eid,
                    "doi": doi,
                    "doi_norm": normalizar_doi(doi),
                    "titulo": titulo,
                    "titulo_norm": normalizar_titulo(titulo),
                    "resumo": resumo,
                    "ano": extrair_ano(linha.get("year")),
                    "autores": (linha.get("author_names") or "").strip(),
                    "fonte_periodico": (linha.get("source_title") or "").strip(),
                    "tipo_documento": (linha.get("document_type") or "").strip(),
                    "palavras_chave": (manual["palavras_chave"] if manual else ""),
                    "url": (linha.get("url") or "").strip(),
                    "citacoes": (linha.get("citedby_count") or "").strip(),
                    "idioma": (manual["idioma"] if manual else ""),
                    "abstract_enriquecido_manualmente": "sim" if (manual and manual["resumo"]) else "nao",
                })

        # Registros que o export manual do site encontrou mas a coleta via API nao trouxe
        # (drift normal de indice entre datas de coleta diferentes) -- adicionados para nao
        # perder cobertura, com id_registro proprio para rastreabilidade.
        for j, (eid, manual) in enumerate(manual_desta_string.items()):
            if eid in eids_vistos_na_api:
                continue
            registros.append({
                "id_registro": f"SCOPUS_MANUAL_NOVO::{string_id_arquivo}::{j:05d}",
                "database": "Scopus",
                "string_id": string_id_arquivo,
                "identificador_fonte": eid,
                "doi": manual["doi"],
                "doi_norm": manual["doi_norm"],
                "titulo": manual["titulo"],
                "titulo_norm": manual["titulo_norm"],
                "resumo": manual["resumo"],
                "ano": manual["ano"],
                "autores": manual["autores"],
                "fonte_periodico": manual["fonte_periodico"],
                "tipo_documento": manual["tipo_documento"],
                "palavras_chave": manual["palavras_chave"],
                "url": manual["url"],
                "citacoes": manual["citacoes"],
                "idioma": manual["idioma"],
                "abstract_enriquecido_manualmente": "sim" if manual["resumo"] else "nao",
            })
    return registros


def ler_crossref():
    registros = []
    arquivos = sorted(glob.glob(os.path.join(CROSSREF_DIR, "crossref_nucleo_a*_raw.csv")))
    for caminho in arquivos:
        nome_base = os.path.basename(caminho)
        with open(caminho, encoding="utf-8-sig", newline="") as f:
            leitor = csv.DictReader(f)
            for i, linha in enumerate(leitor):
                titulo = (linha.get("title") or "").strip()
                doi = (linha.get("doi") or "").strip()
                registros.append({
                    "id_registro": f"CROSSREF::{nome_base}::{i:05d}",
                    "database": "Crossref",
                    "string_id": (linha.get("string_id") or "").strip(),
                    "identificador_fonte": "",
                    "doi": doi,
                    "doi_norm": normalizar_doi(doi),
                    "titulo": titulo,
                    "titulo_norm": normalizar_titulo(titulo),
                    "resumo": limpar_jats((linha.get("abstract") or "").strip()),
                    "ano": extrair_ano(linha.get("published")),
                    "autores": (linha.get("author") or "").strip(),
                    "fonte_periodico": (linha.get("container_title") or "").strip(),
                    "tipo_documento": (linha.get("type") or "").strip(),
                    "palavras_chave": (linha.get("subject") or "").strip(),
                    "url": (linha.get("url") or "").strip(),
                    "citacoes": (linha.get("is_referenced_by_count") or "").strip(),
                    "idioma": (linha.get("language") or "").strip(),
                    "abstract_enriquecido_manualmente": "nao",
                })
    return registros


def parsear_ris(caminho):
    """Parser tolerante para o formato RIS/EndNote exportado manualmente da WoS.
    Cada linha `TAG  - valor` inicia um campo; linhas sem esse padrao sao continuacao
    do ultimo campo aberto (comportamento padrao de RIS)."""
    texto = open(caminho, encoding="utf-8-sig").read()
    linhas = texto.split("\n")
    registros = []
    atual = {}
    ultimo_tag = None
    # O tracador "ER  -" de fim de registro nao tem valor apos o traco (sem espaco final),
    # por isso o valor apos "TAG  -" e opcional aqui (diferente do restante das tags).
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
            if ultimo_tag == "AU":
                pass
            else:
                atual[ultimo_tag] = (atual.get(ultimo_tag, "") + " " + linha.strip()).strip()
    if atual:
        registros.append(atual)
    return registros


def ler_wos():
    registros = []
    arquivos = sorted(glob.glob(os.path.join(WOS_DIR, "WOS_NUCLEO_*.ris")))
    for caminho in arquivos:
        nome_base = os.path.basename(caminho)
        string_id = nome_base.split("_20260708")[0].lower()
        for i, r in enumerate(parsear_ris(caminho)):
            titulo = (r.get("TI") or "").strip()
            doi = (r.get("DO") or "").strip()
            registros.append({
                "id_registro": f"WOS::{nome_base}::{i:05d}",
                "database": "WoS",
                "string_id": string_id,
                "identificador_fonte": (r.get("AN") or "").strip(),
                "doi": doi,
                "doi_norm": normalizar_doi(doi),
                "titulo": titulo,
                "titulo_norm": normalizar_titulo(titulo),
                "resumo": (r.get("AB") or "").strip(),
                "ano": extrair_ano(r.get("PY")),
                "autores": "; ".join(r.get("AU", [])),
                "fonte_periodico": (r.get("T2") or "").strip(),
                "tipo_documento": (r.get("TY") or "").strip(),
                "palavras_chave": (r.get("KW") or "").strip(),
                "url": "",
                "citacoes": "",
                "idioma": (r.get("LA") or "").strip(),
                "abstract_enriquecido_manualmente": "nao",
            })
    return registros


# ---------------------------------------------------------------------------
# Union-Find para deduplicacao
# ---------------------------------------------------------------------------

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


def deduplicar(registros):
    n = len(registros)
    uf = UniaoConjuntos(n)

    por_doi = {}
    for i, r in enumerate(registros):
        if r["doi_norm"]:
            por_doi.setdefault(r["doi_norm"], []).append(i)
    for indices in por_doi.values():
        for i in indices[1:]:
            uf.unir(indices[0], i)

    por_titulo = {}
    for i, r in enumerate(registros):
        if r["titulo_norm"] and len(r["titulo_norm"]) >= 8:
            por_titulo.setdefault(r["titulo_norm"], []).append(i)

    conflitos = []
    for titulo_norm, indices in por_titulo.items():
        if len(indices) < 2:
            continue
        dois_presentes = {registros[i]["doi_norm"] for i in indices if registros[i]["doi_norm"]}

        # Sinal adicional de conflito: dentro da MESMA base, um identificador proprio da fonte
        # diferente (eid da Scopus, accession number "AN" da WoS) indica registros distintos
        # mesmo com titulo identico -- caso observado em titulos genericos de "Book Series"/
        # proceedings onde varios itens distintos compartilham o titulo do volume/serie.
        ids_por_base = {}
        for i in indices:
            ident = registros[i]["identificador_fonte"]
            if ident:
                ids_por_base.setdefault(registros[i]["database"], set()).add(ident)
        conflito_identificador = any(len(s) > 1 for s in ids_por_base.values())

        if len(dois_presentes) <= 1 and not conflito_identificador:
            for i in indices[1:]:
                uf.unir(indices[0], i)
        else:
            conflitos.append({
                "titulo_norm": titulo_norm,
                "ids": [registros[i]["id_registro"] for i in indices],
                "dois": sorted(dois_presentes),
                "motivo": "doi_diferente" if len(dois_presentes) > 1 else "identificador_fonte_diferente",
            })

    grupos = {}
    for i in range(n):
        raiz = uf.encontrar(i)
        grupos.setdefault(raiz, []).append(i)

    return grupos, conflitos


def escolher_melhor(registros, indices, campo, preferir_mais_longo=False):
    valores = [(registros[i][campo], registros[i]["database"]) for i in indices if registros[i][campo]]
    if not valores:
        return ""
    if preferir_mais_longo:
        return max(valores, key=lambda vp: len(vp[0]))[0]
    ordem_prioridade = {"Scopus": 0, "WoS": 1, "Crossref": 2}
    valores.sort(key=lambda vp: ordem_prioridade.get(vp[1], 9))
    return valores[0][0]


def montar_consolidado(registros, grupos):
    linhas = []
    duplicatas = []
    grupos_ordenados = sorted(grupos.values(), key=lambda idxs: min(idxs))
    for n_seq, indices in enumerate(grupos_ordenados, start=1):
        id_unico = f"REG_{n_seq:05d}"
        doi = escolher_melhor(registros, indices, "doi_norm")
        titulo = escolher_melhor(registros, indices, "titulo", preferir_mais_longo=True)
        ano = escolher_melhor(registros, indices, "ano")
        autores = escolher_melhor(registros, indices, "autores", preferir_mais_longo=True)
        fonte = escolher_melhor(registros, indices, "fonte_periodico", preferir_mais_longo=True)
        tipo_doc = escolher_melhor(registros, indices, "tipo_documento")
        resumo = escolher_melhor(registros, indices, "resumo", preferir_mais_longo=True)

        palavras = []
        for i in indices:
            for p in re.split(r"[;,]", registros[i]["palavras_chave"]):
                p = p.strip()
                if p and p.lower() not in [x.lower() for x in palavras]:
                    palavras.append(p)

        bases = sorted({registros[i]["database"] for i in indices})
        strings = sorted({registros[i]["string_id"] for i in indices if registros[i]["string_id"]})
        ids_brutos = [registros[i]["id_registro"] for i in indices]
        enriquecido = any(registros[i].get("abstract_enriquecido_manualmente") == "sim" for i in indices)

        linhas.append({
            "id_unico": id_unico,
            "doi": doi,
            "titulo": titulo,
            "ano": ano,
            "autores": autores,
            "fonte_periodico": fonte,
            "tipo_documento": tipo_doc,
            "resumo": resumo,
            "palavras_chave": "; ".join(palavras),
            "bases_origem": "|".join(bases),
            "strings_origem": "|".join(strings),
            "n_registros_agrupados": len(indices),
            "doi_presente": "sim" if doi else "nao",
            "resumo_presente": "sim" if resumo else "nao",
            "resumo_enriquecido_manualmente": "sim" if enriquecido else "nao",
            "ids_brutos_agrupados": "|".join(ids_brutos),
        })

        if len(indices) > 1:
            dois_no_grupo = {registros[i]["doi_norm"] for i in indices if registros[i]["doi_norm"]}
            titulos_no_grupo = {registros[i]["titulo_norm"] for i in indices if registros[i]["titulo_norm"]}
            if len(dois_no_grupo) >= 1 and len(titulos_no_grupo) > 1:
                criterio = "doi"
            elif len(dois_no_grupo) >= 1:
                criterio = "doi_e_titulo"
            else:
                criterio = "titulo_normalizado"
            duplicatas.append({
                "id_unico": id_unico,
                "criterio_agrupamento": criterio,
                "n_registros_agrupados": len(indices),
                "bases_origem": "|".join(bases),
                "strings_origem": "|".join(strings),
                "titulos_originais": " || ".join(sorted({registros[i]["titulo"] for i in indices if registros[i]["titulo"]})),
                "ids_brutos_agrupados": "|".join(ids_brutos),
            })

    return linhas, duplicatas


# ---------------------------------------------------------------------------
# Escrita de saidas
# ---------------------------------------------------------------------------

def escrever_csv(caminho, campos, linhas):
    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    scopus = ler_scopus()
    crossref = ler_crossref()
    wos = ler_wos()
    registros = scopus + crossref + wos

    escrever_csv(NORMALIZADOS_PATH, NORM_FIELDS, registros)

    grupos, conflitos = deduplicar(registros)
    consolidado, duplicatas = montar_consolidado(registros, grupos)
    escrever_csv(CONSOLIDADO_PATH, CONSOLIDADO_FIELDS, consolidado)
    escrever_csv(DUPLICATAS_PATH, DUPLICATAS_FIELDS, duplicatas)

    # ---- Contagens para o relatorio ----
    n_scopus, n_crossref, n_wos = len(scopus), len(crossref), len(wos)
    n_bruto_total = len(registros)
    n_unicos = len(consolidado)
    n_com_doi_bruto = sum(1 for r in registros if r["doi_norm"])
    n_sem_doi_bruto = n_bruto_total - n_com_doi_bruto
    n_unicos_com_doi = sum(1 for c in consolidado if c["doi_presente"] == "sim")
    n_unicos_sem_doi = n_unicos - n_unicos_com_doi
    n_unicos_com_resumo = sum(1 for c in consolidado if c["resumo_presente"] == "sim")
    n_unicos_sem_resumo = n_unicos - n_unicos_com_resumo
    n_grupos_duplicados = len(duplicatas)
    n_registros_removidos = n_bruto_total - n_unicos
    n_dedup_por_doi = sum(1 for d in duplicatas if d["criterio_agrupamento"] in ("doi", "doi_e_titulo"))
    n_dedup_por_titulo = sum(1 for d in duplicatas if d["criterio_agrupamento"] == "titulo_normalizado")

    contagem_bases_por_unico = {}
    for c in consolidado:
        bases = c["bases_origem"]
        contagem_bases_por_unico[bases] = contagem_bases_por_unico.get(bases, 0) + 1

    linhas_relatorio = []
    linhas_relatorio.append("# RELATORIO DE DEDUPLICACAO -- ETAPA_06\n")
    linhas_relatorio.append("Gerado por `00_CONFIG/consolidar_deduplicar.py`. Todos os numeros abaixo sao "
                             "derivados diretamente dos arquivos em `02_DADOS_BRUTOS/` e podem ser "
                             "reproduzidos executando o script novamente.\n")

    linhas_relatorio.append("## 1. Volume bruto por base (entrada)\n")
    linhas_relatorio.append("| Base | Registros brutos lidos |")
    linhas_relatorio.append("|---|---|")
    linhas_relatorio.append(f"| Scopus | {n_scopus} |")
    linhas_relatorio.append(f"| Crossref | {n_crossref} |")
    linhas_relatorio.append(f"| Web of Science | {n_wos} |")
    linhas_relatorio.append(f"| **Total bruto** | **{n_bruto_total}** |\n")
    linhas_relatorio.append(
        "Nota: o total acima ja inclui o enriquecimento por export manual do site da Scopus "
        "(`SCOPUS_A{1,2,3,4}_*.csv`, com resumo, coletado em 2026-07-09) -- ver secao 4.1. Os 4 "
        "CSVs antigos (`SCOPUS_NUCLEO_01-04_20260708_part01.csv.csv`, string incorreta com MCDM/ESG "
        "obrigatorio) continuam fora de uso -- ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`.\n"
    )

    linhas_relatorio.append("## 2. Metodo de deduplicacao\n")
    linhas_relatorio.append(
        "Conforme `01_PROTOCOLO/protocolo_busca_reprodutivel.md`, secao 7:\n"
        "1. **DOI normalizado** (minusculo, sem prefixo `https://doi.org/`, sem ponto final) = "
        "duplicata forte. Todos os registros com o mesmo DOI normalizado sao agrupados.\n"
        "2. **Titulo normalizado** (minusculo, sem acentos/pontuacao, espacos colapsados, "
        "minimo 8 caracteres) = duplicata provavel. Registros com o mesmo titulo normalizado sao "
        "agrupados, **desde que nao haja DOIs diferentes e ambos presentes no grupo** -- nesse "
        "caso de conflito, os registros NAO sao mesclados automaticamente e ficam listados na "
        "secao 5 para revisao manual (nunca apagar duplicata sem preservar proveniencia).\n"
        "3. Proveniencia preservada em `bases_origem`, `strings_origem` e `ids_brutos_agrupados` "
        "no arquivo `corpus_consolidado.csv`.\n"
    )

    linhas_relatorio.append("## 3. Resultado da deduplicacao\n")
    linhas_relatorio.append("| Metrica | Valor |")
    linhas_relatorio.append("|---|---|")
    linhas_relatorio.append(f"| Registros brutos (entrada) | {n_bruto_total} |")
    linhas_relatorio.append(f"| Registros unicos (corpus_consolidado.csv) | {n_unicos} |")
    linhas_relatorio.append(f"| Registros removidos por duplicacao | {n_registros_removidos} |")
    linhas_relatorio.append(f"| Grupos com mais de 1 registro bruto | {n_grupos_duplicados} |")
    linhas_relatorio.append(f"| Grupos fundidos por DOI (com ou sem reforco de titulo) | {n_dedup_por_doi} |")
    linhas_relatorio.append(f"| Grupos fundidos apenas por titulo normalizado (sem DOI em nenhum membro) | {n_dedup_por_titulo} |\n")

    linhas_relatorio.append("## 4. Cobertura de DOI e resumo\n")
    linhas_relatorio.append("| Metrica | Bruto (antes da dedup) | Apos dedup (corpus_consolidado.csv) |")
    linhas_relatorio.append("|---|---|---|")
    linhas_relatorio.append(f"| Com DOI | {n_com_doi_bruto} | {n_unicos_com_doi} |")
    linhas_relatorio.append(f"| Sem DOI | {n_sem_doi_bruto} | {n_unicos_sem_doi} |")
    linhas_relatorio.append(f"| Com resumo (apos escolha do melhor entre fontes) | - | {n_unicos_com_resumo} |")
    linhas_relatorio.append(f"| Sem resumo | - | {n_unicos_sem_resumo} |\n")
    linhas_relatorio.append(
        "Registros unicos sem resumo nao foram excluidos nesta etapa (regra da secao 7 do "
        "protocolo: nao excluir automaticamente antes de enriquecimento). Ficam marcados por "
        "`resumo_presente=nao` para tratamento na triagem (ETAPA seguinte).\n"
    )

    n_scopus_manual_enriquecidos = sum(1 for r in scopus if r.get("abstract_enriquecido_manualmente") == "sim")
    n_scopus_manual_novos = sum(1 for r in scopus if r["id_registro"].startswith("SCOPUS_MANUAL_NOVO::"))
    n_unicos_enriquecidos = sum(1 for c in consolidado if c["resumo_enriquecido_manualmente"] == "sim")
    linhas_relatorio.append("### 4.1 Enriquecimento manual do resumo da Scopus (2026-07-09)\n")
    linhas_relatorio.append(
        "A coleta via API da Scopus (view=STANDARD) nao traz resumo. Corrigido nesta rodada com "
        "export manual do site da Scopus (com Abstract incluido), casado por EID com os registros "
        "da API -- ver `00_CONFIG/consolidar_deduplicar.py::ler_scopus()` e "
        "`00_CONTROLE/DECISOES_METODOLOGICAS.md`.\n\n"
        f"- Registros brutos de Scopus com resumo vindo do enriquecimento manual: "
        f"{n_scopus_manual_enriquecidos} de {n_scopus}.\n"
        f"- Registros encontrados apenas no export manual, ausentes na coleta via API (drift normal "
        f"de indice entre datas de coleta diferentes -- adicionados ao corpus): "
        f"{n_scopus_manual_novos}.\n"
        f"- Registros unicos do corpus consolidado marcados `resumo_enriquecido_manualmente=sim`: "
        f"{n_unicos_enriquecidos} de {n_unicos}.\n"
    )

    linhas_relatorio.append("## 5. Conflitos de titulo identico nao mesclados automaticamente\n")
    n_conf_doi = sum(1 for c in conflitos if c["motivo"] == "doi_diferente")
    n_conf_ident = sum(1 for c in conflitos if c["motivo"] == "identificador_fonte_diferente")
    if conflitos:
        linhas_relatorio.append(
            f"Foram encontrados {len(conflitos)} grupo(s) de titulo normalizado identico que **nao foram "
            f"fundidos automaticamente** (permanecem como entradas separadas em `corpus_consolidado.csv`), "
            f"por dois motivos possiveis: {n_conf_doi} com DOIs diferentes no mesmo grupo, e {n_conf_ident} "
            "com identificador proprio da fonte diferente (eid da Scopus ou accession number da WoS) "
            "dentro da mesma base -- caso tipico de titulos genericos de volume/serie (\"Book Series\", "
            "proceedings) compartilhados por itens distintos. Revisao manual recomendada:\n"
        )
        for c in conflitos[:50]:
            linhas_relatorio.append(
                f"- titulo_norm: `{c['titulo_norm'][:120]}` | motivo: {c['motivo']} | "
                f"DOIs: {', '.join(c['dois']) if c['dois'] else '(nenhum)'} | ids: {', '.join(c['ids'])}"
            )
        if len(conflitos) > 50:
            linhas_relatorio.append(f"- ... e mais {len(conflitos) - 50} grupo(s) (ver lista completa reproduzindo o script).")
    else:
        linhas_relatorio.append("Nenhum conflito desse tipo foi encontrado.\n")

    linhas_relatorio.append("\n## 6. Distribuicao de registros unicos por combinacao de bases\n")
    linhas_relatorio.append("| Combinacao de bases_origem | N registros unicos |")
    linhas_relatorio.append("|---|---|")
    for bases, qtd in sorted(contagem_bases_por_unico.items(), key=lambda kv: -kv[1]):
        linhas_relatorio.append(f"| {bases} | {qtd} |")

    linhas_relatorio.append("\n## 7. Arquivos gerados\n")
    linhas_relatorio.append("- `03_PROCESSADOS/registros_normalizados.csv` -- 1 linha por registro bruto, campos padronizados entre as 3 bases (sem deduplicar).")
    linhas_relatorio.append("- `03_PROCESSADOS/corpus_consolidado.csv` -- 1 linha por obra unica, apos deduplicacao, com proveniencia preservada.")
    linhas_relatorio.append("- `03_PROCESSADOS/duplicatas_detectadas.csv` -- grupos com mais de 1 registro bruto, para auditoria.")
    linhas_relatorio.append("- `03_PROCESSADOS/relatorio_deduplicacao.md` -- este relatorio.\n")

    linhas_relatorio.append("## 8. Limites desta etapa\n")
    linhas_relatorio.append(
        "Esta etapa nao faz triagem de relevancia tematica (blocos A/B/C/D), nao classifica "
        "corpus descritivo vs. nucleo analitico e nao escreve texto do artigo. O campo "
        "`metodo_decisao` (etiqueta instrumental de MCDM/AHP/TOPSIS) tambem nao e preenchido "
        "aqui -- e pos-processamento de etapa posterior, conforme secao 7 do protocolo."
    )

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_relatorio) + "\n")

    resumo = {
        "n_scopus": n_scopus,
        "n_crossref": n_crossref,
        "n_wos": n_wos,
        "n_bruto_total": n_bruto_total,
        "n_unicos": n_unicos,
        "n_registros_removidos": n_registros_removidos,
        "n_grupos_duplicados": n_grupos_duplicados,
        "n_conflitos_titulo_doi": len(conflitos),
        "n_unicos_com_doi": n_unicos_com_doi,
        "n_unicos_sem_doi": n_unicos_sem_doi,
        "n_unicos_com_resumo": n_unicos_com_resumo,
        "n_unicos_sem_resumo": n_unicos_sem_resumo,
        "n_scopus_manual_enriquecidos": n_scopus_manual_enriquecidos,
        "n_scopus_manual_novos": n_scopus_manual_novos,
        "n_unicos_enriquecidos": n_unicos_enriquecidos,
    }
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
