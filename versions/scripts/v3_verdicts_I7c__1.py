"""Verdicts HI6b et HI7b (D25) et résultat RI7c ; nouvelles entrées pour HI6 et HI7 (les entrées « non tranchée » sont conservées). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I7c_all_units.csv ; I7c_resume.csv ; I7c_tests.csv ; artifacts/data/rotations_v2_I7c.json"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (D25).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HI6b", "confirmée", "75 unités (jeux D, E, F × répétitions 10 à 14) : AUROC C64_fam_negent 0,6690 contre msp (C = 4) 0,6271 : +0,0419, IC95 [0,0324 ; 0,0512] (borne basse ≥ 0,03) ; Wilcoxon unilatéral (écart > 0,03) p = 0,0095 ; permutation p = 0,0087 ; test des signes unilatéral p = 0,032 (46 unités en faveur, 29 contre ; le fichier I7c_tests.csv rapporte le p bilatéral 0,064, la règle exige l'unilatéral). Par jeu : +0,040 ; +0,042 ; +0,044.", "Résultat conforme à la sélection (+0,041) : l'effet de +0,04 est stable sur 3 jeux de rotations et 75 unités. Le test des signes est le plus fragile (p unilatéral 0,032) ; aucune des trois rotations de l'ensemble C de I7b n'avait donné ce résultat (+0,0175, 25 unités, intervalle trop large). Précision : tous les scores de famille donnent +0,035 à +0,043 ; ce n'est pas C64_fam_negent en particulier qui gagne.")
verdict("HI7b", "réfutée", "Baisse du FPR@95 (msp C = 4 moins C64_fam_negent) : 0,0204, IC95 [0,0069 ; 0,0334] (borne haute < 0,05) ; Wilcoxon p = 1,0 ; signes 25 en faveur / 50 contre.", "La confiance de famille améliore l'AUROC mais pas assez le FPR@95 : à 95 % de connus conservés, 85 % des inconnus restent acceptés (0,874 pour le msp, 0,854 pour la famille).")
for old, new, st in (("HI6", "HI6b", "confirmée"), ("HI7", "HI7b", "réfutée")):
    if last(old)["statut"] == "non tranchée" and "I7c" not in (last(old).get("note") or ""):
        J.add(old, "hypothese", last(old)["titre"], last(old)["texte"], justification="Tranchée par la réplication préinscrite D25 (%s, 75 unités) ; l'entrée « non tranchée » précédente est conservée." % new, statut=st, preuve="Voir %s." % new, note="Source : I7c.")
if not J.exists("RI7c"):
    J.add("RI7c", "resultat", "Réplication I7c : rejet d'inconnus sur 75 unités de nouvelles rotations (I4, I7a, I7b conservées)",
          "75 unités (3 jeux de 5 rotations × 5 répétitions) : AUROC msp (C = 4) 0,627 ; scores de famille 0,666 à 0,670 (C16_fam_msp 0,670 ; C64_fam_negent 0,669) ; FPR@95 : msp 0,874 ; famille 0,854 à 0,869. Gain d'AUROC de la famille : +0,04 (stable par jeu : +0,040 ; +0,042 ; +0,044) ; baisse du FPR@95 : 0,02.",
          justification="Résultat final sur le rejet d'inconnus : la confiance de famille est un gain réel et stable d'environ +0,04 d'AUROC sur le MSP (confirmé sur 75 unités de rotations jamais vues), mais le FPR@95 reste voisin de 0,85 et l'AUROC absolu (0,67) est loin du critère S2 (0,80).", preuve=F)
print("ok")
