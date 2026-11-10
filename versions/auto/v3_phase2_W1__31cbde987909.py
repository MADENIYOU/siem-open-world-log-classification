"""Vague 1 (D28, HW1-HW8) : F8 décodage à masses équilibrées, F14 racines, F6 IDF de gabarit + pureté, F9 hiérarchie à vues séparées, F18 format. 30 classes, SIEVE_00, développement seul (v3_blockA.load()).
Étape a : sélection, répétitions 0-4, toutes les variantes. Étape b : confirmation, répétitions 5-9, variantes de artifacts/results/v3/W1_selected.json. Reprenable. Usage : python scripts/v3_phase2_W1.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings, re, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, v3_blockB as B, tp2_runner as R, tp2_fields as F
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
WORD = re.compile(r"[A-Za-z]{2,}"); STOPF = set("jan feb mar apr may jun jul aug sep oct nov dec mon tue wed thu fri sat sun am pm pid utc gmt uid".split())
VARIANTS = ["A1", "A2", "B5", "B6", "B7", "C0", "C1", "C2", "D0.5", "D1", "D2", "E1", "E2"]; REFOF = {"A1": "REF_LR", "A2": "REF_LR"}
_FMT = {}


def fmt_of_groups(dev):
    if not _FMT:
        mode = lambda s: collections.Counter(s).most_common(1)[0][0]
        for g, s in dev.groupby("group").log:
            p = mode([(lambda m: m.group(1).lower() if m else "aucun")(F.RE_PROG.search(x)) for x in s]); f = mode(["-".join(F.vtype(t)[:3] for t in x.split()[:6]) for x in s]); _FMT[g] = p + "|" + f[:15]
    return _FMT


def sinkhorn(P, gamma=0.5, it=10):
    Q = P.copy(); K = Q.shape[1]
    for _ in range(it): Q = Q * ((Q.shape[0] / K) / (Q.sum(0) + 1e-12)) ** gamma; Q = Q / Q.sum(1, keepdims=True)
    return Q


def em_prior(P, pi0, it=30):
    pi = pi0.copy()
    for _ in range(it): Q = P * (pi / pi0); Q = Q / Q.sum(1, keepdims=True); pi = Q.mean(0) + 1e-12
    return Q


def task(r, k, dev, tierA, fold, names, small_cls):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]; sm = [classes.index(c) for c in small_cls]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; ttr, tte = dev.log.values[tr], dev.log.values[te]
    gl, gi = np.unique(dev.group.values[tr], return_inverse=True); res = {}
    def rec(name, pred):
        L = np.unique(yte); a = [c for c in ids if c in L]; s = [c for c in sm if c in L]
        res[name] = {"f1A": float(f1_score(yte, pred, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yte, pred, labels=L, average="macro", zero_division=0)), "f1_small": float(f1_score(yte, pred, labels=s, average="macro", zero_division=0)) if s else float("nan")}
    def need(n): return n in names
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(ttr), v.transform(tte); m0 = LinearSVC(C=1).fit(X, ytr); D0 = m0.decision_function(Xt); cl = m0.classes_; rec("REF_V0", cl[D0.argmax(1)])
    if need("REF_LR") or need("A1") or need("A2"):
        lr = LogisticRegression(C=10, max_iter=300).fit(X, ytr); P = lr.predict_proba(Xt); rec("REF_LR", lr.classes_[P.argmax(1)])
        if need("A1"): rec("A1", lr.classes_[sinkhorn(P).argmax(1)])
        if need("A2"): pi0 = np.bincount(ytr, minlength=len(classes))[lr.classes_] / len(ytr); rec("A2", lr.classes_[em_prior(P, pi0).argmax(1)])
    for kk in (5, 6, 7):
        if need(f"B{kk}"):
            vv = TfidfVectorizer(analyzer=lambda t, kk=kk: [w[:kk] for w in WORD.findall(t.lower())], sublinear_tf=True, min_df=2); mm = LinearSVC(C=1).fit(vv.fit_transform(ttr), ytr); rec(f"B{kk}", mm.classes_[mm.decision_function(vv.transform(tte)).argmax(1)])
    if any(need(f"C{i}") for i in range(3)):
        cv = CountVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, min_df=2); Cc = cv.fit_transform(ttr); Ct = cv.transform(tte); Kc = len(classes)
        Gm = sparse.csr_matrix((np.ones(len(gi)), (gi, np.arange(len(gi)))), shape=(len(gl), len(gi))); Sg = (Gm @ (Cc > 0).astype(float)); Sg.data[:] = 1; dfG = np.asarray(Sg.sum(0)).ravel(); idf = np.log((len(gl) + 1) / (dfG + 1)) + 1
        ygrp = np.zeros(len(gl), int); ygrp[gi] = ytr; Km = sparse.csr_matrix((np.ones(len(gl)), (ygrp, np.arange(len(gl)))), shape=(Kc, len(gl))); ncw = np.asarray((Km @ Sg).todense()); alpha = 2.0
        p = (ncw + alpha / Kc) / (dfG + alpha); kappa = 1 - (-(p * np.log(p + 1e-12)).sum(0)) / np.log(Kc)
        for i, lam in enumerate((0, 1, 2)):
            if need(f"C{i}"):
                w = idf * (1 + lam * kappa); Xc = normalize(Cc.multiply(1).tocsr().astype(float)); Xc.data = np.log1p(Cc.data) if False else Xc.data
                Xs = Cc.copy().astype(float); Xs.data = np.log1p(Xs.data); Xt2 = Ct.copy().astype(float); Xt2.data = np.log1p(Xt2.data); W = sparse.diags(w); Xa, Xb = normalize(Xs @ W), normalize(Xt2 @ W); mm = LinearSVC(C=1).fit(Xa, ytr); rec(f"C{i}", mm.classes_[mm.decision_function(Xb).argmax(1)])
    if any(need(f"D{b}") for b in ("0.5", "1", "2")):
        ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); lf = LogisticRegression(C=10, max_iter=300).fit(ch.fit_transform(ttr), fam_of[ytr]); pf = lf.predict_proba(ch.transform(tte)); logp = np.full((len(tte), len(B.FAMS)), np.log(1e-6)); logp[:, lf.classes_] = np.log(pf + 1e-9); Fc = logp[:, fam_of[cl]]
        for b in ("0.5", "1", "2"):
            if need(f"D{b}"): rec(f"D{b}", cl[(D0 + float(b) * Fc).argmax(1)])
    if need("E1"):
        def an(t):
            pm = F.RE_PROG.search(t); pr = pm.group(1).lower() if pm else None
            return [w for w in WORD.findall(t.lower()) if w not in STOPF and w != pr]
        vv = TfidfVectorizer(analyzer=an, sublinear_tf=True, min_df=2); mm = LinearSVC(C=1).fit(vv.fit_transform(ttr), ytr); rec("E1", mm.classes_[mm.decision_function(vv.transform(tte)).argmax(1)])
    if need("E2"):
        fm = fmt_of_groups(dev); fg = [fm[g] for g in gl]; ygrp = np.zeros(len(gl), int); ygrp[gi] = ytr; N = len(gl); nf = collections.Counter(fg); nc = collections.Counter(ygrp); nfc = collections.Counter(zip(fg, ygrp))
        wg = np.array([np.clip(nf[f] * nc[c] / (N * nfc[(f, c)]), 0.2, 5.0) for f, c in zip(fg, ygrp)]); sw = wg[gi]; sw = sw * len(sw) / sw.sum(); mm = LinearSVC(C=1).fit(X, ytr, sample_weight=sw); rec("E2", mm.classes_[mm.decision_function(Xt).argmax(1)])
    return res


def unit(r, k, dev, tierA, fold, names, small, block, code):
    cfg = {"phase": 2, "iteration": "W1" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": names, "file": "SIEVE_00"}
    return R.run_unit(block, f"W1{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names, small), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); fmt_of_groups(dev); ng = dev.groupby("category").group.nunique(); small = sorted(ng[ng <= 3].index); t0 = time.time()
    if STAGE == "a":
        names = ["REF_V0", "REF_LR"] + VARIANTS; block, code = "P2_W1a_selection", "W1a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else:
        sel = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W1_selected.json"))["variants"]; names = ["REF_V0", "REF_LR"] + sel; block, code = "P2_W1b_confirmation", "W1b.1"; reps = range(5, 10); folds = make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, small, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
