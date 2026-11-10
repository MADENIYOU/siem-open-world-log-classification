"""Vague 10 (D41, HK7-HK10) : degrés étendus (AXE05 : T, alpha ; bases AXE025/AXE075), variantes STK_T{t}_a{alpha}, puis réplication finale sur répétitions 20-39 (conditions toutes, abs8, abs14).
Étape a : sélection, répétitions 0-4 ; étape c : réplication finale, candidats de artifacts/results/v3/W10_selected.json (+ PIPE). Reprenable. Usage : python scripts/v3_phase2_W10.py a|c [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, itertools
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize
from scipy.special import logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R, v3_phase2_W3d as W3d, v3_phase2_W8 as W8, v3_phase2_W9 as W9
from v3_phase2_W4 import AX
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5; PIPE = W9.PIPE; AS = dict(W9.AS, AXE025=(0.25, 1.0, 1.0), AXE075=(0.75, 1.0, 1.0))
E1 = [f"AXE05_B1_T{t}_a{al}" for t, al in itertools.product((2, 3, 4), (0.1, 0.25, 0.4))] + ["AXE025_B1_T2_a0.25", "AXE075_B1_T2_a0.25"]; E2 = [f"STK_T{t}_a{al}" for t, al in itertools.product((1, 2, 3), (0.1, 0.25, 0.5))]; REFS = [PIPE, "AXE05_B1_T2_a0.25", "STK_T1_a0.5"]
CONDS = {"a": (("toutes", 0), ("abs8", 8)), "c": (("toutes", 0), ("abs8", 8), ("abs14", 14))}


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes])
    objs = sorted({AX[c][0] for c in classes}); acts = sorted({AX[c][1] for c in classes}); obj_of = np.array([objs.index(AX[c][0]) for c in classes]); act_of = np.array([acts.index(AX[c][1]) for c in classes])
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; gl, gi = np.unique(dev.group.values[tr], return_inverse=True)
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte); ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc, Xct = ch.fit_transform(ttr), ch.transform(tte)
    dims = (obj_of, act_of, fam_of, K, len(objs), len(acts), len(B.FAMS)); Ls = W9.comps(X, Xc, ytr, np.arange(len(tr)), Xt, Xct, *dims); need = set(names) | {PIPE}; stk_w = None; info = {}
    if any(n.startswith("STK") for n in need):
        rng = np.random.default_rng(100 * r + 10 * k + 3); fg = rng.integers(0, 3, len(gl))[gi]; oof = [np.zeros((len(tr), K)) for _ in range(4)]
        for f in range(3):
            ev = np.where(fg == f)[0]; trn = np.where(fg != f)[0]; cs = W9.comps(X, Xc, ytr, trn, X[ev], Xc[ev], *dims)
            for o, c in zip(oof, cs): o[ev] = c
        ok = oof[0][np.arange(len(tr)), ytr] > -15; Z = [o[ok] for o in oof]; yt = ytr[ok]
        def nll(w): s = sum(wi * z for wi, z in zip(w, Z)); return float(-(s[np.arange(len(yt)), yt] - logsumexp(s, axis=1)).mean())
        sol = minimize(nll, x0=np.array([1.0, 0.0, 0.0, 0.0]), method="L-BFGS-B", bounds=[(0, 5)] * 4); stk_w = sol.x; info = {"stk_weights": [round(float(x), 3) for x in stk_w], "stk_oof_nll": round(float(sol.fun), 4)}
    res = {}
    for cn, nab in CONDS[STAGE]:
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng((1000 if nab == 8 else 2000) * r + k); gone = rg.choice(np.unique(yte), size=min(nab, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]; Lk = [l[keep] for l in Ls]
        def rec(nm, Q): pr = Q.argmax(1); res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pr, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pr, labels=L, average="macro", zero_division=0))}
        cache = {}
        for nm in need:
            p = nm.split("_")
            if p[0] == "STK": t = float(p[1][1:]); al = float(p[2][1:]); rec(nm, W8.decode_mix(W9.score_probs(Lk, stk_w), al, t)); continue
            wc, wo, wa = AS[p[0]]; wf = float(p[1][1:]); key = (p[0], wf)
            if key not in cache: cache[key] = W9.score_probs(Lk, (wc, wo, wa, wf))
            rec(nm, W8.decode_mix(cache[key], float(p[3][1:]), float(p[2][1:])))
    res["_info"] = info; return res


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W10" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": sorted(names), "conditions": [c for c, _ in CONDS[STAGE]], "file": "SIEVE_00"}
    return R.run_unit(block, f"W10{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = E1 + E2 + REFS; block, code = "P2_W10a_selection", "W10a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W10_selected.json"))["candidates"]; block, code = "P2_W10c_final", "W10c.1"; reps = range(20, 40); folds = W3d.make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
