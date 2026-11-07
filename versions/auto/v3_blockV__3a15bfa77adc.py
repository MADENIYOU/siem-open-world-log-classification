"""Bloc V (protocole v3) : vectorisation × bruit. Trois vectorisations (TF-IDF mots, TF-IDF caractères 3 à 5, Skip-gram pondéré IDF) × six fichiers SIEVE (p = 0 à 0,5, entraînement et test dans le même fichier)
× 5 rotations × 2 répétitions × 5 plis de groupes = 300 unités ; développement seul (le test v2 n'est jamais lu), 400 logs au plus par gabarit et par fichier.
Dans chaque unité, MÊMES logs pour : macro-F1 des classes connues et AUROC de détection d'inconnus (MSP, énergie, MSP de la famille). Reprenable. Usage : python scripts/v3_blockV.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from scipy.special import logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, accuracy_score
import v3_blockA as A, v3_blockB as B, v3_blockC as C, tp2_openset as O, tp2_runner as R, tp2_data as D
from tp2_vec import DocEmbedder
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
VECS = ["word", "char", "sg_idf"]; NREP = 2


def load_all():
    VER = D.load_versions(ROOT); sp = D.load_splits_v1(ROOT); G = pd.read_csv(ROOT / "artifacts" / "data" / "groups_v3.csv"); out = {}
    for v in range(6):
        df = VER[v].merge(sp[sp.version == v][["row", "group"]], on="row").merge(G, on="group", suffixes=("", "_g")); assert (df.category == df.category_g).all()
        out[v] = df[df.role == "dev"].sample(frac=1, random_state=0).groupby("group").head(A.CAP).sort_values(["group", "row"]).reset_index(drop=True)
    big = G.groupby("category").size(); return out, sorted(big[big >= 5].index)


def features(vec, tr_txt, te_txt, seed):
    if vec == "word":
        t = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); return t.fit_transform(tr_txt), t.transform(te_txt)
    if vec == "char":
        t = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); return t.fit_transform(tr_txt), t.transform(te_txt)
    e = DocEmbedder(kind="w2v_sg", weighting="idf", workers=2, seed=seed).fit(tr_txt); a, b = e.transform(tr_txt), e.transform(te_txt); sc = StandardScaler().fit(a); return sc.transform(a), sc.transform(b)


def task(v, rot, r, k, devs, tierA):
    dev = devs[v]; ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    tierA_ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values
    te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": f"connus {int(known.sum())}, inconnus {int((~known).sum())}"}
    res = {}
    for vec in VECS:
        t0 = time.time(); Xtr, Xte = features(vec, dev.log.values[tr_i], dev.log.values[te_i], r); lr = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xtr, ytr)
        L = lr.decision_function(Xte); P = lr.predict_proba(Xte); pred = lr.predict(Xte); _, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C.C_HEAD)
        lab = [c for c in tierA_ids if (yte[known] == c).any() and c in lr.classes_]
        sc = {"msp": P.max(1), "energy": logsumexp(L, axis=1), "fam_msp": pf.max(1)}; op = {n: O.open_metrics(np.nan_to_num(s), known) for n, s in sc.items()}
        res[vec] = {"f1A": float(f1_score(yte[known], pred[known], labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte[known], pred[known], labels=np.unique(yte[known]), average="macro", zero_division=0)), "acc": float(accuracy_score(yte[known], pred[known])),
                    "open": {n: {"auroc": m["auroc"], "fpr95": m["fpr95"]} for n, m in op.items()}, "seconds": round(time.time() - t0, 1)}
    res["_info"] = {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "n_train": int(len(tr_i)), "masked": sorted(masked)}
    return res


def unit(v, rot, r, k, devs, tierA):
    cfg = {"block": "V", "file": v, "rotation": rot, "repeat": r, "fold": k, "cap": A.CAP, "C_head": C.C_HEAD, "vecs": VECS, "splits": "groups_v3"}
    return R.run_unit("V_vectorisation_bruit", f"V p{v} rot{rot + 1} r{r} pli{k}", cfg, lambda: task(v, rot, r, k, devs, tierA), code_version="V1")[1]


if __name__ == "__main__":
    devs, tierA = load_all(); print({v: len(d) for v, d in devs.items()}, flush=True)
    jobs = [(0, 0, 0, 0)] if "--smoke" in sys.argv else [(v, rot, r, k) for r in range(NREP) for k in range(5) for rot in range(5) for v in range(6)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(v, rot, r, k, devs, tierA) for v, rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
