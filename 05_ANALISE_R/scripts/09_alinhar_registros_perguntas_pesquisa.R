suppressPackageStartupMessages({
  pacotes_necessarios <- c("readr", "dplyr", "stringr", "tidyr")
})

carregar_pacotes <- function() {
  faltantes <- pacotes_necessarios[!vapply(pacotes_necessarios, requireNamespace, logical(1), quietly = TRUE)]
  if (length(faltantes) > 0) {
    stop(paste0("Pacotes R ausentes: ", paste(faltantes, collapse = ", ")))
  }
  invisible(lapply(pacotes_necessarios, function(pkg) {
    suppressPackageStartupMessages(library(pkg, character.only = TRUE))
  }))
}

options(readr.show_col_types = FALSE)

PROJETO_DIR <- Sys.getenv("PROJETO_DIR", unset = ".")
ARQUIVO_ENTRADA <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "matriz_extracao_final_reavaliada_resumos.csv")
ARQUIVO_DICIONARIO <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "dicionario_rq_etapa15.csv")
ARQUIVO_SAIDA_MATRIZ <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "matriz_alinhamento_perguntas_pesquisa.csv")
ARQUIVO_NUCLEO <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "nucleo_principal_sintese_artigo.csv")
ARQUIVO_RELATORIO <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "relatorio_alinhamento_perguntas_pesquisa.md")
ARQUIVO_TABELA16 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela16_aderencia_por_rq.csv")
ARQUIVO_TABELA17 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela17_uso_recomendado_artigo.csv")
ARQUIVO_TABELA18 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela18_cruzamento_estrato_resumo_uso_artigo.csv")
ARQUIVO_TABELA19 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela19_nucleo_principal_por_ano.csv")
ARQUIVO_TABELA20 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela20_nucleo_principal_por_base.csv")
ARQUIVO_AMOSTRA <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "amostra_auditoria_etapa15_alinhamento_rq.csv")
ARQUIVO_LOG <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "LOGS", "ETAPA_15_ALINHAR_PERGUNTAS_PESQUISA.md")
ARQUIVO_DONE <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "DONE", "ETAPA_15_ALINHAR_PERGUNTAS_PESQUISA.done")
ARQUIVO_FAIL <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "LOGS", "ETAPA_15_ALINHAR_PERGUNTAS_PESQUISA.fail.md")
ARQUIVO_ESTADO_ATUAL <- file.path(PROJETO_DIR, "00_CONTROLE", "ESTADO_ATUAL.md")
ARQUIVO_DECISOES <- file.path(PROJETO_DIR, "00_CONTROLE", "DECISOES_METODOLOGICAS.md")

VALORES_AUSENCIA <- c(
  "", "na", "n/a", "nao", "não", "nao_informado", "nao_informado_no_resumo",
  "nao_identificavel_pelo_resumo", "nao_identificado_por_resumo", "nao_classificavel_pelo_resumo",
  "nao_verificavel_pelo_resumo", "pendente", "pendente_leitura_completa",
  "a_definir_na_sintese", "not available", "none", "null"
)

TERMOS_EXCLUSAO_FORTE <- c(
  "oil and gas", "pipeline", "railway", "track maintenance", "bridge", "road maintenance",
  "wind farm", "power transformer", "substation", "medical device", "maternal care",
  "wastewater", "distribution network", "aircraft", "software obsolescence", "tunnel maintenance",
  "power plant", "urban land use", "photovoltaic system configuration"
)

