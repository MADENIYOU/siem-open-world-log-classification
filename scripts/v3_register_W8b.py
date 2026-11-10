"""Journal : verdicts de sélection HQ2, HQ3 (D38) ; décision D39 (confirmer trois candidats sur 50 plis neufs) et hypothèses HQ6, HQ7, préinscrites avant la confirmation. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8_selected.json"
if last("HQ2")["statut"] == "préinscrite":
    J.add("HQ2", "hypothese", last("HQ2")["titre"], last("HQ2")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D38).", statut="réfutée",
          preuve="Sélection (25 plis) : PIPE 0,5544 ; ENSP30 0,5569 (+0,0025, IC95 [−0,002 ; 0,007]) ; ENSP50 0,5561 (+0,0017, IC95 [−0,007 ; 0,010]) ; bornes hautes < 0,02 ; Holm 1,0.  Fichiers : " + F, note="Ajouter les lettres avant le décodage n'apporte rien : le gain de famille de HF7 ne se traduit pas en gain de classe après décodage.")
    J.add("HQ3", "hypothese", last("HQ3")["titre"], last("HQ3")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D38).", statut="non tranchée",
          preuve="Sélection (25 plis) : ST1 0,5793 contre PIPE 0,5544 : +0,0249, IC95 [0,015 ; 0,036], Wilcoxon unilatéral (contre 0,02) p = 0,30, signes 13/12, permutation p = 0,20 ; ST2 +0,0220, IC95 [0,011 ; 0,034], p = 0,44 : les moyennes dépassent 0,02 mais la porte (Holm p < 0,05) n'est pas franchie et les bornes basses sont sous 0,02.  Fichiers : " + F, note="Même schéma que HY1 et HZ1 : un effet apparent de +0,02 à +0,03 dont la significativité contre le seuil n'est pas établie. Confirmation lancée par D39.")
    J.add("HQ4", "hypothese", last("HQ4")["titre"], last("HQ4")["texte"], justification="Clôture : la porte HQ2/HQ3 n'est pas franchie ; la confirmation est menée par D39 (HQ6, HQ7).", statut="non tranchée", preuve="Non testée au sens de la règle (porte fermée). Remplacée par HQ6 et HQ7 (D39).  Fichiers : " + F)
N = "Écrit le 2026-11-10 avant toute confirmation de la vague 8 (aucune donnée des répétitions 10 à 19 n'a été lue pour ces variantes)."
if not J.exists("D39"):
    J.add("D39", "decision", "Confirmer trois candidats de la vague 8 sur 50 plis neufs (seuil pratique 0,01)",
          "Candidats : G_C30_T1_a0.25 (meilleure configuration de la grille en sélection : +0,0152, IC95 [0,005 ; 0,026], poids 0,25 du prior observé dans la cible), ST1 (+0,0249) et ST2 (+0,0220). Confirmation : répétitions 10-19 (50 plis), conditions toutes et abs8, référence PIPE recalculée sur les mêmes plis. SEUIL : 0,01 (seuil pratique pour un ajout au pipeline décodé, comme HZ8) ; correction pour trois candidats : p < 0,05 / 3 = 0,0167. Précédents : D25, D31, D36. Le test v2 reste scellé.",
          justification="Les gains de sélection sont de l'ordre de +0,015 à +0,025 avec des bornes basses entre 0,005 et 0,015 : trop incertains pour trancher ; 50 plis neufs resserrent l'intervalle.", note=N)
for i, t, tx, j in (("HQ6", "Au moins un candidat améliore PIPE d'au moins 0,01 sur plis neufs", "Sur les 50 plis des répétitions 10-19, condition « toutes » : pour au moins un des trois candidats (G_C30_T1_a0.25, ST1, ST2), le gain de macro-F1 du palier A contre PIPE a une borne basse d'IC95 bootstrap ≥ 0,01 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,01) donnent p < 0,0167 ; réfutée si, pour les trois, la borne haute est < 0,01 ; sinon non tranchée. Si plusieurs candidats remplissent la règle, on retient celui dont le gain moyen est le plus grand ; si aucun, PIPE reste le décodage du pipeline gelé.", "Règle écrite avant le calcul (D39)."),
                    ("HQ7", "Le candidat retenu tient avec 8 classes absentes", "Pour le candidat retenu par HQ6, le gain contre PIPE dans la condition « abs8 » des répétitions 10-19 est > 0 avec borne basse d'IC95 > 0 (contrôle ; sans seuil de gain). Non évaluée si aucun candidat n'est retenu.", "Robustesse à l'absence de classes (HX6).")):
    if not J.exists(i): J.add(i, "hypothese", t, tx, justification=j, statut="préinscrite", note=N)
print("ok")
