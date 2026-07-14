# Log da busca de sensibilidade — Inteligência Artificial / Machine Learning

Data: 2026-07-12
Motivação: a busca original (strings A1–A4 do núcleo, `01_PROTOCOLO/strings_nativas_por_base.md`)
capturou IA/ML apenas incidentalmente — não havia dicionário de termos dedicado a IA/ML em
nenhuma pergunta de pesquisa (RQ0–RQ5) até esta rodada. Esta busca complementar de sensibilidade
foi executada manualmente pelo usuário, fora deste ambiente, nas três mesmas bases do núcleo
original (Scopus, Web of Science, Crossref), com foco explícito em termos de IA/ML aplicados a
manutenção/gestão predial. Nenhuma nova busca foi executada neste ambiente — apenas incorporação,
deduplicação e auditoria temática do que já foi coletado.

## Arquivos recebidos e organizados

- `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/scopus/SCOPUS_A5_2009-2026.csv`
- `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/wos/WOS_NUCLEO_05_20260712_part01.ris`
- `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/wos/WOS_NUCLEO_05_20260712_part02.ris`
- `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/crossref/crossref_ia_todos_resultados.csv`

Contagens recontadas programaticamente (ver `02_DADOS_BRUTOS/busca_sensibilidade_ia_20260712/MANIFESTO.md`,
gerado por `scripts/python/manifesto_busca_sensibilidade.py`, com hash SHA-256 de cada arquivo):

| Arquivo | Base | Registros |
|---|---|---|
| SCOPUS_A5_2009-2026.csv | Scopus | 3.169 |
| WOS_NUCLEO_05_20260712_part01.ris | Web of Science | 1.000 |
| WOS_NUCLEO_05_20260712_part02.ris | Web of Science | 559 |
| crossref_ia_todos_resultados.csv | Crossref | 2.000 (10 consultas × 200, `string_id` = `crossref_ia_01`..`crossref_ia_10`) |

Total bruto desta rodada: 3.169 + 1.559 + 2.000 = **6.728 registros**, antes de qualquer deduplicação.

## Mapeamento arquivo → string_id

Seguindo a convenção do núcleo original (`<base>_nucleo_a{n}_<tema>`), esta rodada de sensibilidade
usa o próximo índice disponível (`a5`) para Scopus e WoS:

| Arquivo | string_id | Registros |
|---|---|---|
| SCOPUS_A5_2009-2026.csv | `scopus_nucleo_a5_sensibilidade_ia_ml` | 3.169 |
| WOS_NUCLEO_05_20260712_part01.ris + part02.ris | `wos_nucleo_a5_sensibilidade_ia_ml` | 1.559 (1.000 + 559, sem overlap de accession number entre as partes — confirmado no manifesto) |
| crossref_ia_todos_resultados.csv | `crossref_ia_01` a `crossref_ia_10` (já vem identificado por linha no próprio CSV) | 2.000 |

## Verificação de overlap WoS part01/part02

O manifesto confirmou **zero** accession numbers (`AN`) em comum entre `part01.ris` e `part02.ris`
— as duas partes não se sobrepõem, o total de 1.559 registros WoS é aditivo e correto.

## Decisão metodológica

Diferente do núcleo original, esta busca de sensibilidade é tratada como um conjunto à parte
(`busca_sensibilidade_ia_20260712`), incorporado ao corpus consolidado apenas após deduplicação
completa contra `corpus_consolidado.csv` (ver `03_PROCESSADOS/relatorio_deduplicacao_sensibilidade.md`)
e auditoria temática dedicada de IA/ML (ver `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` e
`03_PROCESSADOS/sensibilidade_auditoria_classe_ia_ml.csv`).

## Verificação documental das consultas — atualização em 13/07/2026

As strings completas, os campos, o período, a data, os filtros e os parâmetros operacionais da
rodada foram consolidados em
`01_PROTOCOLO/strings_busca_sensibilidade_ia_ml_20260712.md`.

### Scopus

- Campo: `TITLE-ABS-KEY`.
- Período: 2010–2026.
- Data da execução: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total: 3.169 ocorrências brutas.
- String nativa integral: documentada no arquivo de protocolo indicado acima.

### Web of Science

- Base consultada: Web of Science — All Databases.
- Campo: Topic (`TS`).
- Período: 2010–2026.
- Data da execução: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total: 1.559 ocorrências brutas.
- String nativa integral: documentada no arquivo de protocolo indicado acima.

A busca foi executada na opção All Databases. Os registros exportados apresentam indexação na
Web of Science Core Collection; essa indexação não altera a identificação da base efetivamente
consultada.

### Crossref

O arquivo bruto preserva `string_id` e `query_bibliographic` em cada linha. As dez consultas,
com 200 registros por consulta, foram verificadas:

| string_id | query.bibliographic |
|---|---|
| `crossref_ia_01` | building maintenance artificial intelligence machine learning |
| `crossref_ia_02` | facility management deep learning neural networks |
| `crossref_ia_03` | building condition assessment random forest support vector machine decision tree |
| `crossref_ia_04` | predictive maintenance building facilities anomaly detection fault diagnosis |
| `crossref_ia_05` | building operation energy reinforcement learning LSTM transformer |
| `crossref_ia_06` | building inspection computer vision image recognition convolutional neural network |
| `crossref_ia_07` | building maintenance natural language processing work orders |
| `crossref_ia_08` | university building maintenance neural network cost prediction |
| `crossref_ia_09` | facility management generative AI large language model |
| `crossref_ia_10` | digital twin building maintenance machine learning |

Parâmetros comuns: endpoint `https://api.crossref.org/works`, parâmetro
`query.bibliographic`, filtro `from-pub-date:2010-01-01,until-pub-date:2026-12-31`, `rows=200` e
ordenação por relevância. As 2.000 ocorrências correspondem a 1.993 registros após deduplicação
interna.

## Situação documental

As lacunas anteriormente registradas para as expressões nativas da Scopus e da Web of Science
foram encerradas com o fornecimento das strings efetivamente utilizadas pelo pesquisador. Não foi
necessário refazer as buscas nem reconstruir consultas por inferência.

A soma de 12.118 ocorrências da busca principal e 6.728 da busca de sensibilidade resulta em
18.846 ocorrências operacionais. Esse valor não representa corpus bruto homogêneo, pois as
rodadas possuem finalidades e estratégias diferentes.