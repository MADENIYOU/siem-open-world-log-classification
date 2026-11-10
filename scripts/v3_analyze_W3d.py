"""Analyse de la réplication finale W3d (D33, HY9). N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_W3d_final"):
    c = rec["cfg"]
    for m, v in rec["result"].items(): n, cond = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "cond": cond, **v})
df = pd.DataFrame(rows); df.to_csv(out / "W3d_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0]); print(df.pivot_table(index="variant", columns="cond", values="f1A").round(4).to_string()); res = []
for cond in ("toutes", "abs8", "abs14"):
    X = df[df.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A")
    for v in ("M50", "A1"):
        m = S.multi_paired(X[v].values, X["LR"].values, shift=0.02); m.update({"variante": v, "condition": cond, "gain": round(X[v].mean() - X["LR"].mean(), 4)}); res.append(m)
    m = S.multi_paired(X["M50"].values, X["A1"].values, shift=0.0); m.update({"variante": "M50 - A1", "condition": cond, "gain": round(X["M50"].mean() - X["A1"].mean(), 4)}); res.append(m)
G = pd.DataFrame(res); cols = ["variante", "condition", "gain", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "signes +/-", "p_signes_bilat", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / "W3d_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
