"""Journal : décision D17 (confirmation du constat exploratoire d'I1 sur de nouveaux découpages) et hypothèses HF7 à HF9, préinscrites avant tout calcul. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
N = "Écrit le 2026-11-09 avant tout calcul de la confirmation I1b."
if not J.exists("D17"):
    J.add("D17", "decision", "Confirmation I1b : mots + lettres (ENS) améliore-t-il la famille ?",
          "Constat exploratoire d'I1 (vu APRÈS les chiffres, donc non confirmatoire) : ENS (somme des marges SVM mots et SVM caractères) a un macro-F1 de famille de 0,719 contre 0,692 (+0,028, Wilcoxon p = 0,0006, 19 plis sur 25) et une distance dans l'arbre de 0,787 contre 0,812 (−0,025, p = 0,012), sans changer le macro-F1 des classes (−0,001). Pour confirmer : 25 NOUVEAUX plis (répétitions 5 à 9, mêmes StratifiedGroupKFold par gabarit avec les graines 5 à 9), seules les deux variantes V0 et ENS, mêmes réglages, même développement de SIEVE_00 ; le test v2 reste scellé. Limite écrite : ce sont les mêmes gabarits répartis autrement, donc la confirmation vaut pour le hasard du découpage, pas pour de nouveaux gabarits ; la confirmation sur de nouveaux gabarits se fera sur le test v2 (une seule ouverture, à la fin).",
          justification="Demande de l'étudiant (2026-11-09) : confirmer maintenant le constat exploratoire. Règle R2 : une hypothèse vue dans les données ne se confirme pas avec les mêmes données ; on préinscrit donc la règle puis on la teste sur des découpages non utilisés.", note=N)
H = [("HF7", "Mots + lettres améliore le F1 de famille", "Sur les 25 nouveaux plis, le macro-F1 de famille de ENS dépasse celui de V0 (SVM mots) d'au moins 0,01 (Wilcoxon apparié unilatéral p < 0,05). Réfutée si l'IC95 bootstrap de l'écart exclut +0,01 ; sinon non tranchée.", "Les caractères voient la forme des mots, utile pour rapprocher des gabarits d'une même famille."),
     ("HF8", "Mots + lettres rapproche les erreurs dans l'arbre", "Sur les 25 nouveaux plis, la distance moyenne dans l'arbre de ENS est inférieure à celle de V0 d'au moins 0,01 (Wilcoxon apparié, p < 0,05).", "Même mécanisme que HF7, mesure de la gravité des erreurs."),
     ("HF9", "Mots + lettres ne dégrade pas le macro-F1 des classes", "Sur les 25 nouveaux plis, l'écart de macro-F1 (palier A) ENS − V0 est supérieur à −0,01 : l'IC95 bootstrap de l'écart est entièrement au-dessus de −0,01 (équivalence unilatérale).", "Condition pour recommander ENS : le gain de famille ne doit pas se payer sur les classes.")]
for i, t, tx, j in H:
    if not J.exists(i): J.add(i, "hypothese", t, tx, justification=j, statut="préinscrite", note=N)
print("ok")
