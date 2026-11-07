// Soutenance TP2 : « Classer les logs SIEM, reconnaître l'inconnu » (17 diapositives, 16:9), version 2.
// Refonte pour éviter les marques d'une présentation générée par IA (voir ~/.claude/skills/soutenance-pptx/references/indices-ia.md) :
// titres qui énoncent le message, une seule couleur d'accent, pas de cartes répétées ni d'étiquettes en capitales, compositions variées,
// citations [n] numérotées par ordre d'apparition et diapositive finale de références.
const path = require("path");
const pptxgen = require("pptxgenjs");
const SKILL = process.env.PPTX_SKILL_DIR || "";
let applyTheme = null;
try { if (SKILL) applyTheme = require(path.join(SKILL, "scripts", "apply_theme.js")).applyTheme; } catch (e) { /* thème appliqué plus bas si disponible */ }

const FIG = path.join(__dirname, "..", "artifacts", "figures");
const OUT = path.join(__dirname, "Soutenance_SIEM_monde_ouvert.pptx");

// ---- Palette : marine dominant, UNE couleur d'accent (corail), bleu acier réservé aux séries secondaires des graphiques
const NAVY = "0F1B2D", BLUE = "1B365D", INK = "1F2A3C", MUTED = "5F6B7C", LINE = "D5DDE8", PANEL = "F3F6FA", CORAL = "D85A30", STEEL = "7F9BBF", ICE = "CADCFC";
const THEME = { name: "Soutenance SIEM", headFontFace: "Cambria", bodyFontFace: "Calibri",
  colors: { dk1: NAVY, lt1: "FFFFFF", dk2: BLUE, lt2: PANEL, accent1: CORAL, accent2: STEEL, accent3: MUTED, accent4: BLUE, accent5: ICE, accent6: LINE, hlink: BLUE, folHlink: MUTED } };
const HEAD = "Cambria", BODY = "Calibri", MONO = "Courier New";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";                       // 13,33 x 7,5 pouces
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
pres.title = "Classer les logs SIEM, reconnaître l'inconnu"; pres.author = "Mouhamadou Madeniyou SALL"; pres.subject = "Classification hiérarchique de logs SIEM en monde ouvert (SIEVE)";
const W = 13.333, X0 = 0.7, CW = W - 2 * X0;

// ---- Gabarits : titre sombre, contenu (titre = message, à gauche, 30 pt ; numéro de diapositive ; pas d'étiquette décorative)
pres.defineSlideMaster({ title: "TITRE_SOMBRE", background: { color: NAVY }, objects: [] });
pres.defineSlideMaster({ title: "CONTENU", background: { color: "FFFFFF" },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: X0, y: 0.4, w: CW, h: 0.6, fontSize: 28, bold: true, color: BLUE, fontFace: HEAD, margin: 0, valign: "top", align: "left" }, text: "" } }],
  slideNumber: { x: 12.1, y: 7.03, w: 0.55, h: 0.3, fontSize: 10, color: MUTED, fontFace: BODY, align: "right" } });

// ---- Références : numérotées par ordre de première apparition dans les diapositives
const DEFS = {
  ibm: "IBM. Cost of a Data Breach Report 2026. Synthèse : eSecurity Planet, 30 juillet 2026. esecurityplanet.com/cybersecurity/ibm-2026-cost-of-a-data-breach-report-key-findings",
  vectra: "Vectra AI. 2023 State of Threat Detection (enquête auprès de 2 000 analystes SOC). vectra.ai/resources/2023-state-of-threat-detection",
  verizon: "Verizon. 2024 Data Breach Investigations Report. verizon.com/business/resources/reports/dbir/2024",
  sieve: "Artioli, Dentamaro, Galantucci, Magrì, Pellegrini, Semeraro. SIEVE: Generating a cybersecurity log dataset collection for SIEM event classification. Computer Networks 266, 111330, 2025. doi:10.1016/j.comnet.2025.111330",
  msp: "Hendrycks, Gimpel. A Baseline for Detecting Misclassified and Out-of-Distribution Examples in Neural Networks. ICLR 2017. arXiv:1610.02136",
  energy: "Liu, Wang, Owens, Li. Energy-based Out-of-distribution Detection. NeurIPS 2020. arXiv:2010.03759",
  maha: "Lee, Lee, Lee, Shin. A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks. NeurIPS 2018. arXiv:1807.03888",
  knn: "Sun, Ming, Zhu, Li. Out-of-Distribution Detection with Deep Nearest Neighbors. ICML 2022. arXiv:2204.06507",
  openmax: "Bendale, Boult. Towards Open Set Deep Networks. CVPR 2016. arXiv:1511.06233",
  lind: "Linderman, Zhang, Inkawhich, Li, Chen. Fine-grain Inference on Out-of-Distribution Data with Hierarchical Classification. arXiv:2209.04493, 2022",
  uts39: "Unicode Consortium. Unicode Technical Standard #39 : Unicode Security Mechanisms, version 18.0.0. unicode.org/reports/tr39",
  guo: "Guo, Pleiss, Sun, Weinberger. On Calibration of Modern Neural Networks. ICML 2017. arXiv:1706.04599",
  vaze: "Vaze, Han, Vedaldi, Zisserman. Open-Set Recognition: a Good Closed-Set Classifier is All You Need? ICLR 2022. arXiv:2110.06207",
  podolskiy: "Podolskiy, Lipin, Bout, Artemova, Piontkovskaya. Revisiting Mahalanobis Distance for Transformer-Based Out-of-Domain Detection. AAAI 2021. arXiv:2101.03778",
  distil: "Sanh, Debut, Chaumond, Wolf. DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. arXiv:1910.01108, 2019",
  field: "Field, Welsh. Bootstrapping clustered data. Journal of the Royal Statistical Society B 69(3), 369-390, 2007. doi:10.1111/j.1467-9868.2007.00593.x",
  biblio: "Recherche bibliographique du projet (notebook, section 0.1b ; sources_verifiees.md du dépôt), 5 novembre 2026 : 73 références dont la page a été ouverte.",
};
const REFN = {}; const ORDER = []; const cite = (k) => { if (!DEFS[k]) throw new Error("référence inconnue " + k); if (!REFN[k]) { ORDER.push(k); REFN[k] = ORDER.length; } return REFN[k]; };
const C = (k) => ({ cite: k });                       // marqueur de citation à l'intérieur d'un paragraphe

