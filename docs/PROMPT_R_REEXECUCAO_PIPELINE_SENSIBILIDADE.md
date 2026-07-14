# PROMPT PARA CODEX — Reexecução do pipeline R com o núcleo ampliado (busca de sensibilidade IA/ML)

Este documento é o prompt a ser executado externamente (via Codex, não pela sessão Claude que
preparou este pacote — regra do projeto: scripts R não são escritos nem executados por esta
sessão). Copie o conteúdo abaixo para o Codex, apontando para o repositório
`NOVA-revisao-bibliografica`, branch `agent/incorporacao-busca-sensibilidade-ia`.

---

## PROMPT

Você está no repositório `NOVA-revisao-bibliografica`, branch
`agent/incorporacao-busca-sensibilidade-ia`. Um novo núcleo ampliado de estudos foi extraído
qualitativamente (mesma extração de dimensões/critérios/métodos/contexto do núcleo original)
e está em:

```
latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv
```

Esse arquivo tem **121 registros** (os 104 originais + 17 novos vindos da busca de
sensibilidade de IA/ML), no **mesmo schema exato** de
`latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv` (26 colunas idênticas).

### O que fazer

1. **Não sobrescreva os arquivos de saída existentes** (`tabela26_...` a `tabela36_...` e
   `figura09_...` a `figura14_...` em `latex-artigo/fontes/` e `latex-artigo/figuras/`) — eles
   ainda são os produtos válidos do núcleo de 104 registros até a validação humana desta
   rodada estar concluída.

2. Crie uma **cópia modificada** de `scripts/r/10_gerar_produtos_artigo.R` chamada
   `scripts/r/10b_gerar_produtos_artigo_nucleo_ampliado.R` com as seguintes alterações
   mínimas em relação ao original:
   - `ARQUIVO_NUCLEO <- "latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv"`
     (em vez do arquivo de 104 registros).
   - A checagem `if (nrow(dados) != 104L) stop(...)` deve virar
     `if (nrow(dados) != 121L) stop("O nucleo ampliado deve conter exatamente 121 registros.")`.
   - Todos os caminhos de saída (tabelas e figuras) devem receber o sufixo
     `_nucleo_ampliado_121` no lugar de `_nucleo_final_104` (ex.:
     `tabela26_criterios_nucleo_final_104.csv` → `tabela26_criterios_nucleo_ampliado_121.csv`;
     `figura09_distribuicao_temporal_nucleo_final_104.png` →
     `figura09_distribuicao_temporal_nucleo_ampliado_121.png`), preservando os mesmos diretórios
     (`latex-artigo/fontes/` e `latex-artigo/figuras/`).
   - `ARQUIVO_TIPOS_ORIGINAIS` deve apontar para um novo arquivo de distribuição base×tipo do
     núcleo ampliado — se esse arquivo ainda não existir, gere-o a partir da mesma lógica usada
     para o de 104 registros (contagem de `bases_origem` × `tipo_documento` dos 121 registros).
   - Mantenha `ARQUIVO_DICIONARIO` e `ARQUIVO_BUSCAS` iguais (não mudam nesta rodada — a
     estratégia de busca é atualizada em etapa separada, ver seção "Pendências" abaixo).

3. Execute: `Rscript scripts/r/10b_gerar_produtos_artigo_nucleo_ampliado.R`. Corrija erros de
   execução mantendo a mesma lógica estatística/de agregação do script original (não altere
   fórmulas, thresholds ou definições de dimensão/critério — apenas os caminhos de entrada/saída
   e a checagem de contagem, conforme item 2).

4. Depois de rodar com sucesso, gere um relatório curto (`docs/RELATORIO_EXECUCAO_R_NUCLEO_AMPLIADO.md`)
   com: contagem final por tabela/figura gerada, e uma comparação lado a lado das principais
   métricas entre o núcleo de 104 e o núcleo ampliado de 121 (ex.: distribuição de dimensões,
   distribuição temporal, métodos mais frequentes — para o revisor humano decidir se os novos 17
   registros mudam substancialmente as conclusões do artigo antes de promovê-los ao texto final).

5. Commit desses novos arquivos (script `10b_...R`, tabelas/figuras `_nucleo_ampliado_121`,
   e o relatório) na mesma branch `agent/incorporacao-busca-sensibilidade-ia`, com mensagem
   clara (ex. `"analise: reexecuta pipeline R com nucleo ampliado de 121 registros"`). **Não
   sobrescreva nem apague nenhum arquivo `_nucleo_final_104` existente.**

6. **Não** abra pull request. Push apenas para a branch já indicada.

### Pendências que ficam FORA deste prompt (tratadas em outra etapa)

- A tabela `tabela_estrategia_busca.csv` (usada por `verificar_artigo.py` para conferir o total
  bruto de 12.118 registros e o número de consultas por base) ainda não inclui as consultas da
  busca de sensibilidade — isso será atualizado depois que o núcleo ampliado for validado
  humanamente, não nesta rodada de execução R.
- A promoção do núcleo ampliado de 121 para os arquivos "oficiais" (substituindo os de 104) e a
  atualização do texto LaTeX com os novos números **não devem ser feitas automaticamente** —
  aguardam decisão humana após comparar os relatórios desta rodada.

---

## Contexto para quem for revisar o resultado

- Núcleo original: 104 estudos.
- 17 novos estudos vieram da busca de sensibilidade de IA/ML (2026-07-12): 12 identificados
  diretamente na triagem (`04_TRIAGEM/sensibilidade_triagem_final.csv`, decisão `nucleo`) + 5
  registros já existentes no corpus, reavaliados e promovidos
  (`docs/REAVALIACAO_7_REGISTROS_SENSIBILIDADE.md`).
- Todos os 17 passaram pelo mesmo critério do núcleo original (Bloco A "objeto predial" + Bloco B
  "sustentabilidade" de `scripts/python/pre_triagem.py`), mais a confirmação de aplicação de IA/ML
  (RQ6, `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md`), e passaram por revisão manual de título/resumo
  (não amostragem) que já removeu 8 candidatos sem ponte predial real (equipamento industrial,
  aeroespacial, veicular — ver `04_TRIAGEM/relatorio_triagem_sensibilidade.md`).
- A extração qualitativa dos 17 (dimensões/critérios/métodos/contexto) foi feita manualmente,
  registro por registro, seguindo o vocabulário fechado de
  `docs/CODEBOOK_CATEGORIAS_ETAPA_8.md` — ver `scripts/python/extrair_qualitativo_novos_nucleo.py`
  para a extração e justificativa completa de cada um.
