"""Figures pédagogiques de l'état de l'art (TP2, section 0.1b).

Chaque fonction dessine un schéma dans un repère de 680 unités de large (y vers le bas) et renvoie la figure matplotlib.
Les nombres affichés sont CALCULÉS dans le code quand c'est possible (softmax, produits de probabilités, morceaux de lettres),
pour qu'on puisse les vérifier ; seuls les chiffres de nos résultats (étapes 6 à 9) sont saisis à la main avec leur référence.
"""
import json
import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch

# (remplissage, contour, texte) de chaque couleur : mêmes teintes que le reste du notebook
PAL = {"purple": ("#EEEDFE", "#534AB7", "#26215C"), "teal": ("#E1F5EE", "#0F6E56", "#04342C"), "coral": ("#FAECE7", "#993C1D", "#4A1B0C"),
       "amber": ("#FAEEDA", "#854F0B", "#412402"), "gray": ("#F1EFE8", "#5F5E5A", "#2C2C2A"), "green": ("#EAF3DE", "#3B6D11", "#173404"),
       "blue": ("#E6F1FB", "#185FA5", "#042C53"), "red": ("#FCEBEB", "#A32D2D", "#501313")}
TH, TS = 11.5, 9.5          # tailles de police (titre de boîte, texte courant)


def _canvas(w=680, h=300, width_in=9.0):
    fig, ax = plt.subplots(figsize=(width_in, width_in * h / w))
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, title=None, sub=None, color="gray", lw=0.8, rx=8, tsize=None):
    f, e, t = PAL[color]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={rx}", fc=f, ec=e, lw=lw))
    cx = x + w / 2
    if title is not None and sub is not None:
        ax.text(cx, y + h * 0.36, title, ha="center", va="center", fontsize=tsize or TH, fontweight="bold", color=t)
        ax.text(cx, y + h * 0.70, sub, ha="center", va="center", fontsize=TS - 0.5, color=e)
    elif title is not None:
        ax.text(cx, y + h / 2, title, ha="center", va="center", fontsize=tsize or TH, fontweight="bold", color=t)


def _txt(ax, x, y, s, size=TS, ha="center", bold=False, color="#444441"):
    ax.text(x, y, s, ha=ha, va="center", fontsize=size, fontweight="bold" if bold else "normal", color=color)


def _arrow(ax, x1, y1, x2, y2, color="#5F5E5A", lw=1.1, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle=style, color=color, lw=lw, shrinkA=0, shrinkB=0))


def _line(ax, x1, y1, x2, y2, color="#888780", lw=0.7, ls="-"):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls)


def _dot(ax, x, y, color="gray", r=3.2):
    f, e, _ = PAL[color]
    ax.add_patch(Circle((x, y), r, fc=f, ec=e, lw=0.6))


def _blob(ax, x, y, label, color, r=9):
    f, e, t = PAL[color]
    ax.add_patch(Circle((x, y), r, fc=f, ec=e, lw=1.0))
    ax.text(x, y, label, ha="center", va="center", fontsize=TH, fontweight="bold", color=t)


# --------------------------------------------------------------------------------------------------------------------------------
def fig_monde_ferme_ouvert():
    fig, ax = _canvas(680, 270)
    _txt(ax, 170, 26, "Monde fermé", TH, bold=True); _txt(ax, 170, 44, "Toute entrée reçoit une classe")
    _txt(ax, 510, 26, "Monde ouvert", TH, bold=True); _txt(ax, 510, 44, "Une entrée trop éloignée est rejetée")
    for dx, zone in ((0, False), (340, True)):
        for (cx, cy, lab, col) in ((85, 125, "A", "purple"), (175, 95, "B", "teal"), (265, 130, "C", "coral")):
            if zone:
                ax.add_patch(Circle((cx + dx, cy), 42, fc="none", ec="#888780", lw=0.7, ls=(0, (3, 3))))
            f, e, t = PAL[col]
            ax.add_patch(Circle((cx + dx, cy), 28, fc=f, ec=e, lw=0.9)); _txt(ax, cx + dx, cy, lab, TH, bold=True, color=t)
    _blob(ax, 185, 195, "?", "amber", 11); _arrow(ax, 184, 183, 177, 126)
    _txt(ax, 170, 240, "Rangé dans B, à tort")
    _blob(ax, 525, 205, "?", "amber", 11); _txt(ax, 510, 240, "Hors des zones connues : inconnu")
    return fig


