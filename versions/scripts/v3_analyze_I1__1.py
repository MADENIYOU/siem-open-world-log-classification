"""Analyse de l'itération I1 (phase 2) : tests des hypothèses HF1 à HF6 avec leurs règles préinscrites. N'écrit pas le journal (verdicts : v3_verdicts_I1.py)."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_I1_representation"):
    c = rec["cfg"]
    for m, v in rec["result"].items():
        if m == "_info": continue
        rows.append({"repeat": c["repeat"], "fold": c["fold"], "model": m, **{k: v[k] for k in ("f1A", "f1_30", "f1_fam", "tree_dist", "acc")}})
df = pd.DataFrame(rows); df.to_csv(out / "I1_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
tab = df.groupby("model")[["f1A", "f1_30", "f1_fam", "tree_dist", "acc"]].mean().round(4).sort_values("f1A", ascending=False); tab["écart-type f1A"] = df.groupby("model").f1A.std().round(4); tab.to_csv(out / "I1_resume.csv"); print(tab.to_string())
X = df.pivot_table(index=["repeat", "fold"], columns="model", values="f1A")
def pair(a, b, seuil):
    d = X[a] - X[b]; w, p, r = S.wilcoxon_paired(X[a], X[b]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(4000)]
    return {"a": a, "b": b, "écart moyen": float(d.mean()), "IC95": f"[{np.percentile(bs, 2.5):.3f} ; {np.percentile(bs, 97.5):.3f}]", "seuil préinscrit": seuil, "p": p, "plis a>b": int((d > 0).sum())}
fam = {"HF1": [pair(m, "V0", 0.02) for m in ("T2", "T3", "T5")], "HF2": [pair("T3M", "T3", 0.01)], "HF3": [pair("ENS", "V0", 0.02)], "HF4": [pair("WGT", "V0", 0.02)],
       "HF5": [pair("C1", "T3", 0), pair("C1", "WGT", 0), pair("C2", "T3", 0), pair("C2", "ENS", 0), pair("C3", "T3", 0), pair("C3", "ENS", 0), pair("C3", "WGT", 0)], "contexte": [pair(m, "V0", 0) for m in ("C1", "C2", "C3")]}
allp = []
for k, L in fam.items():
    ps = S.holm([x["p"] for x in L])
    for x, ph in zip(L, ps): x["p Holm"] = ph; x["famille"] = k; allp.append(x)
G = pd.DataFrame(allp); G.round(5).to_csv(out / "I1_tests_pairs.csv", index=False); print(G.round(5).to_string(index=False))
print("\nHF6 : meilleure variante", tab.index[0], "f1A =", tab.f1A.iloc[0], "(cible 0,55 ; baseline V0 =", tab.loc["V0", "f1A"], ")")
