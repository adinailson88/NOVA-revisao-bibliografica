# Mapa de triagem e auditoria

## Camadas documentadas

| Camada | Universo | Mecanismo | Campos | Verificação humana | Resultado |
|---|---:|---|---|---|---:|
| Pré-triagem | 9.542 | Regras determinísticas em Python, sem LLM | Título e resumo | Não integral | Cinco classes |
| Auditoria amostral | 100 | Leitura individual, amostra estratificada, semente 42 | Título e resumo | Avaliador único | 34 ajustes |
| Resolução das dúvidas | 4.276 | Decisões preservadas em TSV e aplicadas por R | ID, decisão, confiança, regra e justificativa | Sem segundo avaliador documentado | 206 relevantes; 4.070 descartes |
| Reavaliação dos resumos | 3.678 | Regras determinísticas em R, sem LLM | Título, resumo, palavras-chave e campos extraídos | Regras aprovadas pelo pesquisador | 372 fortes; 830 descritivos; 157 contextuais; 2.319 descartes |
| Alinhamento às RQs | 3.678 | Dicionários e pontuação determinística em R, sem LLM | Título, resumo, palavras-chave e campos extraídos | Sem revisão independente documentada | 137 centrais |
| Auditoria qualitativa | 137 | Decisão estruturada registro a registro | Título, resumo, palavras-chave e campos extraídos | Avaliador único | 104 principais; 21 secundários; 3 mapeamento; 9 exclusões |

## Cobertura

- Auditoria amostral: 100 de 9.542 registros, ou 1,0%.
- Concordância inicial na amostra: 66 de 100; 34 classificações alteradas.
- Resolução das dúvidas: 4.276 de 4.276 registros com decisão preservada.
- Auditoria qualitativa: 137 de 137 registros com decisão preservada.
- Leitura de texto completo: não realizada nessas camadas.

## IA e ASReview

Os scripts e relatórios da pré-triagem, da reavaliação e do alinhamento registram explicitamente regras determinísticas e ausência de LLM. Os arquivos da auditoria qualitativa não registram ferramenta de IA, modelo, versão ou prompt; portanto, essa auditoria não é atribuída a IA no artigo. O campo `asreview_label_compativel` é apenas compatibilidade de formato e não comprova execução do ASReview.

## Independência e conflitos

Não houve segundo avaliador independente. A documentação não registra cálculo de concordância entre revisores nem procedimento de consenso ou arbitragem. As alterações da amostra e as decisões finais permanecem rastreáveis nos arquivos de triagem.
