"""Journal : décision D21 (itération I5 : réglage des modèles linéaires mots + lettres, sélection sur répétitions 0-4, confirmation sur 5-9) et hypothèses HF13, HF14, préinscrites avant tout calcul. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
N = "Écrit le 2026-11-09 avant tout calcul de l'itération I5."
if not J.exists("D21"):
    J.add("D21", "decision", "Itération I5 : régler mots + lettres (procédure D20)",
          "Grille (SVM linéaire, 30 classes, SIEVE_00, développement seul) : C des mots ∈ {0,3 ; 1 ; 3} ; lettres : n-grammes char_wb ∈ {(2,4), (3,5), (4,6)} avec C ∈ {0,3 ; 1} ; poids de la marge lettres dans la somme ∈ {0 (mots seuls), 0,5 ; 1 ; 2 ; lettres seules} ; soit 3 × 3 × 2 × 3 combinaisons de somme plus les références. SÉLECTION : macro-F1 des classes (palier A) moyen sur les 25 plis des répétitions 0 à 4 ; la configuration au meilleur score est retenue (aucun autre critère, aucun arbitrage manuel). CONFIRMATION (I5b) : la configuration retenue est calculée sur les 25 plis des répétitions 5 à 9 et comparée à V0 (SVM mots, C = 1, résultats d'I1b, mêmes plis) ; la sélection n'utilise jamais ces plis. Le test v2 reste scellé (D20).",
          justification="D20 : itérer pour monter la précision ; la séparation sélection (rép. 0-4) / confirmation (rép. 5-9) évite l'optimisme de choisir le maximum d'une grille et de l'annoncer.", note=N)
H = [("HF13", "Le réglage améliore le macro-F1 des classes sur de nouveaux plis", "La configuration retenue sur les répétitions 0 à 4 dépasse V0 d'au moins 0,02 en macro-F1 (palier A) sur les 25 plis des répétitions 5 à 9 (Wilcoxon apparié unilatéral, p < 0,05). Réfutée si l'IC95 bootstrap de l'écart exclut +0,02 ; sinon non tranchée.", "Les réglages par défaut (C = 1, n-grammes 3-5, poids 1) n'ont jamais été optimisés pour les gabarits nouveaux."),
     ("HF14", "Une configuration vaut le coup d'être confirmée", "Sur les répétitions 0 à 4, la meilleure configuration dépasse V0 d'au moins 0,02 en macro-F1 des classes (porte : en dessous, la confirmation n'est pas lancée ; le meilleur d'une grille est biaisé vers le haut, donc ce gain n'est pas un résultat).", "Évite de gaspiller la confirmation et de présenter un maximum de grille comme un gain.")]
for i, t, tx, j in H:
    if not J.exists(i): J.add(i, "hypothese", t, tx, justification=j, statut="préinscrite", note=N)
print("ok")
