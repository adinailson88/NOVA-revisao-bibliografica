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
citacao e submissao. Figuras PDF incorporadas pelo Pandoc são convertidas em
PNG para permanecerem visíveis no Word e no LibreOffice.
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
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


def converter_figuras_pdf_no_docx():
    """Substitui mídias PDF por PNG e atualiza seus relacionamentos OOXML."""
    with tempfile.TemporaryDirectory(prefix="artigo_docx_") as temporario:
        raiz = Path(temporario)
        with zipfile.ZipFile(INTERMEDIARIO) as pacote:
            pacote.extractall(raiz)

        midias_pdf = sorted((raiz / "word" / "media").glob("*.pdf"))
        if not midias_pdf:
            return

        pdftoppm = shutil.which("pdftoppm")
        if not pdftoppm:
            sys.exit(
                "pdftoppm nao encontrado. Instale poppler-utils para converter "
                "as figuras PDF da versao Word."
            )

        substituicoes = {}
        for origem in midias_pdf:
            destino = origem.with_suffix(".png")
            subprocess.run(
                [
                    pdftoppm,
                    "-png",
                    "-singlefile",
                    "-r",
                    "200",
                    str(origem),
                    str(destino.with_suffix("")),
                ],
                check=True,
            )
            substituicoes[origem.name] = destino.name
            origem.unlink()

        for relacoes in raiz.rglob("*.rels"):
            conteudo = relacoes.read_text(encoding="utf-8")
            atualizado = conteudo
            for antigo, novo in substituicoes.items():
                atualizado = atualizado.replace(f"media/{antigo}", f"media/{novo}")
            if atualizado != conteudo:
                relacoes.write_text(atualizado, encoding="utf-8")

        tipos = raiz / "[Content_Types].xml"
        conteudo_tipos = tipos.read_text(encoding="utf-8")
        if 'Extension="png"' not in conteudo_tipos:
            conteudo_tipos = conteudo_tipos.replace(
                "</Types>",
                '<Default Extension="png" ContentType="image/png"/></Types>',
            )
            tipos.write_text(conteudo_tipos, encoding="utf-8")

        convertido = INTERMEDIARIO.with_name("_main_pandoc_figuras_convertidas.docx")
        with zipfile.ZipFile(convertido, "w", zipfile.ZIP_DEFLATED) as pacote:
            for arquivo in sorted(raiz.rglob("*")):
                if arquivo.is_file():
                    pacote.write(arquivo, arquivo.relative_to(raiz))
        convertido.replace(INTERMEDIARIO)
        print(f"Figuras PDF convertidas para PNG: {len(midias_pdf)}")


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


def corrigir_referencias_cruzadas(doc):
    """Troca marcadores que o Pandoc deixa como [tab:...] ou [fig:...] por números."""
    from docx.oxml.ns import qn

    numeros = {}
    contadores = {"tab": 0, "fig": 0}
    for fonte in sorted((LATEX_DIR / "sections").glob("*.tex")):
        conteudo = fonte.read_text(encoding="utf-8")
        for tipo, rotulo in re.findall(r"\\label\{(tab|fig):([^}]+)\}", conteudo):
            contadores[tipo] += 1
            numeros[f"{tipo}:{rotulo}"] = str(contadores[tipo])

    padrao = re.compile(r"\[((?:tab|fig):[^\]]+)\]")
    total = 0
    for no_texto in doc.element.body.iter(qn("w:t")):
        original = no_texto.text or ""
        atualizado, quantidade = padrao.subn(
            lambda achado: numeros.get(achado.group(1), achado.group(0)),
            original,
        )
        if quantidade:
            no_texto.text = atualizado
            total += quantidade
    print(f"Referencias cruzadas numeradas: {total}")


def inserir_figuras_tikz(doc):
    """Renderiza os fluxogramas TikZ omitidos pelo Pandoc e os insere no DOCX."""
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches

    pdflatex = shutil.which("pdflatex")
    pdftoppm = shutil.which("pdftoppm")
    if not pdflatex or not pdftoppm:
        sys.exit(
            "pdflatex e pdftoppm sao necessarios para preservar os fluxogramas "
            "TikZ na versao Word."
        )

    padrao = re.compile(
        r"\\begin\{figure\}.*?(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})"
        r".*?\\caption\{([^{}]+)\}",
        re.DOTALL,
    )
    blocos = []
    for fonte in sorted((LATEX_DIR / "sections").glob("*.tex")):
        conteudo = fonte.read_text(encoding="utf-8")
        blocos.extend(padrao.findall(conteudo))

    legendas = {p.text.strip(): p for p in doc.paragraphs if p.style.name == "Image Caption"}
    inseridas = 0
    with tempfile.TemporaryDirectory(prefix="artigo_tikz_") as temporario:
        raiz = Path(temporario)
        for indice, (tikz, legenda) in enumerate(blocos, start=1):
            paragrafo_legenda = legendas.get(legenda.strip())
            if paragrafo_legenda is None:
                continue

            fonte_tex = raiz / f"figura_tikz_{indice}.tex"
            fonte_tex.write_text(
                "\\documentclass[tikz,border=5pt]{standalone}\n"
                "\\usepackage[utf8]{inputenc}\n"
                "\\usepackage[T1]{fontenc}\n"
                "\\usetikzlibrary{arrows.meta,positioning}\n"
                "\\begin{document}\n"
                f"{tikz}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                [
                    pdflatex,
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    fonte_tex.name,
                ],
                cwd=raiz,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            pdf = fonte_tex.with_suffix(".pdf")
            png = fonte_tex.with_suffix(".png")
            subprocess.run(
                [pdftoppm, "-png", "-singlefile", "-r", "200", str(pdf), str(png.with_suffix(""))],
                check=True,
            )

            paragrafo_imagem = doc.add_paragraph()
            paragrafo_imagem.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragrafo_imagem.add_run().add_picture(str(png), width=Inches(6.2))
            paragrafo_legenda._p.addprevious(paragrafo_imagem._p)
            inseridas += 1

    print(f"Fluxogramas TikZ inseridos: {inseridas}")


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

    corrigir_referencias_cruzadas(doc)
    inserir_figuras_tikz(doc)

    doc.save(DESTINO)

    if not DESTINO.exists() or DESTINO.stat().st_size == 0:
        sys.exit("Falha ao gerar o Word.")

    print(f"Word gerado com {len(doc.paragraphs)} paragrafos e {len(doc.tables)} tabelas.")


if __name__ == "__main__":
    rodar_pandoc()
    converter_figuras_pdf_no_docx()
    corrigir_docx()
    INTERMEDIARIO.unlink(missing_ok=True)
