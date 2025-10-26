# Rapport Machine Learning

## Introduction
Ce rapport a pour but de décrire les étapes et les études réalisées à l'élaboration des modèles de Machine Learning de classification et de régression, en passant par l'exploration des données, la validation des variables d'entraînement, leur traitement, puis les stratégies mises en place pour sélectionner des modèles, et enfin, leur évaluation.
### 🎯Stratégie
>Afin d'orienter l'exploration des données, nous listons le cahier des charges que nous souhaitons implémenter au sein de l'application.

**Ergonomie d'utilisation:** 
- L'utilisateur doit utiliser les modèles pour pouvoir prédire la **classe DPE** de son appartement et/ou **sa consommation**. Ainsi, l'utilisateur doit pouvoir utiliser sa consommation réelle si elle est connue afin d'améliorer la prédiction de sa classe.
-  L'utilisateur de notre application ne pourra fournir qu'une quantité limité de données pour la prédiction de sa classe. Ainsi les données trop techniques, ou difficilement obtenable seront évitées afin de fournir un formulaire de prédiction cohérent.
 
 **Prédictions:** 
 - Nous souhaitons élaborer un modèle capable de prédire chacune des **7 classes DPE**.
- Concernant la régression, nous prédirons le **coût total 5 usages**.
>[!Remarque]
>Le coût total 5 usages fait partie de l'enjeu de prédiction de la régression et fait partie des données utiles à l'estimation de la classe DPE. Un utilisateur possédant sa consommation pourra directement s'en servir pour prédire sa classe DPE. Dans le cas où l'utilisateur ne la possède pas, le **modèle de regression prédira la consommation théorique**, et cet élément sera ensuite utilisé pour **une double prédiction pour prédire la classe DPE**.

**Scope:**
- Nous souhaitons pouvoir élaborer un modèle utilisable sur la l'ensemble du **territoire Français**.
---
## Données

### Sources
 **API de l'ademe**
 Source principale des données de l'entraînement des modèles de classification et de régression.
- DPE logements existants: https://data.ademe.fr/datasets/dpe03existant
- DPE logements neufs: https://data.ademe.fr/datasets/dpe02neuf

**Dataset Communes de France**
Dataset permettant de récupérer l'altitude des communes de France.
- https://www.data.gouv.fr/datasets/communes-france-1/

**API Open-Elevation**
API permettant de récupérer l'altitude à l'aide de la longitude et la latitude, permettant de compléter les données parfois manquantes du *Dataset communes de France*.
- https://open-elevation.com/

**Tableau de répartition des zones climatiques en France**
Permettant de faire intervenir les différences de climat dans la prédiction.
- https://www.ecologie.gouv.fr/sites/default/files/documents/La%20r%C3%A9partition%20des%20d%C3%A9partements%20par%20zone%20climatique.pdf

### Extraction des données
La majorité de la donnée a été récupérée de l'API de **l'ademe**. Afin d'établir un data set représentatif de la totalité de la France, nous avons extrait tout d'abord extrait la *liste de tous les départements et le nombre d'éléments* en utilisant les routes d'API d'agrégation. Cette liste de département nous a ensuite permis d'extraire 10.000 lignes de chaque département, à la fois sur les *logements existants* et sur *les logements neufs*. Ainsi, environ 1 millions de lignes ont pu être récupérées sur l'ensemble du territoire, comptabilisant plus de 2 heures de téléchargement.
### Sélection des variables
Les variables utilisées pour nourrir les modèles de prédiction ont été triées:
- En étudiant la **documentation de l'établissement d'un DPE** et en sélectionnant toutes les variables qui semblent pertinentes et liées à la consommation d'énergie.
- Parmi de nombreuses variables, celles qui possédaient **des valeurs nulles à hauteur de plus de 10% du dataset** ont été **retirées**.
- Les variables dont l'information peut être facilement retrouvées ont été privilégiés: ces variables apparaîtront pour la plupart dans le formulaire de prédiction de l'utilisateur, il ne faut donc pas de demande trop *techniques*.
- Les variables de coûts ou de consommation (pour le modèle de classification), toutes très corrélées entre elles, ont été limitées au `coût_total_5_usages` de l'année en cours.
- Des variables supplémentaires ont été ajoutés de sources externes: **l'altitude et la zone climatique**, pouvant toutes deux influer sur la consommation d'énergie.

Ainsi, la liste suivante de variables ont été retenus:

