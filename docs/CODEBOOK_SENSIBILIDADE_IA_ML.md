# Codebook — Auditoria de classe IA/ML (busca de sensibilidade, 2026-07-12)

## 1. Natureza deste documento

Este codebook formaliza, antes de qualquer auditoria em massa, as regras de classificação
temática de IA/ML aplicadas aos 4.889 registros únicos novos identificados em
`03_PROCESSADOS/sensibilidade_novos_unicos.csv` (Etapa 5) e à reavaliação dos 7 registros já
existentes no corpus (Etapa 6). Segue o mesmo padrão editorial de
`docs/CODEBOOK_CATEGORIAS_ETAPA_8.md`: definição, regra de inclusão, regra de exclusão, exemplo
positivo, exemplo negativo e regra de desempate por categoria.

**Achado que motiva este documento**: a busca original do núcleo (`01_PROTOCOLO/strings_nativas_por_base.md`)
capturou IA/ML apenas incidentalmente. O dicionário de perguntas de pesquisa vigente
(`07_SINTESE_TEMATICA/dicionario_rq_etapa15.csv`, RQ0–RQ5) não tem nenhuma RQ dedicada a IA/ML —
a RQ3 existente (`metodo_decisao`) cobre exclusivamente métodos multicritério (MCDM/AHP/TOPSIS
etc.), tema distinto. Este codebook cria a **RQ6** dedicada a IA/ML, sem alterar o escopo da RQ3.

**Método de auditoria**: classificação por leitura sistemática de título, resumo e palavras-chave
contra as regras fechadas abaixo — não constitui leitura de texto completo. Quando o resumo está
ausente (`resumo_presente=nao`, sistemático na fatia Crossref — ver
`03_PROCESSADOS/relatorio_normalizacao_sensibilidade_ia.md`), a classificação usa apenas
título/palavras-chave/periódico disponíveis, e o campo `nivel_confianca` é rebaixado por
definição (nunca "alto" sem resumo, salvo termo de IA/ML inequívoco no próprio título).

---

## 2. Dois níveis de termos (RQ6 — IA/ML)

### 2.1 Termos que, isoladamente, indicam técnica de IA/ML (nível "confirma")

| Termo/família | Observação |
|---|---|
| machine learning, aprendizado de máquina | — |
| deep learning | apenas em contexto de modelo computacional (ver regra de desambiguação, Seção 4) |
| neural network, artificial neural network, ANN | — |
| convolutional neural network, CNN | — |
| recurrent neural network, RNN, LSTM, GRU | — |
| random forest | — |
| gradient boosting, XGBoost, LightGBM, CatBoost | — |
| support vector machine, SVM | — |
| reinforcement learning | — |
| computer vision | quando aplicado a processamento de imagem por modelo, não a "visão" no sentido figurado |
| natural language processing, NLP | — |
| k-means, k-nearest neighbors, kNN, clustering (quando algoritmo de ML explícito) | — |
| Bayesian network / rede bayesiana (quando estimada por aprendizado, não regra fixa) | ver regra de desambiguação para "Bayesian" genérico |
| transformer (arquitetura de rede neural) | ver regra de desambiguação — não confundir com transformador elétrico |
| generative adversarial network, GAN | — |
| autoencoder | — |
| SHAP, LIME (técnicas de interpretabilidade de modelos de ML) | confirmam IA/ML apenas quando aplicadas a um modelo de ML já confirmado no mesmo estudo |
| large language model, LLM, GPT, BERT, ChatGPT, foundation model | modelos de linguagem baseados em transformer |
| generative AI, generative artificial intelligence, diffusion model | IA generativa (texto, imagem) |

### 2.2 Termos ambíguos — exigem contexto, nunca confirmam IA/ML isoladamente

| Termo/família | Por que é ambíguo |
|---|---|
| predictive maintenance / manutenção preditiva | pode ser regra estatística simples ou monitoramento baseado em condição (CBM) sem ML |
| digital twin | pode ser modelo geométrico/BIM sincronizado, sem nenhum componente de aprendizado |
| BIM | modelagem de informação da construção, não é IA por si |
| IoT / sensores / smart building / smart sensors | captação de dados; não implica algoritmo de IA/ML no processamento |
| decision tree / árvore de decisão | pode ser árvore lógica manual (fluxograma de decisão) ou algoritmo de ML treinado — só confirma se há evidência de treinamento/dados |
| fault detection, fault diagnosis, anomaly detection | podem usar regras fixas (thresholds), estatística clássica, ou ML — só confirma com técnica nomeada |
| remaining useful life (RUL) | pode ser calculado por modelo físico/estatístico, não necessariamente ML |
| ontologia, ontology | representação de conhecimento simbólica, não é ML |
| simulação, simulation | pode ser simulação física/determinística, não é ML |
| otimização, optimization | pode ser programação matemática clássica (programação linear, heurísticas não-ML) |
| fuzzy, fuzzy logic | lógica difusa é técnica de IA simbólica clássica — só confirma nível "aplicação de IA" se o restante do resumo não indicar apenas regra fixa; nunca confirma "machine learning" especificamente |
| big data, data-driven | volume/abordagem orientada a dados, não implica algoritmo de aprendizado |
| algorithm / algoritmo (genérico) | qualquer procedimento computacional é um "algoritmo" — não confirma IA/ML sem qualificação |
| Bayesian (genérico, ex. "Bayesian approach", "Bayesian model") | inferência bayesiana clássica é estatística, não necessariamente ML — só confirma com "Bayesian network", "Bayesian deep learning" ou modelo explicitamente treinado |

---

## 3. As 6 classes de auditoria

