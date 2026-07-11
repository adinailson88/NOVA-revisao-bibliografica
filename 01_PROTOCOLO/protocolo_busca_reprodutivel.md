# PROTOCOLO DE BUSCA REPRODUTÍVEL

Etapa: ETAPA_01 — PLANO_BUSCAS.
Esta etapa apenas planeja a busca. Não executa coleta, não faz triagem, não escreve o artigo.

## 1. Objetivo

Definir, de forma reprodutível, como a revisão irá buscar literatura sobre manutenção predial e
gestão de edificações como estratégia de sustentabilidade do ambiente construído, em contextos
públicos, universitários e institucionais — conforme `00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md`.

Lógica fixa: **mesma matriz conceitual → strings nativas por base → pós-processamento
padronizado.**

## 2. Escopo e limites

- Tipo de revisão: revisão integrativa sistematizada com apoio bibliométrico e síntese temática.
- Período: 2010–2026.
- Idiomas: buscas principais em inglês; português e espanhol apenas como complemento no Google
  Scholar.
- Sem download em massa de PDF, sem Sci-Hub/LibGen. Trabalhar apenas com metadados (título,
  resumo, palavras-chave, autores, ano, periódico, DOI, base, citações, links oficiais).

## 3. Decisão metodológica sobre o papel do MCDM (registro obrigatório)

Versões anteriores deste projeto (ver `ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt`, seções 9–10)
tratavam "multi-criteria/MCDM/AHP/TOPSIS" como um terceiro bloco em AND obrigatório em todas as
strings do núcleo. Isso tornaria métodos multicritério pré-condição de inclusão no corpus
principal — o que contraria a regra atual registrada em `00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md`:
"não voltar ao foco antigo centrado em TOPSIS, AHP, ODS, ESG ou universidade como tema isolado.
Métodos multicritério são instrumentos, não objeto principal."

Decisão adotada nesta etapa: as strings do núcleo (`01_PROTOCOLO/strings_nativas_por_base.md`)
usam apenas BLOCO_1 (objeto predial) AND BLOCO_2 (sustentabilidade) como condição de entrada.
BLOCO_3 (decisão/priorização/MCDM) passa a ser usado só de duas formas:
1. como string de **refinamento instrumental**, rodada sobre o corpus já coletado, apenas para
   caracterizar/etiquetar o subconjunto que emprega método formal de decisão (campo
   `metodo_decisao` da futura matriz de extração);
2. como termo de busca dentro do corpus complementar/conceitual, quando pertinente.

Impacto metodológico: o corpus principal deixa de exigir metodologia multicritério formal para ser
elegível, evitando que o artigo volte a ser organizado em torno de TOPSIS/AHP/ESG/ODS como tema.
Contexto público/universitário/institucional segue como variação lexical de busca (reforço de
recall), não como recorte temático isolado.

## 4. Bases, acesso e observações técnicas

### 4.1 Scopus
- Acesso via API Elsevier, chave `SCOPUS_API_KEY` lida de `00_CONFIG/apis_local.txt` (arquivo
  local, protegido por `.gitignore`). Nunca inserir o valor da chave em código versionado, log ou
  saída de terminal.
- Campo de busca: `TITLE-ABS-KEY`. Filtro de ano: `PUBYEAR`.
- Campos mínimos a capturar: eid, doi, title, abstract, author_names, author_ids (quando
  disponível), year, source_title, document_type, subtype, citedby_count, aggregation_type,
  subject_area (quando disponível), keywords (quando disponível), url, database=Scopus, string_id.
- Cada execução deve registrar: query, data, número bruto de retornos, número exportado, erros
  HTTP e paginação.

### 4.2 Crossref
- REST API, sem autenticação obrigatória, mas usar parâmetro `mailto` (variável
  `CROSSREF_MAILTO`, já configurada localmente) para polite pool.
- Não depender de abstract — muitos registros não possuem resumo. Função: reforço e
  enriquecimento de DOI/metadados, não corpus analítico único.
- Campos mínimos: DOI, title, abstract (se houver), author, published-print/published-online/
  issued, container-title, type, subject, is-referenced-by-count, URL, publisher, language (se
  houver), database=Crossref, string_id.

### 4.3 Web of Science
- Busca manual pelo usuário na WoS Core Collection, Advanced Search, campo `TS` (Topic), período
  `PY=(2010-2026)`. Exportar Full Record com abstract.
- Não usar API se o acesso institucional não estiver habilitado. O script local apenas importa os
  arquivos `.ris` exportados manualmente.

### 4.4 Google Scholar / SerpAPI
- Uso complementar e de verificação — nunca equivalente a Scopus/WoS como base bibliométrica
  controlada (cobertura e metadados dinâmicos, ordenação não controlável).
- Registrar: engine=google_scholar, query, as_ylo=2010, as_yhi=2026, start, num, idioma (quando
  usado), data/hora da coleta.
- Uso previsto: achar artigos-chave ausentes nas outras bases, literatura aplicada/regional,
  checagem de revisões recentes, snowballing por "cited by"/"related" (quando registrado).

## 5. Separação dos blocos de corpus