def fig_msp_seuil(z_connu=(4, 1, 0), z_inconnu=(1.2, 1.0, 0.8), seuil=0.7):
    sm = lambda z: np.exp(z) / np.exp(z).sum()
    pk, pu = sm(np.array(z_connu, float)), sm(np.array(z_inconnu, float))
    fig, ax = _canvas(680, 280)
    for x0, p, titre, col in ((40, pk, "Log connu", "teal"), (370, pu, "Log inconnu", "coral")):
        cx = x0 + 110
        _txt(ax, cx, 28, titre, TH, bold=True); _txt(ax, cx, 46, f"Plus grande probabilité : {p.max():.2f}".replace(".", ","))
        _line(ax, x0, 212, x0 + 220, 212)
        for i, (v, lab) in enumerate(zip(p, "ABC")):
            h = 140 * v; x = x0 + 30 + 50 * i
            f, e, _ = PAL[col if i == int(np.argmax(p)) else "gray"]
            ax.add_patch(FancyBboxPatch((x, 212 - h), 36, max(h, 1.5), boxstyle="round,pad=0,rounding_size=2", fc=f, ec=e, lw=0.8))
            _txt(ax, x + 18, 212 - h - 9, f"{v:.2f}".replace(".", ",")); _txt(ax, x + 18, 232, lab)
    _line(ax, 40, 212 - 140 * seuil, 620, 212 - 140 * seuil, color="#BA7517", lw=1.2, ls=(0, (5, 4)))
    _txt(ax, 315, 212 - 140 * seuil - 7, f"seuil {seuil:.1f}".replace(".", ","))
    _txt(ax, 150, 262, f"{pk.max():.2f} au-dessus du seuil : accepté".replace(".", ","))
    _txt(ax, 480, 262, f"{pu.max():.2f} sous le seuil : rejeté".replace(".", ","))
    return fig


def fig_trois_methodes():
    fig, ax = _canvas(680, 262)
    # OpenMax
    _txt(ax, 120, 26, "OpenMax", TH, bold=True); _txt(ax, 120, 44, "Distance au vecteur typique")
    ax.add_patch(Circle((112, 122), 34, fc="none", ec="#888780", lw=0.7, ls=(0, (3, 3))))
    for (x, y) in ((98, 112), (112, 104), (126, 114), (102, 130), (120, 136), (134, 126), (90, 124)): _dot(ax, x, y)
    _blob(ax, 112, 122, "", "purple", 5); _txt(ax, 112, 170, "typique"); _blob(ax, 190, 196, "?", "amber", 9)
    _arrow(ax, 117, 127, 183, 190); _txt(ax, 120, 236, "Loin du typique : la masse va"); _txt(ax, 120, 252, "vers « inconnu »")
    # Mahalanobis
    _txt(ax, 340, 26, "Mahalanobis", TH, bold=True); _txt(ax, 340, 44, "Tient compte de la forme")
    ax.add_patch(Ellipse((340, 125), 116, 36, fc="none", ec="#0F6E56", lw=1.3))
    ax.add_patch(Circle((340, 125), 46, fc="none", ec="#888780", lw=0.7, ls=(0, (3, 3))))
    for (x, y) in ((318, 122), (336, 130), (352, 120), (366, 128), (326, 132)): _dot(ax, x, y)
    _blob(ax, 386, 125, "A", "green", 7); _blob(ax, 340, 171, "B", "amber", 7)
    _txt(ax, 405, 125, "normal", ha="left"); _txt(ax, 352, 190, "inconnu", ha="left")
    _txt(ax, 340, 236, "Même distance (pointillés),"); _txt(ax, 340, 252, "mais B sort de l'ellipse")
    # kNN
    _txt(ax, 560, 26, "kNN", TH, bold=True); _txt(ax, 560, 44, "Distance aux voisins")
    for (x, y) in ((538, 108), (552, 100), (566, 110), (545, 124), (560, 130), (576, 122), (532, 122), (572, 102)): _dot(ax, x, y)
    for (x, y) in ((579, 124), (569, 112), (563, 132)): _line(ax, 620, 175, x, y, ls=(0, (3, 3)))
    _blob(ax, 620, 175, "?", "amber", 9)
    _txt(ax, 560, 236, "Loin même de ses plus proches"); _txt(ax, 560, 252, "voisins : « inconnu »")
    return fig


