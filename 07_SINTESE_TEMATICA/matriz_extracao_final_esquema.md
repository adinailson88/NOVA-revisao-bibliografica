# ESQUEMA DA MATRIZ DE EXTRAÇÃO FINAL — ETAPA_12

Define o conjunto definitivo de colunas a preencher para cada um dos 3.678 registros do núcleo
analítico revisado (ETAPA_10). Esta etapa **não preenche** nenhuma linha — apenas define nomes de
coluna, valores permitidos e regra de preenchimento. O preenchimento fica para etapa seguinte, ainda
sem número definido.

## 1. Mudança de estratégia (ler antes de preencher)

A matriz de extração final **não depende de leitura de texto completo (PDF)** de nenhum registro.
Toda coluna de conteúdo é preenchida com base apenas em **título + resumo + palavras-chave** — a
mesma base de evidência já usada na ETAPA_11 (síntese temática preliminar). Decisão registrada em
`00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09 ("ETAPA_12: mudança de estratégia").

Consequência direta: nenhuma coluna desta matriz deve ser preenchida com informação que não esteja
explícita no título, resumo ou palavras-chave do registro. Quando a informação não está explícita,
o campo recebe um valor fixo de ausência (ver por coluna, abaixo) — nunca um valor inferido,
simulado ou presumido a partir de conhecimento externo ao resumo.

## 2. Origem das colunas

A matriz final reaproveita integralmente as 33 colunas de metadados e sinalização temática já
resolvidas por `07_SINTESE_TEMATICA/matriz_sintese_tematica_preliminar.csv` (ETAPA_11) — da coluna
`id_unico` até `nucleo_analitico_revisado`. Essas colunas não mudam de nome, tipo ou regra de
preenchimento; ver `07_SINTESE_TEMATICA/relatorio_sintese_tematica_preliminar.md` para o método de
cada uma.

O que esta etapa define é a substituição das colunas de conteúdo que a ETAPA_11 deixou fixas em
`pendente_leitura_completa`, mais 3 colunas novas de controle (`base_evidencia_extracao`,
`resumo_suficiente_para_extracao`, `uso_no_artigo`) que não existiam na matriz preliminar.

## 3. Lista completa de colunas (ordem final)

### 3.1 Metadados e identificação (herdadas da ETAPA_11, sem mudança)

| Coluna | Tipo | Preenchimento |
|---|---|---|
| `id_unico` | texto | herdado de `corpus_consolidado.csv` |
| `doi` | texto | herdado |
| `titulo` | texto | herdado |
| `ano` | inteiro | herdado |
| `autores` | texto | herdado (cobertura baixa, 24,1% do corpus — limitação já registrada na ETAPA_11) |
| `fonte_periodico` | texto | herdado |
| `tipo_documento` | texto | herdado |
| `bases_origem` | texto | herdado |
| `strings_origem` | texto | herdado |
| `resumo_presente` | sim/nao | herdado |
| `palavras_chave` | texto | herdado |
| `resumo` | texto | herdado |

### 3.2 Sinalização temática e de método (herdadas da ETAPA_11, sem mudança)

`bloco_a_presente`, `bloco_b_presente`, `bloco_c_presente`, `bloco_d_presente`,
`bloco_tecnologico_presente`, `bloco_conceitual_presente`, `termos_bloco_a`, `termos_bloco_b`,
`usa_topsis`, `usa_ahp`, `usa_outro_mcdm`, `metodo_mcdm_especifico`, `usa_bim`, `usa_digital_twin`,
`usa_iot`, `usa_data_driven`, `tecnologia_especifica`, `tipo_edificacao_sinal`,
`eixo_tematico_preliminar`, `classe_final_sem_duvida`, `nucleo_analitico_revisado`.

Todas mantêm o método e os valores permitidos já documentados em
`07_SINTESE_TEMATICA/relatorio_sintese_tematica_preliminar.md`. Nenhuma foi alterada nesta etapa.

Nota de correspondência com o roteiro-mestre (seção 14): o roteiro pede também uma coluna
`metodo_decisao` (sim/nao, indicando se o registro usa algum método formal de decisão). Esta
informação já está coberta por `bloco_c_presente` (presença de vocabulário MCDM/decisão) combinado
com `usa_topsis`/`usa_ahp`/`usa_outro_mcdm`/`metodo_mcdm_especifico` — não se cria uma coluna
duplicada. Divergência de nomenclatura já registrada na ETAPA_11 (`00_CONTROLE/
DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09) e mantida aqui pela mesma regra de precedência
(seção 26.6 do roteiro).

### 3.3 Colunas de conteúdo — final, preenchidas por título+resumo+palavras-chave (definidas nesta etapa)

