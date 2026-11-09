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

### R9 : Aucune version de code ne se perd  (version 1, 2026-11-07 22:20:11)

Le code qui produit un résultat est conservé automatiquement : copie par contenu dans `versions/auto/` au premier calcul de chaque processus (`src/tp2_runner.py` R3), empreinte du code dans chaque résultat et dans le registre, vérification `scripts/check_versions.py` (avec `--fix`) à lancer avant chaque commit et en fin de session. Un hachage de commit inexistant est refusé par `tp2_versions.register`.

*Justification.* La première version du script du bloc B (B1) avait été modifiée avant tout commit et n'a pu être conservée ; l'étudiant a demandé que cela ne se reproduise pas. Une faute de frappe sur un hachage (ccd459e au lieu de ccc459e) avait aussi été enregistrée dans VERSIONS.md : trois copies n'avaient pas été créées ; corrigé par ajout d'une correction (journal des versions), sans réécriture.

*Note.* Un crochet git automatique `pre-commit` a été envisagé puis non installé : il exécuterait du code à chaque commit sans accord explicite de l'étudiant. À décider avec lui.

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

### D9 : Garde-fou de conservation du code  (version 1, 2026-11-07 22:20:11)

Mise en œuvre de R9 : runner R3, versions V2 et V3, contrôle CV1 ; pas de crochet git automatique (à décider).

*Justification.* Voir R9 ; le garde-fou ne dépend plus d'un oubli ni d'un commit, mais le contrôle `check_versions.py` reste à lancer avant de commiter.

*Preuve.* VERSIONS.md ; scripts/check_versions.py ; src/tp2_runner.py R3

### D10 : Crochet git pre-commit installé  (version 1, 2026-11-07 22:22:52)

Le crochet `scripts/hooks/pre-commit` est installé dans `.git/hooks/` ; il lance `scripts/check_versions.py --fix` et ajoute `versions/auto` au commit.

*Justification.* Complète R9 sans dépendre d'un oubli. Il avait d'abord été refusé par le contrôle d'autorisation car il exécute du code à chaque commit ; l'étudiant l'a ensuite demandé explicitement (2026-11-07).

*Preuve.* scripts/hooks/pre-commit ; VERSIONS.md (H1)

### D11 : Bloc C : détection d'inconnus, plan et protocole  (version 1, 2026-11-07 22:55:54)

Protocole : 5 rotations de classes masquées (6 classes cachées à l'entraînement) × 5 répétitions × 5 plis de groupes (P2) = 125 unités, SIEVE_00, développement seul (test v2 jamais lu), 400 logs au plus par gabarit. On entraîne sur les logs des 24 classes connues des plis d'entraînement ; le test du pli contient les logs des classes connues (positifs « connu ») et des classes masquées (« inconnu »), tous de gabarits jamais vus. Baseline : probabilité maximale (MSP) d'une régression logistique sur TF-IDF mots (C = 4, comme le notebook v1). Scores comparés (28) : tête TF-IDF (MSP, logit maximal, énergie, entropie négative, ensemble de 5 régressions bootstrap, MSP hiérarchique, MSP famille, OpenMax) ; espace SVD à 100 dimensions normalisé (cosinus au centroïde, Mahalanobis à covariance commune, par classe avec rétrécissement de Ledoit-Wolf, relative, kNN k = 1 et 10, résidu de PCA, densité de mélange gaussien, LOF, forêt d'isolation, distance au gabarit le plus proche avec et sans rayon : notre proposition F3) ; tête sur l'espace SVD (énergie, ASH, SCALE, DICE, NNGuide, SHE, ViM, méthodes de la vision adaptées à des vecteurs signés) ; fusion par moyenne de rangs (MSP, Mahalanobis, kNN). Mesures : AUROC (principale), FPR@95 (inconnus acceptés quand on garde 95 % des connus), AUPR. Tests : Wilcoxon apparié contre le MSP avec correction de Holm, Friedman et Nemenyi sur les 125 unités.

*Justification.* Demande de l'étudiant (2026-11-07) : comparer des scores de détection par le score et par la distance, plus des méthodes récentes, avec une baseline et des tests statistiques ; sources dans sources_v3_methodes.md. Les méthodes de la vision (ASH, SCALE, DICE, NNGuide, SHE) sont ADAPTÉES à des vecteurs signés de logs (activations remplacées par les composantes SVD, magnitude par valeur absolue) : ce sont des adaptations de leur principe, non des reproductions, et le résultat n'établit pas leur performance en vision. OpenMax est une version simplifiée (Weibull sur les 20 plus grandes distances par classe).

*Preuve.* scripts/v3_blockC.py

### D12 : Piste retenue pour la phase 2 : rejet hiérarchique  (version 1, 2026-11-07 23:12:01)

Pour la phase 2, la confiance au niveau de la FAMILLE devient le candidat principal de détection d'inconnus ; on préinscrira une hypothèse la confirmant ou la réfutant sur de nouvelles données (autres répétitions et rotations, puis le test v2 en une seule ouverture).

*Justification.* RC2 : meilleur score, seul à rester nettement au-dessus du hasard dans la pire rotation ; les méthodes de distance, de densité et de la vision n'ont pas fait mieux que la confiance. La conclusion exploratoire doit être confirmée avant d'être affirmée.

*Preuve.* RC2 ; HC1 ; HC2 ; HC8

### D13 : Plan de la vectorisation × bruit (bloc V) et de la grille complète du Transformer (bloc T)  (version 1, 2026-11-07 23:25:34)

**Bloc V (modèles linéaires).** Trois vectorisations (TF-IDF mots, TF-IDF caractères 3 à 5, Skip-gram pondéré IDF) × les six fichiers SIEVE (p = 0 à 0,5, entraînement et test dans le MÊME fichier) × 5 rotations × 2 répétitions (0 et 1) × 5 plis de groupes = 300 unités, développement seul, 400 logs au plus par gabarit et par fichier. Dans chaque unité, MÊMES logs pour deux familles de mesures : macro-F1 des classes connues (palier A) et AUROC de détection d'inconnus (MSP, énergie, MSP de la famille). **Bloc T (Transformer, grille complète).** DistilBERT sans casse (256 jetons, 2 époques, taux 3e-5) × 6 fichiers × 5 rotations × 3 graines (42, 43, 44) = 90 modèles, une seule découpe du développement (répétition 0, pli 0 : mêmes gabarits de test pour tous), 140 logs d'entraînement par classe connue et jusqu'à 133 logs de test par classe, tirage fixe. Chaque unité compare sur LES MÊMES LOGS DE TEST le Transformer et une baseline TF-IDF entraînée sur les mêmes logs d'entraînement. Scores du Transformer : MSP, logit maximal, énergie, MSP de la famille, MSP Monte-Carlo (10 passages), Mahalanobis et kNN sur les vecteurs de 768 valeurs. Les poids ne sont pas conservés (266 Mo par modèle) ; les logits le sont.

*Justification.* Demande de l'étudiant (2026-11-07) : comparer les vectorisations selon le bruit et mener en parallèle la grille complète du Transformer. Deux familles de mesures sur les mêmes unités pour que le monde connu et le monde inconnu soient comparables (demande antérieure). La grille complète est réalisable : l'encodeur s'entraîne sur environ 3 400 logs par modèle (environ 3 minutes sur le GPU du Mac).

*Preuve.* scripts/v3_blockV.py ; scripts/v3_transformer_grid.py

### D14 : Bloc D : attaques sur le texte, trois attaques × cinq degrés, comparées à « sans attaque »  (version 1, 2026-11-09 12:40:19)

Protocole : 5 rotations de classes masquées × répétition 0 × 5 plis de groupes = 25 unités, SIEVE_00, développement seul, 400 logs au plus par gabarit ; attaque d'évasion : seuls les logs de TEST sont attaqués, jamais l'entraînement. Trois attaques de `src/tp2_attacks.py` : fautes de frappe (taux 0,05 ; 0,10 ; 0,20 ; 0,30 ; 0,50), lettres trompeuses ou homoglyphes (mêmes taux), mots ajoutés (taux 0,1 ; 0,3 ; 0,5 ; 1,0 ; 2,0). Modèles : TF-IDF mots et TF-IDF caractères 3 à 5 (régression logistique, C = 4). Pour chaque unité : une mesure « sans attaque » (baseline), 15 mesures attaquées, et 5 mesures « homoglyphes + normalisation UTS #39 » (défense par la table officielle, `unconfuse`). Mesures, sur les mêmes logs : macro-F1 des classes connues (palier A), AUROC de détection d'inconnus (MSP et confiance de la famille), part de connus rejetés à tort avec le seuil réglé sur le test propre (5 % de rejet sans attaque). Analyse : chaque attaque contre « sans attaque » à chaque degré (Wilcoxon apparié, Holm) ; tendance avec le degré (Spearman par unité puis Wilcoxon) ; moyenne sur les degrés par attaque ; PUIS comparaison entre attaques (Friedman, Nemenyi) sur la perte moyenne.

