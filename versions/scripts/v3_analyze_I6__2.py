"""Analyse I6 (D23). Usage : python scripts/v3_analyze_I6.py a|b. Étape a : sélection, porte HF17, Friedman/Nemenyi (HF19), écrit I6_selected.json. Étape b : confirmation HF18 avec plusieurs tests. N'écrit pas le journal."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; stage = sys.argv[1]
def load(block):
    rows = []
    for rec in R.load_block(block):
        c = rec["cfg"]
        for m, v in rec["result"].items(): rows.append({"repeat": c["repeat"], "fold": c["fold"], "config": m, **v})
    return pd.DataFrame(rows)
if stage == "a":
    df = load("P2_I6a_selection"); df.to_csv(out / "I6a_all_units.csv", index=False); n = df[["repeat", "fold"]].drop_duplicates().shape[0]; print("plis :", n)
    X = df.pivot_table(index=["repeat", "fold"], columns="config", values="f1A"); t = df.groupby("config")[["f1A", "f1_fam", "tree_dist"]].mean().round(4)
    ref = pd.read_csv(out / "I5a_all_units.csv") if (out / "I5a_all_units.csv").exists() else None
    V0 = df_v0 = pd.read_csv(out / "I1_all_units.csv"); V0 = V0[(V0.model == "V0") & (V0.repeat < 5)].set_index(["repeat", "fold"]).f1A; v0m = float(V0.mean())
    t["gain f1A vs V0"] = (t.f1A - v0m).round(4); t["plis > V0"] = [int((X[c] > V0.reindex(X.index)).sum()) for c in t.index]; t = t.sort_values("f1A", ascending=False); t.to_csv(out / "I6a_resume.csv"); print("V0 (I1, répétitions 0-4) =", round(v0m, 4)); print(t.to_string())
    f = S.friedman_nemenyi(X.values, list(X.columns)); rk = pd.Series(f["avg_ranks"], index=f["names"]).sort_values(); best = rk.index[0]; indisc = [c for c in rk.index if rk[c] - rk[best] < f["cd"]]   # rang 1 = meilleur
    print("\nFriedman : chi2 = %.1f, p = %.3g, différence critique = %.2f ; meilleur au rang : %s ; configurations indiscernables du meilleur (Nemenyi) : %d" % (f["chi2"], f["p"], f["cd"], best, len(indisc))); print(rk.round(2).head(10).to_string())
    pd.DataFrame({"rang moyen": rk, "indiscernable du meilleur": [c in indisc for c in rk.index]}).to_csv(out / "I6a_friedman.csv")
    top = t.index[0]; gain = float(t.loc[top, "gain f1A vs V0"]); print("\nmeilleure (moyenne f1A) :", top, "gain", gain, "| porte HF17 (>= 0,02) :", gain >= 0.02)
    mp = S.multi_paired(X[top].values, V0.reindex(X.index).values); print("tests (sélection, biaisés) :", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in mp.items()})
    (out / "I6_selected.json").write_text(json.dumps({"config": top, "gain_dev": gain, "f1A_dev": float(t.loc[top, "f1A"]), "porte_HF17": gain >= 0.02, "friedman_p": f["p"], "n_indiscernables": len(indisc)}, indent=1))
else:
    df = load("P2_I6b_confirmation"); df.to_csv(out / "I6b_all_units.csv", index=False); sel = json.load(open(out / "I6_selected.json")); c = sel["config"]; print("plis :", df[["repeat", "fold"]].drop_duplicates().shape[0], "config :", c)
    V0 = pd.read_csv(out / "I1b_all_units.csv"); V0 = V0[V0.model == "V0"].set_index(["repeat", "fold"]); X = df[df.config == c].set_index(["repeat", "fold"]); res = []
    for col in ("f1A", "f1_fam", "tree_dist"):
        sgn = -1 if col == "tree_dist" else 1; a, b = (X[col].values, V0.loc[X.index, col].values); m = S.multi_paired(sgn * a, sgn * b, shift=0.02 if col == "f1A" else 0.0); m["mesure"] = col; res.append(m)
    G = pd.DataFrame(res); G.to_csv(out / "I6b_tests.csv", index=False); print(G.round(5).to_string(index=False)); print("moyennes :", X[["f1A", "f1_fam", "tree_dist"]].mean().round(4).to_dict(), "V0 :", V0.loc[X.index, ["f1A", "f1_fam", "tree_dist"]].mean().round(4).to_dict())
