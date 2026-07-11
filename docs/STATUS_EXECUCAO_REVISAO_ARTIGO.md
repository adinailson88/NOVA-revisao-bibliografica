# Status da revisão metodológica e textual

## Repositório
- URL: https://github.com/adinailson88/NOVA-revisao-bibliografica
- Branch: revisao-metodologica-controlada
- Data de início: 2026-07-10
- Commit de origem: `e10ef825e6a560f19ffc12306d55b142b3c360e3`
- Preservação: branch `preservacao-original-revisao-metodologica-20260710`

## Regra de execução
O trabalho será realizado estritamente conforme o arquivo:
`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`


## Progresso resumido

| Etapa | Situação |
|---|---|
| Etapa 1 | OK |
| Etapa 2 | OK |
| Etapa 3 | OK |
| Etapa 4 | OK |
| Etapa 5 | OK |
| Etapa 6 | OK |
| Etapa 7 | OK |
| Etapa 8 | OK |
| Etapa 9 | OK |

## Etapas

| Etapa | Descrição | Status | Commit | Pendências |
|---:|---|---|---|---|
| 0 | Preparação e preservação dos arquivos | Concluída | Commit exclusivo da Etapa 0; hash registrado no relatório de execução | Recompilação local independente e logs completos: Informação insuficiente para verificar. |
| 1 | Auditoria do tipo de revisão | Concluída | Commit exclusivo da Etapa 1; hash registrado no relatório de execução | Aguardar autorização explícita para a Etapa 2 |
| 2 | Pergunta, objetivos e escopo | Concluída | Commit exclusivo da Etapa 2; hash registrado no relatório de execução | Aguardar autorização explícita para a Etapa 3 |
| 3 | Estratégia de busca e reprodutibilidade | Concluída | Commit exclusivo da Etapa 3; hash registrado no relatório de execução | Pendências regularizadas; ressalva RIS×string e justificativa de 2010 permanecem documentadas |
| 4 | Funil de seleção | Concluída | Commit exclusivo da Etapa 4 e commit de encerramento documental | Sem pendência documental |
| 5 | Deduplicação | Concluída | Commit exclusivo da Etapa 5 | Sem pendência operacional |
| 6 | Triagem e auditoria dos registros | Concluída | Artigo, mapa, relatório e verificador atualizados | Sem pendência bloqueante |
| 7 | Texto completo e elegibilidade | Concluída | Commit exclusivo da Etapa 7 e commit de regularização do verificador | Sem pendência bloqueante; decisão pendente sobre autorizar ou não a Rota B |
| 8 | Dicionário de categorias e extração | Concluída | Commit exclusivo da Etapa 8 | Regeneração local da Figura~11 pendente (ver relatório da Etapa 8) |
| 9 | Avaliação metodológica dos estudos | Concluída | Commit exclusivo da Etapa 9 | Sem pendência bloqueante; instrumentos de qualidade mapeados mas não aplicados (exigem texto completo) |
| 10 | Auditoria dos resultados | Não iniciada | | |
| 11 | Discussão | Não iniciada | | |
| 12 | Matriz analítica | Não iniciada | | |
| 13 | Limitações | Não iniciada | | |
| 14 | Redação e padronização | Não iniciada | | |
| 15 | Referências metodológicas | Não iniciada | | |
| 16 | Consolidação final | Não iniciada | | |

## Registro da Etapa 0

### Arquivos analisados
- Estrutura do repositório e histórico de commits.
- Fonte LaTeX principal e onze seções.
- Bibliografia.
- Bases derivadas, tabelas e figuras.
- Scripts Python e R.
- Workflow de geração e PDF publicado.

### Arquivos alterados
- `docs/INVENTARIO_ARTIGO_REVISAO.md` — criado.
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md` — atualizado.
- Nenhum arquivo do artigo foi alterado.

### Decisões
- A versão inicial foi preservada no commit `e10ef825e6a560f19ffc12306d55b142b3c360e3` e na branch `preservacao-original-revisao-metodologica-20260710`.
- Foram registrados Git blob SHAs para os arquivos principais.
- O `main.pdf` anexado foi usado apenas para compreensão do estado inicial; o repositório permanece como fonte oficial.

### Validações
- Branch de trabalho isolada da `main`.
- PDF publicado existente e legível, com 14 páginas.
- Workflow de compilação localizado.
- Inventário confrontado com o histórico e com a existência dos arquivos principais.
- Nenhuma alteração científica ou textual executada.

### Informações insuficientes
- Recompilação local independente: Informação insuficiente para verificar.
- Logs completos do workflow de origem: Informação insuficiente para verificar.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 1`.


