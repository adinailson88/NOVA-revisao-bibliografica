# Relatório da Etapa 7

## 1. Escopo executado

Verificação da avaliação de texto completo e da elegibilidade dos 104 estudos do núcleo final,
conforme `docs/PLANO_EXECUCAO_REVISAO_ARTIGO.md`, seção 13. Constatada a ausência de leitura de texto
completo em todas as camadas de triagem e na auditoria qualitativa, foram: identificadas as conclusões
que podem ser mantidas e as que precisam de restrição de linguagem; declarada explicitamente a
limitação de elegibilidade; distinguida a análise documental de síntese de evidências; e apresentadas
as Rotas A e B, sem execução da Rota B.

## 2. Arquivos analisados

- `latex-artigo/sections/03_metodologia.tex`
- `latex-artigo/sections/04_panorama.tex`
- `latex-artigo/sections/05_criterios.tex`
- `latex-artigo/sections/06_metodos.tex`
- `latex-artigo/sections/07_aplicabilidade.tex`
- `latex-artigo/sections/08_matriz.tex`
- `latex-artigo/sections/09_limitacoes.tex`
- `latex-artigo/sections/10_consideracoes.tex`
- `docs/RELATORIO_ETAPA_6.md`
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`
- `scripts/python/verificar_artigo.py`

## 3. Evidências encontradas

- `03_metodologia.tex` já declarava, camada a camada, que a pré-triagem, a resolução das dúvidas, o
  alinhamento às perguntas de pesquisa e a auditoria qualitativa dos 137 registros foram realizados
  "sem leitura de texto completo" e "sem leitura integral".
- Um dos 137 registros havia sido sinalizado para verificação pontual em texto completo e foi
  descartado sem que essa leitura fosse realizada; esse ponto já constava na Tabela de rastreabilidade
  do funil de seleção, mas não estava traduzido em uma declaração explícita de elegibilidade.
- `09_limitacoes.tex` não continha, até esta etapa, nenhuma limitação explícita sobre a ausência de
  avaliação de texto completo ou de elegibilidade em texto completo.
- `10_consideracoes.tex` continha a expressão "a literatura ... confirma a relevância de combinar
  custo, desempenho, energia e experiência dos usuários", verbo forte para uma síntese apoiada em
  título, resumo e palavras-chave.
- As demais seções revisadas (`04_panorama`, `05_criterios`, `06_metodos`, `07_aplicabilidade`,
  `08_matriz`) utilizam linguagem compatível com análise documental ("identificou", "aparece", "foram
  encontrados", "reúne"), sem afirmações que pressuponham leitura de texto completo.
- `scripts/python/verificar_artigo.py`, executado antes de qualquer alteração desta etapa (commit
  `523f44f`, encerramento da Etapa 6), já falhava na verificação `exigir(texto_tex.count("\begin{table}")
  == 5, ...)`: o artigo contém 8 tabelas (5 em `03_metodologia.tex`, 1 em `04_panorama.tex`, 1 em
  `05_criterios.tex` e 1 em `07_aplicabilidade.tex`), não 5. Essa divergência é anterior à Etapa 7 e não
  foi introduzida por ela.

## 4. Problemas identificados

- Ausência de declaração explícita de elegibilidade em texto completo no corpo metodológico do
  artigo, apesar de a ausência de leitura integral já estar descrita por camada de triagem.
- Ausência de limitação específica, na Seção de Limitações, sobre a diferença entre análise documental
  e síntese de evidências extraídas de texto completo.
- Uma ocorrência de linguagem que extrapola o nível documental de evidência ("confirma") nas
  Considerações finais.

## 5. Alterações realizadas

- `latex-artigo/sections/03_metodologia.tex`: inserido parágrafo, após a Figura do funil de seleção,
  declarando explicitamente que a elegibilidade do núcleo final não incluiu leitura de texto completo,
  citando o caso do registro sinalizado para verificação pontual e descartado sem essa leitura.
- `latex-artigo/sections/09_limitacoes.tex`: inserido parágrafo declarando a limitação de ausência de
  leitura de texto completo e de avaliação formal de elegibilidade, distinguindo a base documental
  (título, resumo, palavras-chave, campos estruturados) de síntese de evidências extraídas de texto
  completo, avaliação de qualidade metodológica, risco de viés ou verificação de resultados relatados.
- `latex-artigo/sections/10_consideracoes.tex`: substituído "confirma" por "no nível documental
  analisado, reforça", restringindo a conclusão ao nível de evidência efetivamente sustentado.

### Rota A — manutenção da revisão em nível documental

A revisão permanece apoiada em título, resumo, palavras-chave e campos estruturados extraídos dos 104
estudos. Essa é a rota adotada nesta etapa. Ela não exige nova coleta de dados nem novos procedimentos,
mas depende de linguagem consistentemente documental em todo o artigo, o que passou a ser reforçado
pelas alterações desta etapa em `03_metodologia.tex`, `09_limitacoes.tex` e `10_consideracoes.tex`.

### Rota B — elevação para revisão sistemática com texto completo (não executada)

Caso o pesquisador autorize especificamente essa rota em etapa futura, o plano operacional seria:

1. Obtenção do texto completo dos 104 estudos (ou do subconjunto acessível), com registro de
   disponibilidade e de eventuais estudos sem acesso.
2. Definição e aplicação de critérios de elegibilidade em texto completo, distintos dos critérios já
   aplicados em título/resumo.
3. Registro dos motivos de exclusão por estudo, com tabela de rastreabilidade equivalente à do funil
   de seleção já existente.
4. Avaliação metodológica dos estudos elegíveis, compatível com os desenhos identificados (etapa 9 do
   protocolo).
5. Nova extração de dados a partir do texto completo, com dicionário de categorias próprio (etapa 8 do
   protocolo).
6. Auditoria da nova extração, com segundo avaliador independente ou procedimento de resolução de
   divergências documentado.
7. Nova síntese, com atualização proporcional de resultados, discussão, matriz analítica e limitações.

Esta rota não foi executada nesta etapa, por exigir autorização específica e recursos (acesso a texto
completo, tempo de leitura e segundo avaliador) não confirmados neste momento.

## 6. Alterações não realizadas

- Não foi alterada a linguagem de `04_panorama.tex`, `05_criterios.tex`, `06_metodos.tex`,
  `07_aplicabilidade.tex` e `08_matriz.tex`: a auditoria não encontrou, nessas seções, afirmações que
  extrapolassem o nível documental de evidência.
- Não foi iniciada a Rota B (obtenção de texto completo, elegibilidade formal, avaliação metodológica
  ou nova extração), por não haver autorização específica para essa elevação de escopo.
- Não foram alterados números, tabelas, figuras, citações ou referências.
- Não foi corrigida a divergência pré-existente do verificador automático quanto à contagem de tabelas
  (item 3): a causa está fora do escopo da Etapa 7 (texto completo e elegibilidade) e pertence à
  redação/estruturação de tabelas tratada em etapas futuras (por exemplo, Etapa 14).

## 7. Informação insuficiente para verificar

- Se o registro sinalizado para verificação pontual em texto completo (excluído dos 137) teria sido
  incluído ou excluído do núcleo final caso essa leitura tivesse ocorrido: informação insuficiente para
  verificar.
- Disponibilidade de acesso ao texto completo dos 104 estudos, caso a Rota B seja autorizada no futuro:
  informação insuficiente para verificar.

## 8. Validações executadas

- Conferência de que as três seções alteradas mantêm a contagem de 5 tabelas e 6 figuras do artigo.
- Conferência de que nenhuma citação ou chave bibliográfica foi adicionada, removida ou alterada.
- Conferência de que os parágrafos inseridos não usam travessão Unicode nem a sintaxe `" -- "`,
  compatível com as regras de estilo verificadas por `scripts/python/verificar_artigo.py`.
- Execução de `python scripts/python/verificar_artigo.py`: falhou na verificação de contagem de
  tabelas (`O artigo deve manter cinco tabelas essenciais.`). Confirmado, por comparação com o commit
  `523f44f` (encerramento da Etapa 6, anterior a qualquer alteração desta etapa), que essa falha já
  existia antes da Etapa 7 e não foi causada pelas alterações registradas neste relatório. As demais
  verificações do script (citações, bibliografia, corpus final, estratégia de busca, produtos da
  deduplicação, triagem e auditoria) não foram exercidas nesta execução porque o script interrompe na
  primeira falha (`assert`); não podem ser declaradas aprovadas.
- Compilação local do LaTeX: informação insuficiente para verificar (ambiente sem instalação TeX
  disponível nesta sessão); a compilação automatizada permanece a cargo do workflow do repositório.

## 9. Arquivos alterados

- `latex-artigo/sections/03_metodologia.tex`
- `latex-artigo/sections/09_limitacoes.tex`
- `latex-artigo/sections/10_consideracoes.tex`
- `docs/RELATORIO_ETAPA_7.md` (criado)
- `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`

## 10. Commit e push

Registrado após a execução do commit exclusivo da Etapa 7 (ver `docs/STATUS_EXECUCAO_REVISAO_ARTIGO.md`).

## 11. Pendências

- Confirmar, junto ao pesquisador, se a Rota B deve ser autorizada em etapa futura ou se a revisão
  permanece na Rota A até a consolidação final.
- `scripts/python/verificar_artigo.py` falha na verificação de contagem de tabelas desde antes da
  Etapa 7 (8 tabelas presentes contra 5 esperadas pelo script). Essa divergência não foi corrigida
  nesta etapa, por não pertencer ao escopo de texto completo e elegibilidade; permanece pendente para
  correção em etapa futura de redação/padronização ou de ajuste do próprio verificador.

## 12. Próxima etapa prevista

Etapa 8 — dicionário de categorias e extração, somente após autorização explícita.
