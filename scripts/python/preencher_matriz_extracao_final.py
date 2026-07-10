"""
Script da ETAPA_13 - PREENCHER_MATRIZ_EXTRACAO_FINAL.

Preenche as colunas de conteudo da matriz de extracao final (esquema definido na ETAPA_12,
07_SINTESE_TEMATICA/matriz_extracao_final_esquema.md) para os 3.678 registros do nucleo analitico
revisado, a partir de 07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv (ETAPA_11).

Escopo explicito desta etapa (nao ultrapassar):
- Trabalha SOMENTE com titulo + resumo + palavras-chave ja capturados na matriz da ETAPA_11. Nao
  le PDF/texto completo -- decisao de estrategia registrada em
  00_CONTROLE/DECISOES_METODOLOGICAS.md, entrada de 2026-07-09 ("ETAPA_12: mudanca de estrategia").
- Metodo: casamento de frases-chave (regras explicitas, reprodutivel, sem LLM para gerar achados --
  mesmo padrao de 00_CONFIG/pre_triagem.py e 00_CONFIG/sintese_tematica_preliminar.py). Nenhum campo
  e inferido ou simulado alem do que esta explicito no texto normalizado de titulo+resumo+palavras-
  chave.
- Nao decide "uso_no_artigo" -- fica fixo em "pendente" para todos os registros, conforme esquema
  da ETAPA_12 (decisao humana explicita, fora do escopo desta etapa).
- `contribuicao_para_artigo` fica fixo em "a_definir_na_sintese" para todos os registros -- e um
  campo de julgamento reservado para a etapa de sintese/redacao, conforme esquema da ETAPA_12.
- `dados_utilizados` e preenchido por categoria de dado reconhecida por palavra-chave (nao por
  paraphrase livre) -- interpretacao pratica documentada no relatorio desta etapa, para manter o
  metodo reprodutivel.

Saidas:
- 07_SINTESE_TEMATICA/matriz_extracao_final.csv (3.678 linhas, 49 colunas)
- 07_SINTESE_TEMATICA/relatorio_preenchimento_matriz_extracao_final.md
"""

import csv
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IN_PATH = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA", "matriz_sintese_tematica_preliminar.csv")
OUT_DIR = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA")
OUT_PATH = os.path.join(OUT_DIR, "matriz_extracao_final.csv")
RELATORIO_PATH = os.path.join(OUT_DIR, "relatorio_preenchimento_matriz_extracao_final.md")

NAO_INFORMADO = "nao_informado_no_resumo"
NAO_CLASSIFICAVEL = "nao_classificavel_pelo_resumo"
NAO_IDENTIFICAVEL = "nao_identificavel_pelo_resumo"
NAO_VERIFICAVEL = "nao_verificavel_pelo_resumo"
BASE_EVIDENCIA = "titulo_resumo_palavras_chave"

FIELDS_FINAIS = [
    "id_unico", "doi", "titulo", "ano", "autores", "fonte_periodico", "tipo_documento",
    "bases_origem", "strings_origem", "resumo_presente", "palavras_chave", "resumo",
    "bloco_a_presente", "bloco_b_presente", "bloco_c_presente", "bloco_d_presente",
    "bloco_tecnologico_presente", "bloco_conceitual_presente",
    "termos_bloco_a", "termos_bloco_b",
    "usa_topsis", "usa_ahp", "usa_outro_mcdm", "metodo_mcdm_especifico",
    "usa_bim", "usa_digital_twin", "usa_iot", "usa_data_driven", "tecnologia_especifica",
    "tipo_edificacao_sinal",
    "eixo_tematico_preliminar",
    "classe_final_sem_duvida", "nucleo_analitico_revisado",
    "pais_contexto", "tipo_aplicacao", "dados_utilizados", "resultado_principal",
    "contribuicao_para_artigo", "lacuna_identificada",
    "criterios_ambientais", "criterios_economicos", "criterios_sociais",
    "criterios_tecnicos_operacionais", "criterios_institucionais", "criterios_risco",
    "base_evidencia_extracao", "resumo_suficiente_para_extracao", "uso_no_artigo", "observacoes",
]

