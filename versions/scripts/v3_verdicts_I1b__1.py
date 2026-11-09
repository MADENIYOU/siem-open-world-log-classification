"""Verdicts HF7 à HF9 (règles préinscrites, D17) et résultat RI1b. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I1b_all_units.csv ; I1b_tests.csv"
LIM = " Limite : mêmes gabarits que le développement d'I1, répartis autrement ; la confirmation sur de nouveaux gabarits revient au test v2."
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note + LIM)
verdict("HF7", "confirmée", "25 nouveaux plis : macro-F1 de famille ENS 0,720 contre V0 0,690, gain +0,029, IC95 [0,015 ; 0,048] (borne basse au-dessus du seuil 0,01), Wilcoxon unilatéral p = 2e-5, 22 plis sur 25 en faveur.", "Reproduit le constat exploratoire d'I1 (+0,028) : l'effet est stable.")
verdict("HF8", "confirmée", "Distance moyenne dans l'arbre : ENS 0,781 contre V0 0,808, gain +0,028, IC95 [0,013 ; 0,044], p unilatéral 0,0019, 20 plis sur 25 en faveur.")
verdict("HF9", "non tranchée", "Écart de macro-F1 des classes ENS − V0 : −0,0011, IC95 [−0,0109 ; 0,0091] ; la borne basse dépasse de 0,0009 le seuil −0,01 : l'équivalence unilatérale n'est pas établie au sens strict de la règle ; 12 plis sur 25 en faveur d'ENS.", "L'écart moyen est quasi nul (0,001) ; la règle d'équivalence exigeait un intervalle entièrement au-dessus de −0,01 et l'intervalle dépasse ce seuil de très peu. Pas de dégradation visible, mais pas de preuve d'absence de dégradation. Ni les données d'I1 (−0,001, IC [−0,012 ; 0,009]) ni celles d'I1b ne la permettent seules.")
if not J.exists("RI1b"):
    J.add("RI1b", "resultat", "Confirmation I1b : mots + lettres (ENS) contre mots seuls (V0)",
          "Constat exploratoire d'I1 (25 plis) : famille +0,028, distance −0,025, classes −0,001. Confirmation (25 nouveaux plis) : famille +0,029 (IC95 [0,015 ; 0,048]), distance −0,028, classes −0,001 (IC95 [−0,011 ; 0,009]). Les deux séries sont conservées.",
          justification="L'effet exploratoire se reproduit presque à l'identique sur de nouveaux découpages : il est réel au sens du hasard du découpage. Il porte sur la FAMILLE (confusions moins graves), pas sur les classes.", preuve=F)
print("ok")
