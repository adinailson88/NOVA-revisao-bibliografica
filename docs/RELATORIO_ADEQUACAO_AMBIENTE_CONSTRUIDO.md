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
| Máx. 7.000 palavras (Introdução→Conclusões) | 9.600 (versão capítulo de tese) | Reestruturado para ~7.001 palavras (contagem pandoc); auditoria final no Word pendente (Seção 5) |
| Estrutura com títulos não numerados no texto final, mas título/objetivo/lit., método claro, resultados+discussão substanciais, conclusões destacadas | 13 seções numeradas | Fundidas em 4: Introdução, Método de pesquisa, Resultados e discussão, Considerações finais. Numeração mantida no LaTeX (necessária para os `\ref` internos); a versão Word de submissão deve remover a numeração visível dos títulos (ver Seção 6) |
| A4, espaço simples, Times New Roman 12, margens 3/2/3/2 cm, linhas numeradas contínuas | Margens já corretas no LaTeX; fonte `lmodern` (não Times); sem numeração de linha | Confirmado via template oficial (margens em twips = 3/2/3/2 cm exatos); fonte e numeração de linha aplicadas na geração do Word (script `13_preparar_word.py`, ver Seção 6) |
| Word/OpenOffice/RTF, máx. 5 MB | Pipeline já gera `.docx` | Reaproveitado, ver Seção 5 |
| Título ≤ 15 palavras, PT+EN | 13 palavras, com dois-pontos | Substituído por "Priorização multicritério da manutenção sustentável em edificações públicas universitárias" (10 palavras) / "Multi-criteria prioritization of sustainable maintenance in public university buildings", sem dois-pontos — escolha confirmada com o autor |
| Resumo/Abstract 100–200 palavras cada | 216/~215 | Cortados para 200/194 |
| 3–6 palavras-chave (revista) / 3–5 (template) | 5 em cada idioma, separadas por `;` | Mantidas 5 (compatível com ambos os limites); separador trocado para `.` conforme o template oficial |
| Referências NBR 6023:2018, alfabética, >3 autores → 1º + et al. | `biblatex` `style=abnt` | Mantido; renderização do "et al." depende do pacote `biblatex-abnt` (não customizado). 14 entradas com ≥4 autores identificadas para checagem visual no PDF compilado |
| Citações NBR 10520 (2023 no site oficial; o template baixado cita 2001) | `\textcite`/`\parencite` | Divergência entre fontes oficiais registrada; adotado 2023 (página institucional, mais recente) por padrão; **pendência do autor**: confirmar com a revista se o template está desatualizado |
| Tabelas/figuras com legenda e chamada no texto | 11 tabelas + 11 figuras, todas com `\caption`/chamada | Preservadas integralmente, nenhuma removida |
| Figuras ≥300 dpi, jpg/png, coloridas | 14 PNG conferidos, todos exatamente 300 dpi | Conforme |
| Avaliação duplo-cega: remover autoria do arquivo e propriedades | `\author{...}` no `main.tex` | Criado `main_anonimo.tex` (mesmo conteúdo científico, autor/afiliação omitidos) e script `anonimizar_docx.py` para limpar `docProps` do Word |
| Comitê de ética só se pesquisa envolver seres humanos (Resolução 510/2016) | Revisão bibliométrica, sem coleta com seres humanos | Não aplicável — nenhuma declaração necessária |
| Ciência Aberta | Repositório GitHub público | Declaração sustentável; nenhum "formulário" adicional encontrado nas instruções lidas |
| Declaração de uso de IA no Método, se houve uso | Nenhuma | Inserida no Método: uso do Claude (Claude Code, Anthropic, Sonnet 5) restrito a revisão ortográfica/textual e adequação formal, confirmado pelo autor |
| Agradecimento/financiamento só na versão pós-aceite | Nenhum no corpo atual | Preparado separadamente em `docs/AGRADECIMENTO_POS_ACEITE.md` (texto CAPES fornecido pelo autor, com pendência de confirmação de aplicabilidade) |

