"""Bloc B (protocole v3) : classifieurs sous P2 (5 plis de groupes x 5 répétitions), SIEVE_00, développement seul (le test v2 n'est jamais lu), 400 logs au plus par gabarit.
Familles de méthodes : plats (SVM, régression logistique), hiérarchique local (+ repli sur la famille), voisinage et prototypes (kNN, centroïde, k-means par classe, gabarits-prototypes), Naive Bayes,
clustering de types variés dans l'espace SVD(100) du TF-IDF : par classe (k-means, mélange gaussien, Ward) et global non supervisé avec étiquette majoritaire (k-means, Birch, DBSCAN, HDBSCAN).
Reprenable : une unité = (répétition, pli). Usage : python scripts/v3_blockB.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB
from sklearn.neighbors import KNeighborsClassifier, NearestCentroid, NearestNeighbors
from sklearn.cluster import KMeans, MiniBatchKMeans, AgglomerativeClustering, DBSCAN, HDBSCAN, Birch
from sklearn.mixture import GaussianMixture
from sklearn.metrics import f1_score, accuracy_score, pairwise_distances_argmin
import v3_blockA as A, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 5
TAX = json.load(open(ROOT / "artifacts" / "data" / "taxonomy_and_rotations_v1.json"))["taxonomy"]; FAMS = sorted(TAX); TAU_REPLI, SVD_DIM = 0.5, 100
MODELS = ["svm_word", "lr_word", "hier_lr", "hier_repli", "knn5", "knn15", "centroid", "kmeans_pc3", "kmeans_pc10", "tmpl_proto", "nb_word", "gmm_pc3", "ward_pc5", "kmeans_g60", "kmeans_g150", "birch_g150", "dbscan_sub", "dbscan_sub_rej", "hdbscan_sub", "hdbscan_sub_rej"]


def nearest_proto(Zte, P, lab):
    return lab[pairwise_distances_argmin(Zte, P)]


def proto_perclass(Z, y, k, kind, seed):
    P, lab = [], []
    for c in np.unique(y):
        Zc = Z[y == c]
        if kind == "kmeans": cen = KMeans(n_clusters=min(k, len(Zc)), n_init=3, random_state=seed).fit(Zc).cluster_centers_
        else:                                                                                   # Ward : au plus 1500 logs par classe, centroïdes des k groupes
            Zs = Zc[np.random.default_rng(seed).permutation(len(Zc))[:1500]]; kk = min(k, len(Zs)); lb = AgglomerativeClustering(n_clusters=kk, linkage="ward").fit_predict(Zs) if len(Zs) > 1 else np.zeros(1, int)
            cen = np.vstack([Zs[lb == j].mean(0) for j in np.unique(lb)])
        P.append(cen); lab += [c] * len(cen)
    return np.vstack(P), np.array(lab)


def majority(labels_cluster, y, n_clusters):
    out = np.full(n_clusters, -1)
    for j in range(n_clusters):
        m = labels_cluster == j
        if m.any(): out[j] = np.bincount(y[m]).argmax()
    return out


def hier_probs(Xtr, ytr, Xte, fam_of, nfam, ncls, C=10):
    famclf = LogisticRegression(C=C, max_iter=300).fit(Xtr, fam_of[ytr]); pf = np.zeros((Xte.shape[0], nfam)); pf[:, famclf.classes_] = famclf.predict_proba(Xte); P = np.zeros((Xte.shape[0], ncls))
    for f in range(nfam):
        cl = [c for c in np.where(fam_of == f)[0] if (ytr == c).any()]
        if not cl: continue
        if len(cl) == 1: P[:, cl[0]] = pf[:, f]; continue
        m = np.isin(ytr, cl); clf = LogisticRegression(C=C, max_iter=300).fit(Xtr[m], ytr[m]); pc = clf.predict_proba(Xte)
        for j, c in enumerate(clf.classes_): P[:, c] = pf[:, f] * pc[:, j]
    return P, pf


def density_assign(Zs, ys, Zte, kind, seed):
    """DBSCAN / HDBSCAN sur un sous-échantillon stratifié ; test : classe majoritaire du groupe du plus proche point groupé, rejet (-1) si trop loin."""
    nn = NearestNeighbors(n_neighbors=6).fit(Zs); d5 = nn.kneighbors(Zs)[0][:, 5]
    if kind == "dbscan": eps = float(np.percentile(d5, 75)); lb = DBSCAN(eps=eps, min_samples=5).fit(Zs); labels = lb.labels_; keep = np.zeros(len(Zs), bool); keep[lb.core_sample_indices_] = True; thr = eps
    else: labels = HDBSCAN(min_cluster_size=15, min_samples=5).fit(Zs).labels_; keep = labels >= 0; thr = None
    if not (labels[keep] >= 0).any(): return np.full(len(Zte), -1), np.full(len(Zte), -1), {"n_clusters": 0, "noise": 1.0}
    ncl = labels.max() + 1; maj = majority(labels[labels >= 0], ys[labels >= 0], 0) if False else None
    cl_lab = np.full(ncl, -1)
    for j in range(ncl): cl_lab[j] = np.bincount(ys[labels == j]).argmax()
    Zk, lk = Zs[keep], labels[keep]; nk = NearestNeighbors(n_neighbors=2).fit(Zk)
    if thr is None: thr = float(np.percentile(nk.kneighbors(Zk)[0][:, 1], 95))
    d, ix = NearestNeighbors(n_neighbors=1).fit(Zk).kneighbors(Zte); force = cl_lab[lk[ix[:, 0]]]; pred = np.where(d[:, 0] <= thr, force, -1)      # force : sans rejet ; pred : rejet si trop loin
    return force, pred, {"n_clusters": int(ncl), "noise": float((labels < 0).mean()), "thr": thr, "dist_mediane_test": float(np.median(d[:, 0]))}


def task(r, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; tierA_ids = [classes.index(c) for c in tierA]; ncls = len(classes)
    fam_of = np.array([[f for f in FAMS if c in TAX[f]][0] for c in classes]); fam_of = np.array([FAMS.index(f) for f in fam_of])
    fold = dev[f"fold_r{r}"].values; te_i = np.where(fold == k)[0]; tr_i = np.where(fold != k)[0]; ytr, yte = y[tr_i], y[te_i]; grp = dev.group.values[tr_i]
    word = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = word.fit_transform(dev.log.values[tr_i]); Xte = word.transform(dev.log.values[te_i])
    svd = TruncatedSVD(SVD_DIM, random_state=r).fit(Xtr); Ztr = normalize(svd.transform(Xtr)); Zte = normalize(svd.transform(Xte))
    res, extra = {}, {}

    def record(name, pred, t0, note=None):
        pred = np.asarray(pred); ok = pred >= 0; fp = np.where(ok, fam_of[np.maximum(pred, 0)], -1); ft = fam_of[yte]
        dist = np.where(pred == yte, 0, np.where(ok & (fp == ft), 1, 2)); lab = [c for c in tierA_ids if (yte == c).any()]
        res[name] = {"f1A": float(f1_score(yte, pred, labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte, pred, labels=np.unique(yte), average="macro", zero_division=0)), "acc": float(accuracy_score(yte, pred)),
                     "f1_fam": float(f1_score(ft, fp, labels=np.unique(ft), average="macro", zero_division=0)), "tree_dist": float(dist.mean()), "reject": float((~ok).mean()), "seconds": round(time.time() - t0, 1)}
        if note: res[name]["note"] = note
    t0 = time.time(); record("svm_word", LinearSVC(C=1).fit(Xtr, ytr).predict(Xte), t0)
    t0 = time.time(); lr = LogisticRegression(C=10, max_iter=300).fit(Xtr, ytr); record("lr_word", lr.predict(Xte), t0)
    t0 = time.time(); P, pf = hier_probs(Xtr, ytr, Xte, fam_of, len(FAMS), ncls); record("hier_lr", P.argmax(1), t0)
    t0 = time.time(); mx = P.max(1); cov = mx >= TAU_REPLI; pred_cls = P.argmax(1); fam_ans = np.where(cov, fam_of[pred_cls], pf.argmax(1)); ft = fam_of[yte]
    res["hier_repli"] = {"couverture": float(cov.mean()), "acc_classe_couverts": float((pred_cls[cov] == yte[cov]).mean()) if cov.any() else float("nan"), "acc_famille_tous": float((fam_ans == ft).mean()), "acc_famille_sans_repli": float((fam_of[pred_cls] == ft).mean()), "tau": TAU_REPLI, "seconds": round(time.time() - t0, 1)}
    for kk in (5, 15): t0 = time.time(); record(f"knn{kk}", KNeighborsClassifier(n_neighbors=kk, metric="cosine", algorithm="brute").fit(Xtr, ytr).predict(Xte), t0)
    t0 = time.time(); record("centroid", NearestCentroid().fit(Xtr, ytr).predict(Xte), t0)
    for kk in (3, 10): t0 = time.time(); Pp, lp = proto_perclass(Ztr, ytr, kk, "kmeans", r); record(f"kmeans_pc{kk}", nearest_proto(Zte, Pp, lp), t0)
    t0 = time.time(); gl, gi = np.unique(grp, return_inverse=True); Gm = sparse.csr_matrix((np.ones(len(gi)), (gi, np.arange(len(gi)))), shape=(len(gl), len(gi))); Xg = normalize(Gm @ Xtr); gcls = np.array([np.bincount(ytr[gi == j]).argmax() for j in range(len(gl))])
    record("tmpl_proto", gcls[np.asarray((Xte @ Xg.T).todense()).argmax(1)], t0, note=f"{len(gl)} gabarits d'entraînement")
    t0 = time.time(); record("nb_word", ComplementNB(alpha=0.3).fit(Xtr, ytr).predict(Xte), t0)
    t0 = time.time(); cls_present = np.unique(ytr); LL = np.full((len(te_i), ncls), -np.inf)
    for c in cls_present:
        Zc = Ztr[ytr == c]; gm = GaussianMixture(n_components=max(1, min(3, len(Zc) // 10)), covariance_type="diag", reg_covar=1e-3, random_state=r).fit(Zc); LL[:, c] = gm.score_samples(Zte)
    record("gmm_pc3", LL.argmax(1), t0)
    t0 = time.time(); Pw, lw = proto_perclass(Ztr, ytr, 5, "ward", r); record("ward_pc5", nearest_proto(Zte, Pw, lw), t0)
    for K in (60, 150):
        t0 = time.time(); km = MiniBatchKMeans(n_clusters=K, batch_size=4096, n_init=3, random_state=r).fit(Ztr); lab = majority(km.labels_, ytr, K); record(f"kmeans_g{K}", lab[km.predict(Zte)], t0)
    t0 = time.time(); br = Birch(threshold=0.5, n_clusters=150).fit(Ztr); lab = majority(br.labels_, ytr, 150); record("birch_g150", lab[br.predict(Zte)], t0)
    rng = np.random.default_rng(r); sub = np.concatenate([rng.permutation(np.where(ytr == c)[0])[:270] for c in cls_present])
    for kind in ("dbscan", "hdbscan"):
        t0 = time.time(); force, pred, inf = density_assign(Ztr[sub], ytr[sub], Zte, kind, r); record(f"{kind}_sub", force, t0, note=json.dumps(inf)); record(f"{kind}_sub_rej", pred, t0)
    res["_info"] = {"n_train": int(len(tr_i)), "n_test": int(len(te_i)), "n_test_groups": int(len(set(dev.group.values[te_i]))), "n_train_templates": int(len(gl))}
    return res


def unit(r, k, dev, tierA):
    cfg = {"block": "B", "repeat": r, "fold": k, "cap": A.CAP, "models": MODELS, "svd": SVD_DIM, "tau_repli": TAU_REPLI, "file": "SIEVE_00", "splits": "groups_v3"}
    return R.run_unit("B_classification", f"B P2 r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA), code_version="B2")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0)] if "--smoke" in sys.argv else [(r, k) for r in range(A.NREP) for k in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
