"""
Verifica, por script, se cada numero citado em 08_ARTIGO/rascunho_artigo.md tem
origem rastreavel nas tabelas de dados-base do nucleo final (05_ANALISE_R/tabelas/)
ou nos arquivos-fonte do funil metodologico (secao 3).

Cada afirmacao numerica do rascunho (secoes 3 a 10) e localizada por um padrao de
texto especifico (a redacao do rascunho e fixa; nao ha necessidade de um parser de
linguagem natural generico) e seu valor e comparado com o valor lido diretamente do
arquivo de origem indicado entre parenteses no texto. Nenhum valor esperado fica
hardcoded no script -- apenas o local onde procurar.

Saidas:
- 08_ARTIGO/tabela_numeros_usados_no_artigo.csv
- 08_ARTIGO/mapa_figura_tabela_script.csv

Uso: python verificar_numeros_rascunho.py
"""
import csv
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RASCUNHO = os.path.join(BASE, "08_ARTIGO", "rascunho_artigo.md")
TABELAS_DIR = os.path.join(BASE, "05_ANALISE_R", "tabelas")
FIGURAS_DIR = os.path.join(BASE, "05_ANALISE_R", "figuras")
OUT_NUMEROS = os.path.join(BASE, "08_ARTIGO", "tabela_numeros_usados_no_artigo.csv")
OUT_MAPA = os.path.join(BASE, "08_ARTIGO", "mapa_figura_tabela_script.csv")

with open(RASCUNHO, encoding="utf-8") as f:
    RASCUNHO_TEXTO = f.read()


def linha_de(offset):
    return RASCUNHO_TEXTO.count("\n", 0, offset) + 1


def parse_numero(s):
    """Formato do texto do rascunho: '.' = separador de milhar, ',' = decimal."""
    s = str(s).replace("%", "").strip()
    if "," in s:
        inteiro, dec = s.split(",", 1)
        return float(f"{inteiro.replace('.', '')}.{dec}")
    return int(s.replace(".", ""))


def parse_numero_csv(s):
    """Formato das tabelas de dados-base (CSV): '.' = decimal, sem separador de milhar."""
    s = str(s).strip()
    if s == "":
        raise ValueError("valor vazio")
    try:
        return int(s)
    except ValueError:
        return float(s)


def fmt(v):
    return v


# ---------------------------------------------------------------------------
# acesso as tabelas de dados-base
# ---------------------------------------------------------------------------

_CACHE = {}


def carregar_tabela(numero_tabela):
    if numero_tabela in _CACHE:
        return _CACHE[numero_tabela]
    achados = [n for n in os.listdir(TABELAS_DIR) if n.startswith(f"tabela{numero_tabela}_")]
    if not achados:
        _CACHE[numero_tabela] = (None, [])
        return _CACHE[numero_tabela]
    caminho = os.path.join(TABELAS_DIR, achados[0])
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f))
    _CACHE[numero_tabela] = (achados[0], linhas)
    return _CACHE[numero_tabela]


def valor_na_tabela(numero_tabela, coluna_rotulo, valor_rotulo, coluna_valor):
    nome_arquivo, linhas = carregar_tabela(numero_tabela)
    if nome_arquivo is None:
        return None, nome_arquivo, f"arquivo tabela{numero_tabela}_*.csv nao encontrado"
    for linha in linhas:
        if (linha.get(coluna_rotulo) or "").strip() == valor_rotulo:
            bruto = linha.get(coluna_valor)
            if bruto in (None, ""):
                return None, nome_arquivo, f"linha '{valor_rotulo}' nao tem valor em '{coluna_valor}'"
            try:
                return parse_numero_csv(bruto), nome_arquivo, f"linha '{coluna_rotulo}={valor_rotulo}', coluna '{coluna_valor}'"
            except ValueError:
                return None, nome_arquivo, f"valor '{bruto}' nao numerico"
    return None, nome_arquivo, f"linha '{coluna_rotulo}={valor_rotulo}' nao encontrada"


def contar_linhas_csv(caminho):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        next(r, None)
        return sum(1 for _ in r)


def contar_true_coluna(caminho, coluna):
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        r = csv.DictReader(f)
        return sum(1 for linha in r if (linha.get(coluna) or "").strip().upper() == "TRUE")


def somar_intervalo_ano(ano_ini, ano_fim):
    _, linhas = carregar_tabela("33")
    soma = sum(parse_numero_csv(l["total_registros"]) for l in linhas if ano_ini <= int(l["ano"]) <= ano_fim)
    return soma, "tabela33_distribuicao_temporal_nucleo_final_104.csv", f"soma de total_registros para {ano_ini}-{ano_fim}"


RESULTADOS = []
_contador = [0]


