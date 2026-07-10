## Gera as tabelas derivadas e os graficos usados no artigo.
## Entrada principal: latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv
## Execucao: Rscript scripts/r/10_gerar_produtos_artigo.R

suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
  library(tidyr)
  library(stringr)
  library(ggplot2)
  library(scales)
})

options(readr.show_col_types = FALSE)

ARQUIVO_NUCLEO <- "latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv"
ARQUIVO_DICIONARIO <- "latex-artigo/fontes/dicionario_criterio_dimensao_etapa17.csv"
ARQUIVO_BUSCAS <- "latex-artigo/fontes/tabela_estrategia_busca.csv"
ARQUIVO_TIPOS_ORIGINAIS <- "latex-artigo/fontes/tabela34_distribuicao_base_tipo_nucleo_final_104.csv"
DIR_FONTES <- "latex-artigo/fontes"
DIR_FIGURAS <- "latex-artigo/figuras"

dir.create(DIR_FONTES, recursive = TRUE, showWarnings = FALSE)
dir.create(DIR_FIGURAS, recursive = TRUE, showWarnings = FALSE)

dados <- readr::read_csv(ARQUIVO_NUCLEO, progress = FALSE)
if (nrow(dados) != 104L) stop("O nucleo final deve conter exatamente 104 registros.")
if (anyDuplicated(dados$id_unico) > 0L) stop("Foram encontrados id_unico duplicados.")
N <- nrow(dados)

normalizar <- function(x) {
  x |> tidyr::replace_na("") |> stringr::str_squish()
}

expandir_multivalor <- function(base, campo, nome_saida) {
  base |>
    dplyr::transmute(id_unico, valor = normalizar(.data[[campo]])) |>
    tidyr::separate_rows(valor, sep = "\\s*;\\s*") |>
    dplyr::filter(valor != "") |>
    dplyr::distinct(id_unico, valor) |>
    dplyr::rename(!!nome_saida := valor)
}

resumir_multivalor <- function(base_expandida, campo) {
  base_expandida |>
    dplyr::group_by(.data[[campo]]) |>
    dplyr::summarise(
      total_registros = dplyr::n_distinct(id_unico),
      ids = paste(sort(unique(id_unico)), collapse = ";"),
      .groups = "drop"
    ) |>
    dplyr::mutate(percentual_dos_104 = round(100 * total_registros / N, 1)) |>
    dplyr::arrange(dplyr::desc(total_registros), .data[[campo]])
}

tema_artigo <- ggplot2::theme_minimal(base_size = 13) +
  ggplot2::theme(
    panel.grid.minor = ggplot2::element_blank(),
    panel.grid.major.y = ggplot2::element_blank(),
    plot.margin = ggplot2::margin(10, 20, 10, 10),
    axis.title = ggplot2::element_text(size = 13),
    axis.text = ggplot2::element_text(size = 11, colour = "black"),
    strip.text = ggplot2::element_text(size = 12, face = "bold"),
    legend.position = "none"
  )

## Tabelas 26 a 30

criterios_long <- expandir_multivalor(
  dados, "criterios_identificados_leitura", "criterio"
)
dicionario <- readr::read_csv(ARQUIVO_DICIONARIO, progress = FALSE) |>
  dplyr::select(criterio, dimensao_roteiro)

tabela26 <- resumir_multivalor(criterios_long, "criterio") |>
  dplyr::left_join(dicionario, by = "criterio") |>
  dplyr::select(criterio, dimensao_roteiro, total_registros, percentual_dos_104, ids)
readr::write_excel_csv(
  tabela26,
  file.path(DIR_FONTES, "tabela26_criterios_nucleo_final_104.csv"),
  na = ""
)

