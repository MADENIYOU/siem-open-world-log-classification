# Méthodologie d'article : publiable, vérifiable, reproductible (2026-11-10)

Précision de l'étudiant : le mot entendu « OGL » était une erreur de dictée ; l'intention est **une méthodologie d'article** : que le travail devienne un **article publiable et vérifiable**. Ce document traduit cette intention en règles de travail, en plan d'article, en liste de preuves et en écarts à combler. **Aucun calcul n'est lancé ici.**

Les références méthodologiques sont déjà dans `etat_de_l_art/sources_v3_stats_repro.md` (Dodge, Pineau, Demšar, Benavoli, Bouthillier, Gebru, Mitchell, Gundersen, Kapoor, Lones, Raschka, Hendrycks : niveau de vérification indiqué dans ce fichier) ; je ne les redéfinis pas ici et **je ne cite pas de lieu de publication ni de date limite sans les avoir vérifiés** (voir §7).

## 1. Ce qu'un article publiable exige, et où on en est

| Exigence | État | Preuve dans le dépôt |
|---|---|---|
| Question de recherche claire et nouveauté défendable | **À formuler** (voir §3) | PLAN_V3.md §3.1 (lacunes → contributions) |
| Hypothèses écrites avant les résultats, verdicts honnêtes | **Fait** | `journal.jsonl` (append-only), `REGISTRE_V3.md`, règle R2 ; 37 confirmées, 30 réfutées, 9 non tranchées |
| Séparation développement / confirmation / test scellé | **Fait** | test v2 scellé, journal d'accès vide, D20 (itérer puis ouvrir une fois) |
| Résultats négatifs rapportés | **Fait** | RI1, RI2, RI5, RI6, RT2, HF1 à HF6, HF10 à HF12… |
| Statistiques appropriées (unité = gabarit, plusieurs tests, IC, correction multiple) | **Fait** | `src/tp2_stats.py` (Wilcoxon, signes, permutation, Friedman + Nemenyi, Holm, bootstrap), 15 tests unitaires |
| Reproductibilité du code et des données | **Largement fait** | VERSIONS.md (≈ 80 versions), copies figées, crochet git, `requirements.txt`, graines, journal des calculs, empreinte des données |
| Ablations et comparaisons à des bases solides | **Fait pour la phase 1**, **à faire pour nos formules** | blocs A à E ; F6 à F23 à tester |
| Menaces à la validité écrites | **À rédiger** (voir §5) | notes éparses dans le registre |
| Jeu de données et licence | **Contrainte** : données obtenues par demande au professeur (non redistribuables) | à traiter : publier scripts, hachages et découpages, pas les données |
| Éthique et usage dual | **À rédiger** : détection d'inconnus de sécurité, attaques sur le texte (homoglyphes) | §5 |
| Relecture indépendante interne (revue de l'article avant envoi) | **À prévoir** | §6 |

## 2. Règles de travail « article » (à appliquer maintenant à chaque itération)

1. **Une affirmation de l'article = une hypothèse du registre.** Pas de phrase de résultat sans identifiant HA… HI… et verdict. On génère un tableau « affirmation → hypothèse → verdict → fichiers » (`article/TABLE_AFFIRMATIONS.md`, produit par script à partir du journal).
2. **Préinscription avant calcul, daté et immuable** : journal append-only + commit git avant le lancement. Déjà en place.
3. **Sélection sur le développement, confirmation sur des données neuves, test scellé une fois** (D20) ; jamais de réglage sur la confirmation.
4. **Rapporter la distribution, pas le meilleur** : pour toute grille, rapporter la performance de **toutes** les configurations (le maximum d'une grille est optimiste : I6b l'a montré) et le budget de recherche (nombre de configurations, heures de calcul). Référence : « Show Your Work » (Dodge et al.), dans `sources_v3_stats_repro.md`.
5. **Tailles d'effet et intervalles avant les p-valeurs** ; plusieurs tests concordants ; correction de Holm pour les familles ; décision par IC bootstrap (déjà la pratique).
6. **Toute correction est une nouvelle entrée, jamais un remplacement** (R3) : l'article peut raconter ces corrections (OpenMax inversé, LOF, Friedman à l'envers, HA1) comme preuve de rigueur.
7. **Chaque figure et chaque tableau sortent d'un script versionné** (`article/figures/*.py`) lisant `artifacts/results/v3/*.csv`.
8. **Journal de calcul** : machine, durée, appareil, graine, version de code par unité (déjà dans les enregistrements d'unités).
9. **Tout ce qui est exploratoire est étiqueté « exploratoire »** (DG2, RC2) et séparé des confirmations.
10. **Aucune citation sans source ouverte** : « texte intégral lu » / « résumé lu » / « non vérifié » dans chaque tableau de sources.

## 3. Question, contributions et plan de l'article

**Titre de travail** : *Classification hiérarchique de logs de sécurité en monde ouvert : ce qui se généralise à des gabarits nouveaux, et ce qui ne se généralise pas.*

**Questions de recherche (RQ)**
- RQ1 : quel est le vrai niveau de classification de logs quand les gabarits de test ne sont **jamais vus** ? (bloc A)
- RQ2 : quelles méthodes (représentations, classifieurs, hiérarchie, clustering) généralisent le mieux ? (blocs B, V, T, phase 2)
- RQ3 : comment détecter des **classes** inconnues, et le niveau de famille aide-t-il ? (bloc C, I4 à I7c)
- RQ4 : quelle est la robustesse aux perturbations de texte et quelles défenses valent quelque chose ? (bloc D)
- RQ5 : la confiance est-elle calibrée sous décalage de gabarits ? (bloc E)
- RQ6 : **peut-on dépasser le plafond d'environ 0,50 avec des méthodes pensées pour le décalage de gabarits ?** (formules maison, vagues 1 à 4)

**Contributions candidates (honnêtes)**
1. **Quantification de la fuite de gabarits** : 0,986 contre 0,50 sur le même modèle et le même jeu ; protocole par groupes réutilisable (si le professeur confirme que ce n'est pas déjà publié ; à vérifier).
2. **Étude comparative systématique** (19 classifieurs, 3 vectorisations, 32 réglages, Transformer, jetons typés, fusion) montrant un **plafond robuste** et analyse de sa cause (DG2).
3. **Confiance de famille pour le monde ouvert** : +0,04 d'AUROC confirmé sur 75 unités de rotations jamais vues, FPR@95 inchangé (résultat positif modeste).
4. **Défense par table officielle UTS #39** démontrée et correction d'un résultat circulaire (parade « table maison »).
5. **Pratique de rigueur** : préinscription, résultats négatifs, corrections tracées.
6. **Si les vagues réussissent** : nos formules (axes objet × action, décodage à masses équilibrées, désentrelacement du format, invariance entre gabarits) comme contribution méthodologique principale.

*Évaluation honnête* : sans amélioration nette du score, l'article se place comme **étude d'évaluation et résultat négatif informatif** (utile, vérifiable) plutôt que comme nouvelle méthode ; les formules maison décident du genre d'article.

**Plan (IMRaD étendu)**
1. Introduction : problème, fuite de gabarits, RQ, contributions.
2. Travaux liés : logs et gabarits ; classification hiérarchique ; monde ouvert en texte ; robustesse ; calibration (sources vérifiées uniquement).
3. Données et protocole : SIEVE, gabarits reconstruits (311), paliers, protocoles P0-P3, rotations, test scellé ; **menaces** déjà en §5.
4. Méthodes : représentations, classifieurs, scores d'inconnu, formules maison F6-F23 (avec définition et justification).
5. Expériences et résultats : un sous-chapitre par RQ ; tableaux avec IC et tests ; figures.
6. Analyse : DG2, causes du plafond, ablations des formules, résultats négatifs.
7. Menaces à la validité, limites, éthique.
8. Conclusion et travaux futurs.
Annexes : registre complet des hypothèses, table de versions, détails de calcul, listes de configurations, check-list de reproductibilité.

## 4. Preuves de vérifiabilité (paquet de reproduction)
- `requirements.txt` + version de Python, empreinte des données (`DATA_ID`), empreintes des découpages (`groups_v3.csv`, `splits_v3_meta.json`), graines.
- Script unique `scripts/reproduce_all.sh` (à écrire) : régénère les tableaux et figures depuis `artifacts/results/v3/*.csv`, et relance au besoin les unités manquantes.
- Étiquette git par jalon (déjà : `etat-2026-11-07-avant-v3`) ; **étiquette finale avant ouverture du test**, puis étiquette après.
- Test v2 : **un seul** accès journalisé (`test_v2_access_log.json`).
- Données non redistribuables : on publie les **empreintes**, les identifiants de gabarits et les scripts ; la demande d'accès au professeur est décrite.
- Fiches : jeu de données (Gebru et al.), modèle (Mitchell et al.) en annexe (références dans `sources_v3_stats_repro.md`).

## 5. Menaces à la validité (à rédiger, déjà identifiées)
- **Interne** : gabarits **reconstruits** (311 au lieu de 440 annoncés : fusion possible de gabarits) ; plafond de 400 logs par gabarit ; sélection sur le développement ; défauts de code trouvés et corrigés (OpenMax, Friedman) ; plis dépendants (mêmes gabarits) — d'où la confirmation sur nouvelles rotations et nouveaux plis, mais **jamais de nouveaux gabarits avant le test v2**.
- **Externe** : un seul jeu de données **synthétique** (SIEVE), une seule version principale (SIEVE_00) ; 311 gabarits seulement ; taxonomie à 8 familles = **hypothèse de démonstration** ; axes objet × action tirés des noms de classes (à valider).
- **Construit** : macro-F1 du palier A (18 classes) qui exclut les classes à peu de gabarits ; AUROC d'inconnu dépend des classes masquées (forte variabilité entre rotations).
- **Statistique** : l'unité est le gabarit (≈ 311) mais les tests sur 25 plis ne sont pas indépendants ; décisions par IC bootstrap ; beaucoup de « réfutées » ont un IC trop large pour exclure +0,01 (voir F11, F23).
- **Éthique et usage dual** : attaques par homoglyphes ; on publie la défense (table officielle) et des attaques simples déjà connues, pas d'outil offensif.

## 6. Plan de travail jusqu'au samedi 2026-11-14 (version article)
1. **Aujourd'hui** : valider le plan avec l'étudiant ; décider des comptages sans entraînement (format × classe, vocabulaire, axes) ; préinscrire la vague 1.
2. **J+1 à J+2** : vagues 1 et 2 (F8, F14, F6, F9, puis F7, F18, F19/F20), chaque vague avec sélection puis confirmation.
3. **J+3** : vague 3 si le temps le permet (LP-FT, embeddings gelés) ; **gel du pipeline** et étiquette git ; **ouverture unique du test v2** (vendredi au plus tard).
4. **J+3 à J+4** : écriture de l'article (tableau des affirmations généré, figures par scripts), notebook partie 2, présentation ; **relecture croisée** : un sous-agent relit l'article à la recherche d'affirmations sans preuve et de chiffres incohérents avec le registre.
5. Commit et push par version ; livraison.

## 7. Ce qui reste à vérifier avant de promettre une publication
- **Lieu de publication** : ateliers ou revues acceptant études d'évaluation et résultats négatifs, format et date limite : **à rechercher et vérifier** (je ne les cite pas ici).
- **Antériorité** : si l'article du jeu SIEVE ou d'autres travaux ont déjà quantifié la fuite de gabarits ; à vérifier dans le texte intégral (la version actuelle du fichier de sources n'a que des résumés).
- **Droits sur les données** : conditions d'utilisation de SIEVE (demande par e-mail) : ce qu'on peut publier.
- **Accord du professeur** sur : taxonomie, mention des fichiers `output_*.log`, publication.

## 8. Décisions à prendre ensemble
1. Valider que l'objectif est un **article d'évaluation rigoureuse avec résultats négatifs + nos formules**, le genre précis dépendant des vagues.
2. Feu vert pour les trois comptages sans entraînement, puis la vague 1.
3. Je recherche (recherche web, aucun calcul) les lieux de publication adaptés et leurs exigences, pour cadrer le format ?

---

## Rectificatif (2026-11-10) : règle 11, test strictement scellé
**Règle 11.** Le test v2 est **scellé et intouchable** : aucune lecture, aucun comptage, aucune statistique (format, vocabulaire, distribution des classes, nombre de gabarits…) ne le concerne avant l'**unique** ouverture, faite sur un pipeline gelé et journalisée. Les seules opérations autorisées avant : (1) le sceller (déjà fait en D1, journal d'accès vide) ; (2) vérifier **mécaniquement** qu'il n'a pas été ouvert. Propositions de vérification à faire valider par l'étudiant (aucune ne lit le contenu du test) : une empreinte de la liste des identifiants scellés, inscrite dans le journal ; un garde automatique qui refuse tout script lisant le rôle « test2 » ; le contrôle du journal d'accès dans le crochet git. Les menaces à la validité (§5) et le plan (§6) sont à lire avec cette règle.
