"""Bloc A (protocole v3) : quatre protocoles de découpage x six modèles linéaires, sur le développement de SIEVE_00 (le test v2 n'est JAMAIS lu).
Protocoles : P0 au hasard (baseline), P1 simple par gabarit (un pli), P2 par groupes (5 plis x 5 répétitions), P3 imbriqué par groupes (réglage sur 3 plis intérieurs ; répétitions 0 à 2).
Choix écrits d'avance : au plus 400 logs par gabarit (tirage fixe, pour qu'un gabarit de 20 000 logs ne pèse pas 5 000 fois un gabarit de 4) ; macro-F1 sur les classes de 5 gabarits ou plus (« palier A »).
Reprenable : une unité = (protocole, répétition, pli) ; relancer saute ce qui est fait.  Usage : python scripts/v3_blockA.py [--smoke] [--jobs N]"""
import sys, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid
from sklearn.model_selection import KFold, StratifiedGroupKFold
from sklearn.metrics import f1_score, accuracy_score
import tp2_data as D, tp2_runner as R
warnings.filterwarnings("ignore")
CAP, NREP, JOBS = 400, 5, int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5
GRID = {"svm_word": ("C", [0.1, 1, 10]), "svm_char": ("C", [0.1, 1]), "lr_word": ("C", [1, 10, 100]), "nb_word": ("alpha", [0.03, 0.3, 3]), "knn_word": ("k", [3, 5, 15]), "centroid_word": (None, [None])}
DEFAULT = {"svm_word": 1, "svm_char": 1, "lr_word": 10, "nb_word": 0.3, "knn_word": 5, "centroid_word": None}
MODELS = list(GRID)


def load():
    V0 = D.load_versions(ROOT)[0]; sp = D.load_splits_v1(ROOT); G = pd.read_csv(ROOT / "artifacts" / "data" / "groups_v3.csv")
    df = V0.merge(sp[sp.version == 0][["row", "group"]], on="row").merge(G, on="group", suffixes=("", "_g"))
    assert (df.category == df.category_g).all(); dev = df[df.role == "dev"]                       # le test v2 est écarté ici, avant tout calcul
    dev = dev.sample(frac=1, random_state=0).groupby("group").head(CAP).sort_values(["group", "row"]).reset_index(drop=True)      # tirage fixe de 400 logs au plus par gabarit
    big = G.groupby("category").size(); tierA = sorted(big[big >= 5].index); return dev, tierA


def make(name, p):
    return {"svm_word": lambda: LinearSVC(C=p), "svm_char": lambda: LinearSVC(C=p), "lr_word": lambda: LogisticRegression(C=p, max_iter=300),
            "nb_word": lambda: ComplementNB(alpha=p), "knn_word": lambda: KNeighborsClassifier(n_neighbors=p, metric="cosine", algorithm="brute"), "centroid_word": lambda: NearestCentroid()}[name]()


def f1A(y, pred, tierA_ids):
    lab = [c for c in tierA_ids if (y == c).any()]; return float(f1_score(y, pred, labels=lab, average="macro", zero_division=0))


def twin(Xtr, Xte, rng):
    te = rng.choice(Xte.shape[0], size=min(1500, Xte.shape[0]), replace=False); tr = rng.choice(Xtr.shape[0], size=min(20000, Xtr.shape[0]), replace=False)
    best = np.asarray((Xte[te] @ Xtr[tr].T).max(axis=1).todense()).ravel(); return float((best >= 0.90).mean()), float(np.median(best))


def one_task(proto, r, k, dev, tierA):
    y_all = dev.category.astype("category"); classes = list(y_all.cat.categories); y = y_all.cat.codes.values; tierA_ids = [classes.index(c) for c in tierA]
    fold = dev[f"fold_r{r}"].values
    if proto == "P0": tr_i, te_i = [a for a in KFold(5, shuffle=True, random_state=r).split(dev)][k]
    else: te_i = np.where(fold == k)[0]; tr_i = np.where(fold != k)[0]
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xw_tr = word.fit_transform(dev.log.values[tr_i]); Xw_te = word.transform(dev.log.values[te_i])
    char = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000); Xc_tr = char.fit_transform(dev.log.values[tr_i]); Xc_te = char.transform(dev.log.values[te_i])
    res = {}; rng = np.random.default_rng(r)
    tw, med = twin(Xw_tr, Xw_te, rng)
    for m in MODELS:
        Xtr, Xte = (Xc_tr, Xc_te) if "char" in m else (Xw_tr, Xw_te); t0 = time.time(); param = DEFAULT[m]
        if proto == "P3" and GRID[m][0] is not None:                                           # réglage sur 3 plis intérieurs par groupes (gabarits du seul entraînement)
            sub = dev.iloc[tr_i]; inner = StratifiedGroupKFold(3, shuffle=True, random_state=r); scores = {}
            for v in GRID[m][1]:
                s = []
                for a, b in inner.split(sub, sub.category, sub.group):
                    mdl = make(m, v).fit(Xtr[a], y[tr_i][a]); s.append(f1A(y[tr_i][b], mdl.predict(Xtr[b]), tierA_ids))
                scores[v] = float(np.mean(s))
            param = max(scores, key=scores.get)
        mdl = make(m, param).fit(Xtr, y[tr_i]); pred = mdl.predict(Xte)
        res[m] = {"f1A": f1A(y[te_i], pred, tierA_ids), "f1_30": float(f1_score(y[te_i], pred, average="macro", zero_division=0)), "acc": float(accuracy_score(y[te_i], pred)), "param": param, "seconds": round(time.time() - t0, 1)}
    res["_info"] = {"n_train": int(len(tr_i)), "n_test": int(len(te_i)), "n_test_groups": int(dev.group.values[te_i].size and len(set(dev.group.values[te_i]))), "twin_share": tw, "median_nn_cos": med}
    return res


def unit(proto, r, k, dev, tierA):
    cfg = {"protocol": proto, "repeat": r, "fold": k, "cap": CAP, "models": MODELS, "grid": GRID, "file": "SIEVE_00", "splits": "groups_v3"}
    return R.run_unit("A_decoupage", f"{proto} r{r} pli{k}", cfg, lambda: one_task(proto, r, k, dev, tierA), code_version="A1")[1]


if __name__ == "__main__":
    dev, tierA = load(); print(len(dev), "logs (plafonnés) ;", dev.group.nunique(), "gabarits de développement ;", len(tierA), "classes de palier A", flush=True)
    jobs = [("P0", r, k) for r in range(NREP) for k in range(5)] + [("P1", r, 0) for r in range(NREP)] + [("P2", r, k) for r in range(NREP) for k in range(5)] + [("P3", r, k) for r in range(3) for k in range(5)]
    if "--smoke" in sys.argv: jobs = [("P2", 0, 0)]
    t0 = time.time(); out = Parallel(n_jobs=JOBS, verbose=5)(delayed(unit)(p, r, k, dev, tierA) for p, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