// ---- Outils
const T = (s, text, o = {}) => s.addText(text, Object.assign({ isTextBox: true, margin: 0, fontFace: BODY, color: INK, fontSize: 14, valign: "top" }, o));
function runs(paras, base = {}) {                      // paragraphes = tableaux de morceaux (texte, {b:texte gras}, C(clé))
  const out = [];
  paras.forEach((p, i) => { const parts = Array.isArray(p) ? p : [p];
    parts.forEach((part, j) => { const last = j === parts.length - 1, brk = last && i < paras.length - 1;
      if (typeof part === "string") out.push({ text: part, options: Object.assign({}, base.run, { breakLine: brk, paraSpaceAfter: base.gap === undefined ? 6 : base.gap }) });
      else if (part.cite) out.push({ text: `[${cite(part.cite)}]`, options: { color: CORAL, fontSize: 12, bold: true, breakLine: brk, paraSpaceAfter: base.gap === undefined ? 6 : base.gap } });
      else out.push({ text: part.b, options: Object.assign({}, base.run, { bold: true, breakLine: brk, paraSpaceAfter: base.gap === undefined ? 6 : base.gap }) }); }); });
  return out;
}
const P = (s, paras, o = {}) => T(s, runs(paras, { gap: o.gap, run: o.run }), o);
const hline = (s, x, y, w, color = LINE) => s.addShape(pres.ShapeType.line, { x, y, w, h: 0, line: { color, width: 0.75 } });
const RATIO = { "00_sota_monde_ferme_ouvert": 1004 / 413, "00_taxonomie": 1890 / 868, "00_rotations": 1960 / 476, "02_gabarits": 1960 / 728, "02_longueurs_et_p": 2380 / 728, "03_fuite_gabarits": 1890 / 644, "05_longueurs_jetons": 1960 / 672, "assets/qr_depot": 1 };
function image(s, name, x, y, w, h, alt) {
  const r = RATIO[name]; let iw = w, ih = w / r; if (ih > h) { ih = h; iw = h * r; }
  const file = name.startsWith("assets/") ? path.join(__dirname, name + ".png") : path.join(FIG, name + ".png");
  s.addImage({ path: file, x: x + (w - iw) / 2, y: y + (h - ih) / 2, w: iw, h: ih, altText: alt || name });
}
let n = 0;
function slide(title, message, notes) {                // title = intitulé du point demandé ; message = phrase qui énonce le message de la diapositive
  const s = pres.addSlide({ masterName: "CONTENU" }); n += 1;
  s.addText(title, { placeholder: "title" });
  T(s, message, { x: X0, y: 1.02, w: CW, h: 0.75, fontSize: 18, color: INK });
  if (notes) s.addNotes(notes); return s;
}
const dark = (s, x, y, w, h) => s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
const chartBase = (title) => ({ showTitle: true, title, titleFontSize: 13, titleColor: BLUE, titleFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt",
  catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, dataLabelFontSize: 10, catAxisLabelColor: INK, valAxisLabelColor: MUTED, dataLabelColor: INK, valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" }, showValue: true, barGapWidthPct: 45 });
const lab = (s, text, x, y, w) => T(s, text, { x, y, w, h: 0.3, fontSize: 13, bold: true, color: BLUE });   // petit intitulé de bloc, en casse de phrase

const enclair = (s, text, y = 1.42) => T(s, [{ text: "En clair : ", options: { bold: true, color: BLUE } }, { text, options: { color: MUTED } }], { x: X0, y, w: CW, h: 0.45, fontSize: 14 });

// =====================================================================================================
// 1. Titre : schéma monde fermé / monde ouvert dessiné (porte l'idée du sujet)
{
  const s = pres.addSlide({ masterName: "TITRE_SOMBRE" }); n += 1;
  T(s, "Soutenance  ·  Traitement automatique du langage naturel", { x: 0.8, y: 0.9, w: 6.5, h: 0.35, fontSize: 14, color: STEEL });
  T(s, "Classer les logs SIEM,\nreconnaître l'inconnu", { x: 0.8, y: 1.6, w: 6.5, h: 2.3, fontSize: 46, bold: true, color: "FFFFFF", fontFace: HEAD });
  T(s, "Apprendre à un programme à classer des journaux de sécurité, et à dire « inconnu » quand il ne reconnaît pas", { x: 0.8, y: 4.1, w: 6.2, h: 0.9, fontSize: 18, color: ICE });
  T(s, "SIEM : logiciel qui rassemble les journaux (logs) d'une entreprise pour repérer les attaques. Données : jeu SIEVE.", { x: 0.8, y: 5.05, w: 6.2, h: 0.65, fontSize: 13, color: STEEL });
  T(s, "Mouhamadou Madeniyou SALL", { x: 0.8, y: 5.85, w: 8, h: 0.4, fontSize: 20, bold: true, color: "FFFFFF" });
  T(s, "ESP / UCAD   ·   Novembre 2026", { x: 0.8, y: 6.3, w: 6, h: 0.35, fontSize: 14, color: STEEL });
  const ring = (cx, cy, d, dash) => s.addShape(pres.ShapeType.ellipse, { x: cx - d / 2, y: cy - d / 2, w: d, h: d, fill: { color: NAVY }, line: { color: dash ? STEEL : "FFFFFF", width: dash ? 1 : 1.5, dashType: dash ? "dash" : "solid" } });
  const pan = (y0, titre, bas, ouvert) => {
    T(s, titre, { x: 7.9, y: y0, w: 4.6, h: 0.3, fontSize: 14, bold: true, color: "FFFFFF" });
    [["A", 8.6, y0 + 1.3], ["B", 10.2, y0 + 0.95], ["C", 11.8, y0 + 1.35]].forEach(([l, cx, cy]) => { if (ouvert) ring(cx, cy, 1.15, true); ring(cx, cy, 0.62, false); T(s, l, { x: cx - 0.31, y: cy - 0.31, w: 0.62, h: 0.62, fontSize: 16, bold: true, color: "FFFFFF", align: "center", valign: "middle" }); });
    s.addShape(pres.ShapeType.ellipse, { x: 10.05, y: y0 + 2.2, w: 0.3, h: 0.3, fill: { color: CORAL }, line: { color: CORAL, width: 0 } }); T(s, "?", { x: 10.05, y: y0 + 2.2, w: 0.3, h: 0.3, fontSize: 12, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
    if (!ouvert) s.addShape(pres.ShapeType.line, { x: 10.2, y: y0 + 1.3, w: 0.0, h: 0.85, line: { color: CORAL, width: 1.5, endArrowType: "triangle", beginArrowType: "none" }, flipV: true });
    T(s, bas, { x: 7.9, y: y0 + 2.6, w: 4.6, h: 0.3, fontSize: 13, color: ICE });
  };
  pan(0.95, "Monde fermé", "Toute entrée reçoit une classe : rangée dans B, à tort", false);
  pan(4.1, "Monde ouvert", "Une entrée hors des zones connues est reconnue comme inconnue", true);
  s.addNotes("Transition : on commence par l'idée. À dire : un classifieur ordinaire est forcé de ranger tout log dans une classe connue ; ici on veut qu'il sache aussi dire « je ne connais pas ». Question probable : pourquoi « hiérarchique » ? Parce que la taxonomie a deux niveaux, famille puis classe, et qu'un inconnu peut ressembler à une famille connue.");
}

// 2. Contexte
{
  const s = slide("Introduction - Contexte", "Les violations coûtent cher, et deux tiers des alertes sont ignorées",
    "Transition : avant le sujet technique, l'enjeu. À dire : les trois sources sont des rapports de l'industrie de la sécurité ; le chiffre d'IBM vient d'un article qui cite le rapport 2026. Ce que cela implique pour nous : le tri des événements est un travail humain coûteux. Question probable : ces chiffres prouvent-ils que le tri automatique aide ? Non, ils montrent l'ampleur du problème ; notre contribution est de mesurer honnêtement ce qu'un classifieur sait faire.");
  enclair(s, "chaque alerte de sécurité doit être triée par un humain, et il n'y a pas assez de monde pour toutes les traiter.");
  T(s, "4,99 M$", { x: X0, y: 1.95, w: 5.8, h: 1.3, fontSize: 70, color: CORAL, fontFace: HEAD });
  P(s, [["coût moyen d'une violation de données, en hausse de 12 % en un an ", C("ibm")]], { x: X0, y: 3.25, w: 5.5, h: 0.8, fontSize: 19 });
  P(s, [["247 jours pour l'identifier et la contenir ; au-delà de 200 jours, la violation coûte 5,65 M$ contre 4,32 M$ ", C("ibm")]], { x: X0, y: 4.1, w: 5.5, h: 0.9, fontSize: 15, run: { color: MUTED } });
  hline(s, 6.9, 2.0, 5.75);
  T(s, "4 484", { x: 6.9, y: 2.12, w: 2.3, h: 0.8, fontSize: 36, color: BLUE, fontFace: HEAD });
  P(s, [["alertes par jour pour une équipe de surveillance (SOC) ; 67 % sont ignorées ", C("vectra")]], { x: 9.3, y: 2.2, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 3.2, 5.75);
  T(s, "10 626", { x: 6.9, y: 3.32, w: 2.3, h: 0.8, fontSize: 36, color: BLUE, fontFace: HEAD });
  P(s, [["violations confirmées sur 30 458 incidents analysés (année 2023) ", C("verizon")]], { x: 9.3, y: 3.4, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 4.4, 5.75);
  dark(s, X0, 5.35, CW, 1.5);
  T(s, "Pourquoi c'est notre sujet", { x: X0 + 0.35, y: 5.5, w: 5, h: 0.3, fontSize: 13, bold: true, color: ICE });
  T(s, "Un SIEM rassemble les logs de tout le système d'information. Le goulot est humain : classer chaque événement et repérer celui qu'aucune règle ne décrit. Un classifieur qui sait dire « inconnu » réduit cette charge, à condition d'être évalué honnêtement.", { x: X0 + 0.35, y: 5.85, w: CW - 0.7, h: 0.95, fontSize: 16, color: "FFFFFF" });
}

// 3. Problématique
{
  const s = slide("Introduction - Problématique", "Une bonne note à l'examen ne prouve rien si les questions étaient déjà dans le cours",
    "Transition : de l'enjeu à la question. À dire : les scores publiés sur SIEVE atteignent 0,97 parce que les logs viennent d'un nombre fini de gabarits et qu'un découpage aléatoire laisse le même gabarit des deux côtés. Question probable : pourquoi pas simplement un meilleur modèle ? Parce que le problème n'est pas le modèle mais ce que l'évaluation mesure.");
  enclair(s, "un gabarit est une phrase à trous : tous les logs sont fabriqués en remplissant les mêmes phrases avec des valeurs différentes.");
  dark(s, X0, 2.05, 6.7, 2.15);
  T(s, "Question centrale", { x: X0 + 0.3, y: 2.17, w: 5, h: 0.3, fontSize: 13, bold: true, color: ICE });
  T(s, "Comment ranger un événement de sécurité dans une famille puis une classe précise, tout en reconnaissant qu'il n'appartient à aucune classe connue, avec une évaluation qui ne triche pas ?", { x: X0 + 0.3, y: 2.55, w: 6.1, h: 1.6, fontSize: 19, fontFace: HEAD, color: "FFFFFF" });
  const q = [["1", "Que valent les scores publiés ?", "Au test, on retrouve les mêmes phrases à trous qu'à l'entraînement : le score est gonflé."], ["2", "Sait-on repérer une classe jamais vue ?", "Dans un SIEM, l'inconnu est la règle."], ["3", "Le système résiste-t-il aux textes modifiés ?", "Fautes, lettres d'autres alphabets, mots ajoutés."]];
  q.forEach((r, i) => { const y = 4.5 + i * 0.82; T(s, r[0], { x: X0, y, w: 0.5, h: 0.5, fontSize: 26, color: CORAL, fontFace: HEAD }); T(s, r[1], { x: X0 + 0.6, y, w: 6.1, h: 0.32, fontSize: 15, bold: true, color: BLUE }); T(s, r[2], { x: X0 + 0.6, y: y + 0.33, w: 6.1, h: 0.4, fontSize: 12.5, color: MUTED }); });
  P(s, [[{ b: "Ce qui existe" }], ["Des programmes qui classent des logs, évalués avec un découpage au hasard : scores de 0,93 à 0,97 ", C("sieve")], [{ b: "Ce qui manque" }], ["Savoir ce que valent ces scores sur des phrases à trous nouvelles, et si l'on repère les classes jamais vues."]], { x: 7.9, y: 2.05, w: 4.75, h: 4.5, fontSize: 17, gap: 12 });
}

// 4. Objectifs
{
  const s = slide("Introduction - Objectifs", "Le projet mesure honnêtement ; il ne construit pas un produit",
    "Transition : de la question aux objectifs. À dire : volontairement pas de fonctionnalité promise ; l'utilité est un banc d'essai. Question probable : quel est le livrable ? Un notebook exécutable, des résultats chiffrés et un protocole qu'on peut réutiliser pour comparer d'autres classifieurs de logs.");
  lab(s, "Objectif général", X0, 2.0, 4.5);
  T(s, "Mesurer jusqu'où un programme sait classer des journaux de sécurité, reconnaître ceux qu'il n'a jamais vus et résister à des textes modifiés, avec une évaluation qui ne triche pas.", { x: X0, y: 2.4, w: 4.6, h: 3.2, fontSize: 21, fontFace: HEAD });
  lab(s, "Objectifs spécifiques", 6.2, 2.0, 5);
  [["Mesurer", " de combien la triche (mêmes phrases à trous au test) gonfle les scores"], ["Comparer", " trois façons de transformer le texte en nombres : comptage de mots, vecteurs de mots, réseau Transformer"], ["Comparer", " huit façons de repérer l'inconnu, en cachant des classes pour de faux"], ["Tester", " si les attaques sur le texte et les défenses tiennent vraiment"], ["Livrer", " un notebook reproductible, avec les règles de décision écrites avant les résultats"]].forEach((t, i) => {
    const y = 2.45 + i * 0.68; hline(s, 6.2, y - 0.08, 6.45); P(s, [[{ b: t[0] }, t[1]]], { x: 6.2, y, w: 6.45, h: 0.6, fontSize: 15, valign: "middle", run: { color: INK } }); });
  lab(s, "Sur quoi le projet pourrait servir", X0, 6.02, 6);
  T(s, "Un protocole et un banc d'essai réutilisables pour comparer des programmes de classement de logs et leurs détecteurs d'inconnu sans surestimer leurs performances. Rien de plus n'est revendiqué.", { x: X0, y: 6.34, w: 11.9, h: 0.55, fontSize: 14.5 });
}

// 5. État de l'art : vue d'ensemble
{
  const s = slide("État de l'art - Vue d'ensemble", "Aucun travail trouvé ne traite le classement hiérarchique de logs SIEM en monde ouvert",
    "Transition : ce qui existe. À dire : six familles de travaux, chacune avec ses références ; la recherche systématique du projet n'a trouvé aucun travail qui combine hiérarchie, logs SIEM et monde ouvert ; les 73 références ont toutes été ouvertes. Question probable : et la détection d'anomalies dans les logs ? C'est un autre problème : il sépare normal et anormal, sans classer les événements dans une taxonomie.");
  enclair(s, "« monde ouvert » veut dire que le programme peut rencontrer des événements qu'il n'a jamais appris.");
  const F = [["Jeux de logs", "Des journaux de sécurité synthétiques pour s'entraîner", [["SIEVE, Artioli et al., 2025 ", C("sieve")]]],
    ["Détection par le score", "Se méfier quand le modèle hésite entre les classes", [["Hendrycks et Gimpel, 2017 ", C("msp"), " ; Liu et al., 2020 ", C("energy")]]],
    ["Détection par la distance", "Se méfier quand l'exemple est loin de tout ce qui est connu", [["Lee et al., 2018 ", C("maha"), " ; Sun et al., 2022 ", C("knn"), " ; Bendale et Boult, 2016 ", C("openmax")]]],
    ["Hiérarchie", "Si la classe est incertaine, donner au moins la bonne famille", [["Linderman et al., 2022 ", C("lind")]]],
    ["Robustesse du texte", "Résister aux lettres trompeuses (homoglyphes) et aux fautes", [["Norme Unicode UTS #39 ", C("uts39")]]],
    ["Fiabilité de l'évaluation", "Vérifier que la confiance du modèle est honnête", [["Guo et al., 2017 ", C("guo"), " ; Vaze et al., 2022 ", C("vaze")]]]];
  T(s, "Famille", { x: X0, y: 1.95, w: 3, h: 0.3, fontSize: 12, bold: true, color: MUTED }); T(s, "L'idée en clair", { x: 4.1, y: 1.95, w: 4, h: 0.3, fontSize: 12, bold: true, color: MUTED }); T(s, "Travaux", { x: 9.0, y: 1.95, w: 3, h: 0.3, fontSize: 12, bold: true, color: MUTED });
  F.forEach((f, i) => { const y = 2.3 + i * 0.66; hline(s, X0, y - 0.05, CW); T(s, f[0], { x: X0, y, w: 3.4, h: 0.55, fontSize: 16, bold: true, color: BLUE, valign: "middle" }); T(s, f[1], { x: 4.1, y, w: 4.7, h: 0.55, fontSize: 14.5, valign: "middle" }); P(s, f[2], { x: 9.0, y, w: 3.65, h: 0.55, fontSize: 12.5, valign: "middle", run: { color: MUTED } }); });
  hline(s, X0, 6.28, CW);
  P(s, [["Recherche du projet : 73 références vérifiées, dont la page a été ouverte ", C("biblio")]], { x: X0, y: 6.4, w: CW, h: 0.4, fontSize: 13, run: { color: MUTED } });
}

// 6. État de l'art : analyse et propositions
{
  const s = slide("État de l'art - Analyse et propositions", "Chaque famille a une limite, et nos mesures les retrouvent",
    "Transition : de la liste à l'analyse. À dire : lire le tableau par ligne ; la dernière colonne est ce que nous avons observé sur nos données ; les propositions à droite répondent à ces limites. Question probable : pourquoi tester Mahalanobis alors qu'il échoue avec TF-IDF ? Parce que la littérature le donne efficace sur un Transformer affiné ; nos mesures confirment sur l'encodeur et pas sur TF-IDF.");
  enclair(s, "une méthode « de score » juge la confiance du modèle ; une méthode « de distance » juge l'éloignement par rapport aux classes connues.");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 13, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 13, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  s.addTable([[H("Famille"), H("Ce qu'elle apporte"), H("Sa limite, mesurée chez nous")],
    [Cc("Scores de sortie", { bold: true }), Cc("Simples, sans réentraînement"), Cc("La confiance affichée est fausse : écart de 0,15 à 0,25 avec la réalité")],
    [Cc("Distances", { bold: true }), Cc("Mesurent l'éloignement par rapport aux classes connues"), Cc("Avec le comptage de mots : 0,56, à peine mieux que le hasard (0,5). Avec le Transformer : mieux que le score de sortie")],
    [Cc("Hiérarchie", { bold: true }), Cc("Des erreurs moins graves : on garde la bonne famille"), Cc("Gain non démontré : la bonne famille est proposée une fois sur quatre")],
    [Cc("Défenses du texte", { bold: true }), Cc("Efficaces contre l'attaque connue"), Cc("Trompeuses : testées avec la table de l'attaque, elles semblent parfaites")]],
    { x: X0, y: 2.0, w: 7.6, colW: [1.6, 2.5, 3.5], rowH: [0.45, 0.8, 1.0, 0.8, 0.8], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
  P(s, [["Dans la littérature, la distance est efficace sur un Transformer affiné ", C("podolskiy"), "."]], { x: X0, y: 6.3, w: 7.6, h: 0.4, fontSize: 13, run: { color: MUTED } });
  lab(s, "Nos propositions", 8.9, 2.0, 3.8);
  P(s, [[{ b: "Découper par gabarit" }, " (phrase à trous) et sceller le test : on ne l'ouvre qu'une fois"], [{ b: "Écrire les règles avant de voir les chiffres" }], [{ b: "Comparer les scores" }, " sur la sortie du modèle et sur ses vecteurs internes"], [{ b: "Tester la défense" }, " avec une autre table de lettres que celle de l'attaque"]], { x: 8.9, y: 2.5, w: 3.8, h: 4.0, fontSize: 15, gap: 16 });
}

// 7. Matériel
{
  const s = slide("Matériel", "600 000 logs de SIEVE, des fichiers du professeur et un réseau de neurones pré-entraîné",
    "Transition : après la théorie, la matière. À dire : le jeu SIEVE est la base ; les fichiers du professeur servent de contrôle de fuite ; le CDS réel n'était pas dans l'archive donc le transfert vers des logs réels n'a pas pu être fait. Question probable : les logs sont-ils réels ? Non, ils sont générés à partir de 440 gabarits issus de logs réels.");
  lab(s, "SIEVE : six versions de 100 000 logs, de plus en plus abîmées", X0, 1.95, 7);
  ["0", "0,1", "0,2", "0,3", "0,4", "0,5"].forEach((p, i) => { const x = X0 + i * 0.98; s.addShape(pres.ShapeType.rect, { x, y: 2.4, w: 0.88, h: 0.7, fill: { color: i === 0 ? BLUE : "FFFFFF" }, line: { color: BLUE, width: 1 } }); T(s, "p = " + p, { x, y: 2.4, w: 0.88, h: 0.7, fontSize: 13, bold: true, color: i === 0 ? "FFFFFF" : BLUE, align: "center", valign: "middle" }); });
  P(s, [["30 classes équilibrées, 440 gabarits (phrases à trous) ", C("sieve")], ["p mesure à quel point le texte est abîmé : plus il augmente, plus des mots sont remplacés, ajoutés ou déplacés."]], { x: X0, y: 3.3, w: 5.9, h: 1.8, fontSize: 15, gap: 10 });
  const R = [["6 × 35 000", [["logs du professeur : mêmes phrases à trous, valeurs nouvelles"]]], ["1 447", [["lettres d'autres alphabets confondables avec les nôtres (table Unicode officielle ", C("uts39"), ")"]]], ["DistilBERT", [["réseau de neurones déjà entraîné sur du texte ", C("distil")]]], ["8 familles", [["regroupement des 30 classes : notre hypothèse"]]], ["0 log réel", [["aucun log réel fourni : pas de test en conditions réelles"]]]];
  R.forEach((r, i) => { const y = 2.0 + i * 0.62; hline(s, 7.0, y - 0.05, 5.65); T(s, r[0], { x: 7.0, y, w: 2.15, h: 0.52, fontSize: 19, color: CORAL, fontFace: HEAD, valign: "middle" }); P(s, r[1], { x: 9.2, y, w: 3.45, h: 0.52, fontSize: 12.5, valign: "middle" }); });
  s.addShape(pres.ShapeType.rect, { x: X0, y: 5.3, w: CW, h: 1.55, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } });
  T(s, "Même événement (échec de connexion) : propre à p = 0, puis abîmé à p = 0,5. Extraits des fichiers du professeur.", { x: X0 + 0.25, y: 5.38, w: CW - 0.5, h: 0.25, fontSize: 11, color: MUTED });
  T(s, "p = 0    [Wed Nov 03 19:30:11 1976] [error] [client 217.121.56.73] user clarkesummer: authentication failure for \"/at/challenge.png/pass\": Password Mismatch", { x: X0 + 0.25, y: 5.68, w: CW - 0.5, h: 0.5, fontSize: 11.5, color: INK, fontFace: MONO });
  T(s, "p = 0,5  :forauthentication [failure] /authority/car.wavhsandoval 214.18.6.71] user /: client Mismatch Thu Dec 07 03:54:44 2006 \"[Password[]air \" error", { x: X0 + 0.25, y: 6.3, w: CW - 0.5, h: 0.5, fontSize: 11.5, color: INK, fontFace: MONO });
}

// 8. Méthodes
{
  const s = slide("Méthodes", "Quatre étapes séparent le texte brut de la décision d'accepter ou de rejeter",
    "Transition : de la matière à la méthode. À dire : lire de gauche à droite ; le seuil de rejet est calé sur 95 % des logs connus de validation ; les classes masquées servent seulement à mesurer. Question probable : pourquoi huit scores ? Parce que la littérature n'en désigne pas un meilleur dans notre cas ; on compare avec des règles écrites d'avance.");
  enclair(s, "le texte devient des nombres, un modèle choisit une classe, une note dit s'il faut s'en méfier, puis on évalue sans tricher.");
  const cols = [["Transformer le texte en nombres", [["Comptage de mots (TF-IDF, n-grammes)"], ["Vecteurs de mots (Word2Vec, GloVe)"], ["Réseau Transformer (DistilBERT) ", C("distil")]]], ["Choisir la famille puis la classe", [["Un seul niveau : directement la classe"], ["Deux niveaux : la famille d'abord, puis la classe ", C("lind")]]],
    ["Donner une note d'étrangeté", [["Selon la confiance du modèle (MSP ", C("msp"), ", énergie ", C("energy"), ")"], ["Selon la distance aux classes connues (Mahalanobis ", C("maha"), ", kNN ", C("knn"), ", OpenMax ", C("openmax"), ")"], ["On rejette au-delà d'un seuil qui garde 95 % des cas connus"]]], ["Évaluer sans tricher", [["Découpage par gabarit, test scellé"], ["Cinq rotations : six classes cachées pour de faux à chaque fois"], ["Marges d'erreur calculées par gabarit ", C("field")]]]];
  cols.forEach((c, i) => { const x = X0 + i * 3.05; if (i > 0) s.addShape(pres.ShapeType.line, { x: x - 0.22, y: 2.05, w: 0, h: 3.4, line: { color: LINE, width: 0.75 } });
    if (i < 3) s.addShape(pres.ShapeType.rightArrow, { x: x + 2.72, y: 2.22, w: 0.2, h: 0.26, fill: { color: STEEL }, line: { color: STEEL, width: 0 } });
    P(s, [[{ b: String(i + 1) + "  " }, { b: c[0] }]], { x, y: 2.05, w: 2.7, h: 0.75, fontSize: 16, run: { color: BLUE } }); P(s, c[1], { x, y: 2.9, w: 2.7, h: 2.6, fontSize: 14, gap: 12 }); });
  hline(s, X0, 5.65, CW);
  lab(s, "Robustesse et fiabilité", X0, 5.8, 4);
  P(s, [["Attaques : fautes de frappe, lettres trompeuses, mots ajoutés. Défenses : remplacer les lettres trompeuses par la table officielle ", C("uts39"), ", entraîner avec des textes abîmés, recalibrer la confiance ", C("guo")]], { x: X0, y: 6.13, w: CW, h: 0.75, fontSize: 14.5 });
}

// 9. Présentation des données (1/3) : taxonomie et rotations dessinées en natif
{
  const s = slide("Présentation des données (1/3)", "30 classes en 8 familles, chacune masquée dans une rotation sur cinq",
    "Transition : de la méthode aux données. À dire : six fichiers de 100 000 logs, 30 classes équilibrées ; la taxonomie à deux niveaux est notre hypothèse de démonstration, adossée à ECS, pas validée par un expert. Le repère R1 à R5 à droite de chaque classe dit dans quelle rotation elle est masquée pour simuler l'inconnu : six classes par rotation, chaque classe masquée une seule fois. Question probable : pourquoi cinq rotations ? Pour que chaque classe serve une fois d'inconnue et que le résultat ne dépende pas d'un seul choix.");
  enclair(s, "une classe = un type d'événement ; une classe masquée est cachée à l'entraînement pour jouer l'inconnue.");
  P(s, [[{ b: "600 000" }, " logs   ·   ", { b: "30" }, " classes équilibrées   ·   ", { b: "8" }, " familles   ·   ", { b: "6" }, " niveaux de perturbation   ·   ", { b: "440" }, " gabarits"]], { x: X0, y: 1.92, w: CW, h: 0.4, fontSize: 16, run: { color: BLUE } });
  const TAX = {
    file: ["directory-changed", "directory-created", "directory-deleted", "file-action-failure", "file-deleted", "file-modification", "file-read", "file-write"],
    network: ["connection-closed", "connection-failed", "connection-opened", "network-filtered", "network-traffic"], web: ["http-request-failure", "http-request-success"],
    process: ["process-ended", "process-error", "process-info", "process-shutdown", "process-started"], authentication: ["authentication-failed", "authentication-success"],
    identity_session: ["user-creation", "user-deletion", "user-logout", "user-session-open"], system: ["database-operation", "hardware-monitoring", "system-configuration-changed"], security_alert: ["ids-alert"] };
  const ROT = {"directory-created": 1, "http-request-success": 1, "process-info": 1, "process-started": 1, "system-configuration-changed": 1, "user-session-open": 1, "database-operation": 2, "file-deleted": 2, "network-traffic": 2, "process-ended": 2, "process-error": 2, "user-creation": 2, "authentication-failed": 3, "connection-failed": 3, "directory-changed": 3, "file-action-failure": 3, "http-request-failure": 3, "network-filtered": 3, "file-modification": 4, "file-read": 4, "hardware-monitoring": 4, "ids-alert": 4, "process-shutdown": 4, "user-logout": 4, "authentication-success": 5, "connection-closed": 5, "connection-opened": 5, "directory-deleted": 5, "file-write": 5, "user-deletion": 5};
  const COLS = [["file"], ["network", "web"], ["process", "authentication"], ["identity_session", "system", "security_alert"]];
  const cw = 2.85, gx = (CW - 4 * cw) / 3;
  COLS.forEach((fams, col) => { let y = 2.45; const x = X0 + col * (cw + gx);
    fams.forEach((f) => { const cl = TAX[f];
      s.addShape(pres.ShapeType.rect, { x, y, w: cw, h: 0.36, fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
      T(s, f + "  (" + cl.length + ")", { x: x + 0.12, y, w: cw - 0.2, h: 0.36, fontSize: 13, bold: true, color: "FFFFFF", valign: "middle" });
      cl.forEach((c, j) => { const yy = y + 0.42 + j * 0.25; T(s, c, { x: x + 0.12, y: yy, w: cw - 0.65, h: 0.25, fontSize: c.length > 26 ? 9.5 : 11, fontFace: MONO, color: INK, valign: "middle" }); T(s, "R" + ROT[c], { x: x + cw - 0.5, y: yy, w: 0.4, h: 0.25, fontSize: 11, bold: true, color: CORAL, align: "right", valign: "middle" }); });
      y += 0.42 + cl.length * 0.25 + 0.2; }); });
  T(s, "R1 à R5 : numéro de la rotation où la classe est cachée (six classes par rotation). Regroupement en familles : notre hypothèse, non validée par un expert SIEM.", { x: X0, y: 6.5, w: CW, h: 0.4, fontSize: 12, color: MUTED });
}

// 9bis. Présentation des données (2/3) : un gabarit expliqué, dessiné en natif
{
  const s = slide("Présentation des données (2/3)", "Chaque log est une phrase à trous remplie de valeurs : nous avons retrouvé 311 des 440 phrases",
    "À dire : un gabarit est une phrase à trous, par exemple un message d'échec d'authentification avec la date, l'adresse, le nom et le chemin laissés vides. Chaque log du jeu est ce gabarit rempli avec des valeurs différentes ; le gabarit en haut est notre schéma, le log en dessous est un vrai extrait des fichiers du professeur. SIEVE annonce 440 gabarits sans les fournir ; en regroupant les logs, nous en avons retrouvé 311. Question probable : pourquoi n'en retrouve-t-on pas 440 ? Les gabarits rares se confondent ; c'est dit comme limite. Plus p est grand, plus le texte s'éloigne du gabarit.");
  enclair(s, "tous les logs d'une même classe viennent de quelques phrases types, et c'est ce qui rend l'évaluation au hasard trompeuse.");
  lab(s, "1. Le gabarit : une phrase à trous (schéma)", X0, 2.0, 7);
  s.addShape(pres.ShapeType.rect, { x: X0, y: 2.38, w: 7.4, h: 0.85, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } });
  T(s, "[<date>] [error] [client <adresse IP>] user <nom>: authentication failure for \"<chemin>\": Password Mismatch", { x: X0 + 0.2, y: 2.38, w: 7.0, h: 0.85, fontSize: 11.5, fontFace: MONO, valign: "middle" });
  T(s, "↓  on remplit les trous avec des valeurs", { x: X0, y: 3.32, w: 7.4, h: 0.35, fontSize: 14, bold: true, color: CORAL });
  lab(s, "2. Un log : le gabarit rempli (extrait réel)", X0, 3.75, 7);
  s.addShape(pres.ShapeType.rect, { x: X0, y: 4.13, w: 7.4, h: 0.85, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } });
  T(s, "[Wed Nov 03 19:30:11 1976] [error] [client 217.121.56.73] user clarkesummer: authentication failure for \"/at/challenge.png/pass\": Password Mismatch", { x: X0 + 0.2, y: 4.13, w: 7.0, h: 0.85, fontSize: 11.5, fontFace: MONO, valign: "middle" });
  lab(s, "3. Le même log abîmé, à p = 0,5", X0, 5.1, 7);
  s.addShape(pres.ShapeType.rect, { x: X0, y: 5.48, w: 7.4, h: 0.85, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } });
  T(s, ":forauthentication [failure] /authority/car.wavhsandoval 214.18.6.71] user /: client Mismatch Thu Dec 07 03:54:44 2006 \"[Password[]air \" error", { x: X0 + 0.2, y: 5.48, w: 7.0, h: 0.85, fontSize: 11.5, fontFace: MONO, valign: "middle" });
  T(s, "Plus p est grand, plus le texte s'éloigne de la phrase d'origine.", { x: X0, y: 6.45, w: 7.4, h: 0.35, fontSize: 12.5, color: MUTED });
  s.addChart(pres.charts.BAR, [{ name: "gabarits", labels: ["Annoncés par SIEVE", "Retrouvés par nous"], values: [440, 311] }], Object.assign(chartBase("Nombre de gabarits"), { x: 8.5, y: 2.0, w: 4.15, h: 3.9, barDir: "col", chartColors: [STEEL, BLUE], valAxisMinVal: 0, valAxisMaxVal: 500, valAxisMajorUnit: 100, dataLabelFormatCode: "0", showLegend: false }));
  T(s, "Les gabarits rares se confondent entre eux : 129 restent introuvables.", { x: 8.5, y: 6.0, w: 4.15, h: 0.7, fontSize: 13, color: MUTED });
}

// 9ter. Présentation des données (3/3) : fuite
{
  const s = slide("Présentation des données (3/3)", "Avec un découpage au hasard, le voisin le plus proche d'un log de test est de son propre gabarit",
    "À dire : on compare chaque log de test à son plus proche voisin dans l'entraînement. En rouge, découpage aléatoire : la ressemblance est presque parfaite, parce que le même gabarit est des deux côtés. En bleu, découpage par gabarit : la ressemblance chute. Voilà la fuite, c'est elle qui explique 0,97 contre 0,46. Question probable : est-ce propre à SIEVE ? Oui à ce jeu, fabriqué à partir de gabarits ; c'est pourquoi l'évaluation par gabarit est le cœur du travail.");
  T(s, [{ text: "En clair : ", options: { bold: true, color: BLUE } }, { text: "barre à droite = le log de test ressemble à un log déjà vu. ", options: { color: MUTED } }, { text: "Rouge", options: { bold: true, color: "C0392B" } }, { text: " : découpage au hasard, on peut tricher. ", options: { color: MUTED } }, { text: "Bleu", options: { bold: true, color: "3B6FD8" } }, { text: " : découpage par gabarit, test honnête.", options: { color: MUTED } }], { x: X0, y: 1.42, w: CW, h: 0.5, fontSize: 13.5 });
  image(s, "03_fuite_gabarits", X0, 2.05, CW, 4.35, "Fuite entre gabarits");
  T(s, "À gauche : version propre des logs (p = 0). À droite : version abîmée (p = 0,5). Axe horizontal : ressemblance, de 0 (rien à voir) à 1 (identique).", { x: X0, y: 6.5, w: CW, h: 0.35, fontSize: 12, color: MUTED });
}

// 10. Librairies
{
  const s = slide("Librairies utilisées", "Un socle scientifique classique, en versions figées",
    "Transition : des données aux outils. À dire : tout est dans requirements.txt du dépôt avec les versions exactes. Question probable : pourquoi PyTorch et Transformers seulement pour l'encodeur ? Parce que tous les autres modèles sont linéaires, donc scikit-learn suffit.");
  enclair(s, "chaque bibliothèque est une boîte à outils prête à l'emploi ; les versions exactes sont figées pour pouvoir tout rejouer.");
  const L = [["Données et calcul", ["numpy 2.5.4", "pandas 3.1.1", "scipy 1.18.1"]], ["Apprentissage automatique", ["scikit-learn 1.9.1", "joblib 1.6.0"]], ["Texte et vecteurs de mots", ["gensim 4.4.0", "nltk 3.10.4"]], ["Apprentissage profond", ["PyTorch 2.15.0", "Transformers 5.22.1", "tokenizers 0.23.3"]], ["Visualisation", ["matplotlib 3.11.2"]], ["Exécution et reproductibilité", ["ipykernel 7.4.0", "nbclient 0.11.0", "nbformat 5.11.1"]], ["Langage", ["Python 3.12"]]];
  L.forEach((l, i) => { const y = 2.05 + i * 0.68; hline(s, X0, y - 0.08, CW); T(s, l[0], { x: X0, y, w: 4.2, h: 0.5, fontSize: 17, bold: true, color: BLUE, valign: "middle" });
    let x = 5.2; l[1].forEach((lib) => { const w = 0.105 * lib.length + 0.45; s.addShape(pres.ShapeType.roundRect, { x, y: y + 0.05, w, h: 0.4, fill: { color: PANEL }, line: { color: LINE, width: 0.75 }, rectRadius: 0.06 }); T(s, lib, { x, y: y + 0.05, w, h: 0.4, fontSize: 13, fontFace: MONO, align: "center", valign: "middle" }); x += w + 0.2; }); });
  hline(s, X0, 6.8, CW);
}

// 11. Environnement d'exécution : schéma de flux
{
  const s = slide("Environnement d'exécution", "Le calcul est réparti sur un Mac et Colab, et reprend là où il s'est arrêté",
    "Transition : des outils à l'exécution. À dire : les entraînements d'encodeur tournent sur la carte graphique du Mac ou sur Colab ; chaque résultat est sauvegardé donc une interruption ne fait pas tout refaire. Question probable : pourquoi pas tout sur Colab ? Le quota de carte graphique gratuit s'épuise vite ; répartir a évité de perdre du temps.");
  enclair(s, "le gros calcul tourne sur deux machines, chaque résultat est sauvegardé, et tout peut être rejoué.");
  const box = (x, y, w, h, t1, t2, fill) => { s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: fill || "FFFFFF" }, line: { color: BLUE, width: 1.25 } }); T(s, t1, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: 0.4, fontSize: 16, bold: true, color: fill ? "FFFFFF" : BLUE }); T(s, t2, { x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.6, fontSize: 13, color: fill ? ICE : INK }); };
  box(X0, 2.0, 4.0, 1.5, "Mac (puce M3 Pro)", "Modèles simples, vecteurs de mots, et une partie des entraînements du réseau (rotations 3 à 5), sur la carte graphique du Mac");
  box(X0, 3.65, 4.0, 1.5, "Google Colab", "Ordinateur loué dans le nuage, avec une carte graphique : entraînements du réseau (rotations 1 et 2)");
  box(5.7, 2.85, 2.5, 1.5, "Notebook", "Un seul document qui contient le code, les résultats et les figures", BLUE);
  box(9.2, 2.85, 3.43, 1.5, "Dépôt GitHub public", "Notebook, résultats, figures, code ; sans les données SIEVE");
  const arrow = (x1, y1, x2, y2) => s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipV: y2 < y1, line: { color: CORAL, width: 1.75, endArrowType: "triangle" } });
  arrow(X0 + 4.0, 2.75, 5.7, 3.4); arrow(X0 + 4.0, 4.4, 5.7, 3.85); arrow(8.2, 3.6, 9.2, 3.6);
  dark(s, X0, 5.5, CW, 1.3);
  [["13 à 20 min", "pour entraîner un réseau"], ["15 réseaux", "3 essais × 5 rotations"], ["≈ 13 min", "pour rejouer tout le notebook"], ["Reprise", "automatique après interruption"]].forEach((k, i) => { const x = X0 + 0.35 + i * 2.95; T(s, k[0], { x, y: 5.68, w: 2.7, h: 0.5, fontSize: 24, color: "FFFFFF", fontFace: HEAD }); T(s, k[1], { x, y: 6.25, w: 2.7, h: 0.4, fontSize: 13, color: ICE }); });
}

