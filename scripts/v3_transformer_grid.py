"""Bloc T (protocole v3) : grille complète du Transformer. DistilBERT sans casse (256 jetons, 2 époques, 3e-5) × 6 fichiers (p = 0 à 0,5) × 5 rotations × 3 graines = 90 modèles.
Une seule découpe du développement (répétition 0, pli 0) : mêmes gabarits de test pour tous ; 140 logs d'entraînement par classe connue, jusqu'à 133 logs de test par classe (tirage fixe).
Chaque unité compare, sur LES MÊMES logs de test, le Transformer et une baseline TF-IDF entraînée sur les mêmes logs d'entraînement. Le test v2 n'est JAMAIS lu. Les poids ne sont pas conservés ; les logits le sont (npz).
REPRENABLE à deux niveaux : une unité terminée est rechargée ; un entraînement interrompu reprend à son dernier point de contrôle. Usage : python scripts/v3_transformer_grid.py [--smoke] [--seeds 42,43] [--only-p 0,1]"""
import sys, os, time, json, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "colab" / "local"))
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
from scipy.special import logsumexp, softmax
from sklearn.covariance import LedoitWolf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, accuracy_score
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
import tp2_encoder as E
import v3_blockA as A, v3_blockB as B, v3_blockC as C, v3_blockV as V, tp2_openset as O, tp2_runner as R
warnings.filterwarnings("ignore")
NAME, MAXLEN, NTR, NTE = "distilbert-base-uncased", 256, 140, 133
arg = lambda n, d: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else d
SEEDS = [int(s) for s in arg("--seeds", "42,43,44").split(",")]; PS = [int(s) for s in arg("--only-p", "0,1,2,3,4,5").split(",")]
MODELS_DIR = ROOT / "artifacts" / "models" / "encoder_v3"; MODELS_DIR.mkdir(parents=True, exist_ok=True); (R.RES / "T_transformer").mkdir(parents=True, exist_ok=True)


def sample(idx, y_of, n_per, seed):
    rng = np.random.default_rng(seed); out = []
    for c in np.unique(y_of[idx]):
        pool = idx[y_of[idx] == c]; out += list(rng.permutation(pool)[:n_per])
    return np.array(sorted(out))


def metrics(S, known, pred, yte, tierA_ids, classes_known):
    lab = [c for c in tierA_ids if (yte[known] == c).any() and c in classes_known]
    op = {n: O.open_metrics(np.nan_to_num(np.asarray(s, float)), known) for n, s in S.items()}
    return {"closed": {"f1A": float(f1_score(yte[known], pred[known], labels=lab, average="macro", zero_division=0)), "f1_30": float(f1_score(yte[known], pred[known], labels=np.unique(yte[known]), average="macro", zero_division=0)), "acc": float(accuracy_score(yte[known], pred[known]))},
            "open": {n: {"auroc": m["auroc"], "fpr95": m["fpr95"]} for n, m in op.items()}}


def task(p, rot, seed, devs, tierA, npz_path, ckpt):
    dev = devs[p]; ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    tierA_ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev["fold_r0"].values
    te_pool = np.where(fold == 0)[0]; tr_pool = np.where((fold != 0) & ~np.isin(y, mid))[0]; tr_i = sample(tr_pool, y, NTR, 0); te_i = sample(te_pool, y, NTE, 1)
    ytr, yte = y[tr_i], y[te_i]; known = ~np.isin(yte, mid); kcls = np.unique(ytr); K = len(kcls); yi = np.searchsorted(kcls, ytr); txt_tr, txt_te = dev.log.values[tr_i], dev.log.values[te_i]
    if (~known).sum() < 50: return {"skipped": f"inconnus {int((~known).sum())}"}
    t0 = time.time(); model, tok, info = E.train_encoder(NAME, txt_tr, yi, fam_of[ytr], K, len(B.FAMS), max_len=MAXLEN, epochs=2, lr=3e-5, batch_size=32, seed=seed, ckpt_path=str(ckpt))
    pr = E.predict(model, tok, txt_te, max_len=MAXLEN, mc=10); Etr = E.embed(model, tok, txt_tr, max_len=MAXLEN); Ete = E.embed(model, tok, txt_te, max_len=MAXLEN); Lf, Lfam = pr["logits_fine"], pr["logits_fam"]
    Zn_tr, Zn_te = normalize(Etr), normalize(Ete); mu = np.vstack([Etr[yi == j].mean(0) for j in range(K)]); prec = LedoitWolf().fit(Etr - mu[yi]).precision_
    d = np.column_stack([np.einsum("ij,jk,ik->i", Ete - mu[j], prec, Ete - mu[j]) for j in range(K)]); dist = NearestNeighbors(n_neighbors=10).fit(Zn_tr).kneighbors(Zn_te)[0]
    S = {"msp": softmax(Lf, 1).max(1), "maxlogit": Lf.max(1), "energy": logsumexp(Lf, axis=1), "fam_msp": softmax(Lfam, 1).max(1), "mc_msp": pr["mc_fine"].max(1), "maha_shared": -d.min(1), "knn10": -dist[:, 9]}
    pred_t = kcls[Lf.argmax(1)]; tf_res = metrics(S, known, pred_t, yte, tierA_ids, set(kcls)); tsec = round(time.time() - t0, 1)
    w = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = w.fit_transform(txt_tr); Xte = w.transform(txt_te); lr = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xtr, ytr)
    L = lr.decision_function(Xte); _, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C.C_HEAD); S2 = {"msp": lr.predict_proba(Xte).max(1), "energy": logsumexp(L, axis=1), "fam_msp": pf.max(1)}
    np.savez_compressed(npz_path, logits_fine=Lf, logits_fam=Lfam, mc_fine=pr["mc_fine"], y_test=yte, known=known, known_classes=kcls)
    return {"transformer": tf_res, "tfidf_memes_logs": metrics(S2, known, lr.predict(Xte), yte, tierA_ids, set(kcls)), "info": {"n_train": int(len(tr_i)), "n_test": int(len(te_i)), "n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "train_minutes": info["train_minutes"], "device": info["device"], "unit_seconds": tsec, "masked": sorted(masked)}}


def unit(p, rot, seed, devs, tierA):
    cfg = {"block": "T", "file": p, "rotation": rot, "seed": seed, "model": NAME, "max_len": MAXLEN, "epochs": 2, "lr": 3e-5, "batch": 32, "n_train_per_class": NTR, "n_test_per_class": NTE, "split": "r0_pli0", "splits": "groups_v3"}
    name = f"T p{p} rot{rot + 1} seed{seed}"; h = R.config_hash({"block": "T_transformer", "name": name, "cfg": cfg, "code_version": "T1"})
    return R.run_unit("T_transformer", name, cfg, lambda: task(p, rot, seed, devs, tierA, R.RES / "T_transformer" / f"{h}.npz", MODELS_DIR / f"ckpt_{h}.pt"), code_version="T1")[1]


if __name__ == "__main__":
    import torch; torch.set_num_threads(3); devs, tierA = V.load_all(); print("appareil :", E.pick_device(), flush=True)
    jobs = [(0, 0, SEEDS[0])] if "--smoke" in sys.argv else [(p, rot, s) for s in SEEDS for rot in range(5) for p in PS]; t0 = time.time(); done = 0
    for p, rot, s in jobs:
        st = unit(p, rot, s, devs, tierA); done += 1; print(f"[{done}/{len(jobs)}] p{p} rot{rot + 1} graine {s} : {st} ({round((time.time() - t0) / 60, 1)} min écoulées)", flush=True)
    print("terminé", flush=True)
