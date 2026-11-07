"""Analyse du bloc B : tableaux par modèle et tests des hypothèses HB1 à HB7 avec leurs règles préinscrites. N'écrit pas le journal (le verdict est inscrit après lecture, par v3_verdicts_B.py)."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("B_classification"):
    c = rec["cfg"]
    for m, v in rec["result"].items():
        if m in ("_info", "hier_repli"): continue
        rows.append({"repeat": c["repeat"], "fold": c["fold"], "model": m, **{k: v[k] for k in ("f1A", "f1_30", "acc", "f1_fam", "tree_dist", "reject")}})
df = pd.DataFrame(rows); df.to_csv(out / "B_all_units.csv", index=False); n = df[["repeat", "fold"]].drop_duplicates().shape[0]; print("plis :", n)
tab = df.groupby("model")[["f1A", "f1_30", "f1_fam", "tree_dist", "reject"]].mean().round(4).sort_values("f1A", ascending=False); tab["écart-type f1A"] = df.groupby("model").f1A.std().round(4); tab.to_csv(out / "B_resume.csv"); print("\nmoyennes sur les plis (P2)\n", tab.to_string())
M = lambda col: df.pivot_table(index=["repeat", "fold"], columns="model", values=col)
def pair(col, a, b, higher=True):
    X = M(col); d = (X[a] - X[b]) if higher else (X[b] - X[a]); w, p, r = S.wilcoxon_paired(X[a], X[b]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(4000)]
    return {"a": a, "b": b, "mesure": col, "moyenne a-b": float((X[a] - X[b]).mean()), "IC95": f"[{np.percentile(bs, 2.5):.3f} ; {np.percentile(bs, 97.5):.3f}]", "p": p, "r": r}
fam = {"HB1-3": [pair("f1A", "hier_lr", "lr_word"), pair("f1_fam", "hier_lr", "lr_word"), pair("tree_dist", "hier_lr", "lr_word")], "HB4-5": [pair("f1A", "kmeans_pc10", "centroid"), pair("f1A", "tmpl_proto", "centroid"), pair("f1A", "svm_word", "tmpl_proto")],
       "HB6": [pair("f1A", "svm_word", m) for m in ("kmeans_g60", "kmeans_g150", "birch_g150", "dbscan_sub", "hdbscan_sub")]}
allp = []
for k, L in fam.items():
    ps = S.holm([x["p"] for x in L])
    for x, ph in zip(L, ps): x["p Holm"] = ph; x["famille"] = k; allp.append(x)
G = pd.DataFrame(allp); G.round(5).to_csv(out / "B_tests_pairs.csv", index=False); print("\ntests appariés (Wilcoxon, Holm dans chaque famille d'hypothèses)\n", G.drop(columns="r").round(5).to_string(index=False))
f = S.friedman_nemenyi(M("f1A").dropna(axis=1).values, list(M("f1A").dropna(axis=1).columns)); pd.DataFrame(f["nemenyi_p"], index=f["names"], columns=f["names"]).round(4).to_csv(out / "B_nemenyi_tous.csv")
rk = pd.Series(f["avg_ranks"], index=f["names"]).sort_values(); print("\nFriedman, tous les modèles : chi2 = %.1f, p = %.2g, différence critique = %.2f rangs\nrangs moyens :\n%s" % (f["chi2"], f["p"], f["cd"], rk.round(2).to_string()))
best_knn = "knn15" if tab.loc["knn15", "f1A"] >= tab.loc["knn5", "f1A"] else "knn5"; S7 = [best_knn, "kmeans_pc3", "kmeans_pc10", "gmm_pc3", "ward_pc5", "tmpl_proto"]; f7 = S.friedman_nemenyi(M("f1A")[S7].values, S7)
print("\nHB7 (kNN contre clustering par classe et gabarits-prototypes) : Friedman p = %.2g, différence critique = %.2f" % (f7["p"], f7["cd"]))
for nme, r in zip(f7["names"], f7["avg_ranks"]): print(f"  {nme:12s} rang moyen {r:.2f}  écart au kNN {abs(r - f7['avg_ranks'][0]):.2f}  indiscernable du kNN : {abs(r - f7['avg_ranks'][0]) < f7['cd']}")
rep = [rec["result"]["hier_repli"] for rec in R.load_block("B_classification")]; rp = pd.DataFrame(rep).mean().round(4); rp.to_csv(out / "B_repli.csv"); print("\nrepli sur la famille (seuil 0,5), moyenne des plis :\n", rp.to_string())