## 3. Núcleo científico preservado (verificação automatizada)

- 43 referências no `references.bib`; **auditoria automática**: 0 citações sem
  entrada, 0 entradas não citadas (script ad hoc, ver histórico de commits).
- 11 tabelas, 11 figuras/gráficos (9 "Gráfico" + 2 "Figura"/fluxograma) — os
  mesmos 11+11 do capítulo de tese, nenhum removido.
- `scripts/python/verificar_artigo.py` (adaptado nesta branch, ver Seção 4)
  confirma, a partir dos CSVs de dados (não da prosa): 12.118 → 9.542 → 3.678
  → 137 → 104 (núcleo original) → 121 (núcleo vigente, +17 da busca de
  sensibilidade IA/ML), seis dimensões, 15 critérios, crescimento de
  aprendizado de máquina de 9 para 26 registros, e todos os demais números
  centrais do funil.

## 4. Adaptação do script de verificação nesta branch

`scripts/python/verificar_artigo.py` foi escrito para auditar a versão de
capítulo de tese (Etapas 1–16 de uma rodada de revisão anterior) e continha
~40 asserções de frase literal amarradas àquela prosa específica. Como a
tarefa pedia reescrita e condensação do texto, essas asserções foram
substituídas por checagens de substância equivalentes (ex.: a matriz continua
identificada como "não validada"/candidata, as limitações continuam
declaradas, o ASReview continua sem atribuição indevida), sem remover nenhuma
das checagens de integridade numérica/CSV/scripts, que continuam intactas e
passando. Duas checagens adicionais já estavam desalinhadas dos dados atuais
antes desta branch (uma lacuna documental de string de busca que já havia
sido preenchida em atualização de dados anterior) e foram corrigidas para
refletir o estado real dos dados.

## 5. Compilação e validação (workflow `Validar fontes e gerar artigo`)

*[Preenchido após a execução da CI — ver mensagem de fechamento desta etapa]*

## 6. Versão Word e template oficial

O template oficial (`Template AC-OTH.docx`, fornecido pelo autor) confirmou:
página A4, margens 3/2/3/2 cm, fonte padrão Times New Roman, corpo de texto
12pt justificado, espaçamento simples, numeração de linha contínua já
configurada nas propriedades de seção, palavras-chave separadas por ponto.
Os títulos numerados no próprio arquivo de exemplo ("1 INTRODUÇÃO", "4
RESULTADOS E DISCUSSÕES") contradizem o texto das instruções na página do
site ("títulos não numerados", Título 1 em 14pt negrito maiúsculo) — os
títulos do exemplo aparecem em 12pt sem negrito. Diante da divergência entre
o arquivo-modelo e o texto das instruções, prevaleceu o texto das instruções
(mais explícito) para o estilo visual dos títulos na versão Word gerada, e a
numeração foi mantida (matching do arquivo-modelo, mais concreto que o texto
genérico). *Pendência do autor*: confirmar visualmente qual convenção a
revista realmente aplica, comparando com um artigo publicado recente.

## 7. Pendências que dependem exclusivamente do autor

1. Confirmar a norma de citação vigente (NBR 10520:2023 conforme o site, ou
   2001 conforme o template baixado) diretamente com a secretaria editorial.
2. Confirmar o estilo visual dos títulos (numerado vs. não numerado, negrito
   vs. não negrito) comparando com um fascículo publicado recente.
3. Confirmar se há taxa de publicação aplicável (isenção, R$ 350 ou R$ 700,
   conforme associação à ANTAC).
4. Confirmar a aplicabilidade do agradecimento CAPES (`docs/AGRADECIMENTO_POS_ACEITE.md`)
   e de eventuais outras fontes de financiamento.
5. Verificar, no PDF/Word compilados, a renderização do "et al." para as 14
   referências com 4+ autores.
