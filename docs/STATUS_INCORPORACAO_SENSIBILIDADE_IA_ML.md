# Status — Incorporação da busca de sensibilidade IA/ML ao núcleo do artigo

Arquivo único e cumulativo de continuidade para esta tarefa. Qualquer sessão futura (neste
computador ou em outro) deve **atualizar as seções abaixo**, não criar um novo arquivo de
status paralelo. Segue o mesmo padrão de `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md` (que
documenta um fluxo de trabalho anterior e independente, na branch `revisao-metodologica-controlada`
— não confundir os dois).

## Repositório e branch

- URL: https://github.com/adinailson88/NOVA-revisao-bibliografica
- Branch de trabalho: `agent/incorporacao-busca-sensibilidade-ia`
- Branch de origem (fork point): `agent/bibliometria-ampliada-pages`
- Último commit nesta tarefa: `3df7a3c11bf81c8bca536f09bdc018a68b0bf21d` (2026-07-12)
- Nenhum PR foi aberto. Nenhuma alteração foi feita na `main`.
- Clone local de trabalho usado nesta sessão: `C:\Users\adina\AppData\Local\Temp\nova-revisao`
  (fora do repositório do artigo em si — recriar com `git clone` se necessário em outra máquina).

## Objetivo da tarefa

Incorporar ao artigo os resultados de uma busca complementar de **sensibilidade para
inteligência artificial (IA) e aprendizado de máquina**, já executada manualmente pelo usuário
fora deste ambiente (Scopus, Web of Science, Crossref), porque a busca original do núcleo
capturou IA/ML apenas incidentalmente. Nenhuma nova busca foi executada nesta tarefa.

## Regras fixas desta tarefa (memória do projeto + decisões do usuário nesta sessão)

- Nunca registrar em arquivos do projeto que algo foi "feito/auditado por IA" — relatórios
  descrevem o *processo* (ex. "classificação por correspondência de termos"), nunca atribuem
  autoria a IA.
- Scripts **Python**: escritos e executados diretamente nesta sessão.
- Scripts **R**: **não escritos nem executados** nesta sessão, por regra do projeto. Um prompt
  para execução via Codex foi preparado (`docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md`),
  mas os artefatos dessa execução nunca foram commitados na branch. **Decisão do usuário
  (2026-07-12, sessão de continuação)**: em vez de insistir na execução R, a lógica de
  `scripts/r/10_gerar_produtos_artigo.R` foi **recriada em Python**
  (`scripts/python/gerar_produtos_artigo_nucleo_ampliado.py`), replicando termo a termo as
  mesmas regras de agregação/rotulagem. Isso resolveu o bloqueio sem violar a regra "sem R".
- Não forçar os números antigos do núcleo (104/137/372) — os novos totais saem do dado real,
  mesmo quando o crescimento é pequeno (o núcleo cresceu para 121, não para milhares, depois de
  duas recalibrações do critério de triagem — ver "Decisões de calibração" abaixo).
- Não declarar sucesso com erro de compilação ou divergência numérica — `verificar_artigo.py`
  deve passar sem divergências antes de qualquer relatório de conclusão.

## Estado atual: TAREFA CONCLUÍDA NESTA RODADA

Todas as fases previstas (organização dos dados brutos → normalização → deduplicação →
codebook/RQ6 → auditoria de classe IA/ML → triagem → reavaliação de 7 registros → consolidação
do corpus → geração de produtos derivados → atualização do texto LaTeX → validação →
compilação) foram executadas e commitadas. Resumo verificável nos commits (`git log --oneline`
na branch) e nos relatórios listados na seção seguinte.

## Números finais (para referência rápida sem precisar reler os relatórios)

| Métrica | Valor |
|---|---|
| Núcleo original | 104 registros |
| **Núcleo ampliado (atual)** | **121 registros** (+17) |
| Bruto da busca de sensibilidade | 6.728 (3.169 Scopus + 1.559 WoS + 2.000 Crossref) |
| Já existiam no corpus original | 359 |
| Novos únicos auditados (classe IA/ML) | 4.889 (100%, sem amostragem) |
| Núcleo da sensibilidade (após revisão manual) | 12 |
| Secundários da sensibilidade | 289 |
| Registros REG_ promovidos na reavaliação dos 7 | 5 (de 7) |
| Método "machine learning" no núcleo | 9 → 26 (achado central) |

## Arquivos-chave desta tarefa (para retomar rapidamente)

- `docs/CODEBOOK_SENSIBILIDADE_IA_ML.md` — regras de classificação de IA/ML (RQ6).
- `docs/REAVALIACAO_7_REGISTROS_SENSIBILIDADE.md` — decisão registro a registro dos 7 REG_.
- `docs/PROMPT_R_REEXECUCAO_PIPELINE_SENSIBILIDADE.md` — prompt originalmente preparado para
  Codex (não usado ao final; substituído pela reimplementação em Python).
- `docs/RELATORIO_EXECUCAO_R_NUCLEO_AMPLIADO.md` — comparativo completo 104 vs 121, geração dos
  produtos derivados.
- `04_TRIAGEM/relatorio_triagem_sensibilidade.md` — funil de triagem, incluindo a correção
  manual dos 8 falsos positivos de contexto (indústria/aeroespacial/veicular).
