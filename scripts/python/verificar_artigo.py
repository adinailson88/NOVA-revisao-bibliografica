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
nucleo = ler_csv("nucleo_final_pos_auditoria_resumos.csv")
exigir(len(nucleo) == 104, "O nucleo final deve ter 104 registros.")
ids = [linha["id_unico"] for linha in nucleo]
exigir(len(ids) == len(set(ids)), "id_unico duplicado no nucleo final.")

contagem_bases = {"Scopus": 0, "WoS": 0, "Crossref": 0}
combinacoes: dict[str, int] = {}
for linha in nucleo:
    combinacao = linha["bases_origem"]
    combinacoes[combinacao] = combinacoes.get(combinacao, 0) + 1
    for base in combinacao.split("|"):
        contagem_bases[base] += 1
exigir(contagem_bases == {"Scopus": 98, "WoS": 49, "Crossref": 6}, f"Bases divergentes: {contagem_bases}")
exigir(
    combinacoes
    == {
        "Scopus": 52,
        "Scopus|WoS": 41,
        "WoS": 5,
        "Crossref|Scopus|WoS": 3,
        "Crossref|Scopus": 2,
        "Crossref": 1,
    },
    f"Combinacoes de proveniencia divergentes: {combinacoes}",
)

# Estrategia de busca
buscas = ler_csv("tabela_estrategia_busca.csv")
total_bruto = sum(inteiro(linha["retorno_bruto"]) for linha in buscas)
exigir(total_bruto == 12118, f"Total bruto divergente: {total_bruto}")
n_consultas = {
    base: sum(
        1
        for linha in buscas
        if linha["base"] == base and "complemento_manual" not in linha["string_id"]
    )
    for base in ("Scopus", "Web of Science", "Crossref")
}
exigir(
    n_consultas == {"Scopus": 4, "Web of Science": 4, "Crossref": 5},
    f"Numero de consultas divergente: {n_consultas}",
)

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

# Tabelas geradas pelo R
dimensoes = ler_csv("tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv")
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

tipos = ler_csv("tabela34_tipos_documentais_harmonizados_nucleo_final_104.csv")
tipos_obtidos = {linha["tipo_harmonizado"]: inteiro(linha["total_registros"]) for linha in tipos}
exigir(
    tipos_obtidos
    == {
        "Artigo de periodico": 79,
        "Trabalho em evento": 15,
        "Livro ou serie de livro": 10,
    },
    f"Tipos documentais divergentes: {tipos_obtidos}",
)

mencoes = ler_csv("tabela35_mencoes_ods_esg_nucleo_final_104.csv")
mencoes_obtidas = {linha["marcador"]: inteiro(linha["total_registros"]) for linha in mencoes}
exigir(mencoes_obtidas == {"ODS ou SDG": 1, "ESG": 0}, f"ODS/ESG divergentes: {mencoes_obtidas}")

# Todo grafico citado deve ser produzido por um script versionado
script_r = SCRIPT_R.read_text(encoding="utf-8")
script_bib = SCRIPT_BIB.read_text(encoding="utf-8")
graficos_citados = set(re.findall(r"\{figuras/([^}]+\.(?:png|pdf))\}", texto_tex))
for grafico in graficos_citados:
    nome_base = grafico.rsplit(".", 1)[0]
    exigir(
        grafico in script_r or grafico in script_bib or nome_base in script_r or nome_base in script_bib,
        f"Grafico sem geracao em script versionado: {grafico}",
    )


# Auditoria ampliada dos resultados (Etapa 10)
def mapa_totais(nome: str, chave: str) -> dict[str, int]:
    return {linha[chave]: inteiro(linha["total_registros"]) for linha in ler_csv(nome)}


dimensoes_totais = mapa_totais(
    "tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv",
    "dimensao_identificada_leitura",
)
exigir(
    dimensoes_totais
    == {
        "tecnica_operacional": 102,
        "institucional": 92,
        "ambiental": 84,
        "ciclo_de_vida": 60,
        "economica": 59,
        "social": 57,
    },
    f"Dimensoes divergentes: {dimensoes_totais}",
)

