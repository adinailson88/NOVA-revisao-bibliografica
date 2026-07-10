"""
Script de pre-triagem reprodutivel (ETAPA_07 - PRE_TRIAGEM).

Classifica cada registro de 03_PROCESSADOS/corpus_consolidado.csv em uma das 5 classes exigidas
pelo prompt da etapa (00_CONTROLE/ROTINAS/PROMPTS/ETAPA_07_PRE_TRIAGEM.md): relevante, irrelevante,
duvida, sem_resumo, complementar.

Metodo: casamento de frases-chave (script local, regras explicitas, sem uso de LLM para gerar
achados -- conforme roteiro-mestre, ETAPA 7: "nao usar LLM para criar achados; usar apenas para
triagem assistida e justificavel"). Todas as listas de termos usadas ficam registradas no
relatorio para reprodutibilidade.

Regra explicita do prompt da etapa: TOPSIS/AHP/MCDM/universidade/campus/public building NAO
contam como inclusao automatica -- por isso os blocos C (decisao/MCDM) e D (contexto publico/
universitario) sao apenas etiquetas informativas (bloco_c_presente, bloco_d_presente) e nunca,
sozinhos, produzem a classe "relevante".

Bloco A (objeto predial) e dividido em termos fortes (ja contem "building"/"facilit-", contam
sozinhos) e fracos (genericos como "operation and maintenance", "maintenance management" --
tambem aparecem em agua, energia, veiculos, infraestrutura em geral; so contam se acompanhados de
um token de contexto de edificacao no mesmo titulo+resumo). Essa divisao foi introduzida apos
auditoria da primeira rodada: sem ela, "operation and maintenance" sozinho respondia por ~42% dos
registros classificados "relevante", muitos sem nenhuma relacao com edificacoes.

Arvore de decisao (por registro):
1. Sem resumo (resumo_presente == "nao")            -> classe = sem_resumo
   (sinal_titulo informativo calculado a partir do titulo, sem virar classe final -- roteiro
   secao 13: registro sem resumo deve ficar com confianca baixa, nao ser incluido por titulo so).
2. Bloco A (objeto predial, forte ou fraco+contexto) E Bloco B (sustentabilidade) presentes -> relevante
3. Bloco A presente E Bloco tecnologico (BIM/digital twin/IoT/smart campus/predictive
   maintenance) presente, mas sem Bloco B                                          -> complementar
4. Bloco conceitual (built environment/urban metabolism/biophilic/etc.) presente    -> complementar
5. Apenas Bloco A OU apenas Bloco B presente (nao os dois)                          -> duvida
6. Nenhum dos blocos A/B/tecnologico/conceitual presente                            -> irrelevante

Saidas:
- 04_TRIAGEM/matriz_pre_triagem.csv
- 04_TRIAGEM/relatorio_pre_triagem.md
"""

import csv
import os
import re
import unicodedata

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS_PATH = os.path.join(BASE_DIR, "03_PROCESSADOS", "corpus_consolidado.csv")
OUT_DIR = os.path.join(BASE_DIR, "04_TRIAGEM")
MATRIZ_PATH = os.path.join(OUT_DIR, "matriz_pre_triagem.csv")
RELATORIO_PATH = os.path.join(OUT_DIR, "relatorio_pre_triagem.md")

# ---------------------------------------------------------------------------
# Listas de termos (fonte: 01_PROTOCOLO/strings_nativas_por_base.md e
# ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt, secao 13, adaptado pela regra vigente da secao 26.3:
# A+B obrigatorios; C e D so reforcam, nunca incluem sozinhos)
# ---------------------------------------------------------------------------

# Termos fortes: ja contem palavra de edificacao/instalacao, contam sozinhos como Bloco A.
BLOCO_A_FORTE = [
    "building maintenance", "facility management", "facilities management",
    "facilities maintenance", "building asset management", "building operation",
    "building portfolio", "building renovation", "building refurbishment",
    "manutencao predial", "gestao predial", "manutencao de edificacoes",
    "mantenimiento de edificios",
]

