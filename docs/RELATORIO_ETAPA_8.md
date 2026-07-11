# Relatório da Etapa 8

## 1. Escopo executado

Auditoria das categorias já utilizadas na extração do núcleo final de 104 estudos (dimensões de
sustentabilidade, critérios de priorização, métodos de apoio à decisão, contextos de edificação,
ODS, ESG, lacunas, respostas múltiplas e regras de contagem), conforme
`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`, seção 14. Criação de um codebook formal com definição,
inclusão, exclusão, exemplo positivo, exemplo negativo e regra de desempate para cada categoria.

## 2. Arquivos analisados

- `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv`
- `latex-artigo/fontes/dicionario_criterio_dimensao_etapa17.csv`
- `latex-artigo/fontes/tabela26_criterios_nucleo_final_104.csv` a `tabela29_contexto_edificacao_nucleo_final_104.csv`
- `latex-artigo/fontes/tabela35_mencoes_ods_esg_nucleo_final_104.csv`
- `scripts/r/10_gerar_produtos_artigo.R`
- `latex-artigo/sections/03_metodologia.tex`, `05_criterios.tex`, `06_metodos.tex`

## 3. Evidências encontradas

- As colunas de extração (`dimensoes_sustentabilidade_identificadas_leitura`,
  `criterios_identificados_leitura`, `metodos_decisao_identificados_leitura`,
  `contexto_edificacao_identificado_leitura`) foram preenchidas por leitura individual de cada um
  dos 104 estudos durante a auditoria qualitativa (Etapa 6), sem leitura de texto completo, o que
  já estava declarado no artigo.
- As instruções detalhadas fornecidas ao avaliador nessa leitura (o "roteiro" citado como fonte
  em `dicionario_criterio_dimensao_etapa17.csv`) não constituem um arquivo preservado neste
  repositório.
- A coluna bruta de dimensões contém dez rótulos, mas apenas seis são reportados na Tabela de
  dimensões e no gráfico correspondente, por um filtro já existente no script gerador
  (`dimensoes_canonicas`), não explicado na prosa do artigo.
- Três rótulos de métodos formalmente nomeados (`balanced scorecard`, `case-based reasoning`,
  `Bayesian Best Worst Method`, um registro cada) estavam gravados no núcleo final com grafia
  diferente da usada no script de geração da Figura~11 (`metodos_estruturados`), causando exclusão
  silenciosa desses três métodos da figura e da enumeração em prosa de `06_metodos.tex`, embora
  estivessem corretos na tabela numérica (`tabela28`).
- O campo `tipo_contribuicao_artigo` tem dez categorias, das quais apenas uma
  (`lacuna_para_ies_publicas`) gera tabela derivada própria; as demais não têm tabela ou figura
  correspondente, mas seus dados são majoritariamente redundantes com as tabelas de
  critérios/dimensões/métodos já publicadas.
- As contagens de ODS/SDG e ESG (`tabela35`) são geradas por regra lexical reprodutível
  (expressão regular sobre título e campos extraídos), consistente com a ressalva já registrada
  nas limitações de que presença lexical não equivale a comprovação de aplicação metodológica.

## 4. Problemas identificados

1. Filtro de dimensões canônicas não documentado na prosa do artigo.
2. Inconsistência de grafia entre três rótulos de método no script gerador de figura, causando
   omissão silenciosa desses métodos na Figura~11 e na enumeração em prosa.
3. Subutilização do campo `tipo_contribuicao_artigo` (observação de auditoria, sem necessidade de
   correção).

## 5. Alterações realizadas

- `docs/CODEBOOK_CATEGORIAS_ETAPA_8.md` (criado): codebook completo com definição, inclusão,
  exclusão, exemplo positivo, exemplo negativo e regra de desempate para as seis dimensões, os
  quinze critérios, os dezenove métodos e os onze contextos usados no núcleo final.
- `scripts/r/10_gerar_produtos_artigo.R`: corrigida a grafia de três rótulos no vetor
  `metodos_estruturados`, sem alterar nenhum dado do núcleo de 104 estudos.
- `latex-artigo/sections/03_metodologia.tex`: acrescentada uma frase distinguindo dimensão de
  critério e referenciando o codebook de apoio (sem citar caminho de arquivo Markdown, por
  restrição do verificador automático).
- `latex-artigo/sections/06_metodos.tex`: completada a enumeração de métodos formalmente
  nomeados para incluir Delphi, \textit{balanced scorecard} e raciocínio baseado em casos, com
  base nos dados corretos de `tabela28`.

## 6. Alterações não realizadas

- Não foi regenerada a Figura~11 (`figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png`):
  o ambiente desta sessão não possui interpretador R instalado. A correção do script está pronta;
  a regeneração do arquivo PNG depende de execução local por parte do pesquisador.
- Não foi recodificado nenhum dos 104 estudos: a auditoria desta etapa formaliza as categorias já
  atribuídas, sem revisar individualmente a atribuição de cada estudo a cada categoria (isso
  pertenceria a uma nova rodada de extração, fora do escopo desta etapa).
- Não foi criada tabela derivada nova para o campo `tipo_contribuicao_artigo`: a subutilização foi
  apenas registrada como observação de auditoria.
- Não foram alterados números, tabelas de frequência ou figuras além da correção pontual do
  script mencionada.

## 7. Informação insuficiente para verificar

- As instruções originais ("roteiro") fornecidas ao avaliador durante a leitura individual dos
  104 estudos, referenciadas em `dicionario_criterio_dimensao_etapa17.csv` como "roteiro, seção
  19": não constam como arquivo preservado neste repositório. As definições reconstruídas neste
  codebook derivam das justificativas já registradas nesse dicionário e do padrão observado nos
  dados, não do roteiro original.
- Regeneração local da Figura~11 após a correção do script: informação insuficiente para
  verificar nesta sessão (ausência de interpretador R).

## 8. Validações executadas

- Conferência de que as seis dimensões, quinze critérios, dezenove métodos e onze contextos do
  codebook correspondem exatamente aos valores únicos observados nas colunas de extração do
  núcleo final.
- Conferência cruzada dos totais de exemplo (positivos) com os totais publicados em `tabela26` a
  `tabela29`.
- Conferência de que a correção de grafia em `scripts/r/10_gerar_produtos_artigo.R` não altera
  nenhum outro trecho do script nem a lógica das demais tabelas e figuras.
- Execução de `python scripts/python/verificar_artigo.py`: concluída sem divergências após ajuste
  da frase em `03_metodologia.tex` para não citar caminho de arquivo Markdown (regra já existente
  no verificador).
- Compilação local do LaTeX e execução local do script R: informação insuficiente para verificar
  nesta sessão (ambiente sem TeX nem R instalados).

## 9. Arquivos alterados

- `docs/CODEBOOK_CATEGORIAS_ETAPA_8.md` (criado)
- `scripts/r/10_gerar_produtos_artigo.R`
- `latex-artigo/sections/03_metodologia.tex`
- `latex-artigo/sections/06_metodos.tex`
- `docs/RELATORIO_ETAPA_8.md` (criado)
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Registrado após a execução do commit exclusivo da Etapa 8 (ver
`docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`).

## 11. Pendências

- Regeneração local de `figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png` pelo
  pesquisador, com R instalado, para refletir a correção do script.
- Decisão, em etapa futura, sobre se o campo `tipo_contribuicao_artigo` deve gerar tabela própria
  ou permanecer apenas como campo auxiliar de auditoria.

## 12. Próxima etapa prevista

Etapa 9 — avaliação metodológica dos estudos, somente após autorização explícita.
