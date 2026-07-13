# Status — Consolidação da busca de sensibilidade IA/ML e ajuste científico do artigo

Arquivo único e cumulativo de continuidade desta tarefa. Atualizar este documento ao final de
cada etapa. Não criar arquivo de status paralelo.

## Estado verificado em 13/07/2026

- Repositório: `adinailson88/NOVA-revisao-bibliografica`
- Branch: `agent/incorporacao-busca-sensibilidade-ia`
- Pull Request: #4, em modo draft, base `main`
- HEAD verificado antes desta atualização: `29b6869250aa97029f81e6f94273b336ff21ea64`
- Situação do PR na verificação: aberto, porém não mergeável; requer sincronização e resolução
  de conflitos antes da consolidação final.
- Último workflow verificado: “Gerar tabelas, graficos, PDF e Word”, execução 139, concluída
  com sucesso.
- `artigo.docx` já está presente entre os arquivos modificados do PR. A antiga anotação de que
  o DOCX ainda aguardava regeneração foi superada pelo workflow.
- A versão vigente da síntese temática contém 121 registros: 104 do núcleo original e 17
  incorporados após a busca complementar de sensibilidade.

## Objetivo vigente

Consolidar metodológica e textualmente a busca complementar de sensibilidade para inteligência
artificial e aprendizado de máquina, corrigir inconsistências entre os diferentes produtos do
pipeline e, somente depois, executar o ajuste fino global do artigo.

A busca de sensibilidade não substitui a busca principal. Sua função é verificar quanto uma
expressão explicitamente dedicada a IA/aprendizado de máquina altera a identificação de métodos
informacionais e preditivos relacionados à manutenção e à gestão de edificações.

## Regras permanentes

- Relatar os procedimentos executados, sem atribuir autoria ou revisão a sistemas automatizados.
- Não executar nem criar scripts R neste fluxo. Quando necessário, reproduzir a lógica em Python.
- Não forçar totais históricos ou atuais; todo número deve ser recalculado dos dados versionados.
- Não declarar sucesso com divergência numérica, erro de compilação, referência indefinida ou
  `Overfull \\hbox`.
- Preservar os produtos históricos de 104 registros, mas identificar sem ambiguidade quais
  produtos são históricos e quais são vigentes.
- Não criar outro PR e não fazer merge em `main` durante esta tarefa.
- Não apagar relatórios, dados brutos ou decisões que sustentem a rastreabilidade. Informações
  de continuidade comprovadamente obsoletas podem ser substituídas neste arquivo.

## Produtos já concluídos e preservados

- Coleta complementar: 6.728 ocorrências brutas, sendo 3.169 da Scopus, 1.559 da Web of Science
  e 2.000 do Crossref.
- Normalização e deduplicação contra o corpus original.
- Classificação determinística dos 4.889 registros novos únicos segundo o codebook RQ6.
- Revisão individual de título e resumo dos candidatos ao núcleo da sensibilidade.
- Incorporação de 12 novos registros e promoção de cinco registros já presentes no corpus,
  elevando o núcleo temático de 104 para 121.
- Geração, por Python, das tabelas e figuras identificadas pelo sufixo
  `_nucleo_ampliado_121`.
- Atualização preliminar do resumo, método, resultados, discussão, limitações e considerações
  finais com as novas contagens.

## Pendências científicas identificadas na auditoria de 13/07/2026

### 1. Consolidação técnica do PR

- Sincronizar a branch com `main` e resolver a condição não mergeável.
- Confirmar que o workflow não substituiu produtos vigentes de 121 por produtos históricos de
  104 registros.
- Validar conjuntamente `main.pdf`, `artigo.docx`, tabelas, figuras e arquivos auxiliares.
- Atualizar a descrição do PR para refletir a base atual e as pendências reais.

### 2. Integração metodológica da RQ6

- Inserir a RQ6 na introdução como questão complementar de sensibilidade.
- Acrescentar a RQ6 à matriz de alinhamento entre pergunta, seleção, extração e resultados.
- Corrigir a redação que ainda apresenta 104 registros como núcleo final vigente.
- Explicar que a camada bibliométrica de 372 registros permanece derivada da busca principal;
  incorporar nela os resultados de uma busca deliberadamente enriquecida para IA alteraria a
  estrutura temática observada.
