"""Verdict HY9 (D33) et résultat RW3d. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/W3d_all_units.csv ; W3d_tests.csv ; artifacts/data (graines : répétitions 20 à 39)"
if last("HY9")["statut"] == "préinscrite":
    J.add("HY9", "hypothese", last("HY9")["titre"], last("HY9")["texte"], justification="Verdict établi avec la règle de décision préinscrite (D33).", statut="confirmée",
          preuve="100 nouveaux plis (répétitions 20-39). « toutes » : M50 0,5534 contre LR 0,5046 : +0,0488, IC95 [0,041 ; 0,057], Wilcoxon p < 1e-4, permutation p < 1e-4, signes 72/100 (p = 1e-5) : critères remplis. « abs8 » : M50 0,5646 contre LR 0,5292 : +0,0354, IC95 [0,026 ; 0,045] (borne basse ≥ 0,02), Wilcoxon p = 0,0063, permutation p = 0,0012, signes 59/100 (p unilatéral 0,0443) : critères remplis.  Fichiers : " + F,
          note="DÉCISION D33 APPLIQUÉE : M50 entre dans le pipeline gelé. Autres résultats de la même réplication : M50 contre A1 : toutes −0,0085 (IC95 [−0,015 ; −0,002]), abs8 +0,0104 (IC95 [−0,001 ; 0,022]), abs14 +0,0452 (IC95 [0,027 ; 0,063]) ; A1 contre LR : abs14 −0,0357 (IC95 [−0,059 ; −0,012]) : A1 nuit quand 14 classes sont absentes ; M50 contre LR en abs14 : +0,0095 (IC95 [−0,002 ; 0,022]) : pas de gain mais pas de dommage. Limite à écrire : décodage transductif (utilise la composition du lot de test sans étiquette).")
if not J.exists("RW3d"):
    J.add("RW3d", "resultat", "Réplication finale du décodage M50 (100 plis)",
          "Macro-F1 du palier A, 100 plis : toutes : LR 0,5046 ; A1 0,5619 ; M50 0,5534 ; 8 classes absentes : LR 0,5292 ; A1 0,5542 ; M50 0,5646 ; 14 classes absentes : LR 0,5800 ; A1 0,5443 ; M50 0,5895. Gain de M50 sur LR : +0,049 (toutes), +0,035 (abs8), +0,010 (abs14, non significatif).",
          justification="M50 est établi comme décodage robuste ; sur trois séries indépendantes de plis (25 + 25 + 50 puis 100) les gains vont de +0,035 à +0,06 quand au moins 8 classes sur 30 sont présentes.", preuve=F)
print("ok")
