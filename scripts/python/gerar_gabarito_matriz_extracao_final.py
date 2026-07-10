"""Gera o gabarito vazio (0 linhas de dados) da matriz de extracao final da ETAPA_12.

Cabecalho definido em 07_SINTESE_TEMATICA/matriz_extracao_final_esquema.md, secao 3. Nao le
nenhum dado de entrada -- so escreve o cabecalho final, para servir de modelo ao preenchimento
na etapa seguinte.
"""

import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SAIDA = BASE_DIR / "07_SINTESE_TEMATICA" / "matriz_extracao_final_gabarito.csv"

COLUNAS = [
    # 3.1 metadados e identificacao (herdadas da ETAPA_11)
    "id_unico", "doi", "titulo", "ano", "autores", "fonte_periodico", "tipo_documento",
    "bases_origem", "strings_origem", "resumo_presente", "palavras_chave", "resumo",
    # 3.2 sinalizacao tematica e de metodo (herdadas da ETAPA_11)
    "bloco_a_presente", "bloco_b_presente", "bloco_c_presente", "bloco_d_presente",
    "bloco_tecnologico_presente", "bloco_conceitual_presente", "termos_bloco_a",
    "termos_bloco_b", "usa_topsis", "usa_ahp", "usa_outro_mcdm", "metodo_mcdm_especifico",
    "usa_bim", "usa_digital_twin", "usa_iot", "usa_data_driven", "tecnologia_especifica",
    "tipo_edificacao_sinal", "eixo_tematico_preliminar", "classe_final_sem_duvida",
    "nucleo_analitico_revisado",
    # 3.3 colunas de conteudo final, por titulo+resumo+palavras-chave (definidas na ETAPA_12)
    "pais_contexto", "tipo_aplicacao", "dados_utilizados", "resultado_principal",
    "contribuicao_para_artigo", "lacuna_identificada", "criterios_ambientais",
    "criterios_economicos", "criterios_sociais", "criterios_tecnicos_operacionais",
    "criterios_institucionais", "criterios_risco",
    # 3.4 colunas de controle (novas na ETAPA_12)
    "base_evidencia_extracao", "resumo_suficiente_para_extracao", "uso_no_artigo",
    "observacoes",
]


def main() -> None:
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(COLUNAS)
    print(f"Gabarito gerado: {SAIDA} ({len(COLUNAS)} colunas, 0 linhas de dados)")


if __name__ == "__main__":
    main()