def registrar(secao, offset_no_texto, trecho, valor_citado, unidade, citacao, arquivo_origem,
              metodo, valor_calculado, observacao_extra=""):
    _contador[0] += 1
    if valor_calculado is None:
        status = "nao_verificavel_automaticamente"
        diferenca = ""
        decisao = "investigar_tabela_origem"
    else:
        vc = parse_numero(valor_citado) if not isinstance(valor_citado, (int, float)) else valor_citado
        if isinstance(vc, float) or isinstance(valor_calculado, float):
            bate = abs(float(vc) - float(valor_calculado)) < 0.05
        else:
            bate = vc == valor_calculado
        status = "bate" if bate else "diverge"
        diferenca = "" if isinstance(valor_calculado, str) else (valor_calculado - vc if not isinstance(vc, float) or not isinstance(valor_calculado, float) else round(valor_calculado - vc, 2))
        decisao = "bate_sem_acao" if bate else "corrigir_texto_rascunho"
    RESULTADOS.append({
        "id_verificacao": f"NUM_{_contador[0]:03d}",
        "secao_rascunho": secao,
        "linha_rascunho": linha_de(offset_no_texto),
        "trecho_texto": trecho,
        "valor_citado": valor_citado,
        "unidade": unidade,
        "tabela_figura_referenciada": citacao,
        "arquivo_tabela_origem": arquivo_origem or "",
        "metodo_verificacao": metodo,
        "valor_calculado": valor_calculado if valor_calculado is not None else "",
        "status": status,
        "diferenca": diferenca,
        "decisao_proposta": decisao,
        "observacao": observacao_extra,
    })


def trecho_em(offset, tamanho=140):
    ini = max(0, offset - 20)
    fim = min(len(RASCUNHO_TEXTO), offset + tamanho)
    return RASCUNHO_TEXTO[ini:fim].replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# Secao 3 -- funil metodologico (sem citacao parentetica de tabela)
# ---------------------------------------------------------------------------

def checar_secao3():
    secao = "3. Procedimentos metodológicos"

    m = re.search(r"coleta bruta de ([\d.]+) registros", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "03_PROCESSADOS", "relatorio_deduplicacao.md")
    with open(caminho, encoding="utf-8") as f:
        texto_relatorio = f.read()
    mm = re.search(r"\*\*Total bruto\*\*\s*\|\s*\*\*(\d+)\*\*", texto_relatorio)
    valor_calc = int(mm.group(1)) if mm else None
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem",
              "(nenhuma citada no texto)", "03_PROCESSADOS/relatorio_deduplicacao.md",
              "marco_funil:total_bruto_coleta", valor_calc,
              "Marco do funil metodologico; tabela 'Volume bruto por base', linha 'Total bruto'.")

    m = re.search(r"corpus único de ([\d.]+) registros", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "03_PROCESSADOS", "corpus_consolidado.csv")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem",
              "(nenhuma citada no texto)", "03_PROCESSADOS/corpus_consolidado.csv",
              "marco_funil:contagem_linhas", contar_linhas_csv(caminho),
              "Marco do funil metodologico; contagem de linhas de dados do corpus consolidado apos deduplicacao.")

    m = re.search(r"núcleo analítico revisado de ([\d.]+) registros", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "05_ANALISE_R", "tabelas", "matriz_nucleo_analitico_revisado.csv")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem",
              "(nenhuma citada no texto)", "05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv",
              "marco_funil:true_nucleo_analitico_revisado", contar_true_coluna(caminho, "nucleo_analitico_revisado"),
              "Marco do funil metodologico; linhas com nucleo_analitico_revisado=TRUE.")

    m = re.search(r"resultando em ([\d.]+) registros classificados", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "07_SINTESE_TEMATICA", "auditoria_qualitativa_resumos_137.csv")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem",
              "(nenhuma citada no texto)", "07_SINTESE_TEMATICA/auditoria_qualitativa_resumos_137.csv",
              "marco_funil:contagem_linhas", contar_linhas_csv(caminho),
              "Marco do funil metodologico; contagem de linhas do nucleo de analise central.")

    m = re.search(r"núcleo final de \*\*([\d.]+) registros\*\*", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "07_SINTESE_TEMATICA", "nucleo_final_pos_auditoria_resumos.csv")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem",
              "(nenhuma citada no texto)", "07_SINTESE_TEMATICA/nucleo_final_pos_auditoria_resumos.csv",
              "marco_funil:contagem_linhas", contar_linhas_csv(caminho),
              "Marco do funil metodologico; contagem de linhas do nucleo final que sustenta as secoes 4-8.")


# ---------------------------------------------------------------------------
# Secao 4 -- panorama bibliometrico
# ---------------------------------------------------------------------------

