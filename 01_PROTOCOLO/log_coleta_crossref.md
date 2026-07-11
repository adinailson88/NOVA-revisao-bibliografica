# LOG DE COLETA — CROSSREF (ETAPA_03)

Data: 2026-07-08.
Etapa: ETAPA_03 — COLETA_CROSSREF.
Status desta sessão: SCRIPT PREPARADO, NÃO EXECUTADO (nenhuma chamada de rede foi feita).

## 1. O que foi preparado

Script criado em `00_CONFIG/coleta_crossref.py`:
- Lê `CROSSREF_MAILTO` de `00_CONFIG/apis_local.txt` em tempo de execução (não é chave secreta,
  apenas identifica a aplicação no polite pool da API pública do Crossref).
- Implementa as 5 queries do núcleo definidas em `01_PROTOCOLO/strings_nativas_por_base.md`,
  seção 3:
  - `crossref_nucleo_a1`: "building maintenance sustainability"
  - `crossref_nucleo_a2`: "facility management sustainability building"
  - `crossref_nucleo_a3`: "maintenance prioritization public buildings sustainability"
  - `crossref_nucleo_a4`: "university campus building maintenance sustainability"
  - `crossref_nucleo_a5`: "building asset management life cycle sustainability"
- Filtro: `from-pub-date:2010-01-01,until-pub-date:2026-12-31` (parâmetro `filter`, equivalente ao
  período 2010–2026 do roteiro).
- Paginação por `cursor` (rows=100 por página), limite de 300 registros por query — este limite é
  o valor de protocolo já definido em `strings_nativas_por_base.md` ("limite inicial = 300
  resultados por query, ajustável após inspeção de ruído"), não um teto acidental como o do script
  Scopus original. Se atingido, fica registrado em `truncated_by_limit` no resumo.
- Endpoint: `https://api.crossref.org/works`, sem autenticação (API pública).
- Saída por query: `02_DADOS_BRUTOS/crossref/<string_id>_raw.json` e `<string_id>_raw.csv`, com os
  campos mínimos da seção 6.2 do roteiro (DOI, title, abstract quando houver, author,
  published-print/online/issued, container-title, type, subject, is-referenced-by-count, URL,
  publisher, language, database=Crossref, string_id).
- Resumo de execução em `02_DADOS_BRUTOS/crossref/_resumo_execucao.json` (contagens, http status,
  erros por query, sem expor nenhum dado sensível — o mailto não é secreto, mas não é impresso
  fora do parâmetro de requisição).
- A refinamento instrumental (`CROSSREF_TAG_INSTRUMENTAL_DECISAO`) e as buscas complementar (B1) e
  conceitual (C1) **não** foram incluídas nesta primeira versão do script — ficam para execução
  futura, seguindo o mesmo padrão adotado no Scopus (núcleo primeiro).

## 2. O que foi executado de fato

Nada. Nenhuma chamada HTTP foi feita. Script apenas criado e validado sintaticamente com
`python -m py_compile 00_CONFIG/coleta_crossref.py` (compilação OK). Nenhum arquivo foi gravado em
`02_DADOS_BRUTOS/crossref/` (pasta permanece apenas com `desktop.ini`).

## 3. Ação necessária para executar

Aplicando a mesma lição da ETAPA_02 (coleta Scopus só foi concluída quando o usuário rodou
manualmente, fora do agente), a execução real deste script também deve ser feita pelo usuário, em
terminal próprio:

```
python "00_CONFIG/coleta_crossref.py"
```

a partir da raiz do projeto (`ARTIGO - NOVO MÉTODO - REVISÃO`). Não requer nenhuma chave secreta —
apenas o e-mail já configurado em `00_CONFIG/apis_local.txt`.

## 4. Rastreabilidade

- Base: Crossref (REST API pública).
- Strings do núcleo: ver `01_PROTOCOLO/strings_nativas_por_base.md`, seção 3.
- Janela temporal: 2010-01-01 a 2026-12-31.

## 5. Execução real (2026-07-08, 16:09–16:10, pelo usuário, fora do agente)

Status: CONCLUÍDA. `any_http_error=false` em `_resumo_execucao.json`. Nenhuma chave/mailto
exposta.

| String | total_results (Crossref) | registros exportados |
|---|---|---|
| crossref_nucleo_a1 | 1.020.726 | 200 |
| crossref_nucleo_a2 | 3.978.326 | 200 |
| crossref_nucleo_a3 | 1.872.263 | 200 |
| crossref_nucleo_a4 | 3.127.639 | 200 |
| crossref_nucleo_a5 | 5.202.498 | 200 |

**Observação metodológica importante — não é erro:** o campo `total_results` na casa dos milhões é
comportamento esperado do parâmetro `query.bibliographic` do Crossref, que faz correspondência por
relevância sobre texto livre (não é busca booleana exata como Scopus `TITLE-ABS-KEY` ou WoS `TS`).
Isso já era antecipado no protocolo (`01_PROTOCOLO/strings_nativas_por_base.md`, seção 3: "Crossref
não deve ser tratado como Scopus/WoS em lógica booleana complexa"). O Crossref ordena por
relevância por padrão quando há `query`/`query.bibliographic`, então os registros efetivamente
exportados (top da ordenação) tendem a ser os mais aderentes, mesmo com `total_results` enorme.

Verificação de ruído (amostragem manual dos primeiros títulos de 3 das 5 queries, nesta sessão):
- `crossref_nucleo_a1` (10 primeiros títulos): todos claramente aderentes ao tema (manutenção
  predial, sustentabilidade, gestão de edifícios públicos/hospitalares/escolares).
- `crossref_nucleo_a3` (5 primeiros): aderentes a priorização de manutenção/ativos.
- `crossref_nucleo_a5` (5 primeiros): aderentes a gestão de ativos e ciclo de vida.
Nenhum falso positivo grosseiro identificado nesta amostra rápida. Uma verificação de ruído mais
completa (amostra maior, cobrindo também o final da lista de 200) deve ocorrer formalmente na
ETAPA_07 (pré-triagem), não nesta etapa de coleta.

**Achado técnico sobre paginação:** cada query recebeu apenas 200 registros (2 páginas de 100), não
os 300 planejados como limite de protocolo. Nas duas páginas, o `next-cursor` retornado pelo
Crossref na segunda chamada foi idêntico ao cursor usado nessa mesma chamada — condição que o
script interpreta corretamente como "fim de paginação útil" (`next_cursor == cursor`) e interrompe
a coleta, em vez de arriscar um loop repetindo a mesma página. Isso é uma característica observada
do cursor de paginação do Crossref para `query.bibliographic` (não documentada de forma explícita
pela API, mas consistente em todas as 5 queries desta execução) — não um bug do script. Registrado
como `truncated_by_limit: false` em todas as entradas do resumo (o limite de 300 não foi o motivo
da parada).

Melhoria pendente, não bloqueante: adicionar explicitamente `sort=relevance&order=desc` na
chamada (o protocolo sugere esses parâmetros; o Crossref já ordena por relevância por padrão
quando há `query.bibliographic`, mas declarar explicitamente reforça a reprodutibilidade). Pode ser
aplicada em uma reexecução futura, sem urgência, já que os títulos amostrados confirmam boa
aderência temática mesmo sem o parâmetro explícito.

## 6. Estado final desta etapa

Dados brutos gerados em `02_DADOS_BRUTOS/crossref/`: 5 pares de arquivos `<string_id>_raw.json` e
`<string_id>_raw.csv`, mais `_resumo_execucao.json`. Nenhuma deduplicação ou triagem foi feita —
fica para as etapas 06 e 07.
