"""Journal : décision D33 (réplication FINALE de M50 sur 100 nouveaux plis) et hypothèse HY9, préinscrites avant tout calcul. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
N = "Écrit le 2026-11-10 avant tout calcul de la réplication W3d (répétitions 20 à 39 : aucun résultat de ces plis n'a été lu)."
if not J.exists("D33"):
    J.add("D33", "decision", "Réplication finale de M50 sur 100 nouveaux plis (répétitions 20 à 39) : décision définitive",
          "HY8 est restée non tranchée (test des signes 31/50, p unilatéral 0,0595, contre 0,05) ; l'étudiant a choisi (2026-11-10) une dernière réplication préinscrite. 100 plis (répétitions 20 à 39, StratifiedGroupKFold par gabarit, graines 20 à 39), conditions toutes, abs8 (graine 1000·r + k), abs14 (2000·r + k), variantes M50, A1 (rapportée), LR (référence). Règle HY9 identique à HY8, avec n = 100. DÉCISION DÉFINITIVE : si HY9 est confirmée, M50 entre dans le pipeline gelé ; sinon (réfutée ou non tranchée) le décodage équilibré est abandonné du pipeline gelé, QUEL QUE SOIT le résultat des autres comparaisons ; aucune nouvelle réplication ne sera faite pour M50 (évite l'arrêt optionnel). Le test v2 reste scellé.",
          justification="Résoudre un non-tranché sans retoucher la règle, avec le double de plis ; une seule réplication supplémentaire annoncée d'avance, donc pas de répétition jusqu'à un résultat favorable.", note=N)
if not J.exists("HY9"):
    J.add("HY9", "hypothese", "M50 gagne contre LR dans les conditions « toutes » et « abs8 » (réplication finale, 100 plis)", "Sur les 100 plis des répétitions 20 à 39 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A de M50 contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) donnent p < 0,05 ; réfutée si, dans l'une des deux, la borne haute est < 0,02 ; sinon non tranchée.",
          justification="Même règle que HY8 (D33).", statut="préinscrite", note=N)
print("ok")