def fig_ou_lire():
    fig, ax = _canvas(680, 330)
    _txt(ax, 20, 28, "Chemin du modèle TF-IDF", TH, ha="left", bold=True)
    _box(ax, 20, 44, 90, 56, "Log"); _box(ax, 150, 44, 130, 56, "TF-IDF", "9 880 valeurs"); _box(ax, 320, 44, 150, 56, "Classifieur", "LR ou SVM")
    _box(ax, 530, 44, 130, 56, "24 scores", "un par classe", "coral")
    _box(ax, 150, 120, 130, 56, "SVD", "compresse"); _box(ax, 320, 120, 150, 56, "Vecteur dense", "100 valeurs", "teal")
    for a in ((110, 72, 148, 72), (280, 72, 318, 72), (470, 72, 528, 72), (215, 100, 215, 118), (280, 148, 318, 148)): _arrow(ax, *a)
    _txt(ax, 20, 206, "Chemin de l'encodeur DistilBERT", TH, ha="left", bold=True)
    _box(ax, 20, 220, 90, 56, "Log"); _box(ax, 150, 220, 130, 56, "DistilBERT", "lit le log"); _box(ax, 320, 220, 150, 56, "Vecteur dense", "768 valeurs", "teal")
    _box(ax, 530, 220, 130, 56, "24 scores", "un par classe", "coral")
    for a in ((110, 248, 148, 248), (280, 248, 318, 248), (470, 248, 528, 248)): _arrow(ax, *a)
    _txt(ax, 499, 238, "têtes", TS - 1)
    _box(ax, 20, 300, 12, 12, None, None, "coral", rx=2); _txt(ax, 40, 306, "Lu par MSP, énergie, OpenMax", ha="left")
    _box(ax, 340, 300, 12, 12, None, None, "teal", rx=2); _txt(ax, 360, 306, "Lu par Mahalanobis, kNN", ha="left")
    return fig


def fig_taxonomie_erreurs():
    fig, ax = _canvas(680, 270)
    for (x2, y2) in ((120, 84), (340, 84), (560, 84)): _line(ax, 340, 54, x2, y2)
    for fx, cs in ((120, (70, 170)), (340, (290, 390)), (560, (510, 610))):
        for cx in cs: _line(ax, fx, 118, cx, 164)
    _box(ax, 280, 20, 120, 34, "Événement", None, "gray")
    for cx, lab, col in ((120, "authentication", "purple"), (340, "file", "teal"), (560, "network", "coral")): _box(ax, cx - 75, 84, 150, 34, lab, None, col)
    for cx, lab, col, lw in ((70, "auth-failed", "amber", 1.8), (170, "auth-success", "purple", 0.8), (290, "file-deleted", "teal", 0.8),
                              (390, "file-read", "teal", 0.8), (510, "net-traffic", "coral", 0.8), (610, "net-filtered", "coral", 0.8)):
        _box(ax, cx - 45, 164, 90, 40, lab, None, col, lw=lw, tsize=TS)
    _txt(ax, 70, 228, "classe vraie", TH, bold=True)
    _txt(ax, 170, 228, "erreur légère", TH, bold=True); _txt(ax, 170, 246, "distance 1")
    _txt(ax, 290, 228, "erreur grave", TH, bold=True); _txt(ax, 290, 246, "distance 2")
    return fig


def fig_produit_probas(p_fam=(0.8, 0.2), p_cl=((0.6, 0.4), (0.5, 0.5))):
    fig, ax = _canvas(680, 270)
    fams = ((190, "authentication", "purple", ("auth-failed", "auth-success"), (120, 260)), (490, "file", "teal", ("file-deleted", "file-read"), (420, 560)))
    _box(ax, 290, 18, 100, 34, "Événement", None, "gray")
    for i, (fx, lab, col, cls, cxs) in enumerate(fams):
        _line(ax, 340, 52, fx, 86); _box(ax, fx - 65, 86, 130, 34, lab, None, col)
        _txt(ax, (340 + fx) / 2 + (-18 if i == 0 else 18), 66, f"{p_fam[i]:.1f}".replace(".", ","), ha="center")
        for j, (c, cx) in enumerate(zip(cls, cxs)):
            _line(ax, fx, 120, cx, 164); prod = p_fam[i] * p_cl[i][j]
            _txt(ax, (fx + cx) / 2 + (-12 if j == 0 else 12), 142, f"{p_cl[i][j]:.1f}".replace(".", ","))
            best = (i == 0 and j == 0)
            _box(ax, cx - 55, 164, 110, 40, c, None, "amber" if best else col, lw=1.6 if best else 0.8, tsize=TS)
            _txt(ax, cx, 228, f"{p_fam[i]:.1f} × {p_cl[i][j]:.1f} = {prod:.2f}".replace(".", ","), bold=best)
    return fig


