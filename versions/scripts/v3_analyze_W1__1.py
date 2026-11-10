"""Analyse de la vague 1 (D28). a : sélection (porte HW7, tests HW1-HW6, HW8), écrit W1_selected.json ; b : confirmation. N'écrit pas le journal.
Note : D28 annonce « Holm sur les 14 variantes » alors que la liste en compte 13 (A1, A2, B5-B7, C0-C2, D0,5/1/2, E1, E2) : on applique Holm avec m = 14, comme écrit (plus prudent)."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W1a_selection" if stage == "a" else "P2_W1b_confirmation"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": m, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W1{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
P = lambda col: df.pivot_table(index=["repeat", "fold"], columns="variant", values=col); Xa, X30, Xs = P("f1A"), P("f1_30"), P("f1_small")
REF = lambda v: "REF_LR" if v in ("A1", "A2") else "REF_V0"; variants = [c for c in Xa.columns if not c.startswith("REF")]; res = []
for v in variants:
    m = S.multi_paired(Xa[v].values, Xa[REF(v)].values, shift=0.02); m.update({"variante": v, "référence": REF(v), "f1A": round(Xa[v].mean(), 4), "f1A réf": round(Xa[REF(v)].mean(), 4), "gain f1A": round(Xa[v].mean() - Xa[REF(v)].mean(), 4),
        "gain f1_30": round((X30[v] - X30[REF(v)]).mean(), 4), "gain f1_small": round(np.nanmean((Xs[v] - Xs[REF(v)]).values), 4)}); res.append(m)
G = pd.DataFrame(res); ps = list(G.p_wilcoxon_unilat) + [1.0] * max(0, 14 - len(G)); G["p Holm (m=14)"] = S.holm(ps)[:len(G)]; G["passe la porte"] = (G["gain f1A"] >= 0.02) & (G["p Holm (m=14)"] < 0.05)
cols = ["variante", "référence", "f1A", "f1A réf", "gain f1A", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (m=14)", "signes +/-", "p_permutation_unilat", "gain f1_30", "gain f1_small", "passe la porte"]
G[cols].round(5).to_csv(out / f"W1{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False)); print("\nréférences :", {r: round(Xa[r].mean(), 4) for r in ("REF_V0", "REF_LR")})
if stage == "a":
    passing = G[G["passe la porte"]].sort_values("gain f1A", ascending=False); print("\nvariantes passant la porte (HW7) :", list(passing.variante))
    for v in list(passing.variante)[:3]:
        d_small = (Xs[v] - Xs[REF(v)]).dropna(); d_A = (Xa[v] - Xa[REF(v)]).loc[d_small.index]; w, p, r = S.wilcoxon_paired(d_small, d_A); print(f"HW8 {v} : gain classes ≤ 3 gabarits {d_small.mean():+.4f} contre gain palier A {d_A.mean():+.4f} ; Wilcoxon apparié p = {p:.4f}")
    (out / "W1_selected.json").write_text(json.dumps({"variants": list(passing.variante)[:3], "porte_HW7": len(passing) > 0}, indent=1))
