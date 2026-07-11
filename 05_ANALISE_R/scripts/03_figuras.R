## Figuras descritivas do corpus e do nucleo analitico.
## Cada figura tem o arquivo de dados-base correspondente salvo em 05_ANALISE_R/tabelas
## (gerado em 02_tabelas_descritivas.R) -- nao ha numero inventado aqui, so plotagem.

source("05_ANALISE_R/scripts/00_config.R")

dir.create(DIR_FIGURAS, showWarnings = FALSE, recursive = TRUE)

tabela_classe <- readr::read_csv(file.path(DIR_TABELAS, "tabela04_distribuicao_classe_auditada.csv"), show_col_types = FALSE)
tabela_ano <- readr::read_csv(file.path(DIR_TABELAS, "tabela05_distribuicao_por_ano.csv"), show_col_types = FALSE)
tabela_base <- readr::read_csv(file.path(DIR_TABELAS, "tabela06_nucleo_por_base_origem.csv"), show_col_types = FALSE)
tabela_corte <- readr::read_csv(file.path(DIR_TABELAS, "tabela01_corte_nucleo_por_classe.csv"), show_col_types = FALSE)

## Figura 1: distribuicao por classe_auditada (corpus completo, 9542 registros)
fig1 <- ggplot(tabela_classe, aes(x = reorder(classe_auditada, n), y = n)) +
  geom_col(fill = "#2c6e91") +
  geom_text(aes(label = paste0(n, " (", pct, "%)")), hjust = -0.05, size = 3.2) +
  coord_flip() +
  scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
  labs(
    title = "Distribuicao do corpus por classe_auditada",
    subtitle = "matriz_triagem_auditada.csv (n = 9.542)",
    x = NULL, y = "N de registros"
  ) +
  tema_padrao
ggsave(file.path(DIR_FIGURAS, "figura01_distribuicao_classe_auditada.png"), fig1, width = 7.5, height = 4, dpi = 300)

## Figura 2: composicao do nucleo analitico (dentro x fora), por classe_auditada de origem
tabela_corte2 <- tabela_corte %>%
  mutate(
    grupo = ifelse(nucleo_analitico, "Nucleo analitico", "Fora do nucleo"),
    classe_auditada = factor(classe_auditada, levels = c("relevante", "duvida", "complementar", "irrelevante", "sem_resumo"))
  )
fig2 <- ggplot(tabela_corte2, aes(x = classe_auditada, y = n, fill = grupo)) +
  geom_col(position = "stack") +
  geom_text(aes(label = n), position = position_stack(vjust = 0.5), size = 3, color = "white") +
  scale_fill_manual(values = c("Nucleo analitico" = "#1b7a3d", "Fora do nucleo" = "#b0b0b0")) +
  labs(
    title = "Corte do nucleo analitico por classe_auditada",
    subtitle = "Nucleo = relevante + duvida/apenas Bloco A (ver relatorio_analise_r.md)",
    x = NULL, y = "N de registros", fill = NULL
  ) +
  tema_padrao +
  theme(legend.position = "bottom")
ggsave(file.path(DIR_FIGURAS, "figura02_composicao_nucleo_analitico.png"), fig2, width = 7.5, height = 4.5, dpi = 300)

## Figura 3: evolucao temporal, corpus completo x nucleo analitico
tabela_ano_long <- tabela_ano %>%
  tidyr::pivot_longer(cols = c(n_corpus, n_nucleo), names_to = "serie", values_to = "n") %>%
  mutate(serie = recode(serie, n_corpus = "Corpus completo", n_nucleo = "Nucleo analitico"))
fig3 <- ggplot(tabela_ano_long, aes(x = ano, y = n, color = serie)) +
  geom_line(linewidth = 0.9) +
  geom_point(size = 1.6) +
  scale_color_manual(values = c("Corpus completo" = "#888888", "Nucleo analitico" = "#1b7a3d")) +
  labs(
    title = "Evolucao temporal do corpus e do nucleo analitico",
    subtitle = "Por ano de publicacao (2010-2026)",
    x = "Ano", y = "N de registros", color = NULL
  ) +
  tema_padrao +
  theme(legend.position = "bottom")
ggsave(file.path(DIR_FIGURAS, "figura03_evolucao_temporal.png"), fig3, width = 8, height = 4.5, dpi = 300)

## Figura 4: nucleo analitico por base de origem
fig4 <- ggplot(tabela_base, aes(x = reorder(bases_origem, n), y = n)) +
  geom_col(fill = "#2c6e91") +
  geom_text(aes(label = n), hjust = -0.1, size = 3.2) +
  coord_flip() +
  scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
  labs(
    title = "Nucleo analitico por base de origem",
    subtitle = paste0("n = ", sum(tabela_base$n), " registros"),
    x = NULL, y = "N de registros"
  ) +
  tema_padrao
ggsave(file.path(DIR_FIGURAS, "figura04_nucleo_por_base_origem.png"), fig4, width = 7.5, height = 4, dpi = 300)

cat("Figuras salvas em", DIR_FIGURAS, "\n")
