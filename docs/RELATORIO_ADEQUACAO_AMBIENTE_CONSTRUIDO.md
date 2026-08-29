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
| Máx. 7.000 palavras (Introdução→Conclusões) | 9.600 (versão capítulo de tese) | Reestruturado. Contagem oficial no `.docx` compilado (ver Seção 8): **6.773 palavras** |
| Estrutura com títulos não numerados no texto (instruções) vs. numerados (template oficial) | 13 seções numeradas | Fundidas em 4: Introdução, Método de pesquisa, Resultados e discussão, Considerações finais. Numeração mantida (o template oficial usa "1 INTRODUÇÃO", "4 RESULTADOS E DISCUSSÕES", contradizendo o texto das instruções) |
| A4, espaço simples, Times New Roman 12, margens 3/2/3/2 cm, linhas numeradas contínuas | LaTeX já correto (margens e A4); Word gerado pelo pipeline padrão estava em página Carta, margens de 1", fonte Cambria/Calibri, sem numeração de linha | Corrigido no `.docx` por `scripts/python/ajustar_formato_word.py`: A4, margens 1701/1134 twips (3/2 cm), Times New Roman em todo o corpo, `lnNumType` contínuo. Confirmado por inspeção do XML |
| Word/OpenOffice/RTF, máx. 5 MB | Pipeline já gera `.docx` | `artigo.docx` final: 1,17 MB |
| Título ≤ 15 palavras, PT+EN | 13 palavras, com dois-pontos | "Priorização multicritério da manutenção sustentável em edificações públicas universitárias" (10 palavras) / "Multi-criteria prioritization of sustainable maintenance in public university buildings" — escolhido pelo autor entre 3 opções |
| Resumo/Abstract 100–200 palavras cada | 216/~215 | Cortados para 200/194 |
| 3–6 palavras-chave (revista) / 3–5 (template) | 5 em cada idioma, separadas por `;` | Mantidas 5; separador trocado para `.` conforme o template oficial |
| Referências NBR 6023:2018, alfabética, >3 autores → 1º + et al. | PDF: `biblatex` `style=abnt`. Word (até 2026-08-27): `pandoc --citeproc` sem CSL, saía em inglês ("and", sem "et al.") | **Corrigido em 2026-08-28** (Seção 8): `latex-artigo/abnt.csl` (estilo oficial do projeto Citation Style Language, NBR 6023/NBR 10520) ligado via `pandoc --csl`; Word e PDF agora equivalentes. Verificado visualmente: ordem alfabética, "et al." a partir de 4 autores, conectivo "e" em vez de "and", DOIs como links |
| Citações NBR 10520 (2023 no site oficial; o template baixado cita 2001) | `\textcite`/`\parencite` (PDF) e `abnt.csl` (Word, `et-al-min=4`, ambos alinhados a NBR 10520:2023) | Resolvido — adotado 2023 (página institucional, mais recente) em ambos os formatos |
| Tabelas/figuras com legenda e chamada no texto | 11 tabelas + 11 figuras | Preservadas integralmente, nenhuma removida; **verificado visualmente**: nenhuma tabela cortada, nenhuma quebra de página problemática |
| Figuras ≥300 dpi, jpg/png, coloridas | 14 PNG conferidos, todos exatamente 300 dpi | Conforme |
| Avaliação duplo-cega: remover autoria do arquivo e propriedades | `\author{...}` no `main.tex`; `dc:creator` populado no `.docx` gerado | `main_anonimo.tex` compilado com sucesso (PDF sem nome/afiliação); `artigo_anonimo.docx` gerado com parágrafo de autoria removido e `docProps` limpos (verificado: `dc:creator` vazio) |
| Comitê de ética só se pesquisa envolver seres humanos | Revisão bibliométrica, sem coleta com seres humanos | Não aplicável |
| Ciência Aberta | Repositório GitHub público | Declaração sustentável |
| Declaração de uso de IA no Método, se houve uso | Nenhuma | Inserida no Método, confirmada pelo autor |
| Agradecimento/financiamento só na versão pós-aceite | Nenhum no corpo atual | Preparado em `docs/AGRADECIMENTO_POS_ACEITE.md` |

