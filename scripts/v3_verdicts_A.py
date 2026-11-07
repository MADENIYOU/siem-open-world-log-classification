"""Verdicts du bloc A, inscrits comme NOUVELLES versions des hypothèses (les versions « préinscrite » restent dans l'historique). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
P = "artifacts/results/v3/A_*.csv ; A_all_units.csv ; journal.jsonl"
V = {
 "HA1": ("Le découpage au hasard gonfle le score", "Pour chaque modèle, macro-F1 du palier A sous P0 moins sous P2 d'au moins 0,20 (Wilcoxon apparié, Holm p < 0,05).", "confirmée",
         "Écarts P0 moins P2 : centroïde 0,468 ; kNN 0,551 ; LR 0,491 ; Naive Bayes 0,511 ; SVM caractères 0,488 ; SVM mots 0,483. Les six dépassent 0,20 ; Wilcoxon sur 25 plis, p ajusté < 1e-6, Cliff delta = 1 pour tous.", "Réserve : l'appariement par (répétition, pli) entre P0 et P2 n'est pas strict (plis différents) ; l'écart est cependant si grand devant la variabilité (écart-type 0,06) que le verdict ne dépend pas de cet appariement."),
 "HA2": ("Les protocoles par gabarit classent les modèles de la même façon", "Tau de Kendall moyen entre P1, P2 et P3 >= 0,60.", "confirmée",
         "Tau : P1-P2 0,867 ; P1-P3 0,733 ; P2-P3 0,600 ; moyenne 0,733.", "Réserve : avec six modèles, le tau ne prend que des valeurs par pas de 0,067 ; et les trois meilleurs (SVM mots, SVM caractères, régression logistique) ne se distinguent pas statistiquement entre eux (Nemenyi, p > 0,98), donc leurs permutations de rang ne sont pas des désaccords réels."),
 "HA3": ("Le hasard classe les modèles autrement", "Tau(P0, P2) strictement plus faible que la concordance moyenne entre protocoles par gabarit.", "réfutée",
         "Tau(P0, P2) = 0,733, égal à la moyenne des trois tau par gabarit (0,733) : pas plus faible. Tau(P0, P1) = 0,600 et tau(P0, P3) = 0,600 restent dans la fourchette des tau entre protocoles par gabarit (0,600 à 0,867).", "Interprétation : avec ces six modèles linéaires, le découpage au hasard classe les familles de modèles presque comme les découpages par gabarit (SVM et LR devant, kNN et centroïde derniers). Il surestime le NIVEAU de score mais, ici, pas l'ORDRE des méthodes ; il nomme toutefois un autre meilleur modèle (SVM caractères au lieu de SVM mots). Cet effet pourrait apparaître avec des modèles plus capables de mémoriser (Transformer), à tester au bloc B/vectorisation."),
 "HA4": ("Fuite résiduelle", "Quasi-jumeaux : >= 10 % sous P0 ; <= 2 % sous P1, P2, P3.", "confirmée",
         "Part de quasi-jumeaux (cosinus >= 0,90) : P0 20,5 % ; P1 1,3 % ; P2 0,8 % ; P3 0,7 %. Cosinus médian au plus proche voisin : 0,732 ; 0,442 ; 0,465 ; 0,466.", "Résultat cohérent avec le notebook v1 (24 % contre 1 % sur SIEVE_00)."),
 "HA5": ("Voisinage et centroïde sont moins bons que le SVM sur mots", "Sous P2, kNN et centroïde ont un macro-F1 inférieur au SVM sur mots (Holm p < 0,05).", "confirmée",
         "SVM mots moins kNN : +0,093, IC 95 % bootstrap [0,071 ; 0,117], p Holm 9e-7 ; SVM mots moins centroïde : +0,098, IC [0,076 ; 0,119], p Holm 1e-6. Naive Bayes aussi inférieur (+0,070, p Holm 3e-6). Nemenyi : kNN, centroïde et Naive Bayes ne se distinguent pas entre eux.", "Hypothèse peu informative au départ (un pli vu au test de fumée), mais verdict établi sur 25 plis."),
 "HA6": ("Les n-grammes de caractères dépassent les mots", "Sous P2, SVM caractères supérieur au SVM mots (Holm p < 0,05).", "réfutée",
         "Écart SVM mots moins SVM caractères : +0,003 (IC 95 % [-0,015 ; +0,022], p Holm 0,79) ; caractères meilleur dans 11 plis sur 25. L'IC écarte un gain des caractères supérieur à 0,015. Pour contexte : sous P0 l'écart est de +0,002 (en faveur des caractères, p non significatif au sens pratique) et sous P3 de +0,010 (p = 0,33).", "Le résultat du notebook v1 (0,515 contre 0,483) ne se retrouve pas avec ce découpage et ce plafond de 400 logs par gabarit : aucune supériorité démontrée. Les deux représentations restent à comparer sous bruit (bloc vectorisation × fichiers) et sous attaque (bloc D), où les caractères devraient surtout compter."),
 "HA7": ("Le hasard est plus stable mais biaisé", "Écart-type du macro-F1 entre plis plus petit sous P0 que sous P2.", "confirmée",
         "Écart-type moyen entre plis : P0 0,0020 ; P1 0,0632 ; P2 0,0590 ; P3 0,0583.", "Un découpage stable n'est pas un découpage juste : P0 est trente fois plus stable et surestime de près de 0,5."),
}
n = 0
for i, (titre, texte, statut, preuve, note) in V.items():
    if J.entries() and [e for e in J.entries() if e["id"] == i][-1]["statut"] != "préinscrite": continue
    J.add(i, "hypothese", titre, texte, justification="Verdict établi avec les règles de décision préinscrites (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + P, note=note); n += 1
if not J.exists("RA1"):
    J.add("RA1", "resultat", "Bloc A : macro-F1 du palier A par protocole (précédent v1 et actuel v3)",
          "**Précédent (notebook v1, étape 3.7, SVM sur TF-IDF mots, SIEVE_00, palier A, tout le jeu d'entraînement) :** P0 0,9872 ; P1 0,4220 ; P2 0,5070 ; P3 0,5105.  **Actuel (v3, SVM sur mots, 400 logs par gabarit au plus, développement) :** P0 0,986 ; P1 0,471 ; P2 0,503 ; P3 0,487.  Les deux séries sont conservées. Écart notable pour P1 (0,422 contre 0,471) : le P1 de v1 est un seul découpage de 36 gabarits de validation, celui de v3 est la moyenne de 5 plis de gabarits différents (écart-type 0,063) ; la valeur de v1 est dans l'intervalle de celles de v3.  Tous les modèles : P0 de 0,874 (centroïde) à 0,988 (SVM caractères) ; P2 de 0,406 (centroïde) à 0,503 (SVM mots).",
          justification="Montre que le niveau de score et le contraste hasard / gabarit se reproduisent avec un protocole indépendant (autres gabarits de test, nouveau plafond), ce qui renforce la conclusion de v1.", preuve=P, note="Conformément à R3, ni la série v1 ni la série v3 n'est écartée.")
    n += 1
if not J.exists("D7"):
    J.add("D7", "decision", "P2 (validation croisée par groupes, 5 plis × 5 répétitions) est le protocole par défaut des blocs B à E",
          "Pour la comparaison de méthodes sur le développement, on utilise P2.", justification="Sans fuite (0,8 % de quasi-jumeaux), même classement que P1 (tau 0,87), précision proche de P3 (écart-type 0,059 contre 0,058) pour un coût environ neuf fois moindre, et 25 plis donnent assez de blocs pour Friedman et Wilcoxon. Provisoire : confirmé ou infirmé à l'ouverture du test v2 (HA8).",
          preuve="RA1 ; HA2 ; HA4 ; HA7"); n += 1
print(n, "entrées ajoutées"); print(J.render())
