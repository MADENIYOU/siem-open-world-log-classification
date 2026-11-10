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
| **R2** | 2026-11-07 21:54 | Comme R1, et un recalcul forcé archive l'ancien résultat au lieu de l'écraser ; `load_block` ignore les fichiers archivés. | Règle R3 de l'étudiant : on ne supprime jamais un résultat précédent. | L'étudiant a demandé que la perte d'une version de script (B1) ne se reproduise pas : la conservation ne doit plus dépendre d'un commit ni d'un oubli. (par R3) | `versions/src/tp2_runner__R2.py`, commit ccc459e |
|  |  | *Note : Fichier non retrouvé dans git. Correction du 2026-11-07 22:18 (faute de frappe sur le hachage du commit : ccc459e et non ccd459e ; copie figée créée depuis le bon commit) : ancienne valeur {'commit': 'ccd459e', 'fichier': None}.* |  |  |  |
| **R3** | 2026-11-07 22:18 | Comme R2, et copie automatique du code exact (script lancé et modules `src/tp2_*.py`) dans `versions/auto/` au premier calcul de chaque processus ; l'empreinte du code est enregistrée dans chaque résultat et dans le registre. | L'étudiant a demandé que la perte d'une version de script (B1) ne se reproduise pas : la conservation ne doit plus dépendre d'un commit ni d'un oubli. | **version courante** | `versions/src/tp2_runner__R3.py` |

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
| **J1** | 2026-11-07 21:54 | Règles, décisions, hypothèses et résultats ; une nouvelle version d'une entrée ne remplace jamais l'ancienne. | première version | **version courante** | `versions/src/tp2_journal__J1.py`, commit ccc459e |
|  |  | *Note : Fichier non retrouvé dans git. Correction du 2026-11-07 22:18 (faute de frappe sur le hachage du commit : ccc459e et non ccd459e ; copie figée créée depuis le bon commit) : ancienne valeur {'commit': 'ccd459e', 'fichier': None}.* |  |  |  |

## scripts/archive_state.py (archives non écrasables)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AR1** | 2026-11-07 21:54 | Copie un état du projet dans archive/ avec empreintes ; refuse d'écraser une archive. | première version | **version courante** | `versions/scripts/archive_state__AR1.py`, commit ccc459e |
|  |  | *Note : Fichier non retrouvé dans git. Correction du 2026-11-07 22:18 (faute de frappe sur le hachage du commit : ccc459e et non ccd459e ; copie figée créée depuis le bon commit) : ancienne valeur {'commit': 'ccd459e', 'fichier': None}.* |  |  |  |

## etat_de_l_art/sources_v3_stats_repro.md

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SRC1** | 2026-11-07 21:40 | 62 références vérifiées (découpage, tests statistiques, reproductibilité, métriques) + 1 complément (Field et Welsh). | première version | **version courante** | `versions/etat_de_l_art/sources_v3_stats_repro__SRC1.md`, commit 51154ea |

## etat_de_l_art/sources_v3_methodes.md

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SRC1** | 2026-11-07 21:40 | 89 références vérifiées (hiérarchie, prototypes, inconnus, logs, vectorisation, calibration, attaques, fusion). | première version | **version courante** | `versions/etat_de_l_art/sources_v3_methodes__SRC1.md`, commit 51154ea |