dimensoes_canonicas <- c(
  "tecnica_operacional", "institucional", "ambiental",
  "ciclo_de_vida", "economica", "social"
)
dimensoes_long <- expandir_multivalor(
  dados, "dimensoes_sustentabilidade_identificadas_leitura", "dimensao_identificada_leitura"
)
tabela27 <- resumir_multivalor(dimensoes_long, "dimensao_identificada_leitura") |>
  dplyr::filter(dimensao_identificada_leitura %in% dimensoes_canonicas) |>
  dplyr::mutate(ordem = match(dimensao_identificada_leitura, dimensoes_canonicas)) |>
  dplyr::arrange(ordem) |>
  dplyr::select(-ordem)
readr::write_excel_csv(
  tabela27,
  file.path(DIR_FONTES, "tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv"),
  na = ""
)

metodos_long <- expandir_multivalor(
  dados, "metodos_decisao_identificados_leitura", "metodo_identificado_leitura"
)
tabela28 <- resumir_multivalor(metodos_long, "metodo_identificado_leitura")
readr::write_excel_csv(
  tabela28,
  file.path(DIR_FONTES, "tabela28_metodos_decisao_nucleo_final_104.csv"),
  na = ""
)

contextos_long <- expandir_multivalor(
  dados, "contexto_edificacao_identificado_leitura", "contexto_identificado_leitura"
)
tabela29 <- resumir_multivalor(contextos_long, "contexto_identificado_leitura")
readr::write_excel_csv(
  tabela29,
  file.path(DIR_FONTES, "tabela29_contexto_edificacao_nucleo_final_104.csv"),
  na = ""
)

lacuna_texto <- normalizar(dados$lacuna_ou_limite_identificado_leitura)
com_lacuna <- !stringr::str_detect(
  stringr::str_to_lower(lacuna_texto),
  "^nao_identificada"
)
lacuna_ies <- stringr::str_detect(
  normalizar(dados$tipo_contribuicao_artigo),
  "(^|;)lacuna_para_ies_publicas($|;)"
)

montar_linha_lacuna <- function(categoria, seletor) {
  tibble::tibble(
    categoria = categoria,
    total_registros = sum(seletor),
    percentual_dos_104 = round(100 * sum(seletor) / N, 1),
    ids = paste(sort(dados$id_unico[seletor]), collapse = ";")
  )
}

tabela30 <- dplyr::bind_rows(
  montar_linha_lacuna("com_lacuna_identificada_no_resumo", com_lacuna),
  montar_linha_lacuna("sem_lacuna_identificada_no_resumo", !com_lacuna),
  montar_linha_lacuna("lacuna_especifica_ies_publicas", lacuna_ies)
)
readr::write_excel_csv(
  tabela30,
  file.path(DIR_FONTES, "tabela30_lacunas_nucleo_final_104.csv"),
  na = ""
)

## Coocorrencias

tabela31 <- criterios_long |>
  dplyr::inner_join(metodos_long, by = "id_unico") |>
  dplyr::group_by(criterio, metodo = metodo_identificado_leitura) |>
  dplyr::summarise(
    n_registros_comuns = dplyr::n_distinct(id_unico),
    ids = paste(sort(unique(id_unico)), collapse = ";"),
    .groups = "drop"
  ) |>
  dplyr::arrange(dplyr::desc(n_registros_comuns), criterio, metodo)
readr::write_excel_csv(
  tabela31,
  file.path(DIR_FONTES, "tabela31_coocorrencia_criterio_metodo_nucleo_final_104.csv"),
  na = ""
)

dimensoes_matriz <- c(
  "ambiental", "economica", "social", "tecnica_operacional", "institucional"
)
tabela32 <- dimensoes_long |>
  dplyr::filter(dimensao_identificada_leitura %in% dimensoes_matriz) |>
  dplyr::inner_join(metodos_long, by = "id_unico") |>
  dplyr::group_by(
    dimensao_roteiro = dimensao_identificada_leitura,
    metodo = metodo_identificado_leitura
  ) |>
  dplyr::summarise(
    n_registros_comuns = dplyr::n_distinct(id_unico),
    ids = paste(sort(unique(id_unico)), collapse = ";"),
    .groups = "drop"
  ) |>
  dplyr::arrange(dplyr::desc(n_registros_comuns), dimensao_roteiro, metodo)
