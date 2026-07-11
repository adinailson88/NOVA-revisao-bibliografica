# Codebook de categorias — dimensões, critérios, métodos e contextos

## 1. Natureza deste documento

Este codebook é o produto da Etapa 8 (`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`, seção 14). Ele
audita retrospectivamente as categorias já utilizadas na extração do núcleo final de 104 estudos
(`latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv`) e formaliza, para cada categoria,
uma definição, regra de inclusão, regra de exclusão, exemplo positivo, exemplo negativo e regra de
desempate para casos ambíguos.

A extração original das colunas `dimensoes_sustentabilidade_identificadas_leitura`,
`criterios_identificados_leitura`, `metodos_decisao_identificados_leitura` e
`contexto_edificacao_identificado_leitura` foi realizada por leitura individual de título, resumo,
palavras-chave e campos estruturados de cada um dos 104 estudos (Etapa 6/auditoria qualitativa),
sem leitura de texto completo. As instruções detalhadas fornecidas ao avaliador nessa leitura
individual (o "roteiro" referenciado como fonte das definições em
`latex-artigo/fontes/dicionario_criterio_dimensao_etapa17.csv`) não constituem um arquivo
preservado neste repositório. Por isso, este codebook reconstrói as definições operacionais a
partir de três fontes verificáveis: (a) as justificativas já registradas em
`dicionario_criterio_dimensao_etapa17.csv`; (b) o padrão observado nos próprios rótulos aplicados
aos 104 estudos; e (c) os exemplos reais extraídos das tabelas derivadas
(`tabela26` a `tabela29`). Onde a reconstrução não permite recuperar a regra original com
segurança, o campo correspondente é marcado como **Informação insuficiente para verificar**.

Este codebook não altera nenhuma codificação já atribuída aos 104 estudos. Ele formaliza, para uso
futuro (Etapa 9 em diante) e para auditoria externa, os critérios que já estavam implícitos nos
dados.

---

## 2. Dimensões de sustentabilidade (categorias-guarda-chuva)

A Tabela "Dimensões de sustentabilidade identificadas no núcleo final" (`tab:` em
`05_criterios.tex`) reporta apenas seis dimensões-guarda-chuva. A coluna bruta
`dimensoes_sustentabilidade_identificadas_leitura`, no entanto, contém dez rótulos distintos:
além dos seis abaixo, também ocorrem `conforto`, `energia`, `risco` e `seguranca` — os mesmos
quatro rótulos que também existem como **critérios** (Seção 3). O script
`scripts/r/10_gerar_produtos_artigo.R` já restringe a Tabela27/Gráfico de dimensões aos seis
rótulos canônicos (`dimensoes_canonicas`), mas essa restrição não estava explicada na prosa do
artigo antes desta etapa (ver Seção 6, "Problemas identificados").

