# RELATÓRIO DE DEDUPLICAÇÃO — Busca de sensibilidade IA/ML

Gerado por `scripts/python/deduplicar_sensibilidade_ia.py`. Cascata: DOI normalizado → título exato → título aproximado (blocking por palavra rara, limiar 0.9, confirmado por ano±1/autor/periódico) → contra `corpus_consolidado.csv`.

## Funil completo

| Etapa | N |
|---|---|
| Bruto normalizado (entrada) | 6728 |
| Após dedup exata intra+entre-bases (DOI/título exato) | 5254 |
| Após dedup por título aproximado dentro da sensibilidade | 5248 |
| Classificados JA_EXISTIA_NO_CORPUS (automático) | 357 |
| Classificados NOVO_POR_DOI (automático) | 4678 |
| Classificados NOVO_POR_TITULO (automático) | 201 |
| Classificados SEM_IDENTIFICADOR_SUFICIENTE | 0 |
| Classificados DUPLICATA_PROVAVEL_REQUER_REVISAO (antes da revisão manual) | 12 |
| **Novos únicos que seguem para auditoria de classe IA/ML (após revisão manual, ver seção 3)** | **4889** |
| **Já existia no corpus, total final (após revisão manual)** | **359** |

## Teste de sanidade — duplicatas internas conhecidas do Crossref

Duplicatas por DOI dentro do próprio Crossref (das 2000 linhas): **7** (esperado: 7, conforme já documentado pelo usuário nos metadados do arquivo fornecido).

## 3. Revisão manual pontual dos 12 casos de dúvida

Os 12 pares sinalizados por `sensibilidade_duplicatas_requerem_revisao.csv` (título exato ou
aproximado casado contra o corpus, mas com DOI divergente ou sem confirmação por ano/autor/
periódico) foram revisados individualmente:

- **2 confirmados como duplicata real** (mesma obra em DOI de pré-print e DOI de versão
  publicada): `SENS_SCOPUS_00312` (pré-print SSRN) = `REG_08530` (publicado, kscej); e
  `SENS_CROSSREF_01428` (pré-print MDPI Preprints) = `REG_06176` (publicado, MDPI
  Sustainability). Ambos reclassificados para `JA_EXISTIA_NO_CORPUS` e movidos para
  `sensibilidade_ja_existia_corpus.csv`.
- **10 confirmados como registros distintos** (falso positivo do casamento por título
  genérico — DOIs diferentes, obras diferentes): a conferência CSCE em edições de 2019 e 2021
  (`SENS_SCOPUS_02531` vs `REG_07446`), e 9 itens editoriais não-substantivos (Frontmatter,
  Contents, Copyright, References, Introduction) de livros/capítulos distintos que
  compartilham título genérico com outro item do corpus. Promovidos para `NOVO_POR_DOI`/
  `NOVO_POR_TITULO` e incluídos em `sensibilidade_novos_unicos.csv` — a relevância temática
  desses itens editoriais (a maioria não é um estudo de fato, e sim material de capa/sumário/
  referências de um livro) é decidida na auditoria de classe IA/ML (Etapa 5) e na triagem
  (Etapa 6), não nesta etapa de deduplicação.

## Arquivos gerados

- `sensibilidade_dedup_classificacao.csv` — todos os registros únicos com classificação.
- `sensibilidade_ja_existia_corpus.csv` — subconjunto já presente no corpus original.
- `sensibilidade_novos_unicos.csv` — subconjunto que segue para auditoria de classe IA/ML (Etapa 5).
- `sensibilidade_duplicatas_requerem_revisao.csv` — pares ambíguos para revisão manual pontual.
