# Pistes optimistes et formules maison (2026-11-10)

Suite du bilan (`BILAN_A_Z_AVANT_RONDE3.md`) et de l'état de l'art (`etat_de_l_art/sources_v3_ronde3.md`). **Aucun calcul n'a été lancé pour écrire ce document** : tout vient de résultats déjà au registre et de raisonnement. Chaque idée ci-dessous est une **hypothèse à préinscrire puis tester**, pas un résultat. Les noms F6 à F17 continuent la numérotation du plan (F1 à F4 : fusion pondérée, Mahalanobis rétréci, gabarits-prototypes, marqueurs typés).

## 1. Sur ton intuition : vectorisation, entraînement, validation

Ton hypothèse est en grande partie juste, avec une nuance.
- **Le découpage n'est pas un levier** : on ne peut pas le « régler » sans tricher. Le découpage par gabarits disjoints *est* la tâche (comme au test v2, caché). Les trois protocoles par gabarit donnent le même niveau (P1 0,471 ; P2 0,503 ; P3 0,487 ; test v1 0,4832) : le plafond n'est **pas** un artefact de protocole (c'est la réponse à l'hypothèse H10 du sous-agent).
- **Les trois autres leviers n'ont été explorés que dans une direction** : (vectorisation) toutes les représentations essayées sont **lexicales** (sac de mots, lettres, Skip-gram) ou un Transformer **affiné** ; (entraînement) toujours des classifieurs « un log = un exemple, une classe = une étiquette » avec perte standard ; (validation) toujours la macro-F1 en « argmax » comme seul signal de décision. C'est pour cela que tout reste dans la même fourchette : **on a beaucoup bougé les boutons d'une même famille d'idées**.
- Le tableau de DG2 le confirme : aucun réglage ne bouge le plafond (I6 : 25 configurations sur 32 indiscernables), mais les erreurs sont des **gabarits entiers**, absorbés par une classe voisine (ex. `file-read` classé à 93 % connexion échouée ; `file-write` à 89 % connexion ouverte). Ce qui manque n'est pas un meilleur réglage, c'est **une autre façon de représenter, d'apprendre et de mesurer**.

## 2. Relecture des résultats : où le terrain est optimiste

| Bloc | Ce que les résultats montrent | Pourquoi cela ouvre une piste |
|---|---|---|
| A | Hasard 0,986, gabarit 0,50 : les modèles reconnaissent des gabarits, pas des événements | Il faut une représentation qui capture **l'événement** (action, objet, issue) indépendamment des mots du gabarit → F7, F8, F14 |
| B | La hiérarchie ECS (8 familles) n'aide pas les classes (HB1) ni même la famille (HB2) | La hiérarchie « par domaine » ne partage pas l'information utile : une autre taxonomie, **par action**, croise l'arbre → F7 |
| C | Famille meilleure que le MSP (+0,04, stable) ; Mahalanobis, kNN, OpenMax, ViM… ne servent à rien | L'information de **niveau grossier** est plus fiable que celle de niveau fin : un score à plusieurs niveaux (objet, action, famille) peut aller plus loin → F7, F15 |
| C, v1 | Une classe masquée est rangée à 93-100 % dans UNE classe connue | **Effondrement de masse** vers des classes « attractrices » (grandes ou denses) → F8 (décodage à masses équilibrées) |
| V | Lettres 0,51 stables ; mots 0,52 → 0,50 ; Skip-gram monte avec le bruit | Les lettres captent la morphologie ; les mots captent la sémantique lexicale : les **combiner par rôle** (lettres pour la famille, mots pour la classe) → F9 |
| T | Transformer affiné moins bon que TF-IDF (0,47 contre 0,52) | 140 logs/classe pour 66 millions de paramètres : sur-apprentissage aux gabarits ; piste LP-FT ou embeddings gelés + tête → F13 |
| D | Seules les homoglyphes et leur table ; adversarial v1 ne généralise pas à une attaque nouvelle | L'adversarial doit être refait en v3 avec la table officielle et une attaque tenue à part → F16 |
| E | La calibration sous décalage de gabarits échoue | Le jeu de calibration doit contenir des gabarits distincts (déjà vu) ; une calibration **par famille** reste à tester → F15 |
| Phase 2 | Vocabulaire, structure, réglages : rien | Les mots propres à un gabarit **aident** (HF1 réfutée) : ils ne sont pas du bruit ; il faut leur donner moins de poids, pas les retirer → F6 |
| DG2 | Agréger par vrai gabarit ne change rien ; huit classes ont F1 ≈ 0 avec 1 à 3 gabarits | Problème d'apprentissage quasi « à un exemple » : il faut **partager l'information entre classes** (axes communs) → F7, F12 |

