"""Complementa referencias/ com planilhas XLSX e o nucleo final, para auditoria externa.

Uso: python scripts/python/14_gerar_planilhas_auditoria_referencias.py
(rodar depois de scripts/python/12_gerar_lista_referencias.py)

Gera em referencias/:
    lista_referencias.xlsx          -> copia em XLSX de lista_referencias.csv (35 citadas)
    nucleo_final_104_registros.csv  -> copia de 07_SINTESE_TEMATICA/matriz_base_nucleo_final_104.csv
    nucleo_final_104_registros.xlsx -> versao XLSX do arquivo acima

O nucleo final de 104 registros e a base completa que fundamenta a sintese
tematica do artigo (RQs confirmadas, dimensoes, criterios, metodos, nivel de
confianca); as 35 referencias citadas em lista_referencias.csv sao um
subconjunto de uso direto no texto, mais literatura de apoio metodologico que
nao pertence ao corpus bibliometrico. Ver referencias/README.md.
"""
import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[2]
REFERENCIAS = ROOT / "referencias"
NUCLEO_104 = ROOT / "07_SINTESE_TEMATICA" / "matriz_base_nucleo_final_104.csv"


def csv_para_xlsx(origem_csv, destino_xlsx, delimitador, nome_aba):
    wb = Workbook()
    ws = wb.active
    ws.title = nome_aba[:31]
    with open(origem_csv, encoding="utf-8-sig", newline="") as f:
        for i, row in enumerate(csv.reader(f, delimiter=delimitador), start=1):
            ws.append(row)
            if i == 1:
                for cell in ws[1]:
                    cell.font = Font(bold=True)
    ws.freeze_panes = "A2"
    for col_cells in ws.columns:
        largura = max((len(str(c.value)) if c.value is not None else 0) for c in col_cells)
        ws.column_dimensions[get_column_letter(col_cells[0].column)].width = min(60, max(10, largura + 2))
    wb.save(destino_xlsx)


if __name__ == "__main__":
    lista_csv = REFERENCIAS / "lista_referencias.csv"
    if not lista_csv.exists():
        raise SystemExit(
            "referencias/lista_referencias.csv nao encontrado. "
            "Rode antes: python scripts/python/12_gerar_lista_referencias.py"
        )
    csv_para_xlsx(lista_csv, REFERENCIAS / "lista_referencias.xlsx", ",", "Referencias citadas")
    print("lista_referencias.xlsx gerado")

    destino_csv = REFERENCIAS / "nucleo_final_104_registros.csv"
    destino_csv.write_bytes(NUCLEO_104.read_bytes())
    csv_para_xlsx(destino_csv, REFERENCIAS / "nucleo_final_104_registros.xlsx", ",", "Nucleo final 104")
    print("nucleo_final_104_registros.csv/.xlsx gerados")