- Diferenciar claramente classificação determinística, revisão individual de título e resumo e
  leitura integral.

### 3. Estratégia de busca e fluxo de seleção

- Unificar `latex-artigo/fontes/tabela_estrategia_busca.csv`, preservando a separação entre
  busca principal e busca de sensibilidade.
- Incluir as consultas, campos, datas e totais reais da rodada de sensibilidade.
- Atualizar `scripts/python/verificar_artigo.py` para recalcular e validar os dois blocos de
  busca, sem tratar a soma operacional como corpus homogêneo.
- Substituir o funil que termina em 104 por fluxo com dois braços: busca principal e busca de
  sensibilidade, convergindo no núcleo temático de 121.

### 4. Leitura integral dos 17 registros incorporados

- Identificar exatamente os 17 registros que diferenciam os núcleos de 104 e 121.
- Procurar versões legais em acesso aberto e documentar as tentativas.
- Extrair, quando disponíveis, contexto predial, problema, técnica computacional, dados,
  variável-alvo, métricas, validação, integração com decisão e limitações.
- Registrar página, seção, tabela ou figura de cada evidência incorporada.
- Não apresentar leitura de resumo como leitura integral.
- Produzir relatório conforme o padrão dos dois lotes anteriores de texto completo.

### 5. Síntese científica de IA/aprendizado de máquina

- Responder diretamente à RQ6.
- Distinguir previsão, diagnóstico, classificação, otimização e apoio à decisão.
- Verificar se os modelos alimentam critérios multicritério ou permanecem como módulos
  preditivos isolados.
- Avaliar necessidades de dados, interoperabilidade, explicabilidade, deriva e validação
  externa apenas quando sustentadas pelos estudos.
- Posicionar IA/aprendizado de máquina como possível camada de produção de evidências para os
  critérios, não como substituta da governança multicritério.
- Criar tabela comparativa compacta, preferencialmente como material suplementar.

### 6. Reprodutibilidade do pipeline vigente

- Fazer o verificador recalcular totais diretamente do núcleo e comparar resultados com texto,
  tabelas e gráficos.
- Revisar o workflow que ainda pode executar produtos orientados ao núcleo histórico de 104.
- Garantir que CI, pipeline Python e artigo utilizem explicitamente os produtos vigentes de 121.
- Preservar os produtos históricos sem permitir que sejam confundidos com os atuais.

### 7. Ajuste fino global do artigo

Executar somente depois das etapas anteriores:

- reduzir repetição dos mesmos estudos entre fundamentos, métodos e discussão;
- reforçar afirmações teóricas ainda pouco referenciadas;
- melhorar as transições entre bibliometria, síntese temática e protocolo;
- distinguir evidência extraída, síntese do autor e indicador operacional proposto;
- revisar tabelas extensas, resumo, abstract, palavras-chave e conclusão;
- controlar a extensão do texto, transferindo rastreabilidade detalhada para material
  suplementar quando necessário;
- realizar revisão final de coerência numérica, terminológica, bibliográfica e visual.

## Ordem de execução e critério de passagem

1. Consolidação técnica e documental do PR.
2. Arquitetura metodológica e RQ6.
3. Estratégia de busca e novo fluxo de seleção.
4. Leitura integral dos 17 registros.
5. Síntese científica da busca de sensibilidade.
6. Reprodutibilidade do pipeline vigente.
7. Ajuste fino global.

Durante as etapas de conteúdo, atualizar apenas fontes `.tex`, dados, scripts Python e
documentação. Por decisão do pesquisador em 13/07/2026, não regenerar nem editar `main.pdf` ou
`artigo.docx` por enquanto. A compilação integral, Biber, referências indefinidas,
`Overfull \\hbox` e conferência visual de PDF/DOCX serão executados conjuntamente após a
consolidação dos textos. Em cada etapa intermediária:

1. executar validações estáticas e verificações numéricas possíveis;
2. atualizar este arquivo;
3. fazer commit incremental na branch do PR #4;
4. não declarar validação de compilação ou visual antes da etapa acumulada correspondente.

## Registro de execução

### Etapa 1 — consolidação técnica e documental

