"""Analyse du bloc E (calibration) : tableaux et tests de HE1 à HE6 avec leurs règles préinscrites. N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from scipy import stats
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows, cf = [], []
for rec in R.load_block("E_calibration"):
    if rec["code_version"] != "E2": continue
    c, res = rec["cfg"], rec["result"]
    if "skipped" in res: continue
    for m, v in res.items():
        if m in ("_info", "conforme"): continue
        rows.append({"rot": c["rotation"], "fold": c["fold"], "method": m, **v})
    for nm, v in res["conforme"].items(): cf.append({"rot": c["rotation"], "fold": c["fold"], "calibration": nm, **v})
df = pd.DataFrame(rows); df.to_csv(out / "E_all_units.csv", index=False); cfd = pd.DataFrame(cf); cfd.to_csv(out / "E_conforme_units.csv", index=False); nu = df[["rot", "fold"]].drop_duplicates().shape[0]; print("unités :", nu)
tab = df.groupby("method")[["ece", "brier", "nll", "auroc_msp"]].mean().round(4).sort_values("ece"); tab["écart-type ECE"] = df.groupby("method").ece.std().round(4); tab.to_csv(out / "E_resume.csv"); print("\nmoyennes sur les unités\n", tab.to_string())
key = ["rot", "fold"]; X = {c: df.pivot_table(index=key, columns="method", values=c) for c in ("ece", "auroc_msp")}
def pair(col, a, b, alt="less"):
    d = X[col][a] - X[col][b]; w, p, r = S.wilcoxon_paired(X[col][a].values, X[col][b].values); return {"a": a, "b": b, "mesure": col, "écart a-b": float(d.mean()), "p": p}
M6 = ["temperature", "vector_scaling", "isotonique", "binning", "platt", "temperature_classes_cachees"]
g1 = pd.DataFrame([pair("ece", m, "aucune") for m in M6]); g1["p Holm"] = S.holm(g1.p.values); print("\nHE1 : ECE de chaque méthode contre « aucune » (Holm sur 6)\n", g1.round(5).to_string(index=False))
g2 = pd.DataFrame([pair("ece", "vector_scaling", "temperature")]); print("\nHE2 : vector scaling contre température (ECE)\n", g2.round(5).to_string(index=False))
g3 = pd.DataFrame([pair("ece", m, "temperature") for m in ("isotonique", "binning")]); g3["p Holm"] = S.holm(g3.p.values); print("\nHE3 : isotonique et binning contre température (ECE ; négatif = meilleur que la température)\n", g3.round(5).to_string(index=False))
g4 = pd.DataFrame([pair("auroc_msp", m, "aucune") for m in ("temperature", "platt", "vector_scaling")]); print("\nHE4 : variation de l'AUROC d'inconnu du MSP\n", g4.round(5).to_string(index=False))
g5 = pd.DataFrame([pair("ece", "temperature_memes_gabarits", "temperature")]); print("\nHE5 : température sur mêmes gabarits contre gabarits distincts (ECE ; positif = la fuite aggrave)\n", g5.round(5).to_string(index=False))
c6 = cfd.groupby("calibration")[["couverture", "taille_moy", "vides_connus", "vides_inconnus"]].mean().round(4); print("\nHE6 : prédiction conforme à 90 % (moyenne sur les unités)\n", c6.to_string()); print("   unités dont la couverture >= 0,87 : ", cfd.groupby("calibration").apply(lambda d: int((d.couverture >= 0.87).sum()), include_groups=False).to_dict())
f = S.friedman_nemenyi(-X["ece"].dropna(axis=1).values, list(X["ece"].dropna(axis=1).columns)); print("\nFriedman sur l'ECE (rang 1 = ECE le plus faible) : p = %.3g ; différence critique %.2f ; rangs : %s" % (f["p"], f["cd"], dict(zip(f["names"], np.round(f["avg_ranks"], 2)))))
for n, g in (("HE1", g1), ("HE2", g2), ("HE3", g3), ("HE4", g4), ("HE5", g5)): g.round(5).to_csv(out / f"E_{n}.csv", index=False)
