"""Analyse de l'itération I2 (champs typés) : HF10 à HF12 (règles préinscrites, D18). N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_I2_champs_types"):
    c = rec["cfg"]
    for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "model": m, **v})
df = pd.DataFrame(rows); df.to_csv(out / "I2_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
tab = df.groupby("model")[["f1A", "f1_30", "f1_fam", "tree_dist", "acc"]].mean().round(4); tab.to_csv(out / "I2_resume.csv"); print(tab.to_string())
P = lambda col: df.pivot_table(index=["repeat", "fold"], columns="model", values=col)
def pair(col, a, b):
    X = P(col); d = X[a] - X[b]; w, p, r = S.wilcoxon_paired(X[a], X[b]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    return {"mesure": col, "a": a, "b": b, "écart": round(float(d.mean()), 4), "IC95": f"[{np.percentile(bs, 2.5):.4f} ; {np.percentile(bs, 97.5):.4f}]", "p": p, "plis a>b": int((d > 0).sum())}
L = [pair("f1A", "FT", "V0"), pair("f1A", "FTE", "V0")]; ph = S.holm([x["p"] for x in L])
for x, q in zip(L, ph): x["p Holm"] = q
L += [pair("f1_fam", "FTE", "FT"), pair("f1_fam", "FT", "V0"), pair("tree_dist", "FT", "V0"), pair("f1A", "FTo", "V0")]
G = pd.DataFrame(L); G.to_csv(out / "I2_tests.csv", index=False); print(G.round(5).to_string(index=False))
X = P("f1A")["FTo"]; rng = np.random.default_rng(0); bs = [X.values[rng.integers(0, len(X), len(X))].mean() for _ in range(10000)]
print("HF11 : FTo moyenne %.4f, IC95 [%.4f ; %.4f] (seuil 0,30)" % (X.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
