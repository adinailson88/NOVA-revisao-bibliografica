# RELATORIO DE SINTESE TEMATICA PRELIMINAR -- ETAPA_11

Gerado por `00_CONFIG/sintese_tematica_preliminar.py`, a partir do nucleo analitico revisado da ETAPA_10 (`05_ANALISE_R/tabelas/matriz_nucleo_analitico_revisado.csv`, coluna `nucleo_analitico_revisado == TRUE`, 3678 registros), enriquecido com autores/fonte/tipo de documento/resumo/palavras-chave de `03_PROCESSADOS/corpus_consolidado.csv`.

## 1. Escopo e limite desta etapa

Esta etapa trabalha somente com titulo, resumo e palavras-chave -- nao houve leitura de texto completo (PDF) de nenhum dos 3678 registros do nucleo. Por isso, as colunas da matriz de extracao que dependem de leitura de texto completo (`pais_contexto`, `tipo_aplicacao`, `dados_utilizados`, `resultado_principal`, `contribuicao_para_artigo`, `lacuna_identificada`, `criterios_*`, `uso_no_artigo`) foram preenchidas com o valor fixo `pendente_leitura_completa` em todos os registros -- nao inventadas nem inferidas do resumo. A coluna `necessita_leitura_completa` esta `sim` para os 3678 registros. Esta etapa nao decide inclusao/exclusao final no artigo nem redige texto do artigo.

## 2. Correspondencia com a matriz de extracao do roteiro-mestre (secao 14)

A matriz gerada nesta etapa reaproveita os nomes de coluna ja usados no pipeline operacional (`bloco_a_presente`, `bloco_b_presente` etc., ETAPA_07/09/10) em vez dos nomes originais do roteiro (`objeto_predial`, `dimensao_sustentabilidade` etc.) -- ver `ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt`, secao 26.4, que ja documenta essa divergencia de nomenclatura entre o roteiro-mestre e o pipeline real. Correcao de digitacao aplicada conforme secao 26.5 do roteiro: coluna `usa_topsis` (nao `usa_topis`). A coluna `strings_origem` do roteiro existe em `corpus_consolidado.csv` no nivel do registro consolidado (uma string por registro, apos deduplicacao) -- nao no nivel de string de busca original por base; rastreabilidade por string bruta fica em `01_PROTOCOLO` e `02_DADOS_BRUTOS`.

## 3. Eixo tematico preliminar

Rotulo unico por registro, calculado por prioridade (documentada para permitir reproducao): (1) decisao multicriterio (Bloco C ou metodo MCDM nomeado no titulo+resumo); (2) tecnologia aplicada (Bloco tecnologico: BIM, digital twin, IoT, data-driven, smart campus, predictive maintenance); (3) conceitual/biossistemico (Bloco conceitual: built environment, urban metabolism, biophilic, etc.); (4) contexto publico/universitario (Bloco D); (5) gestao predial e sustentabilidade geral (nenhum dos anteriores). Um mesmo registro pode ter mais de um sinal presente (ver colunas `bloco_c_presente`, `bloco_tecnologico_presente` etc., preservadas na matriz); o eixo preliminar so escolhe um rotulo dominante para tabulacao descritiva, pela ordem acima. Rotular um registro com metodo multicriterio dominante e apenas descricao do conteudo do resumo -- nao reintroduz MCDM/AHP/TOPSIS como objeto central do artigo (foco vigente: manutencao predial e gestao de edificacoes -- ver `00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md`).

| Eixo tematico preliminar | N registros | % do nucleo |
|---|---|---|
| gestao_predial_sustentabilidade_geral | 1689 | 45.9% |
| gestao_predial_com_tecnologia_aplicada | 872 | 23.7% |
| gestao_predial_com_decisao_multicriterio | 681 | 18.5% |
| gestao_predial_contexto_publico_universitario | 269 | 7.3% |
| gestao_predial_biossistemica_conceitual | 167 | 4.5% |

## 4. Metodos MCDM nomeados detectados (titulo+resumo)

| Metodo | N registros |
|---|---|
| MCDM/MCDA generico (sem metodo nomeado no titulo+resumo) | 559 |
| AHP | 84 |
| ANP | 20 |
| TOPSIS | 14 |
| BWM | 6 |
| DEMATEL | 4 |
| PROMETHEE | 2 |
| VIKOR | 2 |
| ELECTRE | 1 |

## 5. Tecnologias especificas detectadas (titulo+resumo)

| Tecnologia | N registros |
|---|---|
| BIM | 748 |
| IoT | 243 |
| Digital Twin | 219 |
| Data-driven | 137 |
| outra tecnologia: smart building | 106 |
| outra tecnologia: predictive maintenance | 84 |
| outra tecnologia: intelligent building | 46 |
| outra tecnologia: smart campus | 5 |
| outra tecnologia: campus infrastructure | 3 |

## 6. Sinal de tipo de edificacao (titulo+resumo)

Sinal preliminar, nao definitivo -- baseado em palavra-chave explicita em titulo+resumo, sujeito a leitura de texto completo posterior. Um mesmo registro pode ter mais de um sinal.

| Sinal | N registros |
|---|---|
| nao_identificado_por_resumo | 2267 |
| hospitalar/saude | 451 |
| universitario/campus | 408 |
| residencial | 381 |
| comercial/escritorio | 266 |
| publico_geral | 96 |
| escolar | 65 |
| industrial_predial | 17 |

## 7. Cobertura de resumo dentro do nucleo

0 de 3678 registros do nucleo (0.0%) estao sem resumo (`resumo_presente != sim`) -- para esses, a deteccao de metodo/tecnologia/tipo de edificacao desta etapa usou apenas o titulo, com cobertura de vocabulario proporcionalmente menor. Isso nao afeta a permanencia do registro no nucleo (decisao ja tomada na ETAPA_10), apenas reduz a granularidade da sintese tematica preliminar para esses casos.

## 8. Limites desta etapa

Deteccao por casamento de frases-chave em titulo+resumo, sem LLM para gerar achados -- mesmo metodo e mesmas limitacoes de falso positivo/negativo ja registradas para `00_CONFIG/pre_triagem.py`. `eixo_tematico_preliminar` e um rotulo dominante unico por prioridade fixa -- nao substitui os flags multi-label, que permanecem na matriz para quem precisar de outra prioridade. Nenhuma das colunas dependentes de leitura de texto completo foi preenchida (ver secao 1) -- essa e a fronteira explicita desta etapa, conforme instrucao vigente de nao iniciar leitura full-text nem escrita do artigo. Autores (`autores`) tem cobertura baixa no corpus consolidado (24,1% dos 9542 registros unicos, herdada da ETAPA_06) -- nao e falha desta etapa, e limite dos metadados recuperados na coleta.

## 9. Arquivos gerados

- `07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv` -- 1 linha por registro do nucleo.
- `07_SINTESE_TEMATICA/tabela_eixo_tematico_preliminar.csv`
- `07_SINTESE_TEMATICA/tabela_metodos_mcdm_especificos.csv`
- `07_SINTESE_TEMATICA/tabela_tecnologias_especificas.csv`
- `07_SINTESE_TEMATICA/tabela_tipo_edificacao_sinal.csv`
- `07_SINTESE_TEMATICA/relatorio_sintese_tematica_preliminar.md` -- este relatorio.