criterios_totais = mapa_totais("tabela26_criterios_nucleo_final_104.csv", "criterio")
exigir(
    criterios_totais
    == {
        "desempenho_operacional": 93,
        "informacao_dados": 76,
        "custo": 60,
        "vida_util": 40,
        "energia": 36,
        "risco": 31,
        "condicao_fisica": 27,
        "manutenibilidade": 19,
        "conforto": 17,
        "seguranca": 17,
        "emissoes_carbono": 15,
        "residuos": 13,
        "satisfacao_usuario": 9,
        "qualidade_servico": 6,
        "agua": 5,
    },
    f"Criterios divergentes: {criterios_totais}",
)

metodos_totais = mapa_totais(
    "tabela28_metodos_decisao_nucleo_final_104.csv",
    "metodo_identificado_leitura",
)
exigir(
    metodos_totais
    == {
        "framework": 96,
        "BIM": 26,
        "decision support": 25,
        "optimization": 18,
        "scoring": 17,
        "life-cycle cost": 13,
        "fuzzy": 10,
        "ranking": 9,
        "IoT": 9,
        "machine learning": 9,
        "digital twin": 8,
        "AHP": 5,
        "TOPSIS": 4,
        "ANP": 2,
        "Delphi": 3,
        "MCDM": 3,
        "Bayesian Best Worst Method": 1,
        "balanced scorecard": 1,
        "case-based reasoning": 1,
    },
    f"Metodos divergentes: {metodos_totais}",
)

contextos_totais = mapa_totais(
    "tabela29_contexto_edificacao_nucleo_final_104.csv",
    "contexto_identificado_leitura",
)
exigir(
    contextos_totais
    == {
        "edificio_generico": 93,
        "portfolio_predial": 58,
        "hospital": 17,
        "edificio_comercial": 15,
        "edificio_residencial": 12,
        "universidade": 11,
        "campus": 10,
        "edificio_publico": 5,
        "escola": 5,
        "patrimonio_historico": 4,
        "museu": 1,
        "nao_identificado_no_resumo": 1,
    },
    f"Contextos divergentes: {contextos_totais}",
)

lacunas_totais = mapa_totais("tabela30_lacunas_nucleo_final_104.csv", "categoria")
exigir(
    lacunas_totais
    == {
        "com_lacuna_identificada_no_resumo": 76,
        "sem_lacuna_identificada_no_resumo": 28,
        "lacuna_especifica_ies_publicas": 12,
    },
    f"Lacunas divergentes: {lacunas_totais}",
)

temporal = mapa_totais("tabela33_distribuicao_temporal_nucleo_final_104.csv", "ano")
exigir(sum(temporal.values()) == 104, f"Total temporal divergente: {sum(temporal.values())}")
exigir(sum(v for a, v in temporal.items() if 2019 <= int(a) <= 2026) == 88, "Total de 2019 a 2026 divergente.")
exigir(temporal.get("2025") == 25, f"Total de 2025 divergente: {temporal.get('2025')}")

contribuicoes_totais = mapa_totais(
    "tabela36_tipo_contribuicao_artigo_nucleo_final_104.csv",
    "tipo_contribuicao",
)
exigir(
    contribuicoes_totais
    == {
        "criterios_de_sustentabilidade": 104,
        "criterios_de_priorizacao": 104,
        "metodo_multicriterio_ou_decisao": 80,
        "gestao_manutencao_predial": 104,
        "facility_management": 57,
        "energia_desempenho_operacional": 97,
        "custo_ciclo_de_vida": 82,
        "risco_seguranca_conforto": 53,
        "contexto_publico_universitario": 17,
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
    "Trinta estudos com PDF disponível foram posteriormente lidos",
    "A unidade de análise quantitativa é o registro bibliográfico consolidado.",
):
    exigir(declaracao in texto_tex, f"Limitacao obrigatoria ausente: {declaracao}")


# Uso pontual adicional de texto completo
exigir(
    "30 estudos com PDF disponível foram lidos integralmente; 14 forneceram evidências específicas" in texto_tex,
    "O método deve registrar os dois lotes de texto completo.",
)
for chave in (
    "aldairi_lean6sbm_2017",
    "yoon_fuzzyfm_2018",
    "park_cbrfuzzyahp_2019",
    "chew_manutenibilidadeverde_2016",
    "talib_hospitalfm_2013",
    "conejos_verticalgreenery_2019",
    "tan_fluxoinformacao_2018",
):
    exigir(chave in chaves_citadas, f"Estudo de texto completo sem citacao: {chave}")


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

print("Verificacao do artigo concluida sem divergencias.")
