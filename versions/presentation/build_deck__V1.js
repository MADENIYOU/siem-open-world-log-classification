// Soutenance TP2 : « Classer les logs SIEM, reconnaître l'inconnu » (16 diapositives, 16:9).
// Construction : node build_deck.js   (puis post_process.py pour les transitions)
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL_DIR || "";
let applyTheme = null;
try { if (SKILL) applyTheme = require(path.join(SKILL, "scripts", "apply_theme.js")).applyTheme; } catch (e) { /* thème appliqué plus bas si disponible */ }

const FIG = path.join(__dirname, "..", "artifacts", "figures");
const OUT = path.join(__dirname, "Soutenance_SIEM_monde_ouvert.pptx");

// ---- Thème (palette sobre : marine dominant, corail en accent, vert et gris-bleu en soutien)
const NAVY = "0F1B2D", BLUE = "1B365D", INK = "1F2A3C", MUTED = "5A6678", LIGHT = "F3F6FA", LINE = "D5DDE8", CORAL = "D85A30", GREEN = "1D9E75", STEEL = "7F9BBF", AMBER = "BA7517", VIOLET = "534AB7", ICE = "CADCFC";
const THEME = { name: "Soutenance SIEM", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: NAVY, lt1: "FFFFFF", dk2: BLUE, lt2: LIGHT, accent1: CORAL, accent2: GREEN, accent3: STEEL, accent4: AMBER, accent5: VIOLET, accent6: MUTED, hlink: "1B5FA5", folHlink: VIOLET } };
const HEAD = "Cambria", BODY = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";                       // 13,33 x 7,5 pouces
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
pres.title = "Classer les logs SIEM, reconnaître l'inconnu"; pres.author = "Madeniyou Sall"; pres.subject = "Classification hiérarchique de logs SIEM en monde ouvert (SIEVE)";
const W = 13.333, X0 = 0.6, CW = W - 2 * X0;       // marges de 0,6 pouce

// ---- Gabarits de mise en page (layouts)
pres.defineSlideMaster({ title: "TITRE_SOMBRE", background: { color: NAVY }, objects: [] });
pres.defineSlideMaster({ title: "CONTENU", background: { color: "FFFFFF" },
  objects: [
    { text: { text: "Classer les logs SIEM, reconnaître l'inconnu   ·   NLP   ·   ESP / UCAD", options: { x: X0, y: 7.05, w: 9, h: 0.3, fontSize: 10, color: MUTED, fontFace: BODY, margin: 0 } } },
    { placeholder: { options: { name: "kicker", type: "body", x: X0, y: 0.36, w: 9, h: 0.3, fontSize: 12, bold: true, color: CORAL, fontFace: BODY, charSpacing: 3, margin: 0, valign: "middle", align: "left" }, text: "" } },
    { placeholder: { options: { name: "title", type: "title", x: X0, y: 0.66, w: CW, h: 0.85, fontSize: 34, bold: true, color: BLUE, fontFace: HEAD, margin: 0, valign: "top", align: "left" }, text: "" } },
  ],
  slideNumber: { x: 12.2, y: 7.03, w: 0.55, h: 0.3, fontSize: 10, color: MUTED, fontFace: BODY, align: "right" } });

