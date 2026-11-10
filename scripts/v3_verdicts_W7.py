"""Clôture de la vague 7 : verdicts HL1 et HM1 (non tranchées, non terminées) et résultat RW7. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W7_all_units.csv ; W7_tests.csv ; W7_lpft/ (11 unités)"
INC = " INCIDENTS : le calcul s'est bloqué à trois reprises sur la 12e unité (découpe (3, 3), rotation 2) : 19h14, 20h50, 21h25 (processus à ≈ 2 % de processeur, 8 à 21 Go de mémoire, état « stuck »), malgré la libération de la mémoire entre phases (version 2 du script), le lancement par lots (version 3) et l'arrondi des longueurs de lot (module d'encodeur version 2) ; cause non établie (pilote graphique du Mac après quatre jours d'activité, ou unité particulière). Les unités 1 à 11 ont été calculées avec des longueurs de lot exactes ; aucune unité n'a été calculée avec les longueurs arrondies. Clôture décidée par l'étudiant le 2026-11-10."
if last("HL1")["statut"] == "préinscrite":
    J.add("HL1", "hypothese", last("HL1")["titre"], last("HL1")["texte"], justification="Clôture : la règle exigeait les 20 couples ; 11 seulement ont été calculés.", statut="non tranchée",
          preuve="NON TERMINÉE (11 couples sur 20). Estimation partielle : macro-F1 du palier A, LP-FT 0,4657 contre affinage complet T2 0,4702 : écart −0,0045, IC95 [−0,031 ; 0,029], Wilcoxon unilatéral (contre 0,02) p = 0,93, signes 3 en faveur / 8 contre, permutation p = 0,92 : aucun signe d'un avantage de 0,02.  Fichiers : " + F, note="Verdict « non tranchée, non terminée » : n'est ni confirmée ni réfutée au sens de la règle. Estimation partielle à lire comme exploratoire." + INC)
    J.add("HM1", "hypothese", last("HM1")["titre"], last("HM1")["texte"], justification="Clôture : la règle exigeait les 20 couples ; 11 seulement ont été calculés.", statut="non tranchée",
          preuve="NON TERMINÉE (11 couples sur 20). Estimation partielle : LP-FT adapté (MLM) 0,4848 contre LP-FT 0,4657 : +0,0191, IC95 [−0,011 ; 0,045], Wilcoxon unilatéral (contre 0,02) p = 0,62, signes 6/5, permutation p = 0,52 ; la perte de l'adaptation MLM passe de 4,87 à 1,54 (unité 1).  Fichiers : " + F, note="Verdict « non tranchée, non terminée ». L'intervalle contient 0 et 0,02." + INC)
if not J.exists("RW7"):
    J.add("RW7", "resultat", "Vague 7 : LP-FT et adaptation MLM de DistilBERT (clôturée, 11 couples sur 20)",
          "Protocole de T2 (140 logs par classe, découpes (1,1), (2,2) et début de (3,3)), macro-F1 du palier A sur 11 couples : TF-IDF 0,4965 ; LP-FT adapté (MLM) 0,4848 ; affinage complet T2 0,4702 ; LP-FT 0,4657. LP-FT contre affinage complet −0,0045 ; LP-FT adapté contre LP-FT +0,0191 ; LP-FT adapté contre TF-IDF −0,0117 (IC95 [−0,061 ; 0,036]).",
          justification="Aucun encodeur ne dépasse TF-IDF sur ces logs, même adapté : le pipeline reste TF-IDF + régression logistique + décodage M50. Résultat partiel, non concluant au sens des règles (couples manquants) mais cohérent avec RT2.", preuve=F)
print("ok")
