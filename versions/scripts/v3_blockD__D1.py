"""Bloc D (protocole v3) : attaques sur le texte, trois attaques × cinq degrés, comparées à « sans attaque ». 5 rotations × répétition 0 × 5 plis = 25 unités, SIEVE_00, développement seul.
Attaque d'ÉVASION : seuls les logs de test sont attaqués. Modèles : TF-IDF mots et TF-IDF caractères (régression logistique, C = 4). Mesures sur les mêmes logs : macro-F1 des classes connues, AUROC d'inconnu
(MSP, confiance de la famille), connus rejetés à tort (seuil réglé sur le test propre). Défense : normalisation par la table OFFICIELLE UTS #39 (fichier confusables_ascii.csv), jamais par la table de l'attaque.
Reprenable. Usage : python scripts/v3_blockD.py [--smoke] [--jobs N]"""
import sys, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, pandas as pd
from joblib import Parallel, delayed
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
import v3_blockA as A, v3_blockB as B, v3_blockC as C, tp2_openset as O, tp2_runner as R, tp2_attacks as ATK
warnings.filterwarnings("ignore")
JOBS = int(sys.argv[sys.argv.index("--jobs") + 1]) if "--jobs" in sys.argv else 3
DEGREES = {"typos": [0.05, 0.10, 0.20, 0.30, 0.50], "homoglyphs": [0.05, 0.10, 0.20, 0.30, 0.50], "padding": [0.1, 0.3, 0.5, 1.0, 2.0]}
conf = pd.read_csv(ROOT / "artifacts" / "data" / "confusables_ascii.csv"); conf = conf[conf["caractere"].map(lambda c: ord(c) >= 128)]; CONF_MAP = dict(zip(conf["caractere"], conf["lettre"]))
def canon_official(t): return "".join(CONF_MAP.get(ch, ch) for ch in t)


def task(rot, k, dev, tierA):
    r = 0; ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    tierA_ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev["fold_r0"].values
    te_i = np.where(fold == k)[0]; tr_i = np.where((fold != k) & ~np.isin(y, mid))[0]; yte, ytr = y[te_i], y[tr_i]; known = ~np.isin(yte, mid); txt = dev.log.values[te_i]; trtxt = dev.log.values[tr_i]
    if (~known).sum() < 100 or known.sum() < 100: return {"skipped": "pli sans assez de logs"}
    out = {}
    for mname in ("word", "char"):
        if mname == "word": vec = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2)
        else: vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), sublinear_tf=True, min_df=3, max_features=100000)
        Xtr = vec.fit_transform(trtxt); lr = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xtr, ytr); fam = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xtr, fam_of[ytr])
        lab = [c for c in tierA_ids if (yte[known] == c).any() and c in lr.classes_]; thr = {}
        def measure(texts, ref=False):
            X = vec.transform(texts); P = lr.predict_proba(X); pred = lr.classes_[P.argmax(1)]; msp = P.max(1); fm = fam.predict_proba(X).max(1)
            if ref: thr["msp"] = np.quantile(msp[known], 0.05)
            return {"f1A": float(f1_score(yte[known], pred[known], labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte[known], pred[known], labels=np.unique(yte[known]), average="macro", zero_division=0)), "acc": float(accuracy_score(yte[known], pred[known])),
                    "auroc_msp": float(O.open_metrics(msp, known)["auroc"]), "auroc_fam": float(O.open_metrics(fm, known)["auroc"]), "rej_known": float((msp[known] < thr["msp"]).mean())}
        m = {"clean": measure(txt, ref=True)}
        for ai, (atk, fn) in enumerate(ATK.ATTACKS.items()):
            m[atk] = {}
            for di, rate in enumerate(DEGREES[atk]):
                seed = 1000 * rot + 100 * k + 10 * di + ai; att = [fn(t, rate, seed + 17 * j) for j, t in enumerate(txt)]
                m[atk][str(rate)] = measure(att)
                if atk == "homoglyphs": m.setdefault("homoglyphs_norm", {})[str(rate)] = measure([canon_official(t) for t in att])
        out[mname] = m
    out["_info"] = {"n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "n_train": int(len(tr_i)), "masked": sorted(masked)}
    return out


def unit(rot, k, dev, tierA):
    cfg = {"block": "D", "rotation": rot, "repeat": 0, "fold": k, "cap": A.CAP, "C_head": C.C_HEAD, "degrees": DEGREES, "models": ["word", "char"], "defense": "UTS39 officielle", "splits": "groups_v3"}
    return R.run_unit("D_attaques", f"D rot{rot + 1} r0 pli{k}", cfg, lambda: task(rot, k, dev, tierA), code_version="D1")[1]


if __name__ == "__main__":
    dev, tierA = A.load(); jobs = [(0, 0)] if "--smoke" in sys.argv else [(rot, k) for k in range(5) for rot in range(5)]; t0 = time.time()
    out = Parallel(n_jobs=1 if "--smoke" in sys.argv else JOBS, verbose=5)(delayed(unit)(rot, k, dev, tierA) for rot, k in jobs)
    print("terminé :", sum(o == "calculé" for o in out), "calculées,", sum(o == "rechargé" for o in out), "rechargées en", round(time.time() - t0), "s")
