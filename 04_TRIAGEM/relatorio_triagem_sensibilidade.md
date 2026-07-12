# RELATÓRIO DE TRIAGEM — Busca de sensibilidade IA/ML (v2 — calibrado)

Gerado por `scripts/python/triagem_sensibilidade_ia_ml.py`. **Correção de calibração**: a primeira versão usava apenas detecção lexical de "maintenance" e gerou 2484 candidatos a núcleo (24x o núcleo original de 104), incompatível com a seletividade do pipeline original. Esta versão reaproveita literalmente a lógica de Bloco A (objeto predial) + Bloco B (sustentabilidade) de `scripts/python/pre_triagem.py` — o mesmo critério que gerou a classe "relevante" no corpus original — combinada com a classe de IA/ML já auditada (Etapa 5).

## Distribuição final

| Decisão | N | % |
|---|---|---|
| excluido | 3782 | 77.4% |
| mapeamento | 798 | 16.3% |
| secundario | 289 | 5.9% |
| nucleo | 20 | 0.4% |
| **Total** | **4889** | 100.0% |

## Classe IA/ML × decisão de triagem

| Classe IA/ML | Núcleo | Secundário | Mapeamento | Excluído |
|---|---|---|---|---|
| FALSO_POSITIVO | 0 | 0 | 0 | 60 |
| IA_ML_APLICACAO_CONFIRMADA | 20 | 289 | 719 | 3020 |
| IA_ML_MENCAO_GENERICA | 0 | 0 | 0 | 15 |
| INFORMACAO_INSUFICIENTE | 0 | 0 | 0 | 275 |
| MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA | 0 | 0 | 5 | 122 |
| TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA | 0 | 0 | 74 | 290 |

## Comparação de escala com o núcleo original

Núcleo original: 104 estudos (de 9542 registros consolidados, ~1.1%). Núcleo desta busca de sensibilidade: 20 estudos (de 4889 registros auditados, 0.4%) — proporção agora da mesma ordem de grandeza do critério original, por usar o mesmo filtro Bloco A + Bloco B.

