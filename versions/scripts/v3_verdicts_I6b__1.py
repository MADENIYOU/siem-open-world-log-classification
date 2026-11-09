"""Verdict HF18 après lancement d'I6b (D25). Nouvelle entrée du journal : l'ancienne (« non tranchée », non testée) est conservée. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I6b_all_units.csv ; I6b_tests.csv ; I6_selected.json"
if last("HF18")["statut"] == "non tranchée" and "I6b" not in (last("HF18").get("preuve") or ""):
    J.add("HF18", "hypothese", last("HF18")["titre"], last("HF18")["texte"], justification="Verdict établi avec la règle de décision préinscrite, après lancement de la confirmation I6b demandé par l'étudiant (D25) ; remplace l'entrée « non testée ».", statut="réfutée",
          preuve="25 plis (répétitions 5 à 9) : W1_lr30 0,5105 contre V0 0,5132 : écart −0,0027, IC95 [−0,016 ; 0,011] (borne haute < 0,02), Wilcoxon p = 0,998, signes 5 en faveur / 20 contre (p bilatéral 0,004), permutation p = 0,999. Famille : F1 +0,0075 (IC95 [−0,015 ; 0,030]), distance dans l'arbre −0,008 (non significatifs).  Fichiers : " + F,
          note="Confirmation lancée alors que la porte HF17 était fermée (+0,0085 en développement) : le résultat est conforme à ce que la porte laissait prévoir. La configuration choisie par maximum de grille ne tient pas sur de nouveaux plis (retour vers la moyenne) : elle est même moins bonne que V0 dans 20 plis sur 25.")
print("ok")
