# RELATORIO DE PRE-TRIAGEM -- ETAPA_07

Gerado por `00_CONFIG/pre_triagem.py`, a partir de `03_PROCESSADOS/corpus_consolidado.csv` (9542 registros unicos da ETAPA_06, re-executada em 2026-07-09 com resumo da Scopus enriquecido manualmente -- 94% de cobertura de resumo, contra 20% na rodada de 2026-07-08). Classificacao por casamento de frases-chave (regras explicitas, sem LLM), reprodutivel executando o script novamente. Vocabulario do classificador ampliado em 2026-07-09 (5 termos novos no Bloco A, 5 no Bloco B) apos auditoria da amostra de 2026-07-08 ter confirmado falsos negativos por lacuna de vocabulario -- ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09.

## 1. Metodo

Cada registro e classificado em uma das 5 classes exigidas pelo prompt da etapa (`00_CONTROLE/ROTINAS/PROMPTS/ETAPA_07_PRE_TRIAGEM.md`): `relevante`, `irrelevante`, `duvida`, `sem_resumo`, `complementar`. Arvore de decisao:

1. Sem resumo disponivel -> `sem_resumo` (nao classificado por conteudo; sinal do titulo guardado apenas como informacao auxiliar, nunca como classe final -- roteiro secao 13: nao incluir/excluir por titulo isolado).
2. Bloco A (objeto predial) E Bloco B (sustentabilidade) presentes -> `relevante`.
3. Bloco A presente com termo tecnologico (BIM/digital twin/IoT/smart campus/predictive maintenance), sem Bloco B -> `complementar`.
4. Termo conceitual presente (built environment/urban metabolism/biophilic/etc.) -> `complementar`.
5. Apenas Bloco A OU apenas Bloco B (nao os dois) -> `duvida`.
6. Nenhum dos blocos A/B/tecnologico/conceitual -> `irrelevante`.

Regra explicita do prompt da etapa, respeitada nesta arvore: Bloco C (multi-criteria, MCDM, MCDA, TOPSIS, AHP, ANP, PROMETHEE, ELECTRE, VIKOR, DEMATEL, BWM) e Bloco D (public building, university building/campus, higher education, government building, school, hospital) **nunca** produzem `relevante` sozinhos -- ficam apenas como colunas informativas (`bloco_c_presente`, `bloco_d_presente`) para reforcar a classificacao na auditoria futura (ETAPA_08), nunca como criterio de inclusao.

## 2. Termos usados por bloco (reprodutibilidade)

Bloco A e dividido em termos fortes (contam sozinhos) e fracos (so contam se um token de contexto de edificacao tambem aparecer no mesmo titulo+resumo) -- ver secao 1 e o docstring de `00_CONFIG/pre_triagem.py` para o motivo dessa divisao.

- **Bloco A -- objeto predial, termos FORTES (contam sozinhos)**: building asset management, building maintenance, building operation, building portfolio, building refurbishment, building renovation, facilities maintenance, facilities management, facility management, gestao predial, mantenimiento de edificios, manutencao de edificacoes, manutencao predial
- **Bloco A -- objeto predial, termos FRACOS (exigem token de contexto)**: asset performance, building modernization, building stock management, built asset management, condition assessment, condition based maintenance, condition-based maintenance, deferred maintenance, maintenance backlog, maintenance management, maintenance planning, maintenance prioritization, maintenance priority, maintenance strategy, operation and maintenance, public asset management, renewal prioritization, retrofit
- **Bloco A -- tokens de contexto exigidos para termos fracos**: building, buildings, campus, edific, facilities, facility, predial
- **Bloco B -- sustentabilidade (gating)**: building performance, carbon neutral, climate neutral, environmental criteria, environmental performance, esg, green building, greenhouse gas, life cycle, life cycle cost, life-cycle, net zero, net-zero energy, sdg, service life, social criteria, sostenibilidad, sustainab, sustainability assessment, sustainability indicator, sustainable development goal, sustentab, whole life cost
- **Bloco C -- decisao/MCDM (so etiqueta, nunca inclui sozinho)**: ahp, anp, best-worst method, bwm, decision making, decision support, decision-making, dematel, electre, mcda, mcdm, multi criteria, multi-criteria, multicriteria, prioritiz, promethee, topsis, vikor
- **Bloco D -- contexto publico/universitario (so etiqueta, nunca inclui sozinho)**: campus, educational building, government building, higher education, hospital, public building, public sector building, school building, university building, university campus
- **Bloco tecnologico (complementar)**: bim, building information model, campus infrastructure, data driven, data-driven, digital twin, intelligent building, internet of things, iot, predictive maintenance, smart building, smart campus
- **Bloco conceitual (complementar)**: biophilic building, biophilic design, building as a living system, building metabolism, built environment, campus sustainability, ecosystem services, green campus, green infrastructure, living building, nature-based solutions, regenerative building, regenerative design, sustainable campus, urban metabolism

