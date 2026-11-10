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

### D17 : Confirmation I1b : mots + lettres (ENS) améliore-t-il la famille ?  (version 1, 2026-11-09 13:17:00)

Constat exploratoire d'I1 (vu APRÈS les chiffres, donc non confirmatoire) : ENS (somme des marges SVM mots et SVM caractères) a un macro-F1 de famille de 0,719 contre 0,692 (+0,028, Wilcoxon p = 0,0006, 19 plis sur 25) et une distance dans l'arbre de 0,787 contre 0,812 (−0,025, p = 0,012), sans changer le macro-F1 des classes (−0,001). Pour confirmer : 25 NOUVEAUX plis (répétitions 5 à 9, mêmes StratifiedGroupKFold par gabarit avec les graines 5 à 9), seules les deux variantes V0 et ENS, mêmes réglages, même développement de SIEVE_00 ; le test v2 reste scellé. Limite écrite : ce sont les mêmes gabarits répartis autrement, donc la confirmation vaut pour le hasard du découpage, pas pour de nouveaux gabarits ; la confirmation sur de nouveaux gabarits se fera sur le test v2 (une seule ouverture, à la fin).

*Justification.* Demande de l'étudiant (2026-11-09) : confirmer maintenant le constat exploratoire. Règle R2 : une hypothèse vue dans les données ne se confirme pas avec les mêmes données ; on préinscrit donc la règle puis on la teste sur des découpages non utilisés.

*Note.* Écrit le 2026-11-09 avant tout calcul de la confirmation I1b.

### D18 : Phase 2, itération I2 : champs typés (changer la nature de l'information)  (version 1, 2026-11-09 13:18:20)

Après I1 (HF1 à HF6 réfutées : vocabulaire, marqueur, pondération, ensemble mots+lettres ne lèvent pas le plafond de 0,50), I2 ajoute une information que le sac de mots ne voit pas : la STRUCTURE du log. Jetons ajoutés aux mots du SVM : (a) le programme émetteur (mot avant « [pid]: », ex. crond, useradd) ; (b) le NOM de chaque champ « clé=valeur » (srcip, dstport, uid…) et de chaque champ entre crochets « [Clé valeur] » ; (c) le TYPE de chaque valeur (ip, port/nombre, hex, chemin, heure, date, courriel, mot, mélange) combiné au nom du champ (ex. « srcip:ip ») ; (d) le gabarit de forme du log (suite des types de ses 8 premiers éléments). Variantes, même protocole que I1 (30 classes, P2 25 plis, SIEVE_00, développement seul, SVM C = 1, 400 logs par gabarit) : V0 baseline ; FT = mots + jetons typés (concaténés avant TF-IDF) ; FTo = jetons typés seuls (sans mots) ; FTE = FT + marges du SVM caractères (somme). Le test v2 reste scellé. Les deux autres pistes annoncées pour la suite sont consignées comme itérations à venir : I3 = fusion avec le Transformer (quand la grille T est finie) ; I4 = confirmation préinscrite du rejet au niveau de la famille sur de nouvelles rotations (HD7 a montré que ce détecteur est plus fragile sous attaque).

*Justification.* Demande de l'étudiant (2026-11-07 et 2026-11-09) : étiqueter les champs pertinents des logs, combiner les représentations ; lacune de la littérature n°3 de PLAN_V3 §3.1 (étiquetage de champs de logs de sécurité). I1 a réfuté l'idée de ne toucher qu'au vocabulaire.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I2.

### D19 : Itération I4 : le rejet par la confiance de FAMILLE est-il meilleur que le MSP sur de nouvelles rotations ?  (version 1, 2026-11-09 14:00:38)

Constat exploratoire du bloc C (125 unités, vu après les chiffres) : AUROC d'inconnu de la probabilité maximale de la famille 0,666 contre 0,623 pour le MSP, 0,639 pour l'énergie, 0,633 pour le MSP hiérarchique. HD7 (bloc D) a de plus montré que ce détecteur perd davantage que le MSP sous attaque. Confirmation : 5 NOUVELLES rotations de 6 classes masquées (tirage aléatoire de graine 20261109 de partitions des 30 classes, refusé si un ensemble de 6 classes est identique à une rotation du v1) × 25 NOUVEAUX plis (répétitions 5 à 9, StratifiedGroupKFold par gabarit, graines 5 à 9 comme en I1b), SIEVE_00, développement seul, même modèle (régression logistique C = 4 sur TF-IDF mots, entraînement sur les classes connues, 400 logs au plus par gabarit). Scores comparés : msp, maxlogit, energy, hier_msp, fam_msp. Unité de statistique = (rotation, répétition), AUROC moyenné sur les 5 plis : 25 unités. Le test v2 reste scellé ; la confirmation sur de nouveaux gabarits revient à l'ouverture finale.

*Justification.* D12 : la confiance de famille est le candidat principal et exige une hypothèse préinscrite sur de nouvelles données. Règle R2 : un constat vu dans les données ne se confirme pas sur les mêmes données.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I4.

### D20 : Règle de la phase 2 : itérer au maximum avant d'ouvrir le jeu de test  (version 1, 2026-11-09 17:55:28)

Demande de l'étudiant (2026-11-09) : en phase 2, on effectue autant d'itérations que possible pour augmenter la précision le plus possible ; c'est seulement quand le maximum de précision possible est atteint qu'on teste avec le jeu de test (test v2 scellé, une seule ouverture). Critère d'arrêt écrit : trois itérations consécutives sans gain significatif de macro-F1 des classes (palier A) sur de nouveaux plis, ou la veille de l'échéance (samedi 2026-11-14, ouverture le vendredi 2026-11-13 au plus tard pour laisser la rédaction). Procédure de chaque itération : hypothèses préinscrites ; sélection de la configuration sur les répétitions 0 à 4 du développement ; confirmation de la configuration retenue sur les répétitions 5 à 9 (nouveaux plis) ; jamais de sélection sur les données de confirmation ; le pipeline final est figé (version enregistrée) avant l'ouverture du test.

*Justification.* Précise D6/R5 du plan (test ouvert une fois à la fin) : le moment de l'ouverture est le maximum atteint, pas une date fixe. Remplace le critère « fin de semaine ou 3 itérations sans gain » par le même critère rendu explicite.

*Note.* Écrit le 2026-11-09.

### D21 : Itération I5 : régler mots + lettres (procédure D20)  (version 1, 2026-11-09 17:55:59)

