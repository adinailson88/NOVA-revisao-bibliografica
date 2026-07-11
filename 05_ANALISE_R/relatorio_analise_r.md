# RELATÓRIO DE ANÁLISE EM R — ETAPA_09 (TABELAS E FIGURAS)

Data de execução: 2026-07-10.

Fonte de dados: `04_TRIAGEM/matriz_triagem_auditada.csv` (9.542 registros, gerada na ETAPA_08,
rodada de 2026-07-09). Colunas usadas: `classe_auditada` (classificação final por registro),
`auditado` (sim/não — se o registro foi lido individualmente na auditoria por amostra),
`bloco_a_presente` e `bloco_b_presente` (indicadores por registro), `ano`, `bases_origem`.

## 1. Definição do núcleo analítico

Esta etapa precisou decidir, antes de gerar qualquer tabela ou figura, um ponto que o pipeline
operacional não tinha resolvido em etapa própria (ver `00_CONTROLE/ESTADO_ATUAL.md`, nota final da
versão de 2026-07-09): qual corte de `classe_auditada` compõe o núcleo analítico do artigo.

**Critério adotado:**

| Origem (classe_auditada) | Regra | Decisão |
|---|---|---|
| `relevante` | — | **entra** no núcleo |
| `duvida`, subgrupo "apenas Bloco A" (`bloco_a_presente=sim` e `bloco_b_presente=nao`) | — | **entra** no núcleo |
| `duvida`, subgrupo "apenas Bloco B" (`bloco_a_presente=nao` e `bloco_b_presente=sim`) | — | **fora** do núcleo |
| `duvida`, nenhum bloco presente (4 registros — anomalia residual do classificador, ver seção 4) | — | **fora** do núcleo |
| `complementar` | — | **fora** do núcleo (categoria auxiliar, não é objeto+sustentabilidade nucleares) |
| `irrelevante` | — | **fora** do núcleo |
| `sem_resumo` | — | **fora** do núcleo (sem evidência textual suficiente) |

**Motivo:** `04_TRIAGEM/relatorio_ajustes_triagem.md` (seções 3.3 e 5) registra, com evidência de
duas rodadas de auditoria independentes, que dentro de `duvida` o subgrupo "apenas Bloco B
presente" (sustentabilidade genérica sem objeto predial real) tem taxa de acerto muito baixa quando
verificado por leitura individual — 1 acerto em 17 casos lidos na rodada de 2026-07-09, 0 em 13 na
rodada anterior — comportando-se, na prática, como quase-irrelevante. O subgrupo "apenas Bloco A
presente" teve taxa de acerto oposta e alta — 1 de 1 na rodada de 2026-07-09, 7 de 7 na rodada
anterior. Excluir "apenas Bloco B" e incluir "apenas Bloco A" do núcleo aplica essa evidência ao
corte, em vez de tratar toda a classe `duvida` como um bloco homogêneo.

**Ressalva explícita, não resolvida por esta etapa:** a inclusão do subgrupo "apenas Bloco A" no
núcleo é uma extrapolação de amostra pequena para uma população de 314 registros. Ver tabela 8 —
apenas 1 desses 314 registros (0,3%) foi de fato lido individualmente na auditoria por amostra; os
outros 313 (99,7%) mantêm a classificação automática sem verificação humana. A boa taxa de acerto
observada (8 acertos em 8 leituras, somando as duas rodadas) é evidência favorável, mas de tamanho
amostral muito pequeno para o volume extrapolado. Fica registrado como limitação a considerar em
etapa futura de leitura completa do texto (full-text) do núcleo analítico.

## 2. Resultado do corte

| Grupo | N | % do corpus (9.542) |
|---|---:|---:|
| **Núcleo analítico** | **3.786** | **39,7%** |
| Fora do núcleo | 5.756 | 60,3% |

Composição do núcleo: 3.472 de `relevante` + 314 de `duvida`/apenas Bloco A.

Ver `05_ANALISE_R/tabelas/tabela01_corte_nucleo_por_classe.csv`,
`tabela02_subgrupos_duvida.csv` e `tabela03_resumo_nucleo_analitico.csv` para o detalhe numérico
completo, e `05_ANALISE_R/figuras/figura02_composicao_nucleo_analitico.png` para a visualização.

## 3. Tabelas geradas

Todas em `05_ANALISE_R/tabelas/`, cada uma com dados extraídos diretamente de
`matriz_triagem_auditada.csv` (nenhum número inserido manualmente):

