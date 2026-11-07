"""Analyse du bloc C : tableaux et tests des hypothèses HC1 à HC9 avec leurs règles préinscrites. N'écrit pas le journal (verdicts inscrits après lecture)."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from scipy import stats
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; TAX = json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["taxonomy"]; ROT = json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["rotations"]
fam_of = {c: f for f, cs in TAX.items() for c in cs}; rows, byc, skipped = [], [], 0
for rec in R.load_block("C_inconnus"):
    if rec["code_version"] != "C1": continue
    c, res = rec["cfg"], rec["result"]
    if "skipped" in res: skipped += 1; continue
    for n, v in res["scores"].items(): rows.append({"rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "score": n, **v})
    for n, d in res["by_class"].items():
        for cl, (a, m) in d.items(): byc.append({"rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "score": n, "cls": cl, "auroc": a, "n": m})
df = pd.DataFrame(rows); df.to_csv(out / "C_all_units.csv", index=False); nb = df[["rot", "repeat", "fold"]].drop_duplicates().shape[0]; print(f"unités utilisables : {nb} ; sautées (pli sans assez de logs) : {skipped}")
M = lambda col: df.pivot_table(index=["rot", "repeat", "fold"], columns="score", values=col)
res = df.groupby("score").agg(auroc=("auroc", "mean"), sd=("auroc", "std"), fpr95=("fpr95", "mean"), aupr=("aupr_in", "mean")).round(4).sort_values("auroc", ascending=False); res.to_csv(out / "C_resume.csv"); print("\nmoyennes sur les unités (AUROC, écart-type, FPR@95, AUPR)\n", res.to_string())
def pair(a, b, col="auroc"):
    X = M(col); d = (X[a] - X[b]).dropna(); w, p, r = S.wilcoxon_paired(X.loc[d.index, a], X.loc[d.index, b]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(3000)]
    return {"a": a, "b": b, "moyenne a-b": float(d.mean()), "IC95": f"[{np.percentile(bs, 2.5):.3f} ; {np.percentile(bs, 97.5):.3f}]", "p": p, "n": len(d)}
fam = {"HC2": [pair(s, "msp") for s in ("maha_shared", "maha_class", "maha_rel", "knn1", "knn10", "pca_resid", "gmm_lik", "lof", "iforest")], "HC3": [pair(s, "energy_z") for s in ("ash_s", "scale", "dice", "nnguide", "she", "vim")], "HC4": [pair("tmpl_radius", "msp")], "HC5": [pair("tmpl_radius", "tmpl_dist")]}
comp = res.loc[["msp", "maha_shared", "knn10"], "auroc"].idxmax(); fam["HC6"] = [pair("rank_mean3", comp)]; allp = []
for k, L in fam.items():
    ps = S.holm([x["p"] for x in L])
    for x, ph in zip(L, ps): x["p Holm"] = ph; x["famille"] = k; allp.append(x)
G = pd.DataFrame(allp); G.round(5).to_csv(out / "C_tests_pairs.csv", index=False); print("\ntests appariés (Wilcoxon, Holm dans chaque famille ; HC6 : meilleur composant =", comp, ")\n", G.round(5).to_string(index=False))
X = M("auroc").dropna(); f = S.friedman_nemenyi(X.values, list(X.columns)); pd.DataFrame(f["nemenyi_p"], index=f["names"], columns=f["names"]).round(4).to_csv(out / "C_nemenyi.csv")
rk = pd.Series(f["avg_ranks"], index=f["names"]).sort_values(); print("\nFriedman (%d unités sans valeur manquante) : chi2 = %.1f, p = %.2g, différence critique = %.2f rangs\n%s" % (len(X), f["chi2"], f["p"], f["cd"], rk.round(2).to_string()))
pr = df[df.score == "msp"].groupby("rot").auroc.mean(); pr.to_csv(out / "C_msp_par_rotation.csv"); print("\nHC8 : AUROC du MSP par rotation :", pr.round(3).to_dict(), "; écart-type entre rotations = %.3f" % pr.std())
b = pd.DataFrame(byc); b["famille"] = b.cls.map(fam_of); b["soeur_connue"] = b.apply(lambda r: any((fam_of[c] == r.famille) and (c not in ROT[r.rot]) for c in fam_of), axis=1)
bc = b[b.score == "msp"].groupby(["rot", "cls", "soeur_connue"]).auroc.mean().reset_index(); bc.to_csv(out / "C_msp_par_classe.csv", index=False)
g1, g0 = bc[bc.soeur_connue].auroc.values, bc[~bc.soeur_connue].auroc.values; u = stats.mannwhitneyu(g1, g0, alternative="two-sided")
print("\nHC7 : AUROC du MSP par couple classe x rotation : avec sœur connue %.3f (n=%d), sans sœur connue %.3f (n=%d), écart %.3f, Mann-Whitney p = %.3g" % (g1.mean(), len(g1), g0.mean(), len(g0), g1.mean() - g0.mean(), u.pvalue))
print("\nHC9 : FPR@95 moyen minimal parmi les scores : %s = %.3f ; maximal : %s = %.3f" % (res.fpr95.idxmin(), res.fpr95.min(), res.fpr95.idxmax(), res.fpr95.max()))
print("HC1 : AUROC moyen maximal : %s = %.3f" % (res.auroc.idxmax(), res.auroc.max()))
