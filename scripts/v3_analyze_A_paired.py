"""Analyse de HA1b (montage apparié) et réanalyse non appariée de P0 contre P2 (volet (a) de la remise en cause de HA1)."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from scipy import stats
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("A_decoupage_apparie"):
    c = rec["cfg"]
    for m in rec["result"]["G"]: rows.append({"repeat": c["repeat"], "fold": c["fold"], "model": m, "G": rec["result"]["G"][m]["f1A"], "H": rec["result"]["H"][m]["f1A"]})
df = pd.DataFrame(rows); df.to_csv(out / "A_apparie_all_units.csv", index=False); print("unités :", df[["repeat", "fold"]].drop_duplicates().shape[0]); res = []
for m, d in df.groupby("model"):
    diff = (d.H - d.G).values; w, p, r = S.wilcoxon_paired(d.H, d.G); rng = np.random.default_rng(0); bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(4000)]
    res.append({"model": m, "G (sans fuite)": d.G.mean(), "H (avec fuite)": d.H.mean(), "écart H-G": diff.mean(), "IC95": f"[{np.percentile(bs, 2.5):.3f} ; {np.percentile(bs, 97.5):.3f}]", "min écart sur les plis": diff.min(), "Wilcoxon p": p, "Cliff delta": S.cliffs_delta(d.H, d.G), "n plis": len(d)})
g = pd.DataFrame(res); g["p Holm"] = S.holm(g["Wilcoxon p"].values); g.round(4).to_csv(out / "A_apparie_HA1b.csv", index=False)
print("\nHA1b : effet pur de la fuite sur les mêmes logs de test (macro-F1 palier A)\n", g.round(4).to_string(index=False))
print("\nverdict HA1b (règle : les six écarts >= 0,20 ET p Holm < 0,05) :", "CONFIRMÉE" if (g["écart H-G"] >= 0.20).all() and (g["p Holm"] < 0.05).all() else "NON CONFIRMÉE")
# (a) réanalyse non appariée de P0 contre P2 (mêmes données que la version 2 de HA1)
A = pd.read_csv(out / "A_all_units.csv"); ra = []
for m, d in A.groupby("model"):
    p0, p2 = d[d.protocol == "P0"].f1A.values, d[d.protocol == "P2"].f1A.values; u = stats.mannwhitneyu(p0, p2, alternative="two-sided"); ra.append({"model": m, "P0": p0.mean(), "P2": p2.mean(), "écart": p0.mean() - p2.mean(), "Mann-Whitney p": u.pvalue, "Cliff delta": S.cliffs_delta(p0, p2), "plus petit P0 > plus grand P2": bool(p0.min() > p2.max())})
ga = pd.DataFrame(ra); ga["p Holm"] = S.holm(ga["Mann-Whitney p"].values); ga.round(4).to_csv(out / "A_HA1_reanalyse_non_appariee.csv", index=False)
print("\n(a) réanalyse NON appariée de P0 contre P2 (mêmes données)\n", ga.round(4).to_string(index=False))
