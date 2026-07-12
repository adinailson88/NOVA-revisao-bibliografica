# RELATÓRIO DE TRIAGEM — Busca de sensibilidade IA/ML (v2 — calibrado)

Gerado por `scripts/python/triagem_sensibilidade_ia_ml.py`. **Correção de calibração**: a primeira versão usava apenas detecção lexical de "maintenance" e gerou 2484 candidatos a núcleo (24x o núcleo original de 104), incompatível com a seletividade do pipeline original. Esta versão reaproveita literalmente a lógica de Bloco A (objeto predial) + Bloco B (sustentabilidade) de `scripts/python/pre_triagem.py` — o mesmo critério que gerou a classe "relevante" no corpus original — combinada com a classe de IA/ML já auditada (Etapa 5).

## Distribuição final (após revisão manual dos 20 candidatos a núcleo)

O filtro automático Bloco A + Bloco B + IA/ML confirmada gerou 20 candidatos a núcleo. Leitura
integral do resumo de cada um dos 20 (Etapa 6, revisão manual pontual dos casos de fronteira)
identificou 8 falsos positivos de contexto — IA/ML confirmada e termo "maintenance" presente,
mas sobre domínio industrial/aeroespacial/veicular sem nenhuma ponte predial real (ex.:
manutenção preditiva de máquinas de manufatura, bombas moleculares de instalação de fusão
nuclear, estações de recarga veicular, impressoras 3D, fadiga de componentes aeroespaciais,
contagem de lotação de academia, contagem de tráfego sem contexto de edificação). Esses 8 foram
reclassificados para `excluido` (justificativa individual registrada em cada linha do CSV,
prefixo "REVISÃO MANUAL").

| Decisão | N | % |
|---|---|---|
| excluido | 3790 | 77.5% |
| mapeamento | 798 | 16.3% |
| secundario | 289 | 5.9% |
| nucleo | 12 | 0.2% |
| **Total** | **4889** | 100.0% |

## Classe IA/ML × decisão de triagem (após revisão manual)

| Classe IA/ML | Núcleo | Secundário | Mapeamento | Excluído |
|---|---|---|---|---|
| FALSO_POSITIVO | 0 | 0 | 0 | 60 |
| IA_ML_APLICACAO_CONFIRMADA | 12 | 289 | 719 | 3028 |
| IA_ML_MENCAO_GENERICA | 0 | 0 | 0 | 15 |
| INFORMACAO_INSUFICIENTE | 0 | 0 | 0 | 275 |
| MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA | 0 | 0 | 5 | 122 |
| TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA | 0 | 0 | 74 | 290 |

## Comparação de escala com o núcleo original

Núcleo original: 104 estudos (de 9542 registros consolidados, ~1.1%). Núcleo desta busca de
sensibilidade, após revisão manual: 12 estudos (de 4889 registros auditados, 0.25%) — proporção
da mesma ordem de grandeza (ligeiramente mais seletiva) do critério original. Somados aos 5
registros REG_ promovidos na reavaliação (Etapa 6, `docs/REAVALIACAO_7_REGISTROS_SENSIBILIDADE.md`),
o total de novos estudos de núcleo desta rodada é **17**.

