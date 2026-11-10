"""Diagnostic exploratoire DG2 (non préinscrit, ne produit aucun verdict) : d'où vient le plafond de 0,50 ? (a) F1 par classe, (b) borne haute « oracle » : agréger les marges du SVM par VRAI gabarit au test, (c) lissage par plus proches voisins du test (sans étiquette). Répétition 0, 5 plis."""
import sys, pathlib, warnings
ROOT = pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score
from sklearn.neighbors import NearestNeighbors
import v3_blockA as A
warnings.filterwarnings("ignore")
dev, tierA = A.load(); ya = dev.category.astype("category"); classes = list(ya.cat.categories); y = ya.cat.codes.values; ids = [classes.index(c) for c in tierA]; fold = dev["fold_r0"].values; rows = []; perclass = {}
def f1a(yt, p): lab = [c for c in ids if (yt == c).any()]; return f1_score(yt, p, labels=lab, average="macro", zero_division=0)
for k in range(5):
    te, tr = np.where(fold == k)[0], np.where(fold != k)[0]; v = TfidfVectorizer(token_pattern=r"[A-Za-z]{2,}", lowercase=True, sublinear_tf=True, min_df=2); Xtr, Xte = v.fit_transform(dev.log.values[tr]), v.transform(dev.log.values[te])
    m = LinearSVC(C=1).fit(Xtr, y[tr]); D = m.decision_function(Xte); yt = y[te]; cl = m.classes_; r = {"fold": k, "base": f1a(yt, cl[D.argmax(1)])}
    for c, f in zip(cl, f1_score(yt, cl[D.argmax(1)], labels=cl, average=None, zero_division=0)): perclass.setdefault(classes[c], []).append(f)
    g = dev.group.values[te]; Dg = pd.DataFrame(D).groupby(g).transform("mean").values; r["oracle_gabarit_vrai"] = f1a(yt, cl[Dg.argmax(1)])
    nn = NearestNeighbors(n_neighbors=51, metric="cosine", algorithm="brute").fit(Xte); _, ind = nn.kneighbors(Xte)
    for kk in (5, 10, 20, 50): Ds = D[ind[:, :kk + 1]].mean(1); r[f"voisins_{kk}"] = f1a(yt, cl[Ds.argmax(1)])
    # pureté des voisins : part des voisins du test qui ont le même vrai gabarit / même classe
    r["pureté_gabarit_voisins10"] = float((g[ind[:, 1:11]] == g[:, None]).mean()); r["pureté_classe_voisins10"] = float((yt[ind[:, 1:11]] == yt[:, None]).mean()); rows.append(r)
df = pd.DataFrame(rows); print(df.round(4).to_string(index=False)); print("\nmoyennes :\n", df.drop(columns="fold").mean().round(4).to_string())
pc = pd.Series({c: np.mean(f) for c, f in perclass.items()}).sort_values(); print("\nF1 par classe (30), plus faibles :\n", pc.head(12).round(3).to_string(), "\nplus fortes :\n", pc.tail(6).round(3).to_string())