- Plano e estado atual registrados no commit `837286d`.
- Descrição e título do PR #4 atualizados; removidas informações obsoletas.
- A comparação entre a branch e a `main` mostrou que os dois commits exclusivos da `main`
  alteram somente oito artefatos binários gerados pelo CI: `artigo.docx`, `main.pdf`, quatro
  figuras bibliométricas e duas planilhas.
- Os fontes LaTeX e scripts não divergem por causa desses dois commits.
- As versões da branch foram preservadas para não substituir produtos do núcleo vigente de 121
  por artefatos potencialmente associados ao núcleo histórico de 104.
- A incorporação formal da `main` permanece pendente porque o PR continua não mergeável; a
  resolução deve ocorrer depois de uma nova compilação validada dos fontes atuais.

### Etapa 2 — arquitetura metodológica e RQ6

Implementação iniciada:

- RQ6 formulada na introdução como verificação complementar, sem redefinir retrospectivamente a
  busca principal — commit `ccc0ff1`.
- RQ6 acrescentada à matriz de alinhamento metodológico.
- Camada bibliométrica de 372 explicitamente vinculada à busca principal.
- Núcleo original de 104 diferenciado do núcleo temático vigente de 121.
- Justificado que os resultados da busca deliberadamente enriquecida para IA não entram na
  estrutura bibliométrica geral.
- Funil existente rotulado como fluxo da busca principal até o núcleo original.
- Verificações de regressão adicionadas a `verificar_artigo.py` — commits `1db9d52` e
  `192d98e`.

Verificação estática por leitura dos arquivos passou para os cinco controles novos. A validação
completa por Python, LaTeX, Biber, inspeção de `Overfull \\hbox` e regeneração de PDF/DOCX
ainda precisa ser confirmada pelo workflow ou por checkout local.

### Etapa 3 — estratégia de busca e fluxo integrado

Implementação textual e documental concluída:

- `tabela_estrategia_busca.csv` ampliada para 26 linhas: 13 consultas principais, um
  enriquecimento manual por EID e 12 consultas de sensibilidade — commit `186a188`.
- Totais mantidos em blocos independentes: 12.118 ocorrências na busca principal e 6.728 na
  busca de sensibilidade.
- As strings originais e as dez consultas Crossref da sensibilidade foram preservadas
  integralmente.
- As strings nativas exatas da Scopus e da Web of Science na sensibilidade não constam dos
  arquivos recebidos; foram registradas como “Informação insuficiente para verificar”, sem
  reconstrução por inferência.
- `verificar_artigo.py` atualizado para validar rodada, base, número de consultas, datas,
  período, totais e lacunas documentais — commits `655a452` e `e6f89d8`.
- Metodologia reescrita para separar as finalidades das duas rodadas e impedir que 18.846 seja
  tratado como corpus homogêneo.
- Fluxo metodológico substituído por estrutura em dois braços, convergindo no núcleo vigente de
  121 registros — commits `9959589` e `f79005d`.
- Log de busca atualizado com as dez consultas Crossref verificadas e as duas lacunas de
  string nativa — commit `46e5a8c`.

A verificação estática confirmou 26 linhas, totais de 12.118 e 6.728, distribuição de consultas
4/4/5 na busca principal e 1/1/10 na sensibilidade, além das duas lacunas documentais esperadas.

### Etapa 4 — leitura integral pontual dos 17 registros incorporados

Implementação textual e documental concluída:

- A diferença exata entre o núcleo histórico de 104 e o núcleo vigente de 121 confirmou 17
  registros, documentados individualmente em
  `docs/RELATORIO_USO_TEXTO_COMPLETO_17_REGISTROS_IA_ML.md` — commit `9153034`.
- Foram localizados e consultados sete textos integrais em acesso aberto: REG_05418,
  REG_10348, REG_10391, REG_10862, REG_12351, REG_12451 e REG_12511.
- Dez registros permaneceram no nível de título e resumo: nove sem versão integral aberta
  verificável e um declarado aberto pelo editor, mas sem recuperação efetiva do conteúdo
  integral nesta sessão.
- Cinco dos sete textos lidos acrescentaram resultados quantitativos, desenho de validação ou
  limitações ausentes da evidência curta preservada no corpus.
