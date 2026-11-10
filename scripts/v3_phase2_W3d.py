"""Réplication finale W3d (D33, HY9) : M50, A1 et LR sur 100 nouveaux plis (répétitions 20 à 39), conditions toutes, abs8, abs14. Dev seul. Reprenable. Usage : python scripts/v3_phase2_W3d.py c [--smoke] [--jobs N]"""
import sys, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.model_selection import StratifiedGroupKFold
import v3_phase2_W3 as W3, v3_blockA as A, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5; REPS = range(20, 40); NAMES = ["M50", "A1"]


def make_folds(dev):
    g = dev.groupby("group").agg(category=("category", "first")).reset_index(); out = {}
    for r in REPS:
        f = np.full(len(g), -1)
        for k, (_, te) in enumerate(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=r).split(g, g.category, g.group)): f[te] = k
        out[r] = dict(zip(g.group, f))
    return out


def unit(r, k, dev, tierA, fold):
    cfg = {"phase": 2, "iteration": "W3d", "repeat": r, "fold": k, "cap": A.CAP, "variants": NAMES, "conditions": W3.CONDS, "file": "SIEVE_00"}
    return R.run_unit("P2_W3d_final", f"W3d r{r} pli{k}", cfg, lambda: W3.task(r, k, dev, tierA, fold, NAMES), code_version="W3d.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); folds = make_folds(dev); t0 = time.time(); jobs = [(10, 0)] if "--smoke" in sys.argv else [(r, k) for r in REPS for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, dev.group.map(folds[r]).values) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
