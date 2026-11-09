"""Itération I6 (D23) : nouveaux hyperparamètres pour représentation (I1), structure (I2) et modèle (I5). Étape a : sélection sur répétitions 0-4 (32 configurations). Étape b : confirmation de la configuration retenue (artifacts/results/v3/I6_selected.json) sur répétitions 5-9.
Dev SIEVE_00 seul, 400 logs/gabarit. Reprenable. Usage : python scripts/v3_phase2_I6.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, re
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R, tp2_fields as F
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
WORD = re.compile(r"[A-Za-z]{2,}")
def an_w6(t): return WORD.findall(t.lower()) + [x for x in F.typed_tokens(t) if x.startswith(("prog_", "champ_"))]
VEC = {"W1": lambda: TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=1), "W2": lambda: TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", ngram_range=(1, 2), lowercase=True, sublinear_tf=True, min_df=2),
       "W3": lambda: TfidfVectorizer(token_pattern=r"(?u)\b\w\w+\b", lowercase=True, sublinear_tf=True, min_df=2), "W4": lambda: TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, binary=True, min_df=2),
       "W5": lambda: TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=False, sublinear_tf=True, min_df=2), "W6": lambda: TfidfVectorizer(analyzer=an_w6, sublinear_tf=True, min_df=2),
       "L13": lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 3), sublinear_tf=True, min_df=3, max_features=100000), "L35": lambda: TfidfVectorizer(analyzer="char", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=150000)}
MOD = {"svm0.1": lambda: LinearSVC(C=0.1), "svm10": lambda: LinearSVC(C=10), "svmbal": lambda: LinearSVC(C=1, class_weight="balanced"), "lr30": lambda: LogisticRegression(C=30, max_iter=300), "ridge1": lambda: RidgeClassifier(alpha=1.0)}
CONFIGS = [(w, m) for w in ("W1", "W2", "W3", "W4", "W5", "W6") for m in MOD] + [("L13", "svm10"), ("L35", "svm10")]; cname = lambda c: f"{c[0]}_{c[1]}"


def task(r, k, dev, tierA, fold, cfgs):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; res = {}; cache = {}
    for w, m in cfgs:
        if w not in cache: v = VEC[w](); cache[w] = (v.fit_transform(ttr), v.transform(tte))
        X, Xt = cache[w]; mod = MOD[m]().fit(X, ytr); d = mod.decision_function(Xt); pred = mod.classes_[d.argmax(1)]; ft, fp = fam_of[yte], fam_of[pred]; lab = [c for c in ids if (yte == c).any()]; dist = np.where(pred == yte, 0, np.where(fp == ft, 1, 2))
        res[f"{w}_{m}"] = {"f1A": float(f1_score(yte, pred, labels=lab, average="macro", zero_division=0)), "f1_fam": float(f1_score(ft, fp, labels=np.unique(ft), average="macro", zero_division=0)), "tree_dist": float(dist.mean())}
    return res


def unit(r, k, dev, tierA, fold, cfgs, block, code):
    cfg = {"phase": 2, "iteration": "I6" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "configs": [cname(c) for c in cfgs], "file": "SIEVE_00"}
    return R.run_unit(block, f"I6{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, cfgs), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a":
        jobs = [(0, 0)] if "--smoke" in sys.argv else [(r, k) for r in range(5) for k in range(5)]; cfgs = CONFIGS; block, code = "P2_I6a_selection", "I6a.1"; fold_of = lambda r: dev[f"fold_r{r}"].values
    else:
        sel = json.load(open(ROOT / "artifacts" / "results" / "v3" / "I6_selected.json")); cfgs = [tuple(sel["config"].split("_"))]; folds = make_folds(dev); block, code = "P2_I6b_confirmation", "I6b.1"
        jobs = [(5, 0)] if "--smoke" in sys.argv else [(r, k) for r in range(5, 10) for k in range(5)]; fold_of = lambda r: dev.group.map(folds[r]).values
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), cfgs, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
