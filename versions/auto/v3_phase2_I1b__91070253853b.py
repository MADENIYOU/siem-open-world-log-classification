"""Phase 2, I1b : confirmation du constat exploratoire d'I1 (ENS contre V0) sur 25 NOUVEAUX plis (répétitions 5 à 9). Dev seul. Reprenable. Usage : python scripts/v3_phase2_I1b.py [--jobs N]"""
import sys, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import f1_score, accuracy_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
REPS = range(5, 10)


def make_folds(dev):
    g = dev.groupby("group").agg(category=("category", "first")).reset_index(); out = {}
    for r in REPS:
        f = np.full(len(g), -1)
        for k, (_, te) in enumerate(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=r).split(g, g.category, g.group)): f[te] = k
        out[r] = dict(zip(g.group, f))
    return out


def task(r, k, dev, tierA, folds):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev.group.map(folds[r]).values; te, tr = np.where(fold == k)[0], np.where(fold != k)[0]
    ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); m = LinearSVC(C=1).fit(v.fit_transform(ttr), ytr); d0 = m.decision_function(v.transform(tte))
    ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); mc = LinearSVC(C=1).fit(ch.fit_transform(ttr), ytr); dc = mc.decision_function(ch.transform(tte)); res = {}
    for name, d in (("V0", d0), ("ENS", d0 + dc)):
        pred = m.classes_[d.argmax(1)]; ft, fp = fam_of[yte], fam_of[pred]; lab = [c for c in ids if (yte == c).any()]; dist = np.where(pred == yte, 0, np.where(fp == ft, 1, 2))
        res[name] = {"f1A": float(f1_score(yte, pred, labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte, pred, labels=np.unique(yte), average="macro", zero_division=0)), "acc": float(accuracy_score(yte, pred)),
                     "f1_fam": float(f1_score(ft, fp, labels=np.unique(ft), average="macro", zero_division=0)), "tree_dist": float(dist.mean())}
    return res


def unit(r, k, dev, tierA, folds):
    cfg = {"phase": 2, "iteration": "I1b", "repeat": r, "fold": k, "cap": A.CAP, "variants": ["V0", "ENS"], "file": "SIEVE_00", "folds": "StratifiedGroupKFold graine = répétition (5 à 9)"}
    return R.run_unit("P2_I1b_confirmation", f"I1b r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, folds), code_version="I1b.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); folds = make_folds(dev); t0 = time.time()
    out = Parallel(n_jobs=JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, folds) for r in REPS for k in range(5))
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
