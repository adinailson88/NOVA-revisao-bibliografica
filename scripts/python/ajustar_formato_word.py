"""Ajusta um .docx gerado pelo pipeline para o formato exigido pela Ambiente
Construido (conferido no template oficial da revista, Template AC-OTH.docx):
pagina A4, margens 3 cm (superior/esquerda) e 2 cm (inferior/direita), fonte
padrao Times New Roman 12, numeracao continua de linha.

O gerador padrao (scripts/python/13_preparar_word.py, via Pandoc+LibreOffice)
produz um .docx valido mas com pagina Carta (US Letter), margens de 1 polegada
e fonte Cambria -- adequado para edicao, mas fora do formato de submissao.
Este script corrige apenas essas propriedades de layout, sem tocar no texto,
nas tabelas, nas figuras ou nas referencias.

Uso: python scripts/python/ajustar_formato_word.py artigo.docx artigo.docx
     (ou para um arquivo de saida separado: ... artigo.docx artigo_final.docx)
"""

from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

# Twips (1440 = 1 polegada = 2,54 cm). Valores conferidos no template oficial.
A4_LARGURA = 11906
A4_ALTURA = 16838
MARGEM_SUP_ESQ = 1701  # 3 cm
MARGEM_INF_DIR = 1134  # 2 cm


def ajustar_sect_pr(xml: str) -> tuple[str, int]:
    def substituir(m: re.Match) -> str:
        bloco = m.group(0)
        bloco = re.sub(r"<w:pgSz[^/]*/>", f'<w:pgSz w:w="{A4_LARGURA}" w:h="{A4_ALTURA}"/>', bloco)
        bloco = re.sub(
            r"<w:pgMar[^/]*/>",
            f'<w:pgMar w:top="{MARGEM_SUP_ESQ}" w:right="{MARGEM_INF_DIR}" '
            f'w:bottom="{MARGEM_INF_DIR}" w:left="{MARGEM_SUP_ESQ}" '
            f'w:header="709" w:footer="709" w:gutter="0"/>',
            bloco,
        )
        if "lnNumType" not in bloco:
            bloco = bloco.replace(
                "</w:sectPr>",
                '<w:lnNumType w:countBy="1" w:restart="continuous"/></w:sectPr>',
            )
        return bloco

    novo_xml, n = re.subn(r"<w:sectPr\b.*?</w:sectPr>", substituir, xml, flags=re.S)
    return novo_xml, n


def ajustar_fonte_padrao(xml: str) -> tuple[str, int]:
    novo_xml, n = re.subn(
        r'<w:rFonts w:ascii="[^"]*" w:hAnsi="[^"]*" w:eastAsia="[^"]*"([^/]*)/>',
        r'<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="Times New Roman"\1/>',
        xml,
    )
    return novo_xml, n


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    origem, destino = Path(sys.argv[1]), Path(sys.argv[2])
    if origem != destino:
        shutil.copyfile(origem, destino)
        alvo_leitura = origem
    else:
        alvo_leitura = origem

    with zipfile.ZipFile(alvo_leitura) as zin:
        nomes = zin.namelist()
        conteudos = {n: zin.read(n) for n in nomes}

    doc_xml = conteudos["word/document.xml"].decode("utf-8")
    doc_xml, n_sect = ajustar_sect_pr(doc_xml)
    doc_xml, n_fontes_doc = ajustar_fonte_padrao(doc_xml)
    conteudos["word/document.xml"] = doc_xml.encode("utf-8")

    styles_xml = conteudos["word/styles.xml"].decode("utf-8")
    styles_xml, n_fontes_estilos = ajustar_fonte_padrao(styles_xml)
    conteudos["word/styles.xml"] = styles_xml.encode("utf-8")

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
        for nome in nomes:
            zout.writestr(nome, conteudos[nome])

    print(f"Secoes ajustadas para A4/margens/numeracao de linha: {n_sect}")
    print(f"Fontes trocadas para Times New Roman: {n_fontes_doc} em document.xml, {n_fontes_estilos} em styles.xml.")
    print(f"Arquivo gerado em: {destino}")


if __name__ == "__main__":
    main()