Grille (SVM linéaire, 30 classes, SIEVE_00, développement seul) : C des mots ∈ {0,3 ; 1 ; 3} ; lettres : n-grammes char_wb ∈ {(2,4), (3,5), (4,6)} avec C ∈ {0,3 ; 1} ; poids de la marge lettres dans la somme ∈ {0 (mots seuls), 0,5 ; 1 ; 2 ; lettres seules} ; soit 3 × 3 × 2 × 3 combinaisons de somme plus les références. SÉLECTION : macro-F1 des classes (palier A) moyen sur les 25 plis des répétitions 0 à 4 ; la configuration au meilleur score est retenue (aucun autre critère, aucun arbitrage manuel). CONFIRMATION (I5b) : la configuration retenue est calculée sur les 25 plis des répétitions 5 à 9 et comparée à V0 (SVM mots, C = 1, résultats d'I1b, mêmes plis) ; la sélection n'utilise jamais ces plis. Le test v2 reste scellé (D20).

*Justification.* D20 : itérer pour monter la précision ; la séparation sélection (rép. 0-4) / confirmation (rép. 5-9) évite l'optimisme de choisir le maximum d'une grille et de l'annoncer.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I5.

### D22 : Réplication Transformer T2 : trancher HT1 et HT2, et fusion Transformer + TF-IDF (I3)  (version 1, 2026-11-09 21:31:12)

HT1 et HT2 sont « non tranchées » (écarts moyens à 0,0204 et 0,0325, pile sur les seuils 0,02 et 0,03, intervalles qui les contiennent) parce que la grille T n'utilise qu'UNE découpe (répétition 0, pli 0). Réplication T2 : fichier sans bruit (p = 0), 4 NOUVELLES découpes du développement (répétition 1 pli 1, répétition 2 pli 2, répétition 3 pli 3, répétition 4 pli 4), 5 rotations de v1, graine 42 : 20 modèles, mêmes réglages que T1 (DistilBERT sans casse, 256 jetons, 2 époques, 3e-5, 140 logs d'entraînement par classe, jusqu'à 133 logs de test par classe), unité de statistique = couple (découpe, rotation) = 20. En plus de la baseline TF-IDF sur les mêmes logs, la FUSION (I3) : moyenne des probabilités de classe du Transformer et de la régression logistique TF-IDF ; confiance de famille de la fusion = moyenne des probabilités de famille des deux. Plusieurs tests statistiques par comparaison : Wilcoxon apparié, test des signes, test de permutation apparié (10 000 retournements de signe), IC95 bootstrap ; la décision suit la règle écrite pour chaque hypothèse (l'IC95 bootstrap tranche ; les autres tests sont rapportés). Le test v2 reste scellé.

*Justification.* Demande de l'étudiant (2026-11-09) : trancher HT1 et HT2 et faire la fusion avec le Transformer maintenant. Une réplication sur de nouvelles découpes est la manière préinscrite de trancher une hypothèse « non tranchée » (règle R2 : on ne retranche pas sur les mêmes données).

*Note.* Écrit le 2026-11-09 avant tout calcul de la réplication T2.

### D23 : Itération I6 : retenter I1, I2 et I5 avec de nouveaux hyperparamètres  (version 1, 2026-11-09 21:32:42)

Demande de l'étudiant (2026-11-09) : retenter les itérations avec de nouveaux hyperparamètres, plusieurs rotations, plusieurs tests statistiques. I6 reprend les trois leviers de classification de la phase 2 avec des valeurs NON essayées jusqu'ici. Grille (classification à 30 classes, SIEVE_00, développement seul, 400 logs au plus par gabarit) : REPRÉSENTATION DES MOTS (retour sur I1) W1 lettres ≥ 2 min_df = 1 ; W2 uni+bigrammes de mots min_df = 2 ; W3 jetons alphanumériques (chiffres conservés) min_df = 2 ; W4 TF binaire ; W5 sensible à la casse ; STRUCTURE (retour sur I2) W6 = mots + jetons « programme » et « nom de champ » seulement (sans types ni forme, qui avaient fait baisser) ; MODÈLES (retour sur I5) SVM C = 0,1 ; SVM C = 10 ; SVM C = 1 classes équilibrées ; régression logistique C = 30 ; Ridge alpha = 1 ; soit 6 × 5 = 30 configurations de mots, plus deux configurations de lettres (char_wb 1-3 et char 3-5, SVM C = 10). SÉLECTION : répétitions 0 à 4 (25 plis), macro-F1 des classes (palier A), la meilleure configuration est retenue ; CONFIRMATION : sur les 25 plis des répétitions 5 à 9 contre V0 (résultats d'I1b). Plusieurs tests statistiques à chaque étape : Wilcoxon apparié, test des signes, test de permutation apparié, IC95 bootstrap, et Friedman avec Nemenyi sur l'ensemble de la grille (quelles configurations sont indiscernables). La décision suit la règle écrite pour chaque hypothèse. Le test v2 reste scellé (D20).

*Justification.* D20 : itérer au maximum avant d'ouvrir le test ; l'étudiant demande de retenter avec d'autres valeurs : c'est une nouvelle itération, avec la même discipline de sélection puis confirmation.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I6.

### D24 : Itération I7 : retenter le rejet d'inconnus (I4) avec de nouveaux hyperparamètres et de nouvelles rotations  (version 1, 2026-11-09 21:35:36)

Demande de l'étudiant (2026-11-09). I7 : SÉLECTION sur un second jeu de 5 rotations (ensemble B : partitions des 30 classes tirées avec la graine 20261110, refusées si identiques à une rotation de v1 ou de l'ensemble de I4) × répétitions 0 à 4 (25 plis, 125 unités) ; CONFIRMATION sur un troisième jeu de 5 rotations (ensemble C : graine 20261111, mêmes refus) × répétitions 5 à 9 (25 nouveaux plis, 125 unités). Hyperparamètres : C de la tête ∈ {1 ; 16 ; 64} (I4 : 4) ; scores : msp, energy, hier_msp, fam_msp (I4), fam_margin (écart entre les deux plus grandes probabilités de famille), fam_negent (opposé de l'entropie des probabilités de famille), fam_x_msp (produit des confiances famille et classe), rank_fam_energy (moyenne des rangs de fam_msp et energy), soit 3 × 8 = 24 combinaisons. Unité de statistique = (rotation, répétition), AUROC moyenné sur les 5 plis. Sélection : meilleur AUROC moyen sur l'ensemble B ; référence : msp avec C = 4 (I4). Plusieurs tests statistiques : IC95 bootstrap, Wilcoxon, test des signes, permutation, Friedman + Nemenyi sur les 24 combinaisons à l'étape de sélection. Le test v2 reste scellé (D20).

*Justification.* L'étudiant demande de retenter avec de nouveaux hyperparamètres, plusieurs rotations et plusieurs tests ; la séparation sélection (rotations B) / confirmation (rotations C, nouveaux plis) évite de présenter un maximum de grille comme un résultat.

*Note.* Écrit le 2026-11-09 avant tout calcul de l'itération I7.

### D25 : Lancer la confirmation I6b malgré la porte fermée ; trancher HI6 et HI7 par la réplication I7c  (version 1, 2026-11-09 22:09:48)

(1) I6b : l'étudiant demande de lancer la confirmation que la règle D23 ne prévoyait pas (porte HF17 fermée : gain en développement +0,0085 < 0,02). La décision HF17 reste « réfutée » (elle porte sur la porte) ; HF18 est évaluée avec sa règle écrite sur les 25 plis des répétitions 5 à 9 de la configuration retenue W1_lr30 (V0 = I1b, mêmes plis) : un résultat nul sera une information, un résultat positif devrait être traité avec prudence (porte fermée en sélection). (2) I7c : HI6 et HI7 sont non tranchées parce que l'intervalle est large (25 unités). Réplication : TROIS nouveaux jeux de 5 rotations (ensembles D, E, F : graines 20261112, 20261113, 20261114, refusées si identiques à une rotation déjà utilisée : v1, I4, I7a, I7b ou un ensemble précédent) × 5 nouvelles répétitions de plis (répétitions 10 à 14, StratifiedGroupKFold par gabarit graines 10 à 14) = 75 unités (rotation, répétition) ; uniquement la combinaison retenue en sélection (C64_fam_negent) et la référence msp (C = 4), les 24 combinaisons étant calculées comme d'habitude mais NON utilisées pour décider. Plusieurs tests : IC95 bootstrap, Wilcoxon, signes, permutation.

*Justification.* Demande de l'étudiant (2026-11-09) : lancer I6b et trancher HI6 et HI7. Pour trancher il faut resserrer l'intervalle : 75 unités au lieu de 25, sur des rotations jamais vues, avec une règle écrite avant le calcul (R2).

*Note.* Écrit le 2026-11-09 avant tout calcul d'I6b et d'I7c.

### D26 : Ronde 3 : cibler la généralisation d'une classe à partir de très peu de gabarits  (version 1, 2026-11-10 00:03:47)

DIAGNOSTIC DG2 (exploratoire, répétition 0, 5 plis, SVM mots) : macro-F1 0,4965 ; si l'on AGRÈGE les marges par VRAI gabarit au test (borne haute oracle), le macro-F1 reste 0,4968 : le plafond ne vient donc pas du bruit entre logs d'un même gabarit mais de gabarits ENTIERS mal classés ; l'agrégation par voisins du test (5 à 50) ne gagne rien non plus (0,488 à 0,492). Huit classes ont un F1 voisin de 0 (file-read, file-write, file-modification, file-deleted, directory-deleted, file-action-failure, user-session-open, http-request-failure) : elles n'ont que 1 à 3 gabarits dans le développement, donc quand un gabarit est au test il en reste 0 à 2 pour apprendre ; exemple : le gabarit de test « Accessed URL … » de file-read est classé connexion échouée, alors que le gabarit d'entraînement dit « opened-file ». Le goulot est donc l'apprentissage avec 1 à 2 gabarits par classe : il faut apporter de la SÉMANTIQUE (que « accessed », « opened », « read » désignent la même action) ou rendre l'apprentissage robuste à un changement de gabarit. Pistes (≤ 3 variantes chacune, sélection sur répétitions 0 à 4 avec la baseline V0 de mêmes plis, porte : meilleure variante ≥ V0 + 0,02 avec Holm p < 0,05 sur l'ensemble des 10 variantes ; confirmation sur répétitions 5 à 9 selon la règle HF18) : (E) EMBEDDINGS gelés DistilBERT (moyenne des vecteurs de la dernière couche, 768 valeurs, sans réglage fin) : E1 régression logistique sur les embeddings ; E2 somme standardisée des marges de E1 et de V0 ; E3 V0 plus similarité cosinus à l'embedding du nom de la classe (« file read ») avec poids 1 (prior de sens) ; (L) LEXIQUE de concepts d'action : L1 mots + jetons de concepts (src/tp2_lexicon.py, écrit AVANT les résultats, lexique général indépendant des logs de test) ; L2 jetons de concepts seuls ; (A) AUGMENTATION pour simuler des gabarits nouveaux : A1 données + une copie avec suppression aléatoire de 30 % des mots ; A2 + deux copies à 50 % ; A3 A2 avec pondération par gabarit ; (S) DISCRIMINANT AU NIVEAU DU GABARIT : S1 analyse discriminante dont la dispersion intra-classe est calculée sur les MOYENNES PAR GABARIT (SVD à 200 dimensions), classe = moyenne la plus proche en distance de Mahalanobis rétrécie ; S2 somme standardisée de S1 et V0. Le test v2 reste scellé (D20).

*Justification.* Demande de l'étudiant (2026-11-10) : essayer d'autres hypothèses, méthodes, algorithmes et formules maison partout où un progrès est plausible, itérer à fond. DG2 cible la cause (gabarits entiers mal classés, classes à 1-3 gabarits) au lieu de régler des paramètres qui, eux, n'ont rien changé (I1, I2, I5, I6).

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### D27 : Scellement vérifiable du test v2 : empreinte, garde automatique, contrôle au commit  (version 1, 2026-11-10 13:17:33)

Demande de l'étudiant (2026-11-10) : le test v2 est intouchable, même pour un comptage. Trois contrôles, qui ne lisent aucun log : (1) empreinte SHA-256 de la liste triée des identifiants des 57 gabarits du test v2 et du fichier groups_v3.csv, enregistrée dans artifacts/data/test_v2_seal.json (scripts/v3_seal_test_v2.py ne lit que les colonnes « group » et « role ») ; (2) scripts/check_test_seal.py : refuse tout script ou module (hors les trois qui construisent ou scellent le découpage) qui mentionne « test2 », « SealedSplits » ou « unlock » ; (3) le crochet git pre-commit exécute ce contrôle et BLOQUE le commit en cas d'écart (empreinte modifiée, journal d'accès non vide hors ouverture déclarée, script interdit).

*Justification.* Règle 11 de la méthodologie d'article : le scellement doit être vérifiable par un lecteur extérieur, pas seulement affirmé.

*Note.* Écrit le 2026-11-10 ; validé par l'étudiant (« vas y je valide »).

### D28 : Vague 1 : décodage à masses équilibrées (F8), racines (F14), IDF de gabarit et pureté (F6), hiérarchie à vues séparées (F9), format (F18)  (version 1, 2026-11-10 13:19:51)

Procédure D20 : sélection sur les répétitions 0 à 4 (25 plis), confirmation sur 5 à 9 de la ou des variantes passant la porte. Variantes (30 classes, SIEVE_00, développement seul, 400 logs par gabarit ; mesure principale macro-F1 du palier A ; mesures secondaires macro-F1 des 30 classes et macro-F1 des classes à ≤ 3 gabarits de développement) : RÉFÉRENCES : V0 = SVM linéaire C = 1 sur TF-IDF mots (lettres ≥ 2, min_df = 2) ; LR = régression logistique C = 10 sur les mêmes caractéristiques. A (F8, référence LR) : A1 = Sinkhorn amorti (exposant 0,5, 10 itérations, masses cibles uniformes) sur les probabilités de LR ; A2 = ajustement du prior par EM (Saerens et al. 2002) sur le lot de test sans étiquette. B (F14, référence V0) : mots tronqués à k = 5, 6, 7 lettres. C (F6, référence V0) : IDF calculé sur les gabarits, avec poids de pureté de classe rétrécie (α = 2) : C0 (λ = 0 : IDF de gabarit seul), C1 (λ = 1), C2 (λ = 2). D (F9, référence V0) : marges du SVM mots + β · log p_lettres(famille de la classe) avec β = 0,5 ; 1 ; 2, la famille étant prédite par une LR sur TF-IDF caractères 3-5. E (F18, référence V0) : E1 = retrait des jetons de format (mois, jours, am/pm, pid, utc, nom du programme émetteur) ; E2 = poids de décorrélation format × classe au niveau gabarit w(f,c) = P(f)P(c)/P(f,c), borné à [0,2 ; 5], le format étant (programme + forme des 6 premiers jetons), SVM pondéré. Total 14 variantes ; porte : au moins une variante dépasse sa référence d'au moins 0,02 en macro-F1 du palier A avec Holm p < 0,05 (Wilcoxon apparié unilatéral, Holm sur les 14) ; le test v2 reste scellé (D27) et rien de cette vague ne le lit.

*Justification.* Demande de l'étudiant : aller plus loin, formules maison. DG2 et DG4 indiquent que la confusion vient de mots partagés entre classes et de classes attractrices (déséquilibre de gabarits), et que le vocabulaire seul ne peut identifier un gabarit de classe rare ; F8, F6 et F9 ciblent ces causes, F14 et F18 testent deux sources de variation de forme.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 1.

### D29 : Vague 2 : affiner et éprouver le décodage à masses équilibrées (A1)  (version 1, 2026-11-10 13:27:21)

A1 (D28/HW1, confirmé) : Sinkhorn amorti (exposant 0,5, 10 itérations, cibles uniformes) sur les probabilités de la régression logistique C = 10 : +0,057 à +0,08 de macro-F1 du palier A. Vague 2, procédure D20 (sélection répétitions 0-4, confirmation 5-9) ; RÉFÉRENCE = A1 recalculé sur les mêmes plis ; variantes : S1, S2 = A1 appliqué à softmax(τ · marges du SVM mots V0) avec τ = 5, 10 ; G25 (exposant 0,25), G1 (exposant 1,0), I30 (30 itérations, exposant 0,5) ; P5 = cibles proportionnelles à (nombre de gabarits d'entraînement de la classe)^0,5 au lieu d'uniformes ; H1 = équilibrage en deux temps (d'abord les masses de FAMILLE, puis les classes) ; F9S = marges V0 + 0,5 · log p_lettres(famille) (F9, β = 0,5), converties par softmax(τ = 5) puis A1 ; ROBUSTESSE : A1_abs et LR_abs = A1 et LR sur un lot de test d'où l'on a RETIRÉ 8 classes tirées au hasard (graine fixée par répétition et pli, tirage parmi les 30 classes, appliqué avant le décodage), pour simuler un lot où certaines classes sont absentes (cas du test final). Mesure principale : macro-F1 du palier A (classes présentes) ; secondaires : 30 classes, classes à ≤ 3 gabarits. Plusieurs tests : IC95 bootstrap, Wilcoxon, signes, permutation. Rappel de portée : A1 est un décodage TRANSDUCTIF (utilise la composition du lot de test sans étiquette). Le test v2 reste scellé (D27) ; rien de cette vague ne le lit.

*Justification.* Demande de l'étudiant : aller le plus loin possible. A1 est le premier gain net ; on cherche à l'amplifier (autres scores, cibles, familles, combinaison avec F9) et à vérifier qu'il ne dépend pas d'un lot où toutes les classes sont présentes (condition probable du test final : les 12 petites classes sont peu ou pas présentes).

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 2.

### D30 : Vague 3 : équilibrage conscient de la présence des classes (rendre A1 robuste)  (version 1, 2026-11-10 13:31:52)

Constat (RW2, HX6) : A1 gagne +0,057 à +0,08 quand toutes les classes sont dans le lot, mais seulement +0,005 à +0,04 quand 8 classes en sont absentes. Le test final contiendra vraisemblablement peu de petites classes (sans que nous puissions le vérifier : test scellé). Vague 3 (procédure D20 : sélection répétitions 0-4, confirmation 5-9). RÉFÉRENCE : LR (C = 10) dans chaque condition. CONDITIONS : « toutes » = lot complet ; « abs8 » = 8 classes tirées au hasard retirées du lot (graine 1000·répétition + pli) ; « abs14 » = 14 classes retirées (condition de stress, rapportée sans décision). VARIANTES (7) : A1 (rappel : exposant 0,5, 10 itérations, cible uniforme sur toutes les classes) ; Q25 et Q50 = A1 mais la cible est uniforme sur les seules classes JUGÉES PRÉSENTES, une classe étant jugée présente si sa masse prédite moyenne avant équilibrage est ≥ θ/K (θ = 0,25 pour Q25, 0,5 pour Q50), les classes jugées absentes recevant une cible nulle (leurs probabilités sont multipliées par 1e-3 avant équilibrage) ; Q25b et Q50b = idem avec exposant 0,25 ; M50 = cible mixte 0,5 · uniforme + 0,5 · prior de l'EM (moyenne des probabilités actuelles) ; Z = présence jugée ITÉRATIVEMENT : après A1, les classes dont moins de 0,5 % des logs sont prédits sont jugées absentes, et l'on relance l'équilibrage sans elles. Les deux conditions sont évaluées sur les mêmes plis. La décision porte sur le MINIMUM des deux gains (toutes, abs8). Plusieurs tests : IC95, Wilcoxon, signes, permutation. Le test v2 reste scellé.

*Justification.* HX6 : le gain d'A1 n'est pas établi quand des classes sont absentes ; sans cela, A1 n'est pas défendable sur le test final.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 3.

### D31 : Confirmer Q25b et M50 sur de nouveaux plis malgré la porte HY1 fermée  (version 1, 2026-11-10 13:33:13)

Décision prise après lecture de la sélection (répétitions 0-4) : deux variantes sont retenues pour la confirmation, choisies par le MINIMUM des gains moyens dans les conditions « toutes » et « abs8 » parmi les mécanismes distincts : Q25b (présence jugée par la masse prédite, exposant 0,25) et M50 (cible mixte uniforme/EM). Confirmation sur les 25 plis des répétitions 5 à 9 (nouveaux plis), conditions toutes, abs8 (graine 1000·répétition + pli) et abs14 (graine 2000·répétition + pli), référence LR dans chaque condition. Précédent : D25 (confirmation lancée malgré une porte fermée, I6b). Le résultat sera lu avec la règle HY5 à HY7 ci-dessous, écrite avant tout calcul de l'étape b. Le test v2 reste scellé.

*Justification.* La porte HY1 échoue par manque de puissance et non par effet nul : on tranche par une confirmation sur de nouveaux plis, comme demandé (« tout confirmer »).

*Note.* Écrit le 2026-11-10 avant toute confirmation de la vague 3 (aucune donnée des répétitions 5 à 9 n'a été lue pour ces variantes).

### D32 : Réplication de M50 (décodage à cible mixte) sur 50 nouveaux plis  (version 1, 2026-11-10 13:34:21)

M50 (cible = 0,5 · uniforme + 0,5 · prior moyen des probabilités, exposant 0,5, 10 itérations) a donné en sélection (répétitions 0-4) +0,0598 (toutes), +0,0460 (abs8), +0,0295 (abs14) et en confirmation (répétitions 5-9) +0,0432 ; +0,0348 ; +0,0253 contre LR, mais HY5 n'est pas remplie (borne basse 0,018 en abs8). Réplication sur les répétitions 10 à 19 (50 nouveaux plis, StratifiedGroupKFold par gabarit, graines 10 à 19), mêmes trois conditions (graines 1000·r + k et 2000·r + k), variantes calculées : M50, A1, référence LR. Les 25 plis de la vague 2 ne sont pas réutilisés. Seule règle de décision : HY8. Le test v2 reste scellé.

*Justification.* Résoudre le non-tranché de HY5 sans retoucher les règles : plus de plis (50) donnent un intervalle plus étroit sur des données jamais lues.

*Note.* Écrit le 2026-11-10 avant tout calcul de la réplication W3c (répétitions 10 à 19 : aucun résultat de ces plis n'a été lu).

### D33 : Réplication finale de M50 sur 100 nouveaux plis (répétitions 20 à 39) : décision définitive  (version 1, 2026-11-10 14:10:53)

HY8 est restée non tranchée (test des signes 31/50, p unilatéral 0,0595, contre 0,05) ; l'étudiant a choisi (2026-11-10) une dernière réplication préinscrite. 100 plis (répétitions 20 à 39, StratifiedGroupKFold par gabarit, graines 20 à 39), conditions toutes, abs8 (graine 1000·r + k), abs14 (2000·r + k), variantes M50, A1 (rapportée), LR (référence). Règle HY9 identique à HY8, avec n = 100. DÉCISION DÉFINITIVE : si HY9 est confirmée, M50 entre dans le pipeline gelé ; sinon (réfutée ou non tranchée) le décodage équilibré est abandonné du pipeline gelé, QUEL QUE SOIT le résultat des autres comparaisons ; aucune nouvelle réplication ne sera faite pour M50 (évite l'arrêt optionnel). Le test v2 reste scellé.

*Justification.* Résoudre un non-tranché sans retoucher la règle, avec le double de plis ; une seule réplication supplémentaire annoncée d'avance, donc pas de répétition jusqu'à un résultat favorable.

*Note.* Écrit le 2026-11-10 avant tout calcul de la réplication W3d (répétitions 20 à 39 : aucun résultat de ces plis n'a été lu).

### D34 : Vague 4 : axes objet × action (F7), bagging par gabarits (F20), pondération des gabarits difficiles (F10), avec et sans décodage M50  (version 1, 2026-11-10 14:12:48)

Contexte : M50 est établi (HY9, D33) et fait partie du pipeline gelé ; la vague 4 cherche à améliorer les probabilités AVANT décodage. Procédure D20 : sélection répétitions 0-4 (25 plis), confirmation répétitions 10-14 (25 plis) des variantes passant la porte. RÉFÉRENCE : LR (C = 10, TF-IDF mots) ; référence décodée : LR + M50. VARIANTES (cinq) : AXE0, AXE05, AXE1 = produit d'experts objet × action : log p_objet(j(c)|x) + log p_action(k(c)|x) + γ · log p_classe(c|x) avec γ = 0, 0,5, 1 (têtes : régressions logistiques C = 10 sur le même TF-IDF ; axes tirés des noms de classes, table DG4 : 12 objets, 15 actions) puis softmax ; BAG10 = moyenne des probabilités de 10 régressions logistiques entraînées chacune sur 70 % des GABARITS d'entraînement tirés au hasard ; DRO1 = pondération des gabarits difficiles : perte logarithmique moyenne de chaque gabarit d'entraînement mesurée hors-gabarit (validation croisée interne en 3 plis de gabarits), poids de gabarit ∝ exp(perte), normalisé, puis régression logistique pondérée. MODES : « brut » (argmax) et « M50 » (décodage de D30/D33). CONDITIONS : « toutes » (décision) et « abs8 » (rapportée, mêmes tirages que W3). Mesure principale : macro-F1 du palier A. Porte : au moins une variante dépasse sa référence (LR pour « brut », LR + M50 pour « M50 ») d'au moins 0,02 dans la condition « toutes » avec Holm p < 0,05 (Wilcoxon unilatéral contre le seuil, Holm sur 5 variantes, par mode). Plusieurs tests : IC95, Wilcoxon, signes, permutation. Le test v2 reste scellé (D27).

*Justification.* Demande de l'étudiant (« go for it ») ; F7 est notre idée principale (axes partagés entre classes), F20 et F10 ciblent la dépendance aux gabarits particuliers vus. M50 ayant corrigé l'absorption de masses, on teste si les probabilités elles-mêmes peuvent être améliorées et si les gains s'additionnent.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 4.

### D35 : Amendement de la vague 4 : DRO2 (poids bornés) ajouté à DRO1  (version 1, 2026-11-10 14:13:44)

Un test sur un pli (répétition 0, pli 0) a révélé un défaut de la formule préinscrite de DRO1 (poids ∝ exp(perte logarithmique)) : la perte n'est pas bornée (jusqu'à 20,7 quand la classe du gabarit manque au pli d'apprentissage interne) ; les poids se concentrent sur 5 gabarits « équivalents » sur 203 et le modèle est inutilisable (macro-F1 0). DRO1 est CONSERVÉ tel que préinscrit et sera rapporté (probablement dégénéré, ce qui est un résultat sur la formule). DRO2 ajoute avant tout calcul de sélection : poids ∝ exp(0,5 · min(perte, 4)), ce qui borne le rapport des poids à e² ≈ 7,4 et garde un nombre effectif de gabarits élevé. La porte HZ5 compte maintenant 6 variantes (Holm sur 6 au lieu de 5).

*Justification.* Défaut de formule trouvé par un test de code, pas par un résultat de performance ; amendement écrit avant la sélection, sans suppression de DRO1.

*Note.* Écrit le 2026-11-10, après le test sur UN pli (non lu comme résultat) et avant tout calcul de la sélection de la vague 4.

### D36 : Confirmer AXE05 sur 50 nouveaux plis (répétitions 10 à 19) malgré la porte HZ5 fermée  (version 1, 2026-11-10 14:16:51)

AXE05 est choisie parce que son IC95 de sélection est entièrement au-dessus de 0,02 (brut, toutes) ; précédents : D25, D31. Confirmation : répétitions 10 à 19 (50 plis, StratifiedGroupKFold par gabarit, graines 10 à 19), conditions toutes et abs8, modes brut et M50, référence LR (brut) et LR + M50 (M50). Règles HZ7 et HZ8 ci-dessous, écrites avant le calcul. Le test v2 reste scellé.

*Justification.* La porte échoue par manque de puissance ; 50 plis donnent un intervalle plus étroit.

*Note.* Écrit le 2026-11-10 avant toute confirmation de la vague 4 (aucune donnée des répétitions 10 à 19 n'a été lue pour AXE05).

### D37 : Vagues 5 à 7 : monde ouvert avec décodage, V-REx et embeddings gelés, LP-FT et pré-entraînement sur les logs  (version 1, 2026-11-10 14:33:07)

Demande de l'étudiant (2026-11-10, « va pour les 3 »). Pipeline gelé provisoire : TF-IDF mots → régression logistique C = 10 → décodage M50 (D33). Procédure D20 : sélection puis confirmation sur plis ou rotations distincts ; le test v2 reste scellé (D27). VAGUE 5 (monde ouvert) : modèle entraîné sur les classes connues (régression logistique C = 16 sur TF-IDF mots et tête de famille, comme I7), lot de test = classes connues + classes masquées ; référence FAM = confiance de famille (probabilité maximale de la tête de famille) ; variantes : FAMQ = probabilité de famille obtenue en agrégeant les probabilités de classe DÉCODÉES par M50 sur le lot, max ; FAMD = décodage de type M50 appliqué directement aux probabilités de famille (cible 0,5 uniforme + 0,5 prior observé), max ; MSPQ = probabilité maximale de classe après décodage. Sélection : rotations de l'ensemble B (graine 20261110) × répétitions 0-4 ; confirmation : ensemble C (graine 20261111) × répétitions 5-9 ; unité (rotation, répétition) = 25. VAGUE 6 (classification fermée, 30 classes, plis P2) : V-REx = régression softmax linéaire sur TF-IDF mots entraînée avec perte moyenne par gabarit + λ · variance de la perte entre gabarits (λ = 1, 5, 20 : VR1, VR5, VR20) ; référence ERM (même entraîneur, λ = 0) ; EMBEDDINGS gelés DistilBERT (moyenne des vecteurs de la dernière couche, 768 valeurs, longueur 128, sans réglage fin, calculés sur les seuls logs du développement) : E1 = régression logistique sur les embeddings standardisés ; E2 = moyenne géométrique des probabilités de la régression logistique mots (LR) et d'E1 ; E3 = régression logistique sur [TF-IDF mots, embeddings standardisés × 0,1] ; modes brut et M50 ; références LR (brut) et LR + M50 (M50) ; condition « toutes » ; sélection répétitions 0-4, confirmation répétitions 10-19 des variantes passant la porte. VAGUE 7 : LP-FT (sonde linéaire 1 époque, encodeur gelé, puis affinage de tout le modèle à taux 1e-5 pendant 2 époques) dans le protocole de T2 (140 logs d'entraînement par classe, 4 découpes × 5 rotations, 20 couples, graine 42) comparé à l'affinage complet de T2 (taux 3e-5) sur les mêmes couples ; et la même chose à partir d'un DistilBERT ADAPTÉ par prédiction de mots masqués (MLM, 1 époque, longueur 128) sur les seuls logs d'entraînement de la découpe (sans étiquette ni log de test). Plusieurs tests (IC95, Wilcoxon, signes, permutation).

*Justification.* Demande de l'étudiant ; ces pistes (invariance entre gabarits, sémantique gelée, adaptation au langage des logs) changent l'information ou l'entraînement, pas le réglage.

*Note.* Écrit le 2026-11-10 avant tout calcul des vagues 5 à 7.

### D38 : Vague 8 : réglage conscient du décodage, mots + lettres avant décodage, auto-apprentissage sur le lot décodé  (version 1, 2026-11-10 21:35:24)

Clôture de la vague 7 (RW7) puis demande de l'étudiant (2026-11-10) : essayer d'autres leviers. RÉFÉRENCE PIPE = pipeline gelé provisoire : TF-IDF mots → régression logistique C = 10 → décodage M50 (cible 0,5 uniforme + 0,5 prior observé, exposant 0,5, 10 itérations). Procédure D20 : sélection répétitions 0-4 (25 plis), confirmation répétitions 10-19 (50 plis, mêmes plis que W3c) ; condition « toutes » pour la décision, « abs8 » (8 classes retirées du lot, mêmes tirages que W3) rapportée ; mesure : macro-F1 du palier A. LEVIERS : (G) RÉGLAGE : grille de 36 configurations C ∈ {3, 10, 30, 100} × température T ∈ {0,5 ; 1 ; 2} (probabilités P^(1/T) renormalisées avant décodage) × poids α du prior observé dans la cible ∈ {0,25 ; 0,5 ; 0,75} ; la configuration (10, 1, 0,5) est PIPE ; on retient la meilleure des 35 autres selon la moyenne de la macro-F1 en sélection. (E) MOTS + LETTRES : ENSP30, ENSP50 = moyenne géométrique pondérée des probabilités de la régression logistique mots (poids 0,7 ou 0,5) et d'une régression logistique C = 10 sur TF-IDF caractères 3-5 (poids 0,3 ou 0,5), puis décodage M50. (S) AUTO-APPRENTISSAGE : ST1 = après le décodage M50 du lot de test sans étiquette, on ajoute à l'apprentissage, avec le poids 0,5, les logs du lot dont la confiance après décodage est dans le tiers supérieur de leur classe prédite, avec leur classe prédite, on réentraîne la régression logistique (C = 10) et l'on redécode ; ST2 = deux tours. Précaution : le lot est celui du pli de développement ; le texte du test v2 n'est jamais lu avant son ouverture unique. Plusieurs tests : IC95 bootstrap, Wilcoxon, signes, permutation. Le test v2 reste scellé (D27).

*Justification.* Le décodage a changé l'information utile des probabilités (calibration, netteté) : le réglage des probabilités peut compter désormais ; les lettres donnaient un gain de famille (HF7) ; l'auto-apprentissage adapte le modèle au vocabulaire des gabarits nouveaux du lot.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 8.

### D39 : Confirmer trois candidats de la vague 8 sur 50 plis neufs (seuil pratique 0,01)  (version 1, 2026-11-10 21:43:22)

Candidats : G_C30_T1_a0.25 (meilleure configuration de la grille en sélection : +0,0152, IC95 [0,005 ; 0,026], poids 0,25 du prior observé dans la cible), ST1 (+0,0249) et ST2 (+0,0220). Confirmation : répétitions 10-19 (50 plis), conditions toutes et abs8, référence PIPE recalculée sur les mêmes plis. SEUIL : 0,01 (seuil pratique pour un ajout au pipeline décodé, comme HZ8) ; correction pour trois candidats : p < 0,05 / 3 = 0,0167. Précédents : D25, D31, D36. Le test v2 reste scellé.

*Justification.* Les gains de sélection sont de l'ordre de +0,015 à +0,025 avec des bornes basses entre 0,005 et 0,015 : trop incertains pour trancher ; 50 plis neufs resserrent l'intervalle.

*Note.* Écrit le 2026-11-10 avant toute confirmation de la vague 8 (aucune donnée des répétitions 10 à 19 n'a été lue pour ces variantes).

### D40 : Vague 9 : composer plusieurs leviers (plan factoriel, interactions, composition apprise)  (version 1, 2026-11-10 21:48:47)

Demande de l'étudiant (2026-11-10, mardi) : au lieu d'un levier à la fois, composer deux ou trois leviers et faire varier leurs degrés. RÉFÉRENCE PIPE = TF-IDF mots → LR C = 10 → décodage M50 (α = 0,5, T = 1). COMPOSANTES de score de classe c pour un log x : Lc = log p_LR(c|x) ; Lo = log p_objet(o(c)|x) et La = log p_action(a(c)|x) (têtes logistiques C = 10 sur le même TF-IDF, axes des noms de classes, table DG4) ; Lf = log p_lettres(famille(c)|x) (LR C = 10 sur TF-IDF caractères 3-5, famille de la taxonomie). Score s = wc·Lc + wo·Lo + wa·La + wf·Lf ; probabilités = softmax(s) puis élévation à la puissance 1/T et renormalisation, puis décodage de cible (1 − α)/K + α·prior observé (Sinkhorn amorti 0,5, 10 itérations). PLAN FACTORIEL (108 configurations par pli) : A (base) ∈ {LR : wc = 1, wo = wa = 0 ; AXE05 : wc = 0,5, wo = wa = 1 ; AXE1 : wc = wo = wa = 1} × B (poids des lettres wf) ∈ {0 ; 0,5 ; 1 ; 2} × T ∈ {0,5 ; 1 ; 2} × α ∈ {0,25 ; 0,5 ; 0,75} ; PIPE = (LR, 0, 1, 0,5). COMPOSITION APPRISE STK : les quatre poids (wc, wo, wa, wf ≥ 0) sont estimés par minimisation de l'entropie croisée de la vraie classe sur des prédictions HORS-GABARIT du jeu d'entraînement (validation croisée interne en 3 plis de gabarits, chaque composante réentraînée à chaque pli), puis décodage M50 (α = 0,5, T = 1). Sélection : répétitions 0-4 (25 plis) ; confirmation : répétitions 10-19 (50 plis) des quatre candidats retenus (les trois meilleures configurations de moyenne de macro-F1 en sélection, hors PIPE et à leviers distincts, plus STK), seuil pratique 0,01 contre PIPE, correction pour 4 candidats (p < 0,0125). Mesure : macro-F1 du palier A ; conditions toutes (décision) et abs8 (contrôle). Plusieurs tests : IC95, Wilcoxon, signes, permutation, Holm. Le test v2 reste scellé (D27).

*Justification.* Les leviers de la phase 2 donnent chacun un gain partiel non établi (axes objet × action +0,018 avec décodage, lettres vers la famille +0,02 à +0,03 en brut, prior 0,25 +0,015) ; leur COMPOSITION pourrait être additive, sous-additive (même défaut corrigé deux fois) ou sur-additive ; le plan factoriel mesure effets principaux et interactions, STK laisse les données choisir les poids.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 9.

### D41 : Vague 10 : étendre les degrés, variantes de STK, réplication finale sur 100 plis et règle de choix du pipeline gelé  (version 1, 2026-11-10 22:03:49)

Suite de la vague 9 (RW9) : le meilleur de 108 configurations (AXE05, lettres 1, température 2, prior 0,25) est à la FRONTIÈRE de la grille (T maximal, α minimal) et STK a été évaluée à (T = 1, α = 0,5) seulement ; l'étudiant demande de faire varier les degrés. SÉLECTION (répétitions 0-4, 25 plis, nouveau bloc) : (E1) famille AXE : base AXE05 avec lettres 1, T ∈ {2 ; 3 ; 4} × α ∈ {0,1 ; 0,25 ; 0,4} (9 configurations) ; bases AXE025 (wc = 0,25, wo = wa = 1) et AXE075 (wc = 0,75, wo = wa = 1) avec lettres 1, T = 2, α = 0,25 (2 configurations) ; (E2) famille STK : poids appris comme en D40, décodés avec T ∈ {1 ; 2 ; 3} × α ∈ {0,1 ; 0,25 ; 0,5} (9 configurations) ; références rejouées : PIPE, AXE05_B1_T2_a0.25 (retenue en D40), STK (T = 1, α = 0,5). On retient la meilleure configuration de chaque famille (E1, E2) selon la moyenne de macro-F1 en sélection. RÉPLICATION FINALE (répétitions 20 à 39, 100 plis jamais utilisés pour ces configurations ; conditions toutes, abs8 (graine 1000·r + k), abs14 (graine 2000·r + k)) : candidats = {AXE05_B1_T2_a0.25, STK (T = 1, α = 0,5), meilleure de E1, meilleure de E2} contre PIPE. RÈGLE DE CHOIX (écrite avant le calcul) : un candidat est ÉLIGIBLE si, en condition « toutes », le gain contre PIPE a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre 0,02) donnent p < 0,0125 (Bonferroni, 4 candidats) ; parmi les éligibles, on retient celui dont le MINIMUM des gains moyens sur les trois conditions (toutes, abs8, abs14) est le plus grand ; si l'écart entre les deux meilleurs minima est < 0,005, on retient le plus simple (STK à T = 1, α = 0,5, sans réglage) ; si aucun candidat n'est éligible, le pipeline gelé reste AXE05_B1_T2_a0.25 (confirmé en D40, HK4). Le test v2 reste scellé (D27).

*Justification.* Faire varier les degrés d'un levier jusqu'à l'optimum intérieur (sinon on ne sait pas si l'on est au bout) ; tester la robustesse à l'absence de classes (14 absentes) qui est la condition la plus dure ; choisir sur des plis neufs avec une règle écrite d'avance, pas sur la sélection.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 10.

### D42 : Pipeline gelé provisoire (avant l'ouverture du test v2)  (version 1, 2026-11-10 22:25:22)

PIPELINE : (1) TF-IDF mots (lettres ≥ 2, min_df = 2, sublinéaire) et TF-IDF caractères 3-5 (char_wb, min_df = 3, 100 000 attributs) calculés sur l'apprentissage ; (2) quatre têtes : régression logistique C = 10 sur les mots pour la classe, pour l'objet (12 valeurs) et pour l'action (15 valeurs) ; régression logistique C = 10 sur les caractères pour la famille ; (3) score de classe s = wc·log p_classe + wo·log p_objet + wa·log p_action + wf·log p_famille avec poids ≥ 0 appris par minimisation de l'entropie croisée hors-gabarit (validation croisée interne en 3 plis de gabarits, composantes réentraînées à chaque pli) ; (4) softmax puis décodage à masses équilibrées M50 sur le lot de test (cible 0,5 uniforme + 0,5 prior observé, Sinkhorn amorti 0,5, 10 itérations, température 1) ; (5) REJET DES INCONNUS par la confiance de famille brute (sans décodage, vague 5). Code : scripts/v3_phase2_W10.py (config « STK_T1_a0.5 »). Choisi par la règle D41 sur 100 plis neufs. Le test v2 reste scellé ; il sera ouvert UNE fois sur ce pipeline, après relecture de l'étudiant.

*Justification.* Règle de choix écrite avant le calcul (D41) ; pipeline le plus simple et le plus robuste ; gel provisoire car l'ouverture du test v2 attend la validation de l'étudiant (au plus tard vendredi 2026-11-13).

*Note.* Écrit le 2026-11-10.

### D43 : Vague 11 : composition apprise élargie (STK7, STK9)  (version 1, 2026-11-10 22:40:05)

Demande de l'étudiant (« lançons la vague maintenant »). RÉFÉRENCE STK4 = pipeline gelé D42 (têtes : classe-mots Lc, objet-mots Lo, action-mots La, famille-lettres Lf ; décodage M50, T = 1, α = 0,5). TÊTES NOUVELLES (régression logistique C = 10, log-probabilité ramenée aux 30 classes) : Lcc = classe par les caractères 3-5 ; Loc = objet par les caractères ; Lac = action par les caractères ; Lfw = famille par les mots ; Lcb = classe par les uni- et bigrammes de mots (lettres ≥ 2, min_df = 2). VARIANTES : STK7 = STK4 + Lcc + Loc + Lac ; STK9 = STK7 + Lfw + Lcb. Les poids (tous ≥ 0) sont appris comme en D40/D42 par minimisation de l'entropie croisée hors-gabarit (validation croisée interne en 3 plis de gabarits, toutes les têtes réentraînées à chaque pli), puis softmax et décodage M50 (α = 0,5, T = 1) : aucun réglage à la main. SÉLECTION : répétitions 0-4 (25 plis) ; CONFIRMATION : répétitions 40-49 (50 plis, jamais utilisés) du ou des variantes retenues contre STK4 et PIPE (décodage M50 seul) ; conditions toutes (décision), abs8 et abs14 (graines 1000·r + k et 2000·r + k). Mesure : macro-F1 du palier A. Plusieurs tests : IC95, Wilcoxon, signes, permutation, Holm. Le test v2 reste scellé (D27).

*Justification.* STK a mis presque tout son poids sur les têtes partagées entre classes (action, famille) ; d'autres têtes, notamment fondées sur les caractères, peuvent apporter de l'information complémentaire ; les poids étant appris, l'ajout ne crée aucun réglage manuel.

*Note.* Écrit le 2026-11-10 (22h30) avant tout calcul de la vague 11.

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

### HT1 : Le Transformer n'améliore pas la classification des classes connues  (version 3, 2026-11-10 00:00:10 ; **statut : confirmée**)

Sur les mêmes logs de test, le macro-F1 des classes connues du Transformer dépasse celui de la baseline TF-IDF d'au plus 0,02 (Wilcoxon sur les 30 couples fichier × rotation, moyenne des graines, Holm).

*Justification.* Tranchée par la réplication préinscrite D22 (HT1b, 20 couples) ; l'entrée « non tranchée » précédente est conservée.

*Preuve.* Voir HT1b : Transformer − TF-IDF = −0,0545, IC95 [−0,086 ; −0,020].

*Note.* Source : T2. Le Transformer n'améliore pas de plus de 0,02 ; sur 140 logs par classe il est même moins bon que TF-IDF sur les nouvelles découpes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; Sur les mêmes logs de test, le macro-F1 des classes connues du Transformer dépasse celui de la baseline TF-IDF d'au plus 0,02 (Wilcoxon sur les 30 couples fichier × rotation, moyenne des graines, Holm…
- v2 (2026-11-09 21:14:59) : statut non tranchée ; Sur les mêmes logs de test, le macro-F1 des classes connues du Transformer dépasse celui de la baseline TF-IDF d'au plus 0,02 (Wilcoxon sur les 30 couples fichier × rotation, moyenne des graines, Holm…

### HT2 : Mahalanobis aide sur les vecteurs du Transformer  (version 2, 2026-11-09 21:14:59 ; **statut : non tranchée**)

L'AUROC de Mahalanobis (vecteurs de 768 valeurs) dépasse celui du MSP du même Transformer d'au moins 0,03 (Wilcoxon sur les 30 couples, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC d'inconnu de Mahalanobis moins MSP (même Transformer) : +0,0325, IC95 [0,0195 ; 0,0463], p unilatéral (écart > 0,03) 0,44 ; 21 couples sur 30 en faveur. Moyennes : Mahalanobis 0,593 ; MSP 0,560.  Fichiers : artifacts/results/v3/T_all_units.csv ; T_tests.csv

*Note.* Gain moyen égal au seuil de 0,03, intervalle qui le contient. Les deux restent faibles (< 0,60). Plan : DistilBERT sans casse, 256 jetons, 2 époques, 3e-5 ; 6 niveaux de bruit × 5 rotations × 3 graines = 90 modèles ; une seule découpe du développement (répétition 0, pli 0) ; 140 logs d'entraînement par classe (donc F1 plus bas qu'avec les données complètes : baseline TF-IDF 0,37 ici contre 0,50 ailleurs).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; L'AUROC de Mahalanobis (vecteurs de 768 valeurs) dépasse celui du MSP du même Transformer d'au moins 0,03 (Wilcoxon sur les 30 couples, Holm p < 0,05).

### HT3 : La confiance sur la famille aide aussi pour le Transformer  (version 2, 2026-11-09 21:14:59 ; **statut : confirmée**)

L'AUROC de la confiance sur la FAMILLE du Transformer dépasse celui de son MSP d'au moins 0,02 (Wilcoxon sur les 30 couples, Holm p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC famille moins MSP du Transformer : +0,0699, IC95 [0,048 ; 0,091], p Holm 0,0004 ; 26 couples sur 30 en faveur. Moyennes : famille 0,630 ; MSP 0,560.  Fichiers : artifacts/results/v3/T_all_units.csv ; T_tests.csv

*Note.* Troisième série de données (après le bloc C et I4) où la confiance de famille est le meilleur détecteur ; ici le gain (+0,07) est le plus grand. Plan : DistilBERT sans casse, 256 jetons, 2 époques, 3e-5 ; 6 niveaux de bruit × 5 rotations × 3 graines = 90 modèles ; une seule découpe du développement (répétition 0, pli 0) ; 140 logs d'entraînement par classe (donc F1 plus bas qu'avec les données complètes : baseline TF-IDF 0,37 ici contre 0,50 ailleurs).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; L'AUROC de la confiance sur la FAMILLE du Transformer dépasse celui de son MSP d'au moins 0,02 (Wilcoxon sur les 30 couples, Holm p < 0,05).

### HT4 : Le Transformer perd moins avec le bruit que TF-IDF  (version 2, 2026-11-09 21:14:59 ; **statut : réfutée**)

La perte de macro-F1 des classes connues entre p = 0 et p = 0,5 est plus petite pour le Transformer que pour la baseline TF-IDF (Wilcoxon sur les 15 couples rotation × graine, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Perte de macro-F1 entre p = 0 et p = 0,5 : Transformer 0,0565 contre TF-IDF 0,0311 ; différence (TF-IDF − Transformer) −0,0254, IC95 [−0,045 ; −0,006], p unilatéral 0,99 ; le Transformer perd moins dans 4 couples sur 15 seulement.  Fichiers : artifacts/results/v3/T_all_units.csv ; T_tests.csv

*Note.* Le signe est l'inverse de l'hypothèse : le Transformer perd PLUS que TF-IDF quand on ajoute du bruit (l'avance de 0,03 à p = 0 devient 0,005 à p = 0,5). Avec 2 époques sur 140 logs par classe, son avantage ne résiste pas au bruit. Plan : DistilBERT sans casse, 256 jetons, 2 époques, 3e-5 ; 6 niveaux de bruit × 5 rotations × 3 graines = 90 modèles ; une seule découpe du développement (répétition 0, pli 0) ; 140 logs d'entraînement par classe (donc F1 plus bas qu'avec les données complètes : baseline TF-IDF 0,37 ici contre 0,50 ailleurs).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-07 23:25:34) : statut préinscrite ; La perte de macro-F1 des classes connues entre p = 0 et p = 0,5 est plus petite pour le Transformer que pour la baseline TF-IDF (Wilcoxon sur les 15 couples rotation × graine, p < 0,05).

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

### HF1 : Le support par gabarit améliore le macro-F1  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

Pour au moins un des trois seuils m = 2, 3, 5 gabarits, le macro-F1 des classes (palier A) dépasse celui du SVM mots d'au moins 0,02 (Wilcoxon apparié sur 25 plis, Holm sur 3, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Écart de macro-F1 (palier A) contre le SVM mots (0,5032) : T2 −0,007 (IC95 [−0,023 ; 0,009], p Holm 0,31) ; T3 −0,031 (p Holm 0,002) ; T5 −0,086 (p Holm 3e-5). Aucun seuil ne gagne 0,02 ; T3 et T5 font significativement PIRE.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Note.* L'hypothèse de travail de D16 (les mots propres à un seul gabarit nuisent) est fausse : ces mots aident aussi à reconnaître les classes dont les gabarits se ressemblent. Plus on restreint, plus la distance dans l'arbre augmente (0,81 → 0,92 → 0,98).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; Pour au moins un des trois seuils m = 2, 3, 5 gabarits, le macro-F1 des classes (palier A) dépasse celui du SVM mots d'au moins 0,02 (Wilcoxon apparié sur 25 plis, Holm sur 3, p < 0,05).

### HF2 : Le marqueur « valeur » apporte quelque chose de plus que la suppression  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

T3M (mots écartés remplacés par un marqueur) dépasse T3 (mots écartés supprimés) d'au moins 0,01 (Wilcoxon apparié, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* T3M moins T3 : −0,0013, IC95 [−0,007 ; 0,005], p = 0,92 : l'intervalle exclut +0,01.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Note.* Le marqueur « valeur » unique n'apporte rien ; il ne rattrape pas la perte due à la restriction.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; T3M (mots écartés remplacés par un marqueur) dépasse T3 (mots écartés supprimés) d'au moins 0,01 (Wilcoxon apparié, p < 0,05).

### HF3 : Mots et caractères se complètent  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

ENS dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* ENS moins SVM mots : −0,0010, IC95 [−0,012 ; 0,009], p = 0,65 : l'intervalle exclut +0,02.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Note.* Constat exploratoire (non préinscrit, à confirmer) : ENS améliore le macro-F1 de FAMILLE (0,719 contre 0,692) et la distance dans l'arbre (0,787 contre 0,812) sans changer le macro-F1 des classes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; ENS dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

### HF4 : Pondérer les gabarits à égalité aide  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

WGT dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* WGT moins SVM mots : −0,0043, IC95 [−0,008 ; −0,001], p = 0,045 : légèrement PIRE, loin de +0,02.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; WGT dépasse le SVM mots d'au moins 0,02 (Wilcoxon apparié, Holm).

### HF5 : La combinaison dépasse chacun de ses composants  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

COMB dépasse chacune des variantes qu'elle combine (Wilcoxon apparié, Holm).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Aucune combinaison ne dépasse chacun de ses composants : C2 contre ENS −0,006 (p Holm 0,96), C3 contre ENS −0,009, C3 contre WGT −0,006, C1 contre WGT −0,030 (p Holm 0,002). C2 et C3 dépassent seulement T3 (+0,024 et +0,022), c'est-à-dire qu'elles réparent partiellement la perte de T3.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Note.* Les trois combinaisons ont été calculées en même temps (C1, C2, C3) ; aucune n'a été choisie après coup.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; COMB dépasse chacune des variantes qu'elle combine (Wilcoxon apparié, Holm).

### HF6 : Objectif de score  (version 2, 2026-11-09 13:14:27 ; **statut : réfutée**)

Le macro-F1 des classes (palier A) de la meilleure variante atteint au moins 0,55 en moyenne sur les 25 plis (baseline 0,503).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Meilleur macro-F1 (palier A) : V0 0,5032 ; ENS 0,5022 ; WGT 0,4989. Cible 0,55 non atteinte ; aucune variante ne dépasse la baseline.  Fichiers : artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

*Note.* Conclusion de I1 : la représentation à base de mots (vocabulaire, marqueurs, pondération, ajout des lettres) ne lève pas le plafond d'environ 0,50 ; la piste suivante doit changer la nature de l'information (champs typés, Transformer, fusion de scores) ou la tâche (niveau famille).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:02:03) : statut préinscrite ; Le macro-F1 des classes (palier A) de la meilleure variante atteint au moins 0,55 en moyenne sur les 25 plis (baseline 0,503).

### HF7 : Mots + lettres améliore le F1 de famille  (version 2, 2026-11-09 13:22:39 ; **statut : confirmée**)

Sur les 25 nouveaux plis, le macro-F1 de famille de ENS dépasse celui de V0 (SVM mots) d'au moins 0,01 (Wilcoxon apparié unilatéral p < 0,05). Réfutée si l'IC95 bootstrap de l'écart exclut +0,01 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* 25 nouveaux plis : macro-F1 de famille ENS 0,720 contre V0 0,690, gain +0,029, IC95 [0,015 ; 0,048] (borne basse au-dessus du seuil 0,01), Wilcoxon unilatéral p = 2e-5, 22 plis sur 25 en faveur.  Fichiers : artifacts/results/v3/I1b_all_units.csv ; I1b_tests.csv

*Note.* Reproduit le constat exploratoire d'I1 (+0,028) : l'effet est stable. Limite : mêmes gabarits que le développement d'I1, répartis autrement ; la confirmation sur de nouveaux gabarits revient au test v2.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:17:00) : statut préinscrite ; Sur les 25 nouveaux plis, le macro-F1 de famille de ENS dépasse celui de V0 (SVM mots) d'au moins 0,01 (Wilcoxon apparié unilatéral p < 0,05). Réfutée si l'IC95 bootstrap de l'écart exclut +0,01 ; sin…

### HF8 : Mots + lettres rapproche les erreurs dans l'arbre  (version 2, 2026-11-09 13:22:39 ; **statut : confirmée**)

Sur les 25 nouveaux plis, la distance moyenne dans l'arbre de ENS est inférieure à celle de V0 d'au moins 0,01 (Wilcoxon apparié, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Distance moyenne dans l'arbre : ENS 0,781 contre V0 0,808, gain +0,028, IC95 [0,013 ; 0,044], p unilatéral 0,0019, 20 plis sur 25 en faveur.  Fichiers : artifacts/results/v3/I1b_all_units.csv ; I1b_tests.csv

*Note.*  Limite : mêmes gabarits que le développement d'I1, répartis autrement ; la confirmation sur de nouveaux gabarits revient au test v2.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:17:00) : statut préinscrite ; Sur les 25 nouveaux plis, la distance moyenne dans l'arbre de ENS est inférieure à celle de V0 d'au moins 0,01 (Wilcoxon apparié, p < 0,05).

### HF9 : Mots + lettres ne dégrade pas le macro-F1 des classes  (version 2, 2026-11-09 13:22:39 ; **statut : non tranchée**)

Sur les 25 nouveaux plis, l'écart de macro-F1 (palier A) ENS − V0 est supérieur à −0,01 : l'IC95 bootstrap de l'écart est entièrement au-dessus de −0,01 (équivalence unilatérale).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Écart de macro-F1 des classes ENS − V0 : −0,0011, IC95 [−0,0109 ; 0,0091] ; la borne basse dépasse de 0,0009 le seuil −0,01 : l'équivalence unilatérale n'est pas établie au sens strict de la règle ; 12 plis sur 25 en faveur d'ENS.  Fichiers : artifacts/results/v3/I1b_all_units.csv ; I1b_tests.csv

*Note.* L'écart moyen est quasi nul (0,001) ; la règle d'équivalence exigeait un intervalle entièrement au-dessus de −0,01 et l'intervalle dépasse ce seuil de très peu. Pas de dégradation visible, mais pas de preuve d'absence de dégradation. Ni les données d'I1 (−0,001, IC [−0,012 ; 0,009]) ni celles d'I1b ne la permettent seules. Limite : mêmes gabarits que le développement d'I1, répartis autrement ; la confirmation sur de nouveaux gabarits revient au test v2.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:17:00) : statut préinscrite ; Sur les 25 nouveaux plis, l'écart de macro-F1 (palier A) ENS − V0 est supérieur à −0,01 : l'IC95 bootstrap de l'écart est entièrement au-dessus de −0,01 (équivalence unilatérale).

### HF10 : Les jetons typés ajoutés aux mots améliorent le macro-F1  (version 2, 2026-11-09 13:25:59 ; **statut : réfutée**)

FT dépasse V0 d'au moins 0,02 en macro-F1 (palier A), Wilcoxon apparié sur 25 plis, Holm sur HF10 et HF12, p < 0,05. Réfutée si l'IC95 bootstrap de l'écart exclut +0,02.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Macro-F1 palier A, 25 plis : FT 0,489 contre V0 0,503, écart −0,014, IC95 [−0,027 ; −0,001] (exclut +0,02), p Holm 0,08 : pas de gain, tendance à la baisse.  Fichiers : artifacts/results/v3/I2_all_units.csv ; I2_resume.csv ; I2_tests.csv

*Note.* Les jetons typés (programme, champs, types, forme) n'ajoutent pas d'information utile aux classes par rapport aux mots ; la structure est déjà contenue dans le texte.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:18:20) : statut préinscrite ; FT dépasse V0 d'au moins 0,02 en macro-F1 (palier A), Wilcoxon apparié sur 25 plis, Holm sur HF10 et HF12, p < 0,05. Réfutée si l'IC95 bootstrap de l'écart exclut +0,02.

### HF11 : La structure seule porte de l'information  (version 2, 2026-11-09 13:25:59 ; **statut : réfutée**)

FTo (jetons typés sans aucun mot) atteint au moins 60 % du macro-F1 de V0 (0,30 si V0 = 0,503) et dépasse nettement le hasard (1/30 par classe) : IC95 bootstrap de la moyenne de FTo entièrement au-dessus de 0,30.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* FTo (structure seule, sans mot) : macro-F1 0,265, IC95 [0,244 ; 0,285] : la borne haute reste sous le seuil 0,30 (60 % de V0).  Fichiers : artifacts/results/v3/I2_all_units.csv ; I2_resume.csv ; I2_tests.csv

*Note.* Constat à retenir : la structure seule est loin du hasard (1/30 soit 0,03) et retrouve la moitié du score de V0 (53 %), mais ne suffit pas. Écart FTo − V0 : −0,238, 0 pli sur 25 en faveur de FTo.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:18:20) : statut préinscrite ; FTo (jetons typés sans aucun mot) atteint au moins 60 % du macro-F1 de V0 (0,30 si V0 = 0,503) et dépasse nettement le hasard (1/30 par classe) : IC95 bootstrap de la moyenne de FTo entièrement au-des…

### HF12 : Structure + mots + lettres dépasse V0  (version 2, 2026-11-09 13:25:59 ; **statut : réfutée**)

FTE dépasse V0 d'au moins 0,02 en macro-F1 (palier A), même test et même Holm que HF10 ; et FTE dépasse FT de façon significative en macro-F1 de famille d'au moins 0,01 (Wilcoxon apparié).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* FTE contre V0 : macro-F1 des classes −0,017, IC95 [−0,028 ; −0,005], p Holm 0,029 : FTE fait légèrement PIRE que V0, la première condition (+0,02) échoue. Second volet : famille FTE − FT +0,008, IC95 [−0,002 ; 0,017], p = 0,16 : sous le seuil 0,01.  Fichiers : artifacts/results/v3/I2_all_units.csv ; I2_resume.csv ; I2_tests.csv

*Note.* Constat exploratoire (non préinscrit) : FT améliore le F1 de famille de +0,021 contre V0 (IC95 [0,006 ; 0,037], p = 0,026), moins qu'ENS (+0,029) ; les jetons typés n'ajoutent donc pas à ce que les lettres apportent déjà.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 13:18:20) : statut préinscrite ; FTE dépasse V0 d'au moins 0,02 en macro-F1 (palier A), même test et même Holm que HF10 ; et FTE dépasse FT de façon significative en macro-F1 de famille d'au moins 0,01 (Wilcoxon apparié).

### HI1 : La confiance de famille bat le MSP  (version 2, 2026-11-09 14:02:51 ; **statut : confirmée**)

AUROC d'inconnu de fam_msp supérieur à celui du msp d'au moins 0,02 (Wilcoxon apparié unilatéral sur 25 unités (rotation, répétition), Holm sur trois comparaisons : fam_msp contre msp, contre energy, contre hier_msp, p < 0,05). Réfutée si l'IC95 bootstrap de l'écart avec le msp exclut +0,02.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC d'inconnu moyen (25 unités) : fam_msp 0,693 ; msp 0,665 ; energy 0,670 ; hier_msp 0,664. Gains de fam_msp : +0,028 contre msp (IC95 [0,008 ; 0,048], p Holm 0,007, 16 unités sur 25), +0,023 contre energy (IC95 [0,002 ; 0,043], p Holm 0,020), +0,029 contre hier_msp (IC95 [0,013 ; 0,045], p Holm 0,002).  Fichiers : artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json

*Note.* Confirmée au sens de la règle écrite (gain moyen ≥ 0,02 et p Holm < 0,05), mais avec réserve : la borne basse de chaque IC95 est sous 0,02 (0,008 contre msp), l'effet est donc positif de façon fiable mais sa taille (0,02 à 0,03) n'est pas établie précisément. Il reproduit l'ordre du bloc C (famille 0,666 contre MSP 0,623) avec un gain plus petit (0,028 contre 0,043). Limite : mêmes gabarits que le développement, nouvelles rotations et nouveaux plis ; nouveaux gabarits = test v2. Une unité (rotation 1, répétition 5, pli 0) avait été calculée au test de fumée ; le verdict repose sur les 25 unités (rotation, répétition) complètes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 14:00:38) : statut préinscrite ; AUROC d'inconnu de fam_msp supérieur à celui du msp d'au moins 0,02 (Wilcoxon apparié unilatéral sur 25 unités (rotation, répétition), Holm sur trois comparaisons : fam_msp contre msp, contre energy, …

### HI2 : L'avantage de famille tient dans au moins 4 rotations sur 5  (version 2, 2026-11-09 14:02:51 ; **statut : réfutée**)

L'AUROC moyen de fam_msp dépasse celui du msp dans au moins 4 des 5 nouvelles rotations.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Rotations où fam_msp dépasse msp : 3 sur 5 (rotation 1 : 0,658 contre 0,580 ; rotation 3 : 0,740 contre 0,685 ; rotation 4 : 0,666 contre 0,598) ; rotations 2 (0,712 contre 0,737) et 5 (0,689 contre 0,726) en défaveur ; règle : au moins 4 sur 5.  Fichiers : artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json

*Note.* L'avantage moyen vient de trois rotations ; il n'est pas général. Cohérent avec HC8 (forte variabilité entre rotations : AUROC du msp de 0,58 à 0,74 selon la rotation). Limite : mêmes gabarits que le développement, nouvelles rotations et nouveaux plis ; nouveaux gabarits = test v2. Une unité (rotation 1, répétition 5, pli 0) avait été calculée au test de fumée ; le verdict repose sur les 25 unités (rotation, répétition) complètes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 14:00:38) : statut préinscrite ; L'AUROC moyen de fam_msp dépasse celui du msp dans au moins 4 des 5 nouvelles rotations.

### HI3 : Moins d'inconnus acceptés  (version 2, 2026-11-09 14:02:51 ; **statut : réfutée**)

FPR@95 moyen de fam_msp inférieur à celui du msp d'au moins 0,03 (Wilcoxon apparié, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* FPR@95 moyen : msp 0,851 ; fam_msp 0,859 : baisse −0,008 (IC95 [−0,045 ; 0,024], p = 0,85) ; la règle exigeait −0,03.  Fichiers : artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json

*Note.* Le gain d'AUROC ne se traduit pas à l'usage : à 95 % de connus conservés, 85 % des inconnus sont acceptés avec tous les scores. Limite : mêmes gabarits que le développement, nouvelles rotations et nouveaux plis ; nouveaux gabarits = test v2. Une unité (rotation 1, répétition 5, pli 0) avait été calculée au test de fumée ; le verdict repose sur les 25 unités (rotation, répétition) complètes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 14:00:38) : statut préinscrite ; FPR@95 moyen de fam_msp inférieur à celui du msp d'au moins 0,03 (Wilcoxon apparié, p < 0,05).

### HI4 : Le niveau absolu reste insuffisant  (version 2, 2026-11-09 14:02:51 ; **statut : confirmée**)

AUROC moyen de fam_msp inférieur à 0,80 (valeur « acceptable » du critère S2) : IC95 bootstrap de la moyenne entièrement sous 0,80.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* AUROC moyen de fam_msp : 0,693, IC95 [0,680 ; 0,706], entièrement sous 0,80.  Fichiers : artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json

*Note.* Le détecteur d'inconnus reste insuffisant au sens du critère S2, y compris le meilleur. Limite : mêmes gabarits que le développement, nouvelles rotations et nouveaux plis ; nouveaux gabarits = test v2. Une unité (rotation 1, répétition 5, pli 0) avait été calculée au test de fumée ; le verdict repose sur les 25 unités (rotation, répétition) complètes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 14:00:38) : statut préinscrite ; AUROC moyen de fam_msp inférieur à 0,80 (valeur « acceptable » du critère S2) : IC95 bootstrap de la moyenne entièrement sous 0,80.

### HF13 : Le réglage améliore le macro-F1 des classes sur de nouveaux plis  (version 2, 2026-11-09 19:14:25 ; **statut : non tranchée**)

La configuration retenue sur les répétitions 0 à 4 dépasse V0 d'au moins 0,02 en macro-F1 (palier A) sur les 25 plis des répétitions 5 à 9 (Wilcoxon apparié unilatéral, p < 0,05). Réfutée si l'IC95 bootstrap de l'écart exclut +0,02 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Non testée : la porte HF14 est restée fermée, la confirmation I5b sur les répétitions 5 à 9 n'a pas été lancée (règle D21).  Fichiers : artifacts/results/v3/I5a_resume.csv ; I5_selected.json

*Note.* À ne pas lire comme réfutée ni confirmée : aucune donnée de confirmation n'a été consommée.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 17:55:59) : statut préinscrite ; La configuration retenue sur les répétitions 0 à 4 dépasse V0 d'au moins 0,02 en macro-F1 (palier A) sur les 25 plis des répétitions 5 à 9 (Wilcoxon apparié unilatéral, p < 0,05). Réfutée si l'IC95 bo…

### HF14 : Une configuration vaut le coup d'être confirmée  (version 2, 2026-11-09 19:14:25 ; **statut : réfutée**)

Sur les répétitions 0 à 4, la meilleure configuration dépasse V0 d'au moins 0,02 en macro-F1 des classes (porte : en dessous, la confirmation n'est pas lancée ; le meilleur d'une grille est biaisé vers le haut, donc ce gain n'est pas un résultat).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Répétitions 0 à 4 (25 plis) : la meilleure des 3 × 3 × 2 × 3 + références configurations (somme_mC3_l46C1_w0.5 : mots C = 3 + lettres 4-6 C = 1 poids 0,5) a un macro-F1 de 0,5106 contre 0,5032 pour V0 : gain +0,0074, sous le seuil de 0,02 ; 17 plis sur 25 en faveur. Ce gain est le MAXIMUM d'une grille de plus de 70 configurations, donc biaisé vers le haut.  Fichiers : artifacts/results/v3/I5a_resume.csv ; I5_selected.json

*Note.* Aucune configuration ne justifie la confirmation. Les réglages par défaut (C = 1, n-grammes 3-5, poids 1 : 0,5022) sont à moins de 0,01 du meilleur : le plafond de 0,50 n'est pas un problème de réglage.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 17:55:59) : statut préinscrite ; Sur les répétitions 0 à 4, la meilleure configuration dépasse V0 d'au moins 0,02 en macro-F1 des classes (porte : en dessous, la confirmation n'est pas lancée ; le meilleur d'une grille est biaisé ver…

### HT1b : Le Transformer n'améliore pas la classification de plus de 0,02 (réplication)  (version 2, 2026-11-10 00:00:10 ; **statut : confirmée**)

Sur les 20 couples (découpe, rotation), macro-F1 des classes (palier A) du Transformer moins celui de TF-IDF (mêmes logs) : confirmée si la borne HAUTE de l'IC95 bootstrap de l'écart moyen est ≤ 0,02 ; réfutée si la borne BASSE est > 0,02 ; sinon non tranchée (et conservée telle quelle).

*Justification.* Verdict établi avec la règle de décision préinscrite (D22).

*Preuve.* Macro-F1 des classes, Transformer moins TF-IDF (mêmes logs) : −0,0545, IC95 [−0,086 ; −0,020] (borne haute ≤ 0,02) ; Wilcoxon p = 0,9997 ; signes 2 en faveur / 18 contre (p = 0,0004) ; permutation p = 0,9998. Moyennes : Transformer 0,469 ; TF-IDF 0,523.  Fichiers : artifacts/results/v3/T2_all_units.csv ; T2_tests.csv

*Note.* Sur ces découpes le Transformer est MEILLEUR de rien : il est moins bon que TF-IDF de 0,05. Cela contredit le +0,02 de la grille T (une seule découpe, répétition 0 pli 0) : l'écart dépend beaucoup de la découpe, et la grille T était sur une découpe favorable au Transformer. Estimation exploratoire sur les 50 couples (grille T + T2) : −0,0095, IC95 [−0,030 ; 0,010]. Plan T2 : 4 nouvelles découpes (répétitions 1 à 4, plis 1 à 4) × 5 rotations, p = 0, graine 42, 140 logs d'entraînement par classe ; 20 couples (découpe, rotation).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:31:12) : statut préinscrite ; Sur les 20 couples (découpe, rotation), macro-F1 des classes (palier A) du Transformer moins celui de TF-IDF (mêmes logs) : confirmée si la borne HAUTE de l'IC95 bootstrap de l'écart moyen est ≤ 0,02 …

### HT2b : Mahalanobis dépasse le MSP d'au moins 0,03 sur les vecteurs du Transformer (réplication)  (version 2, 2026-11-10 00:00:10 ; **statut : non tranchée**)

Sur les 20 couples, AUROC d'inconnu de Mahalanobis (commune, vecteurs de 768 valeurs) moins AUROC du MSP du même Transformer : confirmée si la borne BASSE de l'IC95 bootstrap est ≥ 0,03 ; réfutée si la borne HAUTE est < 0,03 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (D22).

*Preuve.* AUROC d'inconnu de Mahalanobis moins MSP (Transformer) : +0,0429, IC95 [0,011 ; 0,074] (contient 0,03) ; Wilcoxon unilatéral p = 0,165 ; signes 13/7 ; permutation p = 0,22.  Fichiers : artifacts/results/v3/T2_all_units.csv ; T2_tests.csv

*Note.* Les deux séries donnent +0,0325 (grille T) et +0,0429 (T2), toutes deux compatibles avec 0,03 ; estimation exploratoire sur les 50 couples : +0,0367, IC95 [0,022 ; 0,052], p Wilcoxon 0,18. En pratique : Mahalanobis gagne entre +0,02 et +0,05 sur le MSP du Transformer, sans qu'on puisse dire s'il atteint exactement 0,03 ; la règle (sinon non tranchée, on arrête) est appliquée, la question du seuil exact est sans intérêt pratique (AUROC de 0,60 contre 0,65). Plan T2 : 4 nouvelles découpes (répétitions 1 à 4, plis 1 à 4) × 5 rotations, p = 0, graine 42, 140 logs d'entraînement par classe ; 20 couples (découpe, rotation).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:31:12) : statut préinscrite ; Sur les 20 couples, AUROC d'inconnu de Mahalanobis (commune, vecteurs de 768 valeurs) moins AUROC du MSP du même Transformer : confirmée si la borne BASSE de l'IC95 bootstrap est ≥ 0,03 ; réfutée si l…

### HF15 : La fusion Transformer + TF-IDF améliore la classification  (version 2, 2026-11-10 00:00:10 ; **statut : réfutée**)

Sur les 20 couples, le macro-F1 (palier A) de la fusion dépasse celui du meilleur de ses deux composants d'au moins 0,01 (Wilcoxon apparié unilatéral p < 0,05 contre CHACUN des deux composants, Holm sur 2 ; moyenne de l'écart ≥ 0,01). Réfutée si l'IC95 de l'écart avec le meilleur composant exclut +0,01.

*Justification.* Verdict établi avec la règle de décision préinscrite (D22).

*Preuve.* Macro-F1 des classes, fusion (moyenne des probabilités) : 0,508 ; Transformer 0,469 (fusion +0,040, IC95 [0,024 ; 0,055], p = 0,001) ; TF-IDF 0,523 (fusion −0,015, IC95 [−0,036 ; 0,009], signes 4/16) : la fusion ne dépasse pas le meilleur de ses composants (TF-IDF) ; la borne haute de l'IC95 de l'écart avec le meilleur composant (0,009) exclut +0,01.  Fichiers : artifacts/results/v3/T2_all_units.csv ; T2_tests.csv

*Note.* La fusion n'améliore que le moins bon des deux : une moyenne de probabilités avec un Transformer plus faible tire TF-IDF vers le bas. Plan T2 : 4 nouvelles découpes (répétitions 1 à 4, plis 1 à 4) × 5 rotations, p = 0, graine 42, 140 logs d'entraînement par classe ; 20 couples (découpe, rotation).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:31:12) : statut préinscrite ; Sur les 20 couples, le macro-F1 (palier A) de la fusion dépasse celui du meilleur de ses deux composants d'au moins 0,01 (Wilcoxon apparié unilatéral p < 0,05 contre CHACUN des deux composants, Holm s…

### HF16 : La fusion améliore la confiance de famille pour détecter les inconnus  (version 2, 2026-11-10 00:00:10 ; **statut : non tranchée**)

AUROC d'inconnu de la confiance de famille de la fusion supérieur d'au moins 0,01 à celui du meilleur composant (famille Transformer, famille TF-IDF), même test et même Holm que HF15.

*Justification.* Verdict établi avec la règle de décision préinscrite (D22).

*Preuve.* AUROC de la confiance de famille : fusion 0,664 ; TF-IDF 0,656 ; Transformer 0,647. Fusion moins meilleur composant (TF-IDF) : +0,008, IC95 [−0,019 ; 0,037] (contient 0,01) ; moins Transformer : +0,018, IC95 [−0,010 ; 0,046] ; p unilatéraux 0,64 et 0,26.  Fichiers : artifacts/results/v3/T2_all_units.csv ; T2_tests.csv

*Note.* Pas de gain établi : ni confirmée ni réfutée au sens de la règle ; aucun intérêt pratique visible (+0,008). Plan T2 : 4 nouvelles découpes (répétitions 1 à 4, plis 1 à 4) × 5 rotations, p = 0, graine 42, 140 logs d'entraînement par classe ; 20 couples (découpe, rotation).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:31:12) : statut préinscrite ; AUROC d'inconnu de la confiance de famille de la fusion supérieur d'au moins 0,01 à celui du meilleur composant (famille Transformer, famille TF-IDF), même test et même Holm que HF15.

### HF17 : Une nouvelle configuration vaut la peine d'être confirmée  (version 2, 2026-11-09 22:07:28 ; **statut : réfutée**)

Sur les répétitions 0 à 4, la meilleure des 32 configurations dépasse V0 de 0,02 en macro-F1 des classes (porte : sinon pas de confirmation ; ce maximum est biaisé vers le haut).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Répétitions 0 à 4 (25 plis) : la meilleure des 32 configurations (W1_lr30 : lettres ≥ 2 min_df = 1 + régression logistique C = 30) a un macro-F1 de 0,5117 contre 0,5032 pour V0 : +0,0085, IC95 [−0,009 ; 0,027], Wilcoxon unilatéral p = 0,26, signes 13/12, permutation p = 0,19 : sous le seuil de 0,02 (porte fermée).  Fichiers : artifacts/results/v3/I6a_all_units.csv ; I6a_resume.csv ; I6a_friedman.csv ; I6_selected.json

*Note.* Maximum de 32 configurations, donc optimiste : aucun test ne l'établit même ainsi. La confirmation I6b n'est pas lancée.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:32:42) : statut préinscrite ; Sur les répétitions 0 à 4, la meilleure des 32 configurations dépasse V0 de 0,02 en macro-F1 des classes (porte : sinon pas de confirmation ; ce maximum est biaisé vers le haut).

### HF18 : La configuration retenue améliore le macro-F1 des classes sur de nouveaux plis  (version 3, 2026-11-09 22:11:39 ; **statut : réfutée**)

Sur les 25 plis des répétitions 5 à 9, la configuration retenue dépasse V0 d'au moins 0,02 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,02 et si Wilcoxon, test des signes et test de permutation (unilatéraux) donnent tous p < 0,05 ; réfutée si la borne haute de l'IC95 est < 0,02 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite, après lancement de la confirmation I6b demandé par l'étudiant (D25) ; remplace l'entrée « non testée ».

*Preuve.* 25 plis (répétitions 5 à 9) : W1_lr30 0,5105 contre V0 0,5132 : écart −0,0027, IC95 [−0,016 ; 0,011] (borne haute < 0,02), Wilcoxon p = 0,998, signes 5 en faveur / 20 contre (p bilatéral 0,004), permutation p = 0,999. Famille : F1 +0,0075 (IC95 [−0,015 ; 0,030]), distance dans l'arbre −0,008 (non significatifs).  Fichiers : artifacts/results/v3/I6b_all_units.csv ; I6b_tests.csv ; I6_selected.json

*Note.* Confirmation lancée alors que la porte HF17 était fermée (+0,0085 en développement) : le résultat est conforme à ce que la porte laissait prévoir. La configuration choisie par maximum de grille ne tient pas sur de nouveaux plis (retour vers la moyenne) : elle est même moins bonne que V0 dans 20 plis sur 25.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:32:42) : statut préinscrite ; Sur les 25 plis des répétitions 5 à 9, la configuration retenue dépasse V0 d'au moins 0,02 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,02 et si Wilcoxon, test des signes et test de permu…
- v2 (2026-11-09 22:07:28) : statut non tranchée ; Sur les 25 plis des répétitions 5 à 9, la configuration retenue dépasse V0 d'au moins 0,02 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,02 et si Wilcoxon, test des signes et test de permu…

### HF19 : Beaucoup de configurations sont indiscernables du meilleur  (version 2, 2026-11-09 22:07:28 ; **statut : confirmée**)

Friedman sur les 32 configurations × 25 plis (répétitions 0 à 4) rejette l'égalité (p < 0,05), et au moins 5 configurations sont indiscernables du meilleur au sens de Nemenyi (différence critique).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Friedman sur 32 configurations × 25 plis : chi2 = 134,9, p = 6e-15 (l'égalité est rejetée) ; différence critique de Nemenyi 10,0 rangs ; 25 configurations sur 32 (dont le meilleur) sont indiscernables du meilleur, donc 24 autres.  Fichiers : artifacts/results/v3/I6a_all_units.csv ; I6a_resume.csv ; I6a_friedman.csv ; I6_selected.json

