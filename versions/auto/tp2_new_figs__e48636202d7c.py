"""Visuels des résultats ajoutés depuis l'étape 4 (TP2) : chaque figure montre le NOUVEAU résultat à côté du résultat d'AVANT.

Toutes les figures lisent les fichiers de résultats déjà écrits dans artifacts/results (aucun recalcul) ; aucune figure existante n'est remplacée.
Convention de couleurs : gris-bleu = résultat obtenu avant ; corail = nouveau résultat ; vert = référence (MSP ou TF-IDF mots).
"""
import ast
import glob
import json
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OLD, NEW, REF, WARN = "#7F9BBF", "#D85A30", "#1D9E75", "#BA7517"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25, "font.size": 10})


def _ci(txt):
    a, b = re.findall(r"[-+]?\d*\.\d+|\d+", str(txt))[:2]
    return float(a), float(b)


def _save(fig, figdir, name):
    fig.savefig(Path(figdir) / name, dpi=140, bbox_inches="tight")
    return fig


# --- 4.11 : décisions de l'étape 4 sous validation croisée par groupes -----------------------------------------
def fig_4_11(res, figdir):
    cv = pd.read_csv(Path(res) / "step4_decisions_validation_croisee.csv"); s4 = pd.read_csv(Path(res) / "step4_pretraitement.csv")
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    names = [v.split()[0] for v in cv["variante"]]; y = np.arange(len(cv))[::-1]
    for i, (_, r) in enumerate(cv.iterrows()):
        folds = ast.literal_eval(r["Δ par pli"]); ax[0].scatter(folds, [y[i] + 0.0] * len(folds), color=NEW, alpha=0.55, s=34, zorder=3, label="un pli (validation croisée)" if i == 0 else None)
        ax[0].scatter(r["Δ moyen"], y[i], marker="D", color=NEW, s=70, zorder=4, label="moyenne des 5 plis" if i == 0 else None)
        m = s4[s4["variante"].str.startswith(r["variante"].split()[0] + " ")]
        if len(m):
            d = float(m["Δ vs V0"].iloc[0]); lo, hi = _ci(m["IC 95 %"].iloc[0])
            ax[0].errorbar(d, y[i] - 0.22, xerr=[[d - lo], [hi - d]], fmt="s", color=OLD, capsize=3, zorder=3, label="étape 4 : Δ et IC 95 % (un découpage)" if i == 0 else None)
    ax[0].axvline(0, color="k", lw=1); ax[0].set_yticks(y); ax[0].set_yticklabels([r["variante"] for _, r in cv.iterrows()], fontsize=8.5)
    ax[0].set_xlabel("Δ de macro-F1 par rapport à V0 (négatif = la variante perd)"); ax[0].set_title("Les décisions de l'étape 4 tiennent-elles sous validation croisée ?"); ax[0].legend(fontsize=8, loc="lower left")
    ax[1].bar(np.arange(len(cv)), cv["plis où la variante perd"], color=[NEW if v >= 4 else OLD for v in cv["plis où la variante perd"]])
    ax[1].set_xticks(np.arange(len(cv))); ax[1].set_xticklabels(names); ax[1].set_ylim(0, 5.4); ax[1].axhline(5, color="k", ls=":", lw=1)
    for i, v in enumerate(cv["plis où la variante perd"]): ax[1].text(i, v + 0.1, f"{v}/5", ha="center")
    ax[1].set_ylabel("plis (sur 5) où la variante perd"); ax[1].set_title("Régularité : 5/5 = perte régulière")
    plt.tight_layout(); return _save(fig, figdir, "04_validation_croisee_decisions.png")


