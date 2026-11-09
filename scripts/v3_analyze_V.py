"""Analyse du bloc V (vectorisation × bruit) : tableaux et tests de HV1 à HV5 avec leurs règles préinscrites. N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from scipy import stats
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows, skipped = [], 0
for rec in R.load_block("V_vectorisation_bruit"):
    if rec["code_version"] != "V1": continue
    c, res = rec["cfg"], rec["result"]
    if "skipped" in res: skipped += 1; continue
    for vec in ("word", "char", "sg_idf"):
        v = res[vec]; rows.append({"p": c["file"], "rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "vec": vec, "f1A": v["f1A"], "f1_30": v["f1_30"], "acc": v["acc"], **{f"auroc_{n}": x["auroc"] for n, x in v["open"].items()}, **{f"fpr95_{n}": x["fpr95"] for n, x in v["open"].items()}})
df = pd.DataFrame(rows); df.to_csv(out / "V_all_units.csv", index=False); blocks = df[["rot", "repeat", "fold"]].drop_duplicates(); print(f"blocs rotation × répétition × pli : {len(blocks)} ; unités sautées : {skipped} ; lignes : {len(df)}")
P = [0, 1, 2, 3, 4, 5];   # indices des fichiers : p = indice / 10
tab = df.groupby(["vec", "p"])[["f1A", "f1_30", "auroc_msp", "auroc_energy", "auroc_fam_msp", "fpr95_msp"]].mean().round(4); tab.to_csv(out / "V_resume.csv"); print("\nmoyennes (macro-F1 classes connues, AUROC MSP / énergie / famille, FPR@95 MSP) par vectorisation et par p\n", tab.round(3).to_string())
key = ["rot", "repeat", "fold"]
def wide(col, vec): return df[df.vec == vec].pivot_table(index=key, columns="p", values=col)
res = []
# HV1 : perte p=0 -> p=0,5, caractères contre mots
lw = (wide("f1A", "word")[0] - wide("f1A", "word")[5]); lc = (wide("f1A", "char")[0] - wide("f1A", "char")[5]); ls = (wide("f1A", "sg_idf")[0] - wide("f1A", "sg_idf")[5])
w, p, r = S.wilcoxon_paired(lc.values, lw.values); print(f"\nHV1 : perte de macro-F1 de p=0 à p=0,5 : mots {lw.mean():.4f} ; caractères {lc.mean():.4f} ; Skip-gram {ls.mean():.4f} ; caractères moins mots = {(lc - lw).mean():.4f} ; Wilcoxon p = {p:.4g} (n = {len(lw)})")
res.append({"hyp": "HV1", "mots": lw.mean(), "caractères": lc.mean(), "skipgram": ls.mean(), "écart car-mots": (lc - lw).mean(), "p": p})
# HV2 : tendance décroissante : rho de Spearman par bloc puis Wilcoxon à un échantillon
hv2 = []
for vec in ("word", "char", "sg_idf"):
    W = wide("f1A", vec); rhos = np.array([stats.spearmanr(P, W.loc[i].values)[0] for i in W.index]); rhos = rhos[~np.isnan(rhos)]; pw = stats.wilcoxon(rhos, alternative="less").pvalue
    hv2.append({"vec": vec, "rho médian": float(np.median(rhos)), "blocs avec rho<0": int((rhos < 0).sum()), "n": len(rhos), "p": pw})
g2 = pd.DataFrame(hv2); g2["p Holm"] = S.holm(g2.p.values); print("\nHV2 : tendance du macro-F1 avec p (Spearman par bloc puis Wilcoxon unilatéral, Holm sur 3)\n", g2.round(5).to_string(index=False))
# HV3 : Skip-gram contre mots à chaque p
hv3 = []
for pp in P:
    a, b = wide("f1A", "sg_idf")[pp], wide("f1A", "word")[pp]; w, p, r = S.wilcoxon_paired(a.values, b.values); hv3.append({"fichier": pp, "sg - mots": float((a - b).mean()), "mots": float(b.mean()), "skipgram": float(a.mean()), "p": p, "Sg inférieur": bool((a - b).mean() < 0)})
g3 = pd.DataFrame(hv3); g3["p Holm"] = S.holm(g3.p.values); print("\nHV3 : Skip-gram contre mots, à chaque niveau de bruit (Holm sur 6)\n", g3.round(5).to_string(index=False))
# HV4 : rangs de Friedman à p=0 et p=0,5
hv4 = {}
for pp in (0, 5):
    X = np.column_stack([wide("f1A", v)[pp].values for v in ("word", "char", "sg_idf")]); f = S.friedman_nemenyi(X, ["word", "char", "sg_idf"]); hv4[pp] = f
    print(f"\nHV4 : p = {pp / 10} : rangs moyens {dict(zip(f['names'], np.round(f['avg_ranks'], 2)))} ; Friedman p = {f['p']:.3g} ; différence critique {f['cd']:.2f}")
# HV5 : AUROC du MSP (mots) avec p
W = wide("auroc_msp", "word"); rhos = np.array([stats.spearmanr(P, W.loc[i].values)[0] for i in W.index]); rhos = rhos[~np.isnan(rhos)]; p5 = stats.wilcoxon(rhos, alternative="less").pvalue
print(f"\nHV5 : AUROC du MSP (mots) selon p : rho médian {np.median(rhos):.3f} ; blocs avec rho<0 : {(rhos < 0).sum()}/{len(rhos)} ; Wilcoxon unilatéral p = {p5:.4g}")
# complément exploratoire : monde connu et inconnu côte à côte, et confiance de la famille selon le bruit
ex = df.groupby(["vec", "p"])[["auroc_msp", "auroc_fam_msp"]].mean().unstack(0).round(3); print("\nAUROC MSP et famille par p (exploratoire)\n", ex.to_string())
g2.round(5).to_csv(out / "V_HV2.csv", index=False); g3.round(5).to_csv(out / "V_HV3.csv", index=False)
