# Rapport de projet — Classification hiérarchique de logs SIEM en monde ouvert

**Projet 2 — Open-World Hierarchical Cybersecurity Log Classification with Uncertainty-Aware Deep Learning**  
**Support d’analyse :** notebook `Open_World_SIEVE_nb.ipynb` et document `Propositions_papiers_SIEVE_pipelines.pdf`  
**Nature du travail :** projet académique / projet de classe

------------------------------------------------------------------------

## Résumé exécutif

Ce projet étudie comment un système de classification de logs de cybersécurité peut faire deux choses à la fois :

1.  reconnaître correctement les événements appartenant aux catégories qu’il a apprises ;
2.  éviter de forcer une prédiction lorsqu’un événement appartient à une catégorie qu’il n’a jamais rencontrée pendant l’entraînement.

Le problème est important dans un contexte SIEM (*Security Information and Event Management*). Un SIEM reçoit des événements issus de sources et de composants différents. Un classificateur classique entraîné sur un ensemble fermé de catégories est généralement obligé de choisir l’une de ces catégories, même si le nouvel événement ne correspond à aucune d’elles. Le projet ajoute donc une capacité de rejet : le modèle peut répondre **« événement inconnu »** au lieu de produire une classe potentiellement trompeuse.

La solution implémentée combine un encodeur textuel DistilBERT, une organisation hiérarchique des 30 classes SIEVE en 9 familles, plusieurs méthodes de calcul d’un score de familiarité et un seuil de décision calibré sur des exemples connus de validation. Le notebook compare également un classificateur hiérarchique à un classificateur plat, teste plusieurs ensembles de classes masquées et mesure l’effet des versions perturbées de SIEVE.

**Conclusion générale :** le notebook couvre une grande partie du cœur du Projet 2 et constitue une implémentation substantielle du sujet. Les expériences montrent que la hiérarchie améliore certains résultats de classification fermée par rapport au modèle plat dans l’expérience initiale, mais qu’elle ne domine pas systématiquement ce dernier en détection open-set. Dans les évaluations strictes agrégées, le meilleur AUROC de détection des inconnus est obtenu par le modèle plat associé à la distance aux prototypes (0,727 ± 0,096). Le projet montre donc surtout qu’il faut évaluer séparément la qualité de classification, la détection des inconnus et la robustesse.

Le travail présente aussi des limites : seules 19 classes sur 30 disposent d’un découpage strict par templates ; le test de transfert CDS prévu dans le document de proposition n’a pas été exécuté dans le notebook ; et le filtrage de la vue stricte de l’évaluation open-set est asymétrique (il porte sur les exemples connus, pas sur les inconnus). Ces points sont détaillés en section 13.

------------------------------------------------------------------------

## 1. Contexte et problématique

### 1.1 Qu’est-ce qu’un log de sécurité ?

Un log est un enregistrement textuel produit par un système, une application, un serveur ou un équipement. Il décrit généralement un événement : une tentative d’authentification, une connexion réseau, une modification de fichier, le démarrage d’un processus, etc.

Exemple simplifié :

``` text
[error] [client 217.121.56.73] user alice: authentication failure
```

Un analyste ou un outil SIEM doit pouvoir déterminer ce que représente cet événement. Dans le dataset SIEVE, chaque log est associé à une étiquette parmi 30 catégories.

### 1.2 Pourquoi la classification classique est insuffisante

Dans une classification dite **fermée** (*closed-set*), le modèle connaît à l’avance toutes les classes possibles. À l’inférence, il choisit obligatoirement une classe parmi celles apprises.

Cela pose un problème opérationnel : si un nouveau type d’événement apparaît, le modèle risque de le ranger dans une catégorie connue mais incorrecte.

La classification **en monde ouvert** (*open-set* ou *open-world* dans le cadre du projet) ajoute une décision supplémentaire :

- si le log ressemble suffisamment aux catégories apprises, le modèle produit une prédiction ;
- s’il semble trop éloigné ou trop incertain, le modèle le rejette comme inconnu.

Le but n’est donc pas seulement d’obtenir une bonne accuracy. Il faut aussi savoir reconnaître les limites de ce que le modèle a appris.

### 1.3 Question du Projet 2

> Comment classer un événement dans une taxonomie de sécurité tout en reconnaissant qu’il ne correspond à aucune des classes apprises ?

L’hypothèse proposée dans le document de cadrage est qu’une architecture hiérarchique, associée à une estimation d’incertitude et à un mécanisme de rejet, peut réduire les erreurs forcées sur les classes inconnues tout en conservant une classification fine des classes connues.

------------------------------------------------------------------------

## 2. Objectifs du travail

Le projet poursuit cinq objectifs techniques et pédagogiques :

