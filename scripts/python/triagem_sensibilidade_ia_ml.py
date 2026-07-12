"""
Triagem em 4 categorias (nucleo / secundario / mapeamento / excluido) dos registros
auditados da busca de sensibilidade IA/ML.

Correcao de calibracao (2026-07-12): a primeira versao deste script usava apenas o campo
`relacao_manutencao_predial` (deteccao lexical simples de "maintenance") como criterio de
nucleo, o que gerou 2484 candidatos -- 24x o tamanho do nucleo original (104), incompativel
com a seletividade do pipeline original. Esta versao REAPROVEITA literalmente a logica de
Bloco A (objeto predial, forte/fraco+contexto) e Bloco B (sustentabilidade) de
`scripts/python/pre_triagem.py` (a mesma regra que classificou "relevante" no corpus
original: Bloco A E Bloco B obrigatorios, nunca um so), combinada com a classe de IA/ML
ja auditada (sensibilidade_auditoria_classe_ia_ml.csv), para produzir um nucleo desta busca
de sensibilidade comparavel em rigor ao nucleo original.

Mapeamento nucleo/secundario/mapeamento/excluido:
- nucleo: Bloco A + Bloco B (== "relevante" no criterio original) E classe_ia_ml =
  IA_ML_APLICACAO_CONFIRMADA.
- secundario: Bloco A + Bloco tecnologico, sem Bloco B (== "complementar" tecnologico no
  criterio original) E classe_ia_ml = IA_ML_APLICACAO_CONFIRMADA -- IA aplicada a
  energia/operacao/tecnologia predial, relacao indireta (nao explicita) com sustentabilidade.
- mapeamento: relevante ou complementar segundo o criterio original, mas classe_ia_ml NAO
  confirmada (mencao generica, tecnica compativel, manutencao preditiva sem IA comprovada) --
  ainda util ao mapeamento descritivo da corrente informacional/digital, sem contar como
  evidencia de IA. Tambem inclui "duvida" (so um dos blocos A/B) com sinal de IA/ML.
- excluido: "irrelevante" pelo criterio original (nem bloco A nem B, nem tecnologico, nem
  conceitual), OU falso positivo de IA/ML, OU sem_resumo sem sinal de titulo suficiente.

Saida: 04_TRIAGEM/sensibilidade_triagem_final.csv
"""

import csv
import os
import re
import sys
import unicodedata
from collections import Counter

csv.field_size_limit(min(sys.maxsize, 2**31 - 1))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROC_DIR = os.path.join(BASE_DIR, "03_PROCESSADOS")
TRIAGEM_DIR = os.path.join(BASE_DIR, "04_TRIAGEM")

IN_PATH = os.path.join(PROC_DIR, "sensibilidade_auditoria_classe_ia_ml.csv")
OUT_PATH = os.path.join(TRIAGEM_DIR, "sensibilidade_triagem_final.csv")
RELATORIO_PATH = os.path.join(TRIAGEM_DIR, "relatorio_triagem_sensibilidade.md")

