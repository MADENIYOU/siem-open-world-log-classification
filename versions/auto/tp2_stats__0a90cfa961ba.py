"""Outils statistiques du protocole v3 (TP2). Tout est écrit à la main sur numpy et scipy.

Principe : l'unité statistique est le GABARIT (les logs d'un même gabarit ne sont pas indépendants).
 - intervalles et p-valeurs par ré-échantillonnage de gabarits (bootstrap par grappes), apparié quand on compare deux méthodes ;
 - comparaisons de plusieurs méthodes sur plusieurs blocs (graines x rotations x plis) : Friedman puis Nemenyi, et Holm pour les paires ;
 - tailles d'effet, tendance monotone (attaques par degré), concordance de classements (Kendall).
"""
import numpy as np
from scipy import stats


# ---------------------------------------------------------------- métriques décomposables par gabarit
def group_confusions(y_true, y_pred, groups, n_classes):
    """Matrice de confusion par gabarit : tableau (G, K, K), et la liste des gabarits dans l'ordre."""
    gl, gi = np.unique(groups, return_inverse=True)
    flat = (gi * n_classes + y_true) * n_classes + y_pred
    cm = np.bincount(flat, minlength=len(gl) * n_classes * n_classes).reshape(len(gl), n_classes, n_classes)
    return gl, cm


def macro_f1_from_cm(cm, present_only=True):
    tp = np.diag(cm).astype(float); fp = cm.sum(0) - tp; fn = cm.sum(1) - tp
    den = 2 * tp + fp + fn; f1 = np.where(den > 0, 2 * tp / np.maximum(den, 1), 0.0)
    if present_only:
        keep = cm.sum(1) > 0
        return float(f1[keep].mean()) if keep.any() else float("nan")
    return float(f1.mean())


def group_score_histograms(score, is_unknown, groups, n_bins=400, lo=None, hi=None):
    """Histogrammes (connus, inconnus) du score par gabarit : permet un AUROC par bootstrap de gabarits, rapide."""
    lo = np.nanmin(score) if lo is None else lo; hi = np.nanmax(score) if hi is None else hi
    edges = np.linspace(lo, hi, n_bins + 1); b = np.clip(np.digitize(score, edges) - 1, 0, n_bins - 1)
    gl, gi = np.unique(groups, return_inverse=True)
    hk = np.bincount(gi[~is_unknown] * n_bins + b[~is_unknown], minlength=len(gl) * n_bins).reshape(len(gl), n_bins)
    hu = np.bincount(gi[is_unknown] * n_bins + b[is_unknown], minlength=len(gl) * n_bins).reshape(len(gl), n_bins)
    return gl, hk, hu


def auroc_from_hist(hk, hu):
    """AUROC (score élevé = inconnu) à partir des histogrammes sommés ; égalités comptées pour 1/2."""
    ck, cu = hk.sum(0).astype(float), hu.sum(0).astype(float); nk, nu = ck.sum(), cu.sum()
    if nk == 0 or nu == 0: return float("nan")
    below = np.cumsum(ck) - ck                       # connus strictement sous le bac
    return float(((cu * below).sum() + 0.5 * (cu * ck).sum()) / (nk * nu))


def fpr_at_tpr_from_hist(hk, hu, tpr=0.95):
    """Part des connus acceptés à tort quand on détecte `tpr` des inconnus (score élevé = inconnu)."""
    ck, cu = hk.sum(0).astype(float), hu.sum(0).astype(float)
    if ck.sum() == 0 or cu.sum() == 0: return float("nan")
    tp = np.cumsum(cu[::-1])[::-1] / cu.sum()        # part des inconnus avec score >= bac
    fp = np.cumsum(ck[::-1])[::-1] / ck.sum()
    ok = np.where(tp >= tpr)[0]
    return float(fp[ok.max()]) if len(ok) else 1.0


# ---------------------------------------------------------------- bootstrap par gabarits
def cluster_bootstrap(stat_fn, n_groups, n_boot=2000, seed=0):
    """stat_fn(indices_de_gabarits) -> nombre. Renvoie le vecteur des n_boot valeurs ré-échantillonnées."""
    rng = np.random.default_rng(seed); out = np.empty(n_boot)
    for i in range(n_boot):
        out[i] = stat_fn(rng.integers(0, n_groups, n_groups))
    return out


def paired_cluster_bootstrap(stat_a, stat_b, n_groups, n_boot=2000, seed=0):
    """Mêmes gabarits tirés pour les deux méthodes : distribution de la différence A - B.
    Renvoie (différence observée, IC 95 %, p-valeur bilatérale par inversion du percentile)."""
    rng = np.random.default_rng(seed); full = np.arange(n_groups); obs = stat_a(full) - stat_b(full); d = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n_groups, n_groups); d[i] = stat_a(idx) - stat_b(idx)
    d = d[~np.isnan(d)]
    lo, hi = np.percentile(d, [2.5, 97.5]); p = 2 * min((d <= 0).mean(), (d >= 0).mean()); p = max(p, 1.0 / (len(d) + 1))
    return float(obs), (float(lo), float(hi)), float(min(p, 1.0))