1.  **Organiser les 30 catégories** de SIEVE dans une taxonomie composée de familles et de classes fines.
2.  **Construire un scénario open-set** en retirant certaines classes de l’entraînement et en les considérant comme inconnues au test.
3.  **Construire un classificateur hiérarchique** qui prédit à la fois une famille et une classe fine.
4.  **Comparer plusieurs scores de familiarité** afin de décider si un log est connu ou inconnu.
5.  **Évaluer la solution** en classification fermée, en détection des inconnus et sous différents niveaux de perturbation.

Le notebook met également en place un modèle plat de comparaison. C’est important : sans baseline, on ne pourrait pas savoir si la complexité hiérarchique apporte réellement un bénéfice.

------------------------------------------------------------------------

## 3. Données utilisées : SIEVE

### 3.1 Présentation générale

Le document de cadrage décrit SIEVE comme une collection de six versions, de SIEVE_00 à SIEVE_05, contenant chacune 100 000 logs répartis sur 30 classes. Les versions correspondent à différents niveaux de perturbation SPICE :

| Version  | Niveau `p` | Rôle dans le notebook                   |
|:---------|-----------:|:----------------------------------------|
| SIEVE_00 |        0,0 | Base d’entraînement et référence propre |
| SIEVE_01 |        0,1 | Test de robustesse                      |
| SIEVE_02 |        0,2 | Test de robustesse                      |
| SIEVE_03 |        0,3 | Test de robustesse                      |
| SIEVE_04 |        0,4 | Test de robustesse                      |
| SIEVE_05 |        0,5 | Test de robustesse                      |

Le paramètre `p` représente le niveau de perturbation utilisé dans les versions du dataset. Il ne faut pas l’interpréter comme une mesure universelle de difficulté : il sert ici à comparer le comportement du modèle face aux versions de plus en plus perturbées.

**Observation importante sur l’exécution du notebook :** les fichiers chargés par le notebook contiennent 35 000 lignes chacun dans l’environnement utilisé. Le notebook travaille donc sur ces fichiers tels qu’ils sont fournis, et non sur les 100 000 lignes par version annoncées dans le document descriptif général. Après les opérations de sélection et de plafonnement, les tailles retenues sont notamment de 21 185 exemples d’entraînement, 6 845 de validation et 6 882 de test pour la base propre, ainsi qu’environ 6 800 à 6 900 exemples de test pour chaque version bruitée.

### 3.2 Les 30 classes

Les labels décrivent le type d’événement observé. Ils couvrent notamment :

- l’authentification ;
- les connexions ;
- les opérations sur les répertoires et les fichiers ;
- les requêtes HTTP ;
- les alertes et événements réseau ;
- les processus ;
- les opérations système ;
- les actions liées aux utilisateurs.

Le label est donc une catégorie sémantique de l’événement, et non une simple chaîne arbitraire.

### 3.3 Préparation des données

Le notebook charge les six fichiers `output_0.log` à `output_0.5.log`, puis récupère le label et le texte de chaque log. SIEVE_00 sert de base propre. Les autres versions sont utilisées comme tests de robustesse, pas comme données d’entraînement du modèle principal.

Cette séparation permet de poser une question précise : **un modèle appris sur des logs non perturbés conserve-t-il ses performances lorsque la forme textuelle des logs est dégradée ?**

------------------------------------------------------------------------

## 4. Construction de la taxonomie : 30 classes vers 9 familles

### 4.1 Pourquoi une hiérarchie ?

Une taxonomie organise les classes selon des relations parent-enfant. Au lieu de considérer les 30 labels comme des catégories totalement indépendantes, on les regroupe selon leur fonction.

Par exemple :

- `authentication-failed` et `authentication-success` appartiennent à la famille `authentication` ;
- `process-started`, `process-ended` et `process-error` appartiennent à la famille `process`.

Cela donne deux niveaux de prédiction :

- **niveau famille** : quel grand type d’événement ?
- **niveau classe fine** : quel événement précis ?

La hiérarchie peut aider à obtenir une prédiction plus informative, même lorsque le modèle hésite entre plusieurs classes proches. Elle ne garantit cependant pas automatiquement une meilleure précision.

### 4.2 Taxonomie effectivement codée

Le notebook définit les neuf familles suivantes :

| Famille            | Classes enfants                                                                         |
|:-------------------|:----------------------------------------------------------------------------------------|
| `authentication`   | `authentication-failed`, `authentication-success`                                       |
| `connection`       | `connection-closed`, `connection-failed`, `connection-opened`                           |
| `directory`        | `directory-changed`, `directory-created`, `directory-deleted`                           |
| `file`             | `file-action-failure`, `file-deleted`, `file-modification`, `file-read`, `file-write`   |
| `http`             | `http-request-failure`, `http-request-success`                                          |
| `network_security` | `ids-alert`, `network-filtered`, `network-traffic`                                      |
| `process`          | `process-ended`, `process-error`, `process-info`, `process-shutdown`, `process-started` |
| `system`           | `database-operation`, `hardware-monitoring`, `system-configuration-changed`             |
| `user`             | `user-creation`, `user-deletion`, `user-logout`, `user-session-open`                    |

