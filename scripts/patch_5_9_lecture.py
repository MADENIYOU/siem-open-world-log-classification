"""Ajoute au notebook la lecture de 5.9 (a à e), le registre V95-V99, H13-H15 dans 10.2b, l'enseignement 16 et la fiche. Idempotent."""
import re
import nbformat as nbf
from pathlib import Path
NB = Path(__file__).resolve().parents[1] / "TP2_logs_hierarchique_monde_ouvert.ipynb"; nb = nbf.read(NB, as_version=4)
txt = lambda c: "".join(c.source)
if any("REV-5.9-L" in txt(c) for c in nb.cells): raise SystemExit("déjà appliqué")
LECTURE = """<!-- REV-5.9-L -->
**Lecture (5.9).** Modèle : TF-IDF mots + SVM linéaire (`C = 1`), macro-F1 sur les 30 classes.

**(a) Fuite sur données fraîches.** Entraîné sur les 59 940 logs d'entraînement de SIEVE (découpage par gabarit de l'étape 3) :

| Jeu évalué | macro-F1 | Exactitude |
|---|---|---|
| Validation (gabarits nouveaux) | **0,6426** | 0,6891 |
| Fichier du professeur p = 0 | **0,8107** | 0,8103 |
| p = 0,1 ; 0,2 ; 0,3 ; 0,4 | 0,8087 ; 0,8072 ; 0,8037 ; 0,8019 | |
| p = 0,5 | 0,7985 | 0,7979 |

**H13 est réfutée telle qu'elle était écrite** (au moins 0,90 à p = 0 et un écart d'au moins 0,25 avec la validation : on obtient 0,81 et 0,17). Le score décroît bien avec p, mais il est **plus bas que prévu**.

**(e) Pourquoi 0,81 ? (décomposition).** Le modèle n'a vu que les gabarits du découpage d'**entraînement** ; 5 000 logs du fichier p = 0, regroupés selon le découpage du log de SIEVE_00 le plus proche :

| Plus proche voisin dans… | Part des logs | Exactitude |
|---|---|---|
| l'entraînement | 63,5 % | **0,957** |
| la validation | 17,0 % | 0,673 |
| le test | 19,6 % | **0,438** |

La règle écrite avant le résultat (au moins 0,90 pour l'entraînement ; au moins 0,15 de moins pour validation et test) est **satisfaite** : **l'explication tient**. Quand le gabarit du log est connu du modèle, il est **quasi parfait** (0,957) ; quand il vient d'un gabarit du jeu de test, on retombe à **0,438**, **au niveau de notre test scellé** (0,459). Le chiffre de 0,81 est une **moyenne** de ces deux situations, pas un résultat propre.

**(b) Taille du jeu : 100K contre 35K.** Entraîné sur 100 000 logs et testé sur 35 000 : **0,9721** (p = 0) à **0,9668** (p = 0,5) ; entraîné sur 35 000 et testé sur 100 000 : **0,9732** à **0,9630**. Quand le modèle a vu **tous les gabarits**, le score est **≈ 0,97**, comme le découpage aléatoire de l'étape 3 (0,987) et l'article (0,9737), et **la taille du jeu ne change presque rien** (écarts de 0,001 à 0,007).

**(c) Courbe de taille (p = 0).** Découpage **aléatoire** (gabarits connus) : 0,9547 (2 000 logs), **0,9721** (5 000), 0,9744, 0,9731, 0,9710, 0,9714 (60 000) : **saturation dès 5 000 logs** ; gain de 35 000 à 60 000 : **+0,0004** (**H14 confirmée**, seuil 0,01). Découpage **par gabarit** (gabarits nouveaux) : 0,6245 → 0,6271 → 0,6284 → 0,6323 → 0,6177 → 0,6155 : **plat** (étendue de 0,017, seuil 0,05 : **H14 confirmée**) ; plus de données **n'aide pas** à généraliser à de nouveaux gabarits.

**(d) Quasi-jumeaux.** Part de logs du professeur ayant un log de SIEVE (même p) de cosinus au moins 0,90 : **0,262** (p = 0), 0,148 ; 0,103 ; 0,078 ; 0,072 ; **0,057** (p = 0,5). Classe du plus proche identique : **0,936** à **0,905**. **H15 confirmée** (≈ 25 % à p = 0, décroissante) ; le taux de 0,262 est celui d'un **découpage aléatoire** (0,254 en 3.7).

**Conclusion.** Les fichiers du professeur sont des logs **neufs sur des gabarits connus**. Ils fournissent une **seconde mise en évidence de la fuite** (H5) : **≈ 0,97** quand le modèle a vu tous les gabarits, **≈ 0,44 à 0,64** quand le gabarit est nouveau ; et la **taille du jeu n'y change rien** (35 000 ou 100 000 logs). Ils **ne remplacent pas** le test scellé. *Limites :* un seul modèle et une seule graine d'échantillonnage ; fichiers produits par le même générateur (pas de logs réels) ; provenance vérifiée dans l'article (taille de 35 000), pas auprès du professeur ; la décomposition (e) utilise le plus proche voisin comme **indicateur** du gabarit (le vrai identifiant de gabarit n'existe pas pour ces fichiers).

**Registre (suite).**

| N° | Affirmation | Source | Niveau |
|---|---|---|---|
| V95 | Fichiers du professeur : six fichiers de 35 000 logs (p = 0 à 0,5), 30 classes équilibrées, mêmes gabarits que SIEVE 100K ; modèle entraîné sur le découpage d'entraînement : macro-F1 0,6426 (validation) contre 0,8107 (p = 0) à 0,7985 (p = 0,5) ; H13 réfutée | Calcul (5.9a) ; article (taille 35 000) | calcul |
| V96 | Décomposition de 0,81 : plus proche voisin dans l'entraînement 63,5 % des logs, exactitude 0,957 ; validation 17,0 %, 0,673 ; test 19,6 %, 0,438 (5 000 logs, p = 0) | Calcul (5.9e) | calcul (indicateur de gabarit) |
| V97 | 100K vers 35K : 0,9721 (p = 0) à 0,9668 (p = 0,5) ; 35K vers 100K : 0,9732 à 0,9630 ; la taille du jeu change peu | Calcul (5.9b) | calcul |
| V98 | Courbe de taille (p = 0) : découpage aléatoire 0,9547 (2 000 logs) à 0,9714 (60 000), gain de 35 000 à 60 000 de +0,0004 ; découpage par gabarit 0,6245 à 0,6155, étendue 0,017 | Calcul (5.9c) | calcul (une graine) |
| V99 | Quasi-jumeaux (cosinus ≥ 0,90) entre les logs du professeur et SIEVE 100K : 0,262 (p = 0) à 0,057 (p = 0,5) ; classe du plus proche identique 0,936 à 0,905 | Calcul (5.9d) | calcul (3 000 logs par fichier) |"""
i = max(k for k, c in enumerate(nb.cells) if c.cell_type == "code" and "fig_5_9b" in txt(c))
c = nbf.v4.new_markdown_cell(LECTURE); c.metadata["rev_auto"] = True; nb.cells.insert(i + 1, c)
def sub(marker, old, new, guard):
    cell = next(c for c in nb.cells if c.cell_type == "markdown" and marker in txt(c))
    if guard in cell.source: return
    assert old in cell.source, f"texte absent : {old[:70]!r}"; cell.source = cell.source.replace(old, new, 1)
