"""Journal : verdicts HY1 et HY2 (D30) ; décision D31 (confirmer Q25b et M50 malgré la porte HY1 fermée) et hypothèses HY5 à HY7, préinscrites avant la confirmation. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W3a_all_units.csv ; W3a_tests.csv ; W3_selected.json"
if last("HY1")["statut"] == "préinscrite":
    J.add("HY1", "hypothese", last("HY1")["titre"], last("HY1")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D30).", statut="réfutée",
          preuve="Sélection (25 plis, répétitions 0-4) : gains minimaux (toutes, abs8) : Q25b +0,0476 ; M50 +0,0460 ; Q25 +0,0435 ; Z +0,0422 ; Q50b +0,0229 ; Q50 +0,0215. Mais Holm (6 variantes, Wilcoxon unilatéral contre le seuil 0,02) : en « abs8 » p Holm 0,077 (Q25b), 0,098 (M50, Q25) : la règle exige p Holm < 0,05 dans les deux conditions : AUCUNE variante ne passe la porte.  Fichiers : " + F,
          note="Le verdict est « réfutée » au sens strict de la porte. Les moyennes de gain sont pourtant ≥ 0,04 dans « toutes » et « abs8 » pour quatre variantes, et la borne basse de l'IC95 est ≥ 0,02 pour Q25b dans les deux conditions : la porte est défaillante par manque de puissance (25 plis, écart-type élevé en abs8), pas par absence d'effet apparent.")
    J.add("HY2", "hypothese", last("HY2")["titre"], last("HY2")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D30).", statut="non tranchée", preuve="Non évaluée : aucune variante n'a passé la porte HY1. À titre indicatif : gain en « toutes » de Z +0,0796 (99 % de celui d'A1), M50 +0,0598 (74 %), Q25b +0,0558 (69 %), Q25 +0,0553 (69 %).  Fichiers : " + F)
N = "Écrit le 2026-11-10 avant toute confirmation de la vague 3 (aucune donnée des répétitions 5 à 9 n'a été lue pour ces variantes)."
if not J.exists("D31"):
    J.add("D31", "decision", "Confirmer Q25b et M50 sur de nouveaux plis malgré la porte HY1 fermée",
          "Décision prise après lecture de la sélection (répétitions 0-4) : deux variantes sont retenues pour la confirmation, choisies par le MINIMUM des gains moyens dans les conditions « toutes » et « abs8 » parmi les mécanismes distincts : Q25b (présence jugée par la masse prédite, exposant 0,25) et M50 (cible mixte uniforme/EM). Confirmation sur les 25 plis des répétitions 5 à 9 (nouveaux plis), conditions toutes, abs8 (graine 1000·répétition + pli) et abs14 (graine 2000·répétition + pli), référence LR dans chaque condition. Précédent : D25 (confirmation lancée malgré une porte fermée, I6b). Le résultat sera lu avec la règle HY5 à HY7 ci-dessous, écrite avant tout calcul de l'étape b. Le test v2 reste scellé.",
          justification="La porte HY1 échoue par manque de puissance et non par effet nul : on tranche par une confirmation sur de nouveaux plis, comme demandé (« tout confirmer »).", note=N)
H = [("HY5", "Q25b et M50 gagnent dans les conditions « toutes » et « abs8 »", "Pour chaque candidat (Q25b, M50), sur les répétitions 5 à 9 : dans chacune des conditions « toutes » et « abs8 », le gain de macro-F1 du palier A contre LR a une borne basse d'IC95 bootstrap ≥ 0,02 ET Wilcoxon, signes et permutation (unilatéraux contre le seuil 0,02) donnent p < 0,025 (Bonferroni sur 2 candidats). Réfutée pour un candidat si, dans l'une des deux conditions, la borne haute est < 0,02 ; sinon non tranchée.", "Même règle que HF18 et HX6."),
     ("HY6", "Le gain reste positif dans la condition de stress « abs14 »", "Pour chaque candidat, sur les répétitions 5 à 9, condition « abs14 » : gain contre LR > 0 avec borne basse de l'IC95 > 0 (contrôle ; pas de seuil de gain).", "Test d'extrême : 14 classes sur 30 absentes."),
     ("HY7", "Choix de la configuration finale du décodage", "Si les deux candidats satisfont HY5, la configuration retenue est celle dont le MINIMUM des gains moyens sur les trois conditions est le plus grand ; si un seul satisfait HY5, c'est lui ; si aucun, on garde A1 avec la réserve de HX6 (non défendable seul).", "Règle de départage écrite avant le calcul.")]
for i, t, tx, j in H:
    if not J.exists(i): J.add(i, "hypothese", t, tx, justification=j, statut="préinscrite", note=N)
print("ok")