La hiérarchie est une construction fonctionnelle définie dans le notebook. Elle n’est pas fournie comme ontologie prête à l’emploi par SIEVE. C’est un choix de modélisation du projet.

------------------------------------------------------------------------

## 5. Reconstruction des templates et prévention des fuites de données

### 5.1 Le problème des variantes d’un même log

Deux logs peuvent être différents textuellement tout en provenant du même modèle de message (*template*). Par exemple, les adresses IP, noms d’utilisateurs, chemins ou horodatages peuvent varier, alors que la structure générale du message reste identique.

Si l’on répartit aléatoirement les lignes, une variante d’un template peut se retrouver dans l’entraînement et une autre dans le test. Le modèle pourrait alors reconnaître une structure déjà vue plutôt que généraliser à un template réellement nouveau.

C’est une **fuite de données** (*data leakage*) : les ensembles d’entraînement et de test ne sont plus suffisamment indépendants.

### 5.2 Approche utilisée

Le notebook tente de reconstruire les groupes de templates à l’aide d’une représentation TF-IDF et d’un regroupement KMeans, classe par classe. Les groupes obtenus servent ensuite à effectuer les partitions train, validation et test.

Les résultats enregistrés indiquent :

- 440 groupes reconstruits au total ;
- un ARI moyen de 0,883 par rapport aux blocs de référence utilisés dans le notebook ;
- une cohérence de 0,9999 entre deux chemins d’assignation des groupes ;
- aucun groupe partagé entre train, validation et test pour les classes marquées strictes.

L’ARI (*Adjusted Rand Index*) mesure la similarité entre deux regroupements. Une valeur proche de 1 indique que les groupes reconstruits ressemblent fortement aux groupes de référence.

### 5.3 Classes strictes et non strictes

Le notebook distingue :

- **19 classes strictes** : elles disposent d’assez de groupes pour réaliser un split par template ;
- **11 classes non strictes** : le nombre de groupes est trop faible pour garantir la même séparation.

Pour les classes strictes, le notebook vérifie qu’aucun groupe n’apparaît dans plusieurs partitions. Pour les classes non strictes, une fuite résiduelle de templates reste possible.

Cette distinction est essentielle pour interpréter les résultats. Le notebook affiche souvent deux vues :

- `all` : toutes les classes ;
- `strict` : uniquement les classes considérées comme strictement séparées par template.

La vue stricte est plus prudente, mais elle porte sur moins de classes et moins d’exemples.

------------------------------------------------------------------------

## 6. Utilisation des versions bruitées SIEVE_01 à SIEVE_05

Le modèle principal est entraîné sur SIEVE_00 (`p = 0`). Les versions SIEVE_01 à SIEVE_05 sont réservées à l’évaluation de robustesse.

Le notebook rattache les logs bruités aux groupes/templates de la base propre, puis sélectionne des exemples pour les tests. La similarité moyenne observée diminue avec l’augmentation de `p` :

| Version | Nombre de lignes chargées | Exemples retenus pour le test | Similarité moyenne |
|:--------|--------------------------:|------------------------------:|--------------------|
| `p=0.1` |                    35 000 |                         6 996 | 0,895              |
| `p=0.2` |                    35 000 |                         6 927 | 0,867              |
| `p=0.3` |                    35 000 |                         6 943 | 0,847              |
| `p=0.4` |                    35 000 |                         6 858 | 0,830              |
| `p=0.5` |                    35 000 |                         6 956 | 0,808              |

Cette diminution est cohérente avec l’idée que les versions deviennent progressivement plus éloignées de la base propre.

**Interprétation :** cette expérience ne teste pas l’apprentissage sur des données bruitées. Elle teste la capacité d’un modèle entraîné sur des logs propres à conserver ses performances lorsque les logs présentés au test sont perturbés.

------------------------------------------------------------------------

## 7. Mise en place du scénario open-set

### 7.1 Principe

Pour simuler l’apparition de catégories inconnues, le notebook masque six classes sur les trente à chaque rotation.

- 24 classes sont considérées comme connues et utilisées pour entraîner le modèle ;
- 6 classes sont exclues de l’entraînement et deviennent inconnues au test ;
- l’opération est répétée sur cinq rotations, avec des groupes de classes cachées différents.

Cela représente 20 % des classes réservées comme inconnues.

### 7.2 Pourquoi plusieurs rotations ?

Si l’on cache toujours les mêmes six catégories, le résultat peut dépendre fortement de leur difficulté particulière. Les rotations permettent de vérifier si le comportement du modèle reste relativement stable lorsque les catégories inconnues changent.

Le notebook génère cinq rotations. Les classes cachées peuvent provenir de familles différentes. Le nombre de classes inconnues strictes varie toutefois selon les rotations, car certaines catégories ne disposent pas d’un split strict par template.

------------------------------------------------------------------------

## 8. Architecture des modèles

