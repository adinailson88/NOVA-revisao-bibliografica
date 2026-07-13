"""Valida coerencia numerica, estilo, citacoes e rastreabilidade do artigo."""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIGO = ROOT / "latex-artigo"
SECOES = ARTIGO / "sections"
FONTES = ARTIGO / "fontes"
PROCESSADOS = ROOT / "03_PROCESSADOS"
TRIAGEM = ROOT / "04_TRIAGEM"
SINTESE = ROOT / "07_SINTESE_TEMATICA"
SCRIPT_R = ROOT / "scripts" / "r" / "10_gerar_produtos_artigo.R"
SCRIPT_NUCLEO_AMPLIADO = ROOT / "scripts" / "python" / "gerar_produtos_artigo_nucleo_ampliado.py"
SCRIPT_BIB = ROOT / "scripts" / "python" / "11_gerar_bibliometria_ampliada.py"


def ler_csv(nome: str) -> list[dict[str, str]]:
    with (FONTES / nome).open(encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def ler_csv_caminho(caminho: Path) -> list[dict[str, str]]:
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def ler_tsv_caminho(caminho: Path) -> list[dict[str, str]]:
    with caminho.open(encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo, delimiter="\t"))


def normalizar_doi(valor: str) -> str:
    doi = (valor or "").strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.rstrip(".").strip()


def inteiro(valor: str) -> int:
    return int(float(valor))


def exigir(condicao: bool, mensagem: str) -> None:
    if not condicao:
        raise AssertionError(mensagem)


tex_arquivos = [ARTIGO / "main.tex", *sorted(SECOES.glob("*.tex"))]
texto_tex = "\n".join(p.read_text(encoding="utf-8") for p in tex_arquivos)
texto_prosa = "\n".join(
    linha for linha in texto_tex.splitlines() if not linha.lstrip().startswith("\\draw")
)

# Estilo solicitado
exigir("Rascunho" not in texto_tex and "rascunho" not in texto_tex, "Subtitulo de rascunho ainda presente.")
exigir(not re.search(r"[–—]", texto_prosa), "Foi encontrado travessao Unicode no artigo.")
exigir(" -- " not in texto_prosa, "Foi encontrado travessao em sintaxe LaTeX no artigo.")
exigir("\\captionsetup{labelsep=period" in texto_tex, "Separador de legenda deve ser ponto.")
exigir("\\texttt{fontes/" not in texto_tex, "Fonte de tabela nao deve expor caminho de arquivo.")
exigir(".md}" not in texto_tex and ".md)" not in texto_tex, "Referencia a arquivo Markdown no artigo.")
# Transparencia metodologica da triagem
exigir("Não houve segundo avaliador independente." in texto_tex, "O artigo deve declarar a ausência de segundo avaliador.")
exigir("não constitui evidência de uso do ASReview" in texto_tex, "O artigo não pode atribuir uso de ASReview sem evidência.")

# Quantidade e nao redundancia estrutural
exigir(texto_tex.count("\\begin{table}") == 11, "O artigo deve conter onze tabelas, incluindo correntes teoricas, rastreabilidade do protocolo e especificacao dos indicadores.")
exigir(texto_tex.count("\\begin{figure}") == 11, "O artigo deve conter dois fluxogramas, cinco graficos tematicos e quatro produtos bibliometricos.")
exigir(texto_tex.count("\\captiongrafico{") == 9, "Os nove produtos quantitativos devem ser chamados de Graficos.")
exigir("figura10_distribuicao_base_tipo" not in texto_tex, "Grafico redundante de base e tipo ainda citado.")
exigir("tab:funil}" not in texto_tex, "Tabela redundante do funil ainda citada.")
exigir("tab:temporal" not in texto_tex, "Tabela temporal redundante ainda citada.")
exigir("tab:dimensoes" not in texto_tex, "Tabela de dimensoes redundante ainda citada.")
exigir("tab:metodos" not in texto_tex, "Tabela de metodos redundante ainda citada.")
exigir("tab:matrizanalitica" not in texto_tex, "Tabela redundante da matriz ainda citada.")
exigir("tab:lacunas" not in texto_tex, "Tabela de lacunas redundante ainda citada.")

