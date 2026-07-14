# RELATÓRIO DE NORMALIZAÇÃO — Busca de sensibilidade IA/ML

Gerado por `scripts/python/normalizar_sensibilidade_ia.py`. Três parsers dedicados (Scopus CSV, WoS RIS tag-a-tag, Crossref CSV) convergem para o schema comum de 21 campos. Reaproveita a mesma lógica de normalização de título/DOI de `consolidar_deduplicar.py`.

## Contagens de entrada/saída por base

| Base | Registros | Com DOI | % DOI | Com resumo | % resumo | Tipo doc. não mapeado |
|---|---|---|---|---|---|---|
| Scopus | 3169 | 2940 | 92.8% | 3169 | 100.0% | 13 |
| WoS | 1559 | 1456 | 93.4% | 1559 | 100.0% | 0 |
| Crossref | 2000 | 2000 | 100.0% | 498 | 24.9% | 273 |
| **Total** | **6728** | **6396** | 95.1% | **5226** | 77.7% | **286** |

## Limitação conhecida

A fatia Crossref apresenta ausência sistemática de resumo (a API do Crossref só retorna `abstract` quando o editor o submeteu — minoria dos registros). Isso é esperado e reduz a confiança da auditoria temática (Etapa 5) nessa fatia — registros sem resumo são auditados apenas por título/palavras-chave/periódico, com `nivel_confianca` rebaixado por definição salvo termo IA/ML inequívoco no próprio título. Não é uma falha de normalização, é uma limitação de cobertura da fonte.

## Tipos documentais não mapeados na harmonização

- [nao_mapeado] Data paper
- [nao_mapeado] Erratum
- [nao_mapeado] Letter
- [nao_mapeado] Retracted
- [nao_mapeado] dataset
- [nao_mapeado] edited-book
- [nao_mapeado] journal-issue
- [nao_mapeado] other
- [nao_mapeado] peer-review
- [nao_mapeado] posted-content
- [nao_mapeado] proceedings
- [nao_mapeado] report
