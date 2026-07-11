# STRINGS NATIVAS POR BASE

Fonte da matriz conceitual: `01_PROTOCOLO/matriz_conceitual_busca.csv`.
Lógica: mesma matriz conceitual → strings nativas por base → pós-processamento padronizado.

Regra herdada de `00_CONTROLE/CONTEXTO_CURTO_ARTIGO.md`: o foco é manutenção predial e gestão de
edificações como estratégia de sustentabilidade do ambiente construído. BLOCO_3 (decisão e
priorização multicritério — MCDM/AHP/TOPSIS/ESG/ODS) é instrumento, não objeto principal. Por isso,
diferente de versões anteriores deste roteiro, BLOCO_3 **não entra em AND obrigatório** nas strings
de coleta do núcleo. Ele aparece apenas em uma string de refinamento instrumental (uso em
pós-processamento/classificação, não em critério de inclusão) e nas buscas complementares.

Todas as strings usam BLOCO_1 (objeto predial) AND BLOCO_2 (sustentabilidade) como condição de
entrada no núcleo. Contexto público/universitário/institucional entra como variação lexical dentro
de BLOCO_1, nunca como recorte isolado.

Janela temporal: 2010–2026 (PUBYEAR/PY/from-pub-date conforme a base).
Idiomas: buscas principais em inglês; português e espanhol apenas em Google Scholar, como
complemento (ver seção 4).

---

## 1. SCOPUS — API Elsevier, campo TITLE-ABS-KEY

Chave: `SCOPUS_API_KEY`, lida de `00_CONFIG/apis_local.txt` (arquivo local, protegido por
`.gitignore`). Nunca inserir o valor da chave em script versionado ou em log.

Rodar uma string por vez. Salvar retorno bruto (JSON e CSV) por string antes de qualquer
consolidação.

### Núcleo — corpus principal

**SCOPUS_NUCLEO_A1_MANUTENCAO_SUSTENTABILIDADE**
```
TITLE-ABS-KEY(
  (
    "building maintenance" OR "facility management" OR "facilities management" OR
    "facilities maintenance" OR "building asset management" OR "building operation" OR
    "operation and maintenance" OR "maintenance management"
  )
  AND
  (
    sustainab* OR "green building*" OR "life cycle" OR "life-cycle" OR
    "sustainability assessment" OR "sustainability indicator*" OR
    "environmental performance" OR "building performance"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```

**SCOPUS_NUCLEO_A2_CONTEXTO_PUBLICO_UNIVERSITARIO**
```
TITLE-ABS-KEY(
  (
    "public building*" OR "university building*" OR "university campus" OR
    "higher education institution*" OR "educational building*" OR
    "government building*" OR "public sector building*" OR "building portfolio"
  )
  AND
  (
    "building maintenance" OR maintenance OR "facility management" OR
    "facilities management" OR "asset management" OR "operation and maintenance"
  )
  AND
  (
    sustainab* OR "environmental performance" OR "life cycle" OR "sustainability assessment"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```

**SCOPUS_NUCLEO_A3_PRIORIZACAO_ESTRATEGIA_MANUTENCAO**
```
TITLE-ABS-KEY(
  (
    "maintenance prioritization" OR "maintenance backlog" OR "deferred maintenance" OR
    "maintenance strategy" OR "maintenance planning" OR "renewal prioritization" OR
    "condition assessment" OR "condition-based maintenance"
  )
  AND
  (
    building* OR "public building*" OR "university building*" OR campus OR
    "building portfolio" OR "built environment" OR "facility management" OR
    "facilities management"
  )
  AND
  (
    sustainab* OR "environmental criteria" OR "social criteria" OR "life cycle" OR
    "risk-based maintenance"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```

**SCOPUS_NUCLEO_A4_GESTAO_ATIVOS_CICLO_VIDA**
```
TITLE-ABS-KEY(
  (
    "building asset management" OR "facility management" OR "facilities management" OR
    "building maintenance" OR "building operation" OR "operation and maintenance"
  )
  AND
  (
    "life cycle" OR "life-cycle" OR "whole life cost" OR "life cycle cost" OR
    "service life" OR durability OR "building performance" OR "asset performance"
  )
  AND
  (
    sustainab* OR "environmental performance" OR "sustainability assessment"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```

### Refinamento instrumental (não é string de coleta — uso em pós-processamento)

**SCOPUS_TAG_INSTRUMENTAL_DECISAO** — aplicar sobre o corpus núcleo já coletado (A1–A4), para
classificar quais registros citam método formal de decisão. Não usar para incluir/excluir
registros do núcleo.
```
(
  "multi-criteria" OR "multi criteria" OR multicriteria OR MCDM OR MCDA OR
  "decision support" OR "decision-making" OR priorit* OR TOPSIS OR AHP OR ANP OR
  PROMETHEE OR ELECTRE OR VIKOR OR DEMATEL OR BWM OR "best-worst method"
)
```