# --- 5.8a : contraires et synonymes ---------------------------------------------------------------------------------
def fig_5_8a(res, figdir):
    d = pd.read_csv(Path(res) / "step5_contraires_skipgram.csv"); d["pct"] = d["part des paires aléatoires moins proches"].astype(str).str.rstrip("%").astype(float)
    d = d.iloc[::-1].reset_index(drop=True); fig, ax = plt.subplots(figsize=(9, 4.6)); cols = [REF if t == "synonymes" else NEW for t in d["type"]]
    ax.barh(d["paire"], d["pct"], color=cols); ax.axvline(50, color="k", ls="--", lw=1); ax.set_xlim(0, 105)
    for i, r in d.iterrows(): ax.text(r["pct"] + 1, i, f"cos {r['cosinus']:.2f}", va="center", fontsize=8.5)
    ax.set_xlabel("part des paires aléatoires de mots fréquents MOINS proches que cette paire (50 % = ni proche ni loin)")
    ax.set_title("Les contraires sont-ils rapprochés par Skip-gram ? (corail : contraires, vert : synonymes)"); plt.tight_layout(); return _save(fig, figdir, "05_contraires_skipgram.png")


# --- 5.8b : encodeur gelé contre les représentations de l'étape 5 ---------------------------------------------------
def fig_5_8b(res, figdir):
    rep = pd.read_csv(Path(res) / "step5_representations.csv"); fro = pd.read_csv(Path(res) / "step5_encodeur_gele.csv"); f1 = {}
    for f in glob.glob(str(Path(res) / "cache_step5" / "*.json")):
        j = json.load(open(f))
        if str(j.get("name", "")).startswith("Encodeur gelé"): f1[j["name"]] = j["f1_A"]
    keep = ["BoW comptages", "TF-IDF mots", "TF-IDF mots 1-2 grammes", "TF-IDF caractères 3-5 (dans les mots)", "Word2Vec Skip-gram | idf", "GloVe 100d (pré-entraîné, TP1) | mean"]
    old = rep[rep["représentation"].isin(keep)][["représentation", "F1 palier A"]].values.tolist(); items = [(n.replace(" (dans les mots)", ""), v, OLD) for n, v in old] + [(n, v, NEW) for n, v in sorted(f1.items())]
    items.sort(key=lambda t: t[1]); fig, ax = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    ax[0].barh([i[0] for i in items], [i[1] for i in items], color=[i[2] for i in items]); ax[0].axvline(float(rep[rep["représentation"] == "TF-IDF mots"]["F1 palier A"].iloc[0]), color=REF, ls="--", lw=1.4, label="TF-IDF mots (référence)")
    for i, t in enumerate(items): ax[0].text(t[1] + 0.003, i, f"{t[1]:.3f}", va="center", fontsize=8.5)
    ax[0].set_xlim(0, max(i[1] for i in items) + 0.07); ax[0].set_xlabel("macro-F1 du palier A (validation)"); ax[0].set_title("Encodeur gelé (corail) parmi les représentations de l'étape 5 (gris-bleu)"); ax[0].legend(fontsize=8, loc="lower right")
    y = np.arange(len(fro))[::-1]
    for i, (_, r) in enumerate(fro.iterrows()):
        lo, hi = _ci(r["IC 95 %"]); d = r["Δ macro-F1"]; ax[1].errorbar(d, y[i], xerr=[[d - lo], [hi - d]], fmt="o", color=NEW, capsize=4)
    ax[1].axvline(0, color="k", lw=1); ax[1].set_yticks(y); ax[1].set_yticklabels([c.replace(" (Δ = second moins premier)", "").replace("comparaison", "") for c in fro.iloc[:, 0]], fontsize=8)
    ax[1].set_xlabel("Δ de macro-F1 et IC 95 % (par gabarit)"); ax[1].set_title("Tous les intervalles contiennent 0"); plt.tight_layout(); return _save(fig, figdir, "05_encodeur_gele.png")