def fig_trois_cas():
    fig, ax = _canvas(680, 280)
    cartes = ((20, "Log connu", "teal", "Famille : 0,90", "Classe dans la famille : 0,85", "Produit : 0,77", "auth-failed", "famille et classe sûres"),
              (240, "Classe nouvelle", "amber", "Famille : 0,88", "Classe dans la famille : 0,45", "Produit : 0,40", "inconnu, famille", "authentication"),
              (460, "Famille nouvelle", "coral", "Famille : 0,36", "Classe dans la famille : 0,50", "Produit : 0,18", "inconnu total", "aucune famille sûre"))
    for x, tit, col, a, b, c, r1, r2 in cartes:
        f, e, t = PAL[col]
        ax.add_patch(FancyBboxPatch((x, 20), 200, 190, boxstyle="round,pad=0,rounding_size=12", fc=f, ec=e, lw=0.8))
        _txt(ax, x + 100, 44, tit, TH, bold=True, color=t)
        for k, s in enumerate((a, b, c)): _txt(ax, x + 100, 72 + 20 * k, s, color=e)
        _txt(ax, x + 100, 150, "Réponse", TH, bold=True, color=t); _txt(ax, x + 100, 172, r1, color=e); _txt(ax, x + 100, 192, r2, color=e)
    _txt(ax, 340, 242, "Seuil de famille 0,7 : sous le seuil, on ne propose aucune famille")
    _txt(ax, 340, 262, "Seuil du produit 0,6 : sous le seuil, on rejette la classe fine")
    return fig


def fig_adversarial():
    """Baisse relative (%) au test, TF-IDF de mots : registre V60 du notebook (étape 9)."""
    data = {"Homoglyphes": (8.2, 3.8, 8.4), "Fautes de frappe": (3.4, 4.0, 4.2), "Remplissage": (4.9, 0.5, 5.7)}
    cols = ("gray", "teal", "coral"); labs = ("sans défense", "entraîné sur cette attaque", "entraîné sans cette attaque")
    fig, ax = _canvas(680, 262)
    for k, (c, l) in enumerate(zip(cols, labs)):
        x = (40, 200, 410)[k]; _box(ax, x, 12, 12, 12, None, None, c, rx=2); _txt(ax, x + 18, 18, l, ha="left")
    _line(ax, 40, 215, 640, 215)
    for g, (name, vals) in enumerate(data.items()):
        x0 = 80 + 220 * g
        for k, v in enumerate(vals):
            h = 14 * v; f, e, _ = PAL[cols[k]]; x = x0 + 48 * k
            ax.add_patch(FancyBboxPatch((x, 215 - h), 30, max(h, 1.5), boxstyle="round,pad=0,rounding_size=2", fc=f, ec=e, lw=0.8))
            _txt(ax, x + 15, 215 - h - 9, f"{v:.1f} %".replace(".", ","), TS - 1)
        _txt(ax, x0 + 63, 238, name, TH, bold=True)
    return fig


def fig_ngrammes(mot="failed", attaque="fаiled", n=3):
    g = lambda w: [w[i:i + n] for i in range(len(w) - n + 1)]
    a, b = g(mot), g(attaque); commun = [x == y for x, y in zip(a, b)]
    fig, ax = _canvas(680, 230)
    _txt(ax, 20, 64, "Mot normal", TH, ha="left", bold=True); _txt(ax, 20, 84, mot, ha="left")
    _txt(ax, 20, 134, "Mot attaqué", TH, ha="left", bold=True); _txt(ax, 20, 154, f"{attaque} (а cyrillique)", ha="left")
    for i, (u, v, ok) in enumerate(zip(a, b, commun)):
        _box(ax, 150 + 80 * i, 44, 70, 40, u, None, "gray"); _box(ax, 150 + 80 * i, 114, 70, 40, v, None, "teal" if ok else "coral")
    _txt(ax, 490, 134, f"{sum(commun)} morceaux sur {len(a)} en commun", ha="left")
    _txt(ax, 150, 186, "Mot entier : 0 en commun sur 1, le mot est perdu", ha="left")
    _box(ax, 150, 204, 12, 12, None, None, "teal", rx=2); _txt(ax, 168, 210, "morceau commun", ha="left")
    _box(ax, 330, 204, 12, 12, None, None, "coral", rx=2); _txt(ax, 348, 210, "morceau perdu", ha="left")
    return fig


