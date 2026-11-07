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
  loghub: "Zhu, He, He, Liu, Zheng, Lyu. Loghub: A Large Collection of System Log Datasets towards Automated Log Analytics. arXiv:2008.06448, 2020",
  deeplog: "Du, Li, Zheng, Srikumar. DeepLog: Anomaly Detection and Diagnosis from System Logs through Deep Learning. ACM CCS 2017. dblp.dagstuhl.de/rec/conf/ccs/Du0ZS17.html",
  logbert: "Guo, Yuan, Wu. LogBERT: Log Anomaly Detection via BERT. arXiv:2103.04475, 2021",
  karlsen: "Karlsen et al. Benchmarking Large Language Models for Log Analysis, Security, and Interpretation. arXiv:2311.14519, 2023",
  sklcv: "scikit-learn. Cross-validation: evaluating estimator performance (documentation). scikit-learn.org/stable/modules/cross_validation.html",
  cawley: "Cawley, Talbot. On Over-fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation. Journal of Machine Learning Research 11, 2010. jmlr.org/papers/v11/cawley10a.html",
  silla: "Silla, Freitas. A survey of hierarchical classification across different application domains. Data Mining and Knowledge Discovery 22, 2011. doi:10.1007/s10618-010-0175-9",
  hiagm: "Zhou et al. Hierarchy-Aware Global Model for Hierarchical Text Classification. ACL 2020. aclanthology.org/2020.acl-main.104",
  hitin: "Zhu et al. HiTIN: Hierarchy-aware Tree Isomorphism Network for Hierarchical Text Classification. ACL 2023. arXiv:2305.15182",
  bertinetto: "Bertinetto et al. Making Better Mistakes: Leveraging Class Hierarchies with Deep Networks. CVPR 2020. arXiv:1912.09393",
  kwon: "Kwon et al. Classification hiérarchique de texte avec étiquettes inconnues. Findings of EACL 2023. aclanthology.org/2023.findings-eacl.46",
  odin: "Liang, Li, Srikant. Enhancing the Reliability of Out-of-distribution Image Detection in Neural Networks. ICLR 2018. arXiv:1706.02690",
  vim: "Wang, Li, Feng, Zhang. ViM: Out-Of-Distribution with Virtual-logit Matching. CVPR 2022. arXiv:2203.10807",
  ens: "Lakshminarayanan, Pritzel, Blundell. Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles. NeurIPS 2017. arXiv:1612.01474",
  mcd: "Gal, Ghahramani. Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning. ICML 2016. arXiv:1506.02142",
  oe: "Hendrycks, Mazeika, Dietterich. Deep Anomaly Detection with Outlier Exposure. ICLR 2019. arXiv:1812.04606",
  baran: "Baran et al. Classical out-of-distribution detection methods benchmark in text classification tasks. arXiv:2307.07002, 2023",
  dalvi: "Dalvi, Domingos, Mausam, Sanghai, Verma. Adversarial Classification. KDD 2004. homes.cs.washington.edu/~pedrod/papers/kdd04.pdf",
  lowd: "Lowd, Meek. Good Word Attacks on Statistical Spam Filters. CEAS 2005. ceas.cc/2005/papers/125.pdf",
  boucher: "Boucher, Shumailov, Anderson, Papernot. Bad Characters: Imperceptible NLP Attacks. IEEE S&P (arXiv 2021). arXiv:2106.09898",
  pruthi: "Pruthi, Dhingra, Lipton. Combating Adversarial Misspellings with Robust Word Recognition. ACL 2019. arXiv:1905.11268",
  jones: "Jones, Jia, Raghunathan, Liang. Robust Encodings: A Framework for Combating Adversarial Typos. ACL 2020. arXiv:2005.01229",
  textfooler: "Jin, Jin, Zhou, Szolovits. Is BERT Really Robust? A Strong Baseline for Natural Language Attack on Text Classification and Entailment. AAAI 2020. arXiv:1907.11932",
  hotflip: "Ebrahimi, Rao, Lowd, Dou. HotFlip: White-Box Adversarial Examples for Text Classification. ACL 2018. arXiv:1712.06751",
  desai: "Desai, Durrett. Calibration of Pre-trained Transformers. EMNLP 2020. arXiv:2003.07892",
  ovadia: "Ovadia et al. Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift. NeurIPS 2019. arXiv:1906.02530",
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
const NOTES = {"1": "Bonjour. Mon sujet tient en une question : un programme qui trie des journaux de sécurité sait-il aussi dire « ça, je ne connais pas » ?\n\nImaginez un standardiste qui doit orienter chaque appel vers l'un de trente services. Si un appel ne correspond à aucun service, un mauvais standardiste l'envoie quand même quelque part. Un bon standardiste dit : « celui-là, je ne sais pas, je le signale ». C'est exactement le schéma à droite. En haut, dans le monde fermé, tout est rangé de force, donc l'erreur est invisible. En bas, dans le monde ouvert, ce qui est loin de tout ce qu'on connaît reçoit un point d'interrogation.\n\nCe que la diapositive ne dit pas : je ne vais pas vous présenter un programme miracle. Mon message est qu'il faut se méfier de la façon dont on note ces programmes, parce que les scores publiés sur ce jeu de données sont trop beaux. Mon plan suit trois questions : que valent ces scores, sait-on repérer l'inconnu, et le système résiste-t-il quand on abîme le texte.", "2": "Je commence par l'enjeu, avec trois sources que j'ai ouvertes une par une.\n\nLe plus gros chiffre, 4,99 millions de dollars, vient du rapport IBM sur le coût des violations de données, dans l'édition 2026. Ce que la diapositive ne montre pas, c'est le lien avec le temps : il faut en moyenne 247 jours pour identifier et contenir une violation, et au-delà de 200 jours elle coûte 5,65 millions de dollars contre 4,32 en dessous. Détecter vite fait donc économiser de l'argent.\n\nLe deuxième chiffre vient d'une enquête auprès de 2 000 analystes : une équipe reçoit 4 484 alertes par jour et en ignore 67 %. Ce n'est pas de la paresse, c'est que personne ne peut tout lire. Le SIEM est le logiciel qui centralise ces alertes. Si un programme trie ce qui est connu et signale ce qui ne l'est pas, il redonne du temps aux humains.\n\nDeux précautions. Ces rapports sont écrits par des acteurs de la sécurité, donc je les prends comme des ordres de grandeur. Et ils ne prouvent pas que ma méthode aide : ils montrent seulement que le problème est réel.", "3": "Voici la question centrale, avec une image : un élève qui s'entraîne sur les annales, puis qui passe un examen contenant les mêmes questions. Sa note est excellente, mais elle ne prouve pas qu'il a compris.\n\nC'est ce qui arrive avec ce jeu de données. Les logs sont fabriqués en remplissant environ 440 phrases types, les gabarits, avec des valeurs différentes. Si on mélange tout au hasard puis qu'on coupe entre entraînement et test, la même phrase type se retrouve des deux côtés. Le programme reconnaît la phrase, il ne comprend rien de plus. D'où des scores publiés entre 0,93 et 0,97.\n\nCe que la diapositive ne dit pas : quand je sépare par phrase type, le score tombe autour de 0,46 à 0,48. Le problème n'est donc pas le modèle, c'est ce que l'évaluation mesure. Les trois questions numérotées sont les trois parties de mon exposé. Et pour l'inconnu : dans un SIEM, ce n'est pas un cas rare, c'est ce qui arrive le jour où une nouvelle attaque apparaît.", "4": "Mon objectif est volontairement modeste : mesurer, pas construire un produit. Je n'ai pas inventé de fonctionnalité, parce que ce n'est pas l'objet du projet.\n\nCe qui donne de la valeur à cette mesure, c'est la discipline derrière les cinq objectifs. Premier point : j'ai écrit mes quinze hypothèses et les règles de décision avant de voir les chiffres, avec pour chacune ce qui la réfuterait. Deux ont été réfutées, les hypothèses H1 et H13, et je les garde dans le rapport au lieu de les cacher. Deuxième point : le jeu de test est scellé. Il n'a été ouvert qu'une fois, avec une trace datée, et mes choix étaient figés avant.\n\nL'utilité à long terme est un banc d'essai : quelqu'un qui veut comparer un autre programme de classement de logs peut rejouer le notebook et se comparer sans surestimer ses résultats. Rien de plus n'est revendiqué.", "5": "Pour ne pas me perdre dans la littérature, je l'ai découpée en cinq blocs, du plus concret au plus technique. A : les logs et la façon de séparer entraînement et test, parce que tout dépend de là. B : la hiérarchie, pour se tromper moins gravement. C : la détection d'inconnus, le cœur du projet. D : que se passe-t-il si un attaquant abîme le texte. E : la calibration, c'est-à-dire si la confiance du modèle est honnête. Pour chaque bloc, je vous montre ce qui existe, sa limite, et ce que j'en retiens.\n\nCe que la diapositive ne dit pas : la recherche a été faite le 5 novembre 2026, dans arXiv, l'ACL Anthology, des pages d'éditeurs et une base de citations. J'ai ouvert la page de 73 références. Dans ce protocole, je n'ai trouvé aucun travail qui traite ensemble hiérarchie, logs SIEM et monde ouvert. Je le dis prudemment : aucune base n'est exhaustive. Ce que je revendique, c'est une évaluation sans fuite avec une comparaison systématique, pas une méthode meilleure que toutes les autres.", "6": "Bloc A, les données. Pour les logs, la littérature fait surtout deux choses. Détecter des séquences anormales, avec DeepLog ou LogBERT : c'est un autre problème, car ils ne disent pas de quel type d'événement il s'agit. Ou classer avec des modèles de langue : Karlsen et ses collègues annoncent 0,998 de F1 sur six jeux, mais le résumé ne décrit pas le découpage, donc je ne peux ni affirmer ni exclure une fuite.\n\nPour SIEVE, les auteurs annoncent 0,93 à 0,97. Chez moi, un SVM obtient 0,9735 avec un découpage au hasard, l'article annonce 0,9737 : je reproduis donc leur résultat, puis je montre que par gabarit on tombe à 0,458. Autre chiffre : au hasard, 24 % des logs de test ont un quasi-jumeau dans l'entraînement, contre 1 % par gabarit.\n\nCe que j'en retiens : un découpage par gabarit, une validation croisée par groupes et imbriquée, et un test scellé.", "7": "Bloc B, la hiérarchie. Trois raisons de s'en servir. Un : toutes les erreurs ne se valent pas. Prendre un échec d'authentification pour un succès est proche dans l'arbre, mais attention, en sécurité cette erreur-là peut cacher une attaque : je garde donc aussi une analyse par paires de classes. Deux : la famille est plus facile à prédire, 0,67 de macro-F1 contre 0,46 pour la classe fine. Trois : en monde ouvert, on peut répondre au niveau de la famille quand le détail est incertain, c'est l'idée de Linderman et ses collègues, en vision.\n\nDans la littérature sur le texte, la hiérarchie est traitée en monde fermé, et Kwon et ses collègues écrivent que gérer des étiquettes inconnues avec une hiérarchie est un problème encore ouvert.\n\nCe que je retiens : une approche locale, avec deux têtes, où la probabilité d'une classe est le produit des deux niveaux. Sa faiblesse : si la famille est fausse, la bonne classe est hors de portée. C'est une des raisons pour lesquelles le gain n'est pas démontré chez moi.", "8": "Bloc C, le cœur du projet. Un classifieur ordinaire n'a pas de case « inconnu » : ses probabilités font toujours 1, donc il range de force.\n\nLa littérature propose quatre familles. Le score de sortie : la probabilité maximale, l'énergie, ODIN, OpenMax. La distance dans l'espace interne : Mahalanobis, kNN, ViM. L'incertitude : plusieurs modèles, ou le dropout. Et un entraînement spécial avec des exemples d'inconnus.\n\nDeux avertissements. Vaze et ses collègues : un bon classifieur fermé suffit presque, la capacité à rejeter suit son exactitude. Baran et ses collègues : en texte, les méthodes classiques ratent beaucoup de décalages.\n\nCe que je retiens : comparer huit scores sur les mêmes classes masquées, avec un seuil réglé sur les classes connues seulement. J'ai écarté ODIN, parce qu'il perturbe l'entrée et que cela n'a pas de sens pour du texte, et Outlier Exposure, parce qu'il exige des exemples d'inconnus. Un chiffre à garder : mon seuil visait 5 % de connus rejetés, il en rejetait 9 à 13 % au test.", "9": "Bloc D, un attaquant qui modifie le texte. Dans un SIEM, une partie du log est contrôlée par l'attaquant : nom d'utilisateur, adresse web, nom de fichier. C'est le jeu des spammeurs contre les filtres. Lowd et Meek montrent que la moitié du spam bloqué passe avec 150 mots ajoutés ou moins, à condition de choisir des mots fréquents : des mots au hasard sont inefficaces. Boucher et ses collègues montrent qu'un seul changement invisible, comme un homoglyphe, peut dégrader un modèle. La défense qu'ils recommandent : assainir l'entrée.\n\nCe que je retiens : trois attaques, chacune à trois degrés ; la normalisation avec la table officielle Unicode comme garde-fou, l'entraînement adversarial en renfort. Un fait utile : la normalisation Unicode standard, NFKC, ne corrige pas les homoglyphes. Je l'ai vérifié : le « a » cyrillique n'est pas une variante de compatibilité.\n\nHors périmètre : les attaques par synonymes ou par gradient, trop coûteuses pour une entrée discrète.", "10": "Bloc E, la calibration. Un modèle est calibré si, quand il se dit sûr à 90 %, il a raison 9 fois sur 10. On le vérifie par un diagramme de fiabilité et un nombre, l'ECE, l'écart moyen entre confiance annoncée et réalité. La correction classique est la température : on divise les scores par un nombre avant de calculer les probabilités.\n\nCe que la diapositive ne dit pas : la température change les probabilités mais pas leur ordre, donc elle ne change ni la classe prédite ni la détection d'inconnus. Ovadia et ses collègues montrent que sous décalage de données, la calibration se dégrade. C'est ce que je mesure : sur l'encodeur, l'ECE passe de 0,18 en validation à 0,35 au test, avec 85 % de confiance annoncée pour 50 % de bonnes réponses. Pour TF-IDF, la température ramène l'ECE de 0,150 à 0,095 sans effet sur l'AUROC. Ce que je retiens : mesurer l'ECE avant et après, sans lui demander de résoudre la détection d'inconnus.", "11": "Voici ma matière première. SIEVE : six fichiers de 100 000 logs, de p = 0, le texte propre, à p = 0,5, le texte très abîmé. Ils sont générés à partir de 440 gabarits réels, en 30 classes équilibrées, soit 20 000 logs par classe. Le jeu n'est pas redistribué, il est fourni sur demande par ses auteurs : mon dépôt public ne contient donc pas les données.\n\nLe professeur m'a fourni six autres fichiers de 35 000 logs, mêmes gabarits, valeurs nouvelles. Je m'en sers comme contrôle de la fuite : un modèle qui a vu tous les gabarits y obtient 0,97, un modèle dont le gabarit vient du test 0,44.\n\nCôté outils : la table Unicode de 1 447 caractères confondables, DistilBERT, une version allégée de BERT, et mon regroupement des classes en huit familles, qui reste une hypothèse. Enfin, aucun log réel : les 440 logs réels du CDS ne sont pas dans l'archive reçue, donc je n'ai pas pu tester en conditions réelles.", "12": "Voici ce que j'ai fait dans le notebook, sous forme de boucle. Un : la vectorisation, transformer le texte en nombres, de trois façons, du simple comptage de mots au réseau Transformer. Deux : la classification, choisir la famille puis la classe. Trois : la détection d'inconnus, donner à chaque log une note d'étrangeté, par la confiance ou par la distance, avec un seuil qui garde 95 % des connus. Quatre : l'évaluation, mais sur la validation : découpage par gabarit, cinq rotations de classes masquées. Cinq : la robustesse et la calibration, attaquer, défendre, corriger la confiance.\n\nPourquoi une boucle : à chaque tour, je règle sur la validation, et si je trouve un défaut, je repars. Deux exemples vécus : la défense circulaire, corrigée à l'étape 9, et le seuil de rejet qui laissait passer 80 à 89 % des inconnus.\n\nEt à droite, hors de la boucle : le test scellé. Il ne sert qu'une fois, à la fin, quand tous les choix sont figés, avec une trace datée dans le notebook. S'il servait dans la boucle, je réglerais sur lui et il ne mesurerait plus rien. Une règle absolue : les réglages se font sans jamais regarder les classes masquées.", "13": "Les données, en trois temps. Premier temps : 30 classes équilibrées, soit 20 000 logs par classe sur l'ensemble. Une classe est un type d'événement, par exemple un échec d'authentification.\n\nDeuxième temps : les huit familles. C'est mon regroupement, adossé à un schéma standard de l'industrie, ECS. Aucun expert SIEM ne l'a validé, donc c'est une hypothèse de démonstration, et je le redis en limite. L'intérêt : se tromper entre authentication-failed et authentication-success est une erreur moins grave que prendre un échec de connexion pour une suppression de fichier.\n\nTroisième temps, les repères R1 à R5. Pour tester l'inconnu, il faut cacher des classes pendant l'entraînement, sinon ce ne serait pas de l'inconnu. À chaque rotation, six classes sont cachées. Au bout de cinq rotations, chaque classe a joué une fois le rôle de l'inconnue, et le résultat ne dépend pas d'un seul choix de classes.", "14": "Une clarification qui m'a été demandée : il n'y a qu'un seul jeu de données. Les auteurs de SIEVE partent de logs réels publics, Loghub, OSSEC et Public Security Log Sharing Site. Ils en tirent 440 gabarits, des phrases à trous, validés par trois spécialistes SIEM, répartis en 30 classes. À partir de ces gabarits, ils génèrent les six fichiers de 100 000 logs, de plus en plus abîmés. Tous mes modèles sont entraînés et testés sur ces logs.\n\nLes 311 gabarits que j'ai reconstitués ne forment pas un autre jeu : c'est un regroupement des mêmes logs, utilisé uniquement pour séparer entraînement et test. En bas, l'exemple : le gabarit, un log qui le remplit, le même log abîmé à p = 0,5.\n\nLimite que je dis d'avance : les 440 logs réels du CDS ne sont pas dans l'archive reçue. Je ne peux donc pas comparer à du réel, d'autant que SIEVE est produit à partir de ces mêmes gabarits : le CDS n'est pas un jeu indépendant.", "15": "Cette diapositive prouve la fuite, sur les logs de SIEVE : les six fichiers de 100 000 logs, pas sur le CDS. Je précise ce que veulent dire les deux découpages. Séparer les logs de SIEVE entre entraînement et test au hasard : on mélange tout, donc le même gabarit se retrouve des deux côtés. Séparer par gabarit : tous les logs d'un même gabarit vont du même côté.\n\nComment lire : pour chaque log de test, je cherche le log d'entraînement qui lui ressemble le plus, et je note la ressemblance de 0 à 1. À gauche, la ressemblance typique, la médiane : élevée avec le découpage au hasard, basse avec le découpage par gabarit. À droite, la part des logs de test qui ont un quasi-jumeau : près d'un quart des logs propres au hasard, presque aucun par gabarit.\n\nSur les logs très abîmés, l'écart se réduit parce que le texte est tellement modifié que même un log du même gabarit ressemble moins à sa copie. Et les fichiers du professeur confirment ce constat : un modèle qui a vu tous les gabarits y obtient 0,97, un modèle dont le gabarit vient du test 0,44.", "16": "Les bibliothèques, sans surprise. Rien d'exotique : un socle scientifique standard de Python.\n\nDeux remarques que le tableau ne dit pas. D'abord, PyTorch et Transformers ne servent que pour le réseau DistilBERT, qui est une version allégée du modèle BERT. Tous les autres modèles tiennent dans scikit-learn. Ensuite, les versions sont figées dans un fichier du dépôt, ce qui permet à quelqu'un de rejouer le notebook et de retrouver les mêmes résultats.\n\nUn détail technique que je mentionne par honnêteté : sur le Mac, j'ai dû utiliser l'attention classique du réseau et non l'attention rapide, parce que la rapide ne gère pas la méthode d'incertitude que je compare, le Monte-Carlo dropout.", "17": "Voici où chaque calcul a tourné, et combien de temps il a pris. Sur le Mac, avec la puce M3 Pro et sa carte graphique intégrée : 17 à 19 minutes pour entraîner un réseau, 8 à 9 minutes de prédiction par jeu, soit environ 38 minutes par rotation. Sur Google Colab, avec une carte T4 : 10 à 15 minutes d'entraînement, et environ 30 à 35 minutes par rotation avec les prédictions.\n\nColab a fait les 11 entraînements de validation, puis les rotations 1 et 2 du test. Mais la limite d'utilisation de la carte a été atteinte une fois, et j'ai terminé sur le Mac, rotations 3 à 5. Pour la comparaison finale, 15 réseaux, trois graines par rotation, ont été recalculés sur le Mac.\n\nLes modèles simples tournent sur le processeur, de 15 secondes à environ deux minutes et demie. Une leçon du projet : un redémarrage du Mac a interrompu un calcul, d'où le principe de tout sauvegarder par unité. Avec ces sauvegardes, rejouer le notebook prend environ 13 minutes.", "18": "Voici le déroulé en onze étapes, qui suit la consigne du projet. Je veux vous faire retenir trois étapes.\n\nL'étape 3, en orange : le découpage. C'est elle qui change les conclusions, car c'est là que je sépare par gabarit au lieu de mélanger. Elle fait passer le score de 0,97 à 0,46. Je compare quatre protocoles de découpage, et le test est scellé : je ne l'ouvre qu'une fois, avec une trace datée.\n\nL'étape 4 : dix variantes de nettoyage du texte, car je ne veux pas supposer qu'un nettoyage est le bon.\n\nL'étape 10 : un registre de 99 affirmations. Chaque chiffre du notebook est relié à sa source ou à son calcul, ce qui me permet de vérifier que rien n'est avancé sans preuve.", "19": "Premier résultat, le plus important, sur un seul modèle, un SVM linéaire sur TF-IDF mots, entraîné et testé sur les logs de SIEVE. Je rappelle ce que mesure le macro-F1 : pour chaque classe, on combine deux questions, les logs étiquetés ainsi sont-ils justes, et a-t-on retrouvé tous les vrais ; puis on moyenne sur les 30 classes.\n\nCe que dit le graphique, sans entrer dans les chiffres : avec un découpage au hasard, le score est presque parfait. Dès qu'on sépare par gabarit, il s'effondre de moitié. Les trois façons de séparer par gabarit donnent des scores voisins : la chute n'est donc pas un accident d'un découpage particulier. Et le test scellé, ouvert une seule fois à la fin, tombe dans la même zone : mes choix n'ont pas été réglés sur lui.\n\nCe qu'on en tire de bien : une mesure solide. De moins bien : les scores publiés mesuraient surtout la reconnaissance de gabarits déjà vus, pas la compréhension. Cette métrique, le macro-F1, revient à la diapositive suivante.", "20": "Cette diapositive met côte à côte les deux questions du projet, pour les mêmes deux modèles, sur les mêmes logs de SIEVE et le même test par gabarit. À gauche, le monde connu : parmi les classes qu'il connaît, le modèle se trompe à peu près une fois sur deux. Au centre et à droite, le monde inconnu : sait-il repérer une classe qu'il n'a jamais vue ?\n\nUne précaution : le macro-F1 et l'AUROC n'ont pas la même échelle. On ne les compare pas entre eux, on compare les deux modèles sur chacun. Et là, le résultat est le même des deux côtés : le Transformer fait un peu moins bien ou pareil. Le type de modèle n'est donc pas le facteur décisif.\n\nCe qu'on en tire de moins bien : repérer l'inconnu reste proche du hasard. La cible fixée avant les résultats, un AUROC d'au moins 0,80, est loin. De bien : on le sait avec une mesure honnête, ce qui était l'objectif.", "21": "Ici, une seule métrique, l'AUROC, pour tous les scores d'inconnu. Ce qu'il faut regarder, c'est la forme du graphique plus que les chiffres. Pour TF-IDF, les six scores sont presque alignés : les différences sont plus petites que le bruit d'une rotation à l'autre, donc aucun n'est vraiment meilleur. Pour le Transformer, il y a un seul gain net : quand on passe de sa confiance à une distance dans ses vecteurs, le score monte nettement et dans les cinq rotations.\n\nPourquoi ? Un Transformer affiné resserre les classes dans son espace interne : un log inconnu s'y trouve plus loin de tous les nuages, même quand sa confiance reste trompeusement haute. C'est ce que dit la littérature, et je le retrouve.\n\nMais même ce meilleur score ne dépasse pas le simple comptage de mots, et aucun n'approche la cible. Un détail instructif : en validation, TF-IDF faisait beaucoup mieux ; au test, sur de nouveaux gabarits, il retombe. Les conclusions par classe sont instables.", "22": "Les trois attaques, chacune à trois degrés, avec les deux mêmes métriques : à gauche, la perte de bonnes réponses dans le monde connu, à droite, le score de détection de l'inconnu.\n\nÀ gauche, la relation entre le degré et la perte. Pour les fautes de frappe et les mots ajoutés, la perte reste faible tant que l'attaque est modérée et ne grimpe qu'à forte dose. Pour les lettres trompeuses, elle croît vite et de plus en plus : c'est l'attaque la plus efficace, parce qu'un mot dont une lettre est d'un autre alphabet devient pour la machine un mot inconnu, alors qu'un humain ne voit rien.\n\nÀ droite, un fait à ne pas manquer : le score de détection de l'inconnu bouge à peine, mais le seuil, lui, se dérègle : le nombre de logs légitimes rejetés à tort monte nettement avec les lettres trompeuses fortes. En pratique, l'analyste reçoit plus de fausses alertes.\n\nCes courbes sont celles du modèle TF-IDF mots. Le modèle par lettres résiste mieux aux lettres trompeuses, moins bien aux mots ajoutés : il n'y a pas de modèle qui résiste à tout.", "23": "Pour la défense, les trois degrés d'attaque, avec l'attaque par la table officielle. Lecture de gauche à droite : sans défense, la perte monte avec le degré. Une table maison ne change presque rien, parce qu'elle ne connaît qu'une partie des caractères. La moitié de la table officielle réduit la perte de moitié environ. La table officielle complète la fait presque disparaître.\n\nLa relation à retenir : plus la défense connaît de caractères confondables, plus elle protège. Ce n'est pas un hasard, c'est la définition d'une table de correspondance.\n\nLe test circulaire, non montré : si je teste la défense avec la table même de l'attaque, elle paraît parfaite. C'est l'erreur que j'avais faite à l'origine et que j'ai corrigée.\n\nÀ droite, les parades : normaliser et entraîner avec des textes abîmés aident chacune, et les deux ensemble sont les plus efficaces. Le pire cas reste nettement plus mauvais que la moyenne : certaines attaques passent mieux que d'autres. Limite : ces attaques restent surtout non adaptatives.", "24": "Je termine la partie conception par ce qui borne mes conclusions, en ordre d'importance.\n\nLa première limite pèse le plus : les données sont synthétiques. Sans logs réels, je ne sais pas si mes conclusions se transfèrent. La deuxième : mon regroupement en familles n'a pas été validé par un expert.\n\nTroisième : un petit nombre de gabarits distincts, 36 en validation et 45 au test. Un écart inférieur à 0,05 est donc impossible à distinguer du bruit. Quatrième : seulement trois essais pour le Transformer, un seul pour la plupart des autres modèles.\n\nCinquième : le test scellé a déjà été ouvert une fois, donc les scores ajoutés ensuite sont comparés sur la validation seulement. Sixième : je n'ai pas de logs réels, et mes attaques ne s'adaptent pas au modèle, donc je ne dis rien d'un attaquant qui connaît le système.", "25": "Maintenant, les limites par rapport à ce que je m'étais fixé. Objectif général : mesurer sans tricher jusqu'où on sait classer et repérer l'inconnu. Atteint en partie : l'évaluation est sans fuite, mais sur des données synthétiques, donc je ne sais pas ce que cela vaut sur du réel.\n\nObjectif 1, mesurer l'effet de la triche : atteint, de 0,97 à 0,46, avec la réserve des gabarits reconstruits, 311 sur 440. Objectif 2, comparer les représentations : atteint, le Transformer n'est pas meilleur, mais avec trois graines et sans balayage de réglages. Objectif 3, comparer huit scores d'inconnu : atteint, aucun n'atteint 0,80, mais avec 36 gabarits en validation et 45 au test, un écart inférieur à 0,05 est indétectable.\n\nObjectif 4, attaques et défenses : atteint, mais pour des attaques surtout non adaptatives et sans les attaques par synonymes. Objectif 5, un notebook reproductible : atteint, mais les données SIEVE ne sont pas redistribuables et le test a déjà été ouvert une fois.", "26": "Pour conclure, objectif par objectif. Général : en partie. Sans fuite, on obtient 0,46 en monde connu et 0,60 pour repérer l'inconnu : le problème reste ouvert. Un : la triche. De 0,97 à 0,46, c'est le découpage, pas le modèle, qui fait l'écart. Deux : les représentations. Le Transformer fait 0,46 contre 0,49 pour TF-IDF ; seul gain net, la distance de Mahalanobis sur ses vecteurs, plus 0,057. Trois : les scores d'inconnu. Le meilleur AUROC est de 0,625 pour une cible à 0,80. Quatre : attaques et défenses. Les lettres trompeuses font perdre jusqu'à 21,5 % ; la table officielle ramène la perte à 0,2 %. Cinq : le notebook est reproductible, avec 99 affirmations vérifiées, un test scellé et un dépôt public.\n\nCe que je ne conclus pas : que le Transformer est inutile, ou que la hiérarchie n'aide pas. Je dis seulement que ce n'est pas démontré dans ces données.", "27": "Chaque limite appelle une perspective. La première est de passer au réel : tester sur de vrais logs, d'abord les 440 logs réels du CDS, puis des logs d'entreprise. Deuxième : faire valider les huit familles par un expert SIEM. Troisième : plus de gabarits distincts et plus de graines, pour mesurer le bruit d'entraînement. Quatrième : pour la détection de l'inconnu, tester une covariance par classe pour Mahalanobis, et mesurer si la famille proposée pour un inconnu rejeté est la bonne. Cinquième : des attaques qui s'adaptent à la défense, et une reconnaissance de mots avant le classifieur, comme le proposent Pruthi et ses collègues.\n\nLa phrase à retenir : avant de croire un score, regarder comment on a séparé l'entraînement du test.", "28": "Merci de votre attention. Si je ne devais garder qu'une phrase : avant de croire un score, regardez comment on a séparé l'entraînement du test.\n\nTout ce que j'ai montré est rejouable : le dépôt public contient le notebook, les résultats chiffrés, les figures et le code. Seules les données SIEVE n'y sont pas, parce qu'elles sont fournies sur demande par leurs auteurs. Le code QR mène au dépôt. La diapositive suivante liste toutes les sources citées.", "29": "Ces deux diapositives listent toutes les sources citées, avec un lien cliquable pour chacune quand il existe : page arXiv, DOI ou site. Deux précisions d'honnêteté. Le chiffre d'IBM vient d'un article de synthèse qui cite le rapport 2026, pas du rapport lui-même. Et la référence « recherche bibliographique » est celle du notebook : 73 références dont j'ai ouvert chaque page, avec leur niveau de vérification.", "30": "Suite des références. Elles sont numérotées dans l'ordre où elles apparaissent dans la présentation."};
let n = 0;
function slide(title, message, notes) {                // title = intitulé du point demandé ; message = phrase qui énonce le message de la diapositive
  const s = pres.addSlide({ masterName: "CONTENU" }); n += 1;
  s.addText(title, { placeholder: "title" });
  T(s, message, { x: X0, y: 1.02, w: CW, h: 0.75, fontSize: 18, color: INK });
  if (NOTES[n]) s.addNotes(NOTES[n]); return s;
}
const dark = (s, x, y, w, h) => s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
const chartBase = (title) => ({ showTitle: true, title, titleFontSize: 13, titleColor: BLUE, titleFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt", dataLabelFontFace: "+mn-lt", legendFontFace: "+mn-lt",
  catAxisLabelFontSize: 10, valAxisLabelFontSize: 10, dataLabelFontSize: 10, catAxisLabelColor: INK, valAxisLabelColor: MUTED, dataLabelColor: INK, valGridLine: { color: "E3E8EF", size: 0.5 }, catGridLine: { style: "none" }, showValue: true, barGapWidthPct: 45 });
