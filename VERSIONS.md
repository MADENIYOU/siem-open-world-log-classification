# Versions des fichiers, scripts et documents
Généré à partir de `artifacts/results/v3/versions.jsonl` (append-only, ne pas modifier à la main). Pour chaque version : ce qu'elle fait, pourquoi elle remplace la précédente, pourquoi elle a été remplacée par la suivante, et où retrouver le fichier (copie dans `versions/` ou commit git). On ne supprime jamais une version.

## Présentation (presentation/Soutenance_SIEM_monde_ouvert.pptx et build_deck.js)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **V1** | 2026-11-06 09:30 | 16 diapositives, une par point demandé, avec cartes, tuiles de chiffres et figures du notebook. | première version | L'étudiant a jugé la V1 « trop PPT généré par IA » : recherche sourcée des indices d'un PPT généré par IA, puis refonte qui les respecte. (par V2) | `versions/presentation/build_deck__V1.js`, commit 63a843a |
| **V2** | 2026-11-06 10:45 | 17 diapositives : titres d'action, fond blanc, une couleur d'accent, citations numérotées [n] et diapositive de références après le Merci. | L'étudiant a jugé la V1 « trop PPT généré par IA » : recherche sourcée des indices d'un PPT généré par IA, puis refonte qui les respecte. | L'étudiant a constaté que les titres des points demandés avaient disparu au profit de phrases-messages ; il a demandé de les restaurer et de combiner le meilleur de la V1 et de la V2. (par V3) | `versions/presentation/build_deck__V2.js`, commit f14934c |
| **V3** | 2026-11-06 10:52 | 17 diapositives : intitulés exacts des points en titre (en haut à gauche), phrase-message dessous, liens cliquables dans les références, nom complet de l'auteur. | L'étudiant a constaté que les titres des points demandés avaient disparu au profit de phrases-messages ; il a demandé de les restaurer et de combiner le meilleur de la V1 et de la V2. | Les schémas de la diapositive des données, réduits dans une mosaïque, étaient illisibles. (par V3.1) | `versions/presentation/build_deck__V3.js`, commit c5ba24d |
| **V3.1** | 2026-11-06 10:56 | 19 diapositives : « Présentation des données » en trois diapositives, taxonomie et rotations redessinées en natif. | Les schémas de la diapositive des données, réduits dans une mosaïque, étaient illisibles. | Audit diapositive par diapositive pour un public non spécialiste : six diapositives incompréhensibles seules. (par V3.2) | `versions/presentation/build_deck__V3.1.js`, commit a35f8ce |
| **V3.2** | 2026-11-06 11:25 | 22 diapositives : ligne « En clair », jargon défini, objectifs, méthodes et pipeline sans codes internes, résultats en quatre diapositives. | Audit diapositive par diapositive pour un public non spécialiste : six diapositives incompréhensibles seules. | L'étudiant a demandé que l'explication orale parle de la diapositive et apporte quelque chose de plus. (par V3.3) | `versions/presentation/build_deck__V3.2.js`, commit 483deb8 |
| **V3.3** | 2026-11-06 11:30 | Mêmes diapositives ; notes de l'orateur réécrites en discours oral qui apporte un plus. | L'étudiant a demandé que l'explication orale parle de la diapositive et apporte quelque chose de plus. | Trop de texte à l'écran sur certaines diapositives. (par V3.4) | `versions/presentation/build_deck__V3.3.js`, commit 1cb8c18 |
| **V3.4** | 2026-11-06 11:34 | Texte allégé sur les diapositives denses (2 à 8, 10, 13, 14, résultats). | Trop de texte à l'écran sur certaines diapositives. | Retours détaillés de l'étudiant : états de l'art incohérents, gabarits donnant l'impression d'un second jeu de données, résultats non comparables, limites non reliées aux objectifs, références à compléter. (par V4) | `versions/presentation/build_deck__V3.4.js`, commit df4bd39 |
| **V4** | 2026-11-07 20:54 | 30 diapositives : état de l'art en un bloc par diapositive, gabarits reliés aux six fichiers SIEVE, cycle graphique des méthodes, temps Mac et Colab séparés, résultats à métriques communes et attaques par degré, limites et conclusion par objectifs, références complètes. | Retours détaillés de l'étudiant : états de l'art incohérents, gabarits donnant l'impression d'un second jeu de données, résultats non comparables, limites non reliées aux objectifs, références à compléter. | Le test ne doit servir qu'une fois, jamais dans la boucle ; il fallait nommer le jeu sur lequel on découpe et expliquer les relations entre les nombres. (par V4.1) | `versions/presentation/build_deck__V4.js`, commit 2aeb456 |
| **V4.1** | 2026-11-07 21:03 | 30 diapositives : test scellé hors de la boucle des méthodes, jeu de données nommé (SIEVE), graphiques natifs de la fuite, « Comment lire » et « Ce qu'on en tire » sur les résultats. | Le test ne doit servir qu'une fois, jamais dans la boucle ; il fallait nommer le jeu sur lequel on découpe et expliquer les relations entre les nombres. | **version courante** | `versions/presentation/build_deck__V4.1.js`, commit 6afc705 |

