suppressPackageStartupMessages({
  library(readr)
  library(dplyr)
})

options(readr.show_col_types = FALSE)

PROJETO_DIR <- Sys.getenv("PROJETO_DIR", unset = ".")
ARQUIVO_ENTRADA <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "matriz_extracao_final.csv")
ARQUIVO_SAIDA_MATRIZ <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "matriz_extracao_final_reavaliada_resumos.csv")
ARQUIVO_RELATORIO <- file.path(PROJETO_DIR, "07_SINTESE_TEMATICA", "relatorio_reavaliacao_criteriosa_resumos.md")
ARQUIVO_TABELA14 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela14_reavaliacao_resumos_por_estrato.csv")
ARQUIVO_TABELA15 <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "tabela15_sinais_reavaliacao_resumos.csv")
ARQUIVO_AMOSTRA <- file.path(PROJETO_DIR, "05_ANALISE_R", "tabelas", "amostra_auditoria_reavaliacao_resumos.csv")
ARQUIVO_LOG <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "LOGS", "ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.md")
ARQUIVO_DONE <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "DONE", "ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.done")
ARQUIVO_FAIL <- file.path(PROJETO_DIR, "00_CONTROLE", "ROTINAS", "LOGS", "ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.fail.md")
ARQUIVO_ESTADO_ATUAL <- file.path(PROJETO_DIR, "00_CONTROLE", "ESTADO_ATUAL.md")
ARQUIVO_DECISOES <- file.path(PROJETO_DIR, "00_CONTROLE", "DECISOES_METODOLOGICAS.md")

VALORES_AUSENCIA <- c(
  "", "na", "n/a", "nao", "não", "nao_informado_no_resumo", "nao_identificavel_pelo_resumo",
  "nao_classificavel_pelo_resumo", "pendente", "pendente_leitura_completa",
  "nao_verificavel_pelo_resumo", "a_definir_na_sintese", "nao_informado", "not available"
)

TERMOS_OBJETO <- c(
  "building", "buildings", "built environment", "facility", "facilities", "school building",
  "university building", "campus", "public building", "hospital building", "healthcare building",
  "educational building", "student housing", "residential building", "office building",
  "heritage building", "building stock", "building portfolio", "building asset", "built asset",
  "public facilities", "institutional building", "government building"
)

TERMOS_MANUTENCAO <- c(
  "maintenance", "maintenance management", "building maintenance", "preventive maintenance",
  "corrective maintenance", "deferred maintenance", "maintenance planning",
  "maintenance prioritization", "maintenance priority", "maintenance strategy",
  "operation and maintenance", "operations and maintenance", "building operation",
  "facility management", "facilities management", "asset management", "condition assessment",
  "condition-based maintenance", "post occupancy", "post-occupancy", "retrofit", "retrofitting",
  "renovation", "recommissioning", "re-commissioning", "building energy management",
  "operation stage", "operational stage"
)

TERMOS_SUSTENTABILIDADE <- c(
  "sustainability", "sustainable", "environmental", "energy efficiency", "energy performance",
  "energy consumption", "carbon", "decarbon", "low carbon", "net zero", "net-zero",
  "greenhouse gas", "climate", "circular", "life cycle", "lifecycle",
  "indoor environmental quality", "thermal comfort", "occupant comfort", "cost", "costs",
  "economic", "risk", "resilience", "safety", "public", "institutional", "social",
  "governance", "performance", "efficiency"
)

TERMOS_METODO <- c(
  "case study", "survey", "interview", "questionnaire", "simulation", "model", "modelling",
  "modeling", "framework", "bibliometric", "systematic review", "literature review", "review",
  "data", "sensor", "iot", "bim", "digital twin", "machine learning", "artificial intelligence",
  "text mining", "work order", "maintenance records", "results show", "findings", "this study",
  "we found", "analysis", "evaluation", "assessment", "prioritization", "decision-making",
  "multicriteria", "multi-criteria", "ahp", "topsis", "mcdm", "mcda"
)

TERMOS_EXCLUSAO <- c(
  "oil and gas", "gas pipeline", "natural gas pipeline", "pipeline", "railway", "track maintenance",
  "road", "bridge", "inland waterway", "port", "wind energy", "wind farm", "offshore renewable",
  "power transformer", "substation equipment", "medical device", "maternal care", "ob/gyn",
  "tourism", "land-use efficiency", "wastewater", "water services", "fecal sludge",
  "battery energy storage system in distribution network", "transmission line", "crude oil",
  "aircraft", "software obsolescence", "nuclear facilities maintenance", "tunnel maintenance",
  "metro tunnel", "power plant", "steam generator", "distribution network",
  "photovoltaic system configuration", "urban land use", "slope recovery"
)