## 3. Núcleo científico preservado (verificação automatizada)

- 44 referências no `references.bib` (as 43 do corpus + o depósito de dados
  suplementares no Zenodo, DOI 10.5281/zenodo.22151875, citado na declaração
  de disponibilidade de dados ao final do artigo); auditoria automática: 0
  citações sem entrada, 0 entradas não citadas.
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

**Contagem oficial de palavras**: ver Seção 8 (auditoria de 2026-08-28) para
o método reproduzível final e o número atual — **6.773 palavras**, com script
dedicado versionado no repositório.

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

1. Confirmar se há taxa de publicação aplicável (isenção, R$ 350 ou R$ 700,
   conforme associação à ANTAC) — informação insuficiente para verificar a
   partir dos fontes consultados.
2. Confirmar com o orientador a caracterização do uso de IA (Seção 8.9): a
   declaração atual cobre apenas esta etapa de preparação para submissão
   (2026-08-27 em diante), não o histórico de curadoria de dados de
   julho/2026 do mesmo repositório.
3. Revisões futuras de texto (mesmo pequenas) devem reconferir a contagem de
   palavras com `scripts/python/contar_palavras_artigo.py` antes do envio
   final — a margem atual (227 palavras, ver Seção 8.6) não é folgada.

## 8. Auditoria independente e correções de 2026-08-28

Uma auditoria independente do `artigo.docx` então publicado encontrou 12
problemas editoriais não cobertos pela Seção 2–7 (produzida numa rodada
anterior). Todos foram corrigidos nesta branch, com commits pequenos e
auditáveis, e a correção de cada um foi validada por regeneração completa do
pipeline (localmente com Pandoc/LibreOffice, e depois pelo build oficial do
GitHub Actions, que tem TeX Live/Biber/pdflatex completos). Durante a
correção, a inspeção visual página a página encontrou mais 4 problemas reais
não cobertos pela lista original de achados; todos também corrigidos, dentro
do escopo desta tarefa.

### 8.1 Citações e referências do Word em estilo ABNT

