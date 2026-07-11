# Relatório de uso pontual de texto completo dos 19 estudos com PDF disponível

Este relatório não corresponde a uma das etapas 0-16 de `docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`.
Trata-se de uma tarefa pontual, autorizada fora da sequência formal, para ler os 19 PDFs de
texto completo já obtidos para estudos do núcleo final (ver `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`,
seção "Atualização do subconjunto com texto completo obtido") e usá-los somente quando
agregassem algo relevante, sem alterar a natureza predominantemente documental do restante da
revisão. A Rota B (elevação a revisão sistemática de todos os 104 estudos) permanece não
autorizada.

## 1. Escopo executado

Leitura de texto completo dos 19 estudos mapeados com PDF disponível (nove obtidos por acesso
aberto via Unpaywall, dez localizados na biblioteca pessoal do pesquisador), comparando o
conteúdo integral com a codificação documental já registrada em
`latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv` para cada estudo (dimensões de
sustentabilidade, critérios de priorização, métodos de apoio à decisão, contexto de edificação,
lacunas). Incorporação, ao artigo, apenas dos achados que a leitura integral efetivamente
sustentou, nos pontos pertinentes das seções já revisadas na Etapa 7.

## 2. Arquivos analisados

- Os 19 PDFs listados no mapa de texto completo do subconjunto.
- `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv` (codificação documental de base).
- `latex-artigo/references.bib`.
- `latex-artigo/sections/03_metodologia.tex`, `04_panorama.tex`, `05_criterios.tex`,
  `06_metodos.tex`, `07_aplicabilidade.tex`, `08_matriz.tex`, `09_limitacoes.tex`,
  `10_consideracoes.tex`.

## 3. Evidências encontradas

Dos 19 estudos lidos em texto completo, sete continham conteúdo que refinava a codificação
documental de forma verificável e relevante para a síntese do artigo:

| id_unico | Achado do texto completo | Uso |
|---|---|---|
| REG_03359 | Revisão sistemática de 123 estudos sobre a evolução de BIM para gêmeos digitais; nenhum alcançou o nível considerado ideal de gêmeo digital. | Sim |
| REG_05430 | Modelo de informação de ativos baseado em ontologia para manutenção preditiva, com deslocamento de lógica de "falha corrigida" para "prevenção antecipada". | Sim |
| REG_06996 | Identifica a dimensão BIM 7D como etapa do modelo especificamente voltada à gestão de facilidades na operação e manutenção. | Sim |
| REG_08052 | Modelo estocástico com redes de Petri e simulação de Monte Carlo para comparar estratégias de manutenção de revestimentos cerâmicos. | Sim |
| REG_05650 | Estatística de que a operação e manutenção pode responder por mais de 80% do custo de ciclo de vida e 50-70% dos custos operacionais anuais. | Sim |
| REG_07476 | Estatística de que até 50% das dificuldades de manutenção poderiam ser evitadas com alterações no projeto na fase de concepção. | Sim |
| REG_08528 | Modelo conceitual articulando gestão sustentável de facilidades, resiliência institucional e ODS 4, 9 e 11 em instituições de ensino técnico-profissional. | Sim |

Os demais doze estudos foram lidos integralmente e a leitura confirmou, sem acrescentar
conteúdo narrativamente relevante e não redundante, a codificação já registrada a partir de
título/resumo/palavras-chave:

| id_unico | Observação da leitura de texto completo |
|---|---|
| REG_00519 | Confirma dimensões ambiental/social/institucional; estudo qualitativo sobre gestão de facilidades urbanas (escala de cidade, não predial isolada). Sem uso individual. |
| REG_01104 | Revisão técnica de ferramentas BIM de simulação de desempenho ambiental interno; o texto completo não sustenta, de forma distinguível, as dimensões econômica e institucional atribuídas na codificação por resumo. Divergência registrada apenas neste relatório; nenhuma tabela agregada foi alterada. |
| REG_02204 | Ferramenta educacional de simulação para ensino de projeto integrado sustentável; não é um método de apoio à decisão operacional de manutenção. A codificação "decision support" é mais ampla do que o conteúdo do texto completo sustenta. Divergência registrada apenas neste relatório; nenhuma tabela agregada foi alterada. |
| REG_02495 | Confirma a revisão de aplicações de gêmeos digitais para eficiência energética, incluindo manutenção como um dos quatro tópicos identificados. |
| REG_03176 | Estudo de caso de monitoramento pós-ocupação de um único edifício de exposição; o texto completo não evidencia uso do método ANP atribuído na codificação por resumo. Divergência registrada apenas neste relatório; nenhuma tabela agregada foi alterada. |
| REG_04163 | Confirma modelo de custo de ciclo de vida (LCC) para seleção de materiais construtivos, coerente com a codificação por resumo. |
| REG_05142 | Confirma revisão sistemática sobre quantificação do valor de investimento em BIM, coerente com a codificação por resumo. |
| REG_05283 | Confirma contexto hospitalar e dimensões econômica/social/institucional; estudo qualitativo sobre abordagens de manutenção (corretiva, preventiva, mista) no setor de saúde nigeriano. |
| REG_05478 | Confirma dimensões técnica-operacional/institucional/risco/ciclo de vida; revisão sobre gêmeos digitais aplicados principalmente à fase de construção de edificações pré-fabricadas. |
| REG_05559 | Confirma aplicação de gêmeos digitais para otimização de ocupação e energia em edifícios de escritório. |
| REG_06585 | Confirma critérios de conforto, manutenibilidade e água; estudo qualitativo sobre componentes de design de interiores sustentável em hotéis. |
| REG_07171 | Confirma dimensões de risco e informação/dados; análise bibliométrica sobre efeitos da COVID-19 na gestão sustentável de facilidades. |