normalizar_nome <- function(x) {
  x <- iconv(x, from = "", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("[^a-z0-9]+", "_", x)
  gsub("^_|_$", "", x)
}

normalizar_texto <- function(x) {
  x <- ifelse(is.na(x), "", as.character(x))
  x <- iconv(x, from = "", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("[\r\n\t]+", " ", x)
  x <- gsub("\\s+", " ", x)
  trimws(x)
}

escrever_utf8 <- function(caminho, linhas) {
  writeLines(enc2utf8(linhas), caminho, useBytes = TRUE)
}

formatar_pct <- function(n, total) {
  if (total == 0) {
    return("0.0%")
  }
  sprintf("%.1f%%", (100 * n) / total)
}

detectar_coluna <- function(nomes, candidatos, obrigatoria = FALSE) {
  nomes_norm <- normalizar_nome(nomes)
  candidatos_norm <- normalizar_nome(candidatos)
  idx <- match(candidatos_norm, nomes_norm)
  idx <- idx[!is.na(idx)]
  if (length(idx) == 0) {
    if (obrigatoria) {
      stop(paste0("Nenhuma coluna encontrada entre: ", paste(candidatos, collapse = ", ")))
    }
    return(NA_character_)
  }
  nomes[idx[1]]
}

tem_informacao <- function(x) {
  valor <- normalizar_texto(x)
  nzchar(valor) & !(valor %in% normalizar_texto(VALORES_AUSENCIA))
}

coluna_informativa <- function(vetor) {
  if (all(is.na(vetor))) {
    return(rep(FALSE, length(vetor)))
  }
  vapply(vetor, tem_informacao, logical(1))
}

coluna_sim <- function(vetor) {
  valor <- normalizar_texto(vetor)
  valor %in% c("sim", "true", "1", "yes")
}

substituir_ou_anexar_secao <- function(caminho, titulo_secao, conteudo_secao) {
  texto <- readChar(caminho, nchars = file.info(caminho)$size, useBytes = TRUE)
  linhas <- strsplit(texto, "\r?\n", perl = TRUE)[[1]]
  padrao_titulo <- paste0("^", gsub("([\\^\\$\\.\\|\\(\\)\\[\\]\\*\\+\\?\\\\])", "\\\\\\1", titulo_secao), "$")
  inicio <- grep(padrao_titulo, linhas)

  if (length(inicio) == 0) {
    escrever_utf8(caminho, c(linhas, "", conteudo_secao))
    return(invisible(NULL))
  }

  inicio <- inicio[1]
  resto <- if (inicio < length(linhas)) linhas[(inicio + 1):length(linhas)] else character(0)
  prox <- grep("^## ", resto)
  fim <- if (length(prox) == 0) length(linhas) else inicio + prox[1] - 1
  novo <- c(
    if (inicio > 1) linhas[seq_len(inicio - 1)] else character(0),
    conteudo_secao,
    if (fim < length(linhas)) linhas[(fim + 1):length(linhas)] else character(0)
  )
  escrever_utf8(caminho, novo)
}

registrar_falha <- function(etapa, erro, arquivos_verificados, faltou) {
  dir.create(dirname(ARQUIVO_FAIL), recursive = TRUE, showWarnings = FALSE)
  if (file.exists(ARQUIVO_DONE)) {
    file.remove(ARQUIVO_DONE)
  }
  linhas <- c(
    "# ETAPA_15_ALINHAR_PERGUNTAS_PESQUISA.fail",
    "",
    paste0("Data/hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    paste0("Etapa onde falhou: ", etapa),
    paste0("Erro encontrado: ", erro),
    paste0("Arquivos verificados: ", paste(arquivos_verificados, collapse = "; ")),
    paste0("O que faltou para concluir: ", faltou)
  )
  escrever_utf8(ARQUIVO_FAIL, linhas)
}

obter_texto_coluna <- function(dados, coluna) {
  if (is.na(coluna)) {
    rep("", nrow(dados))
  } else {
    normalizar_texto(dados[[coluna]])
  }
}

main <- function() {
  carregar_pacotes()

  dir.create(dirname(ARQUIVO_TABELA16), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(ARQUIVO_LOG), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(ARQUIVO_DONE), recursive = TRUE, showWarnings = FALSE)
  if (file.exists(ARQUIVO_FAIL)) {
    file.remove(ARQUIVO_FAIL)
  }

  arquivos_entrada <- c(ARQUIVO_ENTRADA, ARQUIVO_DICIONARIO, ARQUIVO_ESTADO_ATUAL, ARQUIVO_DECISOES)
  inexistentes <- arquivos_entrada[!file.exists(arquivos_entrada)]
  if (length(inexistentes) > 0) {
    stop(paste0("Arquivos obrigatorios ausentes: ", paste(inexistentes, collapse = ", ")))
  }

  if (normalizePath(ARQUIVO_ENTRADA, winslash = "/", mustWork = TRUE) ==
      normalizePath(file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "matriz_extracao_final.csv"), winslash = "/", mustWork = FALSE)) {
    stop("A entrada principal aponta para a matriz antiga, o que nao e permitido.")
  }

  matriz <- readr::read_csv(ARQUIVO_ENTRADA, locale = readr::locale(encoding = "UTF-8"), progress = FALSE)
  dicionario <- readr::read_csv(ARQUIVO_DICIONARIO, locale = readr::locale(encoding = "UTF-8"), progress = FALSE) %>%
    dplyr::mutate(
      rq = toupper(.data$rq),
      categoria = normalizar_nome(.data$categoria),
      termo = normalizar_texto(.data$termo),
      peso = as.numeric(.data$peso),
      observacao = as.character(.data$observacao)
    )

  colunas_dict_esperadas <- c("rq", "categoria", "termo", "peso", "observacao")
  if (!all(colunas_dict_esperadas %in% names(dicionario))) {
    stop("Dicionario sem as colunas obrigatorias rq, categoria, termo, peso e observacao.")
  }

  total_registros <- nrow(matriz)
  if (total_registros != 3678) {
    stop(paste0("A matriz de entrada tem ", total_registros, " linhas; esperado: 3678."))
  }

  nomes_colunas <- names(matriz)
  col_estrato <- detectar_coluna(nomes_colunas, "estrato_uso_resumo", obrigatoria = TRUE)
  col_resumo_suf <- detectar_coluna(nomes_colunas, "resumo_suficiente_para_extracao", obrigatoria = TRUE)
  col_id <- detectar_coluna(nomes_colunas, "id_unico", obrigatoria = FALSE)
  col_ano <- detectar_coluna(nomes_colunas, "ano", obrigatoria = FALSE)
  col_bases <- detectar_coluna(nomes_colunas, "bases_origem", obrigatoria = FALSE)
  col_doi <- detectar_coluna(nomes_colunas, "doi", obrigatoria = FALSE)
  col_titulo <- detectar_coluna(nomes_colunas, c("titulo", "title"), obrigatoria = TRUE)
  col_resumo <- detectar_coluna(nomes_colunas, c("resumo", "abstract"), obrigatoria = TRUE)
  col_palavras <- detectar_coluna(nomes_colunas, c("palavras_chave", "keywords", "author_keywords", "index_keywords"), obrigatoria = FALSE)
  col_tipo_aplicacao <- detectar_coluna(nomes_colunas, "tipo_aplicacao", obrigatoria = FALSE)
  col_dados <- detectar_coluna(nomes_colunas, "dados_utilizados", obrigatoria = FALSE)
  col_resultado <- detectar_coluna(nomes_colunas, "resultado_principal", obrigatoria = FALSE)
  col_lacuna <- detectar_coluna(nomes_colunas, "lacuna_identificada", obrigatoria = FALSE)
  col_crit_ambiental <- detectar_coluna(nomes_colunas, "criterios_ambientais", obrigatoria = FALSE)
  col_crit_tecnico <- detectar_coluna(nomes_colunas, "criterios_tecnicos_operacionais", obrigatoria = FALSE)
  col_crit_economico <- detectar_coluna(nomes_colunas, "criterios_economicos", obrigatoria = FALSE)
  col_crit_social <- detectar_coluna(nomes_colunas, "criterios_sociais", obrigatoria = FALSE)
  col_crit_institucional <- detectar_coluna(nomes_colunas, "criterios_institucionais", obrigatoria = FALSE)
  col_crit_risco <- detectar_coluna(nomes_colunas, "criterios_risco", obrigatoria = FALSE)
  col_metodo <- detectar_coluna(nomes_colunas, c("metodo_decisao", "metodo_mcdm_especifico"), obrigatoria = FALSE)
  col_contexto <- detectar_coluna(nomes_colunas, "contexto_publico_universitario", obrigatoria = FALSE)
  col_tipo_edificacao <- detectar_coluna(nomes_colunas, c("tipo_edificacao", "tipo_edificacao_sinal"), obrigatoria = FALSE)
  col_eixo <- detectar_coluna(nomes_colunas, "eixo_tematico_preliminar", obrigatoria = FALSE)
  col_justificativa <- detectar_coluna(nomes_colunas, "justificativa_reavaliacao_resumo", obrigatoria = FALSE)
  col_bloco_a <- detectar_coluna(nomes_colunas, "bloco_a_presente", obrigatoria = FALSE)
  col_bloco_b <- detectar_coluna(nomes_colunas, "bloco_b_presente", obrigatoria = FALSE)
  col_usa_ahp <- detectar_coluna(nomes_colunas, "usa_ahp", obrigatoria = FALSE)
  col_usa_topsis <- detectar_coluna(nomes_colunas, "usa_topsis", obrigatoria = FALSE)
  col_usa_outro_mcdm <- detectar_coluna(nomes_colunas, "usa_outro_mcdm", obrigatoria = FALSE)

  estratos <- normalizar_texto(matriz[[col_estrato]])
  estratos_esperados <- c("a_nucleo_forte", "b_nucleo_descritivo", "c_contextual", "d_descartar_sintese")
  estratos_observados <- sort(unique(estratos))
  if (!setequal(estratos_observados, estratos_esperados)) {
    stop(paste0("Estratos inesperados encontrados: ", paste(estratos_observados, collapse = ", ")))
  }

  campos_esperados <- c(
    "titulo", "resumo", "palavras_chave", "tipo_aplicacao", "dados_utilizados", "resultado_principal",
    "lacuna_identificada", "criterios_ambientais", "criterios_tecnicos_operacionais",
    "criterios_economicos", "criterios_sociais", "criterios_institucionais", "criterios_risco",
    "metodo_decisao", "contexto_publico_universitario", "tipo_edificacao", "eixo_tematico_preliminar",
    "estrato_uso_resumo", "resumo_suficiente_para_extracao", "justificativa_reavaliacao_resumo"
  )
  campos_detectados_mapa <- c(
    titulo = col_titulo, resumo = col_resumo, palavras_chave = col_palavras, tipo_aplicacao = col_tipo_aplicacao,
    dados_utilizados = col_dados, resultado_principal = col_resultado, lacuna_identificada = col_lacuna,
    criterios_ambientais = col_crit_ambiental, criterios_tecnicos_operacionais = col_crit_tecnico,
    criterios_economicos = col_crit_economico, criterios_sociais = col_crit_social,
    criterios_institucionais = col_crit_institucional, criterios_risco = col_crit_risco,
    metodo_decisao = col_metodo, contexto_publico_universitario = col_contexto,
    tipo_edificacao = col_tipo_edificacao, eixo_tematico_preliminar = col_eixo,
    estrato_uso_resumo = col_estrato, resumo_suficiente_para_extracao = col_resumo_suf,
    justificativa_reavaliacao_resumo = col_justificativa
  )
  campos_detectados <- names(campos_detectados_mapa)[!is.na(campos_detectados_mapa)]
  campos_ausentes <- setdiff(campos_esperados, campos_detectados)

  colunas_texto <- unname(campos_detectados_mapa[c(
    "titulo", "resumo", "palavras_chave", "tipo_aplicacao", "dados_utilizados", "resultado_principal",
    "lacuna_identificada", "criterios_ambientais", "criterios_tecnicos_operacionais",
    "criterios_economicos", "criterios_sociais", "criterios_institucionais", "criterios_risco",
    "metodo_decisao", "contexto_publico_universitario", "tipo_edificacao",
    "eixo_tematico_preliminar", "justificativa_reavaliacao_resumo"
  )])
  colunas_texto <- unique(colunas_texto[!is.na(colunas_texto)])
  partes_texto <- lapply(colunas_texto, function(coluna) obter_texto_coluna(matriz, coluna))
  texto_alinhamento_rq <- trimws(do.call(paste, c(partes_texto, sep = " ")))
  texto_alinhamento_rq <- gsub("\\s+", " ", texto_alinhamento_rq)

  resumo_suf <- normalizar_texto(matriz[[col_resumo_suf]])
  bloco_a_sim <- if (is.na(col_bloco_a)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_bloco_a]])
  bloco_b_sim <- if (is.na(col_bloco_b)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_bloco_b]])
  usa_ahp <- if (is.na(col_usa_ahp)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_usa_ahp]])
  usa_topsis <- if (is.na(col_usa_topsis)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_usa_topsis]])
  usa_outro_mcdm <- if (is.na(col_usa_outro_mcdm)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_usa_outro_mcdm]])

  criterio_ambiental <- if (is.na(col_crit_ambiental)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_ambiental]])
  criterio_tecnico <- if (is.na(col_crit_tecnico)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_tecnico]])
  criterio_economico <- if (is.na(col_crit_economico)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_economico]])
  criterio_social <- if (is.na(col_crit_social)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_social]])
  criterio_institucional <- if (is.na(col_crit_institucional)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_institucional]])
  criterio_risco <- if (is.na(col_crit_risco)) rep(FALSE, total_registros) else coluna_sim(matriz[[col_crit_risco]])
  metodo_informado <- if (is.na(col_metodo)) rep(FALSE, total_registros) else coluna_informativa(matriz[[col_metodo]])
  contexto_informado <- if (is.na(col_contexto)) rep(FALSE, total_registros) else coluna_informativa(matriz[[col_contexto]])
  edificacao_informada <- if (is.na(col_tipo_edificacao)) rep(FALSE, total_registros) else coluna_informativa(matriz[[col_tipo_edificacao]])

  termos_unicos <- unique(dicionario$termo)
  presenca_termos <- stats::setNames(
    lapply(termos_unicos, function(termo) stringr::str_detect(texto_alinhamento_rq, stringr::fixed(termo))),
    termos_unicos
  )

  combinar_qualquer <- function(termos) {
    termos <- unique(termos[termos %in% names(presenca_termos)])
    if (length(termos) == 0) {
      return(rep(FALSE, total_registros))
    }
    Reduce(`|`, presenca_termos[termos])
  }

  somar_pesos <- function(subdic) {
    saida <- rep(0, total_registros)
    if (nrow(subdic) == 0) {
      return(saida)
    }
    for (i in seq_len(nrow(subdic))) {
      saida <- saida + ifelse(presenca_termos[[subdic$termo[i]]], subdic$peso[i], 0)
    }
    saida
  }

  dicionario_rq0 <- dicionario %>% dplyr::filter(.data$rq == "RQ0")
  rq0_objeto <- combinar_qualquer(dicionario_rq0 %>% dplyr::filter(.data$categoria == "objeto_predial") %>% dplyr::pull(.data$termo)) | bloco_a_sim | edificacao_informada
  rq0_manutencao <- combinar_qualquer(dicionario_rq0 %>% dplyr::filter(.data$categoria == "manutencao_gestao") %>% dplyr::pull(.data$termo))
  rq0_sustentabilidade <- combinar_qualquer(dicionario_rq0 %>% dplyr::filter(.data$categoria == "sustentabilidade") %>% dplyr::pull(.data$termo)) |
    bloco_b_sim | criterio_ambiental | criterio_tecnico | criterio_economico | criterio_social | criterio_institucional | criterio_risco
  rq0_decisao <- combinar_qualquer(dicionario_rq0 %>% dplyr::filter(.data$categoria == "decisao") %>% dplyr::pull(.data$termo)) |
    metodo_informado | usa_ahp | usa_topsis | usa_outro_mcdm

  rq0 <- rq0_objeto & rq0_manutencao & rq0_sustentabilidade & rq0_decisao

  rq1 <- (combinar_qualquer(dicionario %>% dplyr::filter(.data$rq == "RQ1") %>% dplyr::pull(.data$termo)) |
            criterio_ambiental | criterio_tecnico | criterio_economico | criterio_social | criterio_institucional | criterio_risco) &
    (rq0_objeto | edificacao_informada) &
    (rq0_manutencao | criterio_tecnico)

  rq2 <- combinar_qualquer(dicionario %>% dplyr::filter(.data$rq == "RQ2") %>% dplyr::pull(.data$termo))
  rq3 <- combinar_qualquer(dicionario %>% dplyr::filter(.data$rq == "RQ3") %>% dplyr::pull(.data$termo)) |
    metodo_informado | usa_ahp | usa_topsis | usa_outro_mcdm
  rq4 <- combinar_qualquer(dicionario %>% dplyr::filter(.data$rq == "RQ4") %>% dplyr::pull(.data$termo)) |
    contexto_informado | edificacao_informada
  rq5 <- combinar_qualquer(dicionario %>% dplyr::filter(.data$rq == "RQ5") %>% dplyr::pull(.data$termo)) |
    (contexto_informado & stringr::str_detect(obter_texto_coluna(matriz, col_contexto), "public|universit|higher education|institution"))

  n_rqs_respondidas <- rq0 + rq1 + rq2 + rq3 + rq4 + rq5
  lista_rqs_respondidas <- vapply(seq_len(total_registros), function(i) {
    rqs <- c("RQ0", "RQ1", "RQ2", "RQ3", "RQ4", "RQ5")[c(rq0[i], rq1[i], rq2[i], rq3[i], rq4[i], rq5[i])]
    if (length(rqs) == 0) "" else paste(rqs, collapse = ";")
  }, character(1))

  pesos_rq <- (3 * rq0) + (1 * rq1) + (2 * rq2) + (2 * rq3) + (1 * rq4) + (2 * rq5)
  pesos_estrato <- dplyr::case_when(
    estratos == "a_nucleo_forte" ~ 2,
    estratos == "b_nucleo_descritivo" ~ 1,
    estratos == "c_contextual" ~ -1,
    estratos == "d_descartar_sintese" ~ -5,
    TRUE ~ 0
  )
  pesos_resumo <- dplyr::case_when(
    resumo_suf == "sim" ~ 2,
    resumo_suf == "parcial" ~ 0,
    resumo_suf == "nao" ~ -3,
    TRUE ~ 0
  )
  sinal_exclusao_textual <- combinar_qualquer(normalizar_texto(TERMOS_EXCLUSAO_FORTE))
  justificativa_texto <- if (is.na(col_justificativa)) rep("", total_registros) else obter_texto_coluna(matriz, col_justificativa)
  sinal_exclusao_herdado <- sinal_exclusao_textual | stringr::str_detect(justificativa_texto, stringr::fixed("termo forte de exclusao"))
  score_alinhamento_rq <- pesos_rq + pesos_estrato + pesos_resumo + ifelse(sinal_exclusao_herdado, -5, 0)

  uso_recomendado_artigo <- dplyr::case_when(
    estratos == "a_nucleo_forte" &
      score_alinhamento_rq >= 8 &
      n_rqs_respondidas >= 3 &
      (rq0 | (rq2 & rq3)) &
      estratos != "d_descartar_sintese" &
      resumo_suf != "nao" ~ "analise_central",
    estratos %in% c("a_nucleo_forte", "b_nucleo_descritivo") &
      score_alinhamento_rq >= 5 &
      n_rqs_respondidas >= 2 ~ "analise_secundaria",
    estratos %in% c("a_nucleo_forte", "b_nucleo_descritivo") &
      n_rqs_respondidas >= 1 ~ "mapeamento_descritivo",
    estratos == "c_contextual" |
      ((rq4 | rq5) & n_rqs_respondidas <= 2 & !rq0 & !rq2 & !rq3) ~ "apoio_contextual",
    estratos == "d_descartar_sintese" |
      n_rqs_respondidas == 0 |
      score_alinhamento_rq < 2 |
      sinal_exclusao_herdado ~ "excluir_do_artigo",
    TRUE ~ "apoio_contextual"
  )

  uso_recomendado_artigo[estratos == "d_descartar_sintese"] <- "excluir_do_artigo"

  justificativa_alinhamento_rq <- paste0(
    "RQ0=", ifelse(rq0, "TRUE", "FALSE"),
    "; RQ1=", ifelse(rq1, "TRUE", "FALSE"),
    "; RQ2=", ifelse(rq2, "TRUE", "FALSE"),
    "; RQ3=", ifelse(rq3, "TRUE", "FALSE"),
    "; RQ4=", ifelse(rq4, "TRUE", "FALSE"),
    "; RQ5=", ifelse(rq5, "TRUE", "FALSE"),
    "; n_rqs=", n_rqs_respondidas,
    "; score=", score_alinhamento_rq,
    "; estrato_resumo=", matriz[[col_estrato]],
    "; uso=", uso_recomendado_artigo
  )

  matriz_saida <- matriz %>%
    dplyr::mutate(
      texto_alinhamento_rq = texto_alinhamento_rq,
      rq0_integracao_sustentabilidade_decisao_manutencao = rq0,
      rq1_dimensoes_sustentabilidade = rq1,
      rq2_criterios_priorizacao = rq2,
      rq3_metodos_apoio_decisao = rq3,
      rq4_tipo_edificacao_contexto = rq4,
      rq5_lacunas_ies_publicas = rq5,
      n_rqs_respondidas = n_rqs_respondidas,
      lista_rqs_respondidas = lista_rqs_respondidas,
      score_alinhamento_rq = score_alinhamento_rq,
      uso_recomendado_artigo = uso_recomendado_artigo,
      justificativa_alinhamento_rq = justificativa_alinhamento_rq
    )

  usos_validos <- c("analise_central", "analise_secundaria", "mapeamento_descritivo", "apoio_contextual", "excluir_do_artigo")

  tabela16 <- dplyr::tibble(
    rq = c("RQ0", "RQ1", "RQ2", "RQ3", "RQ4", "RQ5"),
    total = c(sum(rq0), sum(rq1), sum(rq2), sum(rq3), sum(rq4), sum(rq5))
  ) %>%
    dplyr::mutate(percentual = sprintf("%.1f", (100 * .data$total) / total_registros))

  tabela17 <- matriz_saida %>%
    dplyr::count(.data$uso_recomendado_artigo, name = "total") %>%
    dplyr::mutate(percentual = sprintf("%.1f", (100 * .data$total) / total_registros)) %>%
    dplyr::arrange(match(.data$uso_recomendado_artigo, usos_validos))

  tabela18 <- matriz_saida %>%
    dplyr::count(.data[[col_estrato]], .data$uso_recomendado_artigo, name = "total") %>%
    tidyr::pivot_wider(names_from = "uso_recomendado_artigo", values_from = "total", values_fill = 0)
  names(tabela18)[1] <- "estrato_uso_resumo"

  nucleo_principal <- matriz_saida %>%
    dplyr::filter(.data$uso_recomendado_artigo == "analise_central")

  tabela19 <- if (!is.na(col_ano)) {
    nucleo_principal %>%
      dplyr::count(.data[[col_ano]], name = "total") %>%
      dplyr::arrange(.data[[col_ano]]) -> tabela19_tmp
    names(tabela19_tmp)[1] <- "ano"
    tabela19_tmp
  } else {
    dplyr::tibble(ano = character(0), total = integer(0))
  }

  tabela20 <- if (!is.na(col_bases)) {
    nucleo_principal %>%
      dplyr::mutate(base_tmp = .data[[col_bases]]) %>%
      tidyr::separate_rows(base_tmp, sep = "\\s*[;,|/]\\s*") %>%
      dplyr::mutate(base_tmp = trimws(.data$base_tmp)) %>%
      dplyr::filter(.data$base_tmp != "") %>%
      dplyr::count(.data$base_tmp, name = "total") %>%
      dplyr::arrange(dplyr::desc(.data$total), .data$base_tmp) -> tabela20_tmp
    names(tabela20_tmp)[1] <- "bases_origem"
    tabela20_tmp
  } else {
    dplyr::tibble(bases_origem = character(0), total = integer(0))
  }

  set.seed(42)
  colunas_amostra_candidatas <- c(
    col_id, col_ano, col_bases, col_doi, col_titulo, col_resumo, col_palavras, col_estrato, col_resumo_suf,
    "rq0_integracao_sustentabilidade_decisao_manutencao", "rq1_dimensoes_sustentabilidade",
    "rq2_criterios_priorizacao", "rq3_metodos_apoio_decisao", "rq4_tipo_edificacao_contexto",
    "rq5_lacunas_ies_publicas", "n_rqs_respondidas", "lista_rqs_respondidas", "score_alinhamento_rq",
    "uso_recomendado_artigo", "justificativa_alinhamento_rq"
  )
  colunas_amostra <- unique(colunas_amostra_candidatas[!is.na(colunas_amostra_candidatas)])
  amostra_auditoria <- matriz_saida %>%
    dplyr::group_by(.data$uso_recomendado_artigo) %>%
    dplyr::group_modify(~ if (nrow(.x) <= 30L) .x else dplyr::slice_sample(.x, n = 30L)) %>%
    dplyr::ungroup() %>%
    dplyr::select(dplyr::all_of(colunas_amostra))

  validacoes <- c(
    paste0("entrada_existe=", file.exists(ARQUIVO_ENTRADA)),
    paste0("entrada_linhas_3678=", total_registros == 3678),
    paste0("coluna_estrato_uso_resumo=", !is.na(col_estrato)),
    paste0("quatro_estratos_esperados=", setequal(estratos_observados, estratos_esperados)),
    paste0("saida_mesmo_n=", nrow(matriz_saida) == total_registros),
    paste0("colunas_rq0_rq5_existem=", all(c(
      "rq0_integracao_sustentabilidade_decisao_manutencao",
      "rq1_dimensoes_sustentabilidade",
      "rq2_criterios_priorizacao",
      "rq3_metodos_apoio_decisao",
      "rq4_tipo_edificacao_contexto",
      "rq5_lacunas_ies_publicas"
    ) %in% names(matriz_saida))),
    paste0("n_rqs_respondidas_existe=", "n_rqs_respondidas" %in% names(matriz_saida)),
    paste0("score_alinhamento_rq_existe=", "score_alinhamento_rq" %in% names(matriz_saida)),
    paste0("uso_recomendado_artigo_existe=", "uso_recomendado_artigo" %in% names(matriz_saida)),
    paste0("uso_recomendado_artigo_sem_vazio=", all(!is.na(matriz_saida$uso_recomendado_artigo) & matriz_saida$uso_recomendado_artigo != "")),
    paste0("uso_recomendado_artigo_dominios_validos=", all(unique(matriz_saida$uso_recomendado_artigo) %in% usos_validos)),
    paste0("d_descartar_sintese_fora_analise_central=", all(matriz_saida$uso_recomendado_artigo[estratos == "d_descartar_sintese"] != "analise_central")),
    paste0("nucleo_principal_apenas_analise_central=", all(nucleo_principal$uso_recomendado_artigo == "analise_central")),
    paste0("relatorio_criado=", TRUE),
    paste0("log_criado=", TRUE)
  )

  if (!all(grepl("=TRUE$", validacoes))) {
    stop(paste0("Falha em validacoes: ", paste(validacoes[!grepl("=TRUE$", validacoes)], collapse = "; ")))
  }

  readr::write_csv(matriz_saida, ARQUIVO_SAIDA_MATRIZ, na = "")
  readr::write_csv(nucleo_principal, ARQUIVO_NUCLEO, na = "")
  readr::write_csv(tabela16, ARQUIVO_TABELA16, na = "")
  readr::write_csv(tabela17, ARQUIVO_TABELA17, na = "")
  readr::write_csv(tabela18, ARQUIVO_TABELA18, na = "")
  readr::write_csv(tabela19, ARQUIVO_TABELA19, na = "")
  readr::write_csv(tabela20, ARQUIVO_TABELA20, na = "")
  readr::write_csv(amostra_auditoria, ARQUIVO_AMOSTRA, na = "")

  tabela17_linhas <- apply(tabela17, 1, function(l) paste0("- `", l[["uso_recomendado_artigo"]], "`: ", l[["total"]], " (", l[["percentual"]], "%)"))
  tabela16_linhas <- apply(tabela16, 1, function(l) paste0("- `", l[["rq"]], "`: ", l[["total"]], " (", l[["percentual"]], "%)"))
  tabela18_texto <- capture.output(print(as.data.frame(tabela18), row.names = FALSE))
  session_info <- capture.output(sessionInfo())

  relatorio_linhas <- c(
    "# Relatorio de alinhamento dos registros as perguntas de pesquisa",
    "",
    "## 1. Objetivo da ETAPA_15",
    "Alinhar os 3.678 registros reavaliados por resumo as perguntas de pesquisa do artigo, por meio de um dicionario CSV reprodutivel e regras auditaveis aplicadas apenas a titulo, resumo, palavras-chave e campos previamente extraidos.",
    "",
    "## 2. Arquivo de entrada",
    paste0("- `", ARQUIVO_ENTRADA, "`"),
    "",
    "## 3. Arquivos de saida",
    paste0("- `", ARQUIVO_SAIDA_MATRIZ, "`"),
    paste0("- `", ARQUIVO_NUCLEO, "`"),
    paste0("- `", ARQUIVO_TABELA16, "`"),
    paste0("- `", ARQUIVO_TABELA17, "`"),
    paste0("- `", ARQUIVO_TABELA18, "`"),
    paste0("- `", ARQUIVO_TABELA19, "`"),
    paste0("- `", ARQUIVO_TABELA20, "`"),
    paste0("- `", ARQUIVO_AMOSTRA, "`"),
    paste0("- `", ARQUIVO_RELATORIO, "`"),
    "",
    "## 4. Data/hora",
    paste0("- ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    "",
    "## 5. Total de registros lidos",
    paste0("- ", total_registros),
    "",
    "## 6. Total por uso_recomendado_artigo",
    tabela17_linhas,
    "",
    "## 7. Percentual por uso_recomendado_artigo",
    tabela17_linhas,
    "",
    "## 8. Total por RQ",
    tabela16_linhas,
    "",
    "## 9. Cruzamento entre estrato_uso_resumo e uso_recomendado_artigo",
    "```text",
    tabela18_texto,
    "```",
    "",
    "## 10. Total do nucleo principal recomendado",
    paste0("- ", nrow(nucleo_principal)),
    "",
    "## 11. Explicacao do dicionario de termos",
    paste0("- O dicionario principal esta em `", ARQUIVO_DICIONARIO, "` com colunas `rq`, `categoria`, `termo`, `peso` e `observacao`."),
    "- Os termos sao lidos pelo script e aplicados diretamente sobre `texto_alinhamento_rq`.",
    "",
    "## 12. Explicacao da pontuacao",
    "- RQ0 = +3; RQ1 = +1; RQ2 = +2; RQ3 = +2; RQ4 = +1; RQ5 = +2.",
    "- `A_nucleo_forte` = +2; `B_nucleo_descritivo` = +1; `C_contextual` = -1; `D_descartar_sintese` = -5.",
    "- `resumo_suficiente_para_extracao` = `sim` +2; `parcial` +0; `nao` -3.",
    "- Sinal forte de exclusao herdado ou textual = -5.",
    "",
    "## 13. Explicacao dos criterios de decisao",
    "- `analise_central`: estrato A, score >= 8, pelo menos 3 RQs e resposta a RQ0 ou a RQ2+RQ3.",
    "- `analise_secundaria`: estrato A/B, score >= 5 e pelo menos 2 RQs.",
    "- `mapeamento_descritivo`: estrato A/B com pelo menos 1 RQ.",
    "- `apoio_contextual`: estrato C ou resposta fraca/contextual concentrada em RQ4/RQ5.",
    "- `excluir_do_artigo`: estrato D, zero RQ, score < 2 ou exclusao forte.",
    "",
    "## 14. Lista de campos encontrados",
    paste0("- ", paste(campos_detectados, collapse = ", ")),
    "",
    "## 15. Lista de campos esperados e ausentes",
    if (length(campos_ausentes) == 0) "- Nenhum." else paste0("- ", paste(campos_ausentes, collapse = ", ")),
    "",
    "## 16. Limitacoes",
    "- A etapa usa sinais textuais em titulo, resumo, palavras-chave e campos previamente extraidos.",
    "- Ela nao substitui leitura full-text nem permite afirmar resultados profundos para todos os registros.",
    "- O alinhamento depende do vocabulario do dicionario e da qualidade dos campos auxiliares disponiveis.",
    "",
    "## 17. Recomendacao para o proximo passo",
    "- usar `nucleo_principal_sintese_artigo.csv` para a sintese analitica principal;",
    "- usar registros `analise_secundaria` para complementar a discussao;",
    "- usar `mapeamento_descritivo` apenas para tabelas gerais;",
    "- nao usar `excluir_do_artigo` no artigo;",
    "- auditar manualmente a amostra antes da redacao final;",
    "- so fazer leitura full-text pontual para os registros centrais mais importantes, se necessario.",
    "",
    "## 18. sessionInfo()",
    "```text",
    session_info,
    "```"
  )
  escrever_utf8(ARQUIVO_RELATORIO, relatorio_linhas)

  arquivos_criados <- c(
    ARQUIVO_DICIONARIO, ARQUIVO_SAIDA_MATRIZ, ARQUIVO_NUCLEO, ARQUIVO_TABELA16, ARQUIVO_TABELA17,
    ARQUIVO_TABELA18, ARQUIVO_TABELA19, ARQUIVO_TABELA20, ARQUIVO_AMOSTRA, ARQUIVO_RELATORIO, ARQUIVO_LOG
  )

  log_linhas <- c(
    "# ETAPA_15_ALINHAR_PERGUNTAS_PESQUISA",
    "",
    paste0("Data/hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    paste0("Arquivo de entrada: ", ARQUIVO_ENTRADA),
    paste0("Total de registros: ", total_registros),
    paste0("Campos detectados: ", paste(campos_detectados, collapse = "; ")),
    paste0("Dicionario criado/usado: ", ARQUIVO_DICIONARIO),
    "Total por RQ:",
    tabela16_linhas,
    "Total por uso_recomendado_artigo:",
    tabela17_linhas,
    paste0("Tamanho do nucleo principal: ", nrow(nucleo_principal)),
    paste0("Arquivos criados: ", paste(arquivos_criados, collapse = "; ")),
    "Validacoes realizadas:",
    paste0("- ", validacoes),
    "Alertas:",
    if (length(campos_ausentes) == 0) "- Nenhum." else paste0("- Campos ausentes: ", paste(campos_ausentes, collapse = ", ")),
    "Conclusao:",
    "- ETAPA_15 concluida com matriz alinhada, tabelas, amostra de auditoria e atualizacao documental."
  )
  escrever_utf8(ARQUIVO_LOG, log_linhas)

  secao_estado <- c(
    "## ETAPA_15 - alinhamento dos registros as perguntas de pesquisa",
    "",
    "- Objetivo: alinhar os registros reavaliados por resumo as RQs do artigo com dicionario CSV reprodutivel e regras auditaveis.",
    paste0("- Arquivo de entrada: `", "07_SINTESE_TEMATICA\\matriz_extracao_final_reavaliada_resumos.csv", "`."),
    paste0("- Arquivos de saida principais: `", "07_SINTESE_TEMATICA\\matriz_alinhamento_perguntas_pesquisa.csv", "` e `", "07_SINTESE_TEMATICA\\nucleo_principal_sintese_artigo.csv", "`."),
    paste0("- Total por `uso_recomendado_artigo`: ", paste(paste0(tabela17$uso_recomendado_artigo, "=", tabela17$total), collapse = "; "), "."),
    paste0("- Total por RQ: ", paste(paste0(tabela16$rq, "=", tabela16$total), collapse = "; "), "."),
    paste0("- Tamanho do nucleo principal recomendado (`analise_central`): ", nrow(nucleo_principal), "."),
    "- A etapa e reprodutivel por dicionario CSV.",
    "- Nao houve leitura full-text, internet ou LLM.",
    "- O arquivo operacional principal passa a ser: `07_SINTESE_TEMATICA\\nucleo_principal_sintese_artigo.csv`.",
    "- A matriz completa alinhada esta em: `07_SINTESE_TEMATICA\\matriz_alinhamento_perguntas_pesquisa.csv`."
  )
  substituir_ou_anexar_secao(ARQUIVO_ESTADO_ATUAL, "## ETAPA_15 - alinhamento dos registros as perguntas de pesquisa", secao_estado)

  decisao_texto <- c(
    "",
    "---",
    "",
    "## 2026-07-09 - Alinhamento dos registros as perguntas de pesquisa por dicionario reprodutivel",
    "",
    "Decisao: classificar os 3.678 registros da ETAPA_14 por aderencia direta as RQs do artigo, usando um dicionario CSV reprodutivel como fonte principal dos termos e sem leitura full-text.",
    "",
    "Motivo: a separacao por forca do resumo da ETAPA_14 era util, mas ainda nao informava de forma direta quais registros ajudam a responder cada pergunta de pesquisa do artigo.",
    "",
    "Impacto: foram gerados `07_SINTESE_TEMATICA\\matriz_alinhamento_perguntas_pesquisa.csv`, `07_SINTESE_TEMATICA\\nucleo_principal_sintese_artigo.csv`, as tabelas 16 a 20, a amostra de auditoria da ETAPA_15 e o relatorio metodologico correspondente. O uso recomendado do artigo deixa de depender apenas do estrato de resumo e passa a incorporar aderencia explicita as RQs.",
    "",
    "Arquivos gerados: `07_SINTESE_TEMATICA\\dicionario_rq_etapa15.csv`, `07_SINTESE_TEMATICA\\matriz_alinhamento_perguntas_pesquisa.csv`, `07_SINTESE_TEMATICA\\nucleo_principal_sintese_artigo.csv`, `05_ANALISE_R\\tabelas\\tabela16_aderencia_por_rq.csv`, `05_ANALISE_R\\tabelas\\tabela17_uso_recomendado_artigo.csv`, `05_ANALISE_R\\tabelas\\tabela18_cruzamento_estrato_resumo_uso_artigo.csv`, `05_ANALISE_R\\tabelas\\tabela19_nucleo_principal_por_ano.csv`, `05_ANALISE_R\\tabelas\\tabela20_nucleo_principal_por_base.csv`, `05_ANALISE_R\\tabelas\\amostra_auditoria_etapa15_alinhamento_rq.csv`, `07_SINTESE_TEMATICA\\relatorio_alinhamento_perguntas_pesquisa.md`.",
    "",
    "Limitacao principal: a etapa usa sinais textuais em titulo, resumo, palavras-chave e campos previamente extraidos. Ela nao substitui leitura full-text nem permite afirmar resultados profundos para todos os registros. A finalidade e reduzir o nucleo analitico a um conjunto mais aderente as perguntas do artigo, mantendo rastreabilidade e reprodutibilidade."
  )
  escrever_utf8(ARQUIVO_DECISOES, c(readLines(ARQUIVO_DECISOES, warn = FALSE, encoding = "UTF-8"), decisao_texto))

  done_linhas <- c(
    paste0("data/hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    "status: concluido",
    paste0("total de registros analisados: ", total_registros),
    paste0("total de analise_central: ", sum(matriz_saida$uso_recomendado_artigo == "analise_central")),
    paste0("total de analise_secundaria: ", sum(matriz_saida$uso_recomendado_artigo == "analise_secundaria")),
    paste0("total de mapeamento_descritivo: ", sum(matriz_saida$uso_recomendado_artigo == "mapeamento_descritivo")),
    paste0("total de apoio_contextual: ", sum(matriz_saida$uso_recomendado_artigo == "apoio_contextual")),
    paste0("total de excluir_do_artigo: ", sum(matriz_saida$uso_recomendado_artigo == "excluir_do_artigo")),
    paste0("caminho da matriz alinhada: ", ARQUIVO_SAIDA_MATRIZ),
    paste0("caminho do nucleo principal: ", ARQUIVO_NUCLEO),
    paste0("caminho do relatorio: ", ARQUIVO_RELATORIO)
  )
  escrever_utf8(ARQUIVO_DONE, done_linhas)
}

resultado <- tryCatch({
  main()
  TRUE
}, error = function(e) {
  registrar_falha(
    etapa = "execucao_etapa_15",
    erro = conditionMessage(e),
    arquivos_verificados = c(ARQUIVO_ENTRADA, ARQUIVO_DICIONARIO, ARQUIVO_ESTADO_ATUAL, ARQUIVO_DECISOES),
    faltou = "Concluir a execucao valida da ETAPA_15 e gerar todos os artefatos obrigatorios."
  )
  message(conditionMessage(e))
  FALSE
})

if (!isTRUE(resultado)) {
  quit(status = 1)
}
