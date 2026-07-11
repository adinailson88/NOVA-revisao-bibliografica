# Inventário do artigo de revisão — Etapa 0

## 1. Escopo e estado preservado

- Repositório: https://github.com/adinailson88/NOVA-revisao-bibliografica
- Branch de trabalho: `revisao-metodologica-controlada`
- Branch principal: `main`
- Commit de origem preservado: `e10ef825e6a560f19ffc12306d55b142b3c360e3`
- Cópia de preservação: branch `preservacao-original-revisao-metodologica-20260710`
- Data do inventário: 2026-07-10
- Regra: nenhum conteúdo científico ou textual do artigo foi corrigido nesta etapa.

A branch de preservação aponta diretamente para o commit de origem e mantém a versão integral anterior ao início das alterações controladas.

## 2. Arquivo-fonte principal e produto compilado

| Função | Arquivo | Git blob SHA |
|---|---|---|
| Fonte principal | `latex-artigo/main.tex` | `65f6933fb0234c34af17b9810fb7959b649c785a` |
| Bibliografia | `latex-artigo/references.bib` | `c304ea4e15017bbf0bed9cee48191dd7f6f46ded` |
| PDF publicado | `main.pdf` | `0f94912876f705e7fe3c3dc8813eb89dfa865f58` |
| Workflow de geração | `.github/workflows/latex.yml` | `49120c446ab08d32279875ba18d1678a80b13c24` |

Os valores acima são identificadores SHA-1 de objetos blob do Git. Eles permitem verificar a identidade exata do conteúdo armazenado no repositório, mas não devem ser confundidos com SHA-256 calculado diretamente sobre os bytes.

## 3. Estrutura do texto

| Arquivo | Conteúdo | Git blob SHA |
|---|---|---|
| `sections/00_resumo.tex` | Resumo e abstract | `bbd23f9471acab83f7872c7635c453fc6a38ad5f` |
| `sections/01_introducao.tex` | Introdução | `f53dc8a0f892e515306d1becb2065650335a988a` |
| `sections/02_revisao.tex` | Revisão teórica | `7da0e7e5f400241ff84f88f16f4c7da38710737b` |
| `sections/03_metodologia.tex` | Metodologia | `bdeb4219f797bdb9a771f90de460f777bf108bb8` |
| `sections/04_panorama.tex` | Panorama do corpus | `e4d5f6704aaf4901ec1a19958bfe6e2ffef88c4a` |
| `sections/05_criterios.tex` | Critérios | `d65730d142375ceaf4d33322837a423cadc18b10` |
| `sections/06_metodos.tex` | Métodos de apoio à decisão | `efd4dd7c68a7d3d127e364eda162970054052844` |
| `sections/07_aplicabilidade.tex` | Aplicabilidade | `a12ff26d2567a18031f0acee9175a8b81e712b17` |
| `sections/08_matriz.tex` | Matriz analítica | `aac6087a7c51588c8efb2eef0b9024b253d1589c` |
| `sections/09_limitacoes.tex` | Limitações | `346776331058685953bc303ae75d2fc443c81667` |
| `sections/10_consideracoes.tex` | Considerações finais | `333299b35a46ba19beff4cb6993a4b412fd0cb15` |

Todos os caminhos da tabela estão sob `latex-artigo/`.

## 4. Dados-fonte e tabelas derivadas

### 4.1 Bases centrais verificadas

| Arquivo | Função | Git blob SHA |
|---|---|---|
| `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv` | Núcleo final auditado | `a120c6cfac5127b708d1bd8ee339881ba49ba6fd` |
| `latex-artigo/fontes/dicionario_criterio_dimensao_etapa17.csv` | Dicionário de critérios e dimensões | `cf650a79774083cf8ddd98e393ccc21224eb1752` |

### 4.2 Outros arquivos tabulares identificados

- `tabela_criterios_inclusao_exclusao.csv`
- `tabela_estrategia_busca.csv`
- `tabela_resumo_estrategia_busca.csv`
- `tabela26_criterios_nucleo_final_104.csv`
- `tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv`
- `tabela28_metodos_decisao_nucleo_final_104.csv`
- `tabela29_contexto_edificacao_nucleo_final_104.csv`
- `tabela30_lacunas_nucleo_final_104.csv`
- `tabela31_coocorrencia_criterio_metodo_nucleo_final_104.csv`
- `tabela32_coocorrencia_dimensao_metodo_nucleo_final_104.csv`
- `tabela33_distribuicao_temporal_nucleo_final_104.csv`
- `tabela34_bases_origem_nucleo_final_104.csv`
- `tabela34_tipos_documentais_harmonizados_nucleo_final_104.csv`
- `tabela35_mencoes_ods_esg_nucleo_final_104.csv`

