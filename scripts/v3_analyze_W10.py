"""Analyse de la vague 10 (D41, HK7-HK10). a : degrés étendus, meilleure configuration de chaque famille (HK7), écrit W10_selected.json ; c : réplication finale, éligibilité (HK8), choix du pipeline (HK9), robustesse (HK10). N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W10a_selection" if stage == "a" else "P2_W10c_final"; rows = []; PIPE = "LR_B0_T1_a0.5"
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items():
        if m == "_info": continue
        n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W10{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
M = {cond: df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A") for cond in df.cond.unique()}; T = M["toutes"]; print("PIPE (toutes) :", round(T[PIPE].mean(), 4))
if stage == "a":
    tab = pd.DataFrame({"f1A": T.mean(), "gain vs PIPE": T.mean() - T[PIPE].mean(), "abs8 gain": M["abs8"].mean() - M["abs8"][PIPE].mean()}).sort_values("f1A", ascending=False); tab.round(4).to_csv(out / "W10a_grille.csv"); print(tab.round(4).to_string())
    e1 = [c for c in T.columns if c.startswith("AXE")]; e2 = [c for c in T.columns if c.startswith("STK")]; b1 = tab.loc[e1].index[0]; b2 = tab.loc[e2].index[0]
    t1, a1 = float(b1.split("_")[2][1:]), float(b1.split("_")[3][1:]); t2, a2 = float(b2.split("_")[1][1:]), float(b2.split("_")[2][1:]); hk7 = (t1 < 4 and a1 > 0.1, t2 < 3 and a2 > 0.1)
    print(f"\nmeilleure famille AXE : {b1} (T {t1:g}, alpha {a1:g}) ; meilleure famille STK : {b2} (T {t2:g}, alpha {a2:g}) ; HK7 (optimum intérieur) AXE : {hk7[0]}, STK : {hk7[1]}")
    cand = list(dict.fromkeys(["AXE05_B1_T2_a0.25", "STK_T1_a0.5", b1, b2])); (out / "W10_selected.json").write_text(json.dumps({"candidates": cand, "best_axe": b1, "best_stk": b2, "hk7": {"axe_interieur": bool(hk7[0]), "stk_interieur": bool(hk7[1])}}, indent=1)); print("candidats pour la réplication finale :", cand)
else:
    sel = json.load(open(out / "W10_selected.json")); cands = sel["candidates"]; res = []; summary = {}
    for cond in ("toutes", "abs8", "abs14"):
        X = M[cond]
        for v in cands:
            sh = 0.02 if cond == "toutes" else 0.0; m = S.multi_paired(X[v].values, X[PIPE].values, shift=sh); g = X[v].mean() - X[PIPE].mean(); m.update({"variante": v, "condition": cond, "seuil": sh, "f1A": round(X[v].mean(), 4), "f1A PIPE": round(X[PIPE].mean(), 4), "gain": round(g, 4)}); res.append(m); summary[(v, cond)] = (g, m)
    G = pd.DataFrame(res); cols = ["variante", "condition", "seuil", "f1A", "f1A PIPE", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_signes_bilat", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W10c_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
    from scipy.stats import binomtest
    elig = []; print("\nÉLIGIBILITÉ (HK8) : borne basse >= 0,02 et p < 0,0125 (Wilcoxon, signes unilatéral, permutation), condition toutes")
    for v in cands:
        g, m = summary[(v, "toutes")]; X = T; k = int(((X[v] - X[PIPE]) > 0.02).sum()); n = len(X); ps = binomtest(k, n, 0.5, alternative="greater").pvalue; ok = m["IC95_bas"] >= 0.02 and m["p_wilcoxon_unilat"] < 0.0125 and ps < 0.0125 and m["p_permutation_unilat"] < 0.0125
        mins = min(summary[(v, c)][0] for c in ("toutes", "abs8", "abs14")); print(f"  {v:22s} gain {g:+.4f} IC95 [{m['IC95_bas']:.4f} ; {m['IC95_haut']:.4f}] signes {k}/{n} (p {ps:.4f}) éligible : {ok} ; minimum des gains sur les 3 conditions : {mins:+.4f}"); 
        if ok: elig.append((v, mins))
    elig.sort(key=lambda t: -t[1]); print("\néligibles par minimum décroissant :", [(v, round(m, 4)) for v, m in elig])
    if elig:
        best = elig[0][0]
        if len(elig) > 1 and elig[0][1] - elig[1][1] < 0.005: best = "STK_T1_a0.5" if any(v == "STK_T1_a0.5" for v, _ in elig[:2]) else elig[0][0]
    else: best = "AXE05_B1_T2_a0.25"
    print("CHOIX (HK9) :", best)
    for c in ("abs8", "abs14"): g, m = summary[(best, c)]; print(f"HK10 {best} {c} : gain {g:+.4f} IC95 [{m['IC95_bas']:.4f} ; {m['IC95_haut']:.4f}] borne basse > 0 : {m['IC95_bas'] > 0}")
    (out / "W10_choice.json").write_text(json.dumps({"pipeline_gele": best, "eligibles": [v for v, _ in elig]}, indent=1))
