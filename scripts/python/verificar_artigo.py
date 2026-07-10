"""Valida coerencia numerica, estilo, citacoes e rastreabilidade do artigo."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIGO = ROOT / "latex-artigo"
SECOES = ARTIGO / "sections"
FONTES = ARTIGO / "fontes"
SCRIPT_R = ROOT / "scripts" / "r" / "10_gerar_produtos_artigo.R"


def ler_csv(nome: str) -> list[dict[str, str]]:
    with (FONTES / nome).open(encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def inteiro(valor: str) -> int:
    return int(float(valor))


def exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise AssertionError(mensagem)


tex_arquivos = [ARTIGO / "main.tex", *sorted(SECOES.glob("*.tex"))]
texto_tex = "\n".join(p.read_text(encoding="utf-8") for p in tex_arquivos)
texto_prosa = "\n".join(
    linha for linha in texto_tex.splitlines() if not linha.lstrip().startswith("\\draw")
)

# Estilo solicitado
exigir("Rascunho" not in texto_tex and "rascunho" not in texto_tex, "Subtitulo de rascunho ainda presente.")
exigir(not re.search(r"[–—]", texto_prosa), "Foi encontrado travessao Unicode no artigo.")
exigir(" -- " not in texto_prosa, "Foi encontrado travessao em sintaxe LaTeX no artigo.")
exigir("\\captionsetup{labelsep=period" in texto_tex, "Separador de legenda deve ser ponto.")
exigir("\\texttt{fontes/" not in texto_tex, "Fonte de tabela nao deve expor caminho de arquivo.")
exigir(".md}" not in texto_tex and ".md)" not in texto_tex, "Referencia a arquivo Markdown no artigo.")
for expressao in (
    "não houve dupla",
    "nao houve dupla",
    "revisão sistemática plena",
    "revisao sistematica plena",
    "texto completo",
    "full-text",
):
    exigir(expressao.lower() not in texto_tex.lower(), f"Expressao removida reapareceu: {expressao}")

# Quantidade e nao redundancia estrutural
exigir(texto_tex.count("\\begin{table}") == 5, "O artigo deve manter cinco tabelas essenciais.")
exigir(texto_tex.count("\\begin{figure}") == 6, "O artigo deve manter um fluxograma e cinco graficos.")
exigir(texto_tex.count("\\captiongrafico{") == 5, "Os cinco produtos quantitativos devem ser chamados de Graficos.")
exigir("figura10_distribuicao_base_tipo" not in texto_tex, "Grafico redundante de base e tipo ainda citado.")
exigir("tab:funil" not in texto_tex, "Tabela redundante do funil ainda citada.")
exigir("tab:temporal" not in texto_tex, "Tabela temporal redundante ainda citada.")
exigir("tab:dimensoes" not in texto_tex, "Tabela de dimensoes redundante ainda citada.")
exigir("tab:metodos" not in texto_tex, "Tabela de metodos redundante ainda citada.")
exigir("tab:matrizanalitica" not in texto_tex, "Tabela redundante da matriz ainda citada.")
exigir("tab:lacunas" not in texto_tex, "Tabela de lacunas redundante ainda citada.")

# Citacoes e bibliografia
bib = (ARTIGO / "references.bib").read_text(encoding="utf-8")
chaves_bib = set(re.findall(r"@\w+\{([^,]+),", bib))
chaves_citadas: set[str] = set()
for grupo in re.findall(r"\\(?:textcite|parencite)\{([^}]+)\}", texto_tex):
    chaves_citadas.update(chave.strip() for chave in grupo.split(","))
exigir(not (chaves_citadas - chaves_bib), f"Citacoes sem referencia: {sorted(chaves_citadas - chaves_bib)}")
exigir(not (chaves_bib - chaves_citadas), f"Referencias nao citadas: {sorted(chaves_bib - chaves_citadas)}")
exigir("@phdthesis" not in bib.lower() and "@mastersthesis" not in bib.lower(), "Tese ou dissertacao na bibliografia.")
exigir(len(re.findall(r"@article\{", bib, flags=re.I)) >= 16, "Bibliografia cientifica insuficiente.")

# Corpus final
nucleo = ler_csv("nucleo_final_pos_auditoria_resumos.csv")
exigir(len(nucleo) == 104, "O nucleo final deve ter 104 registros.")
ids = [linha["id_unico"] for linha in nucleo]
exigir(len(ids) == len(set(ids)), "id_unico duplicado no nucleo final.")

contagem_bases = {"Scopus": 0, "WoS": 0, "Crossref": 0}
combinacoes: dict[str, int] = {}
for linha in nucleo:
    combinacao = linha["bases_origem"]
    combinacoes[combinacao] = combinacoes.get(combinacao, 0) + 1
    for base in combinacao.split("|"):
        contagem_bases[base] += 1
exigir(contagem_bases == {"Scopus": 98, "WoS": 49, "Crossref": 6}, f"Bases divergentes: {contagem_bases}")
exigir(
    combinacoes
    == {
        "Scopus": 52,
        "Scopus|WoS": 41,
        "WoS": 5,
        "Crossref|Scopus|WoS": 3,
        "Crossref|Scopus": 2,
        "Crossref": 1,
    },
    f"Combinacoes de proveniencia divergentes: {combinacoes}",
)

# Estrategia de busca
buscas = ler_csv("tabela_estrategia_busca.csv")
total_bruto = sum(inteiro(linha["retorno_bruto"]) for linha in buscas)
exigir(total_bruto == 12118, f"Total bruto divergente: {total_bruto}")
n_consultas = {
    base: sum(
        1
        for linha in buscas
        if linha["base"] == base and "complemento_manual" not in linha["string_id"]
    )
    for base in ("Scopus", "Web of Science", "Crossref")
}
exigir(
    n_consultas == {"Scopus": 4, "Web of Science": 4, "Crossref": 5},
    f"Numero de consultas divergente: {n_consultas}",
)

# Tabelas geradas pelo R
dimensoes = ler_csv("tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv")
dimensoes_esperadas = {
    "tecnica_operacional",
    "institucional",
    "ambiental",
    "ciclo_de_vida",
    "economica",
    "social",
}
exigir(
    {linha["dimensao_identificada_leitura"] for linha in dimensoes} == dimensoes_esperadas,
    "Tabela de dimensoes contem criterios ou perdeu dimensoes canonicas.",
)

tipos = ler_csv("tabela34_tipos_documentais_harmonizados_nucleo_final_104.csv")
tipos_obtidos = {linha["tipo_harmonizado"]: inteiro(linha["total_registros"]) for linha in tipos}
exigir(
    tipos_obtidos
    == {
        "Artigo de periodico": 79,
        "Trabalho em evento": 15,
        "Livro ou serie de livro": 10,
    },
    f"Tipos documentais divergentes: {tipos_obtidos}",
)

mencoes = ler_csv("tabela35_mencoes_ods_esg_nucleo_final_104.csv")
mencoes_obtidas = {linha["marcador"]: inteiro(linha["total_registros"]) for linha in mencoes}
exigir(mencoes_obtidas == {"ODS ou SDG": 1, "ESG": 0}, f"ODS/ESG divergentes: {mencoes_obtidas}")

# Todo grafico citado deve ser produzido pelo script R
script_r = SCRIPT_R.read_text(encoding="utf-8")
graficos_citados = set(re.findall(r"\{figuras/([^}]+\.png)\}", texto_tex))
for grafico in graficos_citados:
    exigir(grafico in script_r, f"Grafico sem geracao no script R: {grafico}")

print("Verificacao do artigo concluida sem divergencias.")