const lab = (s, text, x, y, w) => T(s, text, { x, y, w, h: 0.3, fontSize: 13, bold: true, color: BLUE });   // petit intitulé de bloc, en casse de phrase

const enclair = (s, text, y = 1.42) => T(s, [{ text: "En clair : ", options: { bold: true, color: BLUE } }, { text, options: { color: MUTED } }], { x: X0, y, w: CW, h: 0.45, fontSize: 14 });

const panelRight = (s, lire, bien, mal) => {
  lab(s, "Comment lire", 8.7, 2.05, 4); T(s, lire, { x: 8.7, y: 2.45, w: 3.95, h: 1.9, fontSize: 13.5 });
  dark(s, 8.7, 4.4, 3.95, 2.45); T(s, "Ce qu'on en tire", { x: 8.95, y: 4.5, w: 3.5, h: 0.3, fontSize: 13, bold: true, color: ICE });
  P(s, [[{ b: "Bien : " }, bien], [{ b: "Moins bien : " }, mal]], { x: 8.95, y: 4.85, w: 3.5, h: 1.95, fontSize: 13.5, gap: 8, run: { color: "FFFFFF" } });
};

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
  s.addNotes(NOTES[1]);
}

// 2. Contexte
{
  const s = slide("Introduction - Contexte", "Les violations coûtent cher, et deux tiers des alertes sont ignorées",
    "Transition : avant le sujet technique, l'enjeu. À dire : les trois sources sont des rapports de l'industrie de la sécurité ; le chiffre d'IBM vient d'un article qui cite le rapport 2026. Ce que cela implique pour nous : le tri des événements est un travail humain coûteux. Question probable : ces chiffres prouvent-ils que le tri automatique aide ? Non, ils montrent l'ampleur du problème ; notre contribution est de mesurer honnêtement ce qu'un classifieur sait faire.");
  enclair(s, "chaque alerte de sécurité doit être triée par un humain, et il n'y a pas assez de monde pour toutes les traiter.");
  T(s, "4,99 M$", { x: X0, y: 1.95, w: 5.8, h: 1.3, fontSize: 70, color: CORAL, fontFace: HEAD });
  P(s, [["coût moyen d'une violation de données, en hausse de 12 % en un an ", C("ibm")]], { x: X0, y: 3.25, w: 5.5, h: 0.8, fontSize: 19 });
  P(s, [["247 jours en moyenne pour identifier et contenir une violation ", C("ibm")]], { x: X0, y: 4.1, w: 5.5, h: 0.9, fontSize: 15, run: { color: MUTED } });
  hline(s, 6.9, 2.0, 5.75);
  T(s, "4 484", { x: 6.9, y: 2.12, w: 2.3, h: 0.8, fontSize: 36, color: BLUE, fontFace: HEAD });
  P(s, [["alertes par jour pour une équipe de surveillance (SOC) ; 67 % sont ignorées ", C("vectra")]], { x: 9.3, y: 2.2, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 3.2, 5.75);
  T(s, "10 626", { x: 6.9, y: 3.32, w: 2.3, h: 0.8, fontSize: 36, color: BLUE, fontFace: HEAD });
  P(s, [["violations confirmées sur 30 458 incidents analysés (année 2023) ", C("verizon")]], { x: 9.3, y: 3.4, w: 3.35, h: 0.8, fontSize: 15, valign: "middle" });
  hline(s, 6.9, 4.4, 5.75);
  dark(s, X0, 5.35, CW, 1.5);
  T(s, "Pourquoi c'est notre sujet", { x: X0 + 0.35, y: 5.5, w: 5, h: 0.3, fontSize: 13, bold: true, color: ICE });
  T(s, "Un SIEM rassemble les logs de toute l'entreprise. Le goulot est humain : trier chaque événement et repérer celui qu'aucune règle ne décrit.", { x: X0 + 0.35, y: 5.85, w: CW - 0.7, h: 0.95, fontSize: 16, color: "FFFFFF" });
}

// 3. Problématique
{
  const s = slide("Introduction - Problématique", "Une bonne note à l'examen ne prouve rien si les questions étaient déjà dans le cours",
    "Transition : de l'enjeu à la question. À dire : les scores publiés sur SIEVE atteignent 0,97 parce que les logs viennent d'un nombre fini de gabarits et qu'un découpage aléatoire laisse le même gabarit des deux côtés. Question probable : pourquoi pas simplement un meilleur modèle ? Parce que le problème n'est pas le modèle mais ce que l'évaluation mesure.");
  enclair(s, "un gabarit est une phrase à trous : tous les logs sont fabriqués en remplissant les mêmes phrases avec des valeurs différentes.");
  dark(s, X0, 2.05, 6.7, 2.15);
  T(s, "Question centrale", { x: X0 + 0.3, y: 2.17, w: 5, h: 0.3, fontSize: 13, bold: true, color: ICE });
  T(s, "Comment classer un événement de sécurité, tout en reconnaissant qu'il n'appartient à aucune classe connue, avec une évaluation qui ne triche pas ?", { x: X0 + 0.3, y: 2.55, w: 6.1, h: 1.6, fontSize: 19, fontFace: HEAD, color: "FFFFFF" });
  const q = [["1", "Que valent les scores publiés ?", "Sur SIEVE, les mêmes phrases à trous reviennent au test."], ["2", "Sait-on repérer une classe jamais vue ?", "Dans un SIEM, l'inconnu est la règle."], ["3", "Le système résiste-t-il aux textes modifiés ?", "Fautes, lettres trompeuses, mots ajoutés."]];
  q.forEach((r, i) => { const y = 4.5 + i * 0.82; T(s, r[0], { x: X0, y, w: 0.5, h: 0.5, fontSize: 26, color: CORAL, fontFace: HEAD }); T(s, r[1], { x: X0 + 0.6, y, w: 6.1, h: 0.32, fontSize: 15, bold: true, color: BLUE }); T(s, r[2], { x: X0 + 0.6, y: y + 0.33, w: 6.1, h: 0.4, fontSize: 12.5, color: MUTED }); });
  P(s, [[{ b: "Ce qui existe" }], ["Des scores de 0,93 à 0,97 avec un découpage au hasard ", C("sieve")], [{ b: "Ce qui manque" }], ["Ce que valent ces scores sur de nouveaux gabarits, et si l'on repère l'inconnu."]], { x: 7.9, y: 2.05, w: 4.75, h: 4.5, fontSize: 17, gap: 12 });
}

// 4. Objectifs
{
  const s = slide("Introduction - Objectifs", "Le projet mesure honnêtement ; il ne construit pas un produit",
    "Transition : de la question aux objectifs. À dire : volontairement pas de fonctionnalité promise ; l'utilité est un banc d'essai. Question probable : quel est le livrable ? Un notebook exécutable, des résultats chiffrés et un protocole qu'on peut réutiliser pour comparer d'autres classifieurs de logs.");
  lab(s, "Objectif général", X0, 2.0, 4.5);
  T(s, "Mesurer jusqu'où un programme classe des journaux de sécurité, reconnaît l'inconnu et résiste à des textes modifiés, sans tricher sur l'évaluation.", { x: X0, y: 2.4, w: 4.6, h: 3.2, fontSize: 21, fontFace: HEAD });
  lab(s, "Objectifs spécifiques", 6.2, 2.0, 5);
  [["Mesurer", " de combien la triche gonfle les scores"], ["Comparer", " trois façons de transformer le texte en nombres"], ["Comparer", " huit façons de repérer l'inconnu"], ["Tester", " les attaques sur le texte et les défenses"], ["Livrer", " un notebook reproductible"]].forEach((t, i) => {
    const y = 2.45 + i * 0.68; hline(s, 6.2, y - 0.08, 6.45); P(s, [[{ b: t[0] }, t[1]]], { x: 6.2, y, w: 6.45, h: 0.6, fontSize: 15, valign: "middle", run: { color: INK } }); });
  lab(s, "Sur quoi le projet pourrait servir", X0, 6.02, 6);
  T(s, "Un banc d'essai réutilisable pour comparer des classifieurs de logs sans surestimer leurs scores.", { x: X0, y: 6.34, w: 11.9, h: 0.55, fontSize: 14.5 });
}

// 5. État de l'art : vue d'ensemble (carte des cinq blocs)
{
  const s = slide("État de l'art - Vue d'ensemble", "Cinq blocs, du plus concret au plus technique : pour chacun, ce qui existe et ce que nous en retenons");
  enclair(s, "« monde ouvert » veut dire que le programme peut rencontrer des événements qu'il n'a jamais appris.");
  const B = [["A", "Les logs, SIEVE et le découpage", "Que valent les scores publiés ?"], ["B", "La classification hiérarchique", "Les familles aident-elles à mieux classer et à mieux se tromper ?"], ["C", "La détection d'inconnus", "Comment reconnaître un événement jamais vu ?"], ["D", "La robustesse du texte", "Que se passe-t-il si un attaquant modifie le log ?"], ["E", "La calibration", "La confiance affichée par le modèle est-elle honnête ?"]];
  B.forEach((b, i) => { const y = 2.05 + i * 0.72; hline(s, X0, y - 0.08, CW); T(s, b[0], { x: X0, y, w: 0.6, h: 0.6, fontSize: 28, color: CORAL, fontFace: HEAD, valign: "middle" }); T(s, b[1], { x: 1.5, y, w: 5.0, h: 0.6, fontSize: 18, bold: true, color: BLUE, valign: "middle" }); T(s, b[2], { x: 6.6, y, w: 6.05, h: 0.6, fontSize: 15, valign: "middle" }); });
  dark(s, X0, 5.75, CW, 1.1);
  T(s, "Lacune", { x: X0 + 0.3, y: 5.85, w: 3, h: 0.3, fontSize: 13, bold: true, color: ICE });
  P(s, [["Aucun travail trouvé ne traite ensemble la hiérarchie, les logs SIEM et le monde ouvert (73 références dont la page a été ouverte) ", C("biblio")]], { x: X0 + 0.3, y: 6.2, w: CW - 0.6, h: 0.6, fontSize: 16, run: { color: "FFFFFF" } });
}

// 6 à 10. État de l'art : un bloc par diapositive (ce qui existe, limite, ce que nous retenons)
const sota = (titre, message, clair, existe, limite, retient) => {
  const s = slide(titre, message); enclair(s, clair);
  lab(s, "Ce qui existe", X0, 2.0, 5); P(s, existe, { x: X0, y: 2.4, w: 7.3, h: 3.3, fontSize: 16, gap: 12 });
  hline(s, X0, 5.75, 7.3); lab(s, "Sa limite", X0, 5.85, 5); P(s, [limite], { x: X0, y: 6.2, w: 7.3, h: 0.7, fontSize: 15, run: { color: INK } });
  dark(s, 8.35, 2.0, 4.3, 4.85); T(s, "Ce que nous en retenons", { x: 8.65, y: 2.15, w: 3.8, h: 0.3, fontSize: 13, bold: true, color: ICE });
  P(s, retient, { x: 8.65, y: 2.6, w: 3.8, h: 4.1, fontSize: 17, gap: 16, run: { color: "FFFFFF" } });
};
sota("État de l'art - Bloc A : les logs et le découpage", "Les scores publiés sur les logs dépendent beaucoup de la façon de séparer entraînement et test",
  "un gabarit est une phrase à trous ; si le même gabarit est au test et à l'entraînement, le score est gonflé.",
  [[{ b: "Jeux de logs : " }, "Loghub, 19 jeux sans taxonomie de sécurité ", C("loghub"), " ; SIEVE, logs SIEM générés, 30 classes ", C("sieve")], [{ b: "Anomalies : " }, "DeepLog ", C("deeplog"), ", LogBERT ", C("logbert"), " détectent des séquences anormales, sans classer les types d'événements"], [{ b: "Classer des logs de sécurité : " }, "modèles de langue affinés, F1 de 0,998 annoncé ", C("karlsen"), " ; découpage non décrit dans le résumé"], [{ b: "Découper : " }, "aléatoire, par groupes, imbriquée ", C("sklcv"), ", biais de sélection ", C("cawley")]],
  ["SIEVE : 0,93 à 0,97 de macro-F1, mais avec un découpage au hasard des logs ", C("sieve")],
  [[{ b: "Découpage par gabarit" }, " des logs de SIEVE, reconstruit"], [{ b: "Validation croisée par groupes" }, " et imbriquée"], [{ b: "Test scellé" }, ", ouvert une seule fois"]]);
sota("État de l'art - Bloc B : la classification hiérarchique", "En texte, la hiérarchie est traitée en monde fermé ; avec des inconnus, elle reste un problème ouvert",
  "une hiérarchie range les classes en familles : se tromper de classe dans la bonne famille est moins grave.",
  [[{ b: "Approches locales ou globales : " }, "un classifieur par nœud, ou un seul modèle qui connaît l'arbre ", C("silla")], [{ b: "En texte : " }, "HiAGM ", C("hiagm"), ", HiTIN ", C("hitin"), " modélisent la hiérarchie, en monde fermé"], [{ b: "Erreurs légères : " }, "modifier la perte d'entraînement ", C("bertinetto")], [{ b: "Monde ouvert : " }, "répondre à un niveau plus grossier quand l'entrée est ambiguë ", C("lind"), ", surtout en vision"]],
  ["Pour le texte avec étiquettes inconnues, la hiérarchie est dite « encore ouverte » ", C("kwon")],
  [[{ b: "Approche locale" }, " : une tête famille, une tête classe"], [{ b: "p(classe) = p(famille) × p(classe | famille)" }], [{ b: "Repli sur la famille" }, " quand la classe est incertaine"]]);
sota("État de l'art - Bloc C : la détection d'inconnus", "Quatre familles de méthodes existent ; en texte, les méthodes classiques ratent beaucoup de décalages",
  "un classifieur ordinaire n'a pas de case « inconnu » : il range tout log dans une classe connue.",
  [[{ b: "Score de sortie : " }, "probabilité maximale ", C("msp"), ", énergie ", C("energy"), ", ODIN ", C("odin"), ", OpenMax ", C("openmax")], [{ b: "Distance : " }, "Mahalanobis ", C("maha"), ", kNN profond ", C("knn"), ", ViM ", C("vim"), " ; très efficace sur un Transformer affiné ", C("podolskiy")], [{ b: "Incertitude : " }, "ensembles ", C("ens"), ", dropout Monte-Carlo ", C("mcd")], [{ b: "Entraînement spécial : " }, "Outlier Exposure ", C("oe")]],
  ["Un bon classifieur fermé suffit presque ", C("vaze"), " ; les méthodes classiques ratent beaucoup de décalages en texte ", C("baran")],
  [[{ b: "Huit scores comparés" }, " sur sorties et vecteurs, classes masquées pour de faux"], [{ b: "Seuil réglé" }, " sur les classes connues seulement"], [{ b: "Écartés : " }, "ODIN (perturbe l'entrée) et Outlier Exposure (exige des inconnus)"]]);
sota("État de l'art - Bloc D : la robustesse du texte", "Les attaques sur le texte viennent du spam ; la défense recommandée est d'assainir l'entrée",
  "dans un SIEM, l'attaquant contrôle une partie du log (nom d'utilisateur, adresse, fichier) et peut le déguiser.",
  [[{ b: "Attaques anciennes : " }, "mots ajoutés contre les filtres anti-spam ", C("dalvi"), ", ", C("lowd")], [{ b: "Caractères invisibles : " }, "un seul changement peut dégrader un modèle ", C("boucher")], [{ b: "Défenses : " }, "assainir l'entrée (norme Unicode ", C("uts39"), "), reconnaissance de mots ", C("pruthi"), ", encodages robustes ", C("jones")], [{ b: "Hors périmètre : " }, "attaques par synonymes ", C("textfooler"), " ou par gradient ", C("hotflip")]],
  ["Une défense réussit surtout contre l'attaque qu'elle a déjà vue."],
  [[{ b: "Trois attaques" }, " : fautes, lettres trompeuses, mots ajoutés, chacune à trois degrés"], [{ b: "Normalisation" }, " avec la table officielle, renforcée par l'entraînement adversarial"], [{ b: "Défense testée" }, " contre une autre table que celle de l'attaque"]]);
sota("État de l'art - Bloc E : la calibration", "Un modèle est calibré si sa confiance dit vrai ; sous décalage de données, elle se dégrade",
  "si un modèle se dit sûr à 90 % mais n'a raison que 6 fois sur 10, sa confiance est trompeuse.",
  [[{ b: "Mesurer : " }, "diagramme de fiabilité et ECE, l'écart moyen entre confiance et réalité ", C("guo")], [{ b: "Corriger : " }, "mise à l'échelle par température, un seul nombre à régler ", C("guo")], [{ b: "Transformers : " }, "mieux calibrés en domaine, moins mal hors domaine ", C("desai")], [{ b: "Sous décalage : " }, "la calibration se dégrade, les ensembles tiennent mieux ", C("ovadia")]],
  ["La température change les probabilités, pas leur ordre : elle ne règle pas la détection d'inconnus."],
  [[{ b: "ECE avant et après température" }], [{ b: "Constat chez nous : " }, "l'encodeur annonce 85 % de confiance au test pour 50 % de bonnes réponses"], [{ b: "Pas de promesse" }, " sur l'inconnu : on mesure l'honnêteté, pas le classement"]]);

// 11. Matériel
{
  const s = slide("Matériel", "Un seul jeu de logs, SIEVE, plus les fichiers du professeur et un réseau pré-entraîné");
  lab(s, "SIEVE : six versions de 100 000 logs, de plus en plus abîmées", X0, 1.95, 7);
  ["0", "0,1", "0,2", "0,3", "0,4", "0,5"].forEach((p, i) => { const x = X0 + i * 0.98; s.addShape(pres.ShapeType.rect, { x, y: 2.4, w: 0.88, h: 0.7, fill: { color: i === 0 ? BLUE : "FFFFFF" }, line: { color: BLUE, width: 1 } }); T(s, "p = " + p, { x, y: 2.4, w: 0.88, h: 0.7, fontSize: 13, bold: true, color: i === 0 ? "FFFFFF" : BLUE, align: "center", valign: "middle" }); });
  P(s, [["Générés à partir de 440 gabarits réels, en 30 classes équilibrées ", C("sieve")], ["p mesure à quel point le texte est abîmé."]], { x: X0, y: 3.35, w: 5.9, h: 1.7, fontSize: 16, gap: 12 });
  const R = [["6 × 100 000", [["logs SIEVE, générés à partir des 440 gabarits ", C("sieve")]]], ["6 × 35 000", [["logs du professeur, mêmes gabarits"]]], ["1 447", [["lettres confondables (table Unicode ", C("uts39"), ")"]]], ["DistilBERT", [["réseau déjà entraîné sur du texte ", C("distil")]]], ["8 familles", [["regroupement des classes : notre hypothèse"]]], ["0 log réel", [["les 440 logs réels du CDS ne sont pas fournis"]]]];
  R.forEach((r, i) => { const y = 1.95 + i * 0.8; hline(s, 7.0, y - 0.06, 5.65); T(s, r[0], { x: 7.0, y, w: 2.3, h: 0.68, fontSize: 21, color: CORAL, fontFace: HEAD, valign: "middle" }); P(s, r[1], { x: 9.35, y, w: 3.3, h: 0.68, fontSize: 13.5, valign: "middle" }); });
}

// 12. Méthodes : cycle graphique (étapes du notebook) ; le test scellé est hors de la boucle
{
  const s = slide("Méthodes", "Cinq opérations en boucle, réglées sur la validation ; le test scellé reste hors de la boucle");
  const NODES = [
    ["1  Vectorisation", "Transformer le texte en nombres", [["TF-IDF, vecteurs de mots, DistilBERT ", C("distil")]]],
    ["2  Classification", "Choisir la famille puis la classe", [["Un niveau ou deux niveaux ", C("lind")]]],
    ["3  Détection d'inconnus", "Noter l'étrangeté d'un log", [["Confiance (MSP ", C("msp"), ") ou distance (Mahalanobis ", C("maha"), ")"]]],
    ["4  Évaluation", "Mesurer sur la validation", [["Découpage par gabarit, 5 rotations"]]],
    ["5  Robustesse, calibration", "Attaquer, défendre, corriger", [["Table Unicode ", C("uts39"), ", température ", C("guo")]]]];
  const cx = 5.3, cy = 4.5, rx = 3.3, ry = 2.0, w = 2.7, h = 1.35;
  const pts = NODES.map((_, i) => { const a = (-90 + i * 72) * Math.PI / 180; return [cx + rx * Math.cos(a), cy + ry * Math.sin(a)]; });
  const edge = (c, d) => { const t = Math.min((w / 2) / Math.max(Math.abs(d[0]), 1e-6), (h / 2) / Math.max(Math.abs(d[1]), 1e-6)); return [c[0] + d[0] * t, c[1] + d[1] * t]; };
  NODES.forEach((_, i) => { const a = pts[i], b = pts[(i + 1) % 5]; const d = [b[0] - a[0], b[1] - a[1]]; const L = Math.hypot(d[0], d[1]); const u = [d[0] / L, d[1] / L];
    const p1 = edge(a, u), p2 = edge(b, [-u[0], -u[1]]); const pad = 0.12; const x1 = p1[0] + u[0] * pad, y1 = p1[1] + u[1] * pad, x2 = p2[0] - u[0] * pad, y2 = p2[1] - u[1] * pad;
    s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1), h: Math.abs(y2 - y1), flipH: x2 < x1, flipV: y2 < y1, line: { color: CORAL, width: 2, endArrowType: "triangle" } }); });
  NODES.forEach((nd, i) => { const [px, py] = pts[i], x = px - w / 2, y = py - h / 2;
    s.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } });
    T(s, nd[0], { x: x + 0.15, y: y + 0.08, w: w - 0.3, h: 0.35, fontSize: 14, bold: true, color: BLUE });
    T(s, nd[1], { x: x + 0.15, y: y + 0.45, w: w - 0.3, h: 0.35, fontSize: 12.5, color: INK });
    P(s, nd[2], { x: x + 0.15, y: y + 0.82, w: w - 0.3, h: 0.5, fontSize: 11, run: { color: MUTED } }); });
  T(s, "Boucle : on règle sur la validation, on corrige, on recommence", { x: cx - 1.4, y: cy - 0.45, w: 2.8, h: 0.9, fontSize: 14, bold: true, color: BLUE, align: "center", valign: "middle" });
  s.addShape(pres.ShapeType.line, { x: 10.1, y: 2.0, w: 0, h: 4.8, line: { color: STEEL, width: 1.25, dashType: "dash" } });
  dark(s, 10.3, 2.4, 2.65, 3.7);
  T(s, "Hors de la boucle", { x: 10.5, y: 2.55, w: 2.3, h: 0.3, fontSize: 12.5, bold: true, color: ICE });
  T(s, "Test scellé", { x: 10.5, y: 2.95, w: 2.3, h: 0.6, fontSize: 24, color: "FFFFFF", fontFace: HEAD });
  T(s, "Ouvert une seule fois, à la fin, quand tous les choix sont figés", { x: 10.5, y: 3.7, w: 2.3, h: 1.3, fontSize: 14.5, color: "FFFFFF" });
  T(s, "Trace datée dans le notebook", { x: 10.5, y: 5.3, w: 2.3, h: 0.6, fontSize: 12, color: ICE });
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

