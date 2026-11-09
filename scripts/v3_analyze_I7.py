"""Analyse I7 (D24). Usage : python scripts/v3_analyze_I7.py a|b. a : sélection sur rotations B (porte HI5, Friedman/Nemenyi), écrit I7_selected.json ; b : confirmation HI6, HI7 sur rotations C. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = f"P2_I7{stage}_rejet_v2"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    if "skipped" in rec["result"]: continue
    for n, v in rec["result"]["scores"].items(): rows.append({"rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "score": n, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"I7{stage}_all_units.csv", index=False); U = df.groupby(["rot", "repeat", "score"])[["auroc", "fpr95"]].mean().reset_index(); print("unités (rotation, répétition) :", U[["rot", "repeat"]].drop_duplicates().shape[0])
A = U.pivot_table(index=["rot", "repeat"], columns="score", values="auroc"); Fp = U.pivot_table(index=["rot", "repeat"], columns="score", values="fpr95"); t = U.groupby("score")[["auroc", "fpr95"]].mean().round(4).sort_values("auroc", ascending=False); t.to_csv(out / f"I7{stage}_resume.csv"); print(t.to_string())
if stage == "a":
    cand = [c for c in A.columns if not c.startswith("C4_")]; ref = "C4_msp"; t = t.loc[[c for c in t.index if c in cand]]; top = t.index[0]; gain = float(t.loc[top, "auroc"] - A[ref].mean()); print("référence msp (C = 4) :", round(float(A[ref].mean()), 4), "; meilleure candidate :", top, "gain", round(gain, 4), "| porte HI5 (>= 0,03) :", gain >= 0.03)
    mp = S.multi_paired(A[top].values, A[ref].values, shift=0.03); print("tests (sélection, biaisés) :", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in mp.items()})
    f = S.friedman_nemenyi(A[cand].values, cand); rk = pd.Series(f["avg_ranks"], index=f["names"]).sort_values(); best = rk.index[0]; print("Friedman p = %.3g, différence critique %.2f, meilleur au rang : %s, indiscernables du meilleur : %d" % (f["p"], f["cd"], best, sum(rk - rk[best] < f["cd"])))
    pd.DataFrame({"rang moyen": rk, "indiscernable du meilleur": rk - rk[best] < f["cd"]}).to_csv(out / "I7a_friedman.csv"); top = t.index[0]
    (out / "I7_selected.json").write_text(json.dumps({"score": top, "auroc_B": float(t.loc[top, "auroc"]), "gain_vs_msp_C4": gain, "porte_HI5": gain >= 0.03, "friedman_p": f["p"]}, indent=1)); print("retenue :", top)
else:
    sel = json.load(open(out / "I7_selected.json")); top = sel["score"]; print("retenue :", top)
    res = []
    for ref in ("C4_msp",):
        m = S.multi_paired(A[top].values, A[ref].values, shift=0.03); m["test"] = f"AUROC {top} - {ref} (seuil 0,03)"; res.append(m)
    mf = S.multi_paired(-Fp[top].values, -Fp["C4_msp"].values, shift=0.05); mf["test"] = f"FPR@95 baisse {top} - C4_msp (seuil 0,05)"; res.append(mf)
    G = pd.DataFrame(res); G.to_csv(out / "I7b_tests.csv", index=False); print(G.round(5).to_string(index=False))
