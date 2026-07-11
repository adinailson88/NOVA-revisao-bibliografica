# Relatorio de alinhamento dos registros as perguntas de pesquisa

## 1. Objetivo da ETAPA_15
Alinhar os 3.678 registros reavaliados por resumo as perguntas de pesquisa do artigo, por meio de um dicionario CSV reprodutivel e regras auditaveis aplicadas apenas a titulo, resumo, palavras-chave e campos previamente extraidos.

## 2. Arquivo de entrada
- `C:\tmp\etapa15_stage_20260709_b/07_SINTESE_TEMATICA/matriz_extracao_final_reavaliada_resumos.csv`

## 3. Arquivos de saida
- `C:\tmp\etapa15_stage_20260709_b/07_SINTESE_TEMATICA/matriz_alinhamento_perguntas_pesquisa.csv`
- `C:\tmp\etapa15_stage_20260709_b/07_SINTESE_TEMATICA/nucleo_principal_sintese_artigo.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/tabela16_aderencia_por_rq.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/tabela17_uso_recomendado_artigo.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/tabela18_cruzamento_estrato_resumo_uso_artigo.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/tabela19_nucleo_principal_por_ano.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/tabela20_nucleo_principal_por_base.csv`
- `C:\tmp\etapa15_stage_20260709_b/05_ANALISE_R/tabelas/amostra_auditoria_etapa15_alinhamento_rq.csv`
- `C:\tmp\etapa15_stage_20260709_b/07_SINTESE_TEMATICA/relatorio_alinhamento_perguntas_pesquisa.md`

## 4. Data/hora
- 2026-07-09 01:45:15

## 5. Total de registros lidos
- 3678

## 6. Total por uso_recomendado_artigo
- `analise_central`:  137 (3.7%)
- `analise_secundaria`:  651 (17.7%)
- `mapeamento_descritivo`:  375 (10.2%)
- `apoio_contextual`:  157 (4.3%)
- `excluir_do_artigo`: 2358 (64.1%)

## 7. Percentual por uso_recomendado_artigo
- `analise_central`:  137 (3.7%)
- `analise_secundaria`:  651 (17.7%)
- `mapeamento_descritivo`:  375 (10.2%)
- `apoio_contextual`:  157 (4.3%)
- `excluir_do_artigo`: 2358 (64.1%)

## 8. Total por RQ
- `RQ0`: 1213 (33.0%)
- `RQ1`: 2885 (78.4%)
- `RQ2`: 2401 (65.3%)
- `RQ3`: 1140 (31.0%)
- `RQ4`: 1579 (42.9%)
- `RQ5`: 1273 (34.6%)

## 9. Cruzamento entre estrato_uso_resumo e uso_recomendado_artigo
```text
  estrato_uso_resumo analise_central analise_secundaria excluir_do_artigo
      A_nucleo_forte             137                195                 5
 B_nucleo_descritivo               0                456                34
        C_contextual               0                  0                 0
 D_descartar_sintese               0                  0              2319
 mapeamento_descritivo apoio_contextual
                    35                0
                   340                0
                     0              157
                     0                0
```

## 10. Total do nucleo principal recomendado
- 137

## 11. Explicacao do dicionario de termos
- O dicionario principal esta em `C:\tmp\etapa15_stage_20260709_b/07_SINTESE_TEMATICA/dicionario_rq_etapa15.csv` com colunas `rq`, `categoria`, `termo`, `peso` e `observacao`.
- Os termos sao lidos pelo script e aplicados diretamente sobre `texto_alinhamento_rq`.

## 12. Explicacao da pontuacao
- RQ0 = +3; RQ1 = +1; RQ2 = +2; RQ3 = +2; RQ4 = +1; RQ5 = +2.
- `A_nucleo_forte` = +2; `B_nucleo_descritivo` = +1; `C_contextual` = -1; `D_descartar_sintese` = -5.
- `resumo_suficiente_para_extracao` = `sim` +2; `parcial` +0; `nao` -3.
- Sinal forte de exclusao herdado ou textual = -5.

## 13. Explicacao dos criterios de decisao
- `analise_central`: estrato A, score >= 8, pelo menos 3 RQs e resposta a RQ0 ou a RQ2+RQ3.
- `analise_secundaria`: estrato A/B, score >= 5 e pelo menos 2 RQs.
- `mapeamento_descritivo`: estrato A/B com pelo menos 1 RQ.
- `apoio_contextual`: estrato C ou resposta fraca/contextual concentrada em RQ4/RQ5.
- `excluir_do_artigo`: estrato D, zero RQ, score < 2 ou exclusao forte.

## 14. Lista de campos encontrados
- titulo, resumo, palavras_chave, tipo_aplicacao, dados_utilizados, resultado_principal, lacuna_identificada, criterios_ambientais, criterios_tecnicos_operacionais, criterios_economicos, criterios_sociais, criterios_institucionais, criterios_risco, metodo_decisao, tipo_edificacao, eixo_tematico_preliminar, estrato_uso_resumo, resumo_suficiente_para_extracao, justificativa_reavaliacao_resumo

## 15. Lista de campos esperados e ausentes
- contexto_publico_universitario

## 16. Limitacoes
- A etapa usa sinais textuais em titulo, resumo, palavras-chave e campos previamente extraidos.
- Ela nao substitui leitura full-text nem permite afirmar resultados profundos para todos os registros.
- O alinhamento depende do vocabulario do dicionario e da qualidade dos campos auxiliares disponiveis.

## 17. Recomendacao para o proximo passo
- usar `nucleo_principal_sintese_artigo.csv` para a sintese analitica principal;
- usar registros `analise_secundaria` para complementar a discussao;
- usar `mapeamento_descritivo` apenas para tabelas gerais;
- nao usar `excluir_do_artigo` no artigo;
- auditar manualmente a amostra antes da redacao final;
- so fazer leitura full-text pontual para os registros centrais mais importantes, se necessario.

## 18. sessionInfo()
```text
R version 4.5.3 (2026-03-11 ucrt)
Platform: x86_64-w64-mingw32/x64
Running under: Windows 11 x64 (build 26200)

Matrix products: default
  LAPACK version 3.12.1

locale:
[1] C
system code page: 65001

time zone: America/Bahia
tzcode source: internal

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base     

other attached packages:
[1] tidyr_1.3.2   stringr_1.6.0 dplyr_1.2.1   readr_2.2.0  

loaded via a namespace (and not attached):
 [1] crayon_1.5.3     vctrs_0.7.2      cli_3.6.5        rlang_1.1.7     
 [5] stringi_1.8.7    purrr_1.2.1      generics_0.1.4   glue_1.8.0      
 [9] bit_4.6.0        hms_1.1.4        tibble_3.3.1     tzdb_0.5.0      
[13] lifecycle_1.0.5  compiler_4.5.3   pkgconfig_2.0.3  R6_2.6.1        
[17] tidyselect_1.2.1 vroom_1.7.0      pillar_1.11.1    parallel_4.5.3  
[21] magrittr_2.0.4   tools_4.5.3      withr_3.0.2      bit64_4.6.0-1   
```
