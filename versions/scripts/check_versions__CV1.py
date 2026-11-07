"""Vérifie qu'aucune version de code ne peut se perdre : pour chaque script, module, générateur de présentation et notebook, l'état courant est-il conservé
(copie dans versions/ ou versions/auto/, ou identique au dernier commit git) ? Avec --fix, fige dans versions/auto les états non conservés.
À lancer avant de commiter et en fin de session."""
import hashlib, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILES = sorted((ROOT / "src").glob("tp2_*.py")) + sorted((ROOT / "scripts").glob("*.py")) + [ROOT / "presentation" / "build_deck.js", ROOT / "presentation" / "build.sh", ROOT / "TP2_logs_hierarchique_monde_ouvert.ipynb"]
def sha(b): return hashlib.sha256(b).hexdigest()[:12]
bad = 0
for f in FILES:
    if not f.exists(): continue
    data = f.read_bytes(); s = sha(data); rel = f.relative_to(ROOT)
    git = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel.as_posix()}"], capture_output=True).stdout
    kept = (ROOT / "versions" / "auto" / f"{f.stem}__{s}{f.suffix}").exists() or (git and sha(git) == s) or any(sha(p.read_bytes()) == s for p in (ROOT / "versions").rglob(f"{f.stem}__*{f.suffix}"))
    if not kept:
        bad += 1; print("NON CONSERVÉ :", rel)
        if "--fix" in sys.argv:
            d = ROOT / "versions" / "auto" / f"{f.stem}__{s}{f.suffix}"; d.parent.mkdir(parents=True, exist_ok=True); d.write_bytes(data); print("   figé dans", d.relative_to(ROOT))
print("tout est conservé" if bad == 0 else f"{bad} fichier(s) non conservé(s)"); sys.exit(0 if bad == 0 or "--fix" in sys.argv else 1)