# --- 5.8c : fragmentation ------------------------------------------------------------------------------------------------
def fig_5_8c(res, figdir):
    d = pd.read_csv(Path(res) / "step5_fragmentation.csv"); x = np.arange(len(d)); fig, ax = plt.subplots(1, 2, figsize=(12, 4.3))
    ax[0].bar(x - 0.2, d["exactitude TF-IDF"], 0.4, color=REF, label="TF-IDF mots"); ax[0].bar(x + 0.2, d["exactitude encodeur gelé"], 0.4, color=NEW, label="encodeur gelé")
    ax[0].set_xticks(x); ax[0].set_xticklabels([f"{t}\n({j:.1f} jetons/mot)" for t, j in zip(d.iloc[:, 0], d["jetons par mot (moyenne)"])], fontsize=8.5); ax[0].set_ylabel("exactitude (palier A, validation)"); ax[0].legend(); ax[0].set_title("Exactitude par tiers de fragmentation")
    ax[1].bar(x, d["écart (TF-IDF moins encodeur)"], color=[NEW if v < 0 else OLD for v in d["écart (TF-IDF moins encodeur)"]]); ax[1].axhline(0, color="k", lw=1); ax[1].set_xticks(x); ax[1].set_xticklabels(d.iloc[:, 0], fontsize=8.5)
    ax[1].set_ylabel("écart TF-IDF moins encodeur"); ax[1].set_title("L'écart ne croît pas avec la fragmentation")
    plt.tight_layout(); return _save(fig, figdir, "05_fragmentation.png")


# --- 6.4b : tous les scores d'inconnu, anciens et nouveaux ----------------------------------------------------------------
def fig_6_4b(res, figdir):
    d = pd.read_csv(Path(res) / "step6_mahalanobis_knn.csv"); order = ["msp", "energy", "proto", "maha", "knn1", "knn10", "knn50"]; labels = ["MSP", "énergie", "prototype", "Mahalanobis", "kNN k=1", "kNN k=10", "kNN k=50"]
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6), gridspec_kw={"width_ratios": [1.3, 1.3, 1]})
    for a, rep in zip(ax[:2], d["représentation"].unique()):
        s = d[d["représentation"] == rep].set_index("score").loc[order]; a.bar(labels, s["AUROC"], yerr=s["± entre rotations"], capsize=3, color=[OLD] * 3 + [NEW] * 4, alpha=0.9)
        a.axhline(s.loc["msp", "AUROC"], color=REF, ls="--", lw=1.4, label="MSP"); a.axhline(0.5, color="k", ls=":", lw=1); a.set_ylim(0.3, 0.95); a.set_title(f"{rep}\n(gris-bleu : scores d'avant ; corail : nouveaux)", fontsize=10); a.tick_params(axis="x", rotation=40); a.set_ylabel("AUROC (validation, 5 rotations)"); a.legend(fontsize=8)
    t = d.pivot(index="score", columns="représentation", values="FPR@95").loc[order]; x = np.arange(len(order)); w = 0.4
    for i, c in enumerate(t.columns): ax[2].bar(x + (i - 0.5) * w, t[c], w, label=c, color=[REF, WARN][i])
    ax[2].set_xticks(x); ax[2].set_xticklabels(labels, rotation=40, fontsize=8); ax[2].set_ylabel("FPR@95 (plus bas = mieux)"); ax[2].set_ylim(0.6, 1.0); ax[2].legend(fontsize=7); ax[2].set_title("Inconnus acceptés en gardant 95 % des connus")
    plt.tight_layout(); return _save(fig, figdir, "06_scores_anciens_et_nouveaux.png")


