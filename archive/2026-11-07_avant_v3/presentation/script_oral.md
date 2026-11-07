# Script oral de la soutenance
Un discours par diapositive, à dire avec vos mots. Temps estimé à environ 130 mots par minute. Les mêmes textes sont dans les notes du fichier PowerPoint.

## Diapositive 1 : Titre  (~82 s)

Bonjour. Mon sujet tient en une question : un programme qui trie des journaux de sécurité sait-il aussi dire « ça, je ne connais pas » ?

Imaginez un standardiste qui doit orienter chaque appel vers l'un de trente services. Si un appel ne correspond à aucun service, un mauvais standardiste l'envoie quand même quelque part. Un bon standardiste dit : « celui-là, je ne sais pas, je le signale ». C'est exactement le schéma à droite. En haut, dans le monde fermé, tout est rangé de force, donc l'erreur est invisible. En bas, dans le monde ouvert, ce qui est loin de tout ce qu'on connaît reçoit un point d'interrogation.

Ce que la diapositive ne dit pas : je ne vais pas vous présenter un programme miracle. Mon message est qu'il faut se méfier de la façon dont on note ces programmes, parce que les scores publiés sur ce jeu de données sont trop beaux. Mon plan suit trois questions : que valent ces scores, sait-on repérer l'inconnu, et le système résiste-t-il quand on abîme le texte.

## Diapositive 2 : Introduction - Contexte  (~88 s)

Je commence par l'enjeu, avec trois sources que j'ai ouvertes une par une.

Le plus gros chiffre, 4,99 millions de dollars, vient du rapport IBM sur le coût des violations de données, dans l'édition 2026. Ce que la diapositive ne montre pas, c'est le lien avec le temps : il faut en moyenne 247 jours pour identifier et contenir une violation, et au-delà de 200 jours elle coûte 5,65 millions de dollars contre 4,32 en dessous. Détecter vite fait donc économiser de l'argent.

Le deuxième chiffre vient d'une enquête auprès de 2 000 analystes : une équipe reçoit 4 484 alertes par jour et en ignore 67 %. Ce n'est pas de la paresse, c'est que personne ne peut tout lire. Le SIEM est le logiciel qui centralise ces alertes. Si un programme trie ce qui est connu et signale ce qui ne l'est pas, il redonne du temps aux humains.

Deux précautions. Ces rapports sont écrits par des acteurs de la sécurité, donc je les prends comme des ordres de grandeur. Et ils ne prouvent pas que ma méthode aide : ils montrent seulement que le problème est réel.

## Diapositive 3 : Introduction - Problématique  (~79 s)

Voici la question centrale, avec une image : un élève qui s'entraîne sur les annales, puis qui passe un examen contenant les mêmes questions. Sa note est excellente, mais elle ne prouve pas qu'il a compris.

C'est ce qui arrive avec ce jeu de données. Les logs sont fabriqués en remplissant environ 440 phrases types, les gabarits, avec des valeurs différentes. Si on mélange tout au hasard puis qu'on coupe entre entraînement et test, la même phrase type se retrouve des deux côtés. Le programme reconnaît la phrase, il ne comprend rien de plus. D'où des scores publiés entre 0,93 et 0,97.

Ce que la diapositive ne dit pas : quand je sépare par phrase type, le score tombe autour de 0,46 à 0,48. Le problème n'est donc pas le modèle, c'est ce que l'évaluation mesure. Les trois questions numérotées sont les trois parties de mon exposé. Et pour l'inconnu : dans un SIEM, ce n'est pas un cas rare, c'est ce qui arrive le jour où une nouvelle attaque apparaît.

## Diapositive 4 : Introduction - Objectifs  (~68 s)

Mon objectif est volontairement modeste : mesurer, pas construire un produit. Je n'ai pas inventé de fonctionnalité, parce que ce n'est pas l'objet du projet.

Ce qui donne de la valeur à cette mesure, c'est la discipline derrière les cinq objectifs. Premier point : j'ai écrit mes quinze hypothèses et les règles de décision avant de voir les chiffres, avec pour chacune ce qui la réfuterait. Deux ont été réfutées, les hypothèses H1 et H13, et je les garde dans le rapport au lieu de les cacher. Deuxième point : le jeu de test est scellé. Il n'a été ouvert qu'une fois, avec une trace datée, et mes choix étaient figés avant.

