# Plan de travail du TP2, protocole v3 (étude statistique puis solution maison)

Document de suivi, tenu à jour. Dernière mise à jour : 2026-11-07. **Rendu : samedi 2026-11-14.**
Priorités fixées par l'étudiant : **reproductibilité, traçabilité, document de recherche**, viser le meilleur score possible, et comprendre ce qui est fait. Le travail se poursuit après le rendu.

## 0. Règles de conduite (demande de l'étudiant, 2026-11-07)
- **Méthodique de bout en bout** ; chaque choix, décision et résultat est **justifié** ; chaque hypothèse est préinscrite puis **confirmée ou réfutée**.
- **On ne supprime jamais un résultat précédent, dans aucun document** : on garde le précédent et l'actuel. Mise en œuvre : journal append-only et `REGISTRE_V3.md`, archives non écrasables (`archive/`, `scripts/archive_state.py`), étiquette git `etat-2026-11-07-avant-v3`, archivage automatique du notebook (`run_notebook.py`) et de la présentation (`build.sh`), recalcul forcé qui archive l'ancien fichier.
- Le registre complet (règles R1 à R8, décisions D1 à D6, hypothèses HA1 à HA8) est dans `REGISTRE_V3.md`.

## 1. Décisions prises
| Date | Décision | Raison |
|---|---|---|
| 2026-11-07 | Nouveau **test scellé v2** ; le test v1 (ouvert le 2026-11-05) est déclaré consommé | toute nouvelle comparaison sur les mêmes gabarits n'est plus scellée |
| 2026-11-07 | **Grille complète** pour le Transformer (6 bruits × 5 rotations × 3 graines) | l'encodeur s'entraîne sur 4 200 logs par fichier : environ 3 min par modèle, donc réalisable |
| 2026-11-07 | **Tests statistiques partout** ; unité = le gabarit ; baseline obligatoire pour chaque bloc | demande de l'étudiant |
| 2026-11-07 | Tout calcul **reprenable** : un travail terminé n'est jamais refait, un travail interrompu reprend à son dernier point | idem, et règle du projet |
| 2026-11-07 | Les **affinages** de la phase 2 se font sur le développement ; le test v2 ne s'ouvre **qu'une fois**, sur le pipeline figé (empreinte enregistrée) | éviter de régler sur le test |

## 2. Phase 1, comparer et tester (blocs A à E)
Règles communes : baseline, variantes de l'état de l'art, mêmes données et mêmes rotations ; plusieurs graines ; tests appariés ; correction de Holm pour les comparaisons multiples ; règles de décision écrites avant les chiffres ; ressemblance train/test mesurée et plafonnée.

| Bloc | Baseline | À comparer |
|---|---|---|
| A découpage | au hasard | simple par gabarit, par groupes (k plis répétés), imbriqué ; stabilité du classement des méthodes ; biais par rapport au test v2 |
| B classification | classifieur plat | hiérarchique local + repli ; clustering (prototypes, k-means) ; voisinage (kNN) ; Naive Bayes |
| C inconnu | MSP | énergie, ensemble, prototype, Mahalanobis (covariance commune, par classe, régularisée), kNN, OpenMax, ViM, résidu de PCA, densité gaussienne, LOF, forêt d'isolation |
| D attaques | sans attaque | chaque attaque à 5 degrés (tendance, moyenne), puis comparaison entre attaques ; défenses contre « sans défense » |
| E calibration | aucune | température, par vecteur, isotonique, par bacs, conformelle ; variantes pour le monde ouvert (calibrer sur classes masquées pour de faux) |
| Vectorisation | TF-IDF mots | TF-IDF caractères 3-5, Skip-gram IDF, DistilBERT, sur chacun des 6 fichiers (p = 0 à 0,5) |
| Test | | bruits variés par rotation ; ressemblance au plus proche voisin d'entraînement mesurée ; score selon la ressemblance |

## 3. Phase 2, solution maison
Pistes de l'étudiant : remplacer les valeurs variables par des marqueurs ; étiqueter (baliser) les champs pertinents ; combiner mots, lettres et Transformer ; fusionner plusieurs scores d'inconnu ; Mahalanobis régularisé ; calibration adaptée ; entraînement adversarial avec la table officielle ; **nos propres formules**, chacune expliquée, démontrée, justifiée, et mesurée avec les mêmes tests.

### 3.1 Lacunes de la littérature, donc contributions visées (remarque de l'étudiant, 2026-11-07)
Les agents de recherche n'ont rien trouvé de récent sur trois points : c'est une raison de plus de s'en inspirer et de proposer les nôtres.

