"""Analyse d'I5a : sélection de la configuration (répétitions 0 à 4, D21) et porte HF14. Écrit la configuration retenue dans artifacts/results/v3/I5_selected.json. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("P2_I5a_selection"):
    c = rec["cfg"]
    for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "config": m, **v})
df = pd.DataFrame(rows); n = df[["repeat", "fold"]].drop_duplicates().shape[0]; print("plis :", n)
t = df.groupby("config")[["f1A", "f1_fam", "tree_dist"]].mean().round(4).sort_values("f1A", ascending=False); t["nb plis > V0"] = 0
V0 = df[df.config == "mots_C1"].set_index(["repeat", "fold"]).f1A
for cfg in t.index: t.loc[cfg, "nb plis > V0"] = int((df[df.config == cfg].set_index(["repeat", "fold"]).f1A > V0).sum())
t["gain f1A vs V0"] = (t.f1A - t.loc["mots_C1", "f1A"]).round(4); t.to_csv(out / "I5a_resume.csv"); print(t.head(12).to_string()); print("\nréférences :\n", t.loc[["mots_C1", "somme_mC1_l35C1_w1"]].to_string())
best = t.index[0]; gain = float(t.loc[best, "gain f1A vs V0"]); print("\nmeilleure :", best, "gain", gain, "| porte HF14 (>= 0,02) :", gain >= 0.02)
(out / "I5_selected.json").write_text(json.dumps({"config": best, "gain_dev": gain, "f1A_dev": float(t.loc[best, "f1A"]), "porte_HF14": gain >= 0.02}, indent=1))
