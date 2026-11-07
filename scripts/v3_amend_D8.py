"""Amendement de D8 (nouvelle version, l'ancienne est conservée). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
last = [e for e in J.entries() if e["id"] == "D8"][-1]
if last["version"] == 1:
    J.add("D8", "decision", last["titre"], last["texte"] + " **Amendement :** pour DBSCAN et HDBSCAN, deux sorties sont comparées : « sans rejet » (le log reçoit la classe du groupe du plus proche point groupé, quelle que soit la distance) et « avec rejet » (rejet si la distance dépasse le seuil : eps pour DBSCAN, 95e centile des distances entre points groupés pour HDBSCAN). La comparaison de classification (HB6) porte sur la sortie sans rejet ; la sortie avec rejet est conservée et annonce le bloc C.",
          justification="Le test de fumée (répétition 0, pli 0, vu avant le calcul complet) a montré 95 % (DBSCAN) et 88 % (HDBSCAN) de rejets : les logs de nouveaux gabarits sont plus loin de tous les points d'entraînement que le seuil. Avec rejet seulement, ces méthodes ne classeraient presque rien et la comparaison avec le SVM n'aurait pas de sens ; le taux de rejet est lui-même un résultat. L'amendement est écrit avant le calcul complet.", preuve="scripts/v3_blockB.py (version B2)", note="Version 1 conservée : elle prévoyait seulement la sortie avec rejet.")
    print("D8 amendée")
print(J.render())