// 14. Présentation des données (2/3) : un seul jeu, des 440 gabarits aux six fichiers
{
  const s = slide("Présentation des données (2/3)", "Un seul jeu de données : SIEVE est généré à partir de 440 gabarits réels, et nos modèles n'utilisent que ses logs");
  const F = [["Logs réels publics", "Loghub, OSSEC, Public Security Log Sharing Site"], ["440 gabarits réels (CDS)", "30 classes, validés par 3 experts SIEM"], ["SIEVE : 6 fichiers", "100 000 logs chacun, p = 0 à 0,5"], ["Nos modèles", "entraînés et testés sur ces logs"]];
  const bw = 2.7, gap = (CW - 4 * bw) / 3;
  F.forEach((f, i) => { const x = X0 + i * (bw + gap); s.addShape(pres.ShapeType.rect, { x, y: 1.95, w: bw, h: 1.15, fill: { color: i === 2 ? BLUE : "FFFFFF" }, line: { color: BLUE, width: 1.25 } });
    T(s, f[0], { x: x + 0.15, y: 2.02, w: bw - 0.3, h: 0.4, fontSize: 15, bold: true, color: i === 2 ? "FFFFFF" : BLUE }); T(s, f[1], { x: x + 0.15, y: 2.45, w: bw - 0.3, h: 0.6, fontSize: 12.5, color: i === 2 ? ICE : INK });
    if (i < 3) s.addShape(pres.ShapeType.line, { x: x + bw + 0.04, y: 2.52, w: gap - 0.08, h: 0, line: { color: CORAL, width: 2, endArrowType: "triangle" } }); });
  P(s, [["Source des 440 gabarits : article de SIEVE ", C("sieve")]], { x: X0, y: 3.18, w: CW, h: 0.3, fontSize: 12, run: { color: MUTED } });
  const rows = [["Gabarit (phrase à trous)", "[<date>] [error] [client <adresse IP>] user <nom>: authentication failure for \"<chemin>\": Password Mismatch"], ["Log : le gabarit rempli", "[Wed Nov 03 19:30:11 1976] [error] [client 217.121.56.73] user clarkesummer: authentication failure for \"/at/challenge.png/pass\": Password Mismatch"], ["Le même log abîmé, p = 0,5", ":forauthentication [failure] /authority/car.wavhsandoval 214.18.6.71] user /: client Mismatch Thu Dec 07 03:54:44 2006 \"[Password[]air \" error"]];
  rows.forEach((r, i) => { const y = 3.65 + i * 0.95; T(s, r[0], { x: X0, y, w: 1.9, h: 0.8, fontSize: 12.5, bold: true, color: BLUE, valign: "middle" }); s.addShape(pres.ShapeType.rect, { x: X0 + 2.0, y, w: 6.1, h: 0.8, fill: { color: PANEL }, line: { color: LINE, width: 0.5 } }); T(s, r[1], { x: X0 + 2.12, y, w: 5.9, h: 0.8, fontSize: 10.5, fontFace: MONO, valign: "middle" }); });
  lab(s, "Ce que nous avons ajouté", 9.05, 3.6, 3.6);
  P(s, [[{ b: "311 gabarits retrouvés" }, " sur 440, en regroupant les logs de SIEVE"], ["Ce regroupement sert seulement à ", { b: "séparer entraînement et test" }], ["Les modèles voient donc ", { b: "les mêmes logs" }, " : aucun second jeu de données"]], { x: 9.05, y: 4.0, w: 3.6, h: 2.9, fontSize: 14, gap: 10 });
}