# ---------------------------------------------------------------------------
# Paises/regioes (lista pratica, nao exaustiva -- so os que aparecerem explicitamente citados no
# titulo+resumo sao registrados; ausencia na lista nao e erro, apenas fica nao_informado_no_resumo).
# ---------------------------------------------------------------------------
PAISES = {
    "brazil": "Brasil", "brasil": "Brasil", "china": "China", "united states": "Estados Unidos",
    "usa": "Estados Unidos", "u.s.": "Estados Unidos", "uk": "Reino Unido",
    "united kingdom": "Reino Unido", "england": "Reino Unido", "australia": "Australia",
    "canada": "Canada", "india": "India", "italy": "Italia", "spain": "Espanha",
    "portugal": "Portugal", "france": "Franca", "germany": "Alemanha", "netherlands": "Holanda",
    "sweden": "Suecia", "norway": "Noruega", "denmark": "Dinamarca", "finland": "Finlandia",
    "poland": "Polonia", "greece": "Grecia", "turkey": "Turquia", "iran": "Ira",
    "saudi arabia": "Arabia Saudita", "malaysia": "Malasia", "indonesia": "Indonesia",
    "singapore": "Singapura", "south korea": "Coreia do Sul", "korea": "Coreia do Sul",
    "japan": "Japao", "taiwan": "Taiwan", "hong kong": "Hong Kong", "vietnam": "Vietna",
    "thailand": "Tailandia", "philippines": "Filipinas", "pakistan": "Paquistao",
    "nigeria": "Nigeria", "south africa": "Africa do Sul", "egypt": "Egito", "kenya": "Quenia",
    "ghana": "Gana", "mexico": "Mexico", "chile": "Chile", "colombia": "Colombia",
    "argentina": "Argentina", "peru": "Peru", "new zealand": "Nova Zelandia",
    "united arab emirates": "Emirados Arabes Unidos", "uae": "Emirados Arabes Unidos",
    "qatar": "Catar", "russia": "Russia", "ukraine": "Ucrania", "belgium": "Belgica",
    "switzerland": "Suica", "austria": "Austria", "ireland": "Irlanda", "romania": "Romenia",
    "czech republic": "Republica Tcheca", "hungary": "Hungria", "israel": "Israel",
    "jordan": "Jordania", "iraq": "Iraque", "sub-saharan africa": "Africa Subsaariana",
    "european union": "Uniao Europeia",
}

# ---------------------------------------------------------------------------
# Tipo de aplicacao (ordem de prioridade fixa, documentada; primeira que casar decide).
# ---------------------------------------------------------------------------
TIPO_APLICACAO_REGRAS = [
    ("revisao_sistematica_ou_bibliometrica", [
        "systematic review", "systematic literature review", "literature review",
        "bibliometric analysis", "bibliometric review", "scoping review",
        "state-of-the-art review", "state of the art review", "meta-analysis",
    ]),
    ("estudo_de_caso", [
        "case study", "case-study", "case studies",
    ]),
    ("survey_ou_levantamento_com_especialistas", [
        "questionnaire survey", "expert survey", "survey of experts", "delphi method",
        "delphi study", "interviews with", "semi-structured interviews", "survey questionnaire",
        "structured interviews",
    ]),
    ("simulacao_ou_modelagem_computacional", [
        "simulation model", "computational model", "numerical simulation", "energy simulation",
        "building performance simulation", "monte carlo simulation", "agent-based model",
        "digital twin simulation",
    ]),
    ("proposta_de_framework_ou_modelo", [
        "propose a framework", "proposes a framework", "presents a framework",
        "develop a framework", "develops a framework", "conceptual framework",
        "propose a model", "proposes a model", "presents a model", "develop a model",
        "proposes an approach", "presents a methodology", "proposed methodology",
        "decision support framework", "decision-making framework",
    ]),
    ("estudo_conceitual_sem_aplicacao_empirica", [
        "conceptual paper", "discussion paper", "position paper", "perspective paper",
        "theoretical framework", "opinion paper",
    ]),
]

