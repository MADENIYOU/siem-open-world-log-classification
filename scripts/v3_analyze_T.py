"""Analyse du bloc T (grille Transformer, 90 modèles) : HT1 à HT4 avec leurs règles préinscrites. Unité de HT1-HT3 : couple (fichier p, rotation), moyenne des 3 graines (30 couples) ; HT4 : couples (rotation, graine) 15. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("T_transformer"):
    c, r = rec["cfg"], rec["result"]; t, b = r["transformer"], r["tfidf_memes_logs"]
    row = {"p": c["file"], "rot": c["rotation"], "seed": c["seed"], "f1A_T": t["closed"]["f1A"], "f1A_B": b["closed"]["f1A"], "f1_30_T": t["closed"]["f1_30"], "f1_30_B": b["closed"]["f1_30"], "train_min": r["info"]["train_minutes"]}
    for s, v in t["open"].items(): row[f"auroc_T_{s}"] = v["auroc"]; row[f"fpr95_T_{s}"] = v["fpr95"]
    for s, v in b["open"].items(): row[f"auroc_B_{s}"] = v["auroc"]; row[f"fpr95_B_{s}"] = v["fpr95"]
    rows.append(row)
df = pd.DataFrame(rows); df.to_csv(out / "T_all_units.csv", index=False); print("modèles :", len(df))
print(df.groupby("p")[["f1A_T", "f1A_B", "auroc_T_msp", "auroc_T_fam_msp", "auroc_T_maha_shared", "auroc_B_msp", "auroc_B_fam_msp"]].mean().round(4).to_string())
C = df.groupby(["p", "rot"]).mean(numeric_only=True).reset_index(); print("couples :", len(C))
def boot(d):
    rng = np.random.default_rng(0); b = [d[rng.integers(0, len(d), len(d))].mean() for _ in range(10000)]; return f"[{np.percentile(b, 2.5):.4f} ; {np.percentile(b, 97.5):.4f}]"
res = []
d1 = (C.f1A_T - C.f1A_B).values; w, p, r = S.wilcoxon_paired(C.f1A_T - 0.02, C.f1A_B); p1 = p / 2 if (d1 - 0.02).mean() < 0 else 1 - p / 2
res.append({"hyp": "HT1", "énoncé": "F1A Transformer - TF-IDF <= 0,02", "écart moyen": round(float(d1.mean()), 4), "IC95": boot(d1), "p (unilatéral, H1 : écart < 0,02)": p1, "couples T>B": int((d1 > 0).sum()), "n": len(d1)})
d2 = (C.auroc_T_maha_shared - C.auroc_T_msp).values; w, p, r = S.wilcoxon_paired(C.auroc_T_maha_shared - 0.03, C.auroc_T_msp); p2 = p / 2 if (d2 - 0.03).mean() > 0 else 1 - p / 2
res.append({"hyp": "HT2", "énoncé": "AUROC Mahalanobis - MSP >= 0,03", "écart moyen": round(float(d2.mean()), 4), "IC95": boot(d2), "p (unilatéral, H1 : écart > 0,03)": p2, "couples T>B": int((d2 > 0).sum()), "n": len(d2)})
d3 = (C.auroc_T_fam_msp - C.auroc_T_msp).values; w, p, r = S.wilcoxon_paired(C.auroc_T_fam_msp - 0.02, C.auroc_T_msp); p3 = p / 2 if (d3 - 0.02).mean() > 0 else 1 - p / 2
res.append({"hyp": "HT3", "énoncé": "AUROC famille - MSP >= 0,02", "écart moyen": round(float(d3.mean()), 4), "IC95": boot(d3), "p (unilatéral, H1 : écart > 0,02)": p3, "couples T>B": int((d3 > 0).sum()), "n": len(d3)})
ps = S.holm([x["p (unilatéral, H1 : écart < 0,02)"] if x["hyp"] == "HT1" else x[[k for k in x if k.startswith("p (")][0]] for x in res]); [x.update({"p Holm (HT1-HT3)": q}) for x, q in zip(res, ps)]
P = df.pivot_table(index=["rot", "seed"], columns="p", values=["f1A_T", "f1A_B"]); lossT = (P["f1A_T"][0] - P["f1A_T"][5]).values; lossB = (P["f1A_B"][0] - P["f1A_B"][5]).values; d4 = lossB - lossT; w, p, r = S.wilcoxon_paired(P["f1A_B"][0] - P["f1A_B"][5], P["f1A_T"][0] - P["f1A_T"][5]); p4 = p / 2 if d4.mean() > 0 else 1 - p / 2
res.append({"hyp": "HT4", "énoncé": "perte F1A p0->p0,5 : TF-IDF - Transformer > 0", "écart moyen": round(float(d4.mean()), 4), "IC95": boot(d4), "p (unilatéral, H1 : écart > 0)": p4, "couples T>B": int((d4 > 0).sum()), "n": len(d4), "perte T": round(float(lossT.mean()), 4), "perte B": round(float(lossB.mean()), 4)})
G = pd.DataFrame(res); G.to_csv(out / "T_tests.csv", index=False); print(G.round(5).to_string(index=False))
print("\nmoyennes globales (90 modèles):\n", df[[c for c in df.columns if c.startswith(("f1A", "auroc", "fpr95"))]].mean().round(4).to_string())
