"""Calcula a sobreposição entre a camada bibliométrica e o núcleo temático vigente.

A camada bibliométrica contém os registros classificados como ``A_nucleo_forte``
na matriz reavaliada da busca principal. O núcleo temático vigente contém os 104
registros originais e os 17 incorporados pela busca de sensibilidade IA/ML.
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
MATRIZ = ROOT / "07_SINTESE_TEMATICA" / "matriz_extracao_final_reavaliada_resumos.csv"
NUCLEO = ROOT / "latex-artigo" / "fontes" / "nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv"
SAIDA = ROOT / "latex-artigo" / "fontes" / "intersecao_camadas_372_121.csv"


def main() -> None:
    matriz = pd.read_csv(
        MATRIZ,
        usecols=["id_unico", "estrato_uso_resumo"],
        dtype="string",
        low_memory=False,
    )
    nucleo = pd.read_csv(NUCLEO, usecols=["id_unico"], dtype="string", low_memory=False)

    ids_372 = set(
        matriz.loc[matriz["estrato_uso_resumo"].eq("A_nucleo_forte"), "id_unico"]
        .dropna()
        .str.strip()
    )
    ids_121 = set(nucleo["id_unico"].dropna().str.strip())
    intersecao = ids_372 & ids_121

    if len(ids_372) != 372:
        raise AssertionError(f"Camada bibliométrica divergente: {len(ids_372)} registros.")
    if len(ids_121) != 121:
        raise AssertionError(f"Núcleo temático divergente: {len(ids_121)} registros.")

    resultado = pd.DataFrame(
        [
            {
                "conjunto": "camada_bibliometrica_busca_principal",
                "total_registros": len(ids_372),
                "intersecao_com_outro_conjunto": len(intersecao),
                "exclusivos_do_conjunto": len(ids_372 - ids_121),
            },
            {
                "conjunto": "nucleo_tematico_vigente",
                "total_registros": len(ids_121),
                "intersecao_com_outro_conjunto": len(intersecao),
                "exclusivos_do_conjunto": len(ids_121 - ids_372),
            },
        ]
    )
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    resultado.to_csv(SAIDA, index=False)

    print(f"CAMADA_BIBLIOMETRICA={len(ids_372)}")
    print(f"NUCLEO_TEMATICO={len(ids_121)}")
    print(f"INTERSECAO_372_121={len(intersecao)}")
    print(f"EXCLUSIVOS_372={len(ids_372 - ids_121)}")
    print(f"EXCLUSIVOS_121={len(ids_121 - ids_372)}")
    print(f"SAIDA={SAIDA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