- Cinco referências verificadas foram acrescentadas ao arquivo bibliográfico — commit
  `ff1f57c`.
- A Seção de métodos de apoio à decisão passou a responder diretamente à RQ6, distinguindo
  previsão, diagnóstico, classificação, otimização e uso como camada de evidência, sem tratar
  o módulo computacional como substituto da governança multicritério — commit `e74de83`.
- O método e as limitações registram agora três lotes pontuais, totalizando 37 textos
  integrais consultados, dos quais 19 forneceram evidências específicas — commits
  `a91a94b` e `8d05237`.
- O verificador passou a exigir o relatório, os 17 identificadores, as novas contagens e as
  cinco citações individuais — commit `8fad026`.

A validação estática cruzada dos 14 arquivos LaTeX, das 40 entradas bibliográficas, do
relatório e dos novos controles não encontrou citação sem referência, referência não citada
ou identificador ausente. O comando Python completo, LaTeX, Biber, controle de
`Overfull \\hbox` e inspeção visual permanecem deliberadamente adiados, conforme decisão
do pesquisador de consolidar primeiro os textos e não trabalhar no PDF por enquanto.

### Etapa 5 — síntese científica comparativa da busca de sensibilidade

Implementação textual e documental concluída:

- O relatório dos 17 registros passou a conter sete links diretos para os PDFs abertos
  disponibilizados pelos editores — commit `8beac5f`.
- Foi criada a matriz suplementar
  `latex-artigo/fontes/tabela_sintese_ia_ml_17.csv`, com identificador, DOI, função
  analítica predominante, técnica, contexto, variável-alvo, base documental, integração com
  decisão e limite verificável — commit `6de2579`.
- A classificação por função predominante resultou em oito registros de previsão, dois de
  previsão combinada à otimização, dois de diagnóstico/classificação e cinco de
  síntese/integração.
- A Seção de métodos explicita que a distribuição descreve o lote enriquecido, não a
  prevalência independente no campo, e posiciona os modelos como produtores de evidência
  para critérios — commit `ea065a2`.
- A discussão passou a separar acurácia preditiva de legitimidade decisória e a explicitar
  requisitos de dados, domínio de validade, responsabilização e contestabilidade —
  commit `253900d`.
- As considerações finais respondem diretamente à RQ6 e registram que nenhum dos 17 estudos
  demonstrou a cadeia completa entre treinamento, validação externa, ponderação
  multicritério, vetos e decisão pública auditável — commit `83dabd4`.
- O verificador passou a recalcular as 17 linhas, a distribuição funcional e a cobertura
  documental de sete textos integrais e dez registros baseados em título/resumo — commit
  `ff76146`.

A validação estática confirmou 17 linhas únicas, distribuição funcional 8/2/2/5, cobertura
documental 10/7 e sete links diretos. A execução completa de Python e a compilação continuam
adiadas para a etapa acumulada, sem alteração de PDF ou DOCX.

### Etapa 6 — reprodutibilidade do pipeline vigente

Implementação concluída nos fontes e na configuração:

- O gerador Python do núcleo ampliado passou a identificar os 17 incorporados pela diferença
  real entre os conjuntos de identificadores dos núcleos vigente e histórico, sem depender da
  posição das linhas — commit `5e61d71`.
- O gerador de planilhas de auditoria passou a publicar
  `nucleo_final_121_registros.csv/.xlsx` como produto vigente e a preservar
  `nucleo_final_104_registros.csv/.xlsx` como produto histórico — commit `5c52c86`.
- O workflow deixou de instalar ou executar R e passou a chamar
  `gerar_produtos_artigo_nucleo_ampliado.py` antes da verificação — commit `7a4da72`.
- Em pushes de branch e no PR, o workflow agora executa apenas os produtos Python e
  `verificar_artigo.py`. TeX, Biber, PDF e Word ficaram condicionados a execução manual ou
  push na `main`, respeitando o adiamento da compilação.
- O README principal passou a declarar a possível defasagem temporária de PDF/DOCX e a
  arquitetura atual de 121 registros — commit `4deb4de`.
- O README de referências passou a distinguir o núcleo vigente de 121 do histórico de 104 e
  a documentar o terceiro lote de leitura integral — commit `833b6a4`.
