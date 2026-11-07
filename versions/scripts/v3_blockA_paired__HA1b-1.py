"""HA1b : effet pur de la fuite, sur les MÊMES logs de test (montage apparié). Pour chaque pli de groupes (r, k) : T_b = moitié tirée au hasard des logs du pli (test),
T_a = l'autre moitié. Condition G : entraînement = logs des autres plis. Condition H : entraînement = G plus T_a (logs des mêmes gabarits que T_b). Évaluation sur T_b dans les deux cas.
Le développement seul est lu (le test v2 n'est jamais lu). Reprenable. Usage : python scripts/v3_blockA_paired.py [--jobs N]"""
import sys, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score
import v3_blockA as A, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5


def fit_eval(dev, y, tr_i, te_i, tierA_ids):
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xw_tr = word.fit_transform(dev.log.values[tr_i]); Xw_te = word.transform(dev.log.values[te_i])
    char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc_tr = char.fit_transform(dev.log.values[tr_i]); Xc_te = char.transform(dev.log.values[te_i]); out = {}
    for m in A.MODELS:
        Xtr, Xte = (Xc_tr, Xc_te) if "char" in m else (Xw_tr, Xw_te); mdl = A.make(m, A.DEFAULT[m]).fit(Xtr, y[tr_i]); pred = mdl.predict(Xte)
        out[m] = {"f1A": A.f1A(y[te_i], pred, tierA_ids), "f1_30": float(f1_score(y[te_i], pred, average="macro", zero_division=0))}
    return out


def task(r, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; tierA_ids = [classes.index(c) for c in tierA]
    fold = dev[f"fold_r{r}"].values; te_all = np.where(fold == k)[0]; tr_G = np.where(fold != k)[0]
    perm = np.random.default_rng(1000 * r + k).permutation(te_all); Ta, Tb = perm[: len(perm) // 2], perm[len(perm) // 2:]
    G = fit_eval(dev, y, tr_G, Tb, tierA_ids); H = fit_eval(dev, y, np.concatenate([tr_G, Ta]), Tb, tierA_ids)
    return {"G": G, "H": H, "_info": {"n_test": int(len(Tb)), "n_train_G": int(len(tr_G)), "n_train_H": int(len(tr_G) + len(Ta))}}


def unit(r, k, dev, tierA):
    cfg = {"hypothese": "HA1b", "repeat": r, "fold": k, "cap": A.CAP, "models": A.MODELS, "default": A.DEFAULT, "file": "SIEVE_00", "splits": "groups_v3"}
    return R.run_unit("A_decoupage_apparie", f"HA1b r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA), code_version="HA1b-1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); t0 = time.time()
    out = Parallel(n_jobs=JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA) for r in range(A.NREP) for k in range(5))
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