## 3. Resultado da classificacao

| Classe | N registros | % do total |
|---|---|---|
| relevante | 3482 | 36.5% |
| duvida | 4291 | 45.0% |
| complementar | 429 | 4.5% |
| irrelevante | 774 | 8.1% |
| sem_resumo | 566 | 5.9% |
| **Total** | **9542** | **100.0%** |

## 4. Distribuicao dos relevantes por combinacao de bases

| bases_origem | N registros relevantes |
|---|---|
| Scopus | 2802 |
| Scopus|WoS | 527 |
| WoS | 61 |
| Crossref|Scopus | 47 |
| Crossref | 26 |
| Crossref|Scopus|WoS | 17 |
| Crossref|WoS | 2 |

## 5. Reforco por Bloco C/D dentro dos relevantes (apenas informativo)

Dos 3482 registros classificados `relevante` (A+B), 645 (18.5%) tambem mencionam metodo de decisao/MCDM (Bloco C) e 414 (11.9%) tambem mencionam contexto publico/universitario (Bloco D). Nenhum dos dois percentuais influencia a classe -- sao apenas insumo para a auditoria da ETAPA_08 e para o preenchimento futuro do campo `metodo_decisao` da matriz de extracao.

## 6. Limites desta etapa

Classificacao por casamento de frases-chave e sujeita a falsos positivos/negativos (ex.: termos genericos como "maintenance" ou "campus" isolados nao gatilham bloco algum aqui -- so frases especificas contam, o que pode deixar de fora casos reais com fraseado atipico). Nao houve verificacao humana registro a registro nesta etapa; a amostra estratificada de auditoria (30 relevantes, 30 irrelevantes, 20 duvida, 20 sem_resumo, conforme roteiro secao 15 ETAPA 8) fica para a proxima etapa. `sem_resumo` (566 registros, 5.9% do total) e um bloco grande e esperado -- Crossref raramente traz abstract e parte do nucleo Scopus/WoS tambem nao tem resumo capturado (ver `03_PROCESSADOS/relatorio_deduplicacao.md`, secao 4). Esta pre-triagem nao decide inclusao/exclusao final do artigo -- e insumo para a auditoria (ETAPA_08) e definicao do nucleo analitico (ETAPA_09/roteiro).

Ambiguidade residual conhecida e nao resolvida: a palavra "facility"/"facilities" serve de token de contexto para validar termos fracos do Bloco A (ex. "operation and maintenance"), mas tambem aparece em textos sobre instalacoes que nao sao edificacoes (portos, estacoes de tratamento de agua, plantas industriais). Uma amostra manual encontrou casos assim classificados como `relevante` indevidamente (ex.: avaliacao de resiliencia de porto inteligente, reuso de agua). Resolver isso exigiria julgamento de conteudo alem de casamento de frases -- fora do escopo desta etapa (ETAPA 7: "nao usar LLM para criar achados"); fica como item explicito para a revisao humana da ETAPA_08.

## 7. Arquivos gerados

- `04_TRIAGEM/matriz_pre_triagem.csv` -- 1 linha por registro, com classe, justificativa e blocos detectados.
- `04_TRIAGEM/relatorio_pre_triagem.md` -- este relatorio.
