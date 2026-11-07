"""Construit le découpage v3 (développement + test scellé v2). Usage : .venv312/bin/python scripts/v3_make_split.py
Écrit artifacts/data/groups_v3.csv (une ligne par gabarit : rôle, plis) et splits_v3_meta.json. Reprenable : ne refait rien si les fichiers existent (--force pour refaire)."""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import tp2_data as D, tp2_split_v3 as S
out = ROOT / "artifacts" / "data"; gf, mf = out / "groups_v3.csv", out / "splits_v3_meta.json"
if gf.exists() and mf.exists() and "--force" not in sys.argv:
    print("déjà fait :", gf.name, "(--force pour refaire)"); print(json.dumps(json.loads(mf.read_text()), indent=1, ensure_ascii=False)); sys.exit(0)
V = D.load_versions(ROOT); sp = D.load_splits_v1(ROOT); gt = D.group_table(sp)
g, meta = S.build_v3(ROOT, V, sp, gt)
g.to_csv(gf, index=False); mf.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
print(g.groupby("role").agg(gabarits=("group", "size"), logs=("n_logs", "sum")))
print("classes de 5 gabarits ou plus, gabarits de test v2 :"); big = g.groupby("category").size(); big = big[big >= 5].index
print(g[g.category.isin(big) & (g.role == "test2")].groupby("category").size().to_string())
print(json.dumps(meta, indent=1, ensure_ascii=False))
(ROOT / "artifacts" / "results" / "v3" / "test_v2_access_log.json").write_text("[]")
