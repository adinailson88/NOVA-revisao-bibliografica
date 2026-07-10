"""
Script da ETAPA_11 - SINTESE_TEMATICA_PRELIMINAR.

Constroi a matriz de extracao/sintese tematica preliminar sobre o nucleo analitico revisado da
ETAPA_10 (05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv, coluna
nucleo_analitico_revisado == "TRUE", 3.678 registros).

Escopo explicito desta etapa (nao ultrapassar):
- Trabalha SOMENTE com titulo + resumo + palavras-chave ja capturados em
  03_PROCESSADOS/corpus_consolidado.csv. Nao le PDF/texto completo.
- Nao decide "uso_no_artigo" nem escreve texto do artigo -- essas decisoes exigem leitura de
  texto completo, fora do escopo desta etapa.
- Colunas da matriz de extracao (ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt, secao 14) que dependem de
  leitura de texto completo (resultado_principal, contribuicao_para_artigo, lacuna_identificada,
  dados_utilizados, tipo_aplicacao, criterios_* , pais_contexto, uso_no_artigo) sao preenchidas com
  o valor fixo "pendente_leitura_completa" -- nao inventadas.

Metodo: casamento de frases-chave (regras explicitas, sem LLM para gerar achados -- mesmo padrao
de 00_CONFIG/pre_triagem.py), reutilizando os blocos A/B/C/D/tecnologico/conceitual ja computados
na ETAPA_07/ETAPA_09/ETAPA_10 e adicionando deteccao de metodo MCDM especifico e tecnologia
especifica (exigidos pela matriz de extracao do roteiro, secao 14: usa_topsis, usa_ahp,
usa_outro_mcdm, usa_bim, usa_digital_twin, usa_iot, usa_data_driven).

Eixo tematico preliminar (unico rotulo, para tabulacao descritiva; nao substitui os flags
multi-label, que ficam preservados na matriz): ordem de prioridade documentada no relatorio,
secao 3.

Saidas:
- 07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv
- 07_SINTESE_TEMATICA/tabela_eixo_tematico_preliminar.csv
- 07_SINTESE_TEMATICA/tabela_metodos_mcdm_especificos.csv
- 07_SINTESE_TEMATICA/tabela_tecnologias_especificas.csv
- 07_SINTESE_TEMATICA/tabela_tipo_edificacao_sinal.csv
- 07_SINTESE_TEMATICA/relatorio_sintese_tematica_preliminar.md
"""

import csv
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUCLEO_PATH = os.path.join(BASE_DIR, "05_ANALISE_R", "tabelas", "matriz_nucleo_analitico_revisado.csv")
CORPUS_PATH = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado.csv")
OUT_DIR = os.path.join(BASE_DIR, "07_SINTESE_TEMATICA")
MATRIZ_PATH = os.path.join(OUT_DIR, "matriz_sintese_tematica_preliminar.csv")
TAB_EIXO_PATH = os.path.join(OUT_DIR, "tabela_eixo_tematico_preliminar.csv")
TAB_MCDM_PATH = os.path.join(OUT_DIR, "tabela_metodos_mcdm_especificos.csv")
TAB_TEC_PATH = os.path.join(OUT_DIR, "tabela_tecnologias_especificas.csv")
TAB_TIPO_EDIF_PATH = os.path.join(OUT_DIR, "tabela_tipo_edificacao_sinal.csv")
RELATORIO_PATH = os.path.join(OUT_DIR, "relatorio_sintese_tematica_preliminar.md")

PENDENTE = "pendente_leitura_completa"

# ---------------------------------------------------------------------------
# Vocabulario de metodo MCDM especifico (subconjunto nomeado do Bloco C ja usado em
# 00_CONFIG/pre_triagem.py; aqui so para etiquetar QUAL metodo, nao para decidir inclusao).
# ---------------------------------------------------------------------------
METODOS_MCDM_NOMEADOS = {
    "topsis": "TOPSIS",
    "ahp": "AHP",
    "anp": "ANP",
    "promethee": "PROMETHEE",
    "electre": "ELECTRE",
    "vikor": "VIKOR",
    "dematel": "DEMATEL",
    "bwm": "BWM",
    "best-worst method": "BWM",
}
MCDM_GENERICO = [
    "multi-criteria", "multi criteria", "multicriteria", "mcdm", "mcda",
    "decision support", "decision-making", "decision making", "prioritiz",
]