*Justification.* Demande de l'étudiant (2026-11-07) : pour chacune des trois attaques, comparer à « sans attaque », varier le degré, comparer chaque attaque en interne selon le degré, faire la moyenne, puis comparer les attaques entre elles ; tout par rapport à la baseline. Sources : sources_v3_methodes.md (Lowd et Meek, Boucher et al., UTS #39).

*Preuve.* scripts/v3_blockD.py

### D15 : Bloc E : calibration, plusieurs méthodes dont des variantes pour le monde ouvert  (version 1, 2026-11-09 12:40:19)

Protocole : 5 rotations × répétition 0 × 5 plis de groupes = 25 unités, SIEVE_00, développement seul. Dans chaque unité, les gabarits d'entraînement sont partagés en deux : 75 % servent à entraîner la régression logistique (C = 4, TF-IDF mots), 25 % à CALIBRER (jeu de calibration formé de gabarits que le modèle n'a pas vus, comme le test). Méthodes : aucune (baseline) ; température ; vector scaling ; calibration isotonique (probabilité de la classe prédite) ; histogram binning (15 bacs) ; Platt sur la probabilité de la classe prédite ; température ajustée sur des classes cachées pour de faux (notre variante pour le monde ouvert : on cache 4 classes connues à l'intérieur du jeu de calibration et on ajuste T pour maximiser l'AUROC d'inconnu du MSP) ; prédiction conforme (couverture visée 90 %, rejet quand l'ensemble de prédiction est vide ou trop grand). Témoin « fuite de calibration » : température ajustée sur des logs des MÊMES gabarits que l'entraînement. Mesures sur les classes connues du test (nouveaux gabarits) : ECE (15 bacs de même effectif), score de Brier, log-vraisemblance négative ; AUROC d'inconnu du MSP calibré ; couverture et taille moyenne des ensembles conformes. Tests : Wilcoxon apparié contre « aucune », Holm ; Friedman et Nemenyi entre méthodes.

*Justification.* Demande de l'étudiant (2026-11-07) : tester plusieurs types de calibration, dont des variantes adaptées au monde ouvert, avec tests statistiques. Sources : Guo et al., Kull et al. (Dirichlet), Zadrozny et Elkan, Nixon et al., Ovadia et al., Angelopoulos et Bates (sources_v3_methodes.md).

*Preuve.* scripts/v3_blockE.py

### D16 : Phase 2, itération I1 : corriger la représentation pour généraliser à de nouveaux gabarits  (version 1, 2026-11-09 13:02:03)

Constat des blocs A à V : environ 0,50 de macro-F1 des classes connues pour toutes les méthodes (19 classifieurs, 3 vectorisations) : le goulot est la représentation face à des gabarits nouveaux. Hypothèse de travail : un mot qui n'apparaît que dans UN gabarit d'entraînement est une valeur (nom d'utilisateur, fichier, chemin) ou un mot propre au gabarit ; il aide à reconnaître ce gabarit mais ne peut pas se généraliser à un nouveau. Le TF-IDF actuel garde les mots présents dans au moins 2 LOGS (min_df = 2), ce qui retient les valeurs d'un gabarit de milliers de logs. Variantes comparées au SVM sur mots (baseline), classification à 30 classes, protocole P2 (25 plis), SIEVE_00, développement seul : (T2, T3, T5) vocabulaire restreint aux mots présents dans au moins 2, 3 ou 5 GABARITS d'entraînement ; (T3M) idem avec m = 3 mais les mots écartés sont remplacés par un marqueur « valeur » unique (étiquetage des champs variables détectés par les gabarits) ; (ENS) moyenne des marges du SVM mots et du SVM caractères ; (WGT) apprentissage où chaque gabarit pèse autant (poids 1 / nombre de logs du gabarit) ; (COMB) combinaison des variantes retenues. Le test v2 n'est JAMAIS lu.

*Justification.* Demande de l'étudiant (2026-11-07) : proposer une solution maison (remplacer les valeurs variables par des marqueurs, étiqueter les champs pertinents, combiner mots et lettres, formules maison) et itérer pour atteindre le score maximal. La règle de support par gabarit est notre formule F4 : elle remplace une statistique sur les logs par une statistique sur les gabarits, l'unité de généralisation. Elle découle de HB5 et du bloc A (les gabarits sont l'unité). Le masquage numérique par type est déjà testé au notebook v1 (V1 : écart −0,002, indistinguable).

*Preuve.* scripts/v3_phase2_I1.py

## Hypothèses (préinscrites, puis confirmées ou réfutées)

### HA1 : Le découpage au hasard gonfle le score  (version 4, 2026-11-07 22:29:59 ; **statut : confirmée**)

Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).

*Justification.* Rejouée comme demandé par l'étudiant : l'appariement de la version 2 n'était pas justifié ; les deux nouvelles analyses n'en dépendent pas.

*Preuve.* Deux preuves indépendantes de l'écart entre découpage au hasard et par groupes : (1) HA1b, montage apparié sur les mêmes logs de test (voir HA1b) ; (2) réanalyse non appariée des anciennes données par le test de Mann-Whitney : pour les six modèles, le plus petit score sous P0 dépasse le plus grand sous P2 (écart de 0,47 à 0,55, Cliff delta = 1, p ajusté < 1e-6).  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Version 4. La version 2 (« confirmée », appariement injustifié) et la version 3 (« non tranchée ») restent dans l'historique ; le verdict final repose sur HA1b et la réanalyse non appariée, pas sur l'appariement initial.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 21:54:05) : statut préinscrite ; Pour chaque modèle, le macro-F1 du palier A est plus élevé sous P0 (au hasard) que sous P2 (par groupes) d'au moins 0,20 (Wilcoxon apparié par pli, Holm p < 0,05).
- v2 (2026-11-07 21:58:55) : statut confirmée ; Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).
- v3 (2026-11-07 22:06:03) : statut non tranchée ; Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).

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

### HA1b : Effet pur de la fuite, sur les mêmes logs de test  (version 2, 2026-11-07 22:29:59 ; **statut : confirmée**)

Montage apparié : pour chaque pli de groupes (répétition r, pli k), le test est une moitié tirée au hasard des logs du pli (T_b). Condition G : entraînement = logs des autres plis (aucun log des gabarits de test). Condition H : entraînement = G plus l'autre moitié des logs du pli (T_a), donc des logs des mêmes gabarits que T_b. Les deux conditions sont évaluées sur les MÊMES logs T_b. Hypothèse : pour chacun des six modèles, le macro-F1 du palier A est plus élevé en H qu'en G d'au moins 0,20 (Wilcoxon apparié sur 25 plis, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Écart H moins G (macro-F1 du palier A, mêmes logs de test, 25 plis) : centroïde +0,294 [0,261 ; 0,323] ; kNN +0,521 [0,497 ; 0,543] ; régression logistique +0,483 [0,461 ; 0,504] ; Naive Bayes +0,430 [0,404 ; 0,454] ; SVM caractères +0,477 [0,453 ; 0,502] ; SVM mots +0,474 [0,457 ; 0,491]. Les six dépassent 0,20 ; plus petit écart observé sur un pli : +0,117 (centroïde). Wilcoxon sur 25 plis, p ajusté de Holm < 1e-6, Cliff delta = 1 pour les six. Sans fuite (G), le SVM mots donne 0,504, soit le score de P2 (0,503) : le montage reproduit bien P2.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Plus un modèle mémorise, plus la fuite le gonfle : le kNN passe de 0,41 à 0,93 (+0,52), le centroïde, qui résume chaque classe par un seul centre, ne gagne que +0,29.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Montage apparié : pour chaque pli de groupes (répétition r, pli k), le test est une moitié tirée au hasard des logs du pli (T_b). Condition G : entraînement = logs des autres plis (aucun log des gabar…

### HB1 : La hiérarchie n'améliore pas le macro-F1 des classes  (version 2, 2026-11-07 22:29:59 ; **statut : confirmée**)

Sous P2, le macro-F1 des classes (palier A) du modèle hiérarchique ne diffère pas significativement du modèle plat de même famille (régression logistique) : Wilcoxon, Holm p >= 0,05, ou |écart| < 0,03.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Macro-F1 des classes (palier A), hiérarchique moins plat (régression logistique) : −0,014, IC 95 % [−0,024 ; −0,004], p Holm 0,037. La hiérarchie n'améliore pas : elle est même très légèrement moins bonne (significatif après Holm), mais |écart| = 0,014 < 0,03, donc la règle (« ne diffère pas, ou |écart| < 0,03 ») est satisfaite.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Précédent (notebook v1, étape 7.3, test v1 consommé, palier A) : plat 0,4832 contre hiérarchique 0,5153, écart +0,023, IC [−0,010 ; +0,047], non tranchée. Actuel (v3, développement, P2) : plat 0,4947 contre hiérarchique 0,4806, écart −0,014. Le signe de l'écart diffère, comme le notebook v1 le soupçonnait (H1 : signe qui change) ; les deux sont proches de zéro. Les deux séries sont conservées.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Sous P2, le macro-F1 des classes (palier A) du modèle hiérarchique ne diffère pas significativement du modèle plat de même famille (régression logistique) : Wilcoxon, Holm p >= 0,05, ou |écart| < 0,03…