L'utilité à long terme est un banc d'essai : quelqu'un qui veut comparer un autre programme de classement de logs peut rejouer le notebook et se comparer sans surestimer ses résultats. Rien de plus n'est revendiqué.

## Diapositive 5 : État de l'art - Vue d'ensemble  (~82 s)

Pour ne pas me perdre dans la littérature, je l'ai découpée en cinq blocs, du plus concret au plus technique. A : les logs et la façon de séparer entraînement et test, parce que tout dépend de là. B : la hiérarchie, pour se tromper moins gravement. C : la détection d'inconnus, le cœur du projet. D : que se passe-t-il si un attaquant abîme le texte. E : la calibration, c'est-à-dire si la confiance du modèle est honnête. Pour chaque bloc, je vous montre ce qui existe, sa limite, et ce que j'en retiens.

Ce que la diapositive ne dit pas : la recherche a été faite le 5 novembre 2026, dans arXiv, l'ACL Anthology, des pages d'éditeurs et une base de citations. J'ai ouvert la page de 73 références. Dans ce protocole, je n'ai trouvé aucun travail qui traite ensemble hiérarchie, logs SIEM et monde ouvert. Je le dis prudemment : aucune base n'est exhaustive. Ce que je revendique, c'est une évaluation sans fuite avec une comparaison systématique, pas une méthode meilleure que toutes les autres.

## Diapositive 6 : État de l'art - Bloc A : les logs et le découpage  (~71 s)

Bloc A, les données. Pour les logs, la littérature fait surtout deux choses. Détecter des séquences anormales, avec DeepLog ou LogBERT : c'est un autre problème, car ils ne disent pas de quel type d'événement il s'agit. Ou classer avec des modèles de langue : Karlsen et ses collègues annoncent 0,998 de F1 sur six jeux, mais le résumé ne décrit pas le découpage, donc je ne peux ni affirmer ni exclure une fuite.

Pour SIEVE, les auteurs annoncent 0,93 à 0,97. Chez moi, un SVM obtient 0,9735 avec un découpage au hasard, l'article annonce 0,9737 : je reproduis donc leur résultat, puis je montre que par gabarit on tombe à 0,458. Autre chiffre : au hasard, 24 % des logs de test ont un quasi-jumeau dans l'entraînement, contre 1 % par gabarit.

Ce que j'en retiens : un découpage par gabarit, une validation croisée par groupes et imbriquée, et un test scellé.

## Diapositive 7 : État de l'art - Bloc B : la classification hiérarchique  (~82 s)

Bloc B, la hiérarchie. Trois raisons de s'en servir. Un : toutes les erreurs ne se valent pas. Prendre un échec d'authentification pour un succès est proche dans l'arbre, mais attention, en sécurité cette erreur-là peut cacher une attaque : je garde donc aussi une analyse par paires de classes. Deux : la famille est plus facile à prédire, 0,67 de macro-F1 contre 0,46 pour la classe fine. Trois : en monde ouvert, on peut répondre au niveau de la famille quand le détail est incertain, c'est l'idée de Linderman et ses collègues, en vision.

Dans la littérature sur le texte, la hiérarchie est traitée en monde fermé, et Kwon et ses collègues écrivent que gérer des étiquettes inconnues avec une hiérarchie est un problème encore ouvert.

Ce que je retiens : une approche locale, avec deux têtes, où la probabilité d'une classe est le produit des deux niveaux. Sa faiblesse : si la famille est fausse, la bonne classe est hors de portée. C'est une des raisons pour lesquelles le gain n'est pas démontré chez moi.

## Diapositive 8 : État de l'art - Bloc C : la détection d'inconnus  (~79 s)

Bloc C, le cœur du projet. Un classifieur ordinaire n'a pas de case « inconnu » : ses probabilités font toujours 1, donc il range de force.