// 9ter. Présentation des données (3/3) : fuite, sur les logs de SIEVE
{
  const s = slide("Présentation des données (3/3)", "Sur SIEVE, un découpage au hasard laisse près d'un quart des logs de test avec un quasi-jumeau");
  enclair(s, "on sépare les logs de SIEVE entre entraînement et test : au hasard (on mélange), ou par gabarit (un gabarit reste d'un seul côté).");
  const L = ["SIEVE_00\n(logs propres, p = 0)", "SIEVE_05\n(logs très abîmés, p = 0,5)"];
  s.addChart(pres.charts.BAR, [{ name: "Découpage au hasard", labels: L, values: [0.739, 0.593] }, { name: "Découpage par gabarit", labels: L, values: [0.276, 0.257] }], Object.assign(chartBase("Ressemblance au plus proche voisin"), { x: X0, y: 2.0, w: 3.9, h: 4.55, barDir: "col", chartColors: [CORAL, BLUE], valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", dataLabelFontSize: 11, catAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 10, legendColor: INK }));
  s.addChart(pres.charts.BAR, [{ name: "Découpage au hasard", labels: L, values: [24.0, 5.0] }, { name: "Découpage par gabarit", labels: L, values: [1.0, 0.2] }], Object.assign(chartBase("Quasi-jumeaux dans l'entraînement (%)"), { x: X0 + 4.0, y: 2.0, w: 3.9, h: 4.55, barDir: "col", chartColors: [CORAL, BLUE], valAxisMinVal: 0, valAxisMaxVal: 30, valAxisMajorUnit: 10, dataLabelFormatCode: "0.0", dataLabelFontSize: 11, catAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 10, legendColor: INK }));
  T(s, "Calcul du projet sur les fichiers SIEVE_00 et SIEVE_05 (étape 3). Quasi-jumeau : ressemblance d'au moins 0,90.", { x: X0, y: 6.6, w: 7.9, h: 0.3, fontSize: 11, color: MUTED });
  panelRight(s, "Chaque log de test est comparé à son plus proche voisin dans l'entraînement : 1 = identique, 0 = rien à voir. Mêmes logs SIEVE ; seule la séparation change.",
    "séparés par gabarit, les logs de test ne ressemblent presque plus à l'entraînement : le test est honnête.",
    "séparés au hasard, près d'un quart des logs propres a un quasi-jumeau : le score est gonflé.");
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

// 17. Environnement d'exécution : qui a calculé quoi, et combien de temps
{
  const s = slide("Environnement d'exécution", "Le Mac et Colab ont calculé l'encodeur ; chaque machine a ses temps, et tout reprend là où il s'est arrêté");
  enclair(s, "les réseaux Transformer demandent une carte graphique ; les modèles simples tournent sur le processeur du Mac.");
  const col = (x, titre, sous, K, qui) => {
    s.addShape(pres.ShapeType.rect, { x, y: 2.0, w: 5.85, h: 4.3, fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.25 } });
    s.addShape(pres.ShapeType.rect, { x, y: 2.0, w: 5.85, h: 0.75, fill: { color: BLUE }, line: { color: BLUE, width: 0 } });
    T(s, titre, { x: x + 0.25, y: 2.05, w: 5.4, h: 0.4, fontSize: 17, bold: true, color: "FFFFFF" }); T(s, sous, { x: x + 0.25, y: 2.42, w: 5.4, h: 0.3, fontSize: 12, color: ICE });
    K.forEach((k, i) => { const y = 2.95 + i * 0.68; T(s, k[0], { x: x + 0.25, y, w: 2.2, h: 0.6, fontSize: 22, color: CORAL, fontFace: HEAD, valign: "middle" }); T(s, k[1], { x: x + 2.5, y, w: 3.2, h: 0.6, fontSize: 13.5, valign: "middle" }); if (i > 0) hline(s, x + 0.25, y - 0.04, 5.35); });
    T(s, qui, { x: x + 0.25, y: 5.75, w: 5.4, h: 0.5, fontSize: 12.5, color: MUTED }); };
  col(X0, "Mac, puce M3 Pro", "GPU Apple (MPS)", [["17 à 19 min", "entraînement d'un réseau"], ["8 à 9 min", "prédiction par jeu (validation, test)"], ["≈ 38 min", "par rotation, prédictions comprises"], ["15 réseaux", "3 graines × 5 rotations recalculés"]], "A calculé : rotations 3 à 5 du test, puis les 15 réseaux de la comparaison finale.");
  col(6.78, "Google Colab", "GPU T4, notebook lancé à la main", [["10 à 15 min", "entraînement d'un réseau"], ["≈ 30 à 35 min", "par rotation, prédictions comprises"], ["11", "entraînements pour la validation"], ["2", "rotations du test (1 et 2)"]], "Limite d'utilisation du GPU atteinte une fois : chaque modèle est sauvegardé sur Drive.");
  T(s, "Modèles simples (processeur) : de 15 s à 159 s d'entraînement   ·   Notebook rejoué en ≈ 13 min avec les sauvegardes   ·   Publié sur GitHub, sans les données", { x: X0, y: 6.45, w: CW, h: 0.4, fontSize: 13, bold: true, color: BLUE });
}

// 12. Pipeline : ligne de métro (nœuds reliés), sans cartes
{
  const s = slide("Conception - Pipeline utilisé", "Onze étapes, dont le découpage par gabarit est celle qui change le plus les conclusions",
    "Transition : de l'environnement au déroulé. À dire : chaque étape a ses décisions justifiées dans le notebook ; la 3 est en couleur car c'est elle qui a fait passer le score de 0,97 à 0,46. Les codes H1 à H15 (hypothèses), P0 à P3 (protocoles de découpage) et E1 à E5 (expériences) sont dans le notebook. Question probable : pourquoi 11 étapes ? Elles suivent la consigne du projet (cadrage à conclusion) avec les sous-étapes que nous avons ajoutées.");
  enclair(s, "de la question de départ à la conclusion, onze étapes ; l'étape en orange est celle qui change tout.");
  const P_ = [["Cadrage", "Question, hypothèses, critères"], ["Données", "Récupération, vérification"], ["Exploration", "Classes, gabarits, effet de p"], ["Découpage", "Par gabarit, test scellé"], ["Prétraitement", "Nettoyage du texte"], ["Représentations", "Mots, vecteurs, Transformer"],
    ["Modèles", "Un ou deux niveaux, huit scores"], ["Évaluation", "Test scellé, ouvert une fois"], ["Robustesse", "Attaques sur le texte"], ["Amélioration", "Défenses, calibration"], ["Conclusion", "99 affirmations, limites"]];
  const rows = [[0, 6, 2.2], [6, 11, 4.3]];
  rows.forEach(([a, b, y]) => { const cnt = b - a, step = 2.05, x0 = X0 + 0.6 + (cnt < 6 ? step / 2 : 0); s.addShape(pres.ShapeType.line, { x: x0, y: y + 0.28, w: step * (cnt - 1), h: 0, line: { color: STEEL, width: 2 } });
    for (let i = a; i < b; i++) { const cx = x0 + (i - a) * step, hot = i === 3;
      s.addShape(pres.ShapeType.ellipse, { x: cx - 0.28, y, w: 0.56, h: 0.56, fill: { color: hot ? CORAL : BLUE }, line: { color: "FFFFFF", width: 2 } }); T(s, String(i), { x: cx - 0.28, y, w: 0.56, h: 0.56, fontSize: 15, bold: true, color: "FFFFFF", align: "center", valign: "middle" });
      T(s, P_[i][0], { x: cx - 0.95, y: y + 0.7, w: 1.9, h: 0.35, fontSize: 15, bold: true, color: hot ? CORAL : BLUE, align: "center" }); T(s, P_[i][1], { x: cx - 0.95, y: y + 1.08, w: 1.9, h: 1.2, fontSize: 13.5, align: "center" }); } });
  T(s, "Étape 3, sur les logs de SIEVE : de 0,97 (découpage au hasard) à 0,46 (découpage par gabarit)", { x: X0, y: 6.5, w: CW, h: 0.4, fontSize: 16, bold: true, color: CORAL, align: "center" });
}

// 19 à 23. Résultats : cinq diapositives, mêmes modèles et mêmes métriques d'une diapositive à l'autre
const resultat = (k, message, clair, addChart, lire, bien, mal) => {
  const s = slide("Conception - Présentation et analyse des résultats (" + k + "/5)", message);
  enclair(s, clair); addChart(s); panelRight(s, lire, bien, mal);
};
const CH = { x: X0, y: 2.0, w: 7.9, h: 4.8 };
const CHL = { x: X0, y: 2.0, w: 3.9, h: 4.8 }, CHR = { x: X0 + 4.0, y: 2.0, w: 3.9, h: 4.8 };
const barCol = Object.assign({}, { barDir: "col", dataLabelFontSize: 12, catAxisLabelFontSize: 11 });
resultat(1, "Sur les logs de SIEVE : 0,99 avec un découpage au hasard, 0,42 à 0,51 par gabarit, 0,48 au test scellé", "même modèle (SVM sur TF-IDF mots), mêmes logs SIEVE : seule change la façon de séparer entraînement et test.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "macro-F1", labels: ["Découpage\nau hasard", "Par gabarit", "Par groupes\nde gabarits", "Validation\nimbriquée", "Test scellé"], values: [0.987, 0.422, 0.507, 0.511, 0.483] }], Object.assign(chartBase("Macro-F1 : part de bonnes réponses"), CH, barCol, { chartColors: [STEEL, BLUE, BLUE, BLUE, CORAL], valAxisMaxVal: 1, valAxisMinVal: 0, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", dataLabelFontSize: 13, catAxisLabelFontSize: 12, showLegend: false })),
  "1 = tout est juste. Le macro-F1 est la moyenne des notes des 30 classes.", "les trois découpages par gabarit donnent des scores voisins, et le test scellé tombe dans la même zone : la chute est solide.", "le score élevé du découpage au hasard ne mesurait pas la compréhension, seulement la reconnaissance de gabarits déjà vus.");