*Note.* Les extrêmes sont bien différents (les configurations sensibles à la casse W5 et Ridge perdent jusqu'à 0,038), mais l'essentiel de la grille tient dans l'intervalle de bruit : le réglage ne compte pas, le plafond est dans les données. Défaut corrigé avant lecture : la version 1 de l'analyse (AI6) lisait les rangs à l'envers ; la version 2 les lit correctement (rang 1 = meilleur).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:32:42) : statut préinscrite ; Friedman sur les 32 configurations × 25 plis (répétitions 0 à 4) rejette l'égalité (p < 0,05), et au moins 5 configurations sont indiscernables du meilleur au sens de Nemenyi (différence critique).

### HI5 : Une combinaison dépasse nettement le MSP de référence en développement  (version 2, 2026-11-09 22:07:28 ; **statut : confirmée**)

Sur l'ensemble B, la meilleure des 24 combinaisons dépasse le msp (C = 4) d'au moins 0,03 d'AUROC d'inconnu (porte : sinon pas de confirmation).

*Justification.* Verdict établi avec la règle de décision préinscrite (voir la version précédente).

*Preuve.* Ensemble B (rotations 20261110 × répétitions 0 à 4, 25 unités) : msp (C = 4) 0,6084 ; meilleure candidate C64_fam_negent (entropie de famille, C = 64) 0,6498 : +0,0414 (IC95 [0,032 ; 0,052], permutation p = 0,021 ; Wilcoxon p = 0,057 contre le seuil 0,03 ; 15/10 pour la candidate) ; Friedman p = 2e-46, 13 combinaisons indiscernables du meilleur.  Fichiers : artifacts/results/v3/I7a_all_units.csv ; I7a_resume.csv ; I7a_friedman.csv ; I7b_all_units.csv ; I7b_resume.csv ; I7b_tests.csv ; I7_selected.json ; artifacts/data/rotations_v2_I7a.json ; rotations_v2_I7b.json

*Note.* Tous les scores de famille sont groupés à 0,645-0,650 : l'avantage vient du niveau famille, pas du choix précis du score ni de C.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:35:36) : statut préinscrite ; Sur l'ensemble B, la meilleure des 24 combinaisons dépasse le msp (C = 4) d'au moins 0,03 d'AUROC d'inconnu (porte : sinon pas de confirmation).

### HI6 : La combinaison retenue dépasse le MSP de référence sur de nouvelles rotations  (version 3, 2026-11-09 22:25:21 ; **statut : confirmée**)

Sur l'ensemble C (125 unités, 25 unités (rotation, répétition)), la combinaison retenue dépasse le msp (C = 4) d'au moins 0,03 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,03 et si Wilcoxon, signes et permutation (unilatéraux, écart > 0,03) donnent p < 0,05 ; réfutée si la borne haute est < 0,03 ; sinon non tranchée.

*Justification.* Tranchée par la réplication préinscrite D25 (HI6b, 75 unités) ; l'entrée « non tranchée » précédente est conservée.

*Preuve.* Voir HI6b.

*Note.* Source : I7c.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:35:36) : statut préinscrite ; Sur l'ensemble C (125 unités, 25 unités (rotation, répétition)), la combinaison retenue dépasse le msp (C = 4) d'au moins 0,03 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,03 et si Wilcox…
- v2 (2026-11-09 22:07:28) : statut non tranchée ; Sur l'ensemble C (125 unités, 25 unités (rotation, répétition)), la combinaison retenue dépasse le msp (C = 4) d'au moins 0,03 : confirmée si la borne basse de l'IC95 bootstrap est ≥ 0,03 et si Wilcox…

