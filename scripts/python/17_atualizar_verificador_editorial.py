from __future__ import annotations

from pathlib import Path

PATH = Path("scripts/python/verificar_artigo_integrado.py")


def main() -> None:
    text = PATH.read_text(encoding="utf-8")

    anchor = '''    (
        "não foram acrescentados à camada bibliométrica de 372",
        "não foram acrescentados à camada de 372",
        "separação entre busca direcionada e camada bibliométrica",
    ),
'''
    additions = '''    (
        "Dez concentram-se em previsão ou previsão combinada à otimização",
        "dez estudos em previsão ou previsão com otimização",
        "síntese quantitativa das funções de IA",
    ),
    (
        "Nenhum dos 17 demonstrou uma cadeia completa",
        "Em conjunto, o lote cobre partes da cadeia",
        "integração da cadeia de decisão",
    ),
    (
        "Em resposta à RQ6",
        "A leitura integral do lote incorporado esclarece a RQ6",
        "abertura da síntese da RQ6",
    ),
    (
        "não implica pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo ou metanálise",
        "O escopo declarado distingue esses procedimentos das etapas de pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo e metanálise",
        "escopo metodológico de Hu et al.",
    ),
    (
        "Como verificação complementar, formulou-se a RQ6",
        "Como análise complementar de cobertura, a RQ6 verifica",
        "formulação da RQ6 na introdução",
    ),
'''

    if additions not in text:
        if anchor not in text:
            raise RuntimeError("Ponto de inserção das substituições não localizado.")
        text = text.replace(anchor, additions + anchor, 1)

    PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