resultat(2, "Mêmes modèles, même test : le Transformer n'améliore ni le monde connu ni le monde inconnu", "sur les logs de SIEVE, test par gabarit : à gauche le monde connu (macro-F1), au centre et à droite le monde inconnu (AUROC).",
  (s) => s.addChart(pres.charts.BAR, [{ name: "TF-IDF mots", labels: ["Macro-F1\n(classes connues)", "AUROC\n(score de confiance)", "AUROC\n(meilleur score)"], values: [0.490, 0.599, 0.625] }, { name: "DistilBERT", labels: ["Macro-F1\n(classes connues)", "AUROC\n(score de confiance)", "AUROC\n(meilleur score)"], values: [0.461, 0.548, 0.605] }], Object.assign(chartBase("Test, 5 rotations : monde connu et monde inconnu"), CH, barCol, { chartColors: [BLUE, CORAL], valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.25, dataLabelFormatCode: "0.00", dataLabelFontSize: 13, catAxisLabelFontSize: 12, showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: INK })),
  "Macro-F1 : bonnes réponses sur les classes connues. AUROC : 0,5 = hasard, 1 = parfait. Deux échelles différentes : on compare les modèles entre eux, pas les deux métriques entre elles.", "les deux modèles se comportent de la même façon : le type de modèle n'est pas le facteur décisif.", "repérer l'inconnu reste proche du hasard, loin de la cible fixée d'avance (0,80).");
