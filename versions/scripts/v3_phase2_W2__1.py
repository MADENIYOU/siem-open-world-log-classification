"""Vague 2 (D29, HX1-HX7) : affiner et éprouver A1 (décodage à masses équilibrées). Dev SIEVE_00 seul. Étape a : répétitions 0-4 ; étape b : confirmation répétitions 5-9 des variantes de W2_selected.json (et de la référence A1). Reprenable. Usage : python scripts/v3_phase2_W2.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, re
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.special import softmax
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5
VARS = ["S1", "S2", "G25", "G1", "I30", "P5", "H1", "F9S", "A1_abs", "LR_abs"]


def sink(P, gamma=0.5, it=10, target=None):
    Q = P.copy(); K = Q.shape[1]; tg = np.ones(K) / K if target is None else target
    for _ in range(it): Q = Q * ((Q.shape[0] * tg) / (Q.sum(0) + 1e-12)) ** gamma; Q = Q / Q.sum(1, keepdims=True)
    return Q


def task(r, k, dev, tierA, fold, names, small_cls):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]; sm = [classes.index(c) for c in small_cls]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]
    gl, gi = np.unique(dev.group.values[tr], return_inverse=True); res = {}
    def rec(name, pred, mask=None):
        yy = yte if mask is None else yte[mask]; pp = pred if mask is None else pred[mask]; L = np.unique(yy); a = [c for c in ids if c in L]; s = [c for c in sm if c in L]
        res[name] = {"f1A": float(f1_score(yy, pp, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yy, pp, labels=L, average="macro", zero_division=0)), "f1_small": float(f1_score(yy, pp, labels=s, average="macro", zero_division=0)) if s else float("nan")}
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte)
    lr = LogisticRegression(C=10, max_iter=300).fit(X, ytr); P = lr.predict_proba(Xt); cl = lr.classes_; rec("REF_LR", cl[P.argmax(1)]); rec("A1", cl[sink(P).argmax(1)])
    m0 = LinearSVC(C=1).fit(X, ytr); D0 = m0.decision_function(Xt); assert (m0.classes_ == cl).all()
    for nm, tau in (("S1", 5), ("S2", 10)):
        if nm in names: rec(nm, cl[sink(softmax(tau * D0, axis=1)).argmax(1)])
    for nm, g, it in (("G25", 0.25, 10), ("G1", 1.0, 10), ("I30", 0.5, 30)):
        if nm in names: rec(nm, cl[sink(P, g, it).argmax(1)])
    if "P5" in names:
        nt = np.array([len(set(gl[gi[ytr == c]])) for c in cl], float) ** 0.5; rec("P5", cl[sink(P, target=nt / nt.sum()).argmax(1)])
    if "H1" in names:
        Fm = np.zeros((len(cl), len(B.FAMS))); Fm[np.arange(len(cl)), fam_of[cl]] = 1; Pf = P @ Fm; Pf2 = sink(Pf[:, Fm.sum(0) > 0]); scale = np.ones(len(B.FAMS)); present = Fm.sum(0) > 0; scale[present] = (Pf2.sum(0) / (Pf[:, present].sum(0) + 1e-12)); Pc = P * (Fm @ scale); Pc = Pc / Pc.sum(1, keepdims=True); rec("H1", cl[sink(Pc).argmax(1)])
    if "F9S" in names:
        ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); lf = LogisticRegression(C=10, max_iter=300).fit(ch.fit_transform(ttr), fam_of[ytr]); pf = lf.predict_proba(ch.transform(tte)); logp = np.full((len(tte), len(B.FAMS)), np.log(1e-6)); logp[:, lf.classes_] = np.log(pf + 1e-9)
        rec("F9S", cl[sink(softmax(5 * (D0 + 0.5 * logp[:, fam_of[cl]]), axis=1)).argmax(1)])
    if "A1_abs" in names or "LR_abs" in names:
        rng = np.random.default_rng(1000 * r + k); gone = rng.choice(np.unique(yte), size=min(8, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        Pk = P[keep]; yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]; s = [c for c in sm if c in L]
        for nm, pred in (("LR_abs", cl[Pk.argmax(1)]), ("A1_abs", cl[sink(Pk).argmax(1)])):
            res[nm] = {"f1A": float(f1_score(yk, pred, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pred, labels=L, average="macro", zero_division=0)), "f1_small": float(f1_score(yk, pred, labels=s, average="macro", zero_division=0)) if s else float("nan")}
    return res


def unit(r, k, dev, tierA, fold, names, small, block, code):
    cfg = {"phase": 2, "iteration": "W2" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": names, "file": "SIEVE_00"}
    return R.run_unit(block, f"W2{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names, small), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); ng = dev.groupby("category").group.nunique(); small = sorted(ng[ng <= 3].index); t0 = time.time()
    if STAGE == "a": names = VARS; block, code = "P2_W2a_selection", "W2a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W2_selected.json"))["variants"] + ["A1_abs", "LR_abs"]; block, code = "P2_W2b_confirmation", "W2b.1"; reps = range(5, 10); folds = make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, small, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
