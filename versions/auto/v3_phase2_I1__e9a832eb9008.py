"""Phase 2, itération I1 (protocole v3) : corriger la représentation. Classification à 30 classes, P2 (5 plis × 5 répétitions), SIEVE_00, développement seul (le test v2 n'est JAMAIS lu),
400 logs au plus par gabarit. Variantes (voir D16) : V0 baseline (SVM mots) ; T2, T3, T5 (vocabulaire restreint aux mots présents dans au moins m GABARITS d'entraînement) ; T3M (mots écartés remplacés par un marqueur « valeur ») ;
ENS (somme des marges SVM mots et SVM caractères) ; WGT (chaque gabarit pèse autant) ; C1 = T3 + WGT ; C2 = T3 + ENS ; C3 = T3 + ENS + WGT. Reprenable. Usage : python scripts/v3_phase2_I1.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score, accuracy_score
import re
import v3_blockA as A, v3_blockB as B, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
WORD = re.compile(r"[A-Za-z]{2,}"); VARIANTS = ["V0", "T2", "T3", "T5", "T3M", "ENS", "WGT", "C1", "C2", "C3"]


def template_support(texts, grp_idx, n_groups):
    cv = CountVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, binary=True); Xb = cv.fit_transform(texts)
    G = sparse.csr_matrix((np.ones(len(grp_idx)), (grp_idx, np.arange(len(grp_idx)))), shape=(n_groups, len(grp_idx))); S = (G @ Xb).tocsc(); S.data[:] = 1
    return dict(zip(cv.get_feature_names_out(), np.asarray(S.sum(0)).ravel().astype(int)))


def vec_support(support, m, replace):
    keep = {w for w, s in support.items() if s >= m}
    def analyzer(t):
        out = []
        for w in WORD.findall(t.lower()):
            if w in keep: out.append(w)
            elif replace: out.append("valtok")
        return out
    return TfidfVectorizer(analyzer=analyzer, sublinear_tf=True)


def task(r, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; tierA_ids = [classes.index(c) for c in tierA]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values; te_i = np.where(fold == k)[0]; tr_i = np.where(fold != k)[0]; ytr, yte = y[tr_i], y[te_i]
    ttr, tte = dev.log.values[tr_i], dev.log.values[te_i]; gl, gi = np.unique(dev.group.values[tr_i], return_inverse=True); cnt = np.bincount(gi); w_tpl = 1.0 / cnt[gi]; w_tpl = w_tpl * len(w_tpl) / w_tpl.sum()
    sup = template_support(ttr, gi, len(gl)); res = {}; feats = {}
    def record(name, dec, t0):
        pred = LinearSVC.classes_ if False else None
    def fit_pred(X, Xt, sw=None):
        m = LinearSVC(C=1).fit(X, ytr, sample_weight=sw); return m.classes_, m.decision_function(Xt)
    def metr(cls_, dec, name, t0):
        pred = cls_[dec.argmax(1)]; ft = fam_of[yte]; fp = fam_of[pred]; lab = [c for c in tierA_ids if (yte == c).any()]; dist = np.where(pred == yte, 0, np.where(fp == ft, 1, 2))
        res[name] = {"f1A": float(f1_score(yte, pred, labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte, pred, labels=np.unique(yte), average="macro", zero_division=0)), "acc": float(accuracy_score(yte, pred)),
                     "f1_fam": float(f1_score(ft, fp, labels=np.unique(ft), average="macro", zero_division=0)), "tree_dist": float(dist.mean()), "seconds": round(time.time() - t0, 1)}
    t0 = time.time(); v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X0 = v.fit_transform(ttr); Xt0 = v.transform(tte); c0, d0 = fit_pred(X0, Xt0); metr(c0, d0, "V0", t0); n0 = X0.shape[1]
    for nm, m_, rep in (("T2", 2, False), ("T3", 3, False), ("T5", 5, False), ("T3M", 3, True)):
        t0 = time.time(); vv = vec_support(sup, m_, rep); X = vv.fit_transform(ttr); Xt = vv.transform(tte); c, d = fit_pred(X, Xt); metr(c, d, nm, t0); res[nm]["dim"] = int(X.shape[1])
        if nm == "T3": X3, Xt3, c3, d3 = X, Xt, c, d
    res["V0"]["dim"] = int(n0)
    t0 = time.time(); ch = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc = ch.fit_transform(ttr); Xtc = ch.transform(tte); cc, dc = fit_pred(Xc, Xtc); cw, dcw = fit_pred(Xc, Xtc, w_tpl)
    metr(c0, d0 + dc, "ENS", t0)
    t0 = time.time(); cwv, dwv = fit_pred(X0, Xt0, w_tpl); metr(cwv, dwv, "WGT", t0)
    t0 = time.time(); c1, d1 = fit_pred(X3, Xt3, w_tpl); metr(c1, d1, "C1", t0)
    t0 = time.time(); metr(c3, d3 + dc, "C2", t0)
    t0 = time.time(); metr(c1, d1 + dcw, "C3", t0)
    res["_info"] = {"n_train": int(len(tr_i)), "n_test": int(len(te_i)), "n_train_templates": int(len(gl)), "vocabulaire_V0": int(n0), "mots_support_1": int(sum(1 for s in sup.values() if s == 1)), "mots_total": int(len(sup))}
    return res


def unit(r, k, dev, tierA):
    cfg = {"phase": 2, "iteration": "I1", "repeat": r, "fold": k, "cap": A.CAP, "variants": VARIANTS, "file": "SIEVE_00", "splits": "groups_v3"}
    return R.run_unit("P2_I1_representation", f"I1 r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA), code_version="I1.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0)] if "--smoke" in sys.argv else [(r, k) for r in range(A.NREP) for k in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
