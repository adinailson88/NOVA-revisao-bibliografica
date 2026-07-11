# RELATORIO DE PREENCHIMENTO DA MATRIZ DE EXTRACAO FINAL -- ETAPA_13

Gerado por `00_CONFIG/preencher_matriz_extracao_final.py`, a partir de `07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv` (3678 registros do nucleo analitico revisado). Preenche as colunas de conteudo do esquema definido na ETAPA_12, por casamento de frases-chave em titulo+resumo+palavras-chave -- sem leitura de texto completo, conforme mudanca de estrategia registrada em `00_CONTROLE/DECISOES_METODOLOGICAS.md` (entrada de 2026-07-09).

## 1. Cobertura dos campos de conteudo (fora do valor de ausencia)

| Campo | N preenchido | % do nucleo |
|---|---:|---:|
| `pais_contexto` | 978 | 26.6% |
| `tipo_aplicacao` (classificado) | 1522 | 41.4% |
| `dados_utilizados` | 758 | 20.6% |
| `resultado_principal` | 856 | 23.3% |
| `lacuna_identificada` | 320 | 8.7% |

## 2. Criterios de sustentabilidade/gestao detectados (`sim`, multi-label)

| Criterio | N registros com `sim` | % do nucleo |
|---|---:|---:|
| `criterios_ambientais` | 1619 | 44.0% |
| `criterios_tecnicos_operacionais` | 566 | 15.4% |
| `criterios_economicos` | 546 | 14.8% |
| `criterios_sociais` | 399 | 10.8% |
| `criterios_institucionais` | 292 | 7.9% |
| `criterios_risco` | 277 | 7.5% |

## 3. Distribuicao de `tipo_aplicacao`

| Categoria | N registros | % do nucleo |
|---|---:|---:|
| nao_classificavel_pelo_resumo | 2156 | 58.6% |
| estudo_de_caso | 759 | 20.6% |
| revisao_sistematica_ou_bibliometrica | 396 | 10.8% |
| survey_ou_levantamento_com_especialistas | 156 | 4.2% |
| simulacao_ou_modelagem_computacional | 115 | 3.1% |
| proposta_de_framework_ou_modelo | 80 | 2.2% |
| estudo_conceitual_sem_aplicacao_empirica | 16 | 0.4% |

## 4. Distribuicao de `dados_utilizados` (categorias, multi-label)

| Categoria | N registros |
|---|---:|
| dados_de_questionario_ou_entrevista | 520 |
| dados_de_sensores_ou_iot | 134 |
| dados_historicos_ou_registros_de_manutencao | 104 |
| dados_secundarios_de_literatura_ou_documentais | 36 |
| dados_de_simulacao | 13 |

## 5. `resumo_suficiente_para_extracao`

| Valor | N registros | % do nucleo |
|---|---:|---:|
| sim | 1054 | 28.7% |
| parcial | 2237 | 60.8% |
| nao | 387 | 10.5% |

## 6. Metodo e limites

Deteccao por casamento de frases-chave (listas fixas neste script), sem LLM para gerar achados -- mesmo padrao de `00_CONFIG/pre_triagem.py` e `00_CONFIG/sintese_tematica_preliminar.py`. `resultado_principal` e `lacuna_identificada` sao extraidos como a sentenca literal do resumo que contem uma frase-gatilho (ex.: "results show", "future research") -- nao sao resumos gerados, sao trechos copiados do proprio resumo. `dados_utilizados` e preenchido por categoria reconhecida por palavra-chave, nao por paraphrase livre -- interpretacao pratica do esquema da ETAPA_12 para manter o metodo reprodutivel (divergencia documentada, ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`). `contribuicao_para_artigo` fica fixo em `a_definir_na_sintese` e `uso_no_artigo` fica fixo em `pendente` para todos os registros -- sao decisoes de julgamento reservadas para a etapa de sintese/redacao, fora do escopo desta etapa. Registros sem resumo (`resumo_presente != sim`) tem os seis campos `criterios_*` marcados `nao_verificavel_pelo_resumo` e `resumo_suficiente_para_extracao = nao` automaticamente, sem tentativa de deteccao por palavra-chave restrita ao titulo.

## 7. Arquivos gerados

- `07_SINTESE_TEMATICA/matriz_extracao_final.csv` -- 1 linha por registro do nucleo, 49 colunas.
- `07_SINTESE_TEMATICA/relatorio_preenchimento_matriz_extracao_final.md` -- este relatorio.
