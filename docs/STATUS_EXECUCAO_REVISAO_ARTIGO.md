# Status da revisão metodológica e textual

## Repositório
- URL: https://github.com/adinailson88/NOVA-revisao-bibliografica
- Branch: revisao-metodologica-controlada
- Data de início: 2026-07-10
- Commit de origem: `e10ef825e6a560f19ffc12306d55b142b3c360e3`
- Preservação: branch `preservacao-original-revisao-metodologica-20260710`

## Regra de execução
O trabalho será realizado estritamente conforme o arquivo:
`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`


## Progresso resumido

| Etapa | Situação |
|---|---|
| Etapa 1 | OK |
| Etapa 2 | OK |
| Etapa 3 | OK |
| Etapa 4 | OK |
| Etapa 5 | OK |

## Etapas

| Etapa | Descrição | Status | Commit | Pendências |
|---:|---|---|---|---|
| 0 | Preparação e preservação dos arquivos | Concluída | Commit exclusivo da Etapa 0; hash registrado no relatório de execução | Recompilação local independente e logs completos: Informação insuficiente para verificar. |
| 1 | Auditoria do tipo de revisão | Concluída | Commit exclusivo da Etapa 1; hash registrado no relatório de execução | Aguardar autorização explícita para a Etapa 2 |
| 2 | Pergunta, objetivos e escopo | Concluída | Commit exclusivo da Etapa 2; hash registrado no relatório de execução | Aguardar autorização explícita para a Etapa 3 |
| 3 | Estratégia de busca e reprodutibilidade | Concluída | Commit exclusivo da Etapa 3; hash registrado no relatório de execução | Pendências regularizadas; ressalva RIS×string e justificativa de 2010 permanecem documentadas |
| 4 | Funil de seleção | Concluída | Commit exclusivo da Etapa 4 e commit de encerramento documental | Sem pendência documental |
| 5 | Deduplicação | Concluída | Commit exclusivo da Etapa 5 | Sem pendência operacional |
| 6 | Triagem e auditoria dos registros | Concluída | Artigo, mapa, relatório e verificador atualizados | Sem pendência bloqueante |
| 7 | Texto completo e elegibilidade | Não iniciada | | |
| 8 | Dicionário de categorias e extração | Não iniciada | | |
| 9 | Avaliação metodológica dos estudos | Não iniciada | | |
| 10 | Auditoria dos resultados | Não iniciada | | |
| 11 | Discussão | Não iniciada | | |
| 12 | Matriz analítica | Não iniciada | | |
| 13 | Limitações | Não iniciada | | |
| 14 | Redação e padronização | Não iniciada | | |
| 15 | Referências metodológicas | Não iniciada | | |
| 16 | Consolidação final | Não iniciada | | |

## Registro da Etapa 0

### Arquivos analisados
- Estrutura do repositório e histórico de commits.
- Fonte LaTeX principal e onze seções.
- Bibliografia.
- Bases derivadas, tabelas e figuras.
- Scripts Python e R.
- Workflow de geração e PDF publicado.

### Arquivos alterados
- `docs/INVENTARIO_ARTIGO_REVISAO.md` — criado.
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md` — atualizado.
- Nenhum arquivo do artigo foi alterado.

### Decisões
- A versão inicial foi preservada no commit `e10ef825e6a560f19ffc12306d55b142b3c360e3` e na branch `preservacao-original-revisao-metodologica-20260710`.
- Foram registrados Git blob SHAs para os arquivos principais.
- O `main.pdf` anexado foi usado apenas para compreensão do estado inicial; o repositório permanece como fonte oficial.

### Validações
- Branch de trabalho isolada da `main`.
- PDF publicado existente e legível, com 14 páginas.
- Workflow de compilação localizado.
- Inventário confrontado com o histórico e com a existência dos arquivos principais.
- Nenhuma alteração científica ou textual executada.

### Informações insuficientes
- Recompilação local independente: Informação insuficiente para verificar.
- Logs completos do workflow de origem: Informação insuficiente para verificar.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 1`.


## Registro da Etapa 1

### Data
2026-07-10

### Arquivos analisados
Fonte principal, resumo, introdução, revisão teórica, metodologia, resultados, limitações e considerações finais; Hu et al. (2026) e Franca (2025) nos limites definidos pelo plano.

### Diagnóstico
A denominação documentalmente sustentável é “revisão integrativa sistematizada, com apoio bibliométrico e síntese temática”. Não há base para transformar o trabalho em revisão sistemática por mudança de redação.