readr::write_excel_csv(
  tabela32,
  file.path(DIR_FONTES, "tabela32_coocorrencia_dimensao_metodo_nucleo_final_104.csv"),
  na = ""
)

## Distribuicao temporal, bases, tipos e mencoes a ODS/ESG

tabela33 <- dados |>
  dplyr::count(ano, name = "total_registros") |>
  tidyr::complete(ano = 2010:2026, fill = list(total_registros = 0L)) |>
  dplyr::mutate(
    percentual_dos_104 = round(100 * total_registros / N, 1),
    ids = vapply(
      ano,
      function(a) paste(sort(dados$id_unico[dados$ano == a]), collapse = ";"),
      character(1)
    )
  )
readr::write_excel_csv(
  tabela33,
  file.path(DIR_FONTES, "tabela33_distribuicao_temporal_nucleo_final_104.csv"),
  na = ""
)

bases_long <- dados |>
  dplyr::transmute(id_unico, base = normalizar(bases_origem)) |>
  tidyr::separate_rows(base, sep = "\\s*\\|\\s*") |>
  dplyr::filter(base != "") |>
  dplyr::distinct(id_unico, base)

tabela_bases <- resumir_multivalor(bases_long, "base") |>
  dplyr::rename(categoria = base) |>
  dplyr::mutate(dimensao = "base_origem")
readr::write_excel_csv(
  tabela_bases,
  file.path(DIR_FONTES, "tabela34_bases_origem_nucleo_final_104.csv"),
  na = ""
)

tipos_origem <- readr::read_csv(ARQUIVO_TIPOS_ORIGINAIS, progress = FALSE) |>
  dplyr::filter(dimensao == "tipo_documento") |>
  dplyr::mutate(
    tipo_harmonizado = dplyr::case_when(
      categoria %in% c("Journal", "JOUR", "journal-article") ~ "Artigo de periodico",
      categoria %in% c("Conference Proceeding", "CPAPER") ~ "Trabalho em evento",
      categoria %in% c("Book Series", "Book") ~ "Livro ou serie de livro",
      TRUE ~ "Outro"
    )
  ) |>
  dplyr::group_by(tipo_harmonizado) |>
  dplyr::summarise(
    total_registros = sum(total_registros),
    percentual_dos_104 = round(100 * total_registros / N, 1),
    rotulos_origem = paste(categoria, collapse = ";"),
    .groups = "drop"
  ) |>
  dplyr::arrange(dplyr::desc(total_registros))

readr::write_excel_csv(
  tipos_origem,
  file.path(DIR_FONTES, "tabela34_tipos_documentais_harmonizados_nucleo_final_104.csv"),
  na = ""
)

texto_auditado <- apply(
  dados |>
    dplyr::select(
      titulo, tipo_contribuicao_artigo, criterios_identificados_leitura,
      metodos_decisao_identificados_leitura,
      dimensoes_sustentabilidade_identificadas_leitura,
      lacuna_ou_limite_identificado_leitura, evidencia_curta_do_resumo
    ),
  1,
  paste,
  collapse = " "
)
mencao_ods <- stringr::str_detect(
  texto_auditado,
  stringr::regex("\\b(ODS|SDGs?)\\b", ignore_case = TRUE)
)
mencao_esg <- stringr::str_detect(
  texto_auditado,
  stringr::regex("\\bESG\\b", ignore_case = TRUE)
)

tabela35 <- dplyr::bind_rows(
  tibble::tibble(
    marcador = "ODS ou SDG",
    total_registros = sum(mencao_ods),
    percentual_dos_104 = round(100 * sum(mencao_ods) / N, 1),
    ids = paste(sort(dados$id_unico[mencao_ods]), collapse = ";")
  ),
  tibble::tibble(
    marcador = "ESG",
    total_registros = sum(mencao_esg),
    percentual_dos_104 = round(100 * sum(mencao_esg) / N, 1),
    ids = paste(sort(dados$id_unico[mencao_esg]), collapse = ";")
  )
)
readr::write_excel_csv(
  tabela35,
  file.path(DIR_FONTES, "tabela35_mencoes_ods_esg_nucleo_final_104.csv"),
  na = ""
)

