## Figuras da ETAPA_10 (resolucao da classe "duvida" e nucleo analitico revisado).
## Nao apaga nem sobrescreve as figuras da ETAPA_09 (figura01-04) -- gera figura05-08 novas.
## Cada figura usa apenas dados ja calculados e salvos em 05_ANALISE_R/tabelas por
## 05_aplicar_resolucao_duvidas.R.

source("05_ANALISE_R/scripts/00_config.R")

dir.create(DIR_FIGURAS, showWarnings = FALSE, recursive = TRUE)

tabela09b <- readr::read_csv(file.path(DIR_TABELAS, "tabela09b_resolucao_duvidas_por_subgrupo.csv"), show_col_types = FALSE)
tabela10 <- readr::read_csv(file.path(DIR_TABELAS, "tabela10_comparacao_nucleo_original_revisado.csv"), show_col_types = FALSE)
tabela12 <- readr::read_csv(file.path(DIR_TABELAS, "tabela12_nucleo_revisado_por_base_origem.csv"), show_col_types = FALSE)
tabela13 <- readr::read_csv(file.path(DIR_TABELAS, "tabela13_nucleo_revisado_por_ano.csv"), show_col_types = FALSE)

## Figura 5: resolucao das 4.276 duvidas, por subgrupo de origem (apenas_bloco_a / apenas_bloco_b /
## nenhum_bloco) x decisao revisada (RELEVANTE / DESCARTAR)
fig5 <- ggplot(tabela09b, aes(x = subgrupo_duvida, y = n, fill = decisao_revisada)) +
  geom_col(position = "stack") +
  geom_text(aes(label = n), position = position_stack(vjust = 0.5), size = 3, color = "white") +
  scale_fill_manual(values = c("RELEVANTE" = "#1b7a3d", "DESCARTAR" = "#b0392b")) +
  labs(
    title = "Resolucao da classe 'duvida' por subgrupo de origem",
    subtitle = "4.276 registros avaliados registro a registro (decisao_duvidas_revisada.tsv)",
    x = NULL, y = "N de registros", fill = "Decisao revisada"
  ) +
  tema_padrao +
  theme(legend.position = "bottom")
ggsave(file.path(DIR_FIGURAS, "figura05_resolucao_duvidas.png"), fig5, width = 7.5, height = 4.5, dpi = 300)

## Figura 6: comparacao nucleo anterior (ETAPA_09, heuristica apenas_bloco_a) x nucleo revisado
## (ETAPA_10, decisao registro a registro)
tabela10_long <- tibble::tibble(
  nucleo = c("Anterior (ETAPA_09)", "Revisado (ETAPA_10)"),
  n = c(tabela10$nucleo_anterior, tabela10$nucleo_revisado)
)
fig6 <- ggplot(tabela10_long, aes(x = nucleo, y = n, fill = nucleo)) +
  geom_col(width = 0.55) +
  geom_text(aes(label = n), vjust = -0.5, size = 4) +
  scale_fill_manual(values = c("Anterior (ETAPA_09)" = "#888888", "Revisado (ETAPA_10)" = "#1b7a3d")) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.15))) +
  labs(
    title = "Nucleo analitico: anterior x revisado",
    subtitle = paste0(
      "Diferenca: ", tabela10$diferenca_absoluta, " registros (",
      tabela10$diferenca_percentual, "%)"
    ),
    x = NULL, y = "N de registros"
  ) +
  tema_padrao +
  theme(legend.position = "none")
ggsave(file.path(DIR_FIGURAS, "figura06_comparacao_nucleo_original_revisado.png"), fig6, width = 6, height = 4.5, dpi = 300)

## Figura 7: nucleo revisado por base de origem
fig7 <- ggplot(tabela12, aes(x = reorder(bases_origem, n), y = n)) +
  geom_col(fill = "#2c6e91") +
  geom_text(aes(label = n), hjust = -0.1, size = 3.2) +
  coord_flip() +
  scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
  labs(
    title = "Nucleo analitico revisado por base de origem",
    subtitle = paste0("n = ", sum(tabela12$n), " registros"),
    x = NULL, y = "N de registros"
  ) +
  tema_padrao
ggsave(file.path(DIR_FIGURAS, "figura07_nucleo_revisado_por_base_origem.png"), fig7, width = 7.5, height = 4, dpi = 300)

## Figura 8: evolucao temporal do nucleo revisado x corpus completo
tabela13_long <- tabela13 %>%
  tidyr::pivot_longer(cols = c(n_corpus, n_nucleo_revisado), names_to = "serie", values_to = "n") %>%
  mutate(serie = recode(serie, n_corpus = "Corpus completo", n_nucleo_revisado = "Nucleo revisado"))
fig8 <- ggplot(tabela13_long, aes(x = ano, y = n, color = serie)) +
  geom_line(linewidth = 0.9) +
  geom_point(size = 1.6) +
  scale_color_manual(values = c("Corpus completo" = "#888888", "Nucleo revisado" = "#1b7a3d")) +
  labs(
    title = "Evolucao temporal do corpus e do nucleo analitico revisado",
    subtitle = "Por ano de publicacao (2010-2026)",
    x = "Ano", y = "N de registros", color = NULL
  ) +
  tema_padrao +
  theme(legend.position = "bottom")
ggsave(file.path(DIR_FIGURAS, "figura08_evolucao_temporal_nucleo_revisado.png"), fig8, width = 8, height = 4.5, dpi = 300)

cat("Figuras da ETAPA_10 salvas em", DIR_FIGURAS, "\n")