Corrigido adicionando `latex-artigo/abnt.csl` (estilo
"Associação Brasileira de Normas Técnicas (Português - Brasil)" do
repositório oficial do projeto [Citation Style
Language](https://github.com/citation-style-language/styles), o mesmo
mantenedor usado por Zotero/Mendeley) e ligando via `pandoc --csl=abnt.csl`
em `scripts/python/13_preparar_word.py`. O estilo usa `default-locale="pt-BR"`
(traduz "and" para "e"), `et-al-min="4"` (compatível com NBR 10520:2023) e
ordena a bibliografia por autor (NBR 6023:2018). PDF (via `biblatex-abnt`) e
Word (via este CSL) ficam equivalentes quanto a citações e referências.

### 8.2 Resíduo `(lr)1-6` na Tabela 4 (e perda do rótulo do subtotal)

A investigação mostrou que o problema era mais sério do que um resíduo
visual: o Pandoc não só deixava `\cmidrule(lr){1-6}` como texto cru, como
descartava por completo o conteúdo de `\multicolumn{4}{r}{Subtotal da busca
principal}` — a linha de subtotal ficava sem o rótulo. Corrigido
pré-processando uma cópia temporária dos `.tex` (sem tocar os fontes que o
PDF usa) antes do Pandoc rodar: `\toprule`/`\midrule`/`\bottomrule`/
`\cmidrule` são removidos, e `\multicolumn{N}{...}{texto}` vira "texto" +
células vazias na posição correta.

### 8.3 Quebra de tabela sem cabeçalho repetido

Corrigido marcando a primeira linha de cada uma das 11 tabelas como
cabeçalho repetido (`w:tblHeader`) e todas as linhas como indivisíveis
(`w:cantSplit`), para nenhuma linha (sobretudo as de subtotal) ficar cortada
ou órfã entre páginas.

### 8.4 Numeração de seções ausente no Word

O LaTeX numera `\section`/`\subsection` por padrão (sem alteração de
`secnumdepth`), e as remissões em prosa (`Seção~\ref{sec:x}`) já resolviam
para o número certo no PDF. Corrigido adicionando `pandoc --number-sections`
e estendendo a resolução de referências cruzadas para rótulos `sec:` (antes
só cobria `tab:`/`fig:`), replicando os dois contadores de figura do LaTeX
(um para `\caption{}` normal, outro para o contador customizado `\thegrafico`
usado por `\captiongrafico{}`) para não numerar remissões erradas.

### 8.5 "Seis dimensões e 15 critérios"

Reintroduzido de forma objetiva na abertura do parágrafo que antecede a
Tabela 8 (critérios de priorização), sem alterar nomes, valores ou
frequências.

### 8.6 Contagem de palavras

Script novo e reproduzível: `scripts/python/contar_palavras_artigo.py`
(`python scripts/python/contar_palavras_artigo.py [artigo.docx]`). Conta
palavras visíveis entre os títulos "Introdução" e "Referências", incluindo
texto de tabelas (método mais conservador — conta mais texto, não menos).
Contagem antes das correções desta seção (medida com o mesmo script sobre o
`artigo.docx` de 2026-08-27, antes de qualquer edição desta auditoria):
**6.558 palavras** — número mais baixo que o relatado anteriormente (6.890)
porque aquela versão já tinha os defeitos de conteúdo descritos nas Seções
8.2 e 8.9 (legendas de tabela ausentes, notas de fonte ausentes), ou seja, o
6.890 relatado antes não é diretamente comparável a este método. Contagem
final, após todas as correções desta auditoria (incluindo a restauração de
conteúdo que estava sendo perdido, como legendas e notas de fonte das 11
tabelas): **6.773 palavras**, margem de 227 frente ao limite de 7.000,
abaixo da meta conservadora de 6.880. Verificação automatizada em
`scripts/python/verificar_artigo_word.py`.

### 8.7 Repetições mecânicas

A cadeia "evidência científica, dimensão, critério, indicador observável,
parametrização multicritério futura, veto não compensatório e decisão
pública rastreável" foi mantida por extenso só na Introdução (onde
apresenta a contribuição central); as outras 3 ocorrências (Introdução
novamente, Resultados, Considerações finais) foram reformuladas em versões
mais curtas. O mesmo para o eco de "eficiência, desempenho e edificações
verdes... para BIM...".

### 8.8 Formulações categóricas/promocionais

Suavizadas, sem mudar a conclusão científica, com marcadores epistêmicos
("os resultados sugerem", "essa leitura sugere") e explicitando que a
transição de governança depende de validação institucional futura, nos 3
trechos apontados (Considerações finais ×2, Resultados e discussão ×1).

### 8.9 Declaração de uso de IA

A frase anterior dizia uso "exclusivamente na revisão ortográfica, textual e
de adequação formal". A frase atual declara reestruturação editorial,
condensação textual, revisão linguística e adequação formal — o que de fato
está sendo feito nesta etapa de preparação para submissão —, mantém explícita
a ausência de uso em concepção da pesquisa/coleta de dados/definição do
corpus/codificação/cálculo/criação de evidências, e registra que as
alterações propostas foram revisadas e aprovadas pelo autor. Nome da
ferramenta/modelo mantido ("Claude Code, Anthropic, modelo Claude Sonnet 5")
por ser verificável — é o que produziu exatamente este conjunto de edições.

**Achado adicional, fora do escopo da frase (registrado para o autor
decidir, não alterado por conta própria)**: o histórico completo do
repositório (antes desta branch) mostra 26 commits, de 2026-07-11/12, com
trailer `Co-Authored-By: Claude Sonnet 5` ou `Claude Fable 5
<noreply@anthropic.com>`, cobrindo consolidação de corpus, deduplicação e
classificação de registros — uso mais amplo que "revisão ortográfica",
embora anterior e fora do escopo temporal desta branch de submissão (criada
em 2026-08-27). Nenhuma dessas 26 commits pertence à preparação deste
manuscrito para a Ambiente Construído. Fica como pendência do autor decidir
se quer mencionar esse histórico em algum outro documento (ex.: declaração
de ciência aberta do repositório), fora do escopo desta declaração pontual
no Método.

