"""Analyse de la vague 12 (D44, HN1-HN3). a : sélection (HN1), règle « IC entièrement sous 0 », écrit W12_selected.json ; c : confirmation (HN2, HN3). N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W12a_selection" if stage == "a" else "P2_W12c_confirmation"; rows = []; WT = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items():
        if m == "_info": WT.append(v); continue
        n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W12{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
M = {cond: df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A") for cond in ("toutes", "abs8", "abs14")}; print(pd.DataFrame({c: M[c].mean() for c in M}).round(4).to_string())
if stage == "a":
    T = M["toutes"]; res = []
    for v in [c for c in T.columns if c not in ("PIPE", "STK4")]:
        m = S.multi_paired(T[v].values, T["STK4"].values, shift=0.01); m.update({"variante": v, "gain vs STK4": round(T[v].mean() - T["STK4"].mean(), 4), "abs8 gain": round(M["abs8"][v].mean() - M["abs8"]["STK4"].mean(), 4), "abs14 gain": round(M["abs14"][v].mean() - M["abs14"]["STK4"].mean(), 4), "gain brut (sans seuil)": 0}); res.append(m)
    ph = S.holm([r["p_wilcoxon_unilat"] for r in res] + [1.0] * max(0, 4 - len(res))); [r.update({"p Holm (4)": p}) for r, p in zip(res, ph)]; G = pd.DataFrame(res); cols = ["variante", "gain vs STK4", "abs8 gain", "abs14 gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (4)", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W12a_tests.csv", index=False); print("\n", G[cols].round(4).to_string(index=False))
    for s in ("F4", "F9"):
        d = pd.DataFrame([w[s] for w in WT if s in w]); print(f"\n{s} : F1 hors-gabarit initial {d.oof_f1_init.mean():.4f} -> optimisé {d.oof_f1_opt.mean():.4f} (écart moyen {np.mean(d.oof_f1_opt - d.oof_f1_init):+.4f}) ; poids moyens :", np.round(np.mean([w for w in d.w], axis=0), 3).tolist())
    best = G.sort_values("gain vs STK4", ascending=False).iloc[0]; neg = best.IC95_haut < 0; print("\nmeilleure variante :", best.variante, "gain", best["gain vs STK4"], "| IC entièrement sous 0 (pas de confirmation) :", bool(neg)); (out / "W12_selected.json").write_text(json.dumps({"variants": [best.variante], "confirmer": (not bool(neg))}, indent=1))
else:
    v = json.load(open(out / "W12_selected.json"))["variants"][0]; res = []
    for cond in ("toutes", "abs8", "abs14"):
        X = M[cond]; sh = 0.01 if cond == "toutes" else -0.01; m = S.multi_paired(X[v].values, X["STK4"].values, shift=sh); m.update({"comparaison": f"{v} - STK4", "condition": cond, "seuil": sh, "f1A": round(X[v].mean(), 4), "f1A STK4": round(X["STK4"].mean(), 4), "gain": round(X[v].mean() - X["STK4"].mean(), 4)}); res.append(m)
    G = pd.DataFrame(res); cols = ["comparaison", "condition", "seuil", "f1A", "f1A STK4", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W12c_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
    from scipy.stats import binomtest
    X = M["toutes"]; k = int(((X[v] - X["STK4"]) > 0.01).sum()); print(f"\nHN2 signes (gain > 0,01) : {k}/{len(X)} p unilatéral = {binomtest(k, len(X), 0.5, alternative='greater').pvalue:.4f}")