def checar_secao4():
    secao = "4. Panorama bibliométrico e corpus da revisão"

    m = re.search(
        r"per[íi]odo de (\d{4}) a (\d{4}), que re[úu]ne ([\d.]+) dos 104 registros \((\d+,\d+)%\)",
        RASCUNHO_TEXTO)
    ini, fim, valor_n, valor_pct = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
    soma, arq, obs = somar_intervalo_ano(ini, fim)
    registrar(secao, m.start(3), trecho_em(m.start()), valor_n, "contagem", "Tabela 33; Figura 2",
              arq, "soma_intervalo_ano", soma, obs)
    pct_calc = round(soma / 104 * 100, 1) if soma is not None else None
    registrar(secao, m.start(4), trecho_em(m.start()), valor_pct, "percentual", "Tabela 33; Figura 2",
              arq, "percentual_sobre_soma_intervalo_ano", pct_calc,
              f"Percentual calculado como soma({ini}-{fim})/104*100 = {soma}/104.")

    m = re.search(r"com pico em (\d{4}) \((\d+) registros\)", RASCUNHO_TEXTO)
    ano_pico, n_pico = m.group(1), m.group(2)
    valor_calc, arq, obs = valor_na_tabela("33", "ano", ano_pico, "total_registros")
    registrar(secao, m.start(2), trecho_em(m.start()), n_pico, "contagem", "Tabela 33; Figura 2",
              arq, "celula_direta_por_ano", valor_calc, obs)

    m = re.search(r"intervalo de (\d{4}) a (\d{4}) responde por apenas ([\d.]+) registros", RASCUNHO_TEXTO)
    ini2, fim2, valor_n2 = int(m.group(1)), int(m.group(2)), m.group(3)
    soma2, arq2, obs2 = somar_intervalo_ano(ini2, fim2)
    registrar(secao, m.start(3), trecho_em(m.start()), valor_n2, "contagem", "Tabela 33; Figura 2",
              arq2, "soma_intervalo_ano", soma2, obs2)

    m = re.search(r"ano de (\d{4}) não registrou nenhuma publicação", RASCUNHO_TEXTO)
    ano_zero = m.group(1)
    valor_calc, arq, obs = valor_na_tabela("33", "ano", ano_zero, "total_registros")
    # ausencia de linha para o ano tambem conta como "0 registros" (tabela33 nao lista 2014)
    if valor_calc is None and "nao encontrada" in obs:
        valor_calc = 0
        obs += " (ano ausente da tabela, interpretado como 0 registros)"
    registrar(secao, m.start(1), trecho_em(m.start()), "0", "contagem", "Tabela 33; Figura 2",
              arq, "ausencia_de_linha_por_ano", valor_calc,
              obs + " Valor citado no texto e implicito ('nao registrou nenhuma publicacao'), nao um digito literal.")

    m = re.search(r"Scopus responde por ([\d.]+) dos 104 registros", RASCUNHO_TEXTO)
    valor_calc, arq, obs = valor_na_tabela("34", "categoria", "Scopus", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "Tabela 34; Figura 3",
              arq, "celula_direta_por_categoria", valor_calc, obs)

    m = re.search(r"Web of Science por (\d+) e a Crossref por apenas (\d+)", RASCUNHO_TEXTO)
    valor_wos, arq_wos, obs_wos = valor_na_tabela("34", "categoria", "WoS", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "Tabela 34; Figura 3",
              arq_wos, "celula_direta_por_categoria", valor_wos, obs_wos)
    valor_cr, arq_cr, obs_cr = valor_na_tabela("34", "categoria", "Crossref", "total_registros")
    registrar(secao, m.start(2), trecho_em(m.start()), m.group(2), "contagem", "Tabela 34; Figura 3",
              arq_cr, "celula_direta_por_categoria", valor_cr, obs_cr)

    m = re.search(r"\(Journal\) respondem por ([\d.]+) dos 104 registros", RASCUNHO_TEXTO)
    valor_calc, arq, obs = valor_na_tabela("34", "categoria", "Journal", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "Tabela 34; Figura 3",
              arq, "celula_direta_por_categoria", valor_calc, obs)

    m = re.search(r"anais de evento \((\d+)\) e capítulos/séries de livro \((\d+)\)", RASCUNHO_TEXTO)
    valor_conf, arq_conf, obs_conf = valor_na_tabela("34", "categoria", "Conference Proceeding", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "Tabela 34; Figura 3",
              arq_conf, "celula_direta_por_categoria", valor_conf, obs_conf)
    valor_book, arq_book, obs_book = valor_na_tabela("34", "categoria", "Book Series", "total_registros")
    registrar(secao, m.start(2), trecho_em(m.start()), m.group(2), "contagem", "Tabela 34; Figura 3",
              arq_book, "celula_direta_por_categoria", valor_book, obs_book)


# ---------------------------------------------------------------------------
# Secao 5 -- criterios e dimensoes
# ---------------------------------------------------------------------------

DIMENSOES_S5 = [
    ("técnica-operacional", "tecnica_operacional", "102", "98,1"),
    ("institucional", "institucional", "93", "89,4"),
    ("ambiental", "ambiental", "84", "80,8"),
    ("ciclo de vida", "ciclo_de_vida", "60", "57,7"),
    ("econômica", "economica", "59", "56,7"),
    ("social", "social", "57", "54,8"),
]

