"""Verdicts HN1 à HN3 (D44) et résultat RW12. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W12a_all_units.csv ; W12a_tests.csv ; W12_selected.json"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (D44).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HN1", "réfutée", "Sélection (25 plis, « toutes »), STK4 0,5940 : F4 0,5902 (−0,0038, IC95 [−0,012 ; 0,004], signes 6/19) ; F4s 0,5912 (−0,0028, [−0,008 ; 0,002], 1/24) ; F9 0,5837 (−0,0103, [−0,024 ; 0,003]) ; F9s 0,5839 (−0,0101, [−0,022 ; 0,002]) ; bornes hautes ≤ 0,004 < 0,01 ; Holm 1,0.", "L'optimisation de la macro-F1 hors-gabarit AMÉLIORE bien le critère sur lequel elle porte (F1 hors-gabarit +0,010 à +0,011) mais pas le score sur les plis de test : les prédictions hors-gabarit (modèles entraînés sur deux tiers des gabarits) ne sont pas celles des modèles complets ; les poids d'entropie croisée de STK4 sont déjà bons.")
verdict("HN2", "non tranchée", "Non évaluée : la porte HN1 n'est pas franchie (règle D44 : non évaluée si HN1 n'est pas franchie) ; aucun candidat n'a un gain de sélection dont la borne haute atteigne 0,01.")
verdict("HN3", "non tranchée", "Non évaluée (pas de confirmation) ; à titre indicatif en sélection, abs14 : F4 −0,0013 ; F4s +0,0008 ; F9 −0,0162 ; F9s −0,0171 contre STK4.")
if not J.exists("RW12"):
    J.add("RW12", "resultat", "Vague 12 : poids de la composition optimisés sur la macro-F1 décodée hors-gabarit", "Sélection (25 plis), macro-F1 du palier A, toutes / 8 absentes / 14 absentes : STK4 0,5940 / 0,6284 / 0,6262 ; F4 0,5902 / 0,6302 / 0,6249 ; F4s 0,5912 / 0,6294 / 0,6270 ; F9 0,5837 / 0,6228 / 0,6100 ; F9s 0,5839 / 0,6214 / 0,6091 ; PIPE 0,5544 / 0,5998 / 0,5796. F1 hors-gabarit (critère d'optimisation) : F4 0,4976 → 0,5079 ; F9 0,4973 → 0,5087.",
          justification="Aligner le critère d'apprentissage sur la mesure n'apporte rien sur les plis de test : le pipeline gelé reste STK4 + M50 avec poids d'entropie croisée. Les deux dernières vagues (11 et 12) closent la piste « composition apprise » : plus de têtes ou un autre critère ne font pas mieux que quatre têtes peu corrélées.", preuve=F)
print("ok")