La littérature propose quatre familles. Le score de sortie : la probabilité maximale, l'énergie, ODIN, OpenMax. La distance dans l'espace interne : Mahalanobis, kNN, ViM. L'incertitude : plusieurs modèles, ou le dropout. Et un entraînement spécial avec des exemples d'inconnus.

Deux avertissements. Vaze et ses collègues : un bon classifieur fermé suffit presque, la capacité à rejeter suit son exactitude. Baran et ses collègues : en texte, les méthodes classiques ratent beaucoup de décalages.

Ce que je retiens : comparer huit scores sur les mêmes classes masquées, avec un seuil réglé sur les classes connues seulement. J'ai écarté ODIN, parce qu'il perturbe l'entrée et que cela n'a pas de sens pour du texte, et Outlier Exposure, parce qu'il exige des exemples d'inconnus. Un chiffre à garder : mon seuil visait 5 % de connus rejetés, il en rejetait 9 à 13 % au test.

## Diapositive 9 : État de l'art - Bloc D : la robustesse du texte  (~73 s)

Bloc D, un attaquant qui modifie le texte. Dans un SIEM, une partie du log est contrôlée par l'attaquant : nom d'utilisateur, adresse web, nom de fichier. C'est le jeu des spammeurs contre les filtres. Lowd et Meek montrent que la moitié du spam bloqué passe avec 150 mots ajoutés ou moins, à condition de choisir des mots fréquents : des mots au hasard sont inefficaces. Boucher et ses collègues montrent qu'un seul changement invisible, comme un homoglyphe, peut dégrader un modèle. La défense qu'ils recommandent : assainir l'entrée.

Ce que je retiens : trois attaques, chacune à trois degrés ; la normalisation avec la table officielle Unicode comme garde-fou, l'entraînement adversarial en renfort. Un fait utile : la normalisation Unicode standard, NFKC, ne corrige pas les homoglyphes. Je l'ai vérifié : le « a » cyrillique n'est pas une variante de compatibilité.

Hors périmètre : les attaques par synonymes ou par gradient, trop coûteuses pour une entrée discrète.

## Diapositive 10 : État de l'art - Bloc E : la calibration  (~77 s)

Bloc E, la calibration. Un modèle est calibré si, quand il se dit sûr à 90 %, il a raison 9 fois sur 10. On le vérifie par un diagramme de fiabilité et un nombre, l'ECE, l'écart moyen entre confiance annoncée et réalité. La correction classique est la température : on divise les scores par un nombre avant de calculer les probabilités.

Ce que la diapositive ne dit pas : la température change les probabilités mais pas leur ordre, donc elle ne change ni la classe prédite ni la détection d'inconnus. Ovadia et ses collègues montrent que sous décalage de données, la calibration se dégrade. C'est ce que je mesure : sur l'encodeur, l'ECE passe de 0,18 en validation à 0,35 au test, avec 85 % de confiance annoncée pour 50 % de bonnes réponses. Pour TF-IDF, la température ramène l'ECE de 0,150 à 0,095 sans effet sur l'AUROC. Ce que je retiens : mesurer l'ECE avant et après, sans lui demander de résoudre la détection d'inconnus.

## Diapositive 11 : Matériel  (~78 s)

Voici ma matière première. SIEVE : six fichiers de 100 000 logs, de p = 0, le texte propre, à p = 0,5, le texte très abîmé. Ils sont générés à partir de 440 gabarits réels, en 30 classes équilibrées, soit 20 000 logs par classe. Le jeu n'est pas redistribué, il est fourni sur demande par ses auteurs : mon dépôt public ne contient donc pas les données.

Le professeur m'a fourni six autres fichiers de 35 000 logs, mêmes gabarits, valeurs nouvelles. Je m'en sers comme contrôle de la fuite : un modèle qui a vu tous les gabarits y obtient 0,97, un modèle dont le gabarit vient du test 0,44.

Côté outils : la table Unicode de 1 447 caractères confondables, DistilBERT, une version allégée de BERT, et mon regroupement des classes en huit familles, qui reste une hypothèse. Enfin, aucun log réel : les 440 logs réels du CDS ne sont pas dans l'archive reçue, donc je n'ai pas pu tester en conditions réelles.