### Arquivos alterados
- `latex-artigo/sections/00_resumo.tex`
- `docs/RELATORIO_ETAPA_1.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Decisões
Resumo e abstract foram padronizados à denominação já usada na metodologia. Nenhum procedimento, número, resultado, objetivo ou referência foi alterado.

### Informação insuficiente
Protocolo prévio, pré-registro, leitura integral, avaliação metodológica, dupla revisão e conformidade integral ao PRISMA: Informação insuficiente para verificar.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 2`.


## Registro da Etapa 2

### Data
2026-07-10

### Diagnóstico
A RQ0 foi ajustada para não apresentar o contexto público universitário como característica de todo o corpus. RQ1–RQ5 foram alinhadas ao nível documental dos campos auditados.

### Arquivos alterados
- `latex-artigo/sections/01_introducao.tex`
- `latex-artigo/sections/03_metodologia.tex`
- `docs/RELATORIO_ETAPA_2.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Decisões
Foi inserida matriz explícita de alinhamento. Tema, corpus, método de seleção, números e resultados foram preservados.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 3`.


## Registro da Etapa 3

### Data
2026-07-10

### Diagnóstico
Scopus e Crossref possuem consultas e parâmetros reprodutíveis nos scripts. A Web of Science possui campo, data, período, identificadores e totais, mas não as strings literais. A reprodutibilidade integral do conjunto é parcial.

### Arquivos alterados
- `latex-artigo/sections/03_metodologia.tex`
- `docs/APENDICE_ESTRATEGIAS_BUSCA.md`
- `docs/RELATORIO_ETAPA_3.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 4`.


## Regularização anterior à Etapa 4

As pendências das Etapas 1–3 foram respondidas pelo pesquisador e incorporadas ao artigo e à documentação. Foram corrigidas as datas da Scopus, incluídas as quatro strings da Web of Science e registradas as ausências de pré-registro, texto completo, segundo avaliador e avaliação de qualidade. Os arquivos originais de protocolo citados não foram localizados nesta branch; sua eventual migração permanece pendente.


## Reconciliação final anterior à Etapa 4

- Scopus: 9.438 registros, sendo 9.433 da API e cinco exclusivos do export manual incorporados em 09/07/2026.
- Web of Science: 1.680 registros; A4 corrigido de 502 para 503 após recontagem.
- Crossref: 1.000 registros.
- Total bruto preservado: 12.118.
- O corte 2010–2026 foi mantido por corresponder à busca executada; não foi criada justificativa retrospectiva.
- Os seis arquivos de `01_PROTOCOLO/` foram incorporados à branch de trabalho.


## Registro da Etapa 4

### Data
2026-07-10

### Diagnóstico
O funil fecha numericamente, mas a redação anterior superestimava a extensão da revisão humana. A auditoria individual cobriu 100 de 9.542 registros; os demais mantiveram classificação automática.

### Alterações
Foi inserida tabela completa de rastreabilidade e a figura do funil foi corrigida. Automação, auditoria amostral, alinhamento determinístico e auditoria qualitativa passaram a ser relatados separadamente.

### Próxima ação
Parar e aguardar autorização explícita: `AUTORIZO A ETAPA 5`.


## Encerramento documental da Etapa 4

Os 109 produtos intermediários foram incorporados e organizados nas pastas 03, 04, 05 e 07. Foram validados os totais de deduplicação, o corte inicial de 3.786, a resolução das 4.276 dúvidas, o núcleo revisado de 3.678, a seleção de 137 e a auditoria final de 104. A pendência documental da Etapa 4 está encerrada.


## Registro da Etapa 5

A deduplicação foi especificada e validada sem mudança de lógica. Foram confirmados 1.808 grupos e 2.576 ocorrências removidas. O verificador automático passou a conferir produtos processados, DOI único, IDs e proveniência. Os conflitos detectados foram preservados como registros separados.

Próxima ação: aguardar `AUTORIZO A ETAPA 6`.


## Registro da Etapa 6

As camadas de seleção foram documentadas separadamente: pré-triagem determinística dos 9.542 registros, auditoria amostral de 100, resolução dos 4.276 casos de dúvida, reavaliação dos 3.678 registros, alinhamento de 137 registros centrais e auditoria qualitativa que consolidou 104 estudos. O artigo não atribui uso de IA ou ASReview sem evidência documental e declara a ausência de segundo avaliador independente. O verificador automático passou a conferir todos esses marcos.

Próxima ação: aguardar `AUTORIZO A ETAPA 7`.