# ---------------------------------------------------------------------------
# Vocabulario de tecnologia especifica (subconjunto nomeado do Bloco tecnologico ja usado em
# 00_CONFIG/pre_triagem.py).
# ---------------------------------------------------------------------------
TECNOLOGIAS_NOMEADAS = {
    "bim": "BIM",
    "building information model": "BIM",
    "digital twin": "Digital Twin",
    "iot": "IoT",
    "internet of things": "IoT",
    "data-driven": "Data-driven",
    "data driven": "Data-driven",
}
TECNOLOGIA_OUTRA = [
    "smart campus", "intelligent building", "smart building", "campus infrastructure",
    "predictive maintenance",
]

TIPO_EDIFICACAO_SINAIS = {
    "hospital": "hospitalar/saude",
    "health": "hospitalar/saude",
    "school building": "escolar",
    "educational building": "escolar",
    "university": "universitario/campus",
    "campus": "universitario/campus",
    "higher education": "universitario/campus",
    "residential": "residencial",
    "housing": "residencial",
    "dwelling": "residencial",
    "office building": "comercial/escritorio",
    "commercial building": "comercial/escritorio",
    "government building": "publico_geral",
    "public building": "publico_geral",
    "public sector building": "publico_geral",
    "industrial building": "industrial_predial",
}


def normalizar(texto):
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\s+", " ", t)
    return f" {t.strip()} "


def termos_encontrados(texto_norm, termos):
    return [t for t in termos if t.strip() in texto_norm]


def detectar_metodo_mcdm(texto_norm):
    nomeados = []
    for termo, rotulo in METODOS_MCDM_NOMEADOS.items():
        if termo in texto_norm and rotulo not in nomeados:
            nomeados.append(rotulo)
    generico = bool(termos_encontrados(texto_norm, MCDM_GENERICO))
    if not nomeados and generico:
        nomeados = ["MCDM/MCDA generico (sem metodo nomeado no titulo+resumo)"]
    usa_topsis = "TOPSIS" in nomeados
    usa_ahp = "AHP" in nomeados
    usa_outro_mcdm = any(r not in ("TOPSIS", "AHP") for r in nomeados)
    return usa_topsis, usa_ahp, usa_outro_mcdm, nomeados


def detectar_tecnologia(texto_norm):
    nomeadas = []
    for termo, rotulo in TECNOLOGIAS_NOMEADAS.items():
        if termo in texto_norm and rotulo not in nomeadas:
            nomeadas.append(rotulo)
    outras = termos_encontrados(texto_norm, TECNOLOGIA_OUTRA)
    for termo in outras:
        rotulo = f"outra tecnologia: {termo}"
        if rotulo not in nomeadas:
            nomeadas.append(rotulo)
    usa_bim = "BIM" in nomeadas
    usa_digital_twin = "Digital Twin" in nomeadas
    usa_iot = "IoT" in nomeadas
    usa_data_driven = "Data-driven" in nomeadas
    return usa_bim, usa_digital_twin, usa_iot, usa_data_driven, nomeadas


def detectar_tipo_edificacao(texto_norm):
    achados = []
    for termo, rotulo in TIPO_EDIFICACAO_SINAIS.items():
        if termo in texto_norm and rotulo not in achados:
            achados.append(rotulo)
    return achados if achados else ["nao_identificado_por_resumo"]