## 3. Les formules maison

Notation : `x` = un log, `φ(x)` ses caractéristiques, `c` une classe parmi K = 30, `g` un gabarit d'entraînement (N_G = nombre de gabarits).

### F6 : TF-IDF « de gabarit » avec pureté de classe rétrécie (vectorisation)
- IDF calculé sur les **gabarits**, pas sur les logs : `idf_G(w) = log((N_G+1)/(df_G(w)+1)) + 1`, où `df_G(w)` = nombre de gabarits contenant le mot. (Avec l'IDF par log, un gabarit de 20 000 logs fait monter l'IDF de ses mots comme s'ils étaient fréquents partout.)
- Poids de **pureté de classe** rétrécie : `p(c|w) = (n_cw + α/K) / (n_w + α)` avec `n_cw` = nombre de gabarits de la classe `c` contenant `w`, `α = 2` ; `κ(w) = 1 − H(p(·|w)) / log K`. Un mot vu dans un seul gabarit a une entropie élevée (rétrécissement) : il n'est pas supprimé (HF1 a montré que supprimer nuit), il est **atténué**.
- Caractéristique : `x_w = log(1 + tf_w) · idf_G(w) · (1 + λ·κ(w))`, λ ∈ {0 ; 1 ; 2}.
- Hypothèse : macro-F1 ≥ V0 + 0,02. Coût : minutes. Risque : faible.

### F7 : classification factorisée objet × action (produit d'experts), **notre idée principale**
Observation : les 30 classes se lisent comme **(objet, action)**, et les actions sont partagées :

| Axe action | Classes concernées |
|---|---|
| échec | authentication-failed, connection-failed, file-action-failure, http-request-failure, process-error |
| succès | authentication-success, http-request-success |
| suppression | directory-deleted, file-deleted, user-deletion |
| création | directory-created, user-creation |
| modification | directory-changed, file-modification, system-configuration-changed |
| ouverture/démarrage | connection-opened, process-started, user-session-open |
| fermeture/fin/arrêt | connection-closed, process-ended, process-shutdown, user-logout |

et les objets aussi (fichier 5 classes, processus 5, utilisateur 4, connexion 3, répertoire 3…). Les classes qui échouent (file-read, file-write, user-session-open) ont 1 à 3 gabarits **mais leur objet et leur action sont appris ailleurs** : « fichier » (5 classes) et « ouverture » (3 classes).
- Deux têtes linéaires : `p_obj(j|x)` et `p_act(k|x)` (apprises sur **toutes** les classes qui partagent l'axe), éventuellement une tête classe `p_cls(c|x)`.
- Score de classe : `s(c|x) = log p_obj(j(c)|x) + log p_act(k(c)|x) + γ·log p_cls(c|x)`, γ ∈ {0 ; 0,5 ; 1}.
- Score d'inconnu « hors table » : `ε(x) = max_{(j,k)} [log p_obj(j|x) + log p_act(k|x)] − max_{c valide} s(c|x)` : grand quand le log est un couple (objet, action) **jamais vu ensemble** (un inconnu qui compose deux axes connus), et `ε` combiné avec `1 − max p` pour les inconnus d'un axe nouveau.
- Hypothèses : (a) macro-F1 des classes ≥ V0 + 0,02, avec un gain concentré sur les classes à ≤ 3 gabarits ; (b) AUROC d'inconnu ≥ famille + 0,02.
- Honnêteté : ces axes viennent **des noms de classes** (comme la taxonomie à 8 familles, déjà « hypothèse de démonstration ») ; à faire valider avec le professeur. Coût : faible (têtes linéaires). Risque : moyen ; **c'est la piste au meilleur rapport gain/coût**, car elle attaque le goulot identifié par DG2.

### F8 : décodage à masses équilibrées (Sinkhorn / EM de prior), transductif
- Constat : les classes « attractrices » absorbent des gabarits entiers (DG2, v1 7.6).
- Formule : sur le lot de test, matrice de scores `S` (n × K) ; `Q = diag(u) · exp(S/τ) · diag(v)` avec lignes de somme 1 et colonnes de somme `π_c` ; `π` fixé uniforme sur les classes (aligné sur la macro-F1) ou estimé par EM : `π_c ← mean_i Q_ic` (Saerens, Latinne, Decaestecker 2002). Réponse : `argmax_c Q_ic`.
- Hypothèse : macro-F1 ≥ V0 + 0,02. Coût : quasi nul (post-traitement). Risque : forcer l'équilibre quand un pli ne contient pas une classe ; garde-fou : plancher `π_min` et variante EM.
- Condition d'honnêteté : utilise des logs de test **sans étiquette** (transductif) ; à déclarer comme tel dans le document.

### F9 : hiérarchie à vues séparées (lettres pour la famille, mots pour la classe)
- `s(c|x) = m_mots(c|x) + β · log p_lettres(fam(c)|x)`, β ∈ {0,5 ; 1 ; 2}.
- Fondement : HF7/HF8 confirmées (lettres : famille +0,029) et HB1 (la hiérarchie « mots seuls » n'aide pas). Test d'une hiérarchie dont les deux niveaux n'utilisent pas la même vue.
- Variante empilée (stacking) : méta-régression logistique sur des marges **hors gabarit** (validation croisée interne par groupes).

### F10 : pondération adversariale des gabarits (group-DRO linéaire)
- Poids `q_g` par gabarit ; à chaque tour : `q_g ← q_g · exp(η · L_g)` normalisé (L_g perte moyenne du gabarit hors-gabarit), puis réapprentissage pondéré. 5 à 10 tours. Les gabarits « difficiles » pèsent plus. Inspiré de Sagawa et al. 2020 (Group DRO) ; à vérifier dans la source avant de le citer.

### F11 : mesures de développement plus sensibles
- La macro-F1 « argmax » est bruitée (écart-type 0,05 entre plis ; environ 311 gabarits seulement). Beaucoup de « réfutées » sont en réalité **sous le seuil de détection** (HF1 : IC95 jusqu'à −0,023 à +0,009).
- À adopter comme signal de **développement** (la macro-F1 reste le critère final) : rang réciproque moyen de la vraie classe (MRR), rappel en top-3, log-vraisemblance négative par gabarit. Un effet qui n'inverse pas l'argmax mais remonte la bonne classe d'un rang est visible dans ces mesures.

### F12 : gabarits chimères (augmentation structurée)
- À partir de deux logs de la même classe, couper aux séparateurs (crochets, deux-points, virgules) et recombiner des segments : on fabrique de **nouveaux gabarits plausibles** de la même classe. Plus fort que la suppression aléatoire de mots (HG5) car il change la structure.

### F13 : sonde linéaire puis affinage doux (LP-FT) sur DistilBERT
- Étape 1 : embeddings gelés (moyenne des couches) + régression logistique ; étape 2 : affiner avec un petit taux d'apprentissage en partant de la sonde (Kumar et al. 2022, abstract vérifié par le sous-agent). Hypothèse : fait mieux que 0,469 (affinage complet) et rattrape TF-IDF.

### F14 : normalisation morphologique (troncature de racine)
- Tokens tronqués à `k` lettres (k ∈ {5 ; 6 ; 7}) pour aligner « opened / open / opens », « deleted / deletion / delete ». Jamais testé (les n-grammes de lettres le font partiellement). Coût : minutes.

### F15 : détection d'inconnus à trois niveaux
- `u(x) = a·(1 − max_f p_fam(f|x)) + b·(1 − max p_act) + c·ε(x)` (F7) ; règle ProHOC : « famille sûre, feuille incertaine → inconnu de la famille F ». Calibration par famille sur des gabarits distincts. À comparer à la famille seule (0,67) ; FPR@95 est l'objectif (0,85 actuellement).

### F16 : entraînement adversarial v3
- Reprendre l'étape 9 de v1 en protocole P2, avec la table officielle UTS #39 dans la défense, une attaque **tenue à part** à l'entraînement, plusieurs degrés, tests apparié. Hypothèse : combinaison normalisation + augmentation ≥ chacune seule.

### F17 : contrastif supervisé au niveau gabarit
- Perte contrastive où les positifs sont des logs de **gabarits différents** de la même classe (et non les logs du même gabarit) : force la représentation à se rapprocher par la classe, pas par le gabarit. À tester sur DistilBERT ou sur un petit encodeur sur lettres (Zeng et al. 2021, Gunel et al. 2020 : résumés vérifiés).

## 4. Ordre proposé (gain attendu × coût), 3 à 4 jours

1. **Vague 1, quelques minutes de calcul chacune** : F8 (décodage), F14 (racines), F6 (IDF de gabarit), F9 (vues séparées) ; mesures F11.
2. **Vague 2, linéaire léger** : F7 (axes objet × action), F10 (DRO), F12 (chimères).
3. **Vague 3, DistilBERT** : F13 (LP-FT), F17 (contrastif) ; hypothèses HG1/HG2 (embeddings gelés, nom de la classe).
4. **Vague 4** : F15, F16, puis **empilement final** (stacking hors gabarit) des gagnants.
Chaque vague : hypothèses **préinscrites avant** (seuil, test, règle), sélection sur les répétitions 0 à 4, confirmation sur 5 à 9, plusieurs tests, versions enregistrées. Les petits gains seront **empilés** : plusieurs +0,01 à +0,02 peuvent faire +0,05, ce qu'un seuil de 0,02 par idée ne verrait pas.

## 5. À valider ensemble
1. Les **axes objet × action** (F7) sont une lecture des noms de classes : OK pour les utiliser ?
2. **« L'article de l'OGL »** : je n'ai pas compris à quoi tu fais référence (l'article du jeu SIEVE ? un document de recherche à écrire dans `article/` ?). Dis-moi lequel : je l'intègre au plan.
3. Feu vert pour la **vague 1** (aucun calcul n'est lancé tant que tu ne le dis pas).

---

# Ajout (2026-11-10, suite) : vérification d'autres leviers que les trois cités

Demande : ne pas se limiter à vectorisation, entraînement et validation ; vérifier s'il existe d'autres leviers. Méthode : parcours de **toute la chaîne** (données → étiquettes → prétraitement → représentation → modèle → décision → évaluation → monde ouvert → calibration → déploiement), avec pour chaque maillon : ce qu'on a mesuré, ce qu'on n'a pas essayé, l'optimisme. Aucun calcul lancé.

## 6. Carte de tous les leviers

| # | Maillon | Levier | Déjà exploré ? | Preuve ou raison de l'optimisme |
|---|---|---|---|---|
| L1 | **Données : étiquettes** | Bruit ou ambiguïté d'étiquettes | Partiellement : aucun texte n'a deux classes (notebook 1.4) ; les 49 doublons sont tous `connection-closed` | Pas de bruit détectable par cette voie : **le plafond ne vient probablement pas d'étiquettes contradictoires**. Reste la proximité de sens de classes voisines (non mesurée) |
| L2 | **Données : espace d'étiquettes** | Autre lecture des classes : (objet, action) au lieu de l'arbre à 8 familles | Non | HB1/HB2 : l'arbre ECS n'aide pas ; DG2 : classes à 1-3 gabarits ; axes d'action partagés par 2 à 5 classes → **F7** |
| L3 | **Données : raccourcis** | **Le format du fournisseur (en-tête syslog, programme, forme de l'horodatage) sert de raccourci pour la classe** | **Non, jamais examiné** | Exemples de DG2 : le gabarit de test de `file-read` est un log de type pare-feu PIX (« %PIX-0-… Accessed URL ») classé à 93 % connexion échouée ; celui de `file-write` est un journal de transfert FTP classé à 89 % connexion ouverte. Hypothèse : le modèle apprend « ce format → cette classe » parce que, en entraînement, tel format ne porte que tel ou tel type de gabarits. Dans ce cas, **la généralisation échoue car le format (variable de nuisance) est confondu avec la classe**. → **F18** |
| L4 | **Données : volume** | Utiliser tous les logs au lieu de 400 par gabarit ; ajouter les six versions de bruit | Non mesuré (le plafond de 400 est une décision D3) | Les versions de bruit ne contiennent pas de nouveaux gabarits (notebook 1.4 : pas de copie ligne à ligne, mais mêmes gabarits) : peu d'espoir sur les gabarits ; le plafond pourrait sous-représenter des variantes ; **test simple** |
| L5 | **Prétraitement** | Retirer l'en-tête (horodatage, hôte, programme) ou le normaliser ; masquer noms et chemins | Partiellement (étape 4 v1 : masquage numérique sans effet ; casse défavorable) | Le masquage actuel ne touche ni les **noms d'utilisateur ni les chemins** (de simples mots), qui dominent le vocabulaire des gabarits (ex. « /source/significant/three.mp4 », « brettpearson ») → **F18** (en-tête) et F14 |
| L6 | **Représentation** | Sémantique (synonymes d'actions, embeddings gelés, nom de classe) ; morphologie ; IDF de gabarit | Non pour la sémantique ; non pour l'IDF de gabarit | HG1 à HG3, F6, F14 ; v1 5.8a : les synonymes sont proches dans Skip-gram (0,85 à 0,88) mais **seulement appris sur ces logs** |
| L7 | **Représentation : pré-entraînement** | Pré-entraînement **auto-supervisé** (MLM) sur les ≈ 600 000 logs sans étiquette (training folds seulement en développement) | Non | Aucun modèle n'a vu la **langue des logs** avant la tâche ; DistilBERT sur du texte anglais courant fragmente à ≈ 4 jetons par mot (v1 5.4). Pré-entraîner puis LP-FT → **F21** (coût Mac : plusieurs heures) |
| L8 | **Modèle** | Architecture : char-CNN, BiLSTM, fastText supervisé, GBDT | Non (sauf fastText non supervisé) | Pas de raison d'espérer, mais jamais testé ; faible priorité |
| L9 | **Modèle : variance** | **Bagging par gabarits** (modèles sur sous-ensembles de gabarits, moyenne) | Non | Variance énorme entre découpages (écart-type 0,05 pour 311 gabarits) : un modèle dépend de **quels gabarits** il a vus ; moyenner réduit cette variance → **F20** |
| L10 | **Entraînement : invariance** | Invariance entre gabarits (V-REx / IRM) ou pire gabarit (group-DRO) | Non | DG2 : des gabarits ENTIERS sont mal classés ; la pénalité de variance du risque entre gabarits vise exactement cela → **F10/F19** |
| L11 | **Décision** | Équilibrer les masses prédites ; top-k ; repli sur la famille ; réponse avec abstention | Non (seulement le repli de v1 6.4d et la prédiction conforme E) | F8 ; v1 7.6 : une classe masquée est rangée à 93-100 % dans une seule classe |
| L12 | **Évaluation : métrique** | **F-mesure hiérarchique** (crédit partiel quand la famille est juste), courbe couverture × exactitude | Non (on a la distance dans l'arbre, pas la hF1) | La hiérarchie est évaluée dans la littérature par des mesures hiérarchiques ; elles reflètent mieux l'usage (une alerte « famille réseau » aide un analyste). **Ce n'est pas une astuce** si les deux sont rapportées → **F22** |
| L13 | **Évaluation : puissance statistique** | Mesurer **par gabarit** (≈ 311 unités) avec validation hors-un-gabarit au lieu de 25 plis dépendants | Non | Beaucoup de « réfutées » ont un IC trop large pour exclure +0,01 ; plus de puissance révèle de petits gains empilables → **F11, F23** |
| L14 | **Monde ouvert** | Pseudo-inconnus (outlier exposure), classe « inconnu » explicite, seuil par famille, score à trois niveaux | Partiellement (bloc E « classes cachées » pour la température) | État de l'art : Zhan 2021, Zeng 2021 (abstracts vérifiés) ; F15 |
| L15 | **Test-time** | Adaptation au lot de test (EM de prior, pseudo-étiquettes, regroupement) | Oracle d'agrégation : 0 | F8 seulement (prior), pas l'agrégation |
| L16 | **Données externes ou synthétiques** | Paraphrase ou génération de gabarits synthétiques pour les classes à 1-3 gabarits ; corpus externes (LogHub) | Non | Demande un modèle de langage (Colab/Kaggle) ; fort potentiel pour les huit classes à F1 ≈ 0 ; risque de décalage de style |
| L17 | **Reporting** | Annoncer la macro-F1 sur 30 classes ET sur le palier A ET hF1 ; barres d'erreur au niveau du gabarit | Partiellement | Cohérence avec le professeur et honnêteté |

Réponse à ta question : **oui, il y a d'autres leviers**. Les plus prometteurs hors de tes trois : **L3 (raccourci du format du fournisseur), L2 (axes objet × action), L9 (bagging par gabarits), L10 (invariance entre gabarits), L11 (décision à masses équilibrées), L7 (pré-entraînement sur les logs), L12 (mesure hiérarchique)**. L3 est le plus surprenant : il explique pourquoi des gabarits entiers sont **absorbés par une classe voisine** et n'a jamais été regardé.

## 7. Formules maison supplémentaires

### F18 : désentrelacer format et classe (raccourci du fournisseur)
- **Identifier le format** `f(x)` sans étiquette : on retire des logs les parties variables (nombres, adresses, horodatages) et on regroupe les 40 premiers caractères du texte restant (ou le motif de l'en-tête) en F formats.
- **(a) Retirer l'en-tête** : `x' = x` privé de tout ce qui précède le premier mot du message (horodatage, hôte, `programme[pid]:`), ou masqué par un jeton de format commun.
- **(b) Repondération pour décorréler format et classe** (Kamiran et Calders 2012, à vérifier dans la source) : poids `w(f,c) = P(f)·P(c) / P(f,c)` appliqués aux logs d'entraînement : un format très lié à une seule classe est atténué.
- **(c) Mesure du raccourci** (sans entraînement) : information mutuelle normalisée `I(f ; c) / H(c)` sur les gabarits d'entraînement ; si elle est élevée, le raccourci existe.
- Hypothèse : macro-F1 ≥ V0 + 0,02 (surtout pour les classes dont le format est partagé avec d'autres classes). Coût faible.

### F19 : variance du risque entre gabarits (V-REx linéaire)
- Perte `J = (1/N_G) Σ_g L_g + λ · Var_g(L_g)` ; en pratique, repondération itérative des gabarits `q_g ∝ exp(η (L_g − L̄))` (équivalente à F10 avec un terme de variance). Pénalise le modèle dont le risque varie beaucoup d'un gabarit à l'autre.

### F20 : bagging par gabarits (subagging)
- `M = 15` modèles, chacun entraîné sur 70 % des **gabarits** tirés au hasard, marges moyennées. Réduit la dépendance aux gabarits particuliers vus. Coût : M fois le SVM.

### F21 : pré-entraînement auto-supervisé sur les logs
- Prédiction de mots masqués (MLM) sur les logs sans étiquette, puis LP-FT (F13). Sert à donner au modèle la « langue des logs ». À réserver à la vague 3 (heures de calcul).

### F22 : F-mesure hiérarchique et courbe couverture × exactitude
- hF1 : précision et rappel sur les ancêtres (classe + famille) ; courbe : exactitude des réponses en fonction de la part de logs sur lesquels on répond (repli sur la famille sinon).

### F23 : évaluation hors-un-gabarit
- Validation « leave-one-template-out » (ou groupes très petits) pour obtenir ≈ 311 verdicts par méthode ; tests appariés par gabarit (Wilcoxon, permutation). Surtout utile pour comparer des méthodes proches.

## 8. Vérifications **sans entraînement** à faire en premier (si tu es d'accord)
Il s'agit de simples **comptages** sur les données, qui ne lancent ni entraînement ni modèle :
1. **Raccourci du format (L3, F18c)** : formats d'en-tête par classe ; information mutuelle format × classe sur les gabarits ; les gabarits des huit classes à F1 ≈ 0 : quels formats, et quelles classes d'entraînement portent ces formats.
2. **Vocabulaire à utilité de classe** : parts des mots d'un gabarit de test qui existent dans les gabarits de sa classe contre dans ceux des autres classes (mesure de la « distance sémantique » de départ, sans classifieur).
3. **Taux de redondance des axes (F7)** : nombre de gabarits par axe d'action et d'objet.
Ces trois comptages disent **avant tout calcul** si L3 et F7 sont plausibles.

## 9. À décider
1. Feu vert pour les **trois comptages** ci-dessus (aucun entraînement) ?
2. Ordre des vagues après les comptages (F18 et F8 en premier ?).

---

## Rectificatif (2026-11-10) : le test v2 est intouchable, y compris pour des comptages
Consigne de l'étudiant : **aucune opération, même un simple comptage, ne doit toucher au test** ; le test v2 reste scellé jusqu'à son ouverture unique, sauf pour le sceller. Conséquences :
- Les « trois comptages » du §8 sont **retirés dans leur forme proposée** (le mot « gabarit de test » y était ambigu). Aucun comptage, aucune statistique de format, de vocabulaire ou d'axe n'est calculé sur les 57 gabarits du test v2.
- Les analyses sans entraînement, si on les refait, porteront **uniquement sur le développement**, en **validation croisée interne** (un gabarit du développement mis de côté tour à tour) ; le test v2 n'est ni chargé, ni compté, ni utilisé pour choisir un seuil, un format, un axe ou un réglage.
- Tout ce qui est écrit dans ce document sur des logs « de test » (DG2, DG3) concerne des **plis de validation internes au développement** (`role == "dev"` dans `v3_blockA.load()`), jamais le test v2.