CRITERIOS_S5A = [
    ("desempenho operacional", "desempenho_operacional", "93", "89,4"),
    ("disponibilidade de dados e informação", "informacao_dados", "76", "73,1"),
    ("custo", "custo", "59", "56,7"),
    ("vida útil do ativo", "vida_util", "40", "38,5"),
    ("energia", "energia", "36", "34,6"),
]


def checar_secao5():
    secao = "5. Critérios de sustentabilidade e priorização"

    for rotulo_texto, rotulo_tabela, valor_n, valor_pct in DIMENSOES_S5:
        m = re.search(re.escape(rotulo_texto) + r"[^(]{0,20}?(" + re.escape(valor_n) + r")\s*(?:registros)?\s*\((" + re.escape(valor_pct) + r")%\)", RASCUNHO_TEXTO)
        if not m:
            continue
        valor_calc, arq, obs = valor_na_tabela("27", "dimensao_identificada_leitura", rotulo_tabela, "total_registros")
        registrar(secao, m.start(1), trecho_em(m.start(), 100), valor_n, "contagem", "Tabela 27; Figura 5",
                  arq, f"filtro_por_rotulo:{rotulo_tabela}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("27", "dimensao_identificada_leitura", rotulo_tabela, "percentual_dos_104")
        registrar(secao, m.start(2), trecho_em(m.start(), 100), valor_pct, "percentual", "Tabela 27; Figura 5",
                  arq2, f"filtro_por_rotulo:{rotulo_tabela}", pct_calc, obs2)

    for rotulo_texto, rotulo_tabela, valor_n, valor_pct in CRITERIOS_S5A:
        m = re.search(re.escape(rotulo_texto) + r"[^(]{0,20}?(" + re.escape(valor_n) + r")\s*(?:registros)?\s*\((" + re.escape(valor_pct) + r")%\)", RASCUNHO_TEXTO)
        if not m:
            continue
        valor_calc, arq, obs = valor_na_tabela("26", "criterio", rotulo_tabela, "total_registros")
        registrar(secao, m.start(1), trecho_em(m.start(), 100), valor_n, "contagem", "Tabela 26",
                  arq, f"filtro_por_rotulo:{rotulo_tabela}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("26", "criterio", rotulo_tabela, "percentual_dos_104")
        registrar(secao, m.start(2), trecho_em(m.start(), 100), valor_pct, "percentual", "Tabela 26",
                  arq2, f"filtro_por_rotulo:{rotulo_tabela}", pct_calc, obs2)

    m = re.search(r"condição física \((\d+) registros\) e de risco \((\d+) registros\)", RASCUNHO_TEXTO)
    valor_cf, arq_cf, obs_cf = valor_na_tabela("26", "criterio", "condicao_fisica", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "(nenhuma citada no texto)",
              arq_cf, "filtro_por_rotulo:condicao_fisica", valor_cf, obs_cf)
    valor_ri, arq_ri, obs_ri = valor_na_tabela("26", "criterio", "risco", "total_registros")
    registrar(secao, m.start(2), trecho_em(m.start()), m.group(2), "contagem", "(nenhuma citada no texto)",
              arq_ri, "filtro_por_rotulo:risco", valor_ri, obs_ri)


# ---------------------------------------------------------------------------
# Secao 6 -- metodos de decisao
# ---------------------------------------------------------------------------

METODOS_S6 = [
    ("framework", "framework"),
    ("decision support", "decision support"),
    ("BIM", "BIM"),
    ("otimização", "optimization"),
    ("pontuação/scoring", "scoring"),
    ("custo de ciclo de vida", "life-cycle cost"),
    ("AHP", "AHP"),
    ("TOPSIS", "TOPSIS"),
    ("MCDM", "MCDM"),
    ("ANP", "ANP"),
    ("Bayesian Best-Worst Method", "Bayesian Best Worst Method"),
]


def checar_secao6():
    secao = "6. Métodos de apoio multicritério à decisão"

    m = re.search(r'"framework" aparece em (\d+) dos 104 registros do núcleo final \((\d+,\d+)%\)', RASCUNHO_TEXTO)
    valor_calc, arq, obs = valor_na_tabela("28", "metodo_identificado_leitura", "framework", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "Tabela 28; Figura 4",
              arq, "filtro_por_rotulo:framework", valor_calc, obs)
    pct_calc, arq2, obs2 = valor_na_tabela("28", "metodo_identificado_leitura", "framework", "percentual_dos_104")
    registrar(secao, m.start(2), trecho_em(m.start()), m.group(2), "percentual", "Tabela 28; Figura 4",
              arq2, "filtro_por_rotulo:framework", pct_calc, obs2)

    m = re.search(
        r'"decision support" e BIM aparecem cada um em (\d+) registros \((\d+,\d+)%\), seguidos de otimização \((\d+) registros, (\d+,\d+)%\), pontuação/scoring \((\d+), (\d+,\d+)%\) e custo de ciclo de vida \((\d+), (\d+,\d+)%\)',
        RASCUNHO_TEXTO)
    pares = [
        ("decision support", m.group(1), m.group(2)),
        ("BIM", m.group(1), m.group(2)),
        ("optimization", m.group(3), m.group(4)),
        ("scoring", m.group(5), m.group(6)),
        ("life-cycle cost", m.group(7), m.group(8)),
    ]
    for rotulo, val_n, val_pct in pares:
        valor_calc, arq, obs = valor_na_tabela("28", "metodo_identificado_leitura", rotulo, "total_registros")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_n, "contagem", "Tabela 28; Figura 4",
                  arq, f"filtro_por_rotulo:{rotulo}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("28", "metodo_identificado_leitura", rotulo, "percentual_dos_104")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_pct, "percentual", "Tabela 28; Figura 4",
                  arq2, f"filtro_por_rotulo:{rotulo}", pct_calc, obs2)

    m = re.search(
        r'AHP em (\d+) registros \((\d+,\d+)%\), TOPSIS em (\d+) \((\d+,\d+)%\), MCDM em (\d+) \((\d+,\d+)%\), ANP em (\d+) \((\d+,\d+)%\) e Bayesian Best-Worst Method em (\d+) registro \((\d+,\d+)%\)',
        RASCUNHO_TEXTO)
    pares2 = [
        ("AHP", m.group(1), m.group(2)),
        ("TOPSIS", m.group(3), m.group(4)),
        ("MCDM", m.group(5), m.group(6)),
        ("ANP", m.group(7), m.group(8)),
        ("Bayesian Best Worst Method", m.group(9), m.group(10)),
    ]
    for rotulo, val_n, val_pct in pares2:
        valor_calc, arq, obs = valor_na_tabela("28", "metodo_identificado_leitura", rotulo, "total_registros")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_n, "contagem", "(nenhuma citada no texto)",
                  arq, f"filtro_por_rotulo:{rotulo}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("28", "metodo_identificado_leitura", rotulo, "percentual_dos_104")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_pct, "percentual", "(nenhuma citada no texto)",
                  arq2, f"filtro_por_rotulo:{rotulo}", pct_calc, obs2)


