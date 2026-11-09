"""Verdicts HF10 à HF12 (règles préinscrites, D18) et résultat RI2. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I2_all_units.csv ; I2_resume.csv ; I2_tests.csv"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HF10", "réfutée", "Macro-F1 palier A, 25 plis : FT 0,489 contre V0 0,503, écart −0,014, IC95 [−0,027 ; −0,001] (exclut +0,02), p Holm 0,08 : pas de gain, tendance à la baisse.", "Les jetons typés (programme, champs, types, forme) n'ajoutent pas d'information utile aux classes par rapport aux mots ; la structure est déjà contenue dans le texte.")
verdict("HF11", "réfutée", "FTo (structure seule, sans mot) : macro-F1 0,265, IC95 [0,244 ; 0,285] : la borne haute reste sous le seuil 0,30 (60 % de V0).", "Constat à retenir : la structure seule est loin du hasard (1/30 soit 0,03) et retrouve la moitié du score de V0 (53 %), mais ne suffit pas. Écart FTo − V0 : −0,238, 0 pli sur 25 en faveur de FTo.")
verdict("HF12", "réfutée", "FTE contre V0 : macro-F1 des classes −0,017, IC95 [−0,028 ; −0,005], p Holm 0,029 : FTE fait légèrement PIRE que V0, la première condition (+0,02) échoue. Second volet : famille FTE − FT +0,008, IC95 [−0,002 ; 0,017], p = 0,16 : sous le seuil 0,01.", "Constat exploratoire (non préinscrit) : FT améliore le F1 de famille de +0,021 contre V0 (IC95 [0,006 ; 0,037], p = 0,026), moins qu'ENS (+0,029) ; les jetons typés n'ajoutent donc pas à ce que les lettres apportent déjà.")
if not J.exists("RI2"):
    J.add("RI2", "resultat", "Phase 2, itération I2 : champs typés (série actuelle ; I1 et I1b conservées)",
          "Macro-F1 palier A (25 plis) : V0 0,503 ; FT 0,489 ; FTE 0,487 ; FTo 0,265. F1 de famille : FTE 0,720 ; FT 0,712 ; V0 0,692 ; FTo 0,516. Aucun gain pour les classes ; la structure seule retient environ la moitié du score.",
          justification="Deuxième résultat négatif sur les classes : ni le vocabulaire (I1) ni la structure typée (I2) ne lèvent le plafond de 0,50 ; seule la composante lettres (ENS) améliore, et uniquement la famille (I1b).", preuve=F)
print("ok")
