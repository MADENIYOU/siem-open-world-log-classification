"""Ajoute au notebook la décomposition 5.9e (pourquoi 0,81 et non 0,97) et sa figure. Idempotent."""
import nbformat as nbf
from pathlib import Path
NB = Path(__file__).resolve().parents[1] / "TP2_logs_hierarchique_monde_ouvert.ipynb"; nb = nbf.read(NB, as_version=4)
if any("REV-5.9e" in "".join(c.source) for c in nb.cells): raise SystemExit("déjà appliqué")
code_e = '''# ---- R5.9e : pourquoi 0,81 et non 0,97 ? Décomposition selon le découpage auquel appartient le log SIEVE le plus proche
cF, tF = FRESH["0"]; idx = np.random.default_rng(CONFIG["seed"]).choice(len(tF), 5000, replace=False); tt = [tF[i] for i in idx]; yy = cF[idx]
vecN = TfidfVectorizer(analyzer=word_tokens, min_df=2, sublinear_tf=True, dtype=np.float32).fit(TXTFULL[0]); XR = vecN.transform(TXTFULL[0]); XA = vecN.transform(tt); arg = np.zeros(len(idx), int); best = np.zeros(len(idx))
for s_ in range(0, len(idx), 500): M_ = (XA[s_:s_ + 500] @ XR.T).toarray(); best[s_:s_ + 500] = M_.max(1); arg[s_:s_ + 500] = M_.argmax(1)
split0 = S[S.version == 0].set_index("row")["split"]; nn_split = split0.reindex(arg).values                                          # découpage (entraînement, validation, test) du log SIEVE_00 le plus proche
vecT = TfidfVectorizer(analyzer=word_tokens, min_df=2, sublinear_tf=True, dtype=np.float32).fit(tr_text); clfT = LinearSVC(C=1.0).fit(vecT.transform(tr_text), ytr); ok = (clfT.predict(vecT.transform(tt)) == yy)       # modèle de 5.9a
rows = []
for lab, m in (("plus proche voisin dans l'entraînement", nn_split == "train"), ("plus proche voisin dans la validation", nn_split == "val"), ("plus proche voisin dans le test", nn_split == "test"), ("similarité ≥ 0,90", best >= 0.90), ("similarité < 0,90", best < 0.90)):
    rows.append({"groupe": lab, "part des logs": round(float(m.mean()), 3), "exactitude": round(float(ok[m].mean()), 4) if m.any() else float("nan")})
dfE = pd.DataFrame(rows); print(f"exactitude globale sur ces {len(idx):,} logs : {ok.mean():.4f}"); print(dfE.to_string(index=False)); dfE.to_csv(DIRS["results"] / "step5_donnees_fraiches_decomposition.csv", index=False)
'''
fig_e = 'import tp2_new_figs as NF\nfig = NF.fig_5_9b(DIRS["results"], DIRS["figures"]); plt.show()'
i = next(i for i, c in enumerate(nb.cells) if c.cell_type == "code" and "step5_jumeaux_professeur.csv" in c.source)
new = [nbf.v4.new_markdown_cell("<!-- REV-5.9e -->\n### 5.9e Pourquoi 0,81 et non 0,97 ? (décomposition, ajout après le résultat de 5.9a)\n\nH13 annonçait au moins 0,90 en (a) ; on obtient 0,81. Explication à **vérifier** : le modèle de (a) n'est entraîné que sur les gabarits du découpage d'**entraînement** de l'étape 3 ; une partie des logs du professeur vient de gabarits qui sont dans la **validation** ou le **test** de SIEVE, donc **inconnus** de ce modèle. Mesure : pour 5 000 logs du fichier p = 0, on regarde **à quel découpage appartient le log de SIEVE_00 le plus proche** (cosinus) et l'exactitude du modèle de (a) selon ce découpage. *Règle écrite avant le résultat :* l'explication tient si l'exactitude est **élevée (au moins 0,90)** quand le plus proche voisin est dans l'entraînement et **nettement plus basse** (au moins 0,15 de moins) quand il est dans la validation ou le test."),
       nbf.v4.new_code_cell(code_e), nbf.v4.new_code_cell(fig_e)]
for k, c in enumerate(new): c.metadata["rev_auto"] = True; nb.cells.insert(i + 1 + k, c)
nbf.write(nb, NB); print("5.9e ajoutée ; cellules :", len(nb.cells))
