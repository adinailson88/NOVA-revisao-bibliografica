"""Executa o verificador completo com controles editoriais atualizados.

O arquivo original ``verificar_artigo.py`` permanece como base das verificações acumuladas.
Este adaptador substitui controles textuais obsoletos e acrescenta testes de regressão para
as revisões metodológica e editorial.
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

bloco_estilo_antigo = '''exigir(" -- " not in texto_prosa, "Foi encontrado travessao em sintaxe LaTeX no artigo.")
'''
bloco_estilo_novo = '''texto_prosa_sem_base_wos = texto_prosa.replace("Web of Science -- All Databases", "Web of Science All Databases")
exigir(" -- " not in texto_prosa_sem_base_wos, "Foi encontrado travessao em sintaxe LaTeX no artigo.")
'''

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

bloco_restricao_antigo = '''exigir(
    "github.event_name == 'workflow_dispatch' || github.ref == 'refs/heads/main'" in workflow,
    "PDF e Word devem permanecer restritos a execucao manual ou main.",
)
'''
bloco_restricao_atual = '''exigir(
    "python scripts/python/gerar_produtos_artigo_nucleo_ampliado.py" in workflow,
    "O workflow final deve continuar gerando os produtos temáticos vigentes.",
)
'''

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

substituicoes = (
    (bloco_estilo_antigo, bloco_estilo_novo, "controle editorial"),
    (bloco_lacunas, bloco_documentado, "lacunas das strings"),
    (bloco_texto_antigo, bloco_texto_novo, "controle textual"),
    (bloco_restricao_antigo, bloco_restricao_atual, "restrição de compilação"),
    (bloco_limitacoes_antigo, bloco_limitacoes_novo, "limitações consolidadas"),
    (bloco_textocompleto_antigo, bloco_textocompleto_novo, "uso pontual de texto completo"),
    (
        "Rastreabilidade entre evidências e especificação operacional",
        "Rastreabilidade entre evidências e critérios candidatos",
        "título da tabela de rastreabilidade",
    ),
    (
        "Matriz analítica conceitual informada pela síntese da literatura",
        "Matriz de indicadores e fluxo para parametrização multicritério",
        "identidade da matriz",
    ),
    (
        "As frequências não constituem pesos da matriz.",
        "As frequências sustentam a seleção inicial, enquanto pesos e importância normativa serão definidos na validação institucional.",
        "declaração sobre frequências e pesos",
    ),
    (
        "ela funciona como eixo transversal",
        "a dimensão ciclo de vida atua transversalmente",
        "transversalidade do ciclo de vida",
    ),
    (
        "não é um modelo validado nem um instrumento pronto para decisão",
        "O produto entrega uma especificação para validação futura",
        "estado da especificação",
    ),
    (
        '"matriz analítica conceitual informada pela síntese da literatura",',
        '"Matriz de indicadores e fluxo para parametrização multicritério",',
        "padronização terminológica da matriz",
    ),
    (
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
    (
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
    (
        "não foram acrescentados à camada bibliométrica de 372",
        "não foram acrescentados à camada de 372",
        "separação entre busca direcionada e camada bibliométrica",
    ),
)

for antigo, novo, nome in substituicoes:
    if antigo not in fonte:
        raise RuntimeError(f"Bloco antigo não localizado em verificar_artigo.py: {nome}.")
    fonte = fonte.replace(antigo, novo, 1)

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

controles_parecer = (
    "especificação para parametrização multicritério",
    "109 dos 121 registros do núcleo temático vigente também pertencem ao estrato bibliométrico de 372",
    "Doze registros (9,9\\%) foram classificados especificamente",
    "proposições do autor para validação institucional",
    "O produto entrega uma especificação para validação futura",
    "A contribuição central é uma especificação operacional candidata e rastreável",
    "Intensidade energética em base móvel de 12 meses",
)
for trecho in controles_parecer:
    if trecho not in texto_artigo:
        raise AssertionError(f"Correção do parecer ausente no artigo: {trecho}")

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