# Citacoes e bibliografia
bib = (ARTIGO / "references.bib").read_text(encoding="utf-8")
chaves_bib = set(re.findall(r"@\w+\{([^,]+),", bib))
chaves_citadas: set[str] = set()
for grupo in re.findall(r"\\(?:textcite|parencite)\{([^}]+)\}", texto_tex):
    chaves_citadas.update(chave.strip() for chave in grupo.split(","))
exigir(not (chaves_citadas - chaves_bib), f"Citacoes sem referencia: {sorted(chaves_citadas - chaves_bib)}")
exigir(not (chaves_bib - chaves_citadas), f"Referencias nao citadas: {sorted(chaves_bib - chaves_citadas)}")
exigir("@phdthesis" not in bib.lower() and "@mastersthesis" not in bib.lower(), "Tese ou dissertacao na bibliografia.")
exigir(len(re.findall(r"@article\{", bib, flags=re.I)) >= 16, "Bibliografia cientifica insuficiente.")

# Corpus final
# O nucleo foi ampliado de 104 para 121 registros em 2026-07-12 pela busca complementar de
# sensibilidade para IA/aprendizado de maquina (docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md,
# docs/RELATORIO_EXECUCAO_R_NUCLEO_AMPLIADO.md). O arquivo historico de 104 registros
# (nucleo_final_pos_auditoria_resumos.csv) permanece preservado, sem sobrescrita; o arquivo
# vigente para o artigo passa a ser a versao ampliada.
nucleo = ler_csv("nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv")
exigir(len(nucleo) == 121, "O nucleo final deve ter 121 registros (104 originais + 17 da busca de sensibilidade IA/ML).")
ids = [linha["id_unico"] for linha in nucleo]
exigir(len(ids) == len(set(ids)), "id_unico duplicado no nucleo final.")

contagem_bases = {"Scopus": 0, "WoS": 0, "Crossref": 0}
combinacoes: dict[str, int] = {}
for linha in nucleo:
    combinacao = linha["bases_origem"]
    combinacoes[combinacao] = combinacoes.get(combinacao, 0) + 1
    for base in combinacao.split("|"):
        contagem_bases[base] += 1
exigir(contagem_bases == {"Scopus": 113, "WoS": 51, "Crossref": 6}, f"Bases divergentes: {contagem_bases}")
exigir(
    combinacoes
    == {
        "Scopus": 67,
        "Scopus|WoS": 41,
        "WoS": 7,
        "Crossref|Scopus|WoS": 3,
        "Crossref|Scopus": 2,
        "Crossref": 1,
    },
    f"Combinacoes de proveniencia divergentes: {combinacoes}",
)

# Estrategia de busca
buscas = ler_csv("tabela_estrategia_busca.csv")
exigir(len(buscas) == 26, f"Linhas da estratégia unificada divergentes: {len(buscas)}")

totais_rodada: dict[str, int] = {}
for linha in buscas:
    rodada = linha["rodada"]
    totais_rodada[rodada] = totais_rodada.get(rodada, 0) + inteiro(linha["retorno_bruto"])
exigir(
    totais_rodada == {"principal": 12118, "sensibilidade_ia_ml": 6728},
    f"Totais por rodada divergentes: {totais_rodada}",
)
exigir(
    sum(totais_rodada.values()) == 18846,
    "A soma operacional das duas rodadas deve ser 18.846 ocorrencias, sem equivaler a corpus homogeneo.",
)

def contar_consultas(rodada: str, base: str) -> int:
    return sum(
        1
        for linha in buscas
        if linha["rodada"] == rodada
        and linha["base"] == base
        and "complemento_manual" not in linha["string_id"]
    )


