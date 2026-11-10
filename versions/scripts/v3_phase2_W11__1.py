"""Vague 11 (D43, HJ1-HJ5) : composition apprise élargie. Têtes : Lc, Lo, La (mots), Lf (lettres, famille) [STK4] ; + Lcc, Loc, Lac (lettres) [STK7] ; + Lfw (mots, famille), Lcb (uni- et bigrammes, classe) [STK9]. Poids appris hors-gabarit (3 plis internes), décodage M50. Conditions toutes, abs8, abs14. Dev seul.
Étape a : répétitions 0-4 ; étape c : confirmation répétitions 40-49 des variantes de W11_selected.json (+ STK4, PIPE). Reprenable. Usage : python scripts/v3_phase2_W11.py a|c [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize
from scipy.special import softmax, logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.model_selection import StratifiedGroupKFold
import v3_blockA as A, v3_blockB as B, tp2_runner as R, v3_phase2_W8 as W8
from v3_phase2_W4 import AX
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5; FLOOR = 1e-9
HEADS4 = ["Lc", "Lo", "La", "Lf"]; HEADS7 = HEADS4 + ["Lcc", "Loc", "Lac"]; HEADS9 = HEADS7 + ["Lfw", "Lcb"]; SUBSETS = {"STK4": HEADS4, "STK7": HEADS7, "STK9": HEADS9}; PIPE = "PIPE"


def fp(P, cl, n):
    out = np.full((P.shape[0], n), FLOOR); out[:, cl] = P; return out


def heads(Xw, Xc, Xb, ytr, idx, ev, obj_of, act_of, fam_of, K, nobj, nact, nfam, need):
    """Log-scores (n_eval x K) des têtes demandées, entraînées sur les lignes idx, évaluées sur ev = (Xw_e, Xc_e, Xb_e)."""
    Xw_e, Xc_e, Xb_e = ev; out = {}
    def fit(X, Xe, lab, n, per_class):
        m = LogisticRegression(C=10, max_iter=300).fit(X[idx], lab[idx]); P = np.log(fp(m.predict_proba(Xe), m.classes_, n)); return P if per_class == "cls" else P[:, per_class]
    if "Lc" in need: out["Lc"] = fit(Xw, Xw_e, ytr, K, "cls")
    if "Lo" in need: out["Lo"] = fit(Xw, Xw_e, obj_of[ytr], nobj, obj_of)
    if "La" in need: out["La"] = fit(Xw, Xw_e, act_of[ytr], nact, act_of)
    if "Lf" in need: out["Lf"] = fit(Xc, Xc_e, fam_of[ytr], nfam, fam_of)
    if "Lcc" in need: out["Lcc"] = fit(Xc, Xc_e, ytr, K, "cls")
    if "Loc" in need: out["Loc"] = fit(Xc, Xc_e, obj_of[ytr], nobj, obj_of)
    if "Lac" in need: out["Lac"] = fit(Xc, Xc_e, act_of[ytr], nact, act_of)
    if "Lfw" in need: out["Lfw"] = fit(Xw, Xw_e, fam_of[ytr], nfam, fam_of)
    if "Lcb" in need: out["Lcb"] = fit(Xb, Xb_e, ytr, K, "cls")
    return out


def learn_weights(oof, names, ytr):
    ok = oof["Lc"][np.arange(len(ytr)), ytr] > -15; Z = [oof[n][ok] for n in names]; yt = ytr[ok]
    def nll(w): s = sum(wi * z for wi, z in zip(w, Z)); return float(-(s[np.arange(len(yt)), yt] - logsumexp(s, axis=1)).mean())
    x0 = np.zeros(len(names)); x0[0] = 1.0; sol = minimize(nll, x0=x0, method="L-BFGS-B", bounds=[(0, 5)] * len(names)); return sol.x


def task(r, k, dev, tierA, fold, names):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes])
    objs = sorted({AX[c][0] for c in classes}); acts = sorted({AX[c][1] for c in classes}); obj_of = np.array([objs.index(AX[c][0]) for c in classes]); act_of = np.array([acts.index(AX[c][1]) for c in classes])
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]; gl, gi = np.unique(dev.group.values[tr], return_inverse=True); sub = sorted({s for s in names if s.startswith("STK")}, key=lambda s: len(SUBSETS[s]))
    need = set(HEADS4) | {h for s in sub for h in SUBSETS[s]}
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte); ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc, Xct = ch.fit_transform(ttr), ch.transform(tte)
    vb = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", ngram_range=(1, 2), lowercase=True, sublinear_tf=True, min_df=2); Xb, Xbt = vb.fit_transform(ttr), vb.transform(tte); dims = (obj_of, act_of, fam_of, K, len(objs), len(acts), len(B.FAMS))
    full = heads(X, Xc, Xb, ytr, np.arange(len(tr)), (Xt, Xct, Xbt), *dims, need); rng = np.random.default_rng(100 * r + 10 * k + 3); fg = rng.integers(0, 3, len(gl))[gi]; oof = {n: np.zeros((len(tr), K)) for n in need}
    for f in range(3):
        ev = np.where(fg == f)[0]; trn = np.where(fg != f)[0]; hh = heads(X, Xc, Xb, ytr, trn, (X[ev], Xc[ev], Xb[ev]), *dims, need)
        for n in need: oof[n][ev] = hh[n]
    W = {s: learn_weights(oof, SUBSETS[s], ytr) for s in sub}; info = {s: {h: round(float(w), 3) for h, w in zip(SUBSETS[s], W[s])} for s in sub}; res = {}
    for cn, nab in (("toutes", 0), ("abs8", 8), ("abs14", 14)):
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng((1000 if nab == 8 else 2000) * r + k); gone = rg.choice(np.unique(yte), size=min(nab, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]
        def rec(nm, P): pr = W8.decode_mix(P, 0.5, 1.0).argmax(1); res[f"{nm}|{cn}"] = {"f1A": float(f1_score(yk, pr, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pr, labels=L, average="macro", zero_division=0))}
        rec(PIPE, softmax(full["Lc"][keep], axis=1))
        for s in sub: rec(s, softmax(sum(w * full[h][keep] for w, h in zip(W[s], SUBSETS[s])), axis=1))
    res["_info"] = info; return res


def make_folds(dev, reps):
    g = dev.groupby("group").agg(category=("category", "first")).reset_index(); out = {}
    for r in reps:
        f = np.full(len(g), -1)
        for k, (_, te) in enumerate(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=r).split(g, g.category, g.group)): f[te] = k
        out[r] = dict(zip(g.group, f))
    return out


def unit(r, k, dev, tierA, fold, names, block, code):
    cfg = {"phase": 2, "iteration": "W11" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": sorted(names), "conditions": ["toutes", "abs8", "abs14"], "file": "SIEVE_00"}
    return R.run_unit(block, f"W11{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    if STAGE == "a": names = ["STK4", "STK7", "STK9"]; block, code = "P2_W11a_selection", "W11a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = ["STK4"] + json.load(open(ROOT / "artifacts" / "results" / "v3" / "W11_selected.json"))["variants"]; block, code = "P2_W11c_confirmation", "W11c.1"; reps = range(40, 50); folds = make_folds(dev, reps); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