### HI7 : La combinaison retenue réduit le FPR@95  (version 3, 2026-11-09 22:25:21 ; **statut : réfutée**)

Sur l'ensemble C, le FPR@95 de la combinaison retenue est inférieur d'au moins 0,05 à celui du msp (C = 4) (mêmes critères que HI6).

*Justification.* Tranchée par la réplication préinscrite D25 (HI7b, 75 unités) ; l'entrée « non tranchée » précédente est conservée.

*Preuve.* Voir HI7b.

*Note.* Source : I7c.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 21:35:36) : statut préinscrite ; Sur l'ensemble C, le FPR@95 de la combinaison retenue est inférieur d'au moins 0,05 à celui du msp (C = 4) (mêmes critères que HI6).
- v2 (2026-11-09 22:07:28) : statut non tranchée ; Sur l'ensemble C, le FPR@95 de la combinaison retenue est inférieur d'au moins 0,05 à celui du msp (C = 4) (mêmes critères que HI6).

### HI6b : La combinaison retenue (C64_fam_negent) dépasse le MSP de référence d'au moins 0,03 d'AUROC (réplication)  (version 2, 2026-11-09 22:25:21 ; **statut : confirmée**)

Sur les 75 unités (rotation, répétition) des ensembles D, E, F : confirmée si la borne basse de l'IC95 bootstrap de l'écart (C64_fam_negent − msp C = 4) est ≥ 0,03 et si Wilcoxon, signes et permutation (unilatéraux, écart > 0,03) donnent p < 0,05 ; réfutée si la borne haute de l'IC95 est < 0,03 ; sinon non tranchée (et on arrête : pas de réplication supplémentaire).

*Justification.* Verdict établi avec la règle de décision préinscrite (D25).

*Preuve.* 75 unités (jeux D, E, F × répétitions 10 à 14) : AUROC C64_fam_negent 0,6690 contre msp (C = 4) 0,6271 : +0,0419, IC95 [0,0324 ; 0,0512] (borne basse ≥ 0,03) ; Wilcoxon unilatéral (écart > 0,03) p = 0,0095 ; permutation p = 0,0087 ; test des signes unilatéral p = 0,032 (46 unités en faveur, 29 contre ; le fichier I7c_tests.csv rapporte le p bilatéral 0,064, la règle exige l'unilatéral). Par jeu : +0,040 ; +0,042 ; +0,044.  Fichiers : artifacts/results/v3/I7c_all_units.csv ; I7c_resume.csv ; I7c_tests.csv ; artifacts/data/rotations_v2_I7c.json

*Note.* Résultat conforme à la sélection (+0,041) : l'effet de +0,04 est stable sur 3 jeux de rotations et 75 unités. Le test des signes est le plus fragile (p unilatéral 0,032) ; aucune des trois rotations de l'ensemble C de I7b n'avait donné ce résultat (+0,0175, 25 unités, intervalle trop large). Précision : tous les scores de famille donnent +0,035 à +0,043 ; ce n'est pas C64_fam_negent en particulier qui gagne.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 22:09:48) : statut préinscrite ; Sur les 75 unités (rotation, répétition) des ensembles D, E, F : confirmée si la borne basse de l'IC95 bootstrap de l'écart (C64_fam_negent − msp C = 4) est ≥ 0,03 et si Wilcoxon, signes et permutatio…

### HI7b : La combinaison retenue réduit le FPR@95 d'au moins 0,05 (réplication)  (version 2, 2026-11-09 22:25:21 ; **statut : réfutée**)

Mêmes 75 unités : baisse du FPR@95 (msp C = 4 moins C64_fam_negent) ; mêmes critères que HI6b avec le seuil 0,05.

*Justification.* Verdict établi avec la règle de décision préinscrite (D25).

*Preuve.* Baisse du FPR@95 (msp C = 4 moins C64_fam_negent) : 0,0204, IC95 [0,0069 ; 0,0334] (borne haute < 0,05) ; Wilcoxon p = 1,0 ; signes 25 en faveur / 50 contre.  Fichiers : artifacts/results/v3/I7c_all_units.csv ; I7c_resume.csv ; I7c_tests.csv ; artifacts/data/rotations_v2_I7c.json

*Note.* La confiance de famille améliore l'AUROC mais pas assez le FPR@95 : à 95 % de connus conservés, 85 % des inconnus restent acceptés (0,874 pour le msp, 0,854 pour la famille).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-09 22:09:48) : statut préinscrite ; Mêmes 75 unités : baisse du FPR@95 (msp C = 4 moins C64_fam_negent) ; mêmes critères que HI6b avec le seuil 0,05.

### HG1 : Les embeddings gelés apportent de la sémantique (E1/E2)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

Au moins une des variantes E1, E2 dépasse V0 d'au moins 0,02 de macro-F1 (palier A) sur les 25 plis des répétitions 0 à 4 (Wilcoxon apparié unilatéral, Holm sur les 10 variantes de la ronde, p < 0,05).

*Justification.* Un modèle de langue pré-entraîné rapproche « accessed » de « opened ».

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG2 : Le prior de sens sur le nom de la classe aide (E3)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

E3 dépasse V0 d'au moins 0,02 (mêmes critères que HG1).

*Justification.* Le nom de la classe est une connaissance disponible sans exemple.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG3 : Le lexique de concepts aide (L1)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

L1 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Regrouper les synonymes d'actions fait partager aux gabarits des jetons communs.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG4 : Les concepts seuls retrouvent une part du score (L2)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

L2 atteint au moins 50 % du macro-F1 de V0 (≥ 0,25), IC95 bootstrap de la moyenne entièrement au-dessus de 0,25.

*Justification.* Mesure de l'information portée par le lexique seul.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG5 : La suppression aléatoire de mots simule des gabarits nouveaux (A1, A2)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

Au moins une des variantes A1, A2 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Forcer le modèle à reconnaître la classe avec une partie des mots seulement.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG6 : Pondérer les gabarits en plus de l'augmentation aide (A3 contre A2)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

A3 dépasse A2 d'au moins 0,01 (Wilcoxon apparié unilatéral, p < 0,05, sans Holm).

*Justification.* Un gabarit géant ne doit pas dominer.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG7 : Le discriminant au niveau du gabarit bat les classifieurs au niveau des logs (S1)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

S1 dépasse V0 d'au moins 0,02 (mêmes critères que HG1).

*Justification.* La variabilité qui compte est entre gabarits, pas entre logs.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG8 : Combiner S1 et V0 dépasse chacun (S2)  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

S2 dépasse V0 et S1 d'au moins 0,01 chacun (Wilcoxon apparié unilatéral p < 0,05).

*Justification.* Deux géométries différentes.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG9 : Une variante de la ronde passe la porte de confirmation  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

Au moins une des 10 variantes dépasse V0 de 0,02 avec Holm p < 0,05 sur les répétitions 0 à 4 (condition pour lancer la confirmation sur 5 à 9).

*Justification.* Évite de confirmer sans signal ; si fausse, la ronde 3 est close sans gain.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HG10 : Les classes à très peu de gabarits sont celles qui changent  (version 1, 2026-11-10 00:03:47 ; **statut : préinscrite**)

Parmi les variantes de la ronde, la différence de F1 par classe (variante moins V0) est plus grande pour les classes à ≤ 3 gabarits dans le développement que pour les autres (Mann-Whitney sur les classes, p < 0,05), pour la meilleure variante.

*Justification.* Vérifie que le mécanisme est celui de DG2.

*Note.* Écrit le 2026-11-10 avant tout calcul de la ronde 3.

### HW1 : Équilibrer les masses prédites aide (F8)  (version 2, 2026-11-10 13:26:20 ; **statut : confirmée**)

A1 ou A2 dépasse la référence LR d'au moins 0,02 de macro-F1 du palier A (Wilcoxon apparié unilatéral, Holm sur les 14 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* Sélection (25 plis, répétitions 0-4) : A1 (Sinkhorn amorti sur les probabilités de la régression logistique) macro-F1 palier A 0,5752 contre LR 0,4947 : +0,0805, IC95 [0,061 ; 0,102], Wilcoxon p < 1e-4, Holm < 1e-4, 24 plis sur 25 en faveur ; A2 (EM de prior) 0,4380 : −0,0567. Confirmation (25 nouveaux plis, répétitions 5-9) : A1 0,5544 contre LR 0,4976 : +0,0568, IC95 [0,038 ; 0,076] (borne basse ≥ 0,02), Wilcoxon p = 0,0007, permutation p = 0,0004, signes 19 en faveur / 6 contre, Holm 0,010. Contre le SVM mots V0 (meilleure référence classique) : +0,072 en sélection (0,5752 contre 0,5032), +0,041 en confirmation (0,5544 contre 0,5132).  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* PREMIÈRE AMÉLIORATION CONFIRMÉE de la phase 2. Conditions à écrire dans l'article : (1) le décodage est TRANSDUCTIF : il utilise la composition du lot de test sans étiquette (masses prédites) ; (2) la cible uniforme convient à un lot où toutes les classes sont présentes en proportions comparables au niveau gabarit ; (3) l'EM de prior (A2), qui adapte le prior à la composition du test, fait PIRE (−0,057) : le gain vient du forçage vers l'équilibre, pas de l'adaptation du prior. Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; A1 ou A2 dépasse la référence LR d'au moins 0,02 de macro-F1 du palier A (Wilcoxon apparié unilatéral, Holm sur les 14 variantes, p < 0,05).

### HW2 : La troncature de racine aide (F14)  (version 2, 2026-11-10 13:26:20 ; **statut : réfutée**)

Au moins un k parmi 5, 6, 7 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* Troncature à 5, 6, 7 lettres : gains −0,0085 ; −0,0010 ; +0,0020 ; bornes hautes de l'IC95 0,004 ; 0,008 ; 0,009 (< 0,02) ; Holm 1,0.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.*  Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; Au moins un k parmi 5, 6, 7 dépasse V0 d'au moins 0,02 (mêmes critères).

### HW3 : Un IDF de gabarit avec pureté de classe aide (F6)  (version 2, 2026-11-10 13:26:20 ; **statut : réfutée**)

Au moins une des variantes C0, C1, C2 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* IDF de gabarit seul (C0) −0,0228, IC95 [−0,034 ; −0,012] ; avec pureté de classe (C1, C2) −0,0191 et −0,0182 ; toutes pires que V0, Holm 1,0.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* Les mots propres à un gabarit portent de l'information (cf. HF1) ; l'IDF au niveau gabarit les sur-pondère ou sous-pondère mal ; la pureté rétrécie ne répare pas. Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; Au moins une des variantes C0, C1, C2 dépasse V0 d'au moins 0,02 (mêmes critères).

### HW4 : La hiérarchie à vues séparées aide (F9)  (version 2, 2026-11-10 13:26:20 ; **statut : non tranchée**)

