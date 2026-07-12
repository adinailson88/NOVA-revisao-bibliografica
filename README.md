# Manutenção predial sustentável em edificações públicas universitárias

**[Ler o artigo completo em PDF](main.pdf)**

> **Última atualização do artigo:** 12/07/2026, no branch `agent/bibliometria-ampliada-pages`.
> O PDF é recompilado automaticamente pelo workflow [Gerar tabelas, gráficos e PDF](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml) a cada push que altera o artigo; o commit do bot ("CI: atualiza tabelas, graficos e PDF") confirma que o `main.pdf` reflete a versão mais recente dos fontes.
>
> ⚠️ Ao atualizar o artigo, atualize também a data e o branch desta nota.

## Sobre

Revisão integrativa sistematizada sobre manutenção predial e gestão de edificações como estratégia de sustentabilidade do ambiente construído. O artigo analisa critérios de sustentabilidade, métodos de apoio à decisão, ODS, ESG e lacunas aplicáveis a edificações públicas universitárias.

## O que foi feito

Busca bibliométrica em Scopus, Web of Science e Crossref, no período de 2010 a 2026. O processo partiu de 12.118 registros brutos e resultou em um núcleo final de 104 registros após deduplicação, triagem e auditoria qualitativa estruturada.

O texto utiliza citação autor-data e referências formatadas em padrão ABNT.

## Estrutura deste repositório

- `01_PROTOCOLO/`: protocolo, matriz conceitual, strings nativas e logs das buscas.
- `03_PROCESSADOS/`: corpus normalizado, corpus consolidado, duplicatas e relatório de deduplicação.
- `04_TRIAGEM/`: matrizes de pré-triagem e triagem auditada, amostra e resolução de dúvidas.
- `05_ANALISE_R/`: produtos históricos da análise, organizados em `scripts/`, `tabelas/` e `figuras/`.
- `07_SINTESE_TEMATICA/`: matrizes, dicionários, relatórios e recortes da síntese até o núcleo final.
- `latex-artigo/`: fonte LaTeX, dados derivados e gráficos efetivamente utilizados no artigo.
- `scripts/python/`: scripts reprodutíveis de coleta, consolidação, triagem e verificação.
- `scripts/r/10_gerar_produtos_artigo.R`: fonte vigente das tabelas derivadas e dos gráficos utilizados no texto.
- `docs/`: plano, relatórios por etapa, inventários e mapa de rastreabilidade.

Os dados derivados e os scripts serão vinculados ao depósito público indicado na versão submetida do artigo.