# Termos fracos: genericos demais (aparecem tambem em agua, energia, veiculos, infraestrutura em
# geral, sem relacao com edificacoes) -- so contam como Bloco A se acompanhados de um token de
# contexto de edificacao/instalacao em BLOCO_A_CONTEXTO no mesmo titulo+resumo. Corrigido apos
# auditoria da primeira rodada: "operation and maintenance" sozinho gerava falso positivo em ~42%
# dos registros classificados "relevante" (ex.: manutencao de usinas de energia renovavel, redes de
# agua, veiculos -- nada relacionado a edificacoes).
BLOCO_A_FRACO = [
    "operation and maintenance", "maintenance management", "maintenance planning",
    "maintenance prioritization", "maintenance priority", "maintenance backlog",
    "maintenance strategy", "renewal prioritization", "deferred maintenance",
    "asset performance", "condition assessment", "condition-based maintenance",
    "condition based maintenance",
    # Termos adicionados em 2026-07-09 apos auditoria da ETAPA_08 (amostra de 2026-07-08) ter
    # confirmado, por leitura individual de conteudo, 6 falsos negativos causados por lacuna de
    # vocabulario -- ver 04_TRIAGEM/relatorio_ajustes_triagem.md secao 5 e
    # 00_CONTROLE/DECISOES_METODOLOGICAS.md, entrada de 2026-07-09.
    "retrofit", "building stock management", "building modernization",
    "built asset management", "public asset management",
]

BLOCO_A_CONTEXTO = [
    "building", "buildings", "facility", "facilities", "campus", "edific", "predial",
]

BLOCO_A_OBJETO_PREDIAL = BLOCO_A_FORTE + BLOCO_A_FRACO

BLOCO_B_SUSTENTABILIDADE = [
    "sustainab", "sustentab", "green building", "life cycle", "life-cycle",
    "whole life cost", "life cycle cost", "service life", "sustainability assessment",
    "sustainability indicator", "environmental performance", "building performance",
    "environmental criteria", "social criteria", "sustainable development goal",
    " esg ", " sdg", "sostenibilidad",
    # Termos adicionados em 2026-07-09 -- mesma origem/motivo do Bloco A acima. "ecological" foi
    # recomendado pela auditoria mas NAO aplicado por cautela explicita (termo generico demais,
    # taxa de falso positivo nao avaliada) -- ver DECISOES_METODOLOGICAS.md, entrada de 2026-07-09.
    "climate neutral", "carbon neutral", "net zero", "net-zero energy", "greenhouse gas",
]

BLOCO_C_DECISAO_MCDM = [
    "multi-criteria", "multi criteria", "multicriteria", "mcdm", "mcda",
    "decision support", "decision-making", "decision making", "topsis", "ahp", "anp",
    "promethee", "electre", "vikor", "dematel", "bwm", "best-worst method", "prioritiz",
]

BLOCO_D_CONTEXTO_PUBLICO_UNIVERSITARIO = [
    "public building", "university building", "university campus", "campus",
    "higher education", "educational building", "government building",
    "public sector building", "school building", "hospital",
]

BLOCO_TECNOLOGICO = [
    "smart campus", "intelligent building", "smart building", "campus infrastructure",
    "digital twin", "bim", "building information model", "iot", "internet of things",
    "predictive maintenance", "data-driven", "data driven",
]

BLOCO_CONCEITUAL = [
    "built environment", "sustainable campus", "green campus", "campus sustainability",
    "regenerative building", "regenerative design", "living building",
    "building as a living system", "urban metabolism", "building metabolism",
    "biophilic building", "biophilic design", "ecosystem services",
    "nature-based solutions", "green infrastructure",
]


