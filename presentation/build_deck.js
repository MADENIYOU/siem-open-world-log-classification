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
pres.title = "Classer les logs SIEM, reconnaître l'inconnu"; pres.author = "Madeniyou Sall"; pres.subject = "Classification hiérarchique de logs SIEM en monde ouvert (SIEVE)";
const W = 13.333, X0 = 0.7, CW = W - 2 * X0;

// ---- Gabarits : titre sombre, contenu (titre = message, à gauche, 30 pt ; numéro de diapositive ; pas d'étiquette décorative)
pres.defineSlideMaster({ title: "TITRE_SOMBRE", background: { color: NAVY }, objects: [] });
pres.defineSlideMaster({ title: "CONTENU", background: { color: "FFFFFF" },
  objects: [{ placeholder: { options: { name: "title", type: "title", x: X0, y: 0.45, w: CW, h: 1.15, fontSize: 30, bold: true, color: BLUE, fontFace: HEAD, margin: 0, valign: "top", align: "left" }, text: "" } }],
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
function slide(section, title, notes) {                // section : repère de navigation discret, en pied de page
  const s = pres.addSlide({ masterName: "CONTENU" }); n += 1;
  s.addText(title, { placeholder: "title" });
  T(s, section, { x: X0, y: 7.03, w: 9, h: 0.3, fontSize: 10, color: MUTED, valign: "middle" });
  if (notes) s.addNotes(notes); return s;
}
const chartBase = (title) => ({ showTitle: true, title, titleFontSize: 13, titleColor: BLUE, titleFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt",
  catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, dataLabelFontSize: 10, catAxisLabelColor: INK, valAxisLabelColor: MUTED, dataLabelColor: INK, valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" }, showValue: true, barGapWidthPct: 45 });
const lab = (s, text, x, y, w) => T(s, text, { x, y, w, h: 0.3, fontSize: 13, bold: true, color: BLUE });   // petit intitulé de bloc, en casse de phrase

// =====================================================================================================
// 1. Titre : schéma monde fermé / monde ouvert dessiné (porte l'idée du sujet)
{
  const s = pres.addSlide({ masterName: "TITRE_SOMBRE" }); n += 1;
  T(s, "Soutenance  ·  Traitement automatique du langage naturel", { x: 0.8, y: 0.9, w: 6.5, h: 0.35, fontSize: 14, color: STEEL });
  T(s, "Classer les logs SIEM,\nreconnaître l'inconnu", { x: 0.8, y: 1.6, w: 6.5, h: 2.3, fontSize: 46, bold: true, color: "FFFFFF", fontFace: HEAD });
  T(s, "Classification hiérarchique en monde ouvert sur le jeu SIEVE : évaluer sans fuite, détecter l'inconnu, résister aux attaques", { x: 0.8, y: 4.2, w: 6.2, h: 1.1, fontSize: 18, color: ICE });
  T(s, "Madeniyou Sall", { x: 0.8, y: 5.85, w: 6, h: 0.4, fontSize: 20, bold: true, color: "FFFFFF" });
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
  const s = slide("Introduction · Contexte", "Les violations coûtent cher, et deux tiers des alertes sont ignorées",
    "Transition : avant le sujet technique, l'enjeu. À dire : les trois sources sont des rapports de l'industrie de la sécurité ; le chiffre d'IBM vient d'un article qui cite le rapport 2026. Ce que cela implique pour nous : le tri des événements est un travail humain coûteux. Question probable : ces chiffres prouvent-ils que le tri automatique aide ? Non, ils montrent l'ampleur du problème ; notre contribution est de mesurer honnêtement ce qu'un classifieur sait faire.");
  T(s, "4,99 M$", { x: X0, y: 1.9, w: 5.8, h: 1.4, fontSize: 76, color: CORAL, fontFace: HEAD });
  P(s, [["coût moyen d'une violation de données, en hausse de 12 % en un an ", C("ibm")]], { x: X0, y: 3.3, w: 5.5, h: 0.8, fontSize: 20 });
  P(s, [["247 jours pour l'identifier et la contenir ; au-delà de 200 jours, la violation coûte 5,65 M$ contre 4,32 M$ ", C("ibm")]], { x: X0, y: 4.25, w: 5.5, h: 1.0, fontSize: 15, run: { color: MUTED } });
  hline(s, 6.9, 1.95, 5.75);
  T(s, "4 484", { x: 6.9, y: 2.1, w: 2.3, h: 0.8, fontSize: 38, color: BLUE, fontFace: HEAD });
  P(s, [["alertes par jour et par équipe SOC ; 67 % sont ignorées ", C("vectra")]], { x: 9.3, y: 2.2, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 3.25, 5.75);
  T(s, "10 626", { x: 6.9, y: 3.4, w: 2.3, h: 0.8, fontSize: 38, color: BLUE, fontFace: HEAD });
  P(s, [["violations confirmées sur 30 458 incidents analysés (année 2023) ", C("verizon")]], { x: 9.3, y: 3.5, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 4.55, 5.75);
  T(s, "Un SIEM rassemble les logs de tout le système d'information. Le goulot est humain : classer chaque événement et repérer celui qu'aucune règle ne décrit. Un classifieur qui sait dire « inconnu » réduit cette charge, à condition d'être évalué honnêtement.", { x: X0, y: 5.6, w: 9.6, h: 1.1, fontSize: 17 });
}

// 3. Problématique
{
  const s = slide("Introduction · Problématique", "Une bonne note à l'examen ne prouve rien si les questions étaient déjà dans le cours",
    "Transition : de l'enjeu à la question. À dire : les scores publiés sur SIEVE atteignent 0,97 parce que les logs viennent d'un nombre fini de gabarits et qu'un découpage aléatoire laisse le même gabarit des deux côtés. Question probable : pourquoi pas simplement un meilleur modèle ? Parce que le problème n'est pas le modèle mais ce que l'évaluation mesure.");
  T(s, "Comment classer un événement de sécurité dans une taxonomie à deux niveaux tout en reconnaissant qu'il n'appartient à aucune classe apprise, avec une évaluation qui ne triche pas ?", { x: X0, y: 1.9, w: 6.6, h: 1.9, fontSize: 22, fontFace: HEAD, color: INK });
  const q = [["1", "Que valent les scores publiés ?", "Les jeux de logs sortent de gabarits : un découpage aléatoire fait fuir l'entraînement vers le test."], ["2", "Sait-on détecter une classe jamais vue ?", "Dans un SIEM, l'inconnu est la règle."], ["3", "Le système résiste-t-il aux modifications du texte ?", "Fautes, lettres d'autres alphabets, mots ajoutés."]];
  q.forEach((r, i) => { const y = 4.1 + i * 0.95; T(s, r[0], { x: X0, y, w: 0.5, h: 0.5, fontSize: 28, color: CORAL, fontFace: HEAD }); T(s, r[1], { x: X0 + 0.6, y, w: 6, h: 0.35, fontSize: 16, bold: true, color: BLUE }); T(s, r[2], { x: X0 + 0.6, y: y + 0.36, w: 6, h: 0.4, fontSize: 13, color: MUTED }); });
  image(s, "00_sota_monde_ferme_ouvert", 7.9, 1.9, 4.75, 2.1, "Monde fermé et monde ouvert");
  P(s, [[{ b: "Ce qui existe : " }, "des classifieurs de logs évalués avec un découpage aléatoire, avec des scores de 0,93 à 0,97 ", C("sieve")], [{ b: "Ce qui manque : " }, "savoir ce que ces scores valent quand les gabarits sont nouveaux, et si l'on détecte les classes jamais vues."]], { x: 7.9, y: 4.4, w: 4.75, h: 2.3, fontSize: 14, gap: 10 });
}

// 4. Objectifs
{
  const s = slide("Introduction · Objectifs", "Le projet mesure honnêtement ; il ne construit pas un produit",
    "Transition : de la question aux objectifs. À dire : volontairement pas de fonctionnalité promise ; l'utilité est un banc d'essai. Question probable : quel est le livrable ? Un notebook exécutable, des résultats chiffrés et un protocole qu'on peut réutiliser pour comparer d'autres classifieurs de logs.");
  lab(s, "Objectif général", X0, 1.9, 4.5);
  T(s, "Mesurer jusqu'où un classifieur hiérarchique de logs sait reconnaître l'inconnu et résister aux modifications du texte, avec une évaluation qui ne fuit pas.", { x: X0, y: 2.3, w: 4.6, h: 3.0, fontSize: 22, fontFace: HEAD });
  lab(s, "Objectifs spécifiques", 6.2, 1.9, 5);
  [["Mesurer", " l'effet de la fuite entre gabarits : découpage aléatoire contre par gabarit"], ["Comparer", " des représentations : creuses, vecteurs de mots, encodeur Transformer"], ["Comparer", " huit scores d'inconnu sur cinq rotations de classes masquées"], ["Tester", " la robustesse aux attaques textuelles et la valeur réelle des parades"], ["Livrer", " un notebook reproductible, avec des règles de décision écrites avant les chiffres"]].forEach((t, i) => {
    const y = 2.35 + i * 0.7; hline(s, 6.2, y - 0.08, 6.45); P(s, [[{ b: t[0] }, t[1]]], { x: 6.2, y, w: 6.45, h: 0.6, fontSize: 16, valign: "middle", run: { color: INK } }); });
  lab(s, "Sur quoi le projet pourrait servir", X0, 6.0, 6);
  T(s, "Un protocole et un banc d'essai réutilisables pour comparer des classifieurs de logs et leurs détecteurs d'inconnu sans surestimer leurs performances. Rien de plus n'est revendiqué.", { x: X0, y: 6.32, w: 11.9, h: 0.6, fontSize: 15 });
}

// 5. État de l'art : vue d'ensemble
{
  const s = slide("État de l'art · Vue d'ensemble", "Aucun travail trouvé ne traite la classification hiérarchique de logs SIEM en monde ouvert",
    "Transition : ce qui existe. À dire : six familles de travaux, chacune avec ses références ; la recherche systématique du projet n'a trouvé aucun travail qui combine hiérarchie, logs SIEM et monde ouvert ; les 73 références ont toutes été ouvertes. Question probable : et la détection d'anomalies dans les logs ? C'est un autre problème : il sépare normal et anormal, sans classer les événements dans une taxonomie.");
  const F = [["Jeux de logs", [["SIEVE : logs SIEM synthétiques, 30 classes (Artioli et al., 2025) ", C("sieve")]]], ["Détection par le score", [["probabilité maximale (Hendrycks et Gimpel, 2017) ", C("msp"), " ; énergie (Liu et al., 2020) ", C("energy")]]],
    ["Détection par la distance", [["Mahalanobis (Lee et al., 2018) ", C("maha"), " ; kNN (Sun et al., 2022) ", C("knn"), " ; OpenMax (Bendale et Boult, 2016) ", C("openmax")]]], ["Hiérarchie", [["repli sur la famille quand la classe est incertaine (Linderman et al., 2022) ", C("lind")]]],
    ["Robustesse du texte", [["homoglyphes, table Unicode UTS #39 ", C("uts39"), " ; entraînement adversarial"]]], ["Fiabilité de l'évaluation", [["calibration (Guo et al., 2017) ", C("guo"), " ; lien fermé–ouvert (Vaze et al., 2022) ", C("vaze")]]]];
  F.forEach((f, i) => { const y = 1.95 + i * 0.7; hline(s, X0, y - 0.07, CW); T(s, f[0], { x: X0, y, w: 3.2, h: 0.55, fontSize: 16, bold: true, color: BLUE, valign: "middle" }); P(s, f[1], { x: 4.1, y, w: 8.5, h: 0.55, fontSize: 15, valign: "middle" }); });
  hline(s, X0, 6.2, CW);
  P(s, [["Recherche du projet : 73 références vérifiées, dont la page a été ouverte ", C("biblio")]], { x: X0, y: 6.3, w: CW, h: 0.4, fontSize: 13, run: { color: MUTED } });
}

// 6. État de l'art : analyse et propositions
{
  const s = slide("État de l'art · Analyse et propositions", "Chaque famille a une limite, et nos mesures les retrouvent",
    "Transition : de la liste à l'analyse. À dire : lire le tableau par ligne ; la dernière colonne est ce que nous avons observé sur nos données ; les propositions à droite répondent à ces limites. Question probable : pourquoi tester Mahalanobis alors qu'il échoue avec TF-IDF ? Parce que la littérature le donne efficace sur un Transformer affiné ; nos mesures confirment sur l'encodeur et pas sur TF-IDF.");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 13, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 13, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  s.addTable([[H("Famille"), H("Avantage"), H("Limite, et ce que nous avons mesuré")],
    [Cc("Scores de sortie", { bold: true }), Cc("Simples, sans réentraînement"), Cc("Confiance mal calibrée : calibration de 0,15 à 0,25 d'erreur")],
    [Cc("Distances", { bold: true }), Cc("Exploitent la géométrie des vecteurs"), Cc("Mahalanobis échoue avec TF-IDF (0,56) mais bat le score de sortie sur l'encodeur")],
    [Cc("Hiérarchie, repli", { bold: true }), Cc("Erreurs attendues moins graves"), Cc("Gain non démontré ; le repli propose la bonne famille une fois sur quatre")],
    [Cc("Défenses du texte", { bold: true }), Cc("Efficaces contre l'attaque connue"), Cc("Circulaires si testées avec la table de l'attaque")]],
    { x: X0, y: 1.95, w: 7.6, colW: [1.7, 2.4, 3.5], rowH: [0.45, 0.8, 0.8, 0.8, 0.8], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
  P(s, [["Mahalanobis est efficace sur un Transformer affiné dans la littérature ", C("podolskiy"), "."]], { x: X0, y: 6.15, w: 7.6, h: 0.5, fontSize: 13, run: { color: MUTED } });
  lab(s, "Nos propositions", 8.9, 1.95, 3.8);
  P(s, [[{ b: "Découpage par gabarit" }, ", test scellé et journalisé"], [{ b: "Règles écrites avant les chiffres" }, " ; réglages sans regarder les classes masquées"], [{ b: "Scores comparés" }, " sur les sorties et sur les vecteurs de l'encodeur"], [{ b: "Défenses testées" }, " avec une autre table que celle de l'attaque"]], { x: 8.9, y: 2.45, w: 3.8, h: 4.0, fontSize: 15, gap: 16 });
}

// 7. Matériel
{
  const s = slide("Matériel", "600 000 logs de SIEVE, des fichiers du professeur et un encodeur pré-entraîné",
    "Transition : après la théorie, la matière. À dire : le jeu SIEVE est la base ; les fichiers du professeur servent de contrôle de fuite ; le CDS réel n'était pas dans l'archive donc le transfert vers des logs réels n'a pas pu être fait. Question probable : les logs sont-ils réels ? Non, ils sont générés à partir de 440 gabarits issus de logs réels.");
  lab(s, "SIEVE : six versions de 100 000 logs", X0, 1.9, 6);
  ["0", "0,1", "0,2", "0,3", "0,4", "0,5"].forEach((p, i) => { const x = X0 + i * 0.98; s.addShape(pres.ShapeType.rect, { x, y: 2.35, w: 0.88, h: 0.78, fill: { color: i === 0 ? BLUE : "FFFFFF" }, line: { color: BLUE, width: 1 } }); T(s, "p = " + p, { x, y: 2.35, w: 0.88, h: 0.78, fontSize: 13, bold: true, color: i === 0 ? "FFFFFF" : BLUE, align: "center", valign: "middle" }); });
  P(s, [["30 classes équilibrées, 440 gabarits ; la perturbation p éloigne chaque log de son gabarit ", C("sieve")], ["Chaque log est un gabarit rempli de valeurs ; plus p augmente, plus des mots sont remplacés, ajoutés ou déplacés."]], { x: X0, y: 3.3, w: 5.9, h: 1.6, fontSize: 15, gap: 10 });
  const R = [["Fichiers du professeur", "6 × 35 000 logs, mêmes gabarits, valeurs nouvelles"], ["Table Unicode", ["1 447 caractères confondables (v18.0.0) ", C("uts39")]], ["Encodeur", ["DistilBERT sans casse ", C("distil"), " ; vecteurs GloVe 100 d"]], ["Taxonomie", "8 familles, hypothèse de démonstration"], ["Logs réels (CDS)", "440 logs non fournis : transfert E5 impossible"]];
  R.forEach((r, i) => { const y = 1.95 + i * 0.62; hline(s, 7.0, y - 0.05, 5.65); T(s, r[0], { x: 7.0, y, w: 1.9, h: 0.5, fontSize: 14, bold: true, color: BLUE, valign: "middle" }); P(s, [Array.isArray(r[1]) ? r[1] : [r[1]]], { x: 9.0, y, w: 3.65, h: 0.5, fontSize: 13, valign: "middle" }); });
  s.addShape(pres.ShapeType.rect, { x: X0, y: 5.2, w: CW, h: 1.65, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } });
  T(s, "Même classe (authentication-failed), deux niveaux de perturbation : fichiers du professeur", { x: X0 + 0.25, y: 5.28, w: CW - 0.5, h: 0.25, fontSize: 11, color: MUTED });
  T(s, "p = 0    [Wed Nov 03 19:30:11 1976] [error] [client 217.121.56.73] user clarkesummer: authentication failure for \"/at/challenge.png/pass\": Password Mismatch", { x: X0 + 0.25, y: 5.6, w: CW - 0.5, h: 0.55, fontSize: 12, color: INK, fontFace: MONO });
  T(s, "p = 0,5  :forauthentication [failure] /authority/car.wavhsandoval 214.18.6.71] user /: client Mismatch Thu Dec 07 03:54:44 2006 \"[Password[]air \" error", { x: X0 + 0.25, y: 6.22, w: CW - 0.5, h: 0.55, fontSize: 12, color: INK, fontFace: MONO });
}

// 8. Méthodes
{
  const s = slide("Méthodes", "Quatre étapes séparent le texte brut de la décision d'accepter ou de rejeter",
    "Transition : de la matière à la méthode. À dire : lire de gauche à droite ; le seuil de rejet est calé sur 95 % des logs connus de validation ; les classes masquées servent seulement à mesurer. Question probable : pourquoi huit scores ? Parce que la littérature n'en désigne pas un meilleur dans notre cas ; on compare avec des règles écrites d'avance.");
  const cols = [["Représenter", [["Creuses : sac de mots, TF-IDF, n-grammes"], ["Vecteurs de mots : Word2Vec, FastText, GloVe"], ["Contextuelle : DistilBERT ", C("distil")]]], ["Classer", [["Plat : une tête sur les classes"], ["Hiérarchique : p(famille) × p(classe | famille) ", C("lind")], ["Encodeur à deux têtes"]]],
    ["Détecter l'inconnu", [["Scores : MSP ", C("msp"), ", énergie ", C("energy"), ", prototype, ensemble"], ["Distances : Mahalanobis ", C("maha"), ", kNN ", C("knn"), ", OpenMax ", C("openmax")], ["Seuil à 95 % des connus"]]], ["Évaluer", [["Découpage par gabarit, test scellé"], ["5 rotations de 6 classes masquées"], ["Intervalles par gabarit ", C("field")]]]];
  cols.forEach((c, i) => { const x = X0 + i * 3.05; if (i > 0) s.addShape(pres.ShapeType.line, { x: x - 0.22, y: 2.0, w: 0, h: 3.2, line: { color: LINE, width: 0.75 } });
    T(s, String(i + 1) + "  " + c[0], { x, y: 1.95, w: 2.7, h: 0.5, fontSize: 18, bold: true, color: BLUE }); P(s, c[1], { x, y: 2.65, w: 2.7, h: 2.6, fontSize: 16, gap: 14 }); });
  hline(s, X0, 5.55, CW);
  lab(s, "Robustesse et fiabilité", X0, 5.75, 4);
  P(s, [["Attaques : fautes de frappe, homoglyphes, mots ajoutés  ·  Parades : normalisation Unicode ", C("uts39"), ", entraînement adversarial  ·  Calibration par température ", C("guo")]], { x: X0, y: 6.1, w: CW, h: 0.7, fontSize: 16 });
}

// 9. Présentation des données : mosaïque (une grande figure et quatre moyennes)
{
  const s = slide("Présentation des données", "Les logs viennent de 440 gabarits : la structure des données guide toute l'évaluation",
    "Transition : de la méthode aux données. À dire : en haut les chiffres, puis la taxonomie en 8 familles, les 5 rotations de classes masquées, la reconstruction des gabarits (311 retrouvés sur 440) et l'effet de la perturbation p. Question probable : comment avez-vous retrouvé les gabarits ? En regroupant les logs qui se ressemblent après masquage des valeurs, puis en vérifiant le nombre contre le tableau de l'article.");
  P(s, [[{ b: "600 000" }, " logs   ·   ", { b: "30" }, " classes   ·   ", { b: "440" }, " gabarits (", { b: "311" }, " retrouvés)   ·   ", { b: "8" }, " familles   ·   ", { b: "5 × 6" }, " classes masquées   ·   ", { b: "6" }, " niveaux de perturbation"]], { x: X0, y: 1.75, w: CW, h: 0.4, fontSize: 16, run: { color: BLUE } });
  image(s, "00_taxonomie", X0, 2.3, 6.2, 2.7, "Taxonomie : 30 classes en 8 familles"); T(s, "Taxonomie : 30 classes en 8 familles", { x: X0, y: 5.02, w: 6.2, h: 0.28, fontSize: 11, color: MUTED });
  image(s, "00_rotations", X0, 5.4, 6.2, 1.3, "Cinq rotations de classes masquées"); T(s, "Cinq rotations de six classes masquées", { x: X0, y: 6.72, w: 6.2, h: 0.28, fontSize: 11, color: MUTED });
  image(s, "02_gabarits", 7.2, 2.3, 5.45, 2.0, "Gabarits reconstruits et effet de p"); T(s, "Gabarits reconstruits (311 sur 440) et effet de p", { x: 7.2, y: 4.32, w: 5.45, h: 0.28, fontSize: 11, color: MUTED });
  image(s, "03_fuite_gabarits", 7.2, 4.7, 5.45, 1.9, "Fuite entre gabarits"); T(s, "Fuite entre gabarits : plus proches voisins entre entraînement et test", { x: 7.2, y: 6.62, w: 5.45, h: 0.28, fontSize: 11, color: MUTED });
}

// 10. Librairies
{
  const s = slide("Librairies utilisées", "Un socle scientifique classique, en versions figées",
    "Transition : des données aux outils. À dire : tout est dans requirements.txt du dépôt avec les versions exactes. Question probable : pourquoi PyTorch et Transformers seulement pour l'encodeur ? Parce que tous les autres modèles sont linéaires, donc scikit-learn suffit.");
  const L = [["Données et calcul", "numpy 2.5.4  ·  pandas 3.1.1  ·  scipy 1.18.1"], ["Apprentissage automatique", "scikit-learn 1.9.1  ·  joblib 1.6.0"], ["Texte et vecteurs de mots", "gensim 4.4.0  ·  nltk 3.10.4"], ["Apprentissage profond", "PyTorch 2.15.0  ·  Transformers 5.22.1  ·  tokenizers 0.23.3"], ["Visualisation", "matplotlib 3.11.2"], ["Exécution et reproductibilité", "ipykernel 7.4.0  ·  nbclient 0.11.0  ·  nbformat 5.11.1"], ["Langage", "Python 3.12"]];
  L.forEach((l, i) => { const y = 1.95 + i * 0.68; hline(s, X0, y - 0.08, CW); T(s, l[0], { x: X0, y, w: 4.2, h: 0.5, fontSize: 17, bold: true, color: BLUE, valign: "middle" }); T(s, l[1], { x: 5.2, y, w: 7.45, h: 0.5, fontSize: 14, fontFace: MONO, valign: "middle" }); });
  hline(s, X0, 6.72, CW);
}

// 11. Environnement d'exécution : schéma de flux
{
  const s = slide("Environnement d'exécution", "Le calcul est réparti sur un Mac et Colab, et reprend là où il s'est arrêté",
    "Transition : des outils à l'exécution. À dire : les entraînements d'encodeur tournent sur le GPU du Mac ou sur Colab ; chaque résultat est sauvegardé donc une interruption ne fait pas tout refaire. Question probable : pourquoi pas tout sur Colab ? Le quota de GPU gratuit s'épuise vite ; répartir a évité de perdre du temps.");
  const box = (x, y, w, h, t1, t2, fill) => { s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: fill || "FFFFFF" }, line: { color: BLUE, width: 1.25 } }); T(s, t1, { x: x + 0.2, y: y + 0.12, w: w - 0.4, h: 0.4, fontSize: 16, bold: true, color: fill ? "FFFFFF" : BLUE }); T(s, t2, { x: x + 0.2, y: y + 0.55, w: w - 0.4, h: h - 0.6, fontSize: 13, color: fill ? ICE : INK }); };
  box(X0, 1.95, 4.0, 1.5, "Mac, puce M3 Pro", "Modèles linéaires, vecteurs de mots ; encodeur : rotations 3 à 5, graines 42, 43, 44 ; GPU Apple");
  box(X0, 3.75, 4.0, 1.5, "Google Colab", "GPU T4 ; encodeur : première validation, rotations 1 et 2");
  box(5.7, 2.85, 2.5, 1.5, "Notebook", "Python 3.12, Jupyter, nbclient", BLUE);
  box(9.2, 2.85, 3.43, 1.5, "Dépôt GitHub public", "Notebook, résultats, figures, code ; sans les données SIEVE");
  const arrow = (x1, y1, x2, y2) => s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipV: y2 < y1, line: { color: CORAL, width: 1.75, endArrowType: "triangle" } });
  arrow(X0 + 4.0, 2.7, 5.7, 3.35); arrow(X0 + 4.0, 4.5, 5.7, 3.85); arrow(8.2, 3.6, 9.2, 3.6);
  hline(s, X0, 5.7, CW);
  P(s, [[{ b: "13 à 20 min" }, " par encodeur (2 époques)   ·   ", { b: "15 modèles" }, " (3 graines × 5 rotations)   ·   ", { b: "≈ 13 min" }, " pour rejouer tout le notebook   ·   reprise automatique après interruption"]], { x: X0, y: 5.9, w: CW, h: 0.8, fontSize: 16 });
}

// 12. Pipeline : ligne de métro (nœuds reliés), sans cartes
{
  const s = slide("Conception · Pipeline utilisé", "Onze étapes, dont le découpage par gabarit est celle qui change le plus les conclusions",
    "Transition : de l'environnement au déroulé. À dire : chaque étape a ses décisions justifiées dans le notebook ; la 3 est en couleur car c'est elle qui a fait passer le score de 0,97 à 0,46. Question probable : pourquoi 11 étapes ? Elles suivent la consigne du projet (cadrage à conclusion) avec les sous-étapes que nous avons ajoutées.");
  const P_ = [["Cadrage", "Question, hypothèses H1 à H15, critères de succès"], ["Données", "Acquisition, audit du format"], ["Exploration", "Classes proches, gabarits, effet de p"], ["Découpage", "Par gabarit, test scellé, protocoles P0 à P3"], ["Prétraitement", "Pipeline de texte, 10 variantes"], ["Représentations", "Creuses, vecteurs de mots, encodeur"],
    ["Modèles", "Plat, hiérarchique, huit scores d'inconnu"], ["Évaluation", "Test scellé : E1 à E3"], ["Robustesse", "Attaques textuelles, E4"], ["Amélioration", "Parades, calibration"], ["Conclusion", "Registre de 99 affirmations, limites"]];
  const rows = [[0, 6, 2.0], [6, 11, 4.55]];
  rows.forEach(([a, b, y]) => { const cnt = b - a, step = 2.05, x0 = X0 + 0.6 + (cnt < 6 ? step / 2 : 0); s.addShape(pres.ShapeType.line, { x: x0, y: y + 0.28, w: step * (cnt - 1), h: 0, line: { color: STEEL, width: 2 } });
    for (let i = a; i < b; i++) { const cx = x0 + (i - a) * step, hot = i === 3;
      s.addShape(pres.ShapeType.ellipse, { x: cx - 0.28, y, w: 0.56, h: 0.56, fill: { color: hot ? CORAL : BLUE }, line: { color: "FFFFFF", width: 2 } }); T(s, String(i), { x: cx - 0.28, y, w: 0.56, h: 0.56, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
      T(s, P_[i][0], { x: cx - 0.95, y: y + 0.7, w: 1.9, h: 0.35, fontSize: 15, bold: true, color: hot ? CORAL : BLUE, align: "center" }); T(s, P_[i][1], { x: cx - 0.95, y: y + 1.08, w: 1.9, h: 1.2, fontSize: 13.5, align: "center" }); } });
}

// 13. Résultats : graphiques natifs
{
  const s = slide("Conception · Présentation et analyse des résultats", "De 0,97 à 0,46 : c'est le découpage, pas le modèle, qui fait l'écart",
    "Transition : du déroulé aux résultats. À dire : en haut à gauche la fuite, en haut à droite la détection, en bas les attaques et la défense. Question probable : le 0,97 est-il faux ? Non, il est exact, mais il mesure la reconnaissance de gabarits déjà vus. Détail des valeurs : découpage aléatoire 0,987, par gabarit 0,422, groupes 0,507, imbriquée 0,511, test scellé 0,483 ; AUROC de TF-IDF 0,728 en validation puis 0,599 au test, encodeur 0,548 et 0,605 avec Mahalanobis ; attaques fortes en pourcentage de perte de F1 ; défense 10,8, 0,0, 8,7 et 0,1.");
  const cw = 5.95, ch = 2.25, X1 = X0 + cw + 0.3;
  s.addChart(pres.charts.BAR, [{ name: "macro-F1", labels: ["Aléatoire", "Par gabarit", "Groupes", "Imbriquée", "Test scellé"], values: [0.987, 0.422, 0.507, 0.511, 0.483] }], Object.assign(chartBase("Fuite : macro-F1 selon le découpage"), { x: X0, y: 1.75, w: cw, h: ch, barDir: "col", chartColors: [STEEL, BLUE, BLUE, BLUE, CORAL], valAxisMaxVal: 1, valAxisMinVal: 0, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", showLegend: false }));
  s.addChart(pres.charts.BAR, [{ name: "AUROC", labels: ["TF-IDF val.", "TF-IDF test", "Encodeur MSP", "Encodeur + Mahalanobis"], values: [0.728, 0.599, 0.548, 0.605] }], Object.assign(chartBase("Détection d'inconnus : AUROC (0,5 = hasard)"), { x: X1, y: 1.75, w: cw, h: ch, barDir: "col", chartColors: [STEEL, BLUE, STEEL, CORAL], valAxisMaxVal: 1, valAxisMinVal: 0.4, valAxisMajorUnit: 0.2, dataLabelFormatCode: "0.00", showLegend: false }));
  s.addChart(pres.charts.BAR, [{ name: "Mots", labels: ["Fautes", "Homoglyphes", "Mots ajoutés"], values: [7.8, 21.5, 12.5] }, { name: "Caractères", labels: ["Fautes", "Homoglyphes", "Mots ajoutés"], values: [4.0, 10.6, 14.4] }], Object.assign(chartBase("Attaques fortes : perte relative de F1 (%)"), { x: X0, y: 4.1, w: cw, h: ch, barDir: "col", chartColors: [BLUE, STEEL], valAxisMinVal: 0, dataLabelFormatCode: "0.0", showLegend: true, legendPos: "b", legendFontSize: 10, legendColor: INK }));
  s.addChart(pres.charts.BAR, [{ name: "perte", labels: ["Sans défense", "Table maison\n(sa propre attaque)", "Table maison\n(table officielle)", "Table officielle\ncomplète"], values: [10.8, 0.0, 8.7, 0.1] }], Object.assign(chartBase("Défense homoglyphes : perte relative de F1 (%)"), { x: X1, y: 4.1, w: cw, h: ch, barDir: "col", chartColors: [STEEL, BLUE, CORAL, BLUE], valAxisMinVal: 0, dataLabelFormatCode: "0.0", showLegend: false }));
  T(s, "Le découpage fait l'essentiel de l'écart ; la détection reste faible ; une défense se teste contre une autre table que celle de l'attaque.", { x: X0, y: 6.5, w: CW, h: 0.4, fontSize: 15, bold: true, color: BLUE });
}

// 14. Limites : tableau limite -> conséquence
{
  const s = slide("Conception · Limites de la conception", "Six limites bornent ce que l'on peut affirmer",
    "Transition : des résultats à leurs limites. À dire : chaque ligne dit ce que la limite change dans les conclusions ; ces limites sont aussi dans le README et dans la section 10.6 du notebook. Question probable : laquelle pèse le plus ? Les données synthétiques : sans logs réels, on ne sait pas si les conclusions se transfèrent.");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 14, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 14, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  s.addTable([[H("Limite"), H("Ce que cela change pour les conclusions")],
    [Cc("Données synthétiques : 440 gabarits, 311 reconstruits", { bold: true }), Cc("Les scores mesurent des gabarits, pas des logs réels")],
    [Cc("Taxonomie non validée par un expert SIEM", { bold: true }), Cc("Les 8 familles restent une hypothèse de démonstration")],
    [Cc("36 gabarits en validation, 45 au test", { bold: true }), Cc("Un écart inférieur à 0,05 est indétectable")],
    [Cc("Trois graines pour l'encodeur, une pour la plupart des autres modèles", { bold: true }), Cc("Le bruit d'entraînement n'est pas toujours mesuré")],
    [Cc("Test déjà ouvert", { bold: true }), Cc("Les scores ajoutés ensuite sont comparés sur la validation seulement")],
    [Cc("Pas de logs réels (E5) ; attaques surtout non adaptatives", { bold: true }), Cc("Aucune garantie face à un attaquant qui connaît le modèle")]],
    { x: X0, y: 1.95, w: CW, colW: [6.2, 5.73], rowH: [0.5, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
}

// 15. Conclusion : asymétrique (chiffres à retenir à gauche, limites et perspectives à droite)
{
  const s = slide("Conclusion", "Évaluer par gabarit change la conclusion ; détecter l'inconnu reste un problème ouvert",
    "Transition : des limites à la conclusion. À dire : quatre chiffres suffisent pour résumer le travail ; à droite ce qui borne ces chiffres et ce que nous ferions ensuite. Question probable : que feriez-vous en premier ? Valider la taxonomie avec un expert SIEM et tester sur des logs réels, car c'est ce qui conditionne le reste.");
  lab(s, "À retenir", X0, 1.9, 4);
  [["0,97 → 0,46", "de macro-F1 quand on sépare les logs par gabarit"], ["0,60", "d'AUROC pour détecter l'inconnu au test (0,5 = hasard)"], ["+ 0,057", "pour Mahalanobis sur l'encodeur affiné, contre le score de sortie ", "podolskiy"], ["≈ 0,001", "de perte avec la table officielle complète ; la table de l'attaque ne protégeait que parce qu'elle la connaissait"]].forEach((r, i) => {
    const y = 2.35 + i * 1.12; hline(s, X0, y - 0.08, 6.9); T(s, r[0], { x: X0, y, w: 2.6, h: 0.9, fontSize: 30, color: CORAL, fontFace: HEAD, valign: "middle" }); P(s, [r[2] ? [r[1], C(r[2])] : [r[1]]], { x: X0 + 2.8, y, w: 4.1, h: 0.9, fontSize: 14, valign: "middle" }); });
  lab(s, "Limites", 8.3, 1.9, 4);
  P(s, [["Taxonomie non validée, gabarits reconstruits"], ["Trois graines, peu de gabarits de test"], ["Pas de logs réels : transfert E5 non fait"]], { x: 8.3, y: 2.3, w: 4.35, h: 1.8, fontSize: 14, gap: 8 });
  lab(s, "Perspectives", 8.3, 4.3, 4);
  P(s, [["Valider la taxonomie avec un expert SIEM"], ["Tester sur des logs réels"], ["Plus de graines, covariance par classe, attaques adaptatives"]], { x: 8.3, y: 4.7, w: 4.35, h: 2.0, fontSize: 14, gap: 8 });
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
  const s = slide("Références", "Références citées dans la présentation", "Chaque numéro correspond à un [n] dans une diapositive.");
  const half = Math.ceil(ORDER.length / 2);
  [[0, half, X0], [half, ORDER.length, 6.85]].forEach(([a, b, x]) => {
    const items = ORDER.slice(a, b).map((k, i) => [[{ b: `[${a + i + 1}] ` }, DEFS[k]]]).map((p) => p[0]);
    T(s, runs(items, { gap: 7 }), { x, y: 1.75, w: 5.8, h: 5.1, fontSize: 12 }); });
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (applyTheme) await applyTheme(OUT, THEME); else console.log("apply_theme.js non chargé (définir PPTX_SKILL_DIR)");
  console.log("écrit :", OUT, "—", n, "diapositives ;", ORDER.length, "références :", ORDER.join(", "));
})();
