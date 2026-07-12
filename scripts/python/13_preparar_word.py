"""Converte o PDF validado do artigo em uma versao Word de distribuicao."""

from pathlib import Path
from pdf2docx import Converter

ROOT = Path(__file__).resolve().parents[2]
origem = ROOT / "latex-artigo" / "main.pdf"
destino = ROOT / "artigo.docx"

if not origem.exists() or origem.stat().st_size == 0:
    raise SystemExit("PDF compilado ausente.")

conversor = Converter(str(origem))
try:
    conversor.convert(str(destino))
finally:
    conversor.close()

if not destino.exists() or destino.stat().st_size == 0:
    raise SystemExit("Falha ao gerar o Word.")

print(f"Word gerado a partir do PDF validado: {destino.name}.")