| Bloco | Finalidade | Soma automática ao corpus analítico principal? |
|---|---|---|
| Núcleo (BLOCO_1 AND BLOCO_2) | responder às perguntas do artigo — manutenção/gestão predial + sustentabilidade | Sim |
| Complementar tecnológico (BLOCO_4) | apoio por dados, BIM, gêmeo digital, smart campus, manutenção preditiva | Não — bloco próprio |
| Conceitual exploratório (BLOCO_5) | discussão conceitual sobre ambiente construído, sistemas vivos, campus sustentável, metabolismo urbano, biossistemas construídos | Não — bloco próprio |
| Refinamento instrumental (BLOCO_3) | classificar, dentro do núcleo já coletado, quem usa método formal de decisão (MCDM/AHP/TOPSIS/etc.) | Não é bloco de coleta — é etiqueta de pós-processamento |

Frase de método a manter no artigo (herdada de `ROTEIRO_ARTIGO_NOVO_METODO_REVISAO.txt`, seção 8):
"Foram conduzidas buscas em três blocos: núcleo da revisão, busca complementar tecnológica e busca
conceitual exploratória. Apenas o núcleo da revisão foi utilizado para composição do corpus
analítico principal; os demais blocos subsidiaram contextualização, identificação de lacunas e
discussão teórica."

## 6. Procedimento de execução (para etapas futuras — não executar agora)

1. Rodar cada string do núcleo (Scopus) uma por vez; salvar JSON e CSV brutos em
   `02_DADOS_BRUTOS/scopus/` antes de qualquer consolidação.
2. Rodar cada query Crossref uma por vez; salvar JSON/CSV brutos em `02_DADOS_BRUTOS/crossref/`.
   Não misturar com Scopus.
3. Rodar manualmente as strings WoS na Core Collection; salvar exportações `.ris` em
   `02_DADOS_BRUTOS/wos_manual/`, com nomes padronizados (ver
   `01_PROTOCOLO/strings_nativas_por_base.md`).
4. Rodar as queries Google Scholar/SerpAPI; salvar resultados brutos em
   `02_DADOS_BRUTOS/google_scholar/`.
5. Registrar por execução, sem exceção: base, data/hora, string_id, filtros aplicados, número
   bruto de registros, nome do arquivo gerado, eventuais erros.
6. Não deduplicar nesta fase de coleta bruta. Preservar proveniência (`bases_origem`,
   `strings_origem`) para a deduplicação em etapa posterior.

## 7. Pós-processamento padronizado (etapas futuras)

- Padronizar campos entre bases (`03_PROCESSADOS/`).
- Deduplicar por DOI e por título normalizado, preservando proveniência de bases e strings.
- Classificar em: corpus descritivo (todos deduplicados após elegibilidade mínima), núcleo
  analítico (subconjunto efetivamente usado na síntese), corpus complementar tecnológico e corpus
  conceitual — arquivos separados em `04_TRIAGEM/` (`corpus_descritivo.csv`,
  `corpus_complementar_tecnologico.csv`, `corpus_conceitual.csv`).
- Aplicar a string/etiqueta instrumental (BLOCO_3) sobre o núcleo já coletado para preencher o
  campo `metodo_decisao` (e subcampos como `usa_ahp`, `usa_topsis`, `usa_outro_mcdm`) — sem usar
  esse campo como critério de exclusão do núcleo.
- Critérios de inclusão no corpus principal: presença obrigatória de BLOCO_1 (objeto predial) e
  BLOCO_2 (sustentabilidade). BLOCO_3 (decisão) e o contexto público/universitário/institucional
  reforçam classificação e relevância, mas não são obrigatórios para inclusão.
- Exclusões: registros sem relação com edificação/ambiente construído; manutenção industrial,
  manufatura ou transporte sem ponte explícita com edificações; apenas materiais de construção sem
  operação/manutenção; apenas smart city/mobilidade urbana/tráfego sem edificação; duplicatas.
- Registros sem resumo: não excluir automaticamente antes de tentar enriquecimento por DOI/
  Crossref/Scopus/WoS; se persistir sem resumo, marcar `triagem_por_titulo=sim` e
  `confianca=baixa`.

## 8. Reprodutibilidade

Cada execução de busca deve ser rastreável até: base, string nativa exata executada, data, janela
temporal, filtros, número bruto de registros e arquivo gerado. Nenhuma string deve ser alterada
sem registrar evidência, motivo e impacto metodológico (regra do roteiro-mestre e de
`00_CONTROLE/REGRAS_DE_EXECUCAO.md`).

Arquivos produzidos por esta etapa:
- `01_PROTOCOLO/matriz_conceitual_busca.csv`
- `01_PROTOCOLO/strings_nativas_por_base.md`
- `01_PROTOCOLO/protocolo_busca_reprodutivel.md` (este arquivo)

## 9. Limites desta etapa

Esta etapa não executa nenhuma busca, não baixa dados, não faz triagem e não escreve texto do
artigo. Toda afirmação factual externa incluída em etapas futuras exige referência verificável;
resultado próprio deve estar vinculado a tabela, figura, matriz ou arquivo; na ausência de fonte ou
dado próprio, registrar "Informação insuficiente para verificar" (regra de
`00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md` e `00_CONTROLE/REGRAS_DE_EXECUCAO.md`).

## 10. Próxima etapa sugerida

ETAPA_02 — coleta Scopus API (rodar strings do núcleo, salvar bruto, sem deduplicar). Não iniciar
nesta etapa.
