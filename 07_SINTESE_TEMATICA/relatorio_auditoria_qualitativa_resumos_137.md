# Relatório metodológico — ETAPA_16

## 1. Objetivo da etapa

Refinar o núcleo principal da síntese do artigo por meio da auditoria qualitativa estruturada dos 137 registros previamente classificados como `analise_central` na ETAPA_15.

## 2. Arquivo de entrada

`07_SINTESE_TEMATICA/nucleo_principal_sintese_artigo.csv`

## 3. Total de registros auditados

137 registros, todos com identificador único, título e resumo presentes.

## 4. Método de auditoria

Foi realizada auditoria qualitativa estruturada dos 137 registros previamente classificados como análise central, com base em título, resumo, palavras-chave e campos extraídos nas etapas anteriores. A decisão de uso no artigo foi registrada em tabela auditável, com justificativa e evidência curta por registro. Não houve leitura de texto completo nesta etapa.

## 5. Critérios de decisão

- `manter_nucleo_principal`: contribuição substantiva à pergunta central ou a pelo menos duas perguntas secundárias, com relação aplicável ao ambiente construído.
- `manter_como_secundario`: aderência temática, mas sustentação indireta ou limitada para a síntese principal.
- `usar_apenas_mapeamento`: utilidade descritiva ou panorâmica sem conteúdo suficiente para síntese analítica.
- `excluir_sintese`: falso positivo, baixa aderência ou contexto não predial sem sustentação confiável das perguntas de pesquisa.

## 6. Total por decisão qualitativa

| Decisão | Total | Percentual |
|---|---:|---:|
| manter_nucleo_principal | 105 | 76.6% |
| manter_como_secundario | 21 | 15.3% |
| usar_apenas_mapeamento | 3 | 2.2% |
| excluir_sintese | 8 | 5.8% |

## 7. Núcleo final pós-auditoria

O núcleo final contém **105 registros**.

## 8. Registros secundários

Foram mantidos **21 registros** como apoio secundário.

## 9. Registros para mapeamento

Foram destinados **3 registros** exclusivamente ao mapeamento descritivo.

## 10. Registros excluídos

Foram excluídos **8 registros** da síntese.

## 11. RQs confirmadas após a leitura estruturada

RQ0: 115, RQ1: 137, RQ2: 137, RQ3: 109, RQ4: 134, RQ5: 96.

## 12. Métodos e abordagens de decisão identificados

Os dez termos mais frequentes foram: `framework` (126), `optimization` (33), `decision support` (32), `BIM` (28), `scoring` (22), `fuzzy` (15), `life-cycle cost` (15), `machine learning` (15), `IoT` (12), `ranking` (11). A contagem completa está na Tabela 24. Um registro pode conter mais de um método ou abordagem.

## 13. Critérios de priorização identificados

Os dez critérios mais frequentes foram: `desempenho_operacional` (124), `informacao_dados` (97), `custo` (79), `energia` (59), `vida_util` (49), `risco` (42), `condicao_fisica` (42), `conforto` (25), `emissoes_carbono` (24), `seguranca` (23). A contagem completa está na Tabela 25. Um registro pode conter mais de um critério.

## 14. Necessidade de full-text pontual

1 registro precisa de leitura pontual do texto completo para aprofundar método, critérios ou evidência: REG_07264.

## 15. Limitações

A auditoria foi feita com base em título, resumo, palavras-chave e campos previamente extraídos. Não substitui leitura full-text. As evidências registradas devem ser tratadas como base para síntese por resumo e para priorização de leitura pontual, não como extração completa do conteúdo integral dos artigos. As decisões de fronteira continuam sujeitas a revisão humana antes da redação final.

## 16. Arquivos gerados

- `07_SINTESE_TEMATICA/auditoria_qualitativa_resumos_137.csv`
- `07_SINTESE_TEMATICA/nucleo_final_pos_auditoria_resumos.csv`
- `07_SINTESE_TEMATICA/registros_secundarios_pos_auditoria_resumos.csv`
- `07_SINTESE_TEMATICA/registros_mapeamento_pos_auditoria_resumos.csv`
- `07_SINTESE_TEMATICA/registros_excluidos_pos_auditoria_resumos.csv`
- `05_ANALISE_R/tabelas/tabela21_decisao_qualitativa_resumos_137.csv`
- `05_ANALISE_R/tabelas/tabela22_rqs_confirmadas_auditoria_resumos.csv`
- `05_ANALISE_R/tabelas/tabela23_full_text_pontual_auditoria_resumos.csv`
- `05_ANALISE_R/tabelas/tabela24_metodos_decisao_auditoria_resumos.csv`
- `05_ANALISE_R/tabelas/tabela25_criterios_identificados_auditoria_resumos.csv`
- `07_SINTESE_TEMATICA/relatorio_auditoria_qualitativa_resumos_137.md`
- `00_CONTROLE/ESTADO_ATUAL.md`
- `00_CONTROLE/DECISOES_METODOLOGICAS.md`
- `00_CONTROLE/ROTINAS/LOGS/ETAPA_16_AUDITORIA_QUALITATIVA_RESUMOS_137.md`
- `00_CONTROLE/ROTINAS/DONE/ETAPA_16_AUDITORIA_QUALITATIVA_RESUMOS_137.done`

## 17. Recomendação para a próxima etapa

Utilizar `07_SINTESE_TEMATICA/nucleo_final_pos_auditoria_resumos.csv` como base operacional da síntese analítica, mantendo os registros secundários apenas como apoio. Antes da redação final, revisar humanamente os casos de fronteira e realizar somente a leitura full-text pontual já marcada, sem ampliar automaticamente o corpus.

## 18. Adendo — 2026-07-10

Por decisão explícita do usuário, o registro `REG_07264` ("Path dependencies and sustainable facilities management: a study of housing companies in Sweden"), único marcado com `necessita_full_text_pontual = sim`, foi descartado da síntese em vez de ser encaminhado para leitura full-text pontual. Sua `decisao_qualitativa_final` foi alterada de `manter_nucleo_principal` para `excluir_sintese`, e `asreview_label_compativel` de `include` para `exclude`.

Totais revisados:

| Decisão | Total | Percentual (dos 137) |
|---|---:|---:|
| manter_nucleo_principal | 104 | 75.9% |
| manter_como_secundario | 21 | 15.3% |
| usar_apenas_mapeamento | 3 | 2.2% |
| excluir_sintese | 9 | 6.6% |

O núcleo final pós-auditoria passa de 105 para **104 registros**. A pendência de leitura full-text pontual foi resolvida para **0 registros** (nenhum full-text foi lido; o registro pendente foi descartado, não lido).

Arquivos recalculados nesta rodada: `auditoria_qualitativa_resumos_137.csv`, os quatro recortes por decisão, `tabela21_decisao_qualitativa_resumos_137.csv` e `tabela23_full_text_pontual_auditoria_resumos.csv`. As Tabelas 22, 24 e 25 não foram alteradas, pois refletem sinais de leitura sobre os 137 registros auditados, não a decisão final de uso.