| Categoria | Definição | Inclusão | Exclusão | Exemplo positivo | Exemplo negativo | Regra de desempate |
|---|---|---|---|---|---|---|
| `tecnica_operacional` | Atributos de desempenho físico, funcional e operacional do ativo predial (condição, vida útil, manutenibilidade, desempenho). | Título/resumo menciona desempenho operacional, condição física, vida útil ou manutenibilidade como foco do estudo. | Menção isolada a "operação" sem relação com desempenho ou condição do ativo predial. | REG_00110 (desempenho operacional e informação/dados como foco central). | Estudo sobre operação de rede elétrica sem relação com edificações (já excluído no funil por critério de objeto predial). | Quando o texto trata de "risco" técnico (falha, degradação), classificar como técnica-operacional, não institucional (ver Seção 3, critério `risco`). |
| `institucional` | Governança, conformidade, capacidade de gestão, informação/dados como suporte à decisão institucional. | Menção a governança, gestão de ativos, capacidade institucional, informação/dados aplicada à tomada de decisão. | Menção a "instituição" apenas como tipo de organização financiadora, sem relação com governança predial. | REG_00110 (informação e dados como critério institucional de apoio à gestão). | Menção a "instituição financeira" em contexto de financiamento de obra, sem relação com governança predial. | Termos de risco jurídico/regulatório (conformidade, compliance) são institucionais; risco físico/operacional é técnica-operacional. |
| `ambiental` | Impactos ambientais: energia, emissões, resíduos, água, adaptação climática. | Menção a consumo energético, emissões de carbono, gestão de resíduos, consumo de água ou impacto ambiental do ativo. | Menção a "ambiente" no sentido de ambiente organizacional ou ambiente de negócios, sem relação com impacto ecológico. | REG_00415 (dimensão ambiental associada a critérios de sustentabilidade). | Estudo sobre "clima organizacional" (sem relação com clima físico/energia). | Quando "energia" aparece como critério de priorização (Seção 3), a dimensão ambiental correspondente só é marcada se o resumo tratar energia como atributo de sustentabilidade, não apenas como custo operacional isolado. |
| `ciclo_de_vida` | Abordagem que integra fases de projeto, construção, operação e manutenção ao longo do tempo, incluindo custo de ciclo de vida (LCC). | Menção explícita a ciclo de vida, LCC, ou análise que integra múltiplas fases temporais do ativo. | Menção a "vida útil" isolada, sem referência a integração de fases ou custo ao longo do tempo (nesse caso, classificar apenas como critério `vida_util`, Seção 3). | REG_00110 (ciclo de vida como dimensão explícita). | Estudo que menciona apenas "idade do edifício" sem tratamento de ciclo de vida como abordagem. | Vida útil isolada é critério; ciclo de vida como abordagem metodológica é dimensão. |
| `economica` | Custos de construção, operação, manutenção e ciclo de vida; viabilidade financeira. | Menção a custo, orçamento, viabilidade econômica, retorno de investimento. | Menção a "valor" no sentido de valor arquitetônico/patrimonial, sem relação com custo financeiro. | REG_00110 (custo como critério econômico). | Estudo sobre "valor histórico" de edificação patrimonial sem análise de custo. | Custo de manutenção/reparo é econômico; custo de oportunidade institucional (ex.: continuidade de serviço) é institucional. |
| `social` | Conforto, segurança, satisfação dos usuários, acessibilidade, efeitos sobre grupos de usuários. | Menção a conforto, segurança dos ocupantes, satisfação do usuário, acessibilidade, equidade. | Menção a "segurança" no sentido de segurança de dados/cibersegurança, sem relação com usuários da edificação. | REG_00217 (dimensão social explícita). | Estudo sobre segurança cibernética de sistemas prediais, sem menção a conforto ou satisfação de ocupantes. | Segurança física de ocupantes é social; segurança estrutural/operacional é técnica-operacional (ver Seção 3, critério `seguranca`). |

---

## 3. Critérios de priorização

