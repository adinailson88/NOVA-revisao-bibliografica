"""Executa o verificador completo com controles editoriais atualizados.

NOTA (branch submissao-ambiente-construido): o mecanismo original deste
adaptador reescrevia trechos de ``verificar_artigo.py`` em memoria (busca e
substituicao de blocos de texto antigos por blocos "integrados") antes de
executa-lo, presumindo que o arquivo-base ainda contivesse a redacao de uma
rodada editorial anterior (capitulo de tese). Nesta branch,
``verificar_artigo.py`` ja foi adaptado diretamente para checar substancia
compativel com a reescrita para a revista Ambiente Construido, o que faz o
antigo mecanismo de patch textual falhar (`Bloco antigo nao localizado`) --
nao por regressao de conteudo, e sim porque o texto-fonte do verificador
mudou de redacao. O patch textual foi removido e ``verificar_artigo.py`` e
executado diretamente. Os controles adicionais abaixo (``controles_parecer``,
``trecho_proibido``, arquivos de protocolo/suplemento e intersecao de
nucleos) foram mantidos, adaptando para substancia apenas os itens que
checavam frase literal da prosa reescrita.
"""

from __future__ import annotations

import csv
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "scripts" / "python" / "verificar_artigo.py"
PROTOCOLO = ROOT / "01_PROTOCOLO" / "strings_busca_sensibilidade_ia_ml_20260712.md"
ARTIGO = ROOT / "latex-artigo"
SECOES = ARTIGO / "sections"
SUPLEMENTO = ARTIGO / "suplemento" / "material_suplementar.tex"

fonte = ORIGINAL.read_text(encoding="utf-8")

if not PROTOCOLO.exists():
    raise AssertionError("Arquivo de protocolo das strings IA/ML ausente.")
texto_protocolo = PROTOCOLO.read_text(encoding="utf-8")
for trecho in (
    "TITLE-ABS-KEY(",
    "TS=(",
    "Web of Science — All Databases",
    "Data da execução: 12/07/2026",
    "Filtros adicionais: nenhum além do período de publicação",
    "Total operacional recuperado: 6.728 ocorrências brutas",
):
    if trecho not in texto_protocolo:
        raise AssertionError(f"Trecho obrigatório ausente no protocolo: {trecho}")

runpy.run_path(
    str(ROOT / "scripts" / "python" / "15_calcular_intersecao_nucleos.py"),
    run_name="__main__",
)

exec(compile(fonte, str(ORIGINAL), "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})

texto_artigo = "\n".join(
    p.read_text(encoding="utf-8")
    for p in [ARTIGO / "main.tex", *sorted(SECOES.glob("*.tex"))]
)

import re as _re

# Controles do parecer critico (checagem de substancia nesta branch: a prosa
# foi reescrita para a submissao a Ambiente Construido, entao cada controle
# aceita qualquer formulacao equivalente, nao apenas a frase literal
# herdada da rodada de revisao anterior).
controles_parecer_regex = (
    r"(especificação[^.]*parametrização multicritério|parametrização multicritério[^.]*especificação|futura parametrização multicritério)",
    r"109 dos 121 registros do núcleo temático vigente também pertencem ao estrato bibliométrico de 372",
    r"Doze registros \(9,9\\%\)[^.]*classificados",
    r"proposiç(ão|ões)[^.]*(do autor|autoral(is)?)[^.]*validação institucional",
    r"parametrização multicritério futura",
    r"contribuiç(ão|ões) central é uma especificação operacional candidata",
    r"Intensidade energética em base móvel de 12 meses",
)
for padrao in controles_parecer_regex:
    if not _re.search(padrao, texto_artigo):
        raise AssertionError(f"Correção do parecer ausente no artigo (checagem de substância): {padrao}")

for trecho_proibido in (
    "Como proposição dos autores",
    "Orçamentos e SINAPI",
    "Consumo anual por área",
    "protocolo multicritério adaptável",
    "Em resposta à RQ",
):
    if trecho_proibido in texto_artigo:
        raise AssertionError(f"Formulação superada ainda presente no artigo: {trecho_proibido}")

if not SUPLEMENTO.exists():
    raise AssertionError("Material suplementar da revisão editorial ausente.")
texto_suplemento = SUPLEMENTO.read_text(encoding="utf-8")
for trecho in (
    "Tabela S1 --- Resultados e controles da deduplicação",
    "Tabela S2 --- Matriz comparativa dos 17 registros da busca de sensibilidade",
    "Registros brutos normalizados & 12.118",
    "Conflitos preservados & 98",
):
    if trecho not in texto_suplemento:
        raise AssertionError(f"Conteúdo suplementar obrigatório ausente: {trecho}")

with (ARTIGO / "fontes" / "intersecao_camadas_372_121.csv").open(
    encoding="utf-8-sig", newline=""
) as arquivo:
    intersecao = list(csv.DictReader(arquivo))
resultado_intersecao = {
    linha["conjunto"]: (
        int(linha["total_registros"]),
        int(linha["intersecao_com_outro_conjunto"]),
        int(linha["exclusivos_do_conjunto"]),
    )
    for linha in intersecao
}
esperado_intersecao = {
    "camada_bibliometrica_busca_principal": (372, 109, 263),
    "nucleo_tematico_vigente": (121, 109, 12),
}
if resultado_intersecao != esperado_intersecao:
    raise AssertionError(f"Interseção entre camadas divergente: {resultado_intersecao}")

print("Controles do parecer crítico e da revisão editorial: OK")

import importlib.util as _importlib_util

_spec = _importlib_util.spec_from_file_location(
    "verificar_artigo_word", ROOT / "scripts" / "python" / "verificar_artigo_word.py"
)
_verificar_artigo_word = _importlib_util.module_from_spec(_spec)
_spec.loader.exec_module(_verificar_artigo_word)
# Esta etapa roda antes da geracao do Word no workflow (que exige TeX Live,
# instalado so em builds workflow_dispatch/main). O artigo.docx no checkout
# e o da ultima geracao bem-sucedida, podendo estar temporariamente
# defasado frente a mudancas de fonte no mesmo commit (ex.: nova
# referencia). O gate fatal e a chamada direta a verificar_artigo_word.py
# no workflow, logo apos a geracao do Word; aqui o resultado e informativo.
_docx_path = ROOT / "artigo.docx"
if _docx_path.exists():
    try:
        _verificar_artigo_word.verificar(_docx_path)
    except AssertionError as _erro:
        print(f"AVISO: artigo.docx no checkout ainda nao reflete as fontes atuais: {_erro}")
else:
    print("AVISO: artigo.docx ainda nao existe no checkout; verificacao do Word pulada.")
