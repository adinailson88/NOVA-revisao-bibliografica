# MANIFESTO — Busca de sensibilidade IA/ML (2026-07-12)

Arquivos brutos fornecidos pelo usuário, coletados manualmente fora deste ambiente. Nenhuma nova busca foi executada aqui; este manifesto apenas organiza, recontagem e documenta os arquivos recebidos, preservando seu conteúdo original.

## Arquivos

| Caminho | Base | Registros (recontados) | Tamanho (bytes) | SHA-256 |
|---|---|---|---|---|
| `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/scopus/SCOPUS_A5_2009-2026.csv` | Scopus | 3169 | 34242441 | `3ca70a59bb790a4cc3600139522a63a7ad259e66cc752f44351c252d0bee206b` |
| `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/wos/WOS_NUCLEO_05_20260712_part01.ris` | Web of Science (parte 1) | 1000 | 3007919 | `357a6e211581577585cfba4a5b0a1fe90b4d11d587bbd8540e4eb9c18216f1f1` |
| `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/wos/WOS_NUCLEO_05_20260712_part02.ris` | Web of Science (parte 2) | 559 | 1733042 | `2d70eb12cdb67e6cbad24e1b2200411d351cef65f9487ef9f60ebb1d7414cadb` |
| `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/crossref/crossref_ia_todos_resultados.csv` | Crossref | 2000 | 1488342 | `1b994fee2ae21487f4230882a4eee389a139102c5041a5d30641646a80fabfb4` |

## Contagens agregadas

- Scopus: **3169** registros (esperado: 3169).
- Web of Science: parte 1 = **1000** (esperado 1000), parte 2 = **559** (esperado 559), total = **1559**.
- Crossref: **2000** linhas (esperado 2000, 10 consultas × 200).
- Overlap de accession number (UT/campo `AN`) entre parte 1 e parte 2 do WoS: **0** registro(s) em comum.

## Período coberto (extraído dos dados)

| Base | Ano mínimo | Ano máximo |
|---|---|---|
| Scopus | 2010 | 2026 |
| Web of Science | 2010 | 2026 |
| Crossref | 2010 | 2026 |

## Campos disponíveis por arquivo

- **Scopus** (cabeçalho CSV, 45 campos): Authors, Author full names, Author(s) ID, Title, Year, Source title, Volume, Issue, Art. No., Page start, Page end, Cited by, DOI, Link, Affiliations, Authors with affiliations, Abstract, Author Keywords, Index Keywords, Molecular Sequence Numbers, Chemicals/CAS, Tradenames, Manufacturers, Funding Details, Funding Texts, References, Correspondence Address, Editors, Publisher, Sponsors, Conference name, Conference date, Conference location, Conference code, ISSN, ISBN, CODEN, PubMed ID, Language of Original Document, Abbreviated Source Title, Document Type, Publication Stage, Open Access, Source, EID

- **WoS parte 1** (tags RIS presentes, 32): A1, AB, AD, AN, AU, C3, C6, C7, CP, DA, DO, ED, EP, FU, FX, IS, J9, JI, KW, LA, N1, PA, PI, PU, PY, SN, SP, T2, TI, TY, VL, WE

- **WoS parte 2** (tags RIS presentes, 32): A1, AB, AD, AN, AU, C3, C6, C7, CP, DA, DO, ED, EP, FU, FX, IS, J9, JI, KW, LA, N1, PA, PI, PU, PY, SN, SP, T2, TI, TY, VL, WE

- **Crossref** (cabeçalho CSV, 15 campos): doi, title, abstract, author, published, container_title, type, subject, is_referenced_by_count, url, publisher, language, database, string_id, query_bibliographic


## Data de inclusão neste repositório

2026-07-12 (data informada pelo nome dos arquivos e pela sessão de incorporação).

