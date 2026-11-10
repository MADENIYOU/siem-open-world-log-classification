"""Verdicts HZ7, HZ8 (D36) et résultat RW4. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W4b_all_units.csv ; W4b_tests.csv ; W4b_HZ7_HZ8.csv"
if last("HZ7")["statut"] == "préinscrite":
    J.add("HZ7", "hypothese", last("HZ7")["titre"], last("HZ7")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D36).", statut="non tranchée",
          preuve="50 nouveaux plis (répétitions 10-19), condition « toutes », mode brut : AXE05 0,5386 contre LR 0,5033 : +0,0353, IC95 [0,026 ; 0,045] (borne basse ≥ 0,02 : rempli), Wilcoxon unilatéral p = 0,0077 (rempli), permutation p = 0,0014 (rempli), test des signes : 31 plis sur 50 au-dessus de 0,02, p unilatéral = 0,0595 (NON rempli de peu).  Fichiers : " + F,
          note="Même configuration que HY8 (31/50, 0,0595). Un seul des quatre critères échoue, le plus faible : l'effet est positif mais hétérogène d'un pli à l'autre.")
    J.add("HZ8", "hypothese", last("HZ8")["titre"], last("HZ8")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D36).", statut="non tranchée",
          preuve="Mêmes plis, mode M50, condition « toutes » : AXE05 + M50 0,5765 contre LR + M50 0,5583 : +0,0182, IC95 [0,0105 ; 0,026] (borne basse ≥ 0,01 : rempli), Wilcoxon p = 0,0128 (rempli), permutation p = 0,0222 (rempli), signes 31/50 au-dessus de 0,01, p unilatéral 0,0595 (NON rempli de peu).  Fichiers : " + F,
          note="DÉCISION D36 APPLIQUÉE : HZ8 n'est pas confirmée, le pipeline gelé reste LR + décodage M50 (AXE05 n'y entre pas). En abs8 en mode M50 : +0,002, IC95 [−0,010 ; 0,014] : aucun gain avec 8 classes absentes. Mention exploratoire pour l'article : le produit d'experts objet × action améliore la classification brute (+0,035), mais ce gain est en grande partie absorbé par le décodage équilibré (+0,018) et n'est pas établi au-delà.")
if not J.exists("RW4"):
    J.add("RW4", "resultat", "Vague 4 : produit d'experts objet × action (F7), bagging par gabarits (F20), pondération des gabarits difficiles (F10)",
          "Sélection (25 plis, répétitions 0-4), condition « toutes », macro-F1 du palier A, brut / avec M50 : LR 0,4947 / 0,5544 ; AXE05 0,5330 / 0,5750 ; AXE1 0,5233 / 0,5691 ; AXE0 0,5167 / 0,5520 ; DRO2 0,4957 / 0,5600 ; BAG10 0,4761 / 0,5405 ; DRO1 0,005 (dégénéré). Confirmation d'AXE05 (50 plis, répétitions 10-19) : brut 0,5386 contre LR 0,5033 (+0,035) ; avec M50 0,5765 contre LR + M50 0,5583 (+0,018) ; 8 classes absentes avec M50 : 0,5827 contre 0,5808 (+0,002).",
          justification="Aucune de ces formules n'est établie au-delà du pipeline gelé (LR + M50). F7 est la seule à montrer un gain net en brut, mais son mécanisme annoncé (aider les classes rares) n'est pas observé (HZ6) et le décodage en absorbe plus de la moitié. F20 et F10 n'apportent rien (la pondération non bornée est inutilisable).", preuve=F)
print("ok")