consultas_principais = {
    base: contar_consultas("principal", base)
    for base in ("Scopus", "Web of Science", "Crossref")
}
exigir(
    consultas_principais == {"Scopus": 4, "Web of Science": 4, "Crossref": 5},
    f"Número de consultas principais divergente: {consultas_principais}",
)
consultas_sensibilidade = {
    base: contar_consultas("sensibilidade_ia_ml", base)
    for base in ("Scopus", "Web of Science", "Crossref")
}
exigir(
    consultas_sensibilidade == {"Scopus": 1, "Web of Science": 1, "Crossref": 10},
    f"Número de consultas de sensibilidade divergente: {consultas_sensibilidade}",
)

consultas_nao_preservadas = [
    linha["string_id"]
    for linha in buscas
    if linha["consulta_documentada"] == "Informação insuficiente para verificar."
]
exigir(
    consultas_nao_preservadas
    == ["scopus_nucleo_a5_sensibilidade_ia_ml", "wos_nucleo_a5_sensibilidade_ia_ml"],
    f"Lacunas documentais das strings de sensibilidade divergentes: {consultas_nao_preservadas}",
)
for linha in buscas:
    exigir(linha["data_execucao"].strip() != "", f"Data ausente em {linha['string_id']}")
    exigir(linha["periodo"] == "2010-2026", f"Período divergente em {linha['string_id']}")
    exigir(linha["consulta_documentada"].strip() != "", f"Consulta não documentada em {linha['string_id']}")


# Produtos processados da deduplicacao
normalizados = ler_csv_caminho(PROCESSADOS / "registros_normalizados.csv")
consolidado = ler_csv_caminho(PROCESSADOS / "corpus_consolidado.csv")
grupos_duplicados = ler_csv_caminho(PROCESSADOS / "duplicatas_detectadas.csv")

exigir(len(normalizados) == 12118, f"Registros normalizados divergentes: {len(normalizados)}")
exigir(len(consolidado) == 9542, f"Corpus consolidado divergente: {len(consolidado)}")
exigir(len(grupos_duplicados) == 1808, f"Grupos duplicados divergentes: {len(grupos_duplicados)}")

removidos = sum(inteiro(linha["n_registros_agrupados"]) - 1 for linha in grupos_duplicados)
exigir(removidos == 2576, f"Ocorrencias removidas divergentes: {removidos}")

criterios_duplicacao: dict[str, int] = {}
for linha in grupos_duplicados:
    criterio = linha["criterio_agrupamento"]
    criterios_duplicacao[criterio] = criterios_duplicacao.get(criterio, 0) + 1
exigir(
    criterios_duplicacao
    == {"doi_e_titulo": 1616, "doi": 19, "titulo_normalizado": 173},
    f"Criterios de deduplicacao divergentes: {criterios_duplicacao}",
)

ids_consolidados = [linha["id_unico"] for linha in consolidado]
exigir(len(ids_consolidados) == len(set(ids_consolidados)), "id_unico duplicado no corpus consolidado.")

dois = [normalizar_doi(linha["doi"]) for linha in consolidado if normalizar_doi(linha["doi"])]
exigir(len(dois) == len(set(dois)), "DOI normalizado duplicado permaneceu no corpus consolidado.")

for linha in consolidado:
    exigir(linha["bases_origem"].strip() != "", f"Proveniencia de base ausente em {linha['id_unico']}")
    exigir(linha["strings_origem"].strip() != "", f"Proveniencia de consulta ausente em {linha['id_unico']}")
    exigir(linha["ids_brutos_agrupados"].strip() != "", f"IDs brutos ausentes em {linha['id_unico']}")

# Produtos da triagem e auditoria
pre_triagem = ler_csv_caminho(TRIAGEM / "matriz_pre_triagem.csv")
amostra_auditoria = ler_csv_caminho(TRIAGEM / "_amostra_auditoria_bruta.csv")
decisoes_duvida = ler_tsv_caminho(TRIAGEM / "decisao_duvidas_revisada.tsv")
nucleo_reavaliado = ler_csv_caminho(SINTESE / "matriz_extracao_final_reavaliada_resumos.csv")
nucleo_central = ler_csv_caminho(SINTESE / "nucleo_principal_sintese_artigo.csv")
auditoria_137 = ler_csv_caminho(SINTESE / "auditoria_qualitativa_resumos_137.csv")

