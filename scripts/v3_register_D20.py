"""Journal : décision D20 (règle de la phase 2 : itérer au maximum, test v2 seulement au maximum atteint). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
if not J.exists("D20"):
    J.add("D20", "decision", "Règle de la phase 2 : itérer au maximum avant d'ouvrir le jeu de test",
          "Demande de l'étudiant (2026-11-09) : en phase 2, on effectue autant d'itérations que possible pour augmenter la précision le plus possible ; c'est seulement quand le maximum de précision possible est atteint qu'on teste avec le jeu de test (test v2 scellé, une seule ouverture). Critère d'arrêt écrit : trois itérations consécutives sans gain significatif de macro-F1 des classes (palier A) sur de nouveaux plis, ou la veille de l'échéance (samedi 2026-11-14, ouverture le vendredi 2026-11-13 au plus tard pour laisser la rédaction). Procédure de chaque itération : hypothèses préinscrites ; sélection de la configuration sur les répétitions 0 à 4 du développement ; confirmation de la configuration retenue sur les répétitions 5 à 9 (nouveaux plis) ; jamais de sélection sur les données de confirmation ; le pipeline final est figé (version enregistrée) avant l'ouverture du test.",
          justification="Précise D6/R5 du plan (test ouvert une fois à la fin) : le moment de l'ouverture est le maximum atteint, pas une date fixe. Remplace le critère « fin de semaine ou 3 itérations sans gain » par le même critère rendu explicite.", note="Écrit le 2026-11-09.")
print("ok")
