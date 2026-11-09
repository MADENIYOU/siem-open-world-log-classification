"""Itération I4 : confirmation du rejet par confiance de famille (D19, HI1-HI4) sur 5 NOUVELLES rotations x 25 NOUVEAUX plis (répétitions 5 à 9). Dev SIEVE_00 seul. Reprenable. Usage : python scripts/v3_phase2_I4.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.special import logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import v3_blockA as A, v3_blockB as B, tp2_openset as O, tp2_runner as R
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
SEED, C_HEAD = 20261109, 4.0; V1 = [set(r) for r in json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["rotations"]]


def new_rotations(classes):
    rng = np.random.default_rng(SEED); cl = sorted(classes)
    while True:
        p = list(rng.permutation(cl)); rot = [sorted(p[i * 6:(i + 1) * 6]) for i in range(5)]
        if not any(set(r) in V1 for r in rot): return rot


def task(rot, r, k, dev, folds, ROT):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev.group.map(folds[r]).values
    te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": f"pli sans assez de logs (connus {int(known.sum())}, inconnus {int((~known).sum())})"}
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = word.fit_transform(dev.log.values[tr_i]); Xte = word.transform(dev.log.values[te_i])
    lr = LogisticRegression(C=C_HEAD, max_iter=300).fit(Xtr, ytr); L = lr.decision_function(Xte); P = lr.predict_proba(Xte); S = {"msp": P.max(1), "maxlogit": L.max(1), "energy": logsumexp(L, axis=1)}
    PH, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C_HEAD); S["hier_msp"] = PH.max(1); S["fam_msp"] = pf.max(1)
    out = {n: {kk: v for kk, v in O.open_metrics(np.nan_to_num(s, nan=-1e9), known).items() if kk in ("auroc", "fpr95", "aupr_in")} for n, s in S.items()}
    return {"scores": out, "info": {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "masked": sorted(masked)}}


def unit(rot, r, k, dev, folds, ROT):
    cfg = {"phase": 2, "iteration": "I4", "rotation_v2": rot, "masked": ROT[rot], "repeat": r, "fold": k, "cap": A.CAP, "C_head": C_HEAD, "rot_seed": SEED, "file": "SIEVE_00", "folds": "StratifiedGroupKFold graine = répétition (5 à 9)"}
    return R.run_unit("P2_I4_rejet_famille", f"I4 rot{rot + 1} r{r} pli{k}", cfg, lambda: task(rot, r, k, dev, folds, ROT), code_version="I4.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); folds = make_folds(dev); ROT = new_rotations(dev.category.unique()); (ROOT / "artifacts" / "data" / "rotations_v2_I4.json").write_text(json.dumps({"seed": SEED, "rotations": ROT}, ensure_ascii=False, indent=1))
    jobs = [(0, 5, 0)] if "--smoke" in sys.argv else [(rot, r, k) for rot in range(5) for r in range(5, 10) for k in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, r, k, dev, folds, ROT) for rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