exigir(len(pre_triagem) == 9542, f"Pré-triagem divergente: {len(pre_triagem)}")
exigir(len(amostra_auditoria) == 100, f"Amostra de auditoria divergente: {len(amostra_auditoria)}")
exigir(len(decisoes_duvida) == 4276, f"Decisões de dúvida divergentes: {len(decisoes_duvida)}")
decisoes_obtidas: dict[str, int] = {}
for linha in decisoes_duvida:
    decisao = linha["decisao_revisada"]
    decisoes_obtidas[decisao] = decisoes_obtidas.get(decisao, 0) + 1
exigir(decisoes_obtidas == {"RELEVANTE": 206, "DESCARTAR": 4070}, f"Resolução das dúvidas divergente: {decisoes_obtidas}")
exigir(len(nucleo_reavaliado) == 3678, f"Núcleo reavaliado divergente: {len(nucleo_reavaliado)}")
exigir(len(nucleo_central) == 137, f"Núcleo central divergente: {len(nucleo_central)}")
exigir(len(auditoria_137) == 137, f"Auditoria qualitativa divergente: {len(auditoria_137)}")

# Tabelas geradas pelo pipeline do nucleo ampliado (121)
dimensoes = ler_csv("tabela27_dimensoes_sustentabilidade_nucleo_ampliado_121.csv")
dimensoes_esperadas = {
    "tecnica_operacional",
    "institucional",
    "ambiental",
    "ciclo_de_vida",
    "economica",
    "social",
}
exigir(
    {linha["dimensao_identificada_leitura"] for linha in dimensoes} == dimensoes_esperadas,
    "Tabela de dimensoes contem criterios ou perdeu dimensoes canonicas.",
)

tipos = ler_csv("tabela34_tipos_documentais_harmonizados_nucleo_ampliado_121.csv")
tipos_obtidos = {linha["tipo_harmonizado"]: inteiro(linha["total_registros"]) for linha in tipos}
exigir(
    tipos_obtidos
    == {
        "Artigo de periodico": 90,
        "Trabalho em evento": 20,
        "Livro ou serie de livro": 11,
    },
    f"Tipos documentais divergentes: {tipos_obtidos}",
)

mencoes = ler_csv("tabela35_mencoes_ods_esg_nucleo_ampliado_121.csv")
mencoes_obtidas = {linha["marcador"]: inteiro(linha["total_registros"]) for linha in mencoes}
exigir(mencoes_obtidas == {"ODS ou SDG": 1, "ESG": 0}, f"ODS/ESG divergentes: {mencoes_obtidas}")

# Todo grafico citado deve ser produzido por um script versionado
script_r = SCRIPT_R.read_text(encoding="utf-8")
script_nucleo_ampliado = SCRIPT_NUCLEO_AMPLIADO.read_text(encoding="utf-8")
script_bib = SCRIPT_BIB.read_text(encoding="utf-8")
graficos_citados = set(re.findall(r"\{figuras/([^}]+\.(?:png|pdf))\}", texto_tex))
for grafico in graficos_citados:
    nome_base = grafico.rsplit(".", 1)[0]
    exigir(
        grafico in script_r
        or grafico in script_nucleo_ampliado
        or grafico in script_bib
        or nome_base in script_r
        or nome_base in script_nucleo_ampliado
        or nome_base in script_bib,
        f"Grafico sem geracao em script versionado: {grafico}",
    )


# Auditoria ampliada dos resultados (Etapa 10)
def mapa_totais(nome: str, chave: str) -> dict[str, int]:
    return {linha[chave]: inteiro(linha["total_registros"]) for linha in ler_csv(nome)}


dimensoes_totais = mapa_totais(
    "tabela27_dimensoes_sustentabilidade_nucleo_ampliado_121.csv",
    "dimensao_identificada_leitura",
)
exigir(
    dimensoes_totais
    == {
        "tecnica_operacional": 116,
        "institucional": 97,
        "ambiental": 92,
        "ciclo_de_vida": 65,
        "economica": 63,
        "social": 59,
    },
    f"Dimensoes divergentes: {dimensoes_totais}",
)

