# Relatorio de reavaliacao criteriosa dos resumos

## 1. Objetivo da etapa
Criar uma camada intermediaria, auditavel e reprodutivel de uso do nucleo analitico revisado, separando os 3.678 registros por forca do resumo sem leitura full-text e sem uso de LLM.

## 2. Arquivo de entrada
- `./07_SINTESE_TEMATICA/matriz_extracao_final.csv`

## 3. Arquivos de saida
- `./07_SINTESE_TEMATICA/matriz_extracao_final_reavaliada_resumos.csv`
- `./07_SINTESE_TEMATICA/relatorio_reavaliacao_criteriosa_resumos.md`
- `./05_ANALISE_R/tabelas/tabela14_reavaliacao_resumos_por_estrato.csv`
- `./05_ANALISE_R/tabelas/tabela15_sinais_reavaliacao_resumos.csv`
- `./05_ANALISE_R/tabelas/amostra_auditoria_reavaliacao_resumos.csv`
- `./00_CONTROLE/ROTINAS/LOGS/ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.md`

## 4. Data/hora
- 2026-07-09 01:19:40

## 5. Total de registros lidos
- 3678

## 6. Total por estrato
- `A_nucleo_forte`: 372
- `B_nucleo_descritivo`: 830
- `C_contextual`: 157
- `D_descartar_sintese`: 2319

## 7. Percentual por estrato
- `A_nucleo_forte`: 10.1%
- `B_nucleo_descritivo`: 22.6%
- `C_contextual`: 4.3%
- `D_descartar_sintese`: 63.1%

## 8. Total que entra na sintese analitica forte
- 372

## 9. Total que entra no mapeamento descritivo
- 1202

## 10. Total descartado da sintese
- 2319

## 11. Lista dos campos encontrados e usados
- Coluna de titulo: `titulo`
- Coluna de resumo: `resumo`
- Coluna de palavras-chave: `palavras_chave`
- Campos auxiliares encontrados: `tipo_aplicacao`, `dados_utilizados`, `resultado_principal`, `lacuna_identificada`, `resumo_suficiente_para_extracao`, `criterios_ambientais`, `criterios_tecnicos_operacionais`, `criterios_economicos`, `criterios_sociais`, `criterios_institucionais`, `criterios_risco`, `eixo_tematico_preliminar`

## 12. Lista dos campos esperados que nao foram encontrados
- `metodo_decisao`, `contexto_publico_universitario`, `tipo_edificacao`

## 13. Explicacao das regras
- `A_nucleo_forte`: exige objeto predial, manutencao/gestao, sustentabilidade/desempenho, evidencia analitica, ausencia de exclusao forte, `resumo_suficiente_para_extracao = sim` e pontuacao >= 7.
- `B_nucleo_descritivo`: exige objeto predial, manutencao/gestao, sustentabilidade/desempenho, ausencia de exclusao forte, `resumo_suficiente_para_extracao = sim/parcial` e pontuacao >= 5.
- `C_contextual`: exige objeto predial e pelo menos manutencao/gestao ou sustentabilidade, sem cumprir os criterios de A ou B, e pontuacao >= 3.
- `D_descartar_sintese`: agrega exclusao forte, falta de objeto predial, falta de manutencao/gestao, falta de sustentabilidade/desempenho ou evidencia insuficiente.

## 14. Explicacao da pontuacao
- objeto predial = +2
- manutencao/gestao/operacao/facility management/retrofit/condition assessment = +2
- sustentabilidade/desempenho/energia/custo/risco/conforto/institucional = +2
- metodo/dado/resultado/lacuna = +1
- tipo de aplicacao informativo = +1
- dados utilizados informativos = +1
- resultado principal informativo = +1
- lacuna identificada informativa = +1
- termo forte de exclusao = -4

## 15. Limitacoes
- A etapa nao substitui leitura full-text.
- A ausencia de informacao no resumo nao foi tratada como evidencia positiva.
- Os sinais dependem de titulo, resumo, palavras-chave e campos ja existentes na matriz final.
- Campos auxiliares ausentes nao impediram a execucao, mas reduziram a capacidade de classificacao fina.

## 16. Recomendacao de uso no artigo
- usar `A_nucleo_forte` para a sintese analitica principal;
- usar `A_nucleo_forte + B_nucleo_descritivo` para tabelas e estatisticas descritivas;
- usar `C_contextual` apenas como apoio, se necessario;
- excluir `D_descartar_sintese` da sintese analitica;
- deixar claro no artigo que esta etapa usa titulo, resumo e palavras-chave, sem leitura full-text.
