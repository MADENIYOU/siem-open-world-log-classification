"""Scellement vérifiable du test v2 (D27). Ne lit AUCUN log : seulement les colonnes « group » et « role » de groupes_v3.csv (identifiants de gabarits et rôle).
Écrit artifacts/data/test_v2_seal.json : empreinte SHA-256 de la liste triée des identifiants du test v2, leur nombre, empreinte du fichier groups_v3.csv. Idempotent : n'écrase jamais un scellement existant."""
import sys, csv, json, hashlib, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src"))
import tp2_journal as J
G = ROOT / "artifacts" / "data" / "groups_v3.csv"; OUT = ROOT / "artifacts" / "data" / "test_v2_seal.json"
def fingerprint():
    ids = sorted(int(r["group"]) for r in csv.DictReader(open(G, newline="")) if r["role"] == "test2")
    return {"n_test_v2_groups": len(ids), "sha256_sorted_ids": hashlib.sha256(",".join(map(str, ids)).encode()).hexdigest(), "sha256_groups_v3_csv": hashlib.sha256(G.read_bytes()).hexdigest()}
if __name__ == "__main__":
    if OUT.exists(): print("scellement déjà enregistré (jamais écrasé) :", json.loads(OUT.read_text())); sys.exit(0)
    fp = fingerprint(); fp["written"] = __import__("time").strftime("%Y-%m-%d %H:%M:%S"); OUT.write_text(json.dumps(fp, indent=1)); print(fp)
    if not J.exists("D27"):
        J.add("D27", "decision", "Scellement vérifiable du test v2 : empreinte, garde automatique, contrôle au commit",
              "Demande de l'étudiant (2026-11-10) : le test v2 est intouchable, même pour un comptage. Trois contrôles, qui ne lisent aucun log : (1) empreinte SHA-256 de la liste triée des identifiants des %d gabarits du test v2 et du fichier groups_v3.csv, enregistrée dans artifacts/data/test_v2_seal.json (scripts/v3_seal_test_v2.py ne lit que les colonnes « group » et « role ») ; (2) scripts/check_test_seal.py : refuse tout script ou module (hors les trois qui construisent ou scellent le découpage) qui mentionne « test2 », « SealedSplits » ou « unlock » ; (3) le crochet git pre-commit exécute ce contrôle et BLOQUE le commit en cas d'écart (empreinte modifiée, journal d'accès non vide hors ouverture déclarée, script interdit)." % fp["n_test_v2_groups"],
              justification="Règle 11 de la méthodologie d'article : le scellement doit être vérifiable par un lecteur extérieur, pas seulement affirmé.", note="Écrit le 2026-11-10 ; validé par l'étudiant (« vas y je valide »).")