criterios_totais = mapa_totais("tabela26_criterios_nucleo_ampliado_121.csv", "criterio")
exigir(
    criterios_totais
    == {
        "desempenho_operacional": 99,
        "informacao_dados": 82,
        "custo": 63,
        "energia": 44,
        "vida_util": 44,
        "condicao_fisica": 34,
        "risco": 33,
        "manutenibilidade": 25,
        "conforto": 22,
        "seguranca": 18,
        "emissoes_carbono": 15,
        "residuos": 13,
        "satisfacao_usuario": 9,
        "agua": 6,
        "qualidade_servico": 6,
    },
    f"Criterios divergentes: {criterios_totais}",
)

metodos_totais = mapa_totais(
    "tabela28_metodos_decisao_nucleo_ampliado_121.csv",
    "metodo_identificado_leitura",
)
exigir(
    metodos_totais
    == {
        "framework": 101,
        "decision support": 29,
        "BIM": 28,
        "machine learning": 26,
        "optimization": 19,
        "scoring": 17,
        "life-cycle cost": 16,
        "IoT": 13,
        "digital twin": 11,
        "fuzzy": 11,
        "ranking": 9,
        "AHP": 5,
        "TOPSIS": 4,
        "Delphi": 3,
        "MCDM": 3,
        "ANP": 2,
        "Bayesian Best Worst Method": 1,
        "balanced scorecard": 1,
        "case-based reasoning": 1,
    },
    f"Metodos divergentes: {metodos_totais}",
)

contextos_totais = mapa_totais(
    "tabela29_contexto_edificacao_nucleo_ampliado_121.csv",
    "contexto_identificado_leitura",
)
exigir(
    contextos_totais
    == {
        "edificio_generico": 101,
        "portfolio_predial": 59,
        "hospital": 17,
        "edificio_comercial": 16,
        "edificio_residencial": 15,
        "universidade": 14,
        "campus": 10,
        "patrimonio_historico": 6,
        "edificio_publico": 5,
        "escola": 5,
        "museu": 1,
        "nao_identificado_no_resumo": 1,
    },
    f"Contextos divergentes: {contextos_totais}",
)

lacunas_totais = mapa_totais("tabela30_lacunas_nucleo_ampliado_121.csv", "categoria")
exigir(
    lacunas_totais
    == {
        "com_lacuna_identificada_no_resumo": 76,
        "sem_lacuna_identificada_no_resumo": 45,
        "lacuna_especifica_ies_publicas": 12,
    },
    f"Lacunas divergentes: {lacunas_totais}",
)

temporal = mapa_totais("tabela33_distribuicao_temporal_nucleo_ampliado_121.csv", "ano")
exigir(sum(temporal.values()) == 121, f"Total temporal divergente: {sum(temporal.values())}")
exigir(sum(v for a, v in temporal.items() if 2019 <= int(a) <= 2026) == 101, "Total de 2019 a 2026 divergente.")
exigir(temporal.get("2025") == 29, f"Total de 2025 divergente: {temporal.get('2025')}")

contribuicoes_totais = mapa_totais(
    "tabela36_tipo_contribuicao_artigo_nucleo_ampliado_121.csv",
    "tipo_contribuicao",
)
exigir(
    contribuicoes_totais
    == {
        "gestao_manutencao_predial": 115,
        "energia_desempenho_operacional": 105,
        "criterios_de_priorizacao": 104,
        "criterios_de_sustentabilidade": 104,
        "custo_ciclo_de_vida": 86,
        "metodo_multicriterio_ou_decisao": 80,
        "facility_management": 57,
        "risco_seguranca_conforto": 57,
        "contexto_publico_universitario": 20,
        "lacuna_para_ies_publicas": 12,
    },
    f"Tipos de contribuicao divergentes: {contribuicoes_totais}",
)