# ---------------------------------------------------------------------------
# Dados utilizados (categorias reconhecidas por palavra-chave; um registro pode ter mais de uma).
# ---------------------------------------------------------------------------
DADOS_REGRAS = [
    ("dados_de_questionario_ou_entrevista", [
        "questionnaire", "survey data", "interview", "interviews", "expert opinion",
        "expert judgment", "expert judgement", "respondents",
    ]),
    ("dados_de_sensores_ou_iot", [
        "sensor data", "iot data", "real-time data", "monitoring data", "smart meter",
        "building automation system data",
    ]),
    ("dados_historicos_ou_registros_de_manutencao", [
        "maintenance records", "historical data", "work order", "work orders",
        "maintenance data", "operational data", "facility management data",
    ]),
    ("dados_secundarios_de_literatura_ou_documentais", [
        "secondary data", "literature data", "document analysis", "policy documents",
        "archival data",
    ]),
    ("dados_de_simulacao", [
        "simulated data", "simulation data", "synthetic data",
    ]),
]

# ---------------------------------------------------------------------------
# Sentencas-gatilho para resultado_principal e lacuna_identificada.
# ---------------------------------------------------------------------------
GATILHOS_RESULTADO = [
    "results show", "results indicate", "results reveal", "results suggest",
    "findings show", "findings indicate", "findings reveal", "findings suggest",
    "study shows", "study reveals", "study finds", "we found that", "it was found that",
    "demonstrates that", "demonstrate that", "reveals that", "indicates that",
]
GATILHOS_LACUNA = [
    "future research", "further research", "future studies", "future work",
    "remains unclear", "little is known", "limited research", "few studies have",
    "research gap", "gap in the literature", "not yet been explored", "warrants further",
]

# ---------------------------------------------------------------------------
# Criterios de sustentabilidade/gestao (seis dimensoes; multi-label, um registro pode ter varios
# sim simultaneos).
# ---------------------------------------------------------------------------
CRITERIOS_REGRAS = {
    "criterios_ambientais": [
        "energy consumption", "energy efficiency", "carbon emission", "carbon footprint",
        "greenhouse gas", "co2 emission", "water consumption", "waste management",
        "environmental impact", "renewable energy", "leed", "breeam", "green building",
        "environmental performance", "environmental sustainability", "net zero", "net-zero",
        "climate neutral", "carbon neutral",
    ],
    "criterios_economicos": [
        "life cycle cost", "life-cycle cost", "cost-benefit", "cost benefit", "investment cost",
        "return on investment", "economic feasibility", "financial performance",
        "maintenance cost", "operating cost", "operational cost", "budget constraint",
        "asset value", "capital expenditure", "total cost of ownership",
    ],
    "criterios_sociais": [
        "occupant satisfaction", "user satisfaction", "occupant comfort", "thermal comfort",
        "indoor air quality", "occupant well-being", "occupant wellbeing", "accessibility",
        "occupant health", "quality of life", "social sustainability", "occupant experience",
        "user experience",
    ],
    "criterios_tecnicos_operacionais": [
        "reliability", "maintainability", "structural performance", "technical condition",
        "degradation", "defect detection", "failure rate", "downtime", "operational efficiency",
        "asset condition", "structural health monitoring", "response time",
        "predictive maintenance", "condition assessment",
    ],
    "criterios_institucionais": [
        "governance", "public policy", "regulatory framework", "institutional framework",
        "organizational strategy", "stakeholder engagement", "compliance", "building code",
        "management strategy", "decision-making process", "policy implementation",
    ],
    "criterios_risco": [
        "risk assessment", "risk management", "vulnerability", "resilience", "structural safety",
        "hazard", "disaster risk", "failure risk", "safety risk", "fire risk", "seismic risk",
    ],
}


def normalizar(texto):
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\s+", " ", t)
    return f" {t.strip()} "


