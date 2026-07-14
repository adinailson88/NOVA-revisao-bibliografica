from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    duplicates = '''    (
        'Dez concentram-se em previsão ou previsão combinada à otimização',
        'dez estudos em previsão ou previsão com otimização',
        'síntese quantitativa das funções de IA',
    ),
    (
        'Nenhum dos 17 demonstrou uma cadeia completa',
        'Em conjunto, o lote cobre partes da cadeia',
        'integração da cadeia de decisão',
    ),
    (
        'Em resposta à RQ6',
        'A leitura integral do lote incorporado esclarece a RQ6',
        'abertura da síntese da RQ6',
    ),
    (
        'não implica pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo ou metanálise',
        'O escopo declarado distingue esses procedimentos das etapas de pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo e metanálise',
        'escopo metodológico de Hu et al.',
    ),
    (
        'Como verificação complementar, formulou-se a RQ6',
        'Como análise complementar de cobertura, a RQ6 verifica',
        'formulação da RQ6 na introdução',
    ),
'''
    if duplicates in text:
        text = text.replace(duplicates, "", 1)

    for required in (
        "definição conjunta de AHP",
        "definição conjunta de TOPSIS",
        "definição conjunta de ANP",
    ):
        if required not in text:
            raise RuntimeError(f"Controle terminológico ausente: {required}")

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