# --- 6.4c : Mahalanobis selon la dimension --------------------------------------------------------------------------------
def fig_6_4c(res, figdir):
    m = pd.read_csv(Path(res) / "step6_mahalanobis_dimensions.csv"); b = pd.read_csv(Path(res) / "step6_mahalanobis_knn.csv"); b = b[b["représentation"] == "TF-IDF mots"].set_index("score")
    fig, ax = plt.subplots(figsize=(8.6, 4.6)); k = m["dimension k"]
    ax.plot(k, m["AUROC Mahalanobis"], "o-", color=NEW, lw=2, label="Mahalanobis (SVD de k dimensions)"); ax.fill_between(k, m["AUROC Mahalanobis"] - m["± entre rotations"], m["AUROC Mahalanobis"] + m["± entre rotations"], color=NEW, alpha=0.15)
    for s, c, lab in (("msp", REF, "MSP"), ("knn10", OLD, "kNN (k=10)"), ("proto", WARN, "prototype")): ax.axhline(b.loc[s, "AUROC"], color=c, ls="--", lw=1.4, label=lab)
    ax.axhline(0.5, color="k", ls=":", lw=1); ax2 = ax.twiny(); ax2.set_xlim(ax.get_xlim()); ax2.set_xticks(k); ax2.set_xticklabels([f"{v:.0%}" for v in m["variance gardée"]], fontsize=8); ax2.set_xlabel("part de l'information gardée par la SVD")
    ax.set_xlabel("dimension k de la SVD (TF-IDF mots)"); ax.set_ylabel("AUROC (validation, 5 rotations)"); ax.set_ylim(0.45, 0.85); ax.legend(fontsize=8, loc="lower right"); ax.set_title("Mahalanobis progresse avec les dimensions mais reste sous le MSP", pad=34)
    plt.tight_layout(); return _save(fig, figdir, "06_mahalanobis_dimensions.png")


# --- 6.4d : repli sur la famille ----------------------------------------------------------------------------------------
def fig_6_4d(res, figdir):
    d = pd.read_csv(Path(res) / "step6_repli_famille.csv"); d.columns = ["rep", "meth", "acc", "pire", "meilleure", "part"]; reps = list(d["rep"].unique()); meths = list(d["meth"].unique())
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.5)); x = np.arange(len(meths))
    for j, rep in enumerate(reps):
        s = d[d["rep"] == rep].set_index("meth").loc[meths]; ax[j].bar(x, s["acc"], color=[OLD if "majoritaire" in m else (NEW if "seuil" in m else "#B8C6DA") for m in meths]); ax[j].errorbar(x, s["acc"], yerr=[s["acc"] - s["pire"], s["meilleure"] - s["acc"]], fmt="none", color="k", capsize=3, lw=0.8)
        ax[j].axhline(s.loc[meths[0], "acc"], color=REF, ls="--", lw=1.4, label="famille majoritaire (repère)")
        for i, m in enumerate(meths):
            if "seuil" in m: ax[j].text(i, s.loc[m, "acc"] + 0.03, f"répond dans\n{s.loc[m, 'part']:.0%} des cas", ha="center", fontsize=8)
        ax[j].set_xticks(x); ax[j].set_xticklabels([m.replace("famille de la classe ", "classe ").replace(" (hiérarchique)", "\nhiér.").replace(" (plat)", "\nplat").replace("toujours la ", "").replace(", avec seuil", "\navec seuil").replace(" (avec seuil)", "\navec seuil") for m in meths], fontsize=8)
        ax[j].set_ylim(0, 1.05); ax[j].set_ylabel("exactitude de la famille proposée\n(barres : pire et meilleure rotation)"); ax[j].set_title(rep); ax[j].legend(fontsize=8, loc="upper left")
    plt.tight_layout(); return _save(fig, figdir, "06_repli_famille.png")


