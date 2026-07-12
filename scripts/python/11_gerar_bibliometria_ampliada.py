from pathlib import Path
from collections import Counter
import math
import re
import unicodedata

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans
from sklearn.manifold import MDS


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "bibliometria_372"
FIG = ROOT / "latex-artigo" / "figuras"
TAB = ROOT / "latex-artigo" / "fontes"
for p in (FIG, TAB):
    p.mkdir(parents=True, exist_ok=True)


STOP = {
    "building", "buildings", "maintenance", "management", "sustainable", "sustainability",
    "study", "analysis", "system", "systems", "model", "models", "approach", "framework",
    "performance", "decision", "support", "construction", "facility", "facilities", "method",
    "methods", "assessment", "evaluation", "based", "using", "environment", "built environment",
}

SYNONYMS = {
    "bim": "building information modeling (bim)",
    "building information modeling": "building information modeling (bim)",
    "building information modelling": "building information modeling (bim)",
    "building information modeling bim": "building information modeling (bim)",
    "building information modelling bim": "building information modeling (bim)",
    "facilities management": "facility management",
    "green buildings": "green building",
    "office buildings": "office building",
    "residential buildings": "residential building",
    "smart buildings": "smart building",
    "life-cycle assessment": "life cycle assessment",
    "lifecycle assessment": "life cycle assessment",
    "life cycle assessment lca": "life cycle assessment",
    "life-cycle cost": "life cycle cost",
    "lifecycle cost": "life cycle cost",
    "digital twins": "digital twin",
    "carbon emission": "carbon emissions",
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9+\- ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def split_keywords(s):
    if pd.isna(s):
        return []
    vals = []
    for x in re.split(r"[;|]", str(s)):
        x = norm(x)
        x = SYNONYMS.get(x, x)
        if len(x) >= 3 and x not in STOP and not x.isdigit():
            vals.append(x)
    return sorted(set(vals))


def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(path.with_suffix(".pdf"), bbox_inches="tight", facecolor="white")
    plt.close()


d = pd.read_csv(ROOT / "07_SINTESE_TEMATICA" / "matriz_extracao_final_reavaliada_resumos.csv", low_memory=False)
d = d[d["estrato_uso_resumo"].eq("A_nucleo_forte")].copy()
d["ano"] = pd.to_numeric(d["ano"], errors="coerce").astype("Int64")
d["kw"] = d["palavras_chave"].apply(split_keywords)

availability = []
for col in ["titulo", "ano", "autores", "fonte_periodico", "palavras_chave", "resumo", "doi"]:
    present = d[col].notna() & d[col].astype(str).str.strip().ne("")
    availability.append({"campo": col, "n": int(present.sum()), "percentual": round(100*present.mean(), 1)})
availability += [
    {"campo": "afiliacoes", "n": 0, "percentual": 0.0},
    {"campo": "referencias_citadas", "n": 0, "percentual": 0.0},
]
pd.DataFrame(availability).to_csv(TAB / "disponibilidade_campos_372.csv", index=False)

# ---------- Fontes ----------
sources = (d.assign(fonte=d["fonte_periodico"].fillna("").str.strip())
             .query("fonte != ''").groupby("fonte").size().sort_values(ascending=False)
             .rename("registros").reset_index())
sources["percentual_372"] = (100*sources["registros"]/len(d)).round(1)
cum_articles = sources["registros"].cumsum()
total = sources["registros"].sum()
sources["zona_bradford_aproximada"] = pd.cut(cum_articles, bins=[0, total/3, 2*total/3, total+1], labels=["Nucleo", "Zona 2", "Zona 3"], include_lowest=True)
sources.to_csv(TAB / "fontes_relevantes_372.csv", index=False)

top = sources.head(15).sort_values("registros")
plt.figure(figsize=(10, 6.5))
plt.barh(top["fonte"], top["registros"], color="#2563a6")
plt.xlabel("Registros no corpus bibliométrico (n=372)")
plt.ylabel("")
plt.title("Fontes mais frequentes no corpus bibliométrico")
for i, v in enumerate(top["registros"]):
    plt.text(v + .12, i, str(v), va="center", fontsize=8)
savefig(FIG / "figura_fontes_relevantes_372.png")

# ---------- Matriz de coocorrencia ----------
freq = Counter(k for ks in d["kw"] for k in ks)
terms = [k for k, n in freq.most_common(40) if n >= 3]
idx = {k:i for i,k in enumerate(terms)}
co = np.zeros((len(terms), len(terms)), dtype=float)
for ks in d["kw"]:
    active = [idx[k] for k in ks if k in idx]
    for i in active:
        co[i, i] += 1
    for x in range(len(active)):
        for y in range(x+1, len(active)):
            i, j = active[x], active[y]
            co[i, j] += 1
            co[j, i] += 1

diag = np.diag(co).copy()
assoc = np.zeros_like(co)
for i in range(len(terms)):
    for j in range(len(terms)):
        if i != j and diag[i] and diag[j]:
            assoc[i,j] = co[i,j] / math.sqrt(diag[i]*diag[j])

rows=[]
for i in range(len(terms)):
    for j in range(i+1,len(terms)):
        if co[i,j] >= 2:
            rows.append({"termo_1":terms[i],"termo_2":terms[j],"coocorrencia":int(co[i,j]),"associacao_normalizada":round(assoc[i,j],4)})
pd.DataFrame(rows).sort_values(["associacao_normalizada","coocorrencia"],ascending=False).to_csv(TAB/"rede_coocorrencia_palavras_chave_372.csv",index=False)

# Rede: top 30, arestas mais informativas por associacao
nnet=min(30,len(terms))
A=assoc[:nnet,:nnet].copy()
threshold=np.quantile(A[A>0],.62) if np.any(A>0) else 1
dist=1-np.clip(A,0,1)
np.fill_diagonal(dist,0)
pos=MDS(n_components=2,dissimilarity="precomputed",random_state=42,n_init=4,max_iter=500).fit_transform(dist)
clusters=KMeans(n_clusters=min(5,max(2,nnet//6)),random_state=42,n_init=20).fit_predict(A)
colors=plt.cm.Set2(np.linspace(0,1,clusters.max()+1))
plt.figure(figsize=(12,9))
for i in range(nnet):
    for j in range(i+1,nnet):
        if A[i,j]>=threshold and co[i,j] >= 2:
            plt.plot([pos[i,0],pos[j,0]],[pos[i,1],pos[j,1]],color="#9ca3af",alpha=.25+0.65*A[i,j],lw=.5+3*A[i,j],zorder=1)
sizes=np.array([freq[terms[i]] for i in range(nnet)])
plt.scatter(pos[:,0],pos[:,1],s=45+sizes*18,c=[colors[c] for c in clusters],edgecolor="white",linewidth=.8,zorder=2)
for i,t in enumerate(terms[:nnet]):
    plt.text(pos[i,0],pos[i,1],t,fontsize=7.5,ha="center",va="center",zorder=3)
plt.title("Rede normalizada de coocorrência de palavras-chave")
plt.axis("off")
savefig(FIG/"figura_rede_coocorrencia_372.png")

# ---------- Mapa tematico ----------
# Clusteriza termos e calcula densidade interna e centralidade externa.
k=min(6,max(2,len(terms)//6))
labels=KMeans(n_clusters=k,random_state=42,n_init=30).fit_predict(assoc)
themes=[]
for c in range(k):
    members=np.where(labels==c)[0]
    others=np.where(labels!=c)[0]
    density=float(assoc[np.ix_(members,members)].sum()/(max(1,len(members)*(len(members)-1))))
    central=float(assoc[np.ix_(members,others)].sum()/max(1,len(members)))
    top_terms=sorted(members,key=lambda i:freq[terms[i]],reverse=True)[:2]
    themes.append({"cluster":c+1,"centralidade":central,"densidade":density,"n_termos":len(members),"rotulo":"; ".join(terms[i] for i in top_terms),"frequencia":sum(freq[terms[i]] for i in members)})
themes=pd.DataFrame(themes)
themes.to_csv(TAB/"mapa_tematico_372.csv",index=False)
cx,dy=themes.centralidade.median(),themes.densidade.median()
plt.figure(figsize=(10,7))
plt.axvline(cx,color="#9ca3af",ls="--",lw=1); plt.axhline(dy,color="#9ca3af",ls="--",lw=1)
plt.scatter(themes.centralidade,themes.densidade,s=120+themes.frequencia*4,c=plt.cm.Set2(np.linspace(0,1,len(themes))),alpha=.85,edgecolor="white")
handles=[]
for z,(_,r) in enumerate(themes.iterrows()):
    plt.text(r.centralidade,r.densidade,f"T{z+1}",ha="center",va="center",fontsize=8,fontweight="bold")
    handles.append(Line2D([0],[0],marker="o",color="w",markerfacecolor=plt.cm.Set2(z/max(1,len(themes)-1)),
                          markersize=8,label=f"T{z+1}: {r.rotulo}"))
plt.xlabel("Centralidade no campo")
plt.ylabel("Densidade interna")
plt.title("Mapa temático do corpus bibliométrico")
plt.text(.98,.98,"Temas motores",transform=plt.gca().transAxes,ha="right",va="top",fontsize=9,color="#4b5563")
plt.text(.02,.98,"Temas especializados",transform=plt.gca().transAxes,ha="left",va="top",fontsize=9,color="#4b5563")
plt.text(.98,.02,"Temas básicos",transform=plt.gca().transAxes,ha="right",va="bottom",fontsize=9,color="#4b5563")
plt.text(.02,.02,"Temas emergentes/declinantes",transform=plt.gca().transAxes,ha="left",va="bottom",fontsize=9,color="#4b5563")
plt.legend(handles=handles,loc="upper center",bbox_to_anchor=(.5,-.11),ncol=2,frameon=False,fontsize=7.5)
savefig(FIG/"figura_mapa_tematico_372.png")

# ---------- Evolucao tematica ----------
periods={"2010–2020":d[d.ano<=2020],"2021–2026":d[d.ano>=2021]}
pf={}
for name,sub in periods.items():
    pf[name]=Counter(k for ks in sub.kw for k in ks)
union=Counter()
for ctr in pf.values(): union.update(ctr)
evol_terms=[t for t,n in union.most_common(18)]
evol=pd.DataFrame({"termo":evol_terms})
for name,sub in periods.items():
    evol[name]=[pf[name][t] for t in evol_terms]
    evol[name+" (%)"]=(100*evol[name]/len(sub)).round(1)
evol["delta_pp"]=(evol["2021–2026 (%)"]-evol["2010–2020 (%)"]).round(1)
evol.to_csv(TAB/"evolucao_tematica_dois_periodos_372.csv",index=False)

plot=evol.sort_values("delta_pp")
y=np.arange(len(plot))
plt.figure(figsize=(10,8))
plt.hlines(y,plot["2010–2020 (%)"],plot["2021–2026 (%)"],color="#d1d5db",lw=2)
plt.scatter(plot["2010–2020 (%)"],y,color="#d97706",s=55,label="2010–2020")
plt.scatter(plot["2021–2026 (%)"],y,color="#2563a6",s=55,label="2021–2026")
plt.yticks(y,plot.termo,fontsize=8)
plt.xlabel("Percentual de registros do período")
plt.title("Evolução das palavras-chave entre dois períodos")
plt.legend(frameon=False)
savefig(FIG/"figura_evolucao_tematica_372.png")

# ---------- Relatorio ----------
period_counts={name:len(sub) for name,sub in periods.items()}
report=f"""# Relatório da camada bibliométrica ampliada

## Corpus

- Corpus elegível: 372 registros classificados como `A_nucleo_forte`.
- 2010–2020: {period_counts['2010–2020']} registros.
- 2021–2026: {period_counts['2021–2026']} registros.
- Palavras-chave disponíveis: {sum(bool(x) for x in d.kw)} registros ({100*sum(bool(x) for x in d.kw)/len(d):.1f}%).
- Fontes disponíveis: 372 registros (100%).

## Produtos executados

1. Mapa temático por centralidade e densidade de clusters de palavras-chave.
2. Rede de coocorrência normalizada de palavras-chave.
3. Evolução temática entre 2010–2020 e 2021–2026.
4. Fontes mais frequentes e zona de Bradford aproximada.

## Produtos não executados

- Rede de colaboração: autores disponíveis em apenas {int(d.autores.fillna('').str.strip().ne('').sum())} registros ({100*d.autores.fillna('').str.strip().ne('').mean():.1f}%) e ausência de afiliações. Cobertura insuficiente para representar o campo sem viés elevado.
- Acoplamento bibliográfico: o arquivo consolidado não contém referências citadas. Informação insuficiente para calcular ligações bibliográficas.

## Limites

- A análise usa metadados e palavras-chave preservados no repositório; não envolve nova busca.
- O mapa temático é exploratório e depende da padronização das palavras-chave.
- Centralidade, densidade e associação normalizada não representam qualidade metodológica, causalidade ou força de evidência.
"""
(ROOT/"docs"/"RELATORIO_BIBLIOMETRIA_372.md").write_text(report,encoding="utf-8")
print(f"OK: {len(d)} registros; {len(terms)} termos; {len(sources)} fontes")