## Notebook (TP2_logs_hierarchique_monde_ouvert.ipynb)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **N1** | 2026-11-06 09:30 | Notebook du protocole v1 : étapes 0 à 10, 312 cellules, 0 erreur, registre V1 à V99, journal du test v1 (ouvert le 2026-11-05). | première version | **version courante** | non conservée (voir note) |
|  |  | *Note : Archivé dans `archive/2026-11-07_avant_v3/` et étiquette git `etat-2026-11-07-avant-v3`. La version suivante (partie 2, protocole v3) n'existe pas encore : elle ajoutera des sections sans retirer N1.* |  |  |  |

## src/tp2_runner.py (exécuteur reprenable)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **R1** | 2026-11-07 21:24 | Une unité = une configuration ; si le résultat existe on le recharge, sinon on calcule ; registre append-only ; écriture atomique. | première version | Règle R3 de l'étudiant : on ne supprime jamais un résultat précédent. (par R2) | `versions/src/tp2_runner__R1.py`, commit dd53267 |
| **R2** | 2026-11-07 21:54 | Comme R1, et un recalcul forcé archive l'ancien résultat au lieu de l'écraser ; `load_block` ignore les fichiers archivés. | Règle R3 de l'étudiant : on ne supprime jamais un résultat précédent. | **version courante** | commit ccd459e |
|  |  | *Note :  Fichier non retrouvé dans git.* |  |  |  |

## src/tp2_stats.py (outils statistiques)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **S1** | 2026-11-07 21:24 | Bootstrap par gabarits, Wilcoxon, Friedman et Nemenyi, Holm, tailles d'effet, tendances, concordance de Kendall ; 15 tests unitaires. | première version | **version courante** | `versions/src/tp2_stats__S1.py`, commit dd53267 |

## src/tp2_split_v3.py (découpage v3)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SP1** | 2026-11-07 21:24 | Développement : 5 plis × 5 répétitions de groupes ; test scellé v2 : 57 gabarits jamais utilisés en test, critères d'acceptation écrits d'avance. | première version | **version courante** | `versions/src/tp2_split_v3__SP1.py`, commit dd53267 |

## scripts/v3_blockA.py (bloc A : protocoles de découpage)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **A1** | 2026-11-07 21:28 | Quatre protocoles (P0, P1, P2, P3) × six modèles linéaires, 400 logs au plus par gabarit, une unité par pli. | première version | **version courante** | `versions/scripts/v3_blockA__A1.py`, commit e0538bc |
|  |  | *Note : Un premier essai s'était arrêté sur une erreur (pandas 3 : groupby.apply sans la colonne de groupe), corrigé avant tout résultat ; aucun résultat de cet essai.* |  |  |  |

## scripts/v3_blockA_paired.py (HA1b : montage apparié)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **HA1b-1** | 2026-11-07 22:11 | Mêmes logs de test, entraînement avec ou sans logs des gabarits de test : effet pur de la fuite. | première version | **version courante** | `versions/scripts/v3_blockA_paired__HA1b-1.py`, commit 3d73b0c |

## scripts/v3_blockB.py (bloc B : classifieurs et clustering)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **B1** | 2026-11-07 22:05 | 18 modèles dont DBSCAN et HDBSCAN avec rejet seulement (point de bruit ou trop loin = rejeté). | première version | Le test de fumée de B1 a montré 95 % (DBSCAN) et 88 % (HDBSCAN) de rejets : sans variante sans rejet, la comparaison de classification n'aurait pas de sens (amendement de D8). (par B2) | non conservée (voir note) |
|  |  | *Note : Jamais enregistrée dans git : le fichier a été modifié avant le premier commit. Seule trace : le résultat du test de fumée (unité `cd36dcc072af2134`, répétition 0, pli 0, dans `artifacts/results/v3/B_classification/`).* |  |  |  |
| **B2** | 2026-11-07 22:11 | 20 modèles : DBSCAN et HDBSCAN avec et sans rejet (sorties `_sub` et `_sub_rej`). | Le test de fumée de B1 a montré 95 % (DBSCAN) et 88 % (HDBSCAN) de rejets : sans variante sans rejet, la comparaison de classification n'aurait pas de sens (amendement de D8). | **version courante** | `versions/scripts/v3_blockB__B2.py`, commit 3d73b0c |

## src/tp2_journal.py (journal append-only)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **J1** | 2026-11-07 21:54 | Règles, décisions, hypothèses et résultats ; une nouvelle version d'une entrée ne remplace jamais l'ancienne. | première version | **version courante** | commit ccd459e |
|  |  | *Note :  Fichier non retrouvé dans git.* |  |  |  |

## scripts/archive_state.py (archives non écrasables)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AR1** | 2026-11-07 21:54 | Copie un état du projet dans archive/ avec empreintes ; refuse d'écraser une archive. | première version | **version courante** | commit ccd459e |
|  |  | *Note :  Fichier non retrouvé dans git.* |  |  |  |

## etat_de_l_art/sources_v3_stats_repro.md

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SRC1** | 2026-11-07 21:40 | 62 références vérifiées (découpage, tests statistiques, reproductibilité, métriques) + 1 complément (Field et Welsh). | première version | **version courante** | `versions/etat_de_l_art/sources_v3_stats_repro__SRC1.md`, commit 51154ea |

## etat_de_l_art/sources_v3_methodes.md

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SRC1** | 2026-11-07 21:40 | 89 références vérifiées (hiérarchie, prototypes, inconnus, logs, vectorisation, calibration, attaques, fusion). | première version | **version courante** | `versions/etat_de_l_art/sources_v3_methodes__SRC1.md`, commit 51154ea |
