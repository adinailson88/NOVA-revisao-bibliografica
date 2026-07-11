# Relatório da Etapa 4

## Tabela de progresso

| Etapa | Situação |
|---|---|
| Etapa 1 | OK |
| Etapa 2 | OK |
| Etapa 3 | OK |
| Etapa 4 | OK |

## 1. Escopo executado

Auditoria e correção do funil 12.118 → 9.542 → 3.678 → 137 → 104, distinguindo deduplicação, automação, auditoria amostral, corte analítico, alinhamento às RQs e auditoria qualitativa.

## 2. Arquivos analisados

Metodologia, critérios, núcleo final, scripts de consolidação, pré-triagem, auditoria, corte analítico, reavaliação de resumos, alinhamento às RQs e documentos de protocolo.

## 3. Evidências encontradas

- Deduplicação: 2.576 ocorrências removidas.
- Pré-triagem: regras determinísticas em título e resumo.
- Auditoria da pré-triagem: amostra estratificada de 100 registros, semente 42, 34 ajustes, avaliador único.
- Corte: 3.678 registros retidos por classe e combinação de blocos.
- Alinhamento: 137 selecionados para análise central por regras determinísticas.
- Auditoria qualitativa: 104 mantidos no núcleo principal.
- Não houve texto completo nem segundo avaliador independente.

## 4. Problemas identificados

A redação anterior sugeria resolução individual de todos os casos de dúvida. Na realidade, somente 100 dos 9.542 registros foram auditados individualmente. Os relatórios intermediários gerados pelo pipeline não estão presentes no repositório atual, embora os scripts estejam.

## 5. Alterações realizadas

A metodologia foi reescrita para explicitar cada transição. Foi inserida tabela completa com entrada, procedimento, critério, responsável, incluídos, não retidos e motivos. A figura do funil foi corrigida.

## 6. Alterações não realizadas

Nenhum total do funil foi modificado. Não foi declarada elegibilidade por texto completo, dupla revisão ou auditoria humana integral.

## 7. Informação insuficiente para verificar

A distribuição completa das 3.541 classificações fora da análise central não pode ser reconstituída sem os arquivos intermediários. Os relatórios intermediários originais precisam ser incorporados ao repositório.

## 8. Validações executadas

- 12.118 − 2.576 = 9.542.
- 9.542 − 5.864 = 3.678.
- 3.678 − 3.541 = 137.
- 137 − 33 = 104.
- 21 + 3 + 8 + 1 = 33.
- Núcleo final contém 104 linhas, todas com decisão `manter_nucleo_principal`.
- REG_07264 não está no núcleo final.

## 9. Arquivos alterados

- `latex-artigo/sections/03_metodologia.tex`
- `docs/RELATORIO_ETAPA_4.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Commit exclusivo da Etapa 4, com hash informado ao usuário.

## 11. Pendências

Incorporar, se disponíveis, relatórios e matrizes intermediárias de `03_PROCESSADOS/`, `04_TRIAGEM/`, `05_ANALISE_R/` e `07_SINTESE_TEMATICA/`.

## 12. Próxima etapa prevista

Etapa 5 — Deduplicação.

Execução interrompida conforme o planejamento. Aguardando autorização expressa para prosseguir.