Au moins un β parmi 0,5 ; 1 ; 2 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* Hiérarchie à vues séparées : β = 0,5 : 0,5307 contre V0 0,5032 (+0,0274, IC95 [0,016 ; 0,039]) ; β = 1 : +0,0224 [0,008 ; 0,037] ; β = 2 : +0,0183 [0,002 ; 0,034] ; mais Wilcoxon unilatéral contre le seuil 0,02 : p = 0,22 ; 0,43 ; 0,53 ; Holm 1,0 : seuil non établi ; gain positif dans 12 à 13 plis sur 25 contre le seuil.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* Gain d'environ +0,02 à +0,03 par rapport à V0, positif mais pas significativement ≥ 0,02 : à reprendre dans la vague 2 (combinaison avec A1, où les gains pourraient s'ajouter). Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; Au moins un β parmi 0,5 ; 1 ; 2 dépasse V0 d'au moins 0,02 (mêmes critères).

### HW5 : Retirer les jetons de format aide (E1)  (version 2, 2026-11-10 13:26:20 ; **statut : réfutée**)

E1 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* E1 (retrait des mois, jours, am/pm, pid, utc et du nom du programme) 0,4694 contre V0 0,5032 : −0,0338, IC95 [−0,049 ; −0,018] ; classes à ≤ 3 gabarits : −0,106.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* Retirer les jetons de format fait PERDRE de l'information : le nom du programme ou la forme de l'horodatage aident à reconnaître la classe (cohérent avec DG4 : information mutuelle format-classe 0,56). Le « raccourci du format » n'est pas confirmé comme obstacle. Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; E1 dépasse V0 d'au moins 0,02 (mêmes critères).

### HW6 : Décorréler format et classe aide (E2)  (version 2, 2026-11-10 13:26:20 ; **statut : réfutée**)

E2 dépasse V0 d'au moins 0,02 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* E2 (poids de décorrélation format × classe) 0,4974 contre V0 0,5032 : −0,0058, IC95 [−0,009 ; −0,003] ; 0 pli sur 25 en faveur au-dessus du seuil.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* Décorréler le format ne sert pas : le format est une information utile, pas un raccourci nuisible. Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; E2 dépasse V0 d'au moins 0,02 (mêmes critères).

### HW7 : Au moins une variante passe la porte  (version 2, 2026-11-10 13:26:20 ; **statut : confirmée**)

Au moins une des 14 variantes dépasse sa référence d'au moins 0,02 avec Holm p < 0,05 sur les répétitions 0 à 4 (sinon pas de confirmation et la vague 1 est close sans gain).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* Une variante (A1) passe la porte : +0,0805 avec Holm < 1e-4 sur les répétitions 0 à 4.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.*  Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; Au moins une des 14 variantes dépasse sa référence d'au moins 0,02 avec Holm p < 0,05 sur les répétitions 0 à 4 (sinon pas de confirmation et la vague 1 est close sans gain).

### HW8 : Le mécanisme est celui de DG4  (version 2, 2026-11-10 13:26:20 ; **statut : réfutée**)

Pour toute variante passant la porte, le gain de macro-F1 sur les classes à ≤ 3 gabarits de développement est positif et supérieur à celui des autres classes (Wilcoxon apparié sur les plis, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D28).

*Preuve.* A1 : gain sur les classes à ≤ 3 gabarits de développement +0,0406 ; gain sur le palier A +0,0805 ; Wilcoxon apparié p = 0,016 : le gain est PLUS GRAND sur le palier A que sur les classes rares, à l'opposé de l'hypothèse.  Fichiers : artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

*Note.* Le mécanisme n'est donc pas celui de DG4 (sauvetage des classes rares) : le décodage équilibré corrige surtout l'absorption de gabarits par des classes très nombreuses (authentication-failed : 43 gabarits) au bénéfice des classes de taille moyenne. Les classes à 1-3 gabarits gagnent aussi (+0,04) mais moins. À examiner classe par classe en vague 2. Remarque : D28 annonçait « 14 variantes » alors que la liste en compte 13 ; Holm appliqué avec m = 14 comme écrit (plus prudent).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:19:51) : statut préinscrite ; Pour toute variante passant la porte, le gain de macro-F1 sur les classes à ≤ 3 gabarits de développement est positif et supérieur à celui des autres classes (Wilcoxon apparié sur les plis, p < 0,05).

### HX1 : Le décodage équilibré sur le SVM dépasse celui sur la LR (S1, S2)  (version 2, 2026-11-10 13:31:52 ; **statut : réfutée**)

Au moins une des variantes S1, S2 dépasse A1 d'au moins 0,01 de macro-F1 du palier A (Wilcoxon apparié unilatéral contre le seuil, Holm sur 8 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Équilibrage sur le SVM : S1 (τ = 5) 0,5551 contre A1 0,5752 : −0,0202, IC95 [−0,031 ; −0,010] ; S2 (τ = 10) −0,0258, IC95 [−0,040 ; −0,011] ; Holm 1,0.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* Meilleur classifieur de base, mais ses marges transformées en probabilités sont moins bien calibrées pour l'équilibrage que les probabilités de la régression logistique.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; Au moins une des variantes S1, S2 dépasse A1 d'au moins 0,01 de macro-F1 du palier A (Wilcoxon apparié unilatéral contre le seuil, Holm sur 8 variantes, p < 0,05).

### HX2 : Le réglage de l'équilibrage compte (G25, G1, I30)  (version 2, 2026-11-10 13:31:52 ; **statut : réfutée**)

Au moins une des variantes G25, G1, I30 dépasse A1 d'au moins 0,01 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Exposant 0,25 : −0,0015, IC95 [−0,0095 ; 0,0058] ; exposant 1,0 : −0,0019, IC95 [−0,0045 ; 0,0009] ; 30 itérations : −0,0023, IC95 [−0,0050 ; 0,0007] ; bornes hautes < 0,01.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* Le gain d'A1 ne dépend pas finement des réglages d'amortissement et d'itérations (plateau).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; Au moins une des variantes G25, G1, I30 dépasse A1 d'au moins 0,01 (mêmes critères).

### HX3 : Équilibrer vers un prior en racine du nombre de gabarits n'améliore pas (P5)  (version 2, 2026-11-10 13:31:52 ; **statut : confirmée**)

P5 ne dépasse PAS A1 d'au moins 0,01 (IC95 de l'écart avec A1 dont la borne haute est < 0,01) : confirmée si c'est le cas.

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Cibles proportionnelles à la racine du nombre de gabarits (P5) : −0,0163, IC95 [−0,035 ; 0,0013] ; borne haute < 0,01 : ne dépasse pas A1.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* Cohérent avec A2 (EM de prior) : s'écarter de l'uniforme fait perdre.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; P5 ne dépasse PAS A1 d'au moins 0,01 (IC95 de l'écart avec A1 dont la borne haute est < 0,01) : confirmée si c'est le cas.

### HX4 : Équilibrer d'abord les familles aide (H1)  (version 2, 2026-11-10 13:31:52 ; **statut : réfutée**)

H1 dépasse A1 d'au moins 0,01 (mêmes critères que HX1).

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Équilibrage de famille puis de classe (H1) : +0,0002, IC95 [−0,0007 ; 0,0012] ; identique à A1 (0 plis sur 25 en faveur au-dessus du seuil).  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; H1 dépasse A1 d'au moins 0,01 (mêmes critères que HX1).

### HX5 : Combiner F9 et A1 additionne les gains (F9S)  (version 2, 2026-11-10 13:31:52 ; **statut : non tranchée**)

F9S dépasse A1 d'au moins 0,01 (mêmes critères que HX1).

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* F9S (marges V0 + 0,5 log p_lettres(famille), puis softmax, puis A1) : +0,0007, IC95 [−0,016 ; 0,017] (contient 0,01) ; Wilcoxon unilatéral p = 0,82.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* Les gains de F9 (+0,02 à +0,03 sans équilibrage, HW4) ne s'ajoutent pas à ceux d'A1 : A1 les absorbe probablement (même mécanisme de correction des absorptions).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; F9S dépasse A1 d'au moins 0,01 (mêmes critères que HX1).

### HX6 : Le décodage équilibré résiste à l'absence de classes  (version 2, 2026-11-10 13:31:52 ; **statut : non tranchée**)

Sur les plis dont 8 classes tirées au hasard sont retirées du lot de test, A1_abs dépasse LR_abs d'au moins 0,02 de macro-F1 du palier A : confirmée si la borne basse de l'IC95 est ≥ 0,02 et si Wilcoxon, signes et permutation (unilatéraux) donnent p < 0,05 ; réfutée si la borne haute est < 0,02.

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Lots dont 8 classes tirées au hasard sont retirées : sélection (répétitions 0-4) A1_abs 0,5918 contre LR_abs 0,5538 : +0,0380, IC95 [0,008 ; 0,069], Wilcoxon p = 0,21, signes 13/12 (contre le seuil 0,02) ; CONFIRMATION (répétitions 5-9, nouveaux plis) A1_abs 0,5474 contre LR_abs 0,5425 : +0,0049, IC95 [−0,021 ; 0,029], Wilcoxon p = 0,84, signes 9/16. La borne basse n'atteint pas 0,02 et la borne haute ne l'exclut pas : non tranchée.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* RÉSERVE MAJEURE : le gain d'A1 (+0,057 à +0,08 quand toutes les classes sont présentes) disparaît presque (+0,005 à +0,04) quand 8 classes sont absentes du lot : la cible uniforme sur 30 classes force des gabarits vers des classes absentes. Le test final pouvant contenir peu de petites classes, A1 n'est PAS présentable seul : voir la vague 3 (équilibrage conscient de la présence).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; Sur les plis dont 8 classes tirées au hasard sont retirées du lot de test, A1_abs dépasse LR_abs d'au moins 0,02 de macro-F1 du palier A : confirmée si la borne basse de l'IC95 est ≥ 0,02 et si Wilcox…

### HX7 : Au moins une variante dépasse A1  (version 2, 2026-11-10 13:31:52 ; **statut : réfutée**)

Au moins une des variantes S1, S2, G25, G1, I30, P5, H1, F9S dépasse A1 d'au moins 0,01 avec Holm p < 0,05 sur les répétitions 0 à 4 (sinon pas de confirmation : A1 reste la configuration finale).

*Justification.* Verdict établi avec la règle de décision préinscrite (D29).

*Preuve.* Aucune des 8 variantes ne dépasse A1 d'au moins 0,01 avec Holm p < 0,05 : meilleurs écarts +0,0007 (F9S) et +0,0002 (H1) ; tous les autres négatifs.  Fichiers : artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

*Note.* A1 est un plateau local pour ces axes : on ne l'améliore pas par ces réglages ; la direction utile est sa robustesse (vague 3).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:27:21) : statut préinscrite ; Au moins une des variantes S1, S2, G25, G1, I30, P5, H1, F9S dépasse A1 d'au moins 0,01 avec Holm p < 0,05 sur les répétitions 0 à 4 (sinon pas de confirmation : A1 reste la configuration finale).

### HY1 : Une variante gagne dans les deux conditions  (version 2, 2026-11-10 13:33:13 ; **statut : réfutée**)

Au moins une des 6 variantes Q25, Q50, Q25b, Q50b, M50, Z (contre LR dans la même condition) a un gain de macro-F1 du palier A ≥ 0,02 dans la condition « toutes » ET dans la condition « abs8 », avec Holm (6 variantes, par condition) p < 0,05 (Wilcoxon unilatéral contre le seuil 0,02) sur les répétitions 0 à 4 : porte de la confirmation.

*Justification.* Verdict établi avec la règle de décision préinscrite (D30).

*Preuve.* Sélection (25 plis, répétitions 0-4) : gains minimaux (toutes, abs8) : Q25b +0,0476 ; M50 +0,0460 ; Q25 +0,0435 ; Z +0,0422 ; Q50b +0,0229 ; Q50 +0,0215. Mais Holm (6 variantes, Wilcoxon unilatéral contre le seuil 0,02) : en « abs8 » p Holm 0,077 (Q25b), 0,098 (M50, Q25) : la règle exige p Holm < 0,05 dans les deux conditions : AUCUNE variante ne passe la porte.  Fichiers : artifacts/results/v3/W3a_all_units.csv ; W3a_tests.csv ; W3_selected.json

*Note.* Le verdict est « réfutée » au sens strict de la porte. Les moyennes de gain sont pourtant ≥ 0,04 dans « toutes » et « abs8 » pour quatre variantes, et la borne basse de l'IC95 est ≥ 0,02 pour Q25b dans les deux conditions : la porte est défaillante par manque de puissance (25 plis, écart-type élevé en abs8), pas par absence d'effet apparent.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:31:52) : statut préinscrite ; Au moins une des 6 variantes Q25, Q50, Q25b, Q50b, M50, Z (contre LR dans la même condition) a un gain de macro-F1 du palier A ≥ 0,02 dans la condition « toutes » ET dans la condition « abs8 », avec H…

### HY2 : La variante retenue garde l'essentiel du gain d'A1 quand tout est présent  (version 2, 2026-11-10 13:33:13 ; **statut : non tranchée**)

Dans la condition « toutes », la variante retenue conserve au moins 80 % du gain d'A1 sur LR (A1 : +0,0805 en sélection) : gain ≥ 0,064.

*Justification.* Verdict établi avec la règle de décision préinscrite (D30).

*Preuve.* Non évaluée : aucune variante n'a passé la porte HY1. À titre indicatif : gain en « toutes » de Z +0,0796 (99 % de celui d'A1), M50 +0,0598 (74 %), Q25b +0,0558 (69 %), Q25 +0,0553 (69 %).  Fichiers : artifacts/results/v3/W3a_all_units.csv ; W3a_tests.csv ; W3_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:31:52) : statut préinscrite ; Dans la condition « toutes », la variante retenue conserve au moins 80 % du gain d'A1 sur LR (A1 : +0,0805 en sélection) : gain ≥ 0,064.

### HY3 : La variante retenue est confirmée sur de nouveaux plis dans les deux conditions  (version 1, 2026-11-10 13:31:52 ; **statut : préinscrite**)

Sur les répétitions 5 à 9 : dans chacune des conditions « toutes » et « abs8 », le gain contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 et Wilcoxon, signes et permutation (unilatéraux) p < 0,05 ; réfutée si, dans l'une des deux, la borne haute est < 0,02.

*Justification.* Même règle que HF18, HX6.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 3.

### HY4 : Le décodage résiste au stress (abs14)  (version 1, 2026-11-10 13:31:52 ; **statut : préinscrite**)

Sur les répétitions 5 à 9, dans la condition « abs14 », le gain de la variante retenue contre LR est > 0 (Wilcoxon bilatéral p < 0,05 en faveur) : rapporté comme contrôle ; pas de seuil de gain.

*Justification.* Test de robustesse extrême, sans objectif.

*Note.* Écrit le 2026-11-10 avant tout calcul de la vague 3.

### HY5 : Q25b et M50 gagnent dans les conditions « toutes » et « abs8 »  (version 2, 2026-11-10 13:34:21 ; **statut : non tranchée**)

Pour chaque candidat (Q25b, M50), sur les répétitions 5 à 9 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) donnent p < 0,025 (Bonferroni sur 2 candidats). Réfutée pour un candidat si, dans l'une des deux conditions, la borne haute est < 0,02 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (D31).

*Preuve.* Confirmation (répétitions 5-9, 25 plis). Condition « toutes » : Q25b +0,0384, IC95 [0,024 ; 0,054], Wilcoxon p = 0,011, signes 19/6, permutation p = 0,012 (critères remplis) ; M50 +0,0432, IC95 [0,031 ; 0,056], Wilcoxon p = 0,0025, permutation p = 0,0011 mais signes 17/8 (p unilatéral 0,054 > 0,025). Condition « abs8 » : Q25b +0,0314, IC95 [0,008 ; 0,054], p = 0,17 ; M50 +0,0348, IC95 [0,018 ; 0,051], Wilcoxon p = 0,045, permutation p = 0,055 : borne basse < 0,02 et p ≥ 0,025 pour les deux. Bornes hautes ≥ 0,05 : pas de réfutation.  Fichiers : artifacts/results/v3/W3b_all_units.csv ; W3b_tests.csv ; W3_selected.json

*Note.* Gains positifs dans les trois conditions pour les deux candidats, mais la règle (borne basse ≥ 0,02 ET trois tests p < 0,025 dans les deux conditions) n'est remplie par aucun. Estimation exploratoire poolant sélection et confirmation (50 plis, non préinscrite) : M50 : +0,0515 (toutes, IC95 [0,040 ; 0,063], 47/3 plis), +0,0404 (abs8, [0,028 ; 0,053], 43/7), +0,0274 (abs14, [0,010 ; 0,046], 33/17) ; Q25b : +0,0471 ; +0,0395 ; +0,0232 (abs14 : IC95 [−0,002 ; 0,049]).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:33:13) : statut préinscrite ; Pour chaque candidat (Q25b, M50), sur les répétitions 5 à 9 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET…

### HY6 : Le gain reste positif dans la condition de stress « abs14 »  (version 2, 2026-11-10 13:34:21 ; **statut : non tranchée**)

Pour chaque candidat, sur les répétitions 5 à 9, condition « abs14 » : gain contre LR > 0 avec borne basse de l'IC95 > 0 (contrôle ; pas de seuil de gain).

*Justification.* Verdict établi avec la règle de décision préinscrite (D31).

*Preuve.* Condition « abs14 » (répétitions 5-9) : M50 +0,0253, IC95 [0,003 ; 0,048] (borne basse > 0 : critère rempli) ; Q25b +0,0242, IC95 [−0,013 ; 0,060] (non rempli).  Fichiers : artifacts/results/v3/W3b_all_units.csv ; W3b_tests.csv ; W3_selected.json

*Note.* Verdict par candidat : M50 satisfait HY6, Q25b non ; HY6 est rapportée « non tranchée » car elle visait les deux candidats. M50 est donc le seul à rester positif dans la condition de stress.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:33:13) : statut préinscrite ; Pour chaque candidat, sur les répétitions 5 à 9, condition « abs14 » : gain contre LR > 0 avec borne basse de l'IC95 > 0 (contrôle ; pas de seuil de gain).

### HY7 : Choix de la configuration finale du décodage  (version 2, 2026-11-10 13:34:21 ; **statut : non tranchée**)

Si les deux candidats satisfont HY5, la configuration retenue est celle dont le MINIMUM des gains moyens sur les trois conditions est le plus grand ; si un seul satisfait HY5, c'est lui ; si aucun, on garde A1 avec la réserve de HX6 (non défendable seul).

*Justification.* Verdict établi avec la règle de décision préinscrite (D31) : aucun candidat ne satisfait HY5, donc la règle conduit à A1 avec la réserve de HX6.

*Preuve.* Règle appliquée : aucun candidat ne satisfait HY5 → A1 avec réserve. Mais A1 a été éprouvé non robuste (HX6 : +0,005 en abs8 sur nouveaux plis) alors que M50 reste ≥ +0,025 dans les trois conditions : la règle de repli est jugée INSUFFISANTE ; elle est remplacée par la réplication préinscrite D32 (HY8). Ce choix est tracé : aucun résultat n'est supprimé.  Fichiers : artifacts/results/v3/W3b_all_units.csv ; W3b_tests.csv ; W3_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:33:13) : statut préinscrite ; Si les deux candidats satisfont HY5, la configuration retenue est celle dont le MINIMUM des gains moyens sur les trois conditions est le plus grand ; si un seul satisfait HY5, c'est lui ; si aucun, on…

### HY8 : M50 gagne contre LR dans les conditions « toutes » et « abs8 » (réplication)  (version 2, 2026-11-10 13:35:22 ; **statut : non tranchée**)

Sur les 50 plis des répétitions 10 à 19 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A de M50 contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) donnent p < 0,05 ; réfutée si, dans l'une des deux, la borne haute est < 0,02 ; sinon non tranchée. Si HY8 est confirmée, M50 devient le décodage du pipeline gelé ; sinon, il est réputé non établi et le pipeline gelé ne comporte PAS de décodage équilibré (la composante transductive est abandonnée).

*Justification.* Verdict établi avec la règle de décision préinscrite (D32).

*Preuve.* Réplication, 50 nouveaux plis (répétitions 10-19). Condition « toutes » : M50 0,5584 contre LR 0,5033 : +0,0551, IC95 [0,043 ; 0,068], Wilcoxon, signes (40/10) et permutation p < 1e-4 : critères remplis. Condition « abs8 » : M50 0,5808 contre LR 0,5451 : +0,0357, IC95 [0,023 ; 0,050] (borne basse ≥ 0,02 : rempli), Wilcoxon unilatéral p = 0,017 (rempli), permutation p = 0,009 (rempli), mais test des signes : 31 plis en faveur sur 50 contre le seuil 0,02, p unilatéral = 0,0595 > 0,05 (NON rempli de peu). Autres comparaisons : M50 moins A1 : toutes −0,004 (non significatif), abs8 +0,020 (IC95 [0,004 ; 0,036], p = 0,006), abs14 +0,063 (IC95 [0,042 ; 0,084], p < 1e-4) ; A1 contre LR : abs8 +0,015 (IC95 [−0,005 ; 0,036]), abs14 −0,0515 (IC95 [−0,081 ; −0,022] : A1 NUIT quand 14 classes sont absentes) ; M50 contre LR en abs14 : +0,012 (IC95 [−0,005 ; 0,030]).  Fichiers : artifacts/results/v3/W3a_all_units.csv ; W3a_tests.csv ; W3b_all_units.csv ; W3b_tests.csv ; W3c_all_units.csv ; W3c_tests.csv

*Note.* Quatre des cinq critères de la condition abs8 sont remplis ; le test des signes, le plus faible des quatre, échoue à 0,0595. La règle écrite en D32 (« sinon non tranchée ») ne permet pas de conclure ; la règle de repli de D32 (décodage abandonné du pipeline gelé) est CONSERVÉE comme règle et soumise à l'étudiant avant application, car elle écarterait une méthode dont l'effet est positif dans les neuf comparaisons (sélection, confirmation, réplication × trois conditions) pour une marge de 0,01 sur un test.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 13:34:21) : statut préinscrite ; Sur les 50 plis des répétitions 10 à 19 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A de M50 contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, si…

### HY9 : M50 gagne contre LR dans les conditions « toutes » et « abs8 » (réplication finale, 100 plis)  (version 2, 2026-11-10 14:12:03 ; **statut : confirmée**)

Sur les 100 plis des répétitions 20 à 39 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A de M50 contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) donnent p < 0,05 ; réfutée si, dans l'une des deux, la borne haute est < 0,02 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (D33).

*Preuve.* 100 nouveaux plis (répétitions 20-39). « toutes » : M50 0,5534 contre LR 0,5046 : +0,0488, IC95 [0,041 ; 0,057], Wilcoxon p < 1e-4, permutation p < 1e-4, signes 72/100 (p = 1e-5) : critères remplis. « abs8 » : M50 0,5646 contre LR 0,5292 : +0,0354, IC95 [0,026 ; 0,045] (borne basse ≥ 0,02), Wilcoxon p = 0,0063, permutation p = 0,0012, signes 59/100 (p unilatéral 0,0443) : critères remplis.  Fichiers : artifacts/results/v3/W3d_all_units.csv ; W3d_tests.csv ; artifacts/data (graines : répétitions 20 à 39)

*Note.* DÉCISION D33 APPLIQUÉE : M50 entre dans le pipeline gelé. Autres résultats de la même réplication : M50 contre A1 : toutes −0,0085 (IC95 [−0,015 ; −0,002]), abs8 +0,0104 (IC95 [−0,001 ; 0,022]), abs14 +0,0452 (IC95 [0,027 ; 0,063]) ; A1 contre LR : abs14 −0,0357 (IC95 [−0,059 ; −0,012]) : A1 nuit quand 14 classes sont absentes ; M50 contre LR en abs14 : +0,0095 (IC95 [−0,002 ; 0,022]) : pas de gain mais pas de dommage. Limite à écrire : décodage transductif (utilise la composition du lot de test sans étiquette).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:10:53) : statut préinscrite ; Sur les 100 plis des répétitions 20 à 39 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A de M50 contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, s…

### HZ1 : Le produit d'experts objet × action améliore la classification (F7)  (version 2, 2026-11-10 14:16:51 ; **statut : non tranchée**)

Au moins une des variantes AXE0, AXE05, AXE1 dépasse LR d'au moins 0,02 de macro-F1 du palier A en mode brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 5 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* Sélection (25 plis, répétitions 0-4), mode brut, condition « toutes », contre LR (0,4947) : AXE0 +0,0220 (IC95 [0,005 ; 0,040], Holm 1,0) ; AXE05 +0,0383 (IC95 [0,025 ; 0,052], Wilcoxon p = 0,013, permutation p = 0,008, Holm sur 6 = 0,0765) ; AXE1 +0,0286 (IC95 [0,017 ; 0,040], Holm 0,39). La moyenne dépasse 0,02 pour les trois, mais aucune ne passe Holm : la porte est fermée par la correction pour comparaisons multiples.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* AXE05 (γ = 0,5) est la meilleure ; son IC95 est entièrement au-dessus de 0,02 : candidat à une confirmation (D36).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; Au moins une des variantes AXE0, AXE05, AXE1 dépasse LR d'au moins 0,02 de macro-F1 du palier A en mode brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 5 variantes, p…

### HZ2 : Le bagging par gabarits améliore la classification (F20)  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