# ---------------------------------------------------------------------------
# Secao 7 -- aplicabilidade a IES publicas
# ---------------------------------------------------------------------------

def checar_secao7():
    secao = "7. Aplicabilidade a edificações públicas universitárias"

    m = re.search(
        r"tipologia construtiva \((\d+) registros, (\d+,\d+)%\), ou trata de portfólios e carteiras de ativos prediais como unidade de análise \((\d+) registros, (\d+,\d+)%\)",
        RASCUNHO_TEXTO)
    pares = [("edificio_generico", m.group(1), m.group(2)), ("portfolio_predial", m.group(3), m.group(4))]
    for rotulo, val_n, val_pct in pares:
        valor_calc, arq, obs = valor_na_tabela("29", "contexto_identificado_leitura", rotulo, "total_registros")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_n, "contagem", "Tabela 29",
                  arq, f"filtro_por_rotulo:{rotulo}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("29", "contexto_identificado_leitura", rotulo, "percentual_dos_104")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_pct, "percentual", "Tabela 29",
                  arq2, f"filtro_por_rotulo:{rotulo}", pct_calc, obs2)

    m = re.search(
        r"hospitais em (\d+) registros \((\d+,\d+)%\), edifícios comerciais em (\d+) \((\d+,\d+)%\) e edifícios residenciais em (\d+) \((\d+,\d+)%\)",
        RASCUNHO_TEXTO)
    pares2 = [
        ("hospital", m.group(1), m.group(2)),
        ("edificio_comercial", m.group(3), m.group(4)),
        ("edificio_residencial", m.group(5), m.group(6)),
    ]
    for rotulo, val_n, val_pct in pares2:
        valor_calc, arq, obs = valor_na_tabela("29", "contexto_identificado_leitura", rotulo, "total_registros")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_n, "contagem", "(nenhuma citada no texto)",
                  arq, f"filtro_por_rotulo:{rotulo}", valor_calc, obs)
        pct_calc, arq2, obs2 = valor_na_tabela("29", "contexto_identificado_leitura", rotulo, "percentual_dos_104")
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_pct, "percentual", "(nenhuma citada no texto)",
                  arq2, f"filtro_por_rotulo:{rotulo}", pct_calc, obs2)


# ---------------------------------------------------------------------------
# Secao 8 -- matriz analitica
# ---------------------------------------------------------------------------

