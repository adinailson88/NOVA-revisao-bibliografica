# REAVALIAÇÃO DOS 7 REGISTROS — RQ6 (IA/ML)

Reavaliação manual (leitura integral do resumo de cada um dos 7 registros já existentes no corpus, apontados para revisão) aplicando `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` — não automatizada, dado o volume pequeno (7 registros). Gerado/aplicado por `scripts/python/reavaliar_7_registros_ia_ml.py`.

| id_unico | Decisão anterior | Decisão revisada | Técnica IA/ML | Impacto no núcleo |
|---|---|---|---|---|
| REG_02383 | analise_secundaria | analise_central | back-propagation artificial neural network (BPN) | PROMOVIDO a análise central |
| REG_07814 | analise_secundaria | analise_central | back-propagation artificial neural network (BPN) | PROMOVIDO a análise central |
| REG_07815 | analise_secundaria | analise_central | back-propagation artificial neural network (BPN) | PROMOVIDO a análise central |
| REG_00362 | analise_secundaria | analise_secundaria | random forest classification | mantido em análise secundária |
| REG_05418 | analise_secundaria | analise_central | extreme learning machine (ELM) + simulated annealing | PROMOVIDO a análise central |
| REG_06151 | analise_secundaria | analise_secundaria | LightGBM, XGBoost, SHAP (XAI) | mantido em análise secundária |
| REG_06840 | excluir_do_artigo | analise_central | Deep Neural Network (DNN) + Digital Twin | PROMOVIDO a análise central |

## Evidência e justificativa por registro

### REG_02383

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_central`
- **Evidência**: "multiple regression analysis and back-propagation artificial neural network (BPN) are used to establish a cost model for predicting maintenance costs"
- **Justificativa**: Bloco A (objeto predial: "university buildings", "maintenance") e Bloco B (sustentabilidade: "life-cycle cost analyses") presentes, com técnica de IA/ML explicitamente aplicada e treinada (BPN) para predizer custo de manutenção -- atende ao mesmo critério que classificou "relevante" no corpus original. Promovido a análise central (núcleo).

### REG_07814

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_central`
- **Evidência**: "a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)"
- **Justificativa**: Mesmo padrão de REG_02383/REG_07815 (mesmo grupo de pesquisa, campus da National Taiwan University): Bloco A (university buildings, maintenance) + Bloco B (life-cycle cost) + BPN treinada para predição de custo. Promovido a análise central.

### REG_07815

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_central`
- **Evidência**: "a cost prediction model using the life-cycle cost (LCC) was determined using ... a back propagation artificial neural network (BPN)"
- **Justificativa**: Mesmo padrão de REG_02383/REG_07814: Bloco A + Bloco B (life-cycle cost) + BPN treinada. Promovido a análise central.

### REG_00362

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_secundaria`
- **Evidência**: "a random forest classification model is tested for accuracy in predicting primary space use, magnitude of energy consumption, and type of operational strategy"
- **Justificativa**: IA/ML confirmada (random forest, treinado sobre dados de medidores elétricos), mas sem termo de Bloco A (manutenção/operação predial) nem Bloco B (sustentabilidade) em correspondência literal -- o foco é caracterização de uso/desempenho do edifício a partir de dados de consumo, não manutenção ou sustentabilidade explícitas. Mantido em análise secundária (relação indireta com o escopo da revisão).

### REG_05418

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_central`
- **Evidência**: "A novel ventilation control model, AI-VAV, is developed using a hybrid extreme learning machine (ELM) algorithm combined with simulated annealing (SA) optimisation ... contributing to more sustainable building operations"
- **Justificativa**: Bloco A ("building operation", manutenção de HVAC) + Bloco B ("sustainable building operations") presentes, com técnica de IA/ML explicitamente treinada (ELM) sobre dados de monitoramento de longo prazo. Promovido a análise central.

### REG_06151

- **Decisão anterior**: `analise_secundaria`
- **Decisão revisada**: `analise_secundaria`
- **Evidência**: "This study employs machine learning and Explainable Artificial Intelligence (XAI) to explore the impact ... of energy variables on carbon emissions in office building operations"
- **Justificativa**: IA/ML confirmada (LightGBM/XGBoost/SHAP) e Bloco B presente ("sustainable buildings"), mas sem termo de Bloco A (manutenção predial) em correspondência literal -- foco em emissões de carbono operacionais, não manutenção. Mantido em análise secundária (IA aplicada à energia/operação predial, relação indireta com manutenção).

### REG_06840

- **Decisão anterior**: `excluir_do_artigo`
- **Decisão revisada**: `analise_central`
- **Evidência**: "integrates Digital Twin (DT) technology with machine learning ... employs a Deep Neural Network (DNN) to predict thermal comfort ... sustainable, efficient, and occupant-friendly smart cities"
- **Justificativa**: Exclusão anterior não se sustenta: Bloco A ("smart building operations") + Bloco B ("sustainable", "environmental sustainability") presentes, com IA/ML explicitamente confirmada e validada empiricamente (DNN treinada e comparada a modelos tradicionais). O dicionário anterior (RQ0-RQ5) não reconhecia IA/ML como critério de inclusão, o que motivou a exclusão original apesar da forte relação temática. Exclusão revertida; promovido a análise central.


## Resumo

5 de 7 registros promovidos a análise central (`REG_02383, REG_05418, REG_06840, REG_07814, REG_07815`); os demais 2 (`REG_00362`, `REG_06151`) mantidos em análise secundária, por IA/ML confirmada mas relação com manutenção predial (Bloco A) não estabelecida literalmente no resumo disponível — decisão conservadora, não ampliada por analogia temática.