// 12. Pipeline : ligne de métro (nœuds reliés), sans cartes
{
  const s = slide("Conception - Pipeline utilisé", "Onze étapes, dont le découpage par gabarit est celle qui change le plus les conclusions",
    "Transition : de l'environnement au déroulé. À dire : chaque étape a ses décisions justifiées dans le notebook ; la 3 est en couleur car c'est elle qui a fait passer le score de 0,97 à 0,46. Les codes H1 à H15 (hypothèses), P0 à P3 (protocoles de découpage) et E1 à E5 (expériences) sont dans le notebook. Question probable : pourquoi 11 étapes ? Elles suivent la consigne du projet (cadrage à conclusion) avec les sous-étapes que nous avons ajoutées.");
  enclair(s, "de la question de départ à la conclusion, onze étapes ; l'étape en orange est celle qui change tout.");
  const P_ = [["Cadrage", "Question, hypothèses à tester, critères de succès fixés d'avance"], ["Données", "Récupération et vérification du format"], ["Exploration", "Classes proches, phrases à trous, effet de p"], ["Découpage", "Par gabarit, test scellé, quatre protocoles"], ["Prétraitement", "Nettoyage du texte, 10 variantes"], ["Représentations", "Comptage de mots, vecteurs, Transformer"],
    ["Modèles", "Un ou deux niveaux, huit notes d'étrangeté"], ["Évaluation", "Test scellé, ouvert une seule fois"], ["Robustesse", "Attaques sur le texte"], ["Amélioration", "Défenses, calibration"], ["Conclusion", "99 affirmations vérifiées, limites"]];
  const rows = [[0, 6, 2.2], [6, 11, 4.3]];
  rows.forEach(([a, b, y]) => { const cnt = b - a, step = 2.05, x0 = X0 + 0.6 + (cnt < 6 ? step / 2 : 0); s.addShape(pres.ShapeType.line, { x: x0, y: y + 0.28, w: step * (cnt - 1), h: 0, line: { color: STEEL, width: 2 } });
    for (let i = a; i < b; i++) { const cx = x0 + (i - a) * step, hot = i === 3;
      s.addShape(pres.ShapeType.ellipse, { x: cx - 0.28, y, w: 0.56, h: 0.56, fill: { color: hot ? CORAL : BLUE }, line: { color: "FFFFFF", width: 2 } }); T(s, String(i), { x: cx - 0.28, y, w: 0.56, h: 0.56, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
      T(s, P_[i][0], { x: cx - 0.95, y: y + 0.7, w: 1.9, h: 0.35, fontSize: 15, bold: true, color: hot ? CORAL : BLUE, align: "center" }); T(s, P_[i][1], { x: cx - 0.95, y: y + 1.08, w: 1.9, h: 1.2, fontSize: 13.5, align: "center" }); } });
  T(s, "Étape 3 : de 0,97 (découpage au hasard) à 0,46 (découpage par gabarit)", { x: X0, y: 6.5, w: CW, h: 0.4, fontSize: 16, bold: true, color: CORAL, align: "center" });
}

// 13. Résultats : quatre diapositives, un graphique chacune, graphiques natifs
const resultat = (k, message, clair, addChart, lire, retiens, notes) => {
  const s = slide("Conception - Présentation et analyse des résultats (" + k + "/4)", message, notes);
  enclair(s, clair); addChart(s);
  lab(s, "Comment lire", 8.7, 2.05, 4); T(s, lire, { x: 8.7, y: 2.45, w: 3.95, h: 2.0, fontSize: 14 });
  dark(s, 8.7, 4.55, 3.95, 2.25); T(s, "À retenir", { x: 8.95, y: 4.67, w: 3.5, h: 0.3, fontSize: 13, bold: true, color: ICE }); T(s, retiens, { x: 8.95, y: 5.0, w: 3.5, h: 1.7, fontSize: 15, color: "FFFFFF" });
};
const CH = { x: X0, y: 2.0, w: 7.9, h: 4.8 };
resultat(1, "De 0,99 à 0,48 : le découpage fait l'écart, pas le modèle", "le score mesure la part de bonnes réponses ; avec le découpage au hasard, le programme revoit au test des phrases déjà apprises.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "macro-F1", labels: ["Découpage\nau hasard", "Par gabarit", "Par groupes\nde gabarits", "Validation\nimbriquée", "Test scellé"], values: [0.987, 0.422, 0.507, 0.511, 0.483] }], Object.assign(chartBase("Part de bonnes réponses (macro-F1)"), CH, { barDir: "col", chartColors: [STEEL, BLUE, BLUE, BLUE, CORAL], valAxisMaxVal: 1, valAxisMinVal: 0, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", dataLabelFontSize: 13, catAxisLabelFontSize: 12, showLegend: false })),
  "1 = tout est juste. Le macro-F1 note chaque classe selon deux questions : les logs trouvés sont-ils les bons, et a-t-on trouvé tous les bons ? Il moyenne ensuite les 30 classes.",
  "0,99 au hasard, 0,48 au test scellé : le score élevé venait de phrases à trous déjà vues.",
  "Transition : du déroulé aux résultats. À dire : même modèle, seul le découpage change. Question probable : le 0,97 est-il faux ? Non, il est exact, mais il mesure la reconnaissance de gabarits déjà vus. Valeurs : découpage aléatoire 0,987, par gabarit 0,422, groupes 0,507, imbriquée 0,511, test scellé 0,483.");
