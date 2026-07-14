from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Trecho não localizado: {label}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "('== 11, \"O artigo deve conter onze tabelas', '== 12, \"O artigo deve conter doze tabelas', \"quantidade de tabelas\"),",
        "('== 11, \"O artigo deve conter onze tabelas', '== 11, \"O artigo deve conter onze tabelas', \"quantidade de tabelas\"),",
        "quantidade de tabelas",
    )
    text = replace_once(
        text,
        '"As frequências documentais sustentam a seleção inicial dos critérios, mas não constituem pesos nem definem sua importância normativa.",',
        '"As frequências sustentam a seleção inicial, enquanto pesos e importância normativa serão definidos na validação institucional.",',
        "frequências e pesos",
    )
    text = replace_once(
        text,
        '"não constitui método multicritério parametrizado, modelo validado ou instrumento pronto para decisão",',
        '"O produto entrega uma especificação para validação futura",',
        "estado da especificação",
    )

    insertion_anchor = "bloco_restricao_temporario = '''exigir(\n    \"python scripts/python/gerar_produtos_artigo_nucleo_ampliado.py\" in workflow,\n    \"O workflow final deve continuar gerando os produtos temáticos vigentes.\",\n)\n'''\n"
    extra_blocks = r'''

bloco_limitacoes_antigo = '''padroes_limitacoes = (
    r"Não houve pré-registro(?: público do protocolo)?(?:\\.|,)",
    r"sem (?:segundo revisor independente e sem medida de |revisão independente ou )concordância interavaliadores",
    r"(?:não foram realizadas|Não houve[^.]*?) busca de citações para frente ou para trás",
    r"(?:nem |não houve )busca estruturada de literatura cinzenta",
    r"(?:Trinta e sete estudos com texto completo disponível foram posteriormente lidos|37 textos foram consultados e 19 acrescentaram evidências específicas)",
    r"A unidade (?:de análise )?quantitativa é o registro bibliográfico consolidado",
)
'''
bloco_limitacoes_novo = '''padroes_limitacoes = (
    r"deixou para estudos futuros pré-registro",
    r"Triagem e codificação foram conduzidas por um avaliador",
    r"rastreamento de citações",
    r"busca estruturada de literatura cinzenta",
    r"37 leituras integrais, das quais 19 acrescentaram evidências específicas",
    r"A unidade quantitativa é o registro consolidado",
)
'''

bloco_textocompleto_antigo = '''exigir(
    "37 estudos com texto completo disponível foram lidos integralmente; 19 forneceram evidências específicas" in texto_tex,
    "O método deve registrar os três lotes de texto completo.",
)
'''
bloco_textocompleto_novo = '''exigir(
    "Entre 37 textos completos consultados em tarefas posteriores, 19 acrescentaram evidências específicas" in texto_tex,
    "O método deve registrar o uso pontual de texto completo.",
)
'''
'''
    text = replace_once(
        text,
        insertion_anchor,
        insertion_anchor + extra_blocks,
        "blocos de limitações",
    )

    tuple_anchor = "    (bloco_restricao_antigo, bloco_restricao_temporario, \"restrição temporária de compilação\"),\n"
    tuple_extra = (
        tuple_anchor
        + "    (bloco_limitacoes_antigo, bloco_limitacoes_novo, \"limitações consolidadas\"),\n"
        + "    (bloco_textocompleto_antigo, bloco_textocompleto_novo, \"uso pontual de texto completo\"),\n"
    )
    text = replace_once(text, tuple_anchor, tuple_extra, "tuplas de substituição")

    old_controls = '''controles_parecer = (
    "especificação para parametrização multicritério",
    "109 dos 121 registros do núcleo temático vigente também pertencem ao estrato bibliométrico de 372",
    "12 registros (9,9\\%) foram classificados especificamente",
    "proposições do autor para validação institucional",
    "não constitui método multicritério parametrizado",
    "Como proposição do autor",
    "Intensidade energética em base móvel de 12 meses",
)
'''
    new_controls = '''controles_parecer = (
    "especificação para parametrização multicritério",
    "109 dos 121 registros do núcleo temático vigente também pertencem ao estrato bibliométrico de 372",
    "Doze registros (9,9\\%) foram classificados especificamente",
    "proposições do autor para validação institucional",
    "O produto entrega uma especificação para validação futura",
    "A contribuição central é uma especificação operacional candidata e rastreável",
    "Intensidade energética em base móvel de 12 meses",
)
'''
    text = replace_once(text, old_controls, new_controls, "controles do parecer")

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
