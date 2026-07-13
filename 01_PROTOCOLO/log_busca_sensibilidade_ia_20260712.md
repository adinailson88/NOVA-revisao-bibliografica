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


## Verificação documental das consultas — 13/07/2026

A estratégia foi consolidada em
`latex-artigo/fontes/tabela_estrategia_busca.csv`, mantendo separadas a busca principal e a
busca de sensibilidade.

### Scopus e Web of Science

Os arquivos recebidos preservam campo, data, período, identificador da rodada e totais
exportados, mas não contêm as strings nativas exatas usadas nas interfaces da Scopus e da Web of
Science. Portanto, a formulação exata dessas duas consultas não foi reconstruída por inferência
e foi registrada como:

> Informação insuficiente para verificar.

Essa limitação refere-se à expressão nativa, não às contagens: 3.169 registros na Scopus e
1.559 na Web of Science foram recontados diretamente nos arquivos brutos.

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

A soma de 12.118 ocorrências da busca principal e 6.728 da busca de sensibilidade resulta em
18.846 ocorrências operacionais. Esse valor não representa corpus bruto homogêneo, pois as
rodadas possuem finalidades e estratégias diferentes.
