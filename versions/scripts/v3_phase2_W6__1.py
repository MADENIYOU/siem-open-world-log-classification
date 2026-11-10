"""Vague 6 (D37, HR1-HR4) : V-REx (variance du risque entre gabarits) et embeddings gelés DistilBERT, modes brut et M50, condition « toutes ». 30 classes, SIEVE_00, développement seul.
Étape a : répétitions 0-4 ; étape b : répétitions 10-19, variantes de artifacts/results/v3/W6_selected.json. Reprenable. Usage : python scripts/v3_phase2_W6.py a|b [--smoke] [--jobs N] (nécessite scripts/v3_embed_dev_frozen.py)"""
import sys, time, json, pathlib, warnings, glob
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, scipy.sparse as sp
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, tp2_runner as R, v3_phase2_W3 as W3, v3_phase2_W3c as W3c
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6
VARS = ["VR1", "VR5", "VR20", "E1", "E2", "E3"]; EMB = ROOT / "artifacts" / "results" / "v3" / "emb_distilbert_frozen"


def load_emb():
    return np.concatenate([np.load(f) for f in sorted(glob.glob(str(EMB / "part_*.npy")))])


def full_proba(P, cl, K):
    out = np.full((P.shape[0], K), 1e-9); out[:, cl] = P; return out / out.sum(1, keepdims=True)


def torch_softmax(X, y, gi, Xt, K, lam, C=10, iters=60):
    import torch; torch.set_num_threads(1)
    cl = np.unique(y); yi = np.searchsorted(cl, y); n, V = X.shape; Xc = X.tocoo(); Xtt = torch.sparse_coo_tensor(np.vstack([Xc.row, Xc.col]), Xc.data.astype(np.float32), X.shape).coalesce()
    W = torch.zeros((V, len(cl)), requires_grad=True); b = torch.zeros(len(cl), requires_grad=True); yt = torch.tensor(yi); g = torch.tensor(gi); G = int(gi.max()) + 1; cnt = torch.bincount(g, minlength=G).float(); l2 = 1.0 / (2 * C * n)
    opt = torch.optim.LBFGS([W, b], lr=1.0, max_iter=iters, line_search_fn="strong_wolfe")
    def closure():
        opt.zero_grad(); logits = torch.sparse.mm(Xtt, W) + b; ce = torch.nn.functional.cross_entropy(logits, yt, reduction="none"); Lg = torch.zeros(G).index_add_(0, g, ce) / cnt
        loss = Lg.mean() + lam * Lg.var(unbiased=False) + l2 * (W ** 2).sum(); loss.backward(); return loss
    opt.step(closure); Xc2 = Xt.tocoo(); Xte = torch.sparse_coo_tensor(np.vstack([Xc2.row, Xc2.col]), Xc2.data.astype(np.float32), Xt.shape).coalesce()
    with torch.no_grad(): P = torch.softmax(torch.sparse.mm(Xte, W) + b, 1).numpy()
    return full_proba(P, cl, K)


def task(r, k, dev, tierA, fold, names, EM):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]
    gl, gi = np.unique(dev.group.values[tr], return_inverse=True); v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(dev.log.values[tr]), v.transform(dev.log.values[te]); mats = {}
    lr = LogisticRegression(C=10, max_iter=300).fit(X, ytr); mats["LR"] = full_proba(lr.predict_proba(Xt), lr.classes_, K); mats["ERM"] = torch_softmax(X, ytr, gi, Xt, K, 0.0)
    for nm, lam in (("VR1", 1.0), ("VR5", 5.0), ("VR20", 20.0)):
        if nm in names: mats[nm] = torch_softmax(X, ytr, gi, Xt, K, lam)
    if any(n in names for n in ("E1", "E2", "E3")):
        mu, sd = EM[tr].mean(0), EM[tr].std(0) + 1e-6; Etr, Ete = (EM[tr] - mu) / sd, (EM[te] - mu) / sd
        le = LogisticRegression(C=1, max_iter=200).fit(Etr, ytr); Pe = full_proba(le.predict_proba(Ete), le.classes_, K)
        if "E1" in names: mats["E1"] = Pe
        if "E2" in names: g2 = np.sqrt(mats["LR"] * Pe); mats["E2"] = g2 / g2.sum(1, keepdims=True)
        if "E3" in names:
            l3 = LogisticRegression(C=10, max_iter=300).fit(sp.hstack([X, sp.csr_matrix(0.1 * Etr)]).tocsr(), ytr); mats["E3"] = full_proba(l3.predict_proba(sp.hstack([Xt, sp.csr_matrix(0.1 * Ete)]).tocsr()), l3.classes_, K)
    res = {}; L = np.unique(yte); a = [c for c in ids if c in L]
    for nm, P in mats.items():
        for mode, pred in (("brut", P.argmax(1)), ("M50", W3.decode("M50", P).argmax(1))): res[f"{nm}|toutes|{mode}"] = {"f1A": float(f1_score(yte, pred, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yte, pred, labels=L, average="macro", zero_division=0))}
    return res


def unit(r, k, dev, tierA, fold, names, EM, block, code):
    cfg = {"phase": 2, "iteration": "W6" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": names, "modes": ["brut", "M50"], "file": "SIEVE_00"}
    return R.run_unit(block, f"W6{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names, EM), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); EM = load_emb(); assert len(EM) == len(dev), "embeddings absents ou incomplets (lancer scripts/v3_embed_dev_frozen.py)"; t0 = time.time()
    if STAGE == "a": names = VARS; block, code = "P2_W6a_selection", "W6a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W6_selected.json"))["variants"]; block, code = "P2_W6b_confirmation", "W6b.1"; reps = range(10, 20); folds = W3c.make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, EM, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