### 8.10 Formatação automatizada do Word

`scripts/python/ajustar_formato_word.py` (A4, margens 3/2/3/2 cm, Times New
Roman 12, numeração contínua de linha) era aplicado manualmente após a
geração do Word. Integrado a `13_preparar_word.py` (chamado logo após o
LibreOffice resalvar o arquivo), para todo `artigo.docx` gerado — no CI ou
localmente — já sair formatado, sem passo manual.

### 8.11 Equações, símbolos e formatação de texto

Verificados: `R² = 0,83` (na prosa) sobrevive como fórmula nativa do Word
(objeto OMML), R$, %, kWh/m², acentuação, travessão/hífen, siglas — todos
preservados. Dois problemas reais adicionais, fora da lista original,
encontrados por inspeção visual e corrigidos (mesma causa-raiz das Seções
8.2/8.9: o Pandoc descarta conteúdo que não reconhece dentro do
reconstrutor de tabela):

- **Expoentes em células de tabela** ("R$/m²", "kWh/m²" na Tabela 11)
  desapareciam por completo (viravam "R$/m", "kWh/m") porque
  `paragraph.text` do python-docx só lê texto simples, não o objeto de
  fórmula nativo que o Pandoc cria para `$^2$`. Corrigido convertendo para o
  caractere Unicode de sobrescrito antes do Pandoc rodar.