buscas <- readr::read_csv(ARQUIVO_BUSCAS, progress = FALSE)
tabela_buscas_resumo <- buscas |>
  dplyr::mutate(
    complemento_manual = stringr::str_detect(string_id, "complemento_manual"),
    modelo = dplyr::case_when(
      base == "Scopus" ~ "TITLE-ABS-KEY com expressao booleana",
      base == "Web of Science" ~ "TS com expressao booleana",
      base == "Crossref" ~ "query.bibliographic por relevancia"
    )
  ) |>
  dplyr::group_by(base, modelo) |>
  dplyr::summarise(
    n_consultas = sum(!complemento_manual),
    registros_brutos = sum(retorno_bruto),
    complemento_manual = sum(retorno_bruto[complemento_manual]),
    .groups = "drop"
  )
readr::write_excel_csv(
  tabela_buscas_resumo,
  file.path(DIR_FONTES, "tabela_resumo_estrategia_busca.csv"),
  na = ""
)

if (sum(tabela_buscas_resumo$registros_brutos) != 12118L) {
  stop("O total bruto consolidado da estrategia de busca deve ser 12.118.")
}
if (sum(mencao_ods) != 1L || sum(mencao_esg) != 0L) {
  stop("As contagens de ODS/SDG ou ESG divergiram do nucleo auditado.")
}

## Graficos em tons de cinza

grafico_temporal <- ggplot2::ggplot(
  tabela33,
  ggplot2::aes(x = ano, y = total_registros)
) +
  ggplot2::geom_col(
    fill = "grey72", colour = "black", linewidth = 0.35, width = 0.78
  ) +
  ggplot2::geom_text(
    ggplot2::aes(label = total_registros),
    vjust = -0.45,
    size = 4
  ) +
  ggplot2::scale_x_continuous(breaks = 2010:2026) +
  ggplot2::scale_y_continuous(
    expand = ggplot2::expansion(mult = c(0, 0.12)),
    breaks = scales::breaks_pretty(6)
  ) +
  ggplot2::labs(x = "Ano de publicação", y = "Registros") +
  tema_artigo +
  ggplot2::theme(
    axis.text.x = ggplot2::element_text(angle = 45, hjust = 1)
  )

ggplot2::ggsave(
  file.path(DIR_FIGURAS, "figura09_distribuicao_temporal_nucleo_final_104.png"),
  grafico_temporal,
  width = 9,
  height = 4.8,
  dpi = 300,
  bg = "white"
)

rotulos_dimensoes <- c(
  tecnica_operacional = "Técnica e operacional",
  institucional = "Institucional",
  ambiental = "Ambiental",
  ciclo_de_vida = "Ciclo de vida",
  economica = "Econômica",
  social = "Social"
)
dados_dimensoes_grafico <- tabela27 |>
  dplyr::mutate(
    rotulo = unname(rotulos_dimensoes[dimensao_identificada_leitura]),
    rotulo = factor(rotulo, levels = rev(unname(rotulos_dimensoes)))
  )

grafico_dimensoes <- ggplot2::ggplot(
  dados_dimensoes_grafico,
  ggplot2::aes(x = rotulo, y = total_registros)
) +
  ggplot2::geom_col(
    fill = "grey68", colour = "black", linewidth = 0.35, width = 0.72
  ) +
  ggplot2::geom_text(
    ggplot2::aes(label = paste0(total_registros, " (", percentual_dos_104, "%)")),
    hjust = -0.08,
    size = 4.2
  ) +
  ggplot2::coord_flip() +
  ggplot2::scale_y_continuous(
    limits = c(0, 122),
    expand = ggplot2::expansion(mult = c(0, 0))
  ) +
  ggplot2::labs(x = NULL, y = "Registros") +
  tema_artigo