# Rastreabilidade da matriz analitica (Etapa 12)
exigir("fig:fluxoprotocolo" in texto_tex, "Fluxograma do protocolo ausente.")
exigir("Rastreabilidade entre evidências e especificação operacional" in texto_tex, "Tabela do protocolo deve explicitar a rastreabilidade.")
exigir(
    "Matriz analítica conceitual informada pela síntese da literatura" in texto_tex,
    "A matriz deve ser identificada como sintese conceitual, nao como modelo validado.",
)
exigir(
    "As frequências não constituem pesos da matriz." in texto_tex,
    "A matriz deve declarar que frequencias documentais nao sao pesos.",
)
exigir(
    "ela funciona como eixo transversal" in texto_tex,
    "A dimensao ciclo de vida deve permanecer explicitada como eixo transversal.",
)
exigir(
    "não é um modelo validado nem um instrumento pronto para decisão" in texto_tex,
    "O artigo deve preservar o estado nao validado da matriz.",
)


# Limitacoes metodologicas documentadas (Etapa 13)
for declaracao in (
    "Não houve pré-registro público do protocolo.",
    "sem segundo revisor independente e sem medida de concordância interavaliadores",
    "não foram realizadas busca de citações para frente ou para trás",
    "busca estruturada de literatura cinzenta",
    "Trinta e sete estudos com texto completo disponível foram posteriormente lidos",
    "A unidade de análise quantitativa é o registro bibliográfico consolidado.",
):
    exigir(declaracao in texto_tex, f"Limitacao obrigatoria ausente: {declaracao}")


# Uso pontual adicional de texto completo
exigir(
    "37 estudos com texto completo disponível foram lidos integralmente; 19 forneceram evidências específicas" in texto_tex,
    "O método deve registrar os três lotes de texto completo.",
)
for chave in (
    "aldairi_lean6sbm_2017",
    "yoon_fuzzyfm_2018",
    "park_cbrfuzzyahp_2019",
    "chew_manutenibilidadeverde_2016",
    "talib_hospitalfm_2013",
    "conejos_verticalgreenery_2019",
    "tan_fluxoinformacao_2018",
    "motuziene_ventilacaoia_2025",
    "das_iotai_2025",
    "wu_gnnvidautil_2025",
    "suh_demandaenergiaagua_2012",
    "alici_iotambientes_2026",
):
    exigir(chave in chaves_citadas, f"Estudo de texto completo sem citacao: {chave}")


# Leitura integral dos registros incorporados pela sensibilidade (Etapa 4)
relatorio_ia = ROOT / "docs" / "RELATORIO_USO_TEXTO_COMPLETO_17_REGISTROS_IA_ML.md"
exigir(relatorio_ia.exists(), "Relatorio dos 17 registros IA/ML ausente.")
texto_relatorio_ia = relatorio_ia.read_text(encoding="utf-8")
for declaracao in (
    "17 registros identificados sem ambiguidade",
    "7 textos integrais consultados",
    "5 dos 7 textos lidos acrescentaram",
    "não foram registrados como leitura integral",
):
    exigir(declaracao in texto_relatorio_ia, f"Rastreabilidade da Etapa 4 ausente: {declaracao}")
for id_registro in (
    "REG_02383", "REG_07814", "REG_07815", "REG_05418", "REG_06840",
    "REG_09883", "REG_10348", "REG_10391", "REG_10862", "REG_11003",
    "REG_11158", "REG_11346", "REG_11489", "REG_11552", "REG_12351",
    "REG_12451", "REG_12511",
):
    exigir(id_registro in texto_relatorio_ia, f"Registro ausente no relatorio de texto completo: {id_registro}")


# Sintese cientifica comparativa da RQ6 (Etapa 5)
sintese_ia = ler_csv("tabela_sintese_ia_ml_17.csv")
exigir(len(sintese_ia) == 17, f"Linhas da sintese IA/ML divergentes: {len(sintese_ia)}")
ids_sintese_ia = [linha["id_unico"] for linha in sintese_ia]
exigir(len(ids_sintese_ia) == len(set(ids_sintese_ia)), "id_unico duplicado na sintese IA/ML.")
funcoes_ia: dict[str, int] = {}
bases_documentais_ia: dict[str, int] = {}
for linha in sintese_ia:
    funcoes_ia[linha["funcao_analitica_predominante"]] = (
        funcoes_ia.get(linha["funcao_analitica_predominante"], 0) + 1
    )
    bases_documentais_ia[linha["base_documental"]] = (
        bases_documentais_ia.get(linha["base_documental"], 0) + 1
    )
