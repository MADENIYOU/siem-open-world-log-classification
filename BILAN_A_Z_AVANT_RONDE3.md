# Bilan de A à Z avant la ronde 3 (2026-11-10)

Document de lecture et de discussion. **Rien n'est calculé ici.** Il rassemble ce qui a été fait, confirmé, réfuté, laissé non tranché, bloc par bloc, avec les deux séries de résultats (v1 = notebook, v3 = étude statistique de la semaine). Source des chiffres : `REGISTRE_V3.md` (journal, 141 entrées), le notebook v1 (sections citées), `EXPLICATIONS_V3.md`. Les hypothèses sont notées HA à HT, HD, HE, HF, HI, HG (voir REGISTRE).

## 0. En une page

| Question | Réponse mesurée |
|---|---|
| Quel score en classes connues sur des gabarits nouveaux ? | **≈ 0,50 de macro-F1** (palier A), identique pour 19 classifieurs, 3 vectorisations, 32 réglages, le Transformer, les jetons typés, la fusion. Un découpage au hasard donne 0,986 : le score « excellent » vient de la reconnaissance de gabarits déjà vus. |
| Quel score pour détecter des classes inconnues ? | **AUROC 0,60 à 0,69** ; FPR@95 ≈ 0,85 (85 % des inconnus passent quand on garde 95 % des connus). Seul gain établi : la confiance sur la **famille** (+0,04 d'AUROC sur le MSP, 75 unités de rotations jamais vues). |
| Attaques | Les homoglyphes font perdre jusqu'à 48 % au modèle mots ; la table officielle UTS #39 les annule ; les n-grammes de lettres résistent aux fautes et aux homoglyphes mais pas au remplissage. |
| Calibration | La température n'aide pas sous décalage de gabarits (ECE 0,179 → 0,169, non significatif) ; calibrer sur les mêmes gabarits que l'entraînement trompe (0,296). |
| Transformer | Pas meilleur que TF-IDF sur 140 logs/classe (0,469 contre 0,523 sur 20 couples) ; fusion sans gain. |

Bilan des hypothèses : **37 confirmées, 30 réfutées, 9 non tranchées, 11 préinscrites sans verdict** (HA8 = test v2 scellé ; HG1 à HG10 = ronde 3 **écrite mais non lancée**).

## 1. Données et protocole

- **SIEVE** : logs SIEM synthétiques, 6 versions (p = 0 à 0,5 de perturbation), 30 classes, 8 familles ECS (taxonomie de démonstration), **311 gabarits reconstruits** dans le développement (3 à 20 000 logs par gabarit ; plafond 400 logs par gabarit et par fichier).
- **Unité de statistique = le gabarit** (pas le log). Métrique principale : macro-F1 du **palier A** (18 classes de 5 gabarits ou plus). Open-set : AUROC, FPR@95, AUPR ; calibration : ECE.
- **Protocoles** : P0 au hasard, P1 simple par gabarit, **P2 par groupes 5 plis × 5 répétitions (par défaut)**, P3 imbriqué. **Test v1 consommé** (2026-11-05). **Test v2 : 57 gabarits scellés (17,6 % des logs)**, une seule ouverture, jamais lu.
- **Paliers de classes** : A (≥ 5 gabarits : 18 classes), B (3-4 gabarits : 8 classes), C (1-2 gabarits : 4 classes ; `user-session-open` n'a qu'un gabarit).

## 2. Bloc par bloc

### Bloc A : le découpage (HA1 à HA8)
- v1 : SVM mots, P0 0,987 ; P1 0,422 ; P2 0,507 ; P3 0,511. v3 : 0,986 ; 0,471 ; 0,503 ; 0,487. Audit direct par plus proche voisin : 24,0 % des logs de test d'un découpage au hasard ont un voisin d'entraînement de cosinus ≥ 0,90, contre 1,0 % par gabarit.
- **Confirmées** : HA1 (le hasard gonfle ; version 4 après un défaut d'appariement signalé), HA1b (effet pur de la fuite sur les mêmes logs, +0,29 à +0,52), HA2 (les protocoles par gabarit classent les modèles pareil), HA4, HA5 (kNN et centroïde moins bons que le SVM), HA7. **Réfutées** : HA3 (le hasard classe autrement), **HA6 (les n-grammes de lettres ne dépassent pas les mots)**. **Préinscrite** : HA8 (quel protocole prédit le mieux le test v2 : attend l'ouverture).
- Retenu : le « 0,97 » de l'article est un score de gabarits connus ; le vrai niveau est ≈ 0,50.

### Bloc B : classification (HB1 à HB7)
- v3, P2, 25 plis : SVM mots 0,503 ; LR 0,495 ; hiérarchique 0,481 ; k-means global 0,454 ; gabarits-prototypes 0,449 ; … ; centroïde 0,406 ; HDBSCAN/DBSCAN avec rejet 0,09 à 0,11 (rejettent 82 à 85 % des logs). v1 test : plat 0,4832, hiérarchique 0,5153 ; Skip-gram 0,4027 / 0,4635.
- **Confirmées** : HB1 (la hiérarchie n'améliore pas les classes), HB5, HB7. **Réfutées** : HB2 (la hiérarchie n'améliore même pas le F1 des familles), HB3 (ni la gravité des erreurs). **Non tranchées** : HB4 (plusieurs prototypes), HB6 (clustering non supervisé contre SVM).

### Bloc C : détection d'inconnus (HC1 à HC9)
- 28 scores, 5 rotations × 25 plis = 125 unités. Meilleur : **confiance de famille 0,666** ; énergie 0,639 ; MSP 0,623 ; Mahalanobis 0,597 ; OpenMax corrigé 0,514 ; LOF 0,469. FPR@95 ≥ 0,70 pour tous.
- **Confirmées** : HC1 (aucun score n'atteint 0,80), HC2 (distance/densité ne battent pas le MSP), HC3 (les méthodes de la vision n'apportent rien), HC8 (forte variabilité entre rotations, écart-type ≥ 0,05), HC9. **Réfutées** : HC4 (notre F3 gabarits-prototypes avec rayon), HC5 (le rayon est utile), HC6 (la fusion bat ses composants). **Non tranchée** : HC7 (un frère connu cache l'inconnu).
- Défauts trouvés et corrigés (conservés au registre) : OpenMax implémenté à l'envers (0,465 → 0,514, RC3) ; explication fausse du LOF (« grappes denses ») remplacée par une décomposition en deux signaux de sens opposés (RC4).
- v1 (test consommé) : AUROC 0,728 en validation → **0,599** au test (MSP) ; FPR@95 0,92 ; la classe masquée est souvent rangée à 93-100 % dans UNE seule classe connue (`file-write` → `user-logout` 100 %, `authentication-success` → `authentication-failed` 96 %).

### Bloc V : vectorisation × bruit (HV1 à HV5)
- Macro-F1 selon p = 0 à 0,5 : mots 0,523 → 0,496 ; lettres 0,513 → 0,510 ; Skip-gram IDF 0,437 → 0,468 (monte avec le bruit).
- **Confirmées** : HV1 (les lettres résistent mieux), HV3 (Skip-gram toujours sous TF-IDF mots), HV5 (le bruit abaisse la détection d'inconnus). **Réfutée** : HV2 (le bruit ne dégrade pas chaque vectorisation). **Non tranchée** : HV4.
- v1, étape 5 : Skip-gram IDF 0,4727 ≈ TF-IDF 0,4745 (100 dimensions contre 9 880) ; CBOW 0,43 ; FastText 0,446 ; GloVe pré-entraîné 0,32 ; encodeur gelé pré-entraîné 0,4547 contre initialisé au hasard 0,4447 (indistinguables) ; fragmentation ≈ 4 jetons par mot sans effet démontré.

### Bloc T : le Transformer (HT1 à HT4, T2, I3)
- DistilBERT sans casse, 256 jetons, 2 époques, lr 3e-5, 140 logs d'entraînement par classe ; 90 modèles (6 bruits × 5 rotations × 3 graines) + 20 de réplication sur 4 nouvelles découpes.
- Grille T (une seule découpe) : Transformer 0,42 → 0,37 contre TF-IDF 0,39 → 0,36. **Réplication T2 : Transformer 0,469 contre TF-IDF 0,523** (−0,054, IC95 [−0,086 ; −0,020]) : **HT1 tranchée**, l'avance de la grille venait d'une découpe favorable. Détection d'inconnus : Transformer plus faible que TF-IDF (MSP 0,56 contre 0,60).
- **Confirmées** : HT1/HT1b, HT3 (famille meilleure que le MSP, +0,07). **Réfutée** : HT4 (le Transformer perd PLUS avec le bruit : 0,057 contre 0,031), HF15 (la fusion n'améliore pas : 0,508 sous TF-IDF 0,523). **Non tranchées** : HT2/HT2b (Mahalanobis +0,037 sur le MSP du Transformer, IC95 [0,022 ; 0,052] sur 50 couples, compatible avec le seuil 0,03), HF16.
- v1 : écart de précision de l'encodeur selon la fragmentation non soutenu ; « affinage sur 440 gabarits = mémorisation » et dépendance à la graine **non testés** à l'époque.

### Bloc D : attaques et défenses (HD1 à HD7 ; v1 sections 8.6 et 9.3-9.12)
- v3 (modèle mots, degré maximal) : fautes −0,088 (−16,7 %), **homoglyphes −0,254 (−48,2 %)**, remplissage −0,128 (−24,4 %). Lettres : −0,006 ; −0,024 ; −0,051 en moyenne. Normalisation officielle UTS #39 : perte résiduelle 0 aux cinq degrés.
- **Confirmées** : HD1 à HD6. **Réfutée** : HD7 (la confiance de famille perd PLUS que le MSP sous attaque).
- **Entraînement adversarial (v1, étape 9, 59 940 logs propres + 59 940 copies attaquées)** : baisse moyenne 0,0547 (aucune parade) → 0,0275 (normalisation) → 0,0275 (adversarial) → **0,0069 (les deux)** ; mais **l'entraînement adversarial ne généralise pas à une attaque jamais vue** (homoglyphes 8,4 % contre 8,2 % sans parade) ; il aide les attaques vues (8,2 % → 3,8 %, padding 4,9 % → 0,5 %) ; il redresse l'AUROC sous homoglyphes (+0,033) au prix de plus de connus rejetés ; les fautes ne sont pas traitées. **9.12 : la parade « table maison » était circulaire** (même table que l'attaque) ; avec la table officielle, D4 (NFKC + table complète) annule toutes les attaques de la table.
- **Lacune** : l'entraînement adversarial n'a **pas** été refait en v3 (protocole P2, plusieurs degrés, tests statistiques, attaque jamais vue + normalisation officielle).

### Bloc E : calibration (HE1 à HE6)
- ECE : température 0,169 ; Platt 0,173 ; aucune 0,179 ; isotonique 0,186 ; binning 0,190 ; vector scaling 0,226 ; température sur les mêmes gabarits 0,296 ; sur classes cachées 0,323. Conforme (90 %) : couverture 0,899 avec gabarits distincts, 0,136 avec les mêmes, au prix d'ensembles de 11,9 classes sur ≈ 24.
- **Confirmées** : HE3, HE5, HE6. **Réfutées** : HE1 (toute calibration réduit l'ECE), HE2, HE4 (erreur de formulation reconnue : le vector scaling ne conserve pas l'ordre). v1 : température T = 1,62, ECE 0,150 → 0,095 en validation, effet **non retrouvé** en v3 (protocole plus strict).

### Phase 2 (itérations I1 à I7c)
| Itération | Idée | Résultat |
|---|---|---|
| I1 | vocabulaire restreint aux mots présents dans ≥ m gabarits, marqueur de valeur, pondération par gabarit | HF1 à HF6 **réfutées** ; restreindre dégrade (T3 0,472 ; T5 0,418) |
| I1b | mots + lettres | HF7, HF8 **confirmées** (famille +0,029), HF9 non tranchée (classes −0,001, IC95 [−0,011 ; 0,009]) |
| I2 | jetons typés (programme, champs, types, forme) | HF10 à HF12 **réfutées** (0,489 ; structure seule 0,265) |
| I4, I7a/b/c | rejet par la famille, 24 combinaisons, 3 jeux de rotations | **+0,04 d'AUROC confirmé** (75 unités) ; FPR@95 −0,02 (HI7b réfutée) |
| I5, I6, I6b | réglage de 32 configurations (C, n-grammes, casse, modèle) | maximum de grille +0,0085 puis **−0,003 sur nouveaux plis** (20 plis sur 25 défavorables) ; 25 configurations sur 32 indiscernables du meilleur (HF19 confirmée) |
| T2/I3 | réplication Transformer + fusion | voir bloc T |

## 3. Entraînement et validation : ce qui a été examiné
- **Validation contre test (v1)** : l'AUROC d'inconnu tombe de 0,728 à 0,599 ; la sélection explique au plus 0,01 à 0,03, le reste vient de la variabilité entre gabarits (rotation 5 sous 0,5 au test).
- **Choix du C** (1, 4, 16 : 0,4314 à 0,4344), SVD à 50 puis 100 dimensions (50 pénalisait Mahalanobis), fenêtre 256 jetons, avec/sans casse : aucun ne change l'ordre de grandeur.
- **Optimisme de sélection** : prouvé en I6b (le maximum d'une grille de 32 ne tient pas sur de nouveaux plis).
- **Données fraîches** (v1 5.9) : sur 35 000 logs du professeur par version, le même modèle fait 0,81 (gabarits connus) contre 0,64 en validation (gabarits nouveaux).

## 4. Ce que dit DG2 sur la cause du plafond (exploratoire)
1. **Agréger les marges par VRAI gabarit au test ne change rien** (0,4968 contre 0,4965) : ce ne sont pas des logs isolés qui se trompent mais des **gabarits entiers**. Lisser par plus proches voisins du test (5 à 50) ne gagne rien non plus.
2. **Huit classes ont un F1 voisin de 0** (file-read, file-write, file-modification, file-deleted, directory-deleted, file-action-failure, user-session-open, http-request-failure). Elles ont **1 à 3 gabarits** dans le développement : avec un gabarit au test, il en reste 0 à 2 pour apprendre (cas limite d'apprentissage à un exemple). Exemple : le test « Accessed URL … » de `file-read` est classé connexion échouée, alors que l'entraînement dit « opened-file ».
3. v1 (test) : des classes riches en gabarits échouent aussi (`connection-closed`, 12 gabarits, F1 ≈ 0 ; `network-traffic`, 5 gabarits) : **avoir beaucoup de gabarits ne suffit pas**.
4. Rappel des échecs : réglages, vocabulaire, structure, Transformer et fusion n'ont pas bougé le plafond ; **seule** la composante lettres améliore la famille.

## 5. Les neuf non tranchées et ce qui les trancherait
HB4 et HB6 (prototypes multiples, clustering : plus de plis ou une règle moins stricte) ; HC7 (frère connu : distinguer les classes masquées selon la présence d'une classe sœur connue, plus de rotations) ; HV4 (rang des vectorisations au bruit maximal) ; HT2/HT2b (le seuil 0,03 coïncide avec l'effet : sans enjeu pratique) ; HF9 (équivalence des classes entre mots+lettres et mots : IC95 dépasse le seuil −0,01 de 0,0009) ; HF13 (non testée) ; HF16 (fusion, famille +0,008).

## 6. Lacunes : ce qui n'a PAS été essayé
- Sémantique : embeddings gelés **pondérés** par moyenne de couches, vecteurs d'étiquette (nom de la classe), lexique de synonymes d'actions, **modèles de phrases pré-entraînés** (non disponibles hors ligne : seulement `distilbert-base-uncased`), LLM en zero/few-shot.
- Apprentissage avec peu de gabarits : augmentation par suppression/mélange, méta-apprentissage, prototypes appris, discriminant calculé sur les **moyennes par gabarit**.
- Rejet : pseudo-inconnus par synthèse (outlier exposure), seuils par famille, rejet à trois niveaux (classe / famille / inconnu), entraînement contrastif.
- Données : usage de **tous** les logs (plafond de 400 par gabarit : l'effet n'a pas été mesuré), poids de classe pour les classes à peu de gabarits.
- Robustesse : entraînement adversarial en v3 (voir §2, bloc D).
- Annotation : taxonomie à 8 familles supposée (hypothèse de démonstration) : à confirmer avec le professeur.

## 7. Hypothèses déjà préinscrites mais NON lancées (ronde 3)
D26 et HG1 à HG10 (embeddings gelés, prior de sens sur le nom de la classe, lexique de concepts, suppression aléatoire de mots, discriminant au niveau du gabarit, porte de confirmation). Elles sont dans le journal sous le statut « préinscrite » ; aucun calcul n'a été lancé. À garder, modifier (nouvelle version) ou compléter après la recherche d'état de l'art : voir `etat_de_l_art/sources_v3_ronde3.md` quand elle sera écrite.

## 8. Points à décider ensemble
1. Garder, remplacer ou compléter D26/HG1 à HG10 après l'état de l'art.
2. Refaire l'entraînement adversarial en v3 (oui/non, quelles attaques).
3. Mesurer l'effet du plafond de 400 logs par gabarit et d'un apprentissage sur tous les logs.
4. Quelles ressources (Mac seul, ou aussi Kaggle/Colab pour des modèles de phrases / LLM) : le Mac seul n'a que DistilBERT.
5. Quand figer le pipeline et ouvrir le test v2.
