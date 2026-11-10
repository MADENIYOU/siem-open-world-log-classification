"""Analyse de la vague 4 (D34, D35, HZ1-HZ6). a : sélection (porte HZ5), écrit W4_selected.json ; b : confirmation. Holm sur 6 variantes par mode (brut, M50), condition « toutes » pour la décision. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W4a_selection" if stage == "a" else "P2_W4b_confirmation"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): n, cond, mode = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, "mode": mode, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W4{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
print(df.pivot_table(index="variant", columns=["cond", "mode"], values="f1A").round(4).to_string()); variants = [v for v in df.variant.unique() if v != "LR"]; res = []
for cond in ("toutes", "abs8"):
    for mode in ("brut", "M50"):
        X = df[(df.cond == cond) & (df["mode"] == mode)].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A"); Xs = df[(df.cond == cond) & (df["mode"] == mode)].pivot_table(index=["repeat", "fold"], columns="variant", values="f1_small"); idx0 = len(res)
        for v in variants:
            m = S.multi_paired(X[v].values, X["LR"].values, shift=0.02); m.update({"variante": v, "condition": cond, "mode": mode, "f1A": round(X[v].mean(), 4), "f1A réf": round(X["LR"].mean(), 4), "gain": round(X[v].mean() - X["LR"].mean(), 4), "gain f1_small": round(np.nanmean((Xs[v] - Xs["LR"]).values), 4)}); res.append(m)
        ph = S.holm([r["p_wilcoxon_unilat"] for r in res[idx0:]] + [1.0] * max(0, 6 - (len(res) - idx0)))
        for r, p in zip(res[idx0:], ph): r["p Holm (6)"] = p
G = pd.DataFrame(res); G["passe"] = (G.gain >= 0.02) & (G["p Holm (6)"] < 0.05); cols = ["variante", "condition", "mode", "f1A", "f1A réf", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (6)", "signes +/-", "p_permutation_unilat", "gain f1_small", "passe"]
G[cols].round(5).to_csv(out / f"W4{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
if stage == "a":
    passing = G[(G.condition == "toutes") & G.passe].sort_values("gain", ascending=False); print("\nporte HZ5 (toutes) :", [(r.variante, r["mode"], round(r.gain, 4)) for _, r in passing.iterrows()])
    (out / "W4_selected.json").write_text(json.dumps({"variants": sorted(set(passing.variante))[:3], "details": [[r.variante, r["mode"], round(float(r.gain), 4)] for _, r in passing.iterrows()], "porte_HZ5": len(passing) > 0}, indent=1))
