"""Verdicts HF1 à HF6 (règles préinscrites) et résultat RI1 (itération I1). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I1_all_units.csv ; I1_resume.csv ; I1_tests_pairs.csv"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HF1", "réfutée", "Écart de macro-F1 (palier A) contre le SVM mots (0,5032) : T2 −0,007 (IC95 [−0,023 ; 0,009], p Holm 0,31) ; T3 −0,031 (p Holm 0,002) ; T5 −0,086 (p Holm 3e-5). Aucun seuil ne gagne 0,02 ; T3 et T5 font significativement PIRE.", "L'hypothèse de travail de D16 (les mots propres à un seul gabarit nuisent) est fausse : ces mots aident aussi à reconnaître les classes dont les gabarits se ressemblent. Plus on restreint, plus la distance dans l'arbre augmente (0,81 → 0,92 → 0,98).")
verdict("HF2", "réfutée", "T3M moins T3 : −0,0013, IC95 [−0,007 ; 0,005], p = 0,92 : l'intervalle exclut +0,01.", "Le marqueur « valeur » unique n'apporte rien ; il ne rattrape pas la perte due à la restriction.")
verdict("HF3", "réfutée", "ENS moins SVM mots : −0,0010, IC95 [−0,012 ; 0,009], p = 0,65 : l'intervalle exclut +0,02.", "Constat exploratoire (non préinscrit, à confirmer) : ENS améliore le macro-F1 de FAMILLE (0,719 contre 0,692) et la distance dans l'arbre (0,787 contre 0,812) sans changer le macro-F1 des classes.")
verdict("HF4", "réfutée", "WGT moins SVM mots : −0,0043, IC95 [−0,008 ; −0,001], p = 0,045 : légèrement PIRE, loin de +0,02.")
verdict("HF5", "réfutée", "Aucune combinaison ne dépasse chacun de ses composants : C2 contre ENS −0,006 (p Holm 0,96), C3 contre ENS −0,009, C3 contre WGT −0,006, C1 contre WGT −0,030 (p Holm 0,002). C2 et C3 dépassent seulement T3 (+0,024 et +0,022), c'est-à-dire qu'elles réparent partiellement la perte de T3.", "Les trois combinaisons ont été calculées en même temps (C1, C2, C3) ; aucune n'a été choisie après coup.")
verdict("HF6", "réfutée", "Meilleur macro-F1 (palier A) : V0 0,5032 ; ENS 0,5022 ; WGT 0,4989. Cible 0,55 non atteinte ; aucune variante ne dépasse la baseline.", "Conclusion de I1 : la représentation à base de mots (vocabulaire, marqueurs, pondération, ajout des lettres) ne lève pas le plafond d'environ 0,50 ; la piste suivante doit changer la nature de l'information (champs typés, Transformer, fusion de scores) ou la tâche (niveau famille).")
if not J.exists("RI1"):
    J.add("RI1", "resultat", "Phase 2, itération I1 : représentation par support de gabarit (série actuelle ; baseline v3 conservée)",
          "Macro-F1 palier A (25 plis, P2) : V0 0,503 ; ENS 0,502 ; WGT 0,499 ; C2 0,496 ; T2 0,496 ; C3 0,493 ; T3 0,472 ; T3M 0,470 ; C1 0,469 ; T5 0,418. Aucune amélioration ; restreindre le vocabulaire dégrade. F1 de famille : ENS 0,719 (V0 0,692).",
          justification="Résultat négatif informatif : il réfute l'explication « les valeurs propres à un gabarit causent le plafond » et fait avancer vers les pistes suivantes. Conservé comme les autres.", preuve=F)
print("ok")
