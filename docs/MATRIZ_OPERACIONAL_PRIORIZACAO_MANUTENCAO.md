# Especificação operacional candidata da matriz de priorização

## Finalidade e limite

Protocolo testável para manutenção de edificações públicas universitárias. Não constitui validação empírica nem prescrição definitiva. Pesos, limiares e fontes devem ser calibrados com gestores, equipes técnicas e usuários antes do uso decisório.

## Indicadores candidatos

| Dimensão | Indicador | Unidade | Fonte | Preferência |
|---|---|---:|---|---|
| Técnica-operacional | condição física | 0--100 | inspeção | maior |
| Técnica-operacional | criticidade da falha | 1--5 | ativos e risco | menor |
| Técnica-operacional | tempo médio de reparo | horas | ordens de serviço | menor |
| Técnica-operacional | reincidência de falhas | ocorrências/12 meses | ordens de serviço | menor |
| Técnica-operacional | cumprimento preventivo | % | plano de manutenção | maior |
| Institucional | completude cadastral | % | sistema patrimonial/BIM | maior |
| Institucional | conformidade legal | % | laudos e auditorias | maior |
| Institucional | demandas críticas no prazo | % | ordens de serviço | maior |
| Institucional | rastreabilidade decisória | 0--100 | registros e auditoria | maior |
| Econômica | custo anual de manutenção | R$/m² | sistema financeiro | menor |
| Econômica | desvio orçamentário | % | orçamento e execução | menor |
| Econômica | custo do ciclo de vida | valor presente | orçamento e ativos | menor |
| Ambiental | intensidade energética | kWh/m².ano | medição e faturas | menor |
| Ambiental | intensidade hídrica | m³/usuário.ano | medição e faturas | menor |
| Ambiental | emissões operacionais | kgCO2e/m².ano | energia | menor |
| Ambiental | recuperação de resíduos | % | manifestos e contratos | maior |
| Social | não conformidades de conforto | ocorrências/1.000 usuários | chamados e medições | menor |
| Social | incidentes de segurança | ocorrências ponderadas | registros de segurança | menor |
| Social | satisfação dos usuários | 0--100 | pesquisa | maior |
| Social | acessibilidade funcional | % | inspeção e laudos | maior |

O ciclo de vida é transversal: idade, vida útil remanescente e horizonte da intervenção qualificam indicadores técnicos e econômicos sem peso adicional.

## Pesos-base ajustáveis

Técnica-operacional 30%; institucional 20%; econômica 20%; ambiental 15%; social 15%. Na ausência de elicitação, os indicadores de cada dimensão recebem pesos iguais. Esses valores são hipóteses operacionais, não frequências bibliográficas.

## Normalização e agregação

Benefício: z=(x-min)/(max-min). Custo: z=(max-x)/(max-min). Se máximo e mínimo forem iguais, o indicador é retirado da rodada. O escore é S=100 vezes a soma de w vezes z. Risco à vida, segurança, continuidade essencial ou conformidade legal funciona como veto e força prioridade crítica.

## Sensibilidade

Variar cada peso em mais ou menos 20%, renormalizar os demais e testar cenários de continuidade e segurança, sustentabilidade e restrição orçamentária. Comparar correlação de postos, sobreposição do grupo prioritário, inversões de ordem, dados ausentes, extremos e períodos de observação.

## Validação

Há coerência interna e rastreabilidade de conteúdo preliminar. Ainda são necessárias validação com especialistas locais, teste piloto, confiabilidade das medições, validade de construto e avaliação prospectiva. Até então, o resultado é simulação ou apoio exploratório.