# --- 6.4e et 6.4f : OpenMax ---------------------------------------------------------------------------------------------
def fig_6_4e(res, figdir):
    t = pd.read_csv(Path(res) / "step6_openmax_reglage.csv"); b = pd.read_csv(Path(res) / "step6_mahalanobis_knn.csv").set_index(["représentation", "score"]); t.columns = [c.replace('"', "") for c in t.columns]
    reps = list(t.iloc[:, 0]); fig, ax = plt.subplots(1, 3, figsize=(17, 4.6), gridspec_kw={"width_ratios": [1.25, 1, 1]}); lab = ["MSP", "prototype", "kNN k=10", "OpenMax\n(article)", "OpenMax\n(réglage propre)"]
    for j, rep in enumerate(reps):
        r = t[t.iloc[:, 0] == rep].iloc[0]; vals = [b.loc[(rep, "msp"), "AUROC"], b.loc[(rep, "proto"), "AUROC"], b.loc[(rep, "knn10"), "AUROC"], r.iloc[3], r.iloc[2]]; sd = [b.loc[(rep, s), "± entre rotations"] for s in ("msp", "proto", "knn10")] + [np.nan, np.nan]
        ax[0].bar(np.arange(5) + (j - 0.5) * 0.4, vals, 0.4, label=rep, color=[[REF, OLD, OLD, NEW, NEW][i] for i in range(5)], alpha=0.95 if j == 0 else 0.55, edgecolor="k", lw=0.5)
    ax[0].set_xticks(np.arange(5)); ax[0].set_xticklabels(lab, fontsize=8); ax[0].set_ylim(0.4, 0.85); ax[0].axhline(0.5, color="k", ls=":", lw=1); ax[0].set_ylabel("AUROC (validation, 5 rotations)"); ax[0].set_title(f"OpenMax parmi les scores d'avant\n(foncé : {reps[0]} ; clair : {reps[1]})", fontsize=10)
    grids = {}
    for f in glob.glob(str(Path(res) / "cache_step6" / "x5_*.json")):
        j = json.load(open(f)); grids.setdefault(j["rep"], []).append({k: v for k, v in j.items() if re.match(r"\d+_\d+$", k)})
    for a, (rep, lst) in zip(ax[1:], grids.items()):
        g = pd.DataFrame(lst).mean(); etas = sorted({int(k.split("_")[0]) for k in g.index}); als = sorted({int(k.split("_")[1]) for k in g.index}); M = np.array([[g[f"{e}_{al}"] for al in als] for e in etas])
        im = a.imshow(M, cmap="YlGnBu", aspect="auto"); a.set_xticks(range(len(als))); a.set_xticklabels([f"α={x}" for x in als]); a.set_yticks(range(len(etas))); a.set_yticklabels([f"η={x}" for x in etas])
        for i in range(len(etas)):
            for k in range(len(als)): a.text(k, i, f"{M[i, k]:.3f}", ha="center", va="center", fontsize=8, color="white" if M[i, k] > (M.min() + M.max()) / 2 else "black")
        a.add_patch(plt.Rectangle((als.index(10) - 0.5, etas.index(20) - 0.5), 1, 1, fill=False, ec=NEW, lw=2.5)); a.set_title({"tfidf": "TF-IDF", "sg_idf": "Skip-gram"}.get(rep, rep) + " : AUROC interne\n(cadre : réglage de l'article)", fontsize=10); a.grid(False)
    plt.tight_layout(); return _save(fig, figdir, "06_openmax.png")


# --- 7.2b : pourquoi la baisse validation -> test --------------------------------------------------------------------------
def fig_7_2b(res, figdir):
    v = pd.read_csv(Path(res) / "step7_variabilite_gabarits.csv"); s = pd.read_csv(Path(res) / "step7_optimisme_selection.csv"); fig, ax = plt.subplots(1, 2, figsize=(13, 4.4))
    for i, (_, r) in enumerate(v.iterrows()):
        lo, hi = _ci(r["IC 95 %"]); c = [OLD, NEW, "k"][i]; ax[0].errorbar(r["AUROC observé"], 2 - i, xerr=[[r["AUROC observé"] - lo], [hi - r["AUROC observé"]]], fmt="o", color=c, capsize=5, ms=8)
        ax[0].text(hi + 0.012, 2 - i, f"{r['AUROC observé']:.3f}", va="center")
    ax[0].axvline(0, color="k", lw=0.8); ax[0].axvline(0.5, color="k", ls=":", lw=1); ax[0].set_yticks([2, 1, 0]); ax[0].set_yticklabels(["validation", "test", "différence\n(val. − test)"]); ax[0].set_xlabel("AUROC moyen (TF-IDF, MSP, 5 rotations) et IC 95 % par gabarit"); ax[0].set_title("La baisse dépasse le hasard des gabarits")
    x = np.arange(len(s)); ax[1].bar(x - 0.2, s["avantage maximal de la sélection"], 0.4, color=OLD, label="avantage maximal de la sélection")
    ax[1].bar(x + 0.2, s["plus grande"], 0.4, color=NEW, label="baisse validation → test (la plus grande)"); ax[1].bar(x + 0.2, s["baisse val → test : plus petite"], 0.4, color="#F0997B", label="baisse validation → test (la plus petite)")
    ax[1].set_xticks(x); ax[1].set_xticklabels(s["représentation"]); ax[1].set_ylabel("AUROC"); ax[1].legend(fontsize=8); ax[1].set_title("La sélection explique très peu de la baisse")
    plt.tight_layout(); return _save(fig, figdir, "07_baisse_validation_test.png")


