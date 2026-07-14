# Status — Consolidação da busca de sensibilidade IA/ML e ajuste científico do artigo

Arquivo único e cumulativo de continuidade desta tarefa. Atualizar este documento ao final de cada etapa. Não criar arquivo de status paralelo.

## Estado consolidado em 13/07/2026

- Repositório: `adinailson88/NOVA-revisao-bibliografica`.
- Branch: `agent/incorporacao-busca-sensibilidade-ia`.
- Pull Request: #4, em modo draft, base `main`.
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
- Compilação integral anterior concluída sem divergência numérica, referência indefinida ou `Overfull \hbox`.

## Encerramento das lacunas documentais das strings

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

A antiga declaração “Informação insuficiente para verificar” foi removida da tabela-fonte, do método e das limitações. O verificador integrado passou a exigir a presença das strings completas, da opção All Databases, da data, do período e da declaração de ausência de filtros adicionais.

## Alterações desta consolidação documental

- `d2ee7a8`: criação do registro integral das strings.
- `96fd94a`: atualização do log da busca complementar.
- `d159ad4`: atualização das limitações.
- `d1b38cf`: integração das strings completas na tabela-fonte.
- `55c8000`: atualização da metodologia e da tabela apresentada no artigo.
- `a0821e2` e `f480b7c`: adaptação do verificador acumulado.
- `c4c2a21`: atualização do workflow para executar o verificador integrado.

## Estado final desta etapa

As lacunas documentais das strings estão encerradas nos arquivos-fonte. O PR #4 permanece aberto, em modo draft e mergeável. A execução automatizada correspondente aos últimos commits ainda deve aparecer e ser conferida no GitHub Actions antes da retirada do modo draft e do merge na `main`.