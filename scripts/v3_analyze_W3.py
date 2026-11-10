"""Analyse de la vague 3 (D30). a : sélection (HY1, HY2), écrit W3_selected.json ; b : confirmation (HY3, HY4). Holm sur 6 variantes par condition. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W3a_selection" if stage == "a" else "P2_W3b_confirmation"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W3{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0]); variants = [v for v in df.variant.unique() if v != "LR"]; res = []
print(df.pivot_table(index="variant", columns="cond", values="f1A").round(4).to_string())
for cond in ("toutes", "abs8", "abs14"):
    d = df[df.cond == cond]; X = d.pivot_table(index=["repeat", "fold"], columns="variant", values="f1A")
    for v in variants:
        m = S.multi_paired(X[v].values, X["LR"].values, shift=0.02); m.update({"variante": v, "condition": cond, "f1A": round(X[v].mean(), 4), "f1A LR": round(X["LR"].mean(), 4), "gain": round(X[v].mean() - X["LR"].mean(), 4)}); res.append(m)
G = pd.DataFrame(res); G["p Holm (6)"] = np.nan
for cond in ("toutes", "abs8", "abs14"):
    idx = G[(G.condition == cond) & (G.variante != "A1")].index; G.loc[idx, "p Holm (6)"] = S.holm(list(G.loc[idx, "p_wilcoxon_unilat"]))
cols = ["variante", "condition", "f1A", "f1A LR", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (6)", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / f"W3{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
if stage == "a":
    cand = []
    for v in variants:
        if v == "A1": continue
        g = G[G.variante == v].set_index("condition"); ok = (g.loc["toutes", "gain"] >= 0.02) and (g.loc["abs8", "gain"] >= 0.02) and (g.loc["toutes", "p Holm (6)"] < 0.05) and (g.loc["abs8", "p Holm (6)"] < 0.05); cand.append((v, min(g.loc["toutes", "gain"], g.loc["abs8", "gain"]), ok))
    cand.sort(key=lambda t: -t[1]); print("\nminimum des gains (toutes, abs8) et porte HY1 :", [(v, round(m, 4), ok) for v, m, ok in cand]); a1 = G[(G.variante == "A1") & (G.condition == "toutes")].gain.iloc[0]
    ok_list = [v for v, m, ok in cand if ok]; print("HY2 : gain de la meilleure en « toutes » :", [(v, round(float(G[(G.variante == v) & (G.condition == 'toutes')].gain.iloc[0]), 4)) for v in ok_list[:1]], "≥ 0,064 ?")
    (out / "W3_selected.json").write_text(json.dumps({"variants": ok_list[:1], "porte_HY1": len(ok_list) > 0, "meilleur_min_gain": cand[0][:2] if cand else None}, indent=1))