| Lacune constatée | Notre proposition (à mesurer avec la batterie statistique) | Fiche formule maison |
|---|---|---|
| Les méthodes récentes de détection d'inconnus (ASH, SCALE, DICE, NNGuide, SHE, Gram, ViM, Mahalanobis relatif) sont évaluées en vision ; leur transfert aux logs n'est pas démontré | **Premier banc d'essai de ces méthodes sur des vecteurs de logs** (DistilBERT 768 valeurs, SVD de TF-IDF) sur les 5 rotations ; puis **variantes adaptées au texte** : parcimonie sur les vecteurs, covariance régularisée par classe, **fusion de scores par rangs pondérés par la fiabilité mesurée sur des classes cachées pour de faux** | F1 : score de fusion pondéré ; F2 : Mahalanobis à covariance rétrécie par classe |
| Rien de récent sur le k-means ou les prototypes pour classer, avec rejet | **Classification par gabarits-prototypes** : les logs viennent de gabarits, donc les groupes naturels existent ; on classe par le prototype de gabarit le plus proche et on rejette si on est loin de tous, avec un rayon propre à chaque gabarit | F3 : distance normalisée par le rayon du gabarit |
| Rien sur l'étiquetage des champs variables propre aux logs de sécurité | **Étiquetage typé des champs** (IP, utilisateur, chemin, port, nombre, date) remplaçant les valeurs par des marqueurs ; **TF-IDF « conscient des champs »** (vocabulaire des mots fixes séparé de celui des champs) ; mesure de l'effet sur la fuite et sur les scores | F4 : pondération des mots fixes contre les champs |

Chaque ligne devient une famille d'expériences de la phase 2, avec baseline, tests statistiques, justification écrite (motivation, propriété, ablation) et trace dans le journal des itérations (section 6).

**Boucle d'affinage** (sur plusieurs jours, n'importe où dans le pipeline) : mesurer sur le développement, trouver le maillon le plus faible, proposer une amélioration, la tester avec la même batterie statistique, garder ou rejeter, consigner (hypothèse, configuration, résultat, décision). Chaque itération a un numéro et une empreinte. Critère d'arrêt : fin de la semaine, ou gain non significatif sur trois itérations de suite.

**Fiche d'une formule maison** : motivation, définition, propriétés, justification (argument ou ablation), test statistique contre la baseline et contre la meilleure méthode existante.

## 4. Reproductibilité et traçabilité (priorité)
- **Une expérience = une unité** identifiée par une empreinte de sa configuration (données, découpage, vectorisation, modèle, graine, degré, version du code). Résultat sauvegardé sous cette empreinte : si elle existe, on la recharge ; sinon on calcule.
- **Registre append-only** `artifacts/results/v3/registry.jsonl` : une ligne par unité (empreinte, configuration, métriques, durée, machine, commit, date).
- Entraînements longs : **points de contrôle** et reprise automatique.
- Empreintes des données et des découpages (`splits_v3_meta.json`), journal d'ouverture du test v2.
- Graines fixées ; versions des bibliothèques figées (`requirements.txt`) ; scripts de lancement par machine.
- **Document de recherche** (dossier `article/`) : résumé, introduction, état de l'art, protocole, expériences, résultats, méthode proposée, limites, reproductibilité. Alimenté au fil de l'eau.

## 5. Calendrier (jusqu'au samedi 2026-11-14)
| Jour | Objectif |
|---|---|
| Sam 7 | Protocole v3, outils statistiques (fait, 15 tests), découpage v3 et test v2, exécuteur reprenable |
| Dim 8 | Blocs A et B (modèles linéaires) ; lancement de la grille Transformer en arrière-plan (Mac, puis Colab) |
| Lun 9 | Bloc C ; vectorisation × bruit |
| Mar 10 | Blocs D et E ; suite de la grille Transformer |
| Mer 11 | Fin de la phase 1 ; première itération de la solution maison |
| Jeu 12 à ven 13 | Itérations d'affinage sur le développement ; gel du pipeline ; ouverture unique du test v2 |
| Sam 14 | Document de recherche, PPT, script oral, dépôt à jour ; rendu |

## 6. Journal des itérations de la solution maison
(à remplir : numéro, hypothèse, configuration, résultat, décision)

## 7. Sources vérifiées (demande du 2026-11-07)
Pour **chaque aspect** de l'étude, du début à la toute fin du pipeline, il faut des sources vérifiées **en plus** des 73 références existantes (`etat_de_l_art/sources_verifiees.md`) : page ouverte et lue, avec le niveau de vérification (texte intégral lu, résumé lu, page lue, confirmée seulement), la date et l'adresse.
Aspects couverts : découpage et fuite ; tests statistiques ; classification hiérarchique ; clustering et voisinage ; détection d'inconnus (méthodes récentes) ; analyse et normalisation de logs, valeurs variables et marqueurs ; vectorisation ; calibration (dont monde ouvert) ; attaques et défenses (homoglyphes, entraînement adversarial) ; fusion de scores et ensembles ; reproductibilité et traçabilité.
Fichiers : `etat_de_l_art/sources_v3_stats_repro.md` et `etat_de_l_art/sources_v3_methodes.md` (puis fusion dans le notebook, section 0.1b, et dans les références de la présentation).

### 7.1 État des sources (2026-11-07)
- `etat_de_l_art/sources_v3_stats_repro.md` : 62 références vérifiées (S1 à S62) + 1 complément (S63) : découpage et fuite, tests statistiques, reproductibilité, métriques.
- `etat_de_l_art/sources_v3_methodes.md` : 89 références vérifiées (M1 à M89) : hiérarchie, prototypes, voisinage, Naive Bayes ; inconnus et conformel ; analyse de logs ; vectorisation ; calibration ; attaques et défenses ; fusion et ensembles.
- Niveau : presque toutes « résumé lu » ; les lieux de publication non affichés par la page sont marqués et **à recouper avant le dépôt**. Contrôle par sondage fait (9 entrées rouvertes, conformes).
- À faire : fusionner dans le notebook (section 0.1b) et dans les références de la présentation, au fur et à mesure que chaque méthode est utilisée.
