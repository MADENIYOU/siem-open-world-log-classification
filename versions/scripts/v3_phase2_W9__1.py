"""Vague 9 (D40, HK1-HK6) : composition de leviers. Score s = wc·Lc + wo·Lo + wa·La + wf·Lf (LR mots, têtes objet et action, famille par lettres), plan factoriel A × B × T × alpha (108 configurations) et composition apprise STK (poids estimés hors-gabarit).
PIPE = LR_B0_T1_a0.5. 30 classes, dev SIEVE_00 seul, conditions toutes et abs8. Étape a : répétitions 0-4 ; étape b : répétitions 10-19, configurations de W9_selected.json (+ PIPE). Reprenable. Usage : python scripts/v3_phase2_W9.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize
from scipy.special import softmax, logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R, v3_phase2_W3c as W3c, v3_phase2_W8 as W8
from v3_phase2_W4 import AX
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5
AS = {"LR": (1.0, 0.0, 0.0), "AXE05": (0.5, 1.0, 1.0), "AXE1": (1.0, 1.0, 1.0)}; BS, TS, ALS = (0, 0.5, 1, 2), (0.5, 1, 2), (0.25, 0.5, 0.75)
GRID = [f"{a}_B{b}_T{t}_a{al}" for a, b, t, al in itertools.product(AS, BS, TS, ALS)]; PIPE = "LR_B0_T1_a0.5"; FLOOR = 1e-9


def fp(P, cl, n):
    out = np.full((P.shape[0], n), FLOOR); out[:, cl] = P; return out


def comps(Xw, Xc, ytr, idx, Xw_e, Xc_e, obj_of, act_of, fam_of, K, nobj, nact, nfam):
    """Quatre composantes de log-score (n_eval x K) à partir des lignes idx de l'apprentissage."""
    lr = LogisticRegression(C=10, max_iter=300).fit(Xw[idx], ytr[idx]); Lc = np.log(fp(lr.predict_proba(Xw_e), lr.classes_, K))
    po = LogisticRegression(C=10, max_iter=300).fit(Xw[idx], obj_of[ytr[idx]]); Lo = np.log(fp(po.predict_proba(Xw_e), po.classes_, nobj))[:, obj_of]
    pa = LogisticRegression(C=10, max_iter=300).fit(Xw[idx], act_of[ytr[idx]]); La = np.log(fp(pa.predict_proba(Xw_e), pa.classes_, nact))[:, act_of]
    lf = LogisticRegression(C=10, max_iter=300).fit(Xc[idx], fam_of[ytr[idx]]); Lf = np.log(fp(lf.predict_proba(Xc_e), lf.classes_, nfam))[:, fam_of]
    return Lc, Lo, La, Lf


def score_probs(Ls, w):
    s = sum(wi * L for wi, L in zip(w, Ls) if wi != 0); return softmax(s, axis=1)


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes])
    objs = sorted({AX[c][0] for c in classes}); acts = sorted({AX[c][1] for c in classes}); obj_of = np.array([objs.index(AX[c][0]) for c in classes]); act_of = np.array([acts.index(AX[c][1]) for c in classes])
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; gl, gi = np.unique(dev.group.values[tr], return_inverse=True)
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte); ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc, Xct = ch.fit_transform(ttr), ch.transform(tte)
    dims = (obj_of, act_of, fam_of, K, len(objs), len(acts), len(B.FAMS)); allidx = np.arange(len(tr)); Ls = comps(X, Xc, ytr, allidx, Xt, Xct, *dims); need = set(names) | {PIPE}; info = {}; stk_w = None
    if "STK" in need:
        rng = np.random.default_rng(100 * r + 10 * k + 3); fg = rng.integers(0, 3, len(gl))[gi]; oof = [np.zeros((len(tr), K)) for _ in range(4)]
        for f in range(3):
            ev = np.where(fg == f)[0]; trn = np.where(fg != f)[0]; cs = comps(X, Xc, ytr, trn, X[ev], Xc[ev], *dims)
            for o, c in zip(oof, cs): o[ev] = c
        ok = oof[0][np.arange(len(tr)), ytr] > -15; Z = [o[ok] for o in oof]; yt = ytr[ok]
        def nll(w): s = sum(wi * z for wi, z in zip(w, Z)); return float(-(s[np.arange(len(yt)), yt] - logsumexp(s, axis=1)).mean())
        sol = minimize(nll, x0=np.array([1.0, 0.0, 0.0, 0.0]), method="L-BFGS-B", bounds=[(0, 5)] * 4); stk_w = sol.x; info = {"stk_weights": [round(float(x), 3) for x in stk_w], "stk_oof_nll": round(float(sol.fun), 4), "stk_n": int(ok.sum())}
    res = {}
    for cn, nab in (("toutes", 0), ("abs8", 8)):
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng(1000 * r + k); gone = rg.choice(np.unique(yte), size=min(8, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]; Lk = [l[keep] for l in Ls]
        def rec(nm, Q): pr = Q.argmax(1); res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pr, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pr, labels=L, average="macro", zero_division=0))}
        cache = {}
        for nm in need:
            if nm == "STK": rec(nm, W8.decode_mix(score_probs(Lk, stk_w), 0.5, 1.0)); continue
            an, bn, tn, aln = nm.split("_"); wc, wo, wa = AS[an]; wf = float(bn[1:]); key = (an, wf)
            if key not in cache: cache[key] = score_probs(Lk, (wc, wo, wa, wf))
            rec(nm, W8.decode_mix(cache[key], float(aln[1:]), float(tn[1:])))
    res["_info"] = info; return res


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W9" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": sorted(names), "file": "SIEVE_00"}
    return R.run_unit(block, f"W9{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = GRID + ["STK"]; block, code = "P2_W9a_selection", "W9a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W9_selected.json"))["variants"]; block, code = "P2_W9b_confirmation", "W9b.1"; reps = range(10, 20); folds = W3c.make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
