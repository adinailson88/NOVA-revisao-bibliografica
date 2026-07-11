# Relatório da Etapa 9

## 1. Escopo executado

Classificação do desenho metodológico dos 104 estudos do núcleo final (`docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`,
seção 15) e avaliação de quais instrumentos de avaliação metodológica são compatíveis com cada
desenho, sem aplicação automática de instrumentos clínicos.

## 2. Arquivos analisados

- `latex-artigo/fontes/nucleo_final_pos_auditoria_resumos.csv`
- `docs/RELATORIO_USO_TEXTO_COMPLETO_19_ESTUDOS.md` e `docs/CODEBOOK_CATEGORIAS_ETAPA_8.md`
  (para não duplicar achados já registrados sobre os sete estudos com texto completo citado)
- `latex-artigo/sections/09_limitacoes.tex`

## 3. Evidências encontradas

- O núcleo final não possui, em nenhuma coluna já existente, um campo de desenho metodológico
  (design) por estudo; a classificação por dimensão/critério/método/contexto (Etapa 8) descreve
  *conteúdo temático*, não *desenho de pesquisa*.
- O único campo com texto substantivo suficiente para inferir desenho ao nível documental é
  `evidencia_curta_do_resumo` (excerto de 62 a 220 caracteres, média 171), combinado ao título.
- A classificação por regras (`scripts/python/classificar_desenho_estudos.py`, codebook em
  `docs/CODEBOOK_DESENHO_METODOLOGICO_ETAPA_9.md`) produziu sete categorias, com 24 dos 104
  registros (23,1%) permanecendo sem sinal textual suficiente para classificação — resultado
  honesto, não forçado.
- Nenhum dos 104 estudos é um ensaio clínico, estudo de coorte, caso-controle ou revisão de
  intervenção em saúde humana — mesmo os estudos ambientados em hospitais (REG_01657, REG_04575,
  REG_05283) tratam de gestão de facilidades e manutenção predial hospitalar, não de desfechos
  clínicos de pacientes.

## 4. Tipologia dos estudos

| Categoria | N | % dos 104 |
|---|---:|---:|
| Aplicação de método de decisão quantitativo (fuzzy, AHP, ANP, TOPSIS, MCDM/MCDA, estocástico, otimização, LCC, aprendizado de máquina) | 24 | 23,1% |
| Não classificável pelo excerto documental disponível | 24 | 23,1% |
| Revisão bibliométrica ou de literatura | 19 | 18,3% |
| Proposta de framework ou modelo conceitual | 11 | 10,6% |
| Estudo de caso empírico | 11 | 10,6% |
| Estudo de simulação ou modelagem digital (BIM, gêmeo digital, controle) | 10 | 9,6% |
| Estudo de levantamento ou percepção de stakeholders | 5 | 4,8% |

Tabela completa com definição, inclusão, exclusão, exemplo e regra de desempate em
`docs/CODEBOOK_DESENHO_METODOLOGICO_ETAPA_9.md`. Lista de `id_unico` por categoria em
`latex-artigo/fontes/tabela37_ids_por_desenho_nucleo_final_104.csv`.

## 5. Instrumentos de avaliação metodológica: verificação de compatibilidade

Conforme o plano (seção 15), instrumentos clínicos não podem ser aplicados automaticamente. Nenhum
dos 104 estudos tem desenho compatível com **RoB 2** (ensaios clínicos randomizados), **GRADE**
(graduação de evidência clínica/epidemiológica) ou **Newcastle–Ottawa** (estudos observacionais em
saúde com grupo de comparação e desfecho de doença). Aplicá-los produziria uma avaliação sem
sentido metodológico, pois nenhum desses instrumentos possui itens aplicáveis a estudos de
engenharia, gestão de ativos ou facility management. Por isso, **nenhum instrumento clínico foi
aplicado**, integralmente ou por adaptação, a qualquer um dos 104 estudos.

Para os desenhos identificados nesta etapa, os instrumentos de avaliação metodológica
potencialmente compatíveis — caso a Rota B (texto completo) venha a ser autorizada no futuro —
seriam:

