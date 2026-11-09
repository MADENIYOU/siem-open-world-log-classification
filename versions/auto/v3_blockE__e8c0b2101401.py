"""Bloc E (protocole v3) : calibration. 5 rotations × répétition 0 × 5 plis = 25 unités, SIEVE_00, développement seul, TF-IDF mots + régression logistique (C = 4).
Les gabarits d'entraînement sont partagés : 75 % servent à entraîner (dont 10 % des logs mis de côté comme jeu de calibration « mêmes gabarits », témoin de fuite), 25 % forment le jeu de calibration « gabarits distincts »
(gabarits que le modèle n'a pas vus, comme le test). Méthodes : aucune, température, vector scaling, isotonique, binning (15 bacs), Platt (tous sur la probabilité de la classe prédite ou les logits),
température sur classes cachées pour de faux (variante monde ouvert), température sur mêmes gabarits (fuite), prédiction conforme (90 %). Mesures « classe prédite » sur les logs connus du test :
ECE (15 bacs de même effectif), Brier et log-vraisemblance négative de la correction ; AUROC d'inconnu du MSP calibré. Reprenable. Usage : python scripts/v3_blockE.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize, minimize_scalar
from scipy.special import softmax, logsumexp
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression
import v3_blockA as A, v3_blockC as C, tp2_openset as O, tp2_runner as R
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
ALPHA = 0.10


def ece_eq_mass(conf, correct, bins=15):
    o = np.argsort(conf); c, k = conf[o], correct[o].astype(float); e = 0.0
    for idx in np.array_split(np.arange(len(c)), bins): e += len(idx) / len(c) * abs(k[idx].mean() - c[idx].mean())
    return float(e)


def top_metrics(conf, correct):
    conf = np.clip(conf, 1e-6, 1 - 1e-6); k = correct.astype(float)
    return {"ece": ece_eq_mass(conf, correct), "brier": float(np.mean((conf - k) ** 2)), "nll": float(-np.mean(k * np.log(conf) + (1 - k) * np.log(1 - conf)))}


def fit_temperature(L, yi):
    f = lambda lt: -np.mean(np.take_along_axis(L / np.exp(lt) - logsumexp(L / np.exp(lt), axis=1, keepdims=True), yi[:, None], 1))
    return float(np.exp(minimize_scalar(f, bounds=(np.log(0.05), np.log(10)), method="bounded").x))


def fit_vector(L, yi, K):
    def f(w):
        a, b = w[:K], w[K:]; Z = L * a + b; return -np.mean(np.take_along_axis(Z - logsumexp(Z, axis=1, keepdims=True), yi[:, None], 1)) + 1e-3 * (np.sum((a - 1) ** 2) + np.sum(b ** 2))
    w = minimize(f, np.r_[np.ones(K), np.zeros(K)], method="L-BFGS-B", options={"maxiter": 60}).x; return w[:K], w[K:]


def conformal_q(P, yi):
    s = np.sort(1 - P[np.arange(len(yi)), yi]); n = len(s); k = int(np.ceil((n + 1) * (1 - ALPHA))); return float(s[min(k, n) - 1])


def task(rot, k, dev, tierA):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked]); fold = dev["fold_r0"].values
    te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte = y[te_i]; known = ~np.isin(yte, mid); rng = np.random.default_rng(100 * rot + k)
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": "pli sans assez de logs"}
    grp = dev.group.values[tr_i]; ug = np.unique(grp); cal_g = set(rng.choice(ug, size=max(1, int(0.25 * len(ug))), replace=False)); in_cal = np.array([g in cal_g for g in grp])
    fit_pool = np.where(~in_cal)[0]; leak = np.zeros(len(tr_i), bool); leak[rng.choice(fit_pool, size=int(0.10 * len(fit_pool)), replace=False)] = True; fit_m = ~in_cal & ~leak; cal_m, leak_m = in_cal, leak
    vec = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xf = vec.fit_transform(dev.log.values[tr_i][fit_m]); lr = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xf, y[tr_i][fit_m]); cls = lr.classes_; K = len(cls)
    def logits(idx, texts=None): return lr.decision_function(vec.transform(dev.log.values[idx])) if texts is None else None
    Lc = lr.decision_function(vec.transform(dev.log.values[tr_i][cal_m])); yc = y[tr_i][cal_m]; Ll = lr.decision_function(vec.transform(dev.log.values[tr_i][leak_m])); yl = y[tr_i][leak_m]; Lt = lr.decision_function(vec.transform(dev.log.values[te_i]))
    keepc = np.isin(yc, cls); Lc, yc = Lc[keepc], yc[keepc]; ycI = np.searchsorted(cls, yc); keepl = np.isin(yl, cls); Ll, yl = Ll[keepl], yl[keepl]; ylI = np.searchsorted(cls, yl)
    keept = (~known) | np.isin(yte, cls); Lt, yte, known = Lt[keept], yte[keept], known[keept]                 # un log « connu » dont TOUS les gabarits sont tombés hors de l'entraînement n'a pas de classe apprise : écarté
    ytI = np.where(known, np.searchsorted(cls, np.where(known, yte, cls[0])), -1)
    def evaluate(P_or_conf, kind="P"):
        if kind == "P": pred = P_or_conf.argmax(1); conf = P_or_conf.max(1)
        else: pred, conf = Lt.argmax(1), P_or_conf
        correct = (pred[known] == ytI[known]); m = top_metrics(conf[known], correct); m["auroc_msp"] = float(O.open_metrics(np.nan_to_num(conf), known)["auroc"]); return m
    res = {}; P0 = softmax(Lt, 1); res["aucune"] = evaluate(P0)
    T = fit_temperature(Lc, ycI); res["temperature"] = {**evaluate(softmax(Lt / T, 1)), "T": T}
    a, b = fit_vector(Lc, ycI, K); res["vector_scaling"] = evaluate(softmax(Lt * a + b, 1))
    conf_c = softmax(Lc, 1).max(1); cor_c = (Lc.argmax(1) == ycI); conf_t = P0.max(1)
    iso = IsotonicRegression(out_of_bounds="clip", y_min=0, y_max=1).fit(conf_c, cor_c.astype(float)); res["isotonique"] = evaluate(iso.predict(conf_t), "conf")
    edges = np.quantile(conf_c, np.linspace(0, 1, 16)); edges[0], edges[-1] = -np.inf, np.inf; bidx = np.clip(np.digitize(conf_c, edges) - 1, 0, 14); acc_b = np.array([cor_c[bidx == j].mean() if (bidx == j).any() else np.nan for j in range(15)])
    acc_b = np.where(np.isnan(acc_b), np.nanmean(acc_b), acc_b); res["binning"] = evaluate(acc_b[np.clip(np.digitize(conf_t, edges) - 1, 0, 14)], "conf")
    z = np.log(np.clip(conf_c, 1e-6, 1 - 1e-6) / (1 - np.clip(conf_c, 1e-6, 1 - 1e-6))); pl = LogisticRegression(C=1e6, max_iter=200).fit(z[:, None], cor_c.astype(int)); zt = np.log(np.clip(conf_t, 1e-6, 1 - 1e-6) / (1 - np.clip(conf_t, 1e-6, 1 - 1e-6))); res["platt"] = evaluate(pl.predict_proba(zt[:, None])[:, 1], "conf")
    hid = rng.choice(cls, size=4, replace=False); fm2 = fit_m & ~np.isin(y[tr_i], hid); lr2 = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(vec.transform(dev.log.values[tr_i][fm2]), y[tr_i][fm2])
    Lc2 = lr2.decision_function(vec.transform(dev.log.values[tr_i][cal_m])); isun = np.isin(y[tr_i][cal_m], hid); best, bt = -1, 1.0
    if isun.sum() >= 30 and (~isun).sum() >= 30:
        for t in np.exp(np.linspace(np.log(0.25), np.log(4), 17)):
            au = O.open_metrics(softmax(Lc2 / t, 1).max(1), ~isun)["auroc"]
            if au > best: best, bt = au, t
    res["temperature_classes_cachees"] = {**evaluate(softmax(Lt / bt, 1)), "T": float(bt), "auroc_pseudo": float(best)}
    Tl = fit_temperature(Ll, ylI); res["temperature_memes_gabarits"] = {**evaluate(softmax(Lt / Tl, 1)), "T": Tl}
    cf = {}
    for nm, Lcal, ycal in (("gabarits_distincts", Lc, ycI), ("memes_gabarits", Ll, ylI)):
        q = conformal_q(softmax(Lcal, 1), ycal); sets = softmax(Lt, 1) >= 1 - q; cov = float(sets[known][np.arange(known.sum()), ytI[known]].mean()); cf[nm] = {"q": q, "couverture": cov, "taille_moy": float(sets[known].sum(1).mean()), "vides_connus": float((sets[known].sum(1) == 0).mean()), "vides_inconnus": float((sets[~known].sum(1) == 0).mean())}
    res["conforme"] = cf; res["_info"] = {"n_fit": int(fit_m.sum()), "n_cal": int(cal_m.sum()), "n_leak": int(leak_m.sum()), "n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum())}
    return res


def unit(rot, k, dev, tierA):
    cfg = {"block": "E", "rotation": rot, "repeat": 0, "fold": k, "cap": A.CAP, "C_head": C.C_HEAD, "alpha_conforme": ALPHA, "bins": 15, "calibration_groupes": 0.25, "calibration_memes_gabarits": 0.10, "splits": "groups_v3"}
    return R.run_unit("E_calibration", f"E rot{rot + 1} r0 pli{k}", cfg, lambda: task(rot, k, dev, tierA), code_version="E2")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0)] if "--smoke" in sys.argv else [(rot, k) for k in range(5) for rot in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, k, dev, tierA) for rot, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
