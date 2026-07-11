## Tabelas descritivas sobre o corpus (todas as classes) e sobre o nucleo analitico
## (classe_auditada == "relevante" ou "duvida"/apenas Bloco A -- ver 01_definir_nucleo_analitico.R).
## Depende do arquivo 05_ANALISE_R/tabelas/matriz_nucleo_analitico.csv gerado no script anterior.

source("05_ANALISE_R/scripts/00_config.R")

matriz <- readr::read_csv(
  file.path(DIR_TABELAS, "matriz_nucleo_analitico.csv"),
  show_col_types = FALSE
)

## Tabela 4: distribuicao por classe_auditada (corpus completo, 9542 registros)
tabela_classe <- matriz %>%
  count(classe_auditada, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1)) %>%
  arrange(desc(n))
readr::write_csv(tabela_classe, file.path(DIR_TABELAS, "tabela04_distribuicao_classe_auditada.csv"))

## Tabela 5: distribuicao por ano, nucleo analitico vs. corpus completo
tabela_ano <- matriz %>%
  filter(!is.na(ano)) %>%
  group_by(ano) %>%
  summarise(
    n_corpus = n(),
    n_nucleo = sum(nucleo_analitico),
    .groups = "drop"
  ) %>%
  arrange(ano)
readr::write_csv(tabela_ano, file.path(DIR_TABELAS, "tabela05_distribuicao_por_ano.csv"))

## Tabela 6: distribuicao por base de origem (nucleo analitico)
tabela_base <- matriz %>%
  filter(nucleo_analitico) %>%
  count(bases_origem, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1)) %>%
  arrange(desc(n))
readr::write_csv(tabela_base, file.path(DIR_TABELAS, "tabela06_nucleo_por_base_origem.csv"))

## Tabela 7: proporcao auditada (leitura individual) vs. nao auditada, por classe_auditada
tabela_auditoria <- matriz %>%
  count(classe_auditada, auditado, name = "n") %>%
  group_by(classe_auditada) %>%
  mutate(pct = round(100 * n / sum(n), 1)) %>%
  ungroup() %>%
  arrange(classe_auditada, desc(auditado))
readr::write_csv(tabela_auditoria, file.path(DIR_TABELAS, "tabela07_proporcao_auditada_por_classe.csv"))

## Tabela 8: quantos dos 314 registros "duvida/apenas Bloco A" incluidos no nucleo foram
## de fato lidos individualmente na auditoria por amostra (evidencia direta vs. extrapolada)
tabela_duvida_a_auditoria <- matriz %>%
  filter(classe_auditada == "duvida", subgrupo_duvida == "apenas_bloco_a") %>%
  count(auditado, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1))
readr::write_csv(tabela_duvida_a_auditoria, file.path(DIR_TABELAS, "tabela08_duvida_bloco_a_evidencia_auditoria.csv"))

print(tabela_classe)
print(tabela_duvida_a_auditoria)
cat("Tabelas descritivas salvas em", DIR_TABELAS, "\n")
