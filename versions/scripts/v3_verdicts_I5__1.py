"""Verdicts HF13, HF14 (D21) et résultat RI5. Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/I5a_resume.csv ; I5_selected.json"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HF14", "réfutée", "Répétitions 0 à 4 (25 plis) : la meilleure des 3 × 3 × 2 × 3 + références configurations (somme_mC3_l46C1_w0.5 : mots C = 3 + lettres 4-6 C = 1 poids 0,5) a un macro-F1 de 0,5106 contre 0,5032 pour V0 : gain +0,0074, sous le seuil de 0,02 ; 17 plis sur 25 en faveur. Ce gain est le MAXIMUM d'une grille de plus de 70 configurations, donc biaisé vers le haut.", "Aucune configuration ne justifie la confirmation. Les réglages par défaut (C = 1, n-grammes 3-5, poids 1 : 0,5022) sont à moins de 0,01 du meilleur : le plafond de 0,50 n'est pas un problème de réglage.")
verdict("HF13", "non tranchée", "Non testée : la porte HF14 est restée fermée, la confirmation I5b sur les répétitions 5 à 9 n'a pas été lancée (règle D21).", "À ne pas lire comme réfutée ni confirmée : aucune donnée de confirmation n'a été consommée.")
if not J.exists("RI5"):
    J.add("RI5", "resultat", "Itération I5 : réglage des modèles linéaires mots + lettres",
          "Meilleure configuration sur 25 plis (répétitions 0 à 4) : 0,5106 contre V0 0,5032 (+0,007) et contre la somme par défaut 0,5022 ; F1 de famille jusqu'à 0,722. Confirmation non lancée (porte fermée).",
          justification="Troisième itération consécutive sans gain de macro-F1 des classes (I1, I2, I5) : les modèles linéaires sur TF-IDF mots et lettres sont au plafond d'environ 0,50-0,51 ; critère d'arrêt D20 atteint POUR CETTE FAMILLE de modèles. Reste à essayer ce qui change la nature de l'information : le Transformer (I3).", preuve=F)
print("ok")
