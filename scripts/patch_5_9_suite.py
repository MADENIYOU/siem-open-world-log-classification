"""Compléments de la lecture 5.9 : ligne H5 de 10.2 et plage du registre (cellule 0). Idempotent."""
import nbformat as nbf
from pathlib import Path
NB = Path(__file__).resolve().parents[1] / "TP2_logs_hierarchique_monde_ouvert.ipynb"; nb = nbf.read(NB, as_version=4); done = []
for c in nb.cells:
    if c.cell_type != "markdown": continue
    if "| **H5** |" in c.source and "Contrôle sur logs frais du professeur (5.9)" not in c.source:
        lines = c.source.split("\n"); j = next(k for k, l in enumerate(lines) if l.startswith("| **H5** |")); lines[j] = lines[j].rstrip().rstrip("|").rstrip() + " **Contrôle sur logs frais du professeur (5.9)** : ≈ 0,97 quand le modèle a vu tous les gabarits, 0,44 quand le gabarit vient du jeu de test. |"; c.source = "\n".join(lines); done.append("H5")
    if "**V74 à V79** sont en 0.1b.6 et en 1.7." in c.source:
        c.source = c.source.replace("**V74 à V79** sont en 0.1b.6 et en 1.7.", "**V74 à V99** sont en 0.1b.6, 1.7, 3.7, 4.11, 5.8, 5.9, 6.4, 7.2b, 9.12 et 10.4c.", 1); done.append("plage")
nbf.write(nb, NB); print("appliqué :", done)