### Complementar tecnológico (Bloco B)

**SCOPUS_B1_COMPLEMENTAR_DIGITAL**
```
TITLE-ABS-KEY(
  (
    "smart campus" OR "intelligent building" OR "smart building" OR
    "campus infrastructure" OR "university campus" OR "higher education institution"
  )
  AND
  (
    maintenance OR "asset management" OR "facility management" OR "facilities management" OR
    "operation and maintenance" OR "predictive maintenance"
  )
  AND
  (
    "data-driven" OR predictive OR "digital twin" OR BIM OR
    "building information modeling" OR "building information modelling" OR
    IoT OR "internet of things"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```

### Conceitual exploratório (Bloco C)

**SCOPUS_C1_CONCEITUAL_EXPLORATORIO**
```
TITLE-ABS-KEY(
  (
    "built environment" OR "sustainable campus" OR "green campus" OR
    "campus sustainability" OR "regenerative building" OR "regenerative design" OR
    "living building" OR "building as a living system" OR "urban metabolism" OR
    "building metabolism" OR "biophilic building" OR "biophilic design"
  )
  AND
  (
    maintenance OR "facility management" OR "asset management" OR sustainability OR
    performance OR "ecosystem services" OR "green infrastructure" OR
    "nature-based solutions"
  )
)
AND PUBYEAR > 2009 AND PUBYEAR < 2027
```
Critério: SCOPUS_C1 não entra automaticamente no corpus principal.

---

## 2. WEB OF SCIENCE — Core Collection, busca manual, campo TS (Topic)

Busca manual pelo usuário na WoS Core Collection, Advanced Search. Exportar Full Record com
abstract. Não usar API se o acesso institucional não estiver habilitado.

**WOS_NUCLEO_A1_MANUTENCAO_SUSTENTABILIDADE**
```
TS=(("building maintenance" OR "facility management" OR "facilities management" OR "facilities maintenance" OR "building asset management" OR "building operation" OR "operation and maintenance" OR "maintenance management")
AND
(sustainab* OR "green building*" OR "life cycle" OR "life-cycle" OR "sustainability assessment" OR "sustainability indicator*" OR "environmental performance" OR "building performance"))
AND PY=(2010-2026)
```

**WOS_NUCLEO_A2_CONTEXTO_PUBLICO_UNIVERSITARIO**
```
TS=(("public building*" OR "university building*" OR "university campus" OR "higher education institution*" OR "educational building*" OR "government building*" OR "public sector building*" OR "building portfolio")
AND
("building maintenance" OR maintenance OR "facility management" OR "facilities management" OR "asset management" OR "operation and maintenance")
AND
(sustainab* OR "environmental performance" OR "life cycle" OR "sustainability assessment"))
AND PY=(2010-2026)
```

**WOS_NUCLEO_A3_PRIORIZACAO_ESTRATEGIA_MANUTENCAO**
```
TS=(("maintenance prioritization" OR "maintenance backlog" OR "deferred maintenance" OR "maintenance strategy" OR "maintenance planning" OR "renewal prioritization" OR "condition assessment" OR "condition-based maintenance")
AND
(building* OR "public building*" OR "university building*" OR campus OR "building portfolio" OR "built environment" OR "facility management" OR "facilities management")
AND
(sustainab* OR "environmental criteria" OR "social criteria" OR "life cycle" OR "risk-based maintenance"))
AND PY=(2010-2026)
```

**WOS_NUCLEO_A4_GESTAO_ATIVOS_CICLO_VIDA**
```
TS=(("building asset management" OR "facility management" OR "facilities management" OR "building maintenance" OR "building operation" OR "operation and maintenance")
AND
("life cycle" OR "life-cycle" OR "whole life cost" OR "life cycle cost" OR "service life" OR durability OR "building performance" OR "asset performance")
AND
(sustainab* OR "environmental performance" OR "sustainability assessment"))
AND PY=(2010-2026)
```

**WOS_TAG_INSTRUMENTAL_DECISAO** (mesmo uso do Scopus: classificação pós-coleta, não string de coleta)
```
("multi-criteria" OR "multi criteria" OR multicriteria OR MCDM OR MCDA OR "decision support" OR "decision-making" OR priorit* OR TOPSIS OR AHP OR ANP OR PROMETHEE OR ELECTRE OR VIKOR OR DEMATEL OR BWM OR "best-worst method")
```

