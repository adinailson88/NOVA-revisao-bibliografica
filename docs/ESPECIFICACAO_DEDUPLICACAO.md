# Especificação reprodutível da deduplicação

## Entradas e saídas

| Tipo | Arquivo |
|---|---|
| Entrada padronizada | `03_PROCESSADOS/registros_normalizados.csv` |
| Corpus único | `03_PROCESSADOS/corpus_consolidado.csv` |
| Grupos fundidos | `03_PROCESSADOS/duplicatas_detectadas.csv` |
| Relatório | `03_PROCESSADOS/relatorio_deduplicacao.md` |
| Implementação | `scripts/python/consolidar_deduplicar.py` |
| Verificação | `scripts/python/verificar_artigo.py` |

## Regras

1. DOI: minúsculas; remoção de `https://doi.org/`, `http://dx.doi.org/`, prefixo `doi:`, espaços e ponto final.
2. Título: decomposição Unicode, remoção de acentos e pontuação, minúsculas e espaços colapsados.
3. Títulos normalizados com menos de oito caracteres não agrupam registros.
4. DOI idêntico agrupa automaticamente.
5. Título normalizado idêntico agrupa quando não existe conflito entre DOIs ou identificadores próprios.
6. DOI divergente ou identificador próprio divergente preserva registros separados.
7. Bases, strings e IDs brutos são preservados.
8. Resumo mais longo é preferido; demais campos usam completude e prioridade de fonte.

## Resultados verificados

| Métrica | Valor |
|---|---:|
| Registros brutos | 12.118 |
| Registros únicos | 9.542 |
| Ocorrências removidas | 2.576 |
| Grupos fundidos | 1.808 |
| DOI e título | 1.616 |
| Somente DOI | 19 |
| Somente título normalizado | 173 |
| Conflitos preservados | 98 |
| Com DOI após deduplicação | 8.264 |
| Sem DOI após deduplicação | 1.278 |
| Com resumo | 8.976 |
| Sem resumo | 566 |

Distribuição do tamanho dos 1.808 grupos:

| Tamanho do grupo | Grupos |
|---:|---:|
| 2 | 1.237 |
| 3 | 428 |
| 4 | 106 |
| 5 | 24 |
| 6 | 11 |
| 8 | 2 |

## Limitações

- Não há comparação aproximada ou semântica entre títulos.
- Artigo de evento e versão posterior não são vinculados automaticamente.
- Os 173 grupos fundidos apenas por título possuem maior risco de fusão indevida.
- Os 98 conflitos de título foram preservados, mas não resolvidos manualmente.
- Não houve revisão manual integral dos 1.808 grupos.
- Não é possível afirmar ausência absoluta de duplicatas remanescentes ou fusões incorretas.
