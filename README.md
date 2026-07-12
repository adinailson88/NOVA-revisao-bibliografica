# Manutenção predial sustentável em edificações públicas universitárias

## Arquivos para leitura

- **[Ler o artigo completo em PDF](main.pdf)**
- **[Baixar a versão editável em Word](artigo.docx?raw=1)**
- **[Consultar a lista auditável de referências](referencias/lista_referencias.csv)**
- **[Consultar os arquivos e evidências bibliográficas](referencias/)**

> **Última atualização do artigo:** 12/07/2026 às 14:49 (horário de Brasília/Bahia, UTC-03:00), no branch `agent/bibliometria-ampliada-pages`.
>
> O PDF e o Word são regenerados pelo workflow **[Gerar tabelas, gráficos, PDF e Word](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml)**. A página do workflow permite conferir cada execução, seu commit, horário, etapas e resultado. O commit automático `CI: atualiza tabelas, graficos, PDF e Word [skip ci]` confirma que os arquivos derivados refletem os fontes do branch.
>
> O PDF compilado é a versão editorial de referência. O Word é uma versão editável derivada do LaTeX e pode apresentar pequenas diferenças de paginação ou posicionamento de elementos flutuantes.

## Sobre

Revisão integrativa sistematizada sobre manutenção predial e gestão de edificações como estratégia de sustentabilidade do ambiente construído. O artigo analisa critérios de sustentabilidade, métodos de apoio à decisão, ODS, ESG e lacunas aplicáveis a edificações públicas universitárias.

## O que foi feito

Busca bibliométrica em Scopus, Web of Science e Crossref, no período de 2010 a 2026. O processo partiu de 12.118 registros brutos e resultou em um núcleo final de 104 registros após deduplicação, triagem e auditoria qualitativa estruturada.

O texto utiliza citação autor-data e referências formatadas em padrão ABNT.

## Reprodutibilidade e auditoria

Scripts vigentes que geram ou validam os produtos apresentados:

- [Gerador das tabelas e dos gráficos temáticos em R](scripts/r/10_gerar_produtos_artigo.R)
- [Gerador da bibliometria ampliada em Python](scripts/python/11_gerar_bibliometria_ampliada.py)
- [Gerador do inventário auditável das referências](scripts/python/12_gerar_lista_referencias.py)
- [Verificador de números, texto, citações e rastreabilidade](scripts/python/verificar_artigo.py)
- [Workflow completo de geração e validação](.github/workflows/latex.yml)
- [Demais scripts reprodutíveis em Python](scripts/python/)
- [Scripts históricos da análise em R](05_ANALISE_R/scripts/)

A pasta [`referencias/`](referencias/) reúne o arquivo BibTeX efetivamente usado, a planilha CSV de referências e um mapa dos arquivos de evidência disponíveis. PDFs protegidos por direito autoral não são redistribuídos pelo repositório.

## Estrutura deste repositório

- `01_PROTOCOLO/`: protocolo, matriz conceitual, strings nativas e logs das buscas.
- `03_PROCESSADOS/`: corpus normalizado, corpus consolidado, duplicatas e relatório de deduplicação.
- `04_TRIAGEM/`: matrizes de pré-triagem e triagem auditada, amostra e resolução de dúvidas.
- `05_ANALISE_R/`: produtos históricos da análise, organizados em `scripts/`, `tabelas/` e `figuras/`.
- `07_SINTESE_TEMATICA/`: matrizes, dicionários, relatórios e recortes da síntese até o núcleo final.
- `latex-artigo/`: fonte LaTeX, dados derivados e gráficos efetivamente utilizados no artigo.
- `referencias/`: inventário auditável das referências citadas e mapa das evidências.
- `scripts/`: rotinas reprodutíveis de geração, análise e verificação.
- `docs/`: plano, relatórios por etapa, inventários e mapa de rastreabilidade.