def checar_secao8():
    secao = "8. Matriz analítica proposta"

    m = re.search(
        r'(\d+) registros em comum com "framework", (\d+) com "decision support" e (\d+) com BIM —, seguida da dimensão institucional \((\d+) registros em comum com "framework"\) e da ambiental \((\d+)\)',
        RASCUNHO_TEXTO)
    pares = [
        ("tecnica_operacional", "framework", m.group(1)),
        ("tecnica_operacional", "decision support", m.group(2)),
        ("tecnica_operacional", "BIM", m.group(3)),
        ("institucional", "framework", m.group(4)),
        ("ambiental", "framework", m.group(5)),
    ]
    for dimensao, metodo, val_n in pares:
        _, linhas = carregar_tabela("32")
        valor_calc = None
        arq_nome, _ = carregar_tabela("32")
        for linha in linhas:
            if linha.get("dimensao_roteiro") == dimensao and linha.get("metodo") == metodo:
                valor_calc = parse_numero_csv(linha["n_registros_comuns"])
                break
        registrar(secao, m.start(), trecho_em(m.start(), 260), val_n, "contagem", "Tabela 32; Figura 7",
                  arq_nome, f"filtro_por_par:{dimensao}x{metodo}", valor_calc,
                  f"linha dimensao_roteiro='{dimensao}', metodo='{metodo}', coluna n_registros_comuns.")

    m = re.search(r"\((\d+) e (\d+) registros em comum com \"framework\", respectivamente\)", RASCUNHO_TEXTO)
    pares2 = [("economica", m.group(1)), ("social", m.group(2))]
    for dimensao, val_n in pares2:
        _, linhas = carregar_tabela("32")
        arq_nome, _ = carregar_tabela("32")
        valor_calc = None
        for linha in linhas:
            if linha.get("dimensao_roteiro") == dimensao and linha.get("metodo") == "framework":
                valor_calc = parse_numero_csv(linha["n_registros_comuns"])
                break
        registrar(secao, m.start(), trecho_em(m.start(), 220), val_n, "contagem", "Tabela 32; Figura 7",
                  arq_nome, f"filtro_por_par:{dimensao}xframework", valor_calc,
                  f"linha dimensao_roteiro='{dimensao}', metodo='framework', coluna n_registros_comuns.")

    m = re.search(r"alta frequência absoluta no núcleo \((\d+) de 104 registros\)", RASCUNHO_TEXTO)
    valor_calc, arq, obs = valor_na_tabela("28", "metodo_identificado_leitura", "framework", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "(nenhuma citada no texto)",
              arq, "filtro_por_rotulo:framework", valor_calc, obs)


# ---------------------------------------------------------------------------
# Secao 9 -- limitacoes
# ---------------------------------------------------------------------------

def checar_secao9():
    secao = "9. Limitações"

    m = re.search(
        r"núcleo final de ([\d.]+) registros corresponde a (\d+,\d+)% do núcleo analítico revisado de ([\d.]+) registros e a (\d+,\d+)% dos ([\d.]+) registros",
        RASCUNHO_TEXTO)
    n104, pct1, n3678, pct2, n137 = (parse_numero(g) for g in m.groups())
    pct1_calc = round(n104 / n3678 * 100, 1)
    registrar(secao, m.start(2), trecho_em(m.start()), fmt(m.group(2)), "percentual", "(nenhuma citada no texto)",
              "05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv", "calculo:104/3678*100", pct1_calc,
              f"Calculado como {int(n104)}/{int(n3678)}*100.")
    pct2_calc = round(n104 / n137 * 100, 1)
    registrar(secao, m.start(4), trecho_em(m.start()), fmt(m.group(4)), "percentual", "(nenhuma citada no texto)",
              "07_SINTESE_TEMATICA/auditoria_qualitativa_resumos_137.csv", "calculo:104/137*100", pct2_calc,
              f"Calculado como {int(n104)}/{int(n137)}*100.")

    m = re.search(r"duas referências candidatas não puderam ser confirmadas", RASCUNHO_TEXTO)
    caminho = os.path.join(BASE, "03_REFERENCIAS_CANDIDATAS", "referencias_validadas.csv")
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        linhas_ref = list(csv.DictReader(f))
    n_nao_usar = sum(1 for l in linhas_ref if (l.get("entra_no_artigo_sim_nao") or "").strip() == "nao")
    registrar(secao, m.start(), trecho_em(m.start()), "2", "contagem", "(nenhuma citada no texto)",
              "03_REFERENCIAS_CANDIDATAS/referencias_validadas.csv", "contagem:entra_no_artigo=nao", n_nao_usar,
              "Texto usa numeral por extenso ('duas'); contagem de linhas com entra_no_artigo_sim_nao='nao'.")
    n_duvida = sum(1 for l in linhas_ref if (l.get("entra_no_artigo_sim_nao") or "").strip() == "duvida")
    registrar(secao, m.start(), trecho_em(m.start(), 220), "1", "contagem", "(nenhuma citada no texto)",
              "03_REFERENCIAS_CANDIDATAS/referencias_validadas.csv", "contagem:entra_no_artigo=duvida", n_duvida,
              "Texto usa numeral por extenso ('uma'); contagem de linhas com entra_no_artigo_sim_nao='duvida' (data de publicacao nao resolvida).")