resultat(2, "Repérer l'inconnu reste difficile : 0,60 au test, où 0,5 est le hasard", "chaque barre dit à quel point un programme sait distinguer un événement inconnu d'un événement connu.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "AUROC", labels: ["Comptage de mots\n(validation)", "Comptage de mots\n(test)", "Transformer,\nscore de confiance", "Transformer\n+ distance"], values: [0.728, 0.599, 0.548, 0.605] }], Object.assign(chartBase("Capacité à repérer l'inconnu (AUROC)"), CH, { barDir: "col", chartColors: [STEEL, BLUE, STEEL, CORAL], valAxisMaxVal: 1, valAxisMinVal: 0.4, valAxisMajorUnit: 0.1, dataLabelFormatCode: "0.00", dataLabelFontSize: 13, catAxisLabelFontSize: 12, showLegend: false })),
  "L'AUROC va de 0,5 (hasard) à 1 (parfait). C'est la chance qu'un événement inconnu reçoive une note plus étrange qu'un événement connu.",
  "0,60 au test : à peine mieux que le hasard. La distance (Mahalanobis) sur le Transformer gagne 0,057 sur son score de confiance.",
  "À dire : le score de validation, 0,73, était trop optimiste ; au test sur de nouvelles phrases à trous il tombe à 0,60. Le Transformer seul fait 0,55 ; avec Mahalanobis sur ses vecteurs, 0,605, soit 0,057 de plus. Question probable : pourquoi Mahalanobis ? Parce que la littérature le donne efficace sur un Transformer affiné.");
