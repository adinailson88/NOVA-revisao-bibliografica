## Exporta, em .txt (delimitado por "|"), todos os registros classe_auditada == "duvida"
## (4.276 registros) para revisao pessoal fora do R. Inclui o subgrupo (apenas_bloco_a /
## apenas_bloco_b / nenhum_bloco) e os termos que dispararam cada bloco, para facilitar a decisao
## registro a registro sobre inclusao/exclusao do nucleo analitico.

source("05_ANALISE_R/scripts/00_config.R")

matriz <- readr::read_csv(
  file.path(DIR_TABELAS, "matriz_nucleo_analitico.csv"),
  show_col_types = FALSE
)

duvida <- matriz %>%
  filter(classe_auditada == "duvida") %>%
  select(
    id_unico, subgrupo_duvida, nucleo_analitico, ano, bases_origem, doi,
    termos_bloco_a, termos_bloco_b, auditado, titulo
  ) %>%
  arrange(desc(subgrupo_duvida == "apenas_bloco_a"), subgrupo_duvida, id_unico)

dir.create(DIR_TABELAS, showWarnings = FALSE, recursive = TRUE)

caminho_saida <- file.path(DIR_TABELAS, "registros_duvida_para_revisao.txt")

readr::write_delim(duvida, caminho_saida, delim = "|", na = "")

cat("Total de registros 'duvida' exportados:", nrow(duvida), "\n")
cat("Arquivo salvo em:", caminho_saida, "\n")
print(table(duvida$subgrupo_duvida))
