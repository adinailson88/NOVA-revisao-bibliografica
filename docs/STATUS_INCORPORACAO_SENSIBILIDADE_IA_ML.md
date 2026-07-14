# Status — Consolidação da busca de sensibilidade IA/ML e ajuste científico do artigo

## Estado consolidado

- Repositório: `adinailson88/NOVA-revisao-bibliografica`.
- Branch de trabalho: `agent/incorporacao-busca-sensibilidade-ia`.
- Pull Request: #4.
- Núcleo temático vigente: 121 registros, sendo 104 do núcleo original e 17 incorporados após a busca complementar de sensibilidade.
- Camada bibliométrica: 372 registros derivados exclusivamente da busca principal.
- Busca de sensibilidade: 6.728 ocorrências brutas, sendo 3.169 da Scopus, 1.559 da Web of Science e 2.000 do Crossref.

## Produtos científicos e técnicos concluídos

- Normalização e deduplicação da busca complementar contra o corpus original.
- Classificação determinística dos 4.889 registros novos únicos segundo o manual de codificação da RQ6.
- Revisão individual dos candidatos por título e resumo.
- Incorporação de 12 registros novos e promoção de cinco registros já presentes no corpus.
- Leitura integral pontual de sete dos 17 registros incorporados, com cinco textos acrescentando evidências específicas.
- Matriz comparativa dos 17 registros.
- Resposta direta à RQ6 no método, resultados, discussão e considerações finais.
- Pipeline Python alinhado ao núcleo vigente de 121 registros.
- Preservação explícita dos produtos históricos de 104 registros.
- Revisão de suporte bibliográfico das assertivas gerais.
- Revisão global de concisão, coerência terminológica, resultados, discussão, limitações e conclusão.

## Strings da busca complementar

As expressões integrais da busca complementar foram fornecidas pelo pesquisador e incorporadas ao repositório.

### Scopus

- Campo: `TITLE-ABS-KEY`.
- Período: 2010–2026.
- Data: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total: 3.169 ocorrências brutas.

### Web of Science

- Base consultada: Web of Science — All Databases.
- Campo: Topic (`TS`).
- Período: 2010–2026.
- Data: 12/07/2026.
- Filtros adicionais: nenhum além do período de publicação.
- Total: 1.559 ocorrências brutas.
- Observação: os registros exportados apresentam indexação na Web of Science Core Collection.

### Crossref

- Dez consultas por `query.bibliographic`.
- Filtro: `from-pub-date:2010-01-01,until-pub-date:2026-12-31`.
- `rows=200` e ordenação por relevância.
- Total: 2.000 ocorrências brutas e 1.993 registros após deduplicação interna.

As strings e os parâmetros estão registrados em:

- `01_PROTOCOLO/strings_busca_sensibilidade_ia_ml_20260712.md`;
- `01_PROTOCOLO/log_busca_sensibilidade_ia_20260712.md`;
- `latex-artigo/fontes/tabela_estrategia_busca.csv`.

## Validação final

A execução completa nº 206 do workflow `Validar fontes e gerar artigo` foi concluída com sucesso. Foram validados:

- geração das tabelas e gráficos do núcleo vigente;
- camada bibliométrica ampliada;
- inventário e planilhas de referências;
- coerência numérica, textual e bibliográfica;
- documentação das strings da busca de sensibilidade;
- compilação do PDF;
- geração e integridade do arquivo Word;
- ausência de estouro de margens no PDF;
- publicação dos produtos como artefato.

Após a restauração da política normal do workflow, a execução nº 209 foi concluída com sucesso. O workflow voltou a gerar PDF e Word apenas por execução manual ou na `main`, mantendo nas branches e pull requests as verificações reprodutíveis em Python.

## Situação final

Não permanecem lacunas documentais das strings, divergências numéricas conhecidas, erros de compilação ou falhas do verificador. O PR está apto para retirada do modo draft e merge na `main`.