H = """
| **H13** | Entraîné sur les gabarits d'entraînement, le modèle obtient au moins 0,90 de macro-F1 sur les logs frais du professeur (p = 0), avec un écart d'au moins 0,25 avec la validation | **Réfutée** (expliquée) | 5.9 : 0,81 et écart 0,17 ; le modèle n'a vu que 63,5 % des gabarits : exactitude 0,957 quand le plus proche voisin est dans l'entraînement, 0,438 quand il est dans le test (niveau du test scellé). |
| **H14** | Taille : plateau avec un découpage aléatoire, plat avec un découpage par gabarit | **Confirmée** | 5.9 : aléatoire, gain de 35 000 à 60 000 logs +0,0004 ; par gabarit, étendue 0,017 ; 100K contre 35K : écart de 0,001 à 0,007. |
| **H15** | Part de quasi-jumeaux d'environ 25 % à p = 0 et décroissante | **Confirmée** | 5.9 : 0,262 (p = 0) à 0,057 (p = 0,5). |"""
cell = next(c for c in nb.cells if c.cell_type == "markdown" and "10.2b Les hypothèses ajoutées" in txt(c))
if "| **H13** |" not in cell.source:
    lines = cell.source.split("\n"); j = max(k for k, l in enumerate(lines) if l.startswith("| **H12** |")); lines[j] = lines[j] + H; cell.source = "\n".join(lines)
