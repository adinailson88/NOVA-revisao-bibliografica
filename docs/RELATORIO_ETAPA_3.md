# Relatório da Etapa 3

## Tabela de progresso

| Etapa | Situação |
|---|---|
| Etapa 1 | OK |
| Etapa 2 | OK |
| Etapa 3 | OK |

## 1. Escopo executado

Auditoria da estratégia de busca, datas, campos, strings, operadores, período, filtros, limites, atualização de índice, justificativas e reprodutibilidade nas bases Scopus, Web of Science e Crossref.

## 2. Arquivos analisados

Metodologia, tabelas de estratégia, scripts de coleta Scopus e Crossref, documentação do repositório, relatório anterior e status.

## 3. Evidências encontradas

Foram documentadas 13 consultas em 8 de julho de 2026, seis registros adicionais da Scopus em 9 de julho, quatro strings completas da Scopus, cinco consultas completas do Crossref, campos, período, paginação, limites e totais. O Crossref funciona como fonte complementar.

## 4. Problemas identificados

As strings literais da Web of Science não estão no repositório. Também não foram localizados datas de exportação distintas, busca piloto, estudos-semente, filtros de idioma ou tipo documental e justificativa específica para 2010.

## 5. Alterações realizadas

A metodologia passou a registrar datas, período, campos, limites, caráter complementar do Crossref e informações ausentes. A tabela por base foi ampliada. Foi criado apêndice com todas as consultas verificáveis e avaliação de reprodutibilidade.

## 6. Alterações não realizadas

Nenhuma busca foi repetida; strings não foram reconstruídas; filtros não foram presumidos; totais e corpus não foram modificados.

## 7. Informação insuficiente para verificar

Strings Web of Science, datas de exportação distintas, filtros manuais, busca piloto, estudos-semente e justificativa específica do marco de 2010.

## 8. Validações executadas

Soma por base: 9.439 + 1.679 + 1.000 = 12.118. Soma das quatro consultas Scopus mais complemento: 7.584 + 430 + 510 + 909 + 6 = 9.439. Soma Web of Science: 610 + 557 + 10 + 502 = 1.679. Crossref: 5 × 200 = 1.000. Strings conferidas com os scripts.

## 9. Arquivos alterados

- `latex-artigo/sections/03_metodologia.tex`
- `docs/APENDICE_ESTRATEGIAS_BUSCA.md`
- `docs/RELATORIO_ETAPA_3.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Commit exclusivo da Etapa 3, com hash informado ao usuário.

## 11. Pendências

A ausência das strings literais da Web of Science impede reprodução integral. A coleta não será refeita sem autorização específica.

## 12. Próxima etapa prevista

Etapa 4 — Funil de seleção.

Execução interrompida conforme o planejamento. Aguardando autorização expressa para prosseguir.


## Retificação documental posterior

As pendências foram regularizadas com as informações fornecidas pelo pesquisador:

- quatro strings da Web of Science preservadas;
- buscas e exportações realizadas em 08/07/2026;
- sem filtros de idioma ou tipo documental;
- não houve busca piloto;
- não foram utilizados estudos-semente;
- protocolo elaborado antes da coleta;
- justificativa específica para 2010 não documentada;
- a associação individual entre RIS e strings A1–A4 da Web of Science foi informada de memória;
- não há evidência preservada de complemento da Scopus em 09/07/2026; a diferença de seis registros foi atribuída à consolidação após reexecução em 08/07/2026, sem causa específica preservada.


## Segunda retificação documental

A diferença de seis registros foi reconciliada:

- Scopus: 9.433 registros da API + 5 registros existentes apenas no export manual, adicionados no enriquecimento por EID de 09/07/2026 = 9.438;
- Web of Science: 610 + 557 + 10 + 503 = 1.680; o valor anterior de 502 em A4 decorria de contagem com âncora de linha;
- Crossref: 1.000;
- total bruto: 9.438 + 1.680 + 1.000 = 12.118.

O período 2010–2026 foi mantido porque corresponde à busca efetivamente executada. Não foi criada justificativa retrospectiva para o marco de 2010.