| Coluna | Tipo / valores permitidos | Regra de preenchimento |
|---|---|---|
| `pais_contexto` | texto livre curto (nome de país/região) ou `nao_informado_no_resumo` | Preencher só se o resumo ou título citar explicitamente um país, região ou tipo de contexto geográfico/administrativo (ex.: "in Brazil", "Chinese universities", "European public buildings"). Não inferir nacionalidade do periódico, da afiliação presumida do autor, nem da base de indexação. |
| `tipo_aplicacao` | um de: `estudo_de_caso`, `revisao_sistematica_ou_bibliometrica`, `proposta_de_framework_ou_modelo`, `survey_ou_levantamento_com_especialistas`, `simulacao_ou_modelagem_computacional`, `estudo_conceitual_sem_aplicacao_empirica`, `nao_classificavel_pelo_resumo` | Classificar pelo que o resumo diz sobre o desenho do estudo (ex.: "this paper proposes a framework", "a case study of a university building", "a systematic review of..."). Usar `nao_classificavel_pelo_resumo` quando o resumo não descrever o tipo de estudo com clareza suficiente — não adivinhar pelo título isolado. |
| `dados_utilizados` | texto livre curto ou `nao_informado_no_resumo` | Registrar, em poucas palavras, o tipo de dado mencionado no resumo (ex.: "dados de sensores IoT de 12 meses", "questionário com 45 gestores prediais", "dados secundários de manutenção corretiva"). Não inventar volume/período não mencionado. |
| `resultado_principal` | texto livre curto (1-2 frases, paráfrase, não cópia literal extensa) ou `nao_informado_no_resumo` | Resumir o achado principal tal como declarado no resumo (ex.: redução percentual de custo, ranking de critérios, framework validado). Se o resumo só descreve objetivo/método sem declarar resultado, usar `nao_informado_no_resumo` — não presumir que o resultado foi positivo. |
| `contribuicao_para_artigo` | texto livre curto ou `a_definir_na_sintese` | Registro de trabalho, não julgamento definitivo: anotação curta de como o registro pode servir ao artigo (ex.: "exemplo de critério social pouco frequente", "caso de aplicação em hospital", "framework comparável ao proposto"). Usar `a_definir_na_sintese` quando a relevância específica ainda não estiver clara no momento do preenchimento — este campo pode ser revisto na etapa de redação, não é decisão final de uso (essa é `uso_no_artigo`, coluna separada). |
| `lacuna_identificada` | texto livre curto ou `nao_identificavel_pelo_resumo` | Preencher só se o próprio resumo apontar explicitamente uma lacuna, limitação ou chamado para pesquisa futura (ex.: "future research should address..."). Não é o pesquisador apontando uma lacuna dele mesmo sobre o registro — é o que o registro afirma sobre a lacuna da área. |
| `criterios_ambientais` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | `sim` se o resumo/palavras-chave mencionar critério(s) ambiental(is) explícito(s) (ex.: consumo de energia, emissões, água, resíduos, certificação ambiental). `nao` se o resumo cobre outras dimensões e claramente não menciona ambiental. `nao_verificavel_pelo_resumo` quando o resumo é vago demais para decidir. |
| `criterios_economicos` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | Mesmo critério, para custo, orçamento, ciclo de vida financeiro, retorno de investimento, valor de ativo. |
| `criterios_sociais` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | Mesmo critério, para conforto/bem-estar de usuários, acessibilidade, satisfação, saúde ocupacional, equidade. |
| `criterios_tecnicos_operacionais` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | Mesmo critério, para desempenho técnico do ativo, confiabilidade, manutenibilidade, tempo de resposta operacional. |
| `criterios_institucionais` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | Mesmo critério, para governança, política pública, normativa, gestão institucional/organizacional. |
| `criterios_risco` | `sim` / `nao` / `nao_verificavel_pelo_resumo` | Mesmo critério, para risco, vulnerabilidade, resiliência, segurança predial/estrutural. |

Regra comum aos seis campos `criterios_*`: são independentes entre si (um mesmo registro pode ter
vários `sim` simultâneos). Não são o mesmo campo que `eixo_tematico_preliminar` (que é um rótulo
único dominante) — aqui é permitido e esperado múltiplo `sim`.

### 3.4 Colunas de controle (novas nesta etapa)

| Coluna | Tipo / valores permitidos | Regra de preenchimento |
|---|---|---|
| `base_evidencia_extracao` | valor fixo `titulo_resumo_palavras_chave` | Preenchido igual em todos os 3.678 registros — documenta de forma permanente que nenhum campo desta matriz vem de leitura de texto completo. Substitui, por decisão desta etapa, a coluna `acesso_texto_completo` que o prompt original previa (ver `00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09). |
| `resumo_suficiente_para_extracao` | `sim` / `parcial` / `nao` | Avaliação de trabalho, registro a registro, sobre se o resumo continha informação suficiente para responder às colunas de conteúdo da seção 3.3. `sim`: a maioria dos campos de conteúdo pôde ser preenchida com informação explícita. `parcial`: só parte dos campos. `nao`: quase nenhum campo de conteúdo pôde ser preenchido além dos valores de ausência — normalmente registros sem resumo ou com resumo muito curto/genérico. Substitui a coluna `necessita_leitura_completa` da ETAPA_11 (que pressupunha uma etapa de leitura full-text futura, hoje fora da estratégia vigente). |
| `uso_no_artigo` | um de: `nucleo_analitico`, `contextualizacao`, `metodo`, `discussao_lacuna`, `excluir`, `pendente` | Valores herdados literalmente do roteiro-mestre (seção 14). Decisão de uso efetivo no texto do artigo — não é feita nesta etapa nem deve ser preenchida automaticamente por regra; fica `pendente` até decisão humana explícita na etapa de síntese/redação. |
| `observacoes` | texto livre | Qualquer nota que não caiba nos campos acima (ex.: ambiguidade de classificação, registro que merece checagem futura). |

## 4. O que esta etapa não faz

- Não preenche nenhuma linha da matriz (0 registros de dados no gabarito).
- Não decide `uso_no_artigo` de nenhum registro — todos ficam com o valor permitido `pendente` na
  etapa de preenchimento, a menos que decisão humana explícita mude isso registro a registro.
- Não lê nem simula leitura de texto completo de nenhum artigo.
- Não redige texto do artigo.

## 5. Arquivos desta etapa

- Este documento.
- `07_SINTESE_TEMATICA/matriz_extracao_final_gabarito.csv` — cabeçalho final, 0 linhas de dados.
- `00_CONFIG/gerar_gabarito_matriz_extracao_final.py` — script reprodutível que gera o gabarito a
  partir da lista de colunas deste documento.