### HB2 : La hiérarchie améliore le F1 des familles  (version 2, 2026-11-07 22:29:59 ; **statut : réfutée**)

Le macro-F1 des familles (famille déduite de la classe prédite pour le plat) est plus élevé avec la hiérarchie d'au moins 0,03 (Wilcoxon, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* F1 des familles (famille déduite de la classe prédite), hiérarchique moins plat : +0,013, IC 95 % [+0,002 ; +0,024], p Holm 0,055. Le gain n'est ni d'au moins 0,03 ni significatif après Holm ; l'IC exclut un gain de 0,03.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* La tête « famille » directe est un peu meilleure (0,706 contre 0,693 en F1 famille moyen) mais pas assez pour la règle.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Le macro-F1 des familles (famille déduite de la classe prédite pour le plat) est plus élevé avec la hiérarchie d'au moins 0,03 (Wilcoxon, Holm p < 0,05).

### HB3 : La hiérarchie réduit la gravité des erreurs  (version 2, 2026-11-07 22:29:59 ; **statut : réfutée**)

La distance moyenne d'erreur dans l'arbre (0 même classe, 1 même famille, 2 autre famille) est plus petite avec la hiérarchie (Wilcoxon, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Distance moyenne d'erreur dans l'arbre, hiérarchique moins plat : −0,001, IC [−0,022 ; +0,020], p Holm 0,94. Aucune réduction de la gravité des erreurs.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; La distance moyenne d'erreur dans l'arbre (0 même classe, 1 même famille, 2 autre famille) est plus petite avec la hiérarchie (Wilcoxon, Holm p < 0,05).

### HB4 : Plusieurs prototypes valent mieux qu'un  (version 2, 2026-11-07 22:29:59 ; **statut : non tranchée**)

Le k-means par classe à 10 prototypes dépasse le centroïde unique (Wilcoxon, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* k-means par classe à 10 prototypes moins centroïde unique : +0,026, IC 95 % [−0,000 ; +0,051], p Holm 0,067. Le critère (p Holm < 0,05) n'est pas atteint, mais l'IC ne se distingue de zéro que par un cheveu et n'exclut pas un gain jusqu'à 0,05.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Règle de classement des verdicts : « réfutée » seulement si l'IC exclut un effet notable (cas de HA6, HB2, HB3) ; ici l'effet reste plausible, donc « non tranchée ». À rejouer avec plus de graines ou une autre dimension SVD (itération de la phase 2).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Le k-means par classe à 10 prototypes dépasse le centroïde unique (Wilcoxon, Holm p < 0,05).

### HB5 : Les gabarits-prototypes (F3) dépassent le centroïde mais pas le SVM  (version 2, 2026-11-07 22:29:59 ; **statut : confirmée**)

Sous P2, gabarits-prototypes meilleur que le centroïde (Holm p < 0,05) et inférieur au SVM sur mots d'au moins 0,03.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Gabarits-prototypes moins centroïde : +0,044, IC [+0,020 ; +0,069], p Holm 0,007 ; SVM mots moins gabarits-prototypes : +0,054, IC [+0,035 ; +0,073], p Holm 8e-5 (>= 0,03). Les gabarits-prototypes (0,449) battent le centroïde (0,406) mais pas le SVM (0,503).  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Notre proposition F3 donne le meilleur résultat des méthodes de ressemblance après le k-means global à 150 groupes, sans être entraînée de façon discriminante.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Sous P2, gabarits-prototypes meilleur que le centroïde (Holm p < 0,05) et inférieur au SVM sur mots d'au moins 0,03.

### HB6 : Le clustering non supervisé n'atteint pas le SVM  (version 2, 2026-11-07 22:29:59 ; **statut : non tranchée**)

Aucun des clustering globaux non supervisés (k-means global, Birch, DBSCAN, HDBSCAN) n'atteint le SVM sur mots : écart d'au moins 0,05, Holm p < 0,05, pour chacun.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Écart SVM mots moins chaque clustering global (macro-F1 palier A) : k-means 60 groupes +0,096 ; Birch +0,111 ; DBSCAN +0,092 ; HDBSCAN +0,086 ; k-means 150 groupes +0,049 [0,026 ; 0,072]. Les cinq sont significativement inférieurs au SVM (p Holm < 5e-4), mais k-means 150 manque le seuil préinscrit de 0,05 de 0,001 et son IC contient 0,05.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* L'essentiel de l'hypothèse (aucun clustering global n'atteint le SVM) est confirmé ; le seuil quantitatif ne l'est pas pour un des cinq. Constat additionnel : k-means à 150 groupes (0,454) fait mieux que k-means à 60 groupes (0,408) : des groupes plus fins, proches du nombre de gabarits, aident, ce qui va dans le sens des gabarits-prototypes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Aucun des clustering globaux non supervisés (k-means global, Birch, DBSCAN, HDBSCAN) n'atteint le SVM sur mots : écart d'au moins 0,05, Holm p < 0,05, pour chacun.

### HB7 : Un clustering par classe rivalise avec le kNN  (version 2, 2026-11-07 22:29:59 ; **statut : confirmée**)

Au moins une méthode de clustering supervisé par classe (k-means, mélange gaussien, Ward) ou les gabarits-prototypes est indiscernable du kNN (Friedman puis Nemenyi : différence de rang moyen inférieure à la différence critique).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Friedman sur kNN (k = 15), k-means par classe (3 et 10), mélange gaussien, Ward et gabarits-prototypes : p = 0,23 ; différence critique de Nemenyi 1,51 rang ; les cinq méthodes sont à moins de 1,12 rang du kNN : indiscernables.  Fichiers : artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Réserve : les rangs moyens dépendent de l'ensemble des méthodes comparées (Benavoli et al. 2016, S13 dans sources_v3_stats_repro.md). Dans le Friedman sur les 19 sorties, la différence critique monte à 5,60 rangs et kNN (10,2) et gabarits-prototypes (7,6) restent aussi indiscernables.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:06:03) : statut préinscrite ; Au moins une méthode de clustering supervisé par classe (k-means, mélange gaussien, Ward) ou les gabarits-prototypes est indiscernable du kNN (Friedman puis Nemenyi : différence de rang moyen inférieu…

### HC1 : Aucun score n'atteint la cible  (version 2, 2026-11-07 23:12:01 ; **statut : confirmée**)

L'AUROC moyen (125 unités) de chacun des 28 scores est inférieur à 0,80, la valeur « acceptable » du critère S2 posé au notebook.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC moyen maximal sur 125 unités : 0,666 (probabilité maximale de la famille) ; l'énergie 0,639 ; le MSP 0,623. Aucun des 28 scores n'atteint 0,80.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Le notebook v1 donnait 0,60 au test et 0,73 en validation pour les modèles linéaires. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; L'AUROC moyen (125 unités) de chacun des 28 scores est inférieur à 0,80, la valeur « acceptable » du critère S2 posé au notebook.

### HC2 : Distance et densité ne battent pas le MSP  (version 2, 2026-11-07 23:12:01 ; **statut : confirmée**)

Aucun score de distance ou de densité de l'espace SVD (Mahalanobis commune, par classe, relative ; kNN 1 et 10 ; résidu de PCA ; mélange gaussien ; LOF ; forêt d'isolation) ne dépasse le MSP d'au moins 0,02 d'AUROC (Wilcoxon apparié, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Aucun score de distance ou de densité ne dépasse le MSP. Tous sont significativement MOINS bons (Wilcoxon, p Holm < 0,012) : Mahalanobis commune −0,027 ; par classe −0,082 ; relative −0,043 ; kNN 1 −0,027 ; kNN 10 −0,033 ; résidu de PCA −0,045 ; mélange gaussien −0,045 ; LOF −0,155 ; forêt d'isolation −0,074.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Cohérent avec le notebook v1 (Mahalanobis échoue avec TF-IDF). La covariance par classe est la pire des Mahalanobis : peu de logs par classe et par pli pour estimer une matrice 100 × 100. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; Aucun score de distance ou de densité de l'espace SVD (Mahalanobis commune, par classe, relative ; kNN 1 et 10 ; résidu de PCA ; mélange gaussien ; LOF ; forêt d'isolation) ne dépasse le MSP d'au moin…

### HC3 : Les méthodes de la vision n'apportent rien sur ces vecteurs  (version 2, 2026-11-07 23:12:01 ; **statut : confirmée**)

Aucune des méthodes ASH, SCALE, DICE, NNGuide, SHE, ViM ne dépasse l'énergie de la tête SVD d'au moins 0,02 d'AUROC (Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Écart de chaque méthode de la vision contre l'énergie de la tête SVM : ASH −0,005 [−0,015 ; +0,004] ; SCALE −0,008 ; DICE −0,047 (p Holm 0,0007) ; NNGuide +0,011 [+0,003 ; +0,020] (p Holm 0,039, donc significatif mais inférieur au seuil de 0,02) ; SHE −0,024 ; ViM +0,004 [−0,012 ; +0,020].  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Ces méthodes sont ADAPTÉES à des vecteurs signés (D11) : ce résultat ne dit rien de leur performance sur les réseaux profonds en vision. NNGuide est la seule à apporter un petit gain. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; Aucune des méthodes ASH, SCALE, DICE, NNGuide, SHE, ViM ne dépasse l'énergie de la tête SVD d'au moins 0,02 d'AUROC (Holm p < 0,05).

### HC4 : Notre F3 (gabarits-prototypes avec rayon) bat le MSP  (version 2, 2026-11-07 23:12:01 ; **statut : réfutée**)

Le score « distance au gabarit le plus proche normalisée par son rayon » dépasse le MSP d'au moins 0,02 d'AUROC (Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Score F3 (distance au gabarit le plus proche normalisée par son rayon) moins MSP : −0,043, IC 95 % [−0,060 ; −0,027], p Holm 1e-5. Il est significativement moins bon, et l'IC exclut +0,02.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Notre proposition F3 n'est pas retenue en l'état pour détecter l'inconnu ; son principe (prototypes par gabarit) reste utile pour classer (HB5). Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; Le score « distance au gabarit le plus proche normalisée par son rayon » dépasse le MSP d'au moins 0,02 d'AUROC (Holm p < 0,05).

### HC5 : Le rayon du gabarit est utile  (version 2, 2026-11-07 23:12:01 ; **statut : réfutée**)

Le score avec rayon (F3) dépasse le même score sans rayon (distance brute au gabarit le plus proche) d'au moins 0,01 d'AUROC (Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Score avec rayon moins score sans rayon : −0,018, IC [−0,029 ; −0,007], p Holm 0,007. Le rayon NUIT (distance brute 0,598 contre 0,580 avec rayon).  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Normaliser par la dispersion du gabarit donne un poids exagéré aux gabarits très serrés. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; Le score avec rayon (F3) dépasse le même score sans rayon (distance brute au gabarit le plus proche) d'au moins 0,01 d'AUROC (Holm p < 0,05).

### HC6 : La fusion bat ses composants  (version 2, 2026-11-07 23:12:01 ; **statut : réfutée**)

La fusion par moyenne de rangs de MSP, Mahalanobis commune et kNN 10 dépasse le meilleur de ses trois composants d'au moins 0,01 d'AUROC (Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Fusion par moyenne de rangs (MSP, Mahalanobis commune, kNN 10) moins le MSP, meilleur de ses composants : −0,005, IC [−0,016 ; +0,006], p 0,45 ; l'IC exclut +0,01.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Les composants de distance sont moins bons que le MSP (HC2) : les fusionner ne rattrape pas le meilleur. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; La fusion par moyenne de rangs de MSP, Mahalanobis commune et kNN 10 dépasse le meilleur de ses trois composants d'au moins 0,01 d'AUROC (Holm p < 0,05).

### HC7 : Un frère connu cache l'inconnu  (version 2, 2026-11-07 23:12:01 ; **statut : non tranchée**)

L'AUROC du MSP est plus faible d'au moins 0,05 pour les classes masquées dont la famille contient une autre classe connue que pour celles sans classe sœur connue (Mann-Whitney sur les couples classe × rotation, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Test impossible avec ce plan : sur les 30 couples classe masquée × rotation, 29 ont une classe sœur connue et un seul n'en a pas (la famille « alerte de sécurité » n'a qu'une classe). AUROC du MSP : 0,616 avec sœur connue (n = 29), 0,773 sans (n = 1) ; Mann-Whitney p = 0,53, sans valeur.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* À refaire avec un autre critère, par exemple la ressemblance de la classe masquée à la classe connue la plus proche (itération de la phase 2). Notebook v1 : la comparaison 0,51 contre 0,66 portait sur la famille de la classe de REMPLACEMENT, ce que ce plan ne mesure pas. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; L'AUROC du MSP est plus faible d'au moins 0,05 pour les classes masquées dont la famille contient une autre classe connue que pour celles sans classe sœur connue (Mann-Whitney sur les couples classe ×…

### HC8 : Forte variabilité entre rotations  (version 2, 2026-11-07 23:12:01 ; **statut : confirmée**)

L'écart-type de l'AUROC du MSP entre les cinq rotations (moyennes par rotation) est d'au moins 0,05.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC du MSP par rotation : 0,790 ; 0,636 ; 0,584 ; 0,601 ; 0,506 ; écart-type entre rotations 0,104 (>= 0,05). La rotation 5 est à peine au-dessus du hasard.  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Le résultat dépend fortement des classes cachées : une conclusion sur une seule rotation n'est pas fiable. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; L'écart-type de l'AUROC du MSP entre les cinq rotations (moyennes par rotation) est d'au moins 0,05.

### HC9 : Trop d'inconnus acceptés  (version 2, 2026-11-07 23:12:01 ; **statut : confirmée**)

Le FPR@95 moyen (inconnus acceptés quand on garde 95 % des connus) est d'au moins 0,70 pour chacun des 28 scores.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* FPR@95 moyen (inconnus acceptés quand on garde 95 % des connus) : minimum 0,827 (probabilité maximale de la famille), maximum 0,983 (OpenMax) ; les 28 scores sont au-dessus de 0,82, loin du critère S3 (au plus 0,50).  Fichiers : artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* En pratique : pour garder 95 % des logs connus, on laisse passer 83 à 98 % des inconnus. Une unité (rotation 1, répétition 0, pli 0) avait été vue au test de fumée, avant le calcul complet ; le verdict repose sur les 125 unités.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 22:55:54) : statut préinscrite ; Le FPR@95 moyen (inconnus acceptés quand on garde 95 % des connus) est d'au moins 0,70 pour chacun des 28 scores.

### HV1 : Les caractères résistent mieux au bruit que les mots  (version 2, 2026-11-09 12:37:31 ; **statut : confirmée**)

La perte de macro-F1 des classes connues entre p = 0 et p = 0,5 est plus petite pour TF-IDF caractères que pour TF-IDF mots (Wilcoxon apparié sur les unités rotation × répétition × pli, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte de macro-F1 des classes connues de p = 0 à p = 0,5 : mots 0,027 ; caractères 0,003 ; Skip-gram −0,031 (il gagne). Caractères moins mots = −0,024 ; Wilcoxon apparié sur 50 blocs, p = 1,3e-4.  Fichiers : artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

*Note.* Les caractères sont presque insensibles au bruit : une lettre abîmée ne détruit qu'une partie des n-grammes d'un mot. Une unité (p = 0, rotation 1, répétition 0, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 300 unités (50 blocs rotation × répétition × pli par fichier).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; La perte de macro-F1 des classes connues entre p = 0 et p = 0,5 est plus petite pour TF-IDF caractères que pour TF-IDF mots (Wilcoxon apparié sur les unités rotation × répétition × pli, Holm p < 0,05)…

### HV2 : Le bruit dégrade chaque vectorisation  (version 2, 2026-11-09 12:37:31 ; **statut : réfutée**)

Pour chacune des trois vectorisations, le macro-F1 des classes connues décroît avec p (tendance de Spearman négative, p Holm < 0,05, sur les moyennes par unité).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Tendance du macro-F1 avec p (Spearman par bloc, puis Wilcoxon unilatéral, Holm sur 3) : mots rho médian −0,71, p Holm < 1e-5 (décroît) ; caractères −0,09, p Holm 0,17 (pas de tendance significative) ; Skip-gram +0,26, p Holm 0,99 (il MONTE avec le bruit : 0,437 à p = 0 ; 0,468 à p = 0,5).  Fichiers : artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

*Note.* Seuls les mots baissent. Skip-gram progresse avec le bruit ; explication possible, NON testée : les fichiers bruités fournissent des contextes plus variés (mots déplacés, remplacés) à l'apprentissage des vecteurs. À tester (augmentation par bruit, phase 2). Une unité (p = 0, rotation 1, répétition 0, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 300 unités (50 blocs rotation × répétition × pli par fichier).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; Pour chacune des trois vectorisations, le macro-F1 des classes connues décroît avec p (tendance de Spearman négative, p Holm < 0,05, sur les moyennes par unité).

### HV3 : Skip-gram est moins bon que TF-IDF mots à tous les niveaux de bruit  (version 2, 2026-11-09 12:37:31 ; **statut : confirmée**)

À chacun des six niveaux de p, le macro-F1 de Skip-gram pondéré IDF est inférieur à celui de TF-IDF mots (Wilcoxon, Holm p < 0,05 sur les six).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Skip-gram moins TF-IDF mots à chaque p : −0,086 ; −0,065 ; −0,050 ; −0,042 ; −0,041 ; −0,027 (p de 0 à 0,5). Wilcoxon sur 50 blocs, p Holm < 1e-4 pour les six.  Fichiers : artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

*Note.* L'écart se réduit avec le bruit (de −0,086 à −0,027) parce que les mots baissent et que Skip-gram monte. Une unité (p = 0, rotation 1, répétition 0, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 300 unités (50 blocs rotation × répétition × pli par fichier).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; À chacun des six niveaux de p, le macro-F1 de Skip-gram pondéré IDF est inférieur à celui de TF-IDF mots (Wilcoxon, Holm p < 0,05 sur les six).

### HV4 : Le meilleur au propre reste le meilleur au bruit maximal  (version 2, 2026-11-09 12:37:31 ; **statut : non tranchée**)

La vectorisation au macro-F1 le plus élevé à p = 0 est aussi la meilleure à p = 0,5 (rangs moyens de Friedman).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Rangs moyens de Friedman : à p = 0, mots 1,42, caractères 1,76, Skip-gram 2,82 ; à p = 0,5, caractères 1,62, mots 1,76, Skip-gram 2,62 (différence critique 0,47 dans les deux cas). Le meilleur change au niveau des estimations (mots puis caractères), mais mots et caractères sont dans la différence critique aux deux niveaux : ni le renversement ni la stabilité ne sont établis. Seul Skip-gram est nettement dernier.  Fichiers : artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

*Note.* À préciser avec plus d'unités ; en pratique mots et caractères sont équivalents sur le macro-F1 des classes connues. Une unité (p = 0, rotation 1, répétition 0, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 300 unités (50 blocs rotation × répétition × pli par fichier).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; La vectorisation au macro-F1 le plus élevé à p = 0 est aussi la meilleure à p = 0,5 (rangs moyens de Friedman).

### HV5 : Le bruit abaisse la détection d'inconnus  (version 2, 2026-11-09 12:37:31 ; **statut : confirmée**)

L'AUROC du MSP décroît avec p pour TF-IDF mots (Spearman négatif, p < 0,05 sur les moyennes par unité).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC du MSP (TF-IDF mots) selon p : rho médian −0,31 sur 50 blocs, 30 blocs sur 50 négatifs, Wilcoxon unilatéral p = 0,038. Valeur moyenne de 0,622 à p = 0 à 0,615 à p = 0,5.  Fichiers : artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

*Note.* Effet faible, à la limite du seuil ; le résultat est exploratoire dans son esprit (hypothèse déclarée exploratoire). Une unité (p = 0, rotation 1, répétition 0, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 300 unités (50 blocs rotation × répétition × pli par fichier).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; L'AUROC du MSP décroît avec p pour TF-IDF mots (Spearman négatif, p < 0,05 sur les moyennes par unité).

### HT1 : Le Transformer n'améliore pas la classification des classes connues  (version 1, 2026-11-07 23:25:34 ; **statut : préinscrite**)

Sur les mêmes logs de test, le macro-F1 des classes connues du Transformer dépasse celui de la baseline TF-IDF d'au plus 0,02 (Wilcoxon sur les 30 couples fichier × rotation, moyenne des graines, Holm).

*Justification.* Notebook v1 : encodeur 0,46 contre TF-IDF 0,49 au test (l'encodeur ne fait pas mieux), hypothèse de décalage de domaine.

*Note.* Écrit le 2026-11-07 avant tout calcul des blocs V et T.

### HT2 : Mahalanobis aide sur les vecteurs du Transformer  (version 1, 2026-11-07 23:25:34 ; **statut : préinscrite**)

L'AUROC de Mahalanobis (vecteurs de 768 valeurs) dépasse celui du MSP du même Transformer d'au moins 0,03 (Wilcoxon sur les 30 couples, Holm p < 0,05).

*Justification.* Notebook v1 (10.4c) : +0,057 dans les cinq rotations ; Podolskiy et al. et Zhou et al. (sources v1) la donnent efficace sur des Transformers affinés.

*Note.* Écrit le 2026-11-07 avant tout calcul des blocs V et T.

### HT3 : La confiance sur la famille aide aussi pour le Transformer  (version 1, 2026-11-07 23:25:34 ; **statut : préinscrite**)

L'AUROC de la confiance sur la FAMILLE du Transformer dépasse celui de son MSP d'au moins 0,02 (Wilcoxon sur les 30 couples, Holm p < 0,05).

*Justification.* Extension de la décision D12 (comparaison exploratoire du bloc C, à confirmer sur un autre modèle).

*Note.* Écrit le 2026-11-07 avant tout calcul des blocs V et T.

### HT4 : Le Transformer perd moins avec le bruit que TF-IDF  (version 1, 2026-11-07 23:25:34 ; **statut : préinscrite**)

La perte de macro-F1 des classes connues entre p = 0 et p = 0,5 est plus petite pour le Transformer que pour la baseline TF-IDF (Wilcoxon sur les 15 couples rotation × graine, p < 0,05).

*Justification.* Les sous-mots d'un Transformer tolèrent mieux les mots abîmés que le sac de mots.

*Note.* Écrit le 2026-11-07 avant tout calcul des blocs V et T.

### HD1 : Chaque attaque dégrade le monde connu  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

Pour le modèle TF-IDF mots, au degré maximal, chacune des trois attaques fait baisser le macro-F1 des classes connues par rapport à « sans attaque » (Wilcoxon apparié sur 25 unités, Holm sur 3, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte de macro-F1 (mots, degré 5, 25 unités) : fautes −0,088 (−16,7 %), homoglyphes −0,254 (−48,2 %), remplissage −0,128 (−24,4 %) ; p Holm < 1e-4 pour les trois.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Pour le modèle TF-IDF mots, au degré maximal, chacune des trois attaques fait baisser le macro-F1 des classes connues par rapport à « sans attaque » (Wilcoxon apparié sur 25 unités, Holm sur 3, p < 0,…

### HD2 : La perte croît avec le degré  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

Pour chaque attaque (modèle mots), la perte de macro-F1 augmente avec le degré (Spearman par unité sur les cinq degrés, puis Wilcoxon unilatéral sur les 25 unités, Holm sur 3).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Spearman médian 1,0 pour chaque attaque (25/25, 25/25, 24/25 unités avec rho > 0) ; p Holm < 1e-4. Pertes moyennes par degré : fautes 0,010 → 0,088 ; homoglyphes 0,024 → 0,254 ; remplissage 0,007 → 0,128.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Pour chaque attaque (modèle mots), la perte de macro-F1 augmente avec le degré (Spearman par unité sur les cinq degrés, puis Wilcoxon unilatéral sur les 25 unités, Holm sur 3).

### HD3 : Les lettres trompeuses sont la pire attaque  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

La perte moyenne de macro-F1 sur les cinq degrés (modèle mots) est la plus grande pour les homoglyphes ; Friedman puis Nemenyi : les homoglyphes sont au-delà de la différence critique des deux autres attaques.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte moyenne sur 5 degrés : homoglyphes 0,111 ; remplissage 0,046 ; fautes 0,040. Friedman p = 6,6e-9 ; rangs moyens 3,0 contre 1,56 et 1,44, écarts supérieurs à la différence critique (0,66) ; Nemenyi p < 1e-4 dans les deux comparaisons.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; La perte moyenne de macro-F1 sur les cinq degrés (modèle mots) est la plus grande pour les homoglyphes ; Friedman puis Nemenyi : les homoglyphes sont au-delà de la différence critique des deux autres …

### HD4 : Les caractères résistent mieux aux fautes et aux homoglyphes, pas au remplissage  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

La perte moyenne de macro-F1 du modèle caractères est plus petite que celle du modèle mots pour les fautes et pour les homoglyphes (Wilcoxon apparié, Holm sur 3), mais pas pour les mots ajoutés.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte caractères moins mots : fautes −0,034 (p Holm < 1e-4), homoglyphes −0,087 (p Holm < 1e-4), remplissage +0,005 (p Holm 0,58, pas d'avantage). Les caractères résistent aux déformations de lettres, pas à l'ajout de mots.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; La perte moyenne de macro-F1 du modèle caractères est plus petite que celle du modèle mots pour les fautes et pour les homoglyphes (Wilcoxon apparié, Holm sur 3), mais pas pour les mots ajoutés.

### HD5 : La normalisation UTS #39 annule les homoglyphes  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

Avec la normalisation, la perte résiduelle de macro-F1 des homoglyphes (modèle mots) est inférieure à 0,01 à chacun des cinq degrés.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Avec la normalisation UTS #39 officielle, perte résiduelle des homoglyphes 0,000 aux cinq degrés (sans normalisation : 0,024 / 0,044 / 0,089 / 0,142 / 0,254).  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Note.* La table officielle ramène exactement le texte attaqué au texte d'origine pour les caractères que l'attaque utilise ; la limite est que l'attaquant pourrait employer des caractères absents de la table.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Avec la normalisation, la perte résiduelle de macro-F1 des homoglyphes (modèle mots) est inférieure à 0,01 à chacun des cinq degrés.

### HD6 : Les attaques font rejeter à tort des logs connus  (version 2, 2026-11-09 13:07:19 ; **statut : confirmée**)

Le taux de logs connus rejetés à tort (seuil réglé sur le test propre) augmente avec le degré des homoglyphes (Spearman par unité puis Wilcoxon unilatéral, p < 0,05) pour le MSP du modèle mots.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Connus rejetés à tort (MSP, mots) par degré d'homoglyphes : 0,061 / 0,075 / 0,115 / 0,164 / 0,268 ; rho médian 1,0, 24/25 unités avec rho > 0, p = 3,1e-6.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Le taux de logs connus rejetés à tort (seuil réglé sur le test propre) augmente avec le degré des homoglyphes (Spearman par unité puis Wilcoxon unilatéral, p < 0,05) pour le MSP du modèle mots.

### HD7 : La confiance sur la famille résiste mieux que le MSP  (version 2, 2026-11-09 13:07:19 ; **statut : réfutée**)

Au degré maximal de chaque attaque, la perte d'AUROC d'inconnu de la confiance sur la famille est plus petite que celle du MSP (Wilcoxon apparié, Holm sur 3).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte d'AUROC d'inconnu au degré maximal : famille moins MSP = +0,012 (fautes, p Holm 0,13), +0,035 (homoglyphes, p Holm 0,077), +0,047 (remplissage, p Holm 0,077). Le signe est l'inverse de celui prédit : la confiance sur la famille perd PLUS que le MSP.  Fichiers : artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv

*Note.* Le meilleur détecteur d'inconnus propre (famille) est aussi plus fragile aux attaques ; l'avantage de D12 est donc à confirmer sous attaque, pas à supposer.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Au degré maximal de chaque attaque, la perte d'AUROC d'inconnu de la confiance sur la famille est plus petite que celle du MSP (Wilcoxon apparié, Holm sur 3).

### HE1 : Toute calibration réduit l'ECE  (version 2, 2026-11-09 12:49:37 ; **statut : réfutée**)

Chacune des méthodes de calibration (température, vector scaling, isotonique, binning, Platt, température sur classes cachées) a un ECE plus petit que « aucune » sur les classes connues du test (Wilcoxon apparié sur 25 unités, Holm sur 6).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* ECE moyen (25 unités) : aucune 0,179 ; température 0,169 (écart −0,010, p Holm 1,0) ; Platt 0,173 (−0,006, p Holm 1,0) ; isotonique 0,186 (+0,007) ; binning 0,190 (+0,011) ; vector scaling 0,226 (+0,046, p Holm 0,0009, PIRE) ; température sur classes cachées 0,323 (+0,144, p Holm 1e-5, PIRE). Aucune méthode ne réduit l'ECE de façon significative ; deux l'aggravent nettement.  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Constat à retenir : sous décalage de gabarits, calibrer sur environ 40 gabarits distincts n'améliore pas la calibration de façon fiable (la température ne gagne que 0,010, non significatif). Notebook v1 : ECE de 0,150 à 0,095 avec la température ; cet effet ne se retrouve pas avec ce protocole, qui est plus strict (jeu de calibration à gabarits distincts de l'entraînement comme du test). Variante « classes cachées » : T tombe au bord de la grille (T = 4), car maximiser l'AUROC de la confiance par un seul réglage de température n'a pas de maximum intérieur ; le modèle devient sous-confiant (ECE et NLL très mauvais) sans gain d'AUROC. Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Chacune des méthodes de calibration (température, vector scaling, isotonique, binning, Platt, température sur classes cachées) a un ECE plus petit que « aucune » sur les classes connues du test (Wilco…

### HE2 : Température et vector scaling sont équivalentes  (version 2, 2026-11-09 12:49:37 ; **statut : réfutée**)

L'ECE du vector scaling diffère de celui de la température de moins de 0,01 en moyenne et la différence n'est pas significative (Wilcoxon, p >= 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Vector scaling moins température : ECE +0,056 (0,226 contre 0,169), p = 1,4e-4 : écart supérieur à 0,01 et significatif.  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Un paramètre par classe, estimé sur une quarantaine de gabarits, surajuste les gabarits de calibration : cohérent avec Ovadia et al. (la calibration a posteriori se dégrade sous décalage). Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; L'ECE du vector scaling diffère de celui de la température de moins de 0,01 en moyenne et la différence n'est pas significative (Wilcoxon, p >= 0,05).

### HE3 : Isotonique et binning ne battent pas la température  (version 2, 2026-11-09 12:49:37 ; **statut : confirmée**)

Sous décalage de gabarits, l'ECE de l'isotonique et du binning n'est pas inférieur à celui de la température (Wilcoxon, p >= 0,05 ou ECE supérieur).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Isotonique moins température : +0,016, p Holm 0,090 ; binning moins température : +0,021, p Holm 0,044 (binning significativement PIRE). Aucune des deux n'est inférieure à la température.  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Les méthodes non paramétriques surajustent le jeu de calibration. Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Sous décalage de gabarits, l'ECE de l'isotonique et du binning n'est pas inférieur à celui de la température (Wilcoxon, p >= 0,05 ou ECE supérieur).

### HE4 : La calibration ne change pas la détection d'inconnus  (version 2, 2026-11-09 12:49:37 ; **statut : réfutée**)

Aucune méthode de calibration monotone (température, Platt, vector scaling) ne modifie l'AUROC d'inconnu du MSP de plus de 0,01.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Variation de l'AUROC d'inconnu du MSP contre « aucune » : température +0,003 (p = 0,15) ; Platt 0,000 ; vector scaling −0,044 (p = 0,15). La règle (« aucune méthode ne modifie l'AUROC de plus de 0,01 ») est violée par le vector scaling.  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Erreur dans la formulation de l'hypothèse : le vector scaling (une échelle et un biais PAR classe) ne préserve pas l'ordre des scores, contrairement à la température et à Platt, qui conservent l'ordre ; je l'avais rangé à tort parmi les méthodes monotones. Température et Platt respectent bien la règle (écart <= 0,003). Verdict « réfutée » au sens de la règle écrite ; à reformuler. Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Aucune méthode de calibration monotone (température, Platt, vector scaling) ne modifie l'AUROC d'inconnu du MSP de plus de 0,01.

### HE5 : Calibrer sur les mêmes gabarits trompe  (version 2, 2026-11-09 12:49:37 ; **statut : confirmée**)

La température ajustée sur des logs des mêmes gabarits que l'entraînement donne un ECE plus grand, sur le test de nouveaux gabarits, que la température ajustée sur des gabarits distincts (Wilcoxon apparié, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Température ajustée sur des logs des MÊMES gabarits que l'entraînement : ECE 0,296 contre 0,169 pour la température sur gabarits distincts (écart +0,127, p < 1e-6). Valeurs de T : inférieures à 1 (le modèle est rendu encore plus sûr de lui).  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Même fuite qu'au bloc A : un jeu de calibration qui ressemble à l'entraînement apprend une confiance trop optimiste. Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; La température ajustée sur des logs des mêmes gabarits que l'entraînement donne un ECE plus grand, sur le test de nouveaux gabarits, que la température ajustée sur des gabarits distincts (Wilcoxon app…

### HE6 : La prédiction conforme tient sa couverture seulement avec des gabarits distincts  (version 2, 2026-11-09 12:49:37 ; **statut : confirmée**)

Calibrée sur des gabarits distincts, la prédiction conforme à 90 % couvre au moins 87 % des logs connus du test ; calibrée sur les mêmes gabarits que l'entraînement, elle couvre moins de 87 % (moyenne sur 25 unités).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Prédiction conforme visant 90 % : calibrée sur des gabarits distincts, couverture moyenne 0,899, au moins 0,87 dans 18 unités sur 25 ; calibrée sur les mêmes gabarits que l'entraînement, couverture moyenne 0,136, au moins 0,87 dans 0 unité. Les deux conditions de la règle sont satisfaites.  Fichiers : artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

*Note.* Limite pratique : avec des gabarits distincts, les ensembles de prédiction sont énormes (11,9 classes en moyenne sur environ 24) : la garantie de couverture est tenue au prix d'une information très faible. Une unité (rotation 1, pli 0) avait été vue au test de fumée avant le calcul complet ; le verdict repose sur les 25 unités. Un premier calcul (E1) s'était arrêté sur une erreur d'indice : classes connues sans gabarit dans l'ensemble d'ajustement, voir la version E2 de scripts/v3_blockE.py.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 12:40:19) : statut préinscrite ; Calibrée sur des gabarits distincts, la prédiction conforme à 90 % couvre au moins 87 % des logs connus du test ; calibrée sur les mêmes gabarits que l'entraînement, elle couvre moins de 87 % (moyenne…

### HF1 : Le support par gabarit améliore le macro-F1  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

Pour au moins un des trois seuils m = 2, 3, 5 gabarits, le macro-F1 des classes (palier A) dépasse celui du SVM mots d'au moins 0,02 (Wilcoxon apparié sur 25 plis, Holm sur 3, p < 0,05).

*Justification.* Les mots d'un seul gabarit sont des valeurs ou des mots propres au gabarit, qui encombrent le vocabulaire sans se généraliser.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

### HF2 : Le marqueur « valeur » apporte quelque chose de plus que la suppression  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

T3M (mots écartés remplacés par un marqueur) dépasse T3 (mots écartés supprimés) d'au moins 0,01 (Wilcoxon apparié, p < 0,05).

*Justification.* Le nombre de champs variables d'un log est une information de structure qui disparaît si on supprime les mots.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

### HF3 : Mots et caractères se complètent  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

ENS dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

*Justification.* Deux représentations qui se trompent différemment ; mais au bloc V, mots et caractères étaient équivalents seuls.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

### HF4 : Pondérer les gabarits à égalité aide  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

WGT dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

*Justification.* Les gros gabarits dominent l'apprentissage même avec le plafond de 400 logs.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

### HF5 : La combinaison dépasse chacun de ses composants  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

COMB dépasse chacune des variantes qu'elle combine (Wilcoxon apparié, Holm).

*Justification.* Les gains portent sur des mécanismes différents.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

### HF6 : Objectif de score  (version 1, 2026-11-09 13:02:03 ; **statut : préinscrite**)

Le macro-F1 des classes (palier A) de la meilleure variante atteint au moins 0,55 en moyenne sur les 25 plis (baseline 0,503).

*Justification.* Objectif de l'étudiant : viser le maximum ; 0,55 est un seuil fixé d'avance pour dire si l'itération a franchi une marche notable.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I1.

## Résultats

### RA1 : Bloc A : macro-F1 du palier A par protocole (précédent v1 et actuel v3)  (version 1, 2026-11-07 21:58:55)

**Précédent (notebook v1, étape 3.7, SVM sur TF-IDF mots, SIEVE_00, palier A, tout le jeu d'entraînement) :** P0 0,9872 ; P1 0,4220 ; P2 0,5070 ; P3 0,5105.  **Actuel (v3, SVM sur mots, 400 logs par gabarit au plus, développement) :** P0 0,986 ; P1 0,471 ; P2 0,503 ; P3 0,487.  Les deux séries sont conservées. Écart notable pour P1 (0,422 contre 0,471) : le P1 de v1 est un seul découpage de 36 gabarits de validation, celui de v3 est la moyenne de 5 plis de gabarits différents (écart-type 0,063) ; la valeur de v1 est dans l'intervalle de celles de v3.  Tous les modèles : P0 de 0,874 (centroïde) à 0,988 (SVM caractères) ; P2 de 0,406 (centroïde) à 0,503 (SVM mots).

*Justification.* Montre que le niveau de score et le contraste hasard / gabarit se reproduisent avec un protocole indépendant (autres gabarits de test, nouveau plafond), ce qui renforce la conclusion de v1.

*Preuve.* artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl

*Note.* Conformément à R3, ni la série v1 ni la série v3 n'est écartée.

### RB1 : Bloc B : macro-F1 du palier A sous P2 (précédent v1 et actuel v3)  (version 1, 2026-11-07 22:29:59)

**Actuel (v3, développement, P2, 25 plis) :** SVM mots 0,503 ; régression logistique 0,495 ; hiérarchique 0,481 ; k-means global 150 groupes 0,454 ; gabarits-prototypes 0,449 ; k-means par classe 3 prototypes 0,441 ; Ward 0,439 ; Naive Bayes 0,434 ; k-means par classe 10 prototypes 0,431 ; kNN 15 0,423 ; mélange gaussien 0,422 ; HDBSCAN (sans rejet) 0,418 ; DBSCAN (sans rejet) 0,411 ; kNN 5 0,410 ; k-means 60 groupes 0,408 ; centroïde 0,406 ; Birch 0,392 ; HDBSCAN avec rejet 0,110 ; DBSCAN avec rejet 0,089 (les deux rejettent 82 à 85 % des logs de test).  Repli sur la famille (seuil 0,5) : répond au niveau de la classe pour 72,9 % des logs, justesse de classe sur ces logs 61,7 % ; justesse de famille 71,1 % avec ou sans repli.  **Précédent (notebook v1, étape 7.3, test v1 consommé) :** TF-IDF plat 0,4832, hiérarchique 0,5153 (palier A) ; Skip-gram 0,4027 et 0,4635 (validation).  Les deux séries sont conservées ; aucun modèle ne dépasse 0,51 dans l'une ou l'autre.

*Justification.* Le plafond d'environ 0,50 se retrouve avec un protocole indépendant et 19 méthodes de natures très différentes : le goulot est la représentation (mots) face à des gabarits nouveaux, pas le choix du classifieur. C'est la motivation des pistes de la phase 2 (marqueurs typés, combinaison mots, lettres, Transformer).

*Preuve.* artifacts/results/v3/A_apparie_HA1b.csv ; A_HA1_reanalyse_non_appariee.csv ; B_resume.csv ; B_tests_pairs.csv ; B_nemenyi_tous.csv ; B_repli.csv

*Note.* Cas particulier : les sorties avec rejet de DBSCAN et HDBSCAN comptent un rejet comme une erreur ; elles mesurent surtout que les logs de nouveaux gabarits sont loin de tous les points d'entraînement (utile au bloc C).

### RC1 : Bloc C : AUROC de détection d'inconnus (précédent v1 et actuel v3)  (version 2, 2026-11-09 12:37:31)

**Actuel (v3, développement, P2, 5 rotations × 25 plis = 125 unités, AUROC moyen) :** probabilité maximale de la famille 0,666 ; énergie 0,639 ; logit maximal 0,636 ; MSP hiérarchique 0,633 ; entropie négative 0,632 ; NNGuide 0,625 ; ensemble 0,624 ; MSP (baseline) 0,623 ; fusion de rangs 0,618 ; ViM 0,618 ; énergie de la tête SVD 0,614 ; ASH 0,608 ; SCALE 0,606 ; distance au gabarit 0,598 ; Mahalanobis commune 0,597 ; kNN 1 0,597 ; centroïde 0,594 ; kNN 10 0,591 ; SHE 0,590 ; Mahalanobis relative 0,580 ; F3 avec rayon 0,580 ; mélange gaussien 0,579 ; résidu de PCA 0,579 ; DICE 0,567 ; forêt d'isolation 0,550 ; Mahalanobis par classe 0,541 ; LOF 0,469 ; OpenMax 0,465. Écart-types entre unités de 0,11 à 0,14.  **Précédent (notebook v1, étape 7.5, test v1 consommé, TF-IDF mots, 5 rotations) :** MSP 0,599 ; énergie 0,598 ; prototype 0,625 ; ensemble 0,601 ; MSP hiérarchique 0,609 ; MSP famille 0,623 ; (validation : MSP 0,728). Skip-gram : MSP 0,594.  Les deux séries sont conservées.  **Correction (calcul C2, 2026-11-07) :** OpenMax corrigé = 0,514 (la valeur 0,465 de la version C1 venait d'une formule lue à l'envers ; voir RC3). Les 27 autres scores sont inchangés. Valeur de LOF : 0,469, inchangée, mais son explication était fausse (voir RC4).

*Justification.* Les valeurs v1 au test (0,59 à 0,63) sont dans la fourchette des valeurs v3 ; la valeur de validation v1 (0,73) était optimiste (36 gabarits de validation), comme le notebook l'avait déjà analysé. Le plafond d'environ 0,65 se retrouve avec un protocole indépendant et 28 scores.

*Preuve.* artifacts/results/v3/C_resume.csv ; C_tests_pairs.csv ; C_nemenyi.csv ; C_msp_par_rotation.csv ; C_msp_par_classe.csv ; C_all_units.csv

*Note.* Version 2. La note de la version 1 (« OpenMax simplifié ; LOF : grappes denses, explication non testée ») est remplacée : l'explication des grappes denses est réfutée par construction et par diagnostic (RC4) ; OpenMax avait un défaut d'implémentation corrigé (RC3). La version 1 reste dans l'historique.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:12:01) : statut None ; **Actuel (v3, développement, P2, 5 rotations × 25 plis = 125 unités, AUROC moyen) :** probabilité maximale de la famille 0,666 ; énergie 0,639 ; logit maximal 0,636 ; MSP hiérarchique 0,633 ; entropie…

### RC2 : Bloc C, comparaisons exploratoires (NON préinscrites, décidées après lecture des résultats)  (version 1, 2026-11-07 23:12:01)

Contre le MSP, sur 125 unités, Holm sur 3 comparaisons : probabilité maximale de la famille +0,043, IC 95 % [+0,030 ; +0,056], meilleure dans 90 unités sur 125, p Holm < 1e-5 ; énergie +0,016 [+0,009 ; +0,022], 83 unités sur 125 ; logit maximal +0,012 [+0,008 ; +0,017], 94 unités sur 125. Nemenyi : famille contre MSP p = 0,0003 ; famille contre énergie p = 0,72 (indiscernables). Par rotation, la famille bat le MSP dans les cinq rotations (0,788 contre 0,790 en rotation 1, 0,683 contre 0,636, 0,624 contre 0,584, 0,624 contre 0,601, 0,613 contre 0,506).

*Justification.* Exploratoire : ces trois comparaisons n'avaient pas été préinscrites ; elles sont signalées comme telles et devront être confirmées par une hypothèse préinscrite à la prochaine itération (cela évite de choisir l'hypothèse après coup, règle R2).

*Preuve.* artifacts/results/v3/C_exploratoire_vs_msp.csv

*Note.* Lecture en mots simples : si le modèle ne sait pas dans QUELLE FAMILLE ranger un log, c'est probablement un inconnu. La hiérarchie n'aide pas à classer (HB1) mais aide à rejeter, ce qui rejoint l'idée de repli sur la famille de Linderman et al. (S34 des sources). Dans la rotation 5, où le MSP est au hasard (0,506), la famille garde 0,613.

### RV1 : Bloc V : macro-F1 des classes connues (palier A) selon le bruit (précédent v1 et actuel v3)  (version 1, 2026-11-09 12:37:31)

**Actuel (v3, développement, 50 blocs par fichier, moyenne) :** TF-IDF mots 0,523 ; 0,510 ; 0,510 ; 0,499 ; 0,496 ; 0,496 (p = 0 à 0,5). TF-IDF caractères 0,513 ; 0,520 ; 0,517 ; 0,509 ; 0,508 ; 0,510. Skip-gram IDF 0,437 ; 0,445 ; 0,460 ; 0,458 ; 0,454 ; 0,468.  AUROC du MSP : mots 0,622 à 0,615 ; caractères 0,611 à 0,618 ; Skip-gram 0,564 à 0,563. AUROC de la confiance sur la famille : mots 0,660 à 0,643 ; caractères 0,664 à 0,656 ; Skip-gram 0,599 à 0,590.  **Précédent (notebook v1, étape 8.3, E4a, validation, plat) :** TF-IDF mots 0,493 ; 0,490 ; 0,492 ; 0,481 ; 0,469 ; 0,474 ; Skip-gram IDF 0,405 ; 0,404 ; 0,414 ; 0,399 ; 0,391 ; 0,401.  Les deux séries sont conservées.

*Justification.* Dans les deux séries, TF-IDF mots baisse avec le bruit (de 0,02 à 0,03) et Skip-gram reste derrière (de 0,09 à 0,03). Le gain de Skip-gram avec le bruit, absent de la série v1 (plate), est nouveau et n'est pas expliqué. La confiance sur la FAMILLE bat le MSP pour les trois vectorisations et à tous les niveaux de bruit (écart de 0,02 à 0,05) : réplication, sur d'autres fichiers et d'autres vectorisations, de la comparaison exploratoire RC2 (D12), toujours non préinscrite.

*Preuve.* artifacts/results/v3/V_all_units.csv ; V_resume.csv ; V_HV2.csv ; V_HV3.csv

### RC3 : OpenMax : défaut d'implémentation corrigé (C1 contre C2)  (version 1, 2026-11-09 12:37:31)

OpenMax de la version C1 appliquait la formule de l'article à l'envers : la probabilité de Weibull (qui mesure « loin du signe moyen de la classe ») était utilisée comme son contraire, si bien que plus un log s'éloignait, moins on lui retirait de score. Preuve : sur 15 unités, la version C1 et la version du code de référence de Bendale et Boult sont presque des images miroirs unité par unité (0,29 contre 0,65 ; 0,26 contre 0,70 ; 0,71 contre 0,27). Résultat sur 125 unités : **C1 : AUROC 0,465 ; C2 (corrigé) : 0,514** (écart-type 0,114 ; FPR@95 0,964). OpenMax corrigé est donc proche du hasard.

*Justification.* Vérification demandée par l'étudiant (« il faut en être sûr »). Les verdicts HC1 (maximum 0,666) et HC9 (FPR@95 minimum 0,827) ne changent pas : OpenMax n'est ni le meilleur ni le moins mauvais en FPR@95.

*Preuve.* scripts/v3_diag_C.py ; artifacts/results/v3/C_diagnostic_openmax_lof.csv ; C_resume_C2.csv ; v3_blockC.py (versions C1 et C2)

### RC4 : LOF : explication « grappes denses » réfutée, cause réelle identifiée  (version 1, 2026-11-09 12:37:31)

Diagnostic sur 15 unités (3 par rotation). (1) Le code est correct : la formule du LOF recalculée à la main égale celle de scikit-learn dans 15 unités sur 15. (2) L'explication donnée en RC1 version 1 (les logs d'un même nouveau gabarit forment des grappes denses) est fausse par construction : en mode « nouveauté », chaque log de test est jugé seul contre le jeu d'entraînement, la densité des autres logs de test ne joue aucun rôle. (3) Cause réelle : le LOF est le produit de la densité du voisinage dans le jeu d'entraînement par la sparsité propre du log ; la sparsité propre indique l'inconnu (AUROC 0,607, bon sens) mais la densité du voisinage indique le CONNU (0,590 : les logs connus ont des voisinages plus denses) ; le produit tire dans deux sens opposés : AUROC moyen 0,454. (4) Le signe dépend des classes cachées : AUROC moyen par rotation 0,34 ; 0,68 ; 0,44 ; 0,48 ; 0,34 ; sensibilité faible à k (k = 5 : 0,475 ; k = 20 : 0,454 ; k = 50 : 0,448) et à la banque (complète : 0,483).

*Justification.* Vérification demandée par l'étudiant. Limite : le diagnostic porte sur 15 unités, non 125.

*Preuve.* scripts/v3_diag_C.py ; artifacts/results/v3/C_diagnostic_openmax_lof.csv

### RE1 : Bloc E : calibration (précédent v1 et actuel v3)  (version 1, 2026-11-09 12:49:37)

**Actuel (v3, 25 unités, ECE des classes connues du test, 15 bacs de même effectif) :** température 0,169 ; Platt 0,173 ; aucune 0,179 ; isotonique 0,186 ; binning 0,190 ; vector scaling 0,226 ; température sur mêmes gabarits 0,296 ; température sur classes cachées 0,323. Score de Brier : 0,201 (température) à 0,316. AUROC d'inconnu du MSP : 0,62 pour aucune, température et Platt. Conforme : couverture 0,899 (gabarits distincts) contre 0,136 (mêmes gabarits).  **Précédent (notebook v1, étape 9.6) :** TF-IDF, T = 1,62, ECE de 0,150 à 0,095 en validation, AUROC inchangé 0,603 ; encodeur : ECE 0,18 (validation) puis 0,35 (test) ; confiance annoncée 85 % pour 50 % de bonnes réponses.  Les deux séries sont conservées.

*Justification.* Les deux séries s'accordent sur l'essentiel (la calibration par température ne change pas l'AUROC ; la confiance est trop élevée sous décalage de gabarits : ECE 0,18 ici sans calibration contre 0,15 en v1) mais pas sur le gain de la température (0,150 → 0,095 en v1 ; 0,179 → 0,169 non significatif ici). Le protocole v3, avec calibration sur gabarits distincts, mesure ce que v1 ne mesurait pas : l'instabilité de la température estimée sur peu de gabarits.

*Preuve.* artifacts/results/v3/E_all_units.csv ; E_resume.csv ; E_HE1.csv ; E_HE2.csv ; E_HE3.csv ; E_HE4.csv ; E_HE5.csv ; E_conforme_units.csv

### RD1 : Bloc D : attaques (précédent v1 et actuel v3)  (version 1, 2026-11-09 13:07:19)

**Actuel (v3, 25 unités, modèle mots, degré 5 de 5) :** perte de macro-F1 fautes −0,088, homoglyphes −0,254, remplissage −0,128 ; la perte croît avec le degré dans les trois cas ; le modèle caractères perd 0,006 / 0,024 / 0,051 en moyenne sur les degrés ; la normalisation officielle annule les homoglyphes ; les connus rejetés à tort montent de 0,061 à 0,268. **Précédent :** tableau des attaques du notebook v1 (8.6 et 9.12), conservé tel quel.

*Justification.* La série v3 reprend les trois attaques sur cinq degrés avec tests appariés ; elle précise et n'infirme pas la série v1 (mêmes sens de variation). Elle ajoute la table officielle et le rejet à tort.

*Preuve.* artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv
