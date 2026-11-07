"""Bloc C (protocole v3) : détection d'inconnus. 5 rotations de classes masquées x 5 répétitions x 5 plis de groupes (P2) = 125 unités, SIEVE_00, développement seul
(le test v2 n'est JAMAIS lu), 400 logs au plus par gabarit. Entraînement sur les logs des 24 classes connues ; test = logs du pli (connus = positifs, classes masquées = inconnus).
Tous les scores : plus grand = plus connu. Méthodes de la vision ADAPTÉES à des vecteurs signés (voir D11). Reprenable : une unité = (rotation, répétition, pli).
Usage : python scripts/v3_blockC.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.special import logsumexp, softmax
from scipy.stats import rankdata, weibull_min
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.preprocessing import normalize
from sklearn.linear_model import LogisticRegression
from sklearn.covariance import LedoitWolf
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import LocalOutlierFactor, NearestNeighbors
from sklearn.ensemble import IsolationForest
from sklearn.metrics import roc_auc_score
import v3_blockA as A, v3_blockB as B, tp2_openset as O, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 4
ROT = json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["rotations"]; C_HEAD, SVD_DIM = 4.0, 100
BYCLASS = ["msp", "energy", "maha_class", "knn10", "tmpl_radius"]


def lw_prec(X):
    return LedoitWolf().fit(X).precision_


def maha2(Z, mu, prec):
    d = Z - mu; return np.einsum("ij,jk,ik->i", d, prec, d)


def openmax_score(Ltr, ytr_idx, Lte, K, alpha=5, tail=20):
    mav, params = [], []
    pred = Ltr.argmax(1)
    for j in range(K):
        m = (ytr_idx == j) & (pred == j); mu = Ltr[m].mean(0) if m.any() else Ltr[ytr_idx == j].mean(0); mav.append(mu)
        d = np.sort(np.linalg.norm(Ltr[m] - mu, axis=1))[::-1][:tail] if m.sum() >= 5 else np.array([1.0, 1.1, 1.2, 1.3, 1.4])
        try: c, loc, sc = weibull_min.fit(d, floc=0); params.append((c, sc))
        except Exception: params.append((2.0, float(d.mean()) + 1e-6))
    mav = np.array(mav); n = Lte.shape[0]; cdf = np.zeros((n, K))
    for j in range(K): cdf[:, j] = weibull_min.cdf(np.linalg.norm(Lte - mav[j], axis=1), params[j][0], 0, params[j][1])
    order = np.argsort(-Lte, axis=1); w = np.ones((n, K)); rows = np.arange(n)
    for i in range(1, alpha + 1): j = order[:, i - 1]; w[rows, j] = 1 - ((alpha - i) / alpha) * (1 - cdf[rows, j])
    vhat = Lte * w; v0 = (Lte * (1 - w)).sum(1); full = np.hstack([vhat, v0[:, None]]); pu = softmax(full, axis=1)[:, -1]
    return 1 - pu


def task(rot, r, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(ROT[rot]); mid = np.array([classes.index(c) for c in masked if c in classes])
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values
    te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": f"pli sans assez de logs (connus {int(known.sum())}, inconnus {int((~known).sum())})"}
    rng = np.random.default_rng(r + 100 * rot + 10 * k)
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = word.fit_transform(dev.log.values[tr_i]); Xte = word.transform(dev.log.values[te_i])
    lr = LogisticRegression(C=C_HEAD, max_iter=300).fit(Xtr, ytr); cls_ids = lr.classes_; K = len(cls_ids); yi = np.searchsorted(cls_ids, ytr)
    L = lr.decision_function(Xte); P = lr.predict_proba(Xte); Ltr = lr.decision_function(Xtr); S = {}
    S["msp"] = P.max(1); S["maxlogit"] = L.max(1); S["energy"] = logsumexp(L, axis=1); S["negent"] = (P * np.log(P + 1e-12)).sum(1)
    ens = []
    for b in range(5): ib = rng.integers(0, len(ytr), len(ytr)); ens.append(LogisticRegression(C=C_HEAD, max_iter=300).fit(Xtr[ib], ytr[ib]).predict_proba(Xte))
    S["ens_msp"] = np.mean(ens, axis=0).max(1)
    PH, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C_HEAD); S["hier_msp"] = PH.max(1); S["fam_msp"] = pf.max(1)
    S["openmax"] = openmax_score(Ltr, yi, L, K)
    svd = TruncatedSVD(SVD_DIM, random_state=r).fit(Xtr); Ztr = normalize(svd.transform(Xtr)); Zte = normalize(svd.transform(Xte)); mu = np.vstack([Ztr[yi == j].mean(0) for j in range(K)])
    S["proto_cos"] = (Zte @ normalize(mu).T).max(1)
    centered = Ztr - mu[yi]; P_sh = lw_prec(centered); d_sh = np.column_stack([maha2(Zte, mu[j], P_sh) for j in range(K)]); S["maha_shared"] = -d_sh.min(1)
    d_cl = []
    for j in range(K):
        Zc = Ztr[yi == j]; Pj = lw_prec(Zc) if len(Zc) >= 20 else P_sh; d_cl.append(maha2(Zte, mu[j], Pj))
    S["maha_class"] = -np.column_stack(d_cl).min(1)
    mu0 = Ztr.mean(0); P0 = lw_prec(Ztr); S["maha_rel"] = -(d_sh.min(1) - maha2(Zte, mu0, P0))
    nn = NearestNeighbors(n_neighbors=10, algorithm="brute").fit(Ztr); dist = nn.kneighbors(Zte)[0]; S["knn1"] = -dist[:, 0]; S["knn10"] = -dist[:, 9]
    pca = PCA(30, random_state=r).fit(Ztr); S["pca_resid"] = -np.linalg.norm(Zte - pca.inverse_transform(pca.transform(Zte)), axis=1)
    LLk = np.full((len(te_i), K), -np.inf)
    for j in range(K):
        Zc = Ztr[yi == j]; LLk[:, j] = GaussianMixture(n_components=max(1, min(3, len(Zc) // 10)), covariance_type="diag", reg_covar=1e-3, random_state=r).fit(Zc).score_samples(Zte)
    S["gmm_lik"] = LLk.max(1)
    sub = rng.permutation(len(Ztr))[:8000]; S["lof"] = LocalOutlierFactor(n_neighbors=20, novelty=True).fit(Ztr[sub]).score_samples(Zte); S["iforest"] = IsolationForest(n_estimators=100, random_state=r).fit(Ztr[sub]).score_samples(Zte)
    grp = dev.group.values[tr_i]; gl, gi = np.unique(grp, return_inverse=True); Cg = normalize(np.vstack([Ztr[gi == g].mean(0) for g in range(len(gl))])); rad = np.array([max(0.02, np.percentile(1 - Ztr[gi == g] @ Cg[g], 90)) for g in range(len(gl))])
    sims = Zte @ Cg.T; jn = sims.argmax(1); dn = 1 - sims[np.arange(len(jn)), jn]; S["tmpl_dist"] = -dn; S["tmpl_radius"] = -dn / (rad[jn] + 0.05)
    lz = LogisticRegression(C=10, max_iter=300).fit(Ztr, ytr); W, b = lz.coef_, lz.intercept_; Lz = Zte @ W.T + b; Lztr = Ztr @ W.T + b; S["energy_z"] = logsumexp(Lz, axis=1)
    keep = int(round(0.35 * SVD_DIM)); idx = np.argpartition(-np.abs(Zte), keep, axis=1)[:, :keep]; msk = np.zeros_like(Zte); np.put_along_axis(msk, idx, 1.0, axis=1); Hp = Zte * msk; s1, s2 = np.abs(Zte).sum(1), np.abs(Hp).sum(1) + 1e-12
    S["ash_s"] = logsumexp((Hp * np.exp(s1 / s2)[:, None]) @ W.T + b, axis=1); S["scale"] = logsumexp((Hp * (s1 / s2)[:, None]) @ W.T + b, axis=1)
    contrib = W * Ztr.mean(0)[None, :]; Wd = W * (contrib >= np.quantile(contrib, 0.7)); S["dice"] = logsumexp(Zte @ Wd.T + b, axis=1)
    bank = Ztr[sub].astype(np.float32); sm = Zte.astype(np.float32) @ bank.T; guide = np.partition(sm, -10, axis=1)[:, -10:].mean(1); S["nnguide"] = S["energy_z"] * guide
    predz = Lz.argmax(1); okz = Lztr.argmax(1) == yi; mus = np.vstack([Ztr[(yi == j) & okz].mean(0) if ((yi == j) & okz).any() else mu[j] for j in range(K)]); S["she"] = (Zte * mus[predz]).sum(1)
    o = -np.linalg.pinv(W) @ b; Xo = (Ztr - o)[sub]; vt = np.linalg.svd(Xo, full_matrices=False)[2]; Pm = vt[:50].T
    resid = lambda Z: np.linalg.norm((Z - o) - ((Z - o) @ Pm) @ Pm.T, axis=1); alpha = Lztr.max(1).mean() / (resid(Ztr[sub]).mean() + 1e-12); S["vim"] = S["energy_z"] - alpha * resid(Zte)
    S["rank_mean3"] = np.mean([rankdata(S[n]) / len(te_i) for n in ("msp", "maha_shared", "knn10")], axis=0)
    out, byc = {}, {s: {} for s in BYCLASS}
    for n, v in S.items():
        v = np.nan_to_num(np.asarray(v, float), nan=-1e9, posinf=1e9, neginf=-1e9); m = O.open_metrics(v, known); out[n] = {"auroc": m["auroc"], "fpr95": m["fpr95"], "aupr_in": m["aupr_in"]}
        if n in byc:
            for c in mid:
                mk = known | (yte == c)
                if (yte == c).sum() >= 30: byc[n][classes[c]] = [float(roc_auc_score(known[mk], v[mk])), int((yte == c).sum())]
    return {"scores": out, "by_class": byc, "info": {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "n_train": int(len(tr_i)), "closed_acc": float((lr.predict(Xte)[known] == yte[known]).mean()), "masked": sorted(masked), "n_templates_train": int(len(gl))}}


def unit(rot, r, k, dev, tierA):
    cfg = {"block": "C", "rotation": rot, "repeat": r, "fold": k, "cap": A.CAP, "svd": SVD_DIM, "C_head": C_HEAD, "file": "SIEVE_00", "splits": "groups_v3"}
    return R.run_unit("C_inconnus", f"C rot{rot + 1} r{r} pli{k}", cfg, lambda: task(rot, r, k, dev, tierA), code_version="C1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0, 0)] if "--smoke" in sys.argv else [(rot, r, k) for rot in range(5) for r in range(A.NREP) for k in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, r, k, dev, tierA) for rot, r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