resultat(3, "Les lettres trompeuses sont l'attaque la plus efficace : jusqu'à 21,5 % de score en moins", "on abîme les logs de trois façons et on mesure de combien le score baisse.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "Modèle par mots", labels: ["Fautes de frappe", "Lettres trompeuses", "Mots ajoutés"], values: [7.8, 21.5, 12.5] }, { name: "Modèle par lettres", labels: ["Fautes de frappe", "Lettres trompeuses", "Mots ajoutés"], values: [4.0, 10.6, 14.4] }], Object.assign(chartBase("Perte de score après l'attaque (%)"), CH, { barDir: "col", chartColors: [BLUE, STEEL], valAxisMinVal: 0, dataLabelFormatCode: "0.0", dataLabelFontSize: 13, catAxisLabelFontSize: 12, showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: INK })),
  "Une barre haute = le modèle est très perturbé. Les « lettres trompeuses » sont des lettres d'autres alphabets qui ressemblent aux nôtres (un a cyrillique, par exemple).",
  "Le modèle par mots perd 21,5 % avec des lettres trompeuses ; le modèle par lettres résiste mieux à celle-ci, moins aux mots ajoutés.",
  "À dire : attaques fortes, mesurées en perte relative de macro-F1. Question probable : que veut dire modèle par mots ? Il compte les mots entiers ; le modèle par lettres compte des morceaux de mots, donc une lettre changée le trouble moins.");
