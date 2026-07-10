## ETAPA_10 -- aplica a resolucao da classe "duvida" a partir da tabela de decisao revisada
## (04_TRIAGEM/decisao_duvidas_revisada.tsv), eliminando "duvida" das contas do nucleo analitico.
## Nao refaz a triagem: apenas incorpora, por left_join em id_unico, uma decisao ja tomada fora
## deste script e documentada em 00_CONTROLE/CONTINUAR_RESOLUCAO_DUVIDAS.txt.
##
## Entrada:
##   - 04_TRIAGEM/matriz_triagem_auditada.csv         (matriz vigente, 9.542 registros)
##   - 04_TRIAGEM/decisao_duvidas_revisada.tsv         (decisao registro a registro para "duvida")
## Saida:
##   - 05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv
##   - 05_ANALISE_R/tabelas/tabela09_resolucao_duvidas.csv
##   - 05_ANALISE_R/tabelas/tabela10_comparacao_nucleo_original_revisado.csv
##   - 05_ANALISE_R/tabelas/tabela11_distribuicao_classe_final_sem_duvida.csv
##   - 05_ANALISE_R/tabelas/tabela12_nucleo_revisado_por_base_origem.csv
##   - 05_ANALISE_R/tabelas/tabela13_nucleo_revisado_por_ano.csv

source("05_ANALISE_R/scripts/00_config.R")

NUCLEO_ANTERIOR_ESPERADO <- 3786
NUCLEO_REVISADO_ESPERADO <- 3678
TOTAL_DUVIDA_ESPERADO <- 4276
RELEVANTE_ESPERADO <- 206
DESCARTAR_ESPERADO <- 4070

## 1. Carregar matriz vigente (fonte de verdade da triagem/auditoria -- nao refeita aqui)
matriz <- readr::read_csv(CAMINHO_MATRIZ, show_col_types = FALSE)

## 2. Carregar tabela de decisao revisada (fonte de verdade da resolucao de "duvida")
decisao <- readr::read_tsv(
  "04_TRIAGEM/decisao_duvidas_revisada.tsv",
  show_col_types = FALSE,
  locale = readr::locale(encoding = "UTF-8")
)

## --- Validacoes obrigatorias antes de aplicar qualquer coisa ---
erros <- character(0)

if (any(is.na(decisao$id_unico) | decisao$id_unico == "")) {
  erros <- c(erros, "Existem linhas em decisao_duvidas_revisada.tsv sem id_unico.")
}
if (any(duplicated(decisao$id_unico))) {
  erros <- c(erros, paste0(
    "Existem id_unico duplicados em decisao_duvidas_revisada.tsv: ",
    sum(duplicated(decisao$id_unico)), " duplicatas."
  ))
}
if (any(is.na(decisao$decisao_revisada) | decisao$decisao_revisada == "")) {
  erros <- c(erros, "Existem linhas em decisao_duvidas_revisada.tsv sem decisao_revisada.")
}
categorias_validas <- c("RELEVANTE", "DESCARTAR")
categorias_encontradas <- unique(decisao$decisao_revisada)
categorias_invalidas <- setdiff(categorias_encontradas, categorias_validas)
if (length(categorias_invalidas) > 0) {
  erros <- c(erros, paste0(
    "Categorias de decisao_revisada fora do esperado (RELEVANTE/DESCARTAR): ",
    paste(categorias_invalidas, collapse = ", ")
  ))
}
if (nrow(decisao) != TOTAL_DUVIDA_ESPERADO) {
  erros <- c(erros, paste0(
    "Total de decisoes (", nrow(decisao), ") diferente do esperado (", TOTAL_DUVIDA_ESPERADO, ")."
  ))
}
n_relevante_tsv <- sum(decisao$decisao_revisada == "RELEVANTE")
n_descartar_tsv <- sum(decisao$decisao_revisada == "DESCARTAR")
if (n_relevante_tsv != RELEVANTE_ESPERADO) {
  erros <- c(erros, paste0(
    "Total RELEVANTE no TSV (", n_relevante_tsv, ") diferente do esperado (", RELEVANTE_ESPERADO, ")."
  ))
}
if (n_descartar_tsv != DESCARTAR_ESPERADO) {
  erros <- c(erros, paste0(
    "Total DESCARTAR no TSV (", n_descartar_tsv, ") diferente do esperado (", DESCARTAR_ESPERADO, ")."
  ))
}

ids_duvida_matriz <- matriz$id_unico[matriz$classe_auditada == "duvida"]
ids_sem_decisao <- setdiff(ids_duvida_matriz, decisao$id_unico)
if (length(ids_sem_decisao) > 0) {
  erros <- c(erros, paste0(
    length(ids_sem_decisao), " registros classe_auditada=='duvida' na matriz nao tem decisao no TSV. ",
    "Exemplos: ", paste(head(ids_sem_decisao, 5), collapse = ", ")
  ))
}

if (length(erros) > 0) {
  cat("BLOQUEIO -- validacao da tabela de decisao falhou:\n")
  for (e in erros) cat(" - ", e, "\n")
  stop("Execucao interrompida: ver mensagens de bloqueio acima. Nao prosseguir sem corrigir a divergencia.")
}

