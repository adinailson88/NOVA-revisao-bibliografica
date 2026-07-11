# Relatório de uso pontual de texto completo dos 11 novos estudos

## 1. Escopo executado

Foram examinados os resumos detalhados, produzidos a partir da leitura integral realizada pelo pesquisador, de 11 estudos pertencentes ao núcleo final de 104 registros. O conteúdo foi comparado, registro a registro, com a codificação documental preservada em `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv`.

A tarefa foi executada fora da sequência formal das Etapas 0 a 16. Nenhum PDF foi incorporado ao repositório. Nenhum resultado agregado foi recalculado.

## 2. Arquivos analisados

- `docs/RESUMOS_DETALHADOS_11_NOVOS_ESTUDOS.txt`
- `docs/MAPA_FULLTEXT_11_NOVOS_ESTUDOS.csv`
- `docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md`
- `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv`
- Seções atuais do artigo e `latex-artigo/references.bib`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`
- `docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`

Os 11 identificadores foram encontrados no núcleo final. Não há sobreposição com os 19 estudos examinados anteriormente.

## 3. Verificação bibliográfica

### 3.1 Referências inicialmente incompletas

Os metadados das três referências assinaladas no arquivo de resumos foram completados antes de qualquer proposta de citação.

1. **REG_00110 — Yoon e Cha (2018)**  
   Yoon, Jong Han; Cha, Hee Sung. *Optimal FM Strategy for Commercial Office Buildings Using Fuzzy Synthetic Evaluation*. Journal of Performance of Constructed Facilities, v. 32, n. 3, art. 04018025, 2018. DOI: 10.1061/(ASCE)CF.1943-5509.0001176.

2. **REG_00852 — Chew e Conejos (2016)**  
   Chew, Michael Yit Lin; Conejos, Sheila. *Developing a green maintainability framework for green walls in Singapore*. Structural Survey, v. 34, n. 4/5, p. 379-406, 2016. DOI: 10.1108/SS-02-2016-0007.

3. **REG_00217 — Tan, Zaman e Sutrisna (2018)**  
   Tan, Adeline Zhu Teng; Zaman, Atiq Uz; Sutrisna, Monty. *Enabling an effective knowledge and information flow between the phases of building construction and facilities management*. Facilities, v. 36, n. 3/4, p. 151-170, 2018. DOI: 10.1108/F-03-2016-0028.

### 3.2 Divergências corrigidas no diagnóstico

- O mapa apresentava DOI incompleto para `REG_00852`. O DOI correto é `10.1108/SS-02-2016-0007`.
- O mapa apresentava `10.1108/F-10-2019-0106` para `REG_03230`. O DOI editorial e o DOI existente no núcleo são `10.1108/F-10-2019-0108`.
- `REG_03230` foi publicado on-line em 2020 e integra o volume 39, número 5/6, páginas 366-388, atribuído editorialmente a 2021. A diferença entre ano on-line e ano do fascículo deve ser tratada de modo consistente na referência.
- O título de `REG_00110` pertence ao *Journal of Performance of Constructed Facilities*, não ao *Journal of Cold Regions Engineering*.

## 4. Comparação individual com a codificação documental

| ID | Resultado da comparação | Evidência obtida no texto completo | Implicação |
|---|---|---|---|
| REG_00489 | Refina | Confirma sustentabilidade, desempenho, informação, apoio à decisão e `framework`. Acrescenta a arquitetura Lean Six Sigma baseada em conhecimento, o ciclo DMAIC, reuso de lições de manutenção e ausência de validação empírica. | Candidato a incorporação em métodos ou discussão. |
| REG_00110 | Refina | Confirma contexto comercial, critérios econômicos e operacionais, abordagem fuzzy e pontuação. Especifica avaliação sintética fuzzy aplicada à comparação de estratégias de FM mediante julgamentos de especialistas. | Candidato a incorporação em métodos. |
| REG_04052 | Confirma e refina | Confirma AHP, fuzzy, raciocínio baseado em casos, dados históricos, condição, desempenho e manutenibilidade. Especifica a combinação CBR + Fuzzy-AHP para prever cronogramas de reparo. | Candidato a incorporação em métodos. |
| REG_00888 | Confirma e refina | Confirma otimização, risco, energia, ciclo de vida e contexto residencial. Acrescenta resiliência a inundação e otimização multiobjetivo em decisões de projeto. | Achado tangencial à manutenção; manter no relatório, sem incorporação narrativa prioritária. |
| REG_00852 | Refina | Confirma manutenibilidade, energia, condição, ciclo de vida e `framework`. Acrescenta cinco fatores de manutenibilidade verde, defeitos observados, riscos de acesso e necessidade de considerar manutenção desde o projeto. | Candidato a incorporação em critérios. |
| REG_01046 | Confirma e refina | Confirma BIM, `framework`, energia, informação, ciclo de vida e edifícios comerciais. Identifica lacunas reais de integração entre aspectos técnicos, organizacionais e legais do retrofit, ausentes no campo documental de lacuna. | Confirma achado já representado por estudos BIM; não exige nova citação narrativa. |
| REG_01657 | Refina | Confirma hospital público, desempenho, dimensões social, técnica e institucional. Especifica adaptação do AEDET, survey com profissionais e limites de um caso único australiano. O campo documental de lacuna continha apenas texto editorial. | Candidato a incorporação em aplicabilidade. |
| REG_04122 | Refina | Confirma custo, risco, segurança, condição, água, manutenibilidade e `framework`. Acrescenta evidência empírica de campo sobre defeitos, acesso, irrigação, segurança ocupacional e coordenação de atores em sistemas vegetados verticais. | Candidato a incorporação em critérios, em conjunto com REG_00852. |
| REG_03230 | Contradiz parcialmente e permanece insuficiente | O contexto é museu de arte, não edifício comercial. O DOI correto termina em 0108. A codificação registra otimização e custo do ciclo de vida, mas o resumo detalhado não permite distinguir com segurança o método do estudo próprio dos métodos apenas revisados na literatura. | Não incorporar até confirmação metodológica nas páginas completas pertinentes. Registrar correção futura de contexto em nível individual. |
| REG_00415 | Refina | Confirma AHP, ANP, fuzzy, pontuação e apoio à decisão. Acrescenta integral de Choquet, 54 indicadores, survey com 31 respostas e aplicação a quatro modelos de negócio. O texto completo evidencia dimensão econômica e custo não registrados entre as dimensões e critérios do CSV. | Metodologicamente relevante, mas tangencial à manutenção predial; manter como evidência secundária. |
| REG_00217 | Confirma, refina e contradiz parcialmente | Confirma BIM, `framework`, informação, ciclo de vida e portfólio. Acrescenta três casos, 18 especialistas, Soft Landings e modelo integrado de compartilhamento de conhecimento. A leitura integral não sustenta `ranking` como método decisório formal; há classificação qualitativa de capacidades, não ranqueamento multicritério. | Candidato a incorporação em aplicabilidade ou discussão; registrar ressalva sobre `ranking`. |

## 5. Síntese das decisões

### 5.1 Estudos com acréscimo narrativo recomendado

Sete estudos apresentam conteúdo de texto completo que acrescenta informação específica e não meramente repetitiva:

- `REG_00489` — Lean Six Sigma, DMAIC e gestão do conhecimento na manutenção;
- `REG_00110` — avaliação sintética fuzzy de estratégias de FM;
- `REG_04052` — CBR + Fuzzy-AHP para previsão de reparos;
- `REG_00852` — fatores de manutenibilidade verde desde a fase de projeto;
- `REG_01657` — avaliação de desempenho em hospital público e adaptação do AEDET;
- `REG_04122` — evidências empíricas de manutenibilidade de sistemas vegetados verticais;
- `REG_00217` — fluxo de informação, Soft Landings e integração BIM/FM na entrega do edifício.

### 5.2 Estudos sem incorporação narrativa prioritária

- `REG_00888` acrescenta resiliência a inundação, mas permanece centrado em decisão de projeto residencial.
- `REG_01046` confirma BIM e retrofit verde, já representados por referências incorporadas.
- `REG_00415` acrescenta método híbrido robusto, mas seu objeto principal são modelos de negócio de construção sustentável, com aderência indireta à manutenção.
- `REG_03230` não deve ser incorporado enquanto método e contexto não forem reconciliados com segurança.

### 5.3 Contradições ou omissões registradas

Não houve contradição capaz de invalidar resultados agregados. Foram identificadas inconsistências individuais:

- contexto comercial indevido em `REG_03230`;
- `ranking` não confirmado como método formal em `REG_00217`;
- dimensão econômica e custo não registrados em `REG_00415`;
- campos de lacuna sem conteúdo analítico em `REG_01046` e `REG_01657`;
- DOI incorreto de `REG_03230` e DOI incompleto de `REG_00852` no mapa novo.

Essas ocorrências devem permanecer documentadas. Eventual recodificação do CSV exigirá decisão específica, porque modificaria a base individual que alimenta produtos agregados.

## 6. Proposta de incorporação posterior ao artigo

A incorporação, se aprovada, deverá ser limitada a frases individualizadas, sem recalcular tabelas ou frequências.

### 6.1 Seção de critérios

Usar `REG_00852` e `REG_04122` para demonstrar que manutenibilidade verde envolve desempenho, custo, risco, impacto ambiental e consumo de recursos, com evidências de acesso, irrigação, segurança e coordenação profissional.

### 6.2 Seção de métodos

Usar:

- `REG_00489` para Lean Six Sigma baseado em conhecimento;
- `REG_00110` para avaliação sintética fuzzy de estratégias de FM;
- `REG_04052` para CBR combinado a Fuzzy-AHP na programação de reparos.

### 6.3 Seção de aplicabilidade ou discussão

Usar:

- `REG_01657` para adaptação de instrumento de desempenho a hospital público;
- `REG_00217` para perda de informação na transição construção-operação e integração entre BIM, Soft Landings e gestão de facilidades.

Cada inclusão deverá ser acompanhada de entrada bibliográfica verificada. A redação deverá informar explicitamente que a evidência decorre da leitura pontual de texto completo.

## 7. Alterações realizadas

Foi criado somente este relatório. Nenhum arquivo do artigo, referência bibliográfica, dataset, tabela, figura ou script foi alterado.

## 8. Alterações não realizadas

- Não foram criadas entradas em `references.bib`.
- Não foram inseridas citações nas seções LaTeX.
- Não foi recodificado nenhum dos 104 registros.
- Não foram recalculados totais, percentuais ou coocorrências.
- Não foi alterada a declaração de natureza predominantemente documental.
- Não foram versionados PDFs.

## 9. Informação insuficiente para verificar

- Método próprio completo de `REG_03230`, separado dos métodos citados em sua revisão: Informação insuficiente para verificar.
- Efeito das correções individuais sobre os produtos agregados sem recálculo controlado: Informação insuficiente para verificar.
- Necessidade de recodificação formal dos registros contraditórios: depende de decisão metodológica do pesquisador.

## 10. Validações executadas

- 11 IDs conferidos contra o núcleo final;
- ausência de interseção com o lote anterior de 19;
- DOI e título confrontados com o núcleo;
- metadados incompletos de Yoon, Chew e Tan completados;
- DOI de Hassanizadeh e Noorzai corrigido;
- comparação das cinco colunas documentais solicitadas;
- separação entre confirmação, refinamento e contradição;
- preservação dos direitos autorais e ausência dos PDFs no repositório.

## 11. Arquivos alterados

- `docs/RELATORIO_USO_TEXTO_COMPLETO_11_NOVOS_ESTUDOS.md` — criado.

## 12. Commit e push

Mensagem prevista: `docs: audita texto completo de 11 novos estudos`.

## 13. Pendências

Antes de alterar o artigo:

1. validar quais dos sete estudos recomendados devem ser incorporados;
2. decidir se os registros com divergência individual serão recodificados ou apenas documentados;
3. confirmar se `REG_03230` permanecerá excluído da incorporação;
4. aprovar a criação das novas entradas em `references.bib`;
5. restaurar ou executar formalmente a Etapa 14, que não consta no estado atual do branch.

## 14. Próxima ação prevista

Parada obrigatória para validação do pesquisador. Após aprovação, poderão ser incorporadas apenas as evidências autorizadas, mantendo inalterados os resultados agregados e a natureza predominantemente documental da revisão.
