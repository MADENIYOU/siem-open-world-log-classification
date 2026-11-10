"""Analyse de la vague 8 (D38, HQ1-HQ5). a : sélection (porte HQ2/HQ3, candidat de réglage HQ1), écrit W8_selected.json ; b : confirmation. N'écrit pas le journal. Holm sur 4 variantes (ENSP30, ENSP50, ST1, ST2) contre PIPE, seuil 0,02."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W8a_selection" if stage == "a" else "P2_W8b_confirmation"; rows = []; PIPE = "G_C10_T1_a0.5"
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W8{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
Xc = {cond: df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A") for cond in ("toutes", "abs8")}; M = Xc["toutes"]; print("PIPE (toutes) :", round(M[PIPE].mean(), 4), "; abs8 :", round(Xc["abs8"][PIPE].mean(), 4))
others = [v for v in M.columns if not v.startswith("G_") and v != PIPE]; grid = [v for v in M.columns if v.startswith("G_") and v != PIPE]; res = []
if stage == "a":
    gtab = pd.DataFrame({"f1A": M[grid].mean(), "gain vs PIPE": M[grid].mean() - M[PIPE].mean()}).sort_values("f1A", ascending=False); gtab.round(4).to_csv(out / "W8a_grille.csv"); print("\nGRILLE (top 6) :\n", gtab.head(6).round(4).to_string()); best = gtab.index[0]
    for v in others:
        m = S.multi_paired(M[v].values, M[PIPE].values, shift=0.02); m.update({"variante": v, "condition": "toutes", "f1A": round(M[v].mean(), 4), "gain": round(M[v].mean() - M[PIPE].mean(), 4)}); res.append(m)
    ph = S.holm([r["p_wilcoxon_unilat"] for r in res] + [1.0] * max(0, 4 - len(res))); [r.update({"p Holm (4)": p}) for r, p in zip(res, ph)]
    m = S.multi_paired(M[best].values, M[PIPE].values, shift=0.01); m.update({"variante": best + " (candidat HQ1, biaisé)", "condition": "toutes", "f1A": round(M[best].mean(), 4), "gain": round(M[best].mean() - M[PIPE].mean(), 4), "p Holm (4)": np.nan}); res.append(m)
    G = pd.DataFrame(res); cols = ["variante", "condition", "f1A", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (4)", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W8a_tests.csv", index=False); print("\n", G[cols].round(4).to_string(index=False))
    ok = G[(G.variante.isin(others)) & (G.gain >= 0.02) & (G["p Holm (4)"] < 0.05)]; print("\nporte HQ2/HQ3 :", list(ok.variante)); (out / "W8_selected.json").write_text(json.dumps({"variants": [best] + list(ok.variante), "tuning_candidate": best, "porte_HQ2_HQ3": len(ok) > 0}, indent=1))
else:
    sel = json.load(open(out / "W8_selected.json")); cand = sel["tuning_candidate"]
    for cond in ("toutes", "abs8"):
        X = Xc[cond]
        for v in [x for x in X.columns if x != PIPE]:
            sh = 0.01   # D39 : seuil pratique 0,01 pour les trois candidats; m = S.multi_paired(X[v].values, X[PIPE].values, shift=sh); m.update({"variante": v, "condition": cond, "seuil": sh, "f1A": round(X[v].mean(), 4), "f1A PIPE": round(X[PIPE].mean(), 4), "gain": round(X[v].mean() - X[PIPE].mean(), 4)}); res.append(m)
    G = pd.DataFrame(res); cols = ["variante", "condition", "seuil", "f1A", "f1A PIPE", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W8b_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
