"""Gera artigo.docx a partir dos fontes LaTeX do artigo, para leitura fora do LaTeX.

Requer Pandoc (https://pandoc.org/) e python-docx instalados. Uso:

    python scripts/python/13_preparar_word.py

O Pandoc converte main.tex (com citeproc, a partir de references.bib) para um
docx intermediario, preservando texto real, titulos, citacoes e a lista de
referencias. O leitor LaTeX do Pandoc nao reconhece os ambientes
tabularx/booktabs com especificacoes de coluna customizadas usados no artigo
(ver latex-artigo/sections/*.tex), entao cada tabela sai como um paragrafo cru
com celulas separadas por " & ". Este script detecta esses paragrafos e os
reconstroi como tabelas nativas do Word, e adiciona o titulo "Referencias"
antes da lista bibliografica gerada pelo citeproc (que sai sem cabecalho de
secao). A formatacao ABNT fina, o fluxograma em TikZ e a paginacao do PDF nao
sao preservados; o PDF (main.pdf) continua sendo a versao de referencia para
citacao e submissao.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LATEX_DIR = ROOT / "latex-artigo"
INTERMEDIARIO = LATEX_DIR / "_main_pandoc_bruto.docx"
DESTINO = ROOT / "artigo.docx"

COLSPEC = re.compile(r"^(?:(?:>p[\d.]+cm|Y)\s*)+")


def rodar_pandoc():
    pandoc = shutil.which("pandoc")
    if not pandoc:
        sys.exit(
            "Pandoc nao encontrado no PATH. Instale em https://pandoc.org/installing.html "
            "e rode este script novamente."
        )
    subprocess.run(
        [
            pandoc,
            "main.tex",
            "--bibliography=references.bib",
            "--citeproc",
            "-o",
            str(INTERMEDIARIO),
            "--resource-path=.;sections;figuras",
        ],
        cwd=LATEX_DIR,
        check=True,
    )


def eh_paragrafo_de_tabela(texto):
    if " & " not in texto:
        return False
    primeira_linha = texto.split("\n", 1)[0]
    return bool(COLSPEC.match(primeira_linha)) or texto.count(" & ") >= 2


def aplicar_bordas(tabela):
    from docx.oxml.ns import qn

    tbl_pr = tabela._tbl.tblPr
    borders = tbl_pr.makeelement(qn("w:tblBorders"), {})
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = tbl_pr.makeelement(
            qn(f"w:{lado}"),
            {
                qn("w:val"): "single",
                qn("w:sz"): "4",
                qn("w:space"): "0",
                qn("w:color"): "999999",
            },
        )
        borders.append(el)
    tbl_pr.append(borders)


def construir_tabela(doc, texto):
    from docx.shared import Pt

    texto = COLSPEC.sub("", texto, count=1).strip()
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    matriz = [[c.strip() for c in ln.split(" & ")] for ln in linhas]
    ncols = max(len(r) for r in matriz)
    for r in matriz:
        while len(r) < ncols:
            r.append("")
    tabela = doc.add_table(rows=len(matriz), cols=ncols)
    aplicar_bordas(tabela)
    for i, linha in enumerate(matriz):
        for j, valor in enumerate(linha):
            cell = tabela.cell(i, j)
            cell.text = valor
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9)
                    if i == 0:
                        run.font.bold = True
    return tabela


def corrigir_docx():
    from docx import Document

    doc = Document(INTERMEDIARIO)

    alvos = [p for p in doc.paragraphs if eh_paragrafo_de_tabela(p.text)]
    for p in alvos:
        tabela = construir_tabela(doc, p.text)
        p._p.addnext(tabela._tbl)
        legenda = doc.add_paragraph()
        tabela._tbl.addnext(legenda._p)
        p._p.getparent().remove(p._p)
    print(f"Tabelas reconstruidas: {len(alvos)}")

    vazias = [t for t in doc.tables if len(t.rows) == 0]
    for t in vazias:
        t._tbl.getparent().remove(t._tbl)

    # O nome interno do estilo de titulo de secao varia entre versoes do Pandoc
    # (ex.: "Heading 1" vs "Heading1"), entao reaproveita o estilo de um heading
    # de nivel 1 ja existente no documento em vez de referenciar por nome fixo.
    estilo_h1 = next((p.style for p in doc.paragraphs if p.text.strip() == "Introdução"), None)
    for p in doc.paragraphs:
        if p.style.name == "Bibliography":
            titulo = p.insert_paragraph_before("Referências")
            if estilo_h1 is not None:
                titulo.style = estilo_h1
            break

    doc.save(DESTINO)

    if not DESTINO.exists() or DESTINO.stat().st_size == 0:
        sys.exit("Falha ao gerar o Word.")

    print(f"Word gerado com {len(doc.paragraphs)} paragrafos e {len(doc.tables)} tabelas.")


if __name__ == "__main__":
    rodar_pandoc()
    corrigir_docx()
    INTERMEDIARIO.unlink(missing_ok=True)