# --- 9.12 : défense honnête -----------------------------------------------------------------------------------------------
def fig_9_12(res, figdir):
    d = pd.read_csv(Path(res) / "step9_defense_honnete.csv"); p = pd.read_csv(Path(res) / "step9_parades.csv"); fig, ax = plt.subplots(1, 2, figsize=(15, 4.8), gridspec_kw={"width_ratios": [1.5, 1]})
    M = d.pivot_table(index="attaque", columns="défense", values="baisse relative", aggfunc="mean"); M = M.loc[sorted(M.index)]; im = ax[0].imshow(M.values, cmap="Reds", vmin=0, vmax=0.12, aspect="auto")
    ax[0].set_xticks(range(M.shape[1])); ax[0].set_xticklabels([c.replace(" ", "\n", 2) for c in M.columns], fontsize=7.5); ax[0].set_yticks(range(M.shape[0])); ax[0].set_yticklabels([a.replace(" (celle de la parade)", "\n(celle de la parade)").replace(" hors moitié connue du défenseur D3 (adaptative)", "\nhors moitié connue de D3\n(adaptative)").replace(" hors table maison (adaptative contre D1)", "\nhors table maison\n(adaptative contre D1)") for a in M.index], fontsize=8)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): ax[0].text(j, i, f"{M.values[i, j]:.3f}", ha="center", va="center", fontsize=9, color="white" if M.values[i, j] > 0.07 else "black")
    ax[0].grid(False); ax[0].set_title("Baisse relative de F1 (moyenne des 3 intensités) : attaques × défenses"); plt.colorbar(im, ax=ax[0], fraction=0.03)
    a1, a2 = [i for i in M.index if i.startswith("A1")][0], [i for i in M.index if i.startswith("A2")][0]; d1 = [c for c in M.columns if c.startswith("D1")][0]; d4 = [c for c in M.columns if c.startswith("D4")][0]
    labs = ["sans défense\n(attaque maison)", "table maison\ncontre sa propre\nattaque (avant)", "table maison\ncontre la table\nofficielle (honnête)", "table officielle\ncomplète\n(honnête)"]; vals = [M.loc[a1, "D0 aucune"], M.loc[a1, d1], M.loc[a2, d1], M.loc[a2, d4]]
    ax[1].bar(range(4), vals, color=[OLD, OLD, NEW, REF]); [ax[1].text(i, v + 0.003, f"{v:.3f}", ha="center") for i, v in enumerate(vals)]; ax[1].set_xticks(range(4)); ax[1].set_xticklabels(labs, fontsize=8); ax[1].set_ylabel("baisse relative de F1")
    ax[1].set_title("Avant (circulaire) et après (honnête)"); plt.tight_layout(); return _save(fig, figdir, "09_defense_honnete.png")


