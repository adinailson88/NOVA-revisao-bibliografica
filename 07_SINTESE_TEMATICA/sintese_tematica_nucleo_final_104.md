# Síntese temática do núcleo final — ETAPA_17

## 1. Objetivo da etapa

Construir a síntese temática aprofundada exigida pelo roteiro-mestre (seção 11) a partir do
núcleo final pós-auditoria — os 104 registros com `decisao_qualitativa_final = manter_nucleo_principal`
resultantes da ETAPA_16 e do adendo de descarte de 2026-07-10 (registro `REG_07264`). Cada
afirmação abaixo aponta os `id_unico` que a sustentam, conforme exigido pelo roteiro
("Não afirmar achados sem apontar IDs dos registros que sustentam").

## 2. Arquivos de entrada

- `07_SINTESE_TEMATICA/nucleo_final_pos_auditoria_resumos.csv` (104 registros, leitura estruturada da ETAPA_16)
- `07_SINTESE_TEMATICA/nucleo_principal_sintese_artigo.csv` (137 registros, metadados bibliográficos e flags de extração automática da ETAPA_13/15, filtrado aos 104)

## 3. Método

Não houve leitura de texto completo, uso de internet ou geração de achados por inferência livre.
Os campos usados já haviam sido extraídos em etapas anteriores por dois meios documentados:
extração automática por casamento de frases-chave em título+resumo+palavras-chave (ETAPA_13) e
leitura estruturada de título, resumo, palavras-chave e campos extraídos (ETAPA_16). Esta etapa
apenas explode os campos multi-valorados (separados por `;`) em formato longo, rastreável por
`id_unico`, e tabula frequências. O mapeamento de cada critério à dimensão de sustentabilidade do
roteiro (seção 19) está registrado em `07_SINTESE_TEMATICA/dicionario_criterio_dimensao_etapa17.csv`,
com justificativa por critério.

## 4. Arquivos gerados

- `07_SINTESE_TEMATICA/matriz_base_nucleo_final_104.csv` — matriz combinada (base de tudo abaixo)
- `07_SINTESE_TEMATICA/dicionario_criterio_dimensao_etapa17.csv`
- `07_SINTESE_TEMATICA/matriz_criterios_sustentabilidade.csv`
- `07_SINTESE_TEMATICA/matriz_metodos_decisao.csv`
- `07_SINTESE_TEMATICA/matriz_dimensoes_sustentabilidade.csv`
- `07_SINTESE_TEMATICA/matriz_contexto_edificacao.csv`
- `07_SINTESE_TEMATICA/matriz_lacunas.csv`
- `05_ANALISE_R/tabelas/tabela26_criterios_nucleo_final_104.csv`
- `05_ANALISE_R/tabelas/tabela27_dimensoes_sustentabilidade_nucleo_final_104.csv`
- `05_ANALISE_R/tabelas/tabela28_metodos_decisao_nucleo_final_104.csv`
- `05_ANALISE_R/tabelas/tabela29_contexto_edificacao_nucleo_final_104.csv`
- `05_ANALISE_R/tabelas/tabela30_lacunas_nucleo_final_104.csv`

## 5. RQ1 — Dimensões de sustentabilidade associadas à manutenção/gestão de edificações

Sobre os 104 registros do núcleo final, a dimensão técnica-operacional é a mais presente
(102 registros, 98,1% — ex.: `REG_00110`, `REG_00217`, `REG_00415`, `REG_00489`, `REG_00852`),
seguida da institucional (93, 89,4% — ex.: `REG_00110`, `REG_01046`, `REG_02069`) e da ambiental
(84, 80,8% — ex.: `REG_00415`, `REG_00489`, `REG_01046`). A dimensão de ciclo de vida aparece em
60 registros (57,7%), a econômica em 59 (56,7%) e a social em 57 (54,8%). Dimensões mais
específicas — energia (36, 34,6%), risco (26, 25,0%), conforto (19, 18,3%) e segurança
(16, 15,4%) — aparecem como recortes dentro dessas dimensões maiores. A tabela completa, com a
lista de `id_unico` por dimensão, está na Tabela 27.

## 6. RQ2 — Critérios usados para priorizar intervenções de manutenção/gestão de ativos

O critério mais frequente é desempenho operacional (93 registros, 89,4% — ex.: `REG_00110`,
`REG_00217`, `REG_00415`), seguido de disponibilidade/uso de dados e informação (76, 73,1%),
custo (59, 56,7% — mapeado à dimensão econômica), vida útil (40, 38,5%) e energia
(36, 34,6% — dimensão ambiental). Critérios de condição física (27, 26,0%) e risco
(31, 29,8%) aparecem como recortes técnico-operacionais explícitos. Critérios sociais —
conforto (17, 16,3%), segurança (17, 16,3%) e satisfação do usuário (9, 8,7%) — e ambientais
específicos — emissões de carbono (15, 14,4%), resíduos (13, 12,5%) e água (5, 4,8%) — aparecem
com menor frequência, mas de forma explícita no resumo. A lista completa de critérios, dimensão
mapeada e `id_unico` está na Tabela 26 e em `matriz_criterios_sustentabilidade.csv`.

## 7. RQ3 — Métodos de apoio à decisão presentes na literatura