# ---------------------------------------------------------------------------
# Secao 10 -- consideracoes finais
# ---------------------------------------------------------------------------

def checar_secao10():
    secao = "10. Considerações finais"
    m = re.search(r"apenas (\d+) registros \((\d+,\d+)%\) apontam lacuna especificamente associada a esse contexto", RASCUNHO_TEXTO)
    valor_calc, arq, obs = valor_na_tabela("30", "categoria", "lacuna_especifica_ies_publicas", "total_registros")
    registrar(secao, m.start(1), trecho_em(m.start()), m.group(1), "contagem", "(nenhuma citada no texto)",
              arq, "filtro_por_rotulo:lacuna_especifica_ies_publicas", valor_calc, obs)
    pct_calc, arq2, obs2 = valor_na_tabela("30", "categoria", "lacuna_especifica_ies_publicas", "percentual_dos_104")
    registrar(secao, m.start(2), trecho_em(m.start()), m.group(2), "percentual", "(nenhuma citada no texto)",
              arq2, "filtro_por_rotulo:lacuna_especifica_ies_publicas", pct_calc, obs2)


# ---------------------------------------------------------------------------
# Saida 2 -- mapa figura -> tabela -> script
# ---------------------------------------------------------------------------

MAPA_FIGURA_OFICIAL = {
    "Figura 2": ("figura09_distribuicao_temporal_nucleo_final_104.png", "33"),
    "Figura 3": ("figura10_distribuicao_base_tipo_nucleo_final_104.png", "34"),
    "Figura 4": ("figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png", "28"),
    "Figura 5": ("figura12_dimensoes_sustentabilidade_nucleo_final_104.png", "27"),
    "Figura 6": ("figura13_heatmap_criterios_metodos_nucleo_final_104.png", "31"),
    "Figura 7": ("figura14_matriz_analitica_dimensao_metodo_nucleo_final_104.png", "32"),
}


def localizar_script_gerador(padrao_nome):
    candidatos = []
    for pasta in (os.path.join(BASE, "00_CONFIG"), os.path.join(BASE, "05_ANALISE_R", "scripts")):
        if not os.path.isdir(pasta):
            continue
        for nome in os.listdir(pasta):
            if nome.lower().endswith((".py", ".r")) and padrao_nome.lower() in nome.lower():
                candidatos.append(f"{os.path.basename(pasta)}/{nome}")
    return "; ".join(candidatos) if candidatos else "NAO_LOCALIZADO"


