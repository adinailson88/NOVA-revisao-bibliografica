# Relatório da Etapa 10

## 1. Escopo executado

Foi auditada a consistência dos resultados do núcleo final de 104 registros: totais, percentuais, denominadores, respostas múltiplas, categorias exclusivas, séries anuais, bases, tipos documentais, dimensões, critérios, métodos, contextos, lacunas, ODS, ESG e coocorrências. A etapa permaneceu no nível documental definido nas etapas anteriores.

## 2. Arquivos analisados

Foram analisadas as seções 04 a 08 e 10 do artigo; o núcleo final de 104 registros; as tabelas derivadas 26 a 35; as matrizes de coocorrência; o script `scripts/r/10_gerar_produtos_artigo.R`; o verificador `scripts/python/verificar_artigo.py`; os codebooks das Etapas 8 e 9; e o status cumulativo.

## 3. Evidências encontradas

Os totais e percentuais conferem com denominador 104. A série anual soma 104, contém 88 registros entre 2019 e 2026 e apresenta máximo de 25 em 2025. As bases admitem respostas múltiplas e totalizam 98 registros com origem Scopus, 49 com origem Web of Science e seis com origem Crossref. Os tipos documentais são exclusivos e somam 104: 79 artigos, 15 trabalhos em evento e dez livros ou séries.

As frequências de dimensões, critérios, métodos, contextos, lacunas e menções a ODS/ESG coincidem entre núcleo, tabelas e texto. As matrizes 31 e 32 contam registros distintos por par de categorias.

## 4. Problemas identificados

Três categorias de frequência muito alta poderiam ser interpretadas de forma excessiva: `framework` (96), técnica-operacional (102) e edificação genérica (93). Elas são categorias documentais amplas e não comprovam aplicação metodológica, importância científica ou especialização tipológica.

As coocorrências representam codificações simultâneas no mesmo registro; não estimam associação estatística, efeito, causalidade, peso ou importância.

O arquivo derivado `tabela36_tipo_contribuicao_artigo_nucleo_final_104.csv` estava previsto no script, mas ainda não publicado devido à interrupção anterior do workflow no controle de margens.

## 5. Alterações realizadas

Foram qualificadas as interpretações nas seções de critérios, métodos, aplicabilidade e matriz. O verificador passou a conferir integralmente as séries numéricas centrais e a tabela de tipos de contribuição gerada pelo script. Nenhum registro foi recodificado e nenhum total foi modificado.

## 6. Alterações não realizadas

Não foram reestruturadas a discussão ou as considerações finais, não foram alteradas perguntas de pesquisa, não foram introduzidos novos métodos, não foram modificados gráficos manualmente e não foi antecipada a Etapa 11.

## 7. Informação insuficiente para verificar

A aplicação efetiva de cada método nos estudos sem texto completo: Informação insuficiente para verificar.

A importância científica relativa das categorias a partir de frequência documental: Informação insuficiente para verificar.

Associação causal ou efeito entre categorias a partir das coocorrências: Informação insuficiente para verificar.

## 8. Validações executadas

Foram confrontados núcleo, tabelas derivadas, texto e regras do script gerador. O verificador foi ampliado para impedir divergências futuras nos resultados auditados. A validação completa pelo GitHub Actions depende da execução disparada pelo commit desta etapa.

## 9. Arquivos alterados

- `latex-artigo/sections/05_criterios.tex`
- `latex-artigo/sections/06_metodos.tex`
- `latex-artigo/sections/07_aplicabilidade.tex`
- `latex-artigo/sections/08_matriz.tex`
- `scripts/python/verificar_artigo.py`
- `docs/RELATORIO_ETAPA_10.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Commit exclusivo da etapa com a mensagem `etapa-10: audita consistencia e interpretacao dos resultados`.

## 11. Pendências

Confirmar a conclusão do workflow, incluindo a regeneração e publicação dos produtos derivados e do PDF.

## 12. Próxima etapa prevista

Etapa 11 — Discussão, somente após autorização expressa.

Execução interrompida conforme o planejamento. Aguardando autorização expressa para prosseguir.