## Registro da Etapa 1

### Data
2026-07-10

### Arquivos analisados
Fonte principal, resumo, introdução, revisão teórica, metodologia, resultados, limitações e considerações finais; Hu et al. (2026) e Franca (2025) nos limites definidos pelo plano.

### Diagnóstico
A denominação documentalmente sustentável é “revisão integrativa sistematizada, com apoio bibliométrico e síntese temática”. Não há base para transformar o trabalho em revisão sistemática por mudança de redação.

### Arquivos alterados
- `latex-artigo/sections/00_resumo.tex`
- `docs/RELATORIO_ETAPA_1.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Decisões
Resumo e abstract foram padronizados à denominação já usada na metodologia. Nenhum procedimento, número, resultado, objetivo ou referência foi alterado.

### Informação insuficiente
Protocolo prévio, pré-registro, leitura integral, avaliação metodológica, dupla revisão e conformidade integral ao PRISMA: Informação insuficiente para verificar.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 2`.


## Registro da Etapa 2

### Data
2026-07-10

### Diagnóstico
A RQ0 foi ajustada para não apresentar o contexto público universitário como característica de todo o corpus. RQ1–RQ5 foram alinhadas ao nível documental dos campos auditados.

### Arquivos alterados
- `latex-artigo/sections/01_introducao.tex`
- `latex-artigo/sections/03_metodologia.tex`
- `docs/RELATORIO_ETAPA_2.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Decisões
Foi inserida matriz explícita de alinhamento. Tema, corpus, método de seleção, números e resultados foram preservados.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 3`.


## Registro da Etapa 3

### Data
2026-07-10

### Diagnóstico
Scopus e Crossref possuem consultas e parâmetros reprodutíveis nos scripts. A Web of Science possui campo, data, período, identificadores e totais, mas não as strings literais. A reprodutibilidade integral do conjunto é parcial.

### Arquivos alterados
- `latex-artigo/sections/03_metodologia.tex`
- `docs/APENDICE_ESTRATEGIAS_BUSCA.md`
- `docs/RELATORIO_ETAPA_3.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 4`.


## Regularização anterior à Etapa 4

As pendências das Etapas 1–3 foram respondidas pelo pesquisador e incorporadas ao artigo e à documentação. Foram corrigidas as datas da Scopus, incluídas as quatro strings da Web of Science e registradas as ausências de pré-registro, texto completo, segundo avaliador e avaliação de qualidade. Os arquivos originais de protocolo citados não foram localizados nesta branch; sua eventual migração permanece pendente.


## Reconciliação final anterior à Etapa 4

- Scopus: 9.438 registros, sendo 9.433 da API e cinco exclusivos do export manual incorporados em 09/07/2026.
- Web of Science: 1.680 registros; A4 corrigido de 502 para 503 após recontagem.
- Crossref: 1.000 registros.
- Total bruto preservado: 12.118.
- O corte 2010–2026 foi mantido por corresponder à busca executada; não foi criada justificativa retrospectiva.
- Os seis arquivos de `01_PROTOCOLO/` foram incorporados à branch de trabalho.


## Registro da Etapa 4

### Data
2026-07-10

### Diagnóstico
O funil fecha numericamente, mas a redação anterior superestimava a extensão da revisão humana. A auditoria individual cobriu 100 de 9.542 registros; os demais mantiveram classificação automática.

