"""Gera uma copia visual paginada do PDF validado em formato Word."""

from pathlib import Path
from tempfile import TemporaryDirectory

import fitz
from docx import Document
from docx.enum.text import WD_BREAK, WD_LINE_SPACING
from docx.shared import Mm, Pt

ROOT = Path(__file__).resolve().parents[2]
origem = ROOT / "latex-artigo" / "main.pdf"
destino = ROOT / "artigo.docx"

if not origem.exists() or origem.stat().st_size == 0:
    raise SystemExit("PDF compilado ausente.")

pdf = fitz.open(origem)
documento = Document()
secao = documento.sections[0]
secao.page_width = Mm(210)
secao.page_height = Mm(297)
secao.top_margin = Mm(1)
secao.bottom_margin = Mm(1)
secao.left_margin = Mm(1)
secao.right_margin = Mm(1)
secao.header_distance = Mm(0)
secao.footer_distance = Mm(0)

primeiro = documento.add_paragraph()
with TemporaryDirectory() as temporario:
    pasta = Path(temporario)
    for numero, pagina in enumerate(pdf):
        paragrafo = primeiro if numero == 0 else documento.add_paragraph()
        formato = paragrafo.paragraph_format
        formato.space_before = Pt(0)
        formato.space_after = Pt(0)
        formato.line_spacing_rule = WD_LINE_SPACING.SINGLE
        imagem = pasta / f"pagina-{numero + 1:03d}.jpg"
        matriz = fitz.Matrix(1.8, 1.8)
        pagina.get_pixmap(matrix=matriz, alpha=False).save(imagem, jpg_quality=92)
        paragrafo.add_run().add_picture(str(imagem), width=Mm(208), height=Mm(295))
        if numero < len(pdf) - 1:
            paragrafo.add_run().add_break(WD_BREAK.PAGE)

pdf.close()
documento.save(destino)

if not destino.exists() or destino.stat().st_size == 0:
    raise SystemExit("Falha ao gerar o Word.")

print(f"Word visual gerado com {len(documento.paragraphs)} paginas do PDF validado.")
