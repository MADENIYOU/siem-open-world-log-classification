"""Journal append-only du protocole v3 : règles, décisions, hypothèses, résultats.
Aucune entrée n'est jamais modifiée ni supprimée : changer le statut d'une hypothèse ajoute une NOUVELLE version de la même entrée (l'historique reste lisible).
`render()` produit REGISTRE_V3.md : la version la plus récente de chaque entrée, plus l'historique de ses versions précédentes."""
import json, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "artifacts" / "results" / "v3" / "journal.jsonl"
STATUTS = ("préinscrite", "confirmée", "réfutée", "non tranchée", "abandonnée")


def entries():
    return [json.loads(l) for l in JOURNAL.read_text(encoding="utf-8").splitlines() if l.strip()] if JOURNAL.exists() else []


def add(id, type, titre, texte, justification="", statut=None, preuve="", note=""):
    """type : regle | decision | hypothese | resultat. Pour une hypothèse, statut parmi STATUTS. Ajoute une version (jamais d'écrasement)."""
    assert type in ("regle", "decision", "hypothese", "resultat"); assert statut is None or statut in STATUTS
    ver = 1 + sum(1 for e in entries() if e["id"] == id); JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    rec = {"id": id, "version": ver, "type": type, "date": time.strftime("%Y-%m-%d %H:%M:%S"), "titre": titre, "texte": texte, "justification": justification, "statut": statut, "preuve": preuve, "note": note}
    with open(JOURNAL, "a", encoding="utf-8") as fh: fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def exists(id):
    return any(e["id"] == id for e in entries())


def render(path=None):
    path = Path(path or ROOT / "REGISTRE_V3.md"); es = entries(); by = {}
    for e in es: by.setdefault(e["id"], []).append(e)
    out = ["# Registre du protocole v3 (règles, décisions, hypothèses, résultats)\n",
           "Généré à partir de `artifacts/results/v3/journal.jsonl` (append-only : rien n'est jamais supprimé ni écrasé ; un changement de statut ajoute une version). Ne pas modifier à la main.\n"]
    for typ, titre in (("regle", "Règles de travail"), ("decision", "Décisions"), ("hypothese", "Hypothèses (préinscrites, puis confirmées ou réfutées)"), ("resultat", "Résultats")):
        ids = [i for i, v in by.items() if v[-1]["type"] == typ]
        if not ids: continue
        out.append(f"\n## {titre}\n")
        for i in ids:
            v = by[i]; last = v[-1]; st = f" ; **statut : {last['statut']}**" if last["statut"] else ""
            out.append(f"\n### {i} : {last['titre']}  (version {last['version']}, {last['date']}{st})\n\n{last['texte']}\n")
            if last["justification"]: out.append(f"\n*Justification.* {last['justification']}\n")
            if last["preuve"]: out.append(f"\n*Preuve.* {last['preuve']}\n")
            if last["note"]: out.append(f"\n*Note.* {last['note']}\n")
            if len(v) > 1:
                out.append("\n*Historique des versions précédentes (conservées) :*\n")
                for p in v[:-1]: out.append(f"- v{p['version']} ({p['date']}) : statut {p['statut']} ; {p['texte'][:200]}{'…' if len(p['texte']) > 200 else ''}\n")
    path.write_text("".join(out), encoding="utf-8"); return path