| Classe | Definição | Regra de desempate |
|---|---|---|
| `IA_ML_APLICACAO_CONFIRMADA` | Pelo menos um termo do nível "confirma" (Seção 2.1) aplicado como técnica computacional efetivamente usada no estudo (treinada, aplicada, avaliada — não apenas citada como tendência). | Se o termo aparece só na lista de "trabalhos futuros" ou na introdução como tendência de mercado, não conta — ver `IA_ML_MENCAO_GENERICA`. |
| `IA_ML_MENCAO_GENERICA` | Termo de IA/ML citado (ex. "a IA está transformando a manutenção predial"), mas sem aplicação própria do estudo — é revisão/discussão sobre a tendência, não implementação. | — |
| `TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA` | Apenas termos ambíguos (Seção 2.2), sem termo de nível "confirma" e sem detalhe suficiente para saber se há algoritmo de aprendizado por trás. | Nunca promovido a `IA_ML_APLICACAO_CONFIRMADA` só por acúmulo de termos ambíguos. |
| `MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA` | Estudo é claramente sobre manutenção preditiva/CBM, mas o resumo não evidencia nenhuma técnica de IA/ML (regra fixa, threshold, estatística descritiva). | Subcaso de `TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA`, usado quando o foco central do estudo é manutenção preditiva especificamente (não genérico). |
| `FALSO_POSITIVO` | Termo de IA/ML (ou termo ambíguo) capturado por correspondência lexical, mas fora de contexto de IA (ex. "transformer" = equipamento elétrico; "tree" em "decision tree" referindo-se a árvore/vegetação; item editorial sem conteúdo técnico — Frontmatter/Contents/References). | — |
| `INFORMACAO_INSUFICIENTE` | Resumo ausente ou insuficiente, título/palavras-chave não permitem decidir entre as classes acima. Nunca inferir a partir de silêncio — declarar explicitamente "Informação insuficiente para verificar." | Aplica-se sistematicamente a boa parte da fatia Crossref sem resumo. |

---

## 4. Regras de desambiguação obrigatórias

- **"transformer"**: confirma IA/ML apenas com co-ocorrência de termos como "transformer model", "transformer architecture", "attention mechanism", "self-attention", "BERT", "GPT", "vision transformer". Sem esses sinais, e com co-ocorrência de "substation", "oil", "winding", "electrical failure", "power transformer", classificar como `FALSO_POSITIVO` (equipamento elétrico, não arquitetura de rede neural).
- **"decision tree"**: confirma IA/ML apenas se o resumo indica que a árvore foi **treinada/induzida a partir de dados** (ex. "decision tree classifier", "trained on a dataset", "CART algorithm"). Se é apenas um fluxograma lógico de apoio à decisão gerencial, classificar como `TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA` (é método de decisão, possivelmente já coberto pela RQ3 existente, não IA/ML).
- **"deep learning" fora de contexto técnico**: se aparece em contexto pedagógico/curricular (ex. "deep learning about sustainability", "aprendizagem profunda sobre X" no sentido de aprendizagem humana), classificar `FALSO_POSITIVO`.
- **Manutenção preditiva, BIM, digital twin, IoT, data-driven**: **nunca**, isoladamente, geram `IA_ML_APLICACAO_CONFIRMADA` — mesmo que sejam o foco central do estudo. Exigem termo de nível "confirma" (Seção 2.1) explícito para subir de classe.
- **Itens editoriais** (Frontmatter, Contents/Table of Contents, Copyright, References-only, Index): classificar `FALSO_POSITIVO`, `decisao_triagem=excluido`, independentemente de termos capturados no título — não são estudos.

---

## 5. Campos de auditoria por registro (domínio fechado)

| Campo | Domínio |
|---|---|
| `termo_encontrado` | termo(s) literal(is) do texto que motivaram a classificação, separados por `;` |
| `campo_encontrado` | `titulo`, `resumo`, `palavras_chave`, ou combinação separada por `;` |
| `evidencia_curta` | trecho literal ≤ 200 caracteres |
| `classe_ia_ml` | uma das 6 classes da Seção 3 |
| `tecnica_ia_ml` | técnica nomeada (ex. `random_forest`, `LSTM`, `CNN`) ou `nao_aplicavel` |
| `tipo_aplicacao` | `predicao`, `classificacao`, `deteccao_anomalia`, `otimizacao`, `visao_computacional`, `processamento_linguagem`, `outro`, `nao_aplicavel` |
| `relacao_manutencao_predial` | `sim`/`nao`/`indireta` |
| `relacao_sustentabilidade` | `sim`/`nao`/`indireta` |
| `relacao_apoio_decisao` | `sim`/`nao` |
| `contexto_publico_universitario` | `sim`/`nao`/`nao_identificado` |
| `decisao_triagem` | `nucleo`, `secundario`, `mapeamento`, `excluido` (Etapa 6) |
| `justificativa` | texto livre curto, sem atribuir a análise a "IA" — descreve o processo ("classificação por correspondência de termos do dicionário RQ6 aplicada ao título/resumo") |
| `nivel_confianca` | `alto`, `medio`, `baixo` — nunca `alto` sem resumo, salvo termo de nível "confirma" no próprio título |

---

## 6. Limite metodológico declarado

Nenhuma classificação desta auditoria implica leitura de texto completo. "Informação
insuficiente para verificar" é a resposta correta e esperada para uma fração relevante dos
registros sem resumo (majoritariamente Crossref). Presença documental de termos de IA/ML não
equivale a maturidade institucional de adoção — distinção explicitada no artigo (Etapa 8, seção
de discussão/limitações).
