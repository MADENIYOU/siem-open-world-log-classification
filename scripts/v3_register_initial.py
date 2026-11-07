"""Inscrit dans le journal v3 les règles, les décisions déjà prises et les hypothèses du bloc A (préinscrites avant lecture de l'analyse). Idempotent : n'ajoute que ce qui manque."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
N = "Écrit le 2026-11-07 (soir) avant lecture de l'analyse du bloc A ; seul un pli (P2, répétition 0, pli 0) avait été vu lors du test de fumée."
REGLES = [
 ("R1", "Méthodique de bout en bout", "Chaque choix, chaque décision et chaque résultat est justifié par écrit (texte, raison, preuve).", "Demande de l'étudiant (2026-11-07) ; condition de la défense et de la publication."),
 ("R2", "Toute hypothèse reçoit un verdict", "Une hypothèse est préinscrite avant de voir les chiffres, puis confirmée, réfutée ou déclarée non tranchée. Aucune n'est laissée sans verdict.", "Évite de choisir l'hypothèse après coup."),
 ("R3", "On ne supprime jamais un résultat précédent", "Dans tout document (notebook, présentation, script oral, tableaux, registre), on garde le résultat précédent ET l'actuel, côte à côte quand c'est utile. Un recalcul forcé archive l'ancien fichier ; les archives ne sont jamais écrasées (`archive/`, `scripts/archive_state.py`) ; le journal est append-only.", "Traçabilité : on doit pouvoir montrer l'évolution et ce qui a changé, et pourquoi."),
 ("R4", "Unité statistique et baseline", "L'unité est le gabarit ; chaque bloc a une baseline ; comparaisons appariées ; correction de Holm pour les comparaisons multiples.", "Les logs d'un même gabarit ne sont pas indépendants (de 3 à 20 000 logs par gabarit)."),
 ("R5", "Test scellé v2 : une seule ouverture", "Le test v2 n'est lu par aucun script d'expérience ; il s'ouvre une fois, sur le pipeline figé (empreinte enregistrée), avec une trace datée.", "Le test v1 a été consommé le 2026-11-05 ; régler sur le test fausserait toute mesure."),
 ("R6", "Calculs reprenables et tracés", "Une unité terminée n'est jamais refaite ; une interruption ne coûte que l'unité en cours ; chaque unité écrit son empreinte, sa configuration, sa durée, sa machine et le commit.", "Demande de l'étudiant ; `src/tp2_runner.py`."),
 ("R7", "Sources vérifiées pour chaque aspect", "Chaque méthode ou choix s'appuie sur des sources dont la page a été ouverte, avec le niveau de vérification.", "Demande de l'étudiant ; `etat_de_l_art/sources_v3_*.md`."),
 ("R8", "Affinage itératif journalisé", "Chaque itération de la phase 2 a un numéro, une hypothèse, une configuration, un résultat et une décision ; arrêt à la fin de la semaine ou après trois itérations sans gain significatif.", "Rend l'affinage traçable et évite de s'arrêter trop tôt ou de tourner en rond."),
]
DECISIONS = [
 ("D1", "Nouveau test scellé v2", "Nouveau découpage des gabarits : 57 gabarits de test (17,6 % des logs), tirés parmi ceux qui n'ont jamais servi de test en v1 ; le test v1 est déclaré consommé.", "Toute nouvelle comparaison sur les mêmes gabarits n'est plus scellée.", "artifacts/data/splits_v3_meta.json"),
 ("D2", "Grille complète pour le Transformer", "6 bruits × 5 rotations × 3 graines.", "L'encodeur s'entraîne sur 4 200 logs par fichier : environ 3 minutes par modèle, donc réalisable sur Mac et Colab.", "colab/encoder_data_v2.csv.gz (25 200 logs d'entraînement)"),
 ("D3", "Au plus 400 logs par gabarit", "Dans les expériences linéaires de développement, tirage fixe d'au plus 400 logs par gabarit, pour l'entraînement comme pour l'évaluation.", "La taille des gabarits va de 3 à 20 000 logs : sans plafond, un gros gabarit pèserait 5 000 fois un petit et dominerait le macro-F1 ; le plafond accélère aussi le calcul.", "scripts/v3_blockA.py"),
 ("D4", "Métrique principale : macro-F1 du palier A", "Macro-F1 sur les classes de 5 gabarits ou plus (18 classes) ; le macro-F1 des 30 classes est rapporté en complément.", "Une classe de 1 à 2 gabarits ne peut pas être évaluée honnêtement (tous ses logs d'un seul côté) ; même convention que le notebook (sections 3.2 et 7.4).", "notebook v1, sections 3.2 et 7.4"),
 ("D5", "Critères d'acceptation du tirage du test v2", "Part de logs de test entre 10 et 22 %, au moins 1 gabarit de test par classe de 5 gabarits ou plus, quasi-jumeaux (cosinus >= 0,90) au plus 2 % ; sinon graine suivante.", "Garantit un test peu semblable à l'entraînement (demande de l'étudiant) et assez grand ; la graine 1 a été acceptée du premier coup (0,22 % de quasi-jumeaux).", "artifacts/data/splits_v3_meta.json"),
 ("D6", "Protocole imbriqué (P3) sur trois répétitions seulement", "P3 est calculé pour les répétitions 0 à 2 (15 plis) et non 0 à 4.", "Coût : le réglage intérieur multiplie le calcul par environ 9 ; trois répétitions suffisent pour estimer la variabilité. Limite assumée et à rappeler dans les résultats.", "scripts/v3_blockA.py"),
]
HYP = [
 ("HA1", "Le découpage au hasard gonfle le score", "Pour chaque modèle, le macro-F1 du palier A est plus élevé sous P0 (au hasard) que sous P2 (par groupes) d'au moins 0,20 (Wilcoxon apparié par pli, Holm p < 0,05).", "Notebook v1 : 0,9735 contre 0,458 pour le SVM ; ici avec plafond de 400 logs par gabarit, à confirmer."),
 ("HA2", "Les protocoles par gabarit classent les modèles de la même façon", "Les classements des six modèles sous P1, P2 et P3 sont concordants (tau de Kendall moyen entre eux >= 0,60).", "Si les trois protocoles par gabarit disent la même chose, le choix du protocole ne change pas la conclusion sur les méthodes."),
 ("HA3", "Le hasard classe les modèles autrement", "Le tau de Kendall entre P0 et P2 est plus faible que la concordance moyenne entre protocoles par gabarit.", "Le hasard récompense la mémorisation de gabarits (par exemple le voisinage) : il peut donc faire choisir un mauvais modèle."),
 ("HA4", "Fuite résiduelle", "Part moyenne de quasi-jumeaux (cosinus >= 0,90) : au moins 10 % sous P0, au plus 2 % sous P1, P2 et P3.", "Notebook v1 : 24 % contre 1 % sur SIEVE_00 ; à vérifier avec le plafond de 400 logs par gabarit."),
 ("HA5", "Voisinage et centroïde sont moins bons que le SVM sur mots", "Sous P2, kNN et centroïde ont un macro-F1 inférieur à celui du SVM sur mots (Holm p < 0,05).", "Hypothèse peu informative : le test de fumée (un pli) allait déjà dans ce sens ; elle reste testée sur les 25 plis."),
 ("HA6", "Les n-grammes de caractères dépassent les mots", "Sous P2, le SVM sur caractères (3 à 5) dépasse le SVM sur mots (Holm p < 0,05).", "Notebook v1 : 0,515 contre 0,483 au test ; le test de fumée (un pli) allait dans l'autre sens : verdict à établir sur 25 plis."),
 ("HA7", "Le hasard est plus stable mais biaisé", "L'écart-type du macro-F1 entre plis est plus petit sous P0 que sous P2.", "Un découpage au hasard a moins de variabilité entre plis (les plis se ressemblent) mais surestime ; la stabilité ne prouve pas la justesse."),
 ("HA8", "Quel protocole prédit le mieux le test v2 ?", "À l'ouverture unique du test v2 : pour au moins 5 des 6 modèles, l'écart entre l'estimation du développement et le score du test v2 est plus petit sous P2 ou P3 que sous P0.", "C'est le seul critère qui mesure le biais réel d'un protocole ; verdict à l'ouverture du test v2 (R5)."),
]
n = 0
for i, t, tx, j in REGLES:
    if not J.exists(i): J.add(i, "regle", t, tx, justification=j); n += 1
for i, t, tx, j, pr in DECISIONS:
    if not J.exists(i): J.add(i, "decision", t, tx, justification=j, preuve=pr); n += 1
for i, t, tx, j in HYP:
    if not J.exists(i): J.add(i, "hypothese", t, tx, justification=j, statut="préinscrite", note=N); n += 1
print(n, "entrées ajoutées ;", len(J.entries()), "au total"); print(J.render())