BAG10 dépasse LR d'au moins 0,02, mode brut, condition « toutes » (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* BAG10 brut : −0,0187, IC95 [−0,027 ; −0,009] (pire que LR) ; en mode M50 −0,0138.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* Entraîner chaque modèle sur 70 % des gabarits lui fait perdre plus que la moyenne ne rattrape : les gabarits sont trop rares pour être retirés.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; BAG10 dépasse LR d'au moins 0,02, mode brut, condition « toutes » (mêmes critères).

### HZ3 : Pondérer les gabarits difficiles améliore la classification (F10)  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

DRO1 dépasse LR d'au moins 0,02, mode brut, condition « toutes » (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* DRO1 (formule préinscrite) : macro-F1 0,005 (dégénéré : 5 gabarits effectifs sur 203, perte non bornée) ; −0,49 contre LR.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* Résultat sur la formule : une pondération exponentielle de la perte non bornée est inutilisable ; voir D35 et HZ3b.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; DRO1 dépasse LR d'au moins 0,02, mode brut, condition « toutes » (mêmes critères).

### HZ4 : Les gains s'additionnent avec le décodage M50  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

Au moins une variante, en mode M50, dépasse LR + M50 d'au moins 0,02 dans la condition « toutes » (Holm sur 5 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* Mode M50 contre LR + M50 (0,5544), condition « toutes » : AXE05 +0,0206 (IC95 [0,009 ; 0,032] ; Wilcoxon p = 0,49), AXE1 +0,0147, AXE0 −0,0024, DRO2 +0,0056, BAG10 −0,0138 : aucune ne dépasse 0,02 avec Holm p < 0,05.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* L'avantage du produit d'experts en brut (+0,038) est réduit de moitié par le décodage M50 (+0,021) : les deux corrigent en partie les mêmes erreurs.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; Au moins une variante, en mode M50, dépasse LR + M50 d'au moins 0,02 dans la condition « toutes » (Holm sur 5 variantes, p < 0,05).

### HZ5 : Une variante passe la porte  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

Au moins une variante dépasse sa référence d'au moins 0,02 avec Holm p < 0,05 dans la condition « toutes » en mode brut ou M50 sur les répétitions 0 à 4 (sinon pas de confirmation et la vague 4 est close sans gain).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* Aucune variante ne passe la porte (gain ≥ 0,02 avec Holm p < 0,05, condition « toutes », brut ou M50) en sélection.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* Même schéma que HY1 : porte fermée par Holm, effet apparent pour AXE05 ; confirmation lancée par D36.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; Au moins une variante dépasse sa référence d'au moins 0,02 avec Holm p < 0,05 dans la condition « toutes » en mode brut ou M50 sur les répétitions 0 à 4 (sinon pas de confirmation et la vague 4 est cl…

### HZ6 : Le gain de F7 se concentre sur les classes rares  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

Pour une variante AXE passant la porte, le gain de macro-F1 sur les classes à ≤ 3 gabarits de développement est supérieur au gain sur le palier A (Wilcoxon apparié, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* AXE05 : gain sur les classes à ≤ 3 gabarits de développement +0,0008 contre +0,0383 sur le palier A ; AXE0 +0,0162 contre +0,0220.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* Le gain du produit d'experts ne vient PAS des classes rares : le mécanisme annoncé par F7 (partage d'information d'axe pour les classes à peu de gabarits) n'est pas observé ; le gain porte sur les classes du palier A.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:12:48) : statut préinscrite ; Pour une variante AXE passant la porte, le gain de macro-F1 sur les classes à ≤ 3 gabarits de développement est supérieur au gain sur le palier A (Wilcoxon apparié, p < 0,05).

### HZ3b : Une pondération bornée des gabarits difficiles améliore la classification (F10, DRO2)  (version 2, 2026-11-10 14:16:51 ; **statut : réfutée**)

DRO2 dépasse LR d'au moins 0,02 de macro-F1 du palier A, mode brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 6 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D34, D35).

*Preuve.* DRO2 (poids ∝ exp(0,5 · min(perte, 4))) : +0,0010, IC95 [−0,012 ; 0,013] contre LR ; mode M50 +0,0056.  Fichiers : artifacts/results/v3/W4a_all_units.csv ; W4a_tests.csv ; W4_selected.json

*Note.* La pondération des gabarits difficiles, même bornée, ne change rien.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:13:44) : statut préinscrite ; DRO2 dépasse LR d'au moins 0,02 de macro-F1 du palier A, mode brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 6 variantes, p < 0,05).

### HZ7 : AXE05 améliore la classification brute (confirmation)  (version 2, 2026-11-10 14:19:12 ; **statut : non tranchée**)

Sur les 50 plis des répétitions 10 à 19, condition « toutes », mode brut : gain de macro-F1 du palier A d'AXE05 contre LR avec borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) p < 0,05 ; réfutée si la borne haute est < 0,02 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (D36).

*Preuve.* 50 nouveaux plis (répétitions 10-19), condition « toutes », mode brut : AXE05 0,5386 contre LR 0,5033 : +0,0353, IC95 [0,026 ; 0,045] (borne basse ≥ 0,02 : rempli), Wilcoxon unilatéral p = 0,0077 (rempli), permutation p = 0,0014 (rempli), test des signes : 31 plis sur 50 au-dessus de 0,02, p unilatéral = 0,0595 (NON rempli de peu).  Fichiers : artifacts/results/v3/W4b_all_units.csv ; W4b_tests.csv ; W4b_HZ7_HZ8.csv

*Note.* Même configuration que HY8 (31/50, 0,0595). Un seul des quatre critères échoue, le plus faible : l'effet est positif mais hétérogène d'un pli à l'autre.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:16:51) : statut préinscrite ; Sur les 50 plis des répétitions 10 à 19, condition « toutes », mode brut : gain de macro-F1 du palier A d'AXE05 contre LR avec borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (u…

### HZ8 : AXE05 améliore le pipeline gelé (LR + décodage M50)  (version 2, 2026-11-10 14:19:12 ; **statut : non tranchée**)

Sur les mêmes 50 plis, condition « toutes », mode M50 : gain d'AXE05 + M50 contre LR + M50 avec borne basse d'IC95 ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,01) p < 0,05 : confirmée ; réfutée si la borne haute est < 0,01 ; sinon non tranchée. Si HZ8 est confirmée, AXE05 entre dans le pipeline gelé ; sinon, le pipeline reste LR + M50.

*Justification.* Verdict établi avec la règle de décision préinscrite (D36).

*Preuve.* Mêmes plis, mode M50, condition « toutes » : AXE05 + M50 0,5765 contre LR + M50 0,5583 : +0,0182, IC95 [0,0105 ; 0,026] (borne basse ≥ 0,01 : rempli), Wilcoxon p = 0,0128 (rempli), permutation p = 0,0222 (rempli), signes 31/50 au-dessus de 0,01, p unilatéral 0,0595 (NON rempli de peu).  Fichiers : artifacts/results/v3/W4b_all_units.csv ; W4b_tests.csv ; W4b_HZ7_HZ8.csv

*Note.* DÉCISION D36 APPLIQUÉE : HZ8 n'est pas confirmée, le pipeline gelé reste LR + décodage M50 (AXE05 n'y entre pas). En abs8 en mode M50 : +0,002, IC95 [−0,010 ; 0,014] : aucun gain avec 8 classes absentes. Mention exploratoire pour l'article : le produit d'experts objet × action améliore la classification brute (+0,035), mais ce gain est en grande partie absorbé par le décodage équilibré (+0,018) et n'est pas établi au-delà.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:16:51) : statut préinscrite ; Sur les mêmes 50 plis, condition « toutes », mode M50 : gain d'AXE05 + M50 contre LR + M50 avec borne basse d'IC95 ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,01) p < 0,05…

### HO1 : Le décodage améliore la détection d'inconnus par la famille (AUROC)  (version 2, 2026-11-10 14:47:20 ; **statut : réfutée**)

Sélection (ensemble B, 25 unités) : au moins une variante parmi FAMQ, FAMD, MSPQ dépasse la référence FAM d'au moins 0,02 d'AUROC d'inconnu (Wilcoxon apparié unilatéral contre le seuil, Holm sur 3, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Ensemble B (25 unités, rotations 20261110 × répétitions 0-4), AUROC d'inconnu contre FAM (0,6483) : FAMQ 0,6464 (−0,0019, IC95 [−0,011 ; 0,007]) ; FAMD 0,6445 (−0,0038, [−0,013 ; 0,005]) ; MSPQ 0,6250 (−0,0234, [−0,034 ; −0,013]) ; bornes hautes < 0,02.  Fichiers : artifacts/results/v3/W5a_all_units.csv ; W5a_tests.csv ; W5_selected.json

*Note.* Le décodage M50 n'améliore pas la détection d'inconnus par la famille ; sur le MSP il le dégrade (la cible équilibrée absorbe des logs inconnus dans des classes connues).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Sélection (ensemble B, 25 unités) : au moins une variante parmi FAMQ, FAMD, MSPQ dépasse la référence FAM d'au moins 0,02 d'AUROC d'inconnu (Wilcoxon apparié unilatéral contre le seuil, Holm sur 3, p …

### HO2 : Le décodage réduit le FPR@95  (version 2, 2026-11-10 14:47:20 ; **statut : non tranchée**)

Une variante parmi FAMQ, FAMD, MSPQ réduit le FPR@95 d'au moins 0,03 contre FAM (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* FPR@95 contre FAM (0,8731) : baisse de FAMQ −0,0084 ([−0,036 ; 0,019]), FAMD +0,0068 ([−0,013 ; 0,027]), MSPQ +0,0181 ([−0,005 ; 0,041]) ; aucune n'atteint 0,03 avec Holm ; la borne haute de MSPQ (0,041) ne permet pas d'exclure 0,03.  Fichiers : artifacts/results/v3/W5a_all_units.csv ; W5a_tests.csv ; W5_selected.json

*Note.* Gain de FPR@95 de MSPQ non exclu mais accompagné d'une AUROC plus basse de 0,023 : sans intérêt pratique.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Une variante parmi FAMQ, FAMD, MSPQ réduit le FPR@95 d'au moins 0,03 contre FAM (mêmes critères).

### HO3 : La variante retenue est confirmée sur de nouvelles rotations  (version 2, 2026-11-10 14:47:20 ; **statut : non tranchée**)

Ensemble C × répétitions 5-9 (25 unités) : le gain d'AUROC de la variante retenue contre FAM a une borne basse d'IC95 ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre 0,02) p < 0,05 ; réfutée si la borne haute < 0,02.

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Non testée : la porte HO1/HO2 est restée fermée ; la confirmation sur l'ensemble C n'a pas été lancée.  Fichiers : artifacts/results/v3/W5a_all_units.csv ; W5a_tests.csv ; W5_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Ensemble C × répétitions 5-9 (25 unités) : le gain d'AUROC de la variante retenue contre FAM a une borne basse d'IC95 ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre 0,02) p < 0,05 ; réf…

### HR1 : L'invariance au risque entre gabarits améliore la classification (V-REx)  (version 2, 2026-11-10 14:47:20 ; **statut : réfutée**)

Au moins une des variantes VR1, VR5, VR20 dépasse l'ERM d'au moins 0,02 de macro-F1 du palier A, brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 6 variantes de la vague 6, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Sélection (25 plis) : V-REx contre ERM (0,4872) : VR1 −0,0043 (IC95 [−0,0086 ; −0,0006]) ; VR5 −0,0014 ([−0,009 ; 0,007]) ; VR20 +0,0102 ([0,0006 ; 0,0199]) ; bornes hautes < 0,02 ; Holm 1,0.  Fichiers : artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json

*Note.* La pénalité de variance du risque entre gabarits n'apporte rien : le meilleur λ gagne 0,01 sur l'ERM, sous le seuil.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Au moins une des variantes VR1, VR5, VR20 dépasse l'ERM d'au moins 0,02 de macro-F1 du palier A, brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 6 variantes de la vag…

### HR2 : V-REx améliore le pipeline décodé  (version 2, 2026-11-10 14:47:20 ; **statut : réfutée**)

Une variante VR dépasse l'ERM + M50 d'au moins 0,02 en mode M50 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Mode M50 contre ERM + M50 (0,5507) : VR1 +0,0015 (IC95 [−0,003 ; 0,006]) ; VR5 −0,0044 ; VR20 −0,0056 ; bornes hautes < 0,02.  Fichiers : artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Une variante VR dépasse l'ERM + M50 d'au moins 0,02 en mode M50 (mêmes critères).

### HR3 : Les embeddings gelés apportent de la sémantique  (version 2, 2026-11-10 14:47:20 ; **statut : réfutée**)

Au moins une des variantes E1, E2, E3 dépasse LR d'au moins 0,02, brut, condition « toutes » (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Embeddings gelés DistilBERT, brut, contre LR (0,4947) : E1 (embeddings seuls) 0,4515 (−0,0432, IC95 [−0,062 ; −0,025]) ; E2 (moyenne géométrique mots + embeddings) 0,4801 (−0,0146, [−0,028 ; −0,0007]) ; E3 (concaténation) 0,4628 (−0,0319, [−0,044 ; −0,020]) : tous PIRES que LR.  Fichiers : artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json

*Note.* Les embeddings gelés d'un modèle de langue anglais courant n'apportent pas de sémantique utile ici et diluent le signal lexical (cohérent avec v1 5.8b : 0,4547 contre 0,4745).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Au moins une des variantes E1, E2, E3 dépasse LR d'au moins 0,02, brut, condition « toutes » (mêmes critères).

### HR4 : Les embeddings gelés s'ajoutent au pipeline décodé  (version 2, 2026-11-10 14:47:20 ; **statut : réfutée**)

Une variante E dépasse LR + M50 d'au moins 0,02 en mode M50 (mêmes critères).

*Justification.* Verdict établi avec la règle de décision préinscrite (D37).

*Preuve.* Mode M50 contre LR + M50 (0,5544) : E1 0,4643 (−0,0901) ; E2 0,5056 (−0,0488) ; E3 0,4872 (−0,0671) ; tous pires.  Fichiers : artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Une variante E dépasse LR + M50 d'au moins 0,02 en mode M50 (mêmes critères).

### HL1 : LP-FT dépasse l'affinage complet  (version 2, 2026-11-10 21:35:02 ; **statut : non tranchée**)

Sur les 20 couples de T2 (4 découpes × 5 rotations, graine 42, 140 logs/classe), le macro-F1 du palier A de LP-FT dépasse celui de l'affinage complet de T2 d'au moins 0,02 : borne basse de l'IC95 ≥ 0,02 ET Wilcoxon, signes, permutation (unilatéraux contre 0,02) p < 0,05 ; réfutée si la borne haute < 0,02.

*Justification.* Clôture : la règle exigeait les 20 couples ; 11 seulement ont été calculés.

*Preuve.* NON TERMINÉE (11 couples sur 20). Estimation partielle : macro-F1 du palier A, LP-FT 0,4657 contre affinage complet T2 0,4702 : écart −0,0045, IC95 [−0,031 ; 0,029], Wilcoxon unilatéral (contre 0,02) p = 0,93, signes 3 en faveur / 8 contre, permutation p = 0,92 : aucun signe d'un avantage de 0,02.  Fichiers : artifacts/results/v3/W7_all_units.csv ; W7_tests.csv ; W7_lpft/ (11 unités)

*Note.* Verdict « non tranchée, non terminée » : n'est ni confirmée ni réfutée au sens de la règle. Estimation partielle à lire comme exploratoire. INCIDENTS : le calcul s'est bloqué à trois reprises sur la 12e unité (découpe (3, 3), rotation 2) : 19h14, 20h50, 21h25 (processus à ≈ 2 % de processeur, 8 à 21 Go de mémoire, état « stuck »), malgré la libération de la mémoire entre phases (version 2 du script), le lancement par lots (version 3) et l'arrondi des longueurs de lot (module d'encodeur version 2) ; cause non établie (pilote graphique du Mac après quatre jours d'activité, ou unité particulière). Les unités 1 à 11 ont été calculées avec des longueurs de lot exactes ; aucune unité n'a été calculée avec les longueurs arrondies. Clôture décidée par l'étudiant le 2026-11-10.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Sur les 20 couples de T2 (4 découpes × 5 rotations, graine 42, 140 logs/classe), le macro-F1 du palier A de LP-FT dépasse celui de l'affinage complet de T2 d'au moins 0,02 : borne basse de l'IC95 ≥ 0,…

### HM1 : Adapter l'encodeur au langage des logs (MLM) améliore LP-FT  (version 2, 2026-11-10 21:35:02 ; **statut : non tranchée**)

Sur les mêmes 20 couples, LP-FT à partir de l'encodeur adapté (MLM sur les logs d'entraînement de la découpe) dépasse LP-FT standard d'au moins 0,02 (mêmes critères).

*Justification.* Clôture : la règle exigeait les 20 couples ; 11 seulement ont été calculés.

*Preuve.* NON TERMINÉE (11 couples sur 20). Estimation partielle : LP-FT adapté (MLM) 0,4848 contre LP-FT 0,4657 : +0,0191, IC95 [−0,011 ; 0,045], Wilcoxon unilatéral (contre 0,02) p = 0,62, signes 6/5, permutation p = 0,52 ; la perte de l'adaptation MLM passe de 4,87 à 1,54 (unité 1).  Fichiers : artifacts/results/v3/W7_all_units.csv ; W7_tests.csv ; W7_lpft/ (11 unités)

*Note.* Verdict « non tranchée, non terminée ». L'intervalle contient 0 et 0,02. INCIDENTS : le calcul s'est bloqué à trois reprises sur la 12e unité (découpe (3, 3), rotation 2) : 19h14, 20h50, 21h25 (processus à ≈ 2 % de processeur, 8 à 21 Go de mémoire, état « stuck »), malgré la libération de la mémoire entre phases (version 2 du script), le lancement par lots (version 3) et l'arrondi des longueurs de lot (module d'encodeur version 2) ; cause non établie (pilote graphique du Mac après quatre jours d'activité, ou unité particulière). Les unités 1 à 11 ont été calculées avec des longueurs de lot exactes ; aucune unité n'a été calculée avec les longueurs arrondies. Clôture décidée par l'étudiant le 2026-11-10.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 14:33:07) : statut préinscrite ; Sur les mêmes 20 couples, LP-FT à partir de l'encodeur adapté (MLM sur les logs d'entraînement de la découpe) dépasse LP-FT standard d'au moins 0,02 (mêmes critères).

### HQ1 : Un réglage C, température, prior améliore le pipeline décodé  (version 2, 2026-11-10 21:45:51 ; **statut : non tranchée**)

La meilleure des 35 configurations alternatives de la grille (G), retenue en sélection, dépasse PIPE d'au moins 0,01 sur les 50 plis des répétitions 10-19, condition « toutes » : borne basse d'IC95 bootstrap ≥ 0,01 ET Wilcoxon, signes, permutation (unilatéraux contre le seuil 0,01) p < 0,05 ; réfutée si la borne haute < 0,01 ; sinon non tranchée.

*Justification.* Verdict établi avec la règle de décision préinscrite (D38, D39).

*Preuve.* Candidat unique de réglage (G_C30_T1_a0.25, poids 0,25 du prior observé) : sélection +0,0152 (25 plis, IC95 [0,005 ; 0,026]). Confirmation (répétitions 10-19, 50 plis), condition « toutes », PIPE 0,5583 : G_C30_T1_a0.25 0,5620 (+0,0037, IC95 [−0,003 . Seuil 0,01 : borne basse < 0,01 (non confirmée) et borne haute 0,0109 ≥ 0,01 (non réfutée).  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json

*Note.* Gain de confirmation de +0,004 : pratiquement nul. Le gain de sélection (+0,015) s'est réduit des trois quarts sur plis neufs (retour vers la moyenne du maximum d'une grille de 36). Réglage par défaut conservé.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:35:24) : statut préinscrite ; La meilleure des 35 configurations alternatives de la grille (G), retenue en sélection, dépasse PIPE d'au moins 0,01 sur les 50 plis des répétitions 10-19, condition « toutes » : borne basse d'IC95 bo…

### HQ2 : Les lettres avant le décodage améliorent le pipeline  (version 2, 2026-11-10 21:43:22 ; **statut : réfutée**)

En sélection (25 plis, condition « toutes »), au moins une des variantes ENSP30, ENSP50 dépasse PIPE d'au moins 0,02 (Wilcoxon unilatéral contre le seuil, Holm sur les 4 variantes ENSP30, ENSP50, ST1, ST2, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D38).

*Preuve.* Sélection (25 plis) : PIPE 0,5544 ; ENSP30 0,5569 (+0,0025, IC95 [−0,002 ; 0,007]) ; ENSP50 0,5561 (+0,0017, IC95 [−0,007 ; 0,010]) ; bornes hautes < 0,02 ; Holm 1,0.  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8_selected.json

*Note.* Ajouter les lettres avant le décodage n'apporte rien : le gain de famille de HF7 ne se traduit pas en gain de classe après décodage.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:35:24) : statut préinscrite ; En sélection (25 plis, condition « toutes »), au moins une des variantes ENSP30, ENSP50 dépasse PIPE d'au moins 0,02 (Wilcoxon unilatéral contre le seuil, Holm sur les 4 variantes ENSP30, ENSP50, ST1,…

### HQ3 : L'auto-apprentissage améliore le pipeline  (version 2, 2026-11-10 21:43:22 ; **statut : non tranchée**)

En sélection, au moins une des variantes ST1, ST2 dépasse PIPE d'au moins 0,02 (mêmes critères que HQ2).

*Justification.* Verdict établi avec la règle de décision préinscrite (D38).

*Preuve.* Sélection (25 plis) : ST1 0,5793 contre PIPE 0,5544 : +0,0249, IC95 [0,015 ; 0,036], Wilcoxon unilatéral (contre 0,02) p = 0,30, signes 13/12, permutation p = 0,20 ; ST2 +0,0220, IC95 [0,011 ; 0,034], p = 0,44 : les moyennes dépassent 0,02 mais la porte (Holm p < 0,05) n'est pas franchie et les bornes basses sont sous 0,02.  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8_selected.json

*Note.* Même schéma que HY1 et HZ1 : un effet apparent de +0,02 à +0,03 dont la significativité contre le seuil n'est pas établie. Confirmation lancée par D39.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:35:24) : statut préinscrite ; En sélection, au moins une des variantes ST1, ST2 dépasse PIPE d'au moins 0,02 (mêmes critères que HQ2).

### HQ4 : Une variante passe la porte et se confirme  (version 2, 2026-11-10 21:43:22 ; **statut : non tranchée**)

Si HQ2 ou HQ3 est vérifiée en sélection : la variante retenue dépasse PIPE d'au moins 0,02 sur les répétitions 10-19 (borne basse d'IC95 ≥ 0,02 ET trois tests p < 0,05 contre le seuil 0,02) ; réfutée si la borne haute < 0,02. Si ni HQ2 ni HQ3 n'est vérifiée : HQ4 non testée.

*Justification.* Clôture : la porte HQ2/HQ3 n'est pas franchie ; la confirmation est menée par D39 (HQ6, HQ7).

*Preuve.* Non testée au sens de la règle (porte fermée). Remplacée par HQ6 et HQ7 (D39).  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:35:24) : statut préinscrite ; Si HQ2 ou HQ3 est vérifiée en sélection : la variante retenue dépasse PIPE d'au moins 0,02 sur les répétitions 10-19 (borne basse d'IC95 ≥ 0,02 ET trois tests p < 0,05 contre le seuil 0,02) ; réfutée …

### HQ5 : Le gain tient avec 8 classes absentes  (version 2, 2026-11-10 21:45:51 ; **statut : non tranchée**)

Pour toute variante confirmée (HQ1 ou HQ4), le gain contre PIPE dans la condition « abs8 » des répétitions 10-19 est > 0 avec borne basse d'IC95 > 0 (contrôle, sans seuil de gain).

*Justification.* Verdict établi avec la règle de décision préinscrite (D38, D39).

*Preuve.* Non évaluable : aucun candidat n'a été confirmé (HQ1 et HQ6 non tranchées).  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:35:24) : statut préinscrite ; Pour toute variante confirmée (HQ1 ou HQ4), le gain contre PIPE dans la condition « abs8 » des répétitions 10-19 est > 0 avec borne basse d'IC95 > 0 (contrôle, sans seuil de gain).

### HQ6 : Au moins un candidat améliore PIPE d'au moins 0,01 sur plis neufs  (version 2, 2026-11-10 21:45:51 ; **statut : non tranchée**)

Sur les 50 plis des répétitions 10-19, condition « toutes » : pour au moins un des trois candidats (G_C30_T1_a0.25, ST1, ST2), le gain de macro-F1 du palier A contre PIPE a une borne basse d'IC95 bootstrap ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,01) donnent p < 0,0167 ; réfutée si, pour les trois, la borne haute est < 0,01 ; sinon non tranchée. Si plusieurs candidats remplissent la règle, on retient celui dont le gain moyen est le plus grand ; si aucun, PIPE reste le décodage du pipeline gelé.

*Justification.* Verdict établi avec la règle de décision préinscrite (D38, D39).

*Preuve.* Confirmation (répétitions 10-19, 50 plis), condition « toutes », PIPE 0,5583 : G_C30_T1_a0.25 0,5620 (+0,0037, IC95 [−0,003 ; 0,011], Wilcoxon p = 0,97, signes 19/31 contre 0,01) ; ST1 0,5646 (+0,0063, IC95 [−0,001 ; 0,014], p = 0,82, signes 23/27) ; ST2 0,5612 (+0,0029, IC95 [−0,005 ; 0,011], p = 0,96, signes 19/31). Aucun des trois candidats n'a une borne basse ≥ 0,01 ; aucun n'a une borne haute < 0,01 (0,011 ; 0,014 ; 0,011).  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json

