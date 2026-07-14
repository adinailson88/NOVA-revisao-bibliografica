"""Executa o verificador completo com os controles atualizados das strings IA/ML.

O arquivo original ``verificar_artigo.py`` permanece como base das verificações acumuladas.
Este adaptador substitui apenas os dois blocos que exigiam a permanência das antigas lacunas
documentais, mantendo todas as demais asserções do verificador.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "scripts" / "python" / "verificar_artigo.py"
PROTOCOLO = ROOT / "01_PROTOCOLO" / "strings_busca_sensibilidade_ia_ml_20260712.md"

fonte = ORIGINAL.read_text(encoding="utf-8")

bloco_lacunas = '''consultas_nao_preservadas = [
    linha["string_id"]
    for linha in buscas
    if linha["consulta_documentada"] == "Informação insuficiente para verificar."
]
exigir(
    consultas_nao_preservadas
    == ["scopus_nucleo_a5_sensibilidade_ia_ml", "wos_nucleo_a5_sensibilidade_ia_ml"],
    f"Lacunas documentais das strings de sensibilidade divergentes: {consultas_nao_preservadas}",
)
'''

bloco_documentado = '''consultas_nao_preservadas = [
    linha["string_id"]
    for linha in buscas
    if linha["consulta_documentada"] == "Informação insuficiente para verificar."
]
exigir(
    consultas_nao_preservadas == [],
    f"Ainda existem lacunas documentais nas strings de sensibilidade: {consultas_nao_preservadas}",
)
linhas_sensibilidade = {
    linha["string_id"]: linha
    for linha in buscas
    if linha["rodada"] == "sensibilidade_ia_ml"
}
scopus_ia = linhas_sensibilidade["scopus_nucleo_a5_sensibilidade_ia_ml"]
wos_ia = linhas_sensibilidade["wos_nucleo_a5_sensibilidade_ia_ml"]
exigir(scopus_ia["consulta_documentada"].startswith("TITLE-ABS-KEY("), "String Scopus IA/ML ausente ou inválida.")
exigir("machine learning" in scopus_ia["consulta_documentada"], "Bloco de IA/ML ausente na string Scopus.")
exigir("PUBYEAR > 2009" in scopus_ia["consulta_documentada"] and "PUBYEAR < 2027" in scopus_ia["consulta_documentada"], "Período ausente na string Scopus.")
exigir(wos_ia["consulta_documentada"].startswith("TS=("), "String Web of Science IA/ML ausente ou inválida.")
exigir("machine learning" in wos_ia["consulta_documentada"], "Bloco de IA/ML ausente na string Web of Science.")
exigir("PY=(2010-2026)" in wos_ia["consulta_documentada"], "Período ausente na string Web of Science.")
exigir("All Databases" in wos_ia["observacao"], "A opção All Databases deve estar documentada para a Web of Science.")
exigir("nenhum filtro adicional" in scopus_ia["observacao"].lower(), "Ausência de filtros adicionais não documentada para a Scopus.")
exigir("nenhum filtro adicional" in wos_ia["observacao"].lower(), "Ausência de filtros adicionais não documentada para a Web of Science.")
'''

bloco_texto_antigo = '''exigir(
    texto_tex.count("String nativa exata não preservada") == 2,
    "As duas lacunas documentais de string nativa devem permanecer explícitas na tabela.",
)
'''

bloco_texto_novo = '''exigir(
    "String nativa exata não preservada" not in texto_tex,
    "O artigo ainda apresenta como ausentes strings que já foram documentadas.",
)
for declaracao in (
    "Web of Science -- All Databases",
    "String integral documentada",
    "sem filtros adicionais além do período",
):
    exigir(declaracao in texto_tex, f"Documentação atualizada da busca de sensibilidade ausente: {declaracao}")
'''

if bloco_lacunas not in fonte:
    raise RuntimeError("Bloco antigo de lacunas não localizado em verificar_artigo.py.")
if bloco_texto_antigo not in fonte:
    raise RuntimeError("Bloco antigo de controle textual não localizado em verificar_artigo.py.")

fonte = fonte.replace(bloco_lacunas, bloco_documentado, 1)
fonte = fonte.replace(bloco_texto_antigo, bloco_texto_novo, 1)

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

exec(compile(fonte, str(ORIGINAL), "exec"), {"__name__": "__main__", "__file__": str(ORIGINAL)})