def eixo_tematico(bloco_c_presente, usa_outro_mcdm_flag, usa_topsis, usa_ahp,
                   bloco_tecnologico_presente, bloco_conceitual_presente, bloco_d_presente):
    if bloco_c_presente or usa_outro_mcdm_flag or usa_topsis or usa_ahp:
        return "gestao_predial_com_decisao_multicriterio"
    if bloco_tecnologico_presente:
        return "gestao_predial_com_tecnologia_aplicada"
    if bloco_conceitual_presente:
        return "gestao_predial_biossistemica_conceitual"
    if bloco_d_presente:
        return "gestao_predial_contexto_publico_universitario"
    return "gestao_predial_sustentabilidade_geral"


MATRIZ_FIELDS = [
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
    "uso_no_artigo", "necessita_leitura_completa", "observacoes",
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(NUCLEO_PATH, encoding="utf-8-sig", newline="") as f:
        nucleo_rows = list(csv.DictReader(f))
    nucleo_rows = [r for r in nucleo_rows if r.get("nucleo_analitico_revisado") == "TRUE"]

    with open(CORPUS_PATH, encoding="utf-8-sig", newline="") as f:
        corpus_rows = list(csv.DictReader(f))
    corpus_por_id = {r["id_unico"]: r for r in corpus_rows}

    linhas = []
    sem_correspondencia_corpus = []

    for nrow in nucleo_rows:
        id_unico = nrow["id_unico"]
        crow = corpus_por_id.get(id_unico)
        if crow is None:
            sem_correspondencia_corpus.append(id_unico)
            continue

        titulo_norm = normalizar(nrow.get("titulo", ""))
        resumo_norm = normalizar(crow.get("resumo", ""))
        texto_norm = titulo_norm + resumo_norm

        usa_topsis, usa_ahp, usa_outro_mcdm, metodos = detectar_metodo_mcdm(texto_norm)
        usa_bim, usa_digital_twin, usa_iot, usa_data_driven, tecnologias = detectar_tecnologia(texto_norm)
        tipos_edificacao = detectar_tipo_edificacao(texto_norm)

        bloco_c_presente = nrow.get("bloco_c_presente") == "sim"
        bloco_d_presente = nrow.get("bloco_d_presente") == "sim"
        bloco_tec_presente = nrow.get("bloco_tecnologico_presente") == "sim"
        bloco_conc_presente = nrow.get("bloco_conceitual_presente") == "sim"

        eixo = eixo_tematico(
            bloco_c_presente, usa_outro_mcdm, usa_topsis, usa_ahp,
            bloco_tec_presente, bloco_conc_presente, bloco_d_presente,
        )

        linha = {
            "id_unico": id_unico,
            "doi": nrow.get("doi", ""),
            "titulo": nrow.get("titulo", ""),
            "ano": nrow.get("ano", ""),
            "autores": crow.get("autores", ""),
            "fonte_periodico": crow.get("fonte_periodico", ""),
            "tipo_documento": crow.get("tipo_documento", ""),
            "bases_origem": nrow.get("bases_origem", ""),
            "strings_origem": crow.get("strings_origem", ""),
            "resumo_presente": nrow.get("resumo_presente", ""),
            "palavras_chave": crow.get("palavras_chave", ""),
            "resumo": crow.get("resumo", ""),
            "bloco_a_presente": nrow.get("bloco_a_presente", ""),
            "bloco_b_presente": nrow.get("bloco_b_presente", ""),
            "bloco_c_presente": nrow.get("bloco_c_presente", ""),
            "bloco_d_presente": nrow.get("bloco_d_presente", ""),
            "bloco_tecnologico_presente": nrow.get("bloco_tecnologico_presente", ""),
            "bloco_conceitual_presente": nrow.get("bloco_conceitual_presente", ""),
            "termos_bloco_a": nrow.get("termos_bloco_a", ""),
            "termos_bloco_b": nrow.get("termos_bloco_b", ""),
            "usa_topsis": "sim" if usa_topsis else "nao",
            "usa_ahp": "sim" if usa_ahp else "nao",
            "usa_outro_mcdm": "sim" if usa_outro_mcdm else "nao",
            "metodo_mcdm_especifico": "; ".join(metodos),
            "usa_bim": "sim" if usa_bim else "nao",
            "usa_digital_twin": "sim" if usa_digital_twin else "nao",
            "usa_iot": "sim" if usa_iot else "nao",
            "usa_data_driven": "sim" if usa_data_driven else "nao",
            "tecnologia_especifica": "; ".join(tecnologias),
            "tipo_edificacao_sinal": "; ".join(tipos_edificacao),
            "eixo_tematico_preliminar": eixo,
            "classe_final_sem_duvida": nrow.get("classe_final_sem_duvida", ""),
            "nucleo_analitico_revisado": nrow.get("nucleo_analitico_revisado", ""),
            "pais_contexto": PENDENTE,
            "tipo_aplicacao": PENDENTE,
            "dados_utilizados": PENDENTE,
            "resultado_principal": PENDENTE,
            "contribuicao_para_artigo": PENDENTE,
            "lacuna_identificada": PENDENTE,
            "criterios_ambientais": PENDENTE,
            "criterios_economicos": PENDENTE,
            "criterios_sociais": PENDENTE,
            "criterios_tecnicos_operacionais": PENDENTE,
            "criterios_institucionais": PENDENTE,
            "criterios_risco": PENDENTE,
            "uso_no_artigo": PENDENTE,
            "necessita_leitura_completa": "sim",
            "observacoes": "",
        }
        linhas.append(linha)

    if sem_correspondencia_corpus:
        raise SystemExit(
            f"ERRO: {len(sem_correspondencia_corpus)} id_unico do nucleo nao encontrados em "
            f"corpus_consolidado.csv -- interrompendo sem gravar saida. Exemplos: "
            f"{sem_correspondencia_corpus[:5]}"
        )

    with open(MATRIZ_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MATRIZ_FIELDS)
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)

    total = len(linhas)

    def contagem(campo):
        c = {}
        for linha in linhas:
            v = linha[campo]
            c[v] = c.get(v, 0) + 1
        return c

    cont_eixo = contagem("eixo_tematico_preliminar")

    cont_mcdm = {}
    for linha in linhas:
        for m in linha["metodo_mcdm_especifico"].split("; "):
            if m:
                cont_mcdm[m] = cont_mcdm.get(m, 0) + 1

    cont_tec = {}
    for linha in linhas:
        for t in linha["tecnologia_especifica"].split("; "):
            if t:
                cont_tec[t] = cont_tec.get(t, 0) + 1

    cont_tipo_edif = {}
    for linha in linhas:
        for t in linha["tipo_edificacao_sinal"].split("; "):
            if t:
                cont_tipo_edif[t] = cont_tipo_edif.get(t, 0) + 1

    with open(TAB_EIXO_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["eixo_tematico_preliminar", "n_registros", "pct_do_nucleo"])
        for k, v in sorted(cont_eixo.items(), key=lambda kv: -kv[1]):
            w.writerow([k, v, f"{100*v/total:.1f}"])

    with open(TAB_MCDM_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metodo_mcdm_especifico", "n_registros"])
        for k, v in sorted(cont_mcdm.items(), key=lambda kv: -kv[1]):
            w.writerow([k, v])

    with open(TAB_TEC_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tecnologia_especifica", "n_registros"])
        for k, v in sorted(cont_tec.items(), key=lambda kv: -kv[1]):
            w.writerow([k, v])

    with open(TAB_TIPO_EDIF_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tipo_edificacao_sinal", "n_registros"])
        for k, v in sorted(cont_tipo_edif.items(), key=lambda kv: -kv[1]):
            w.writerow([k, v])

    n_sem_resumo = sum(1 for l in linhas if l["resumo_presente"] != "sim")

    rel = []
    rel.append("# RELATORIO DE SINTESE TEMATICA PRELIMINAR -- ETAPA_11\n")
    rel.append(
        "Gerado por `00_CONFIG/sintese_tematica_preliminar.py`, a partir do nucleo analitico "
        f"revisado da ETAPA_10 (`05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv`, "
        f"coluna `nucleo_analitico_revisado == TRUE`, {total} registros), enriquecido com "
        "autores/fonte/tipo de documento/resumo/palavras-chave de "
        "`03_PROCESSADOS/corpus_consolidado.csv`.\n"
    )

    rel.append("## 1. Escopo e limite desta etapa\n")
    rel.append(
        "Esta etapa trabalha somente com titulo, resumo e palavras-chave -- nao houve leitura de "
        "texto completo (PDF) de nenhum dos "
        f"{total} registros do nucleo. Por isso, as colunas da matriz de extracao que dependem de "
        "leitura de texto completo (`pais_contexto`, `tipo_aplicacao`, `dados_utilizados`, "
        "`resultado_principal`, `contribuicao_para_artigo`, `lacuna_identificada`, `criterios_*`, "
        f"`uso_no_artigo`) foram preenchidas com o valor fixo `{PENDENTE}` em todos os registros -- "
        "nao inventadas nem inferidas do resumo. A coluna `necessita_leitura_completa` esta `sim` "
        "para os {0} registros. Esta etapa nao decide inclusao/exclusao final no artigo nem redige "
        "texto do artigo.\n".format(total)
    )

    rel.append("## 2. Correspondencia com a matriz de extracao do roteiro-mestre (secao 14)\n")
    rel.append(
        "A matriz gerada nesta etapa reaproveita os nomes de coluna ja usados no pipeline "
        "operacional (`bloco_a_presente`, `bloco_b_presente` etc., ETAPA_07/09/10) em vez dos nomes "
        "originais do roteiro (`objeto_predial`, `dimensao_sustentabilidade` etc.) -- ver "
        "`ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt`, secao 26.4, que ja documenta essa divergencia de "
        "nomenclatura entre o roteiro-mestre e o pipeline real. Correcao de digitacao aplicada "
        "conforme secao 26.5 do roteiro: coluna `usa_topsis` (nao `usa_topis`). A coluna "
        "`strings_origem` do roteiro existe em `corpus_consolidado.csv` no nivel do registro "
        "consolidado (uma string por registro, apos deduplicacao) -- nao no nivel de string de "
        "busca original por base; rastreabilidade por string bruta fica em `01_PROTOCOLO` e "
        "`02_DADOS_BRUTOS`.\n"
    )

    rel.append("## 3. Eixo tematico preliminar\n")
    rel.append(
        "Rotulo unico por registro, calculado por prioridade (documentada para permitir "
        "reproducao): (1) decisao multicriterio (Bloco C ou metodo MCDM nomeado no titulo+resumo); "
        "(2) tecnologia aplicada (Bloco tecnologico: BIM, digital twin, IoT, data-driven, smart "
        "campus, predictive maintenance); (3) conceitual/biossistemico (Bloco conceitual: built "
        "environment, urban metabolism, biophilic, etc.); (4) contexto publico/universitario "
        "(Bloco D); (5) gestao predial e sustentabilidade geral (nenhum dos anteriores). Um mesmo "
        "registro pode ter mais de um sinal presente (ver colunas `bloco_c_presente`, "
        "`bloco_tecnologico_presente` etc., preservadas na matriz); o eixo preliminar so escolhe um "
        "rotulo dominante para tabulacao descritiva, pela ordem acima. Rotular um registro com "
        "metodo multicriterio dominante e apenas descricao do conteudo do resumo -- nao reintroduz "
        "MCDM/AHP/TOPSIS como objeto central do artigo (foco vigente: manutencao predial e gestao "
        "de edificacoes -- ver `00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md`).\n"
    )
    rel.append("| Eixo tematico preliminar | N registros | % do nucleo |")
    rel.append("|---|---|---|")
    for k, v in sorted(cont_eixo.items(), key=lambda kv: -kv[1]):
        rel.append(f"| {k} | {v} | {100*v/total:.1f}% |")
    rel.append("")

    rel.append("## 4. Metodos MCDM nomeados detectados (titulo+resumo)\n")
    if cont_mcdm:
        rel.append("| Metodo | N registros |")
        rel.append("|---|---|")
        for k, v in sorted(cont_mcdm.items(), key=lambda kv: -kv[1]):
            rel.append(f"| {k} | {v} |")
    else:
        rel.append("Nenhum metodo MCDM nomeado detectado.")
    rel.append("")

    rel.append("## 5. Tecnologias especificas detectadas (titulo+resumo)\n")
    if cont_tec:
        rel.append("| Tecnologia | N registros |")
        rel.append("|---|---|")
        for k, v in sorted(cont_tec.items(), key=lambda kv: -kv[1]):
            rel.append(f"| {k} | {v} |")
    else:
        rel.append("Nenhuma tecnologia especifica detectada.")
    rel.append("")

    rel.append("## 6. Sinal de tipo de edificacao (titulo+resumo)\n")
    rel.append(
        "Sinal preliminar, nao definitivo -- baseado em palavra-chave explicita em titulo+resumo, "
        "sujeito a leitura de texto completo posterior. Um mesmo registro pode ter mais de um sinal.\n"
    )
    rel.append("| Sinal | N registros |")
    rel.append("|---|---|")
    for k, v in sorted(cont_tipo_edif.items(), key=lambda kv: -kv[1]):
        rel.append(f"| {k} | {v} |")
    rel.append("")

    rel.append("## 7. Cobertura de resumo dentro do nucleo\n")
    rel.append(
        f"{n_sem_resumo} de {total} registros do nucleo ({100*n_sem_resumo/total:.1f}%) estao sem "
        "resumo (`resumo_presente != sim`) -- para esses, a deteccao de metodo/tecnologia/tipo de "
        "edificacao desta etapa usou apenas o titulo, com cobertura de vocabulario proporcionalmente "
        "menor. Isso nao afeta a permanencia do registro no nucleo (decisao ja tomada na ETAPA_10), "
        "apenas reduz a granularidade da sintese tematica preliminar para esses casos.\n"
    )

    rel.append("## 8. Limites desta etapa\n")
    rel.append(
        "Deteccao por casamento de frases-chave em titulo+resumo, sem LLM para gerar achados -- "
        "mesmo metodo e mesmas limitacoes de falso positivo/negativo ja registradas para "
        "`00_CONFIG/pre_triagem.py`. `eixo_tematico_preliminar` e um rotulo dominante unico por "
        "prioridade fixa -- nao substitui os flags multi-label, que permanecem na matriz para "
        "quem precisar de outra prioridade. Nenhuma das colunas dependentes de leitura de texto "
        "completo foi preenchida (ver secao 1) -- essa e a fronteira explicita desta etapa, "
        "conforme instrucao vigente de nao iniciar leitura full-text nem escrita do artigo. Autores "
        f"(`autores`) tem cobertura baixa no corpus consolidado (24,1% dos {9542} registros "
        "unicos, herdada da ETAPA_06) -- nao e falha desta etapa, e limite dos metadados "
        "recuperados na coleta.\n"
    )

    rel.append("## 9. Arquivos gerados\n")
    rel.append("- `07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv` -- 1 linha por registro do nucleo.")
    rel.append("- `07_SINTESE_TEMATICA/tabela_eixo_tematico_preliminar.csv`")
    rel.append("- `07_SINTESE_TEMATICA/tabela_metodos_mcdm_especificos.csv`")
    rel.append("- `07_SINTESE_TEMATICA/tabela_tecnologias_especificas.csv`")
    rel.append("- `07_SINTESE_TEMATICA/tabela_tipo_edificacao_sinal.csv`")
    rel.append("- `07_SINTESE_TEMATICA/relatorio_sintese_tematica_preliminar.md` -- este relatorio.")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(rel) + "\n")

    print(f"Total nucleo processado: {total}")
    print("Eixo tematico preliminar:")
    for k, v in sorted(cont_eixo.items(), key=lambda kv: -kv[1]):
        print(f"  {k}: {v} ({100*v/total:.1f}%)")
    print(f"Registros sem correspondencia no corpus: {len(sem_correspondencia_corpus)}")


if __name__ == "__main__":
    main()
