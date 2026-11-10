"""Analyse de la vague 5 (D37, HO1-HO3). a : sélection, écrit W5_selected.json ; b : confirmation. Unité (rotation, répétition). Holm sur 3 variantes. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]; rows = []
for rec in R.load_block(f"P2_W5{stage}_rejet_decode"):
    c = rec["cfg"]
    if "skipped" in rec["result"]: continue
    for n, v in rec["result"]["scores"].items(): rows.append({"rot": c["rotation"], "repeat": c["repeat"], "fold": c["fold"], "score": n, **v})
df = pd.DataFrame(rows); df.to_csv(out / f"W5{stage}_all_units.csv", index=False); U = df.groupby(["rot", "repeat", "score"])[["auroc", "fpr95"]].mean().reset_index(); print("unités (rotation, répétition) :", U[["rot", "repeat"]].drop_duplicates().shape[0])
A = U.pivot_table(index=["rot", "repeat"], columns="score", values="auroc"); Fp = U.pivot_table(index=["rot", "repeat"], columns="score", values="fpr95"); print(U.groupby("score")[["auroc", "fpr95"]].mean().round(4).to_string())
res = []; cand = ["FAMQ", "FAMD", "MSPQ"]
for v in cand:
    m = S.multi_paired(A[v].values, A["FAM"].values, shift=0.02); m.update({"variante": v, "mesure": "AUROC (gain)"}); res.append(m)
ph = S.holm([r["p_wilcoxon_unilat"] for r in res]); [r.update({"p Holm (3)": p}) for r, p in zip(res, ph)]; n1 = len(res)
for v in cand:
    m = S.multi_paired(-Fp[v].values, -Fp["FAM"].values, shift=0.03); m.update({"variante": v, "mesure": "FPR@95 (baisse)"}); res.append(m)
ph = S.holm([r["p_wilcoxon_unilat"] for r in res[n1:]]); [r.update({"p Holm (3)": p}) for r, p in zip(res[n1:], ph)]
G = pd.DataFrame(res); cols = ["variante", "mesure", "écart moyen", "IC95_bas", "IC95_haut", "p_wilcoxon_unilat", "p Holm (3)", "signes +/-", "p_permutation_unilat"]; G[cols].round(5).to_csv(out / f"W5{stage}_tests.csv", index=False); print(G[cols].round(4).to_string(index=False))
if stage == "a":
    ok = G[(G["écart moyen"] >= (0.02 if True else 0)) & (G["p Holm (3)"] < 0.05)]; ok = ok.assign(seuil=np.where(ok.mesure.str.startswith("AUROC"), 0.02, 0.03)); ok = ok[ok["écart moyen"] >= ok.seuil]
    print("\nporte (HO1/HO2) :", [(r.variante, r.mesure, round(r["écart moyen"], 4)) for _, r in ok.iterrows()]); (out / "W5_selected.json").write_text(json.dumps({"variants": sorted(set(ok.variante))[:1], "porte": len(ok) > 0}, indent=1))
