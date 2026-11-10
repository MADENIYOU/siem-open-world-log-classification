"""Vague 5 (D37, HO1-HO3) : détection d'inconnus par la famille AVEC décodage M50 sur le lot. Rotations de l'ensemble B (étape a, graine 20261110, répétitions 0-4) ou C (étape b, graine 20261111, répétitions 5-9) comme I7. Dev seul. Reprenable. Usage : python scripts/v3_phase2_W5.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import v3_blockA as A, v3_blockB as B, tp2_openset as O, tp2_runner as R, v3_phase2_I7 as I7, v3_phase2_W3 as W3
from v3_phase2_I1b import make_folds
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6; C = 16


def task(rot, r, k, dev, fold, ROT):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": "pli sans assez de logs"}
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = word.fit_transform(dev.log.values[tr_i]); Xte = word.transform(dev.log.values[te_i])
    lr = LogisticRegression(C=C, max_iter=300).fit(Xtr, ytr); P = lr.predict_proba(Xte); PH, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C)
    Q = W3.decode("M50", P); Fm = np.zeros((P.shape[1], len(B.FAMS))); Fm[np.arange(P.shape[1]), fam_of[lr.classes_]] = 1.0; pfq = Q @ Fm; pfd = W3.decode("M50", pf + 1e-9)
    S = {"MSP": P.max(1), "FAM": pf.max(1), "FAMQ": pfq.max(1), "FAMD": pfd.max(1), "MSPQ": Q.max(1)}
    out = {n: {kk: v for kk, v in O.open_metrics(np.nan_to_num(s, nan=-1e9), known).items() if kk in ("auroc", "fpr95")} for n, s in S.items()}
    return {"scores": out, "info": {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "masked": sorted(masked)}}


def unit(rot, r, k, dev, fold, ROT, block, code):
    cfg = {"phase": 2, "iteration": "W5" + STAGE, "rotation_set": STAGE, "rotation": rot, "masked": ROT[rot], "repeat": r, "fold": k, "cap": A.CAP, "rot_seed": I7.SEEDS[STAGE], "C": C, "file": "SIEVE_00"}
    return R.run_unit(block, f"W5{STAGE} rot{rot + 1} r{r} pli{k}", cfg, lambda: task(rot, r, k, dev, fold, ROT), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); ROT = I7.new_rotations(dev.category.unique(), I7.SEEDS[STAGE]); ref = json.load(open(ROOT / "artifacts" / "data" / f"rotations_v2_I7{STAGE}.json"))["rotations"]; assert ROT == ref, "les rotations ne sont pas celles d'I7"; t0 = time.time()
    if STAGE == "a": reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: reps = range(5, 10); folds = make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    block, code = f"P2_W5{STAGE}_rejet_decode", f"W5{STAGE}.1"; jobs = [(0, reps[0], 0)] if "--smoke" in sys.argv else [(rot, r, k) for rot in range(5) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, r, k, dev, fold_of(r), ROT, block, code) for rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
