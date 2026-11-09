"""Itération I7c (D25) : réplication du rejet d'inconnus sur 3 nouveaux jeux de 5 rotations x répétitions 10 à 14 (75 unités rotation x répétition). Dev SIEVE_00 seul. Reprenable. Usage : python scripts/v3_phase2_I7c.py c [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.model_selection import StratifiedGroupKFold
import v3_phase2_I7 as I7, v3_blockA as A, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
SETS = {"D": 20261112, "E": 20261113, "F": 20261114}; REPS = range(10, 15)
for s in ("a", "b"): I7.FORBID += [set(r) for r in json.load(open(ROOT / "artifacts" / "data" / f"rotations_v2_I7{s}.json"))["rotations"]]


def make_folds(dev):
    g = dev.groupby("group").agg(category=("category", "first")).reset_index(); out = {}
    for r in REPS:
        f = np.full(len(g), -1)
        for k, (_, te) in enumerate(StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=r).split(g, g.category, g.group)): f[te] = k
        out[r] = dict(zip(g.group, f))
    return out


def unit(name, rot, r, k, dev, fold, ROT):
    cfg = {"phase": 2, "iteration": "I7c", "rotation_set": name, "rotation": rot, "masked": ROT[rot], "repeat": r, "fold": k, "cap": A.CAP, "rot_seed": SETS[name], "C_head": I7.CH, "file": "SIEVE_00"}
    return R.run_unit("P2_I7c_rejet", f"I7c {name} rot{rot + 1} r{r} pli{k}", cfg, lambda: I7.task(rot, r, k, dev, fold, ROT), code_version="I7c.1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); folds = make_folds(dev); ROTS = {}
    for name, seed in SETS.items(): ROTS[name] = I7.new_rotations(dev.category.unique(), seed); I7.FORBID += [set(r) for r in ROTS[name]]
    (ROOT / "artifacts" / "data" / "rotations_v2_I7c.json").write_text(json.dumps({"seeds": SETS, "rotations": ROTS}, ensure_ascii=False, indent=1)); t0 = time.time()
    jobs = [("D", 0, 10, 0)] if "--smoke" in sys.argv else [(n, rot, r, k) for n in SETS for rot in range(5) for r in REPS for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(n, rot, r, k, dev, dev.group.map(folds[r]).values, ROTS[n]) for n, rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