resultat(4, "Une défense qui connaît l'attaque paraît parfaite, mais ne protège pas contre une autre table", "on essaie de réparer les lettres trompeuses avec une table de correspondance, puis on la teste de deux façons.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "perte", labels: ["Sans défense", "Table de l'attaque,\ntestée contre elle-même", "Table de l'attaque,\ntestée contre la\ntable officielle", "Table officielle\ncomplète"], values: [10.8, 0.0, 8.7, 0.1] }], Object.assign(chartBase("Perte de score malgré la défense (%)"), CH, { barDir: "col", chartColors: [STEEL, BLUE, CORAL, BLUE], valAxisMinVal: 0, dataLabelFormatCode: "0.0", dataLabelFontSize: 13, catAxisLabelFontSize: 11, showLegend: false })),
  "Une barre basse = la défense marche. Testée contre la table même qui l'a conçue, elle paraît parfaite : c'est un test circulaire.",
  "0,0 % était trompeur : contre la table officielle, la perte revient à 8,7 %. Seule la table officielle complète tient (0,1 %).",
  "À dire : la défense « maison » est construite avec la table de l'attaque, donc elle y réussit à 100 %. Testée contre la table officielle Unicode, elle perd 8,7 %. La table officielle complète limite la perte à 0,1 %. Question probable : que conclure ? Une défense se teste contre une autre table que celle de l'attaque.");