cat("Validacao da tabela de decisao: OK -- ", nrow(decisao), " decisoes, ",
    n_relevante_tsv, " RELEVANTE, ", n_descartar_tsv, " DESCARTAR.\n", sep = "")

## 3. left_join por id_unico (mantem todas as colunas da matriz; so usa decisao_revisada e
##    subgrupo_duvida do TSV para nao duplicar colunas ja existentes na matriz)
decisao_min <- decisao %>%
  select(id_unico, decisao_revisada, confianca, regra, justificativa_reprodutivel)

matriz_revisada <- matriz %>%
  left_join(decisao_min, by = "id_unico")

## 4. classe_final_sem_duvida
matriz_revisada <- matriz_revisada %>%
  mutate(
    classe_final_sem_duvida = case_when(
      classe_auditada == "relevante" ~ "relevante",
      classe_auditada == "duvida" & decisao_revisada == "RELEVANTE" ~ "relevante",
      classe_auditada == "duvida" & decisao_revisada == "DESCARTAR" ~ "irrelevante_resolvido",
      classe_auditada == "complementar" ~ "complementar",
      classe_auditada == "irrelevante" ~ "irrelevante",
      classe_auditada == "sem_resumo" ~ "sem_resumo",
      TRUE ~ "erro_classificacao"
    ),
    nucleo_analitico_revisado = classe_final_sem_duvida == "relevante"
  )

## Reconstroi subgrupo_duvida (apenas_bloco_a/apenas_bloco_b/nenhum_bloco) localmente, caso a
## coluna nao exista na matriz de entrada -- necessaria para a tabela 9.
if (!"subgrupo_duvida" %in% names(matriz_revisada)) {
  matriz_revisada <- matriz_revisada %>%
    mutate(
      subgrupo_duvida = case_when(
        classe_auditada != "duvida" ~ NA_character_,
        bloco_a_presente == "sim" & bloco_b_presente == "nao" ~ "apenas_bloco_a",
        bloco_a_presente == "nao" & bloco_b_presente == "sim" ~ "apenas_bloco_b",
        bloco_a_presente == "sim" & bloco_b_presente == "sim" ~ "ambos_blocos",
        TRUE ~ "nenhum_bloco"
      )
    )
}

## --- Checagens pos-aplicacao (regra 4/5/6 da tarefa 8) ---
n_erro_classificacao <- sum(matriz_revisada$classe_final_sem_duvida == "erro_classificacao")
## Checagem estrita: classe_final_sem_duvida nunca pode valer "duvida" (regra 5 da tarefa 8) --
## diferente de contar quantos registros ORIGINALMENTE "duvida" foram resolvidos para dentro do
## nucleo (isso e esperado = 206, nao e um erro).
n_classe_final_igual_duvida <- sum(matriz_revisada$classe_final_sem_duvida == "duvida")
n_duvida_original_resolvida_no_nucleo <- sum(matriz_revisada$classe_auditada == "duvida" & matriz_revisada$nucleo_analitico_revisado)
n_duvida_apenas_a_sem_decisao_no_nucleo <- sum(
  matriz_revisada$classe_auditada == "duvida" &
    matriz_revisada$subgrupo_duvida == "apenas_bloco_a" &
    matriz_revisada$nucleo_analitico_revisado &
    is.na(matriz_revisada$decisao_revisada)
)
if (n_duvida_apenas_a_sem_decisao_no_nucleo > 0) {
  stop("BLOQUEIO: ha registros 'duvida'/apenas_bloco_a no nucleo revisado sem decisao explicita no TSV -- nao permitido (regra 4 da tarefa 8).")
}

dir.create(DIR_TABELAS, showWarnings = FALSE, recursive = TRUE)
readr::write_csv(matriz_revisada, file.path(DIR_TABELAS, "matriz_nucleo_analitico_revisado.csv"))

## Tabela 9 -- resolucao das duvidas
tabela09_resumo <- tibble::tibble(
  total_duvidas_avaliadas = nrow(decisao),
  total_relevante = n_relevante_tsv,
  total_descartar = n_descartar_tsv
)
tabela09_por_subgrupo <- matriz_revisada %>%
  filter(classe_auditada == "duvida") %>%
  count(subgrupo_duvida, decisao_revisada, name = "n") %>%
  arrange(subgrupo_duvida, decisao_revisada)

readr::write_csv(tabela09_resumo, file.path(DIR_TABELAS, "tabela09_resolucao_duvidas.csv"))
## Anexa o detalhe por subgrupo no mesmo arquivo logico, em CSV separado para nao misturar forma
readr::write_csv(tabela09_por_subgrupo, file.path(DIR_TABELAS, "tabela09b_resolucao_duvidas_por_subgrupo.csv"))

