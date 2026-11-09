"""Analyse de la confirmation I1b : HF7 à HF9 (règles préinscrites, D17). N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_I1b_confirmation"):
    c = rec["cfg"]
    for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "model": m, **v})
df = pd.DataFrame(rows); df.to_csv(out / "I1b_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
print(df.groupby("model")[["f1A", "f1_30", "f1_fam", "tree_dist", "acc"]].mean().round(4).to_string())
res = []
for col, sgn, seuil, hyp in (("f1_fam", 1, 0.01, "HF7"), ("tree_dist", -1, 0.01, "HF8"), ("f1A", 1, -0.01, "HF9")):
    X = df.pivot_table(index=["repeat", "fold"], columns="model", values=col); d = sgn * (X["ENS"] - X["V0"]); w, p, r = S.wilcoxon_paired(X["ENS"], X["V0"]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    p1 = p / 2 if d.mean() > 0 else 1 - p / 2
    res.append({"hypothèse": hyp, "mesure": col, "écart (gain signé)": round(float(d.mean()), 4), "IC95": f"[{np.percentile(bs, 2.5):.4f} ; {np.percentile(bs, 97.5):.4f}]", "seuil": seuil, "p bilatéral": p, "p unilatéral": p1, "plis en faveur": int((d > 0).sum())})
G = pd.DataFrame(res); G.to_csv(out / "I1b_tests.csv", index=False); print(G.round(5).to_string(index=False))
