# Relatório final da revisão metodológica e textual do artigo

## 1. Estado final

As Etapas 0 a 16 foram concluídas na branch `revisao-metodologica-controlada`. A versão de origem permanece preservada no commit `e10ef825e6a560f19ffc12306d55b142b3c360e3` e na branch `preservacao-original-revisao-metodologica-20260710`.

No ponto de comparação anterior à consolidação, a branch estava 63 commits à frente da origem, com 168 arquivos alterados ou adicionados. A comparação registrou 149 arquivos novos e 19 modificados, incluindo protocolos, produtos intermediários, codebooks, relatórios, scripts, tabelas, figuras e o artigo.

## 2. Síntese das etapas

- Etapa 0: inventário, preservação e rastreabilidade inicial.
- Etapa 1: classificação como revisão integrativa sistematizada, com apoio bibliométrico e síntese temática.
- Etapa 2: alinhamento entre pergunta, RQs, seleção, extração e resultados.
- Etapa 3: documentação de Scopus, Web of Science e Crossref, período 2010-2026 e 13 consultas.
- Etapa 4: reconciliação do funil 12.118, 9.542, 3.678, 137 e 104.
- Etapa 5: especificação da deduplicação e preservação da proveniência.
- Etapa 6: separação das camadas de triagem, automação, auditoria e decisão.
- Etapa 7: adoção da Rota A, com síntese predominantemente documental.
- Etapa 8: codebook de dimensões, critérios, métodos e contextos.
- Etapa 9: tipologia documental dos desenhos, sem aplicação indevida de instrumentos clínicos.
- Etapa 10: auditoria numérica e qualificação de categorias amplas e coocorrências.
- Etapa 11: criação de discussão autônoma e integrada.
- Etapa 12: delimitação da matriz como conceitual, sem pesos ou validação.
- Etapa 13: atualização das limitações conforme o método real.
- Etapa 14: padronização de siglas, termos e redação.
- Etapa 15: uso delimitado de Hu et al. (2026) como parâmetro de transparência do relato.
- Etapa 16: consolidação, comparação e validação final.

## 3. Texto completo pontual

Duas tarefas extraordinárias examinaram 30 estudos com PDF disponível. Quatorze estudos forneceram evidências específicas incorporadas com citações individualizadas. Os demais foram confirmatórios, tangenciais ou apresentaram divergências documentadas.

O segundo lote de 11 estudos gerou o relatório `docs/RELATORIO_USO_TEXTO_COMPLETO_11_NOVOS_ESTUDOS.md`. Sete foram incorporados. Os metadados de Yoon e Cha, Chew e Conejos e Tan, Zaman e Sutrisna foram completados. Os DOIs do mapa de Chew e de Hassanizadeh e Noorzai foram corrigidos.

Nenhum PDF protegido foi versionado.

## 4. Mudanças metodológicas

Não houve criação retrospectiva de procedimentos. Foram explicitados:

- avaliador único e ausência de concordância interavaliadores;
- ausência de pré-registro;
- ausência de elegibilidade integral em texto completo;
- regras determinísticas e auditoria amostral;
- Crossref como fonte complementar;
- diferença entre registro, estudo, frequência, aplicação e evidência;
- ausência de avaliação formal de qualidade e risco de viés;
- caráter conceitual e não validado da matriz.

## 5. Mudanças textuais e estruturais

- resumo e abstract alinhados ao método real;
- siglas e termos estrangeiros padronizados;
- seção autônoma de discussão;
- limitações reescritas;
- matriz renomeada e delimitada;
- referências de texto completo e referência metodológica verificadas;
- referências cruzadas, legendas e numeração preservadas.

## 6. Resultados preservados

Foram mantidos os totais centrais:

- 12.118 registros brutos;
- 9.542 registros únicos;
- 3.678 registros reavaliados;
- 137 registros centrais;
- 104 registros no núcleo final.

A leitura pontual de texto completo não alterou tabelas, frequências, percentuais ou coocorrências agregadas.

## 7. Validações finais

O workflow nº 74 concluiu com sucesso:

- geração das tabelas e figuras em R;
- execução de `python scripts/python/verificar_artigo.py`;
- consistência de citações e bibliografia;
- compilação LaTeX;
- ausência de `Overfull hbox`;
- geração do PDF;
- publicação do artefato.

PDF final validado antes da consolidação documental: blob `e259dede10d780a5ff0fe06729da6672f79bce62`.

## 8. Arquivos centrais

- `latex-artigo/main.tex`
- `latex-artigo/references.bib`
- `latex-artigo/sections/`
- `latex-artigo/fontes/`
- `latex-artigo/figuras/`
- `scripts/python/verificar_artigo.py`
- `scripts/r/10_gerar_produtos_artigo.R`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`
- relatórios das Etapas 1 a 15 e relatórios de texto completo.

## 9. Limitações remanescentes

- 74 registros do núcleo não foram lidos integralmente.
- Não houve avaliação formal de qualidade metodológica ou risco de viés.
- Não houve segundo avaliador independente.
- A matriz não possui pesos, indicadores operacionais, análise de sensibilidade ou validação empírica.
- Algumas divergências individuais de codificação identificadas nos lotes de texto completo permanecem documentadas, sem recálculo agregado.
- A associação individual entre arquivos RIS e strings da Web of Science foi informada de memória.
- O ano de 2026 é parcial.

Esses itens são limitações declaradas, não pendências técnicas ocultas.

## 10. Recomendações não executadas

- Rota B com elegibilidade integral dos 104 estudos;
- aplicação de instrumentos de avaliação metodológica compatíveis por desenho;
- recodificação individual e regeneração dos agregados;
- validação empírica da matriz em instituições públicas universitárias;
- merge da branch na `main`.

## 11. Reprodutibilidade

A reprodução utiliza os scripts, fontes CSV, produtos processados, codebooks e workflow versionados. O comando de verificação é:

`python scripts/python/verificar_artigo.py`

A geração de produtos utiliza:

`Rscript scripts/r/10_gerar_produtos_artigo.R`

A compilação utiliza `latexmk` e `biber`, conforme `.github/workflows/latex.yml`.

## 12. Conclusão

O artigo está consolidado na branch de trabalho, com método, resultados, discussão, matriz, limitações, redação e referências validados. Não há pendência técnica bloqueante. A única ação de integração externa não realizada é o merge na `main`.
