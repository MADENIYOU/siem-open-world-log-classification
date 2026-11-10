# Revue de Littérature : Classification Hiérarchique de Logs SIEM en Monde Ouvert avec Apprentissage Profond Sensible à l'Incertitude

## Résumé Analytique
Ce rapport constitue une synthèse exhaustive de l'état de l'art concernant la classification sémantique et hiérarchique des journaux de sécurité (logs SIEM) dans un environnement de monde ouvert (Open-World). L'analyse porte sur une sélection rigoureuse de 10 articles pivots publiés entre 2020 et 2026, explorant les synergies entre le traitement du langage naturel (NLP), les structures taxonomiques et la gestion de l'incertitude via l'apprentissage profond.

Les conclusions mettent en évidence une transition technologique majeure : l'abandon des méthodes heuristiques au profit de modèles Transformers spécialisés (BERT, DeBERTa, SecureBERT). Bien que ces modèles excellent dans la capture de la sémantique cyber, une lacune critique subsiste : l'absence d'architectures intégrées capables de réaliser une classification hiérarchique tout en détectant et rejetant les événements inconnus (Out-of-Distribution). Le projet proposé, centré sur le dataset SIEVE, vise à combler ce vide en introduisant un mécanisme de rejet basé sur l'incertitude au sein d'une structure de décision hiérarchique, garantissant ainsi la robustesse du système face aux menaces émergentes et non répertoriées.

