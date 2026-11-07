"""Découpage v3 : développement (validation croisée par groupes répétée) et test scellé v2.

Règles (écrites avant de tirer) :
 1. L'unité est le gabarit reconstruit (311) ; tous ses logs, dans les 6 fichiers, vont du même côté. Les 25 gabarits que le protocole v1 avait coupés sont rendus entiers.
 2. Test v2 : ceux des gabarits qui n'ont JAMAIS servi de test en v1, à raison de ceil(15 %) par classe (au moins 1 pour une classe de 3 gabarits ou plus), sans laisser moins de 2 gabarits au développement.
 3. Un tirage est accepté si : la part de logs de test est entre 10 et 22 %, chaque classe de 5 gabarits ou plus a au moins 1 gabarit de test, et la part de quasi-jumeaux
    (cosinus TF-IDF >= 0,90 avec un log d'entraînement de la même classe, mesurée sur SIEVE_00) est <= 2 %. Sinon on passe à la graine suivante ; la graine retenue et le nombre de refus sont enregistrés.
 4. Développement : validation croisée par groupes à 5 plis, répétée 5 fois (graines 0 à 4), stratifiée par classe.
"""
import hashlib, json, time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.feature_extraction.text import TfidfVectorizer

FRAC, MIN_DEV_GROUPS, SHARE_RANGE, TWIN_MAX, TWIN_COS = 0.15, 2, (0.10, 0.22), 0.02, 0.90
N_SPLITS, N_REPEATS = 5, 5


def draw_test_groups(gt, seed):
    rng = np.random.default_rng(seed); chosen = []
    for c, g in gt.groupby("category"):
        T = len(g); n2 = int(np.ceil(FRAC * T)) if T >= 3 else 0
        avail = g[~g.in_v1_test]; n2 = min(n2, len(avail), T - MIN_DEV_GROUPS)
        if n2 > 0: chosen += list(rng.choice(avail.group.values, size=n2, replace=False))
    return set(int(x) for x in chosen)


def twin_share(V0, rows0, test_groups, rng_seed=0, per_class=800, ref_cap=15000):
    """Part de logs de test de SIEVE_00 ayant un quasi-jumeau (même classe) parmi les logs de développement ; échantillon par classe."""
    d = V0.merge(rows0[["row", "group"]], on="row"); is_test = d.group.isin(test_groups).values
    tv = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); X = tv.fit_transform(d["log"]); rng = np.random.default_rng(rng_seed); best, total = [], []
    for c in sorted(d.category.unique()):
        te = np.where((d.category.values == c) & is_test)[0]; tr = np.where((d.category.values == c) & ~is_test)[0]
        if len(te) == 0 or len(tr) == 0: continue
        te = rng.choice(te, size=min(per_class, len(te)), replace=False); tr = rng.choice(tr, size=min(ref_cap, len(tr)), replace=False)
        sim = (X[te] @ X[tr].T).tocsr(); best += list(np.asarray(sim.max(axis=1).todense()).ravel())
    best = np.array(best); return float((best >= TWIN_COS).mean()), float(np.median(best))


def build_v3(root, versions, splits_v1, groups_tbl, max_tries=300, log=print):
    root = Path(root); rows0 = splits_v1[splits_v1.version == 0]; V0 = versions[0]
    total = groups_tbl.n_logs.sum(); big = groups_tbl[groups_tbl.category.map(groups_tbl.groupby("category").size()) >= 5].category.unique()
    refused = []
    for seed in range(1, max_tries + 1):
        tg = draw_test_groups(groups_tbl, seed); share = groups_tbl[groups_tbl.group.isin(tg)].n_logs.sum() / total
        cover = groups_tbl[groups_tbl.group.isin(tg)].category.unique()
        if not (SHARE_RANGE[0] <= share <= SHARE_RANGE[1]) or not set(big) <= set(cover): refused.append((seed, "part ou couverture")); continue
        ts, med = twin_share(V0, rows0, tg)
        if ts > TWIN_MAX: refused.append((seed, f"quasi-jumeaux {ts:.3f}")); continue
        log(f"graine retenue {seed} ; part de logs de test {share:.3f} ; quasi-jumeaux {ts:.4f} ; cosinus médian {med:.3f} ; refus avant : {len(refused)}")
        break
    else:
        raise RuntimeError("aucun tirage accepté")
    g = groups_tbl.copy(); g["role"] = np.where(g.group.isin(tg), "test2", "dev")
    dev = g[g.role == "dev"].reset_index(drop=True)
    for r in range(N_REPEATS):
        sgkf = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=r); fold = np.full(len(dev), -1)
        for k, (_, te_idx) in enumerate(sgkf.split(dev, dev.category, dev.group)): fold[te_idx] = k
        dev[f"fold_r{r}"] = fold
    g = g.merge(dev[["group"] + [f"fold_r{r}" for r in range(N_REPEATS)]], on="group", how="left")
    for r in range(N_REPEATS): g[f"fold_r{r}"] = g[f"fold_r{r}"].fillna(-1).astype(int)
    meta = {"version": 3, "created": time.strftime("%Y-%m-%d %H:%M:%S"), "test2_seed": seed, "refused_before": len(refused), "frac": FRAC, "min_dev_groups": MIN_DEV_GROUPS,
            "share_range": SHARE_RANGE, "twin_max": TWIN_MAX, "twin_cos": TWIN_COS, "twin_share": ts, "median_nn_cos": med, "n_splits": N_SPLITS, "n_repeats": N_REPEATS,
            "n_groups": int(len(g)), "n_test2_groups": int((g.role == "test2").sum()), "test2_log_share": float(share),
            "test2_groups_sha256": hashlib.sha256(",".join(map(str, sorted(tg))).encode()).hexdigest()[:16]}
    return g, meta