### 8.1 Encodeur textuel : DistilBERT

Le notebook utilise `distilbert-base-uncased` comme encodeur. DistilBERT est un Transformer pré-entraîné destiné à produire des représentations contextuelles de texte.

Le traitement suit les grandes étapes suivantes :

1.  le texte du log est tokenisé ;
2.  les tokens sont convertis en identifiants numériques ;
3.  les séquences sont tronquées ou complétées pour respecter une longueur maximale de 96 tokens ;
4.  DistilBERT produit des représentations vectorielles ;
5.  le notebook effectue un *mean pooling* masqué pour obtenir un vecteur représentant le log.

Le masquage évite de considérer les tokens de remplissage (*padding*) comme du contenu réel.

### 8.2 Modèle hiérarchique

À partir de la représentation du log, deux têtes de classification sont utilisées :

- une tête famille, qui prédit une distribution sur les 9 familles ;
- une tête fine, qui prédit une distribution sur les classes connues de la rotation.

La sortie n’a donc pas toujours 30 classes : dans une rotation open-set, la tête fine ne contient que les classes connues de cette rotation.

### 8.3 Modèle plat de comparaison

Le modèle plat utilise un encodeur comparable, mais prédit directement les classes fines, sans tête famille.

La comparaison répond à une question importante : **est-ce que le fait d’ajouter une hiérarchie améliore réellement les résultats ?**

### 8.4 Fonction de perte hiérarchique

Le modèle hiérarchique combine trois composantes :

$$L = L_{\text{fine}} + L_{\text{famille}} + \lambda \, L_{\text{cohérence}}$$

- $L_{\text{fine}}$ : entropie croisée sur la classe fine, elle pénalise une mauvaise prédiction de classe ;
- $L_{\text{famille}}$ : entropie croisée sur la famille, elle pénalise une mauvaise prédiction de famille ;
- $L_{\text{cohérence}}$ : encourage la compatibilité entre la distribution des classes fines et celle des familles ;
- $\lambda$ : règle le poids de cette contrainte. Le notebook utilise `lambda_cons = 0.5`.

Le terme de cohérence s’écrit, avec $p_k$ la probabilité de la classe fine $k$, $q_f$ la probabilité de la famille $f$ et $\varphi(k)$ la famille de la classe $k$ :

$$L_{\text{cohérence}} = -\log \sum_{k} p_k \, q_{\varphi(k)}$$

L’idée est d’éviter une situation incohérente où le modèle prédit une classe enfant appartenant à une famille différente de celle qu’il prédit au niveau parent.

Il faut distinguer deux notions :

- la **cohérence de la structure** : la classe et la famille prédites sont compatibles ;
- la **justesse de la prédiction** : la classe et la famille prédites correspondent effectivement au label réel.

Un modèle peut être très cohérent tout en se trompant de classe.

------------------------------------------------------------------------

## 9. Estimation de familiarité et rejet des inconnus

### 9.1 Pourquoi calculer un score ?

La sortie d’un classificateur fournit des scores ou probabilités sur les classes apprises. Pour prendre une décision open-set, le notebook calcule différents indicateurs de familiarité.

Dans la convention utilisée, **un score élevé signifie que l’exemple est jugé plus familier / connu**. Si le score est inférieur au seuil calibré, le modèle peut rejeter l’exemple.

### 9.2 Méthodes implémentées

Le notebook compare cinq méthodes :

| Méthode                             | Idée générale                                                          | Lecture intuitive                                                                |
|:------------------------------------|:-----------------------------------------------------------------------|:---------------------------------------------------------------------------------|
| MSP (*Maximum Softmax Probability*) | Maximum des probabilités softmax de la tête fine                       | Le modèle est-il très confiant dans sa meilleure classe ?                        |
| Energy                              | Score calculé à partir des logits avec `logsumexp`                     | Les activations globales du classificateur indiquent-elles un exemple familier ? |
| Prototypes                          | Similarité / distance de la représentation à des prototypes de classes | Le log est-il proche des représentations typiques des classes apprises ?         |
| MC-Dropout                          | Variabilité des prédictions sur plusieurs passages avec dropout        | Les prédictions changent-elles lorsque le modèle est légèrement perturbé ?       |
| Score hiérarchique                  | Score combinant des informations du niveau famille et du niveau classe | Les niveaux parent et enfant donnent-ils un signal de familiarité compatible ?   |

Le notebook effectue cinq passages MC-Dropout (`mc_passes = 5`). Cette méthode estime une forme d’incertitude en observant la variation des prédictions entre plusieurs passages.

### 9.3 Prototypes

Un prototype est un vecteur représentatif d’une classe, calculé à partir des représentations des exemples de cette classe. Un nouvel exemple est comparé à ces prototypes.

L’intuition est simple : si la représentation d’un log est proche d’un prototype connu, il ressemble à ce que le modèle a déjà appris. S’il est éloigné de tous les prototypes, il peut être candidat au rejet.

