"""Classification hiérarchique de logs en monde ouvert (TP2, étape 6).

Un modèle = une représentation (TF-IDF de mots, vecteurs de mots...) + un classifieur PLAT (une tête sur les classes connues)
+ un classifieur HIÉRARCHIQUE (une tête famille + une tête par famille) + des scores d'incertitude pour rejeter les inconnus.
Tout est appris sur les classes CONNUES ; les classes masquées n'apparaissent jamais à l'apprentissage, ni dans le vocabulaire.
"""
import numpy as np
from scipy.special import logsumexp
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score


def tree_distance(a, b, child2fam):
    """0 : même classe ; 1 : autre classe de la même famille ; 2 : autre famille."""
    return 0 if a == b else (1 if child2fam[a] == child2fam[b] else 2)


class OpenSetModel:
    def __init__(self, rep, known, child2fam, C=4.0, seed=42, n_ens=5, max_iter=300):
        self.rep = rep; self.known = list(known); self.child2fam = child2fam; self.C = C; self.seed = seed
        self.n_ens = n_ens; self.max_iter = max_iter
        self.fams = sorted({child2fam[c] for c in self.known})

    # --- représentation (ajustée sur les classes connues seulement) ---------------------------------------------
    def _fit_rep(self, tr_txt, known_all_txt, word_tokens=None):
        from tp2_logtext import tokenize as _word_tokens                                    # fonction de module (sérialisable), pipeline A
        if self.rep == "tfidf":
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vec_ = TfidfVectorizer(analyzer=_word_tokens, min_df=2, sublinear_tf=True, dtype=np.float32).fit(tr_txt)
        elif self.rep == "sg_idf":
            from sklearn.preprocessing import StandardScaler
            from tp2_vec import DocEmbedder
            self.emb_ = DocEmbedder(kind="w2v_sg", weighting="idf", workers=8, seed=self.seed).fit(known_all_txt)
            self.sc_ = StandardScaler().fit(self.emb_.transform(tr_txt))
        elif self.rep == "char35":
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vec_ = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=3, max_features=300000, sublinear_tf=True, dtype=np.float32).fit(tr_txt)
        else:
            raise ValueError(self.rep)

    def transform(self, txt):
        if self.rep == "sg_idf":
            return self.sc_.transform(self.emb_.transform(txt))
        return self.vec_.transform(txt)

    def _lr(self, X, y, seed=None):
        return LogisticRegression(C=self.C, max_iter=self.max_iter, random_state=self.seed if seed is None else seed).fit(X, y)

    # --- apprentissage ------------------------------------------------------------------------------------------
    def fit(self, tr_txt, y_tr, known_all_txt, word_tokens=None):
        y_tr = np.asarray(y_tr); self._fit_rep(tr_txt, known_all_txt, word_tokens); X = self.transform(tr_txt)
        self.flat_ = self._lr(X, y_tr)                                                      # tête plate sur les classes connues
        fam = np.array([self.child2fam[c] for c in y_tr]); self.fam_ = self._lr(X, fam)     # tête famille
        self.child_ = {}
        for f in self.fams:                                                                  # une tête fine par famille ayant au moins 2 classes connues
            kids = [c for c in self.known if self.child2fam[c] == f]
            if len(kids) >= 2:
                m = fam == f; self.child_[f] = self._lr(X[m], y_tr[m])
            else:
                self.child_[f] = kids[0]                                                    # une seule classe connue : probabilité conditionnelle = 1
        self.centroids_ = {}                                                                 # prototypes : un centroïde normalisé par classe connue
        for c in self.known:
            m = np.where(y_tr == c)[0]; v = np.asarray(X[m].mean(0)).ravel(); self.centroids_[c] = v / (np.linalg.norm(v) + 1e-12)
        rng = np.random.default_rng(self.seed); self.ens_ = []                               # ensemble : modèles plats sur rééchantillons bootstrap
        for b in range(self.n_ens):
            idx = rng.integers(0, X.shape[0], X.shape[0]); self.ens_.append(self._lr(X[idx], y_tr[idx], seed=self.seed + b + 1))
        return self

    # --- prédiction et scores ----------------------------------------------------------------------------------
    def scores(self, txt):
        X = self.transform(txt); cls = list(self.flat_.classes_)
        logits = self.flat_.decision_function(X); P = self.flat_.predict_proba(X)
        out = {"classes": cls, "pred_flat": np.array(cls)[P.argmax(1)], "P_flat": P}
        # tête hiérarchique : p(classe) = p(famille) x p(classe | famille), donc enfant toujours dans la famille prédite
        PF = self.fam_.predict_proba(X); famc = list(self.fam_.classes_); PH = np.zeros((X.shape[0], len(cls)))
        for j, c in enumerate(cls):
            f = self.child2fam[c]; pf = PF[:, famc.index(f)] if f in famc else np.zeros(X.shape[0]); ch = self.child_[f]
            pc = np.ones(X.shape[0]) if isinstance(ch, str) else ch.predict_proba(X)[:, list(ch.classes_).index(c)]
            PH[:, j] = pf * pc
        out["P_hier"] = PH; out["pred_hier"] = np.array(cls)[PH.argmax(1)]
        out["pred_family"] = np.array(famc)[PF.argmax(1)]; out["P_family"] = PF
        # scores de « connu » (plus grand = plus connu)
        out["msp"] = P.max(1)                                                                # probabilité softmax maximale
        out["energy"] = logsumexp(logits, axis=1)                                            # -energy : grand si un logit domine
        from sklearn.preprocessing import normalize
        cent = np.vstack([self.centroids_[c] for c in cls]); Xn = normalize(X)
        out["proto"] = np.asarray(Xn @ cent.T).max(1)                                        # cosinus au centroïde le plus proche
        out["ens_msp"] = np.mean([m.predict_proba(X) for m in self.ens_], axis=0).max(1) if self.ens_ else out["msp"]
        out["hier_msp"] = PH.max(1); out["fam_msp"] = PF.max(1)
        return out


# --- métriques ---------------------------------------------------------------------------------------------------
def open_metrics(score, is_known, correct=None):
    """score : plus grand = plus connu ; is_known : booléens ; correct : prédiction exacte (pour OSCR)."""
    s = np.asarray(score, dtype=float); k = np.asarray(is_known, dtype=bool)
    out = {"auroc": float(roc_auc_score(k, s)), "aupr_in": float(average_precision_score(k, s))}
    thr = np.quantile(s[k], 0.05)                                  # on garde 95 % des connus
    out["fpr95"] = float((s[~k] >= thr).mean())
    out["reject_known"] = float((s[k] < thr).mean())               # = 5 % par construction
    if correct is not None:
        c = np.asarray(correct, dtype=bool); order = np.argsort(-s); kk = k[order]; cc = (c & k)[order]
        ccr = np.cumsum(cc) / max(k.sum(), 1); fpr = np.cumsum(~kk) / max((~k).sum(), 1)
        out["oscr"] = float(np.trapezoid(ccr, fpr))
    return out


def ece(conf, correct, bins=10):
    conf = np.asarray(conf); correct = np.asarray(correct, dtype=float); e = 0.0
    for lo in np.linspace(0, 1, bins, endpoint=False):
        m = (conf > lo) & (conf <= lo + 1 / bins)
        if m.any():
            e += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return float(e)