# ---------------------------------------------------------------- plusieurs méthodes, plusieurs blocs
def holm(pvals):
    """Correction de Holm-Bonferroni : p-valeurs ajustées (même ordre que l'entrée)."""
    p = np.asarray(pvals, float); m = len(p); order = np.argsort(p); adj = np.empty(m); run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i]); adj[i] = min(1.0, run)
    return adj


def wilcoxon_paired(a, b):
    """Wilcoxon signé apparié (a et b mesurés sur les mêmes blocs). Renvoie (statistique, p, taille d'effet r de rang bisérié)."""
    a, b = np.asarray(a, float), np.asarray(b, float); d = a - b; d = d[d != 0]
    if len(d) == 0: return 0.0, 1.0, 0.0
    res = stats.wilcoxon(d, zero_method="wilcox", alternative="two-sided", method="auto")
    ranks = stats.rankdata(np.abs(d)); r = (ranks[d > 0].sum() - ranks[d < 0].sum()) / ranks.sum()
    return float(res.statistic), float(res.pvalue), float(r)


def friedman_nemenyi(scores, names=None, higher_is_better=True):
    """scores : (n_blocs, k_méthodes). Friedman global, puis Nemenyi (différence critique à 5 %) et p-valeurs par paires (Nemenyi).
    Renvoie un dictionnaire : rangs moyens, chi2, p, CD, matrice des p-valeurs de Nemenyi."""
    X = np.asarray(scores, float); n, k = X.shape
    ranks = np.vstack([stats.rankdata(-r if higher_is_better else r) for r in X]); avg = ranks.mean(0)
    chi2, p = stats.friedmanchisquare(*[X[:, j] for j in range(k)]) if k >= 3 else (float("nan"), float("nan"))
    q = stats.studentized_range.ppf(0.95, k, np.inf) / np.sqrt(2); cd = q * np.sqrt(k * (k + 1) / (6.0 * n))
    P = np.ones((k, k))
    for i in range(k):
        for j in range(k):
            if i != j:
                z = abs(avg[i] - avg[j]) / np.sqrt(k * (k + 1) / (6.0 * n)); P[i, j] = float(stats.studentized_range.sf(z * np.sqrt(2), k, np.inf))
    return {"names": list(names) if names is not None else list(range(k)), "avg_ranks": avg, "chi2": float(chi2), "p": float(p), "cd": float(cd), "nemenyi_p": P, "n_blocks": n}


# ---------------------------------------------------------------- tailles d'effet, tendances, concordance
def cliffs_delta(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    gt = (a[:, None] > b[None, :]).sum(); lt = (a[:, None] < b[None, :]).sum(); return float((gt - lt) / (len(a) * len(b)))


def monotone_trend(degrees, values):
    """Tendance monotone d'une mesure selon le degré d'attaque : Spearman et pente de Theil-Sen. Renvoie (rho, p, pente)."""
    rho, p = stats.spearmanr(degrees, values); slope = stats.theilslopes(values, degrees)[0]; return float(rho), float(p), float(slope)


def jonckheere(groups_by_degree):
    """Test de Jonckheere-Terpstra (tendance croissante entre degrés ordonnés). Entrée : liste d'échantillons, du plus faible au plus fort degré.
    Renvoie (statistique J, z, p unilatérale croissante)."""
    k = len(groups_by_degree); J = 0.0
    for i in range(k - 1):
        for j in range(i + 1, k):
            a, b = np.asarray(groups_by_degree[i], float), np.asarray(groups_by_degree[j], float)
            J += (b[None, :] > a[:, None]).sum() + 0.5 * (b[None, :] == a[:, None]).sum()
    n = np.array([len(g) for g in groups_by_degree], float); N = n.sum()
    mean = (N * N - (n * n).sum()) / 4.0; var = (N * N * (2 * N + 3) - (n * n * (2 * n + 3)).sum()) / 72.0
    z = (J - mean) / np.sqrt(var); return float(J), float(z), float(stats.norm.sf(z))


def kendall_concordance(rank_lists):
    """Concordance moyenne (tau de Kendall) entre plusieurs classements des mêmes méthodes (un classement par protocole)."""
    taus = [stats.kendalltau(a, b)[0] for i, a in enumerate(rank_lists) for b in rank_lists[i + 1:]]
    return float(np.nanmean(taus))
