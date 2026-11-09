"""Analyse de la réplication I7c (D25) : HI6b, HI7b sur 75 unités (rotation, répétition) des ensembles D, E, F. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_I7c_rejet"):
    c = rec["cfg"]
    if "skipped" in rec["result"]: continue
    for n, v in rec["result"]["scores"].items(): rows.append({"set": c["rotation_set"], "rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "score": n, **v})
df = pd.DataFrame(rows); df.to_csv(out / "I7c_all_units.csv", index=False); U = df.groupby(["set", "rot", "repeat", "score"])[["auroc", "fpr95"]].mean().reset_index(); print("unités (jeu, rotation, répétition) :", U[["set", "rot", "repeat"]].drop_duplicates().shape[0])
A = U.pivot_table(index=["set", "rot", "repeat"], columns="score", values="auroc"); Fp = U.pivot_table(index=["set", "rot", "repeat"], columns="score", values="fpr95")
t = U.groupby("score")[["auroc", "fpr95"]].mean().round(4).sort_values("auroc", ascending=False); t.to_csv(out / "I7c_resume.csv"); print(t.head(10).to_string(), "\n", t.loc[["C4_msp", "C64_msp"]].to_string())
top = json.load(open(out / "I7_selected.json"))["score"]; res = []
m = S.multi_paired(A[top].values, A["C4_msp"].values, shift=0.03); m["test"] = f"HI6b AUROC {top} - C4_msp (seuil 0,03)"; res.append(m)
m = S.multi_paired(-Fp[top].values, -Fp["C4_msp"].values, shift=0.05); m["test"] = f"HI7b baisse FPR@95 {top} (seuil 0,05)"; res.append(m)
m = S.multi_paired(A[top].values, A["C4_msp"].values, shift=0.0); m["test"] = f"exploratoire : AUROC {top} - C4_msp (seuil 0)"; res.append(m)
G = pd.DataFrame(res); G.to_csv(out / "I7c_tests.csv", index=False); print(G.round(5).to_string(index=False))
for s in "DEF": d = (A.loc[s][top] - A.loc[s]["C4_msp"]); print(f"jeu {s} : gain moyen {d.mean():+.4f} ({int((d > 0).sum())}/{len(d)} unités en faveur)")
fam = [c for c in A.columns if "fam_" in c and not c.startswith("C4_fam_x")]; print("exploratoire : gain moyen des scores de famille sur C4_msp :", {c: round(float((A[c] - A["C4_msp"]).mean()), 4) for c in fam})
