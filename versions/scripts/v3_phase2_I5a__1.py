"""Itération I5a : sélection de la configuration mots + lettres sur les répétitions 0 à 4 (D21). Dev SIEVE_00 seul. Reprenable. Usage : python scripts/v3_phase2_I5a.py [--smoke] [--jobs N]"""
import sys, time, pathlib, warnings, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
CW, NG, CC, WT = [0.3, 1, 3], [(2, 4), (3, 5), (4, 6)], [0.3, 1], [0.5, 1, 2]


def metrics(d, classes_, yte, fam_of, ids):
    pred = classes_[d.argmax(1)]; ft, fp = fam_of[yte], fam_of[pred]; lab = [c for c in ids if (yte == c).any()]; dist = np.where(pred == yte, 0, np.where(fp == ft, 1, 2))
    return {"f1A": float(f1_score(yte, pred, labels=lab, average="macro", zero_division=0)), "f1_fam": float(f1_score(ft, fp, labels=np.unique(ft), average="macro", zero_division=0)), "tree_dist": float(dist.mean())}


def task(r, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values; te, tr = np.where(fold == k)[0], np.where(fold != k)[0]
    ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; res = {}
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xw, Xtw = v.fit_transform(ttr), v.transform(tte); dw = {}
    for c in CW: m = LinearSVC(C=c).fit(Xw, ytr); dw[c] = m.decision_function(Xtw); res[f"mots_C{c}"] = metrics(dw[c], m.classes_, yte, fam_of, ids)
    cls = m.classes_
    for ng in NG:
        ch = TfidfVectorizer(analyzer="char_wb", ngram_range=ng, sublinear_tf=True, min_df=3, max_features=100000); Xc, Xtc = ch.fit_transform(ttr), ch.transform(tte)
        for c2 in CC:
            dc = LinearSVC(C=c2).fit(Xc, ytr).decision_function(Xtc); res[f"lettres_{ng[0]}{ng[1]}_C{c2}"] = metrics(dc, cls, yte, fam_of, ids)
            for c, w in itertools.product(CW, WT): res[f"somme_mC{c}_l{ng[0]}{ng[1]}C{c2}_w{w}"] = metrics(dw[c] + w * dc, cls, yte, fam_of, ids)
    return res


def unit(r, k, dev, tierA):
    cfg = {"phase": 2, "iteration": "I5a", "repeat": r, "fold": k, "cap": A.CAP, "grid": {"CW": CW, "NG": NG, "CC": CC, "WT": WT}, "file": "SIEVE_00"}
    return R.run_unit("P2_I5a_selection", f"I5a r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA), code_version="I5a.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0)] if "--smoke" in sys.argv else [(r, k) for r in range(5) for k in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