resultat(3, "Aucun des dix scores d'inconnu n'approche 0,80 ; le seul gain net est la distance sur le Transformer", "même métrique pour tous les scores : l'AUROC au test, moyenne des cinq rotations.",
  (s) => s.addChart(pres.charts.BAR, [{ name: "AUROC", labels: ["TF-IDF : confiance", "TF-IDF : énergie", "TF-IDF : prototype", "TF-IDF : ensemble", "TF-IDF : hiérarchique", "TF-IDF : famille", "DistilBERT : confiance", "DistilBERT : énergie", "DistilBERT : Mahalanobis", "DistilBERT : kNN"], values: [0.599, 0.598, 0.625, 0.601, 0.609, 0.623, 0.548, 0.564, 0.605, 0.600] }], Object.assign(chartBase("AUROC au test, par score d'inconnu"), CH, { barDir: "bar", chartColors: [BLUE, BLUE, BLUE, BLUE, BLUE, BLUE, STEEL, STEEL, CORAL, STEEL], valAxisMinVal: 0.4, valAxisMaxVal: 0.9, valAxisMajorUnit: 0.1, dataLabelFormatCode: "0.00", dataLabelFontSize: 12, catAxisLabelFontSize: 11, catAxisOrientation: "maxMin", showLegend: false })),
  "0,5 = hasard, 1 = parfait. Les écarts entre scores de TF-IDF sont plus petits que le bruit entre rotations.", "pour le Transformer, mesurer la distance dans ses vecteurs aide un peu plus que sa seule confiance.", "aucune méthode ne se détache, et aucune n'approche la cible.");
