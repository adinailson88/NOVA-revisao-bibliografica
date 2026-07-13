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

Ao final de cada etapa:

1. executar `python scripts/python/verificar_artigo.py`;
2. compilar integralmente com LaTeX e Biber;
3. verificar referências indefinidas e `Overfull \\hbox`;
4. conferir visualmente PDF e DOCX quando alterados;
5. atualizar este arquivo;
6. fazer commit e push incremental na branch do PR #4.

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

## Etapa atual

**Etapa 2 — arquitetura metodológica e RQ6, aguardando validação completa.**

Depois da validação, a próxima etapa será unificar a estratégia de busca e construir o fluxo de
seleção em dois braços, convergindo no núcleo temático de 121 registros.