| Categoria | Definição | Inclusão | Exclusão | Exemplo positivo | Exemplo negativo | Regra de desempate |
|---|---|---|---|---|---|---|
| `desempenho_operacional` | Indicador de quanto o ativo cumpre sua função pretendida. | Menção a desempenho, eficiência operacional, indicadores de performance. | Menção a "desempenho financeiro" da empresa, sem relação com o ativo predial. | REG_00110 (93 registros no total). | Estudo sobre desempenho de mercado imobiliário sem análise do ativo em si. | — |
| `informacao_dados` | Uso de dados, sensores, BIM ou sistemas de informação para subsidiar decisão. | Menção a dados, informação, monitoramento, sistemas de informação predial. | Menção a "dados" no sentido genérico de dados de pesquisa (metodologia do próprio estudo), sem relação com dados do ativo predial. | REG_00110 (76 registros no total). | Estudo cuja metodologia usa "dados de survey" sem relação com dados operacionais do ativo. | — |
| `custo` | Custo de construção, operação, manutenção, reparo ou ciclo de vida. | Menção a custo, orçamento, gasto, investimento relacionado ao ativo predial. | Menção a "custo de oportunidade" institucional genérico sem valor monetário predial. | REG_01104 (59 registros no total). | Estudo sobre custo de programas educacionais sem relação com manutenção predial. | — |
| `vida_util` | Tempo de vida esperado ou remanescente do ativo ou de seus componentes. | Menção a vida útil, expectativa de vida, idade do ativo. | Menção a "vida útil de bateria" ou de equipamento não predial. | REG_00110 (40 registros no total). | Estudo sobre vida útil de equipamento médico isolado. | — |
| `energia` | Consumo, eficiência ou geração de energia associada ao ativo predial. | Menção a consumo energético, eficiência energética, energia renovável aplicada ao edifício. | Menção a "energia" no sentido figurado (energia organizacional, energia social). | REG_00489 (36 registros no total). | Menção a política energética nacional sem relação com o ativo predial específico. | — |
| `risco` | Probabilidade de falha, degradação ou evento adverso associado ao ativo. | Menção a risco de falha, risco estrutural, risco de degradação, gestão de risco predial. | Menção a risco jurídico/regulatório puro, sem relação com condição física do ativo (nesse caso, considerar dimensão institucional). | REG_00110 (31 registros no total). | Menção a risco de mercado financeiro sem relação com o ativo predial. | Ambiguidade documentada em `dicionario_criterio_dimensao_etapa17.csv`: quando o resumo não permite diferenciar risco técnico de risco institucional, adotou-se leitura conservadora técnico-operacional. |
| `condicao_fisica` | Estado de conservação, deterioração ou integridade física dos componentes. | Menção a condição, deterioração, estado de conservação. | Menção a "condições de trabalho" (segurança ocupacional), sem relação com condição física do ativo. | REG_00852 (27 registros no total). | Estudo sobre condições trabalhistas de operários de manutenção, sem avaliação de condição do ativo. | — |
| `manutenibilidade` | Facilidade e custo de manter, reparar ou substituir componentes. | Menção a manutenibilidade, facilidade de manutenção, acessibilidade para reparo. | Menção a "manutenção" genérica sem qualificação de facilidade/dificuldade. | REG_00852 (19 registros no total). | Estudo que apenas relata a existência de um plano de manutenção, sem discutir manutenibilidade do projeto. | — |
| `conforto` | Conforto térmico, acústico, visual ou olfativo dos ocupantes. | Menção a conforto térmico, qualidade do ar interno, conforto acústico/visual. | Menção a "conforto" no sentido de conveniência administrativa. | REG_01104 (17 registros no total). | Estudo sobre conveniência de agendamento de serviços de manutenção. | — |
| `seguranca` | Segurança física dos ocupantes e do patrimônio. | Menção a segurança contra incêndio, segurança estrutural, segurança de uso. | Menção a segurança cibernética/de dados sem relação com segurança física dos ocupantes. | REG_02635 (17 registros no total). | Estudo sobre segurança de rede de sensores IoT sem relação com segurança física predial. | — |
| `emissoes_carbono` | Emissões de gases de efeito estufa associadas ao ativo. | Menção a emissões de carbono, pegada de carbono, neutralidade de carbono. | Menção a "emissões" de poluentes industriais não relacionados a edificações. | REG_00888 (15 registros no total). | Estudo sobre emissões industriais de fábrica, sem relação com edificação. | — |
| `residuos` | Geração, gestão ou reciclagem de resíduos associados ao ativo. | Menção a resíduos de construção, resíduos operacionais, reciclagem. | Menção a "resíduos" químicos industriais não prediais. | REG_03383 (13 registros no total). | Estudo sobre gestão de resíduos hospitalares clínicos, sem relação com manutenção predial. | — |
| `satisfacao_usuario` | Percepção e satisfação dos usuários/ocupantes com o ativo. | Menção a satisfação, percepção dos usuários, experiência do ocupante. | Menção a "satisfação do cliente" em sentido comercial genérico, sem relação com ocupação predial. | REG_02540 (nove registros no total). | Estudo de satisfação de clientes de serviço de manutenção terceirizado, sem relação com percepção sobre o ativo em si. | — |
| `qualidade_servico` | Qualidade dos serviços de operação e manutenção prestados. | Menção a qualidade de serviço, nível de serviço, SLA de manutenção. | Menção a "qualidade" de material de construção (nesse caso, considerar condição física). | REG_00110 (seis registros no total). | Estudo sobre qualidade de concreto, sem relação com prestação de serviço de manutenção. | Qualidade de serviço foi mapeada como técnica-operacional (não institucional) por não haver item de "qualidade" na lista de dimensão institucional do roteiro original (`dicionario_criterio_dimensao_etapa17.csv`). |
| `agua` | Consumo, eficiência ou gestão de água associada ao ativo. | Menção a consumo de água, eficiência hídrica, reuso de água. | Menção a "água" em contexto de infraestrutura hídrica urbana não predial (já excluída no funil por critério de objeto predial). | REG_04122 (cinco registros no total). | Estudo sobre tratamento de água em estação de tratamento municipal. | — |

