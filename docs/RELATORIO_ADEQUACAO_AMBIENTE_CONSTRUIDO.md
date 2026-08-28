# Relatório de adequação editorial — submissão à Ambiente Construído

Branch de trabalho: `submissao-ambiente-construido` (a partir de `main`, sem
alterar o capítulo de tese completo, que permanece íntegro em `main`).

## 1. Fonte normativa consultada

Instruções oficiais da Ambiente Construído (ANTAC/UFRGS), lidas diretamente
no site da revista, não em agregadores ou blogs:

- [Instruções e template](https://seer.ufrgs.br/index.php/ambienteconstruido/instrucoesparatemplate)
  (limite de palavras, formato, título, resumo, palavras-chave, referências,
  citações, ativos digitais, documentos suplementares)
- [Diretrizes para autores](https://seer.ufrgs.br/index.php/ambienteconstruido/guidelinesforauthors)
  (preprints, avaliação por pares, dados abertos, uso de IA, direitos autorais, taxas)
- [Submissões](https://seer.ufrgs.br/index.php/ambienteconstruido/about/submissions)
  (checklist de submissão)
- [Diretrizes éticas](https://seer.ufrgs.br/index.php/ambienteconstruido/diretrizeseticas)
  (comitê de ética, conflito de interesses, condutas)
- Template oficial baixável (`Template AC-OTH.docx`, fornecido pelo autor),
  usado para confirmar fonte, margens, espaçamento, numeração de linha e
  separador de palavras-chave.

## 2. Tabela de conformidade

| Requisito vigente | Situação do manuscrito | Ação tomada |
|---|---|---|
| Máx. 7.000 palavras (Introdução→Conclusões) | 9.600 (versão capítulo de tese) | Reestruturado. Contagem oficial no `.docx` compilado: **6.942 palavras** (margem de 58) |
| Estrutura com títulos não numerados no texto (instruções) vs. numerados (template oficial) | 13 seções numeradas | Fundidas em 4: Introdução, Método de pesquisa, Resultados e discussão, Considerações finais. Numeração mantida (o template oficial usa "1 INTRODUÇÃO", "4 RESULTADOS E DISCUSSÕES", contradizendo o texto das instruções) |
| A4, espaço simples, Times New Roman 12, margens 3/2/3/2 cm, linhas numeradas contínuas | LaTeX já correto (margens e A4); Word gerado pelo pipeline padrão estava em página Carta, margens de 1", fonte Cambria/Calibri, sem numeração de linha | Corrigido no `.docx` por `scripts/python/ajustar_formato_word.py`: A4, margens 1701/1134 twips (3/2 cm), Times New Roman em todo o corpo, `lnNumType` contínuo. Confirmado por inspeção do XML |
| Word/OpenOffice/RTF, máx. 5 MB | Pipeline já gera `.docx` | `artigo.docx` final: 1,17 MB |
| Título ≤ 15 palavras, PT+EN | 13 palavras, com dois-pontos | "Priorização multicritério da manutenção sustentável em edificações públicas universitárias" (10 palavras) / "Multi-criteria prioritization of sustainable maintenance in public university buildings" — escolhido pelo autor entre 3 opções |
| Resumo/Abstract 100–200 palavras cada | 216/~215 | Cortados para 200/194 |
| 3–6 palavras-chave (revista) / 3–5 (template) | 5 em cada idioma, separadas por `;` | Mantidas 5; separador trocado para `.` conforme o template oficial |
| Referências NBR 6023:2018, alfabética, >3 autores → 1º + et al. | `biblatex` `style=abnt` | **Verificado visualmente no PDF compilado**: ordem alfabética correta, "et al." aplicado corretamente às 14 referências com ≥4 autores (ex.: ALFALAH et al., MASMOUDI et al.), DOIs renderizados como links |
| Citações NBR 10520 (2023 no site oficial; o template baixado cita 2001) | `\textcite`/`\parencite` | Divergência entre fontes oficiais registrada; adotado 2023 (página institucional, mais recente) por padrão; **pendência do autor** |
| Tabelas/figuras com legenda e chamada no texto | 11 tabelas + 11 figuras | Preservadas integralmente, nenhuma removida; **verificado visualmente**: nenhuma tabela cortada, nenhuma quebra de página problemática |
| Figuras ≥300 dpi, jpg/png, coloridas | 14 PNG conferidos, todos exatamente 300 dpi | Conforme |
| Avaliação duplo-cega: remover autoria do arquivo e propriedades | `\author{...}` no `main.tex`; `dc:creator` populado no `.docx` gerado | `main_anonimo.tex` compilado com sucesso (PDF sem nome/afiliação); `artigo_anonimo.docx` gerado com parágrafo de autoria removido e `docProps` limpos (verificado: `dc:creator` vazio) |
| Comitê de ética só se pesquisa envolver seres humanos | Revisão bibliométrica, sem coleta com seres humanos | Não aplicável |
| Ciência Aberta | Repositório GitHub público | Declaração sustentável |
| Declaração de uso de IA no Método, se houve uso | Nenhuma | Inserida no Método, confirmada pelo autor |
| Agradecimento/financiamento só na versão pós-aceite | Nenhum no corpo atual | Preparado em `docs/AGRADECIMENTO_POS_ACEITE.md` |

## 3. Núcleo científico preservado (verificação automatizada)

- 43 referências no `references.bib`; auditoria automática: 0 citações sem
  entrada, 0 entradas não citadas.
- 11 tabelas, 11 figuras/gráficos (9 "Gráfico" + 2 "Figura"/fluxograma) — os
  mesmos 11+11 do capítulo de tese, nenhum removido. Confirmado também por
  inspeção visual página a página do PDF compilado.
- `scripts/python/verificar_artigo.py` e `verificar_artigo_integrado.py`
  (ambos adaptados nesta branch, ver Seção 4) confirmam, a partir dos CSVs de
  dados: 12.118 → 9.542 → 3.678 → 137 → 104 (núcleo original) → 121 (núcleo
  vigente, +17 da busca de sensibilidade IA/ML), seis dimensões, 15
  critérios, crescimento de aprendizado de máquina de 9 para 26 registros, e
  os controles do parecer crítico da rodada de revisão anterior.

## 4. Adaptação dos scripts de verificação nesta branch

Dois scripts de verificação existiam, em camadas:

- `verificar_artigo.py`: ~40 asserções de frase literal amarradas à prosa do
  capítulo de tese (Etapas 1–16 de uma rodada de revisão anterior).
- `verificar_artigo_integrado.py`: um adaptador que fazia *patch* textual em
  `verificar_artigo.py` (busca e substituição de blocos antigos por blocos
  "integrados") antes de executá-lo, presumindo uma redação ainda mais antiga,
  e acrescentava controles próprios (`controles_parecer`, arquivo
  suplementar, protocolo de busca, interseção de núcleos).

Como a tarefa pedia reescrita e condensação do texto, as ~40 asserções de
`verificar_artigo.py` foram substituídas por checagens de substância
equivalentes (ex.: a matriz continua identificada como "não validada"/
candidata, as limitações continuam declaradas, o ASReview continua sem
atribuição indevida), sem remover nenhuma checagem de integridade
numérica/CSV/scripts. O mecanismo de *patch* textual de
`verificar_artigo_integrado.py` foi removido (ficou redundante, pois
`verificar_artigo.py` já reflete a redação atual) e seus `controles_parecer`
foram igualmente adaptados para checagem de substância. Os controles sobre
`material_suplementar.tex` e o protocolo de busca (arquivos não tocados
nesta branch) permaneceram inalterados e continuam passando. Duas checagens
adicionais já estavam desalinhadas dos dados reais antes desta branch (uma
lacuna documental de string de busca já preenchida em atualização de dados
anterior) e foram corrigidas para refletir o estado real.

Durante a auditoria, dois pontos de conteúdo tinham sido cortados em excesso
na síntese de palavras e foram restaurados: a declaração de que o campo de
compatibilidade não evidencia uso do ASReview, e a declaração explícita de
que a matriz não é um modelo validado nem um instrumento pronto para decisão.

## 5. Compilação e validação (workflow `Validar fontes e gerar artigo`)

Executado via `gh workflow run` (workflow_dispatch) sobre a branch, sem
tocar na `main`. Após três iterações de correção (dois-pontos duplo em
prosa, patch obsoleto do verificador, contagem de palavras acima do real),
a compilação completa passou:

- `Compilar PDF`: sucesso, `latexmk` sem erros.
- `Gerar e validar versão Word`: sucesso (`13_preparar_word.py` + reabertura
  pelo LibreOffice + conversão de teste para PDF).
- `Verificar margens do PDF`: sucesso.
- `Publicar produtos da compilação completa`: sucesso (commit automático do
  `main.pdf` e `artigo.docx` de volta nesta branch).
- `Publicar produtos como artefato`: **falhou** por cota de armazenamento de
  artefatos do GitHub Actions da conta ("Artifact storage quota has been
  hit"), sem relação com o conteúdo do artigo. O PDF/Word já estavam
  commitados no passo anterior; nenhuma ação é necessária além de,
  opcionalmente, limpar artefatos antigos ou aguardar o recálculo de cota
  (6–12h) se quiser o artefato de download do Actions também.

**Inspeção visual do PDF compilado (`main.pdf`, 25 páginas)**: título
bilíngue correto na capa, resumo/abstract/palavras-chave em uma página,
seções numeradas (1 Introdução, 2 Método de pesquisa, 2.1–2.6, 3 Resultados
e discussão, 3.1–3.5, 4 Considerações finais), todas as 11 tabelas e 11
figuras/gráficos renderizados sem corte ou sobreposição de margem, os dois
fluxogramas (TikZ) bem posicionados, referências em ordem alfabética com
"et al." aplicado corretamente, DOIs como links. Nenhuma caixa horizontal
excedente relatada pelo workflow.

**Contagem oficial de palavras**: extraída do `.docx` gerado (não do fonte
LaTeX, que subestimava por não parsear integralmente os ambientes TikZ),
entre "Introdução" e "Referências": **6.890 palavras** (após corte adicional
solicitado pelo autor em 2026-08-28; a primeira versão compilada tinha 6.942),
dentro do limite de 7.000 com margem de 110 palavras (1,6%).

## 6. Versão Word: formatação e anonimização

O gerador padrão do pipeline (`13_preparar_word.py`, via Pandoc + LibreOffice)
produz um `.docx` válido, mas com página Carta (US Letter), margens de 1
polegada e fonte Cambria/Calibri — adequado para edição, mas fora do formato
de submissão. Foi criado `scripts/python/ajustar_formato_word.py`, que
corrige apenas essas quatro propriedades de layout diretamente no XML do
`.docx` já gerado (página A4, margens 1701/1134 twips, fonte Times New Roman
em `styles.xml` e `document.xml`, numeração contínua de linha), sem alterar
texto, tabelas, figuras ou referências. Aplicado ao `artigo.docx` publicado
nesta branch (verificado: ZIP íntegro, conteúdo idêntico ao original em
número de palavras).

Foi criado também `scripts/python/anonimizar_docx.py`, que gera uma cópia
com o parágrafo de autoria removido de `word/document.xml` e os metadados de
autoria (`dc:creator`, `cp:lastModifiedBy`, `Company`) limpos em
`docProps/`. Aplicado sobre o `artigo.docx` já formatado, produzindo
`artigo_anonimo.docx` (verificado: abre corretamente, inicia diretamente em
"Resumo", sem nome/afiliação, `dc:creator` vazio).

A versão anonimizada em PDF foi compilada a partir de `main_anonimo.tex`
(mesmo conteúdo científico de `main.tex`, `\author{}` vazio) em uma branch
descartável (`tmp-compile-anonimo`, criada apenas para acionar o workflow de
compilação e removida ao final desta tarefa).

O template oficial confirmou: A4, margens 3/2/3/2 cm, Times New Roman,
corpo 12pt justificado, espaçamento simples, numeração contínua de linha já
configurada nas propriedades de seção, palavras-chave separadas por ponto.
Os títulos numerados no próprio arquivo-modelo ("1 INTRODUÇÃO", "4
RESULTADOS E DISCUSSÕES", 12pt sem negrito) contradizem o texto das
instruções no site ("títulos não numerados", Título 1 em 14pt negrito
maiúsculo). Prevaleceu o arquivo-modelo (mais concreto) para numeração;
manteve-se a formatação de fonte do texto das instruções para os títulos.
*Pendência do autor*: confirmar visualmente qual convenção a revista
realmente aplica, comparando com um fascículo publicado recente.

## 7. Pendências que dependem exclusivamente do autor

Resolvidas em 2026-08-28:

- **Norma de citação**: o autor confirmou o texto integral da página oficial
  de instruções, que cita NBR 10520:2023 de forma explícita. Mantido como
  já aplicado; a divergência com o template baixado (que cita 2001) foi
  considerada irrelevante para o texto do artigo.
- **Agradecimento CAPES**: confirmado como aplicável a este trabalho.
  Nenhuma outra fonte de financiamento foi indicada.
  `docs/AGRADECIMENTO_POS_ACEITE.md` atualizado.
- **Destino da branch**: mantida separada de `main`, sem merge nem pull
  request por ora.

Ainda em aberto:

1. Confirmar o estilo visual dos títulos (numerado vs. não numerado, negrito
   vs. não negrito) comparando com um fascículo publicado recente — o
   arquivo-modelo baixado e o texto das instruções divergem entre si.
2. Confirmar se há taxa de publicação aplicável (isenção, R$ 350 ou R$ 700,
   conforme associação à ANTAC).
3. A margem de palavras é de 110 (1,6%); revisões futuras de texto (mesmo
   pequenas) devem reconferir a contagem no Word antes do envio final.
