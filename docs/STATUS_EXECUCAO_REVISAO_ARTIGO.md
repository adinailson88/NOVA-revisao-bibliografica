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
| 7 | Texto completo e elegibilidade | Concluída | Commit exclusivo da Etapa 7 e commit de regularização do verificador | Sem pendência bloqueante; decisão pendente sobre autorizar ou não a Rota B |
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


## Registro da Etapa 7

A avaliação de texto completo dos 104 estudos do núcleo final não ocorreu em nenhuma camada de triagem ou auditoria, o que já estava descrito por camada em `03_metodologia.tex`. Foi acrescentada uma declaração explícita de elegibilidade, incluindo o caso do registro sinalizado para verificação pontual e descartado sem leitura integral. Foi acrescentada uma limitação específica em `09_limitacoes.tex`, distinguindo análise documental de síntese de evidências de texto completo. Em `10_consideracoes.tex`, a expressão "confirma" foi substituída por uma formulação compatível com o nível documental de evidência. Foram apresentadas as Rotas A (manutenção em nível documental, adotada) e B (elevação para revisão sistemática com texto completo, não executada, com plano operacional descrito em `docs/RELATORIO_ETAPA_7.md`).

A execução de `scripts/python/verificar_artigo.py` revelou uma falha pré-existente, anterior a esta etapa (confirmada no commit `523f44f`, encerramento da Etapa 6): o script exigia exatamente 5 tabelas no artigo, mas há 8 tabelas presentes, todas elas legítimas e correspondentes a produtos criados durante as Etapas 2 a 6 (matriz de alinhamento, estratégia de busca, critérios de seleção, deduplicação e rastreabilidade do funil em `03_metodologia.tex`, além das tabelas de base/tipo, critérios de priorização e contexto de edificação nas Seções de resultados). A constante do script nunca havia sido atualizada conforme essas tabelas foram legitimamente adicionadas.


## Regularização do verificador automático (pós-Etapa 7)

Corrigidos, em commit próprio de regularização, dois problemas do próprio verificador — não do artigo:

1. A verificação de contagem de tabelas foi ajustada de 5 para 8, refletindo o número real e correto
   de tabelas do artigo (nenhuma tabela foi removida ou criada por essa correção).
2. A verificação da tabela redundante do funil (`"tab:funil" not in texto_tex`) gerava falso positivo,
   pois o rótulo atual e legítimo `tab:funilselecao` contém a substring `tab:funil`. A verificação foi
   ajustada para `"tab:funil}" not in texto_tex`, preservando a intenção original (impedir a
   reintrodução da antiga tabela redundante) sem acusar a tabela de rastreabilidade legítima.
3. A leitura de `04_TRIAGEM/decisao_duvidas_revisada.tsv` usava `delimiter="\\t"` (dois caracteres:
   barra invertida e "t"), que o módulo `csv` rejeita por não ser um único caractere; corrigido para
   `delimiter="\t"` (caractere de tabulação). Esse bug pré-existente impedia a conclusão de qualquer
   execução do verificador que chegasse a essa checagem.

Após as três correções, `python scripts/python/verificar_artigo.py` conclui sem divergências. Nenhum
número, tabela, figura, citação ou referência do artigo foi alterado nesta regularização.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Regularização da declaração de acesso a texto completo (pós-Etapa 7)

O pesquisador buscou, fora do escopo formal das etapas, obter texto completo dos 104 estudos por
acesso aberto legítimo (consulta à API pública do Unpaywall a partir dos DOIs do núcleo final). Dez
estudos tiveram PDF de acesso aberto obtido e validado; os demais permanecem sem texto completo
disponível por essa via, por ausência de versão aberta ou por dependerem de acesso institucional aos
periódicos. Nenhum desses PDFs foi lido ou incorporado à síntese do artigo até o momento; apenas os
arquivos foram obtidos e reservados fora do repositório.

Para refletir esse cenário sem antecipar procedimento não realizado, `03_metodologia.tex` e
`09_limitacoes.tex` foram ajustados para declarar que a síntese permanece predominantemente apoiada em
título, resumo, palavras-chave e campos estruturados, em razão do acesso institucional restrito a
parte dos periódicos, e que o eventual uso de texto completo do pequeno subconjunto obtido por acesso
aberto será indicado e referenciado individualmente por estudo, caso venha a ocorrer, sem alterar a
natureza predominantemente documental da revisão como um todo.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.


## Atualização do subconjunto com texto completo obtido (pós-Etapa 7)

Além dos dez estudos com PDF de acesso aberto obtido via Unpaywall, um cruzamento entre os títulos do
núcleo final e a biblioteca pessoal do pesquisador no Zotero identificou nove estudos adicionais com
texto completo disponível localmente, totalizando dezenove estudos do núcleo final com PDF acessível
(dezoito de fato mapeados e confirmados; um candidato de baixa confiança foi descartado por
inconsistência entre título e conteúdo do arquivo). Nenhum desses PDFs foi lido ou incorporado à
síntese do artigo até o momento; a leitura e a eventual incorporação, quando ocorrerem, serão
registradas e referenciadas individualmente por estudo, conforme já declarado em `03_metodologia.tex`
e `09_limitacoes.tex`.

Próxima ação: aguardar `AUTORIZO A ETAPA 8`.
