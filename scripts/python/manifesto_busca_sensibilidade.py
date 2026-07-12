"""
Gera o manifesto de proveniencia da busca de sensibilidade IA/ML (2026-07-12).

Le os 3 arquivos brutos ja copiados para 02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/
(Scopus CSV, WoS RIS em duas partes, Crossref CSV) sem alterar seu conteudo, reconta
programaticamente cada um (nao confia apenas no numero informado), calcula SHA-256,
extrai periodo coberto e lista campos disponiveis, e verifica overlap de accession
number (UT) entre as duas partes do WoS.

Saida: 02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/MANIFESTO.md
"""

import csv
import hashlib
import os
import re
import sys

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DIR = os.path.join(BASE_DIR, "02_DADOS_BRUTOS", "busca_sensibilidade_ia_20260712")
MANIFESTO_PATH = os.path.join(RAW_DIR, "MANIFESTO.md")


def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(bloco)
    return h.hexdigest()


def contar_scopus(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        campos = leitor.fieldnames
        linhas = list(leitor)
    anos = [int(l["Year"]) for l in linhas if (l.get("Year") or "").strip().isdigit()]
    return {
        "n_registros": len(linhas),
        "campos": campos,
        "periodo": (min(anos), max(anos)) if anos else (None, None),
    }


def parsear_ris_tags(caminho):
    """Parser tag-a-tag tolerante (mesma logica de consolidar_deduplicar.py::parsear_ris),
    retorna lista de dicts por registro."""
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


def contar_wos(caminho):
    registros = parsear_ris_tags(caminho)
    tags_presentes = sorted({tag for r in registros for tag in r.keys()})
    anos = [int(r["PY"]) for r in registros if (r.get("PY") or "").strip().isdigit()]
    accessions = [r.get("AN", "").strip() for r in registros if r.get("AN", "").strip()]
    return {
        "n_registros": len(registros),
        "campos": tags_presentes,
        "periodo": (min(anos), max(anos)) if anos else (None, None),
        "accessions": accessions,
    }


def contar_crossref(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        campos = leitor.fieldnames
        linhas = list(leitor)
    anos = []
    for l in linhas:
        m = re.search(r"(19|20)\d{2}", l.get("published") or "")
        if m:
            anos.append(int(m.group(0)))
    return {
        "n_registros": len(linhas),
        "campos": campos,
        "periodo": (min(anos), max(anos)) if anos else (None, None),
    }


def main():
    scopus_path = os.path.join(RAW_DIR, "scopus", "SCOPUS_A5_2009-2026.csv")
    wos1_path = os.path.join(RAW_DIR, "wos", "WOS_NUCLEO_05_20260712_part01.ris")
    wos2_path = os.path.join(RAW_DIR, "wos", "WOS_NUCLEO_05_20260712_part02.ris")
    crossref_path = os.path.join(RAW_DIR, "crossref", "crossref_ia_todos_resultados.csv")

    scopus = contar_scopus(scopus_path)
    wos1 = contar_wos(wos1_path)
    wos2 = contar_wos(wos2_path)
    crossref = contar_crossref(crossref_path)

    overlap = set(wos1["accessions"]) & set(wos2["accessions"])

    linhas = []
    linhas.append("# MANIFESTO — Busca de sensibilidade IA/ML (2026-07-12)\n")
    linhas.append(
        "Arquivos brutos fornecidos pelo usuário, coletados manualmente fora deste ambiente. "
        "Nenhuma nova busca foi executada aqui; este manifesto apenas organiza, recontagem e "
        "documenta os arquivos recebidos, preservando seu conteúdo original.\n"
    )

    linhas.append("## Arquivos\n")
    linhas.append("| Caminho | Base | Registros (recontados) | Tamanho (bytes) | SHA-256 |")
    linhas.append("|---|---|---|---|---|")
    for caminho, base, n in [
        (scopus_path, "Scopus", scopus["n_registros"]),
        (wos1_path, "Web of Science (parte 1)", wos1["n_registros"]),
        (wos2_path, "Web of Science (parte 2)", wos2["n_registros"]),
        (crossref_path, "Crossref", crossref["n_registros"]),
    ]:
        rel = os.path.relpath(caminho, BASE_DIR).replace("\\", "/")
        tam = os.path.getsize(caminho)
        h = sha256_arquivo(caminho)
        linhas.append(f"| `{rel}` | {base} | {n} | {tam} | `{h}` |")

    linhas.append("\n## Contagens agregadas\n")
    linhas.append(f"- Scopus: **{scopus['n_registros']}** registros (esperado: 3169).")
    linhas.append(
        f"- Web of Science: parte 1 = **{wos1['n_registros']}** (esperado 1000), "
        f"parte 2 = **{wos2['n_registros']}** (esperado 559), "
        f"total = **{wos1['n_registros'] + wos2['n_registros']}**."
    )
    linhas.append(f"- Crossref: **{crossref['n_registros']}** linhas (esperado 2000, 10 consultas × 200).")
    linhas.append(
        f"- Overlap de accession number (UT/campo `AN`) entre parte 1 e parte 2 do WoS: "
        f"**{len(overlap)}** registro(s) em comum."
    )
    if overlap:
        linhas.append(f"  - IDs sobrepostos: {sorted(overlap)[:20]}" + (" (truncado)" if len(overlap) > 20 else ""))

    linhas.append("\n## Período coberto (extraído dos dados)\n")
    linhas.append("| Base | Ano mínimo | Ano máximo |")
    linhas.append("|---|---|---|")
    linhas.append(f"| Scopus | {scopus['periodo'][0]} | {scopus['periodo'][1]} |")
    wos_anos = [a for a in (wos1["periodo"][0], wos2["periodo"][0]) if a] + [a for a in (wos1["periodo"][1], wos2["periodo"][1]) if a]
    linhas.append(f"| Web of Science | {min(wos_anos) if wos_anos else '-'} | {max(wos_anos) if wos_anos else '-'} |")
    linhas.append(f"| Crossref | {crossref['periodo'][0]} | {crossref['periodo'][1]} |")

    linhas.append("\n## Campos disponíveis por arquivo\n")
    linhas.append(f"- **Scopus** (cabeçalho CSV, {len(scopus['campos'])} campos): {', '.join(scopus['campos'])}\n")
    linhas.append(f"- **WoS parte 1** (tags RIS presentes, {len(wos1['campos'])}): {', '.join(wos1['campos'])}\n")
    linhas.append(f"- **WoS parte 2** (tags RIS presentes, {len(wos2['campos'])}): {', '.join(wos2['campos'])}\n")
    linhas.append(f"- **Crossref** (cabeçalho CSV, {len(crossref['campos'])} campos): {', '.join(crossref['campos'])}\n")

    linhas.append("\n## Data de inclusão neste repositório\n")
    linhas.append("2026-07-12 (data informada pelo nome dos arquivos e pela sessão de incorporação).\n")

    with open(MANIFESTO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    print(f"Scopus: {scopus['n_registros']}")
    print(f"WoS parte1: {wos1['n_registros']}, parte2: {wos2['n_registros']}, overlap: {len(overlap)}")
    print(f"Crossref: {crossref['n_registros']}")
    print(f"Manifesto escrito em {MANIFESTO_PATH}")


if __name__ == "__main__":
    main()
