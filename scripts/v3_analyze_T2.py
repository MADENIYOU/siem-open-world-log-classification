"""Analyse de la réplication T2 (D22) : HT1b, HT2b, HF15, HF16 avec plusieurs tests. Unité = couple (découpe, rotation) : 20. N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; rows = []
for rec in R.load_block("T2_replication"):
    c, r = rec["cfg"], rec["result"]
    if "skipped" in r: continue
    row = {"split": f"r{c['split_repeat']}k{c['split_fold']}", "rot": c["rotation"], "f1A_T": r["transformer"]["closed"]["f1A"], "f1A_B": r["tfidf_memes_logs"]["closed"]["f1A"], "f1A_F": r["fusion"]["closed"]["f1A"], "maha": r["transformer"]["open"]["maha_shared"]["auroc"], "msp_T": r["transformer"]["open"]["msp"]["auroc"],
           "fam_T": r["transformer"]["open"]["fam_msp"]["auroc"], "fam_B": r["tfidf_memes_logs"]["open"]["fam_msp"]["auroc"], "fam_F": r["fusion"]["open"]["fam_msp"]["auroc"], "msp_B": r["tfidf_memes_logs"]["open"]["msp"]["auroc"], "msp_F": r["fusion"]["open"]["msp"]["auroc"]}
    rows.append(row)
df = pd.DataFrame(rows); df.to_csv(out / "T2_all_units.csv", index=False); print("couples :", len(df)); print(df[[c for c in df.columns if c not in ("split", "rot")]].mean().round(4).to_string())
def show(name, a, b, shift=0.0):
    m = S.multi_paired(a, b, shift=shift); print(f"\n{name} (seuil {shift}) :", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in m.items()}); m["test"] = name; m["seuil"] = shift; return m
res = [show("HT1b : F1A Transformer - TF-IDF", df.f1A_T.values, df.f1A_B.values, 0.02), show("HT2b : AUROC Mahalanobis - MSP (Transformer)", df.maha.values, df.msp_T.values, 0.03),
       show("HF15 : F1A fusion - Transformer", df.f1A_F.values, df.f1A_T.values, 0.01), show("HF15 : F1A fusion - TF-IDF", df.f1A_F.values, df.f1A_B.values, 0.01),
       show("HF16 : AUROC famille fusion - Transformer", df.fam_F.values, df.fam_T.values, 0.01), show("HF16 : AUROC famille fusion - TF-IDF", df.fam_F.values, df.fam_B.values, 0.01),
       show("exploratoire : AUROC famille Transformer - TF-IDF", df.fam_T.values, df.fam_B.values, 0.0), show("exploratoire : AUROC MSP Transformer - TF-IDF", df.msp_T.values, df.msp_B.values, 0.0)]
pd.DataFrame(res).to_csv(out / "T2_tests.csv", index=False)
