"""DG4 (exploratoire, aucun verdict, AUCUN entraînement) : trois comptages sur le DÉVELOPPEMENT seulement, en validation « hors-un-gabarit » interne.
(1) format du log (en-tête, programme) contre classe : raccourci possible ? (2) vocabulaire constant d'un gabarit mis de côté contre sa classe et les autres ; (3) gabarits par axe d'action et d'objet.
Le chargeur v3_blockA.load() n'expose que le développement."""
import sys, re, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, pandas as pd
import v3_blockA as A, tp2_fields as F
dev, _ = A.load(); out = ROOT / "artifacts" / "results" / "v3"; WORD = re.compile(r"[A-Za-z]{2,}")
def sig_forme(t): return "-".join(F.vtype(x)[:3] for x in t.split()[:6])
def sig_prog(t): m = F.RE_PROG.search(t); return m.group(1).lower() if m else "aucun"
def mode(s): return collections.Counter(s).most_common(1)[0][0]
G = dev.groupby("group"); T = pd.DataFrame({"classe": G.category.first(), "n_logs": G.size()})
T["forme6"] = G.log.apply(lambda s: mode([sig_forme(x) for x in s])); T["prog"] = G.log.apply(lambda s: mode([sig_prog(x) for x in s]))
T["format"] = T.prog + "|" + T.forme6.str[:15]; print("gabarits du développement :", len(T), "; classes :", T.classe.nunique(), "; gabarits par classe (min, médiane, max) :", T.classe.value_counts().min(), int(T.classe.value_counts().median()), T.classe.value_counts().max())
# (1) format x classe
def nmi(f, c):
    ct = pd.crosstab(T[f], T[c]).values.astype(float); p = ct / ct.sum(); pf, pc = p.sum(1, keepdims=True), p.sum(0, keepdims=True); mi = np.nansum(p * np.log(p / (pf * pc) + 1e-300)); hc = -np.nansum(pc * np.log(pc + 1e-300)); return mi / hc
res1 = []
for f in ("prog", "forme6", "format"):
    lk = []; 
    for g, r in T.iterrows():
        o = T.drop(index=g); o = o[o[f] == r[f]]
        lk.append((r.classe, mode(list(o.classe)) if len(o) else None, len(o)))
    L = pd.DataFrame(lk, columns=["vrai", "pred", "n"]); cov = L.pred.notna().mean(); acc = (L.pred == L.vrai)[L.pred.notna()].mean(); rec = L.assign(ok=L.pred == L.vrai).groupby("vrai").ok.mean()
    res1.append({"signature": f, "NMI format-classe": round(nmi(f, "classe"), 3), "formats distincts": T[f].nunique(), "couverture (gabarit a un autre gabarit de même format)": round(cov, 3), "exactitude sur les couverts": round(acc, 3), "rappel moyen par classe (tous gabarits)": round(rec.mean(), 3), "classes avec rappel > 0": int((rec > 0).sum())})
R1 = pd.DataFrame(res1); R1.to_csv(out / "DG4_format_classe.csv", index=False); print("\n(1) format × classe, prédiction du gabarit mis de côté par la classe majoritaire des autres gabarits de même format\n", R1.to_string(index=False))
# (2) vocabulaire constant
const = {}; allw = {}
for g, s in G.log:
    ws = [set(WORD.findall(x.lower())) for x in s]; n = len(ws); cnt = collections.Counter(w for x in ws for w in x); const[g] = {w for w, k in cnt.items() if k >= 0.8 * n}; allw[g] = set(cnt)
rows = []
for g, r in T.iterrows():
    C = const[g]
    if not C: continue
    other = [h for h in T.index if h != g]; byc = collections.defaultdict(set)
    for h in other: byc[T.classe[h]] |= const[h]
    union = set().union(*[const[h] for h in other]); cov = {c: len(C & V) / len(C) for c, V in byc.items()}; own = cov.get(r.classe, 0.0); best_other = max((v for c, v in cov.items() if c != r.classe), default=0.0)
    rows.append({"gabarit": g, "classe": r.classe, "n_mots_constants": len(C), "couverture_classe": own, "meilleure_autre_classe": best_other, "mots_jamais_vus_ailleurs": len(C - union) / len(C), "autres_gabarits_de_la_classe": int((T.classe == r.classe).sum()) - 1})
