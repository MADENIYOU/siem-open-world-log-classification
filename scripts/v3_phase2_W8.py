"""Vague 8 (D38, HQ1-HQ5) : réglage conscient du décodage (C, T, alpha), mots + lettres avant décodage (ENSP30, ENSP50), auto-apprentissage sur le lot décodé (ST1, ST2). PIPE = (C 10, T 1, alpha 0,5). 30 classes, dev SIEVE_00 seul, conditions toutes et abs8.
Étape a : répétitions 0-4 (toutes les variantes) ; étape b : répétitions 10-19, variantes de W8_selected.json (+ PIPE). Reprenable. Usage : python scripts/v3_phase2_W8.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, scipy.sparse as sp
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, tp2_runner as R, v3_phase2_W3 as W3, v3_phase2_W3c as W3c
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6
CS, TS, ALS = (3, 10, 30, 100), (0.5, 1, 2), (0.25, 0.5, 0.75); GRID = [f"G_C{c}_T{t}_a{a}" for c, t, a in itertools.product(CS, TS, ALS)]; PIPE = "G_C10_T1_a0.5"; OTHERS = ["ENSP30", "ENSP50", "ST1", "ST2"]


def decode_mix(P, alpha, T=1.0):
    P = P ** (1.0 / T); P = P / P.sum(1, keepdims=True); K = P.shape[1]; pi = P.mean(0); pi = pi / pi.sum(); return W3.sink(P, 0.5, 10, (1 - alpha) / K + alpha * pi)


def full(P, cl, K):
    out = np.full((P.shape[0], K), 1e-9); out[:, cl] = P; return out / out.sum(1, keepdims=True)


def selftrain(X, ytr, Xl, P0, K, rounds):
    Q = decode_mix(P0, 0.5); outs = []
    for _ in range(rounds):
        yp = Q.argmax(1); conf = Q.max(1); sel = np.zeros(len(yp), bool)
        for c in np.unique(yp):
            ii = np.where(yp == c)[0]
            if len(ii) >= 3: sel[ii[conf[ii] >= np.quantile(conf[ii], 2 / 3)]] = True
        lr = LogisticRegression(C=10, max_iter=300).fit(sp.vstack([X, Xl[sel]]).tocsr(), np.r_[ytr, yp[sel]], sample_weight=np.r_[np.ones(len(ytr)), 0.5 * np.ones(sel.sum())]); Q = decode_mix(full(lr.predict_proba(Xl), lr.classes_, K), 0.5); outs.append(Q)
    return outs


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(dev.log.values[tr]), v.transform(dev.log.values[te]); need = set(names)
    Cs = sorted({int(n.split("_")[1][1:]) for n in need if n.startswith("G_")} | ({10} if need & set(OTHERS) | {PIPE} else set())); PC = {}
    for c in Cs: lr = LogisticRegression(C=c, max_iter=300).fit(X, ytr); PC[c] = full(lr.predict_proba(Xt), lr.classes_, K)
    Pc = None
    if need & {"ENSP30", "ENSP50"}:
        ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); lc = LogisticRegression(C=10, max_iter=300).fit(ch.fit_transform(dev.log.values[tr]), ytr); Pc = full(lc.predict_proba(ch.transform(dev.log.values[te])), lc.classes_, K)
    res = {}
    for cn, nab in (("toutes", 0), ("abs8", 8)):
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng(1000 * r + k); gone = rg.choice(np.unique(yte), size=min(8, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]
        def rec(nm, Q): pr = Q.argmax(1); res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pr, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pr, labels=L, average="macro", zero_division=0))}
        for nm in need:
            if nm.startswith("G_"): _, c, t, al = nm.split("_"); rec(nm, decode_mix(PC[int(c[1:])][keep], float(al[1:]), float(t[1:])))
        if PIPE not in need: rec(PIPE, decode_mix(PC[10][keep], 0.5, 1.0))
        if "ENSP30" in need: g = PC[10][keep] ** 0.7 * Pc[keep] ** 0.3; rec("ENSP30", decode_mix(g / g.sum(1, keepdims=True), 0.5))
        if "ENSP50" in need: g = PC[10][keep] ** 0.5 * Pc[keep] ** 0.5; rec("ENSP50", decode_mix(g / g.sum(1, keepdims=True), 0.5))
        if need & {"ST1", "ST2"}:
            outs = selftrain(X, ytr, Xt[keep], PC[10][keep], K, 2 if "ST2" in need else 1)
            if "ST1" in need: rec("ST1", outs[0])
            if "ST2" in need: rec("ST2", outs[1])
    return res


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W8" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": sorted(names), "file": "SIEVE_00"}
    return R.run_unit(block, f"W8{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = GRID + OTHERS; block, code = "P2_W8a_selection", "W8a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W8_selected.json"))["variants"]; block, code = "P2_W8b_confirmation", "W8b.1"; reps = range(10, 20); folds = W3c.make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
