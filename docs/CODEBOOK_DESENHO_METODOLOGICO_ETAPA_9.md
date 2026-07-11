# Codebook de desenho metodológico — Etapa 9

## 1. Natureza deste documento

Este codebook formaliza a tipologia de desenho metodológico aplicada aos 104 estudos do núcleo
final, produzida por `scripts/python/classificar_desenho_estudos.py`. A classificação usa apenas
título e o campo `evidencia_curta_do_resumo` (excerto documental curto, entre 62 e 220 caracteres,
já registrado na auditoria qualitativa da Etapa 6) — não houve leitura de texto completo para
esta classificação, com a exceção já registrada dos sete estudos citados individualmente na tarefa
pontual de texto completo (ver `docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md`), cuja
classificação aqui permanece a mesma obtida pela regra documental, para preservar a
reprodutibilidade uniforme do método em todo o núcleo.

Categoria única por registro, por ordem de prioridade fixa (permite reprodução):

| Categoria | Definição | Inclusão | Exclusão | Exemplo positivo | Regra de desempate |
|---|---|---|---|---|---|
| `revisao_bibliometrica` | Estudo autodeclarado como revisão de literatura ou análise bibliométrica. | Título ou excerto contém "review", "bibliometric", "overview of". | Menção a "review" em sentido de revisão de projeto/processo administrativo, não de literatura. | REG_02635 ("A thematic review on..."). | Maior prioridade: se autodeclarado como revisão, prevalece sobre qualquer outro sinal. |
| `estudo_caso_empirico` | Estudo de caso ou ambiente/instituição real nomeados como objeto de investigação. | Título ou excerto contém "case study"/"case-study". | Menção a "case" fora do sentido de estudo de caso (ex.: "in this case"). | REG_01657 ("...healthcare: A case study"). | Prevalece sobre método quantitativo e simulação, pois indica o ambiente empírico do estudo. |
| `estudo_survey_percepcao` | Levantamento com coleta de dados de percepção, stakeholders ou instrumentos de pesquisa social. | Menção a survey, questionnaire, interview, percepção ou stakeholders. | Menção a "interview" em sentido de entrevista de emprego ou mídia, não de coleta de dados de pesquisa. | REG_04759 ("...a stakeholder..."). | Prevalece sobre método quantitativo quando ambos aparecem, pois indica a fonte primária de dados. |
| `aplicacao_metodo_decisao_quantitativo` | Método multicritério, estocástico, de otimização, de custo de ciclo de vida ou de aprendizado de máquina nomeado explicitamente. | Menção a fuzzy, AHP, ANP, TOPSIS, MCDM/MCDA, stochastic, optimization, Delphi, regression, machine learning, life cycle cost/LCC. | Menção a "optimization" em sentido coloquial (ex.: "otimizar recursos"), sem método formal nomeado. | REG_00110 ("...Fuzzy Synthetic Evaluation"). | Prevalece sobre simulação/framework, por ser um sinal mais específico de desenho analítico. |
| `estudo_simulacao_modelagem_digital` | Simulação computacional, gêmeo digital, BIM ou modelo computacional aplicado, sem método de decisão nomeado. | Menção a simulation, digital twin, BIM, computational model, control strategy/logic. | Menção a "model" em sentido genérico de "modelo conceitual" sem simulação/computação. | REG_02495 ("Digital Twins' Applications..."). | Prevalece sobre framework genérico, por indicar instrumento computacional específico. |
| `proposta_framework_conceitual` | Proposta de framework, modelo conceitual ou metodologia, sem os sinais anteriores. | Menção a framework, conceptual, "propose(s) a", "development of a/an", "methodology for". | Menção a "framework" em sentido de arcabouço legal/institucional, sem proposta metodológica do próprio estudo. | REG_04225 ("...conceptual framework..."). | Categoria residual entre os sinais positivos; usada apenas quando nenhuma categoria anterior se aplica. |
| `nao_classificavel_pelo_resumo` | Nenhum dos sinais acima presente no título e no excerto documental disponível. | Ausência de qualquer termo das listas acima. | — | REG_00519 (excerto trata do problema geral, sem sinal de método/desenho). | Categoria de honestidade documental: não força uma classificação sem sinal textual suficiente. |

## 2. Resultado da classificação

| Categoria | N | % dos 104 |
|---|---:|---:|
| Aplicação de método de decisão quantitativo | 24 | 23,1% |
| Não classificável pelo resumo | 24 | 23,1% |
| Revisão bibliométrica | 19 | 18,3% |
| Proposta de framework conceitual | 11 | 10,6% |
| Estudo de caso empírico | 11 | 10,6% |
| Estudo de simulação/modelagem digital | 10 | 9,6% |
| Estudo de levantamento/percepção | 5 | 4,8% |

Fonte: `latex-artigo/fontes/tabela37_desenho_metodologico_nucleo_final_104.csv` e
`latex-artigo/fontes/tabela37_ids_por_desenho_nucleo_final_104.csv` (lista de `id_unico` por
categoria).

## 3. Por que 23,1% permanecem não classificáveis

O campo `evidencia_curta_do_resumo` é um excerto curto (62 a 220 caracteres, média de 171), em
geral apenas a primeira frase do resumo, frequentemente dedicada ao problema geral ("Purpose: This
study examines...") sem detalhar o método antes do corte. Essa é uma limitação estrutural do nível
documental já declarado na metodologia do artigo, não uma falha do classificador. Forçar uma
classificação sem sinal textual suficiente violaria a regra de não tratar inferência como
comprovação (`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`, seção 4). Os 24 registros não classificados
permanecem no núcleo final e em todas as demais tabelas do artigo; apenas não recebem um rótulo de
desenho metodológico nesta etapa.
