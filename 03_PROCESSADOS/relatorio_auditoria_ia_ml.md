# RELATÓRIO DE AUDITORIA — Classe IA/ML (busca de sensibilidade)

Gerado por `scripts/python/auditar_classe_ia_ml.py`, aplicando literalmente as regras de `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` sobre os 4889 registros de `sensibilidade_novos_unicos.csv` — **sem amostragem, cobertura de 100%**. Método: correspondência sistemática de termos do dicionário RQ6 em título/resumo/palavras-chave, com regras de desambiguação (transformer, decision tree, deep learning fora de contexto) e heurística lexical de aplicação efetiva vs. menção genérica. Não constitui leitura de texto completo.

## Distribuição por classe

| Classe | N | % |
|---|---|---|
| IA_ML_APLICACAO_CONFIRMADA | 4048 | 82.8% |
| TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA | 364 | 7.4% |
| INFORMACAO_INSUFICIENTE | 275 | 5.6% |
| MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA | 127 | 2.6% |
| FALSO_POSITIVO | 60 | 1.2% |
| IA_ML_MENCAO_GENERICA | 15 | 0.3% |
| **Total** | **4889** | 100.0% |

## Distribuição por classe × base

| Classe | Scopus | WoS | Crossref |
|---|---|---|---|
| IA_ML_APLICACAO_CONFIRMADA | 2353 | 126 | 1569 |
| TECNICA_COMPATIVEL_MAS_NAO_CONFIRMADA | 291 | 44 | 29 |
| MANUTENCAO_PREDITIVA_SEM_IA_COMPROVADA | 99 | 22 | 6 |
| FALSO_POSITIVO | 26 | 9 | 25 |
| INFORMACAO_INSUFICIENTE | 0 | 0 | 275 |
| IA_ML_MENCAO_GENERICA | 0 | 0 | 15 |

## Nível de confiança

| Nível | N |
|---|---|
| alto | 4063 |
| medio | 551 |
| baixo | 275 |

## Cobertura de resumo

- Registros sem resumo: 1444 de 4889 (29.5%).
- Distribuição de classe entre os registros sem resumo (auditados apenas por título/palavras-chave):
  - IA_ML_APLICACAO_CONFIRMADA: 1136
  - INFORMACAO_INSUFICIENTE: 275
  - FALSO_POSITIVO: 19
  - IA_ML_MENCAO_GENERICA: 14

Conforme já documentado na normalização, a ausência de resumo concentra-se na fatia Crossref e reduz sistematicamente o nível de confiança da auditoria nesse subconjunto — não é uma falha da auditoria, é limitação de cobertura da fonte.
