# Referências do artigo — pasta auditável

Esta pasta reúne, em formatos abertos e legíveis, todas as referências utilizadas no
artigo (`latex-artigo/main.tex`), para permitir conferência independente sem precisar
abrir os fontes em LaTeX.

## Arquivos

| Arquivo | Conteúdo | Registros |
| --- | --- | --- |
| `referencias_citadas_artigo.bib` | Cópia exata de `latex-artigo/references.bib`, a fonte de verdade usada pela compilação do artigo (biblatex). | 35 |
| `referencias_citadas_artigo.csv` / `.xlsx` | O mesmo `.bib` convertido em planilha (chave, autores, ano, título, fonte, volume, número, páginas, DOI, link). | 35 |
| `nucleo_final_104_registros.csv` / `.xlsx` | Base completa do núcleo temático que fundamentou a síntese do artigo, com metadados de auditoria (dimensões, critérios, métodos, RQs confirmadas, nível de confiança, evidência do resumo). Cópia de `07_SINTESE_TEMATICA/matriz_base_nucleo_final_104.csv`. | 104 |

## Como as duas listas se relacionam

- As **104** entradas do núcleo final são o corpus que sustenta a síntese temática e a
  bibliometria do artigo (ver `latex-artigo/sections/03_metodologia.tex` para o funil de
  seleção completo, de 12.118 registros brutos até este núcleo).
- As **35** entradas efetivamente citadas no texto (`\parencite`/`\textcite`) são um
  subconjunto de uso direto: parte vem do núcleo de 104 (evidências específicas e
  leituras integrais), e parte é literatura de apoio metodológico que não pertence ao
  corpus bibliométrico (normas técnicas, guias de revisão integrativa/bibliometria,
  artigos sobre deduplicação, e a documentação da API do Crossref).
- Toda citação do artigo tem par obrigatório no `.bib` e vice-versa — verificado
  automaticamente a cada build pelo script
  [`scripts/python/verificar_artigo.py`](../scripts/python/verificar_artigo.py).

## Rastreabilidade adicional

Para o funil completo de coleta e seleção (Scopus, Web of Science, Crossref — 12.118
registros brutos → 9.542 únicos → 372 no estrato de núcleo forte → 104 no núcleo final),
consulte:

- `03_PROCESSADOS/` — corpus normalizado, consolidado e relatório de deduplicação.
- `04_TRIAGEM/` — matrizes de pré-triagem, auditoria amostral e resolução de dúvidas.
- `07_SINTESE_TEMATICA/` — matrizes completas de extração e síntese até o núcleo final.
