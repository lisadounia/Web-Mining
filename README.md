# Web-Mining
# Analyse des inégalités sociales  

## Présentation du projet  
Dans le cadre du cours de **Web Mining**, nous nous sommes improvisés consultants pour l’ambassade britannique afin de mener une analyse approfondie sur les **inégalités sociales**. Ce projet vise à apporter des insights clés pour préparer les prochaines campagnes de sensibilisation et d’action.  

Deux questions principales ont orienté notre travail :  
1. **Quelles sont les thématiques clés permettant de mieux comprendre les inégalités sociales ?**  
2. **Comment les concepts clés liés aux inégalités sociales interagissent-ils entre eux ?**  

Pour y répondre, nous avons adopté une démarche en deux étapes principales :  
- **Web scraping** : Extraction d’articles pertinents depuis les sites **Wikipedia** et **BBC News**.
- **Analyses combinées** : Intégration de la **Link Analysis** et de la **Text Analysis**  pour une compréhension globale.  

Ces analyses nous ont permis de :  
- Identifier les thématiques essentielles en lien avec les inégalités sociales.  
- Visualiser les interactions complexes entre ces thématiques et concepts grâce à des graphes et des représentations textuelles.  
- Fournir des résultats exploitables pour guider les actions de l’ambassade.  

---
## Contributions  
- **Demolin Cyril**  
- **Dounia Lisa**  
- **Nanat Inas** 
---

## Arborescence des modules et scripts

- **data_collection** :  Récupération et structuration des données.
  - `Data_collection.py` : Extraction des données
  - `Collecte_de_BBC.py` : Collecter d'articles de la BBC
- **link_analysis** : Analyse des relations et visualisation des graphes.
  - `A.Structure_Cohésion` : Analyse de la structure et de la cohésion
  - `B.Analyse_similarités` : Étude des similarités
  - `C.Distances_euclidiennes` : Calcul des distances entre concepts

- **text_analysis** : Analyse sémantique et textuelle pour approfondir les résultats.
  - `Analyse_sémantique.py` : Étude des concepts clés
  - `Analyse_temporelle.py` : Analyse temporelle des articles
  - `BBC_ranking.py` : Classement des articles BBC
  - `Class_wiki.py` : Classification des articles Wikipedia
  - `Clustering.py` : Clustering thématique
  - `co_occurence.py` : Analyse de co-occurrences
  - `texte_nettoyage.py` : Prétraitement des données textuelles
  - `treemap.py` : Visualisation en treemap
  - `wikiquote.py` : Extraction de citations
  - `word_cloud.py` : Génération de nuages de mots
 



---
# Partie : Data Collection 
---

## Création Graphe

#### Objectif du Code
Ce code permet de construire un graphe représentant la structure de Wikipédia à partir d'un article donné (par défaut : **Social Inequality**). Il explore les relations entre articles similaires sur deux niveaux d'exploration de Wikipédia. 

Les étapes principales incluent : 
1. Création d'une matrice **terme-document**.
2. Vectorisation de cette matrice.
3. Construction d'une matrice de similarité pour relier les articles.

#### Utilisation du Code
1. Par défaut, le code commence avec l'article Wikipédia **Social Inequality**.
2. Si vous souhaitez changer le point de départ, modifiez la variable `start_url` située à la ligne 190 dans le script.
3. Exécutez le code pour générer le graphe de similarité.

#### Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le code. Vous pouvez les installer via `pip` si nécessaire.

- **NLTK** : (Natural Language Toolkit) pour l'analyse textuelle.
- **requests** : Requêtes HTTP pour récupérer des données depuis Wikipédia.
- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **pandas** : Manipulation de données.
- **scipy** : Calculs scientifiques pour construire la matrice de similarité.

---
---
## Collection_de_BBC 

#### Objectif du Code
Ce code parcourt les pages du site **BBC News** pour collecter les articles liés aux inégalités sociales, en enregistrant leurs dates, catégories, et autres informations pertinentes.

#### Utilisation du Code
1. Exécutez le script Python.
2. Le programme générera automatiquement un fichier **CSV** contenant toutes les informations collectées.

#### Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le code. Vous pouvez les installer via `pip` si nécessaire.

- **requests** : Pour récupérer les données depuis le site BBC News.
- **BeautifulSoup (BS4)** : Pour scraper et analyser les données HTML.
- **pandas** : Pour manipuler et sauvegarder les données dans un fichier CSV.
---

# Partie : Link Analysis  
---
## A.Structure_Cohésion

### Points d'Articulation, Ponts et Composantes Fortement Connexes  

#### Objectif du Code
Ce script utilise une matrice d'adjacence pour analyser les propriétés structurelles d'un graphe dirigé représentant des concepts liés aux **inégalités sociales**.  
Il identifie les **points d'articulation**, les **ponts**, et les **composantes fortement connexes (SCC)** pour mieux comprendre les relations entre les nœuds du graphe.



#### Utilisation du Code

1. Assurez-vous de disposer de la matrice d'adjacence au format Excel (`adjacency_matrix_V2.xlsx`).
2. Exécutez le script Python.
3. Le programme fournira des informations sur :
   - Les propriétés générales du graphe (nœuds, arêtes, densité).
   - Les points d'articulation et leur impact.
   - Les ponts critiques dans la connectivité.
   - La composante fortement connexes et sa structure.



#### Packages à Installer

Avant d'exécuter le script, installez les packages suivants via `pip` :

- `pandas` : Manipulation de la matrice d'adjacence.

---

### Sous-groupes, Cliques et K-Cores dans les Graphes  

#### Objectif du Code  
Ce script utilise une matrice d'adjacence pour explorer les propriétés structurelles du graphe et identifie différents sous-graphe. 


#### Utilisation du Code  

1. Assurez-vous de disposer de la matrice d'adjacence au format Excel (`adjacency_matrix_V2.xlsx`).  
2. Exécutez le script Python.  
3. Le programme fournira des informations sur :  
   - Les propriétés générales du graphe (nœuds, arêtes, densité, distance géodésique moyenne).  
   - Les cliques 
   - Les n-cliques
   - Les clans 
   - Les k-cores 



#### Packages à Installer  

Avant d'exécuter le script, installez les packages suivants via `pip` :  
- `pandas` : Manipulation de la matrice d'adjacence.  
- `networkx` : Analyse et visualisation des graphes.  
- `collections` : Pour les compteurs (Counter).

___

## B.Analyse_similarités

###  Analyse de Similarité globale :  Probabilités Stationnaires et Clusters  

#### Objectif du Code  
Ce script calcule les probabilités stationnaires d'un graphe basé sur une matrice de transition aléatoire.  
Il identifie également les **clusters** du graphe et calcule la somme des probabilités stationnaires pour chaque cluster.  

Ces analyses permettent de :  
- Identifier les nœuds les plus influents selon leur probabilité stationnaire.  
- Comprendre la distribution des probabilités dans les différents clusters.


#### Utilisation du Code  

1. Assurez-vous de disposer des fichiers nécessaires :  
   - `nodes.xlsx` : Contient les informations sur les nœuds du graphe (ID et Label).  
   - `random_walk_transition_matrix.xlsx` : Matrice de transition pour le calcul des probabilités stationnaires.  
   - `dico_clusters_links` : Fichier JSON contenant la répartition des nœuds par cluster.  

2. Exécutez le script Python.  

3. Les résultats suivants seront générés :  
   - `stationary_probabilities.xlsx` : Classement des nœuds selon leur probabilité stationnaire.  
   - `cluster_stationary_probabilities.xlsx` : Somme des probabilités stationnaires pour chaque cluster.  



#### Packages à Installer  

Avant d'exécuter le script, installez les packages suivants via `pip` :  

- `pandas` : Manipulation des données tabulaires.  
- `numpy` : Calcul des valeurs et vecteurs propres.  
- `json` : Manipulation des fichiers JSON.  

___
###  Analyses de Similarité locale

