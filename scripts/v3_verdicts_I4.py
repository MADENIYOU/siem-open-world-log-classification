"""Verdicts HI1 à HI4 (règles préinscrites, D19) et résultat RI4. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I4_all_units.csv ; I4_resume.csv ; I4_HI1.csv ; I4_HI2.csv ; I4_HI3.csv ; artifacts/data/rotations_v2_I4.json"
LIM = " Limite : mêmes gabarits que le développement, nouvelles rotations et nouveaux plis ; nouveaux gabarits = test v2. Une unité (rotation 1, répétition 5, pli 0) avait été calculée au test de fumée ; le verdict repose sur les 25 unités (rotation, répétition) complètes."
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note + LIM)
verdict("HI1", "confirmée", "AUROC d'inconnu moyen (25 unités) : fam_msp 0,693 ; msp 0,665 ; energy 0,670 ; hier_msp 0,664. Gains de fam_msp : +0,028 contre msp (IC95 [0,008 ; 0,048], p Holm 0,007, 16 unités sur 25), +0,023 contre energy (IC95 [0,002 ; 0,043], p Holm 0,020), +0,029 contre hier_msp (IC95 [0,013 ; 0,045], p Holm 0,002).", "Confirmée au sens de la règle écrite (gain moyen ≥ 0,02 et p Holm < 0,05), mais avec réserve : la borne basse de chaque IC95 est sous 0,02 (0,008 contre msp), l'effet est donc positif de façon fiable mais sa taille (0,02 à 0,03) n'est pas établie précisément. Il reproduit l'ordre du bloc C (famille 0,666 contre MSP 0,623) avec un gain plus petit (0,028 contre 0,043).")
verdict("HI2", "réfutée", "Rotations où fam_msp dépasse msp : 3 sur 5 (rotation 1 : 0,658 contre 0,580 ; rotation 3 : 0,740 contre 0,685 ; rotation 4 : 0,666 contre 0,598) ; rotations 2 (0,712 contre 0,737) et 5 (0,689 contre 0,726) en défaveur ; règle : au moins 4 sur 5.", "L'avantage moyen vient de trois rotations ; il n'est pas général. Cohérent avec HC8 (forte variabilité entre rotations : AUROC du msp de 0,58 à 0,74 selon la rotation).")
verdict("HI3", "réfutée", "FPR@95 moyen : msp 0,851 ; fam_msp 0,859 : baisse −0,008 (IC95 [−0,045 ; 0,024], p = 0,85) ; la règle exigeait −0,03.", "Le gain d'AUROC ne se traduit pas à l'usage : à 95 % de connus conservés, 85 % des inconnus sont acceptés avec tous les scores.")
verdict("HI4", "confirmée", "AUROC moyen de fam_msp : 0,693, IC95 [0,680 ; 0,706], entièrement sous 0,80.", "Le détecteur d'inconnus reste insuffisant au sens du critère S2, y compris le meilleur.")
if not J.exists("RI4"):
    J.add("RI4", "resultat", "Itération I4 : rejet par confiance de famille sur nouvelles rotations (bloc C conservé)",
          "Nouvelles rotations × nouveaux plis (25 unités) : AUROC fam_msp 0,693 ; maxlogit 0,671 ; energy 0,670 ; msp 0,665 ; hier_msp 0,664. FPR@95 : 0,85 à 0,87 pour tous. Bloc C (v1 rotations, 125 unités) : fam_msp 0,666 ; énergie 0,639 ; msp 0,623. Les deux séries sont conservées.",
          justification="La confiance de famille reste le meilleur score dans les deux séries (+0,03 à +0,04 d'AUROC sur le MSP), mais l'avantage est inégal selon les rotations (3 sur 5) et n'améliore pas le FPR@95 : c'est une amélioration modeste, pas une solution. HD7 ajoute qu'elle est plus fragile sous attaque.", preuve=F)
print("ok")