Os arquivos desta subseção estão sob `latex-artigo/fontes/`. Os dados brutos licenciados das bases Scopus e Web of Science não aparecem redistribuídos no repositório. A suficiência dos dados para reproduzir cada transição do funil será auditada nas etapas específicas.

## 5. Figuras

Foram identificadas em `latex-artigo/figuras/`:

- `figura09_distribuicao_temporal_nucleo_final_104.png`
- `figura10_distribuicao_base_tipo_nucleo_final_104.png`
- `figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png`
- `figura12_dimensoes_sustentabilidade_nucleo_final_104.png`
- `figura13_heatmap_criterios_metodos_nucleo_final_104.png`
- `figura14_matriz_analitica_dimensao_metodo_nucleo_final_104.png`

## 6. Scripts

### 6.1 Python

Foram identificados em `scripts/python/`:

- `amostrar_auditoria.py`
- `auditoria_triagem.py`
- `coleta_crossref.py`
- `coleta_scopus.py`
- `consolidar_deduplicar.py`
- `gerar_gabarito_matriz_extracao_final.py`
- `pre_triagem.py`
- `preencher_matriz_extracao_final.py`
- `priorizar_leitura_full_text.py`
- `sintese_tematica_preliminar.py`
- `verificar_numeros_rascunho.py`
- `verificar_artigo.py` — Git blob SHA `25e077cdc00efd551f8ef1a1915054890a3a7ca4`

### 6.2 R

Foram identificados em `scripts/r/`:

- `00_config.R`
- `01_definir_nucleo_analitico.R`
- `02_tabelas_descritivas.R`
- `03_figuras.R`
- `04_exportar_duvida_para_revisao.R`
- `05_aplicar_resolucao_duvidas.R`
- `06_figuras_nucleo_revisado.R`
- `08_reavaliar_resumos_criterioso.R`
- `09_alinhar_registros_perguntas_pesquisa.R`
- `10_gerar_produtos_artigo.R` — Git blob SHA `1838f4e5eac656cdba7d9264f52777b14b2e64ee`

## 7. Documentação e automação

- `README.md`: descreve escopo, números gerais e estrutura.
- `.github/workflows/latex.yml`: gera tabelas e gráficos, executa `verificar_artigo.py`, instala TeX Live/Biber, compila `latex-artigo/main.tex`, verifica caixas horizontais excedentes, copia o PDF para a raiz e publica artefato.
- `docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`: plano oficial.
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`: acompanhamento das etapas.
- Não foi localizado `AGENTS.md` na raiz.

## 8. Verificação de compilação e estado inicial

O histórico mostra a seguinte cadeia imediatamente anterior ao início do trabalho:

1. `9c003696862a3347884183d8f33a18b5e2f1cd4c`: revisão editorial, metodológica e visual, incluindo fonte LaTeX, scripts, tabelas, figuras e PDF;
2. `e10ef825e6a560f19ffc12306d55b142b3c360e3`: commit do GitHub Actions que atualizou tabelas, gráficos e `main.pdf`.

O PDF existente foi aberto e possui 14 páginas, título e resumo legíveis. A existência do commit automatizado e do PDF resultante comprova que o workflow concluiu a geração do produto publicado nesse estado. A API de status consultada não retornou checks associados, e não foi possível executar uma recompilação local independente porque o ambiente não possui checkout autenticado do repositório privado nem cliente `gh`.

Portanto:

- PDF compilado no estado de origem: verificado;
- workflow de compilação: identificado;
- recompilação independente no ambiente local: **Informação insuficiente para verificar.**
- erros de compilação existentes: não identificados no produto publicado;
- logs completos da execução: **Informação insuficiente para verificar.**

## 9. Lacunas registradas sem correção

- Os dados brutos de Scopus e Web of Science não estão redistribuídos no repositório.
- Ainda não foi verificada, nesta etapa, a reprodutibilidade integral das transições 12.118 → 9.542 → 3.678 → 137 → 104.
- Ainda não foi auditada a correspondência entre cada tabela/figura e sua fonte.
- Ainda não foi auditada a suficiência documental das datas e strings de busca.
- Ainda não foi auditado se houve leitura de texto completo, dupla revisão, protocolo ou pré-registro.
- Nenhuma dessas lacunas foi preenchida por inferência.

## 10. Resultado da Etapa 0

A versão original foi preservada por referência imutável de commit e por branch específica; os arquivos principais, derivados, scripts, figuras, documentação e automação foram inventariados; os identificadores dos principais objetos foram registrados; e o estado do PDF compilado foi verificado. O artigo não foi modificado.