## Diapositive 12 : Méthodes  (~94 s)

Voici ce que j'ai fait dans le notebook, sous forme de boucle. Un : la vectorisation, transformer le texte en nombres, de trois façons, du simple comptage de mots au réseau Transformer. Deux : la classification, choisir la famille puis la classe. Trois : la détection d'inconnus, donner à chaque log une note d'étrangeté, par la confiance ou par la distance, avec un seuil qui garde 95 % des connus. Quatre : l'évaluation, mais sur la validation : découpage par gabarit, cinq rotations de classes masquées. Cinq : la robustesse et la calibration, attaquer, défendre, corriger la confiance.

Pourquoi une boucle : à chaque tour, je règle sur la validation, et si je trouve un défaut, je repars. Deux exemples vécus : la défense circulaire, corrigée à l'étape 9, et le seuil de rejet qui laissait passer 80 à 89 % des inconnus.

Et à droite, hors de la boucle : le test scellé. Il ne sert qu'une fois, à la fin, quand tous les choix sont figés, avec une trace datée dans le notebook. S'il servait dans la boucle, je réglerais sur lui et il ne mesurerait plus rien. Une règle absolue : les réglages se font sans jamais regarder les classes masquées.

## Diapositive 13 : Présentation des données (1/3)  (~67 s)

Les données, en trois temps. Premier temps : 30 classes équilibrées, soit 20 000 logs par classe sur l'ensemble. Une classe est un type d'événement, par exemple un échec d'authentification.

Deuxième temps : les huit familles. C'est mon regroupement, adossé à un schéma standard de l'industrie, ECS. Aucun expert SIEM ne l'a validé, donc c'est une hypothèse de démonstration, et je le redis en limite. L'intérêt : se tromper entre authentication-failed et authentication-success est une erreur moins grave que prendre un échec de connexion pour une suppression de fichier.

Troisième temps, les repères R1 à R5. Pour tester l'inconnu, il faut cacher des classes pendant l'entraînement, sinon ce ne serait pas de l'inconnu. À chaque rotation, six classes sont cachées. Au bout de cinq rotations, chaque classe a joué une fois le rôle de l'inconnue, et le résultat ne dépend pas d'un seul choix de classes.

## Diapositive 14 : Présentation des données (2/3)  (~78 s)

Une clarification qui m'a été demandée : il n'y a qu'un seul jeu de données. Les auteurs de SIEVE partent de logs réels publics, Loghub, OSSEC et Public Security Log Sharing Site. Ils en tirent 440 gabarits, des phrases à trous, validés par trois spécialistes SIEM, répartis en 30 classes. À partir de ces gabarits, ils génèrent les six fichiers de 100 000 logs, de plus en plus abîmés. Tous mes modèles sont entraînés et testés sur ces logs.

Les 311 gabarits que j'ai reconstitués ne forment pas un autre jeu : c'est un regroupement des mêmes logs, utilisé uniquement pour séparer entraînement et test. En bas, l'exemple : le gabarit, un log qui le remplit, le même log abîmé à p = 0,5.

Limite que je dis d'avance : les 440 logs réels du CDS ne sont pas dans l'archive reçue. Je ne peux donc pas comparer à du réel, d'autant que SIEVE est produit à partir de ces mêmes gabarits : le CDS n'est pas un jeu indépendant.

## Diapositive 15 : Présentation des données (3/3)  (~91 s)

Cette diapositive prouve la fuite, sur les logs de SIEVE : les six fichiers de 100 000 logs, pas sur le CDS. Je précise ce que veulent dire les deux découpages. Séparer les logs de SIEVE entre entraînement et test au hasard : on mélange tout, donc le même gabarit se retrouve des deux côtés. Séparer par gabarit : tous les logs d'un même gabarit vont du même côté.

Comment lire : pour chaque log de test, je cherche le log d'entraînement qui lui ressemble le plus, et je note la ressemblance de 0 à 1. À gauche, la ressemblance typique, la médiane : élevée avec le découpage au hasard, basse avec le découpage par gabarit. À droite, la part des logs de test qui ont un quasi-jumeau : près d'un quart des logs propres au hasard, presque aucun par gabarit.

