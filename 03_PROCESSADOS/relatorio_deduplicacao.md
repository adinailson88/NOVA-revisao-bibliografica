# RELATORIO DE DEDUPLICACAO -- ETAPA_06

Gerado por `00_CONFIG/consolidar_deduplicar.py`. Todos os numeros abaixo sao derivados diretamente dos arquivos em `02_DADOS_BRUTOS/` e podem ser reproduzidos executando o script novamente.

## 1. Volume bruto por base (entrada)

| Base | Registros brutos lidos |
|---|---|
| Scopus | 9438 |
| Crossref | 1000 |
| Web of Science | 1680 |
| **Total bruto** | **12118** |

Nota: o total acima ja inclui o enriquecimento por export manual do site da Scopus (`SCOPUS_A{1,2,3,4}_*.csv`, com resumo, coletado em 2026-07-09) -- ver secao 4.1. Os 4 CSVs antigos (`SCOPUS_NUCLEO_01-04_20260708_part01.csv.csv`, string incorreta com MCDM/ESG obrigatorio) continuam fora de uso -- ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`.

## 2. Metodo de deduplicacao

Conforme `01_PROTOCOLO/protocolo_busca_reprodutivel.md`, secao 7:
1. **DOI normalizado** (minusculo, sem prefixo `https://doi.org/`, sem ponto final) = duplicata forte. Todos os registros com o mesmo DOI normalizado sao agrupados.
2. **Titulo normalizado** (minusculo, sem acentos/pontuacao, espacos colapsados, minimo 8 caracteres) = duplicata provavel. Registros com o mesmo titulo normalizado sao agrupados, **desde que nao haja DOIs diferentes e ambos presentes no grupo** -- nesse caso de conflito, os registros NAO sao mesclados automaticamente e ficam listados na secao 5 para revisao manual (nunca apagar duplicata sem preservar proveniencia).
3. Proveniencia preservada em `bases_origem`, `strings_origem` e `ids_brutos_agrupados` no arquivo `corpus_consolidado.csv`.

## 3. Resultado da deduplicacao

| Metrica | Valor |
|---|---|
| Registros brutos (entrada) | 12118 |
| Registros unicos (corpus_consolidado.csv) | 9542 |
| Registros removidos por duplicacao | 2576 |
| Grupos com mais de 1 registro bruto | 1808 |
| Grupos fundidos por DOI (com ou sem reforco de titulo) | 1635 |
| Grupos fundidos apenas por titulo normalizado (sem DOI em nenhum membro) | 173 |

## 4. Cobertura de DOI e resumo

| Metrica | Bruto (antes da dedup) | Apos dedup (corpus_consolidado.csv) |
|---|---|---|
| Com DOI | 10576 | 8264 |
| Sem DOI | 1542 | 1278 |
| Com resumo (apos escolha do melhor entre fontes) | - | 8976 |
| Sem resumo | - | 566 |

Registros unicos sem resumo nao foram excluidos nesta etapa (regra da secao 7 do protocolo: nao excluir automaticamente antes de enriquecimento). Ficam marcados por `resumo_presente=nao` para tratamento na triagem (ETAPA seguinte).

### 4.1 Enriquecimento manual do resumo da Scopus (2026-07-09)

A coleta via API da Scopus (view=STANDARD) nao traz resumo. Corrigido nesta rodada com export manual do site da Scopus (com Abstract incluido), casado por EID com os registros da API -- ver `00_CONFIG/consolidar_deduplicar.py::ler_scopus()` e `00_CONTROLE/DECISOES_METODOLOGICAS.md`.

- Registros brutos de Scopus com resumo vindo do enriquecimento manual: 9341 de 9438.
- Registros encontrados apenas no export manual, ausentes na coleta via API (drift normal de indice entre datas de coleta diferentes -- adicionados ao corpus): 5.
- Registros unicos do corpus consolidado marcados `resumo_enriquecido_manualmente=sim`: 8141 de 9542.

## 5. Conflitos de titulo identico nao mesclados automaticamente

Foram encontrados 98 grupo(s) de titulo normalizado identico que **nao foram fundidos automaticamente** (permanecem como entradas separadas em `corpus_consolidado.csv`), por dois motivos possiveis: 51 com DOIs diferentes no mesmo grupo, e 47 com identificador proprio da fonte diferente (eid da Scopus ou accession number da WoS) dentro da mesma base -- caso tipico de titulos genericos de volume/serie ("Book Series", proceedings) compartilhados por itens distintos. Revisao manual recomendada:

- titulo_norm: `development of condition based maintenance for sugar mill assets` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00131, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00646, WOS::WOS_NUCLEO_01_20260708_part01.ris::00392
- titulo_norm: `energy quality management` | motivo: doi_diferente | DOIs: 10.1016/b978-0-12-809597-3.00521-6, 10.1016/b978-0-44-313219-3.00076-9 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00166, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00329, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::05881
- titulo_norm: `1st geomeast international congress and exhibition on sustainable civil infrastructures egypt 2017` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00182, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00183, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00186, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00187, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00188, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00189, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00190, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00191, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00194, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00195, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00196, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00197, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00199, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00201, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00202, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00658, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00659, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00660, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00661, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00662, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00663, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00664, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00665, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00666, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00667, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00668, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00669, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00670, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00671, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00672
- titulo_norm: `sustainability` | motivo: doi_diferente | DOIs: 10.1002/9781118426470.ch8, 10.1002/9781119572626.ch8, 10.1515/energyo.0095.00002, 10.2307/jj.10286089.12 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00185, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00655, CROSSREF::crossref_nucleo_a1_raw.csv::00049, CROSSREF::crossref_nucleo_a1_raw.csv::00052, CROSSREF::crossref_nucleo_a1_raw.csv::00053, CROSSREF::crossref_nucleo_a2_raw.csv::00011, WOS::WOS_NUCLEO_01_20260708_part01.ris::00560
- titulo_norm: `bim implementation in facilities management an analysis of implementation processes` | motivo: identificador_fonte_diferente | DOIs: 10.1061/9780784481264.071 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00211, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00500
- titulo_norm: `direction of research and development of life cycle maintenance` | motivo: identificador_fonte_diferente | DOIs: 10.53829/ntr201801fa1 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00251, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::07280
- titulo_norm: `innovative and sustainable operation and maintenance of bridges` | motivo: doi_diferente | DOIs: 10.1080/15732479.2019.1604772, 10.1201/9781315189390-8 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00275, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::03842, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00557, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00678, WOS::WOS_NUCLEO_04_20260708_part01.ris::00205
- titulo_norm: `bim as a tool for sustainable design` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00307, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::04444
- titulo_norm: `the practice of sustainable facilities management design sentiments and the knowledge chasm` | motivo: doi_diferente | DOIs: 10.3763/aedm.2009.0909, 10.4324/9781315065991-9 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00416, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00541
- titulo_norm: `sustainable urban facilities management` | motivo: doi_diferente | DOIs: 10.1016/b978-0-12-409548-9.10183-6, 10.1016/b978-0-323-90386-8.00161-3 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00423, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::06567
- titulo_norm: `building information modeling and building performance optimization` | motivo: doi_diferente | DOIs: 10.1016/b978-0-12-409548-9.10200-3, 10.1016/b978-0-323-90386-8.00109-1 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00424, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::06507, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00311
- titulo_norm: `high integrity pressure protection system hipps and implementation challenges` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00606, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00607
- titulo_norm: `design for safety knowledge based bim integrated risk register system` | motivo: identificador_fonte_diferente | DOIs: 10.14455/isec.res.2017.46 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00616, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00617
- titulo_norm: `showhow a flexible structured approach to commit university stakeholders to sustainable development` | motivo: doi_diferente | DOIs: 10.1007/978-3-319-47877-7_33, 10.1007/978-3-319-47877-7_33 10.1007/978-3-319-47877-7 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00621, WOS::WOS_NUCLEO_01_20260708_part01.ris::00507, WOS::WOS_NUCLEO_02_20260708_part01.ris::00319
- titulo_norm: `socioeconomic environmental and social impacts of a concentrated solar power energy project in northern chile` | motivo: identificador_fonte_diferente | DOIs: 10.1007/978-3-319-30746-6_68 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00623, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00801
- titulo_norm: `the politics of water payments and stakeholder participation in the limpopo river basin mozambique` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00664, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00740
- titulo_norm: `sustainable energy campus a challenge on smart facilities and operations` | motivo: doi_diferente | DOIs: 10.1007/978-3-319-47895-1_15, 10.1007/978-3-319-47895-1_15 10.1007/978-3-319-47895-1 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00683, WOS::WOS_NUCLEO_02_20260708_part01.ris::00316
- titulo_norm: `a new green index as an overall quantitative green performance indicator of a facility` | motivo: doi_diferente | DOIs: 10.1007/s10098-016-1182-3, 10.3303/cet1545075 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00731, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01042, WOS::WOS_NUCLEO_01_20260708_part01.ris::00028
- titulo_norm: `diagnostics and life cycle assessment of medium voltage cables in nuclear power plants during regular overhaul process` | motivo: identificador_fonte_diferente | DOIs: 10.1115/1.4032782 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00734, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01212
- titulo_norm: `operations and maintenance for whole school sustainability` | motivo: doi_diferente | DOIs: 10.4324/9781315880525, 10.4324/9781315880525-7 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00758, CROSSREF::crossref_nucleo_a1_raw.csv::00128
- titulo_norm: `life cycle costs any use` | motivo: identificador_fonte_diferente | DOIs: 10.2749/222137814814069615 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00884, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01438, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00739
- titulo_norm: `introduction` | motivo: doi_diferente | DOIs: 10.1007/978-81-322-2722-9_1, 10.1201/9780429001055-1, 10.1201/9781003357483-1 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00926, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::04353, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::07425, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00752
- titulo_norm: `facility integrity learnings from the equipment lifecycle` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00968, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::00969
- titulo_norm: `facility management variables that influence sustainability of building facilities` | motivo: identificador_fonte_diferente | DOIs: 10.11113/jt.v75.5270 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01057, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01169, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00767, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00781, CROSSREF::crossref_nucleo_a2_raw.csv::00007, WOS::WOS_NUCLEO_04_20260708_part01.ris::00043, WOS::WOS_NUCLEO_04_20260708_part01.ris::00044
- titulo_norm: `a study on soundness evaluation and rational maintenance for mountain tunnels` | motivo: identificador_fonte_diferente | DOIs: 10.1201/b17618-94 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01196, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01453
- titulo_norm: `analysis of sustainable maintenance behaviors in housing operation` | motivo: identificador_fonte_diferente | DOIs: 10.14455/isec.res.2015.39 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01259, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01273
- titulo_norm: `australia s first build own operate csg produced water treatment and beneficial reuse project` | motivo: identificador_fonte_diferente | DOIs: 10.2118/174991-ms | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01285, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01309
- titulo_norm: `reflecting on future research concerning the added value of fm` | motivo: doi_diferente | DOIs: 10.1108/f-04-2013-0070, 10.1108/f-09-2012-0070 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01345, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01346
- titulo_norm: `4th international conference on civil engineering architecture and building materials ceabm 2014` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01414, SCOPUS::scopus_nucleo_a2_contexto_publico_universitario_raw.csv::00391, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00818
- titulo_norm: `social enterprise applications in an urban facilities management setting` | motivo: identificador_fonte_diferente | DOIs: 10.1108/02632771311307106 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01723, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02267
- titulo_norm: `pdo s journey of process control optimisation a look back to the 15 years of existence of the pco team challenges achiev` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01784, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01786
- titulo_norm: `industry based skills standards for building operators a business case` | motivo: identificador_fonte_diferente | DOIs: 10.1080/10485236.2013.10596285 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01810, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02106
- titulo_norm: `proactive sewer planning in colombia plan and prioritization for cleaning and cctv inspection of the medellin sewer syst` | motivo: identificador_fonte_diferente | DOIs: 10.2175/193864713813674162 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01825, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01829, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01841
- titulo_norm: `electrical integration and interface management` | motivo: doi_diferente | DOIs: 10.1049/ic.2010.0101, 10.1049/ic.2012.0057 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01936, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02313
- titulo_norm: `sustainability in multi tenant office buildings anatomy of a leed ebom program` | motivo: identificador_fonte_diferente | DOIs: 10.1080/01998595.2012.10483744 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::01997, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02258
- titulo_norm: `the first functional safety management system tuv certified in americas` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02113, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02245
- titulo_norm: `a new concept for a plm process in steam turbine service business` | motivo: doi_diferente | DOIs: 10.1515/zwf-2011-1061112, 10.3139/104.110659 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02124, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02231
- titulo_norm: `designing energy efficient buildings a methodological approach based on computer simulation` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02207, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02240, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00886, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00895
- titulo_norm: `industrial wastewater reuse applications in romania` | motivo: doi_diferente | DOIs: 10.1007/978-94-007-1805-0_15, 10.1007/978-941-0074805-0_15 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02244, WOS::WOS_NUCLEO_01_20260708_part01.ris::00505
- titulo_norm: `water services in south africa 1994 2009` | motivo: doi_diferente | DOIs: 10.1007/978-90-481-9367-7_3, 10.1007/978-90-481-9367-7_3 10.1007/978-90-481-9367-7 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02254, WOS::WOS_NUCLEO_01_20260708_part01.ris::00587
- titulo_norm: `time variant reliability analysis for rocksalt energy storage caverns based on creep behavior` | motivo: identificador_fonte_diferente | DOIs: (nenhum) | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02277, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02391
- titulo_norm: `pipeline rehabilitation systems for service life extension` | motivo: doi_diferente | DOIs: 10.1016/b978-1-84569-398-5.50010-9, 10.1533/9780857090928 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02295, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00898, WOS::WOS_NUCLEO_01_20260708_part01.ris::00499, WOS::WOS_NUCLEO_04_20260708_part01.ris::00436
- titulo_norm: `lca based environmental assessment of the use and maintenance of heating and ventilation systems in dutch dwellings` | motivo: identificador_fonte_diferente | DOIs: 10.1016/j.buildenv.2010.04.012 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02299, SCOPUS::scopus_nucleo_a4_gestao_ativos_ciclo_vida_raw.csv::00899, WOS::WOS_NUCLEO_04_20260708_part01.ris::00125, WOS::WOS_NUCLEO_04_20260708_part01.ris::00126
- titulo_norm: `a structured approach to process safety management` | motivo: doi_diferente | DOIs: 10.2118/126445-ms, 10.2523/126445-ms | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02384, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02385
- titulo_norm: `improving building energy footprint and asset performance using digital twin technology` | motivo: doi_diferente | DOIs: 10.1016/j.ifacol.2020.11.062, 10.1680/jsmic.21.00001 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02710, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::03970
- titulo_norm: `bim fm integrated solution resourcing to digital techniques` | motivo: identificador_fonte_diferente | DOIs: 10.1007/s00521-023-08907-0 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02724, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::06314, SCOPUS::scopus_nucleo_a3_priorizacao_estrategia_manutencao_raw.csv::00155, SCOPUS::scopus_nucleo_a3_priorizacao_estrategia_manutencao_raw.csv::00244, WOS::WOS_NUCLEO_01_20260708_part01.ris::00344
- titulo_norm: `7 10 shallow systems geothermal heat pumps` | motivo: identificador_fonte_diferente | DOIs: 10.1016/b978-0-12-819727-1.00105-9 | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02914, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02930
- titulo_norm: `improving management of manually emptied pit latrine waste in nairobi s urban informal settlements` | motivo: doi_diferente | DOIs: 10.3362/1756-3488.20-00003, 10.3362/1756-3488.20-00003oa | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02959, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::03512
- titulo_norm: `vaca muerta oil production facility energy efficiency analysis` | motivo: identificador_fonte_diferente | DOIs: 10.2118/210025-ms | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02980, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::02984
- titulo_norm: `optimization of ict street infrastructure in smart cities` | motivo: doi_diferente | DOIs: 10.1007/978-981-16-0708-0_13, 10.1007/s42979-021-00577-w | ids: SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::03194, SCOPUS::scopus_nucleo_a1_manutencao_sustentabilidade_raw.csv::03368
- ... e mais 48 grupo(s) (ver lista completa reproduzindo o script).