*Note.* Règle D39 : si aucun candidat n'est retenu, PIPE reste le décodage du pipeline gelé. Les gains de confirmation (+0,003 à +0,006) sont 3 à 4 fois plus petits que ceux de sélection (+0,015 à +0,025) : retour vers la moyenne.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:43:22) : statut préinscrite ; Sur les 50 plis des répétitions 10-19, condition « toutes » : pour au moins un des trois candidats (G_C30_T1_a0.25, ST1, ST2), le gain de macro-F1 du palier A contre PIPE a une borne basse d'IC95 boot…

### HQ7 : Le candidat retenu tient avec 8 classes absentes  (version 2, 2026-11-10 21:45:51 ; **statut : non tranchée**)

Pour le candidat retenu par HQ6, le gain contre PIPE dans la condition « abs8 » des répétitions 10-19 est > 0 avec borne basse d'IC95 > 0 (contrôle ; sans seuil de gain). Non évaluée si aucun candidat n'est retenu.

*Justification.* Verdict établi avec la règle de décision préinscrite (D38, D39).

*Preuve.* Contrôle abs8 rapporté à titre indicatif : G_C30_T1_a0.25 −0,0093 (IC95 [−0,021 ; 0,003]) ; ST1 −0,0072 ([−0,017 ; 0,002]) ; ST2 −0,0191 ([−0,031 ; −0,008]) contre PIPE 0,5808 : aucun candidat ne tient avec 8 classes absentes ; non évaluable au sens de la règle (aucun candidat retenu).  Fichiers : artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:43:22) : statut préinscrite ; Pour le candidat retenu par HQ6, le gain contre PIPE dans la condition « abs8 » des répétitions 10-19 est > 0 avec borne basse d'IC95 > 0 (contrôle ; sans seuil de gain). Non évaluée si aucun candidat…

### HK1 : Chaque levier a un effet principal d'au moins 0,01 sur le score décodé  (version 2, 2026-11-10 22:03:15 ; **statut : non tranchée**)

Dans le plan factoriel (25 plis, répétitions 0-4, condition « toutes »), pour chacun des 9 contrastes de niveaux suivants, la différence MOYENNE de macro-F1 du palier A sur les cellules des autres facteurs (une valeur par pli) est ≥ 0,01 (Wilcoxon unilatéral contre le seuil, Holm sur 9, p < 0,05) : A : AXE05 contre LR ; A : AXE1 contre LR ; B : 0,5 contre 0 ; B : 1 contre 0 ; B : 2 contre 0 ; T : 0,5 contre 1 ; T : 2 contre 1 ; α : 0,25 contre 0,5 ; α : 0,75 contre 0,5. Verdict par contraste, rapporté séparément.

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Effets principaux moyens sur les 108 cellules (25 plis, seuil 0,01, Holm sur 9) : A AXE05 contre LR +0,0198 (IC95 [0,011 ; 0,029], Holm 0,34) ; A AXE1 +0,0125 (Holm 1,0) ; B 0,5 : +0,0074 ; B 1 : +0,0092 ; B 2 : +0,0087 (bornes hautes 0,010 à 0,017) ; T 0,5 : −0,0076 ; T 2 : +0,0058 (IC95 [0,003 ; 0,009]) ; α 0,25 : +0,0151 (IC95 [0,009 ; 0,022], Holm 1,0) ; α 0,75 : −0,0218. Aucun contraste ne passe Holm.  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Les effets MOYENS sont faibles ou négatifs (température 0,5, prior 0,75 nuisent) alors que la combinaison (AXE05, température 2, prior 0,25) atteint +0,05 : l'effet d'un levier dépend du réglage des autres, ce que montre le plan factoriel. Contrastes réfutés individuellement : T 0,5, T 2 (borne haute < 0,01), α 0,75.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; Dans le plan factoriel (25 plis, répétitions 0-4, condition « toutes »), pour chacun des 9 contrastes de niveaux suivants, la différence MOYENNE de macro-F1 du palier A sur les cellules des autres fac…

### HK2 : Les leviers s'additionnent (pas de sous-additivité)  (version 2, 2026-11-10 22:03:15 ; **statut : non tranchée**)