| Arquivo | Conteúdo |
|---|---|
| `matriz_nucleo_analitico.csv` | Matriz completa (9.542 linhas) com as colunas adicionais `subgrupo_duvida` e `nucleo_analitico` (base para as demais tabelas/figuras) |
| `tabela01_corte_nucleo_por_classe.csv` | N por `classe_auditada` × dentro/fora do núcleo |
| `tabela02_subgrupos_duvida.csv` | Detalhe do subgrupo dentro de `duvida` (apenas A / apenas B / nenhum bloco) × dentro/fora do núcleo |
| `tabela03_resumo_nucleo_analitico.csv` | N e % total, núcleo vs. fora |
| `tabela04_distribuicao_classe_auditada.csv` | Distribuição do corpus completo por `classe_auditada` |
| `tabela05_distribuicao_por_ano.csv` | N por ano de publicação (2010–2026), corpus completo vs. núcleo |
| `tabela06_nucleo_por_base_origem.csv` | N do núcleo por base de origem (Scopus/WoS/Crossref e combinações) |
| `tabela07_proporcao_auditada_por_classe.csv` | % de registros lidos individualmente (`auditado=sim`) por `classe_auditada` |
| `tabela08_duvida_bloco_a_evidencia_auditoria.csv` | Quantos dos 314 registros "duvida/apenas Bloco A" do núcleo foram de fato auditados individualmente (evidência direta vs. extrapolada — ver seção 1) |

**Achados descritivos relevantes:**

- Distribuição do corpus completo por `classe_auditada`: `duvida` 44,8% (4.276), `relevante` 36,4%
  (3.472), `irrelevante` 8,3% (796), `sem_resumo` 5,9% (566), `complementar` 4,5% (432).
- Proporção auditada por classe (tabela 7) é baixa em todas as classes (0,1%–6,5%), consistente com
  a limitação já registrada na ETAPA_08: a auditoria cobriu 100 de 9.542 registros (1,0% do corpus).
- Núcleo analítico concentrado em Scopus (79,7%) e Scopus|WoS (14,3%) — tabela 6.
- Crescimento do núcleo analítico ao longo do tempo acompanha o crescimento do corpus completo
  (tabela 5, figura 3): de 87 registros em 2010 a 495 em 2025 (2026 parcial, ano corrente).

## 4. Figuras geradas

Todas em `05_ANALISE_R/figuras/`, formato PNG, 300 dpi, cada uma com o arquivo de dados-base
correspondente indicado na seção 3:

| Arquivo | Conteúdo | Dados-base |
|---|---|---|
| `figura01_distribuicao_classe_auditada.png` | Barras horizontais — corpus completo por `classe_auditada` | `tabela04_distribuicao_classe_auditada.csv` |
| `figura02_composicao_nucleo_analitico.png` | Barras empilhadas — núcleo vs. fora do núcleo, por `classe_auditada` de origem | `tabela01_corte_nucleo_por_classe.csv` |
| `figura03_evolucao_temporal.png` | Linhas — corpus completo e núcleo analítico por ano (2010–2026) | `tabela05_distribuicao_por_ano.csv` |
| `figura04_nucleo_por_base_origem.png` | Barras horizontais — núcleo analítico por base de origem | `tabela06_nucleo_por_base_origem.csv` |

## 5. Anomalia residual encontrada (registrada, não corrigida nesta etapa)

4 registros de `duvida` têm `bloco_a_presente=nao` e `bloco_b_presente=nao` simultaneamente
(nenhum dos dois blocos presente) — inconsistente com a árvore de decisão da ETAPA_07, que exige
pelo menos um bloco presente para gerar `duvida`. Tratados como fora do núcleo por segurança (mesma
regra de "nenhum bloco" = sem evidência textual dos dois critérios). Não investigado a fundo por
estar fora do escopo desta etapa (tabelas/figuras); fica registrado para o usuário decidir se vale
apuração pontual desses 4 registros.

## 6. Scripts gerados

Em `05_ANALISE_R/scripts/`, em ordem de execução:

1. `00_config.R` — carrega pacotes (`readr`, `dplyr`, `tidyr`, `ggplot2`, `scales`), define caminhos
   e tema gráfico comuns.
2. `01_definir_nucleo_analitico.R` — aplica o critério da seção 1, gera `matriz_nucleo_analitico.csv`
   e as tabelas 1–3.
3. `02_tabelas_descritivas.R` — gera as tabelas 4–8 a partir da matriz com o corte já aplicado.
4. `03_figuras.R` — gera as figuras 1–4 a partir das tabelas 1, 4, 5 e 6.

Scripts em R base + tidyverse (`readr`/`dplyr`/`tidyr`/`ggplot2`/`scales`), sem hardcode de números —
toda estatística é recalculada a partir do CSV de entrada a cada execução.

## 7. Limites desta etapa

- Não decide inclusão/exclusão final de nenhum registro individual para o artigo — só aplica, de
  forma sistemática e documentada, o corte de classe já discutido nas etapas anteriores.
- O corte do núcleo analítico depende de uma extrapolação de amostra pequena para o subgrupo
  "duvida/apenas Bloco A" (seção 1) — não resolvida aqui, registrada para decisão em etapa futura
  (leitura de texto completo do núcleo, se o usuário optar por isso).
- Esta etapa não escreve texto do artigo nem avança para leitura de texto completo (full-text) do
  núcleo analítico.
