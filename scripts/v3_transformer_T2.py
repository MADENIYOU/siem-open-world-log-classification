"""Bloc T2 (D22) : réplication du Transformer sur 4 NOUVELLES découpes (p = 0) + fusion Transformer/TF-IDF. 20 modèles = 4 découpes x 5 rotations, graine 42. Reprenable (unités + points de contrôle). Usage : python scripts/v3_transformer_T2.py [--smoke]"""
import sys, os, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "colab" / "local"))
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import numpy as np
from scipy.special import logsumexp, softmax
from sklearn.covariance import LedoitWolf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import normalize
import tp2_encoder as E
import v3_blockB as B, v3_blockC as C, v3_blockV as V, tp2_runner as R
import v3_transformer_grid as G
warnings.filterwarnings("ignore")
NAME, MAXLEN, NTR, NTE, SEED = G.NAME, G.MAXLEN, G.NTR, G.NTE, 42
SPLITS = [(1, 1), (2, 2), (3, 3), (4, 4)]; MODELS_DIR = G.MODELS_DIR; (R.RES / "T2_replication").mkdir(parents=True, exist_ok=True)


def task(sp, rot, devs, tierA, ckpt):
    r, k = sp; dev = devs[0]; ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ncls = len(classes); masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked])
    tierA_ids = [classes.index(c) for c in tierA]; fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values
    te_pool = np.where(fold == k)[0]; tr_pool = np.where((fold != k) & ~np.isin(y, mid))[0]; tr_i = G.sample(tr_pool, y, NTR, 0); te_i = G.sample(te_pool, y, NTE, 1)
    ytr, yte = y[tr_i], y[te_i]; known = ~np.isin(yte, mid); kcls = np.unique(ytr); K = len(kcls); yi = np.searchsorted(kcls, ytr); txt_tr, txt_te = dev.log.values[tr_i], dev.log.values[te_i]
    if (~known).sum() < 50: return {"skipped": f"inconnus {int((~known).sum())}"}
    t0 = time.time(); model, tok, info = E.train_encoder(NAME, txt_tr, yi, fam_of[ytr], K, len(B.FAMS), max_len=MAXLEN, epochs=2, lr=3e-5, batch_size=32, seed=SEED, ckpt_path=str(ckpt))
    pr = E.predict(model, tok, txt_te, max_len=MAXLEN, mc=10); Etr = E.embed(model, tok, txt_tr, max_len=MAXLEN); Ete = E.embed(model, tok, txt_te, max_len=MAXLEN); Lf, Lfam = pr["logits_fine"], pr["logits_fam"]
    Zn_tr, Zn_te = normalize(Etr), normalize(Ete); mu = np.vstack([Etr[yi == j].mean(0) for j in range(K)]); prec = LedoitWolf().fit(Etr - mu[yi]).precision_
    d = np.column_stack([np.einsum("ij,jk,ik->i", Ete - mu[j], prec, Ete - mu[j]) for j in range(K)]); dist = NearestNeighbors(n_neighbors=10).fit(Zn_tr).kneighbors(Zn_te)[0]
    Pt = softmax(Lf, 1); Pft = softmax(Lfam, 1); S = {"msp": Pt.max(1), "maxlogit": Lf.max(1), "energy": logsumexp(Lf, axis=1), "fam_msp": Pft.max(1), "mc_msp": pr["mc_fine"].max(1), "maha_shared": -d.min(1), "knn10": -dist[:, 9]}
    tf_res = G.metrics(S, known, kcls[Lf.argmax(1)], yte, tierA_ids, set(kcls)); tsec = round(time.time() - t0, 1)
    w = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr = w.fit_transform(txt_tr); Xte = w.transform(txt_te); lr = LogisticRegression(C=C.C_HEAD, max_iter=300).fit(Xtr, ytr)
    Pb = lr.predict_proba(Xte); _, pf = B.hier_probs(Xtr, ytr, Xte, fam_of, len(B.FAMS), ncls, C=C.C_HEAD); S2 = {"msp": Pb.max(1), "energy": logsumexp(lr.decision_function(Xte), axis=1), "fam_msp": pf.max(1)}
    base = G.metrics(S2, known, lr.predict(Xte), yte, tierA_ids, set(kcls)); Pf = (Pt + Pb) / 2; Pfam = (Pft + pf[:, :Pft.shape[1]]) / 2 if pf.shape[1] == Pft.shape[1] else (Pft + pf) / 2
    fus = G.metrics({"msp": Pf.max(1), "fam_msp": Pfam.max(1)}, known, kcls[Pf.argmax(1)], yte, tierA_ids, set(kcls))
    return {"transformer": tf_res, "tfidf_memes_logs": base, "fusion": fus, "info": {"n_train": int(len(tr_i)), "n_test": int(len(te_i)), "n_known_test": int(known.sum()), "n_unknown_test": int((~known).sum()), "train_minutes": info["train_minutes"], "unit_seconds": tsec, "masked": sorted(masked)}}


def unit(sp, rot, devs, tierA):
    cfg = {"block": "T2", "split_repeat": sp[0], "split_fold": sp[1], "rotation": rot, "seed": SEED, "model": NAME, "max_len": MAXLEN, "epochs": 2, "lr": 3e-5, "batch": 32, "n_train_per_class": NTR, "n_test_per_class": NTE, "p": 0}
    name = f"T2 r{sp[0]}k{sp[1]} rot{rot + 1}"; h = R.config_hash({"block": "T2_replication", "name": name, "cfg": cfg, "code_version": "T2.1"})
    return R.run_unit("T2_replication", name, cfg, lambda: task(sp, rot, devs, tierA, MODELS_DIR / f"ckpt_{h}.pt"), code_version="T2.1")[1]


if __name__ == "__main__":
    import torch; torch.set_num_threads(3); devs, tierA = V.load_all(); print("appareil :", E.pick_device(), flush=True)
    jobs = [(SPLITS[0], 0)] if "--smoke" in sys.argv else [(sp, rot) for sp in SPLITS for rot in range(5)]; t0 = time.time()
    for n, (sp, rot) in enumerate(jobs, 1):
        st = unit(sp, rot, devs, tierA); print(f"[{n}/{len(jobs)}] découpe {sp} rot{rot + 1} : {st} ({round((time.time() - t0) / 60, 1)} min)", flush=True)
    print("terminé", flush=True)
