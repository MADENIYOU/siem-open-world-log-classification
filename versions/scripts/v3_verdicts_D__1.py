"""Verdicts HD1 à HD7 (règles préinscrites) et résultat RD1 (précédent v1 et actuel v3). Idempotent."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import tp2_journal as J
def last(i): return [e for e in J.entries() if e["id"] == i][-1]
F = "artifacts/results/v3/D_all_units.csv ; D_resume.csv ; D_HD1.csv ; D_HD2.csv ; D_HD4.csv ; D_HD7.csv"
def verdict(i, statut, preuve, note=""):
    if last(i)["statut"] == "préinscrite": J.add(i, "hypothese", last(i)["titre"], last(i)["texte"], justification="Verdict établi avec la règle de décision préinscrite (voir la version précédente).", statut=statut, preuve=preuve + "  Fichiers : " + F, note=note)
verdict("HD1", "confirmée", "Perte de macro-F1 (mots, degré 5, 25 unités) : fautes −0,088 (−16,7 %), homoglyphes −0,254 (−48,2 %), remplissage −0,128 (−24,4 %) ; p Holm < 1e-4 pour les trois.")
verdict("HD2", "confirmée", "Spearman médian 1,0 pour chaque attaque (25/25, 25/25, 24/25 unités avec rho > 0) ; p Holm < 1e-4. Pertes moyennes par degré : fautes 0,010 → 0,088 ; homoglyphes 0,024 → 0,254 ; remplissage 0,007 → 0,128.")
verdict("HD3", "confirmée", "Perte moyenne sur 5 degrés : homoglyphes 0,111 ; remplissage 0,046 ; fautes 0,040. Friedman p = 6,6e-9 ; rangs moyens 3,0 contre 1,56 et 1,44, écarts supérieurs à la différence critique (0,66) ; Nemenyi p < 1e-4 dans les deux comparaisons.")
verdict("HD4", "confirmée", "Perte caractères moins mots : fautes −0,034 (p Holm < 1e-4), homoglyphes −0,087 (p Holm < 1e-4), remplissage +0,005 (p Holm 0,58, pas d'avantage). Les caractères résistent aux déformations de lettres, pas à l'ajout de mots.")
verdict("HD5", "confirmée", "Avec la normalisation UTS #39 officielle, perte résiduelle des homoglyphes 0,000 aux cinq degrés (sans normalisation : 0,024 / 0,044 / 0,089 / 0,142 / 0,254).", "La table officielle ramène exactement le texte attaqué au texte d'origine pour les caractères que l'attaque utilise ; la limite est que l'attaquant pourrait employer des caractères absents de la table.")
verdict("HD6", "confirmée", "Connus rejetés à tort (MSP, mots) par degré d'homoglyphes : 0,061 / 0,075 / 0,115 / 0,164 / 0,268 ; rho médian 1,0, 24/25 unités avec rho > 0, p = 3,1e-6.")
verdict("HD7", "réfutée", "Perte d'AUROC d'inconnu au degré maximal : famille moins MSP = +0,012 (fautes, p Holm 0,13), +0,035 (homoglyphes, p Holm 0,077), +0,047 (remplissage, p Holm 0,077). Le signe est l'inverse de celui prédit : la confiance sur la famille perd PLUS que le MSP.", "Le meilleur détecteur d'inconnus propre (famille) est aussi plus fragile aux attaques ; l'avantage de D12 est donc à confirmer sous attaque, pas à supposer.")
if not J.exists("RD1"):
    J.add("RD1", "resultat", "Bloc D : attaques (précédent v1 et actuel v3)",
          "**Actuel (v3, 25 unités, modèle mots, degré 5 de 5) :** perte de macro-F1 fautes −0,088, homoglyphes −0,254, remplissage −0,128 ; la perte croît avec le degré dans les trois cas ; le modèle caractères perd 0,006 / 0,024 / 0,051 en moyenne sur les degrés ; la normalisation officielle annule les homoglyphes ; les connus rejetés à tort montent de 0,061 à 0,268. **Précédent :** tableau des attaques du notebook v1 (8.6 et 9.12), conservé tel quel.",
          justification="La série v3 reprend les trois attaques sur cinq degrés avec tests appariés ; elle précise et n'infirme pas la série v1 (mêmes sens de variation). Elle ajoute la table officielle et le rejet à tort.", preuve=F)
print(J.render())