def normalizar(texto):
    if not texto:
        return ""
    t = unicodedata.normalize("NFKD", texto)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.lower()
    t = re.sub(r"\s+", " ", t)
    return f" {t.strip()} "


def termos_encontrados(texto_norm, termos):
    achados = [t for t in termos if t.strip() in texto_norm]
    return achados


def bloco_a_valido(texto_norm):
    """Bloco A conta se: (a) algum termo forte presente, ou (b) algum termo fraco presente E
    algum token de contexto de edificacao/instalacao tambem presente no mesmo texto."""
    fortes = termos_encontrados(texto_norm, BLOCO_A_FORTE)
    fracos = termos_encontrados(texto_norm, BLOCO_A_FRACO)
    contexto = termos_encontrados(texto_norm, BLOCO_A_CONTEXTO)
    if fortes:
        return fortes + (fracos if contexto else []), True
    if fracos and contexto:
        return fracos, True
    return fracos, False


def classificar(row):
    titulo_norm = normalizar(row.get("titulo", ""))
    resumo_presente = (row.get("resumo_presente") or "").strip().lower() == "sim"
    resumo_norm = normalizar(row.get("resumo", ""))

    termos_titulo_a, valido_titulo_a = bloco_a_valido(titulo_norm)
    sinal_titulo_b = termos_encontrados(titulo_norm, BLOCO_B_SUSTENTABILIDADE)
    if valido_titulo_a and sinal_titulo_b:
        sinal_titulo = "sugere_relevante"
    elif valido_titulo_a or sinal_titulo_b:
        sinal_titulo = "sugere_parcial"
    else:
        sinal_titulo = "sem_sinal"

    if not resumo_presente:
        return {
            "classe_pre_triagem": "sem_resumo",
            "justificativa": (
                "Registro sem resumo disponivel; nao classificado por conteudo (regra: nao "
                "incluir/excluir por titulo isolado, confianca baixa). Sinal do titulo: "
                f"{sinal_titulo}."
            ),
            "sinal_titulo": sinal_titulo,
            "bloco_a_presente": "sim" if valido_titulo_a else "nao",
            "bloco_b_presente": "sim" if sinal_titulo_b else "nao",
            "bloco_c_presente": "sim" if termos_encontrados(titulo_norm, BLOCO_C_DECISAO_MCDM) else "nao",
            "bloco_d_presente": "sim" if termos_encontrados(titulo_norm, BLOCO_D_CONTEXTO_PUBLICO_UNIVERSITARIO) else "nao",
            "bloco_tecnologico_presente": "nao",
            "bloco_conceitual_presente": "nao",
            "termos_bloco_a": "; ".join(termos_titulo_a),
            "termos_bloco_b": "; ".join(sinal_titulo_b),
        }

    texto_norm = titulo_norm + resumo_norm
    termos_a, bloco_a = bloco_a_valido(texto_norm)
    termos_b = termos_encontrados(texto_norm, BLOCO_B_SUSTENTABILIDADE)
    termos_c = termos_encontrados(texto_norm, BLOCO_C_DECISAO_MCDM)
    termos_d = termos_encontrados(texto_norm, BLOCO_D_CONTEXTO_PUBLICO_UNIVERSITARIO)
    termos_tec = termos_encontrados(texto_norm, BLOCO_TECNOLOGICO)
    termos_conc = termos_encontrados(texto_norm, BLOCO_CONCEITUAL)

    bloco_b = bool(termos_b)
    bloco_tec = bool(termos_tec)
    bloco_conc = bool(termos_conc)

    if bloco_a and bloco_b:
        classe = "relevante"
        justificativa = f"Bloco A ({'; '.join(termos_a[:3])}) e Bloco B ({'; '.join(termos_b[:3])}) presentes."
    elif bloco_a and bloco_tec:
        classe = "complementar"
        justificativa = (
            f"Bloco A presente ({'; '.join(termos_a[:3])}) com termo tecnologico "
            f"({'; '.join(termos_tec[:3])}), sem Bloco B explicito -- complementar tecnologico."
        )
    elif bloco_conc:
        classe = "complementar"
        justificativa = f"Termo conceitual presente ({'; '.join(termos_conc[:3])}) -- complementar/conceitual."
    elif bloco_a or bloco_b:
        classe = "duvida"
        falta = "Bloco B (sustentabilidade)" if bloco_a else "Bloco A (objeto predial)"
        justificativa = f"Apenas um bloco obrigatorio presente; falta {falta}. Requer revisao humana."
    else:
        classe = "irrelevante"
        justificativa = "Nenhum termo de Bloco A nem Bloco B encontrado em titulo+resumo."

    return {
        "classe_pre_triagem": classe,
        "justificativa": justificativa,
        "sinal_titulo": sinal_titulo,
        "bloco_a_presente": "sim" if bloco_a else "nao",
        "bloco_b_presente": "sim" if bloco_b else "nao",
        "bloco_c_presente": "sim" if termos_c else "nao",
        "bloco_d_presente": "sim" if termos_d else "nao",
        "bloco_tecnologico_presente": "sim" if bloco_tec else "nao",
        "bloco_conceitual_presente": "sim" if bloco_conc else "nao",
        "termos_bloco_a": "; ".join(termos_a),
        "termos_bloco_b": "; ".join(termos_b),
    }


