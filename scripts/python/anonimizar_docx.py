"""Gera uma copia anonimizada de um .docx para avaliacao duplo-cega.

Uso: python scripts/python/anonimizar_docx.py artigo.docx artigo_anonimo.docx

O que faz:
- remove metadados de autoria de docProps/core.xml (dc:creator,
  cp:lastModifiedBy) e docProps/app.xml (Company), sem apagar o restante;
- remove, em word/document.xml, o(s) paragrafo(s) que contem o nome do
  autor, a afiliacao (Programa de Pos-Graduacao em Biossistemas) e a sigla
  da instituicao (UFSB), preservando todo o restante do documento;
- nao toca no corpo cientifico do artigo.
"""

from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

AUTOR_MARCADORES = (
    "Adinailson",
    "Guimarães de Oliveira",
    "Fabricio Berton Zanchi",
    "Programa de Pós-Graduação em Biossistemas",
    "Universidade Federal do Sul da Bahia",
)


def limpar_core_xml(xml: str) -> str:
    xml = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator></dc:creator>", xml, flags=re.S)
    xml = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "<cp:lastModifiedBy></cp:lastModifiedBy>", xml, flags=re.S)
    return xml


def limpar_app_xml(xml: str) -> str:
    xml = re.sub(r"<Company>.*?</Company>", "<Company></Company>", xml, flags=re.S)
    return xml


def remover_paragrafos_autor(xml: str) -> tuple[str, int]:
    paragrafos = re.findall(r"<w:p\b.*?</w:p>", xml, flags=re.S)
    removidos = 0
    for p in paragrafos:
        texto = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.S))
        if any(marcador in texto for marcador in AUTOR_MARCADORES):
            xml = xml.replace(p, "", 1)
            removidos += 1
    return xml, removidos


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        raise SystemExit(1)
    origem, destino = Path(sys.argv[1]), Path(sys.argv[2])
    shutil.copyfile(origem, destino)

    with zipfile.ZipFile(origem) as zin:
        nomes = zin.namelist()
        conteudos = {n: zin.read(n) for n in nomes}

    doc_xml = conteudos["word/document.xml"].decode("utf-8")
    doc_xml, removidos = remover_paragrafos_autor(doc_xml)
    conteudos["word/document.xml"] = doc_xml.encode("utf-8")

    if "docProps/core.xml" in conteudos:
        core = conteudos["docProps/core.xml"].decode("utf-8")
        conteudos["docProps/core.xml"] = limpar_core_xml(core).encode("utf-8")

    if "docProps/app.xml" in conteudos:
        app = conteudos["docProps/app.xml"].decode("utf-8")
        conteudos["docProps/app.xml"] = limpar_app_xml(app).encode("utf-8")

    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
        for nome in nomes:
            zout.writestr(nome, conteudos[nome])

    print(f"Paragrafos de autoria removidos: {removidos}")
    print(f"Arquivo anonimizado gerado em: {destino}")
    if removidos == 0:
        print("AVISO: nenhum paragrafo de autoria foi identificado e removido. Verifique manualmente.")


if __name__ == "__main__":
    main()