resultat(4, "Les lettres trompeuses sont l'attaque la plus efficace, et leur effet croît avec le degré", "chaque attaque est jouée à trois degrés : faible, moyen, fort ; on suit les deux mêmes métriques.",
  (s) => { const L = ["Fautes de frappe", "Lettres\ntrompeuses", "Mots ajoutés"];
    s.addChart(pres.charts.BAR, [{ name: "Faible", labels: L, values: [1.3, 2.6, 1.1] }, { name: "Moyen", labels: L, values: [3.7, 8.5, 1.3] }, { name: "Fort", labels: L, values: [7.8, 21.5, 12.5] }], Object.assign(chartBase("Monde connu : perte de macro-F1 (%)"), CHL, barCol, { chartColors: [ICE, STEEL, BLUE], valAxisMinVal: 0, dataLabelFormatCode: "0.0", dataLabelFontSize: 10, catAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 11, legendColor: INK }));
    s.addChart(pres.charts.BAR, [{ name: "Faible", labels: L, values: [0.599, 0.5945, 0.6052] }, { name: "Moyen", labels: L, values: [0.592, 0.5803, 0.611] }, { name: "Fort", labels: L, values: [0.5822, 0.5619, 0.5982] }], Object.assign(chartBase("Monde inconnu : AUROC"), CHR, barCol, { chartColors: [ICE, STEEL, BLUE], valAxisMinVal: 0.5, valAxisMaxVal: 0.65, valAxisMajorUnit: 0.05, dataLabelFormatCode: "0.00", dataLabelFontSize: 10, catAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 11, legendColor: INK })); },
  "Modèle TF-IDF mots, logs SIEVE. Degrés : fautes et lettres sur 5, 15, 30 % ; mots ajoutés 10, 30, 100 %.", "les fautes et les mots ajoutés ne gênent qu'à forte dose, et le classement des inconnus tient.", "les lettres trompeuses gênent vite et font rejeter de plus en plus de logs légitimes.");