### Alterações
Foi inserida tabela completa de rastreabilidade e a figura do funil foi corrigida. Automação, auditoria amostral, alinhamento determinístico e auditoria qualitativa passaram a ser relatados separadamente.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 5`.


## Encerramento documental da Etapa 4

Os 109 produtos intermediários foram incorporados e organizados nas pastas 03, 04, 05 e 07. Foram validados os totais de deduplicação, o corte inicial de 3.786, a resolução das 4.276 dúvidas, o núcleo revisado de 3.678, a seleção de 137 e a auditoria final de 104. A pendência documental da Etapa 4 está encerrada.


## Registro da Etapa 5

A deduplicação foi especificada e validada sem mudança de lógica. Foram confirmados 1.808 grupos e 2.576 ocorrências removidas. O verificador automático passou a conferir produtos processados, DOI único, IDs e proveniência. Os conflitos detectados foram preservados como registros separados.

Próxima ação: aguardar `AUTORIZO A ETAPA 6`.


## Registro da Etapa 6

As camadas de seleção foram documentadas separadamente: pré-triagem determinística dos 9.542 registros, auditoria amostral de 100, resolução dos 4.276 casos de dúvida, reavaliação dos 3.678 registros, alinhamento de 137 registros centrais e auditoria qualitativa que consolidou 104 estudos. O artigo não atribui uso de IA ou ASReview sem evidência documental e declara a ausência de segundo avaliador independente. O verificador automático passou a conferir todos esses marcos.

Próxima ação: aguardar `AUTORIZO A ETAPA 7`.


## Registro da Etapa 7

A avaliação de texto completo dos 104 estudos do núcleo final não ocorreu em nenhuma camada de triagem ou auditoria, o que já estava descrito por camada em `03_metodologia.tex`. Foi acrescentada uma declaração explícita de elegibilidade, incluindo o caso do registro sinalizado para verificação pontual e descartado sem leitura integral. Foi acrescentada uma limitação específica em `09_limitacoes.tex`, distinguindo análise documental de síntese de evidências de texto completo. Em `10_consideracoes.tex`, a expressão "confirma" foi substituída por uma formulação compatível com o nível documental de evidência. Foram apresentadas as Rotas A (manutenção em nível documental, adotada) e B (elevação para revisão sistemática com texto completo, não executada, com plano operacional descrito em `docs/RELATORIO_ETAPA_7.md`).

A execução de `scripts/python/verificar_artigo.py` revelou uma falha pré-existente, anterior a esta etapa (confirmada no commit `523f44f`, encerramento da Etapa 6): o script exigia exatamente 5 tabelas no artigo, mas há 8 tabelas presentes, todas elas legítimas e correspondentes a produtos criados durante as Etapas 2 a 6 (matriz de alinhamento, estratégia de busca, critérios de seleção, deduplicação e rastreabilidade do funil em `03_metodologia.tex`, além das tabelas de base/tipo, critérios de priorização e contexto de edificação nas Seções de resultados). A constante do script nunca havia sido atualizada conforme essas tabelas foram legitimamente adicionadas.


## Regularização do verificador automático (pós-Etapa 7)

Corrigidos, em commit próprio de regularização, dois problemas do próprio verificador — não do artigo:

1. A verificação de contagem de tabelas foi ajustada de 5 para 8, refletindo o número real e correto
   de tabelas do artigo (nenhuma tabela foi removida ou criada por essa correção).
2. A verificação da tabela redundante do funil (`"tab:funil" not in texto_tex`) gerava falso positivo,
   pois o rótulo atual e legítimo `tab:funilselecao` contém a substring `tab:funil`. A verificação foi
   ajustada para `"tab:funil}" not in texto_tex`, preservando a intenção original (impedir a
   reintrodução da antiga tabela redundante) sem acusar a tabela de rastreabilidade legítima.
3. A leitura de `04_TRIAGEM/decisao_duvidas_revisada.tsv` usava `delimiter="\\t"` (dois caracteres:
   barra invertida e "t"), que o módulo `csv` rejeita por não ser um único caractere; corrigido para
   `delimiter="\t"` (caractere de tabulação). Esse bug pré-existente impedia a conclusão de qualquer
   execução do verificador que chegasse a essa checagem.

Após as três correções, `python scripts/python/verificar_artigo.py` conclui sem divergências. Nenhum
número, tabela, figura, citação ou referência do artigo foi alterado nesta regularização.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Regularização da declaração de acesso a texto completo (pós-Etapa 7)

O pesquisador buscou, fora do escopo formal das etapas, obter texto completo dos 104 estudos por
acesso aberto legítimo (consulta à API pública do Unpaywall a partir dos DOIs do núcleo final). Dez
estudos tiveram PDF de acesso aberto obtido e validado; os demais permanecem sem texto completo
disponível por essa via, por ausência de versão aberta ou por dependerem de acesso institucional aos
periódicos. Nenhum desses PDFs foi lido ou incorporado à síntese do artigo até o momento; apenas os
arquivos foram obtidos e reservados fora do repositório.

Para refletir esse cenário sem antecipar procedimento não realizado, `03_metodologia.tex` e
`09_limitacoes.tex` foram ajustados para declarar que a síntese permanece predominantemente apoiada em
título, resumo, palavras-chave e campos estruturados, em razão do acesso institucional restrito a
parte dos periódicos, e que o eventual uso de texto completo do pequeno subconjunto obtido por acesso
aberto será indicado e referenciado individualmente por estudo, caso venha a ocorrer, sem alterar a
natureza predominantemente documental da revisão como um todo.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Atualização do subconjunto com texto completo obtido (pós-Etapa 7)

Além dos dez estudos com PDF de acesso aberto obtido via Unpaywall, um cruzamento entre os títulos do
núcleo final e a biblioteca pessoal do pesquisador no Zotero identificou nove estudos adicionais com
texto completo disponível localmente, totalizando dezenove estudos do núcleo final com PDF acessível
(dezoito de fato mapeados e confirmados; um candidato de baixa confiança foi descartado por
inconsistência entre título e conteúdo do arquivo). Nenhum desses PDFs foi lido ou incorporado à
síntese do artigo até o momento; a leitura e a eventual incorporação, quando ocorrerem, serão
registradas e referenciadas individualmente por estudo, conforme já declarado em `03_metodologia.tex`
e `09_limitacoes.tex`.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Uso pontual de texto completo dos 19 estudos (fora da sequência de etapas 0-16)

Tarefa pontual, autorizada fora da sequência formal do plano controlado: leitura de texto completo
dos 19 estudos do núcleo final com PDF disponível (relatório completo em
`docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md`). A leitura comparou cada estudo com a codificação
documental já registrada em `nucleo_final_pos_auditoria_resumos.csv`. Sete estudos (REG_03359,
REG_05430, REG_06996, REG_08052, REG_05650, REG_07476, REG_08528) continham conteúdo, verificável em
texto completo, que refinava a síntese em pontos específicos e foram incorporados com citação
individual nova em `05_criterios.tex`, `06_metodos.tex` e `07_aplicabilidade.tex`, com sete novas
entradas em `references.bib`. Os demais doze estudos foram lidos integralmente; a leitura confirmou a
codificação documental existente, sem acrescentar conteúdo narrativamente relevante e não redundante,
exceto três divergências pontuais de codificação individual (REG_01104, REG_02204, REG_03176),
registradas apenas no relatório desta tarefa, sem alteração das tabelas agregadas do núcleo de 104
estudos.

Nenhuma tabela agregada, número do funil de seleção, resultado da deduplicação ou declaração de
natureza predominantemente documental em `03_metodologia.tex` e `09_limitacoes.tex` foi alterada. A
Rota B (elevação a revisão sistemática de todos os 104 estudos) permanece não autorizada.

A execução de `python scripts/python/verificar_artigo.py` após as alterações concluiu sem
divergências.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Registro da Etapa 8

A auditoria das categorias de extração (relatório completo em `docs/RELATORIO_ETAPA_8.md`) formalizou
um codebook (`docs/CODEBOOK_CATEGORIAS_ETAPA_8.md`) com definição, inclusão, exclusão, exemplo
positivo, exemplo negativo e regra de desempate para as seis dimensões de sustentabilidade, os
quinze critérios de priorização, os dezenove métodos de apoio à decisão e os onze contextos de
edificação já usados no núcleo final de 104 estudos. A auditoria identificou dois problemas: (1) o
filtro que restringe a Tabela de dimensões às seis categorias-guarda-chuva, já existente no script
gerador, não estava explicado na prosa do artigo; e (2) três rótulos de método
(`balanced scorecard`, `case-based reasoning`, `Bayesian Best Worst Method`, um registro cada)
estavam grafados de forma diferente entre o núcleo final e o script gerador da Figura~11,
causando exclusão silenciosa desses métodos da figura e da enumeração em prosa, embora
corretamente contabilizados na tabela numérica.

Foram corrigidos, com alteração limitada ao escopo da Etapa 8: a grafia dos três rótulos em
`scripts/r/10_gerar_produtos_artigo.R`; uma frase em `03_metodologia.tex` distinguindo dimensão de
critério; e a enumeração de métodos formalmente nomeados em `06_metodos.tex`. Nenhum estudo do
núcleo final foi recodificado e nenhum número agregado, além da correção pontual da enumeração de
métodos, foi alterado. A regeneração da Figura~11 com a correção do script permanece pendente,
por ausência de interpretador R no ambiente desta sessão.

A execução de `python scripts/python/verificar_artigo.py` após as alterações concluiu sem
divergências.

Próxima ação: aguardar `AUTORIZO A ETAPA 9`.


## Nota sobre a integração contínua (pós-Etapa 8)

Após o registro acima, foram feitas várias iterações de ajuste de layout (largura de colunas e
fonte de tabelas em `03_metodologia.tex`) para tentar eliminar um estouro de margem residual
(\textit{overfull hbox}) que impedia o fluxo de integração contínua (`.github/workflows/latex.yml`)
de concluir a compilação do PDF e publicar automaticamente as tabelas e figuras regeneradas. O
estouro foi reduzido de 115,27pt para menos de 7pt ao longo dessas iterações, mas não foi
eliminado por completo nesta sessão. Por decisão do pesquisador, o ajuste fino remanescente ficará
a cargo de outra ferramenta, fora desta sessão. Isso não afeta o conteúdo científico do artigo:
`scripts/python/verificar_artigo.py` (que audita dados, números, citações e referências) passa sem
divergências em todas as versões; apenas a regeneração automática da Figura~11 e do PDF publicado
pela integração contínua permanece pendente.


## Registro da Etapa 9

A avaliação metodológica dos 104 estudos do núcleo final (relatório completo em
`docs/RELATORIO_ETAPA_9.md`, codebook em `docs/CODEBOOK_DESENHO_METODOLOGICO_ETAPA_9.md`) classificou
o desenho metodológico de cada estudo por regras reprodutíveis sobre título e excerto documental
curto do resumo (`scripts/python/classificar_desenho_estudos.py`), sem leitura de texto completo.
A classificação resultou em sete categorias: aplicação de método de decisão quantitativo (23,1%),
não classificável pelo excerto disponível (23,1%), revisão bibliométrica ou de literatura (18,3%),
proposta de framework conceitual (10,6%), estudo de caso empírico (10,6%), estudo de simulação ou
modelagem digital (9,6%) e estudo de levantamento ou percepção de stakeholders (4,8%).

Nenhum instrumento clínico de avaliação metodológica (RoB 2, GRADE, Newcastle–Ottawa) foi aplicado,
por incompatibilidade de desenho com o corpus de engenharia, gestão de ativos e facility
management. Foi produzido um mapeamento teórico de instrumentos de engenharia potencialmente
compatíveis com cada desenho identificado (transparência de revisão, descrição de caso,
transparência amostral, transparência de método quantitativo, validação de modelo de simulação),
mas nenhum desses instrumentos foi efetivamente aplicado a qualquer estudo: todos exigiriam leitura
de texto completo, fora do escopo documental desta revisão. Foi acrescentado um parágrafo em
`09_limitacoes.tex` declarando essa ausência de avaliação de risco de viés/qualidade metodológica
e o caráter de síntese de frequência (não de recomendação validada) da matriz analítica do artigo.

A execução de `python scripts/python/verificar_artigo.py` após as alterações concluiu sem
divergências.

Próxima ação: aguardar `AUTORIZO A ETAPA 10`.


## Nota de continuidade

A partir deste ponto (commit `59cbfd5`), a execução deste plano poderá continuar em outra sessão
de trabalho, operando diretamente neste repositório. O arquivo de origem da execução continua
sendo `docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`; este arquivo de status continua sendo o registro
único e cumulativo de progresso — qualquer continuidade deve atualizar as seções existentes acima,
não criar um novo arquivo de status paralelo.

Pendência não bloqueante conhecida neste ponto: o fluxo de integração contínua
(`.github/workflows/latex.yml`) falha no passo "Verificar margens do PDF" por um estouro de
margem residual de 1,25pt (menos de meio milímetro) em `latex-artigo/sections/03_metodologia.tex`,
linha 24 (fechamento da tabela `tab:alinhamentorq`, "Matriz de alinhamento entre perguntas,
seleção, extração e resultados"). O estouro já foi reduzido de 115,27pt para 1,25pt por ajustes de
largura de coluna nos commits `057b0c9` a `608df91`; o valor residual é o mesmo independentemente
de qual das quatro colunas fixas da tabela recebe mais largura, o que sugere que a origem pode
estar na última coluna flexível (`Y`, "Resultado correspondente") ou em um efeito de microtipografia
não identificado. Essa pendência não afeta o conteúdo científico do artigo — apenas impede que a
integração contínua regenere e publique automaticamente as tabelas, figuras e o PDF mais recentes.


## Registro da Etapa 10

A auditoria dos resultados confirmou a consistência dos totais, percentuais e denominadores do núcleo final de 104 registros nas séries de anos, bases, tipos documentais, dimensões, critérios, métodos, contextos, lacunas, ODS, ESG e coocorrências. Nenhum registro foi recodificado e nenhum número foi alterado.

Foram explicitados os limites interpretativos das categorias documentais amplas `framework`, técnica-operacional e edificação genérica, bem como das coocorrências, que não demonstram aplicação metodológica, importância científica, associação estatística, efeito ou causalidade. O verificador automático foi ampliado para conferir todas as séries centrais e a tabela de tipos de contribuição gerada pelo script.

Relatório completo em `docs/RELATORIO_ETAPA_10.md`.

Próxima ação: aguardar `AUTORIZO A ETAPA 11`.


## Registro da Etapa 11

A discussão foi reestruturada em seção autônoma, sem alteração dos resultados numéricos. A nova seção integra convergências e divergências, evolução temporal, contextos de aplicação, diferenças entre formulações conceituais e aplicações empíricas, métodos mencionados e aplicados, critérios identificados e operacionalizados, relação entre sustentabilidade e decisão, implicações para gestão pública universitária, limites da evidência e agenda de pesquisa.

As interpretações preservam a distinção entre frequência e importância, menção e aplicação, coocorrência e associação, síntese conceitual e validação. Foram utilizadas apenas referências existentes e verificadas no artigo. Relatório completo em `docs/RELATORIO_ETAPA_11.md`.

Próxima ação: aguardar `AUTORIZO A ETAPA 12`.


## Registro da Etapa 12

A matriz foi auditada e passou a ser denominada “matriz analítica conceitual informada pela síntese da literatura”. Foram distinguidos critérios extraídos, dimensões documentais, desdobramentos conceituais e requisitos futuros de operacionalização. A dimensão ciclo de vida foi explicitada como eixo transversal. Governança, conformidade e capacidade de execução foram identificadas como proposições ainda não contabilizadas individualmente, e custo do ciclo de vida foi distinguido do critério genérico custo.

Foi declarado que frequências e coocorrências não constituem pesos e que a matriz ainda não possui indicadores operacionais, normalização, limiares, função de agregação, método decisório selecionado ou validação empírica. Nenhum resultado ou registro foi alterado. Relatório completo em `docs/RELATORIO_ETAPA_12.md`.

Próxima ação: aguardar `AUTORIZO A ETAPA 13`.


## Registro da Etapa 13

As limitações foram atualizadas conforme o método efetivamente realizado. Foram explicitadas a dependência da cobertura e atualização das bases, o caráter complementar e limitado do Crossref, o ano de 2026 parcial, a ausência de pré-registro público, de busca de citações e de literatura cinzenta, o avaliador único sem concordância interavaliadores, o uso de regras determinísticas com auditoria amostral, a predominância documental, a unidade de análise como registro bibliográfico e a ausência de avaliação metodológica.

A descrição do texto completo foi corrigida para registrar a leitura pontual de 19 estudos, dos quais sete forneceram evidências específicas incorporadas. Não foi incluída afirmação genérica de duplicatas remanescentes. Nenhum resultado foi alterado. Relatório completo em `docs/RELATORIO_ETAPA_13.md`.

Próxima ação: aguardar `AUTORIZO A ETAPA 14`.


## Uso pontual de texto completo dos 11 novos estudos

Foram comparados 11 novos estudos lidos integralmente com a codificação documental do núcleo final, sem sobreposição com o lote anterior de 19. Sete estudos forneceram evidências específicas incorporadas individualmente nas seções de critérios, métodos e aplicabilidade; quatro permaneceram confirmatórios, tangenciais ou com informação insuficiente para incorporação. Os metadados de Yoon e Cha (2018), Chew e Conejos (2016) e Tan, Zaman e Sutrisna (2018) foram completados, e divergências individuais foram documentadas em `docs/RELATORIO_USO_TEXTO_COMPLETO_11_NOVOS_ESTUDOS.md`.

No conjunto das duas tarefas pontuais, 30 estudos foram lidos integralmente e 14 forneceram evidências específicas incorporadas. Os números e produtos agregados do núcleo de 104 registros não foram modificados, e a revisão permanece predominantemente documental.
