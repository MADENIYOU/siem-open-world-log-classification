"""Analyse de l'itération I4 : HI1 à HI4 (règles préinscrites, D19). Unité = (rotation, répétition), moyenne sur les 5 plis. N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []; skipped = 0
for rec in R.load_block("P2_I4_rejet_famille"):
    c = rec["cfg"]
    if "skipped" in rec["result"]: skipped += 1; continue
    for n, v in rec["result"]["scores"].items(): rows.append({"rot": c["rotation_v2"], "repeat": c["repeat"], "fold": c["fold"], "score": n, **v})
df = pd.DataFrame(rows); df.to_csv(out / "I4_all_units.csv", index=False); print("unités calculées :", df[["rot", "repeat", "fold"]].drop_duplicates().shape[0], "; plis écartés :", skipped)
U = df.groupby(["rot", "repeat", "score"])[["auroc", "fpr95", "aupr_in"]].mean().reset_index(); print("unités (rotation, répétition) :", U[["rot", "repeat"]].drop_duplicates().shape[0])
print(U.groupby("score")[["auroc", "fpr95", "aupr_in"]].mean().round(4).sort_values("auroc", ascending=False).to_string()); U.groupby("score")[["auroc", "fpr95", "aupr_in"]].mean().round(4).to_csv(out / "I4_resume.csv")
A = U.pivot_table(index=["rot", "repeat"], columns="score", values="auroc"); Fp = U.pivot_table(index=["rot", "repeat"], columns="score", values="fpr95")
def pair(X, a, b, sgn=1):
    d = sgn * (X[a] - X[b]); w, p, r = S.wilcoxon_paired(X[a], X[b]); rng = np.random.default_rng(0); bs = [d.values[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]
    return {"a": a, "b": b, "gain signé": round(float(d.mean()), 4), "IC95": f"[{np.percentile(bs, 2.5):.4f} ; {np.percentile(bs, 97.5):.4f}]", "p bilatéral": p, "p unilatéral": p / 2 if d.mean() > 0 else 1 - p / 2, "unités en faveur": int((d > 0).sum()), "n": len(d)}
L = [pair(A, "fam_msp", b) for b in ("msp", "energy", "hier_msp")]; ph = S.holm([x["p unilatéral"] for x in L])
for x, q in zip(L, ph): x["p Holm"] = q
G = pd.DataFrame(L); print("\nHI1 (AUROC)\n", G.round(5).to_string(index=False)); G.to_csv(out / "I4_HI1.csv", index=False)
byrot = A.groupby("rot")[["fam_msp", "msp", "energy", "hier_msp"]].mean().round(4); byrot["fam > msp"] = byrot.fam_msp > byrot.msp; print("\nHI2 (par rotation)\n", byrot.to_string(), "\nrotations favorables :", int(byrot["fam > msp"].sum()), "/ 5"); byrot.to_csv(out / "I4_HI2.csv")
G3 = pd.DataFrame([pair(Fp, "msp", "fam_msp")]); print("\nHI3 (FPR@95, gain = baisse de fam_msp par rapport au msp)\n", G3.round(5).to_string(index=False)); G3.to_csv(out / "I4_HI3.csv", index=False)
x = A["fam_msp"]; rng = np.random.default_rng(0); bs = [x.values[rng.integers(0, len(x), len(x))].mean() for _ in range(10000)]; print("\nHI4 : AUROC fam_msp %.4f, IC95 [%.4f ; %.4f] (seuil 0,80)" % (x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5)))