// 14. Limites : tableau limite -> conséquence
{
  const s = slide("Conception - Limites de la conception", "Six limites bornent ce que l'on peut affirmer",
    "Transition : des résultats à leurs limites. À dire : chaque ligne dit ce que la limite change dans les conclusions ; ces limites sont aussi dans le README et dans la section 10.6 du notebook. Question probable : laquelle pèse le plus ? Les données synthétiques : sans logs réels, on ne sait pas si les conclusions se transfèrent.");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 14, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 14, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  const N = (t) => Cc(String(t), { fontFace: HEAD, fontSize: 22, color: CORAL });
  s.addTable([[H(""), H("Limite"), H("Ce que cela change pour les conclusions")],
    [N(1), Cc("Données synthétiques : 440 gabarits, 311 reconstruits", { bold: true }), Cc("Les scores mesurent des gabarits, pas des logs réels")],
    [N(2), Cc("Taxonomie non validée par un expert SIEM", { bold: true }), Cc("Les 8 familles restent une hypothèse de démonstration")],
    [N(3), Cc("Peu de gabarits distincts : 36 en validation, 45 au test", { bold: true }), Cc("Un écart inférieur à 0,05 est indétectable")],
    [N(4), Cc("Trois essais pour le Transformer, un seul pour la plupart des autres modèles", { bold: true }), Cc("Le bruit d'entraînement n'est pas toujours mesuré")],
    [N(5), Cc("Test scellé déjà ouvert une fois", { bold: true }), Cc("Les scores ajoutés ensuite sont comparés sur la validation seulement")],
    [N(6), Cc("Pas de logs réels ; attaques qui ne s'adaptent pas à la défense", { bold: true }), Cc("Aucune garantie face à un attaquant qui connaît le modèle")]],
    { x: X0, y: 2.0, w: CW, colW: [0.7, 5.6, 5.63], rowH: [0.45, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
}

// 15. Conclusion : panneau sombre à gauche (chiffres à retenir), limites et perspectives à droite
{
  const s = slide("Conclusion", "Évaluer par gabarit change la conclusion ; détecter l'inconnu reste un problème ouvert",
    "Transition : des limites à la conclusion. À dire : quatre chiffres suffisent pour résumer le travail ; à droite ce qui borne ces chiffres et ce que nous ferions ensuite. Question probable : que feriez-vous en premier ? Valider la taxonomie avec un expert SIEM et tester sur des logs réels, car c'est ce qui conditionne le reste.");
  dark(s, X0, 1.95, 7.2, 4.95);
  T(s, "À retenir", { x: X0 + 0.35, y: 2.1, w: 4, h: 0.3, fontSize: 13, bold: true, color: ICE });
  [["0,97 → 0,46", "de bonnes réponses (macro-F1) quand on sépare les logs par gabarit"], ["0,60", "de capacité à repérer l'inconnu au test (0,5 = hasard)"], ["+ 0,057", "pour la distance (Mahalanobis) sur le Transformer, contre son score de confiance ", "podolskiy"], ["≈ 0,001", "de perte avec la table officielle complète ; la table de l'attaque ne protégeait que parce qu'elle la connaissait"]].forEach((r, i) => {
    const y = 2.55 + i * 1.08; if (i > 0) s.addShape(pres.ShapeType.line, { x: X0 + 0.35, y: y - 0.1, w: 6.5, h: 0, line: { color: "3A5380", width: 0.75 } });
    T(s, r[0], { x: X0 + 0.35, y, w: 2.7, h: 0.85, fontSize: 30, color: "F08A66", fontFace: HEAD, valign: "middle" }); P(s, [r[2] ? [r[1], C(r[2])] : [r[1]]], { x: X0 + 3.2, y, w: 3.7, h: 0.85, fontSize: 14, valign: "middle", run: { color: "FFFFFF" } }); });
  lab(s, "Limites", 8.4, 2.0, 4);
  P(s, [["Taxonomie non validée, gabarits reconstruits"], ["Trois essais, peu de gabarits de test"], ["Pas de logs réels : transfert non testé"]], { x: 8.4, y: 2.4, w: 4.25, h: 1.8, fontSize: 14, gap: 8 });
  lab(s, "Perspectives", 8.4, 4.35, 4);
  P(s, [["Valider la taxonomie avec un expert SIEM"], ["Tester sur des logs réels"], ["Plus d'essais, attaques qui s'adaptent à la défense"]], { x: 8.4, y: 4.75, w: 4.25, h: 2.0, fontSize: 14, gap: 8 });
}

// 16. Merci : clôture avec message à retenir et accès au dépôt
{
  const s = pres.addSlide({ masterName: "TITRE_SOMBRE" }); n += 1;
  T(s, "Merci", { x: 0.8, y: 1.3, w: 7, h: 1.1, fontSize: 60, bold: true, color: "FFFFFF", fontFace: HEAD });
  T(s, "À retenir : évaluer par gabarit, mesurer la détection d'inconnus, tester une défense contre une autre table que celle de l'attaque.", { x: 0.8, y: 2.8, w: 6.6, h: 1.4, fontSize: 22, color: ICE, fontFace: HEAD });
  T(s, "Notebook, résultats, figures et code :\ngithub.com/MADENIYOU/siem-open-world-log-classification", { x: 0.8, y: 4.9, w: 7.2, h: 0.9, fontSize: 16, color: "FFFFFF" });
  T(s, "Références : diapositive suivante", { x: 0.8, y: 6.3, w: 6, h: 0.3, fontSize: 13, color: STEEL });
  s.addShape(pres.ShapeType.rect, { x: 8.7, y: 1.5, w: 3.6, h: 3.6, fill: { color: "FFFFFF" }, line: { color: "FFFFFF", width: 0 } }); image(s, "assets/qr_depot", 8.85, 1.65, 3.3, 3.3, "Code QR du dépôt GitHub");
  T(s, "Dépôt public", { x: 8.7, y: 5.3, w: 3.6, h: 0.35, fontSize: 14, color: STEEL, align: "center" });
  s.addNotes("Clôture. À dire : merci, et le message en une phrase ; le dépôt contient tout ce qu'il faut pour rejouer le notebook, sauf les données SIEVE qui ne sont pas redistribuées. Si une question porte sur une source, la diapositive suivante liste toutes les références.");
}

// 17. Références (générée à partir des citations réellement utilisées)
{
  const s = slide("Références", "Chaque numéro correspond à un [n] placé à côté d'une information dans une diapositive", "Chaque numéro correspond à un [n] dans une diapositive.");
  const half = Math.ceil(ORDER.length / 2);
  [[0, half, X0], [half, ORDER.length, 6.85]].forEach(([a, b, x]) => {
    const items = [];
    ORDER.slice(a, b).forEach((k, i) => {
      const d = DEFS[k], m = d.match(/(arXiv:\d{4}\.\d{4,5})|(doi:\S+?)(?=[.,]?(\s|$))|(\b[a-z0-9.-]+\.(?:com|org|ai)\/\S+)/);
      let url = null;
      if (m) url = m[1] ? "https://arxiv.org/abs/" + m[1].slice(6) : m[2] ? "https://doi.org/" + m[2].slice(4) : "https://" + m[4];
      const base = { fontSize: 12, color: INK, fontFace: BODY, paraSpaceAfter: 7 };
      if (!m) { items.push({ text: `[${a + i + 1}] `, options: { ...base, bold: true, color: CORAL } }, { text: d, options: { ...base, breakLine: true } }); return; }
      const before = d.slice(0, m.index), after = d.slice(m.index + m[0].length);
      items.push({ text: `[${a + i + 1}] `, options: { ...base, bold: true, color: CORAL } }, { text: before, options: base },
        { text: m[0], options: { ...base, color: "1F5FBF", underline: { style: "sng" }, hyperlink: { url, tooltip: url } } }, { text: after, options: { ...base, breakLine: true } });
    });
    T(s, items, { x, y: 1.95, w: 5.8, h: 4.95, fontSize: 12 }); });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (applyTheme) await applyTheme(OUT, THEME); else console.log("apply_theme.js non chargé (définir PPTX_SKILL_DIR)");
  console.log("écrit :", OUT, "—", n, "diapositives ;", ORDER.length, "références :", ORDER.join(", "));
})();