---

## 4. Métodos de apoio à decisão

Dividem-se em dois grupos já usados no artigo (`06_metodos.tex`, Gráfico de métodos): abordagens e
instrumentos gerais, e métodos formalmente nomeados (multicritério ou correlatos).

| Categoria | Definição | Inclusão | Exclusão | Exemplo positivo | Regra de desempate |
|---|---|---|---|---|---|
| `framework` (geral) | Estrutura conceitual ou operacional proposta pelo estudo, sem instrumento formal nomeado. | Uso do termo "framework" ou estrutura equivalente para organizar critérios/decisão. | Uso de "framework" apenas como sinônimo de "artigo" ou "estudo", sem função estruturante. | 96 registros no total; ver `tabela28`. | Quando o estudo usa framework E um método formal nomeado (ex.: AHP), ambos são registrados (respostas múltiplas). |
| `decision support` (geral) | Sistema ou abordagem de apoio à decisão sem método formal nomeado. | Menção a "decision support system" ou apoio à decisão sem detalhamento do algoritmo. | Menção a "decisão" administrativa genérica sem relação com apoio técnico à priorização. | 26 registros no total. | — |
| `BIM` (geral) | Uso de modelagem de informação da construção como base de dados/decisão. | Menção a BIM, Building Information Modeling. | Menção a "modelo" genérico sem uso de BIM. | 26 registros no total. | — |
| `optimization` (geral) | Uso de técnicas de otimização matemática (programação linear, algoritmos genéticos etc.). | Menção a otimização, minimização/maximização de função objetivo. | Menção a "otimizar" em sentido coloquial, sem técnica formal. | 18 registros no total. | — |
| `scoring` (geral) | Sistemas de pontuação para comparar alternativas. | Menção a scoring, sistema de pontos, índice composto. | Menção a "nota" de avaliação qualitativa sem sistema formal. | 17 registros no total. | — |
| `life-cycle cost` (geral) | Modelo de custo de ciclo de vida (LCC) como instrumento de decisão. | Menção a LCC, custo de ciclo de vida como método de cálculo. | Menção a "custo" isolado sem modelo de ciclo de vida (nesse caso, apenas critério `custo`). | 13 registros no total. | — |
| `fuzzy` (geral) | Uso de lógica fuzzy/difusa em qualquer etapa da decisão. | Menção a fuzzy, lógica difusa. | — | 10 registros no total. | Geralmente combinado com outro método (ex.: ANP fuzzy); ambos são registrados. |
| `ranking` (geral) | Ordenação de alternativas sem método formal nomeado. | Menção a ranking, ordenação, classificação comparativa. | Menção a "ranking" de mercado imobiliário sem relação com priorização de manutenção. | 10 registros no total. | — |
| `IoT` (geral) | Uso de Internet das Coisas para coleta de dados prediais. | Menção a IoT, sensores conectados, monitoramento remoto. | Menção a "conectividade" genérica sem sensoriamento predial. | Nove registros no total. | — |
| `machine learning` (geral) | Uso de aprendizado de máquina para previsão ou classificação. | Menção a machine learning, redes neurais, algoritmos preditivos. | Menção a "inteligência artificial" genérica sem técnica de ML especificada. | Nove registros no total. | — |
| `digital twin` (geral) | Uso de gêmeo digital como plataforma de decisão/monitoramento. | Menção a digital twin, gêmeo digital. | Menção a "modelo digital" genérico sem sincronização com o ativo físico. | Oito registros no total. | — |
| `AHP` (estruturado) | Analytic Hierarchy Process. | Menção explícita a AHP. | — | Cinco registros no total. | — |
| `TOPSIS` (estruturado) | Technique for Order of Preference by Similarity to Ideal Solution. | Menção explícita a TOPSIS. | — | Quatro registros no total. | — |
| `ANP` (estruturado) | Analytic Network Process. | Menção explícita a ANP. | — | Três registros no total. | — |
| `MCDM` (estruturado) | Rótulo genérico de método multicritério formal, sem instrumento específico nomeado. | Menção a MCDM/MCDA sem AHP/TOPSIS/ANP específicos. | Menção a "multicritério" apenas como qualificador do problema, sem método aplicado. | Três registros no total. | Se o estudo nomeia um método específico (AHP, TOPSIS etc.), registrar o método específico; MCDM é usado apenas quando o resumo não especifica. |
| `Delphi` (estruturado) | Método Delphi (painel de especialistas, rodadas iterativas). | Menção explícita a Delphi. | — | Três registros no total. | — |
| `Bayesian Best Worst Method` (estruturado) | Método Best-Worst bayesiano de ponderação de critérios. | Menção explícita ao método. | — | Um registro no total (REG_05338). | — |
| `balanced scorecard` (estruturado) | Balanced Scorecard como instrumento de gestão/priorização. | Menção explícita ao método. | — | Um registro no total (REG_00110). | — |
| `case-based reasoning` (estruturado) | Raciocínio baseado em casos anteriores. | Menção explícita ao método. | — | Um registro no total (REG_04052). | — |

