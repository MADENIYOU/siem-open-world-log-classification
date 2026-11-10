"""Journal : amendement D35 de la vague 4 (variante DRO2 ajoutée avant tout calcul de sélection) et hypothèse HZ3b. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
N = "Écrit le 2026-11-10, après le test sur UN pli (non lu comme résultat) et avant tout calcul de la sélection de la vague 4."
if not J.exists("D35"):
    J.add("D35", "decision", "Amendement de la vague 4 : DRO2 (poids bornés) ajouté à DRO1",
          "Un test sur un pli (répétition 0, pli 0) a révélé un défaut de la formule préinscrite de DRO1 (poids ∝ exp(perte logarithmique)) : la perte n'est pas bornée (jusqu'à 20,7 quand la classe du gabarit manque au pli d'apprentissage interne) ; les poids se concentrent sur 5 gabarits « équivalents » sur 203 et le modèle est inutilisable (macro-F1 0). DRO1 est CONSERVÉ tel que préinscrit et sera rapporté (probablement dégénéré, ce qui est un résultat sur la formule). DRO2 ajoute avant tout calcul de sélection : poids ∝ exp(0,5 · min(perte, 4)), ce qui borne le rapport des poids à e² ≈ 7,4 et garde un nombre effectif de gabarits élevé. La porte HZ5 compte maintenant 6 variantes (Holm sur 6 au lieu de 5).",
          justification="Défaut de formule trouvé par un test de code, pas par un résultat de performance ; amendement écrit avant la sélection, sans suppression de DRO1.", note=N)
if not J.exists("HZ3b"):
    J.add("HZ3b", "hypothese", "Une pondération bornée des gabarits difficiles améliore la classification (F10, DRO2)", "DRO2 dépasse LR d'au moins 0,02 de macro-F1 du palier A, mode brut, condition « toutes » (Wilcoxon apparié unilatéral contre le seuil, Holm sur 6 variantes, p < 0,05).",
          justification="Version corrigée de HZ3 (D35).", statut="préinscrite", note=N)
print("ok")
