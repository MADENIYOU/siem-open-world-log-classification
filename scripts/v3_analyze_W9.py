"""Analyse de la vague 9 (D40, HK1-HK6). a : effets principaux (HK1), interactions (HK2), STK (HK3), choix des candidats ; b : confirmation (HK4-HK6). N'écrit pas le journal."""
import sys, json, pathlib, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W9a_selection" if stage == "a" else "P2_W9b_confirmation"; rows = []; PIPE = "LR_B0_T1_a0.5"; info = []
for rec in R.load_block(block):
    c = rec["cfg"]
    if "_info" in rec["result"] and rec["result"]["_info"]: info.append(rec["result"]["_info"].get("stk_weights"))
    for m, v in rec["result"].items():
        if m == "_info": continue
        n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W9{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0])
M = {cond: df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A") for cond in ("toutes", "abs8")}; T = M["toutes"]; print("PIPE (toutes) :", round(T[PIPE].mean(), 4), "; abs8 :", round(M["abs8"][PIPE].mean(), 4))
parse = lambda n: dict(zip("A B T a".split(), (n.split("_")[0], float(n.split("_")[1][1:]), float(n.split("_")[2][1:]), float(n.split("_")[3][1:])))) if n != "STK" else None
if stage == "a":
    grid = [c for c in T.columns if c != "STK"]; tab = pd.DataFrame({"f1A": T[grid].mean(), "gain vs PIPE": T[grid].mean() - T[PIPE].mean(), "abs8 gain": (M["abs8"][grid].mean() - M["abs8"][PIPE].mean())}).sort_values("f1A", ascending=False); tab.round(4).to_csv(out / "W9a_grille.csv"); print("\nTOP 8 :\n", tab.head(8).round(4).to_string())
    print("STK :", round(T["STK"].mean(), 4), "gain", round(T["STK"].mean() - T[PIPE].mean(), 4), "| poids moyens (wc, wo, wa, wf) :", np.round(np.nanmean([w for w in info if w], axis=0), 3).tolist())
    def mean_over(filter_fn): cols = [c for c in grid if filter_fn(parse(c))]; return T[cols].mean(1)
    def paired_contrast(fac, l1, l0):
        d = []
        for c in grid:
            p = parse(c)
            if p[fac] == l1: q = dict(p); q[fac] = l0; c0 = f"{q['A']}_B{q['B']:g}_T{q['T']:g}_a{q['a']:g}"; d.append(T[c] - T[c0])
        return pd.concat(d, axis=1).mean(1)
    G = []
    for fac, l1, l0 in (("A", "AXE05", "LR"), ("A", "AXE1", "LR"), ("B", 0.5, 0.0), ("B", 1.0, 0.0), ("B", 2.0, 0.0), ("T", 0.5, 1.0), ("T", 2.0, 1.0), ("a", 0.25, 0.5), ("a", 0.75, 0.5)):
        d = paired_contrast(fac, l1, l0); m = S.multi_paired(d.values, np.zeros(len(d)), shift=0.01); m.update({"contraste": f"{fac}: {l1} contre {l0}", "effet moyen": round(float(d.mean()), 4)}); G.append(m)
    ph = S.holm([g["p_wilcoxon_unilat"] for g in G]); [g.update({"p Holm (9)": p}) for g, p in zip(G, ph)]; H1 = pd.DataFrame(G); cols = ["contraste", "effet moyen", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (9)", "signes +/-", "p_permutation_unilat"]; H1[cols].round(5).to_csv(out / "W9a_HK1.csv", index=False); print("\nHK1 effets principaux (seuil 0,01) :\n", H1[cols].round(4).to_string(index=False))
    f = lambda c: T[c]; cellsTa = [(t, al) for t in (0.5, 1.0, 2.0) for al in (0.25, 0.5, 0.75)]; I = []
    def inter(name, vals): v = pd.concat(vals, axis=1).mean(1); m = S.multi_paired(v.values, np.zeros(len(v)), shift=0.0); m.update({"interaction": name, "valeur moyenne": round(float(v.mean()), 4)}); I.append(m)
    inter("A=AXE05 x B=0,5", [f(f"AXE05_B0.5_T{t:g}_a{al:g}") - f(f"AXE05_B0_T{t:g}_a{al:g}") - f(f"LR_B0.5_T{t:g}_a{al:g}") + f(f"LR_B0_T{t:g}_a{al:g}") for t, al in cellsTa])
    inter("A=AXE05 x alpha=0,25", [f(f"AXE05_B{b:g}_T{t:g}_a0.25") - f(f"AXE05_B{b:g}_T{t:g}_a0.5") - f(f"LR_B{b:g}_T{t:g}_a0.25") + f(f"LR_B{b:g}_T{t:g}_a0.5") for b in BS_ for t in (0.5, 1.0, 2.0)] if (BS_ := (0, 0.5, 1, 2)) else [])
    inter("B=0,5 x alpha=0,25", [f(f"{a}_B0.5_T{t:g}_a0.25") - f(f"{a}_B0.5_T{t:g}_a0.5") - f(f"{a}_B0_T{t:g}_a0.25") + f(f"{a}_B0_T{t:g}_a0.5") for a in ("LR", "AXE05", "AXE1") for t in (0.5, 1.0, 2.0)])
    H2 = pd.DataFrame(I); H2[["interaction", "valeur moyenne", "IC95_bas", "IC95_haut", "signes +/-"]].round(5).to_csv(out / "W9a_HK2.csv", index=False); print("\nHK2 interactions (additivité = 0) :\n", H2[["interaction", "valeur moyenne", "IC95_bas", "IC95_haut", "signes +/-"]].round(4).to_string(index=False))
    m = S.multi_paired(T["STK"].values, T[PIPE].values, shift=0.02); print("\nHK3 STK contre PIPE (seuil 0,02) :", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in m.items()}); pd.DataFrame([m]).to_csv(out / "W9a_HK3.csv", index=False)
    cand, seen = [], set()
    for c in tab.index:
        if c == PIPE: continue
        p = parse(c); key = (p["A"], p["B"])
        if key in seen: continue
        seen.add(key); cand.append(c)
        if len(cand) == 3: break
    print("\ncandidats (3 meilleures configurations à (A, B) distincts) + STK :", cand); (out / "W9_selected.json").write_text(json.dumps({"variants": cand + ["STK"], "gain_selection": {c: round(float(T[c].mean() - T[PIPE].mean()), 4) for c in cand + ["STK"]}}, indent=1))
else:
    sel = json.load(open(out / "W9_selected.json")); sg = sel["gain_selection"]; res = []
    for cond in ("toutes", "abs8"):
        X = M[cond]
        for v in sel["variants"]:
            m = S.multi_paired(X[v].values, X[PIPE].values, shift=0.01); g = X[v].mean() - X[PIPE].mean(); m.update({"variante": v, "condition": cond, "f1A": round(X[v].mean(), 4), "f1A PIPE": round(X[PIPE].mean(), 4), "gain": round(g, 4), "gain sélection": sg[v], "ratio conf/sél": round(g / sg[v], 2) if sg[v] else np.nan}); res.append(m)
    G = pd.DataFrame(res); cols = ["variante", "condition", "f1A", "f1A PIPE", "gain", "gain sélection", "ratio conf/sél", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W9b_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