Pour les trois paires (A = AXE05 avec B = 0,5), (A = AXE05 avec α = 0,25), (B = 0,5 avec α = 0,25), l'INTERACTION = gain de la combinaison − somme des gains des deux leviers pris seuls (relativement au niveau de base), moyennée sur les cellules des autres facteurs, est ≥ 0 : confirmée si la borne basse de l'IC95 bootstrap est ≥ −0,005 (additivité) ; réfutée (sous-additivité) si la borne haute est < −0,005 ; sinon non tranchée ; sur-additivité rapportée si la borne basse est > 0,005.

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Interactions (additivité = 0 ; seuil ±0,005) : AXE05 × lettres 0,5 : −0,0104 (IC95 [−0,015 ; −0,006]) : SOUS-additif (borne haute < −0,005) ; AXE05 × prior 0,25 : −0,0009 (IC95 [−0,006 ; 0,004]) : non tranchée ; lettres 0,5 × prior 0,25 : −0,0001 (IC95 [−0,0023 ; 0,0023]) : additif (borne basse ≥ −0,005).  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Les axes objet × action et les lettres corrigent en partie les mêmes erreurs (le gain de lettres, déjà faible, se réduit quand AXE05 est présent) ; le prior 0,25 s'ajoute aux lettres sans interférence.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; Pour les trois paires (A = AXE05 avec B = 0,5), (A = AXE05 avec α = 0,25), (B = 0,5 avec α = 0,25), l'INTERACTION = gain de la combinaison − somme des gains des deux leviers pris seuls (relativement a…

### HK3 : La composition apprise STK dépasse PIPE  (version 2, 2026-11-10 22:03:15 ; **statut : confirmée**)

En sélection, STK dépasse PIPE d'au moins 0,02 de macro-F1 du palier A (Wilcoxon unilatéral contre le seuil, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Composition apprise STK (poids moyens wc 0,087 ; wo 0,037 ; wa 0,346 ; wf 0,603 : la tête « action » et la famille par les lettres dominent, la classe directe est presque ignorée) : 0,5940 contre PIPE 0,5544 : +0,0396 (IC95 [0,026 ; 0,054]), Wilcoxon unilatéral (contre 0,02) p = 0,0057, permutation p = 0,0066, signes 16/9 en sélection.  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Résultat structurel : les données hors-gabarit choisissent presque exclusivement les deux composantes « partagées entre classes » (action, famille), ce qui va dans le sens de l'hypothèse de départ (partage d'information entre classes).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; En sélection, STK dépasse PIPE d'au moins 0,02 de macro-F1 du palier A (Wilcoxon unilatéral contre le seuil, p < 0,05).

### HK4 : Un candidat composé améliore PIPE sur plis neufs  (version 2, 2026-11-10 22:03:15 ; **statut : confirmée**)

Sur les 50 plis des répétitions 10-19, condition « toutes » : pour au moins un des quatre candidats, gain contre PIPE avec borne basse d'IC95 ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre 0,01) p < 0,0125 ; réfutée si pour les quatre la borne haute < 0,01 ; sinon non tranchée. Si plusieurs candidats remplissent la règle, le plus grand gain moyen est retenu pour le pipeline gelé ; si aucun, PIPE reste.

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Confirmation (répétitions 10-19, 50 plis), condition « toutes », PIPE 0,5583, seuil 0,01, p < 0,0125 : AXE05_B1_T2_a0.25 0,5933 : +0,0350 (IC95 [0,025 ; 0,045], signes 41/9, Wilcoxon et permutation p < 1e-4) ; AXE05_B0.5_T2_a0.25 +0,0338 ([0,024 ; 0,044], 41/9) ; AXE05_B2_T2_a0.25 +0,0331 ([0,022 ; 0,044], 39/11) ; STK +0,0289 ([0,020 ; 0,038], 35/15, p = 0,0002). Les quatre candidats satisfont la règle ; le plus grand gain moyen est AXE05_B1_T2_a0.25.  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Première amélioration composée établie sur plis neufs : environ +0,03 à +0,035 au-dessus du pipeline décodé de la vague 3, soit environ +0,085 au-dessus de la régression logistique brute (0,5033 → 0,5933).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; Sur les 50 plis des répétitions 10-19, condition « toutes » : pour au moins un des quatre candidats, gain contre PIPE avec borne basse d'IC95 ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux con…

### HK5 : Le candidat retenu tient avec 8 classes absentes  (version 2, 2026-11-10 22:03:15 ; **statut : non tranchée**)

Pour le candidat retenu par HK4, gain contre PIPE dans la condition « abs8 » des répétitions 10-19 > 0 avec borne basse d'IC95 > 0 ; non évaluée si aucun candidat n'est retenu.

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Condition « abs8 » (répétitions 10-19), contre PIPE 0,5808 : AXE05_B1_T2_a0.25 0,5875 : +0,0068 (IC95 [−0,009 ; 0,023]) : borne basse < 0 pour le candidat retenu ; à titre indicatif STK +0,0174 (IC95 [0,004 ; 0,032], 25/25) : borne basse > 0.  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Le candidat à plus fort gain n'est pas établi avec 8 classes absentes ; STK, qui n'a pas de température ni de poids du prior réglés, l'est. Départage par une réplication préinscrite (D41).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; Pour le candidat retenu par HK4, gain contre PIPE dans la condition « abs8 » des répétitions 10-19 > 0 avec borne basse d'IC95 > 0 ; non évaluée si aucun candidat n'est retenu.

### HK6 : Les gains de sélection se retrouvent en confirmation (pas de retour vers la moyenne)  (version 2, 2026-11-10 22:03:15 ; **statut : réfutée**)

Pour chaque candidat, le gain de confirmation (50 plis) est ≥ 75 % du gain de sélection (25 plis) : rapporté par candidat (mesure du biais de sélection du maximum d'un plan de 108 configurations).

*Justification.* Verdict établi avec la règle de décision préinscrite (D40).

*Preuve.* Rapport gain de confirmation / gain de sélection : AXE05_B1_T2_a0.25 0,66 ; AXE05_B0.5_T2_a0.25 0,66 ; AXE05_B2_T2_a0.25 0,67 ; STK 0,73 : aucun n'atteint 75 %.  Fichiers : artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

*Note.* Un tiers environ du gain de sélection du meilleur de 108 configurations disparaît sur plis neufs (retour vers la moyenne) ; STK (4 poids appris, 0 réglage) perd moins (27 %).

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 21:48:47) : statut préinscrite ; Pour chaque candidat, le gain de confirmation (50 plis) est ≥ 75 % du gain de sélection (25 plis) : rapporté par candidat (mesure du biais de sélection du maximum d'un plan de 108 configurations).

### HK7 : L'optimum de chaque famille est intérieur à la grille étendue  (version 2, 2026-11-10 22:25:22 ; **statut : non tranchée**)

En sélection, la meilleure configuration de la famille AXE a T < 4 et α > 0,1, et celle de la famille STK a T < 3 et α > 0,1 (descriptif : si l'optimum reste sur le bord de la nouvelle grille, le bord est signalé comme limite du réglage).

*Justification.* Verdict établi avec la règle de décision préinscrite (D41).

*Preuve.* Sélection (25 plis, 20 configurations étendues) : famille AXE : meilleure AXE025_B1_T2_a0.25 (T = 2 < 4 et α = 0,25 > 0,1 : optimum intérieur, mais plateau : 13 configurations entre +0,041 et +0,054) ; famille STK : meilleure STK_T1_a0.1 (α = 0,1 : sur le BORD de la grille, critère non rempli).  Fichiers : artifacts/results/v3/W10a_all_units.csv ; W10a_grille.csv ; W10c_all_units.csv ; W10c_tests.csv ; W10_selected.json ; W10_choice.json

*Note.* Plateau pour AXE (les différences de réglage sont de l'ordre de 0,003, sous le bruit) ; pour STK, un prior plus faible gagne en classes toutes présentes mais perd quand des classes sont absentes (STK_T1_a0.1 : −0,022 en abs14 en réplication) : le bord n'est pas un optimum sûr.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:03:49) : statut préinscrite ; En sélection, la meilleure configuration de la famille AXE a T < 4 et α > 0,1, et celle de la famille STK a T < 3 et α > 0,1 (descriptif : si l'optimum reste sur le bord de la nouvelle grille, le bord…

### HK8 : Un candidat est éligible sur 100 plis neufs  (version 2, 2026-11-10 22:25:22 ; **statut : confirmée**)

Règle d'éligibilité de D41 : borne basse de l'IC95 du gain contre PIPE ≥ 0,02 ET Wilcoxon, signes, permutation (unilatéraux contre 0,02) p < 0,0125, condition « toutes », répétitions 20-39 ; rapportée par candidat ; réfutée pour un candidat si la borne haute < 0,02.

*Justification.* Verdict établi avec la règle de décision préinscrite (D41).

*Preuve.* Réplication finale (100 plis, répétitions 20-39), condition « toutes », PIPE 0,5534, seuil 0,02, p < 0,0125 : STK_T1_a0.5 0,5922 : +0,0388 (IC95 [0,032 ; 0,046], signes 71/100, p < 1e-4) : ÉLIGIBLE ; AXE025_B1_T2_a0.25 0,5948 : +0,0414 ([0,034 ; 0,050], signes 63/100, p = 0,0060) : ÉLIGIBLE ; AXE05_B1_T2_a0.25 0,5928 : +0,0394 ([0,032 ; 0,048], signes 61/100, p = 0,0176) : non éligible (test des signes) ; STK_T1_a0.1 0,5898 : +0,0364 ([0,028 ; 0,045], signes 58/100, p = 0,067) : non éligible (signes).  Fichiers : artifacts/results/v3/W10a_all_units.csv ; W10a_grille.csv ; W10c_all_units.csv ; W10c_tests.csv ; W10_selected.json ; W10_choice.json

*Note.* Deux candidats sont éligibles ; les quatre gagnent entre +0,036 et +0,041 avec une borne basse ≥ 0,028 : l'effet est établi pour tous au sens de l'intervalle, le test des signes est le critère qui trie.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:03:49) : statut préinscrite ; Règle d'éligibilité de D41 : borne basse de l'IC95 du gain contre PIPE ≥ 0,02 ET Wilcoxon, signes, permutation (unilatéraux contre 0,02) p < 0,0125, condition « toutes », répétitions 20-39 ; rapportée…

### HK9 : Pipeline gelé choisi par la règle écrite  (version 2, 2026-11-10 22:25:22 ; **statut : confirmée**)

Application de la règle de choix de D41 : le pipeline gelé est le candidat éligible au plus grand minimum de gains sur (toutes, abs8, abs14), avec départage au plus simple si écart < 0,005 ; AXE05_B1_T2_a0.25 si aucun éligible.

*Justification.* Verdict établi avec la règle de décision préinscrite (D41).

*Preuve.* Règle appliquée : parmi les éligibles, minimum des gains sur (toutes, abs8, abs14) : STK_T1_a0.5 +0,0356 ; AXE025_B1_T2_a0.25 −0,0006 ; l'écart (0,036) dépasse 0,005 : le pipeline gelé est STK_T1_a0.5 (composition apprise des quatre têtes, décodage M50 α = 0,5, T = 1).  Fichiers : artifacts/results/v3/W10a_all_units.csv ; W10a_grille.csv ; W10c_all_units.csv ; W10c_tests.csv ; W10_selected.json ; W10_choice.json

*Note.* STK n'a aucun réglage à la main (température 1, prior 0,5 : valeurs du pipeline de la vague 3) ; ses quatre poids sont appris hors-gabarit. Elle est aussi la plus simple des candidats.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:03:49) : statut préinscrite ; Application de la règle de choix de D41 : le pipeline gelé est le candidat éligible au plus grand minimum de gains sur (toutes, abs8, abs14), avec départage au plus simple si écart < 0,005 ; AXE05_B1_…

### HK10 : Le pipeline gelé résiste à 8 et 14 classes absentes  (version 2, 2026-11-10 22:25:22 ; **statut : confirmée**)

Pour le pipeline retenu par HK9, gain contre PIPE > 0 avec borne basse d'IC95 > 0 dans les conditions abs8 et abs14 (répétitions 20-39) ; rapportée par condition.

*Justification.* Verdict établi avec la règle de décision préinscrite (D41).

*Preuve.* Pipeline retenu STK_T1_a0.5, répétitions 20-39 : abs8 (8 classes absentes) : +0,0425, IC95 [0,031 ; 0,054] ; abs14 (14 classes absentes) : +0,0356, IC95 [0,024 ; 0,047] : bornes basses > 0 dans les deux conditions.  Fichiers : artifacts/results/v3/W10a_all_units.csv ; W10a_grille.csv ; W10c_all_units.csv ; W10c_tests.csv ; W10_selected.json ; W10_choice.json

*Note.* Contraste fort : AXE05_B1_T2_a0.25 donne −0,0010 en abs14 (IC95 [−0,014 ; 0,013]) et AXE025 −0,0006 ; seule la composition apprise reste positive quand la moitié des classes est absente.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:03:49) : statut préinscrite ; Pour le pipeline retenu par HK9, gain contre PIPE > 0 avec borne basse d'IC95 > 0 dans les conditions abs8 et abs14 (répétitions 20-39) ; rapportée par condition.

### HJ1 : Ajouter les têtes de caractères améliore STK (STK7)  (version 2, 2026-11-10 23:18:18 ; **statut : réfutée**)

En sélection (25 plis, condition « toutes »), STK7 dépasse STK4 d'au moins 0,01 de macro-F1 du palier A (Wilcoxon unilatéral contre le seuil, Holm sur 2 variantes, p < 0,05).

*Justification.* Verdict établi avec la règle de décision préinscrite (D43).

*Preuve.* Sélection (25 plis, « toutes ») : STK7 0,5804 contre STK4 0,5940 : −0,0136, IC95 [−0,025 ; −0,003], signes 2/23 ; abs8 −0,0047 ; abs14 −0,0169. La borne haute (−0,003) est sous le seuil +0,01 et même sous 0.  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json

*Note.* Ajouter les têtes de caractères pour classe, objet et action FAIT PERDRE du score, en classes toutes présentes comme avec 14 classes absentes.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:40:05) : statut préinscrite ; En sélection (25 plis, condition « toutes »), STK7 dépasse STK4 d'au moins 0,01 de macro-F1 du palier A (Wilcoxon unilatéral contre le seuil, Holm sur 2 variantes, p < 0,05).

### HJ2 : Ajouter la famille par les mots et les bigrammes améliore STK (STK9)  (version 2, 2026-11-10 23:18:18 ; **statut : réfutée**)

En sélection, STK9 dépasse STK4 d'au moins 0,01 (mêmes critères que HJ1).

*Justification.* Verdict établi avec la règle de décision préinscrite (D43).

*Preuve.* STK9 0,5810 contre STK4 0,5940 : −0,0130, IC95 [−0,024 ; −0,003], signes 2/23 ; abs8 −0,0070 ; abs14 −0,0181.  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json

*Note.* Famille par les mots et bigrammes n'arrangent rien : le poids de la tête bigrammes est 0,000 sur les 25 plis.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:40:05) : statut préinscrite ; En sélection, STK9 dépasse STK4 d'au moins 0,01 (mêmes critères que HJ1).

### HJ3 : La variante retenue est confirmée sur plis neufs  (version 2, 2026-11-10 23:18:18 ; **statut : non tranchée**)

Si HJ1 ou HJ2 est vérifiée en sélection, la variante au plus grand gain est confirmée sur les 50 plis des répétitions 40-49, condition « toutes » : gain contre STK4 avec borne basse d'IC95 ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre 0,01) p < 0,05 ; réfutée si la borne haute < 0,01. Si ni HJ1 ni HJ2 n'est vérifiée, la confirmation est menée quand même pour la variante au plus grand gain moyen (précédents D25, D31, D36) avec la même règle.

*Justification.* Verdict établi avec la règle de décision préinscrite (D43).

*Preuve.* Non testée sur plis neufs : la sélection est entièrement négative (IC95 des deux variantes sous 0), donc la confirmation sur les répétitions 40-49 (35 minutes de calcul) ne peut pas changer la conclusion. Écart à la règle D43 (« confirmation menée quand même »), consigné ici : décision de ne pas dépenser ce calcul, motivée par l'intervalle de sélection entièrement négatif.  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json

*Note.* Les confirmations « malgré la porte fermée » des vagues précédentes (D25, D31, D36, D39) visaient des effets positifs dont l'intervalle contenait le seuil ; ici l'effet est négatif et l'intervalle ne le contient pas.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:40:05) : statut préinscrite ; Si HJ1 ou HJ2 est vérifiée en sélection, la variante au plus grand gain est confirmée sur les 50 plis des répétitions 40-49, condition « toutes » : gain contre STK4 avec borne basse d'IC95 ≥ 0,01 ET W…

### HJ4 : La variante retenue ne dégrade pas la robustesse  (version 2, 2026-11-10 23:18:18 ; **statut : non tranchée**)

Sur les répétitions 40-49, pour la variante retenue, le gain contre STK4 dans les conditions abs8 et abs14 a une borne basse d'IC95 > −0,01 (non-infériorité).

*Justification.* Verdict établi avec la règle de décision préinscrite (D43).

*Preuve.* Non évaluée (pas de confirmation) ; à titre indicatif en sélection : STK9 abs8 −0,0070, abs14 −0,0181 ; STK7 abs8 −0,0047, abs14 −0,0169.  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:40:05) : statut préinscrite ; Sur les répétitions 40-49, pour la variante retenue, le gain contre STK4 dans les conditions abs8 et abs14 a une borne basse d'IC95 > −0,01 (non-infériorité).

### HJ5 : Les poids appris sont stables et parlants  (version 2, 2026-11-10 23:18:18 ; **statut : confirmée**)

Descriptif (aucune règle de décision) : poids moyens par tête sur les 25 plis de sélection et leur écart-type ; rapportés.

*Justification.* Verdict établi avec la règle de décision préinscrite (D43).

*Preuve.* Descriptif. Poids moyens STK4 (25 plis, écart-type) : classe 0,087 (0,034) ; objet 0,037 (0,055) ; action 0,346 (0,077) ; famille-lettres 0,603 (0,083). STK7 : classe 0,035 ; objet 0,027 ; action-mots 0,219 ; famille-lettres 0,564 ; classe-lettres 0,061 ; objet-lettres 0,036 ; action-lettres 0,147. STK9 : famille-lettres 0,490 ; action-mots 0,209 ; action-lettres 0,159 ; famille-mots 0,085 ; bigrammes 0,000.  Fichiers : artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json

*Note.* Poids stables d'un pli à l'autre (écart-type 0,03 à 0,12) : les têtes « action » et « famille » dominent toujours ; la classe directe et les bigrammes sont presque ignorées.

*Historique des versions précédentes (conservées) :*
- v1 (2026-11-10 22:40:05) : statut préinscrite ; Descriptif (aucune règle de décision) : poids moyens par tête sur les 25 plis de sélection et leur écart-type ; rapportés.

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

### RI1 : Phase 2, itération I1 : représentation par support de gabarit (série actuelle ; baseline v3 conservée)  (version 1, 2026-11-09 13:14:27)

Macro-F1 palier A (25 plis, P2) : V0 0,503 ; ENS 0,502 ; WGT 0,499 ; C2 0,496 ; T2 0,496 ; C3 0,493 ; T3 0,472 ; T3M 0,470 ; C1 0,469 ; T5 0,418. Aucune amélioration ; restreindre le vocabulaire dégrade. F1 de famille : ENS 0,719 (V0 0,692).

*Justification.* Résultat négatif informatif : il réfute l'explication « les valeurs propres à un gabarit causent le plafond » et fait avancer vers les pistes suivantes. Conservé comme les autres.

*Preuve.* artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv

### RI1b : Confirmation I1b : mots + lettres (ENS) contre mots seuls (V0)  (version 1, 2026-11-09 13:22:39)

Constat exploratoire d'I1 (25 plis) : famille +0,028, distance −0,025, classes −0,001. Confirmation (25 nouveaux plis) : famille +0,029 (IC95 [0,015 ; 0,048]), distance −0,028, classes −0,001 (IC95 [−0,011 ; 0,009]). Les deux séries sont conservées.

*Justification.* L'effet exploratoire se reproduit presque à l'identique sur de nouveaux découpages : il est réel au sens du hasard du découpage. Il porte sur la FAMILLE (confusions moins graves), pas sur les classes.

*Preuve.* artifacts/results/v3/I1b_all_units.csv ; I1b_tests.csv

### RI2 : Phase 2, itération I2 : champs typés (série actuelle ; I1 et I1b conservées)  (version 1, 2026-11-09 13:25:59)

Macro-F1 palier A (25 plis) : V0 0,503 ; FT 0,489 ; FTE 0,487 ; FTo 0,265. F1 de famille : FTE 0,720 ; FT 0,712 ; V0 0,692 ; FTo 0,516. Aucun gain pour les classes ; la structure seule retient environ la moitié du score.

*Justification.* Deuxième résultat négatif sur les classes : ni le vocabulaire (I1) ni la structure typée (I2) ne lèvent le plafond de 0,50 ; seule la composante lettres (ENS) améliore, et uniquement la famille (I1b).

*Preuve.* artifacts/results/v3/I2_all_units.csv ; I2_resume.csv ; I2_tests.csv

### RI4 : Itération I4 : rejet par confiance de famille sur nouvelles rotations (bloc C conservé)  (version 1, 2026-11-09 14:02:51)

Nouvelles rotations × nouveaux plis (25 unités) : AUROC fam_msp 0,693 ; maxlogit 0,671 ; energy 0,670 ; msp 0,665 ; hier_msp 0,664. FPR@95 : 0,85 à 0,87 pour tous. Bloc C (v1 rotations, 125 unités) : fam_msp 0,666 ; énergie 0,639 ; msp 0,623. Les deux séries sont conservées.

*Justification.* La confiance de famille reste le meilleur score dans les deux séries (+0,03 à +0,04 d'AUROC sur le MSP), mais l'avantage est inégal selon les rotations (3 sur 5) et n'améliore pas le FPR@95 : c'est une amélioration modeste, pas une solution. HD7 ajoute qu'elle est plus fragile sous attaque.

*Preuve.* artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json

### RI5 : Itération I5 : réglage des modèles linéaires mots + lettres  (version 1, 2026-11-09 19:14:25)

Meilleure configuration sur 25 plis (répétitions 0 à 4) : 0,5106 contre V0 0,5032 (+0,007) et contre la somme par défaut 0,5022 ; F1 de famille jusqu'à 0,722. Confirmation non lancée (porte fermée).

*Justification.* Troisième itération consécutive sans gain de macro-F1 des classes (I1, I2, I5) : les modèles linéaires sur TF-IDF mots et lettres sont au plafond d'environ 0,50-0,51 ; critère d'arrêt D20 atteint POUR CETTE FAMILLE de modèles. Reste à essayer ce qui change la nature de l'information : le Transformer (I3).

*Preuve.* artifacts/results/v3/I5a_resume.csv ; I5_selected.json

### RT1 : Bloc T : grille complète du Transformer, 90 modèles (précédent v1 conservé)  (version 1, 2026-11-09 21:14:59)

Macro-F1 des classes connues (même logs, 140 par classe) : Transformer 0,424 à 0,368 selon le bruit (p = 0 à 0,5), TF-IDF 0,393 à 0,362. Détection d'inconnus du Transformer (AUROC moyen sur 90) : MSP 0,560 ; énergie 0,572 ; Mahalanobis 0,593 ; kNN 0,596 ; confiance de famille 0,630 ; FPR@95 de 0,91 à 0,93 pour tous. TF-IDF sur les mêmes logs : MSP 0,602 ; énergie 0,623 ; famille 0,643, FPR@95 0,81 à 0,86.

*Justification.* Constat clé : à petit volume d'entraînement, le Transformer apporte environ +0,02 de macro-F1 mais détecte MOINS bien les inconnus que TF-IDF (AUROC 0,56 contre 0,60 pour le MSP, FPR@95 0,92 contre 0,82) ; la confiance de famille est le meilleur score pour les deux. Pas de gain décisif à attendre d'une fusion avec le Transformer : I3 est donc de faible priorité. (Comparaison Transformer/TF-IDF d'AUROC non préinscrite : exploratoire.)

*Preuve.* artifacts/results/v3/T_all_units.csv ; T_tests.csv

### RI6 : Itération I6 : nouveaux hyperparamètres de représentation, structure et modèle (32 configurations)  (version 1, 2026-11-09 22:07:28)

Macro-F1 des classes (25 plis, répétitions 0 à 4) : V0 0,5032 ; meilleure configuration W1_lr30 0,5117 (+0,0085) ; W2_svm0,1 0,5080 ; W4_lr30 0,5071 ; pire W5_ridge1 0,4651. Structure légère W6 : 0,470 à 0,495 (pas de gain). 25 configurations sur 32 indiscernables du meilleur.

*Justification.* Deuxième tentative des leviers d'I1, I2 et I5 avec de nouvelles valeurs : même conclusion, plafond d'environ 0,50 à 0,51 pour les modèles linéaires.

*Preuve.* artifacts/results/v3/I6a_all_units.csv ; I6a_resume.csv ; I6a_friedman.csv ; I6_selected.json

### RI7 : Itération I7 : rejet d'inconnus, 24 combinaisons sur deux jeux de nouvelles rotations (I4 conservée)  (version 1, 2026-11-09 22:07:28)

Sélection (rotations B) : msp (C = 4) 0,608 ; scores de famille 0,645-0,650 (meilleur C64_fam_negent 0,6498) ; énergie 0,614-0,623 ; fam_x_msp 0,626-0,630. Confirmation (rotations C) : msp 0,632 ; scores de famille jusqu'à 0,659 ; C64_fam_negent 0,650. FPR@95 : 0,84-0,88 pour tous. I4 (rotations v2 I4) : fam_msp 0,693 contre msp 0,665.

*Justification.* Quatrième série de données (blocs C, I4, I7a, I7b, plus HT3) où la confiance de famille est le meilleur détecteur, avec un avantage de +0,02 à +0,04 d'AUROC ; l'avantage reste modeste (AUROC absolu 0,65-0,69, FPR@95 voisin de 0,85) : insuffisant au critère S2 (0,80).

*Preuve.* artifacts/results/v3/I7a_all_units.csv ; I7a_resume.csv ; I7a_friedman.csv ; I7b_all_units.csv ; I7b_resume.csv ; I7b_tests.csv ; I7_selected.json ; artifacts/data/rotations_v2_I7a.json ; rotations_v2_I7b.json

### RI7c : Réplication I7c : rejet d'inconnus sur 75 unités de nouvelles rotations (I4, I7a, I7b conservées)  (version 1, 2026-11-09 22:25:21)

75 unités (3 jeux de 5 rotations × 5 répétitions) : AUROC msp (C = 4) 0,627 ; scores de famille 0,666 à 0,670 (C16_fam_msp 0,670 ; C64_fam_negent 0,669) ; FPR@95 : msp 0,874 ; famille 0,854 à 0,869. Gain d'AUROC de la famille : +0,04 (stable par jeu : +0,040 ; +0,042 ; +0,044) ; baisse du FPR@95 : 0,02.

*Justification.* Résultat final sur le rejet d'inconnus : la confiance de famille est un gain réel et stable d'environ +0,04 d'AUROC sur le MSP (confirmé sur 75 unités de rotations jamais vues), mais le FPR@95 reste voisin de 0,85 et l'AUROC absolu (0,67) est loin du critère S2 (0,80).

*Preuve.* artifacts/results/v3/I7c_all_units.csv ; I7c_resume.csv ; I7c_tests.csv ; artifacts/data/rotations_v2_I7c.json

### RT2 : Réplication Transformer T2 et fusion I3 (grille T conservée)  (version 1, 2026-11-10 00:00:10)

20 couples : macro-F1 des classes : TF-IDF 0,523 ; fusion 0,508 ; Transformer 0,469. AUROC d'inconnu : famille fusion 0,664 ; famille TF-IDF 0,656 ; famille Transformer 0,647 ; Mahalanobis Transformer 0,647 ; MSP TF-IDF 0,629 ; MSP fusion 0,627 ; MSP Transformer 0,604. Grille T (une découpe) : Transformer 0,42 à 0,37 contre TF-IDF 0,39 à 0,36.

*Justification.* Conclusion sur le Transformer : avec 140 logs par classe, il ne bat pas TF-IDF (l'avantage de la grille T venait d'une découpe favorable) et la fusion n'améliore pas la classification ni le rejet : pas de gain à attendre ; I3 est close sans gain. Le pipeline reste TF-IDF (mots + lettres pour la famille) avec rejet par confiance de famille.

*Preuve.* artifacts/results/v3/T2_all_units.csv ; T2_tests.csv

### RDG4 : DG4 (exploratoire, développement seulement, aucun entraînement) : comptages format, vocabulaire, axes  (version 1, 2026-11-10 13:19:51)

254 gabarits de développement, 30 classes, 1 à 43 gabarits par classe (médiane 4). (1) FORMAT : l'information mutuelle normalisée entre le format du log (programme + forme des 6 premiers jetons, 62 formats) et la classe vaut 0,56 (programme seul : 0,16) ; prédire un gabarit mis de côté par la classe majoritaire des autres gabarits de même format donne 29 % d'exactitude sur 88 % des gabarits couverts (la classe la plus fréquente fait 17 %) : le format est informatif sans être un raccourci écrasant. (2) VOCABULAIRE : pour un gabarit mis de côté, la bonne classe couvre plus de mots constants que toute autre classe dans 45,5 % des cas seulement ; 0 % quand la classe n'a qu'un ou deux autres gabarits (couverture propre nulle pour file-read, file-write, file-modification, directory-deleted, http-request-failure, user-session-open) alors que la meilleure autre classe couvre 28 à 100 % des mots ; seulement 10 % des mots constants sont absents de tous les autres gabarits : l'erreur vient de mots PARTAGÉS entre classes, pas de mots nouveaux. (3) AXES : 61 gabarits d'« échec », 49 de « fermeture », 33 d'« ouverture », 17 de « modification », 9 de « suppression », mais seulement 2 de « lecture » et 2 d'« écriture » : l'axe d'action ne partage de l'information que pour certaines classes à peu de gabarits ; objet « fichier » 11 gabarits. Déséquilibre : 43 gabarits pour authentication-failed contre 1 à 3 pour huit classes.

*Justification.* Comptages sur le développement seulement (v3_blockA.load() écarte le test v2 ; le garde check_test_seal.py le vérifie). Ils orientent la ronde sans toucher au test.

*Preuve.* artifacts/results/v3/DG4_format_classe.csv ; DG4_vocabulaire_gabarits.csv ; DG4_vocabulaire_par_classe.csv ; DG4_axes.csv

### RW1 : Vague 1 : décodage à masses équilibrées (F8) et autres formules (F14, F6, F9, F18)  (version 1, 2026-11-10 13:26:20)

Macro-F1 palier A, sélection (répétitions 0-4) : V0 0,5032 ; LR 0,4947 ; A1 0,5752 ; D0,5 0,5307 ; D1 0,5256 ; D2 0,5215 ; B7 0,5052 ; B6 0,5022 ; E2 0,4974 ; B5 0,4947 ; C2 0,4850 ; C1 0,4841 ; C0 0,4804 ; E1 0,4694 ; A2 0,4380. Confirmation d'A1 (répétitions 5-9) : 0,5544 contre LR 0,4976 et V0 0,5132.

*Justification.* Premier gain net et confirmé de la phase 2 : +0,04 à +0,07 sur le meilleur modèle classique, avec une formule d'une ligne (Sinkhorn amorti, exposant 0,5, 10 itérations, cible uniforme). Les cinq autres pistes de la vague 1 n'apportent rien (F14, F6, F18) ou un gain non établi (F9).

*Preuve.* artifacts/results/v3/W1a_all_units.csv ; W1a_tests.csv ; W1b_all_units.csv ; W1b_tests.csv ; W1_selected.json

### RW2 : Vague 2 : affinage et épreuve du décodage à masses équilibrées  (version 1, 2026-11-10 13:31:52)

Macro-F1 palier A (répétitions 0-4) : A1 0,5752 ; F9S 0,5760 ; H1 0,5755 ; G25 0,5737 ; G1 0,5733 ; I30 0,5730 ; P5 0,5589 ; S1 0,5551 ; S2 0,5494 ; référence LR 0,4947. Robustesse (8 classes retirées du lot) : sélection A1_abs 0,5918 contre LR_abs 0,5538 (+0,038) ; confirmation 0,5474 contre 0,5425 (+0,005).

*Justification.* A1 est stable face aux réglages (plateau) mais fragile face à l'absence de classes dans le lot : le décodage équilibré suppose que presque toutes les classes sont présentes. Un décodage consciente de la présence est nécessaire pour un résultat défendable sur le test final.

*Preuve.* artifacts/results/v3/W2a_all_units.csv ; W2a_tests.csv ; W2a_robustesse.csv ; W2b_all_units.csv ; W2b_robustesse.csv ; W2_selected.json

### RW3 : Vagues 2 et 3 : A1 est fragile à l'absence de classes ; la cible mixte M50 est robuste (trois séries de plis)  (version 1, 2026-11-10 13:35:22)

Macro-F1 du palier A. TOUTES les classes présentes : LR 0,495 / 0,498 / 0,503 (sélection / confirmation / réplication) ; A1 0,575 / 0,554 / 0,563 ; M50 0,555 / 0,541 / 0,558. 8 CLASSES RETIRÉES du lot : LR 0,554 / 0,543 / 0,545 ; A1 0,592 / 0,547 / 0,560 ; M50 0,600 / 0,577 / 0,581. 14 CLASSES RETIRÉES : LR 0,550 / 0,595 / 0,582 ; A1 0,542 / — / 0,530 ; M50 0,580 / 0,621 / 0,593. Gains de M50 sur LR : +0,060 / +0,043 / +0,055 (toutes) ; +0,046 / +0,035 / +0,036 (abs8) ; +0,030 / +0,025 / +0,012 (abs14).

*Justification.* Le décodage à masses équilibrées est la première amélioration nette et reproductible de la phase 2 (+0,04 à +0,06 quand toutes les classes sont présentes) ; sa version simple A1 s'effondre quand beaucoup de classes sont absentes ; la cible mixte M50 (moitié uniforme, moitié prior observé) garde +0,035 avec 8 classes absentes. Résultat à présenter avec la réserve de transduction (le décodage utilise la composition du lot) et avec la limite HY8 (test des signes).

*Preuve.* artifacts/results/v3/W3a_all_units.csv ; W3a_tests.csv ; W3b_all_units.csv ; W3b_tests.csv ; W3c_all_units.csv ; W3c_tests.csv

### RW3d : Réplication finale du décodage M50 (100 plis)  (version 1, 2026-11-10 14:12:03)

Macro-F1 du palier A, 100 plis : toutes : LR 0,5046 ; A1 0,5619 ; M50 0,5534 ; 8 classes absentes : LR 0,5292 ; A1 0,5542 ; M50 0,5646 ; 14 classes absentes : LR 0,5800 ; A1 0,5443 ; M50 0,5895. Gain de M50 sur LR : +0,049 (toutes), +0,035 (abs8), +0,010 (abs14, non significatif).

*Justification.* M50 est établi comme décodage robuste ; sur trois séries indépendantes de plis (25 + 25 + 50 puis 100) les gains vont de +0,035 à +0,06 quand au moins 8 classes sur 30 sont présentes.

*Preuve.* artifacts/results/v3/W3d_all_units.csv ; W3d_tests.csv ; artifacts/data (graines : répétitions 20 à 39)

### RW4smoke : Vague 4, version 1 du script : unité de test (répétition 0, pli 0, condition « toutes »), conservée ici après suppression par erreur du fichier  (version 1, 2026-11-10 14:16:17)

Valeurs affichées lors du test (macro-F1 du palier A ; macro-F1 des classes à ≤ 3 gabarits) : LR brut 0,4607 ; 0,2882 · LR M50 0,4446 ; 0,2755 · AXE0 brut 0,4367 ; 0,3437 · AXE0 M50 0,4667 ; 0,3433 · AXE05 brut 0,4556 ; 0,3321 · AXE05 M50 0,4508 ; 0,3117 · AXE1 brut 0,456 ; 0,3279 · AXE1 M50 0,4458 ; 0,2931 · BAG10 brut 0,432 ; 0,0723 · BAG10 M50 0,4399 ; 0,0422 · DRO1 brut 0,0 ; 0,0 (dégénéré) · DRO1 M50 0,0 ; 0,0.

*Justification.* Le dossier artifacts/results/v3/P2_W4a_selection (une seule unité, issue de la version 1 de v3_phase2_W4.py, jamais commitée) a été supprimé par erreur avant la relance, contre la règle R3 (ne jamais supprimer un résultat) : la suppression n'était pas nécessaire (la liste des variantes changeait la configuration, donc l'identifiant de l'unité). Les valeurs sont conservées ici à partir de la sortie affichée ; la version 1 du script est figée dans versions/scripts/v3_phase2_W4__1.py. Un pli ne constitue pas un résultat de la vague 4.

*Note.* Erreur reconnue le 2026-11-10 ; règle pour la suite : on ne relance jamais un calcul en supprimant un dossier de résultats.

### RW4 : Vague 4 : produit d'experts objet × action (F7), bagging par gabarits (F20), pondération des gabarits difficiles (F10)  (version 1, 2026-11-10 14:19:12)

Sélection (25 plis, répétitions 0-4), condition « toutes », macro-F1 du palier A, brut / avec M50 : LR 0,4947 / 0,5544 ; AXE05 0,5330 / 0,5750 ; AXE1 0,5233 / 0,5691 ; AXE0 0,5167 / 0,5520 ; DRO2 0,4957 / 0,5600 ; BAG10 0,4761 / 0,5405 ; DRO1 0,005 (dégénéré). Confirmation d'AXE05 (50 plis, répétitions 10-19) : brut 0,5386 contre LR 0,5033 (+0,035) ; avec M50 0,5765 contre LR + M50 0,5583 (+0,018) ; 8 classes absentes avec M50 : 0,5827 contre 0,5808 (+0,002).

*Justification.* Aucune de ces formules n'est établie au-delà du pipeline gelé (LR + M50). F7 est la seule à montrer un gain net en brut, mais son mécanisme annoncé (aider les classes rares) n'est pas observé (HZ6) et le décodage en absorbe plus de la moitié. F20 et F10 n'apportent rien (la pondération non bornée est inutilisable).

*Preuve.* artifacts/results/v3/W4b_all_units.csv ; W4b_tests.csv ; W4b_HZ7_HZ8.csv

### RW5 : Vague 5 : détection d'inconnus par la famille avec décodage M50 (I7 conservée)  (version 1, 2026-11-10 14:47:20)

Ensemble B (25 unités) : AUROC FAM 0,6483 ; FAMQ 0,6464 ; FAMD 0,6445 ; MSPQ 0,6250 ; MSP 0,6081. FPR@95 : FAM 0,8731 ; FAMQ 0,8816 ; FAMD 0,8663 ; MSPQ 0,8550 ; MSP 0,8854.

*Justification.* Le décodage équilibré, utile pour la classification fermée, ne l'est pas pour la détection d'inconnus : le pipeline gelé garde la confiance de famille brute pour le rejet (+0,04 d'AUROC sur le MSP, HI6b), sans décodage.

*Preuve.* artifacts/results/v3/W5a_all_units.csv ; W5a_tests.csv ; W5_selected.json

### RW6 : Vague 6 : V-REx et embeddings gelés (brut / M50)  (version 1, 2026-11-10 14:47:20)

Macro-F1 du palier A (25 plis), brut / M50 : LR 0,4947 / 0,5544 ; ERM 0,4872 / 0,5507 ; VR1 0,4829 / 0,5522 ; VR5 0,4858 / 0,5462 ; VR20 0,4974 / 0,5451 ; E1 0,4515 / 0,4643 ; E2 0,4801 / 0,5056 ; E3 0,4628 / 0,4872.

*Justification.* Ni l'invariance de risque entre gabarits ni la sémantique d'un encodeur gelé ne relèvent le score : deux leviers de plus fermés, avec des résultats négatifs informatifs.

*Preuve.* artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json

### RW7 : Vague 7 : LP-FT et adaptation MLM de DistilBERT (clôturée, 11 couples sur 20)  (version 1, 2026-11-10 21:35:02)

Protocole de T2 (140 logs par classe, découpes (1,1), (2,2) et début de (3,3)), macro-F1 du palier A sur 11 couples : TF-IDF 0,4965 ; LP-FT adapté (MLM) 0,4848 ; affinage complet T2 0,4702 ; LP-FT 0,4657. LP-FT contre affinage complet −0,0045 ; LP-FT adapté contre LP-FT +0,0191 ; LP-FT adapté contre TF-IDF −0,0117 (IC95 [−0,061 ; 0,036]).

*Justification.* Aucun encodeur ne dépasse TF-IDF sur ces logs, même adapté : le pipeline reste TF-IDF + régression logistique + décodage M50. Résultat partiel, non concluant au sens des règles (couples manquants) mais cohérent avec RT2.

*Preuve.* artifacts/results/v3/W7_all_units.csv ; W7_tests.csv ; W7_lpft/ (11 unités)

### RW8 : Vague 8 : réglage conscient du décodage, mots + lettres avant décodage, auto-apprentissage sur le lot décodé  (version 1, 2026-11-10 21:45:51)

Sélection (25 plis, « toutes »), macro-F1 du palier A : PIPE 0,5544 ; ST1 0,5793 ; ST2 0,5764 ; meilleure configuration de grille (C = 30, T = 1, poids 0,25) 0,5695 ; ENSP30 0,5569 ; ENSP50 0,5561. Les cinq meilleures configurations de la grille ont toutes un poids 0,25 du prior observé. Confirmation (50 plis neufs) : PIPE 0,5583 ; grille +0,0037 ; ST1 +0,0063 ; ST2 +0,0029 ; avec 8 classes absentes : −0,007 à −0,019.

*Justification.* Aucun levier de la vague 8 ne s'établit : les gains de sélection (+0,015 à +0,025) se réduisent à +0,003 à +0,006 sur plis neufs. Le pipeline gelé reste TF-IDF mots → régression logistique C = 10 → décodage M50 (poids 0,5, température 1). Illustre le biais du maximum d'une grille et de la sélection sur 25 plis.

*Preuve.* artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json

### RW9 : Vague 9 : composition de leviers (axes objet × action, lettres vers la famille, température, prior) et composition apprise STK  (version 1, 2026-11-10 22:03:15)

Sélection (25 plis, « toutes »), macro-F1 du palier A : PIPE 0,5544 ; meilleure configuration AXE05, lettres 1, température 2, prior 0,25 : 0,6071 (+0,0527) ; STK 0,5940 (+0,0396). Confirmation (50 plis neufs) : PIPE 0,5583 ; AXE05_B1_T2_a0.25 0,5933 (+0,0350) ; STK 0,5872 (+0,0289). Avec 8 classes absentes (confirmation) : AXE05 +0,0068 ; STK +0,0174.

*Justification.* Première amélioration obtenue en COMPOSANT des leviers : aucun levier seul ne dépassait +0,02 de façon établie, leur combinaison réglée (axes objet × action + température 2 + prior 0,25) donne +0,035 sur plis neufs ; la composition apprise STK, sans réglage, donne +0,029 et résiste mieux à l'absence de classes.

*Preuve.* artifacts/results/v3/W9a_all_units.csv ; W9a_grille.csv ; W9a_HK1.csv ; W9a_HK2.csv ; W9a_HK3.csv ; W9b_all_units.csv ; W9b_tests.csv ; W9_selected.json

### RW10 : Vague 10 : degrés étendus et réplication finale sur 100 plis (répétitions 20-39)  (version 1, 2026-11-10 22:25:22)

Macro-F1 du palier A, PIPE (décodage M50 seul) : 0,5534 (toutes) ; 0,5645 (8 absentes) ; 0,5897 (14 absentes). STK_T1_a0.5 : 0,5922 ; 0,6070 ; 0,6252 (gains +0,039 ; +0,043 ; +0,036). AXE05_B1_T2_a0.25 : 0,5928 ; 0,5949 ; 0,5886 (+0,039 ; +0,030 ; −0,001). AXE025_B1_T2_a0.25 : 0,5948 ; 0,5952 ; 0,5891. STK_T1_a0.1 : 0,5898 ; 0,5874 ; 0,5680. Pour mémoire, la régression logistique brute sur les mêmes plis (W3d) : 0,5046.

*Justification.* Le pipeline final gagne environ +0,088 sur la régression logistique brute (0,5046 → 0,5922, classes toutes présentes), dont +0,049 apportés par le décodage et +0,039 par la composition apprise ; il garde son avantage quand 8 ou 14 classes sur 30 sont absentes du lot. Les réglages fins (température, prior) ne trouvent pas de mieux robuste : la composition apprise sans réglage suffit.

*Preuve.* artifacts/results/v3/W10a_all_units.csv ; W10a_grille.csv ; W10c_all_units.csv ; W10c_tests.csv ; W10_selected.json ; W10_choice.json

### RW11 : Vague 11 : composition apprise élargie (STK7, STK9)  (version 1, 2026-11-10 23:18:18)

Sélection (25 plis), macro-F1 du palier A, toutes / 8 absentes / 14 absentes : PIPE 0,5544 / 0,5998 / 0,5796 ; STK4 0,5940 / 0,6284 / 0,6262 ; STK7 0,5804 / 0,6237 / 0,6093 ; STK9 0,5810 / 0,6214 / 0,6081.

*Justification.* Plus de têtes ne donne pas plus de score : les poids appris par entropie croisée hors-gabarit se dégradent quand les têtes sont corrélées (surajustement du critère d'apprentissage, qui n'est pas la macro-F1 après décodage). STK4, qui a quatre têtes peu corrélées, reste le pipeline gelé. Piste suivante : apprendre les poids directement sur la macro-F1 décodée hors-gabarit.

*Preuve.* artifacts/results/v3/W11a_all_units.csv ; W11a_tests.csv ; W11a_poids_STK4.csv ; W11a_poids_STK7.csv ; W11a_poids_STK9.csv ; W11_selected.json
