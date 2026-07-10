"""
Script de coleta Crossref (ETAPA_03 - COLETA_CROSSREF).

Le CROSSREF_MAILTO de 00_CONFIG/apis_local.txt em tempo de execucao (nao e uma chave secreta,
apenas identifica a aplicacao no polite pool da API publica).
Salva retorno bruto (JSON e CSV) por query em 02_DADOS_BRUTOS/crossref/, sem deduplicar.
Gera um resumo objetivo em 02_DADOS_BRUTOS/crossref/_resumo_execucao.json.
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
OUT_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "crossref")
API_URL = "https://api.crossref.org/works"

FROM_PUB_DATE = "2010-01-01"
UNTIL_PUB_DATE = "2026-12-31"
ROWS = 100
# Limite deliberado do protocolo (nao e bug, ver 01_PROTOCOLO/strings_nativas_por_base.md, secao 3):
# "limite inicial = 300 resultados por query, ajustavel apos inspecao de ruido."
LIMIT_PER_QUERY = 300

# Queries do nucleo (01_PROTOCOLO/strings_nativas_por_base.md, secao 3)
QUERIES = {
    "crossref_nucleo_a1": "building maintenance sustainability",
    "crossref_nucleo_a2": "facility management sustainability building",
    "crossref_nucleo_a3": "maintenance prioritization public buildings sustainability",
    "crossref_nucleo_a4": "university campus building maintenance sustainability",
    "crossref_nucleo_a5": "building asset management life cycle sustainability",
}

CSV_FIELDS = [
    "doi", "title", "abstract", "author", "published", "container_title", "type",
    "subject", "is_referenced_by_count", "url", "publisher", "language",
    "database", "string_id",
]


def load_mailto():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("CROSSREF_MAILTO="):
                return line.split("=", 1)[1].strip()
    return None


def call_crossref(query, mailto, cursor="*", rows=ROWS):
    params = {
        "query.bibliographic": query,
        "filter": f"from-pub-date:{FROM_PUB_DATE},until-pub-date:{UNTIL_PUB_DATE}",
        "rows": str(rows),
        "cursor": cursor,
        "mailto": mailto,
    }
    url = API_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        status = resp.getcode()
        body = resp.read().decode("utf-8")
        return status, json.loads(body)


def extract_published(item):
    for key in ("published-print", "published-online", "issued"):
        node = item.get(key)
        if node and node.get("date-parts"):
            parts = node["date-parts"][0]
            return "-".join(str(p) for p in parts if p is not None)
    return ""


def extract_csv_row(item, string_id):
    authors = item.get("author") or []
    author_names = "; ".join(
        " ".join(filter(None, [a.get("given", ""), a.get("family", "")]))
        for a in authors if isinstance(a, dict)
    )
    container = item.get("container-title") or []
    subject = item.get("subject") or []
    return {
        "doi": item.get("DOI", ""),
        "title": "; ".join(item.get("title") or []),
        "abstract": item.get("abstract", ""),
        "author": author_names,
        "published": extract_published(item),
        "container_title": "; ".join(container) if isinstance(container, list) else container,
        "type": item.get("type", ""),
        "subject": "; ".join(subject) if isinstance(subject, list) else subject,
        "is_referenced_by_count": item.get("is-referenced-by-count", ""),
        "url": item.get("URL", ""),
        "publisher": item.get("publisher", ""),
        "language": item.get("language", ""),
        "database": "Crossref",
        "string_id": string_id,
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    mailto = load_mailto()
    summary = {"queries": []}

    if not mailto:
        summary["fatal_error"] = "CROSSREF_MAILTO ausente ou vazio em 00_CONFIG/apis_local.txt"
        with open(os.path.join(OUT_DIR, "_resumo_execucao.json"), "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print("FATAL: CROSSREF_MAILTO ausente")
        sys.exit(2)

    any_http_error = False

    for string_id, query in QUERIES.items():
        entry = {
            "string_id": string_id,
            "query_bibliographic": query,
            "filter": f"from-pub-date:{FROM_PUB_DATE},until-pub-date:{UNTIL_PUB_DATE}",
            "pages": [],
            "total_results": None,
            "records_exported": 0,
            "truncated_by_limit": False,
            "http_errors": [],
        }
        all_items = []
        cursor = "*"
        try:
            while len(all_items) < LIMIT_PER_QUERY:
                status, data = call_crossref(query, mailto, cursor=cursor, rows=ROWS)
                message = data.get("message", {})
                total_results = message.get("total-results")
                entry["total_results"] = total_results
                items = message.get("items", [])
                all_items.extend(items)
                next_cursor = message.get("next-cursor")
                entry["pages"].append({
                    "cursor": cursor,
                    "http_status": status,
                    "returned": len(items),
                })
                if not items or next_cursor is None or next_cursor == cursor:
                    break
                cursor = next_cursor
                if len(all_items) >= LIMIT_PER_QUERY:
                    entry["truncated_by_limit"] = True
                    break
                time.sleep(1)
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8")
            except Exception:
                pass
            entry["http_errors"].append({"code": e.code, "reason": str(e.reason), "body_snippet": body[:300]})
            any_http_error = True
        except urllib.error.URLError as e:
            entry["http_errors"].append({"code": None, "reason": str(e.reason)})
            any_http_error = True
        except Exception as e:
            entry["http_errors"].append({"code": None, "reason": repr(e)})
            any_http_error = True

        all_items = all_items[:LIMIT_PER_QUERY]

        raw_path = os.path.join(OUT_DIR, string_id + "_raw.json")
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump({"string_id": string_id, "query_bibliographic": query, "items": all_items}, f, ensure_ascii=False, indent=2)

        csv_path = os.path.join(OUT_DIR, string_id + "_raw.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for item in all_items:
                writer.writerow(extract_csv_row(item, string_id))

        entry["records_exported"] = len(all_items)
        entry["raw_file"] = os.path.basename(raw_path)
        entry["csv_file"] = os.path.basename(csv_path)
        summary["queries"].append(entry)

    summary["any_http_error"] = any_http_error
    with open(os.path.join(OUT_DIR, "_resumo_execucao.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("DONE any_http_error=" + str(any_http_error))


if __name__ == "__main__":
    main()
