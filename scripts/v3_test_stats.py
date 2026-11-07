"""Tests unitaires de src/tp2_stats.py : on vérifie chaque outil sur des cas dont on connaît la réponse. Usage : python scripts/v3_test_stats.py"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from scipy import stats
import tp2_stats as S
rng = np.random.default_rng(0); ok = []
def check(name, cond): ok.append(bool(cond)); print(("OK  " if cond else "ECHEC"), name)
# 1. macro-F1 par matrice de confusion = sklearn
from sklearn.metrics import f1_score, roc_auc_score
yt = rng.integers(0, 5, 3000); yp = np.where(rng.random(3000) < .6, yt, rng.integers(0, 5, 3000)); grp = rng.integers(0, 40, 3000)
gl, cm = S.group_confusions(yt, yp, grp, 5)
check("macro-F1 depuis les confusions par gabarit = sklearn", abs(S.macro_f1_from_cm(cm.sum(0)) - f1_score(yt, yp, average="macro")) < 1e-12)
# 2. AUROC par histogrammes ~ sklearn
unk = rng.random(5000) < .3; sc = rng.normal(0, 1, 5000) + 0.8 * unk; g2 = rng.integers(0, 50, 5000)
gl2, hk, hu = S.group_score_histograms(sc, unk, g2, n_bins=2000)
check("AUROC par histogrammes ~ sklearn (écart < 0,002)", abs(S.auroc_from_hist(hk, hu) - roc_auc_score(unk, sc)) < 2e-3)
# 3. bootstrap par gabarits : IC contient la vraie valeur ; diff appariée détecte un vrai écart et pas une égalité
f = lambda idx: S.macro_f1_from_cm(cm[idx].sum(0)); b = S.cluster_bootstrap(f, len(gl), 400, seed=1)
check("bootstrap par gabarits : IC 95 % contient la valeur observée", np.percentile(b, 2.5) <= f(np.arange(len(gl))) <= np.percentile(b, 97.5))
h = lambda idx: S.macro_f1_from_cm(cm[idx].sum(0)) - 0.15
_, ci, p = S.paired_cluster_bootstrap(f, h, len(gl), 400, seed=2); check("différence appariée : écart de 0,15 détecté (p < 0,01, IC > 0)", p < 0.01 and ci[0] > 0)
_, ci0, p0 = S.paired_cluster_bootstrap(f, f, len(gl), 400, seed=3); check("différence appariée : une méthode contre elle-même, p proche de 1", p0 > 0.5)
# 4. Holm
check("Holm : p ajustées ordonnées et >= p brutes", np.all(S.holm([0.01, 0.04, 0.03]) >= np.array([0.01, 0.04, 0.03])) and abs(S.holm([0.01, 0.04, 0.03])[0] - 0.03) < 1e-12)
# 5. Wilcoxon : vrai écart / pas d'écart (taux de faux positifs)
a = rng.normal(0, 1, 40); check("Wilcoxon : écart réel détecté", S.wilcoxon_paired(a + 1.0, a)[1] < 0.001)
fp = np.mean([S.wilcoxon_paired(x := rng.normal(0, 1, 30), x + rng.normal(0, 1, 30))[1] < 0.05 for _ in range(400)]); check(f"Wilcoxon : faux positifs sous H0 = {fp:.3f} (attendu ~ 0,05)", 0.02 < fp < 0.09)
# 6. Friedman / Nemenyi : méthodes A < B < C nettement séparées
M = np.column_stack([rng.normal(m, 0.3, 30) for m in (0.0, 1.0, 2.0)]); r = S.friedman_nemenyi(M)
check("Friedman : différence globale détectée (p < 1e-6)", r["p"] < 1e-6); check("Nemenyi : A et C séparées, rangs moyens ordonnés", r["nemenyi_p"][0, 2] < 0.001 and r["avg_ranks"][2] < r["avg_ranks"][0])
Z = rng.normal(0, 1, (30, 4)); rz = S.friedman_nemenyi(Z); check("Friedman : aucune différence sous H0 (p > 0,01)", rz["p"] > 0.01)
# 7. tailles d'effet, tendance, concordance
check("Cliff's delta : +1 si tout A > tout B", S.cliffs_delta([3, 4, 5], [0, 1, 2]) == 1.0)
rho, p, slope = S.monotone_trend([1, 2, 3, 4, 5], [1.0, 2.1, 2.9, 4.2, 5.1]); check("tendance monotone : rho = 1 et pente ~ 1", rho > 0.99 and abs(slope - 1) < 0.2)
J, z, pj = S.jonckheere([rng.normal(m, 1, 12) for m in (0, 0.8, 1.6, 2.4)]); check("Jonckheere : tendance croissante détectée (p < 0,01)", pj < 0.01)
check("Kendall : classements identiques = 1", abs(S.kendall_concordance([[1, 2, 3, 4], [1, 2, 3, 4]]) - 1) < 1e-12)
print(f"\n{sum(ok)}/{len(ok)} tests réussis"); sys.exit(0 if all(ok) else 1)
