"""Construit la PARTIE 2 du notebook (protocole v3) : sections AJOUTÉES à la fin, sans rien retirer ni réécrire de la v1. Les cellules générées portent metadata {"part2": true} ;
relancer le script régénère uniquement ces cellules (les cellules v1 ne sont jamais touchées) ; le notebook est archivé avant chaque réécriture (archive/). Tableaux et figures sortent du journal et de artifacts/results/v3. Usage : python scripts/build_notebook_part2.py"""
import sys, json, time, shutil, uuid, collections, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
import tp2_journal as J
NB = ROOT / "TP2_logs_hierarchique_monde_ouvert.ipynb"; RES = ROOT / "artifacts" / "results" / "v3"; FIG = ROOT / "artifacts" / "figures"; FIG.mkdir(exist_ok=True)
CORAL, TEAL, SAND, NAVY, GREY, GOLD = "#E8664F", "#2A9D8F", "#E9C46A", "#264653", "#9AA5B1", "#F4A261"
plt.rcParams.update({"font.size": 11, "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 130})
E = collections.OrderedDict()
for e in J.entries(): E.setdefault(e["id"], []).append(e)
last = lambda i: E[i][-1]
def md(text): return {"cell_type": "markdown", "id": uuid.uuid4().hex[:8], "metadata": {"part2": True}, "source": text.strip("\n").splitlines(keepends=True)}
def res(i): return last(i)["texte"].replace("\n", " ")
def ci(a, b): return f"[{a:.3f} ; {b:.3f}]"
cells = []
# ---------- figures ----------
def fig_decoding():
    rows = []
    for nm, f in (("sélection (25 plis)", "W3a"), ("confirmation (25)", "W3b"), ("réplication (50)", "W3c"), ("réplication finale (100)", "W3d")):
        d = pd.read_csv(RES / f"{f}_all_units.csv")
        for cond in ("toutes", "abs8", "abs14"):
            X = d[d.cond == cond].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A")
            for v in ("M50", "A1"):
                if v in X.columns: rows.append({"série": nm, "condition": cond, "variante": v, "gain": (X[v] - X["LR"]).mean(), "n": len(X), "se": (X[v] - X["LR"]).std() / np.sqrt(len(X))})
    G = pd.DataFrame(rows); fig, ax = plt.subplots(1, 3, figsize=(13, 4.2), sharey=True)
    for a, cond, title in zip(ax, ("toutes", "abs8", "abs14"), ("toutes les classes présentes", "8 classes absentes du lot", "14 classes absentes du lot")):
        S = G[G.condition == cond]; ser = list(dict.fromkeys(S["série"])); x = np.arange(len(ser)); w = 0.38
        for k, (v, col) in enumerate((("A1", GREY), ("M50", CORAL))):
            T = S[S.variante == v].set_index("série").reindex(ser); a.bar(x + (k - 0.5) * w, T.gain, w, yerr=1.96 * T.se, color=col, label="A1 (cible uniforme)" if v == "A1" else "M50 (cible mixte)", capsize=3)
        a.axhline(0, color="black", lw=0.8); a.axhline(0.02, color=TEAL, lw=1, ls="--"); a.set_xticks(x); a.set_xticklabels([s.replace(" (", "\n(") for s in ser], fontsize=8); a.set_title(title, fontsize=10)
    ax[0].set_ylabel("gain de macro-F1 (palier A)\nsur la régression logistique"); ax[0].legend(fontsize=8, loc="upper right"); fig.suptitle("Le décodage équilibré gagne ; seule la cible mixte (M50) tient quand des classes sont absentes", fontsize=12); fig.tight_layout(); p = FIG / "p2_decodage_gains.png"; fig.savefig(p); plt.close(fig); return p, G
def fig_verdicts():
    fam = collections.OrderedDict([("A", "A (découpage)"), ("B", "B (classification)"), ("C", "C (inconnus)"), ("V", "V (bruit)"), ("T", "T (Transformer)"), ("D", "D (attaques)"), ("E", "E (calibration)"), ("F", "F (représentation)"), ("I", "I (rejet par famille)"), ("X", "W2-W4 (affinages)"), ("Y", "W3 (présence)"), ("Z", "W4 (axes, bagging)"), ("W", "W1"), ("O", "W5 (inconnus décodés)"), ("R", "W6 (V-REx, embeddings)"), ("L", "W7 (LP-FT)"), ("M", "W7 (MLM)"), ("G", "ronde 3 (non lancée)")])
    cnt = collections.defaultdict(collections.Counter)
    for i, L in E.items():
        if L[-1]["type"] == "hypothese" and i[0] == "H": cnt[i[1]][L[-1]["statut"]] += 1
    keys = [k for k in fam if k in cnt]; st = [("confirmée", TEAL), ("réfutée", CORAL), ("non tranchée", SAND), ("préinscrite", GREY)]; fig, ax = plt.subplots(figsize=(11, 4.4)); bot = np.zeros(len(keys))
    for s, c in st: v = np.array([cnt[k][s] for k in keys]); ax.bar(range(len(keys)), v, bottom=bot, color=c, label=s); bot += v
    ax.set_ylim(0, max(bot) * 1.15); ax.set_xticks(range(len(keys))); ax.set_xticklabels([fam[k] for k in keys], rotation=35, ha="right", fontsize=9); ax.set_ylabel("nombre d'hypothèses"); ax.legend(ncol=4, fontsize=9); ax.set_title("Toutes les hypothèses préinscrites, avec leur verdict final", fontsize=12); fig.tight_layout(); p = FIG / "p2_verdicts.png"; fig.savefig(p); plt.close(fig); return p, cnt
def fig_open():
    rows = [("Bloc C\n(125 unités)", 0.623, 0.666), ("I4\n(25)", None, None), ("I7a\n(25)", None, None), ("I7b\n(25)", None, None), ("I7c\n(75)", None, None)]
    I4 = pd.read_csv(RES / "I4_resume.csv", index_col=0); rows[1] = ("I4\n(25)", I4.loc["msp", "auroc"], I4.loc["fam_msp", "auroc"])
    for k, f, nm in ((2, "I7a", "I7a\n(25)"), (3, "I7b", "I7b\n(25)"), (4, "I7c", "I7c\n(75)")):
        d = pd.read_csv(RES / f"{f}_resume.csv", index_col=0); rows[k] = (nm, d.loc["C4_msp", "auroc"], d.loc["C64_fam_negent", "auroc"])
    fig, ax = plt.subplots(figsize=(9, 4.2)); x = np.arange(len(rows)); ax.bar(x - 0.2, [r[1] for r in rows], 0.38, color=GREY, label="confiance de classe (MSP)"); ax.bar(x + 0.2, [r[2] for r in rows], 0.38, color=CORAL, label="confiance de famille")
    ax.axhline(0.8, color=TEAL, ls="--", lw=1); ax.text(len(rows) - 0.5, 0.805, "critère « acceptable » 0,80", color=TEAL, ha="right", fontsize=9); ax.set_ylim(0.5, 0.85); ax.set_xticks(x); ax.set_xticklabels([r[0] for r in rows]); ax.set_ylabel("AUROC d'inconnu"); ax.legend(loc="upper left"); ax.set_title("Détecter une classe inconnue : la famille gagne +0,04, partout, mais reste loin de 0,80", fontsize=11); fig.tight_layout(); p = FIG / "p2_inconnus.png"; fig.savefig(p); plt.close(fig); return p
def fig_ladder():
    d = pd.read_csv(RES / "W3d_all_units.csv"); X = d[d.cond == "toutes"].pivot_table(index=["repeat", "fold"], columns="variant", values="f1A"); a = pd.read_csv(RES / "A_all_units.csv") if (RES / "A_all_units.csv").exists() else None
    v0 = 0.5032; lab = ["SVM mots\n(25 plis)", "Régression\nlogistique", "+ décodage M50", "+ décodage A1\n(toutes classes)"]; val = [v0, X["LR"].mean(), X["M50"].mean(), X["A1"].mean()]; col = [GREY, GREY, CORAL, SAND]
    fig, ax = plt.subplots(figsize=(8.4, 4.2)); b = ax.bar(lab, val, color=col)
    for r, v in zip(b, val): ax.text(r.get_x() + r.get_width() / 2, v + 0.004, f"{v:.3f}", ha="center", fontsize=11)
    ax.set_ylim(0.45, 0.6); ax.set_ylabel("macro-F1 du palier A"); ax.set_title("De 0,50 à 0,55 : le seul levier établi sur les classes connues", fontsize=11); fig.tight_layout(); p = FIG / "p2_echelle_scores.png"; fig.savefig(p); plt.close(fig); return p, X
pD, GD = fig_decoding(); pV, CNT = fig_verdicts(); pO = fig_open(); pL, XL = fig_ladder()
def verdict_table():
    out = ["| Id | Hypothèse | Verdict final | Historique |", "|---|---|---|---|"]
    for i, L in E.items():
        if L[-1]["type"] != "hypothese": continue
        out.append(f"| {i} | {L[-1]['titre'].replace('|', '/')} | **{L[-1]['statut']}** | {' → '.join(x['statut'] for x in L)} |")
    return "\n".join(out)
def results_block(ids): return "\n\n".join(f"**{i} : {last(i)['titre']}** — {res(i)}" for i in ids if i in E)
d3 = pd.read_csv(RES / "W3d_tests.csv"); g = lambda v, c: d3[(d3.variante == v) & (d3.condition == c)].iloc[0]
# ---------- cellules ----------
cells += [md("""
<!-- PARTIE-2 -->
---
# Partie 2 : l'étude statistique v3 (protocole préinscrit, résultats de la v1 conservés)

*Cette partie est **ajoutée** à la fin du notebook : rien de la partie 1 (v1) n'est retiré ni réécrit. Quand un même résultat existe en v1 et en v3, les deux séries sont montrées côte à côte.*
""")]
cells += [md("""
## P2.0 Pourquoi une partie 2, et selon quelles règles
**En simple.** Le TP a d'abord été fait avec un seul découpage et un test ouvert une fois. Cela donne un chiffre, pas une preuve : on ne sait pas si l'écart entre deux méthodes est réel ou dû au hasard du découpage. La partie 2 refait l'étude avec **des règles écrites avant de regarder les chiffres**.

| Règle | Contenu |
|---|---|
| Préinscription | chaque hypothèse est écrite, avec sa règle de décision, **avant** le calcul (journal append-only `artifacts/results/v3/journal.jsonl`) |
| Verdict | toute hypothèse reçoit un verdict : confirmée, réfutée ou non tranchée |
| Rien ne se supprime | un résultat corrigé devient une **nouvelle entrée** ; l'ancienne reste (OpenMax inversé, Friedman à l'envers, deux erreurs de procédure : tout est tracé) |
| Unité statistique | le **gabarit** (≈ 311), pas le log ; plis par groupes de gabarits |
| Sélection puis confirmation | on choisit sur des plis, on confirme sur des plis **jamais vus** ; le maximum d'une grille est biaisé vers le haut |
| Plusieurs tests | intervalle de confiance bootstrap, Wilcoxon, test des signes, test de permutation, Holm |
| Test v2 scellé | 57 gabarits jamais lus ; une seule ouverture, à la fin, sur un pipeline gelé ; empreinte et garde automatique (`scripts/check_test_seal.py`, crochet git bloquant) |
""")]
cells += [md(f"""
## P2.1 Données et protocole v3
- **Développement** : {254} gabarits, 30 classes, 400 logs au plus par gabarit ; **test v2** : 57 gabarits (17,6 % des logs), scellé (D1, D27).
- **Protocoles** : P0 au hasard, P1 simple par gabarit, **P2 validation par groupes 5 plis × 5 répétitions (par défaut)**, P3 imbriqué.
- **Rotations** : 5 jeux de 6 classes masquées pour simuler des classes inconnues ; trois autres jeux de 5 rotations (I7a, I7b, I7c) pour confirmer.
- **Mesure principale** : macro-F1 du palier A (18 classes de 5 gabarits ou plus) ; open-set : AUROC et FPR@95.

**En simple.** « Gabarit » = la forme fixe d'un log (ex. « l'utilisateur X a ouvert le fichier Y »). Un découpage au hasard met des logs du même gabarit des deux côtés : le modèle triche en reconnaissant le gabarit. Découper par gabarit mesure la vraie généralisation.
""")]
cells += [md(f"""
## P2.2 Bloc A : le découpage change tout
{results_block(['RA1'])}

**En simple.** Même modèle, même données : 0,986 si on découpe au hasard, 0,50 si on découpe par gabarit. Le « presque parfait » de l'article vient de gabarits déjà vus. Les protocoles par gabarit (P1, P2, P3) donnent tous le même niveau : ce n'est pas un défaut du protocole.
""")]
cells += [md(f"""
## P2.3 Bloc B : quel classifieur ?
{results_block(['RB1'])}

**En simple.** 19 façons de classer donnent presque le même score (entre 0,40 et 0,50). La hiérarchie d'ECS (familles) ne l'améliore pas ; le clustering fait moins bien que le SVM.
""")]
cells += [md(f"""
## P2.4 Bloc C : détecter une classe inconnue
{results_block(['RC1', 'RC2', 'RC3', 'RC4'])}

![inconnus](artifacts/figures/p2_inconnus.png)

**En simple.** Aucune méthode connue (OpenMax, Mahalanobis, kNN, énergie…) ne bat la simple confiance du modèle, sauf **la confiance sur la famille** (+0,04 d'AUROC, confirmé sur 75 unités de rotations jamais vues). Mais même elle reste loin de 0,80 : en gardant 95 % des logs connus, environ 85 % des inconnus passent.
""")]
cells += [md(f"""
## P2.5 Vectorisation × bruit, Transformer, attaques, calibration
{results_block(['RV1', 'RT1', 'RT2', 'RD1', 'RE1'])}

**En simple.** (1) Les lettres résistent mieux au bruit que les mots. (2) Un Transformer réglé sur 140 logs par classe ne bat pas TF-IDF (0,469 contre 0,523 sur 20 couples de plis) et la fusion n'aide pas. (3) Les homoglyphes (lettres trompeuses) font perdre jusqu'à 48 % ; la **table officielle UTS #39** les annule ; l'entraînement adversarial seul ne protège pas d'une attaque jamais vue (v1, étape 9). (4) La température ne corrige pas la confiance sous décalage de gabarits.
""")]
cells += [md(f"""
## P2.6 La phase 2 : chercher à dépasser 0,50, itération par itération
Chaque itération a ses hypothèses préinscrites, une sélection, puis une confirmation sur des plis neufs.

{results_block(['RI1', 'RI1b', 'RI2', 'RI5', 'RI6', 'RW1', 'RW2'])}

**En simple.** Changer le vocabulaire, les jetons, les réglages, les racines, l'IDF, le format, la structure (champs typés), le bagging, la pondération des gabarits, V-REx ou les embeddings gelés : **aucun effet établi**. Un seul levier a marché : changer la façon de **décider**, pas de représenter.
""")]
cells += [md(f"""
## P2.7 Le résultat principal : le décodage à masses équilibrées (formule maison)
**Idée.** Le modèle laisse certaines classes « avaler » des gabarits entiers d'autres classes (par exemple `authentication-failed` : 43 gabarits). On corrige en demandant que la masse prédite sur le lot soit mieux répartie entre classes. Sur le lot de test (sans étiquette), on met à l'échelle les colonnes des probabilités (algorithme de Sinkhorn amorti, exposant 0,5, 10 itérations) vers une cible. **A1** : cible uniforme. **M50** : cible mixte, moitié uniforme et moitié prior observé.

![gains](artifacts/figures/p2_decodage_gains.png)

![échelle](artifacts/figures/p2_echelle_scores.png)

| Condition (100 plis, répétitions 20-39) | Gain de M50 sur la régression logistique | IC95 | Signes |
|---|---|---|---|
| toutes les classes présentes | {g('M50', 'toutes')['gain']:+.4f} | {ci(g('M50', 'toutes')['IC95_bas'], g('M50', 'toutes')['IC95_haut'])} | {g('M50', 'toutes')['signes +/-']} |
| 8 classes absentes | {g('M50', 'abs8')['gain']:+.4f} | {ci(g('M50', 'abs8')['IC95_bas'], g('M50', 'abs8')['IC95_haut'])} | {g('M50', 'abs8')['signes +/-']} |
| 14 classes absentes | {g('M50', 'abs14')['gain']:+.4f} | {ci(g('M50', 'abs14')['IC95_bas'], g('M50', 'abs14')['IC95_haut'])} | {g('M50', 'abs14')['signes +/-']} |

{results_block(['RW3', 'RW3d'])}

**Limites à lire absolument.** (1) Décodage **transductif** : il utilise la composition du lot de test, sans étiquette, pas seulement chaque log séparément. (2) La cible uniforme (A1) s'effondre quand beaucoup de classes sont absentes (HX6) : on garde M50. (3) À 14 classes absentes, M50 ne gagne plus de façon significative. (4) Le gain porte sur le palier A, pas sur les classes rares (HW8, HZ6 réfutées).

**En simple.** On ne change ni le modèle ni les données : on change la manière de trancher quand un lot de logs arrive. C'est comme corriger un jury qui donne presque tous ses prix à quelques candidats très connus.
""")]
cells += [md(f"""
## P2.8 Ce qui n'a pas marché (résultats négatifs, conservés)
{results_block(['RW4', 'RW5', 'RW6'])}

**En simple.** Le produit d'experts objet × action améliore la classification brute (+0,035) mais ce gain est absorbé par le décodage ; le décodage ne sert pas à détecter les inconnus ; ni V-REx ni les embeddings gelés ne relèvent le score.
""")]
cells += [md(f"""
## P2.9 Registre complet des hypothèses

![verdicts](artifacts/figures/p2_verdicts.png)

{verdict_table()}
""")]
cells += [md("""
## P2.10 Limites, menaces à la validité, erreurs reconnues
- **Données** : un seul jeu **synthétique** (SIEVE_00), 311 gabarits **reconstruits** (440 annoncés) ; taxonomie à 8 familles = hypothèse de démonstration ; axes objet × action tirés des noms de classes.
- **Statistique** : plis dépendants (mêmes gabarits) ; beaucoup de « réfutées » ont un intervalle trop large pour exclure +0,01 ; le test des signes est le plus sévère (HY8 puis HY9, HZ7 : 31 plis sur 50 donnent p = 0,0595).
- **Transduction** : le décodage M50 suppose un lot de test.
- **Erreurs de procédure, reconnues et tracées** : OpenMax implémenté à l'envers ; rangs de Friedman lus à l'envers ; une unité de résultat supprimée par erreur (valeurs conservées, RW4smoke) ; deux versions de script enregistrées avec une description fausse (corrections ajoutées) ; défaut de formule d'une pondération non bornée (DRO1).
- **Test v2** : toujours scellé au moment de cette rédaction ; une seule ouverture, à la fin, sur le pipeline gelé (TF-IDF mots → régression logistique C = 10 → décodage M50 ; rejet par confiance de famille brute).
""")]
cells += [md("""
## P2.11 Fiche de questions de vérification (partie 2)
| Question | Réponse courte |
|---|---|
| Pourquoi 0,50 et pas 0,97 ? | Le 0,97 vient de gabarits déjà vus (découpage au hasard). Par gabarit : 0,50 (bloc A). |
| Qu'est-ce qui a vraiment amélioré le score ? | Le décodage à masses équilibrées M50 : +0,05 (toutes classes) et +0,035 (8 classes absentes) sur 100 plis. |
| Pourquoi M50 et pas A1 ? | A1 perd son gain, voire nuit (−0,036) quand beaucoup de classes sont absentes du lot ; M50 reste positif. |
| Le décodage est-il de la triche ? | Non, mais il est **transductif** : il lit la composition du lot de test, sans étiquette. C'est dit. |
| Quel score pour détecter les inconnus ? | AUROC 0,65-0,69 par la famille (+0,04 sur le MSP, confirmé) ; FPR@95 ≈ 0,85 ; loin de 0,80. |
| Pourquoi tant d'hypothèses réfutées ? | Parce qu'elles étaient écrites avant de voir les chiffres ; une réfutation est un résultat. |
| Que veut dire « non tranchée » ? | L'intervalle est trop large pour conclure dans un sens ou dans l'autre. |
| Comment sait-on que le test n'a pas servi à choisir ? | Journal d'accès vide, empreinte SHA-256 des 57 identifiants, garde automatique au commit. |
| Qu'a appris l'entraînement adversarial ? | Il aide contre les attaques vues, pas contre une attaque nouvelle ; la normalisation par la table officielle UTS #39 est la parade qui généralise (v1 9.12, v3 HD5). |
""")]
# ---------- écriture ----------
nb = json.load(open(NB)); old = [c for c in nb["cells"] if not c.get("metadata", {}).get("part2")]; had = len(nb["cells"]) - len(old)
if had == 0:   # première construction seulement : les relances ne régénèrent que les cellules de la partie 2 (cellules v1 vérifiées identiques)
    arc = ROOT / "archive" / f"{time.strftime('%Y-%m-%d_%H%M')}_avant_partie2_notebook"; arc.mkdir(parents=True, exist_ok=True); shutil.copy2(NB, arc / NB.name)
nb["cells"] = old + cells; json.dump(nb, open(NB, "w"), ensure_ascii=False, indent=1); print(f"cellules v1 conservées : {len(old)} ; cellules de la partie 2 : {len(cells)} (avant : {had}) ; figures : {pD.name}, {pV.name}, {pO.name}, {pL.name}")
