"""Vague 4 (D34, HZ1-HZ6) : F7 axes objet × action, F20 bagging par gabarits, F10 pondération des gabarits difficiles, modes brut et M50, conditions toutes et abs8. Dev SIEVE_00 seul.
Étape a : répétitions 0-4 ; étape b : répétitions 10-14, variantes de artifacts/results/v3/W4_selected.json. Reprenable. Usage : python scripts/v3_phase2_W4.py a|b [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np
from joblib import Parallel, delayed
from scipy.special import softmax
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
import v3_blockA as A, tp2_runner as R, v3_phase2_W3 as W3
import v3_phase2_W3c as W3c
warnings.filterwarnings("ignore")
STAGE = sys.argv[1]; JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 6
VARS = ["AXE0", "AXE05", "AXE1", "BAG10", "DRO1", "DRO2"]
AX = {"authentication-failed": ("authentification", "échec"), "authentication-success": ("authentification", "succès"), "connection-closed": ("connexion", "fermeture"), "connection-failed": ("connexion", "échec"), "connection-opened": ("connexion", "ouverture"),
      "database-operation": ("base de données", "opération"), "directory-changed": ("répertoire", "modification"), "directory-created": ("répertoire", "création"), "directory-deleted": ("répertoire", "suppression"), "file-action-failure": ("fichier", "échec"),
      "file-deleted": ("fichier", "suppression"), "file-modification": ("fichier", "modification"), "file-read": ("fichier", "lecture"), "file-write": ("fichier", "écriture"), "hardware-monitoring": ("matériel", "surveillance"),
      "http-request-failure": ("http", "échec"), "http-request-success": ("http", "succès"), "ids-alert": ("ids", "alerte"), "network-filtered": ("réseau", "filtrage"), "network-traffic": ("réseau", "trafic"), "process-ended": ("processus", "fermeture"),
      "process-error": ("processus", "échec"), "process-info": ("processus", "information"), "process-shutdown": ("processus", "fermeture"), "process-started": ("processus", "ouverture"), "system-configuration-changed": ("système", "modification"),
      "user-creation": ("utilisateur", "création"), "user-deletion": ("utilisateur", "suppression"), "user-logout": ("utilisateur", "fermeture"), "user-session-open": ("utilisateur", "ouverture")}


def full_proba(model, Xt, K):
    P = np.full((Xt.shape[0], K), 1e-9); P[:, model.classes_] = model.predict_proba(Xt); return P / P.sum(1, keepdims=True)


def task(r, k, dev, tierA, fold, names, small_cls):
    ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; K = len(classes); ids = [classes.index(c) for c in tierA]; sm = [classes.index(c) for c in small_cls]
    objs = sorted({AX[c][0] for c in classes}); acts = sorted({AX[c][1] for c in classes}); obj_of = np.array([objs.index(AX[c][0]) for c in classes]); act_of = np.array([acts.index(AX[c][1]) for c in classes])
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; ytr, yte = y[tr], y[te]; gl, gi = np.unique(dev.group.values[tr], return_inverse=True)
    v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X, Xt = v.fit_transform(dev.log.values[tr]), v.transform(dev.log.values[te]); mats = {}
    lr = LogisticRegression(C=10, max_iter=300).fit(X, ytr); P0 = full_proba(lr, Xt, K); mats["LR"] = P0
    if any(n.startswith("AXE") for n in names):
        po = LogisticRegression(C=10, max_iter=300).fit(X, obj_of[ytr]); pa = LogisticRegression(C=10, max_iter=300).fit(X, act_of[ytr]); Po = np.full((Xt.shape[0], len(objs)), 1e-9); Po[:, po.classes_] = po.predict_proba(Xt); Pa = np.full((Xt.shape[0], len(acts)), 1e-9); Pa[:, pa.classes_] = pa.predict_proba(Xt)
        base = np.log(Po[:, obj_of]) + np.log(Pa[:, act_of])
        for nm, g in (("AXE0", 0.0), ("AXE05", 0.5), ("AXE1", 1.0)):
            if nm in names: mats[nm] = softmax(base + g * np.log(P0), axis=1)
    if "BAG10" in names:
        rng = np.random.default_rng(100 * r + 10 * k); acc = np.zeros_like(P0)
        for b in range(10): sel = rng.random(len(gl)) < 0.7; m = sel[gi]; mb = LogisticRegression(C=10, max_iter=300).fit(X[m], ytr[m]); acc += full_proba(mb, Xt, K)
        mats["BAG10"] = acc / acc.sum(1, keepdims=True)
    if "DRO1" in names or "DRO2" in names:
        rng = np.random.default_rng(100 * r + 10 * k + 7); fg = rng.integers(0, 3, len(gl)); lossg = np.zeros(len(gl)); cnt = np.zeros(len(gl))
        for f in range(3):
            mtr = (fg == f)[gi]; mte = ~mtr
            if mtr.sum() == 0 or mte.sum() == 0: continue
            mb = LogisticRegression(C=10, max_iter=200).fit(X[~mtr], ytr[~mtr]); Pb = full_proba(mb, X[mtr], K); ll = -np.log(Pb[np.arange(mtr.sum()), ytr[mtr]]); np.add.at(lossg, gi[mtr], ll); np.add.at(cnt, gi[mtr], 1)
        Lg = lossg / np.maximum(cnt, 1)
        for nm, Lq in (("DRO1", Lg), ("DRO2", 0.5 * np.minimum(Lg, 4.0))):
            if nm not in names: continue
            q = np.exp(Lq - Lq.max()); q = q / q.sum(); sw = (q * len(gl))[gi] / np.bincount(gi)[gi]; sw = sw * len(sw) / sw.sum(); md = LogisticRegression(C=10, max_iter=300).fit(X, ytr, sample_weight=sw); mats[nm] = full_proba(md, Xt, K)
    res = {}
    for cn, nab in (("toutes", 0), ("abs8", 8)):
        if nab == 0: keep = np.ones(len(yte), bool)
        else: rg = np.random.default_rng(1000 * r + k); gone = rg.choice(np.unique(yte), size=min(8, len(np.unique(yte)) - 1), replace=False); keep = ~np.isin(yte, gone)
        yk = yte[keep]; L = np.unique(yk); a = [c for c in ids if c in L]; s = [c for c in sm if c in L]
        for nm, P in mats.items():
            Pk = P[keep]
            for mode, pred in (("brut", Pk.argmax(1)), ("M50", W3.decode("M50", Pk).argmax(1))):
                res[f"{nm}|{cn}|{mode}"] = {"f1A": float(f1_score(yk, pred, labels=a, average="macro", zero_division=0)), "f1_30": float(f1_score(yk, pred, labels=L, average="macro", zero_division=0)), "f1_small": float(f1_score(yk, pred, labels=s, average="macro", zero_division=0)) if s else float("nan")}
    return res


def unit(r, k, dev, tierA, fold, names, small, block, code):
    cfg = {"phase": 2, "iteration": "W4" + STAGE, "repeat": r, "fold": k, "cap": A.CAP, "variants": names, "modes": ["brut", "M50"], "conditions": ["toutes", "abs8"], "file": "SIEVE_00"}
    return R.run_unit(block, f"W4{STAGE} r{r} pli{k}", cfg, lambda: task(r, k, dev, tierA, fold, names, small), code_version=code)[1]


if __name__ == "__main__":
    dev, tierA = A.load(); ng = dev.groupby("category").group.nunique(); small = sorted(ng[ng <= 3].index); t0 = time.time()
    if STAGE == "a": names = VARS; block, code = "P2_W4a_selection", "W4a.1"; reps = range(5); fold_of = lambda r: dev[f"fold_r{r}"].values
    else: names = json.load(open(ROOT / "artifacts" / "results" / "v3" / "W4_selected.json"))["variants"]; block, code = "P2_W4b_confirmation", "W4b.1"; reps = range(10, 20); folds = W3c.make_folds(dev); fold_of = lambda r: dev.group.map(folds[r]).values
    jobs = [(reps[0], 0)] if "--smoke" in sys.argv else [(r, k) for r in reps for k in range(5)]
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(r, k, dev, tierA, fold_of(r), names, small, block, code) for r, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées en", round(time.time() - t0), "s")
