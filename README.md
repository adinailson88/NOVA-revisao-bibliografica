# Manutenção predial sustentável em edificações públicas universitárias

## Arquivos para leitura

Os links abaixo apontam para arquivos publicados no GitHub Pages e funcionam sem depender do visualizador de arquivos binários do aplicativo GitHub:

- **[Abrir ou baixar o artigo em PDF](https://adinailson88.github.io/NOVA-revisao-bibliografica/artigo.pdf)**
- **[Baixar a versão Word validada](https://adinailson88.github.io/NOVA-revisao-bibliografica/artigo.docx)**
- **[Abrir a página do artigo com os botões de download](https://adinailson88.github.io/NOVA-revisao-bibliografica/)**
- **[Consultar a lista auditável de referências](referencias/lista_referencias.csv)**
- **[Consultar os arquivos e evidências bibliográficas](referencias/)**

> **Estado atual:** núcleo temático vigente de 121 registros, com o núcleo histórico de 104 preservado.
>
> O PDF e o Word são regenerados pelo workflow **[Validar fontes e gerar artigo](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml)** em cada atualização da `main`. O Word é aberto e resalvo pelo LibreOffice, validado como pacote OOXML e convertido novamente em PDF como teste de abertura antes da publicação.

## Sobre

Revisão integrativa sistematizada sobre manutenção predial e gestão de edificações como estratégia de sustentabilidade do ambiente construído. O artigo analisa critérios de sustentabilidade, métodos de apoio à decisão, ODS, ESG e lacunas aplicáveis a edificações públicas universitárias.

## O que foi feito

Busca bibliométrica em Scopus, Web of Science e Crossref, no período de 2010 a 2026. O processo principal partiu de 12.118 ocorrências brutas e resultou em um núcleo original de 104 registros após deduplicação, triagem e auditoria qualitativa estruturada. Uma busca complementar de sensibilidade para IA/aprendizado de máquina recuperou 6.728 ocorrências e incorporou 17 registros, formando o núcleo temático vigente de 121. A camada bibliométrica de 372 permanece derivada apenas da busca principal.

O texto utiliza citação autor-data e referências formatadas em padrão ABNT.

## Versão em Word

`artigo.docx` é gerado a partir dos fontes LaTeX, e não por reconversão do PDF. O Pandoc preserva texto, títulos, citações e referências; o script [`scripts/python/13_preparar_word.py`](scripts/python/13_preparar_word.py) reconstrói as tabelas nativas, converte figuras incompatíveis, insere os fluxogramas e corrige referências cruzadas. Em seguida, o documento é aberto e resalvo pelo LibreOffice e submetido a três controles:

1. integridade do pacote ZIP/OOXML;
2. abertura pela biblioteca `python-docx`;
3. conversão integral para PDF pelo LibreOffice.

O `main.pdf` permanece a versão de referência para citação e submissão.

Para regenerar localmente, com Pandoc, LibreOffice, LaTeX e Python instalados:

```bash
python scripts/python/13_preparar_word.py
```

## Reprodutibilidade e auditoria

Scripts vigentes que geram ou validam os produtos apresentados:

- [Gerador Python das tabelas e dos gráficos do núcleo vigente de 121](scripts/python/gerar_produtos_artigo_nucleo_ampliado.py)
- [Gerador da bibliometria ampliada em Python](scripts/python/11_gerar_bibliometria_ampliada.py)
- [Gerador do inventário auditável das referências](scripts/python/12_gerar_lista_referencias.py)
- [Gerador e validador da versão Word](scripts/python/13_preparar_word.py)
- [Gerador das planilhas XLSX e do núcleo final para auditoria](scripts/python/14_gerar_planilhas_auditoria_referencias.py)
- [Verificador de números, texto, citações e rastreabilidade](scripts/python/verificar_artigo.py)
- [Workflow completo de geração e validação](.github/workflows/latex.yml)
- [Demais scripts reprodutíveis em Python](scripts/python/)
- [Scripts históricos da análise em R](05_ANALISE_R/scripts/)

A pasta [`referencias/`](referencias/) reúne o arquivo BibTeX efetivamente usado, a planilha das referências citadas, o núcleo vigente de 121 registros e o núcleo original de 104 preservado como produto histórico, com metadados de auditoria. PDFs protegidos por direito autoral não são redistribuídos pelo repositório.

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