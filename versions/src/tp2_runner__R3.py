"""Exécuteur reprenable et traçable (protocole v3).

Une expérience = une UNITÉ décrite par une configuration (dictionnaire). Son empreinte (hash de la configuration + version du code déclarée)
donne le nom du fichier de résultat. Si ce fichier existe, on le recharge ; sinon on calcule, on écrit le résultat de façon atomique et on
ajoute une ligne au registre (append-only) : empreinte, configuration, métriques, durée, machine, commit, date.
Une interruption ne coûte donc que l'unité en cours ; relancer le même script reprend où l'on s'était arrêté.
"""
import hashlib, json, os, platform, shutil, socket, subprocess, sys, time
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


AUTO = ROOT / "versions" / "auto"
_CODE = None


def snapshot_code():
    """Garde-fou (règle : aucune version de code ne se perd) : au premier calcul d'un processus, copie le script lancé et les modules `src/tp2_*.py`
    dans versions/auto/<nom>__<empreinte>.<ext> (adressage par contenu : jamais d'écrasement, une copie par état distinct) et renvoie leurs empreintes.
    Ainsi le code qui a produit un résultat est conservé même s'il n'a jamais été commité."""
    global _CODE
    if _CODE is not None: return _CODE
    files = [Path(sys.argv[0]).resolve()] if sys.argv and sys.argv[0] else []
    files += sorted((ROOT / "src").glob("tp2_*.py")); shas = {}
    for f in files:
        try:
            if ROOT not in f.parents: continue
            data = f.read_bytes(); sha = hashlib.sha256(data).hexdigest()[:12]; shas[f.name] = sha
            dest = AUTO / f"{f.stem}__{sha}{f.suffix}"
            if not dest.exists():
                AUTO.mkdir(parents=True, exist_ok=True); tmp = dest.with_suffix(dest.suffix + f".tmp{os.getpid()}"); tmp.write_bytes(data); os.replace(tmp, dest)
        except OSError:
            pass
    _CODE = shas; return _CODE


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
    snapshot_code()                                                                          # le code est conservé AVANT de calculer
    t0 = time.time(); result = fn(); sec = round(time.time() - t0, 2)
    rec = {"hash": h, "block": block, "name": name, "cfg": cfg, "code_version": code_version, "result": result, "seconds": sec,
           "machine": machine(), "commit": git_commit(), "code": snapshot_code(), "date": time.strftime("%Y-%m-%d %H:%M:%S")}
    _atomic_write(path, json.dumps(rec, ensure_ascii=False, indent=1, default=float))
    with open(REGISTRY, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({k: rec[k] for k in ("hash", "block", "name", "seconds", "machine", "commit", "code", "date")}, ensure_ascii=False) + "\n")
    if not quiet: print(f"[{block}] {name} : calculé en {sec} s ({h})")
    return result, "calculé"


def load_block(block):
    """Tous les résultats d'un bloc : liste d'enregistrements complets."""
    d = RES / block
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(d.glob("*.json")) if ".ancien-" not in p.name] if d.exists() else []
