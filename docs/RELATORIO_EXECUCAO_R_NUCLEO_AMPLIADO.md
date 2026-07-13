# RELATÓRIO — Geração dos produtos do núcleo ampliado (121 registros)

## Nota metodológica sobre a execução

Este relatório substitui a execução via R/Codex originalmente prevista em
`docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md`. Nenhum artefato dessa execução (script
`10b_...R`, tabelas/figuras `_nucleo_ampliado_121`, relatório comparativo) foi encontrado na
branch quando a sessão foi retomada. Por decisão explícita do usuário nesta sessão ("não sei
rodar R -- faça a validação de outro jeito"), a lógica de `scripts/r/10_gerar_produtos_artigo.R`
foi **recriada em Python**, reimplementando termo a termo as mesmas regras de expansão
multivalor, agregação e rotulagem — ver `scripts/python/gerar_produtos_artigo_nucleo_ampliado.py`.
Nenhum script R foi escrito ou executado nesta sessão.

## Validação de consistência

- Entrada: `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv`, 121
  registros, sem `id_unico` duplicado (verificado por assert no script).
- Contagem de base×combinação recalculada diretamente do arquivo de entrada (não copiada):
  Scopus 67, Scopus\|WoS 41, WoS 7, Crossref\|Scopus\|WoS 3, Crossref\|Scopus 2, Crossref 1.
- Tipo documental: 5 dos 17 novos registros (`REG_02383`, `REG_07814`, `REG_07815`, `REG_05418`,
  `REG_06840`, promovidos na reavaliação) vieram do corpus original com `tipo_documento` em
  rótulo bruto (ex. "Journal"), não harmonizado — bug identificado e corrigido durante a geração
  (harmonização aplicada de forma condicional, reaproveitando o mesmo mapeamento usado para os
  104 originais) antes de aceitar os números finais.

## Comparativo 104 → 121

### Dimensões de sustentabilidade

| Dimensão | 104 (N / %) | 121 (N / %) |
|---|---|---|
| Técnica e operacional | 102 / 98,1% | 116 / 95,9% |
| Institucional | 92 / 88,5% | 97 / 80,2% |
| Ambiental | 84 / 80,8% | 92 / 76,0% |
| Ciclo de vida | 60 / 57,7% | 65 / 53,7% |
| Econômica | 59 / 56,7% | 63 / 52,1% |
| Social | 57 / 54,8% | 59 / 48,8% |

Todas as dimensões crescem em N absoluto; os percentuais recuam ligeiramente porque o
denominador cresce mais rápido que algumas dimensões específicas — não há mudança de ordenação
relativa (técnica-operacional continua predominante, social continua a menor).

### Critérios de priorização (top 10)

| Critério | 104 | 121 | Δ |
|---|---|---|---|
| desempenho_operacional | 93 | 99 | +6 |
| informacao_dados | 76 | 82 | +6 |
| custo | 60 | 63 | +3 |
| energia | 36 | 44 | **+8** |
| vida_util | 40 | 44 | +4 |
| condicao_fisica | 27 | 34 | **+7** |
| risco | 31 | 33 | +2 |
| manutenibilidade | 19 | 25 | **+6** |
| conforto | 17 | 22 | **+5** |
| seguranca | 17 | 18 | +1 |

`energia`, `condicao_fisica`, `manutenibilidade` e `conforto` crescem proporcionalmente mais que
a média — coerente com o perfil temático dos 17 novos estudos (aplicações de IA/ML em eficiência
energética, detecção de dano/condição física e conforto térmico).

### Métodos/técnicas — achado central desta rodada

| Método | 104 | 121 | Δ |
|---|---|---|---|
| **machine learning** | **9** | **26** | **+17** |
| framework | 96 | 101 | +5 |
| decision support | 25 | 29 | +4 |
| BIM | 26 | 28 | +2 |
| IoT | 9 | 13 | +4 |
| digital twin | 8 | 11 | +3 |
| life-cycle cost | 13 | 16 | +3 |
| optimization | 18 | 19 | +1 |
| fuzzy | 10 | 11 | +1 |
| scoring, ranking, AHP, TOPSIS, ANP, MCDM, Delphi, balanced scorecard, case-based reasoning, Bayesian BWM | inalterados | inalterados | 0 |

Nenhum método novo (fora do vocabulário já usado nos 104) foi necessário. O crescimento de
`machine learning` (+17, de 9 para 26 — o dobro em N absoluto quase triplicado) é exatamente o
esperado por construção: todos os 17 novos registros foram admitidos ao núcleo justamente por
IA/ML aplicada confirmada (RQ6). Os demais métodos (BIM, IoT, digital twin, decision support)
crescem de forma modesta e proporcional ao crescimento geral de N — não há evidência de que a
busca de sensibilidade tenha inflado artificialmente outras categorias metodológicas.

### Tipos documentais harmonizados

| Tipo | 104 | 121 |
|---|---|---|
| Artigo de periódico | 79 (76,0%) | 90 (74,4%) |
| Trabalho em evento | 15 (14,4%) | 20 (16,5%) |
| Livro ou série de livro | 10 (9,6%) | 11 (9,1%) |

### Menções ODS/ESG

Inalterado: 1 registro com menção a ODS/SDG (o mesmo `masmoudi_ahptopsis_2026` do núcleo
original), 0 com ESG. Nenhum dos 17 novos registros menciona esses termos nos campos auditados.

### Distribuição por base de origem

| Base | 104 | 121 |
|---|---|---|
| Scopus | 98 | 113 |
| WoS | 49 | 51 |
| Crossref | 6 | 6 |

Todos os 17 novos vêm de Scopus (15) e WoS (2); nenhum novo registro de núcleo veio do Crossref
nesta rodada (a fatia Crossref concentrou a ausência de resumo, reduzindo sua taxa de aprovação
na triagem — ver `03_PROCESSADOS/relatorio_normalizacao_sensibilidade_ia.md`).

## Arquivos gerados

Todos em `latex-artigo/fontes/` (sufixo `_nucleo_ampliado_121`) e `latex-artigo/figuras/`
(mesmo sufixo), sem sobrescrever nenhum arquivo `_nucleo_final_104`:
tabela26 a tabela36 (exceto tabela_estrategia_busca, que trata de estratégia de busca bruta e
não do núcleo), figura09, figura11, figura12, figura13, figura14.

## Recomendação

Os números do núcleo ampliado são internamente consistentes (validados contra o arquivo de
entrada, sem duplicatas, com o teste de sanidade de ODS/ESG batendo com o núcleo original) e
prontos para uso na atualização do texto do artigo (Fase 8).