| Nom de la variable                      | Description                                            | Unité                                                              | Interprétation                                                                       |
| --------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| **`cout_total_5_usages`**               | Coût total annuel associé aux 5 usages énergétiques    | € / an                                                             | Reflète la dépense énergétique globale du logement.                                  |
| **`surface_habitable_logement`**        | Surface habitable totale du logement                   | m²                                                                 | Plus la surface est grande, plus la consommation énergétique potentielle est élevée. |
| **`nombre_niveau_logement`**            | Nombre total de niveaux (étages) du logement           | nombre entier                                                      | Influence la répartition thermique et la surface d’échange avec l’extérieur.         |
| **`age_batiment`**                      | Âge du bâtiment depuis sa construction                 | années                                                             | Les bâtiments anciens ont souvent une isolation moins performante.                   |
| **`altitude_moyenne`**                  | Altitude moyenne du logement                           | mètres                                                             | Influence les conditions climatiques locales (température moyenne, humidité).        |
| **`type_energie_principale_chauffage`** | Source d’énergie principale utilisée pour le chauffage | électricité, gaz, fioul, bois, pompe à chaleur...                  | Influence directe sur le coût énergétique et les émissions.                          |
| **`type_batiment`**                     | Catégorie du bâtiment résidentiel                      | maison individuelle, immeuble collectif, logement intermédiaire... | Reflète les besoins énergétiques moyens.                                             |
| **`zone_climatique`**                   | Zone climatique de localisation du logement            | H1, H2, H3                                                         | Impacte la rigueur climatique.                                                       |

### Transformation des données
Les données ont été scrupuleusement vérifiées, homogénéisés et transformées pour réduire le bruit. La grande quantité de données que nous avons extraites a permis d'éliminer certains outliers ainsi que certaines valeurs manquantes quand aucune solution raisonnable n'a pu être trouvé. Ci-dessous, le détail des principales transformations effectuées:
- **age du bâtiment**: Calculé à partir de l'année du bâtiment. Transformé en âge pour permettre au modèle d'apprendre plus facilement qu'avec l'année.
- **Coût 5 usages**: Utilisation de la méthode *inter-quartile* pour supprimer les valeurs qui semblaient aberrates.
- **Type Energie chauffage**: Variable à 14 modalités, dont 2 principales. Les modalités trop rares ont été *groupées* dans une modalité 'autres'.
- **Surface logement**: Utilisation de la méthode interquartile pour supprimer les valeurs aberrantes.
- **Nombre niveau logement**: Les étages ont été limitées à 10 maximum.
- **Type bâtiment**: Suppression des lignes contenant des valeurs manquantes (peu de valeurs nulles).
- **Altitude**: L'altitude a été récupérée en croisant les données récupérées sur l'API élévation et le dataset des villes de France sur le code INSEE. Les données manquantes ont été moyennées sur le département. 

### Répartition des classes DPE
La répartition des classes DPEs après extraction est restée quasiment inchangée lors du traitement:
<img width="553" height="425" alt="image" src="https://github.com/user-attachments/assets/44ad48dc-b23f-4783-9514-91de2423dd9c" />

---
## Modèle de classification
### Sélection des modèles
Le choix du modèle a été réalisé en testant et comparant plusieurs modèles mettant en jeux des algorithmes différents afin de chercher le plus adapté.
- **Des arbres**: Random Forest, XGBoost (avec et sans pénalisation).
- **Un classifieur linéaire**: Régression logistique.
- **Un classifieur à frontière quadratique**: Analyse discriminante quadratique.
- **Un classifieur basé sur le calcul des distances**: le KNN (K Nearest Neighbors).
### Préparation des données entraînement/test
**Préparation du set d'entraînement**: Utilisation d'un split **stratifié** 70/30.
**Pipeline de prétraitement**: un `Scaler` ainsi qu'un `OneHotEncoder` pour centrer réduire les variables d'apprentissage (sauf pour le *RandomForest*).
**Label Encoder**: Pour labéliser en variable numérique la classe DPE, permettant d'introduire la notion de hiérarchie entre les classes.

### Détermination des hyperparamètres pour chacun des modèles.
La méthodologie suivante à été appliquée, en utilisant le même set d'entraînement pour tous les algorithmes :
- Recherche des meilleurs hyper-paramètres pour chacun des algorithmes à l'aide d'un **GridSearchCV** et un paramétrage de **5 folds** pour la **validation croisée stratifiée**. (150 entraînements/modèles environ)
- Suivi des expériences à l'aide de la librairie **MLFlow**.
- La **métrique** utilisée pour comparer les modèles est la **balanced_accuracy**, permettant d'évaluer les modèles en prenant en compte **les modalités rares** afin d'essayer de pousser le modèle à na pas négliger les classes G et F, moins représentées.

### Comparaison des algorithmes
Une fois les hyperparamètres trouvés pour chacun des algorithmes, nous avons tenté d'évaluer la performance des modèles et de les comparer. Nous donc répéter **30** fois la procédure suivante, pour chacun des algorithmes:
- Re-générer le split Train/Test.
- Entraîner le modèle et effectuer l'évaluation sur les données d'entraînement. (**balanced_accuracy, accuracy, f1_score, hamming_loss**)
- **30** Récupérations des métriques de test: meilleure évaluation en prenant la moyenne.
- Estimation de la stabilité en calculant les intervalles de confiances à l'aide d'un **test de Student** à 95%.
  
