# Arquivos e evidências das referências

Esta pasta concentra os materiais bibliográficos que podem ser redistribuídos e auditados
no repositório, para conferência independente sem precisar abrir os fontes em LaTeX.

## Arquivos gerados automaticamente

| Arquivo | Conteúdo | Registros | Gerado por |
| --- | --- | --- | --- |
| `references.bib` | Cópia sincronizada do `.bib` usado pela compilação LaTeX (fonte de verdade). | 35 | [`12_gerar_lista_referencias.py`](../scripts/python/12_gerar_lista_referencias.py) |
| `lista_referencias.csv` / `.xlsx` | Chave, tipo, autoria, título, ano, periódico ou instituição, volume, número, páginas, DOI e link DOI de todas as referências citadas no texto. | 35 | [`12_gerar_lista_referencias.py`](../scripts/python/12_gerar_lista_referencias.py) + [`14_gerar_planilhas_auditoria_referencias.py`](../scripts/python/14_gerar_planilhas_auditoria_referencias.py) |
| `nucleo_final_104_registros.csv` / `.xlsx` | Base completa do núcleo temático que fundamentou a síntese do artigo, com metadados de auditoria (autores, periódico, dimensões, critérios, métodos, RQs confirmadas, nível de confiança, evidência do resumo). Cópia de [`07_SINTESE_TEMATICA/matriz_base_nucleo_final_104.csv`](../07_SINTESE_TEMATICA/matriz_base_nucleo_final_104.csv). | 104 | [`14_gerar_planilhas_auditoria_referencias.py`](../scripts/python/14_gerar_planilhas_auditoria_referencias.py) |

A geração de `lista_referencias.csv` falha se existir citação sem entrada BibTeX ou entrada
BibTeX não citada — toda citação do artigo tem par obrigatório no `.bib` e vice-versa.

## Como as duas listas se relacionam

- As **104** entradas do núcleo final são o corpus que sustenta a síntese temática e a
  bibliometria do artigo (ver [`latex-artigo/sections/03_metodologia.tex`](../latex-artigo/sections/03_metodologia.tex)
  para o funil de seleção completo, de 12.118 registros brutos até este núcleo).
- As **35** entradas de `lista_referencias.csv` são um subconjunto de uso direto no texto
  (`\parencite`/`\textcite`): parte vem do núcleo de 104 (evidências específicas e leituras
  integrais), e parte é literatura de apoio metodológico que não pertence ao corpus
  bibliométrico (normas técnicas, guias de revisão integrativa/bibliometria, artigos sobre
  deduplicação, e a documentação da API do Crossref).

## Evidências e dados de apoio versionados

- [Núcleo final de 104 registros (versão resumida, sem autores/periódico)](../latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv)
- [Corpus bibliométrico ampliado de 372 registros](../latex-artigo/fontes/corpus_bibliometrico_372.csv)
- [Relatório bibliométrico dos 372 registros](../docs/RELATORIO_BIBLIOMETRIA_372.md)
- [Relatório do primeiro lote de textos completos](../docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md)
- [Relatório do segundo lote de textos completos](../docs/RELATORIO_USO_TEXTO_COMPLETO_11_NOVOS_ESTUDOS.md)
- [Resumos detalhados e parafraseados do segundo lote](../docs/RESUMOS_DETALHADOS_11_NOVOS_ESTUDOS.txt)
- [Mapa do segundo lote de textos completos](../docs/MAPA_FULLTEXT_11_NOVOS_ESTUDOS.csv)

## Direitos autorais

Os PDFs originais de artigos comerciais ou obtidos por acesso institucional não são
redistribuídos. O repositório preserva metadados, DOI, codificações, resumos parafraseados
e relatórios de leitura, permitindo verificar a origem das afirmações sem publicar cópias
protegidas.