## Tabela 10 -- comparacao nucleo original x revisado
n_nucleo_anterior <- sum(matriz$id_unico %in% matriz_revisada$id_unico[matriz_revisada$classe_auditada == "relevante"]) # placeholder, recalculado abaixo
## Nucleo anterior real: recarrega a definicao da ETAPA_09 (relevante + duvida/apenas_bloco_a)
matriz_nucleo_anterior <- readr::read_csv(file.path(DIR_TABELAS, "matriz_nucleo_analitico.csv"), show_col_types = FALSE)
n_nucleo_anterior <- sum(matriz_nucleo_anterior$nucleo_analitico)
n_nucleo_revisado <- sum(matriz_revisada$nucleo_analitico_revisado)

tabela10 <- tibble::tibble(
  nucleo_anterior = n_nucleo_anterior,
  nucleo_revisado = n_nucleo_revisado,
  diferenca_absoluta = n_nucleo_revisado - n_nucleo_anterior,
  diferenca_percentual = round(100 * (n_nucleo_revisado - n_nucleo_anterior) / n_nucleo_anterior, 2)
)
readr::write_csv(tabela10, file.path(DIR_TABELAS, "tabela10_comparacao_nucleo_original_revisado.csv"))

if (n_nucleo_revisado != NUCLEO_REVISADO_ESPERADO) {
  cat("\nATENCAO -- divergencia no total do nucleo revisado:\n")
  cat("  Esperado:", NUCLEO_REVISADO_ESPERADO, " | Obtido:", n_nucleo_revisado, "\n")

  ids_nucleo_anterior <- matriz_nucleo_anterior$id_unico[matriz_nucleo_anterior$nucleo_analitico]
  ids_nucleo_revisado <- matriz_revisada$id_unico[matriz_revisada$nucleo_analitico_revisado]
  saiu_do_nucleo <- setdiff(ids_nucleo_anterior, ids_nucleo_revisado)
  entrou_no_nucleo <- setdiff(ids_nucleo_revisado, ids_nucleo_anterior)
  cat("  Registros que saem do nucleo anterior e nao estao no revisado:", length(saiu_do_nucleo), "\n")
  cat("  Registros que entram no nucleo revisado e nao estavam no anterior:", length(entrou_no_nucleo), "\n")
  divergencia_ids <- tibble::tibble(
    id_unico = c(saiu_do_nucleo, entrou_no_nucleo),
    movimento = c(rep("saiu_do_nucleo_anterior", length(saiu_do_nucleo)), rep("entrou_no_nucleo_revisado", length(entrou_no_nucleo)))
  )
  readr::write_csv(divergencia_ids, file.path(DIR_TABELAS, "tabela10b_divergencia_nucleo_ids.csv"))
  cat("  Detalhe salvo em tabela10b_divergencia_nucleo_ids.csv -- nao forcado o valor esperado.\n")
}

## Tabela 11 -- distribuicao por classe_final_sem_duvida
tabela11 <- matriz_revisada %>%
  count(classe_final_sem_duvida, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1)) %>%
  arrange(desc(n))
readr::write_csv(tabela11, file.path(DIR_TABELAS, "tabela11_distribuicao_classe_final_sem_duvida.csv"))

## Tabela 12 -- nucleo revisado por base de origem
tabela12 <- matriz_revisada %>%
  filter(nucleo_analitico_revisado) %>%
  count(bases_origem, name = "n") %>%
  mutate(pct = round(100 * n / sum(n), 1)) %>%
  arrange(desc(n))
readr::write_csv(tabela12, file.path(DIR_TABELAS, "tabela12_nucleo_revisado_por_base_origem.csv"))

## Tabela 13 -- nucleo revisado por ano
tabela13 <- matriz_revisada %>%
  filter(!is.na(ano)) %>%
  group_by(ano) %>%
  summarise(
    n_corpus = n(),
    n_nucleo_revisado = sum(nucleo_analitico_revisado),
    .groups = "drop"
  ) %>%
  arrange(ano)
readr::write_csv(tabela13, file.path(DIR_TABELAS, "tabela13_nucleo_revisado_por_ano.csv"))

## --- Relatorio de validacao final (tarefa 8) impresso no console e retornado para o log ---
cat("\n===== VALIDACAO FINAL (tarefa 8) =====\n")
cat("Total da matriz original:", nrow(matriz), "\n")
cat("Total em 'duvida' na matriz:", sum(matriz$classe_auditada == "duvida"), "\n")
cat("Total de decisoes importadas:", nrow(decisao), "\n")
cat("Total resolvido como RELEVANTE:", n_relevante_tsv, "\n")
cat("Total resolvido como DESCARTAR:", n_descartar_tsv, "\n")
cat("Nucleo anterior:", n_nucleo_anterior, "\n")
cat("Nucleo revisado:", n_nucleo_revisado, "\n")
cat("classe_final_sem_duvida ainda igual a 'duvida' (deve ser 0):", n_classe_final_igual_duvida, "\n")
cat("Registros originalmente 'duvida' resolvidos para dentro do nucleo (esperado = 206):",
    n_duvida_original_resolvida_no_nucleo, "\n")
cat("Registros com classe_final_sem_duvida == 'erro_classificacao':", n_erro_classificacao, "\n")
cat("=======================================\n")