#### Objectif du Code  
Ce script réalise différentes analyses de similarité entre les nœuds d'un graphe basé sur :  
- **Cosine Similarity** : Calcul des similarités cosinus entre les nœuds.  
- **Préférence Attachée** : Mesure de la probabilité qu'un lien soit formé en fonction des degrés des nœuds.  
- **Voisins Communs** : Identification des paires de nœuds partageant un nombre significatif de voisins communs.  
- **Analyse Combinée** : Intégration de plusieurs similarités avec vérification des clusters.  

Le script génère des résultats exploitables sous forme de fichiers Excel pour visualiser et analyser les similarités et les relations entre nœuds.



#### Utilisation du Code  

1. **Fichiers nécessaires** :  
   - `similarity_cosine.xlsx` : Matrice de similarité cosinus.  
   - `similarity_preferential_attachment.xlsx` : Matrice de préférence attachée.  
   - `similarity_common_neighbors.xlsx` : Matrice des voisins communs.  
   - `nodes.xlsx` : Liste des nœuds avec leurs identifiants et labels.  
   - `dico_clusters_links` : Fichier JSON contenant les clusters.  

2. **Étapes d'exécution** :  
   - Exécutez le script Python après avoir configuré les chemins vers les fichiers.  
   - Le programme produira plusieurs fichiers Excel avec les résultats de chaque analyse.  



#### Packages à Installer  

Avant d'exécuter le script, installez les packages suivants via `pip` :  

- `pandas` : Manipulation des données tabulaires.  
- `numpy` : Calcul des valeurs numériques.  
- `json` : Manipulation des fichiers JSON.  

___

### Matrices de similarités

#### Objectif du Code  
Ce script réalise des calculs de **similarité locale** et **globale** sur les nœuds d'un graphe en utilisant une matrice d'adjacence.  
Il génère des matrices de similarité et exporte les résultats sous forme de fichiers Excel pour des analyses ultérieures.



#### Utilisation du Code  

1. **Fichier nécessaire** :  
   - `adjacency_matrix_V2.xlsx` : Matrice d'adjacence du graphe.  

2. **Étapes d'exécution** :  
   - Configurez le chemin vers la matrice d'adjacence dans le script.  
   - Exécutez le script Python.  
   - Les matrices de similarité seront exportées sous forme de fichiers Excel dans le dossier spécifié.  



#### Packages à Installer  

Avant d'exécuter le script, installez les packages suivants via `pip` :  

-`math` : Opération mathématique 
- `numpy` : Calcul matriciel et algébrique.  
- `pandas` : Manipulation des données tabulaires et export des matrices.  
- `scipy` : Calculs scientifiques et manipulation des matrices creuses.  

---
## C.Distances_euclidiennes

### Analyse des Clusters et Distances Euclidiennes  

#### Objectif du Code  
Ce script effectue une analyse des clusters basés sur leurs coordonnées géographiques (`X`, `Y`) et leur modularité.  
Il génère :  
1. Un graphique représentant les clusters avec des cercles proportionnels à leurs rayons.  
2. Une matrice des distances euclidiennes entre les centres des clusters.  



#### Utilisation du Code  

1. **Fichier nécessaire** :  
   - `Linkclusters_info.csv` : Contient les informations des clusters, y compris les coordonnées (`X`, `Y`) et les classes de modularité (`modularity_class`).  

2. **Étapes d'exécution** :  
   - Chargez le fichier CSV contenant les informations des clusters.  
   - Exécutez le script Python.  
   - Les résultats suivants seront générés :  
     - Un graphique des clusters.  
     - Un fichier Excel contenant les distances entre les clusters (`cluster_distance_matrix.xlsx`).  


#### Packages à Installer  

Avant d'exécuter le script, installez les packages suivants via `pip` :  

- `pandas` : Manipulation des données tabulaires.  
- `matplotlib` : Visualisation des clusters.  
- `itertools` : Combinaisons pour le calcul des distances.  
- `math` : Calcul des distances euclidiennes.  



---
# Partie : Text Analysis
---
## Analyse Temporelle  ( `Analyse_temporelle.py` )

#### Objectif du Code  
Ce code a pour objectif d'analyser l'historique d'un article fourni et de représenter, sous forme de graphique, l'évolution des tokens pertinents les plus fréquents sur une période déterminée.



