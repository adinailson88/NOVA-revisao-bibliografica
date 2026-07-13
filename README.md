# Manutenção predial sustentável em edificações públicas universitárias

## Arquivos para leitura

- **[Ler o artigo completo em PDF](main.pdf)**
- **[Baixar a versão Word para leitura e comentários](artigo.docx?raw=1)**
- **[Consultar a lista auditável de referências](referencias/lista_referencias.csv)**
- **[Consultar os arquivos e evidências bibliográficas](referencias/)**

> **Estado dos fontes:** consolidação em andamento na branch `agent/incorporacao-busca-sensibilidade-ia`, com núcleo temático vigente de 121 registros.
>
> Durante a consolidação textual, pushes e pull requests executam apenas o pipeline Python e o verificador. PDF e Word são regenerados pelo workflow **[Validar fontes e gerar artigo](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml)** somente por execução manual ou por push na `main`.
>
> Por isso, os arquivos `main.pdf` e `artigo.docx` podem permanecer temporariamente anteriores aos fontes `.tex`. Essa defasagem é deliberada e será encerrada pela compilação acumulada, com Biber, controle de referências e inspeção de margens.

## Sobre

Revisão integrativa sistematizada sobre manutenção predial e gestão de edificações como estratégia de sustentabilidade do ambiente construído. O artigo analisa critérios de sustentabilidade, métodos de apoio à decisão, ODS, ESG e lacunas aplicáveis a edificações públicas universitárias.

## O que foi feito

Busca bibliométrica em Scopus, Web of Science e Crossref, no período de 2010 a 2026. O processo principal partiu de 12.118 ocorrências brutas e resultou em um núcleo original de 104 registros após deduplicação, triagem e auditoria qualitativa estruturada. Uma busca complementar de sensibilidade para IA/aprendizado de máquina recuperou 6.728 ocorrências e incorporou 17 registros, formando o núcleo temático vigente de 121. A camada bibliométrica de 372 permanece derivada apenas da busca principal.

O texto utiliza citação autor-data e referências formatadas em padrão ABNT.

## Versão em Word

`artigo.docx` é gerado a partir dos fontes LaTeX (não do PDF, que não é reconvertido para
texto), via [Pandoc](https://pandoc.org/) com citeproc, a partir do `references.bib`. O
texto corrido, os títulos, as citações e a lista de referências ficam com texto real e
selecionável; as 11 tabelas do artigo são reconstruídas como tabelas nativas do Word por
[`scripts/python/13_preparar_word.py`](scripts/python/13_preparar_word.py), porque o Pandoc
não interpreta os ambientes `tabularx`/`booktabs` customizados usados no artigo. O
fluxograma em TikZ e a formatação ABNT fina não são preservados — o `main.pdf` continua
sendo a versão de referência para citação e submissão. Para regenerar após uma atualização
do artigo (requer [Pandoc](https://pandoc.org/installing.html) instalado):

```
python scripts/python/13_preparar_word.py
```

## Reprodutibilidade e auditoria

Scripts vigentes que geram ou validam os produtos apresentados:

- [Gerador Python das tabelas e dos gráficos do núcleo vigente de 121](scripts/python/gerar_produtos_artigo_nucleo_ampliado.py)
- [Gerador da bibliometria ampliada em Python](scripts/python/11_gerar_bibliometria_ampliada.py)
- [Gerador do inventário auditável das referências](scripts/python/12_gerar_lista_referencias.py)
- [Gerador da versão Word a partir dos fontes LaTeX](scripts/python/13_preparar_word.py)
- [Gerador das planilhas XLSX e do núcleo final para auditoria](scripts/python/14_gerar_planilhas_auditoria_referencias.py)
- [Verificador de números, texto, citações e rastreabilidade](scripts/python/verificar_artigo.py)
- [Workflow completo de geração e validação](.github/workflows/latex.yml)
- [Demais scripts reprodutíveis em Python](scripts/python/)
- [Scripts históricos da análise em R](05_ANALISE_R/scripts/)

A pasta [`referencias/`](referencias/) reúne o arquivo BibTeX efetivamente usado, a
planilha (CSV e XLSX) das referências citadas, o núcleo vigente de 121 registros e o núcleo
original de 104 preservado como produto histórico, com metadados de auditoria (dimensões,
critérios, métodos, RQs confirmadas e nível de confiança). Ver o `README.md` da
pasta para a relação entre as duas listas. PDFs protegidos por direito autoral não são
redistribuídos pelo repositório.

## Estrutura deste repositório

- `01_PROTOCOLO/`: protocolo, matriz conceitual, strings nativas e logs das buscas.
- `03_PROCESSADOS/`: corpus normalizado, corpus consolidado, duplicatas e relatório de deduplicação.
- `04_TRIAGEM/`: matrizes de pré-triagem e triagem auditada, amostra e resolução de dúvidas.
- `05_ANALISE_R/`: produtos históricos da análise, organizados em `scripts/`, `tabelas/` e `figuras/`.
- `07_SINTESE_TEMATICA/`: matrizes, dicionários, relatórios e recortes da síntese até o núcleo final.
- `latex-artigo/`: fonte LaTeX, dados derivados e gráficos efetivamente utilizados no artigo.
- `referencias/`: inventário auditável das referências citadas, planilhas do núcleo final e mapa das evidências.
- `scripts/`: rotinas reprodutíveis de geração, análise e verificação.
- `docs/`: plano, relatórios por etapa, inventários e mapa de rastreabilidade.