Sur les logs très abîmés, l'écart se réduit parce que le texte est tellement modifié que même un log du même gabarit ressemble moins à sa copie. Et les fichiers du professeur confirment ce constat : un modèle qui a vu tous les gabarits y obtient 0,97, un modèle dont le gabarit vient du test 0,44.

## Diapositive 16 : Librairies utilisées  (~51 s)

Les bibliothèques, sans surprise. Rien d'exotique : un socle scientifique standard de Python.

Deux remarques que le tableau ne dit pas. D'abord, PyTorch et Transformers ne servent que pour le réseau DistilBERT, qui est une version allégée du modèle BERT. Tous les autres modèles tiennent dans scikit-learn. Ensuite, les versions sont figées dans un fichier du dépôt, ce qui permet à quelqu'un de rejouer le notebook et de retrouver les mêmes résultats.

Un détail technique que je mentionne par honnêteté : sur le Mac, j'ai dû utiliser l'attention classique du réseau et non l'attention rapide, parce que la rapide ne gère pas la méthode d'incertitude que je compare, le Monte-Carlo dropout.

## Diapositive 17 : Environnement d'exécution  (~80 s)

Voici où chaque calcul a tourné, et combien de temps il a pris. Sur le Mac, avec la puce M3 Pro et sa carte graphique intégrée : 17 à 19 minutes pour entraîner un réseau, 8 à 9 minutes de prédiction par jeu, soit environ 38 minutes par rotation. Sur Google Colab, avec une carte T4 : 10 à 15 minutes d'entraînement, et environ 30 à 35 minutes par rotation avec les prédictions.

Colab a fait les 11 entraînements de validation, puis les rotations 1 et 2 du test. Mais la limite d'utilisation de la carte a été atteinte une fois, et j'ai terminé sur le Mac, rotations 3 à 5. Pour la comparaison finale, 15 réseaux, trois graines par rotation, ont été recalculés sur le Mac.

Les modèles simples tournent sur le processeur, de 15 secondes à environ deux minutes et demie. Une leçon du projet : un redémarrage du Mac a interrompu un calcul, d'où le principe de tout sauvegarder par unité. Avec ces sauvegardes, rejouer le notebook prend environ 13 minutes.

## Diapositive 18 : Conception - Pipeline utilisé  (~59 s)

Voici le déroulé en onze étapes, qui suit la consigne du projet. Je veux vous faire retenir trois étapes.

L'étape 3, en orange : le découpage. C'est elle qui change les conclusions, car c'est là que je sépare par gabarit au lieu de mélanger. Elle fait passer le score de 0,97 à 0,46. Je compare quatre protocoles de découpage, et le test est scellé : je ne l'ouvre qu'une fois, avec une trace datée.

L'étape 4 : dix variantes de nettoyage du texte, car je ne veux pas supposer qu'un nettoyage est le bon.

L'étape 10 : un registre de 99 affirmations. Chaque chiffre du notebook est relié à sa source ou à son calcul, ce qui me permet de vérifier que rien n'est avancé sans preuve.

## Diapositive 19 : Conception - Présentation et analyse des résultats (1/5)  (~79 s)

Premier résultat, le plus important, sur un seul modèle, un SVM linéaire sur TF-IDF mots, entraîné et testé sur les logs de SIEVE. Je rappelle ce que mesure le macro-F1 : pour chaque classe, on combine deux questions, les logs étiquetés ainsi sont-ils justes, et a-t-on retrouvé tous les vrais ; puis on moyenne sur les 30 classes.

Ce que dit le graphique, sans entrer dans les chiffres : avec un découpage au hasard, le score est presque parfait. Dès qu'on sépare par gabarit, il s'effondre de moitié. Les trois façons de séparer par gabarit donnent des scores voisins : la chute n'est donc pas un accident d'un découpage particulier. Et le test scellé, ouvert une seule fois à la fin, tombe dans la même zone : mes choix n'ont pas été réglés sur lui.

