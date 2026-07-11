# Relatório da Etapa 5

## Tabela de progresso

| Etapa | Situação |
|---|---|
| Etapa 1 | OK |
| Etapa 2 | OK |
| Etapa 3 | OK |
| Etapa 4 | OK |
| Etapa 5 | OK |

## 1. Escopo executado

Auditoria da normalização de DOI e título, agrupamento, conflitos, proveniência, registros sem DOI, versões relacionadas e risco de duplicatas remanescentes.

## 2. Arquivos analisados

Script de consolidação, três produtos processados, relatório de deduplicação, metodologia e verificador automatizado do artigo.

## 3. Evidências encontradas

A deduplicação consolidou 12.118 ocorrências em 9.542 registros únicos, removendo 2.576 ocorrências em 1.808 grupos. Foram 1.635 grupos com DOI e 173 apenas por título. Noventa e oito conflitos foram preservados sem fusão.

## 4. Problemas identificados

A rotina não usa similaridade aproximada nem estabelece vínculo automático entre evento e artigo posterior. Os 98 conflitos detectados foram preservados como registros separados.

## 5. Alterações realizadas

Foi inserida especificação detalhada na metodologia, criado documento técnico e ampliado o verificador automático para conferir contagens, critérios, IDs, DOI único e proveniência.

## 6. Alterações não realizadas

A lógica de deduplicação não foi modificada. Nenhum grupo foi fundido ou separado nesta etapa.

## 7. Informação insuficiente para verificar

Nenhuma informação adicional foi necessária para descrever o procedimento executado.

## 8. Validações executadas

- 12.118 − 9.542 = 2.576.
- Soma de `n_registros_agrupados − 1` = 2.576.
- 1.616 + 19 + 173 = 1.808.
- IDs únicos e DOI normalizado único no corpus consolidado.
- Proveniência obrigatória por base, string e IDs brutos.
- Distribuição dos tamanhos dos grupos conferida.

## 9. Arquivos alterados

- `latex-artigo/sections/03_metodologia.tex`
- `scripts/python/verificar_artigo.py`
- `docs/ESPECIFICACAO_DEDUPLICACAO.md`
- `docs/RELATORIO_ETAPA_5.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Commit exclusivo da Etapa 5, com hash informado ao usuário.

## 11. Pendências

Sem pendência operacional para a Etapa 5.

## 12. Próxima etapa prevista

Etapa 6 — Triagem e auditoria dos registros.

Execução interrompida conforme o planejamento. Aguardando autorização expressa para prosseguir.