resultat(5, "Une défense se juge contre une autre table que celle de l'attaque : seule la table officielle complète tient", "attaque par lettres trompeuses de la table officielle, aux trois degrés ; à droite, les parades testées au test.",
  (s) => { const C3 = ["Faible\n(5 %)", "Moyen\n(15 %)", "Fort\n(30 %)"], PL = ["Aucune", "Normali-\nsation", "Entraîn.\nadverse", "Les deux"];
    s.addChart(pres.charts.BAR, [{ name: "Sans défense", labels: C3, values: [2.5, 8.5, 16.5] }, { name: "Table maison", labels: C3, values: [2.3, 8.1, 15.6] }, { name: "Moitié de la table officielle", labels: C3, values: [1.4, 4.3, 8.0] }, { name: "Table officielle complète", labels: C3, values: [0.0, 0.2, 0.2] }], Object.assign(chartBase("Perte de macro-F1 (%) par degré"), CHL, barCol, { chartColors: [ICE, STEEL, BLUE, CORAL], valAxisMinVal: 0, dataLabelFormatCode: "0.0", dataLabelFontSize: 9, catAxisLabelFontSize: 10, showLegend: true, legendPos: "b", legendFontSize: 9, legendColor: INK }));
    s.addChart(pres.charts.BAR, [{ name: "Baisse moyenne", labels: PL, values: [6.7, 3.1, 2.3, 0.6] }, { name: "Pire baisse", labels: PL, values: [21.5, 12.5, 7.2, 6.5] }], Object.assign(chartBase("Parades au test : baisse (%)"), CHR, barCol, { chartColors: [BLUE, CORAL], valAxisMinVal: 0, dataLabelFormatCode: "0.0", dataLabelFontSize: 10, catAxisLabelFontSize: 9, showLegend: true, legendPos: "b", legendFontSize: 11, legendColor: INK })); },
  "Barre basse = défense efficace. Testée avec sa propre table, une défense paraît parfaite : test circulaire, non montré.", "plus la défense connaît de caractères, plus la perte baisse, et combiner les parades est le plus efficace.", "une défense incomplète laisse passer une grande partie de l'attaque, surtout au degré fort.");

// 24 et 25. Limites : du protocole, puis par rapport aux objectifs
{
  const s = slide("Conception - Limites de la conception (1/2)", "Six limites des données et du protocole bornent ce que l'on peut affirmer");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 14, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 14, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  const N = (t) => Cc(String(t), { fontFace: HEAD, fontSize: 22, color: CORAL });
  s.addTable([[H(""), H("Limite"), H("Ce que cela change pour les conclusions")],
    [N(1), Cc("Données synthétiques : 440 gabarits, 311 reconstruits", { bold: true }), Cc("Les scores mesurent des gabarits, pas des logs réels")],
    [N(2), Cc("Taxonomie non validée par un expert SIEM", { bold: true }), Cc("Les 8 familles restent une hypothèse de démonstration")],
    [N(3), Cc("Peu de gabarits distincts : 36 en validation, 45 au test", { bold: true }), Cc("Un écart inférieur à 0,05 est indétectable")],
    [N(4), Cc("Trois essais pour le Transformer, un seul pour la plupart des autres modèles", { bold: true }), Cc("Le bruit d'entraînement n'est pas toujours mesuré")],
    [N(5), Cc("Test scellé déjà ouvert une fois", { bold: true }), Cc("Les scores ajoutés ensuite sont comparés sur la validation seulement")],
    [N(6), Cc("Pas de logs réels ; attaques surtout non adaptatives", { bold: true }), Cc("Aucune garantie face à un attaquant qui connaît le modèle")]],
    { x: X0, y: 2.0, w: CW, colW: [0.7, 5.6, 5.63], rowH: [0.45, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
}
{
  const s = slide("Conception - Limites de la conception (2/2)", "Chaque objectif fixé est atteint, mais chacun a sa limite ; l'objectif général l'est en partie seulement");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 13.5, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 13, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  s.addTable([[H("Objectif fixé"), H("Résultat"), H("Sa limite")],
    [Cc("Général : mesurer jusqu'où, sans tricher", { bold: true }), Cc("Évaluation sans fuite réalisée"), Cc("Données synthétiques : valeur sur du réel inconnue")],
    [Cc("1  Mesurer l'effet de la triche", { bold: true }), Cc("Atteint : de 0,97 à 0,46"), Cc("Gabarits reconstruits : 311 sur 440")],
    [Cc("2  Comparer trois représentations", { bold: true }), Cc("Atteint : le Transformer n'est pas meilleur"), Cc("3 graines, pas de balayage de réglages")],
    [Cc("3  Comparer huit scores d'inconnu", { bold: true }), Cc("Atteint : aucun n'atteint 0,80"), Cc("36 et 45 gabarits : écart inférieur à 0,05 indétectable")],
    [Cc("4  Tester attaques et défenses", { bold: true }), Cc("Atteint : table officielle à 0,2 % de perte"), Cc("Attaques surtout non adaptatives ; synonymes exclus")],
    [Cc("5  Livrer un notebook reproductible", { bold: true }), Cc("Atteint : 99 affirmations, test scellé"), Cc("Données SIEVE non redistribuables ; test déjà ouvert")]],
    { x: X0, y: 2.0, w: CW, colW: [3.9, 3.9, 4.13], rowH: [0.45, 0.72, 0.72, 0.72, 0.72, 0.72, 0.72], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
}

// 26 et 27. Conclusion : réponse aux objectifs, puis perspectives
{
  const s = slide("Conclusion (1/2)", "Évaluer par gabarit change la conclusion ; détecter l'inconnu reste un problème ouvert");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 13.5, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 13.5, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  const K = (t) => Cc(t, { bold: true, color: CORAL, fontFace: HEAD, fontSize: 16 });
  s.addTable([[H("Objectif"), H("Verdict"), H("Ce qu'il faut retenir")],
    [Cc("Général", { bold: true }), Cc("En partie"), Cc("Sans fuite, 0,46 en monde connu et 0,60 pour repérer l'inconnu : le problème reste ouvert")],
    [Cc("1  Triche", { bold: true }), Cc("Atteint"), Cc("Sur SIEVE, 0,97 → 0,46 : c'est le découpage, pas le modèle, qui fait l'écart")],
    [Cc("2  Représentations", { bold: true }), Cc("Atteint"), Cc("Transformer 0,46 contre 0,49 ; la distance Mahalanobis gagne 0,057 sur ses vecteurs ")],
    [Cc("3  Scores d'inconnu", { bold: true }), Cc("Atteint"), Cc("Meilleur AUROC 0,625 pour une cible à 0,80")],
    [Cc("4  Attaques, défenses", { bold: true }), Cc("Atteint"), Cc("Lettres trompeuses : jusqu'à 21,5 % de perte ; table officielle : 0,2 %")],
    [Cc("5  Notebook", { bold: true }), Cc("Atteint"), Cc("Reproductible : 99 affirmations vérifiées, test scellé, dépôt public")]],
    { x: X0, y: 2.0, w: CW, colW: [2.6, 1.5, 7.83], rowH: [0.45, 0.78, 0.72, 0.72, 0.72, 0.72, 0.72], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
}
{
  const s = slide("Conclusion (2/2)", "Chaque limite appelle une perspective, et la première est de passer au réel");
  const H = (t) => ({ text: t, options: { bold: true, color: BLUE, fontSize: 13.5, fontFace: BODY, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: BLUE, pt: 1.25 }, { type: "none" }] } });
  const Cc = (t, o = {}) => ({ text: t, options: Object.assign({ fontSize: 14, fontFace: BODY, color: INK, valign: "middle", border: [{ type: "none" }, { type: "none" }, { type: "solid", color: LINE, pt: 0.75 }, { type: "none" }] }, o) });
  s.addTable([[H("Limite"), H("Perspective")],
    [Cc("Données synthétiques", { bold: true }), Cc("Tester sur de vrais logs : les 440 logs réels du CDS, puis des logs d'entreprise")],
    [Cc("Taxonomie non validée", { bold: true }), Cc("Faire valider les 8 familles par un expert SIEM")],
    [Cc("Peu de gabarits, peu de graines", { bold: true }), Cc("Plus de gabarits distincts et plus de graines, pour mesurer le bruit")],
    [Cc("Détection de l'inconnu faible", { bold: true }), Cc("Covariance par classe pour Mahalanobis ; mesurer si la famille proposée est la bonne")],
    [Cc("Attaques peu adaptatives", { bold: true }), Cc("Attaques qui s'adaptent à la défense ; reconnaissance de mots avant le classifieur ")]],
    { x: X0, y: 2.0, w: CW, colW: [4.2, 7.73], rowH: [0.45, 0.62, 0.62, 0.62, 0.62, 0.62], margin: [0.05, 0.1, 0.05, 0.05], autoPage: false });
  dark(s, X0, 6.0, CW, 0.85);
  T(s, "À retenir : avant de croire un score, regarder comment on a séparé l'entraînement du test.", { x: X0 + 0.3, y: 6.0, w: CW - 0.6, h: 0.85, fontSize: 18, fontFace: HEAD, color: "FFFFFF", valign: "middle" });
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
  s.addNotes(NOTES[n]);
}

// 29 et 30. Références (générées à partir des citations réellement utilisées, liens cliquables)
{
  const PER = 12, nCols = 2, nPages = Math.ceil(ORDER.length / (PER * nCols));
  for (let pg = 0; pg < nPages; pg++) {
    const s = slide("Références" + (nPages > 1 ? " (" + (pg + 1) + "/" + nPages + ")" : ""), "Chaque numéro correspond à un [n] placé à côté d'une information dans une diapositive");
    for (let c = 0; c < nCols; c++) {
      const a = pg * PER * nCols + c * PER, b = Math.min(a + PER, ORDER.length); if (a >= ORDER.length) break;
      const items = [];
      ORDER.slice(a, b).forEach((k, i) => {
        const d = DEFS[k], m = d.match(/(arXiv:\d{4}\.\d{4,5})|(doi:\S+?)(?=[.,]?(\s|$))|(\b[a-z0-9.-]+\.(?:com|org|ai|edu|cc|de)\/\S+)/);
        let url = null;
        if (m) url = m[1] ? "https://arxiv.org/abs/" + m[1].slice(6) : m[2] ? "https://doi.org/" + m[2].slice(4) : "https://" + m[4];
        const base = { fontSize: 10.5, color: INK, fontFace: BODY, paraSpaceAfter: 5 };
        if (!m) { items.push({ text: `[${a + i + 1}] `, options: { ...base, bold: true, color: CORAL } }, { text: d, options: { ...base, breakLine: true } }); return; }
        const before = d.slice(0, m.index), after = d.slice(m.index + m[0].length);
        items.push({ text: `[${a + i + 1}] `, options: { ...base, bold: true, color: CORAL } }, { text: before, options: base },
          { text: m[0], options: { ...base, color: "1F5FBF", underline: { style: "sng" }, hyperlink: { url, tooltip: url } } }, { text: after, options: { ...base, breakLine: true } });
      });
      T(s, items, { x: c === 0 ? X0 : 6.85, y: 1.6, w: 5.8, h: 5.3, fontSize: 10.5 });
    }
  }
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  if (applyTheme) await applyTheme(OUT, THEME); else console.log("apply_theme.js non chargé (définir PPTX_SKILL_DIR)");
  console.log("écrit :", OUT, "—", n, "diapositives ;", ORDER.length, "références :", ORDER.join(", "));
})();
