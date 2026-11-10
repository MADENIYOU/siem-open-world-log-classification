"""Analyse de la vague 7 (D37, HL1, HM1) : LP-FT et LP-FT depuis un DistilBERT adapté (MLM) contre l'affinage complet de T2 et contre TF-IDF sur les mêmes couples (découpe, rotation). N'écrit pas le journal."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import tp2_runner as R, tp2_stats as S
out = ROOT / "artifacts" / "results" / "v3"; t2 = {}
for rec in R.load_block("T2_replication"):
    c, r = rec["cfg"], rec["result"]
    if "skipped" in r: continue
    t2[(c["split_repeat"], c["split_fold"], c["rotation"])] = (r["transformer"]["closed"]["f1A"], r["tfidf_memes_logs"]["closed"]["f1A"])
rows = []
for rec in R.load_block("W7_lpft"):
    c, r = rec["cfg"], rec["result"]; key = (c["split_repeat"], c["split_fold"], c["rotation"])
    if "skipped" in r or key not in t2: continue
    rows.append({"split": f"r{key[0]}k{key[1]}", "rot": key[2], "full_ft": t2[key][0], "tfidf": t2[key][1], "lpft": r["lpft"]["f1A"], "lpft_adapt": r["lpft_adapt"]["f1A"], "mlm_min": r["lpft_adapt"]["mlm_minutes"], "mlm_loss_first": r["lpft_adapt"]["loss_first"], "mlm_loss_last": r["lpft_adapt"]["loss_last"]})
df = pd.DataFrame(rows); df.to_csv(out / "W7_all_units.csv", index=False); print("couples :", len(df)); print(df[["full_ft", "tfidf", "lpft", "lpft_adapt"]].mean().round(4).to_string()); res = []
if len(df) >= 3:
    for name, a, b, sh in (("HL1 : LP-FT - affinage complet (seuil 0,02)", "lpft", "full_ft", 0.02), ("HM1 : LP-FT adapté - LP-FT (seuil 0,02)", "lpft_adapt", "lpft", 0.02), ("exploratoire : LP-FT - TF-IDF", "lpft", "tfidf", 0.0), ("exploratoire : LP-FT adapté - TF-IDF", "lpft_adapt", "tfidf", 0.0), ("exploratoire : LP-FT adapté - affinage complet", "lpft_adapt", "full_ft", 0.0)):
        m = S.multi_paired(df[a].values, df[b].values, shift=sh); m["test"] = name; res.append(m)
    G = pd.DataFrame(res); G.to_csv(out / "W7_tests.csv", index=False); print(G.round(4).to_string(index=False))