def reliability_from_files(colab_dir, data_csv):
    """Diagramme de fiabilité réel de l'encodeur (5 rotations regroupées, logs de classes connues)."""
    import pandas as pd
    from scipy.special import softmax
    df = pd.read_csv(data_csv); out = {}
    for split in ("val", "test"):
        d = df[df.split == split].reset_index(drop=True); conf, corr = [], []
        for r in range(1, 6):
            base = "out_v2" if r <= 2 else "out_v2_local"; tag = f"uncased_rot{r}_len256_s42"
            m = json.load(open(f"{colab_dir}/{base}/{tag}.json")); z = np.load(f"{colab_dir}/{base}/{tag}_{split}.npz")["logits_fine"]
            known = np.array(m["known"]); isk = d.category.isin(known).values; p = softmax(z, 1)
            conf.append(p.max(1)[isk]); corr.append((known[p.argmax(1)] == d.category.values)[isk])
        conf, corr = np.concatenate(conf), np.concatenate(corr); idx = np.clip(np.digitize(conf, np.linspace(0, 1, 11)[1:-1]), 0, 9); bins = []
        for b in range(10):
            mk = idx == b
            if mk.sum() >= 50: bins.append((float(conf[mk].mean()), float(corr[mk].mean()), int(mk.sum())))
        out[split] = {"bins": bins, "conf": float(conf.mean()), "acc": float(corr.mean()), "ece": float(sum(n / len(conf) * abs(a - c) for c, a, n in bins))}
    return out


def fig_fiabilite(rel):
    fig, ax = _canvas(680, 330)
    X = lambda c: 70 + 240 * c; Y = lambda a: 280 - 240 * a
    _line(ax, 70, 280, 310, 280); _line(ax, 70, 280, 70, 40); _line(ax, 70, 280, 310, 40, ls=(0, (4, 3)))
    for v, lab in ((0, "0"), (0.5, "0,5"), (1, "1")):
        _txt(ax, X(v), 298, lab); _txt(ax, 62, Y(v) + 3, lab, ha="right")
    _txt(ax, 190, 318, "confiance annoncée"); _txt(ax, 70, 24, "exactitude réelle", ha="left")
    for split, col, ec, y0, titre in (("val", "teal", "#0F6E56", 70, "Validation"), ("test", "coral", "#993C1D", 170, "Test")):
        b = rel[split]["bins"]; xs = [X(c) for c, a, n in b]; ys = [Y(a) for c, a, n in b]
        ax.plot(xs, ys, color=ec, lw=1.5)
        for x, y in zip(xs, ys): _dot(ax, x, y, col)
        _box(ax, 360, y0, 12, 12, None, None, col, rx=2); _txt(ax, 380, y0 + 6, titre, TH, ha="left", bold=True)
        _txt(ax, 380, y0 + 28, f"confiance moyenne {rel[split]['conf']:.2f}".replace(".", ","), ha="left")
        _txt(ax, 380, y0 + 46, f"exactitude réelle {rel[split]['acc']:.2f}".replace(".", ","), ha="left")
        _txt(ax, 380, y0 + 64, f"ECE {rel[split]['ece']:.2f}".replace(".", ","), ha="left")
    _txt(ax, 360, 276, "Pointillés : calibration parfaite", ha="left")
    return fig


def fig_decoupage():
    fig, ax = _canvas(680, 250)
    _txt(ax, 170, 24, "Découpage aléatoire", TH, bold=True); _txt(ax, 510, 24, "Découpage par gabarit", TH, bold=True)
    for x, w in ((20, 190), (220, 100), (360, 190), (560, 100)):
        ax.add_patch(FancyBboxPatch((x, 40), w, 130, boxstyle="round,pad=0,rounding_size=8", fc="none", ec="#888780", lw=0.7, ls=(0, (4, 3))))
    cols = ("purple", "teal", "coral", "amber")
    for r in range(2):
        for c in range(4): _box(ax, 41 + 40 * c, 72 + 36 * r, 28, 28, None, None, cols[c], rx=4)
    for k, c in enumerate(cols): _box(ax, 238 + 36 * (k % 2), 72 + 36 * (k // 2), 28, 28, None, None, c, rx=4)
    for r in range(3):
        for c in range(3): _box(ax, 405 + 36 * c, 66 + 34 * r, 28, 28, None, None, cols[c], rx=4)
        _box(ax, 596, 66 + 34 * r, 28, 28, None, None, "amber", rx=4)
    for x, s in ((115, "entraînement"), (270, "test"), (455, "entraînement"), (610, "test")): _txt(ax, x, 190, s)
    _txt(ax, 170, 218, "Même gabarit des deux côtés :"); _txt(ax, 170, 234, "le modèle le reconnaît")
    _txt(ax, 510, 218, "Gabarits du test jamais vus :"); _txt(ax, 510, 234, "mesure honnête")
    return fig