## etat_de_l_art/sources_v3_clustering.md

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **SRC1** | 2026-11-07 22:20 | 50 références vérifiées sur les types de clustering (k-means, hiérarchique, mélanges gaussiens, densité, BIRCH et spectral, clustering pour classer ou détecter l'inconnu, évaluation, documentation scikit-learn 1.9.1). | première version | **version courante** | `versions/etat_de_l_art/sources_v3_clustering__SRC1.md` |
|  |  | *Note : 10 références n'ont que titre, auteurs, revue et année (notice Crossref ; éditeurs inaccessibles). Contrôle par sondage : 3 pages rouvertes, conformes.* |  |  |  |

## src/tp2_versions.py (versionnage)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **V1** | 2026-11-07 22:14 | Registre append-only des versions (ce que fait la version, pourquoi elle remplace la précédente) et copies figées. | première version | Une faute de frappe sur un hachage de commit avait été enregistrée (ccd459e au lieu de ccc459e) : le registre doit refuser ce cas et permettre de corriger sans réécrire. (par V2) | `versions/src/tp2_versions__V1.py`, commit 4126e97 |
|  |  | *Note : Correction du 2026-11-07 22:19 (la date de V1 était celle de l'enregistrement tardif ; la vraie date est celle du commit 4126e97) : ancienne valeur {'date': '2026-11-07 22:30'}.* |  |  |  |
| **V2** | 2026-11-07 22:18 | Comme V1, avec refus d'un commit inexistant et fonction `correct` (correction ajoutée au journal, ancienne valeur conservée). | Une faute de frappe sur un hachage de commit avait été enregistrée (ccd459e au lieu de ccc459e) : le registre doit refuser ce cas et permettre de corriger sans réécrire. | Une version enregistrée après coup (V1) s'affichait après V2 et semblait lui succéder : l'ordre doit suivre les dates. (par V3) | `versions/src/tp2_versions__V2.py` |
| **V3** | 2026-11-07 22:19 | Comme V2, avec tri chronologique des versions à l'affichage. | Une version enregistrée après coup (V1) s'affichait après V2 et semblait lui succéder : l'ordre doit suivre les dates. | **version courante** | `versions/src/tp2_versions__V3.py` |

## scripts/check_versions.py (contrôle de conservation)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **CV1** | 2026-11-07 22:18 | Vérifie que l'état courant de chaque script, module, générateur de présentation et notebook est conservé (copie ou commit) ; `--fix` fige dans `versions/auto/` ceux qui ne le sont pas. | première version | **version courante** | `versions/scripts/check_versions__CV1.py` |

## scripts/hooks/pre-commit (crochet git de conservation)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **H1** | 2026-11-07 22:22 | Avant chaque commit, fige dans `versions/auto/` tout état de script, module, notebook ou générateur non conservé et l'ajoute au commit ; ne bloque jamais le commit. Copie versionnée ; installation : `cp scripts/hooks/pre-commit .git/hooks/pre-commit`. | première version | **version courante** | `versions/scripts/hooks/pre-commit__H1` |

## scripts/v3_analyze_B.py (analyse du bloc B)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AB1** | 2026-11-07 22:28 | Analyse des hypothèses HB1 à HB7 sur toutes les unités du dossier B_classification. | première version | Le dossier du bloc B contenait aussi l'unité de fumée B1 (répétition 0, pli 0, autre liste de modèles) : elle aurait été moyennée avec l'unité B2 du même pli et aurait faussé les valeurs de ce pli, surtout pour DBSCAN et HDBSCAN. (par AB2) | `versions/scripts/v3_analyze_B__AB1.py` |
| **AB2** | 2026-11-07 22:29 | Comme AB1, en ne lisant que les unités du script B2 (exclut l'unité de fumée B1). | Le dossier du bloc B contenait aussi l'unité de fumée B1 (répétition 0, pli 0, autre liste de modèles) : elle aurait été moyennée avec l'unité B2 du même pli et aurait faussé les valeurs de ce pli, surtout pour DBSCAN et HDBSCAN. | **version courante** | `versions/scripts/v3_analyze_B__AB2.py` |

## EXPLICATIONS_V3.md (explications demandées par l'étudiant)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **E1** | 2026-11-07 22:30 | Huit explications en mots simples : origine des 440 gabarits, F1 et macro-F1, explications orales des diapositives, bloc A, Wilcoxon, Friedman et Holm, pourquoi HA1 a été rejouée, méthodes du bloc B (dont le clustering), résultats du bloc B. | première version | Nouvelle explication à noter après le bloc C (règle : toute explication est notée) ; l'index est complété, rien n'est retiré. (par E2) | `versions/EXPLICATIONS_V3__E1.md` |
|  |  | *Note : Document qui s'allonge : toute nouvelle explication demandée y est ajoutée dans une nouvelle version, sans rien retirer.* |  |  |  |
| **E2** | 2026-11-07 23:12 | E1 plus E9 : les scores d'inconnu du bloc C, leur principe et leurs résultats en mots simples. | Nouvelle explication à noter après le bloc C (règle : toute explication est notée) ; l'index est complété, rien n'est retiré. | Explications demandées par l'étudiant (Weibull et LOF) et correction d'une explication fausse de E9 ; le texte erroné de E9 est conservé dans la version E2 et signalé par un renvoi, pas supprimé. (par E3) | `versions/EXPLICATIONS_V3__E2.md` |
| **E3** | 2026-11-09 12:38 | E2 plus E9b (correction de E9), E10 (loi de Weibull et OpenMax), E11 (LOF) et E12 (vectorisation × bruit). | Explications demandées par l'étudiant (Weibull et LOF) et correction d'une explication fausse de E9 ; le texte erroné de E9 est conservé dans la version E2 et signalé par un renvoi, pas supprimé. | **version courante** | `versions/EXPLICATIONS_V3__E3.md` |

## scripts/v3_blockC.py (bloc C : détection d'inconnus)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **C1** | 2026-11-07 22:58 | 28 scores d'inconnu (tête TF-IDF, espace SVD, tête SVD, fusion) sur 5 rotations × 5 répétitions × 5 plis de groupes ; développement seul ; ASH, SCALE, DICE, NNGuide, SHE et ViM adaptés à des vecteurs signés. | première version | OpenMax de C1 lisait la formule de l'article à l'envers (probabilité de Weibull utilisée dans le mauvais sens) : AUROC de 0,465, sans valeur. Preuve : les versions C1 et corrigée sont presque des images miroirs unité par unité (diagnostic sur 15 unités, fichier artifacts/results/v3/C_diagnostic_openmax_lof.csv). (par C2) | `versions/scripts/v3_blockC__C1.py` |
| **C2** | 2026-11-07 23:24 | Comme C1, avec OpenMax corrigé selon le code de référence de Bendale et Boult ; tous les autres scores identiques. | OpenMax de C1 lisait la formule de l'article à l'envers (probabilité de Weibull utilisée dans le mauvais sens) : AUROC de 0,465, sans valeur. Preuve : les versions C1 et corrigée sont presque des images miroirs unité par unité (diagnostic sur 15 unités, fichier artifacts/results/v3/C_diagnostic_openmax_lof.csv). | **version courante** | `versions/scripts/v3_blockC__C2.py` |
|  |  | *Note : Correction du 2026-11-07 23:25 (le shell avait supprimé le nom du fichier de diagnostic dans le texte (accents graves)) : ancienne valeur {'pourquoi': "OpenMax de C1 lisait la formule de l'article à l'envers (probabilité de Weibull utilisée dans le mauvais sens) : AUROC de 0,465, sans valeur. Preuve : les versions C1 et corrigée sont presque des images miroirs unité par unité (diagnostic sur 15 unités, )."}.* |  |  |  |

## scripts/v3_analyze_C.py (analyse du bloc C)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AC1** | 2026-11-07 22:58 | Tableaux et tests des hypothèses HC1 à HC9 (Wilcoxon apparié, Holm, Friedman et Nemenyi, Mann-Whitney, variabilité entre rotations). | première version | Le calcul du bloc C a été refait (C2) après la correction d'OpenMax : il faut analyser C2 sans écraser les sorties de C1, conservées côte à côte. (par AC2) | `versions/scripts/v3_analyze_C__AC1.py` |
| **AC2** | 2026-11-07 23:39 | Comme AC1, avec la version du calcul en paramètre (par défaut C2) ; chaque version écrit ses propres fichiers (suffixe _C2) et ne réécrit jamais ceux de la version précédente. | Le calcul du bloc C a été refait (C2) après la correction d'OpenMax : il faut analyser C2 sans écraser les sorties de C1, conservées côte à côte. | **version courante** | `versions/scripts/v3_analyze_C__AC2.py` |

## scripts/v3_register_C.py et v3_register_B.py (préinscriptions)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **P1** | 2026-11-07 22:58 | Inscription au journal des décisions et hypothèses des blocs avant tout calcul. | première version | **version courante** | `versions/scripts/v3_register_C__P1.py` |

## scripts/v3_blockV.py (bloc V : vectorisation × bruit)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **V1** | 2026-11-07 23:39 | 3 vectorisations × 6 fichiers × 5 rotations × 2 répétitions × 5 plis (300 unités) ; macro-F1 des classes connues et AUROC (MSP, énergie, MSP de la famille) sur les mêmes logs. | première version | **version courante** | `versions/scripts/v3_blockV__V1.py` |

## scripts/v3_transformer_grid.py (bloc T : grille du Transformer)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **T1** | 2026-11-07 23:39 | DistilBERT × 6 fichiers × 5 rotations × 3 graines (90 modèles) ; baseline TF-IDF sur les mêmes logs ; logits conservés ; reprise à deux niveaux (unité et point de contrôle). | première version | **version courante** | `versions/scripts/v3_transformer_grid__T1.py` |

## scripts/v3_diag_C.py (diagnostic d'OpenMax et de LOF)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **DG1** | 2026-11-07 23:39 | Décompose le LOF (sparsité propre, densité du voisinage, rapport ; sensibilité à k et à la banque) et compare OpenMax C1 à la version du code de référence, sur 15 unités. | première version | **version courante** | `versions/scripts/v3_diag_C__DG1.py` |

## scripts/v3_register_VT.py (préinscriptions V et T)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **P2** | 2026-11-07 23:39 | Décision D13 et hypothèses HV1 à HV5, HT1 à HT4 inscrites avant tout calcul ; correction du texte de C2. | première version | **version courante** | `versions/scripts/v3_register_VT__P2.py` |

## scripts/v3_analyze_V.py (analyse du bloc V)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AV1** | 2026-11-09 12:38 | Tableaux et tests de HV1 à HV5 (Wilcoxon apparié, Spearman par bloc, Friedman, Holm). | première version | **version courante** | `versions/scripts/v3_analyze_V__AV1.py` |

## scripts/v3_verdicts_V.py (verdicts V et corrections C)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **VV1** | 2026-11-09 12:38 | Verdicts HV1 à HV5, résultat RV1, corrections RC1 version 2, RC3 (OpenMax) et RC4 (LOF). | première version | **version courante** | `versions/scripts/v3_verdicts_V__VV1.py` |

## scripts/v3_blockE.py (bloc E : calibration)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **E2** | 2026-11-09 12:45 | Comme E1, en écartant du test les logs « connus » dont la classe n'a aucun gabarit dans l'ensemble d'ajustement (classe non apprise par le modèle) et des jeux de calibration les logs de classes non apprises. | E1 s'arrêtait avec une erreur d'indice : certaines classes connues, ayant peu de gabarits, voyaient tous leurs gabarits tomber dans les jeux de calibration, donc le modèle ne les apprenait pas (22 classes au lieu de 24). L'unité de fumée E1 (rotation 1, pli 0) reste dans les résultats, avec la version E1. | **version courante** | `versions/scripts/v3_blockE__E2.py` |

## scripts/v3_blockD.py (bloc D : attaques par degré)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **D1** | 2026-11-09 12:48 | Trois attaques × cinq degrés + normalisation par la table officielle UTS #39, modèles mots et caractères, 25 unités ; mesures sur les mêmes logs (macro-F1 connu, AUROC MSP et famille, faux rejets). | première version | **version courante** | `versions/scripts/v3_blockD__D1.py` |

## scripts/v3_analyze_D.py (analyse du bloc D)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AD1** | 2026-11-09 12:48 | Tableaux et tests de HD1 à HD7 (Wilcoxon, Spearman par unité, Friedman et Nemenyi, Holm). | première version | **version courante** | `versions/scripts/v3_analyze_D__AD1.py` |

## scripts/v3_analyze_E.py (analyse du bloc E)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **AE1** | 2026-11-09 12:48 | Tableaux et tests de HE1 à HE6 (Wilcoxon contre « aucune », Holm, Friedman, couverture conforme). | première version | **version courante** | `versions/scripts/v3_analyze_E__AE1.py` |

## scripts/v3_register_DE.py (préinscriptions D et E)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **P3** | 2026-11-09 12:48 | Décisions D14 et D15 et hypothèses HD1 à HD7 et HE1 à HE6 inscrites avant tout calcul. | première version | **version courante** | `versions/scripts/v3_register_DE__P3.py` |

## scripts/v3_verdicts_E.py (verdicts du bloc E)

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **VE1** | 2026-11-09 12:49 | Verdicts HE1 à HE6 et résultat RE1 (v1 et v3 conservés). | première version | **version courante** | `versions/scripts/v3_verdicts_E__VE1.py` |

## I1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:05 | Itération I1 de la phase 2 : 10 variantes de représentation (vocabulaire restreint aux mots présents dans au moins 2/3/5 gabarits, marqueur de valeur, ensemble mots+lettres, pondération par gabarit) sous P2 25 plis, 30 classes | Première version : exécute les HF1 à HF6 préinscrites (D16) ; ne remplace rien | **version courante** | `versions/scripts/v3_phase2_I1__1.py` |

## AD1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:07 | Analyse du bloc D (attaques) : tests appariés, Friedman/Nemenyi, Spearman, normalisation | Première version | **version courante** | `versions/scripts/v3_analyze_D__1.py` |

## VD1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:07 | Verdicts HD1 à HD7 et résultat RD1 | Première version | **version courante** | `versions/scripts/v3_verdicts_D__1.py` |

## AI1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:14 | Analyse de l'itération I1 (tests HF1-HF6) | Première version | **version courante** | `versions/scripts/v3_analyze_I1__1.py` |

## VI1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:14 | Verdicts HF1 à HF6 et résultat RI1 | Première version | **version courante** | `versions/scripts/v3_verdicts_I1__1.py` |

## RI1reg

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:14 | Préinscription de l'itération I1 (D16, HF1 à HF6) | Première version | **version courante** | `versions/scripts/v3_register_I1__1.py` |

## RI1b

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:17 | Préinscription D17, HF7 à HF9 (confirmation du constat exploratoire d'I1) | Première version | **version courante** | `versions/scripts/v3_register_I1b__1.py` |

## I1b

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:17 | Confirmation sur 25 nouveaux plis (répétitions 5 à 9) : V0 contre ENS | Première version ; I1 n'est pas remplacée | **version courante** | `versions/scripts/v3_phase2_I1b__1.py` |

## RI2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:18 | Préinscription D18, HF10 à HF12 (champs typés) | Première version | **version courante** | `versions/scripts/v3_register_I2__1.py` |

## FLD1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:18 | Extracteur de jetons typés (programme, champs clé=valeur, types de valeurs, forme) | Première version | **version courante** | `versions/src/tp2_fields__1.py` |

## I2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:18 | Itération I2 : V0, FT, FTo, FTE sur P2 25 plis | Première version ; ne remplace ni I1 ni I1b | **version courante** | `versions/scripts/v3_phase2_I2__1.py` |

## AI1b

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:22 | Analyse de la confirmation I1b | Première version | **version courante** | `versions/scripts/v3_analyze_I1b__1.py` |

## VI1b

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:22 | Verdicts HF7 à HF9 et résultat RI1b | Première version | **version courante** | `versions/scripts/v3_verdicts_I1b__1.py` |

## AI2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:22 | Analyse de l'itération I2 (HF10 à HF12) | Première version | **version courante** | `versions/scripts/v3_analyze_I2__1.py` |

## VI2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 13:25 | Verdicts HF10 à HF12 et résultat RI2 | Première version | **version courante** | `versions/scripts/v3_verdicts_I2__1.py` |

## RI4

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 14:00 | Préinscription D19, HI1 à HI4 (rejet de famille) | Première version | **version courante** | `versions/scripts/v3_register_I4__1.py` |

## I4

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 14:00 | Itération I4 : rejet par la confiance de famille sur 5 nouvelles rotations x 25 nouveaux plis | Première version | **version courante** | `versions/scripts/v3_phase2_I4__1.py` |

## AI4

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 14:02 | Analyse de l'itération I4 (HI1 à HI4) | Première version | **version courante** | `versions/scripts/v3_analyze_I4__1.py` |

## VI4

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 14:02 | Verdicts HI1 à HI4 et résultat RI4 | Première version | **version courante** | `versions/scripts/v3_verdicts_I4__1.py` |

## RD20

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 17:55 | Décision D20 : règle d'arrêt de la phase 2 | Première version | **version courante** | `versions/scripts/v3_register_D20__1.py` |

## RI5

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 17:55 | Préinscription D21, HF13 et HF14 (réglage mots + lettres) | Première version | **version courante** | `versions/scripts/v3_register_I5__1.py` |

## I5a

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 17:55 | Itération I5a : sélection mots + lettres sur répétitions 0 à 4 | Première version | **version courante** | `versions/scripts/v3_phase2_I5a__1.py` |

## AI5a

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 19:14 | Analyse d'I5a : sélection et porte HF14 | Première version | **version courante** | `versions/scripts/v3_analyze_I5a__1.py` |

## VI5

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 19:14 | Verdicts HF13, HF14 et résultat RI5 | Première version | **version courante** | `versions/scripts/v3_verdicts_I5__1.py` |

## AT1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:14 | Analyse du bloc T (grille Transformer) : HT1 à HT4 | Première version | **version courante** | `versions/scripts/v3_analyze_T__1.py` |

## VT1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:14 | Verdicts HT1 à HT4 et résultat RT1 | Première version | **version courante** | `versions/scripts/v3_verdicts_T__1.py` |

## RT2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:31 | Préinscription D22, HT1b, HT2b, HF15, HF16 | Première version | **version courante** | `versions/scripts/v3_register_T2__1.py` |

## T2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:31 | Réplication Transformer (4 nouvelles découpes x 5 rotations) + fusion avec TF-IDF | Première version ; T1 (grille) non remplacée | **version courante** | `versions/scripts/v3_transformer_T2__1.py` |

## RI6

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:32 | Préinscription D23, HF17 à HF19 (I6) | Première version | **version courante** | `versions/scripts/v3_register_I6__1.py` |

## I6

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:33 | Itération I6 : 32 configurations (représentation, structure, modèle), sélection puis confirmation | Première version ; I1, I2, I5 non remplacées | **version courante** | `versions/scripts/v3_phase2_I6__1.py` |

## STAT2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:35 | Ajout à tp2_stats : test des signes, permutation apparié, multi_paired (IC95 + Wilcoxon + signes + permutation) | Ajout seulement ; les fonctions existantes ne changent pas | **version courante** | `versions/src/tp2_stats__1.py` |

## AI6

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:35 | Analyse I6 (sélection a, confirmation b) avec plusieurs tests | Première version | La version 1 classait le rang 24 comme meilleur : le nombre de configurations indiscernables du meilleur (20) et le nom du meilleur au rang étaient faux ; la sélection par moyenne de F1 n'était pas touchée (par 2) | `versions/scripts/v3_analyze_I6__1.py` |
| **2** | 2026-11-09 22:00 | Corrige l'ordre des rangs de Friedman (rang 1 = meilleur) : le meilleur au rang était pris à l'envers | La version 1 classait le rang 24 comme meilleur : le nombre de configurations indiscernables du meilleur (20) et le nom du meilleur au rang étaient faux ; la sélection par moyenne de F1 n'était pas touchée | **version courante** | `versions/scripts/v3_analyze_I6__2.py` |

## RI7

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:35 | Préinscription D24, HI5 à HI7 (I7) | Première version | **version courante** | `versions/scripts/v3_register_I7__1.py` |

## I7

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:35 | Itération I7 : 24 combinaisons de rejet d'inconnus (C x score), sélection puis confirmation sur rotations différentes | Première version ; I4 non remplacée | La version 1 ne calculait pas le msp (C = 4) exigé par la préinscription D24 comme référence ; l'ancien bloc P2_I7a_rejet (une douzaine d'unités) est conservé, non utilisé (par 2) | `versions/scripts/v3_phase2_I7__1.py` |
| **2** | 2026-11-09 21:37 | Ajoute C = 4 comme RÉFÉRENCE (msp de D24) calculée sur les mêmes unités ; bloc de résultats P2_I7a_rejet_v2 | La version 1 ne calculait pas le msp (C = 4) exigé par la préinscription D24 comme référence ; l'ancien bloc P2_I7a_rejet (une douzaine d'unités) est conservé, non utilisé | **version courante** | `versions/scripts/v3_phase2_I7__2.py` |

## AT2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:37 | Analyse de la réplication T2 (HT1b, HT2b, HF15, HF16) | Première version | **version courante** | `versions/scripts/v3_analyze_T2__1.py` |

## AI7

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 21:37 | Analyse I7 (sélection a, confirmation b) | Première version | Suit I7 version 2 (par 2) | `versions/scripts/v3_analyze_I7__1.py` |
| **2** | 2026-11-09 21:37 | Analyse I7 : référence msp C = 4, candidates sans C = 4, bloc v2 | Suit I7 version 2 | Même défaut que AI6 version 1, corrigé avant tout usage (par 3) | `versions/scripts/v3_analyze_I7__2.py` |
| **3** | 2026-11-09 22:00 | Corrige l'ordre des rangs de Friedman (rang 1 = meilleur) | Même défaut que AI6 version 1, corrigé avant tout usage | **version courante** | `versions/scripts/v3_analyze_I7__3.py` |

## VI67

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:07 | Verdicts HF17-HF19, HI5-HI7 et résultats RI6, RI7 | Première version | **version courante** | `versions/scripts/v3_verdicts_I6_I7__1.py` |

## RD25

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:09 | Préinscription D25, HI6b, HI7b | Première version | **version courante** | `versions/scripts/v3_register_D25__1.py` |

## I7c

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:09 | Réplication I7c : 3 nouveaux jeux de rotations x répétitions 10 à 14 | Première version ; I7a et I7b non remplacées | **version courante** | `versions/scripts/v3_phase2_I7c__1.py` |

## VI6b

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:11 | Verdict HF18 après lancement d'I6b | Première version | **version courante** | `versions/scripts/v3_verdicts_I6b__1.py` |

## AI7c

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:11 | Analyse de la réplication I7c (HI6b, HI7b) | Première version | **version courante** | `versions/scripts/v3_analyze_I7c__1.py` |

## VI7c

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-09 22:25 | Verdicts HI6b, HI7b, tranche HI6 et HI7, résultat RI7c | Première version | **version courante** | `versions/scripts/v3_verdicts_I7c__1.py` |

## VT2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 00:00 | Verdicts HT1b, HT2b, HF15, HF16, tranche HT1, résultat RT2 | Première version | **version courante** | `versions/scripts/v3_verdicts_T2__1.py` |

## DG2

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 00:03 | Diagnostic exploratoire du plafond : F1 par classe, oracle d'agrégation par vrai gabarit, lissage par voisins du test | Première version (diagnostic, aucun verdict) | **version courante** | `versions/scripts/v3_diag_DG2__1.py` |

## RR3

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 00:03 | Préinscription D26, HG1 à HG10 (ronde 3) | Première version | **version courante** | `versions/scripts/v3_register_R3__1.py` |

## HOOK

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **2** | 2026-11-10 13:17 | Ajoute le contrôle du scellement du test v2 (bloque le commit en cas d'écart) | La version 1 ne faisait que figer les versions de code et ne bloquait jamais ; la version 2 garde en plus le test v2 (D27, validé par l'étudiant) | **version courante** | `versions/scripts/hooks/pre-commit__2` |

## CHKSEAL

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:17 | Contrôle du scellement (journal, empreintes, scan des scripts) | Première version (D27) | **version courante** | `versions/scripts/check_test_seal__1.py` |

## SEAL

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:17 | Scellement vérifiable du test v2 : empreinte des identifiants, sans lire aucun log | Première version (D27) | **version courante** | `versions/scripts/v3_seal_test_v2__1.py` |

## DG4

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:19 | Comptages exploratoires sur le développement seulement (format × classe, vocabulaire d'un gabarit mis de côté, axes) | Première version (aucun entraînement, aucun verdict) | **version courante** | `versions/scripts/v3_comptages_dev__1.py` |

## RW1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:19 | Préinscription D28, HW1 à HW8 et résultat exploratoire RDG4 | Première version | **version courante** | `versions/scripts/v3_register_W1__1.py` |

## W1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:20 | Vague 1 : F8, F14, F6, F9, F18 (14 variantes), sélection puis confirmation | Première version | **version courante** | `versions/scripts/v3_phase2_W1__1.py` |

## AW1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:25 | Analyse de la vague 1 (porte HW7, tests, HW8) | Première version | **version courante** | `versions/scripts/v3_analyze_W1__1.py` |

## VW1

| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |
|---|---|---|---|---|---|
| **1** | 2026-11-10 13:26 | Verdicts HW1 à HW8 et résultat RW1 | Première version | **version courante** | `versions/scripts/v3_verdicts_W1__1.py` |