$$CI = \left( \bar{x} - t_{\alpha/2} \cdot \frac{s}{\sqrt{n}},\; \bar{x} + t_{\alpha/2} \cdot \frac{s}{\sqrt{n}} \right)$$

>- $\bar{x}$ → moyenne de l’échantillon
>- $s$ → écart-type
>- $n$ → taille de l’échantillon (30)
>- $t_{\alpha/2}$​ → quantile de la loi de Student pour le niveau de confiance choisi
>- $CI$ → intervalle de confiance

<img width="778" height="466" alt="image" src="https://github.com/user-attachments/assets/eb26b4bb-78eb-4403-8a02-21de4822a6be" />



| **Modèle**                 | **Métrique**      | **Moyenne (mean)** | **Écart-type (std)** | **IC95%**      |
| -------------------------- | ----------------- | ------------------ | -------------------- | -------------- |
| 🟥 **XGBoost**             | Balanced Accuracy | 0.743              | 0.001                | [0.743, 0.743] |
|                            | Accuracy          | 0.797              | 0.001                | [0.797, 0.797] |
|                            | F1-score (macro)  | 0.747              | 0.001                | [0.747, 0.748] |
|                            | F1-score (micro)  | 0.797              | 0.001                | [0.797, 0.797] |
| 🟨 **KNN**                 | Balanced Accuracy | 0.707              | 0.001                | [0.706, 0.707] |
|                            | Hamming Loss      | 0.203              | 0.001                | [0.203, 0.203] |
|                            | Accuracy          | 0.777              | 0.001                | [0.777, 0.778] |
|                            | F1-score (macro)  | 0.714              | 0.001                | [0.713, 0.714] |
|                            | F1-score (micro)  | 0.777              | 0.001                | [0.777, 0.778] |
|                            | Hamming Loss      | 0.223              | 0.001                | [0.222, 0.223] |
| 🟦 **Logistic Regression** | Balanced Accuracy | 0.632              | 0.001                | [0.631, 0.632] |
|                            | Accuracy          | 0.713              | 0.001                | [0.713, 0.714] |
|                            | F1-score (macro)  | 0.643              | 0.001                | [0.643, 0.644] |
|                            | F1-score (micro)  | 0.713              | 0.001                | [0.713, 0.714] |
|                            | Hamming Loss      | 0.287              | 0.001                | [0.286, 0.287] |
| 🟩 **QDA**                 | Balanced Accuracy | 0.537              | 0.002                | [0.536, 0.538] |
|                            | Accuracy          | 0.633              | 0.001                | [0.632, 0.633] |
|                            | F1-score (macro)  | 0.546              | 0.002                | [0.545, 0.547] |
|                            | F1-score (micro)  | 0.633              | 0.001                | [0.632, 0.633] |
|                            | Hamming Loss      | 0.367              | 0.001                | [0.367, 0.368] |
| 🟫 **Random Forest**       | Balanced Accuracy | 0.292              | 0.004                | [0.290, 0.294] |
|                            | Accuracy          | 0.440              | 0.001                | [0.440, 0.441] |
|                            | F1-score (macro)  | 0.257              | 0.008                | [0.254, 0.260] |
|                            | F1-score (micro)  | 0.440              | 0.001                | [0.440, 0.441] |
|                            | Hamming Loss      | 0.560              | 0.001                | [0.559, 0.560] |

### XGBoost: évaluation finale
Les opérations effectuées ci-dessus nous permettent de conclure notre choix pour l'**XGBoost**. Afin d'estimer la véritable efficacité de notre algorithme. Nous effectuons un dernier split des données pour un entraînement et un test. Nous pouvons ainsi générer la **matrice de confusion** suivante qui complémente les précédentes mesures:

<img width="798" height="621" alt="image" src="https://github.com/user-attachments/assets/e9ce3ae5-ab99-4559-b62e-afd7071b037f" />


- Nous pouvons remarquer que l'algorithme arrive à prédire raisonnablement bien une grande partie des classes. Nous pouvons aussi noter que le modèle à appris de la **hiérarchisation des classes**: lorsque la prédiction est mauvaise, le modèle parvient tout de même à **prédire une classe proche** avec une tendance à modérer ses prédictions pour les classes centrales (C et D).


### Importance des variables
La librairie **XGBoost** permettant de monter le modèle offre le moyen de récupérer l'importance des variables dans la determination des classes. Cette "importance" est déterminé selon deux critères:
- Le nombre de fois où la variable à été **utilisée pour séparer un nœud de l'arbre**.
- L'importance du **Gain** engendré par la séparation de la variable (réduction de l'enthropie ou de l'impureté de Gini)
<img width="1263" height="673" alt="image" src="https://github.com/user-attachments/assets/b4ed71e7-dc35-407c-a48e-5e6aecb2219f" />

Ainsi notre modèle se base principalement sur **l'âge du bâtiment**, **le type d'énergie principale pour le chauffage**, et le **type du bâtiment**.
