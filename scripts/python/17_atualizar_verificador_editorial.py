from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    individual_entries = '''    (
        'AHP corresponde a \\textit{Analytic Hierarchy Process}',
        'AHP, TOPSIS e ANP correspondem, respectivamente, a \\textit{Analytic Hierarchy Process}',
        'definição conjunta de AHP',
    ),
    (
        'TOPSIS a \\textit{Technique for Order Preference by Similarity to Ideal Solution}',
        '\\textit{Technique for Order Preference by Similarity to Ideal Solution}',
        'definição conjunta de TOPSIS',
    ),
    (
        'ANP a \\textit{Analytic Network Process}',
        '\\textit{Analytic Network Process}',
        'definição conjunta de ANP',
    ),
'''
    if individual_entries in text:
        text = text.replace(individual_entries, "", 1)

    variable_anchor = "substituicoes = (\n"
    term_blocks = r'''bloco_terminologia_antigo = '''for declaracao in (
    "ambiental, social e de governança (ESG",
    "MCDM designa \\textit{multi-criteria decision-making}",
    "MCDA, \\textit{multi-criteria decision analysis}",
    "AHP corresponde a \\textit{Analytic Hierarchy Process}",
    "TOPSIS a \\textit{Technique for Order Preference by Similarity to Ideal Solution}",
    "ANP a \\textit{Analytic Network Process}",
    "modelagem da informação da construção (BIM",
    "matriz analítica conceitual informada pela síntese da literatura",
):
    exigir(declaracao in texto_tex, f"Padronizacao terminologica ausente: {declaracao}")
'''
bloco_terminologia_novo = '''for declaracao in (
    "ambiental, social e de governança (ESG",
    "MCDM designa \\textit{multi-criteria decision-making}",
    "MCDA, \\textit{multi-criteria decision analysis}",
    "AHP, TOPSIS e ANP correspondem, respectivamente, a \\textit{Analytic Hierarchy Process}",
    "\\textit{Technique for Order Preference by Similarity to Ideal Solution}",
    "\\textit{Analytic Network Process}",
    "modelagem da informação da construção (BIM",
    "Matriz de indicadores e fluxo para parametrização multicritério",
):
    exigir(declaracao in texto_tex, f"Padronizacao terminologica ausente: {declaracao}")
'''

'''
    if "bloco_terminologia_antigo =" not in text:
        if variable_anchor not in text:
            raise RuntimeError("Âncora das substituições não localizada.")
        text = text.replace(variable_anchor, term_blocks + variable_anchor, 1)

    tuple_anchor = '    (bloco_textocompleto_antigo, bloco_textocompleto_novo, "uso pontual de texto completo"),\n'
    tuple_entry = '    (bloco_terminologia_antigo, bloco_terminologia_novo, "padronização terminológica consolidada"),\n'
    if tuple_entry not in text:
        if tuple_anchor not in text:
            raise RuntimeError("Âncora da tupla terminológica não localizada.")
        text = text.replace(tuple_anchor, tuple_anchor + tuple_entry, 1)

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
