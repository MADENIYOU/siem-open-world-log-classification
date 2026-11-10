"""Verdicts HQ1, HQ5, HQ6, HQ7 (D38, D39) et résultat RW8. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W8a_all_units.csv ; W8a_tests.csv ; W8a_grille.csv ; W8b_all_units.csv ; W8b_tests.csv ; W8_selected.json"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (D38, D39).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
CONF = "Confirmation (répétitions 10-19, 50 plis), condition « toutes », PIPE 0,5583 : G_C30_T1_a0.25 0,5620 (+0,0037, IC95 [−0,003 ; 0,011], Wilcoxon p = 0,97, signes 19/31 contre 0,01) ; ST1 0,5646 (+0,0063, IC95 [−0,001 ; 0,014], p = 0,82, signes 23/27) ; ST2 0,5612 (+0,0029, IC95 [−0,005 ; 0,011], p = 0,96, signes 19/31)."
verdict("HQ1", "non tranchée", "Candidat unique de réglage (G_C30_T1_a0.25, poids 0,25 du prior observé) : sélection +0,0152 (25 plis, IC95 [0,005 ; 0,026]). " + CONF.split(";")[0] + ". Seuil 0,01 : borne basse < 0,01 (non confirmée) et borne haute 0,0109 ≥ 0,01 (non réfutée).", "Gain de confirmation de +0,004 : pratiquement nul. Le gain de sélection (+0,015) s'est réduit des trois quarts sur plis neufs (retour vers la moyenne du maximum d'une grille de 36). Réglage par défaut conservé.")
verdict("HQ6", "non tranchée", CONF + " Aucun des trois candidats n'a une borne basse ≥ 0,01 ; aucun n'a une borne haute < 0,01 (0,011 ; 0,014 ; 0,011).", "Règle D39 : si aucun candidat n'est retenu, PIPE reste le décodage du pipeline gelé. Les gains de confirmation (+0,003 à +0,006) sont 3 à 4 fois plus petits que ceux de sélection (+0,015 à +0,025) : retour vers la moyenne.")
verdict("HQ5", "non tranchée", "Non évaluable : aucun candidat n'a été confirmé (HQ1 et HQ6 non tranchées).")
verdict("HQ7", "non tranchée", "Contrôle abs8 rapporté à titre indicatif : G_C30_T1_a0.25 −0,0093 (IC95 [−0,021 ; 0,003]) ; ST1 −0,0072 ([−0,017 ; 0,002]) ; ST2 −0,0191 ([−0,031 ; −0,008]) contre PIPE 0,5808 : aucun candidat ne tient avec 8 classes absentes ; non évaluable au sens de la règle (aucun candidat retenu).")
if not J.exists("RW8"):
    J.add("RW8", "resultat", "Vague 8 : réglage conscient du décodage, mots + lettres avant décodage, auto-apprentissage sur le lot décodé",
          "Sélection (25 plis, « toutes »), macro-F1 du palier A : PIPE 0,5544 ; ST1 0,5793 ; ST2 0,5764 ; meilleure configuration de grille (C = 30, T = 1, poids 0,25) 0,5695 ; ENSP30 0,5569 ; ENSP50 0,5561. Les cinq meilleures configurations de la grille ont toutes un poids 0,25 du prior observé. Confirmation (50 plis neufs) : PIPE 0,5583 ; grille +0,0037 ; ST1 +0,0063 ; ST2 +0,0029 ; avec 8 classes absentes : −0,007 à −0,019.",
          justification="Aucun levier de la vague 8 ne s'établit : les gains de sélection (+0,015 à +0,025) se réduisent à +0,003 à +0,006 sur plis neufs. Le pipeline gelé reste TF-IDF mots → régression logistique C = 10 → décodage M50 (poids 0,5, température 1). Illustre le biais du maximum d'une grille et de la sélection sur 25 plis.", preuve=F)
print("ok")
