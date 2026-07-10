"""
Script de coleta Scopus (ETAPA_02 - COLETA_SCOPUS).

Le a chave SCOPUS_API_KEY de 00_CONFIG/apis_local.txt em tempo de execucao.
Nunca imprime, loga ou grava a chave em nenhum arquivo de saida.
Salva retorno bruto (JSON) por string em 02_DADOS_BRUTOS/scopus/.
Gera um resumo objetivo (sem chave) em 02_DADOS_BRUTOS/scopus/_resumo_execucao.json,
usado depois para montar 01_PROTOCOLO/log_coleta_scopus.md.

Nota sobre o limite de 5000 (2026-07-08): a API de busca da Scopus rejeita qualquer paginacao em
que start+count ultrapasse 5000 resultados, com erro HTTP 400
"Exceeds the number of search results" (statusCode INVALID_INPUT) -- e um limite real e
documentado da propria API Elsevier, nao um teto arbitrario deste script. Quando uma string tem
total_results > 5000 (caso de SCOPUS_NUCLEO_A1, com 7584), o script particiona automaticamente a
janela de anos (PUBYEAR) em sub-faixas ate que cada sub-faixa fique com total_results <= 5000, e
depois funde os resultados das sub-faixas, sem deduplicar (a deduplicacao real ocorre na ETAPA_06).
"""

import csv
import json
import os
import sys
import time
import urllib.request
import urllib.parse
import urllib.error

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "00_CONFIG", "apis_local.txt")
OUT_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "scopus")
API_URL = "https://api.elsevier.com/content/search/scopus"

# Corpo booleano de cada string do nucleo, SEM o filtro de ano (o ano e adicionado dinamicamente
# por _build_query, permitindo particionar a busca em sub-faixas de ano quando necessario).
QUERY_BODIES = {
    "scopus_nucleo_a1_manutencao_sustentabilidade": (
        'TITLE-ABS-KEY(("building maintenance" OR "facility management" OR '
        '"facilities management" OR "facilities maintenance" OR "building asset management" OR '
        '"building operation" OR "operation and maintenance" OR "maintenance management") '
        'AND (sustainab* OR "green building*" OR "life cycle" OR "life-cycle" OR '
        '"sustainability assessment" OR "sustainability indicator*" OR "environmental performance" OR '
        '"building performance"))'
    ),
    "scopus_nucleo_a2_contexto_publico_universitario": (
        'TITLE-ABS-KEY(("public building*" OR "university building*" OR "university campus" OR '
        '"higher education institution*" OR "educational building*" OR "government building*" OR '
        '"public sector building*" OR "building portfolio") AND ("building maintenance" OR maintenance OR '
        '"facility management" OR "facilities management" OR "asset management" OR '
        '"operation and maintenance") AND (sustainab* OR "environmental performance" OR "life cycle" OR '
        '"sustainability assessment"))'
    ),
    "scopus_nucleo_a3_priorizacao_estrategia_manutencao": (
        'TITLE-ABS-KEY(("maintenance prioritization" OR "maintenance backlog" OR "deferred maintenance" OR '
        '"maintenance strategy" OR "maintenance planning" OR "renewal prioritization" OR '
        '"condition assessment" OR "condition-based maintenance") AND (building* OR "public building*" OR '
        '"university building*" OR campus OR "building portfolio" OR "built environment" OR '
        '"facility management" OR "facilities management") AND (sustainab* OR "environmental criteria" OR '
        '"social criteria" OR "life cycle" OR "risk-based maintenance"))'
    ),
    "scopus_nucleo_a4_gestao_ativos_ciclo_vida": (
        'TITLE-ABS-KEY(("building asset management" OR "facility management" OR "facilities management" OR '
        '"building maintenance" OR "building operation" OR "operation and maintenance") AND ("life cycle" OR '
        '"life-cycle" OR "whole life cost" OR "life cycle cost" OR "service life" OR durability OR '
        '"building performance" OR "asset performance") AND (sustainab* OR "environmental performance" OR '
        '"sustainability assessment"))'
    ),
}

YEAR_MIN = 2010
YEAR_MAX = 2026
PAGE_SIZE = 25
# Limite real e documentado da API de busca Scopus: start+count nunca pode ultrapassar 5000.
API_HARD_WINDOW = 5000

CSV_FIELDS = [
    "eid", "doi", "title", "abstract", "author_names", "year", "source_title",
    "document_type", "subtype", "citedby_count", "aggregation_type", "url",
    "database", "string_id", "year_range_origem",
]


def _build_query(body, y0, y1):
    return f"{body} AND PUBYEAR > {y0 - 1} AND PUBYEAR < {y1 + 1}"


def extract_csv_row(entry, string_id, year_range_origem):
    authors = entry.get("author") or []
    if isinstance(authors, list):
        author_names = "; ".join(
            a.get("authname", "") for a in authors if isinstance(a, dict)
        )
    else:
        author_names = ""
    links = entry.get("link") or []
    url = ""
    for link in links if isinstance(links, list) else []:
        if isinstance(link, dict) and link.get("@ref") == "scopus":
            url = link.get("@href", "")
            break
    return {
        "eid": entry.get("eid", ""),
        "doi": entry.get("prism:doi", ""),
        "title": entry.get("dc:title", ""),
        "abstract": entry.get("dc:description", ""),
        "author_names": author_names,
        "year": (entry.get("prism:coverDate", "") or "")[:4],
        "source_title": entry.get("prism:publicationName", ""),
        "document_type": entry.get("prism:aggregationType", ""),
        "subtype": entry.get("subtypeDescription", ""),
        "citedby_count": entry.get("citedby-count", ""),
        "aggregation_type": entry.get("prism:aggregationType", ""),
        "url": url,
        "database": "Scopus",
        "string_id": string_id,
        "year_range_origem": year_range_origem,
    }


