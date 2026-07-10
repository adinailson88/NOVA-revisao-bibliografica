"""
Auditoria da triagem por amostra estratificada (ETAPA_08 - AUDITORIA_TRIAGEM).

Rodada de 2026-07-09, sobre o corpus_consolidado.csv reprocessado (9.542 registros, 94% com
resumo, apos enriquecimento manual do resumo da Scopus -- ver 00_CONTROLE/ESTADO_ATUAL.md) e sobre
o pre_triagem.py com vocabulario ampliado nesta mesma sessao (5 termos novos no Bloco A, 5 no
Bloco B -- ver 00_CONTROLE/DECISOES_METODOLOGICAS.md, entrada de 2026-07-09). Substitui a rodada de
2026-07-08 (corpus antigo, 20% com resumo, vocabulario sem os termos novos) -- a amostra anterior
nao e mais representativa da composicao atual do corpus e nao pode ser reaproveitada.

Le a matriz da ETAPA_07 (04_TRIAGEM/matriz_pre_triagem.csv) e a amostra estratificada sorteada por
00_CONFIG/amostrar_auditoria.py (semente fixa 42, reprodutivel -- mesma semente da rodada anterior,
mas amostra diferente porque a populacao de origem mudou). Cada um dos 100 registros da amostra foi
lido individualmente (titulo + resumo) e julgado contra os criterios A (objeto predial) + B
(sustentabilidade) do roteiro-mestre. As correcoes abaixo (AJUSTES) tem justificativa textual
amarrada ao conteudo lido -- nao sao reclassificacao automatica, mas tambem nao usam nenhuma
informacao externa ao que ja estava no corpus (nenhum achado foi "inventado").

Escopo: apenas os 100 registros amostrados foram auditados individualmente. Os outros 9.442
registros do corpus mantem a classe da ETAPA_07 sem verificacao humana/assistida -- ver
04_TRIAGEM/relatorio_ajustes_triagem.md para o porque disso nao ser um problema nesta etapa
(auditoria por amostra, nao reclassificacao integral) e para os padroes sistematicos encontrados
(lacunas de vocabulario e de rigidez de frase residuais) que deveriam orientar um proximo
refinamento do classificador, se decidido pelo usuario.

Saidas:
- 04_TRIAGEM/matriz_triagem_auditada.csv (9.542 linhas -- classe_pre_triagem preservada +
  classe_auditada + auditado + justificativa_auditoria)
- 04_TRIAGEM/relatorio_ajustes_triagem.md
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIAGEM_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "matriz_pre_triagem.csv")
AMOSTRA_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "_amostra_auditoria_bruta.csv")
MATRIZ_AUDITADA_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "matriz_triagem_auditada.csv")
RELATORIO_PATH = os.path.join(BASE_DIR, "04_TRIAGEM", "relatorio_ajustes_triagem.md")

# Ajustes decididos apos leitura individual de titulo+resumo de cada um dos 100 registros da
# amostra de 2026-07-09 (ver 04_TRIAGEM/_amostra_auditoria_bruta.csv). Chave = id_unico; valor =
# (nova_classe, justificativa). Registros da amostra NAO listados aqui foram lidos e CONFIRMADOS na
# classe da ETAPA_07 (concordancia, sem ajuste).
AJUSTES = {
    # --- amostra "relevante" da ETAPA_07: 11 de 30 ajustados ---
    "REG_02609": ("complementar", (
        "Sistema de gerenciamento de informacao predial via Blockchain/BIM/IoT/Self Sovereign "
        "Identity -- objeto predial real (BIM, ciclo de vida do artefato predial), mas "
        "'life cycle' aparece so como termo de rastreabilidade/gestao de informacao, nao como "
        "criterio de sustentabilidade ambiental/social/economica analisado no estudo. Encaixa "
        "melhor como complementar tecnologico (BIM + blockchain + IoT) do que nucleo A+B."
    )),
    "REG_03629": ("irrelevante", (
        "Placemaking como abordagem de 'sustainable urban facilities management' -- o objeto real "
        "e planejamento urbano/engajamento comunitario em espacos publicos (placemaking), nao "
        "gestao de edificacoes. Roteiro exclui infraestrutura urbana generica sem edificacao."
    )),
    "REG_03530": ("irrelevante", (
        "Economia circular na India: politica nacional de gestao de residuos (EPA 1986 e normas "
        "correlatas) -- sem qualquer relacao com edificacao ou manutencao/gestao predial."
    )),
    "REG_00048": ("irrelevante", (
        "Servicos de informacao ao viajante em rodovias (HiTISS) -- sistema de transporte urbano/ "
        "mobilidade rodoviaria, sem edificacao."
    )),
    "REG_03692": ("irrelevante", (
        "Avaliacoes de sustentabilidade na construcao feitas por estudantes, estudo de caso LEED "
        "lab -- foco e aprendizagem/avaliacao pedagogica de estudantes sobre sustentabilidade, nao "
        "gestao/manutencao do edificio em si. Mesmo padrao ja identificado na auditoria anterior "
        "(educacao para sustentabilidade != gestao predial, ver REG_09325 da rodada de 2026-07-08)."
    )),
    "REG_02435": ("irrelevante", (
        "Predicao de vida util restante de bomba de engrenagem (equipamento hidraulico industrial) "
        "via deep learning -- manutencao preditiva de maquina industrial, sem qualquer relacao com "
        "edificacoes. Exclusao explicita do roteiro (manutencao industrial/maquinas sem ponte com "
        "edificacoes)."
    )),
    "REG_03335": ("irrelevante", (
        "Ontologia IFCInfra4OM para integrar informacao de operacao e manutencao em modelagem de "
        "informacao de rodovias (BIM para infraestrutura de transporte) -- nao e edificacao. "
        "Mesmo padrao ja identificado na auditoria anterior (infraestrutura de transporte sem "
        "ponte com edificacoes, ver REG_06030 da rodada de 2026-07-08)."
    )),
    "REG_00420": ("irrelevante", (
        "Sistema de gestao de manutencao (TPM/Six Sigma) para equipamentos de servico em geral "
        "(medicao de emissao, seguranca, condicionamento ambiental) -- manutencao industrial "
        "generica, sem relacao especifica com edificacoes."
    )),
    "REG_07861": ("irrelevante", (
        "Visao geral da manutencao de sistemas publicos de esgotamento sanitario na Croacia -- "
        "infraestrutura de saneamento; 'buildings' aparece so como fonte de efluente sanitario, "
        "nao como objeto de manutencao. Mesmo padrao da auditoria anterior (infraestrutura "
        "hidrica/saneamento sem edificacao, ver REG_01547 da rodada de 2026-07-08)."
    )),
    "REG_06680": ("irrelevante", (
        "Modelagem de corrosao de juntas soldadas em instalacoes de energia eolica offshore -- "
        "usina de geracao de energia, nao edificacao."
    )),
    "REG_03515": ("complementar", (
        "Comparacao de ontologias (Brick, Project Haystack) para Building Automation System (BAS) "
        "e aplicacoes de smart building -- eficiencia energetica aparece so como motivacao "
        "contextual ('ultimately attaining peak performance in energy use'), nao como criterio de "
        "sustentabilidade efetivamente analisado no estudo. Melhor classificado como complementar "
        "tecnologico (bloco A + termo tecnologico 'smart building')."
    )),

    # --- amostra "irrelevante" da ETAPA_07: 4 de 30 ajustados para `duvida` (falsos negativos por "
    #     rigidez de frase, distintos dos 5 termos de vocabulario adicionados nesta sessao) ---
    "REG_08588": ("duvida", (
        "Priorizacao de manutencao/reabilitacao de edificios escolares publicos via problema da "
        "mochila (knapsack) sob restricao orcamentaria -- objeto predial real (edificios "
        "escolares, alocacao de recursos), mas sem termo de sustentabilidade explicito no texto "
        "lido. Bloco A nao foi capturado pelo classificador por rigidez de frase: o titulo diz "
        "'Maintenance and Rehabilitation Prioritization of School Buildings', que nao contem a "
        "sequencia literal 'maintenance prioritization' (interrompida por 'and Rehabilitation'). "
        "Falso negativo por rigidez de frase, nao por lacuna de vocabulario dos termos novos "
        "adicionados nesta sessao."
    )),
    "REG_08115": ("duvida", (
        "Priorizacao de tarefas de manutencao baseada em risco para um 'large facility portfolio' "
        "-- objeto predial real (portfolio de instalacoes, hierarquias de instalacao, sistema de "
        "apoio a decisao para manutencao), mas sem termo de sustentabilidade explicito no texto "
        "lido. Bloco A nao capturado por rigidez singular/plural: o texto usa 'facility "
        "maintenance'/'facility portfolio' (singular), enquanto a lista do classificador tem "
        "'facilities maintenance' (plural) e 'building portfolio' (nao 'facility portfolio')."
    )),
    "REG_08613": ("duvida", (
        "Avaliacao de edificios publicos desativados para fins de reuso (estruturas de saude "
        "historicas italianas), com mapeamento GIS e triagem de ativos publicos -- objeto predial "
        "real (edificios publicos, patrimonio historico, reuso), mas nenhuma frase de Bloco A/B "
        "foi capturada literalmente pelo classificador (menciona 'public assets' generico, nao "
        "'public asset management'; motivacao em '2030 European Agenda'/'Recovery and Resilience "
        "Plan', sem termo de sustentabilidade explicito). Falso negativo por lacuna de vocabulario "
        "residual, fora dos termos adicionados nesta rodada."
    )),
    "REG_07764": ("duvida", (
        "Reinterpretacao de hierarquias arquitetonicas centenarias para bibliotecas publicas "
        "(bibliotecas Carnegie), usando HBIM (historic building information modelling) -- objeto "
        "predial real (edificios publicos patrimoniais, reuso), mas sem frase de Bloco A "
        "capturada literalmente (menciona 'building information modelling' para patrimonio, nao "
        "'building maintenance'/'facility management') e sem termo de sustentabilidade explicito "
        "no texto lido."
    )),

    # --- amostra "duvida" da ETAPA_07: 19 de 20 ajustados (17 para irrelevante, 1 para "
    #     complementar, 1 para relevante) ---
    # Confirma o padrao ja identificado na rodada de 2026-07-08: dentro de `duvida`, o subgrupo
    # "apenas Bloco B presente" (linguagem generica de sustentabilidade/ciclo de vida, comum em
    # varios dominios de engenharia, sem Bloco A real) tem taxa de acerto muito baixa -- a leitura
    # confirma que o objeto NAO e edificacao na quase totalidade dos casos lidos nesta rodada
    # (agua/saneamento, petroleo/gas, energia solar/eolica/biomassa, ferrovia, blockchain,
    # geotecnia geral, seguranca eletrica industrial, educacao para sustentabilidade). Reforca a
    # recomendacao ja registrada (secao 5) de tratar 'apenas Bloco B' como subclasse separada de
    # 'apenas Bloco A' num proximo refinamento do classificador.
    "REG_09255": ("irrelevante", (
        "Framework de IA/redes sem fio 5G para gestao administrativa/alocacao de recursos em "
        "'smart campus' -- decisao institucional/orcamentaria, sem objeto predial real (manutencao/"
        "operacao de edificacoes). Mesmo padrao da auditoria anterior (ver REG_09251, rodada de "
        "2026-07-08)."
    )),
    "REG_02220": ("irrelevante", (
        "Diretrizes para tomadores de decisao sobre trilhos e infraestrutura de trem de alta "
        "velocidade -- infraestrutura ferroviaria de transporte, sem edificacao."
    )),
    "REG_09317": ("irrelevante", (
        "Framework analitico para 'brokering' de parcerias comunidade-campus -- parceria "
        "organizacional/social entre instituicoes academicas e comunidade; 'campus' aparece so "
        "como contexto institucional, nao como objeto predial."
    )),
    "REG_05536": ("irrelevante", (
        "Revisao sistematica de falhas em sistemas urbanos de abastecimento de agua e saneamento "
        "na Africa Subsaariana -- infraestrutura hidrica, sem edificacao."
    )),
    "REG_03958": ("irrelevante", (
        "IA para operacao e manutencao preditiva de sistemas de coleta de petroleo bruto (dutos) "
        "-- infraestrutura industrial de oleo e gas (corrosao interna, parafina, deposicao em "
        "dutos), sem qualquer relacao com edificacoes no texto lido."
    )),
    "REG_03653": ("irrelevante", (
        "Fatores de viabilidade economica de investimentos em energia fotovoltaica -- geracao de "
        "energia solar, sem edificacao."
    )),
    "REG_09336": ("irrelevante", (
        "Conhecimento e expectativas sobre sistemas alimentares sustentaveis entre estudantes "
        "universitarios georgianos -- educacao para sustentabilidade alimentar, nao gestao "
        "predial. Mesmo padrao de exclusao ja identificado (educacao para sustentabilidade != "
        "gestao predial)."
    )),
    "REG_04459": ("irrelevante", (
        "Fundo global de acesso a agua para cobrir deficits de operacao e manutencao de "
        "concessionarias de agua -- financiamento de infraestrutura hidrica/saneamento, sem "
        "edificacao."
    )),
    "REG_04286": ("irrelevante", (
        "Programa de seguranca eletrica (NFPA 70E) em empresa petroquimica -- seguranca "
        "ocupacional em instalacao industrial, sem relacao com gestao/manutencao predial."
    )),
    "REG_03695": ("irrelevante", (
        "Governanca blockchain como mecanismo de coordenacao entre stakeholders de uma cadeia de "
        "valor -- 'maintenance' aqui refere-se a manutencao de infraestrutura de rede blockchain "
        "(tecnologica), nao edificacao."
    )),
    "REG_07104": ("irrelevante", (
        "O que engenheiros geotecnicos querem saber sobre confiabilidade -- metodologia de "
        "confiabilidade geotecnica para sistemas de engenharia em geral (geoazardos, fundacoes), "
        "sem foco especifico em edificacoes no texto lido."
    )),
    "REG_01871": ("irrelevante", (
        "Abordagem de custo de ciclo de vida (LCCA) para entrega sustentavel de servicos de agua "
        "na zona rural de Andhra Pradesh, India -- setor WASH (agua, saneamento e higiene), "
        "infraestrutura hidrica rural, sem edificacao."
    )),
    "REG_06813": ("irrelevante", (
        "Viabilidade tecnico-economica RETScreen de projeto de usina solar fotovoltaica flutuante "
        "de 145 MW na Indonesia -- geracao de energia solar, sem edificacao."
    )),
    "REG_03361": ("irrelevante", (
        "Otimizacao de infraestrutura de TIC em ruas de cidades inteligentes na India -- "
        "infraestrutura urbana de tecnologia da informacao em nivel de rua, sem edificacao. "
        "Exclusao explicita do roteiro (smart city sem edificacao)."
    )),
    "REG_09486": ("complementar", (
        "Parede viva (living wall) para paisagismo em ambiente educacional, instalada na fachada "
        "de um predio da Faculdade de Belas Artes e Design (campus universitario na Turquia) -- "
        "mais proximo do bloco conceitual (biophilic design/green infrastructure) do que do "
        "nucleo A+B, ja que o estudo trata do desempenho do sistema vegetal/paisagistico, nao de "
        "manutencao ou gestao do edificio em si."
    )),
    "REG_01361": ("irrelevante", (
        "Analise economica e ambiental de aquecimento descentralizado por gaseificacao de biomassa "
        "e biogas domestico em area rural da China -- comparacao de tecnologias de aquecimento em "
        "nivel domiciliar, sem gestao/manutencao predial como objeto."
    )),
    "REG_09160": ("irrelevante", (
        "Sistemas de reabilitacao de tubulacoes para extensao de vida util (tecnologia sem "
        "trincheira/trenchless) -- infraestrutura subterranea de dutos, sem edificacao."
    )),
    "REG_00669": ("relevante", (
        "Avaliacao de sistema de isolamento termico (retrofit de envoltoria construtiva) em "
        "edificios institucionais/administrativos da UE, com monitoramento continuo de flutuacoes "
        "climaticas sazonais/diarias -- objeto predial real (edificios institucionais, retrofit de "
        "envoltoria) e sustentabilidade real e explicita no texto lido ('energy sustainability "
        "point of view', 'energy efficiency of buildings maintenance'). Falso negativo: Bloco A "
        "nao foi capturado por rigidez singular/plural -- o texto usa 'buildings maintenance' "
        "(plural), a lista do classificador tem 'building maintenance' (singular)."
    )),
    "REG_09104": ("irrelevante", (
        "Gestao de recursos florestais, avaliacao de ciclo de vida e certificacao florestal -- "
        "madeira como materia-prima aparece so como exemplo de material de construcao ('wood as a "
        "building material'), nao ha operacao/manutencao/gestao predial como objeto do estudo. "
        "Exclusao explicita do roteiro (estudos apenas sobre materiais de construcao sem ponte "
        "com operacao/manutencao predial)."
    )),
    # REG_09209 (duvida, Bloco A presente/Bloco B ausente -- preocupacoes de gestores de instalacoes
    # de governos locais noruegueses, edificios publicos mencionados explicitamente) foi lido e
    # CONFIRMADO sem ajuste: objeto predial real (facility management, edificios publicos), mas
    # genuinamente sem termo de sustentabilidade no texto lido (preocupacao fiscal/orcamentaria e
    # condicao fisica, nao ambiental) -- fronteira genuina, nao falso negativo.
}

# Registros da amostra "sem_resumo" (20 registros): nenhum ajustado nesta rodada, mesma regra da
# rodada anterior -- roteiro-mestre secao 13 exige tentativa de enriquecimento antes de decidir por
# titulo isolado. Titulos lidos sao coerentes com o sinal_titulo calculado na ETAPA_07: titulos
# claramente prediais com sustentabilidade explicita ("Buildings Sustainability Certifications...",
# "Prioritization of Sustainability Dimensions and Indicators for Office Buildings", "Building
# Envelopes: A Passive Way to Achieve Energy Sustainability...") tem sinal positivo; titulos
# claramente fora de escopo ("An efficient implementation of the Gale and Shapley...", "Enhancing
# Safety and Security in Renewable Energy Systems within Smart Cities") tem sem_sinal.


def main():
    with open(TRIAGEM_PATH, encoding="utf-8-sig", newline="") as f:
        leitor = csv.DictReader(f)
        campos = leitor.fieldnames + ["classe_auditada", "auditado", "justificativa_auditoria"]
        registros = list(leitor)

    with open(AMOSTRA_PATH, encoding="utf-8-sig", newline="") as f:
        ids_amostrados = {r["id_unico"] for r in csv.DictReader(f)}

    n_auditados = 0
    n_ajustados = 0
    for row in registros:
        id_ = row["id_unico"]
        if id_ in ids_amostrados:
            n_auditados += 1
            row["auditado"] = "sim"
            if id_ in AJUSTES:
                nova_classe, motivo = AJUSTES[id_]
                row["classe_auditada"] = nova_classe
                row["justificativa_auditoria"] = f"AJUSTADO ({row['classe_pre_triagem']} -> {nova_classe}): {motivo}"
                n_ajustados += 1
            else:
                row["classe_auditada"] = row["classe_pre_triagem"]
                row["justificativa_auditoria"] = "Confirmado apos leitura individual de titulo+resumo -- classe da ETAPA_07 mantida."
        else:
            row["auditado"] = "nao"
            row["classe_auditada"] = row["classe_pre_triagem"]
            row["justificativa_auditoria"] = "Nao incluido na amostra estratificada desta etapa -- classe da ETAPA_07 nao verificada individualmente."

    with open(MATRIZ_AUDITADA_PATH, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for row in registros:
            w.writerow(row)

    # ---- estatisticas para o relatorio ----
    por_estrato = {}
    with open(AMOSTRA_PATH, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            por_estrato.setdefault(r["estrato"], []).append(r["id_unico"])

    linhas_estrato = []
    for estrato, ids in por_estrato.items():
        ajustados = [id_ for id_ in ids if id_ in AJUSTES]
        linhas_estrato.append((estrato, len(ids), len(ajustados)))

    destino_ajustes = {}
    for id_, (nova, _) in AJUSTES.items():
        destino_ajustes[nova] = destino_ajustes.get(nova, 0) + 1

    # Cruzamento Bloco C / Bloco D x classe sobre o corpus completo (nao so a amostra), para o
    # controle de vies pedido pelo prompt da etapa -- recalculado nesta rodada sobre o
    # matriz_pre_triagem.csv atual (9.542 registros).
    bloco_c_por_classe = {}
    bloco_d_por_classe = {}
    with open(TRIAGEM_PATH, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            cls = r["classe_pre_triagem"]
            if r["bloco_c_presente"] == "sim":
                bloco_c_por_classe[cls] = bloco_c_por_classe.get(cls, 0) + 1
            if r["bloco_d_presente"] == "sim":
                bloco_d_por_classe[cls] = bloco_d_por_classe.get(cls, 0) + 1

    rel = []
    rel.append("# RELATORIO DE AJUSTES DA TRIAGEM -- ETAPA_08\n")
    rel.append(
        "Gerado por `00_CONFIG/auditoria_triagem.py`, a partir da leitura individual (titulo + "
        "resumo) dos 100 registros da amostra estratificada sorteada por "
        "`00_CONFIG/amostrar_auditoria.py` (semente fixa 42, reprodutivel). Cada julgamento usa "
        "apenas o conteudo ja presente em `03_PROCESSADOS/corpus_consolidado.csv` -- nenhum achado "
        "externo foi adicionado. **Rodada de 2026-07-09**, sobre o corpus reprocessado (9.542 "
        "registros, 94% com resumo) e o classificador com vocabulario ampliado nesta mesma sessao "
        "-- substitui integralmente a rodada de 2026-07-08 (corpus antigo, 20% com resumo, amostra "
        "diferente por a populacao de origem ter mudado). Ver "
        "`00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09, para o detalhe da mudanca "
        "de vocabulario.\n"
    )

    rel.append("## 1. Composicao da amostra e taxa de ajuste por estrato\n")
    rel.append("| Estrato (classe ETAPA_07) | N amostrado | N ajustado | % ajustado |")
    rel.append("|---|---|---|---|")
    for estrato, n, n_adj in sorted(linhas_estrato, key=lambda x: -x[1]):
        rel.append(f"| {estrato} | {n} | {n_adj} | {100*n_adj/n:.0f}% |")
    total_amostra = sum(n for _, n, _ in linhas_estrato)
    total_ajustes = sum(n_adj for _, _, n_adj in linhas_estrato)
    rel.append(f"| **Total** | **{total_amostra}** | **{total_ajustes}** | **{100*total_ajustes/total_amostra:.0f}%** |\n")
    rel.append(
        f"Taxa de concordancia entre ETAPA_07 (automatica) e a leitura individual desta auditoria: "
        f"{100*(total_amostra-total_ajustes)/total_amostra:.0f}% ({total_amostra-total_ajustes} de "
        f"{total_amostra} confirmados sem alteracao). Taxa de ajuste bem mais alta que a rodada de "
        "2026-07-08 (23%), principalmente por causa do estrato `duvida`: com 94% do corpus agora "
        "com resumo (contra 20% antes), a amostra `duvida` desta rodada e dominada pelo padrao "
        "'apenas Bloco B presente' (sustentabilidade generica de outros dominios de engenharia sem "
        "objeto predial real), que a rodada anterior ja havia identificado como tendo baixa taxa de "
        "acerto -- ver secao 3.3.\n"
    )

    rel.append("## 2. Para onde foram os ajustes\n")
    rel.append("| Classe destino do ajuste | N registros |")
    rel.append("|---|---|")
    for destino, n in sorted(destino_ajustes.items(), key=lambda kv: -kv[1]):
        rel.append(f"| {destino} | {n} |")
    rel.append("")

    rel.append("## 3. Padroes encontrados e ajustes individuais\n")

    rel.append("### 3.1 Amostra `relevante` (30 registros, 11 ajustados)\n")
    rel.append(
        "Taxa de ajuste bem mais alta que a rodada anterior (37% contra 13%) -- padrao "
        "predominante: Bloco A validado por termo fraco generico ('operation and maintenance', "
        "'facility'/'facilities' como token de contexto) em registros cujo objeto real e "
        "infraestrutura industrial, de transporte, hidrica ou energetica, sem edificacao "
        "(bombas hidraulicas industriais, rodovias, esgotamento sanitario, usinas eolicas "
        "offshore, sistemas de gestao de manutencao TPM genericos). Dois casos adicionais "
        "(REG_02609, REG_03515) tinham objeto predial real mas sustentabilidade so como motivacao "
        "contextual, nao como criterio efetivamente analisado -- reclassificados como complementar "
        "tecnologico.\n"
    )
    for id_, (nova, motivo) in AJUSTES.items():
        estrato_origem = next((e for e, ids in por_estrato.items() if id_ in ids), "?")
        if estrato_origem == "relevante":
            rel.append(f"- **{id_}** ({estrato_origem} -> {nova}): {motivo}")
    rel.append("")

    rel.append("### 3.2 Amostra `irrelevante` (30 registros, 4 ajustados para `duvida`)\n")
    rel.append(
        "Os 4 ajustes sao falsos negativos por **rigidez de frase** do classificador -- distintos "
        "dos 5 termos de vocabulario adicionados nesta sessao (retrofit, building stock "
        "management, building modernization, built asset management, public asset management), "
        "que ja foram incorporados ao `pre_triagem.py` antes desta rodada rodar. Os 4 casos "
        "encontrados agora sao problemas de correspondencia literal (singular/plural, ordem de "
        "palavras, frase interrompida por outra palavra) em registros com objeto predial real: "
        "'facility maintenance' (singular) vs. 'facilities maintenance' (lista, plural); "
        "'Maintenance and Rehabilitation Prioritization' (frase interrompida) vs. 'maintenance "
        "prioritization' (lista, contigua); 'public assets' generico vs. 'public asset management' "
        "(lista); 'building information modelling' para patrimonio historico, sem frase de Bloco A "
        "correspondente.\n"
    )
    for id_, (nova, motivo) in AJUSTES.items():
        estrato_origem = next((e for e, ids in por_estrato.items() if id_ in ids), "?")
        if estrato_origem == "irrelevante":
            rel.append(f"- **{id_}** ({estrato_origem} -> {nova}): {motivo}")
    rel.append("")

    rel.append("### 3.3 Amostra `duvida` (20 registros, 19 ajustados)\n")
    rel.append(
        "Taxa de ajuste ainda mais alta que a rodada anterior (95% contra 65%). Confirma "
        "fortemente o padrao ja identificado em 2026-07-08: dentro de `duvida`, o subgrupo "
        "'apenas Bloco B presente' (linguagem generica de sustentabilidade/ciclo de vida, comum em "
        "varios dominios de engenharia) tem taxa de acerto muito baixa quando o objeto real e "
        "verificado por leitura -- nesta rodada, 16 dos 17 casos 'apenas Bloco B' lidos eram "
        "genuinamente fora do escopo do artigo (agua/saneamento, petroleo e gas, energia solar/"
        "eolica/biomassa, ferrovia, governanca blockchain, geotecnia generica, seguranca eletrica "
        "industrial, educacao para sustentabilidade, parceria comunidade-campus, certificacao "
        "florestal), e apenas 1 (REG_00669) era um falso negativo genuino (retrofit de envoltoria "
        "em edificios institucionais da UE, com sustentabilidade explicita no texto -- Bloco A nao "
        "capturado por rigidez singular/plural: 'buildings maintenance' no texto vs. 'building "
        "maintenance' na lista). O unico caso 'apenas Bloco A presente' da amostra (REG_09209) foi "
        "confirmado sem ajuste -- fronteira genuina, nao falso negativo (ver nota apos o dicionario "
        "AJUSTES em `00_CONFIG/auditoria_triagem.py`). Um caso (REG_09486, parede viva/biophilic em "
        "fachada de predio universitario) foi reclassificado para `complementar` por se encaixar "
        "melhor no bloco conceitual do que no nucleo A+B.\n"
    )
    for id_, (nova, motivo) in AJUSTES.items():
        estrato_origem = next((e for e, ids in por_estrato.items() if id_ in ids), "?")
        if estrato_origem == "duvida":
            rel.append(f"- **{id_}** ({estrato_origem} -> {nova}): {motivo}")
    rel.append("")
    rel.append(
        "O unico registro de `duvida` mantido sem ajuste apos leitura foi **REG_09209** "
        "(preocupacoes de gestores de instalacoes de governos locais noruegueses -- Bloco A "
        "presente/genuino, Bloco B genuinamente ausente no texto lido: preocupacao e fiscal/"
        "orcamentaria e sobre condicao fisica dos edificios publicos, nao ambiental).\n"
    )

    rel.append("### 3.4 Amostra `sem_resumo` (20 registros, 0 ajustados)\n")
    rel.append(
        "Nenhum registro sem resumo foi reclassificado nesta etapa -- regra do roteiro-mestre "
        "(secao 13): nao incluir/excluir por titulo isolado, exigindo tentativa de enriquecimento "
        "(DOI/Crossref/Scopus/WoS) antes de decidir, o que esta fora do escopo desta etapa. A "
        "leitura dos titulos confirma que o sinal do titulo calculado na ETAPA_07 e coerente: "
        "titulos claramente prediais com sustentabilidade explicita no proprio titulo (\"Buildings "
        "Sustainability Certifications and the Common European Framework Level(s)\", "
        "\"Prioritization of Sustainability Dimensions and Indicators for Office Buildings\", "
        "\"Building Envelopes: A Passive Way to Achieve Energy Sustainability through "
        "Energy-Efficient Buildings\") tem sinal positivo forte; titulos claramente fora de escopo "
        "(\"An efficient implementation of the Gale and Shapley 'propose-and-reject' algorithm\", "
        "\"Enhancing Safety and Security in Renewable Energy Systems within Smart Cities\") tem "
        "sem_sinal. Nota: com 566 registros sem resumo nesta rodada (contra 7.623 antes), este "
        "estrato ficou proporcionalmente muito menor e mais dificil de enriquecer -- a maior parte "
        "e Crossref-only (ver 00_CONTROLE/ESTADO_ATUAL.md).\n"
    )

    rel.append("## 4. Controle de vies -- Bloco C (MCDM/AHP/TOPSIS) e Bloco D (campus/universidade/public building)\n")
    rel.append(
        "Verificacao pedida explicitamente pelo prompt da etapa: presenca de termos de decisao "
        "(Bloco C) ou de contexto publico/universitario (Bloco D) nao deve, sozinha, determinar a "
        "classe. Cruzamento completo recalculado nesta rodada sobre todo o corpus "
        f"({sum(bloco_c_por_classe.values())} registros com Bloco C, {sum(bloco_d_por_classe.values())} "
        f"com Bloco D, de 9.542 no total) a partir de `04_TRIAGEM/matriz_pre_triagem.csv`: dos "
        "registros com Bloco C presente, a distribuicao por classe e "
        f"{', '.join(f'{k}={v}' for k, v in sorted(bloco_c_por_classe.items(), key=lambda kv: -kv[1]))} "
        "-- ou seja, Bloco C aparece em TODAS as classes, nao concentrado em `relevante`. O mesmo "
        "vale para Bloco D: "
        f"{', '.join(f'{k}={v}' for k, v in sorted(bloco_d_por_classe.items(), key=lambda kv: -kv[1]))}. "
        "Isso confirma, por evidencia quantitativa e nao so por design do codigo, que nenhum dos "
        "dois blocos operou como criterio automatico de inclusao -- consistente com a regra "
        "explicita do prompt desta etapa e com o resultado da rodada anterior.\n"
    )

    rel.append("## 5. Recomendacoes para um proximo refinamento do classificador\n")
    rel.append(
        "Das recomendacoes registradas na rodada de 2026-07-08, 5 dos 6 termos ja foram aplicados "
        "ao `pre_triagem.py` antes desta rodada rodar (ver "
        "`00_CONTROLE/DECISOES_METODOLOGICAS.md`, entrada de 2026-07-09): 'retrofit', 'building "
        "stock management', 'building modernization', 'built asset management', 'public asset "
        "management' no Bloco A; 'climate neutral', 'carbon neutral', 'net zero', 'net-zero "
        "energy', 'greenhouse gas' no Bloco B. **Nao aplicado**: 'ecological' (mantido fora por "
        "cautela explicita ja registrada -- termo generico demais, taxa de falso positivo nao "
        "avaliada).\n\n"
        "Novas lacunas de vocabulario/rigidez de frase encontradas nesta rodada, registradas aqui "
        "para decisao do usuario, nao executadas (aplicar isso exigiria reclassificar os 9.442 "
        "registros nao amostrados, fora do escopo de uma auditoria por amostra):\n\n"
        "- Normalizar singular/plural antes do casamento de frases (ou adicionar as duas formas "
        "explicitamente): 'facility maintenance' vs. 'facilities maintenance'; 'building "
        "maintenance' vs. 'buildings maintenance'. Encontrados 2 casos nesta rodada (REG_08115, "
        "REG_00669) onde esse foi o unico motivo do falso negativo.\n"
        "- Frases interrompidas por outra palavra nao sao capturadas por casamento de substring "
        "exato (ex.: 'Maintenance and Rehabilitation Prioritization' nao bate com 'maintenance "
        "prioritization'). Resolver isso exigiria correspondencia mais flexível (proximidade de "
        "termos, nao substring exato) -- mudanca de abordagem, nao so de lista de termos.\n"
        "- Considerar adicionar 'public assets' (alem de 'public asset management' ja adicionado) "
        "ao Bloco A fraco, com token de contexto -- encontrado em REG_08613.\n"
        "- A confirmacao mais forte desta rodada: a subdivisao de `duvida` em 'apenas Bloco A' "
        "(boa taxa de acerto -- 1 de 1 nesta amostra, 7 de 7 na rodada anterior) e 'apenas Bloco B' "
        "(taxa de acerto muito baixa -- 1 de 17 nesta amostra, 0 de 13 na rodada anterior) "
        "continua valida e agora tem evidencia de duas rodadas independentes. Recomenda-se "
        "fortemente dividir `duvida` nessas duas subclasses num proximo refinamento, ja que 'apenas "
        "Bloco B' se comporta na pratica como quase-irrelevante.\n"
    )

    with open(TRIAGEM_PATH, encoding="utf-8-sig", newline="") as f:
        total_corpus = sum(1 for _ in csv.DictReader(f))

    rel.append("## 6. Limites desta etapa\n")
    rel.append(
        f"Apenas 100 dos {total_corpus} registros (1,0%) "
        "foram lidos e verificados individualmente. Os outros 9.442 (99,0%) mantem a classe da "
        "ETAPA_07 sem verificacao humana/assistida nesta auditoria -- `matriz_triagem_auditada.csv` "
        "marca isso explicitamente na coluna `auditado` (sim/nao). Dado que a taxa de ajuste na "
        f"amostra foi de {100*total_ajustes/total_amostra:.0f}% (bem mais alta que os 23% da rodada "
        "anterior, concentrada no estrato `duvida`), e razoavel supor uma fracao de erro "
        "semelhante ou maior no restante do corpus classificado como `duvida` -- reforca a "
        "recomendacao da secao 5 de tratar 'apenas Bloco B' como quase-irrelevante por padrao. Isso "
        "e uma limitacao explicita, nao resolvida aqui -- fica registrada para a definicao do "
        "nucleo analitico (proxima etapa do roteiro) considerar. Esta etapa nao decide "
        "inclusao/exclusao final do artigo nem escreve texto do artigo.\n"
    )

    rel.append("## 7. Arquivos gerados\n")
    rel.append("- `04_TRIAGEM/matriz_triagem_auditada.csv` -- 9.542 linhas, com `classe_auditada`, `auditado` e `justificativa_auditoria`.")
    rel.append("- `04_TRIAGEM/relatorio_ajustes_triagem.md` -- este relatorio.")

    with open(RELATORIO_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(rel) + "\n")

    print(f"Registros auditados: {n_auditados}")
    print(f"Ajustados: {n_ajustados} ({100*n_ajustados/n_auditados:.0f}%)")


if __name__ == "__main__":
    main()
