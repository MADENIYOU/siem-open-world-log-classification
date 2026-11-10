"""Vague 7 (D37, HL1, HM1) : LP-FT et LP-FT depuis un DistilBERT adapté (MLM) dans le protocole de T2 (4 découpes × 5 rotations, p = 0, graine 42, 140 logs d'entraînement par classe, mêmes logs que T2). Dev seul. Reprenable par unité. Usage : python scripts/v3_transformer_W7.py [--smoke]"""
import sys, os, time, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts")); sys.path.insert(0, str(ROOT / "colab" / "local"))
os.environ.setdefault("HF_HUB_OFFLINE", "1"); os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
import gc
import numpy as np
from scipy.special import softmax
import tp2_encoder as E, tp2_encoder_lpft as L
import v3_blockB as B, v3_blockC as C, v3_blockV as V, tp2_runner as R, v3_transformer_grid as G, v3_transformer_T2 as T2
warnings.filterwarnings("ignore")
NTR, NTE, SEED, MLM_CAP = G.NTR, G.NTE, 42, 20000; (R.RES / "W7_lpft").mkdir(parents=True, exist_ok=True); ADAPT = ROOT / "artifacts" / "models" / "encoder_v3" / "adapt_w7"; ADAPT.mkdir(parents=True, exist_ok=True)


def free():
    import torch; gc.collect()
    if torch.backends.mps.is_available(): torch.mps.empty_cache()


def task(sp, rot, devs, tierA):
    r, k = sp; dev = devs[0]; ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; masked = set(C.ROT[rot]); mid = np.array([classes.index(c) for c in masked]); tierA_ids = [classes.index(c) for c in tierA]
    fam_of = np.array([B.FAMS.index([f for f in B.FAMS if c in B.TAX[f]][0]) for c in classes]); fold = dev[f"fold_r{r}"].values; te_pool = np.where(fold == k)[0]; tr_pool = np.where((fold != k) & ~np.isin(y, mid))[0]
    tr_i = G.sample(tr_pool, y, NTR, 0); te_i = G.sample(te_pool, y, NTE, 1); ytr, yte = y[tr_i], y[te_i]; known = ~np.isin(yte, mid); kcls = np.unique(ytr); K = len(kcls); yi = np.searchsorted(kcls, ytr); txt_tr, txt_te = dev.log.values[tr_i], dev.log.values[te_i]; res = {}
    model, tok, info = L.train_lpft("distilbert-base-uncased", txt_tr, yi, fam_of[ytr], K, len(B.FAMS), max_len=256, seed=SEED); pr = E.predict(model, tok, txt_te, max_len=256, mc=0); Lf = pr["logits_fine"]
    res["lpft"] = {**G.metrics({"msp": softmax(Lf, 1).max(1)}, known, kcls[Lf.argmax(1)], yte, tierA_ids, set(kcls))["closed"], "train_minutes": info["train_minutes"]}; del model, pr, Lf; free()
    pool = np.where((fold != k) & ~np.isin(y, mid))[0]; rng = np.random.default_rng(100 * r + 10 * k + rot); sel = rng.permutation(pool)[:MLM_CAP]; ad = ADAPT / f"r{r}k{k}rot{rot + 1}"
    mi = L.adapt_mlm(dev.log.values[sel], str(ad), seed=SEED); free(); model, tok, info = L.train_lpft(str(ad), txt_tr, yi, fam_of[ytr], K, len(B.FAMS), max_len=256, seed=SEED); pr = E.predict(model, tok, txt_te, max_len=256, mc=0); Lf = pr["logits_fine"]
    res["lpft_adapt"] = {**G.metrics({"msp": softmax(Lf, 1).max(1)}, known, kcls[Lf.argmax(1)], yte, tierA_ids, set(kcls))["closed"], "train_minutes": info["train_minutes"], **mi}; del model, pr, Lf; free()
    return res


def unit(sp, rot, devs, tierA):
    cfg = {"block": "W7", "split_repeat": sp[0], "split_fold": sp[1], "rotation": rot, "seed": SEED, "n_train_per_class": NTR, "n_test_per_class": NTE, "lp": [1, 1e-3], "ft": [2, 1e-5], "mlm": {"epochs": 1, "cap": MLM_CAP, "len": 128, "lr": 5e-5}, "p": 0}
    return R.run_unit("W7_lpft", f"W7 r{sp[0]}k{sp[1]} rot{rot + 1}", cfg, lambda: task(sp, rot, devs, tierA), code_version="W7.1")[1]


if __name__ == "__main__":
    import torch; torch.set_num_threads(3); devs, tierA = V.load_all(); jobs = [(T2.SPLITS[0], 0)] if "--smoke" in sys.argv else [(sp, rot) for sp in T2.SPLITS for rot in range(5)]; t0 = time.time()
    for n, (sp, rot) in enumerate(jobs, 1):
        st = unit(sp, rot, devs, tierA); print(f"[{n}/{len(jobs)}] découpe {sp} rot{rot + 1} : {st} ({round((time.time() - t0) / 60, 1)} min)", flush=True)
    print("terminé", flush=True)