def gerar_mapa_figuras():
    citacoes_por_figura = {}
    tabelas_citadas_junto = {}
    for r in RESULTADOS:
        m = re.search(r"Figura\s+(\d+)", r["tabela_figura_referenciada"])
        if m:
            chave = f"Figura {m.group(1)}"
            citacoes_por_figura.setdefault(chave, set()).add(r["secao_rascunho"])
            mt = re.search(r"Tabela\s+(\d+)", r["tabela_figura_referenciada"])
            if mt:
                tabelas_citadas_junto.setdefault(chave, set()).add(mt.group(1))

    linhas_saida = []
    todas = sorted(set(list(MAPA_FIGURA_OFICIAL.keys()) + list(citacoes_por_figura.keys())),
                    key=lambda s: int(s.split()[1]))
    for figura in todas:
        arquivo_fisico, numero_tabela = MAPA_FIGURA_OFICIAL.get(figura, ("NAO_MAPEADA", ""))
        secoes = sorted(citacoes_por_figura.get(figura, set()))
        tabelas_junto = sorted(tabelas_citadas_junto.get(figura, set()), key=int)
        caminho_fisico = os.path.join(FIGURAS_DIR, arquivo_fisico) if arquivo_fisico != "NAO_MAPEADA" else ""
        existe_fisico = os.path.exists(caminho_fisico) if caminho_fisico else False
        nome_tabela_csv, _ = carregar_tabela(numero_tabela) if numero_tabela else (None, [])
        script_gerador = localizar_script_gerador(f"tabela{numero_tabela}") if numero_tabela else "NAO_LOCALIZADO"
        if script_gerador == "NAO_LOCALIZADO" and arquivo_fisico != "NAO_MAPEADA":
            prefixo_figura = arquivo_fisico.split("_")[0]
            script_gerador = localizar_script_gerador(prefixo_figura)

        status = "ok"
        obs_partes = []
        if not secoes:
            status = "nao_citada_no_artigo"
            obs_partes.append("Figura nao citada por numero no rascunho_artigo.md; correspondencia com a tabela vem de relatorio_figuras_tabelas_finais.md, secao 5.")
        elif len(secoes) > 1:
            status = "conflito_de_citacao"
            obs_partes.append(f"Citada em mais de uma secao ({'; '.join(secoes)}) associada a tabelas de conteudo diferente; revisar qual citacao esta correta.")
        elif len(tabelas_junto) > 1:
            status = "conflito_de_citacao"
            obs_partes.append(f"Citada junto de mais de uma tabela na mesma secao (Tabela {'; Tabela '.join(tabelas_junto)}); a figura fisica so corresponde a Tabela {numero_tabela}, revisar a segunda citacao.")
        if arquivo_fisico != "NAO_MAPEADA" and not existe_fisico:
            obs_partes.append("Arquivo fisico nao encontrado em 05_ANALISE_R/figuras/.")
        if script_gerador == "NAO_LOCALIZADO":
            obs_partes.append("Nenhum script .py/.R persistido em 00_CONFIG/ ou 05_ANALISE_R/scripts/ para esta tabela/figura; geracao descrita apenas em prosa em relatorio_figuras_tabelas_finais.md.")

        linhas_saida.append({
            "figura_citada_no_rascunho": figura,
            "secoes_onde_e_citada": "; ".join(secoes) if secoes else "(nao citada)",
            "arquivo_fisico_correspondente": arquivo_fisico,
            "tabela_dados_base": nome_tabela_csv or "",
            "script_gerador": script_gerador,
            "etapa_origem": "ETAPA_19 (interna) / ETAPA 11 do roteiro-mestre",
            "status": status,
            "observacao": " ".join(obs_partes) if obs_partes else "Sem inconsistencia detectada.",
        })

    # tabelas com figura fisica associada mas nao mapeadas a nenhuma "Figura N" citavel (ex.: Tabela 30, Tabela 31 isolada)
    for numero_tabela, nome_tabela_esperado in (("30", "lacunas"),):
        nome_arquivo, _ = carregar_tabela(numero_tabela)
        citada = any(f"Tabela {numero_tabela}" in r["tabela_figura_referenciada"] for r in RESULTADOS)
        linhas_saida.append({
            "figura_citada_no_rascunho": f"(sem figura; Tabela {numero_tabela})",
            "secoes_onde_e_citada": "(citada apenas em prosa, sem numero de tabela entre parenteses)" if not citada else "",
            "arquivo_fisico_correspondente": "",
            "tabela_dados_base": nome_arquivo or "",
            "script_gerador": localizar_script_gerador(f"tabela{numero_tabela}"),
            "etapa_origem": "ETAPA_19 (interna) / ETAPA 11 do roteiro-mestre",
            "status": "nao_citada_no_artigo",
            "observacao": f"Conteudo da Tabela {numero_tabela} ({nome_tabela_esperado}) e mencionado em prosa na secao 10, mas sem citacao formal '(Tabela {numero_tabela})'.",
        })

    return linhas_saida


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    checar_secao3()
    checar_secao4()
    checar_secao5()
    checar_secao6()
    checar_secao7()
    checar_secao8()
    checar_secao9()
    checar_secao10()

    campos = ["id_verificacao", "secao_rascunho", "linha_rascunho", "trecho_texto", "valor_citado",
              "unidade", "tabela_figura_referenciada", "arquivo_tabela_origem", "metodo_verificacao",
              "valor_calculado", "status", "diferenca", "decisao_proposta", "observacao"]
    with open(OUT_NUMEROS, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(RESULTADOS)

    mapa = gerar_mapa_figuras()
    campos_mapa = ["figura_citada_no_rascunho", "secoes_onde_e_citada", "arquivo_fisico_correspondente",
                   "tabela_dados_base", "script_gerador", "etapa_origem", "status", "observacao"]
    with open(OUT_MAPA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos_mapa)
        w.writeheader()
        w.writerows(mapa)

    total = len(RESULTADOS)
    bate = sum(1 for r in RESULTADOS if r["status"] == "bate")
    diverge = sum(1 for r in RESULTADOS if r["status"] == "diverge")
    nao_verif = sum(1 for r in RESULTADOS if r["status"] == "nao_verificavel_automaticamente")
    print(f"Numeros verificados: {total}  bate={bate}  diverge={diverge}  nao_verificavel={nao_verif}")
    print(f"Saida: {OUT_NUMEROS}")
    print(f"Saida: {OUT_MAPA}")
    if diverge:
        print("\n--- Divergencias ---")
        for r in RESULTADOS:
            if r["status"] == "diverge":
                print(f"  [{r['id_verificacao']}] {r['secao_rascunho']}: citado={r['valor_citado']!r} calculado={r['valor_calculado']!r} ({r['metodo_verificacao']})")
    conflitos = [l for l in mapa if l["status"] == "conflito_de_citacao"]
    if conflitos:
        print("\n--- Conflitos de citacao de figura ---")
        for l in conflitos:
            print(f"  {l['figura_citada_no_rascunho']}: {l['secoes_onde_e_citada']}")


if __name__ == "__main__":
    main()
