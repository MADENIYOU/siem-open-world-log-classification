"""Analyse de la vague 6 (D37, HR1-HR4). a : sélection (porte), écrit W6_selected.json ; b : confirmation. Références : V-REx contre ERM ; embeddings contre LR ; mode M50 contre la référence décodée. Holm sur 6 variantes par mode. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; block = "P2_W6a_selection" if stage == "a" else "P2_W6b_confirmation"; rows = []
for rec in R.load_block(block):
    c = rec["cfg"]
    for m, v in rec["result"].items(): n, cond, mode = m.split("|"); rows.append({"repeat": c["repeat"], "fold": c["fold"], "variant": n, "mode": mode, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W6{stage}_all_units.csv", index=False); print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0]); print(df.pivot_table(index="variant", columns="mode", values="f1A").round(4).to_string())
REF = lambda v: "ERM" if v.startswith("VR") else "LR"; res = []
for mode in ("brut", "M50"):
    X = df[df["mode"] == mode].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A"); idx0 = len(res)
    for v in [c for c in X.columns if c not in ("LR", "ERM")]:
        m = S.multi_paired(X[v].values, X[REF(v)].values, shift=0.02); m.update({"variante": v, "mode": mode, "f1A": round(X[v].mean(), 4), "f1A réf": round(X[REF(v)].mean(), 4), "réf": REF(v), "gain": round(X[v].mean() - X[REF(v)].mean(), 4), "gain vs LR": round(X[v].mean() - X["LR"].mean(), 4)}); res.append(m)
    ph = S.holm([r["p_wilcoxon_unilat"] for r in res[idx0:]] + [1.0] * max(0, 6 - (len(res) - idx0)))
    for r, p in zip(res[idx0:], ph): r["p Holm (6)"] = p
G = pd.DataFrame(res); G["passe"] = (G.gain >= 0.02) & (G["p Holm (6)"] < 0.05); cols = ["variante", "mode", "réf", "f1A", "f1A réf", "gain", "gain vs LR", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (6)", "signes +/-", "p_permutation_unilat", "passe"]
G[cols].round(5).to_csv(out / f"W6{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
if stage == "a":
    ok = G[G.passe]; print("\nporte :", [(r.variante, r["mode"], round(r.gain, 4)) for _, r in ok.iterrows()]); (out / "W6_selected.json").write_text(json.dumps({"variants": sorted(set(ok.variante))[:3], "porte": len(ok) > 0}, indent=1))