- `03_PROCESSADOS/relatorio_deduplicacao_sensibilidade.md`, `relatorio_normalizacao_sensibilidade_ia.md`,
  `relatorio_auditoria_ia_ml.md` — relatórios de cada etapa de processamento.
- `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos_v2_sensibilidade.csv` — o núcleo de
  121 registros vigente (o arquivo original de 104 permanece preservado, sem sobrescrita).
- `scripts/python/gerar_produtos_artigo_nucleo_ampliado.py` — reimplementação Python do script R,
  gera tabela26–36 e figura09/11/12/13/14 com sufixo `_nucleo_ampliado_121`.
- `scripts/python/verificar_artigo.py` — atualizado para ler o núcleo de 121; passa sem
  divergências.

## Decisões de calibração (importante para não repetir o mesmo erro)

A triagem automática de núcleo passou por duas correções nesta sessão:

1. **Primeira versão**: usava só detecção lexical de "maintenance" → gerou 2.484 falsos
   candidatos a núcleo (24x o núcleo original). Corrigida reaproveitando a lógica real de
   Bloco A (objeto predial) + Bloco B (sustentabilidade) de `scripts/python/pre_triagem.py`
   (o mesmo critério que gerou a classe "relevante" no corpus original) combinada com a classe
   de IA/ML já auditada → gerou 20 candidatos.
2. **Segunda correção (revisão manual)**: dos 20 candidatos, 8 eram falsos positivos de
   contexto (IA/ML confirmada + termo "maintenance" presente, mas em domínio industrial,
   aeroespacial ou veicular sem nenhuma ponte predial real — ex. manutenção preditiva de
   maquinário de manufatura, bombas moleculares de instalação de fusão nuclear, estações de
   recarga veicular). Removidos manualmente após leitura do resumo completo de cada um →
   núcleo final de 12 da sensibilidade.

**Lição para sessões futuras**: qualquer novo critério de triagem automática para este corpus
deve ser testado contra a ordem de grandeza esperada (núcleo original é ~1% do corpus
consolidado) antes de aceitar o resultado como final.

## Pendências conhecidas (não bloqueantes)

- **`artigo.docx`** não foi regenerado localmente nesta sessão por ausência de Pandoc no
  ambiente. Será regenerado automaticamente pelo workflow de CI (`.github/workflows/latex.yml`)
  no próximo push que não tenha `[skip ci]`.
- **CI de regeneração automática** (`CI: atualiza tabelas, graficos, PDF e Word [skip ci]`) roda
  a cada push e usa o script R **original** (`10_gerar_produtos_artigo.R`, focado no núcleo de
  104) para os produtos que ele já gerava antes (figuras `_372`, `referencias/*.xlsx`) — isso é
  **esperado e inofensivo**: esses produtos não fazem parte do escopo desta tarefa (núcleo
  ampliado) e o CI não sabe gerar os artefatos `_nucleo_ampliado_121` (esses só existem via o
  script Python desta tarefa). Se o CI abrir conflito de merge em `main.pdf` num push futuro,
  resolver mantendo a versão local mais recente (`git checkout --ours main.pdf`), pois o CI
  roda com os LaTeX sources do momento do push anterior e pode ficar defasado em relação a
  edições feitas na mesma sessão após o push que o disparou.
- **Merge/push**: sempre `git fetch` + checar `git log HEAD..origin/<branch>` antes de dar push,
  porque o CI cria commits automáticos na mesma branch a cada push. Isso já aconteceu duas vezes
  nesta sessão (commits `b0d89c8` e `1a43b5d`) e exigiu merge manual do `main.pdf`.
- **Tabela de estratégia de busca** (`latex-artigo/fontes/tabela_estrategia_busca.csv`,
  referenciada por `03_metodologia.tex` e por `verificar_artigo.py`) **não foi atualizada** com
  as consultas da busca de sensibilidade — permanece com os 12.118 registros/13 consultas
  originais. A busca de sensibilidade é descrita separadamente, em prosa, na nova Seção 3.5
  (`sec:buscaia`). Se uma tarefa futura decidir unificar as duas tabelas, isso exigirá também
  atualizar as asserções correspondentes em `verificar_artigo.py`.

## Como retomar em outra máquina

```bash
git clone https://github.com/adinailson88/NOVA-revisao-bibliografica.git
cd NOVA-revisao-bibliografica
git checkout agent/incorporacao-busca-sensibilidade-ia
python scripts/python/verificar_artigo.py   # deve passar sem divergencias
cd latex-artigo && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Requer: Python 3 com `matplotlib` (para `gerar_produtos_artigo_nucleo_ampliado.py`, só necessário
se for preciso regenerar tabelas/figuras), MiKTeX/TeXLive com `biblatex-abnt` e `latexmk`.

## Próxima ação sugerida

Nenhuma pendência bloqueante para o estado atual do artigo. Ações possíveis para uma próxima
sessão, se desejado pelo usuário:
1. Regenerar `artigo.docx` num ambiente com Pandoc.
2. Decidir se a tabela de estratégia de busca deve incorporar as consultas de sensibilidade.
3. Considerar leitura de texto completo pontual dos 17 novos registros do núcleo (mesmo padrão
   já aplicado aos 30 estudos do núcleo original — ver `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`),
   caso o usuário autorize essa tarefa fora do escopo documental desta rodada.