#### Utilisation du Code  
1. Exécutez le script Python.  
2. Lorsque le programme le demande, fournissez le lien de l'article à analyser.



#### Sources  
Le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :  
- [Tutoriel](https://www.youtube.com/watch?v=TKjjlp5_r7o)


#### Packages à Installer  
Avant d'exécuter le code, assurez-vous que les packages suivants sont installés. Vous pouvez les installer via `pip` si nécessaire :  
- **numpy** : Calculs numériques  
- **gensim** : Analyse de texte avancée  
- **Spacy** : Traitement de langage naturel  
- **NLTK** : (Natural Language Toolkit) pour l'analyse textuelle  
- **requests** : Requêtes HTTP pour récupérer des données  
- **PyLDAvis** : Visualisation des modèles de sujets (LDA)  
- **BeautifulSoup (BS4)** : Scraping de données HTML  
- **pandas** : Manipulation de données  
- **matplotlib** : Création de graphiques  
- **datetime** : Manipulation de dates et d'horaires 

---
## Analyse_Semantique 

#### Objectif du Code
Ce code réalise une **analyse sémantique** basée sur le fichier JSON contenant les citations nettoyées. Voici les principales étapes effectuées par le script :  
1. Analyse de chaque citation pour chaque personne dans le fichier JSON, phrase par phrase.  
2. Calcul d'un **score sémantique** (compris entre -1 et 1) pour chaque phrase.  
3. Classification des citations en **positives**, **négatives**, ou **neutres**.  
4. Calcul du **score final** pour l'ensemble des citations de chaque personne, avec une évaluation du **caractère général** (positif, négatif ou neutre).  
5. Enregistrement des résultats dans un fichier **JSON** pour une analyse ultérieure.  

#### Utilisation du Code
1. Assurez-vous de disposer du fichier JSON contenant les citations nettoyées.  
2. Exécutez le script Python.  
3. Le script analysera les citations et générera un fichier JSON contenant :  
   - Le nombre total de citations positives, négatives, ou neutres pour chaque personne.  
   - Le score final et le caractère général des citations de chaque personne.  

#### Package à Installer
Avant d'exécuter le script, installez le package suivant à l'aide de `pip` si nécessaire :  
- **vaderSentiment** : Pour effectuer l'analyse sémantique des phrases.  



---
## BBC_ranking

#### Objectif du Code
Ce code analyse le fichier généré par le script **Collection_de_BBC** pour établir un classement des termes les plus abordés au cours d'une année précise. Les résultats sont présentés sous forme d'un tableau évolutif.

#### Utilisation du Code
1. Assurez-vous d'avoir exécuté le script **Collection_de_BBC** au préalable pour générer le fichier de données.
2. Exécutez ce script et fournissez :
   - Le nom du fichier CSV généré par **Collection_de_BBC**.
   - L'année à analyser.
3. Notez que les articles publiés avant 2023 sont moins catégorisés sur BBC News, ce qui peut affecter la qualité de l'analyse.

#### Packages à Installer
Avant d'exécuter le code, installez les packages suivants via `pip` si nécessaire :

- **ast** : Manipulation des structures de données littérales en Python.
- **matplotlib** : Création de graphiques.
- **seaborn** : Visualisations statistiques avancées.
- **pandas** : Manipulation des données.

---

## Class_Wiki 

#### Objectif du Code
Ce code a pour objectif de regrouper les **sous-classes** issues du fichier Excel généré précédemment en **30 classes principales**. Cela permet de passer d'une granularité fine (sous-classes) à une classification plus générale.  
Une nouvelle colonne intitulée **"Classes"** sera ajoutée au fichier Excel, représentant la classification générale correspondant à chaque sous-classe.

#### Utilisation du Code
1. Assurez-vous d'avoir le fichier Excel généré précédemment contenant les sous-classes.  
2. Exécutez le script Python.  
3. Le script analysera les sous-classes et les répartira dans l'une des 30 classes principales, en ajoutant une colonne **"Classes"** au fichier Excel.

#### Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **pandas** : Pour manipuler les données du fichier Excel.  
- **scikit-learn** : Pour la classification des sous-classes en classes principales.  
- **SentenceTransformer** : Pour l'encodage des sous-classes en vecteurs permettant leur regroupement. 
---
## Clustering 

#### Objectif du Code
Ce code utilise un fichier **CSV** contenant une liste de 100 liens Wikipédia en entrée et génère en sortie un fichier **HTML** représentant les différents clusters du corpus. Le modèle de clustering utilisé est l'**allocation latente de Dirichlet (LDA)**.

#### Utilisation du Code
1. Préparez un fichier **CSV** contenant vos 100 liens Wikipédia.
2. Exécutez le script et fournissez le nom du fichier CSV lorsque le programme le demande.
3. Le script générera un fichier **HTML** que vous pourrez ouvrir dans n'importe quel navigateur pour visualiser les clusters.

#### Sources
Ce code s'inspire fortement des deux vidéos suivantes :
- [Tutoriel 1](https://www.youtube.com/watch?v=TKjjlp5_r7o)
- [Tutoriel 2](https://www.youtube.com/watch?v=UEn3xHNBXJU&t=935s)

#### Packages à Installer
Avant de lancer le script, assurez-vous que les packages suivants sont installés. Vous pouvez les installer avec `pip` si nécessaire :

- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée et modélisation thématique.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **requests** : Requêtes HTTP pour récupérer des données.
- **PyLDAvis** : Visualisation des modèles LDA.
- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **pandas** : Manipulation de données.

---
## Co-occurrence 

#### Objectif du Code
Ce code prend un article Wikipédia en entrée et génère un tableau de co-occurrence des 5 tokens les plus fréquents dans l'article.

#### Utilisation du Code
1. Lancez le script Python.
2. Fournissez le lien de l'article Wikipédia lorsque le programme le demande.
3. Le script analysera l'article et affichera un tableau de co-occurrence des tokens les plus fréquents.

#### Sources
le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :
- [Tutoriel](https://www.youtube.com/watch?v=TKjjlp5_r7o)


#### Packages à Installer
Assurez-vous que les packages suivants sont installés avant d'exécuter le script. Vous pouvez les installer avec `pip` si nécessaire :

- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **requests** : Requêtes HTTP pour récupérer des données.
- **pandas** : Manipulation de données.
- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **PyLDAvis** : Visualisation des modèles thématiques (LDA).

---
## Extraire_Subclass 

#### Objectif du Code
Ce code a pour objectif d'extraire les **sous-classes** associées à chaque article Wikipédia en se basant sur les données disponibles dans l'onglet Wikidata. Voici les étapes principales effectuées par le script :  
1. Transformation des liens Wikipédia du fichier Excel en liens Wikiquote.  
2. Extraction des sous-classes à partir des liens transformés.  
3. Ajout d'une nouvelle colonne intitulée **"subclass"** dans le fichier Excel original, contenant la sous-classe correspondant à chaque article Wikipédia.

#### Utilisation du Code
1. Assurez-vous d'avoir le fichier **`nodes.xlsx`** généré dans la partie "Link Analysis".  
2. Exécutez le script Python.  
3. Le script transformera les liens, effectuera l'extraction des sous-classes, et mettra à jour le fichier Excel avec une colonne supplémentaire.  

#### Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **requests** : Pour envoyer des requêtes HTTP aux serveurs.  
- **BeautifulSoup (BS4)** : Pour effectuer le scraping des données HTML.  
- **pandas** : Pour la manipulation et la mise à jour du fichier Excel.  

 ## Texte_Nettoyage

#### Objectif du Code
Ce code a pour objectif de **nettoyer les citations** précédemment extraites. Il supprime tous les éléments non pertinents, tels que :  
- Les sources  
- Les pages  
- Les dates  
- Les volumes  
- Les chapitres  
- Et d'autres informations inutiles.  

À l'issue du nettoyage, le script enregistre les citations nettoyées dans un nouveau fichier au format **JSON**.

#### Utilisation du Code
1. Assurez-vous de disposer du fichier JSON contenant les citations brutes extraites à l'aide du script précédent.  
2. Exécutez le script Python.  
3. Le code nettoiera les citations et enregistrera les résultats dans un nouveau fichier JSON.  

## Packages à Installer
Avant d'exécuter le script, assurez-vous que les packages suivants sont installés :  
- **pandas** : Pour la manipulation des données structurées.  
- **json** : Pour lire et écrire les fichiers JSON. (Généralement inclus avec Python.)  


---
## Treemap

#### Objectif du Code
Ce code a pour objectif de générer une **treemap** des différentes classes associées à nos liens Wikipédia.  
La treemap offre une visualisation claire et intuitive de la répartition des classes, en mettant en évidence leur fréquence relative.

#### Utilisation du Code
1. Assurez-vous de disposer d'un fichier contenant les classes associées à vos liens Wikipédia.  
2. Exécutez le script Python.  
3. Le script générera une **treemap** qui permettra d'observer la répartition des classes en fonction de leur fréquence.  

#### Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **plotly_express** : Pour générer la treemap.  
- **pandas** : Pour manipuler les données en entrée.  
---


## Wikiquote 

#### Objectif du Code
Ce code exploite les **16 clusters** identifiés lors de la "link analysis" et sélectionne une **personnalité publique** représentative pour chacun de ces clusters. Voici les étapes principales du processus :  
1. À partir des liens Wikipédia des personnalités sélectionnées, le code génère leurs liens Wikiquote.  
2. Il accède à l'onglet Wikiquote correspondant et extrait uniquement le **corpus** de la page, c'est-à-dire leurs **citations** et **discours**, en excluant les titres, sous-titres, etc.  
3. Le contenu extrait est ensuite stocké dans un **dictionnaire** au format JSON, où chaque clé est l'URL Wikipédia de la personnalité, et chaque valeur contient l'ensemble de ses citations.

#### Utilisation du Code
1. Assurez-vous d'avoir accès aux liens Wikipédia des personnalités publiques des 16 clusters identifiés.  
2. Exécutez le script Python.  
3. Le code générera un fichier JSON contenant les citations de chaque personnalité, organisées par leur URL Wikipédia.  

#### Packages à Installer
Avant d'exécuter le script, installez les packages suivants à l'aide de `pip` si nécessaire :  
- **requests** : Pour récupérer le contenu HTML des pages Wikiquote.  
- **BeautifulSoup (BS4)** : Pour extraire le corpus à partir du code HTML des pages Wikiquote.  

---
## Word_cloud 

#### Objectif du Code
Ce code génère un **nuage de mots** (word cloud) basé sur les tokens les plus importants d'un article Wikipédia donné en entrée.

#### Utilisation du Code
1. Fournissez un lien vers un article Wikipédia lorsque le programme le demande.
2. Si le lien est un lien Wikipédia standard, exécutez le code tel quel.
3. Si le lien provient de **Wikiquote**, remplacez le `"p"` par `"ul"` à la ligne 38 du script avant de l'exécuter.
4. Le code génèrera un nuage de mots des tokens les plus pertinents.

#### Sources
le traitement des tokens de ce code s'inspire fortement de la vidéo suivante :
- [Tutoriel 1](https://www.youtube.com/watch?v=TKjjlp5_r7o)

La création du nuage de mot à été très fortement inspirée par la vidéo suivante : 

- [Tutoriel 2](https://www.youtube.com/watch?v=HcKUU5nNmrs)


#### Packages à Installer
Avant d'exécuter le script, assurez-vous que les packages suivants sont installés. Vous pouvez les installer via `pip` si nécessaire :

- **BeautifulSoup (BS4)** : Scraping de données HTML.
- **requests** : Requêtes HTTP pour récupérer des données.
- **pandas** : Manipulation de données.
- **numpy** : Calculs numériques.
- **gensim** : Analyse de texte avancée.
- **spacy** : Traitement de langage naturel.
- **nltk** : (Natural Language Toolkit) pour l'analyse textuelle.
- **PyLDAvis** : Visualisation des modèles thématiques (LDA).
- **Wordcloud** : Génération de nuages de mots.