MATRIZ_FIELDS = [
    "id_unico", "doi", "titulo", "ano", "bases_origem", "resumo_presente",
    "classe_pre_triagem", "justificativa", "sinal_titulo",
    "bloco_a_presente", "bloco_b_presente", "bloco_c_presente", "bloco_d_presente",
    "bloco_tecnologico_presente", "bloco_conceitual_presente",
    "termos_bloco_a", "termos_bloco_b",
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    with open(CORPUS_PATH, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        registros = list(leitor)

    linhas = []
    for row in registros:
        resultado = classificar(row)
        linhas.append({
            "id_unico": row["id_unico"],
            "doi": row["doi"],
            "titulo": row["titulo"],
            "ano": row["ano"],
            "bases_origem": row["bases_origem"],
            "resumo_presente": row["resumo_presente"],
            **resultado,
        })

    with open(MATRIZ_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=MATRIZ_FIELDS)
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)

    total = len(linhas)
    contagem = {}
    for linha in linhas:
        c = linha["classe_pre_triagem"]
        contagem[c] = contagem.get(c, 0) + 1

    contagem_bases_relevante = {}
    for linha in linhas:
        if linha["classe_pre_triagem"] == "relevante":
            b = linha["bases_origem"]
            contagem_bases_relevante[b] = contagem_bases_relevante.get(b, 0) + 1

    n_relevante_com_c = sum(1 for l in linhas if l["classe_pre_triagem"] == "relevante" and l["bloco_c_presente"] == "sim")
    n_relevante_com_d = sum(1 for l in linhas if l["classe_pre_triagem"] == "relevante" and l["bloco_d_presente"] == "sim")

    rel = []
    rel.append("# RELATORIO DE PRE-TRIAGEM -- ETAPA_07\n")
    rel.append(
        "Gerado por `00_CONFIG/pre_triagem.py`, a partir de "
        f"`03_PROCESSADOS/corpus_consolidado.csv` ({total} registros unicos da ETAPA_06, "
        "re-executada em 2026-07-09 com resumo da Scopus enriquecido manualmente -- 94% de "
        "cobertura de resumo, contra 20% na rodada de 2026-07-08). Classificacao por casamento de "
        "frases-chave (regras explicitas, sem LLM), reprodutivel executando o script novamente. "
        "Vocabulario do classificador ampliado em 2026-07-09 (5 termos novos no Bloco A, 5 no "
        "Bloco B) apos auditoria da amostra de 2026-07-08 ter confirmado falsos negativos por "
        "lacuna de vocabulario -- ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de "
        "2026-07-09.\n"
    )

    rel.append("## 1. Metodo\n")
    rel.append(
        "Cada registro e classificado em uma das 5 classes exigidas pelo prompt da etapa "
        "(`00_CONTROLE/ROTINAS/PROMPTS/ETAPA_07_PRE_TRIAGEM.md`): `relevante`, `irrelevante`, "
        "`duvida`, `sem_resumo`, `complementar`. Arvore de decisao:\n\n"
        "1. Sem resumo disponivel -> `sem_resumo` (nao classificado por conteudo; sinal do titulo "
        "guardado apenas como informacao auxiliar, nunca como classe final -- roteiro secao 13: "
        "nao incluir/excluir por titulo isolado).\n"
        "2. Bloco A (objeto predial) E Bloco B (sustentabilidade) presentes -> `relevante`.\n"
        "3. Bloco A presente com termo tecnologico (BIM/digital twin/IoT/smart campus/predictive "
        "maintenance), sem Bloco B -> `complementar`.\n"
        "4. Termo conceitual presente (built environment/urban metabolism/biophilic/etc.) -> "
        "`complementar`.\n"
        "5. Apenas Bloco A OU apenas Bloco B (nao os dois) -> `duvida`.\n"
        "6. Nenhum dos blocos A/B/tecnologico/conceitual -> `irrelevante`.\n\n"
        "Regra explicita do prompt da etapa, respeitada nesta arvore: Bloco C (multi-criteria, "
        "MCDM, MCDA, TOPSIS, AHP, ANP, PROMETHEE, ELECTRE, VIKOR, DEMATEL, BWM) e Bloco D "
        "(public building, university building/campus, higher education, government building, "
        "school, hospital) **nunca** produzem `relevante` sozinhos -- ficam apenas como colunas "
        "informativas (`bloco_c_presente`, `bloco_d_presente`) para reforcar a classificacao na "
        "auditoria futura (ETAPA_08), nunca como criterio de inclusao.\n"
    )

    rel.append("## 2. Termos usados por bloco (reprodutibilidade)\n")
    rel.append(
        "Bloco A e dividido em termos fortes (contam sozinhos) e fracos (so contam se um token de "
        "contexto de edificacao tambem aparecer no mesmo titulo+resumo) -- ver secao 1 e o "
        "docstring de `00_CONFIG/pre_triagem.py` para o motivo dessa divisao.\n"
    )
    for nome, lista in [
        ("Bloco A -- objeto predial, termos FORTES (contam sozinhos)", BLOCO_A_FORTE),
        ("Bloco A -- objeto predial, termos FRACOS (exigem token de contexto)", BLOCO_A_FRACO),
        ("Bloco A -- tokens de contexto exigidos para termos fracos", BLOCO_A_CONTEXTO),
        ("Bloco B -- sustentabilidade (gating)", BLOCO_B_SUSTENTABILIDADE),
        ("Bloco C -- decisao/MCDM (so etiqueta, nunca inclui sozinho)", BLOCO_C_DECISAO_MCDM),
        ("Bloco D -- contexto publico/universitario (so etiqueta, nunca inclui sozinho)", BLOCO_D_CONTEXTO_PUBLICO_UNIVERSITARIO),
        ("Bloco tecnologico (complementar)", BLOCO_TECNOLOGICO),
        ("Bloco conceitual (complementar)", BLOCO_CONCEITUAL),
    ]:
        rel.append(f"- **{nome}**: {', '.join(sorted(t.strip() for t in lista))}")
    rel.append("")

    rel.append("## 3. Resultado da classificacao\n")
    rel.append("| Classe | N registros | % do total |")
    rel.append("|---|---|---|")
    for classe in ["relevante", "duvida", "complementar", "irrelevante", "sem_resumo"]:
        n = contagem.get(classe, 0)
        rel.append(f"| {classe} | {n} | {100*n/total:.1f}% |")
    rel.append(f"| **Total** | **{total}** | **100.0%** |\n")

    rel.append("## 4. Distribuicao dos relevantes por combinacao de bases\n")
    rel.append("| bases_origem | N registros relevantes |")
    rel.append("|---|---|")
    for bases, qtd in sorted(contagem_bases_relevante.items(), key=lambda kv: -kv[1]):
        rel.append(f"| {bases} | {qtd} |")
    rel.append("")

    rel.append("## 5. Reforco por Bloco C/D dentro dos relevantes (apenas informativo)\n")
    n_relevante = contagem.get("relevante", 0)
    rel.append(
        f"Dos {n_relevante} registros classificados `relevante` (A+B), {n_relevante_com_c} "
        f"({100*n_relevante_com_c/n_relevante:.1f}%) tambem mencionam metodo de decisao/MCDM "
        f"(Bloco C) e {n_relevante_com_d} ({100*n_relevante_com_d/n_relevante:.1f}%) tambem "
        "mencionam contexto publico/universitario (Bloco D). Nenhum dos dois percentuais influencia "
        "a classe -- sao apenas insumo para a auditoria da ETAPA_08 e para o preenchimento futuro "
        "do campo `metodo_decisao` da matriz de extracao.\n"
    )

    rel.append("## 6. Limites desta etapa\n")
    rel.append(
        "Classificacao por casamento de frases-chave e sujeita a falsos positivos/negativos (ex.: "
        "termos genericos como \"maintenance\" ou \"campus\" isolados nao gatilham bloco algum "
        "aqui -- so frases especificas contam, o que pode deixar de fora casos reais com fraseado "
        "atipico). Nao houve verificacao humana registro a registro nesta etapa; a amostra "
        "estratificada de auditoria (30 relevantes, 30 irrelevantes, 20 duvida, 20 sem_resumo, "
        "conforme roteiro secao 15 ETAPA 8) fica para a proxima etapa. `sem_resumo` "
        f"({contagem.get('sem_resumo', 0)} registros, {100*contagem.get('sem_resumo', 0)/total:.1f}% "
        "do total) e um bloco grande e esperado -- Crossref raramente traz abstract e parte do "
        "nucleo Scopus/WoS tambem nao tem resumo capturado (ver `03_PROCESSADOS/"
        "relatorio_deduplicacao.md`, secao 4). Esta pre-triagem nao decide inclusao/exclusao final "
        "do artigo -- e insumo para a auditoria (ETAPA_08) e definicao do nucleo analitico "
        "(ETAPA_09/roteiro).\n\n"
        "Ambiguidade residual conhecida e nao resolvida: a palavra \"facility\"/\"facilities\" serve "
        "de token de contexto para validar termos fracos do Bloco A (ex. \"operation and "
        "maintenance\"), mas tambem aparece em textos sobre instalacoes que nao sao edificacoes "
        "(portos, estacoes de tratamento de agua, plantas industriais). Uma amostra manual "
        "encontrou casos assim classificados como `relevante` indevidamente (ex.: avaliacao de "
        "resiliencia de porto inteligente, reuso de agua). Resolver isso exigiria julgamento de "
        "conteudo alem de casamento de frases -- fora do escopo desta etapa (ETAPA 7: \"nao usar "
        "LLM para criar achados\"); fica como item explicito para a revisao humana da ETAPA_08.\n"
    )

    rel.append("## 7. Arquivos gerados\n")
    rel.append("- `04_TRIAGEM/matriz_pre_triagem.csv` -- 1 linha por registro, com classe, justificativa e blocos detectados.")
    rel.append("- `04_TRIAGEM/relatorio_pre_triagem.md` -- este relatorio.")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(rel) + "\n")

    print(f"Total: {total}")
    for classe, n in sorted(contagem.items(), key=lambda kv: -kv[1]):
        print(f"{classe}: {n} ({100*n/total:.1f}%)")


if __name__ == "__main__":
    main()
