"""Archive un état du projet SANS JAMAIS écraser une archive existante (règle : on garde toujours le précédent et l'actuel).
Usage : python scripts/archive_state.py ÉTIQUETTE [chemin ...]   (sans chemin : notebook, résultats, figures, présentation, README, plans).
Crée archive/ÉTIQUETTE/ avec une copie des fichiers et MANIFEST.json (empreintes sha256, taille, date, commit). Refuse si l'étiquette existe."""
import hashlib, json, shutil, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
DEFAULT = ["TP2_logs_hierarchique_monde_ouvert.ipynb", "artifacts/results", "artifacts/figures", "presentation/Soutenance_SIEM_monde_ouvert.pptx", "presentation/build_deck.js", "presentation/script_oral.md", "README.md", "PLAN_V3.md", "REGISTRE_V3.md"]
SKIP = {"v3", "node_modules", ".venv", "_render", "__pycache__"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def snapshot(label, paths=None):
    dest = ROOT / "archive" / label
    if dest.exists(): raise SystemExit(f"archive/{label} existe déjà : on n'écrase jamais une archive (choisir une autre étiquette)")
    files = []
    for rel in (paths or DEFAULT):
        src = ROOT / rel
        if not src.exists(): continue
        items = [src] if src.is_file() else [f for f in src.rglob("*") if f.is_file() and not (set(f.relative_to(src).parts) & SKIP)]
        for f in items:
            target = dest / f.relative_to(ROOT); target.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(f, target)
            files.append({"path": str(f.relative_to(ROOT)), "sha256": sha(f), "bytes": f.stat().st_size})
    try: commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception: commit = "inconnu"
    (dest / "MANIFEST.json").write_text(json.dumps({"label": label, "date": time.strftime("%Y-%m-%d %H:%M:%S"), "commit": commit, "files": files}, ensure_ascii=False, indent=1))
    return dest, len(files)


if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    d, n = snapshot(sys.argv[1], sys.argv[2:] or None); print(f"archivé : {n} fichiers dans {d.relative_to(ROOT)}")
