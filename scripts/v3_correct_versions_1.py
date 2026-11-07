"""Correction de trois entrées de VERSIONS.md (R2, J1, AR1) : le commit avait été saisi ccd459e au lieu de ccc459e (faute de frappe), donc les copies figées n'avaient pas été créées. Idempotent."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import tp2_versions as V
for art, ver, path in [("src/tp2_runner.py (exécuteur reprenable)", "R2", "src/tp2_runner.py"), ("src/tp2_journal.py (journal append-only)", "J1", "src/tp2_journal.py"), ("scripts/archive_state.py (archives non écrasables)", "AR1", "scripts/archive_state.py")]:
    e = [x for x in V.entries() if x["artefact"] == art and x["version"] == ver][0]
    if e["commit"] != "ccc459e":
        f = V.freeze(ROOT / path, ver, commit="ccc459e"); V.correct(art, ver, "faute de frappe sur le hachage du commit : ccc459e et non ccd459e ; copie figée créée depuis le bon commit", commit="ccc459e", fichier=str(f.relative_to(ROOT)))
        print("corrigé :", ver, f.relative_to(ROOT))
for art, ver, fait, why, path in [
 ("src/tp2_runner.py (exécuteur reprenable)", "R3", "Comme R2, et copie automatique du code exact (script lancé et modules `src/tp2_*.py`) dans `versions/auto/` au premier calcul de chaque processus ; l'empreinte du code est enregistrée dans chaque résultat et dans le registre.", "L'étudiant a demandé que la perte d'une version de script (B1) ne se reproduise pas : la conservation ne doit plus dépendre d'un commit ni d'un oubli.", "src/tp2_runner.py"),
 ("src/tp2_versions.py (versionnage)", "V2", "Comme V1, avec refus d'un commit inexistant et fonction `correct` (correction ajoutée au journal, ancienne valeur conservée).", "Une faute de frappe sur un hachage de commit avait été enregistrée (ccd459e au lieu de ccc459e) : le registre doit refuser ce cas et permettre de corriger sans réécrire.", "src/tp2_versions.py"),
 ("scripts/check_versions.py (contrôle de conservation)", "CV1", "Vérifie que l'état courant de chaque script, module, générateur de présentation et notebook est conservé (copie ou commit) ; `--fix` fige dans `versions/auto/` ceux qui ne le sont pas.", None, "scripts/check_versions.py")]:
    f = V.freeze(ROOT / path, ver)
    if V.register(art, ver, fait, why, fichier=str(f.relative_to(ROOT)), date=None): print("ajoutée :", ver)
V.register("src/tp2_versions.py (versionnage)", "V1", "Registre append-only des versions (ce que fait la version, pourquoi elle remplace la précédente) et copies figées.", None, fichier="versions/src/tp2_versions__V1.py", commit="4126e97", date="2026-11-07 22:30")
print(V.render())