| Desenho | Instrumento potencialmente compatível | Por que é compatível | Por que não foi aplicado agora |
|---|---|---|---|
| Revisão bibliométrica/literatura | Checklist de transparência de revisão (ex.: itens de escopo, critérios de busca e síntese, adaptados de PRISMA ou AMSTAR-2, sem adotar a ferramenta integralmente) | Itens sobre transparência da busca, dos critérios de seleção e da síntese são aplicáveis a qualquer revisão, independentemente da área. | Exige leitura de texto completo do estudo revisado para verificar se a busca, os critérios e a síntese foram de fato relatados; não verificável a partir de título e excerto. |
| Estudo de caso empírico | Critérios próprios de engenharia: descrição do caso, transparência dos dados coletados, replicabilidade do procedimento | Estudos de caso em engenharia/gestão predial são avaliados pela clareza do contexto e dos dados, não por desfecho clínico. | Exige leitura de texto completo para verificar se o caso, os dados e o procedimento foram descritos com detalhamento suficiente. |
| Levantamento/percepção de stakeholders | Critérios de transparência amostral (tamanho da amostra, instrumento de coleta, taxa de resposta) | Aplicável a qualquer levantamento com coleta de dados primários. | Exige texto completo para verificar amostra, instrumento e taxa de resposta; não declarado no título/resumo. |
| Aplicação de método de decisão quantitativo | Critérios de transparência do método (pesos/parâmetros declarados, consistência do julgamento, validação com dados reais) | Aplicável a qualquer estudo que aplique MCDM, otimização ou modelo estocástico. | Exige texto completo para verificar se pesos, consistência (ex.: razão de consistência do AHP) e validação foram relatados. |
| Simulação/modelagem digital | Critérios de validação do modelo (comparação com dados reais, sensibilidade, limitações declaradas) | Aplicável a qualquer estudo de simulação ou modelagem computacional. | Exige texto completo para verificar validação e análise de sensibilidade. |
| Proposta de framework conceitual | Critérios de aplicabilidade (framework testado ou apenas proposto) | Distingue frameworks validados empiricamente de propostas puramente teóricas. | Exige texto completo para verificar se houve teste/validação do framework proposto. |
| Não classificável | Nenhum | Não há desenho identificado ao nível documental. | Não aplicável. |

**Nenhum desses instrumentos foi efetivamente aplicado a nenhum dos 104 estudos nesta etapa.**
Todos exigem leitura de texto completo para verificação, o que está fora do escopo documental da
revisão (Rota A, adotada desde a Etapa 7). A tabela acima é um mapeamento de compatibilidade
teórica, não uma avaliação executada.

## 6. Critérios próprios de engenharia (nível documental)

No nível documental (título, resumo, palavras-chave), é possível verificar apenas três sinais
superficiais, já usados nesta classificação e nas anteriores:

1. **Presença de um caso/ambiente nomeado** (contexto identificável: hospital, universidade,
   campus, edifício comercial etc. — já registrado na Etapa 8, Tabela de contexto de edificação).
2. **Presença de um método nomeado** (AHP, TOPSIS, fuzzy etc. — já registrado na Etapa 8, Tabela
   de métodos).
3. **Presença de linguagem de revisão versus linguagem de proposta/aplicação** (já registrado
   nesta etapa, Seção 4).

Não é possível, ao nível documental, verificar: adequação da amostra, validade dos instrumentos de
coleta, consistência de julgamento em métodos multicritério, validação de modelos de simulação,
risco de viés de seleção dos casos ou conflito de interesse. Esses itens exigiriam leitura de
texto completo, não realizada.

## 7. Impacto sobre a força das conclusões

- As conclusões do artigo devem ser lidas como **padrões de conteúdo declarado na literatura**
  (quais dimensões, critérios, métodos e contextos aparecem com que frequência), não como
  **evidência validada de eficácia** de qualquer método ou critério específico.
- A predominância de estudos de aplicação de método quantitativo (23,1%) e de proposta de
  framework conceitual (10,6%) indica que boa parte do núcleo propõe ou aplica instrumentos sem
  que a força da validação empírica desses instrumentos tenha sido auditada nesta revisão.