// ---- Outils
let n = 0;
const T = (s, text, o = {}) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: BODY, color: INK, fontSize: 14, valign: "top" }, o));
const rect = (s, x, y, w, h, o = {}) => s.addShape(o.round === false ? pres.ShapeType.rect : pres.ShapeType.roundRect, Object.assign({ x, y, w, h, fill: { color: LIGHT }, line: { color: LINE, width: 0.75 }, rectRadius: 0.08 }, o, { round: undefined }));
const circle = (s, x, y, d, color) => s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color }, line: { color, width: 0 } });
const RATIO = { "00_sota_monde_ferme_ouvert": 1004 / 413, "00_taxonomie": 1890 / 868, "00_rotations": 1960 / 476, "02_gabarits": 1960 / 728, "02_longueurs_et_p": 2380 / 728, "03_fuite_gabarits": 1890 / 644, "05_longueurs_jetons": 1960 / 672, "assets/qr_depot": 1 };
function image(s, name, x, y, w, h, alt) {                                   // image contenue dans une boîte, centrée
  const r = RATIO[name]; let iw = w, ih = w / r; if (ih > h) { ih = h; iw = h * r; }
  const file = name.startsWith("assets/") ? path.join(__dirname, name + ".png") : path.join(FIG, name + ".png");
  s.addImage({ path: file, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: alt || name });
}
function slide(kicker, title, notes) {
  const s = pres.addSlide({ masterName: "CONTENU" }); n += 1;
  s.addText(kicker.toUpperCase(), { placeholder: "kicker" }); s.addText(title, { placeholder: "title" }); if (notes) s.addNotes(notes); return s;
}
function bullets(s, items, x, y, w, h, o = {}) {
  const runs = items.map((t, i) => ({ text: t, options: { bullet: { indent: 16 }, breakLine: i < items.length - 1, paraSpaceAfter: o.gap === undefined ? 6 : o.gap } }));
  T(s, runs, Object.assign({ x, y, w, h, fontSize: 14 }, o.text || {}));
}
const chartBase = (title) => ({ showTitle: true, title, titleFontSize: 13, titleColor: BLUE, titleFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt",
  catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, dataLabelFontSize: 10, catAxisLabelColor: INK, valAxisLabelColor: MUTED, dataLabelColor: INK, valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" }, showValue: true, barGapWidthPct: 45 });

// =====================================================================================================
// 1. Titre
{
  const s = pres.addSlide({ masterName: "TITRE_SOMBRE" }); n += 1;
  T(s, "SOUTENANCE  ·  TRAITEMENT AUTOMATIQUE DU LANGAGE NATUREL", { x: 0.8, y: 0.85, w: 11, h: 0.35, fontSize: 14, bold: true, color: CORAL, charSpacing: 3 });
  T(s, "Classer les logs SIEM,\nreconnaître l'inconnu", { x: 0.8, y: 1.55, w: 6.6, h: 2.4, fontSize: 46, bold: true, color: "FFFFFF", fontFace: HEAD });
  T(s, "Classification hiérarchique en monde ouvert sur le jeu SIEVE : évaluer sans fuite, détecter l'inconnu, résister aux attaques", { x: 0.8, y: 4.2, w: 6.3, h: 1.1, fontSize: 18, color: ICE });
  T(s, "Madeniyou Sall", { x: 0.8, y: 5.85, w: 6, h: 0.4, fontSize: 20, bold: true, color: "FFFFFF" });
  T(s, "ESP / UCAD   ·   Novembre 2026", { x: 0.8, y: 6.3, w: 6, h: 0.35, fontSize: 14, color: STEEL });
  rect(s, 7.55, 1.75, 5.2, 3.15, { fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } });
  image(s, "00_sota_monde_ferme_ouvert", 7.7, 1.9, 4.9, 2.85, "Monde fermé : toute entrée reçoit une classe ; monde ouvert : une entrée trop éloignée est rejetée");
  T(s, "Monde fermé : tout reçoit une classe.\nMonde ouvert : l'inconnu est reconnu comme tel.", { x: 7.55, y: 5.15, w: 5.2, h: 0.8, fontSize: 14, color: ICE, align: "center" });
  s.addNotes("Titre. Une phrase : on veut un classifieur de logs qui sache aussi dire « je ne connais pas cet événement », et on veut l'évaluer honnêtement.");
}

// 2. Contexte
{
  const s = slide("Introduction · Contexte", "Un enjeu qui se chiffre", "Sources : IBM, Cost of a Data Breach Report 2026 (via eSecurity Planet, 30/07/2026) ; Vectra, 2023 State of Threat Detection (enquête auprès de 2 000 analystes SOC) ; Verizon, 2024 Data Breach Investigations Report. Lien avec le projet : les logs sont la matière première du SIEM ; classer chaque événement et signaler ce qu'aucune classe ne décrit est le travail que l'analyste fait à la main.");
  const stats = [["4,99 M$", "coût moyen d'une violation de données, en hausse de 12 % en un an", "IBM, 2026"], ["247 jours", "pour identifier et contenir une violation ; au-delà de 200 jours : 5,65 M$ contre 4,32 M$", "IBM, 2026"],
    ["4 484", "alertes reçues par jour par une équipe SOC, dont 67 % sont ignorées", "Vectra, 2023"], ["10 626", "violations confirmées, sur 30 458 incidents analysés", "Verizon DBIR, 2024"]];
  const cw = 2.85, gap = 0.233;
  stats.forEach((st, i) => { const x = X0 + i * (cw + gap); rect(s, x, 1.75, cw, 3.2);
    T(s, st[0], { x: x + 0.25, y: 1.95, w: cw - 0.5, h: 0.9, fontSize: 34, bold: true, color: CORAL, fontFace: HEAD }); T(s, st[1], { x: x + 0.25, y: 2.95, w: cw - 0.5, h: 1.45, fontSize: 16 }); T(s, st[2], { x: x + 0.25, y: 4.5, w: cw - 0.5, h: 0.3, fontSize: 11, color: MUTED, italic: true }); });
  rect(s, X0, 5.25, CW, 1.5, { fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  T(s, "Pourquoi c'est notre sujet", { x: X0 + 0.35, y: 5.4, w: 4, h: 0.35, fontSize: 14, bold: true, color: CORAL });
  T(s, "Un SIEM rassemble les logs de tout le système d'information. Le goulot d'étranglement est humain : classer chaque événement et repérer celui qu'aucune règle ne décrit. Un classifieur qui sait dire « inconnu » réduit cette charge, à condition de l'évaluer honnêtement.", { x: X0 + 0.35, y: 5.8, w: CW - 0.7, h: 0.9, fontSize: 15, color: "FFFFFF" });
}

// 3. Problématique
{
  const s = slide("Introduction · Problématique", "Reconnaître l'inconnu, sans se tromper soi-même", "Ce qui existe : des classifieurs de logs évalués avec un découpage aléatoire (scores proches de 0,97) ; la détection d'inconnus étudiée surtout sur les images. Ce qui manque : savoir ce que valent ces scores quand les gabarits sont nouveaux, et si l'on sait détecter les classes jamais vues.");
  rect(s, X0, 1.75, 6.55, 2.45, { fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
  T(s, "Question centrale", { x: X0 + 0.3, y: 1.9, w: 5.9, h: 0.3, fontSize: 12, bold: true, color: CORAL, charSpacing: 2 });
  T(s, "Comment classer un événement de sécurité dans une taxonomie à deux niveaux tout en reconnaissant qu'il n'appartient à aucune classe apprise, avec une évaluation qui ne triche pas ?", { x: X0 + 0.3, y: 2.3, w: 5.95, h: 1.8, fontSize: 20, color: "FFFFFF", fontFace: HEAD });
  rect(s, 7.45, 1.75, 5.28, 2.45, { fill: { color: "FFFFFF" } }); image(s, "00_sota_monde_ferme_ouvert", 7.55, 1.85, 5.08, 2.25, "Monde fermé et monde ouvert");
  const q = [["1", "Que valent les scores publiés ?", "Les jeux de logs sont fabriqués à partir de gabarits : un découpage aléatoire laisse fuir les gabarits d'entraînement vers le test."], ["2", "Sait-on détecter les classes jamais vues ?", "Dans un SIEM, l'inconnu est la règle, pas l'exception."], ["3", "Les attaques sur le texte cassent-elles tout ?", "Fautes, lettres d'autres alphabets, mots ajoutés : une défense doit être testée honnêtement."]];
  q.forEach((r, i) => { const x = X0 + i * 4.1; rect(s, x, 4.45, 3.95, 2.1); circle(s, x + 0.25, 4.65, 0.5, CORAL); T(s, r[0], { x: x + 0.25, y: 4.65, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, r[1], { x: x + 0.9, y: 4.65, w: 2.9, h: 0.6, fontSize: 15, bold: true, color: BLUE }); T(s, r[2], { x: x + 0.25, y: 5.35, w: 3.5, h: 1.15, fontSize: 14 }); });
}

// 4. Objectifs
{
  const s = slide("Introduction · Objectifs", "Mesurer honnêtement, pas construire un produit", "Pas de fonctionnalité inventée : le projet fournit un banc d'essai d'évaluation, pas un système déployable. Utilité possible : comparer des classifieurs de logs avec un protocole qui ne fuit pas.");
  rect(s, X0, 1.75, 4.2, 3.45, { fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
  T(s, "Objectif général", { x: X0 + 0.3, y: 1.95, w: 3.6, h: 0.3, fontSize: 12, bold: true, color: CORAL, charSpacing: 2 });
  T(s, "Mesurer jusqu'où un classifieur hiérarchique de logs sait reconnaître l'inconnu et résister aux modifications du texte, avec une évaluation qui ne fuit pas.", { x: X0 + 0.3, y: 2.4, w: 3.65, h: 2.8, fontSize: 18, color: "FFFFFF", fontFace: HEAD });
  const obj = ["Mesurer l'effet de la fuite entre gabarits (découpage aléatoire contre par gabarit)", "Comparer des représentations : creuses, vecteurs de mots, encodeur Transformer", "Comparer huit scores d'inconnu sur cinq rotations de classes masquées", "Tester la robustesse aux attaques textuelles et la valeur réelle des parades", "Livrer un notebook reproductible, avec des règles de décision écrites avant les chiffres"];
  obj.forEach((t, i) => { const y = 1.75 + i * 0.73; circle(s, 5.1, y + 0.04, 0.46, CORAL); T(s, String(i + 1), { x: 5.1, y: y + 0.04, w: 0.46, h: 0.46, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle" }); T(s, t, { x: 5.8, y, w: 6.9, h: 0.6, fontSize: 15, valign: "middle" }); });
  rect(s, X0, 5.6, CW, 1.15);
  T(s, "Ce sur quoi le projet pourrait servir", { x: X0 + 0.3, y: 5.72, w: 6, h: 0.3, fontSize: 12, bold: true, color: CORAL, charSpacing: 1 });
  T(s, "Un protocole et un banc d'essai réutilisables pour comparer des classifieurs de logs et leurs détecteurs d'inconnu, sans surestimer leurs performances. Rien de plus n'est revendiqué.", { x: X0 + 0.3, y: 6.08, w: CW - 0.6, h: 0.6, fontSize: 14 });
}

// 5. État de l'art : vue d'ensemble
{
  const s = slide("État de l'art · Vue d'ensemble", "Six familles de travaux", "73 références dont le résumé ou le texte intégral a été ouvert ; le niveau de vérification est noté pour chacune dans le notebook (section 0.1b) et dans etat_de_l_art/sources_verifiees.md.");
  const fam = [["Jeux de logs", "SIEVE : logs de sécurité synthétiques, 30 classes (Artioli et al., 2025)", CORAL], ["Détection par le score", "Probabilité maximale (Hendrycks et Gimpel, 2017), énergie (Liu et al., 2020)", BLUE],
    ["Détection par la distance", "Mahalanobis (Lee et al., 2018), kNN (Sun et al., 2022), OpenMax (Bendale et Boult, 2016)", GREEN], ["Hiérarchie", "Probabilité famille × classe, repli sur la famille (Linderman et al., 2022)", VIOLET],
    ["Robustesse du texte", "Fautes de frappe, homoglyphes (Unicode UTS #39), entraînement adversarial", AMBER], ["Fiabilité de l'évaluation", "Calibration (Guo et al., 2017), lien fermé–ouvert (Vaze et al., 2022), bootstrap par grappes", STEEL]];
  fam.forEach((f, i) => { const x = X0 + (i % 3) * 4.1, y = 1.75 + Math.floor(i / 3) * 2.2; rect(s, x, y, 3.95, 2.05); circle(s, x + 0.25, y + 0.25, 0.3, f[2]);
    T(s, f[0], { x: x + 0.7, y: y + 0.2, w: 3.1, h: 0.4, fontSize: 16, bold: true, color: BLUE, valign: "middle" }); T(s, f[1], { x: x + 0.25, y: y + 0.8, w: 3.5, h: 1.15, fontSize: 15 }); });
  rect(s, X0, 6.2, CW, 0.6, { fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  T(s, "73 références vérifiées (page ouverte, niveau de vérification noté)   ·   registre de 99 affirmations chiffrées sourcées", { x: X0 + 0.3, y: 6.2, w: CW - 0.6, h: 0.6, fontSize: 14, color: "FFFFFF", valign: "middle", bold: true });
}

// 6. État de l'art : analyse et propositions
{
  const s = slide("État de l'art · Analyse et propositions", "Ce qui marche, ce qui bloque, ce que l'on propose", "Limite commune : la plupart des évaluations utilisent un découpage aléatoire, rapportent peu d'intervalles de confiance et testent les défenses avec la table de l'attaquant. Nos propositions répondent à ces trois points.");
  const H = (t) => ({ text: t, options: { bold: true, color: "FFFFFF", fill: { color: BLUE }, fontSize: 13, fontFace: BODY, valign: "middle" } });
  const C = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 12, fontFace: BODY, color: INK, valign: "middle" }, o) });
  const rows = [[H("Famille"), H("Avantages"), H("Inconvénients et limites")],
    [C("Scores de sortie (MSP, énergie)", { bold: true }), C("Simples, sans réentraînement"), C("Confiance mal calibrée ; aveugles à l'inconnu proche d'une classe connue")],
    [C("Distances (Mahalanobis, kNN, OpenMax)", { bold: true }), C("Exploitent la géométrie des vecteurs"), C("Dépendent de la représentation ; coût de calcul")],
    [C("Hiérarchie, repli sur la famille", { bold: true }), C("Erreurs attendues moins graves"), C("Cumule deux erreurs ; gain rarement mesuré avec des intervalles")],
    [C("Défenses du texte", { bold: true }), C("Efficaces contre l'attaque connue"), C("Ne généralisent pas ; trompeuses si testées avec la table de l'attaquant")]];
  s.addTable(rows, { x: X0, y: 1.75, w: 7.7, colW: [2.4, 2.3, 3.0], rowH: [0.45, 0.85, 0.85, 0.85, 0.85], border: { type: "solid", color: LINE, pt: 0.75 }, fill: { color: "FFFFFF" }, margin: [0.05, 0.1, 0.05, 0.1], autoPage: false });
  T(s, "Limite commune : découpage aléatoire, peu d'intervalles de confiance, défenses testées contre leur propre table.", { x: X0, y: 6.15, w: 7.7, h: 0.6, fontSize: 13, italic: true, color: MUTED });
  rect(s, 8.55, 1.75, 4.18, 5.0, { fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
  T(s, "Nos propositions", { x: 8.85, y: 1.95, w: 3.6, h: 0.3, fontSize: 12, bold: true, color: CORAL, charSpacing: 2 });
  bullets(s, ["Découpage par gabarit et test scellé et journalisé", "Règles écrites avant les chiffres ; réglages sans jamais regarder les classes masquées", "Scores comparés sur les sorties et sur les vecteurs de l'encodeur", "Défenses testées avec une autre table que celle de l'attaque"], 8.85, 2.45, 3.65, 4.1, { gap: 14, text: { color: "FFFFFF", fontSize: 16 } });
}

// 7. Matériel
{
  const s = slide("Matériel", "Données et ressources", "Exemple de log : classe authentication-failed (SIEVE_00). Les 440 logs réels du CDS ne faisaient pas partie de l'archive reçue : l'expérience de transfert E5 n'a pas pu être faite.");
  const it = [["600 000 logs", "SIEVE : 6 versions de 100 000, perturbation p de 0 à 0,5, 30 classes équilibrées, 440 gabarits", CORAL], ["6 × 35 000", "Fichiers du professeur : mêmes gabarits, valeurs nouvelles (contrôle de fuite)", GREEN], ["8 familles", "Taxonomie à deux niveaux adossée à ECS, hypothèse de démonstration", BLUE],
    ["1 447", "Caractères confondables de la table Unicode UTS #39 (v18.0.0)", VIOLET], ["DistilBERT", "Encodeur pré-entraîné sans casse ; vecteurs GloVe 100 d", AMBER], ["440 logs réels", "CDS : non fournis, transfert E5 impossible", MUTED]];
  it.forEach((f, i) => { const x = X0 + (i % 3) * 4.1, y = 1.75 + Math.floor(i / 3) * 1.95; rect(s, x, y, 3.95, 1.8); T(s, f[0], { x: x + 0.25, y: y + 0.15, w: 3.5, h: 0.55, fontSize: 26, bold: true, color: f[2], fontFace: HEAD }); T(s, f[1], { x: x + 0.25, y: y + 0.8, w: 3.5, h: 0.95, fontSize: 14 }); });
  rect(s, X0, 5.75, CW, 1.05, { fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  T(s, "Exemple de log (classe authentication-failed)", { x: X0 + 0.3, y: 5.85, w: 6, h: 0.25, fontSize: 11, bold: true, color: CORAL });
  T(s, '[Fri Mar 23 00:47:56 1979] [error] [client 91.192.239.161] user angeladavis: authentication failure for "/west/local.tiff/every": Password Mismatch', { x: X0 + 0.3, y: 6.15, w: CW - 0.6, h: 0.55, fontSize: 13, color: "FFFFFF", fontFace: "Courier New" });
}

// 8. Méthodes
{
  const s = slide("Méthodes", "De la représentation à la décision", "Le seuil de rejet est calé sur les seuls logs connus de validation (95 % acceptés). Les classes masquées servent seulement à mesurer, jamais à régler.");
  const cols = [["Représenter", ["Creuses : sac de mots, TF-IDF, n-grammes", "Vecteurs de mots : Word2Vec, FastText, GloVe", "Contextuelle : DistilBERT"], CORAL], ["Classer", ["Plat : une tête sur les classes", "Hiérarchique : p(famille) × p(classe | famille)", "Encodeur à deux têtes"], BLUE],
    ["Détecter l'inconnu", ["Scores : MSP, énergie, prototype, ensemble", "Distances : Mahalanobis, kNN, OpenMax", "Dropout Monte-Carlo ; seuil à 95 % des connus"], GREEN], ["Évaluer", ["Découpage par gabarit, test scellé", "5 rotations de 6 classes masquées", "Intervalles par gabarit, règles écrites d'avance"], VIOLET]];
  cols.forEach((c, i) => { const x = X0 + i * 3.1, w = 2.85; rect(s, x, 1.75, w, 3.55); circle(s, x + 0.25, 1.95, 0.4, c[2]); T(s, String(i + 1), { x: x + 0.25, y: 1.95, w: 0.4, h: 0.4, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, c[0], { x: x + 0.8, y: 1.95, w: w - 1, h: 0.4, fontSize: 17, bold: true, color: BLUE, valign: "middle" }); bullets(s, c[1], x + 0.25, 2.6, w - 0.45, 2.6, { gap: 12, text: { fontSize: 15 } });
    if (i < 3) s.addShape(pres.ShapeType.rightArrow, { x: x + w + 0.02, y: 3.35, w: 0.22, h: 0.3, fill: { color: STEEL }, line: { color: STEEL, width: 0 } }); });
  rect(s, X0, 5.55, CW, 1.2, { fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
  T(s, "Robustesse et fiabilité", { x: X0 + 0.3, y: 5.68, w: 5, h: 0.3, fontSize: 12, bold: true, color: CORAL, charSpacing: 2 });
  T(s, "Attaques : fautes de frappe, homoglyphes, mots ajoutés   ·   Parades : normalisation Unicode UTS #39, entraînement adversarial   ·   Calibration par température", { x: X0 + 0.3, y: 6.05, w: CW - 0.6, h: 0.6, fontSize: 15, color: "FFFFFF" });
}

// 9. Présentation des données
{
  const s = slide("Présentation des données", "Ce que contiennent les données", "Figures du notebook : taxonomie des 30 classes en 8 familles ; rotations de classes masquées ; validation de la reconstruction des gabarits (311 retrouvés sur 440) et effet de p ; fuite entre gabarits selon le découpage ; longueur des logs en jetons.");
  const st = [["600 000", "logs"], ["30", "classes"], ["440", "gabarits (311 retrouvés)"], ["8", "familles"], ["5 × 6", "classes masquées"]];
  st.forEach((a, i) => { const x = X0 + i * 2.46; rect(s, x, 1.65, 2.3, 0.7, { fill: { color: BLUE }, line: { color: BLUE, width: 0 } }); T(s, a[0], { x: x + 0.15, y: 1.65, w: 1.3, h: 0.7, fontSize: 20, bold: true, color: "FFFFFF", fontFace: HEAD, valign: "middle" }); T(s, a[1], { x: x + 1.4, y: 1.65, w: 0.85, h: 0.7, fontSize: 11, color: ICE, valign: "middle" }); });
  const g = [["00_taxonomie", "Taxonomie : 30 classes en 8 familles"], ["00_rotations", "Cinq rotations : six classes masquées chacune"], ["02_gabarits", "Gabarits reconstruits (311 sur 440) et effet de p"], ["02_longueurs_et_p", "Longueur des logs et perturbation p"], ["03_fuite_gabarits", "Fuite entre gabarits : voisins proches"], ["05_longueurs_jetons", "Longueur en jetons de l'encodeur"]];
  g.forEach((f, i) => { const x = X0 + (i % 3) * 4.1, y = 2.5 + Math.floor(i / 3) * 2.3; rect(s, x, y, 3.95, 2.2, { fill: { color: "FFFFFF" } }); image(s, f[0], x + 0.08, y + 0.06, 3.79, 1.78, f[1]); T(s, f[1], { x: x + 0.1, y: y + 1.88, w: 3.75, h: 0.28, fontSize: 11, color: MUTED, align: "center" }); });
}

// 10. Librairies
{
  const s = slide("Librairies utilisées", "Python 3.12 et un socle scientifique", "Versions figées dans requirements.txt du dépôt.");
  const L = [["Données et calcul", ["numpy 2.5.4", "pandas 3.1.1", "scipy 1.18.1"], BLUE], ["Apprentissage automatique", ["scikit-learn 1.9.1", "joblib 1.6.0"], CORAL], ["Texte et vecteurs de mots", ["gensim 4.4.0", "nltk 3.10.4"], GREEN],
    ["Apprentissage profond", ["PyTorch 2.15.0", "Transformers 5.22.1", "tokenizers 0.23.3"], VIOLET], ["Visualisation", ["matplotlib 3.11.2"], AMBER], ["Exécution et reproductibilité", ["ipykernel 7.4.0", "nbclient 0.11.0", "nbformat 5.11.1"], STEEL]];
  L.forEach((f, i) => { const x = X0 + (i % 3) * 4.1, y = 1.75 + Math.floor(i / 3) * 2.5; rect(s, x, y, 3.95, 2.3); circle(s, x + 0.25, y + 0.25, 0.28, f[2]); T(s, f[0], { x: x + 0.65, y: y + 0.2, w: 3.2, h: 0.4, fontSize: 16, bold: true, color: BLUE, valign: "middle" });
    f[1].forEach((l, j) => { rect(s, x + 0.25, y + 0.85 + j * 0.46, 2.6, 0.36, { fill: { color: "FFFFFF" }, rectRadius: 0.06 }); T(s, l, { x: x + 0.4, y: y + 0.85 + j * 0.46, w: 2.4, h: 0.36, fontSize: 13, valign: "middle", fontFace: "Courier New" }); }); });
}

// 11. Environnement d'exécution
{
  const s = slide("Environnement d'exécution", "Calcul réparti entre trois environnements", "Les calculs longs sont reprenables : cache par modèle, rotation et graine, points de reprise pendant l'entraînement. Le notebook complet se rejoue en environ 13 minutes avec les caches.");
  const E = [["Mac, puce M3 Pro", ["Modèles linéaires, vecteurs de mots", "Encodeur : rotations 3 à 5 et graines 42, 43, 44", "GPU Apple (MPS), attention classique"], CORAL], ["Google Colab", ["GPU T4", "Encodeur : première validation, rotations 1 et 2", "Reprise limitée par le quota de GPU"], GREEN], ["Notebook et dépôt", ["Python 3.12, Jupyter, exécution par nbclient", "Git et GitHub : dépôt public", "Données SIEVE non redistribuées"], BLUE]];
  E.forEach((e, i) => { const x = X0 + i * 4.1; rect(s, x, 1.75, 3.95, 3.0); circle(s, x + 0.25, 1.95, 0.4, e[2]); T(s, e[0], { x: x + 0.8, y: 1.95, w: 3, h: 0.4, fontSize: 17, bold: true, color: BLUE, valign: "middle" }); bullets(s, e[1], x + 0.25, 2.6, 3.5, 2.1, { gap: 10, text: { fontSize: 15 } }); });
  const k = [["13 à 20 min", "par encodeur (2 époques)"], ["15 modèles", "3 graines × 5 rotations"], ["≈ 13 min", "pour rejouer tout le notebook"], ["Reprise", "automatique après interruption"]];
  k.forEach((a, i) => { const x = X0 + i * 3.1; rect(s, x, 5.2, 2.95, 1.55, { fill: { color: NAVY }, line: { color: NAVY, width: 0 } }); T(s, a[0], { x: x + 0.2, y: 5.4, w: 2.55, h: 0.6, fontSize: 24, bold: true, color: CORAL, fontFace: HEAD }); T(s, a[1], { x: x + 0.2, y: 6.1, w: 2.55, h: 0.55, fontSize: 13, color: "FFFFFF" }); });
}

// 12. Conception : pipeline
{
  const s = slide("Conception · Pipeline utilisé", "Onze étapes, de la question à la conclusion", "Chaque étape est dans le notebook avec ses décisions justifiées, ses analyses et ses figures. L'étape 3 (découpage) est celle qui change le plus les conclusions.");
  const P = [["0", "Cadrage", "Question, hypothèses H1 à H15, critères de succès"], ["1", "Données", "Acquisition et audit du format"], ["2", "Exploration", "Classes proches, gabarits, effet de p"], ["3", "Découpage", "Par gabarit, test scellé, protocoles P0 à P3"], ["4", "Prétraitement", "Pipeline de texte, 10 variantes"], ["5", "Représentations", "Creuses, vecteurs de mots, encodeur"],
    ["6", "Modèles", "Plat, hiérarchique, huit scores d'inconnu"], ["7", "Évaluation", "Test scellé : E1 à E3"], ["8", "Robustesse", "Attaques textuelles, E4"], ["9", "Amélioration", "Parades, calibration"], ["10", "Conclusion", "Registre de 99 affirmations, limites"]];
  P.forEach((p, i) => { const row = i < 6 ? 0 : 1, col = i < 6 ? i : i - 6, w = 1.9, x = X0 + col * 2.04 + (row ? 1.02 : 0), y = 1.75 + row * 2.45;
    rect(s, x, y, w, 2.2, { fill: { color: i === 3 ? "FDEFE9" : LIGHT }, line: { color: i === 3 ? CORAL : LINE, width: i === 3 ? 1.5 : 0.75 } }); circle(s, x + 0.15, y + 0.17, 0.42, i === 3 ? CORAL : BLUE); T(s, p[0], { x: x + 0.15, y: y + 0.17, w: 0.42, h: 0.42, fontSize: 14, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, p[1], { x: x + 0.15, y: y + 0.72, w: w - 0.3, h: 0.4, fontSize: 14, bold: true, color: BLUE }); T(s, p[2], { x: x + 0.15, y: y + 1.15, w: w - 0.3, h: 1.0, fontSize: 13 });
    if (col < (row ? 4 : 5)) s.addShape(pres.ShapeType.rightArrow, { x: x + w + 0.0, y: y + 1.05, w: 0.14, h: 0.22, fill: { color: STEEL }, line: { color: STEEL, width: 0 } }); });
  T(s, "Encadré : l'étape 3 (découpage par gabarit et test scellé) change le plus les conclusions.", { x: X0, y: 6.5, w: 9, h: 0.3, fontSize: 12, color: MUTED, italic: true });
}

// 13. Conception : résultats
{
  const s = slide("Conception · Présentation et analyse des résultats", "Ce que les mesures montrent", "Découpage : P0 aléatoire 0,987 ; P1 0,422 ; P2 0,507 ; P3 0,511 ; test scellé 0,483 (macro-F1 du palier A). Détection : TF-IDF MSP 0,728 (validation) puis 0,599 (test) ; encodeur MSP 0,548 et Mahalanobis sur ses vecteurs 0,605 (3 graines). Attaques à intensité forte, perte relative de F1. Défense : 0,108 sans défense, 0,000 contre sa propre table, 0,087 contre la table officielle, 0,001 avec la table officielle complète.");
  const cw = 6.0, ch = 2.2, X1 = X0 + cw + 0.13;
  s.addChart(pres.charts.BAR, [{ name: "macro-F1", labels: ["Aléatoire", "Par gabarit", "Groupes", "Imbriquée", "Test scellé"], values: [0.987, 0.422, 0.507, 0.511, 0.483] }], Object.assign(chartBase("Fuite : macro-F1 selon le découpage"), { x: X0, y: 1.65, w: cw, h: ch, barDir: "col", chartColors: [CORAL, STEEL, STEEL, STEEL, BLUE], valAxisMaxVal: 1, valAxisMinVal: 0, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", showLegend: false }));
  s.addChart(pres.charts.BAR, [{ name: "AUROC", labels: ["TF-IDF val.", "TF-IDF test", "Encodeur MSP", "Encodeur + Mahalanobis"], values: [0.728, 0.599, 0.548, 0.605] }], Object.assign(chartBase("Détection d'inconnus : AUROC (0,5 = hasard)"), { x: X1, y: 1.65, w: cw, h: ch, barDir: "col", chartColors: [STEEL, BLUE, STEEL, GREEN], valAxisMaxVal: 1, valAxisMinVal: 0.4, valAxisMajorUnit: 0.2, dataLabelFormatCode: "0.00", showLegend: false }));
  rect(s, X0, 6.28, CW, 0.62, { fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
  T(s, "Le découpage fait l'essentiel de l'écart   ·   la détection reste faible   ·   une défense se teste contre une autre table", { x: X0 + 0.3, y: 6.28, w: CW - 0.6, h: 0.62, fontSize: 14, bold: true, color: "FFFFFF", valign: "middle" });
  s.addChart(pres.charts.BAR, [{ name: "Mots", labels: ["Fautes", "Homoglyphes", "Mots ajoutés"], values: [7.8, 21.5, 12.5] }, { name: "Caractères", labels: ["Fautes", "Homoglyphes", "Mots ajoutés"], values: [4.0, 10.6, 14.4] }], Object.assign(chartBase("Attaques fortes : perte relative de F1 (%)"), { x: X0, y: 3.95, w: cw, h: ch, barDir: "col", chartColors: [CORAL, STEEL], valAxisMinVal: 0, dataLabelFormatCode: "0.0", showLegend: true, legendPos: "b", legendFontSize: 10, legendColor: INK }));
  s.addChart(pres.charts.BAR, [{ name: "perte", labels: ["Sans défense", "Table maison\n(sa propre attaque)", "Table maison\n(table officielle)", "Table officielle\ncomplète"], values: [10.8, 0.0, 8.7, 0.1] }], Object.assign(chartBase("Défense homoglyphes : perte relative de F1 (%)"), { x: X1, y: 3.95, w: cw, h: ch, barDir: "col", chartColors: [STEEL, GREEN, CORAL, GREEN], valAxisMinVal: 0, dataLabelFormatCode: "0.0", showLegend: false }));
}

// 14. Limites de la conception
{
  const s = slide("Conception · Limites de la conception", "Ce que ce travail ne permet pas de conclure", "Les limites sont aussi dans le README du dépôt et la section 10.6 du notebook.");
  const L = [["Données synthétiques", "SIEVE vient de 440 gabarits ; 311 ont été reconstruits, pas fournis.", CORAL], ["Taxonomie non validée", "Les 8 familles sont une hypothèse de démonstration, sans expert SIEM.", BLUE], ["Puissance statistique", "36 gabarits en validation, 45 au test : un écart sous 0,05 est indétectable.", GREEN],
    ["Peu de graines", "Trois graines pour l'encodeur, une pour la plupart des autres modèles.", VIOLET], ["Test déjà ouvert", "Les scores ajoutés ensuite sont mesurés sur la validation, sans test neuf.", AMBER], ["Hors de portée", "Pas de logs réels (transfert E5) ; attaques surtout non adaptatives.", MUTED]];
  L.forEach((l, i) => { const x = X0 + (i % 3) * 4.1, y = 1.75 + Math.floor(i / 3) * 2.55; rect(s, x, y, 3.95, 2.4); circle(s, x + 0.25, y + 0.25, 0.5, l[2]); T(s, String(i + 1), { x: x + 0.25, y: y + 0.25, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    T(s, l[0], { x: x + 0.9, y: y + 0.25, w: 2.9, h: 0.5, fontSize: 16, bold: true, color: BLUE, valign: "middle" }); T(s, l[1], { x: x + 0.25, y: y + 0.95, w: 3.5, h: 1.35, fontSize: 15 }); });
}

// 15. Conclusion
{
  const s = slide("Conclusion", "Ce qu'il faut retenir de ce travail", "Perspectives réalistes : validation de la taxonomie par un expert SIEM, tests sur logs réels, plus de graines, covariance par classe, attaques adaptatives.");
  const C3 = [["À retenir", CORAL, ["Le découpage compte plus que le modèle : de 0,97 à 0,46 de macro-F1", "Détecter l'inconnu reste difficile : AUROC de 0,60 au test", "Sur l'encodeur affiné, Mahalanobis bat le MSP (+0,057)", "Une défense se teste avec une autre table que celle de l'attaque"]],
    ["Limites", AMBER, ["Taxonomie non validée, gabarits reconstruits", "Trois graines, peu de gabarits de test", "Pas de logs réels : transfert E5 non fait"]], ["Perspectives", GREEN, ["Valider la taxonomie avec un expert SIEM", "Tester sur des logs réels (CDS)", "Plus de graines, covariance par classe, attaques adaptatives"]]];
  C3.forEach((c, i) => { const x = X0 + i * 4.1; rect(s, x, 1.75, 3.95, 5.0, { fill: { color: i === 0 ? BLUE : LIGHT }, line: { color: i === 0 ? BLUE : LINE, width: i === 0 ? 0 : 0.75 } }); circle(s, x + 0.25, 1.98, 0.3, c[1]);
    T(s, c[0], { x: x + 0.7, y: 1.95, w: 3, h: 0.36, fontSize: 18, bold: true, color: i === 0 ? "FFFFFF" : BLUE, valign: "middle" }); bullets(s, c[2], x + 0.25, 2.6, 3.5, 4.0, { gap: 14, text: { fontSize: 16, color: i === 0 ? "FFFFFF" : INK } }); });
}

// 16. Merci
{
  const s = pres.addSlide({ masterName: "TITRE_SOMBRE" }); n += 1;
  T(s, "Merci", { x: 0.8, y: 1.7, w: 7, h: 1.2, fontSize: 64, bold: true, color: "FFFFFF", fontFace: HEAD });
  T(s, "Questions", { x: 0.8, y: 3.0, w: 7, h: 0.7, fontSize: 28, color: CORAL, fontFace: HEAD });
  T(s, "Notebook, résultats, figures et code :\ngithub.com/MADENIYOU/siem-open-world-log-classification", { x: 0.8, y: 4.4, w: 7.2, h: 1, fontSize: 16, color: ICE });
  rect(s, 8.7, 1.8, 3.6, 3.6, { fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } }); image(s, "assets/qr_depot", 8.85, 1.95, 3.3, 3.3, "Code QR du dépôt GitHub");
  T(s, "Dépôt public", { x: 8.7, y: 5.55, w: 3.6, h: 0.35, fontSize: 14, color: STEEL, align: "center" });
  s.addNotes("Clôture. Le dépôt contient le notebook exécuté, les résultats chiffrés et les figures ; les données SIEVE ne sont pas redistribuées.");
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (applyTheme) await applyTheme(OUT, THEME); else console.log("apply_theme.js non chargé (définir PPTX_SKILL_DIR)");
  console.log("écrit :", OUT, "—", n, "diapositives");
})();