def load_api_key():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("SCOPUS_API_KEY="):
                return line.split("=", 1)[1].strip()
    return None


def call_scopus(query, api_key, start=0, count=PAGE_SIZE):
    params = {
        "query": query,
        "start": str(start),
        "count": str(count),
        "view": "COMPLETE",
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("X-ELS-APIKey", api_key)
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.getcode()
        body = resp.read().decode("utf-8")
        return status, json.loads(body)


def fetch_year_range(body, api_key, y0, y1, api_calls_log, http_errors_log):
    """
    Busca todos os registros de [y0, y1] para uma string. Se total_results > API_HARD_WINDOW e o
    intervalo ainda puder ser dividido (y0 < y1), particiona recursivamente em duas metades por
    ano. Retorna (entries, truncated_single_year: bool).
    """
    query = _build_query(body, y0, y1)
    start = 0
    entries = []
    total_results = None
    while True:
        try:
            status, data = call_scopus(query, api_key, start=start, count=PAGE_SIZE)
        except urllib.error.HTTPError as e:
            body_snippet = ""
            try:
                body_snippet = e.read().decode("utf-8")
            except Exception:
                pass
            http_errors_log.append({
                "code": e.code, "reason": str(e.reason), "body_snippet": body_snippet[:300],
                "year_range": f"{y0}-{y1}", "start": start,
            })
            if e.code == 400 and "Exceeds the number of search results" in body_snippet and y0 < y1:
                # janela de 5000 estourada: particiona o intervalo de anos em duas metades e refaz
                mid = (y0 + y1) // 2
                left, left_trunc = fetch_year_range(body, api_key, y0, mid, api_calls_log, http_errors_log)
                right, right_trunc = fetch_year_range(body, api_key, mid + 1, y1, api_calls_log, http_errors_log)
                return left + right, (left_trunc or right_trunc)
            # y0 == y1 (nao da para particionar mais) ou erro de outra natureza: para aqui
            break
        except (urllib.error.URLError, Exception) as e:
            http_errors_log.append({"code": None, "reason": repr(e), "year_range": f"{y0}-{y1}", "start": start})
            break

        sr = data.get("search-results", {})
        total_results_raw = sr.get("opensearch:totalResults")
        try:
            total_results = int(total_results_raw)
        except (TypeError, ValueError):
            total_results = None
        page_entries = sr.get("entry", [])
        entries.extend(page_entries)
        api_calls_log.append({
            "year_range": f"{y0}-{y1}", "start": start, "http_status": status, "returned": len(page_entries),
            "total_results": total_results_raw,
        })

        if not page_entries or len(page_entries) < PAGE_SIZE:
            break
        start += PAGE_SIZE
        if total_results is not None and start >= total_results:
            break
        if start + PAGE_SIZE > API_HARD_WINDOW and y0 < y1:
            # evita bater no limite real da API: particiona preventivamente antes do erro 400
            mid = (y0 + y1) // 2
            left, left_trunc = fetch_year_range(body, api_key, y0, mid, api_calls_log, http_errors_log)
            right, right_trunc = fetch_year_range(body, api_key, mid + 1, y1, api_calls_log, http_errors_log)
            # descarta as entradas parciais desta janela ampla (serao recobertas pelas sub-faixas)
            return left + right, (left_trunc or right_trunc)
        if start >= API_HARD_WINDOW:
            # y0 == y1: nao da para particionar mais por ano; aceitar truncamento nesta faixa
            return entries, True
        time.sleep(1)

    truncated = total_results is not None and len(entries) < total_results and y0 == y1
    return entries, truncated


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    api_key = load_api_key()
    summary = {"queries": []}

    if not api_key:
        summary["fatal_error"] = "SCOPUS_API_KEY ausente ou vazia em 00_CONFIG/apis_local.txt"
        with open(os.path.join(OUT_DIR, "_resumo_execucao.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print("FATAL: chave ausente")
        sys.exit(2)

    any_http_error = False

    for string_id, body in QUERY_BODIES.items():
        api_calls_log = []
        http_errors_log = []
        all_entries, truncated_single_year = fetch_year_range(
            body, api_key, YEAR_MIN, YEAR_MAX, api_calls_log, http_errors_log
        )

        if http_errors_log:
            any_http_error = True

        year_ranges_used = sorted(set(c["year_range"] for c in api_calls_log))

        entry = {
            "string_id": string_id,
            "year_ranges_used": year_ranges_used,
            "api_calls": api_calls_log,
            "records_exported": len(all_entries),
            "truncated_single_year_over_5000": truncated_single_year,
            "http_errors": http_errors_log,
        }

        raw_path = os.path.join(OUT_DIR, string_id + "_raw.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(
                {"string_id": string_id, "query_body": body, "year_ranges_used": year_ranges_used,
                 "entries": all_entries},
                f, ensure_ascii=False, indent=2,
            )

        csv_path = os.path.join(OUT_DIR, string_id + "_raw.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for e in all_entries:
                writer.writerow(extract_csv_row(e, string_id, "|".join(year_ranges_used)))

        entry["raw_file"] = os.path.basename(raw_path)
        entry["csv_file"] = os.path.basename(csv_path)
        summary["queries"].append(entry)

    summary["any_http_error"] = any_http_error
    with open(os.path.join(OUT_DIR, "_resumo_execucao.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("DONE any_http_error=" + str(any_http_error))


if __name__ == "__main__":
    main()