ggplot2::ggsave(
  file.path(DIR_FIGURAS, "figura12_dimensoes_sustentabilidade_nucleo_final_104.png"),
  grafico_dimensoes,
  width = 8.5,
  height = 5.2,
  dpi = 300,
  bg = "white"
)

metodos_gerais <- c(
  "framework", "decision support", "BIM", "optimization", "scoring",
  "life-cycle cost", "fuzzy", "ranking", "IoT", "machine learning", "digital twin"
)
metodos_estruturados <- c(
  "AHP", "TOPSIS", "ANP", "MCDM", "Delphi",
  "Balanced scorecard", "Case-based reasoning", "Bayesian Best-Worst Method"
)
rotulos_metodos <- stats::setNames(
  c(
    "Framework", "Apoio à decisão", "BIM", "Otimização", "Pontuação",
    "Custo do ciclo de vida", "Lógica difusa", "Ordenação", "IoT",
    "Aprendizado de máquina", "Gêmeo digital", "AHP", "TOPSIS", "ANP",
    "MCDM", "Delphi", "Balanced scorecard", "Raciocínio baseado em casos",
    "Bayesian Best-Worst Method"
  ),
  c(metodos_gerais, metodos_estruturados)
)

dados_metodos_grafico <- tabela28 |>
  dplyr::filter(
    metodo_identificado_leitura %in% c(metodos_gerais, metodos_estruturados)
  ) |>
  dplyr::mutate(
    grupo = ifelse(
      metodo_identificado_leitura %in% metodos_estruturados,
      "Métodos formalmente nomeados",
      "Abordagens e instrumentos gerais"
    ),
    rotulo = unname(rotulos_metodos[metodo_identificado_leitura])
  ) |>
  dplyr::arrange(grupo, total_registros) |>
  dplyr::mutate(rotulo = factor(rotulo, levels = unique(rotulo)))

grafico_metodos <- ggplot2::ggplot(
  dados_metodos_grafico,
  ggplot2::aes(x = rotulo, y = total_registros, fill = grupo)
) +
  ggplot2::geom_col(colour = "black", linewidth = 0.3, width = 0.72) +
  ggplot2::geom_text(
    ggplot2::aes(label = total_registros),
    hjust = -0.12,
    size = 4
  ) +
  ggplot2::coord_flip() +
  ggplot2::facet_grid(
    grupo ~ .,
    scales = "free_y",
    space = "free_y",
    switch = "y"
  ) +
  ggplot2::scale_fill_manual(
    values = c(
      "Abordagens e instrumentos gerais" = "grey72",
      "Métodos formalmente nomeados" = "grey45"
    )
  ) +
  ggplot2::scale_y_continuous(
    expand = ggplot2::expansion(mult = c(0, 0.12))
  ) +
  ggplot2::labs(x = NULL, y = "Registros") +
  tema_artigo +
  ggplot2::theme(
    strip.placement = "outside",
    strip.background = ggplot2::element_rect(fill = "grey92", colour = "black"),
    strip.text.y.left = ggplot2::element_text(angle = 0)
  )

ggplot2::ggsave(
  file.path(DIR_FIGURAS, "figura11_metodos_mcdm_mais_frequentes_nucleo_final_104.png"),
  grafico_metodos,
  width = 9,
  height = 8.2,
  dpi = 300,
  bg = "white"
)

top_criterios <- tabela26 |>
  dplyr::slice_max(total_registros, n = 10, with_ties = FALSE) |>
  dplyr::pull(criterio)
top_metodos <- tabela28 |>
  dplyr::slice_max(total_registros, n = 10, with_ties = FALSE) |>
  dplyr::pull(metodo_identificado_leitura)

rotulos_criterios <- c(
  desempenho_operacional = "Desempenho operacional",
  informacao_dados = "Informação e dados",
  custo = "Custo",
  vida_util = "Vida útil",
  energia = "Energia",
  risco = "Risco",
  condicao_fisica = "Condição física",
  manutenibilidade = "Manutenibilidade",
  conforto = "Conforto",
  seguranca = "Segurança"
)