sub("10.2b Les hypothèses ajoutées", "H12 a été écrite **avant** les chiffres de 9.12.", "H12 a été écrite **avant** les chiffres de 9.12 ; H13 à H15 (fichiers du professeur, 5.9) avant les chiffres de 5.9.", "H13 à H15 (fichiers")
cell = next(c for c in nb.cells if c.cell_type == "markdown" and "## 10.5 Ce que le projet a appris" in txt(c))
if "16. **Les logs neufs" not in cell.source:
    lines = cell.source.split("\n"); j = max(k for k, l in enumerate(lines) if l.startswith("15. **Le bruit d'entraînement compte.**"))
    lines[j] = lines[j] + "\n16. **Les logs neufs ne suffisent pas à tester la généralisation.** Les fichiers du professeur (35 000 logs par version, mêmes gabarits que SIEVE 100K) donnent ≈ 0,97 quand le modèle a vu tous les gabarits et 0,44 quand le gabarit vient du jeu de test : c'est la **fuite** (H5) mise en évidence sur des données indépendantes, et la taille du jeu (35 000 ou 100 000) n'y change rien. Seule la séparation **par gabarit** mesure la généralisation."
    cell.source = "\n".join(lines)
cell = next(c for c in nb.cells if c.cell_type == "markdown" and "| **H5** |" in txt(c))
if "logs frais du professeur" not in cell.source:
    lines = cell.source.split("\n"); j = next(k for k, l in enumerate(lines) if l.startswith("| **H5** |")); lines[j] = lines[j].rstrip().rstrip("|").rstrip() + " **Contrôle sur logs frais du professeur (5.9)** : 0,97 quand le modèle a vu tous les gabarits. |"; cell.source = "\n".join(lines)
for c in nb.cells:
    if c.cell_type == "markdown":
        c.source = c.source.replace("registre V1 à V94", "registre V1 à V99").replace("**V74 à V94** sont en 0.1b.6, 1.7, 3.7, 4.11, 5.8, 6.4, 7.2b, 9.12 et 10.4c.", "**V74 à V99** sont en 0.1b.6, 1.7, 3.7, 4.11, 5.8, 5.9, 6.4, 7.2b, 9.12 et 10.4c.")
FICHE_ADD = """## Étape 5 (suite) : fichiers du professeur
| Question | Réponse courte |
|---|---|
| Peut-on utiliser les `output_*.log` du professeur comme jeu de test ? | Pas comme test de généralisation : ce sont des logs neufs mais sur les **mêmes gabarits** que SIEVE 100K (26 % de quasi-jumeaux à p = 0, comme un découpage aléatoire). Ils servent de contrôle de fuite. |
| Pourquoi un modèle entraîné sur SIEVE n'obtient-il que 0,81 sur ces fichiers, et non 0,97 ? | Il n'a vu que les gabarits du découpage d'entraînement : 0,957 quand le gabarit du log est dans son entraînement (63,5 % des logs), 0,438 quand il vient du jeu de test (19,6 %), niveau de notre test scellé. |
| La taille du jeu (35 000 ou 100 000 logs) change-t-elle le résultat ? | Presque pas : 0,972 dans les deux sens ; la courbe sature dès 5 000 logs avec un découpage aléatoire et reste plate avec un découpage par gabarit. Plus de données n'aide pas à généraliser à de nouveaux gabarits. |

"""
fiche = next(c for c in nb.cells if c.cell_type == "markdown" and "REV-FICHE" in txt(c))
if "fichiers du professeur" not in fiche.source and "## Étape 6 : modèles et scores d'inconnu" in fiche.source: fiche.source = fiche.source.replace("## Étape 6 : modèles et scores d'inconnu", FICHE_ADD + "## Étape 6 : modèles et scores d'inconnu", 1)
nbf.write(nb, NB); print("lecture 5.9 et mises à jour appliquées ; cellules :", len(nb.cells))
