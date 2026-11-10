"""Analyse de la vague 2 (D29). a : sélection, HX1-HX5, HX7, HX6 (robustesse) ; écrit W2_selected.json. b : confirmation. N'écrit pas le journal. Holm sur 8 variantes (S1, S2, G25, G1, I30, P5, H1, F9S)."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W2a_selection" if stage == "a" else "P2_W2b_confirmation"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": m, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W2{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
P = lambda col: df.pivot_table(index=["repeat", "fold"], columns="variant", values=col); Xa, X30, Xs = P("f1A"), P("f1_30"), P("f1_small"); print({c: round(Xa[c].mean(), 4) for c in Xa.columns})
cands = [c for c in Xa.columns if c not in ("REF_LR", "A1", "A1_abs", "LR_abs")]; res = []
for v in cands:
    m = S.multi_paired(Xa[v].values, Xa["A1"].values, shift=0.01); m.update({"variante": v, "f1A": round(Xa[v].mean(), 4), "f1A A1": round(Xa["A1"].mean(), 4), "gain vs A1": round(Xa[v].mean() - Xa["A1"].mean(), 4), "gain f1_30": round((X30[v] - X30["A1"]).mean(), 4), "gain f1_small": round(np.nanmean((Xs[v] - Xs["A1"]).values), 4)}); res.append(m)
G = pd.DataFrame(res)
if len(G):
    ps = list(G.p_wilcoxon_unilat) + [1.0] * max(0, 8 - len(G)); G["p Holm (m=8)"] = S.holm(ps)[:len(G)]; G["passe"] = (G["gain vs A1"] >= 0.01) & (G["p Holm (m=8)"] < 0.05)
    cols = ["variante", "f1A", "f1A A1", "gain vs A1", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (m=8)", "signes +/-", "p_permutation_unilat", "gain f1_30", "gain f1_small", "passe"]; G[cols].round(5).to_csv(out / f"W2{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
if "A1_abs" in Xa.columns:
    m = S.multi_paired(Xa["A1_abs"].values, Xa["LR_abs"].values, shift=0.02); print("\nHX6 robustesse (8 classes retirées du lot) A1_abs - LR_abs, seuil 0,02 :", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in m.items()}, "| f1A A1_abs", round(Xa["A1_abs"].mean(), 4), "LR_abs", round(Xa["LR_abs"].mean(), 4))
    pd.DataFrame([m]).to_csv(out / f"W2{stage}_robustesse.csv", index=False)
if stage == "a":
    passing = G[G["passe"]].sort_values("gain vs A1", ascending=False) if len(G) else G; print("\nvariantes passant la porte HX7 :", list(passing.variante)); (out / "W2_selected.json").write_text(json.dumps({"variants": list(passing.variante)[:2], "porte_HX7": len(passing) > 0}, indent=1))