- A ausência de avaliação de risco de viés (Etapa 9, item explicitamente não realizado) significa
  que a matriz analítica proposta no artigo (Seção "Matriz analítica proposta") é uma síntese de
  frequência de menção na literatura, não uma recomendação validada por avaliação crítica da
  qualidade dos estudos que a sustentam. Essa limitação já é compatível com a natureza documental
  da revisão, declarada desde a Etapa 7.

## 8. Alterações realizadas

- `scripts/python/classificar_desenho_estudos.py` (criado): classifica o desenho metodológico dos
  104 estudos por regras reproduzíveis sobre título e excerto documental.
- `latex-artigo/fontes/tabela37_desenho_metodologico_nucleo_final_104.csv` (criado).
- `latex-artigo/fontes/tabela37_ids_por_desenho_nucleo_final_104.csv` (criado).
- `docs/CODEBOOK_DESENHO_METODOLOGICO_ETAPA_9.md` (criado).
- `latex-artigo/sections/09_limitacoes.tex`: acrescentado um parágrafo declarando a ausência de
  avaliação formal de risco de viés/qualidade metodológica, a incompatibilidade dos instrumentos
  clínicos com o corpus, e a natureza dos critérios de engenharia potencialmente aplicáveis em
  etapa futura com texto completo.

## 9. Alterações não realizadas

- Nenhum instrumento de avaliação de qualidade (clínico ou de engenharia) foi efetivamente
  aplicado a qualquer um dos 104 estudos: todos exigem texto completo, não lido nesta etapa.
- Não foi alterada a matriz analítica (Seção "Matriz analítica proposta", Etapa 12) nem os números
  de nenhuma tabela agregada do núcleo de 104 estudos.
- Não foi criada uma nova seção do artigo para a tipologia de desenho; ela permanece como produto
  de dados auditável (`tabela37`) e como conteúdo deste relatório, disponível para uso em etapas
  futuras de redação (Etapa 14), caso o pesquisador decida publicá-la no corpo do artigo.

## 10. Informação insuficiente para verificar

- Desenho metodológico dos 24 estudos (23,1%) sem sinal textual suficiente no título e no excerto
  documental disponível: informação insuficiente para verificar sem leitura de texto completo.
- Risco de viés, validade interna, adequação amostral e consistência de julgamento multicritério
  de qualquer um dos 104 estudos: informação insuficiente para verificar ao nível documental.

## 11. Validações executadas

- Execução de `scripts/python/classificar_desenho_estudos.py`: 104 registros processados, soma das
  sete categorias igual a 104.
- Conferência cruzada de exemplos positivos do codebook com os títulos reais do núcleo final.
- Execução de `python scripts/python/verificar_artigo.py` após a alteração em `09_limitacoes.tex`:
  ver Seção 12.
- Compilação local do LaTeX: informação insuficiente para verificar nesta sessão (mesma limitação
  de ambiente já registrada nas etapas anteriores); a integração contínua do repositório
  (`.github/workflows/latex.yml`) permanece responsável pela compilação e pela verificação de
  margens, com uma pendência de ajuste fino de layout já em andamento e a cargo do pesquisador,
  conforme combinado.

## 12. Arquivos alterados

- `scripts/python/classificar_desenho_estudos.py` (criado)
- `latex-artigo/fontes/tabela37_desenho_metodologico_nucleo_final_104.csv` (criado)
- `latex-artigo/fontes/tabela37_ids_por_desenho_nucleo_final_104.csv` (criado)
- `docs/CODEBOOK_DESENHO_METODOLOGICO_ETAPA_9.md` (criado)
- `latex-artigo/sections/09_limitacoes.tex`
- `docs/RELATORIO_ETAPA_9.md` (criado)
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 13. Commit e push

Registrado após a execução do commit exclusivo da Etapa 9 (ver
`docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`).

## 14. Pendências

- Ajuste fino de layout do PDF no fluxo de integração contínua (estouro de margem residual em uma
  tabela), já em andamento e assumido pelo pesquisador fora desta sessão; não bloqueia o conteúdo
  desta etapa.
- Decisão, em etapa futura (Etapa 14), sobre se a tipologia de desenho metodológico deve ser
  publicada como tabela no corpo do artigo.

## 15. Próxima etapa prevista

Etapa 10 — auditoria dos resultados, somente após autorização explícita.
