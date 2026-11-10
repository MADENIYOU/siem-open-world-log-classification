"""Contrôle du scellement du test v2 (D27). Sortie 0 si tout est conforme, 1 sinon (le crochet pre-commit bloque alors le commit). Ne lit aucun log."""
import sys, json, pathlib, re
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "scripts"))
import v3_seal_test_v2 as S
ALLOW = {"scripts/v3_make_split.py", "src/tp2_split_v3.py", "scripts/v3_seal_test_v2.py", "scripts/check_test_seal.py", "scripts/v3_register_D27.py"}
FORBID = re.compile(r"test2|SealedSplits|\.unlock\(|test_v2_access")
problems = []
log = ROOT / "artifacts" / "results" / "v3" / "test_v2_access_log.json"
if json.loads(log.read_text()) != [] and "--opened" not in sys.argv: problems.append("le journal d'accès au test v2 n'est pas vide")
seal = S.OUT
if not seal.exists(): problems.append("pas de scellement enregistré (lancer scripts/v3_seal_test_v2.py)")
else:
    ref, now = json.loads(seal.read_text()), S.fingerprint()
    for k in ("n_test_v2_groups", "sha256_sorted_ids", "sha256_groups_v3_csv"):
        if ref[k] != now[k]: problems.append(f"empreinte modifiée : {k}")
for d in ("scripts", "src", "colab", "presentation"):
    for p in (ROOT / d).rglob("*.py"):
        rel = p.relative_to(ROOT).as_posix()
        if "/versions/" in "/" + rel or rel in ALLOW: continue
        if FORBID.search(p.read_text(errors="ignore")): problems.append(f"référence interdite au test v2 : {rel}")
if problems: print("SCELLEMENT DU TEST v2 : ÉCART\n - " + "\n - ".join(problems)); sys.exit(1)
print("scellement du test v2 : conforme (journal d'accès vide, empreintes identiques, aucun script ne le référence)")