---

## 5. Contextos de edificação

| Categoria | Definição | Inclusão | Exclusão | Exemplo positivo | Regra de desempate |
|---|---|---|---|---|---|
| `edificio_generico` | Edificação sem tipologia específica declarada, ou "building" genérico. | Resumo trata de edificações em geral, sem especificar tipologia. | Resumo especifica tipologia (nesse caso, usar a categoria específica, além de `edificio_generico` se ambos aparecerem). | 93 registros no total. | Respostas múltiplas: um estudo pode ser genérico E também mencionar portfólio. |
| `portfolio_predial` | Conjunto/carteira de edificações geridas de forma agregada. | Menção a portfólio, carteira de ativos, múltiplos edifícios sob gestão comum. | Menção a "portfólio" financeiro sem relação com ativos prediais. | 58 registros no total. | — |
| `hospital` | Edificação ou instalação de saúde. | Menção a hospital, unidade de saúde, healthcare building. | Menção a "saúde" no sentido de saúde estrutural do edifício (expressão idiomática), sem relação com uso hospitalar. | 17 registros no total. | — |
| `edificio_comercial` | Edificação de uso comercial (escritórios, varejo, hotéis). | Menção a edifício comercial, escritório, hotel, shopping. | — | 16 registros no total. | — |
| `edificio_residencial` | Edificação de uso habitacional. | Menção a edifício residencial, habitação, moradia. | — | 12 registros no total. | — |
| `universidade` | Edificação ou campus universitário. | Menção explícita a universidade, ensino superior. | Menção a "escola" sem nível superior (nesse caso, usar `escola`). | 11 registros no total. | — |
| `campus` | Contexto de campus (conjunto de edificações de uma instituição). | Menção a campus, sem necessariamente especificar nível de ensino. | — | 10 registros no total. | Pode coocorrer com `universidade` ou `escola` (respostas múltiplas). |
| `edificio_publico` | Edificação de propriedade ou gestão pública, fora do contexto educacional. | Menção a edifício público, governamental, sem ser hospital/escola/universidade. | — | Cinco registros no total. | — |
| `escola` | Edificação de ensino básico ou técnico, fora do nível superior. | Menção a escola, ensino básico/técnico. | Menção a "escola de pensamento" (uso metafórico). | Cinco registros no total. | — |
| `patrimonio_historico` | Edificação de valor histórico ou patrimonial. | Menção a patrimônio histórico, edificação tombada, conservação patrimonial. | — | Quatro registros no total. | — |
| `nao_identificado_no_resumo` | Resumo não permite identificar tipologia de edificação. | Ausência de qualquer termo de contexto no resumo. | — | Um registro no total (REG_05379). | Usado apenas quando nenhuma outra categoria de contexto se aplica. |

---

## 6. Problemas identificados nesta auditoria

1. **Filtragem não documentada na prosa (dimensões vs. critérios).** A coluna bruta
   `dimensoes_sustentabilidade_identificadas_leitura` contém dez rótulos, mas a Tabela27 e o
   Gráfico de dimensões (`05_criterios.tex`) reportam apenas os seis rótulos canônicos, via
   filtro já existente em `scripts/r/10_gerar_produtos_artigo.R`
   (`dimensoes_canonicas`). Essa restrição é metodologicamente razoável — evita duplicar, como
   "dimensão", rótulos que já são tratados como critérios de priorização (Seção 3) — mas não
   estava explicada na prosa do artigo antes desta etapa. Corrigido nesta etapa com uma frase
   em `03_metodologia.tex` (ver Seção 7).