- O verificador ganhou controles de regressão para impedir execução de R no workflow,
  identificação posicional dos 17 registros ou publicação exclusiva do núcleo histórico —
  commit `0544647`.

A inspeção estática confirmou todos os novos controles. Como nenhuma execução de workflow
foi associada automaticamente aos commits produzidos pela interface de conteúdo, o gerador
Python foi executado em ambiente temporário reconstruído apenas com as entradas versionadas.
A execução confirmou 121 registros, 17 incorporados pela diferença entre conjuntos, bases
113/51/6, tipos documentais 90/20/11, aprendizado de máquina em 26 registros e ODS/ESG em
1/0. As 12 tabelas CSV geradas foram semanticamente idênticas às versões da branch. As cinco
imagens mantiveram dimensões idênticas; diferenças rasterizadas entre 3,6% e 6,7% dos canais
foram atribuídas ao ambiente de renderização, sem mudança nos dados ou na geometria dos
gráficos. Para evitar ruído binário, as imagens versionadas foram preservadas. Nenhum script
R foi executado e nenhum PDF ou DOCX foi alterado.

### Etapa 7 — ajuste fino global da escrita

Implementação iniciada:

- Resumo e abstract reestruturados em objetivo, método, resultados e contribuição, com os
  totais recalculados do pipeline e resposta compacta à RQ6 — commit `340054a`.
- Introdução ampliada para explicitar a lacuna entre diagnóstico técnico, sustentabilidade,
  digitalização e decisão pública, além da contribuição em três níveis — commit `afe46fe`.
- Fundamentos teóricos ajustados para distinguir plataforma informacional, modelo preditivo e
  decisão institucional, com integração das evidências de texto completo da sensibilidade —
  commit `b5a5710`.
- O filtro editorial do verificador foi corrigido para não confundir comando de caminho TikZ
  com travessão na prosa — commit `6e81714`.
- A conferência cruzada manteve 11 tabelas, 11 figuras, 40 referências citadas e nenhuma
  citação sem entrada bibliográfica.


### Etapa 7 — suporte bibliográfico das assertivas gerais

Foi aplicada a regra editorial solicitada pelo orientador: afirmações gerais ou teóricas
precisam de apoio bibliográfico; resultados calculados pelo próprio estudo, decisões
metodológicas declaradas e proposições explicitamente apresentadas como contribuição dos
autores não recebem citação externa artificial.

A conferência abrangeu todas as seções do artigo e concentrou alterações nos pontos em que
havia afirmações gerais sem apoio suficientemente próximo:

- a introdução passou a apoiar explicitamente decisões reativas, combinação de dados,
  integração multicritério e fragmentação entre diagnóstico, digitalização e decisão;
- os fundamentos passaram a citar a organização das correntes, a influência da
  manutenibilidade, o tratamento transversal do ciclo de vida e as funções dos métodos
  multicritério;
- a metodologia passou a apoiar as definições dos métodos e a distinção entre plataforma
  digital, modelo treinado e mecanismo decisório;
- a seção de aplicabilidade incorporou evidências de estudos de caso em universidades
  públicas;
- a matriz candidata passou a apoiar bibliograficamente elicitação de pesos e vetos
  normativos.

O acervo bibliográfico disponibilizado pelo pesquisador foi consultado de forma seletiva.
Três artigos foram acrescentados por aderência direta, após conferência de seus textos e
metadados: Lateef, Khamidi e Idrus (2010), Maia, Scheer e Freitas (2016) e Barbosa et al.
(2020). A bibliografia passou de 40 para 43 entradas; as 43 estão citadas e não há chave
citada sem entrada correspondente.

Commits incrementais desta conferência:

- `4bb0eee`: inclusão das três referências;
- `17a8acc`: suporte bibliográfico na introdução;
- `ef80516` e `12d96a8`: suporte bibliográfico nos fundamentos;
- `4e22b44`: definições e distinções metodológicas;
- `e921e5e`: evidências de casos universitários públicos;
- `cd97885`: fundamentação dos procedimentos candidatos do protocolo.