## Table des Matières
1. [Introduction](#1-introduction)
2. [Synthèse Thématique de l'État de l'Art](#2-synthèse-thématique-de-létat-de-lart)
    - [Axe 1 : Évolution du NLP pour l'Analyse des Logs SIEM](#axe-1--évolution-du-nlp-pour-lanalyse-des-logs-siem)
    - [Axe 2 : Modélisation Hiérarchique et Cohérence des Taxonomies](#axe-2--modélisation-hiérarchique-et-cohérence-des-taxonomies)
    - [Axe 3 : Détection en Monde Ouvert et Estimation de l'Incertitude](#axe-3--détection-en-monde-ouvert-et-estimation-de-lincertitude)
3. [Matrice de Littérature et Analyse Critique](#3-matrice-de-littérature-et-analyse-critique)
    - [Tableau de Synthèse des Travaux Clés](#tableau-de-synthèse-des-travaux-clés)
    - [Discussion Détaillée des Études Sélectionnées](#discussion-détaillée-des-études-sélectionnées)
4. [Identification du Research Gap et Contribution du Projet](#4-identification-du-research-gap-et-contribution-du-projet)
    - [Le Vide Scientifique Actuel](#le-vide-scientifique-actuel)
    - [Innovation du Pipeline SIEVE](#innovation-du-pipeline-sieve)
5. [Conclusion](#5-conclusion)

---

## 1. Introduction
La cybersécurité moderne est confrontée à un déluge de données de logs, dont l'analyse est devenue le goulot d'étranglement des SOC (Security Operations Centers). La classification automatique de ces événements est essentielle pour prioriser les alertes et détecter les incidents. Historiquement, cette tâche était accomplie par des systèmes rigides basés sur des expressions régulières, incapables de s'adapter à la variabilité du langage machine et aux tactiques d'évasion des attaquants.

L'émergence des modèles Transformers a marqué un tournant, permettant une compréhension contextuelle des logs. Cependant, deux réalités opérationnelles compliquent cette tâche : la structure intrinsèquement hiérarchique des taxonomies de sécurité et le caractère "ouvert" du domaine de la menace, où de nouvelles classes d'attaques apparaissent continuellement. Cette revue de littérature examine comment les recherches actuelles traitent ces dimensions et identifie les opportunités pour une approche unifiée combinant hiérarchie et détection d'inconnus.

---

## 2. Synthèse Thématique de l'État de l'Art

### Axe 1 : Évolution du NLP pour l'Analyse des Logs SIEM
Le passage au NLP "parser-free" (sans parseur) est la tendance dominante. Les modèles ne se contentent plus de traiter des jetons isolés, mais apprennent la sémantique structurelle des logs.
- **Spécialisation du Domaine :** Les travaux sur **SecureBERT [10]** et **CySecBERT [8]** démontrent l'importance du pré-entraînement adaptatif. En utilisant des corpus de cybersécurité (rapports de vulnérabilités, logs réels), ces modèles développent un vocabulaire et une compréhension des relations techniques supérieurs aux modèles BERT génériques.
- **Robustesse Sémantique :** **Russkikh et al. (2026)** montrent que les modèles basés sur BERT sont plus performants pour détecter des activités malveillantes sémantiquement complexes ou obscurcies, là où les méthodes statistiques classiques comme TF-IDF échouent à percevoir l'intention derrière les variations syntaxiques [1].
- **Efficacité et Légèreté :** Pour des applications SIEM en temps réel, l'utilisation de modèles plus légers comme DistilBERT [4] ou de stratégies comme LoRA (Low-Rank Adaptation) [5] permet de maintenir des performances élevées avec des ressources computationnelles réduites.

### Axe 2 : Modélisation Hiérarchique et Cohérence des Taxonomies
La classification hiérarchique permet de structurer la connaissance de sécurité. Elle assure qu'un événement est compris non seulement comme une instance unique, mais comme faisant partie d'une catégorie fonctionnelle plus large.
- **Cohérence Parent-Enfant :** Un défi majeur est d'éviter les prédictions illogiques. **Pan & Wu (2025)** proposent des mécanismes de régularisation de cohérence pour s'assurer que les prédictions au niveau de la classe fine respectent la sémantique de la classe parente [12].
- **Exploitation de la Sémantique des Labels :** Des modèles comme **HLAST [4]** utilisent des transformateurs conscients des étiquettes (label-aware), où les définitions textuelles des classes sont intégrées dans le processus d'apprentissage, facilitant la classification dans des taxonomies complexes.
- **Structuration de l'Espace Latent :** L'approche de **Corbelle et al. (2024)** utilise des codes hiérarchiques pour guider l'organisation des vecteurs d'embedding dans BERT, améliorant ainsi la séparation des clusters d'anomalies [6].

### Axe 3 : Détection en Monde Ouvert et Estimation de l'Incertitude
En cybersécurité, un modèle qui prédit toujours une classe connue est dangereux. La gestion du "monde ouvert" (Open-Set) est donc impérative.
- **Scores d'Incertitude :** La littérature explore plusieurs métriques pour identifier les données hors-distribution (OOD). Si le Maximum Softmax Probability (MSP) reste une référence, des scores plus robustes comme l'énergie (Energy-based scores) ou la distance de Mahalanobis dans l'espace d'embedding sont de plus en plus privilégiés pour leur capacité de séparation [3], [7].
- **Mécanismes de Rejet :** L'approche bi-couche de **Prasetyo et al. (2025)** illustre l'utilisation de deux modèles (BERT et RoBERTa) pour séparer le connu de l'inconnu [7].
- **Incertitude Bayésienne :** L'utilisation de **Bayesian Ensemble Transformers [2]** permet une décomposition fine de l'incertitude, distinguant ce que le modèle "ne sait pas" parce qu'il n'a pas vu de données similaires de ce qui est intrinsèquement ambigu.

---

## 3. Matrice de Littérature et Analyse Critique

### Tableau de Synthèse des Travaux Clés

| Titre et Année | Auteurs et Conférence | Méthodologie NLP/Architecture | Limites / Gaps (vs Projet) |
| :--- | :--- | :--- | :--- |
| **Influence of Log Structure... (2026)** [1] | Russkikh et al., RusAutoCon | 6 modèles Transformer vs TF-IDF. Attention désencapsulée. | Pas de hiérarchie ni de gestion open-world. |
| **HLAST: Hierarchical Log Analysis (2025)** [4] | Vasan et al., ICAICCIT | DistilBERT + T5 (Label-aware summarisation). | Pas de détection OOD/Open-set. |
| **Semantic Hierarchical Classification (2024)** [6] | Corbelle et al., Applied Sciences | BERT-base avec codes hiérarchiques sémantiques. | Pas de mécanisme de rejet explicite. |
| **Classification Of Cyber Attack (2025)** [7] | Prasetyo et al., IJEEEMI | BERT + RoBERTa (double couche pour anomalies). | Pas de structure hiérarchique de labels. |
| **CySecBERT (2022)** [8] | Bayer et al., arXiv | DAPT (Domain Adaptive Pre-training) sur corpus cyber. | Modèle de base, pas de tête hiérarchique OOD. |
| **SecMTL-BERT (2026)** [9] | Muslam et al., IJASCA | Cadre multi-tâches avec module Cross-Task Attention. | Tâches isolées, manque de cohérence hiérarchique. |
| **Hierarchical classification (2025)** [12] | Pan & Wu, arXiv | Sémantique BERT + régularisation de cohérence. | Généraliste, pas spécifique aux logs SIEM. |
| **LLM-Refined Taxonomies (2026)** [13] | Golde et al., arXiv | Raffinement de taxonomies par LLM pour BERT. | Pas de focus sur le monde ouvert/rejet. |
| **LogBERT (2021)** [11] | Guo et al., IJCNN | Apprentissage auto-supervisé (MLM) pour anomalies. | Classification plate, pas de hiérarchie. |
| **SecureBERT (2022)** [10] | Aghaei et al., IEEE | RoBERTa avec tokenizer BPE cyber spécialisé. | Monde fermé, pas de gestion taxonomique. |

### Discussion Détaillée des Études Sélectionnées
L'analyse approfondie de ces travaux révèle plusieurs points critiques. **SecureBERT [10]** et **CySecBERT [8]** ont posé les jalons de l'adaptation au domaine, prouvant que les connaissances linguistiques spécifiques à la cybersécurité sont indispensables pour une classification précise. Cependant, ils s'arrêtent à une classification "flat" qui ne reflète pas la réalité des SIEM. 

Les travaux de **Vasan et al. [4]** sur **HLAST** introduisent la notion de hiérarchie et de résumé, ce qui est crucial pour les analystes SOC, mais leur modèle reste vulnérable aux classes inconnues car il ne dispose d'aucun mécanisme de rejet. À l'inverse, **Prasetyo et al. [7]** adressent le monde ouvert avec une architecture bi-couche ingénieuse, mais perdent l'avantage sémantique d'une taxonomie structurée.

Le travail de **Pan & Wu [12]** est celui qui se rapproche le plus de nos préoccupations de cohérence hiérarchique, mais son application à des logs SIEM (dont la structure est très différente du langage naturel classique) reste à explorer. Enfin, **LogBERT [11]** demeure la référence pour l'apprentissage de la normalité des logs, mais sa transition vers une classification multi-classes en monde ouvert hiérarchique constitue le saut qualitatif que notre projet se propose de réaliser.

---

## 4. Identification du Research Gap et Contribution du Projet

### Le Vide Scientifique Actuel
Le "Research Gap" identifié réside dans le manque d'intégration. La littérature actuelle est segmentée en trois silos :
1. **Les modèles sémantiques cyber** (bons pour comprendre le log, mais en monde fermé et plat).
2. **Les modèles hiérarchiques** (bons pour structurer la connaissance, mais sans gestion de l'incertitude).
3. **Les détecteurs d'inconnus (OOD)** (bons pour rejeter les nouveautés, mais sans cadre taxonomique).

### Innovation du Pipeline SIEVE
Notre projet comble ce vide par une approche holistique. En utilisant le dataset SIEVE, nous construisons une taxonomie de 30 classes regroupées en familles fonctionnelles.
- **Nouveauté 1 :** L'architecture propose deux têtes de classification (Famille et Classe Fine) avec une contrainte de cohérence sémantique, assurant qu'une "Alerte de Processus" ne soit jamais classée par erreur comme un "Événement Réseau".
- **Nouveauté 2 :** L'intégration de scores d'incertitude calibrés (Energy score ou Prototype-based) permet au modèle de rejeter les logs ne correspondant à aucune classe apprise, tout en conservant une prédiction fiable au niveau de la famille si possible.
- **Nouveauté 3 :** Le protocole expérimental open-set, avec des rotations de classes masquées, garantit que les résultats ne dépendent pas d'un choix spécifique de classes connues, assurant ainsi une généralisation réelle.

---

## 5. Conclusion
La revue de littérature confirme la pertinence et la nouveauté du projet "Open-World Hierarchical Cybersecurity Log Classification". Alors que les briques technologiques individuelles (Transformers, Hiérarchie, OOD) ont fait leurs preuves, leur fusion dans un système unifié pour les logs SIEM représente une avancée majeure pour la résilience des SOC. Notre approche permet de passer d'une détection réactive et fragile à une intelligence de sécurité proactive, capable de discerner avec précision le connu de l'inconnu tout en respectant la sémantique complexe du domaine.

## References

[1]A. R. Russkikh, D. Levshun, and I. Ushakov, “Influence of Log Structure and Semantic Complexity on the Expediency of BERT-Based Models for Malicious Activity Detection,” pp. 555–560, Sept. 2026, doi: 10.1109/rusautocon69876.2026.11707425.

[2]C. Prihantoro, “Automatic Network Incident Classification Menggunakan IndoBERT”, [Online]. Available: https://jurnal.imsi.or.id/index.php/jcosis/article/view/278

[3]S. K. T, S. Sathishwaran, and R. S, “AI-Powered Log Analysis with BERT for Automated Event Detection and Categorization,” pp. 1–6, Oct. 2025, doi: 10.1109/iceconf65644.2025.11379598.

[4]S. Vasan, S. V. Singh, D. Sharma, and S. Yadav, “HLAST: Hierarchical Label-Aware Summarisation Transformer for Enhanced Cybersecurity Log Analysis,” vol. 1, pp. 1296–1301, Oct. 2025, doi: 10.1109/icaiccit68829.2025.11434164.

[5]C. Hewagama, “Threat Detection Based on Log Analysis for Automating Security Information and Event Management (SIEM) Functionality”, [Online]. Available: https://rda.sliit.lk/entities/publication/9582fcc0-2803-43f4-9ad5-d503820f5a8f

[6]C. Corbelle, V. Carneiro, and F. Cacheda, “Semantic Hierarchical Classification Applied to Anomaly Detection Using System Logs with a BERT Model,” Applied Sciences, vol. 14, no. 13, pp. 5388–5388, June 2024, doi: 10.3390/app14135388.

[7]E. D. Prasetyo, B. Rahmat, A. P. Sari, and E. D. Prasetyo, “Classification Of Cyber Attack And Anomaly In Web Server Using Transformer and Transfer Learning,” Indonesian Journal of Electronics, Electromedical Engineering, and Medical Informatics, vol. 7, no. 4, pp. 713–723, Nov. 2025, doi: 10.35882/ijeeemi.v7i4.119.

[8]M. Bayer, P. Kuehn, R. Shanehsaz, and C. A. Reuter, “CySecBERT: A Domain-Adapted Language Model for the Cybersecurity Domain,” arXiv.org, vol. abs/2212.02974, Dec. 2022, doi: 10.48550/arXiv.2212.02974.

[9]A. Muslam, A. B. A. Alaasam, A. H. Mohammed, and Z. H. Khalil, “SecMTL-BERT: A Multi-Task Transformer Framework for Unified Information Systems Security Text Intelligence,” International journal of advances in soft computing and its applications, July 2026, doi: 10.15849/ijasca.v18i2.133.

[10]E. Aghaei, X. Niu, W. G. Shadid, and E. Al-Shaer, “SecureBERT: A Domain-Specific Language Model for Cybersecurity,” pp. 39–56, Apr. 2022, doi: 10.1007/978-3-031-25538-0_3.

[11]H. Guo, S. Yuan, and X. Wu, “LogBERT: Log Anomaly Detection via BERT,” Mar. 07, 2021. [Online]. Available: https://arxiv.org/abs/2103.04475v1

[12]S. Pan and D. Wu, “Hierarchical Text Classification with LLMs via BERT-Based Semantic Modeling and Consistency Regularization,” Aug. 2025, doi: 10.1145/3772900.3772994.

[13]J. Golde, N. Jedema, R. Krishnan, and P. Le, “Hierarchical Text Classification with LLM-Refined Taxonomies,” Jan. 26, 2026. [Online]. Available: https://arxiv.org/abs/2601.18375v1