Ce qu'on en tire de bien : une mesure solide. De moins bien : les scores publiés mesuraient surtout la reconnaissance de gabarits déjà vus, pas la compréhension. Cette métrique, le macro-F1, revient à la diapositive suivante.

## Diapositive 20 : Conception - Présentation et analyse des résultats (2/5)  (~76 s)

Cette diapositive met côte à côte les deux questions du projet, pour les mêmes deux modèles, sur les mêmes logs de SIEVE et le même test par gabarit. À gauche, le monde connu : parmi les classes qu'il connaît, le modèle se trompe à peu près une fois sur deux. Au centre et à droite, le monde inconnu : sait-il repérer une classe qu'il n'a jamais vue ?

Une précaution : le macro-F1 et l'AUROC n'ont pas la même échelle. On ne les compare pas entre eux, on compare les deux modèles sur chacun. Et là, le résultat est le même des deux côtés : le Transformer fait un peu moins bien ou pareil. Le type de modèle n'est donc pas le facteur décisif.

Ce qu'on en tire de moins bien : repérer l'inconnu reste proche du hasard. La cible fixée avant les résultats, un AUROC d'au moins 0,80, est loin. De bien : on le sait avec une mesure honnête, ce qui était l'objectif.

## Diapositive 21 : Conception - Présentation et analyse des résultats (3/5)  (~76 s)

Ici, une seule métrique, l'AUROC, pour tous les scores d'inconnu. Ce qu'il faut regarder, c'est la forme du graphique plus que les chiffres. Pour TF-IDF, les six scores sont presque alignés : les différences sont plus petites que le bruit d'une rotation à l'autre, donc aucun n'est vraiment meilleur. Pour le Transformer, il y a un seul gain net : quand on passe de sa confiance à une distance dans ses vecteurs, le score monte nettement et dans les cinq rotations.

Pourquoi ? Un Transformer affiné resserre les classes dans son espace interne : un log inconnu s'y trouve plus loin de tous les nuages, même quand sa confiance reste trompeusement haute. C'est ce que dit la littérature, et je le retrouve.

Mais même ce meilleur score ne dépasse pas le simple comptage de mots, et aucun n'approche la cible. Un détail instructif : en validation, TF-IDF faisait beaucoup mieux ; au test, sur de nouveaux gabarits, il retombe. Les conclusions par classe sont instables.

## Diapositive 22 : Conception - Présentation et analyse des résultats (4/5)  (~87 s)

Les trois attaques, chacune à trois degrés, avec les deux mêmes métriques : à gauche, la perte de bonnes réponses dans le monde connu, à droite, le score de détection de l'inconnu.

À gauche, la relation entre le degré et la perte. Pour les fautes de frappe et les mots ajoutés, la perte reste faible tant que l'attaque est modérée et ne grimpe qu'à forte dose. Pour les lettres trompeuses, elle croît vite et de plus en plus : c'est l'attaque la plus efficace, parce qu'un mot dont une lettre est d'un autre alphabet devient pour la machine un mot inconnu, alors qu'un humain ne voit rien.

À droite, un fait à ne pas manquer : le score de détection de l'inconnu bouge à peine, mais le seuil, lui, se dérègle : le nombre de logs légitimes rejetés à tort monte nettement avec les lettres trompeuses fortes. En pratique, l'analyste reçoit plus de fausses alertes.

Ces courbes sont celles du modèle TF-IDF mots. Le modèle par lettres résiste mieux aux lettres trompeuses, moins bien aux mots ajoutés : il n'y a pas de modèle qui résiste à tout.

## Diapositive 23 : Conception - Présentation et analyse des résultats (5/5)  (~77 s)

Pour la défense, les trois degrés d'attaque, avec l'attaque par la table officielle. Lecture de gauche à droite : sans défense, la perte monte avec le degré. Une table maison ne change presque rien, parce qu'elle ne connaît qu'une partie des caractères. La moitié de la table officielle réduit la perte de moitié environ. La table officielle complète la fait presque disparaître.

La relation à retenir : plus la défense connaît de caractères confondables, plus elle protège. Ce n'est pas un hasard, c'est la définition d'une table de correspondance.

