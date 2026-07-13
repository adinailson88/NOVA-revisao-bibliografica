"""Gera inventario CSV das referencias efetivamente citadas no artigo."""

from __future__ import annotations

import csv
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIGO = ROOT / "latex-artigo"
DESTINO = ROOT / "referencias"
BIB = ARTIGO / "references.bib"


def extrair_entradas(texto: str) -> list[tuple[str, str, str]]:
    entradas = []
    pos = 0
    inicio = re.compile(r"@(\w+)\s*\{\s*([^,]+),", re.I)
    while achado := inicio.search(texto, pos):
        profundidade = 1
        i = achado.end()
        while i < len(texto) and profundidade:
            if texto[i] == "{":
                profundidade += 1
            elif texto[i] == "}":
                profundidade -= 1
            i += 1
        if profundidade:
            raise ValueError(f"Entrada BibTeX incompleta: {achado.group(2)}")
        entradas.append((achado.group(1), achado.group(2).strip(), texto[achado.end(): i - 1]))
        pos = i
    return entradas


def campos(corpo: str) -> dict[str, str]:
    saida: dict[str, str] = {}
    padrao = re.compile(r"(\w+)\s*=\s*\{", re.I)
    pos = 0
    while achado := padrao.search(corpo, pos):
        profundidade = 1
        i = achado.end()
        while i < len(corpo) and profundidade:
            if corpo[i] == "{":
                profundidade += 1
            elif corpo[i] == "}":
                profundidade -= 1
            i += 1
        valor = corpo[achado.end(): i - 1]
        valor = re.sub(r"\s+", " ", valor).strip()
        saida[achado.group(1).lower()] = valor
        pos = i
    return saida


texto_tex = "\n".join(
    arquivo.read_text(encoding="utf-8")
    for arquivo in [ARTIGO / "main.tex", *sorted((ARTIGO / "sections").glob("*.tex"))]
)
citadas: set[str] = set()
for grupo in re.findall(r"\\(?:textcite|parencite)\{([^}]+)\}", texto_tex):
    citadas.update(chave.strip() for chave in grupo.split(","))

entradas = extrair_entradas(BIB.read_text(encoding="utf-8"))
mapa = {chave: (tipo, campos(corpo)) for tipo, chave, corpo in entradas}
faltantes = citadas - mapa.keys()
nao_citadas = mapa.keys() - citadas
if faltantes or nao_citadas:
    raise SystemExit(f"Divergencia entre citacoes e BibTeX. Faltantes={sorted(faltantes)}; nao citadas={sorted(nao_citadas)}")

DESTINO.mkdir(exist_ok=True)
shutil.copyfile(BIB, DESTINO / "references.bib")
colunas = ["chave_bibtex", "tipo", "autoria", "titulo", "ano", "periodico_ou_instituicao", "volume", "numero", "paginas", "doi", "url_doi"]
with (DESTINO / "lista_referencias.csv").open("w", encoding="utf-8-sig", newline="") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=colunas)
    escritor.writeheader()
    for chave in sorted(citadas):
        tipo, item = mapa[chave]
        doi = item.get("doi", "")
        escritor.writerow({
            "chave_bibtex": chave,
            "tipo": tipo,
            "autoria": item.get("author", ""),
            "titulo": item.get("title", ""),
            "ano": item.get("year", ""),
            "periodico_ou_instituicao": item.get("journal", item.get("institution", "")),
            "volume": item.get("volume", ""),
            "numero": item.get("number", ""),
            "paginas": item.get("pages", ""),
            "doi": doi,
            "url_doi": f"https://doi.org/{doi}" if doi else "",
        })

print(f"Inventario gerado com {len(citadas)} referencias citadas.")