- **Itálico em células de tabela** (ex.: "*digital twin*", nomes de
  periódicos indexados como *Journal*/*JOUR*) virava texto sem formatação.
  Corrigido com um marcador de área de uso privado Unicode (compatível com
  XML, ao contrário do primeiro marcador tentado) que preserva o itálico
  só dentro das 11 tabelas — fora delas o Pandoc já converte `\textit{}`
  nativamente e não foi tocado.

**Dois achados adicionais fora da lista original, também corrigidos:**

- **Especificação de coluna solta como texto visível**: a linha
  `>p2.1cm >p2.1cm ... Y` da definição de colunas da `tabularx` às vezes
  sobrava como parágrafo próprio, visível antes de várias tabelas (não só a
  4). Corrigido detectando e removendo esses parágrafos.
- **Nota de fonte ausente em todas as 11 tabelas**: `\fonteautor` ("Fonte:
  elaborado pelo autor.") e a nota metodológica adicional das Tabelas 4 e 11
  desapareciam por completo do Word (mesma causa-raiz: comandos de
  espaçamento/tamanho de fonte que o Pandoc não entende dentro do fallback
  de tabela). Corrigido com a mesma técnica de marcador de texto simples
  antes do Pandoc rodar, reconstruído depois como parágrafo pequeno e
  itálico logo após a tabela.

### 8.12 Verificadores automatizados

Novo `scripts/python/verificar_artigo_word.py`, chamado a partir de
`verificar_artigo_integrado.py` (que já roda em todo push do CI). Cobre,
contra o `artigo.docx` final: frase "seis dimensões"/"15 critérios";
ausência de resíduo LaTeX (`\cmidrule`/`\multicolumn`/"(lr)1-6"/etc.) e de
remissão cruzada não resolvida; ausência de `" and "` em citação
autor-data; exatamente 44 referências, 11 tabelas, 11 legendas de tabela e
11 legendas de figura/gráfico (nenhuma sem número); títulos de seção
numerados; A4/margens/Times New Roman/numeração de linha; contagem de
palavras (< 7.000, margem ≥ 100, meta ≤ 6.880); limitações de rastreamento
de citações e literatura cinzenta declaradas como não realizadas, também no
texto final do Word; declaração de uso de IA presente com a ressalva de
escopo; e paridade mínima de conteúdo (números-âncora do corpus ainda
presentes no Word).

### 8.13 Validação de ponta a ponta

- `verificar_artigo.py` e `verificar_artigo_integrado.py` (que agora inclui
  `verificar_artigo_word.py`): sem divergências.
- Build oficial via GitHub Actions (`workflow_dispatch`, TeX Live completo):
  PDF e PDF anonimizado compilados sem erro, Word e Word anonimizado
  gerados e validados, nenhum `Overfull \hbox`, produtos publicados de volta
  na branch pelo próprio workflow.
- Inspeção visual página a página: renderizado `main.pdf` (25 páginas) e o
  PDF de inspeção gerado a partir do `artigo.docx` final via LibreOffice (30
  páginas — diferença esperada de paginação entre LaTeX e Word/LibreOffice,
  não de conteúdo), comparando capa/resumo/abstract, a Tabela 4 completa
  (cabeçalho repetido, subtotal correto, nota de fonte), o Gráfico 6 com
  legenda numerada e a frase dos 15 critérios, os 2 fluxogramas TikZ, a
  declaração de uso de IA, e a lista de 43 referências terminando sem corte.
- `artigo_anonimo.docx`: ZIP íntegro, nenhum marcador de autoria no texto,
  `docProps/core.xml` sem `dc:creator`/`cp:lastModifiedBy`.
- Tamanhos finais: `artigo.docx` ≈1,17 MB, `artigo_anonimo.docx` ≈1,17 MB,
  `main.pdf` ≈1,23 MB, `main_anonimo.pdf` ≈1,23 MB — todos abaixo do limite
  de 5 MB.

### 8.14 Pendência de infraestrutura (não relacionada ao conteúdo)

O passo "Publicar produtos como artefato" do workflow falha desde antes
desta auditoria por cota de armazenamento de artefatos do GitHub Actions da
conta esgotada ("Artifact storage quota has been hit"). Isso não impede a
entrega: o PDF/Word oficiais são commitados diretamente na branch pelo passo
anterior (`Publicar produtos da compilação completa`), que sempre teve
sucesso. Ação recomendada ao autor (fora do escopo desta tarefa): limpar
artefatos antigos de outras execuções ou aguardar o recálculo de cota do
GitHub (6–12h) se quiser também o artefato de download do próprio Actions.

### 8.15 Citação do dataset suplementar depositado no Zenodo (2026-08-29)

O autor depositou o pacote de dados brutos/intermediários/finais no Zenodo
(DOI 10.5281/zenodo.22151875) e pediu para citá-lo no artigo. Alterações:

- Nova entrada `oliveira_dadosuplementares_2026` em `latex-artigo/references.bib`
  (tipo `@misc`, com `doi`, `url` e `publisher = Zenodo`).
- Nova subseção não numerada "Disponibilidade de dados" ao final de
  `latex-artigo/sections/04_consideracoes_finais.tex`, citando essa entrada
  via `\parencite`. Isso eleva a bibliografia de 43 para 44 referências.
- `scripts/python/verificar_artigo_word.py` atualizado para exigir 44
  referências na bibliografia do Word (era 43).
- `scripts/python/12_gerar_lista_referencias.py` exige que toda entrada do
  `.bib` esteja citada no `.tex` e vice-versa; como a nova entrada agora está
  citada, o build deve passar sem alterações adicionais nesse script.

**Problemas encontrados na página do Zenodo que só o autor pode corrigir**
(edição de metadados exige login na conta Zenodo do autor):

1. **Nome do autor malformado**: o campo "Creators" está gravado como
   "de Oliveira, Adinailson Guimarães de Oliveira" (sobrenome duplicado).
   Deveria ser "Oliveira, Adinailson Guimarães de".
2. **Coautor ausente**: Fabricio Berton Zanchi não está listado como
   criador/coautor do depósito, embora conste como coautor do artigo.
3. **Descrição cortada no meio da frase**: o último parágrafo termina em
   "Ao citar este conjunto de dados, referencie também o artigo publicado"
   — falta o final ("na revista Ambiente Construído."). Confirmado via
   `GET https://zenodo.org/api/records/22151875`, não é artefato de
   renderização.

Nenhuma dessas três correções foi feita por esta sessão: exigem login na
conta Zenodo do autor, fora do escopo de acesso desta tarefa. Depois de
corrigidas, o DOI/URL citados no `references.bib` continuam válidos (Zenodo
mantém o mesmo DOI de versão ao editar metadados sem trocar arquivos).
