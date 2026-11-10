"""Analyse de la vague 11 (D43, HJ1-HJ5). a : sélection (HJ1, HJ2, poids HJ5), écrit W11_selected.json ; c : confirmation (HJ3, HJ4). N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W11a_selection" if stage == "a" else "P2_W11c_confirmation"; rows = []; W = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items():
        if m == "_info": W.append(v); continue
        n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W11{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
M = {cond: df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A") for cond in ("toutes", "abs8", "abs14")}
print(pd.DataFrame({c: M[c].mean() for c in M}).round(4).to_string())
if stage == "a":
    T = M["toutes"]; res = []
    for v in ("STK7", "STK9"):
        m = S.multi_paired(T[v].values, T["STK4"].values, shift=0.01); m.update({"variante": v, "gain vs STK4": round(T[v].mean() - T["STK4"].mean(), 4), "gain vs PIPE": round(T[v].mean() - T["PIPE"].mean(), 4), "abs8 gain vs STK4": round(M["abs8"][v].mean() - M["abs8"]["STK4"].mean(), 4), "abs14 gain vs STK4": round(M["abs14"][v].mean() - M["abs14"]["STK4"].mean(), 4)}); res.append(m)
    ph = S.holm([r["p_wilcoxon_unilat"] for r in res]); [r.update({"p Holm (2)": p}) for r, p in zip(res, ph)]; G = pd.DataFrame(res); cols = ["variante", "gain vs STK4", "gain vs PIPE", "abs8 gain vs STK4", "abs14 gain vs STK4", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (2)", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W11a_tests.csv", index=False); print("\n", G[cols].round(4).to_string(index=False))
    wt = {s: pd.DataFrame([w[s] for w in W if s in w]) for s in ("STK4", "STK7", "STK9")}
    for s, d in wt.items(): print(f"\npoids moyens {s} (écart-type) :", {c: f"{d[c].mean():.3f} ({d[c].std():.3f})" for c in d.columns}); d.agg(["mean", "std"]).round(4).to_csv(out / f"W11a_poids_{s}.csv")
    best = G.sort_values("gain vs STK4", ascending=False).iloc[0].variante; (out / "W11_selected.json").write_text(json.dumps({"variants": [best]}, indent=1)); print("\nvariante retenue pour la confirmation :", best)
else:
    sel = json.load(open(out / "W11_selected.json"))["variants"]; v = sel[0]; res = []
    for cond in ("toutes", "abs8", "abs14"):
        X = M[cond]; sh = 0.01 if cond == "toutes" else -0.01
        m = S.multi_paired(X[v].values, X["STK4"].values, shift=sh); m.update({"comparaison": f"{v} - STK4", "condition": cond, "seuil": sh, "f1A": round(X[v].mean(), 4), "f1A réf": round(X["STK4"].mean(), 4), "gain": round(X[v].mean() - X["STK4"].mean(), 4)}); res.append(m)
        m = S.multi_paired(X["STK4"].values, X["PIPE"].values, shift=0.0); m.update({"comparaison": "STK4 - PIPE", "condition": cond, "seuil": 0.0, "f1A": round(X["STK4"].mean(), 4), "f1A réf": round(X["PIPE"].mean(), 4), "gain": round(X["STK4"].mean() - X["PIPE"].mean(), 4)}); res.append(m)
    G = pd.DataFrame(res); cols = ["comparaison", "condition", "seuil", "f1A", "f1A réf", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W11c_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
    from scipy.stats import binomtest
    X = M["toutes"]; k = int(((X[v] - X["STK4"]) > 0.01).sum()); print(f"\nHJ3 signes (gain > 0,01) : {k}/{len(X)} p unilatéral = {binomtest(k, len(X), 0.5, alternative='greater').pvalue:.4f}")
