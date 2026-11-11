"""Vague 12 (D44, HN1-HN3) : poids de la composition appris sur la macro-F1 décodée hors-gabarit (F4, F4s, F9, F9s). Réutilise les têtes de v3_phase2_W11. Conditions toutes, abs8, abs14. Dev seul.
Étape a : répétitions 0-4 ; étape c : répétitions 40-49, variante de W12_selected.json (+ STK4, PIPE). Reprenable. Usage : python scripts/v3_phase2_W12.py a|c [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize
from scipy.special import softmax
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R, v3_phase2_W8 as W8, v3_phase2_W11 as W11
from v3_phase2_W4 import AX
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5; H4, H9 = W11.HEADS4, W11.HEADS9; PIPE = "PIPE"


def f1_weights(oof, names, ytr, init, ids):
    ok = oof["Lc"][np.arange(len(ytr)), ytr] > -15; Z = [oof[n][ok] for n in names]; yt = ytr[ok]; lab = [c for c in ids if (yt == c).any()]
    def neg_f1(w): P = softmax(sum(wi * z for wi, z in zip(w, Z)), axis=1); pr = W8.decode_mix(P, 0.5, 1.0).argmax(1); return -float(f1_score(yt, pr, labels=lab, average="macro", zero_division=0))
    sol = minimize(neg_f1, x0=np.clip(init, 0, 3), method="Nelder-Mead", bounds=[(0, 3)] * len(names), options={"maxfev": 150, "xatol": 1e-2, "fatol": 1e-4}); return np.clip(sol.x, 0, 3), -float(sol.fun), -neg_f1(np.clip(init, 0, 3))


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes])
    objs = sorted({AX[c][0] for c in classes}); acts = sorted({AX[c][1] for c in classes}); obj_of = np.array([objs.index(AX[c][0]) for c in classes]); act_of = np.array([acts.index(AX[c][1]) for c in classes])
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; gl, gi = np.unique(dev.group.values[tr], return_inverse=True); need9 = any(n.endswith("9") or n.endswith("9s") for n in names); hs = H9 if need9 else H4; need = set(hs)
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte); ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc, Xct = ch.fit_transform(ttr), ch.transform(tte)
    vb = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", ngram_range=(1, 2), lowercase=True, sublinear_tf=True, min_df=2); Xb, Xbt = vb.fit_transform(ttr), vb.transform(tte); dims = (obj_of, act_of, fam_of, K, len(objs), len(acts), len(B.FAMS))
    full = W11.heads(X, Xc, Xb, ytr, np.arange(len(tr)), (Xt, Xct, Xbt), *dims, need); rng = np.random.default_rng(100 * r + 10 * k + 3); fg = rng.integers(0, 3, len(gl))[gi]; oof = {n: np.zeros((len(tr), K)) for n in need}
    for f in range(3):
        ev = np.where(fg == f)[0]; trn = np.where(fg != f)[0]; hh = W11.heads(X, Xc, Xb, ytr, trn, (X[ev], Xc[ev], Xb[ev]), *dims, need)
        for n in need: oof[n][ev] = hh[n]
    Wd = {}; info = {}
    w4n = W11.learn_weights(oof, H4, ytr); Wd["STK4"] = (H4, w4n)
    if "F4" in names or "F4s" in names:
        w4f, f1o, f1i = f1_weights(oof, H4, ytr, w4n, ids); Wd["F4"] = (H4, w4f); Wd["F4s"] = (H4, 0.5 * (w4n + w4f)); info["F4"] = {"oof_f1_init": round(f1i, 4), "oof_f1_opt": round(f1o, 4), "w": [round(float(x), 3) for x in w4f]}
    if need9:
        w9n = W11.learn_weights(oof, H9, ytr); w9f, f1o, f1i = f1_weights(oof, H9, ytr, w9n, ids); Wd["F9"] = (H9, w9f); Wd["F9s"] = (H9, 0.5 * (w9n + w9f)); info["F9"] = {"oof_f1_init": round(f1i, 4), "oof_f1_opt": round(f1o, 4), "w": [round(float(x), 3) for x in w9f]}
    res = {}
    for cn, nab in (("toutes", 0), ("abs8", 8), ("abs14", 14)):
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng((1000 if nab == 8 else 2000) * r + k); gone = rg.choice(np.unique(yte), size=min(nab, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]
        def rec(nm, P): pr = W8.decode_mix(P, 0.5, 1.0).argmax(1); res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pr, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pr, labels=L, average="macro", zero_division=0))}
        rec(PIPE, softmax(full["Lc"][keep], axis=1))
        for s, (hn, w) in Wd.items():
            if s in names or s == "STK4": rec(s, softmax(sum(wi * full[h][keep] for wi, h in zip(w, hn)), axis=1))
    res["_info"] = info; return res


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W12" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": sorted(names), "conditions": ["toutes", "abs8", "abs14"], "optimiseur": "Nelder-Mead 150", "file": "SIEVE_00"}
    return R.run_unit(block, f"W12{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = ["F4", "F4s", "F9", "F9s"]; block, code = "P2_W12a_selection", "W12a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W12_selected.json"))["variants"]; block, code = "P2_W12c_confirmation", "W12c.1"; reps = range(40, 50); folds = W11.make_folds(dev, reps); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