# --- Encodeur à plusieurs graines et scores sur ses vecteurs (H8) ----------------------------------------------------------
def fig_encodeur_graines(res, figdir):
    d = pd.read_csv(Path(res) / "step10_encodeur_graines.csv"); fig, ax = plt.subplots(1, 2, figsize=(14, 4.6), gridspec_kw={"width_ratios": [1.1, 1.3]}); rots = sorted(d["rotation"].unique())
    for k, r in enumerate(rots):
        s = d[(d["rotation"] == r) & (d["score"] == "msp")]; ax[0].scatter([r] * len(s), s["AUROC"], color=NEW, s=45, alpha=0.8, zorder=3, label="encodeur (une graine)" if k == 0 else None)
        ax[0].plot([r - 0.25, r + 0.25], [s["AUROC"].mean()] * 2, color="k", lw=2)
        if "AUROC TF-IDF" in d.columns: ax[0].scatter([r], [s["AUROC TF-IDF"].iloc[0]], marker="s", color=REF, s=70, zorder=4, label="TF-IDF (référence)" if k == 0 else None)
    ax[0].set_xticks(rots); ax[0].set_xlabel("rotation"); ax[0].set_ylabel("AUROC du MSP (test)"); ax[0].axhline(0.5, color="k", ls=":", lw=1); ax[0].legend(fontsize=8); ax[0].set_title("L'encodeur d'une graine à l'autre (trait noir : moyenne)")
    sc = [s for s in ("msp", "energy", "maha", "knn1", "knn10", "knn50") if s in set(d["score"])]; lab = {"msp": "MSP", "energy": "énergie", "maha": "Mahalanobis\n(vecteurs)", "knn1": "kNN k=1", "knn10": "kNN k=10", "knn50": "kNN k=50"}
    g = d.groupby("score")["AUROC"].agg(["mean", "std"]).loc[sc]; ax[1].bar([lab[s] for s in sc], g["mean"], yerr=g["std"].fillna(0), capsize=3, color=[OLD if s in ("msp", "energy") else NEW for s in sc]); ax[1].axhline(0.5, color="k", ls=":", lw=1)
    ax[1].set_ylabel("AUROC (test, moyenne des rotations et des graines)"); ax[1].set_title("Scores sur l'encodeur : scores d'avant (gris-bleu) et sur vecteurs (corail)"); plt.tight_layout(); return _save(fig, figdir, "10_encodeur_graines_vecteurs.png")


