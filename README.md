# Manutenção predial sustentável em edificações públicas universitárias

**[Ler o artigo completo em PDF](main.pdf)** · **[Baixar versão em Word (.docx)](main.docx)**

> **Última atualização do artigo:** 12/07/2026, 16h32 (horário de Brasília), no branch `agent/bibliometria-ampliada-pages`.
> O PDF é recompilado automaticamente pelo workflow [Gerar tabelas, gráficos e PDF](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml) a cada push que altera o artigo; o commit do bot ("CI: atualiza tabelas, graficos e PDF") confirma que o `main.pdf` reflete a versão mais recente dos fontes. Veja o [histórico de execuções](https://github.com/adinailson88/NOVA-revisao-bibliografica/actions/workflows/latex.yml) para conferir a última compilação bem-sucedida.
>
> ⚠️ Ao atualizar o artigo, atualize também a data/hora e o branch desta nota, e regenere o `main.docx` (ver seção [Versão em Word](#versão-em-word)).

## Referências e material auditável para o orientador

- **[`08_REFERENCIAS/`](08_REFERENCIAS/)** — pasta com o `.bib` usado na compilação, uma
  planilha (CSV e XLSX) das 35 referências citadas no texto, e a planilha completa (CSV e
  XLSX) dos 104 registros do núcleo final que fundamentam a síntese temática, com
  metadados de auditoria. Ver o `README.md` da pasta para a relação entre as duas listas.
- **Scripts que geram os produtos do artigo:**
  - [`scripts/python/verificar_artigo.py`](scripts/python/verificar_artigo.py) — checagem automática de consistência (contagens, citações, números do corpus) rodada a cada build.
  - [`scripts/python/11_gerar_bibliometria_ampliada.py`](scripts/python/11_gerar_bibliometria_ampliada.py) — gera os gráficos e tabelas da camada bibliométrica ampliada (fontes, mapa temático, rede de coocorrência, evolução temática).
  - [`scripts/python/12_gerar_versao_word.py`](scripts/python/12_gerar_versao_word.py) — gera o `main.docx` a partir dos fontes LaTeX (ver [Versão em Word](#versão-em-word)).
  - [`scripts/python/13_gerar_planilha_referencias.py`](scripts/python/13_gerar_planilha_referencias.py) — gera as planilhas de `08_REFERENCIAS/` a partir do `.bib` e do núcleo final.
  - [`scripts/r/10_gerar_produtos_artigo.R`](scripts/r/10_gerar_produtos_artigo.R) — gera as demais tabelas e gráficos derivados do núcleo final de 104 registros.
  - [`scripts/python/`](scripts/python/) — demais scripts de coleta, deduplicação, triagem e consolidação do corpus.

## Sobre

Revisão integrativa sistematizada sobre manutenção predial e gestão de edificações como estratégia de sustentabilidade do ambiente construído. O artigo analisa critérios de sustentabilidade, métodos de apoio à decisão, ODS, ESG e lacunas aplicáveis a edificações públicas universitárias.

## O que foi feito

Busca bibliométrica em Scopus, Web of Science e Crossref, no período de 2010 a 2026. O processo partiu de 12.118 registros brutos e resultou em um núcleo final de 104 registros após deduplicação, triagem e auditoria qualitativa estruturada.

O texto utiliza citação autor-data e referências formatadas em padrão ABNT.

## Versão em Word

`main.docx` é gerado a partir dos fontes LaTeX (não do PDF, que o Pandoc não converte de
volta), via [Pandoc](https://pandoc.org/) com citeproc, para leitura e comentários fora do
LaTeX (ex.: revisão pelo orientador no Word). O texto corrido, os títulos, as citações e a
lista de referências vêm do próprio `references.bib`; as 11 tabelas do artigo são
reconstruídas como tabelas nativas do Word por
[`scripts/python/12_gerar_versao_word.py`](scripts/python/12_gerar_versao_word.py), porque
o Pandoc não interpreta os ambientes `tabularx`/`booktabs` customizados usados no artigo. O
fluxograma em TikZ e a formatação ABNT fina não são preservados — o `main.pdf` continua
sendo a versão de referência para citação e submissão. Para regenerar após uma atualização
do artigo (requer [Pandoc](https://pandoc.org/installing.html) instalado):

```
python scripts/python/12_gerar_versao_word.py
```

## Estrutura deste repositório

- `01_PROTOCOLO/`: protocolo, matriz conceitual, strings nativas e logs das buscas.
- `03_PROCESSADOS/`: corpus normalizado, corpus consolidado, duplicatas e relatório de deduplicação.
- `04_TRIAGEM/`: matrizes de pré-triagem e triagem auditada, amostra e resolução de dúvidas.
- `05_ANALISE_R/`: produtos históricos da análise, organizados em `scripts/`, `tabelas/` e `figuras/`.
- `07_SINTESE_TEMATICA/`: matrizes, dicionários, relatórios e recortes da síntese até o núcleo final.
- `08_REFERENCIAS/`: `.bib` e planilhas (CSV/XLSX) das referências citadas e do núcleo final de 104 registros — material auditável independente do LaTeX.
- `latex-artigo/`: fonte LaTeX, dados derivados e gráficos efetivamente utilizados no artigo.
- `scripts/python/`: scripts reprodutíveis de coleta, consolidação, triagem e verificação.
- `scripts/r/10_gerar_produtos_artigo.R`: fonte vigente das tabelas derivadas e dos gráficos utilizados no texto.
- `docs/`: plano, relatórios por etapa, inventários e mapa de rastreabilidade.

Os dados derivados e os scripts serão vinculados ao depósito público indicado na versão submetida do artigo.