Cette méthode est intéressante car elle ne se limite pas à la confiance softmax.

### 9.4 Calibration du seuil

Le notebook calibre un seuil $\tau$ à partir des scores des exemples connus de validation. Le seuil correspond au 5e percentile des scores connus, conformément au paramètre de calibration du notebook (95 % des exemples connus de validation sont conservés).

La règle générale est :

$$\text{décision}(x) = \begin{cases} \text{classe connue}, & s(x) \geq \tau \\ \text{événement inconnu}, & s(x) < \tau \end{cases}$$

où $s(x)$ est le score de familiarité de l’exemple $x$.

Cette calibration cherche à limiter le rejet d’exemples connus. Elle ne garantit pas que les inconnus seront correctement rejetés : c’est précisément ce que les expériences doivent mesurer.

### 9.5 Interprétation opérationnelle

Le système ne doit pas simplement retourner une classe à chaque fois. Il doit pouvoir signaler qu’un log ne ressemble pas suffisamment aux catégories apprises. Dans un SIEM, cette décision est utile car elle peut orienter un événement inhabituel vers une analyse humaine plutôt que de lui attribuer automatiquement une catégorie erronée.

------------------------------------------------------------------------

## 10. Protocole expérimental

Le document de proposition définit cinq expériences. Le notebook en réalise principalement quatre.

### E1 — Classification fermée

**Question :** lorsque les classes sont toutes connues, quelle est la qualité de classification du modèle hiérarchique par rapport au modèle plat ?

Les métriques incluent :

- Macro-F1 ;
- accuracy fine ;
- accuracy famille ;
- distance taxonomique ;
- ECE (*Expected Calibration Error*).

### E2 — Détection open-set

**Question :** le système sait-il différencier les classes connues des classes masquées ?

Le protocole utilise cinq rotations et compare les méthodes de score avec les modèles plat et hiérarchique.

Les métriques principales sont :

- AUROC ;
- AUPR ;
- FPR@95TPR ;
- OSCR ;
- taux de rejet des connus ;
- taux d’acceptation des inconnus.

### E3 — Qualité hiérarchique

**Question :** la prédiction de famille apporte-t-elle une information utile et la prédiction fine reste-t-elle cohérente ?

Le notebook observe notamment l’accuracy famille, la qualité fine, la distance taxonomique, l’ECE et la cohérence brute famille-enfant.

### E4 — Robustesse aux perturbations

**Question :** les performances diminuent-elles lorsque l’on passe de SIEVE_00 aux versions de plus en plus perturbées ?

Le seuil de rejet est calibré sur la validation propre puis conservé pour les tests bruités. Cela permet d’observer l’effet des perturbations sans recalibrer le seuil à chaque niveau.

------------------------------------------------------------------------

## 11. Résultats et interprétation

### 11.1 E1 — Classification fermée

Résultats sur SIEVE_00 propre :

| Modèle       | Vue    | Macro-F1 | Accuracy fine | Accuracy famille | Distance taxonomique |    ECE |
|:-------------|:-------|---------:|--------------:|-----------------:|---------------------:|-------:|
| Hiérarchique | Toutes |   0,6813 |        0,7203 |           0,8155 |               0,4643 | 0,2134 |
| Plat         | Toutes |   0,6644 |        0,7058 |           0,7958 |               0,4984 | 0,2248 |
| Hiérarchique | Strict |   0,5291 |        0,5809 |           0,7326 |               0,6865 | 0,3397 |
| Plat         | Strict |   0,5062 |        0,5578 |           0,7013 |               0,7409 | 0,3625 |

**Interprétation :**

- Sur la vue `all`, le modèle hiérarchique obtient un Macro-F1 de 0,6813 contre 0,6644 pour le modèle plat.
- Son accuracy fine est également supérieure : 72,03 % contre 70,58 %.
- L’accuracy famille est supérieure, ce qui est logique puisque le modèle possède une tête dédiée à ce niveau.
- La distance taxonomique et l’ECE sont plus faibles pour le modèle hiérarchique dans cette expérience, ce qui est favorable selon la définition de ces métriques.

Sur la vue stricte, les deux modèles perdent en performance. Le modèle hiérarchique reste devant le modèle plat dans les métriques affichées, mais les valeurs sont nettement plus faibles.

**Ce qu’il faut retenir :** l’organisation hiérarchique apporte un gain modéré dans cette expérience fermée initiale, mais les scores montrent que la classification fine reste difficile.

### 11.2 Les confusions entre classes

Les dix confusions hiérarchiques les plus fréquentes incluent :

| Classe réelle            | Classe prédite           | Nombre |
|:-------------------------|:-------------------------|-------:|
| `process-ended`          | `process-started`        |    194 |
| `network-traffic`        | `connection-failed`      |    194 |
| `process-error`          | `connection-closed`      |    186 |
| `process-info`           | `authentication-success` |    158 |
| `connection-failed`      | `connection-opened`      |    152 |
| `user-logout`            | `connection-closed`      |    122 |
| `authentication-success` | `authentication-failed`  |    100 |

