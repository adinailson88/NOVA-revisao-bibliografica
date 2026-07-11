# Log da busca manual Web of Science

Data: 2026-07-08
Base: Web of Science Core Collection
Modo: busca manual via Advanced Search
Campo: TS = Topic
Janela: PY = 2010-2026
Formato exportado: RIS

## Resultados brutos

- WOS_NUCLEO_01 = 610 registros
- WOS_NUCLEO_02 = 557 registros
- WOS_NUCLEO_03 = 10 registros
- Total bruto antes de deduplicação = 1.177 registros

## Arquivos exportados

- WOS_NUCLEO_01_20260708_part01.ris
- WOS_NUCLEO_02_20260708_part01.ris
- WOS_NUCLEO_03_20260708_part01.ris

## Decisão metodológica

A busca Web of Science foi encerrada nesta rodada com as três strings do núcleo principal. Buscas conceituais, tecnológicas ou biossistêmicas não foram incorporadas ao corpus principal para evitar ampliação indevida do escopo.

## Mapeamento arquivo → string (registrado em 2026-07-08, sessão de saneamento)

O protocolo (`01_PROTOCOLO/strings_nativas_por_base.md`) define 4 strings de núcleo para a WoS
(A1–A4). Apenas 3 arquivos `.ris` existem nesta pasta. O usuário confirmou nesta sessão a
correspondência 1:1 abaixo, por ordem de execução — **atenção: essa correspondência foi assumida
pelo usuário de memória nesta sessão, não reconstruída a partir de evidência registrada no momento
da busca original (não havia log de qual string gerou qual arquivo).** Se o usuário lembrar de
uma ordem diferente, corrigir esta tabela antes de usá-la em qualquer relatório de reprodutibilidade.

| Arquivo | String correspondente (assumida) | Registros |
|---|---|---|
| WOS_NUCLEO_01_20260708_part01.ris | WOS_NUCLEO_A1_MANUTENCAO_SUSTENTABILIDADE | 610 |
| WOS_NUCLEO_02_20260708_part01.ris | WOS_NUCLEO_A2_CONTEXTO_PUBLICO_UNIVERSITARIO | 557 |
| WOS_NUCLEO_03_20260708_part01.ris | WOS_NUCLEO_A3_PRIORIZACAO_ESTRATEGIA_MANUTENCAO | 10 |
| WOS_NUCLEO_04_20260708_part01.ris | WOS_NUCLEO_A4_GESTAO_ATIVOS_CICLO_VIDA | 502 |

## Pendência — RESOLVIDA em 2026-07-08 (15:01)

O usuário já havia rodado a string A4 antes mesmo de ela ser formalmente solicitada nesta sessão.
`WOS_NUCLEO_04_20260708_part01.ris` confirmado com 502 registros (contagem de blocos `TY  -`).
Amostra dos 5 primeiros títulos (`TI  -`) confere com o tema da string A4 (gestão de ativos,
ciclo de vida, custo de ciclo de vida, BIM aplicado a condição de edificação) — sem falso positivo
óbvio na amostra. As 4 strings do núcleo da Web of Science estão agora completas:
610 + 557 + 10 + 502 = **1.679 registros brutos**, antes de deduplicação.

Nota: o nome do arquivo não segue o padrão sugerido (`wos_nucleo_a4_gestao_ativos_ciclo_vida_
YYYYMMDD.ris`) — manteve o padrão já em uso pelos arquivos 01–03 (`WOS_NUCLEO_04_20260708_part01.ris`),
o que é aceitável por consistência com os demais.
