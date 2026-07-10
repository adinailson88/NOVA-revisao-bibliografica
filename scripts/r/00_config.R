## Configuracao comum aos scripts da etapa de tabelas e figuras.
## Caminhos relativos a raiz do projeto (assume working directory = raiz do projeto).

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
  library(ggplot2)
  library(scales)
})

CAMINHO_MATRIZ <- "04_TRIAGEM/matriz_triagem_auditada.csv"
DIR_TABELAS <- "05_ANALISE_R/tabelas"
DIR_FIGURAS <- "05_ANALISE_R/figuras"

carregar_matriz <- function(caminho = CAMINHO_MATRIZ) {
  readr::read_csv(caminho, show_col_types = FALSE, progress = FALSE)
}

tema_padrao <- theme_minimal(base_size = 11) +
  theme(
    plot.title = element_text(face = "bold", size = 12),
    panel.grid.minor = element_blank()
  )