Le test circulaire, non montré : si je teste la défense avec la table même de l'attaque, elle paraît parfaite. C'est l'erreur que j'avais faite à l'origine et que j'ai corrigée.

À droite, les parades : normaliser et entraîner avec des textes abîmés aident chacune, et les deux ensemble sont les plus efficaces. Le pire cas reste nettement plus mauvais que la moyenne : certaines attaques passent mieux que d'autres. Limite : ces attaques restent surtout non adaptatives.

## Diapositive 24 : Conception - Limites de la conception (1/2)  (~66 s)

Je termine la partie conception par ce qui borne mes conclusions, en ordre d'importance.

La première limite pèse le plus : les données sont synthétiques. Sans logs réels, je ne sais pas si mes conclusions se transfèrent. La deuxième : mon regroupement en familles n'a pas été validé par un expert.

Troisième : un petit nombre de gabarits distincts, 36 en validation et 45 au test. Un écart inférieur à 0,05 est donc impossible à distinguer du bruit. Quatrième : seulement trois essais pour le Transformer, un seul pour la plupart des autres modèles.

Cinquième : le test scellé a déjà été ouvert une fois, donc les scores ajoutés ensuite sont comparés sur la validation seulement. Sixième : je n'ai pas de logs réels, et mes attaques ne s'adaptent pas au modèle, donc je ne dis rien d'un attaquant qui connaît le système.

## Diapositive 25 : Conception - Limites de la conception (2/2)  (~76 s)

Maintenant, les limites par rapport à ce que je m'étais fixé. Objectif général : mesurer sans tricher jusqu'où on sait classer et repérer l'inconnu. Atteint en partie : l'évaluation est sans fuite, mais sur des données synthétiques, donc je ne sais pas ce que cela vaut sur du réel.

Objectif 1, mesurer l'effet de la triche : atteint, de 0,97 à 0,46, avec la réserve des gabarits reconstruits, 311 sur 440. Objectif 2, comparer les représentations : atteint, le Transformer n'est pas meilleur, mais avec trois graines et sans balayage de réglages. Objectif 3, comparer huit scores d'inconnu : atteint, aucun n'atteint 0,80, mais avec 36 gabarits en validation et 45 au test, un écart inférieur à 0,05 est indétectable.

Objectif 4, attaques et défenses : atteint, mais pour des attaques surtout non adaptatives et sans les attaques par synonymes. Objectif 5, un notebook reproductible : atteint, mais les données SIEVE ne sont pas redistribuables et le test a déjà été ouvert une fois.

## Diapositive 26 : Conclusion (1/2)  (~71 s)

Pour conclure, objectif par objectif. Général : en partie. Sans fuite, on obtient 0,46 en monde connu et 0,60 pour repérer l'inconnu : le problème reste ouvert. Un : la triche. De 0,97 à 0,46, c'est le découpage, pas le modèle, qui fait l'écart. Deux : les représentations. Le Transformer fait 0,46 contre 0,49 pour TF-IDF ; seul gain net, la distance de Mahalanobis sur ses vecteurs, plus 0,057. Trois : les scores d'inconnu. Le meilleur AUROC est de 0,625 pour une cible à 0,80. Quatre : attaques et défenses. Les lettres trompeuses font perdre jusqu'à 21,5 % ; la table officielle ramène la perte à 0,2 %. Cinq : le notebook est reproductible, avec 99 affirmations vérifiées, un test scellé et un dépôt public.

Ce que je ne conclus pas : que le Transformer est inutile, ou que la hiérarchie n'aide pas. Je dis seulement que ce n'est pas démontré dans ces données.

## Diapositive 27 : Conclusion (2/2)  (~57 s)

Chaque limite appelle une perspective. La première est de passer au réel : tester sur de vrais logs, d'abord les 440 logs réels du CDS, puis des logs d'entreprise. Deuxième : faire valider les huit familles par un expert SIEM. Troisième : plus de gabarits distincts et plus de graines, pour mesurer le bruit d'entraînement. Quatrième : pour la détection de l'inconnu, tester une covariance par classe pour Mahalanobis, et mesurer si la famille proposée pour un inconnu rejeté est la bonne. Cinquième : des attaques qui s'adaptent à la défense, et une reconnaissance de mots avant le classifieur, comme le proposent Pruthi et ses collègues.

