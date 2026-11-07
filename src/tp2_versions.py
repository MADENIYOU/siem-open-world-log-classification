"""Versionnage des fichiers, scripts et documents : pour chaque artefact, chaque version dit CE QU'ELLE FAIT et POURQUOI elle remplace la précédente ;
la raison pour laquelle une version a été remplacée est celle de la version suivante. Journal append-only (artifacts/results/v3/versions.jsonl) rendu en VERSIONS.md.
Pratique à suivre : AVANT de modifier un fichier, `freeze` copie son état courant dans versions/ ; APRÈS, `register` consigne la nouvelle version et sa raison."""
import json, shutil, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "artifacts" / "results" / "v3" / "versions.jsonl"


def entries():
    return [json.loads(l) for l in FILE.read_text(encoding="utf-8").splitlines() if l.strip()] if FILE.exists() else []


def exists(artefact, version):
    return any(e["artefact"] == artefact and e["version"] == version for e in entries())


def register(artefact, version, fait, pourquoi=None, fichier=None, commit=None, date=None, note=""):
    """pourquoi : raison pour laquelle cette version remplace la précédente (None pour la première version). Idempotent."""
    if exists(artefact, version): return False
    FILE.parent.mkdir(parents=True, exist_ok=True)
    rec = {"artefact": artefact, "version": version, "date": date or time.strftime("%Y-%m-%d %H:%M"), "fait": fait, "pourquoi": pourquoi, "fichier": fichier, "commit": commit, "note": note}
    with open(FILE, "a", encoding="utf-8") as fh: fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return True


def freeze(path, version, commit=None):
    """Copie l'état d'un fichier dans versions/<dossier>/<nom>__<version>.<ext> (jamais d'écrasement). Avec `commit`, prend l'état de ce commit git."""
    path = Path(path); rel = path.relative_to(ROOT) if path.is_absolute() else path
    dest = ROOT / "versions" / rel.parent / f"{rel.stem}__{version}{rel.suffix}"
    if dest.exists(): return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    if commit:
        r = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:{rel.as_posix()}"], capture_output=True)
        if r.returncode != 0: return None
        dest.write_bytes(r.stdout)
    else:
        shutil.copy2(ROOT / rel, dest)
    return dest


def render(path=None):
    path = Path(path or ROOT / "VERSIONS.md"); by = {}
    for e in entries(): by.setdefault(e["artefact"], []).append(e)
    out = ["# Versions des fichiers, scripts et documents\n",
           "Généré à partir de `artifacts/results/v3/versions.jsonl` (append-only, ne pas modifier à la main). Pour chaque version : ce qu'elle fait, pourquoi elle remplace la précédente, pourquoi elle a été remplacée par la suivante, et où retrouver le fichier (copie dans `versions/` ou commit git). On ne supprime jamais une version.\n"]
    for art, vs in by.items():
        out.append(f"\n## {art}\n\n| Version | Date | Ce que fait cette version | Pourquoi elle remplace la précédente | Pourquoi elle a été remplacée | Où la retrouver |\n|---|---|---|---|---|---|\n")
        for i, v in enumerate(vs):
            nxt = vs[i + 1] if i + 1 < len(vs) else None
            rep = (nxt["pourquoi"] or "(non renseigné)") + f" (par {nxt['version']})" if nxt else "**version courante**"
            where = ", ".join(x for x in (f"`{v['fichier']}`" if v["fichier"] else None, f"commit {v['commit']}" if v["commit"] else None) if x) or "non conservée (voir note)"
            out.append(f"| **{v['version']}** | {v['date']} | {v['fait']} | {v['pourquoi'] or 'première version'} | {rep} | {where} |\n")
            if v["note"]: out.append(f"|  |  | *Note : {v['note']}* |  |  |  |\n")
    path.write_text("".join(out), encoding="utf-8"); return path