A execução de `python scripts/python/verificar_artigo.py` em cópia diagnóstica sincronizada
com a branch aprovou as verificações iniciais de estilo, estrutura, citações e bibliografia.
A execução não pôde alcançar as asserções numéricas porque a cópia reconstruída nesta
sessão não contém os grandes arquivos históricos de entrada, começando por
`03_PROCESSADOS/registros_normalizados.csv`. A conferência cruzada independente confirmou
13 seções, 43 entradas bibliográficas, 43 chaves citadas, nenhuma citação ausente e nenhuma
referência órfã. A execução integral do verificador permanece pendente em checkout completo.
PDF e DOCX não foram compilados nem alterados nesta etapa, conforme orientação vigente do
pesquisador.



### Etapa 7 — ajuste de discussão, limitações e conclusão

A continuação do ajuste fino preservou a regra de suporte bibliográfico e reforçou a
distinção entre resultados do corpus, interpretação e proposição dos autores:

- a discussão passou a responder explicitamente à RQ0, sem apresentar os componentes
  encontrados na literatura como modelo já transferível;
- a interpretação sobre ODS e ESG foi separada entre resultado lexical do corpus e
  compatibilidade com literatura externa;
- o protocolo e sua agenda de validação foram identificados como proposições do artigo;
- as limitações passaram a registrar a ausência das strings nativas exatas de Scopus e Web
  of Science na sensibilidade e a impossibilidade de interpretar o aumento de aprendizado
  de máquina como prevalência no campo;
- a conclusão deixou de atribuir eficácia antecipada ao protocolo, removeu prazos
  institucionais arbitrários e eliminou comentários editoriais sobre uma futura versão do
  artigo.

Commits incrementais:

- `c539dfe`: síntese, resposta à RQ0 e autoria na discussão;
- `d9056b0`: limites adicionais da busca de sensibilidade;
- `a0d123d`: conclusão mais científica e não prescritiva.

A conferência cruzada posterior manteve 13 seções, 43 entradas bibliográficas e 43 chaves
citadas, sem referências órfãs ou citações ausentes. Não foram introduzidos travessões na
prosa; as ocorrências de ` -- ` permanecem restritas aos comandos TikZ excluídos pelo
verificador. PDF e DOCX permaneceram inalterados.



### Etapa 7 — ajuste das seções de resultados e síntese

As seções de bibliometria, panorama, critérios, métodos, aplicabilidade e matriz foram
revisadas para melhorar a progressão analítica e reduzir repetição:

- a bibliometria passou a encerrar com uma transição explícita entre estrutura documental e
  síntese temática, sem atribuir maturidade decisória à coocorrência de termos;
- o panorama passou a distinguir composição documental, proveniência entre bases e
  qualidade da evidência;
- critérios, métodos e contextos passaram a responder explicitamente às RQ1, RQ2, RQ3 e
  RQ4;
- tecnologias digitais foram separadas de requisitos mínimos para aplicação do protocolo;
- as evidências de texto completo sobre integração digital, simulação e métodos decisórios
  foram consolidadas na seção de métodos;
- a discussão passou a remeter a essa consolidação, evitando repetir os mesmos estudos,
  números e exemplos;
- a matriz passou a explicitar sua contribuição arquitetural à RQ0 e a preservar a
  distinção entre especificação candidata e instrumento validado.

Commits incrementais:

- `869a850`: transição entre bibliometria e síntese;
- `c985c53`: delimitação da composição documental;
- `aaea9da`: respostas às RQ1 e RQ2;
- `602ace0`: compactação das evidências e separação entre tecnologia e requisito;
- `35546c4`: resposta à RQ4 e limite de transferência;
- `1b8318b`: contribuição da matriz para a RQ0;
- `a480507`: redução da repetição das leituras integrais na discussão.

A conferência estrutural posterior confirmou 13 seções, 11 tabelas, 11 figuras e nove
legendas quantitativas. Permanecem 43 entradas bibliográficas e 43 chaves citadas, sem
referências órfãs ou citações ausentes. Não foram identificados travessões na prosa nem
marcadores de rascunho. PDF e DOCX permaneceram inalterados.


## Etapa atual

**Etapa 7 — ajuste fino iniciado pelo resumo, introdução e fundamentos.**

A continuação revisará resultados, transições para a matriz, discussão, limitações e
considerações finais, preservando o modelo estrutural já consolidado. PDF e DOCX continuam
adiados para a compilação acumulada.