def dividir_sentencas(texto):
    if not texto:
        return []
    partes = re.split(r"(?<=[.!?])\s+", texto.strip())
    return [p.strip() for p in partes if p.strip()]


def detectar_pais(texto_norm):
    achados = []
    for termo, rotulo in PAISES.items():
        if f" {termo} " in texto_norm and rotulo not in achados:
            achados.append(rotulo)
    return "; ".join(achados) if achados else NAO_INFORMADO


def detectar_tipo_aplicacao(texto_norm):
    for rotulo, termos in TIPO_APLICACAO_REGRAS:
        for termo in termos:
            if termo in texto_norm:
                return rotulo
    return NAO_CLASSIFICAVEL


def detectar_dados(texto_norm):
    achados = []
    for rotulo, termos in DADOS_REGRAS:
        for termo in termos:
            if termo in texto_norm:
                achados.append(rotulo)
                break
    return "; ".join(achados) if achados else NAO_INFORMADO


def extrair_sentenca_gatilho(resumo_original, gatilhos):
    for sentenca in dividir_sentencas(resumo_original):
        sentenca_norm = normalizar(sentenca)
        for gatilho in gatilhos:
            if gatilho in sentenca_norm:
                return sentenca.strip()
    return None


def detectar_criterios(texto_norm):
    resultado = {}
    for campo, termos in CRITERIOS_REGRAS.items():
        resultado[campo] = any(termo in texto_norm for termo in termos)
    return resultado


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(IN_PATH, encoding="utf-8-sig", newline="") as f:
        linhas_entrada = list(csv.DictReader(f))

    linhas_saida = []
    contadores = {
        "pais_informado": 0,
        "tipo_aplicacao_classificado": 0,
        "dados_informado": 0,
        "resultado_informado": 0,
        "lacuna_informada": 0,
        "resumo_suficiente_sim": 0,
        "resumo_suficiente_parcial": 0,
        "resumo_suficiente_nao": 0,
    }
    cont_criterios = {c: 0 for c in CRITERIOS_REGRAS}
    cont_tipo_aplicacao = {}
    cont_dados = {}

    for row in linhas_entrada:
        titulo = row.get("titulo", "") or ""
        resumo = row.get("resumo", "") or ""
        palavras_chave = row.get("palavras_chave", "") or ""
        resumo_presente = row.get("resumo_presente", "") == "sim"

        texto_norm = normalizar(titulo) + normalizar(resumo) + normalizar(palavras_chave)

        pais_contexto = detectar_pais(texto_norm)
        tipo_aplicacao = detectar_tipo_aplicacao(texto_norm)
        dados_utilizados = detectar_dados(texto_norm)

        sentenca_resultado = extrair_sentenca_gatilho(resumo, GATILHOS_RESULTADO)
        resultado_principal = sentenca_resultado if sentenca_resultado else NAO_INFORMADO

        sentenca_lacuna = extrair_sentenca_gatilho(resumo, GATILHOS_LACUNA)
        lacuna_identificada = sentenca_lacuna if sentenca_lacuna else NAO_IDENTIFICAVEL

        if resumo_presente:
            criterios = detectar_criterios(texto_norm)
            criterios_valores = {c: ("sim" if v else "nao") for c, v in criterios.items()}
        else:
            criterios = {c: False for c in CRITERIOS_REGRAS}
            criterios_valores = {c: NAO_VERIFICAVEL for c in CRITERIOS_REGRAS}

        # contagem de campos com informacao alem do valor de ausencia, para
        # resumo_suficiente_para_extracao
        n_preenchidos = sum([
            pais_contexto != NAO_INFORMADO,
            tipo_aplicacao != NAO_CLASSIFICAVEL,
            dados_utilizados != NAO_INFORMADO,
            resultado_principal != NAO_INFORMADO,
            lacuna_identificada != NAO_IDENTIFICAVEL,
            any(criterios.values()),
        ])
        if not resumo_presente:
            resumo_suficiente = "nao"
        elif n_preenchidos >= 3:
            resumo_suficiente = "sim"
        elif n_preenchidos >= 1:
            resumo_suficiente = "parcial"
        else:
            resumo_suficiente = "nao"

        contadores["resumo_suficiente_" + resumo_suficiente] += 1
        if pais_contexto != NAO_INFORMADO:
            contadores["pais_informado"] += 1
        if tipo_aplicacao != NAO_CLASSIFICAVEL:
            contadores["tipo_aplicacao_classificado"] += 1
        if dados_utilizados != NAO_INFORMADO:
            contadores["dados_informado"] += 1
        if resultado_principal != NAO_INFORMADO:
            contadores["resultado_informado"] += 1
        if lacuna_identificada != NAO_IDENTIFICAVEL:
            contadores["lacuna_informada"] += 1
        for c, v in criterios.items():
            if v:
                cont_criterios[c] += 1
        cont_tipo_aplicacao[tipo_aplicacao] = cont_tipo_aplicacao.get(tipo_aplicacao, 0) + 1
        for rotulo in dados_utilizados.split("; ") if dados_utilizados != NAO_INFORMADO else []:
            cont_dados[rotulo] = cont_dados.get(rotulo, 0) + 1

        linha_saida = {campo: row.get(campo, "") for campo in FIELDS_FINAIS if campo in row}
        linha_saida.update({
            "pais_contexto": pais_contexto,
            "tipo_aplicacao": tipo_aplicacao,
            "dados_utilizados": dados_utilizados,
            "resultado_principal": resultado_principal,
            "contribuicao_para_artigo": "a_definir_na_sintese",
            "lacuna_identificada": lacuna_identificada,
            "criterios_ambientais": criterios_valores["criterios_ambientais"],
            "criterios_economicos": criterios_valores["criterios_economicos"],
            "criterios_sociais": criterios_valores["criterios_sociais"],
            "criterios_tecnicos_operacionais": criterios_valores["criterios_tecnicos_operacionais"],
            "criterios_institucionais": criterios_valores["criterios_institucionais"],
            "criterios_risco": criterios_valores["criterios_risco"],
            "base_evidencia_extracao": BASE_EVIDENCIA,
            "resumo_suficiente_para_extracao": resumo_suficiente,
            "uso_no_artigo": "pendente",
            "observacoes": row.get("observacoes", "") or "",
        })
        linhas_saida.append({campo: linha_saida.get(campo, "") for campo in FIELDS_FINAIS})

    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS_FINAIS)
        w.writeheader()
        for linha in linhas_saida:
            w.writerow(linha)

    total = len(linhas_saida)

    rel = []
    rel.append("# RELATORIO DE PREENCHIMENTO DA MATRIZ DE EXTRACAO FINAL -- ETAPA_13\n")
    rel.append(
        f"Gerado por `00_CONFIG/preencher_matriz_extracao_final.py`, a partir de "
        f"`07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv` ({total} registros do "
        "nucleo analitico revisado). Preenche as colunas de conteudo do esquema definido na "
        "ETAPA_12, por casamento de frases-chave em titulo+resumo+palavras-chave -- sem leitura de "
        "texto completo, conforme mudanca de estrategia registrada em "
        "`00_CONTROLE/DECISOES_METODOLOGICAS.md` (entrada de 2026-07-09).\n"
    )

    rel.append("## 1. Cobertura dos campos de conteudo (fora do valor de ausencia)\n")
    rel.append("| Campo | N preenchido | % do nucleo |")
    rel.append("|---|---:|---:|")
    rel.append(f"| `pais_contexto` | {contadores['pais_informado']} | {100*contadores['pais_informado']/total:.1f}% |")
    rel.append(f"| `tipo_aplicacao` (classificado) | {contadores['tipo_aplicacao_classificado']} | {100*contadores['tipo_aplicacao_classificado']/total:.1f}% |")
    rel.append(f"| `dados_utilizados` | {contadores['dados_informado']} | {100*contadores['dados_informado']/total:.1f}% |")
    rel.append(f"| `resultado_principal` | {contadores['resultado_informado']} | {100*contadores['resultado_informado']/total:.1f}% |")
    rel.append(f"| `lacuna_identificada` | {contadores['lacuna_informada']} | {100*contadores['lacuna_informada']/total:.1f}% |")
    rel.append("")

    rel.append("## 2. Criterios de sustentabilidade/gestao detectados (`sim`, multi-label)\n")
    rel.append("| Criterio | N registros com `sim` | % do nucleo |")
    rel.append("|---|---:|---:|")
    for c, v in sorted(cont_criterios.items(), key=lambda kv: -kv[1]):
        rel.append(f"| `{c}` | {v} | {100*v/total:.1f}% |")
    rel.append("")

    rel.append("## 3. Distribuicao de `tipo_aplicacao`\n")
    rel.append("| Categoria | N registros | % do nucleo |")
    rel.append("|---|---:|---:|")
    for k, v in sorted(cont_tipo_aplicacao.items(), key=lambda kv: -kv[1]):
        rel.append(f"| {k} | {v} | {100*v/total:.1f}% |")
    rel.append("")

    rel.append("## 4. Distribuicao de `dados_utilizados` (categorias, multi-label)\n")
    if cont_dados:
        rel.append("| Categoria | N registros |")
        rel.append("|---|---:|")
        for k, v in sorted(cont_dados.items(), key=lambda kv: -kv[1]):
            rel.append(f"| {k} | {v} |")
    else:
        rel.append("Nenhuma categoria de dado detectada.")
    rel.append("")

    rel.append("## 5. `resumo_suficiente_para_extracao`\n")
    rel.append("| Valor | N registros | % do nucleo |")
    rel.append("|---|---:|---:|")
    for k in ("sim", "parcial", "nao"):
        v = contadores[f"resumo_suficiente_{k}"]
        rel.append(f"| {k} | {v} | {100*v/total:.1f}% |")
    rel.append("")

    rel.append("## 6. Metodo e limites\n")
    rel.append(
        "Deteccao por casamento de frases-chave (listas fixas neste script), sem LLM para gerar "
        "achados -- mesmo padrao de `00_CONFIG/pre_triagem.py` e "
        "`00_CONFIG/sintese_tematica_preliminar.py`. `resultado_principal` e `lacuna_identificada` "
        "sao extraidos como a sentenca literal do resumo que contem uma frase-gatilho (ex.: "
        "\"results show\", \"future research\") -- nao sao resumos gerados, sao trechos copiados do "
        "proprio resumo. `dados_utilizados` e preenchido por categoria reconhecida por palavra-"
        "chave, nao por paraphrase livre -- interpretacao pratica do esquema da ETAPA_12 para manter "
        "o metodo reprodutivel (divergencia documentada, ver "
        "`00_CONTROLE/DECISOES_METODOLOGICAS.md`). `contribuicao_para_artigo` fica fixo em "
        "`a_definir_na_sintese` e `uso_no_artigo` fica fixo em `pendente` para todos os registros -- "
        "sao decisoes de julgamento reservadas para a etapa de sintese/redacao, fora do escopo "
        "desta etapa. Registros sem resumo (`resumo_presente != sim`) tem os seis campos "
        f"`criterios_*` marcados `{NAO_VERIFICAVEL}` e `resumo_suficiente_para_extracao = nao` "
        "automaticamente, sem tentativa de deteccao por palavra-chave restrita ao titulo.\n"
    )

    rel.append("## 7. Arquivos gerados\n")
    rel.append("- `07_SINTESE_TEMATICA/matriz_extracao_final.csv` -- 1 linha por registro do nucleo, 49 colunas.")
    rel.append("- `07_SINTESE_TEMATICA/relatorio_preenchimento_matriz_extracao_final.md` -- este relatorio.")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(rel) + "\n")

    print(f"Total processado: {total}")
    print(f"resumo_suficiente_para_extracao: sim={contadores['resumo_suficiente_sim']} "
          f"parcial={contadores['resumo_suficiente_parcial']} nao={contadores['resumo_suficiente_nao']}")


if __name__ == "__main__":
    main()