**WOS_B1_COMPLEMENTAR_DIGITAL**
```
TS=(("smart campus" OR "intelligent building" OR "smart building" OR "campus infrastructure" OR "university campus" OR "higher education institution")
AND
(maintenance OR "asset management" OR "facility management" OR "facilities management" OR "operation and maintenance" OR "predictive maintenance")
AND
("data-driven" OR predictive OR "digital twin" OR BIM OR "building information modeling" OR "building information modelling" OR IoT OR "internet of things"))
AND PY=(2010-2026)
```

**WOS_C1_CONCEITUAL_EXPLORATORIO**
```
TS=(("built environment" OR "sustainable campus" OR "green campus" OR "campus sustainability" OR "regenerative building" OR "regenerative design" OR "living building" OR "building as a living system" OR "urban metabolism" OR "building metabolism" OR "biophilic building" OR "biophilic design")
AND
(maintenance OR "facility management" OR "asset management" OR sustainability OR performance OR "ecosystem services" OR "green infrastructure" OR "nature-based solutions"))
AND PY=(2010-2026)
```

Nomes de exportação padronizados:
```
wos_nucleo_a1_manutencao_sustentabilidade_YYYYMMDD.ris
wos_nucleo_a2_contexto_publico_universitario_YYYYMMDD.ris
wos_nucleo_a3_priorizacao_estrategia_manutencao_YYYYMMDD.ris
wos_nucleo_a4_gestao_ativos_ciclo_vida_YYYYMMDD.ris
wos_b1_complementar_digital_YYYYMMDD.ris
wos_c1_conceitual_exploratorio_YYYYMMDD.ris
```

---

## 3. CROSSREF — REST API, query.bibliographic

Usar com `mailto` (variável `CROSSREF_MAILTO`, já configurada em `00_CONFIG/apis_local.txt`) para
polite pool. Não depender de abstract (muitos registros não têm resumo). Crossref é reforço e
enriquecimento, não corpus analítico único.

Filtros: `from-pub-date:2010-01-01`, `until-pub-date:2026-12-31`.
Parâmetros sugeridos: `rows=100`, `sort=relevance`, `order=desc`, `cursor=*`.
Limite inicial: 300 resultados por query, ajustável após inspeção de ruído.

Núcleo — corpus principal:
```
CROSSREF_NUCLEO_A1: "building maintenance sustainability"
CROSSREF_NUCLEO_A2: "facility management sustainability building"
CROSSREF_NUCLEO_A3: "maintenance prioritization public buildings sustainability"
CROSSREF_NUCLEO_A4: "university campus building maintenance sustainability"
CROSSREF_NUCLEO_A5: "building asset management life cycle sustainability"
```

Refinamento instrumental (rodar sobre os mesmos filtros de data, usar apenas para caracterizar
subconjunto metodológico, não para compor o núcleo):
```
CROSSREF_TAG_INSTRUMENTAL_DECISAO: "building maintenance sustainability multi-criteria decision"
```

Complementar tecnológico:
```
CROSSREF_B1: "smart campus predictive maintenance digital twin facility management"
```

Conceitual exploratório:
```
CROSSREF_C1: "regenerative building maintenance sustainability built environment"
```

---

## 4. GOOGLE SCHOLAR / SERPAPI — complementar e de verificação

Não é base bibliográfica controlada equivalente a Scopus/WoS. Não somar automaticamente ao corpus
principal. Usar para: identificar artigos-chave ausentes em Scopus/WoS/Crossref, literatura aplicada
e regional, snowballing por "cited by"/"related" (quando registrado).

Parâmetros: `engine=google_scholar`, `as_ylo=2010`, `as_yhi=2026`, `num=20`,
`start=0,20,40,60,80`. Limite inicial: 100 resultados por query, com deduplicação posterior.
Registrar data/hora da coleta.

Inglês:
```
GS_A1: "building maintenance" "sustainability"
GS_A2: "facility management" "sustainability" "building"
GS_A3: "maintenance prioritization" "public buildings" "sustainability"
GS_A4: "university campus" "maintenance" "sustainability"
GS_A5: "building asset management" "life cycle" "sustainability"
GS_TAG_INSTRUMENTAL: "building maintenance" "sustainability" "multi-criteria" OR "AHP" OR "TOPSIS"
GS_B1: "smart campus" "predictive maintenance" "digital twin" "facility management"
```

Português (complementar, `as_ylo`/`as_yhi` iguais):
```
GS_PT1: "manutenção predial" "sustentabilidade"
GS_PT2: "edifícios públicos" "manutenção predial" "priorização"
```

Espanhol (complementar):
```
GS_ES1: "mantenimiento de edificios" "sostenibilidad"
GS_ES2: "gestión de activos inmobiliarios" "edificios públicos" "sostenibilidad"
```
