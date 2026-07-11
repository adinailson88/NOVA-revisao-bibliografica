# Estrutura e fontes de verdade do pipeline

## Organização preservada

Os 109 produtos intermediários foram mantidos nos caminhos originais para preservar as referências internas dos scripts e a rastreabilidade do pipeline.

| Diretório | Função | Fonte principal |
|---|---|---|
| `01_PROTOCOLO/` | Planejamento, strings e logs de coleta | Protocolo e registros contemporâneos da busca |
| `03_PROCESSADOS/` | Normalização e deduplicação | `corpus_consolidado.csv` e `relatorio_deduplicacao.md` |
| `04_TRIAGEM/` | Pré-triagem, auditoria amostral e decisões de dúvida | `matriz_triagem_auditada.csv` e `decisao_duvidas_revisada.tsv` |
| `05_ANALISE_R/` | Scripts e produtos históricos da análise | Tabelas 01–34, figuras 01–14 e relatório |
| `07_SINTESE_TEMATICA/` | Extração, alinhamento, auditoria qualitativa e núcleo final | `auditoria_qualitativa_resumos_137.csv` e `nucleo_final_pos_auditoria_resumos.csv` |
| `latex-artigo/` | Material diretamente consumido pelo artigo | Fonte LaTeX, tabelas e figuras publicadas |
| `scripts/` | Implementação vigente e verificações | Python do pipeline e `scripts/r/10_gerar_produtos_artigo.R` |
| `docs/` | Governança da revisão controlada | Plano, status, inventários e relatórios |

## Regras para evitar duplicidade ambígua

1. Os arquivos em `05_ANALISE_R/` preservam o histórico e os produtos intermediários.
2. Os arquivos em `latex-artigo/fontes/` e `latex-artigo/figuras/` são os produtos consumidos diretamente pelo artigo.
3. O script `scripts/r/10_gerar_produtos_artigo.R` é a fonte vigente para regenerar as tabelas e figuras finais.
4. Nenhum arquivo intermediário foi movido ou renomeado, pois os scripts dependem dos caminhos existentes.
5. Divergências futuras devem ser resolvidas na fonte vigente e regeneradas, não corrigidas manualmente em múltiplas cópias.

## Fechamento da Etapa 4

Os produtos incorporados confirmam:

- 12.118 registros brutos;
- 9.542 registros únicos após deduplicação;
- 3.786 no corte analítico inicial;
- 3.678 após resolução dos casos de dúvida;
- 137 na análise central;
- 104 no núcleo final.

A pendência documental da Etapa 4 está encerrada.