La phrase à retenir : avant de croire un score, regarder comment on a séparé l'entraînement du test.

## Diapositive 28 : Merci  (~36 s)

Merci de votre attention. Si je ne devais garder qu'une phrase : avant de croire un score, regardez comment on a séparé l'entraînement du test.

Tout ce que j'ai montré est rejouable : le dépôt public contient le notebook, les résultats chiffrés, les figures et le code. Seules les données SIEVE n'y sont pas, parce qu'elles sont fournies sur demande par leurs auteurs. Le code QR mène au dépôt. La diapositive suivante liste toutes les sources citées.

## Diapositive 29 : Références (1/2)  (~31 s)

Ces deux diapositives listent toutes les sources citées, avec un lien cliquable pour chacune quand il existe : page arXiv, DOI ou site. Deux précisions d'honnêteté. Le chiffre d'IBM vient d'un article de synthèse qui cite le rapport 2026, pas du rapport lui-même. Et la référence « recherche bibliographique » est celle du notebook : 73 références dont j'ai ouvert chaque page, avec leur niveau de vérification.

## Diapositive 30 : Références (2/2)  (~6 s)

Suite des références. Elles sont numérotées dans l'ordre où elles apparaissent dans la présentation.

---
Total : environ 35 minutes de parole, sans les questions.

## Questions probables

**Pourquoi des logs synthétiques ?**
C'est le jeu fourni, SIEVE : les vrais logs d'entreprise sont rarement publics. Je le dis comme première limite : mes conclusions valent pour ces gabarits, pas encore pour du réel.

**Pourquoi un test scellé ?**
Pour ne pas régler mes choix sur le test. Il n'est ouvert qu'une fois, avec une trace datée, et mes règles de décision étaient écrites avant.

**Le 0,97 publié est-il faux ?**
Non, il est exact. Mais il mesure la reconnaissance de gabarits déjà vus, pas la compréhension. Séparé par gabarit, on tombe autour de 0,46 à 0,48.

**Que veulent dire macro-F1 et AUROC ?**
Macro-F1 : la note moyenne des 30 classes, qui combine « les logs trouvés sont-ils les bons » et « a-t-on trouvé tous les bons ». AUROC : la chance qu'un événement inconnu reçoive une note plus étrange qu'un connu ; 0,5 est le hasard, 1 est parfait.

**Pourquoi Mahalanobis ?**
La littérature le donne efficace sur un Transformer affiné. Je l'ai testé : il dépasse le score de confiance dans les cinq rotations, de 0,057 en moyenne, mais ne dépasse pas le comptage de mots.

**La hiérarchie aide-t-elle ?**
Pas démontré : le signe de l'écart change entre validation et test, toujours dans les marges d'erreur. La bonne famille est proposée une fois sur quatre.

**Pourquoi seulement 311 gabarits retrouvés sur 440 ?**
Les gabarits rares se confondent entre eux. Douze classes sur trente en ont moins de cinq. C'est dans mes limites.

**La défense par table officielle est-elle suffisante ?**
Elle limite la perte à 0,1 % face à mes attaques, mais ces attaques ne s'adaptent pas au modèle : je ne garantis rien face à un attaquant qui le connaît.

**À quoi servent les fichiers du professeur ?**
Ils ont les mêmes gabarits avec des valeurs nouvelles : un contrôle de fuite. Un modèle qui a vu tous les gabarits y obtient 0,97, un modèle dont le gabarit vient du test 0,44.

**Que feriez-vous en premier avec plus de temps ?**
Faire valider le regroupement en familles par un expert SIEM et tester sur de vrais logs, car c'est ce qui conditionne tout le reste.

## Conseils

- Ne dépassez pas ce que disent les chiffres : « à peine mieux que le hasard », pas « ça marche ».
- Sur les diapositives de résultats, dites d'abord la conclusion (le titre), puis montrez le graphique.
- Si une question vous dépasse, dites ce que vous avez mesuré et ce que vous ne savez pas.
