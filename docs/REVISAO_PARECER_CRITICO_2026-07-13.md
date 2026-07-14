# Revisão do parecer crítico — 13/07/2026

## Escopo

Revisão integral dos pontos apresentados no parecer crítico sobre o artigo, com correções textuais, metodológicas e de rastreabilidade executadas em branch própria.

## Plano de execução

1. Conferir cada crítica contra o texto e os arquivos geradores.
2. Quantificar a relação entre o estrato bibliométrico de 372 registros e o núcleo temático vigente de 121.
3. Corrigir arquitetura argumentativa, terminologia, rastreabilidade e assertivas sem sustentação suficiente.
4. Reenquadrar o produto como especificação operacional candidata à parametrização multicritério, sem alegar protocolo decisório validado.
5. Diferenciar, na matriz, evidência derivada da revisão e proposição autoral.
6. Reduzir redundâncias da RQ6, das ressalvas epistêmicas e do agrupamento repetido de citações.
7. Corrigir RQ5, siglas, traduções, singular/plural, métricas e periodicidades.
8. Atualizar verificadores automatizados para impedir regressão dos pontos críticos.
9. Validar dados, citações, estrutura, PDF e Word antes de encerrar a revisão.

## Registro de execução

- [x] Parecer recebido e convertido em lista de verificação.
- [x] Branch `agent/revisao-parecer-critico` criada a partir do `main` no commit `ee00030`.
- [x] PR nº 5 aberto para preservar a versão estável da `main` durante a revisão.
- [x] Conferência do resumo, introdução, fundamentos teóricos, metodologia, resultados, discussão, limitações, considerações e workflow.
- [x] Confirmada e corrigida a ausência de declaração explícita da interseção 372 × 121.
- [x] Interseção calculada por script: 109 registros comuns; 263 exclusivos da camada bibliométrica; 12 exclusivos do núcleo temático.
- [x] Resultado preservado em `latex-artigo/fontes/intersecao_camadas_372_121.csv` e regenerado pelo verificador integrado.
- [x] Tabela-glossário inserida para distinguir os conjuntos de 3.678, 372, 137, 104 e 121 registros.
- [x] Transição dos 314 casos iniciais para os 4.276 casos de dúvida explicitada sem dupla contagem.
- [x] Funil da RQ6 completado na Metodologia: 20 candidatos, oito exclusões, 12 novos registros e cinco promoções.
- [x] Título, resumo e introdução reenquadrados: contribuição central definida como especificação operacional para futura parametrização multicritério.
- [x] Bibliometria, síntese temática e RQ6 subordinadas como camadas de evidência, sem competir com a contribuição central.
- [x] Ordem dos resultados corrigida: panorama do núcleo temático antes da estrutura bibliométrica.
- [x] MCDM, MCDA, AHP, TOPSIS e ANP definidos no primeiro uso.
- [x] `facility management` padronizado como gestão de facilidades, com equivalência indicada na primeira ocorrência.
- [x] `decision support` identificado como rótulo do manual de codificação (`decision_support`).
- [x] Distinção entre plataformas informacionais e modelos treinados marcada como organização analítica do autor, com referências usadas como exemplos.
- [x] Métricas de custo do ciclo de vida e de custos operacionais anuais separadas em bases de cálculo distintas.
- [x] Resultado da RQ5 apresentado em Resultados: 12 registros (9,9%) classificados com lacuna específica para IES públicas.
- [x] Evidências de contextos africanos qualificadas geograficamente e não generalizadas automaticamente ao Brasil.
- [x] Matriz separada em duas camadas: evidências da revisão e proposição operacional do autor.
- [x] Fontes, periodicidades, unidades e direções dos indicadores explicitadas como proposições autorais para validação.
- [x] Referência específica ao SINAPI retirada da tabela por ausência de derivação direta na revisão.
- [x] Indicador energético corrigido para intensidade em base móvel de 12 meses com apuração mensal.
- [x] Pesos, normalização, função de agregação, limiares e vetos declarados como parâmetros ainda não definidos.
- [x] Agrupamento repetido de citações sobre MCDM concentrado na Seção de Métodos e substituído por remissões nas demais seções.
- [x] Discussão da RQ6 condensada para evitar desproporção em relação às RQ1–RQ5.
- [x] `Como proposição dos autores` corrigido para `Como proposição do autor`.
- [x] Verificador atualizado para exigir as correções do parecer e impedir regressão das formulações superadas.
- [x] Falhas encontradas durante a validação foram corrigidas na fonte: controle legado de tabelas, asserções da matriz, escapes LaTeX e expressões regulares do gerador Word e largura do cabeçalho da tabela-glossário.
- [x] Verificador integrado executado sem divergências de dados, texto, citações, referências, strings ou controles específicos do parecer.
- [x] PDF compilado integralmente em formato A4, sem erro e sem `Overfull hbox` na execução final.
- [x] Word gerado com as 12 tabelas e os fluxogramas, validado como pacote OOXML e reconvertido integralmente em PDF pelo LibreOffice.
- [x] Artefatos PDF e Word publicados pela execução nº 280 do workflow `Validar fontes e gerar artigo`.
- [x] Workflows e arquivos temporários de diagnóstico removidos após a validação.
- [x] Workflow permanente restaurado para executar a compilação completa na `main` ou manualmente, mantendo no PR a validação de dados, texto e referências.
- [x] Revisão final de coerência e rastreabilidade concluída; a execução nº 289 confirmou o estado limpo do PR sem divergências.
- [x] PR nº 5 integrado à `main` por squash no commit `b144951`.
- [x] Compilação definitiva da `main` concluída; o commit automático `554fc8f` atualizou `main.pdf`, `artigo.docx`, `site/artigo.pdf` e `site/artigo.docx`.
- [x] Hashes das cópias da raiz e do site conferidos: PDF `e4b4a2d630aa41a97f022d8b75493954029f153a`; Word `017815d348508d75354e7bcc4d51163ae3b87109`.

Este arquivo preserva o histórico verificável das alterações, dos erros encontrados durante a compilação e das respectivas correções.