## 4. Problemas identificados

Três dos 19 estudos (REG_01104, REG_02204, REG_03176) apresentaram, na leitura de texto
completo, conteúdo que diverge parcialmente da codificação obtida a partir de título e resumo
(ver Seção 3). Essas divergências pontuais não foram corrigidas nas tabelas agregadas do núcleo
de 104 estudos, porque a correção de codificação individual pertence ao escopo do dicionário de
categorias e da extração (Etapa 8), não autorizado nesta tarefa pontual. A divergência é apenas
registrada neste relatório para conhecimento do pesquisador.

## 5. Alterações realizadas

- `latex-artigo/sections/06_metodos.tex`: acrescentado um parágrafo, ao final da seção, citando
  individualmente quatro estudos (REG_03359, REG_05430, REG_06996, REG_08052) com base em
  leitura de texto completo, qualificando a maturidade e a diversidade dos métodos de apoio à
  decisão além do nível documental.
- `latex-artigo/sections/05_criterios.tex`: acrescentado um parágrafo, ao final da seção, citando
  dois estudos (REG_05650, REG_07476) com estatísticas de custo de ciclo de vida e de
  manutenibilidade obtidas em texto completo.
- `latex-artigo/sections/07_aplicabilidade.tex`: acrescentado um parágrafo, ao final da seção,
  citando um estudo (REG_08528) sobre resiliência institucional e ODS em instituições de ensino
  técnico-profissional, obtido em texto completo.
- `latex-artigo/references.bib`: incluídas sete novas entradas bibliográficas, uma para cada
  estudo efetivamente citado, com dados extraídos diretamente dos PDFs.

Todas as três seções alteradas mantiveram os parágrafos e tabelas pré-existentes; nenhum número,
tabela, figura ou citação já existente foi removido ou modificado.

## 6. Alterações não realizadas

- Não foi alterada a Seção "Procedimentos metodológicos" (`03_metodologia.tex`) nem a Seção
  "Limitações" (`09_limitacoes.tex`): a declaração de que a síntese permanece predominantemente
  documental já era adequada e não exigia ajuste.
- Não foram alteradas as tabelas agregadas do núcleo de 104 estudos (dimensões, critérios,
  métodos, contexto), nem os números do funil de seleção ou da deduplicação.
- Não foi corrigida, nas tabelas agregadas, a codificação individual dos três estudos com
  divergência identificada na Seção 4: essa correção pertenceria ao dicionário de categorias e à
  extração (Etapa 8), fora do escopo desta tarefa pontual.
- Não foi alterada a seção "Considerações finais" (`10_consideracoes.tex`).
- Não foi iniciada a Rota B (obtenção de texto completo para os demais estudos do núcleo,
  elegibilidade formal, avaliação metodológica ou nova extração).

## 7. Informação insuficiente para verificar

- Se a leitura de texto completo dos 85 estudos do núcleo final ainda sem PDF disponível
  alteraria a codificação documental desses estudos: informação insuficiente para verificar.
- Página final do artigo de Espinosa Gispert et al. (chave `gispert_ontologiaativos_2025`) na
  revista *Smart and Sustainable Built Environment*: a paginação registrada em `references.bib`
  (740-757) reflete a numeração observada nas páginas lidas do PDF; a confirmação editorial
  completa do intervalo de páginas é informação insuficiente para verificar nesta sessão.

## 8. Validações executadas

- Conferência de que as sete novas chaves de citação usadas nas seções alteradas correspondem a
  sete novas entradas em `references.bib`, sem duplicidade com chaves existentes.
- Conferência de que nenhuma citação, referência, tabela, figura ou número pré-existente foi
  removido ou alterado.
- Conferência de que os parágrafos inseridos não usam travessão Unicode nem a sintaxe `" -- "`.
- Execução de `python scripts/python/verificar_artigo.py`: concluída sem divergências.
- Compilação local do LaTeX: informação insuficiente para verificar (ambiente sem instalação TeX
  disponível nesta sessão); a compilação automatizada permanece a cargo do workflow do
  repositório.

## 9. Arquivos alterados

- `latex-artigo/sections/05_criterios.tex`
- `latex-artigo/sections/06_metodos.tex`
- `latex-artigo/sections/07_aplicabilidade.tex`
- `latex-artigo/references.bib`
- `docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md` (criado)
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Registrado após a execução do commit exclusivo desta tarefa pontual (ver
`docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`).

## 11. Pendências

- Nenhuma pendência bloqueante para a continuidade das etapas 0-16. A decisão sobre autorizar ou
  não a Rota B permanece em aberto, como já registrado ao final da Etapa 7.

## 12. Próxima etapa prevista

Etapa 8 — dicionário de categorias e extração, somente após autorização explícita.