`framework` é o termo mais recorrente (96 registros, 92,3%), usado no sentido amplo de estrutura
metodológica proposta pelo estudo, não necessariamente um método multicritério formal. Entre os
métodos e abordagens mais específicas: `decision support` (26, 25,0%), `BIM` (26, 25,0% — apoio
tecnológico à decisão), `optimization` (18, 17,3%), `scoring` (17, 16,3%) e `life-cycle cost`
(13, 12,5%). Métodos multicritério formais nomeados explicitamente no resumo aparecem em menor
número: `AHP` (5 registros, 4,8% — `REG_00415`, `REG_04052`, `REG_04552`, `REG_05812`,
`REG_09113`), `TOPSIS` (4, 3,8% — `REG_03843`, `REG_03844`, `REG_04552`, `REG_04813`), `MCDM`
(3, 2,9%), `ANP` (3, 2,9%) e `Bayesian Best Worst Method` (1, 1,0%). Isso é consistente com a
decisão metodológica vigente do projeto de não tratar MCDM/AHP/TOPSIS como pré-condição de
inclusão (ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`, entradas de 2026-07-08): o método
multicritério aparece como um entre vários instrumentos de apoio à decisão na literatura do
núcleo, não como tema dominante. A lista completa está na Tabela 28 e em
`matriz_metodos_decisao.csv`, que também traz, por registro, as flags de extração automática da
ETAPA_13 (`usa_ahp`, `usa_topsis`, `usa_outro_mcdm`, `metodo_mcdm_especifico`) para checagem cruzada.

## 8. RQ4 — Tipos de edificação e contextos de aplicação

A maioria dos registros descreve o objeto predial de forma genérica, sem especificar tipologia
(`edificio_generico`: 93, 89,4%) ou trata de portfólios/carteiras de ativos prediais
(`portfolio_predial`: 58, 55,8% — ex.: `REG_00110`, `REG_00217`, `REG_00519`). Contextos
específicos aparecem em proporção menor: hospitais (17, 16,3%), edifícios comerciais
(16, 15,4%), edifícios residenciais (12, 11,5%), universidades (11, 10,6% — `REG_02540`,
`REG_03383`, `REG_04569`, `REG_05161`, `REG_05495`, `REG_05632`, `REG_05925`, `REG_06548`,
`REG_07061`, `REG_08528`, `REG_09290`), campus (10, 9,6%), edifícios públicos (5, 4,8%), escolas
(5, 4,8%) e patrimônio histórico (4, 3,8%). O contexto explicitamente público/universitário
(universidade + campus + edifício público + escola, sem dupla contagem) está presente em um
subconjunto minoritário do núcleo final, o que já era esperado pelo desenho do corpus (contexto
público/universitário é reforço de relevância, não critério obrigatório de inclusão, conforme
`00_CONTROLE/DECISOES_METODOLOGICAS.md`). A lista completa está na Tabela 29 e em
`matriz_contexto_edificacao.csv`.

## 9. RQ5 — Lacunas para aplicação em instituições públicas de ensino superior

76 dos 104 registros (73,1%) trazem alguma lacuna, limitação ou indicação de pesquisa futura
explícita no resumo (Tabela 30, categoria `com_lacuna_identificada_no_resumo`); os outros 28
(26,9%) não trazem esse elemento de forma identificável apenas pelo resumo. Dentro do núcleo
final, 12 registros (11,5%) trazem lacuna especificamente relacionada a instituições de ensino
superior públicas ou ao contexto universitário/escolar (`REG_01657`, `REG_02540`, `REG_03126`,
`REG_03383`, `REG_04126`, `REG_04569`, `REG_04575`, `REG_05161`, `REG_05404`, `REG_05632`,
`REG_05925`, `REG_07061`) — coerente com a baixa presença de contexto público/universitário
observada na RQ4. A lista completa de textos de lacuna por registro está em
`matriz_lacunas.csv`; a contagem agregada, na Tabela 30.

## 10. RQ0 — Síntese integrada

Combinando as seções 5 a 9: o núcleo final de 104 registros mostra literatura concentrada na
dimensão técnica-operacional e institucional da manutenção/gestão predial (RQ1), priorizada
sobretudo por critérios de desempenho operacional, dados/informação e custo (RQ2), com métodos de
apoio à decisão dominados por frameworks genéricos e abordagens de suporte à decisão/otimização —
métodos multicritério formais nomeados (AHP, TOPSIS, MCDM) presentes, mas minoritários (RQ3) —,
aplicados majoritariamente a edificações e portfólios prediais sem especificação de tipologia, com
contexto público/universitário presente em cerca de um décimo dos registros (RQ4), e uma lacuna
recorrente sobre aplicação a instituições públicas de ensino superior confirmada em 12 registros
(RQ5). Esses achados descrevem o que está explicitamente registrado nos 104 resumos do núcleo
final; não constituem, por si só, o texto de discussão do artigo.

## 11. Limitações

Esta síntese é derivada de título, resumo, palavras-chave e campos já extraídos nas etapas
anteriores, sem leitura full-text. Termos genéricos como `framework`, `edificio_generico` e
`desempenho_operacional` têm alta frequência porque captam formulações amplas comuns em resumos
científicos; não devem ser lidos como evidência de convergência metodológica forte sem
qualificação adicional na redação do artigo. O mapeamento critério→dimensão
(`dicionario_criterio_dimensao_etapa17.csv`) envolveu uma decisão de classificação para termos
ambíguos (notadamente `risco` e `qualidade_servico`), documentada e justificada no próprio
dicionário, mas sujeita a revisão humana. Esta etapa não escreve o artigo nem produz figuras;
produz apenas as matrizes e tabelas de base, com rastreabilidade por `id_unico`.

## 12. Recomendação para a próxima etapa

Usar estas matrizes como base direta das seções de resultados do artigo (critérios e dimensões de
sustentabilidade; métodos de apoio à decisão; aplicabilidade a edificações públicas
universitárias; lacunas), e como insumo para a matriz analítica proposta como contribuição autoral
(roteiro, seção 19). Próximo passo natural, ainda não iniciado: estruturação do artigo
(`estrutura_artigo.md`, roteiro seção 15/ETAPA 12) e produção das figuras correspondentes em R,
com dados-base nas Tabelas 26 a 30.
