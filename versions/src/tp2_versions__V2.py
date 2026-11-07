"""Versionnage des fichiers, scripts et documents : pour chaque artefact, chaque version dit CE QU'ELLE FAIT et POURQUOI elle remplace la précédente ;
la raison pour laquelle une version a été remplacée est celle de la version suivante. Journal append-only (artifacts/results/v3/versions.jsonl) rendu en VERSIONS.md.
Pratique à suivre : AVANT de modifier un fichier, `freeze` copie son état courant dans versions/ ; APRÈS, `register` consigne la nouvelle version et sa raison."""
import json, shutil, subprocess, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "artifacts" / "results" / "v3" / "versions.jsonl"


def raw_entries():
    return [json.loads(l) for l in FILE.read_text(encoding="utf-8").splitlines() if l.strip()] if FILE.exists() else []


def entries():
    """Versions avec les corrections appliquées ; chaque correction est ajoutée au journal (jamais de modification) et signalée dans la note."""
    base = [e for e in raw_entries() if not e.get("correction")]
    for c in (e for e in raw_entries() if e.get("correction")):
        for b in base:
            if b["artefact"] == c["artefact"] and b["version"] == c["version"]:
                old = {k: b.get(k) for k in c["champs"]}; b.update(c["champs"])
                b["note"] = (b.get("note", "") + f" Correction du {c['date']} ({c['raison']}) : ancienne valeur {old}.").strip()
    return base


def exists(artefact, version):
    return any(e["artefact"] == artefact and e["version"] == version for e in entries())


def commit_exists(commit):
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{commit}^{{commit}}"], capture_output=True).returncode == 0


def register(artefact, version, fait, pourquoi=None, fichier=None, commit=None, date=None, note=""):
    """pourquoi : raison pour laquelle cette version remplace la précédente (None pour la première version). Idempotent.
    Garde-fou : un commit indiqué doit exister (une faute de frappe sur un hachage est refusée au lieu d'être enregistrée)."""
    if commit and not commit_exists(commit): raise ValueError(f"commit inexistant : {commit}")
    if exists(artefact, version): return False
    FILE.parent.mkdir(parents=True, exist_ok=True)
    rec = {"artefact": artefact, "version": version, "date": date or time.strftime("%Y-%m-%d %H:%M"), "fait": fait, "pourquoi": pourquoi, "fichier": fichier, "commit": commit, "note": note}
    with open(FILE, "a", encoding="utf-8") as fh: fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return True


def correct(artefact, version, raison, **champs):
    """Corrige un champ d'une version déjà enregistrée SANS modifier le journal : ajoute une correction, appliquée à l'affichage avec l'ancienne valeur conservée."""
    if "commit" in champs and champs["commit"] and not commit_exists(champs["commit"]): raise ValueError("commit inexistant")
    with open(FILE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"correction": True, "artefact": artefact, "version": version, "date": time.strftime("%Y-%m-%d %H:%M"), "raison": raison, "champs": champs}, ensure_ascii=False) + "\n")


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