exigir(
    funcoes_ia
    == {
        "previsao": 8,
        "previsao_otimizacao": 2,
        "diagnostico_classificacao": 2,
        "sintese_integracao": 5,
    },
    f"Funcoes analiticas IA/ML divergentes: {funcoes_ia}",
)
exigir(
    bases_documentais_ia == {"titulo_resumo": 10, "texto_integral": 7},
    f"Base documental IA/ML divergente: {bases_documentais_ia}",
)
for declaracao in (
    "Dez concentram-se em previsão ou previsão combinada à otimização",
    "dois em diagnóstico e classificação de danos",
    "cinco em síntese ou integração tecnológica",
    "Nenhum dos 17 demonstrou uma cadeia completa",
    "Em resposta à RQ6",
):
    exigir(declaracao in texto_tex, f"Sintese comparativa da RQ6 ausente: {declaracao}")


# Padronizacao terminologica e editorial (Etapa 14)
for declaracao in (
    "ambiental, social e de governança (ESG",
    "MCDM designa \\textit{multi-criteria decision-making}",
    "MCDA, \\textit{multi-criteria decision analysis}",
    "AHP corresponde a \\textit{Analytic Hierarchy Process}",
    "TOPSIS a \\textit{Technique for Order Preference by Similarity to Ideal Solution}",
    "ANP a \\textit{Analytic Network Process}",
    "modelagem da informação da construção (BIM",
    "matriz analítica conceitual, informada pela síntese da literatura",
):
    exigir(declaracao in texto_tex, f"Padronizacao terminologica ausente: {declaracao}")


# Referencia metodologica de Hu et al. (Etapa 15)
exigir("hu_revisao_sintese_2026" in chaves_citadas, "Hu et al. deve ser citado apenas no relato metodologico.")
exigir(
    "não implica pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo ou metanálise" in texto_tex,
    "O uso de Hu et al. deve explicitar os procedimentos nao realizados.",
)


# Integracao metodologica da busca complementar de sensibilidade (Etapa 2)
exigir(
    "Como verificação complementar, formulou-se a RQ6" in texto_tex,
    "A introducao deve formular explicitamente a RQ6.",
)
exigir(
    "RQ6 & Efeito da busca de sensibilidade" in texto_tex,
    "A matriz de alinhamento deve incluir a RQ6.",
)
exigir(
    "não foram acrescentados à camada bibliométrica de 372" in texto_tex,
    "O método deve justificar a separacao entre a busca direcionada e a camada bibliometrica.",
)
exigir(
    "O núcleo final de 104 registros permaneceu como base" not in texto_tex,
    "O método ainda apresenta o núcleo histórico de 104 como núcleo final vigente.",
)
exigir(
    "104 registros no núcleo original" in texto_tex,
    "O funil principal deve identificar 104 como núcleo original.",
)


# Estrategia unificada e fluxo em dois bracos (Etapa 3)
for declaracao in (
    "Estratégia de busca consolidada por rodada e base",
    "Subtotal da busca principal",
    "Subtotal da busca de sensibilidade",
    "não constitui corpus homogêneo",
    "Fluxo integrado da busca principal e da busca complementar de sensibilidade",
    "Núcleo temático vigente",
):
    exigir(declaracao in texto_tex, f"Integracao das duas buscas ausente: {declaracao}")
exigir(
    texto_tex.count("String nativa exata não preservada") == 2,
    "As duas lacunas documentais de string nativa devem permanecer explícitas na tabela.",
)
exigir(
    "Fluxo de seleção do corpus" not in texto_tex,
    "A legenda antiga do fluxo ainda está presente.",
)

print("Verificacao do artigo concluida sem divergencias.")
