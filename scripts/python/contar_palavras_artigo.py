"""Conta as palavras visiveis do artigo.docx entre os titulos "Introducao" e
"Referencias" (exclusive), incluindo o texto de tabelas -- metodo mais
conservador (conta mais texto, nao menos), usado para garantir margem frente
ao limite de 7.000 palavras da Ambiente Construido ("a minuta do artigo deve
ter o maximo de 7.000 palavras, contando-se a partir da introducao do
artigo, ate as conclusoes").

Uso:
    python scripts/python/contar_palavras_artigo.py [caminho/para/artigo.docx]

Sem argumento, usa artigo.docx na raiz do repositorio.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _texto_do_elemento(elemento):
    from docx.oxml.ns import qn

    return "".join(no.text or "" for no in elemento.iter(qn("w:t")))


def contar_palavras(caminho_docx):
    from docx import Document

    doc = Document(caminho_docx)
    contando = False
    total = 0
    for filho in doc.element.body:
        tag = filho.tag.split("}")[-1]
        if tag not in ("p", "tbl"):
            continue
        texto = _texto_do_elemento(filho)
        texto_limpo = texto.strip()
        if tag == "p":
            if not contando and texto_limpo.endswith("Introdução"):
                contando = True
                continue
            if contando and texto_limpo == "Referências":
                break
        if contando:
            total += len(texto_limpo.split())
    return total


if __name__ == "__main__":
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "artigo.docx"
    total = contar_palavras(caminho)
    print(f"Palavras entre 'Introdução' e 'Referências' (paragrafos + tabelas) em {caminho.name}: {total}")
