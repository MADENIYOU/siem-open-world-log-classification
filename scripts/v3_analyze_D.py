"""Analyse du bloc D (attaques par degré) : tableaux et tests de HD1 à HD7 avec leurs règles préinscrites. N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from scipy import stats
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("D_attaques"):
    if rec["code_version"] != "D1": continue
    c, res = rec["cfg"], rec["result"]
    if "skipped" in res: continue
    for m in ("word", "char"):
        d = res[m]; rows.append({"rot": c["rotation"], "fold": c["fold"], "model": m, "attack": "clean", "deg": 0, **d["clean"]})
        for atk in ("typos", "homoglyphs", "padding", "homoglyphs_norm"):
            for di, (rate, v) in enumerate(d[atk].items()): rows.append({"rot": c["rotation"], "fold": c["fold"], "model": m, "attack": atk, "deg": di + 1, "rate": float(rate), **v})
df = pd.DataFrame(rows); df.to_csv(out / "D_all_units.csv", index=False); nu = df[["rot", "fold"]].drop_duplicates().shape[0]; print("unités :", nu)
tab = df.groupby(["model", "attack", "deg"])[["f1A", "auroc_msp", "auroc_fam", "rej_known"]].mean().round(4); tab.to_csv(out / "D_resume.csv"); print("\nmoyennes sur les unités\n", tab.round(3).to_string())
key = ["rot", "fold"]
def W(model, attack, col): return df[(df.model == model) & (df.attack == attack)].pivot_table(index=key, columns="deg", values=col)
clean = {(m, c): df[(df.model == m) & (df.attack == "clean")].set_index(key)[c] for m in ("word", "char") for c in ("f1A", "auroc_msp", "auroc_fam", "rej_known")}
def loss(model, attack, col="f1A"): w = W(model, attack, col); return -(w.sub(clean[(model, col)], axis=0)) if col != "rej_known" else w.sub(clean[(model, col)], axis=0)   # perte = propre - attaqué (hausse pour rej_known)
ATK = ["typos", "homoglyphs", "padding"]
# HD1
r = []
for a in ATK:
    L = loss("word", a)[5]; w, p, rr = S.wilcoxon_paired(W("word", a, "f1A")[5].values, clean[("word", "f1A")].loc[W("word", a, "f1A").index].values); r.append({"attaque": a, "perte au degré max": L.mean(), "perte relative %": 100 * L.mean() / clean[("word", "f1A")].mean(), "p": p})
g1 = pd.DataFrame(r); g1["p Holm"] = S.holm(g1.p.values); print("\nHD1 (mots, degré maximal vs sans attaque)\n", g1.round(5).to_string(index=False))
# HD2
r = []
for a in ATK:
    L = loss("word", a); rhos = np.array([stats.spearmanr([1, 2, 3, 4, 5], L.loc[i].values)[0] for i in L.index]); rhos = rhos[~np.isnan(rhos)]; r.append({"attaque": a, "rho médian": float(np.median(rhos)), "unités rho>0": int((rhos > 0).sum()), "n": len(rhos), "p": stats.wilcoxon(rhos, alternative="greater").pvalue, "pertes moyennes par degré": [round(x, 3) for x in L.mean().values]})
g2 = pd.DataFrame(r); g2["p Holm"] = S.holm(g2.p.values); print("\nHD2 (mots, tendance de la perte avec le degré)\n", g2.round(5).to_string(index=False))
# HD3
M = np.column_stack([loss("word", a).mean(1).values for a in ATK]); f = S.friedman_nemenyi(-M, ATK)   # -perte : plus grand = meilleur ; rang 1 = perte la plus faible
print("\nHD3 (mots, perte moyenne sur les cinq degrés par attaque) :", dict(zip(ATK, np.round(M.mean(0), 4))), "; rangs moyens (1 = perte la plus faible) :", dict(zip(f["names"], np.round(f["avg_ranks"], 2))), f"; Friedman p = {f['p']:.3g} ; différence critique {f['cd']:.2f}")
print("   Nemenyi p (homoglyphes contre fautes, contre remplissage) :", round(f["nemenyi_p"][1, 0], 5), round(f["nemenyi_p"][1, 2], 5))
# HD4
r = []
for a in ATK:
    lw, lc = loss("word", a).mean(1), loss("char", a).mean(1); w, p, rr = S.wilcoxon_paired(lc.values, lw.values); r.append({"attaque": a, "perte mots": lw.mean(), "perte caractères": lc.mean(), "car - mots": (lc - lw).mean(), "p": p})
g4 = pd.DataFrame(r); g4["p Holm"] = S.holm(g4.p.values); print("\nHD4 (perte moyenne sur les degrés : caractères contre mots)\n", g4.round(5).to_string(index=False))
# HD5
res5 = (clean[("word", "f1A")].mean() - W("word", "homoglyphs_norm", "f1A").mean()).round(4); res5b = (clean[("word", "f1A")].mean() - W("word", "homoglyphs", "f1A").mean()).round(4)
print("\nHD5 (mots) perte résiduelle avec normalisation officielle, par degré :", res5.values, "; sans normalisation :", res5b.values)
# HD6
L = loss("word", "homoglyphs", "rej_known"); rhos = np.array([stats.spearmanr([1, 2, 3, 4, 5], L.loc[i].values)[0] for i in L.index]); rhos = rhos[~np.isnan(rhos)]; print(f"\nHD6 (mots, MSP) connus rejetés à tort : par degré {np.round(W('word', 'homoglyphs', 'rej_known').mean().values, 3)} ; rho médian {np.median(rhos):.3f} ; unités rho>0 : {(rhos > 0).sum()}/{len(rhos)} ; p = {stats.wilcoxon(rhos, alternative='greater').pvalue:.4g}")
# HD7
r = []
for a in ATK:
    lm, lf = loss("word", a, "auroc_msp")[5], loss("word", a, "auroc_fam")[5]; w, p, rr = S.wilcoxon_paired(lf.values, lm.values); r.append({"attaque": a, "perte AUROC MSP": lm.mean(), "perte AUROC famille": lf.mean(), "famille - MSP": (lf - lm).mean(), "p": p})
g7 = pd.DataFrame(r); g7["p Holm"] = S.holm(g7.p.values); print("\nHD7 (mots, degré maximal : perte d'AUROC, famille contre MSP)\n", g7.round(5).to_string(index=False))
rel = {(m, a): [round(100 * loss(m, a).mean()[d] / clean[(m, "f1A")].mean(), 1) for d in range(1, 6)] for m in ("word", "char") for a in ATK}; print("\nperte relative % de macro-F1 par degré :", rel)
for n, g in (("HD1", g1), ("HD2", g2), ("HD4", g4), ("HD7", g7)): g.round(5).to_csv(out / f"D_{n}.csv", index=False)