Ces erreurs montrent que certaines classes ont des représentations textuelles ou des contextes suffisamment proches pour être confondues par le modèle.

Un point important : une confusion entre `process-started` et `process-ended` est une erreur de classe fine, mais les deux événements appartiennent à la même famille `process`. La prédiction au niveau famille peut donc rester correcte alors que la classe précise est fausse. C’est l’un des intérêts de l’évaluation hiérarchique.

### 11.3 E2 — Détection des classes inconnues

Résultats moyens sur cinq rotations, vue stricte (exemples connus stricts contre l'ensemble des inconnus, voir la section 13.6) :

| Modèle       | Méthode            | AUROC moyen ± écart-type |  OSCR | OSR-F1 | Rejet des connus | Acceptation des inconnus |
|:-------------|:-------------------|-------------------------:|------:|-------:|-----------------:|-------------------------:|
| Plat         | Prototypes         |        **0,727 ± 0,096** | 0,537 |  0,339 |            6,4 % |                   80,3 % |
| Plat         | Energy             |            0,722 ± 0,098 | 0,533 |  0,336 |            6,4 % |                   82,3 % |
| Plat         | MC-Dropout         |            0,716 ± 0,101 | 0,524 |  0,336 |            6,1 % |                   81,5 % |
| Plat         | MSP                |            0,711 ± 0,104 | 0,521 |  0,335 |            5,7 % |                   82,4 % |
| Hiérarchique | Prototypes         |            0,702 ± 0,076 | 0,522 |  0,335 |            9,1 % |                   77,8 % |
| Hiérarchique | Energy             |            0,693 ± 0,090 | 0,519 |  0,332 |            8,1 % |                   78,9 % |
| Hiérarchique | Score hiérarchique |            0,692 ± 0,076 | 0,517 |  0,328 |            7,8 % |                   84,5 % |
| Hiérarchique | MC-Dropout         |            0,679 ± 0,090 | 0,506 |  0,331 |            9,1 % |                   79,3 % |
| Hiérarchique | MSP                |            0,677 ± 0,089 | 0,508 |  0,331 |            9,0 % |                   82,6 % |

**Interprétation :**

- La meilleure AUROC stricte observée est obtenue par le modèle plat avec les prototypes : 0,727.
- Les prototypes donnent également le meilleur OSCR et le meilleur OSR-F1 parmi les lignes présentées pour le modèle plat.
- Le modèle hiérarchique n’est pas systématiquement meilleur en détection des inconnus.
- Les taux d’acceptation des inconnus restent élevés : selon la méthode, environ 78 % à 85 % des inconnus sont acceptés comme s’ils étaient connus dans cette vue stricte.

Ce dernier résultat est particulièrement important. Une AUROC autour de 0,73 indique une capacité de séparation utile mais imparfaite. Elle ne signifie pas que le système reconnaît correctement tous les événements inconnus. Le taux d’acceptation élevé montre qu’il reste difficile de rejeter les classes jamais vues.

### 11.4 Pourquoi AUROC et taux d’acceptation doivent être lus ensemble

L’AUROC mesure la capacité du score à classer les exemples connus au-dessus des inconnus sur l’ensemble des seuils possibles. Le taux d’acceptation des inconnus, lui, décrit le comportement à un seuil de décision précis.

Un modèle peut donc avoir une AUROC raisonnable tout en laissant passer beaucoup d’inconnus au seuil choisi. Il faut toujours lire les métriques ensemble.

### 11.5 E3 — Qualité hiérarchique sur cinq rotations

Résultats moyens sur cinq rotations :

| Modèle       | Vue    | Macro-F1 | Accuracy fine | Accuracy famille | Distance taxonomique |   ECE | Cohérence brute |
|:-------------|:-------|---------:|--------------:|-----------------:|---------------------:|------:|----------------:|
| Plat         | Toutes |    0,725 |         0,765 |            0,837 |                0,398 | 0,168 |               — |
| Hiérarchique | Toutes |    0,719 |         0,762 |            0,839 |                0,399 | 0,177 |           0,982 |
| Plat         | Strict |    0,589 |         0,646 |            0,760 |                0,593 | 0,268 |               — |
| Hiérarchique | Strict |    0,583 |         0,642 |            0,764 |                0,594 | 0,280 |           0,982 |

**Interprétation :**

- Sur les rotations, le modèle hiérarchique obtient une accuracy famille légèrement supérieure.
- Le modèle plat conserve un léger avantage sur le Macro-F1 et l’accuracy fine.
- La cohérence brute du modèle hiérarchique est d’environ 98,2 %.
- Une cohérence élevée ne signifie pas que 98,2 % des prédictions sont correctes : elle indique que les sorties famille et classe sont généralement compatibles selon la règle de cohérence définie.

Le résultat illustre un compromis : le modèle hiérarchique structure les prédictions, mais cette structure ne garantit pas une amélioration de toutes les métriques.

### 11.6 E4 — Robustesse aux niveaux de perturbation

Résultats closed-set stricts :

| Niveau `p` | Modèle plat Macro-F1 | Modèle hiérarchique Macro-F1 | Plat accuracy fine | Hiérarchique accuracy fine |
|-----------:|---------------------:|-----------------------------:|-------------------:|---------------------------:|
|        0,0 |               0,5894 |                       0,5827 |             0,6463 |                     0,6420 |
|        0,1 |               0,5884 |                       0,5749 |             0,6403 |                     0,6304 |
|        0,2 |               0,5828 |                       0,5689 |             0,6312 |                     0,6226 |
|        0,3 |               0,5736 |                       0,5569 |             0,6189 |                     0,6051 |
|        0,4 |               0,5683 |                       0,5491 |             0,6114 |                     0,5967 |
|        0,5 |               0,5552 |                       0,5344 |             0,5948 |                     0,5774 |

**Interprétation :**

- Les deux modèles se dégradent lorsque le niveau de perturbation augmente.
- Le modèle plat conserve un Macro-F1 légèrement supérieur à chaque niveau dans cette vue stricte.
- Entre `p=0` et `p=0.5`, le Macro-F1 du modèle plat passe de 0,5894 à 0,5552.
- Pour le modèle hiérarchique, il passe de 0,5827 à 0,5344.

Cela indique que les perturbations rendent la classification plus difficile, même si le modèle conserve une partie de ses capacités.

Pour la détection open-set, l’AUROC de la méthode prototypes diminue également :

| Niveau `p` | Plat + prototypes AUROC | Hiérarchique + prototypes AUROC |
|-----------:|-------------------------|--------------------------------:|
|        0,0 | 0,7268                  |                          0,7024 |
|        0,1 | 0,7218                  |                          0,6977 |
|        0,2 | 0,7156                  |                          0,6917 |
|        0,3 | 0,7037                  |                          0,6824 |
|        0,4 | 0,6975                  |                          0,6774 |
|        0,5 | 0,6882                  |                          0,6703 |

La tendance est régulière : plus les logs sont perturbés, plus la séparation entre connus et inconnus devient difficile.

------------------------------------------------------------------------

## 12. Bilan par rapport aux exigences du Projet 2

Le tableau suivant met en correspondance le document de proposition et le notebook fourni.

| Exigence du Projet 2                             | État dans le notebook       | Commentaire                                               |
|:-------------------------------------------------|:----------------------------|:----------------------------------------------------------|
| Construire une taxonomie des 30 classes          | Réalisé                     | 9 familles définies explicitement                         |
| Définir plusieurs scénarios open-set             | Réalisé                     | 5 rotations, 6 classes masquées par rotation              |
| Utiliser un encodeur Transformer                 | Réalisé                     | DistilBERT                                                |
| Prévoir une tête famille et une tête classe fine | Réalisé                     | Modèle hiérarchique à deux têtes                          |
| Ajouter une contrainte de cohérence              | Réalisé                     | Loss de cohérence pondérée par 0,5                        |
| Comparer plusieurs scores d’incertitude          | Réalisé                     | MSP, Energy, prototypes, MC-Dropout et score hiérarchique |
| Calibrer un seuil de rejet sur validation        | Réalisé                     | Seuil fondé sur le 5e percentile des scores connus        |
| Comparer modèle plat et hiérarchique             | Réalisé                     | Résultats E1 à E3                                         |
| Évaluer la robustesse SIEVE_00 à SIEVE_05        | Réalisé                     | E4                                                        |

**Bilan :** le notebook répond largement au cœur fonctionnel du Projet 2  
hiérarchie, classes masquées, détection open-set, comparaison de scores et robustesse.

------------------------------------------------------------------------

### 13 Entraînement et ressources

La configuration enregistrée dans le notebook est :

| Paramètre                      |                    Valeur |
|:-------------------------------|--------------------------:|
| Encodeur                       | `distilbert-base-uncased` |
| Longueur maximale              |                 96 tokens |
| Batch size                     |                        64 |
| Époques                        |                         3 |
| Learning rate                  |                      5e-5 |
| Weight decay                   |                      0,01 |
| Warmup ratio                   |                      0,06 |
| Poids de cohérence             |                       0,5 |
| Rotations                      |                         5 |
| Classes inconnues par rotation |                         6 |
| Passages MC-Dropout            |                         5 |
| Matériel observé dans les logs |  GPU Tesla T4, AMP activé |

Ces paramètres décrivent l’exécution observée. Ils ne démontrent pas qu’ils sont optimaux ; ils permettent de reproduire et d’expliquer le protocole réalisé.

------------------------------------------------------------------------

## 14. Conclusion générale

Ce projet met en œuvre une chaîne complète d’expérimentation autour de la classification de logs SIEM en monde ouvert.

La démarche commence par l’organisation des 30 classes SIEVE en neuf familles. Elle prend ensuite en compte le risque de fuite de données en reconstruisant des groupes de templates et en réalisant des partitions par groupe lorsque cela est possible. Un encodeur DistilBERT transforme les logs en représentations vectorielles. Deux architectures sont comparées : un classificateur plat et un classificateur hiérarchique avec une tête famille, une tête classe fine et une contrainte de cohérence.

Pour simuler des événements inconnus, six classes sont masquées à chaque rotation. Plusieurs méthodes de familiarité sont comparées, puis un seuil calibré sur validation permet de décider si un exemple doit être accepté ou rejeté. Enfin, les performances sont mesurées sur les classes connues, les classes inconnues et les versions perturbées de SIEVE.

Les résultats montrent trois enseignements principaux :

1.  **La hiérarchie peut aider la classification fermée**, comme le montre l’expérience E1, mais le gain reste modéré et ne se retrouve pas systématiquement dans toutes les rotations.
2.  **Les prototypes sont la méthode de détection la plus performante parmi celles testées dans la vue stricte**, avec une AUROC moyenne de 0,727 pour le modèle plat.
3.  **Les perturbations dégradent progressivement la classification et la détection**, ce qui confirme l’intérêt de tester la robustesse plutôt que de se limiter à un jeu de données propre.

Le projet répond donc largement à l’objectif du Projet 2 : construire et évaluer une solution qui combine classification hiérarchique et rejet des classes inconnues. Il reste des améliorations possibles, notamment la symétrisation du filtrage strict.

La conclusion n’est pas que le modèle hiérarchique est toujours supérieur. Elle est plus nuancée et plus intéressante : **la hiérarchie apporte une structure utile, mais elle ne suffit pas à résoudre la détection des inconnus ; le choix du score de familiarité et la qualité du protocole d’évaluation jouent également un rôle essentiel.**

------------------------------------------------------------------------

## 15. Glossaire rapide

| Terme        | Explication                                                                |
|:-------------|:---------------------------------------------------------------------------|
| SIEM         | Outil qui centralise et analyse des événements de sécurité                 |
| Log          | Enregistrement textuel décrivant un événement                              |
| Classe fine  | Catégorie précise, par exemple `authentication-failed`                     |
| Famille      | Groupe général de classes, par exemple `authentication`                    |
| Taxonomie    | Organisation hiérarchique des catégories                                   |
| Closed-set   | Situation où toutes les classes possibles sont connues à l’entraînement    |
| Open-set     | Situation où des exemples peuvent appartenir à des classes jamais apprises |
| OOD          | *Out-of-Distribution*, exemple éloigné de la distribution connue           |
| Template     | Structure générale d’un log, indépendamment de certaines valeurs variables |
| Data leakage | Fuite d’information entre entraînement et test                             |
| Transformer  | Architecture de réseau neuronal adaptée au traitement de séquences         |
| DistilBERT   | Version compacte de BERT utilisée comme encodeur textuel                   |
| Logits       | Scores bruts produits par une tête de classification avant softmax         |
| Softmax      | Transformation des logits en probabilités normalisées                      |
| Prototype    | Vecteur représentatif d’une classe                                         |
| Calibration  | Ajustement d’une décision ou d’un seuil à partir de données de validation  |
| Macro-F1     | Moyenne du F1 calculé séparément pour chaque classe                        |
| AUROC        | Mesure de la capacité d’un score à séparer deux groupes                    |
| AUPR         | Aire sous la courbe précision-rappel                                       |
| FPR@95TPR    | Taux de faux positifs lorsque le taux de vrais positifs atteint 95 %       |
| OSCR         | Mesure combinant reconnaissance des connus et rejet des inconnus           |
| ECE          | Mesure de l’écart entre confiance annoncée et exactitude observée          |
| MC-Dropout   | Estimation de l’incertitude en répétant des prédictions avec dropout actif |

------------------------------------------------------------------------

## 16. Fichiers et artefacts produits par le notebook

Le notebook indique qu’il génère notamment :

- `outputs/recap.log` : journal chronologique de l’exécution ;
- `outputs/RECAP.md` : résumé des résultats ;
- `outputs/tables/` : tableaux CSV ;
- `outputs/figs/` : figures ;
- `outputs/ckpt/` : checkpoints et résultats sauvegardés ;
- `outputs.zip` : archive des artefacts.

Les figures enregistrées dans les sorties sont :

- `F1_auroc_boxplot.png` : comparaison des scores AUROC ;
- `F2_robustness_noise.png` : effet du bruit ;
- `F3_reject_per_class.png` : rejet par classe ;
- `F4_E1_confusion.png` : matrice de confusion E1 ;
- `F5_score_hist_rot0.png` : distributions de scores pour une rotation.

------------------------------------------------------------------------