normalizar_nome <- function(x) {
  x <- iconv(x, from = "", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("[^a-z0-9]+", "_", x)
  gsub("^_|_$", "", x)
}

normalizar_texto <- function(x) {
  x <- ifelse(is.na(x), "", x)
  x <- iconv(x, from = "", to = "ASCII//TRANSLIT")
  x <- tolower(x)
  x <- gsub("\\s+", " ", x)
  trimws(x)
}

detectar_coluna <- function(nomes, candidatos, obrigatoria = TRUE) {
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
  x_norm <- normalizar_texto(as.character(x))
  !(is.na(x) | x_norm %in% VALORES_AUSENCIA)
}

termo_presente <- function(texto, termos) {
  if (!nzchar(texto)) {
    return(FALSE)
  }
  any(vapply(termos, function(termo) grepl(termo, texto, fixed = TRUE), logical(1)))
}

formatar_pct <- function(n, total) {
  if (total == 0) {
    return("0.0%")
  }
  sprintf("%.1f%%", 100 * n / total)
}

escrever_utf8 <- function(caminho, linhas) {
  writeLines(enc2utf8(linhas), caminho, useBytes = TRUE)
}

substituir_ou_anexar_secao <- function(caminho, titulo_secao, conteudo_secao) {
  texto <- readChar(caminho, nchars = file.info(caminho)$size, useBytes = TRUE)
  linhas <- strsplit(texto, "\r?\n", perl = TRUE)[[1]]
  inicio <- grep(paste0("^", gsub("([\\^\\$\\.\\|\\(\\)\\[\\]\\*\\+\\?\\\\])", "\\\\\\1", titulo_secao), "$"), linhas)

  if (length(inicio) == 0) {
    novo <- c(linhas, "", conteudo_secao)
    escrever_utf8(caminho, novo)
    return(invisible(NULL))
  }

  inicio <- inicio[1]
  resto <- if (inicio < length(linhas)) linhas[(inicio + 1):length(linhas)] else character(0)
  prox <- grep("^## ", resto)
  fim <- if (length(prox) == 0) length(linhas) else inicio + prox[1] - 1
  novo <- c(linhas[seq_len(inicio - 1)], conteudo_secao, if (fim < length(linhas)) linhas[(fim + 1):length(linhas)] else character(0))
  escrever_utf8(caminho, novo)
}

registrar_falha <- function(mensagem) {
  dir.create(dirname(ARQUIVO_FAIL), recursive = TRUE, showWarnings = FALSE)
  linhas <- c(
    "# ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.fail",
    "",
    paste0("Data/hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    paste0("Causa: ", mensagem)
  )
  escrever_utf8(ARQUIVO_FAIL, linhas)
}

main <- function() {
  dir.create(dirname(ARQUIVO_TABELA14), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(ARQUIVO_LOG), recursive = TRUE, showWarnings = FALSE)
  dir.create(dirname(ARQUIVO_DONE), recursive = TRUE, showWarnings = FALSE)

  if (!file.exists(ARQUIVO_ENTRADA)) {
    stop(paste0("Arquivo de entrada inexistente: ", ARQUIVO_ENTRADA))
  }

  matriz <- readr::read_csv(
    ARQUIVO_ENTRADA,
    locale = readr::locale(encoding = "UTF-8"),
    progress = FALSE
  )

  nomes_colunas <- names(matriz)
  total_registros <- nrow(matriz)

  col_titulo <- detectar_coluna(nomes_colunas, c("titulo", "title"))
  col_resumo <- detectar_coluna(nomes_colunas, c("resumo", "abstract"))
  col_palavras <- detectar_coluna(nomes_colunas, c("palavras_chave", "keywords", "author_keywords", "index_keywords"), obrigatoria = FALSE)

  campos_esperados <- c(
    "tipo_aplicacao", "dados_utilizados", "resultado_principal", "lacuna_identificada",
    "resumo_suficiente_para_extracao", "criterios_ambientais", "criterios_tecnicos_operacionais",
    "criterios_economicos", "criterios_sociais", "criterios_institucionais", "criterios_risco",
    "metodo_decisao", "contexto_publico_universitario", "tipo_edificacao", "eixo_tematico_preliminar"
  )

  nomes_norm <- normalizar_nome(nomes_colunas)
  campos_detectados <- campos_esperados[normalizar_nome(campos_esperados) %in% nomes_norm]
  campos_ausentes <- setdiff(campos_esperados, campos_detectados)

  buscar_coluna_opcional <- function(nome) {
    idx <- match(normalizar_nome(nome), nomes_norm)
    if (is.na(idx)) NA_character_ else nomes_colunas[idx]
  }

  col_tipo_aplicacao <- buscar_coluna_opcional("tipo_aplicacao")
  col_dados <- buscar_coluna_opcional("dados_utilizados")
  col_resultado <- buscar_coluna_opcional("resultado_principal")
  col_lacuna <- buscar_coluna_opcional("lacuna_identificada")
  col_resumo_suf <- buscar_coluna_opcional("resumo_suficiente_para_extracao")
  col_criterios_ambientais <- buscar_coluna_opcional("criterios_ambientais")
  col_criterios_tecnicos <- buscar_coluna_opcional("criterios_tecnicos_operacionais")
  col_criterios_economicos <- buscar_coluna_opcional("criterios_economicos")
  col_criterios_sociais <- buscar_coluna_opcional("criterios_sociais")
  col_criterios_institucionais <- buscar_coluna_opcional("criterios_institucionais")
  col_criterios_risco <- buscar_coluna_opcional("criterios_risco")
  col_metodo_decisao <- buscar_coluna_opcional("metodo_decisao")
  col_tipo_edificacao <- buscar_coluna_opcional("tipo_edificacao")
  col_eixo <- buscar_coluna_opcional("eixo_tematico_preliminar")
  col_bloco_a <- buscar_coluna_opcional("bloco_a_presente")
  col_bloco_b <- buscar_coluna_opcional("bloco_b_presente")

  obter_texto <- function(coluna) {
    if (is.na(coluna)) rep("", total_registros) else normalizar_texto(as.character(matriz[[coluna]]))
  }

  titulo <- obter_texto(col_titulo)
  resumo <- obter_texto(col_resumo)
  palavras <- obter_texto(col_palavras)
  texto_completo <- trimws(paste(titulo, resumo, palavras))

  resumo_suf <- if (is.na(col_resumo_suf)) rep("nao_informado", total_registros) else normalizar_texto(as.character(matriz[[col_resumo_suf]]))

  criterio_sim <- function(coluna) {
    if (is.na(coluna)) {
      rep(FALSE, total_registros)
    } else {
      normalizar_texto(as.character(matriz[[coluna]])) == "sim"
    }
  }

  informativo <- function(coluna) {
    if (is.na(coluna)) {
      rep(FALSE, total_registros)
    } else {
      tem_informacao(matriz[[coluna]])
    }
  }

  bloco_a_sim <- if (is.na(col_bloco_a)) rep(FALSE, total_registros) else normalizar_texto(as.character(matriz[[col_bloco_a]])) == "sim"
  bloco_b_sim <- if (is.na(col_bloco_b)) rep(FALSE, total_registros) else normalizar_texto(as.character(matriz[[col_bloco_b]])) == "sim"

  criterio_ambiental <- criterio_sim(col_criterios_ambientais)
  criterio_tecnico <- criterio_sim(col_criterios_tecnicos)
  criterio_economico <- criterio_sim(col_criterios_economicos)
  criterio_social <- criterio_sim(col_criterios_sociais)
  criterio_institucional <- criterio_sim(col_criterios_institucionais)
  criterio_risco <- criterio_sim(col_criterios_risco)

  tipo_aplicacao_info <- informativo(col_tipo_aplicacao)
  dados_info <- informativo(col_dados)
  resultado_info <- informativo(col_resultado)
  lacuna_info <- informativo(col_lacuna)
  metodo_decisao_info <- informativo(col_metodo_decisao)
  tipo_edificacao_info <- informativo(col_tipo_edificacao)
  eixo_info <- informativo(col_eixo)

  objeto_texto <- vapply(texto_completo, termo_presente, logical(1), termos = TERMOS_OBJETO)
  manutencao_texto <- vapply(texto_completo, termo_presente, logical(1), termos = TERMOS_MANUTENCAO)
  sustentabilidade_texto <- vapply(texto_completo, termo_presente, logical(1), termos = TERMOS_SUSTENTABILIDADE)
  metodo_texto <- vapply(texto_completo, termo_presente, logical(1), termos = TERMOS_METODO)
  exclusao_forte <- vapply(texto_completo, termo_presente, logical(1), termos = TERMOS_EXCLUSAO)

  objeto_predial <- objeto_texto | tipo_edificacao_info | bloco_a_sim
  manutencao_gestao <- manutencao_texto
  sustentabilidade <- sustentabilidade_texto | bloco_b_sim | criterio_ambiental | criterio_tecnico |
    criterio_economico | criterio_social | criterio_institucional | criterio_risco
  metodo_dado_resultado <- metodo_texto | tipo_aplicacao_info | dados_info | resultado_info |
    lacuna_info | metodo_decisao_info | eixo_info

  pontuacao <- integer(total_registros)
  pontuacao <- pontuacao + ifelse(objeto_predial, 2L, 0L)
  pontuacao <- pontuacao + ifelse(manutencao_gestao, 2L, 0L)
  pontuacao <- pontuacao + ifelse(sustentabilidade, 2L, 0L)
  pontuacao <- pontuacao + ifelse(metodo_dado_resultado, 1L, 0L)
  pontuacao <- pontuacao + ifelse(tipo_aplicacao_info, 1L, 0L)
  pontuacao <- pontuacao + ifelse(dados_info, 1L, 0L)
  pontuacao <- pontuacao + ifelse(resultado_info, 1L, 0L)
  pontuacao <- pontuacao + ifelse(lacuna_info, 1L, 0L)
  pontuacao <- pontuacao - ifelse(exclusao_forte, 4L, 0L)

  resumo_sim <- resumo_suf == "sim"
  resumo_parcial <- resumo_suf == "parcial"

  estrato <- ifelse(
    objeto_predial & manutencao_gestao & sustentabilidade & metodo_dado_resultado &
      !exclusao_forte & resumo_sim & pontuacao >= 7,
    "A_nucleo_forte",
    ifelse(
      objeto_predial & manutencao_gestao & sustentabilidade &
        !exclusao_forte & (resumo_sim | resumo_parcial) & pontuacao >= 5,
      "B_nucleo_descritivo",
      ifelse(
        !exclusao_forte & objeto_predial & (manutencao_gestao | sustentabilidade) & pontuacao >= 3,
        "C_contextual",
        "D_descartar_sintese"
      )
    )
  )

  entra_sintese_forte <- estrato == "A_nucleo_forte"
  entra_mapeamento <- estrato %in% c("A_nucleo_forte", "B_nucleo_descritivo")

  justificativa <- paste0(
    "objeto_predial=", objeto_predial,
    "; manutencao_gestao=", manutencao_gestao,
    "; sustentabilidade=", sustentabilidade,
    "; metodo_dado_resultado=", metodo_dado_resultado,
    "; exclusao_forte=", exclusao_forte,
    "; resumo_suficiente=", resumo_suf,
    "; pontos=", pontuacao
  )

  matriz_saida <- matriz %>%
    mutate(
      estrato_uso_resumo = estrato,
      entra_sintese_analitica_forte = entra_sintese_forte,
      entra_mapeamento_descritivo = entra_mapeamento,
      justificativa_reavaliacao_resumo = justificativa
    )

  tabela14 <- matriz_saida %>%
    count(estrato_uso_resumo, name = "n_registros") %>%
    mutate(
      percentual = round(100 * n_registros / sum(n_registros), 1),
      entra_sintese_analitica_forte_n = vapply(
        estrato_uso_resumo,
        function(x) sum(matriz_saida$estrato_uso_resumo == x & matriz_saida$entra_sintese_analitica_forte),
        numeric(1)
      ),
      entra_mapeamento_descritivo_n = vapply(
        estrato_uso_resumo,
        function(x) sum(matriz_saida$estrato_uso_resumo == x & matriz_saida$entra_mapeamento_descritivo),
        numeric(1)
      )
    ) %>%
    arrange(match(estrato_uso_resumo, c("A_nucleo_forte", "B_nucleo_descritivo", "C_contextual", "D_descartar_sintese")))

  tabela15 <- tibble::tibble(
    sinal = c(
      "objeto_predial", "manutencao_gestao", "sustentabilidade",
      "metodo_dado_resultado", "exclusao_forte", "resumo_suficiente_sim",
      "resumo_suficiente_parcial", "entra_sintese_analitica_forte", "entra_mapeamento_descritivo"
    ),
    n = c(
      sum(objeto_predial), sum(manutencao_gestao), sum(sustentabilidade),
      sum(metodo_dado_resultado), sum(exclusao_forte), sum(resumo_sim),
      sum(resumo_parcial), sum(entra_sintese_forte), sum(entra_mapeamento)
    )
  ) %>%
    mutate(percentual = round(100 * n / total_registros, 1))

  set.seed(42)
  colunas_amostra_desejadas <- c(
    "id_unico", "ano", "bases_origem", "doi", col_titulo, col_resumo, col_palavras,
    col_tipo_aplicacao, col_dados, col_resultado, col_lacuna, col_resumo_suf,
    "estrato_uso_resumo", "entra_sintese_analitica_forte", "entra_mapeamento_descritivo",
    "justificativa_reavaliacao_resumo"
  )
  colunas_amostra <- unique(colunas_amostra_desejadas[!is.na(colunas_amostra_desejadas) & colunas_amostra_desejadas %in% names(matriz_saida)])

  amostra <- matriz_saida %>%
    group_by(estrato_uso_resumo) %>%
    group_modify(~ dplyr::slice_sample(.x, n = min(30, nrow(.x)))) %>%
    ungroup() %>%
    select(all_of(colunas_amostra))

  readr::write_csv(matriz_saida, ARQUIVO_SAIDA_MATRIZ, na = "")
  readr::write_csv(tabela14, ARQUIVO_TABELA14, na = "")
  readr::write_csv(tabela15, ARQUIVO_TABELA15, na = "")
  readr::write_csv(amostra, ARQUIVO_AMOSTRA, na = "")

  totais_por_estrato <- setNames(tabela14$n_registros, tabela14$estrato_uso_resumo)
  total_a <- unname(totais_por_estrato["A_nucleo_forte"])
  total_b <- unname(totais_por_estrato["B_nucleo_descritivo"])
  total_c <- unname(totais_por_estrato["C_contextual"])
  total_d <- unname(totais_por_estrato["D_descartar_sintese"])

  total_a[is.na(total_a)] <- 0
  total_b[is.na(total_b)] <- 0
  total_c[is.na(total_c)] <- 0
  total_d[is.na(total_d)] <- 0

  linhas_relatorio <- c(
    "# Relatorio de reavaliacao criteriosa dos resumos",
    "",
    "## 1. Objetivo da etapa",
    "Criar uma camada intermediaria, auditavel e reprodutivel de uso do nucleo analitico revisado, separando os 3.678 registros por forca do resumo sem leitura full-text e sem uso de LLM.",
    "",
    "## 2. Arquivo de entrada",
    paste0("- `", ARQUIVO_ENTRADA, "`"),
    "",
    "## 3. Arquivos de saida",
    paste0("- `", ARQUIVO_SAIDA_MATRIZ, "`"),
    paste0("- `", ARQUIVO_RELATORIO, "`"),
    paste0("- `", ARQUIVO_TABELA14, "`"),
    paste0("- `", ARQUIVO_TABELA15, "`"),
    paste0("- `", ARQUIVO_AMOSTRA, "`"),
    paste0("- `", ARQUIVO_LOG, "`"),
    "",
    "## 4. Data/hora",
    paste0("- ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    "",
    "## 5. Total de registros lidos",
    paste0("- ", total_registros),
    "",
    "## 6. Total por estrato",
    paste0("- `A_nucleo_forte`: ", total_a),
    paste0("- `B_nucleo_descritivo`: ", total_b),
    paste0("- `C_contextual`: ", total_c),
    paste0("- `D_descartar_sintese`: ", total_d),
    "",
    "## 7. Percentual por estrato",
    paste0("- `A_nucleo_forte`: ", formatar_pct(total_a, total_registros)),
    paste0("- `B_nucleo_descritivo`: ", formatar_pct(total_b, total_registros)),
    paste0("- `C_contextual`: ", formatar_pct(total_c, total_registros)),
    paste0("- `D_descartar_sintese`: ", formatar_pct(total_d, total_registros)),
    "",
    "## 8. Total que entra na sintese analitica forte",
    paste0("- ", sum(entra_sintese_forte)),
    "",
    "## 9. Total que entra no mapeamento descritivo",
    paste0("- ", sum(entra_mapeamento)),
    "",
    "## 10. Total descartado da sintese",
    paste0("- ", total_d),
    "",
    "## 11. Lista dos campos encontrados e usados",
    paste0("- Coluna de titulo: `", col_titulo, "`"),
    paste0("- Coluna de resumo: `", col_resumo, "`"),
    paste0("- Coluna de palavras-chave: `", ifelse(is.na(col_palavras), "nao encontrada", col_palavras), "`"),
    paste0("- Campos auxiliares encontrados: ", ifelse(length(campos_detectados) == 0, "nenhum", paste(paste0("`", campos_detectados, "`"), collapse = ", "))),
    "",
    "## 12. Lista dos campos esperados que nao foram encontrados",
    paste0("- ", ifelse(length(campos_ausentes) == 0, "Nenhum campo ausente.", paste(paste0("`", campos_ausentes, "`"), collapse = ", "))),
    "",
    "## 13. Explicacao das regras",
    "- `A_nucleo_forte`: exige objeto predial, manutencao/gestao, sustentabilidade/desempenho, evidencia analitica, ausencia de exclusao forte, `resumo_suficiente_para_extracao = sim` e pontuacao >= 7.",
    "- `B_nucleo_descritivo`: exige objeto predial, manutencao/gestao, sustentabilidade/desempenho, ausencia de exclusao forte, `resumo_suficiente_para_extracao = sim/parcial` e pontuacao >= 5.",
    "- `C_contextual`: exige objeto predial e pelo menos manutencao/gestao ou sustentabilidade, sem cumprir os criterios de A ou B, e pontuacao >= 3.",
    "- `D_descartar_sintese`: agrega exclusao forte, falta de objeto predial, falta de manutencao/gestao, falta de sustentabilidade/desempenho ou evidencia insuficiente.",
    "",
    "## 14. Explicacao da pontuacao",
    "- objeto predial = +2",
    "- manutencao/gestao/operacao/facility management/retrofit/condition assessment = +2",
    "- sustentabilidade/desempenho/energia/custo/risco/conforto/institucional = +2",
    "- metodo/dado/resultado/lacuna = +1",
    "- tipo de aplicacao informativo = +1",
    "- dados utilizados informativos = +1",
    "- resultado principal informativo = +1",
    "- lacuna identificada informativa = +1",
    "- termo forte de exclusao = -4",
    "",
    "## 15. Limitacoes",
    "- A etapa nao substitui leitura full-text.",
    "- A ausencia de informacao no resumo nao foi tratada como evidencia positiva.",
    "- Os sinais dependem de titulo, resumo, palavras-chave e campos ja existentes na matriz final.",
    "- Campos auxiliares ausentes nao impediram a execucao, mas reduziram a capacidade de classificacao fina.",
    "",
    "## 16. Recomendacao de uso no artigo",
    "- usar `A_nucleo_forte` para a sintese analitica principal;",
    "- usar `A_nucleo_forte + B_nucleo_descritivo` para tabelas e estatisticas descritivas;",
    "- usar `C_contextual` apenas como apoio, se necessario;",
    "- excluir `D_descartar_sintese` da sintese analitica;",
    "- deixar claro no artigo que esta etapa usa titulo, resumo e palavras-chave, sem leitura full-text."
  )
  escrever_utf8(ARQUIVO_RELATORIO, linhas_relatorio)

  alertas <- character(0)
  if (any(is.na(col_palavras))) {
    alertas <- c(alertas, "Coluna de palavras-chave nao encontrada; classificacao baseada em titulo e resumo.")
  }
  if (length(campos_ausentes) > 0) {
    alertas <- c(alertas, paste0("Campos auxiliares ausentes: ", paste(campos_ausentes, collapse = ", ")))
  }

  linhas_log <- c(
    "# LOG - ETAPA_14: reavaliar resumos criterioso",
    "",
    paste0("Data/hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    paste0("Arquivo de entrada: `", ARQUIVO_ENTRADA, "`"),
    paste0("Total de registros: ", total_registros),
    paste0("Coluna de titulo detectada: `", col_titulo, "`"),
    paste0("Coluna de resumo detectada: `", col_resumo, "`"),
    paste0("Coluna de palavras-chave detectada: `", ifelse(is.na(col_palavras), "nao encontrada", col_palavras), "`"),
    paste0("Campos auxiliares encontrados: ", ifelse(length(campos_detectados) == 0, "nenhum", paste(campos_detectados, collapse = ", "))),
    paste0("Campos auxiliares ausentes: ", ifelse(length(campos_ausentes) == 0, "nenhum", paste(campos_ausentes, collapse = ", "))),
    "",
    "## Total por estrato",
    paste0("- A_nucleo_forte: ", total_a),
    paste0("- B_nucleo_descritivo: ", total_b),
    paste0("- C_contextual: ", total_c),
    paste0("- D_descartar_sintese: ", total_d),
    "",
    "## Arquivos gerados",
    paste0("- `", ARQUIVO_SAIDA_MATRIZ, "`"),
    paste0("- `", ARQUIVO_RELATORIO, "`"),
    paste0("- `", ARQUIVO_TABELA14, "`"),
    paste0("- `", ARQUIVO_TABELA15, "`"),
    paste0("- `", ARQUIVO_AMOSTRA, "`"),
    "",
    "## Alertas",
    if (length(alertas) == 0) "- nenhum" else paste0("- ", alertas),
    "",
    "## Conclusao",
    "Etapa concluida com reavaliacao conservadora, auditavel e reprodutivel do uso dos resumos."
  )
  escrever_utf8(ARQUIVO_LOG, linhas_log)

  secao_estado <- c(
    "## ETAPA_14 - reavaliacao criteriosa dos resumos",
    "",
    "Etapa criada para evitar leitura full-text massiva de 3.678 artigos. A reavaliacao usa apenas titulo, resumo, palavras-chave e campos ja preenchidos na matriz final. Nao usa LLM. Nao usa texto completo. Gera quatro estratos de uso do nucleo:",
    "",
    paste0("- `A_nucleo_forte`: ", total_a, " (", formatar_pct(total_a, total_registros), ")"),
    paste0("- `B_nucleo_descritivo`: ", total_b, " (", formatar_pct(total_b, total_registros), ")"),
    paste0("- `C_contextual`: ", total_c, " (", formatar_pct(total_c, total_registros), ")"),
    paste0("- `D_descartar_sintese`: ", total_d, " (", formatar_pct(total_d, total_registros), ")"),
    "",
    paste0("Arquivo que passa a orientar a proxima etapa: `", ARQUIVO_SAIDA_MATRIZ, "`."),
    ""
  )
  substituir_ou_anexar_secao(ARQUIVO_ESTADO_ATUAL, "## ETAPA_14 - reavaliacao criteriosa dos resumos", secao_estado)

  secao_decisao <- c(
    "---",
    "",
    paste0("## ", format(Sys.Date(), "%Y-%m-%d"), " - Reavaliacao criteriosa dos resumos como alternativa a leitura full-text massiva"),
    "",
    "Decisao: criar uma etapa intermediaria, auditavel e reprodutivel, para reavaliar os 3.678 registros do nucleo analitico revisado apenas com base em titulo, resumo, palavras-chave e campos ja preenchidos na matriz final, separando os registros em quatro estratos de uso (`A_nucleo_forte`, `B_nucleo_descritivo`, `C_contextual`, `D_descartar_sintese`).",
    "",
    "Motivo: a ETAPA_13 mostrou que 71,3% do nucleo ficou com `resumo_suficiente_para_extracao = parcial` ou `nao`, o que impede tratar todos os registros como igualmente fortes para sintese analitica profunda sem criar um corte intermediario conservador.",
    "",
    "Impacto: a matriz original nao foi alterada. A nova fonte operacional para a etapa seguinte passa a ser `07_SINTESE_TEMATICA/matriz_extracao_final_reavaliada_resumos.csv`, acompanhada de relatorio metodologico, tabelas agregadas, amostra de auditoria e log de execucao.",
    "",
    "Arquivos gerados:",
    "- `07_SINTESE_TEMATICA/matriz_extracao_final_reavaliada_resumos.csv`",
    "- `07_SINTESE_TEMATICA/relatorio_reavaliacao_criteriosa_resumos.md`",
    "- `05_ANALISE_R/tabelas/tabela14_reavaliacao_resumos_por_estrato.csv`",
    "- `05_ANALISE_R/tabelas/tabela15_sinais_reavaliacao_resumos.csv`",
    "- `05_ANALISE_R/tabelas/amostra_auditoria_reavaliacao_resumos.csv`",
    "- `00_CONTROLE/ROTINAS/LOGS/ETAPA_14_REAVALIAR_RESUMOS_CRITERIOSO.md`",
    "",
    "Limitacao principal: a etapa nao substitui leitura full-text e nao permite afirmar resultados profundos para todos os registros. Ela apenas cria um corte intermediario, auditavel e reprodutivel, para separar sintese analitica forte, mapeamento descritivo, uso contextual e descarte da sintese.",
    ""
  )
  texto_decisoes <- readChar(ARQUIVO_DECISOES, nchars = file.info(ARQUIVO_DECISOES)$size, useBytes = TRUE)
  if (!grepl("Reavaliacao criteriosa dos resumos como alternativa a leitura full-text massiva", texto_decisoes, fixed = TRUE)) {
    escrever_utf8(ARQUIVO_DECISOES, c(strsplit(texto_decisoes, "\r?\n", perl = TRUE)[[1]], secao_decisao))
  }

  valores_validos <- c("A_nucleo_forte", "B_nucleo_descritivo", "C_contextual", "D_descartar_sintese")
  erros_validacao <- character(0)

  if (!file.exists(ARQUIVO_SAIDA_MATRIZ)) erros_validacao <- c(erros_validacao, "Matriz de saida nao foi criada.")
  if (nrow(matriz_saida) != nrow(matriz)) erros_validacao <- c(erros_validacao, "Matriz de saida nao manteve o mesmo numero de linhas da entrada.")
  if (!"estrato_uso_resumo" %in% names(matriz_saida)) erros_validacao <- c(erros_validacao, "Coluna estrato_uso_resumo ausente.")
  if (!"entra_sintese_analitica_forte" %in% names(matriz_saida)) erros_validacao <- c(erros_validacao, "Coluna entra_sintese_analitica_forte ausente.")
  if (!"entra_mapeamento_descritivo" %in% names(matriz_saida)) erros_validacao <- c(erros_validacao, "Coluna entra_mapeamento_descritivo ausente.")
  if (!"justificativa_reavaliacao_resumo" %in% names(matriz_saida)) erros_validacao <- c(erros_validacao, "Coluna justificativa_reavaliacao_resumo ausente.")
  if (any(is.na(matriz_saida$estrato_uso_resumo) | matriz_saida$estrato_uso_resumo == "")) erros_validacao <- c(erros_validacao, "Existem registros sem estrato_uso_resumo.")
  if (!setequal(unique(matriz_saida$estrato_uso_resumo), valores_validos)) erros_validacao <- c(erros_validacao, "Os valores de estrato_uso_resumo diferem dos quatro estratos esperados.")
  if (!file.exists(ARQUIVO_RELATORIO)) erros_validacao <- c(erros_validacao, "Relatorio metodologico nao foi criado.")
  if (!file.exists(ARQUIVO_TABELA14) | !file.exists(ARQUIVO_TABELA15)) erros_validacao <- c(erros_validacao, "Tabelas obrigatorias nao foram criadas.")
  if (!file.exists(ARQUIVO_AMOSTRA)) erros_validacao <- c(erros_validacao, "Amostra de auditoria nao foi criada.")
  if (!file.exists(ARQUIVO_LOG)) erros_validacao <- c(erros_validacao, "Log nao foi criado.")

  if (length(erros_validacao) > 0) {
    stop(paste(erros_validacao, collapse = " "))
  }

  linhas_done <- c(
    paste0("data_hora: ", format(Sys.time(), "%Y-%m-%d %H:%M:%S")),
    "status: concluido",
    paste0("total_registros: ", total_registros),
    paste0("A_nucleo_forte: ", total_a),
    paste0("B_nucleo_descritivo: ", total_b),
    paste0("C_contextual: ", total_c),
    paste0("D_descartar_sintese: ", total_d),
    paste0("matriz_reavaliada: ", ARQUIVO_SAIDA_MATRIZ),
    paste0("relatorio: ", ARQUIVO_RELATORIO)
  )
  escrever_utf8(ARQUIVO_DONE, linhas_done)

  cat("ETAPA_14 concluida com sucesso.\n")
  cat("Total de registros:", total_registros, "\n")
  cat("A_nucleo_forte:", total_a, "\n")
  cat("B_nucleo_descritivo:", total_b, "\n")
  cat("C_contextual:", total_c, "\n")
  cat("D_descartar_sintese:", total_d, "\n")
}

tryCatch(
  main(),
  error = function(e) {
    registrar_falha(conditionMessage(e))
    stop(e)
  }
)
