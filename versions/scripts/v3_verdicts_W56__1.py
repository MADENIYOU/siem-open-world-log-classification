"""Verdicts HO1-HO3 (vague 5) et HR1-HR4 (vague 6), résultats RW5 et RW6. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F5 = "artifacts/results/v3/W5a_all_units.csv ; W5a_tests.csv ; W5_selected.json"; F6 = "artifacts/results/v3/W6a_all_units.csv ; W6a_tests.csv ; W6_selected.json ; emb_distilbert_frozen/index.json"
def verdict(i, statut, preuve, F, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (D37).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HO1", "réfutée", "Ensemble B (25 unités, rotations 20261110 × répétitions 0-4), AUROC d'inconnu contre FAM (0,6483) : FAMQ 0,6464 (−0,0019, IC95 [−0,011 ; 0,007]) ; FAMD 0,6445 (−0,0038, [−0,013 ; 0,005]) ; MSPQ 0,6250 (−0,0234, [−0,034 ; −0,013]) ; bornes hautes < 0,02.", F5, "Le décodage M50 n'améliore pas la détection d'inconnus par la famille ; sur le MSP il le dégrade (la cible équilibrée absorbe des logs inconnus dans des classes connues).")
verdict("HO2", "non tranchée", "FPR@95 contre FAM (0,8731) : baisse de FAMQ −0,0084 ([−0,036 ; 0,019]), FAMD +0,0068 ([−0,013 ; 0,027]), MSPQ +0,0181 ([−0,005 ; 0,041]) ; aucune n'atteint 0,03 avec Holm ; la borne haute de MSPQ (0,041) ne permet pas d'exclure 0,03.", F5, "Gain de FPR@95 de MSPQ non exclu mais accompagné d'une AUROC plus basse de 0,023 : sans intérêt pratique.")
verdict("HO3", "non tranchée", "Non testée : la porte HO1/HO2 est restée fermée ; la confirmation sur l'ensemble C n'a pas été lancée.", F5)
verdict("HR1", "réfutée", "Sélection (25 plis) : V-REx contre ERM (0,4872) : VR1 −0,0043 (IC95 [−0,0086 ; −0,0006]) ; VR5 −0,0014 ([−0,009 ; 0,007]) ; VR20 +0,0102 ([0,0006 ; 0,0199]) ; bornes hautes < 0,02 ; Holm 1,0.", F6, "La pénalité de variance du risque entre gabarits n'apporte rien : le meilleur λ gagne 0,01 sur l'ERM, sous le seuil.")
verdict("HR2", "réfutée", "Mode M50 contre ERM + M50 (0,5507) : VR1 +0,0015 (IC95 [−0,003 ; 0,006]) ; VR5 −0,0044 ; VR20 −0,0056 ; bornes hautes < 0,02.", F6)
verdict("HR3", "réfutée", "Embeddings gelés DistilBERT, brut, contre LR (0,4947) : E1 (embeddings seuls) 0,4515 (−0,0432, IC95 [−0,062 ; −0,025]) ; E2 (moyenne géométrique mots + embeddings) 0,4801 (−0,0146, [−0,028 ; −0,0007]) ; E3 (concaténation) 0,4628 (−0,0319, [−0,044 ; −0,020]) : tous PIRES que LR.", F6, "Les embeddings gelés d'un modèle de langue anglais courant n'apportent pas de sémantique utile ici et diluent le signal lexical (cohérent avec v1 5.8b : 0,4547 contre 0,4745).")
verdict("HR4", "réfutée", "Mode M50 contre LR + M50 (0,5544) : E1 0,4643 (−0,0901) ; E2 0,5056 (−0,0488) ; E3 0,4872 (−0,0671) ; tous pires.", F6)
if not J.exists("RW5"):
    J.add("RW5", "resultat", "Vague 5 : détection d'inconnus par la famille avec décodage M50 (I7 conservée)", "Ensemble B (25 unités) : AUROC FAM 0,6483 ; FAMQ 0,6464 ; FAMD 0,6445 ; MSPQ 0,6250 ; MSP 0,6081. FPR@95 : FAM 0,8731 ; FAMQ 0,8816 ; FAMD 0,8663 ; MSPQ 0,8550 ; MSP 0,8854.",
          justification="Le décodage équilibré, utile pour la classification fermée, ne l'est pas pour la détection d'inconnus : le pipeline gelé garde la confiance de famille brute pour le rejet (+0,04 d'AUROC sur le MSP, HI6b), sans décodage.", preuve=F5)
if not J.exists("RW6"):
    J.add("RW6", "resultat", "Vague 6 : V-REx et embeddings gelés (brut / M50)", "Macro-F1 du palier A (25 plis), brut / M50 : LR 0,4947 / 0,5544 ; ERM 0,4872 / 0,5507 ; VR1 0,4829 / 0,5522 ; VR5 0,4858 / 0,5462 ; VR20 0,4974 / 0,5451 ; E1 0,4515 / 0,4643 ; E2 0,4801 / 0,5056 ; E3 0,4628 / 0,4872.",
          justification="Ni l'invariance de risque entre gabarits ni la sémantique d'un encodeur gelé ne relèvent le score : deux leviers de plus fermés, avec des résultats négatifs informatifs.", preuve=F6)
print("ok")