2. **Inconsistência de grafia em três rótulos de método, causando exclusão silenciosa da
   figura.** Em `scripts/r/10_gerar_produtos_artigo.R`, o vetor `metodos_estruturados` usa os
   rótulos `"Balanced scorecard"`, `"Case-based reasoning"` e `"Bayesian Best-Worst Method"`
   (com maiúsculas/hífen), enquanto os rótulos efetivamente gravados em
   `criterios_identificados_leitura`/`metodos_decisao_identificados_leitura` do núcleo final são
   `"balanced scorecard"`, `"case-based reasoning"` e `"Bayesian Best Worst Method"` (sem hífen).
   Como o filtro de `dados_metodos_grafico` exige correspondência exata de string, esses três
   métodos (um registro cada: REG_00110, REG_04052 e REG_05338) ficam de fora da
   Figura "Abordagens e métodos de apoio à decisão identificados no núcleo final"
   (`figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png`), embora estejam corretamente
   contabilizados em `tabela28_metodos_decisao_nucleo_final_104.csv`. A tabela bruta está
   correta; apenas a figura e, por decorrência, a enumeração em prosa de `06_metodos.tex`
   omitiam esses três métodos. Corrigido nesta etapa no script (ver Seção 7) e na prosa do
   artigo; a regeneração da figura em si permanece pendente (ver Seção 8).

3. **Campo `tipo_contribuicao_artigo` subutilizado.** A coluna registra dez categorias de
   contribuição por estudo, mas apenas a categoria `lacuna_para_ies_publicas` é usada em uma
   tabela derivada (`tabela30`). As demais nove categorias (`contexto_publico_universitario`,
   `criterios_de_priorizacao`, `criterios_de_sustentabilidade`, `custo_ciclo_de_vida`,
   `energia_desempenho_operacional`, `facility_management`, `gestao_manutencao_predial`,
   `metodo_multicriterio_ou_decisao`, `risco_seguranca_conforto`) não geram tabela ou figura
   própria. Isso não é um erro — os dados dessas categorias são, em grande parte, redundantes
   com as tabelas de critérios/dimensões/métodos já existentes —, mas é registrado aqui como
   observação de auditoria, sem alteração proposta nesta etapa.

## 7. Alterações realizadas no artigo e nos scripts

- `scripts/r/10_gerar_produtos_artigo.R`: corrigida a grafia de três rótulos no vetor
  `metodos_estruturados` (`"balanced scorecard"`, `"case-based reasoning"`,
  `"Bayesian Best Worst Method"`), para corresponder exatamente aos rótulos gravados no núcleo
  final. Nenhum dado do núcleo de 104 estudos foi alterado; apenas a lógica de geração da figura.
- `latex-artigo/sections/03_metodologia.tex`: acrescentada uma frase, ao final do último
  parágrafo, esclarecendo a distinção entre dimensão (categoria-guarda-chuva) e critério
  (atributo operacional específico), e referenciando este codebook.
- `latex-artigo/sections/06_metodos.tex`: a enumeração de métodos formalmente nomeados foi
  completada para incluir Delphi, balanced scorecard e raciocínio baseado em casos (um registro
  cada), com base nos dados corretos de `tabela28_metodos_decisao_nucleo_final_104.csv`.

## 8. Pendência de regeneração de figura

A correção do script (Seção 7) altera a lógica de geração de
`figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png`, mas o ambiente desta sessão não
possui interpretador R instalado (`Rscript` não encontrado). A regeneração efetiva do arquivo PNG
com `Rscript scripts/r/10_gerar_produtos_artigo.R` é responsabilidade do pesquisador, em ambiente
local com R e os pacotes `readr`, `dplyr`, `tidyr`, `stringr`, `ggplot2` e `scales` instalados.
Até a regeneração, a figura publicada no artigo permanece a anterior à correção (sem os três
métodos de um registro cada); a tabela numérica (`tabela28`) e a prosa de `06_metodos.tex` já
estão corretas.
