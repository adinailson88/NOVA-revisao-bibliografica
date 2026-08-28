# Prompt para auditoria externa (ChatGPT)

Copie e cole o texto abaixo no ChatGPT.

---

Preciso que você faça uma auditoria crítica e independente de uma adaptação editorial de artigo científico, feita por outro assistente de IA (Claude). Não conheço detalhes do processo além do que está documentado no repositório abaixo — quero sua leitura própria, não uma confirmação do que já foi dito.

Repositório: https://github.com/adinailson88/NOVA-revisao-bibliografica
Branch da submissão: `submissao-ambiente-construido` (a branch `main` é o capítulo de tese original, intocado; não avalie a `main`, avalie a branch de submissão)

Contexto: o artigo é uma revisão bibliométrica sobre manutenção sustentável em edificações públicas universitárias, com uma especificação operacional candidata (matriz de critérios/indicadores) para futura parametrização multicritério. A tarefa foi adaptar o capítulo de tese completo (~9.600 palavras, 13 seções) para o formato exigido pela revista Ambiente Construído (ANTAC/UFRGS): máximo de 7.000 palavras entre Introdução e Conclusões, estrutura em 4 blocos (Introdução, Método de pesquisa, Resultados e discussão, Considerações finais), preservando integralmente os números, resultados, tabelas, figuras e referências — sem nova pesquisa, sem alterar o corpus, sem inventar dados.

Arquivos-chave para revisar, nesta ordem:

1. `docs/RELATORIO_ADEQUACAO_AMBIENTE_CONSTRUIDO.md` — relatório de conformidade e do que foi feito, segundo o Claude.
2. `latex-artigo/sections/*.tex` (01 a 04) — o texto reescrito.
3. `latex-artigo/references.bib` — as referências.
4. `main.pdf` e `artigo.docx` na raiz do repositório — os produtos finais compilados.
5. `scripts/python/verificar_artigo.py` e `verificar_artigo_integrado.py` — os scripts de verificação automatizada, que foram adaptados durante a tarefa (veja o histórico de commits para entender por quê).
6. Histórico de commits da branch (`git log main..submissao-ambiente-construido`) para ver a sequência real do trabalho, não só o relatório final.

Por favor, verifique especificamente:

- Os números centrais do funil bibliométrico (12.118 → 9.542 → 3.678 → 137 → 104 → 121 registros, seis dimensões, 15 critérios, crescimento de aprendizado de máquina de 9 para 26) aparecem de forma consistente entre o resumo, o corpo do texto e as tabelas, sem contradição.
- Toda citação no texto tem entrada correspondente no `references.bib`, e toda entrada do `.bib` está de fato citada no texto (não confie apenas na afirmação do relatório — confira você mesmo, por amostragem ou integralmente).
- A matriz de indicadores/critérios é tratada como proposta candidata, não como resultado validado ou método já testado — isso é uma exigência explícita da tarefa original.
- O texto não introduz elementos que não deveriam estar lá: GLPI como requisito obrigatório, NBR 15575 sem necessidade demonstrada, substituição dos vetos por AVCB, ou qualquer normativa/dado inventado.
- A adaptação do script de verificação (`verificar_artigo.py`/`verificar_artigo_integrado.py`) não está mascarando uma perda real de conteúdo por trás de uma justificativa de "reescrita editorial" — ou seja, se as checagens antigas foram enfraquecidas de forma que esconderia um problema real.
- Contagem de palavras: confirme, por conta própria, que o texto de Introdução a Considerações finais está de fato dentro (ou muito próximo) do limite de 7.000 palavras.
- Qualidade da redação em português: presença de dois-pontos em excesso, repetições, tom promocional, ou qualquer traço que pareça texto gerado por IA sem revisão.

Me devolva um relatório objetivo: o que está correto, o que está incerto ou merece checagem manual minha, e qualquer discrepância real entre o que o relatório do Claude afirma e o que você encontrou nos arquivos.
