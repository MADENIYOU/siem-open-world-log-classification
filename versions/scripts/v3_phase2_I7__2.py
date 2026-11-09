"""Itération I7 (D24) : rejet d'inconnus, 24 combinaisons (C de la tête x score). Étape a : rotations B x répétitions 0-4 ; étape b : rotations C x répétitions 5-9. Dev SIEVE_00 seul. Reprenable. Usage : python scripts/v3_phase2_I7.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.special import logsumexp
from scipy.stats import rankdata
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import v3_blockA as A, v3_blockB as B, tp2_openset as O, tp2_runner as R
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
SEEDS = {"a": 20261110, "b": 20261111}; CH = [4, 1, 16, 64]   # C = 4 : RÉFÉRENCE (msp de la baseline D24) ; seuls C = 1, 16, 64 sont des candidats
FORBID = [set(r) for r in json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["rotations"]] + [set(r) for r in json.load(open(ROOT / "artifacts" / "data" / "rotations_v2_I4.json"))["rotations"]]


def new_rotations(classes, seed):
    rng = np.random.default_rng(seed); cl = sorted(classes)
    while True:
        p = list(rng.permutation(cl)); rot = [sorted(p[i * 6:(i + 1) * 6]) for i in range(5)]
        if not any(set(r) in FORBID for r in rot): return rot


def scores(P, L, pf, PH):
    top2 = np.sort(pf, 1)[:, -2:]; e = logsumexp(L, axis=1); fm = pf.max(1)
    return {"msp": P.max(1), "energy": e, "hier_msp": PH.max(1), "fam_msp": fm, "fam_margin": top2[:, 1] - top2[:, 0], "fam_negent": (pf * np.log(pf + 1e-12)).sum(1), "fam_x_msp": fm * P.max(1),
            "rank_fam_energy": (rankdata(fm) + rankdata(e)) / 2}


def task(rot, r, k, dev, fold, ROT):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": "pli sans assez de logs"}
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = word.fit_transform(dev.log.values[tr_i]); Xte = word.transform(dev.log.values[te_i]); out = {}
    for ch in CH:
        lr = LogisticRegression(C=ch, max_iter=300).fit(Xtr, ytr); L = lr.decision_function(Xte); P = lr.predict_proba(Xte); PH, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=ch)
        for n, s in scores(P, L, pf, PH).items(): m = O.open_metrics(np.nan_to_num(s, nan=-1e9), known); out[f"C{ch}_{n}"] = {"auroc": m["auroc"], "fpr95": m["fpr95"], "aupr_in": m["aupr_in"]}
    return {"scores": out, "info": {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "masked": sorted(masked)}}


def unit(rot, r, k, dev, fold, ROT, block, code):
    cfg = {"phase": 2, "iteration": "I7" + STAGE, "rotation_set": STAGE, "rotation": rot, "masked": ROT[rot], "repeat": r, "fold": k, "cap": A.CAP, "rot_seed": SEEDS[STAGE], "C_head": CH, "file": "SIEVE_00"}
    return R.run_unit(block, f"I7{STAGE} rot{rot + 1} r{r} pli{k}", cfg, lambda: task(rot, r, k, dev, fold, ROT), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); ROT = new_rotations(dev.category.unique(), SEEDS[STAGE]); (ROOT / "artifacts" / "data" / f"rotations_v2_I7{STAGE}.json").write_text(json.dumps({"seed": SEEDS[STAGE], "rotations": ROT}, ensure_ascii=False, indent=1)); t0 = time.time()
    if STAGE == "a": reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: reps = range(5, 10); folds = make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(0, reps[0], 0)] if "--smoke" in sys.argv else [(rot, r, k) for rot in range(5) for r in reps for k in range(5)]; block, code = f"P2_I7{STAGE}_rejet_v2", f"I7{STAGE}.2"
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, r, k, dev, fold_of(r), ROT, block, code) for rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
