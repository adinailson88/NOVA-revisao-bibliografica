"""Gera artigo.docx a partir dos fontes LaTeX do artigo, para leitura fora do LaTeX.

Requer Pandoc, python-docx e, no workflow, LibreOffice. O Pandoc converte o
texto e as referências; o script reconstrói tabelas, corrige referências
cruzadas, insere fluxogramas TikZ e, por fim, abre e resalva o documento pelo
LibreOffice para maximizar a compatibilidade com Microsoft Word, LibreOffice e
visualizadores móveis.
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
        sys.exit("Pandoc nao encontrado no PATH.")
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
    """Substitui mídias PDF por PNG e atualiza relacionamentos OOXML."""
    with tempfile.TemporaryDirectory(prefix="artigo_docx_") as temporario:
        raiz = Path(temporario)
        with zipfile.ZipFile(INTERMEDIARIO) as pacote:
            pacote.extractall(raiz)

        pasta_midias = raiz / "word" / "media"
        midias_pdf = sorted(pasta_midias.glob("*.pdf")) if pasta_midias.exists() else []
        if not midias_pdf:
            return

        pdftoppm = shutil.which("pdftoppm")
        if not pdftoppm:
            sys.exit("pdftoppm nao encontrado para converter figuras PDF.")

        substituicoes = {}
        for origem in midias_pdf:
            destino = origem.with_suffix(".png")
            subprocess.run(
                [pdftoppm, "-png", "-singlefile", "-r", "200", str(origem), str(destino.with_suffix(""))],
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
                "</Types>", '<Default Extension="png" ContentType="image/png"/></Types>'
            )
        conteudo_tipos = re.sub(
            r'<Default Extension="pdf" ContentType="application/pdf"\s*/>',
            "",
            conteudo_tipos,
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
            {qn("w:val"): "single", qn("w:sz"): "4", qn("w:space"): "0", qn("w:color"): "999999"},
        )
        borders.append(el)
    tbl_pr.append(borders)


def construir_tabela(doc, texto):
    from docx.shared import Pt

    texto = COLSPEC.sub("", texto, count=1).strip()
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    matriz = [[c.strip() for c in ln.split(" & ")] for ln in linhas]
    ncols = max(len(r) for r in matriz)
    for linha in matriz:
        linha.extend([""] * (ncols - len(linha)))
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
        atualizado, quantidade = padrao.subn(lambda achado: numeros.get(achado.group(1), achado.group(0)), original)
        if quantidade:
            no_texto.text = atualizado
            total += quantidade
    print(f"Referencias cruzadas numeradas: {total}")


def inserir_figuras_tikz(doc):
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches

    pdflatex = shutil.which("pdflatex")
    pdftoppm = shutil.which("pdftoppm")
    if not pdflatex or not pdftoppm:
        sys.exit("pdflatex e pdftoppm sao necessarios para preservar fluxogramas TikZ.")

    padrao = re.compile(
        r"\\begin\{figure\}.*?(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}).*?\\caption\{([^{}]+)\}",
        re.DOTALL,
    )
    blocos = []
    for fonte in sorted((LATEX_DIR / "sections").glob("*.tex")):
        blocos.extend(padrao.findall(fonte.read_text(encoding="utf-8")))

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
                "\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n"
                "\\usetikzlibrary{arrows.meta,positioning}\n\\begin{document}\n"
                f"{tikz}\n\\end{document}\n",
                encoding="utf-8",
            )
            subprocess.run(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", fonte_tex.name],
                cwd=raiz,
                check=True,
                stdout=subprocess.DEVNULL,
            )
            pdf = fonte_tex.with_suffix(".pdf")
            png = fonte_tex.with_suffix(".png")
            subprocess.run([pdftoppm, "-png", "-singlefile", "-r", "200", str(pdf), str(png.with_suffix(""))], check=True)
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
    for paragrafo in alvos:
        tabela = construir_tabela(doc, paragrafo.text)
        paragrafo._p.addnext(tabela._tbl)
        legenda = doc.add_paragraph()
        tabela._tbl.addnext(legenda._p)
        paragrafo._p.getparent().remove(paragrafo._p)
    print(f"Tabelas reconstruidas: {len(alvos)}")

    estilo_h1 = next((p.style for p in doc.paragraphs if p.text.strip() == "Introdução"), None)
    for paragrafo in doc.paragraphs:
        if paragrafo.style.name == "Bibliography":
            titulo = paragrafo.insert_paragraph_before("Referências")
            if estilo_h1 is not None:
                titulo.style = estilo_h1
            break

    corrigir_referencias_cruzadas(doc)
    inserir_figuras_tikz(doc)
    doc.save(DESTINO)
    if not DESTINO.exists() or DESTINO.stat().st_size == 0:
        sys.exit("Falha ao gerar o Word.")
    print(f"Word gerado com {len(doc.paragraphs)} paragrafos e {len(doc.tables)} tabelas.")


def normalizar_com_libreoffice():
    """Abre e resalva o DOCX para corrigir incompatibilidades OOXML silenciosas."""
    soffice = shutil.which("libreoffice") or shutil.which("soffice")
    if not soffice:
        print("LibreOffice nao encontrado; normalizacao adicional ignorada.")
        return
    with tempfile.TemporaryDirectory(prefix="normalizar_docx_") as temporario:
        saida = Path(temporario)
        subprocess.run(
            [soffice, "--headless", "--convert-to", "docx", "--outdir", str(saida), str(DESTINO)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=180,
        )
        normalizado = saida / DESTINO.name
        if not normalizado.exists() or normalizado.stat().st_size == 0:
            sys.exit("LibreOffice nao produziu o DOCX normalizado.")
        normalizado.replace(DESTINO)
    print("Word aberto e resalvo com sucesso pelo LibreOffice.")


def validar_docx():
    from docx import Document

    if not zipfile.is_zipfile(DESTINO):
        sys.exit("O arquivo Word gerado nao e um pacote DOCX valido.")
    with zipfile.ZipFile(DESTINO) as pacote:
        erro = pacote.testzip()
        if erro:
            sys.exit(f"Entrada corrompida no DOCX: {erro}")
        obrigatorios = {"[Content_Types].xml", "word/document.xml", "word/_rels/document.xml.rels"}
        ausentes = obrigatorios.difference(pacote.namelist())
        if ausentes:
            sys.exit(f"Partes obrigatorias ausentes no DOCX: {sorted(ausentes)}")
    documento = Document(DESTINO)
    if not documento.paragraphs:
        sys.exit("O Word foi aberto, mas nao contem paragrafos.")
    print(f"Word validado: {DESTINO.stat().st_size} bytes.")


if __name__ == "__main__":
    rodar_pandoc()
    converter_figuras_pdf_no_docx()
    corrigir_docx()
    normalizar_com_libreoffice()
    validar_docx()
    INTERMEDIARIO.unlink(missing_ok=True)
