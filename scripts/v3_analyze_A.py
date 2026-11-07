"""Analyse statistique du bloc A : lit les unités calculées par v3_blockA.py et produit les tableaux (CSV) et un résumé lisible.
Questions (règles écrites avant de voir les chiffres) : (1) le découpage au hasard gonfle-t-il le score ? (apparié par pli, Wilcoxon et Cliff) ;
(2) les protocoles par gabarit classent-ils les modèles de la même façon ? (Kendall) ; (3) les méthodes sont-elles réellement différentes ? (Friedman puis Nemenyi, Holm pour les paires) ;
(4) quelle précision d'estimation donne chaque protocole ? (écart-type entre plis) ; (5) fuite résiduelle : part de quasi-jumeaux. Le biais par rapport au test v2 sera mesuré à son ouverture unique."""
import sys, pathlib, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
recs = R.load_block("A_decoupage"); rows = []
for r in recs:
    c, res = r["cfg"], r["result"]
    for m, v in res.items():
        if m == "_info": continue
        rows.append({"protocol": c["protocol"], "repeat": c["repeat"], "fold": c["fold"], "model": m, "f1A": v["f1A"], "f1_30": v["f1_30"], "acc": v["acc"], "param": str(v["param"]), "twin": res["_info"]["twin_share"], "median_nn": res["_info"]["median_nn_cos"]})
df = pd.DataFrame(rows); out = ROOT / "artifacts" / "results" / "v3"; df.to_csv(out / "A_all_units.csv", index=False)
print("unités :", df.groupby("protocol").apply(lambda d: d[["repeat", "fold"]].drop_duplicates().shape[0], include_groups=False).to_dict())
tab = df.groupby(["protocol", "model"]).f1A.agg(["mean", "std", "count"]).round(4); tab.to_csv(out / "A_f1A_par_protocole_modele.csv"); print("\nmacro-F1 palier A (moyenne, écart-type entre plis, nombre de plis)\n", tab.unstack(0)["mean"].round(3).to_string())
tw = df.drop_duplicates(["protocol", "repeat", "fold"]).groupby("protocol").agg(twin=("twin", "mean"), nn=("median_nn", "mean")).round(3); tw.to_csv(out / "A_fuite_par_protocole.csv"); print("\nquasi-jumeaux (cosinus >= 0,90) et cosinus médian au plus proche voisin, par protocole\n", tw.to_string())
# (1) optimisme du hasard : P0 contre P2, apparié par (répétition, pli)
piv = df.pivot_table(index=["repeat", "fold", "model"], columns="protocol", values="f1A").reset_index(); rows1 = []
for m, d in piv.groupby("model"):
    d = d.dropna(subset=["P0", "P2"]); w, p, rr = S.wilcoxon_paired(d.P0, d.P2); rows1.append({"model": m, "P0 moyen": d.P0.mean(), "P2 moyen": d.P2.mean(), "écart (P0 - P2)": d.P0.mean() - d.P2.mean(), "Wilcoxon p": p, "rang bisérié r": rr, "Cliff delta": S.cliffs_delta(d.P0, d.P2), "n": len(d)})
g1 = pd.DataFrame(rows1); g1["p Holm"] = S.holm(g1["Wilcoxon p"].values); g1.round(4).to_csv(out / "A_optimisme_hasard.csv", index=False); print("\n(1) le découpage au hasard gonfle-t-il le score ?\n", g1.round(4).to_string(index=False))
# (2) concordance des classements des modèles entre protocoles
rk = {p: d.groupby("model").f1A.mean().rank(ascending=False) for p, d in df.groupby("protocol")}; ranks = pd.DataFrame(rk); ranks.to_csv(out / "A_rangs_par_protocole.csv"); print("\nrang moyen des modèles par protocole (1 = meilleur)\n", ranks.to_string())
pairs = {f"{a}-{b}": S.kendall_concordance([ranks[a].values, ranks[b].values]) for a, b in itertools.combinations(ranks.columns, 2)}; print("concordance de Kendall entre protocoles :", {k: round(v, 3) for k, v in pairs.items()})
# (3) Friedman + Nemenyi par protocole (blocs = répétition x pli)
rows3 = []
for p, d in df.groupby("protocol"):
    M = d.pivot_table(index=["repeat", "fold"], columns="model", values="f1A").dropna(); fr = S.friedman_nemenyi(M.values, list(M.columns))
    rows3.append({"protocol": p, "blocs": fr["n_blocks"], "chi2": fr["chi2"], "p Friedman": fr["p"], "différence critique (rangs)": fr["cd"], "meilleur": fr["names"][int(np.argmin(fr["avg_ranks"]))]})
    pd.DataFrame(fr["nemenyi_p"], index=fr["names"], columns=fr["names"]).round(4).to_csv(out / f"A_nemenyi_{p}.csv")
g3 = pd.DataFrame(rows3); g3.round(5).to_csv(out / "A_friedman.csv", index=False); print("\n(3) Friedman par protocole\n", g3.round(5).to_string(index=False))
# (4) précision d'estimation
prec = df.groupby("protocol").apply(lambda d: d.groupby("model").f1A.std().mean(), include_groups=False).round(4); prec.to_csv(out / "A_precision.csv"); print("\n(4) écart-type moyen entre plis (plus petit = estimation plus précise)\n", prec.to_string())