# --- Mesmos blocos de scripts/python/pre_triagem.py (reaproveitados literalmente) -------
BLOCO_A_FORTE = [
    "building maintenance", "facility management", "facilities management",
    "facilities maintenance", "building asset management", "building operation",
    "building portfolio", "building renovation", "building refurbishment",
    "manutencao predial", "gestao predial", "manutencao de edificacoes",
    "mantenimiento de edificios",
]
BLOCO_A_FRACO = [
    "operation and maintenance", "maintenance management", "maintenance planning",
    "maintenance prioritization", "maintenance priority", "maintenance backlog",
    "maintenance strategy", "renewal prioritization", "deferred maintenance",
    "asset performance", "condition assessment", "condition-based maintenance",
    "condition based maintenance", "retrofit", "building stock management",
    "building modernization", "built asset management", "public asset management",
]
BLOCO_A_CONTEXTO = ["building", "buildings", "facility", "facilities", "campus", "edific", "predial"]
BLOCO_B_SUSTENTABILIDADE = [
    "sustainab", "sustentab", "green building", "life cycle", "life-cycle",
    "whole life cost", "life cycle cost", "service life", "sustainability assessment",
    "sustainability indicator", "environmental performance", "building performance",
    "environmental criteria", "social criteria", "sustainable development goal",
    " esg ", " sdg", "sostenibilidad", "climate neutral", "carbon neutral", "net zero",
    "net-zero energy", "greenhouse gas",
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
    return [t for t in termos if t.strip() in texto_norm]


def bloco_a_valido(texto_norm):
    fortes = termos_encontrados(texto_norm, BLOCO_A_FORTE)
    fracos = termos_encontrados(texto_norm, BLOCO_A_FRACO)
    contexto = termos_encontrados(texto_norm, BLOCO_A_CONTEXTO)
    if fortes:
        return fortes + (fracos if contexto else []), True
    if fracos and contexto:
        return fracos, True
    return fracos, False


def classificar_original(titulo, resumo, resumo_presente):
    titulo_norm = normalizar(titulo)
    resumo_norm = normalizar(resumo)
    termos_titulo_a, valido_titulo_a = bloco_a_valido(titulo_norm)
    sinal_titulo_b = termos_encontrados(titulo_norm, BLOCO_B_SUSTENTABILIDADE)

    if not resumo_presente:
        if valido_titulo_a and sinal_titulo_b:
            sinal = "sugere_relevante"
        elif valido_titulo_a or sinal_titulo_b:
            sinal = "sugere_parcial"
        else:
            sinal = "sem_sinal"
        return "sem_resumo", sinal

    texto_norm = titulo_norm + resumo_norm
    termos_a, bloco_a = bloco_a_valido(texto_norm)
    termos_b = termos_encontrados(texto_norm, BLOCO_B_SUSTENTABILIDADE)
    termos_tec = termos_encontrados(texto_norm, BLOCO_TECNOLOGICO)
    termos_conc = termos_encontrados(texto_norm, BLOCO_CONCEITUAL)
    bloco_b, bloco_tec, bloco_conc = bool(termos_b), bool(termos_tec), bool(termos_conc)

    if bloco_a and bloco_b:
        return "relevante", None
    if bloco_a and bloco_tec:
        return "complementar", None
    if bloco_conc:
        return "complementar", None
    if bloco_a or bloco_b:
        return "duvida", None
    return "irrelevante", None


def triar(row):
    classe_ia = row["classe_ia_ml"]
    classe_original, sinal = classificar_original(
        row.get("titulo", ""), row.get("resumo", ""), row.get("resumo_presente") == "sim"
    )
    confirmada = classe_ia == "IA_ML_APLICACAO_CONFIRMADA"

    if classe_ia == "FALSO_POSITIVO":
        return "excluido", f"Falso positivo lexical de IA/ML (critério original: {classe_original})."

    if classe_original == "relevante":
        if confirmada:
            return "nucleo", "Bloco A (objeto predial) + Bloco B (sustentabilidade) presentes, mesmo critério que classificou 'relevante' no corpus original, com IA/ML aplicada confirmada."
        return "mapeamento", f"Bloco A + Bloco B presentes (critério original 'relevante'), mas classe IA/ML = {classe_ia} (não confirmada) -- útil ao mapeamento descritivo, não conta como evidência de IA."

    if classe_original == "complementar":
        if confirmada:
            return "secundario", "Bloco A (objeto predial) + termo tecnológico/conceitual presentes (critério original 'complementar'), sem Bloco B explícito, com IA/ML aplicada confirmada -- relação indireta com sustentabilidade."
        return "mapeamento", f"Critério original 'complementar' (tecnológico/conceitual), classe IA/ML = {classe_ia} não confirmada."

    if classe_original == "duvida":
        if confirmada:
            return "mapeamento", "Apenas um dos blocos A/B presente (critério original 'dúvida'), IA/ML confirmada -- inclusão apenas no mapeamento, sem elegibilidade plena ao núcleo/secundário."
        return "excluido", "Apenas um dos blocos A/B presente e classe IA/ML não confirmada."

    if classe_original == "sem_resumo":
        if sinal == "sugere_relevante" and confirmada:
            return "mapeamento", "Sem resumo na fonte; título sugere Bloco A + Bloco B, e termo de IA/ML confirmado no título -- mapeamento apenas (confiança baixa sem resumo)."
        return "excluido", f"Sem resumo na fonte; sinal de título insuficiente ({sinal}) para justificar inclusão."

    return "excluido", "Critério original 'irrelevante' (nenhum bloco A/B/tecnológico/conceitual encontrado)."


def main():
    os.makedirs(TRIAGEM_DIR, exist_ok=True)
    with open(IN_PATH, encoding="utf-8-sig", newline="") as f:
        registros = list(csv.DictReader(f))

    for r in registros:
        decisao, justificativa = triar(r)
        r["decisao_triagem"] = decisao
        r["justificativa"] = r.get("justificativa", "") + " | Triagem (Bloco A/B + IA/ML): " + justificativa

    campos = list(registros[0].keys())
    with open(OUT_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(registros)

    contagem = Counter(r["decisao_triagem"] for r in registros)
    contagem_classe_decisao = Counter((r["classe_ia_ml"], r["decisao_triagem"]) for r in registros)

    linhas_rel = []
    linhas_rel.append("# RELATÓRIO DE TRIAGEM — Busca de sensibilidade IA/ML (v2 — calibrado)\n")
    linhas_rel.append(
        "Gerado por `scripts/python/triagem_sensibilidade_ia_ml.py`. **Correção de "
        "calibração**: a primeira versão usava apenas detecção lexical de \"maintenance\" "
        "e gerou 2484 candidatos a núcleo (24x o núcleo original de 104), incompatível com "
        "a seletividade do pipeline original. Esta versão reaproveita literalmente a lógica "
        "de Bloco A (objeto predial) + Bloco B (sustentabilidade) de "
        "`scripts/python/pre_triagem.py` — o mesmo critério que gerou a classe \"relevante\" "
        "no corpus original — combinada com a classe de IA/ML já auditada (Etapa 5).\n"
    )
    linhas_rel.append("## Distribuição final\n")
    linhas_rel.append("| Decisão | N | % |")
    linhas_rel.append("|---|---|---|")
    for d, n in contagem.most_common():
        linhas_rel.append(f"| {d} | {n} | {n/len(registros)*100:.1f}% |")
    linhas_rel.append(f"| **Total** | **{len(registros)}** | 100.0% |\n")

    linhas_rel.append("## Classe IA/ML × decisão de triagem\n")
    linhas_rel.append("| Classe IA/ML | Núcleo | Secundário | Mapeamento | Excluído |")
    linhas_rel.append("|---|---|---|---|---|")
    for classe in sorted({r["classe_ia_ml"] for r in registros}):
        linhas_rel.append(
            f"| {classe} | {contagem_classe_decisao.get((classe,'nucleo'),0)} | "
            f"{contagem_classe_decisao.get((classe,'secundario'),0)} | "
            f"{contagem_classe_decisao.get((classe,'mapeamento'),0)} | "
            f"{contagem_classe_decisao.get((classe,'excluido'),0)} |"
        )

    linhas_rel.append(
        f"\n## Comparação de escala com o núcleo original\n\nNúcleo original: 104 estudos "
        f"(de 9542 registros consolidados, ~1.1%). Núcleo desta busca de sensibilidade: "
        f"{contagem.get('nucleo', 0)} estudos (de {len(registros)} registros auditados, "
        f"{contagem.get('nucleo', 0)/len(registros)*100:.1f}%) — proporção agora da mesma "
        f"ordem de grandeza do critério original, por usar o mesmo filtro Bloco A + Bloco B.\n"
    )

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas_rel) + "\n")

    print(dict(contagem))
    print(f"Escrito: {OUT_PATH}")


if __name__ == "__main__":
    main()
