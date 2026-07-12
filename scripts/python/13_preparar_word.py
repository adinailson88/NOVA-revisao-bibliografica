"""Prepara uma copia do LaTeX compativel com a conversao para Word."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIGO = ROOT / "latex-artigo"
MAIN = ARTIGO / "main.tex"
SAIDA = ARTIGO / "word-main.tex"


def expandir_inputs(texto: str) -> str:
    padrao = re.compile(r"\\input\{([^}]+)\}")
    while padrao.search(texto):
        texto = padrao.sub(
            lambda m: (ARTIGO / f"{m.group(1)}.tex").read_text(encoding="utf-8"),
            texto,
        )
    return texto


def numerar_rotulos(texto: str, ambiente: str) -> dict[str, int]:
    padrao = re.compile(
        rf"\\begin\{{{ambiente}\}}.*?\\end\{{{ambiente}\}}",
        re.S,
    )
    mapa: dict[str, int] = {}
    for numero, bloco in enumerate(padrao.findall(texto), start=1):
        achado = re.search(r"\\label\{([^}]+)\}", bloco)
        if achado:
            mapa[achado.group(1)] = numero
    return mapa


def converter_tabularx(achado: re.Match[str]) -> str:
    corpo = achado.group("corpo")
    linhas = [
        linha for linha in corpo.splitlines()
        if "&" in linha and not linha.lstrip().startswith("%")
    ]
    n_colunas = max((linha.count("&") + 1 for linha in linhas), default=1)
    corpo = re.sub(r"\\(?:toprule|midrule|bottomrule)\s*", "", corpo)
    corpo = re.sub(r"\\addlinespace(?:\[[^]]*\])?\s*", "", corpo)
    return "\\begin{longtable}{" + ("l" * n_colunas) + "}\n" + corpo + "\n\\end{longtable}"


texto = expandir_inputs(MAIN.read_text(encoding="utf-8"))
rotulos = {
    **numerar_rotulos(texto, "table"),
    **numerar_rotulos(texto, "figure"),
}
texto = re.sub(
    r"\\begin\{tabularx\}[^\\n]*\\n(?P<corpo>.*?)\\end\{tabularx\}",
    converter_tabularx,
    texto,
    flags=re.S,
)
texto = texto.replace(r"\captiongrafico", r"\caption")
texto = texto.replace(r"\fonteautor", r"\par Fonte: elaborado pelo autor.")
texto = re.sub(r"\\label\{[^}]+\}", "", texto)
texto = re.sub(
    r"\\ref\{([^}]+)\}",
    lambda m: str(rotulos.get(m.group(1), "")),
    texto,
)
texto = re.sub(r"\\(?:scriptsize|footnotesize|small)\b", "", texto)
titulo = re.search(r"\\title\{([^}]+)\}", texto, re.S).group(1)
autor = re.search(r"\\author\{(.*?)\}\s*\\date", texto, re.S).group(1)
corpo = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", texto, re.S).group(1)
corpo = corpo.replace(
    r"\maketitle",
    "\\section*{" + titulo + "}\n\\begin{center}" + autor + "\\end{center}",
)
SAIDA.write_text(corpo, encoding="utf-8")
print(f"Fonte intermediaria para Word criada em {SAIDA.relative_to(ROOT)}.")
