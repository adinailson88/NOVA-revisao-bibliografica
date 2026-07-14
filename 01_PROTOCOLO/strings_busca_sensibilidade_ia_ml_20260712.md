# Strings da busca complementar de inteligência artificial e aprendizado de máquina

## Registro da execução

- Data da execução: 12/07/2026.
- Período de publicação: 2010–2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total operacional recuperado: 6.728 ocorrências brutas.
- Finalidade: busca complementar de sensibilidade, mantida separada da busca principal.

## 1. Scopus

- Base consultada: Scopus.
- Campo pesquisado: título, resumo e palavras-chave (`TITLE-ABS-KEY`).
- Período: 2010–2026.
- Data da execução: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total recuperado: 3.169 ocorrências brutas.

```text
TITLE-ABS-KEY(
  (
    "building maintenance"
    OR "facilities maintenance"
    OR "building maintenance management"
    OR "facility maintenance"
    OR "building operation and maintenance"
    OR "building operations and maintenance"
    OR "facility management"
    OR "facilities management"
    OR "building asset management"
    OR "building condition assessment"
    OR "building inspection"
    OR (
      "predictive maintenance"
      AND (
        building*
        OR facilit*
        OR HVAC
        OR "building system*"
      )
    )
  )
  AND
  (
    "artificial intelligence"
    OR "AI-based"
    OR "AI-enabled"
    OR "AI-driven"
    OR "machine learning"
    OR "deep learning"
    OR "reinforcement learning"
    OR "supervised learning"
    OR "unsupervised learning"
    OR "transfer learning"
    OR "artificial neural network*"
    OR "neural network*"
    OR "convolutional neural network*"
    OR "recurrent neural network*"
    OR CNN
    OR RNN
    OR LSTM
    OR transformer*
    OR autoencoder*
    OR "random forest*"
    OR "support vector machine*"
    OR SVM
    OR "gradient boosting"
    OR XGBoost
    OR "decision tree*"
    OR "computer vision"
    OR "image recognition"
    OR "natural language processing"
    OR "large language model*"
    OR "generative AI"
    OR "anomaly detection"
    OR "fault detection"
    OR "fault diagnosis"
    OR "remaining useful life"
  )
)
AND PUBYEAR > 2009
AND PUBYEAR < 2027
```

## 2. Web of Science

- Base consultada: Web of Science — All Databases.
- Campo pesquisado: Topic (`TS`), abrangendo título, resumo, palavras-chave dos autores e Keywords Plus.
- Período: 2010–2026.
- Data da execução: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total recuperado: 1.559 ocorrências brutas.

A busca foi realizada na opção All Databases da plataforma Web of Science. Os registros exportados apresentam indexação na Web of Science Core Collection.

```text
TS=(
  (
    "building maintenance"
    OR "facilities maintenance"
    OR "building maintenance management"
    OR "facility maintenance"
    OR "building operation and maintenance"
    OR "building operations and maintenance"
    OR "facility management"
    OR "facilities management"
    OR "building asset management"
    OR "building condition assessment"
    OR "building inspection"
    OR (
      "predictive maintenance"
      AND (
        building*
        OR facilit*
        OR HVAC
        OR "building system*"
      )
    )
  )
  AND
  (
    "artificial intelligence"
    OR "AI-based"
    OR "AI-enabled"
    OR "AI-driven"
    OR "machine learning"
    OR "deep learning"
    OR "reinforcement learning"
    OR "supervised learning"
    OR "unsupervised learning"
    OR "transfer learning"
    OR "artificial neural network*"
    OR "neural network*"
    OR "convolutional neural network*"
    OR "recurrent neural network*"
    OR CNN
    OR RNN
    OR LSTM
    OR transformer*
    OR autoencoder*
    OR "random forest*"
    OR "support vector machine*"
    OR SVM
    OR "gradient boosting"
    OR XGBoost
    OR "decision tree*"
    OR "computer vision"
    OR "image recognition"
    OR "natural language processing"
    OR "large language model*"
    OR "generative AI"
    OR "anomaly detection"
    OR "fault detection"
    OR "fault diagnosis"
    OR "remaining useful life"
  )
)
AND PY=(2010-2026)
```

## 3. Crossref

- Base consultada: Crossref.
- Endpoint: `https://api.crossref.org/works`.
- Parâmetro de consulta: `query.bibliographic`.
- Período: 2010–2026.
- Data da execução: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Quantidade por consulta: 200 registros.
- Ordenação: relevância.
- Total recuperado: 2.000 ocorrências brutas.
- Total após deduplicação interna: 1.993 registros.

Consultas executadas:

1. `building maintenance artificial intelligence machine learning`
2. `facility management deep learning neural networks`
3. `building condition assessment random forest support vector machine decision tree`
4. `predictive maintenance building facilities anomaly detection fault diagnosis`
5. `building operation energy reinforcement learning LSTM transformer`
6. `building inspection computer vision image recognition convolutional neural network`
7. `building maintenance natural language processing work orders`
8. `university building maintenance neural network cost prediction`
9. `facility management generative AI large language model`
10. `digital twin building maintenance machine learning`

Modelo de requisição:

```text
https://api.crossref.org/works
  ?query.bibliographic={CONSULTA}
  &filter=from-pub-date:2010-01-01,until-pub-date:2026-12-31
  &rows=200
  &sort=relevance
```

A divisão em dez consultas complementares constitui adaptação operacional às características da API da Crossref e não reprodução literal da sintaxe booleana usada na Scopus e na Web of Science.

## Totais da rodada

| Base | Número de consultas | Ocorrências brutas |
|---|---:|---:|
| Scopus | 1 | 3.169 |
| Web of Science — All Databases | 1 | 1.559 |
| Crossref | 10 | 2.000 |
| **Total operacional** | **12** | **6.728** |

O total operacional não deve ser interpretado como corpus homogêneo. Os resultados das três fontes foram normalizados e deduplicados antes da seleção e da incorporação ao núcleo temático.