V = pd.DataFrame(rows); V["propre_gagne"] = V.couverture_classe > V.meilleure_autre_classe; V.to_csv(out / "DG4_vocabulaire_gabarits.csv", index=False)
S = V.groupby("classe").agg(gabarits=("gabarit", "size"), couverture_classe=("couverture_classe", "median"), meilleure_autre=("meilleure_autre_classe", "median"), propre_gagne=("propre_gagne", "mean"), jamais_vus=("mots_jamais_vus_ailleurs", "median")).round(3); S.to_csv(out / "DG4_vocabulaire_par_classe.csv")
print("\n(2) vocabulaire constant (mots présents dans ≥ 80 % des logs du gabarit) : couverture par sa classe contre la meilleure autre classe, gabarit mis de côté")
print("   part des gabarits où la bonne classe couvre strictement plus que toute autre :", round(V.propre_gagne.mean(), 3), "; médiane des mots constants jamais vus dans un autre gabarit :", round(V.mots_jamais_vus_ailleurs.median(), 3))
print("   par nombre d'autres gabarits dans la classe : ", V.groupby(V.autres_gabarits_de_la_classe.clip(upper=4)).propre_gagne.agg(["mean", "size"]).round(3).to_dict())
print(S.sort_values("propre_gagne").head(12).to_string())
# (3) axes
AX = {"authentication-failed": ("authentification", "échec"), "authentication-success": ("authentification", "succès"), "connection-closed": ("connexion", "fermeture"), "connection-failed": ("connexion", "échec"), "connection-opened": ("connexion", "ouverture"),
      "database-operation": ("base de données", "opération"), "directory-changed": ("répertoire", "modification"), "directory-created": ("répertoire", "création"), "directory-deleted": ("répertoire", "suppression"), "file-action-failure": ("fichier", "échec"),
      "file-deleted": ("fichier", "suppression"), "file-modification": ("fichier", "modification"), "file-read": ("fichier", "lecture"), "file-write": ("fichier", "écriture"), "hardware-monitoring": ("matériel", "surveillance"),
      "http-request-failure": ("http", "échec"), "http-request-success": ("http", "succès"), "ids-alert": ("ids", "alerte"), "network-filtered": ("réseau", "filtrage"), "network-traffic": ("réseau", "trafic"), "process-ended": ("processus", "fermeture"),
      "process-error": ("processus", "échec"), "process-info": ("processus", "information"), "process-shutdown": ("processus", "fermeture"), "process-started": ("processus", "ouverture"), "system-configuration-changed": ("système", "modification"),
      "user-creation": ("utilisateur", "création"), "user-deletion": ("utilisateur", "suppression"), "user-logout": ("utilisateur", "fermeture"), "user-session-open": ("utilisateur", "ouverture")}
T["objet"] = T.classe.map(lambda c: AX[c][0]); T["action"] = T.classe.map(lambda c: AX[c][1]); A3 = T.groupby("classe").agg(gabarits=("n_logs", "size"), logs=("n_logs", "sum")); A3["objet"] = A3.index.map(lambda c: AX[c][0]); A3["action"] = A3.index.map(lambda c: AX[c][1])
A3["gabarits_de_même_objet"] = A3.objet.map(T.objet.value_counts()); A3["gabarits_de_même_action"] = A3.action.map(T.action.value_counts()); A3.to_csv(out / "DG4_axes.csv")
print("\n(3) gabarits par classe, par objet et par action (axes tirés des noms de classes)\n", A3.sort_values("gabarits").to_string())
print("\nnombre de gabarits : par action :", T.action.value_counts().to_dict(), "\n par objet :", T.objet.value_counts().to_dict())
