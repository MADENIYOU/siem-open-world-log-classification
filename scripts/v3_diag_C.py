"""Diagnostic de OpenMax et de LOF (AUROC sous 0,5 au bloc C1). Sur 15 unités (3 par rotation), reprend les données du bloc C et décompose les deux scores.
LOF : composantes (sparsité propre, densité du voisinage, rapport) et sensibilité à k et à la taille de la banque. OpenMax : version C1 (formule lue à l'envers) contre la version du code de référence des auteurs."""
import sys, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from scipy.special import softmax
from scipy.stats import weibull_min
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import LocalOutlierFactor, NearestNeighbors
from sklearn.metrics import roc_auc_score
import v3_blockA as A, v3_blockC as C
warnings.filterwarnings("ignore")
def openmax_ref(Ltr, yi, Lte, K, alpha=5, tail=20):
    """Code de référence de Bendale et Boult : v_hat_i = v_i (1 - w_i * (alpha+1-rang)/alpha) avec w = CDF de Weibull (probabilité d'être dans la queue, donc « loin du signe moyen de la classe »)."""
    pred = Ltr.argmax(1); mav, par = [], []
    for j in range(K):
        m = (yi == j) & (pred == j); mu = Ltr[m].mean(0) if m.any() else Ltr[yi == j].mean(0); mav.append(mu)
        d = np.sort(np.linalg.norm(Ltr[m] - mu, axis=1))[::-1][:tail] if m.sum() >= 5 else np.array([1., 1.1, 1.2, 1.3, 1.4]); c, loc, sc = weibull_min.fit(d, floc=0); par.append((c, sc))
    mav = np.array(mav); n = Lte.shape[0]; cdf = np.column_stack([weibull_min.cdf(np.linalg.norm(Lte - mav[j], axis=1), par[j][0], 0, par[j][1]) for j in range(K)])
    order = np.argsort(-Lte, axis=1); rows = np.arange(n); aw = np.zeros((n, K))
    for i in range(1, alpha + 1): aw[rows, order[:, i - 1]] = (alpha + 1 - i) / alpha
    shift = Lte - Lte.min(1, keepdims=True)                                   # activations positives (le code de référence travaille sur des activations >= 0)
    vhat = shift * (1 - cdf * aw); v0 = (shift * cdf * aw).sum(1); return 1 - softmax(np.hstack([vhat, v0[:, None]]), axis=1)[:, -1]
def lof_parts(Zbank, Zte, k):
    nn = NearestNeighbors(n_neighbors=k).fit(Zbank); dbank, ibank = nn.kneighbors(Zbank, n_neighbors=k + 1); kdist = dbank[:, -1]; lrd_bank = 1 / (np.mean(np.maximum(dbank[:, 1:], kdist[ibank[:, 1:]]), axis=1) + 1e-10)
    d, i = nn.kneighbors(Zte); lrd_x = 1 / (np.mean(np.maximum(d, kdist[i]), axis=1) + 1e-10); return {"sparsite_propre": 1 / lrd_x, "densite_voisinage": lrd_bank[i].mean(1), "lof": lrd_bank[i].mean(1) / lrd_x, "k_distance": d[:, -1]}
dev, tierA = A.load(); rows = []; rng = np.random.default_rng(0)
for rot in range(5):
    for (r, k) in [(0, 0), (1, 2), (2, 4)]:
        ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked]); fold = dev[f"fold_r{r}"].values
        te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid)
        w = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = w.fit_transform(dev.log.values[tr_i]); Xte = w.transform(dev.log.values[te_i])
        lr = LogisticRegression(C=4.0, max_iter=300).fit(Xtr, ytr); K = len(lr.classes_); yi = np.searchsorted(lr.classes_, ytr); Ltr, L = lr.decision_function(Xtr), lr.decision_function(Xte)
        svd = TruncatedSVD(100, random_state=r).fit(Xtr); Ztr = normalize(svd.transform(Xtr)); Zte = normalize(svd.transform(Xte)); out = {"rot": rot + 1, "r": r, "k": k}
        out["openmax_C1"] = roc_auc_score(known, C.openmax_score(Ltr, yi, L, K)); out["openmax_ref"] = roc_auc_score(known, openmax_ref(Ltr, yi, L, K))
        sub = rng.permutation(len(Ztr))[:8000]
        for nm, bank, kk in (("lof_8000_k20", Ztr[sub], 20), ("lof_complet_k20", Ztr, 20), ("lof_8000_k5", Ztr[sub], 5), ("lof_8000_k50", Ztr[sub], 50)):
            p = lof_parts(bank, Zte, kk); out[nm] = roc_auc_score(known, -p["lof"])
            if nm == "lof_8000_k20":
                out["part_sparsite_propre"] = roc_auc_score(known, -p["sparsite_propre"]); out["part_densite_voisinage"] = roc_auc_score(known, p["densite_voisinage"]); out["part_k_distance"] = roc_auc_score(known, -p["k_distance"])
                lo = LocalOutlierFactor(n_neighbors=20, novelty=True).fit(bank); out["controle_sklearn_egal_formule"] = bool(np.allclose(-lo.score_samples(Zte), p["lof"], rtol=1e-3))
        rows.append(out)
import pandas as pd
df = pd.DataFrame(rows); df.to_csv(ROOT / "artifacts" / "results" / "v3" / "C_diagnostic_openmax_lof.csv", index=False); pd.set_option("display.width", 200)
print(df.drop(columns=["controle_sklearn_egal_formule"]).round(3).to_string(index=False)); print("\nmoyennes sur 15 unités :\n", df.drop(columns=["rot", "r", "k", "controle_sklearn_egal_formule"]).mean().round(3).to_string()); print("\nformule du LOF recalculée = sklearn dans", int(df.controle_sklearn_egal_formule.sum()), "unités sur", len(df))