# --- 5.9 : fichiers du professeur (SIEVE 35 000 logs) : fuite sur données fraîches, taille du jeu, quasi-jumeaux -----------------------
def fig_5_9(res, figdir):
    res = Path(res); A = pd.read_csv(res / "step5_donnees_fraiches.csv"); B = pd.read_csv(res / "step5_taille_croisee.csv"); C = pd.read_csv(res / "step5_courbe_taille.csv"); D = pd.read_csv(res / "step5_jumeaux_professeur.csv")
    e1 = pd.read_csv(res / "step7_E1.csv"); test30 = float(e1[(e1.iloc[:, 0] == "TF-IDF mots") & (e1.iloc[:, 1] == "plat")]["F1 30 classes"].iloc[0]); prot = pd.read_csv(res / "step3_protocoles.csv"); p0share = float(str(prot.iloc[0, -1]).rstrip("%")) / 100
    fig, ax = plt.subplots(2, 2, figsize=(14, 9))
    names = ["validation\n(gabarits\nnouveaux)"] + [f"fichier prof.\np={p}" for p in ["0", "0,1", "0,2", "0,3", "0,4", "0,5"]]; v = A["macro-F1 (30 classes)"].values
    ax[0, 0].bar(range(len(v)), v, color=[OLD] + [NEW] * (len(v) - 1)); ax[0, 0].axhline(test30, color=REF, ls="--", lw=1.4, label=f"test scellé, gabarits nouveaux ({test30:.2f})"); [ax[0, 0].text(i, x + 0.012, f"{x:.2f}", ha="center", fontsize=9) for i, x in enumerate(v)]
    ax[0, 0].set_xticks(range(len(v))); ax[0, 0].set_xticklabels(names, fontsize=8); ax[0, 0].set_ylim(0, 1.08); ax[0, 0].set_ylabel("macro-F1, 30 classes"); ax[0, 0].legend(fontsize=8, loc="lower left"); ax[0, 0].set_title("Fuite sur données fraîches : même modèle, gabarits connus ou nouveaux")
    ax[0, 1].plot(B["p"], B["entraîné sur 100K, testé sur 35K"], "o-", color=NEW, label="entraîné sur 100K, testé sur 35K"); ax[0, 1].plot(B["p"], B["entraîné sur 35K, testé sur 100K"], "s-", color=OLD, label="entraîné sur 35K, testé sur 100K")
    ax[0, 1].set_xlabel("niveau de perturbation p"); ax[0, 1].set_ylabel("macro-F1, 30 classes"); ax[0, 1].set_ylim(0.5, 1.02); ax[0, 1].legend(fontsize=8); ax[0, 1].set_title("Taille du jeu : 100K contre 35K, dans les deux sens (mêmes gabarits)")
    ax[1, 0].plot(C.iloc[:, 0], C.iloc[:, 1], "o-", color=NEW, label="découpage aléatoire (mêmes gabarits)"); ax[1, 0].plot(C.iloc[:, 2], C.iloc[:, 3], "s-", color=OLD, label="découpage par gabarit (gabarits nouveaux)")
    ax[1, 0].set_xscale("log"); ax[1, 0].set_xlabel("logs d'entraînement (échelle logarithmique)"); ax[1, 0].set_ylabel("macro-F1, 30 classes (p = 0)"); ax[1, 0].set_ylim(0, 1.02); ax[1, 0].legend(fontsize=8); ax[1, 0].set_title("Courbe de taille : plus de données aide-t-il ?")
    ax[1, 1].bar(range(len(D)), D["part >= 0,90"], color=NEW, label="logs du professeur"); ax[1, 1].axhline(p0share, color=REF, ls="--", lw=1.4, label=f"découpage aléatoire de l'étape 3 ({p0share:.0%})"); [ax[1, 1].text(i, x + 0.006, f"{x:.0%}", ha="center", fontsize=9) for i, x in enumerate(D["part >= 0,90"])]
    ax[1, 1].set_xticks(range(len(D))); ax[1, 1].set_xticklabels([f"p={p}" for p in ["0", "0,1", "0,2", "0,3", "0,4", "0,5"]]); ax[1, 1].set_ylabel("part de logs avec un quasi-jumeau (cosinus ≥ 0,90)"); ax[1, 1].legend(fontsize=8); ax[1, 1].set_title("Mêmes gabarits que SIEVE 100K : quasi-jumeaux selon p")
    plt.tight_layout(); return _save(fig, figdir, "05_donnees_professeur.png")


def fig_5_9b(res, figdir):
    d = pd.read_csv(Path(res) / "step5_donnees_fraiches_decomposition.csv"); a = pd.read_csv(Path(res) / "step5_donnees_fraiches.csv"); b = pd.read_csv(Path(res) / "step5_taille_croisee.csv")
    fig, ax = plt.subplots(figsize=(11, 4.6)); cols = [NEW if "entraînement" in g or "≥" in g else OLD for g in d["groupe"]]; ax.bar(range(len(d)), d["exactitude"], color=cols)
    for i, r in d.iterrows(): ax.text(i, r["exactitude"] + 0.015, f"{r['exactitude']:.2f}\n({r['part des logs']:.0%} des logs)", ha="center", fontsize=8.5)
    ax.axhline(float(a.iloc[1, 2]), color="k", ls=":", lw=1.2, label=f"ensemble du fichier p=0 ({float(a.iloc[1, 2]):.2f})"); ax.axhline(float(b.iloc[0, 1]), color=REF, ls="--", lw=1.4, label=f"modèle qui a vu tous les gabarits ({float(b.iloc[0, 1]):.2f})")
    ax.set_xticks(range(len(d))); ax.set_xticklabels([g.replace(" : ", "\n") for g in d["groupe"]], fontsize=8); ax.set_ylim(0, 1.18); ax.set_ylabel("exactitude du modèle de 5.9a (fichier du professeur, p = 0)"); ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Pourquoi 0,81 et non 0,97 ? Le modèle de 5.9a n'a vu qu'une partie des gabarits"); plt.tight_layout(); return _save(fig, figdir, "05_donnees_professeur_decomposition.png")
