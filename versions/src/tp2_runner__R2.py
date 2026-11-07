"""Exécuteur reprenable et traçable (protocole v3).

Une expérience = une UNITÉ décrite par une configuration (dictionnaire). Son empreinte (hash de la configuration + version du code déclarée)
donne le nom du fichier de résultat. Si ce fichier existe, on le recharge ; sinon on calcule, on écrit le résultat de façon atomique et on
ajoute une ligne au registre (append-only) : empreinte, configuration, métriques, durée, machine, commit, date.
Une interruption ne coûte donc que l'unité en cours ; relancer le même script reprend où l'on s'était arrêté.
"""
import hashlib, json, os, platform, socket, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "artifacts" / "results" / "v3"
REGISTRY = RES / "registry.jsonl"


def config_hash(cfg):
    return hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:16]


def git_commit():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=5).stdout.strip() or "inconnu"
    except Exception:
        return "inconnu"


def machine():
    return {"host": socket.gethostname(), "platform": platform.platform(), "python": platform.python_version()}


def _atomic_write(path, text):
    tmp = path.with_suffix(path.suffix + ".tmp"); tmp.write_text(text, encoding="utf-8"); os.replace(tmp, path)


def run_unit(block, name, cfg, fn, code_version="1", force=False, quiet=False):
    """block : sous-dossier (ex. 'A_decoupage'). name : nom lisible. cfg : configuration complète (tout ce qui change le résultat).
    fn() -> dict de métriques (JSON-compatible). Renvoie (résultat, 'calculé' ou 'rechargé')."""
    full = {"block": block, "name": name, "cfg": cfg, "code_version": code_version}; h = config_hash(full)
    d = RES / block; d.mkdir(parents=True, exist_ok=True); path = d / f"{h}.json"
    if path.exists() and not force:
        if not quiet: print(f"[{block}] {name} : rechargé ({h})")
        return json.loads(path.read_text(encoding="utf-8"))["result"], "rechargé"
    if path.exists() and force:                                                               # règle : on ne supprime jamais un résultat précédent
        os.replace(path, path.with_name(f"{h}.ancien-{time.strftime('%Y%m%d-%H%M%S')}.json"))
    t0 = time.time(); result = fn(); sec = round(time.time() - t0, 2)
    rec = {"hash": h, "block": block, "name": name, "cfg": cfg, "code_version": code_version, "result": result, "seconds": sec,
           "machine": machine(), "commit": git_commit(), "date": time.strftime("%Y-%m-%d %H:%M:%S")}
    _atomic_write(path, json.dumps(rec, ensure_ascii=False, indent=1, default=float))
    with open(REGISTRY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({k: rec[k] for k in ("hash", "block", "name", "seconds", "machine", "commit", "date")}, ensure_ascii=False) + "\n")
    if not quiet: print(f"[{block}] {name} : calculé en {sec} s ({h})")
    return result, "calculé"


def load_block(block):
    """Tous les résultats d'un bloc : liste d'enregistrements complets."""
    d = RES / block
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json")) if ".ancien-" not in p.name] if d.exists() else []
