"""Vague 3 (D30, HY1-HY4) : équilibrage conscient de la présence des classes. Conditions : toutes, abs8, abs14 (classes retirées du lot de test). Dev SIEVE_00 seul.
Étape a : répétitions 0-4, toutes les variantes ; étape b : répétitions 5-9, variantes de W3_selected.json. Reprenable. Usage : python scripts/v3_phase2_W3.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, tp2_runner as R
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5
VARS = ["A1", "Q25", "Q50", "Q25b", "Q50b", "M50", "Z"]; CONDS = {"toutes": 0, "abs8": 8, "abs14": 14}


def sink(P, gamma=0.5, it=10, target=None):
    Q = P.copy(); K = Q.shape[1]; tg = np.ones(K) / K if target is None else target
    for _ in range(it): Q = Q * ((Q.shape[0] * tg) / (Q.sum(0) + 1e-12)) ** gamma; Q = Q / Q.sum(1, keepdims=True)
    return Q


def aware(P, theta, gamma):
    K = P.shape[1]; pres = P.mean(0) >= theta / K; P2 = P.copy(); P2[:, ~pres] *= 1e-3; tg = pres / pres.sum(); return sink(P2, gamma, 10, tg)


def decode(name, P):
    if name == "A1": return sink(P)
    if name == "Q25": return aware(P, 0.25, 0.5)
    if name == "Q50": return aware(P, 0.5, 0.5)
    if name == "Q25b": return aware(P, 0.25, 0.25)
    if name == "Q50b": return aware(P, 0.5, 0.25)
    if name == "M50": K = P.shape[1]; pi = P.mean(0); return sink(P, 0.5, 10, 0.5 / K + 0.5 * pi / pi.sum())
    if name == "Z":
        Q = sink(P); share = np.bincount(Q.argmax(1), minlength=P.shape[1]) / len(P); pres = share >= 0.005; P2 = P.copy(); P2[:, ~pres] *= 1e-3; return sink(P2, 0.5, 10, pres / pres.sum())


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]; te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(dev.log.values[tr]), v.transform(dev.log.values[te]); lr = LogisticRegression(C=10, max_iter=300).fit(X, ytr); P = lr.predict_proba(Xt); cl = lr.classes_; res = {}
    for cn, nab in CONDS.items():
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rng = np.random.default_rng((1000 if nab == 8 else 2000) * r + k); gone = rng.choice(np.unique(yte), size=min(nab, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        Pk, yk = P[keep], yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]
        def rec(nm, pred): res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pred, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pred, labels=L, average="macro", zero_division=0)), "n_classes_lot": int(len(L))}
        rec("LR", cl[Pk.argmax(1)])
        for nm in names: rec(nm, cl[decode(nm, Pk).argmax(1)])
    return res


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W3" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": names, "conditions": CONDS, "file": "SIEVE_00"}
    return R.run_unit(block, f"W3{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = VARS; block, code = "P2_W3a_selection", "W3a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W3_selected.json"))["variants"]; block, code = "P2_W3b_confirmation", "W3b.1"; reps = range(5, 10); folds = make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
