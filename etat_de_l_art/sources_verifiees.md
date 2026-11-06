# Sources de l'état de l'art du TP2 (vérifiées en ouvrant la page, 2026-11-05)

Niveau de vérification : **résumé lu** = la page arXiv ou éditeur a été ouverte et le résumé lu ; **texte intégral lu** = l'article entier lu ; **non vérifié** = page inaccessible. Ce fichier est une **base de travail** : il n'est pas dans le notebook.

## Bloc C : détection d'inconnus (open-set / OOD)

| Réf | Année | Méthode | Idée (paraphrase du résumé) | Exige | Niveau | URL |
|---|---|---|---|---|---|---|
| OpenMax, Bendale et Boult | 2015-2016 | OpenMax | Un réseau doit toujours choisir parmi ses classes ; OpenMax ajoute une couche qui estime, à partir des activations de l'avant-dernière couche et d'une méta-reconnaissance, la probabilité d'une classe inconnue | activations/logits ; ajustement sur le jeu d'entraînement | résumé lu | https://arxiv.org/abs/1511.06233 |
| ODIN, Liang et al. | 2017 (ICLR 2018) | ODIN | Température et petites perturbations de l'entrée pour écarter les scores softmax des entrées connues et inconnues, sans modifier le modèle | modèle entraîné ; gradients de l'entrée | résumé lu | https://arxiv.org/abs/1706.02690 |
| Mahalanobis, Lee et al. | 2018 | distance de Mahalanobis | Gaussiennes par classe sur les features ; score = distance de Mahalanobis aux classes | features d'un modèle entraîné | résumé lu | https://arxiv.org/abs/1807.03888 |
| Energy, Liu et al. | 2020 | énergie | Score d'énergie calculé à partir des sorties du classifieur, au lieu de la confiance softmax jugée trop sûre d'elle | logits | résumé lu | https://arxiv.org/abs/2010.03759 |
| Outlier Exposure, Hendrycks et al. | 2018 (ICLR 2019) | OE | Entraîner le détecteur avec un jeu auxiliaire d'exemples « autres » | jeu d'outliers auxiliaire | résumé lu | https://arxiv.org/abs/1812.04606 |
| kNN profond, Sun et al. | 2022 | kNN | Distance au k-ième plus proche voisin parmi les données connues, sans supposer de forme de distribution | features, données d'entraînement | résumé lu | https://arxiv.org/abs/2204.06507 |
| ViM, Wang et al. | 2022 (CVPR) | ViM | Combine un score d'espace de features (partie hors sous-espace principal) et les logits | features + logits | résumé lu | https://arxiv.org/abs/2203.10807 |
| Vaze et al. | 2021 (ICLR 2022) | « bon classifieur fermé » | La capacité à rejeter est fortement corrélée à l'exactitude en fermé ; un score simple (logit maximal) bien entraîné atteint l'état de l'art | rien de plus | résumé lu | https://arxiv.org/abs/2110.06207 |
| OpenOOD, Yang et al. | 2022 | benchmark | Code unifié pour plus de 30 méthodes OOD, évaluation commune | — | résumé lu | https://arxiv.org/abs/2210.07242 |
| OpenOOD v1.5, Zhang et al. | 2023 | benchmark | Benchmark standardisé, grande échelle (ImageNet, CLIP, DINOv2), « full-spectrum » | — | résumé lu | https://arxiv.org/abs/2306.09301 |
| Geng et al. | 2018-2020 | survey OSR | Revue de la reconnaissance en monde ouvert (définitions, évaluation, comparaisons) | — | résumé lu | https://arxiv.org/abs/1811.08581 |
| Yang et al. | 2021-2024 | survey OOD | Cadre unifié (détection d'anomalies, de nouveauté, OSR, OOD, outliers) | — | résumé lu | https://arxiv.org/abs/2110.11334 |

### Bloc C (suite) : détection d'inconnus en texte (NLP), prototypes, ensembles, incertitude

| Réf | Année | Méthode | Idée (paraphrase du résumé) | Exige | Niveau | URL |
|---|---|---|---|---|---|---|
| Zhou et al. (EMNLP 2021) | 2021 | perte contrastive + Mahalanobis | Affiner un Transformer avec une perte contrastive à marge, puis score de Mahalanobis sur l'avant-dernière couche ; sans données hors distribution | ré-entraînement, features | résumé lu | https://arxiv.org/abs/2104.08812 |
| Arora et al. | 2021 | types de textes OOD | Distingue décalage de fond et décalage sémantique ; l'estimation de densité bat la calibration sur le fond mais pas sur le sémantique ; les deux ratent souvent les cas difficiles | — | résumé lu | https://arxiv.org/abs/2109.06827 |
| Hendrycks et al. | 2020 | Transformers préentraînés | Sur 7 jeux NLP, les Transformers préentraînés perdent moins en exactitude sous décalage et détectent mieux l'OOD que sacs de mots, ConvNets, LSTM ; la taille seule ne suffit pas | — | résumé lu | https://arxiv.org/abs/2004.06100 |
| Podolskiy et al. | 2021 | Mahalanobis + Transformer | Transformer affiné + distance de Mahalanobis donne la meilleure détection d'intentions hors domaine, sans données hors domaine ; représentations resserrées | features d'un modèle affiné | résumé lu | https://arxiv.org/abs/2101.03778 |
| Zhang et al. (AAAI 2021) | 2020 | frontière adaptative | Post-traitement : frontière sphérique par classe connue apprise sur les features, perte équilibrant risque empirique et risque d'espace ouvert | features, données connues seulement | résumé lu | https://arxiv.org/abs/2012.10209 |
| Yang et al. (prototypes) | 2018 | prototypes | Classer par similarité à des prototypes appris ; perte de prototype resserrant les clusters ; meilleur rejet | entraînement spécifique | résumé lu | https://arxiv.org/abs/1805.03438 |
| ReAct, Sun et al. | 2021 | activations rectifiées | Réduit la sur-confiance en tronquant les activations anormales de l'avant-dernière couche | accès aux activations | résumé lu | https://arxiv.org/abs/2111.12797 |
| Deep ensembles, Lakshminarayanan et al. | 2016 (NIPS 2017) | ensembles | Plusieurs réseaux entraînés indépendamment ; incertitude bien calibrée, parallélisable | N entraînements | résumé lu | https://arxiv.org/abs/1612.01474 |
| MC dropout, Gal et Ghahramani | 2015 (ICML 2016) | dropout bayésien | Le dropout actif à l'inférence approxime une inférence bayésienne ; incertitude sans changer l'entraînement | modèle avec dropout | résumé lu | https://arxiv.org/abs/1506.02142 |
| Lang et al. (TMLR 2024) | 2023 | survey OOD en NLP | Première revue centrée sur le NLP : définitions, taxonomie selon les données et étiquettes disponibles, jeux, métriques | — | résumé lu | https://arxiv.org/abs/2305.03236 |
| Baran et al. | 2023 | benchmark méthodes classiques OOD en texte | Huit méthodes adaptables sans données supplémentaires ; elles ratent beaucoup de décalages, surtout décalage de fond et désordre des mots | — | résumé lu | https://arxiv.org/abs/2307.07002 |
| Costache et al. | 2025 | survey classification de texte sous décalage de classes | Revue de la classification de texte en monde ouvert (Universum, zéro-coup, open-set) | — | résumé lu | https://arxiv.org/abs/2502.12965 |

## Bloc B : classification hiérarchique

| Réf | Année | Thème | Idée (paraphrase) | Limite pour nous | Niveau | URL |
|---|---|---|---|---|---|---|
| Silla et Freitas (DMKD 22) | 2011 | survey classification hiérarchique | Définit la tâche, propose un cadre unifiant (approches locales / globales) et compare conceptuellement avantages et inconvénients | pas de monde ouvert, pas de texte spécifique | résumé lu (via recherche, DOI 10.1007/s10618-010-0175-9) | https://link.springer.com/doi/10.1007/s10618-010-0175-9 |
| HiAGM, Zhou et al. (ACL 2020) | 2020 | texte hiérarchique | Hiérarchie vue comme graphe orienté ; encodeurs sensibles à la hiérarchie ; deux variantes | classes fermées | résumé lu | https://aclanthology.org/2020.acl-main.104/ |
| HiTIN, Zhu et al. (ACL 2023) | 2023 | texte hiérarchique | Réseau léger basé sur la seule structure de l'arbre (entropie structurelle) | classes fermées | résumé lu | https://arxiv.org/abs/2305.15182 |
| Bertinetto et al. (CVPR 2020) | 2019 | « Making Better Mistakes » | Deux modifications simples de l'entropie croisée pour rendre les erreurs moins graves dans la hiérarchie | vision ; inconnus non traités | résumé lu | https://arxiv.org/abs/1912.09393 |
| Kosmopoulos et al. | 2013 | métriques hiérarchiques | Cadre unifié et nouvelles mesures pour évaluer la classification hiérarchique | — | résumé lu | https://arxiv.org/abs/1306.6802 |
| Linderman et al. | 2022 | hiérarchique + OOD | Un détecteur qui prédit à un niveau plus grossier quand l'entrée est ambiguë, au lieu de dire seulement « inconnu » | vision | résumé lu | https://arxiv.org/abs/2209.04493 |
| ProTeCt, Wu et al. (CVPR 2024) | 2023 | taxonomie ouverte | Cohérence hiérarchique des prédictions pour modèles vision-langage ; nouvelles métriques | vision-langage | résumé lu | https://arxiv.org/abs/2306.02240 |
| Hannum et al. | 2024 | OSR hiérarchique | Construit l'arbre des classes dans l'espace d'embedding par regroupement ascendant contraint | vision (AwA2) | résumé lu | https://arxiv.org/abs/2411.02635 |
| Wallin et al. | 2026 | OSR hiérarchique semi-supervisé | Place les classes nouvelles sous le groupe le plus adapté ; enseignant-élève avec pseudo-étiquettes | vision (iNaturalist) | résumé lu | https://arxiv.org/abs/2601.16541 |

## Bloc A : logs et sécurité

| Réf | Année | Thème | Idée (paraphrase) | Ce qu'il ne traite pas | Niveau | URL |
|---|---|---|---|---|---|---|
| DeepLog, Du et al. (CCS 2017) | 2017 | anomalies dans les logs | LSTM qui modélise le journal comme une séquence ; une déviation de la séquence normale signale une anomalie | classification de types d'événements ; monde ouvert hiérarchique | résumé lu (via recherche, DBLP) | https://dblp.dagstuhl.de/rec/conf/ccs/Du0ZS17.html |
| LogBERT, Guo et al. | 2021 | anomalies dans les logs | BERT auto-supervisé qui apprend les motifs de séquences normales avec deux objectifs | idem | résumé lu | https://arxiv.org/abs/2103.04475 |
| Landauer et al. | 2022-2023 | survey | Apprentissage profond pour l'anomalie dans les logs : architectures, prétraitement, détection, évaluation | — | résumé lu | https://arxiv.org/abs/2207.03820 |
| Loghub, Zhu et al. | 2020 | jeux de logs | 19 jeux de logs de systèmes variés avec statistiques et résultats de référence | pas de taxonomie d'événements de sécurité | résumé lu | https://arxiv.org/abs/2008.06448 |

### Bloc A (suite) : sécurité, logs, monde ouvert en intrusion

| Réf | Année | Thème | Idée (paraphrase) | Niveau | URL |
|---|---|---|---|---|---|
| Artioli et al., SIEVE (Computer Networks 266) | 2025 | jeu SIEVE | Jeu de logs SIEM généré à partir de gabarits (SPICE) ; SVM (MaF1 0,9323 à 0,9737) et BERT (0,9528 à 0,9730) sur SIEVE ; BERT peu robuste sur logs réels | texte intégral lu (en partie, PDF local `TP/sieve-journal.pdf`) | https://doi.org/10.1016/j.comnet.2025.111330 |
| Karlsen et al. | 2023 | LLM pour logs de sécurité | 60 modèles (BERT, RoBERTa, DistilRoBERTa, GPT-2, GPT-Neo) affinés sur 6 jeux de logs ; meilleur : DistilRoBERTa, F1 moyen 0,998 ; le résumé ne parle ni de fuite ni de découpage | résumé lu | https://arxiv.org/abs/2311.14519 |
| Akhtar et al. | 2025 | survey LLM et logs de sécurité | Revue des usages de LLM (affinage, RAG, in-context) pour l'analyse de journaux d'événements | résumé lu | https://arxiv.org/abs/2502.00677 |
| Souza et al. | 2021 (Computers & Security 2025) | intrusion en monde ouvert | Classifieur de flux réseau à énergie adapté au monde ouvert, connus et attaques jamais vues | résumé lu | https://arxiv.org/abs/2109.11224 |
| VAEMax, Qiu et al. | 2024 | intrusion en monde ouvert | OpenMax en premier étage puis autoencodeur variationnel sur les classes prédites ; CIC-IDS2017 et CSE-CIC-IDS2018 | résumé lu | https://arxiv.org/abs/2403.04193 |
| Dhamija et al. | 2018 | agnostophobie | Seuiller le softmax ou ajouter une classe « fond » ne suffit pas ; pertes entropiques avec exemples négatifs | résumé lu | https://arxiv.org/abs/1811.04110 |

## Bloc D : robustesse du texte

| Réf | Année | Thème | Idée (paraphrase) | Niveau | URL |
|---|---|---|---|---|---|
| Boucher et al. (IEEE S&P) | 2021 | attaques invisibles | Caractères cachés, homoglyphes, réordonnancement, suppression : un seul changement dégrade, trois cassent la plupart des modèles ; défense recommandée : assainir l'entrée | résumé lu | https://arxiv.org/abs/2106.09898 |
| Pruthi et al. (ACL 2019) | 2019 | fautes de frappe | Étage de reconnaissance de mots avant le classifieur ; réduction relative de l'erreur d'environ 32 % | résumé lu | https://arxiv.org/abs/1905.11268 |
| Jones et al. (ACL 2020) | 2020 | encodages robustes | Goulot d'étranglement discret donnant une robustesse prouvable aux fautes de frappe avec BERT | résumé lu | https://arxiv.org/abs/2005.01229 |
| FreeLB, Zhu et al. | 2019 | entraînement adversarial | Bruit adversarial sur les embeddings de mots, perte minimisée sur un voisinage | résumé lu | https://arxiv.org/abs/1909.11764 |
| TextAttack, Morris et al. | 2020 | cadre d'attaques | Bibliothèque modulaire d'attaques, d'augmentation et d'entraînement adversarial | résumé lu | https://arxiv.org/abs/2005.05909 |
| Morris et al. (réévaluation) | 2020 | réalisme des attaques | Un exemple adversarial doit tromper le modèle ET respecter des règles linguistiques ; avec des seuils plus stricts, le taux de succès chute de plus de 70 points | résumé lu | https://arxiv.org/abs/2004.14174 |
| AdvGLUE, Wang et al. | 2021 | benchmark | 14 attaques sur GLUE avec validation humaine ; tous les modèles testés chutent fortement | résumé lu | https://arxiv.org/abs/2111.02840 |
| TextFooler, Jin et al. (AAAI 2020) | 2019 | attaque par synonymes | Remplacement de mots pour tromper BERT en préservant sens et grammaire | résumé lu | https://arxiv.org/abs/1907.11932 |
| BERT-Attack, Li et al. | 2020 | attaque | Utilise un modèle de langue masqué pour proposer des remplacements | résumé lu | https://arxiv.org/abs/2004.09984 |
| HotFlip, Ebrahimi et al. (ACL 2018) | 2017 | attaque boîte blanche | Échanges de caractères guidés par les gradients ; permet l'entraînement adversarial | résumé lu | https://arxiv.org/abs/1712.06751 |
| Unicode UTS #39 (v18.0.0, 2026-08-27) | — | confusables | « Squelette » pour comparer des chaînes visuellement similaires ; **à usage de comparaison interne, pas pour l'affichage ni la normalisation** | page lue (début) | https://www.unicode.org/reports/tr39/ |
| Dalvi et al. (KDD 2004) | 2004 | classification adverse, spam | Texte intégral lu : les spammeurs insèrent des mots « non-spam » et cassent les mots par de la ponctuation | texte intégral lu | https://homes.cs.washington.edu/~pedrod/papers/kdd04.pdf |
| Lowd et Meek (CEAS 2005) | 2005 | good word attacks | Existence confirmée (DBLP, via recherche) ; résumé non lu ; un compte rendu secondaire signale qu'ajouter des mots aléatoires est peu efficace contre un filtre bayésien naïf | référence confirmée, résumé non lu | https://dblp.uni-trier.de/rec/conf/ceas/LowdM05.html |

## Bloc E : calibration et baselines

| Réf | Année | Thème | Idée (paraphrase) | Niveau | URL |
|---|---|---|---|---|---|
| Guo et al. | 2017 | calibration | Les réseaux profonds sont mal calibrés ; la mise à l'échelle par température corrige bien | résumé lu | https://arxiv.org/abs/1706.04599 |
| Desai et Durrett | 2020 | calibration des Transformers | BERT et RoBERTa bien calibrés en domaine, moins mal calibrés hors domaine que les bases ; température utile en domaine, lissage d'étiquettes hors domaine | résumé lu | https://arxiv.org/abs/2003.07892 |
| Ovadia et al. | 2019 | incertitude sous décalage | La calibration a posteriori et plusieurs méthodes se dégradent sous décalage ; les méthodes qui moyennent plusieurs modèles tiennent mieux | résumé lu | https://arxiv.org/abs/1906.02530 |
| Lin et al. (ACL 2023) | 2023 | baseline linéaire | Les classifieurs linéaires sur sac de mots doivent être lancés à côté des modèles avancés : souvent performants, rapides, robustes, et ils aident à vérifier la crédibilité des résultats | résumé lu | https://arxiv.org/abs/2306.07111 |
| DistilBERT, Sanh et al. | 2019 | modèle | BERT distillé : 40 % plus petit, environ 60 % plus rapide, environ 97 % de la compréhension | résumé lu | https://arxiv.org/abs/1910.01108 |
| BERT, Devlin et al. | 2018 | modèle | Encodeur bidirectionnel préentraîné, état de l'art sur 11 tâches | résumé lu | https://arxiv.org/abs/1810.04805 |
| Wang et Manning (ACL 2012) | 2012 | baselines et bigrammes | Fiche bibliographique confirmée ; résumé non affiché par la page | référence confirmée, résumé non lu | https://aclanthology.org/P12-2018/ |

## Vérifications complémentaires (2026-11-05, après la demande « vérifie »)

| Réf | Résultat de la vérification | Niveau | Source lue |
|---|---|---|---|
| Lowd et Meek (CEAS 2005) | Résumé lu en entier : une « good word attack » consiste à insérer ou ajouter des mots indicatifs d'un courriel légitime ; attaques **passives** (sans retour du filtre) : 50 % du spam bloqué passe avec 150 mots ou moins ; attaques **actives** (requêtes test) : 30 mots. Le texte précise que des mots tirés au hasard dans un dictionnaire sont inefficaces, alors que des mots **fréquents** font bien mieux | texte (résumé et corps) lu | PDF CEAS 2005 (`ceas.cc/2005/papers/125.pdf`) |
| Wang et Manning (ACL 2012) | Résumé lu en entier : NB et SVM servent de baselines mais varient beaucoup selon variante, descripteurs et jeu ; les bigrammes aident de façon constante en sentiment ; NB meilleur que SVM sur courts extraits, l'inverse sur documents longs ; une variante SVM utilisant les rapports log-count de NB (NBSVM) performe bien partout | résumé lu (PDF) | https://aclanthology.org/P12-2018.pdf |
| Kwon et al. (Findings EACL 2023) « Hierarchical Label Generation for Text Classification » | Le résumé dit que gérer des étiquettes **inconnues** tout en tenant compte de la **hiérarchie** des étiquettes est « un problème encore ouvert » pour les applications réelles ; ils proposent un classifieur génératif Seq2Seq | résumé lu (PDF) | https://aclanthology.org/2023.findings-eacl.46.pdf |
| Shu et al. | 2017 | DOC : classification ouverte de documents texte | Les classifieurs supervisés supposent que toutes les classes de test ont été vues ; approche profonde pour la classification en monde ouvert (le mécanisme précis reste à lire dans le texte) | résumé lu | https://arxiv.org/abs/1709.08716 |
| Erlygin et al. | 2026 | incertitude pour le texte en monde ouvert | Adapte HolUE au texte (authorship, intentions, thèmes) ; deux signaux d'incertitude ; améliore le Prediction Rejection Ratio | résumé lu | https://arxiv.org/abs/2604.08560 |
| Vaarandi et al. | 2024 | gabarits dans les logs de sécurité | Détection non supervisée de gabarits d'événements par LLM | résumé lu | https://arxiv.org/abs/2409.05045 |

## Protocole de recherche pour la lacune (hiérarchie + monde ouvert + logs SIEM)

Date : 2026-11-05. Sources interrogées : arXiv (pages de résumé ouvertes), ACL Anthology, Springer/DBLP/Semantic Scholar (API) et moteur de recherche web (modes standard et étendu). Requêtes effectuées (résultats pertinents relevés) :
1. « hierarchical open-set text classification unknown classes taxonomy » (2 formulations) : trouvé uniquement de la vision (Wallin 2026, Linderman 2022, Hannum 2024, ProTeCt 2024) et du texte à plat (surveys Lang 2023, Costache 2025, Erlygin 2026) ; Kwon 2023 dit que le cas texte + hiérarchie + étiquettes inconnues est « ouvert ».
2. « open-world OR open-set classification of security log events SIEM unknown event types » : trouvé des brevets (SIEM + classifieur de types d'événements), SIEVE, de l'intrusion réseau en monde ouvert (OpenMax, énergie) ; **aucune** classification hiérarchique de logs SIEM en monde ouvert.
3. « novel log type detection / unseen log event / open-set log parsing » : travaux sur l'analyse de gabarits et l'anomalie (LogParse, NeuralLog, ULog, Vaarandi 2024), **non formulés** comme classification en monde ouvert.
4. Citations de SIEVE (API Semantic Scholar, DOI 10.1016/j.comnet.2025.111330) : **6 travaux citants** (2025-2026) ; aucun ne porte sur la classification hiérarchique ou le monde ouvert (titres : revue SIEM-SOAR, audit de conformité cloud, bancs d'essai cybersécurité, sécurité de centres de données loués, priorisation d'alertes Splunk, évaluation de systèmes de détection d'intrusion APT).
Limites déclarées : aucune base ne garantit l'exhaustivité (couverture variable de Semantic Scholar, moteur de recherche US) ; la lacune est donc affirmée **dans le périmètre de ce protocole**, avec les requêtes ci-dessus pour la reproduire.

## Bloc A : découpage et validation croisée

| Réf | Année | Idée (paraphrase) | Niveau | URL |
|---|---|---|---|---|
| scikit-learn, « Cross-validation » | doc | k plis ; `GroupKFold` et `StratifiedGroupKFold` (un groupe jamais coupé) ; fuite par réglage répété sur le test ou prétraitement ajusté avant découpage ; jeu de test gardé à part | page lue | https://scikit-learn.org/stable/modules/cross_validation.html |
| Cawley et Talbot (JMLR 11) | 2010 | Le critère de sélection de modèle doit avoir une faible variance ; sinon surapprentissage de la sélection et biais d'évaluation | résumé lu | https://jmlr.org/papers/v11/cawley10a.html |
| Varoquaux | 2017 | Avec peu d'échantillons, la validation croisée a de grandes marges d'erreur et l'écart entre plis les sous-estime | résumé lu | https://arxiv.org/abs/1706.07581 |
| scikit-learn, « Nested versus non-nested cross-validation » | doc | Boucle intérieure pour régler, boucle extérieure pour évaluer ; sans imbrication, le score est optimiste (écart moyen d'environ 0,0076 sur l'exemple iris) | page lue | https://scikit-learn.org/stable/auto_examples/model_selection/plot_nested_cross_validation_iris.html |
| scikit-learn, GroupShuffleSplit / LeaveOneGroupOut / LeavePGroupsOut | doc | Découpages aléatoires indépendants de groupes entiers ; un groupe laissé de côté par découpage ; toutes les combinaisons de P groupes | page lue | https://scikit-learn.org/stable/modules/cross_validation.html |