## 6. Distribuicao de registros unicos por combinacao de bases

| Combinacao de bases_origem | N registros unicos |
|---|---|
| Scopus | 7101 |
| Scopus|WoS | 1036 |
| Crossref | 878 |
| WoS | 437 |
| Crossref|Scopus | 62 |
| Crossref|Scopus|WoS | 21 |
| Crossref|WoS | 7 |

## 7. Arquivos gerados

- `03_PROCESSADOS/registros_normalizados.csv` -- 1 linha por registro bruto, campos padronizados entre as 3 bases (sem deduplicar).
- `03_PROCESSADOS/corpus_consolidado.csv` -- 1 linha por obra unica, apos deduplicacao, com proveniencia preservada.
- `03_PROCESSADOS/duplicatas_detectadas.csv` -- grupos com mais de 1 registro bruto, para auditoria.
- `03_PROCESSADOS/relatorio_deduplicacao.md` -- este relatorio.

## 8. Limites desta etapa

Esta etapa nao faz triagem de relevancia tematica (blocos A/B/C/D), nao classifica corpus descritivo vs. nucleo analitico e nao escreve texto do artigo. O campo `metodo_decisao` (etiqueta instrumental de MCDM/AHP/TOPSIS) tambem nao e preenchido aqui -- e pos-processamento de etapa posterior, conforme secao 7 do protocolo.
