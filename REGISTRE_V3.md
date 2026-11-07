# Registre du protocole v3 (règles, décisions, hypothèses, résultats)
Généré à partir de `artifacts/results/v3/journal.jsonl` (append-only : rien n'est jamais supprimé ni écrasé ; un changement de statut ajoute une version). Ne pas modifier à la main.

## Règles de travail

### R1 : Méthodique de bout en bout  (version 1, 2026-11-07 21:54:05)

Chaque choix, chaque décision et chaque résultat est justifié par écrit (texte, raison, preuve).

*Justification.* Demande de l'étudiant (2026-11-07) ; condition de la défense et de la publication.

### R2 : Toute hypothèse reçoit un verdict  (version 1, 2026-11-07 21:54:05)

Une hypothèse est préinscrite avant de voir les chiffres, puis confirmée, réfutée ou déclarée non tranchée. Aucune n'est laissée sans verdict.

*Justification.* Évite de choisir l'hypothèse après coup.

### R3 : On ne supprime jamais un résultat précédent  (version 1, 2026-11-07 21:54:05)

Dans tout document (notebook, présentation, script oral, tableaux, registre), on garde le résultat précédent ET l'actuel, côte à côte quand c'est utile. Un recalcul forcé archive l'ancien fichier ; les archives ne sont jamais écrasées (`archive/`, `scripts/archive_state.py`) ; le journal est append-only.

*Justification.* Traçabilité : on doit pouvoir montrer l'évolution et ce qui a changé, et pourquoi.

### R4 : Unité statistique et baseline  (version 1, 2026-11-07 21:54:05)

L'unité est le gabarit ; chaque bloc a une baseline ; comparaisons appariées ; correction de Holm pour les comparaisons multiples.

*Justification.* Les logs d'un même gabarit ne sont pas indépendants (de 3 à 20 000 logs par gabarit).

### R5 : Test scellé v2 : une seule ouverture  (version 1, 2026-11-07 21:54:05)

Le test v2 n'est lu par aucun script d'expérience ; il s'ouvre une fois, sur le pipeline figé (empreinte enregistrée), avec une trace datée.

*Justification.* Le test v1 a été consommé le 2026-11-05 ; régler sur le test fausserait toute mesure.

### R6 : Calculs reprenables et tracés  (version 1, 2026-11-07 21:54:05)

Une unité terminée n'est jamais refaite ; une interruption ne coûte que l'unité en cours ; chaque unité écrit son empreinte, sa configuration, sa durée, sa machine et le commit.

*Justification.* Demande de l'étudiant ; `src/tp2_runner.py`.

### R7 : Sources vérifiées pour chaque aspect  (version 1, 2026-11-07 21:54:05)

Chaque méthode ou choix s'appuie sur des sources dont la page a été ouverte, avec le niveau de vérification.

*Justification.* Demande de l'étudiant ; `etat_de_l_art/sources_v3_*.md`.

### R8 : Affinage itératif journalisé  (version 1, 2026-11-07 21:54:05)

Chaque itération de la phase 2 a un numéro, une hypothèse, une configuration, un résultat et une décision ; arrêt à la fin de la semaine ou après trois itérations sans gain significatif.

*Justification.* Rend l'affinage traçable et évite de s'arrêter trop tôt ou de tourner en rond.

## Décisions

### D1 : Nouveau test scellé v2  (version 1, 2026-11-07 21:54:05)

Nouveau découpage des gabarits : 57 gabarits de test (17,6 % des logs), tirés parmi ceux qui n'ont jamais servi de test en v1 ; le test v1 est déclaré consommé.

*Justification.* Toute nouvelle comparaison sur les mêmes gabarits n'est plus scellée.

*Preuve.* artifacts/data/splits_v3_meta.json

### D2 : Grille complète pour le Transformer  (version 1, 2026-11-07 21:54:05)

6 bruits × 5 rotations × 3 graines.

*Justification.* L'encodeur s'entraîne sur 4 200 logs par fichier : environ 3 minutes par modèle, donc réalisable sur Mac et Colab.

*Preuve.* colab/encoder_data_v2.csv.gz (25 200 logs d'entraînement)

### D3 : Au plus 400 logs par gabarit  (version 1, 2026-11-07 21:54:05)

Dans les expériences linéaires de développement, tirage fixe d'au plus 400 logs par gabarit, pour l'entraînement comme pour l'évaluation.

*Justification.* La taille des gabarits va de 3 à 20 000 logs : sans plafond, un gros gabarit pèserait 5 000 fois un petit et dominerait le macro-F1 ; le plafond accélère aussi le calcul.

*Preuve.* scripts/v3_blockA.py

### D4 : Métrique principale : macro-F1 du palier A  (version 1, 2026-11-07 21:54:05)

Macro-F1 sur les classes de 5 gabarits ou plus (18 classes) ; le macro-F1 des 30 classes est rapporté en complément.

*Justification.* Une classe de 1 à 2 gabarits ne peut pas être évaluée honnêtement (tous ses logs d'un seul côté) ; même convention que le notebook (sections 3.2 et 7.4).

*Preuve.* notebook v1, sections 3.2 et 7.4

### D5 : Critères d'acceptation du tirage du test v2  (version 1, 2026-11-07 21:54:05)

Part de logs de test entre 10 et 22 %, au moins 1 gabarit de test par classe de 5 gabarits ou plus, quasi-jumeaux (cosinus >= 0,90) au plus 2 % ; sinon graine suivante.

*Justification.* Garantit un test peu semblable à l'entraînement (demande de l'étudiant) et assez grand ; la graine 1 a été acceptée du premier coup (0,22 % de quasi-jumeaux).

*Preuve.* artifacts/data/splits_v3_meta.json

### D6 : Protocole imbriqué (P3) sur trois répétitions seulement  (version 1, 2026-11-07 21:54:05)

P3 est calculé pour les répétitions 0 à 2 (15 plis) et non 0 à 4.

*Justification.* Coût : le réglage intérieur multiplie le calcul par environ 9 ; trois répétitions suffisent pour estimer la variabilité. Limite assumée et à rappeler dans les résultats.

*Preuve.* scripts/v3_blockA.py

### D7 : P2 (validation croisée par groupes, 5 plis × 5 répétitions) est le protocole par défaut des blocs B à E  (version 1, 2026-11-07 21:58:55)

Pour la comparaison de méthodes sur le développement, on utilise P2.

*Justification.* Sans fuite (0,8 % de quasi-jumeaux), même classement que P1 (tau 0,87), précision proche de P3 (écart-type 0,059 contre 0,058) pour un coût environ neuf fois moindre, et 25 plis donnent assez de blocs pour Friedman et Wilcoxon. Provisoire : confirmé ou infirmé à l'ouverture du test v2 (HA8).

*Preuve.* RA1 ; HA2 ; HA4 ; HA7

### D8 : Bloc B : classifieurs comparés et protocole  (version 2, 2026-11-07 22:10:08)

Protocole P2 (5 plis de groupes × 5 répétitions), SIEVE_00, 400 logs au plus par gabarit, baseline = SVM sur mots. Plats : SVM mots, régression logistique. Hiérarchique local p(famille) × p(classe | famille). Voisinage et prototypes : kNN (k = 5 et 15), centroïde, k-means par classe (k = 3 et 10 prototypes), gabarits-prototypes (notre proposition F3), Naive Bayes. Clustering de types variés, dans l'espace SVD de dimension 100 du TF-IDF : par classe (k-means, mélange gaussien, classification hiérarchique ascendante de Ward) et global non supervisé avec étiquette majoritaire (k-means à K = 60 et 150, Birch, DBSCAN, HDBSCAN ; les points de bruit sont comptés comme rejetés). **Amendement :** pour DBSCAN et HDBSCAN, deux sorties sont comparées : « sans rejet » (le log reçoit la classe du groupe du plus proche point groupé, quelle que soit la distance) et « avec rejet » (rejet si la distance dépasse le seuil : eps pour DBSCAN, 95e centile des distances entre points groupés pour HDBSCAN). La comparaison de classification (HB6) porte sur la sortie sans rejet ; la sortie avec rejet est conservée et annonce le bloc C.

*Justification.* Le test de fumée (répétition 0, pli 0, vu avant le calcul complet) a montré 95 % (DBSCAN) et 88 % (HDBSCAN) de rejets : les logs de nouveaux gabarits sont plus loin de tous les points d'entraînement que le seuil. Avec rejet seulement, ces méthodes ne classeraient presque rien et la comparaison avec le SVM n'aurait pas de sens ; le taux de rejet est lui-même un résultat. L'amendement est écrit avant le calcul complet.

*Preuve.* scripts/v3_blockB.py (version B2)

*Note.* Version 1 conservée : elle prévoyait seulement la sortie avec rejet.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut None ; Protocole P2 (5 plis de groupes × 5 répétitions), SIEVE_00, 400 logs au plus par gabarit, baseline = SVM sur mots. Plats : SVM mots, régression logistique. Hiérarchique local p(famille) × p(classe | f…

## Hypothèses (préinscrites, puis confirmées ou réfutées)

### HA1 : Le découpage au hasard gonfle le score  (version 3, 2026-11-07 22:06:03 ; **statut : non tranchée**)

Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).

*Justification.* Remise en cause par l'étudiant (2026-11-07) : le test de Wilcoxon apparié comparait P0 et P2 pli par pli, alors que ces deux protocoles n'évaluent pas les mêmes logs ; la différence de plis peut influer sur les scores et les écarts. L'appariement n'était donc pas justifié.

*Preuve.* Écarts P0 moins P2 : centroïde 0,468 ; kNN 0,551 ; LR 0,491 ; Naive Bayes 0,511 ; SVM caractères 0,488 ; SVM mots 0,483. Les six dépassent 0,20 ; Wilcoxon sur 25 plis, p ajusté < 1e-6, Cliff delta = 1 pour tous.  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Le verdict « confirmée » de la version 2 est conservé dans l'historique. Rejouée de deux façons : (a) réanalyse des mêmes données avec un test NON apparié (Mann-Whitney) ; (b) HA1b, montage apparié sur les mêmes logs de test.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Pour chaque modèle, le macro-F1 du palier A est plus élevé sous P0 (au hasard) que sous P2 (par groupes) d'au moins 0,20 (Wilcoxon apparié par pli, Holm p < 0,05).
- v2 (2026-11-07 21:58:55) : statut confirmée ; Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).

### HA2 : Les protocoles par gabarit classent les modèles de la même façon  (version 2, 2026-11-07 21:58:55 ; **statut : confirmée**)

Tau de Kendall moyen entre P1, P2 et P3 >= 0,60.

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* Tau : P1-P2 0,867 ; P1-P3 0,733 ; P2-P3 0,600 ; moyenne 0,733.  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Réserve : avec six modèles, le tau ne prend que des valeurs par pas de 0,067 ; et les trois meilleurs (SVM mots, SVM caractères, régression logistique) ne se distinguent pas statistiquement entre eux (Nemenyi, p > 0,98), donc leurs permutations de rang ne sont pas des désaccords réels.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Les classements des six modèles sous P1, P2 et P3 sont concordants (tau de Kendall moyen entre eux >= 0,60).

### HA3 : Le hasard classe les modèles autrement  (version 2, 2026-11-07 21:58:55 ; **statut : réfutée**)

Tau(P0, P2) strictement plus faible que la concordance moyenne entre protocoles par gabarit.

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* Tau(P0, P2) = 0,733, égal à la moyenne des trois tau par gabarit (0,733) : pas plus faible. Tau(P0, P1) = 0,600 et tau(P0, P3) = 0,600 restent dans la fourchette des tau entre protocoles par gabarit (0,600 à 0,867).  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Interprétation : avec ces six modèles linéaires, le découpage au hasard classe les familles de modèles presque comme les découpages par gabarit (SVM et LR devant, kNN et centroïde derniers). Il surestime le NIVEAU de score mais, ici, pas l'ORDRE des méthodes ; il nomme toutefois un autre meilleur modèle (SVM caractères au lieu de SVM mots). Cet effet pourrait apparaître avec des modèles plus capables de mémoriser (Transformer), à tester au bloc B/vectorisation.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Le tau de Kendall entre P0 et P2 est plus faible que la concordance moyenne entre protocoles par gabarit.

### HA4 : Fuite résiduelle  (version 2, 2026-11-07 21:58:55 ; **statut : confirmée**)

Quasi-jumeaux : >= 10 % sous P0 ; <= 2 % sous P1, P2, P3.

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* Part de quasi-jumeaux (cosinus >= 0,90) : P0 20,5 % ; P1 1,3 % ; P2 0,8 % ; P3 0,7 %. Cosinus médian au plus proche voisin : 0,732 ; 0,442 ; 0,465 ; 0,466.  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Résultat cohérent avec le notebook v1 (24 % contre 1 % sur SIEVE_00).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Part moyenne de quasi-jumeaux (cosinus >= 0,90) : au moins 10 % sous P0, au plus 2 % sous P1, P2 et P3.

### HA5 : Voisinage et centroïde sont moins bons que le SVM sur mots  (version 2, 2026-11-07 21:58:55 ; **statut : confirmée**)

Sous P2, kNN et centroïde ont un macro-F1 inférieur au SVM sur mots (Holm p < 0,05).

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* SVM mots moins kNN : +0,093, IC 95 % bootstrap [0,071 ; 0,117], p Holm 9e-7 ; SVM mots moins centroïde : +0,098, IC [0,076 ; 0,119], p Holm 1e-6. Naive Bayes aussi inférieur (+0,070, p Holm 3e-6). Nemenyi : kNN, centroïde et Naive Bayes ne se distinguent pas entre eux.  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Hypothèse peu informative au départ (un pli vu au test de fumée), mais verdict établi sur 25 plis.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Sous P2, kNN et centroïde ont un macro-F1 inférieur à celui du SVM sur mots (Holm p < 0,05).

### HA6 : Les n-grammes de caractères dépassent les mots  (version 3, 2026-11-07 21:59:12 ; **statut : réfutée**)

Sous P2, SVM caractères supérieur au SVM mots (Holm p < 0,05).

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* Écart SVM mots moins SVM caractères : +0,003 (IC 95 % [-0,015 ; +0,022], p Holm 0,79) ; caractères meilleur dans 11 plis sur 25. L'IC écarte un gain des caractères supérieur à 0,015. Pour contexte : sous P0 l'écart est de +0,002 (en faveur des caractères ; statistiquement significatif, p < 1e-5, mais d'une taille négligeable devant l'écart-type entre plis de 0,002 à 0,06) et sous P3 de +0,010 (p = 0,33).  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Le résultat du notebook v1 (0,515 contre 0,483) ne se retrouve pas avec ce découpage et ce plafond de 400 logs par gabarit : aucune supériorité démontrée. Les deux représentations restent à comparer sous bruit (bloc vectorisation × fichiers) et sous attaque (bloc D), où les caractères devraient surtout compter.  Correction (version 3) : la formulation « p non significatif au sens pratique » de la version 2 pour P0 était ambiguë ; le verdict (réfutée) ne change pas, car l'hypothèse portait sur P2 et exigeait une supériorité significative.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Sous P2, le SVM sur caractères (3 à 5) dépasse le SVM sur mots (Holm p < 0,05).
- v2 (2026-11-07 21:58:55) : statut réfutée ; Sous P2, SVM caractères supérieur au SVM mots (Holm p < 0,05).

### HA7 : Le hasard est plus stable mais biaisé  (version 2, 2026-11-07 21:58:55 ; **statut : confirmée**)

Écart-type du macro-F1 entre plis plus petit sous P0 que sous P2.

*Justification.* Verdict établi avec les règles de décision préinscrites (voir la version précédente).

*Preuve.* Écart-type moyen entre plis : P0 0,0020 ; P1 0,0632 ; P2 0,0590 ; P3 0,0583.  Fichiers : artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Un découpage stable n'est pas un découpage juste : P0 est trente fois plus stable et surestime de près de 0,5.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; L'écart-type du macro-F1 entre plis est plus petit sous P0 que sous P2.

### HA8 : Quel protocole prédit le mieux le test v2 ?  (version 1, 2026-11-07 21:54:05 ; **statut : préinscrite**)

À l'ouverture unique du test v2 : pour au moins 5 des 6 modèles, l'écart entre l'estimation du développement et le score du test v2 est plus petit sous P2 ou P3 que sous P0.

*Justification.* C'est le seul critère qui mesure le biais réel d'un protocole ; verdict à l'ouverture du test v2 (R5).

*Note.* Écrit le 2026-11-07 (soir) avant lecture de l'analyse du bloc A ; seul un pli (P2, répétition 0, pli 0) avait été vu lors du test de fumée.

### HA1b : Effet pur de la fuite, sur les mêmes logs de test  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Montage apparié : pour chaque pli de groupes (répétition r, pli k), le test est une moitié tirée au hasard des logs du pli (T_b). Condition G : entraînement = logs des autres plis (aucun log des gabarits de test). Condition H : entraînement = G plus l'autre moitié des logs du pli (T_a), donc des logs des mêmes gabarits que T_b. Les deux conditions sont évaluées sur les MÊMES logs T_b. Hypothèse : pour chacun des six modèles, le macro-F1 du palier A est plus élevé en H qu'en G d'au moins 0,20 (Wilcoxon apparié sur 25 plis, Holm p < 0,05).

*Justification.* Seule la présence de logs du même gabarit dans l'entraînement change : c'est l'effet pur de la fuite, mesuré sans que les plis ni les logs de test diffèrent. Le seuil de 0,20 est fixé par prudence, très en dessous de l'écart de 0,48 à 0,55 observé entre P0 et P2.

*Note.* Écrit le 2026-11-07 avant tout calcul de ce montage.

### HB1 : La hiérarchie n'améliore pas le macro-F1 des classes  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Sous P2, le macro-F1 des classes (palier A) du modèle hiérarchique ne diffère pas significativement du modèle plat de même famille (régression logistique) : Wilcoxon, Holm p >= 0,05, ou |écart| < 0,03.

*Justification.* Notebook v1 : gain « non démontré », signe qui change entre validation et test.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB2 : La hiérarchie améliore le F1 des familles  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Le macro-F1 des familles (famille déduite de la classe prédite pour le plat) est plus élevé avec la hiérarchie d'au moins 0,03 (Wilcoxon, Holm p < 0,05).

*Justification.* La tête famille est entraînée directement sur la famille, plus facile (0,67 contre 0,46 au notebook v1).

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB3 : La hiérarchie réduit la gravité des erreurs  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

La distance moyenne d'erreur dans l'arbre (0 même classe, 1 même famille, 2 autre famille) est plus petite avec la hiérarchie (Wilcoxon, Holm p < 0,05).

*Justification.* Une classe prédite cohérente avec la famille prédite rapproche les erreurs ; notebook v1 : 0,83 contre 0,86 pour TF-IDF.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB4 : Plusieurs prototypes valent mieux qu'un  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Le k-means par classe à 10 prototypes dépasse le centroïde unique (Wilcoxon, Holm p < 0,05).

*Justification.* Une classe contient plusieurs gabarits : un seul centre les moyenne et se place entre eux.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB5 : Les gabarits-prototypes (F3) dépassent le centroïde mais pas le SVM  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Sous P2, gabarits-prototypes meilleur que le centroïde (Holm p < 0,05) et inférieur au SVM sur mots d'au moins 0,03.

*Justification.* Les gabarits sont les groupes naturels, mais un nouveau gabarit n'a pas de prototype proche : on s'attend à mieux que le centroïde sans égaler un classifieur discriminant.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB6 : Le clustering non supervisé n'atteint pas le SVM  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Aucun des clustering globaux non supervisés (k-means global, Birch, DBSCAN, HDBSCAN) n'atteint le SVM sur mots : écart d'au moins 0,05, Holm p < 0,05, pour chacun.

*Justification.* Sans les étiquettes, les groupes se forment sur les gabarits et non sur les classes ; l'étiquette majoritaire est une approximation.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

### HB7 : Un clustering par classe rivalise avec le kNN  (version 1, 2026-11-07 22:06:03 ; **statut : préinscrite**)

Au moins une méthode de clustering supervisé par classe (k-means, mélange gaussien, Ward) ou les gabarits-prototypes est indiscernable du kNN (Friedman puis Nemenyi : différence de rang moyen inférieure à la différence critique).

*Justification.* Ces méthodes utilisent les mêmes distances que le kNN avec un résumé des classes.

*Note.* Écrit le 2026-11-07 avant tout calcul du bloc B (hormis les modèles kNN, centroïde et Naive Bayes déjà vus au bloc A, sous le même protocole).

## Résultats

### RA1 : Bloc A : macro-F1 du palier A par protocole (précédent v1 et actuel v3)  (version 1, 2026-11-07 21:58:55)

**Précédent (notebook v1, étape 3.7, SVM sur TF-IDF mots, SIEVE_00, palier A, tout le jeu d'entraînement) :** P0 0,9872 ; P1 0,4220 ; P2 0,5070 ; P3 0,5105.  **Actuel (v3, SVM sur mots, 400 logs par gabarit au plus, développement) :** P0 0,986 ; P1 0,471 ; P2 0,503 ; P3 0,487.  Les deux séries sont conservées. Écart notable pour P1 (0,422 contre 0,471) : le P1 de v1 est un seul découpage de 36 gabarits de validation, celui de v3 est la moyenne de 5 plis de gabarits différents (écart-type 0,063) ; la valeur de v1 est dans l'intervalle de celles de v3.  Tous les modèles : P0 de 0,874 (centroïde) à 0,988 (SVM caractères) ; P2 de 0,406 (centroïde) à 0,503 (SVM mots).

*Justification.* Montre que le niveau de score et le contraste hasard / gabarit se reproduisent avec un protocole indépendant (autres gabarits de test, nouveau plafond), ce qui renforce la conclusion de v1.

*Preuve.* artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Conformément à R3, ni la série v1 ni la série v3 n'est écartée.
