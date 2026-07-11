# Apêndice documental — Estratégias de busca

## 1. Escopo

Este apêndice registra as consultas e os parâmetros da busca executada e exportada em 8 de julho de 2026. As strings da Web of Science foram fornecidas pelo pesquisador a partir do protocolo original; a associação individual A1--A4 aos arquivos RIS foi informada de memória, conforme ressalva do log da busca manual.

## 2. Scopus

Parâmetros documentados:

- Endpoint: `https://api.elsevier.com/content/search/scopus`
- Campo: `TITLE-ABS-KEY`
- Período: 2010–2026, acrescentado dinamicamente como `PUBYEAR > 2009 AND PUBYEAR < 2027`
- Paginação: 25 registros
- Janela máxima da API: 5.000 resultados
- Tratamento da janela: particionamento recursivo por intervalos de ano
- Filtros de idioma: não aplicados
- Filtros de tipo documental: não aplicados

### S1 — manutenção e sustentabilidade

```text
TITLE-ABS-KEY(("building maintenance" OR "facility management" OR "facilities management" OR "facilities maintenance" OR "building asset management" OR "building operation" OR "operation and maintenance" OR "maintenance management") AND (sustainab* OR "green building*" OR "life cycle" OR "life-cycle" OR "sustainability assessment" OR "sustainability indicator*" OR "environmental performance" OR "building performance"))
```

Retorno bruto documentado: 7.584.

### S2 — contexto público universitário

```text
TITLE-ABS-KEY(("public building*" OR "university building*" OR "university campus" OR "higher education institution*" OR "educational building*" OR "government building*" OR "public sector building*" OR "building portfolio") AND ("building maintenance" OR maintenance OR "facility management" OR "facilities management" OR "asset management" OR "operation and maintenance") AND (sustainab* OR "environmental performance" OR "life cycle" OR "sustainability assessment"))
```

Retorno bruto documentado: 430.

### S3 — priorização e estratégia de manutenção

```text
TITLE-ABS-KEY(("maintenance prioritization" OR "maintenance backlog" OR "deferred maintenance" OR "maintenance strategy" OR "maintenance planning" OR "renewal prioritization" OR "condition assessment" OR "condition-based maintenance") AND (building* OR "public building*" OR "university building*" OR campus OR "building portfolio" OR "built environment" OR "facility management" OR "facilities management") AND (sustainab* OR "environmental criteria" OR "social criteria" OR "life cycle" OR "risk-based maintenance"))
```

Retorno bruto documentado: 510.

### S4 — gestão de ativos e ciclo de vida

```text
TITLE-ABS-KEY(("building asset management" OR "facility management" OR "facilities management" OR "building maintenance" OR "building operation" OR "operation and maintenance") AND ("life cycle" OR "life-cycle" OR "whole life cost" OR "life cycle cost" OR "service life" OR durability OR "building performance" OR "asset performance") AND (sustainab* OR "environmental performance" OR "sustainability assessment"))
```

Retorno bruto documentado: 909.

A coleta pela API totalizou 9.433 registros. Em 9 de julho de 2026, o enriquecimento manual por casamento de EID identificou cinco registros existentes apenas no export do site, incorporados ao corpus. Total Scopus: 9.438.

## 3. Web of Science

Parâmetros documentados:

- Campo: \`TS (Topic)\`
- Período: \`PY=(2010-2026)\`
- Execução e exportação: manual, em 8 de julho de 2026
- Filtros de idioma: não aplicados
- Filtros de tipo documental: não aplicados
- Número de consultas: quatro
- Retornos: W1 = 610; W2 = 557; W3 = 10; W4 = 503
- Total: 1.680
- Ressalva de proveniência: a correspondência individual entre arquivos RIS e strings A1--A4 foi informada de memória pelo pesquisador, não reconstruída a partir de evidência registrada no momento da busca.

### W1 — manutenção e sustentabilidade

\`\`\`text
TS=(("building maintenance" OR "facility management" OR "facilities management" OR "facilities maintenance" OR "building asset management" OR "building operation" OR "operation and maintenance" OR "maintenance management") AND (sustainab* OR "green building*" OR "life cycle" OR "life-cycle" OR "sustainability assessment" OR "sustainability indicator*" OR "environmental performance" OR "building performance")) AND PY=(2010-2026)
\`\`\`

### W2 — contexto público universitário

\`\`\`text
TS=(("public building*" OR "university building*" OR "university campus" OR "higher education institution*" OR "educational building*" OR "government building*" OR "public sector building*" OR "building portfolio") AND ("building maintenance" OR maintenance OR "facility management" OR "facilities management" OR "asset management" OR "operation and maintenance") AND (sustainab* OR "environmental performance" OR "life cycle" OR "sustainability assessment")) AND PY=(2010-2026)
\`\`\`

### W3 — priorização e estratégia de manutenção

\`\`\`text
TS=(("maintenance prioritization" OR "maintenance backlog" OR "deferred maintenance" OR "maintenance strategy" OR "maintenance planning" OR "renewal prioritization" OR "condition assessment" OR "condition-based maintenance") AND (building* OR "public building*" OR "university building*" OR campus OR "building portfolio" OR "built environment" OR "facility management" OR "facilities management") AND (sustainab* OR "environmental criteria" OR "social criteria" OR "life cycle" OR "risk-based maintenance")) AND PY=(2010-2026)
\`\`\`

### W4 — gestão de ativos e ciclo de vida

\`\`\`text
TS=(("building asset management" OR "facility management" OR "facilities management" OR "building maintenance" OR "building operation" OR "operation and maintenance") AND ("life cycle" OR "life-cycle" OR "whole life cost" OR "life cycle cost" OR "service life" OR durability OR "building performance" OR "asset performance") AND (sustainab* OR "environmental performance" OR "sustainability assessment")) AND PY=(2010-2026)
\`\`\`

## 4. Crossref

Parâmetros documentados:

- Endpoint: `https://api.crossref.org/works`
- Modelo: `query.bibliographic`
- Filtro: `from-pub-date:2010-01-01,until-pub-date:2026-12-31`
- Paginação: 100 registros
- Limite deliberado: 200 registros por consulta
- Ordenação: relevância fornecida pelo Crossref
- Filtros de idioma: não localizados no script
- Filtros de tipo documental: não localizados no script

| ID | Consulta literal | Correspondências informadas | Exportados |
|---|---|---:|---:|
| C1 | `building maintenance sustainability` | 1.020.726 | 200 |
| C2 | `facility management sustainability building` | 3.978.326 | 200 |
| C3 | `maintenance prioritization public buildings sustainability` | 1.872.263 | 200 |
| C4 | `university campus building maintenance sustainability` | 3.127.639 | 200 |
| C5 | `building asset management life cycle sustainability` | 5.202.498 | 200 |

Total Crossref: 1.000 registros. Por causa do limite e da ordenação por relevância, o resultado é complementar e não exaustivo.

## 5. Informações ausentes

| Elemento | Situação |
|---|---|
| Strings literais da Web of Science | Preservadas; associação individual aos RIS informada de memória. |
| Datas de exportação | Mesmas datas das execuções: 08/07/2026. |
| Filtros de idioma | Não aplicados. |
| Filtros de tipo documental | Não aplicados. |
| Busca piloto | Não houve. |
| Estudos-semente | Não foram utilizados. |
| Marco inicial de 2010 | Adotado para mapear o desenvolvimento do tema desde o início da década de 2010 até a data da busca. |
| Reconciliação do total bruto | +5 Scopus no enriquecimento manual de 09/07/2026; +1 Web of Science por correção da contagem de A4. |

## 6. Avaliação da reprodutibilidade

| Base | Avaliação | Fundamentação |
|---|---|---|
| Scopus | Alta quanto à consulta e ao script; dependente de acesso à API e do estado temporal do índice | Strings, campo, período, paginação e tratamento da janela estão documentados. |
| Web of Science | Moderada | Strings, campo, período, data e ausência de filtros estão documentados; associação individual aos RIS foi informada de memória. |
| Crossref | Alta quanto ao procedimento limitado; não exaustiva | Consultas, filtro temporal, paginação e limite estão documentados; resultados variam com relevância e atualização do índice. |
| Conjunto | Moderada | As consultas e a reconciliação dos 12.118 registros estão documentadas; permanece a ressalva de associação individual dos RIS da Web of Science. |