heat_criterios <- tabela31 |>
  dplyr::filter(criterio %in% top_criterios, metodo %in% top_metodos) |>
  tidyr::complete(
    criterio = top_criterios,
    metodo = top_metodos,
    fill = list(n_registros_comuns = 0L)
  ) |>
  dplyr::mutate(
    criterio_rotulo = factor(
      unname(rotulos_criterios[criterio]),
      levels = rev(unname(rotulos_criterios[top_criterios]))
    ),
    metodo_rotulo = factor(
      unname(rotulos_metodos[metodo]),
      levels = unname(rotulos_metodos[top_metodos])
    )
  )

grafico_heat_criterios <- ggplot2::ggplot(
  heat_criterios,
  ggplot2::aes(
    x = metodo_rotulo, y = criterio_rotulo, fill = n_registros_comuns
  )
) +
  ggplot2::geom_tile(colour = "white", linewidth = 0.4) +
  ggplot2::geom_text(
    ggplot2::aes(
      label = n_registros_comuns,
      colour = n_registros_comuns > max(n_registros_comuns) * 0.55
    ),
    size = 4.2
  ) +
  ggplot2::scale_fill_gradient(low = "white", high = "grey18") +
  ggplot2::scale_colour_manual(values = c("FALSE" = "black", "TRUE" = "white")) +
  ggplot2::labs(x = "Instrumento de apoio à decisão", y = "Critério") +
  tema_artigo +
  ggplot2::theme(
    axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, size = 10.5),
    axis.text.y = ggplot2::element_text(size = 10.5)
  )

ggplot2::ggsave(
  file.path(DIR_FIGURAS, "figura13_heatmap_criterios_metodos_nucleo_final_104.png"),
  grafico_heat_criterios,
  width = 10.5,
  height = 7.2,
  dpi = 300,
  bg = "white"
)

heat_dimensoes <- tabela32 |>
  dplyr::filter(
    dimensao_roteiro %in% dimensoes_matriz,
    metodo %in% top_metodos
  ) |>
  tidyr::complete(
    dimensao_roteiro = dimensoes_matriz,
    metodo = top_metodos,
    fill = list(n_registros_comuns = 0L)
  ) |>
  dplyr::mutate(
    dimensao_rotulo = factor(
      unname(rotulos_dimensoes[dimensao_roteiro]),
      levels = rev(unname(rotulos_dimensoes[dimensoes_matriz]))
    ),
    metodo_rotulo = factor(
      unname(rotulos_metodos[metodo]),
      levels = unname(rotulos_metodos[top_metodos])
    )
  )

grafico_heat_dimensoes <- ggplot2::ggplot(
  heat_dimensoes,
  ggplot2::aes(
    x = metodo_rotulo, y = dimensao_rotulo, fill = n_registros_comuns
  )
) +
  ggplot2::geom_tile(colour = "white", linewidth = 0.4) +
  ggplot2::geom_text(
    ggplot2::aes(
      label = n_registros_comuns,
      colour = n_registros_comuns > max(n_registros_comuns) * 0.55
    ),
    size = 4.4
  ) +
  ggplot2::scale_fill_gradient(low = "white", high = "grey18") +
  ggplot2::scale_colour_manual(values = c("FALSE" = "black", "TRUE" = "white")) +
  ggplot2::labs(x = "Instrumento de apoio à decisão", y = "Dimensão") +
  tema_artigo +
  ggplot2::theme(
    axis.text.x = ggplot2::element_text(angle = 45, hjust = 1, size = 10.5),
    axis.text.y = ggplot2::element_text(size = 11)
  )

ggplot2::ggsave(
  file.path(DIR_FIGURAS, "figura14_matriz_analitica_dimensao_metodo_nucleo_final_104.png"),
  grafico_heat_dimensoes,
  width = 10.5,
  height = 5.6,
  dpi = 300,
  bg = "white"
)

cat("Tabelas e graficos do artigo gerados com sucesso.\n")
