"""Versionnage en ligne de commande.
  python scripts/version_file.py freeze CHEMIN VERSION_ACTUELLE        copie l'état courant dans versions/ (à faire AVANT de modifier)
  python scripts/version_file.py register ARTEFACT VERSION "ce que fait" "pourquoi remplace la précédente" [CHEMIN]   consigne la nouvelle version (APRÈS modification) et fige son fichier"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import tp2_versions as V
a = sys.argv[1:]
if a[:1] == ["freeze"] and len(a) == 3: print("copie :", V.freeze(ROOT / a[1], a[2]))
elif a[:1] == ["register"] and len(a) >= 5:
    f = V.freeze(ROOT / a[5], a[2]) if len(a) > 5 else None
    print("ajoutée" if V.register(a[1], a[2], a[3], a[4], fichier=str(f.relative_to(ROOT)) if f else None) else "déjà présente"); print(V.render())
else: raise SystemExit(__doc__)
