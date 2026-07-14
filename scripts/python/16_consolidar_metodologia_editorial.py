from __future__ import annotations

import re
import subprocess
from pathlib import Path

BASE_COMMIT = "2bc86d2227874e572145964cc638d4854504a701"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"Bloco não localizado: {label}")
    return text.replace(old, new, 1)


def citation_keys(text: str) -> set[str]:
    pattern = re.compile(
        r"\\(?:paren|text|auto|foot|smart|super)?cite\*?"
        r"(?:\[[^\]]*\]){0,2}\{([^}]*)\}"
    )
    keys: set[str] = set()
    for group in pattern.findall(text):
        keys.update(key.strip() for key in group.split(",") if key.strip())
    return keys


def count_words(text: str) -> int:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]+\}", " ", text)
    text = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}$&_^~\\]", " ", text)
    return len(
        re.findall(
            r"[A-Za-zÀ-ÖØ-öø-ÿ0-9]+(?:[-'][A-Za-zÀ-ÖØ-öø-ÿ0-9]+)*",
            text,
        )
    )


def baseline(path: Path) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASE_COMMIT}:{path.as_posix()}"], text=True
    )


def main() -> None:
    methodology = Path("latex-artigo/sections/03_metodologia.tex")
    text = methodology.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "A organização do relato metodológico explicita pergunta, busca, seleção, extração e síntese, elementos de transparência e reprodutibilidade destacados por \\textcite{hu_revisao_sintese_2026}. A referência é empregada apenas como parâmetro de relato; não implica pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo ou metanálise, procedimentos não realizados.",
        "A organização do relato explicita pergunta, busca, seleção, extração e síntese, elementos de transparência e reprodutibilidade destacados por \\textcite{hu_revisao_sintese_2026}. O escopo declarado distingue esses procedimentos das etapas de pré-registro, dupla revisão, avaliação de risco de viés, elegibilidade integral em texto completo e metanálise.",
        "escopo do relato",
    )
    text = replace_once(
        text,
        "O caráter determinístico das rotinas reduz variações de execução: a mesma entrada, a mesma versão do código e os mesmos parâmetros produzem a mesma saída. Isso não elimina subjetividade. O manual de codificação, os limiares, as categorias, as expressões de busca e as decisões humanas sobre casos duvidosos incorporam escolhas analíticas. A automação torna essas escolhas mais auditáveis, mas não as converte em verdade objetiva.",
        "O caráter determinístico reduz variações de execução: a mesma entrada, versão do código e parâmetros produzem a mesma saída. A subjetividade permanece explicitada no manual de codificação, nos limiares, nas categorias, nas expressões de busca e nas decisões sobre casos duvidosos. A automação torna essas escolhas reproduzíveis e auditáveis.",
        "determinismo",
    )
    text = replace_once(
        text,
        "A literatura cinzenta não foi incluída em busca estruturada porque o desenho priorizou fontes com metadados bibliográficos interoperáveis e campos necessários à deduplicação e à análise. Essa decisão melhora a comparabilidade dos registros, mas pode reduzir a cobertura de relatórios técnicos, normas internas, planos de manutenção e experiências institucionais não indexadas. Portanto, a ausência desses documentos é uma limitação de cobertura e não deve ser apresentada como evidência de maior qualidade do corpus.",
        "O desenho priorizou fontes com metadados bibliográficos interoperáveis e campos necessários à deduplicação e à análise. Essa escolha favorece a comparabilidade e delimita a cobertura de relatórios técnicos, normas internas, planos de manutenção e experiências institucionais presentes na literatura cinzenta.",
        "literatura cinzenta",
    )

    dedup_start = text.index(
        "A Tabela~\\ref{tab:deduplicacao} apresenta os resultados e os controles conservadores da deduplicação."
    )
    dedup_end_marker = (
        "A coleta produziu 12.118 registros brutos: 9.433 recuperados pela API da Scopus, "
        "cinco registros existentes apenas no export manual da Scopus, 1.680 da Web of Science "
        "e 1.000 do Crossref. A deduplicação por DOI normalizado e título normalizado removeu "
        "2.576 ocorrências repetidas e resultou em 9.542 registros únicos, com preservação da proveniência."
    )
    dedup_end = text.index(dedup_end_marker, dedup_start) + len(dedup_end_marker)
    dedup_summary = (
        "A aplicação dessas regras consolidou 12.118 ocorrências em 9.542 registros únicos e "
        "removeu 2.576 repetições. Dos 1.808 grupos com duplicidade, 1.635 foram agrupados por DOI "
        "e 173 por título normalizado; 98 conflitos de identificadores permaneceram separados. "
        "O procedimento adotou igualdade exata e preservou distinções entre trabalhos de evento "
        "e artigos posteriores. A Tabela S1 do material suplementar apresenta os indicadores completos."
    )
    text = text[:dedup_start] + dedup_summary + text[dedup_end:]

    eligibility_start = text.index(
        "A avaliação de elegibilidade do núcleo temático original não incluiu leitura de texto completo dos 104 estudos."
    )
    eligibility_end_marker = (
        "os dez registros restantes do lote de sensibilidade permanecem caracterizados por título e resumo."
    )
    eligibility_end = text.index(eligibility_end_marker, eligibility_start) + len(
        eligibility_end_marker
    )
    eligibility_summary = (
        "A elegibilidade e a extração do núcleo temático apoiaram-se predominantemente em título, "
        "resumo, palavras-chave e campos estruturados. Entre 37 textos completos consultados em "
        "tarefas posteriores, 19 acrescentaram evidências específicas citadas individualmente. "
        "No lote de sensibilidade, sete dos 17 textos estavam disponíveis integralmente e cinco "
        "ampliaram resultados quantitativos, desenho de validação ou limitações; os demais "
        "permaneceram caracterizados pela documentação bibliográfica disponível."
    )
    text = text[:eligibility_start] + eligibility_summary + text[eligibility_end:]
    methodology.write_text(text, encoding="utf-8")

    matrix = Path("latex-artigo/sections/08_matriz.tex")
    matrix_text = matrix.read_text(encoding="utf-8").replace(
        "Em resposta à RQ0, a matriz converte dimensões e critérios recorrentes em indicadores candidatos e etapas verificáveis.",
        "A matriz converte dimensões e critérios recorrentes em indicadores candidatos e etapas verificáveis, sintetizando a resposta à RQ0.",
    )
    matrix.write_text(matrix_text, encoding="utf-8")

    candidates: list[str] = []
    for root in (
        Path("latex-artigo/fontes"),
        Path("07_SINTESE_TEMATICA"),
        Path("referencias"),
    ):
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and any(
                token in path.name.lower()
                for token in ("sensibilidade", "rq6", "17_reg", "matriz")
            ):
                candidates.append(path.as_posix())
    candidates = sorted(set(candidates))

    supplement = Path("latex-artigo/suplemento")
    supplement.mkdir(parents=True, exist_ok=True)
    items = "\n".join(f"\\item \\nolinkurl{{{path}}}" for path in candidates[:20])
    supplement_text = f"""\\section*{{Material suplementar}}

\\subsection*{{Tabela S1 --- Resultados e controles da deduplicação}}

\\begin{{table}}[htbp]
\\centering
\\small
\\begin{{tabularx}}{{\\textwidth}}{{Y >{{\\raggedleft\\arraybackslash}}p{{2.3cm}} >{{\\RaggedRight\\arraybackslash}}p{{5.7cm}}}}
\\toprule
Indicador & Total & Interpretação \\\\
\\midrule
Registros brutos normalizados & 12.118 & Uma linha por ocorrência recuperada antes da deduplicação. \\\\
Registros únicos & 9.542 & Uma linha por grupo consolidado. \\\\
Ocorrências removidas & 2.576 & Diferença entre registros brutos e únicos. \\\\
Grupos com duplicidade & 1.808 & 1.635 agrupados por DOI e 173 apenas por título normalizado. \\\\
Registros únicos com DOI & 8.264 & DOI presente após consolidação. \\\\
Registros únicos sem DOI & 1.278 & Controle por título e identificadores. \\\\
Conflitos preservados & 98 & 51 por DOI divergente e 47 por identificador próprio divergente. \\\\
\\bottomrule
\\end{{tabularx}}
\\fonteautor
\\end{{table}}

\\subsection*{{Tabela S2 --- Matriz comparativa dos 17 registros da busca de sensibilidade}}

A matriz comparativa permanece preservada nos produtos auditáveis do repositório. Arquivos relacionados:

\\begin{{itemize}}
{items}
\\end{{itemize}}
"""
    (supplement / "material_suplementar.tex").write_text(
        supplement_text, encoding="utf-8"
    )

    section_files = sorted(Path("latex-artigo/sections").glob("*.tex"))
    before = "\n".join(baseline(path) for path in section_files)
    after = "\n".join(path.read_text(encoding="utf-8") for path in section_files)
    before_words = count_words(before)
    after_words = count_words(after)
    reduction = 100 * (before_words - after_words) / before_words
    removed = sorted(citation_keys(before) - citation_keys(after))
    added = sorted(citation_keys(after) - citation_keys(before))
    if removed:
        raise RuntimeError("Referências removidas: " + ", ".join(removed))

    expressions = ("Em resposta à RQ", "não constitui", "não equivale")
    counts = {expression: (before.count(expression), after.count(expression)) for expression in expressions}
    report = Path("docs/REVISAO_EDITORIAL_ENXUTA_2026-07-14.md")
    report.write_text(
        "# Revisão editorial enxuta — 14/07/2026\n\n"
        f"- Palavras nas seções antes: {before_words}\n"
        f"- Palavras nas seções depois: {after_words}\n"
        f"- Redução: {reduction:.1f}%\n"
        f"- Chaves bibliográficas removidas: {len(removed)}\n"
        f"- Chaves bibliográficas acrescentadas: {len(added)}\n\n"
        "## Marcas repetitivas\n\n"
        + "\n".join(
            f"- `{expression}`: {old} → {new}"
            for expression, (old, new) in counts.items()
        )
        + "\n\n## Arquivos suplementares relacionados à sensibilidade\n\n"
        + ("\n".join(f"- `{path}`" for path in candidates) if candidates else "- Nenhum candidato localizado automaticamente.")
        + "\n\n## Regra de referências\n\nTodas as chaves bibliográficas presentes antes da revisão permanecem citadas após a consolidação.\n",
        encoding="utf-8",
    )
    print(report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
