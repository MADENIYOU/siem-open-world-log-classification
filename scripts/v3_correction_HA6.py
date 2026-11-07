"""Version corrective de HA6 (une entrée n'est jamais modifiée : on ajoute une version). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
last = [e for e in J.entries() if e["id"] == "HA6"][-1]
if last["version"] == 2:
    J.add("HA6", "hypothese", last["titre"], last["texte"], justification=last["justification"], statut="réfutée", preuve=last["preuve"].replace("(en faveur des caractères, p non significatif au sens pratique)", "(en faveur des caractères ; statistiquement significatif, p < 1e-5, mais d'une taille négligeable devant l'écart-type entre plis de 0,002 à 0,06)"),
          note=last["note"] + "  Correction (version 3) : la formulation « p non significatif au sens pratique » de la version 2 pour P0 était ambiguë ; le verdict (réfutée) ne change pas, car l'hypothèse portait sur P2 et exigeait une supériorité significative.")
    print("version corrective ajoutée")
print(J.render())
