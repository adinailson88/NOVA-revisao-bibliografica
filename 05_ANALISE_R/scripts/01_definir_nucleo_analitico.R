## Define o corte do nucleo analitico a partir de matriz_triagem_auditada.csv.
##
## Criterio adotado (ver justificativa completa em 05_ANALISE_R/relatorio_analise_r.md,
## secao "Definicao do nucleo analitico"):
##   - classe_auditada == "relevante"                                  -> nucleo
##   - classe_auditada == "duvida" E bloco_a_presente == "sim"
##     E bloco_b_presente == "nao" (subgrupo "apenas Bloco A")         -> nucleo
##   - classe_auditada == "duvida" E bloco_b_presente == "sim"
##     E bloco_a_presente == "nao" (subgrupo "apenas Bloco B")         -> fora do nucleo
##   - qualquer outra combinacao dentro de "duvida" (ambos ou nenhum
##     bloco presente)                                                 -> fora do nucleo
##   - classe_auditada em complementar, irrelevante, sem_resumo        -> fora do nucleo

source("05_ANALISE_R/scripts/00_config.R")

matriz <- carregar_matriz()

matriz <- matriz %>%
  mutate(
    subgrupo_duvida = case_when(
      classe_auditada != "duvida" ~ NA_character_,
      bloco_a_presente == "sim" & bloco_b_presente == "nao" ~ "apenas_bloco_a",
      bloco_a_presente == "nao" & bloco_b_presente == "sim" ~ "apenas_bloco_b",
      bloco_a_presente == "sim" & bloco_b_presente == "sim" ~ "ambos_blocos",
      TRUE ~ "nenhum_bloco"
    ),
    nucleo_analitico = case_when(
      classe_auditada == "relevante" ~ TRUE,
      classe_auditada == "duvida" & subgrupo_duvida == "apenas_bloco_a" ~ TRUE,
      TRUE ~ FALSE
    )
  )

dir.create(DIR_TABELAS, showWarnings = FALSE, recursive = TRUE)

readr::write_csv(matriz, "05_ANALISE_R/tabelas/matriz_nucleo_analitico.csv")

## Tabela 1: contagem por classe_auditada x nucleo_analitico
tabela_corte <- matriz %>%
  count(classe_auditada, nucleo_analitico, name = "n") %>%
  arrange(desc(nucleo_analitico), desc(n))
readr::write_csv(tabela_corte, file.path(DIR_TABELAS, "tabela01_corte_nucleo_por_classe.csv"))

## Tabela 2: detalhe do subgrupo dentro de duvida
tabela_duvida <- matriz %>%
  filter(classe_auditada == "duvida") %>%
  count(subgrupo_duvida, nucleo_analitico, name = "n") %>%
  arrange(desc(n))
readr::write_csv(tabela_duvida, file.path(DIR_TABELAS, "tabela02_subgrupos_duvida.csv"))

## Resumo final do nucleo analitico
resumo_nucleo <- matriz %>%
  count(nucleo_analitico, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1))
readr::write_csv(resumo_nucleo, file.path(DIR_TABELAS, "tabela03_resumo_nucleo_analitico.csv"))

cat("Total de registros:", nrow(matriz), "\n")
cat("Nucleo analitico (TRUE):", sum(matriz$nucleo_analitico), "\n")
cat("Fora do nucleo (FALSE):", sum(!matriz$nucleo_analitico), "\n")
print(tabela_corte)
print(tabela_duvida)
